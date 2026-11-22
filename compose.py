#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

One image, six stories, drawn with Pillow only: a masthead naming the
day, a hero story, four panels and a bottom strip. Every word is set
from the strings below, so the text stays crisp at any size.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 36)
NAVY = (16, 42, 78)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
AMBER = (176, 112, 0)
GREEN = (34, 110, 60)
SLATE = (84, 96, 110)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, width, leading=6):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, text, color):
    f = font(BOLD, 17)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 24


def sun(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for a in range(0, 360, 30):
        import math
        x0 = cx + int((r + 6) * math.cos(math.radians(a)))
        y0 = cy + int((r + 6) * math.sin(math.radians(a)))
        x1 = cx + int((r + 16) * math.cos(math.radians(a)))
        y1 = cy + int((r + 16) * math.sin(math.radians(a)))
        d.line([x0, y0, x1, y1], fill=color, width=5)


def star(d, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def flame(d, x, y, s, c1, c2):
    d.polygon([(x, y), (x + s * 0.55, y - s * 0.45), (x + s * 0.4, y - s * 1.0),
               (x + s * 0.75, y - s * 0.7), (x + s, y - s * 0.1),
               (x + s * 0.8, y + s * 0.25), (x + s * 0.2, y + s * 0.25)],
              fill=c1)
    d.polygon([(x + s * 0.3, y), (x + s * 0.5, y - s * 0.4),
               (x + s * 0.7, y), (x + s * 0.5, y + s * 0.15)], fill=c2)


def scales(d, cx, cy, s, color):
    d.line([cx, cy - s, cx, cy + s], fill=color, width=6)
    d.line([cx - s, cy - s * 0.7, cx + s, cy - s * 0.7], fill=color, width=6)
    for sx in (cx - s, cx + s):
        d.line([sx, cy - s * 0.7, sx, cy - s * 0.15], fill=color, width=4)
        d.polygon([(sx - s * 0.55, cy - s * 0.15), (sx + s * 0.55, cy - s * 0.15),
                   (sx, cy + s * 0.35)], fill=color)
    d.rectangle([cx - s * 0.7, cy + s, cx + s * 0.7, cy + s + 8], fill=color)


def quake(d, x, y, w, color):
    pts = [(x, y), (x + w * 0.2, y + 16), (x + w * 0.4, y - 10),
           (x + w * 0.6, y + 18), (x + w * 0.8, y - 4), (x + w, y + 12)]
    d.line(pts, fill=color, width=6, joint="curve")
    d.polygon([(x + 6, y + 58), (x + w * 0.3, y + 26), (x + w * 0.52, y + 58)],
              outline=color, width=4)
    d.polygon([(x + w * 0.55, y + 58), (x + w * 0.78, y + 32),
               (x + w, y + 58)], outline=color, width=4)


def rain(d, x, y, s, color):
    for i, dx in enumerate((0, 34, 68)):
        dy = (i % 2) * 16
        d.ellipse([x + dx, y + dy, x + dx + 16, y + dy + 24], fill=color)
        d.polygon([(x + dx + 8, y + dy - 12), (x + dx, y + dy + 6),
                   (x + dx + 16, y + dy + 6)], fill=color)


def panel(d, x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(205, 198, 184), width=2)
    d.rectangle([x, y, x + w, y + 7], fill=accent)


def story(d, x, y, w, h, accent, tag, head, body, draw_icon):
    panel(d, x, y, w, h, accent)
    ix, iy = x + w - 108, y + 18
    draw_icon(d, ix, iy)
    kicker(d, x + 18, y + 20, tag, accent)
    yy = para(d, x + 18, y + 48, head, font(BOLD, 27), INK, w - 140, leading=4)
    para(d, x + 18, yy + 4, body, font(REG, 18), (52, 58, 68), w - 150,
         leading=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 16), "THE WORLD IN ONE DAY", font=font(BOLD, 52), fill=(255, 255, 255))
    d.text((32, 76), "SUNDAY  •  22 NOVEMBER 2026", font=font(BOLD, 26),
           fill=(255, 201, 60))
    d.text((W - 32, 84), "SIX STORIES", font=font(BOLD, 22),
           fill=(170, 190, 220), anchor="ra")

    # Hero: COP31 climate talks, Antalya.
    hx, hy, hw, hh = 24, 136, 976, 252
    panel(d, hx, hy, hw, hh, TEAL)
    d.rectangle([hx, hy, hx + hw, hy + 7], fill=TEAL)
    sun(d, hx + hw - 105, hy + 78, 42, (255, 176, 32))
    d.arc([hx + hw - 190, hy + 108, hx + hw - 20, hy + 218], 180, 360,
          fill=(14, 110, 110), width=6)
    d.arc([hx + hw - 190, hy + 128, hx + hw - 20, hy + 238], 180, 360,
          fill=(34, 110, 60), width=6)
    kicker(d, hx + 22, hy + 20, "Climate  •  Antalya, Turkey", TEAL)
    para(d, hx + 22, hy + 50, "COP31 talks spill into a second day of overtime",
         font(BOLD, 33), INK, hw - 250, leading=4)
    para(d, hx + 22, hy + 132,
         "A new draft deal aims to avert collapse as nations stay split over "
         "fossil fuels and funding for poorer countries; the EU says it wants "
         "a good deal or no deal.",
         font(REG, 21), (52, 58, 68), hw - 250, leading=6)

    # Four panels, 2 x 2.
    gy, ph, pw = 404, 228, 482
    story(d, 24, gy, pw, ph, RED, "Mexico", "Top drug lord captured",
          "Fausto Isidro Meza Flores, 'El Chapo Isidro', was arrested in a "
          "shoot-out; 11 people were killed in the operation.",
          lambda dd, x, y: star(dd, x + 42, y + 42, 40, (212, 160, 32)))
    story(d, 518, gy, pw, ph, AMBER, "Gulf  •  Bahrain",
          "Iranian attack hits industrial site",
          "Bahrain says Iran set fire to a civilian industrial site; two oil "
          "tankers were hit near the Strait of Hormuz.",
          lambda dd, x, y: flame(dd, x + 8, y + 78, 62, (226, 84, 28), (255, 176, 32)))
    story(d, 24, gy + ph + 14, pw, ph, NAVY, "The Hague  •  Justice",
          "ICJ: Myanmar guilty of genocide",
          "The world court ruled 9-6 that Myanmar committed genocide against "
          "the Rohingya in 2017 — a first for a state.",
          lambda dd, x, y: scales(dd, x + 50, y + 52, 34, NAVY))
    story(d, 518, gy + ph + 14, pw, ph, SLATE, "Peru",
          "Magnitude 6.8 quake shakes Andes",
          "A strong earthquake struck Peru's central Andean region.",
          lambda dd, x, y: quake(dd, x + 4, y + 34, 88, SLATE))

    # Bottom strip: Gaza winter floods.
    sy = gy + 2 * ph + 28
    d.rectangle([24, sy, 1000, sy + 68], fill=(226, 238, 244),
                outline=(205, 198, 184), width=2)
    d.rectangle([24, sy, 1000, sy + 7], fill=(14, 110, 110))
    rain(d, 905, sy + 26, 1, (40, 110, 170))
    kicker(d, 42, sy + 14, "Gaza", TEAL)
    para(d, 150, sy + 20,
         "Winter storms flood shelters for over a million displaced people; "
         "Australia, Canada, Italy and the UK call for aid access.",
         font(REG, 20), INK, 730, leading=4)

    # Footer.
    d.line([24, 972, 1000, 972], fill=(150, 142, 128), width=2)
    d.text((24, 982), "Events first reported on 22 November 2026",
           font=font(BOLD, 18), fill=(52, 58, 68))
    d.text((1000, 982), "BBC  •  Reuters  •  Al Jazeera  •  Xinhua",
           font=font(REG, 18), fill=(84, 96, 110), anchor="ra")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
