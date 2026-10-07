# -*- coding: utf-8 -*-
"""A-13 阿拉伯半島：Thurayya 與沙漠的雨季｜概念圖（C 系列骨架）

C-A13-01 星星年曆（月站層、季節層、今天層）：28 站 × 13 天＋1＝365，昴宿 6/7 開年
C-A13-02 守望者（地平層、升起層、落下層、引文層）：12 月黎明冠冕升起＝昴宿落下
C-A13-03 月亮會昴宿（月相層、諺語層、今年層）：qirān 13→3 與 2026–27 實際日期
C-A13-04 沙漠星名小辭典（9:16 圖卡）
C-A13-05 這週末往東看（9:16 圖卡；台北 2026/12/12–13）

天象全部 PyEphem 自算（氣壓 1010 hPa，含折射）；民間星曆日期：昴宿晨升 6/7 起，每站 13 天、
al-Jabhah 14 天（Stellarium arabic_arabian_peninsula description）；雨季 al-Wasm 10/16 起 52 天、
最冷四十天 al-Murabbaʿāniyya 12/7 起（沙烏地／阿聯媒體與 al-Misnad）；qirān 諺語（A. Al-Misnad）。
執行：python3 make_a13_diagrams.py
"""
import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_a13_v4 as A13

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-13_阿拉伯半島/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
S = None
TPE = (25.0330, 121.5654)
RUH = (24.7136, 46.6753)
AR = G.rtl
Y0 = datetime.date(2026, 6, 7)


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, rot=0, va="center"):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, rotation=rot, rotation_mode="anchor")


def observer(lat, lon, elev=0):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = elev; o.pressure = 1010
    return o


def body(ra, dec):
    import ephem
    b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec); b._epoch = ephem.J2000
    return b


# ══════════════════════ C-A13-01 星星年曆 ══════════════════════
CX, CY = 0.0, -0.04
R0, R1 = 0.26, 0.52            # 月站環
RM = 0.565                     # 月份
RA_ = 0.625                    # 季節弧
SHORT = ["昴宿", "小跟班", "圓斑", "低彎", "前臂", "鼻尖", "眼睛", "額頭", "鬃毛", "變天", "彎弧", "高舉者",
         "遮蓋", "蠍螯", "冠冕", "心臟", "蠍尾", "鴕鳥", "空地", "屠夫", "吞嚥", "吉中吉", "帳篷", "前口",
         "後口", "桶繩", "記號", "小肚"]


def frac(d):
    """日期 → 從 6/7 起算的一年比例（0 在正上方，順時針）"""
    dd = d if isinstance(d, datetime.date) else datetime.date(*d)
    n = (dd - Y0).days % 365
    return n / 365.0


def ang(f):
    return math.pi / 2 - 2 * math.pi * f


def pol(r, f):
    a = ang(f)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def arc_pts(r, f0, f1, n=120):
    if f1 < f0:
        f1 += 1.0
    return [pol(r, f0 + (f1 - f0) * i / n) for i in range(n + 1)]


def radial_text(ax, r, f, s, size, col, w="bold"):
    a = math.degrees(ang(f))
    x, y = pol(r, f)
    a = (a + 180) % 360 - 180
    rot = a if -90 <= a <= 90 else a + 180
    ctext(ax, x, y, s, size, col, w=w, rot=((rot + 180) % 360) - 180)


def c01_stations(ax):
    T(ax, 0.0, 0.93, "沙漠的星星年曆", 30, WHITE)
    T(ax, 0.0, 0.855, "天亮前，東方第一次露臉的星：一顆管 13 天，28 顆排一圈", 15, GREY, w="normal")
    ds = A13.DATES
    for i, d in enumerate(ds):
        f0 = frac(d); f1 = frac(ds[(i + 1) % 28])
        hot = i in (0, 14)
        poly = arc_pts(R1, f0, f1, 30) + arc_pts(R0, f0, f1, 30)[::-1]
        ax.add_patch(CB.Polygon(poly, closed=True, fc=(AMBER if hot else PANEL), ec=WHITE, lw=0.8,
                                alpha=(0.35 if hot else 0.6), zorder=3))
        fm = (f0 + ((f1 - f0) % 1.0) / 2) % 1.0
        radial_text(ax, 0.43, fm, SHORT[i], 11, AMBER if hot else WHITE)
        radial_text(ax, 0.295, fm, f"{d.month}/{d.day}", 7.5, GREY, w="normal")
    for m in range(1, 13):
        f = frac(datetime.date(2026 if m >= 6 else 2027, m, 1))
        x0, y0 = pol(R1 + 0.005, f); x1, y1 = pol(R1 + 0.03, f)
        ax.plot([x0, x1], [y0, y1], c=WHITE, lw=1.1, alpha=.6, zorder=4)
        fm = frac(datetime.date(2026 if m >= 6 else 2027, m, 16))
        radial_text(ax, RM, fm, f"{m}月", 9.5, GREY, w="normal")
    ctext(ax, CX, CY + 0.05, "13 × 28 ＋ 1", 19, WHITE)
    ctext(ax, CX, CY - 0.03, "＝ 365 天", 16, WHITE)
    ctext(ax, CX, CY - 0.10, "（額頭那站多 1 天）", 9, GREY, w="normal")
    ctext(ax, 0.0, -0.955, "納季德民間星曆：昴宿晨升 6/7 開年（Stellarium arabic_arabian_peninsula；al-Ajaji）",
          9.5, GREY, w="normal")


def c01_seasons(ax):
    for d0, d1, col in [((2026, 10, 16), (2026, 12, 7), GREEN), ((2026, 12, 7), (2027, 1, 16), BLUE)]:
        pts = arc_pts(RA_, frac(d0), frac(d1))
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=8, alpha=.9, solid_capstyle="butt", zorder=5)
    # 弧的說明：右下（雨季）、左下（最冷四十天）
    x, y = pol(RA_ + 0.02, frac((2026, 11, 11)))
    ctext(ax, 0.86, -0.56, "雨季 al-Wasm", 14, GREEN, ha="right")
    ctext(ax, 0.86, -0.615, "10/16 起 52 天：「烙印」", 10.5, GREEN, w="normal", ha="right")
    ax.plot([x, 0.40], [y, -0.60], c=GREEN, lw=1.0, alpha=.6, zorder=4)
    x, y = pol(RA_ + 0.02, frac((2026, 12, 30)))
    ctext(ax, -0.86, -0.56, "最冷四十天", 14, BLUE, ha="left")
    ctext(ax, -0.86, -0.615, "al-Murabbaʿāniyya：12/7 起（大雪）", 10.5, BLUE, w="normal", ha="left")
    ax.plot([x, -0.40], [y, -0.60], c=BLUE, lw=1.0, alpha=.6, zorder=4)
    # 兩個晨升標記：昴宿（芒種）、Suhail（處暑）
    for d, (lx, ly, ha), t1, t2 in [((2026, 6, 7), (0.0, 0.715, "center"), "6/7 昴宿晨升：夏天開始", "（芒種 6/5）"),
                                    ((2026, 8, 24), (0.93, 0.30, "right"), "8/24 Suhail 晨升：熱退", "（處暑 8/23）")]:
        x0, y0 = pol(R1 + 0.035, frac(d)); x1, y1 = pol(RA_ + 0.03, frac(d))
        ax.plot([x0, x1], [y0, y1], c=AMBER, lw=3.0, zorder=6)
        ax.scatter([x1], [y1], s=55, c=AMBER, zorder=7)
        ctext(ax, lx, ly, t1, 13, AMBER, ha=ha)
        ctext(ax, lx, ly - 0.05, t2, 10.5, WHITE, w="normal", ha=ha)


def c01_today(ax):
    d = (2026, 12, 11)
    x1, y1 = pol(R1 + 0.02, frac(d))
    ax.scatter([x1], [y1], s=150, c=RED, zorder=9, marker="v")
    pts = arc_pts(R1 + 0.004, frac((2026, 12, 7)), frac((2026, 12, 20)), 30) + \
        arc_pts(R0 - 0.004, frac((2026, 12, 7)), frac((2026, 12, 20)), 30)[::-1]
    ax.add_patch(CB.Polygon(pts, closed=True, fc="none", ec=RED, lw=3.0, zorder=8))
    ctext(ax, 0.0, -0.80, "今天 12/11：冠冕 al-Iklīl（第 15 站）", 14, RED)
    ctext(ax, 0.0, -0.86, "昴宿在黎明落下＝最冷四十天開始；12/22 冬至月亮會昴宿", 11, WHITE, w="normal")


# ══════════════════════ C-A13-02 守望者 ══════════════════════
HZ = -0.30


def c02_horizon(ax):
    T(ax, 0.0, 0.93, "黎明的兩端：守望者", 30, WHITE)
    T(ax, 0.0, 0.85, "12 月初，利雅德，天亮前（太陽在地平線下約 10°）", 15, GREY, w="normal")
    ax.plot([-0.95, 0.95], [HZ, HZ], c=WHITE, lw=2.4, alpha=.85, zorder=4)
    ax.add_patch(CB.Rectangle((-0.95, -0.40), 1.9, HZ + 0.40, fc="#141A2E", ec="none", zorder=3))
    ctext(ax, -0.86, HZ - 0.06, "東", 18, WHITE)
    ctext(ax, 0.86, HZ - 0.06, "西", 18, WHITE)
    for k in range(6):
        r = 0.06 + 0.06 * k
        pts = [(-0.95 + r * math.cos(t * math.pi / 60), HZ + 0.6 * r * math.sin(t * math.pi / 60)) for t in range(61)]
        pts = [(max(-0.95, x), y) for x, y in pts]
        ax.add_patch(CB.Polygon(pts, closed=True, fc=AMBER, ec="none", alpha=0.06, zorder=2))
    ctext(ax, -0.82, HZ + 0.035, "太陽快出來了", 10.5, AMBER, w="normal", ha="left")
    pts = [(-0.62 + 1.24 * i / 80, HZ + 0.06 + 0.78 * math.sin(math.pi * i / 80)) for i in range(81)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=WHITE, lw=1.4, alpha=.35, ls=(0, (4, 5)), zorder=3)
    ctext(ax, 0.0, HZ + 0.90, "相隔半個天空：第 15 站 ↔ 第 1 站", 12, GREY, w="normal")


def c02_rise(ax):
    pts = [(-0.66, HZ + 0.12), (-0.62, HZ + 0.19), (-0.575, HZ + 0.15)]
    for p, s in zip(pts, (160, 200, 150)):
        ax.scatter([p[0]], [p[1]], s=s, c=WHITE, zorder=7)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=AMBER, lw=2.0, alpha=.9, zorder=6)
    CB.arrow(ax, (-0.47, HZ + 0.30), (-0.47, HZ + 0.10), c=AMBER, lw=2.6, alpha=.95, style="->")
    ctext(ax, -0.43, HZ + 0.20, "升起", 14, AMBER, ha="left")
    ctext(ax, -0.62, HZ + 0.50, AR("الإكليل"), 24, AMBER, w="normal")
    ctext(ax, -0.62, HZ + 0.41, "al-Iklīl 冠冕（天蠍的頭）", 12.5, WHITE)


def c02_set(ax):
    import random
    rnd = random.Random(7)
    cx, cy = 0.62, HZ + 0.13
    for _ in range(7):
        ax.scatter([cx + rnd.uniform(-0.035, 0.035)], [cy + rnd.uniform(-0.02, 0.02)],
                   s=rnd.uniform(40, 110), c=WHITE, zorder=7)
    ax.add_patch(CB.Circle((cx, cy), 0.07, fc=MW, ec="none", alpha=0.10, zorder=6))
    CB.arrow(ax, (0.47, HZ + 0.10), (0.47, HZ + 0.30), c=BLUE, lw=2.6, alpha=.95, style="->")
    ctext(ax, 0.43, HZ + 0.20, "落下", 14, BLUE, ha="right")
    ctext(ax, 0.62, HZ + 0.50, AR("الثريا"), 24, BLUE, w="normal")
    ctext(ax, 0.62, HZ + 0.41, "al-Thurayyā 昴宿", 12.5, WHITE)


def c02_quote(ax):
    box(ax, -0.88, -0.93, 1.76, 0.50, ec=GREY, fc=PANEL, lw=1.2, alpha=0.92, z=8)
    ctext(ax, -0.50, -0.49, AR("رقيب"), 18, AMBER, w="normal", z=10)
    ctext(ax, -0.40, -0.49, "raqīb＝守望者：一個升起，另一個就落下", 14, WHITE, ha="left", z=10)
    ctext(ax, 0.0, -0.57, "古人相信：星星在黎明落下的那幾天會帶來雨（nawʾ，星雨）", 12, WHITE, w="normal", z=10)
    ctext(ax, 0.0, -0.64, "「所有的星雨裡，昴宿的最多」——這段日子就是沙漠最冷的四十天", 12, AMBER, w="normal", z=10)
    ctext(ax, 0.0, -0.72, "六月反過來：昴宿在黎明升起、冠冕落下＝夏天開始", 12, WHITE, w="normal", z=10)
    ctext(ax, 0.0, -0.80, "上週的參商不相見：中國寫成離別，阿拉伯拿來算雨", 12, GREEN, w="normal", z=10)
    ctext(ax, 0.0, -0.885, "利雅德 2026：冠冕 12/8 前後黎明初見、昴宿 12/3–6 黎明落下（PyEphem 自算）", 9.5, GREY,
          w="normal", z=10)


# ══════════════════════ C-A13-03 月亮會昴宿 ══════════════════════
QIR = [("11月", 15, "滿月會昴宿", "", (2026, 11, 24), 15.2),
       ("12月", 13, "冬天開始", "", (2026, 12, 22), 12.9),
       ("1月", 11, "冷，露臉了", "قران حادي، برد بادي", (2027, 1, 18), 10.5),
       ("2月", 9, "冷得像\n被蠍子螫", "قران تاسع، برد لاسع", (2027, 2, 15), 8.0),
       ("3月", 7, "有的吃飽、\n有的還餓", "قران سابع، مجيع وشابع", (2027, 3, 14), 5.5),
       ("4月", 5, "春草\n淹沒地面", "قران خامس، ربيع طامس", (2027, 4, 10), 3.2),
       ("5月", 3, "春天要走了", "قران ثالث، ربيع ذالف", (2027, 5, 7), 1.0)]
XS = [-0.80 + 1.60 * i / 6 for i in range(7)]
YM = 0.42


def moon_icon(ax, x, y, r, age):
    """北半球看：盈月右亮；age＝月齡（天）"""
    ph = (age % 29.53) / 29.53
    ax.add_patch(CB.Circle((x, y), r, fc="#2A3150", ec=WHITE, lw=1.0, zorder=5))
    k = math.cos(2 * math.pi * ph)          # 明暗界線（橢圓半寬 = k·r）
    pts = []
    for i in range(61):
        t = -math.pi / 2 + math.pi * i / 60
        pts.append((x + r * math.cos(t), y + r * math.sin(t)))       # 右半圓
    for i in range(61):
        t = math.pi / 2 - math.pi * i / 60
        pts.append((x + k * r * math.cos(t), y + r * math.sin(t)))   # 明暗界線
    if ph > 0.5:                             # 虧月：左亮
        pts = [(2 * x - px, py) for px, py in pts]
    ax.add_patch(CB.Polygon(pts, closed=True, fc="#FFF6DA", ec="none", zorder=6))


def c03_phase(ax):
    T(ax, 0.0, 0.93, "月亮會昴宿：第幾晚相會，就是季節", 28, WHITE)
    T(ax, 0.0, 0.85, "月亮每個月經過昴宿一次，但每個月提早約兩晚", 15, GREY, w="normal")
    for (m, n, zh, ar_s, d, age), x in zip(QIR, XS):
        ctext(ax, x, YM + 0.17, m, 15, WHITE)
        moon_icon(ax, x, YM, 0.075, n - 0.5)
        ax.scatter([x + 0.055], [YM + 0.055], s=22, c=AMBER, zorder=8)      # 昴宿
        ctext(ax, x, YM - 0.15, f"{n}", 30, AMBER if n == 13 else WHITE)
        ctext(ax, x, YM - 0.24, "晚", 11, GREY, w="normal")
    ctext(ax, 0.0, -0.86, "月亮回到昴宿要 27.3 天，月相輪一回要 29.5 天——每個月差 2.2 天", 11.5, GREY, w="normal")


def c03_saying(ax):
    for (m, n, zh, ar_s, d, age), x in zip(QIR, XS):
        col = AMBER if n == 13 else WHITE
        if zh:
            words = zh
            ax.text(x, YM - 0.38, words, fontproperties=CB.FP, fontsize=12, color=col, ha="center",
                    va="center", weight="bold", zorder=9, linespacing=1.3)
        if ar_s:
            ctext(ax, x, YM - 0.50, AR(ar_s), 10, GREY, w="normal")
    ctext(ax, 0.0, -0.20, "貝都因諺語（押韻）：第 11 晚「冷，露臉了」、第 9 晚「冷得像被蠍子螫」……", 12, WHITE,
          w="normal")


def c03_year(ax):
    box(ax, -0.88, -0.72, 1.76, 0.36, ec=GREY, fc=PANEL, lw=1.2, alpha=0.92, z=8)
    ctext(ax, 0.0, -0.42, "2026–27 實際相會（台北時間，月齡）", 13, AMBER, z=10)
    row1 = "11/24 15.2　12/22 12.9　1/18 10.5　2/15 8.0"
    row2 = "3/14 5.5　4/10 3.2　5/7 1.0　→ 六月昴宿被太陽遮住"
    ctext(ax, 0.0, -0.51, row1, 12.5, WHITE, w="normal", z=10)
    ctext(ax, 0.0, -0.59, row2, 12.5, WHITE, w="normal", z=10)
    ctext(ax, 0.0, -0.67, "12/22 清晨的「第十三晚」，剛好冬至（PyEphem 自算）", 11.5, GREEN, w="normal", z=10)


# ══════════════════════ C-A13-04 沙漠星名小辭典（9:16） ══════════════════════
GLOSS = [("金星的四個名字", None, None, AMBER),
         ("نجمة الصبح", "Najmat al-Ṣubḥ", "晨星：清晨的金星", WHITE),
         ("نجمة العشا", "Najmat al-ʿShā", "昏星：黃昏的金星", WHITE),
         ("الجغمة", "al-Jughmah", "一口：孩子討奶，大人說等「一口」落下", WHITE),
         ("نجمة الهودان", "Najmat al-Hawdān", "al-Hawdān 之星：每晚說明早走、每早都留下的部落", WHITE),
         ("認星的生活", None, None, AMBER),
         ("الجدي", "al-Jady", "小山羊：北極星", WHITE),
         ("الحويجزين", "al-Ḥuwaijzain", "兩個守衛：小熊座 β、γ（辨方向）", WHITE),
         ("بنات نعش", "Banāt Naʿsh", "Naʿsh 的女兒們：北斗（抬著棺架）", WHITE),
         ("الشداد", "al-Shdād", "駱駝鞍：仙后座（紅海沿岸）", WHITE),
         ("المغزل", "al-Mighzal", "羊毛紡錘：天鵝座（祖勒菲）", WHITE),
         ("مسجد الثريا", "Masjid al-Thurayyā", "昴宿的清真寺：先於昴宿升起的三角", WHITE),
         ("ظهر الجوزا", "Ẓahr al-Jawzā", "她的背：獵戶腰帶（紅海漁民）", WHITE),
         ("التويبع", "al-Twaibiʿ", "小跟班：畢宿五，跟在昴宿後面", WHITE),
         ("المباري", "al-Mbārī", "並行者：五車二，和昴宿並肩", WHITE),
         ("الكانون", "al-Kanūn", "火爐：牛郎星（al-Ḫalāwī 的詩）", WHITE),
         ("محلف", "Miḥlif", "發誓星：水委一，常被當成 Suhail，吵到發誓", WHITE),
         ("سهيل", "Suhail", "老人星：八月底晨升，熱退", WHITE)]


def c04_card(ax):
    ctext(ax, 0.5, 0.955, "沙漠星名小辭典", 30, WHITE)
    ctext(ax, 0.5, 0.918, "阿拉伯半島民間的星名（口傳與詩）", 13, GREY, w="normal")
    y = 0.875
    for ar_s, tr, zh, col in GLOSS:
        if tr is None:
            y -= 0.008
            ctext(ax, 0.06, y, ar_s, 14.5, col, ha="left")
            ax.plot([0.06, 0.94], [y - 0.016, y - 0.016], c=col, lw=1.0, alpha=.5)
            y -= 0.040
            continue
        ctext(ax, 0.30, y, AR(ar_s), 15, AMBER, w="normal", ha="right")
        ctext(ax, 0.33, y + 0.010, tr, 9, GREY, w="normal", ha="left")
        ctext(ax, 0.33, y - 0.011, zh, 11, col, w="normal", ha="left")
        y -= 0.0425
    ctext(ax, 0.5, 0.055, "來源：Stellarium arabic_arabian_peninsula（Khalid al-Ajaji 整理）", 9.5, GREY, w="normal")
    ctext(ax, 0.5, 0.025, "#萬國星空　#師大天文社", 12, WHITE, w="normal")


# ══════════════════════ C-A13-05 這週末往東看（9:16） ══════════════════════
def altaz_fn(when_local, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = observer(lat, lon)
    o.date = ephem.Date(ephem.Date(when_local) - tz * ephem.hour)

    def f(ra, dec):
        b = body(ra, dec); b.compute(o)
        return math.degrees(float(b.alt)), math.degrees(float(b.az))
    return f, o


def sky_panel(ax, y0, y1, az0, az1, alt1, when, title, marks, extra=()):
    """方位等距小天空：x＝方位（左→右＝az0→az1），y＝高度（0→alt1）"""
    f, o = altaz_fn(when)
    xa, xb = 0.06, 0.94

    def q(alt, az):
        x = xa + (az - az0) / (az1 - az0) * (xb - xa)
        y = y0 + alt / alt1 * (y1 - y0)
        return x, y
    box(ax, 0.04, y0 - 0.055, 0.92, (y1 - y0) + 0.10, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ctext(ax, 0.5, y1 + 0.025, title, 15, WHITE, z=12)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=1.6, alpha=.8, zorder=5)
    for az, lab in ((45, "東北"), (67.5, "東北東"), (90, "東"), (112.5, "東南東"), (135, "東南"), (157.5, "南南東")):
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
        alt, az = f(ra, dec)
        if not (0 < alt < alt1 and az0 < az < az1):
            continue
        x, y = q(alt, az)
        pos[h] = (x, y)
        ax.scatter([x], [y], s=max(1.0, (5.6 - v) ** 2.2 * 2.6), c=WHITE, zorder=7, lw=0)
    for segs, col in extra:
        for seg in segs:
            for a, b in zip(seg, seg[1:]):
                if a in pos and b in pos:
                    ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=col, lw=1.0, alpha=.5, zorder=6)
    for spec in marks:
        kind, key, lab, col, dx, dy = spec
        if kind == "hip":
            if key not in pos:
                continue
            x, y = pos[key]
        elif kind == "radec":
            alt, az = f(*key)
            x, y = q(alt, az)
        else:                                   # 行星
            import ephem
            b = getattr(ephem, key)(); b.compute(o)
            alt, az = math.degrees(float(b.alt)), math.degrees(float(b.az))
            x, y = q(alt, az)
            ax.scatter([x], [y], s=260, c=WHITE, zorder=8, lw=0)
            ax.add_patch(CB.Circle((x, y), 0.022, fc=WHITE, ec="none", alpha=0.18, zorder=7))
        if kind == "radec":
            ax.add_patch(CB.Circle((x, y), 0.025, fc="none", ec=col, lw=2.0, zorder=8))
        ctext(ax, x + dx, y + dy, lab, 11.5, col, ha="left" if dx > 0 else ("right" if dx < 0 else "center"), z=12)
    return f


def c05_card(ax):
    ctext(ax, 0.5, 0.962, "這週末往東看", 30, WHITE)
    ctext(ax, 0.5, 0.928, "台北　2026/12/12（六）、12/13（日）", 13, GREY, w="normal")
    sky_panel(ax, 0.60, 0.84, 45.0, 135.0, 55.0, "2026/12/12 18:30", "黃昏 18:30　往東：昴宿入夜就升起",
              [("radec", A13.M45, "昴宿 al-Thurayyā", AMBER, 0.035, 0.012),
               ("hip", A13.ALDEBARAN, "畢宿五 小跟班", WHITE, 0.03, -0.012),
               ("hip", A13.BETELGEUSE, "參宿四", WHITE, 0.02, 0.016)],
              extra=[(A13.AP["Jwza"], BLUE), (A13.AP["MThu"], GREEN)])
    sky_panel(ax, 0.235, 0.47, 95.0, 155.0, 40.0, "2026/12/12 05:45", "清晨 5:45　往東南：冠冕（天蠍的頭）升起",
              [("planet", "Venus", "金星 al-Hawdān 之星", WHITE, 0.035, 0.0),
               ("hip", A13.DSCHUBBA, "冠冕 al-Iklīl", AMBER, 0.03, 0.02)],
              extra=[(A13.AP["Ikll"], AMBER), (A13.AP["Akrb"], RED)])
    lines = [("12/21（一）晚上：快滿的月亮就在昴宿旁，不到一個拳頭", AMBER),
             ("12/22 清晨相會＝「第十三晚」，同一天冬至", AMBER),
             ("Suhail 老人星：半夜 0:53 正南方，高 12°（高雄 15°）", WHITE),
             ("週末黃昏的細月 8 點多就落下，不擋星", WHITE),
             ("方位、高度、時刻：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.155 - i * 0.027, s, 11 if col != GREY else 9.5, col, w="normal")
    ctext(ax, 0.5, 0.022, "#萬國星空　#師大天文社", 12, WHITE, w="normal")


def main():
    global S
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A13 概念圖 ──")
    CB.emit("", [("月站", c01_stations), ("季節", c01_seasons), ("今天", c01_today)], title="C-A13-01_星星年曆")
    CB.emit("", [("地平", c02_horizon), ("升起", c02_rise), ("落下", c02_set), ("引文", c02_quote)],
            title="C-A13-02_守望者")
    CB.emit("", [("月相", c03_phase), ("諺語", c03_saying), ("今年", c03_year)], title="C-A13-03_月亮會昴宿")
    for name, fn in [("C-A13-04_沙漠星名小辭典", c04_card), ("C-A13-05_這週末往東看", c05_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
