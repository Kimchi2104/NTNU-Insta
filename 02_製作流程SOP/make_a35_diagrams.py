# -*- coding: utf-8 -*-
"""A-35 現代星座（上）：88 個星座誰說了算｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A35-01_88個星座從哪來     → 逐字稿 02／04／05b／06 鏡（88 格堆疊，一鏡一層，每層都是「到那一年為止」的累計圖）
                                 到150年層 → 到1597年層 → 到1690年層 → 到1756年層（＝88）
  C-A35-02_邊界是一塊地       → 逐字稿 10 鏡（長蛇層→南十字層；同一比例、等面積投影）
  C-A35-03_巨蛇被切成兩塊     → 逐字稿 11 鏡（三塊層→89塊層）
  C-A35-04_88星座出身表       → 逐字稿 08 鏡（9:16 圖卡）
  C-A35-05_今晚的巨蛇與盾牌   → 逐字稿 14 鏡（9:16 圖卡，可存圖；台北 2027/6/11 21:00 面向東南）
輸出：05_素材/A-35_現代星座上/_概念圖/（--lang en → _概念圖/en/，這次只出 zh）

來源：88 星座的出身分組＝逐字稿考據備忘（托勒密 48→今 50、Keyser＆de Houtman／Plancius 12、Plancius 3、南十字、
      后髮、Hevelius 7、Lacaille 14）；IAU 邊界多邊形與面積＝make_a35_v4.py 的 IAUGrid（constellations_spans.dat，
      Delporte 1930，B1875 → J2000）；連線＝Stellarium modern_iau；天象 PyEphem 4.2.1 自算（台北 25.033°N、121.565°E）。
      C-A35-02／03 用正弦（Sanson–Flamsteed）等面積投影：形狀會變、面積比例正確（圖上註明）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch
import gen_ep_assets as G
import make_a35_v4 as A

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-35_現代星座上/_概念圖")
C.set_base(OUT)
RED, GREY, BG = "#FF6B6B", "#9AA6C0", "#0B0F1E"
S = None
LANG = "zh"
EN_NAME = {c: A.IAU[c]["common_name"]["native"] for c in A.IAU}
TXT = {
    "zh": {
        "c01_title": "88 個星座從哪來", "c01_sub": "一格＝一個星座；顏色＝誰加進來的",
        "g_ptol": "約 150 年　托勒密 48 座（南船今拆成三座＝50）",
        "g_key": "1597　Keyser＆de Houtman 觀測・Plancius　+12",
        "g_oth": "16–17 世紀　Plancius 3・南十字・后髮　+5",
        "g_hev": "1690　Hevelius　+7",
        "g_lac": "1756　Lacaille　+14　＝ 88",
        "c02_title": "星座是一塊地", "c02_sub": "同一比例尺・等面積投影（形狀會變，面積比例正確）",
        "hya": "長蛇座", "hya_a": "1,302.84 平方度・最大", "cru": "南十字座", "cru_a": "68.45 平方度・最小",
        "x19": "長蛇 ÷ 南十字 ≈ 19 倍",
        "c03_title": "巨蛇座被切成兩塊", "c03_sub": "IAU 邊界（Delporte 1930）",
        "caput": "蛇頭", "cauda": "蛇尾", "oph": "蛇夫座", "caput_en": "Serpens Caput", "cauda_en": "Serpens Cauda",
        "n89": "88 個星座，89 塊", "n89b": "唯一分成兩塊的星座",
        "c04_title": "88 個星座出身表", "c04_sub": "1922 年 IAU 名單・中文正式名",
        "h_ptol": "托勒密《天文學大成》約 150 年（48 座→今 50）",
        "h_key": "南天 12 座：Keyser＆de Houtman 觀測，Plancius 1597/98 天球儀",
        "h_oth": "Plancius 3 座・南十字・后髮",
        "h_hev": "Hevelius 1690 年星圖 7 座",
        "h_lac": "Lacaille 1756 年 14 座（13 件儀器＋一座山）",
        "c04_foot": "南船座（Argo）拆成船底、船尾、船帆，所以托勒密 48 座今天算 50 個",
        "c05_title": "今晚的巨蛇與盾牌", "c05_sub": "2027/6/11（五）21:00・台北・面向東南",
        "east": "東", "se": "東南", "south": "南",
        "caput_l": "蛇頭（天市右垣七）", "oph_l": "蛇夫（候）", "cauda_l": "蛇尾", "sct_l": "盾牌座",
        "alt": "高 {:.0f}°",
        "n1": "同一個星座，分在蛇夫的兩邊",
        "n2": "市區大概只認得出蛇頭最亮那顆；",
        "n3": "蛇尾、盾牌用雙筒望遠鏡更好",
        "n4": "西邊（背後右手）：上弦月 39°，00:03 才下山",
        "n5": "PyEphem 自算；方位、高度為台北 21:00",
    },
    "en": {
        "c01_title": "Where the 88 constellations came from", "c01_sub": "One square = one constellation; colour = who added it",
        "g_ptol": "c. 150 AD  Ptolemy's 48 (Argo now split in three = 50)",
        "g_key": "1597  Keyser & de Houtman, via Plancius  +12",
        "g_oth": "16th–17th c.  Plancius 3 · Crux · Coma  +5",
        "g_hev": "1690  Hevelius  +7",
        "g_lac": "1756  Lacaille  +14  = 88",
        "c02_title": "A constellation is a piece of land", "c02_sub": "Same scale, equal-area projection",
        "hya": "Hydra", "hya_a": "1,302.84 sq deg · largest", "cru": "Crux", "cru_a": "68.45 sq deg · smallest",
        "x19": "Hydra ÷ Crux ≈ 19",
        "c03_title": "Serpens, cut in two", "c03_sub": "IAU boundaries (Delporte 1930)",
        "caput": "Head", "cauda": "Tail", "oph": "Ophiuchus", "caput_en": "Serpens Caput", "cauda_en": "Serpens Cauda",
        "n89": "88 constellations, 89 pieces", "n89b": "the only constellation in two parts",
        "c04_title": "The 88, by origin", "c04_sub": "IAU list of 1922",
        "h_ptol": "Ptolemy, Almagest, c. 150 AD (48 → 50 today)",
        "h_key": "12 southern: Keyser & de Houtman, Plancius 1597/98",
        "h_oth": "Plancius 3 · Crux · Coma Berenices",
        "h_hev": "Hevelius 1690: 7", "h_lac": "Lacaille 1756: 14 (13 instruments + a mountain)",
        "c04_foot": "Argo Navis was split into Carina, Puppis and Vela",
        "c05_title": "Tonight: the Serpent and the Shield", "c05_sub": "Fri 11 June 2027, 21:00 · Taipei · facing SE",
        "east": "E", "se": "SE", "south": "S",
        "caput_l": "Serpent's head (Unukalhai)", "oph_l": "Ophiuchus (Rasalhague)", "cauda_l": "Serpent's tail",
        "sct_l": "Scutum", "alt": "alt {:.0f}°",
        "n1": "One constellation, on both sides of Ophiuchus",
        "n2": "In the city you may only spot the head's brightest star;",
        "n3": "binoculars help for the tail and the shield",
        "n4": "West (behind you, right): first-quarter Moon at 39°, sets 00:03",
        "n5": "Computed with PyEphem for Taipei, 21:00",
    },
}


def tx(k):
    return TXT[LANG][k]


def nm(c):
    return A.ZH[c] if LANG == "zh" else EN_NAME[c]


# ══════════════════════ C-A35-01 88 格堆疊 ══════════════════════
GROUPS = [("ptol", A.PTOL, AMBER), ("key", A.KEYSER, GREEN), ("oth", A.OTHER5, WHITE), ("hev", A.HEV, BLUE),
          ("lac", A.LAC, PURPLE)]
STAGE = {"到150年": ["ptol"], "到1597年": ["ptol", "key"], "到1690年": ["ptol", "key", "oth", "hev"],
         "到1756年": ["ptol", "key", "oth", "hev", "lac"]}
NC, CW, CH, X0, Y0 = 11, 0.154, 0.142, -0.847, 0.70


def _cells():
    out, k = [], 0
    for g, cs, col in GROUPS:
        for c in sorted(cs, key=lambda c: A.ZH[c]):
            r, q = divmod(k, NC)
            out.append((g, c, col, X0 + q * CW, Y0 - r * CH))
            k += 1
    return out


def c01(stage):
    def draw(ax):
        T(ax, 0, 0.90, tx("c01_title"), 32, WHITE)
        T(ax, 0, 0.815, tx("c01_sub"), 16, GREY, w="normal")
        on = STAGE[stage]
        for g, c, col, x, y in _cells():
            ax.add_patch(Rectangle((x + 0.006, y - CH + 0.006), CW - 0.012, CH - 0.012, fc=BG, ec="none", zorder=2))
            if g in on:
                ax.add_patch(Rectangle((x + 0.006, y - CH + 0.006), CW - 0.012, CH - 0.012, fc=col, ec="none",
                                       alpha=0.30, zorder=3))
                ax.add_patch(Rectangle((x + 0.006, y - CH + 0.006), CW - 0.012, CH - 0.012, fc="none", ec=col,
                                       lw=1.6, zorder=4))
                T(ax, x + CW / 2, y - CH / 2, nm(c), 12 if LANG == "zh" else 7, WHITE, w="normal")
            else:
                ax.add_patch(Rectangle((x + 0.006, y - CH + 0.006), CW - 0.012, CH - 0.012, fc="none", ec=GREY,
                                       lw=0.8, alpha=0.35, ls=(0, (3, 3)), zorder=4))
        ys = -0.62
        for g, cs, col in GROUPS:
            if g in on:
                ax.add_patch(Rectangle((-0.86, ys - 0.018), 0.036, 0.036, fc=col, ec="none", zorder=5))
                T(ax, -0.80, ys, tx("g_" + g), 15, col, ha="left", w="bold" if g == on[-1] else "normal")
            ys -= 0.065
    return draw


# ══════════════════════ 等面積投影（正弦） ══════════════════════
def sinus(loops, ra0, dec0=0.0):
    out = []
    for lp in loops:
        q = []
        for ra, dec in lp:
            d = ((ra - ra0 + 180) % 360) - 180
            q.append((-d * math.cos(math.radians(dec)), dec - dec0))      # 東在左
        out.append(q)
    return out


def poly(ax, loops, sc, ox, oy, col, alpha=0.30, lw=2.2):
    for q in loops:
        P = [(ox + x * sc, oy + y * sc) for x, y in q]
        ax.add_patch(Polygon(P, closed=True, fc=BG, ec="none", zorder=2))
        ax.add_patch(Polygon(P, closed=True, fc=col, ec="none", alpha=alpha, zorder=3))
        ax.add_patch(Polygon(P, closed=True, fc="none", ec=col, lw=lw, zorder=4))


HYA = None


def _hya():
    global HYA
    if HYA is None:
        ra0, _ = A.GRID.centroid("HYA")
        L = sinus(A.GRID.loops({"HYA"}), ra0)
        xs = [x for q in L for x, y in q]; ys = [y for q in L for x, y in q]
        HYA = (L, (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, max(xs) - min(xs))
    return HYA


def _sc():
    return 1.50 / _hya()[3]


def c02_hya(ax):
    T(ax, 0, 0.90, tx("c02_title"), 32, WHITE)
    T(ax, 0, 0.815, tx("c02_sub"), 16, GREY, w="normal")
    L, cx, cy, w = _hya()
    sc = _sc()
    poly(ax, L, sc, -cx * sc, 0.33 - cy * sc, BLUE)
    T(ax, -0.15, 0.58, tx("hya"), 26, BLUE)
    T(ax, -0.15, 0.51, tx("hya_a"), 16, WHITE, w="normal")


def c02_cru(ax):
    sc = _sc()
    ra0, dec0 = A.GRID.centroid("CRU")
    L = sinus(A.GRID.loops({"CRU"}), ra0, dec0)
    poly(ax, L, sc, -0.62, -0.42, AMBER, alpha=0.45)
    T(ax, -0.62, -0.26, tx("cru"), 24, AMBER)
    T(ax, -0.62, -0.58, tx("cru_a"), 15, WHITE, w="normal")
    # 19 塊同樣大小的方塊（等面積）＝長蛇
    side = math.sqrt(A.AREA["CRU"]) * sc
    for k in range(19):
        r, q = divmod(k, 6)
        x, y = -0.08 + q * (side + 0.012), -0.17 - r * (side + 0.012)
        ax.add_patch(Rectangle((x, y - side), side, side, fc=BLUE, ec=BLUE, alpha=0.35, lw=1.2, zorder=3))
    T(ax, 0.38, -0.86, tx("x19"), 20, WHITE)


# ══════════════════════ C-A35-03 巨蛇兩塊 ══════════════════════
def _ser():
    ra0, dec0 = A.GRID.centroid("OPH")
    parts = {k: sinus(A.GRID.loops({k}), ra0, dec0) for k in ("SerCaput", "SerCauda", "OPH")}
    xs = [x for L in parts.values() for q in L for x, y in q]
    ys = [y for L in parts.values() for q in L for x, y in q]
    sc = 1.60 / max(max(xs) - min(xs), (max(ys) - min(ys)) / 0.75)
    return parts, sc, (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, ra0, dec0


def c03_parts(ax):
    T(ax, 0, 0.90, tx("c03_title"), 32, WHITE)
    T(ax, 0, 0.815, tx("c03_sub"), 16, GREY, w="normal")
    parts, sc, cx, cy, ra0, dec0 = _ser()
    ox, oy = -cx * sc, 0.05 - cy * sc
    poly(ax, parts["OPH"], sc, ox, oy, AMBER, alpha=0.22)
    poly(ax, parts["SerCaput"], sc, ox, oy, GREEN, alpha=0.30)
    poly(ax, parts["SerCauda"], sc, ox, oy, GREEN, alpha=0.30)
    for key, col, lw in (("Ser", GREEN, 2.6), ("Oph", AMBER, 2.0)):
        for seg in A.SEG[key]:
            P = [sinus([[S[h][:2]]], ra0, dec0)[0][0] for h in seg if h in S]
            ax.plot([ox + x * sc for x, y in P], [oy + y * sc for x, y in P], c=col, lw=lw, alpha=.95, zorder=6)
            ax.scatter([ox + x * sc for x, y in P], [oy + y * sc for x, y in P], s=14, c=WHITE, zorder=7)
    for k, lab, en, col in (("SerCaput", "caput", "caput_en", GREEN), ("SerCauda", "cauda", "cauda_en", GREEN),
                            ("OPH", "oph", None, AMBER)):
        ra, dec = A.GRID.centroid(k)
        x, y = sinus([[(ra, dec)]], ra0, dec0)[0][0]
        lx, ly = {"SerCaput": (ox + x * sc, 0.72), "SerCauda": (-0.62, -0.40), "OPH": (0.46, -0.34)}[k]
        T(ax, lx, ly, tx(lab), 24, col)
        if en:
            T(ax, lx, ly - 0.055, tx(en), 13, WHITE, w="normal")


def c03_89(ax):
    ax.add_patch(FancyBboxPatch((-0.55, -0.90), 1.10, 0.20, boxstyle="round,pad=0.01,rounding_size=0.04",
                                fc=BG, ec=GREEN, lw=2.0, alpha=0.95, zorder=8))
    T(ax, 0, -0.775, tx("n89"), 26, GREEN, z=9)
    T(ax, 0, -0.845, tx("n89b"), 14, WHITE, w="normal", z=9)


# ══════════════════════ C-A35-04 出身表（9:16） ══════════════════════
def wrap_names(cs, per):
    names = [nm(c) for c in sorted(cs, key=lambda c: A.ZH[c])]
    return ["・".join(names[i:i + per]) for i in range(0, len(names), per)]


def c04_card(ax):
    T(ax, 0.5, 0.835, tx("c04_title"), 26, WHITE)
    T(ax, 0.5, 0.805, tx("c04_sub"), 12, GREY, w="normal")
    y = 0.765
    for g, cs, col in GROUPS:
        T(ax, 0.07, y, f"{len(cs)}", 22, col, ha="left")
        T(ax, 0.16, y, tx("h_" + g), 11.5, col, ha="left")
        y -= 0.030
        for line in wrap_names(cs, 9):
            T(ax, 0.16, y, line, 12.5, WHITE, ha="left", w="normal")
            y -= 0.026
        y -= 0.018
    T(ax, 0.5, y - 0.005, tx("c04_foot"), 10, GREY, w="normal")
    T(ax, 0.5, y - 0.035, "50 + 12 + 5 + 7 + 14 ＝ 88", 18, AMBER)


# ══════════════════════ C-A35-05 今晚（9:16） ══════════════════════
AZ0, AZ1, ALT1 = 72.0, 192.0, 74.0
PX0, PX1, PY0 = 0.06, 0.94, 0.33


def _azalt(ra, dec):
    a, z = A.altaz(ra, dec, "2027/6/11 21:00")
    return z, a


def _xy(az, alt):
    s = (PX1 - PX0) / (AZ1 - AZ0)
    return PX0 + (az - AZ0) * s, PY0 + alt * s * (6.075 / 10.8)


def c05_card(ax):
    T(ax, 0.5, 0.835, tx("c05_title"), 26, WHITE)
    T(ax, 0.5, 0.805, tx("c05_sub"), 12, GREY, w="normal")
    x0, y0 = _xy(AZ0, 0); x1, y1 = _xy(AZ1, ALT1)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#0E1530", ec="none", zorder=1))
    for alt in (20, 40, 60):
        a, b = _xy(AZ0, alt), _xy(AZ1, alt)
        ax.plot([a[0], b[0]], [a[1], a[1]], c=GREY, lw=0.6, alpha=.35, ls=(0, (3, 4)), zorder=2)
        T(ax, a[0] + 0.005, a[1] + 0.008, f"{alt}°", 8, GREY, ha="left", w="normal")
    for k, v in S.items():
        ra, dec, mag = v
        if mag > 4.6:
            continue
        az, alt = _azalt(ra, dec)
        if AZ0 + 1.5 < az < AZ1 - 1.5 and 0.5 < alt < ALT1 - 1.5:
            x, y = _xy(az, alt)
            ax.scatter([x], [y], s=max(1.5, (5.0 - mag) * 9), c=WHITE, lw=0, zorder=4, alpha=.9)
    for key, col in (("Ser", GREEN), ("Oph", AMBER), ("Sct", BLUE)):
        for seg in A.SEG[key]:
            P = [_xy(*_azalt(*S[h][:2])) for h in seg if h in S]
            ax.plot([p[0] for p in P], [p[1] for p in P], c=col, lw=1.8, alpha=.9, zorder=5)
    labs = ((A.UNUK, "caput_l", GREEN, 0.16, 0.008), (A.RASALHAGUE, "oph_l", AMBER, 0.0, 0.028),
            (A.ETA_SER, "cauda_l", GREEN, -0.03, 0.026), (A.ALPHA_SCT, "sct_l", BLUE, 0.0, -0.030))
    for h, k, col, dx, dy in labs:
        az, alt = _azalt(*S[h][:2])
        x, y = _xy(az, alt)
        ax.scatter([x], [y], s=110, facecolors="none", edgecolors=col, lw=1.4, zorder=6)
        T(ax, x + dx, y + dy, tx(k), 11, col)
        T(ax, x + dx, y + dy - 0.016, tx("alt").format(alt), 8.5, WHITE, w="normal")
    # 地平線與方位
    ax.plot([x0, x1], [y0, y0], c="#48E39B", lw=2.2, zorder=6)
    ax.add_patch(Rectangle((x0, y0 - 0.05), x1 - x0, 0.05, fc="#05070F", ec="none", zorder=5))
    for az, k in ((90, "east"), (135, "se"), (180, "south")):
        x, _ = _xy(az, 0)
        ax.plot([x, x], [y0, y0 + 0.008], c="#48E39B", lw=2, zorder=7)
        T(ax, x, y0 - 0.022, tx(k), 14, "#48E39B")
    y = y0 - 0.075
    for k, col, sz in (("n1", GREEN, 13), ("n2", WHITE, 11.5), ("n3", WHITE, 11.5), ("n4", WHITE, 11.5)):
        T(ax, 0.5, y, tx(k), sz, col, w="bold" if k == "n1" else "normal")
        y -= 0.03
    T(ax, 0.5, y - 0.01, tx("n5"), 8.5, GREY, w="normal")


def run_all():
    C.emit("", [(k, c01(k)) for k in STAGE], title="C-A35-01_88個星座從哪來")
    C.emit("", [("長蛇", c02_hya), ("南十字", c02_cru)], title="C-A35-02_邊界是一塊地")
    C.emit("", [("三塊", c03_parts), ("89塊", c03_89)], title="C-A35-03_巨蛇被切成兩塊")
    for nm_, fn in (("C-A35-04_88星座出身表", c04_card), ("C-A35-05_今晚的巨蛇與盾牌", c05_card)):
        f, ax = C.newcard(dark=True)
        fn(ax)
        C.save(f, "", f"{nm_}_圖卡.png", transparent=False)
    # 每一階段各一張黑底預覽（QA 用；emit 的預覽只有最後的累計）
    for k in STAGE:
        f, ax = C.newfig(1.0, dark=True); c01(k)(ax)
        C.save(f, "", f"C-A35-01_88個星座從哪來_預覽-{k}_黑底.png", transparent=False)


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:                      # 英文版寫到 _概念圖/en/
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    run_all()


if __name__ == "__main__":
    main()
