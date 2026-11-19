# -*- coding: utf-8 -*-
"""X-07 銀河環球：一條河、一條路、一道縫｜大畫布 v4.6（長圖帶狀主秀＋北盤一段＋南盤兩段，跨文化專題）

論點：同一條光帶，各地看見的東西分成幾家——河（中國天河、阿拉伯鴕鳥喝水的河）、路（黑腳狼之路、瓜拉尼貘之路、
洛科諾腳印、薩米／俄語／芬蘭鳥之路、白令海峽烏鴉的雪鞋腳印）、縫（蒙古天空的縫線、Igloolik 分隔線）、
活的東西（毛利長魚、曼達爾的龍）、灰（ǀXam 柴火灰、萬那杜 Nemrau）；最後回到「我們在盤子裡」和這幾晚的銀心。

來源：Stellarium（舊版 stellarium-skycultures-master）chinese（005 斗宿、008 箕宿、213 天船、224 天潢、229 天江、232 天津、
  273 咸池）、arabic_ancient（3001 下河喝水的鴕鳥、3002 喝飽離開的鴕鳥）、maori（004 塔瑪雷雷提的大獨木舟＝天蠍尾）、
  tupi（003 北方的貘，瓜拉尼；Afonso：鼻子＝天津四）、western（Cyg 天鵝座）。
  逐字稿：04_腳本庫/X-07-銀河環球一條河一條路一道縫-逐字稿-v1.md。銀心 Sgr A* J2000 17h45m40.0s −29°00′28″。
  天象 PyEphem 4.2.1 自算（恆星 J2000；台北 25.033°N、121.565°E）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 350 → 03 鏡的捲動路線（御夫咸池 x −90 → 英仙天船 −63…−42 → 仙后 −20 → 天鵝天津 +31…+54 → 人馬箕斗 +63…+79
             → 天江 +88…+91）整段在 x ±180 以內、不跨接縫；走廊 x＝0（赤經 23h20m）往北正好沿著仙后—仙王一段銀河，
             06→07 長圖轉北盤時畫面一路都在銀河上。銀心 x +83.6。
  D_s = 60、D_r = 64 → 長圖帶要容下天船（η Per +55.9、鹿豹 HIP 19949 +53.6）與天津（+30…+46.8）：逐字稿原以為天船在帶外、
             要畫「往北的箭頭」，D_s 提到 60 後整組天船都在帶內，箭頭不需要（回報）。南邊箕斗最南 η Sgr −36.8、天蠍尾 −43.2。
             R 鏡頭的主角（北盤：仙后—英仙—御夫的銀河；南盤：天蠍尾、南十字、船底）都在 |dec| < 64 的填滿環上：
             07、08、09 進出盤都由 gen_canva_pages 自動插「回中心／上移」「歸位／下移」，盤心 fov ≤ 50 換組，不在 R 起訖格直接切。
  D_fill = 15 → k＝2.2037、R_fill＝165.28（盤寬 ÷ 畫布寬＝0.918200，同 H-七夕／A-03）；|x_t|＋R_fill ≤ 180 ✓。
             南盤要放得下天蠍尾（−43 → r 104）到船底（−52…−70 → r 44–84）：整個南天銀河一格（09）。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 rot 正＝順時針＝時間前進；北盤 rot 負＝逆時針＝時間前進；每段 M&M < 170°。

鏡頭（逐字稿 13 鏡、秒數不變，總長 225 秒；鏡號不拆）
  01 長圖 Z 天蠍—人馬 → 整條夏季銀河 → 02 定格（字卡《詩經》）→ 03【硬切】御夫起捲：咸池／天潢 → 天船 → 天津 → 停在人馬（天江）
  → 04 推近箕斗＋鴕鳥兩群＋C-X07-01 → 05 拉遠整條銀河 → 天鵝（北方的貘）→ 06 定格天鵝（鳥之路）
  → 07【換北盤】仙后—英仙—御夫（縫）→ 08【硬切】南盤 天蠍尾＝船頭（活的東西）→ 09 南盤拉遠整個南天銀河（灰）
  → 10【換長圖】只留銀河＋9:16 圖卡 C-X07-02 → 11 拉遠到最大＋C-X07-03 → 12 推近銀心＋9:16 圖卡 C-X07-04 → 13 拉遠、下集
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-07"
ROOT = os.path.join(BASE, "05_素材/X-07_銀河環球")
OUT = os.path.join(ROOT, "_v4大畫布")
LST0 = 350.0
D_S, D_R, D_FILL = 60.0, 64.0, 15.0
TPE = (25.0330, 121.5654)
GC = (266.4167, -29.0078)                     # 銀心 Sgr A*（J2000）

WARN_OK = """
  07、08、09 R「起／迄格畫面含長圖側扇區」：06→07 長圖轉北盤、09→10 南盤轉長圖由 gen_canva_pages 自動插
  「回中心／上移／長圖轉北盤」「歸位／南盤轉長圖／下移」（盤心 fov ≤ 50，盤緣圈內逐點重合）再換組；07→08 是【硬切】北盤→南盤
  （旁白換主角「活的東西」），不經大畫布。R 起訖格不直接切回大畫布，⚠ 可接受。
"""

SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_old(cu):
    d = json.load(open(os.path.join(SC_OLD, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"].split()[-1]] = [s for s in segs if len(set(s)) >= 2]
    return out


CN, AR, MA, TU, WE = (load_old(c) for c in ("chinese", "arabic_ancient", "maori", "tupi", "western"))
SEG_JI, SEG_DOU = CN["008"], CN["005"]                # 箕宿、斗宿
SEG_CHUAN, SEG_HUANG, SEG_JIANG, SEG_JIN, SEG_XIAN = CN["213"], CN["224"], CN["229"], CN["232"], CN["273"]
SEG_OST_IN, SEG_OST_OUT = AR["3001"], AR["3002"]      # 下河喝水／喝飽離開的鴕鳥
SEG_WAKA = MA["004"]                                  # Te Waka o Tamarēreti（天蠍尾＝船頭）
SEG_TAPIR = TU["003"]                                 # 北方的貘（tupi，Afonso）
SEG_CYG = WE["Cyg"]


def stars_of(segs):
    return sorted({h for s in segs for h in s})


JI, DOU = stars_of(SEG_JI), stars_of(SEG_DOU)
OST_IN, OST_OUT = stars_of(SEG_OST_IN), stars_of(SEG_OST_OUT)
assert set(OST_IN) == set(JI), (OST_IN, JI)           # 箕宿四星＝下河的鴕鳥（同一組 HIP）
assert set(OST_OUT) == {92041, 92855, 93864, 93506}   # φ σ τ ζ＝斗宿一、四、五、六
CHUAN, HUANG, JIANG, JIN, XIAN = (stars_of(s) for s in (SEG_CHUAN, SEG_HUANG, SEG_JIANG, SEG_JIN, SEG_XIAN))
WAKA = stars_of(SEG_WAKA)
DENEB, CAPELLA, SCHEDAR, MIRFAK = 102098, 24608, 3179, 15863
ANTARES, SHAULA, ACRUX, GACRUX, RIGIL, HADAR = 80763, 85927, 60718, 61084, 71683, 68702
ETA_CAR, MIAPLACIDUS, AVIOR, ASPIDISKE, ALTAIR, VEGA = 52468, 45238, 41037, 45556, 97649, 91262
CAS = [746, 3179, 4427, 6686, 8886]
DOU_FADE = [90496, 89341]                              # 斗宿二、三（λ、μ）：不是鴕鳥，04 鏡淡化

LG = {
    "池": [(SEG_XIAN, "blue", 1.1), (SEG_HUANG, "blue", 1.0)],
    "船": [(SEG_CHUAN, "blue", 1.1)],
    "津": [(SEG_JIN, "blue", 1.1)],
    "江": [(SEG_JIANG, "blue", 1.1)],
    "箕斗": [(SEG_JI, "amber", 1.15), (SEG_DOU, "amber", 1.15)],
    "鴕鳥": [(SEG_OST_IN, "green", 1.1), (SEG_OST_OUT, "green", 1.1)],
    "貘": [(SEG_TAPIR, "purple", 0.9)],
    "天鵝": [(SEG_CYG, "#E8ECF5", 1.0)],
    "船頭": [(SEG_WAKA, "red", 1.15)],
}
LNAME = {"池": "連線-咸池天潢", "船": "連線-天船", "津": "連線-天津", "江": "連線-天江", "箕斗": "連線-箕宿斗宿",
         "鴕鳥": "連線-鴕鳥", "貘": "連線-北方的貘", "天鵝": "連線-天鵝座", "船頭": "連線-獨木舟船頭"}
CUSTOM_KEYS = {"銀心": "銀心", "暈": "單星光暈"}
WATER = ["池", "船", "津", "江"]

MAINS = sorted({h for k in ("池", "船", "津", "江", "箕斗", "鴕鳥", "船頭") for segs, *_ in LG[k] for s in segs for h in s}
               | {DENEB, CAPELLA, ANTARES, ALTAIR, VEGA, ACRUX, GACRUX, RIGIL, HADAR})


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


def x_to_ra(x):
    return (LST0 - x) % 360.0


def mw(l, b=0.0):
    """銀道座標 → 赤道（J2000）：標籤錨在銀河本身上"""
    ra, dec = G.gal2eq(l, b)
    return (round(ra, 3), round(dec, 3))


def _uv(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return np.array([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])


def _rd(v):
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(float(v[2])))


def sep(a, b):
    return math.degrees(math.acos(float(np.clip(_uv(*a) @ _uv(*b), -1, 1))))


def disc_xy(m, ra, dec, rot, north):
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（12 鏡、圖卡 C-X07-04 的數字）
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1]):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    return o


def altaz(radec, when):
    import ephem
    o = _obs(when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(radec[0]), math.radians(radec[1])
    s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


# ══════════════════════════════════════════════════════════════════
# 一、自訂圖層
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    wht = COLORS["white"]

    def gcen(s, pos, runs):
        for p in pos(*GC):
            s.circle(p[0], p[1], 1.6, stroke=wht, w=0.14, opacity=0.95)
            s.circle(p[0], p[1], 2.6, stroke=wht, w=0.08, opacity=0.45)
            s.polylines([[(p[0] - 0.7, p[1]), (p[0] + 0.7, p[1])], [(p[0], p[1] - 0.7), (p[0], p[1] + 0.7)]],
                        stroke=wht, w=0.08, opacity=0.9)

    return [("銀心", gcen)]


def write_custom(m, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n), lambda pts, n=north: m._runs_disc(pts, n))
                m._write_disc(s, north, name)


# ══════════════════════════════════════════════════════════════════
# 二、旁白字數（中文字＋外文音節；外文照逐字稿配音提示）
# ══════════════════════════════════════════════════════════════════
SYL = {"Linnunrata": 4, "Igloolik": 4, "Aviguti": 4, "Milky Way": 3, "ǀXam": 1}


def vo_units(t):
    n = 0
    for w, c in SYL.items():
        n += t.count(w) * c
        t = t.replace(w, " ")
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōū]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 三、名詞總表（＝標籤對照表）：key: (錨點, 原文, 英文, 中文, 顏色, 來源)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "天河": (mw(45.0), "天河・河漢", "Celestial River (Han)", "天上的漢水", "white", "《詩經・小雅・大東》毛傳「漢，天河也」"),
    "咸池": (XIAN, "咸池", "Pool of Harmony", "水池（魚囿）", "blue", "chinese 273；《晉書》「魚囿也」"),
    "天潢": (HUANG, "天潢", "Celestial Pier（Stellarium 英譯）", "積水池", "blue", "chinese 224；《說文》潢，積水池"),
    "天船": (CHUAN, "天船", "Celestial Boat", "天上的船", "blue", "chinese 213；《晉書》「所以濟不通也」"),
    "天津": (JIN, "天津", "Celestial Ford", "天上的渡口", "blue", "chinese 232"),
    "天江": (JIANG, "天江", "Celestial River", "天上的江", "blue", "chinese 229"),
    "箕宿": (JI, "箕宿", "Winnowing Basket", "箕宿", "amber", "chinese 008"),
    "斗宿": (DOU, "斗宿", "Dipper", "斗宿", "amber", "chinese 005"),
    "漢津": (None, "漢津", "Ford of the Han", "箕斗之間", "amber", "《爾雅・釋天》「箕、斗之間，漢津也」"),
    "鴕下": (OST_IN, "al-Naʿām al-wārid", "Ostriches going down to drink", "下河喝水的鴕鳥", "green",
           "arabic_ancient 3001（al-Ajaji）"),
    "鴕離": (OST_OUT, "al-Naʿām al-ṣādir", "Ostriches leaving the river", "喝飽離開的鴕鳥", "green",
           "arabic_ancient 3002；φ σ τ ζ＝斗宿一、四、五、六"),
    "狼": (mw(70.0), "Wolf Trail", "Wolf Trail（黑腳族）", "狼之路", "white", "McClintock 1910 p.324"),
    "貘": ([DENEB], "Tapi'i rapé", "Path of the Tapir（瓜拉尼）", "貘之路", "purple", "Afonso pp.1、8；tupi 003"),
    "洛科諾": (mw(30.0), "Waya nukuthi bunaha", "Path of the carriers of clay（洛科諾）", "挖陶土的人的腳印", "white",
            "lokono（Rybka 2018）"),
    "薩米": (mw(85.0), "Lodde-raiddaras", "bird path（薩米）", "鳥之路", "white", "sami（Lundmark 1982）"),
    "俄語": (mw(75.0), "Гусиная дорога", "Goose Road（俄語）", "鵝之路", "white", "russian_siberian"),
    "芬蘭": (mw(65.0), "Linnunrata", "Path of the birds（芬蘭語）", "鳥的路", "white", "芬蘭語通用詞"),
    "尤皮克": (mw(80.0), "Tanglurallret", "Raven's snowshoe track（尤皮克語）", "烏鴉的雪鞋腳印", "white",
            "MacDonald 1998 p.91（引 Nelson 1899:449）"),
    "蒙古": (mw(125.0), "Тэнгэрийн заадас", "seam of the sky（蒙古）", "天空的縫線", "white", "mongolian；A-07"),
    "因紐特": (mw(150.0), "Aviguti", "the Divider（Igloolik 因紐特）", "分隔線", "white", "MacDonald 1998 pp.91–92"),
    "毛利": (mw(345.0), "Te Ikaroa", "the long fish（毛利）", "一條長長的大魚", "white", "Te Aka；Best 1922"),
    "船頭": (WAKA, "Te Waka o Tamarēreti", "Tamarēreti's canoe", "船頭＝天蠍尾", "red", "maori 004；Te Aka"),
    "曼達爾": (mw(330.0), "Bittoéng Naga", "dragon star（曼達爾）", "龍", "white", "Rasyid et al. 2021 p.557"),
    "桑人": (mw(300.0), "ǀXam", "ǀXam（桑人的一支）", "撒上天的柴火灰", "white", "Bleek & Lloyd 1911 pp.73–77"),
    "萬那杜": (mw(320.0), "Nemrau", "ash（萬那杜 Netwar 語）", "灰", "white", "vanuatu_netwar"),
    "奶": (mw(60.0), "Milky Way", "Milky Way", "奶的路", "white", "Stellarium modern（Hercules）"),
    "銀心": (GC, "銀河中心", "Galactic Centre（Sgr A*）", "2.7 萬光年外", "white", "GRAVITY 2019、2021"),
}


# ══════════════════════════════════════════════════════════════════
# 四、建置
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    for k, segs in list(LG.items()):              # 連線裡不在星表的暗星去掉（tupi 的貘有 6 等星）
        LG[k] = [([[h for h in s if h in S] for s in sg if len([h for h in s if h in S]) >= 2], c, w)
                 for sg, c, w in segs]
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    def cxy(a):
        ra, dec = (S[a][:2] if isinstance(a, int) else a)
        return x_of(ra), dec

    def zfit(cx, cy, fov, step=0.5):
        f = fov
        while not all(m.covered(cx + sx * f / 2, cy + sy * f * 8 / 9) for sx in (-1, 1) for sy in (-1, 1)):
            f -= step
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    def cfit(pts, pad=0.18, minfov=24.0, dx=0.0, dy=0.0, band=False):
        """band=True：畫面上下緣不超過縫合帶（|y| ≤ D_r−0.5），否則填滿圓會把同一片天再畫一次（天船就是這樣露出第二份）"""
        xy = [cxy(p) for p in pts]
        xs, ys = [p[0] for p in xy], [p[1] for p in xy]
        f = max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cy = (max(ys) + min(ys)) / 2 + dy
        if band:
            cy = max(min(cy, D_R - 0.5 - f * 8 / 9), -(D_R - 0.5) + f * 8 / 9)
        return zfit((max(xs) + min(xs)) / 2 + dx, cy, f)

    def dpts(pts, rot, north):
        return [disc_xy(m, *(S[h][:2] if isinstance(h, int) else h), rot, north) for h in pts]

    def safe(cx, cy, f, north):
        yc = yp if north else -yp
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yc)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(pts, rot, north, pad=0.14, minfov=30.0, dx=0.0, dy=0.0):
        P = dpts(pts, rot, north)
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        f = max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while not safe(cx, cy, f, north):
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def bestrot(pts, north, pad=0.08, lo=-179.0, hi=180.0):
        best = None
        for r in np.arange(lo, hi, 1.0):
            fr = dfit(pts, round(float(r), 1), north, pad=pad, minfov=10.0)
            if best is None or fr[2] < best[2]:
                best = fr
        return best[3]

    # ── 長圖 ──
    F01a = cfit([ANTARES, SHAULA] + JI + DOU, pad=0.12, minfov=40.0)
    F01b = cfit([ANTARES, SHAULA, DENEB, VEGA, ALTAIR] + JIN, pad=0.08, minfov=60.0)
    F03a = cfit(XIAN + HUANG + [CAPELLA], pad=0.25, minfov=40.0, dy=-4.0, band=True)
    F03b = cfit(CHUAN + [MIRFAK], pad=0.20, minfov=40.0, band=True)
    F03c = cfit(JIN + [DENEB], pad=0.20, minfov=44.0, band=True)
    F03d = cfit(JIANG + JI + DOU, pad=0.10, minfov=44.0, dy=2.0)
    F04 = cfit(JI + DOU, pad=0.22, minfov=26.0)
    F05a = zfit(10.0, 0.0, 150.0)
    TAP = stars_of([s for sg, *_ in LG["貘"] for s in sg])
    F05b = cfit(TAP, pad=0.12, minfov=60.0, dy=-8.0)
    F06 = cfit(stars_of(SEG_CYG) + JIN, pad=0.25, minfov=46.0, band=True)
    F10 = F01b
    F11 = zfit(40.0, 0.0, 220.0)
    F12 = cfit(JI + DOU + JIANG + [GC], pad=0.16, minfov=34.0, dy=1.0)
    F13 = zfit(50.0, 0.0, 120.0)

    # ── 北盤（07：仙后—英仙—御夫，縫） ──
    ROT = {}
    NM = CAS + CHUAN + [CAPELLA] + XIAN
    ROT["07b"] = bestrot(NM, True, hi=150.0)             # 起格要在 +180° 以內（07a＝07b＋30）
    ROT["07a"] = round(ROT["07b"] + 30.0, 1)             # 由 +30° 逆時針轉到最省版面的角度（時間往前兩小時）
    F07a = dfit(NM, ROT["07a"], True, pad=0.16, minfov=60.0)
    F07b = dfit(NM, ROT["07b"], True, pad=0.16, minfov=60.0)

    # ── 南盤（08：天蠍尾＝船頭；09：整個南天銀河） ──
    SM = WAKA + JI
    ROT["08b"] = bestrot(SM, False, lo=-139.0)           # 起格要在 −180° 以內（08a＝08b−40）
    ROT["08a"] = round(ROT["08b"] - 40.0, 1)
    F08a = dfit(SM, ROT["08a"], False, pad=0.22, minfov=50.0)
    F08b = dfit(SM, ROT["08b"], False, pad=0.22, minfov=50.0)
    SW = WAKA + [ACRUX, GACRUX, RIGIL, HADAR, ETA_CAR, MIAPLACIDUS, AVIOR]
    ROT["09"] = bestrot(SW, False, lo=max(-179.0, ROT["08b"] - 90.0), hi=min(180.0, ROT["08b"] + 90.0))
    F09 = dfit(SW, ROT["09"], False, pad=0.10, minfov=80.0)

    FR = dict(F01a=F01a, F01b=F01b, F03a=F03a, F03b=F03b, F03c=F03c, F03d=F03d, F04=F04, F05a=F05a, F05b=F05b,
              F06=F06, F07a=F07a, F07b=F07b, F08a=F08a, F08b=F08b, F09=F09, F11=F11, F12=F12, F13=F13)
    print("\n── 構圖 ──")
    for kk, v in FR.items():
        print(f"  {kk} {v}")
    print("  旋轉：" + "、".join(f"{kk} {v:+.1f}°" for kk, v in ROT.items()))

    # ════════════════════ 標籤 ════════════════════
    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = _rd(sum(_uv(*S[h][:2]) for h in a))
        return {"ra": round(ra, 3), "dec": round(dec, 3)}

    def sz(px, fov):
        return px * fov / (m.fu * 1080.0)

    def item(a, text, color, px, fov, dx, dy, key, disc=False):
        it = dict(anchor(a), text=text, color=color, size=round(sz(px, fov), 3), dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    def term(key, fov, px1=60, px2=44, dx=0.0, dy=0.0, zh=None, one=False, disc=False, col=None, a=None, orig=None):
        a0, orig0, en, zh0, c, _ = TERMS[key]
        a = a if a is not None else a0
        o = orig or orig0
        if one:
            return [item(a, zh or o, col or c, px1, fov, dx, dy, key, disc)]
        g = (px1 + px2) * 0.62 * fov / 1080.0
        return [item(a, o, col or c, px1, fov, dx, dy + g / 2, key, disc),
                item(a, zh or zh0, "white", px2, fov, dx, dy - g / 2, key + "-zh", disc)]

    ford = _rd(_uv(*S[90185][:2]) + _uv(*S[92041][:2]))         # 箕宿三（ε）與斗宿一（φ）的中點＝漢津
    LB = {}
    f = F01b[2]
    LB["天河"] = term("天河", f, 64, 0, dx=-12.0, dy=0.0, one=True)
    LB["水池"] = (term("咸池", F03a[2], 60, 40, dx=8.0, dy=7.0, zh="水池")
                + term("天潢", F03a[2], 52, 40, dx=-8.0, dy=-6.0, zh="積水池"))
    LB["天船"] = term("天船", F03b[2], 60, 0, dx=0.0, dy=-6.0, one=True)
    LB["天津"] = term("天津", F03c[2], 60, 40, dx=-12.0, dy=0.0, zh="渡口")
    LB["天江"] = term("天江", F03d[2], 60, 0, dx=0.0, dy=4.5, one=True)
    f4 = F04[2]
    LB["箕斗"] = (term("箕宿", f4, 64, 0, dx=1.0, dy=-5.2, one=True)
                + term("斗宿", f4, 64, 0, dx=-1.0, dy=4.0, one=True)
                + [item(ford, "漢津", "amber", 56, f4, 0.0, 1.6, "漢津"),
                   item(ford, "箕斗之間", "white", 40, f4, 0.0, -0.4, "漢津-zh")])
    LB["鴕鳥"] = (term("鴕下", f4, 44, 40, dx=2.0, dy=-6.8)
                + term("鴕離", f4, 44, 40, dx=-1.5, dy=5.6)
                + [item(ford, "渡口", "amber", 52, f4, 0.0, 0.6, "漢津2")])
    f5a, f5b = F05a[2], F05b[2]
    ROAD = (x_to_ra(F05b[0]), F05b[1])                  # 05 迄格中心：路的三組標籤排在貘的下方（銀河往天鷹那一段）
    LB["路"] = (term("狼", f5b, 60, 44, dx=-14.0, dy=-30.0, a=ROAD)
               + term("洛科諾", f5b, 52, 44, dx=8.0, dy=-50.0, a=ROAD))
    LB["貘"] = (term("貘", f5b, 60, 44, dx=-6.0, dy=-14.0)
               + [item(TAP, "北方的貘（示意）", "purple", 40, f5b, 0.0, 14.0, "貘示意")])
    f6 = F06[2]
    BIRD = (x_to_ra(F06[0]), 20.0)                       # 三組鳥之路疊成一欄，放在天鵝座下方（銀河往天鷹那一段）
    LB["鳥"] = (term("薩米", f6, 52, 40, dx=0.0, dy=4.0, a=BIRD)
               + term("俄語", f6, 52, 40, dx=0.0, dy=-4.0, a=BIRD)
               + term("芬蘭", f6, 52, 40, dx=0.0, dy=-12.0, a=BIRD))
    LB["雪鞋"] = term("尤皮克", f6, 56, 44, dx=0.0, dy=-4.0, a=BIRD)
    f7 = F07b[2]
    SEAM = mw(140.0)                                     # 兩組同一錨點上下排（蒙古原本錨在 l=125，07 迄格被切到左緣）
    LB["縫"] = (term("蒙古", f7, 56, 44, dx=0.0, dy=12.0, disc=True, a=SEAM)
               + term("因紐特", f7, 60, 44, dx=0.0, dy=-12.0, disc=True, a=SEAM))
    f8 = F08b[2]
    LB["船頭"] = (term("船頭", f8, 52, 44, dx=8.0, dy=-8.0, disc=True)
                + [item(WAKA, "船尾在獵戶腰帶（Te Aka）", "white", 36, f8, 10.0, -19.0, "船尾", disc=True)])
    LB["活"] = (term("毛利", f8, 56, 44, dx=0.0, dy=10.0, disc=True)
               + term("曼達爾", f8, 56, 44, dx=0.0, dy=-8.0, disc=True))
    f9 = F09[2]
    ASH = mw(310.0)                                      # 同一錨點上下排，避免兩組貼在一起
    LB["灰"] = (term("桑人", f9, 60, 44, dx=0.0, dy=12.0, disc=True, a=ASH)
               + term("萬那杜", f9, 60, 44, dx=0.0, dy=-12.0, disc=True, a=ASH))
    f11 = F11[2]
    LB["奶"] = term("奶", f11, 64, 48, dx=0.0, dy=18.0)
    f12 = F12[2]
    LB["銀心"] = (term("銀心", f12, 60, 44, dx=0.0, dy=-4.6)
                + term("箕宿", f12, 48, 0, dx=1.0, dy=-4.6, one=True)
                + [item(ford, "漢津", "amber", 44, f12, 0.0, -2.0, "漢津")])
    f13 = F13[2]
    LB["下集"] = [item((x_to_ra(50.0), 30.0), "下集：第一季完結", "amber", 60, f13, 0.0, 0.0, "下集")]
    label_sets = [(v, k2) for k2, v in LB.items()]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    LG_MAIN = LG["池"] + LG["船"] + LG["津"] + LG["江"] + LG["箕斗"]
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), ([DENEB, ANTARES, CAPELLA], "單星光暈", "ring")]
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_MAIN, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    LINES_KEY = dict({"L4": "星座連線"}, **LNAME, **CUSTOM_KEYS)
    LINE_GROUPS = dict({"L4": LG_MAIN}, **LG, **{kk: [] for kk in CUSTOM_KEYS})

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=15, north=True, frames=[F01a, F01b], layers=[], labels=[],
             vo="上週在紐西蘭，昴宿升起就是新年。今晚，我們沿著銀河繞地球一圈：同一片星空，全世界看見——一條河、一條路、一道縫。",
             card="一條河、一條路、一道縫",
             note=f"長圖：天蠍—人馬起格（fov {F01a[2]:.0f}，銀河最亮的一段；銀河層在 Canva 調亮）→ Z 拉遠到整條夏季銀河"
                  f"（fov {F01b[2]:.0f}，天蠍→天鵝）；只開銀河、星點，不開連線；開場字卡"),
        dict(code="02", kind="Z", sec=10, north=True, frames=[F01b], layers=[], labels=ls("天河"),
             vo="先說河。中國人叫它天河、河漢。《詩經》寫：「維天有漢，監亦有光」——天上有一條漢水，抬頭看，也閃著光。",
             card="維天有漢，監亦有光",
             note="長圖定格（＝01 迄格）；標籤「天河・河漢」沿天鷹一段銀河；字卡用朗讀體"),
        dict(code="03", kind="Z", sec=9, north=True, cut=True, frames=[F03a, F03b, F03c, F03d], layers=WATER,
             labels_start=ls("水池"), labels=ls("天船", "天津"), labels_end=ls("天江"),
             vo="沿著這條河，中國人還放了幾座水池，像咸池；還有一艘天船、一個渡口天津，和一條天江。",
             card="咸池・天船・天津・天江",
             note="【硬切】從御夫起：咸池＋天潢（藍）→ 往西沿銀河捲：天船（英仙，D_s 提到 60 後整組在長圖帶內，不需往北的箭頭）"
                  "→ 天津（天鵝）→ 天江（蛇夫，銀心右上方）；四組依旁白順序在 Canva 亮起；終點停在人馬座，接 04 不用回捲。"
                  "捲動跨過仙后（dec +60，長圖帶上緣）用 Z 規則驗 covered（S 規則 |cy|+fov·8/9 ≤ 60 放不下天船）"),
        dict(code="04", kind="Z", sec=20, north=True, frames=[F03d, F04], layers=["箕斗", "鴕鳥", "江"],
             labels=ls("箕斗"), labels_end=ls("鴕鳥"), overlay="C-X07-01_箕斗之間",
             overlay_layers=["中國層", "阿拉伯層", "疊合層"],
             vo="再往前，是箕宿和斗宿。《爾雅》說，箕斗之間，是銀河的渡口。更巧的是，箕宿這四顆星，在古阿拉伯是四隻鴕鳥，"
                "正走下河去喝水；斗宿裡的四顆，是喝飽了、正要離開的鴕鳥。中國人的渡口，就在牠們中間。",
             card="箕斗之間，漢津也／四隻下河、四隻離開",
             note=f"長圖推近人馬座（fov {F03d[2]:.0f}→{F04[2]:.0f}）：箕宿＋斗宿（琥珀）先亮＋標籤「漢津／箕斗之間」，疊第一張字卡；"
                  "「更巧的是」起鴕鳥兩群（綠）疊上：箕宿 4 星＝下河、斗宿一四五六（φ σ τ ζ）＝離開，斗宿二、三（λ μ）淡化（Canva 調連線透明度）；"
                  "迄格換鴕鳥標籤；結束後疊 C-X07-01（中國層→阿拉伯層→疊合層）＋第二張字卡"),
        dict(code="05", kind="Z", sec=23, north=True, frames=[F04, F05a, F05b], layers=["貘"],
             labels=[], labels_start=[], labels_end=ls("路", "貘"),
             vo="也有人看見路。北美的黑腳族叫它「狼之路」，說人死了，靈魂就走這條天上的路，去到靈魂的世界。巴西很多原住民族，"
                "像瓜拉尼人，叫它「貘之路」，因為銀河裡就連出了一頭貘。南美北岸的洛科諾人說，那是去挖陶土的人留下的一串腳印。",
             card="狼之路・貘之路・腳印",
             note=f"長圖 Z 拉遠到整條銀河（fov {F05a[2]:.0f}）→ 往北捲到天鵝—仙后（fov {F05b[2]:.0f}）：瓜拉尼「北方的貘」"
                  "（紫，tupi 003；鼻子＝天津四）＋「示意」；標籤三組（Wolf Trail／Tapi'i rapé／Waya nukuthi bunaha）迄格亮；"
                  "中格（整條銀河）在 Canva 先放 Wolf Trail、Waya nukuthi bunaha 兩組（labels_end 的「路」層）"),
        dict(code="06", kind="Z", sec=21, north=True, frames=[F05b, F06], layers=["天鵝"],
             labels_start=ls("貘"), labels=ls("鳥"), labels_end=ls("雪鞋"),
             vo="也有人說，那是鳥的路。薩米人叫它「鳥之路」，西伯利亞的俄羅斯人叫「鵝之路」；芬蘭語到今天還叫它 Linnunrata，"
                "意思就是鳥的路，傳說候鳥就沿著它飛。到了白令海峽一帶，它是烏鴉走過天空留下的雪鞋腳印。",
             card="鳥之路・鵝之路／烏鴉的雪鞋腳印",
             note=f"長圖滑到天鵝定格（fov {F06[2]:.0f}；天鵝座本身就是鳥，白色現代連線）；標籤三組（Lodde-raiddaras／Гусиная дорога"
                  "（俄語）／Linnunrata）；「白令海峽」起迄格換標籤 Tanglurallret（尤皮克語，字源＝雪鞋），疊第二張字卡"),
        dict(code="07", kind="R", sec=20, north=True, frames=[F07a, F07b], layers=[], labels=ls("縫"),
             vo="還有人看見一道縫。蒙古人說，那是天空的縫線。加拿大北極圈 Igloolik 的因紐特人叫它 Aviguti，意思是分隔線。"
                "一位長老聽父親說，那是風的分界，兩股風在那裡相撞；它往哪邊偏，風就從哪邊吹來。",
             card="Aviguti＝分隔線",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）；北盤 {ROT['07a']:+.1f}°→{ROT['07b']:+.1f}°"
                  "（逆時針＝時間往前）：銀河從仙后—英仙—御夫劃過北天；不開連線；標籤（Тэнгэрийн заадас／Aviguti）；只放一張字卡"),
        dict(code="08", kind="R", sec=23, north=False, cut=True, frames=[F08a, F08b], layers=["船頭"],
             labels=ls("活"), labels_end=ls("活", "船頭"),
             vo="除了河、路和縫，也有人看見活的東西。毛利人說，那是一條長長的大魚；天蠍座彎彎的尾巴，是塔瑪雷雷提那艘大獨木舟的船頭。"
                "印尼的曼達爾漁民叫它「龍」，拿它找漁場；這條龍通常從東南方升起，要是看不見了，就怕要起大風。",
             card="大魚・龍",
             note=f"【硬切】北盤→南盤；南盤 {ROT['08a']:+.1f}°→{ROT['08b']:+.1f}°（順時針＝時間往前）轉到天蠍：天蠍尾 9 星（紅，"
                  "maori 004）標「船頭＝天蠍尾」＋小字「船尾在獵戶腰帶（Te Aka）」；標籤（Te Ikaroa／Bittoéng Naga）；"
                  "龍不畫漢式飛龍，只放標籤"),
        dict(code="09", kind="R", sec=14, north=False, frames=[F08b, F09], layers=["船頭"], labels=ls("灰"),
             labels_start=ls("活", "船頭"),
             vo="南非有一支桑人，叫 ǀXam。他們說，很久以前，有個女孩把柴火的灰撒上天，讓夜裡的人看得見回家的路。"
                "遠在太平洋的萬那杜，也叫它「灰」。",
             card="撒上天的柴火灰",
             note=f"南盤拉遠到整個南天銀河（船底—南十字—天蠍，fov {F08b[2]:.0f}→{F09[2]:.0f}，{ROT['08b']:+.1f}°→{ROT['09']:+.1f}°）；"
                  "船頭連線在 Canva 淡掉；銀河層透明度由 0 漸升（畫面語言＝灰撒上去）；標籤（ǀXam／Nemrau）"),
        dict(code="10", kind="Z", sec=15, north=True, frames=[F10], layers=[], labels=[],
             overlay="C-X07-02_銀河的名字",
             vo="北美的納瓦荷人叫它「等待黎明的」。它怎麼來的，有一個故事；但納瓦荷的星星故事只在冬天講。"
                "一月的納瓦荷那集講過了，現在是七月，這裡就不說。",
             card="故事，冬天才說",
             note="【換組】南盤→長圖（自動插歸位／南盤轉長圖／下移）；長圖整條夏季銀河，只留銀河層、不開任何連線（刻意不畫納瓦荷星座）；"
                  "字卡淡入淡出；結束後疊 9:16 圖卡 C-X07-02「銀河的名字」（可存圖）"),
        dict(code="11", kind="Z", sec=19, north=True, frames=[F10, F11], layers=[], labels_end=ls("奶"),
             overlay="C-X07-03_我們在盤子裡", overlay_layers=["側視層", "視線層"],
             vo="英文叫它 Milky Way，奶的路，相傳來自希臘神話：天后赫拉的奶，灑了一整片天。其實它是我們住的星系——"
                "一個十萬光年寬的大盤子；我們在盤子裡往盤面看，幾千億顆星，就疊成了一條河。",
             card="Milky Way＝奶的路／我們就在盤子裡",
             note=f"長圖 Z 拉遠到最大（fov {F10[2]:.0f}→{F11[2]:.0f}；上下露出南北盤）＋標籤 Milky Way／奶的路；"
                  "「其實」起疊 C-X07-03（側視層：盤＋太陽＋銀心 → 視線層：往盤面看＝一條河），第二張字卡"),
        dict(code="12", kind="Z", sec=25, north=True, frames=[F11, F12], layers=["箕斗", "銀心"], labels=ls("銀心"),
             overlay="C-X07-04_這幾晚看銀心",
             vo="夏夜，我們正對著盤子的中心，就在人馬座、剛才那個渡口旁邊，兩萬七千光年外。兩週前我們說，銀河等新月再看——"
                "就是這幾晚：今晚到下週二，晚上九點到半夜一點，月亮都不在天上。找個遠離城市燈光、南方開闊的地方；晚上十一點，它在正南方最高。",
             card="7/2–7/6・九點到一點",
             note=f"長圖推近人馬座（fov {F11[2]:.0f}→{F12[2]:.0f}）：銀心白圈（就在箕宿旁，回扣 04 鏡）＋箕斗（琥珀）＋標籤；"
                  "結束後疊 9:16 圖卡 C-X07-04「這幾晚看銀心」（7/2 台北對時，可存圖）"),
        dict(code="13", kind="Z", sec=11, north=True, frames=[F12, F13], layers=[], labels=ls("下集"),
             vo="下週五，第一季最後一集：這一年，在同一片星空裡，我們看見了多少種目光？",
             card="下集見｜第一季完結：同一片星空的 27 種目光",
             note=f"長圖拉遠（fov {F12[2]:.0f}→{F13[2]:.0f}）；端卡「下集見｜第一季完結：同一片星空的 27 種目光」＋追蹤 CTA"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"]
        cu = len(re.findall(r"[㐀-鿿A-Za-z0-9]", sh.get("card", "")))
        print(f"  {sh['code']:>3}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u/tot_s:.2f} 字/秒")
    m.check_shots(shots)
    print("  判斷後接受的 ⚠：" + WARN_OK)
    for sh in shots:
        rs = [fr[3] for fr in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 170.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° ≥ 170°")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                yc = m.y_pole if sh["north"] else -m.y_pole
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0], "位移Y px": off[1],
                         "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    print("\n── 數字核對 ──")
    print(f"  y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}")
    print(f"  x：咸池 {x_of(S[25048][0]):+.1f}、天船 {x_of(S[13268][0]):+.1f}…{x_of(S[20156][0]):+.1f}、天津四 {x_of(S[DENEB][0]):+.1f}、"
          f"箕宿一 {x_of(S[88635][0]):+.1f}、斗宿六 {x_of(S[93506][0]):+.1f}、天江 {x_of(S[85340][0]):+.1f}…{x_of(S[84314][0]):+.1f}、"
          f"銀心 {x_of(GC[0]):+.1f}")
    print(f"  天船赤緯 {min(S[h][1] for h in CHUAN):+.1f}…{max(S[h][1] for h in CHUAN):+.1f}（D_s {D_S}）")
    print(f"  銀心距箕宿一 γ² {sep(GC, S[88635][:2]):.1f}°、距天江 {min(sep(GC, S[h][:2]) for h in JIANG):.1f}°–"
          f"{max(sep(GC, S[h][:2]) for h in JIANG):.1f}°；漢津（ε—φ 中點）距銀心 {sep(GC, ford):.1f}°")
    for t in ("2027/7/2 20:00", "2027/7/2 21:00", "2027/7/2 22:59", "2027/7/3 01:00"):
        print(f"  台北 {t} 銀心 {altaz(GC, t)}")

    terms = {}
    for key, (a, orig, en, zh, col, note) in TERMS.items():
        terms[key] = dict(hips=a if isinstance(a, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                          顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot": ROT, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV = LG_MAIN + LG["鴕鳥"] + LG["貘"] + LG["天鵝"] + LG["船頭"]
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=PREV,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_MAIN)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for kk in sh.get("layers", []) for x in LINE_GROUPS.get(kk, [])]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
