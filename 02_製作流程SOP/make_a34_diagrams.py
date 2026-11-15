# -*- coding: utf-8 -*-
"""A-34 蘇菲之書｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A34-01_蘇菲是誰            → 逐字稿 02 鏡（生平層→書名層）
  C-A34-02_托勒密到蘇菲        → 逐字稿 03 鏡（星表層→核對層）
  C-A34-03_歲差                → 逐字稿 04 鏡（黃道層→平移層）
  C-A34-03b_蘇菲的尺           → 逐字稿 05 鏡（單位層→銀河層）
  C-A34-04_天空與天球儀        → 逐字稿 08 鏡（天空層→天球儀層）
  C-A34-05_用蘇菲的眼睛看天    → 逐字稿 14 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-34_蘇菲之書/_概念圖/（--lang en → _概念圖/en/，這次只出 zh）

來源：Stellarium arabic_al-sufi（stellarium-master；al-Ajaji：description 的「一肘＝2°20′」「矛＝6 肘」、
      Aql_9「碰到銀河」原文、And／SFA 連線）；Kunitzsch 1987（ESO Messenger 49：Ptolemy + 12°42′、
      每個星座兩張圖：天球儀上／天空中）；Kunitzsch 1989（全書結構）；Hafez 2010（964 年曆元）；
      生卒 903–986、約 964 年獻書 ʿAḍud al-Dawla（逐字稿考據備忘）；天象 PyEphem 4.2.1 自算（台北 6/4–6/5）。
      02、03 的星點是示意（不代表特定星的星等或黃經），圖上註明「示意」。
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-34_蘇菲之書/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#9AA6C0"
S = None
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "蘇菲是誰", "c01_sub": "ʿAbd al-Raḥmān al-Ṣūfī・歐洲人叫他 Azophi",
        "e903": "903", "e903b": "生於 Rayy\n（今德黑蘭附近）",
        "ecourt": "布伊王朝", "ecourtb": "在宮廷\n做天文",
        "e964": "約 964", "e964b": "把書獻給君主\nʿAḍud al-Dawla",
        "e986": "986", "e986b": "去世",
        "persian": "波斯人，用當時學術通用的阿拉伯文寫作",
        "book_zh": "《恆星圖像之書》", "book_tr": "Kitāb Ṣuwar al-Kawākib al-Thābita",
        "age": "到 2027 年：一千零六十多年",
        "c02_title": "托勒密 → 蘇菲", "c02_sub": "示意：星點大小＝亮度",
        "ptol": "托勒密《天文學大成》", "ptol2": "約西元 150 年・48 星座・1,000 多顆星",
        "sufi": "蘇菲重新對著天空看", "sufi2": "約 964 年・一顆一顆核對",
        "fix": "亮度不對 → 改", "miss": "星表漏掉的星 → 在書裡點出來",
        "c03_title": "歲差：整片星空沿黃道慢慢挪動", "c03_sub": "示意：星點位置不代表特定的星",
        "ecl": "黃道", "east": "← 東（黃經增加）",
        "p137": "托勒密星表（曆元 137 年）", "p964": "蘇菲（964 年）",
        "shift": "全部 ＋12°42′",
        "c03b_title": "蘇菲的尺", "c03b_sub": "全書七百多處角距離",
        "moon": "月亮直徑 ≈ 0.5°", "cubit": "一肘 ≈ 2°20′", "spear": "一矛 ＝ 6 肘 ≈ 14°",
        "others": "還有人高、拃、指",
        "aql": "天鷹座（蘇菲的連線）", "touch": "這顆星「碰到銀河」",
        "touch2": "Aql_9：天鷹尾巴下面、有點距離的那顆",
        "mw": "銀河",
        "c04_title": "每個星座畫兩次", "c04_sub": "仙女座＋大魚（本集星圖的連線）",
        "sky": "天空中\n抬頭看到的", "globe": "天球儀上\n從外面看天",
        "mirror": "左右相反",
        "e": "東", "w": "西",
        "c05_title": "用蘇菲的眼睛看天", "c05_date": "2027 年 6 月 4 日（五）台北",
        "r1t": "晚上 8 點", "r1a": "大角", "r1b": "東方高處 71°，快到頭頂",
        "r1c": "al-Simāk al-Rāmiḥ　拿矛的高舉者",
        "r2a": "角宿一", "r2b": "南方偏東 53°（8:29 正南）", "r2c": "al-Simāk al-Aʿzal　沒拿武器的高舉者",
        "r3a": "織女", "r3b": "東北 19°", "r3c": "al-Nasr al-Wāqiʿ　俯衝的老鷹 → Vega",
        "r4t": "晚上 10 點", "r4a": "牛郎", "r4b": "正東 18.5°（8:36 升起）",
        "r4c": "al-Nasr al-Ṭāʾir　飛翔的老鷹 → Altair",
        "r5t": "6/5 凌晨 2:30–3:30", "r5a": "仙女座大星系", "r5b": "東北 24°→35°",
        "r5c": "蘇菲記下的「一小抹像雲的光斑」・3.4 等",
        "moon_note": "6/5 03:40 新月：整夜沒有月光", "dark": "找遠離光害的暗處，肉眼就看得到",
        "src": "PyEphem 自算（台北 25.0°N）；Stellarium arabic_al-sufi",
    },
    "en": {
        "c01_title": "Who was al-Ṣūfī?", "c01_sub": "ʿAbd al-Raḥmān al-Ṣūfī · Latin: Azophi",
        "e903": "903", "e903b": "born in Rayy\n(near modern Tehran)",
        "ecourt": "Buyid court", "ecourtb": "astronomer\nat court",
        "e964": "c. 964", "e964b": "dedicates the book\nto ʿAḍud al-Dawla",
        "e986": "986", "e986b": "dies",
        "persian": "A Persian, writing in Arabic — the language of scholarship",
        "book_zh": "Book of the Images of the Fixed Stars", "book_tr": "Kitāb Ṣuwar al-Kawākib al-Thābita",
        "age": "Over 1,060 years old in 2027",
        "c02_title": "Ptolemy → al-Ṣūfī", "c02_sub": "Schematic: dot size = brightness",
        "ptol": "Ptolemy's Almagest", "ptol2": "c. 150 CE · 48 constellations · 1,000+ stars",
        "sufi": "al-Ṣūfī checks the real sky", "sufi2": "c. 964 · star by star",
        "fix": "wrong brightness → corrected", "miss": "stars the catalogue missed → noted in the text",
        "c03_title": "Precession: the whole sky creeps along the ecliptic", "c03_sub": "Schematic positions",
        "ecl": "ecliptic", "east": "← east (longitude increases)",
        "p137": "Ptolemy's catalogue (epoch 137)", "p964": "al-Ṣūfī (964)",
        "shift": "all + 12°42′",
        "c03b_title": "al-Ṣūfī's rulers", "c03b_sub": "700+ angular distances in the book",
        "moon": "Moon ≈ 0.5°", "cubit": "1 cubit ≈ 2°20′", "spear": "1 spear = 6 cubits ≈ 14°",
        "others": "also: man's height, span, finger",
        "aql": "Aquila (al-Ṣūfī's lines)", "touch": "this star “touches the Milky Way”",
        "touch2": "Aql_9: some distance under the eagle's tail",
        "mw": "Milky Way",
        "c04_title": "Every constellation, drawn twice", "c04_sub": "Andromeda + the Great Fish",
        "sky": "in the sky\nlooking up", "globe": "on the globe\nseen from outside",
        "mirror": "mirror images",
        "e": "E", "w": "W",
        "c05_title": "See the sky with al-Ṣūfī's eyes", "c05_date": "Fri 4 June 2027 · Taipei",
        "r1t": "8 pm", "r1a": "Arcturus", "r1b": "high in the east, 71°",
        "r1c": "al-Simāk al-Rāmiḥ — the high one with the spear",
        "r2a": "Spica", "r2b": "south, 53° (due south 8:29)", "r2c": "al-Simāk al-Aʿzal — the unarmed high one",
        "r3a": "Vega", "r3b": "northeast, 19°", "r3c": "al-Nasr al-Wāqiʿ — the swooping eagle",
        "r4t": "10 pm", "r4a": "Altair", "r4b": "due east, 18.5° (rises 8:36)",
        "r4c": "al-Nasr al-Ṭāʾir — the flying eagle",
        "r5t": "5 June 2:30–3:30 am", "r5a": "Andromeda Galaxy", "r5b": "northeast, 24°→35°",
        "r5c": "al-Ṣūfī's “cloud-like smudge” · mag 3.4",
        "moon_note": "New Moon 5 June 03:40: no moonlight all night", "dark": "Find a dark site — naked eye",
        "src": "PyEphem (Taipei 25.0°N); Stellarium arabic_al-sufi",
    },
}


def tx(k):
    return TXT[LANG][k]


AR_BOOK = "كتاب صور الكواكب الثابتة"
AR_TOUCH = "مماس للمجرّة"


def AR(ax, x, y, s, size, c=WHITE):
    ax.text(x, y, G.rtl(s), fontproperties=C.FP, fontsize=size, color=c, ha="center", va="center", zorder=12)


# ══════════════════════ C-A34-01 蘇菲是誰 ══════════════════════
EV = [(-0.72, "e903", "e903b", WHITE), (-0.24, "ecourt", "ecourtb", GREY),
      (0.24, "e964", "e964b", AMBER), (0.72, "e986", "e986b", WHITE)]


def c01_life(ax):
    T(ax, 0.0, 0.80, tx("c01_title"), 34, WHITE)
    T(ax, 0.0, 0.70, tx("c01_sub"), 18, GREY, w="normal")
    y = 0.28
    ax.plot([-0.86, 0.86], [y, y], c=WHITE, lw=2.0, alpha=.5)
    for x, a, b, col in EV:
        ax.scatter([x], [y], s=260 if col == AMBER else 160, c=col, zorder=5, lw=0)
        T(ax, x, y + 0.10, tx(a), 24, col)
        ax.text(x, y - 0.15, tx(b), fontproperties=C.FP, fontsize=15, color=WHITE, ha="center", va="center",
                linespacing=1.35, alpha=.9, zorder=12)
    T(ax, 0.0, -0.05, tx("persian"), 17, GREY, w="normal")


def c01_book(ax):
    ax.add_patch(C.FancyBboxPatch((-0.78, -0.80), 1.56, 0.62, boxstyle="round,pad=0.0,rounding_size=0.04",
                                  fc="#141B33", ec=AMBER, lw=1.6, zorder=3))
    AR(ax, 0.0, -0.30, AR_BOOK, 30, AMBER)
    T(ax, 0.0, -0.45, tx("book_tr"), 16, GREY, w="normal")
    T(ax, 0.0, -0.58, tx("book_zh"), 26, WHITE)
    T(ax, 0.0, -0.71, tx("age"), 16, AMBER, w="normal")


# ══════════════════════ C-A34-02 托勒密 → 蘇菲 ══════════════════════
# 示意星點：(x, y, 托勒密給的大小, 蘇菲改過的大小)；None＝托勒密星表裡沒有
DOTS = [(-0.20, 0.30, 3, 3), (0.05, 0.42, 2, 2), (0.22, 0.22, 4, 2), (-0.05, 0.08, 3, 3),
        (0.30, -0.05, 2, 4), (-0.25, -0.10, 4, 4), (0.08, -0.25, None, 5)]
RAD = {1: 0.040, 2: 0.031, 3: 0.023, 4: 0.016, 5: 0.011}


def c02_table(ax):
    T(ax, 0.0, 0.86, tx("c02_title"), 32, WHITE)
    T(ax, 0.0, 0.77, tx("c02_sub"), 16, GREY, w="normal")
    ax.add_patch(C.FancyBboxPatch((-0.92, -0.45), 0.86, 1.08, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#141B33", ec=GREY, lw=1.2, zorder=2))
    T(ax, -0.49, 0.55, tx("ptol"), 19, WHITE)
    T(ax, -0.49, 0.48, tx("ptol2"), 12.5, GREY, w="normal")
    for x, y, a, b in DOTS:
        if a:
            ax.add_patch(C.Circle((x - 0.49, y - 0.05), RAD[a], fc=WHITE, ec="none", zorder=4))


def c02_check(ax):
    ax.add_patch(C.FancyBboxPatch((0.06, -0.45), 0.86, 1.08, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#141B33", ec=AMBER, lw=1.4, zorder=2))
    T(ax, 0.49, 0.55, tx("sufi"), 19, AMBER)
    T(ax, 0.49, 0.48, tx("sufi2"), 12.5, GREY, w="normal")
    C.arrow(ax, (0.04, 0.10), (-0.04, 0.10), c=AMBER, lw=2.4, alpha=.9, style="-|>")
    for x, y, a, b in DOTS:
        X, Y = x + 0.49, y - 0.05
        ax.add_patch(C.Circle((X, Y), RAD[b], fc=WHITE, ec="none", zorder=4))
        if a is None:
            ax.add_patch(C.Circle((X, Y), 0.045, fc="none", ec=GREEN, lw=2.0, zorder=5))
        elif a != b:
            ax.add_patch(C.Circle((X, Y), 0.06, fc="none", ec=AMBER, lw=2.0, zorder=5))
    ax.add_patch(C.Circle((-0.70, -0.60), 0.035, fc="none", ec=AMBER, lw=2.0))
    T(ax, -0.62, -0.60, tx("fix"), 17, AMBER, ha="left")
    ax.add_patch(C.Circle((-0.70, -0.72), 0.035, fc="none", ec=GREEN, lw=2.0))
    T(ax, -0.62, -0.72, tx("miss"), 17, GREEN, ha="left")


# ══════════════════════ C-A34-03 歲差 ══════════════════════
SC3 = 0.026          # 每 1° 黃經的圖上長度（東在左：黃經增加＝往左）
PTS3 = [(14, 0.10, 0.020), (6, -0.06, 0.026), (-2, 0.05, 0.016), (-10, -0.09, 0.022),
        (-17, 0.03, 0.030), (-24, 0.12, 0.014)]          # (相對黃經°, 黃緯示意 y, 半徑)
SHIFT = 12 + 42 / 60


def c03_ecl(ax):
    T(ax, 0.0, 0.80, tx("c03_title"), 26, WHITE)
    T(ax, 0.0, 0.71, tx("c03_sub"), 15, GREY, w="normal")
    ax.plot([-0.95, 0.95], [0, 0], c=AMBER, lw=1.6, alpha=.6, ls=(0, (6, 4)))
    T(ax, 0.86, 0.05, tx("ecl"), 15, AMBER, w="normal")
    for d in range(-36, 37, 6):
        x = -d * SC3
        ax.plot([x, x], [-0.025, 0.025], c=AMBER, lw=1.0, alpha=.5)
    T(ax, -0.62, -0.30, tx("east"), 15, GREY, w="normal")
    for L, y, r in PTS3:
        ax.add_patch(C.Circle((-L * SC3 + 0.16, y), r, fc=WHITE, ec="none", alpha=.45, zorder=4))
    T(ax, 0.30, 0.36, tx("p137"), 17, WHITE, w="normal")


def c03_shift(ax):
    for L, y, r in PTS3:
        x0, x1 = -L * SC3 + 0.16, -(L + SHIFT) * SC3 + 0.16
        ax.add_patch(C.Circle((x1, y), r, fc=AMBER, ec="none", zorder=5))
    yA = -0.20
    C.arrow(ax, (0.16 - SHIFT * SC3, yA), (0.16, yA), c=AMBER, lw=2.6, alpha=.95, style="-|>")
    T(ax, 0.16 - SHIFT * SC3 / 2, yA - 0.07, tx("shift"), 22, AMBER)
    T(ax, -0.40, 0.36, tx("p964"), 17, AMBER)


# ══════════════════════ C-A34-03b 蘇菲的尺 ══════════════════════
U3 = 0.085            # 每 1° 的圖上長度


def c03b_units(ax):
    T(ax, 0.0, 0.86, tx("c03b_title"), 32, WHITE)
    T(ax, 0.0, 0.78, tx("c03b_sub"), 16, GREY, w="normal")
    x0 = -0.42
    rows = [(0.62, 0.5, "moon", GREY, 2.0), (0.50, 7 / 3, "cubit", AMBER, 6.0), (0.38, 14.0, "spear", BLUE, 3.0)]
    for y, deg, key, col, lw in rows:
        ax.plot([x0, x0 + deg * U3], [y, y], c=col, lw=lw, solid_capstyle="butt")
        ax.plot([x0, x0], [y - 0.02, y + 0.02], c=col, lw=1.4)
        ax.plot([x0 + deg * U3] * 2, [y - 0.02, y + 0.02], c=col, lw=1.4)
        T(ax, x0 - 0.03, y, tx(key), 15, col, ha="right")
    for i in range(1, 6):
        x = x0 + i * 7 / 3 * U3
        ax.plot([x, x], [0.37, 0.39], c=BLUE, lw=1.2, alpha=.8)
    T(ax, 0.0, 0.28, tx("others"), 14, GREY, w="normal")


def _aql_xy():
    """天鷹座：以 HIP 97278／93747 一帶為中心的切面投影（東在左、北在上）"""
    ra0, de0 = 292.0, 6.0
    def p(ra, dec):
        a, d, a0, d0 = map(math.radians, (ra, dec, ra0, de0))
        cc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
        x = math.cos(d) * math.sin(a - a0) / cc
        y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / cc
        return -math.degrees(x) * 0.030, math.degrees(y) * 0.030 - 0.35
    return p


def c03b_mw(ax):
    p = _aql_xy()
    # 銀河：銀緯 ±9°（外）、±4°（內）兩層半透明帶；畫面外的部分由座標軸裁掉
    def edge(b):
        return [p(*G.gal2eq(l, b)) for l in range(-10, 100)]
    for bw, al in ((9, .07), (4, .07)):
        up, dn = edge(bw), edge(-bw)
        poly = up + dn[::-1]
        clip = C.Rectangle((-0.95, -0.95), 1.9, 1.13, transform=ax.transData)
        for pt in ax.fill([q[0] for q in poly], [q[1] for q in poly], c=MW, alpha=al, lw=0, zorder=1):
            pt.set_clip_path(clip)                 # 只在下半（天鷹座那一區），不壓到上面的比例尺
    T(ax, -0.36, -0.66, tx("mw"), 16, MW, w="normal")
    d = json.load(open(os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures/arabic_al-sufi/"
                                          "index.json"), encoding="utf-8"))
    segs = next(c["lines"] for c in d["constellations"] if c["id"].endswith(" Aql"))
    for l in segs:
        pts = [p(*S[h][:2]) for h in l if h in S]
        ax.plot([q[0] for q in pts], [q[1] for q in pts], c=AMBER, lw=2.0, alpha=.9, zorder=3)
    for h in {h for l in segs for h in l if h in S}:
        x, y = p(*S[h][:2])
        r = max(0.006, (6.5 - S[h][2]) ** 1.7 * 0.0022)
        ax.add_patch(C.Circle((x, y), r, fc=WHITE, ec="none", zorder=4))
    x, y = p(*S[93747][:2])
    ax.add_patch(C.Circle((x, y), 0.05, fc="none", ec=GREEN, lw=2.4, zorder=5))
    T(ax, x + 0.08, y + 0.10, tx("touch"), 18, GREEN, ha="left")
    AR(ax, x + 0.30, y + 0.02, AR_TOUCH, 20, GREEN)
    T(ax, 0.0, -0.88, tx("touch2"), 13, GREY, w="normal")
    T(ax, 0.55, 0.12, tx("aql"), 13, AMBER, w="normal")


# ══════════════════════ C-A34-04 天空與天球儀 ══════════════════════
def _and_proj(mirror=False):
    ra0, de0 = 13.0, 35.0
    def p(ra, dec):
        a, d, a0, d0 = map(math.radians, (ra, dec, ra0, de0))
        cc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
        x = math.cos(d) * math.sin(a - a0) / cc
        y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / cc
        x = -math.degrees(x) * 0.0145
        return (-x if mirror else x), math.degrees(y) * 0.0145
    return p


def _draw_and(ax, cx, mirror, title, e_left):
    d = json.load(open(os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures/arabic_al-sufi/"
                                          "index.json"), encoding="utf-8"))
    get = lambda k: next(c["lines"] for c in d["constellations"] if c["id"].endswith(" " + k))
    p = _and_proj(mirror)
    ax.add_patch(C.FancyBboxPatch((cx - 0.44, -0.62), 0.88, 1.22, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#141B33", ec=GREY, lw=1.0, zorder=1))
    stars = set()
    for key, col, lw in (("And", AMBER, 1.8), ("SFA", GREEN, 2.4)):
        for l in get(key):
            pts = [p(*S[h][:2]) for h in l if h in S]
            stars |= {h for h in l if h in S}
            ax.plot([cx + q[0] for q in pts], [q[1] for q in pts], c=col, lw=lw, alpha=.9, zorder=3)
    for h in stars:
        x, y = p(*S[h][:2])
        ax.add_patch(C.Circle((cx + x, y), max(0.005, (6.5 - S[h][2]) ** 1.7 * 0.0016), fc=WHITE, ec="none",
                              zorder=4))
    ax.text(cx, 0.48, title, fontproperties=C.FP, fontsize=17, color=WHITE, ha="center", va="center",
            linespacing=1.3, weight="bold", zorder=12)
    T(ax, cx - 0.36, -0.55, tx("e") if e_left else tx("w"), 15, GREY, w="normal")
    T(ax, cx + 0.36, -0.55, tx("w") if e_left else tx("e"), 15, GREY, w="normal")


def c04_sky(ax):
    T(ax, 0.0, 0.86, tx("c04_title"), 32, WHITE)
    T(ax, 0.0, 0.77, tx("c04_sub"), 16, GREY, w="normal")
    _draw_and(ax, -0.47, False, tx("sky"), True)


def c04_globe(ax):
    _draw_and(ax, 0.47, True, tx("globe"), False)
    C.arrow(ax, (0.07, -0.72), (-0.07, -0.72), c=AMBER, lw=2.0, alpha=.9, style="<|-|>")
    T(ax, 0.0, -0.81, tx("mirror"), 20, AMBER)


# ══════════════════════ C-A34-05 9:16 圖卡 ══════════════════════
def c05_card(ax):
    ax.text(0.5, 0.905, tx("c05_title"), fontproperties=C.FP, fontsize=27, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.865, tx("c05_date"), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center")
    rows = [("r1t", "r1a", "r1b", "r1c", AMBER), (None, "r2a", "r2b", "r2c", BLUE),
            (None, "r3a", "r3b", "r3c", GREEN), ("r4t", "r4a", "r4b", "r4c", GREEN),
            ("r5t", "r5a", "r5b", "r5c", WHITE)]
    y = 0.80
    for t, a, b, c, col in rows:
        if t:
            ax.plot([0.06, 0.94], [y + 0.012, y + 0.012], c=WHITE, lw=0.8, alpha=.3)
            ax.text(0.06, y - 0.018, tx(t), fontproperties=C.FP, fontsize=16, color=AMBER, ha="left",
                    va="center", weight="bold")
            y -= 0.050
        ax.text(0.08, y, tx(a), fontproperties=C.FP, fontsize=19, color=col, ha="left", va="center", weight="bold")
        ax.text(0.40, y, tx(b), fontproperties=C.FP, fontsize=14, color=WHITE, ha="left", va="center")
        ax.text(0.08, y - 0.034, tx(c), fontproperties=C.FP, fontsize=12, color=GREY, ha="left", va="center")
        y -= 0.088
    ax.plot([0.06, 0.94], [y + 0.03, y + 0.03], c=WHITE, lw=0.8, alpha=.3)
    ax.text(0.5, y - 0.005, tx("moon_note"), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center",
            va="center", weight="bold")
    ax.text(0.5, y - 0.045, tx("dark"), fontproperties=C.FP, fontsize=14, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.075, tx("src"), fontproperties=C.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.045, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


def run_all():
    C.emit("", [("生平", c01_life), ("書名", c01_book)], title="C-A34-01_蘇菲是誰")
    C.emit("", [("星表", c02_table), ("核對", c02_check)], title="C-A34-02_托勒密到蘇菲")
    C.emit("", [("黃道", c03_ecl), ("平移", c03_shift)], title="C-A34-03_歲差")
    C.emit("", [("單位", c03b_units), ("銀河", c03b_mw)], title="C-A34-03b_蘇菲的尺")
    C.emit("", [("天空", c04_sky), ("天球儀", c04_globe)], title="C-A34-04_天空與天球儀")
    f, ax = C.newcard(dark=True)
    c05_card(ax)
    C.save(f, "", "C-A34-05_用蘇菲的眼睛看天_圖卡.png", transparent=False)


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:                      # 英文版寫到 _概念圖/en/
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    run_all()


if __name__ == "__main__":
    main()
