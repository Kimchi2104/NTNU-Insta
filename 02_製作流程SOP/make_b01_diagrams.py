# -*- coding: utf-8 -*-
"""B-01 秋觀｜概念圖（方形透明分層＝Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-B01-01_方位_1930西方    → 02 鏡  19:30 抬頭偏西：夏季大三角
  C-B01-02_方位_2200東南    → 06 鏡  22:00 東南方：土星、秋季四邊形
  C-B01-03_方位_0100東北    → 13 鏡  01:00 東北方：英仙、御夫、δ 流星雨輻射點、昴宿
  C-B01-04_方位_0430南方    → 15 鏡  04:30 南方：獵戶、金牛、天狼星
  C-B01-05_方位_0400東方    → 17 鏡  04:00 東方：火星＋蜂巢、木星、軒轅十四
  C-B01-06_土星衝           → 05 鏡  太陽—地球—土星一直線（俯視，非等比例）
  C-B01-07_火星過蜂巢       → 16 鏡  雙筒望遠鏡放大圖：10/10–10/14 清晨 4 點火星的位置
  C-B01-08_今晚時間表       → 18 鏡  9:16 圖卡（可存圖）
輸出：05_素材/B-01_秋觀星空導覽/_概念圖/

方位卡＝真正的地平座標（北緯 24.0°、東經 121.0°）：以面向的方位、仰角為中心的立體投影（stereographic），
畫面上方＝天頂方向、左右＝方位；地平線以下塗黑。恆星用 Hipparcos（Stellarium 星表快取）J2000 位置，
行星與時刻用 PyEphem 當晚自算；文中仰角四捨五入到整數度。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_b01_v4 as B

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/B-01_秋觀星空導覽/_概念圖")
C.set_base(OUT)
RED, GREY, GROUND = "#FF6B6B", "#7C8BA8", "#05070F"
PAL = {"blue": BLUE, "purple": PURPLE, "green": GREEN, "red": RED, "amber": AMBER,
       "white": WHITE}
S = dict(G.load_stars(BASE))
for _k, _h in B.PL_HIP.items():
    S[_h] = B.PLANETS[_k]
LAT = math.radians(B.LAT)


# ══════════════════════ 地平座標與立體投影 ══════════════════════
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
    """面向 az0、視線仰角 alt0 的立體投影；畫面座標 x∈[-1,1]，y 往上；scale＝r=2tan(θ/2) 的縮放"""

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


BOX = (-0.98, 0.98, -0.70, 0.74)          # 天空區（x0,x1,y0,y1）；標題在上、說明在下


def inbox(p, pad=0.0):
    return p and BOX[0] + pad <= p[0] <= BOX[1] - pad and BOX[2] + pad <= p[1] <= BOX[3] - pad


DIR8 = {0: "北", 45: "東北", 90: "東", 135: "東南", 180: "南", 225: "西南", 270: "西", 315: "西北"}


def text_box(txt, pt):
    """字框半寬、半高（座標單位）：圖寬 10.8 in×190 dpi＝2052 px 對應 2 單位"""
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
        self.targets = []
        self.boxes = []                       # 已占用的字框 (x0,x1,y0,y1)
        tset = set()
        for key, txt, col, (dx, dy) in targets:
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
            self.targets.append((p, c, txt, al, tx, ty, ha))
            for t, pt, yy in ((txt, 21, ty + 0.025), (f"仰角 {al:.0f}°", 17, ty - 0.035)):
                hw, hh = text_box(t, pt)
                x0 = tx if ha == "left" else tx - 2 * hw
                self.boxes.append((x0, x0 + 2 * hw, yy - hh, yy + hh))
            self.boxes.append((p[0] - 0.06, p[0] + 0.06, p[1] - 0.06, p[1] + 0.06))
        self.labels = []
        for key, txt, col, dx, dy in cons:    # 星座名：錨在質心，可以離開較遠
            if isinstance(key, tuple):
                ra, dec = key
            else:
                ra, dec = B.centroid(B.uniq([B.W[k] for k in B.CONS[key][0]]), S)
            al, az = altaz(ra, dec, lst)
            p = v.xy(al, az)
            if inbox(p, 0.04) and al > 3:
                self.place(txt, 20, (p[0] + dx, p[1] + dy), PAL.get(col, col), True, far=True)
        for h, txt, col, dx, dy in stars:     # 星名：貼著星
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
            for p, c, txt, al, tx, ty, ha in self.targets:
                ax.add_patch(C.Circle(p, 0.055, fill=False, ec=c, lw=3.0, zorder=9))
                sx = 0.055 * (1 if ha == "left" else -1)
                ax.plot([p[0] + sx, tx - 0.01 * (1 if ha == "left" else -1)], [p[1], ty],
                        c=c, lw=1.6, alpha=.8, zorder=9)
                ax.text(tx, ty + 0.025, txt, fontproperties=C.FP, fontsize=21, color=c,
                        ha=ha, va="center", weight="bold", zorder=10)
                ax.text(tx, ty - 0.035, f"仰角 {al:.0f}°", fontproperties=C.FP, fontsize=17,
                        color=WHITE, ha=ha, va="center", zorder=10)
            T(ax, 0.0, -0.84, note, 17, WHITE, w="normal")
        return draw


SUB = "10/10（六）秋觀・北緯 24°（台灣中部山區）"


def card(code, name, when, title, az0, alt0, scale, lines, stars, cons, targets, note, extra=()):
    lst = B.LST_AT[when]
    v = View(az0, alt0, scale)
    cd = Card(lst, v, lines, stars, cons, targets, extra)
    C.emit("", [("天空", cd.sky(title, SUB)), ("目標", cd.target(note))],
           title=f"C-B01-{code}_方位_{name}")


def cards():
    card("01", "1930西方", "10/10 19:30", "19:30　抬頭偏西", 285.0, 48.0, 0.62,
         ["夏"],
         [(B.VEGA, "織女星", "blue", 0.0, -0.05), (B.ALTAIR, "牛郎星", "blue", 0.0, -0.05),
          (B.DENEB, "天津四", "blue", 0.0, -0.05)],
         [("Cyg", "天鵝座", "blue", 0.10, 0.04), ("Aql", "天鷹座", "blue", 0.0, -0.10),
          ("Lyr", "天琴座", "blue", 0.0, -0.10)],
         [(B.VEGA, "織女星", "blue", (0.16, 0.05)), (B.DENEB, "天津四", "blue", (0.16, 0.05)),
          (B.ALTAIR, "牛郎星", "blue", (-0.16, 0.0))],
         "天一全黑（18:49）就在頭頂偏西；織女、牛郎約 00:45 西沉，天津四約 03:10")
    card("02", "2200東南", "10/10 22:00", "22:00　面向東南", 135.0, 42.0, 0.62,
         ["飛馬", "鯨魚"],
         [(B.MARKAB, "室宿一", "purple", 0.0, -0.05), (B.ALGENIB, "壁宿一", "purple", 0.0, -0.05),
          (B.DIPHDA, "土司空", "blue", 0.0, -0.05)],
         [("Peg", "飛馬座", "purple", 0.0, 0.0), ("Cet", "鯨魚座", "blue", 0.0, 0.0),
          ("Psc", "雙魚座", "blue", 0.0, 0.0)],
         [(B.SATURN, "土星", "amber", (0.17, 0.0))],
         "土星 17:18 東升、23:23 最高（南方仰角 68°）、清晨 5:27 西沉")
    card("03", "0100東北", "10/11 01:00", "01:00　面向東北", 52.0, 40.0, 0.62,
         ["英仙", "御夫", "仙后"],
         [(B.CAPELLA, "五車二", "amber", 0.0, -0.05), (B.MIRFAK, "天船三", "red", 0.0, -0.05),
          (B.ALGOL, "大陵五", "red", 0.0, -0.05), (B.ALDEBARAN, "畢宿五", "amber", 0.0, -0.05)],
         [("Per", "英仙座", "red", 0.0, 0.0), ("Aur", "御夫座", "amber", 0.0, 0.0),
          ("Cas", "仙后座", "green", 0.0, 0.0), ("Tau", "金牛座", "amber", 0.0, 0.0),
          (B.M45, "昴宿星團", "white", 0.0, -0.06)],
         [(B.DAU, "δ 流星雨輻射點", "white", (0.18, -0.08))],
         "輻射點午夜仰角 35°、清晨 4 點近 70°；極大 10/11 清晨，每小時約 2 顆",
         extra=[lambda ax: radiant_rays(ax, B.LST_AT["10/11 01:00"], View(52.0, 40.0, 0.62))])
    card("04", "0430南方", "10/11 04:30", "04:30　面向南方", 180.0, 45.0, 0.62,
         ["獵戶", "御夫"],
         [(B.BETELGEUSE, "參宿四", "amber", 0.0, -0.05), (B.RIGEL, "參宿七", "amber", 0.0, -0.05),
          (B.SIRIUS, "天狼星", "white", 0.0, -0.05), (B.ALDEBARAN, "畢宿五", "amber", 0.0, -0.05)],
         [("Ori", "獵戶座", "amber", 0.0, 0.0), ("Tau", "金牛座", "amber", 0.0, 0.0)],
         [(B.BETELGEUSE, "參宿四", "amber", (-0.20, 0.07)), (B.RIGEL, "參宿七", "amber", (0.18, -0.02))],
         "參宿四 22:20 東升、清晨 4:34 過中天；4:36 天空開始變亮")
    card("05", "0400東方", "10/11 04:00", "04:00　面向東方", 88.0, 33.0, 0.62,
         ["巨蟹"],
         [(B.REGULUS, "軒轅十四", "red", 0.0, -0.05)],
         [("Cnc", "巨蟹座", "red", 0.0, 0.0), ("Leo", "獅子座", "red", 0.0, 0.0)],
         [(B.MARS, "火星＋蜂巢", "red", (0.17, 0.03)), (B.JUPITER, "木星", "white", (0.17, 0.0))],
         "火星 00:39 東升、木星 01:44 東升；04:36 天光前看蜂巢最清楚")


def radiant_rays(ax, lst, v):
    ra0, dec0 = B.DAU
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


# ══════════════════════ C-B01-06 土星衝（俯視，非等比例） ══════════════════════
def helio_lon(body, date):
    import ephem
    b = body(); b.compute(date)
    return math.degrees(b.hlon)


def opp_orbits(ax):
    import ephem
    d = ephem.Date("2026/10/04 12:00")
    sun = ephem.Sun(); sun.compute(d)
    lam_e = (math.degrees(ephem.Ecliptic(sun).lon) + 180.0) % 360.0      # 地球日心黃經
    lam_s = helio_lon(ephem.Saturn, d)
    T(ax, 0.0, 0.92, "10 月 4 日：土星衝", 34, WHITE)
    T(ax, 0.0, 0.84, "從北黃極俯視太陽系（距離非等比例）", 19, GREY, w="normal")
    cx, cy = -0.05, 0.04
    ax.add_patch(C.Circle((cx, cy), 0.075, fc=AMBER, ec="none", zorder=5))
    T(ax, cx, cy - 0.13, "太陽", 20, AMBER)
    for r, col, nm in ((0.22, BLUE, "地球軌道"), (0.56, AMBER, "土星軌道")):
        ax.add_patch(C.Circle((cx, cy), r, fill=False, ec=col, lw=1.6, alpha=.55,
                              ls=(0, (6, 5)) if r > 0.5 else "-", zorder=3))
    for lam, r, col, nm, sz in ((lam_e, 0.22, BLUE, "地球", 0.035), (lam_s, 0.56, AMBER, "土星", 0.045)):
        a = math.radians(lam)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        ax.add_patch(C.Circle((x, y), sz, fc=C.BG, ec=col, lw=2.6, zorder=7))
        if nm == "土星":
            ax.add_patch(C.Ellipse((x, y), sz * 3.6, sz * 1.0, angle=-18.0,
                                   fill=False, ec=col, lw=2.0, zorder=8))
        ox = 0.11 * math.cos(a + math.radians(35)); oy = 0.11 * math.sin(a + math.radians(35))
        T(ax, x + ox, y + oy, nm, 21, col)
    # 公轉方向
    for r in (0.22, 0.56):
        a0 = math.radians(lam_e + 40)
        ax.annotate("", xy=(cx + r * math.cos(a0 + 0.25), cy + r * math.sin(a0 + 0.25)),
                    xytext=(cx + r * math.cos(a0), cy + r * math.sin(a0)),
                    arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.4, alpha=.5))
    T(ax, 0.0, -0.62, "地球公轉較快，大約每 378 天追上土星一次", 18, GREY, w="normal")


def opp_line(ax):
    import ephem
    d = ephem.Date("2026/10/04 12:00")
    sun = ephem.Sun(); sun.compute(d)
    lam = (math.degrees(ephem.Ecliptic(sun).lon) + 180.0) % 360.0
    cx, cy = -0.05, 0.04
    a = math.radians(lam)
    ux, uy = math.cos(a), math.sin(a)
    ax.plot([cx, cx + 0.70 * ux], [cy, cy + 0.70 * uy], c=WHITE, lw=2.4, alpha=.9, zorder=6)
    s = ephem.Saturn(); s.compute(d)
    km = s.earth_distance * 149.5978707e6
    lt = s.earth_distance * 499.004784 / 60.0
    # 說明：放在連線的對側
    T(ax, 0.0, 0.73, "太陽—地球—土星排成一直線", 24, WHITE)
    T(ax, 0.0, -0.71, "日落時土星東升、午夜前後最高、日出時西沉＝整夜可見", 19, AMBER)
    T(ax, 0.0, -0.78, f"地球到土星 {s.earth_distance:.2f} AU ≈ {km/1e8:.1f} 億公里；光走 {lt:.0f} 分鐘", 17,
      WHITE, w="normal")
    T(ax, 0.0, -0.85, "10/10 秋觀：衝後 6 天，亮度 0.35 等（衝日 0.32 等）", 17, WHITE, w="normal")


# ══════════════════════ C-B01-07 火星過蜂巢（雙筒視野） ══════════════════════
FOV_R = 1.5                    # 圖面半徑（度）：放大圖，直徑 3°（雙筒視野 5°～6° 的中央）


def m44_xy(ra, dec):
    ra0, dec0 = B.M44
    x = -((ra - ra0 + 540) % 360 - 180) * math.cos(math.radians(dec0))   # 東在左
    y = dec - dec0
    return x / FOV_R * 0.62, y / FOV_R * 0.62 - 0.02


def m44_field(ax):
    T(ax, 0.0, 0.92, "雙筒望遠鏡裡的蜂巢星團", 34, WHITE)
    T(ax, 0.0, 0.84, "巨蟹座 M44（鬼宿・積屍氣），約 600 光年；放大圖，直徑 3°", 19, GREY, w="normal")
    ax.add_patch(C.Circle((0.0, -0.02), 0.64, fc="#02030A", ec=WHITE, lw=2.4, alpha=1.0, zorder=1))
    ra0, dec0 = B.M44
    xs, ys, ss = [], [], []
    for h, (ra, dec, mg) in S.items():
        if h >= 9_000_000 or mg > 9.5:
            continue
        if abs(dec - dec0) > FOV_R + 0.2:
            continue
        x, y = m44_xy(ra, dec)
        if math.hypot(x, y + 0.02) > 0.63:
            continue
        xs.append(x); ys.append(y); ss.append(max(3.0, (10.2 - mg) ** 2.2 * 3.2))
    ax.scatter(xs, ys, s=ss, c=WHITE, lw=0, zorder=3)
    T(ax, 0.0, 0.67, "北", 18, GREY, w="normal")
    T(ax, -0.70, -0.02, "東", 18, GREY, w="normal")
    T(ax, 0.0, -0.84, "星點：Hipparcos 星表 9.5 等以內的真實位置；北在上、東在左（和抬頭看到的一樣）",
      15, WHITE, w="normal")


def m44_mars(ax):
    import ephem
    pts = []
    for d in range(10, 15):
        when = ephem.Date(ephem.Date(f"2026/10/{d} 04:00") - 8 * ephem.hour)
        m = ephem.Mars(); m.compute(when, epoch=ephem.J2000)
        pts.append((d, math.degrees(m.a_ra), math.degrees(m.a_dec)))
    xy = [m44_xy(ra, dec) for d, ra, dec in pts]
    ax.plot([p[0] for p in xy], [p[1] for p in xy], c=RED, lw=1.4, alpha=.5, ls=(0, (4, 4)), zorder=4)
    for (d, ra, dec), (x, y) in zip(pts, xy):
        hi = d in (11, 12)
        ax.add_patch(C.Circle((x, y), 0.018 if hi else 0.013, fc=RED, ec="none",
                              alpha=1.0 if hi else 0.7, zorder=6))
        T(ax, x, y + (0.06 if d % 2 else -0.06), f"10/{d}", 17 if hi else 14, RED if hi else WHITE,
          w="bold" if hi else "normal")
    T(ax, 0.0, -0.73, "清晨 4 點的火星：10/11 離中心不到半度，10/12 最近", 20, RED)


# ══════════════════════ C-B01-08 今晚時間表（9:16） ══════════════════════
ROWS = [
    ("17:18", "土星從東方升起（整夜可見）", AMBER),
    ("17:34", "日落", WHITE),
    ("18:49", "天全黑・新月，整夜無月光", WHITE),
    ("19:30", "頭頂偏西：夏季大三角", BLUE),
    ("22:00", "土星：東南方仰角 60°；仙后座 W 在北偏東", AMBER),
    ("22:20", "獵戶座參宿四從東方升起", AMBER),
    ("23:23", "土星最高：南方仰角 68°", AMBER),
    ("00:00～", "御夫座 δ 流星雨：輻射點在東北方越升越高", WHITE),
    ("00:39", "火星從東方升起，正走進蜂巢星團", RED),
    ("01:44", "木星從東方升起", WHITE),
    ("04:00", "火星＋蜂巢：東方仰角 44°（雙筒望遠鏡）", RED),
    ("04:34", "參宿四過中天：獵戶座在正南最高", AMBER),
    ("04:36", "天空開始變亮", WHITE),
]


def timetable(ax):
    ax.text(0.5, 0.925, "10/10 秋觀", fontproperties=C.FP, fontsize=40, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.875, "今晚時間表", fontproperties=C.FP, fontsize=30, color=AMBER,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.835, "北緯 24°（台灣中部山區）・全台時刻差不到 5 分鐘", fontproperties=C.FP,
            fontsize=13, color=GREY, ha="center", va="center")
    y0, dy = 0.775, 0.047
    ax.plot([0.25, 0.25], [y0 + 0.012, y0 - dy * (len(ROWS) - 1) - 0.012], c=WHITE, lw=1.2, alpha=.35)
    for i, (t, txt, col) in enumerate(ROWS):
        y = y0 - i * dy
        ax.scatter([0.25], [y], s=60, c=col, zorder=3)
        ax.text(0.21, y, t, fontproperties=C.FP, fontsize=17, color=col, ha="right", va="center",
                weight="bold")
        ax.text(0.285, y, txt, fontproperties=C.FP, fontsize=15.5, color=WHITE, ha="left",
                va="center")
    ax.text(0.5, 0.115, "帶外套・紅光手電筒・雙筒望遠鏡", fontproperties=C.FP, fontsize=19,
            color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.07, "時刻由 PyEphem 計算（北緯 24.0°、東經 121.0°）", fontproperties=C.FP,
            fontsize=11.5, color=GREY, ha="center", va="center")


def composite(title, layers):
    """兩層疊成一張「合成層」：Canva 上一頁就放完（B-01 只有 43 頁可用，定格頁不分兩步揭露）"""
    from PIL import Image
    base = None
    for nm in layers:
        im = Image.open(os.path.join(OUT, f"{title}_{nm}層_透明.png")).convert("RGBA")
        base = im if base is None else Image.alpha_composite(base, im)
    base.save(os.path.join(OUT, f"{title}_合成層_透明.png"))
    print("  ✓", f"{title}_合成層_透明.png")


def main():
    cards()
    C.emit("", [("軌道", opp_orbits), ("衝", opp_line)], title="C-B01-06_土星衝")
    C.emit("", [("星團", m44_field), ("火星", m44_mars)], title="C-B01-07_火星過蜂巢")
    for t in ("C-B01-01_方位_1930西方", "C-B01-02_方位_2200東南", "C-B01-03_方位_0100東北",
              "C-B01-04_方位_0430南方", "C-B01-05_方位_0400東方"):
        composite(t, ["天空", "目標"])
    composite("C-B01-06_土星衝", ["軌道", "衝"])
    composite("C-B01-07_火星過蜂巢", ["星團", "火星"])
    f, ax = C.newcard(dark=True)
    timetable(ax)
    C.save(f, "", "C-B01-08_今晚時間表_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
