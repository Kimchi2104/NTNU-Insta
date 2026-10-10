# -*- coding: utf-8 -*-
"""B-02 行前觀星預報：11/14 五校聯合觀星（新竹尖石）｜大畫布 v4.6

一晚從黃昏到清晨（畫面往左＝往清晨走）：
  西南方眉月（人馬座南斗旁，約 21:00 月沒）→ 光害方向、天鵝座北美星雲 → 土星（20:56 正南 66°）
  → 21:00 的子午線一整條：仙女座大星系、土星、玉夫座星系 → 00:09 昴宿到頭頂＋北金牛座流星雨輻射點
  → 獵戶座（01:56 獵戶座大星雲過中天）→ 23:42／23:45 火星、木星一起東升（04:00 相距 1.3°；11/16 最近）
  → 軒轅十四、獅子座流星雨輻射點 → 05:00 東南東低空的金星（旁邊角宿一 1.5°）。

觀測地與時間
  新竹縣尖石鄉煤源一帶（油羅溪谷），計算點取北緯 24.72°、東經 121.19°、海拔 500 m（位置差幾公里，時刻差不到 1 分鐘）。
  2026/11/14（六）晚上到 11/15（日）清晨。PyEphem 自算（見逐字稿「星空對時」）：
  日落 17:09、天文暮光終 18:27、月沒 21:00（20:59:33；月相 23%）、天文曙光始 04:52、日出 06:11。

參數
  lst = 65 → 走廊（x=0）＝RA 65°（約 00:40 的子午線，昴宿 x +8、畢宿五 x −4）。
             往右（西）是土星（x +56）、仙女座大星系（+54）、玉夫座星系（+53）——21:00 的子午線一整條；
             天鵝（+115）、月亮（+135，18:30 的位置）、人馬座南斗（+139～+152）。
             往左（東）是獵戶（−19～−24）、蜂巢（−65）、火星＋木星（−83）、軒轅十四（−87）、金星與角宿一（−135）。
  D_s = 55、D_r = 59 → 天津四 +45.3、五車二 +46.0、北美星雲 +44.3、仙女座大星系 +41.3 離帶界還有 9° 以上，
             天鵝座整個框得進來（D_s 47 時 fov 40 的框頂會超界）；月亮 −25、南斗 −25～−30、北落師門 −29.6、
             玉夫座星系 −25.3 都在帶內。全片只用長圖（盤組照規格輸出、未使用）。
  D_fill = 0 → k=1.848、R_fill=166.3。x_tN = x_tS = 0。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS
from gen_projection import great_circle

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "B-02"
OUT = os.path.join(BASE, "05_素材/B-02_五校聯合觀星/_v4大畫布")
LST0 = 65.0
LAT, LON, ELEV = 24.72, 121.19, 500.0
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


def ephem_night():
    import ephem
    pl = {}
    for key, body, when in (("土星", ephem.Saturn(), "11/14 20:56"),
                            ("火星", ephem.Mars(), "11/15 04:00"),
                            ("木星", ephem.Jupiter(), "11/15 04:00"),
                            ("金星", ephem.Venus(), "11/15 05:00"),
                            ("天王星", ephem.Uranus(), "11/15 00:28")):
        body.compute(at(when), epoch=ephem.J2000)
        pl[key] = (math.degrees(body.a_ra), math.degrees(body.a_dec), round(body.mag, 2))
    o = site("11/14 18:30"); o.epoch = ephem.J2000           # 月亮視差近 1°：用觀測地看到的位置（站心），換到 J2000
    mo = ephem.Moon(); mo.compute(o)                          # ※ a_ra／a_dec 是地心位置，會差 0.6°
    moon = (round(math.degrees(float(mo.ra)), 2), round(math.degrees(float(mo.dec)), 2),
            round(mo.phase))
    lst = {}
    for s in ("11/14 18:30", "11/14 21:00", "11/15 00:00", "11/15 02:00", "11/15 04:00",
              "11/15 05:00"):
        o = site(s)
        lst[s] = math.degrees(o.sidereal_time())
    return pl, moon, lst


PLANETS, MOON, LST_AT = ephem_night()
SATURN, MARS, JUPITER, VENUS, URANUS = 9_000_001, 9_000_002, 9_000_003, 9_000_004, 9_000_005
PL_HIP = {"土星": SATURN, "火星": MARS, "木星": JUPITER, "金星": VENUS, "天王星": URANUS}

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
VEGA, ALTAIR, DENEB = 91262, 97649, 102098
NUNKI, ASCELLA, KAUS_AUS, PHI_SGR, TAU_SGR, LAM_SGR, MU_SGR = 92855, 93506, 90185, 92041, 93864, 90496, 89341
NANDOU = [PHI_SGR, LAM_SGR, MU_SGR, NUNKI, TAU_SGR, ASCELLA]          # 南斗六星（斗宿一～六）
FOMALHAUT, DIPHDA, MARKAB, ALPHERATZ = 113368, 3419, 113963, 677
ALDEBARAN, ALCYONE, CAPELLA = 21421, 17702, 24608
BETELGEUSE, RIGEL, SIRIUS, PROCYON, POLLUX = 27989, 24436, 32349, 37279, 37826
REGULUS, ALGIEBA, DENEBOLA, SPICA, ZET_VIR = 49669, 50583, 57632, 65474, 66249

MAINS = [VEGA, ALTAIR, DENEB, NUNKI, ASCELLA, FOMALHAUT, DIPHDA, MARKAB, ALPHERATZ,
         ALDEBARAN, ALCYONE, CAPELLA, BETELGEUSE, RIGEL, SIRIUS, REGULUS, SPICA,
         SATURN, MARS, JUPITER, VENUS]

# 深空天體（J2000；位置、大小取 SIMBAD／Messier 常用值）
M31 = (10.685, 41.269)            # 仙女座大星系：3.2°×1.0°，位置角 35°
M33 = (23.462, 30.660)            # 三角座星系：70′×40′，位置角 23°
NGC253 = (11.888, -25.288)        # 玉夫座星系：27′×7′，位置角 52°
M45 = (56.75, 24.12)              # 昴宿星團
M42 = (83.82, -5.39)              # 獵戶座大星雲
M44 = (130.10, 19.67)             # 蜂巢星團
NGC7000 = (314.75, 44.33)         # 北美星雲
NGC2237 = (97.98, 5.05)           # 玫瑰星雲
LEO_R = (150.0, 23.0)             # 獅子座流星雨輻射點：IMO 每日漂移的 11/15 位置（極大 11/17–18 時約 α 152°、δ +22°）
NTA_R = (58.0, 22.0)              # 北金牛座流星雨輻射點（約；IMO：極大 11/12 附近 α 58°、δ +22°，兩天內只差 1–2°）


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
TRI = [[VEGA, DENEB, ALTAIR, VEGA]]
NANDOU_L = [[PHI_SGR, LAM_SGR, MU_SGR], [PHI_SGR, NUNKI, TAU_SGR, ASCELLA, PHI_SGR]]
LG_SUM = [(W["Cyg"], "blue", 1.0), (W["Lyr"], "blue", 1.0), (W["Aql"], "blue", 1.0), (TRI, "blue", 0.45)]
LG_SGR = [(W["Sgr"], "amber", 1.0)]
LG_PEG = [(W["Peg"], "purple", 1.0), (W["And"], "purple", 1.0), (W["Tri"], "purple", 1.0)]
LG_CET = [(W["Psc"], "blue", 0.8), (W["Cet"], "blue", 1.0), (W["Scl"], "blue", 0.8), (W["PsA"], "blue", 0.8)]
LG_TAU = [(W["Tau"], "amber", 1.0), (W["Per"], "red", 0.7), (W["Aur"], "amber", 0.7)]
LG_ORI = [(W["Ori"], "amber", 1.0), (W["CMa"], "blue", 0.8), (W["Gem"], "green", 0.7)]
LG_LEO = [(W["Leo"], "red", 1.0), (W["Cnc"], "red", 0.7)]
LG_VIR = [(W["Vir"], "green", 1.0)]
LG_ALL = LG_SUM + LG_SGR + LG_PEG + LG_CET + LG_TAU + LG_ORI + LG_LEO + LG_VIR
LINE_SETS = [(LG_SUM, "連線-夏季大三角"), (LG_SGR, "連線-人馬"), (LG_PEG, "連線-飛馬仙女"),
             (LG_CET, "連線-雙魚鯨魚玉夫"), (LG_TAU, "連線-金牛英仙御夫"), (LG_ORI, "連線-獵戶大犬雙子"),
             (LG_LEO, "連線-獅子巨蟹"), (LG_VIR, "連線-室女")]
LINES_KEY = {"L4": "星座連線", "夏": "連線-夏季大三角", "人馬": "連線-人馬", "飛馬": "連線-飛馬仙女",
             "鯨魚": "連線-雙魚鯨魚玉夫", "金牛": "連線-金牛英仙御夫", "獵戶": "連線-獵戶大犬雙子",
             "獅子": "連線-獅子巨蟹", "室女": "連線-室女",
             "深空": "深空天體", "行星": "行星標記", "流星": "流星雨輻射點", "月": "月亮（11-14 18-30）"}
LINE_GROUPS = {"L4": LG_ALL, "夏": LG_SUM, "人馬": LG_SGR, "飛馬": LG_PEG, "鯨魚": LG_CET,
               "金牛": LG_TAU, "獵戶": LG_ORI, "獅子": LG_LEO, "室女": LG_VIR}


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
    "Cyg": (["Cyg"], "天鵝座", "blue", 7.0, -5.0),
    "Lyr": (["Lyr"], "天琴座", "blue", 0.0, -5.0),
    "Aql": (["Aql"], "天鷹座", "blue", 6.0, -6.0),
    "Sgr": (["Sgr"], "人馬座", "amber", 0.0, 9.0),
    "Peg": (["Peg"], "飛馬座", "purple", 4.0, -9.0),
    "And": (["And"], "仙女座", "purple", -3.0, 6.0),
    "Tri": (["Tri"], "三角座", "purple", -2.0, 3.0),
    "Psc": (["Psc"], "雙魚座", "blue", 16.0, -8.0),
    "Cet": (["Cet"], "鯨魚座", "blue", -4.0, -6.0),
    "Scl": (["Scl"], "玉夫座", "blue", 0.0, -4.0),
    "PsA": (["PsA"], "南魚座", "blue", 0.0, -4.0),
    "Tau": (["Tau"], "金牛座", "amber", 2.0, -8.0),
    "Per": (["Per"], "英仙座", "red", -4.0, 2.0),
    "Aur": (["Aur"], "御夫座", "amber", -3.0, 2.0),
    "Ori": (["Ori"], "獵戶座", "amber", 0.0, -16.0),
    "CMa": (["CMa"], "大犬座", "blue", 0.0, -8.0),
    "Gem": (["Gem"], "雙子座", "green", 0.0, 8.0),
    "Cnc": (["Cnc"], "巨蟹座", "red", 0.0, -6.0),
    "Leo": (["Leo"], "獅子座", "red", -2.0, 9.0),
    "Vir": (["Vir"], "室女座", "green", 0.0, 8.0),
}

ZH = {VEGA: "織女星", ALTAIR: "牛郎星", DENEB: "天津四", NUNKI: "斗宿四",
      FOMALHAUT: "北落師門", DIPHDA: "土司空", MARKAB: "室宿一", ALPHERATZ: "壁宿二",
      ALDEBARAN: "畢宿五", CAPELLA: "五車二", BETELGEUSE: "參宿四", RIGEL: "參宿七",
      SIRIUS: "天狼星", PROCYON: "南河三", POLLUX: "北河三", REGULUS: "軒轅十四",
      SPICA: "角宿一"}
COLOR = {VEGA: "blue", ALTAIR: "blue", DENEB: "blue", NUNKI: "amber", FOMALHAUT: "blue",
         DIPHDA: "blue", MARKAB: "purple", ALPHERATZ: "purple", ALDEBARAN: "amber",
         CAPELLA: "amber", BETELGEUSE: "amber", RIGEL: "amber", SIRIUS: "blue",
         PROCYON: "white", POLLUX: "green", REGULUS: "red", SPICA: "green"}
OFF = {VEGA: (-4.4, 1.0), ALTAIR: (4.6, -1.0), DENEB: (4.4, 1.0), NUNKI: (0.0, 2.6),
       FOMALHAUT: (4.6, 0.0), DIPHDA: (4.4, -0.4), MARKAB: (4.4, -1.0), ALPHERATZ: (-4.4, 1.2),
       ALDEBARAN: (4.6, -0.6), CAPELLA: (-4.4, 0.8), BETELGEUSE: (-4.6, 0.6), RIGEL: (4.4, -0.6),
       SIRIUS: (0.0, -2.4), PROCYON: (-4.4, 0.0), POLLUX: (-4.4, 0.6), REGULUS: (4.6, -0.6),
       SPICA: (4.4, -1.2)}

PL_COLOR = {"土星": "amber", "火星": "red", "木星": "white", "金星": "amber", "天王星": "green"}
PL_OFF = {"土星": (3.6, -0.4), "火星": (-3.4, 0.6), "木星": (3.4, 0.2), "金星": (-3.6, 0.4),
          "天王星": (-3.2, -0.6)}
OBJ = {    # 天體：(ra, dec, 文字, 顏色, dx, dy)
    "M31": (*M31, "仙女座大星系", "white", 0.0, -3.0),
    "M33": (*M33, "三角座星系", "white", 0.0, -2.4),
    "NGC253": (*NGC253, "玉夫座星系", "white", 0.0, -2.4),
    "M45": (*M45, "昴宿星團", "white", 0.0, 2.8),
    "M42": (*M42, "獵戶座大星雲", "white", 6.6, -1.0),
    "M44": (*M44, "蜂巢星團", "white", 0.0, -2.4),
    "NGC7000": (*NGC7000, "北美星雲", "white", 0.0, -2.6),
    "NGC2237": (*NGC2237, "玫瑰星雲", "white", 0.0, -2.4),
    "NTA": (*NTA_R, "北金牛座流星雨輻射點", "white", 0.0, -3.4),
    "LEO": (*LEO_R, "獅子座流星雨輻射點", "white", 0.0, -3.4),
}
CN = {     # 中國星官：(錨點, 名, 顏色, dx, dy)
    "南斗": (NANDOU, "南斗", "amber", 0.0, -5.2),
    "昴宿": ([ALCYONE], "昴宿", "amber", 0.0, -2.8),
    "軒轅": ([REGULUS, ALGIEBA, 50335, 49583, 47908, 48455], "軒轅", "red", 6.0, 1.0),
    "角宿": ([SPICA, ZET_VIR], "角宿", "green", 4.0, -2.6),
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


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*M31, 1.6, 0.5, 35.0), (*M33, 0.55, 0.35, 23.0),
                                      (*NGC253, 0.45, 0.12, 52.0), (*M42, 0.5, 0.45, 0.0),
                                      (*NGC7000, 1.0, 0.8, 0.0), (*NGC2237, 0.7, 0.7, 0.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.14), (0.42, 0.22), (0.2, 0.35)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        for (ra0, dec0, rad, vmax) in [(*M44, 0.75, 9.5), (*M45, 1.1, 8.5)]:
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
            r = 0.9 if key == "天王星" else max(1.3, m.sz_star(v) * 5.0)
            for p in pos(ra, dec):
                s.circle(p[0], p[1], r, stroke=COLORS[PL_COLOR[key]], w=0.12, opacity=0.95)

    def radiant(s, pos, runs):
        for ra0, dec0 in (LEO_R, NTA_R):
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
            ("月亮（11-14 18-30）", moon)]


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

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

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
            sz = size * (0.9 if key == "天王星" else 1.15)
            dx, dy = PL_OFF[key]
            w, _ = MC.label_box(key, sz, m.fu)
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

    def cn_items(size, only=None):
        out = []
        for k, (hips, txt, col, dx, dy) in CN.items():
            if only is not None and k not in only:
                continue
            out.append(dict(anchor(hips), text=txt, color=col, size=size, dx=dx, dy=dy, key="中-" + k))
        return out

    label_sets = [
        (cons_items(1.6), "星座名"),
        (star_items(1.1), "亮星名"),
        (obj_items(1.0), "天體"),
        (cn_items(1.15), "中國星官"),
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
    OPEN0 = (150.0, -4.0, 48.0, 0.0)                         # 開場：西方（人馬＋天鷹）
    OPEN1 = (128.0, -4.0, 48.0, 0.0)
    MOON_F = (round(xm + 5.0, 1), -21.0, 34.0, 0.0)          # 眉月＋南斗（月亮在框中心左下）
    CYG_F = (114.0, 19.0, 40.0, 0.0)                         # 天鵝座（北美星雲）＋天鷹
    SAT_F = (56.0, 2.0, 30.0, 0.0)                           # 土星
    MER_F = (55.0, 7.0, 50.0, 0.0)                           # 21:00 的子午線：仙女座大星系—土星—玉夫座星系
    PLE_F = (6.0, 21.0, 30.0, 0.0)                           # 昴宿＋輻射點
    ORI_F = (-22.0, -4.0, 40.0, 0.0)                         # 獵戶＋玫瑰
    MJ_F = (-80.0, 14.0, 34.0, 0.0)                          # 火星＋木星＋軒轅十四
    MJ_Z = (-83.0, 12.0, 14.0, 0.0)                          # 推近：火木 1.3°、軒轅十四 4.4°
    LEO_F = (-88.0, 17.0, 36.0, 0.0)                         # 獅子座＋輻射點
    VEN_F = (-134.0, -8.0, 30.0, 0.0)                        # 金星＋角宿一
    WIDE_F = (-70.0, 2.0, 52.0, 0.0)                         # 東半天全景
    END_F = (-20.0, 4.0, 52.0, 0.0)

    shots = [
        dict(code="01", kind="S", sec=12, north=True,
             frames=[OPEN0, OPEN1], layers=["深空", "行星", "月"], labels=[],
             vo="十一月十四日，五校聯合觀星，地點在新竹尖石。天黑先有一彎眉月，九點前就下山；"
                "之後一路暗到清晨。今晚抬頭，第一眼找誰？",
             card="11/14 五校聯合觀星｜今晚抬頭，第一眼找誰？",
             note="開場字卡；人馬座、天鷹座往東緩慢平移（畫面往左＝往清晨走），先不開連線"),
        dict(code="02", kind="Z", sec=13, north=True,
             frames=[OPEN1, MOON_F], layers=["人馬", "月", "深空", "行星"], labels=["亮星名", "中國星官"],
             labels_end=["星座名", "亮星名", "中國星官"],
             overlay="C-B02-01_方位_1830西南", overlay_layers=["合成層"],
             vo="五點零九分日落，六點半天全黑。西南方那彎眉月，只亮兩成多，就在人馬座的南斗旁邊；"
                "等它九點前沉到山後，才是拍深空的時間。",
             note="推近眉月（18:30 的位置）與人馬座南斗；結束後疊方位卡 18:30（西南方）"),
        dict(code="03", kind="Z", sec=15, north=True,
             frames=[MOON_F, CYG_F], labels_start=["星座名", "亮星名", "中國星官"],
             layers=["夏", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             overlay="C-B02-02_光害方位", overlay_layers=["城鎮層", "暗區層"],
             vo="先認方向：西邊十公里是竹東，西北是新竹、竹北，北邊是關西、中壢、桃園，"
                "這半圈都有光害；東邊到南邊，往山裡最暗。天鵝座的北美星雲在西北，十點前拍完。",
             note="往北（上）滑到天鵝座與北美星雲；結束後疊光害方位卡（兩層：城鎮 → 最暗的方向）"),
        dict(code="04", kind="Z", sec=12, north=True,
             frames=[CYG_F, SAT_F], labels_start=["星座名", "亮星名", "天體"],
             layers=["鯨魚", "深空", "行星"], labels=["亮星名"],
             vo="天一黑，第一個看土星：九點前後升到正南，仰角六十六度，今晚最高。"
                "望遠鏡看得到環，今年只斜六度，是扁扁的一圈。",
             note="往東（左）滑到土星（行星標記：琥珀圈），在雙魚座與鯨魚座交界"),
        dict(code="05", kind="Z", sec=15, north=True,
             frames=[SAT_F, MER_F], labels_start=["亮星名"],
             layers=["飛馬", "鯨魚", "深空", "行星"], labels=["亮星名", "天體"],
             overlay="C-B02-03_方位_2100南方", overlay_layers=["合成層"],
             vo="九點這條子午線上，排成一整條：頭頂偏北是兩百五十萬光年外的仙女座大星系，"
                "正南是土星，再往下二十六度，還有一個側著的大星系——玉夫座星系。",
             note="拉遠成 21:00 的子午線（仙女座大星系 21:05、土星 20:56、玉夫座星系 21:10 過中天）；"
                  "結束後疊方位卡 21:00（南方）"),
        dict(code="06", kind="Z", sec=14, north=True,
             frames=[MER_F, PLE_F], labels_start=["亮星名", "天體"],
             layers=["金牛", "流星", "深空", "行星"], labels=["亮星名", "天體"],
             vo="午夜十二點零九分，昴宿星團升到正頭頂，仰角將近九十度。旁邊是北金牛座流星雨的輻射點："
                "十二日剛過極大，每小時大約五顆，很慢，偶爾有火流星。",
             note="往東滑到昴宿（00:09 過中天）；輻射點（流星雨輻射點層）在昴宿東南約 2.4°"),
        dict(code="07", kind="Z", sec=12, north=True,
             frames=[PLE_F, ORI_F], labels_start=["亮星名", "天體"],
             layers=["獵戶", "金牛", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             overlay="C-B02-04_攝影時間窗",
             vo="十點半以後，獵戶座爬過東邊的山；兩點前後升到正南，獵戶座大星雲仰角六十度。"
                "馬頭、火焰、玫瑰星雲，都在這段時間最高。",
             note="往下（南）滑到獵戶座、玫瑰星雲；結束後疊 9:16 攝影時間窗（可存圖）"),
        dict(code="08", kind="Z", sec=13, north=True,
             frames=[ORI_F, MJ_F], labels_start=["星座名", "亮星名", "天體"],
             layers=["獅子", "深空", "行星"], labels=["星座名", "亮星名"],
             overlay="C-B02-05_方位_0400東方", overlay_layers=["合成層"],
             vo="午夜前，火星和木星一起從東方升起，只差三分鐘。清晨四點升到東方仰角五十七度："
                "火星偏紅、木星最亮，相距一點三度——十六日最接近。",
             note="往東滑到獅子座：火星（紅圈）、木星（白圈）、軒轅十四；結束後疊方位卡 04:00（東方）"),
        dict(code="09", kind="Z", sec=12, north=True,
             frames=[MJ_F, MJ_Z], labels_start=["星座名", "亮星名"],
             layers=["獅子", "深空", "行星"], labels=["亮星名"],
             overlay="C-B02-06_火木相合", overlay_layers=["視野層", "軌跡層"],
             vo="離木星四度多，是獅子座最亮的軒轅十四。一般雙筒望遠鏡，一個視野就裝得下這三顆，"
                "連木星的衛星都看得到。",
             note="推近火星、木星、軒轅十四；結束後疊概念圖 火木相合（兩層：雙筒視野 → 11/13–11/18 清晨 4 點火星的位置）"),
        dict(code="10", kind="Z", sec=12, north=True,
             frames=[MJ_Z, LEO_F], labels_start=["亮星名"],
             layers=["獅子", "流星", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             labels_end=["星座名", "天體"],
             vo="獅子的頭，也是獅子座流星雨的輻射點，兩點以後越升越高。極大在十七日深夜到十八日清晨，"
                "今晚還早，流星不多，但每一顆都很快。",
             note="拉遠到獅子座：輻射點（流星雨輻射點層）在獅子頭的鐮刀"),
        dict(code="11", kind="Z", sec=14, north=True,
             frames=[LEO_F, VEN_F], labels_start=["星座名", "天體"],
             layers=["室女", "深空", "行星"], labels=["星座名", "亮星名"],
             overlay="C-B02-07_方位_0500東南東", overlay_layers=["合成層"],
             vo="四點五十二分，天開始亮。五點前後，東南東低空冒出全天最亮的金星，負四點八等；"
                "望遠鏡裡是一彎細細的眉月，旁邊一度半是角宿一。",
             note="往東滑到室女座：金星（11/15 05:00 的位置）與角宿一；"
                  "結束後疊方位卡 05:00（東南東）"),
        dict(code="12", kind="Z", sec=12, north=True,
             frames=[VEN_F, WIDE_F], labels_start=["亮星名"],
             layers=["L4", "深空", "行星", "流星"], labels=[],
             vo="山谷夜裡露水很重，鏡頭要掛加熱帶、帶足行動電源；東北季風來的時候，"
                "雲會從山谷灌上來，出發前先看衛星雲圖。",
             note="拉遠成東半天全景（全部連線）；這格沒有標籤，留給字幕"),
        dict(code="13", kind="Z", sec=9, north=True,
             frames=[WIDE_F, END_F],
             layers=["L4", "深空", "行星", "流星"], labels=[],
             overlay="C-B02-08_今晚時間表",
             vo="眉月、土星、頭頂的昴宿，天亮前的火星、木星和金星——十一月十四日，尖石見。",
             card="11/14 尖石見｜追蹤師大天文社",
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

    print("  x：月亮 %+.1f（dec %+.1f，%d%%）、土星 %+.1f、仙女座大星系 %+.1f、玉夫座星系 %+.1f、昴宿六 %+.1f、"
          "參宿四 %+.1f、火星 %+.1f、木星 %+.1f、軒轅十四 %+.1f、金星 %+.1f、角宿一 %+.1f" % (
              xm, MOON[1], MOON[2], x_of(S[SATURN][0]), x_of(M31[0]), x_of(NGC253[0]),
              x_of(S[ALCYONE][0]), x_of(S[BETELGEUSE][0]), x_of(S[MARS][0]), x_of(S[JUPITER][0]),
              x_of(S[REGULUS][0]), x_of(S[VENUS][0]), x_of(S[SPICA][0])))

    terms = {}
    for h, z in ZH.items():
        terms[f"HIP {h}"] = dict(hips=[h], 原文=z, 拼音="", 英文翻譯="", 中文=z,
                                 顏色=COLOR.get(h, "white"), 來源備註="台灣通行星名")
    for k, (hips, z, col, dx, dy) in CN.items():
        terms["中-" + k] = dict(hips=hips, 原文=z, 拼音="", 英文翻譯="", 中文=z, 顏色=col,
                               來源備註="中國星官（Stellarium chinese）")
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
