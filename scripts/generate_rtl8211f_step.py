#!/usr/bin/env python3
"""Generate the nominal RTL8211F-CG STEP model using FreeCAD's Python modules.

Run with the Python interpreter that can import FreeCAD and Part, e.g. on
Debian: PYTHONPATH=/usr/lib/freecad/lib /usr/bin/python3 scripts/generate_rtl8211f_step.py
"""

from pathlib import Path

import FreeCAD
import Part

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "lib/3dmodels/downloaded/RTL8211F_C187932.step"

# Realtek JATR-8275-15 rev. 1.4, §11/11.1 (datasheets/rtl8211f.pdf), mm.
BODY = 5.00  # D/E
HEIGHT = 0.85  # A
STANDOFF = 0.02  # A1
LEADFRAME = 0.20  # A3, reference
PAD = 3.70  # D2/E2
PITCH = 0.40  # e
LEAD_WIDTH = 0.20  # b
LEAD_LENGTH = 0.40  # L, including the rounded inner end
LEADS_PER_SIDE = 10


def build_package():
    """Construct the molded body, 40 terminals, and exposed pad as solids."""
    vector = FreeCAD.Vector
    half = BODY / 2
    radius = LEAD_WIDTH / 2
    leads = []
    # Section 11 detail A shows a flat outer end and a rounded inner end.
    for side in range(4):
        for index in range(LEADS_PER_SIDE):
            y = (index - (LEADS_PER_SIDE - 1) / 2) * PITCH
            x = half - LEAD_LENGTH + radius
            outer = Part.makeBox(LEAD_LENGTH - radius, LEAD_WIDTH, LEADFRAME,
                                 vector(x, y - radius, 0))
            inner = Part.makeCylinder(radius, LEADFRAME, vector(x, y, 0))
            lead = outer.fuse(inner).removeSplitter()
            lead.rotate(vector(0, 0, 0), vector(0, 0, 1), side * 90)
            leads.append(lead)

    exposed_pad = Part.makeBox(PAD, PAD, LEADFRAME, vector(-PAD / 2, -PAD / 2, 0))
    metal = Part.Compound([*leads, exposed_pad])
    mold = Part.makeBox(BODY, BODY, HEIGHT - STANDOFF, vector(-half, -half, STANDOFF))
    mold = mold.cut(metal).removeSplitter()
    # Cosmetic laser marking and optional pad notch aren't dimensioned. Leave
    # those out of the nominal MCAD model rather than inventing dimensions.
    return Part.Compound([mold, *leads, exposed_pad])


def validate(shape):
    bounds = shape.BoundBox
    pairs = zip((bounds.XLength, bounds.YLength, bounds.ZLength, bounds.ZMin),
                (BODY, BODY, HEIGHT, 0.0))
    if not all(abs(actual - expected) < 1e-6 for actual, expected in pairs):
        raise ValueError(f"Unexpected package bounds: {bounds}")
    count = 2 + 4 * LEADS_PER_SIDE
    if len(shape.Solids) != count or not shape.isValid():
        raise ValueError(f"Expected {count} valid solids, got {len(shape.Solids)}")


def main():
    shape = build_package()
    validate(shape)
    shape.exportStep(str(OUTPUT))
    # OCCT pads a few entity lines with spaces. Keep the checked-in text clean.
    lines = OUTPUT.read_bytes().splitlines()
    OUTPUT.write_bytes(b"\n".join(line.rstrip() for line in lines) + b"\n")
    validate(Part.read(str(OUTPUT)))


if __name__ == "__main__":
    main()
