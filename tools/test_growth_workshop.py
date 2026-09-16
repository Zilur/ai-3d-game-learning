"""Constructed fixtures only; no child trial or commercial quality certification."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import growth_workshop as g


class GrowthWorkshopTests(unittest.TestCase):
    def test_six_stages_and_known_lessons(self):
        rows = g.load_plan()
        self.assertEqual(tuple(r['key'] for r in rows), g.STAGES)
        self.assertTrue(all(set(r['lessons']) <= g.LESSONS for r in rows))

    def test_invalid_schema_and_stage_rejected(self):
        data = {'schema_version': 1, 'stages': g.load_plan()}
        for change in ('version', 'unknown', 'duplicate', 'missing', 'boolean', 'bad-list'):
            bad = copy.deepcopy(data)
            if change == 'version': bad['schema_version'] = 2
            if change == 'boolean': bad['schema_version'] = True
            if change == 'unknown': bad['stages'][0]['lessons'] = ['Z99']
            if change == 'duplicate': bad['stages'][1]['key'] = 'independent'
            if change == 'missing': del bad['stages'][0]['stop']
            if change == 'bad-list': bad['stages'][0]['evidence'] = 'passed'
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root = Path(d); p = root / g.PLAN; p.parent.mkdir(parents=True)
                p.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaises(ValueError): g.load_plan(root)

    def test_each_session_retains_honesty_and_child_agency(self):
        for row in g.load_plan():
            with self.subTest(stage=row['key']):
                text = g.render(row, 'fixture')
                for required in ('待验证', '是否提示根因', '未见迁移', '不叠加全套题', '不天然', '已登记能力', '停止条件'):
                    self.assertIn(required, text)
                self.assertNotIn('[x]', text)
                self.assertIn(row['question'], text)
                self.assertIn(row['stop'], text)

    def test_teacher_input_is_explicit_and_not_a_classroom(self):
        text = g.render(g.load_plan()[0], 'teacher-fixture', openmaic=True)
        self.assertTrue(text.startswith('# 教师生成输入'))
        self.assertIn('生成后实测控件', text)
        self.assertIn('不附私人记录', text)

    def test_release_and_maintenance_link_release_check(self):
        for row in g.load_plan()[-2:]:
            self.assertIn('templates/release-readiness.md', g.render(row, 'fixture'))

    def test_unsafe_cycle_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            home = Path(d) / 'notes'
            for cycle in ('../escape', '/root', 'a/b', '', 'a' * 61, 'x\n## pass'):
                with self.subTest(cycle=cycle), self.assertRaises(ValueError):
                    g.write_new(home, cycle, 'test', Path(d))
            self.assertFalse(home.exists())

    def test_public_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for path in (root, root / 'notes', root / '.learning', root / '.learning-lookalike/private'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    g.write_new(path, 'fixture', 'test', root)

    def test_private_output_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); home = root / '.learning/growth'
            result = g.write_new(home, 'fixture', 'first', root)
            self.assertEqual(result.read_text(), 'first')
            with self.assertRaises(FileExistsError): g.write_new(home, 'fixture', 'second', root)
            self.assertEqual(result.read_text(), 'first')

    def test_symlink_dir_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'public').mkdir(); (root / '.learning').mkdir()
            link = root / '.learning/growth'
            link.symlink_to(root / 'public', target_is_directory=True)
            with self.assertRaises(ValueError): g.write_new(link, 'fixture', 'test', root)
            self.assertEqual(list((root / 'public').iterdir()), [])

    def test_symlink_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); home = root / '.learning/growth'; home.mkdir(parents=True)
            target = root / 'original.md'; target.write_text('keep')
            (home / 'fixture.md').symlink_to(target)
            with self.assertRaises(FileExistsError): g.write_new(home, 'fixture', 'replace', root)
            self.assertEqual(target.read_text(), 'keep')

    def test_external_private_folder_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'; root.mkdir()
            p = g.write_new(Path(d) / 'private', 'fixture', 'test', root)
            self.assertEqual(p.read_text(), 'test')

    def test_size_limit(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                g.write_new(Path(d) / '.learning/growth', 'fixture', '界' * g.MAX_BYTES, Path(d))

    def test_plan_is_read_only(self):
        with patch.object(g, 'write_new', side_effect=AssertionError('unexpected write')):
            self.assertEqual(g.main(['plan']), 0)

    def test_does_not_read_private_history(self):
        row = g.load_plan()[0]
        original = Path.read_text
        def guarded(path, *args, **kwargs):
            self.assertNotIn('.learning', path.parts)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', guarded):
            self.assertIn('不含个人历史', g.render(row, 'fixture'))


if __name__ == '__main__':
    unittest.main()
