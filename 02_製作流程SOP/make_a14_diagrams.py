# -*- coding: utf-8 -*-
"""A-14 因紐特：極夜裡的星鐘｜概念圖（C 系列骨架）

C-A14-01 極夜（地平層、台北層、Igloolik層、極夜層）：冬至正午太陽高度 台北 +41.5° vs Igloolik −2.8°；
         2026–27 Igloolik 太陽 11/29 最後一次露臉 → 1 月中回來
C-A14-02 星鐘（傍晚層、後半夜層、清晨層）：鎖骨 Quturjuuk 在 Igloolik 傍晚斜、後半夜擺平、清晨斜向另一邊
C-A14-03 Aagjuuk初見（地平層、十二月初層、第二週層、冬至層）：太陽在地平線下 12° 的同一個黎明時刻，
         牛郎星一天比一天高——十二月第二週第一次清楚露臉
C-A14-04 太陽回來（油燈層、半邊笑層）：吹熄油燈、換燈芯、從同一把新火點亮；半邊臉笑
C-A14-05 因紐特星名小辭典（9:16 圖卡）
C-A14-06 這週末抬頭看（9:16 圖卡；台北 2026/12/19）
C-A14-魚叉（1080×1920 滿版透明：04 迄格～06 迄格疊在北盤上，魚叉對準盤心＝北極星）

天象全部 PyEphem 自算（Igloolik 69.37°N 81.80°W UTC−5，−30°C／1010 hPa；台北 15°C）；
口述與名稱：John MacDonald《The Arctic Sky》（1998）。
執行：python3 make_a14_diagrams.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-14_因紐特/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
GROUND = "#141A2E"
S = None
IGL = (69.3667, -81.8, 30, -5, -30)          # lat, lon, elev, tz, °C
TPE = (25.0330, 121.5654, 0, 8, 15)
HIP = dict(Altair=97649, Tarazed=97278, Capella=24608, Menkalinan=28360, Castor=36850, Pollux=37826,
           Vega=91262, Aldebaran=21421, Alnilam=26311, Alnitak=26727, Mintaka=25930, Betelgeuse=27989,
           Rigel=24436, Dubhe=54061, Merak=53910, Polaris=11767, Alcyone=17702)


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, rot=0, va="center", alpha=1.0):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, rotation=rot, rotation_mode="anchor", alpha=alpha)


def observer(site, local):
    import ephem
    lat, lon, el, tz, temp = site
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = el
    o.pressure = 1010; o.temp = temp
    o.date = ephem.Date(ephem.Date(local) - tz * ephem.hour)
    return o


def body(ra, dec):
    import ephem
    b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec); b._epoch = ephem.J2000
    return b


def altaz(o, h):
    ra, dec, v = S[HIP[h] if isinstance(h, str) else h]
    b = body(ra, dec); b.compute(o)
    return math.degrees(float(b.alt)), math.degrees(float(b.az))


def sun_morning(site, ds, target=-12.0):
    """當地早上太陽升到 target 度的那一刻（Observer）"""
    import ephem
    o = observer(site, ds + " 04:00"); s = ephem.Sun(); t0 = o.date; prev = None
    for i in range(10 * 60):
        o.date = ephem.Date(t0 + i * ephem.minute); s.compute(o); a = math.degrees(float(s.alt))
        if prev is not None and prev < target <= a:
            return o, math.degrees(float(s.az))
        prev = a
    raise RuntimeError(ds)


def noon_alt(site):
    import ephem
    o = observer(site, "2026/12/21 12:00"); o.pressure = 0
    s = ephem.Sun(); o.date = o.next_transit(s, start=ephem.Date(o.date - 0.5)); s.compute(o)
    return math.degrees(float(s.alt))


def sun_icon(ax, x, y, r, alpha=1.0, z=7, dashed=False):
    for k, op in ((2.4, 0.06), (1.7, 0.12)):
        ax.add_patch(CB.Circle((x, y), r * k, fc=AMBER, ec="none", alpha=op * alpha, zorder=z - 1))
    ax.add_patch(CB.Circle((x, y), r, fc=AMBER if not dashed else "none", ec=AMBER, lw=2.0,
                           ls=(0, (3, 3)) if dashed else "-", alpha=alpha, zorder=z))


# ══════════════════════ C-A14-01 極夜 ══════════════════════
HZ1 = -0.18
PANELS = {"台北": (-0.95, -0.03), "Igloolik": (0.03, 0.95)}


def c01_horizon(ax):
    T(ax, 0.0, 0.93, "冬至中午，太陽在哪裡？", 30, WHITE)
    T(ax, 0.0, 0.855, "2026/12/21，面向正南", 15, GREY, w="normal")
    for nm, (x0, x1) in PANELS.items():
        ax.add_patch(CB.Rectangle((x0, HZ1 - 0.20), x1 - x0, 0.20, fc=GROUND, ec="none", zorder=3))
        ax.plot([x0, x1], [HZ1, HZ1], c=WHITE, lw=2.2, alpha=.85, zorder=4)
        ctext(ax, (x0 + x1) / 2, HZ1 - 0.08, "南", 16, WHITE)
        lat = "25°N" if nm == "台北" else "69°N"
        ctext(ax, (x0 + x1) / 2, 0.72, f"{nm}　{lat}", 19, WHITE)
        ax.scatter([x0 + 0.10], [HZ1], s=60, c=WHITE, zorder=6)
    ax.plot([0.0, 0.0], [HZ1 - 0.20, 0.66], c=GREY, lw=1.0, alpha=.4, zorder=2)


def _sight(ax, x0, alt, length, col, label, dashed=False):
    a = math.radians(alt)
    xs, ys = x0 + 0.10, HZ1
    xe, ye = xs + length * math.cos(a), ys + length * math.sin(a)
    ax.plot([xs, xe], [ys, ye], c=col, lw=1.6, alpha=.75, ls=(0, (4, 4)), zorder=5)
    r = 0.16
    th = [math.radians(alt * i / 30) for i in range(31)]
    ax.plot([xs + r * math.cos(t) for t in th], [ys + r * math.sin(t) for t in th], c=col, lw=1.4, zorder=5)
    sun_icon(ax, xe, ye, 0.045, alpha=(0.55 if dashed else 1.0), dashed=dashed)
    return xe, ye


def c01_taipei(ax):
    alt = noon_alt(TPE)
    x0 = PANELS["台北"][0]
    xe, ye = _sight(ax, x0, alt, 0.62, AMBER, "")
    ctext(ax, x0 + 0.33, HZ1 + 0.075, f"{alt:.1f}°", 16, AMBER)
    ctext(ax, (PANELS["台北"][0] + PANELS["台北"][1]) / 2, 0.60, "太陽有四十一度高", 14, AMBER)


def c01_igloolik(ax):
    alt = noon_alt(IGL)
    x0, x1 = PANELS["Igloolik"]
    clip = CB.Rectangle((x0, HZ1), x1 - x0, 0.80, fc="none", ec="none")
    ax.add_patch(clip)
    for k in range(7):                        # 地平線上方的微光（裁在面板內、地平線以上）
        e = CB.Ellipse((x0 + 0.62, HZ1), 1.60 - 0.18 * k, 0.30 - 0.035 * k, fc=AMBER, ec="none", alpha=0.05,
                       zorder=2)
        ax.add_patch(e); e.set_clip_path(clip)
    xe, ye = _sight(ax, x0, alt, 0.62, AMBER, "", dashed=True)
    ctext(ax, x0 + 0.44, HZ1 - 0.13, f"{alt:.1f}°（在地平線下）".replace("-", "−"), 13, AMBER, z=10)
    ctext(ax, (x0 + x1) / 2, 0.60, "太陽躲在地平線下", 14, AMBER)
    ctext(ax, (x0 + x1) / 2, 0.53, "中午前後，南邊天空只透出微光", 11.5, WHITE, w="normal")


def c01_night(ax):
    import datetime
    y = -0.60
    d0, d1 = datetime.date(2026, 11, 15), datetime.date(2027, 1, 31)
    span = (d1 - d0).days

    def X(d):
        return -0.86 + 1.72 * (d - d0).days / span
    box(ax, -0.95, -0.92, 1.90, 0.52, ec=GREY, fc=PANEL, lw=1.2, alpha=0.92, z=7)
    ctext(ax, 0.0, -0.455, "Igloolik 的極夜：Tauvikjuaq（大黑暗）", 15, WHITE, z=10)
    ax.add_patch(CB.Rectangle((-0.86, y - 0.03), 1.72, 0.06, fc="#2A3150", ec="none", zorder=8))
    a, b = X(datetime.date(2026, 11, 29)), X(datetime.date(2027, 1, 12))
    ax.add_patch(CB.Rectangle((a, y - 0.03), b - a, 0.06, fc="#05070F", ec=BLUE, lw=1.4, zorder=9))
    ctext(ax, (X(datetime.date(2026, 12, 22)) + b) / 2, y, "太陽不升起：約一個半月", 12, BLUE, z=10)
    for d, lab, col, dy in [(datetime.date(2026, 11, 29), "11/29\n最後一次露臉", WHITE, -0.085),
                            (datetime.date(2026, 12, 18), "12/18\n今天", RED, 0.08),
                            (datetime.date(2026, 12, 22), "12/22\n冬至", AMBER, -0.085),
                            (datetime.date(2027, 1, 12), "1/12–14\n回來", WHITE, -0.085)]:
        x = X(d)
        ax.plot([x, x], [y - 0.035, y + 0.035], c=col, lw=2.0, zorder=10)
        ax.text(x, y + dy, lab, fontproperties=CB.FP, fontsize=10.5, color=col, ha="center",
                va="center", weight="bold", zorder=10, linespacing=1.15)
    ctext(ax, 0.0, -0.81, "回來的日子看氣溫：愈冷，大氣折射愈強，太陽愈早露臉（1/12–14）", 10, GREY, w="normal", z=10)
    ctext(ax, 0.0, -0.865, "PyEphem 自算（Igloolik 69.37°N，−30°C）；MacDonald《The Arctic Sky》p.101、107", 9,
          GREY, w="normal", z=10)


# ══════════════════════ C-A14-02 星鐘（鎖骨） ══════════════════════
QUT = ["Capella", "Menkalinan", "Castor", "Pollux"]
CLOCK = [("2026/12/18 18:00", "傍晚 6 點", "斜向一邊", -0.62),
         ("2026/12/19 01:00", "凌晨 1 點", "擺平了", 0.0),
         ("2026/12/19 06:00", "清晨 6 點", "斜向另一邊", 0.62)]
DIRS = [(0, "北"), (45, "東北"), (90, "東"), (135, "東南"), (180, "南"), (225, "西南"), (270, "西"),
        (315, "西北"), (360, "北")]
DIRS16 = DIRS + [(22.5, "北北東"), (67.5, "東北東"), (112.5, "東南東"), (157.5, "南南東"), (202.5, "南南西"),
                 (247.5, "西南西"), (292.5, "西北西"), (337.5, "北北西")]


def dir_name(az):
    return min(DIRS16, key=lambda d: abs(d[0] - az))[1]


def gnomonic(o, names, center):
    """切平面投影，切點＝center 那兩顆的中點（那裡的「水平」才準）：右＝方位增加、上＝天頂方向"""
    vec = {}
    for n in names:
        alt, az = altaz(o, n)
        a, z = math.radians(alt), math.radians(az)
        vec[n] = (math.cos(a) * math.sin(z), math.cos(a) * math.cos(z), math.sin(a), alt, az)
    c = [sum(vec[n][i] for n in center) for i in range(3)]
    nc = math.sqrt(sum(x * x for x in c)); c = [x / nc for x in c]
    zc = c[2]
    u = [-zc * c[0], -zc * c[1], 1 - zc * c[2]]
    nu = math.sqrt(sum(x * x for x in u)); u = [x / nu for x in u]
    r = [c[1] * u[2] - c[2] * u[1], c[2] * u[0] - c[0] * u[2], c[0] * u[1] - c[1] * u[0]]
    out = {}
    for n, v in vec.items():
        d = v[0] * c[0] + v[1] * c[1] + v[2] * c[2]
        out[n] = ((v[0] * r[0] + v[1] * r[1] + v[2] * r[2]) / d,
                  (v[0] * u[0] + v[1] * u[1] + v[2] * u[2]) / d, v[3], v[4])
    calt = math.degrees(math.asin(zc))
    caz = math.degrees(math.atan2(c[0], c[1])) % 360
    return out, calt, caz


def _clock(ax, i):
    when, tlab, verdict, xc = CLOCK[i]
    o = observer(IGL, when)
    P, calt, caz = gnomonic(o, QUT, ("Capella", "Menkalinan"))
    xs = [p[0] for p in P.values()]; ys = [p[1] for p in P.values()]
    sc = min(0.40 / (max(xs) - min(xs) + 1e-9), 0.55 / (max(ys) - min(ys) + 1e-9), 1.25)
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    yc = 0.06
    pts = {n: (xc + (p[0] - mx) * sc, yc + (p[1] - my) * sc) for n, p in P.items()}
    box(ax, xc - 0.29, -0.50, 0.58, 1.18, ec=GREY, fc="#0E1428", lw=1.0, z=1, alpha=0.9)
    ctext(ax, xc, 0.59, tlab, 16, WHITE)
    ctext(ax, xc, 0.53, f"五車二在{dir_name(caz)}方，{calt:.0f}° 高", 11.5, GREY, w="normal")
    # 水平參考線（穿過五車二那一對的中點）
    hy = (pts["Capella"][1] + pts["Menkalinan"][1]) / 2
    ax.plot([xc - 0.25, xc + 0.25], [hy, hy], c=WHITE, lw=1.0, alpha=.35, ls=(0, (4, 4)), zorder=3)
    ctext(ax, xc - 0.255, hy + 0.022, "水平", 8.5, GREY, w="normal", ha="left")
    for a, b, lw, al in [("Capella", "Menkalinan", 4.5, 0.95), ("Castor", "Pollux", 2.0, 0.55)]:
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=GREEN, lw=lw, alpha=al, zorder=5,
                solid_capstyle="round")
    for n, (x, y) in pts.items():
        v = S[HIP[n]][2]
        ax.scatter([x], [y], s=max(14, (5.6 - v) ** 2.2 * 5.5), c=WHITE, zorder=6, lw=0)
    for n, lab, dy in [("Capella", "五車二", -0.045), ("Castor", "北河二", -0.045)]:
        x, y = pts[n]
        ctext(ax, x, y + dy, lab, 9, WHITE, w="normal", z=7)
    ax.annotate("", xy=(xc - 0.24, 0.47), xytext=(xc - 0.24, 0.39),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ctext(ax, xc - 0.215, 0.43, "天頂", 8.5, GREY, w="normal", ha="left")
    ctext(ax, xc, -0.42, verdict, 17, AMBER)


def c02_dusk(ax):
    T(ax, 0.0, 0.93, "鎖骨時鐘：Quturjuuk", 30, WHITE)
    T(ax, 0.0, 0.855, "Igloolik，12/18 傍晚 → 12/19 清晨；看最亮的五車二那一對", 14, GREY, w="normal")
    _clock(ax, 0)
    ctext(ax, 0.0, -0.66, "Amaaq（Igloolik 長老）：傍晚斜一邊，後來像擺直了；天快亮時，又斜向另一邊", 12.5,
          WHITE, w="normal")
    ctext(ax, 0.0, -0.73, "北河二、北河三那一對（細線）一整夜都斜著；指針是五車二那一對", 11, GREY, w="normal")
    ctext(ax, 0.0, -0.80, "MacDonald《The Arctic Sky》p.200；位置與傾角 PyEphem 自算", 9.5, GREY, w="normal")


def c02_night(ax):
    _clock(ax, 1)


def c02_dawn(ax):
    _clock(ax, 2)


# ══════════════════════ C-A14-03 Aagjuuk 初見 ══════════════════════
AZ0, AZ1, ALT1 = 45.0, 135.0, 14.0
PX0, PX1, PY0, PY1 = -0.90, 0.90, -0.20, 0.52
FIRST = [("2026/12/01", "12/1", "還貼著地平線：看不出來", GREY, "十二月初"),
         ("2026/12/12", "12/12", "第二週：Aagjuuk 出來了！", AMBER, "第二週"),
         ("2026/12/22", "12/22", "冬至：又更高了", WHITE, "冬至")]


def _q(alt, az):
    return (PX0 + (az - AZ0) / (AZ1 - AZ0) * (PX1 - PX0), PY0 + alt / ALT1 * (PY1 - PY0))


def c03_horizon(ax):
    T(ax, 0.0, 0.93, "同一個黎明時刻，牛郎星一天比一天高", 26, WHITE)
    T(ax, 0.0, 0.855, "Igloolik，太陽在地平線下 12°（天邊開始亮）那一刻，往東看", 14, GREY, w="normal")
    o, saz = sun_morning(IGL, "2026/12/12")
    x, _ = _q(0, min(saz, AZ1 - 2))
    clip = CB.Rectangle((PX0, PY0), PX1 - PX0, 0.9, fc="none", ec="none")
    ax.add_patch(clip)
    for k in range(8):
        e = CB.Ellipse((x, PY0), 1.3 - 0.13 * k, 0.07 + 0.05 * k, fc=AMBER, ec="none", alpha=0.05, zorder=2)
        ax.add_patch(e); e.set_clip_path(clip)
    ax.add_patch(CB.Rectangle((PX0, PY0 - 0.12), PX1 - PX0, 0.12, fc=GROUND, ec="none", zorder=3))
    ax.plot([PX0, PX1], [PY0, PY0], c=WHITE, lw=2.2, alpha=.85, zorder=4)
    for az, lab in ((45, "東北"), (67.5, "東北東"), (90, "東"), (112.5, "東南東"), (135, "東南")):
        xx, _ = _q(0, az)
        ctext(ax, xx, PY0 - 0.055, lab, 12, WHITE, w="normal")
    for alt in (5, 10):
        _, yy = _q(alt, AZ0)
        ax.plot([PX0, PX1], [yy, yy], c=WHITE, lw=0.6, alpha=.2, ls=(0, (3, 4)), zorder=2)
        ax.text(PX0 + 0.01, yy + 0.012, f"{alt}°", fontproperties=CB.FP, fontsize=9, color=GREY, zorder=3)
    ctext(ax, x - 0.06, PY0 + 0.05, "太陽在這下面", 10.5, AMBER, w="normal", ha="right")


def _first(ax, i):
    ds, short, lab, col, _ = FIRST[i]
    o, saz = sun_morning(IGL, ds)
    pa = [_q(*altaz(o, n)) for n in ("Altair", "Tarazed")]
    ax.plot([pa[0][0], pa[1][0]], [pa[0][1], pa[1][1]], c=col, lw=2.4, alpha=.9, zorder=6)
    for (x, y), s in zip(pa, (220, 90)):
        ax.scatter([x], [y], s=s, c=WHITE if col != GREY else GREY, zorder=7, lw=0)
    x, y = pa[1]
    ctext(ax, x + 0.03, y + 0.07, short, 15, col, ha="left", z=10)
    alt = altaz(o, "Altair")[0]
    ctext(ax, x + 0.03, y + 0.025, f"{lab}（{alt:.1f}°）", 11.5, col, w="normal", ha="left", z=10)


def c03_dec1(ax):
    _first(ax, 0)


def c03_week2(ax):
    _first(ax, 1)
    box(ax, -0.90, -0.80, 1.80, 0.40, ec=GREY, fc=PANEL, lw=1.2, alpha=0.92, z=8)
    ctext(ax, 0.0, -0.46, "aagjuliqtuq：「Aagjuuk 出來了」→ 一天的活開始", 15, AMBER, z=10)
    ctext(ax, 0.0, -0.53, "孩子們天沒亮就被叫出門看；牛郎星每天早 4 分鐘升起，同一個時刻就高一點", 11.5,
          WHITE, w="normal", z=10)


def c03_solstice(ax):
    _first(ax, 2)
    ctext(ax, 0.0, -0.61, "1990/12/19：長老 Jacobie Avingnaq 在社區廣播宣布「冬至到了」——因為他看見了 Aagjuuk", 11,
          GREEN, w="normal", z=10)
    ctext(ax, 0.0, -0.68, "也是辦冬至慶典 tivajuut、髭海豹靠岸的時候", 11, WHITE, w="normal", z=10)
    ctext(ax, 0.0, -0.75, "MacDonald《The Arctic Sky》p.44–51；位置 PyEphem 自算（Igloolik，−30°C）", 9.5, GREY,
          w="normal", z=10)


# ══════════════════════ C-A14-04 太陽回來 ══════════════════════
def qulliq(ax, x, y, s, flame=0, smoke=False, wick=False):
    """海豹油燈 qulliq：半月形淺石盤（側視），沿直邊一排小火"""
    pts = [(x - 0.20 * s, y)]
    for i in range(41):
        t = math.pi * i / 40
        pts.append((x - 0.20 * s * math.cos(t), y - 0.07 * s * math.sin(t)))
    pts.append((x + 0.20 * s, y))
    ax.add_patch(CB.Polygon(pts, closed=True, fc="#8F9AAF", ec=WHITE, lw=1.4, zorder=5))
    ax.add_patch(CB.Rectangle((x - 0.19 * s, y - 0.004), 0.38 * s, 0.012 * s, fc="#D9C08A", ec="none", zorder=6))
    if wick:
        ax.plot([x - 0.17 * s, x + 0.17 * s], [y + 0.012 * s, y + 0.012 * s], c=GREEN, lw=3.0 * s, zorder=7,
                solid_capstyle="round")
    if flame:
        for k in range(flame):
            fx = x - 0.15 * s + 0.30 * s * k / max(1, flame - 1)
            fl = [(fx - 0.012 * s, y + 0.012 * s), (fx, y + 0.07 * s), (fx + 0.012 * s, y + 0.012 * s)]
            ax.add_patch(CB.Polygon(fl, closed=True, fc=AMBER, ec="none", alpha=.95, zorder=8))
            ax.add_patch(CB.Circle((fx, y + 0.03 * s), 0.03 * s, fc=AMBER, ec="none", alpha=.12, zorder=7))
    if smoke:
        for k in range(3):
            fx = x - 0.10 * s + 0.10 * s * k
            ys = [y + 0.02 * s + 0.13 * s * i / 30 for i in range(31)]
            ax.plot([fx + 0.014 * s * math.sin(70 * (v - y) / s + k) for v in ys], ys, c=GREY, lw=1.6, alpha=.65,
                    zorder=7)


def c04_lamps(ax):
    T(ax, 0.0, 0.93, "太陽回來的那一天", 30, WHITE)
    T(ax, 0.0, 0.855, "Igloolik，一月中（Piugaattuk、Aqatsiaq 口述）", 14, GREY, w="normal")
    xs = [-0.62, 0.0, 0.62]
    qulliq(ax, xs[0], 0.48, 1.25, smoke=True)
    qulliq(ax, xs[1], 0.48, 1.25, wick=True)
    qulliq(ax, xs[2], 0.48, 1.25, flame=7)
    for x0, x1 in ((xs[0] + 0.26, xs[1] - 0.26), (xs[1] + 0.26, xs[2] - 0.26)):
        CB.arrow(ax, (x1, 0.47), (x0, 0.47), c=WHITE, lw=2.0, alpha=.7)
    for x, a, b in [(xs[0], "① 吹熄", "孩子們挨家挨戶跑"), (xs[1], "② 換新燈芯", "舊的燈芯拿掉"),
                    (xs[2], "③ 重新點亮", "全村從同一把新火")]:
        ctext(ax, x, 0.30, a, 15, AMBER)
        ctext(ax, x, 0.245, b, 11.5, WHITE, w="normal")
    ctext(ax, 0.0, 0.16, "一切重新開始——長老說，這樣春天的太陽會更暖", 13, GREEN)


def c04_smile(ax):
    cx, cy, r = 0.0, -0.30, 0.25
    th = [2 * math.pi * i / 120 for i in range(121)]
    ax.plot([cx + r * math.cos(t) for t in th], [cy + r * 1.08 * math.sin(t) for t in th], c=WHITE, lw=3.0, zorder=6)
    for ex in (-0.09, 0.09):
        ax.plot([cx + ex - 0.035, cx + ex + 0.035], [cy + 0.08, cy + 0.08], c=WHITE, lw=3.0, zorder=6,
                solid_capstyle="round")
    # 嘴：觀眾左邊（他的右邊）平的；觀眾右邊（他的左邊）上揚
    ax.plot([cx - 0.12, cx], [cy - 0.10, cy - 0.10], c=WHITE, lw=3.4, zorder=6, solid_capstyle="round")
    xs = [cx + 0.13 * i / 30 for i in range(31)]
    ax.plot(xs, [cy - 0.10 + 0.07 * (i / 30) ** 2 for i in range(31)], c=AMBER, lw=3.4, zorder=6,
            solid_capstyle="round")
    ctext(ax, cx + 0.34, cy + 0.02, "這半邊笑", 15, AMBER, ha="left")
    ctext(ax, cx + 0.34, cy - 0.04, "歡迎溫暖回來", 12, AMBER, w="normal", ha="left")
    ctext(ax, cx - 0.34, cy + 0.02, "這半邊不笑", 15, WHITE, ha="right")
    ctext(ax, cx - 0.34, cy - 0.04, "冷，還沒過完", 12, WHITE, w="normal", ha="right")
    ctext(ax, 0.0, -0.67, "第一個看見太陽的人，只能用半邊臉笑（Piugaattuk：用左半邊）", 12.5, WHITE, w="normal")
    ctext(ax, 0.0, -0.74, "Ijjangiaq：一邊歡迎溫暖，板著的那一邊承認——還會冷上好一陣子", 11, GREY, w="normal")
    ctext(ax, 0.0, -0.81, "MacDonald《The Arctic Sky》p.109–112", 9.5, GREY, w="normal")


# ══════════════════════ C-A14-05 因紐特星名小辭典（9:16） ══════════════════════
GLOSS = [("報時的星 qausiut「天亮的指標」", None, None, AMBER),
         ("Aagjuuk", "牛郎星＋河鼓三", "十二月第二週第一次在黎明出現＝冬至；天天報曉", WHITE),
         ("Akuttujuuk", "參宿四＋參宿五", "「相隔很遠的兩顆」：天黑前就看得到＝白天變長", WHITE),
         ("Quturjuuk", "五車二＋五車三、北河二＋北河三", "鎖骨：傍晚斜、後半夜平、清晨斜向另一邊", WHITE),
         ("Tukturjuit", "北斗七星", "馴鹿：快到半夜，用後腳站起來", WHITE),
         ("Amaruqjuit", "牧夫座三顆（Pelly Bay）", "追著馴鹿的狼群", WHITE),
         ("Nuutuittuq", "北極星", "從來不動的：在 Igloolik 快七十度高", WHITE),
         ("Sivulliik", "大角＋牧夫 η", "在前面的兩顆：「倒過來掛了，該起床」", WHITE),
         ("長夜的故事", None, None, AMBER),
         ("Ullaktut", "獵戶腰帶", "奔跑的人：追北極熊上了天", WHITE),
         ("Nanurjuk", "畢宿五", "北極熊（像北極熊的）", WHITE),
         ("Qimmiit", "畢宿 V 字", "狗群", WHITE),
         ("Kingulliq", "參宿七／織女星", "落在後面的（掉手套的獵人／老奶奶）", WHITE),
         ("Singuuriq", "天狼星", "閃個不停的：最高只有 4°", WHITE),
         ("Sikuliarsiujuittuq", "南河三", "不敢走上新冰的人（被殺害的大個子）", WHITE),
         ("Qangiamariik", "獵戶座大星雲", "姪兒們：替獵人送衣服的孩子", WHITE),
         ("冰屋裡的家當", None, None, AMBER),
         ("Pituaq", "仙后三顆亮星", "油燈的燈架", WHITE),
         ("Ursuutaattiaq", "仙后 W", "裝海豹油的皮袋", WHITE),
         ("Sakiattiak", "昴宿", "胸骨", WHITE),
         ("Aviguti", "銀河", "分隔線", WHITE)]


def c05_card(ax):
    ctext(ax, 0.5, 0.962, "因紐特星名小辭典", 28, WHITE)
    ctext(ax, 0.5, 0.930, "Igloolik 長老口述（拼法照 MacDonald《The Arctic Sky》）", 11.5, GREY, w="normal")
    y = 0.893
    for nat, west, zh, col in GLOSS:
        if west is None:
            y -= 0.006
            ctext(ax, 0.06, y, nat, 13.5, col, ha="left")
            ax.plot([0.06, 0.94], [y - 0.014, y - 0.014], c=col, lw=1.0, alpha=.5)
            y -= 0.036
            continue
        ctext(ax, 0.06, y + 0.008, nat, 12.5, AMBER, w="bold", ha="left")
        ctext(ax, 0.06, y - 0.011, west, 9, GREY, w="normal", ha="left")
        ctext(ax, 0.40, y - 0.002, zh, 10.5, col, w="normal", ha="left")
        y -= 0.0385
    ctext(ax, 0.5, 0.072, "Tauvikjuaq 大黑暗（極夜）　｜　qauppat 明天＝「如果天亮的話」", 11, GREEN, w="normal")
    ctext(ax, 0.5, 0.045, "Stellarium inuit 依同一本書改編；部分拼法不同（Akkuttujuuk、Qimmiitt…）", 8.5, GREY, w="normal")
    ctext(ax, 0.5, 0.018, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


# ══════════════════════ C-A14-06 這週末抬頭看（9:16） ══════════════════════
def sky_panel(ax, y0, y1, az0, az1, alt1, when, title, marks, lines=()):
    o = observer(TPE, when)
    xa, xb = 0.06, 0.94

    def q(alt, az):
        return xa + (az - az0) / (az1 - az0) * (xb - xa), y0 + alt / alt1 * (y1 - y0)
    box(ax, 0.04, y0 - 0.055, 0.92, (y1 - y0) + 0.10, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ctext(ax, 0.5, y1 + 0.025, title, 14.5, WHITE, z=12)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=1.6, alpha=.8, zorder=5)
    for az, lab in DIRS16:
        if az0 <= az <= az1:
            x, _ = q(0, az)
            ctext(ax, x, y0 - 0.022, lab, 10.5, WHITE, w="normal", z=12)
    for alt in (20, 40):
        if alt < alt1:
            _, y = q(alt, az0)
            ax.plot([xa, xb], [y, y], c=WHITE, lw=0.6, alpha=.18, ls=(0, (3, 4)), zorder=2)
            ax.text(xa + 0.005, y + 0.004, f"{alt}°", fontproperties=CB.FP, fontsize=8, color=GREY, zorder=3)
    pos = {}
    for h, (ra, dec, v) in S.items():
        if v > 4.3:
            continue
        b = body(ra, dec); b.compute(o)
        alt, az = math.degrees(float(b.alt)), math.degrees(float(b.az))
        if not (0 < alt < alt1 and az0 < az < az1):
            continue
        x, y = q(alt, az)
        pos[h] = (x, y)
        ax.scatter([x], [y], s=max(1.0, (5.6 - v) ** 2.2 * 2.6), c=WHITE, zorder=7, lw=0)
    for seg, col in lines:
        for a, b in zip(seg, seg[1:]):
            a, b = HIP.get(a, a), HIP.get(b, b)
            if a in pos and b in pos:
                ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=col, lw=1.6, alpha=.75, zorder=6)
    for key, lab, col, dx, dy in marks:
        h = HIP.get(key, key)
        if h not in pos:
            continue
        x, y = pos[h]
        ctext(ax, x + dx, y + dy, lab, 11, col, ha="left" if dx > 0 else ("right" if dx < 0 else "center"), z=12)


def c06_card(ax):
    ctext(ax, 0.5, 0.962, "這週末抬頭看", 30, WHITE)
    ctext(ax, 0.5, 0.928, "台北　2026/12/19（六）、12/20（日）", 13, GREY, w="normal")
    sky_panel(ax, 0.625, 0.845, 225.0, 330.0, 45.0, "2026/12/19 18:30",
              "18:30 往西：Aagjuuk 還有二十幾度高（8 點多落下）",
              [("Altair", "牛郎星", AMBER, 0.03, -0.012), ("Tarazed", "河鼓三", AMBER, 0.03, 0.012),
               ("Vega", "織女星", WHITE, -0.03, 0.0)],
              lines=[(["Tarazed", "Altair"], AMBER)])
    sky_panel(ax, 0.265, 0.505, 40.0, 130.0, 60.0, "2026/12/19 19:30",
              "19:30 往東：奔跑的人追著北極熊爬上來",
              [("Alnilam", "Ullaktut 奔跑的人", BLUE, 0.0, -0.04),
               ("Aldebaran", "Nanurjuk 北極熊", RED, 0.03, 0.0),
               ("Capella", "鎖骨（五車二）", GREEN, 0.035, 0.0),
               ("Castor", "鎖骨（北河二）", GREEN, 0.035, 0.012),
               (32349, "天狼星 Singuuriq（剛升起）", WHITE, -0.035, 0.0)],
              lines=[([26727, 26311, 25930], BLUE), (["Aldebaran", 20894, 20205, 20455, 20889], RED),
                     (["Capella", "Menkalinan"], GREEN), (["Castor", "Pollux"], GREEN)])
    lines = [("12/22（二）04:50 冬至：一年白天最短", AMBER),
             ("北斗（馴鹿）晚上 7 點才從北方地平線冒出頭，後半夜才爬高", WHITE),
             ("月亮（七成多亮）掛在頭頂附近，凌晨 2 點落下——往東西兩邊低空找星", WHITE),
             ("同一時刻的 Igloolik：太陽 11/29 下山，要到 1 月中才回來", GREY),
             ("方位、高度、時刻：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.165 - i * 0.0255, s, 11 if col != GREY else 9.5, col, w="normal")
    ctext(ax, 0.5, 0.018, "#萬國星空　#師大天文社", 12, WHITE, w="normal")


# ══════════════════════ 魚叉（滿版 1080×1920 透明） ══════════════════════
def harpoon(pole_xy=(540.0, 852.0), base=(735.0, 1735.0), length=520.0):
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(5.4, 9.6), dpi=200)
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1080); ax.set_ylim(1920, 0); ax.axis("off")
    f.patch.set_alpha(0); ax.patch.set_alpha(0)
    bx, by = base; px, py = pole_xy
    dx, dy = px - bx, py - by
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    tx, ty = bx + ux * length, by + uy * length
    nx, ny = -uy, ux
    # 擋風雪牆 uquutaq（兩排雪磚，在魚叉後面）
    for row, (y0, x0, n) in enumerate([(1690.0, 760.0, 3), (1640.0, 795.0, 2)]):
        for k in range(n):
            ax.add_patch(CB.Rectangle((x0 + 74 * k, y0), 70, 46, fc="#DDE6F2", ec="#9FB0C8", lw=1.5,
                                      alpha=0.92, zorder=2))
    # 視線（虛線）
    ax.plot([tx + ux * 90, px - ux * 26], [ty + uy * 90, py - uy * 26], c="#FFFFFF", lw=2.0, alpha=.45,
            ls=(0, (6, 7)), zorder=3)
    # 柄
    ax.plot([bx, tx], [by, ty], c="#D9B48A", lw=10, solid_capstyle="round", zorder=4)
    ax.plot([bx, tx], [by, ty], c="#8C6A45", lw=2, alpha=.6, zorder=5)
    for k in (0.20, 0.235):                     # 綁繩
        cx_, cy_ = bx + ux * length * k, by + uy * length * k
        ax.plot([cx_ - nx * 10, cx_ + nx * 10], [cy_ - ny * 10, cy_ + ny * 10], c="#6E5238", lw=3, zorder=6)
    # 魚叉頭（骨製、帶倒鉤）
    hx, hy = tx + ux * 95, ty + uy * 95
    head = [(tx + nx * 9, ty + ny * 9), (hx, hy), (tx - nx * 9, ty - ny * 9),
            (tx - ux * 10 - nx * 24, ty - uy * 10 - ny * 24), (tx + ux * 22 - nx * 9, ty + uy * 22 - ny * 9)]
    ax.add_patch(CB.Polygon(head, closed=True, fc="#F2EEE4", ec="#B9B3A6", lw=1.5, zorder=6))
    ax.add_patch(CB.Circle((px, py), 22, fc="none", ec=AMBER, lw=2.4, alpha=.8, zorder=6))
    d = os.path.join(OUT); os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, "C-A14-魚叉_透明.png")
    f.savefig(fn, transparent=True); plt.close(f)
    print("  ✓ C-A14-魚叉_透明.png", (round(hx), round(hy)), "→", pole_xy)


def main():
    global S
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A14 概念圖 ──")
    CB.emit("", [("地平", c01_horizon), ("台北", c01_taipei), ("Igloolik", c01_igloolik), ("極夜", c01_night)],
            title="C-A14-01_極夜")
    CB.emit("", [("傍晚", c02_dusk), ("後半夜", c02_night), ("清晨", c02_dawn)], title="C-A14-02_星鐘")
    CB.emit("", [("地平", c03_horizon), ("十二月初", c03_dec1), ("第二週", c03_week2), ("冬至", c03_solstice)],
            title="C-A14-03_Aagjuuk初見")
    CB.emit("", [("油燈", c04_lamps), ("半邊笑", c04_smile)], title="C-A14-04_太陽回來")
    for name, fn in [("C-A14-05_因紐特星名小辭典", c05_card), ("C-A14-06_這週末抬頭看", c06_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)
    harpoon()


if __name__ == "__main__":
    main()
