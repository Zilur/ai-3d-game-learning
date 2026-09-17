"""Constructed fixtures only; these tests never contact OpenMAIC or a real learner."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import family_learning as f
import openmaic_handoff as h
from test_family_learning import report, OBJ, NOW

class HandoffTests(unittest.TestCase):
    def test_empty_has_no_invented_mastery(self):
        text = h.build_context(f.new_state(), OBJ, 'A04', NOW)
        self.assertIn('"current_lesson_gaps": []', text)
        self.assertIn('"due_review": []', text)
        self.assertNotIn('reports', text)
        self.assertIn('不是OpenMAIC原生导入格式', text)

    def test_specific_gap_without_private_paths(self):
        state = f.new_state(); r = report(score=1, support='L2')
        r['items'][0]['diagnosis']['basis'] = '本次混淆外观与碰撞 /Users/child/private.txt a@example.com'
        f.add_report(state, r, OBJ, NOW)
        text = h.build_context(state, OBJ, 'A04', NOW)
        self.assertIn('本次混淆', text)
        self.assertIn('L2', text)
        self.assertNotIn('/Users/', text)
        self.assertNotIn('a@example.com', text)
        self.assertNotIn('"reports"', text)

    def test_unknown_lesson(self):
        with self.assertRaises(ValueError): h.build_context(f.new_state(), OBJ, '../other', NOW)

    def test_preview_readonly_confirm_nonoverwriting(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            root = Path(d) / 'source'; root.mkdir()
            home = Path(d) / 'private'; home.mkdir(); f.save_state(home, f.new_state())
            before = (home/'state.md').read_bytes()
            with patch.object(f, 'catalog', return_value=(OBJ, {}, {}, ['A04'])):
                text, path = h.export_context(home, 'A04', root=root)
                self.assertIsNone(path)
                self.assertEqual(set(p.name for p in home.iterdir()), {'state.md'})
                _, path = h.export_context(home, 'A04', confirm=True, root=root)
                self.assertEqual(path.read_text(encoding='utf-8'), text)
                with self.assertRaises(FileExistsError): h.export_context(home, 'A04', confirm=True, root=root)
            self.assertEqual((home/'state.md').read_bytes(), before)

    def test_public_home_refused(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            root = Path(d); public = root/'openmaic'; public.mkdir()
            with self.assertRaises(ValueError): h.private_directory(public, root)

    def test_write_lock_refused(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home = Path(d); (home/'.write-lock').touch()
            with self.assertRaises(ValueError): h.private_directory(home, home/'other')

    def test_original_openmaic_mode_stays_private_free(self):
        source = (h.ROOT/'tools/family_learning.py').read_text(encoding='utf-8')
        self.assertIn('仅供教师生成课堂，不含私人学习记录。', source)
        self.assertNotIn('openmaic_handoff', source)

if __name__ == '__main__': unittest.main()
