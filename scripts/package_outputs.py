#!/usr/bin/env python3
"""Package board previews, schematic PDFs and checked draft outputs."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from project import BOARDS, ROOT

BUILD = ROOT / "build"
SKIP_DIRS = frozenset({".cache", "__pycache__", ".git"})
SKIP_SUFFIX = frozenset({".log", ".Zone.Identifier"})


def load_settings() -> dict[str, str]:
    env_file = ROOT / os.environ.get("SETTINGS_FILE", "settings.env")
    if not env_file.is_file():
        sys.exit(f"Missing {env_file}")
    out: dict[str, str] = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def zip_build(package_name: str) -> Path:
    zip_path = BUILD / "release" / f"{package_name}.zip"
    files = sorted(
        p
        for p in BUILD.rglob("*")
        if p.is_file()
        and not any(part in SKIP_DIRS for part in p.relative_to(BUILD).parts)
        and p.suffix not in SKIP_SUFFIX
        and not (p.parent.name == "release" and p.suffix == ".zip")
    )
    if not files:
        sys.exit("No files to zip under build/")

    total = sum(p.stat().st_size for p in files)
    print(f"Zipping {len(files)} files ({total / 1_000_000:.1f} MB uncompressed)")

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", ZIP_DEFLATED, compresslevel=6) as zf:
        for i, path in enumerate(files, 1):
            zf.write(path, path.relative_to(BUILD))
            if i % 25 == 0 or i == len(files):
                print(f"  packed {i}/{len(files)}")

    mb = zip_path.stat().st_size / 1_000_000
    print(f"WRITE: {zip_path} ({mb:.1f} MB)")
    return zip_path


def main() -> None:
    settings = load_settings()
    release_board = settings.get("RELEASE_BOARD", "power")
    package_name = settings.get("PACKAGE_NAME", "woki-cam")

    subprocess.run(
        [sys.executable, str(ROOT / "scripts/render_collage.py")], check=True
    )

    schematic = BUILD / release_board / "docs" / f"{release_board}-schematic.pdf"
    if not schematic.is_file() or schematic.stat().st_size == 0:
        sys.exit(f"Missing required schematic PDF: {schematic}")
    dest = BUILD / "docs" / "woki-cam-schematic.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(schematic.read_bytes())
    print(f"COPY: {dest}")

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/check_layout.py"),
            str(BUILD),
            "--expected-reports",
            str(len(BOARDS)),
        ],
        check=True,
    )
    layout = json.loads((BUILD / "layout-status.json").read_text())
    status_text = (
        "PCB layout checks passed.\n"
        if layout["manufacturing_ready"]
        else "DRAFT PCB PACKAGE — NOT READY FOR MANUFACTURE.\n"
        "Resolve DRC issues and unrouted connections first.\n"
    )
    (BUILD / "readme.txt").write_text(
        status_text + "See layout-status.json and per-board checks/.\n"
    )

    preview = BUILD / "images" / "woki-cam-3d.png"
    if not preview.is_file():
        sys.exit("Missing generated board preview")

    def source_entry(path: Path, base: Path) -> dict[str, str]:
        return {
            "path": path.relative_to(base).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    manifest = {
        "source_commit": os.environ.get("GITHUB_SHA", "local"),
        "preview": source_entry(preview, BUILD),
        "boards": [
            source_entry(
                ROOT / "boards" / b["directory"] / f"{b['board']}.kicad_pcb", ROOT
            )
            for b in BOARDS
        ],
        "models": [
            source_entry(path, ROOT)
            for path in sorted((ROOT / "lib" / "3dmodels").rglob("*.step"))
        ],
    }
    manifest_path = BUILD / "release" / "preview-sources.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    zip_build(package_name)


if __name__ == "__main__":
    main()
