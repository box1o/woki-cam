#!/usr/bin/env python3
"""Ensure the Bel MagJack's existing PCB footprint has its 3D model attached.

KiCad embeds footprints in .kicad_pcb; editing the library alone does not update
already placed components. This script edits the checked-out board for rendering.
"""
from pathlib import Path
import re
import sys

PCB = Path("boards/01-power/power.kicad_pcb")
MODEL = "${KIPRJMOD}/../../lib/3dmodels/manufacturer/Bel_0826-1X1T-HS-F.wrl"
MODEL_BLOCK = f'''\n    (model "{MODEL}"
      (offset (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )'''

def end_of_form(s: str, start: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for i in range(start, len(s)):
        ch = s[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unbalanced KiCad footprint expression")

def main():
    text = PCB.read_text()
    matches = list(re.finditer(r'\(footprint\s+"([^"]+)"', text))
    updated = 0
    found = 0
    for m in reversed(matches):
        start = m.start()
        end = end_of_form(text, start)
        block = text[start:end + 1]
        if "Bel_0826_1X1T_HS_F" not in m.group(1) and "0826-1X1T-HS-F" not in block:
            continue
        found += 1
        if MODEL in block:
            continue
        # Replace a previous model association if present, rather than layering meshes.
        for old in reversed(list(re.finditer(r'\(model\s+"[^"]+"', block))):
            oe = end_of_form(block, old.start())
            block = block[:old.start()] + block[oe+1:]
        block = block[:-1] + MODEL_BLOCK + "\n  )"
        text = text[:start] + block + text[end+1:]
        updated += 1
    if not found:
        sys.exit("Bel 0826 MagJack footprint not found on power PCB")
    if updated:
        PCB.write_text(text)
    print(f"Bel MagJack footprint(s): {found}; model attachments updated: {updated}")

if __name__ == "__main__":
    main()
