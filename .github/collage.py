#!/usr/bin/env python3
"""Compose per-board 3D renders into the README/release collage."""

from __future__ import annotations

import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parents[1] / "build"
OUTPUT = BUILD / "images" / "woki-cam-3d.png"

HERO = ("power", "01 Power")
SIDE = (
    ("fpga_control", "02 FPGA"),
    ("camera", "03 Camera"),
    ("ir_led", "04 IR LED"),
)

W, H = 1800, 1100
PAD, GAP = 36, 24
LABEL_GAP, FONT_SIZE = 8, 20
LEFT_FRAC = 0.62
TRIM_PAD = 16
HERO_FILL = 0.90
SIDE_FILL = 0.58
ISO_FRAC = 0.52
TEXT = (32, 32, 32, 255)


def trim(image, pad: int = TRIM_PAD):
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return image
    l, t, r, b = bbox
    return image.crop(
        (max(0, l - pad), max(0, t - pad), min(image.width, r + pad), min(image.height, b + pad))
    )


def load(path: Path, required: bool = False):
    from PIL import Image, ImageDraw

    if path.is_file() and path.stat().st_size > 0:
        return trim(Image.open(path).convert("RGBA"))
    if required:
        sys.exit(f"Missing required render: {path}")
    ph = Image.new("RGBA", (640, 480), (0, 0, 0, 0))
    ImageDraw.Draw(ph).text((24, 220), "No render", fill=(140, 140, 140, 255))
    return ph


def fit(image, max_w: int, max_h: int, fill: float):
    from PIL import Image

    max_w, max_h = int(max_w * fill), int(max_h * fill)
    scale = min(max_w / image.width, max_h / image.height)
    nw, nh = max(1, int(image.width * scale)), max(1, int(image.height * scale))
    if nw == image.width and nh == image.height:
        return image
    return image.resize((nw, nh), Image.Resampling.LANCZOS)


def paste_center(canvas, image, x: int, y: int, w: int, h: int) -> None:
    canvas.paste(image, (x + (w - image.width) // 2, y + (h - image.height) // 2), image)


def paste_bottom(canvas, image, x: int, y: int, w: int, h: int) -> None:
    canvas.paste(image, (x + (w - image.width) // 2, y + h - image.height), image)


def main() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Pillow required: pip install pillow")

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    label_h = FONT_SIZE + 10
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    left_w = int(W * LEFT_FRAC) - PAD - GAP // 2
    right_x = PAD + left_w + GAP
    right_w = W - right_x - PAD
    top, bottom = PAD, H - PAD

    name, label = HERO
    hero_dir = BUILD / name / "images"
    box_h = bottom - top - label_h - LABEL_GAP
    split_gap = GAP // 2
    iso_h = int((box_h - split_gap) * ISO_FRAC)
    bottom_h = box_h - split_gap - iso_h

    iso_path = hero_dir / f"{name}-3d-iso.png"
    bottom_path = hero_dir / f"{name}-3d-bottom.png"

    paste_center(
        canvas,
        fit(load(iso_path, required=True), left_w, iso_h, HERO_FILL),
        PAD,
        top,
        left_w,
        iso_h,
    )
    bottom_y = top + iso_h + split_gap
    paste_bottom(
        canvas,
        fit(load(bottom_path, required=True), left_w, bottom_h, HERO_FILL),
        PAD,
        bottom_y,
        left_w,
        bottom_h,
    )
    draw.text((PAD + 4, top + box_h + LABEL_GAP), label, fill=TEXT, font=font)

    n = len(SIDE)
    row_h = (bottom - top - GAP * (n - 1)) // n
    img_h = row_h - label_h - LABEL_GAP

    for i, (board, lbl) in enumerate(SIDE):
        y = top + i * row_h + i * GAP
        paste_center(
            canvas,
            fit(load(BUILD / board / "images" / f"{board}-3d.png"), right_w, img_h, SIDE_FILL),
            right_x,
            y,
            right_w,
            img_h,
        )
        draw.text((right_x + 4, y + img_h + LABEL_GAP), lbl, fill=TEXT, font=font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, format="PNG", optimize=True)
    print(f"WRITE: {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
