"""Unified curriculum checks. Not an engine, visual or learner assessment."""
from __future__ import annotations
import ast
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks = 0

def check(ok: bool, message: str) -> None:
    global checks
    checks += 1
    if not ok:
        errors.append(message)

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def main() -> int:
    vendor = ROOT / "openmaic/vendor/THU-MAIC-OpenMAIC"
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".godot", "node_modules"} for part in path.parts):
            continue
        # Exact upstream snapshots retain upstream-relative links; verify their bytes separately.
        if vendor in path.parents:
            continue
        for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith(("#", "mailto:")):
                continue
            target = unquote(link.split("#", 1)[0].split("?", 1)[0])
            check((path.parent / target).exists(), f"Broken link: {path.relative_to(ROOT)} -> {target}")
    expected = {f"C{i:02}" for i in range(1, 33)}
    concepts = set(re.findall(r"\bC\d{2}\b", read("curriculum/concept-map.md")))
    check(concepts == expected, "Expected canonical C01-C32 concepts")
    qids = re.findall(r'\*\*(C\d{2}-[PT])', read("assessments/question-bank.md"))
    check(len(qids) == len(set(qids)) == 64, "Expected 64 distinct cross-stage P/T questions")
    check(set(qids) == {f"{c}-{kind}" for c in expected for kind in ("P", "T")}, "Question/concept mismatch")
    answers = set(re.findall(r"\bC\d{2}\b", read("assessments/answer-key.md")))
    check(expected <= answers, "Teacher answers must cover canonical concepts")
    check(not (ROOT / "assessment").exists(), "Competing assessment directory restored")
    mastery = read("assessments/mastery.md")
    check("统一0–2评分锚点" in mastery, "Missing active 0-2 scoring heading")
    headers = re.findall(r'^\|证据\|.*$', mastery, re.M)
    check(headers == ["|证据|0|1|2|"], "Active scoring table must have exactly 0, 1, 2")
    for path in ("START-HERE.md", "print/必须牢记.md", "openmaic/requirements/B02-scene-node.md",
                 "curriculum/beginner/02-scene-node/lesson.md", "curriculum/beginner/02-scene-node/assessment.md",
                 "curriculum/beginner/02-scene-node/answer-key.md"):
        check((ROOT / path).is_file(), f"Missing learning entry: {path}")
    lesson = read("curriculum/beginner/02-scene-node/lesson.md")
    check(all(word in lesson for word in ("M 必须掌握", "K 理解即可", "停止线", "starter.tscn", "broken.tscn", "reference.tscn")), "B02 needs depth, boundaries and materials")
    for path in (ROOT / "game").rglob("*"):
        if ".godot" in path.parts or path.suffix not in {".gd", ".tscn", ".godot", ".gdshader"}:
            continue
        text = path.read_text(encoding="utf-8")
        for resource in re.findall(r'res://([^"\s\x27)]+)', text):
            if "%" not in resource:
                check((ROOT / "game" / resource).exists(), f"Missing resource in {path.name}: {resource}")
        if path.suffix == ".tscn":
            for kind in ("ext", "sub"):
                ids = re.findall(r'\[' + kind + r'_resource[^\n]* id="([^"]+)"', text)
                check(len(ids) == len(set(ids)), f"Duplicate {kind} resource IDs: {path}")
    for path in ROOT.rglob("*.py"):
        if any(part in {".git", ".godot", "node_modules"} for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            check(False, str(exc))
    mesh = json.loads(read("game/assets/star.gltf"))
    raw = base64.b64decode(mesh["buffers"][0]["uri"].split(",", 1)[1], validate=True)
    check(len(raw) == mesh["buffers"][0]["byteLength"], "glTF buffer length mismatch")
    for view in mesh["bufferViews"]:
        check(0 <= view.get("byteOffset", 0) <= view.get("byteOffset", 0) + view["byteLength"] <= len(raw), "glTF view out of bounds")
    vertices, faces = [], []
    for line in read("game/assets/star.obj").splitlines():
        parts = line.split()
        if parts and parts[0] == "v":
            vertices.append(tuple(map(float, parts[1:4])))
        elif parts and parts[0] == "f":
            faces.append([int(v.split("/")[0]) - 1 for v in parts[1:]])
    check(len(vertices) == 22 and len(faces) == 40, "Unexpected reference OBJ topology")
    edges: Counter[tuple[int, int]] = Counter()
    for face in faces:
        check(len(face) == 3 and all(0 <= v < len(vertices) for v in face), "Invalid OBJ face")
        for a, b in zip(face, face[1:] + face[:1]):
            edges[tuple(sorted((a, b)))] += 1
    check(bool(edges) and all(n == 2 for n in edges.values()), "Reference OBJ must have closed edges")
    # The first authored-source commit precedes expansion; once present, outputs must stay in sync.
    if (ROOT / "curriculum/materials-manifest.json").exists():
        result = subprocess.run([sys.executable, str(ROOT / "tools/build_course_materials.py"), "--check"], cwd=ROOT, check=False)
        check(result.returncode == 0, "Generated lesson Markdown does not match authored content")
        guided = subprocess.run([sys.executable, str(ROOT / "tools/check_lesson_delivery.py")], cwd=ROOT, check=False)
        check(guided.returncode == 0, "Per-lesson guided delivery contract failed")
        check(len(list((ROOT / "openmaic/lessons").glob("*.md"))) == 47, "Expected 47 teacher inputs")
        check(len(list((ROOT / "curriculum/lessons").glob("*.md"))) == 47, "Expected 47 student handouts")
        for path in (ROOT / "curriculum/lessons").glob("*.md"):
            check("## 11. 教师反馈" not in path.read_text(encoding="utf-8"), "Teacher answers leaked to student handout")
        pinned = runpy.run_path(str(ROOT / "tools/vendor_openmaic.py"))
        for source, expected_sha in pinned["FILES"].items():
            path = vendor / source.removeprefix("skills/openmaic/")
            check(path.is_file(), f"Missing upstream reference: {source}")
            if path.is_file():
                data = path.read_bytes()
                actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
                check(actual == expected_sha, f"Upstream reference bytes changed: {source}")
        check((vendor / "UPSTREAM.json").is_file(), "Missing upstream provenance")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"COURSE VALIDATION PASS: {checks} checks; 32 concepts, 64 P/T questions; B02 materials preserved")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
