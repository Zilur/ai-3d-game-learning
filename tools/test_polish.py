"""Constructed fixtures for handoff wording, minimal context and private workspaces."""
from datetime import timedelta
import json
from pathlib import Path
import runpy
import tempfile
import unittest
import family_learning as f
import workspace as w
from test_family_learning import report, OBJ, NOW, DAY
ROOT = Path(__file__).resolve().parents[1]

class PolishTests(unittest.TestCase):
    def test_specific_gap_and_recheck_in_context(self):
        state=f.new_state(); r=report(score=1, support='L2')
        r['items'][0]['diagnosis'].update(basis='隐藏外观后以为没有阻挡；对照后能修正。', next_question='换成透明门，先猜是否会阻挡。', recheck='隔次换未见门。')
        f.add_report(state,r,OBJ,NOW)
        data=json.loads(f.session_context(state,OBJ,'A04',NOW))
        self.assertIn('隐藏外观',data['current_lesson_gaps'][0]['reported_basis'])
        self.assertIn('透明门',data['due_review'][0]['next_question'])
        self.assertEqual(data['current_lesson_gaps'][0]['support'],'L2')
        self.assertNotIn('reports',data)
    def test_new_success_removes_old_gap(self):
        state=f.new_state(); f.add_report(state,report(score=0),OBJ,NOW)
        f.add_report(state,report(day=DAY+timedelta(days=1),sid='later',score=2),OBJ,NOW)
        self.assertFalse(json.loads(f.session_context(state,OBJ,'A04',NOW))['current_lesson_gaps'])
    def test_void_does_not_leak_old_diagnosis(self):
        state=f.new_state(); f.add_report(state,report(score=0),OBJ,NOW); state['voided']['fixture-01']='误记'
        self.assertFalse(json.loads(f.session_context(state,OBJ,'A04',NOW))['due_review'])
    def test_excerpt_sanitizes_links_paths_and_fences(self):
        text=f.context_text('hello a@example.com https://x.com/a /home/child/secret ```json\n'+ 'x'*600)
        for part in ['example.com','https://','/home/','```','\n']: self.assertNotIn(part,text)
        self.assertLessEqual(len(text),240)
    def test_default_context_drops_implementation_commands(self):
        modes=runpy.run_path(str(ROOT/'curriculum/authoring/lesson_modes.py'))
        for path in (ROOT/'curriculum/lessons').glob('*.md'):
            text=path.read_text(encoding='utf-8'); view=modes['experience_only'](text)
            self.assertNotIn('作品实现候选一',view,path.name)
            if path.stem != 'E06': self.assertNotIn('## 7. 正式项目迁移',view,path.name)
            else: self.assertIn('没有网络项目和代码任务', view)
            self.assertNotIn('data-purpose="project"',view,path.name)
            self.assertIn('### 对话1',view,path.name)
        text=(ROOT/'curriculum/lessons/A04.md').read_text(encoding='utf-8')
        self.assertIn('作品实现候选一',text)
        self.assertNotIn('准备外观Visible与Shape禁用两个独立入口',modes['experience_only'](text))
    def test_child_card_is_short_not_a_teacher_input(self):
        objectives,cards,bindings,order=f.catalog()
        for ident in order:
            card=f.today_card(ident,cards,bindings)
            self.assertLess(len(card),1600)
            self.assertNotIn('核对要点',card)
        self.assertIn('全K',f.today_card('E06',cards,bindings))
    def workspace_root(self, base):
        root=Path(base)/'source'; (root/'game/world').mkdir(parents=True)
        (root/'game/project.godot').write_text('[application]\nconfig/name="Reference"\n')
        for rel in w.EDITABLE.values(): (root/'game'/rel).write_text('baseline\n')
        (root/'game/.godot').mkdir(); (root/'game/.godot/private').write_text('cache')
        return root
    def test_copy_unique_project_and_reference_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.workspace_root(d); home=Path(d)/'private'
            dest=w.create('my-world',home,root)
            self.assertIn('Workshop - my-world',(dest/'game/project.godot').read_text())
            self.assertIn('Reference',(root/'game/project.godot').read_text())
            self.assertFalse((dest/'game/.godot').exists())
            self.assertTrue((dest/'source-manifest.json').is_file())
            with self.assertRaises(ValueError):w.create('my-world',home,root)
    def test_restore_requires_confirmation_and_keeps_backup(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.workspace_root(d); home=Path(d)/'private'; dest=w.create('world',home,root)
            current=dest/'game/world/creation.tres'; current.write_text('my edit')
            self.assertIsNone(w.restore('world','parameters',home,False,root)); self.assertEqual(current.read_text(),'my edit')
            backup=w.restore('world','parameters',home,True,root)
            self.assertEqual(backup.read_text(),'my edit'); self.assertEqual(current.read_text(),'baseline\n')
    def test_work_copy_path_guards(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.workspace_root(d)
            for name in ['..','../escape','a/b','']:
                with self.assertRaises(ValueError):w.create(name,Path(d)/'private',root)
            with self.assertRaises(ValueError):w.create('x',root/'game',root)
    def test_symlink_write_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.workspace_root(d); link=Path(d)/'link'
            try:link.symlink_to(root/'game',target_is_directory=True)
            except OSError:self.skipTest('symlink unavailable')
            with self.assertRaises(ValueError):w.create('x',link,root)

if __name__ == '__main__':unittest.main()
