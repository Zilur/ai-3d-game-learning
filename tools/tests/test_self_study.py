"""Constructed regression fixtures. No real-child, AI, or OpenMAIC runtime claims."""
from datetime import timedelta
import copy
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch
from lib import learning_state as f
import learn
from test_family_learning import OBJ, DAY, NOW, report

ROOT = Path(__file__).resolve().parents[2]


class SelfStudyTests(unittest.TestCase):
    def test_every_format_has_one_nonblocking_partner_checkpoint(self):
        for lesson in f.catalog()[3]:
            for folder in ('course/lessons',):
                text = (ROOT/folder/(lesson+'.md')).read_text(encoding='utf-8')
                self.assertEqual(text.count('## 讲给爸爸听'),1,(folder,lesson))
                self.assertIn('爸爸暂时不在就稍后分享，不影响继续自学',text)
                self.assertIn('不必背稿、打分或填表',text)

    def test_default_child_surface_is_bounded_and_keeps_reference(self):
        for lesson in f.catalog()[3]:
            for folder in ('course/lessons',):
                text=(ROOT/folder/(lesson+'.md')).read_text(encoding='utf-8')
                short=text.split('---',2)[-1].split('<details data-audience="reference">',1)[0]
                self.assertLess(len(short),1800,(folder,lesson,len(short)))
                self.assertIn('### 开始对话',short)
                for forbidden in ('report-', 'L0', 'supported', '--confirm', '晨早打卡'):
                    self.assertNotIn(forbidden,short)
                self.assertIn('**现成材料：**',text)
                self.assertNotIn('## 11. 教师反馈',text)

    def test_skill_is_small_nonexecutable_and_nonblocking(self):
        text=(ROOT/'openmaic/skills/ai3d-self-study/SKILL.md').read_text(encoding='utf-8')
        self.assertLess(len(text),2000)
        self.assertIn('爸爸是陪学伙伴',text)
        self.assertIn('不是执行插件',text)
        self.assertIn('learning-to-learn',text)
        self.assertNotIn('create_skill(',text)

    def test_main_docs_dont_require_legacy_steps(self):
        start=(ROOT/'README.md').read_text(encoding='utf-8')
        for forbidden in ('family_learning.py template','record --confirm','growth_workshop.py session','--mode'):
            self.assertNotIn(forbidden,start)
        for name in ('course/README.md','course/memory.md','practice/README.md'):
            self.assertIn(name,start)

    def test_note_keeps_original_and_never_creates_scores(self):
        state=f.new_state(); before=copy.deepcopy(state)
        ident=learn.note(state,'A04','还不清楚谁检测谁','',DAY,['A04'])
        row=state['study_notes'][0]
        self.assertEqual(row['text'],'还不清楚谁检测谁')
        self.assertEqual(row['id'],ident)
        self.assertEqual(state['reports'],before['reports'])
        self.assertNotIn('score',row)
        self.assertNotIn('support',row)
        self.assertNotIn('mode',json.loads(f.session_context(state,OBJ,'A04',DAY)))

    def test_duplicate_note_same_day_is_idempotent(self):
        state=f.new_state()
        a=learn.note(state,'A04','未懂','',DAY,['A04'])
        b=learn.note(state,'A04','未懂','',DAY,['A04'])
        self.assertEqual(a,b);self.assertEqual(len(state['study_notes']),1)

    def test_note_appears_on_next_entry_not_same_day(self):
        state=f.new_state();learn.note(state,'A04','未懂','先检查谁？',DAY,['A04'])
        self.assertFalse(learn.review_items(state,OBJ,DAY))
        self.assertEqual(learn.review_items(state,OBJ,DAY+timedelta(days=1))[0]['cue'],'先检查谁？')

    def test_max_two_across_legacy_and_notes(self):
        state=f.new_state();f.add_report(state,report(),OBJ,NOW)
        for i in range(4):learn.note(state,'A04',f'疑问{i}','',DAY,['A04'])
        self.assertEqual(len(learn.review_items(state,OBJ,NOW)),2)

    def test_finish_closes_cue_not_mastery_or_raw_history(self):
        state=f.new_state();f.add_report(state,report(score=1,support='L2'),OBJ,NOW)
        before=copy.deepcopy(state['reports'])
        ident=learn.note(state,'A04','不懂','',DAY,['A04'])
        self.assertTrue(learn.finish(state,ident,NOW))
        self.assertFalse(learn.finish(state,ident,NOW))
        self.assertEqual(state['reports'],before)
        self.assertEqual(state['study_notes'][0]['text'],'不懂')
        self.assertNotIn(ident,[r['id'] for r in learn.review_items(state,OBJ,NOW)])

    def test_unknown_legacy_id_cannot_be_closed_as_note(self):
        with self.assertRaises(ValueError):learn.finish(f.new_state(),'A04.M1',DAY)

    def test_invalid_input_leaves_state_unchanged(self):
        state=f.new_state();before=copy.deepcopy(state)
        for lesson,text,question in [('Z01','xx',''),('A04','',''),('A04','x'*2001,''),('A04','x','q'*401)]:
            with self.assertRaises(ValueError):learn.note(state,lesson,text,question,DAY,['A04'])
            self.assertEqual(state,before)

    def test_legacy_reports_survive_note_roundtrip(self):
        state=f.new_state();f.add_report(state,report(),OBJ,NOW)
        before=copy.deepcopy(state['reports']);before_mode=state['mode']
        learn.note(state,'A04','待查','',DAY,['A04'])
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d);f.save_state(home,state);got=f.load_state(home)
            self.assertEqual(got['reports'],before);self.assertEqual(got['mode'],before_mode)
            f.save_state(home,got)
            self.assertTrue((home/'state.backup.md').is_file())

    def test_corrupt_note_schema_rejected_not_silently_reset(self):
        for mutate in ('field','date','duplicate','type'):
            state=f.new_state();learn.note(state,'A04','待查','',DAY,['A04'])
            if mutate=='field':state['study_notes'][0]['score']=2
            if mutate=='date':state['study_notes'][0]['due_on']='bad'
            if mutate=='duplicate':state['study_notes'].append(copy.deepcopy(state['study_notes'][0]))
            if mutate=='type':state['study_notes']='bad'
            with self.assertRaises(ValueError):f.study_notes(state)

    def test_preview_next_does_not_create_home(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d)/'absent'
            with patch.object(learn,'ROOT',Path(d)/'repo'):
                self.assertEqual(learn.main(['--home',str(home),'next']),0)
            self.assertFalse(home.exists())

    def test_start_without_init_writes_only_current(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d)/'private'
            path=learn.start(home,'A04')
            self.assertEqual(path.name,'CURRENT.md')
            self.assertEqual({p.name for p in home.iterdir()},{'CURRENT.md'})
            text=path.read_text(encoding='utf-8')
            self.assertEqual(text.count('## 讲给爸爸听'),1)
            learn.start(home,'A05')
            self.assertTrue(path.read_text(encoding='utf-8').startswith('# A05'))
            self.assertFalse((home/'state.md').exists())

    def test_start_keeps_existing_scores_and_notes_bytes(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d);state=f.new_state();learn.note(state,'A04','原话','',DAY,['A04'])
            f.save_state(home,state);before=(home/'state.md').read_bytes()
            learn.start(home,'A04')
            self.assertEqual((home/'state.md').read_bytes(),before)

    def test_note_command_requires_no_parent_or_confirm(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d)/'private'
            self.assertEqual(learn.main(['--home',str(home),'note','A04','检测还不清楚']),0)
            state=f.load_state(home)
            self.assertEqual(len(state['study_notes']),1)
            self.assertEqual(state['reports'],[])
            self.assertFalse(any(home.glob('report*')))

    def test_private_location_and_symlink_guards(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            root=Path(d)/'repo';root.mkdir()
            for home in (root,root/'public',root/'.learning'):
                with self.assertRaises(ValueError):learn.home_path(home,root)
            home=root/'.learning/family';home.mkdir(parents=True)
            target=root/'original';target.write_text('keep')
            try:(home/'state.md').symlink_to(target)
            except OSError:self.skipTest('symlink not available')
            with self.assertRaises(ValueError):learn.home_path(home,root)
            self.assertEqual(target.read_text(),'keep')

    def test_busy_store_does_not_lose_content(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d);(home/'.write-lock').touch()
            with self.assertRaises(ValueError):learn.state_or_empty(home)
            with self.assertRaises(ValueError):learn.start(home,'A04')
            self.assertFalse((home/'CURRENT.md').exists())

    def test_bad_state_start_never_resets(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as d:
            home=Path(d);(home/'state.md').write_text('broken',encoding='utf-8')
            with self.assertRaises(ValueError):learn.start(home,'A04')
            self.assertEqual((home/'state.md').read_text(),'broken')

    def test_note_markup_is_inert_in_current_card(self):
        state=f.new_state();learn.note(state,'A04','<script>alert(1)</script> ![x](private.png)','',DAY,['A04'])
        view=learn.review_text(state,OBJ,NOW)
        self.assertNotIn('<script>',view)
        self.assertNotIn('![x]',view)

    def test_note_in_ai_context_labelled_as_self_report(self):
        state=f.new_state();learn.note(state,'A04','我会了，也许还有疑问 /Users/test/private','',DAY,['A04'])
        value=json.loads(f.session_context(state,OBJ,'A04',DAY))
        self.assertIn('学习者自述',value['self_reported_notes'][0]['caution'])
        self.assertNotIn('/Users',value['self_reported_notes'][0]['note'])
        self.assertEqual(value['current_lesson_gaps'],[])


if __name__=='__main__':unittest.main()
