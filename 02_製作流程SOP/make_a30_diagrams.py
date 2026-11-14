# -*- coding: utf-8 -*-
"""A-30 呂埃勒：1786 年，一張只有線的星圖｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A30-01_連線簡史      → 09 鏡（單層時間軸：1786 Ruelle → 19 世紀 → 1922／1928 IAU → 1952 Rey）
  C-A30-02_1802個連線    → 12 鏡「點陣」層＋「口音」層（上下分區，可疊）
  C-A30-03_這週末抬頭看  → 14 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-30_呂埃勒/_概念圖/（--lang en → _概念圖/en/）；這次只出 zh。

來源：連線＝Stellarium ruelle／western_rey 的 index.json（獅子縮圖照實際星位畫，不臨摹任何出版圖）；
      Bucur, D. (2022) PLOS ONE 17(7): e0272270 2.3 節（56 個星空文化、1,802 個連線圖；中國源流＝暗星簡單形，
      美索不達米亞源流＝亮星複雜形）——口音層是示意，不重繪論文圖、不指認具體星官；
      Stellarium ruelle／western_rey description（19 世紀改畫連線）；IAU 1922／1928。
      天象：PyEphem 4.2.1 自算（台北 25.033°N、121.565°E，2027/4/30 20:00，含大氣折射）。
"""
import os, sys, math, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-30_呂埃勒/_概念圖")
C.set_base(OUT)
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")
RED, GREY = "#FF6B6B", "#7C8BA8"
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "太早的點子", "c01_sub": "星圖上的星座連線，是什麼時候流行起來的？",
        "c01_e1y": "1786", "c01_e1": "Ruelle《新星圖》", "c01_e1b": "拿掉圖畫、只留直線",
        "c01_e1c": "當年沒有流行起來",
        "c01_e2y": "19 世紀", "c01_e2": "歐洲星圖慢慢改畫連線", "c01_e2b": "到世紀末才普遍",
        "c01_e3y": "1922／1928", "c01_e3": "IAU 定下 88 個星座", "c01_e3b": "只有名字和邊界，沒有連線",
        "c01_e4y": "1952", "c01_e4": "H. A. Rey 重畫", "c01_e4b": "讓線看得出形狀",
        "c01_leo1": "Ruelle 的獅子：32 條", "c01_leo2": "Rey 的獅子：18 條",
        "c01_foot": "連線：Stellarium ruelle、western_rey 資料，依實際星位重畫",
        "c02_title": "56 個星空文化，1,802 個星座連線", "c02_sub": "Doina Bucur（2022）把它們放在一起比較",
        "c02_dot": "每一點＝一個星空文化（示意）",
        "c02_a_title": "連線也有「口音」", "c02_cn": "源自中國", "c02_cn2": "暗星・簡單的形狀",
        "c02_me": "源自美索不達米亞", "c02_me2": "亮星・複雜的圖形",
        "c02_foot": "示意圖，不指認具體星官；出處 Bucur, PLOS ONE 17(7), 2022",
        "c03_title": "這週末抬頭看", "c03_sub": "2027/4/30（五）20:00・台北・頭頂在圓心",
        "N": "北", "S": "南", "E": "東", "W": "西",
        "leo": "獅子座（頭頂）", "reg": "軒轅十四", "mars": "火星：別連進去", "jup": "木星",
        "crt": "巨爵座", "crt2": "最亮 3.6 等，要暗處", "crv": "烏鴉座", "spi": "角宿一", "arc": "大角",
        "c03_n1": "天黑到午夜前都看得到；月亮 5/1 01:49 才升起",
        "c03_n2": "拿張紙，照你的眼睛連連看", "c03_line": "琥珀線＝Ruelle 1786 的連法",
        "c03_tag": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "An idea ahead of its time", "c01_sub": "When did star charts start drawing lines?",
        "c01_e1y": "1786", "c01_e1": "Ruelle's Nouvelle Uranographie", "c01_e1b": "figures removed, only lines",
        "c01_e1c": "it did not catch on",
        "c01_e2y": "19th c.", "c01_e2": "European atlases slowly add lines", "c01_e2b": "common by the century's end",
        "c01_e3y": "1922/1928", "c01_e3": "IAU fixes 88 constellations", "c01_e3b": "names and borders, no lines",
        "c01_e4y": "1952", "c01_e4": "H. A. Rey redraws them", "c01_e4b": "lines that look like their names",
        "c01_leo1": "Ruelle's Leo: 32 lines", "c01_leo2": "Rey's Leo: 18 lines",
        "c01_foot": "Lines: Stellarium ruelle and western_rey data, drawn on real star positions",
        "c02_title": "56 sky cultures, 1,802 constellation figures", "c02_sub": "compared by Doina Bucur (2022)",
        "c02_dot": "each dot = one sky culture (schematic)",
        "c02_a_title": "Line figures have accents", "c02_cn": "Chinese-derived", "c02_cn2": "faint stars, simple shapes",
        "c02_me": "Mesopotamian-derived", "c02_me2": "bright stars, complex shapes",
        "c02_foot": "Schematic, not real asterisms; after Bucur, PLOS ONE 17(7), 2022",
        "c03_title": "Look up this weekend", "c03_sub": "Fri 30 Apr 2027, 20:00, Taipei; zenith at centre",
        "N": "N", "S": "S", "E": "E", "W": "W",
        "leo": "Leo (overhead)", "reg": "Regulus", "mars": "Mars: don't connect it", "jup": "Jupiter",
        "crt": "Crater", "crt2": "brightest is mag 3.6: find a dark spot", "crv": "Corvus", "spi": "Spica",
        "arc": "Arcturus",
        "c03_n1": "Visible until midnight; the Moon rises only at 01:49",
        "c03_n2": "Take a sheet of paper and join the dots your way", "c03_line": "amber = Ruelle's 1786 lines",
        "c03_tag": "#WorldSkyCultures",
    },
}


def tx(k):
    return TXT[LANG][k]


S = None


def sc_lines(cu, cid):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    c = next(c for c in d["constellations"] if c["id"] == cid)
    return [[h for h in l if isinstance(h, int)] for l in c["lines"]]


# ══════════════════════ 共用：獅子縮圖（實際星位、東在左） ══════════════════════
def leo_thumb(ax, segs, cx, cy, sc, col, lw=2.0):
    hs = sorted({h for s in segs for h in s})
    ra0 = sum(S[h][0] for h in hs) / len(hs)
    de0 = sum(S[h][1] for h in hs) / len(hs)
    P = lambda h: (cx - (S[h][0] - ra0) * math.cos(math.radians(de0)) * sc, cy + (S[h][1] - de0) * sc)
    for s in segs:
        for a, b in zip(s, s[1:]):
            (x1, y1), (x2, y2) = P(a), P(b)
            ax.plot([x1, x2], [y1, y2], c=col, lw=lw, alpha=.9, solid_capstyle="round", zorder=4)
    for h in hs:
        x, y = P(h)
        ax.scatter([x], [y], s=max(4, (5.2 - S[h][2]) ** 2 * 3.2), c=WHITE, lw=0, zorder=5)


# ══════════════════════ C-A30-01 連線簡史 ══════════════════════
def c01_history(ax):
    T(ax, 0, 0.90, tx("c01_title"), 31)
    T(ax, 0, 0.82, tx("c01_sub"), 17, GREY, w="normal")
    y0, X0, X1 = -0.02, -0.86, 0.86
    yr0, yr1 = 1770, 1965
    fx = lambda y: X0 + (y - yr0) / (yr1 - yr0) * (X1 - X0)
    ax.plot([X0, X1], [y0, y0], c=WHITE, lw=2.0, alpha=.55)
    for yr in (1800, 1900, 1950):
        ax.plot([fx(yr), fx(yr)], [y0 - 0.012, y0 + 0.012], c=WHITE, lw=1.2, alpha=.5)
        T(ax, fx(yr), y0 - 0.045, str(yr), 11, GREY, w="normal")
    # 19 世紀：漸強的帶
    for i in range(40):
        a, b = 1800 + i * 2.5, 1800 + (i + 1) * 2.5
        ax.add_patch(Rectangle((fx(a), y0 - 0.008), fx(b) - fx(a), 0.016, fc=GREEN, ec="none",
                               alpha=0.10 + 0.55 * i / 39, zorder=3))
    ev = [(1786, "c01_e1y", "c01_e1", "c01_e1b", AMBER, +1), (1850, "c01_e2y", "c01_e2", "c01_e2b", GREEN, -1),
          (1925, "c01_e3y", "c01_e3", "c01_e3b", GREY, -1), (1952, "c01_e4y", "c01_e4", "c01_e4b", BLUE, +1)]
    for yr, ky, k1, k2, col, side in ev:
        x = fx(yr)
        ax.scatter([x], [y0], s=170, c=col, zorder=6)
        if side > 0:                                  # 上方：獅子縮圖＋文字
            ax.plot([x, x], [y0, y0 + 0.08], c=col, lw=1.6, alpha=.7)
            T(ax, x, y0 + 0.115, tx(ky), 19, col)
        else:
            ax.plot([x, x], [y0, y0 - 0.10], c=col, lw=1.6, alpha=.7)
            T(ax, x, y0 - 0.135, tx(ky), 19, col)
            T(ax, x, y0 - 0.205, tx(k1), 15, WHITE)
            T(ax, x, y0 - 0.265, tx(k2), 13.5, GREY, w="normal")
    # 1786：Ruelle 的獅子（左上）；1952：Rey 的獅子（右上）
    leo_thumb(ax, sc_lines("ruelle", "CON ruelle Leo"), -0.50, 0.47, 0.0092, AMBER)
    T(ax, -0.50, 0.215, tx("c01_e1"), 15, WHITE)
    T(ax, -0.50, 0.160, tx("c01_e1b") + "；" + tx("c01_e1c") if LANG == "zh"
      else tx("c01_e1b") + "; " + tx("c01_e1c"), 13, GREY, w="normal")
    T(ax, -0.50, 0.70, tx("c01_leo1"), 14, AMBER)
    leo_thumb(ax, sc_lines("western_rey", "CON western_rey Leo"), 0.52, 0.47, 0.0092, BLUE)
    T(ax, 0.52, 0.215, tx("c01_e4"), 15, WHITE)
    T(ax, 0.52, 0.160, tx("c01_e4b"), 13, GREY, w="normal")
    T(ax, 0.52, 0.70, tx("c01_leo2"), 14, BLUE)
    for x0, yr in ((-0.50, 1786), (0.52, 1952)):        # 縮圖→時間軸的細虛線
        ax.plot([x0, fx(yr)], [0.135, y0 + 0.145], c=GREY, lw=1.0, alpha=.45, ls=(0, (3, 3)))
    T(ax, 0, -0.62, tx("c01_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-A30-02 1802 個連線 ══════════════════════
def c02_dots(ax):
    T(ax, 0, 0.90, tx("c02_title"), 27)
    T(ax, 0, 0.82, tx("c02_sub"), 16, GREY, w="normal")
    rnd = random.Random(30)
    cols, rows = 14, 4
    for i in range(56):
        r, c = divmod(i, cols)
        x, y = -0.78 + c * 0.12, 0.64 - r * 0.12
        ax.add_patch(Circle((x, y), 0.034, fc=BLUE, ec="none", alpha=0.30 + 0.5 * rnd.random(), zorder=4))
    T(ax, 0, 0.215, tx("c02_dot"), 14, GREY, w="normal")


def _shape(ax, cx, cy, pts, edges, col, mags):
    P = [(cx + x, cy + y) for x, y in pts]
    for a, b in edges:
        ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], c=col, lw=2.2, alpha=.85, zorder=4)
    for (x, y), mg in zip(P, mags):
        ax.scatter([x], [y], s=mg, c=WHITE, lw=0, zorder=5)


def c02_accent(ax):
    T(ax, 0, 0.08, tx("c02_a_title"), 25, AMBER)
    for x0 in (-0.44, 0.44):
        ax.add_patch(FancyBboxPatch((x0 - 0.38, -0.70), 0.76, 0.66, boxstyle="round,pad=0,rounding_size=0.05",
                                    fc="none", ec=GREY, lw=1.2, alpha=.5, zorder=2))
    # 左：暗星＋簡單的形（一條折線、一個小方框）
    _shape(ax, -0.44, -0.30, [(-0.26, 0.10), (-0.13, 0.16), (0.0, 0.10), (0.13, 0.15), (0.26, 0.08),
                              (-0.10, -0.02), (0.06, -0.02), (0.06, -0.12), (-0.10, -0.12)],
           [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8), (8, 5)], BLUE, [12] * 9)
    T(ax, -0.44, -0.55, tx("c02_cn"), 18, BLUE)
    T(ax, -0.44, -0.62, tx("c02_cn2"), 14, WHITE, w="normal")
    # 右：亮星＋三角網
    pts = [(-0.24, 0.12), (-0.04, 0.18), (0.20, 0.10), (-0.16, -0.06), (0.06, -0.02), (0.24, -0.10),
           (-0.06, -0.22), (0.14, -0.24)]
    ed = [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 6), (4, 7),
          (5, 7), (6, 7)]
    _shape(ax, 0.44, -0.27, pts, ed, AMBER, [150, 110, 130, 90, 160, 100, 120, 85])
    T(ax, 0.44, -0.55, tx("c02_me"), 18, AMBER)
    T(ax, 0.44, -0.62, tx("c02_me2"), 14, WHITE, w="normal")
    T(ax, 0, -0.80, tx("c02_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-A30-03 這週末抬頭看（圖卡） ══════════════════════
def c03_card(ax):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.elevation = 0
    o.temp, o.pressure = 20.0, 1010.0
    o.date = ephem.Date("2027/4/30 12:00")
    ax.text(0.5, 0.925, tx("c03_title"), fontproperties=C.FP, fontsize=25, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.885, tx("c03_sub"), fontproperties=C.FP, fontsize=12.5, color=GREY, ha="center", va="center")
    cx, cy, R = 0.5, 0.53, 0.43
    asp = 9 / 16

    def xy(alt, az):
        r = (90 - alt) / 90 * R
        a = math.radians(az)
        return cx - r * math.sin(a), cy + r * math.cos(a) * asp     # 北上、東左（仰望）

    ax.add_patch(Ellipse((cx, cy), 2 * R, 2 * R * asp, fc="#0E1530", ec=GREY, lw=1.2, zorder=1))
    for alt in (30, 60):
        ax.add_patch(Ellipse((cx, cy), 2 * R * (90 - alt) / 90, 2 * R * (90 - alt) / 90 * asp, fc="none", ec=GREY,
                             lw=0.6, alpha=.35, ls=(0, (3, 3)), zorder=2))
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = xy(-7, az)
        ax.text(x, y, tx(k), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center", weight="bold")

    def star(h):
        st = ephem.FixedBody(); st._ra, st._dec, st._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        st.compute(o); return math.degrees(st.alt), math.degrees(st.az)

    # Ruelle 的獅子、巨爵、烏鴉（琥珀細線）
    for cid in ("Leo", "Crt", "Crv"):
        for s in sc_lines("ruelle", f"CON ruelle {cid}"):
            for a, b in zip(s, s[1:]):
                (x1, y1), (x2, y2) = xy(*star(a)), xy(*star(b))
                ax.plot([x1, x2], [y1, y2], c=AMBER, lw=1.1, alpha=.75, zorder=3)
    for h, (ra, dec, v) in ((h, S[h][:3]) for h in S):
        if v > 4.2:
            continue
        alt, az = star(h)
        if alt < 0:
            continue
        x, y = xy(alt, az)
        ax.scatter([x], [y], s=max(1.2, (4.6 - v) ** 2.1 * 2.0), c=WHITE, lw=0, zorder=4)

    def body(b):
        b.compute(o); return math.degrees(b.alt), math.degrees(b.az)
    marks = [(star(49669), "reg", WHITE, 0, (0.0, -0.020)), (body(ephem.Mars()), "mars", RED, 70, (0.13, -0.040)),
             (body(ephem.Jupiter()), "jup", WHITE, 90, (0.040, 0.0)), (star(53740), "crt", AMBER, 0, (0.072, -0.004)),
             (star(59803), "crv", WHITE, 0, (0.0, -0.022)), (star(65474), "spi", WHITE, 0, (0.0, -0.020)),
             (star(69673), "arc", WHITE, 0, (0.0, 0.020)), (star(54872), "leo", AMBER, 0, (0.0, 0.085))]
    for (alt, az), key, col, s, (dx, dy) in marks:
        x, y = xy(alt, az)
        if s:
            ax.scatter([x], [y], s=s, c=col, lw=0, zorder=6)
        ax.text(x + dx, y + dy, tx(key), fontproperties=C.FP, fontsize=11.5, color=col, ha="center", va="center",
                weight="bold", zorder=7)
        if key == "mars":                             # 細引線：火星→標籤
            ax.plot([x + 0.012, x + dx - 0.05], [y - 0.004, y + dy + 0.008], c=RED, lw=0.8, alpha=.7, zorder=6)
        if key == "crt":
            ax.text(x + dx, y + dy - 0.018, tx("crt2"), fontproperties=C.FP, fontsize=9.5, color=WHITE,
                    ha="center", va="center", zorder=7)
    ax.text(0.5, 0.235, tx("c03_line"), fontproperties=C.FP, fontsize=11, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.195, tx("c03_n1"), fontproperties=C.FP, fontsize=12.5, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.150, tx("c03_n2"), fontproperties=C.FP, fontsize=14, color=AMBER, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.035, tx("c03_tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ 輸出 ══════════════════════
def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    f, ax = C.newfig(); c01_history(ax); C.save(f, "", "C-A30-01_連線簡史_透明.png")
    f, ax = C.newfig(dark=True); c01_history(ax); C.save(f, "", "C-A30-01_連線簡史_預覽_黑底.png", transparent=False)
    C.emit("", [("點陣", c02_dots), ("口音", c02_accent)], title="C-A30-02_1802個連線")
    f, ax = C.newcard(dark=True); c03_card(ax); C.save(f, "", "C-A30-03_這週末抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
