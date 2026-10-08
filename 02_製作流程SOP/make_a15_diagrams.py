# -*- coding: utf-8 -*-
"""A-15 北歐：Yule 之夜的狼與神駒｜概念圖（C 系列骨架）

C-A15-01 Yule變聖誕（仲冬層、立法層、今天層）：仲冬夜起連過三晚 → 十世紀 Hákon 立法跟聖誕節同一天
         （每人備一份啤酒，不然罰錢；酒喝多久、節就過多久）→ 今天北歐語的聖誕節＝jul／jól
C-A15-02 八隻馴鹿（神駒層、一頭層、八隻層）：Edda 的 Sleipnir 八條腿 → 1821 紐約一頭馴鹿 → 1823〈A Visit
         from St. Nicholas〉八隻有名字的馴鹿；兩者之間古書裡找不到關係
C-A15-03 天上的追逐（太陽層、月亮層、神駒層）：Snorri《Gylfaginning》10–12、51
C-A15-04 引路星一千年（今天層、一千年前層）：北天極的歲差；北極星 2026 年離極 0.6°、1000 年 6.2°
C-A15-05 同一個V字（9:16 圖卡）：畢宿 V 字在各文化＝嘴、下巴、夾子、網、狗群…
C-A15-06 北歐星名小辭典（9:16 圖卡）
C-A15-07 這週末抬頭看（9:16 圖卡；台北 2026/12/25 20:00）

天象全部 PyEphem 自算；文本：Snorri《Edda》（Gylfaginning、Skáldskaparmál）、《Vafþrúðnismál》14、
《Heimskringla・Hákonar saga góða》；星名：Stellarium norse／norse_edda、Beckman & Kålund《Alfræði íslenzk II》。
執行：python3 make_a15_diagrams.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import matplotlib.patheffects as PE

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-15_北歐/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
S = None
TPE = (25.0330, 121.5654, 0, 8, 15)
HIP = dict(Aldebaran=21421, Alnilam=26311, Alnitak=26727, Mintaka=25930, Betelgeuse=27989, Rigel=24436,
           Capella=24608, Menkalinan=28360, Castor=36850, Pollux=37826, Polaris=11767, Kochab=72607,
           Pherkad=75097, Dubhe=54061, Merak=53910, Procyon=37279, Sirius=32349, Alcyone=17702, Elnath=25428)
HYADES = [21421, 20894, 20205, 20455, 20889]


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, rot=0, va="center", alpha=1.0):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, rotation=rot, rotation_mode="anchor", alpha=alpha, linespacing=1.25)


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


def poly(ax, pts, x, y, s, fc, ec="none", lw=1.5, z=6, flip=False, alpha=1.0):
    """單位座標輪廓 → 畫布（flip＝左右鏡像）"""
    P = [(x + (-px if flip else px) * s, y + py * s) for px, py in pts]
    ax.add_patch(CB.Polygon(P, closed=True, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


# 輪廓（單位座標，面向右）
WOLF = [(0.00, 0.00), (0.04, 0.50), (0.22, 0.72), (0.33, 1.00), (0.44, 0.74), (0.60, 0.70), (0.76, 0.55),
        (1.04, 0.44), (1.03, 0.34), (0.82, 0.27), (0.64, 0.17), (0.36, 0.04)]
HORSE = [(0.00, 0.00), (0.10, 0.62), (0.28, 0.92), (0.34, 1.06), (0.40, 0.92), (0.56, 0.84), (0.98, 0.46),
         (1.04, 0.33), (0.97, 0.22), (0.80, 0.25), (0.55, 0.36), (0.40, 0.18), (0.36, 0.00)]


def wolf_head(ax, x, y, s, col=GREY, flip=False, z=6):
    poly(ax, WOLF, x, y, s, col, z=z, flip=flip)
    ex = x + (-0.56 if flip else 0.56) * s
    ax.add_patch(CB.Circle((ex, y + 0.55 * s), 0.035 * s, fc="#0B0F1E", ec="none", zorder=z + 1))


def horse_head(ax, x, y, s, col=WHITE, flip=False, z=6, mane=None):
    poly(ax, HORSE, x, y, s, col, z=z, flip=flip)
    sg = -1 if flip else 1
    ax.add_patch(CB.Circle((x + sg * 0.52 * s, y + 0.70 * s), 0.035 * s, fc="#0B0F1E", ec="none", zorder=z + 1))
    if mane:                                    # 鬃毛：沿頸背的短線
        for k in range(6):
            t = k / 5
            px, py = 0.02 + 0.24 * t, 0.10 + 0.80 * t
            ax.plot([x + sg * px * s, x + sg * (px - 0.16) * s], [y + py * s, y + (py + 0.05) * s],
                    c=mane, lw=2.6, solid_capstyle="round", zorder=z + 1)


def reindeer(ax, x, y, s, col=WHITE, z=6):
    horse_head(ax, x, y, s, col=col, z=z)
    for sg in (1, -1):                          # 鹿角：兩支分岔
        bx, by = x + 0.34 * s, y + 1.0 * s
        tx, ty = bx - 0.18 * s + sg * 0.05 * s, by + 0.55 * s
        ax.plot([bx, tx], [by, ty], c=col, lw=2.2 * s / 0.12, solid_capstyle="round", zorder=z)
        for f in (0.45, 0.75):
            mx, my = bx + (tx - bx) * f, by + (ty - by) * f
            ax.plot([mx, mx + 0.16 * s], [my, my + 0.12 * s], c=col, lw=1.8 * s / 0.12,
                    solid_capstyle="round", zorder=z)


def sun_icon(ax, x, y, r, alpha=1.0, z=7):
    for k, op in ((2.4, 0.06), (1.7, 0.12)):
        ax.add_patch(CB.Circle((x, y), r * k, fc=AMBER, ec="none", alpha=op * alpha, zorder=z - 1))
    ax.add_patch(CB.Circle((x, y), r, fc=AMBER, ec=AMBER, lw=2.0, alpha=alpha, zorder=z))


def moon_icon(ax, x, y, r, z=7):
    """彎月：外緣半圓＋內緣橢圓弧"""
    th = [math.pi / 2 + math.pi * i / 40 for i in range(41)]
    outer = [(x + r * math.cos(t), y + r * math.sin(t)) for t in th]
    inner = [(x - 0.35 * r * math.cos(t), y + r * math.sin(t)) for t in th[::-1]]
    ax.add_patch(CB.Circle((x, y), r * 1.5, fc=MW, ec="none", alpha=0.08, zorder=z - 1))
    ax.add_patch(CB.Polygon(outer + inner, closed=True, fc="#E8EEF8", ec="none", zorder=z))


# ══════════════════════ C-A15-01 Yule 變聖誕 ══════════════════════
def c01_old(ax):
    T(ax, 0.0, 0.92, "Yule 怎麼變成聖誕節？", 30, WHITE)
    T(ax, 0.0, 0.845, "北歐的 jól（英文古字 Yule）", 15, GREY, w="normal")
    box(ax, -0.95, 0.30, 1.90, 0.45, ec=BLUE, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, 0.69, "改信基督教以前", 16, BLUE, ha="left")
    ctext(ax, -0.90, 0.625, "從「仲冬夜」（hǫkunótt）開始，連過三晚", 14, WHITE, w="normal", ha="left")
    for i in range(3):                          # 三個夜晚
        cx = -0.55 + 0.55 * i
        ax.add_patch(CB.Circle((cx, 0.445), 0.085, fc="#05070F", ec=BLUE, lw=1.6, zorder=4))
        moon_icon(ax, cx - 0.02, 0.46, 0.035, z=5)
        for dx, dy in ((0.04, -0.03), (0.035, 0.035), (-0.045, -0.035)):
            ax.scatter([cx + dx], [0.445 + dy], s=6, c=WHITE, zorder=6, lw=0)
        ctext(ax, cx, 0.335, f"第 {i + 1} 晚", 12, WHITE, w="normal")


def c01_law(ax):
    box(ax, -0.95, -0.30, 1.90, 0.52, ec=AMBER, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, 0.16, "十世紀　挪威國王 Hákon（善王）立法", 16, AMBER, ha="left")
    CB.arrow(ax, (-0.10, 0.06), (-0.55, 0.06), c=AMBER, lw=2.4, alpha=.9)
    ctext(ax, -0.72, 0.06, "仲冬", 15, BLUE)
    box(ax, -0.02, -0.01, 0.40, 0.14, ec=AMBER, fc="#2A2410", lw=1.6, z=4)
    ctext(ax, 0.18, 0.06, "12/25 聖誕節", 15, AMBER)
    ctext(ax, 0.62, 0.06, "同一天過", 13, WHITE, w="normal")
    # 啤酒杯（牛角杯）
    # 牛角杯：上緣是開口、往下彎成尖角
    up = [(0.60 + 0.26 * t, -0.04 + 0.02 * t - 0.20 * (1 - t) ** 2) for t in [i / 20 for i in range(21)]]
    lo = [(0.66 + 0.20 * t, -0.25 + 0.17 * t + 0.0 * t * t) for t in [i / 20 for i in range(21)]]
    horn = [(0.60, -0.24)] + up[1:] + [(0.90, -0.06)] + lo[::-1]
    ax.add_patch(CB.Polygon(horn, closed=True, fc="#D9B48A", ec="#8C6A45", lw=1.4, zorder=5))
    ax.add_patch(CB.Ellipse((0.88, -0.03), 0.07, 0.045, angle=-10, fc="#F2D27A", ec="#8C6A45", lw=1.2, zorder=6))
    for k in (0.35, 0.6):                       # 金屬箍
        x = 0.62 + 0.26 * k
        ax.plot([x, x + 0.01], [-0.25 + 0.17 * k + 0.02, -0.04 + 0.02 * k - 0.20 * (1 - k) ** 2 - 0.02],
                c="#8C6A45", lw=2.0, zorder=6)
    ctext(ax, -0.90, -0.12, "每個人都得備好一份啤酒，不然就罰錢", 14, WHITE, w="normal", ha="left")
    ctext(ax, -0.90, -0.20, "——酒喝多久，節就過多久", 14, WHITE, w="normal", ha="left")
    ctext(ax, -0.90, -0.265, "Snorri《Heimskringla・Hákonar saga góða》（約 1230 年寫成）", 10, GREY, w="normal", ha="left")


def c01_today(ax):
    box(ax, -0.95, -0.80, 1.90, 0.42, ec=GREEN, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, -0.43, "今天：聖誕節還叫這個名字", 16, GREEN, ha="left")
    words = [("jul", "瑞典・挪威・丹麥"), ("jól", "冰島"), ("joulu", "芬蘭（借字）"), ("Yule", "英文古字")]
    for i, (w, where) in enumerate(words):
        x = -0.70 + 0.47 * i
        ctext(ax, x, -0.56, w, 24, WHITE)
        ctext(ax, x, -0.645, where, 11, GREY, w="normal")
    ctext(ax, 0.0, -0.735, "God jul！＝聖誕快樂（瑞典、挪威、丹麥）", 13, GREEN, w="normal")


# ══════════════════════ C-A15-02 八隻馴鹿 ══════════════════════
def c02_sleipnir(ax):
    T(ax, 0.0, 0.92, "聖誕老人的八隻馴鹿，從哪裡來？", 26, WHITE)
    box(ax, -0.95, 0.30, 1.90, 0.50, ec=PURPLE, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, 0.74, "13 世紀　Edda：奧丁的神駒 Sleipnir", 15, PURPLE, ha="left")
    ctext(ax, -0.90, 0.675, "八條腿的灰馬", 13, WHITE, w="normal", ha="left")
    # 八條腿的馬（側面，面向右）
    col = "#C8CFDC"
    x0, y0 = 0.10, 0.56
    ax.add_patch(CB.Ellipse((x0, y0), 0.46, 0.13, fc=col, ec="none", zorder=4))
    neck = [(x0 + 0.12, y0 + 0.04), (x0 + 0.18, y0 + 0.11), (x0 + 0.25, y0 + 0.10), (x0 + 0.21, y0 - 0.03)]
    ax.add_patch(CB.Polygon(neck, closed=True, fc=col, ec="none", zorder=4))
    horse_head(ax, x0 + 0.16, y0 + 0.06, 0.13, col=col, z=5, mane="#9AA6BE")
    tail = [(x0 - 0.22, y0 + 0.03), (x0 - 0.31, y0 - 0.02), (x0 - 0.33, y0 - 0.12), (x0 - 0.27, y0 - 0.05)]
    ax.add_patch(CB.Polygon(tail, closed=True, fc="#9AA6BE", ec="none", zorder=4))
    for i in range(8):                          # 八條腿：後腿四條、前腿四條
        lx = x0 - 0.17 + 0.038 * i + (0.10 if i >= 4 else 0.0)
        ax.plot([lx, lx + 0.012 * (1 if i % 2 else -1)], [y0 - 0.04, y0 - 0.19], c=col, lw=3.0,
                solid_capstyle="round", zorder=4)
    ctext(ax, 0.70, 0.46, "8", 34, PURPLE)
    ctext(ax, 0.70, 0.385, "條腿", 12, PURPLE, w="normal")


def c02_one(ax):
    box(ax, -0.95, -0.22, 1.90, 0.46, ec=WHITE, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, 0.18, "1821 年　紐約的兒童詩集", 15, WHITE, ha="left")
    ctext(ax, -0.90, 0.115, "雪橇第一次由「一頭」馴鹿拉（沒有名字）", 13, WHITE, w="normal", ha="left")
    reindeer(ax, 0.45, -0.17, 0.20, col="#C8CFDC")
    ctext(ax, -0.50, -0.06, "1", 40, WHITE)
    ctext(ax, -0.50, -0.15, "頭", 12, WHITE, w="normal")


def c02_eight(ax):
    box(ax, -0.95, -0.92, 1.90, 0.64, ec=AMBER, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, -0.90, -0.34, "1823 年　美國紐約〈A Visit from St. Nicholas〉", 15, AMBER, ha="left")
    ctext(ax, -0.90, -0.405, "第一次出現八隻，還都有名字", 13, WHITE, w="normal", ha="left")
    names = ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Dunder", "Blixem"]
    for i, nm in enumerate(names):
        x = -0.82 + 0.233 * (i % 8)
        reindeer(ax, x - 0.05, -0.62, 0.085, col="#E9D9A6")
        ctext(ax, x, -0.68, nm, 8.5, AMBER, w="normal")
    ctext(ax, 0.0, -0.78, "Sleipnir 的八條腿 → 八隻馴鹿？古書裡找不到這條線", 14, RED)
    ctext(ax, 0.0, -0.85, "（最後兩隻原名 Dunder、Blixem，荷蘭語「雷」和「閃電」）", 10, GREY, w="normal")


# ══════════════════════ C-A15-03 天上的追逐 ══════════════════════
def c03_sun(ax):
    T(ax, 0.0, 0.92, "天上的追逐", 30, WHITE)
    T(ax, 0.0, 0.845, "Snorri《Edda・Gylfaginning》", 14, GREY, w="normal")
    box(ax, -0.95, 0.28, 1.90, 0.48, ec=AMBER, fc=PANEL, z=2, alpha=0.95)
    sun_icon(ax, 0.10, 0.52, 0.075)
    ctext(ax, 0.10, 0.36, "太陽 Sól", 15, AMBER)
    wolf_head(ax, -0.72, 0.42, 0.24, col="#9AA6BE")
    ctext(ax, -0.60, 0.33, "狼 Sköll", 14, WHITE)
    CB.arrow(ax, (-0.10, 0.52), (-0.42, 0.52), c=RED, lw=2.4, alpha=.85)
    ctext(ax, -0.26, 0.585, "追", 14, RED)
    ctext(ax, -0.26, 0.69, "太陽跑得急，因為後面有狼", 11.5, WHITE, w="normal")


def c03_moon(ax):
    box(ax, -0.95, -0.27, 1.90, 0.48, ec=BLUE, fc=PANEL, z=2, alpha=0.95)
    moon_icon(ax, 0.10, -0.03, 0.065)
    ctext(ax, 0.10, -0.18, "月亮 Máni", 15, BLUE)
    wolf_head(ax, -0.72, -0.13, 0.24, col="#9AA6BE")
    ctext(ax, -0.60, -0.22, "狼 Hati", 14, WHITE)
    CB.arrow(ax, (-0.10, -0.03), (-0.42, -0.03), c=RED, lw=2.4, alpha=.85)
    ctext(ax, -0.26, 0.035, "追", 14, RED)
    ctext(ax, 0.62, -0.03, "到了諸神的黃昏，\n狼會把太陽吞下去", 12, RED, w="normal")


def c03_horses(ax):
    # 太陽車的兩匹馬（畫在太陽前面）
    ax.plot([0.20, 0.40], [0.52, 0.50], c=AMBER, lw=1.6, alpha=.7, zorder=5)     # 韁繩
    ax.plot([0.20, 0.48], [0.50, 0.42], c=AMBER, lw=1.6, alpha=.7, zorder=5)
    horse_head(ax, 0.38, 0.48, 0.13, col="#F2D27A", mane=AMBER)
    horse_head(ax, 0.47, 0.37, 0.13, col="#E9C46A", mane=AMBER)
    ctext(ax, 0.80, 0.55, "Árvakr「早起」", 12.5, AMBER, w="normal")
    ctext(ax, 0.80, 0.47, "Alsviðr「飛快」", 12.5, AMBER, w="normal")
    ctext(ax, 0.80, 0.39, "拉太陽車的兩匹馬", 10.5, WHITE, w="normal")
    box(ax, -0.95, -0.94, 1.90, 0.58, ec=WHITE, fc=PANEL, z=2, alpha=0.95)
    ctext(ax, 0.0, -0.42, "白天和黑夜，也各騎一匹馬", 15, WHITE)
    horse_head(ax, -0.88, -0.64, 0.15, col="#F2D27A", mane="#FFF4C8")
    ctext(ax, -0.62, -0.53, "Skinfaxi「亮鬃」", 14, AMBER, ha="left")
    ctext(ax, -0.62, -0.60, "白天騎牠，鬃毛照亮天空和大地", 11, WHITE, w="normal", ha="left")
    horse_head(ax, -0.88, -0.85, 0.15, col="#7F93B8", mane="#E8F1FF")
    ctext(ax, -0.62, -0.72, "Hrímfaxi「霜鬃」", 14, BLUE, ha="left")
    ctext(ax, -0.62, -0.79, "黑夜騎牠；每天早上，嚼子上滴下的白沫", 11, WHITE, w="normal", ha="left")
    ctext(ax, -0.62, -0.85, "就是山谷裡的露水", 11, WHITE, w="normal", ha="left")
    for dx, dy in ((0.0, 0.0), (0.012, -0.045), (-0.010, -0.085)):    # 嚼子滴下的露水
        ax.add_patch(CB.Ellipse((-0.725 + dx, -0.83 + dy), 0.018, 0.028, fc="#BFD8FF", ec="none", alpha=.9,
                                zorder=8))
    ctext(ax, 0.55, -0.905, "《Gylfaginning》10–12、51；《Vafþrúðnismál》14", 9, GREY, w="normal")


# ══════════════════════ C-A15-04 引路星一千年 ══════════════════════
def pole_j2000(year):
    import ephem
    e = ephem.Equatorial(0, math.radians(90), epoch=ephem.Date(f"{year}/1/1"))
    j = ephem.Equatorial(e, epoch=ephem.J2000)
    return math.degrees(float(j.ra)), math.degrees(float(j.dec))


PC = (0.08, 0.12)              # 畫面中 1000 年的北天極
SCL = 0.085                    # 每度
C04_CEN = None


def c04_xy(ra, dec):
    """以 1000 年北天極為中心的切平面投影（東在左）"""
    ra0, dec0 = C04_CEN
    a, d, a0, d0 = map(math.radians, (ra, dec, ra0, dec0))
    c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / c
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / c
    return PC[0] - math.degrees(x) * SCL, PC[1] + math.degrees(y) * SCL


def _pole_ring(ax, year, col, label, dashed, ldx, ldy):
    pr, pd = pole_j2000(year)
    px, py = c04_xy(pr, pd)
    qx, qy = c04_xy(*S[HIP["Polaris"]][:2])      # 圈＝北極星繞著這個年代的北天極轉一晚的路
    r = math.hypot(px - qx, py - qy)
    th = [2 * math.pi * i / 180 for i in range(181)]
    ax.plot([px + r * math.cos(t) for t in th], [py + r * math.sin(t) for t in th], c=col, lw=2.0,
            ls=(0, (5, 5)) if dashed else "-", alpha=.85, zorder=4)
    ax.plot([px - 0.03, px + 0.03], [py, py], c=col, lw=2.0, zorder=6)
    ax.plot([px, px], [py - 0.03, py + 0.03], c=col, lw=2.0, zorder=6)
    ctext(ax, px + ldx, py + ldy, label, 13, col)
    return px, py, r


def c04_today(ax):
    T(ax, 0.0, 0.92, "引路的星，一千年前在哪裡？", 28, WHITE)
    T(ax, 0.0, 0.845, "北天極會慢慢移動（歲差），北極星不是一直都在正北", 13, GREY, w="normal")
    # 北極星附近的亮星（J2000）
    qx, qy = c04_xy(*S[HIP["Polaris"]][:2])
    ax.scatter([qx], [qy], s=130, c=WHITE, zorder=8, lw=0)
    ctext(ax, qx + 0.07, qy + 0.035, "北極星 Leiðarstjarna", 13, AMBER, ha="left")
    px, py, r = _pole_ring(ax, 2026, GREEN, "", False, 0, 0)
    ctext(ax, px + 0.07, py - 0.045, "今天的北天極", 12, GREEN, ha="left")
    ctext(ax, -0.90, -0.62, "今天：北極星離北天極 0.6°，一整晚幾乎不動", 14, GREEN, ha="left")
    # 比例尺：滿月
    ax.plot([0.55, 0.55 + 0.5 * SCL], [-0.80, -0.80], c=WHITE, lw=2.0, zorder=6)
    ax.add_patch(CB.Circle((0.55 + 0.25 * SCL, -0.80), 0.25 * SCL, fc="none", ec=WHITE, lw=1.0, zorder=6))
    ctext(ax, 0.62, -0.86, "滿月直徑 0.5°", 10, WHITE, w="normal", ha="left")


def c04_1000(ax):
    px, py, r = _pole_ring(ax, 1000, AMBER, "", True, 0, 0)
    ctext(ax, px, py + 0.07, "1000 年的北天極", 12, AMBER)
    qx, qy = c04_xy(*S[HIP["Polaris"]][:2])
    ax.plot([px, qx], [py, qy], c=AMBER, lw=1.2, alpha=.7, ls=(0, (2, 3)), zorder=5)
    ctext(ax, (px + qx) / 2 - 0.07, (py + qy) / 2, "6.2°", 15, AMBER)
    pts = [c04_xy(*pole_j2000(yr)) for yr in range(1000, 2027, 25)]      # 北天極走過的路
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=WHITE, lw=1.4, alpha=.55, ls=(0, (1, 3)), zorder=5)
    for yr in (1500,):
        x, y = c04_xy(*pole_j2000(yr))
        ax.scatter([x], [y], s=14, c=WHITE, zorder=6, lw=0)
        ctext(ax, x + 0.04, y + 0.03, f"{yr}", 10, WHITE, w="normal", ha="left")
    ctext(ax, -0.90, -0.70, "一千年前（維京時代）：離北天極 6.2°——自己也繞著虛線的小圈轉", 13, AMBER, ha="left")
    ctext(ax, -0.90, -0.92, "PyEphem 自算（IAU 歲差模型）", 9, GREY, w="normal", ha="left")


# ══════════════════════ 9:16 圖卡 ══════════════════════
def hyades_drawing(ax, cx, cy, sc, col=RED):
    """畢宿 V 字＋畢宿五（切平面投影，東在左）"""
    pts = {h: S[h] for h in HYADES}
    ra0 = sum(p[0] for p in pts.values()) / len(pts); dec0 = sum(p[1] for p in pts.values()) / len(pts)
    xy = {}
    for h, (ra, dec, v) in pts.items():
        x = -(ra - ra0) * math.cos(math.radians(dec0)) * sc
        y = (dec - dec0) * sc * 0.5625            # 圖卡是 9:16，y 方向換算
        xy[h] = (cx + x, cy + y)
    seq = HYADES
    ax.plot([xy[h][0] for h in seq], [xy[h][1] for h in seq], c=col, lw=2.6, alpha=.9, zorder=5)
    ax.text(xy[21421][0] - 0.03, xy[21421][1], "畢宿五", fontproperties=CB.FP, fontsize=11, color=WHITE,
            ha="right", va="center", zorder=7)
    for h, (ra, dec, v) in pts.items():
        ax.scatter([xy[h][0]], [xy[h][1]], s=max(10, (5.6 - v) ** 2.2 * 8), c=WHITE, zorder=6, lw=0)
    return xy


def c05_card(ax):
    ctext(ax, 0.5, 0.962, "同一個 V 字", 30, WHITE)
    ctext(ax, 0.5, 0.930, "金牛座的畢宿（Hyades），在世界各地被看成什麼？", 12, GREY, w="normal")
    hyades_drawing(ax, 0.5, 0.83, 0.060)
    rows = [("一張嘴、一副下巴", None, RED),
            ("北歐", "Úlfs kjaptr　狼嘴（冰島手抄本，12 世紀）", RED),
            ("古巴比倫", "Is lê　公牛的下顎（MUL.APIN）", RED),
            ("亞馬遜 Tikuna", "Coyatchicüra　鱷魚的嘴", RED),
            ("巴西 圖皮", "Tapi'i rainhyka　貘的下巴", RED),
            ("蘇利南、蓋亞那 洛科諾", "Kama tâla　貘的下巴", RED),
            ("古埃及（重建）", "「下巴」", RED),
            ("一把夾子", None, AMBER),
            ("阿努塔", "Te Angaanga　火鉗", AMBER),
            ("萬那杜 Netwar", "Kou　夾熱石頭的鉗子", AMBER),
            ("其他", None, BLUE),
            ("中國", "畢　捕鳥兔的長柄網", BLUE),
            ("因紐特", "Qimmiit　狗群（畢宿五是北極熊）", BLUE),
            ("東加", "Tu'ulalupe　鴿子的棲架", BLUE),
            ("羅馬尼亞", "Vierii　野豬群", BLUE),
            ("白俄羅斯", "Vuzhy　草蛇", BLUE)]
    y = 0.735
    for a, b, col in rows:
        if b is None:
            y -= 0.006
            ctext(ax, 0.06, y, a, 14, col, ha="left")
            ax.plot([0.06, 0.94], [y - 0.016, y - 0.016], c=col, lw=1.0, alpha=.5)
            y -= 0.040
            continue
        ctext(ax, 0.06, y, a, 11, WHITE, ha="left")
        ctext(ax, 0.40, y, b, 11, col, w="normal", ha="left")
        y -= 0.034
    ctext(ax, 0.5, 0.075, "名稱與連線：Stellarium 各文化星空（norse、babylonian_mulapin、tikuna、tupi、", 8.5, GREY,
          w="normal")
    ctext(ax, 0.5, 0.055, "lokono、egyptian、anutan、vanuatu_netwar、chinese、inuit、tongan、romanian、belarusian）",
          8.5, GREY, w="normal")
    ctext(ax, 0.5, 0.020, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


GLOSS = [("冰島手抄本（12 世紀，拉丁文天文學旁的註解）", None, None, AMBER),
         ("Úlfs kjaptr", "Ulf's Keptr", "狼嘴＝畢宿", RED),
         ("Fiskikarlar", "", "漁夫＝獵戶腰帶", BLUE),
         ("Karlvagn", "", "男人的車＝北斗", AMBER),
         ("Kvennavagn", "", "女人的車＝小熊", GREEN),
         ("Leiðarstjarna", "Leidarstjarna", "引路的星＝北極星", AMBER),
         ("Asar bardagi", "", "眾神之戰＝御夫（字義有爭議）", PURPLE),
         ("Edda 神話（13 世紀，Snorri）", None, None, PURPLE),
         ("Þjaza augu", "", "巨人 Þjazi 的眼睛（哪兩顆不知道，常猜北河二、三）", WHITE),
         ("Aurvandils tá", "", "Aurvandil 的腳趾（哪顆不知道；Stellarium 放北冕座）", WHITE),
         ("Sköll／Hati", "", "追太陽、追月亮的兩匹狼", RED),
         ("Árvakr、Alsviðr", "", "拉太陽車的「早起」「飛快」", AMBER),
         ("Hrímfaxi／Skinfaxi", "", "黑夜的「霜鬃」、白天的「亮鬃」", BLUE),
         ("民間與今天", None, None, GREEN),
         ("Friggerock", "", "Frigg 的紡紗桿＝獵戶腰帶（瑞典民間）", PURPLE),
         ("Karlavagnen", "", "北斗（今天的瑞典語）", AMBER),
         ("jul／jól", "", "聖誕節（＝Yule）", GREEN)]


def c06_card(ax):
    ctext(ax, 0.5, 0.962, "北歐星名小辭典", 28, WHITE)
    ctext(ax, 0.5, 0.930, "古北歐語（拼法照正規化寫法；Stellarium 另有寫法）", 10.5, GREY, w="normal")
    y = 0.893
    for nat, west, zh, col in GLOSS:
        if west is None:
            y -= 0.004
            ctext(ax, 0.06, y, nat, 13, col, ha="left")
            ax.plot([0.06, 0.94], [y - 0.015, y - 0.015], c=col, lw=1.0, alpha=.5)
            y -= 0.036
            continue
        ctext(ax, 0.06, y + (0.008 if west else 0.0), nat, 12.5, AMBER, ha="left")
        if west:
            ctext(ax, 0.06, y - 0.012, west, 8.5, GREY, w="normal", ha="left")
        ctext(ax, 0.37, y, zh, 10.5, col, w="normal", ha="left")
        y -= 0.040
    ctext(ax, 0.5, 0.060, "維京人沒有留下星圖：這些就是留下來的全部線索", 11, GREEN, w="normal")
    ctext(ax, 0.5, 0.036, "Beckman & Kålund《Alfræði íslenzk II》；Snorri《Edda》；Stellarium norse、norse_edda", 8.5,
          GREY, w="normal")
    ctext(ax, 0.5, 0.012, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


DIRS16 = [(0, "北"), (22.5, "北北東"), (45, "東北"), (67.5, "東北東"), (90, "東"), (112.5, "東南東"),
          (135, "東南"), (157.5, "南南東"), (180, "南")]


def sky_panel(ax, y0, y1, az0, az1, alt1, when, title, marks, lines=(), moon=False):
    import ephem
    o = observer(TPE, when)
    xa, xb = 0.06, 0.94

    def q(alt, az):
        return xa + (az - az0) / (az1 - az0) * (xb - xa), y0 + alt / alt1 * (y1 - y0)
    box(ax, 0.04, y0 - 0.055, 0.92, (y1 - y0) + 0.10, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ctext(ax, 0.5, y1 + 0.025, title, 14, WHITE, z=12)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=1.6, alpha=.8, zorder=5)
    for az, lab in DIRS16:
        if az0 <= az <= az1:
            x, _ = q(0, az)
            ctext(ax, x, y0 - 0.022, lab, 10.5, WHITE, w="normal", z=12)
    for alt in (20, 40, 60):
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
        ax.text(x + dx, y + dy, lab, fontproperties=CB.FP, fontsize=11, color=col, weight="bold", va="center",
                ha="left" if dx > 0 else ("right" if dx < 0 else "center"), zorder=12,
                path_effects=[PE.withStroke(linewidth=4, foreground="#0E1428")])
    if moon:
        mo = ephem.Moon(o)
        alt, az = math.degrees(float(mo.alt)), math.degrees(float(mo.az))
        x, y = q(alt, az)
        k = CB.CARD_W / CB.CARD_H                # 圖卡 x、y 單位長度不同：圓要畫成橢圓才會是圓
        ax.add_patch(CB.Ellipse((x, y), 0.032, 0.032 * k, fc="#F4F1E6", ec="none", zorder=9))
        ax.add_patch(CB.Ellipse((x, y), 0.060, 0.060 * k, fc="#F4F1E6", ec="none", alpha=.15, zorder=8))
        ax.text(x, y - 0.045, f"聖誕節的月亮（{mo.phase:.0f}% 亮）", fontproperties=CB.FP, fontsize=11,
                color="#F4F1E6", weight="bold", va="center", ha="center", zorder=12,
                path_effects=[PE.withStroke(linewidth=4, foreground="#0E1428")])
        return alt, az, mo.phase
    return None


def c07_card(ax):
    ctext(ax, 0.5, 0.962, "這週末抬頭看", 30, WHITE)
    ctext(ax, 0.5, 0.928, "台北　2026/12/25（五・聖誕節）晚上 8 點", 13, GREY, w="normal")
    sky_panel(ax, 0.38, 0.86, 30.0, 135.0, 65.0, "2026/12/25 20:00",
              "20:00 往東看：狼嘴、漁夫、巨人的眼睛",
              [("Aldebaran", "Úlfs kjaptr 狼嘴", RED, -0.03, -0.018),
               ("Alnilam", "Fiskikarlar 漁夫（腰帶）", BLUE, 0.0, -0.035),
               ("Capella", "五車二", PURPLE, 0.03, 0.0),
               ("Pollux", "北河三", AMBER, -0.03, -0.016),
               ("Castor", "北河二", AMBER, -0.03, 0.012),
               ("Betelgeuse", "參宿四", WHITE, -0.03, 0.0),
               ("Sirius", "天狼星", WHITE, 0.03, 0.0)],
              lines=[([26727, 26311, 25930], BLUE), (["Aldebaran", 20894, 20205, 20455, 20889], RED),
                     (["Castor", "Pollux"], AMBER)], moon=True)
    lines = [("月亮 18:33 從東北東升起，整晚就在北河三旁邊（相距約 4.5°）", WHITE),
             ("巨人 Þjazi 的眼睛＝北河二、三？Edda 沒說是哪兩顆，這是後人的猜測", GREY),
             ("晚上 10 點，畢宿五幾乎爬到頭頂（高度 81°）", WHITE),
             ("北斗的斗口晚上 8 點左右才在北北東低空露臉（後半夜才爬高）", WHITE),
             ("12/24 滿月；方位、高度、時刻：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.235 - i * 0.030, s, 11 if col != GREY else 9.5, col, w="normal")
    ctext(ax, 0.5, 0.018, "#萬國星空　#師大天文社", 12, WHITE, w="normal")


def main():
    global S, C04_CEN
    S = dict(G.load_stars(BASE))
    C04_CEN = pole_j2000(1000)
    os.makedirs(OUT, exist_ok=True)
    print("── C-A15 概念圖 ──")
    CB.emit("", [("仲冬", c01_old), ("立法", c01_law), ("今天", c01_today)], title="C-A15-01_Yule變聖誕")
    CB.emit("", [("神駒", c02_sleipnir), ("一頭", c02_one), ("八隻", c02_eight)], title="C-A15-02_八隻馴鹿")
    CB.emit("", [("太陽", c03_sun), ("月亮", c03_moon), ("神駒", c03_horses)], title="C-A15-03_天上的追逐")
    CB.emit("", [("今天", c04_today), ("一千年前", c04_1000)], title="C-A15-04_引路星一千年")
    for name, fn in [("C-A15-05_同一個V字", c05_card), ("C-A15-06_北歐星名小辭典", c06_card),
                     ("C-A15-07_這週末抬頭看", c07_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
