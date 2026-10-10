# -*- coding: utf-8 -*-
"""B-02 五校聯合觀星（11/14 新竹尖石）｜概念圖（方形透明分層＝Reels 定格頁；9:16 圖卡＝滿版）
  C-B02-01_方位_1830西南   → 02 鏡  18:30 西南方：眉月、人馬座南斗
  C-B02-02_光害方位        → 03 鏡  光害從哪裡來（城鎮的方位與距離 → 最暗的方向）
  C-B02-03_方位_2100南方   → 05 鏡  21:00 南方：土星、玉夫座星系
  C-B02-04_攝影時間窗      → 07 鏡  9:16 圖卡：各目標仰角 30° 以上的時段（可存圖）
  C-B02-05_方位_0400東方   → 08 鏡  04:00 東方：火星、木星、軒轅十四、獅子座流星雨輻射點
  C-B02-06_火木相合        → 09 鏡  雙筒望遠鏡放大圖（04:00 抬頭看到的方向）＋ 11/12–11/18 火星的位置
  C-B02-07_方位_0500東南東 → 11 鏡  05:00 東南東低空：金星、角宿一
  C-B02-08_今晚時間表      → 13 鏡  9:16 圖卡（可存圖）
輸出：05_素材/B-02_五校聯合觀星/_概念圖/

方位卡＝真正的地平座標（北緯 24.72°、東經 121.19°，新竹尖石煤源一帶）：以面向的方位、仰角為中心的立體投影，
畫面上方＝天頂方向；地平線以下塗黑（數學地平，不含山稜）。恆星 Hipparcos J2000，行星、日月、時刻 PyEphem 自算。
"""
import os, sys, math
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_b02_v4 as B

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/B-02_五校聯合觀星/_概念圖")
C.set_base(OUT)
RED, GREY, GROUND = "#FF6B6B", "#7C8BA8", "#05070F"
PAL = {"blue": BLUE, "purple": PURPLE, "green": GREEN, "red": RED, "amber": AMBER, "white": WHITE}
S = dict(G.load_stars(BASE))
for _k, _h in B.PL_HIP.items():
    S[_h] = B.PLANETS[_k]
LAT = math.radians(B.LAT)
SUB = "11/14（六）五校聯合觀星・新竹尖石（北緯 24.7°）"


# ══════════════════════ 星曆小工具 ══════════════════════
def obs(when):
    """when＝台灣時間 datetime"""
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(B.LAT), str(B.LON); o.elevation = B.ELEV
    o.pressure = 1013; o.temp = 12
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
            if hz:
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


def card(code, name, when, title, az0, alt0, scale, lines, stars, cons, targets, note, extra=()):
    lst = lst_at(when)
    v = View(az0, alt0, scale)
    cd = Card(lst, v, lines, stars, cons, targets, extra)
    C.emit("", [("天空", cd.sky(title, SUB)), ("目標", cd.target(note))],
           title=f"C-B02-{code}_方位_{name}")
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
        ax.add_patch(C.Circle(p, r, fc="#2A2F44", ec="none", zorder=7))
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


def cards():
    import ephem
    ev = night_events()
    W18 = datetime(2026, 11, 14, 18, 30)
    lst, v = lst_at(W18), View(232.0, 30.0, 0.62)
    card("01", "1830西南", W18, "18:30　面向西南", 232.0, 30.0, 0.62,
         ["人馬", "夏"],
         [(B.NUNKI, "斗宿四", "amber", 0.0, -0.05), (B.ALTAIR, "牛郎星", "blue", 0.0, -0.05),
          (B.VEGA, "織女星", "blue", 0.0, -0.05)],
         [("Sgr", "人馬座", "amber", 0.0, -0.10), ("Aql", "天鷹座", "blue", 0.0, 0.0),
          (tuple(B.centroid(B.NANDOU, S)), "南斗", "amber", 0.0, 0.09)],
         [((B.MOON[0], B.MOON[1]), f"眉月（{B.MOON[2]}%）", "white", (-0.17, 0.08),
           dict(alt=ephem_alt(ephem.Moon, W18)))],
         f"{hm(ev['天全黑'])} 天全黑；月亮約 {hm(ev['月沒'])} 沉到地平線（被山擋住會更早）\n"
         f"月落以後整晚無月，到 {hm(ev['天亮'])} 天才開始亮",
         extra=[crescent(W18, lst, v)])
    W21 = datetime(2026, 11, 14, 21, 0)
    card("03", "2100南方", W21, "21:00　面向南方", 180.0, 42.0, 0.62,
         ["鯨魚", "飛馬"],
         [(B.FOMALHAUT, "北落師門", "blue", 0.0, -0.05), (B.DIPHDA, "土司空", "blue", 0.0, -0.05)],
         [("Cet", "鯨魚座", "blue", 0.0, 0.0), ("Psc", "雙魚座", "blue", 0.0, 0.0),
          ("Scl", "玉夫座", "blue", 0.0, 0.0), ("PsA", "南魚座", "blue", 0.0, 0.0)],
         [(B.SATURN, "土星", "amber", (0.17, 0.02), dict(alt=ephem_alt(ephem.Saturn, W21))),
          (B.NGC253, "玉夫座星系", "white", (-0.17, -0.02))],
         "土星 20:56 過中天（最高）；玉夫座星系 21:10 過中天\n仙女座大星系 21:05 在頭頂偏北（仰角 73°）")
    W04 = datetime(2026, 11, 15, 4, 0)
    lst4, v4 = lst_at(W04), View(95.0, 52.0, 2.0)
    card("05", "0400東方", W04, "04:00　面向東方（抬頭 50° 以上）", 95.0, 52.0, 2.0,
         ["獅子"],
         [(B.REGULUS, "軒轅十四", "red", 0.0, -0.05), (B.ALGIEBA, "軒轅十二", "red", 0.0, -0.05),
          (B.DENEBOLA, "五帝座一", "red", 0.0, -0.05)],
         [("Leo", "獅子座", "red", 0.0, -0.06)],
         [(B.MARS, "火星", "red", (-0.11, 0.10), dict(alt=ephem_alt(ephem.Mars, W04), r=0.026)),
          (B.JUPITER, "木星", "white", (0.13, 0.03), dict(alt=ephem_alt(ephem.Jupiter, W04), r=0.032)),
          (B.LEO_R, "獅子座流星雨輻射點", "white", (-0.10, -0.13), dict(r=0.04))],
         f"火星 {hm(ev['火星升'])}、木星 {hm(ev['木星升'])} 東升（被山擋住會更晚）；兩顆相距 1.3°，11/16 最近\n"
         "獅子座流星雨極大：11/17 深夜到 11/18 清晨",
         extra=[radiant_rays(lst4, v4, B.LEO_R)])
    W05 = datetime(2026, 11, 15, 5, 0)
    card("07", "0500東南東", W05, "05:00　面向東南東", 108.0, 19.0, 1.5,
         ["室女"],
         [(B.SPICA, "角宿一", "green", 0.0, -0.05)],
         [("Vir", "室女座", "green", 0.0, 0.0)],
         [(B.VENUS, "金星（−4.4 等）", "amber", (0.15, 0.05), dict(alt=ephem_alt(ephem.Venus, W05), r=0.04))],
         f"金星 {hm(ev['金星升'])} 東升（被山擋住會更晚）；角宿一在旁 1.5°\n"
         f"{hm(ev['天亮'])} 天開始亮、{hm(ev['日出'])} 日出")


# ══════════════════════ C-B02-02 光害方位（俯視示意，非地圖） ══════════════════════
TOWNS = [   # 名稱, 緯度, 經度, 名稱相對點的位置 (dx, dy)
    ("竹東", 24.737, 121.090, (-0.085, -0.01)), ("新竹市", 24.804, 120.968, (-0.105, 0.0)),
    ("竹北", 24.839, 121.004, (-0.02, 0.085)), ("關西", 24.789, 121.177, (-0.085, 0.0)),
    ("龍潭", 24.864, 121.216, (-0.095, 0.0)), ("中壢", 24.965, 121.225, (-0.095, 0.01)),
    ("桃園", 24.993, 121.301, (0.06, 0.075)), ("大溪", 24.881, 121.287, (0.10, -0.01)),
    ("台北", 25.040, 121.560, (0.0, -0.095)), ("頭份", 24.688, 120.913, (-0.10, -0.01))]
RMAX = 55.0                                   # 圖面半徑＝55 公里
RC = 0.60                                     # 圖面半徑（座標單位）


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


def lp_towns(ax):
    T(ax, 0.0, 0.92, "光害從哪裡來？", 34, WHITE)
    T(ax, 0.0, 0.84, "從觀星點看出去：城鎮的方向與直線距離（示意圖，不是地圖）", 19, GREY, w="normal")
    cy = -0.02
    for dkm in (10, 25, 50):
        ax.add_patch(C.Circle((0, cy), RC * dkm / RMAX, fill=False, ec=WHITE, lw=1.0, alpha=.25,
                              ls=(0, (4, 4)), zorder=2))
        x, y = pxy(118, dkm, cy)
        T(ax, x + 0.012, y + 0.02, f"{dkm} km", 13, GREY, w="normal", ha="left")
    for az, nm in DIR8.items():
        x, y = pxy(az, RMAX * (1.12 if az % 90 == 0 else 1.20), cy)
        T(ax, x, y, nm, 22 if az % 90 == 0 else 17, AMBER if az % 90 == 0 else GREY,
          w="bold" if az % 90 == 0 else "normal")
    ax.add_patch(C.Circle((0, cy), RC, fill=False, ec=WHITE, lw=1.4, alpha=.45, zorder=2))
    for nm, la, lo, (dx, dy) in TOWNS:
        az, d = az_dist(la, lo)
        x, y = pxy(az, d, cy)
        big = nm in ("新竹市", "竹北", "中壢", "桃園", "台北")
        for k, a in ((0.11 if big else 0.07, 0.10), (0.065 if big else 0.045, 0.16), (0.03, 0.30)):
            ax.add_patch(C.Circle((x, y), k, fc=AMBER, ec="none", alpha=a, zorder=3))
        ax.add_patch(C.Circle((x, y), 0.012, fc=AMBER, ec="none", zorder=4))
        tx, ty = x + dx, y + dy
        T(ax, tx, ty + 0.014, nm, 17, WHITE)
        T(ax, tx, ty - 0.026, f"{d:.0f} km", 12, GREY, w="normal")
    ax.add_patch(C.Circle((0, cy), 0.022, fc=GREEN, ec=WHITE, lw=1.5, zorder=6))
    T(ax, 0.0, cy - 0.065, "觀星點", 16, GREEN)
    T(ax, 0.0, -0.775, "西邊到北邊：竹東、新竹、竹北、關西、龍潭、中壢、桃園；東北遠方是台北", 17, WHITE, w="normal")


def lp_dark(ax):
    cy = -0.02
    import numpy as np
    a0, a1 = 90.0, 250.0                       # 最暗的半圈：東 → 南 → 西南偏南（往山裡）
    th = np.radians(np.linspace(a0, a1, 80))
    poly = [(0, cy)] + [(RC * math.sin(t), cy + RC * math.cos(t)) for t in th]
    ax.add_patch(C.Polygon(poly, closed=True, fc=GREEN, ec="none", alpha=.16, zorder=1))
    ax.plot([RC * math.sin(t) for t in th], [cy + RC * math.cos(t) for t in th], c=GREEN, lw=4.0,
            alpha=.9, zorder=5, solid_capstyle="round")
    x, y = pxy(165, RMAX * 0.55, cy)
    T(ax, x, y + 0.03, "最暗：東、東南、南", 24, GREEN)
    T(ax, x, y - 0.035, "背對城市、往山裡（雪山山脈方向）", 16, WHITE, w="normal")
    T(ax, 0.0, -0.84, "拍低空目標，盡量挑東到南；西、北方仰角 25° 以下會被光害洗白", 17, GREEN)
    T(ax, 0.0, -0.90, "計算點：北緯 24.72°、東經 121.19°（尖石煤源一帶）；距離＝直線距離", 13, GREY, w="normal")


# ══════════════════════ C-B02-06 火木相合（雙筒視野，04:00 抬頭看到的方向） ══════════════════════
FOV_R = 3.4                     # 圖面半徑（度）：直徑 6.8°，約 7×50 雙筒的視野


def mj_view():
    w = datetime(2026, 11, 15, 4, 0)
    lst = lst_at(w)
    import ephem
    o = obs(w)
    ju = ephem.Jupiter(o); re_ = S[B.REGULUS]
    al_j, az_j = math.degrees(ju.alt), math.degrees(ju.az)
    al_r, az_r = altaz(re_[0], re_[1], lst)
    # 視野中心＝木星與軒轅十四的中點（天頂在上）
    alt0, az0 = (al_j + al_r) / 2 + 0.6, (az_j + az_r) / 2
    v = View(az0, alt0, 1.0)
    k = 0.62 / (2 * math.tan(math.radians(FOV_R) / 2))
    return lst, v, k


def mj_xy(v, k, alt, az):
    p = v.xy(alt, az)
    return (p[0] * k, p[1] * k - 0.02) if p else (9.0, 9.0)


def mj_field(ax):
    import ephem
    lst, v, k = mj_view()
    T(ax, 0.0, 0.92, "雙筒望遠鏡裡的火星、木星、軒轅十四", 32, WHITE)
    T(ax, 0.0, 0.84, "11/15 清晨 4 點，面向東方抬頭看到的方向（上＝天頂）；直徑約 7°", 18, GREY,
      w="normal")
    ax.add_patch(C.Circle((0.0, -0.02), 0.64, fc="#02030A", ec=WHITE, lw=2.4, zorder=1))
    xs, ys, ss = [], [], []
    for h, (ra, dec, mg) in S.items():
        if h >= 9_000_000 or mg > 8.5:
            continue
        al, az = altaz(ra, dec, lst)
        if al < 20:
            continue
        x, y = mj_xy(v, k, al, az)
        if math.hypot(x, y + 0.02) > 0.63:
            continue
        xs.append(x); ys.append(y); ss.append(max(3.0, (9.2 - mg) ** 2.2 * 3.4))
    ax.scatter(xs, ys, s=ss, c=WHITE, lw=0, zorder=3)
    o = obs(datetime(2026, 11, 15, 4, 0))
    for body, col, nm, sz, dx in ((ephem.Jupiter(o), WHITE, "木星 −2.0 等", 0.030, 0.07),
                                  (ephem.Mars(o), RED, "火星 0.7 等", 0.020, -0.07)):
        x, y = mj_xy(v, k, math.degrees(body.alt), math.degrees(body.az))
        ax.add_patch(C.Circle((x, y), sz * 2.2, fc=col, ec="none", alpha=.12, zorder=4))
        ax.add_patch(C.Circle((x, y), sz, fc=col, ec="none", zorder=5))
        T(ax, x + dx, y + 0.005, nm, 19, col, ha="left" if dx > 0 else "right")
    al, az = altaz(S[B.REGULUS][0], S[B.REGULUS][1], lst)
    x, y = mj_xy(v, k, al, az)
    T(ax, x + 0.07, y, "軒轅十四 1.4 等", 18, RED, ha="left")
    T(ax, 0.0, 0.67, "天頂方向", 15, GREY, w="normal")
    T(ax, 0.0, -0.74, "雙筒拿穩（靠在東西上），木星兩側還看得到幾顆木衛（離木星太近，圖上沒畫）", 16, WHITE, w="normal")


def mj_track(ax):
    import ephem
    lst, v, k = mj_view()
    pts = []
    for d in range(13, 19):
        o = obs(datetime(2026, 11, d, 4, 0))
        ma = ephem.Mars(); ma.compute(o.date, epoch=ephem.J2000)
        ju = ephem.Jupiter(); ju.compute(o.date, epoch=ephem.J2000)
        sep = math.degrees(ephem.separation((ma.a_ra, ma.a_dec), (ju.a_ra, ju.a_dec)))
        al, az = altaz(math.degrees(ma.a_ra), math.degrees(ma.a_dec), lst)    # 固定在 11/15 04:00 的星空
        pts.append((d, mj_xy(v, k, al, az), sep))
    ax.plot([p[1][0] for p in pts], [p[1][1] for p in pts], c=RED, lw=1.4, alpha=.5,
            ls=(0, (4, 4)), zorder=6)
    for d, (x, y), sep in pts:
        hi = d in (15, 16)
        if d == 15:
            continue                                  # 11/15 就是視野層畫的那顆火星
        ax.add_patch(C.Circle((x, y), 0.011, fc=RED, ec="none", alpha=1.0 if hi else 0.6, zorder=6))
        T(ax, x - 0.03, y - 0.045, f"{d}", 14, RED if hi else WHITE, w="bold" if hi else "normal")
    best = min(pts, key=lambda p: p[2])
    T(ax, 0.0, -0.81, f"清晨 4 點的火星（數字＝11 月幾日）：15 日相距 {pts[2][2]:.1f}°、"
                      f"{best[0]} 日最近 {best[2]:.1f}°", 17, RED)
    T(ax, 0.0, -0.875, "火星每天往東走約半度（這個角度看是往下）；木星幾乎不動", 15, WHITE, w="normal")


# ══════════════════════ 時刻計算（時間表、攝影時間窗共用） ══════════════════════
def night_events():
    import ephem
    t0 = datetime(2026, 11, 14, 12, 0)
    ev = {}
    o = obs(t0); ev["日落"] = o.next_setting(ephem.Sun())
    o = obs(t0); o.horizon = "-18"; ev["天全黑"] = o.next_setting(ephem.Sun(), use_center=True)
    o = obs(t0); ev["月沒"] = o.next_setting(ephem.Moon())
    t1 = datetime(2026, 11, 15, 0, 0)
    o = obs(t1); o.horizon = "-18"; ev["天亮"] = o.next_rising(ephem.Sun(), use_center=True)
    o = obs(t1); ev["日出"] = o.next_rising(ephem.Sun())
    o = obs(t0); ev["土星中天"] = o.next_transit(ephem.Saturn())
    o = obs(t0); ev["火星升"] = o.next_rising(ephem.Mars())
    o = obs(t0); ev["木星升"] = o.next_rising(ephem.Jupiter())
    o = obs(t0); ev["金星升"] = o.next_rising(ephem.Venus())
    return ev


TARGETS = [   # 名稱, 編號, (ra, dec) 或行星 key
    ("北美星雲", "NGC 7000", B.NGC7000), ("仙女座大星系", "M31", B.M31), ("三角座星系", "M33", B.M33),
    ("玉夫座星系", "NGC 253", B.NGC253), ("土星", "", "土星"), ("英仙座雙星團", "NGC 869／884", (35.2, 57.1)),
    ("昴宿星團", "M45", B.M45), ("加州星雲", "NGC 1499", (60.8, 36.4)),
    ("獵戶座大星雲", "M42＋馬頭 IC 434", B.M42), ("玫瑰星雲", "NGC 2237", B.NGC2237),
    ("蜂巢星團", "M44", B.M44), ("火星＋木星", "", "木星"), ("獅子座三重星系", "M65／M66", (169.8, 13.1)),
]


def target_track(key):
    """18:00–05:00 每 5 分鐘的仰角；回傳 [(datetime, alt)] 與過中天時刻"""
    import ephem
    out = []
    t = datetime(2026, 11, 14, 18, 0)
    while t <= datetime(2026, 11, 15, 5, 0):
        o = obs(t)
        if isinstance(key, str):
            b = {"土星": ephem.Saturn, "木星": ephem.Jupiter}[key](); b.compute(o)
            al = math.degrees(b.alt)
        else:
            al, az = altaz(key[0], key[1], math.degrees(o.sidereal_time()))
        out.append((t, al))
        t += timedelta(minutes=5)
    return out


def tx_of(t):
    """時間 → 圖面 x：18:00＝0、05:00＝1"""
    h = (t - datetime(2026, 11, 14, 18, 0)).total_seconds() / 3600.0
    return h / 11.0


def windows(ax):
    ev = night_events()
    dark0, dark1, moon = lt(ev["天全黑"]), lt(ev["天亮"]), lt(ev["月沒"])
    X0, X1 = 0.35, 0.95
    ax.text(0.5, 0.94, "11/14 攝影目標時間窗", fontproperties=C.FP, fontsize=34, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.905, "仰角 30° 以上的時段・新竹尖石（北緯 24.7°）", fontproperties=C.FP,
            fontsize=15, color=GREY, ha="center", va="center")
    # 圖例（單一色系：深＝無月的暗夜、淺＝月亮還在天上；白點＝過中天）
    ly = 0.872
    ax.add_patch(C.FancyBboxPatch((0.14, ly - 0.006), 0.05, 0.012, boxstyle="round,pad=0,rounding_size=0.006",
                                  fc=BLUE, ec="none"))
    ax.text(0.20, ly, "無月暗夜", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    ax.add_patch(C.FancyBboxPatch((0.37, ly - 0.006), 0.05, 0.012, boxstyle="round,pad=0,rounding_size=0.006",
                                  fc=BLUE, ec="none", alpha=.35))
    ax.text(0.43, ly, "月亮還在（23%）", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    ax.scatter([0.66], [ly], s=60, c=WHITE, zorder=5)
    ax.text(0.68, ly, "過中天（最高）", fontproperties=C.FP, fontsize=12.5, color=WHITE, va="center")
    top, rowh = 0.81, 0.052
    n = len(TARGETS)
    y_end = top - rowh * (n - 1)
    # 時間格線
    for h in range(18, 30):
        t = datetime(2026, 11, 14, 18, 0) + timedelta(hours=h - 18)
        x = X0 + (X1 - X0) * tx_of(t)
        ax.plot([x, x], [y_end - 0.03, top + 0.025], c=WHITE, lw=0.8, alpha=.12, zorder=1)
        if h % 2 == 0:
            ax.text(x, y_end - 0.05, f"{h % 24:02d}", fontproperties=C.FP, fontsize=13, color=GREY,
                    ha="center", va="center")
    # 天光、月光底色
    for a, b, col, al in ((datetime(2026, 11, 14, 18, 0), dark0, "#3A4A6B", .35),
                          (dark1, datetime(2026, 11, 15, 5, 0), "#3A4A6B", .35)):
        ax.add_patch(C.Rectangle((X0 + (X1 - X0) * tx_of(a), y_end - 0.03),
                                 (X1 - X0) * (tx_of(b) - tx_of(a)), top - y_end + 0.055,
                                 fc=col, ec="none", alpha=al, zorder=0))
    xm = X0 + (X1 - X0) * tx_of(moon)
    ax.plot([xm, xm], [y_end - 0.03, top + 0.025], c=AMBER, lw=1.2, alpha=.6, ls=(0, (3, 3)), zorder=2)
    ax.text(xm, top + 0.035, f"月沒 {hm(ev['月沒'])}", fontproperties=C.FP, fontsize=12, color=AMBER,
            ha="center", va="center")
    for i, (nm, cat, key) in enumerate(TARGETS):
        y = top - i * rowh
        ax.text(X0 - 0.02, y + (0.008 if cat else 0.0), nm, fontproperties=C.FP, fontsize=14,
                color=WHITE, ha="right", va="center")
        if cat:
            ax.text(X0 - 0.02, y - 0.014, cat, fontproperties=C.FP, fontsize=10.5, color=GREY,
                    ha="right", va="center")
        tr = target_track(key)
        ok = [t for t, al in tr if al >= 30 and dark0 <= t <= dark1]
        if ok:
            a, b = ok[0], ok[-1]
            for s, e, alpha in ((a, min(b, moon), .35), (max(a, moon), b, 1.0)):
                if e > s:
                    ax.add_patch(C.FancyBboxPatch(
                        (X0 + (X1 - X0) * tx_of(s), y - 0.009), (X1 - X0) * (tx_of(e) - tx_of(s)), 0.018,
                        boxstyle="round,pad=0,rounding_size=0.008", fc=BLUE, ec="none", alpha=alpha,
                        zorder=3))
        best = max(tr, key=lambda p: p[1])
        if dark0 <= best[0] <= dark1:
            ax.scatter([X0 + (X1 - X0) * tx_of(best[0])], [y], s=48, c=WHITE, zorder=5,
                       edgecolors=C.BG, linewidths=1.5)
    ax.text(0.5, 0.115, "西、北方低空有竹東、新竹、桃園的光害：北美星雲越晚越低，先拍", fontproperties=C.FP,
            fontsize=13, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.085, f"灰底＝天還沒全黑（{hm(ev['天全黑'])} 前）／開始變亮（{hm(ev['天亮'])} 後）", fontproperties=C.FP,
            fontsize=12, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.058, "仰角、時刻由 PyEphem 計算（北緯 24.72°、東經 121.19°）；不含山稜遮擋",
            fontproperties=C.FP, fontsize=11, color=GREY, ha="center", va="center")


# ══════════════════════ C-B02-08 今晚時間表（9:16） ══════════════════════
def timetable(ax):
    ev = night_events()
    rows = [
        (hm(ev["日落"]), "日落", WHITE),
        (hm(ev["天全黑"]), "天全黑；眉月（23%）在西南方", WHITE),
        (hm(ev["土星中天"]), "土星最高：正南仰角 66°", AMBER),
        (hm(ev["月沒"]), "月亮下山（被山擋住會更早），之後無月", WHITE),
        ("21:05", "仙女座大星系：頭頂偏北，仰角 73°", WHITE),
        ("21:10", "玉夫座星系：正南仰角 40°", WHITE),
        ("22:07", "北美星雲降到仰角 30° 以下（先拍）", BLUE),
        (f"{hm(ev['火星升'])}／{hm(ev['木星升'])[3:]}", "火星、木星從東方升起", RED),
        ("00:09", "昴宿星團過頭頂（仰角 89°）", AMBER),
        ("01:56", "獵戶座大星雲過中天：正南仰角 60°", AMBER),
        ("02:44", "老人星：正南仰角 13°（要南方山稜夠低）", WHITE),
        ("04:00", "火星＋木星：東方仰角 57°，相距 1.3°", RED),
        ("04:00", "獅子座流星雨輻射點升到仰角 56°", WHITE),
        (hm(ev["天亮"]), "天開始變亮", WHITE),
        ("05:00", "金星：東南東仰角 13°，旁邊 1.5° 是角宿一", AMBER),
        (hm(ev["日出"]), "日出", WHITE),
    ]
    ax.text(0.5, 0.935, "11/14 五校聯合觀星", fontproperties=C.FP, fontsize=36, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.888, "今晚時間表", fontproperties=C.FP, fontsize=30, color=AMBER,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.851, "新竹尖石（北緯 24.7°）・時刻不含山稜遮擋", fontproperties=C.FP,
            fontsize=13, color=GREY, ha="center", va="center")
    y0, dy = 0.800, 0.0415
    ax.plot([0.27, 0.27], [y0 + 0.012, y0 - dy * (len(rows) - 1) - 0.012], c=WHITE, lw=1.2, alpha=.35)
    for i, (t, txt, col) in enumerate(rows):
        y = y0 - i * dy
        ax.scatter([0.27], [y], s=55, c=col, zorder=3)
        ax.text(0.235, y, t, fontproperties=C.FP, fontsize=15.5 if len(t) <= 5 else 13.5, color=col,
                ha="right", va="center", weight="bold")
        ax.text(0.30, y, txt, fontproperties=C.FP, fontsize=14, color=WHITE, ha="left", va="center")
    ax.text(0.5, 0.115, "外套・紅光手電筒・雙筒望遠鏡・鏡頭加熱帶＋行動電源", fontproperties=C.FP,
            fontsize=16, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.078, "東北季風來時雲會從山谷灌上來：出發前看衛星雲圖", fontproperties=C.FP,
            fontsize=13, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.05, "時刻由 PyEphem 計算（北緯 24.72°、東經 121.19°、海拔 500 m）",
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
    C.emit("", [("城鎮", lp_towns), ("暗區", lp_dark)], title="C-B02-02_光害方位")
    C.emit("", [("視野", mj_field), ("軌跡", mj_track)], title="C-B02-06_火木相合")
    for t in ("C-B02-01_方位_1830西南", "C-B02-03_方位_2100南方", "C-B02-05_方位_0400東方",
              "C-B02-07_方位_0500東南東"):
        composite(t, ["天空", "目標"])
    f, ax = C.newcard(dark=True)
    windows(ax)
    C.save(f, "", "C-B02-04_攝影時間窗_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    timetable(ax)
    C.save(f, "", "C-B02-08_今晚時間表_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
