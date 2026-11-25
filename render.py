#!/usr/bin/env python3
"""Draw the 25 November 2026 front page (1024x1024 PNG).

Fresh build for make.fun news-image-20261125. Every fact on the page was
checked against a real source on Wednesday morning, 25 November 2026; see
BUILD_NOTES.md for the sources. Draws a newspaper front page with PIL
only — no network, no photographs, no copied artwork.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
NEWS = (250, 246, 238)      # newsprint
INK = (22, 22, 22)
SCARLET = (172, 30, 32)
NAVY = (18, 33, 61)
STEEL = (84, 96, 116)
MIST = (226, 231, 238)
RULE = (196, 188, 172)
WHITE = (255, 255, 255)
GOLD = (198, 142, 32)

FONT_DIR = "/usr/share/fonts/truetype/noto/"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_XB = lambda s: load("NotoSerif-Black.ttf", s)
SERIF_B = lambda s: load("NotoSerif-Bold.ttf", s)
SANS_XB = lambda s: load("NotoSans-Black.ttf", s)
SANS_B = lambda s: load("NotoSans-Bold.ttf", s)
SANS = lambda s: load("NotoSans-Regular.ttf", s)


def split_lines(draw, text, fnt, width):
    """Greedy wrap: pack as many words per line as fit."""
    out = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def para(draw, xy, text, fnt, width, leading, color=INK):
    """Draw a wrapped paragraph; return the y just below it."""
    x, y = xy
    for line in split_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline_block(draw, x, y, width, kicker, head, head_size, body,
                   body_size, kicker_color=SCARLET):
    """A kicker, a wrapped headline and a wrapped body paragraph."""
    draw.text((x, y), kicker, font=SANS_XB(20), fill=kicker_color)
    y += 30
    y = para(draw, (x, y), head, SERIF_XB(head_size), width,
             head_size + 8)
    y += 6
    y = para(draw, (x, y), body, SANS(body_size), width, body_size + 8)
    return y


def rocket(draw, cx, cy):
    """A simple ascending rocket over a star field, in a navy panel."""
    draw.rectangle((cx - 118, cy - 118, cx + 118, cy + 118), fill=NAVY)
    for sx, sy in ((-88, -84), (-52, -96), (66, -88), (92, -52),
                   (-96, 22), (88, 34), (-64, 78), (52, 92)):
        draw.ellipse((cx + sx - 3, cy + sy - 3, cx + sx + 3, cy + sy + 3),
                     fill=WHITE)
    # body
    draw.polygon([(cx, cy - 92), (cx + 26, cy - 44), (cx + 26, cy + 34),
                  (cx - 26, cy + 34), (cx - 26, cy - 44)], fill=WHITE)
    draw.polygon([(cx, cy - 92), (cx + 26, cy - 44), (cx - 26, cy - 44)],
                 fill=SCARLET)
    draw.ellipse((cx - 11, cy - 52, cx + 11, cy - 30), fill=NAVY)
    # fins
    draw.polygon([(cx - 26, cy + 10), (cx - 52, cy + 52), (cx - 26, cy + 40)],
                 fill=SCARLET)
    draw.polygon([(cx + 26, cy + 10), (cx + 52, cy + 52), (cx + 26, cy + 40)],
                 fill=SCARLET)
    # flame
    draw.polygon([(cx - 16, cy + 36), (cx + 16, cy + 36), (cx, cy + 92)],
                 fill=GOLD)
    draw.polygon([(cx - 8, cy + 36), (cx + 8, cy + 36), (cx, cy + 66)],
                 fill=SCARLET)


def paint():
    img = Image.new("RGB", CANVAS, NEWS)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle((0, 0, 1024, 116), fill=NAVY)
    d.text((36, 26), "THE WORLD TODAY", font=SERIF_XB(58), fill=WHITE)
    d.text((700, 30), "WEDNESDAY", font=SANS_XB(30), fill=WHITE)
    d.text((700, 68), "25 NOVEMBER 2026", font=SANS_B(24),
           fill=(196, 205, 224))
    d.rectangle((0, 116, 1024, 124), fill=SCARLET)

    # --- lead story ----------------------------------------------------
    y = 148
    d.text((36, y), "LEAD  ·  SPACE", font=SANS_XB(20), fill=SCARLET)
    y += 32
    y = para(d, (36, y), "Pakistan's first astronaut reaches orbit",
             SERIF_XB(42), 640, 50)
    y += 10
    lead_body = ("China's Shenzhou-24 lifted off at 08:18 on Wednesday "
                 "carrying Tang Hongbo, Wu Yi and Pakistani payload "
                 "specialist Muhammad Zeeshan Ali — the first Pakistani "
                 "in orbit and the first foreign astronaut aboard the "
                 "Tiangong station.")
    y = para(d, (36, y), lead_body, SANS(23), 640, 31)
    rocket(d, 852, 268)
    d.text((742, 398), "Shenzhou-24 to Tiangong",
           font=SANS_B(17), fill=STEEL)

    # --- divider -------------------------------------------------------
    d.line((36, 448, 988, 448), fill=RULE, width=2)

    # --- two columns ---------------------------------------------------
    headline_block(
        d, 36, 470, 452,
        "BUSINESS  ·  UNITED STATES",
        "Huawei convicted in US trial — 10 of 12 counts",
        30,
        "A Brooklyn jury found the Chinese telecom giant guilty of "
        "bank fraud and trade-secret theft on Tuesday, but cleared it "
        "of racketeering. Sentencing is set for September 2027.",
        21)
    headline_block(
        d, 536, 470, 452,
        "MIDDLE EAST  ·  SAUDI ARABIA",
        "Houthis hit Riyadh's tallest tower",
        30,
        "At least 11 people were wounded on Tuesday in the second "
        "strike on the capital's tallest tower in under a week, Saudi "
        "Civil Defense said.",
        21)

    # --- divider -------------------------------------------------------
    d.line((36, 724, 988, 724), fill=RULE, width=2)

    # --- Zelenskiy strip ----------------------------------------------
    d.rectangle((36, 742, 988, 856), fill=MIST)
    d.rectangle((36, 742, 46, 856), fill=SCARLET)
    d.text((66, 758), "UKRAINE  ·  TUESDAY", font=SANS_XB(19), fill=SCARLET)
    para(d, (66, 784), "Zelenskiy confirms Ukraine hit Russian ship",
         SERIF_XB(29), 890, 36)
    d.text((66, 824),
           "Kyiv owns Saturday's drone strike on a Russian cargo ship in "
           "the Gulf of Finland; Norway urges caution.",
           font=SANS(19), fill=INK)

    # --- ticker --------------------------------------------------------
    d.rectangle((0, 884, 1024, 972), fill=NAVY)
    ticker = ("Giuliani gets Medal of Freedom  •  Sarkozy case to trial  •  "
              "CIA and ODNI hit by cyber breach  •  Nepal quake 5.6  •  "
              "Chess title match: Game 1 drawn 0.5-0.5  •  "
              "AIDS deaths 570,000 in 2025, lowest in 20+ years  •  "
              "Nasdaq -1.5%, Nvidia -6%  •  Cartagena: 25 hostages held")
    para(d, (28, 896), ticker, SANS_B(19), 968, 27, color=WHITE)

    # --- footer --------------------------------------------------------
    d.text((36, 986),
           "Stories verified against Reuters, Xinhua, BBC, ChessBase and "
           "UNAIDS  ·  Wednesday, 25 November 2026",
           font=SANS(15), fill=STEEL)
    return img


if __name__ == "__main__":
    paint().save("entry.png", optimize=True)
    print("wrote entry.png")
