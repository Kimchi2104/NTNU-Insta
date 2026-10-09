# -*- coding: utf-8 -*-
"""H-冬至：一根棍子如何量出一年｜概念圖（C 系列骨架）

C-HDZ-01 圭表（表與圭層、夏至層、冬至層）：《周髀算經》表高八尺，夏至晷一尺六寸、冬至一丈三尺五寸；
         正午太陽在南、影子朝北
C-HDZ-02 一年的影子（影長層、一年層、一度層）：登封（北緯 34.4°）八尺表的正午影長（計算值），
         兩次最長之間＝365¼ 日；周天 365¼ 度＝太陽一天走一度
C-HDZ-03 折取其中（平頂層、兩天層、取中層）：祖沖之大明五年（461）建康實測三次（《宋書．律曆志》），
         影長相同的兩天取中＝十一月三日夜半後三十一刻
C-HDZ-04 四丈高表（八尺層、四丈層、景符層）：郭守敬把表加高到四丈（橫梁離圭面四十尺），影長五倍；
         景符＝有小孔的銅片，讓太陽的小亮影與橫梁的細影同時落在圭上（《元史．天文志》）
C-HDZ-05 一年有多長（9:16 圖卡；可存圖）
C-HDZ-06 今天怎麼看（9:16 圖卡；台北 2026/12/22，PyEphem 自算）

執行：python3 make_hdz_diagrams.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import matplotlib.patheffects as PE

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/H-冬至_圭表/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL, STONE = "#FF6B6B", "#7C8BA8", "#1B2240", "#9AA6BF"
TROPICAL = 365.24219          # 今天的平均回歸年（J2000）
TPE = (25.0330, 121.5654)


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, rot=0, va="center", alpha=1.0, halo=False):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, rotation=rot, rotation_mode="anchor", alpha=alpha, linespacing=1.25,
            path_effects=[PE.withStroke(linewidth=4, foreground=CB.BG)] if halo else None)


def sun(ax, x, y, r, z=8):
    for k, op in ((2.2, .10), (1.6, .18)):
        ax.add_patch(CB.Circle((x, y), r * k, fc=AMBER, ec="none", alpha=op, zorder=z))
    ax.add_patch(CB.Circle((x, y), r, fc="#FFE08A", ec="none", zorder=z + 1))


def chi(x):
    """尺 → 中文（一丈三尺五寸）"""
    zh = "〇一二三四五六七八九"
    zhang, rest = divmod(round(x * 10), 100)
    c, cun = divmod(rest, 10)
    s = (f"{zh[zhang]}丈" if zhang else "") + (f"{zh[c]}尺" if c else "") + (f"{zh[cun]}寸" if cun else "")
    return s


# ══════════════════════ C-HDZ-01 圭表 ══════════════════════
G0X, G0Y, SC = -0.55, -0.33, 0.095          # 表的底、每尺的長度（畫布單位）
TOP = (G0X, G0Y + 8 * SC)


def shadow_case(ax, L, col, label, alt_note, lab_xy, ha, k):
    tip = (G0X + L * SC, G0Y)
    dx, dy = TOP[0] - tip[0], TOP[1] - tip[1]
    sx, sy = TOP[0] + dx * k, TOP[1] + dy * k
    ax.plot([tip[0], sx], [tip[1], sy], c=AMBER, lw=1.6, alpha=.55, ls=(0, (6, 4)), zorder=5)
    sun(ax, sx, sy, 0.035)
    ax.plot([G0X, tip[0]], [G0Y + 0.012, G0Y + 0.012], c=col, lw=9, alpha=.85, zorder=6,
            solid_capstyle="butt")
    ctext(ax, lab_xy[0], lab_xy[1], label, 17, col, ha=ha)
    ctext(ax, lab_xy[0], lab_xy[1] - 0.055, alt_note, 11.5, GREY, w="normal", ha=ha)


def c01_base(ax):
    T(ax, 0.0, 0.92, "圭表：一根竿子量影子", 30, WHITE)
    T(ax, 0.0, 0.85, "《周髀算經》：表高八尺　每天正午量影子", 13.5, GREY, w="normal")
    ax.plot([-0.95, 0.95], [G0Y, G0Y], c=WHITE, lw=1.2, alpha=.45, zorder=2)
    # 圭：平放的石尺（往北）
    ax.add_patch(CB.Rectangle((G0X, G0Y - 0.045), 14.6 * SC, 0.045, fc=STONE, ec="none", alpha=.55, zorder=3))
    for i in range(15):
        x = G0X + i * SC
        h = 0.03 if i % 5 == 0 else 0.016
        ax.plot([x, x], [G0Y - 0.045, G0Y - 0.045 + h], c=CB.BG, lw=1.4, zorder=4)
        if i % 5 == 0:
            ctext(ax, x, G0Y - 0.085, f"{i} 尺", 11, GREY, w="normal")
    # 表：八尺的竿子
    ax.add_patch(CB.Rectangle((G0X - 0.018, G0Y), 0.036, 8 * SC, fc=WHITE, ec="none", zorder=7))
    ctext(ax, G0X - 0.06, G0Y + 4 * SC, "表\n八尺", 16, WHITE, ha="right")
    ctext(ax, G0X + 7.3 * SC, G0Y - 0.14, "圭：平放在地上、量影子的尺", 14, STONE)
    ctext(ax, -0.92, -0.52, "南", 15, WHITE, ha="left")
    ctext(ax, 0.92, -0.52, "北", 15, WHITE, ha="right")
    ax.annotate("", xy=(0.86, -0.52), xytext=(-0.84, -0.52),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2, alpha=.6))
    ctext(ax, 0.0, -0.66, "北半球：正午太陽在南方，影子朝北", 14, WHITE, w="normal")


def c01_summer(ax):
    shadow_case(ax, 1.6, BLUE, "夏至　一尺六寸", "太陽高約 79°（依影長換算）", (-0.33, -0.05), "left", 0.28)


def c01_winter(ax):
    shadow_case(ax, 13.5, AMBER, "冬至　一丈三尺五寸", "最長的一天；太陽高約 31°（依影長換算）",
                (0.88, 0.06), "right", 0.20)
    ctext(ax, 0.0, -0.76, "一年裡影子最長的那天，就是冬至", 17, AMBER)
    ctext(ax, 0.0, -0.88, "影長：《周髀算經》；示意圖（太陽方向依影長換算）", 10.5, GREY, w="normal")


# ══════════════════════ C-HDZ-02 一年的影子 ══════════════════════
PHI_DF = 34.40                   # 登封告成鎮（周公測景台、觀星台）
EPS = 23.44
CH = dict(x0=-0.84, x1=0.88, y0=-0.20, y1=0.62, t0=-50, t1=420, L0=0.0, L1=14.0)


def noon_shadow(t, phi=PHI_DF, h=8.0):
    dec = -EPS * math.cos(2 * math.pi * t / TROPICAL)
    alt = 90 - phi + dec
    return h / math.tan(math.radians(alt))


def cx(t):
    return CH["x0"] + (t - CH["t0"]) / (CH["t1"] - CH["t0"]) * (CH["x1"] - CH["x0"])


def cy(L):
    return CH["y0"] + (L - CH["L0"]) / (CH["L1"] - CH["L0"]) * (CH["y1"] - CH["y0"])


def c02_curve(ax):
    T(ax, 0.0, 0.92, "一年的影子", 30, WHITE)
    T(ax, 0.0, 0.85, "登封（北緯 34.4°）八尺表的正午影長（計算值）", 13.5, GREY, w="normal")
    ax.plot([CH["x0"], CH["x1"]], [CH["y0"], CH["y0"]], c=WHITE, lw=1.2, alpha=.5, zorder=3)
    ax.plot([CH["x0"], CH["x0"]], [CH["y0"], CH["y1"]], c=WHITE, lw=1.2, alpha=.5, zorder=3)
    for L in (0, 5, 10):
        ax.plot([CH["x0"] - 0.012, CH["x0"]], [cy(L), cy(L)], c=WHITE, lw=1.2, alpha=.5)
        ctext(ax, CH["x0"] - 0.025, cy(L), f"{L} 尺", 11, GREY, w="normal", ha="right")
    marks = [(0, "冬至"), (91.3, "春分"), (182.6, "夏至"), (273.9, "秋分"), (365.24, "冬至")]
    for t, s in marks:
        ax.plot([cx(t), cx(t)], [CH["y0"], CH["y0"] - 0.015], c=WHITE, lw=1.2, alpha=.5)
        ctext(ax, cx(t), CH["y0"] - 0.05, s, 12, GREY, w="normal")
    ts = [CH["t0"] + i * (CH["t1"] - CH["t0"]) / 600 for i in range(601)]
    ax.plot([cx(t) for t in ts], [cy(noon_shadow(t)) for t in ts], c=AMBER, lw=3.2, zorder=6)
    ctext(ax, cx(182.6), cy(noon_shadow(182.6)) + 0.07, f"夏至 約{chi(noon_shadow(182.6))}", 13, BLUE)


def c02_year(ax):
    Lm = noon_shadow(0)
    for t in (0, 365.24):
        ax.scatter([cx(t)], [cy(Lm)], s=160, c=AMBER, zorder=8, lw=0)
        ax.plot([cx(t), cx(t)], [cy(Lm), cy(Lm) + 0.09], c=AMBER, lw=1.4, alpha=.8, zorder=7)
    y = cy(Lm) + 0.09
    ax.annotate("", xy=(cx(365.24), y), xytext=(cx(0), y),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=2.2), zorder=7)
    ctext(ax, (cx(0) + cx(365.24)) / 2, y + 0.06, "最長 → 最長＝一年：365¼ 天", 19, AMBER, halo=True)
    ctext(ax, cx(0), cy(Lm) - 0.17, f"冬至\n約{chi(Lm)}", 12, AMBER, halo=True)


def c02_degree(ax):
    box(ax, -0.90, -0.92, 1.80, 0.56, ec=GREEN, fc=PANEL, z=1, alpha=0.95)
    x0, y0, r = -0.58, -0.64, 0.20
    ax.add_patch(CB.Circle((x0, y0), r, fc="none", ec=WHITE, lw=1.2, alpha=.5, zorder=4))
    for i in range(0, 366, 5):
        a = math.pi / 2 - 2 * math.pi * i / 365.25
        k = 0.88 if i % 30 == 0 else 0.94
        ax.plot([x0 + r * k * math.cos(a), x0 + r * math.cos(a)], [y0 + r * k * math.sin(a), y0 + r * math.sin(a)],
                c=WHITE, lw=0.8, alpha=.45, zorder=4)
    for j, op in ((0, 1.0), (1, .55), (2, .3)):
        a = math.pi / 2 - 2 * math.pi * (40 - 6 * j) / 365.25
        ax.scatter([x0 + r * math.cos(a)], [y0 + r * math.sin(a)], s=90 - 20 * j, c=AMBER, alpha=op, zorder=6, lw=0)
    ctext(ax, x0, y0, "周天", 14, WHITE)
    ctext(ax, -0.30, -0.47, "所以天空也分成 365¼ 度", 18, GREEN, ha="left")
    ctext(ax, -0.30, -0.58, "太陽每天沿著它，走一度", 16, WHITE, ha="left", w="normal")
    ctext(ax, -0.30, -0.70, "（古度：1 度約等於今天的 0.986°）", 12, GREY, ha="left", w="normal")
    ctext(ax, -0.30, -0.82, "影長曲線為示意計算，未計地球軌道偏心", 10.5, GREY, ha="left", w="normal")


# ══════════════════════ C-HDZ-03 折取其中 ══════════════════════
# 祖沖之大明五年三次實測（《宋書．律曆志》）；日數以十一月三日 0 時為原點（十月小月 29 日）
ZU = [(-22, 10.775, "十月十日", "一丈七寸七分半"),
      (22, 10.8175, "十一月二十五日", "一丈八寸一分太"),
      (23, 10.75083, "十一月二十六日", "一丈七寸五分強")]
C_Q = None
T0 = None
L_MAX = None
PZ = dict(x0=-0.66, x1=0.88, y0=-0.42, y1=0.60, t0=-40, t1=40, L0=9.6, L1=11.75)


def zq(t):
    return L_MAX - C_Q * (t - T0) ** 2


def px(t):
    return PZ["x0"] + (t - PZ["t0"]) / (PZ["t1"] - PZ["t0"]) * (PZ["x1"] - PZ["x0"])


def py(L):
    return PZ["y0"] + (L - PZ["L0"]) / (PZ["L1"] - PZ["L0"]) * (PZ["y1"] - PZ["y0"])


def c03_flat(ax):
    T(ax, 0.0, 0.92, "折取其中：祖沖之怎麼找冬至", 28, WHITE)
    T(ax, 0.0, 0.85, "南朝宋．大明五年（461）建康實測　《宋書．律曆志》", 13, GREY, w="normal")
    ax.plot([PZ["x0"], PZ["x1"]], [PZ["y0"], PZ["y0"]], c=WHITE, lw=1.2, alpha=.5)
    ax.plot([PZ["x0"], PZ["x0"]], [PZ["y0"], PZ["y1"]], c=WHITE, lw=1.2, alpha=.5)
    for L in (10.0, 10.5, 11.0, 11.5):
        ax.plot([PZ["x0"] - 0.012, PZ["x0"]], [py(L), py(L)], c=WHITE, lw=1.2, alpha=.5)
        ctext(ax, PZ["x0"] - 0.025, py(L), chi(L), 10.5, GREY, w="normal", ha="right")
    for t in (-30, -20, -10, 0, 10, 20, 30):
        ax.plot([px(t), px(t)], [PZ["y0"], PZ["y0"] - 0.012], c=WHITE, lw=1.2, alpha=.5)
        ctext(ax, px(t), PZ["y0"] - 0.045, "冬至" if t == 0 else f"{t:+d} 天", 10.5, GREY, w="normal")
    ts = [PZ["t0"] + i * 0.2 for i in range(401)]
    ts = [t for t in ts if zq(t) >= PZ["L0"] + 0.05]
    ax.plot([px(t) for t in ts], [py(zq(t)) for t in ts], c=AMBER, lw=3.0, zorder=6)
    ax.add_patch(CB.Rectangle((px(-6), py(zq(T0)) - 0.10), px(6) - px(-6), 0.15, fc=AMBER, ec="none",
                              alpha=.12, zorder=4))
    d = (zq(T0) - zq(T0 + 5)) * 100
    ctext(ax, px(0), py(zq(T0)) + 0.10, f"冬至前後五天，影長只差約 {d:.1f} 分：看不出哪天最長", 13.5, WHITE,
          w="normal", halo=True)
    ctext(ax, 0.0, -0.62, "（一尺＝十寸＝百分；曲線依三次實測配出，示意）", 10.5, GREY, w="normal")


def c03_two(ax):
    for t, L, d, v in ZU:
        ax.scatter([px(t)], [py(L)], s=120, c=BLUE, zorder=8, lw=0)
    ctext(ax, px(-22), py(ZU[0][1]) - 0.08, f"{ZU[0][2]}\n{ZU[0][3]}", 12.5, BLUE, halo=True)
    ctext(ax, px(22) - 0.02, py(ZU[1][1]) + 0.10, f"{ZU[1][2]}\n{ZU[1][3]}", 12, BLUE, ha="right", halo=True)
    ctext(ax, px(23) + 0.02, py(ZU[2][1]) - 0.09, f"{ZU[2][2]}\n{ZU[2][3]}", 12, BLUE, ha="left", halo=True)


def c03_mid(ax):
    tm = 2 * T0 + 22                         # 十月十日影長在冬至後的對稱點
    y = py(ZU[0][1])
    ax.plot([px(-22), px(tm)], [y, y], c=GREEN, lw=1.6, ls=(0, (6, 4)), zorder=7)
    ax.scatter([px(tm)], [y], s=110, facecolors="none", edgecolors=GREEN, lw=2, zorder=8)
    ax.plot([px(T0), px(T0)], [PZ["y0"], py(zq(T0)) + 0.02], c=GREEN, lw=2.0, zorder=7)
    ax.annotate("", xy=(px(T0) - 0.01, y), xytext=(px(-22) + 0.02, y),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6), zorder=8)
    ax.annotate("", xy=(px(T0) + 0.01, y), xytext=(px(tm) - 0.02, y),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6), zorder=8)
    ctext(ax, px(T0), -0.70, "影子一樣長的兩天，正中間就是冬至", 17, GREEN)
    ctext(ax, px(T0), -0.80, "推得：十一月三日，夜半後三十一刻（比當時的《元嘉曆》晚一天）", 14, WHITE, w="normal")
    ctext(ax, 0.0, -0.90, "原文：「折取其中，則中天冬至，應在十一月三日」", 11, GREY, w="normal")


# ══════════════════════ C-HDZ-04 四丈高表 ══════════════════════
ALT_DF = 90 - PHI_DF - 23.52                  # 1279 年登封冬至正午太陽高度（黃赤交角 23.52°）
B0X, B0Y, S4 = -0.84, -0.55, 0.0262


def c04_eight(ax):
    T(ax, 0.0, 0.92, "四丈高表：把影子拉長五倍", 28, WHITE)
    T(ax, 0.0, 0.85, f"元．郭守敬　登封冬至正午（太陽高約 {ALT_DF:.0f}°）", 13, GREY, w="normal")
    ax.plot([-0.95, 0.95], [B0Y, B0Y], c=WHITE, lw=1.2, alpha=.45, zorder=2)
    ax.add_patch(CB.Rectangle((B0X, B0Y - 0.03), 66 * S4, 0.03, fc=STONE, ec="none", alpha=.5, zorder=3))
    L8 = 8 / math.tan(math.radians(ALT_DF))
    ax.add_patch(CB.Rectangle((B0X + 0.03, B0Y), 0.02, 8 * S4, fc=WHITE, ec="none", zorder=7))
    ax.plot([B0X + 0.04, B0X + 0.04 + L8 * S4], [B0Y + 0.008, B0Y + 0.008], c=BLUE, lw=8, zorder=6,
            solid_capstyle="butt")
    ctext(ax, B0X + 0.04 + L8 * S4 + 0.02, B0Y + 0.07, f"八尺表：影長約{chi(L8)}", 14, BLUE, ha="left")


def c04_forty(ax):
    L40 = 40 / math.tan(math.radians(ALT_DF))
    xb = B0X - 0.04
    ax.add_patch(CB.Rectangle((xb - 0.02, B0Y), 0.04, 40 * S4, fc=AMBER, ec="none", alpha=.9, zorder=5))
    ax.plot([xb - 0.07, xb + 0.07], [B0Y + 40 * S4] * 2, c=AMBER, lw=4, zorder=6)
    ctext(ax, xb + 0.09, B0Y + 40 * S4, "橫梁（離圭面四丈）", 13, AMBER, ha="left")
    tip = (xb + L40 * S4, B0Y)
    ax.plot([xb, tip[0]], [B0Y + 40 * S4, tip[1]], c=AMBER, lw=1.4, alpha=.5, ls=(0, (6, 4)), zorder=4)
    ax.plot([xb, tip[0]], [B0Y - 0.012, B0Y - 0.012], c=AMBER, lw=8, alpha=.85, zorder=6, solid_capstyle="butt")
    ctext(ax, tip[0], B0Y - 0.07, f"四丈高表：影長約{chi(L40)}（五倍）", 14, AMBER, ha="right")
    ctext(ax, 0.0, -0.72, "影子越長，量得越細；可是影子的邊緣也越模糊", 15, WHITE, w="normal")


def c04_fu(ax):
    box(ax, 0.06, 0.18, 0.86, 0.58, ec=GREEN, fc=PANEL, z=2, alpha=0.97)
    ctext(ax, 0.10, 0.70, "景符：有小孔的銅片", 16, GREEN, ha="left", z=10)
    gx0, gx1, gy = 0.14, 0.86, 0.27
    ax.plot([gx0, gx1], [gy, gy], c=STONE, lw=5, alpha=.8, zorder=4)
    ctext(ax, gx1, gy - 0.035, "圭面", 11, GREY, ha="right", w="normal")
    hx, hy = 0.50, 0.50                       # 小孔
    ax.plot([hx - 0.12, hx + 0.12], [hy - 0.05, hy + 0.05], c="#C9A46A", lw=5, zorder=6)
    ax.scatter([hx], [hy], s=30, c=CB.BG, zorder=7, lw=0)
    for dx in (-0.05, 0.05):
        ax.plot([hx - 0.18 + dx, hx, hx + 0.12 - dx * 0.6], [0.66, hy, gy], c=AMBER, lw=1.0, alpha=.45, zorder=5)
    ix = hx + 0.12
    ax.add_patch(CB.Ellipse((ix, gy + 0.012), 0.10, 0.03, fc="#FFE08A", ec="none", alpha=.95, zorder=7))
    ax.plot([ix - 0.004, ix + 0.004], [gy - 0.004, gy + 0.03], c=CB.BG, lw=2.2, zorder=8)
    ctext(ax, ix + 0.07, gy + 0.075, "太陽的小亮影", 11.5, AMBER, ha="left", w="normal")
    ctext(ax, ix + 0.07, gy + 0.040, "＋橫梁的細影", 11.5, WHITE, ha="left", w="normal")
    ctext(ax, 0.49, 0.215, "細影切過亮影正中央時讀數（《元史．天文志》）", 10.5, GREY, w="normal", z=10)


# ══════════════════════ 9:16 圖卡 ══════════════════════
YEARS = [("《尚書．堯典》", "366 日", "「期三百有六旬有六日」", 366.0, RED),
         ("四分曆（戰國～東漢）", "365¼ 日", "四年 1461 日", 365.25, AMBER),
         ("祖沖之《大明曆》（462）", "365.2428 日", "南朝宋", 365.2428148, AMBER),
         ("郭守敬等《授時曆》（1281）", "365.2425 日", "元；此值沿用南宋《統天曆》（1199）", 365.2425, GREEN),
         ("格里曆（1582）", "365.2425 日", "今天用的公曆", 365.2425, GREEN)]


def fmt_diff(d):
    s = abs(d) * 86400
    if s >= 3600:
        return f"多約 {s / 3600:.0f} 小時"
    if s >= 60:
        return f"多約 {s / 60:.0f} 分鐘"
    return "多不到一分鐘" if s >= 30 else "多不到半分鐘"


def c05_card(ax):
    ctext(ax, 0.5, 0.955, "一年有多長？", 30, WHITE)
    ctext(ax, 0.5, 0.920, "從冬至量到下一個冬至", 13, GREY, w="normal")
    x_line = 0.10
    y_top, step = 0.84, 0.122
    ax.plot([x_line, x_line], [y_top + 0.02, y_top - step * (len(YEARS) - 1) - 0.02], c=WHITE, lw=1.4, alpha=.35)
    for i, (who, val, note, yr, col) in enumerate(YEARS):
        y = y_top - i * step
        ax.scatter([x_line], [y], s=140, c=col, zorder=5, lw=0)
        ctext(ax, x_line + 0.05, y + 0.030, who, 13.5, WHITE, ha="left")
        ctext(ax, x_line + 0.05, y - 0.012, val, 22, col, ha="left")
        ctext(ax, x_line + 0.05, y - 0.050, note, 10.5, GREY, w="normal", ha="left")
        ctext(ax, 0.94, y - 0.012, fmt_diff(yr - TROPICAL), 13, col, ha="right", w="normal")
    y = y_top - len(YEARS) * step - 0.03
    box(ax, 0.06, y - 0.075, 0.88, 0.11, ec=WHITE, fc=PANEL, z=1, alpha=0.95)
    ctext(ax, 0.5, y - 0.005, "今天量到的一年：365.24219 日", 16, WHITE)
    ctext(ax, 0.5, y - 0.048, "（平均回歸年，2000 年；右欄＝跟它比，一年多出多少）", 10, GREY, w="normal")
    ctext(ax, 0.5, 0.075, "授時曆和公曆用的是同一個數字，時間相差三百年", 12, GREEN, w="normal")
    ctext(ax, 0.5, 0.045, "《堯典》的 366 日是約數；曆法另用閏月讓月份對上季節", 9.5, GREY, w="normal")
    ctext(ax, 0.5, 0.016, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


TODAY = {}


def compute_today():
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.pressure = 0; o.elevation = 10
    sol = ephem.Date(ephem.next_solstice("2026/12/1") + 8 * ephem.hour)
    o.date = ephem.Date("2026/12/22 00:00") - 8 * ephem.hour
    sun_ = ephem.Sun()
    tr = o.next_transit(sun_); o.date = tr; sun_.compute(o)
    alt = math.degrees(sun_.alt)
    o.date = ephem.Date("2026/12/22 00:00") - 8 * ephem.hour; o.horizon = "-0:34"
    r = o.next_rising(ephem.Sun()); s = o.next_setting(ephem.Sun())
    o.horizon = "0"
    alc = ephem.star("Alcyone")
    o.date = ephem.Date("2026/12/22 12:00") - 8 * ephem.hour
    ta = o.next_transit(alc); o.date = ta; alc.compute(o)
    mo = ephem.Moon(); mo.compute(o)
    gp = ephem.FixedBody(); gp._ra = math.radians(3.309); gp._dec = math.radians(15.18); gp._epoch = ephem.J2000
    o.date = ephem.Date("2026/12/22 18:00") - 8 * ephem.hour; gp.compute(o)
    loc = lambda d: ephem.Date(d + 8 * ephem.hour).tuple()
    TODAY.update(sol=ephem.Date(sol).tuple(), noon=loc(tr), alt=alt, shadow=1 / math.tan(math.radians(alt)),
                 rise=loc(r), set=loc(s), daylen=(s - r) * 24, alc_t=loc(ta), alc_alt=math.degrees(alc.alt),
                 moon_ph=mo.phase, moon_sep=math.degrees(ephem.separation(mo, alc)),
                 gp_alt=math.degrees(gp.alt), gp_az=math.degrees(gp.az))
    print(f"  · 今天：冬至 {TODAY['sol']}、正午 {TODAY['noon']} 高 {alt:.2f}° 影 {TODAY['shadow']:.3f} m、"
          f"晝長 {TODAY['daylen']:.3f} h、昴宿中天 {TODAY['alc_t']} 高 {TODAY['alc_alt']:.1f}°、"
          f"月 {TODAY['moon_ph']:.0f}% 距 {TODAY['moon_sep']:.1f}°、18:00 壁宿一 {TODAY['gp_alt']:.1f}°/{TODAY['gp_az']:.0f}°")


def hm(t):
    h, m = t[3], t[4] + (1 if t[5] >= 30 else 0)
    if m == 60:
        h, m = h + 1, 0
    return f"{h:02d}:{m:02d}"


def c06_card(ax):
    ctext(ax, 0.5, 0.955, "冬至，今天怎麼看", 30, WHITE)
    ctext(ax, 0.5, 0.920, "台北　2026/12/22（二）", 13, GREY, w="normal")
    # 上：正午的影子
    box(ax, 0.06, 0.555, 0.88, 0.335, ec=AMBER, fc=PANEL, z=1, alpha=0.95)
    gy, x0, s = 0.625, 0.20, 0.30
    ax.plot([0.10, 0.90], [gy, gy], c=WHITE, lw=1.2, alpha=.45, zorder=3)
    ax.add_patch(CB.Rectangle((x0 - 0.006, gy), 0.012, s * 0.5625, fc=WHITE, ec="none", zorder=6))
    sh = TODAY["shadow"] * s
    ax.plot([x0, x0 + sh], [gy + 0.004, gy + 0.004], c=AMBER, lw=7, zorder=5, solid_capstyle="butt")
    top = (x0, gy + s * 0.5625)
    k = 0.25
    ax.plot([x0 + sh, top[0] - sh * k], [gy, top[1] + (top[1] - gy) * k], c=AMBER, lw=1.4, alpha=.55,
            ls=(0, (6, 4)), zorder=4)
    sun(ax, top[0] - sh * k, top[1] + (top[1] - gy) * k, 0.018)
    ctext(ax, x0 - 0.025, gy + s * 0.28, "1 公尺", 11, WHITE, ha="right", w="normal")
    ctext(ax, x0 + sh / 2, gy - 0.025, f"影子約 {TODAY['shadow']:.2f} 公尺", 12, AMBER, w="normal")
    ctext(ax, 0.50, 0.855, f"正午 {hm(TODAY['noon'])}　太陽高 {TODAY['alt']:.1f}°", 16, AMBER)
    ctext(ax, 0.62, 0.79, "立一根 1 公尺的棍子", 12.5, WHITE, w="normal", ha="left")
    ctext(ax, 0.62, 0.755, "影子是今年最長的", 12.5, WHITE, w="normal", ha="left")
    ctext(ax, 0.62, 0.72, "（地面要平，棍子要直）", 10.5, GREY, w="normal", ha="left")
    # 中：時間表
    rows = [(f"{hm(TODAY['sol'])}", "冬至交節", WHITE),
            (f"{hm(TODAY['rise'])}–{hm(TODAY['set'])}",
             f"白天 {int(TODAY['daylen'])} 小時 {round((TODAY['daylen'] % 1) * 60)} 分，一年最短", WHITE),
            ("18:00", f"正南方高處（仰角約 {TODAY['gp_alt']:.0f}°）：東壁", BLUE),
            ("", "飛馬座大四邊形東邊的兩顆星", GREY),
            (hm(TODAY["alc_t"]), f"昴宿到頭頂正上方（仰角 {TODAY['alc_alt']:.0f}°）", AMBER),
            ("", f"月亮 {TODAY['moon_ph']:.0f}%，就在昴宿東邊約 {TODAY['moon_sep']:.0f}°（12/24 滿月）", GREY)]
    y = 0.495
    for t, s_, col in rows:
        if t:
            ctext(ax, 0.10, y, t, 15, col, ha="left")
        ctext(ax, 0.36, y, s_, 13 if col != GREY else 11, col if col != GREY else GREY, ha="left",
              w="bold" if col != GREY else "normal")
        y -= 0.055 if col != GREY else 0.06
    box(ax, 0.06, 0.085, 0.88, 0.085, ec=GREEN, fc=PANEL, z=1, alpha=0.95)
    ctext(ax, 0.5, 0.140, "《堯典》：日短星昴，以正仲冬", 14, GREEN)
    ctext(ax, 0.5, 0.106, "古人在冬至黃昏看到昴宿；今天要等到晚上九點半過後", 11, WHITE, w="normal")
    ctext(ax, 0.5, 0.050, "時刻、仰角：PyEphem 自算（台北，不含大氣折射）", 9.5, GREY, w="normal")
    ctext(ax, 0.5, 0.016, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


def main():
    global T0, L_MAX, C_Q
    # 祖沖之的算法：十月十日的影長落在二十五、二十六日之間 → 內插出對稱日 → 取中；
    # 再用對稱拋物線（以冬至為軸）穿過三次實測，畫示意曲線
    frac = (ZU[1][1] - ZU[0][1]) / (ZU[1][1] - ZU[2][1])
    mirror = 22 + frac
    T0 = (-22 + mirror) / 2
    C_Q = (ZU[1][1] - ZU[2][1]) / ((23 - T0) ** 2 - (22 - T0) ** 2)
    L_MAX = ZU[0][1] + C_Q * (-22 - T0) ** 2
    print(f"  · 祖沖之：對稱日 +{mirror:.3f}、冬至 t0 = {T0:.3f} 日（{T0 * 100:.0f} 刻）、最長 {L_MAX:.3f} 尺")
    os.makedirs(OUT, exist_ok=True)
    print("── C-HDZ 概念圖 ──")
    CB.emit("", [("表與圭", c01_base), ("夏至", c01_summer), ("冬至", c01_winter)], title="C-HDZ-01_圭表")
    CB.emit("", [("影長", c02_curve), ("一年", c02_year), ("一度", c02_degree)], title="C-HDZ-02_一年的影子")
    print(f"  · 登封八尺表：冬至 {noon_shadow(0):.2f} 尺、夏至 {noon_shadow(182.62):.2f} 尺")
    CB.emit("", [("平頂", c03_flat), ("兩天", c03_two), ("取中", c03_mid)], title="C-HDZ-03_折取其中")
    CB.emit("", [("八尺", c04_eight), ("四丈", c04_forty), ("景符", c04_fu)], title="C-HDZ-04_四丈高表")
    compute_today()
    for name, fn in [("C-HDZ-05_一年有多長", c05_card), ("C-HDZ-06_今天怎麼看", c06_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
