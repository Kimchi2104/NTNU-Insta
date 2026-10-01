# -*- coding: utf-8 -*-
"""A-08 西伯利亞｜概念圖（方形透明分層：Reels 定格頁一頁疊一層）
  C-A08-01_宇宙追獵     → 逐字稿 06 鏡（埃文基層／米克馬克層）
  C-A08-02_候鳥看轉軸   → 逐字稿 08 鏡（北極星層／參宿四層）
輸出：05_素材/A-08_西伯利亞/_概念圖/
來源：埃文基＝Анисимов；Berezkin 母題索引（宇宙追獵）；米克馬克＝Hagar 1900〈The Celestial Bear〉；
      候鳥＝S. T. Emlen, Science 170 (1970) 1198；Scientific American 233(2) (1975)。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-08_西伯利亞/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#7C8BA8"

# 北斗示意（斗口在左、斗柄往右上）：天樞 天璇 天璣 天權 玉衡 開陽 搖光
DIP = [(0.00, 0.17), (0.02, 0.00), (0.24, -0.03), (0.25, 0.12),
       (0.40, 0.17), (0.53, 0.21), (0.68, 0.14)]
BOO = [(0.80, 0.06), (0.90, -0.03), (0.86, -0.15), (0.98, -0.22)]   # 牧夫座四顆（示意）
UMI = [(-0.40, 0.62), (-0.46, 0.57), (-0.51, 0.51), (-0.58, 0.45), (-0.55, 0.37),
       (-0.67, 0.34), (-0.70, 0.42), (-0.58, 0.45)]          # 小熊座（北極星在斗柄前端）


def dipper(ax, ox, oy, s, bowl_c, handle_c, extra=None, extra_c=None):
    P = [(ox + x * s, oy + y * s) for x, y in DIP]
    bowl = [P[0], P[1], P[2], P[3], P[0]]
    ax.plot(*zip(*bowl), c=bowl_c, lw=3.2, zorder=4)
    ax.plot(*zip(*[P[3], P[4], P[5], P[6]]), c=handle_c, lw=3.2, zorder=4)
    for i, p in enumerate(P):
        ax.scatter([p[0]], [p[1]], s=150, c=bowl_c if i < 4 else handle_c, zorder=5)
    if extra:
        E = [(ox + x * s, oy + y * s) for x, y in extra]
        ax.plot(*zip(*([P[6]] + E)), c=extra_c, lw=2.4, ls=(0, (4, 3)), zorder=4)
        for p in E:
            ax.scatter([p[0]], [p[1]], s=120, c=extra_c, zorder=5)
    return P


def c01_evenki(ax):
    T(ax, 0.0, 0.93, "一場永不結束的狩獵", 34, WHITE)
    T(ax, 0.0, 0.855, "北斗的宇宙追獵：西伯利亞 → 北美", 19, GREY, w="normal")
    T(ax, -0.88, 0.74, "埃文基（西伯利亞）", 21, AMBER, ha="left")
    P = dipper(ax, -0.12, 0.40, 0.95, AMBER, GREEN)
    ax.plot(*zip(*UMI), c=BLUE, lw=2.4, zorder=4)
    for p in UMI:
        ax.scatter([p[0]], [p[1]], s=90, c=BLUE, zorder=5)
    T(ax, -0.56, 0.27, "小熊座＝小駝鹿", 15, BLUE)
    # 銀河＝雪橇痕：畫面下緣一道
    xs = [-0.86 + i * 0.0288 for i in range(61)]
    ys = [0.12 + 0.025 * math.sin(i / 6.0) for i in range(61)]
    ax.plot(xs, ys, c=MW, lw=12, alpha=.20, zorder=3, solid_capstyle="round")
    ax.plot(xs, ys, c=MW, lw=2.2, alpha=.8, ls=(0, (6, 4)), zorder=3)
    T(ax, 0.50, 0.215, "銀河＝Манги 的雪橇痕", 16, MW)
    T(ax, P[1][0] + 0.10, P[1][1] - 0.075, "斗口＝駝鹿 Хэглэн（的腳）", 17, AMBER)
    T(ax, P[5][0] + 0.02, P[5][1] + 0.10, "斗柄＝追牠的獵人", 17, GREEN)
    T(ax, 0.0, 0.02, "駝鹿傍晚把太陽頂走，獵人追上、射中、把太陽搶回來——每天重演", 15.5,
      WHITE, w="normal")


def c01_mikmaq(ax):
    ax.plot([-0.90, 0.90], [-0.08, -0.08], c="#2A3456", lw=1.4, zorder=1)
    T(ax, 0.0, -0.155, "↓　有學者推測：一萬多年前跟著人走過白令陸橋　↓", 15.5, GREY,
      w="normal")
    T(ax, -0.88, -0.27, "米克馬克（北美東北部）", 21, AMBER, ha="left")
    P = dipper(ax, -0.52, -0.52, 0.95, AMBER, GREEN, extra=BOO, extra_c=GREEN)
    T(ax, P[1][0] + 0.02, P[1][1] - 0.075, "斗口＝熊", 17, AMBER)
    T(ax, 0.34, -0.25, "斗柄＋牧夫座＝七個獵人", 17, GREEN)
    T(ax, 0.0, -0.92, "同一個追獵的故事：只有獵物從駝鹿換成了熊", 17, WHITE, w="normal")


def pole_panel(ax, cx, cy, name, col, sub):
    r0 = 0.30
    for k, r in enumerate((0.12, 0.21, r0)):
        a0 = 20 + 55 * k
        ax.add_patch(C.Arc((cx, cy), 2 * r, 2 * r, theta1=a0, theta2=a0 + 250,
                           color=WHITE, lw=1.6, alpha=.45, ls=(0, (5, 4)), zorder=3))
        th = math.radians(a0 + 250)
        ax.annotate("", xy=(cx + r * math.cos(th + 0.12), cy + r * math.sin(th + 0.12)),
                    xytext=(cx + r * math.cos(th), cy + r * math.sin(th)),
                    arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=1.4, alpha=.6),
                    zorder=3)
    ax.scatter([cx], [cy], s=420, c=col, zorder=6, marker="*")
    T(ax, cx, cy + 0.075, name, 19, col)
    # 鳥：朝遠離轉軸的方向（往下）
    C.arrow(ax, (cx, cy - 0.60), (cx, cy - 0.36), c=AMBER, lw=4.0, alpha=.95, style="-|>")
    T(ax, cx, cy - 0.67, sub, 16, AMBER)


def c02_polaris(ax):
    T(ax, 0.0, 0.93, "候鳥看的是天空的轉軸", 34, WHITE)
    T(ax, 0.0, 0.855, "Emlen 1970：在天象儀裡養大的靛藍彩鵐", 19, GREY, w="normal")
    T(ax, -0.47, 0.66, "星空繞北極星轉", 19, WHITE)
    pole_panel(ax, -0.47, 0.22, "北極星", BLUE, "秋天往南飛")


def c02_betelgeuse(ax):
    T(ax, 0.47, 0.66, "把轉軸換成參宿四", 19, WHITE)
    pole_panel(ax, 0.47, 0.22, "參宿四", RED, "背著參宿四飛")
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.86), 1.76, 0.24,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.6, zorder=2))
    T(ax, 0.0, -0.69, "鳥記住的不是哪一顆星", 21, WHITE)
    T(ax, 0.0, -0.79, "是整片天空繞著轉的那一點", 21, AMBER)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    C.emit("", [("埃文基", c01_evenki), ("米克馬克", c01_mikmaq)], title="C-A08-01_宇宙追獵")
    C.emit("", [("北極星", c02_polaris), ("參宿四", c02_betelgeuse)],
           title="C-A08-02_候鳥看轉軸")
