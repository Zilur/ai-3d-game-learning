#!/usr/bin/env python3
"""CI-only: download one pinned official Linux Godot asset and verify its digest.
Does not read tokens or install into system directories. Requires network access.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import urllib.request
import zipfile

VERSION = "4.7.2"
BINARY = f"Godot_v{VERSION}-stable_linux.x86_64"
ASSET = BINARY + ".zip"
API = f"https://api.github.com/repos/godotengine/godot-builds/releases/tags/{VERSION}-stable"


def request(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-3d-game-learning-ci"})
    return urllib.request.urlopen(req, timeout=120)


def main() -> None:
    if not os.environ.get("RUNNER_TEMP"):
        raise RuntimeError("This installer is for GitHub Actions. Install Godot normally on your own computer.")
    destination = Path(os.environ["RUNNER_TEMP"]) / "godot-verified"
    destination.mkdir(parents=True, exist_ok=True)
    with request(API) as response:
        release = json.load(response)
    assets = [item for item in release["assets"] if item["name"] == ASSET]
    if len(assets) != 1:
        raise RuntimeError(f"Expected one official asset named {ASSET}")
    asset = assets[0]
    digest = asset.get("digest", "")
    if not digest.startswith("sha256:"):
        raise RuntimeError("Official SHA-256 digest missing; refusing unverified install")
    with tempfile.TemporaryDirectory(dir=destination) as temporary:
        archive = Path(temporary) / ASSET
        with request(asset["browser_download_url"]) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
        with archive.open("rb") as source:
            actual = hashlib.file_digest(source, "sha256").hexdigest()
        if actual != digest.removeprefix("sha256:"):
            raise RuntimeError("Godot archive checksum mismatch")
        # Extract exactly one expected entry; do not extract arbitrary archive paths.
        with zipfile.ZipFile(archive) as package:
            with package.open(BINARY) as source, (destination / "godot").open("wb") as output:
                shutil.copyfileobj(source, output)
    (destination / "godot").chmod(0o755)
    with open(os.environ["GITHUB_PATH"], "a", encoding="utf-8") as path_file:
        path_file.write(str(destination) + "\n")
    print(f"Verified {ASSET} ({digest})")


if __name__ == "__main__":
    main()
