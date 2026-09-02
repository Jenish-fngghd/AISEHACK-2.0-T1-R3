"""Combine four shipped figures into one 2x2 panel for the midnight check-in PDF.

Panels: A the deliverable, B the D1 consistency check, C value of information
per acquisition, D re-flight stability of the attention list.
No new analysis - this only assembles PNGs that src/p3_figures.py already wrote.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FIG = Path(__file__).resolve().parents[1] / "results" / "figures"
PANELS = [("A", "p3_f1_deliverable.png"), ("B", "p3_f3_d1.png"),
          ("C", "p3_f7_voi.png"),         ("D", "p3_f8_speckle.png")]
CELL_W, CELL_H, PAD = 2084, 900, 24


def font(size):
    for name in ("arialbd.ttf", "seguisb.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def cell(path, letter):
    im = Image.open(path).convert("RGB")
    s = min(CELL_W / im.width, CELL_H / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    box = Image.new("RGB", (CELL_W, CELL_H), "white")
    box.paste(im, ((CELL_W - im.width) // 2, (CELL_H - im.height) // 2))
    d = ImageDraw.Draw(box)
    d.rectangle([0, 0, CELL_W - 1, CELL_H - 1], outline=(200, 200, 200), width=3)
    d.text((18, 12), letter, fill=(20, 20, 20), font=font(58))
    return box


def main():
    missing = [f for _, f in PANELS if not (FIG / f).exists()]
    if missing:
        raise SystemExit(f"missing source figures: {missing} - run src/p3_figures.py first")
    cells = [cell(FIG / f, L) for L, f in PANELS]
    W = CELL_W * 2 + PAD * 3
    H = CELL_H * 2 + PAD * 3
    out = Image.new("RGB", (W, H), "white")
    for i, c in enumerate(cells):
        x = PAD + (i % 2) * (CELL_W + PAD)
        y = PAD + (i // 2) * (CELL_H + PAD)
        out.paste(c, (x, y))
    dst = FIG / "checkin_composite.png"
    out.save(dst, optimize=True)
    print(f"{dst}  {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf8")
    main()
