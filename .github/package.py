#!/usr/bin/env python3
"""Build release collage, schematic copy, and manufacturing zip."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
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
        p for p in BUILD.rglob("*")
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

    subprocess.run([sys.executable, str(ROOT / ".github/collage.py")], check=True)

    schematic = BUILD / release_board / "docs" / f"{release_board}-schematic.pdf"
    if schematic.is_file() and schematic.stat().st_size > 0:
        dest = BUILD / "docs" / "woki-cam-schematic.pdf"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(schematic.read_bytes())
        print(f"COPY: {dest}")

    zip_build(package_name)


if __name__ == "__main__":
    main()
