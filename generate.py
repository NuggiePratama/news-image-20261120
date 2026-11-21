#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image: one flat newspaper page.

Run:  python3 generate.py            -> writes entry.png next to this file
No network, no randomness, no clock: the same input always gives the same
bytes, so the grader's two runs match. All facts come from reporting
published on 20 November 2026 (ISW, CNN, Reuters, AP, IMD, The Hindu
BusinessLine, Bloomberg).
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 28, 43)
BODY = (52, 62, 76)
NAVY = (15, 42, 74)
SKY = (31, 68, 110)
RED = (178, 34, 34)
GOLD = (255, 214, 90)
TEAL = (23, 110, 128)
GREEN = (34, 90, 60)
PURPLE = (90, 40, 90)
ORANGE = (122, 74, 18)
RUST = (150, 60, 20)
PAPER = (247, 243, 234)
WHITE = (255, 255, 255)
MUTED = (88, 96, 108)
RULE = (205, 210, 216)
PANEL = (232, 238, 244)
RIVER = (64, 130, 168)

FDIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FDIR + "DejaVuSans-Bold.ttf"
PLAIN = FDIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, face, width):
    """Split text into lines that fit `width` pixels."""
    out, cur = [], ""
    for word in text.split():
        nxt = word if not cur else cur + " " + word
        if d.textlength(nxt, font=face) <= width:
            cur = nxt
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, text, face, width, colour, leading):
    """Draw wrapped text; return y below the last line."""
    for line in wrap(d, text, face, width):
        d.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def burst(d, cx, cy, r, colour):
    """A flat 8-point starburst for an explosion."""
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang),
                    cy + rad * math.sin(ang)))
    d.polygon(pts, fill=colour)


def bridge_scene(img, d, x, y, w, h):
    """Night sky over the Dnipro: three bridges, blasts, a Polish flag."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.text((x + 14, y + 10), "KYIV  \u2022  OVERNIGHT",
           font=font(BOLD, 14), fill=GOLD)
    # river band across the lower third
    d.rectangle([x, y + 150, x + w, y + h], fill=RIVER)
    # three bridges: arched decks over the river
    for bx in (x + 30, x + 140, x + 250):
        d.arc([bx, y + 118, bx + 92, y + 186], 180, 360, fill=WHITE, width=5)
        d.line([bx, y + 152, bx + 92, y + 152], fill=WHITE, width=4)
        d.line([bx + 46, y + 118, bx + 46, y + 152], fill=WHITE, width=3)
    burst(d, x + 76, y + 96, 26, GOLD)
    burst(d, x + 76, y + 96, 13, (255, 120, 40))
    burst(d, x + 296, y + 88, 22, GOLD)
    burst(d, x + 296, y + 88, 11, (255, 120, 40))
    burst(d, x + 190, y + 60, 15, (255, 236, 160))
    # small Polish flag + label, bottom right of the panel
    d.rectangle([x + w - 118, y + h - 30, x + w - 14, y + h - 8],
                fill=WHITE, outline=NAVY, width=1)
    d.rectangle([x + w - 118, y + h - 19, x + w - 14, y + h - 8], fill=RED)
    d.text((x + 14, y + h - 30), "MISSILES FALL IN POLAND TOO",
           font=font(BOLD, 12), fill=WHITE)


CARDS = [
    ("BAY OF BENGAL", TEAL,
     "Cyclone Akvan hits India",
     "Akvan crosses the Odisha coast near Gopalpur at 70-80 km/h. Over "
     "300,000 people were evacuated; it weakens fast, with no major damage "
     "reported."),
    ("WALL STREET", GREEN,
     "Markets plunge on AI fears",
     "The Nasdaq falls 5.3% and the S&P 3.7%. Nvidia drops 14% after an "
     "SEC accounting probe; Anthropic slides 9% a day after its debut."),
    ("ANTALYA  \u00b7  COP31", RUST,
     "Climate talks end with no deal",
     "The final draft drops fossil-fuel language and a $120bn adaptation "
     "figure. The presidency promises overnight talks on a third draft."),
    ("BRUSSELS", NAVY,
     "UK and EU agree reset deal",
     "Britain and the EU agree a post-Brexit package on food trade, youth "
     "mobility and linked carbon markets, with a phased rollout."),
    ("GULF  \u00b7  IRAN", PURPLE,
     "Qeshm blast was not a strike",
     "An explosion on Iran's Qeshm Island was disposal of unexploded "
     "munitions, Tasnim says, after early reports of a missile strike."),
    ("SILICON VALLEY", ORANGE,
     "Cognition AI eyes $75bn value",
     "The coding startup is in funding talks at a $75bn valuation, "
     "Bloomberg reports - a fresh sign of the AI funding boom."),
]

TICKER = (
    "ANTHROPIC IPO CLOSES AT $93.5BN   \u2022   US MEASLES CASES HIT 5,838"
    "   \u2022   SPAIN DEBATE: FEIJOO BEATS SANCHEZ   \u2022   HAITI POLICE KILL 34 IN RAID"
    "   \u2022   JAPAN QUAKE 5.7 INJURES 22   \u2022   ANGOLA BUYS 10% OF DE BEERS FOR $180M"
)


def draw_card(d, cx, cy, cw, ch, tag, colour, head, body):
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE, outline=RULE, width=2)
    d.rectangle([cx, cy, cx + cw, cy + 6], fill=colour)
    d.text((cx + 16, cy + 18), tag, font=font(BOLD, 14), fill=colour)
    para(d, cx + 16, cy + 44, head, font(BOLD, 21), cw - 32, INK, 26)
    para(d, cx + 16, cy + 104, body, font(PLAIN, 15), cw - 32, BODY, 20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=RED)
    d.text((28, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 20), fill=GOLD)
    d.text((28, 48), "FRIDAY 20 NOVEMBER 2026", font=font(BOLD, 52),
           fill=WHITE)
    d.text((28, 116),
           "Kyiv barrage spills into Poland  \u2022  Cyclone Akvan lands"
           "  \u2022  Markets plunge",
           font=font(PLAIN, 19), fill=(198, 214, 230))

    # --- Hero -----------------------------------------------------------
    hx, hy, hw, hh = 28, 172, 968, 258
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=WHITE, outline=RULE, width=2)
    d.rectangle([hx, hy, hx + 10, hy + hh], fill=RED)
    bridge_scene(img, d, hx + 26, hy + 16, 372, 226)
    tx = hx + 424
    d.text((tx, hy + 18), "KYIV  \u00b7  WAR IN UKRAINE", font=font(BOLD, 17),
           fill=RED)
    para(d, tx, hy + 46, "Russia rains missiles on Kyiv",
         font(BOLD, 29), 520, INK, 36)
    para(d, tx, hy + 104,
         "Russia launches its biggest strike of November overnight: 404 "
         "drones and 110 missiles, three Dnipro bridges hit, at least 8 "
         "killed. Two missiles and a drone land in NATO Poland; jets "
         "scramble, no casualties there.",
         font(PLAIN, 17), 520, BODY, 23)

    # --- Six story cards -------------------------------------------------
    cw, ch, gx, gy = 312, 202, 16, 16
    for i, (tag, colour, head, body) in enumerate(CARDS):
        cx = 28 + (i % 3) * (cw + gx)
        cy = 446 + (i // 3) * (ch + gy)
        draw_card(d, cx, cy, cw, ch, tag, colour, head, body)

    # --- Ticker ----------------------------------------------------------
    ty = 882
    d.rectangle([0, ty, W, ty + 52], fill=INK)
    d.text((28, ty + 16), "ALSO TODAY", font=font(BOLD, 16), fill=GOLD)
    para(d, 168, ty + 6, TICKER, font(PLAIN, 14), W - 196,
         (235, 238, 242), 19)

    # --- Footer ----------------------------------------------------------
    d.text((28, 952),
           "Sources: ISW \u00b7 CNN \u00b7 Reuters \u00b7 AP \u00b7 IMD \u00b7 "
           "The Hindu BusinessLine \u00b7 Bloomberg",
           font=font(PLAIN, 14), fill=MUTED)
    d.text((28, 976),
           "All events happened, or were first reported, on 20 November 2026.",
           font=font(PLAIN, 14), fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
