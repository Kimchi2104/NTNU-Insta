# -*- coding: utf-8 -*-
"""X-05 南天的十字路口｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-X05-01_找南方的兩條線 → 03 鏡（延長層→中垂線層→地平線層）
  C-X05-02_南十字的名字   → 04 鏡（9:16 圖卡，可存圖）
  C-X05-03_認錯十字       → 06 鏡（真南層→假十字層）
  C-X05-04_台灣怎麼分     → 08 鏡（9:16 圖卡，可存圖）
  C-X05-05_歲差           → 11 鏡（軌跡層→高度層）
  C-X05-06_今晚看南十字   → 13 鏡（9:16 圖卡，可存圖）
輸出：05_素材/X-05_南天十字/_概念圖/（--lang en → _概念圖/en/，只出方形三組）

做法：星位一律 03_星點座標表（J2000）；01 用 make_x05_v4 的南盤投影（rot＝5/14 21:00 面南，十字直立）；
      03、04、06 以 PyEphem（含折射）算地平座標，再用面向南方的立體投影畫（地平線是弧線）；
      05 以黃南極為心的方位等距投影，南天極的位置用 PyEphem 把「各年代的南天極」換回 J2000。
      「延長 4.5 倍」＝過十字架二再延長 4.5 個十字架一→十字架二的長度（逐字稿 4.45 倍；離南天極 2.68°）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, BG, T
from matplotlib.patches import Polygon as MPoly, Circle
import gen_ep_assets as G
import make_x05_v4 as X

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-05_南天十字/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#7C8BA8"
LANG = "zh"
S = None
LAT_SEA = -21.0          # 06 鏡「南緯二十度左右的海上」（東加）

TXT = {
    "zh": {
        "c01_title": "找南方的兩條線", "ext": "延長 4.5 倍", "pole": "南天極", "near": "差不到 3°",
        "gamma": "十字架一", "alpha": "十字架二", "pointers": "指針", "rigil": "南門二", "hadar": "馬腹一",
        "bis": "中垂線", "c01_s1": "① 十字架一 → 十字架二，再延長 4.5 倍",
        "c01_s2": "② 南門二—馬腹一的中垂線，也指到同一帶",
        "hz": "地平線", "south": "正南", "drop": "③ 從南天極垂直落到地平線＝正南",
        "c01_foot": "南盤投影；南天極在地平線上方的情形（南半球，例：南緯 21°）。兩線交點離南天極 2.95°",
        "c03_title": "照南十字的方法找假十字：南方偏掉多少？",
        "c03_sub": "南緯 21° 的海上，假十字站到最高時（面向南方）",
        "true": "真南 180°", "crux_m": "南十字同法 183°", "f1": "156°（偏東 24°）", "f2": "222°（偏西 42°）",
        "fc": "假十字", "c03_foot": "延長＝過下面那顆星再延長 4.5 倍，從那一點垂直落到地平線；只適用上中天（PyEphem 自算）",
        "E": "東南", "S": "南", "W": "西南",
        "c05_title": "地軸像陀螺一樣慢慢晃：南天極在動",
        "track": "南天極的軌跡（約 2.6 萬年一圈）", "sep": "黃南極",
        "y1": "公元元年", "y1000": "1000 年", "y2027": "2027 年", "crux": "南十字",
        "c05_alt": "台北看十字架二最高時離地平線", "deg": "{:.1f}°",
        "ptol": "托勒密（約 150 年）在亞歷山卓：十字架二 5.9°、十字架一 11.9°",
        "c05_foot": "幾何高度，未計大氣折射；PyEphem 歲差",
    },
    "en": {
        "c01_title": "Two lines to the south", "ext": "extend 4.5×", "pole": "South Celestial Pole",
        "near": "within 3°", "gamma": "Gacrux", "alpha": "Acrux", "pointers": "the Pointers",
        "rigil": "α Cen", "hadar": "β Cen", "bis": "perpendicular bisector",
        "c01_s1": "① Gacrux → Acrux, then 4.5 times further",
        "c01_s2": "② The Pointers' bisector lands in the same patch",
        "hz": "horizon", "south": "due south", "drop": "③ Drop straight down from the pole = due south",
        "c01_foot": "Southern disc projection; pole above the horizon (e.g. 21°S). The lines cross 2.95° from the pole",
        "c03_title": "Use the False Cross the same way: how far off is 'south'?",
        "c03_sub": "At sea, 21°S, with the False Cross at its highest (facing south)",
        "true": "true south 180°", "crux_m": "Crux method 183°", "f1": "156° (24° east)", "f2": "222° (42° west)",
        "fc": "False Cross",
        "c03_foot": "Extend 4.5× past the lower star, then drop to the horizon; valid at culmination only (computed)",
        "E": "SE", "S": "S", "W": "SW",
        "c05_title": "Earth's axis wobbles like a top: the pole moves",
        "track": "Path of the south celestial pole (~26,000 yr)", "sep": "S. ecliptic pole",
        "y1": "AD 1", "y1000": "AD 1000", "y2027": "2027", "crux": "Crux",
        "c05_alt": "Acrux at its highest, seen from Taipei", "deg": "{:.1f}°",
        "ptol": "Ptolemy (c. AD 150), Alexandria: Acrux 5.9°, Gacrux 11.9°",
        "c05_foot": "Geometric altitude, no refraction; precession by PyEphem",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 共用：地平座標與立體投影（同 A-31） ══════════════════════
def altaz_fn(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)

    def f(ra, dec):
        b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
        b.compute(o)
        return math.degrees(b.alt), math.degrees(b.az)
    return f


def altaz_lst(lat, lst):
    """幾何地平座標（不計折射；06 鏡的海上示意用恆星時直接算）"""
    f_ = math.radians(lat)

    def f(ra, dec):
        H = math.radians(lst - ra); d = math.radians(dec)
        alt = math.asin(math.sin(f_) * math.sin(d) + math.cos(f_) * math.cos(d) * math.cos(H))
        az = math.atan2(-math.cos(d) * math.sin(H), math.sin(d) * math.cos(f_) - math.cos(d) * math.sin(f_) * math.cos(H))
        return math.degrees(alt), math.degrees(az) % 360
    return f


def stereo(az0, alt0, sc, oy, ox=0.0):
    def v(alt, az):
        a, z = math.radians(alt), math.radians(az)
        return (math.sin(z) * math.cos(a), math.cos(z) * math.cos(a), math.sin(a))
    c = v(alt0, az0)
    r = (c[1], -c[0], 0.0); n = math.hypot(r[0], r[1]); r = (r[0] / n, r[1] / n, 0.0)
    u = (r[1] * c[2] - 0.0, 0.0 - r[0] * c[2], r[0] * c[1] - r[1] * c[0])

    def P(alt, az):
        w = v(alt, az)
        k = 1.0 / (1.0 + sum(p * q for p, q in zip(w, c)))
        return ox + sc * k * sum(p * q for p, q in zip(w, r)), oy + sc * k * sum(p * q for p, q in zip(w, u))
    return P


def segs_plot(ax, segs, Pf, col, lw=2.2, alpha=.95, z=5):
    for seg in segs:
        q = [Pf(*S[h][:2]) for h in seg if h in S]
        q = [p for p in q if p is not None]
        if len(q) >= 2:
            ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=lw, alpha=alpha, zorder=z)


def stars_plot(ax, Pf, vmax=4.6, box=(-1, 1, -1, 1), k=3.0, decmax=-20, z=4):
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < vmax and S[h][1] < decmax]:
        p = Pf(ra, dec)
        if p and box[0] < p[0] < box[1] and box[2] < p[1] < box[3]:
            ax.scatter([p[0]], [p[1]], s=max(0.4, (vmax + 0.4 - vm)) ** 1.8 * k, c=WHITE, lw=0, zorder=z, alpha=.9)


# ══════════════════════ C-X05-01 找南方的兩條線 ══════════════════════
_G = {}


def _geo():
    if "g" not in _G:
        _G["g"] = X.geometry(S)
        _G["m"] = _M()
    return _G["g"], _G["m"]


Y_POLE01, SC01 = -0.30, 0.0150


def P01(ra, dec):
    g, m = _geo()
    x, y = X.disc_xy(m, ra, dec, X.ROT_C)
    px, py = X.disc_xy(m, 0.0, -90.0, X.ROT_C)
    return (x - px) * SC01 + 0.10, (y - py) * SC01 + Y_POLE01


def c01_ext(ax):
    g, m = _geo()
    T(ax, 0.0, 0.92, tx("c01_title"), 30, WHITE)
    stars_plot(ax, P01, vmax=4.4, box=(-0.97, 0.97, -0.55, 0.80), k=3.2)
    segs_plot(ax, X.SEG_CRUX, P01, AMBER, lw=2.6)
    q = [P01(*p) for p in g["crux_ext"]]
    ax.plot([p[0] for p in q], [p[1] for p in q], c=WHITE, lw=2.0, ls=(0, (5, 4)), alpha=.95, zorder=6)
    q = [P01(*p) for p in g["X_circle"]]
    ax.plot([p[0] for p in q], [p[1] for p in q], c=WHITE, lw=1.8, zorder=6)
    px, py = P01(0.0, -90.0)
    for dx, dy in ((0.03, 0), (0, 0.03)):
        ax.plot([px - dx, px + dx], [py - dy, py + dy], c=WHITE, lw=2.4, zorder=7)
    T(ax, px - 0.06, py - 0.06, tx("pole"), 17, WHITE, ha="right")
    x, y = P01(*g["X"]); T(ax, x + 0.10, y + 0.02, tx("near"), 16, WHITE, ha="left")
    x, y = P01(*S[X.GACRUX][:2]); T(ax, x + 0.06, y + 0.02, tx("gamma"), 15, AMBER, ha="left")
    x, y = P01(*S[X.ACRUX][:2]); T(ax, x + 0.06, y - 0.03, tx("alpha"), 15, AMBER, ha="left")
    mid = g["crux_ext"][len(g["crux_ext"]) * 3 // 5]
    x, y = P01(*mid); T(ax, x + 0.05, y, tx("ext"), 16, WHITE, ha="left")
    T(ax, -0.95, 0.83, tx("c01_s1"), 16, AMBER, ha="left", w="normal")


def c01_bis(ax):
    g, m = _geo()
    segs_plot(ax, [[X.RIGIL, X.HADAR]], P01, WHITE, lw=1.4, alpha=.6)
    q = [P01(*p) for p in g["bis"]]
    ax.plot([p[0] for p in q], [p[1] for p in q], c=GREEN, lw=2.0, ls=(0, (5, 4)), alpha=.95, zorder=6)
    for h, k, dx, dy in ((X.RIGIL, "rigil", -0.05, -0.04), (X.HADAR, "hadar", 0.05, -0.01)):
        x, y = P01(*S[h][:2])
        ax.scatter([x], [y], s=150, c=WHITE, zorder=7)
        T(ax, x + dx, y + dy, tx(k), 15, WHITE, ha="right" if dx < 0 else "left")
    x, y = P01(*X.radec([sum(X.vec(*S[h][:2])[i] for h in (X.RIGIL, X.HADAR)) for i in range(3)]))
    T(ax, x - 0.08, y + 0.14, tx("pointers"), 18, WHITE)
    x, y = P01(*g["bis"][len(g["bis"]) // 2]); T(ax, x - 0.05, y, tx("bis"), 15, GREEN, ha="right")
    T(ax, -0.95, 0.76, tx("c01_s2"), 16, GREEN, ha="left", w="normal")


def c01_hz(ax):
    px, py = P01(0.0, -90.0)
    hy = py - 21.0 * _M().k * SC01                 # 南緯 21°：南天極在地平線上 21°（盤上 k·21）
    ax.plot([-0.95, 0.95], [hy, hy], c=GREEN, lw=2.4, zorder=6)
    ax.add_patch(MPoly([(-0.95, hy), (0.95, hy), (0.95, -0.80), (-0.95, -0.80)], closed=True, fc=BG, alpha=.85,
                       ec="none", zorder=5))
    T(ax, 0.92, hy + 0.035, tx("hz"), 14, GREEN, ha="right", w="normal")
    C.arrow(ax, (px, hy + 0.01), (px, py - 0.03), c=WHITE, lw=2.4, alpha=.95, style="-|>")
    ax.plot([px, px], [hy - 0.03, hy + 0.03], c=WHITE, lw=2.4, zorder=7)
    T(ax, px + 0.05, hy - 0.06, tx("south"), 20, WHITE, ha="left")
    T(ax, -0.95, 0.69, tx("drop"), 16, WHITE, ha="left", w="normal")
    T(ax, 0.0, -0.94, tx("c01_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-X05-03 認錯十字 ══════════════════════
def _c03():
    fc = X.radec([sum(X.vec(*S[h][:2])[i] for h in X.FCR) for i in range(3)])
    f = altaz_lst(LAT_SEA, fc[0])
    Pp = stereo(190.0, 24.0, 1.45, -0.02)
    return f, (lambda alt, az: Pp(alt, az))


def _drop(ax, f, Pp, pt, col, lab, dx, dy, lw=2.0):
    alt, az = f(*pt)
    q = [Pp(alt * (1 - i / 30), az) for i in range(31)]
    ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=1.4, ls=(0, (2, 3)), zorder=6)
    x, y = Pp(0.0, az)
    C.arrow(ax, (x, y), q[-6], c=col, lw=lw, alpha=.95, style="-|>")
    T(ax, x + dx, y + dy, lab, 15, col)
    return az


def c03_true(ax):
    f, Pp = _c03()
    T(ax, 0.0, 0.92, tx("c03_title"), 22, WHITE)
    T(ax, 0.0, 0.85, tx("c03_sub"), 15, GREY, w="normal")
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 4.2]:
        alt, az = f(ra, dec)
        if alt > 0.5:
            x, y = Pp(alt, az)
            if abs(x) < 0.96 and -0.5 < y < 0.80:
                ax.scatter([x], [y], s=max(0.5, (4.6 - vm)) ** 1.8 * 2.6, c=WHITE, lw=0, zorder=4, alpha=.85)
    hz = [Pp(0.0, az) for az in range(120, 261)]
    ax.add_patch(MPoly(hz + [(hz[-1][0], -0.85), (hz[0][0], -0.85)], closed=True, fc=BG, ec="none", zorder=5))
    ax.plot([p[0] for p in hz], [p[1] for p in hz], c=GREEN, lw=2.4, zorder=6)
    for az in range(140, 241, 10):
        x, y = Pp(0.0, az)
        ax.plot([x, x], [y, y - 0.02], c=GREEN, lw=1.4, zorder=6)
    for az, k in ((140, "E"), (240, "W")):                  # 東在左（面向南方）
        x, y = Pp(0.0, az)
        T(ax, x, y + 0.05, tx(k), 14, GREEN, w="normal")
    g, m = _geo()
    segs_plot(ax, X.SEG_CRUX, lambda ra, dec: Pp(*f(ra, dec)), AMBER, lw=2.2)
    x, y = Pp(*f(*S[X.GACRUX][:2])); T(ax, x - 0.03, y + 0.05, tx("crux"), 14, AMBER)
    pa, paz = f(0.0, -90.0)
    x, y = Pp(pa, paz)
    for d in ((0.025, 0), (0, 0.025)):
        ax.plot([x - d[0], x + d[0]], [y - d[1], y + d[1]], c=WHITE, lw=2.2, zorder=7)
    T(ax, x + 0.04, y + 0.035, tx("pole") if LANG == "zh" else "SCP", 14, WHITE, ha="left")
    _drop(ax, f, Pp, (0.0, -90.0), WHITE, tx("true"), 0.0, -0.08, lw=2.6)
    end = g["crux_ext"][-1]
    a2, z2 = f(*end)
    x2, y2 = Pp(0.0, z2)
    T(ax, x2 + 0.02, y2 - 0.15, tx("crux_m"), 13, AMBER, w="normal")
    T(ax, 0.0, -0.93, tx("c03_foot"), 11, GREY, w="normal")


def c03_false(ax):
    f, Pp = _c03()
    g, m = _geo()
    segs_plot(ax, X.SEG_FCR, lambda ra, dec: Pp(*f(ra, dec)), RED, lw=2.6)
    for k in ("f1", "f2"):
        q = [Pp(*f(*p)) for p in g[k]]
        ax.plot([p[0] for p in q], [p[1] for p in q], c=RED, lw=1.8, ls=(0, (5, 4)), zorder=6)
    z1 = _drop(ax, f, Pp, g["f1"][-1], RED, tx("f1"), -0.02, -0.08)
    z2 = _drop(ax, f, Pp, g["f2"][-1], RED, tx("f2"), 0.02, -0.08)
    fcx = Pp(*f(*S[X.DEL_VEL][:2]))
    T(ax, fcx[0] + 0.12, fcx[1] + 0.06, tx("fc"), 18, RED, ha="left")
    _C03[:] = [z1, z2]


_C03 = []


# ══════════════════════ C-X05-05 歲差 ══════════════════════
SEP = (90.0, -66.5607)                   # 黃南極（J2000）
SC05, OY05 = 0.0125, 0.30


def P05(ra, dec):
    """以黃南極為心的方位等距投影（南天朝外看：東在左）"""
    a, b = X.vec(*SEP), X.vec(ra, dec)
    d = math.degrees(math.acos(max(-1, min(1, X.dot(a, b)))))
    # 方位：以「往南天極」為上
    up = X.unit(X.cross(X.cross(a, (0, 0, -1)), a))
    e = X.unit(X.cross(a, up))
    t = X.unit(tuple(b[i] - X.dot(a, b) * a[i] for i in range(3))) if d > 1e-6 else up
    ang = math.atan2(X.dot(t, e), X.dot(t, up))
    return -d * math.sin(ang) * SC05, OY05 - 32 * SC05 + d * math.cos(ang) * SC05


def pole_j2000(year):
    import ephem
    e = ephem.Date(f"{year}/1/1")
    b = ephem.FixedBody(); b._ra, b._dec, b._epoch = 0.0, math.radians(-89.9999), e
    o = ephem.Observer(); o.date = ephem.J2000; o.epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.a_ra), math.degrees(b.a_dec)


def crux_alt_taipei(year, hip=X.ACRUX):
    import ephem
    e = ephem.Date(f"{year}/6/1")
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(S[hip][0]), math.radians(S[hip][1]); b._epoch = ephem.J2000
    o = ephem.Observer(); o.date = e; o.epoch = e
    b.compute(o)
    return 90.0 - 25.033 + math.degrees(b.a_dec)


def c05_track(ax):
    T(ax, 0.0, 0.92, tx("c05_title"), 24, WHITE)
    box = (-0.95, 0.95, -0.05, 0.84)
    stars_plot(ax, P05, vmax=3.6, box=box, k=2.4, decmax=-30)
    segs_plot(ax, X.SEG_CRUX, P05, AMBER, lw=2.4)
    x, y = P05(*S[X.GACRUX][:2]); T(ax, x + 0.08, y + 0.02, tx("crux"), 15, AMBER, ha="left")
    circ = [X.small_circle(SEP, 23.44)][0]
    q = [P05(*p) for p in circ]
    q = [p for p in q if box[2] < p[1] < box[3]]
    ax.scatter([p[0] for p in q], [p[1] for p in q], s=1.2, c=GREY, zorder=3)
    sx, sy = P05(*SEP)
    if sy > box[2]:
        ax.scatter([sx], [sy], s=30, c=GREY, zorder=4); T(ax, sx, sy - 0.04, tx("sep"), 12, GREY, w="normal")
    for yr, k, col, dx, dy, ha in ((1, "y1", WHITE, 0.05, -0.05, "left"), (1000, "y1000", WHITE, 0.0, 0.07, "center"),
                                   (2027, "y2027", AMBER, -0.05, 0.04, "right")):
        x, y = P05(*pole_j2000(yr))
        ax.scatter([x], [y], s=110, facecolors="none", edgecolors=col, lw=2.0, zorder=6)
        T(ax, x + dx, y + dy, tx(k), 14, col, ha=ha)
    T(ax, -0.93, 0.03, tx("track"), 13, GREY, ha="left", w="normal")


def c05_alt(ax):
    T(ax, 0.0, -0.10, tx("c05_alt"), 17, WHITE)
    y0, sc = -0.78, 0.034
    ax.plot([-0.80, 0.80], [y0, y0], c=GREEN, lw=2.4, zorder=5)
    for x, yr, k in ((-0.50, 1, "y1"), (0.0, 1000, "y1000"), (0.50, 2027, "y2027")):
        a = crux_alt_taipei(yr)
        col = AMBER if yr == 2027 else WHITE
        ax.add_patch(MPoly([(x - 0.10, y0), (x + 0.10, y0), (x + 0.10, y0 + a * sc), (x - 0.10, y0 + a * sc)],
                           closed=True, fc=col, alpha=.30, ec=col, lw=1.6, zorder=4))
        ax.scatter([x], [y0 + a * sc], s=90, c=col, zorder=6)
        T(ax, x, y0 + a * sc + 0.05, tx("deg").format(a), 18, col)
        T(ax, x, y0 - 0.05, tx(k), 14, col, w="normal")
    T(ax, 0.0, -0.20, tx("ptol"), 13, GREY, w="normal")
    T(ax, 0.0, -0.93, tx("c05_foot"), 11.5, GREY, w="normal")


# ══════════════════════ 9:16 圖卡（只出中文） ══════════════════════
def ctext(ax, x, y, s, size, col=WHITE, ha="center", w="normal"):
    ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=col, ha=ha, va="center", weight=w)


ROWS2 = [  # (原文, 文化, 意思, 顏色)
    ("Toloa", "東加（Collocott 1922）", "野鴨", AMBER),
    ("Hānaiakamalama", "夏威夷", "月亮照看的孩子", AMBER),
    ("Te Kupenga", "阿努塔（Feinberg 1988）", "漁網；網柄＝南門二、馬腹一", GREEN),
    ("Sapo Kepang", "曼達爾（印尼蘇拉威西）", "歪房子；屋頂多一顆半人馬 δ", BLUE),
    ("Bola Képpang", "布吉斯（印尼蘇拉威西）", "瘸腿的房子；多一顆 μ Cru", PURPLE),
    ("Uphaigʉ／Yurara", "圖卡諾（Cardoso 2007）", "淡水龜", WHITE),
    ("Mahutonga", "毛利（Stellarium 舊版說明）", "南十字的另一個名字", WHITE),
    ("十字架", "中國（明朝末年）", "十字架一～四", AMBER),
]


def mini_crux(ax, y0, h, segsets):
    """圖卡上的小南十字（南盤投影，直立）"""
    g, m = _geo()
    objs = X.CRUX + [X.RIGIL, X.HADAR, X.DEL_CEN, X.MU_CRU]
    pts = [X.disc_xy(m, *S[o][:2], X.ROT_C) for o in objs]
    cx = (max(p[0] for p in pts) + min(p[0] for p in pts)) / 2
    cy = (max(p[1] for p in pts) + min(p[1] for p in pts)) / 2
    sc = h / (max(p[1] for p in pts) - min(p[1] for p in pts)) / 1.25

    def P(ra, dec):
        x, y = X.disc_xy(m, ra, dec, X.ROT_C)
        return 0.5 + (x - cx) * sc * 1920 / 1080, y0 + (y - cy) * sc
    for hp, (ra, dec, vm) in [(hp, S[hp][:3]) for hp in S if S[hp][2] < 5.0 and -72 < S[hp][1] < -45]:
        x, y = P(ra, dec)
        if 0.08 < x < 0.92 and y0 - h / 2 < y < y0 + h / 2:
            ax.scatter([x], [y], s=max(0.5, (5.2 - vm)) ** 1.8 * 1.5, c=WHITE, lw=0, zorder=4)
    for segs, col, dxy in segsets:
        for seg in segs:
            q = [P(*S[hh][:2]) for hh in seg]
            ax.plot([p[0] + dxy for p in q], [p[1] + dxy for p in q], c=col, lw=1.4, alpha=.85, zorder=3)
    return P


def c02_card(ax):
    ctext(ax, 0.5, 0.950, "同一個十字的名字", 28, WHITE, w="bold")
    ctext(ax, 0.5, 0.915, "南十字這一帶，各地的叫法（連線照各自的資料畫）", 13, GREY)
    P = mini_crux(ax, 0.79, 0.20, [(X.SEG_NET, GREEN, -0.004), (X.SEG_SAPO, BLUE, 0.0),
                                    (X.SEG_BOLA, PURPLE, 0.004), (X.SEG_CRUX, AMBER, 0.0)])
    for h, nm, dx in ((X.RIGIL, "南門二", -0.02), (X.HADAR, "馬腹一", -0.02)):
        x, y = P(*S[h][:2]); ctext(ax, x + dx, y - 0.015, nm, 10.5, WHITE, ha="right")
    x, y = P(*S[X.DEL_CEN][:2]); ctext(ax, x + 0.02, y, "半人馬 δ", 10, BLUE, ha="left")
    x, y = P(*S[X.MU_CRU][:2]); ctext(ax, x - 0.05, y + 0.006, "μ Cru", 10, PURPLE, ha="right")
    ax.plot([0.03, 0.97], [0.675, 0.675], c=WHITE, lw=1.0, alpha=.4)
    y = 0.668
    for nat, who, what, col in ROWS2:
        ctext(ax, 0.04, y - 0.020, nat, 15, col, ha="left", w="bold")
        ctext(ax, 0.96, y - 0.020, who, 10.5, GREY, ha="right")
        ctext(ax, 0.04, y - 0.048, what, 12.5, WHITE, ha="left")
        y -= 0.062
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ctext(ax, 0.5, y - 0.026, "指針（南門二＋馬腹一）", 14, WHITE, w="bold")
    ctext(ax, 0.5, y - 0.053, "東加：兩個人 Ongo Tangata｜毛利：Tamarereti 獨木舟的纜繩", 11, WHITE)
    ctext(ax, 0.5, y - 0.075, "卡米拉羅伊：兩隻鳳頭鸚鵡 Muraay｜夏威夷：指針", 11, WHITE)
    ctext(ax, 0.5, 0.074, "Stellarium tongan／hawaiian_starlines／anutan／mandar／bugis／maori／kamilaroi", 8.6, GREY)
    ctext(ax, 0.5, 0.056, "Collocott 1922；Feinberg 1988；Rasyid et al. 2021；Ammarell 1999；Cardoso 2007", 8.6, GREY)
    ctext(ax, 0.5, 0.030, "#萬國星空　#師大天文社", 13, WHITE)


def _card_sky(ax, y0, when, lat, lon, segsets, labels, half=0.44, az_rng=(130, 230), alt0=0.0, cen=180.0):
    """圖卡上的小天空（面向南、立體投影）：中心 x=0.5、地平線南點約在 y0"""
    f = altaz_fn(lat, lon, 8, when)
    P0 = stereo(cen, alt0, 1.0, 0.0)
    sc = half / max(abs(P0(0.0, az_rng[0])[0]), abs(P0(0.0, az_rng[1])[0]))
    P = lambda alt, az: (0.5 + P0(alt, az)[0] * sc, y0 + (P0(alt, az)[1] - P0(0.0, cen)[1]) * sc * 1080 / 1920)
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 4.4 and S[h][1] < 0]:
        alt, az = f(ra, dec)
        if alt > 0.3:
            x, y = P(alt, az)
            if 0.05 < x < 0.95 and y < y0 + 0.20:
                ax.scatter([x], [y], s=max(0.5, (4.8 - vm)) ** 1.8 * 1.3, c=WHITE, lw=0, zorder=4)
    for segs, col in segsets:
        for seg in segs:
            q = [P(*f(*S[h][:2])) for h in seg]
            ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=1.8, zorder=5)
    hz = [P(0.0, az) for az in range(az_rng[0] - 10, az_rng[1] + 11)]
    ax.add_patch(MPoly(hz + [(hz[-1][0], y0 - 0.05), (hz[0][0], y0 - 0.05)], closed=True, fc=BG, ec="none",
                       zorder=6))
    ax.plot([p[0] for p in hz], [p[1] for p in hz], c=GREEN, lw=1.6, zorder=7)
    for az, k in ((135, "東南"), (180, "南"), (225, "西南")):
        x, y = P(0.0, az)
        if 0.04 < x < 0.96:
            ctext(ax, x, y - 0.014, k, 11, GREEN)
    for (ra, dec), txt, dx, dy, col in labels:
        x, y = P(*f(ra, dec))
        ctext(ax, x + dx, y + dy, txt, 12, col)
    return f


def c04_card(ax):
    ctext(ax, 0.5, 0.950, "台灣怎麼分：真十字與假十字", 24, WHITE, w="bold")
    ctext(ax, 0.5, 0.915, "墾丁・面向正南（南方海面要開闊）", 13, GREY)
    ax.plot([0.03, 0.97], [0.895, 0.895], c=WHITE, lw=1.0, alpha=.4)
    ctext(ax, 0.04, 0.870, "3 月底　晚上 9 點", 16, AMBER, ha="left", w="bold")
    cen = lambda hs: X.radec([sum(X.vec(*S[h][:2])[i] for h in hs) for i in range(3)])
    _card_sky(ax, 0.610, "2027/3/26 21:00", *X.KT, [(X.SEG_FCR, RED), (X.SEG_CRUX, AMBER)],
              [(cen(X.FCR), "假十字", 0.0, 0.045, RED), (S[X.GACRUX][:2], "南十字剛升起", 0.07, 0.035, AMBER)])
    ctext(ax, 0.04, 0.535, "假十字立在正南方，離地平線 8–13°；真的南十字才剛要從東南方升起。", 11.5, WHITE, ha="left")
    ax.plot([0.03, 0.97], [0.508, 0.508], c=WHITE, lw=0.8, alpha=.3)
    ctext(ax, 0.04, 0.483, "4 月中　晚上 9 點半", 16, AMBER, ha="left", w="bold")
    _card_sky(ax, 0.225, "2027/4/15 21:30", *X.KT, [(X.SEG_FCR, RED), (X.SEG_CRUX, AMBER)],
              [(cen(X.FCR), "右：假十字", 0.03, 0.050, RED), (cen(X.CRUX), "左：南十字", -0.03, 0.050, AMBER)])
    ctext(ax, 0.04, 0.150, "兩個十字並排在南方低空：右邊大的是假的，左邊小的才是真的。", 12.5, WHITE, ha="left", w="bold")
    ctext(ax, 0.04, 0.124, "真十字：小、十字裡有第五顆小星、左邊有兩顆很亮的指針（南門二、馬腹一）。", 10.5, WHITE, ha="left")
    ctext(ax, 0.04, 0.100, "墾丁視角；台北此時海石一已落。4/15 月亮 68% 在西方高空，避開月光或改在 4 月下旬看。", 9.6, GREY,
          ha="left")
    ctext(ax, 0.5, 0.066, "高度：PyEphem 自算（含大氣折射）；連線：Stellarium modern（假十字）", 9.6, GREY)
    ctext(ax, 0.5, 0.030, "#萬國星空　#師大天文社", 13, WHITE)


def c06_card(ax):
    ctext(ax, 0.5, 0.950, "今晚看南十字", 28, WHITE, w="bold")
    ctext(ax, 0.5, 0.915, "2027/5/14（五）21:00　南十字直立在正南方", 14, AMBER)
    ax.plot([0.03, 0.97], [0.893, 0.893], c=WHITE, lw=1.0, alpha=.4)
    f = _card_sky(ax, 0.540, "2027/5/14 21:00", *X.KT, [(X.SEG_CRUX, AMBER)],
                  [(S[X.GACRUX][:2], "十字架一 10.9°", 0.11, 0.0, AMBER), (S[X.ACRUX][:2], "十字架二 5.0°", 0.11, -0.005, AMBER),
                   (S[X.RIGIL][:2], "南門二", -0.02, -0.018, WHITE), (S[X.HADAR][:2], "馬腹一", 0.0, 0.020, WHITE)],
                  half=0.40, az_rng=(150, 210))
    ctext(ax, 0.04, 0.860, "墾丁、蘭嶼（面向正南）", 15, AMBER, ha="left", w="bold")
    rows = [("墾丁、蘭嶼", "十字架一 10.9°、十字架二 5.0°；20:00–22:00 最高", AMBER),
            ("", "左下：南門二、馬腹一；南方海面要開闊", WHITE),
            ("台北", "十字架一 7.8°、十字架二 2.0°：整組在 8° 以下，很難看到", WHITE),
            ("月光", "65%，在西南方高 57°（01:28 落下）：往南看時找東西擋住", WHITE),
            ("季節", "晚上 9 點看整個十字：4 月中到 6 月初（墾丁）", WHITE)]
    y = 0.470
    for k, v, col in rows:
        if k:
            ax.plot([0.03, 0.97], [y + 0.012, y + 0.012], c=WHITE, lw=0.6, alpha=.2)
            ctext(ax, 0.04, y - 0.012, k, 13.5, col, ha="left", w="bold")
            y -= 0.040
        ctext(ax, 0.06, y, v, 11.8, WHITE, ha="left")
        y -= 0.040
    ctext(ax, 0.5, y - 0.020, "怎麼認：小、第五顆小星、兩顆指針、旁邊一塊黑（煤袋）", 12, AMBER, w="bold")
    ctext(ax, 0.5, 0.066, "高度與時刻：PyEphem 自算（含大氣折射）", 9.6, GREY)
    ctext(ax, 0.5, 0.030, "#萬國星空　#師大天文社", 13, WHITE)


# ══════════════════════ 主程式 ══════════════════════
_MM = {}


def _M():
    if "m" not in _MM:
        from gen_master_canvas import Master
        tmp = os.path.join(OUT, "_tmp")
        _MM["m"] = Master("X-05", S, tmp, lst=X.LST0, D_s=50, D_r=54, D_fill=-20.0,
                          w_c=34, feather=8, x_tN=0.0, x_tS=0.0, maglim=5.5)
        try:
            os.rmdir(tmp)
        except OSError:
            pass
    return _MM["m"]


def check():
    """核對逐字稿數字（印出來比對）"""
    f, Pp = _c03()
    g, m = _geo()
    print(f"  06 鏡（南緯 21°、假十字上中天）：δ→ι {f(*g['f1'][-1])[1]:.1f}°、κ→ε {f(*g['f2'][-1])[1]:.1f}°、"
          f"南十字同法 {f(*g['crux_ext'][-1])[1]:.1f}°（逐字稿 155.7／221.9／182.9）")
    print("  11 鏡（台北十字架二上中天幾何高度）：" +
          "、".join(f"{y} 年 {crux_alt_taipei(y):.1f}°" for y in (1, 1000, 2027)) + "（逐字稿 12.9／7.4／1.7）")
    for when, ll, nm in (("2027/3/26 21:00", X.KT, "墾丁 3/26"), ("2027/4/15 21:30", X.KT, "墾丁 4/15"),
                         ("2027/5/14 21:00", X.KT, "墾丁 5/14"), ("2027/5/14 21:00", X.TPE, "台北 5/14")):
        fa = altaz_fn(*ll, 8, when)
        print(f"  {nm} {when[-5:]}: " + "　".join(
            f"{n} {fa(*S[h][:2])[0]:.1f}°/{fa(*S[h][:2])[1]:.0f}°" for h, n in
            ((X.GACRUX, "十字架一"), (X.ACRUX, "十字架二"), (X.DEL_VEL, "天社三"), (X.KAP_VEL, "天社五"),
             (X.EPS_CAR, "海石一"), (X.IOT_CAR, "海石二"))))


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    else:
        os.makedirs(OUT, exist_ok=True)
        check()
    C.emit("", [("延長", c01_ext), ("中垂線", c01_bis), ("地平線", c01_hz)], title="C-X05-01_找南方的兩條線")
    C.emit("", [("真南", c03_true), ("假十字", c03_false)], title="C-X05-03_認錯十字")
    C.emit("", [("軌跡", c05_track), ("高度", c05_alt)], title="C-X05-05_歲差")
    if LANG != "zh":
        return
    f, ax = C.newcard(dark=True); c02_card(ax)
    C.save(f, "", "C-X05-02_南十字的名字_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True); c04_card(ax)
    C.save(f, "", "C-X05-04_台灣怎麼分_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True); c06_card(ax)
    C.save(f, "", "C-X05-06_今晚看南十字_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
