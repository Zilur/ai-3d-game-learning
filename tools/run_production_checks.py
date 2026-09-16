"""Cross-platform runner for native regression; separate processes for persistence."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ERRORS = re.compile(r'SCRIPT ERROR|Parse Error|ERROR:|PRODUCTION CHECK FAILED|ObjectDB instances leaked|resources still in use')
SUITES = [('smoke','SMOKE PASS'), ('visual_lab','VISUAL LAB PASS'), ('concept_labs','CONCEPT LAB PASS'),
          ('b02','B02 PASS'), ('practical_labs','PRACTICAL LAB PASS'), ('production_suite','PRODUCTION SUITE PASS'), ('study_safety','STUDY SAFETY PASS')]


def run(command: list[str], log: Path, marker: str | None = None) -> None:
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding='utf-8', errors='replace', timeout=180)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(result.stdout, encoding='utf-8')
    print(result.stdout)
    if result.returncode or ERRORS.search(result.stdout) or marker and marker not in result.stdout:
        raise RuntimeError('Native check failed: ' + log.name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', default='godot')
    parser.add_argument('--logs', type=Path, default=Path('build/production-evidence'))
    parser.add_argument('--new-only', action='store_true')
    args = parser.parse_args()
    run([args.godot, '--version'], args.logs / 'engine.log', '4.7.2.stable')
    base = [args.godot, '--headless', '--audio-driver', 'Dummy', '--path', str(ROOT / 'game')]
    run(base + ['--editor', '--import'], args.logs / 'import.log')
    for suite, marker in SUITES[-2:] if args.new_only else SUITES:
        run(base + ['--fixed-fps', '60', '--script', f'res://tests/{suite}.gd'], args.logs / (suite+'.log'), marker)
    for phase in ('write', 'read'):
        run(base + ['--script', 'res://tests/save_roundtrip.gd', '--', phase],
            args.logs / ('persistence-'+phase+'.log'), 'SAVE ROUNDTRIP '+phase.upper()+' PASS')
    print('NATIVE PRODUCTION CHECKS PASS: process runtime, not GPU/child trial certification')


if __name__ == '__main__':
    main()
