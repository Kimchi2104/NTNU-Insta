# -*- coding: utf-8 -*-
"""X-02 獵戶環球：全世界都認得的三顆星｜概念圖（C 系列骨架）

C-X02-01 正東升起（北方層、台北層、南方層）：參宿三赤緯 −0.3° → 北極圈內的特羅姆瑟、台北、紐西蘭威靈頓
         都從正東（方位 89–91°）升起；南半球整個獵戶倒過來
C-X02-02 一條腿（圖皮層、洛科諾層、提庫納層）：南美三個民族都在腰帶上看見一條腿
C-X02-03 三地的火（澳洲層、馬雅層、阿茲特克層）：卡米拉羅伊的營火、馬雅的三塊爐石、阿茲特克的鑽火棍
C-X02-04 年輕的巨星（亮度層、年齡層）：每顆都比太陽亮十幾萬倍以上；幾百萬歲，比恐龍滅絕晚得多
C-X02-05 腰帶的名字（9:16 圖卡；可存圖）
C-X02-06 今晚往東南東看（9:16 圖卡；台北 2027/1/1 20:00）

星點與連線：Stellarium 新版 skycultures（modern、tupi、lokono、tikuna、maya、aztec）；天象全部 PyEphem 自算。
執行：python3 make_x02_diagrams.py
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import matplotlib.patheffects as PE

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-02_獵戶環球/_概念圖")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
S = None
TPE = (25.0330, 121.5654, 0, 8, 15)
SITES = [("北方層", "特羅姆瑟（挪威）", "北緯 69.6°・北極圈內", (69.65, 18.96, 0, 1, -5), BLUE),
         ("台北層", "台北", "北緯 25.0°", (25.0330, 121.5654, 0, 8, 15), AMBER),
         ("南方層", "威靈頓（紐西蘭）", "南緯 41.3°", (-41.29, 174.78, 0, 13, 15), GREEN)]
HIP = dict(Mintaka=25930, Alnilam=26311, Alnitak=26727, Betelgeuse=27989, Bellatrix=25336, Rigel=24436,
           Saiph=27366, Meissa=26207, Hatysa=26241, Sirius=32349, Aldebaran=21421, Alcyone=17702)
BELT = [25930, 26311, 26727]
SWORD = [26241, 26221, 26237]
M42 = (83.82, -5.39)


def sc(culture, english):
    d = json.load(open(os.path.join(SC_NEW, culture, "index.json"), encoding="utf-8"))
    for c in d["constellations"]:
        if c["common_name"].get("english") == english:
            segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
            return [s for s in segs if len(set(s)) >= 2]
    raise KeyError((culture, english))


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, rot=0, va="center", alpha=1.0, halo=False):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, rotation=rot, rotation_mode="anchor", alpha=alpha, linespacing=1.25,
            path_effects=[PE.withStroke(linewidth=4, foreground=CB.BG)] if halo else None)


def observer(site, local):
    import ephem
    lat, lon, el, tz, temp = site
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = el
    o.pressure = 1010; o.temp = temp
    o.date = ephem.Date(ephem.Date(local) - tz * ephem.hour)
    return o


def body(ra, dec):
    import ephem
    b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec); b._epoch = ephem.J2000
    return b


def star_r(v, k=1.0):
    return max(1.2, (5.6 - v) ** 2.2 * 2.2 * k)


def tangent(ra, dec, ra0, dec0):
    """切平面（gnomonic）投影，單位：度；東在左"""
    a, d, a0, d0 = map(math.radians, (ra, dec, ra0, dec0))
    c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / c
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / c
    return -math.degrees(x), math.degrees(y)


class Field:
    """一格星圖：(ra0,dec0) 切平面，畫在畫布 (cx,cy)，每度 scl，範圍 hx×hy 度（半寬）"""

    def __init__(self, ra0, dec0, cx, cy, scl, hx, hy, maglim=5.0):
        self.ra0, self.dec0, self.cx, self.cy, self.scl, self.hx, self.hy = ra0, dec0, cx, cy, scl, hx, hy
        self.maglim = maglim

    def xy(self, ra, dec):
        x, y = tangent(ra, dec, self.ra0, self.dec0)
        return self.cx + x * self.scl, self.cy + y * self.scl

    def inside(self, ra, dec):
        x, y = tangent(ra, dec, self.ra0, self.dec0)
        return abs(x) <= self.hx and abs(y) <= self.hy

    def frame(self, ax, col=GREY):
        box(ax, self.cx - self.hx * self.scl, self.cy - self.hy * self.scl, 2 * self.hx * self.scl,
            2 * self.hy * self.scl, ec=col, fc="#070A16", lw=1.2, z=1, alpha=0.95)

    def stars(self, ax, k=1.0, z=6):
        for h, (ra, dec, v) in S.items():
            if v > self.maglim or not self.inside(ra, dec):
                continue
            x, y = self.xy(ra, dec)
            ax.scatter([x], [y], s=star_r(v, k), c=WHITE, zorder=z, lw=0)

    def lines(self, ax, segs, col, lw=2.4, alpha=.9, z=5):
        for seg in segs:
            pts = [self.xy(*S[h][:2]) for h in seg if h in S]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=lw, alpha=alpha, zorder=z,
                    solid_capstyle="round")

    def at(self, h):
        return self.xy(*S[h][:2]) if isinstance(h, int) else self.xy(*h)

    def ring(self, ax, h, r, col, lw=2.0, z=7):
        x, y = self.at(h)
        ax.add_patch(CB.Circle((x, y), r, fc="none", ec=col, lw=lw, zorder=z))

    def glow(self, ax, ra, dec, r_deg, z=4):
        x, y = self.xy(ra, dec)
        for k, op in ((1.0, 0.10), (0.7, 0.16), (0.42, 0.26), (0.2, 0.4)):
            ax.add_patch(CB.Circle((x, y), r_deg * k * self.scl, fc=MW, ec="none", alpha=op, zorder=z))


def flame(ax, x, y, s, z=8):
    """營火：外焰紅、內焰琥珀（單位座標水滴形）"""
    def drop(sc):
        pts = []
        for i in range(41):
            t = math.pi * i / 40
            r = math.sin(t / 2) ** 0.8
            pts.append((x + sc * 0.55 * r * math.sin(t) * 0.9, y + sc * (1.0 - t / math.pi * 1.6) - sc * 0.15))
        pts += [(2 * x - px, py) for px, py in pts[::-1]]
        return pts
    ax.add_patch(CB.Polygon(drop(s), closed=True, fc=RED, ec="none", alpha=.9, zorder=z))
    ax.add_patch(CB.Polygon(drop(s * 0.55), closed=True, fc=AMBER, ec="none", alpha=.95, zorder=z + 1))


# ══════════════════════ C-X02-01 正東升起 ══════════════════════
ORI_SEGS = None
TRACK_H = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
RISE = {}


def _rise_info(site):
    import ephem
    o = observer(site, "2027/1/1 12:00")
    b = body(*S[HIP["Mintaka"]][:2])
    r = o.next_rising(b)
    o.date = r; b.compute(o)
    return r, math.degrees(float(b.az))


def site_panel(ax, idx):
    key, name, lat_s, site, col = SITES[idx]
    import ephem
    y0 = 0.31 - idx * 0.575                     # 地平線 y
    az0, az1, alt1 = 40.0, 140.0, 42.0
    xa, xb = -0.90, 0.90
    h_ = 0.40

    def q(alt, az):
        return xa + (az - az0) / (az1 - az0) * (xb - xa), y0 + alt / alt1 * h_
    if idx == 0:
        T(ax, 0.0, 0.92, "為什麼全世界都看得到？", 30, WHITE)
        T(ax, 0.0, 0.85, "參宿三差不多就在天赤道上（赤緯 −0.3°）：在哪裡都從正東升起", 13.5, GREY, w="normal")
        T(ax, 0.0, 0.805, "虛線：腰帶升起後 3 小時走的路；星圖：升起後 2 小時（2027/1/1）", 10.5, GREY, w="normal")
    box(ax, -0.95, y0 - 0.075, 1.90, h_ + 0.115, ec=col, fc="#070A16", lw=1.3, z=1, alpha=0.95)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=2.0, alpha=.85, zorder=5)
    for az, lab in ((45, "東北"), (90, "正東"), (135, "東南")):
        x, _ = q(0, az)
        ax.plot([x, x], [y0, y0 - 0.015], c=WHITE, lw=1.4, zorder=5)
        ctext(ax, x, y0 - 0.040, lab, 12 if az != 90 else 14, WHITE if az != 90 else AMBER,
              w="normal" if az != 90 else "bold")
    ctext(ax, -0.92, y0 + h_ - 0.005, name, 15, col, ha="left", va="top", z=12, halo=True)
    ctext(ax, -0.92, y0 + h_ - 0.062, lat_s, 11, GREY, w="normal", ha="left", va="top", z=12)
    r, raz = _rise_info(site)
    RISE[key] = (ephem.Date(r + site[3] * ephem.hour), raz)
    # 腰帶升起後每半小時的位置
    bx, by = [], []
    for dh in TRACK_H:
        o = observer(site, "2027/1/1 12:00"); o.date = ephem.Date(r + dh * ephem.hour)
        b = body(*S[HIP["Alnilam"]][:2]); b.compute(o)
        x, y = q(math.degrees(float(b.alt)), math.degrees(float(b.az)))
        bx.append(x); by.append(y)
    ax.plot(bx, by, c=col, lw=1.4, alpha=.6, ls=(0, (2, 3)), zorder=4)
    ax.annotate("", xy=(bx[-1], by[-1]), xytext=(bx[-2], by[-2]),
                arrowprops=dict(arrowstyle="->", color=col, lw=1.6, alpha=.8), zorder=4)
    # 升起後 2 小時的整個獵戶
    o = observer(site, "2027/1/1 12:00"); o.date = ephem.Date(r + 2.0 * ephem.hour)
    pos = {}
    for h, (ra, dec, v) in S.items():
        if v > 4.2:
            continue
        b = body(ra, dec); b.compute(o)
        alt, az = math.degrees(float(b.alt)), math.degrees(float(b.az))
        if 0 < alt < alt1 and az0 < az < az1:
            pos[h] = q(alt, az)
            ax.scatter([pos[h][0]], [pos[h][1]], s=star_r(v, 1.3), c=WHITE, zorder=7, lw=0)
    for seg in ORI_SEGS:
        for a, b2 in zip(seg, seg[1:]):
            if a in pos and b2 in pos:
                ax.plot([pos[a][0], pos[b2][0]], [pos[a][1], pos[b2][1]], c=WHITE, lw=1.2, alpha=.45, zorder=6)
    for a, b2 in zip(BELT, BELT[1:]):
        if a in pos and b2 in pos:
            ax.plot([pos[a][0], pos[b2][0]], [pos[a][1], pos[b2][1]], c=AMBER, lw=3.0, alpha=.95, zorder=6)
    for h, lab, c2 in ((HIP["Betelgeuse"], "參宿四", RED), (HIP["Rigel"], "參宿七", BLUE)):
        if h in pos:
            ctext(ax, pos[h][0] + 0.035, pos[h][1], lab, 11, c2, ha="left", z=12, halo=True)
    x, _ = q(0, raz)
    ax.scatter([x], [y0], s=60, c=AMBER, zorder=8, lw=0)
    ctext(ax, 0.92, y0 + h_ - 0.005, f"升起方位 {raz:.1f}°", 13, AMBER, ha="right", va="top", z=12, halo=True)
    if idx == 2:
        ctext(ax, 0.0, -0.962, "南半球也從正東升起——只是整個獵戶倒過來（參宿七在上）", 13.5, GREEN)


def c01_north(ax):
    site_panel(ax, 0)


def c01_tpe(ax):
    site_panel(ax, 1)


def c01_south(ax):
    site_panel(ax, 2)


# ══════════════════════ C-X02-02 一條腿 ══════════════════════
LEG = None
COLS = [-0.635, 0.0, 0.635]


def leg_field(i):
    return Field(76.0, -3.0, COLS[i], 0.03, 0.0148, 20.5, 34.0, maglim=4.2)


def leg_panel(ax, i, title, sub, col, segs, notes):
    F = leg_field(i)
    F.frame(ax, col)
    F.stars(ax, k=0.6)
    F.lines(ax, segs, col, lw=3.0)
    ctext(ax, COLS[i], 0.66, title, 15.5, col, z=12)
    ctext(ax, COLS[i], 0.615, sub, 11, GREY, w="normal", z=12)
    for (anc, txt, c2, dx, dy) in notes:
        x, y = F.at(anc)
        ctext(ax, x + dx, y + dy, txt, 10.5, c2, z=12, halo=True)
    return F


def c02_tupi(ax):
    T(ax, 0.0, 0.92, "一條腿：南美洲三個民族", 30, WHITE)
    T(ax, 0.0, 0.85, "隔著上千公里，都在獵戶的腰帶上看見一條腿", 13.5, GREY, w="normal")
    F = leg_panel(ax, 0, "圖皮（巴西）", "Tuivaé　老人", GREEN, LEG["tupi"],
                  [(HIP["Betelgeuse"], "斷掉的地方", RED, 0.02, 0.055),
                   (HIP["Alnilam"], "好腿的膝蓋", GREEN, 0.105, -0.03)])
    F.ring(ax, HIP["Betelgeuse"], 0.022, RED)
    ctext(ax, COLS[0], -0.56, "妻子愛上他的弟弟，\n砍斷他膝蓋以下的腿；\n腰帶是他好腿的膝蓋", 11, WHITE,
          w="normal", va="top")


def c02_lokono(ax):
    F = leg_panel(ax, 1, "洛科諾（蘇利南、蓋亞那）", "Mabukuli　沒有大腿的人", BLUE, LEG["lokono"],
                  [(HIP["Aldebaran"], "身體＝畢宿", BLUE, 0.0, -0.06),
                   (HIP["Alnilam"], "沒有大腿的人", BLUE, 0.11, -0.035)])
    ctext(ax, COLS[1], -0.56, "打不到獵物的獵人\n切下自己的腿，騙家人是貘肉；\n身體變成畢宿（貘的下巴）", 11, WHITE,
          w="normal", va="top")


def c02_tikuna(ax):
    F = leg_panel(ax, 2, "Tikuna（亞馬遜）", "Wücütcha　神獸的腿", PURPLE, LEG["tikuna"],
                  [(HIP["Alnilam"], "腳趾", PURPLE, 0.075, 0.02)])
    ctext(ax, COLS[2], -0.56, "天上神獸 Wücütcha 的腿，\n腰帶是牠的腳趾", 11, WHITE, w="normal", va="top")
    ctext(ax, 0.0, -0.93, "連線：Stellarium tupi、lokono、tikuna；圖皮的故事見 Afonso 2006（圖皮—瓜拉尼天文）", 9, GREY,
          w="normal")


# ══════════════════════ C-X02-03 三地的火 ══════════════════════
FIRE = None


def fire_field(i):
    return Field(83.3, -4.6, COLS[i], 0.10, 0.041, 7.2, 9.6, maglim=5.2)


def fire_panel(ax, i, title, sub, col):
    F = fire_field(i)
    F.frame(ax, col)
    ctext(ax, COLS[i], 0.62, title, 15.5, col, z=12)
    ctext(ax, COLS[i], 0.575, sub, 11, GREY, w="normal", z=12)
    return F


def c03_kami(ax):
    T(ax, 0.0, 0.92, "三地的火", 30, WHITE)
    T(ax, 0.0, 0.85, "同一塊星空：腰帶、獵戶的劍、參宿七", 13.5, GREY, w="normal")
    F = fire_panel(ax, 0, "卡米拉羅伊（澳洲）", "Birray Birray　三個男孩", AMBER)
    F.stars(ax, k=1.0)
    F.lines(ax, [BELT], AMBER, lw=3.0)
    F.lines(ax, [SWORD], RED, lw=2.0, alpha=.7)
    x, y = F.at(HIP["Rigel"])
    flame(ax, x + 0.055, y + 0.005, 0.045)
    ctext(ax, x - 0.02, y - 0.075, "營火＝參宿七", 11, RED, z=12, halo=True)
    x, y = F.at(SWORD[1])
    ctext(ax, x - 0.025, y - 0.02, "撥火棍\n＝劍", 11, RED, ha="right", z=12, halo=True)
    x, y = F.at(HIP["Alnilam"])
    ctext(ax, x, y + 0.075, "三個男孩", 11, AMBER, z=12, halo=True)
    ctext(ax, COLS[0], -0.40, "三個還沒成年的男孩，\n圍著營火", 11, WHITE, w="normal", va="top")


def c03_maya(ax):
    F = fire_panel(ax, 1, "馬雅（中美洲）", "Oxib' Xk'ub'　三塊爐石", RED)
    F.glow(ax, *M42, 0.55)
    F.stars(ax, k=1.0)
    F.lines(ax, FIRE["maya"], RED, lw=2.4)
    x, y = F.at(M42)
    ctext(ax, x + 0.06, y + 0.012, "煙", 13, WHITE, z=12, halo=True)
    for h, lab, dx, dy in ((HIP["Alnitak"], "參宿一", -0.02, 0.04), (HIP["Saiph"], "參宿六", -0.02, -0.04),
                           (HIP["Rigel"], "參宿七", 0.03, -0.04)):
        x, y = F.at(h)
        ctext(ax, x + dx, y + dy, lab, 10.5, WHITE, z=12, halo=True)
    ctext(ax, COLS[1], -0.40, "創世時的第一把火：\n三顆星是火爐的三塊石頭，\n獵戶座大星雲是火冒出的煙", 11, WHITE,
          w="normal", va="top")


def c03_aztec(ax):
    F = fire_panel(ax, 2, "阿茲特克（墨西哥）", "Mamalhuaztli　鑽火棍", AMBER)
    F.stars(ax, k=1.0)
    F.lines(ax, FIRE["aztec"], AMBER, lw=2.4)
    ctext(ax, COLS[2], -0.40, "曆法每 52 年走完一輪，\n熄掉所有的火，\n在山頂鑽出新的火", 11, WHITE,
          w="normal", va="top")
    ctext(ax, 0.0, -0.93, "連線：Stellarium kamilaroi（說明）、maya、aztec；火的圖示為示意", 9, GREY, w="normal")


# ══════════════════════ C-X02-04 年輕的巨星 ══════════════════════
def c04_bright(ax):
    T(ax, 0.0, 0.92, "年輕的藍色巨星", 30, WHITE)
    T(ax, 0.0, 0.85, "參宿一、參宿二、參宿三", 13.5, GREY, w="normal")
    box(ax, -0.95, 0.12, 1.90, 0.62, ec=BLUE, fc=PANEL, z=1, alpha=0.95)
    ctext(ax, -0.90, 0.69, "有多亮？（跟太陽比，對數刻度）", 16, BLUE, ha="left")
    xa, xb, y = -0.82, 0.86, 0.36

    def X(L):
        return xa + math.log10(L) / 6.0 * (xb - xa)
    ax.plot([xa, xb], [y, y], c=WHITE, lw=1.6, alpha=.7, zorder=4)
    for e in range(7):
        x = X(10 ** e)
        ax.plot([x, x], [y - 0.012, y + 0.012], c=WHITE, lw=1.2, alpha=.7, zorder=4)
        lab = ["1", "10", "100", "1,000", "1 萬", "10 萬", "100 萬"][e]
        ctext(ax, x, y - 0.045, lab, 11, GREY, w="normal")
    ax.scatter([X(1)], [y], s=140, c="#FFE08A", zorder=6, lw=0)
    ctext(ax, X(1), y + 0.07, "太陽", 13, "#FFE08A")
    ax.scatter([X(25)], [y], s=90, c=WHITE, zorder=6, lw=0)
    ctext(ax, X(25), y + 0.07, "天狼星 約 25 倍", 12, WHITE, w="normal")
    ax.annotate("", xy=(xb + 0.02, y), xytext=(X(1.2e5), y),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=7, alpha=.75, mutation_scale=28), zorder=5)
    ax.scatter([X(1.2e5)], [y], s=150, c="#CFE0FF", zorder=6, lw=0)
    ctext(ax, X(1.2e5) + 0.04, y + 0.075, "腰帶三星：每顆十幾萬倍以上", 13, BLUE, ha="right")
    ctext(ax, -0.90, 0.20, "離我們大約 1,200～1,400 光年（這幾顆的距離本身就量不太準，各研究略有不同）", 11, GREY,
          w="normal", ha="left")


def c04_age(ax):
    box(ax, -0.95, -0.80, 1.90, 0.82, ec=GREEN, fc=PANEL, z=1, alpha=0.95)
    ctext(ax, -0.90, -0.03, "幾歲了？", 16, GREEN, ha="left")
    xa, xb, y = -0.85, 0.85, -0.42

    def X(myr):                                   # 7000 萬年前 → 今天
        return xa + (70 - myr) / 70 * (xb - xa)
    ax.plot([xa, xb], [y, y], c=WHITE, lw=1.6, alpha=.7, zorder=4)
    for myr in (70, 60, 50, 40, 30, 20, 10, 0):
        x = X(myr)
        ax.plot([x, x], [y - 0.012, y + 0.012], c=WHITE, lw=1.2, alpha=.7, zorder=4)
        ctext(ax, x, y - 0.045, "今天" if myr == 0 else f"{myr:,}00 萬年前".replace(",", ""), 9.5, GREY,
              w="normal")
    x = X(66)
    ax.plot([x, x], [y, y + 0.22], c=RED, lw=1.6, alpha=.8, zorder=5)
    ax.scatter([x], [y], s=90, c=RED, zorder=6, lw=0)
    ctext(ax, x - 0.02, y + 0.27, "恐龍滅絕\n6,600 萬年前", 12, RED, ha="left")
    ax.add_patch(CB.Rectangle((X(8), y - 0.03), X(3) - X(8), 0.06, fc=BLUE, ec="none", alpha=.7, zorder=5))
    ctext(ax, X(5) - 0.03, y + 0.24, "腰帶三星誕生\n大約幾百萬年前", 12, BLUE, ha="right")
    ax.plot([X(6), X(6)], [y + 0.03, y + 0.17], c=BLUE, lw=1.4, alpha=.8, zorder=5)
    ax.scatter([X(0)], [y], s=90, c=GREEN, zorder=6, lw=0)
    ctext(ax, X(0) - 0.01, y - 0.14, "獵戶座大星雲\n現在還在生出新星", 12, GREEN, ha="right")
    ctext(ax, -0.90, -0.74, "恐龍滅絕的時候，這三顆星還沒出生（年齡為恆星演化模型估計，誤差可達數百萬年）", 10.5,
          GREY, w="normal", ha="left")


# ══════════════════════ 9:16 圖卡 ══════════════════════
NAMES = [("數字「三」", None, None, AMBER),
         ("中國", "參", "三", AMBER),
         ("滿洲", "Ilan usiha", "三顆星", AMBER),
         ("阿努塔", "Ara Toru", "三星之路", AMBER),
         ("東加", "ʻAlotolu", "一船三人", AMBER),
         ("人", None, None, BLUE),
         ("北歐（冰島）", "Fiskikarlar", "漁夫們", BLUE),
         ("白俄羅斯", "Kastsy", "割草的人", BLUE),
         ("西伯利亞", "Kichigi", "打穀的人", BLUE),
         ("因紐特", "Ullaktut", "奔跑的人", BLUE),
         ("澳洲 卡米拉羅伊", "Birray Birray", "三個男孩", BLUE),
         ("羅馬尼亞", "Trisfetitele", "三位聖人", BLUE),
         ("薩丁尼亞", "Sas Tres Marias", "三個瑪利亞", BLUE),
         ("南非 科薩", "amaKroza", "排成一列的人", BLUE),
         ("器物", None, None, GREEN),
         ("日本", "からすきぼし", "唐鋤星（犁）＊", GREEN),
         ("羅馬尼亞", "Sfredelul mare", "大螺旋鑽＊", GREEN),
         ("亞馬遜 圖卡諾", "Sioyahpu", "錛的柄＊", GREEN),
         ("萬那杜 Netwar", "Kasulia apam", "長軛", GREEN),
         ("動物", None, None, PURPLE),
         ("蒙古", "Гурван марал", "三頭母鹿", PURPLE),
         ("南部非洲 那馬", "—", "三匹斑馬", PURPLE)]


def c05_card(ax):
    ctext(ax, 0.5, 0.962, "腰帶的名字", 30, WHITE)
    ctext(ax, 0.5, 0.930, "同樣三顆星，世界各地叫它什麼？", 12, GREY, w="normal")
    y = 0.893
    for a, b, c, col in NAMES:
        if b is None:
            y -= 0.004
            ctext(ax, 0.06, y, a, 14, col, ha="left")
            ax.plot([0.06, 0.94], [y - 0.016, y - 0.016], c=col, lw=1.0, alpha=.5)
            y -= 0.040
            continue
        ctext(ax, 0.06, y, a, 11, WHITE, ha="left")
        ctext(ax, 0.38, y, b, 11.5, col, ha="left")
        ctext(ax, 0.68, y, c, 11, WHITE, w="normal", ha="left")
        y -= 0.0335
    ctext(ax, 0.5, 0.098, "這集的：南美的一條腿（圖皮、洛科諾、Tikuna）、中美洲的火（馬雅、阿茲特克）", 10, GREY,
          w="normal")
    ctext(ax, 0.5, 0.074, "＊連同附近其他星一起組成", 9.5, GREY, w="normal")
    ctext(ax, 0.5, 0.050, "Stellarium 各文化星空；東加依 Collocott 1922（見 A-10）；蒙古、那馬見 A-07、X-01", 8.5,
          GREY, w="normal")
    ctext(ax, 0.5, 0.018, "#萬國星空　#師大天文社", 11.5, WHITE, w="normal")


DIRS16 = [(67.5, "東北東"), (90, "東"), (112.5, "東南東"), (135, "東南"), (157.5, "南南東"), (180, "南")]
TONIGHT = {}


def sky_panel(ax, y0, y1, az0, az1, alt1, when):
    import ephem
    o = observer(TPE, when)
    xa, xb = 0.06, 0.94

    def q(alt, az):
        return xa + (az - az0) / (az1 - az0) * (xb - xa), y0 + alt / alt1 * (y1 - y0)
    box(ax, 0.04, y0 - 0.055, 0.92, (y1 - y0) + 0.08, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=1.6, alpha=.8, zorder=5)
    for az, lab in DIRS16:
        if az0 <= az <= az1:
            x, _ = q(0, az)
            ctext(ax, x, y0 - 0.022, lab, 10.5 if az != 112.5 else 12, WHITE if az != 112.5 else AMBER,
                  w="normal" if az != 112.5 else "bold", z=12)
    for alt in (20, 40, 60):
        if alt < alt1:
            _, y = q(alt, az0)
            ax.plot([xa, xb], [y, y], c=WHITE, lw=0.6, alpha=.18, ls=(0, (3, 4)), zorder=2)
            ax.text(xa + 0.005, y + 0.004, f"{alt}°", fontproperties=CB.FP, fontsize=8, color=GREY, zorder=3)
    pos = {}
    for h, (ra, dec, v) in S.items():
        if v > 4.5:
            continue
        b = body(ra, dec); b.compute(o)
        alt, az = math.degrees(float(b.alt)), math.degrees(float(b.az))
        TONIGHT[h] = (alt, az)
        if not (0 < alt < alt1 and az0 < az < az1):
            continue
        x, y = q(alt, az)
        pos[h] = (x, y)
        ax.scatter([x], [y], s=max(1.0, (5.6 - v) ** 2.2 * 2.6), c=WHITE, zorder=7, lw=0)
    for seg in ORI_SEGS:
        for a, b in zip(seg, seg[1:]):
            if a in pos and b in pos:
                ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=WHITE, lw=1.1, alpha=.4, zorder=6)
    for a, b in zip(BELT, BELT[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=AMBER, lw=2.6, alpha=.9, zorder=6)
    for key, lab, col, dx, dy in (("Betelgeuse", "參宿四（紅）", RED, -0.03, 0.0),
                                  ("Rigel", "參宿七（藍白）", BLUE, 0.03, 0.0),
                                  ("Alnilam", "腰帶", AMBER, 0.035, 0.022),
                                  ("Sirius", "天狼星", WHITE, 0.035, 0.0)):
        x, y = pos[HIP[key]]
        ax.text(x + dx, y + dy, lab, fontproperties=CB.FP, fontsize=11.5, color=col, weight="bold", va="center",
                ha="left" if dx > 0 else "right", zorder=12,
                path_effects=[PE.withStroke(linewidth=4, foreground="#0E1428")])


def c06_card(ax):
    import ephem
    ctext(ax, 0.5, 0.962, "今晚往東南東看", 30, WHITE)
    ctext(ax, 0.5, 0.928, "台北　2027/1/1（五・元旦）晚上 8 點", 13, GREY, w="normal")
    sky_panel(ax, 0.40, 0.86, 82.0, 150.0, 62.0, "2027/1/1 20:00")
    a4, z4 = TONIGHT[HIP["Betelgeuse"]]; a7, z7 = TONIGHT[HIP["Rigel"]]
    ab, zb = TONIGHT[HIP["Alnilam"]]; asr, zsr = TONIGHT[HIP["Sirius"]]
    o = observer(TPE, "2027/1/1 12:00")
    mr = ephem.Date(o.next_rising(ephem.Moon()) + 8 * ephem.hour)
    tr = ephem.Date(o.next_transit(body(*S[HIP["Alnilam"]][:2])) + 8 * ephem.hour)
    mr_t, tr_t = mr.tuple(), tr.tuple()
    lines = [(f"腰帶在東南東、高度約 {ab:.0f}°：獵戶整個橫躺著", WHITE),
             (f"參宿四（左）{a4:.0f}°、參宿七（右）{a7:.0f}°——兩顆一樣高", WHITE),
             (f"天狼星在腰帶正下方，高度約 {asr:.0f}°", WHITE),
             (f"{tr_t[3]}:{tr_t[4]:02d} 獵戶走到正南方最高處；月亮 1/2 凌晨 {mr_t[3]}:{mr_t[4]:02d} 才升起", WHITE),
             ("方位、高度、時刻：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.265 - i * 0.032, s, 11.5 if col != GREY else 9.5, col, w="normal")
    ctext(ax, 0.5, 0.018, "#萬國星空　#師大天文社", 12, WHITE, w="normal")
    print(f"  · 今晚：腰帶 {ab:.1f}°/{zb:.1f}°、參宿四 {a4:.1f}°/{z4:.1f}°、參宿七 {a7:.1f}°/{z7:.1f}°、"
          f"天狼 {asr:.1f}°/{zsr:.1f}°；中天 {tr}、月出 {mr}")


def main():
    global S, ORI_SEGS, LEG, FIRE
    S = dict(G.load_stars(BASE))
    ORI_SEGS = sc("modern", "Orion")
    LEG = dict(tupi=sc("tupi", "Old Man"),
               lokono=sc("lokono", "Man without a thigh") + sc("lokono", "Jaw of the tapir"),
               tikuna=sc("tikuna", "Wücütcha's leg"))
    FIRE = dict(maya=sc("maya", "Primordial Fire"), aztec=sc("aztec", "The New fire"))
    os.makedirs(OUT, exist_ok=True)
    print("── C-X02 概念圖 ──")
    CB.emit("", [("北方", c01_north), ("台北", c01_tpe), ("南方", c01_south)], title="C-X02-01_正東升起")
    for k, (t, raz) in RISE.items():
        print(f"  · {k}：參宿三升起 {t}（當地時）方位 {raz:.2f}°")
    CB.emit("", [("圖皮", c02_tupi), ("洛科諾", c02_lokono), ("提庫納", c02_tikuna)], title="C-X02-02_一條腿")
    CB.emit("", [("澳洲", c03_kami), ("馬雅", c03_maya), ("阿茲特克", c03_aztec)], title="C-X02-03_三地的火")
    CB.emit("", [("亮度", c04_bright), ("年齡", c04_age)], title="C-X02-04_年輕的巨星")
    for name, fn in [("C-X02-05_腰帶的名字", c05_card), ("C-X02-06_今晚往東南東看", c06_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
