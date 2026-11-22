#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

Draws a newspaper front page with PIL: masthead, red dateline, main story
(Mexico captures 'El Chapo Isidro'), second story (Gen Z protests, day two),
a four-item bottom row and an ALSO strip. Deterministic: fixed layout, no
randomness, no timestamps, no network. All text is baked into this script.
"""
import math

from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/makefun/news-image-22nov/entry.png"
W = H = 1024
PAPER = (247, 240, 221)
PANEL = (232, 222, 196)
INK = (26, 26, 26)
RED = (178, 34, 34)
GREY = (110, 105, 90)
BLUE = (30, 60, 110)
GOLD = (245, 180, 40)
TAN = (176, 160, 140)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def load(path, size):
    return ImageFont.truetype(path, size)


def width(s, f):
    return d.textlength(s, font=f)


def shrink(text, path, size, max_w):
    """Biggest size at or under `size` that fits `text` in `max_w`."""
    while size > 10 and width(text, load(path, size)) > max_w:
        size -= 2
    return size


def pair_size(line1, line2, path, size, max_w):
    """One shared size so two headline lines sit evenly."""
    return min(shrink(line1, path, size, max_w),
               shrink(line2, path, size, max_w))


def wrap_text(s, f, max_w):
    """Greedy word wrap of `s` to lines fitting `max_w`."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if width(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(y, s, f, fill=INK):
    d.text(((W - width(s, f)) / 2, y), s, font=f, fill=fill)


def centred_in(cx, y, s, f, fill=INK):
    d.text((cx - width(s, f) / 2, y), s, font=f, fill=fill)


def hline(y, w=3, x0=32, x1=992):
    d.line([(x0, y), (x1, y)], fill=INK, width=w)


def para(x, y, s, f, max_w, leading):
    """Draw a wrapped paragraph; return the y just below its last line."""
    for line in wrap_text(s, f, max_w):
        d.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def starburst(cx, cy, r, fill):
    """Twelve-point star, alternating long and short spikes."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.55
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def draw_wanted_poster(x0, y0, x1, y1):
    """WANTED poster: red heading, dark silhouette, caption below."""
    d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=3)
    cx = (x0 + x1) / 2
    centred_in(cx, y0 + 10, "WANTED", load(SANS_B, 30), RED)
    # silhouette: round head, trapezoid shoulders
    d.ellipse([cx - 33, y0 + 56, cx + 33, y0 + 122], fill=INK)
    d.polygon([(cx - 44, y1 - 8), (cx + 44, y1 - 8),
               (cx + 30, y0 + 148), (cx - 30, y0 + 148)], fill=INK)
    centred_in(cx, y1 + 8, "EL CHAPO ISIDRO", load(SANS_B, 18), INK)
    centred_in(cx, y1 + 30, "11 KILLED IN THE RAID", load(SANS_B, 18), RED)


def draw_crowd(cx, cy):
    """Three marchers: heads and shoulders in red, ink and blue."""
    for dx, r, fill in ((-90, 17, RED), (0, 19, INK), (90, 17, BLUE)):
        hx = cx + dx
        d.ellipse([hx - r, cy - r, hx + r, cy + r], fill=fill)
        d.pieslice([hx - 30, cy + 12, hx + 30, cy + 56], 180, 360, fill=fill)


def draw_sun(cx, cy):
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=GOLD)
    for i in range(8):
        ang = math.pi * i / 4
        x1 = cx + 26 * math.cos(ang)
        y1 = cy + 26 * math.sin(ang)
        x2 = cx + 34 * math.cos(ang)
        y2 = cy + 34 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=4)


def draw_radar(cx, cy):
    for r in (12, 22, 32):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=270, end=360,
              fill=BLUE, width=3)
    d.line([(cx, cy), (cx + 30, cy - 8)], fill=BLUE, width=3)
    d.ellipse([cx + 18, cy - 22, cx + 26, cy - 14], fill=RED)


def draw_planet(cx, cy):
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=TAN)
    for dx, dy, r in ((-8, -6, 4), (7, 4, 3), (-2, 10, 3)):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=(140, 125, 110))
    d.arc([cx - 36, cy - 12, cx + 36, cy + 12], start=200, end=340,
          fill=GREY, width=2)


# ---- Masthead ----
centred(6, "THE WORLD", load(SERIF_B, 118))
hline(138, 4)
hline(146, 2)

# ---- Dateline ----
centred(158, "SUNDAY, 22 NOVEMBER 2026", load(SANS_B, 44), RED)
centred(206, "THE DAY'S WORLD NEWS  —  IN ONE PAGE", load(SANS, 21), GREY)
hline(240, 3)

# ---- Main story: Mexico captures El Chapo Isidro ----
MX, MW = 32, 620
d.text((MX, 256), "MEXICO  —  CARTEL CRACKDOWN",
       font=load(SANS_B, 25), fill=RED)
msize = pair_size("EL CHAPO", "ISIDRO CAPTURED", SERIF_B, 66, MW)
mf = load(SERIF_B, msize)
d.text((MX, 288), "EL CHAPO", font=mf, fill=INK)
d.text((MX, 354), "ISIDRO CAPTURED", font=mf, fill=INK)
deck = ("FBI most-wanted drug lord seized in northern Mexico; 11 killed "
        "as the arrest sparks gunfights in Sinaloa.")
y = para(MX, 426, deck, load(SERIF, 27), MW, 32)
print("main deck ends at y =", y)
assert y <= 524, f"main deck overflows: y={y}"
draw_wanted_poster(700, 258, 962, 478)
hline(530, 3)

# ---- Second story: Gen Z protests, day two ----
d.text((MX, 546), "EUROPE  —  GEN Z, DAY TWO",
       font=load(SANS_B, 25), fill=RED)
ssize = pair_size("GEN Z PROTESTS", "DAY TWO IN EUROPE", SERIF_B, 60, MW)
sf = load(SERIF_B, ssize)
d.text((MX, 578), "GEN Z PROTESTS", font=sf, fill=INK)
d.text((MX, 638), "DAY TWO IN EUROPE", font=sf, fill=INK)
deck2 = ("82,500 march in France, 144 detained; Italy's transport "
         "strike halts trains.")
y = para(MX, 700, deck2, load(SERIF, 27), MW, 33)
print("second deck ends at y =", y)
assert y <= 768, f"second deck overflows: y={y}"
draw_crowd(830, 632)
centred_in(830, 700, "82,500 IN FRANCE", load(SANS_B, 19), RED)
hline(774, 3)

# ---- Bottom row: four items ----
COL_W, GAP, BX, BY = 224, 16, 32, 788
items = [
    ("CLIMATE", "COP31 DEADLOCK DRAGS ON",
     "Fossil-fuel row pushes talks into overtime.", "sun"),
    ("BAHRAIN", "IRGC TARGETS US RADAR",
     "Tehran says it hit US radar sites in Bahrain.", "radar"),
    ("WASHINGTON", "TRUMP: CAP CARD RATES AT 10%",
     "Vow to cap credit-card interest at 10%.", "pct"),
    ("SPACE", "BEPICOLOMBO AT MERCURY",
     "ESA/JAXA probe starts its Mercury burn.", "planet"),
]
for i, (kick, head, body, icon) in enumerate(items):
    x = BX + i * (COL_W + GAP)
    d.text((x, BY), kick, font=load(SANS_B, 22), fill=RED)
    if icon == "sun":
        draw_sun(x + 28, BY + 52)
    elif icon == "radar":
        draw_radar(x + 28, BY + 52)
    elif icon == "pct":
        centred_in(x + 28, BY + 30, "10%", load(SERIF_B, 40), RED)
    elif icon == "planet":
        draw_planet(x + 28, BY + 52)
    hy = BY + 80
    hf = load(SANS_B, 21)
    hlines = wrap_text(head, hf, COL_W)
    assert len(hlines) <= 2, f"bottom headline {i} wraps to {len(hlines)}"
    for line in hlines:
        d.text((x, hy), line, font=hf, fill=INK)
        hy += 26
    by = hy + 6
    bf = load(SERIF, 19)
    blines = wrap_text(body, bf, COL_W)
    assert len(blines) <= 2, f"bottom body {i} wraps to {len(blines)}"
    for line in blines:
        d.text((x, by), line, font=bf, fill=INK)
        by += 24
    print(f"bottom item {i} ends at y =", by)
    assert by <= 976, f"bottom item {i} overflows: by={by}"

# ---- ALSO strip ----
hline(982, 2)
also = ("ALSO:  Brussels flights cancelled  ·  Gaza aid call  ·  "
        "Seattle ICE arrests  ·  Nigeria boat toll 24")
af = load(SANS, 17)
assert width(also, af) <= 960, "ALSO strip too wide"
d.text((32, 990), also, font=af, fill=GREY)

img.save(OUT)
print("saved", OUT)
