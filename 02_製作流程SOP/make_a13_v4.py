# -*- coding: utf-8 -*-
"""A-13 阿拉伯半島：Thurayya 與沙漠的雨季｜大畫布 v4.6

論點：沙漠裡的季節不好從地上認，伊斯蘭曆又是純陰曆（一年 354 天，比四季短 11 天），
所以阿拉伯半島的貝都因人與農人把日曆寫在天上——黎明前東方第一次露臉的星（月站），
一顆管 13 天，28 顆排一圈，13×28＋1（al-Jabhah 14 天）＝365 天，從昴宿晨升（6/7）開年。
十二月：天蠍的頭 al-Iklīl 晨升（12/7）＝昴宿晨落＝「守望者」一升一落（anwāʾ），
昴宿落下的雨最多；沙漠最冷的四十天 al-Murabbaʿāniyya 開始。黃昏的昴宿＝牧人找斗篷。
月亮每月提早兩晚碰到昴宿（qirān）：第幾晚相會就是季節（13 冬始、11 冷露臉、9 冷螫人、7 半飽）。
北天：北極星 al-Jady（小山羊）殺了 Naʿsh，七個女兒（北斗）抬著棺架繞著它轉；兩個守衛（β、γ UMi）。
清晨金星＝al-Hawdān 之星（每晚說明早出發、每早都留下的部落）。

來源：Stellarium arabic_arabian_peninsula（Khalid al-Ajaji，新舊兩版 index.json／description／
names_dictionary；al-Ajaji 2013《al-Qāḍī anwāʾ 與星辰詩注》、2018《al-Ḫalāwī 天文詩注》與口傳）；
古典諺語（Ibn Qutayba《Kitāb al-Anwāʾ》、Quṭrub 升星曆，經 D. Adams 英譯）；
qirān 諺語（A. Al-Misnad，卡西姆大學）；納季德星曆日期（沙烏地／阿聯媒體）；PyEphem 自算。

鏡頭路線：昴宿開場 → 為什麼要星曆 → 28 站年曆（概念圖）→ 昴宿晨升＝夏 → 長圖往東滑過月站
→ 走廊往南到 Suhail → 回帶、往東滑過獅子到雨季四星 → 天蠍的頭（守望者，概念圖）→ 最冷四十天
→ 清晨金星 al-Hawdān →【硬切】黃昏昴宿（斗篷）→ 月亮會昴宿（概念圖）→ 12/21 月亮在昴宿旁
→【硬切】走廊往北到北極星 → 北盤轉：Naʿsh 的女兒繞著小山羊 → 這週末往東看（圖卡）→ 下集預告。

參數
  lst = 110 → 走廊（x=0）＝RA 110（南河三 x −4.8、兩隻小狗 x +3～+5、老人星 x +14）：
             往南的 T 鏡頭一路到老人星（Suhail），往北的 T 到北極星都在走廊上。
             月站沿黃道：昴宿 x +53 → 畢宿五 +41 → 獵戶頭 +26 → 雙子腳 +9 → 南河三 −5 → 鬼宿 −20
             → 獅子 −36…−67 → 角宿一 −91 → 天秤 −113…−119 → 天蠍頭 −130 → 心宿二 −137。
             接縫 x=±180 在 RA 290（人馬座東邊的 al-Baldah「空地」），整集不碰。
  D_s = 45、D_r = 49 → 帶內 |dec|<45：天蠍尾 −43、仙女座 +41、昴宿 +24 都在；
             北斗最南 Alkaid +49.31 剛好整把勺在北盤本體；老人星 −52.7 在南盤本體。
             （五車二 +46、天津四 +45.3 落在縫合帶：本集不標）
  D_fill = 0 → k=1.397、R_fill=125.771；盤寬 ÷ 畫布寬 ＝ 0.698728（同 A-05/07/08）
  x_tN = x_tS = 0（Canva 可水平置中）
"""
import os, sys, json, math, csv, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-13"
OUT = os.path.join(BASE, "05_素材/A-13_阿拉伯半島/_v4大畫布")
LST0 = 110.0
TPE = (25.0330, 121.5654)
RUH = (24.7136, 46.6753)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


def body_radec(name, when_utc):
    """月亮／金星的 J2000 赤經赤緯（台北站心），when_utc＝'YYYY/MM/DD HH:MM'"""
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.elevation = 0
    o.date = when_utc; o.epoch = ephem.J2000
    b = getattr(ephem, name)(); b.compute(o)
    return math.degrees(float(b.a_ra)), math.degrees(float(b.a_dec)), math.degrees(float(b.radius))


LST_AT = {"台北 12/11 18:30": lst_at(*TPE, 8, "2026/12/11 18:30"),
          "台北 12/11 20:00": lst_at(*TPE, 8, "2026/12/11 20:00")}
MOON_1221 = body_radec("Moon", "2026/12/21 12:00")      # 台北 12/21 20:00
VENUS_1212 = body_radec("Venus", "2026/12/11 22:00")    # 台北 12/12 06:00


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALCYONE, ALDEBARAN = 17702, 21421
BETELGEUSE, RIGEL, BELLATRIX, SAIPH, MEISSA = 27989, 24436, 25336, 27366, 26207
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
SIRIUS, ADHARA, WEZEN, CANOPUS, ACHERNAR = 32349, 33579, 34444, 30438, 7588
PROCYON, GOMEISA, ALHENA, CASTOR, POLLUX = 37279, 36188, 31681, 36850, 37826
REGULUS, DENEBOLA, SPICA, ARCTURUS = 49669, 57632, 65474, 69673
DSCHUBBA, ACRAB, PI_SCO, ANTARES, SHAULA = 78401, 78820, 78265, 80763, 85927
HAMAL, SHERATAN, MOTHALLAH, BETA_TRI = 9884, 8903, 8796, 10064
MARKAB, SCHEAT, ALPHERATZ, ALGENIB, MIRACH = 113963, 113881, 677, 1067, 5447
POLARIS, KOCHAB, PHERKAD = 11767, 72607, 75097
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN = 746, 3179, 4427, 6686, 8886
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
BELT = [MINTAKA, ALNILAM, ALNITAK]
MAINS = ([ALCYONE, ALDEBARAN, BETELGEUSE, RIGEL, SIRIUS, PROCYON, CANOPUS, REGULUS, DENEBOLA,
          SPICA, DSCHUBBA, ACRAB, PI_SCO, ANTARES, HAMAL, POLARIS, KOCHAB, PHERKAD, SHAULA]
         + BELT + DIPPER)

M42 = (83.82, -5.39)
M44 = (130.10, 19.67)
M45 = (56.75, 24.12)


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


def ra_of(x):
    return (LST0 - x) % 360.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium arabic_arabian_peninsula，新版 index.json）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
IDX = json.load(open(os.path.join(SC_NEW, "arabic_arabian_peninsula", "index.json"), encoding="utf-8"))
AP, AP_HIPS = {}, {}                 # AP＝連線（兩顆以上）；AP_HIPS＝全部成員（含單星月站）
for c in IDX["constellations"]:
    k = c["id"].split()[-1]
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    AP.setdefault(k, [])
    AP[k] += [s for s in segs if len(set(s)) >= 2]
    AP_HIPS.setdefault(k, set()).update(h for s in segs for h in s)

# 28 月站（本文化從昴宿數起）：(index.json id, 原文, 拼音, 中譯, 白話)
STATIONS = [
    ("Thur", "الثريا", "al-Thurayyā", "昴宿", "一位女子"),
    ("Twbi", "التويبع", "al-Twaibiʿ", "小跟班", "畢宿五"),
    ("Haqa", "الهقعة", "al-Haqʿah", "圓斑", "馬身上的旋毛"),
    ("Hana", "الهنعة", "al-Hanʿah", "低彎", ""),
    ("Thra", "الذراع", "al-Dhirāʿ", "前臂", "獅子"),
    ("Nath", "النثرة", "al-Nathrah", "鼻尖", "獅子"),
    ("Tarf", "الطرف", "al-Ṭarf", "眼睛", "獅子"),
    ("Jabh", "الجبهة", "al-Jabhah", "額頭", "獅子"),
    ("Zubr", "الزبرة", "al-Zubrah", "鬃毛", "獅子"),
    ("Sarf", "الصرفة", "al-Ṣarfah", "變天", ""),
    ("Awwa", "العوا", "al-ʿAwwāʾ", "彎弧", "吠叫的狗"),
    ("Smak", "السماك", "al-Simāk", "高舉者", "角宿一"),
    ("Ghfr", "الغفر", "al-Ghafr", "遮蓋", ""),
    ("Zban", "الزبانى", "al-Zubānā", "蠍螯", ""),
    ("Ikll", "الإكليل", "al-Iklīl", "冠冕", "天蠍的頭"),
    ("Qalb", "القلب", "al-Qalb", "心臟", "心宿二"),
    ("Shwl", "الشولة", "al-Shawlah", "翹起的蠍尾", ""),
    ("Naim", "النعائم", "al-Naʿāʾim", "鴕鳥群", ""),
    ("Blda", "البلدة", "al-Baldah", "空地", ""),
    ("SDab", "سعد الذابح", "Saʿd al-Dhābiḥ", "屠夫的吉星", ""),
    ("SBul", "سعد بلع", "Saʿd Bulaʿ", "吞嚥者的吉星", ""),
    ("SSud", "سعد السعود", "Saʿd al-Suʿūd", "吉中之吉", ""),
    ("SAkh", "سعد الأخبية", "Saʿd al-Akhbiyah", "帳篷的吉星", ""),
    ("Mqdm", "المقدم", "al-Muqaddam", "水桶前口", ""),
    ("Mkhr", "المؤخر", "al-Muʾakhkhar", "水桶後口", ""),
    ("Rsha", "الرشا", "al-Rishāʾ", "水桶繩", ""),
    ("Shrt", "الشرطين", "al-Sharaṭain", "兩個記號", ""),
    ("Btyn", "البطين", "al-Buṭain", "小肚子", ""),
]


def station_dates(year=2026):
    """納季德民間星曆：昴宿晨升 6/7 開年，每站 13 天，al-Jabhah 14 天（13×27＋14＝365）"""
    d = datetime.date(year, 6, 7)
    out = []
    for i, st in enumerate(STATIONS):
        out.append(d)
        d += datetime.timedelta(days=14 if st[0] == "Jabh" else 13)
    assert d == datetime.date(year + 1, 6, 7), d
    return out


DATES = station_dates()
LG_ST = [(AP[k], "amber", 1.0) for k, *_ in STATIONS if k not in ("Thur", "Blda")]
LG_NORTH = [(AP["BNas"], "amber", 1.0), (AP["Hjzn"], "green", 1.0),
            (AP["Shda"], "purple", 1.0), (AP["Migz"], "blue", 1.0)]
LG_FIG = [(AP["Jwza"], "blue", 1.0), (AP["Akrb"], "red", 0.85)]
LG_OTHER = [(AP["MThu"], "green", 1.0), (AP["Klib"], "blue", 1.0)]
LG_ALL = LG_ST + LG_NORTH + LG_FIG + LG_OTHER
LINE_SETS = [(LG_ST, "連線-月站"), (LG_NORTH, "連線-北天"), (LG_FIG, "連線-女子與蠍子"),
             (LG_OTHER, "連線-清真寺與小狗")]
LINES_KEY = {"L4": "星座連線", "站": "連線-月站", "北": "連線-北天", "形": "連線-女子與蠍子",
             "他": "連線-清真寺與小狗", "深空": "深空天體", "月": "月亮-1221", "金": "金星-1212"}
LINE_GROUPS = {"L4": LG_ALL, "站": LG_ST, "北": LG_NORTH, "形": LG_FIG, "他": LG_OTHER}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A 系列同一套算法）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōū]+", w.lower().replace("ʻ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層：深空天體、月亮（12/21 20:00）、金星（12/12 06:00）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
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
        if v > vmax or abs(dec - dec0) > rad:
            continue
        if math.hypot((ra - ra0) * c, dec - dec0) > rad:
            continue
        out.append((ra, dec, v))
    return out


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*M42, 0.5, 0.45, 0.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.15), (0.42, 0.24), (0.2, 0.36)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        for c0, r0 in ((M45, 1.1), (M44, 0.8)):
            for k, op in ((1.0, 0.07), (0.6, 0.10)):
                s.poly_fill(runs(ellipse(*c0, r0 * k, r0 * k, 0.0)), fill=mw, opacity=op)
        dots = []
        for c0, r0 in ((M45, 1.1), (M44, 0.8)):
            for ra, dec, v in cluster_stars(S, *c0, r0, 8.5):
                if v <= m.maglim:
                    continue
                for p in pos(ra, dec):
                    dots.append((p[0], p[1], 0.05 + 0.028 * (8.5 - v)))
        if dots:
            s.dots(dots, fill="#FFFFFF", opacity=0.85)

    def moon(s, pos, runs):
        """12/21 20:00 台北的月亮（93% 盈凸；真實大小 0.56°＋光暈）"""
        ra, dec, rad = MOON_1221
        for p in pos(ra, dec):
            for k, op in ((4.0, 0.06), (2.6, 0.10), (1.7, 0.18)):
                s.circle(p[0], p[1], rad * k, fill="#FFF6DA", opacity=op)
            s.circle(p[0], p[1], rad, fill="#FFF6DA", opacity=0.98)

    def venus(s, pos, runs):
        """12/12 06:00 台北的金星（約 −4.8 等；四芒光）"""
        ra, dec, _ = VENUS_1212
        for p in pos(ra, dec):
            x0, y0 = p[0], p[1]
            rays = []
            for i in range(4):
                a = math.radians(45 + 90 * i)
                rays.append([(x0 + 0.35 * math.cos(a), y0 + 0.35 * math.sin(a)),
                             (x0 + 1.5 * math.cos(a), y0 + 1.5 * math.sin(a))])
            s.polylines(rays, stroke="#FFFFFF", w=0.10, opacity=0.8)
            for k, op in ((1.2, 0.12), (0.7, 0.25)):
                s.circle(x0, y0, k, fill="#FFFFFF", opacity=op)
            s.circle(x0, y0, 0.36, fill="#FFFFFF", opacity=1.0)

    return [("深空天體", deep), ("月亮-1221", moon), ("金星-1212", venus)]


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
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
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

    def item(a, text, color, size, dx, dy, key, side=0, logical=None):
        """side=±1：標籤放在錨點右／左邊，dx 自動加半個字寬（東在左）。
        logical＝阿拉伯文的邏輯順序原字（Canva 原生打字用；text 是整形＋反轉後給 SVG 的字）"""
        if side:
            w, _ = MC.label_box(text, size, m.fu)
            dx = side * (abs(dx) + w / 2)
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if logical:
            it["logical"] = logical
        return it

    AR = {}                                      # 整形後 → 邏輯順序（給 Canva 原生打字）

    def ar(s):
        t = G.rtl(s)
        AR[t] = s
        return t

    # ── 28 月站：原文在上、中譯（含起始日）在下 ──
    ST_HIPS = {k: sorted(AP_HIPS[k]) for k, *_ in STATIONS if AP_HIPS.get(k)}
    ANCH = {"Thur": M45, "Blda": (293.6, -22.0)}
    #           id      原文 dx, dy     中譯 dy（相對原文）
    OFF = {"Thur": (0.0, 4.6), "Twbi": (0.0, -3.4), "Haqa": (0.0, 3.6), "Hana": (0.0, 3.9),
           "Thra": (0.0, -3.6), "Nath": (0.0, 3.6), "Tarf": (0.0, 5.6), "Jabh": (0.0, -4.4),
           "Zubr": (0.0, 4.6), "Sarf": (0.0, -3.4), "Awwa": (0.0, 5.0), "Smak": (0.0, -3.4),
           "Ghfr": (0.0, 3.6), "Zban": (0.0, -6.0), "Ikll": (0.0, 4.4), "Qalb": (0.0, -3.6),
           "Shwl": (0.0, -3.4), "Naim": (0.0, 4.4), "Blda": (0.0, 0.0), "SDab": (0.0, -3.4),
           "SBul": (0.0, -3.4), "SSud": (0.0, 3.4), "SAkh": (0.0, -4.0), "Mqdm": (0.0, -5.4),
           "Mkhr": (0.0, -5.4), "Rsha": (0.0, 4.4), "Shrt": (0.0, -3.6), "Btyn": (0.0, 3.4)}
    STA_AR, STA_ZH = [], []
    for (k, nat, pr, zh, gloss), d in zip(STATIONS, DATES):
        a = ANCH.get(k) or (ST_HIPS[k] if len(ST_HIPS[k]) > 1 else [ST_HIPS[k][0]])
        dx, dy = OFF[k]
        up = dy >= 0
        y_ar = dy + (1.1 if up else 0.0)
        y_zh = y_ar - 2.2
        zh_txt = f"{zh} {d.month}/{d.day}"
        STA_AR.append(item(a, ar(nat), "amber", 1.5, dx, y_ar, f"站-{k}", logical=nat))
        STA_ZH.append(item(a, zh_txt, "white", 1.1, dx, y_zh, f"站-{k}-zh"))

    # ── 星名（長圖帶＋南盤本體）──
    NM = [((CANOPUS,), "سهيل", "Suhail 老人星", 0.0, -3.2),
          ((SIRIUS,), "المرزم", "al-Mirzam 天狼星", 0.0, -3.0),
          ((ADHARA, WEZEN), "الكليبين", "兩隻小狗", 0.0, -3.4),
          ((BETELGEUSE, RIGEL, BELLATRIX, SAIPH), "الجوزاء", "al-Jawzā 一位女子（獵戶）", 0.0, -13.0),
          ((MINTAKA, ALNILAM, ALNITAK), "ظهر الجوزاء", "她的背（腰帶）", 11.0, -2.0),
          ((HAMAL, MOTHALLAH, BETA_TRI), "مسجد الثريا", "昴宿的清真寺", -7.0, 3.6),
          ((ra_of(x_of(VENUS_1212[0])), VENUS_1212[1]), "نجمة الهودان", "al-Hawdān 之星（金星）", 2.0, -3.4),
          ((MOON_1221[0], MOON_1221[1]), "قران", "12/21 晚上八點的月亮", 0.0, 3.2)]
    NAME_AR, NAME_ZH = [], []
    for a, nat, zh, dx, dy in NM:
        a = a if isinstance(a[0], float) else list(a)
        if isinstance(a, list) and len(a) == 1:
            a = [a[0]]
        NAME_AR.append(item(a if isinstance(a, list) else tuple(a), ar(nat), "amber", 1.4, dx, dy + 0.9,
                            f"名-{zh[:6]}", logical=nat))
        NAME_ZH.append(item(a if isinstance(a, list) else tuple(a), zh, "white", 1.05, dx, dy - 1.2,
                            f"名-{zh[:6]}-zh"))

    # ── 北天（北盤本體：|dec| ≥ 49）──
    NO = [([POLARIS], "الجدي", "al-Jady 小山羊（北極星）", 0.0, -3.0),
          ([KOCHAB, PHERKAD], "الحويجزين", "兩個守衛", 0.0, -3.4),
          (DIPPER, "بنات نعش", "Naʿsh 的女兒們（北斗）", 12.0, 0.0),
          ([CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN], "الشداد", "駱駝鞍（仙后）", -9.0, 0.0)]
    NOR_AR, NOR_ZH = [], []
    for a, nat, zh, dx, dy in NO:
        NOR_AR.append(item(a, ar(nat), "amber", 1.6, dx, dy + 1.0, f"北-{zh[:5]}", logical=nat))
        NOR_ZH.append(item(a, zh, "white", 1.15, dx, dy - 1.3, f"北-{zh[:5]}-zh"))

    label_sets = [(STA_AR, "月站原文"), (STA_ZH, "月站中譯"), (NAME_AR, "星名原文"),
                  (NAME_ZH, "星名中譯"), (NOR_AR, "北天原文"), (NOR_ZH, "北天中譯")]

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
    yp = m.y_pole

    def P(h):
        return m.pos_primary(*S[h][:2])

    can = P(CANOPUS)
    OPEN0 = (46.0, 0.0, 50.0, 0.0)            # 黃昏東方：獵戶、畢、昴
    OPEN1 = (50.0, 14.0, 28.0, 0.0)           # 昴＋畢
    THUR = (53.0, 21.0, 16.0, 0.0)            # 昴宿特寫
    SC1 = (36.0, 8.0, 40.0, 0.0)              # 月站往東滑：畢、獵戶頭、雙子腳
    CORR = (0.0, 6.0, 40.0, 0.0)              # 走廊：南河三、天狼、兩隻小狗
    SUH = (0.0, can[1] + 8.0, 44.0, 0.0)      # 走廊往南：老人星（Suhail）
    LION = (-42.0, 6.0, 40.0, 0.0)            # 獅子：眼睛、額頭、鬃毛
    WASM = (-95.0, 0.0, 48.0, 0.0)            # 雨季四星：彎弧、角宿一、遮蓋、蠍螯
    IKL = (-126.0, -8.0, 38.0, 0.0)           # 天蠍的頭（冠冕）、心宿二
    DAWN = (-114.0, -8.0, 40.0, 0.0)          # 清晨：金星（遮蓋）＋冠冕
    DUSK = (60.0, 9.0, 40.0, 0.0)             # 黃昏：昴宿、清真寺、畢宿五
    QIR = (56.0, 21.0, 18.0, 0.0)             # 月亮在昴宿旁（12/21）
    QIR2 = (55.0, 22.0, 15.0, 0.0)
    NCOR = (0.0, 20.0, 44.0, 0.0)             # 走廊（北）
    POLE = (0.0, yp, 44.0, 0.0)
    ROT_A, ROT_B = -60.0, -150.0              # 北盤逆時針（時間往前）：4 小時 → 10 小時
    DISC_A = (0.0, yp, 110.0, ROT_A)
    DISC_B = (0.0, yp, 110.0, ROT_B)
    GUIDE = (40.0, 2.0, 48.0, 0.0)            # 這週末往東看
    END = (50.0, 16.0, 30.0, 0.0)

    def ls(*names):
        return list(names)

    ST = ls("月站原文", "月站中譯")
    NMS = ls("星名原文", "星名中譯")
    shots = [
        dict(code="01", kind="Z", sec=12, north=True,
             frames=[OPEN0, OPEN1], layers=["深空"], labels=[],
             vo="上週我們說，沙漠裡的人看昴宿，就知道雨季快來了。今晚到阿拉伯半島："
                "同一片星空，沙漠裡的人看見——一本日曆。",
             card="同一片星空，沙漠裡的人看見——一本日曆。",
             note="開場字卡；黃昏東方（獵戶、畢、昴）推近到昴宿＋畢宿五（先不開連線）"),
        dict(code="02", kind="Z", sec=18, north=True,
             frames=[OPEN1, (52.0, 16.0, 24.0, 0.0)], layers=["深空"], labels=[],
             vo="沙漠裡的季節，不容易從地上看出來；伊斯蘭曆又是純陰曆，一年三百五十四天，"
                "比四季短了十一天，齋月每年都往前跑。什麼時候會下雨、什麼時候該搬家，"
                "得抬頭問星星。",
             note="緩推昴宿"),
        dict(code="03", kind="Z", sec=17, north=True,
             frames=[(52.0, 16.0, 24.0, 0.0)], layers=["深空"], labels=[],
             overlay="C-A13-01_星星年曆", overlay_layers=["月站層", "季節層", "今天層"],
             vo="他們的辦法很簡單：天快亮的時候，看東方地平線上，第一次冒出來的是哪顆星。"
                "一顆星管十三天，二十八顆排成一圈；十三乘二十八，再多一天，剛好三百六十五天。",
             note="定格疊概念圖 C-A13-01 星星年曆（月站層 → 季節層 → 今天層）"),
        dict(code="04", kind="Z", sec=17, north=True,
             frames=[(52.0, 16.0, 24.0, 0.0), THUR], layers=["站", "深空"], labels=ST,
             vo="一年從昴宿開始。六月七號前後，al-Thurayyā 在黎明前第一次露臉，夏天就到了。"
                "一千兩百年前的書上記著：它一升起，熱氣逼人，草乾得一碰就碎，成群的野驢互相啃咬。",
             note="推近昴宿；月站標籤（الثريا 昴宿 6/7）"),
        dict(code="05", kind="S", sec=16, north=True,
             frames=[THUR, SC1, CORR], layers=["站", "深空"], labels=ST,
             vo="接著十三天換一顆：先是跟在後面的小跟班 al-Twaibiʿ，就是畢宿五；"
                "再來是獵戶的頭、雙子的腳；七月底，輪到南河三——一頭大獅子的前臂。",
             note="拉遠後往東（左）滑：昴 → 畢宿五 → 獵戶頭 → 雙子腳 → 南河三（走廊）"),
        dict(code="06", kind="T", sec=14, north=True,
             frames=[CORR, SUH], layers=["站", "他", "深空"], labels=NMS,
             vo="八月底，獅子的眼睛升起時，南方低空也冒出一顆亮星：Suhail，老人星。"
                "有兩句諺語：Suhail 一出來，夜就好過了；可是看到它，別以為不會淹水。",
             note="沿走廊往南：天狼（al-Mirzam）、兩隻小狗 → 老人星（Suhail）；星名標籤"),
        dict(code="07", kind="Z", sec=21, north=True,
             frames=[SUH, CORR, LION, WASM], layers=["站", "深空"], labels=ST,
             labels_start=NMS,                 # 起格＝06 迄格（老人星）：留著 Suhail／兩隻小狗的星名
             vo="獅子的眼睛、額頭、鬃毛，一顆接一顆升上來。十月中，輪到獅子身後的四組星，"
                "雨季開始了：al-Wasm，意思是「烙印」——第一場雨，在乾地上烙下一片綠。"
                "傳說這時的雨落進海裡，會變成珍珠；落在沙地上，會長出松露。",
             note="回到走廊（＝06 倒放）→ 往東（左）滑過獅子 → 雨季四星（彎弧、高舉者、遮蓋、蠍螯）"),
        dict(code="08", kind="Z", sec=20, north=True,
             frames=[WASM, IKL], layers=["站", "形", "深空"], labels=ST,
             overlay="C-A13-02_守望者", overlay_layers=["地平層", "升起層", "落下層", "引文層"],
             vo="十二月七號，天蠍的頭——al-Iklīl，「冠冕」——在黎明前升起；"
                "同一個黎明，西邊的昴宿正好落下。阿拉伯人說，這一對互為「守望者」："
                "一個升起，另一個就落下。上週參商那種「你升我落」，阿拉伯人也看見了——只是他們拿來算雨。",
             note="往東推近天蠍的頭（al-ʿAqrab 紅線淡開）；結束後疊概念圖 C-A13-02 守望者"),
        dict(code="09", kind="Z", sec=18, north=True,
             frames=[IKL, (-128.0, -10.0, 34.0, 0.0)], layers=["站", "形", "深空"], labels=ST,
             vo="伊斯蘭以前的人相信，星星在黎明落下的那幾天會帶來雨，而昴宿落下的那幾天，被認為雨最多。"
                "從這天起，就是沙漠最冷的四十天：al-Murabbaʿāniyya。今年，它跟我們的「大雪」同一天開始。",
             note="緩推冠冕"),
        dict(code="10", kind="Z", sec=21, north=True,
             frames=[(-128.0, -10.0, 34.0, 0.0), DAWN], layers=["站", "金", "深空"],
             labels=ls("月站原文", "月站中譯", "星名原文", "星名中譯"),
             overlay="C-A13-04_沙漠星名小辭典",
             vo="這個月的清晨，冠冕上方最亮的那顆是金星，它還叫「al-Hawdān 之星」。民間故事說，al-Hawdān 部落"
                "每晚都約好：明天一早看到它就出發；結果每天早上——都決定再待一天。"
                "沙漠的星名，常常就是這麼有生活味。",
             note="往西（右）上移到金星（12/12 06:00 位置，在 al-Ghafr 一帶）；金星標籤；結束後疊 9:16 圖卡 沙漠星名小辭典（可存圖）"),
        dict(code="11", kind="Z", sec=18, north=True, cut=True,
             frames=[DUSK, (58.0, 12.0, 32.0, 0.0)], layers=["他", "深空"],
             labels=ls("星名原文", "星名中譯"),
             vo="換到黃昏：太陽一下山，昴宿已經掛在東方。一千多年前的阿拉伯人說："
                "「昴宿入夜就升起，牧羊人要找斗篷了。」這星期，台灣晚上六點半往東看，它已經快四十度高。",
             note="【硬切】回到昴宿（黃昏東方）；昴宿的清真寺（綠線）＋星名標籤"),
        dict(code="12", kind="Z", sec=26, north=True,
             frames=[(58.0, 12.0, 32.0, 0.0), QIR], layers=["月", "深空"], labels=NMS,
             overlay="C-A13-03_月亮會昴宿", overlay_layers=["月相層", "諺語層", "今年層"],
             vo="還有一招更聰明：看月亮哪一晚碰到昴宿。月亮每個月經過昴宿一次，但每個月提早兩晚——"
                "所以「第幾晚相會」，就是季節。十二月第十三晚，冬天開始；一月第十一晚，「冷，露臉了」；"
                "二月初第九晚，「冷得螫人」；二月底第七晚，「有的吃飽、有的還餓」——草開始長了。",
             note="推近昴宿，月亮（12/21 20:00）入鏡；結束後疊概念圖 C-A13-03 月亮會昴宿"),
        dict(code="13", kind="Z", sec=12, north=True,
             frames=[QIR, QIR2], layers=["月", "深空"], labels=NMS,
             vo="今年的「第十三晚」就是十二月二十一號這一夜，剛好碰上冬至。那晚抬頭，"
                "快滿的月亮就在昴宿旁邊，不到一個拳頭。",
             note="輕推；月亮與昴宿同框"),
        dict(code="14", kind="T", sec=5, north=True, cut=True,
             frames=[NCOR, POLE], layers=["北", "深空"], labels=[],
             labels_end=ls("北天原文", "北天中譯"),   # 旁白唸到 al-Jady 時就淡入（不必等到換北盤）
             vo="夜裡趕路，就看北邊。北極星叫 al-Jady，小山羊。",
             note="【硬切】回北走廊，往上到北極星；迄格＝15 起格（長圖轉北盤）"),
        dict(code="15", kind="R", sec=19, north=True,
             frames=[POLE, DISC_A, DISC_B], layers=["北"], labels=ls("北天原文", "北天中譯"),
             vo="傳說小山羊殺了一個叫 Naʿsh 的人；他的七個女兒——北斗七星——抬著父親的棺架，"
                "一夜一夜繞著北極星轉，發誓不報仇就不下葬。北極星只好找兩顆星當保鏢："
                "小熊座這兩顆，就叫「兩個守衛」。",
             note=f"長圖轉北盤 → 拉遠到 fov 110＋逆時針 {ROT_A:+.0f}° → {ROT_B:+.0f}°（{-ROT_B/15.041:.1f} 小時）；北天標籤"),
        dict(code="16", kind="Z", sec=22, north=True,
             frames=[GUIDE], layers=["形", "深空"], labels=NMS,
             overlay="C-A13-05_這週末往東看",
             vo="這週末來看：天黑以後，昴宿在東方三四十度，紅色的畢宿五在它下面；"
                "八點，獵戶整個爬上來。早起的人，清晨五點四十五分往東南看：最亮的金星正下方、"
                "貼著地平線，天蠍的頭正要升起——沙漠最冷的四十天，已經開始了。",
             note="北盤轉回長圖後回到黃昏東方；定格疊 9:16 圖卡 這週末往東看（台北 12/12；天蠍頭 12/12 只高 4–6°，12/20 前後同時刻約 12°）"),
        dict(code="17", kind="Z", sec=7, north=True,
             frames=[GUIDE, END], layers=["深空"], labels=[],
             vo="下週五往北極圈：冬天太陽不出來的地方，因紐特人用星星讀時間。",
             card="下集見｜因紐特：極夜裡的星鐘",
             note="推近昴宿；端卡＋追蹤 CTA"),
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
                xt = m.xtN if sh["north"] else m.xtS
                yc = m.y_pole if sh["north"] else -m.y_pole
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-(cx - xt) / fov * 1080), round((cy - yc) / fov * 1080))
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

    print(f"\n  月亮 12/21 20:00 RA {MOON_1221[0]:.2f} Dec {MOON_1221[1]:+.2f}（x {x_of(MOON_1221[0]):+.1f}）；"
          f"昴宿 x {x_of(M45[0]):+.1f}；金星 12/12 06:00 RA {VENUS_1212[0]:.2f} Dec {VENUS_1212[1]:+.2f}"
          f"（x {x_of(VENUS_1212[0]):+.1f}）；老人星 {tuple(round(v, 1) for v in can)}")
    print("  月站起始日：" + "、".join(f"{st[3]} {d.month}/{d.day}" for st, d in zip(STATIONS, DATES)))

    def T(hips, 原文, 拼音, 英文, 中文, 顏色, 備註):
        return dict(hips=hips, 原文=原文, 拼音=拼音, 英文翻譯=英文, 中文=中文, 顏色=顏色, 來源備註=備註)

    eng = {c["id"].split()[-1]: c["common_name"]["english"] for c in IDX["constellations"]}
    terms = {}
    for (k, nat, pr, zh, gloss), d in zip(STATIONS, DATES):
        terms[pr] = T(ST_HIPS.get(k, []), nat, pr, eng.get(k, ""), zh + (f"（{gloss}）" if gloss else ""),
                      "amber", f"第 {STATIONS.index((k, nat, pr, zh, gloss)) + 1} 站；納季德星曆起始 {d.month}/{d.day}"
                               "（昴宿晨升 6/7 起算，每站 13 天，al-Jabhah 14 天）")
    extra = [([CANOPUS], "سهيل", "Suhail", "Suhayl", "老人星", "8/24 前後晨升＝熱退；兩句諺語「Suhail 一出，夜就好過」「看到 Suhail，別以為不會淹水」"),
             ([SIRIUS], "المرزم", "al-Mirzam", "Al-Mirzam", "天狼星", "用來對第 5 站（al-Dhirāʿ）的時"),
             ([ADHARA, WEZEN], "الكليبين", "al-Klaibain", "The Two Little Dogs", "兩隻小狗（大犬 δ、ε）", "晨升＝第 6 站時節"),
             ([BETELGEUSE, RIGEL, BELLATRIX, SAIPH, MINTAKA, ALNILAM, ALNITAK], "الجوزاء", "al-Jawzā", "Al-Jawza", "一位女子（獵戶）", "與古阿拉伯同"),
             (BELT, "ظهر الجوزاء", "Ẓahr al-Jawzā", "Back of Al-Jawza", "她的背（腰帶）", "紅海漁民（Umluj）口傳"),
             ([HAMAL, MOTHALLAH, BETA_TRI], "مسجد الثريا", "Masjid al-Thurayyā", "Mosque of Al-Thurayya", "昴宿的清真寺", "Wadi al-Dawasir 口傳；在昴宿之前升起"),
             ([POLARIS], "الجدي", "al-Jady", "The Kid", "小山羊（北極星）", "傳說殺了 Naʿsh"),
             ([KOCHAB, PHERKAD], "الحويجزين", "al-Ḥuwaijzain", "The Two Guards", "兩個守衛（小熊 β、γ）", "沙漠辨方向；北極星的保鏢"),
             (DIPPER, "بنات نعش", "Banāt Naʿsh", "Daughters of Naʿsh", "Naʿsh 的女兒們（北斗）", "抬著父親的棺架繞北極星，發誓報仇"),
             ([CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN], "الشداد", "al-Shdād", "Saddle of the Camel", "駱駝鞍（仙后）", "紅海沿岸西部用名"),
             ([ACHERNAR], "محلف", "Miḥlif", "The Oath Star", "發誓之星（水委一）", "常被誤認成 Suhail，吵到發誓"),
             ([], "نجمة الهودان", "Najmat al-Hawdān", "The Star of Al-Hawdan", "al-Hawdān 之星（金星）", "民間故事：部落每晚約好明早看到它就出發、每早又決定留下（al-Hawdān 是真實部落，故事屬口傳）"),
             ([], "الجغمة", "al-Jughmah", "The Sip", "一口（金星）", "孩子討奶時，大人說等『一口』落下"),
             ([], "قران الثريا", "qirān al-Thurayyā", "Moon–Pleiades conjunction", "月亮會昴宿", "第幾晚相會＝季節（13 冬始、11 冷露臉、9 冷螫人、7 半飽、5 春草滿、3 春將盡）")]
    for hips, nat, pr, en, zh, note in extra:
        terms[pr] = T(hips, nat, pr, en, zh, "amber", note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "ar_logical": AR,
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "moon_1221": MOON_1221, "venus_1212": VENUS_1212,
               "station_dates": {st[2]: f"{d.month}/{d.day}" for st, d in zip(STATIONS, DATES)}},
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
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ST + LG_NORTH + LG_FIG + LG_OTHER,
              labels=[dict(it, pt=5) for it in STA_ZH + NAME_ZH + NOR_ZH],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
