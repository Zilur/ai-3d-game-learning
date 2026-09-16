"""Rule tests with constructed, anonymous fixtures; not a trial with a child."""
import copy
from datetime import date, timedelta
import json
from pathlib import Path
import runpy
import tempfile
import unittest

import family_learning as f

OBJ = {
    'A04.M1': {'lesson': 'A04', 'level': 'M', 'text': '区分外观、阻挡和检测。'},
    'A04.M2': {'lesson': 'A04', 'level': 'M', 'text': '说明谁检测谁。'},
    'E06.K1': {'lesson': 'E06', 'level': 'K', 'text': '理解联网用途。'},
}
DAY = date(2026, 1, 1)
NOW = date(2026, 12, 31)


def report(day=DAY, sid='fixture-01', axis='reasoning', score=2, support='L0', ident='A04.M1', mode='simulation'):
    r = f.report_template(OBJ[ident]['lesson'], OBJ, day)
    r['family'].update(session_id=sid, mode=mode)
    r['target_objectives'] = [ident]
    r['items'] = [x for x in r['items'] if x['objective'] == ident]
    item = r['items'][0]
    if score is not None:
        kind = {'application': 'software', 'transfer': 'transfer'}.get(axis, 'answer')
        item['evidence'] = [{'id': 'fixture-e1', 'kind': kind, 'reference': '构造测试样例，不是真实孩子数据', 'summary': '仅测试程序结构。'}]
        item['observations'][axis] = {'score': score, 'support': support, 'evidence_ids': ['fixture-e1']}
    if axis == 'transfer': r['family']['novel_objectives'] = [ident]
    return r


class FamilyRules(unittest.TestCase):
    def setUp(self):
        self.state = f.new_state()

    def add(self, r):
        return f.add_report(self.state, r, OBJ, NOW)

    def track(self, axis='reasoning'):
        return f.tracks(self.state, OBJ, NOW)[('A04.M1', axis)]

    def test_empty_is_not_pass_or_failure(self):
        self.assertEqual(f.tracks(self.state, OBJ, NOW), {})
        self.assertEqual(f.due_items(self.state, OBJ, NOW), [])
        self.assertNotIn('|A04.M1|', f.dashboard(self.state, OBJ, NOW))

    def test_first_review_is_next_day(self):
        self.add(report())
        self.assertEqual(self.track()['due'], DAY + timedelta(days=1))
        self.assertEqual(f.due_items(self.state, OBJ, DAY), [])

    def test_idempotent_import(self):
        self.assertTrue(self.add(report()))
        self.assertFalse(self.add(report()))
        self.assertEqual(len(self.state['reports']), 1)

    def test_conflicting_same_id_rejected(self):
        self.add(report())
        with self.assertRaises(ValueError): self.add(report(score=1))

    def test_same_day_cannot_inflate_stage(self):
        self.add(report())
        self.add(report(sid='fixture-02'))
        self.assertEqual(self.track()['stage'], 0)
        self.assertEqual(len(self.track()['good_days']), 1)

    def test_due_success_expands_gap(self):
        self.add(report())
        self.add(report(day=DAY + timedelta(days=1), sid='fixture-02'))
        self.assertEqual(self.track()['stage'], 1)
        self.assertEqual(self.track()['due'], DAY + timedelta(days=4))

    def test_early_repeat_does_not_postpone(self):
        self.add(report())
        self.add(report(day=DAY + timedelta(days=1), sid='fixture-02'))
        self.add(report(day=DAY + timedelta(days=2), sid='fixture-03'))
        self.assertEqual(self.track()['due'], DAY + timedelta(days=4))

    def test_error_resets_memory_interval(self):
        self.add(report())
        self.add(report(day=DAY + timedelta(days=1), sid='fixture-02'))
        self.add(report(day=DAY + timedelta(days=4), sid='fixture-03', score=0))
        self.assertEqual(self.track()['stage'], 0)
        self.assertEqual(self.track()['due'], DAY + timedelta(days=5))
        self.assertEqual(self.track()['good_days'], [])

    def test_hint_does_not_equal_independent(self):
        self.add(report(score=1, support='L2'))
        self.assertEqual(self.track()['good_days'], [])

    def test_missing_axis_stays_pending(self):
        self.add(report())
        self.assertNotIn(('A04.M1', 'application'), f.tracks(self.state, OBJ, NOW))
        self.assertIn('待验证', f.dashboard(self.state, OBJ, NOW))

    def test_null_observation_creates_no_schedule(self):
        self.add(report(score=None))
        self.assertEqual(f.tracks(self.state, OBJ, NOW), {})

    def test_k_is_not_drilled(self):
        self.add(report(ident='E06.K1'))
        self.assertEqual(f.due_items(self.state, OBJ, NOW), [])

    def test_k_cannot_have_implementation_grade(self):
        with self.assertRaises(ValueError): self.add(report(ident='E06.K1', axis='application', mode='software'))

    def test_simulation_cannot_be_software_evidence(self):
        with self.assertRaises(ValueError): self.add(report(axis='application'))

    def test_software_and_memory_are_separate(self):
        self.add(report(axis='application', mode='software'))
        self.assertEqual(f.due_items(self.state, OBJ, NOW), [])
        self.assertIn(('A04.M1', 'application'), f.tracks(self.state, OBJ, NOW))

    def test_transfer_requires_novel_declaration(self):
        r = report(axis='transfer'); r['family']['novel_objectives'] = []
        with self.assertRaises(ValueError): self.add(r)

    def test_transfer_with_evidence_allowed(self):
        self.add(report(axis='transfer'))
        self.assertEqual(self.track('transfer')['last_score'], 2)

    def test_future_date_rejected(self):
        with self.assertRaises(ValueError): self.add(report(day=NOW + timedelta(days=1)))

    def test_boolean_score_rejected(self):
        with self.assertRaises(ValueError): self.add(report(score=True))

    def test_revealed_answer_cannot_score_independent(self):
        with self.assertRaises(ValueError): self.add(report(support='L3'))

    def test_missing_evidence_rejected(self):
        r = report(); r['items'][0]['observations']['reasoning']['evidence_ids'] = []
        with self.assertRaises(ValueError): self.add(r)

    def test_unknown_objective_rejected(self):
        r = report(); r['target_objectives'] = ['Z99.M1']
        with self.assertRaises(ValueError): self.add(r)

    def test_wrong_evidence_kind_rejected(self):
        r = report(); r['items'][0]['evidence'][0]['kind'] = 'software'
        with self.assertRaises(ValueError): self.add(r)

    def test_queue_cap_and_one_entry_per_objective(self):
        self.add(report())
        self.add(report(axis='recall', sid='fixture-02'))
        self.add(report(ident='A04.M2', sid='fixture-03'))
        self.state['review_limit'] = 1
        self.assertEqual(len(f.due_items(self.state, OBJ, NOW)), 1)

    def test_void_preserves_source_but_removes_effect(self):
        self.add(report())
        self.state['voided']['fixture-01'] = '构造更正'
        self.assertEqual(len(self.state['reports']), 1)
        self.assertEqual(f.tracks(self.state, OBJ, NOW), {})

    def test_out_of_order_days_rebuilt(self):
        self.add(report(day=DAY + timedelta(days=1), sid='fixture-02'))
        self.add(report())
        self.assertEqual(self.track()['due'], DAY + timedelta(days=4))

    def test_same_day_uses_import_order_not_id_order(self):
        self.add(report(sid='z-first'))
        self.add(report(sid='a-second', score=0))
        self.assertEqual(self.track()['last_score'], 0)

    def test_context_is_minimal(self):
        self.add(report(score=0))
        context = json.loads(f.session_context(self.state, OBJ, 'A04', NOW))
        self.assertEqual(len(context['current_lesson_gaps']), 1)
        self.assertNotIn('reports', context)
        self.assertNotIn('evidence', context)

    def test_state_roundtrip_and_backup(self):
        with tempfile.TemporaryDirectory() as d:
            home = Path(d)
            f.save_state(home, self.state)
            self.add(report())
            f.save_state(home, self.state)
            self.assertEqual(f.load_state(home), self.state)
            self.assertIn('"reports": []', (home / 'state.backup.md').read_text())

    def test_corrupt_state_is_not_reset(self):
        with tempfile.TemporaryDirectory() as d:
            home = Path(d); path = home / 'state.md'; path.write_text('bad data')
            with self.assertRaises(ValueError): f.load_state(home)
            self.assertEqual(path.read_text(), 'bad data')

    def test_concurrent_lock_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            home = Path(d)
            with f.locked(home):
                with self.assertRaises(ValueError):
                    with f.locked(home): pass
            self.assertFalse((home / '.write-lock').exists())

    def test_public_log_location_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with self.assertRaises(ValueError): f.private_home(root / 'public-logs', root)
            self.assertEqual(f.private_home(root / '.learning/family', root), root / '.learning/family')

    def test_calendar_utc_and_folding(self):
        data = f.calendar_text('Asia/Tokyo', DAY, 2, '07:30', '19:30')
        self.assertEqual(data.count('BEGIN:VEVENT'), 4)
        self.assertIn('DTSTART:20251231T223000Z', data)
        self.assertNotIn('A04.M1', data)
        self.assertTrue(all(len(x.encode('utf-8')) <= 75 for x in data.split('\r\n')))
        self.assertTrue(data.endswith('\r\n'))

    def test_calendar_invalid_input(self):
        for days, hour in [(0, '07:30'), (91, '07:30'), (1, '25:00'), (1, '7:30')]:
            with self.assertRaises(ValueError): f.calendar_text('Asia/Tokyo', DAY, days, hour)

    def test_card_registry_has_47_unique_ids(self):
        cards = runpy.run_path(str(f.ROOT / 'curriculum/authoring/family_cards.py'))['CARDS']
        self.assertEqual(len(cards), 47)
        expected = [f'{group}{n:02}' for group, count in [('A',8),('B',13),('C',12),('D',7),('E',7)] for n in range(1,count+1)]
        self.assertEqual(set(cards), set(expected))

    def test_e06_card_does_not_add_mastery_gate(self):
        cards = {'E06': ('联网用途', '解释一个用途即可。', '需要协调什么？')}
        bindings = {'E06': ([], '讨论', '全K', '选修')}
        text = f.card_text('E06', OBJ, cards, bindings)
        self.assertIn('不进每日复习', text)
        self.assertNotIn('讲给爸爸：', text)


if __name__ == '__main__':
    unittest.main()
