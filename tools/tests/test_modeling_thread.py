"""Source/assembly regression checks, not a claim of instructional effectiveness."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.course import ROOT, build_input, read_lesson, read_text, section

ANCHORS = ('A03', 'A05', 'B06', 'B08', 'B13', 'C05', 'C10', 'D07')


class ModelingThreadTests(unittest.TestCase):
    def test_anchor_is_authored_once_and_reaches_both_inputs(self):
        for ident in ANCHORS:
            with self.subTest(lesson=ident):
                row = read_lesson(ident)
                self.assertEqual(row['body'].count('## 这次多看一层\n'), 1)
                focus = section(row['body'], '这次多看一层')
                focus = focus.split('<details', 1)[0].strip()
                self.assertTrue(focus)
                self.assertIn('给AI的引导', focus)
                for purpose in ('experience', 'project'):
                    text, hashes = build_input(ident, purpose=purpose)
                    self.assertIn(focus, text)
                    self.assertEqual(text.count('## 讲给爸爸听'), 1)
                    self.assertEqual(set(hashes), {'lesson', 'teacher', 'memory', 'skill'})
                    if purpose == 'experience':
                        self.assertNotIn('data-purpose="project"', text)

    def test_revisits_connect_examples_without_new_prerequisites(self):
        required = {
            'B06': {'A03', 'A05'},
            'B08': {'A03', 'A05', 'B06'},
            'B13': {'B08'},
            'C05': {'B06', 'B08'},
            'C10': {'B06', 'B08', 'C05'},
            'D07': {'B08', 'B13', 'C05', 'C10'},
        }
        for ident, links in required.items():
            with self.subTest(lesson=ident):
                self.assertTrue(links.issubset(set(read_lesson(ident)['meta']['revisit'])))

    def test_c05_has_actual_runtime_sample_not_just_materials(self):
        row = read_lesson('C05')
        path = 'practice/godot/scenes/main.tscn'
        self.assertIn(path, row['meta']['labs'])
        self.assertTrue((ROOT / path).is_file())
        self.assertIn('TH04', row['meta']['memory'])

    def test_independent_opening_is_present_in_generation_contract(self):
        # Presence checks cannot prove that a generated classroom obeys the contract.
        skill = read_text(ROOT / 'openmaic/skills/ai3d-self-study/SKILL.md')
        self.assertIn('B13、D07', skill)
        self.assertIn('初始学生页面', skill)
        for ident in ('B13', 'D07'):
            row = read_lesson(ident)
            self.assertIn('先让我提出第一步', row['body'])
            text, _ = build_input(ident)
            self.assertIn('先让我提出第一步', text)

    def test_original_assessment_surface_and_e06_scope_remain(self):
        for ident in ANCHORS:
            row = read_lesson(ident)
            self.assertEqual(len(row['questions']), 4)
            self.assertEqual(
                [key for key, value in row['objectives'].items() if value['level'] == 'M'],
                [ident + '.M1', ident + '.M2'],
            )
        elective = read_lesson('E06')
        self.assertFalse(elective['meta']['labs'])
        self.assertTrue(all(value['level'] == 'K' for value in elective['objectives'].values()))

    def test_author_map_links_to_actual_lesson_sources(self):
        guide = read_text(ROOT / 'docs/modeling-thread.md')
        for ident in ANCHORS:
            self.assertIn('../course/lessons/' + ident + '.md', guide)
        design = read_text(ROOT / 'docs/design.md')
        self.assertIn('(modeling-thread.md)', design)


if __name__ == '__main__':
    unittest.main()
