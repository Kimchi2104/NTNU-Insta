# -*- coding: utf-8 -*-
"""C-03 麒麟與倮獸：消失的第五象｜概念圖＋星圖 v2（方形透明分層：Canva 定格頁一頁疊一層）

輸出：05_素材/C-03_麒麟與倮獸/{四象盤, 五蟲說, 四象五蟲對照, 曾侯乙漆箱, 側面判讀, 民族來源,
      考工記五旗, 軒轅十七星, 牛郎織女, 弧矢九星, 倮獸主星候選, _圖卡}/
規格：2052px 方形透明 PNG 分層＋黑底預覽；9:16 圖卡 1215×2160。
      放進 Canva 是 1080 寬 → 圖上 1pt ≈ 1.39px，所以正文 ≥ 22pt、題辭 ≥ 26pt；標籤離邊 x ≤ ±0.93。
星圖：用 gen_ep_assets 的星表與投影（東在左、北在上），標籤改由本檔畫（字級與顏色才能照 C 系列規格）。
      軒轅 17 顆星逐顆編號（可數），兩顆 >5.5 等的暗星另加最小點徑，否則數不到。
來源（原文照引，見逐字稿 v2 首留言）：
  《大戴禮記・易本命》：有羽之蟲三百六十，而鳳皇為之長；有毛之蟲三百六十，而麒麟為之長；
      有甲之蟲三百六十，而神龜為之長；有鱗之蟲三百六十，而蛟龍為之長；倮之蟲三百六十，而聖人為之長。
  《禮記・月令》：中央土……其帝黃帝……其蟲倮（倮亦作裸）。
  《周禮・考工記・輈人》：龍旂九斿，以象大火也；鳥旟七斿，以象鶉火也；熊旗六斿，以象伐也；
      龜蛇四斿，以象營室也；弧旌枉矢，以象弧也。
  《史記・天官書》：權，軒轅。軒轅，黃龍體。／其東有大星曰狼……下有四星曰弧，直狼。
  曾侯乙墓漆箱（E.66，戰國早期，約前 433 年）：蓋面「斗」＋二十八宿全名＋青龍、白虎；
      側面（北方）的讀法不一：整面塗黑＝玄武／兩獸相對、中夾三星（危宿），社團簡報讀作麒麟。
  中國星座（師大天文社）.pptx p.9–21：四象與族群（東夷／南蠻／西羌／夏越、北方神鹿＝東胡）、
      倮獸主星三候選（軒轅十七星？牛郎織女星？弧矢星？）——社團考據觀點。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, Wedge, FancyBboxPatch
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, BG, T, arrow, emit, save, newfig, newcard
import gen_ep_assets as Gx

BASE = Gx.find_base(os.path.dirname(os.path.abspath(__file__)))
C.set_base(os.path.join(BASE, "05_素材/C-03_麒麟與倮獸"))
TIGER = "#E8ECF5"          # 白虎（近白，與 WHITE 區隔）


def footer(ax, s="示意圖・非等比例", y=-0.92):
    T(ax, 0, y, s, 22, WHITE, alpha=.55)


def title(ax, t, sub=None, size=38):
    T(ax, 0, 0.90, t, size, WHITE)
    if sub: T(ax, 0, 0.80, sub, 22, WHITE, alpha=.72)


# ══════════════════════════════════════════════════════════════
# 獸形符號（平滑輪廓，戰國漆器圖案化風格）。局部座標約 x∈[-1.4,1.4]、y∈[-0.6,1.0]，面朝右
# ══════════════════════════════════════════════════════════════
def catmull(pts, n=12, closed=False):
    P = [np.array(p, float) for p in pts]
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t*t
                              + (-p0 + 3*p1 - 3*p2 + p3)*t**3))
    if not closed:
        out.append(P[-2])
    return np.array(out)


class G:
    """把局部座標轉到畫布：平移 (x,y)、縮放 s、旋轉 rot 度、flip 左右翻"""
    def __init__(self, ax, x, y, s, c, lw=2.6, rot=0.0, flip=False, alpha=1.0, z=6):
        self.ax, self.x, self.y, self.s, self.c, self.lw = ax, x, y, s, c, lw
        self.ca, self.sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        self.f, self.alpha, self.z = (-1.0 if flip else 1.0), alpha, z

    def xf(self, pts):
        pts = np.asarray(pts, float)
        px, py = self.f * pts[:, 0], pts[:, 1]
        return np.c_[self.x + self.s*(px*self.ca - py*self.sa), self.y + self.s*(px*self.sa + py*self.ca)]

    def line(self, pts, lw=None, smooth=0, alpha=None, c=None):
        p = catmull(pts, smooth) if smooth else np.asarray(pts, float)
        q = self.xf(p)
        self.ax.plot(q[:, 0], q[:, 1], c=c or self.c, lw=lw or self.lw, alpha=alpha or self.alpha,
                     zorder=self.z, solid_capstyle="round", solid_joinstyle="round")

    def shape(self, pts, smooth=10, fill_alpha=.18, lw=None, c=None, fill=None):
        p = catmull(pts, smooth, closed=True) if smooth else np.asarray(pts, float)
        q = self.xf(p)
        self.ax.add_patch(Polygon(q, closed=True, fc=BG, ec="none", alpha=1.0, zorder=self.z - 1))
        self.ax.add_patch(Polygon(q, closed=True, fc=fill or c or self.c, ec="none",
                                  alpha=fill_alpha, zorder=self.z - 0.5))
        self.ax.add_patch(Polygon(q, closed=True, fill=False, ec=c or self.c, lw=lw or self.lw,
                                  alpha=self.alpha, zorder=self.z, joinstyle="round"))

    def dot(self, xy, r=0.045, c=None):
        q = self.xf([xy])[0]
        self.ax.add_patch(Circle(q, r*self.s, fc=c or self.c, ec="none", zorder=self.z + 1))


def tiger(ax, x, y, s, c=TIGER, lw=2.6, rot=0.0, flip=False):
    g = G(ax, x, y, s, c, lw, rot, flip)
    g.line([(-0.92, 0.24), (-1.18, 0.28), (-1.36, 0.50), (-1.28, 0.74), (-1.10, 0.76)], smooth=10, lw=lw+0.6)
    body = [(-0.95, 0.28), (-0.50, 0.36), (-0.05, 0.33), (0.38, 0.40), (0.60, 0.52), (0.70, 0.68),
            (0.74, 0.86), (0.86, 0.76), (1.00, 0.72), (1.18, 0.54), (1.16, 0.34), (0.94, 0.24),
            (0.72, 0.18), (0.64, -0.02), (0.68, -0.42), (0.80, -0.50), (0.50, -0.50), (0.46, -0.06),
            (0.08, -0.06), (-0.52, -0.08), (-0.56, -0.42), (-0.46, -0.50), (-0.76, -0.50),
            (-0.84, -0.12), (-1.00, 0.06)]
    g.shape(body, smooth=6)
    for bx in (-0.72, -0.46, -0.20, 0.06, 0.32):
        g.line([(bx, 0.33), (bx + 0.05, 0.20), (bx - 0.02, 0.08)], lw=lw - 0.6, smooth=6)
    g.dot((0.90, 0.54), 0.05)
    g.line([(1.06, 0.38), (0.92, 0.36)], lw=lw - 1.0)


def deer(ax, x, y, s, c=WHITE, lw=2.6, rot=0.0, flip=False, horn="one"):
    """麒麟／鹿：細腿長頸。horn='one'＝一角（麒麟），'antler'＝分叉角（鹿）"""
    g = G(ax, x, y, s, c, lw, rot, flip)
    body = [(-0.78, 0.18), (-0.30, 0.26), (0.22, 0.26), (0.42, 0.36), (0.54, 0.62), (0.64, 0.74),
            (0.86, 0.70), (1.00, 0.60), (0.96, 0.52), (0.74, 0.54), (0.62, 0.40), (0.50, 0.08),
            (-0.20, 0.00), (-0.72, 0.02), (-0.86, 0.10)]
    g.shape(body, smooth=6)
    for a, b in [((0.40, 0.06), (0.46, -0.52)), ((0.26, 0.04), (0.20, -0.52)),
                 ((-0.56, 0.02), (-0.52, -0.52)), ((-0.70, 0.04), (-0.78, -0.52))]:
        g.line([a, b])
    g.line([(-0.84, 0.16), (-1.00, 0.30), (-0.96, 0.40)], smooth=6)
    g.line([(0.64, 0.74), (0.56, 0.86)], lw=lw - 0.6)
    if horn == "one":
        g.line([(0.74, 0.74), (0.80, 0.96), (0.92, 1.02)], smooth=6, lw=lw + 0.2)
    else:
        g.line([(0.72, 0.74), (0.70, 1.00)], lw=lw - 0.2)
        g.line([(0.71, 0.88), (0.86, 0.98)], lw=lw - 0.8)
        g.line([(0.70, 1.00), (0.80, 1.10)], lw=lw - 0.8)
    g.dot((0.84, 0.64), 0.045)


def dragon(ax, x, y, s, c=GREEN, lw=2.4, rot=0.0, flip=False):
    g = G(ax, x, y, s, c, lw, rot, flip)
    spine = catmull([(-1.40, -0.05), (-1.05, 0.22), (-0.62, 0.05), (-0.20, -0.18), (0.22, 0.02),
                     (0.56, 0.22), (0.78, 0.28)], 14)
    n = len(spine)
    up, dn = [], []
    for i in range(n):
        t = i / (n - 1)
        a = spine[max(i-1, 0)]; b = spine[min(i+1, n-1)]
        d = b - a; d = d / (np.hypot(*d) + 1e-9); nrm = np.array([-d[1], d[0]])
        w = 0.02 + 0.10 * t
        up.append(spine[i] + nrm*w); dn.append(spine[i] - nrm*w)
    outline = up + dn[::-1]
    g.shape(outline, smooth=0)
    for i in range(6, n - 6, 5):                                         # 背鰭
        p = up[i]; q = up[i+2]
        d = q - p; nrm = np.array([-d[1], d[0]]); nrm /= (np.hypot(*nrm) + 1e-9)
        g.line([p, (p + q)/2 + nrm*0.08, q], lw=lw - 1.0)
    for i in range(8, n - 8, 6):                                         # 鱗紋
        a, b = up[i], dn[i]
        m = (a + b) / 2
        g.line([a*0.6 + m*0.4, m + (spine[min(i+2, n-1)] - spine[i])*0.6, b*0.6 + m*0.4], lw=lw - 1.4, alpha=.7)
    head = [(0.72, 0.40), (0.92, 0.46), (1.16, 0.40), (1.26, 0.30), (1.08, 0.27), (1.24, 0.18),
            (1.10, 0.12), (0.90, 0.16), (0.74, 0.18)]
    g.shape(head, smooth=0)
    g.line([(0.86, 0.44), (0.78, 0.64), (0.62, 0.72)], smooth=6, lw=lw)
    g.line([(0.94, 0.45), (0.94, 0.62), (0.86, 0.70)], smooth=6, lw=lw - 0.6)
    g.line([(1.20, 0.30), (1.34, 0.42), (1.36, 0.56)], smooth=6, lw=lw - 1.0)
    g.dot((1.00, 0.35), 0.04)
    for t in (0.36, 0.78):
        i = int(t * (n - 1)); p = dn[i]
        g.line([p, p + (0.06, -0.22), p + (0.18, -0.30)], lw=lw - 0.2)
        f = p + (0.18, -0.30)
        for dx, dy in [(0.08, 0.02), (0.08, -0.04), (0.02, -0.08)]:
            g.line([f, f + (dx, dy)], lw=lw - 1.2)


def bird(ax, x, y, s, c=AMBER, lw=2.4, rot=0.0, flip=False):
    g = G(ax, x, y, s, c, lw, rot, flip)
    for pts in [[(-0.28, 0.02), (-0.70, 0.10), (-1.05, 0.34), (-1.22, 0.58), (-1.10, 0.66)],
                [(-0.30, -0.04), (-0.78, -0.06), (-1.16, 0.06), (-1.30, 0.22)],
                [(-0.28, -0.10), (-0.70, -0.24), (-1.02, -0.34), (-1.16, -0.24)]]:
        g.line(pts, smooth=10, lw=lw)
    body = [(-0.34, 0.00), (-0.10, 0.18), (0.20, 0.20), (0.34, 0.28), (0.40, 0.48), (0.46, 0.60),
            (0.58, 0.64), (0.66, 0.58), (0.86, 0.56), (0.66, 0.50), (0.56, 0.40), (0.48, 0.12),
            (0.30, -0.12), (0.00, -0.18), (-0.24, -0.12)]
    g.shape(body, smooth=6)
    g.line([(0.52, 0.66), (0.44, 0.84), (0.56, 0.78), (0.58, 0.92)], smooth=6, lw=lw - 0.4)
    g.shape([(0.00, 0.14), (-0.18, 0.46), (-0.02, 0.70), (0.16, 0.56), (0.20, 0.22)], smooth=8, lw=lw - 0.4)
    g.dot((0.60, 0.58), 0.04)
    g.line([(0.06, -0.18), (0.08, -0.46), (0.20, -0.50)], lw=lw - 0.6)
    g.line([(0.18, -0.16), (0.22, -0.46), (0.34, -0.50)], lw=lw - 0.6)


def turtle(ax, x, y, s, c=BLUE, lw=2.4, rot=0.0, flip=False, snake=True):
    g = G(ax, x, y, s, c, lw, rot, flip)
    for lx in (-0.42, -0.20, 0.22, 0.44):
        g.line([(lx, -0.02), (lx + 0.04, -0.22)], lw=lw + 1.0)
    head = [(0.52, 0.04), (0.70, 0.14), (0.86, 0.10), (0.88, 0.00), (0.70, -0.04), (0.52, -0.06)]
    g.shape(head, smooth=6)
    shell = [(-0.62, -0.02)] + [(0.62*math.cos(a), 0.44*math.sin(a)) for a in np.linspace(math.pi, 0, 14)] + [(0.62, -0.02)]
    g.shape(shell, smooth=0)
    g.line([(-0.30, 0.0), (-0.24, 0.24), (0.0, 0.32), (0.24, 0.24), (0.30, 0.0)], lw=lw - 1.0, alpha=.8)
    g.line([(0.0, 0.32), (0.0, 0.44)], lw=lw - 1.0, alpha=.8)
    g.line([(-0.24, 0.24), (-0.48, 0.30)], lw=lw - 1.0, alpha=.8)
    g.line([(0.24, 0.24), (0.48, 0.30)], lw=lw - 1.0, alpha=.8)
    g.dot((0.78, 0.07), 0.035)
    if snake:
        g.line([(-0.86, -0.12), (-0.70, 0.30), (-0.30, 0.56), (0.10, 0.44), (0.34, 0.64), (0.24, 0.86),
                (0.04, 0.84)], smooth=10, lw=lw + 0.8)
        g.line([(-0.86, -0.12), (-0.98, -0.20)], lw=lw - 0.6)
        g.dot((0.04, 0.84), 0.06)


def human(ax, x, y, s, c=PURPLE, lw=2.6, rot=0.0):
    g = G(ax, x, y, s, c, lw, rot)
    ax.add_patch(Circle(g.xf([(0, 0.80)])[0], 0.17*s, fc=c, ec="none", alpha=.9, zorder=g.z))
    body = [(-0.30, 0.56), (0.30, 0.56), (0.36, 0.40), (0.24, -0.02), (0.22, -0.60), (0.06, -0.60),
            (0.00, -0.10), (-0.06, -0.60), (-0.22, -0.60), (-0.24, -0.02), (-0.36, 0.40)]
    g.shape(body, smooth=0, fill_alpha=.55)
    g.line([(-0.33, 0.50), (-0.52, 0.10), (-0.50, -0.14)], lw=lw + 0.6, smooth=6)
    g.line([(0.33, 0.50), (0.52, 0.10), (0.50, -0.14)], lw=lw + 0.6, smooth=6)


def bow(ax, x, y, s, c=PURPLE, lw=2.6, rot=0.0):
    """弓＋箭（弧旌枉矢）"""
    g = G(ax, x, y, s, c, lw, rot)
    a = np.linspace(-1.1, 1.1, 30)
    g.line(np.c_[-0.20 + 0.55*np.cos(a), 0.90*np.sin(a)], lw=lw + 0.8)
    top, bot = (-0.20 + 0.55*math.cos(1.1), 0.90*math.sin(1.1)), (-0.20 + 0.55*math.cos(-1.1), 0.90*math.sin(-1.1))
    g.line([top, (-0.22, 0.0), bot], lw=lw - 1.0, alpha=.8)
    g.line([(-0.22, 0.0), (0.92, 0.0)], lw=lw)
    g.line([(0.78, 0.10), (0.94, 0.0), (0.78, -0.10)], lw=lw)
    g.line([(-0.22, 0.0), (-0.34, 0.08)], lw=lw - 1.0)
    g.line([(-0.22, 0.0), (-0.34, -0.08)], lw=lw - 1.0)


def flag(ax, x, y, s, c, n, lw=2.2):
    """旗：旗桿＋旗面＋ n 條斿（垂帶）"""
    g = G(ax, x, y, s, c, lw)
    g.line([(-0.60, -0.90), (-0.60, 0.95)], lw=lw + 0.6)
    g.shape([(-0.60, 0.90), (0.62, 0.80), (0.70, 0.50), (-0.60, 0.40)], smooth=0, fill_alpha=.35)
    for k in range(n):
        fx = -0.50 + 1.10 * (k + 0.5) / n
        top = 0.40 + (0.50 - 0.40) * (fx + 0.6) / 1.30
        g.line([(fx, top), (fx + 0.04, top - 0.55), (fx - 0.02, top - 0.85)], lw=lw - 0.8, smooth=6)


# ══════════════════════════════════════════════════════════════
# 1. 四象盤（方位依地圖慣例：上北、右東）；中央先留空，後填倮獸
#    同一組幾何也給「民族來源」用
# ══════════════════════════════════════════════════════════════
WC, WR, W0 = (0.0, 0.0), 0.60, 0.19          # 圓心、外半徑、中央格半徑
SECT = {   # 方位: (中心角, 名, 色, 繪獸, 族群)
    "東": (0,   "青龍", GREEN, lambda ax, x, y: dragon(ax, x, y, 0.082, GREEN, 2.2), "東夷"),
    "北": (90,  "玄武", BLUE,  lambda ax, x, y: turtle(ax, x, y, 0.13, BLUE, 2.2),   "夏越"),
    "西": (180, "白虎", TIGER, lambda ax, x, y: tiger(ax, x, y, 0.082, TIGER, 2.2),  "西羌"),
    "南": (270, "朱雀", AMBER, lambda ax, x, y: bird(ax, x, y, 0.10, AMBER, 2.2),    "南蠻"),
}


def _pol(r, deg):
    return WC[0] + r*math.cos(math.radians(deg)), WC[1] + r*math.sin(math.radians(deg))


def wheel_ring(ax):
    ax.add_patch(Circle(WC, WR, fill=False, ec=WHITE, lw=2.0, alpha=.45))
    for d in (45, 135, 225, 315):
        (x0, y0), (x1, y1) = _pol(W0, d), _pol(WR, d)
        ax.plot([x0, x1], [y0, y1], c=WHITE, lw=1.6, alpha=.35)


def wheel_sector(k, glyph=True, direction=True, ethnic=False):
    a, nm, c, fn, eth = SECT[k]

    def f(ax):
        ax.add_patch(Wedge(WC, WR, a - 45, a + 45, width=WR - W0, fc=c, ec="none", alpha=.16))
        ax.add_patch(Wedge(WC, WR, a - 45, a + 45, width=WR - W0, fill=False, ec=c, lw=2.2, alpha=.6))
        ew = k in "東西"
        if glyph:
            if ew:
                gx, gy = _pol(0.41, a)
                fn(ax, gx, gy + 0.075)
                T(ax, gx, gy - 0.10, nm, 28, c)
            else:
                gx, gy = _pol(0.44, a)
                fn(ax, gx, gy - 0.03)
                T(ax, *_pol(0.275, a), nm, 28, c)
        elif ew:
            x0, y0 = _pol(0.38, a)
            T(ax, x0, y0 + 0.06, nm, 30, c)
        else:
            T(ax, *_pol(0.31, a), nm, 30, c)
        if direction:
            T(ax, *_pol(0.69, a), k, 26, WHITE, alpha=.75)
    return f


def wheel_center_empty(ax):
    ax.add_patch(Circle(WC, W0, fc=BG, ec=WHITE, lw=2.4, ls=(0, (6, 5)), alpha=.9))
    T(ax, WC[0], WC[1] + 0.035, "？", 44, WHITE)
    T(ax, WC[0], WC[1] - 0.10, "中央", 22, WHITE, alpha=.7)


def wheel_center_human(sub="倮・人"):
    def f(ax):
        ax.add_patch(Circle(WC, W0, fc=BG, ec="none"))
        ax.add_patch(Circle(WC, W0, fc=PURPLE, ec="none", alpha=.30))
        ax.add_patch(Circle(WC, W0, fill=False, ec=PURPLE, lw=3.2))
        human(ax, WC[0], WC[1] + 0.02, 0.085, PURPLE, 2.2)
        T(ax, WC[0], WC[1] - 0.115, sub, 22, WHITE)
    return f


def four_title(ax):
    title(ax, "四象", "東青龍・南朱雀・西白虎・北玄武")
    footer(ax, "方位依地圖慣例：上北、右東", y=-0.86)


def center_title(ax):
    title(ax, "中央，是誰的位置？")


def yueling(ax):
    T(ax, 0, -0.80, "「中央土……其帝黃帝……其蟲倮」", 28, AMBER)
    T(ax, 0, -0.89, "《禮記・月令》（倮，亦作裸）", 22, WHITE, alpha=.7)


# ══════════════════════════════════════════════════════════════
# 2. 五蟲說（《大戴禮記・易本命》）：一列一層
# ══════════════════════════════════════════════════════════════
WU = [("有羽之蟲", "鳳皇", AMBER, lambda ax, x, y: bird(ax, x, y, 0.062, AMBER, 2.0)),
      ("有毛之蟲", "麒麟", TIGER, lambda ax, x, y: deer(ax, x, y - 0.012, 0.062, TIGER, 2.0)),
      ("有甲之蟲", "神龜", BLUE,  lambda ax, x, y: turtle(ax, x, y - 0.012, 0.075, BLUE, 2.0, snake=False)),
      ("有鱗之蟲", "蛟龍", GREEN, lambda ax, x, y: dragon(ax, x, y, 0.05, GREEN, 2.0)),
      ("倮之蟲",   "聖人", PURPLE, lambda ax, x, y: human(ax, x, y, 0.06, PURPLE, 2.0))]
WU_Y = [0.53, 0.34, 0.15, -0.04, -0.23]


def wu_title(ax):
    title(ax, "五蟲說", "《大戴禮記・易本命》：動物分五類，每類有一個「長」")
    footer(ax, "原文每一類都是「三百六十」", y=-0.92)


def wu_head(ax):
    T(ax, -0.62, 0.69, "類", 22, WHITE, alpha=.6)
    T(ax, 0.48, 0.69, "之長", 22, WHITE, alpha=.6)
    ax.plot([-0.86, 0.86], [0.635, 0.635], c=WHITE, lw=1.2, alpha=.3)


def wu_row(i):
    cat, lead, c, fn = WU[i]
    y = WU_Y[i]
    hi = (i == 4)

    def f(ax):
        ax.add_patch(FancyBboxPatch((-0.86, y - 0.075), 1.72, 0.15, boxstyle="round,pad=0,rounding_size=0.02",
                                    fc=c, ec=AMBER if hi else "none", lw=3.0 if hi else 0, alpha=.13 if not hi else .20))
        if hi:
            ax.add_patch(FancyBboxPatch((-0.86, y - 0.075), 1.72, 0.15, boxstyle="round,pad=0,rounding_size=0.02",
                                        fill=False, ec=AMBER, lw=3.0))
        T(ax, -0.80, y, cat, 30, WHITE, ha="left")
        fn(ax, 0.20, y)
        T(ax, 0.50, y, lead, 32, c, ha="left")
        T(ax, 0.86 - 0.02, y, "長", 22, WHITE, ha="right", alpha=.55)
    return f


def wu_end(ax):
    T(ax, 0, -0.44, "倮＝沒有羽毛，也沒有鱗甲", 30, WHITE)
    T(ax, 0, -0.57, "「倮之蟲三百六十，而聖人為之長」", 26, AMBER)
    T(ax, 0, -0.68, "——倮蟲之長，就是人", 24, WHITE, alpha=.8)


# ══════════════════════════════════════════════════════════════
# 3. 四象 × 五蟲之長：對上三格、對不上兩格
# ══════════════════════════════════════════════════════════════
CMP = [("青龍", GREEN, "蛟龍", GREEN, True, None),
       ("朱雀", AMBER, "鳳皇", AMBER, True, None),
       ("玄武", BLUE, "神龜", BLUE, True, None),
       ("白虎", TIGER, "麒麟", TIGER, False, "毛蟲之長是麒麟，不是虎"),
       ("", WHITE, "聖人", PURPLE, False, "四象沒有這一格")]
CY = [0.47, 0.27, 0.07, -0.15, -0.37]
CXL, CXR, CR = -0.46, 0.46, 0.085


def cmp_title(ax):
    title(ax, "兩張名單，對不上兩格", "四象 × 五蟲之長")
    footer(ax, "※ 四象與五蟲是不同來源的分類，此圖為對照示意", y=-0.90)


def cmp_head(ax):
    T(ax, CXL, 0.64, "四象", 28, WHITE)
    T(ax, CXR, 0.64, "五蟲之長", 28, WHITE)


def cmp_items(ax):
    for (l, cl, r, cr, ok, _), y in zip(CMP, CY):
        if l:
            ax.add_patch(Circle((CXL, y), CR, fc=cl, ec=cl, lw=2.4, alpha=.22))
            ax.add_patch(Circle((CXL, y), CR, fill=False, ec=cl, lw=2.4))
            T(ax, CXL, y, l, 26, WHITE)
        else:
            ax.add_patch(Circle((CXL, y), CR, fill=False, ec=WHITE, lw=2.2, ls=(0, (5, 4)), alpha=.6))
            T(ax, CXL, y, "無", 24, WHITE, alpha=.55)
        ax.add_patch(Circle((CXR, y), CR, fc=cr, ec=cr, lw=2.4, alpha=.22))
        ax.add_patch(Circle((CXR, y), CR, fill=False, ec=cr, lw=2.4))
        T(ax, CXR, y, r, 26, WHITE)


def cmp_links_ok(ax):
    for (l, cl, r, cr, ok, _), y in zip(CMP, CY):
        if ok:
            ax.plot([CXL + CR + 0.02, CXR - CR - 0.02], [y, y], c=WHITE, lw=2.4, alpha=.7)
            T(ax, 0, y + 0.045, "對得上", 22, WHITE, alpha=.6)


def cmp_links_bad(ax):
    for (l, cl, r, cr, ok, lab), y in zip(CMP, CY):
        if not ok:
            ax.plot([CXL + CR + 0.02, CXR - CR - 0.02], [y, y], c=AMBER, lw=2.6, ls=(0, (7, 5)))
            T(ax, 0, y + 0.05, lab, 22, AMBER)
    T(ax, 0, -0.62, "白虎不在名單裡，多出來的是「人」", 28, AMBER)


# ══════════════════════════════════════════════════════════════
# 4. 曾侯乙墓漆箱・箱蓋（E.66，戰國早期，約前 433 年）
#    宿名以今名示意；東宮七宿靠青龍一側、西宮七宿靠白虎一側
# ══════════════════════════════════════════════════════════════
XIU = list("角亢氐房心尾箕") + list("斗牛女虛危室壁") + list("奎婁胃昴畢觜參") + list("井鬼柳星張翼軫")
LC, LA, LB = (0.0, 0.04), 0.50, 0.36


def lid_title(ax):
    title(ax, "曾侯乙墓漆箱・箱蓋", "戰國早期・約公元前 433 年・湖北隨州擂鼓墩", 36)
    footer(ax, "示意圖・宿名以今名標示（原器多為古寫）", y=-0.92)


def lid_box(ax):
    ax.add_patch(FancyBboxPatch((-0.90, -0.46), 1.80, 1.02, boxstyle="round,pad=0,rounding_size=0.06",
                                fc="#0A0606", ec="none", alpha=.85))
    ax.add_patch(FancyBboxPatch((-0.90, -0.46), 1.80, 1.02, boxstyle="round,pad=0,rounding_size=0.06",
                                fill=False, ec=AMBER, lw=2.2, alpha=.55))
    T(ax, -0.86, 0.50, "箱蓋", 22, WHITE, ha="left", alpha=.55)


def lid_ring(ax):
    ax.add_patch(Ellipse(LC, 2*LA - 0.14, 2*LB - 0.14, fill=False, ec=WHITE, lw=1.2, alpha=.25))
    for i, ch in enumerate(XIU):
        # 東宮（角…箕）在右側，往上經北宮（頂）、西宮（左）、南宮（底）回到東
        deg = -40.5 + i * (360 / 28)
        x = LC[0] + LA*math.cos(math.radians(deg)); y = LC[1] + LB*math.sin(math.radians(deg))
        T(ax, x, y, ch, 24, WHITE, alpha=.92)


def lid_dou(ax):
    T(ax, LC[0], LC[1] + 0.005, "斗", 84, AMBER)


def lid_beasts(ax):
    dragon(ax, 0.73, 0.04, 0.12, GREEN, 2.6, rot=90)
    tiger(ax, -0.74, 0.03, 0.115, TIGER, 2.6, rot=-90, flip=True)
    T(ax, 0.73, -0.34, "青龍", 26, GREEN)
    T(ax, -0.74, -0.34, "白虎", 26, TIGER)


def lid_end(ax):
    T(ax, 0, -0.60, "目前所見最早的二十八宿全名", 30, AMBER)
    T(ax, 0, -0.72, "蓋上的神獸只有兩隻：青龍、白虎", 24, WHITE, alpha=.85)


# ══════════════════════════════════════════════════════════════
# 5. 側面判讀：北方那一面，兩種讀法（並列、不下定論）
# ══════════════════════════════════════════════════════════════
PX1, PX2, PW, PY0, PY1 = -0.46, 0.46, 0.76, -0.24, 0.30


def side_title(ax):
    title(ax, "那北方呢？", "箱子側面：同一面，兩種讀法", 36)
    footer(ax, "※ 側面圖案的辨識各家不一，本集並列兩說", y=-0.90)


def side_frames(ax):
    for cx, lab in [(PX1, "讀法一"), (PX2, "讀法二")]:
        ax.add_patch(Rectangle((cx - PW/2, PY0), PW, PY1 - PY0, fill=False, ec=WHITE, lw=1.8, alpha=.45))
        T(ax, cx, PY1 + 0.11, lab, 28, WHITE)
        T(ax, cx - PW/2 + 0.02, PY1 - 0.045, "北面", 22, WHITE, ha="left", alpha=.55)
    ax.plot([0, 0], [PY0 - 0.30, PY1 + 0.16], c=WHITE, lw=1.2, alpha=.25)


def side_read1(ax):
    ax.add_patch(Rectangle((PX1 - PW/2 + 0.025, PY0 + 0.025), PW - 0.05, PY1 - PY0 - 0.10,
                           fc="#020306", ec=BLUE, lw=2.0, alpha=1.0))
    T(ax, PX1, -0.38, "整面塗黑", 28, BLUE)
    T(ax, PX1, -0.48, "黑色主北 → 玄武", 24, WHITE, alpha=.9)


def side_read2(ax):
    deer(ax, PX2 - 0.20, 0.00, 0.105, TIGER, 2.2, horn="one")
    deer(ax, PX2 + 0.20, 0.00, 0.105, TIGER, 2.2, horn="one", flip=True)
    for yy, r in [(0.15, 0.022), (0.03, 0.018), (-0.09, 0.018)]:
        ax.add_patch(Circle((PX2, yy), r, fc=AMBER, ec="none"))
        ax.add_patch(Circle((PX2, yy), r*2.4, fc=AMBER, ec="none", alpha=.18))
    T(ax, PX2, -0.38, "兩獸相對，中夾三星", 28, AMBER)
    T(ax, PX2, -0.48, "社團簡報：讀作麒麟", 24, WHITE, alpha=.9)
    T(ax, PX2, -0.57, "三星一般讀作危宿", 22, WHITE, alpha=.6)


# ══════════════════════════════════════════════════════════════
# 6. 民族來源（社團考據觀點）：四方 × 族群；北方另一說＝東胡的麒麟／神鹿
# ══════════════════════════════════════════════════════════════
def eth_title(ax):
    title(ax, "四方，四個族群？", "師大天文社的考據觀點", 36)
    footer(ax, "※ 族群對應為社團考據觀點，學界尚無定論", y=-0.88)


def eth_labels(ax):
    for k, (a, nm, c, fn, eth) in SECT.items():
        if k in "東西":
            x0, y0 = _pol(0.38, a)
            T(ax, x0, y0 - 0.07, eth, 26, WHITE, alpha=.9)
        else:
            T(ax, *_pol(0.45, a), eth, 26, WHITE, alpha=.9)
    wheel_center_human("中土・人")(ax)


def eth_donghu(ax):
    cx, cy = _pol(0.38, 90)
    ax.add_patch(Ellipse((cx, cy), 0.42, 0.30, fill=False, ec=AMBER, lw=2.6, ls=(0, (6, 4))))
    arrow(ax, (0.47, 0.49), (0.19, 0.42), AMBER, 2.6, .95, style="-|>,head_width=0.35,head_length=0.7")
    deer(ax, 0.70, 0.66, 0.075, AMBER, 2.2, horn="antler", flip=True)
    T(ax, 0.70, 0.52, "或：麒麟／神鹿", 26, AMBER)
    T(ax, 0.70, 0.43, "來自東胡", 24, WHITE)


# ══════════════════════════════════════════════════════════════
# 7. 《考工記》車上的五面旗：四面是動物，第五面是弓
# ══════════════════════════════════════════════════════════════
QI = [("龍旂九斿", "以象大火也", "東・心宿", GREEN, 9),
      ("鳥旟七斿", "以象鶉火也", "南・柳星張", AMBER, 7),
      ("熊旗六斿", "以象伐也", "西・參宿", TIGER, 6),
      ("龜蛇四斿", "以象營室也", "北・室宿", BLUE, 4),
      ("弧旌枉矢", "以象弧也", "弧矢", PURPLE, 0)]
QY = [0.52, 0.33, 0.14, -0.05, -0.26]


def qi_title(ax):
    title(ax, "車上的五面旗", "《周禮・考工記・輈人》")
    footer(ax, "原文照引；方位與星宿為後世對應", y=-0.90)


def qi_row(i):
    nm, q, note, c, n = QI[i]
    y = QY[i]

    def f(ax):
        if n:
            flag(ax, -0.80, y - 0.005, 0.075, c, n, 2.0)
        else:
            ax.add_patch(FancyBboxPatch((-0.90, y - 0.085), 1.80, 0.17, boxstyle="round,pad=0,rounding_size=0.02",
                                        fc=PURPLE, ec=AMBER, lw=3.0, alpha=.18))
            ax.add_patch(FancyBboxPatch((-0.90, y - 0.085), 1.80, 0.17, boxstyle="round,pad=0,rounding_size=0.02",
                                        fill=False, ec=AMBER, lw=3.0))
            bow(ax, -0.79, y, 0.075, PURPLE, 2.4)
        T(ax, -0.66, y, nm, 30, c, ha="left")
        T(ax, -0.04, y, q, 28, WHITE, ha="left")
        T(ax, 0.86, y, note, 22, WHITE, ha="right", alpha=.65)
    return f


def qi_end(ax):
    T(ax, 0, -0.50, "四面是動物，第五面是人做的弓", 30, AMBER)


# ══════════════════════════════════════════════════════════════
# 8. 星圖（gen_ep_assets 星表＋投影；本檔畫標籤）
# ══════════════════════════════════════════════════════════════
XY_CHAIN = [44248, 44700, 45688, 45860, 47617, 47701, 46146, 46750, 47908, 48455,
            50335, 50583, 49583, 49669, 47508, 51624, 49637]          # 軒轅十七星（依連線順序編號）
HS_STARS = [34444, 35904, 37819, 38901, 38070, 37229, 33579, 32759, 35264]  # 弧矢九星
SIRIUS = 32349
VEGA, ALTAIR, DENEB = 91262, 97649, 102098

SKY = {
    "軒轅": {"episode": "C-03", "outdir": "05_素材/C-03_麒麟與倮獸/軒轅十七星", "prefix": "軒轅",
             "field": {"center": [146.5, 25.0], "radius": 24, "maglim": 5.8},
             "layers": [{"type": "stars", "mains": XY_CHAIN},
                        {"type": "lines", "name": "軒轅", "source": {"culture": "chinese", "names": ["轩辕"]}},
                        {"type": "lines", "name": "獅子座", "source": {"culture": "western", "iau": "Leo"}}]},
    "牛女": {"episode": "C-03", "outdir": "05_素材/C-03_麒麟與倮獸/牛郎織女", "prefix": "牛郎織女",
             "field": {"center": [295.0, 30.0], "radius": 28, "maglim": 5.5},
             "layers": [{"type": "stars", "mains": [VEGA, ALTAIR, DENEB, 98036, 97278, 91919, 91971]},
                        {"type": "lines", "name": "河鼓", "source": {"culture": "chinese", "names": ["河鼓"]}},
                        {"type": "lines", "name": "織女", "source": {"culture": "chinese", "names": ["织女"]}}]},
    "弧矢": {"episode": "C-03", "outdir": "05_素材/C-03_麒麟與倮獸/弧矢九星", "prefix": "弧矢",
             "field": {"center": [110.0, -27.0], "radius": 17, "maglim": 5.8},
             "layers": [{"type": "stars", "mains": HS_STARS + [SIRIUS]},
                        {"type": "lines", "name": "弧矢", "source": {"culture": "chinese", "names": ["弧矢"]}}]},
}
_ENG = {}


def eng(k):
    if k not in _ENG:
        _ENG[k] = Gx.Engine(BASE, SKY[k])
    return _ENG[k]


def P(e, h):
    x, y = Gx.stereo(*e.S[h][:2], e.ra0, e.dec0)
    return x / e.lim, y / e.lim


def sky_fig(e, dark=False):
    f, ax = e.fig(dark=dark)
    ax2 = f.add_axes([0, 0, 1, 1]); ax2.set_xlim(-1, 1); ax2.set_ylim(-1, 1)
    ax2.set_aspect("equal"); ax2.axis("off"); ax2.patch.set_alpha(0)
    return f, ax, ax2


def emit_sky(e, sub, prefix, layers, previews):
    for nm, fn in layers:
        f, ax, ax2 = sky_fig(e); fn(e, ax, ax2)
        save(f, sub, f"{prefix}_{nm}層_透明.png")
    d = dict(layers)
    for pv, names in previews:
        f, ax, ax2 = sky_fig(e, dark=True)
        for n in names: d[n](e, ax, ax2)
        save(f, sub, f"{prefix}_預覽_{pv}_黑底.png", transparent=False)


def stars_layer(mains, min_size=46):
    def f(e, ax, ax2):
        e.d_stars(ax, mains)
        for h in mains:                       # 暗的成員星（>5.5 等）給最小點徑，才數得到
            if h in e.S and e.S[h][2] > 5.0:
                x, y = Gx.stereo(*e.S[h][:2], e.ra0, e.dec0)
                ax.scatter([x], [y], s=min_size, c=WHITE, lw=0, zorder=4)
                ax.scatter([x], [y], s=min_size*4, c=WHITE, alpha=.15, lw=0, zorder=3)
    return f


def lines_layer(group, color, lw=3.2, ls="-"):
    def f(e, ax, ax2):
        for segs in e.line_groups[group].values():
            for seg in segs:
                pts = [Gx.stereo(*e.S[h][:2], e.ra0, e.dec0) for h in seg if h in e.S]
                ax.plot([p[0] for p in pts], [p[1] for p in pts], c=color, lw=lw, ls=ls,
                        solid_capstyle="round", alpha=.95, zorder=5)
    return f


def mw_layer(e, ax, ax2):
    e.d_mw(ax)


def cap(fn):
    """純文字／示意層：畫在 ax2（−1..1 座標）"""
    return lambda e, ax, ax2: fn(ax2)


# —— 軒轅 ——
def xy_title(ax):
    title(ax, "候選一：軒轅", "「軒轅，黃龍體」《史記・天官書》", 36)


def xy_name(e, ax, ax2):
    T(ax2, 0.60, 0.16, "軒轅", 34, PURPLE)
    T(ax2, 0.60, 0.06, "十七顆星", 24, WHITE, alpha=.85)
    x, y = P(e, 49669)                         # 軒轅十四＝編號 14
    ax2.plot([x + 0.04, 0.16], [y + 0.01, -0.39], c=WHITE, lw=1.4, alpha=.5)
    T(ax2, 0.30, -0.38, "軒轅十四", 26, WHITE)
    T(ax2, 0.30, -0.465, "（獅子座 α）", 22, WHITE, alpha=.75)


def xy_numbers(e, ax, ax2):
    pos = {h: np.array(P(e, h)) for h in XY_CHAIN}
    nb = {h: set() for h in XY_CHAIN}
    for segs in e.line_groups["軒轅"].values():
        for seg in segs:
            for a, b in zip(seg, seg[1:]):
                nb[a].add(b); nb[b].add(a)
    for i, h in enumerate(XY_CHAIN, 1):
        p = pos[h]
        m = np.mean([pos[n] for n in nb[h]], axis=0) if nb[h] else p + (0, -1)
        d = p - m
        if np.hypot(*d) < 1e-3: d = np.array([1.0, 0.0])
        d = d / np.hypot(*d)
        q = p + d * 0.062
        ax2.add_patch(Circle(q, 0.030, fc=BG, ec=AMBER, lw=1.6, alpha=.95, zorder=8))
        ax2.text(q[0], q[1] - 0.002, str(i), fontproperties=C.FP, fontsize=22 if i < 10 else 20,
                 color=AMBER, ha="center", va="center", weight="bold", zorder=9)


def xy_end(ax):
    T(ax, 0, -0.86, "線索：黃帝號軒轅；《月令》的中央之帝，正是黃帝", 22, WHITE, alpha=.85)


# —— 牛郎織女 ——
def nn_title(ax):
    title(ax, "候選二：牛郎織女", "天上少數有「人」的故事", 36)


def nn_names(e, ax, ax2):
    x, y = P(e, VEGA); T(ax2, x + 0.02, y + 0.10, "織女星", 30, AMBER)
    x, y = P(e, ALTAIR); T(ax2, x + 0.30, y, "牛郎星", 30, AMBER)
    T(ax2, x + 0.30, y - 0.085, "（河鼓二）", 22, WHITE, alpha=.75)


def nn_deer(e, ax, ax2):
    pts = [P(e, h) for h in (VEGA, ALTAIR, DENEB, VEGA)]
    ax2.plot([p[0] for p in pts], [p[1] for p in pts], c=GREEN, lw=2.6, ls=(0, (7, 5)), zorder=6)
    x, y = P(e, DENEB); T(ax2, x - 0.02, y + 0.10, "天津四", 28, GREEN)
    cx = np.mean([p[0] for p in pts[:3]]); cy = np.mean([p[1] for p in pts[:3]])
    T(ax2, cx, cy + 0.02, "蒙古：三鹿", 28, GREEN)
    T(ax2, cx, cy - 0.07, "（A-07 蒙古篇）", 22, WHITE, alpha=.7)


# —— 弧矢 ——
def hs_title(ax):
    title(ax, "候選三：弧矢", "「弧旌枉矢，以象弧也」《考工記》", 36)


def hs_name(e, ax, ax2):
    T(ax2, -0.62, -0.42, "弧矢", 34, BLUE)
    T(ax2, -0.62, -0.52, "後世星表：九星", 22, WHITE, alpha=.75)


def hs_sirius(e, ax, ax2):
    x, y = P(e, SIRIUS)
    T(ax2, x + 0.15, y + 0.04, "天狼", 30, WHITE)


def hs_aim(e, ax, ax2):
    (x0, y0), (x1, y1) = P(e, 34444), P(e, SIRIUS)
    ax2.annotate("", xy=(x1 - (x1 - x0)*0.06, y1 - (y1 - y0)*0.06), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>,head_width=0.5,head_length=1.0", color=AMBER, lw=3.0), zorder=7)
    T(ax2, 0, -0.80, "「下有四星曰弧，直狼」", 28, AMBER)
    T(ax2, 0, -0.89, "《史記・天官書》：這把弓，對著天狼", 22, WHITE, alpha=.75)


# ══════════════════════════════════════════════════════════════
# 9. 倮獸主星：三個候選並列（明說未解）
# ══════════════════════════════════════════════════════════════
CAND = [("軒轅", PURPLE, "軒轅", ["黃帝號軒轅", "十七顆星"]),
        ("牛郎織女", AMBER, "牛女", ["天上的「人」", "蒙古三鹿之二"]),
        ("弧矢", BLUE, "弧矢", ["第五面旗：弓", "直指天狼"])]
CBX, CBW, CBY0, CBY1 = [-0.60, 0.0, 0.60], 0.54, -0.46, 0.50


def cand_title(ax):
    title(ax, "倮獸的星，是哪一組？", "社團列出的三個候選", 36)
    footer(ax, "※ 候選與線索為社團考據與本集整理，非古籍明文", y=-0.92)


def _mini(ax, k, cx, cy, w, h, c):
    e = eng(k)
    if k == "軒轅":
        hs = XY_CHAIN; segs = [s for v in e.line_groups["軒轅"].values() for s in v]
    elif k == "牛女":
        hs = [VEGA, ALTAIR, DENEB]; segs = [[VEGA, ALTAIR], [ALTAIR, DENEB], [DENEB, VEGA]]
    else:
        hs = HS_STARS + [SIRIUS]; segs = [s for v in e.line_groups["弧矢"].values() for s in v] + [[34444, SIRIUS]]
    pts = {h: np.array(P(e, h)) for h in hs}
    xs = [p[0] for p in pts.values()]; ys = [p[1] for p in pts.values()]
    sc = min(w / (max(xs) - min(xs)), h / (max(ys) - min(ys)))
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    tr = lambda p: (cx + (p[0] - mx)*sc, cy + (p[1] - my)*sc)
    for s in segs:
        q = [tr(pts[h]) for h in s if h in pts]
        dash = (k == "牛女") or (s == [34444, SIRIUS])
        ax.plot([a[0] for a in q], [a[1] for a in q], c=c if not (k == "弧矢" and s == [34444, SIRIUS]) else AMBER,
                lw=2.2, alpha=.85, ls=(0, (5, 4)) if dash else "-")
    for h, p in pts.items():
        r = 0.016 if (h in (VEGA, ALTAIR, DENEB, SIRIUS, 49669)) else 0.010
        ax.add_patch(Circle(tr(p), r, fc=WHITE, ec="none", zorder=7))


def cand_boxes(ax):
    for cx, (nm, c, k, clues) in zip(CBX, CAND):
        ax.add_patch(FancyBboxPatch((cx - CBW/2, CBY0), CBW, CBY1 - CBY0, boxstyle="round,pad=0,rounding_size=0.03",
                                    fc=c, ec="none", alpha=.10))
        ax.add_patch(FancyBboxPatch((cx - CBW/2, CBY0), CBW, CBY1 - CBY0, boxstyle="round,pad=0,rounding_size=0.03",
                                    fill=False, ec=c, lw=2.4, alpha=.85))
        T(ax, cx, 0.40, nm, 30 if len(nm) < 4 else 28, c)
        _mini(ax, k, cx, 0.13, 0.38, 0.30, c)
        for j, s in enumerate(clues):
            T(ax, cx, -0.13 - 0.085*j, s, 22, WHITE, alpha=.9)


def cand_q(ax):
    for cx, (nm, c, k, clues) in zip(CBX, CAND):
        T(ax, cx, -0.36, "？", 44, AMBER)


def cand_end(ax):
    T(ax, 0, -0.62, "這一題，還沒有答案", 34, WHITE)
    T(ax, 0, -0.74, "沒有傳世文獻明說：中央倮獸對應哪一組星官", 22, WHITE, alpha=.8)


# ══════════════════════════════════════════════════════════════
# 10. 9:16 圖卡
# ══════════════════════════════════════════════════════════════
def card():
    f, ax = newcard()

    def t(x, y, s, size=13, c=WHITE, ha="center", w="bold", a=1.0):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=c, ha=ha, va="center", weight=w, alpha=a)

    def rule(y): ax.plot([0.06, 0.94], [y, y], c=WHITE, lw=1.0, alpha=.3)
    t(0.5, 0.945, "麒麟與倮獸：消失的第五象", 22)
    t(0.5, 0.905, "四象排完，中間那一格是誰？", 12, a=.7)
    rule(0.88)
    t(0.5, 0.855, "四象", 15, WHITE)
    t(0.5, 0.822, "東青龍・南朱雀・西白虎・北玄武　中央：空", 11.5, WHITE, w="normal", a=.9)
    rule(0.795)
    t(0.5, 0.77, "五蟲說《大戴禮記・易本命》", 15, AMBER)
    for i, (cat, lead, c, _) in enumerate(WU):
        y = 0.735 - 0.03*i
        t(0.30, y, cat, 12, WHITE, "left", "normal", .9); t(0.62, y, lead, 13, c, "left")
    t(0.5, 0.57, "《禮記・月令》「中央土……其帝黃帝……其蟲倮」", 11.5, WHITE, w="normal", a=.9)
    rule(0.545)
    t(0.5, 0.52, "曾侯乙墓漆箱（約前 433 年）", 15, GREEN)
    t(0.5, 0.488, "蓋：「斗」＋二十八宿全名＋青龍、白虎", 11.5, WHITE, w="normal", a=.9)
    t(0.5, 0.46, "北面：整面塗黑（玄武）？兩獸相對（麒麟）？", 11.5, WHITE, w="normal", a=.9)
    rule(0.435)
    t(0.5, 0.41, "《考工記》五面旗", 15, PURPLE)
    t(0.5, 0.378, "龍・鳥・熊・龜蛇……第五面：弧旌枉矢", 11.5, WHITE, w="normal", a=.9)
    rule(0.352)
    t(0.5, 0.325, "倮獸的星：三個候選", 15, WHITE)
    for i, (nm, c, k, clues) in enumerate(CAND):
        y = 0.29 - 0.032*i
        t(0.22, y, nm, 13, c, "left"); t(0.50, y, "・".join(clues), 11, WHITE, "left", "normal", .85)
    t(0.5, 0.17, "這一題，還沒有答案", 16, AMBER)
    t(0.5, 0.13, "族群對應與三候選為社團考據觀點，學界尚無定論", 10, WHITE, w="normal", a=.6)
    t(0.5, 0.035, "萬國星空 C-03・師大天文社", 10.5, WHITE, w="normal", a=.5)
    save(f, "_圖卡", "麒麟與倮獸_圖卡_黑底.png", transparent=False)


def preview(sub, name, fns):
    f, ax = newfig(dark=True)
    for fn in fns: fn(ax)
    save(f, sub, name, transparent=False)


if __name__ == "__main__":
    print("── 四象盤 ──")
    ring = [("題辭_四象", four_title), ("外圈", wheel_ring)] + \
           [(f"{SECT[k][1]}", wheel_sector(k)) for k in ("東", "南", "西", "北")] + \
           [("中央留空", wheel_center_empty), ("題辭_中央", center_title),
            ("中央倮獸", wheel_center_human()), ("月令", yueling)]
    emit("四象與五象", ring, title="四象盤",
         preview_layers=["題辭_四象", "外圈", "青龍", "朱雀", "白虎", "玄武", "中央留空"])
    preview("四象與五象", "四象盤_預覽_中央倮獸_黑底.png",
            [center_title, wheel_ring] + [wheel_sector(k) for k in ("東", "南", "西", "北")] +
            [wheel_center_human(), yueling])

    print("── 五蟲說 ──")
    emit("五蟲說", [("題辭", wu_title), ("表頭", wu_head)] + [(f"列{i+1}", wu_row(i)) for i in range(5)] +
         [("結語", wu_end)], title="五蟲說")

    print("── 四象五蟲對照 ──")
    emit("四象五蟲對照", [("題辭", cmp_title), ("欄位", cmp_head), ("項目", cmp_items),
                          ("對得上", cmp_links_ok), ("對不上", cmp_links_bad)], title="對照")

    print("── 曾侯乙漆箱 ──")
    emit("曾侯乙漆箱", [("題辭", lid_title), ("箱蓋", lid_box), ("宿環", lid_ring), ("斗字", lid_dou),
                        ("龍虎", lid_beasts), ("結語", lid_end)], title="漆箱蓋面")

    print("── 側面判讀 ──")
    emit("側面判讀", [("題辭", side_title), ("外框", side_frames), ("讀法一", side_read1),
                      ("讀法二", side_read2)], title="側面判讀")

    print("── 民族來源 ──")
    emit("民族來源", [("題辭", eth_title), ("外圈", wheel_ring)] +
         [(f"{SECT[k][1]}", wheel_sector(k, glyph=False, direction=False)) for k in ("東", "南", "西", "北")] +
         [("族群", eth_labels), ("東胡", eth_donghu)], title="民族來源")

    print("── 考工記五旗 ──")
    emit("考工記五旗", [("題辭", qi_title)] + [(f"旗{i+1}", qi_row(i)) for i in range(5)] + [("結語", qi_end)],
         title="五旗")

    print("── 星圖：軒轅 ──")
    e = eng("軒轅")
    emit_sky(e, "軒轅十七星", "軒轅",
             [("題辭", cap(xy_title)), ("星點", stars_layer(XY_CHAIN)), ("連線", lines_layer("軒轅", PURPLE)),
              ("獅子座", lines_layer("獅子座", BLUE, 2.0, (0, (6, 5)))), ("名稱", xy_name),
              ("編號", xy_numbers), ("線索", cap(xy_end))],
             [("軒轅", ["題辭", "星點", "連線", "名稱"]), ("編號", ["題辭", "星點", "連線", "名稱", "編號", "線索"])])

    print("── 星圖：牛郎織女 ──")
    e = eng("牛女")
    emit_sky(e, "牛郎織女", "牛郎織女",
             [("題辭", cap(nn_title)), ("星點", stars_layer([VEGA, ALTAIR, DENEB, 98036, 97278, 91919, 91971])),
              ("銀河", mw_layer), ("連線", lambda e, ax, ax2: (lines_layer("河鼓", AMBER, 2.6)(e, ax, ax2),
                                                               lines_layer("織女", AMBER, 2.6)(e, ax, ax2))),
              ("名稱", nn_names), ("三鹿", nn_deer)],
             [("牛郎織女", ["題辭", "星點", "銀河", "連線", "名稱"]),
              ("三鹿", ["題辭", "星點", "銀河", "連線", "名稱", "三鹿"])])

    print("── 星圖：弧矢 ──")
    e = eng("弧矢")
    emit_sky(e, "弧矢九星", "弧矢",
             [("題辭", cap(hs_title)), ("星點", stars_layer(HS_STARS + [SIRIUS])), ("銀河", mw_layer),
              ("連線", lines_layer("弧矢", BLUE)), ("名稱", hs_name), ("天狼", hs_sirius), ("直狼", hs_aim)],
             [("弧矢", ["題辭", "星點", "銀河", "連線", "名稱", "天狼"]),
              ("直狼", ["題辭", "星點", "銀河", "連線", "名稱", "天狼", "直狼"])])

    print("── 倮獸主星候選 ──")
    emit("倮獸主星候選", [("題辭", cand_title), ("方框", cand_boxes), ("問號", cand_q), ("結語", cand_end)],
         title="候選")

    print("── 圖卡 ──")
    card()
    print("all done")
