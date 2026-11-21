#!/usr/bin/env python3
"""Fail CI if the power-board MagJack loses its persistent 3D model link."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
pcb = (root / "boards/01-power/power.kicad_pcb").read_text()
footprint = (root / "lib/footprints/woki.pretty/Bel_0826_1X1T_HS_F.kicad_mod").read_text()
model = root / "lib/3dmodels/manufacturer/Bel_0826-1X1T-HS-F.wrl"
relative = "${KIPRJMOD}/../../lib/3dmodels/manufacturer/Bel_0826-1X1T-HS-F.wrl"
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
if failures:
    sys.exit("\n".join(failures))
print("PASS: J2 and footprint library both reference the committed MagJack 3D model")
