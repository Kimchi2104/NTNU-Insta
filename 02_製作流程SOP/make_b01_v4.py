# -*- coding: utf-8 -*-
"""B-01 行前觀星預報：10/10 秋觀｜大畫布 v4.6

一晚從黃昏到清晨：夏季大三角 → 飛馬（秋季四邊形）→ 土星（10/4 衝）→ 仙女、仙后、北極星
→（北盤）王室神話、面向北方、仙王（造父變星）、英仙（大陵五）、御夫（δ 流星雨輻射點）
→（長圖）金牛、獵戶 → 火星闖進蜂巢星團、木星。

輸出：L1銀河 L2星點（含當晚土星、火星、木星） L3經緯線 L4星座連線（全開）
      L5…連線-夏季大三角／飛馬仙女／雙魚鯨魚／仙后仙王／英仙／御夫金牛／獵戶／巨蟹獅子
      主角星白點／白圈、深空天體、行星標記、流星雨輻射點
      標籤：星座名／亮星名／天體／中國星官（長圖）＋ 星座名-盤／亮星名-盤／天體-盤／神話（盤）
      ＋ 南北盤圖層組 / 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單 / 標籤資料
執行：python3 make_b01_v4.py

觀測地與時間
  北緯 24.0°、東經 121.0°（台灣中部山區；全台時刻差不到 ±5 分鐘），2026/10/10（六）晚上到 10/11（日）清晨。
  PyEphem 自算（見逐字稿「星空對時」）：日落 17:34、天文昏影終 18:49、天文晨光始 04:36、日出 05:51；
  新月 10/10 23:50，整夜無月。

參數
  lst = 15 → 走廊（x=0）＝RA 15：土星（x +4.3）正下方、仙女座大星系（x +4.3）、仙后座 W（x −10～+11）、
             北極星一路在走廊上——07 鏡一個 T 從土星抬頭到北極星。
             往右（西）是飛馬（x +12～+29）、天鵝（+65）、天鷹（+77）、天琴（+96）；
             往左（東）是英仙（−18～−36）、金牛（−42～−66）、御夫（−64）、獵戶（−64～−74）、
             巨蟹＋火星（−115）、木星（−128）。由右往左＝黃昏到清晨。
  D_s = 51、D_r = 55 → 天船三 +49.9、五車二 +46.0、天津四 +45.3、仙女座大星系 +41.3 都在帶內；
             仙后座（王良四 +56.5 起）整個進盤本體；英仙座北端（+53.5～+55.9）落在縫合帶。
  D_fill = −19 → k=1.637、R_fill=178.4（|x_t|+R_fill ≤ 180 的上限）；北盤收到 dec −19：
             英仙、御夫在盤上變形比長圖小（dec 45 處長圖橫向 ×1.41，盤上 ×1.11），所以 08–13 鏡在北盤上導覽。
  x_tN = x_tS = 0（Canva 可水平置中）
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS
from gen_projection import great_circle

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "B-01"
OUT = os.path.join(BASE, "05_素材/B-01_秋觀星空導覽/_v4大畫布")
LST0 = 15.0
LAT, LON = 24.0, 121.0
PHI = LAT


# ══════════════════════════════════════════════════════════════════
# 〇、當晚星曆（PyEphem）：行星位置、各時刻的地方恆星時
# ══════════════════════════════════════════════════════════════════
def ephem_night():
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(LAT), str(LON); o.elevation = 0

    def at(s):                                  # 台灣時間 "MM/DD HH:MM"
        md, hm = s.split(); mo, d = md.split("/")
        return ephem.Date(ephem.Date(f"2026/{mo}/{d} {hm}") - 8 * ephem.hour)

    pl = {}
    for key, body, when in (("土星", ephem.Saturn(), "10/10 22:00"),
                            ("火星", ephem.Mars(), "10/11 04:00"),
                            ("木星", ephem.Jupiter(), "10/11 04:00")):
        body.compute(at(when), epoch=ephem.J2000)
        pl[key] = (math.degrees(body.a_ra), math.degrees(body.a_dec), round(body.mag, 2))
    lst = {}
    for s in ("10/10 19:30", "10/10 21:00", "10/10 22:00", "10/11 00:00", "10/11 01:00",
              "10/11 04:00", "10/11 04:30"):
        o.date = at(s)
        lst[s] = math.degrees(o.sidereal_time())
    return pl, lst


PLANETS, LST_AT = ephem_night()
SATURN, MARS, JUPITER = 9_000_001, 9_000_002, 9_000_003
PL_HIP = {"土星": SATURN, "火星": MARS, "木星": JUPITER}

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALTAIR, TARAZED, ALSHAIN, VEGA = 97649, 97278, 98036, 91262
DENEB, SADR, ALBIREO = 102098, 100453, 95947
MARKAB, SCHEAT, ALGENIB, ALPHERATZ = 113963, 113881, 1067, 677
MIRACH, ALMACH = 5447, 9640
DIPHDA, MENKAR, MIRA = 3419, 14135, 10826
SCHEDAR, CAPH, GAM_CAS, RUCHBAH, SEGIN = 3179, 746, 4427, 6686, 8886
POLARIS = 11767
ALDERAMIN, ALFIRK, ERRAI, DEL_CEP, ZET_CEP, MU_CEP = 105199, 106032, 116727, 110991, 109492, 107259
MIRFAK, ALGOL = 15863, 14576
CAPELLA, MENKALINAN, ELNATH = 24608, 28360, 25428
ALDEBARAN, ALCYONE = 21421, 17702
BETELGEUSE, RIGEL, BELLATRIX, MINTAKA, ALNILAM, ALNITAK = 27989, 24436, 25336, 25930, 26311, 26727
SIRIUS, REGULUS = 32349, 49669

MAINS = [ALTAIR, VEGA, DENEB, ALBIREO, MARKAB, SCHEAT, ALGENIB, ALPHERATZ,
         SCHEDAR, CAPH, GAM_CAS, RUCHBAH, SEGIN, POLARIS, ALDERAMIN, DEL_CEP,
         MIRFAK, ALGOL, CAPELLA, ALDEBARAN, BETELGEUSE, RIGEL, REGULUS,
         SATURN, MARS, JUPITER]

# 深空天體（J2000；位置、大小取自 SIMBAD／Messier 常用值）
M31 = (10.685, 41.269)            # 仙女座大星系：3.2°×1.0°，位置角 35°
M44 = (130.10, 19.67)             # 蜂巢星團（鬼宿 積屍氣）
HCHI = [(34.75, 57.13), (35.58, 57.15)]   # 英仙座雙星團 h、χ
M42 = (83.82, -5.39)
M45 = (56.75, 24.12)
DAU = (84.0, 44.0)                # 御夫座 δ 流星雨輻射點（IMO 2026：α 5h36m、δ +44°；極大 10/11、ZHR≈2）


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium western index.json）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


W = sc_lines("western")
TRI = [[VEGA, DENEB, ALTAIR, VEGA]]                     # 夏季大三角（星群，細線）
LG_SUM = [(W["Aql"], "blue", 1.0), (W["Cyg"], "blue", 1.0), (W["Lyr"], "blue", 1.0),
          (TRI, "blue", 0.45)]
LG_PEG = [(W["Peg"], "purple", 1.0), (W["And"], "purple", 1.0)]
LG_CET = [(W["Psc"], "blue", 0.8), (W["Cet"], "blue", 1.0)]
LG_CAS = [(W["Cas"], "green", 1.0), (W["Cep"], "green", 1.0)]
LG_PER = [(W["Per"], "red", 1.0)]
LG_AUR = [(W["Aur"], "amber", 1.0), (W["Tau"], "amber", 1.0)]
LG_ORI = [(W["Ori"], "amber", 1.0)]
LG_CNC = [(W["Cnc"], "red", 1.0), (W["Leo"], "red", 0.8)]
LG_ALL = LG_SUM + LG_PEG + LG_CET + LG_CAS + LG_PER + LG_AUR + LG_ORI + LG_CNC
LINE_SETS = [(LG_SUM, "連線-夏季大三角"), (LG_PEG, "連線-飛馬仙女"), (LG_CET, "連線-雙魚鯨魚"),
             (LG_CAS, "連線-仙后仙王"), (LG_PER, "連線-英仙"), (LG_AUR, "連線-御夫金牛"),
             (LG_ORI, "連線-獵戶"), (LG_CNC, "連線-巨蟹獅子")]
LINES_KEY = {"L4": "星座連線", "夏": "連線-夏季大三角", "飛馬": "連線-飛馬仙女",
             "鯨魚": "連線-雙魚鯨魚", "仙后": "連線-仙后仙王", "英仙": "連線-英仙",
             "御夫": "連線-御夫金牛", "獵戶": "連線-獵戶", "巨蟹": "連線-巨蟹獅子",
             "深空": "深空天體", "行星": "行星標記", "流星": "流星雨輻射點"}
LINE_GROUPS = {"L4": LG_ALL, "夏": LG_SUM, "飛馬": LG_PEG, "鯨魚": LG_CET, "仙后": LG_CAS,
               "英仙": LG_PER, "御夫": LG_AUR, "獵戶": LG_ORI, "巨蟹": LG_CNC}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（＝標籤對照表）：台灣通行譯名
# ══════════════════════════════════════════════════════════════════
CONS = {   # 星座名：(連線 key 群, 中文, 顏色, dx, dy)
    "Aql": (["Aql"], "天鷹座", "blue", 6.0, -6.0),
    "Cyg": (["Cyg"], "天鵝座", "blue", 0.0, 7.0),
    "Lyr": (["Lyr"], "天琴座", "blue", 0.0, -5.0),
    "Peg": (["Peg"], "飛馬座", "purple", 4.0, -9.0),
    "And": (["And"], "仙女座", "purple", -3.0, 4.5),
    "Psc": (["Psc"], "雙魚座", "blue", 16.0, -8.0),
    "Cet": (["Cet"], "鯨魚座", "blue", 0.0, -6.0),
    "Cas": (["Cas"], "仙后座", "green", 0.0, 6.0),
    "Cep": (["Cep"], "仙王座", "green", 0.0, 7.0),
    "Per": (["Per"], "英仙座", "red", -4.0, 2.0),
    "Aur": (["Aur"], "御夫座", "amber", -3.0, 2.0),
    "Tau": (["Tau"], "金牛座", "amber", 2.0, -8.0),
    "Ori": (["Ori"], "獵戶座", "amber", 0.0, -16.0),
    "Cnc": (["Cnc"], "巨蟹座", "red", 0.0, -8.0),
    "Leo": (["Leo"], "獅子座", "red", 0.0, 9.0),
}
ROLE = {"Cep": "國王", "Cas": "王后", "And": "公主", "Per": "英雄", "Cet": "海怪", "Peg": "飛馬"}

ZH = {ALTAIR: "牛郎星", VEGA: "織女星", DENEB: "天津四", ALBIREO: "輦道增七",
      MARKAB: "室宿一", SCHEAT: "室宿二", ALGENIB: "壁宿一", ALPHERATZ: "壁宿二",
      SCHEDAR: "王良四", POLARIS: "北極星", DEL_CEP: "造父一", ALDERAMIN: "天鉤五",
      MIRFAK: "天船三", ALGOL: "大陵五", CAPELLA: "五車二", ALDEBARAN: "畢宿五",
      BETELGEUSE: "參宿四", RIGEL: "參宿七", SIRIUS: "天狼星", REGULUS: "軒轅十四",
      DIPHDA: "土司空", MIRA: "蒭藁增二"}
COLOR = {ALTAIR: "blue", VEGA: "blue", DENEB: "blue", ALBIREO: "blue",
         MARKAB: "purple", SCHEAT: "purple", ALGENIB: "purple", ALPHERATZ: "purple",
         SCHEDAR: "green", DEL_CEP: "green", ALDERAMIN: "green",
         MIRFAK: "red", ALGOL: "red", CAPELLA: "amber", ALDEBARAN: "amber",
         BETELGEUSE: "amber", RIGEL: "amber", REGULUS: "red", DIPHDA: "blue", MIRA: "blue"}
# 星名偏移（畫布單位；東在左）：(dx, dy)；左右放時 dx 會自動加上半個字寬
OFF = {ALTAIR: (4.6, -1.0), VEGA: (-4.4, 1.0), DENEB: (4.4, 1.0), ALBIREO: (-5.0, 0.0),
       MARKAB: (4.4, -1.0), SCHEAT: (4.4, 1.0), ALGENIB: (-4.4, -1.0), ALPHERATZ: (-4.4, 1.2),
       SCHEDAR: (4.0, -1.2), POLARIS: (0.0, 2.4), DEL_CEP: (4.4, -0.6), ALDERAMIN: (4.4, 0.6),
       MIRFAK: (-4.4, 0.8), ALGOL: (4.0, -0.6), CAPELLA: (-4.4, 0.8), ALDEBARAN: (4.6, -0.6),
       BETELGEUSE: (-4.6, 0.6), RIGEL: (4.4, -0.6), SIRIUS: (0.0, -2.4), REGULUS: (4.6, -0.4),
       DIPHDA: (4.4, -0.4), MIRA: (4.6, 0.0)}

PL_COLOR = {"土星": "amber", "火星": "red", "木星": "white"}
PL_OFF = {"土星": (3.6, -0.4), "火星": (-3.6, 0.9), "木星": (3.6, -0.4)}
OBJ = {    # 天體：(ra, dec, 文字, 顏色, dx, dy)
    "M31": (*M31, "仙女座大星系", "white", 0.0, -3.0),
    "M44": (*M44, "蜂巢星團", "white", 1.2, -2.6),
    "M45": (*M45, "昴宿星團", "white", 0.0, 2.6),
    "HCHI": (35.2, 57.1, "雙星團", "white", 0.0, -2.6),
    "M42": (*M42, "獵戶座大星雲", "white", 6.6, -1.0),
    "DAU": (*DAU, "δ 流星雨輻射點", "white", 0.0, -3.2),
}
CN = {     # 中國星官：(錨點, 名, 顏色, dx, dy)
    "河鼓": ([ALTAIR, TARAZED, ALSHAIN], "河鼓（牛郎）", "blue", 7.0, 3.4),
    "織女": ([VEGA], "織女", "blue", 0.0, -3.0),
    "天津": ([DENEB, SADR], "天津", "blue", -6.5, -1.0),
    "室宿": ([MARKAB, SCHEAT], "室宿", "purple", 4.8, 0.0),
    "壁宿": ([ALGENIB, ALPHERATZ], "壁宿", "purple", -4.6, 0.0),
    "王良": ([SCHEDAR, CAPH], "王良", "green", 5.0, 0.0),
    "造父": ([DEL_CEP, ZET_CEP, MU_CEP], "造父", "green", 4.2, -2.4),
    "大陵": ([ALGOL], "大陵", "red", 3.6, -2.6),
    "五車": ([CAPELLA, MENKALINAN, ELNATH, 23015, 28380], "五車", "amber", 0.0, -1.0),
    "畢宿": ([ALDEBARAN, 20205, 20455, 20889, 20894], "畢宿", "amber", 0.0, -3.2),
    "昴宿": ([ALCYONE], "昴宿", "amber", 0.0, -2.8),
    "參宿": ([BETELGEUSE, RIGEL, BELLATRIX, MINTAKA, ALNILAM, ALNITAK, 27366], "參宿",
             "amber", 7.0, 0.0),
    "鬼宿": ([], "鬼宿 積屍氣", "white", 1.2, -4.8),
}
DY_ROLE = -3.4
# 盤上（原生文字不跟著盤轉）：星座名的偏移是「畫面方向」；全家福（0°）與 22:00 面向北方（−155°）共用
CONS_DISC = {"Per": (0.0, 7.0), "Aur": (7.0, -8.0), "Cas": (0.0, 7.0), "Cep": (0.0, 0.0),
             "And": (0.0, 5.0), "Peg": (0.0, 0.0), "Cet": (0.0, 0.0), "Psc": (0.0, 0.0)}


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節＋希臘字母）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏ]+|[α-ω]|\d+|[㐀-鿿]", t):
        if re.match(r"[㐀-鿿]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2                               # δ＝delta 兩個音節
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouy]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、自訂圖層：深空天體、行星標記、流星雨輻射點（大畫布＋南北盤同步出）
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
        u, v = a * math.cos(t), b * math.sin(t)         # u 沿長軸
        th = math.radians(pa)                           # 位置角：北起向東
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
    """回傳 [(name, draw(svg, pos, runs))]；pos(ra,dec)→[點]，runs(pts)→[折線]"""
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*M31, 1.6, 0.5, 35.0), (*M42, 0.5, 0.45, 0.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.14), (0.42, 0.22), (0.2, 0.35)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        for (ra0, dec0, rad, vmax) in [(*M44, 0.75, 9.5)] + [(r, d, 0.32, 9.5) for r, d in HCHI] + \
                [(*M45, 1.1, 8.5)]:
            for k, op in ((1.0, 0.07), (0.6, 0.10)):
                s.poly_fill(runs(ellipse(ra0, dec0, rad * k, rad * k, 0.0)), fill=mw, opacity=op)
            dots = []
            for ra, dec, v in cluster_stars(S, ra0, dec0, rad, vmax):
                if v <= m.maglim:
                    continue                     # 亮星已在 L2 星點
                for p in pos(ra, dec):
                    dots.append((p[0], p[1], 0.05 + 0.028 * (vmax - v)))
            if dots:
                s.dots(dots, fill="#FFFFFF", opacity=0.85)

    def planets(s, pos, runs):
        for key, h in PL_HIP.items():
            ra, dec, v = S[h]
            for p in pos(ra, dec):
                s.circle(p[0], p[1], max(1.3, m.sz_star(v) * 5.0),
                         stroke=COLORS[PL_COLOR[key]], w=0.12, opacity=0.95)

    def radiant(s, pos, runs):
        ra0, dec0 = DAU
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

    return [("深空天體", deep), ("行星標記", planets), ("流星雨輻射點", radiant)]


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
# 六、盤上取景：讓某顆星（或某點）出現在畫面指定位置
# ══════════════════════════════════════════════════════════════════
def rot_at(lst_obs):
    """盤轉到「該地方恆星時、面向北方」（北盤逆時針＝時間前進；Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return r + 360.0 if r <= -180.0 else r


def disc_frame(m, ra, dec, fov, rot, sx=0.0, sy=0.0):
    """回傳 R 鏡頭 frame：(ra,dec) 出現在畫面中心＋(sx,sy) 畫布單位處（y 向上）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, True), True)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return (round(x - sx, 2), round(m.y_pole + y - sy, 2), fov, round(rot, 2))


def build():
    S = dict(G.load_stars(BASE))
    for k, h in PL_HIP.items():
        S[h] = PLANETS[k]
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=51, D_r=55, D_fill=-19,
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

    def star_items(size, disc=False, only=None):
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
            it = {"hip": h, "text": txt, "color": COLOR.get(h, "white"), "size": size,
                  "dx": round(dx, 2), "dy": round(dy, 2), "key": f"HIP {h}"}
            if disc:
                it["disc"] = True
            out.append(it)
        for key, h in PL_HIP.items():
            dx, dy = PL_OFF[key]
            w, _ = MC.label_box(key, size * 1.15, m.fu)
            dx = math.copysign(abs(dx) * size / 1.1 + w / 2 - 1.6, dx)
            it = {"ra": S[h][0], "dec": S[h][1], "text": key, "color": PL_COLOR[key],
                  "size": round(size * 1.15, 2), "dx": round(dx, 2), "dy": dy, "key": key}
            if disc:
                it["disc"] = True
            if only is None or h in only:
                out.append(it)
        return out

    def cons_items(size, disc=False, role=False, only=None, offs=None):
        out = []
        for ab, (keys, zh, col, dx, dy) in CONS.items():
            if offs is not None:
                dx, dy = offs.get(ab, (0.0, 0.0))
            if only is not None and ab not in only:
                continue
            if role and ab not in ROLE:
                continue
            ra, dec = centroid(uniq([W[k] for k in keys]), S)
            sc = size / 1.6
            it = dict(ra=ra, dec=dec, text=ROLE[ab] if role else zh, color=col,
                      size=size, dx=dx * sc, dy=dy * sc + (DY_ROLE * size / 1.6 if role else 0.0),
                      key=ab)
            if disc:
                it["disc"] = True
            out.append(it)
        return out

    def obj_items(size, disc=False, only=None):
        out = []
        for k, (ra, dec, txt, col, dx, dy) in OBJ.items():
            if only is not None and k not in only:
                continue
            it = dict(ra=ra, dec=dec, text=txt, color=col, size=size, dx=dx, dy=dy, key=k)
            if disc:
                it["disc"] = True
            out.append(it)
        return out

    def cn_items(size, disc=False, only=None):
        out = []
        for k, (hips, txt, col, dx, dy) in CN.items():
            if only is not None and k not in only:
                continue
            a = anchor(hips) if hips else {"ra": M44[0], "dec": M44[1]}
            it = dict(a, text=txt, color=col, size=size, dx=dx, dy=dy, key="中-" + k)
            if disc:
                it["disc"] = True
            out.append(it)
        return out

    DISC_STARS = {POLARIS, DEL_CEP, MIRFAK, ALGOL, CAPELLA}
    label_sets = [
        (cons_items(1.6), "星座名"),
        (star_items(1.1), "亮星名"),
        (obj_items(1.0), "天體"),
        (cn_items(1.15), "中國星官"),
        (cons_items(2.6, disc=True, offs=CONS_DISC), "星座名-盤"),
        (cons_items(1.9, disc=True, role=True, offs=CONS_DISC), "神話"),
        (star_items(1.9, disc=True, only=DISC_STARS), "亮星名-盤"),
        (obj_items(1.7, disc=True, only=["M31", "HCHI", "DAU"]), "天體-盤"),
        (cn_items(1.9, disc=True, only=["王良", "五車"]), "中國星官-盤"),
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
    m.L_marks(MAINS, "主角星白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot"), (MAINS, "主角星白圈", "ring")])
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole
    ROT22 = rot_at(LST_AT["10/10 22:00"])                   # −155.2：10/10 22:00 面向北方
    TRI_F = (80.0, 10.0, 50.0, 0.0)                         # 夏季大三角
    CYG_F = (72.0, 16.0, 40.0, 0.0)                         # 天鵝＋天鷹
    PEG_F = (22.0, 14.0, 44.0, 0.0)                         # 秋季四邊形
    SAT_F = (6.0, 6.0, 40.0, 0.0)                           # 土星（在四邊形下方）
    CET_F = (-8.0, -2.0, 48.0, 0.0)                         # 土星＋鯨魚座
    UP0 = (0.0, 12.0, 44.0, 0.0)                            # 走廊起點（07 T）
    SW = (0.0, yp, 44.0, 0.0)                               # 長圖 ⇄ 北盤 換組格
    CAS_F = (0.0, 66.0, 44.0, 0.0)                          # 仙后座 W（走廊上）
    FAMILY = (0.0, round(yp - 71.0, 2), 110.0, 0.0)         # 王室全家福（未旋轉；角落距盤心 ≤ R_fill）
    N22 = (0.0, round(yp + 34.0, 2), 118.0, ROT22)          # 22:00 面向北方（北極星 24°）
    CEP_F = disc_frame(m, 330.0, 66.0, 56.0, ROT22, sy=-6.0)
    PER_F = disc_frame(m, 50.0, 46.0, 60.0, ROT22, sy=-4.0)
    AUR_F = disc_frame(m, 76.0, 42.0, 62.0, ROT22, sy=-6.0)
    RAD_F = disc_frame(m, *DAU, 46.0, ROT22, sy=-8.0)
    TAU_A = (-46.0, 20.0, 40.0, 0.0)
    TAU_F = (-52.0, 18.0, 36.0, 0.0)
    ORI_F = (-69.0, -2.0, 34.0, 0.0)
    M44_A = (-112.0, 16.0, 34.0, 0.0)
    M44_Z = (-115.0, 18.6, 22.0, 0.0)
    EAST_F = (-126.0, 14.0, 42.0, 0.0)
    END_F = (-60.0, 0.0, 56.0, 0.0)

    shots = [
        dict(code="01", kind="S", sec=14, north=True,
             frames=[(80.0, 0.0, 56.0, 0.0), (62.0, 0.0, 56.0, 0.0)],
             layers=["深空", "行星"], labels=[],
             vo="十月十日，秋觀出隊。這一晚是新月，整夜沒有月光；土星剛過衝，火星闖進蜂巢。"
                "五點半日落，七點前天就全黑，一路暗到清晨四點半。今晚抬頭，第一眼找誰？",
             card="10/10 秋觀｜今晚抬頭，第一眼找誰？",
             note="開場字卡；夏季大三角往東緩慢平移（畫面往左＝時間往前），先不開連線"),
        dict(code="02", kind="Z", sec=14, north=True,
             frames=[(62.0, 0.0, 56.0, 0.0), TRI_F],
             labels_end=["亮星名"], layers=["夏", "深空", "行星"], labels=[],
             overlay="C-B01-01_方位_1930西方", overlay_layers=["天空層", "目標層"],
             vo="天一黑，先看頭頂偏西：三顆亮星排成一個大三角——織女星、牛郎星，"
                "還有天鵝尾巴上的天津四。這是夏季大三角，夏天留給秋天的最後一幕。",
             note="夏季大三角（L 夏，藍）；結束後疊方位卡 19:30（頭頂偏西）"),
        dict(code="03", kind="Z", sec=18, north=True,
             frames=[TRI_F, CYG_F],
             labels_start=["星座名", "亮星名"], layers=["夏", "深空", "行星"], labels=["星座名", "亮星名"],
             labels_end=["星座名", "中國星官"],
             vo="希臘神話裡，天鷹座是宙斯的老鷹；天鵝座有一說是宙斯變成的天鵝，"
                "沿著銀河展翅，十字形的身體又叫北十字。七夕那集的牛郎和織女，"
                "就是河鼓二和織女一；天津四，是銀河上的渡口。",
             note="推近天鵝、天鷹；迄格換中國星官（河鼓、織女、天津）"),
        dict(code="04", kind="Z", sec=21, north=True,
             frames=[CYG_F, PEG_F],
             labels_start=["星座名", "中國星官"], layers=["飛馬", "深空", "行星"], labels=["星座名", "亮星名"],
             labels_end=["星座名", "中國星官"],
             vo="轉向東方高空，四顆星框出一個大方塊：秋季四邊形，飛馬座的身體。"
                "英雄柏修斯砍下梅杜莎的頭，飛馬就從她的脖子裡躍出。中國把它看成室宿和壁宿，"
                "《詩經》說「定之方中，作于楚宮」：營室黃昏時升到正南，就是蓋房子的季節。",
             note="往東（左）滑到秋季四邊形；迄格換中國星官（室宿、壁宿）"),
        dict(code="05", kind="Z", sec=18, north=True,
             frames=[PEG_F, SAT_F],
             labels_start=["星座名", "中國星官"], labels_end=["亮星名"], layers=["飛馬", "鯨魚", "深空", "行星"], labels=["亮星名"],
             overlay="C-B01-06_土星衝", overlay_layers=["軌道層", "衝層"],
             vo="四邊形下方，那顆不閃、偏黃的亮點，就是土星。十月四日土星衝："
                "地球跑到太陽和土星正中間，三者排成一直線——土星整夜都在天上，"
                "也離我們最近、最亮。整個十月，都是看土星最好的時候。",
             note="下移到土星（行星標記：琥珀圈）；結束後疊概念圖 土星衝（軌道→一直線）"),
        dict(code="06", kind="Z", sec=20, north=True,
             frames=[SAT_F, CET_F],
             labels_start=["亮星名"], labels_end=["星座名", "亮星名"], layers=["鯨魚", "深空", "行星"], labels=["亮星名"],
             overlay="C-B01-02_方位_2200東南", overlay_layers=["天空層", "目標層"],
             vo="土星日落時從東方升起，晚上十點在東南方、仰角六十度，十一點二十分最高。"
                "它在雙魚座南緣，照國際的星座邊界，剛好跨進鯨魚座——神話裡要吞掉公主的海怪。"
                "小望遠鏡看得到環，今年只斜七度，像一道細線。",
             note="稍拉遠帶進鯨魚座；結束後疊方位卡 22:00（東南方）"),
        dict(code="07", kind="T", sec=16, north=True,
             frames=[UP0, CAS_F, SW],
             labels_start=["星座名", "天體"], labels_end=[], layers=["飛馬", "仙后", "深空", "行星"], labels=["星座名", "天體"],
             vo="順著四邊形往北，經過仙女座：那團模糊的光，是兩百五十萬光年外的仙女座大星系，"
                "肉眼看得到最遠的天體之一。再往上，一個大大的 W，是仙后座。",
             note="沿走廊從土星一路抬頭：仙女座大星系 →（中格停在仙后 W）→ 北極星（迄格＝08 起格：長圖轉北盤）"),
        dict(code="08", kind="R", sec=18, north=True,
             frames=[SW, FAMILY],
             labels_start=[], layers=["L4", "深空", "行星"], labels=[],
             vo="這一片天，是同一齣神話：王后仙后座誇口女兒比海中仙女還美，"
                "海神派海怪鯨魚座來；國王仙王座只好把公主仙女座鎖在海邊的岩石上。"
                "剛砍下梅杜莎頭的英雄英仙座經過，救下了她。",
             note="長圖轉北盤（同框換組）→ 不旋轉、拉遠成全家福（fov 110）；神話角色標在星座名下方"),
        dict(code="09", kind="R", sec=13, north=True,
             frames=[FAMILY, N22],
             labels_start=["星座名-盤", "神話"], layers=["仙后", "深空", "行星"], labels=[], horizon=[PHI],
             vo="把天空轉到今晚十點，面向北方：仙后座的 W 高掛在北偏東，北極星在正北、"
                "仰角二十四度——北極星有多高，就是你所在的緯度。",
             note=f"盤逆時針轉 {ROT22:+.1f}°（＝10/10 22:00、北緯 24° 面向北方）、拉遠到 fov 118；"
                  "山升到地平線。旋轉中不放原生標籤（字不會跟著轉）"),
        dict(code="10", kind="R", sec=21, north=True,
             frames=[N22, CEP_F],
             labels_start=["星座名-盤", "亮星名-盤"], layers=["仙后", "深空", "行星"], labels=["星座名-盤", "亮星名-盤"],
             labels_end=["星座名-盤", "亮星名-盤", "中國星官-盤"], horizon=[PHI],
             vo="旁邊像一間小屋子的，是國王仙王座。屋角的造父一，每五天多亮暗一次；"
                "這種星越亮，變得越慢，天文學家拿它當尺。一九二三年，哈伯在仙女座大星系裡"
                "找到一顆，才確定它在銀河外面。這種星，中文就叫造父變星。",
             note="同角度推近仙王座；迄格加中國星官（造父、王良）"),
        dict(code="11", kind="R", sec=17, north=True,
             frames=[CEP_F, PER_F],
             labels_start=["星座名-盤", "亮星名-盤", "中國星官-盤"], layers=["仙后", "英仙", "深空", "行星"], labels=["星座名-盤", "亮星名-盤"],
             labels_end=["星座名-盤", "亮星名-盤", "中國星官-盤"], horizon=[PHI],
             vo="王后另一邊，是在東北方升起的英雄英仙座，手上提著梅杜莎的頭。"
                "那顆眼睛叫大陵五：每兩天又二十一小時，就暗下去將近十個小時——"
                "其實是兩顆星互相遮擋。阿拉伯人叫它魔頭。",
             note="同角度往右下（東北）移到英仙座；迄格加中國星官（大陵）"),
        dict(code="12", kind="R", sec=20, north=True,
             frames=[PER_F, AUR_F],
             labels_start=["星座名-盤", "亮星名-盤", "中國星官-盤"], layers=["英仙", "御夫", "深空", "行星"], labels=["星座名-盤", "亮星名-盤"],
             labels_end=["星座名-盤", "亮星名-盤", "中國星官-盤"], horizon=[PHI],
             vo="英仙座底下，剛從東北方升起的五角形，是御夫座，最亮的五車二全天排第六。"
                "御夫是駕車的人；巧的是，中國在這片天也有車：御夫座叫五車，"
                "仙后座裡的王良、仙王座裡的造父，都是古代最會駕車的人。",
             note="同角度移到御夫座（剛出地平線）；迄格加中國星官（五車、王良、造父）"),
        dict(code="13", kind="R", sec=17, north=True,
             frames=[AUR_F, RAD_F],
             labels_start=["星座名-盤", "亮星名-盤", "中國星官-盤"], labels_end=["星座名-盤", "天體-盤"], layers=["御夫", "流星", "深空", "行星"], labels=["星座名-盤", "天體-盤"],
             horizon=[PHI],
             overlay="C-B01-03_方位_0100東北", overlay_layers=["天空層", "目標層"],
             vo="十一日清晨是御夫座 δ 流星雨極大。它很弱，每小時大概兩顆，"
                "但遇上新月，值得碰碰運氣：過了午夜，輻射點在東北方越升越高，"
                "躺下來，看整片天。",
             note="推近輻射點（流星雨輻射點層）；結束後疊方位卡 01:00（東北方）"),
        dict(code="14", kind="Z", sec=15, north=True,
             frames=[TAU_A, TAU_F],
             labels_start=["星座名", "亮星名", "天體"], layers=["御夫", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             labels_end=["星座名", "中國星官"],
             vo="往東是金牛座：宙斯變成白牛，載走公主歐羅巴，歐洲的名字據說就來自她。"
                "牛臉是 V 字形的畢宿星團，橘紅的牛眼是畢宿五；牛背上那一小團，是昴宿星團。",
             note="北盤轉長圖（盤轉回 0°、換組、沿走廊下移）→ 往東滑到金牛座；迄格換中國星官（畢、昴）"),
        dict(code="15", kind="Z", sec=18, north=True,
             frames=[TAU_F, ORI_F],
             labels_start=["星座名", "中國星官"], labels_end=["星座名", "亮星名"], layers=["獵戶", "御夫", "深空", "行星"], labels=["星座名", "亮星名"],
             overlay="C-B01-04_方位_0430南方", overlay_layers=["天空層", "目標層"],
             vo="十點多，獵戶座從東方爬起來，清晨四點半升到正南最高：紅色的參宿四、"
                "藍白的參宿七，中間三顆腰帶星。神話裡他被蠍子刺死，所以天蠍落下，他才升起。"
                "秋天熬到天亮，就能先看到冬天。",
             note="往下移到獵戶座；結束後疊方位卡 04:30（南方）"),
        dict(code="16", kind="Z", sec=20, north=True,
             frames=[ORI_F, M44_A, M44_Z],
             labels_start=["星座名", "亮星名"], layers=["巨蟹", "深空", "行星"], labels=["星座名", "亮星名", "天體"],
             labels_end=["亮星名", "天體", "中國星官"],
             overlay="C-B01-07_火星過蜂巢", overlay_layers=["星團層", "火星層"],
             vo="壓軸在東方：十二點四十分火星升起，正走進巨蟹座的蜂巢星團。"
                "十一日清晨，火星離星團中心不到半度；十二日清晨最近。"
                "拿雙筒望遠鏡看，紅色的火星就泡在一窩星星裡。這團星，中國古人叫積屍氣。",
             note="往東滑到巨蟹座，推近蜂巢星團；迄格換中國星官（鬼宿 積屍氣）；結束後疊概念圖 雙筒視野"),
        dict(code="17", kind="Z", sec=12, north=True,
             frames=[M44_Z, EAST_F],
             labels_start=["亮星名", "天體", "中國星官"], labels_end=["亮星名", "天體"], layers=["巨蟹", "深空", "行星"], labels=["亮星名", "天體"],
             overlay="C-B01-05_方位_0400東方", overlay_layers=["天空層", "目標層"],
             vo="清晨四點，火星和蜂巢已經爬到東方仰角四十多度；底下更亮、不閃的那顆是木星，"
                "再往下是獅子座的軒轅十四。",
             note="拉遠帶進木星、軒轅十四；結束後疊方位卡 04:00（東方）"),
        dict(code="18", kind="Z", sec=11, north=True,
             frames=[EAST_F, END_F],
             labels_start=["亮星名", "天體"], labels_end=["星座名"], layers=["L4", "深空", "行星"], labels=[],
             overlay="C-B01-08_今晚時間表",
             vo="新月、土星、火星，還有一場小流星雨。帶外套、紅光手電筒和雙筒望遠鏡——"
                "十月十日，秋觀見。",
             card="10/10 秋觀見｜追蹤師大天文社",
             note="拉遠、全部連線亮起；疊 9:16 今晚時間表（可存圖）；端卡＋追蹤 CTA"),
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
            if sh["kind"] == "R":
                which = "北盤圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-cx / fov * 1080), round((cy - m.y_pole) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0],
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
               "lines": LINES_KEY,
               "line_groups": LINE_GROUPS,
               "planets": {k: dict(ra=v[0], dec=v[1], mag=v[2]) for k, v in PLANETS.items()},
               "lst_at": LST_AT, "rot22": ROT22},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL,
              labels=[dict(it, pt=5) for it in label_sets[0][0] + label_sets[1][0]],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
