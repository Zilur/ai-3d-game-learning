"""Synthetic course-export containers only; no model calls or real classroom claims."""
import copy
import json
from pathlib import Path
import shutil
import stat
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

from lib.course import ROOT, ORDER, build_input, catalog, memory_sections, memory_cues, read_lesson
from lib import learning_state
import openmaic as om
import release
import check


def make_root(base):
    root=Path(base)/'repo';root.mkdir()
    shutil.copytree(ROOT/'course',root/'course')
    shutil.copytree(ROOT/'openmaic/skills',root/'openmaic/skills')
    shutil.copy2(ROOT/'openmaic/catalog.json',root/'openmaic/catalog.json')
    # Resolve every real resource reference, without copying/generating game assets.
    for ident in ORDER:
        for rel in read_lesson(ident)['meta']['labs']:
            p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture, not an asset',encoding='utf-8')
    p=root/'practice/godot/project.godot';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture')
    (root/'README.md').write_text('# Fixture\n')
    return root


def container(path, *, version=1, missing=False, extras=()):
    data={'formatVersion':version,'stage':{'name':'Synthetic test, not a generated course'},
          'agents':[], 'scenes':[{'type':'quiz','title':'fixture','order':0,'content':{}}],
          'mediaIndex':{'test':{'missing':True}} if missing else {}}
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('manifest.json',json.dumps(data))
        for name,value in extras:
            # Explicit metadata retains deliberately unsafe fixture names on Windows.
            # ZipInfo's constructor otherwise normalizes os.sep before the reader sees it.
            info=zipfile.ZipInfo('fixture-entry')
            info.filename=name;info.orig_filename=name
            z.writestr(info,value)
    return path


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        self.root=make_root(self.temp.name)

    def prepared(self):return om.prepare('A04','test-run',root=self.root)
    def accepted(self, missing=False):
        path=self.prepared();src=container(Path(self.temp.name)/'fixture.maic.zip',missing=missing)
        om.attach_export('A04','test-run',src,self.root)
        p=path/'review.md';p.write_text(p.read_text(encoding='utf-8').replace('- [ ]','- [x]'),encoding='utf-8')
        return path,src

    def test_prepare_only_three_trace_files_not_fake_classroom(self):
        p=self.prepared();self.assertEqual({x.name for x in p.iterdir()},{'input.md','run.json','review.md'})
        data=json.loads((p/'run.json').read_text());self.assertEqual(data['status'],'prepared');self.assertIsNone(data['export'])
        self.assertFalse(om.inspect('A04','test-run',self.root)['review_complete'])
        self.assertFalse((self.root/'.learning').exists())

    def test_prepare_no_model_or_private_record_read(self):
        with patch.object(learning_state,'load_state',side_effect=AssertionError('private read')):
            self.prepared()
        self.assertEqual(json.loads((self.root/'openmaic/catalog.json').read_text())['courses'],{})

    def test_same_run_never_overwritten(self):
        p=self.prepared();before={x.name:x.read_bytes() for x in p.iterdir()}
        with self.assertRaises(ValueError):self.prepared()
        self.assertEqual(before,{x.name:x.read_bytes() for x in p.iterdir()})

    def test_unsafe_id_and_unsupported_lesson_rejected(self):
        for lesson,ident in [('A04','../escape'),('A04','/tmp/escape'),('A04','a/b'),('A04',''),('Z00','run')]:
            with self.assertRaises(ValueError):om.prepare(lesson,ident,root=self.root)
        self.assertFalse((self.root/'openmaic/output').exists())

    def test_run_symlink_rejected(self):
        out=self.root/'openmaic/output'
        try:out.symlink_to(Path(self.temp.name),target_is_directory=True)
        except OSError:self.skipTest('symlink not available')
        with self.assertRaises(ValueError):self.prepared()

    def test_input_snapshot_tamper_refused(self):
        p=self.prepared();(p/'input.md').write_text('tampered')
        with self.assertRaises(ValueError):om.inspect('A04','test-run',self.root)

    def test_unrelated_edits_do_not_invalidate_selected_inputs(self):
        self.prepared()
        p=self.root/'course/lessons/A05.md';p.write_text(p.read_text(encoding='utf-8')+'\nExtra reference\n',encoding='utf-8')
        p=self.root/'course/teacher-notes.md';s=p.read_text(encoding='utf-8').replace('### A05-P1','### A05-P1\nAn unrelated teaching note');p.write_text(s,encoding='utf-8')
        (self.root/'README.md').write_text('new intro')
        self.assertFalse(om.inspect('A04','test-run',self.root)['source_changed'])

    def test_metadata_change_included_in_dependency_digest(self):
        self.prepared();p=self.root/'course/lessons/A04.md'
        raw=p.read_text(encoding='utf-8');head,body=raw[4:].split('\n---\n',1)
        meta=json.loads(head);meta['revisit']=['A01']
        p.write_text('---\n'+json.dumps(meta,ensure_ascii=False,indent=2)+'\n---\n'+body,encoding='utf-8')
        self.assertIn('lesson',om.inspect('A04','test-run',self.root)['source_changed'])

    def test_registry_busy_preserves_previous_catalog(self):
        self.accepted();release.classroom_archive('A04','test-run','v1',self.root);p=self.root/'openmaic/catalog.json';before=p.read_bytes()
        with learning_state.locked(self.root/'openmaic'):
            with self.assertRaises(ValueError):om.register('A04','test-run','v1','https://example.org/A04.maic.zip',confirm=True,root=self.root)
        self.assertEqual(p.read_bytes(),before)

    def test_relevant_lesson_change_identified(self):
        self.prepared();p=self.root/'course/lessons/A04.md';p.write_text(p.read_text(encoding='utf-8')+'\nNew concept note\n',encoding='utf-8')
        self.assertIn('lesson',om.inspect('A04','test-run',self.root)['source_changed'])

    def test_relevant_teacher_change_identified(self):
        self.prepared();p=self.root/'course/teacher-notes.md';p.write_text(p.read_text(encoding='utf-8').replace('### A04-P1','### A04-P1\nNew feedback'),encoding='utf-8')
        self.assertIn('teacher',om.inspect('A04','test-run',self.root)['source_changed'])

    def test_related_memory_change_identified(self):
        self.prepared();p=self.root/'course/memory.md';p.write_text(p.read_text(encoding='utf-8').replace('### KN06｜','### KN06｜New wording '),encoding='utf-8')
        self.assertIn('memory',om.inspect('A04','test-run',self.root)['source_changed'])

    def test_skill_change_identified(self):
        self.prepared();p=self.root/'openmaic/skills/ai3d-self-study/SKILL.md';p.write_text(p.read_text(encoding='utf-8')+'\nAdditional constraint',encoding='utf-8')
        self.assertIn('skill',om.inspect('A04','test-run',self.root)['source_changed'])

    def test_project_choice_changes_input_without_touching_lesson(self):
        p=self.root/'course/lessons/A04.md';before=p.read_bytes()
        simple,_=build_input('A04',root=self.root);project,_=build_input('A04',purpose='project',root=self.root)
        self.assertNotIn('data-purpose="project"',simple);self.assertIn('data-purpose="project"',project)
        self.assertEqual(before,p.read_bytes())

    def test_invalid_or_future_zip_contract_refused(self):
        for version in (2,0,True,'1'):
            src=container(Path(self.temp.name)/'bad.maic.zip',version=version)
            with self.assertRaises(ValueError):om.check_export(src)
        src=Path(self.temp.name)/'bad.maic.zip'
        with zipfile.ZipFile(src,'w') as z:z.writestr('other.json','{}')
        with self.assertRaises(ValueError):om.check_export(src)

    def test_zip_traversal_and_absolute_paths_refused(self):
        for name in ('../secret','/etc/test','folder\\secret','C:/secret','safe\0secret'):
            with self.subTest(member=name):
                src=container(Path(self.temp.name)/'bad.maic.zip',extras=[(name,'x')])
                # Verify the on-disk member, before ZipInfo normalizes it at read time.
                raw=src.read_bytes()
                self.assertEqual(raw.count(name.encode('utf-8')),2)
                with self.assertRaises(ValueError):om.check_export(src)
                # Exercise Windows reader normalization even on the Linux CI host.
                original_init=zipfile.ZipInfo.__init__
                def windows_init(info,*args,**kwargs):
                    original_init(info,*args,**kwargs)
                    info.filename=info.filename.replace('\\','/')
                with patch.object(zipfile.ZipInfo,'__init__',windows_init):
                    with self.assertRaises(ValueError):om.check_export(src)

    def test_duplicate_zip_names_refused(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            src=container(Path(self.temp.name)/'bad.maic.zip',extras=[('manifest.json','{}')])
        with self.assertRaises(ValueError):om.check_export(src)

    def test_zip_symlinks_refused_without_extracting(self):
        src=container(Path(self.temp.name)/'bad.maic.zip')
        info=zipfile.ZipInfo('link');info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16
        with zipfile.ZipFile(src,'a') as z:z.writestr(info,'../../target')
        with self.assertRaises(ValueError):om.check_export(src)
        self.assertFalse((self.root/'target').exists())

    def test_actual_export_copied_byte_exact_once(self):
        path=self.prepared();src=container(Path(self.temp.name)/'fixture.maic.zip')
        facts=om.attach_export('A04','test-run',src,self.root)
        self.assertEqual(src.read_bytes(),(path/'A04.maic.zip').read_bytes())
        self.assertEqual(facts['validation'],'container-only; classroom not executed')
        with self.assertRaises(ValueError):om.attach_export('A04','test-run',src,self.root)

    def test_bad_export_does_not_advance_status(self):
        self.prepared();src=container(Path(self.temp.name)/'bad.maic.zip',version=2)
        with self.assertRaises(ValueError):om.attach_export('A04','test-run',src,self.root)
        self.assertEqual(om.load_run('A04','test-run',self.root)[1]['status'],'prepared')

    def test_export_hash_change_blocks_release(self):
        p,_=self.accepted();(p/'A04.maic.zip').write_bytes(b'tampered')
        with self.assertRaises(ValueError):release.classroom_archive('A04','test-run','v1',self.root)

    def test_unreviewed_run_cannot_publish(self):
        self.prepared();src=container(Path(self.temp.name)/'fixture.maic.zip');om.attach_export('A04','test-run',src,self.root)
        with self.assertRaises(ValueError):release.classroom_archive('A04','test-run','v1',self.root)
        self.assertFalse((self.root/'dist').exists())

    def test_changed_source_requires_new_run(self):
        self.accepted();p=self.root/'course/lessons/A04.md';p.write_text(p.read_text(encoding='utf-8')+'\nchange',encoding='utf-8')
        with self.assertRaises(ValueError):om.require_publishable('A04','test-run',self.root)

    def test_declared_missing_media_blocks_release(self):
        self.accepted(missing=True)
        with self.assertRaises(ValueError):release.classroom_archive('A04','test-run','v1',self.root)

    def test_reviewed_synthetic_run_package_has_only_four_files(self):
        p,src=self.accepted();(p/'PRIVATE.txt').write_text('must not travel')
        dest=release.classroom_archive('A04','test-run','test-only',self.root)
        with zipfile.ZipFile(dest) as z:
            self.assertEqual(set(z.namelist()),{'input.md','run.json','review.md','A04.maic.zip'})
            self.assertEqual(z.read('A04.maic.zip'),src.read_bytes())
        with self.assertRaises(ValueError):release.classroom_archive('A04','test-run','test-only',self.root)

    def test_registration_preview_is_read_only(self):
        self.accepted();release.classroom_archive('A04','test-run','v1',self.root);p=self.root/'openmaic/catalog.json';before=p.read_bytes()
        om.register('A04','test-run','v1','https://example.org/A04.maic.zip',root=self.root)
        self.assertEqual(before,p.read_bytes())
        om.register('A04','test-run','v1','https://example.org/A04.maic.zip',confirm=True,root=self.root)
        record=json.loads(p.read_text())['courses']['A04']
        self.assertEqual(record['sha256'],om.digest(self.root/'dist/openmaic/A04/v1.zip'))
        self.assertNotEqual(record['sha256'],record['classroom_sha256'])

    def test_registration_requires_matching_version_bundle(self):
        path,_=self.accepted()
        with self.assertRaises(ValueError):om.register('A04','test-run','v1','https://example.org/v1.zip',confirm=True,root=self.root)
        release.classroom_archive('A04','test-run','v1',self.root)
        (path/'review.md').write_text((path/'review.md').read_text(encoding='utf-8')+'\nChanged review',encoding='utf-8')
        with self.assertRaises(ValueError):om.register('A04','test-run','v1','https://example.org/v1.zip',confirm=True,root=self.root)

    def test_registration_rejects_credential_urls(self):
        self.accepted()
        for url in ('http://example.org/x','https://user:pass@example.org/x','https://example.org/x?token=secret','https://example.org/x#secret'):
            with self.assertRaises(ValueError):om.register('A04','test-run','v1',url,confirm=True,root=self.root)
        self.assertEqual(json.loads((self.root/'openmaic/catalog.json').read_text())['courses'],{})

    def test_sources_exclude_private_generated_cache_and_fonts(self):
        self.prepared()
        for rel in ('.learning/family/state.md','build/test.log','dist/previous.zip','practice/godot/.godot/cache','practice/font.ttf','tools/__pycache__/bad.pyc','openmaic/.env.local'):
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('private or cache')
        out,count=release.source_archive(self.root/'dist/source.zip',self.root)
        with zipfile.ZipFile(out) as z:
            paths=z.namelist();self.assertEqual(count,len(paths))
            self.assertIn('ai-3d-game-learning/course/lessons/A04.md',paths)
            for token in ('.learning/','build/','dist/','output/','.godot/','.ttf','.pyc','.env'):self.assertFalse(any(token in n for n in paths),token)
        with self.assertRaises(ValueError):release.source_archive(out,self.root)

    def test_source_export_rejects_public_symlink(self):
        p=self.root/'course/unsafe.md'
        try:p.symlink_to(self.root/'README.md')
        except OSError:self.skipTest('symlink not available')
        with self.assertRaises(ValueError):release.source_archive(self.root/'dist/source.zip',self.root)

    def test_output_cannot_leave_dist(self):
        for dest in (self.root/'README.md',self.root/'.learning/stuff.zip',self.root/'openmaic/output/stuff.zip',Path(self.temp.name)/'out.zip'):
            with self.assertRaises(ValueError):release.output_path(dest,self.root)

    def test_clean_preview_and_confirm_only_touch_build(self):
        for rel in ('build/transient.txt','.learning/state.md','openmaic/output/real.maic.zip','dist/approved.zip'):
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('keep')
        items=check.clean_build(self.root);self.assertEqual(items,['build/transient.txt']);self.assertTrue((self.root/'build/transient.txt').exists())
        check.clean_build(self.root,True);self.assertFalse((self.root/'build').exists())
        for rel in ('.learning/state.md','openmaic/output/real.maic.zip','dist/approved.zip'):self.assertEqual((self.root/rel).read_text(),'keep')

    def test_clean_rejects_symlink(self):
        p=self.root/'build';p.mkdir()
        try:(p/'link').symlink_to(self.root/'course',target_is_directory=True)
        except OSError:self.skipTest('symlink not available')
        with self.assertRaises(ValueError):check.clean_build(self.root,True)
        self.assertTrue((self.root/'course/lessons/A04.md').exists())


class SourceDesignTests(unittest.TestCase):
    def test_all_core_memory_available_without_learner_state(self):
        parts=memory_sections();self.assertEqual(len(parts),47)
        for key,text in parts.items():
            for label in ('规则','例子','遮住后自问'):self.assertIn(label,text,(key,label))
        self.assertIn('TH',memory_cues('A04'));self.assertIn('不背诵',memory_cues('E06'))

    def test_no_second_author_database(self):
        for name in ('curriculum','learning-system','assessments','print','glossary','docs/archive'):
            self.assertFalse((ROOT/name).exists(),name)
        self.assertEqual(len(list((ROOT/'course/lessons').glob('*.md'))),47)
        self.assertEqual(set(p.name for p in ROOT.glob('*.md')),{'README.md','AGENTS.md'})

    def test_growth_keeps_six_product_stages_without_manager(self):
        text=(ROOT/'course/growth.md').read_text(encoding='utf-8')
        for phrase in ('独立小作品','玩法原型','品质样段','受控生产','候选发布','发布后维护','第二段','代价','AI'):
            self.assertIn(phrase,text)
        self.assertNotIn('growth_workshop.py',text)
        self.assertFalse((ROOT/'tools/growth_workshop.py').exists())

    def test_no_fake_published_classrooms(self):
        # A real future catalog is allowed, but each registration must carry trace evidence.
        data=json.loads((ROOT/'openmaic/catalog.json').read_text())
        for key,row in data['courses'].items():
            self.assertIn(key,ORDER)
            for field in ('version','run_id','input_sha256','sha256','url'):self.assertIn(field,row)
