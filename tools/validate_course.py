#!/usr/bin/env python3
"""Offline repository checks, not a substitute for a Godot or teaching test."""
from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"Missing required file: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_links() -> None:
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".godot", "node_modules", ".venv"} for part in path.parts):
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for destination in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            parsed = urlsplit(destination.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            check(target.is_relative_to(ROOT) and target.exists(),
                  f"Broken local link in {path.relative_to(ROOT)}: {destination}")


def validate_coverage() -> None:
    bank = read("assessment/question-bank.md")
    found = re.findall(r"^- ((?:C\d{2}-[PRT])|K\d{2})：", bank, flags=re.M)
    expected = {f"C{i:02d}-{kind}" for i in range(1, 27) for kind in "PRT"}
    expected.update(f"K{i:02d}" for i in range(1, 13))
    check(set(found) == expected, f"Question coverage mismatch: {sorted(expected.symmetric_difference(found))}")
    check(len(found) == len(set(found)) == 90, "Question IDs must be unique (78 core + 12 awareness)")
    concepts = read("curriculum/concept-map.md")
    core_ids = re.findall(r"^\| (C\d{2}) \|", concepts, flags=re.M)
    knowledge_ids = re.findall(r"^\| (K\d{2}) \|", concepts, flags=re.M)
    check(set(core_ids) == {f"C{i:02d}" for i in range(1, 27)}, "Missing C concepts")
    check(set(knowledge_ids) == {f"K{i:02d}" for i in range(1, 13)}, "Missing K concepts")
    answers = read("assessment/answer-key.md")
    for i in range(1, 27):
        check(bool(re.search(rf"^## C{i:02d}\s*$", answers, flags=re.M)), f"Missing answer anchor C{i:02d}")
    for relative, prefix, count in (
        ("curriculum/beginner/lesson-playbook.md", "B", 16),
        ("curriculum/intermediate/lesson-playbook.md", "I", 12),
    ):
        text = read(relative)
        for i in range(1, count + 1):
            check(bool(re.search(rf"^## {prefix}{i:02d}\b", text, flags=re.M)), f"Missing lesson {prefix}{i:02d}")


def validate_resources() -> None:
    for path in (ROOT / "game").rglob("*"):
        if not path.is_file() or ".godot" in path.parts:
            continue
        if path.suffix not in {".gd", ".tscn", ".gdshader", ".godot"}:
            continue
        text = path.read_text(encoding="utf-8")
        for relative in re.findall(r'res://([^"\s]+)', text):
            check((ROOT / "game" / relative).is_file(), f"Missing resource in {path.name}: {relative}")
        if path.suffix == ".tscn":
            header = re.search(r"load_steps=(\d+)", text)
            total = len(re.findall(r"^\[(?:ext_resource|sub_resource)\b", text, flags=re.M)) + 1
            check(header is not None and int(header.group(1)) == total,
                  f"Wrong load_steps in {path.name}; expected {total}")
    for folder in (ROOT / "tools", ROOT / "blender"):
        for path in folder.glob("*.py"):
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                check(True, str(path))
            except SyntaxError as exc:
                check(False, f"Python syntax error: {exc}")


def validate_star() -> None:
    vertices: list[tuple[float, float, float]] = []
    faces: list[list[int]] = []
    for line in read("game/assets/star.obj").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "v":
            vertices.append(tuple(map(float, parts[1:4])))
        elif parts[0] == "f":
            faces.append([int(value.split("/")[0]) - 1 for value in parts[1:]])
    check(len(vertices) == 22 and len(faces) == 40, "Star should have 22 vertices and 40 triangles")
    valid_faces = all(len(face) == 3 and all(0 <= i < len(vertices) for i in face) for face in faces)
    check(valid_faces, "Invalid OBJ faces")
    if not valid_faces:
        return
    edges: Counter[tuple[int, int]] = Counter()
    volume = 0.0
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((x, y)))] += 1
        va, vb, vc = vertices[a], vertices[b], vertices[c]
        volume += (va[0] * (vb[1] * vc[2] - vb[2] * vc[1])
                   + va[1] * (vb[2] * vc[0] - vb[0] * vc[2])
                   + va[2] * (vb[0] * vc[1] - vb[1] * vc[0])) / 6.0
    check(all(count == 2 for count in edges.values()), "Star must be a closed two-face-per-edge mesh")
    check(volume > 0.0, "Star winding should yield positive signed volume")
    print(f"OBJ: {len(vertices)} vertices, {len(faces)} triangles, signed volume {volume:.9f}")


def main() -> int:
    validate_links()
    validate_coverage()
    validate_resources()
    validate_star()
    for message in errors:
        print("FAIL:", message, file=sys.stderr)
    if errors:
        print(f"VALIDATION FAILED: {len(errors)} issue(s), {checks} checks", file=sys.stderr)
        return 1
    print(f"COURSE VALIDATION PASS: {checks} checks, 90 unique questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
