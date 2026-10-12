# -*- coding: utf-8 -*-
"""B-03 行前觀星預報：12/5 星空嘉年華（台東縱谷・鹿野）｜大畫布 v4.6

一晚從黃昏到清晨（畫面往左＝往清晨走）：
  黃昏的土星（19:32 正南 68°，旁邊 6° 是海王星）→ 縱谷的方向與光害 → 頭頂偏北的仙女座大星系、三角座星系
  → 22:46 昴宿到頭頂（天王星在旁 5°）、加州星雲、金牛座暗星雲 → 00:15 御夫座焰星／蝌蚪星雲
  → 00:34–00:42 獵戶座大星雲、馬頭、火焰 → 01:30 玫瑰、01:39 聖誕樹星團、雙子座流星雨輻射點
  → 22:30／22:59 木星、火星東升，04:00 和軒轅十四排成一串 → 03:10 金星、03:46 殘月（亮面約 10%）東升。

觀測地與時間
  台東縣鹿野鄉（鹿野高台一帶），計算點取北緯 22.92°、東經 121.12°、海拔 350 m（位置差幾公里，時刻差不到 1 分鐘）。
  2026/12/5（六）晚上到 12/6（日）清晨。PyEphem 自算（見逐字稿「星空對時」）：
  日落 17:10、天文暮光終 18:30（18:29:34）、月出 03:46（03:45:41；亮面 10%）、天文曙光始 05:03、日出 06:22。

參數
  lst = 75 → 走廊（x=0）＝RA 75°（約 00:00 的子午線，昴宿 x +18、獵戶座大星雲 x −9）。
             往右（西）是土星（x +67）、海王星（+73）、仙女座大星系（+64）、三角座星系（+52）——黃昏的天；
             往左（東）是玫瑰（−23）、雙子座流星雨輻射點（−28）、木星＋火星＋軒轅十四（−74～−81）、
             角宿一（−126）、金星（−134）、月亮（−140，12/6 04:30 的位置）、水星（−162）。
  D_s = 55、D_r = 59 → 五車二 +46.0、仙女座大星系 +41.3、加州星雲 +36.4 都框得進來；北落師門 −29.6、
             天狼星 −16.7 也在帶內。全片只用長圖（盤組照規格輸出、未使用）。
  D_fill = 0 → k=1.848、R_fill=166.3。x_tN = x_tS = 0。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS
from gen_projection import great_circle

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "B-03"
OUT = os.path.join(BASE, "05_素材/B-03_星空嘉年華/_v4大畫布")
LST0 = 75.0
LAT, LON, ELEV = 22.92, 121.12, 350.0
PHI = LAT


# ══════════════════════════════════════════════════════════════════
# 〇、當晚星曆（PyEphem）
# ══════════════════════════════════════════════════════════════════
def at(s):
    """台灣時間 'MM/DD HH:MM' → ephem.Date（UTC）"""
    import ephem
    md, hm = s.split(); mo, d = md.split("/")
    return ephem.Date(ephem.Date(f"2026/{mo}/{d} {hm}") - 8 * ephem.hour)


def site(when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(LAT), str(LON); o.elevation = ELEV
    o.pressure = 0; o.date = at(when)
    return o


def mh_mag(key, body, when):
    """Mallama & Hilton（2018）的行星星等（Stellarium、JPL 用的那一套）；PyEphem 內建公式的金星偏暗約 0.4 等"""
    import ephem
    r, d = body.sun_distance, body.earth_distance
    se = ephem.Sun(); se.compute(when)
    R = se.earth_distance
    i = math.degrees(math.acos(max(-1.0, min(1.0, (r * r + d * d - R * R) / (2 * r * d)))))   # 相位角
    k = 5 * math.log10(r * d)
    if key == "金星":
        return -4.384 - 1.044e-3 * i + 3.687e-4 * i ** 2 - 2.814e-6 * i ** 3 + 8.938e-9 * i ** 4 + k
    if key == "火星":
        return -1.601 + 2.267e-2 * i - 1.302e-4 * i ** 2 + k
    if key == "木星":
        return -9.395 - 3.7e-4 * i + 6.16e-4 * i ** 2 + k
    if key == "水星":
        return (-0.613 + 6.3280e-2 * i - 1.6336e-3 * i ** 2 + 3.3644e-5 * i ** 3 - 3.4265e-7 * i ** 4
                + 1.6893e-9 * i ** 5 - 3.0334e-12 * i ** 6 + k)
    return body.mag


def ephem_night():
    import ephem
    pl = {}
    for key, body, when in (("土星", ephem.Saturn(), "12/05 19:32"),
                            ("海王星", ephem.Neptune(), "12/05 19:07"),
                            ("天王星", ephem.Uranus(), "12/05 23:03"),
                            ("火星", ephem.Mars(), "12/06 04:00"),
                            ("木星", ephem.Jupiter(), "12/06 04:00"),
                            ("金星", ephem.Venus(), "12/06 04:30"),
                            ("水星", ephem.Mercury(), "12/06 05:45")):
        body.compute(at(when), epoch=ephem.J2000)
        mag = body.mag
        if key in ("金星", "火星", "木星", "水星"):
            b2 = type(body)(); b2.compute(at(when))
            mag = mh_mag(key, b2, at(when))
        pl[key] = (math.degrees(body.a_ra), math.degrees(body.a_dec), round(mag, 2))
    o = site("12/06 04:30"); o.epoch = ephem.J2000           # 月亮視差近 1°：用觀測地看到的位置（站心），換到 J2000
    mo = ephem.Moon(); mo.compute(o)                          # ※ a_ra／a_dec 是地心位置，會差 0.6°
    moon = (round(math.degrees(float(mo.ra)), 2), round(math.degrees(float(mo.dec)), 2),
            round(mo.phase))
    lst = {}
    for s in ("12/05 18:30", "12/05 19:32", "12/05 22:46", "12/06 00:00", "12/06 00:38",
              "12/06 01:30", "12/06 04:00", "12/06 04:30"):
        o = site(s)
        lst[s] = math.degrees(o.sidereal_time())
    return pl, moon, lst


PLANETS, MOON, LST_AT = ephem_night()
SATURN, MARS, JUPITER, VENUS, URANUS, NEPTUNE, MERCURY = (9_000_001, 9_000_002, 9_000_003, 9_000_004,
                                                          9_000_005, 9_000_006, 9_000_007)
PL_HIP = {"土星": SATURN, "海王星": NEPTUNE, "天王星": URANUS, "火星": MARS, "木星": JUPITER,
          "金星": VENUS, "水星": MERCURY}

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
FOMALHAUT, DIPHDA, MARKAB, ALPHERATZ, MIRACH, HAMAL = 113368, 3419, 113963, 677, 5447, 9884
ALDEBARAN, ALCYONE, CAPELLA, ELNATH = 21421, 17702, 24608, 25428
BETELGEUSE, RIGEL, BELLATRIX, ALNITAK = 27989, 24436, 25336, 26727
SIRIUS, PROCYON, POLLUX, CASTOR = 32349, 37279, 37826, 36850
REGULUS, ALGIEBA, DENEBOLA, SPICA, ZET_VIR = 49669, 50583, 57632, 65474, 66249

MAINS = [FOMALHAUT, DIPHDA, ALPHERATZ, ALDEBARAN, ALCYONE, CAPELLA, BETELGEUSE, RIGEL,
         SIRIUS, PROCYON, POLLUX, REGULUS, SPICA, SATURN, MARS, JUPITER, VENUS]

# 深空天體（J2000；位置、大小取 SIMBAD／Messier 常用值）
M31 = (10.685, 41.269)            # 仙女座大星系：3.2°×1.0°，位置角 35°
M33 = (23.462, 30.660)            # 三角座星系：70′×40′，位置角 23°
NGC1499 = (60.81, 36.37)          # 加州星雲：約 2.5°×0.7°
M45 = (56.75, 24.12)              # 昴宿星團
TAUDARK = (66.5, 27.5)            # 金牛座暗星雲（B7、B10 在 α 64°、δ +28°；B22 在 α 70°、δ +26°）：只標字
IC405 = (79.07, 34.27)            # 焰星星雲（御夫座 AE 星）
IC410 = (80.68, 33.42)            # 蝌蚪星雲
M42 = (83.82, -5.39)              # 獵戶座大星雲（旁邊 0.5° 是奔跑者星雲 NGC 1977）
NGC2024 = (85.42, -1.85)          # 火焰星雲（馬頭星雲 B33 在南邊 0.6°）
NGC2237 = (97.98, 4.95)           # 玫瑰星雲
NGC2264 = (100.24, 9.90)          # 聖誕樹星團＋錐狀星雲
GEM_R = (103.0, 33.0)             # 雙子座流星雨輻射點：IMO 每日漂移的 12/5 位置（極大 12/14 時約 α 112°、δ +33°）


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium western index.json）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    # 大犬座的線段開頭有 "thin"（Stellarium 的細線標記），只留 HIP 號
    return {c["id"].split()[-1]: [[h for h in seg if isinstance(h, int)] for seg in c["lines"]]
            for c in d["constellations"]}


W = sc_lines("western")
LG_PEG = [(W["Peg"], "purple", 1.0), (W["And"], "purple", 1.0), (W["Tri"], "purple", 1.0)]
LG_CET = [(W["Psc"], "blue", 0.8), (W["Cet"], "blue", 1.0), (W["PsA"], "blue", 0.8)]
LG_TAU = [(W["Tau"], "amber", 1.0), (W["Per"], "red", 0.7), (W["Aur"], "amber", 0.7)]
LG_ORI = [(W["Ori"], "amber", 1.0), (W["CMa"], "blue", 0.8)]
LG_GEM = [(W["Gem"], "green", 0.8), (W["Mon"], "purple", 0.7), (W["CMi"], "white", 0.7)]
LG_LEO = [(W["Leo"], "red", 1.0), (W["Cnc"], "red", 0.7)]
LG_VIR = [(W["Vir"], "green", 1.0)]
LG_ALL = LG_PEG + LG_CET + LG_TAU + LG_ORI + LG_GEM + LG_LEO + LG_VIR
LINE_SETS = [(LG_PEG, "連線-飛馬仙女"), (LG_CET, "連線-雙魚鯨魚"), (LG_TAU, "連線-金牛英仙御夫"),
             (LG_ORI, "連線-獵戶大犬"), (LG_GEM, "連線-雙子麒麟小犬"), (LG_LEO, "連線-獅子巨蟹"),
             (LG_VIR, "連線-室女")]
LINES_KEY = {"L4": "星座連線", "飛馬": "連線-飛馬仙女", "鯨魚": "連線-雙魚鯨魚",
             "金牛": "連線-金牛英仙御夫", "獵戶": "連線-獵戶大犬", "雙子": "連線-雙子麒麟小犬",
             "獅子": "連線-獅子巨蟹", "室女": "連線-室女",
             "深空": "深空天體", "行星": "行星標記", "流星": "流星雨輻射點", "月": "月亮（12-06 04-30）"}
LINE_GROUPS = {"L4": LG_ALL, "飛馬": LG_PEG, "鯨魚": LG_CET, "金牛": LG_TAU, "獵戶": LG_ORI,
               "雙子": LG_GEM, "獅子": LG_LEO, "室女": LG_VIR}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg if isinstance(h, int)})


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（台灣通行譯名）
# ══════════════════════════════════════════════════════════════════
CONS = {   # 星座名：(連線 key 群, 中文, 顏色, dx, dy)
    "Peg": (["Peg"], "飛馬座", "purple", 4.0, -9.0),
    "And": (["And"], "仙女座", "purple", -3.0, 6.0),
    "Tri": (["Tri"], "三角座", "purple", -2.4, -2.0),
    "Psc": (["Psc"], "雙魚座", "blue", 0.0, 0.0),
    "Cet": (["Cet"], "鯨魚座", "blue", -4.0, -6.0),
    "PsA": (["PsA"], "南魚座", "blue", 0.0, -4.0),
    "Tau": (["Tau"], "金牛座", "amber", 2.0, -8.0),
    "Per": (["Per"], "英仙座", "red", -4.0, 2.0),
    "Aur": (["Aur"], "御夫座", "amber", -3.0, 2.0),
    "Ori": (["Ori"], "獵戶座", "amber", -2.0, 0.0),
    "CMa": (["CMa"], "大犬座", "blue", 0.0, -8.0),
    "Gem": (["Gem"], "雙子座", "green", 0.0, 0.0),
    "Mon": (["Mon"], "麒麟座", "purple", -3.0, -6.0),
    "CMi": (["CMi"], "小犬座", "white", 0.0, -3.0),
    "Cnc": (["Cnc"], "巨蟹座", "red", 0.0, -6.0),
    "Leo": (["Leo"], "獅子座", "red", -2.0, 9.0),
    "Vir": (["Vir"], "室女座", "green", 0.0, 8.0),
}

ZH = {FOMALHAUT: "北落師門", DIPHDA: "土司空", MARKAB: "室宿一", ALPHERATZ: "壁宿二",
      ALDEBARAN: "畢宿五", CAPELLA: "五車二", BETELGEUSE: "參宿四", RIGEL: "參宿七",
      SIRIUS: "天狼星", PROCYON: "南河三", POLLUX: "北河三", REGULUS: "軒轅十四",
      SPICA: "角宿一"}
COLOR = {FOMALHAUT: "blue", DIPHDA: "blue", MARKAB: "purple", ALPHERATZ: "purple", ALDEBARAN: "amber",
         CAPELLA: "amber", BETELGEUSE: "amber", RIGEL: "amber", SIRIUS: "blue",
         PROCYON: "white", POLLUX: "green", REGULUS: "red", SPICA: "green"}
OFF = {FOMALHAUT: (4.6, 0.0), DIPHDA: (4.4, -0.4), MARKAB: (4.4, -1.0), ALPHERATZ: (2.45, 1.4),
       ALDEBARAN: (-0.2, -2.4), CAPELLA: (-4.4, 0.8), BETELGEUSE: (-2.35, -2.0), RIGEL: (4.4, -0.6),
       SIRIUS: (1.0, 2.0), PROCYON: (-4.4, 0.0), POLLUX: (-4.4, 0.6), REGULUS: (0.0, -2.9),
       SPICA: (0.0, -2.6)}

PL_COLOR = {"土星": "amber", "海王星": "blue", "天王星": "green", "火星": "red", "木星": "white",
            "金星": "amber", "水星": "purple"}
# 行星圈半徑＝max(1.3, 星點×3.5)：木星 2.2°、金星 3.5°；字一律放在圈外
PL_OFF = {"土星": (-3.6, -0.4), "海王星": (3.2, -0.6), "天王星": (0.0, -2.0), "火星": (-3.6, 0.0),
          "木星": (4.6, 0.0), "金星": (-5.6, 2.0), "水星": (0.0, 3.4)}
OBJ = {    # 天體：(ra, dec, 文字, 顏色, dx, dy)
    "M31": (*M31, "仙女座大星系", "white", 0.0, -3.0),
    "M33": (*M33, "三角座星系", "white", 0.0, -2.4),
    "NGC1499": (*NGC1499, "加州星雲", "white", -1.2, 2.0),
    "M45": (*M45, "昴宿星團", "white", 0.0, 2.8),
    "TAUD": (*TAUDARK, "金牛座暗星雲", "white", 0.0, 0.0),
    "IC405": (*IC405, "焰星星雲", "white", 0.0, 1.6),
    "IC410": (*IC410, "蝌蚪星雲", "white", 0.0, -1.6),
    "M42": (*M42, "獵戶座大星雲", "white", 9.6, -0.4),
    "NGC2024": (*NGC2024, "馬頭／火焰星雲", "white", -5.6, 0.0),
    "NGC2237": (*NGC2237, "玫瑰星雲", "white", 1.2, -2.8),
    "NGC2264": (*NGC2264, "聖誕樹星團", "white", 0.0, -1.6),
    "GEM": (*GEM_R, "雙子座流星雨輻射點", "white", 0.0, 2.0),
}


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節＋希臘字母）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏ]+|[α-ω]|\d+|[㐀-鿿]", t):
        if re.match(r"[㐀-鿿]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouy]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、自訂圖層：深空天體、行星標記、流星雨輻射點、月亮（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    """以 (ra0,dec0) 為切點的小角度偏移（度）→ (ra, dec)；x 向東、y 向北"""
    dec = dec0 + y
    ra = ra0 + x / max(0.05, math.cos(math.radians(dec0)))
    return ra % 360, dec


def ellipse(ra0, dec0, a, b, pa, n=48):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        u, v = a * math.cos(t), b * math.sin(t)
        th = math.radians(pa)
        x = u * math.sin(th) + v * math.cos(th)
        y = u * math.cos(th) - v * math.sin(th)
        pts.append(tangent_pt(ra0, dec0, x, y))
    return pts


def cluster_stars(S, ra0, dec0, rad, vmax):
    out = []
    c = math.cos(math.radians(dec0))
    for h, (ra, dec, v) in S.items():
        if v > vmax or h >= 9_000_000:
            continue
        if abs(dec - dec0) > rad or math.hypot((ra - ra0) * c, dec - dec0) > rad:
            continue
        out.append((ra, dec, v))
    return out


def pl_ring(m, key, v):
    return 0.9 if key in ("天王星", "海王星") else max(1.3, m.sz_star(v) * 3.5)


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*M31, 1.6, 0.5, 35.0), (*M33, 0.55, 0.35, 23.0),
                                      (*NGC1499, 1.2, 0.33, 120.0), (*IC405, 0.3, 0.22, 0.0),
                                      (*IC410, 0.32, 0.3, 0.0), (*M42, 0.5, 0.45, 0.0),
                                      (*NGC2024, 0.25, 0.25, 0.0), (*NGC2237, 0.7, 0.7, 0.0),
                                      (*NGC2264, 0.35, 0.2, 0.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.14), (0.42, 0.22), (0.2, 0.35)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        for (ra0, dec0, rad, vmax) in [(*M45, 1.1, 8.5)]:
            for k, op in ((1.0, 0.07), (0.6, 0.10)):
                s.poly_fill(runs(ellipse(ra0, dec0, rad * k, rad * k, 0.0)), fill=mw, opacity=op)
            dots = []
            for ra, dec, v in cluster_stars(S, ra0, dec0, rad, vmax):
                if v <= m.maglim:
                    continue
                for p in pos(ra, dec):
                    dots.append((p[0], p[1], 0.05 + 0.028 * (vmax - v)))
            if dots:
                s.dots(dots, fill="#FFFFFF", opacity=0.85)

    def planets(s, pos, runs):
        for key, h in PL_HIP.items():
            ra, dec, v = S[h]
            r = pl_ring(m, key, v)
            for p in pos(ra, dec):
                s.circle(p[0], p[1], r, stroke=COLORS[PL_COLOR[key]], w=0.12, opacity=0.95)

    def radiant(s, pos, runs):
        for ra0, dec0 in (GEM_R,):
            for p in pos(ra0, dec0):
                s.circle(p[0], p[1], 0.9, stroke=COLORS["white"], w=0.10, opacity=0.9)
            segs = []
            for i in range(12):
                th = math.radians(i * 30 + 12)
                r0, r1 = (2.2, 7.5) if i % 2 == 0 else (3.2, 10.5)
                a = tangent_pt(ra0, dec0, r0 * math.sin(th), r0 * math.cos(th))
                b = tangent_pt(ra0, dec0, r1 * math.sin(th), r1 * math.cos(th))
                segs += runs(great_circle(*a, *b))
            s.polylines(segs, stroke=COLORS["white"], w=0.14, opacity=0.75)

    def circle(ra0, dec0, r, n=48):
        return [tangent_pt(ra0, dec0, r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n))
                for i in range(n + 1)]

    def moon(s, pos, runs):
        ra0, dec0 = MOON[0], MOON[1]
        for k, op in ((2.6, 0.05), (1.8, 0.08), (1.25, 0.14)):
            s.poly_fill(runs(circle(ra0, dec0, 0.28 * k)), fill="#FFF6D8", opacity=op)
        s.poly_fill(runs(circle(ra0, dec0, 0.28)), fill="#FFF6D8", opacity=1.0)

    return [("深空天體", deep), ("行星標記", planets), ("流星雨輻射點", radiant),
            ("月亮（12-06 04-30）", moon)]


def write_custom(m, S, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n),
                   lambda pts, n=north: m._runs_disc(pts, n))
                m._write_disc(s, north, name)


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    for k, h in PL_HIP.items():
        S[h] = PLANETS[k]
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=55, D_r=59, D_fill=0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def star_items(size, only=None):
        out = []
        for h, txt in ZH.items():
            if only is not None and h not in only:
                continue
            dx, dy = OFF.get(h, (0.0, 2.4))
            w, _ = MC.label_box(txt, size, m.fu)
            if abs(dx) > 0.1:
                dx = math.copysign(abs(dx) * size / 1.1 + w / 2 - 1.6, dx)
            else:
                dy = dy * size / 1.1
            out.append({"hip": h, "text": txt, "color": COLOR.get(h, "white"), "size": size,
                        "dx": round(dx, 2), "dy": round(dy, 2), "key": f"HIP {h}"})
        for key, h in PL_HIP.items():
            if only is not None and h not in only:
                continue
            sz = size * (0.9 if key in ("天王星", "海王星") else 1.15)
            dx, dy = PL_OFF[key]
            w, _ = MC.label_box(key, sz, m.fu)
            if abs(dx) > 0.1:
                dx = math.copysign(abs(dx) * size / 1.1 + w / 2 - 1.6, dx)
            out.append({"ra": S[h][0], "dec": S[h][1], "text": key, "color": PL_COLOR[key],
                        "size": round(sz, 2), "dx": round(dx, 2), "dy": dy, "key": key})
        if only is None or "月" in only:
            txt = f"月亮（{MOON[2]}%）"
            out.append({"ra": MOON[0], "dec": MOON[1], "text": txt, "color": "white",
                        "size": round(size * 1.15, 2), "dx": 0.0, "dy": -2.8, "key": "月"})
        return out

    def cons_items(size, only=None):
        out = []
        for ab, (keys, zh, col, dx, dy) in CONS.items():
            if only is not None and ab not in only:
                continue
            ra, dec = centroid(uniq([W[k] for k in keys]), S)
            sc = size / 1.6
            out.append(dict(ra=ra, dec=dec, text=zh, color=col, size=size, dx=dx * sc, dy=dy * sc, key=ab))
        return out

    def obj_items(size, only=None):
        out = []
        for k, (ra, dec, txt, col, dx, dy) in OBJ.items():
            if only is not None and k not in only:
                continue
            out.append(dict(ra=ra, dec=dec, text=txt, color=col, size=size, dx=dx, dy=dy, key=k))
        return out

    label_sets = [
        (cons_items(1.6), "星座名"),
        (star_items(1.1), "亮星名"),
        (obj_items(1.0), "天體"),
    ]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, S, custom)
    m.L_marks(MAINS, "主角星白點", "dot")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot")])
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    xm = x_of(MOON[0])
    OPEN0 = (96.0, 4.0, 48.0, 0.0)                           # 開場：黃昏的西南半天（北落師門、飛馬）
    OPEN1 = (78.0, 4.0, 48.0, 0.0)
    SAT_F = (70.0, 0.0, 24.0, 0.0)                           # 土星＋海王星
    DIR_F = (66.0, 6.0, 50.0, 0.0)                           # 黃昏全景（疊縱谷光害卡）
    AND_F = (60.0, 19.0, 40.0, 0.0)                          # 仙女座大星系＋三角座星系
    PLE_F = (12.0, 26.0, 32.0, 0.0)                          # 昴宿＋天王星＋加州星雲＋金牛座暗星雲
    ORI_F = (-8.0, 12.0, 40.0, 0.0)                          # 御夫座焰星／蝌蚪＋獵戶
    MON_F = (-26.0, 12.0, 36.0, 0.0)                         # 玫瑰、聖誕樹、雙子座流星雨輻射點
    MJ_F = (-77.3, 12.8, 22.0, 0.0)                          # 木星、軒轅十四、火星（兩側的字都要在畫面內）
    DAWN_F = (round(xm + 4.0, 1), -13.0, 30.0, 0.0)           # 殘月、金星、角宿一
    WIDE_F = (-70.0, 2.0, 52.0, 0.0)                         # 東半天全景
    END_F = (-10.0, 4.0, 52.0, 0.0)

    shots = [
        dict(code="01", kind="S", sec=14, north=True,
             frames=[OPEN0, OPEN1], layers=["深空", "行星"], labels=[],
             vo="十二月五日星空嘉年華，在台東縱谷。月亮要到清晨三點四十六分才升起，"
                "天全黑以後，有九個多小時是暗的。全台天文社都在的那晚，天上有什麼？",
             card="12/5 星空嘉年華｜全台天文社都在的那晚，天上有什麼？",
             note="開場字卡；黃昏的西南半天往東緩慢平移（畫面往左＝往清晨走），先不開連線"),
        dict(code="02", kind="Z", sec=14, north=True,
             frames=[OPEN1, SAT_F], layers=["鯨魚", "深空", "行星"], labels=["亮星名"],
             overlay="C-B03-01_方位_1930南方", overlay_layers=["合成層"],
             vo="五點十分日落，六點半天全黑。第一個看土星：七點半升到正南，仰角六十八度；"
                "環只斜六度，是扁扁的一圈。旁邊六度還有海王星，要望遠鏡才看得到。",
             note="推近土星（琥珀圈）與海王星（藍圈），在雙魚座與鯨魚座交界；結束後疊方位卡 19:30（南方）"),
        dict(code="03", kind="Z", sec=12, north=True,
             frames=[SAT_F, DIR_F], labels_start=["亮星名"],
             layers=["飛馬", "鯨魚", "深空", "行星"], labels=["星座名", "亮星名"],
             overlay="C-B03-02_縱谷光害", overlay_layers=["城鎮層", "山脈層"],
             vo="先認方向：縱谷西邊是中央山脈，東邊是海岸山脈，低空都會被山擋住。"
                "最亮的光害在南方的台東市；北邊的關山、池上小得多。",
             note="拉遠成黃昏全景；結束後疊縱谷光害卡（兩層：城鎮 → 兩側山脈）"),
        dict(code="04", kind="Z", sec=13, north=True,
             frames=[DIR_F, AND_F], labels_start=["星座名", "亮星名"],
             layers=["飛馬", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             vo="天一黑，仙女座大星系就在頭頂偏北：七點四十三分，仰角七十二度；三角座星系更高，八十二度。"
                "這兩個要先拍：午夜到一點，就降到三十度以下。",
             note="往北（上）滑到仙女座大星系、三角座星系（19:42、20:33 過中天）"),
        dict(code="05", kind="Z", sec=15, north=True,
             frames=[AND_F, PLE_F], labels_start=["星座名", "亮星名", "天體"],
             layers=["金牛", "深空", "行星"], labels=["亮星名", "天體"],
             vo="十點四十六分，昴宿星團升到正頭頂，仰角將近九十度。旁邊五度是天王星，五點六等，"
                "用雙筒就找得到。北邊的加州星雲、東邊的金牛座暗星雲，也都在頭頂附近。",
             note="往東（左）滑到昴宿（22:46 過中天）；天王星（綠圈）在昴宿東南 5°"),
        dict(code="06", kind="Z", sec=14, north=True,
             frames=[PLE_F, ORI_F], labels_start=["亮星名", "天體"],
             layers=["獵戶", "金牛", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             overlay="C-B03-03_方位_0040南方", overlay_layers=["合成層"],
             vo="十二點多，御夫座的焰星、蝌蚪星雲經過頭頂；十二點半到四十分，獵戶座大星雲、奔跑者、"
                "馬頭和火焰星雲一個個升到正南，仰角六十二到六十五度。",
             note="往下（南）滑到御夫座焰星／蝌蚪星雲與獵戶座；結束後疊方位卡 00:40（南方）"),
        dict(code="07", kind="Z", sec=13, north=True,
             frames=[ORI_F, MON_F], labels_start=["星座名", "亮星名", "天體"],
             layers=["雙子", "獵戶", "流星", "深空", "行星"], labels=["星座名", "天體"],
             overlay="C-B03-04_攝影時間窗",
             vo="一點半，玫瑰星雲到正南，仰角七十二度；一點四十分，錐狀星雲和聖誕樹星團接著到。"
                "雙子座流星雨的輻射點，兩點前後升到最高，將近八十度。",
             note="往東滑到麒麟座、雙子座；輻射點（流星雨輻射點層）在北河二西南；結束後疊 9:16 攝影時間窗（可存圖）"),
        dict(code="08", kind="Z", sec=12, north=True,
             frames=[MON_F, MON_F], labels_start=["星座名", "天體"],
             layers=["雙子", "獵戶", "流星", "深空", "行星"], labels=["星座名", "天體"],
             vo="不過今晚離極大還有九天，流星不多。真正的極大在十四日晚上九點多，"
                "月亮九點半多就下山，是今年條件很好的一次，記得再出來。",
             note="定格在雙子座流星雨輻射點（畫面不動，字幕帶 12/14 21:50 極大、21:37 月沒）"),
        dict(code="09", kind="Z", sec=13, north=True,
             frames=[MON_F, MJ_F], labels_start=["星座名", "天體"],
             layers=["獅子", "深空", "行星"], labels=["星座名", "亮星名"],
             labels_end=["亮星名"],
             overlay="C-B03-05_方位_0400東南東", overlay_layers=["合成層"],
             vo="晚上十點半木星東升，十一點火星跟上。清晨四點，兩顆高掛在東南東，仰角七十度上下；"
                "軒轅十四剛好夾在中間：木星離它三度，火星四度。",
             note="往東滑到獅子座並推近：木星（白圈）、軒轅十四、火星（紅圈）排成一串；結束後疊方位卡 04:00（東南東）"),
        dict(code="10", kind="Z", sec=13, north=True,
             frames=[MJ_F, DAWN_F], labels_start=["亮星名"],
             layers=["室女", "月", "深空", "行星"], labels=["亮星名"],
             vo="三點十分，金星先從東方升起，負四點八等；三點四十六分，一成亮的殘月跟上，"
                "被海岸山脈擋住，要再晚一點才露臉。金星在月亮上方十一度。",
             note="往東滑到室女座：金星（12/6 04:30 的位置）、月亮（04:30）、角宿一"),
        dict(code="11", kind="Z", sec=14, north=True,
             frames=[DAWN_F, DAWN_F], labels_start=["亮星名"],
             layers=["室女", "月", "深空", "行星"], labels=["亮星名"],
             overlay="C-B03-06_方位_0430東南東", overlay_layers=["天空層", "目標層", "鏡頭層"],
             vo="月亮的暗面被地球反射的光照亮，叫地照。兩顆相距十一度，用五十到八十五毫米的鏡頭"
                "就能框在一起，四點半到五點最好拍；五點零三分，天就開始亮了。",
             note="定格；疊方位卡 04:30（東南東）三層：天空 → 目標 → 50／85／135 mm 鏡頭框"),
        dict(code="12", kind="Z", sec=11, north=True,
             frames=[DAWN_F, WIDE_F], labels_start=["亮星名"],
             layers=["L4", "月", "深空", "行星", "流星"], labels=[],
             vo="縱谷的夜很潮濕，鏡頭要掛加熱帶、帶足行動電源。看行星要等望遠鏡跟外面一樣冷，"
                "影像才會穩；出發前先看雲圖。",
             note="拉遠成東半天全景（全部連線）；這格沒有標籤，留給字幕"),
        dict(code="13", kind="Z", sec=9, north=True,
             frames=[WIDE_F, END_F],
             layers=["L4", "深空", "行星", "流星"], labels=[],
             overlay="C-B03-07_今晚時間表",
             vo="土星、仙女座、頭頂的昴宿和獵戶，天亮前的木星、火星，還有月亮和金星——十二月五日，台東見。",
             card="12/5 台東見｜追蹤師大天文社",
             note="往西拉回、全部連線亮起；疊 9:16 今晚時間表（可存圖）；端卡＋追蹤 CTA"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"]
        print(f"  {sh['code']}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u/tot_s:.2f} 字/秒")
    m.check_shots(shots)

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            ew = 360.0 / fov * 1080
            off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "大畫布圖層組", "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1),
                         "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  x：土星 %+.1f、海王星 %+.1f、仙女座大星系 %+.1f、三角座星系 %+.1f、昴宿六 %+.1f、天王星 %+.1f、"
          "獵戶座大星雲 %+.1f、玫瑰 %+.1f、輻射點 %+.1f、木星 %+.1f、軒轅十四 %+.1f、火星 %+.1f、"
          "角宿一 %+.1f、金星 %+.1f、月亮 %+.1f（dec %+.1f，%d%%）、水星 %+.1f" % (
              x_of(S[SATURN][0]), x_of(S[NEPTUNE][0]), x_of(M31[0]), x_of(M33[0]), x_of(S[ALCYONE][0]),
              x_of(S[URANUS][0]), x_of(M42[0]), x_of(NGC2237[0]), x_of(GEM_R[0]), x_of(S[JUPITER][0]),
              x_of(S[REGULUS][0]), x_of(S[MARS][0]), x_of(S[SPICA][0]), x_of(S[VENUS][0]), xm,
              MOON[1], MOON[2], x_of(S[MERCURY][0])))
    print("  行星星等：" + "、".join(f"{k} {v[2]:+.2f}" for k, v in PLANETS.items()))

    terms = {}
    for h, z in ZH.items():
        terms[f"HIP {h}"] = dict(hips=[h], 原文=z, 拼音="", 英文翻譯="", 中文=z,
                                 顏色=COLOR.get(h, "white"), 來源備註="台灣通行星名")
    for ab, (keys, z, col, dx, dy) in CONS.items():
        terms[ab] = dict(hips=[], 原文=ab, 拼音="", 英文翻譯="", 中文=z, 顏色=col,
                         來源備註="IAU 星座；連線 Stellarium western")
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS,
               "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "planets": {k: dict(ra=v[0], dec=v[1], mag=v[2]) for k, v in PLANETS.items()},
               "moon": dict(ra=MOON[0], dec=MOON[1], phase=MOON[2]), "lst_at": LST_AT},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)

    print("\n── 預覽與分鏡 ──")

    def shot_groups(sh):
        g = []
        for k in sh.get("layers", []):
            g += LINE_GROUPS.get(k, [])
        return g

    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)

    LSD = {n: it for it, n in label_sets}
    panels = iter([(sh, i) for sh in shots for i in range(len(sh["frames"]))])
    draw0 = m.draw_mpl

    def draw_per_shot(ax, line_groups, **kw):
        sh, i = next(panels)
        last = i == len(sh["frames"]) - 1
        names = sh.get("labels_end", sh.get("labels", [])) if last else \
            sh.get("labels_start", sh.get("labels", []))
        kw["labels"] = [dict(it, pt=5) for n in names for it in LSD[n]]
        return draw0(ax, shot_groups(sh), **kw)
    m.draw_mpl = draw_per_shot
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=[],
              labels=[],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
