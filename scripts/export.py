#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "mechanical" / "freecad"

BOARDS = (
    ("01-power", "power"),
    ("02-fpga-control", "fpga_control"),
    ("03-camera", "camera"),
    ("04-ir-led", "ir_led"),
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export KiCad STEP models.")
    parser.add_argument(
        "--rewrite",
        action="store_true",
        help="Overwrite existing STEP files",
    )
    args = parser.parse_args()

    kicad_cli = shutil.which("kicad-cli")
    if not kicad_cli:
        sys.exit("kicad-cli not found on PATH")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for board_dir, basename in BOARDS:
        pcb = ROOT / "boards" / board_dir / f"{basename}.kicad_pcb"
        if not pcb.is_file():
            sys.exit(f"Missing PCB: {pcb}")

        step_path = OUTPUT_DIR / f"{basename}.step"
        if step_path.is_file() and not args.rewrite:
            print(f"SKIP: {step_path}")
            continue

        cmd = [
            kicad_cli,
            "pcb",
            "export",
            "step",
            str(pcb),
            "-o",
            str(step_path),
            "--subst-models",
        ]
        if args.rewrite:
            cmd.append("--force")

        print(f"RUN: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            sys.exit(f"STEP export failed for {basename} (exit {result.returncode})")

        print(f"WRITE: {step_path}")

    print("Done.")


if __name__ == "__main__":
    main()
