# -*- coding: utf-8 -*-
"""A-32 阿拉伯月站｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A32-01_每晚13度       → 逐字稿 03 鏡（月亮層→尺度層）
  C-A32-02_列宿           → 逐字稿 04 鏡（原文層→直譯層→馬堅層）
  C-A32-03_月站與眉月     → 逐字稿 05 鏡（月站層→眉月層）
  C-A32-04_星圖上的月站   → 逐字稿 09 鏡（9:16 圖卡，可存圖）
  C-A32-05_同一批星       → 逐字稿 10b 鏡（三組層→更多層）
  C-A32-06_今晚八點抬頭看 → 逐字稿 12 鏡（9:16 圖卡，可存圖）
  C-A32-07_月站宇宙       → 逐字稿 14 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-32_阿拉伯月站/_概念圖/（--lang en → _概念圖/en/）

來源：《古蘭經》10:5（Ḥafṣ 讀法；馬堅譯本照 quran.com 所載）；Stellarium arabic_indigenous（28 站、等分站界：
      第 1 站中心＝昴宿六）、chinese（二十八宿）；IAU WGSN 星名（Stellarium common_names.tab 來源 12、
      modern_iau/index.json）；天象 PyEphem 4.2.1 自算（台北 25.033°N、121.565°E，UTC+8；恆星 J2000）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-32_阿拉伯月站/_概念圖")
C.set_base(OUT)
RED, GREY, DIM = "#FF6B6B", "#9AA6C0", "#5A5F6E"
MOONC = "#F4F1E6"
LANG = "zh"
TPE = (25.0330, 121.5654)

TXT = {
    "zh": {
        "c01_title": "月亮每晚往東挪 13°", "c01_sub": "台北，每天清晨 04:30；東在左",
        "east": "← 東", "west": "西 →", "ecl": "黃道",
        "dates": ["5/26", "5/27", "5/28", "5/29", "5/30", "5/31", "6/1"],
        "deg13": "一晚 ≈ 13°", "fist": "伸直手臂，一個拳頭 ≈ 10°", "fist2": "13° ＝ 一個拳頭再寬一點",
        "lap": "27.3 天繞天一圈：360° ÷ 27.3 ≈ 13.2°", "manzil": "manzil　下榻處（單數）",
        "manazil": "manāzil　一站一站（複數）",
        "c02_title": "《古蘭經》10:5", "c02_tr": "huwa lladhī jaʿala l-shamsa ḍiyāʾan wa-l-qamara nūran wa-qaddarahū manāzila …",
        "c02_lit1": "祂讓太陽發光、月亮明亮，", "c02_lit2": "又為月亮定下", "c02_lit3": "一站一站",
        "c02_lit4": "，好讓你們知道年數和曆算。", "c02_litnote": "本社直譯",
        "c02_mj1": "馬堅譯本：「……並為月亮而定", "c02_mj2": "列宿", "c02_mj3": "……」",
        "c02_mj4": "列宿的「宿」＝二十八宿的「宿」", "c02_mj5": "（據 quran.com 所載馬堅譯本）",
        "c03_title": "月站 ≠ 伊斯蘭曆",
        "c03_l1": "月站：月亮在哪裡", "c03_l2": "一晚住一站，28 站繞一圈",
        "c03_r1": "眉月 hilāl：今天幾號", "c03_r2": "月初日落後，西方低空", "c03_r3": "第一次看到細眉月＝新的月份開始",
        "c03_w": "西", "c03_sun": "太陽剛下山",
        "c04_title": "星圖上的月站", "c04_sub": "28 間旅店裡，18 間的名字還在國際天文聯合會（IAU）的正式星名表上",
        "c04_h": ["站", "月站名（意思）", "今天的星名"],
        "c04_foot1": "＊名字後來被移到附近另一顆星：Subra、Iklil、Albaldah、Alrescha",
        "c04_foot2": "字源據 Kunitzsch & Smart（經 Wikipedia 轉引）；IAU 星名表（WGSN）",
        "c05_title": "同一批星，兩套旅店", "c05_sub": "中國二十八宿 × 阿拉伯月站",
        "c05_rows": [("室宿", "水桶的前口", "α、β Peg　同兩顆"), ("壁宿", "水桶的後口", "γ Peg、α And　同兩顆"),
                     ("心宿二", "al-Qalb 心臟", "α Sco　都叫「心」")],
        "c05_more": "更多：", "c05_mrows": [("觜宿", "圓斑", "λ、φ¹、φ² Ori 同三顆"), ("胃宿", "小肚子", "35、39、41 Ari（Stellarium 版）"),
                                          ("亢宿", "≈ 遮蓋", "四顆裡的三顆"), ("鬼宿", "≈ 鼻尖", "兩顆＋鬼星團"),
                                          ("房宿", "≈ 冠冕", "房宿多一顆 ρ Sco")],
        "c05_niu": "牛宿一＝屠夫：同一顆，東亞看見牛，阿拉伯看見宰羊的人",
        "c06_title": "今晚八點抬頭看", "c06_sub": "2027/5/28（五）20:00　台北",
        "c06_E": "東", "c06_SE": "東南", "c06_S": "南", "c06_SW": "西南", "c06_W": "西",
        "c06_names": {"軒轅十四": "軒轅十四", "木星": "木星", "火星": "火星", "角宿一": "角宿一", "氐宿一": "氐宿一",
                      "氐宿四": "氐宿四", "心宿二": "心宿二", "大角": "大角"},
        "c06_st": {"眼睛": "眼睛", "額頭": "額頭", "高舉者": "高舉者", "兩隻螯": "兩隻螯", "心臟": "心臟"},
        "c06_n1": "木星 −1.9 等、火星 +0.7 等，在軒轅十四兩旁（10°、5.5°）",
        "c06_n2": "木星 22:45 前都在 10° 以上；心宿二整晚可見",
        "c06_n3": "週末清晨 04:30：下弦月從「帳篷的吉星」搬進「水桶的前口」",
        "c06_n4": "6/6（日）19:00–19:30：西北偏西低空，第一彎眉月",
        "c06_foot": "PyEphem 自算；行星星等 Mallama & Hilton 2018；高度含大氣折射",
        "c07_title": "月站宇宙", "c07_sub": "同一條月亮的路，好幾種住法",
        "c07_rows": [("A-05", "日本", "照抄中國的格子，配上農具與家事的和名"),
                     ("A-06", "中秋・四文明", "中國、印度、阿拉伯、日本：月亮的二十八間房"),
                     ("A-13", "阿拉伯半島", "看黎明升起的星：13 天一站的沙漠星曆"),
                     ("A-28", "印度", "月亮的二十七位妻子，一晚住一家"),
                     ("A-32", "阿拉伯月站", "跟著月亮走：二十八間旅店的招牌")],
        "c07_foot": "月站系列到這裡；下週五：蘇菲之書",
        "tag": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "The Moon moves 13° east each night", "c01_sub": "Taipei, 04:30 every morning; east is left",
        "east": "← East", "west": "West →", "ecl": "ecliptic",
        "dates": ["26 May", "27 May", "28 May", "29 May", "30 May", "31 May", "1 Jun"],
        "deg13": "one night ≈ 13°", "fist": "a fist at arm's length ≈ 10°", "fist2": "13° = a fist and a bit",
        "lap": "Once round the sky in 27.3 days: 360° ÷ 27.3 ≈ 13.2°", "manzil": "manzil   a lodging (singular)",
        "manazil": "manāzil   lodgings, stage by stage (plural)",
        "c02_title": "Qurʾān 10:5", "c02_tr": "huwa lladhī jaʿala l-shamsa ḍiyāʾan wa-l-qamara nūran wa-qaddarahū manāzila …",
        "c02_lit1": "He made the Sun a radiance and the Moon a light,", "c02_lit2": "and measured out for it",
        "c02_lit3": "stations", "c02_lit4": ", that you may know the number of years and the reckoning.",
        "c02_litnote": "our translation",
        "c02_mj1": "Ma Jian's Chinese: “… 並為月亮而定", "c02_mj2": "列宿", "c02_mj3": " …”",
        "c02_mj4": "lièxiù — the same xiù as the 28 Chinese lunar lodges", "c02_mj5": "(Ma Jian, as given on quran.com)",
        "c03_title": "Lunar stations ≠ Islamic calendar",
        "c03_l1": "Stations: where the Moon is", "c03_l2": "one station a night, 28 round the sky",
        "c03_r1": "Crescent hilāl: what day it is", "c03_r2": "after sunset, low in the west,",
        "c03_r3": "the first thin crescent starts the month",
        "c03_w": "W", "c03_sun": "just after sunset",
        "c04_title": "Lunar stations on today's star maps",
        "c04_sub": "18 of the 28 stations still name stars on the IAU's official list",
        "c04_h": ["#", "Station (meaning)", "IAU star name"],
        "c04_foot1": "* name later moved to a nearby star: Subra, Iklil, Albaldah, Alrescha",
        "c04_foot2": "Etymologies after Kunitzsch & Smart (via Wikipedia); IAU WGSN star names",
        "c05_title": "Same stars, two sets of inns", "c05_sub": "Chinese lunar lodges × Arabic lunar stations",
        "c05_rows": [("Shì", "front mouth of the bucket", "α, β Peg — same pair"),
                     ("Bì", "rear mouth of the bucket", "γ Peg, α And — same pair"),
                     ("Xīn", "al-Qalb, the heart", "α Sco — both say “heart”")],
        "c05_more": "More:", "c05_mrows": [("Zī", "the circular mark", "λ, φ¹, φ² Ori — same three"),
                                          ("Wèi", "the little belly", "35, 39, 41 Ari (Stellarium)"),
                                          ("Kàng", "≈ the cover", "three of its four"),
                                          ("Guǐ", "≈ the nostrils", "two stars + the Beehive"),
                                          ("Fáng", "≈ the diadem", "Fáng adds ρ Sco")],
        "c05_niu": "β Cap: an ox in China, a slaughterer in Arabia",
        "c06_title": "Look up tonight at 8 pm", "c06_sub": "Fri 28 May 2027, 20:00, Taipei",
        "c06_E": "E", "c06_SE": "SE", "c06_S": "S", "c06_SW": "SW", "c06_W": "W",
        "c06_names": {"軒轅十四": "Regulus", "木星": "Jupiter", "火星": "Mars", "角宿一": "Spica",
                      "氐宿一": "Zubenelgenubi", "氐宿四": "Zubeneschamali", "心宿二": "Antares", "大角": "Arcturus"},
        "c06_st": {"眼睛": "the eyes", "額頭": "the forehead", "高舉者": "the high one", "兩隻螯": "the claws",
                   "心臟": "the heart"},
        "c06_n1": "Jupiter (−1.9) and Mars (+0.7) flank Regulus (10°, 5.5°)",
        "c06_n2": "Jupiter stays above 10° until 22:45; Antares all night",
        "c06_n3": "Weekend, 04:30: the last-quarter Moon moves from the Tents into the Front Bucket Mouth",
        "c06_n4": "Sun 6 Jun, 19:00–19:30: first thin crescent, low in the WNW",
        "c06_foot": "Computed with PyEphem; planet magnitudes Mallama & Hilton 2018; altitudes include refraction",
        "c07_title": "The lunar-station universe", "c07_sub": "One road for the Moon, many ways to lodge",
        "c07_rows": [("A-05", "Japan", "China's grid, with Japanese names of farm and household tools"),
                     ("A-06", "Four civilisations", "China, India, Arabia, Japan: 28 rooms for the Moon"),
                     ("A-13", "Arabian Peninsula", "Dawn-rising stars: a desert calendar, 13 days a station"),
                     ("A-28", "India", "The Moon's 27 wives, one house a night"),
                     ("A-32", "Arabic stations", "Follow the Moon: the signs of 28 inns")],
        "c07_foot": "End of the lunar-station series; next Friday: al-Ṣūfī's Book",
        "tag": "#WorldSkyCultures  #NTNUAstronomy",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 天象 ══════════════════════
def _obs(when, tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.elevation = 0
    o.temp, o.pressure = 25.0, 1010.0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def moons_week():
    import ephem
    out = []
    for d in ("2027/5/26", "2027/5/27", "2027/5/28", "2027/5/29", "2027/5/30", "2027/5/31", "2027/6/1"):
        o = _obs(d + " 04:30"); b = ephem.Moon(); b.compute(o)
        e = ephem.Ecliptic(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=o.date)
        out.append((math.degrees(e.lon), math.degrees(e.lat), b.phase / 100.0))
    return out


def altaz_8pm():
    import ephem
    o = _obs("2027/5/28 20:00")
    S = dict(G.load_stars(BASE))
    pts = {}
    for nm, h in (("軒轅十四", 49669), ("角宿一", 65474), ("氐宿一", 72622), ("氐宿四", 74785),
                  ("心宿二", 80763), ("大角", 69673), ("Algieba", 50583), ("Denebola", 57632),
                  ("Zosma", 54872), ("δSco", 78401), ("βSco", 78820), ("πSco", 78265), ("σSco", 80112),
                  ("τSco", 81266), ("γVir", 61941), ("εVir", 63608), ("δVir", 63090), ("ηLeo", 49583),
                  ("ζLeo", 50335), ("μLeo", 48455), ("εLeo", 47908), ("θLeo", 54879)):
        ra, dec = S[h][:2]
        b = ephem.FixedBody(); b._ra, b._dec, b._epoch = math.radians(ra), math.radians(dec), ephem.J2000
        b.compute(o)
        pts[nm] = (math.degrees(b.az), math.degrees(b.alt), S[h][2])
    for nm, b in (("木星", ephem.Jupiter()), ("火星", ephem.Mars())):
        b.compute(o)
        pts[nm] = (math.degrees(b.az), math.degrees(b.alt), float(b.mag))
    return pts


def moon_disc(ax, x, y, r, frac, sun_left=True, dim=1.0, z=6):
    """月相：亮面朝太陽（sun_left＝太陽在左邊）"""
    ax.add_patch(C.Circle((x, y), r, fc=DIM, ec="none", alpha=.6 * dim, zorder=z))
    s = -1.0 if sun_left else 1.0
    pts = [(x + s * r * math.cos(math.radians(t)), y + r * math.sin(math.radians(t))) for t in range(-90, 91, 6)]
    pts += [(x + s * r * (1 - 2 * frac) * math.cos(math.radians(t)), y + r * math.sin(math.radians(t)))
            for t in range(90, -91, -6)]
    ax.add_patch(C.Polygon(pts, closed=True, fc=MOONC, ec="none", alpha=.98 * dim, zorder=z + 1))


# ══════════════════════ C-A32-01 每晚 13° ══════════════════════
MW = moons_week()


def c01_x(lon):
    return -(lon - 336.0) * 0.0205           # 東在左；寶瓶 336° 置中


def c01_moons(ax):
    T(ax, 0, 0.86, tx("c01_title"), 30, WHITE)
    T(ax, 0, 0.78, tx("c01_sub"), 17, GREY, w="normal")
    ax.plot([c01_x(370), c01_x(298)], [c01_x(0) * 0 + 0.10 + (-0.0), 0.10], c=GREY, lw=1.2, alpha=.0)
    xs = [c01_x(l if l > 200 else l + 360) for l, b, f in MW]
    ys = [0.12 + b * 0.02 for l, b, f in MW]
    ax.plot([c01_x(368), c01_x(300)], [0.12 + 0.0, 0.12], c="#A9B8D6", lw=1.6, alpha=.5, ls=(0, (6, 4)))
    T(ax, 0.90, 0.17, tx("ecl"), 14, "#A9B8D6", w="normal", ha="right")
    for (l, b, f), x, y, d in zip(MW, xs, ys, tx("dates")):
        moon_disc(ax, x, y, 0.058, f, sun_left=True)      # 清晨：太陽在東方（左）
        T(ax, x, y - 0.13, d, 16, WHITE)
        T(ax, x, y - 0.20, f"{f * 100:.0f}%", 13, GREY, w="normal")
    T(ax, -0.88, 0.40, tx("east"), 17, AMBER, ha="left")
    T(ax, 0.88, 0.40, tx("west"), 17, GREY, ha="right", w="normal")


def c01_scale(ax):
    xs = [c01_x(l if l > 200 else l + 360) for l, b, f in MW]
    a, b = xs[3], xs[4]
    y = 0.34
    ax.plot([b, b, a, a], [y - 0.03, y, y, y - 0.03], c=AMBER, lw=2.4, zorder=8)
    T(ax, (a + b) / 2, y + 0.06, tx("deg13"), 20, AMBER)
    # 伸臂拳頭比例尺（10°）
    f10 = 10 * 0.0215
    x0, y0 = -0.45, -0.38
    ax.add_patch(C.FancyBboxPatch((x0, y0 - 0.06), f10, 0.12, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="none", ec=WHITE, lw=2.0, alpha=.9, zorder=8))
    for i in range(1, 4):
        ax.plot([x0 + f10 * i / 4] * 2, [y0 + 0.01, y0 + 0.06], c=WHITE, lw=1.2, alpha=.6, zorder=8)
    ax.plot([x0, x0 + 13 * 0.0215], [y0 - 0.10] * 2, c=AMBER, lw=2.4, zorder=8)
    T(ax, x0 + f10 + 0.06, y0 + 0.02, tx("fist"), 16, WHITE, ha="left", w="normal")
    T(ax, x0 + 13 * 0.0215 + 0.04, y0 - 0.10, tx("fist2"), 16, AMBER, ha="left")
    T(ax, 0, -0.56, tx("lap"), 15, GREY, w="normal")
    T(ax, 0, -0.68, tx("manzil"), 19, WHITE)
    T(ax, 0, -0.77, tx("manazil"), 19, AMBER)


# ══════════════════════ C-A32-02 列宿 ══════════════════════
AYA = "هُوَ الَّذِي جَعَلَ الشَّمْسَ ضِيَاءً وَالْقَمَرَ نُورًا"
AYA2 = "وَقَدَّرَهُ مَنَازِلَ لِتَعْلَمُوا عَدَدَ السِّنِينَ وَالْحِسَابَ"


def c02_orig(ax):
    T(ax, 0, 0.84, tx("c02_title"), 30, WHITE)
    T(ax, 0, 0.66, AYA, 24, WHITE, w="normal")
    T(ax, 0, 0.54, AYA2, 24, WHITE, w="normal")
    T(ax, 0, 0.38, "مَنَازِلَ", 40, AMBER, w="normal")
    T(ax, 0, 0.27, "manāzil", 22, AMBER)
    T(ax, 0, 0.18, tx("c02_tr"), 10.5, GREY, w="normal")


def c02_lit(ax):
    T(ax, 0, 0.02, tx("c02_lit1"), 20, WHITE, w="normal")
    if LANG == "zh":
        T(ax, -0.18, -0.08, tx("c02_lit2"), 20, WHITE, w="normal")
        T(ax, 0.10, -0.08, tx("c02_lit3"), 22, AMBER)
        T(ax, 0, -0.18, tx("c02_lit4")[1:], 20, WHITE, w="normal")
    else:
        T(ax, 0, -0.08, tx("c02_lit2") + " " + tx("c02_lit3"), 20, WHITE, w="normal")
        T(ax, 0, -0.18, tx("c02_lit4")[2:], 17, WHITE, w="normal")
    T(ax, 0.86, -0.26, tx("c02_litnote"), 13, GREY, w="normal", ha="right")


def c02_mj(ax):
    if LANG == "zh":
        T(ax, -0.10, -0.42, tx("c02_mj1"), 20, WHITE, w="normal")
        T(ax, 0.335, -0.42, tx("c02_mj2"), 26, AMBER)
        T(ax, 0.475, -0.42, tx("c02_mj3"), 20, WHITE, w="normal")
    else:
        T(ax, 0, -0.42, tx("c02_mj1") + tx("c02_mj2") + tx("c02_mj3"), 18, WHITE, w="normal")
    ax.plot([-0.55, 0.55], [-0.52, -0.52], c=AMBER, lw=1.0, alpha=.5)
    T(ax, 0, -0.62, tx("c02_mj4"), 20, AMBER)
    T(ax, 0, -0.73, tx("c02_mj5"), 13, GREY, w="normal")


# ══════════════════════ C-A32-03 月站與眉月 ══════════════════════
def c03_st(ax):
    T(ax, 0, 0.86, tx("c03_title"), 30, WHITE)
    cx, cy, R = -0.47, 0.10, 0.34
    for i in range(28):
        a = math.radians(90 + i * 360 / 28)
        ax.plot([cx + R * 0.82 * math.cos(a), cx + R * 1.08 * math.cos(a)],
                [cy + R * 0.82 * math.sin(a), cy + R * 1.08 * math.sin(a)], c=AMBER, lw=1.2, alpha=.8)
    for r in (0.82, 1.08):
        ax.add_patch(C.Circle((cx, cy), R * r, fc="none", ec=AMBER, lw=1.4, alpha=.8))
    for k, al in ((0, .35), (1, .6), (2, 1.0)):
        a = math.radians(90 + (k + 0.5) * 360 / 28)
        moon_disc(ax, cx + R * 0.95 * math.cos(a), cy + R * 0.95 * math.sin(a), 0.035, 0.5,
                  sun_left=False, dim=al)
    C.arrow(ax, (cx + R * 0.6 * math.cos(math.radians(150)), cy + R * 0.6 * math.sin(math.radians(150))),
            (cx + R * 0.6 * math.cos(math.radians(100)), cy + R * 0.6 * math.sin(math.radians(100))),
            c=AMBER, lw=2.0, alpha=.9, style="-|>")
    T(ax, cx, -0.42, tx("c03_l1"), 20, AMBER)
    T(ax, cx, -0.52, tx("c03_l2"), 15, WHITE, w="normal")


def c03_hilal(ax):
    x0, x1, yh = 0.04, 0.92, -0.18
    for i, al in enumerate((0.05, 0.06, 0.08, 0.10)):
        ax.add_patch(C.Ellipse((0.62, yh), 0.56 - i * 0.12, 0.34 - i * 0.07,
                               fc="#FF9A4A", ec="none", alpha=al, zorder=2))
    ax.plot([x0, x1], [yh, yh], c=WHITE, lw=2.0, alpha=.8, zorder=4)
    ax.add_patch(C.Rectangle((x0, yh - 0.2), x1 - x0, 0.2, fc="#05070F", ec="none", zorder=3))
    T(ax, (x0 + x1) / 2 + 0.14, yh - 0.06, tx("c03_w"), 16, WHITE)
    T(ax, (x0 + x1) / 2 + 0.14, yh - 0.14, tx("c03_sun"), 12, GREY, w="normal")
    # 細眉月（亮邊朝右下＝太陽方向）
    mx, my, r = 0.40, 0.22, 0.075
    ax.add_patch(C.Circle((mx, my), r, fc=DIM, ec="none", alpha=.35, zorder=5))
    ang = math.radians(-35)
    pts = [(mx + r * math.cos(t + ang), my + r * math.sin(t + ang)) for t in
           [math.radians(a) for a in range(-90, 91, 5)]]
    pts += [(mx + r * 0.72 * math.cos(t + ang), my + r * math.sin(t + ang)) for t in
            [math.radians(a) for a in range(90, -91, -5)]]
    ax.add_patch(C.Polygon(pts, closed=True, fc=MOONC, ec="none", alpha=.98, zorder=6))
    T(ax, 0.48, 0.42, "هِلَال", 26, AMBER, w="normal")
    T(ax, 0.48, -0.42, tx("c03_r1"), 20, AMBER)
    T(ax, 0.48, -0.52, tx("c03_r2"), 15, WHITE, w="normal")
    T(ax, 0.48, -0.60, tx("c03_r3"), 15, WHITE, w="normal")


# ══════════════════════ C-A32-04 星圖上的月站（圖卡） ══════════════════════
ROWS4 = [  # (站號, 轉寫, 中譯, 英譯, IAU 名（拜耳）)
    (1, "al-Thurayyā", "昴宿", "the Pleiades", "—"),
    (2, "al-Dabarān", "跟在後面的", "the follower", "Aldebaran（α Tau）"),
    (4, "al-Hanʿah", "低彎", "the downward bend", "Alhena（γ Gem）"),
    (7, "al-Ṭarf", "眼睛", "the eyes", "Alterf（λ Leo）・Tarf（β Cnc）"),
    (8, "al-Jabhah", "額頭", "the forehead", "Algieba（γ Leo）"),
    (9, "al-Zubrah", "鬃毛", "the mane", "Subra＊（ο Leo）"),
    (11, "al-ʿAwwāʾ", "彎曲處", "the bend", "Zavijava（β Vir）・Minelauva（δ Vir）"),
    (13, "al-Ghafr", "遮蓋", "the cover", "Elgafar（φ Vir）"),
    (14, "al-Zubānā", "兩隻螯", "the claws", "Zubenelgenubi・Zubeneschamali・Zubenelhakrabi"),
    (15, "al-Iklīl", "冠冕", "the diadem", "Iklil＊（ρ Sco）"),
    (17, "al-Shawlah", "翹起的尾巴", "the raised tail", "Shaula（λ Sco）"),
    (19, "al-Baldah", "空地", "the empty place", "Albaldah＊（π Sgr）"),
    (20, "Saʿd al-Dhābiḥ", "屠夫的吉星", "the slaughterer", "Dabih（β Cap）"),
    (21, "Saʿd Bulaʿ", "吞嚥者的吉星", "the swallower", "Albali（ε Aqr）"),
    (22, "Saʿd al-Suʿūd", "吉中之吉", "luckiest of the lucky", "Sadalsuud（β Aqr）"),
    (23, "Saʿd al-Akhbiyah", "帳篷的吉星", "of the tents", "Sadachbia（γ Aqr）"),
    (26, "al-Rishāʾ", "水桶的繩子", "the bucket rope", "Alrescha＊（α Psc）"),
    (27, "al-Sharaṭān", "兩個記號", "the two signs", "Sheratan（β Ari）"),
    (28, "al-Buṭayn", "小肚子", "the little belly", "Botein（δ Ari）"),
]


def c04_card(ax):
    T(ax, 0.5, 0.950, tx("c04_title"), 26, WHITE)
    ax.text(0.5, 0.912, tx("c04_sub"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center",
            va="center", wrap=True)
    ax.plot([0.03, 0.97], [0.890, 0.890], c=WHITE, lw=1.0, alpha=.4)
    X0, X1, X2 = 0.04, 0.12, 0.50
    for x, h in zip((X0, X1, X2), tx("c04_h")):
        ax.text(x, 0.872, h, fontproperties=C.FP, fontsize=11, color=GREY, ha="left", va="center", weight="bold")
    y = 0.852
    for n, tr, zh, en, iau in ROWS4[1:]:
        ax.plot([0.03, 0.97], [y + 0.012, y + 0.012], c=WHITE, lw=0.5, alpha=.15)
        ax.text(X0, y - 0.006, f"{n}", fontproperties=C.FP, fontsize=11, color=GREY, ha="left", va="center")
        ax.text(X1, y + 0.001, tr, fontproperties=C.FP, fontsize=11, color=AMBER, ha="left", va="center",
                weight="bold")
        ax.text(X1, y - 0.016, zh if LANG == "zh" else en, fontproperties=C.FP, fontsize=10, color=WHITE,
                ha="left", va="center")
        parts = iau.split("・")
        if len(parts) > 2:
            ax.text(X2, y + 0.001, "・".join(parts[:2]), fontproperties=C.FP, fontsize=10.5, color=WHITE,
                    ha="left", va="center")
            ax.text(X2, y - 0.016, parts[2], fontproperties=C.FP, fontsize=10.5, color=WHITE, ha="left",
                    va="center")
        else:
            ax.text(X2, y - 0.006, iau if len(iau) < 26 else iau.replace("・", "\n"), fontproperties=C.FP,
                    fontsize=10.5, color=WHITE, ha="left", va="center", linespacing=1.15)
        y -= 0.0425
    ax.text(0.5, 0.072, tx("c04_foot1"), fontproperties=C.FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.052, tx("c04_foot2"), fontproperties=C.FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.026, tx("tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A32-05 同一批星 ══════════════════════
def c05_three(ax):
    T(ax, 0, 0.86, tx("c05_title"), 30, WHITE)
    T(ax, 0, 0.78, tx("c05_sub"), 16, GREY, w="normal")
    y = 0.58
    for cn, ar, note in tx("c05_rows"):
        T(ax, -0.52, y, cn, 26, PURPLE)
        T(ax, -0.25, y, "＝", 24, WHITE)
        T(ax, 0.25, y, ar, 24 if LANG == "zh" else 19, AMBER)
        T(ax, 0.0, y - 0.085, note, 14, GREY, w="normal")
        y -= 0.22


def c05_more(ax):
    ax.plot([-0.8, 0.8], [-0.12, -0.12], c=WHITE, lw=0.8, alpha=.3)
    T(ax, -0.80, -0.19, tx("c05_more"), 15, GREY, ha="left")
    y = -0.27
    for cn, ar, note in tx("c05_mrows"):
        T(ax, -0.62, y, cn, 16, PURPLE, ha="left")
        T(ax, -0.36, y, ar, 16, AMBER, ha="left")
        T(ax, 0.10, y, note, 13, GREY, ha="left", w="normal")
        y -= 0.085
    T(ax, 0, y - 0.04, tx("c05_niu"), 14, WHITE, w="normal")


# ══════════════════════ C-A32-06 今晚八點抬頭看（圖卡） ══════════════════════
def c06_card(ax):
    P = altaz_8pm()
    T(ax, 0.5, 0.950, tx("c06_title"), 28, WHITE)
    T(ax, 0.5, 0.912, tx("c06_sub"), 14, GREY, w="normal")
    AZ0, AZ1, Y0, ALT1 = 85.0, 285.0, 0.36, 80.0
    px = lambda az: 0.04 + (az - AZ0) / (AZ1 - AZ0) * 0.92
    py = lambda alt: Y0 + alt / ALT1 * 0.50
    ax.add_patch(C.Rectangle((0.0, Y0 - 0.06), 1.0, 0.06, fc="#05070F", ec="none", zorder=3))
    ax.plot([0.02, 0.98], [Y0, Y0], c=WHITE, lw=1.6, alpha=.8, zorder=4)
    for alt in (20, 40, 60):
        ax.plot([0.04, 0.96], [py(alt)] * 2, c=WHITE, lw=0.6, alpha=.12, ls=(0, (3, 4)))
        ax.text(0.965, py(alt), f"{alt}°", fontproperties=C.FP, fontsize=8.5, color=GREY, ha="left", va="center")
    for az, k in ((90, "c06_E"), (135, "c06_SE"), (180, "c06_S"), (225, "c06_SW"), (270, "c06_W")):
        ax.text(px(az), Y0 - 0.025, tx(k), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center",
                va="center", weight="bold", zorder=5)
    for a, b, col in (("軒轅十四", "Algieba", BLUE), ("Algieba", "ζLeo", BLUE), ("ζLeo", "μLeo", BLUE),
                      ("μLeo", "εLeo", BLUE), ("Algieba", "Zosma", BLUE), ("Zosma", "Denebola", BLUE),
                      ("Denebola", "θLeo", BLUE), ("θLeo", "軒轅十四", BLUE),
                      ("氐宿一", "氐宿四", RED), ("δSco", "πSco", RED), ("δSco", "βSco", RED),
                      ("δSco", "σSco", RED), ("σSco", "心宿二", RED), ("心宿二", "τSco", RED)):
        if a in P and b in P:
            ax.plot([px(P[a][0]), px(P[b][0])], [py(P[a][1]), py(P[b][1])], c=col, lw=1.3, alpha=.7, zorder=5)
    for nm, (az, alt, v) in P.items():
        if alt < 0 or nm in ("木星", "火星"):
            continue
        s = max(4, (5.5 - v) ** 1.8 * 4)
        ax.scatter([px(az)], [py(alt)], s=s, c=WHITE, lw=0, zorder=6)
    ax.scatter([px(P["木星"][0])], [py(P["木星"][1])], s=90, c=WHITE, lw=0, zorder=7)
    ax.scatter([px(P["火星"][0])], [py(P["火星"][1])], s=50, c=RED, lw=0, zorder=7)
    N, ST = tx("c06_names"), tx("c06_st")
    lab = [("木星", 0.0, -0.024, WHITE, "眼睛"), ("火星", -0.085, 0.0, RED, "額頭"),
           ("軒轅十四", 0.075, -0.012, WHITE, None),
           ("角宿一", 0.0, -0.022, WHITE, "高舉者"), ("氐宿一", 0.0, -0.022, WHITE, None),
           ("氐宿四", 0.0, 0.020, WHITE, None), ("心宿二", 0.0, -0.022, RED, "心臟"),
           ("大角", 0.0, 0.020, WHITE, None)]
    for nm, dx, dy, col, st in lab:
        az, alt, v = P[nm]
        t = N[nm] + (f"（{ST[st]}）" if st and LANG == "zh" else (f" ({ST[st]})" if st else ""))
        ax.text(px(az) + dx, py(alt) + dy, t, fontproperties=C.FP, fontsize=10.5, color=col, ha="center",
                va="center", zorder=8)
    zb = ((P["氐宿一"][0] + P["氐宿四"][0]) / 2, (P["氐宿一"][1] + P["氐宿四"][1]) / 2)
    ax.text(px(zb[0]) - 0.07, py(zb[1]), ST["兩隻螯"], fontproperties=C.FP, fontsize=10, color=AMBER,
            ha="center", va="center")
    y = 0.255
    for k in ("c06_n1", "c06_n2", "c06_n3", "c06_n4"):
        ax.text(0.5, y, tx(k), fontproperties=C.FP, fontsize=10.5 if LANG == "zh" else 9, color=WHITE,
                ha="center", va="center")
        y -= 0.038
    ax.text(0.5, 0.060, tx("c06_foot"), fontproperties=C.FP, fontsize=8.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, tx("tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")
    return P


# ══════════════════════ C-A32-07 月站宇宙（圖卡） ══════════════════════
def c07_card(ax):
    T(ax, 0.5, 0.950, tx("c07_title"), 28, WHITE)
    T(ax, 0.5, 0.912, tx("c07_sub"), 14, GREY, w="normal")
    w = 0.40
    iax = ax.figure.add_axes([0.5 - w / 2, 0.735 - w * 1215 / 2160 / 2, w, w * 1215 / 2160])
    iax.set_xlim(-1, 1); iax.set_ylim(-1, 1); iax.set_aspect("equal"); iax.axis("off"); iax.patch.set_alpha(0)
    for i in range(28):
        a = math.radians(90 + i * 360 / 28)
        iax.plot([0.80 * math.cos(a), math.cos(a)], [0.80 * math.sin(a), math.sin(a)], c=AMBER, lw=1.0, alpha=.7)
    for r in (0.80, 1.0):
        iax.add_patch(C.Circle((0, 0), r, fc="none", ec=AMBER, lw=1.2, alpha=.7))
    moon_disc(iax, 0, 0, 0.30, 0.5, sun_left=False)
    y = 0.53
    for ep, nm, desc in tx("c07_rows"):
        col = AMBER if ep == "A-32" else WHITE
        ax.add_patch(C.FancyBboxPatch((0.05, y - 0.045), 0.90, 0.075,
                                      boxstyle="round,pad=0.004,rounding_size=0.012",
                                      fc="#1B2240", ec=col, lw=1.1, zorder=3))
        ax.text(0.08, y + 0.008, ep, fontproperties=C.FP, fontsize=11, color=GREY, ha="left", va="center",
                zorder=4)
        ax.text(0.20, y + 0.008, nm, fontproperties=C.FP, fontsize=13, color=col, ha="left", va="center",
                weight="bold", zorder=4)
        ax.text(0.08, y - 0.022, desc, fontproperties=C.FP, fontsize=10.5 if LANG == "zh" else 9, color=WHITE,
                ha="left", va="center", zorder=4)
        y -= 0.092
    ax.text(0.5, 0.060, tx("c07_foot"), fontproperties=C.FP, fontsize=11, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, tx("tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


def emit_all():
    C.emit("", [("月亮", c01_moons), ("尺度", c01_scale)], title="C-A32-01_每晚13度")
    C.emit("", [("原文", c02_orig), ("直譯", c02_lit), ("馬堅", c02_mj)], title="C-A32-02_列宿")
    C.emit("", [("月站", c03_st), ("眉月", c03_hilal)], title="C-A32-03_月站與眉月")
    C.emit("", [("三組", c05_three), ("更多", c05_more)], title="C-A32-05_同一批星")
    for name, fn in (("C-A32-04_星圖上的月站", c04_card), ("C-A32-06_今晚八點抬頭看", c06_card),
                     ("C-A32-07_月站宇宙", c07_card)):
        f, ax = C.newcard(dark=True)
        r = fn(ax)
        C.save(f, "", f"{name}_圖卡.png", transparent=False)
        if isinstance(r, dict):
            for k, (az, alt, v) in r.items():
                if not k[0].isascii():
                    print(f"    {k}: 方位 {az:.0f}° 高 {alt:.1f}°")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("  月亮 04:30：" + "、".join(f"{d} 黃經 {l:.1f}° {f * 100:.0f}%" for (l, b, f), d in
                                    zip(MW, TXT["zh"]["dates"])))
    emit_all()


if __name__ == "__main__":
    main()
