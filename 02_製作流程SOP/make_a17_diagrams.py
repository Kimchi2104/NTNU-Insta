# -*- coding: utf-8 -*-
"""A-17 黑腳族：留在天上的六個孩子｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A17-01 三層的帳篷（帳篷、夜空、大地）→ 02–04 鏡
C-A17-02 逃上天（熊、箭、樹叢、湖、大樹）→ 05–06 鏡
C-A17-03 羽毛女與洞（天上、洞）→ 10 鏡
C-A17-04 春天看不見（日曆、回來）→ 15 鏡（Browning：5/1 最後一次黃昏可見 → 6/24 清晨回來；10/10 回到黃昏天空）
C-A17-05 今晚與明晨（9:16 圖卡，可存圖；台北 1/15 20:00、1/16 05:30）→ 18 鏡
C-A17-06 蜘蛛人的帳篷（帳篷＝北冕、手指＝武仙〔一說〕、垂降＝蜘蛛絲＋草原上的石圈）→ 11 鏡（v2 加回）
C-A17-07 1905 年的兩顆晨星（木星、金星、太陽；Browning 1905/7/6 清晨）→ 13 鏡（v2 加回）
C-A17-08 是狗求來了雨（泉水、月亮、雨；Wissler & Duvall 1908 pp.71–72）→ 16 鏡（v2 加回）
C-A17-天上的洞（1080×1920 滿版透明：09 鏡迄格疊在北盤上，暖光圈圓心＝北極星＝畫面中心）

尊重文化的做法（逐字稿製作備註）：彩繪帳篷的圖案屬於帳篷主人——只畫「三層」的通用示意（大地、
中間留白、夜空），不重現任何真實帳篷的設計、不用 McClintock 書中照片；不畫人臉、不畫太陽舞。
故事：McClintock《The Old North Trail》1910（帳篷 pp.217–220、星星故事 pp.487–501）。
天象 PyEphem 自算（台北 25.033°N 121.565°E UTC+8；Browning 48.556°N 113.013°W UTC−7）。

執行：python3 make_a17_diagrams.py            （中文，輸出 05_素材/A-17_黑腳族/_概念圖/）
      python3 make_a17_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW
import gen_ep_assets as G
import make_a16_diagrams as D16
from make_a16_diagrams import star, cluster, sky_panel
from make_a17_v4 import SEG_LODGE, SEG_FING
from matplotlib.patches import Wedge

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-17_黑腳族/_概念圖")
CB.set_base(OUT)
RED, GREY, EARTH, HIDE = "#FF6B6B", "#7C8BA8", "#3A2E22", "#D9C3A0"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "帳篷上的三層", "c01_sub": "McClintock 1910 pp.217–220；通用示意，不重現任何一頂帳篷",
        "sky": "最上面一圈：夜空", "dipper": "北斗", "pleiades": "昴宿", "morning": "晨星（十字）",
        "middle": "中間：屬於主人的圖案（這裡不畫）",
        "earth": "最下面一圈：大地", "dusty": "塵土星＝掉下來的流星",
        "c02_title": "七兄妹逃上天", "c02_sub": "McClintock 1910 pp.488–489",
        "bear": "大熊", "arrow": "射一支箭：飛到箭落的地方", "bush": "揮羽毛：長出樹叢", "lake": "變出湖",
        "tree": "爬上大樹", "fall": "四個被撞下樹＝斗口四星",
        "c03_title": "不能挖的大蕪菁", "c03_sub": "McClintock 1910 p.492 起；羽毛女 So-at-sa-ki",
        "skyland": "天上的地面", "turnip": "大蕪菁", "hole": "從洞裡往下看：地上的家",
        "c04_title": "春天看不見走失的孩子", "c04_sub": "Browning（黑腳保留地）昴宿的看不見期；PyEphem 自算",
        "months": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], "mon": "月",
        "gone": "看不見", "yellow": "小牛皮還是黃的", "last": "5/1 最後一次黃昏可見", "back": "6/24 清晨回來",
        "brown": "秋天小牛轉成褐色：每晚回來", "oct": "10/10 回到黃昏天空",
        "c05_title": "今晚與明晨", "c05_date": "2027/1/15（五）晚上・1/16（六）清晨・台北",
        "p1": "今晚 8 點：抬頭", "p2": "明晨 5:30：往東南", "p3": "明晨 5:30：往北",
        "zenith": "頭頂", "Pleiades": "走失的孩子（昴宿）", "Venus": "晨星（金星）", "Dipper": "七兄弟和小妹（北斗）",
        "E": "東", "SE": "東南", "S": "南", "N": "北", "NE": "東北", "NW": "西北",
        "tip1": "木星 19:37 從東方升起：疤臉 Poïa", "tip2": "今晚的北斗 22:00 後才整組升起",
        "tip3": "高度、方位：PyEphem 自算（含大氣折射）", "tags": "#萬國星空　#師大天文社",
        "c06_title": "蜘蛛人的帳篷", "c06_sub": "McClintock 1910 p.500；星的位置照 HIP 星表，連線：Miller 1997",
        "lodge": "蜘蛛人的帳篷（北冕）", "fingers": "蜘蛛人的手指（武仙，一說）",
        "silk": "蜘蛛絲：把羽毛女和兒子垂降回地上", "ring": "草原上壓帳篷的石圈",
        "c07_title": "1905 年的兩顆晨星", "c07_sub": "1905/7/6 清晨，以 Browning 計算（當地 UTC−7）；PyEphem 自算；McClintock 1910 pp.499、503",
        "c07_pos": "行星位置：03:30", "jup": "01:44　Poïa（木星）先上來", "ven": "02:01　父親晨星（金星）接著升起",
        "sun": "04:36　然後是祖父太陽", "ENE": "東北東", "E2": "東",
        "c08_title": "是狗求來了雨", "c08_sub": "另一個版本：Wissler & Duvall 1908 pp.71–72",
        "spring": "地上的水被蒸乾：狗在河岸挖出泉水", "howl": "第七天，年老的白狗對天嚎叫",
        "rain": "第八天，下雨了",
    },
    "en": {
        "c01_title": "Three bands on a lodge", "c01_sub": "McClintock 1910 pp.217–220; generic sketch, no real design",
        "sky": "Top band: the night sky", "dipper": "Big Dipper", "pleiades": "Pleiades", "morning": "Morning Star (cross)",
        "middle": "Middle: the owner's design (not shown)",
        "earth": "Bottom band: the earth", "dusty": "dusty stars = fallen meteors",
        "c02_title": "Seven siblings escape to the sky", "c02_sub": "McClintock 1910 pp.488–489",
        "bear": "the bear", "arrow": "an arrow: they fly where it lands", "bush": "a feather: bushes grow",
        "lake": "a lake appears", "tree": "up the tall tree", "fall": "four knocked down = the bowl",
        "c03_title": "The turnip she must not dig", "c03_sub": "McClintock 1910 p.492 ff.; Feather Woman",
        "skyland": "the sky country", "turnip": "great turnip", "hole": "through the hole: home below",
        "c04_title": "The Lost Children vanish in spring", "c04_sub": "Pleiades at Browning (Blackfeet Reservation); PyEphem",
        "months": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], "mon": "",
        "gone": "not seen", "yellow": "calf robes still yellow", "last": "May 1: last evening view", "back": "Jun 24: back at dawn",
        "brown": "autumn, calves turn brown: back every night", "oct": "Oct 10: back in the evening sky",
        "c05_title": "Tonight and tomorrow at dawn", "c05_date": "Fri Jan 15 evening · Sat Jan 16 dawn · Taipei",
        "p1": "8 pm: look straight up", "p2": "5:30 am: look southeast", "p3": "5:30 am: look north",
        "zenith": "zenith", "Pleiades": "Lost Children (Pleiades)", "Venus": "Morning Star (Venus)",
        "Dipper": "Seven Brothers and Sister (Big Dipper)",
        "E": "E", "SE": "SE", "S": "S", "N": "N", "NE": "NE", "NW": "NW",
        "tip1": "Jupiter rises in the east at 7:37 pm: Scarface, Poïa", "tip2": "Tonight the whole Dipper is up only after 10 pm",
        "tip3": "Altitudes and azimuths: PyEphem (with refraction)", "tags": "#WorldSkyCultures #NTNUAstro",
        "c06_title": "The Spider Man's lodge", "c06_sub": "McClintock 1910 p.500; HIP positions, lines: Miller 1997",
        "lodge": "Lodge of the Spider Man (Corona Borealis)", "fingers": "Spider Man's Fingers (Hercules, uncertain)",
        "silk": "a web line lowers Feather Woman and her son", "ring": "a tipi ring of stones on the prairie",
        "c07_title": "Two morning stars, 1905", "c07_sub": "Dawn of Jul 6, 1905, computed for Browning (UTC−7); PyEphem; McClintock 1910 pp.499, 503",
        "c07_pos": "planets at 3:30 am", "jup": "1:44  Poïa (Jupiter) rises first", "ven": "2:01  his father, Morning Star (Venus)",
        "sun": "4:36  then grandfather Sun", "ENE": "ENE", "E2": "E",
        "c08_title": "The dogs brought the rain", "c08_sub": "Another version: Wissler & Duvall 1908 pp.71–72",
        "spring": "the water dried up: dogs dug a spring", "howl": "day 7: an old white dog howled to the sky",
        "rain": "day 8: rain",
    },
}


def tx(k):
    return TXT[LANG][k]


def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12, va="center"):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=c, ha=ha, va=va, weight=w, alpha=alpha, zorder=z)


def head(ax, title, sub=None):
    T(ax, 0, 0.90, title, 30, WHITE)
    if sub:
        T(ax, 0, 0.80, sub, 15, GREY, w="normal")


# ══════════════════ C-A17-01 三層的帳篷 ══════════════════
APEX, BASEY, HALF = (-0.25, 0.55), -0.62, 0.48     # 帳篷錐頂、底、半寬


def tipi_x(y):
    """帳篷某高度的左右邊界"""
    t = (APEX[1] - y) / (APEX[1] - BASEY)
    return APEX[0] - HALF * t, APEX[0] + HALF * t


def band(ax, y0, y1, fc, alpha=1.0, z=4):
    xl0, xr0 = tipi_x(y0); xl1, xr1 = tipi_x(y1)
    ax.add_patch(CB.Polygon([(xl0, y0), (xr0, y0), (xr1, y1), (xl1, y1)], closed=True, fc=fc, ec="none",
                            alpha=alpha, zorder=z))


def c01_tipi(ax):
    head(ax, tx("c01_title"), tx("c01_sub"))
    # 遠山與草原
    ax.fill([-0.95, -0.7, -0.5, -0.3, 0.0, 0.25, 0.5, 0.75, 0.95, 0.95, -0.95],
            [-0.30, -0.05, -0.18, 0.02, -0.15, -0.02, -0.20, -0.08, -0.25, -0.62, -0.62], color="#24304F", zorder=1)
    ax.fill_between([-0.95, 0.95], [-0.62, -0.62], [-0.72, -0.72], color="#3A4A2A", zorder=2)
    ax.add_patch(CB.Polygon([APEX, (APEX[0] - HALF, BASEY), (APEX[0] + HALF, BASEY)], closed=True,
                            fc=HIDE, ec="#8C6A45", lw=2, zorder=3))
    for dx in (-0.06, -0.02, 0.03, 0.07):          # 撐竿
        ax.plot([APEX[0], APEX[0] + dx], [APEX[1], APEX[1] + 0.12], c="#8C6A45", lw=2.2, zorder=3)
    ax.add_patch(CB.Polygon([(APEX[0] - 0.03, BASEY), (APEX[0] - 0.07, BASEY + 0.20), (APEX[0] + 0.07, BASEY + 0.20),
                             (APEX[0] + 0.03, BASEY)], closed=True, fc="#5C4630", ec="none", zorder=5))   # 門


def c01_sky(ax):
    y0, y1 = 0.22, 0.55
    band(ax, y0, y1 - 0.001, "#141414")
    # 北斗七點、昴宿六點、晨星十字（通用示意）
    for x, y in [(-0.38, 0.27), (-0.31, 0.29), (-0.27, 0.25), (-0.22, 0.27), (-0.17, 0.30), (-0.13, 0.27), (-0.08, 0.26)]:
        star(ax, -0.25 + (x + 0.23) * 0.55, y + 0.03, 26, WHITE, glow=False)
    cluster(ax, -0.285, 0.385, 0.018, WHITE, 16)
    ax.plot([-0.215, -0.185], [0.375, 0.375], c=AMBER, lw=3, zorder=6)
    ax.plot([-0.20, -0.20], [0.36, 0.39], c=AMBER, lw=3, zorder=6)
    T(ax, 0.30, 0.47, tx("sky"), 17, WHITE, ha="left")
    T(ax, 0.30, 0.40, tx("dipper") + "・" + tx("pleiades"), 14, WHITE, ha="left", w="normal")
    T(ax, 0.30, 0.34, tx("morning"), 14, AMBER, ha="left", w="normal")
    T(ax, 0.30, 0.02, tx("middle"), 13, GREY, ha="left", w="normal")


def c01_earth(ax):
    y0, y1 = -0.62, -0.48
    band(ax, y0, y1, "#4A2F1C")
    xl, xr = tipi_x(-0.55)
    for i in range(9):
        star(ax, xl + 0.05 + (xr - xl - 0.10) * i / 8, -0.55, 40, "#F0E0C0", glow=False)
    T(ax, 0.30, -0.46, tx("earth"), 17, WHITE, ha="left")
    T(ax, 0.30, -0.53, tx("dusty"), 14, "#F0E0C0", ha="left", w="normal")


# ══════════════════ C-A17-02 逃上天 ══════════════════
def bear(ax, x, y, s, c="#8A6A50"):
    body = [(-0.30, 0.00), (-0.25, 0.12), (-0.05, 0.17), (0.12, 0.15), (0.20, 0.10), (0.30, 0.10), (0.36, 0.05),
            (0.30, -0.02), (0.22, -0.02), (0.20, -0.20), (0.13, -0.20), (0.10, -0.06), (-0.12, -0.06),
            (-0.14, -0.20), (-0.21, -0.20), (-0.23, -0.04), (-0.30, 0.00)]
    ax.add_patch(CB.Polygon([(x + a * s, y + b * s) for a, b in body], closed=True, fc=c, ec="none", zorder=6))
    ax.add_patch(CB.Circle((x + 0.24 * s, y + 0.135 * s), 0.025 * s, fc=c, ec="none", zorder=6))   # 耳


def c02_bear(ax):
    head(ax, tx("c02_title"), tx("c02_sub"))
    ax.plot([-0.95, 0.95], [-0.62, -0.62], c="#D9B48A", lw=2, alpha=.6, zorder=2)
    bear(ax, -0.62, -0.45, 0.9)
    T(ax, -0.62, -0.72, tx("bear"), 16, "#C8A88A")


def c02_arrow(ax):
    xs = [-0.30 + 0.60 * k / 40 for k in range(41)]
    ys = [0.30 + 0.25 * math.sin(math.pi * k / 40) for k in range(41)]
    ax.plot(xs, ys, c=AMBER, lw=2, ls=(0, (5, 4)), zorder=5)
    ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-3], ys[-3]),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2))
    T(ax, 0.0, 0.66, tx("arrow"), 15, AMBER)


def c02_bush(ax):
    for x, y, r in [(-0.30, -0.05, 0.07), (-0.20, -0.02, 0.09), (-0.10, -0.06, 0.06)]:
        ax.add_patch(CB.Circle((x, y), r, fc="#3E7A4A", ec="none", zorder=5))
    T(ax, -0.20, -0.20, tx("bush"), 14, GREEN)


def c02_lake(ax):
    ax.add_patch(CB.Ellipse((0.15, -0.40), 0.42, 0.13, fc="#2E5C9A", ec=BLUE, lw=1.5, zorder=5))
    T(ax, 0.15, -0.53, tx("lake"), 14, BLUE)


def c02_tree(ax):
    tx0 = 0.66
    ax.plot([tx0, tx0], [-0.62, 0.25], c="#7A5A3A", lw=10, zorder=5, solid_capstyle="butt")
    for dy, w in ((0.10, 0.22), (-0.05, 0.26), (-0.20, 0.22)):
        ax.plot([tx0 - w / 2, tx0 + w / 2], [dy + 0.03, dy - 0.03], c="#7A5A3A", lw=4, zorder=5)
    ax.add_patch(CB.Ellipse((tx0, 0.25), 0.36, 0.22, fc="#2F6B3C", ec="none", zorder=4))
    pts = [(tx0 - 0.10, 0.28), (tx0 - 0.03, 0.31), (tx0 + 0.04, 0.29), (tx0 + 0.11, 0.26)]
    for p in pts:
        star(ax, *p, 60, WHITE)
    for k, (fx, fy) in enumerate([(0.48, -0.10), (0.44, -0.24), (0.86, -0.12), (0.88, -0.30)]):
        star(ax, fx, fy, 60, WHITE, alpha=.55)
        ax.annotate("", xy=(fx, fy - 0.08), xytext=(fx, fy - 0.01),
                    arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.2, alpha=.5))
    T(ax, tx0, 0.45, tx("tree"), 15, WHITE)
    T(ax, tx0, -0.72, tx("fall"), 13, GREY, w="normal")


# ══════════════════ C-A17-03 羽毛女與洞 ══════════════════
def c03_sky(ax):
    head(ax, tx("c03_title"), tx("c03_sub"))
    ax.add_patch(CB.Polygon([(-0.95, -0.05), (0.95, -0.05), (0.75, 0.30), (-0.75, 0.30)], closed=True,
                            fc="#2A2F4E", ec="#6F7AA8", lw=1.5, zorder=2))
    T(ax, -0.62, 0.38, tx("skyland"), 15, "#AFB8DD")
    # 大蕪菁：葉＋露出的根頭
    for a in (-35, -10, 15, 40):
        ax.add_patch(CB.Ellipse((0.40 + 0.06 * math.sin(math.radians(a)), 0.30), 0.06, 0.24, angle=a,
                                fc="#5FA05A", ec="none", zorder=4))
    ax.add_patch(CB.Ellipse((0.40, 0.15), 0.16, 0.10, fc="#E9D9F0", ec="#B79ACB", lw=1.2, zorder=5))
    T(ax, 0.40, 0.48, tx("turnip"), 15, PURPLE)


def c03_hole(ax):
    hx, hy = 0.05, 0.10
    ax.add_patch(CB.Ellipse((hx, hy), 0.42, 0.13, fc="#0B0F1E", ec="#D9B48A", lw=2.5, zorder=6))
    # 從洞往下：一個圓形視窗裡的草原與帳篷
    cx, cy, r = 0.05, -0.48, 0.30
    ax.add_patch(CB.Circle((cx, cy), r, fc="#1D2B4A", ec="#D9B48A", lw=2, zorder=3))
    ax.add_patch(CB.Rectangle((cx - r * 0.98, cy - r), 2 * r * 0.98, r * 0.85, fc="#3A5A30", ec="none", zorder=4,
                              clip_on=True))
    for k, dx in enumerate((-0.14, 0.0, 0.13)):
        b = cy - 0.12 + 0.02 * (k % 2)
        ax.add_patch(CB.Polygon([(cx + dx, b + 0.13), (cx + dx - 0.06, b), (cx + dx + 0.06, b)], closed=True,
                                fc=HIDE, ec="#8C6A45", lw=1, zorder=5))
    for k in (-1, 1):
        ax.plot([hx + k * 0.20, cx + k * r * 0.96], [hy - 0.03, cy + 0.06], c="#D9B48A", lw=1, alpha=.4,
                ls=(0, (3, 4)), zorder=2)
    T(ax, 0.55, -0.48, tx("hole"), 15, WHITE, ha="left")


# ══════════════════ C-A17-04 春天看不見 ══════════════════
X0, X1, YB = -0.85, 0.85, 0.05


def dx_of(m, d):
    doy = sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:m - 1]) + d - 1
    return X0 + (X1 - X0) * doy / 365.0


def c04_cal(ax):
    head(ax, tx("c04_title"), tx("c04_sub"))
    ax.add_patch(CB.Rectangle((X0, YB - 0.04), X1 - X0, 0.08, fc="#2A3560", ec="none", zorder=2))
    a, b = dx_of(5, 1), dx_of(6, 24)
    ax.add_patch(CB.Rectangle((a, YB - 0.04), b - a, 0.08, fc="#555A66", ec="none", zorder=3))
    for m in range(1, 13):
        x = dx_of(m, 1)
        ax.plot([x, x], [YB - 0.05, YB + 0.05], c=WHITE, lw=1, alpha=.4, zorder=4)
        T(ax, dx_of(m, 16), YB - 0.10, tx("months")[m - 1] + tx("mon"), 12, GREY, w="normal")
    cluster(ax, (a + b) / 2, YB + 0.17, 0.03, GREY, 22, alpha=.5)
    T(ax, (a + b) / 2, YB + 0.29, tx("gone"), 17, GREY)
    T(ax, a - 0.02, YB - 0.22, tx("last"), 13, WHITE, ha="right", w="normal")
    T(ax, b + 0.02, YB - 0.22, tx("back"), 13, WHITE, ha="left", w="normal")
    ax.add_patch(CB.Ellipse(((a + b) / 2, YB - 0.42), 0.20, 0.10, fc="#E8C35A", ec="none", zorder=4))
    T(ax, (a + b) / 2, YB - 0.54, tx("yellow"), 14, "#E8C35A")


def c04_back(ax):
    c = dx_of(10, 10)
    cluster(ax, c, YB + 0.17, 0.03, AMBER, 26)
    T(ax, c, YB + 0.29, tx("oct"), 13, AMBER)
    ax.add_patch(CB.Ellipse((c, YB - 0.42), 0.20, 0.10, fc="#7A4A2A", ec="none", zorder=4))
    T(ax, 0.0, -0.72, tx("brown"), 16, "#D9A070")


# ══════════════════ C-A17-05 今晚與明晨（9:16） ══════════════════
def altaz(when, names=(), fixed=()):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.pressure, o.temp = 1010, 15
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    out = {}
    for n in names:
        b = getattr(ephem, n)() if n in ("Venus", "Jupiter") else ephem.star(n)
        b.compute(o); out[n] = (math.degrees(b.alt), math.degrees(b.az))
    S = dict(G.load_stars(BASE))
    for nm, h in fixed:
        b = ephem.FixedBody(); b._ra, b._dec, b._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        b.compute(o); out[nm] = (math.degrees(b.alt), math.degrees(b.az))
    return out


def c05_card(ax):
    T(ax, 0.5, 0.955, tx("c05_title"), 30, WHITE)
    T(ax, 0.5, 0.920, tx("c05_date"), 13, GREY, w="normal")
    # ① 今晚 20:00 頭頂：昴宿（天頂圓盤示意）
    A = altaz("2027/1/15 20:00", names=("Alcyone",))
    alt = A["Alcyone"][0]
    cx, cy, r = 0.5, 0.775, 0.085
    T(ax, 0.5, 0.885, tx("p1"), 15, WHITE)
    ax.add_patch(CB.Ellipse((cx, cy), 2 * r * 1.15, 2 * r * 1.15 * CB.CARD_W / CB.CARD_H, fc="#10162C", ec=WHITE,
                            lw=1, zorder=1))
    rr = r * (90 - alt) / 30
    cluster(ax, cx, cy + rr * 0.6, 0.012, AMBER, 14)
    ax.plot([cx - 0.008, cx + 0.008], [cy, cy], c=GREY, lw=1); ax.plot([cx, cx], [cy - 0.005, cy + 0.005], c=GREY, lw=1)
    T(ax, cx + 0.12, cy + 0.012, tx("Pleiades"), 12, AMBER, ha="left")
    T(ax, cx + 0.12, cy - 0.012, f"{alt:.1f}°（{tx('zenith')}）", 10, GREY, ha="left", w="normal")
    # ② 明晨 05:30 東南：金星
    B = altaz("2027/1/16 05:30", names=("Venus", "Dubhe", "Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid"))
    mk = lambda n, lab="", col=WHITE, dx=0.0, dy=0.03, ha="center": (B[n][0], B[n][1], lab, col, dx, dy, ha)
    sky_panel(ax, 0.40, 0.625, 95, 165, 40, tx("p2"), {"Venus": mk("Venus", tx("Venus"), AMBER, 0.0, 0.04)}, [],
              [(tx("SE"), 135)])
    # ③ 明晨 05:30 往北：北斗
    north = {n: mk(n) for n in ("Merak", "Phecda", "Megrez", "Alioth", "Mizar")}
    north["Dubhe"] = mk("Dubhe", tx("Dipper"), AMBER, 0.0, -0.05)
    north["Alkaid"] = mk("Alkaid", "", AMBER)
    sky_panel(ax, 0.115, 0.345, 315, 75, 75, tx("p3"), north,
              [(["Dubhe", "Merak", "Phecda", "Megrez", "Dubhe"], AMBER), (["Megrez", "Alioth", "Mizar", "Alkaid"], AMBER)],
              [(tx("NW"), 320), (tx("N"), 0), (tx("NE"), 45)])
    for i, (k, col) in enumerate((("tip1", AMBER), ("tip2", WHITE), ("tip3", GREY))):
        T(ax, 0.5, 0.085 - i * 0.02, tx(k), 11 if col != GREY else 9.5, col, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 12, WHITE, w="normal")
    print(f"  昴宿六 20:00 {alt:.1f}°；05:30 金星 {B['Venus'][0]:.1f}°/{B['Venus'][1]:.0f}°、天樞 {B['Dubhe'][0]:.1f}°、"
          f"搖光 {B['Alkaid'][0]:.1f}°")


# ══════════════════ 天上的洞（1080×1920 滿版透明） ══════════════════
def hole_overlay(c=(540.0, 960.0)):
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(5.4, 9.6), dpi=200)
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1080); ax.set_ylim(1920, 0); ax.axis("off")
    f.patch.set_alpha(0); ax.patch.set_alpha(0)
    for rr, al in ((150, .06), (110, .10), (80, .16), (58, .24)):
        ax.add_patch(CB.Circle(c, rr, fc="#FFD27A", ec="none", alpha=al))
    ax.add_patch(CB.Circle(c, 42, fc="none", ec="#FFE3A0", lw=3, alpha=.8))
    os.makedirs(OUT, exist_ok=True)
    f.savefig(os.path.join(OUT, "C-A17-天上的洞_透明.png"), transparent=True); plt.close(f)
    print("  ✓ C-A17-天上的洞_透明.png")


# ══════════════════ C-A17-06 蜘蛛人的帳篷（11 鏡，v2 加回） ══════════════════
C06_RA0, C06_DEC0, C06_SC = 256.0, 27.5, 0.025      # 視野中心（北冕與武仙之間）、每度 0.034 單位


def c06_xy(ra, dec):
    """切面（gnomonic）投影：東在左、北在上；回傳圖面座標（上半部天空）"""
    a, d, a0, d0 = map(math.radians, (ra, dec, C06_RA0, C06_DEC0))
    cc = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / cc
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / cc
    k = C06_SC * 180 / math.pi
    return -x * k, 0.12 + y * k


def c06_stars(ax, segs, col, maglim=4.6):
    S = dict(G.load_stars(BASE))
    hips = sorted({h for sg in segs for h in sg if h in S})
    for sg in segs:
        pts = [c06_xy(*S[h][:2]) for h in sg if h in S]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=2.2, alpha=.85, zorder=5)
    for h in hips:
        ra, dec, v = S[h][:3]
        x, y = c06_xy(ra, dec)
        star(ax, x, y, max(14, 120 * 10 ** (-0.32 * (v - 1.5))), WHITE)
    return [c06_xy(*S[h][:2]) for h in hips]


def c06_lodge(ax):
    head(ax, tx("c06_title"), tx("c06_sub"))
    S = dict(G.load_stars(BASE))
    for h, (ra, dec, v) in ((h, S[h][:3]) for h in S):      # 背景淡星
        if v < 4.8 and abs(ra - C06_RA0) < 38 and abs(dec - C06_DEC0) < 22:
            x, y = c06_xy(ra, dec)
            if -0.95 < x < 0.95 and -0.15 < y < 0.70:
                star(ax, x, y, 8, GREY, glow=False, alpha=.55, z=3)
    pts = c06_stars(ax, SEG_LODGE, PURPLE)
    x = sum(p[0] for p in pts) / len(pts); y = min(p[1] for p in pts)
    T(ax, x, y - 0.09, tx("lodge"), 16, PURPLE)


def c06_fingers(ax):
    pts = c06_stars(ax, SEG_FING, BLUE)
    x = sum(p[0] for p in pts) / len(pts); y = max(p[1] for p in pts)
    T(ax, x, min(y + 0.07, 0.66), tx("fingers"), 15, BLUE)


def c06_silk(ax):
    S = dict(G.load_stars(BASE))
    lx, ly = c06_xy(*S[76267][:2])                 # 貫索四（帳篷的門口那顆最亮的）
    gx, gy = lx, -0.58                             # 地上的石圈
    ax.plot([lx, gx], [ly - 0.03, gy + 0.11], c=WHITE, lw=1.0, alpha=.6, ls=(0, (2, 3)), zorder=4)
    ax.fill_between([-0.95, 0.95], [-0.60, -0.60], [-0.80, -0.80], color="#3A4A2A", zorder=2)
    ax.add_patch(CB.Ellipse((gx, gy - 0.08), 0.62, 0.13, fc="#4A5C36", ec="none", zorder=3))
    for k in range(18):
        a = 2 * math.pi * k / 18
        ax.add_patch(CB.Ellipse((gx + 0.27 * math.cos(a), gy - 0.08 + 0.05 * math.sin(a)), 0.035, 0.022,
                                fc="#B8B0A0", ec="#6E675C", lw=0.8, zorder=4))
    T(ax, gx - 0.33, gy - 0.08, tx("ring"), 14, "#D8D0C0", ha="right", w="normal")
    T(ax, lx - 0.04, (ly + gy) / 2 - 0.05, tx("silk"), 13, WHITE, ha="right", w="normal")


# ══════════════════ C-A17-07 1905 年的兩顆晨星（13 鏡，v2 加回） ══════════════════
AZ0, AZ1, ALT1 = 30.0, 110.0, 32.0                 # 面向東北東：方位 30°–110°、高度 0–32°


def c07_xy(alt, az):
    return -0.88 + 1.76 * (az - AZ0) / (AZ1 - AZ0), -0.40 + 0.95 * alt / ALT1


def c07_ephem():
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "48.556", "-113.013"; o.pressure, o.temp = 1010, 15
    o.date = ephem.Date("1905/7/6 07:00")                  # 當地 00:00（UTC−7）
    rise = {n: ephem.Date(o.next_rising(getattr(ephem, n)()) - 7 * ephem.hour) for n in ("Jupiter", "Venus", "Sun")}
    o.date = ephem.Date("1905/7/6 10:30")                  # 當地 03:30
    pos = {}
    for n in ("Jupiter", "Venus"):
        b = getattr(ephem, n)(); b.compute(o); pos[n] = (math.degrees(b.alt), math.degrees(b.az))
    sun = ephem.Sun(); o.date = ephem.Date(rise["Sun"] + 7 * ephem.hour); sun.compute(o)
    pos["Sun"] = (0.0, math.degrees(sun.az))
    return rise, pos


C07 = {}


def c07_data():
    if not C07:
        r, p = c07_ephem(); C07.update(rise=r, pos=p)
        print("  1905/7/6 Browning 升起：" + "、".join(f"{k} {str(v)[-8:-3]}" for k, v in r.items())
              + f"；03:30 木星 {p['Jupiter'][0]:.1f}°/{p['Jupiter'][1]:.0f}°、金星 {p['Venus'][0]:.1f}°/{p['Venus'][1]:.0f}°")
    return C07


def c07_jup(ax):
    head(ax, tx("c07_title"), tx("c07_sub"))
    d = c07_data()
    ax.fill_between([-0.95, 0.95], [-0.40, -0.40], [-0.75, -0.75], color="#1E2A1C", zorder=2)
    ax.plot([-0.95, 0.95], [-0.40, -0.40], c="#D9B48A", lw=1.5, alpha=.7, zorder=3)
    for lab, az in ((tx("NE"), 45), (tx("ENE"), 67.5), (tx("E2"), 90)):
        x, _ = c07_xy(0, az)
        T(ax, x, -0.47, lab, 13, GREY, w="normal")
    T(ax, 0.88, 0.62, tx("c07_pos"), 12, GREY, ha="right", w="normal")
    x, y = c07_xy(*d["pos"]["Jupiter"])
    star(ax, x, y, 150, AMBER)
    T(ax, x - 0.05, y + 0.07, tx("jup"), 15, AMBER, ha="right")


def c07_ven(ax):
    d = c07_data()
    x, y = c07_xy(*d["pos"]["Venus"])
    star(ax, x, y, 260, WHITE)
    T(ax, x + 0.05, y - 0.07, tx("ven"), 15, WHITE, ha="left")


def c07_sun(ax):
    d = c07_data()
    x, y = c07_xy(*d["pos"]["Sun"])
    for rr, al in ((0.22, .10), (0.15, .18), (0.09, .35)):
        ax.add_patch(Wedge((x, -0.40), rr, 0, 180, fc="#FFB347", ec="none", alpha=al, zorder=4))
    T(ax, x, -0.58, tx("sun"), 15, "#FFB347")


# ══════════════════ C-A17-08 是狗求來了雨（16 鏡，v2 加回） ══════════════════
DOG = [(-0.30, 0.00), (-0.26, 0.10), (0.10, 0.12), (0.18, 0.16), (0.24, 0.30), (0.30, 0.36), (0.34, 0.33),
       (0.31, 0.25), (0.33, 0.18), (0.28, 0.08), (0.22, 0.02), (0.20, -0.20), (0.15, -0.20), (0.13, -0.04),
       (-0.16, -0.04), (-0.18, -0.20), (-0.23, -0.20), (-0.25, -0.02), (-0.36, 0.08), (-0.38, 0.06), (-0.30, 0.00)]
DOG_DIG = [(-0.30, 0.06), (-0.26, 0.14), (0.08, 0.12), (0.16, 0.06), (0.26, -0.02), (0.30, -0.10), (0.24, -0.12),
           (0.16, -0.06), (0.14, -0.20), (0.09, -0.20), (0.06, -0.06), (-0.16, -0.02), (-0.18, -0.20),
           (-0.23, -0.20), (-0.26, 0.00), (-0.34, 0.14), (-0.36, 0.12), (-0.30, 0.06)]


def dog(ax, x, y, s, shape, c):
    ax.add_patch(CB.Polygon([(x + a * s, y + b * s) for a, b in shape], closed=True, fc=c, ec="none", zorder=6))


def c08_spring(ax):
    head(ax, tx("c08_title"), tx("c08_sub"))
    ax.fill_between([-0.95, 0.95], [-0.45, -0.45], [-0.78, -0.78], color="#5A4630", zorder=2)
    for k in range(9):                                       # 乾裂的地面
        x = -0.85 + 0.2 * k
        ax.plot([x, x + 0.06, x + 0.02], [-0.50, -0.60, -0.70], c="#3A2E22", lw=1.2, zorder=3)
    dog(ax, -0.50, -0.28, 0.75, DOG_DIG, "#8C7A66")
    ax.add_patch(CB.Ellipse((-0.26, -0.47), 0.20, 0.06, fc="#2E5C9A", ec=BLUE, lw=1.2, zorder=5))
    T(ax, -0.40, -0.66, tx("spring"), 14, BLUE)


def c08_moon(ax):
    ax.add_patch(CB.Circle((0.55, 0.52), 0.10, fc="#F2EBD0", ec="none", zorder=4))
    ax.add_patch(CB.Circle((0.55, 0.52), 0.16, fc="#F2EBD0", ec="none", alpha=.10, zorder=3))
    dog(ax, 0.40, -0.28, 0.75, DOG, "#E8E4DC")
    for k in range(3):                                       # 嚎叫的聲波
        ax.add_patch(CB.Arc((0.67, 0.02), 0.10 + 0.08 * k, 0.10 + 0.08 * k, angle=45, theta1=-40, theta2=40,
                            ec=WHITE, lw=1.2, alpha=.6 - 0.15 * k, zorder=5))
    T(ax, 0.40, -0.52, tx("howl"), 14, WHITE)


def c08_rain(ax):
    rnd = random.Random(8)
    for _ in range(70):
        x = rnd.uniform(-0.9, 0.9); y = rnd.uniform(-0.40, 0.62)
        ax.plot([x, x - 0.015], [y, y - 0.06], c=BLUE, lw=1.2, alpha=.55, zorder=7)
    T(ax, 0.0, 0.70, tx("rain"), 18, BLUE)


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A17 概念圖 ──")
    CB.emit("", [("帳篷", c01_tipi), ("夜空", c01_sky), ("大地", c01_earth)], title="C-A17-01_三層的帳篷")
    CB.emit("", [("熊", c02_bear), ("箭", c02_arrow), ("樹叢", c02_bush), ("湖", c02_lake), ("大樹", c02_tree)],
            title="C-A17-02_逃上天")
    CB.emit("", [("天上", c03_sky), ("洞", c03_hole)], title="C-A17-03_羽毛女與洞")
    CB.emit("", [("日曆", c04_cal), ("回來", c04_back)], title="C-A17-04_春天看不見")
    CB.emit("", [("帳篷", c06_lodge), ("手指", c06_fingers), ("垂降", c06_silk)], title="C-A17-06_蜘蛛人的帳篷")
    CB.emit("", [("木星", c07_jup), ("金星", c07_ven), ("太陽", c07_sun)], title="C-A17-07_1905年的兩顆晨星")
    CB.emit("", [("泉水", c08_spring), ("月亮", c08_moon), ("雨", c08_rain)], title="C-A17-08_是狗求來了雨")
    fig, ax = CB.newcard(dark=True)
    c05_card(ax)
    CB.save(fig, "", "C-A17-05_今晚與明晨_圖卡.png", transparent=False)
    if LANG == "zh":
        hole_overlay()


if __name__ == "__main__":
    main()
