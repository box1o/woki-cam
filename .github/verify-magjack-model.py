#!/usr/bin/env python3
"""Fail CI if the power-board MagJack loses its persistent 3D model link."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
pcb = (root / "boards/01-power/power.kicad_pcb").read_text()
footprint = (root / "lib/footprints/woki.pretty/Bel_0826_1X1T_HS_F.kicad_mod").read_text()
model = root / "lib/3dmodels/manufacturer/bel-0826-1x1t-hs-f.wrl"
relative = "${KIPRJMOD}/../../lib/3dmodels/manufacturer/bel-0826-1x1t-hs-f.wrl"
failures = []
if not model.is_file() or model.stat().st_size < 1000:
    failures.append("Missing or empty MagJack VRML file")
if relative not in footprint:
    failures.append("MagJack footprint library is missing its 3D model association")
start = pcb.find('(footprint "Woki:Bel_0826_1X1T_HS_F"')
if start < 0:
    failures.append("J2 MagJack footprint missing from saved power PCB")
else:
    next_footprint = pcb.find('\n\t(footprint ', start + 1)
    block = pcb[start:next_footprint if next_footprint >= 0 else len(pcb)]
    if relative not in block:
        failures.append("J2's saved PCB footprint is missing its 3D model association")
    if not re.search(r'\(property "Reference" "J2"', block):
        failures.append("MagJack footprint is not J2")
# Verify the inch-based source is converted and placed correctly in KiCad.
if model.is_file() and not model.read_bytes().startswith(b"#VRML V2.0"):
    failures.append("MagJack mesh must use supported VRML 2.0 syntax")
for label, text in [("footprint library", footprint), ("saved PCB footprint", block if start >= 0 else "")]:
    model_start = text.find('(model "' + relative + '"')
    section = text[model_start:] if model_start >= 0 else ""
    for field, expected in [("offset", (0, 10.668, 0.9906)), ("scale", (10, 10, 10)), ("rotate", (270, 0, 180))]:
        match = re.search(r"\(" + field + r"\s+\(xyz\s+([^)]*)\)\)", section)
        actual = tuple(map(float, match[1].split())) if match else ()
        if len(actual) != 3 or any(abs(a-b) > 0.000001 for a, b in zip(actual, expected)):
            failures.append(f"Incorrect MagJack {field} in {label}: {actual}")
if failures:
    sys.exit("\n".join(failures))
print("PASS: J2 and footprint library both reference the committed MagJack 3D model")
