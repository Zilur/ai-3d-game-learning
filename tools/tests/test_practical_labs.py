"""Negative probes for the readiness contract. Engine/Blender run separately."""
import copy
import runpy
import unittest
from pathlib import Path
from lib.checks.check_practical_labs import validate_mesh, validate_bindings, ROOT

class Readiness(unittest.TestCase):
    def setUp(self):
        self.mesh = runpy.run_path(str(ROOT/'tools/assets/make_practice_robot.py'))['build']()
        from lib.course import catalog
        _, _, self.bindings, self.order = catalog(ROOT)
    def test_valid(self):
        validate_mesh(self.mesh)
        validate_bindings(self.bindings,self.order)
    def test_missing_skin(self):
        self.mesh['skins'] = []
        with self.assertRaises(ValueError): validate_mesh(self.mesh)
    def test_missing_weights(self):
        del self.mesh['meshes'][0]['primitives'][0]['attributes']['WEIGHTS_0']
        with self.assertRaises(ValueError): validate_mesh(self.mesh)
    def test_missing_action(self):
        self.mesh['animations'].pop()
        with self.assertRaises(ValueError): validate_mesh(self.mesh)
    def test_invalid_bone(self):
        self.mesh['skins'][0]['joints'][0] = -1
        with self.assertRaises(ValueError): validate_mesh(self.mesh)
    def test_missing_lesson(self):
        del self.bindings['C11']
        with self.assertRaises(ValueError): validate_bindings(self.bindings,self.order)
    def test_no_hidden_setup_requirement(self):
        self.bindings['C11'] = (['practice/godot/labs/absent_file.tscn'],'first','limit','P1')
        with self.assertRaises(ValueError): validate_bindings(self.bindings,self.order)
    def test_path_escape(self):
        self.bindings['A04'] = (['../README.md'],'first','limit','P1')
        with self.assertRaises(ValueError): validate_bindings(self.bindings,self.order)
    def test_k_boundary(self):
        self.bindings['E06'] = (['practice/godot/scenes/main.tscn'],'first','limit','P1')
        with self.assertRaises(ValueError): validate_bindings(self.bindings,self.order)

if __name__ == '__main__': unittest.main()
