"""Discovery source/assembly contracts; runtime assertions live in discovery_lab.gd.

These tests do not prove that generated classes follow the rules or that children learn.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.course import ROOT, build_input, read_lesson, read_text, section

FOCUSED = ('B06', 'B08', 'B13', 'C10', 'D07')
STEPS = ('先留一个问题', '你来选一个验证', '试过再解释', '把发现带走')


class DiscoveryThreadTests(unittest.TestCase):
    def test_discovery_is_authored_in_lessons_and_reaches_both_inputs(self):
        for ident in FOCUSED:
            with self.subTest(lesson=ident):
                row = read_lesson(ident)
                focus = section(row['body'], '这次多看一层').split('<details', 1)[0].strip()
                offsets = []
                for label in STEPS:
                    token = '**' + label + '：**'
                    self.assertEqual(focus.count(token), 1)
                    offsets.append(focus.index(token))
                self.assertEqual(offsets, sorted(offsets))
                self.assertIn('给AI的引导', focus)
                for purpose in ('experience', 'project'):
                    text, _ = build_input(ident, purpose=purpose)
                    self.assertIn(focus, text)
                    self.assertIn('情绪不评分', text)
                    self.assertEqual(text.count('## 讲给爸爸听'), 1)
                    if purpose == 'experience':
                        self.assertNotIn('data-purpose="project"', text)

    def test_no_new_objectives_quiz_ids_or_prerequisite_gates(self):
        prerequisites = {'B06': ['B05', 'A04'], 'B08': ['B07'], 'B13': ['B12'],
                         'C10': ['C06'], 'D07': ['C12', 'C04', 'C06', 'C02']}
        for ident in FOCUSED:
            with self.subTest(lesson=ident):
                row = read_lesson(ident)
                self.assertEqual(row['meta']['prerequisites'], prerequisites[ident])
                self.assertEqual(row['questions'], [ident+'-P1', ident+'-D2', ident+'-T3', ident+'-K4'])
                self.assertEqual([k for k, v in row['objectives'].items() if v['level'] == 'M'],
                                 [ident+'.M1', ident+'.M2'])
                self.assertIn('不新增一轮作业', row['body'])
        elective = read_lesson('E06')
        self.assertFalse(elective['meta']['labs'])
        self.assertTrue(all(v['level'] == 'K' for v in elective['objectives'].values()))

    def test_shared_skill_does_not_require_aha_or_hide_help(self):
        skill = read_text(ROOT / 'openmaic/skills/ai3d-self-study/SKILL.md')
        for phrase in ('初始只展示', '不无限追问', '情绪不评分', '不暗中破坏作品',
                       '先听他的关系', '不替他说'):
            # Two equivalent forms are accepted for the help and attribution constraints.
            if phrase == '不无限追问':
                self.assertIn('不靠无限追问', skill)
            elif phrase == '不替他说':
                self.assertIn('不要替他说', skill)
            else:
                self.assertIn(phrase, skill)
        self.assertIn('B13、D07的初始学生页面', skill)
        self.assertIn('已有解释可查', skill)

    def test_controls_and_native_suite_are_connected(self):
        lab = read_text(ROOT / 'practice/godot/labs/event_lab.gd')
        for control in ('counter', 'visual', 'mechanism', 'guard'):
            self.assertIn('toggle("' + control + '"', lab)
        self.assertIn('var mechanism_visible := false', lab)
        self.assertIn('history.append(', lab)
        native = read_text(ROOT / 'practice/godot/tests/discovery_lab.gd')
        self.assertIn('extends "res://tests/practical_labs.gd"', native)
        self.assertIn('DISCOVERY LAB PASS', native)
        runner = read_text(ROOT / 'tools/lib/checks/run_production_checks.py')
        self.assertIn("('discovery_lab','DISCOVERY LAB PASS')", runner)

    def test_actual_lab_boundary_is_in_the_course(self):
        b06 = read_lesson('B06')['body']
        b08 = read_lesson('B08')['body']
        self.assertIn('只有一枚物品', b06)
        self.assertIn('没有同步重入或第二层防重开关', b06)
        self.assertIn('没有0/1/3目标选择器', b08)
        self.assertIn('最近12条', b06)
        self.assertIn('test_discovery_thread.py', read_text(ROOT / 'docs/modeling-thread.md'))


if __name__ == '__main__':
    unittest.main()
