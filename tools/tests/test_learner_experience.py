"""Course/assembly/UI-text contracts only; no model or child-psychology evaluation."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.course import ROOT, ORDER, read_lesson, read_text, build_input, catalog, short_card, teacher_section
import learn


class LearnerExperienceTests(unittest.TestCase):
    def test_each_lesson_has_one_specific_source_authored_opening(self):
        entries = []
        for ident in ORDER:
            with self.subTest(lesson=ident):
                row = read_lesson(ident)
                entries.append(row['entry'])
                self.assertEqual(row['body'].count('**先从这里开始：**'), 1)
                self.assertTrue(20 < len(row['entry']) < 180)
                head, detail = row['body'].split('<details data-audience="reference">', 1)
                self.assertIn(row['entry'], head)
                self.assertIn('**带学提醒（按当前需要使用）：**', detail)
                self.assertNotIn('## 这次多看一层', head)
                self.assertNotIn('**核对要点：**', row['body'])
                for purpose in ('experience', 'project'):
                    text, hashes = build_input(ident, purpose=purpose)
                    self.assertIn(row['entry'], text)
                    self.assertIn('带学提醒', text)
                    self.assertEqual(set(hashes), {'lesson', 'teacher', 'memory', 'skill'})
        self.assertEqual(len(set(entries)), len(ORDER))

    def test_learner_card_starts_with_own_task_not_demo_or_recall(self):
        _, cards, bindings, order = catalog()
        for ident in order:
            with self.subTest(lesson=ident):
                card = short_card(ident, cards, bindings)
                opening = card.split('<details>', 1)[0]
                self.assertIn(read_lesson(ident)['entry'], opening)
                self.assertNotIn(cards[ident][1], opening)
                self.assertNotIn('核对要点', opening)
                self.assertNotIn('记忆项', opening)
                self.assertEqual(card.count('## 讲给爸爸听'), 1)
                self.assertEqual(card.count('<details>'), card.count('</details>'))
                self.assertLess(len(card), 1600)

    def test_current_card_does_not_start_with_old_gaps(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            target = learn.start(Path(d)/'private', 'B13')
            text = target.read_text(encoding='utf-8')
            opening = text.split('<details>', 1)[0]
            self.assertIn(read_lesson('B13')['entry'], opening)
            self.assertNotIn('下次先回想', opening)
            self.assertNotIn('TH01', opening)
            self.assertLess(text.index('今天先试'), text.index('需要时回看旧问题'))
            self.assertEqual(text.count('<details>'), text.count('</details>'))
            self.assertFalse((target.parent/'state.md').exists())

    def test_shared_feedback_is_loaded_and_hashed_for_each_lesson(self):
        header = read_text(ROOT/'course/teacher-notes.md').partition('\n## ')[0].strip()
        for ident in ORDER:
            with self.subTest(lesson=ident):
                self.assertIn(header, teacher_section(ident))
                self.assertIn(header, build_input(ident)[0])
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            root = Path(d)
            for folder in ('course', 'openmaic', 'practice'):
                shutil.copytree(ROOT/folder, root/folder,
                                ignore=shutil.ignore_patterns('.godot', 'output', '__pycache__'))
            _, before = build_input('A04', root=root)
            notes = root/'course/teacher-notes.md'
            notes.write_text(notes.read_text(encoding='utf-8').replace(
                '只读当前课，先看学员真实回应。', '只读当前课，先看学员真实回应。\n新增教师约定。', 1), encoding='utf-8')
            _, after = build_input('A04', root=root)
            self.assertNotEqual(before['teacher'], after['teacher'])
            self.assertEqual(before['lesson'], after['lesson'])
            self.assertEqual(before['skill'], after['skill'])
            # Unrelated feedback still does not invalidate a selected course.
            notes.write_text(notes.read_text(encoding='utf-8')+'\nE07 supplemental test text.\n', encoding='utf-8')
            self.assertEqual(after, build_input('A04', root=root)[1])

    def test_no_new_gate_or_mental_state_classifier(self):
        skill = read_text(ROOT/'openmaic/skills/ai3d-self-study/SKILL.md')
        for wording in ('直接解释', '不让他先答对', '不由沉默', '不假称同步OpenMAIC',
                        '情绪不评分', '爸爸是陪学伙伴', 'learning-to-learn'):
            self.assertIn(wording, skill)
        self.assertLess(len(skill), 2000)
        elective = read_lesson('E06')
        self.assertFalse(elective['meta']['labs'])
        self.assertTrue(all(x['level']=='K' for x in elective['objectives'].values()))
        self.assertNotIn('动手试一项', elective['body'])
        self.assertNotIn('请在自己的副本中写回场景', elective['body'])
        self.assertIn('正常保存与读取，再逐项', read_lesson('C11')['binding'][1])
        self.assertEqual(len(catalog()[0]), 147)


if __name__ == '__main__':
    unittest.main()
