# -*- coding: utf-8 -*-
"""A-16 納瓦荷：只在冬天說的星星故事｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A16-01 冬天才說的故事（日曆環、今天、睡、昴宿）→ 02–03 鏡（日曆環→今天→睡）、12 鏡（日曆環＋昴宿）
C-A16-02 黑神的晶石（hooghan、腳踝、膝、腰、肩、太陽穴）→ 05–06 鏡
C-A16-03 郊狼吹散星星（郊狼、吹散）→ 14 鏡
C-A16-04 規矩與混亂（混亂、規矩）→ 15 鏡
C-A16-05 今晚十一點（9:16 圖卡，可存圖；台北 2027/1/8 23:00）→ 19 鏡
C-A16-06 播種（地平線、作物）→ 11 鏡
C-A16-07 郊狼的星（地平線、WindowRock、台北）→ 16 鏡
C-A16-hooghan（1080×1920 滿版透明：09 鏡迄格疊在北盤上，八角形圓心＝北極星＝畫面中心）

尊重文化的做法（逐字稿製作備註）：不畫黑神或任何神聖的人們的形象、不畫人形；不用沙畫或沙畫照片，
大地母親／天空父親只用兩個抽象色塊；郊狼只畫側面剪影、不擬人。
天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E UTC+8 15°C／1010 hPa；Window Rock 35.68°N 109.05°W）。
故事：Childrey《Star Trails: Navajo》2004 pp.29–39、54、58、72；冬天才說：Navajo Skies 導覽手冊。

執行：python3 make_a16_diagrams.py            （中文，輸出 05_素材/A-16_納瓦荷/_概念圖/）
      python3 make_a16_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-16_納瓦荷/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL, EARTH = "#FF6B6B", "#7C8BA8", "#1B2240", "#3A2E22"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "天上的故事，只在冬天說", "c01_sub": "Navajo Skies 導覽手冊；一年只分夏、冬兩季",
        "months": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
        "frost": "初霜", "frost2": "冬天開始", "thunder": "春雷", "thunder2": "停止說故事",
        "season": "說故事的季節", "summer": "夏天：先收藏",
        "today": "今天 1/8",
        "sleep1": "冬天：蛇和蜘蛛都睡了", "sleep2": "故事不會驚動它們（一種說法）",
        "ple1": "十月中：昴宿黃昏東升", "ple2": "冬天的儀式開始", "ple3": "春雷一響：儀式結束",
        "c02_title": "黑神的晶石", "c02_sub": "Childrey 2004（依 Nightway 傳統）；不畫人形、不用沙畫",
        "hooghan": "hooghan（第一座泥土屋）", "door": "門朝東", "earth": "大地母親", "sky": "天空父親",
        "abstract": "抽象色塊示意",
        "steps": ["腳踝", "膝蓋", "腰", "肩膀", "太陽穴"], "stars": "「這叫星星」",
        "c03_title": "郊狼搶走了鹿皮袋", "c03_sub": "Childrey 2004 pp.37–39", "bag": "鹿皮袋",
        "blow": "呼——",
        "c04_title": "規矩，在混亂裡面", "chaos": "郊狼撒出的混亂", "order": "黑神排好的規矩",
        "c04_foot": "大部分的星都沒有名字",
        "c06_title": "五月初的黃昏", "west": "西", "slim": "第一個瘦長的人（獵戶）沉向西方",
        "crops": ["玉米", "豆子", "南瓜", "菸草"], "sow": "該播種了",
        "c06_foot": "Childrey 2004 p.58；Window Rock 5/1 民用昏影結束：參宿四 29°、參宿七 11.5°（自算）",
        "c07_title": "郊狼的星：老人星有多高？", "south": "南",
        "wr": "Window Rock", "wr2": "（納瓦荷族政府所在地）", "tp": "台北",
        "wr_alt": "最高 1.6°", "tp_alt": "最高 12.3°",
        "c07_foot": "老人星中天的幾何高度（PyEphem 自算）；貼地平線時大氣消光很重",
        "c05_title": "今晚十一點", "c05_date": "2027/1/8（五）新月・台北",
        "north_panel": "往北看：旋轉的男人和女人繞著北火", "south_panel": "往南看：郊狼的星",
        "N": "北", "NE": "東北", "NW": "西北", "S": "南", "SE": "東南", "SW": "西南",
        "Polaris": "北火（北極星）", "Dipper": "旋轉的男人（北斗）", "Cas": "旋轉的女人（仙后座）",
        "Sirius": "天狼星", "Canopus": "郊狼的星（老人星）", "Orion": "第一個瘦長的人（獵戶）",
        "tip1": "找南方沒有高樓、山擋住的地方", "tip2": "北斗勺柄這時還很低，午夜後比較高",
        "tip3": "整夜無月（新月 1/8 04:24）", "tip4": "高度、方位：PyEphem 自算（含大氣折射）",
        "tags": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Sky stories are told only in winter", "c01_sub": "Navajo Skies guide; the year has two seasons",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "frost": "First frost", "frost2": "winter begins", "thunder": "First thunder", "thunder2": "stories stop",
        "season": "Storytelling season", "summer": "Summer: save it for later",
        "today": "Today, Jan 8",
        "sleep1": "In winter, snakes and spiders sleep", "sleep2": "the stories won't disturb them (one telling)",
        "ple1": "Mid-Oct: Pleiades rise at dusk", "ple2": "winter ceremonies begin", "ple3": "First thunder: they end",
        "c02_title": "Black God's crystals", "c02_sub": "Childrey 2004 (Nightway tradition); no figures, no sandpainting",
        "hooghan": "hooghan (the first earth lodge)", "door": "door faces east", "earth": "Mother Earth",
        "sky": "Father Sky", "abstract": "abstract blocks only",
        "steps": ["ankle", "knee", "hip", "shoulder", "temple"], "stars": "“They are called stars”",
        "c03_title": "Coyote grabs the fawnskin pouch", "c03_sub": "Childrey 2004 pp.37–39", "bag": "pouch",
        "blow": "Whoosh—",
        "c04_title": "Order inside the chaos", "chaos": "Coyote's scattered chaos", "order": "Black God's order",
        "c04_foot": "Most stars have no names",
        "c06_title": "Early May, at dusk", "west": "W", "slim": "First Slim One (Orion) sinks in the west",
        "crops": ["corn", "beans", "squash", "tobacco"], "sow": "time to plant",
        "c06_foot": "Childrey 2004 p.58; Window Rock May 1, end of civil twilight: Betelgeuse 29°, Rigel 11.5°",
        "c07_title": "Coyote Star: how high is Canopus?", "south": "S",
        "wr": "Window Rock", "wr2": "(Navajo Nation capital)", "tp": "Taipei",
        "wr_alt": "max 1.6°", "tp_alt": "max 12.3°",
        "c07_foot": "Geometric altitude of Canopus at transit (PyEphem); heavy extinction near the horizon",
        "c05_title": "Tonight at 11 pm", "c05_date": "Fri Jan 8, 2027 · new moon · Taipei",
        "north_panel": "Look north: the Revolving Male and Female", "south_panel": "Look south: the Coyote Star",
        "N": "N", "NE": "NE", "NW": "NW", "S": "S", "SE": "SE", "SW": "SW",
        "Polaris": "North Fire (Polaris)", "Dipper": "Revolving Male (Big Dipper)",
        "Cas": "Revolving Female (Cassiopeia)", "Sirius": "Sirius", "Canopus": "Coyote Star (Canopus)",
        "Orion": "First Slim One (Orion)",
        "tip1": "Find a southern horizon free of buildings and hills", "tip2": "The Dipper's handle is still low; higher after midnight",
        "tip3": "No moon all night (new moon Jan 8, 04:24)", "tip4": "Altitudes and azimuths: PyEphem (with refraction)",
        "tags": "#WorldSkyCultures #NTNUAstro",
    },
}


def tx(k):
    return TXT[LANG][k]


def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12, va="center"):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=c, ha=ha, va=va, weight=w,
            alpha=alpha, zorder=z)


def head(ax, title, sub=None):
    T(ax, 0, 0.90, title, 30, WHITE)
    if sub:
        T(ax, 0, 0.80, sub, 15, GREY, w="normal")


def star(ax, x, y, s=60, c=WHITE, z=8, glow=True, alpha=1.0):
    if glow:
        ax.scatter([x], [y], s=s * 5, c=c, alpha=0.15 * alpha, zorder=z - 1, lw=0)
    ax.scatter([x], [y], s=s, c=c, zorder=z, lw=0, alpha=alpha)


PLE_SHAPE = [(0, 0), (-0.55, 0.25), (-0.95, 0.05), (-0.45, -0.35), (0.35, 0.55), (0.75, 0.15), (0.25, -0.65)]


def cluster(ax, x, y, s=0.05, c=WHITE, size=40, alpha=1.0):
    for dx, dy in PLE_SHAPE:
        star(ax, x + dx * s, y + dy * s, size, c, alpha=alpha)


# ══════════════════ C-A16-01 冬天才說的故事 ══════════════════
R1, C1 = 0.56, (0.0, -0.06)


def ang(m, d=1):
    """月 m 日 d 在環上的角度（一月在上、順時針）"""
    return math.radians(90 - ((m - 1) + (d - 1) / 30.0) * 30)


def on(r, a):
    return C1[0] + r * math.cos(a), C1[1] + r * math.sin(a)


def arc(ax, a0, a1, r, **kw):
    n = 120
    xs, ys = zip(*[on(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)])
    ax.plot(xs, ys, **kw)


def c01_ring(ax):
    head(ax, tx("c01_title"), tx("c01_sub"))
    # 夏天（3/1 → 10/15）淡灰虛線；冬天（10/15 → 3/1）藍色粗弧
    arc(ax, ang(3, 1), ang(10, 15) - 0, R1, c=GREY, lw=3, alpha=.45, ls=(0, (4, 5)), zorder=3)
    arc(ax, ang(10, 15), ang(3, 1) - 2 * math.pi, R1, c=BLUE, lw=11, alpha=.9, solid_capstyle="round", zorder=4)
    for m in range(1, 13):
        a = ang(m)
        x0, y0 = on(R1 - 0.035, a); x1, y1 = on(R1 + 0.035, a)
        ax.plot([x0, x1], [y0, y1], c=WHITE, lw=1.4, alpha=.6, zorder=5)
        xm, ym = on(R1 - 0.10, ang(m, 16))
        T(ax, xm, ym, tx("months")[m - 1], 13, WHITE if m in (10, 11, 12, 1, 2) else GREY, w="normal")
    # 初霜（十月中）
    fx, fy = on(R1, ang(10, 15))
    ax.scatter([fx], [fy], s=260, marker=(6, 2, 0), c=WHITE, lw=2.2, zorder=7)
    T(ax, fx - 0.07, fy + 0.03, tx("frost"), 19, WHITE, ha="right")
    T(ax, fx - 0.07, fy - 0.045, tx("frost2"), 13, GREY, ha="right", w="normal")
    # 春雷（二月底、三月初）
    tx_, ty_ = on(R1, ang(3, 1))
    bolt = [(0.02, 0.05), (-0.012, 0.0), (0.012, 0.0), (-0.02, -0.05)]
    ax.plot([tx_ + a for a, _ in bolt], [ty_ + b for _, b in bolt], c=AMBER, lw=3, zorder=7)
    T(ax, tx_ + 0.06, ty_ + 0.04, tx("thunder"), 19, AMBER, ha="left")
    T(ax, tx_ + 0.06, ty_ - 0.025, tx("thunder2"), 13, GREY, ha="left", w="normal")
    # 季節字
    sx, sy = on(R1 + 0.10, ang(11, 20))
    T(ax, sx, sy, tx("season"), 18, BLUE, ha="right")
    gx, gy = on(R1 + 0.10, ang(6, 25))
    T(ax, gx, gy, tx("summer"), 15, GREY, ha="right", w="normal")


def c01_today(ax):
    x, y = on(R1, ang(1, 8))
    star(ax, x, y, 260, AMBER)
    T(ax, x + 0.05, y + 0.10, tx("today"), 19, AMBER, ha="left")


def c01_sleep(ax):
    cx, cy = C1[0], C1[1] - 0.02
    # 月亮（新月形）
    ax.add_patch(CB.Circle((cx - 0.20, cy + 0.17), 0.075, fc="#E8E2C8", ec="none", zorder=6))
    ax.add_patch(CB.Circle((cx - 0.17, cy + 0.19), 0.068, fc=CB.BG, ec="none", zorder=7))
    T(ax, cx - 0.08, cy + 0.22, "z", 14, GREY, w="normal")
    T(ax, cx - 0.04, cy + 0.26, "z", 17, GREY, w="normal")
    T(ax, cx + 0.01, cy + 0.31, "Z", 20, GREY, w="normal")
    # 蛇（蜷著）
    th = [i / 60 * 4 * math.pi for i in range(61)]
    ax.plot([cx - 0.17 + 0.012 * t * math.cos(t) * 0.55 for t in th],
            [cy - 0.02 + 0.012 * t * math.sin(t) * 0.55 for t in th], c=GREEN, lw=3, zorder=6)
    # 蜘蛛
    sx, sy = cx + 0.02, cy - 0.02
    ax.add_patch(CB.Circle((sx, sy), 0.028, fc=PURPLE, ec="none", zorder=6))
    for k in range(4):
        for sgn in (-1, 1):
            a = math.radians(30 + 25 * k)
            ax.plot([sx, sx + sgn * 0.06 * math.cos(a - 0.6), sx + sgn * 0.075 * math.cos(a - 0.3)],
                    [sy, sy + 0.05 * math.sin(a) - 0.02, sy + 0.02 * math.sin(a) - 0.05 + 0.02 * k],
                    c=PURPLE, lw=1.6, zorder=6)
    # 雷（暗）
    bx, by = cx + 0.20, cy - 0.02
    bolt = [(0.03, 0.08), (-0.015, 0.0), (0.015, 0.0), (-0.03, -0.08)]
    ax.plot([bx + a for a, _ in bolt], [by + b for _, b in bolt], c=AMBER, lw=3, alpha=.35, zorder=6)
    T(ax, cx, cy - 0.17, tx("sleep1"), 17, WHITE)
    T(ax, cx, cy - 0.24, tx("sleep2"), 13, GREY, w="normal")


def c01_pleiades(ax):
    x, y = on(R1, ang(10, 17))
    cluster(ax, x - 0.13, y - 0.12, 0.035, AMBER, 30)
    T(ax, -0.97, y - 0.22, tx("ple1"), 15, AMBER, ha="left")
    T(ax, -0.97, y - 0.28, tx("ple2"), 13, WHITE, ha="left", w="normal")
    x2, y2 = on(R1, ang(3, 1))
    T(ax, x2 + 0.06, y2 - 0.10, tx("ple3"), 13, WHITE, ha="left", w="normal")


# ══════════════════ C-A16-02 黑神的晶石 ══════════════════
HC, HR = (-0.33, 0.0), 0.52
LAD_X, LAD_Y = 0.62, [-0.62, -0.30, -0.02, 0.26, 0.56]


def c02_hooghan(ax):
    head(ax, tx("c02_title"), tx("c02_sub"))
    pts = [(HC[0] + HR * math.cos(math.radians(22.5 + 45 * k)), HC[1] + HR * math.sin(math.radians(22.5 + 45 * k)))
           for k in range(8)]
    # 八角形，東（右）邊留門
    for k in range(8):
        a, b = pts[k], pts[(k + 1) % 8]
        if k == 7:          # 右側那一邊（−22.5°→22.5°）＝門：只畫兩小段
            for s0, s1 in ((0.0, 0.3), (0.7, 1.0)):
                ax.plot([b[0] + (a[0] - b[0]) * s0, b[0] + (a[0] - b[0]) * s1],
                        [b[1] + (a[1] - b[1]) * s0, b[1] + (a[1] - b[1]) * s1], c="#D9B48A", lw=5, zorder=4)
            continue
        ax.plot([a[0], b[0]], [a[1], b[1]], c="#D9B48A", lw=5, zorder=4)
    ax.add_patch(CB.Polygon(pts, closed=True, fc=EARTH, ec="none", alpha=.55, zorder=2))
    T(ax, HC[0] + HR + 0.05, HC[1], tx("door"), 13, "#D9B48A", ha="left", w="normal")
    T(ax, HC[0], HC[1] - HR - 0.07, tx("hooghan"), 16, "#D9B48A")
    # 兩個抽象色塊（頭朝東）
    for dy, fc, ec, lab in ((0.17, BLUE, BLUE, tx("earth")), (-0.17, "#0A0A12", WHITE, tx("sky"))):
        ax.add_patch(CB.FancyBboxPatch((HC[0] - 0.28, HC[1] + dy - 0.07), 0.50, 0.14,
                                       boxstyle="round,pad=0.0,rounding_size=0.07", fc=fc, ec=ec,
                                       lw=1.4, alpha=.85, zorder=5))
        T(ax, HC[0] - 0.03, HC[1] + dy, lab, 15, WHITE, z=12)
    T(ax, HC[0], HC[1] - HR - 0.14, tx("abstract"), 11, GREY, w="normal")
    # 跳的路徑（不畫人形）：一條淡淡的虛線
    ax.plot([LAD_X, LAD_X], [LAD_Y[0], LAD_Y[-1]], c=WHITE, lw=1.2, alpha=.25, ls=(0, (3, 5)), zorder=3)


def _step(i):
    def f(ax):
        y = LAD_Y[i]
        ax.plot([LAD_X - 0.03, LAD_X + 0.03], [y, y], c=WHITE, lw=1.5, alpha=.5, zorder=4)
        T(ax, LAD_X + 0.10, y, tx("steps")[i], 16, WHITE, ha="left")
        if i > 0:
            y0 = LAD_Y[i - 1]
            xs = [LAD_X - 0.11 - 0.07 * math.sin(math.pi * k / 20) for k in range(21)]
            ys = [y0 + (y - y0) * k / 20 for k in range(21)]
            ax.plot(xs, ys, c=AMBER, lw=1.8, alpha=.55, zorder=4)
        cluster(ax, LAD_X - 0.11, y, 0.032, AMBER if i == 4 else "#FFE3A0", 26 if i < 4 else 40,
                alpha=1.0 if i == 4 else 0.75)
        if i == 4:
            T(ax, LAD_X - 0.02, y + 0.13, tx("stars"), 17, AMBER)
    return f


# ══════════════════ C-A16-03 郊狼吹散星星 ══════════════════
def coyote(ax, x, y, s, c="#B9A68C"):
    """側面剪影（四腳著地、不擬人）：身體、頭、尖耳、尖吻、蓬尾"""
    body = [(-0.30, 0.02), (-0.20, 0.10), (0.05, 0.12), (0.20, 0.10), (0.27, 0.16), (0.30, 0.27),
            (0.33, 0.21), (0.37, 0.27), (0.38, 0.17), (0.50, 0.12), (0.52, 0.09), (0.40, 0.06),
            (0.32, 0.02), (0.24, -0.04), (0.23, -0.26), (0.19, -0.26), (0.17, -0.05), (0.08, -0.04),
            (0.02, -0.26), (-0.02, -0.26), (-0.04, -0.03), (-0.17, -0.03), (-0.20, -0.26), (-0.24, -0.26),
            (-0.25, -0.02), (-0.30, 0.02)]
    tail = [(-0.30, 0.04), (-0.42, 0.02), (-0.55, -0.10), (-0.52, -0.14), (-0.40, -0.08), (-0.29, -0.02)]
    for poly in (body, tail):
        ax.add_patch(CB.Polygon([(x + a * s, y + b * s) for a, b in poly], closed=True, fc=c, ec="none",
                                zorder=6))
    return x + 0.52 * s, y + 0.09 * s           # 吻尖


def c03_coyote(ax):
    head(ax, tx("c03_title"), tx("c03_sub"))
    mx, my = coyote(ax, -0.42, -0.42, 0.9)
    bx, by = mx + 0.09, my + 0.02                 # 鹿皮袋（咬在嘴上）
    ax.add_patch(CB.Ellipse((bx, by), 0.13, 0.17, angle=-30, fc="#C8A070", ec="#8C6A45", lw=2, zorder=7))
    for k in range(6):
        ax.scatter([bx - 0.035 + 0.02 * (k % 3)], [by - 0.04 + 0.03 * (k // 3)], s=10, c="#8C6A45", zorder=8)
    T(ax, bx + 0.02, by - 0.15, tx("bag"), 14, "#D9B48A")


def c03_blow(ax):
    rng = random.Random(16)
    ox, oy = 0.10, -0.32
    for _ in range(420):
        a = math.radians(rng.uniform(20, 80))
        r = 0.08 + 1.05 * rng.random() ** 0.7
        x, y = ox + r * math.cos(a) + rng.gauss(0, 0.03), oy + r * math.sin(a) + rng.gauss(0, 0.03)
        if x > 0.97 or y > 0.70:
            continue
        sz = 4 + 40 * rng.random() ** 4
        ax.scatter([x], [y], s=sz, c=rng.choice([WHITE, WHITE, MW, "#FFE3A0"]), lw=0, zorder=5,
                   alpha=0.6 + 0.4 * rng.random())
    T(ax, -0.22, -0.12, tx("blow"), 24, WHITE, ha="left", alpha=.8)


# ══════════════════ C-A16-04 規矩與混亂 ══════════════════
ORDER = {   # 示意：北火＋旋轉的男人＋旋轉的女人＋瘦長的人（幾何依實際星形縮放，非等比星圖）
    "fire": [(-0.02, 0.32)],
    "male": [(-0.55, 0.05), (-0.42, 0.10), (-0.35, 0.02), (-0.47, -0.06), (-0.55, 0.05)],
    "male2": [(-0.35, 0.02), (-0.25, 0.08), (-0.16, 0.11), (-0.08, 0.20)],
    "fem": [(0.25, 0.55), (0.35, 0.47), (0.43, 0.56), (0.52, 0.47), (0.62, 0.55)],
    "slim": [(0.30, -0.10), (0.48, -0.12), (0.37, -0.30), (0.40, -0.32), (0.43, -0.34), (0.32, -0.52),
             (0.52, -0.50)],
}


def c04_chaos(ax):
    head(ax, tx("c04_title"))
    rng = random.Random(4)
    for _ in range(700):
        x, y = rng.uniform(-0.95, 0.95), rng.uniform(-0.80, 0.72)
        ax.scatter([x], [y], s=3 + 30 * rng.random() ** 5, c=WHITE, lw=0, alpha=.35 + .5 * rng.random(), zorder=3)
    T(ax, -0.62, -0.72, tx("chaos"), 16, GREY, w="normal")
    T(ax, 0.0, -0.86, tx("c04_foot"), 13, GREY, w="normal")


def c04_order(ax):
    ax.add_patch(CB.Circle(ORDER["fire"][0], 0.05, fc=AMBER, alpha=.25, ec="none", zorder=6))
    star(ax, *ORDER["fire"][0], 160, AMBER)
    for key, col in (("male", AMBER), ("male2", AMBER), ("fem", GREEN)):
        xs, ys = zip(*ORDER[key])
        ax.plot(xs, ys, c=col, lw=2.6, zorder=6)
        for p in ORDER[key]:
            star(ax, *p, 70, WHITE, glow=False)
    s = ORDER["slim"]
    for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6)):
        ax.plot([s[a][0], s[b][0]], [s[a][1], s[b][1]], c=BLUE, lw=2.6, zorder=6)
    for p in s:
        star(ax, *p, 70, WHITE, glow=False)
    T(ax, 0.62, -0.72, tx("order"), 16, AMBER)


# ══════════════════ C-A16-06 播種 ══════════════════
HY6 = -0.20


def c06_horizon(ax):
    head(ax, tx("c06_title"))
    ax.fill_between([-0.95, 0.95], [HY6, HY6], [HY6 - 0.06, HY6 - 0.06], color=EARTH, alpha=.9, zorder=3)
    ax.plot([-0.95, 0.95], [HY6, HY6], c="#D9B48A", lw=2.4, zorder=4)
    T(ax, 0.0, HY6 - 0.11, tx("west"), 22, "#D9B48A")
    # 獵戶（示意，斜躺沉向地平線）
    o = [(-0.10, 0.20), (0.10, 0.30), (0.02, 0.08), (0.05, 0.06), (0.08, 0.04), (-0.05, -0.10), (0.18, -0.06)]
    for a, b in ((0, 2), (1, 4), (2, 3), (3, 4), (2, 5), (4, 6)):
        ax.plot([o[a][0], o[b][0]], [o[a][1], o[b][1]], c=BLUE, lw=2.4, zorder=5)
    for p in o:
        star(ax, *p, 70, WHITE)
    ax.annotate("", xy=(0.30, HY6 + 0.05), xytext=(0.48, 0.30),
                arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.6, alpha=.5))
    T(ax, 0.0, 0.48, tx("slim"), 17, BLUE)


def corn(ax, x, y):
    ax.add_patch(CB.Ellipse((x, y + 0.03), 0.06, 0.16, fc=AMBER, ec="none", zorder=6))
    for dx in (-0.045, 0.045):
        ax.add_patch(CB.Ellipse((x + dx, y), 0.035, 0.17, angle=-25 * (1 if dx > 0 else -1), fc=GREEN,
                                ec="none", zorder=7))


def bean(ax, x, y):
    xs = [x - 0.08 + 0.16 * k / 30 for k in range(31)]
    ax.fill_between(xs, [y + 0.02 * math.sin(math.pi * k / 30) + 0.025 for k in range(31)],
                    [y - 0.03 * math.sin(math.pi * k / 30) - 0.02 for k in range(31)], color=GREEN, zorder=6)
    for k in range(3):
        ax.add_patch(CB.Circle((x - 0.05 + 0.05 * k, y), 0.017, fc="#B6E8BF", ec="none", zorder=7))


def squash(ax, x, y):
    ax.add_patch(CB.Ellipse((x, y), 0.15, 0.11, fc="#F0A040", ec="#C07020", lw=1.5, zorder=6))
    for dx in (-0.035, 0.0, 0.035):
        ax.plot([x + dx, x + dx * 1.2], [y + 0.05, y - 0.05], c="#C07020", lw=1, zorder=7)
    ax.plot([x, x + 0.01], [y + 0.055, y + 0.09], c=GREEN, lw=3, zorder=7)


def tobacco(ax, x, y):
    ax.add_patch(CB.Ellipse((x, y), 0.08, 0.18, angle=15, fc="#8FBF5A", ec="none", zorder=6))
    ax.plot([x - 0.02, x + 0.02], [y - 0.08, y + 0.08], c="#5F8A35", lw=1.4, zorder=7)


def c06_crops(ax):
    xs = [-0.60, -0.20, 0.20, 0.60]
    yc = -0.52
    for x, fn, lab in zip(xs, (corn, bean, squash, tobacco), tx("crops")):
        fn(ax, x, yc)
        T(ax, x, yc - 0.15, lab, 15, WHITE)
    T(ax, 0.0, -0.80, tx("sow"), 20, GREEN)
    T(ax, 0.0, -0.92, tx("c06_foot"), 10.5, GREY, w="normal")


# ══════════════════ C-A16-07 郊狼的星 ══════════════════
HY7, KD = -0.42, 0.055        # 地平線 y；每度 0.055（高度照比例）


def c07_horizon(ax):
    head(ax, tx("c07_title"))
    ax.fill_between([-0.95, 0.95], [HY7, HY7], [HY7 - 0.07, HY7 - 0.07], color=EARTH, alpha=.9, zorder=3)
    ax.plot([-0.95, 0.95], [HY7, HY7], c="#D9B48A", lw=2.4, zorder=4)
    T(ax, 0.0, HY7 - 0.13, tx("south"), 22, "#D9B48A")
    for d in (5, 10, 15):
        y = HY7 + d * KD
        ax.plot([-0.95, 0.95], [y, y], c=WHITE, lw=0.8, alpha=.15, ls=(0, (3, 6)), zorder=2)
        T(ax, -0.92, y + 0.025, f"{d}°", 11, GREY, ha="left", w="normal")
    T(ax, 0.0, -0.88, tx("c07_foot"), 11, GREY, w="normal")


def c07_place(x, alt, name, name2, alt_txt):
    def f(ax):
        y = HY7 + alt * KD
        ax.plot([x, x], [HY7, y], c=RED, lw=1.4, alpha=.6, zorder=4)
        star(ax, x, y, 150, "#FFF4D6")
        T(ax, x, y + 0.10, alt_txt, 20, RED)
        T(ax, x, HY7 - 0.23, name, 17, WHITE)
        if name2:
            T(ax, x, HY7 - 0.30, name2, 12, GREY, w="normal")
    return f


# ══════════════════ C-A16-05 今晚十一點（9:16 圖卡） ══════════════════
def altaz(names, when="2027/1/8 23:00"):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.pressure, o.temp = 1010, 15
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    out = {}
    for n in names:
        s = ephem.star(n); s.compute(o)
        out[n] = (math.degrees(s.alt), math.degrees(s.az))
    return out


def sky_panel(ax, y0, y1, az0, az1, alt1, title, marks, lines, dirs):
    x0, x1 = 0.06, 0.94
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#10162C", ec=WHITE, lw=1.0, alpha=1, zorder=1))
    gy = y0 + 0.035

    def P(alt, az):
        d = (az - az0) % 360
        return x0 + (x1 - x0) * d / ((az1 - az0) % 360), gy + (y1 - 0.05 - gy) * alt / alt1

    ax.fill_between([x0 + 0.003, x1 - 0.003], [y0 + 0.003] * 2, [gy] * 2, color=EARTH, zorder=2)
    ax.plot([x0, x1], [gy, gy], c="#D9B48A", lw=1.6, zorder=3)
    for lab, az in dirs:
        x, _ = P(0, az)
        T(ax, x, gy - 0.017, lab, 11, "#D9B48A")
    T(ax, 0.5, y1 + 0.022, title, 15, WHITE)
    for seg, col in lines:
        xs, ys = zip(*[P(*marks[n][:2]) for n in seg])
        ax.plot(xs, ys, c=col, lw=1.8, zorder=4)
    for n, (alt, az, lab, col, dx, dy, ha) in marks.items():
        x, y = P(alt, az)
        star(ax, x, y, 30 if not lab else 55, WHITE, glow=bool(lab))
        if lab:
            T(ax, x + dx, y + dy, lab, 11.5, col, ha=ha)
            T(ax, x + dx, y + dy - 0.017, f"{alt:.0f}°", 10, GREY, ha=ha, w="normal")


def c05_card(ax):
    T(ax, 0.5, 0.955, tx("c05_title"), 30, WHITE)
    T(ax, 0.5, 0.920, tx("c05_date"), 14, GREY, w="normal")
    A = altaz(["Polaris", "Dubhe", "Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid",
               "Schedar", "Caph", "Sirius", "Canopus", "Betelgeuse", "Rigel"])
    # Cas 另三顆（ephem 內建表沒有）：用星表 RA/Dec 自算
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.pressure, o.temp = 1010, 15
    o.date = ephem.Date(ephem.Date("2027/1/8 23:00") - 8 * ephem.hour)
    S = dict(G.load_stars(BASE))
    for nm, h in (("Navi", 4427), ("Ruchbah", 6686), ("Segin", 8886)):
        b = ephem.FixedBody(); b._ra, b._dec, b._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        b.compute(o); A[nm] = (math.degrees(b.alt), math.degrees(b.az))
    mk = lambda n, lab="", col=WHITE, dx=0.0, dy=0.03, ha="center": (A[n][0], A[n][1], lab, col, dx, dy, ha)
    north = {n: mk(n) for n in ("Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid", "Caph", "Navi",
                                 "Ruchbah", "Segin")}
    north["Polaris"] = mk("Polaris", tx("Polaris"), AMBER, 0.0, 0.035)
    north["Dubhe"] = mk("Dubhe", tx("Dipper"), AMBER, 0.0, 0.045)
    north["Schedar"] = mk("Schedar", tx("Cas"), GREEN, 0.0, -0.055)
    sky_panel(ax, 0.52, 0.86, 295, 65, 45, tx("north_panel"), north,
              [(["Dubhe", "Merak", "Phecda", "Megrez", "Dubhe"], AMBER),
               (["Megrez", "Alioth", "Mizar", "Alkaid"], AMBER),
               (["Segin", "Ruchbah", "Navi", "Schedar", "Caph"], GREEN)],
              [(tx("NW"), 315), (tx("N"), 0), (tx("NE"), 45)])
    south = {"Sirius": mk("Sirius", tx("Sirius"), WHITE, 0.05, 0.02, "left"),
             "Canopus": mk("Canopus", tx("Canopus"), RED, 0.0, 0.04),
             "Betelgeuse": mk("Betelgeuse", tx("Orion"), BLUE, 0.0, 0.035),
             "Rigel": mk("Rigel")}
    sky_panel(ax, 0.13, 0.465, 128, 232, 78, tx("south_panel"), south, [],
              [(tx("SE"), 135), (tx("S"), 180), (tx("SW"), 225)])
    for i, (k, col) in enumerate((("tip1", WHITE), ("tip2", WHITE), ("tip3", WHITE), ("tip4", GREY))):
        T(ax, 0.5, 0.098 - i * 0.019, tx(k), 11 if col == WHITE else 9.5, col, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 12, WHITE, w="normal")


# ══════════════════ hooghan 輪廓（1080×1920 滿版透明） ══════════════════
def hooghan_overlay(r=500.0, c=(540.0, 960.0)):
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(5.4, 9.6), dpi=200)
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1080); ax.set_ylim(1920, 0); ax.axis("off")
    f.patch.set_alpha(0); ax.patch.set_alpha(0)
    pts = [(c[0] + r * math.cos(math.radians(22.5 + 45 * k)), c[1] - r * math.sin(math.radians(22.5 + 45 * k)))
           for k in range(8)]
    for k in range(8):
        a, b = pts[k], pts[(k + 1) % 8]
        if k == 7:                        # 東（畫面右）＝門
            for s0, s1 in ((0.0, 0.3), (0.7, 1.0)):
                ax.plot([b[0] + (a[0] - b[0]) * s0, b[0] + (a[0] - b[0]) * s1],
                        [b[1] + (a[1] - b[1]) * s0, b[1] + (a[1] - b[1]) * s1], c="#D9B48A", lw=4, alpha=.55)
            continue
        ax.plot([a[0], b[0]], [a[1], b[1]], c="#D9B48A", lw=4, alpha=.55)
    for rr, al in ((46, .10), (30, .18), (18, .30)):        # 爐火的光暈（中心＝北極星）
        ax.add_patch(CB.Circle(c, rr, fc=AMBER, ec="none", alpha=al))
    d = OUT; os.makedirs(d, exist_ok=True)
    f.savefig(os.path.join(d, "C-A16-hooghan_透明.png"), transparent=True); plt.close(f)
    print("  ✓ C-A16-hooghan_透明.png")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A16 概念圖 ──")
    CB.emit("", [("日曆環", c01_ring), ("今天", c01_today), ("睡", c01_sleep), ("昴宿", c01_pleiades)],
            title="C-A16-01_冬天才說的故事")
    CB.emit("", [("hooghan", c02_hooghan)] + [(n, _step(i)) for i, n in enumerate(["腳踝", "膝", "腰", "肩", "太陽穴"])],
            title="C-A16-02_黑神的晶石")
    CB.emit("", [("郊狼", c03_coyote), ("吹散", c03_blow)], title="C-A16-03_郊狼吹散星星")
    CB.emit("", [("混亂", c04_chaos), ("規矩", c04_order)], title="C-A16-04_規矩與混亂")
    CB.emit("", [("地平線", c06_horizon), ("作物", c06_crops)], title="C-A16-06_播種")
    CB.emit("", [("地平線", c07_horizon),
                 ("WindowRock", c07_place(-0.45, 1.6, tx("wr"), tx("wr2"), tx("wr_alt"))),
                 ("台北", c07_place(0.45, 12.3, tx("tp"), "", tx("tp_alt")))], title="C-A16-07_郊狼的星")
    fig, ax = CB.newcard(dark=True)
    c05_card(ax)
    CB.save(fig, "", "C-A16-05_今晚十一點_圖卡.png", transparent=False)
    if LANG == "zh":
        hooghan_overlay()


if __name__ == "__main__":
    main()
