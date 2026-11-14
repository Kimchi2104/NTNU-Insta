# -*- coding: utf-8 -*-
"""A-36 現代星座（下）：課本沒教的星群｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A36-01_星座與星群        → 02 鏡（大熊層：IAU 大熊座邊界＋19 星連線 → 北斗層：北斗＝星群）
  C-A36-02_夏季大三角的距離  → 04 鏡（近處層：牛郎 16.7、織女 25.0 光年 → 天津四層：遠到畫面外）
  C-A36-03_衣架的真實距離    → 08 鏡（單層：10 顆星的 Gaia DR3 距離）
  C-A36-04_查理的橡樹        → 09 鏡（單層：南天小窗，台北看得到的最南 −65°）
  C-A36-05_六月晚上的五個星群 → 12 鏡（9:16 圖卡，可存圖：台北 2027/6/18 22:00 全天）
  C-A36-06_星群也有國籍      → 9:16 圖卡（貼文輪播用；逐字稿分鏡表沒有指定鏡頭，不進 Reels 逐頁表）
輸出：05_素材/A-36_現代星群/_概念圖/（--lang en → _概念圖/en/）；這次只出 zh。

來源：星位＝Stellarium hip_gaia3 星表（07_資料來源/_cache）；連線＝02_星群Asterisms.csv、Stellarium modern_iau
      （UMa 19 星、IAU 邊界 edges B1875→J2000，與 make_a36_v4.py 同一份）、chinese、arabic_indigenous；
      距離：織女 130.23 mas、牛郎 194.95 mas（van Leeuwen 2007）、天津四 Hipparcos 2.31 mas／大氣模型 802 pc
      （Schiller & Przybilla 2008）；衣架 10 星＝Stellarium hip_gaia3 星表的 Gaia DR3 視差（自讀二進位檔）。
      天象：PyEphem 4.2.1 自算（台北 25.033°N、121.565°E，2027/6/18 22:00，含大氣折射）。
      不臨摹任何出版星圖；全部依實際星位重畫。
"""
import os, sys, math, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Polygon
import gen_ep_assets as G
import make_a36_v4 as V

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-36_現代星群/_概念圖")
C.set_base(OUT)
RED, GREY, TEAL = "#FF6B6B", "#7C8BA8", V.TEAL
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "星座＝一塊天區；星群＝一個圖案",
        "c01_uma": "大熊座 Ursa Major", "c01_uma2": "IAU 88 個星座之一：有邊界的一塊天",
        "c01_uma3": "連線 19 顆星（Stellarium modern_iau）",
        "c01_bd": "北斗七星＝星群 asterism", "c01_bd2": "大家都認得，卻不是正式星座",
        "c01_bd3": "只是大熊的後半身和尾巴",
        "c01_foot": "白虛線＝IAU 1930 年星座邊界；依實際星位重畫",
        "c02_title": "看起來排在一起，距離差很多", "c02_sub": "從地球往外量（側視示意，方向不按比例）",
        "c02_earth": "地球", "c02_ly": "光年",
        "c02_alt": "牛郎（河鼓二）", "c02_alt2": "16.7 光年", "c02_vega": "織女", "c02_vega2": "25.0 光年",
        "c02_den": "天津四", "c02_den2": "1,000 光年以外", "c02_den3": "（估計約 1,400–2,600 光年）",
        "c02_far": "照同樣比例，天津四要放到右邊十幾個畫面以外",
        "c02_foot": "距離：Hipparcos 新歸算（van Leeuwen 2007）；天津四另見 Schiller & Przybilla 2008",
        "c03_title": "衣架：看起來排在一起，其實遠近不一", "c03_sky": "從地球看：狐狸座的衣架",
        "c03_axis": "離地球的距離（光年）", "c03_bar": "橫桿 6 星", "c03_hook": "鉤 4 星",
        "c03_foot": "距離：Gaia DR3 視差（Stellarium 星表）；不是真正的星團",
        "c04_title": "查理的橡樹 Robur Carolinum", "c04_sub": "Halley 1679 年命名；今天只是 Stellarium 裡的星群",
        "c04_lim": "台北看得到的最南：赤緯 −65°", "c04_no": "台灣看不全",
        "c04_car": "船底座", "c04_vel": "船帆座", "c04_cen": "半人馬座",
        "c04_foot": "紅虛線＝Stellarium modern 星群 RoC；白虛線＝IAU 邊界",
        "c05_title": "六月晚上的五個星群", "c05_sub": "2027/6/18（五）22:00・台北・頭頂在圓心",
        "N": "北", "S": "南", "E": "東", "W": "西",
        "c05_tri": "夏季大三角", "c05_bd": "北斗（斗柄朝上）", "c05_arc": "春季大曲線",
        "c05_arc2": "大角→角宿一", "c05_tea": "茶壺", "c05_coh": "衣架（雙筒；月光下難）",
        "c05_moon": "月亮（明早 08:44 滿月）",
        "c05_n1": "月光很亮：亮的星群照樣好認，銀河、衣架等 7/4 新月前後再看",
        "c05_n2": "存起來，晚上十點對著天空找", "c05_tag": "#萬國星空　#師大天文社",
        "c06_title": "星群也有國籍", "c06_sub": "同一批星，三種看法",
        "c06_h": ["", "西方（現代星群）", "中國（星官）", "阿拉伯"],
        "c06_r1": ["北斗七星", "Big Dipper 大勺子\n（英國叫 Plough 犁）", "北斗\n一個獨立的星官", "بنات نعش\n棺架的女兒們"],
        "c06_r2": ["夏季大三角", "Summer Triangle", "織女・河鼓二\n天津四", "兩隻鷹＋\n母雞的尾巴"],
        "c06_r3": ["人馬座茶壺", "Teapot 茶壺\nMilk Dipper 奶勺", "南斗六星\n＋箕宿", "下河喝水的\n鴕鳥"],
        "c06_r4": ["飛馬大四邊形", "Great Square\n跨飛馬、仙女兩座", "室宿＋壁宿", "—"],
        "c06_foot": "Stellarium：modern、chinese、arabic_al-sufi、arabic_indigenous",
        "c06_tag": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Constellation = an area; asterism = a pattern",
        "c01_uma": "Ursa Major", "c01_uma2": "one of the IAU's 88: a bounded patch of sky",
        "c01_uma3": "19 stars in its stick figure (Stellarium modern_iau)",
        "c01_bd": "Big Dipper = an asterism", "c01_bd2": "everyone knows it, yet it is no constellation",
        "c01_bd3": "just the bear's hindquarters and tail",
        "c01_foot": "dashed white = IAU 1930 boundaries; drawn on real star positions",
        "c02_title": "Side by side in the sky, far apart in space", "c02_sub": "distance from Earth (schematic side view)",
        "c02_earth": "Earth", "c02_ly": "light-years",
        "c02_alt": "Altair", "c02_alt2": "16.7 ly", "c02_vega": "Vega", "c02_vega2": "25.0 ly",
        "c02_den": "Deneb", "c02_den2": "over 1,000 ly", "c02_den3": "(estimates 1,400–2,600 ly)",
        "c02_far": "On this scale Deneb sits a dozen screens to the right",
        "c02_foot": "Distances: Hipparcos new reduction (van Leeuwen 2007); Deneb also Schiller & Przybilla 2008",
        "c03_title": "The Coathanger: lined up, not together", "c03_sky": "as seen from Earth (Vulpecula)",
        "c03_axis": "distance from Earth (light-years)", "c03_bar": "bar: 6 stars", "c03_hook": "hook: 4 stars",
        "c03_foot": "Distances: Gaia DR3 parallaxes (Stellarium catalogue); not a true cluster",
        "c04_title": "Charles' Oak, Robur Carolinum", "c04_sub": "named by Halley, 1679; today just a Stellarium asterism",
        "c04_lim": "southern limit from Taipei: Dec −65°", "c04_no": "never fully up in Taiwan",
        "c04_car": "Carina", "c04_vel": "Vela", "c04_cen": "Centaurus",
        "c04_foot": "dashed red = Stellarium modern asterism RoC; dashed white = IAU boundaries",
        "c05_title": "Five asterisms on a June night", "c05_sub": "Fri 18 Jun 2027, 22:00, Taipei; zenith at centre",
        "N": "N", "S": "S", "E": "E", "W": "W",
        "c05_tri": "Summer Triangle", "c05_bd": "Big Dipper (handle up)", "c05_arc": "Arc to Arcturus",
        "c05_arc2": "Arcturus → Spica", "c05_tea": "Teapot", "c05_coh": "Coathanger (binoculars; moonlit)",
        "c05_moon": "Moon (full at 08:44 tomorrow)",
        "c05_n1": "Bright moonlight: asterisms are easy, Milky Way and Coathanger wait for the 4 July new moon",
        "c05_n2": "Save this and look up at ten tonight", "c05_tag": "#WorldSkyCultures",
        "c06_title": "Asterisms have nationalities", "c06_sub": "same stars, three ways of seeing",
        "c06_h": ["", "West (modern)", "China (asterisms)", "Arabic"],
        "c06_r1": ["Big Dipper", "Big Dipper\n(Plough in Britain)", "Beidou\nits own asterism", "بنات نعش\nDaughters of the Bier"],
        "c06_r2": ["Summer Triangle", "Summer Triangle", "Zhinü, Hegu\nTianjin", "two eagles +\nthe hen's tail"],
        "c06_r3": ["Teapot", "Teapot\nMilk Dipper", "Southern Dipper\n+ Winnowing Basket", "ostriches going\nto drink"],
        "c06_r4": ["Great Square", "Great Square\nacross Peg and And", "Encampment\n+ Wall", "—"],
        "c06_foot": "Stellarium: modern, chinese, arabic_al-sufi, arabic_indigenous",
        "c06_tag": "#WorldSkyCultures",
    },
}


def tx(k):
    return TXT[LANG][k]


S = None


# ══════════════════════ 共用：切平面投影（東在左、北在上） ══════════════════════
def gnomonic(ra0, dec0, sc, cx=0.0, cy=0.0):
    a0, d0 = math.radians(ra0), math.radians(dec0)

    def P(ra, dec):
        a, d = math.radians(ra), math.radians(dec)
        c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
        x = math.cos(d) * math.sin(a - a0) / c
        y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / c
        return cx - math.degrees(x) * sc, cy + math.degrees(y) * sc
    return P


def draw_segs(ax, P, segs, col, lw=2.2, alpha=.9, ls="-", z=4):
    for s in segs:
        pts = [P(*S[h][:2]) for h in s if h in S]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            ax.plot([x1, x2], [y1, y2], c=col, lw=lw, alpha=alpha, ls=ls, solid_capstyle="round", zorder=z)


def draw_stars(ax, P, box, vmax=5.0, k=3.4, z=5, only=None, alpha=1.0):
    x0, x1, y0, y1 = box
    for h, (ra, dec, v) in ((h, S[h][:3]) for h in (only or S)):
        if v > vmax:
            continue
        x, y = P(ra, dec)
        if x0 <= x <= x1 and y0 <= y <= y1:
            ax.scatter([x], [y], s=max(2.0, (5.6 - v) ** 2.0 * k), c=WHITE, lw=0, zorder=z, alpha=alpha)


def draw_edges(ax, P, sel, box, col=WHITE, lw=1.4, alpha=.6):
    x0, x1, y0, y1 = box
    for pts, a, b in V.EDGES:
        if not sel(a, b):
            continue
        q = [P(ra, dec) for ra, dec in pts]
        for (xa, ya), (xb, yb) in zip(q, q[1:]):
            if all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in ((xa, ya), (xb, yb))):
                ax.plot([xa, xb], [ya, yb], c=col, lw=lw, alpha=alpha, ls=(0, (4, 3)), zorder=3)


# ══════════════════════ C-A36-01 星座與星群 ══════════════════════
P01 = None
BOX01 = (-0.95, 0.95, -0.62, 0.70)


def c01_uma(ax):
    T(ax, 0, 0.88, tx("c01_title"), 27)
    draw_edges(ax, P01, lambda a, b: "UMA" in (a, b), BOX01, lw=1.6, alpha=.75)
    draw_stars(ax, P01, BOX01, vmax=4.6, alpha=.55)
    draw_segs(ax, P01, V.SEG["UMa"], WHITE, lw=2.0, alpha=.85)
    T(ax, -0.55, -0.66, tx("c01_uma"), 21, WHITE)
    T(ax, -0.55, -0.74, tx("c01_uma2"), 14.5, GREY, w="normal")
    T(ax, -0.55, -0.81, tx("c01_uma3"), 13, GREY, w="normal")
    T(ax, 0, -0.93, tx("c01_foot"), 11.5, GREY, w="normal")


def c01_bd(ax):
    draw_segs(ax, P01, V.SEG["BDr"], AMBER, lw=5.0, alpha=.95, z=6)
    for h in V.flat(V.SEG["BDr"]):
        x, y = P01(*S[h][:2])
        ax.scatter([x], [y], s=95, c=AMBER, lw=0, zorder=7)
    T(ax, 0.50, -0.66, tx("c01_bd"), 21, AMBER)
    T(ax, 0.50, -0.74, tx("c01_bd2"), 14.5, WHITE, w="normal")
    T(ax, 0.50, -0.81, tx("c01_bd3"), 13, GREY, w="normal")


# ══════════════════════ C-A36-02 夏季大三角的距離 ══════════════════════
X0, XS = -0.82, 0.026                            # 地球位置、每光年 0.026（25 光年＝0.65）


def c02_near(ax):
    T(ax, 0, 0.80, tx("c02_title"), 27)
    T(ax, 0, 0.72, tx("c02_sub"), 15, GREY, w="normal")
    y = -0.05
    ax.plot([X0, 0.90], [y, y], c=WHITE, lw=1.6, alpha=.45, zorder=2)
    for ly in (0, 10, 20, 30):
        x = X0 + ly * XS
        ax.plot([x, x], [y - 0.015, y + 0.015], c=WHITE, lw=1.2, alpha=.5)
        T(ax, x, y - 0.06, f"{ly}", 12, GREY, w="normal")
    T(ax, X0 + 32 * XS, y - 0.06, tx("c02_ly"), 12, GREY, w="normal", ha="left")
    ax.add_patch(Circle((X0, y), 0.035, fc=BLUE, ec="none", zorder=5))
    T(ax, X0, y + 0.09, tx("c02_earth"), 16, BLUE)
    for d, k1, k2, yy in ((1000 / 194.95 * 3.26156, "c02_alt", "c02_alt2", 0.20),
                          (1000 / 130.23 * 3.26156, "c02_vega", "c02_vega2", 0.52)):
        x = X0 + d * XS
        ax.plot([x, x], [y, yy - 0.05], c=BLUE, lw=1.2, alpha=.6, ls=(0, (3, 3)))
        ax.scatter([x], [yy], s=420, c=WHITE, lw=0, zorder=6)
        ax.scatter([x], [yy], s=1500, c=BLUE, lw=0, alpha=.18, zorder=5)
        T(ax, x, yy + 0.10, tx(k1), 19, WHITE)
        T(ax, x, yy - 0.10, tx(k2), 16, BLUE)
    T(ax, 0, -0.86, tx("c02_foot"), 11, GREY, w="normal")


def c02_deneb(ax):
    y = -0.05
    x = 0.62
    for dx in (0.0, 0.035):                         # 斷軸記號
        ax.plot([x - 0.015 + dx, x + 0.015 + dx], [y - 0.03, y + 0.03], c=WHITE, lw=2.0, alpha=.8, zorder=6)
    C.arrow(ax, (0.96, 0.32), (0.70, 0.32), c=AMBER, lw=3.0, alpha=.95)
    T(ax, 0.62, 0.45, tx("c02_den"), 21, AMBER)
    T(ax, 0.62, 0.20, tx("c02_den2"), 17, AMBER)
    T(ax, 0.62, 0.13, tx("c02_den3"), 12.5, GREY, w="normal")
    T(ax, 0, -0.42, tx("c02_far"), 17, WHITE)


# ══════════════════════ C-A36-03 衣架的真實距離 ══════════════════════
def gaia_plx(hips):
    d = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/stars/hip_gaia3/")
    import numpy as np
    dt = np.dtype([("gaia", "<i8"), ("x0", "<i4"), ("x1", "<i4"), ("x2", "<i4"), ("dx0", "<i4"), ("dx1", "<i4"),
                   ("dx2", "<i4"), ("bv", "<i2"), ("vmag", "<i2"), ("plx", "<u2"), ("plx_err", "<u2"),
                   ("rv", "<i2"), ("sp", "<u2"), ("objtype", "u1"), ("hip3", "3u1")])
    out = {}
    for f in ["stars_0_0v0_21.cat", "stars_1_0v0_16.cat", "stars_2_0v0_17.cat", "stars_3_0v0_10.cat"]:
        with open(d + f, "rb") as fh:
            _m, _t, _ma, _mi, level, _mm = struct.unpack("<6I", fh.read(24)); fh.read(4)
            nz = 20 * 4 ** level + 1
            zs = np.frombuffer(fh.read(4 * nz), dtype="<u4")
            rec = np.frombuffer(fh.read(48 * int(zs.sum())), dtype=dt)
        h3 = rec["hip3"].astype(np.uint32)
        hip = (h3[:, 0] | (h3[:, 1] << 8) | (h3[:, 2] << 16)) >> 5
        for i in np.where(np.isin(hip, list(hips)))[0]:
            out[int(hip[i])] = (rec["plx"][i] * 0.02, rec["plx_err"][i] * 0.02)     # mas（單位 0.02 mas）
    return out


def c03_coh(ax):
    T(ax, 0, 0.88, tx("c03_title"), 25)
    hs = V.COH
    plx = gaia_plx(hs)
    ra0 = sum(S[h][0] for h in hs) / len(hs); de0 = sum(S[h][1] for h in hs) / len(hs)
    P = gnomonic(ra0, de0, 0.62, cx=0.0, cy=0.50)
    T(ax, 0, 0.74, tx("c03_sky"), 15, GREY, w="normal")
    draw_segs(ax, P, V.SEG["CoH"], PURPLE, lw=2.4, alpha=.85)
    bar = set(V.SEG["CoH"][0])
    order = sorted(hs, key=lambda h: 1000.0 / plx[h][0])
    ya = -0.42
    lo, hi = 0.0, 1800.0
    fx = lambda ly: -0.80 + (ly - lo) / (hi - lo) * 1.60
    ax.plot([fx(0), fx(hi)], [ya, ya], c=WHITE, lw=1.6, alpha=.5)
    for ly in range(0, 1801, 300):
        ax.plot([fx(ly), fx(ly)], [ya - 0.015, ya + 0.015], c=WHITE, lw=1.2, alpha=.5)
        T(ax, fx(ly), ya - 0.055, f"{ly:,}", 11.5, GREY, w="normal")
    T(ax, 0, ya - 0.12, tx("c03_axis"), 13, GREY, w="normal")
    for h in hs:
        x, y = P(*S[h][:2])
        ly = 1000.0 / plx[h][0] * 3.26156
        col = PURPLE if h in bar else AMBER
        ax.scatter([x], [y], s=max(30, (7.6 - S[h][2]) ** 2 * 30), c=WHITE, lw=0, zorder=6)
        ax.plot([x, fx(ly)], [y - 0.02, ya + 0.02], c=col, lw=1.0, alpha=.45, zorder=3)
        ax.scatter([fx(ly)], [ya], s=70, c=col, lw=0, zorder=6)
    T(ax, -0.62, 0.16, tx("c03_bar"), 14, PURPLE)
    T(ax, 0.62, 0.16, tx("c03_hook"), 14, AMBER)
    T(ax, 0, -0.70, tx("c03_foot"), 11.5, GREY, w="normal")
    print("  衣架距離（光年）：" + "、".join(f"{h} {1000.0 / plx[h][0] * 3.26156:.0f}" for h in order))


# ══════════════════════ C-A36-04 查理的橡樹 ══════════════════════
def c04_oak(ax):
    T(ax, 0, 0.88, tx("c04_title"), 25, RED)
    T(ax, 0, 0.80, tx("c04_sub"), 14.5, GREY, w="normal")
    hs = V.flat(V.SEG["RoC"])
    ra0 = sum(S[h][0] for h in hs) / len(hs); de0 = sum(S[h][1] for h in hs) / len(hs)
    P = gnomonic(ra0, de0, 0.040, cx=0.0, cy=0.0)
    box = (-0.95, 0.95, -0.72, 0.72)
    lim = -(90 - V.PHI)                              # 台北看得到的最南（不計大氣折射）
    pts = [P(ra0 + d, lim) for d in range(-40, 41, 2)]
    pts = [(x, y) for x, y in pts if box[0] <= x <= box[1]]
    ax.add_patch(Polygon(pts + [(pts[-1][0], -0.72), (pts[0][0], -0.72)], closed=True, fc="#000000",
                         ec="none", alpha=.55, zorder=2))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=GREEN, lw=2.2, alpha=.9, zorder=7)
    draw_edges(ax, P, lambda a, b: any(c in (a, b) for c in ("CAR", "VEL", "CEN")), box, lw=1.1, alpha=.45)
    draw_stars(ax, P, box, vmax=4.8, k=2.6, alpha=.75)
    draw_segs(ax, P, V.SEG["RoC"], RED, lw=2.0, alpha=.95, ls=(0, (4, 2.5)))
    x, y = pts[len(pts) // 2]
    T(ax, -0.50, y + 0.12, tx("c04_lim"), 13.5, GREEN)
    T(ax, 0.50, y - 0.12, tx("c04_no"), 17, WHITE)
    for k, (ra, dec) in (("c04_car", (138, -62)), ("c04_vel", (150, -47)), ("c04_cen", (185, -48))):
        px, py = P(ra, dec)
        if box[0] < px < box[1] and box[2] < py < box[3]:
            T(ax, px, py, tx(k), 13, GREY, w="normal")
    T(ax, 0, -0.80, tx("c04_foot"), 11, GREY, w="normal")


# ══════════════════════ C-A36-05 六月晚上的五個星群（圖卡） ══════════════════════
def c05_card(ax):
    import ephem
    o = V._obs("2027/6/18 22:00")
    ax.text(0.5, 0.925, tx("c05_title"), fontproperties=C.FP, fontsize=24, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.885, tx("c05_sub"), fontproperties=C.FP, fontsize=12, color=GREY, ha="center", va="center")
    cx, cy, R = 0.5, 0.55, 0.44
    asp = 9 / 16

    def xy(alt, az):
        r = (90 - alt) / 90 * R
        a = math.radians(az)
        return cx - r * math.sin(a), cy + r * math.cos(a) * asp     # 北上、東左（仰望）

    ax.add_patch(Ellipse((cx, cy), 2 * R, 2 * R * asp, fc="#0E1530", ec=GREY, lw=1.2, zorder=1))
    for alt in (30, 60):
        ax.add_patch(Ellipse((cx, cy), 2 * R * (90 - alt) / 90, 2 * R * (90 - alt) / 90 * asp, fc="none", ec=GREY,
                             lw=0.6, alpha=.35, ls=(0, (3, 3)), zorder=2))
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = xy(-8, az)
        ax.text(x, y, tx(k), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center", weight="bold")

    def star(h):
        return V.altaz(*S[h][:2], "2027/6/18 22:00")

    for h, (ra, dec, v) in ((h, S[h][:3]) for h in S):
        if v > 4.0:
            continue
        alt, az = star(h)
        if alt < 0:
            continue
        x, y = xy(alt, az)
        ax.scatter([x], [y], s=max(1.2, (4.6 - v) ** 2.1 * 1.8), c=WHITE, lw=0, zorder=4)
    for key, col in (("STr", BLUE), ("BDr", AMBER), ("RH1", GREEN), ("Tea", AMBER), ("CoH", PURPLE)):
        for s in V.SEG[key]:
            for a, b in zip(s, s[1:]):
                (x1, y1), (x2, y2) = xy(*star(a)), xy(*star(b))
                ax.plot([x1, x2], [y1, y2], c=col, lw=1.6 if key != "CoH" else 1.0, alpha=.9, zorder=3)
    mx, my = xy(V.MOON["alt"], V.MOON["az"])
    ax.scatter([mx], [my], s=260, c="#FFF6D8", lw=0, zorder=6)
    ax.scatter([mx], [my], s=1300, c="#FFF6D8", lw=0, alpha=.15, zorder=5)
    cen = lambda key: [sum(c) / len(c) for c in zip(*[xy(*star(h)) for h in V.flat(V.SEG[key])])]
    hx, hy = xy(*star(95487))
    vx, vy = xy(*star(V.VEGA))
    labs = [((vx, vy), "c05_tri", BLUE, (-0.03, 0.040)), (cen("BDr"), "c05_bd", AMBER, (0.02, -0.05)),
            (cen("Tea"), "c05_tea", AMBER, (-0.02, -0.040)), ((hx, hy), "c05_coh", PURPLE, (-0.01, -0.050)),
            ((mx, my), "c05_moon", WHITE, (0.07, 0.030))]
    ax2 = xy(*star(V.ARCT)); sp = xy(*star(V.SPICA))
    labs.append((((ax2[0] + sp[0]) / 2 + 0.10, (ax2[1] + sp[1]) / 2), "c05_arc", GREEN, (0.0, 0.0)))
    for (x, y), key, col, (dx, dy) in labs:
        ax.text(x + dx, y + dy, tx(key), fontproperties=C.FP, fontsize=11.5, color=col, ha="center", va="center",
                weight="bold", zorder=7)
    x, y = labs[-1][0]
    ax.text(x, y - 0.018, tx("c05_arc2"), fontproperties=C.FP, fontsize=9.5, color=WHITE, ha="center", va="center",
            zorder=7)
    ax.text(0.5, 0.215, tx("c05_n1"), fontproperties=C.FP, fontsize=11, color=WHITE, ha="center", va="center",
            wrap=True)
    ax.text(0.5, 0.165, tx("c05_n2"), fontproperties=C.FP, fontsize=14, color=AMBER, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.035, tx("c05_tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A36-06 星群也有國籍（圖卡） ══════════════════════
def thumb(ax, key, x, y, w, col):
    segs = V.SEG[key]
    hs = V.flat(segs)
    ra0 = math.degrees(math.atan2(sum(math.sin(math.radians(S[h][0])) for h in hs),
                                  sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    de0 = sum(S[h][1] for h in hs) / len(hs)
    P0 = gnomonic(ra0, de0, 1.0)
    pts = [P0(*S[h][:2]) for h in hs]
    span = max(max(p[0] for p in pts) - min(p[0] for p in pts), (max(p[1] for p in pts) - min(p[1] for p in pts)) / 0.5625)
    sc = w / span
    mx = (max(p[0] for p in pts) + min(p[0] for p in pts)) / 2
    my = (max(p[1] for p in pts) + min(p[1] for p in pts)) / 2
    P = lambda ra, dec: (x + (P0(ra, dec)[0] - mx) * sc, y + (P0(ra, dec)[1] - my) * sc * 0.5625)
    draw_segs(ax, P, segs, col, lw=1.3, alpha=.9)
    for h in hs:
        px, py = P(*S[h][:2])
        ax.scatter([px], [py], s=max(2, (5.0 - S[h][2]) ** 2 * 1.6), c=WHITE, lw=0, zorder=5)


def c06_card(ax):
    ax.text(0.5, 0.925, tx("c06_title"), fontproperties=C.FP, fontsize=25, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.885, tx("c06_sub"), fontproperties=C.FP, fontsize=13, color=GREY, ha="center", va="center")
    cols = [0.14, 0.40, 0.64, 0.86]
    hcol = [WHITE, AMBER, TEAL, GREEN]
    for x, h, c in zip(cols, tx("c06_h"), hcol):
        ax.text(x, 0.835, h, fontproperties=C.FP, fontsize=11.5, color=c, ha="center", va="center", weight="bold")
    rows = [("c06_r1", "BDr", AMBER), ("c06_r2", "STr", BLUE), ("c06_r3", "Tea", AMBER), ("c06_r4", "GSP", AMBER)]
    y0, dy = 0.735, 0.165
    for i, (rk, key, col) in enumerate(rows):
        y = y0 - i * dy
        ax.add_patch(FancyBboxPatch((0.03, y - 0.070), 0.94, 0.140, boxstyle="round,pad=0,rounding_size=0.015",
                                    fc="#141C38", ec=GREY, lw=0.8, alpha=.85, zorder=1))
        r = tx(rk)
        thumb(ax, key, cols[0], y + 0.015, 0.17, col)
        ax.text(cols[0], y - 0.050, r[0], fontproperties=C.FP, fontsize=11, color=WHITE, ha="center", va="center",
                weight="bold", zorder=6)
        for x, t, c in zip(cols[1:], r[1:], hcol[1:]):
            from gen_ep_assets import rtl
            t = "\n".join(rtl(l) if any("؀" <= ch <= "ۿ" for ch in l) else l for l in t.split("\n"))
            ax.text(x, y, t, fontproperties=C.FP, fontsize=10.5, color=WHITE if c != TEAL else "#A8E0D4",
                    ha="center", va="center", linespacing=1.35, zorder=6)
    ax.text(0.5, 0.075, tx("c06_foot"), fontproperties=C.FP, fontsize=9, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.035, tx("c06_tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ 輸出 ══════════════════════
def main():
    global S, LANG, P01
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    hs = V.flat(V.SEG["UMa"])
    P01 = gnomonic(sum(S[h][0] for h in hs) / len(hs) + 2.0, sum(S[h][1] for h in hs) / len(hs) - 2.0, 0.026,
                   cx=0.0, cy=0.06)
    C.emit("", [("大熊", c01_uma), ("北斗", c01_bd)], title="C-A36-01_星座與星群")
    C.emit("", [("近處", c02_near), ("天津四", c02_deneb)], title="C-A36-02_夏季大三角的距離")
    f, ax = C.newfig(); c03_coh(ax); C.save(f, "", "C-A36-03_衣架的真實距離_透明.png")
    f, ax = C.newfig(dark=True); c03_coh(ax); C.save(f, "", "C-A36-03_衣架的真實距離_預覽_黑底.png", transparent=False)
    f, ax = C.newfig(); c04_oak(ax); C.save(f, "", "C-A36-04_查理的橡樹_透明.png")
    f, ax = C.newfig(dark=True); c04_oak(ax); C.save(f, "", "C-A36-04_查理的橡樹_預覽_黑底.png", transparent=False)
    f, ax = C.newcard(dark=True); c05_card(ax); C.save(f, "", "C-A36-05_六月晚上的五個星群_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True); c06_card(ax); C.save(f, "", "C-A36-06_星群也有國籍_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
