# -*- coding: utf-8 -*-
"""C-02 地有四游｜概念圖 v2（方形透明分層：Canva 定格頁一頁疊一層）

輸出：05_素材/C-02_地有四游/{地有四游, 日影推演, 舟行不覺, 兩種視角, 時間軸, 姚信人形比天, _圖卡}/
規格：2052px 方形透明 PNG 分層＋黑底預覽；9:16 圖卡 1215×2160。
      放進 Canva 是 1080 寬 → 圖上 1pt ≈ 1.39px，所以正文 ≥ 22pt、題辭 ≥ 26pt；標籤離邊 x ≤ ±0.93。
會動的圖層（在 Canva 用位移做 Match & Move，不另出逐格圖）：
  地有四游_地塊俯視層／地塊側視層：畫在「春秋分」正中；冬至位移 (−135, −135)／(0, −108) px，夏至反向。
  舟行不覺_船層／閉牖層／人層：三層同位移，整艘船往右走。
來源（原文照引，見逐字稿 v2 首留言）：
  《尚書・考靈曜》：地有四游，冬至地上，北而西三萬里；夏至地下，南而東復三萬里；春秋二分其中矣。
      地恆動不止，而人不知，譬如人在大舟中閉牖而坐，舟行而人不覺也。
  《晉書・天文志》載姚信：人為靈蟲，形最似天。今人頤前侈臨胸，而項不能覆背。近取諸身，
      故知天之體南低入地，北則偏高。又冬至極低…日去人遠…故冰寒也。夏至極起…日去人近…故蒸熱也。
  伽利略 1632《關於兩大世界體系的對話》第二日：大船船艙的思想實驗。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Arc
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, BG, T, arrow, emit, save, newfig, newcard, water
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
C.set_base(os.path.join(BASE, "05_素材/C-02_地有四游"))
PX = 540.0                       # 1 個畫布單位 = Canva 540 px（方形圖層 1080 寬）


def footer(ax, s="示意圖・非等比例", y=-0.94):
    T(ax, 0, y, s, 20, WHITE, alpha=.55)


def catmull(pts, n=16):
    """Catmull-Rom 平滑曲線（人像側影用）"""
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = map(np.array, (p[i-1], p[i], p[i+1], p[i+2]))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t
                              + (-p0 + 3*p1 - 3*p2 + p3)*t**3))
    out.append(np.array(pts[-1]))
    return np.array(out)


# ══════════════════════════════════════════════════════════════
# 1. 地有四游：左＝俯視（東西南北），右＝側視（上下）
#    冬至地上、北而西三萬里；夏至地下、南而東復三萬里；春秋二分其中
# ══════════════════════════════════════════════════════════════
TVX, TVY = -0.34, 0.16           # 俯視：春秋分（正中）
D = 135 / PX                     # 三萬里（示意）= 位移 135 px
BW, BH = 0.12, 0.085             # 地塊半寬、半高
SVX, SH = 0.64, 108 / PX         # 側視：中心 x、上下位移 108 px
SW, SHH = 0.17, 0.04             # 側視地塊半寬、半高
STN = {"冬至": (-1, AMBER), "春秋分": (0, WHITE), "夏至": (+1, BLUE)}   # k：-1 = 北西／上


def tv_pos(k): return TVX + k * D, TVY - k * D
def sv_y(k): return TVY - k * SH


def sy_title(ax):
    T(ax, 0, 0.90, "地有四游", 40, WHITE)
    T(ax, 0, 0.80, "《尚書・考靈曜》（漢代緯書）", 22, WHITE, alpha=.7)
    footer(ax, "依原文方位示意・非等比例")


def sy_frame(ax):
    ax.plot([-0.84, 0.16], [TVY, TVY], c=WHITE, lw=1.4, ls=(0, (6, 6)), alpha=.3)
    ax.plot([TVX, TVX], [-0.30, 0.60], c=WHITE, lw=1.4, ls=(0, (6, 6)), alpha=.3)
    for x, y, s in [(TVX, 0.66, "北"), (TVX, -0.36, "南"), (-0.88, TVY, "西"), (0.22, TVY, "東")]:
        T(ax, x, y, s, 26, WHITE, alpha=.75)
    T(ax, -0.86, 0.66, "俯視", 22, WHITE, ha="left", alpha=.55)
    ax.plot([0.34, 0.34], [-0.30, 0.62], c=WHITE, lw=1.2, alpha=.25)
    T(ax, SVX, 0.66, "側視", 22, WHITE, alpha=.55)
    arrow(ax, (0.885, 0.50), (0.885, TVY), WHITE, 2.2, .7, style="-|>,head_width=0.35,head_length=0.7")
    arrow(ax, (0.885, -0.18), (0.885, TVY), WHITE, 2.2, .7, style="-|>,head_width=0.35,head_length=0.7")
    T(ax, 0.885, 0.56, "上", 24, WHITE, alpha=.8)
    T(ax, 0.885, -0.25, "下", 24, WHITE, alpha=.8)


def sy_stations(ax):
    for nm, (k, c) in STN.items():
        x, y = tv_pos(k)
        ax.add_patch(Rectangle((x - BW, y - BH), 2*BW, 2*BH, fc=c, ec="none", alpha=.07))
        ax.add_patch(Rectangle((x - BW, y - BH), 2*BW, 2*BH, fill=False, ec=c, lw=2.0,
                               ls=(0, (5, 4)), alpha=.75))
        yy = sv_y(k)
        ax.add_patch(Rectangle((SVX - SW, yy - SHH), 2*SW, 2*SHH, fill=False, ec=c, lw=2.0,
                               ls=(0, (5, 4)), alpha=.75))
        T(ax, SVX, yy, nm, 22, c, alpha=.9)
    T(ax, tv_pos(-1)[0], tv_pos(-1)[1] + BH + 0.06, "冬至", 26, AMBER)
    T(ax, tv_pos(1)[0], tv_pos(1)[1] - BH - 0.06, "夏至", 26, BLUE)
    T(ax, TVX - 0.15, TVY - 0.14, "春秋分", 24, WHITE, ha="right", alpha=.9)


def sy_track(ax):
    for k0, k1 in [(-1, 0), (0, 1)]:                 # 只畫站與站之間（不穿過地塊）
        (x0, y0), (x1, y1) = tv_pos(k0), tv_pos(k1)
        ax.plot([x0 + BH, x1 - BH], [y0 - BH, y1 + BH], c=WHITE, lw=2.6, ls=(0, (7, 5)), alpha=.6)
    T(ax, -0.57, 0.235, "三萬里", 22, AMBER)
    T(ax, -0.12, 0.10, "三萬里", 22, BLUE)


def sy_block_tv(ax, dx=0.0, dy=0.0):
    x, y = TVX + dx, TVY + dy
    ax.add_patch(Rectangle((x - BW, y - BH), 2*BW, 2*BH, fc=GREEN, ec="none", alpha=.45))
    ax.add_patch(Rectangle((x - BW, y - BH), 2*BW, 2*BH, fill=False, ec=GREEN, lw=3.4))
    T(ax, x, y, "地", 30, WHITE)


def sy_block_sv(ax, dy=0.0):
    y = TVY + dy
    ax.add_patch(Rectangle((SVX - SW, y - SHH), 2*SW, 2*SHH, fc=GREEN, ec="none", alpha=.45))
    ax.add_patch(Rectangle((SVX - SW, y - SHH), 2*SW, 2*SHH, fill=False, ec=GREEN, lw=3.4))


QUOTE = {"冬至": ("「冬至地上，北而西三萬里」", AMBER, -0.50),
         "夏至": ("「夏至地下，南而東復三萬里」", BLUE, -0.61),
         "春秋分": ("「春秋二分其中矣」", WHITE, -0.72)}


def sy_quote(k):
    s, c, y = QUOTE[k]
    return lambda ax: T(ax, 0, y, s, 26, c)


# ══════════════════════════════════════════════════════════════
# 1b. 日影推演：照原文方向推——冬至地北移 → 日偏低、影長；夏至地南移 → 日偏高、影短
#     （這是依原文方位做的幾何推演，不是古籍原話；圖上與旁白都講明）
# ══════════════════════════════════════════════════════════════
SUN = (-0.62, 0.60)
GY, GH = -0.18, 0.34


def rg_title(ax):
    T(ax, 0, 0.90, "照這個方向推：影子會變", 36, WHITE)
    T(ax, 0, 0.80, "依原文方位推演・只看南北", 22, WHITE, alpha=.7)
    footer(ax)


def rg_sun(ax):
    ax.scatter([SUN[0]], [SUN[1]], s=1500, c=AMBER, alpha=.95, zorder=5)
    ax.scatter([SUN[0]], [SUN[1]], s=3600, c=AMBER, alpha=.15, zorder=4)
    T(ax, SUN[0] - 0.14, SUN[1], "日", 28, AMBER)
    ax.plot([-0.90, 0.90], [GY, GY], c=WHITE, lw=2.0, alpha=.45)
    T(ax, -0.86, GY - 0.08, "南", 26, WHITE, alpha=.75)
    T(ax, 0.86, GY - 0.08, "北", 26, WHITE, alpha=.75)


def rg_case(ax, gx, c, short, lab, ax0, ax1):
    tx, ty = gx, GY + GH
    vx, vy = tx - SUN[0], ty - SUN[1]
    ex = tx + vx * (GH / -vy)
    ax.plot([SUN[0], ex], [SUN[1], GY], c=c, lw=2.2, ls=(0, (6, 4)), alpha=.8)
    ax.plot([gx, ex], [GY, GY], c=c, lw=9, alpha=.95, solid_capstyle="butt", zorder=6)
    ax.plot([gx, gx], [GY, ty], c=WHITE, lw=7, solid_capstyle="round", zorder=7)
    T(ax, (gx + ex) / 2, GY - 0.09, "影短" if short else "影長", 26, c)
    arrow(ax, (ax1, -0.42), (ax0, -0.42), c, 3.2, .9, style="-|>,head_width=0.45,head_length=0.9")
    T(ax, (ax0 + ax1) / 2, -0.51, lab, 26, c)


def rg_winter(ax): rg_case(ax, 0.22, AMBER, False, "冬至：地往北", 0.10, 0.42)
def rg_summer(ax): rg_case(ax, -0.32, BLUE, True, "夏至：地往南", -0.20, -0.52)


def rg_end(ax):
    T(ax, 0, -0.68, "太陽在動？還是地在動？", 34, WHITE)
    T(ax, 0, -0.79, "同一個影子變化，兩種說法都解釋得通", 24, WHITE, alpha=.85)


# ══════════════════════════════════════════════════════════════
# 2. 舟行而人不覺：船（有篷的艙，剖開看得到裡面）＋閉牖＋坐著的人
# ══════════════════════════════════════════════════════════════
WL = -0.26                       # 水線
FL = WL + 0.08                   # 艙板


def hull_pts(ox=0.0, oy=0.0, s=1.0):
    top = [(-0.74, 0.20), (-0.62, 0.11), (-0.40, 0.08), (0.40, 0.08), (0.62, 0.12), (0.78, 0.24)]
    bot = [(0.66, 0.02), (0.45, -0.10), (-0.45, -0.10), (-0.64, -0.01)]
    return [(ox + x*s, oy + WL*s + y*s) if False else (ox + x*s, oy + (WL + y)*s) for x, y in top + bot]


def boat(ax, ox=0.0, oy=0.0, s=1.0, c=GREEN):
    """船身＋有篷的艙（艙壁剖開，看得到艙內）"""
    Z = lambda x, y: (ox + x*s, oy + y*s)
    body = hull_pts(ox, oy, s)
    ax.add_patch(Polygon(body, closed=True, fc=BG, ec="none", zorder=3))
    ax.add_patch(Polygon(body, closed=True, fc=c, ec="none", alpha=.28, zorder=3))
    ax.add_patch(Polygon(body, closed=True, fill=False, ec=c, lw=4.0*s, zorder=4, joinstyle="round"))
    for yy in (WL + 0.02, WL - 0.04):                                  # 船板
        ax.plot(*zip(Z(-0.52, yy), Z(0.56, yy)), c=c, lw=1.6*s, alpha=.45, zorder=4)
    x0, x1, top = -0.36, 0.30, FL + 0.44                               # 艙
    ax.add_patch(Rectangle(Z(x0, FL), (x1 - x0)*s, (top - FL)*s, fc=BG, ec="none", zorder=4))
    ax.add_patch(Rectangle(Z(x0, FL), (x1 - x0)*s, (top - FL)*s, fc=c, ec="none", alpha=.07, zorder=4))
    for x in (x0, x1):
        ax.plot(*zip(Z(x, FL), Z(x, top)), c=c, lw=3.4*s, zorder=5)
    ax.plot(*zip(Z(x0 - 0.02, FL), Z(x1 + 0.02, FL)), c=c, lw=3.4*s, zorder=5)
    th = np.linspace(0, np.pi, 60)                                     # 弧形篷頂
    rx, cx, h = (x1 - x0)/2 + 0.07, (x0 + x1)/2, 0.11
    arc = [Z(cx + rx*np.cos(t), top + h*np.sin(t)) for t in th]
    ax.add_patch(Polygon(arc + [Z(cx - rx, top - 0.015), Z(cx + rx, top - 0.015)][::-1], closed=True,
                         fc=c, ec=c, lw=3.0*s, alpha=.35, zorder=5))
    ax.plot(*zip(*arc), c=c, lw=3.4*s, zorder=6)
    ax.plot(*zip(Z(cx - rx, top - 0.015), Z(cx + rx, top - 0.015)), c=c, lw=3.0*s, zorder=6)
    for f in (-0.55, -0.18, 0.18, 0.55):                               # 篷的竹骨
        t0 = math.acos(f)
        ax.plot(*zip(Z(cx + rx*f, top - 0.015), Z(cx + rx*f, top + h*math.sin(t0))),
                c=c, lw=1.6*s, alpha=.55, zorder=6)


def windows(ax, ox=0.0, oy=0.0, s=1.0, xs=(-0.25, 0.18)):
    Z = lambda x, y: (ox + x*s, oy + y*s)
    for x in xs:                                                       # 關上的窗（直欞＋橫檔）
        ax.add_patch(Rectangle(Z(x - 0.07, FL + 0.20), 0.14*s, 0.16*s, fc=BG, ec=WHITE,
                               lw=2.6*s, zorder=6))
        for k in range(1, 4):
            xx = x - 0.07 + k*0.035
            ax.plot(*zip(Z(xx, FL + 0.20), Z(xx, FL + 0.36)), c=WHITE, lw=1.6*s, alpha=.7, zorder=7)
        ax.plot(*zip(Z(x - 0.07, FL + 0.28), Z(x + 0.07, FL + 0.28)), c=WHITE, lw=1.6*s, alpha=.7, zorder=7)


def sitter(ax, ox=0.0, oy=0.0, s=1.0, c=AMBER, hx=-0.06):
    """艙中坐者（側面、面朝船頭＝右）：長凳上坐著，手放膝上"""
    Z = lambda x, y: (ox + x*s, oy + y*s)
    j = dict(solid_capstyle="round", solid_joinstyle="round", zorder=8)
    ax.plot(*zip(Z(hx - 0.07, FL + 0.11), Z(hx + 0.05, FL + 0.11)), c=WHITE, lw=5*s, alpha=.6, **j)   # 凳
    for x in (hx - 0.06, hx + 0.04):
        ax.plot(*zip(Z(x, FL + 0.11), Z(x, FL)), c=WHITE, lw=3*s, alpha=.5, **j)
    hip, sh, knee, ank, toe = (hx, FL + 0.14), (hx + 0.01, FL + 0.30), (hx + 0.13, FL + 0.145), \
        (hx + 0.14, FL + 0.015), (hx + 0.19, FL + 0.015)
    ax.plot(*zip(Z(*hip), Z(*sh)), c=c, lw=15*s, **j)                  # 軀幹
    ax.plot(*zip(Z(*hip), Z(*knee)), c=c, lw=13*s, **j)                # 大腿
    ax.plot(*zip(Z(*knee), Z(*ank)), c=c, lw=12*s, **j)                # 小腿
    ax.plot(*zip(Z(*ank), Z(*toe)), c=c, lw=9*s, **j)                  # 腳
    ax.plot(*zip(Z(hx + 0.015, FL + 0.28), Z(hx + 0.06, FL + 0.205), Z(hx + 0.12, FL + 0.165)),
            c=c, lw=9*s, **j)                                           # 手臂搭膝
    ax.add_patch(Circle(Z(hx + 0.02, FL + 0.37), 0.052*s, fc=c, ec="none", zorder=8))   # 頭


def boat_quote(ax):
    T(ax, 0, 0.88, "「譬如人在大舟中閉牖而坐」", 30, WHITE)
    T(ax, 0, 0.79, "《尚書・考靈曜》", 22, WHITE, alpha=.7)


def boat_water(ax):
    water(ax, y=WL, x0=-0.97, x1=0.97, c=BLUE, rows=3, amp=0.022, freq=14)


def boat_hull(ax): boat(ax)
def boat_windows(ax):
    windows(ax)
    T(ax, -0.62, FL + 0.50, "閉牖", 28, WHITE)
    arrow(ax, (-0.33, FL + 0.33), (-0.56, FL + 0.46), WHITE, 2.0, .7)
def boat_sitter(ax): sitter(ax)


def boat_motion(ax):
    arrow(ax, (0.92, FL + 0.30), (0.66, FL + 0.30), GREEN, 4.0, .95, style="-|>,head_width=0.5,head_length=1.0")
    T(ax, 0.79, FL + 0.40, "舟行", 26, GREEN)
    T(ax, 0, -0.62, "「舟行而人不覺也」", 36, WHITE)
    T(ax, 0, -0.73, "船在走，艙裡的人卻一點也感覺不到", 24, WHITE, alpha=.85)


def heng_dong(ax):
    T(ax, 0, 0.12, "「地恆動不止，", 46, WHITE)
    T(ax, 0.04, -0.02, "而人不知」", 46, WHITE)
    T(ax, 0, -0.18, "《尚書・考靈曜》", 24, WHITE, alpha=.7)


# ══════════════════════════════════════════════════════════════
# 2b. 兩種視角：從岸上看（船在動）／從艙裡看（一切靜止）
# ══════════════════════════════════════════════════════════════
def rv_split(ax):
    T(ax, 0, 0.88, "同一艘船，兩種視角", 36, WHITE)
    ax.plot([0, 0], [-0.42, 0.66], c=WHITE, lw=1.4, alpha=.3)
    T(ax, -0.47, 0.62, "從岸上看", 30, GREEN)
    T(ax, 0.47, 0.62, "從艙裡看", 30, AMBER)


def rv_outside(ax):
    ox, oy, s = -0.47, 0.20, 0.52
    water(ax, y=oy + WL*s, x0=-0.93, x1=-0.05, c=BLUE, rows=2, amp=0.012, freq=26)
    boat(ax, ox, oy, s); windows(ax, ox, oy, s)
    for k, (dx, ln) in enumerate([(0.02, 0.10), (0.05, 0.16), (0.08, 0.10)]):          # 尾流
        yy = oy + (WL + 0.02 + 0.05*k)*s
        ax.plot([ox - 0.80*s - dx, ox - 0.80*s - dx - ln], [yy, yy], c=GREEN, lw=2.4, alpha=.6 - .12*k)
    arrow(ax, (ox + 0.44, oy + (FL + 0.30)*s), (ox + 0.28, oy + (FL + 0.30)*s), GREEN, 3.0, .9,
          style="-|>,head_width=0.45,head_length=0.9")
    T(ax, -0.47, -0.24, "船在動", 30, GREEN)
    T(ax, -0.47, -0.34, "岸和水都在往後退", 22, WHITE, alpha=.8)


def rv_inside(ax):
    x0, x1, y0, y1 = 0.12, 0.84, -0.12, 0.46
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=BG, ec=AMBER, lw=3.0, zorder=5))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=AMBER, ec="none", alpha=.05, zorder=5))
    s, ox, oy = 0.95, 0.47, -0.12 - FL*0.95
    windows(ax, ox, oy, s, xs=(-0.22, 0.24))
    sitter(ax, ox, oy, s, hx=-0.05)
    ax.plot([0.47 + 0.20, 0.47 + 0.20], [y1, y1 - 0.14], c=WHITE, lw=1.8, alpha=.7, zorder=7)   # 吊燈
    ax.add_patch(Polygon([(0.62, y1 - 0.14), (0.72, y1 - 0.14), (0.69, y1 - 0.19), (0.65, y1 - 0.19)],
                         closed=True, fc=AMBER, ec=AMBER, alpha=.8, zorder=7))
    T(ax, 0.47, -0.24, "一切靜止", 30, AMBER)
    T(ax, 0.47, -0.34, "燈直直垂著，沒有線索", 22, WHITE, alpha=.8)


def rv_end(ax):
    T(ax, 0, -0.62, "誰在動？關在艙裡，判斷不出來", 30, WHITE)
    T(ax, 0, -0.73, "地在動而人不知，是同一個道理", 24, WHITE, alpha=.85)


# ══════════════════════════════════════════════════════════════
# 3. 時間軸：考靈曜 ↔ 伽利略；以及兩者「地動」的差異（不可剪）
# ══════════════════════════════════════════════════════════════
TY = 0.30


def tl_title(ax):
    T(ax, 0, 0.88, "同一個比喻", 40, WHITE)
    T(ax, 0, 0.78, "舟行而人不覺 × 伽利略的大船船艙", 24, WHITE, alpha=.8)


def tl_axis(ax):
    ax.plot([-0.86, 0.86], [TY, TY], c=WHITE, lw=2.4, alpha=.6)
    for x, c, top, lines in [(-0.60, AMBER, "西漢末～東漢初", ["《尚書・考靈曜》", "舟行而人不覺"]),
                             (0.60, BLUE, "1632 年", ["伽利略", "《關於兩大世界", "體系的對話》"])]:
        ax.scatter([x], [TY], s=420, c=c, zorder=5)
        T(ax, x, TY + 0.10, top, 26, c)
        for i, s in enumerate(lines):
            T(ax, x, TY - 0.10 - 0.085*i, s, 24 if i == 0 else 22, WHITE, alpha=.95 if i == 0 else .8)


def tl_gap(ax):
    y = -0.06
    ax.plot([-0.60, 0.60], [y, y], c=WHITE, lw=2.0, alpha=.6)
    for x in (-0.60, 0.60):
        ax.plot([x, x], [y - 0.04, y + 0.04], c=WHITE, lw=2.0, alpha=.6)
    T(ax, 0, y - 0.10, "相隔約一千六百年", 34, WHITE)


def tl_diff(ax):
    T(ax, 0, -0.33, "但兩者說的「地動」不一樣", 26, GREEN)
    T(ax, 0, -0.44, "四游：大地一年來回平移，天仍繞著地轉", 24, AMBER)
    T(ax, 0, -0.54, "伽利略：地球自轉，又繞太陽公轉", 24, BLUE)


def tl_same(ax):
    T(ax, 0, -0.68, "相同的是：身在其中，察覺不到自己在動", 26, WHITE)
    T(ax, 0, -0.80, "※ 不宜說成「中國比西方更早發現地動」", 20, WHITE, alpha=.6)


# ══════════════════════════════════════════════════════════════
# 4. 姚信：人為靈蟲，形最似天（近取諸身）→ 天南低北高；冬至極低而寒、夏至極起而熱
#    人面朝右＝南；天球：左＝北、右＝南
# ══════════════════════════════════════════════════════════════
HX, HY, HS = -0.50, 0.14, 0.74
FRONT = [(0.00, 0.50), (0.17, 0.44), (0.25, 0.32), (0.27, 0.22), (0.265, 0.18), (0.345, 0.085),
         (0.29, 0.045), (0.30, 0.005), (0.28, -0.025), (0.30, -0.06), (0.29, -0.14), (0.24, -0.195),
         (0.14, -0.21), (0.12, -0.30), (0.15, -0.42), (0.22, -0.55)]
BACK = [(0.00, 0.50), (-0.18, 0.45), (-0.28, 0.29), (-0.275, 0.10), (-0.20, -0.02), (-0.145, -0.12),
        (-0.15, -0.25), (-0.25, -0.40), (-0.36, -0.55)]


def hp(x, y): return HX + x*HS, HY + y*HS


def yao_title(ax):
    T(ax, 0, 0.88, "「人為靈蟲，形最似天」", 34, WHITE)
    T(ax, 0, 0.79, "《晉書・天文志》載三國吳・姚信", 22, WHITE, alpha=.7)
    T(ax, 0, -0.91, "※ 以人體類比天體的推論，非觀測證據", 20, WHITE, alpha=.55)


def yao_head(ax):
    f = catmull([hp(*p) for p in FRONT]); b = catmull([hp(*p) for p in BACK])
    ax.add_patch(Polygon(np.vstack([f, b[::-1]]), closed=True, fc=WHITE, ec="none", alpha=.08, zorder=3))
    ax.plot(f[:, 0], f[:, 1], c=AMBER, lw=5, zorder=5, solid_capstyle="round")
    ax.plot(b[:, 0], b[:, 1], c=BLUE, lw=5, zorder=5, solid_capstyle="round")
    ax.scatter(*hp(0.19, 0.19), s=90, c=WHITE, zorder=6)                                # 眼
    e = hp(-0.05, 0.12)
    ax.add_patch(Arc(e, 0.07, 0.11, theta1=100, theta2=280, ec=WHITE, lw=2.4, alpha=.6, zorder=6))
    T(ax, HX, 0.62, "人（側面，面朝南）", 22, WHITE, alpha=.7)


def yao_head_labels(ax):
    cx, cy = hp(0.30, -0.10)
    T(ax, -0.26, -0.40, "頤前侈臨胸", 26, AMBER)
    T(ax, -0.26, -0.49, "下巴前伸蓋到胸", 22, WHITE, alpha=.8)
    arrow(ax, (cx + 0.01, cy - 0.04), (-0.24, -0.35), AMBER, 2.2, .85)
    nx, ny = hp(-0.15, -0.16)
    T(ax, -0.74, -0.40, "項不能覆背", 26, BLUE)
    T(ax, -0.74, -0.49, "後頸蓋不到背", 22, WHITE, alpha=.8)
    arrow(ax, (nx - 0.01, ny - 0.02), (-0.72, -0.35), BLUE, 2.2, .85)


def yao_head_tilt(ax):
    (x0, y0), (x1, y1) = hp(-0.30, 0.02), hp(0.40, -0.18)
    ax.plot([x0, x1], [y0, y1], c=WHITE, lw=2.6, ls=(0, (7, 5)), alpha=.85, zorder=7)
    T(ax, x0 - 0.02, y0 + 0.07, "後高", 24, WHITE)
    T(ax, x1 + 0.02, y1 - 0.07, "前低", 24, WHITE)


SKX, SKY, SKR = 0.52, 0.14, 0.31


def yao_sky(ax):
    ax.add_patch(Circle((SKX, SKY), SKR, fill=False, ec=WHITE, lw=3.0, alpha=.9))
    ax.add_patch(Circle((SKX, SKY), SKR, fc=WHITE, ec="none", alpha=.04))
    ax.plot([SKX - SKR - 0.05, SKX + SKR + 0.05], [SKY, SKY], c=GREEN, lw=2.6, alpha=.8)
    T(ax, SKX - SKR - 0.03, SKY - 0.07, "北", 24, WHITE, alpha=.8)
    T(ax, SKX + SKR + 0.03, SKY - 0.07, "南", 24, WHITE, alpha=.8)
    T(ax, SKX, SKY + SKR + 0.10, "天", 30, WHITE)


def pole_layer(alt, c, lab_n, lab_s):
    def f(ax):
        a = math.radians(alt)
        nx, ny = SKX - SKR*math.cos(a), SKY + SKR*math.sin(a)
        sx, sy = 2*SKX - nx, 2*SKY - ny
        ax.plot([sx, nx], [sy, ny], c=c, lw=2.4, ls=(0, (6, 4)), alpha=.85)
        ax.add_patch(Ellipse((SKX, SKY), 2*SKR, 2*SKR*0.30, angle=90 - alt, fill=False, ec=c, lw=2.0, alpha=.55))
        ax.scatter([nx], [ny], s=240, c=AMBER, zorder=6)
        ax.scatter([sx], [sy], s=240, c=BLUE, zorder=6)
        T(ax, nx - 0.04, ny + 0.05, lab_n, 24, AMBER, ha="right")
        T(ax, sx + 0.02, sy - 0.09, lab_s, 24, BLUE)
    return f


def yao_bridge(ax):
    arrow(ax, (0.13, 0.14), (-0.13, 0.14), WHITE, 3.0, .85, style="-|>,head_width=0.45,head_length=0.9")
    T(ax, 0, 0.23, "近取諸身", 24, WHITE)


def yao_text(ax):
    T(ax, 0, -0.62, "「近取諸身，故知天之體", 28, WHITE)
    T(ax, 0.02, -0.73, "南低入地，北則偏高」", 28, WHITE)


def yao_seasons(ax):
    T(ax, 0, -0.62, "冬至極低：日去人遠 → 冰寒", 28, BLUE)
    T(ax, 0, -0.73, "夏至極起：日去人近 → 蒸熱", 28, AMBER)


# ══════════════════════════════════════════════════════════════
# 5. 圖卡：地有四游一頁看懂（9:16）
# ══════════════════════════════════════════════════════════════
def card():
    f, ax = newcard()
    def t(x, y, s, size=13, c=WHITE, ha="center", w="bold", a=1.0):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=c, ha=ha, va="center", weight=w, alpha=a)
    def rule(y): ax.plot([0.06, 0.94], [y, y], c=WHITE, lw=1.0, alpha=.3)
    t(0.5, 0.945, "地有四游", 28)
    t(0.5, 0.905, "《尚書・考靈曜》（漢代緯書）", 12, a=.7)
    for i, (k, v, c) in enumerate([("冬至", "地上，北而西三萬里", AMBER), ("夏至", "地下，南而東三萬里", BLUE),
                                   ("春秋分", "其中（居中）", WHITE)]):
        y = 0.845 - 0.05*i
        t(0.10, y, k, 15, c, "left"); t(0.33, y, v, 13, WHITE, "left", "normal", .9)
    rule(0.715)
    t(0.5, 0.675, "「地恆動不止，而人不知」", 16, AMBER)
    t(0.5, 0.63, "譬如人在大舟中閉牖而坐，", 12.5, WHITE, w="normal", a=.9)
    t(0.5, 0.60, "舟行而人不覺也", 12.5, WHITE, w="normal", a=.9)
    rule(0.565)
    t(0.5, 0.53, "約一千六百年後・伽利略（1632）", 14, BLUE)
    t(0.5, 0.49, "《關於兩大世界體系的對話》也把人關進大船船艙，", 11.5, WHITE, w="normal", a=.85)
    t(0.5, 0.46, "說明我們感覺不到地球在動", 11.5, WHITE, w="normal", a=.85)
    rule(0.43)
    t(0.5, 0.395, "但兩者說的「地動」不一樣", 13.5, GREEN)
    t(0.5, 0.358, "四游：大地一年來回平移，天仍繞著地轉", 11.5, WHITE, w="normal", a=.85)
    t(0.5, 0.328, "伽利略：地球自轉，又繞太陽公轉", 11.5, WHITE, w="normal", a=.85)
    t(0.5, 0.29, "相同的是：身在其中，察覺不到自己在動", 12.5, WHITE)
    rule(0.26)
    t(0.5, 0.225, "三國吳・姚信：「人為靈蟲，形最似天」", 13, WHITE)
    t(0.5, 0.188, "頤前侈臨胸、項不能覆背 → 天南低北高", 11.5, WHITE, w="normal", a=.85)
    t(0.5, 0.158, "冬至極低而冰寒，夏至極起而蒸熱", 11.5, WHITE, w="normal", a=.85)
    t(0.5, 0.075, "一個拿船來比，一個拿身體來比", 13, WHITE)
    t(0.5, 0.035, "萬國星空 C-02・師大天文社", 10.5, WHITE, w="normal", a=.5)
    save(f, "_圖卡", "地有四游_圖卡_黑底.png", transparent=False)


def preview(sub, name, fns):
    f, ax = newfig(dark=True)
    for fn in fns: fn(ax)
    save(f, sub, name, transparent=False)


if __name__ == "__main__":
    print("── 地有四游 ──")
    sy = [("題辭", sy_title), ("框", sy_frame), ("站位", sy_stations), ("軌跡", sy_track),
          ("地塊俯視", sy_block_tv), ("地塊側視", sy_block_sv),
          ("冬至", sy_quote("冬至")), ("夏至", sy_quote("夏至")), ("春秋分", sy_quote("春秋分"))]
    emit("地有四游", sy, title="地有四游")
    base = [sy_title, sy_frame, sy_stations, sy_track]
    for nm, k in [("冬至", -1), ("夏至", 1)]:        # 核對用：地塊移到該站（Canva 位移後的樣子）
        preview("地有四游", f"地有四游_預覽_{nm}_黑底.png",
                base + [lambda a, k=k: sy_block_tv(a, k*D, -k*D), lambda a, k=k: sy_block_sv(a, -k*SH),
                        sy_quote(nm)])

    print("── 日影推演 ──")
    emit("日影推演", [("題辭", rg_title), ("日", rg_sun), ("冬至", rg_winter), ("夏至", rg_summer),
                      ("結論", rg_end)], title="日影推演")

    print("── 舟行不覺 ──")
    emit("舟行不覺", [("恆動", heng_dong)], title="舟行不覺", preview_name="預覽_恆動")
    emit("舟行不覺", [("題辭", boat_quote), ("水", boat_water), ("船", boat_hull), ("閉牖", boat_windows),
                      ("人", boat_sitter), ("行進", boat_motion)], title="舟行不覺")

    print("── 兩種視角 ──")
    emit("兩種視角", [("分隔", rv_split), ("艙外", rv_outside), ("艙內", rv_inside), ("結論", rv_end)],
         title="兩種視角")

    print("── 時間軸 ──")
    emit("時間軸", [("題辭", tl_title), ("軸", tl_axis), ("間隔", tl_gap), ("差異", tl_diff), ("相同", tl_same)],
         title="時間軸")

    print("── 姚信：人形比天 ──")
    yao = [("題辭", yao_title), ("人形", yao_head), ("人形標註", yao_head_labels), ("傾斜軸", yao_head_tilt),
           ("天", yao_sky), ("極軸", pole_layer(36, WHITE, "北　偏高", "南　低入地")),
           ("極軸_冬至", pole_layer(20, BLUE, "冬至　極低", "")),
           ("極軸_夏至", pole_layer(52, AMBER, "夏至　極起", "")),
           ("類比箭頭", yao_bridge), ("近取諸身", yao_text), ("寒暑", yao_seasons)]
    emit("姚信人形比天", yao, title="人形比天",
         preview_layers=["題辭", "人形", "人形標註", "傾斜軸", "天", "極軸", "類比箭頭", "近取諸身"])
    preview("姚信人形比天", "人形比天_預覽_寒暑_黑底.png",
            [yao_title, yao_head, yao_head_tilt, yao_sky, pole_layer(20, BLUE, "冬至　極低", ""),
             pole_layer(52, AMBER, "夏至　極起", ""), yao_seasons])

    print("── 圖卡 ──")
    card()
    print("all done")
