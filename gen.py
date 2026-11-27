"""news-26-b34-numbers — V32 ALSO-first layout. Renders 1024x1024 entry.png.
Layout V32: masthead + DATE CHECK (2 lines) -> ALSO 3 cols (37) FIRST ->
3 heroes side-by-side -> cards 2x5 -> map strip -> timeline -> footer.
All strings measured with real PIL font metrics; no truncation anywhere.
"""
import os
import re
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(font, s):
    return font.getlength(s)


def wrap(text, font, max_w):
    """Greedy wrap; returns list of lines, each measured to fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(font, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, max_w, max_lines):
    lines = wrap(text, font, max_w)
    assert len(lines) <= max_lines, "OVERFLOW lines=%d > %d: %r" % (len(lines), max_lines, text)
    for ln in lines:
        assert tw(font, ln) <= max_w, "OVERFLOW width: %r" % ln
    return lines


def assert_fit(text, font, max_w):
    assert tw(font, text) <= max_w, "TOO WIDE (%d > %d): %r" % (tw(font, text), max_w, text)


def draw_lines(dr, lines, x, y, font, fill, lh):
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------- palette ----------------
INK = (18, 18, 20)
PAPER = (250, 247, 238)
NAVY = (16, 34, 64)
RED = (178, 34, 34)
GOLD = (198, 142, 22)
TEAL = (14, 90, 86)
CREAM = (255, 252, 244)
GREY = (90, 90, 96)
LIGHT = (232, 228, 218)
SKY = (168, 205, 232)
SEA = (38, 84, 124)
LAND = (196, 190, 168)
OCEAN = (214, 230, 240)

# ---------------- content ----------------
MASTHEAD_TITLE = "THE WORLD IN ONE PAGE"
MASTHEAD_SUB = "THURSDAY, 26 NOVEMBER 2026  ·  50 STORIES"
DATECHECK = [
    "DATE CHECK — THURSDAY 26 NOVEMBER 2026  ·  EVERY STORY BELOW IS FROM 26 NOV UNLESS MARKED 25 NOV",
    "NOT 26 NOV — EXCLUDED: COP31 (22 NOV)  ·  SHENZHOU-24 (25 NOV)  ·  CAIRO TANKER (25 NOV)  ·  CARTAGENA HOSTAGES (25 NOV)",
]

HEROES = [
    {
        "kicker": "HERO 1  ·  NEW YORK",
        "color": NAVY,
        "art": "macys",
        "head": "MACY'S 100TH PARADE POSTPONED — FIRST TIME EVER FOR WEATHER",
        "deck": "Thanksgiving storm forces the first weather postponement in the parade's 100-year history; balloons inflated Wed, then deflated.",
        "why": "WHY IT MATTERS: America's most-watched holiday ritual bends to the weather for the first time, a symbol of a stormy Thanksgiving.",
        "stat": "100TH  ·  GUSTS 60 MPH  ·  BACK SAT 28 NOV",
        "tag": "[C]",
    },
    {
        "kicker": "HERO 2  ·  STRAIT OF HORMUZ",
        "color": RED,
        "art": "hormuz",
        "head": "IRGC CLAIMS 2 TANKERS HIT BY MINES IN HORMUZ",
        "deck": "Tehran claims two tankers exploded after hitting sea mines off Khasab; one is a supertanker carrying over 2M barrels. Claim unverified.",
        "why": "WHY IT MATTERS: An unverified mine claim in the busiest oil chokepoint still moved crude and widened the Iran war at sea.",
        "stat": "2M-BARREL TANKER  ·  BRENT $93.8",
        "tag": "[CL]",
    },
    {
        "kicker": "HERO 3  ·  GLOBAL MARKETS",
        "color": TEAL,
        "art": "tariffs",
        "head": "MARKETS REBOUND AS TRUMP TARIFF SALVO LANDS SOFTER THAN FEARED",
        "deck": "European and Asian markets rebound as the tariff salvo looks softer than feared — levies won't stack on July duties; Wall Street shut.",
        "why": "WHY IT MATTERS: The rebound shows investors read the tariff salvo as manageable, capping a week of trade-war nerves.",
        "stat": "STOXX +1.6%  ·  14 PARTNERS  ·  CHINA 20%",
        "tag": "[C]",
    },
]

CARDS = [
    ("DEIR AL-BALAH", "ISRAEL KILLS SENIOR HAMAS EDUCATION OFFICIAL",
     "Khaled Abu Nada and his wife die in overnight strike; 9 killed.",
     "9 KILLED  ·  3RD NIGHT OF STRIKES", "gaza", "[C]"),
    ("KYIV", "RUSSIAN MISSILE HITS KYIV MALL; 7 HURT",
     "Ballistic missiles and 113 drones hit the capital overnight.",
     "113 DRONES  ·  7 WOUNDED", "kyiv", "[C]"),
    ("BOGOR", "FLOODED ILLEGAL GOLD MINE: 13 DEAD, 13 MISSING",
     "Miners trapped ~100 m underground after heavy rain in Bogor.",
     "13 DEAD  ·  13 MISSING", "bogor", "[C]"),
    ("JERUSALEM", "JUDGE URGES DROP OF NETANYAHU BRIBERY CHARGE",
     "Court recommends dropping Case 4000, the only bribery count.",
     "CASE 4000  ·  SOLE BRIBERY COUNT", "netanyahu", "[C]"),
    ("PYONGYANG", "KIM TOURS NUCLEAR PLANT, URGES MORE TACTICAL NUKES",
     "Kim visits a nuclear-materials plant, pushes wider tactical use.",
     "TACTICAL NUKES PUSH", "kim", "[C]"),
    ("WASHINGTON", "FCC CLEARS SPACEX PLAN FOR 1M ORBITAL SATELLITES",
     "First US approval for space data centres; AI chips in orbit.",
     "1M SATELLITES  ·  APPROVED NOV 25", "spacex", "[C]"),
    ("LONDON", "UK NET MIGRATION FALLS TO 77,000",
     "Lowest since 1997 outside the pandemic, in year to June 2026.",
     "77,000  ·  LOWEST SINCE 1997", "london", "[C]"),
    ("MOSCOW", "RUSSIA APPROVES RECORD POST-SOVIET MILITARY BUDGET",
     "Moscow signs off its biggest defence budget since the Soviet era.",
     "RECORD DEFENCE BUDGET", "moscow", "[C]"),
    ("BANGKOK", "BLAST AT BANGKOK OIL DEPOT HURTS 7",
     "Explosion triggers evacuation warnings; fire out in ~30 minutes.",
     "7 HURT  ·  FIRE OUT IN 30 MIN", "bangkok", "[C]"),
    ("COLOGNE", "2 IRAQI SUSPECTS HELD OVER SYNAGOGUE ATTACK PLOT",
     "Arrests in Cologne and Heidelberg over a late-March attack plot.",
     "2 HELD  ·  COLOGNE + HEIDELBERG", "cologne", "[C]"),
]

ALSO = [
    "Eisenkot seals first Israel coalition deal [C]",
    "Merz warns Russia's ambitions stretch beyond Ukraine [C]",
    "UK on drone alert at airbases [C]",
    "Norse Atlantic halts flights, warns of bankruptcy [C]",
    "Poundland into administration, 11,000 jobs at risk [C]",
    "Malaysia sues Google $146M over harmful content [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers Zelensky flight to Moscow; he refuses [C]",
    "Kushner calls Putin 'significant figure' [C]",
    "Estonia decides to close border [C]",
    "Copernicus: longest stretch above 2°C warming [C]",
    "Nvidia halts AI server shipments to 4 countries [C]",
    "US Bitcoin funds hit record $4.94B [C]",
    "Houthis claim Ras Tanura + Riyadh strikes — 25 Nov [CL]",
    "Cargo ship claimed hit near Odesa [CL]",
    "Saudi downs 2 ballistic missiles bound for Riyadh [CL]",
    "UKMTO: blast 50 NM west of Dubai, crew safe [CL]",
    "UKMTO: tanker hit 18 NM east of Khasab — 25 Nov [CL]",
    "Nvidia slides 3.91% to $149.30 [C]",
    "Nasdaq fell 0.62% Wed after sliding 4% intraday [C]",
    "Dow rose 0.33% Wed as S&P slipped 0.25% [C]",
    "Gold $3,572/oz, −8% in a month [C]",
    "Dollar flat at 103.71 [C]",
    "WTI crude $83.32, +0.2% [C]",
    "MSCI global index +0.4% [C]",
    "US stock futures +0.5% on the holiday [C]",
    "Ukraine drones hit Savasleyka airbase, 5 jets damaged [C]",
    "Subkhankulovo pump station ablaze 1,300 km away [C]",
    "Kryvyi Rih: 18 wounded in Russian strikes [C]",
    "UN rights chief warns of atrocity risk in Gaza [C]",
    "OPEC+ to meet 29 Nov on 2027 output [C]",
    "Philadelphia's Thanksgiving parade also cancelled [C]",
    "NYC balloon rule: grounded above 23 mph wind [C]",
    "NBC to air 2025 parade Thu, live 2026 parade Sat [C]",
    "NYC Mayor Mamdani to miss rescheduled parade [C]",
    "Iran war enters day 272 [C]",
    "EU faces 15% tariff; Vietnam up to 35% in US plan [C]",
]

TIMELINE = ("OVERNIGHT Kyiv + Gaza strikes  ·  10:00 NYC wind warning  ·  MORNING markets rebound  ·  "
            "MIDDAY Hormuz mine claim  ·  DAY UK migration 77,000  ·  EVENING Bangkok blast")
FOOTER = ("SOURCES: REUTERS  ·  AP  ·  BBC  ·  CNN  ·  NPR  ·  UKMTO  ·  ONS  ·  KCNA     "
          "[C] CONFIRMED  ·  [R] REPORTED  ·  [CL] CLAIM — UNVERIFIED")

# ---------------- validation (runs before any drawing) ----------------
STOP = set("the and for with from after over into amid that this have been were will would their there about under".split())


def distinctive(text):
    words = re.findall(r"[a-z]+", text.lower())
    out = set()
    for wd in words:
        if len(wd) >= 4 and wd not in STOP:
            out.add(wd[:-1] if wd.endswith("s") and len(wd) > 4 else wd)
    return out


def validate():
    assert len(HEROES) == 3 and len(CARDS) == 10 and len(ALSO) == 37
    assert 3 + 10 + 37 == 50, "total stories must be 50"
    all_text = " ".join([MASTHEAD_TITLE, MASTHEAD_SUB] + DATECHECK +
                        [h["head"] + " " + h["deck"] + " " + h["why"] + " " + h["stat"] for h in HEROES] +
                        [c[0] + " " + c[1] + " " + c[2] + " " + c[3] for c in CARDS] +
                        ALSO + [TIMELINE, FOOTER])
    low = all_text.lower()
    assert "bangchak" not in low, "banned word Bangchak present"
    assert "third senior hamas official" not in low, "banned duplicate item present"
    assert low.count("philadelphia") == 1, "Philadelphia must appear exactly once, got %d" % low.count("philadelphia")
    for bad in ("186", "161", "720"):
        assert bad not in all_text, "banned cross-date number %s present" % bad
    # hero stat numbers must not repeat in ALSO (one place only)
    hero_nums = set()
    for h in HEROES:
        for tok in re.findall(r"\$?\d[\d,\.]*(?:%|M|B|mph)?", h["stat"]):
            hero_nums.add(tok.replace(",", "").replace("$", ""))
    also_text = " ".join(ALSO)
    also_nums = set(re.findall(r"\$?\d[\d,\.]*(?:%|M|B|mph)?", also_text))
    also_nums = set(t.replace(",", "").replace("$", "") for t in also_nums)
    for tok in hero_nums:
        if len(tok) >= 2:
            assert tok not in also_nums, "hero stat number %r repeated in ALSO" % tok
    # duplicate scan: >=3 distinctive words shared = flag
    pool = []
    for h in HEROES:
        pool.append(("hero:" + h["head"][:20], h["head"] + " " + h["deck"] + " " + h["why"]))
    for c in CARDS:
        pool.append(("card:" + c[1][:20], c[1] + " " + c[2]))
    flags = []
    for i, item in enumerate(ALSO):
        di = distinctive(item)
        for name, other in pool:
            shared = di & distinctive(other)
            if len(shared) >= 3:
                flags.append((i, item, name, sorted(shared)))
        for j in range(i):
            shared = di & distinctive(ALSO[j])
            if len(shared) >= 3:
                flags.append((i, item, "also#%d" % j, sorted(shared)))
    assert not flags, "DUPLICATE FLAGS: %r" % (flags,)
    # every item carries a literal tag
    for item in ALSO:
        assert item.rstrip().endswith(("[C]", "[R]", "[CL]")), "ALSO item missing tag: %r" % item
    return hero_nums


# ---------------- art (each drawn on its own layer, clamped to its box) ----------------
def layer(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def art_macys(w, h):
    img, d = layer(w, h, SKY)
    d.rectangle([0, h - 26, w, h], fill=(70, 74, 84))
    for bx, bw, bh in ((8, 34, 52), (48, 26, 70), (80, 40, 44), (126, 30, 62),
                       (162, 36, 48), (204, 28, 66), (238, 34, 50), (278, 30, 58)):
        d.rectangle([bx, h - 26 - bh, bx + bw, h - 26], fill=(52, 56, 66))
        for wy in range(h - 26 - bh + 6, h - 30, 12):
            d.rectangle([bx + 5, wy, bx + 12, wy + 6], fill=(250, 220, 120))
    # giant balloon + net
    d.ellipse([w // 2 - 52, 6, w // 2 + 52, 62], fill=(178, 34, 34), outline=(120, 20, 20), width=2)
    d.ellipse([w // 2 - 30, 14, w // 2 + 30, 54], fill=(212, 70, 60))
    for gx in range(w // 2 - 52, w // 2 + 53, 13):
        d.line([gx, 8, gx, 60], fill=(90, 20, 20), width=1)
    d.line([w // 2 - 52, 34, w // 2 + 52, 34], fill=(90, 20, 20), width=1)
    d.polygon([(w // 2 - 14, 62), (w // 2 + 14, 62), (w // 2 + 6, h - 26), (w // 2 - 6, h - 26)],
              fill=(120, 20, 20))
    return img


def art_hormuz(w, h):
    import math
    img, d = layer(w, h, (232, 196, 150))
    d.rectangle([0, h // 2 + 6, w, h], fill=SEA)
    for x in range(0, w, 26):
        d.arc([x, h // 2 + 10, x + 24, h // 2 + 22], 0, 180, fill=(160, 200, 225), width=2)
    # tanker
    d.rectangle([40, h // 2 - 16, w - 40, h // 2 + 10], fill=(40, 40, 44))
    d.rectangle([52, h // 2 - 34, 92, h // 2 - 16], fill=(60, 60, 66))
    d.rectangle([w - 110, h // 2 - 28, w - 70, h // 2 - 16], fill=(60, 60, 66))
    d.line([40, h // 2 + 10, w - 40, h // 2 + 10], fill=(20, 20, 24), width=2)
    # fire + smoke
    for cx, cy, r, col in ((w // 2 - 30, h // 2 - 26, 16, (240, 120, 30)),
                           (w // 2 - 8, h // 2 - 36, 20, (250, 180, 40)),
                           (w // 2 + 16, h // 2 - 26, 14, (240, 120, 30))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for cx, cy, r in ((w // 2 - 8, h // 2 - 56, 12), (w // 2 + 6, h // 2 - 68, 15), (w // 2 - 20, h // 2 - 66, 10)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 80, 84))
    # mine
    mx, my = w - 26, h - 22
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(20, 20, 22))
    for ang in range(0, 360, 45):
        x1 = mx + 9 * math.cos(math.radians(ang))
        y1 = my + 9 * math.sin(math.radians(ang))
        x2 = mx + 14 * math.cos(math.radians(ang))
        y2 = my + 14 * math.sin(math.radians(ang))
        d.line([x1, y1, x2, y2], fill=(20, 20, 22), width=2)
    return img


def art_tariffs(w, h):
    img, d = layer(w, h, (238, 240, 232))
    base = h - 22
    vals = [26, 34, 30, 44, 40, 58, 66]
    bw = (w - 20) // len(vals)
    for i, v in enumerate(vals):
        x0 = 10 + i * bw
        col = (178, 34, 34) if i < 3 else (14, 120, 86)
        d.rectangle([x0 + 3, base - v, x0 + bw - 3, base], fill=col)
    d.line([8, base, w - 8, base], fill=INK, width=2)
    d.line([w - 34, 10, w - 10, 10], fill=(14, 120, 86), width=3)
    d.polygon([(w - 34, 10), (w - 22, 4), (w - 22, 16)], fill=(14, 120, 86))
    # containers
    for cx, cy, col in ((16, 12, (198, 142, 22)), (44, 12, (14, 90, 86)), (30, 26, (178, 34, 34))):
        d.rectangle([cx, cy, cx + 24, cy + 10], fill=col, outline=(255, 255, 255))
    return img


def art_mini(kind, w, h):
    img, d = layer(w, h, (226, 222, 210))
    if kind == "gaza":
        d.rectangle([0, h - 12, w, h], fill=(120, 116, 104))
        d.rectangle([14, 16, 66, h - 12], fill=(90, 88, 80))
        d.rectangle([74, 14, 120, h - 12], fill=(110, 106, 96))
        d.ellipse([96, 2, 136, 30], fill=(150, 150, 150))
        d.ellipse([112, 8, 150, 34], fill=(120, 120, 120))
        d.polygon([(30, 16), (44, 4), (58, 16)], fill=(240, 120, 30))
    elif kind == "kyiv":
        d.rectangle([0, h - 12, w, h], fill=(70, 74, 84))
        d.rectangle([20, 14, 110, h - 12], fill=(52, 56, 66))
        d.rectangle([124, 18, 168, h - 12], fill=(70, 74, 84))
        d.ellipse([58, 2, 96, 28], fill=(250, 180, 40))
        d.ellipse([66, 8, 88, 26], fill=(240, 120, 30))
    elif kind == "bogor":
        d.rectangle([0, 0, w, h // 2], fill=(120, 160, 90))
        d.rectangle([0, h // 2, w, h], fill=(90, 70, 50))
        d.polygon([(w // 2 - 26, h // 2), (w // 2 + 26, h // 2), (w // 2 + 12, h), (w // 2 - 12, h)], fill=(40, 30, 22))
        d.rectangle([0, h // 2 - 4, w, h // 2 + 2], fill=(38, 84, 124))
    elif kind == "netanyahu":
        d.rectangle([0, h - 12, w, h], fill=(150, 146, 134))
        for x in (24, 62, 100, 138):
            d.rectangle([x, 14, x + 10, h - 12], fill=(250, 247, 238))
        d.polygon([(12, 14), (w // 2, 0), (w - 12, 14)], fill=(178, 34, 34))
    elif kind == "kim":
        d.rectangle([0, h - 12, w, h], fill=(70, 74, 84))
        d.rectangle([30, 20, 90, h - 12], fill=(120, 120, 118))
        d.rectangle([100, 16, 150, h - 12], fill=(90, 90, 92))
        d.ellipse([w // 2 - 12, 4, w // 2 + 12, 28], fill=(198, 142, 22))
        d.ellipse([w // 2 - 5, 11, w // 2 + 5, 21], fill=(250, 247, 238))
    elif kind == "spacex":
        d.rectangle([0, 0, w, h], fill=(16, 34, 64))
        for sx, sy in ((30, 12), (90, 26), (140, 10), (60, 34), (120, 40)):
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        d.rectangle([w // 2 - 26, h // 2 - 8, w // 2 + 26, h // 2 + 8], fill=(198, 142, 22))
        d.rectangle([w // 2 - 40, h // 2 - 3, w // 2 - 26, h // 2 + 3], fill=(150, 150, 150))
        d.rectangle([w // 2 + 26, h // 2 - 3, w // 2 + 40, h // 2 + 3], fill=(150, 150, 150))
    elif kind == "london":
        d.rectangle([0, h - 12, w, h], fill=(120, 116, 104))
        d.rectangle([w // 2 - 12, 6, w // 2 + 12, h - 12], fill=(90, 88, 80))
        d.polygon([(w // 2 - 14, 6), (w // 2, -2), (w // 2 + 14, 6)], fill=(90, 88, 80))
        d.ellipse([w // 2 - 7, 10, w // 2 + 7, 24], fill=(250, 247, 238))
        d.rectangle([26, 20, 60, h - 12], fill=(110, 106, 96))
        d.rectangle([120, 22, 154, h - 12], fill=(110, 106, 96))
    elif kind == "moscow":
        d.rectangle([0, h - 12, w, h], fill=(120, 116, 104))
        for x, hh in ((20, 26), (52, 34), (84, 30), (116, 38), (148, 26)):
            hh = int(hh * h / 44)
            d.rectangle([x, h - 12 - hh, x + 18, h - 12], fill=(178, 34, 34))
            d.ellipse([x + 2, h - 12 - hh - 8, x + 16, h - 12 - hh + 6], fill=(198, 142, 22))
    elif kind == "bangkok":
        d.rectangle([0, h - 12, w, h], fill=(70, 74, 84))
        for x in (18, 62, 106):
            d.rectangle([x, 18, x + 34, h - 12], fill=(150, 146, 134))
            d.ellipse([x + 2, 16, x + 32, 28], fill=(150, 146, 134))
        d.polygon([(130, 24), (142, 6), (154, 24)], fill=(240, 120, 30))
        d.ellipse([136, 10, 152, 24], fill=(250, 180, 40))
    elif kind == "cologne":
        d.rectangle([0, h - 12, w, h], fill=(120, 116, 104))
        d.rectangle([30, 20, 80, h - 12], fill=(90, 88, 80))
        d.polygon([(30, 20), (55, 2), (80, 20)], fill=(70, 68, 60))
        d.rectangle([100, 14, 150, h - 12], fill=(110, 106, 96))
        d.polygon([(100, 14), (125, 0), (150, 14)], fill=(90, 88, 80))
    return img

# ---------------- world map (rough equirectangular polygons, lon/lat) ----------------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 66), (-75, 62),
     (-60, 55), (-55, 47), (-65, 44), (-75, 35), (-80, 25), (-90, 21), (-97, 16),
     (-105, 20), (-117, 32), (-125, 40), (-125, 49), (-140, 60), (-158, 58), (-168, 66)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -38),
     (-65, -45), (-70, -55), (-73, -40), (-73, -20), (-80, -5), (-80, 10)],
    [(-10, 36), (-2, 37), (3, 43), (7, 44), (12, 45), (19, 45), (23, 40), (28, 41),
     (30, 36), (23, 36), (19, 40), (12, 44), (0, 46), (-2, 48), (-5, 50), (-10, 54),
     (-10, 58), (-5, 60), (5, 58), (8, 57), (18, 56), (21, 55), (24, 59), (30, 60),
     (30, 70), (20, 70), (12, 70), (5, 60), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -20), (32, -28), (26, -34), (20, -35),
     (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-17, 15)],
    [(30, 36), (35, 36), (43, 41), (48, 40), (50, 46), (55, 51), (60, 55), (68, 70),
     (75, 73), (90, 75), (110, 76), (130, 72), (160, 70), (178, 66), (170, 60),
     (162, 56), (158, 52), (142, 50), (140, 40), (135, 35), (127, 35), (122, 30),
     (120, 22), (110, 20), (105, 8), (100, 8), (98, 15), (92, 21), (88, 22),
     (80, 15), (75, 8), (70, 20), (60, 25), (55, 26), (50, 29), (48, 30), (43, 12), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38),
     (147, -39), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (113, -22)],
]
# (lon, lat, label, dx, dy) — dx/dy nudge the label so close pins don't collide
PINS = [
    (-74.0, 40.7, "NYC", -34, -14),
    (-77.0, 38.9, "WASHINGTON", -72, 10),
    (56.2, 26.2, "HORMUZ", 10, -14),
    (46.7, 24.6, "RIYADH", 14, 14),
    (35.2, 31.8, "JERUSALEM", -70, 16),
    (34.5, 31.5, "GAZA", 10, 16),
    (30.5, 50.4, "KYIV", -14, -14),
    (7.0, 50.9, "COLOGNE", -8, -14),
    (-0.1, 51.5, "LONDON", -52, -12),
    (37.6, 55.8, "MOSCOW", -62, 8),
    (125.8, 39.0, "PYONGYANG", -40, -14),
    (100.5, 13.8, "BANGKOK", -30, -14),
    (106.8, -6.6, "BOGOR", -20, 10),
]
MAP_LEGEND = ("WORLD MAP — PINS MARK THE STORIES ON THIS PAGE  ·  NYC  ·  HORMUZ  ·  KYIV  ·  GAZA  ·  "
              "BOGOR  ·  BANGKOK  ·  COLOGNE  ·  LONDON  ·  MOSCOW  ·  PYONGYANG  ·  WASHINGTON  ·  JERUSALEM  ·  RIYADH")


def render():
    hero_nums = validate()
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    MX = 16
    CW = 992
    # ---- masthead 0-60 ----
    f_title = F(SERIF, 34)
    f_sub = F(SANS_B, 12)
    assert_fit(MASTHEAD_TITLE, f_title, 700)
    dr.text((MX, 6), MASTHEAD_TITLE, font=f_title, fill=NAVY)
    dr.text((MX, 44), MASTHEAD_SUB, font=f_sub, fill=RED)
    f_badge = F(SANS_B, 15)
    badge = "50 STORIES"
    bw = tw(f_badge, badge) + 20
    dr.rectangle([W - MX - bw, 8, W - MX, 34], fill=RED)
    dr.text((W - MX - bw + 10, 12), badge, font=f_badge, fill=(255, 255, 255))
    f_small = F(SANS, 10)
    small = "news-image-20261126  ·  $100 TOP-50"
    assert_fit(small, f_small, 300)
    dr.text((W - MX - tw(f_small, small), 40), small, font=f_small, fill=GREY)
    dr.line([MX, 59, W - MX, 59], fill=NAVY, width=2)
    # ---- DATE CHECK 60-106 ----
    dr.rectangle([MX, 60, W - MX, 106], fill=LIGHT)
    dr.rectangle([MX, 60, MX + 5, 106], fill=RED)
    f_dc1 = F(SANS_B, 12)
    f_dc2 = F(SANS, 11)
    for ln in DATECHECK:
        assert_fit(ln, f_dc1, CW - 24)
    dr.text((MX + 16, 66), DATECHECK[0], font=f_dc1, fill=INK)
    dr.text((MX + 16, 85), DATECHECK[1], font=f_dc2, fill=(60, 60, 64))
    # ---- ALSO header 106-130 ----
    f_ah = F(SANS_B, 15)
    f_ar = F(SANS_B, 10)
    ah = "ALSO TODAY — 37 MORE STORIES"
    assert_fit(ah, f_ah, 500)
    dr.text((MX, 110), ah, font=f_ah, fill=NAVY)
    ar = "LAYOUT V32 — ALSO FIRST  ·  EVERY ITEM TAGGED [C] CONFIRMED / [CL] CLAIM"
    assert_fit(ar, f_ar, 560)
    dr.text((W - MX - tw(f_ar, ar), 113), ar, font=f_ar, fill=GREY)
    # ---- ALSO 3 columns, 130-325 (13 rows x 15px) ----
    f_also = F(SANS, 11)
    f_tag = F(SANS_B, 11)
    col_w = 322
    col_x = [MX, MX + col_w + 12, MX + 2 * (col_w + 12)]
    counts = [13, 12, 12]
    idx = 0
    for ci in range(3):
        for ri in range(counts[ci]):
            item = ALSO[idx]
            idx += 1
            body, _, tag = item.rpartition(" [")
            tag = "[" + tag
            line = "•  " + body + "  " + tag
            assert_fit(line, f_also, col_w)
            y = 130 + ri * 15
            x = col_x[ci]
            dr.text((x, y), "•  " + body + "  ", font=f_also, fill=INK)
            tx = x + tw(f_also, "•  " + body + "  ")
            dr.text((tx, y), tag, font=f_tag, fill=RED if tag == "[CL]" else NAVY)
    assert idx == 37
    # ---- heroes 333-593 ----
    hero_x = [MX, MX + 322 + 12, MX + 2 * (322 + 12)]
    hero_w = 322
    for hi, hero in enumerate(HEROES):
        x = hero_x[hi]
        y0 = 333
        f_kick = F(SANS_B, 11)
        dr.rectangle([x, y0, x + hero_w, y0 + 18], fill=hero["color"])
        dr.text((x + 8, y0 + 3), hero["kicker"], font=f_kick, fill=(255, 255, 255))
        tw_tag = tw(f_kick, hero["tag"])
        dr.text((x + hero_w - 8 - tw_tag, y0 + 3), hero["tag"], font=f_kick, fill=(255, 220, 120))
        art_fn = {"macys": art_macys, "hormuz": art_hormuz, "tariffs": art_tariffs}[hero["art"]]
        img.paste(art_fn(hero_w, 92), (x, y0 + 18))
        dr.rectangle([x, y0 + 18, x + hero_w, y0 + 110], outline=GREY, width=1)
        f_head = F(SERIF, 16)
        head_lines = fit_lines(hero["head"], f_head, hero_w - 8, 2)
        y = y0 + 114
        y = draw_lines(dr, head_lines, x + 4, y, f_head, INK, 19)
        f_deck = F(SANS, 11)
        deck_lines = fit_lines(hero["deck"], f_deck, hero_w - 8, 3)
        y = draw_lines(dr, deck_lines, x + 4, y + 4, f_deck, (40, 40, 44), 13)
        f_why = F(SANS_I, 10)
        why_lines = fit_lines(hero["why"], f_why, hero_w - 8, 3)
        y = draw_lines(dr, why_lines, x + 4, y + 4, f_why, (60, 40, 40), 12)
        why_bottom = y
        stat_top = y0 + 242
        assert stat_top - why_bottom >= 6, "hero %d WHY/stat gap %d < 6" % (hi + 1, stat_top - why_bottom)
        f_stat = F(SANS_B, 11)
        assert_fit(hero["stat"], f_stat, hero_w - 8)
        dr.rectangle([x, stat_top, x + hero_w, y0 + 260], fill=hero["color"])
        dr.text((x + (hero_w - tw(f_stat, hero["stat"])) / 2, stat_top + 3),
                hero["stat"], font=f_stat, fill=(255, 255, 255))
    # ---- cards 601-841 (2 rows x 5) ----
    card_w = 190
    card_xs = [MX + i * 200 for i in range(5)]
    for ci, card in enumerate(CARDS):
        row, col = divmod(ci, 5)
        x = card_xs[col]
        y0 = 601 + row * 124
        label, head, deck, stat, kind, tag = card
        img.paste(art_mini(kind, card_w, 36), (x, y0))
        dr.rectangle([x, y0, x + card_w, y0 + 36], outline=GREY, width=1)
        f_lab = F(SANS_B, 10)
        dr.rectangle([x, y0 + 36, x + card_w, y0 + 49], fill=NAVY)
        lab = label + "  " + tag
        assert_fit(lab, f_lab, card_w - 8)
        dr.text((x + 5, y0 + 38), lab, font=f_lab, fill=(255, 255, 255))
        f_ch = F(SANS_B, 11)
        head_lines = fit_lines(head, f_ch, card_w - 8, 2)
        y = draw_lines(dr, head_lines, x + 4, y0 + 52, f_ch, INK, 12)
        f_cd = F(SANS, 10)
        deck_lines = fit_lines(deck, f_cd, card_w - 8, 2)
        deck_y = y + 2
        y = draw_lines(dr, deck_lines, x + 4, deck_y, f_cd, (40, 40, 44), 11)
        # rev b34: deck ink must end >=3px above the stat line (was overlap -2px)
        deck_bottom = max(dr.textbbox((x + 4, deck_y + i * 11), ln, font=f_cd)[3]
                          for i, ln in enumerate(deck_lines))
        stat_top = y0 + 105
        assert deck_bottom + 3 <= stat_top, \
            "card %s deck/stat overlap: deck_bottom=%d stat_top=%d" % (label, deck_bottom, stat_top)
        f_cs = F(SANS_B, 9)
        assert_fit(stat, f_cs, card_w - 8)
        dr.text((x + 4, stat_top), stat, font=f_cs, fill=RED)
        dr.rectangle([x, y0, x + card_w, y0 + 116], outline=GREY, width=1)
    # ---- map 849-945 ----
    my0, my1 = 849, 927
    dr.rectangle([MX, my0, W - MX, my1], fill=OCEAN)
    mh = my1 - my0

    def proj(lon, lat):
        return (MX + (lon + 180.0) / 360.0 * CW, my0 + (75.0 - lat) / 130.0 * mh)

    for poly in CONTINENTS:
        dr.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(150, 144, 122))
    f_pin = F(SANS_B, 9)
    # rev b34: label boxes must not touch (2px margin); leader lines must
    # not cross any other label's box (sampled segment test)
    label_boxes = {}
    for lon, lat, lab, dx, dy in PINS:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        label_boxes[lab] = (lx, ly, lx + tw(f_pin, lab), ly + 10, px, py)
    _labs = list(label_boxes.items())
    for _i in range(len(_labs)):
        for _j in range(_i + 1, len(_labs)):
            _n1, (_x1, _y1, _x2, _y2, _, _) = _labs[_i]
            _n2, (_u1, _v1, _u2, _v2, _, _) = _labs[_j]
            assert _x2 + 2 <= _u1 or _u2 + 2 <= _x1 or _y2 + 2 <= _v1 or _v2 + 2 <= _y1, \
                "map labels touch: %s vs %s" % (_n1, _n2)

    def _seg_hits_box(ax, ay, bx, by, box):
        for _t in range(101):
            _f = _t / 100.0
            _sx, _sy = ax + (bx - ax) * _f, ay + (by - ay) * _f
            if box[0] <= _sx <= box[2] and box[1] <= _sy <= box[3]:
                return True
        return False

    for _lab, (_lx, _ly, _rx, _ry, _px, _py) in label_boxes.items():
        _cx, _cy = _lx + tw(f_pin, _lab) / 2, _ly + 4
        for _other, _obox in label_boxes.items():
            if _other == _lab:
                continue
            assert not _seg_hits_box(_px, _py, _cx, _cy, _obox), \
                "leader line %s crosses label %s" % (_lab, _other)
    for lon, lat, lab, dx, dy in PINS:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        if abs(dx) > 6 or abs(dy) > 6:
            dr.line([px, py, lx + tw(f_pin, lab) / 2, ly + 4], fill=(90, 90, 96), width=1)
        assert MX <= lx and lx + tw(f_pin, lab) <= W - MX, "pin label out of map: %s" % lab
        assert my0 <= ly and ly + 10 <= my1, "pin label out of map vertically: %s" % lab
        dr.text((lx, ly), lab, font=f_pin, fill=INK)
        dr.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=(255, 255, 255), width=1)
    f_leg = F(SANS, 9)
    assert_fit(MAP_LEGEND, f_leg, CW)
    dr.text((MX, 931), MAP_LEGEND, font=f_leg, fill=GREY)
    # ---- timeline 953-979 ----
    f_tl = F(SANS_B, 10)
    assert_fit(TIMELINE, f_tl, CW)
    dr.line([MX, 953, W - MX, 953], fill=GREY, width=1)
    dr.text((MX + (CW - tw(f_tl, TIMELINE)) / 2, 960), TIMELINE, font=f_tl, fill=NAVY)
    dr.line([MX, 979, W - MX, 979], fill=GREY, width=1)
    # ---- footer 987-1016 ----
    f_ft = F(SANS, 9)
    assert_fit(FOOTER, f_ft, CW)
    dr.text((MX + (CW - tw(f_ft, FOOTER)) / 2, 990), FOOTER, font=f_ft, fill=GREY)
    dr.text((MX + (CW - tw(f_ft, "50 STORIES  ·  THURSDAY 26 NOVEMBER 2026  ·  V32 ALSO-FIRST")) / 2, 1004),
            "50 STORIES  ·  THURSDAY 26 NOVEMBER 2026  ·  V32 ALSO-FIRST", font=f_ft, fill=GREY)
    img.save(OUT)
    print("saved", OUT, img.size)
    return OUT


if __name__ == "__main__":
    render()
