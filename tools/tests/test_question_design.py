"""Authored item/assembly contracts, not empirical difficulty or child assessment."""
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.course import ROOT, ORDER, read_lesson, read_text, section, teacher_section, build_input, catalog

ITEM = r'(?:[A-E]\d{2}-[PDTK]\d+|KN\d+-[PT]|K\d+)'


def bands(text):
    """Reject unlabeled, multiply labeled, or unrecognized authored item bands."""
    result = {}
    for match in re.finditer(r'^### (' + ITEM + r')\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S):
        ident, body = match.groups()
        labels = re.findall(r'^\*\*预设层次：\*\* (基础|扩展候选)；', body, re.M)
        if len(labels) != 1 or body.count('**预设层次：**') != 1 or ident in result:
            raise ValueError('Invalid or duplicate item band: ' + ident)
        result[ident] = labels[0]
    return result


class QuestionDesignTests(unittest.TestCase):
    def test_all_existing_core_and_supplemental_questions_have_one_band(self):
        text = read_text(ROOT/'course/teacher-notes.md')
        expected = set()
        for ident in ORDER:
            row = read_lesson(ident)
            qids = set(row['questions']) | set(re.findall(
                r'^### ((?:KN\d+-[PT]|K\d+))｜', row['body'], re.M))
            actual = bands(section(text, ident))
            self.assertEqual(set(actual), qids, ident)
            expected |= qids
        self.assertEqual(set(bands(text)), expected)
        self.assertEqual(len(expected), 264)
        self.assertEqual(len(catalog()[0]), 147)

    def test_missing_or_unknown_band_is_not_silently_accepted(self):
        text = section(read_text(ROOT/'course/teacher-notes.md'), 'A02')
        for changed in (text.replace('**预设层次：** 基础；', '', 1),
                        text.replace('**预设层次：** 基础；', '**预设层次：** 困难；', 1)):
            with self.assertRaises(ValueError):
                bands(changed)

    def test_type_does_not_imply_difficulty_and_e06_stays_purpose_only(self):
        actual = bands(read_text(ROOT/'course/teacher-notes.md'))
        self.assertEqual(actual['A02-D2'], '基础')
        self.assertEqual(actual['B07-T3'], '基础')
        self.assertEqual(actual['B06-D2'], '扩展候选')
        self.assertEqual(actual['D07-T3'], '扩展候选')
        elective = read_lesson('E06')
        self.assertFalse(elective['meta']['labs'])
        self.assertTrue(all(v['level'] == 'K' for v in elective['objectives'].values()))
        self.assertTrue(all(v == '基础' for v in bands(
            section(read_text(ROOT/'course/teacher-notes.md'), 'E06')).values()))

    def test_ten_item_example_references_real_questions_and_is_eight_plus_two(self):
        design = read_text(ROOT/'docs/design.md').split('<a id="question-difficulty"></a>', 1)[1]
        design = design.split('<a id="design-decisions"></a>', 1)[0]
        rows = re.findall(r'^\|\[([A-E]\d{2}-[PDTK]\d+)\]\([^\n]+?\)\|([^\n|]+)\|(基础|扩展)\|$', design, re.M)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r[0] for r in rows}), 10)
        self.assertEqual(sum(r[2] == '基础' for r in rows), 8)
        actual = bands(read_text(ROOT/'course/teacher-notes.md'))
        for qid, judgment, level in rows:
            self.assertIn(qid, read_lesson(qid.split('-')[0])['questions'])
            self.assertEqual(actual[qid], '基础' if level == '基础' else '扩展候选')
            self.assertTrue(judgment.strip())
        self.assertIn('不是新的试卷或新增必做任务', design)
        self.assertIn('独立判断时应拆开计数', design)

    def test_common_contract_and_item_bands_reach_both_inputs_for_all_lessons(self):
        common = read_text(ROOT/'course/teacher-notes.md').partition('\n## ')[0]
        for phrase in ('不是提问数量任务', '不必先证明值得问', '默认8道基础＋2道可选扩展',
                       '不是每课十题', '80%', '按实际作答负担', '对应M仍须', 'K保持用途'):
            self.assertIn(phrase, common)
        for ident in ORDER:
            expected = bands(teacher_section(ident))
            for purpose in ('experience', 'project'):
                text, hashes = build_input(ident, purpose=purpose)
                self.assertIn(common.strip(), text)
                self.assertEqual(bands(text.split('# 教师答案：初始学生页面不可展示', 1)[1]), expected)
                self.assertEqual(set(hashes), {'lesson', 'teacher', 'memory', 'skill'})
                self.assertEqual(text.count('## 讲给爸爸听'), 1)

    def test_question_cues_do_not_create_an_extra_task_or_answer_gate(self):
        for ident in ('A04', 'B06', 'B12', 'B13', 'C10', 'D07'):
            row = read_lesson(ident)
            head, reference = row['body'].split('<details data-audience="reference">', 1)
            self.assertIn('带学提醒', reference)
            self.assertNotIn('预设层次', head)
            self.assertEqual(row['questions'], [ident+'-'+kind+str(i+1) for i, kind in enumerate('PDTK')])
        b12 = read_lesson('B12')['body']
        self.assertIn('一句具体问题', b12)
        self.assertIn('已有证据支持的部分可以接受', b12)
        skill = read_text(ROOT/'openmaic/skills/ai3d-self-study/SKILL.md')
        self.assertIn('不按问题数量评价思维活跃', skill)
        self.assertIn('不懂词义也可直接问', skill)
        self.assertIn('当前证据足够就接受并继续', skill)
        self.assertIn('不是每课十题或80%答对率', skill)
        self.assertLess(len(skill), 2000)


if __name__ == '__main__':
    unittest.main()
