# -*- coding: utf-8 -*-
"""A-10 東加｜概念圖 v2（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A10-01_東加地圖       → 逐字稿 02 鏡（島嶼層）、11 鏡（島嶼層→航線層）
  C-A10-02_Tafahi的翅膀   → 逐字稿 10 鏡（地平層→母雞層）
  C-A10-03_兩份東加星圖   → 逐字稿 15 鏡（9:16 對照表圖卡，可存圖）
輸出：05_素材/A-10_東加/_概念圖/

v1（2026/7，同檔名舊版）畫的是「三隻野鴨從同一個方位接力升起」：查證後不成立——
獵戶腰帶從正東升起（方位 90°），假十字、南十字從東南偏南升起（方位約 150°），三者不同方位；
「三隻野鴨」本身也是 Stellarium 的版本，Collocott 1922 的 Toloa 只指南十字。v2 全部重做。

來源：Collocott, E. E. V. 1922. Tongan Astronomy and Calendar. Bishop Museum Occasional Papers 8(4):157–173
      （星名幾乎全出自 Siaosi Tukuʻaho 的航海指南；Tukuʻaho 1890–93 任東加首相）；
      Stellarium skycultures/tongan（Dan Smale 提供；參考 Kik 1990、Fale 1990、Collocott）；
      Gifford, E. W. 1924. Tongan Myths and Tales（ʻAlotolu＝Hina 一家三人的船）。
      地圖＝經緯度實際位置（等距圓柱投影，島形示意）；距離為大圓距離（自算）；
      仰角、方位以 PyEphem 自算（Vavaʻu Neiafu 18.65°S、173.98°W，2026/11/13 21:48）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-10_東加/_概念圖")
C.set_base(OUT)
RED, GREY, SEA = "#FF6B6B", "#7C8BA8", "#2A4A7A"


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371.0 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) *
                                            math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


# ══════════════════════ C-A10-01 東加地圖 ══════════════════════
LONC, LATC, SC = -176.75, -17.4, 0.134
COSL = math.cos(math.radians(17.4))
P = {   # (lat, lon)
    "Tongatapu": (-21.14, -175.20), "ʻEua": (-21.38, -174.93), "Haʻapai": (-19.80, -174.35),
    "Vavaʻu": (-18.65, -173.98), "Niuatoputapu": (-15.96, -173.78), "Tafahi": (-15.85, -173.72),
    "Niuafoʻou": (-15.60, -175.63), "ʻAta": (-22.34, -176.20),
    "ʻUvea": (-13.28, -176.17), "Futuna": (-14.29, -178.12),
    "Savaiʻi": (-13.62, -172.45), "Upolu": (-13.92, -171.75),
    "Lakeba": (-18.20, -178.81), "Vanua Levu": (-16.60, 179.30),
}


def mp(lat, lon):
    lon = lon - 360.0 if lon > 0 else lon
    return (lon - LONC) * COSL * SC, (lat - LATC) * SC


def c01_islands(ax):
    T(ax, 0.0, 0.92, "東加王國：一百七十座左右的島", 31, WHITE)
    T(ax, 0.0, 0.845, "島的位置依實際經緯度；島形示意", 17, GREY, w="normal")
    for lat in (-14, -16, -18, -20, -22):
        a, b = mp(lat, -182.7), mp(lat, -170.8)
        ax.plot([a[0], b[0]], [a[1], a[1]], c=WHITE, lw=0.8, alpha=.18, ls=(0, (4, 5)), zorder=2)
        T(ax, a[0] - 0.01, a[1] + 0.022, f"{abs(lat)}°S", 11, GREY, w="normal", ha="left")
    big = {"Tongatapu": 420, "Vavaʻu": 300, "Haʻapai": 220, "ʻEua": 140, "Niuatoputapu": 160,
           "Tafahi": 90, "Niuafoʻou": 130, "ʻAta": 60, "ʻUvea": 200, "Futuna": 120,
           "Savaiʻi": 520, "Upolu": 460, "Lakeba": 120, "Vanua Levu": 700}
    tonga = {"Tongatapu", "ʻEua", "Haʻapai", "Vavaʻu", "Niuatoputapu", "Tafahi", "Niuafoʻou", "ʻAta"}
    for nm, (lat, lon) in P.items():
        x, y = mp(lat, lon)
        ax.scatter([x], [y], s=big[nm], c=AMBER if nm in tonga else GREY,
                   alpha=1 if nm in tonga else .8, zorder=8, lw=0)
    lab = {  # 名稱, dx, dy, 字級, 顏色, ha
        "Tongatapu": ("Tongatapu 東加本島", -0.05, -0.01, 17, WHITE, "right"),
        "ʻEua": ("ʻEua", 0.04, -0.03, 13, GREY, "left"),
        "Haʻapai": ("Haʻapai 群島", 0.05, 0.0, 16, WHITE, "left"),
        "Vavaʻu": ("Vavaʻu 群島", 0.05, 0.0, 17, WHITE, "left"),
        "Niuatoputapu": ("Niuatoputapu", 0.05, -0.035, 14, WHITE, "left"),
        "Tafahi": ("Tafahi", 0.04, 0.03, 16, AMBER, "left"),
        "Niuafoʻou": ("Niuafoʻou", 0.04, 0.0, 14, WHITE, "left"),
        "ʻAta": ("ʻAta", -0.035, 0.0, 12, GREY, "right"),
        "ʻUvea": ("ʻUvea（今法屬瓦利斯）", -0.04, 0.0, 15, WHITE, "right"),
        "Futuna": ("Futuna", 0.0, -0.045, 12, GREY, "center"),
        "Savaiʻi": ("薩摩亞", 0.03, 0.06, 15, GREY, "center"),
        "Upolu": ("", 0, 0, 1, GREY, "left"),
        "Lakeba": ("斐濟 Lau 群島", 0.0, -0.05, 13, GREY, "center"),
        "Vanua Levu": ("斐濟", 0.0, 0.05, 15, GREY, "center"),
    }
    for nm, (txt, dx, dy, fs, col, ha) in lab.items():
        if not txt:
            continue
        x, y = mp(*P[nm])
        T(ax, x + dx, y + dy, txt, fs, col, ha=ha, w="bold" if col == WHITE else "normal")
    # 南北跨度
    x = 0.80
    y1, y0 = mp(*P["Niuafoʻou"])[1], mp(*P["ʻAta"])[1]
    ax.plot([x, x], [y0, y1], c=AMBER, lw=1.6, alpha=.8)
    for yy in (y0, y1):
        ax.plot([x - 0.02, x + 0.02], [yy, yy], c=AMBER, lw=1.6, alpha=.8)
    km = gc_km(P["Niuafoʻou"], P["ʻAta"])
    ax.text(x + 0.045, (y0 + y1) / 2, f"南北約 {round(km, -1):.0f} 公里", fontproperties=C.FP,
            fontsize=15, color=AMBER, ha="center", va="center", rotation=90, weight="bold")
    # 比例尺
    sx0, sy = -0.80, -0.80
    L = 200 / 111.2 * SC * 1.0                 # 緯度 1° ≈ 111.2 km（南北向比例尺）
    ax.plot([sx0, sx0 + L], [sy, sy], c=WHITE, lw=2.0, alpha=.7)
    T(ax, sx0 + L / 2, sy + 0.035, "200 km", 12, GREY, w="normal")
    T(ax, 0.0, -0.92, "星名出處：Tukuʻaho 的航海指南（十九世紀末）→ Collocott 1922", 15, GREY,
      w="normal")


def wicon(ax, x, y, s, col):
    pts = [(-2, 0.6), (-1, -0.2), (0, 0.4), (1, -0.4), (2, 0.5)]
    xs = [x + p[0] * s for p in pts]; ys = [y + p[1] * s for p in pts]
    ax.plot(xs, ys, c=col, lw=1.8, alpha=.9, zorder=9)
    ax.scatter(xs, ys, s=28, c=WHITE, zorder=10)


def ringicon(ax, x, y, r, col):
    th = [math.radians(200 + i * 22) for i in range(7)]      # 北冕像一個沒合起來的圈
    xs = [x + r * math.cos(t) for t in th]; ys = [y + r * math.sin(t) for t in th]
    ax.plot(xs, ys, c=col, lw=1.8, alpha=.9, zorder=9)
    ax.scatter(xs, ys, s=24, c=WHITE, zorder=10)


def c01_routes(ax):
    for a, b, col, txt, dx, dy, ha in (
            ("Vavaʻu", "Tafahi", GREEN, "Kapakau ʻo Tafahi", 0.06, -0.02, "left"),
            ("Tongatapu", "ʻUvea", GREEN, "ʻAo ʻo ʻUvea", -0.05, 0.08, "right")):
        p0, p1 = mp(*P[a]), mp(*P[b])
        C.arrow(ax, p1, p0, c=col, lw=3.0, alpha=.95, style="-|>")
        km, br = gc_km(P[a], P[b]), bearing(P[a], P[b])
        dirn = "正北" if abs(((br + 180) % 360) - 180) < 1 else \
            (f"北偏西 {360 - br:.0f}°" if br > 180 else f"北偏東 {br:.0f}°")
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        T(ax, mx + dx, my + dy, txt, 17, col, ha=ha)
        T(ax, mx + dx, my + dy - 0.055, f"{km:.0f} km・{dirn}", 15, WHITE, w="normal", ha=ha)
    tx, ty = mp(*P["Tafahi"])
    wicon(ax, tx + 0.02, ty + 0.13, 0.025, GREEN)
    ux, uy = mp(*P["ʻUvea"])
    ringicon(ax, ux, uy + 0.12, 0.05, GREEN)


# ══════════════════════ C-A10-02 Tafahi 的翅膀 ══════════════════════
CAS = {"王良一 Caph": 746, "王良四 Schedar": 3179, "策 Navi": 4427, "閣道三 Ruchbah": 6686,
       "閣道二 Segin": 8886}
HZ, SD = -0.25, 0.042           # 地平線 y、每度（仰角／方位同比例）


def cas_altaz():
    import ephem
    S = G.load_stars(BASE)
    o = ephem.Observer(); o.lat, o.lon = "-18.6508", "-173.9832"; o.pressure = 0
    o.date = ephem.Date(ephem.Date("2026/11/13 21:48") - 13 * ephem.hour)
    out = {}
    for nm, h in CAS.items():
        ra, dec, v = S[h]
        b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec)
        b._epoch = ephem.J2000; b.compute(o)
        az = (math.degrees(b.az) + 180) % 360 - 180
        out[nm] = (math.degrees(b.alt), az, v)
    return out


ALTAZ = None


def xy(alt, az):
    return az * SD, HZ + alt * SD


def c02_horizon(ax):
    T(ax, 0.0, 0.92, "從 Vavaʻu 往北看", 32, WHITE)
    T(ax, 0.0, 0.845, "11 月中・晚上十點前後（2026/11/13 21:48）", 18, GREY, w="normal")
    ax.add_patch(C.Rectangle((-0.95, -0.95), 1.9, HZ + 0.95, fc=C.BG, ec="none", zorder=3))
    ax.plot([-0.94, 0.94], [HZ, HZ], c=WHITE, lw=2.2, alpha=.7, zorder=5)
    for k in range(3):
        C.water(ax, y=HZ - 0.07 - k * 0.07, x0=-0.94, x1=0.94, c=BLUE, rows=1,
                amp=0.010, freq=16 + 5 * k, phase=k * 1.3)
    for az in (-20, -10, 0, 10, 20):
        x = az * SD
        ax.plot([x, x], [HZ - 0.018, HZ + 0.018], c=WHITE, lw=1.4, alpha=.6, zorder=6)
        lab = "正北" if az == 0 else (f"北偏西 {-az}°" if az < 0 else f"北偏東 {az}°")
        T(ax, x, HZ - 0.33, lab, 14 if az else 17, WHITE if az == 0 else GREY,
          w="bold" if az == 0 else "normal")
    # Tafahi 的方向（312 km 外，海面以下看不到）
    br = bearing(P["Vavaʻu"], P["Tafahi"])
    x = br * SD
    ax.plot([x, x], [HZ, HZ + 0.70], c=AMBER, lw=1.4, ls=(0, (5, 5)), alpha=.55, zorder=6)
    ax.add_patch(C.Polygon([(x - 0.03, HZ - 0.005), (x + 0.03, HZ - 0.005), (x, HZ + 0.035)],
                           closed=True, fc=AMBER, ec="none", alpha=.9, zorder=7))
    T(ax, x + 0.04, HZ - 0.075, f"Tafahi 在這個方向（{gc_km(P['Vavaʻu'], P['Tafahi']):.0f} 公里外，看不到）",
      15, AMBER, ha="left")
    # 仰角尺
    for alt in (10, 20):
        y = HZ + alt * SD
        ax.plot([-0.93, -0.90], [y, y], c=WHITE, lw=1.2, alpha=.5)
        T(ax, -0.885, y, f"{alt}°", 12, GREY, w="normal", ha="left")
    ax.plot([-0.915, -0.915], [HZ, HZ + 22 * SD], c=WHITE, lw=1.0, alpha=.4)


def c02_hen(ax):
    pts = {nm: xy(alt, az) for nm, (alt, az, v) in ALTAZ.items()}
    order = ["閣道二 Segin", "閣道三 Ruchbah", "策 Navi", "王良四 Schedar", "王良一 Caph"]
    xs = [pts[n][0] for n in order]; ys = [pts[n][1] for n in order]
    # 翅膀：從中間的「策」往兩側張開（示意虛線）
    cx, cy = pts["策 Navi"]
    for side in (order[:2], order[3:]):
        far = pts[side[0] if side == order[:2] else side[-1]]
        mx, my = (cx + far[0]) / 2, max(cy, far[1]) + 0.22
        t = [i / 30 for i in range(31)]
        bx = [(1 - s) ** 2 * cx + 2 * (1 - s) * s * mx + s ** 2 * far[0] for s in t]
        by = [(1 - s) ** 2 * (cy + 0.02) + 2 * (1 - s) * s * my + s ** 2 * far[1] for s in t]
        ax.plot(bx, by, c=GREEN, lw=1.6, ls=(0, (4, 4)), alpha=.6, zorder=7)
    ax.plot(xs, ys, c=GREEN, lw=3.0, alpha=.95, zorder=8)
    for n in order:
        alt, az, v = ALTAZ[n]
        ax.scatter([pts[n][0]], [pts[n][1]], s=max(30, (6.0 - v) ** 2.2 * 22), c=WHITE, zorder=9,
                   lw=0)
    top = max(ys)
    T(ax, cx, top + 0.30, "Kapakau ʻo Tafahi", 26, GREEN)
    T(ax, cx, top + 0.225, "Tafahi 的翅膀", 19, GREEN, w="normal")
    lo, hi = min(a for a, _, _ in ALTAZ.values()), max(a for a, _, _ in ALTAZ.values())
    T(ax, max(xs) + 0.05, (min(ys) + max(ys)) / 2, f"高 {lo:.0f}–{hi:.0f}°", 16, WHITE, ha="left",
      w="normal")
    ax.add_patch(C.FancyBboxPatch((-0.86, -0.90), 1.72, 0.22,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=GREEN, lw=1.4, zorder=4))
    T(ax, 0.0, -0.745, "「像一隻母雞，張開翅膀孵在 Tafahi 上」", 19, WHITE)
    T(ax, 0.0, -0.835, "Collocott 1922 記為八顆星；是哪八顆說法不一，Stellarium 推測是仙后座", 13.5,
      GREY, w="normal")


# ══════════════════════ C-A10-03 兩份東加星圖（9:16 圖卡） ══════════════════════
ROWS = [  # 國際名, Collocott 1922, Stellarium, 是否對不上
    ("南十字", "Toloa 野鴨\n頭 γ、尾 α、兩翼 β δ", "Toloatonga\n南方的野鴨", True),
    ("南門二＋馬腹一", "Ongo Tangata 兩個人\n丟石頭砸傷鴨翅", "Fungasia\n土丘頂", True),
    ("南十字 ε 星", "Maka 石頭", "—", False),
    ("北河二＋北河三", "—", "Lua tangata\n兩個人", True),
    ("獵戶腰帶", "ʻAlotolu\n一船三人（Hina 的船）", "Toloa 野鴨", True),
    ("獵戶之劍", "Tuinga ika 一串魚", "Tuinga ika\n（連成腰帶＋劍）", False),
    ("假十字", "—", "Toloalahi 大野鴨", True),
    ("腰帶→假十字→南十字", "—", "Houmatoloa\n野鴨的岬角", True),
    ("昴宿星團", "Mataliki", "Motuliki", True),
    ("大／小麥哲倫雲", "Maʻafutoka 躺著的火＝大\nMaʻafulele 跑動的火＝小\n（大小對應是 Baker 說）", "對調；兩個名字\n另給老人星、天狼星", True),
    ("（北方五顆星）", "Tuʻulalupe 鴿子的棲架\n直立才能用", "畢宿", False),
    ("（圓形星群）", "ʻAo ʻo ʻUvea ʻUvea 的圓環\n戴在 ʻUvea 上空才用", "北冕座（推測）", False),
    ("（八顆星）", "Kapakau ʻo Tafahi\n孵在 Tafahi 上的翅膀", "仙后座（推測）", False),
]


def c03_card(ax):
    ax.text(0.5, 0.945, "同一片東加星空，兩份紀錄", fontproperties=C.FP, fontsize=27, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.905, "Collocott 1922（Tukuʻaho 航海指南）vs Stellarium", fontproperties=C.FP,
            fontsize=13.5, color=GREY, ha="center", va="center")
    X0, X1, X2 = 0.035, 0.30, 0.665
    y = 0.862
    for x, txt, col in ((X0, "星", GREY), (X1, "Collocott 1922", AMBER), (X2, "Stellarium", PURPLE)):
        ax.text(x, y, txt, fontproperties=C.FP, fontsize=14, color=col, ha="left", va="center",
                weight="bold")
    ax.plot([0.03, 0.97], [0.845, 0.845], c=WHITE, lw=1.0, alpha=.4)
    y = 0.825
    for star, col_c, col_s, diff in ROWS:
        n = max(col_c.count("\n"), col_s.count("\n")) + 1
        h = 0.022 * n + 0.012
        yc = y - h / 2
        if diff:
            ax.add_patch(C.Rectangle((0.03, y - h + 0.004), 0.94, h - 0.006, fc="#2A1E3F",
                                     ec="none", alpha=.85, zorder=0))
        ax.text(X0, yc, star, fontproperties=C.FP, fontsize=12.5, color=WHITE, ha="left",
                va="center")
        ax.text(X1, yc, col_c, fontproperties=C.FP, fontsize=12.5, color=AMBER, ha="left",
                va="center", linespacing=1.25)
        ax.text(X2, yc, col_s, fontproperties=C.FP, fontsize=12.5, color=PURPLE, ha="left",
                va="center", linespacing=1.25)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.add_patch(C.Rectangle((0.035, y - 0.034), 0.03, 0.018, fc="#2A1E3F", ec="none"))
    ax.text(0.075, y - 0.025, "＝兩份對不上", fontproperties=C.FP, fontsize=11.5, color=GREY,
            ha="left", va="center")
    ax.text(0.5, 0.075, "Stellarium 另參考 Kik 1990、Fale 1990；東加各群島叫法本來就不同",
            fontproperties=C.FP, fontsize=11.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.040, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


def main():
    global ALTAZ
    os.makedirs(OUT, exist_ok=True)
    ALTAZ = cas_altaz()
    for nm, (alt, az, v) in ALTAZ.items():
        print(f"  {nm}: 高 {alt:.1f}°、方位 {az:+.1f}°")
    print(f"  Vavaʻu→Tafahi {gc_km(P['Vavaʻu'], P['Tafahi']):.0f} km、{bearing(P['Vavaʻu'], P['Tafahi']):.1f}°；"
          f"Tongatapu→ʻUvea {gc_km(P['Tongatapu'], P['ʻUvea']):.0f} km、{bearing(P['Tongatapu'], P['ʻUvea']):.1f}°")
    C.emit("", [("島嶼", c01_islands), ("航線", c01_routes)], title="C-A10-01_東加地圖")
    C.emit("", [("地平", c02_horizon), ("母雞", c02_hen)], title="C-A10-02_Tafahi的翅膀")
    f, ax = C.newcard(dark=True)
    c03_card(ax)
    C.save(f, "", "C-A10-03_兩份東加星圖_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
