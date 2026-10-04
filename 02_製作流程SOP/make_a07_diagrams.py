# -*- coding: utf-8 -*-
"""A-07 蒙古｜概念圖（C 系列骨架）
  C-A07-01_生肖本命星兩個版本   → 逐字稿 06–07 鏡疊用（9:16 圖卡＋方形分層）
  C-A07-02_七兄弟不是一家人     → 逐字稿 08 鏡疊用（距離＋大熊座移動星群）
輸出：05_素材/A-07_蒙古/_概念圖/
距離＝依巴谷視差（van Leeuwen 2007）換算，四捨五入到 0.1 光年；見逐字稿考據備忘。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, BG, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-07_蒙古/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#7C8BA8"

STARS = ["天樞", "天璇", "天璣", "天權", "玉衡", "開陽", "搖光"]
XJ = ["貪狼", "巨門", "祿存", "文曲", "廉貞", "武曲", "破軍"]
LOOP = ["鼠・羊", "牛・猴", "虎・雞", "兔・狗", "龍・豬", "蛇", "馬"]
SWING = ["鼠", "牛・豬", "虎・狗", "兔・雞", "龍・猴", "蛇・羊", "馬"]


def route(ax, y, seq2, col, lab):
    """一條直線上的七顆星：下排＝第一輪 1–7（鼠…馬），上排＝第二輪 8–12（羊…豬）"""
    xs = [.14 + i * .12 for i in range(7)]
    ax.plot([xs[0], xs[-1]], [y, y], c=GREY, lw=1.4, alpha=.5, zorder=2)
    for i, x in enumerate(xs):
        ax.scatter([x], [y], s=90, c=WHITE, zorder=5)
        T(ax, x, y - .024, STARS[i], 9.5, WHITE, w="normal")
        T(ax, x, y - .045, str(i + 1), 10, GREY)
    for k, si in enumerate(seq2):
        T(ax, xs[si], y + .026, str(k + 8), 11.5, col)
    a, b = seq2[0], 6
    C.arrow(ax, (xs[a], y + .047), (xs[b], y + .047), c=col, lw=1.6, alpha=.8)
    T(ax, .5, y + .072, lab, 11.5, col)


def card_01():
    f, ax = C.newcard(dark=True)
    T(ax, .5, .945, "生肖本命星：兩個版本", 24, WHITE)
    T(ax, .5, .905, "七顆星、十二生肖——數到斗柄尾端之後怎麼辦？", 12.5, GREY, w="normal")
    # 表頭
    y0, dy = .83, .046
    for x, t, c in ((.16, "北斗", WHITE), (.40, "循環版", AMBER), (.66, "折返版", BLUE),
                    (.88, "本命星君", BLUE)):
        T(ax, x, y0, t, 14, c)
    T(ax, .40, y0 - .026, "Stellarium 記錄", 9, AMBER, w="normal")
    T(ax, .66, y0 - .026, "蒙古《北斗七星經》", 9, BLUE, w="normal")
    T(ax, .88, y0 - .026, "台灣禮斗同一張表", 9, BLUE, w="normal")
    for i in range(7):
        y = y0 - .07 - i * dy
        if i % 2 == 0:
            ax.add_patch(C.Rectangle((.04, y - dy / 2), .92, dy, fc="#141A30",
                                     ec="none", zorder=1))
        T(ax, .16, y, STARS[i], 15, WHITE)
        T(ax, .40, y, LOOP[i], 15, AMBER)
        T(ax, .66, y, SWING[i], 15, BLUE)
        T(ax, .88, y, XJ[i], 13, BLUE, w="normal")
    # 2026 馬年、2027 羊年
    yb = y0 - .07 - 7 * dy + .005
    ax.add_patch(C.FancyBboxPatch((.06, yb - .085), .88, .075,
                                  boxstyle="round,pad=0.008,rounding_size=0.015",
                                  fc="#1B2240", ec=AMBER, lw=1.2, zorder=2))
    T(ax, .5, yb - .03, "2026 馬年出生：兩版都是 搖光（破軍）", 13.5, AMBER)
    T(ax, .5, yb - .062, "2027 羊年出生起分家：循環版回到天樞　折返版退到開陽", 11, WHITE,
      w="normal")
    # 兩條路線示意（第二輪 8–12 落在哪顆星）
    route(ax, .262, [0, 1, 2, 3, 4], AMBER, "循環：7 馬之後跳回天樞，8 羊…12 豬")
    route(ax, .122, [5, 4, 3, 2, 1], BLUE, "折返：7 馬之後原路退回，8 羊在開陽…12 豬在天璇")
    T(ax, .5, .045, "資料：Stellarium mongolian／Elverskog 2006〈The Mongolian Big Dipper Sūtra〉"
                    "／《太上玄靈北斗本命延生真經》", 7.5, GREY, w="normal")
    C.save(f, "", "C-A07-01_生肖本命星兩個版本_圖卡.png", transparent=False)


DIST = [("天樞", "Dubhe", 123.0, False), ("天璇", "Merak", 79.7, True),
        ("天璣", "Phecda", 83.2, True), ("天權", "Megrez", 80.5, True),
        ("玉衡", "Alioth", 82.6, True), ("開陽", "Mizar", 82.9, True),
        ("搖光", "Alkaid", 103.9, False)]


def card_02():
    f, ax = C.newcard(dark=True)
    T(ax, .5, .945, "七兄弟不是一家人", 25, WHITE)
    T(ax, .5, .905, "北斗七星離我們多遠（光年）", 13, GREY, w="normal")
    x0, x1, d0, d1 = .14, .92, 70.0, 130.0
    X = lambda d: x0 + (x1 - x0) * (d - d0) / (d1 - d0)
    ytop, dy = .80, .075
    for d in range(70, 131, 10):
        ax.plot([X(d), X(d)], [ytop + .03, ytop - 6 * dy - .03], c="#1E2640", lw=1,
                zorder=1)
        T(ax, X(d), ytop - 6 * dy - .06, f"{d}", 10, GREY, w="normal")
    ax.add_patch(C.Rectangle((X(78.5), ytop - 6 * dy - .03), X(85) - X(78.5),
                             6 * dy + .06, fc=AMBER, ec="none", alpha=.12, zorder=1))
    for i, (zh, en, d, member) in enumerate(DIST):
        y = ytop - i * dy
        c = AMBER if member else WHITE
        ax.plot([x0, X(d)], [y, y], c=c, lw=2.2, alpha=.35 if member else .5, zorder=2)
        ax.scatter([X(d)], [y], s=160, c=c, zorder=5)
        T(ax, .075, y + .012, zh, 14, c)
        T(ax, .075, y - .016, en, 8.5, GREY, w="normal")
        T(ax, X(d) + (.06 if d < 110 else -.075), y, f"{d:.0f}", 13, c)
    yb = ytop - 6 * dy - .13
    T(ax, .5, yb, "中間五顆：80 光年上下，一起誕生、朝同一個方向走", 13.5, AMBER)
    T(ax, .5, yb - .035, "＝大熊座移動星群（開陽旁的輔也是成員）", 11, AMBER, w="normal")
    T(ax, .5, yb - .085, "天樞、搖光：不同距離、不同方向——只是剛好路過", 13.5, WHITE)
    T(ax, .5, yb - .135, "約五萬年後，勺子就認不出來了", 15, WHITE)
    T(ax, .5, .045, "距離：依巴谷視差（van Leeuwen 2007）換算", 8, GREY, w="normal")
    C.save(f, "", "C-A07-02_七兄弟不是一家人_圖卡.png", transparent=False)


# ═══════ Reels 用：方形透明分層（疊在天空上的定格頁，一頁多一層；圖卡留給輪播） ═══════
ROWY = [0.50 - i * 0.135 for i in range(7)]
COLX = dict(星=-0.64, 循環=-0.08, 折返=0.52)


def z01_base(ax):
    T(ax, 0.0, 0.93, "生肖本命星：兩個版本", 34, WHITE)
    T(ax, 0.0, 0.855, "七顆星、十二生肖——數到斗柄尾端之後怎麼辦？", 19, GREY, w="normal")
    T(ax, COLX["星"], 0.68, "北斗", 24, WHITE)
    for i, y in enumerate(ROWY):
        if i % 2 == 0:
            ax.add_patch(C.Rectangle((-0.92, y - 0.0675), 1.84, 0.135, fc="#141A30",
                                     ec="none", alpha=.85, zorder=1))
        T(ax, COLX["星"], y, STARS[i], 24, WHITE)


def z01_loop(ax):
    T(ax, COLX["循環"], 0.70, "循環版", 24, AMBER)
    T(ax, COLX["循環"], 0.625, "Stellarium 記錄", 15, AMBER, w="normal")
    for i, y in enumerate(ROWY):
        T(ax, COLX["循環"], y, LOOP[i], 24, AMBER)


def z01_swing(ax):
    T(ax, COLX["折返"], 0.70, "折返版", 24, BLUE)
    T(ax, COLX["折返"], 0.625, "蒙古《北斗七星經》", 15, BLUE, w="normal")
    for i, y in enumerate(ROWY):
        T(ax, COLX["折返"], y, SWING[i], 24, BLUE)
    ax.add_patch(C.FancyBboxPatch((-0.90, -0.88), 1.80, 0.22,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.6, zorder=2))
    T(ax, 0.0, -0.72, "2026 馬年出生：兩版都是 搖光", 21, AMBER)
    T(ax, 0.0, -0.815, "2027 羊年起分家：循環版回到天樞　折返版退到開陽", 17, WHITE,
      w="normal")


D0, D1, BX0, BX1 = 70.0, 130.0, -0.60, 0.86
DX = lambda d: BX0 + (BX1 - BX0) * (d - D0) / (D1 - D0)
DROW = [0.60 - i * 0.125 for i in range(7)]


def z02_dist(ax):
    T(ax, 0.0, 0.93, "七兄弟不是一家人", 34, WHITE)
    T(ax, 0.0, 0.855, "北斗七星離我們多遠（光年）", 19, GREY, w="normal")
    ybot = DROW[-1] - 0.08
    for d in range(70, 131, 10):
        ax.plot([DX(d), DX(d)], [DROW[0] + 0.06, ybot], c="#2A3456", lw=1.2, zorder=1)
        T(ax, DX(d), ybot - 0.05, f"{d}", 15, GREY, w="normal")
    ax.add_patch(C.Rectangle((DX(78.5), ybot), DX(85) - DX(78.5), DROW[0] + 0.06 - ybot,
                             fc=AMBER, ec="none", alpha=.14, zorder=1))
    for (zh, en, d, member), y in zip(DIST, DROW):
        c = AMBER if member else WHITE
        ax.plot([BX0, DX(d)], [y, y], c=c, lw=3, alpha=.35 if member else .55, zorder=2)
        ax.scatter([DX(d)], [y], s=260, c=c, zorder=5)
        T(ax, -0.80, y + 0.018, zh, 21, c)
        T(ax, -0.80, y - 0.035, en, 13, GREY, w="normal")
        T(ax, DX(d) + (0.09 if d < 110 else -0.11), y, f"{d:.0f}", 19, c)


def z02_note(ax):
    y = DROW[-1] - 0.24
    T(ax, 0.0, y, "中間五顆：80 光年上下，一起誕生、朝同一個方向走", 20, AMBER)
    T(ax, 0.0, y - 0.075, "＝大熊座移動星群", 16, AMBER, w="normal")
    T(ax, 0.0, y - 0.18, "天樞、搖光：不同距離、不同方向——只是剛好路過", 20, WHITE)
    T(ax, 0.0, y - 0.29, "約五萬年後，勺子就認不出來了", 23, WHITE)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    card_01()
    card_02()
    C.emit("", [("北斗", z01_base), ("循環版", z01_loop), ("折返版", z01_swing)],
           title="C-A07-01_生肖本命星兩個版本")
    C.emit("", [("距離", z02_dist), ("結論", z02_note)], title="C-A07-02_七兄弟不是一家人")
