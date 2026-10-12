# -*- coding: utf-8 -*-
"""B-03 星空嘉年華（12/5 台東縱谷・鹿野）｜概念圖（方形透明分層＝Reels 定格頁；9:16 圖卡＝滿版）
  C-B03-01_方位_1930南方   → 02 鏡  19:30 南方：土星最高、旁邊的海王星
  C-B03-02_縱谷光害        → 03 鏡  城鎮的方位與距離 → 兩側的山（示意圖，不是地圖）
  C-B03-03_方位_0040南方   → 06 鏡  00:40 南方：獵戶座大星雲、馬頭／火焰、玫瑰、老人星
  C-B03-04_攝影時間窗      → 07 鏡  9:16 圖卡：各目標仰角 30° 以上的時段（可存圖）
  C-B03-05_方位_0400東南   → 09 鏡  04:00 東南方高空：木星、軒轅十四、火星
  C-B03-06_方位_0430東南東 → 11 鏡  04:30 東南東低空：殘月（地照）、金星、角宿一＋鏡頭框（全片幅 50／85／135／300 mm）
  C-B03-07_今晚時間表      → 13 鏡  9:16 圖卡（可存圖）
輸出：05_素材/B-03_星空嘉年華/_概念圖/

方位卡＝真正的地平座標（北緯 22.92°、東經 121.12°，台東鹿野高台一帶）：以面向的方位、仰角為中心的立體投影，
畫面上方＝天頂方向；地平線以下塗黑（數學地平，不含山稜）。恆星 Hipparcos J2000，行星、日月、時刻 PyEphem 自算。
"""
import os, sys, math
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_b03_v4 as B

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/B-03_星空嘉年華/_概念圖")
C.set_base(OUT)
RED, GREY, GROUND = "#FF6B6B", "#7C8BA8", "#05070F"
DARK_LIMB = "#3A4260"                         # 地照：月亮的暗面不是全黑
PAL = {"blue": BLUE, "purple": PURPLE, "green": GREEN, "red": RED, "amber": AMBER, "white": WHITE}
S = dict(G.load_stars(BASE))
for _k, _h in B.PL_HIP.items():
    S[_h] = B.PLANETS[_k]
LAT = math.radians(B.LAT)
SUB = "12/5（六）星空嘉年華・台東鹿野（北緯 22.9°）"
SUB_DAWN = "12/6（日）清晨・星空嘉年華・台東鹿野（北緯 22.9°）"
CANOPUS = 30438


# ══════════════════════ 星曆小工具 ══════════════════════
def obs(when):
    """when＝台灣時間 datetime"""
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(B.LAT), str(B.LON); o.elevation = B.ELEV
    o.pressure = 980; o.temp = 15
    o.date = ephem.Date(when - timedelta(hours=8))
    return o


def lt(d):
    import ephem
    return (ephem.Date(d).datetime() + timedelta(hours=8))


def hm(d):
    t = lt(d) + timedelta(seconds=30)
    return t.strftime("%H:%M")


def lst_at(when):
    return math.degrees(obs(when).sidereal_time())


# ══════════════════════ 地平座標與立體投影（同 B-01） ══════════════════════
def altaz(ra, dec, lst):
    h = math.radians((lst - ra) % 360.0)
    d = math.radians(dec)
    sa = math.sin(LAT) * math.sin(d) + math.cos(LAT) * math.cos(d) * math.cos(h)
    alt = math.asin(max(-1.0, min(1.0, sa)))
    y = -math.cos(d) * math.sin(h)
    x = math.sin(d) * math.cos(LAT) - math.cos(d) * math.sin(LAT) * math.cos(h)
    return math.degrees(alt), math.degrees(math.atan2(y, x)) % 360.0


def vec(alt, az):
    a, z = math.radians(alt), math.radians(az)
    return (math.cos(a) * math.sin(z), math.cos(a) * math.cos(z), math.sin(a))


class View:
    def __init__(self, az0, alt0, scale, y0=0.0):
        self.f = vec(alt0, az0)
        z = math.radians(az0)
        self.r = (math.cos(z), -math.sin(z), 0.0)
        f, r = self.f, self.r
        self.u = (r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0])
        self.s, self.y0 = scale, y0

    def xy(self, alt, az):
        p = vec(alt, az)
        c = sum(a * b for a, b in zip(p, self.f))
        if c < -0.2:
            return None
        k = 2.0 / (1.0 + c) * self.s
        return (k * sum(a * b for a, b in zip(p, self.r)),
                self.y0 + k * sum(a * b for a, b in zip(p, self.u)))


BOX = (-0.98, 0.98, -0.70, 0.74)


def inbox(p, pad=0.0):
    return p and BOX[0] + pad <= p[0] <= BOX[1] - pad and BOX[2] + pad <= p[1] <= BOX[3] - pad


DIR8 = {0: "北", 45: "東北", 90: "東", 135: "東南", 180: "南", 225: "西南", 270: "西", 315: "西北"}


def text_box(txt, pt):
    k = pt * 190 / 72 / 1026.0
    w = sum(1.0 if ord(c) > 0x2E80 else 0.58 for c in txt) * k
    return w / 2 + 0.008, k * 0.62 + 0.006


class Card:
    """一張方位卡：先算好星、連線、目標的位置，再用避讓法擺名稱，最後分兩層畫"""

    def __init__(self, lst, v, lines, stars, cons, targets, extra=()):
        self.lst, self.v = lst, v
        self.pts, self.segs = [], []
        for h, (ra, dec, mg) in S.items():
            if mg > 4.8:
                continue
            al, az = altaz(ra, dec, lst)
            p = v.xy(al, az) if al >= 0 else None
            if inbox(p):
                self.pts.append((p[0], p[1], max(2.0, (5.6 - mg) ** 2.1 * 5.2), mg))
        for key in lines:
            for segs, col, lws in B.LINE_GROUPS[key]:
                for seg in segs:
                    hs = [h for h in seg if h in S]
                    for a, b in zip(hs, hs[1:]):
                        q = []
                        for t in range(11):
                            ra = S[a][0] + ((S[b][0] - S[a][0] + 540) % 360 - 180) * t / 10
                            dec = S[a][1] + (S[b][1] - S[a][1]) * t / 10
                            al, az = altaz(ra, dec, lst)
                            q.append(v.xy(al, az) if al > -1 else None)
                        if all(p and inbox(p) for p in q):
                            self.segs.append((q, PAL[col], lws))
        self.targets, self.boxes = [], []
        tset = set()
        for tg in targets:
            key, txt, col, (dx, dy) = tg[:4]
            opt = tg[4] if len(tg) > 4 else {}
            ra, dec = key if isinstance(key, tuple) else S[key][:2]
            if not isinstance(key, tuple):
                tset.add(key)
            al, az = altaz(ra, dec, lst)
            p = v.xy(al, az)
            if not p:
                continue
            c = PAL.get(col, col)
            tx, ty = p[0] + dx, p[1] + dy
            ha = "left" if dx > 0 else "right"
            al = opt.get("alt", al)                  # 行星、月亮：用 PyEphem 當時的仰角
            rr = opt.get("r", 0.055)
            self.targets.append((p, c, txt, al, tx, ty, ha, rr))
            for t, pt, yy in ((txt, 21, ty + 0.025), (f"仰角 {al:.0f}°", 17, ty - 0.035)):
                hw, hh = text_box(t, pt)
                x0 = tx if ha == "left" else tx - 2 * hw
                self.boxes.append((x0, x0 + 2 * hw, yy - hh, yy + hh))
            self.boxes.append((p[0] - rr - 0.005, p[0] + rr + 0.005, p[1] - rr - 0.005, p[1] + rr + 0.005))
        self.labels = []
        for key, txt, col, dx, dy in cons:
            if isinstance(key, tuple):
                ra, dec = key
            else:
                ra, dec = B.centroid(B.uniq([B.W[k] for k in B.CONS[key][0]]), S)
            al, az = altaz(ra, dec, lst)
            p = v.xy(al, az)
            if inbox(p, 0.04) and al > 3:
                self.place(txt, 20, (p[0] + dx, p[1] + dy), PAL.get(col, col), True, far=True)
        for h, txt, col, dx, dy in stars:
            if h in tset:
                continue
            al, az = altaz(S[h][0], S[h][1], lst)
            p = v.xy(al, az)
            if inbox(p, 0.02) and al > 1:
                self.place(txt, 16, p, PAL.get(col, col), False, far=False)
        self.extra = extra

    def cost(self, cx, cy, hw, hh):
        x0, x1, y0, y1 = cx - hw, cx + hw, cy - hh, cy + hh
        if x0 < BOX[0] or x1 > BOX[1] or y0 < BOX[2] + 0.02 or y1 > BOX[3]:
            return 1e9
        hz = self.v.xy(0.0, self.az_at(cx))
        if hz and y0 < hz[1] + 0.02:
            return 1e9
        c = 0.0
        for x, y, s, mg in self.pts:
            if x0 - 0.01 < x < x1 + 0.01 and y0 - 0.01 < y < y1 + 0.01:
                c += 1.0 + max(0.0, 3.5 - mg) * 2.0
        for q, col, lws in self.segs:
            for x, y in q:
                if x0 < x < x1 and y0 < y < y1:
                    c += 1.5
        for b in self.boxes:
            ox = min(x1, b[1]) - max(x0, b[0]); oy = min(y1, b[3]) - max(y0, b[2])
            if ox > 0 and oy > 0:
                c += 200.0
        return c

    def az_at(self, x):
        best, bx = 0.0, 9.0
        for az in range(0, 360, 2):
            p = self.v.xy(0.0, az)
            if p and abs(p[0] - x) < bx:
                bx, best = abs(p[0] - x), az
        return best

    def place(self, txt, pt, anchor, col, bold, far):
        hw, hh = text_box(txt, pt)
        ax_, ay = anchor
        if far:
            cand = [(0, 0)] + [(dx * s, dy * s) for s in (1, 2) for dx, dy in
                               ((0, 0.07), (0, -0.07), (0.13, 0), (-0.13, 0), (0.13, 0.07),
                                (-0.13, 0.07), (0.13, -0.07), (-0.13, -0.07))]
        else:
            g = 0.035
            cand = [(0, -(hh + g)), (0, hh + g), (hw + g, 0), (-(hw + g), 0),
                    (hw + g, -(hh + g)), (-(hw + g), -(hh + g)), (hw + g, hh + g),
                    (-(hw + g), hh + g)]
        best = None
        for i, (dx, dy) in enumerate(cand):
            c = self.cost(ax_ + dx, ay + dy, hw, hh) + 0.25 * i
            if best is None or c < best[0]:
                best = (c, ax_ + dx, ay + dy)
        if best[0] >= 1e9:
            return
        _, x, y = best
        self.boxes.append((x - hw, x + hw, y - hh, y + hh))
        self.labels.append((x, y, txt, pt, col, bold))

    def sky(self, title, sub):
        def draw(ax):
            v, lst = self.v, self.lst
            T(ax, 0.0, 0.92, title, 34, WHITE)
            T(ax, 0.0, 0.84, sub, 19, GREY, w="normal")
            for alt in (30, 60):
                pts = [v.xy(alt, az) for az in range(0, 361, 2)]
                run = []
                for p in pts + [None]:
                    if p and inbox(p):
                        run.append(p)
                    else:
                        if len(run) > 1:
                            ax.plot([a for a, b in run], [b for a, b in run], c=WHITE, lw=1.0,
                                    alpha=.22, ls=(0, (4, 4)), zorder=2)
                        run = []
                lab = [p for p in pts if p and inbox(p, 0.05)]
                if lab:
                    p = min(lab, key=lambda q: abs(q[0] - 0.86))
                    T(ax, p[0], p[1] + 0.025, f"{alt}°", 14, GREY, w="normal")
            import random
            random.seed(11)
            xs, ys = [], []
            for _ in range(6000):
                l = random.uniform(0, 360); b = random.gauss(0, 6.2)
                ra, dec = G.gal2eq(l, b)
                al, az = altaz(ra, dec, lst)
                if al < 0:
                    continue
                p = v.xy(al, az)
                if inbox(p):
                    xs.append(p[0]); ys.append(p[1])
            ax.scatter(xs, ys, s=3, c=MW, alpha=.16, lw=0, zorder=1)
            for q, col, lws in self.segs:
                ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=2.2 * lws, alpha=.85,
                        zorder=3, solid_capstyle="round")
            ax.scatter([p[0] for p in self.pts], [p[1] for p in self.pts],
                       s=[p[2] for p in self.pts], c=WHITE, lw=0, zorder=4)
            hz = sorted(p for p in (v.xy(0.0, az / 2) for az in range(0, 720)) if p
                        and -1.05 <= p[0] <= 1.05)
            if hz and any(p[1] > BOX[2] for p in hz):           # 地平線在畫面外就不畫（不要畫出假的地平線）
                poly = [(-1.0, BOX[2])] + [(max(-1.0, min(1.0, x)), max(BOX[2], y)) for x, y in hz] \
                    + [(1.0, BOX[2])]
                ax.add_patch(C.Polygon(poly, closed=True, fc=GROUND, ec="none", zorder=5))
                ax.plot([p[0] for p in hz], [max(BOX[2], p[1]) for p in hz], c=WHITE, lw=2.0,
                        alpha=.75, zorder=6)
            for az in range(0, 360, 15):
                p = v.xy(0.0, az)
                if not (p and -0.95 <= p[0] <= 0.95 and p[1] > BOX[2] + 0.06):
                    continue
                big = az in DIR8
                ax.plot([p[0], p[0]], [p[1], p[1] - (0.035 if big else 0.018)], c=WHITE,
                        lw=1.6, alpha=.7, zorder=6)
                if big:
                    T(ax, p[0], p[1] - 0.075, DIR8[az], 22, AMBER)
            for x, y, txt, pt, col, bold in self.labels:
                T(ax, x, y, txt, pt, col, w="bold" if bold else "normal")
            for fn in self.extra:
                fn(ax)
        return draw

    def target(self, note):
        def draw(ax):
            for p, c, txt, al, tx, ty, ha, rr in self.targets:
                ax.add_patch(C.Circle(p, rr, fill=False, ec=c, lw=3.0, zorder=9))
                sx = rr * (1 if ha == "left" else -1)
                ax.plot([p[0] + sx, tx - 0.01 * (1 if ha == "left" else -1)], [p[1], ty],
                        c=c, lw=1.6, alpha=.8, zorder=9)
                ax.text(tx, ty + 0.025, txt, fontproperties=C.FP, fontsize=21, color=c,
                        ha=ha, va="center", weight="bold", zorder=10)
                ax.text(tx, ty - 0.035, f"仰角 {al:.0f}°", fontproperties=C.FP, fontsize=17,
                        color=WHITE, ha=ha, va="center", zorder=10)
            for i, line in enumerate(note.split("\n")):
                T(ax, 0.0, -0.80 - 0.065 * i, line, 17, WHITE, w="normal")
        return draw


def card(code, name, when, title, az0, alt0, scale, lines, stars, cons, targets, note, extra=(), more=None, sub=SUB):
    lst = lst_at(when)
    v = View(az0, alt0, scale)
    cd = Card(lst, v, lines, stars, cons, targets, extra)
    C.emit("", [("天空", cd.sky(title, sub)), ("目標", cd.target(note))] + (more(lst, v) if more else []),
           title=f"C-B03-{code}_方位_{name}")
    return lst, v


def radiant_rays(lst, v, rad):
    def draw(ax):
        ra0, dec0 = rad
        for i in range(12):
            th = math.radians(i * 30 + 12)
            r0, r1 = (3.0, 11.0) if i % 2 == 0 else (4.5, 15.0)
            pts = []
            for r in (r0, r1):
                ra, dec = B.tangent_pt(ra0, dec0, r * math.sin(th), r * math.cos(th))
                al, az = altaz(ra, dec, lst)
                pts.append(v.xy(al, az))
            if all(p and inbox(p) for p in pts):
                ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], c=WHITE, lw=1.6, alpha=.6,
                        zorder=7)
    return draw


def crescent(when, lst, v):
    """眉月：亮的那一側朝向太陽（地平線下的太陽，在畫面上的方向）"""
    import ephem
    def draw(ax):
        o = obs(when)
        mo, su = ephem.Moon(o), ephem.Sun(o)
        p = v.xy(math.degrees(mo.alt), math.degrees(mo.az))
        q = v.xy(math.degrees(su.alt), math.degrees(su.az))
        if not (p and q):
            return
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        r = 0.032
        ax.add_patch(C.Circle(p, r * 2.8, fc="#FFF6D8", ec="none", alpha=.08, zorder=7))
        ax.add_patch(C.Circle(p, r, fc=DARK_LIMB, ec="none", zorder=7))
        f = mo.phase / 100.0                         # 亮面比例
        th = [-math.pi / 2 + i * math.pi / 40 for i in range(41)]
        limb = [(r * math.cos(t), r * math.sin(t)) for t in th]                 # 亮側半圓（+x＝朝太陽）
        term = [((1 - 2 * f) * r * math.cos(t), r * math.sin(t)) for t in reversed(th)]   # 明暗界線
        poly = limb + term
        ca, sa = math.cos(ang), math.sin(ang)
        poly = [(p[0] + x * ca - y * sa, p[1] + x * sa + y * ca) for x, y in poly]
        ax.add_patch(C.Polygon(poly, closed=True, fc="#FFF6D8", ec="none", zorder=8))
    return draw


def ephem_alt(body, when):
    import ephem
    b = body(); b.compute(obs(when))
    return math.degrees(b.alt)


def transit(ra, dec, day=5):
    """過中天時刻（台灣時間）與仰角（歲差到當天、不含大氣折射）"""
    import ephem
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    o = obs(datetime(2026, 12, day, 12, 0))
    t = o.next_transit(b)
    o.date = t; o.pressure = 0
    b.compute(o)
    return t, math.degrees(b.alt)


def half_up(x):
    """先取到 0.1°，再四捨五入到整數度（71.49→71.5→72）"""
    return int(math.floor(round(x, 1) + 0.5))


def moon_phase(when):
    import ephem
    return ephem.Moon(obs(when)).phase


def cards():
    import ephem
    ev = night_events()
    W1930 = datetime(2026, 12, 5, 19, 30)
    t31, a31 = transit(*B.M31)
    card("01", "1930南方", W1930, "19:30　面向南方", 180.0, 45.0, 0.62,
         ["鯨魚", "飛馬"],
         [(B.FOMALHAUT, "北落師門", "blue", 0.0, -0.05), (B.DIPHDA, "土司空", "blue", 0.0, -0.05),
          (B.MARKAB, "室宿一", "purple", 0.0, -0.05)],
         [("Cet", "鯨魚座", "blue", 0.0, 0.0), ("Psc", "雙魚座", "blue", 0.0, 0.0),
          ("PsA", "南魚座", "blue", 0.0, 0.0), ("Peg", "飛馬座", "purple", 0.0, 0.0)],
         [(B.SATURN, "土星", "amber", (-0.17, 0.03), dict(alt=ephem_alt(ephem.Saturn, W1930))),
          (B.NEPTUNE, "海王星（7.9 等）", "blue", (0.15, -0.07), dict(alt=ephem_alt(ephem.Neptune, W1930), r=0.03))],
         f"土星 {hm(ev['土星中天'])} 過中天（最高）；海王星在土星西邊 6°，要望遠鏡\n"
         f"仙女座大星系 {hm(t31)} 在頭頂偏北（仰角 {half_up(a31)}°）")
    W0040 = datetime(2026, 12, 6, 0, 40)
    t42, a42 = transit(*B.M42)
    tca, aca = transit(*S[CANOPUS][:2])
    tF, aF = transit(*B.NGC2024)
    card("03", "0040南方", W0040, "00:40　面向南方", 180.0, 38.0, 0.58,
         ["獵戶", "金牛"],
         [(B.BETELGEUSE, "參宿四", "amber", 0.0, -0.05), (B.RIGEL, "參宿七", "amber", 0.0, -0.05),
          (B.SIRIUS, "天狼星", "blue", 0.0, -0.05), (B.ALDEBARAN, "畢宿五", "amber", 0.0, -0.05)],
         [("Ori", "獵戶座", "amber", 0.0, 0.0), ("CMa", "大犬座", "blue", 0.0, 0.0), ("Tau", "金牛座", "amber", 0.0, 0.0)],
         [(B.M42, "獵戶座大星雲", "white", (0.17, -0.04), dict(r=0.022)),
          (B.NGC2024, "馬頭／火焰星雲", "white", (-0.19, -0.07), dict(r=0.022)),
          (B.NGC2237, "玫瑰星雲", "white", (-0.15, 0.09), dict(r=0.03)), (CANOPUS, "老人星", "white", (0.15, 0.03), dict(r=0.04))],
         f"獵戶座大星雲 {hm(t42)}、馬頭／火焰 {hm(tF)} 過中天（仰角 {half_up(a42)}–{half_up(aF)}°）\n"
         f"老人星 {hm(tca)} 過中天：正南仰角 {half_up(aca)}°，正好在台東市光害的方向")
    W04 = datetime(2026, 12, 6, 4, 0)
    card("05", "0400東南", W04, "04:00　面向東南（抬頭 60° 以上）", 119.0, 68.0, 1.5,
         ["獅子"],
         [(B.REGULUS, "軒轅十四", "red", 0.0, -0.05), (B.ALGIEBA, "軒轅十二", "red", 0.0, -0.05),
          (B.DENEBOLA, "五帝座一", "red", 0.0, -0.05)],
         [("Leo", "獅子座", "red", 0.0, -0.06)],
         [(B.JUPITER, "木星（−2.2 等）", "white", (0.13, 0.04), dict(alt=ephem_alt(ephem.Jupiter, W04), r=0.02)),
          (B.MARS, "火星（0.4 等）", "red", (-0.12, 0.07), dict(alt=ephem_alt(ephem.Mars, W04), r=0.016))],
         f"木星 {hm(ev['木星升'])}、火星 {hm(ev['火星升'])} 東升（被山擋住會更晚）\n"
         "軒轅十四夾在中間：離木星 3.3°、離火星 4.0°；木星和火星相距 6.9°", sub=SUB_DAWN)
    W0430 = datetime(2026, 12, 6, 4, 30)
    lst6, v6 = lst_at(W0430), View(113.0, 17.0, 1.6)
    card("06", "0430東南東", W0430, "04:30　面向東南東", 113.0, 17.0, 1.6,
         ["室女"],
         [(B.SPICA, "角宿一", "green", 0.0, -0.05)],
         [("Vir", "室女座", "green", 0.0, 0.0)],
         [(B.VENUS, "金星（−4.8 等）", "amber", (-0.36, 0.10), dict(alt=ephem_alt(ephem.Venus, W0430), r=0.024)),
          ((B.MOON[0], B.MOON[1]), f"殘月（亮面 {B.MOON[2]}%）", "white", (0.36, -0.06),
           dict(alt=ephem_alt(ephem.Moon, W0430)))],
         f"金星 {hm(ev['金星升'])}、月亮 {hm(ev['月出'])} 東升（被海岸山脈擋住會更晚）\n"
         f"兩顆相距 11°；月亮的暗面有地照（地球反射的光）；{hm(ev['天亮'])} 天開始亮",
         extra=[crescent(W0430, lst6, v6)], more=lenses, sub=SUB_DAWN)


# ══════════════════════ C-B03-06 鏡頭框（全片幅相機的視野，直線鏡頭） ══════════════════════
LENS = [   # 名稱, 寬°, 高°, 顏色, 中心（"中點"／"月"）, 字的位置
    ("50 mm", 39.6, 27.0, GREEN, "中點", "右上外"), ("85 mm", 23.9, 16.1, BLUE, "中點", "左上內"),
    ("135 mm（直幅）", 10.2, 15.2, AMBER, "中點", "中內"), ("300 mm", 6.9, 4.6, RED, "月", "左中外")]


def lenses(lst, v):
    import ephem
    o = obs(datetime(2026, 12, 6, 4, 30))
    mo, ve = ephem.Moon(o), ephem.Venus(o)
    am, zm = math.degrees(mo.alt), math.degrees(mo.az)
    av, zv = math.degrees(ve.alt), math.degrees(ve.az)

    def frame(alt_c, az_c, wdeg, hdeg):
        f = vec(alt_c, az_c)
        z = math.radians(az_c)
        r = (math.cos(z), -math.sin(z), 0.0)
        u = (r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0])
        tw, th = math.tan(math.radians(wdeg / 2)), math.tan(math.radians(hdeg / 2))
        edge = []
        for x, y in ([(-tw + 2 * tw * i / 30, th) for i in range(31)] + [(tw, th - 2 * th * i / 30) for i in range(31)]
                     + [(tw - 2 * tw * i / 30, -th) for i in range(31)] + [(-tw, -th + 2 * th * i / 30) for i in range(31)]):
            p = [f[k] + x * r[k] + y * u[k] for k in range(3)]
            n = math.sqrt(sum(c * c for c in p))
            al = math.degrees(math.asin(p[2] / n)); az = math.degrees(math.atan2(p[0], p[1])) % 360
            edge.append(v.xy(al, az))
        return edge

    def draw(ax):
        for nm, w, h, col, ctr, where in LENS:
            a0, z0 = ((am + av) / 2, (zm + zv) / 2) if ctr == "中點" else (am, zm)
            e = frame(a0, z0, w, h)
            if not all(e):
                continue
            ax.plot([p[0] for p in e], [p[1] for p in e], c=col, lw=2.4, alpha=.9, zorder=11)
            x0, x1 = min(p[0] for p in e), max(p[0] for p in e)
            y0, y1 = min(p[1] for p in e), max(p[1] for p in e)
            if where == "右上外":
                T(ax, x1, y1 + 0.03, nm, 17, col, ha="right")
            elif where == "左上內":
                T(ax, x0 + 0.015, y1 - 0.03, nm, 17, col, ha="left")
            elif where == "中內":
                T(ax, (x0 + x1) / 2, (y0 + y1) / 2 + 0.01, nm, 15, col)
            else:
                T(ax, x0 - 0.015, (y0 + y1) / 2, nm, 17, col, ha="right")
        T(ax, 0.0, -0.94, "框＝全片幅相機的視野：50、85 mm 輕鬆框住兩顆；135 mm 橫幅很勉強、直幅比較從容；300 mm 只拍得到一顆",
          13.5, WHITE, w="normal")
    return [("鏡頭", draw)]


# ══════════════════════ C-B03-02 縱谷光害（俯視示意，非地圖） ══════════════════════
TOWNS = [   # 名稱, 緯度, 經度, 名稱相對點的位置 (dx, dy), 光的大小（0 小、1 中、2 大）
    ("台東市", 22.755, 121.150, (0.0, -0.10), 2), ("初鹿", 22.822, 121.068, (-0.085, 0.0), 0),
    ("知本", 22.705, 121.060, (-0.085, 0.0), 0), ("鹿野村", 22.911, 121.136, (0.10, -0.02), 0),
    ("關山", 23.048, 121.163, (0.085, 0.0), 1), ("池上", 23.098, 121.220, (0.085, 0.0), 1),
    ("玉里", 23.335, 121.312, (0.085, 0.0), 1)]
RMAX = 55.0                                   # 圖面半徑＝55 公里
RC = 0.60                                     # 圖面半徑（座標單位）
AXIS = 21.0                                   # 縱谷走向（方位角，示意：鹿野村→玉里）


def az_dist(lat, lon):
    p1 = (math.radians(B.LAT), math.radians(B.LON)); p2 = (math.radians(lat), math.radians(lon))
    dl = p2[1] - p1[1]
    y = math.sin(dl) * math.cos(p2[0])
    x = math.cos(p1[0]) * math.sin(p2[0]) - math.sin(p1[0]) * math.cos(p2[0]) * math.cos(dl)
    az = (math.degrees(math.atan2(y, x)) + 360) % 360
    d = 6371 * math.acos(min(1, math.sin(p1[0]) * math.sin(p2[0]) +
                             math.cos(p1[0]) * math.cos(p2[0]) * math.cos(dl)))
    return az, d


def pxy(az, d, cy=-0.02):
    r = RC * d / RMAX
    return r * math.sin(math.radians(az)), cy + r * math.cos(math.radians(az))


def kxy(e, n, cy=-0.02):
    """公里（東、北）→ 圖面"""
    return RC * e / RMAX, cy + RC * n / RMAX


def lp_towns(ax):
    T(ax, 0.0, 0.92, "光害從哪裡來？", 34, WHITE)
    T(ax, 0.0, 0.84, "從觀星點看出去：城鎮的方向與直線距離（示意圖，不是地圖）", 19, GREY, w="normal")
    cy = -0.02
    for dkm in (10, 25, 50):
        ax.add_patch(C.Circle((0, cy), RC * dkm / RMAX, fill=False, ec=WHITE, lw=1.0, alpha=.25,
                              ls=(0, (4, 4)), zorder=2))
        x, y = pxy(300, dkm, cy)
        T(ax, x - 0.012, y + 0.02, f"{dkm} km", 13, GREY, w="normal", ha="right")
    for az, nm in DIR8.items():
        x, y = pxy(az, RMAX * (1.12 if az % 90 == 0 else 1.20), cy)
        T(ax, x, y, nm, 22 if az % 90 == 0 else 17, AMBER if az % 90 == 0 else GREY,
          w="bold" if az % 90 == 0 else "normal")
    ax.add_patch(C.Circle((0, cy), RC, fill=False, ec=WHITE, lw=1.4, alpha=.45, zorder=2))
    for nm, la, lo, (dx, dy), big in TOWNS:
        az, d = az_dist(la, lo)
        x, y = pxy(az, d, cy)
        g1, g2 = {2: (0.16, 0.09), 1: (0.10, 0.06), 0: (0.06, 0.04)}[big]
        for k, a in ((g1, 0.10), (g2, 0.16), (0.03, 0.30)):
            ax.add_patch(C.Circle((x, y), k, fc=AMBER, ec="none", alpha=a, zorder=3))
        ax.add_patch(C.Circle((x, y), 0.012, fc=AMBER, ec="none", zorder=4))
        tx, ty = x + dx, y + dy
        T(ax, tx, ty + 0.014, nm, 17, WHITE)
        T(ax, tx, ty - 0.026, f"{d:.0f} km", 12, GREY, w="normal")
    # 中央山脈另一側的大城市（圖外）
    az, d = az_dist(22.627, 120.301)
    x, y = pxy(az, RMAX * 0.97, cy)
    C.arrow(ax, (x, y), (x * 0.80, cy + (y - cy) * 0.80), c=AMBER, lw=2.0, alpha=.6)
    T(ax, x - 0.01, y - 0.075, "屏東、高雄", 15, AMBER, ha="center")
    T(ax, x - 0.01, y - 0.115, "70–90 km（山的另一邊）", 11, GREY, w="normal", ha="center")
    ax.add_patch(C.Circle((0, cy), 0.022, fc=GREEN, ec=WHITE, lw=1.5, zorder=6))
    T(ax, 0.0, cy + 0.055, "觀星點", 16, GREEN)
    T(ax, 0.0, -0.775, "最亮的光在南方：台東市（約 10 萬人）；北邊的關山、池上、玉里都是小鎮", 17, WHITE, w="normal")


def lp_mountains(ax):
    """示意：縱谷中線（大約通過鹿野村、池上、玉里，走向約北偏東 21°）兩側的山"""
    cy = -0.02
    import numpy as np
    d = (math.sin(math.radians(AXIS)), math.cos(math.radians(AXIS)))     # 沿谷方向（東、北 km）
    w = (-d[1], d[0])                                                      # 往西
    c0 = (2.0, 0.0)                                                        # 中線在觀星點東邊約 2 km

    def band(t0, t1, s0, s1, col, alpha):
        pts = [(c0[0] + s * d[0] + t0 * w[0], c0[1] + s * d[1] + t0 * w[1]) for s in np.linspace(s0, s1, 60)]
        pts += [(c0[0] + s * d[0] + t1 * w[0], c0[1] + s * d[1] + t1 * w[1]) for s in np.linspace(s1, s0, 60)]
        poly = []
        for e, nn in pts:
            r = math.hypot(e, nn)
            if r > RMAX:
                e, nn = e * RMAX / r, nn * RMAX / r
            poly.append(kxy(e, nn, cy))
        ax.add_patch(C.Polygon(poly, closed=True, fc=col, ec="none", alpha=alpha, zorder=1))
    band(4.0, 90.0, -80.0, 80.0, "#7C8BA8", .30)                          # 中央山脈：西側
    band(-5.0, -24.0, -14.0, 80.0, "#7C8BA8", .30)                        # 海岸山脈：東側（南端在台東市北邊）
    T(ax, -0.36, 0.12, "中央山脈", 26, WHITE)
    T(ax, -0.36, 0.06, "西邊：沒有城鎮，但山擋住低空", 14, WHITE, w="normal")
    T(ax, 0.38, -0.10, "海岸山脈", 24, WHITE)
    T(ax, 0.38, -0.16, "東邊：山後面是太平洋", 14, WHITE, w="normal")
    x, y = kxy(c0[0] + 30 * d[0], c0[1] + 30 * d[1], cy)
    T(ax, x - 0.03, y, "縱谷", 16, GREEN, ha="right")
    T(ax, 0.0, -0.84, "東、西兩側最暗，但低空會被山擋住；南方台東市的方向最亮", 17, GREEN)
    T(ax, 0.0, -0.90, "計算點：北緯 22.92°、東經 121.12°（鹿野高台一帶）；山脈位置是示意，距離＝直線距離", 13, GREY,
      w="normal")


# ══════════════════════ 時刻計算（時間表、攝影時間窗共用） ══════════════════════
def night_events():
    import ephem
    t0 = datetime(2026, 12, 5, 12, 0)
    ev = {}
    o = obs(t0); ev["日落"] = o.next_setting(ephem.Sun())
    o = obs(t0); o.horizon = "-18"; ev["天全黑"] = o.next_setting(ephem.Sun(), use_center=True)
    t1 = datetime(2026, 12, 6, 0, 0)
    o = obs(t1); ev["月出"] = o.next_rising(ephem.Moon())
    o = obs(t1); o.horizon = "-18"; ev["天亮"] = o.next_rising(ephem.Sun(), use_center=True)
    o = obs(t1); ev["日出"] = o.next_rising(ephem.Sun())
    o = obs(t0); ev["土星中天"] = o.next_transit(ephem.Saturn())
    o = obs(t0); ev["火星升"] = o.next_rising(ephem.Mars())
    o = obs(t0); ev["木星升"] = o.next_rising(ephem.Jupiter())
    o = obs(t1); ev["金星升"] = o.next_rising(ephem.Venus())
    return ev


TARGETS = [   # 名稱, 編號, (ra, dec) 或行星 key, 門檻仰角
    ("仙女座大星系", "M31", B.M31, 30), ("三角座星系", "M33", B.M33, 30), ("土星", "", "土星", 30),
    ("加州星雲", "NGC 1499", B.NGC1499, 30), ("昴宿星團", "M45", B.M45, 30),
    ("金牛座暗星雲", "B7／B10／B22", B.TAUDARK, 30), ("焰星／蝌蚪星雲", "IC 405／IC 410", B.IC405, 30),
    ("獵戶座大星雲", "M42＋奔跑者 NGC 1977", B.M42, 30), ("馬頭／火焰星雲", "B33／NGC 2024", B.NGC2024, 30),
    ("巴納德環", "Sh2-276", (86.0, -1.0), 30), ("玫瑰星雲", "NGC 2237", B.NGC2237, 30),
    ("錐狀星雲／聖誕樹", "NGC 2264", B.NGC2264, 30), ("木星＋火星", "兩顆都在 30° 以上", "木火", 30),
    ("殘月＋金星", "兩顆都在 10° 以上", "月金", 10),
]
T0, T1 = datetime(2026, 12, 5, 18, 0), datetime(2026, 12, 6, 6, 0)


def target_track(key):
    """18:00–06:00 每 5 分鐘的仰角"""
    import ephem
    out = []
    t = T0
    while t <= T1:
        o = obs(t)
        if key == "月金":
            al = min(math.degrees(ephem.Moon(o).alt), math.degrees(ephem.Venus(o).alt))
        elif key == "木火":
            al = min(math.degrees(ephem.Jupiter(o).alt), math.degrees(ephem.Mars(o).alt))
        elif isinstance(key, str):
            b = {"土星": ephem.Saturn, "木星": ephem.Jupiter}[key](); b.compute(o)
            al = math.degrees(b.alt)
        else:
            al, az = altaz(key[0], key[1], math.degrees(o.sidereal_time()))
        out.append((t, al))
        t += timedelta(minutes=5)
    return out


def tx_of(t):
    """時間 → 圖面 x：18:00＝0、06:00＝1"""
    return (t - T0).total_seconds() / 3600.0 / 12.0


def windows(ax):
    ev = night_events()
    dark0, dark1, mrise = lt(ev["天全黑"]), lt(ev["天亮"]), lt(ev["月出"])
    X0, X1 = 0.36, 0.95
    ax.text(0.5, 0.94, "12/5 攝影目標時間窗", fontproperties=C.FP, fontsize=34, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.905, "仰角 30° 以上的時段・台東鹿野（北緯 22.9°）", fontproperties=C.FP,
            fontsize=15, color=GREY, ha="center", va="center")
    ly = 0.872
    ax.add_patch(C.FancyBboxPatch((0.12, ly - 0.006), 0.05, 0.012, boxstyle="round,pad=0,rounding_size=0.006",
                                  fc=BLUE, ec="none"))
    ax.text(0.18, ly, "暗夜", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    ax.add_patch(C.FancyBboxPatch((0.33, ly - 0.006), 0.05, 0.012, boxstyle="round,pad=0,rounding_size=0.006",
                                  fc=BLUE, ec="none", alpha=.35))
    ax.text(0.39, ly, "天開始亮", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    ax.scatter([0.62], [ly], s=60, c=WHITE, zorder=5)
    ax.text(0.64, ly, "過中天（最高）", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    top, rowh = 0.815, 0.046
    n = len(TARGETS)
    y_end = top - rowh * (n - 1)
    for h in range(18, 31):
        t = T0 + timedelta(hours=h - 18)
        x = X0 + (X1 - X0) * tx_of(t)
        ax.plot([x, x], [y_end - 0.03, top + 0.025], c=WHITE, lw=0.8, alpha=.12, zorder=1)
        if h % 2 == 0:
            ax.text(x, y_end - 0.05, f"{h % 24:02d}", fontproperties=C.FP, fontsize=13, color=GREY,
                    ha="center", va="center")
    for a, b in ((T0, dark0), (dark1, T1)):
        ax.add_patch(C.Rectangle((X0 + (X1 - X0) * tx_of(a), y_end - 0.03),
                                 (X1 - X0) * (tx_of(b) - tx_of(a)), top - y_end + 0.055,
                                 fc="#3A4A6B", ec="none", alpha=.35, zorder=0))
    xm = X0 + (X1 - X0) * tx_of(mrise)
    ax.plot([xm, xm], [y_end - 0.03, top + 0.025], c=AMBER, lw=1.2, alpha=.6, ls=(0, (3, 3)), zorder=2)
    ax.text(xm, y_end - 0.078, f"月出 {hm(ev['月出'])}（亮面 {half_up(moon_phase(mrise))}%）", fontproperties=C.FP, fontsize=12,
            color=AMBER, ha="center", va="center")
    for i, (nm, cat, key, thr) in enumerate(TARGETS):
        y = top - i * rowh
        ax.text(X0 - 0.02, y + (0.008 if cat else 0.0), nm, fontproperties=C.FP, fontsize=14,
                color=WHITE, ha="right", va="center")
        if cat:
            ax.text(X0 - 0.02, y - 0.014, cat, fontproperties=C.FP, fontsize=10.5, color=GREY,
                    ha="right", va="center")
        tr = target_track(key)
        end = T1 if key == "月金" else dark1
        ok = [t for t, al in tr if al >= thr and dark0 <= t <= end]
        if ok:
            a, b = ok[0], ok[-1]
            for s, e, alpha in ((a, min(b, dark1), 1.0), (max(a, dark1), b, .35)):
                if e > s:
                    ax.add_patch(C.FancyBboxPatch(
                        (X0 + (X1 - X0) * tx_of(s), y - 0.009), (X1 - X0) * (tx_of(e) - tx_of(s)), 0.018,
                        boxstyle="round,pad=0,rounding_size=0.008", fc=BLUE, ec="none", alpha=alpha,
                        zorder=3))
        best = max(tr, key=lambda p: p[1])
        if dark0 <= best[0] <= dark1 and key not in ("月金", "木火"):
            ax.scatter([X0 + (X1 - X0) * tx_of(best[0])], [y], s=48, c=WHITE, zorder=5,
                       edgecolors=C.BG, linewidths=1.5)
    ax.text(0.5, 0.115, "仙女座、三角座八點前後最高：先拍；獵戶座一帶午夜過後最高", fontproperties=C.FP,
            fontsize=13, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.085, f"灰底＝天還沒全黑（{hm(ev['天全黑'])} 前）／開始變亮（{hm(ev['天亮'])} 後）", fontproperties=C.FP,
            fontsize=12, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.058, "仰角、時刻由 PyEphem 計算（北緯 22.92°、東經 121.12°）；不含山稜遮擋",
            fontproperties=C.FP, fontsize=11, color=GREY, ha="center", va="center")


# ══════════════════════ C-B03-07 今晚時間表（9:16） ══════════════════════
def timetable(ax):
    import ephem
    ev = night_events()
    tM31, aM31 = transit(*B.M31)
    tM33, aM33 = transit(*B.M33)
    tM45, aM45 = transit(*B.M45)
    tCal, aCal = transit(*B.NGC1499)
    tIC, aIC = transit(*B.IC405)
    tIC2, aIC2 = transit(*B.IC410)
    tM42, aM42 = transit(*B.M42)
    tF, aF = transit(*B.NGC2024)
    tCa, aCa = transit(*S[CANOPUS][:2])
    tRo, aRo = transit(*B.NGC2237)
    tGe, aGe = transit(*B.GEM_R)
    o = obs(datetime(2026, 12, 5, 19, 32)); sa = math.degrees(ephem.Saturn(o).alt)
    rows = [
        (hm(ev["日落"]), "日落", WHITE),
        (hm(ev["天全黑"]), f"天全黑；整晚無月，到清晨 {hm(ev['月出'])} 月出", WHITE),
        (hm(ev["土星中天"]), f"土星最高：正南仰角 {sa:.0f}°（海王星在旁 6°）", AMBER),
        (hm(tM31), f"仙女座大星系：頭頂偏北，仰角 {half_up(aM31)}°", WHITE),
        (hm(tM33), f"三角座星系：頭頂偏北，仰角 {half_up(aM33)}°", WHITE),
        (hm(ev["木星升"]), "木星從東方升起", RED),
        (hm(tM45), f"昴宿星團過頭頂（仰角 {half_up(aM45)}°）；天王星在旁 5°", AMBER),
        (hm(ev["火星升"]), "火星從東方升起", RED),
        (hm(tCal), f"加州星雲：頭頂偏北，仰角 {half_up(aCal)}°", WHITE),
        (f"{hm(tIC)}／{hm(tIC2)}", f"焰星／蝌蚪星雲：頭頂偏北，仰角 {half_up(aIC)}°", WHITE),
        (f"{hm(tM42)}–{hm(tF)}", f"獵戶座大星雲、馬頭、火焰：正南 {half_up(aM42)}–{half_up(aF)}°", AMBER),
        (hm(tCa), f"老人星：正南仰角 {half_up(aCa)}°（台東市光害方向）", WHITE),
        (hm(tRo), f"玫瑰星雲：正南仰角 {half_up(aRo)}°", WHITE),
        (hm(tGe), f"雙子座流星雨輻射點最高（仰角 {half_up(aGe)}°）", WHITE),
        (hm(ev["金星升"]), "金星東升（−4.8 等）", AMBER),
        (hm(ev["月出"]), f"殘月東升（亮面 {half_up(moon_phase(lt(ev['月出'])))}%；被山擋住會更晚）", WHITE),
        ("04:00", "木星、火星：東南方 68–74°，軒轅十四在中間", RED),
        (hm(ev["天亮"]), "天開始變亮", WHITE),
        (hm(ev["日出"]), "日出", WHITE),
    ]
    ax.text(0.5, 0.935, "12/5 星空嘉年華", fontproperties=C.FP, fontsize=36, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.888, "今晚時間表", fontproperties=C.FP, fontsize=30, color=AMBER,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.851, "台東鹿野（北緯 22.9°）・時刻不含山稜遮擋", fontproperties=C.FP,
            fontsize=13, color=GREY, ha="center", va="center")
    y0, dy = 0.805, 0.034
    ax.plot([0.27, 0.27], [y0 + 0.012, y0 - dy * (len(rows) - 1) - 0.012], c=WHITE, lw=1.2, alpha=.35)
    for i, (t, txt, col) in enumerate(rows):
        y = y0 - i * dy
        ax.scatter([0.27], [y], s=50, c=col, zorder=3)
        ax.text(0.235, y, t, fontproperties=C.FP, fontsize=15 if len(t) <= 5 else 11, color=col,
                ha="right", va="center", weight="bold")
        ax.text(0.30, y, txt, fontproperties=C.FP, fontsize=13.5, color=WHITE, ha="left", va="center")
    ax.text(0.5, 0.163, "下一場：12/14（一）晚上 10 點前後雙子座流星雨極大", fontproperties=C.FP,
            fontsize=14, color=AMBER, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.139, "（IMO：14h UT）月亮 21:37 就下山", fontproperties=C.FP,
            fontsize=12, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.108, "外套・紅光手電筒・雙筒望遠鏡・鏡頭加熱帶＋行動電源", fontproperties=C.FP,
            fontsize=16, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.076, "縱谷夜裡濕氣重；望遠鏡先放到外面降溫，看行星才穩", fontproperties=C.FP,
            fontsize=13, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.05, "時刻由 PyEphem 計算（北緯 22.92°、東經 121.12°、海拔 350 m）",
            fontproperties=C.FP, fontsize=11, color=GREY, ha="center", va="center")


def composite(title, layers):
    from PIL import Image
    base = None
    for nm in layers:
        im = Image.open(os.path.join(OUT, f"{title}_{nm}層_透明.png")).convert("RGBA")
        base = im if base is None else Image.alpha_composite(base, im)
    base.save(os.path.join(OUT, f"{title}_合成層_透明.png"))
    print("  ✓", f"{title}_合成層_透明.png")


def main():
    cards()
    C.emit("", [("城鎮", lp_towns), ("山脈", lp_mountains)], title="C-B03-02_縱谷光害")
    for t in ("C-B03-01_方位_1930南方", "C-B03-03_方位_0040南方", "C-B03-05_方位_0400東南"):
        composite(t, ["天空", "目標"])
    f, ax = C.newcard(dark=True)
    windows(ax)
    C.save(f, "", "C-B03-04_攝影時間窗_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    timetable(ax)
    C.save(f, "", "C-B03-07_今晚時間表_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
