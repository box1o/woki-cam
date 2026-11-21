#!/usr/bin/env python3
"""Export the four KiCad boards as STEP assemblies."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

from project import BOARDS, ROOT, board_file

OUTPUT_DIR = ROOT / "mechanical" / "freecad"


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

    for board in BOARDS:
        basename = board["board"]
        pcb = board_file(board, "kicad_pcb")
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
