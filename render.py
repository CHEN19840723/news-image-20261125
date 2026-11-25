"""Draw the 25 November 2026 front page (1024x1024) with Pillow.

No network, no randomness: the same run always produces the same PNG.
Run directly (`python3 render.py`) to write entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (22, 35, 63)
NAVY_LIGHT = (31, 48, 84)
RED = (178, 34, 34)
CREAM = (247, 243, 232)
INK = (24, 24, 24)
GREY = (90, 90, 90)
STRIP_BG = (232, 238, 246)
GOLD = (232, 164, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def draw_rocket(draw, bx, by, bw, bh):
    """A small stylised rocket on a navy sky, inside box (bx, by, bw, bh)."""
    draw.rectangle([bx, by, bx + bw, by + bh], fill=NAVY_LIGHT)
    cx = bx + bw // 2
    # stars
    for sx, sy, r in [(30, 30, 4), (70, 55, 3), (bw - 40, 35, 4),
                      (bw - 70, 90, 3), (45, bh - 45, 3), (bw - 45, bh - 30, 4),
                      (bw // 2 - 90, 70, 3)]:
        draw.ellipse([bx + sx - r, by + sy - r, bx + sx + r, by + sy + r],
                     fill=(255, 255, 255))
    top = by + 28
    body_w, body_h = 74, 118
    x0, x1 = cx - body_w // 2, cx + body_w // 2
    y0, y1 = top + 34, top + 34 + body_h
    # fins
    draw.polygon([(x0, y1 - 52), (x0 - 34, y1 + 6), (x0, y1 - 6)], fill=RED)
    draw.polygon([(x1, y1 - 52), (x1 + 34, y1 + 6), (x1, y1 - 6)], fill=RED)
    # body and nose cone
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    draw.polygon([(x0, y0), (x1, y0), (cx, top)], fill=RED)
    # window
    draw.ellipse([cx - 13, y0 + 26, cx + 13, y0 + 52], fill=NAVY)
    # flame
    draw.polygon([(cx - 16, y1), (cx + 16, y1), (cx, y1 + 52)], fill=GOLD)
    draw.polygon([(cx - 8, y1), (cx + 8, y1), (cx, y1 + 30)], fill=RED)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 110], fill=NAVY)
    d.text((36, 30), "THE WORLD TODAY",
           font=font(SERIF, 52), fill=(255, 255, 255))
    d.text((988, 24), "WEDNESDAY", font=font(SANS_BOLD, 32),
           fill=(255, 255, 255), anchor="ra")
    d.text((988, 62), "25 NOVEMBER 2026", font=font(SANS_BOLD, 24),
           fill=(200, 205, 220), anchor="ra")
    d.rectangle([0, 110, W, 118], fill=RED)

    # ---- lead story ----------------------------------------------------
    d.text((36, 142), "LEAD  \u00b7  SPACE", font=font(SANS_BOLD, 21),
           fill=RED)
    d.text((36, 172), "Pakistan's first astronaut",
           font=font(SERIF, 46), fill=INK)
    d.text((36, 224), "reaches orbit",
           font=font(SERIF, 46), fill=INK)
    lead_body = (
        "China's Shenzhou-24 lifted off at 08:18 on Wednesday carrying "
        "Tang Hongbo, Wu Yi and Pakistani payload specialist Muhammad "
        "Zeeshan Ali \u2014 the first Pakistani in orbit and the first "
        "foreign astronaut aboard Tiangong.")
    para(d, 36, 292, lead_body, font(SANS, 23), 622, 32)

    draw_rocket(d, 700, 142, 288, 216)
    d.text((700, 368), "Shenzhou-24 to Tiangong",
           font=font(SANS_ITALIC, 19), fill=(70, 80, 105))

    d.line([(36, 442), (988, 442)], fill=(190, 180, 160), width=2)

    # ---- two middle stories --------------------------------------------
    col_y = 462
    d.text((36, col_y), "BUSINESS  \u00b7  UNITED STATES",
           font=font(SANS_BOLD, 20), fill=RED)
    d.text((36, col_y + 28), "Huawei convicted in US",
           font=font(SERIF, 30), fill=INK)
    d.text((36, col_y + 64), "trial \u2014 10 of 12 counts",
           font=font(SERIF, 30), fill=INK)
    huawei = (
        "A Brooklyn jury found the telecom giant guilty of bank fraud "
        "and trade-secret theft on Tuesday, but cleared it of "
        "racketeering. Sentencing is September 2027.")
    para(d, 36, col_y + 112, huawei, font(SANS, 21), 448, 30)

    d.text((520, col_y), "MIDDLE EAST  \u00b7  SAUDI ARABIA",
           font=font(SANS_BOLD, 20), fill=RED)
    d.text((520, col_y + 28), "Houthis hit Riyadh's",
           font=font(SERIF, 30), fill=INK)
    d.text((520, col_y + 64), "tallest tower",
           font=font(SERIF, 30), fill=INK)
    houthi = (
        "At least 11 people were wounded on Tuesday in the second "
        "strike on the capital's tallest tower in under a week, Saudi "
        "Civil Defense said.")
    para(d, 520, col_y + 118, houthi, font(SANS, 22), 468, 31)

    d.line([(36, 706), (988, 706)], fill=(190, 180, 160), width=2)

    # ---- Ukraine strip ---------------------------------------------------
    d.rectangle([36, 724, 988, 838], fill=STRIP_BG)
    d.rectangle([36, 724, 50, 838], fill=RED)
    d.text((70, 738), "UKRAINE  \u00b7  TUESDAY",
           font=font(SANS_BOLD, 20), fill=RED)
    d.text((70, 766), "Zelenskiy confirms Ukraine hit Russian ship",
           font=font(SERIF, 30), fill=INK)
    strip_body = (
        "Kyiv owns Saturday's drone strike on a Russian cargo ship in "
        "the Gulf of Finland.")
    para(d, 70, 806, strip_body, font(SANS, 19), 900, 26)

    # ---- ticker ----------------------------------------------------------
    d.rectangle([0, 856, W, 972], fill=NAVY)
    ticker = (
        "Giuliani gets Medal of Freedom \u00b7 Sarkozy case to trial "
        "\u00b7 CIA and ODNI hit by cyber breach \u00b7 Nepal quake 5.6 "
        "\u00b7 Chess title match: Game 1 drawn \u00b7 AIDS deaths "
        "570,000 in 2025, lowest in 20+ years \u00b7 Nasdaq -1.5%, "
        "Nvidia -6% \u00b7 Cartagena: 25 hostages held")
    para(d, 28, 864, ticker, font(SANS_BOLD, 19), 968, 27,
         color=(255, 255, 255))

    # ---- footer ----------------------------------------------------------
    d.text((36, 986),
           "Stories verified against Reuters, Xinhua, BBC, ChessBase and "
           "UNAIDS  \u00b7  Wednesday, 25 November 2026",
           font=font(SANS, 17), fill=GREY)
    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    build().save(out, "PNG")
    print("wrote", out)
