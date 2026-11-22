"""Draw the front page for Sunday 22 November 2026 as a 1024x1024 PNG.

One module, one job: take the day's stories (hard-coded here, researched
from Sunday's news wires) and paint a newspaper front page with PIL.
No network, no clock, no randomness: the same input always paints the
same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 30

PAPER = (247, 243, 234)
INK = (24, 24, 24)
FAINT = (90, 86, 76)
RED = (178, 34, 28)
BLUE = (28, 68, 128)
GREEN = (34, 110, 58)
GREEN_BG = (226, 240, 228)
RULE = (24, 24, 24)
CELL_BG = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "...", font=fnt) > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1] + "..."
    return lines


def draw_center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def hline(draw, y, x0, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A small globe: blue disc, green land blobs, pale latitude lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 208, 232),
                 outline=BLUE, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    for frac in (-0.55, 0.0, 0.55):
        y = cy + frac * r
        half = (r * r - (frac * r) ** 2) ** 0.5
        draw.arc([cx - half, y - 6, cx + half, y + 6], 180, 360,
                 fill=(120, 160, 200), width=2)
        draw.arc([cx - half, y - 6, cx + half, y + 6], 0, 180,
                 fill=(120, 160, 200), width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    draw.polygon([(cx - 52, cy - 30), (cx - 18, cy - 44), (cx + 6, cy - 18),
                  (cx - 8, cy + 2), (cx - 40, cy - 2)], fill=(96, 160, 96))
    draw.polygon([(cx + 12, cy + 22), (cx + 44, cy + 8), (cx + 58, cy + 34),
                  (cx + 30, cy + 52), (cx + 8, cy + 40)], fill=(96, 160, 96))
    draw.polygon([(cx - 58, cy + 34), (cx - 30, cy + 26), (cx - 22, cy + 52),
                  (cx - 48, cy + 58)], fill=(96, 160, 96))


def draw_stamp(draw, cx, cy, text, fnt):
    """A red rubber-stamp label, slightly tilted, over the lead picture."""
    stamp = Image.new("RGBA", (260, 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, 255, 59], outline=RED, width=4)
    sd.text((130 - sd.textlength(text, font=fnt) / 2, 14), text,
            font=fnt, fill=RED)
    stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
    draw._image.paste(stamp, (cx - stamp.width // 2, cy - stamp.height // 2),
                      stamp)


def icon_flame(draw, x, y, s, color=RED):
    pts = [(x + s * 0.5, y + s * 0.02), (x + s * 0.78, y + s * 0.34),
           (x + s * 0.92, y + s * 0.62), (x + s * 0.72, y + s * 0.98),
           (x + s * 0.28, y + s * 0.98), (x + s * 0.08, y + s * 0.62),
           (x + s * 0.24, y + s * 0.34)]
    draw.polygon(pts, fill=color)
    draw.ellipse([x + s * 0.34, y + s * 0.58, x + s * 0.66, y + s * 0.92],
                 fill=(245, 180, 60))


def icon_building(draw, x, y, s, color=BLUE):
    draw.rectangle([x + s * 0.14, y + s * 0.18, x + s * 0.86, y + s * 0.98],
                   fill=color)
    draw.rectangle([x + s * 0.34, y + s * 0.02, x + s * 0.66, y + s * 0.2],
                   fill=color)
    for row in range(3):
        for col in range(3):
            wx = x + s * (0.24 + col * 0.24)
            wy = y + s * (0.30 + row * 0.22)
            draw.rectangle([wx, wy, wx + s * 0.12, wy + s * 0.12],
                           fill=(255, 240, 170))


def icon_shield(draw, x, y, s, color=BLUE):
    draw.polygon([(x + s * 0.5, y + s * 0.02), (x + s * 0.94, y + s * 0.2),
                  (x + s * 0.94, y + s * 0.58), (x + s * 0.5, y + s * 0.98),
                  (x + s * 0.06, y + s * 0.58), (x + s * 0.06, y + s * 0.2)],
                 fill=color)
    draw.text((x + s * 0.5 - 11, y + s * 0.3), "?", font=font(SANS_BOLD, 34),
              fill=(255, 255, 255))


def icon_car(draw, x, y, s, color=INK):
    draw.polygon([(x + s * 0.22, y + s * 0.42), (x + s * 0.34, y + s * 0.2),
                  (x + s * 0.66, y + s * 0.2), (x + s * 0.78, y + s * 0.42)],
                 fill=color)
    draw.rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.72],
                   fill=color)
    draw.ellipse([x + s * 0.16, y + s * 0.66, x + s * 0.36, y + s * 0.86],
                 fill=INK)
    draw.ellipse([x + s * 0.64, y + s * 0.66, x + s * 0.84, y + s * 0.86],
                 fill=INK)
    draw.polygon([(x + s * 0.06, y + s * 0.72), (x + s * 0.16, y + s * 0.5),
                  (x + s * 0.06, y + s * 0.5)], fill=RED)


def icon_boat(draw, x, y, s, color=BLUE):
    draw.polygon([(x + s * 0.08, y + s * 0.58), (x + s * 0.92, y + s * 0.58),
                  (x + s * 0.78, y + s * 0.82), (x + s * 0.22, y + s * 0.82)],
                 fill=color)
    draw.line([(x + s * 0.5, y + s * 0.1), (x + s * 0.5, y + s * 0.58)],
              fill=INK, width=5)
    draw.polygon([(x + s * 0.54, y + s * 0.14), (x + s * 0.54, y + s * 0.52),
                  (x + s * 0.86, y + s * 0.52)], fill=RED)
    draw.arc([x + s * 0.06, y + s * 0.84, x + s * 0.5, y + s * 1.02],
             180, 360, fill=color, width=5)
    draw.arc([x + s * 0.5, y + s * 0.84, x + s * 0.94, y + s * 1.02],
             180, 360, fill=color, width=5)


def icon_screen(draw, x, y, s, color=INK):
    draw.rectangle([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.78],
                   fill=color)
    draw.rectangle([x + s * 0.16, y + s * 0.16, x + s * 0.84, y + s * 0.7],
                   fill=(200, 225, 245))
    draw.line([(x + s * 0.24, y + s * 0.3), (x + s * 0.5, y + s * 0.56),
               (x + s * 0.76, y + s * 0.3)], fill=RED, width=6)
    draw.rectangle([x + s * 0.4, y + s * 0.78, x + s * 0.6, y + s * 0.9],
                   fill=color)
    draw.rectangle([x + s * 0.26, y + s * 0.9, x + s * 0.74, y + s * 0.96],
                   fill=color)


ICONS = {
    "flame": icon_flame,
    "building": icon_building,
    "shield": icon_shield,
    "car": icon_car,
    "waves": icon_boat,
    "screen": icon_screen,
}

LEAD = {
    "kicker": "CLIMATE  •  ANTALYA, TURKEY",
    "headline": "COP31 ENDS WITH NO DEAL",
    "deck": "Climate talks collapse over fossil fuels",
    "body": ("The UN climate summit closed on Sunday with no deal after "
             "the EU rejected a draft that ignored fossil fuels."),
}

STORIES = [
    {
        "icon": "shield", "kicker": "GULF  •  BAHRAIN",
        "headline": "Bahrain counts two hurt in Iranian strike",
        "body": ("Bahrain said two were wounded in Saturday's attack "
                 "and demanded UN action."),
    },
    {
        "icon": "building", "kicker": "UKRAINE  •  KYIV REGION",
        "headline": "Drone hits flats near Kyiv; 14 missing",
        "body": ("A Russian drone hit a five-storey block in Dymer; "
                 "rescuers search the rubble."),
    },
    {
        "icon": "flame", "kicker": "INDONESIA  •  CIKANDE",
        "headline": "Factory fire kills 3; dozens missing",
        "body": ("A blaze at a candy factory left three dead and dozens "
                 "unaccounted for."),
    },
    {
        "icon": "screen", "kicker": "UNITED STATES  •  WASHINGTON",
        "headline": "FBI probes hack of crime database",
        "body": ("The FBI is investigating an apparent breach of its "
                 "crime records database."),
    },
    {
        "icon": "car", "kicker": "WEST BANK  •  RAMALLAH",
        "headline": "Settlers torch cars; Israel opens inquiry",
        "body": ("Settlers torched 12 vehicles in four villages near "
                 "Ramallah; Israel opened an inquiry."),
    },
    {
        "icon": "waves", "kicker": "NIGERIA",
        "headline": "Boat capsizes; at least 24 dead",
        "body": ("A boat carrying people to a funeral capsized; at least "
                 "24 people died."),
    },
]

BRIGHT = ("BRIGHT SPOT — Verstappen wins the Las Vegas Grand Prix.")

TICKER = ("MARKETS: S&P 500 in correction after Friday's 3.7% slide  •  "
          "SEOUL: Minister quits over exam-cheating scandal")

FOOTER = ("All stories reported Sunday 22 November 2026  •  "
          "Sources: AP, Reuters, BBC, AFP")


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- Masthead ----
    name_f = font(SERIF_BOLD, 66)
    draw_center(draw, W // 2, 22, "THE WORLD TODAY", name_f)
    hline(draw, 102, MARGIN, W - MARGIN, 2)
    date_f = font(SANS_BOLD, 30)
    draw_center(draw, W // 2, 112, "SUNDAY, 22 NOVEMBER 2026", date_f,
                fill=RED)
    sub_f = font(SANS, 19)
    draw_center(draw, W // 2, 150,
                "One day's world news, in one page", sub_f, fill=FAINT)
    hline(draw, 182, MARGIN, W - MARGIN, 4)

    # ---- Lead story ----
    lead_y = 198
    kick_f = font(SANS_BOLD, 20)
    draw.text((MARGIN, lead_y), LEAD["kicker"], font=kick_f, fill=RED)
    head_f = font(SERIF_BOLD, 50)
    lines = fit_lines(draw, LEAD["headline"], head_f, 660, 2)
    y = lead_y + 30
    for line in lines:
        draw.text((MARGIN, y), line, font=head_f, fill=INK)
        y += 58
    deck_f = font(SERIF, 26)
    draw.text((MARGIN, y + 4), LEAD["deck"], font=deck_f, fill=INK)
    body_f = font(SANS, 20)
    blines = fit_lines(draw, LEAD["body"], body_f, 660, 2)
    y = y + 46
    for line in blines:
        draw.text((MARGIN, y), line, font=body_f, fill=INK)
        y += 26

    # Lead picture: globe + NO DEAL stamp, right of the lead text.
    gx, gy = 830, 280
    draw_globe(draw, gx, gy, 78)
    stamp_f = font(SANS_BOLD, 30)
    draw_stamp(draw, gx, gy + 88, "NO DEAL", stamp_f)

    hline(draw, 444, MARGIN, W - MARGIN, 3)

    # ---- Secondary stories: 2 columns x 3 rows ----
    grid_y = 458
    cell_w = (W - 2 * MARGIN - 24) // 2
    cell_h = 132
    row_gap = 10
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x0 = MARGIN + col * (cell_w + 24)
        y0 = grid_y + row * (cell_h + row_gap)
        draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=CELL_BG,
                       outline=(200, 194, 180), width=1)
        ix, iy = x0 + 14, y0 + 16
        ICONS[story["icon"]](draw, ix, iy, 64)
        tx = x0 + 94
        tw = cell_w - 94 - 14
        draw.text((tx, y0 + 12), story["kicker"], font=font(SANS_BOLD, 15),
                  fill=RED)
        hlines = fit_lines(draw, story["headline"],
                           font(SERIF_BOLD, 21), tw, 2)
        hy = y0 + 34
        for line in hlines:
            draw.text((tx, hy), line, font=font(SERIF_BOLD, 21), fill=INK)
            hy += 26
        blines = fit_lines(draw, story["body"], font(SANS, 16), tw, 2)
        by = hy + 2
        for line in blines:
            draw.text((tx, by), line, font=font(SANS, 16), fill=INK)
            by += 21

    # ---- Bright spot ----
    bright_y = grid_y + 3 * cell_h + 2 * row_gap + 10
    draw.rectangle([MARGIN, bright_y, W - MARGIN, bright_y + 52],
                   fill=GREEN_BG, outline=GREEN, width=2)
    bf = font(SANS_BOLD, 20)
    blines = fit_lines(draw, BRIGHT, bf, W - 2 * MARGIN - 28, 2)
    by = bright_y + 5 if len(blines) > 1 else bright_y + 14
    for line in blines:
        draw.text((MARGIN + 14, by), line, font=bf, fill=GREEN)
        by += 23

    # ---- Ticker ----
    tick_y = bright_y + 62
    tf = font(SANS, 17)
    draw.text((MARGIN, tick_y), TICKER, font=tf, fill=FAINT)
    hline(draw, tick_y + 26, MARGIN, W - MARGIN, 2)

    # ---- Footer ----
    ff = font(SANS, 15)
    draw_center(draw, W // 2, tick_y + 34, FOOTER, ff, fill=FAINT)

    return img
