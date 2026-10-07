# -*- coding: utf-8 -*-
"""X-01 昴宿環球之旅：概念圖（C 系列骨架）

C-X01-01 七還是六（星點層、星等層、傳說層）
C-X01-02 太平洋的同一個字（9:16 圖卡）
C-X01-03 黎明重現（年輪層、黎明層）
C-X01-04 黃昏升起（年輪層、黃昏層）
C-X01-05 昴宿的真身（數字層、距離層、年齡層）
C-X01-06 七姊妹的一百個名字（9:16 圖卡）
C-X01-07 今晚往東看（9:16 圖卡；台北 2026/11/27 19:00）

天象（黎明重現／黃昏升起日期、台北方位高度、月掩昴）全部用 PyEphem 自算（氣壓 1010 hPa，含折射）。
來源：Stellarium skycultures（新舊兩版 index.json／description）；Hesiod《工作與時日》383–384；
      Melis et al. 2014（VLBI 136.2 pc）；Hipparcos 1997（約 120 pc）；POLLEX *mata-liki。
執行：python3 make_x01_diagrams.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_x01_v4 as X1

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-01_昴宿環球/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
S = None
TPE = ("25.0330", "121.5654")
NAMES = {X1.ALCYONE: ("Alcyone", "昴宿六"), X1.ATLAS: ("Atlas", "昴宿七"), X1.ELECTRA: ("Electra", "昴宿一"),
         X1.MAIA: ("Maia", "昴宿四"), X1.MEROPE: ("Merope", "昴宿五"), X1.TAYGETA: ("Taygeta", "昴宿二"),
         X1.PLEIONE: ("Pleione", "昴宿增十二"), X1.CELAENO: ("Celaeno", "昴宿增九"),
         X1.ASTEROPE: ("Asterope", "昴宿三")}


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va="center", weight=w, zorder=z)


def body(ra, dec):
    import ephem
    b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec); b._epoch = ephem.J2000
    return b


def observer(lat, lon):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.pressure = 1010
    return o


# ══════════════════════ 天象計算 ══════════════════════
def season_dates(lat, lon, tz, year=2026):
    """黎明重現（太陽 −10° 時昴宿 ≥ 5°，第一天）、黃昏升起（昴宿在日落前升起，第一天）、
    黃昏最後一見（太陽 −10° 時昴宿在西方 ≥ 5°，最後一天）"""
    import ephem
    o = observer(lat, lon); sun = ephem.Sun(); ple = body(*X1.M45)
    hel = acr = last = None
    d0 = ephem.Date(f"{year}/01/01")
    for k in range(366):
        day = ephem.Date(d0 + k)
        noon = ephem.Date(day + (12 - tz) / 24.0)
        o.date = noon
        ss = o.next_setting(sun)
        o.date = ephem.Date(ss - 0.5); rr = o.next_rising(ple)
        if acr is None and k > 200 and rr <= ss:
            acr = day
        o.horizon = "-10"
        o.date = ephem.Date(noon - 0.5)
        try:
            dawn = o.next_rising(sun, use_center=True)
            o.date = noon
            dusk = o.next_setting(sun, use_center=True)
        except Exception:
            dawn = dusk = None
        o.horizon = "0"
        if dawn and hel is None and k > 120:
            o.date = dawn; ple.compute(o)
            if math.degrees(ple.alt) >= 5:
                hel = day
        if dusk and 60 < k < 150:
            o.date = dusk; ple.compute(o)
            if math.degrees(ple.alt) >= 5 and math.degrees(ple.az) > 180:
                last = day
    return hel, acr, last


def doy(d):
    import ephem
    y, m, dd = ephem.Date(d).triple()[:3]
    import datetime
    return datetime.date(int(y), int(m), int(dd)).timetuple().tm_yday


# ══════════════════════ C-X01-01 七還是六 ══════════════════════
def p1(ra, dec):
    """星團切平面（東在左）；中心 M45；1° ≈ 1.1 畫布單位"""
    ra0, dec0 = 56.85, 24.20
    x = -(ra - ra0) * math.cos(math.radians(dec0)) * 0.85
    y = (dec - dec0) * 0.85
    return x, 0.44 + y


def c01_stars(ax):
    T(ax, 0.0, 0.92, "七姊妹，為什麼大多只看到六顆？", 29, WHITE)
    T(ax, 0.0, 0.845, "昴宿星團最亮的九顆（Hipparcos 星等；東在左、北在上）", 15, GREY, w="normal")
    import numpy as np
    for ra, dec, v in X1.cluster_stars(S, *X1.M45, 1.3, 8.0):
        x, y = p1(ra, dec)
        if abs(x) < 0.95 and 0.12 < y < 0.76 and v > 5.8:
            ax.scatter([x], [y], s=max(2, (8.2 - v) * 3), c=MW, alpha=.5, lw=0, zorder=4)
    off = {X1.ALCYONE: (0.0, -0.075), X1.ATLAS: (-0.07, -0.04), X1.PLEIONE: (-0.07, 0.04),
           X1.ELECTRA: (0.07, -0.02), X1.CELAENO: (0.07, 0.03), X1.MAIA: (0.0, -0.065),
           X1.TAYGETA: (0.07, 0.03), X1.ASTEROPE: (0.0, 0.06), X1.MEROPE: (0.0, -0.065)}
    for h, (gr, zh) in NAMES.items():
        ra, dec, v = S[h]
        x, y = p1(ra, dec)
        ax.scatter([x], [y], s=max(25, (6.3 - v) ** 2.4 * 55), c=WHITE if v < 4.5 else BLUE, zorder=6, lw=0)
        dx, dy = off[h]
        ha = "center" if dx == 0 else ("right" if dx < 0 else "left")
        ctext(ax, x + dx, y + dy + 0.012, gr, 12.5, WHITE if v < 4.5 else BLUE, w="normal", ha=ha)
        ctext(ax, x + dx, y + dy - 0.022, zh, 10.5, GREY, w="normal", ha=ha)


def c01_mag(ax):
    y0, x0, x1 = -0.27, -0.82, 0.82
    vmin, vmax = 2.5, 6.3
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    for v0, v1, lab, col in ((2.5, 4.0, "城市裡\n約 4 等以內", "#3A4466"), (4.0, 5.0, "郊區\n約 5 等", "#2C3556"),
                             (5.0, 6.3, "很暗的山上\n約 6 等", "#222A46")):
        ax.add_patch(CB.Rectangle((X(v0), y0 - 0.04), X(v1) - X(v0), 0.08, fc=col, ec="none", zorder=3))
        ax.text((X(v0) + X(v1)) / 2, y0 - 0.075, lab, fontproperties=CB.FP, fontsize=11, color=GREY,
                ha="center", va="top", zorder=5, linespacing=1.25)
    ax.plot([x0, x1], [y0, y0], c=WHITE, lw=1.6, alpha=.6, zorder=4)
    ctext(ax, x0 - 0.04, y0, "亮", 13, WHITE, ha="right")
    ctext(ax, x1 + 0.04, y0, "暗", 13, GREY, ha="left")
    for v in (3, 4, 5, 6):
        ax.plot([X(v), X(v)], [y0 - 0.015, y0 + 0.015], c=WHITE, lw=1.2, alpha=.6, zorder=4)
        ctext(ax, X(v), y0 - 0.025, f"{v}", 9.5, GREY, w="normal")
    tier = {X1.ALCYONE: 0, X1.ATLAS: 0, X1.ELECTRA: 1, X1.MAIA: 2, X1.MEROPE: 0, X1.TAYGETA: 1,
            X1.PLEIONE: 0, X1.CELAENO: 1, X1.ASTEROPE: 0}
    for h, (gr, zh) in NAMES.items():
        v = S[h][2]
        ax.scatter([X(v)], [y0], s=max(25, (6.3 - v) ** 2.4 * 40), c=WHITE if v < 4.5 else BLUE,
                   zorder=6, lw=0)
        yy = y0 + 0.085 + 0.055 * tier[h]
        ax.plot([X(v), X(v)], [y0 + 0.025, yy - 0.018], c=WHITE, lw=0.8, alpha=.4, zorder=4)
        ctext(ax, X(v), yy, f"{gr} {v:.1f}", 10.5, WHITE if v < 4.5 else BLUE, w="normal")
    ax.plot([X(4.6), X(4.6)], [y0 - 0.05, y0 + 0.25], c=AMBER, lw=2.0, ls=(0, (4, 3)), zorder=5)
    ctext(ax, X(4.6) - 0.02, y0 + 0.27, "← 這六顆都在 4.3 等以內", 13, AMBER, ha="right")
    ctext(ax, X(4.6) + 0.02, y0 + 0.27, "第七亮只有 5.1 等 →", 13, BLUE, ha="left")


def c01_legend(ax):
    box(ax, -0.92, -0.94, 1.84, 0.42, ec=PURPLE)
    ctext(ax, 0.0, -0.56, "名字裡常是七，看見的常是六", 16, PURPLE)
    rows = [("澳洲・卡米拉羅伊", "七姊妹 Miyay Miyay 裡有一個害羞，躲起來了"),
            ("北美・黑腳族", "六個沒人照顧的孩子 Lost Children"),
            ("名字裡的七", "希臘七姊妹、滿族七少女、布吉斯 Bintoéng Pitu（七星）"),
            ("", "巴比倫 MUL.MUL 也和「七神」連在一起")]
    for i, (a, b) in enumerate(rows):
        y = -0.63 - i * 0.068
        if a:
            ctext(ax, -0.86, y, a, 13, PURPLE, ha="left")
        ctext(ax, -0.40, y, b, 13, WHITE, w="normal", ha="left")
    ctext(ax, 0.0, -0.905, "說法：Stellarium skycultures（kamilaroi、blackfoot、chinese_manchu、bugis、babylonian）", 9.5,
          GREY, w="normal")


# ══════════════════════ C-X01-02 太平洋的同一個字（9:16） ══════════════════════
def c02_card(ax):
    ctext(ax, 0.5, 0.955, "太平洋的同一個字", 30, WHITE)
    ctext(ax, 0.5, 0.918, "玻里尼西亞各島叫昴宿的名字", 14, GREY, w="normal")
    rows = [("毛利（紐西蘭）", "Matariki", "六、七月黎明重現＝新年（2022 年起國定假日）"),
            ("阿努塔（所羅門群島）", "Matariki", "Stellarium：小臉、小眼睛"),
            ("大溪地", "Matariʻi", "小眼睛；11–5 月是 Matariʻi i niʻa 豐收季"),
            ("薩摩亞", "Matāliʻi", "Liʻi 的臉；黃昏升起＝新年"),
            ("東加", "Mataliki", "Stellarium 名稱表寫 Motuliki，說明文寫 Mataliki"),
            ("夏威夷", "Makaliʻi", "Stellarium：酋長之眼；黃昏升起＝Makahiki 新年")]
    y = 0.885
    for isl, word, note in rows:
        ax.plot([0.04, 0.96], [y, y], c=WHITE, lw=0.6, alpha=.2)
        ctext(ax, 0.06, y - 0.022, isl, 12.5, GREY, w="normal", ha="left")
        ctext(ax, 0.94, y - 0.03, word, 24, BLUE, ha="right")
        ctext(ax, 0.06, y - 0.055, note, 11, WHITE, w="normal", ha="left")
        y -= 0.078
    ax.plot([0.04, 0.96], [y, y], c=WHITE, lw=0.6, alpha=.2)
    ctext(ax, 0.5, 0.375, "還原成同一個古字（mata＝眼睛、臉）", 14, AMBER)
    ctext(ax, 0.5, 0.320, "mata  ＋  liki", 32, AMBER)
    box(ax, 0.06, 0.160, 0.42, 0.105, ec=BLUE)
    box(ax, 0.52, 0.160, 0.42, 0.105, ec=PURPLE)
    ctext(ax, 0.27, 0.238, "一說：liki＝小", 13, BLUE)
    ctext(ax, 0.27, 0.188, "「小小的眼睛」", 15, WHITE)
    ctext(ax, 0.73, 0.238, "一說：ariki＝首領", 13, PURPLE)
    ctext(ax, 0.73, 0.188, "「首領（神）的眼睛」", 15, WHITE)
    ctext(ax, 0.5, 0.128, "語言學界還沒定論", 12.5, GREY, w="normal")
    ctext(ax, 0.5, 0.093, "毛利、大溪地念 r；薩摩亞、東加、夏威夷念 l；夏威夷再把 t 念成 k", 11, WHITE, w="normal")
    ctext(ax, 0.5, 0.058, "Stellarium：maori／anutan／ruanui（大溪地）／samoan／tongan／hawaiian_starlines；POLLEX *mata-liki",
          8.5, GREY, w="normal")
    ctext(ax, 0.5, 0.025, "#萬國星空　#師大天文社", 13, WHITE, w="normal")


# ══════════════════════ C-X01-03／04 年輪 ══════════════════════
MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
RING_C, RING_R = (0.0, 0.20), 0.40


def ang(day):
    """一年 → 角度：1/1 在正上方，順時針"""
    return math.pi / 2 - 2 * math.pi * (day - 1) / 365.0


def rp(day, r):
    a = ang(day)
    return RING_C[0] + r * math.cos(a), RING_C[1] + r * math.sin(a)


def ring(ax, title, sub, dates):
    import numpy as np
    hel, acr, last = dates
    T(ax, 0.0, 0.92, title, 30, WHITE)
    T(ax, 0.0, 0.845, sub, 15, GREY, w="normal")
    th = np.linspace(0, 2 * math.pi, 361)
    ax.plot(RING_C[0] + RING_R * np.cos(th), RING_C[1] + RING_R * np.sin(th), c=WHITE, lw=2.0, alpha=.5, zorder=3)
    cum = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    for i, d in enumerate(cum):
        x0, y0 = rp(d, RING_R - 0.03); x1, y1 = rp(d, RING_R + 0.03)
        ax.plot([x0, x1], [y0, y1], c=WHITE, lw=1.2, alpha=.5, zorder=3)
        mx, my = rp(d + 15, RING_R - 0.09)
        ctext(ax, mx, my, MONTHS[i], 12, GREY, w="normal")
    # 看不見的一段（太陽旁邊）
    a0, a1 = doy(last) + 1, doy(hel) - 1
    arc = np.linspace(ang(a0), ang(a1), 60)
    ax.plot(RING_C[0] + RING_R * np.cos(arc), RING_C[1] + RING_R * np.sin(arc), c=GREY, lw=10, alpha=.35,
            solid_capstyle="round", zorder=4)
    mx, my = rp((a0 + a1) / 2 - 6, RING_R + 0.24)
    ctext(ax, mx, my, f"看不見\n約 {a1 - a0 + 1} 天\n（躲在太陽旁）", 11, GREY, w="normal")
    ctext(ax, RING_C[0], RING_C[1] + 0.03, "昴宿", 22, WHITE)
    ctext(ax, RING_C[0], RING_C[1] - 0.04, "的一年", 14, GREY, w="normal")


def mark(ax, day, col, lab, sub):
    import numpy as np
    x, y = rp(day, RING_R)
    ax.scatter([x], [y], s=260, c=col, zorder=7, lw=0)
    ax.scatter([x], [y], s=900, c=col, alpha=.2, zorder=6, lw=0)
    lx, ly = rp(day, RING_R + 0.17)
    ctext(ax, lx, ly + 0.02, lab, 15, col)
    ctext(ax, lx, ly - 0.03, sub, 11, WHITE, w="normal")


DATES = None


def c03_ring(ax):
    ring(ax, "每年六月：黎明前重新出現", "昴宿躲在太陽旁邊約一個多月，再出現時是在天亮前的東方", DATES)


def c03_dawn(ax):
    hel = DATES[0]
    mark(ax, doy(hel), AMBER, "黎明重現", f"台北約 {int(ephem_month(hel))}/{int(ephem_day(hel))}")
    box(ax, -0.94, -0.94, 1.88, 0.40, ec=AMBER)
    rows = [("紐西蘭・毛利", "Matariki 新年（六、七月；2022 年起國定假日，2026 年是 7/10）"),
            ("南美・洛科諾", "六月第一次在東方出現＝新的一年開始"),
            ("南非・祖魯、科薩", "isiLimela「挖土的星」：清晨看見它，就該播種"),
            ("阿拉伯", "al-Thurayya 六月初在黎明升起（月站第三宿）"),
            ("希臘・赫西俄德", "昴升起（當時在五月）→ 開始收割")]
    for i, (a, b) in enumerate(rows):
        y = -0.59 - i * 0.066
        ctext(ax, -0.89, y, a, 12.5, AMBER, ha="left")
        ctext(ax, -0.42, y, b, 12.5, WHITE, w="normal", ha="left")


def c04_ring(ax):
    ring(ax, "每年十一月：黃昏從東方升起", "太陽一落下，昴宿就從東方地平線冒出來，整夜都在天上", DATES)


def c04_dusk(ax):
    acr = DATES[1]
    mark(ax, doy(acr), BLUE, "黃昏升起", f"台北約 {int(ephem_month(acr))}/{int(ephem_day(acr))}")
    box(ax, -0.94, -0.94, 1.88, 0.40, ec=BLUE)
    rows = [("夏威夷", "Makaliʻi 黃昏東升＝Makahiki 新年（約十一月中到一、二月）"),
            ("大溪地", "Matariʻi i niʻa：十一月到五月，豐收的季節"),
            ("薩摩亞", "Matāliʻi 黃昏升起＝新年、第一批收成"),
            ("亞馬遜・提庫納", "十一月底黃昏重現 → 估今年的雨有多大"),
            ("滿族・希臘", "七少女黃昏東升＝入冬；赫西俄德：昴清晨西沉 → 犁田")]
    for i, (a, b) in enumerate(rows):
        y = -0.59 - i * 0.066
        ctext(ax, -0.89, y, a, 12.5, BLUE, ha="left")
        ctext(ax, -0.50, y, b, 12.5, WHITE, w="normal", ha="left")


def ephem_month(d):
    import ephem
    return ephem.Date(d).triple()[1]


def ephem_day(d):
    import ephem
    return ephem.Date(d).triple()[2]


# ══════════════════════ C-X01-05 昴宿的真身 ══════════════════════
def c05_numbers(ax):
    T(ax, 0.0, 0.92, "昴宿星團的真身", 30, WHITE)
    T(ax, 0.0, 0.845, "肉眼六、七顆，望遠鏡裡是一整窩年輕的星", 15, GREY, w="normal")
    for x, big, small, col in ((-0.60, "1,000+", "顆星（蓋亞衛星）", AMBER), (0.0, "約 1 億", "歲（恐龍時代誕生）", GREEN),
                               (0.60, "約 444", "光年", BLUE)):
        box(ax, x - 0.27, 0.48, 0.54, 0.27, ec=col)
        ctext(ax, x, 0.645, big, 30, col)
        ctext(ax, x, 0.54, small, 13, WHITE, w="normal")


def c05_distance(ax):
    y0, x0, x1 = 0.17, -0.85, 0.85
    X = lambda ly: x0 + ly / 500.0 * (x1 - x0)
    ctext(ax, -0.85, 0.37, "距離：吵了十七年", 17, WHITE, ha="left")
    ax.plot([x0, x1], [y0, y0], c=WHITE, lw=1.6, alpha=.6)
    for ly in (0, 100, 200, 300, 400, 500):
        ax.plot([X(ly), X(ly)], [y0 - 0.015, y0 + 0.015], c=WHITE, lw=1.2, alpha=.6)
        ctext(ax, X(ly), y0 - 0.045, f"{ly}", 10.5, GREY, w="normal")
    ctext(ax, x1 + 0.02, y0 - 0.085, "光年", 10.5, GREY, w="normal", ha="right")
    ax.scatter([X(0)], [y0], s=140, c=AMBER, zorder=6, lw=0)
    ctext(ax, X(0), y0 + 0.05, "地球", 12, AMBER)
    ax.scatter([X(392)], [y0], s=180, c=RED, zorder=6, lw=0)
    ax.plot([X(392), X(392)], [y0 - 0.02, y0 - 0.10], c=RED, lw=1.2, alpha=.7)
    ctext(ax, X(392) - 0.02, y0 - 0.125, "依巴谷衛星（1997）：約 392 光年", 12, RED, ha="right")
    ax.scatter([X(444)], [y0], s=180, c=BLUE, zorder=6, lw=0)
    ax.plot([X(444), X(444)], [y0 + 0.02, y0 + 0.10], c=BLUE, lw=1.2, alpha=.7)
    ctext(ax, X(444) + 0.03, y0 + 0.13, "電波望遠鏡 VLBI（2014）、蓋亞衛星：約 444 光年", 12, BLUE, ha="right")
    ctext(ax, 0.0, -0.03, "差了一成多。天文學家一度懷疑「年輕的星有我們不懂的物理」——最後證明是依巴谷的系統誤差", 11.5,
          GREY, w="normal")


def c05_age(ax):
    y0, x0, x1 = -0.40, -0.85, 0.85
    ctext(ax, -0.85, -0.17, "年紀：太陽的四十幾分之一", 17, WHITE, ha="left")
    X = lambda myr: x1 - myr / 4600.0 * (x1 - x0)
    ax.plot([x0, x1], [y0, y0], c=WHITE, lw=1.6, alpha=.6)
    for myr, lab in ((4600, "46 億年前"), (3000, "30 億"), (1000, "10 億"), (0, "現在")):
        ax.plot([X(myr), X(myr)], [y0 - 0.015, y0 + 0.015], c=WHITE, lw=1.2, alpha=.6)
        ctext(ax, X(myr), y0 - 0.05, lab, 11, GREY, w="normal")
    ax.scatter([X(4600)], [y0], s=220, c=AMBER, zorder=6, lw=0)
    ctext(ax, X(4600), y0 + 0.07, "太陽誕生", 13, AMBER)
    ax.scatter([X(100)], [y0], s=220, c=BLUE, zorder=6, lw=0)
    ctext(ax, X(100) - 0.02, y0 + 0.07, "昴宿誕生（約 1 億年前）", 13, BLUE, ha="right")
    ax.add_patch(CB.Rectangle((X(145), y0 - 0.03), X(66) - X(145), 0.06, fc=GREEN, ec="none", alpha=.6, zorder=5))
    ctext(ax, X(100) - 0.02, y0 - 0.11, "白堊紀（恐龍還在）", 12, GREEN, w="normal", ha="right")
    box(ax, -0.92, -0.93, 1.84, 0.30, ec=GREY)
    ctext(ax, 0.0, -0.70, "最亮的幾顆是又熱又藍的 B 型星；四周的藍色雲氣（梅洛普星雲）", 12.5, WHITE, w="normal")
    ctext(ax, 0.0, -0.765, "不是生它的雲，是它正好穿過的一片塵埃", 12.5, WHITE, w="normal")
    ctext(ax, 0.0, -0.86, "數字：Melis et al. 2014（VLBI 136.2 pc）；Hipparcos 1997；年齡約 1–1.25 億年", 9.5, GREY,
          w="normal")


# ══════════════════════ C-X01-06 七姊妹的一百個名字（9:16） ══════════════════════
FAM = [
    ("女孩・姊妹・孩子", PURPLE, [("Pleiades", "七姊妹（希臘）"), ("Miyay Miyay", "七姊妹（卡米拉羅伊）"),
                           ("Lamankurrk", "女孩們（澳洲布朗）"), ("Nadan Narhū", "七少女（滿族）"),
                           ("al-Thurayya", "一位女子（阿拉伯）"), ("Kṛttikā", "戰神的乳母（印度）"),
                           ("天神的女兒", "南非那馬人"), ("Lost Children", "迷途的孩子（黑腳族）"),
                           ("Lapnuman", "男孩、女孩（萬那杜）")]),
    ("小小的眼睛", BLUE, [("Matariki", "毛利、阿努塔"), ("Matariʻi", "大溪地"), ("Matāliʻi", "薩摩亞"),
                     ("Mataliki", "東加"), ("Makaliʻi", "夏威夷")]),
    ("雞、窩、一群動物", GREEN, [("昴日雞", "中國二十八禽"), ("Cloșca cu pui", "母雞帶小雞（羅馬尼亞）"),
                          ("Квачка", "母雞（馬其頓）"), ("Куркі", "母雞（白俄羅斯）"),
                          ("Утиное гнездо", "鴨巢（西伯利亞）"), ("Eixu", "黃蜂窩（巴西圖皮）"),
                          ("Baweta", "一群烏龜（提庫納）"), ("Rougot", "狗群（薩米）"),
                          ("Flock", "一群（古埃及）")]),
    ("一束・一群", AMBER, [("すばる", "束成一把（日本）"), ("S'Udrone", "一串（薩丁尼亞）"),
                      ("Tianquiztli", "市集（阿茲特克）"), ("Yôkoro wiwa", "成群的星（洛科諾）"),
                      ("Nhorkoatero", "星群（圖卡諾）"), ("Worong-porongngé", "一團（布吉斯）")]),
    ("一撮頭髮", RED, [("昴＝髦頭", "《史記．天官書》"), ("zappu", "鬃毛（巴比倫）"),
                   ("Worong-mpolong", "一撮毛（布吉斯）")]),
    ("其他", WHITE, [("Sakiattiak", "胸骨（因紐特）"), ("isiLimela", "挖土的星（祖魯）"),
                   ("Dilyéhé", "（北美納瓦荷）"), ("Bittoéng Malunus", "飛魚季記號（曼達）")]),
]


def c06_card(ax):
    n = sum(len(r) for _, _, r in FAM)
    ctext(ax, 0.5, 0.958, "七姊妹的一百個名字", 28, WHITE)
    ctext(ax, 0.5, 0.925, f"這裡先收 {n} 個（Stellarium skycultures）", 13, GREY, w="normal")
    cols = {0: [0, 1, 4], 1: [2, 3, 5]}
    for c, idx in cols.items():
        x0 = 0.03 + 0.49 * c
        y = 0.895
        for i in idx:
            title, col, rows = FAM[i]
            ax.plot([x0, x0 + 0.455], [y, y], c=WHITE, lw=0.8, alpha=.35)
            ctext(ax, x0 + 0.01, y - 0.017, title, 12.5, col, ha="left")
            y -= 0.038
            for nat, zh in rows:
                ctext(ax, x0 + 0.015, y, nat, 9.5, col, ha="left")
                ctext(ax, x0 + 0.225, y, zh, 10, WHITE, w="normal", ha="left")
                y -= 0.0245
            y -= 0.012
    ctext(ax, 0.5, 0.062, "「一百」是個大概——光 Stellarium 新舊兩版，就有四十多個文化替它取了名字", 9.5, GREY,
          w="normal")
    ctext(ax, 0.5, 0.027, "#萬國星空　#師大天文社", 13, WHITE, w="normal")


# ══════════════════════ C-X01-07 今晚往東看（9:16） ══════════════════════
WHEN7 = "2026/11/27 19:00"
AZ7, ALT7, K7, XC7, YC7 = 72.0, 34.0, 0.47 / (2 * math.tan(math.radians(25))), 0.5, 0.47
ASP = 1215 / 2160


def proj7(alt, az):
    a, z = math.radians(alt), math.radians(az)
    v = (math.cos(a) * math.sin(z), math.cos(a) * math.cos(z), math.sin(a))
    a0, z0 = math.radians(ALT7), math.radians(AZ7)
    c = (math.cos(a0) * math.sin(z0), math.cos(a0) * math.cos(z0), math.sin(a0))
    e = (math.cos(z0), -math.sin(z0), 0.0)
    u = (-math.sin(a0) * math.sin(z0), -math.sin(a0) * math.cos(z0), math.cos(a0))
    d = sum(p * q for p, q in zip(v, c))
    if d <= -0.2:
        return None
    X = sum(p * q for p, q in zip(v, e)) * 2 / (1 + d)
    Y = sum(p * q for p, q in zip(v, u)) * 2 / (1 + d)
    return XC7 + X * K7, YC7 + Y * K7 * ASP


def altaz_at(when_local, tz=8):
    import ephem
    o = observer(*TPE)
    o.date = ephem.Date(ephem.Date(when_local) - tz * ephem.hour)

    def f(ra, dec):
        b = body(ra, dec); b.compute(o)
        return math.degrees(b.alt), math.degrees(b.az)
    return f


def c07_card(ax):
    f = altaz_at(WHEN7)
    ctext(ax, 0.5, 0.955, "今晚往東看", 30, WHITE)
    ctext(ax, 0.5, 0.918, "台北　2026/11/27（五）晚上 7:00", 14, GREY, w="normal")
    ok = lambda q: q and 0.02 < q[0] < 0.98 and 0.235 < q[1] < 0.89
    hz = [q for q in (proj7(0, az) for az in range(0, 151, 2)) if q]
    ax.plot([q[0] for q in hz], [q[1] for q in hz], c=WHITE, lw=2.0, alpha=.8, zorder=5)
    y_h = min(q[1] for q in hz)
    ax.add_patch(CB.Rectangle((0, 0), 1, y_h, fc="#141A2E", ec="none", zorder=4))
    poly = [(q[0], q[1]) for q in hz] + [(hz[-1][0], 0), (hz[0][0], 0)]
    ax.add_patch(CB.Polygon(poly, closed=True, fc="#141A2E", ec="none", zorder=4))
    for az, lab in ((22.5, "北北東"), (45, "東北"), (67.5, "東北東"), (90, "東"), (112.5, "東南東")):
        q = proj7(0, az)
        if q and 0.04 < q[0] < 0.96:
            ctext(ax, q[0], q[1] - 0.018, lab, 12 if az != 67.5 else 15, WHITE)
    for alt in (30, 60):
        arc = [q for q in (proj7(alt, az) for az in range(0, 151, 2)) if ok(q)]
        ax.plot([q[0] for q in arc], [q[1] for q in arc], c=WHITE, lw=0.8, alpha=.25, ls=(0, (3, 4)), zorder=3)
        if arc:
            ax.text(arc[-1][0] - 0.01, arc[-1][1] + 0.008, f"{alt}°", fontproperties=CB.FP, fontsize=9,
                    color=GREY, ha="right", va="bottom", zorder=3)
    pos = {}
    for h, (ra, dec, v) in S.items():
        if v > 4.6:
            continue
        alt, az = f(ra, dec)
        if alt < 0:
            continue
        q = proj7(alt, az)
        if ok(q):
            pos[h] = q
            ax.scatter([q[0]], [q[1]], s=max(1.2, max(0.0, 6.0 - v) ** 2.2 * 3.2), c=WHITE, zorder=7, lw=0)
    for segs in X1.W["Tau"] + X1.W["Ori"]:
        for a, b in zip(segs, segs[1:]):
            if a in pos and b in pos:
                ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=WHITE, lw=1.0, alpha=.35, zorder=6)
    alt, az = f(*X1.M45)
    q = proj7(alt, az)
    ax.add_patch(CB.Circle(q, 0.035, fc="none", ec=AMBER, lw=2.2, zorder=8))
    ctext(ax, q[0] + 0.05, q[1] + 0.012, "昴宿星團", 16, AMBER, ha="left")
    ctext(ax, q[0] + 0.05, q[1] - 0.018, f"高 {alt:.0f}°", 11, WHITE, w="normal", ha="left")
    for h, lab, dx, dy in ((X1.ALDEBARAN, "畢宿五（紅）", 0.0, -0.02), (24608, "五車二", 0.0, -0.02),
                           (X1.BETELGEUSE, "參宿四", 0.0, 0.02)):
        if h in pos:
            ctext(ax, pos[h][0] + dx, pos[h][1] + dy, lab, 11.5, WHITE, w="normal")
    qb = proj7(0, 90)
    ctext(ax, qb[0] + 0.02, qb[1] + 0.03, "獵戶正在升起 ↑", 11.5, GREY, w="normal", ha="left")
    lines = [("日落 17:04，昴宿已在東北東、高 7°", WHITE),
             ("19:00 高 32°；23:17 幾乎從頭頂經過（高 89°）", WHITE),
             ("月亮 19:46 才升起（88%）——之前看最清楚", AMBER),
             ("11/24 傍晚滿月掩昴；下次台灣看得到：2027/11/15 凌晨", BLUE),
             ("方位、高度、掩星：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.185 - i * 0.031, s, 11.5 if col != GREY else 10, col, w="normal")
    ctext(ax, 0.5, 0.030, "#萬國星空　#師大天文社", 13, WHITE, w="normal")


def main():
    global S, DATES
    os.makedirs(OUT, exist_ok=True)
    S = dict(G.load_stars(BASE))
    DATES = season_dates(25.033, 121.565, 8)
    print("  台北：黎明重現", DATES[0], "黃昏升起", DATES[1], "黃昏最後一見", DATES[2])
    CB.emit("", [("星點", c01_stars), ("星等", c01_mag), ("傳說", c01_legend)], title="C-X01-01_七還是六")
    CB.emit("", [("年輪", c03_ring), ("黎明", c03_dawn)], title="C-X01-03_黎明重現")
    CB.emit("", [("年輪", c04_ring), ("黃昏", c04_dusk)], title="C-X01-04_黃昏升起")
    CB.emit("", [("數字", c05_numbers), ("距離", c05_distance), ("年齡", c05_age)], title="C-X01-05_昴宿的真身")
    for fn, name in ((c02_card, "C-X01-02_太平洋的同一個字"), (c06_card, "C-X01-06_七姊妹的一百個名字"),
                     (c07_card, "C-X01-07_今晚往東看")):
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
