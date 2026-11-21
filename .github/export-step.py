#!/usr/bin/env python3
"""Export STEP without VRML-only models, preserving the checked-in PCB and previews."""

import argparse
from pathlib import Path
import re
import subprocess
import tempfile


def without_vrml_models(board):
    """Remove only unsupported VRML model blocks from a temporary PCB copy."""
    pattern = re.compile(r'\(model\s+"[^"]+\.wrl"', re.IGNORECASE)
    removed = []
    cursor = 0
    result = []
    for match in pattern.finditer(board):
        start = match.start()
        if start < cursor:
            continue
        depth = 0
        in_string = False
        escaped = False
        end = None
        for i in range(start, len(board)):
            char = board[i]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
            elif char == '"':
                in_string = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            raise ValueError("Unterminated VRML model block")
        result.append(board[cursor:start])
        removed.append(match.group(0))
        cursor = end
    result.append(board[cursor:])
    return "".join(result), removed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pcb", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    original = args.pcb.read_text(encoding="utf-8")
    cleaned, removed = without_vrml_models(original)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.pcb.parent, prefix=".step-export-") as tmp:
        # KIPRJMOD is the PCB directory, so use the original board directory.
        # A temporary subdirectory would break relative 3D model paths.
        tmp_pcb = args.pcb.parent / (Path(tmp).name + ".kicad_pcb")
        try:
            tmp_pcb.write_text(cleaned, encoding="utf-8")
            for model in removed:
                print(f"STEP: skipping unsupported VRML-only model: {model}", flush=True)
            subprocess.run([
                "kicad-cli", "pcb", "export", "step",
                "-o", str(args.output), "-f", "--grid-origin",
                "--subst-models", "--include-silkscreen",
                "--include-soldermask", str(tmp_pcb)
            ], check=True)
        finally:
            tmp_pcb.unlink(missing_ok=True)
    if not args.output.is_file() or args.output.stat().st_size == 0:
        raise RuntimeError("STEP export did not create a non-empty file")


if __name__ == "__main__":
    main()
