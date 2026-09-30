# -*- coding: utf-8 -*-
"""C-01 論天三家｜概念圖 v2（方形透明分層：Canva 定格頁一頁疊一層）

輸出：05_素材/C-01_論天三家/{蓋天說, 渾天說, 宣夜說, _三家並置}/
規格：2052px 方形透明 PNG 分層＋黑底預覽；9:16 對照表圖卡 1215×2160。
      放進 Canva 是 1080 寬 → 圖上 1pt ≈ 1.39px，所以正文 ≥ 22pt、題辭 ≥ 26pt。
來源（原文照引，見逐字稿 v2 首留言）：
  《晉書・天文志》：古言天者有三家／周髀家「天員如張蓋，地方如棋局」「蟻行磨石」／
      蓋天「天似蓋笠，地法覆槃…日去地恒八萬里」／蔡邕上書／郗萌記宣夜之說
  《周髀算經》：天象蓋笠，地法覆槃；七衡徑數；八尺表影；正南千里句一尺五寸
  傳張衡《渾天儀注》：渾天如雞子，天體圓如彈丸，地如雞子中黃…北極出地上三十六度…半見半隱
  《大戴禮記・曾子天圓》：如誠天圓而地方，則是四角之不揜也
  唐開元十二年（724）南宮說、一行測影：滑州白馬至豫州上蔡 526 里 270 步，夏至影差二寸有餘
"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, FancyBboxPatch
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, BG, T, arrow, emit, save, newfig
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
C.set_base(os.path.join(BASE, "05_素材/C-01_論天三家"))
RED = "#FF6B6B"
SUB = {"蓋": "蓋天說", "渾": "渾天說", "宣": "宣夜說", "三": "_三家並置"}


def footer(ax, s="示意圖・非等比例", y=-0.94):
    T(ax, 0, y, s, 20, WHITE, alpha=.55)


def curved_arrow(ax, r, a0, a1, c=WHITE, lw=3.0, alpha=.85, cx=0.0, cy=0.0):
    """圓弧箭頭：從角度 a0 畫到 a1（度），箭頭在 a1"""
    ts = np.radians(np.linspace(a0, a1, 80))
    xs, ys = cx + r*np.cos(ts), cy + r*np.sin(ts)
    ax.plot(xs[:-3], ys[:-3], c=c, lw=lw, alpha=alpha, solid_capstyle="round")
    arrow(ax, (xs[-1], ys[-1]), (xs[-6], ys[-6]), c=c, lw=lw, alpha=alpha,
          style="-|>,head_width=0.5,head_length=0.9")


def dim_arrow(ax, x, y0, y1, c=WHITE, lw=2.0, alpha=.8):
    """垂直雙箭頭（尺寸標註）"""
    arrow(ax, (x, y1), (x, y0), c=c, lw=lw, alpha=alpha, style="<|-|>,head_width=0.35,head_length=0.7")


# ══════════════════════════════════════════════════════════════
# 蓋天說 1｜蓋天兩版（第一版：天員如張蓋、地方如棋局 → 周髀：天象蓋笠、地法覆槃）
# ══════════════════════════════════════════════════════════════
def gai2_title(ax):
    T(ax, 0, 0.91, "蓋天說，其實有兩版", 40, WHITE)
    footer(ax)


def gai2_v1(ax):
    T(ax, -0.70, 0.74, "第一版", 30, AMBER, ha="left")
    T(ax, -0.70, 0.645, "「天員如張蓋，地方如棋局」", 26, WHITE, ha="left")
    cx = -0.20
    yf, yb, hf, hb = 0.10, 0.22, 0.52, 0.40          # 棋局：略帶透視的方格地面
    for i in range(9):
        k = i/8
        ax.plot([cx-hf+2*hf*k, cx-hb+2*hb*k], [yf, yb], c=GREEN, lw=1.8, alpha=.75)
    for j in range(4):
        k = j/3; y = yf + (yb-yf)*k; h = hf + (hb-hf)*k
        ax.plot([cx-h, cx+h], [y, y], c=GREEN, lw=1.8, alpha=.75)
    ax.add_patch(Polygon([(cx-hf, yf), (cx+hf, yf), (cx+hb, yb), (cx-hb, yb)], closed=True,
                         fc=GREEN, alpha=.10, ec="none"))
    ts = np.linspace(0, math.pi, 90)                 # 張蓋：撐開的傘蓋（圓頂＋傘骨）
    ax.plot(cx + 0.46*np.cos(ts), 0.30 + 0.24*np.sin(ts), c=AMBER, lw=4)
    for a in np.linspace(0.15, math.pi-0.15, 7):
        ax.plot([cx, cx + 0.46*math.cos(a)], [0.54, 0.30 + 0.24*math.sin(a)], c=AMBER, lw=1.6, alpha=.6)
    ax.plot([cx-0.46, cx+0.46], [0.30, 0.30], c=AMBER, lw=1.6, alpha=.5, ls=(0, (4, 4)))
    T(ax, cx, 0.035, "《晉書・天文志》引周髀家", 20, WHITE, alpha=.6)


def gai2_corners(ax):
    """曾子：如誠天圓而地方，則是四角之不揜也（俯視：圓蓋蓋不住方地的四角）"""
    cx, cy, h = 0.64, 0.36, 0.15
    sq = [(cx-h, cy-h), (cx+h, cy-h), (cx+h, cy+h), (cx-h, cy+h)]
    ax.add_patch(Polygon(sq, closed=True, fc=RED, alpha=.35, ec=GREEN, lw=2.5))
    ax.add_patch(Circle((cx, cy), h, fc=BG, ec="none", alpha=1.0))
    ax.add_patch(Circle((cx, cy), h, fc=AMBER, alpha=.25, ec=AMBER, lw=2.5))
    T(ax, cx, cy+h+0.06, "俯視", 20, WHITE, alpha=.6)
    T(ax, cx, cy-h-0.065, "四角之不揜", 24, RED)
    T(ax, cx, cy-h-0.14, "——曾子", 20, WHITE, alpha=.7)


def gai2_v2(ax):
    T(ax, -0.70, -0.09, "第二版《周髀算經》", 30, AMBER, ha="left")
    T(ax, -0.70, -0.185, "「天象蓋笠，地法覆槃」", 26, WHITE, ha="left")
    xs = np.linspace(-0.80, 0.80, 161)
    sky = -0.33 - 0.17*(xs/0.8)**2
    earth = sky - 0.22
    ax.plot(xs, sky, c=AMBER, lw=4)
    ax.plot(xs, earth, c=GREEN, lw=4)
    ax.fill_between(xs, earth, earth-0.035, color=GREEN, alpha=.18, lw=0)
    for sgn in (-1, 1):
        x0, x1 = sgn*0.50, sgn*0.72
        y0 = -0.33 - 0.17*(x0/0.8)**2 - 0.27
        y1 = -0.33 - 0.17*(x1/0.8)**2 - 0.27
        arrow(ax, (x1, y1), (x0, y0), c=GREEN, lw=2.4, alpha=.9, style="-|>,head_width=0.4,head_length=0.8")
    T(ax, 0, -0.83, "中高外下・滂沲四隤", 26, GREEN)


# ══════════════════════════════════════════════════════════════
# 蓋天說 2｜側視（依《晉書・天文志》數值等比例）
#   外衡半徑 238000 里（周髀）；北極下地高於外衡下地 60000；外衡天高於北極下地 20000；
#   天中高於外衡 60000 → 天地處處相距 80000（日去地恒八萬里）
# ══════════════════════════════════════════════════════════════
SV_R, SV_Y0 = 0.72, -0.20
SV_K = SV_R/238000


def sv_earth(x):
    return SV_Y0 + SV_K*60000*(1 - (x/SV_R)**2)


def sv_sky(x):
    return SV_Y0 + SV_K*80000 + SV_K*60000*(1 - (x/SV_R)**2)


def side_frame(ax):
    xs = np.linspace(-0.92, 0.92, 185)
    ax.plot(xs, sv_sky(xs), c=AMBER, lw=4)
    ax.plot(xs, sv_earth(xs), c=GREEN, lw=4)
    ax.fill_between(xs, sv_earth(xs), sv_earth(xs)-0.04, color=GREEN, alpha=.20, lw=0)
    ax.plot([0, 0], [sv_earth(0), sv_sky(0)+0.04], c=WHITE, lw=1.4, ls=(0, (5, 5)), alpha=.5)
    ax.scatter([0], [sv_sky(0)], s=160, c=AMBER, zorder=6)
    ax.scatter([0], [sv_earth(0)], s=130, c=GREEN, zorder=6)
    T(ax, 0, sv_sky(0)+0.08, "北極（天中）", 22, AMBER)
    T(ax, -0.63, sv_sky(-0.63)+0.10, "天似蓋笠", 28, AMBER)
    T(ax, 0.62, sv_earth(0.62)-0.13, "地法覆槃", 28, GREEN)
    for sgn in (-1, 1):
        ax.plot([sgn*SV_R]*2, [sv_earth(SV_R)-0.04, sv_sky(SV_R)], c=WHITE, lw=1.2, ls=(0, (3, 4)), alpha=.35)
    T(ax, -SV_R, sv_earth(SV_R)-0.10, "外衡", 22, WHITE, alpha=.8)


def side_numbers(ax):
    dim_arrow(ax, -0.035, sv_earth(0)+0.01, sv_sky(0)-0.01, c=WHITE)
    T(ax, -0.07, (sv_earth(0)+sv_sky(0))/2, "八萬里", 24, WHITE, ha="right")
    dim_arrow(ax, -SV_R, sv_earth(SV_R)+0.01, sv_sky(SV_R)-0.01, c=WHITE)
    T(ax, -SV_R-0.035, (sv_earth(SV_R)+sv_sky(SV_R))/2, "八萬里", 24, WHITE, ha="right")
    for y, s, c in [(-0.50, "天中高於外衡　　　　　　六萬里", AMBER),
                    (-0.60, "北極下地高於外衡下地　　六萬里", GREEN),
                    (-0.70, "天地隆高相從，日去地恒　八萬里", WHITE)]:
        T(ax, 0, y, s, 24, c)


def side_sun(ax):
    """日麗天而平轉：太陽貼著天蓋，在水平圓上繞北極轉"""
    for r, col, nm in [(0.36, AMBER, "夏至\n內衡"), (SV_R, BLUE, "冬至\n外衡")]:
        y = sv_sky(r)
        ax.add_patch(Ellipse((0, y), 2*r, 0.045*r/SV_R, fill=False, ec=col, lw=2.2, ls=(0, (6, 4)), alpha=.8))
        ax.scatter([r], [y], s=420, c=AMBER, zorder=7, edgecolors=col, linewidths=3)
        T(ax, r + 0.06, y + 0.10, nm, 22, col, ha="left")
    T(ax, 0, 0.43, "日麗天而平轉", 28, WHITE)


def side_title(ax):
    T(ax, 0, 0.90, "蓋天說：天和地都是弧面", 38, WHITE)
    T(ax, 0, 0.80, "《晉書・天文志》", 22, WHITE, alpha=.7)
    footer(ax, "高度與外衡依文獻數值等比例・曲面形狀為示意")


# ══════════════════════════════════════════════════════════════
# 蓋天說 3｜七衡六間（俯視）
#   《周髀算經》內衡徑 238000 里、中衡徑 357000、外衡徑 476000；七衡等距，每間 19833⅓ 里（半徑）
# ══════════════════════════════════════════════════════════════
R_IN, R_OUT = 119000.0, 238000.0
HENG = [R_IN + i*(R_OUT - R_IN)/6 for i in range(7)]
QS = 0.76/R_OUT
NAMES = ["內衡", "二衡", "三衡", "中衡", "五衡", "六衡", "外衡"]
SEASON = {0: "夏至", 3: "春分・秋分", 6: "冬至"}
DIAM = {0: "徑 23.8 萬里", 3: "徑 35.7 萬里", 6: "徑 47.6 萬里"}
SUN_A = math.radians(222)


def ring(ax, r, c, lw, a, gap=False):
    """gap：上下各留 ±24° 缺口，給貼在內側那一圈的標籤（文字高度比環距大）"""
    th = np.radians(np.arange(0, 361))
    if gap:
        d = np.degrees(th) % 180
        th = np.where(np.abs(d - 90) < 24, np.nan, th)
    ax.plot(r*np.cos(th), r*np.sin(th), c=c, lw=lw, alpha=a)


def qi_rings(ax):
    for i, r in enumerate(HENG):
        key = i in SEASON
        ring(ax, r*QS, AMBER if key else WHITE, 4.0 if key else 2.0, .95 if key else .45, gap=(i-1) in SEASON)


def qi_center(ax):
    ax.scatter([0], [0], s=220, c=AMBER, zorder=6)
    T(ax, 0, -0.075, "北極", 24, AMBER)
    T(ax, 0, 0.92, "七衡六間（俯視）", 40, WHITE)


def qi_labels(ax):
    for i in SEASON:
        rr = HENG[i]*QS
        T(ax, 0, rr + 0.035, f"{NAMES[i]}（{SEASON[i]}）", 24, AMBER)
        T(ax, 0, -rr - 0.04, DIAM[i], 22, WHITE, alpha=.85)
    footer(ax, "七衡等距・內衡：外衡 ＝ 1：2（《周髀算經》）", -0.93)


def qi_sun(ax):
    ri, ro = HENG[0]*QS, HENG[6]*QS
    for r, col in [(ri, AMBER), (ro, BLUE)]:
        ax.scatter([r*math.cos(SUN_A)], [r*math.sin(SUN_A)], s=520, c=AMBER, zorder=7,
                   edgecolors=col, linewidths=3)
    a2 = SUN_A + math.radians(9)
    arrow(ax, (ro*math.cos(a2)*0.97, ro*math.sin(a2)*0.97), (ri*math.cos(a2)*1.06, ri*math.sin(a2)*1.06),
          c=WHITE, lw=2.4, alpha=.8, style="<|-|>,head_width=0.4,head_length=0.8")
    T(ax, ri*math.cos(SUN_A)+0.05, ri*math.sin(SUN_A)+0.075, "夏至", 22, AMBER, ha="left")
    T(ax, ro*math.cos(SUN_A)-0.02, ro*math.sin(SUN_A)-0.08, "冬至", 22, BLUE)


def qi_single(ax, k):
    for i, r in enumerate(HENG):
        if i == k:
            ring(ax, r*QS, AMBER, 5.0, 1.0)
        else:
            ring(ax, r*QS, WHITE, 1.4, .18, gap=(i == k+1))
    r = HENG[k]*QS
    ax.scatter([r*math.cos(SUN_A)], [r*math.sin(SUN_A)], s=520, c=AMBER, zorder=7)
    T(ax, 0, r + 0.035, NAMES[k] + (f"（{SEASON[k]}）" if k in SEASON else ""), 24, AMBER)


# ══════════════════════════════════════════════════════════════
# 蓋天說 4｜圭表測影（《周髀算經》八尺表：夏至影一尺六寸、冬至一丈三尺五寸）＋寸差千里
#   北在右：影子朝北，太陽在南（左上）；日高 = atan(8/影長)
# ══════════════════════════════════════════════════════════════
GB_X, GB_Y, GB_S = -0.25, -0.22, 0.05          # 表的位置、地面高度、一尺的畫布長度
GB_TOP = (GB_X, GB_Y + 8*GB_S)


def gb_base(ax):
    ax.plot([-0.95, 0.95], [GB_Y, GB_Y], c=WHITE, lw=2.2, alpha=.7)
    ax.plot([GB_X, GB_X], [GB_Y, GB_TOP[1]], c=WHITE, lw=7, solid_capstyle="butt")
    ax.add_patch(Polygon([(GB_X-0.05, GB_Y), (GB_X+0.05, GB_Y), (GB_X+0.035, GB_Y+0.03),
                          (GB_X-0.035, GB_Y+0.03)], closed=True, fc=WHITE, ec="none"))
    T(ax, GB_X-0.05, GB_Y+4*GB_S, "表\n八尺", 22, WHITE, ha="right")
    T(ax, -0.90, GB_Y+0.05, "南", 24, WHITE, alpha=.7)
    T(ax, 0.90, GB_Y+0.05, "北", 24, WHITE, alpha=.7)
    T(ax, 0, 0.91, "圭表測影", 40, WHITE)
    T(ax, 0, 0.815, "《周髀算經》：周髀長八尺", 22, WHITE, alpha=.75)


def gb_case(ax, chi, col, nm, zh, dist, ly, dy, lab_xy):
    L = chi*GB_S
    tip = (GB_X + L, GB_Y)
    ax.plot([GB_X, tip[0]], [GB_Y+dy, GB_Y+dy], c=col, lw=8, alpha=.95, solid_capstyle="butt", zorder=4)
    u = np.array([GB_TOP[0]-tip[0], GB_TOP[1]-tip[1]]); u /= np.linalg.norm(u)
    sun = (GB_TOP[0] + dist*u[0], GB_TOP[1] + dist*u[1])
    ax.plot([tip[0], sun[0]], [tip[1], sun[1]], c=col, lw=2.0, ls=(0, (7, 5)), alpha=.85)
    ax.add_patch(Circle(sun, 0.05, fc=AMBER, ec=col, lw=3, zorder=6))
    alt = math.degrees(math.atan2(8, chi))
    ax.add_patch(Arc(tip, 0.20, 0.20, theta1=180-alt, theta2=180, color=col, lw=2.0))
    T(ax, sun[0] + lab_xy[0], sun[1] + lab_xy[1], f"{nm}　日高約 {alt:.0f}°", 22, col, ha="left")
    T(ax, GB_X + L/2 if L > 0.2 else GB_X + 0.02, ly, f"{nm}影長 {zh}", 24, col,
      ha="center" if L > 0.2 else "left")


def gb_summer(ax):
    gb_case(ax, 1.6, AMBER, "夏至", "一尺六寸", 0.52, GB_Y - 0.075, 0.012, (0.09, 0.005))


def gb_winter(ax):
    gb_case(ax, 13.5, BLUE, "冬至", "一丈三尺五寸", 0.62, GB_Y - 0.165, -0.012, (-0.05, 0.10))


def gb_cunqian(ax):
    """寸差千里：周髀的假設 vs 唐開元十二年實測"""
    x0 = -0.80; k = 1.40/1000
    T(ax, x0, -0.49, "《周髀》：南北每差一千里，影長差一寸", 22, WHITE, ha="left")
    ax.plot([x0, x0 + 1000*k], [-0.56, -0.56], c=AMBER, lw=12, solid_capstyle="butt", alpha=.9)
    T(ax, x0 + 1000*k + 0.02, -0.56, "千里", 22, AMBER, ha="left")
    T(ax, x0, -0.68, "唐・南宮說、一行實測（724）：", 22, WHITE, ha="left")
    T(ax, x0, -0.755, "南北 526 里多，夏至影差兩寸多", 22, WHITE, ha="left")
    ax.plot([x0, x0 + 250*k], [-0.83, -0.83], c=BLUE, lw=12, solid_capstyle="butt", alpha=.9)
    T(ax, x0 + 250*k + 0.02, -0.83, "兩百多里就差一寸", 22, BLUE, ha="left")


# ══════════════════════════════════════════════════════════════
# 蓋天說 5｜蟻行磨石（《晉書・天文志》引周髀家）
#   磨盤與螞蟻各一層、都以畫布中心為圓心：Canva 裡直接旋轉元素（Match & Move 會平滑轉動）
#   磨左旋（逆時針，Canva 旋轉角為負）快；蟻右行（順時針）慢
# ══════════════════════════════════════════════════════════════
MILL_R = 0.50


def mill(ax, rot=0.0):
    ax.add_patch(Circle((0, 0), MILL_R, fc="#2A3150", ec=WHITE, lw=4, zorder=2))
    for k in range(12):
        a = math.radians(rot + k*30)
        for r0, r1, da, lw, al in [(0.10, 0.47, 16, 2.4, .60), (0.26, 0.46, 9, 1.6, .40)]:
            b = a + math.radians(15 if r0 > 0.2 else 0)
            p0 = (r0*math.cos(b), r0*math.sin(b))
            p1 = (r1*math.cos(b - math.radians(da)), r1*math.sin(b - math.radians(da)))
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], c=MW, lw=lw, alpha=al, zorder=3)
    ax.add_patch(Circle((0, 0), 0.075, fc=BG, ec=WHITE, lw=2.5, zorder=4))


def ant(ax, x, y, heading, L=0.17, c=AMBER):
    """折線螞蟻：頭、胸、腹三節＋三對腳＋觸角；heading 為前進方向（弧度）"""
    ch, sh = math.cos(heading), math.sin(heading)

    def P(u, v):
        return (x + (u*ch - v*sh)*L, y + (u*sh + v*ch)*L)

    def blob(u0, a, b):
        return [P(u0 + a*math.cos(t), b*math.sin(t)) for t in np.linspace(0, 2*math.pi, 40)]
    for u0, a, b in [(-0.33, 0.24, 0.16), (0.02, 0.14, 0.085), (0.27, 0.11, 0.10)]:
        ax.add_patch(Polygon(blob(u0, a, b), closed=True, fc=c, ec=c, lw=1, zorder=8))
    ax.plot(*zip(P(-0.06, 0), P(-0.14, 0)), c=c, lw=4, zorder=8)
    for u0, (u1, v1), (u2, v2) in [(0.08, (0.20, 0.22), (0.36, 0.34)),
                                   (0.02, (0.02, 0.26), (0.06, 0.44)),
                                   (-0.04, (-0.16, 0.22), (-0.36, 0.34))]:
        for s in (1, -1):
            ax.plot(*zip(P(u0, 0), P(u1, s*v1), P(u2, s*v2)), c=c, lw=3.2, zorder=7,
                    solid_capstyle="round", solid_joinstyle="round")
    for s in (1, -1):
        ax.plot(*zip(P(0.35, s*0.04), P(0.50, s*0.15), P(0.64, s*0.13)), c=c, lw=2.4, zorder=7,
                solid_capstyle="round", solid_joinstyle="round")


ANT_A = math.radians(58)


def mill_ant(ax, rot=0.0):
    a = ANT_A + math.radians(rot)
    ant(ax, 0.36*math.cos(a), 0.36*math.sin(a), a - math.pi/2)


def mill_dirs(ax):
    curved_arrow(ax, 0.64, 115, 245, c=WHITE, lw=4.5, alpha=.9)
    T(ax, -0.72, 0.64, "磨左旋（天）", 26, WHITE)
    T(ax, -0.72, 0.565, "轉得快", 22, WHITE, alpha=.7)
    curved_arrow(ax, 0.62, 52, 28, c=AMBER, lw=3.5, alpha=.95)
    T(ax, 0.70, 0.56, "蟻右行（日月）", 26, AMBER)
    T(ax, 0.70, 0.485, "爬得慢", 22, AMBER, alpha=.8)


def mill_title(ax):
    T(ax, 0, 0.91, "蟻行磨石", 40, WHITE)
    T(ax, 0, 0.815, "日月實東行，而天牽之以西沒", 24, WHITE, alpha=.8)
    T(ax, 0, -0.74, "磨左旋而蟻右去，磨疾而蟻遲，", 26, WHITE)
    T(ax, 0, -0.825, "故不得不隨磨以左迴焉", 26, WHITE)
    T(ax, 0, -0.925, "《晉書・天文志》引周髀家", 20, WHITE, alpha=.55)


# ══════════════════════════════════════════════════════════════
# 渾天說｜天球（正投影立體：前半實線、後半虛線）
#   傳張衡《渾天儀注》：北極出地上三十六度（古度，周天 365¼）；黃赤交角取二十四古度
#   二十八宿依漢代距度（角12 亢9 … 軫17，斗 26¼）沿赤道排列
# ══════════════════════════════════════════════════════════════
HR, HC = 0.60, (0.0, -0.03)
GU = 360/365.25
PHI, EPS = math.radians(36*GU), math.radians(24*GU)
_az, _el = math.radians(125), math.radians(12)
CAM = np.array([-math.sin(_az)*math.cos(_el), -math.cos(_az)*math.cos(_el), math.sin(_el)])
RV = np.cross([0, 0, 1.0], CAM); RV /= np.linalg.norm(RV)
UV = np.cross(CAM, RV)
POLE = np.array([0, math.cos(PHI), math.sin(PHI)])
E1, NORTH = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
EQ2 = np.cross(POLE, E1)
EC2 = math.cos(EPS)*EQ2 + math.sin(EPS)*POLE
XIU = [("角", 12), ("亢", 9), ("氐", 15), ("房", 5), ("心", 5), ("尾", 18), ("箕", 11),
       ("斗", 26.25), ("牛", 8), ("女", 12), ("虛", 10), ("危", 17), ("室", 16), ("壁", 9),
       ("奎", 16), ("婁", 12), ("胃", 14), ("昴", 11), ("畢", 16), ("觜", 2), ("參", 9),
       ("井", 33), ("鬼", 4), ("柳", 15), ("星", 7), ("張", 18), ("翼", 18), ("軫", 17)]


def pj(p, r=1.0):
    p = np.asarray(p)*r
    return HC[0] + HR*float(RV @ p), HC[1] + HR*float(UV @ p), float(CAM @ p)


def circ3(ax, e1, e2, c, lw=3.0, r=1.0):
    """三維大圓：前半實線、後半虛線"""
    pts = [pj(math.cos(t)*e1 + math.sin(t)*e2, r) for t in np.radians(np.arange(0, 361, 1))]
    for front in (True, False):
        seg = []
        for x, y, d in pts + [(None, None, None)]:
            if d is not None and (d >= 0) == front:
                seg.append((x, y)); continue
            if len(seg) > 1:
                ax.plot(*zip(*seg), c=c, lw=lw if front else lw*0.7, alpha=.95 if front else .35,
                        ls="-" if front else (0, (5, 4)))
            seg = []


def hun_sphere(ax):
    ax.add_patch(Circle(HC, HR, fill=False, ec=WHITE, lw=4, alpha=.9))
    ax.add_patch(Circle(HC, HR, fc=MW, ec="none", alpha=.05))


def horizon_pts(r=1.0):
    return [pj((math.cos(t)*E1 + math.sin(t)*NORTH)*r) for t in np.radians(np.arange(0, 361, 2))]


def hun_water(ax):
    """天表裏有水：下半球盛水，水面即地平面"""
    hz = horizon_pts()
    ax.add_patch(Polygon([(x, y) for x, y, _ in hz], closed=True, fc=BLUE, ec=BLUE, lw=1.5, alpha=.22))
    lower = [(HC[0] + HR*math.cos(t), HC[1] + HR*math.sin(t)) for t in np.radians(np.arange(180, 361, 2))]
    front = sorted([(x, y) for x, y, d in hz if d >= 0], key=lambda p: -p[0])
    ax.add_patch(Polygon(lower + front, closed=True, fc=BLUE, ec="none", alpha=.14))
    for k, (yy, w) in enumerate([(-0.40, 0.40), (-0.50, 0.30)]):
        xs = np.linspace(-w, w, 60)
        ax.plot(xs, HC[1] + yy + 0.012*np.sin(xs*40 + k), c=BLUE, lw=2, alpha=.6)
    T(ax, 0, -0.76, "天表裏有水……天地各乘氣而立，載水而浮", 24, BLUE)


def hun_earth(ax):
    d = horizon_pts(0.42)
    ax.add_patch(Polygon([(x, y) for x, y, _ in d], closed=True, fc=GREEN, ec=GREEN, lw=2.5,
                         alpha=.55, zorder=5))
    T(ax, -0.93, -0.20, "地如\n雞子中黃", 24, GREEN, ha="left")
    ex, ey, _ = pj(-E1*0.42)
    ax.plot([-0.69, ex-0.01], [-0.23, ey], c=GREEN, lw=1.2, alpha=.6)


def hun_poles(ax):
    n, s = pj(POLE*1.22), pj(-POLE*1.22)
    ax.plot([s[0], n[0]], [s[1], n[1]], c=WHITE, lw=1.6, ls=(0, (5, 4)), alpha=.6)
    pn, ps = pj(POLE), pj(-POLE)
    ax.scatter([pn[0], ps[0]], [pn[1], ps[1]], s=150, c=WHITE, zorder=7)
    T(ax, pn[0]-0.04, pn[1]+0.06, "北極", 24, WHITE, ha="right")
    T(ax, ps[0]+0.04, ps[1]-0.07, "南極", 24, WHITE, ha="left")
    arc = [pj(np.array([0, math.cos(a), math.sin(a)])*0.55) for a in np.linspace(0, PHI, 30)]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], c=WHITE, lw=2.2, alpha=.85)
    nh = pj(NORTH)
    ax.plot([HC[0], nh[0]], [HC[1], nh[1]], c=WHITE, lw=1.2, alpha=.5)
    mid = arc[len(arc)//2]
    ax.plot([-0.71, mid[0]-0.02], [0.11, mid[1]], c=WHITE, lw=1.2, alpha=.5)
    T(ax, -0.93, 0.14, "北極出地", 22, WHITE, ha="left")
    T(ax, -0.93, 0.075, "三十六度", 22, WHITE, ha="left")


def hun_equator(ax):
    circ3(ax, E1, EQ2, BLUE, lw=3.5)
    x, y, _ = pj(math.cos(math.radians(240))*E1 + math.sin(math.radians(240))*EQ2)
    T(ax, x+0.05, y+0.07, "赤道", 24, BLUE, ha="left")


def hun_ecliptic(ax):
    circ3(ax, E1, EC2, AMBER, lw=3.5)
    x, y, _ = pj(math.cos(math.radians(90))*E1 + math.sin(math.radians(90))*EC2)
    T(ax, x-0.06, y-0.07, "黃道", 24, AMBER, ha="right")
    T(ax, 0.64, -0.06, "黃赤交角", 22, AMBER, ha="left")
    T(ax, 0.64, -0.125, "約二十四度", 22, AMBER, ha="left")


def xiu_points():
    acc, out = 0.0, []
    for nm, w in XIU:
        t = math.radians(acc*GU - 30)
        out.append((nm, math.cos(t)*E1 + math.sin(t)*EQ2))
        acc += w
    return out


def hun_xiu(ax):
    for nm, p in xiu_points():
        x, y, d = pj(p)
        a = (1.0 if p[2] >= 0 else .30)*(1 if d >= 0 else .7)
        ax.scatter([x], [y], s=110 if d >= 0 else 60, c=WHITE, alpha=a, zorder=8, lw=0)


def hun_halves(ax):
    T(ax, 0.70, 0.24, "半見", 26, WHITE, ha="left")
    T(ax, 0.70, -0.50, "半隱", 26, WHITE, alpha=.45, ha="left")
    T(ax, 0, -0.85, "周天三百六十五度四分度之一……故二十八宿半見半隱", 22, WHITE, alpha=.9)


def hun_title(ax):
    T(ax, 0, 0.91, "「渾天如雞子，天體圓如彈丸，", 30, WHITE)
    T(ax, 0, 0.83, "地如雞子中黃」", 30, WHITE)
    T(ax, 0, 0.75, "傳張衡《渾天儀注》", 22, WHITE, alpha=.7)
    footer(ax)


# ══════════════════════════════════════════════════════════════
# 宣夜說｜無天殼，日月眾星浮於氣中（《晉書・天文志》引郗萌記先師所傳）
# ══════════════════════════════════════════════════════════════
def qi_layer(k):
    def fn(ax):
        rnd = random.Random(7 + k*13)
        if k == 0:        # 大團薄霧
            for _ in range(70):
                ax.scatter([rnd.gauss(0, .55)], [rnd.gauss(0, .5)], s=rnd.uniform(9000, 30000), c=PURPLE,
                           alpha=rnd.uniform(.025, .05), lw=0)
        elif k == 1:      # 中型氣團
            for _ in range(260):
                ax.scatter([rnd.uniform(-1, 1)], [rnd.uniform(-1, 1)], s=rnd.uniform(600, 3500), c=BLUE,
                           alpha=rnd.uniform(.03, .07), lw=0)
        else:             # 細塵
            for _ in range(1500):
                ax.scatter([rnd.uniform(-1, 1)], [rnd.uniform(-1, 1)], s=rnd.uniform(2, 16), c=MW,
                           alpha=rnd.uniform(.15, .45), lw=0)
    return fn


def xy_stars(ax):
    rnd = random.Random(11)
    n = 0
    while n < 170:
        x, y = rnd.uniform(-.96, .96), rnd.uniform(-.96, .96)
        size, a = rnd.uniform(6, 70), rnd.uniform(.45, 1.0)
        if y > 0.84 or y < -0.64:          # 題辭區不放星（避免星點看起來像筆畫）
            continue
        ax.scatter([x], [y], s=size, c=WHITE, alpha=a, lw=0, zorder=3)
        n += 1


def crescent(ax, x, y, r, c):
    ts = np.linspace(-math.pi/2, math.pi/2, 60)
    outer = [(x + r*math.cos(t), y + r*math.sin(t)) for t in ts]
    inner = [(x + 0.45*r*math.cos(t), y + r*math.sin(t)) for t in ts[::-1]]
    ax.add_patch(Polygon(outer + inner, closed=True, fc=c, ec="none", zorder=6))


BODIES = [(-0.45, 0.28, "日", None), (0.45, 0.38, "月", None),
          (0.06, 0.12, "歲星", (0.14, 0.03)), (-0.22, -0.28, "熒惑", (-0.13, 0.05)),
          (0.58, -0.12, "填星", (0.10, -0.02)), (-0.66, -0.02, "太白", (0.05, 0.12)),
          (0.28, -0.44, "辰星", (-0.12, -0.05))]


def xy_bodies(ax):
    for x, y, nm, v in BODIES:
        if nm == "日":
            for s, a in [(5200, .10), (2600, .18)]:
                ax.scatter([x], [y], s=s, c=AMBER, alpha=a, lw=0)
            ax.scatter([x], [y], s=1300, c=AMBER, zorder=6)
            T(ax, x, y-0.13, "日", 26, AMBER)
        elif nm == "月":
            crescent(ax, x, y, 0.065, WHITE)
            T(ax, x, y-0.12, "月", 26, WHITE)
        else:
            ax.scatter([x], [y], s=320, c=PURPLE, zorder=6)
            T(ax, x, y-0.075, nm, 22, PURPLE)
            arrow(ax, (x+v[0], y+v[1]), (x, y), c=PURPLE, lw=2.4, alpha=.8)


def xy_title(ax):
    T(ax, 0, 0.91, "「天了無質，仰而瞻之，高遠無極」", 30, WHITE)
    T(ax, 0, -0.925, "《晉書・天文志》引東漢郗萌記先師所傳", 20, WHITE, alpha=.6)


def xy_title2(ax):
    T(ax, 0, -0.71, "「日月眾星，自然浮生虛空之中，", 26, WHITE)
    T(ax, 0, -0.795, "其行其止皆須氣焉」", 26, WHITE)


# 青非真色：遠山皆青、深谷窈黑 —— 天的藍不是天殼的顏色
def ridge(base, peaks, seed, n=600):
    """山稜剪影：peaks = [(中心x, 半寬, 高), ...]，峰形略尖，加一點細碎起伏"""
    xs = np.linspace(-1.02, 1.02, n)
    ys = np.full(n, base)
    for c, w, h in peaks:
        ys = np.maximum(ys, base + h*np.clip(1 - np.abs(xs - c)/w, 0, None)**1.25)
    rnd = random.Random(seed)
    ys = ys + 0.006*np.sin(xs*47 + rnd.uniform(0, 6)) + 0.004*np.sin(xs*91 + rnd.uniform(0, 6))
    return xs, ys


VALLEY_X, VALLEY_W = -0.36, 0.09
HILLS = [(0.26, "#6F8FD8", 1, [(-0.80, 0.30, 0.16), (-0.35, 0.28, 0.22), (0.10, 0.30, 0.14), (0.55, 0.26, 0.24), (0.95, 0.25, 0.15)]),
         (0.14, "#7F98C4", 2, [(-0.95, 0.30, 0.18), (-0.55, 0.30, 0.20), (-0.05, 0.34, 0.24), (0.40, 0.25, 0.14), (0.80, 0.30, 0.20)]),
         (0.00, "#A59A78", 3, [(-0.75, 0.32, 0.20), (-0.20, 0.30, 0.16), (0.25, 0.32, 0.26), (0.75, 0.30, 0.15)]),
         (-0.16, "#C9A55A", 4, [(-0.66, 0.34, 0.30), (-0.08, 0.32, 0.36), (0.50, 0.36, 0.26), (0.98, 0.30, 0.22)])]


def qing_hills(ax):
    bottom = -0.50
    for base, col, seed, peaks in HILLS:
        xs, ys = ridge(base, peaks, seed)
        ax.fill_between(xs, ys, bottom, color=col, lw=0)
    base, _, seed, peaks = HILLS[-1]
    nx, near = ridge(base, peaks, seed)                            # 近山兩峰之間切出千仞深谷（V 形）
    xs = np.linspace(VALLEY_X-VALLEY_W, VALLEY_X+VALLEY_W, 41)
    rim = [(x, float(np.interp(x, nx, near)) + 0.005) for x in xs]
    ax.add_patch(Polygon(rim + [(VALLEY_X+0.012, bottom), (VALLEY_X-0.012, bottom)], closed=True,
                         fc="#000000", ec="none"))


def qing_labels(ax):
    T(ax, 0.50, 0.62, "遠道之黃山而皆青", 26, "#8FB0FF")
    arrow(ax, (0.55, 0.51), (0.53, 0.58), c="#8FB0FF", lw=2.4, alpha=.9)
    T(ax, 0.30, -0.60, "千仞之深谷而窈黑", 26, WHITE)
    arrow(ax, (VALLEY_X+0.015, -0.36), (0.02, -0.58), c=WHITE, lw=2.4, alpha=.9)


def qing_title(ax):
    T(ax, 0, 0.91, "青非真色", 40, WHITE)
    T(ax, 0, 0.815, "天看起來是藍的，不代表天有一層殼", 24, WHITE, alpha=.8)
    T(ax, 0, -0.75, "「夫青非真色，而黑非有體也」", 30, WHITE)
    T(ax, 0, -0.86, "《晉書・天文志》引郗萌記宣夜之說", 20, WHITE, alpha=.6)


# ══════════════════════════════════════════════════════════════
# 三家並置（一圖三欄，每欄一層；蔡邕評語各一層）
# ══════════════════════════════════════════════════════════════
COLX = {"蓋": -0.62, "渾": 0.0, "宣": 0.62}
COLC = {"蓋": AMBER, "渾": BLUE, "宣": PURPLE}
ICON_Y = 0.12


def trio_col(key):
    cx = COLX[key]

    def fn(ax):
        if key == "蓋":
            xs = np.linspace(-0.26, 0.26, 60)
            ax.plot(cx + xs, ICON_Y + 0.10 - 0.16*(xs/0.26)**2, c=AMBER, lw=4)
            ax.plot(cx + xs, ICON_Y - 0.12 - 0.16*(xs/0.26)**2, c=GREEN, lw=4)
            ax.scatter([cx], [ICON_Y + 0.10], s=120, c=AMBER, zorder=5)
            name, sub = "蓋天說", "天象蓋笠"
        elif key == "渾":
            ax.add_patch(Circle((cx, ICON_Y), 0.24, fill=False, ec=WHITE, lw=3.5))
            ax.add_patch(Ellipse((cx, ICON_Y), 0.48, 0.12, angle=-28, fill=False, ec=BLUE, lw=2.6))
            ax.add_patch(Ellipse((cx, ICON_Y), 0.48, 0.12, angle=-6, fill=False, ec=AMBER, lw=2.6))
            ax.add_patch(Ellipse((cx, ICON_Y), 0.22, 0.06, fc=GREEN, ec=GREEN, alpha=.8))
            name, sub = "渾天說", "渾天如雞子"
        else:
            rnd = random.Random(3)
            for _ in range(28):
                ax.scatter([cx + max(-.16, min(.16, rnd.gauss(0, .09)))], [ICON_Y + max(-.14, min(.14, rnd.gauss(0, .07)))],
                           s=rnd.uniform(1500, 4000), c=PURPLE, alpha=.05, lw=0)
            for _ in range(70):
                a = rnd.uniform(0, 2*math.pi); r = 0.27*math.sqrt(rnd.uniform(0, 1))
                ax.scatter([cx + r*math.cos(a)], [ICON_Y + r*math.sin(a)], s=rnd.uniform(6, 80),
                           c=WHITE, alpha=rnd.uniform(.4, 1), lw=0)
            name, sub = "宣夜說", "天了無質"
        T(ax, cx, -0.25, name, 36, COLC[key])
        T(ax, cx, -0.35, f"「{sub}」", 24, WHITE, alpha=.85)
    return fn


CAI = {"蓋": ["考驗天狀，", "多所違失」"], "渾": ["近得其情」"], "宣": ["絕無師法」"]}


def trio_cai(key):
    cx, col, lines = COLX[key], COLC[key], CAI[key]

    def fn(ax):
        n = len(lines)
        h = 0.05 + 0.085*n
        yc = -0.47 - h/2
        ax.add_patch(FancyBboxPatch((cx-0.27, -0.47-h), 0.54, h, boxstyle="round,pad=0.012,rounding_size=0.03",
                                    fc=BG, ec=col, lw=2.2, alpha=.95))
        for i, s in enumerate(lines):
            T(ax, cx, yc + (n-1)*0.0425 - i*0.085, ("「" if i == 0 else "") + s, 24, col)
    return fn


def trio_title(ax):
    T(ax, 0, 0.84, "論天三家", 44, WHITE)
    T(ax, 0, 0.73, "「古言天者有三家」——《晉書・天文志》", 22, WHITE, alpha=.75)


def trio_cai_note(ax):
    T(ax, 0, -0.80, "東漢蔡邕上書評三家", 24, WHITE, alpha=.85)
    T(ax, 0, -0.88, "見《晉書・天文志》", 20, WHITE, alpha=.55)


def trio_glow(ax):
    cx = COLX["宣"]
    for lw, a in [(14, .10), (8, .22), (3.5, .95)]:
        ax.add_patch(FancyBboxPatch((cx-0.29, -0.42), 0.58, 0.84, boxstyle="round,pad=0.01,rounding_size=0.05",
                                    fill=False, ec=PURPLE, lw=lw, alpha=a))


# ══════════════════════════════════════════════════════════════
# 9:16 對照表圖卡（輪播／片尾總結）
# ══════════════════════════════════════════════════════════════
ROWS = [("核心圖像", ["天象蓋笠\n地法覆槃", "天體圓如彈丸\n地如雞子中黃", "天了無質\n高遠無極"]),
        ("代表文本", ["《周髀算經》", "傳張衡\n《渾天儀注》", "郗萌記\n先師所傳"]),
        ("地的形狀", ["中高外下\n早期如棋局", "平而靜\n居天之中", "文獻未詳"]),
        ("日月怎麼走", ["附天平轉\n七衡六間", "隨天球周轉\n出沒地平", "浮於氣中\n或順或逆"]),
        ("能算曆法嗎", ["能（圭表）\n與實測不合", "能（渾儀）", "難以儀器化"]),
        ("蔡邕評語", ["考驗天狀\n多所違失", "近得其情", "絕無師法"]),
        ("後來", ["漢後式微", "成為主流\n沿用到明清", "思想史上\n影響深遠"])]


def card():
    f, ax = C.newcard(dark=True)
    cols = [(0.365, AMBER, "蓋天說"), (0.615, BLUE, "渾天說"), (0.865, PURPLE, "宣夜說")]
    T(ax, 0.5, 0.945, "論天三家 對照", 28, WHITE)
    T(ax, 0.5, 0.905, "「古言天者有三家」——《晉書・天文志》", 12, WHITE, alpha=.7)
    for x, c, nm in cols:
        T(ax, x, 0.85, nm, 18, c)
    ax.plot([0.05, 0.95], [0.825, 0.825], c=WHITE, lw=1.6, alpha=.5)
    y, h = 0.775, 0.095
    for lab, cells in ROWS:
        T(ax, 0.06, y, lab, 13, WHITE, ha="left", w="normal", alpha=.85)
        for (x, c, _), s in zip(cols, cells):
            ax.text(x, y, s, fontproperties=C.FP, fontsize=12.5, color=c, ha="center", va="center",
                    linespacing=1.5, zorder=12)
        ax.plot([0.05, 0.95], [y - h/2, y - h/2], c=WHITE, lw=0.8, alpha=.18)
        y -= h
    T(ax, 0.5, 0.075, "宣夜說算不出曆法，卻最接近今天的宇宙", 13, WHITE, w="normal")
    T(ax, 0.5, 0.035, "萬國星空 C-01・師大天文社", 10.5, WHITE, w="normal", alpha=.5)
    save(f, SUB["三"], "三家對照表_圖卡_黑底.png", transparent=False)


if __name__ == "__main__":
    print("── 蓋天兩版 ──")
    emit(SUB["蓋"], [("題辭", gai2_title), ("第一版", gai2_v1), ("四角", gai2_corners), ("第二版", gai2_v2)],
         title="蓋天兩版")
    print("── 側視（等比例）──")
    emit(SUB["蓋"], [("題辭", side_title), ("天地", side_frame), ("數值", side_numbers), ("日行", side_sun)],
         title="側視")
    print("── 七衡六間 ──")
    emit(SUB["蓋"], [("環", qi_rings), ("中心", qi_center), ("標籤", qi_labels), ("日位", qi_sun)],
         title="七衡六間")
    for i in range(7):
        f, ax = newfig(); qi_single(ax, i)
        save(f, SUB["蓋"], f"七衡六間_逐衡_{i+1}_{NAMES[i]}_透明.png")
    print("── 圭表測影 ──")
    emit(SUB["蓋"], [("表", gb_base), ("夏至", gb_summer), ("冬至", gb_winter), ("寸差千里", gb_cunqian)],
         title="圭表日影")
    print("── 蟻行磨石 ──")
    emit(SUB["蓋"], [("題辭", mill_title), ("磨盤", mill), ("蟻", mill_ant), ("旋向", mill_dirs)],
         title="蟻行磨石")
    C.emit_frames(SUB["蓋"], "蟻行磨石_磨盤", lambda ax, i: mill(ax, i*7.5), 4)
    print("── 渾天：天球 ──")
    emit(SUB["渾"], [("題辭", hun_title), ("天球", hun_sphere), ("載水而浮", hun_water), ("地", hun_earth),
                     ("極軸", hun_poles), ("赤道", hun_equator), ("黃道", hun_ecliptic),
                     ("二十八宿", hun_xiu), ("半見半隱", hun_halves)],
         preview_layers=["題辭", "天球", "載水而浮", "地", "極軸", "赤道", "黃道", "二十八宿"], title="天球")
    print("── 宣夜 ──")
    emit(SUB["宣"], [("氣_第1", qi_layer(0)), ("氣_第2", qi_layer(1)), ("氣_第3", qi_layer(2)),
                     ("眾星", xy_stars), ("日月五星", xy_bodies), ("題辭", xy_title), ("題辭2", xy_title2)],
         title="宣夜")
    emit(SUB["宣"], [("山", qing_hills), ("標籤", qing_labels), ("題辭", qing_title)], title="青非真色")
    print("── 三家並置 ──")
    emit(SUB["三"], [("題辭", trio_title), ("蓋天", trio_col("蓋")), ("渾天", trio_col("渾")),
                     ("宣夜", trio_col("宣")), ("評_蓋天", trio_cai("蓋")), ("評_渾天", trio_cai("渾")),
                     ("評_宣夜", trio_cai("宣")), ("評_出處", trio_cai_note), ("宣夜高亮", trio_glow)],
         title="論天三家")
    card()
    print("done")
