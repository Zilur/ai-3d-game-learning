"""Mac/Windows are the only user-facing release targets."""
from pathlib import Path
import unittest
from lib.desktop_export import release_target

ROOT = Path(__file__).resolve().parents[2]

class SupportedPlatformTests(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(release_target('Windows'), ('Windows', 'Starlight.exe'))
        self.assertEqual(release_target('Darwin'), ('macOS', 'Starlight-macOS.zip'))

    def test_unsupported_refused(self):
        for system in ('Linux', 'FreeBSD', ''):
            with self.assertRaises(ValueError):
                release_target(system)

    def test_only_two_presets(self):
        text = (ROOT / 'practice/godot/export_presets.cfg').read_text(encoding='utf-8')
        self.assertNotIn('Linux', text)
        self.assertIn('[preset.0]', text)
        self.assertIn('[preset.1]', text)
        self.assertNotIn('[preset.2]', text)

    def test_release_matrix_and_instructions(self):
        text = (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8')
        self.assertIn('os: [windows-2025, macos-15]', text)
        self.assertNotIn('ubuntu', text)
        self.assertNotIn('--render', text)
        source = (ROOT / 'tools/lib/desktop_export.py').read_text(encoding='utf-8')
        self.assertNotIn('Starlight.x86_64', source)

if __name__ == '__main__':
    unittest.main()
