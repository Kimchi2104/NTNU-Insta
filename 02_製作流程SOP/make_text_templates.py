# -*- coding: utf-8 -*-
"""字幕／字卡版型的示意圖（給美宣當起始想法，不是成品）

輸出到 01_視覺與品牌/版型預覽/：中文 4 種、英文 3 種、英文版封面 1 張，全部 1080×1920。
背景＝團隊漸層（135°，#000000→#3533cd）＋示意星點＋山的剪影（位置照 canva_ops.MOUNT：山稜線上緣 Y≈1622）。
字型：Noto Serif CJK（近似品牌字筑紫Aオールド明朝）；英文沿用同一字型的拉丁字。

    python3 02_製作流程SOP/make_text_templates.py
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.font_manager import FontProperties

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "01_視覺與品牌", "版型預覽")
W, H = 1080, 1920
SAFE_TOP, SAFE_BOT = 250, 1670          # Reels 安全區（Canva逐頁文字放置規格）
GRID_TOP, GRID_BOT = 285, 1635          # IG 格狀縮圖 4:5 裁切（1080×1350 置中）
ACCENT = "#F2B134"                      # 封面填空詞的黃（照中文版）
BOX = dict(fc="#000000", ec="none", alpha=0.62)

SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FP = FontProperties(fname=SERIF)
FPB = FontProperties(fname=SERIF_B)


def pt(px):                              # dpi=100：1 pt = 100/72 px
    return px * 0.72


def canvas(stars_seed=7):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    yy, xx = np.mgrid[0:H, 0:W]
    t = np.clip((xx / W + yy / H) / 2, 0, 1)[..., None]
    c0, c1 = np.array([0, 0, 0]), np.array([0x35, 0x33, 0xcd])
    ax.imshow((c0 * (1 - t) + c1 * t).astype(np.uint8), extent=(0, W, H, 0), zorder=0)
    rng = np.random.default_rng(stars_seed)
    n = 900
    xs, ys = rng.uniform(0, W, n), rng.uniform(0, 1650, n)
    sz = rng.exponential(1.4, n) + 0.3
    ax.scatter(xs, ys, s=sz ** 2 * 1.2, c="white", alpha=0.6, lw=0, zorder=1)
    bright = rng.choice(n, 14, replace=False)
    ax.scatter(xs[bright], ys[bright], s=28, c="white", alpha=0.95, lw=0, zorder=1)
    return fig, ax


def mountain(ax):
    x = np.linspace(-20, 1100, 120)
    # 最高點 ≈ 1622（canva_ops.MOUNT 的 top），山谷比山頂低 0–140 px
    y = 1762 - 55 * np.exp(-((x - 240) / 110) ** 2) - 140 * np.exp(-((x - 700) / 150) ** 2) \
        - 60 * np.exp(-((x - 980) / 90) ** 2) + 6 * np.sin(x / 23)
    pts = [(-20, H)] + list(zip(x, y)) + [(1100, H)]
    ax.add_patch(Polygon(pts, closed=True, fc="#000000", ec="none", zorder=5))


def guides(ax, grid=False):
    for yv in (SAFE_TOP, SAFE_BOT):
        ax.plot([0, W], [yv, yv], ls=(0, (6, 6)), lw=1.2, c="white", alpha=0.35, zorder=9)
    ax.text(24, SAFE_TOP - 12, "Reels 安全區 250 px（上下）", fontproperties=FP, fontsize=pt(22),
            color="white", alpha=0.5, zorder=9)
    if grid:
        for yv in (GRID_TOP, GRID_BOT):
            ax.plot([0, W], [yv, yv], ls=(0, (2, 6)), lw=1.2, c=ACCENT, alpha=0.6, zorder=9)
        ax.text(W - 24, GRID_BOT - 14, "IG 格狀縮圖 4:5 裁切線（Y 285–1635）", fontproperties=FP,
                fontsize=pt(22), color=ACCENT, alpha=0.8, ha="right", va="bottom", zorder=9)


def box(ax, x, y, w, h, r=48, **kw):
    st = dict(BOX); st.update(kw)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", zorder=6, **st))


def text(ax, x, y, s, px, bold=False, color="white", ha="center", va="center", lh=1.3, alpha=1.0, ls=0):
    """多行文字：每行自己排（行高＝px×lh），ls＝字距（英文標題用）"""
    lines = s.split("\n")
    fp = FPB if bold else FP
    for i, ln in enumerate(lines):
        yy = y + i * px * lh
        if ls:
            ln = ls.join(ln) if isinstance(ls, str) else ln
        ax.text(x, yy, ln, fontproperties=fp, fontsize=pt(px), color=color, ha=ha, va=va, alpha=alpha, zorder=7)


def vtext(ax, x, y_top, s, px, color="white", gap=1.08):
    """直排：一列一個字，由上往下；標點換成直排用的字形"""
    s = s.translate(str.maketrans("，。：；！？", "︐︒︓︔︕︖"))
    for i, ch in enumerate(s):
        ax.text(x, y_top + i * px * gap, ch, fontproperties=FP, fontsize=pt(px), color=color,
                ha="center", va="center", zorder=7)


def label(ax, x, y, s, px=40, color="#FFC94A"):
    ax.scatter([x], [y - px * 1.1], s=70, c="white", zorder=7)
    ax.text(x, y, s, fontproperties=FP, fontsize=pt(px), color=color, ha="center", va="center", zorder=7)


def caption(ax, s):
    """頁頂說明（示意圖專用，不是成品的一部分）；可用 \\n 分兩行"""
    for i, ln in enumerate(s.split("\n")):
        ax.text(W / 2, 70 + i * 40, ln, fontproperties=FP, fontsize=pt(28), color="white", alpha=0.75,
                ha="center", zorder=9)


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name); fig.savefig(p, dpi=100); plt.close(fig); print("  ✓", p)


# ───────────────────── 中文 ─────────────────────
def zh_A():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "中-A　下方橫排（預設）：字幕框 Y 1330–1600，44 px，每行 ≤16 字")
    label(ax, 560, 760, "Manu 大鳥")
    box(ax, 60, 1340, 960, 230)
    text(ax, W / 2, 1400, "但天上最大的，是一隻鳥：Manu。\n天狼星是牠的身體，老人星是東翼，\n南河三是北翼。", 44)
    save(fig, "中-A_下方橫排.png")


def zh_B():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "中-B　上方橫排：主角在畫面下半（低空星、地平線鏡頭）時用")
    label(ax, 540, 1480, "老人星 Suhail", 40)
    box(ax, 60, 300, 960, 230)
    text(ax, W / 2, 360, "再往南，地平線上這顆亮星，\n是 Suhail，老人星；\n在阿拉伯，這是一個男人的名字。", 44)
    save(fig, "中-B_上方橫排.png")


def zh_C():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "中-C　側邊直排：明朝體的直排最有古星圖感；每列 ≤12 字，最多兩列")
    label(ax, 420, 900, "旋轉的女人")
    box(ax, 840, 420, 190, 720)
    vtext(ax, 970, 470, "對面再擺五顆，一個女人", 48)
    vtext(ax, 900, 470, "旋轉的女人，就是仙后座", 48)
    save(fig, "中-C_側邊直排.png")


def zh_D():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "中-D　字卡＋一句：字卡 72 px 在上，旁白只留關鍵一句在下")
    box(ax, 120, 330, 840, 150, r=40)
    text(ax, W / 2, 405, "旋轉的男人・旋轉的女人", 72)
    label(ax, 560, 880, "北斗 Big Dipper")   # 示意用；ǫ、ą 這類字母要另外確認字型有沒有（防豆腐）
    box(ax, 150, 1400, 780, 110, r=40)
    text(ax, W / 2, 1455, "兩個人繞著火爐轉，像一家人住在 hooghan 裡。", 40)
    save(fig, "中-D_字卡加一句.png")


# ───────────────────── 英文 ─────────────────────
def en_A():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "EN-A  Headline + line\nhook ≤ 6 words on top (bold); one sentence below, left-aligned")
    box(ax, 60, 300, 960, 280, r=40)
    text(ax, 110, 370, "One island.\nA whole sky of sails.", 84, bold=True, ha="left", lh=1.2)
    label(ax, 560, 1000, "Manu, the Bird")
    box(ax, 60, 1360, 960, 200, r=40)
    text(ax, 110, 1420, "The sky's biggest shape is a bird:\nSirius is its body, Canopus a wing.", 44, ha="left")
    save(fig, "EN-A_headline_line.png")


def en_B():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "EN-B  Lower-third\none left-aligned box; accent bar in the episode colour")
    label(ax, 620, 820, "Canopus · Suhail")
    box(ax, 60, 1380, 900, 190, r=32)
    ax.add_patch(FancyBboxPatch((60, 1380), 14, 190, boxstyle="round,pad=0,rounding_size=7",
                                fc=ACCENT, ec="none", zorder=7))
    text(ax, 120, 1440, "North of 37° latitude, Canopus never rises.\nTo the Arabs it was Suhail — a man's name.",
         44, ha="left")
    save(fig, "EN-B_lower_third.png")


def en_C():
    fig, ax = canvas(); mountain(ax); guides(ax)
    caption(ax, "EN-C  Centered caption\ntwo short lines, for pages where the stars are the point")
    label(ax, 400, 700, "Alula", 40); label(ax, 560, 900, "Tania", 40); label(ax, 740, 1080, "Talitha", 40)
    box(ax, 120, 1380, 840, 170, r=40)
    text(ax, W / 2, 1435, "Three pairs of stars under the Great Bear:\nthe hoofprints of a startled gazelle.", 44)
    save(fig, "EN-C_centered_caption.png")


def en_cover():
    fig, ax = canvas(stars_seed=3); mountain(ax); guides(ax, grid=True)
    caption(ax, "EN cover\nbackground, mountain, layout = Chinese cover; only the text changes")
    # 版本角標（右上，安全區內）
    box(ax, 820, 300, 200, 64, r=32, alpha=0.5)
    text(ax, 920, 332, "EN · EP01", 30, color=ACCENT)
    # 主標（英文在前、中文小字在後，社團英文名）
    text(ax, W / 2, 480, "World Sky Cultures", 96, bold=True)
    text(ax, W / 2, 575, "萬國星空", 40, alpha=0.85)
    text(ax, W / 2, 650, "NTNU Astronomy Club", 32, alpha=0.75)
    # 填空句（固定句型 One sky. The ◯◯ saw — ◯◯.）
    text(ax, W / 2, 920, "One sky.", 72)
    text(ax, W / 2, 1020, "The people of Anuta saw —", 60)
    text(ax, W / 2, 1140, "a great bird.", 84, bold=True, color=ACCENT)
    # 鉤子（取代中文版第二句）
    text(ax, W / 2, 1330, "An island of 0.4 km² that remembers\na whole sea of stars.", 44, alpha=0.9)
    save(fig, "EN-封面.png")


if __name__ == "__main__":
    for f in (zh_A, zh_B, zh_C, zh_D, en_A, en_B, en_C, en_cover):
        f()
