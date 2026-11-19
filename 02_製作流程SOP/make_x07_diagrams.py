# -*- coding: utf-8 -*-
"""X-07 銀河環球｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-X07-01_箕斗之間      → 04 鏡迄格（中國層 → 阿拉伯層 → 疊合層）
  C-X07-02_銀河的名字    → 10 鏡迄格（9:16 圖卡，可存圖）
  C-X07-03_我們在盤子裡  → 11 鏡迄格（側視層 → 視線層）
  C-X07-04_這幾晚看銀心  → 12 鏡迄格（9:16 圖卡，可存圖）
輸出：05_素材/X-07_銀河環球/_概念圖/（--lang en → _概念圖/en/）

來源：逐字稿 v1 星名表與考據備忘；箕斗星位＝03_星點座標表（Hipparcos J2000）心射投影、東在左；銀道面＝IAU 銀道座標換算；
  銀心 Sgr A* J2000；銀河系數字（直徑約 10 萬光年、太陽距銀心約 2.7 萬光年〔GRAVITY 2019、2021〕、恆星幾千億顆）；
  天象 PyEphem 4.2.1（台北 25.033°N、121.565°E，含折射；條件＝太陽 < −18°、月亮在地平線下、銀心高 > 20°，逐 5 分鐘掃描）。
  側視圖是示意（厚度、旋臂不按比例），不臨摹已出版的銀河系圖。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-07_銀河環球/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#8A97B4"
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "箕斗之間，漢津也", "c01_src": "《爾雅・釋天》",
        "ji": "箕宿", "dou": "斗宿", "river": "銀河", "ford": "漢津（渡口）",
        "dou_note": "斗宿二、三不在鴕鳥裡",
        "ost_in": "下河喝水的鴕鳥", "ost_in2": "al-Naʿām al-wārid",
        "ost_out": "喝飽離開的鴕鳥", "ost_out2": "al-Naʿām al-ṣādir",
        "ar_src": "古阿拉伯（Stellarium arabic_ancient，al-Ajaji）",
        "c01_mid1": "同樣這八顆星：", "c01_mid2": "中國人的渡口，就在兩群鴕鳥中間",
        "c01_foot": "星位照實際天空（東在左）；鴕鳥是示意",
        "c02_title": "銀河的名字", "c02_sub": "同一條光帶，各地看見的東西",
        "c02_groups": [
            ("河", BLUE, [("中國", "天河・河漢", "天上的漢水"),
                          ("古阿拉伯", "al-Naʿām", "鴕鳥下去喝水的河"),
                          ("阿拉斯加 Nunamiut", "", "一條河")]),
            ("路", AMBER, [("黑腳族", "Wolf Trail", "狼之路：亡靈走的路"),
                           ("瓜拉尼", "Tapi'i rapé", "貘之路"),
                           ("洛科諾", "Waya nukuthi bunaha", "挖陶土的人的腳印"),
                           ("科伊桑", "", "星星的路"),
                           ("薩米", "Lodde-raiddaras", "鳥之路"),
                           ("俄語（西伯利亞）", "", "鵝之路・馬麥之路"),
                           ("芬蘭", "Linnunrata", "鳥的路"),
                           ("尤皮克（白令海峽）", "Tanglurallret", "烏鴉的雪鞋腳印")]),
            ("縫・線", PURPLE, [("蒙古", "Тэнгэрийн заадас", "天空的縫線"),
                               ("因紐特（Igloolik）", "Aviguti", "分隔線：風的分界"),
                               ("西格陵蘭", "Qilaup sivdlin", "天空的剖線"),
                               ("拉布拉多", "kopput", "條紋")]),
            ("活的東西", GREEN, [("毛利", "Te Ikaroa", "長魚"),
                                ("曼達爾／布吉斯", "Bittoéng Naga", "龍"),
                                ("科薩", "umNyele", "怒犬背上豎起的鬃毛"),
                                ("馬雅", "", "半鱷半鹿的神獸"),
                                ("卡米拉羅伊", "", "暗帶裡的鴯鶓")]),
            ("灰", "#D9D9D9", [("ǀXam（南非）", "", "女孩撒上天的柴火灰"),
                              ("萬那杜 Netwar", "Nemrau", "灰")]),
            ("其他", GREY, [("祖魯", "Umthala Wezinkanyezi", "星星的溪流（意象是長矛）"),
                           ("納瓦荷", "Yikáísdáhí", "等待黎明的"),
                           ("英語", "Milky Way", "奶的路")]),
        ],
        "c02_foot": "萬國星空 EP47｜X-07 銀河環球　可存圖",
        "c03_title": "我們在盤子裡", "c03_sub": "銀河系側視示意（厚度不按比例）",
        "dia": "直徑約 10 萬光年", "gc": "銀河中心", "sun": "太陽（我們）", "dist": "約 2.7 萬光年",
        "stars": "幾千億顆星",
        "c03_l1": "沿著盤面看：", "c03_l1b": "星一層疊一層＝一條河",
        "c03_l2": "往盤外看：星稀稀落落",
        "c03_l3": "夏夜正對盤心（人馬座）",
        "c04_title": "這幾晚看銀河中心", "c04_sub": "台北・往東南到南方看",
        "c04_sun": "7/2 日落 18:47　天全黑 20:16　7/4 新月",
        "c04_rows": [
            ("7/2 21:00・東南偏南", "銀河中心 {a21}°", "方位 {z21}°；在人馬座「茶壺」壺嘴上方", AMBER),
            ("22:59・正南", "最高 {a23}°", "台北最高就這麼高——南方要開闊", AMBER),
            ("01:00・西南偏南", "還有 {a01}°", "方位 {z01}°；兩點以後太低", AMBER),
        ],
        "c04_tbl": "月亮不在天上、天全黑、銀心高於 20°",
        "c04_win": [("7/1–7/5", "20:20–約 02:00", "最好（7/4 新月）"),
                    ("7/6", "20:45–01:45", "月落後"),
                    ("7/7", "21:25–01:40", "月落後")],
        "c04_city": "城市裡看不到銀河，要到遠離燈光的地方",
        "c04_foot": "PyEphem 計算，含大氣折射；銀心＝Sgr A*",
        "tags": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Between the Basket and the Dipper lies the Ford of the Han", "c01_src": "Erya, Shitian",
        "ji": "Winnowing Basket", "dou": "Dipper", "river": "Milky Way", "ford": "Ford of the Han",
        "dou_note": "λ, μ Sgr are not ostriches",
        "ost_in": "ostriches going down to drink", "ost_in2": "al-Naʿām al-wārid",
        "ost_out": "ostriches leaving, thirst quenched", "ost_out2": "al-Naʿām al-ṣādir",
        "ar_src": "Ancient Arabic (Stellarium arabic_ancient, al-Ajaji)",
        "c01_mid1": "The same eight stars:", "c01_mid2": "the Chinese ford sits between the two flocks",
        "c01_foot": "Star positions as in the sky (east left); ostriches schematic",
        "c02_title": "Names of the Milky Way", "c02_sub": "one band of light, many things seen",
        "c02_groups": [
            ("River", BLUE, [("China", "Tianhe, Hehan", "the Han river in the sky"),
                             ("Ancient Arabic", "al-Naʿām", "river the ostriches drink from"),
                             ("Nunamiut, Alaska", "", "a river")]),
            ("Road", AMBER, [("Blackfoot", "Wolf Trail", "path of the dead"),
                             ("Guarani", "Tapi'i rapé", "path of the tapir"),
                             ("Lokono", "Waya nukuthi bunaha", "footprints of the clay carriers"),
                             ("Khoisan", "", "the stars' road"),
                             ("Sámi", "Lodde-raiddaras", "bird path"),
                             ("Russian (Siberia)", "", "Goose Road, Mamay Road"),
                             ("Finnish", "Linnunrata", "path of the birds"),
                             ("Yupik (Bering Strait)", "Tanglurallret", "Raven's snowshoe track")]),
            ("Seam", PURPLE, [("Mongolian", "Тэнгэрийн заадас", "seam of the sky"),
                              ("Inuit (Igloolik)", "Aviguti", "the divider of winds"),
                              ("West Greenland", "Qilaup sivdlin", "the sky's cut line"),
                              ("Labrador", "kopput", "stripe")]),
            ("Living thing", GREEN, [("Māori", "Te Ikaroa", "the long fish"),
                                     ("Mandar / Bugis", "Bittoéng Naga", "dragon"),
                                     ("Xhosa", "umNyele", "bristled hair of an angry dog"),
                                     ("Maya", "", "crocodile-deer creature"),
                                     ("Kamilaroi", "", "the emu in the dark lanes")]),
            ("Ash", "#D9D9D9", [("ǀXam (South Africa)", "", "a girl's wood ashes thrown up"),
                                ("Netwar, Vanuatu", "Nemrau", "ash")]),
            ("Other", GREY, [("Zulu", "Umthala Wezinkanyezi", "stream of stars (thrown spears)"),
                             ("Navajo", "Yikáísdáhí", "Awaits the Dawn"),
                             ("English", "Milky Way", "the milk road")]),
        ],
        "c02_foot": "World Sky Cultures EP47 | save this card",
        "c03_title": "We live inside the disc", "c03_sub": "Milky Way side view, schematic (thickness not to scale)",
        "dia": "about 100,000 light-years across", "gc": "Galactic Centre", "sun": "Sun (us)",
        "dist": "about 27,000 ly", "stars": "hundreds of billions of stars",
        "c03_l1": "Along the disc:", "c03_l1b": "stars pile up into a river",
        "c03_l2": "Out of the disc: sparse stars",
        "c03_l3": "Summer nights face the centre (Sagittarius)",
        "c04_title": "See the Galactic Centre", "c04_sub": "Taipei, look SE to S",
        "c04_sun": "2 Jul sunset 18:47  full dark 20:16  new moon 4 Jul",
        "c04_rows": [
            ("2 Jul 21:00, SSE", "Galactic Centre {a21}°", "azimuth {z21}°; above the Teapot", AMBER),
            ("22:59, due south", "highest {a23}°", "that's as high as it gets in Taipei", AMBER),
            ("01:00, SSW", "still {a01}°", "azimuth {z01}°; too low after 2 am", AMBER),
        ],
        "c04_tbl": "No Moon, full dark, centre above 20°",
        "c04_win": [("1–5 Jul", "20:20 – c. 02:00", "best (new moon 4 Jul)"),
                    ("6 Jul", "20:45 – 01:45", "after moonset"),
                    ("7 Jul", "21:25 – 01:40", "after moonset")],
        "c04_city": "Not visible from the city: find a dark site",
        "c04_foot": "PyEphem, with refraction; centre = Sgr A*",
        "tags": "#WorldSkyCultures",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ C-X07-01 箕斗之間 ══════════════════════
S = dict(G.load_stars(BASE))
JI = [88635, 89931, 90185, 89642]              # γ² δ ε η Sgr
DOU = [89341, 90496, 92041, 92855, 93864, 93506]
OST_OUT = [92041, 92855, 93864, 93506]         # φ σ τ ζ＝斗宿一四五六
RA0, DE0 = 279.5, -28.5
SC = 0.060                                     # 每度多少圖單位
OX, OY = 0.0, 0.0


def proj(ra, dec):
    """心射投影，東在左（天空樣子）"""
    a, d, a0, d0 = map(math.radians, (ra, dec, RA0, DE0))
    cc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / cc
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / cc
    return -math.degrees(x) * SC + OX, math.degrees(y) * SC + OY


def _center():
    """十顆星的外框置中在 (−0.05, 0.08)"""
    global OX, OY
    pts = [proj(*S[h][:2]) for h in JI + DOU]
    OX = -0.05 - (max(p[0] for p in pts) + min(p[0] for p in pts)) / 2
    OY = 0.08 - (max(p[1] for p in pts) + min(p[1] for p in pts)) / 2


_center()


def P(h):
    return proj(*S[h][:2])


def ssize(h):
    return max(0.05, 6.5 - S[h][2]) ** 1.7 * 22


def chain(ax, hs, col, lw=2.4, alpha=.9, close=False):
    pts = [P(h) for h in hs] + ([P(hs[0])] if close else [])
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=lw, alpha=alpha, zorder=4)


def river(ax):
    """銀道面附近 b −7…+9 的帶（示意亮帶）"""
    for b0, b1, al in ((-7, 9, .10), (-4, 6, .12), (-1, 4, .14)):
        up = [proj(*G.gal2eq(l, b1)) for l in range(-30, 31)]
        lo = [proj(*G.gal2eq(l, b0)) for l in range(30, -31, -1)]
        ax.add_patch(C.Polygon(up + lo, closed=True, fc=MW, ec="none", alpha=al, zorder=1))


def c01_cn(ax):
    T(ax, 0.0, 0.90, tx("c01_title"), 30 if LANG == "zh" else 20, AMBER)
    T(ax, 0.0, 0.83, tx("c01_src"), 15, GREY, w="normal")
    ax.add_patch(C.Rectangle((-0.95, -0.62), 1.9, 1.36, fc="none", ec="none"))
    import matplotlib.path as mp
    clip = C.Rectangle((-0.95, -0.66), 1.9, 1.40, transform=ax.transData, fc="none", ec="none")
    n0 = len(ax.patches)
    river(ax)
    for p in ax.patches[n0:]:
        p.set_clip_path(clip)
    rx, ry = proj(*G.gal2eq(18, 4))
    T(ax, rx, ry, tx("river"), 16, MW, w="normal", alpha=.9)
    chain(ax, JI, AMBER, close=True)
    chain(ax, DOU, AMBER)
    for h in JI + DOU:
        x, y = P(h)
        ax.scatter([x], [y], s=ssize(h), c=WHITE, zorder=6, lw=0)
    jx = max(P(h)[0] for h in JI); jy = sum(P(h)[1] for h in JI) / 4
    T(ax, jx + 0.06, jy, tx("ji"), 20, AMBER, ha="left")
    dx_ = min(P(h)[0] for h in DOU); dy_ = max(P(h)[1] for h in DOU)
    T(ax, dx_ - 0.02, dy_ + 0.07, tx("dou"), 20, AMBER, ha="left")
    fx, fy = [(a + b) / 2 for a, b in zip(P(90185), P(92041))]
    ax.scatter([fx], [fy], s=320, facecolors="none", edgecolors=AMBER, lw=2.0, zorder=7, ls=(0, (3, 2)))
    T(ax, fx, fy - 0.075, tx("ford"), 17, AMBER)


def c01_ar(ax):
    chain(ax, JI, GREEN, lw=3.2, alpha=.85, close=True)
    chain(ax, OST_OUT, GREEN, lw=3.2, alpha=.85, close=True)
    for h in DOU:
        if h not in OST_OUT:
            x, y = P(h)
            ax.scatter([x], [y], s=ssize(h) * 2.6, facecolors="none", edgecolors=GREY, lw=1.0, zorder=7, alpha=.8)
    lx, ly = P(89341)
    T(ax, lx + 0.02, ly + 0.07, tx("dou_note"), 12, GREY, w="normal")
    # 方向箭頭：下河（往銀河中心那側）、離開（往外）
    jx = sum(P(h)[0] for h in JI) / 4; jy = sum(P(h)[1] for h in JI) / 4
    ox = sum(P(h)[0] for h in OST_OUT) / 4; oy = sum(P(h)[1] for h in OST_OUT) / 4
    jb = min(P(h)[1] for h in JI)
    jr = max(P(h)[0] for h in JI)
    C.arrow(ax, (jr + 0.24, jy - 0.06), (jr + 0.04, jy - 0.12), c=GREEN, lw=2.6, alpha=.95, style="-|>")   # 往銀河（西＝右）下河
    ol = min(P(h)[0] for h in OST_OUT); oly = [P(h)[1] for h in OST_OUT if P(h)[0] == ol][0]
    C.arrow(ax, (ol - 0.22, oly + 0.02), (ol - 0.04, oly), c=GREEN, lw=2.6, alpha=.95, style="-|>")   # 往東（左）離開
    T(ax, jx, jb - 0.08, tx("ost_in"), 17, GREEN)
    T(ax, jx, jb - 0.14, tx("ost_in2"), 13, GREEN, w="normal")
    T(ax, ox - 0.10, oy - 0.20, tx("ost_out"), 17, GREEN)
    T(ax, ox - 0.10, oy - 0.26, tx("ost_out2"), 13, GREEN, w="normal")
    T(ax, 0.0, -0.66, tx("ar_src"), 12, GREY, w="normal")


def c01_mix(ax):
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.95), 1.76, 0.21, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.4, zorder=9))
    T(ax, 0.0, -0.79, tx("c01_mid1"), 15, WHITE, w="normal", z=13)
    T(ax, 0.0, -0.87, tx("c01_mid2"), 21 if LANG == "zh" else 16, AMBER, z=13)
    T(ax, 0.0, -0.715, "", 1)
    T(ax, 0.62, 0.76, tx("c01_foot"), 10.5, GREY, w="normal", ha="center")


# ══════════════════════ C-X07-03 我們在盤子裡 ══════════════════════
R_D = 0.86           # 半徑 5 萬光年
SUN_X = -R_D * 26.8 / 50.0


def c03_side(ax):
    import numpy as np
    T(ax, 0.0, 0.90, tx("c03_title"), 32, WHITE)
    T(ax, 0.0, 0.835, tx("c03_sub"), 14, GREY, w="normal")
    rng = np.random.default_rng(7)
    n = 9000
    r = np.abs(rng.normal(0, 0.42, n)) % R_D
    x = r * rng.choice([-1, 1], n)
    y = rng.normal(0, 0.020 + 0.015 * (1 - np.abs(x) / R_D), n)
    ax.scatter(x, y, s=1.4, c=MW, alpha=.45, lw=0, zorder=2)
    b = rng.normal(0, 0.06, (1500, 2))
    ax.scatter(b[:, 0] * 1.4, b[:, 1], s=1.8, c="#FFE8B0", alpha=.55, lw=0, zorder=3)
    ax.add_patch(C.Ellipse((0, 0), 2 * R_D, 0.12, fc="none", ec=MW, lw=1.0, alpha=.35, zorder=2))
    ax.annotate("", xy=(R_D, -0.30), xytext=(-R_D, -0.30),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4))
    T(ax, 0.0, -0.35, tx("dia"), 15, GREY, w="normal")
    ax.scatter([0], [0], s=90, c=AMBER, zorder=6, marker="+", lw=2)
    T(ax, 0.0, 0.17, tx("gc"), 16, AMBER)
    ax.plot([0, 0], [0.04, 0.13], c=AMBER, lw=1.0, alpha=.7)
    ax.scatter([SUN_X], [0.012], s=140, c=AMBER, zorder=8, lw=0)
    ax.scatter([SUN_X], [0.012], s=520, c=AMBER, zorder=7, lw=0, alpha=.22)
    T(ax, SUN_X - 0.05, -0.075, tx("sun"), 16, AMBER, ha="right")
    ax.annotate("", xy=(-0.02, -0.15), xytext=(SUN_X, -0.15),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.4, alpha=.8))
    T(ax, SUN_X / 2, -0.20, tx("dist"), 15, AMBER, w="normal")
    T(ax, 0.55, 0.12, tx("stars"), 14, WHITE, w="normal", alpha=.85)


def c03_sight(ax):
    sy = 0.012
    for x1, al in ((0.80, .95), (-0.95, .75)):
        ax.annotate("", xy=(x1, sy), xytext=(SUN_X + (0.04 if x1 > 0 else -0.04), sy),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=3.0, alpha=al), zorder=9)
    for ang in (60, 90, 120):
        a = math.radians(ang)
        ax.annotate("", xy=(SUN_X + 0.42 * math.cos(a), sy + 0.42 * math.sin(a)), xytext=(SUN_X, sy + 0.03),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6, alpha=.7, ls=(0, (3, 3))), zorder=9)
    T(ax, SUN_X, 0.53, tx("c03_l2"), 15, GREY, w="normal")
    by = -0.62
    ax.add_patch(C.FancyBboxPatch((-0.88, by - 0.17), 1.76, 0.30, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#1B2240", ec=BLUE, lw=1.4, zorder=9))
    T(ax, 0.0, by + 0.06, tx("c03_l1"), 16, WHITE, w="normal", z=13)
    T(ax, 0.0, by - 0.03, tx("c03_l1b"), 22 if LANG == "zh" else 17, BLUE, z=13)
    T(ax, 0.0, by - 0.115, tx("c03_l3"), 13, AMBER, w="normal", z=13)


# ══════════════════════ 9:16 圖卡 ══════════════════════
def c02_card(ax):
    ax.text(0.5, 0.955, tx("c02_title"), fontproperties=C.FP, fontsize=28, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.922, tx("c02_sub"), fontproperties=C.FP, fontsize=13, color=GREY, ha="center", va="center")
    y = 0.895
    LH = 0.0218
    for head, col, rows in tx("c02_groups"):
        hh = 0.038 + LH * len(rows)
        ax.add_patch(C.FancyBboxPatch((0.04, y - hh), 0.92, hh - 0.007, boxstyle="round,pad=0.0,rounding_size=0.015",
                                      fc="#141B36", ec=col, lw=1.4, zorder=2))
        ax.text(0.07, y - 0.021, head, fontproperties=C.FP, fontsize=16, color=col, ha="left", va="center",
                weight="bold", zorder=3)
        for i, (who, orig, mean) in enumerate(rows):
            yy = y - 0.046 - LH * i
            ax.text(0.07, yy, who, fontproperties=C.FP, fontsize=10, color=GREY, ha="left", va="center", zorder=3)
            ax.text(0.33, yy, mean, fontproperties=C.FP, fontsize=11, color=WHITE, ha="left", va="center",
                    weight="bold", zorder=3)
            if orig:                                   # 原文同一行、靠右（上下兩行會疊字）
                ax.text(0.935, yy, orig, fontproperties=C.FP, fontsize=8.5, color=col, ha="right",
                        va="center", alpha=.95, zorder=3)
        y -= hh + 0.004
    ax.text(0.5, 0.050, tx("c02_foot"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.024, tx("tags"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")
    return y


def c04_card(ax, nums):
    ax.text(0.5, 0.945, tx("c04_title"), fontproperties=C.FP, fontsize=27, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, tx("c04_sub"), fontproperties=C.FP, fontsize=16, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.872, tx("c04_sun"), fontproperties=C.FP, fontsize=12, color=GREY, ha="center", va="center")
    y = 0.842
    for when, what, detail, col in tx("c04_rows"):
        hh = 0.135
        ax.add_patch(C.FancyBboxPatch((0.05, y - hh), 0.90, hh - 0.012, boxstyle="round,pad=0.0,rounding_size=0.02",
                                      fc="#141B36", ec=col, lw=1.5, zorder=2))
        ax.text(0.09, y - 0.030, when, fontproperties=C.FP, fontsize=13, color=col, ha="left", va="center",
                weight="bold", zorder=3)
        ax.text(0.09, y - 0.068, what.format(**nums), fontproperties=C.FP, fontsize=20, color=WHITE, ha="left",
                va="center", weight="bold", zorder=3)
        ax.text(0.09, y - 0.103, detail.format(**nums), fontproperties=C.FP, fontsize=11.5, color=WHITE, ha="left",
                va="center", alpha=.85, zorder=3)
        y -= hh + 0.006
    y -= 0.010
    hh = 0.205
    ax.add_patch(C.FancyBboxPatch((0.05, y - hh), 0.90, hh, boxstyle="round,pad=0.0,rounding_size=0.02",
                                  fc="#141B36", ec=GREEN, lw=1.5, zorder=2))
    ax.text(0.09, y - 0.032, tx("c04_tbl"), fontproperties=C.FP, fontsize=13, color=GREEN, ha="left", va="center",
            weight="bold", zorder=3)
    for i, (d, t, n) in enumerate(tx("c04_win")):
        yy = y - 0.078 - 0.042 * i
        ax.text(0.09, yy, d, fontproperties=C.FP, fontsize=15, color=WHITE, ha="left", va="center", weight="bold", zorder=3)
        ax.text(0.33, yy, t, fontproperties=C.FP, fontsize=15, color=WHITE, ha="left", va="center", zorder=3)
        ax.text(0.66, yy, n, fontproperties=C.FP, fontsize=11, color=GREY, ha="left", va="center", zorder=3)
    y -= hh + 0.030
    ax.text(0.5, y, tx("c04_city"), fontproperties=C.FP, fontsize=14, color=AMBER, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.075, tx("c04_foot"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.038, tx("tags"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")


def ephem_nums():
    """圖卡數字自己算一次（逐字稿星空對時表同法），不照抄"""
    import ephem

    def ob(t):
        o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.pressure, o.temp = 1010, 20
        o.date = ephem.Date(ephem.Date(t) - 8 * ephem.hour)
        return o
    g = ephem.FixedBody(); g._ra, g._dec = math.radians(266.4167), math.radians(-29.0078); g._epoch = ephem.J2000
    out = {}
    for key, t in (("21", "2027/7/2 21:00"), ("23", "2027/7/2 22:59"), ("01", "2027/7/3 01:00")):
        g.compute(ob(t))
        out["a" + key], out["z" + key] = f"{math.degrees(g.alt):.1f}", f"{math.degrees(g.az):.0f}"
    for d in range(1, 8):
        ok = []
        for k in range(0, 12 * 12 + 1):
            t = ephem.Date(f"2027/7/{d} 18:00") + k * 5 * ephem.minute
            o = ob(t); s, mo = ephem.Sun(o), ephem.Moon(o); g.compute(o)
            if s.alt < math.radians(-18) and mo.alt < 0 and g.alt > math.radians(20):
                ok.append(t)
        f = lambda t: ephem.Date(t).datetime().strftime("%H:%M")      # t 本身就是台北時間的寫法（ob() 才減 8 小時）
        print(f"  7/{d} 可看 {f(ok[0]) if ok else '-'}–{f(ok[-1]) if ok else '-'}")
    print("  銀心：" + "、".join(f"{k} {v}" for k, v in out.items()))
    return out


def run():
    C.emit("", [("中國", c01_cn), ("阿拉伯", c01_ar), ("疊合", c01_mix)], title="C-X07-01_箕斗之間")
    C.emit("", [("側視", c03_side), ("視線", c03_sight)], title="C-X07-03_我們在盤子裡")
    f, ax = C.newcard(dark=True)
    y = c02_card(ax)
    print(f"  C-X07-02 最後一框下緣 y={y:.3f}（要 > 0.07）")
    C.save(f, "", "C-X07-02_銀河的名字_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    c04_card(ax, ephem_nums())
    C.save(f, "", "C-X07-04_這幾晚看銀心_圖卡.png", transparent=False)


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    run()


if __name__ == "__main__":
    main()
