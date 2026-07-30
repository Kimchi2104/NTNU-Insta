# -*- coding: utf-8 -*-
"""萬國星空 C 系列（學術番外）概念圖共用骨架
與星圖素材同規格：2052px 方形、透明 PNG 分層＋黑底預覽、同一組色票。
各集只需 import 此模組，定義各自的繪圖函式，再用 emit() 批次輸出。
"""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc, Rectangle, FancyBboxPatch
from matplotlib.font_manager import FontProperties, fontManager

# ── 全案統一色票（與星圖引擎一致）──
AMBER, BLUE, WHITE = "#FFC94A", "#6FA8FF", "#FFFFFF"
GREEN, PURPLE      = "#7BD88F", "#B78AFF"
MW, BG             = "#C9DAF5", "#0B0F1E"
CANVAS, DPI        = 10.8, 190          # 10.8in × 190dpi = 2052px
CARD_W, CARD_H, CARD_DPI = 6.075, 10.8, 200   # 9:16 圖卡 1215×2160

_BASE = None
def set_base(path):
    """設定本集素材輸出根目錄"""
    global _BASE; _BASE = path

def font():
    """CJK ＋ DejaVu fallback（梵文變音、阿拉伯文等）"""
    fams = []
    for f in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            fontManager.addfont(f); fams.append(FontProperties(fname=f).get_name())
    fams.append("DejaVu Sans")
    return FontProperties(family=fams)
FP = font()

def newfig(lim=1.0, dark=False):
    f = plt.figure(figsize=(CANVAS, CANVAS), dpi=DPI)
    ax = f.add_axes([0,0,1,1]); ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_aspect("equal"); ax.axis("off")
    if dark: f.patch.set_facecolor(BG)
    else: f.patch.set_alpha(0); ax.patch.set_alpha(0)
    return f, ax

def newcard(dark=True):
    """9:16 直式圖卡（輪播用）"""
    f = plt.figure(figsize=(CARD_W, CARD_H), dpi=CARD_DPI)
    ax = f.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    if dark: f.patch.set_facecolor(BG)
    else: f.patch.set_alpha(0); ax.patch.set_alpha(0)
    return f, ax

def save(f, sub, name, transparent=True):
    d = os.path.join(_BASE, sub); os.makedirs(d, exist_ok=True)
    f.savefig(os.path.join(d, name), transparent=transparent); plt.close(f)
    print("  ✓", sub + "/" + name)

def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12):
    """文字預設置於高 zorder，避免被後畫的不透明色塊蓋住"""
    ax.text(x, y, s, fontproperties=FP, fontsize=size, color=c, ha=ha,
            va="center", weight=w, alpha=alpha, zorder=z)

def arrow(ax, xy, xytext, c=WHITE, lw=2.0, alpha=.7, style="->"):
    ax.annotate("", xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle=style, color=c, lw=lw, alpha=alpha))

def emit(sub, layers, preview_name="預覽", preview_layers=None, lim=1.0, title=None):
    """批次輸出：每個圖層一張透明 PNG＋一張黑底合成預覽
    layers: [(檔名標籤, 繪圖函式), ...]
    preview_layers: 預覽要疊哪些（預設全部）
    """
    for nm, fn in layers:
        f, ax = newfig(lim); fn(ax); save(f, sub, f"{title or sub}_{nm}層_透明.png")
    f, ax = newfig(lim, dark=True)
    for nm, fn in layers:
        if preview_layers is None or nm in preview_layers: fn(ax)
    save(f, sub, f"{title or sub}_{preview_name}_黑底.png", transparent=False)

def emit_frames(sub, name, make_fn, n, lim=1.0):
    """逐格圖（供循環動畫）：make_fn(ax, i)"""
    for i in range(n):
        f, ax = newfig(lim); make_fn(ax, i)
        save(f, sub, f"{name}_格{i+1}_透明.png")

# ── 常用元件 ──
def human_figure(ax, x=0, y=0, s=1.0, c=WHITE, alpha=1.0, seated=False):
    """簡化人形側影（坐姿／站姿）"""
    hd = Circle((x, y+0.30*s), 0.075*s, fc=c, ec="none", alpha=alpha); ax.add_patch(hd)
    ax.plot([x, x],[y+0.225*s, y-0.02*s], c=c, lw=5.0*s, alpha=alpha,
            solid_capstyle="round")
    if seated:
        ax.plot([x, x+0.16*s],[y-0.02*s, y-0.02*s], c=c, lw=4.5*s, alpha=alpha,
                solid_capstyle="round")
        ax.plot([x+0.16*s, x+0.16*s],[y-0.02*s, y-0.20*s], c=c, lw=4.5*s, alpha=alpha,
                solid_capstyle="round")
        ax.plot([x, x+0.14*s],[y+0.16*s, y+0.08*s], c=c, lw=3.5*s, alpha=alpha,
                solid_capstyle="round")
    else:
        for dx in (-0.10*s, 0.10*s):
            ax.plot([x, x+dx],[y-0.02*s, y-0.28*s], c=c, lw=4.0*s, alpha=alpha,
                    solid_capstyle="round")
            ax.plot([x, x+dx*1.3],[y+0.18*s, y+0.02*s], c=c, lw=3.2*s, alpha=alpha,
                    solid_capstyle="round")

def water(ax, y=0.0, x0=-0.95, x1=0.95, c=BLUE, rows=3, amp=0.020, freq=22, phase=0.0):
    """水波（多列，供動畫錯位）"""
    xs = [x0 + (x1-x0)*i/240 for i in range(241)]
    for k in range(rows):
        ax.plot(xs, [y - k*0.045 + amp*math.sin(x*freq + phase + k*1.5) for x in xs],
                c=c, lw=2.4-0.6*k, alpha=.75-0.18*k)

def timeline(ax, events, y=0.0, c=WHITE):
    """時間軸：events = [(x位置 0~1, 年代標籤, 事件標籤, 顏色), ...]"""
    ax.plot([-0.88, 0.88],[y, y], c=c, lw=2.0, alpha=.6)
    for px, era, ev, col in events:
        x = -0.88 + 1.76*px
        ax.scatter([x],[y], s=200, c=col, zorder=5)
        ax.plot([x, x],[y, y+0.10], c=col, lw=1.6, alpha=.6)
        T(ax, x, y+0.155, era, 16, col)
        T(ax, x, y-0.10, ev, 14, WHITE, alpha=.8)
