"""
Build og-image.png for the "Evolving Agentic Workflows" deck (Frontier Creatives).

Output: 1200 x 630 PNG, for Open Graph / Twitter card.

Composition (left to right):
  - bkg.png as the base layer, with a dark vignette so text stays readable
    and a warm peach radial highlight (top-right), matching the deck background.
  - Pathfinder Foundry lockup (top-left, dot grid + wordmark).
  - Top-right date tag.
  - Eyebrow: FRONTIER CREATIVES · PIONEER SQUARE LABS (PF yellow accent).
  - Two-line headline: "Evolving Agentic / Workflows".
  - Italic serif tagline: "Design thinking, rebuilt for agents." (PF yellow).
  - Marc Krejci byline (bottom-left).
  - Marc's circular avatar (right side, with a PF yellow ring).

Run from the frontier-creatives folder:
  python3 scripts/build-og-image.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
OUT = ROOT / "og-image.png"

WIDTH, HEIGHT = 1200, 630
ACCENT = (255, 204, 100, 255)   # PF Yellow (#FFCC64)
TEXT = (245, 245, 245, 255)
TEXT_MUTED = (168, 168, 168, 255)
VIGNETTE = (12, 18, 20)          # deck's dark teal floor (~#0a1216 / #14242a)


# ---------- Font helpers ----------
def find_font(*candidates):
    for path in candidates:
        if Path(path).exists():
            return path
    return None


SANS_BOLD = find_font(
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)
SANS_REG = find_font(
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
SERIF_ITALIC = find_font(
    "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
)


def font(path, size):
    return ImageFont.truetype(path, size) if path else ImageFont.load_default()


def text_width(draw, s, f):
    bbox = draw.textbbox((0, 0), s, font=f)
    return bbox[2] - bbox[0]


# ---------- Background composition ----------
def make_background():
    base = Image.new("RGB", (WIDTH, HEIGHT), VIGNETTE)

    # Place bkg.png as a cover-fit, centered layer.
    src = Image.open(IMAGES / "bkg.png").convert("RGB")
    sw, sh = src.size
    scale = max(WIDTH / sw, HEIGHT / sh)
    src = src.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
    nw, nh = src.size
    left, top = (nw - WIDTH) // 2, (nh - HEIGHT) // 2
    src = src.crop((left, top, left + WIDTH, top + HEIGHT))
    base.paste(src, (0, 0))

    # Vertical dark vignette so text stays readable (darker top + bottom).
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        if t < 0.18:
            a = int(210 - (210 - 95) * (t / 0.18))      # dark top band
        elif t < 0.55:
            a = int(95 + (150 - 95) * ((t - 0.18) / 0.37))
        else:
            a = int(150 + (190 - 150) * ((t - 0.55) / 0.45))
        od.line([(0, y), (WIDTH, y)], fill=(*VIGNETTE, max(0, min(255, a))))
    composite = Image.alpha_composite(base.convert("RGBA"), overlay)

    # Warm peach radial highlight, top-right (matches the deck's warm glow).
    warm = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    wd = ImageDraw.Draw(warm)
    cx, cy, rmax = int(WIDTH * 0.78), int(HEIGHT * 0.26), 380
    for r in range(rmax, 0, -2):
        a = int(34 * (1 - r / rmax) ** 1.7)
        wd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 200, 200, a))
    warm = warm.filter(ImageFilter.GaussianBlur(radius=14))
    composite = Image.alpha_composite(composite, warm)

    return composite


# ---------- Pathfinder lockup (top-left) ----------
def draw_pf_lockup(draw, x, y, scale=1.0):
    r = int(2.6 * scale)
    gap = int(8 * scale)
    rows = [
        [True, True, True, True],
        [True, True, True, True],
        [True, False, True, False],
    ]
    for ry, row in enumerate(rows):
        for cx, on in enumerate(row):
            if not on:
                continue
            dx, dy = x + cx * gap, y + ry * gap
            draw.ellipse((dx - r, dy - r, dx + r, dy + r), fill=ACCENT)
    word_x = x + 4 * gap + int(10 * scale)
    f_word = font(SANS_REG, int(18 * scale))
    f_word_it = font(SERIF_ITALIC, int(15 * scale))
    draw.text((word_x, y - int(2 * scale)), "pathfinder", font=f_word, fill=TEXT)
    word_w = text_width(draw, "pathfinder", f_word)
    f_w = text_width(draw, "foundry", f_word_it)
    draw.text((word_x + word_w - f_w, y + int(15 * scale)), "foundry",
              font=f_word_it, fill=TEXT)


# ---------- Avatar with PF yellow ring ----------
def make_avatar(diameter):
    src = Image.open(IMAGES / "MKrejci - CircleAvatar - WhiteBorder.png").convert("RGBA")
    sw, sh = src.size
    side = min(sw, sh)
    src = src.crop(((sw - side) // 2, (sh - side) // 2,
                    (sw - side) // 2 + side, (sh - side) // 2 + side))
    src = src.resize((diameter, diameter), Image.LANCZOS)

    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    out.paste(src, (0, 0), mask)

    ring_pad = 14
    ring = Image.new("RGBA", (diameter + ring_pad * 2, diameter + ring_pad * 2), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    for i in range(ring_pad, 0, -1):
        a = int(60 * (i / ring_pad) ** 2)
        rd.ellipse((ring_pad - i, ring_pad - i,
                    diameter + ring_pad + i, diameter + ring_pad + i),
                   outline=(255, 204, 100, a), width=2)
    rd.ellipse((ring_pad - 1, ring_pad - 1, diameter + ring_pad + 1, diameter + ring_pad + 1),
               outline=(255, 204, 100, 220), width=2)
    ring.paste(out, (ring_pad, ring_pad), out)
    return ring


# ---------- Compose ----------
def build():
    img = make_background()
    draw = ImageDraw.Draw(img)

    draw_pf_lockup(draw, 56, 56, scale=1.4)

    # Top-right date tag.
    f_tag = font(SANS_BOLD, 13)
    tag = "JUN 9, 2026"
    draw.text((WIDTH - 56 - text_width(draw, tag, f_tag), 64), tag,
              font=f_tag, fill=(245, 245, 245, 140))

    # Eyebrow.
    f_eyebrow = font(SANS_BOLD, 17)
    draw.text((56, 182), "FRONTIER CREATIVES  ·  PIONEER SQUARE LABS",
              font=f_eyebrow, fill=ACCENT, spacing=4)

    # Headline (two lines).
    f_head = font(SANS_BOLD, 62)
    y = 222
    for line in ["Evolving Agentic", "Workflows"]:
        draw.text((56, y), line, font=f_head, fill=TEXT)
        y += 78

    # Tagline, italic serif accent.
    f_tagline = font(SERIF_ITALIC, 27)
    draw.text((56, y + 16), "Design thinking, rebuilt for agents.",
              font=f_tagline, fill=ACCENT)

    # Byline, bottom-left.
    f_name = font(SANS_BOLD, 22)
    f_role = font(SANS_REG, 16)
    draw.text((56, HEIGHT - 92), "Marc Krejci", font=f_name, fill=TEXT)
    draw.text((56, HEIGHT - 62), "Pathfinder Foundry  ·  pfndr.co",
              font=f_role, fill=TEXT_MUTED)

    # Avatar on the right.
    av = make_avatar(340)
    aw, ah = av.size
    img.alpha_composite(av, (WIDTH - aw - 56, (HEIGHT - ah) // 2 + 16))

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    build()
