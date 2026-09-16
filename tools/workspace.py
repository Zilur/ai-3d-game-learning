#!/usr/bin/env python3
"""One private, non-overwriting game copy. No network, AI calls or learner grading."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EDITABLE = {'parameters': 'world/creation.tres', 'layout': 'world/exploration.tscn'}
SKIP = {'.godot', '.git', '.learning', 'build', 'exports', '.export', 'export_credentials.cfg'}


def clean_path(path: Path) -> Path:
    absolute = path.absolute()
    if any(p.is_symlink() for p in (absolute, *absolute.parents)):
        raise ValueError('不沿符号链接写入工作副本。')
    return absolute.resolve()


def target(name: str, home: Path, root=ROOT) -> Path:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,40}', name):
        raise ValueError('副本名使用1–41位字母、数字、短横线或下划线，不用真实姓名。')
    home, root = clean_path(home), root.resolve()
    if home == root or root in home.parents and not (root / '.learning' == home or root / '.learning' in home.parents):
        raise ValueError('仓库内工作副本只能放.learning下；也可指定仓库外私人目录。')
    return clean_path(home / name)


def create(name: str, home: Path, root=ROOT) -> Path:
    dest = target(name, home, root)
    if dest.exists(): raise ValueError('已有同名副本，不覆盖。请继续使用，或换一个副本名。')
    source = root / 'game'
    files = []
    for path in source.rglob('*'):
        rel = path.relative_to(source)
        if any(x in SKIP for x in rel.parts) or path.suffix in ('.log', '.tmp'): continue
        if path.is_symlink(): raise ValueError('源工程包含符号链接，拒绝复制。')
        if path.is_file(): files.append((path, rel))
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.workspace-', dir=dest.parent) as temp:
        stage = Path(temp) / name
        (stage / 'game').mkdir(parents=True)
        records = {}
        for path, rel in files:
            out = stage / 'game' / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, out)
            records[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        project = stage / 'game/project.godot'
        original = project.read_text(encoding='utf-8')
        changed, count = re.subn(r'^config/name=.*$', 'config/name="Starlight Workshop - ' + name + '"', original, count=1, flags=re.M)
        if count != 1: raise ValueError('找不到唯一项目名，未创建副本。')
        project.write_text(changed, encoding='utf-8')
        (stage / '.baseline').mkdir()
        for key, rel in EDITABLE.items(): shutil.copy2(stage / 'game' / rel, stage / '.baseline' / (key + Path(rel).suffix))
        (stage / 'source-manifest.json').write_text(json.dumps({'schema_version': 1, 'source_files': records}, ensure_ascii=False, indent=2), encoding='utf-8')
        (stage / 'WORKSPACE.md').write_text('''# 我的工作副本

打开本目录game/project.godot，不要改原参考。F5玩，F6运行当前实验。

**只调一个体验参数：** 在文件面板选择world/creation.tres，用Inspector调整Walk Speed / Run Speed / Jump Velocity / Gravity / Path Color，Ctrl+S保存，F5比较。它是本项目的自定义Resource，不是Godot内置设置。

**只换一颗星的位置：** 打开world/exploration.tscn，选StarLayout中的一个Marker3D，按F聚焦，移动一小段，再Ctrl+S。彩色板和球是编辑定位示意，运行时隐藏；真正星星读取同名标记的位置。不要重命名标记或物品ID，也不要移动StarLayout父节点。先在所属区域的可达道路旁微调，不穿墙或越过锁门。

**验证：** 关闭Godot后重新打开，确认参数与标记仍在，再新开一局检查。旧存档中已收集的星星不会因为移动标记而重新出现。按R新开局前会确认，原磁盘存档保留。

**恢复：** 用撤销，或由成人从.baseline恢复一项。workspace.py restore提供预览，--confirm后先保留当前文件为恢复备份；不修改原参考。

**保持项：** 镜头策略、碰撞、稳定物品ID、钥匙门和存档格式不随外观练习修改。改动后的布局能否通关仍需实走，不自动继承原版的通过结论。

本副本使用独立项目名，因此Godot用户数据目录与参考工程隔离。学习记录继续放原仓库.learning/family，不往游戏包里放私人观察。
''', encoding='utf-8')
        # Atomic publication; a competing existing destination must not be replaced.
        if dest.exists(): raise ValueError('目标刚被创建，取消复制。')
        shutil.copytree(stage, dest)  # Exclusive destination mkdir; never replace an existing directory.
    return dest


def restore(name: str, key: str, home: Path, confirm=False, root=ROOT) -> Path | None:
    dest = target(name, home, root)
    rel = EDITABLE[key]
    current = clean_path(dest / 'game' / rel)
    baseline = clean_path(dest / '.baseline' / (key + Path(rel).suffix))
    if not current.is_file() or not baseline.is_file(): raise ValueError('工作副本或基线缺失，不从当前新版本猜测旧内容。')
    if not confirm:
        print('将恢复 ' + str(current) + '；当前文件会先备份。未修改；核对后加--confirm。')
        return None
    backup_dir = clean_path(dest / 'restore-backups')
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup = backup_dir / (stamp + '-' + current.name)
    with backup.open('xb') as f: f.write(current.read_bytes())
    from family_learning import atomic_write
    atomic_write(current, baseline.read_text(encoding='utf-8'))
    return backup


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home', type=Path, default=ROOT / '.learning/projects')
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('create'); q.add_argument('name')
    q = sub.add_parser('restore'); q.add_argument('name'); q.add_argument('--file', choices=EDITABLE, required=True); q.add_argument('--confirm', action='store_true')
    a = p.parse_args(argv)
    if a.command == 'create': print('已创建：' + str(create(a.name, a.home) / 'game/project.godot'))
    else:
        backup = restore(a.name, a.file, a.home, a.confirm)
        if backup: print('已恢复一项，改前备份：' + str(backup))


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError) as exc: print('未完成：' + str(exc), file=sys.stderr); sys.exit(2)
