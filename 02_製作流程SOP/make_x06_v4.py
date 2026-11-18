# -*- coding: utf-8 -*-
"""X-06 星星導航總集：在羅盤上船以前｜大畫布 v4.6（北盤＋南盤雙主秀＋長圖開場與結尾，跨文化專題）

論點：不同的海、同一套問題——方向、緯度、季節。把系列裡的航海文化（夏威夷 A-09、東加 A-10、阿努塔 A-11、
布吉斯 A-26／曼達爾 A-27、阿拉伯 A-32 的引子）串起來；「一萬年」證明不了，最早的文字紀錄是《奧德賽》，
船上用指南針最早是《萍洲可談》（1119）；最後在台北自己導航（北極星高度＝緯度、南十字、大角天頂距 6°）。

來源：Stellarium（舊版 stellarium-skycultures-master）hawaiian_starlines（MAN 魚鉤、IWI 脊椎骨）、tongan（001 南方野鴨＝南十字、
  010 ʻUvea 的圓環＝北冕、006 南門二＋馬腹一）、anutan（009 Te Paka Poi Ika Tapu＝人馬）、mandar（001 斜屋、002 鯊魚、003 魟魚）；
  新版 stellarium-master greek_almagest（UMa 托勒密大熊全形）；A-32 的 28 月站（arabic_indigenous，本土序）。
  逐字稿：04_腳本庫/X-06-星星導航總集在羅盤上船以前-逐字稿-v1.md。天象 PyEphem 4.2.1 自算（恆星 J2000）。

自訂圖層（大畫布＋南北盤同步出；全部是天球座標，盤轉到該鏡的角度時才和地平線對齊）：
  指南線（06a：南十字 γ→α 沿大圓延長到最接近南天極處；同 A-10 pointer_path）、
  阿拉伯地平線（09：北緯 20° 的地平線＋北極星正北＋五顆亮星的升起點／落下點；恆星時＝台北 5/21 20:30，與 11 鏡同角度）、
  北極星高度（11：台北 5/21 20:30 北點→北極星的大圓，25°）、十度線（11a：台北 20:30 高度 10° 等高線，方位 120°–240°）、
  天頂（11b：台北 22:14 天頂十字＋半徑 6° 虛線圈＋天頂→大角）、月亮（12：台北 21:30 站心位置，圖示放大約 3 倍＝示意）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 250 → 走廊 x＝0 在天蠍：心宿二 x +3.6、魟魚頭 β¹ Sco +8.8、人馬 x −25…−36（12、13 鏡 Z 在走廊裡、不碰洞）；
             大角 x +36、北冕 +17、南十字（南盤本體）+62。
  D_s = 45、D_r = 49 → 北盤本體要容下整個北斗（搖光 +49.3，03 鏡奧德賽）；南盤本體：南十字 −57…−63、斜屋 δ Cen −50.7、
             南門二 −60.8、鯊魚頭 α Ara −49.9、β Ara −55.5。長圖帶容下天蠍（ζ² −42.4、θ −43.0）。k＝1.3975。
  D_fill = −35 → R_fill＝174.68（盤寬 ÷ 畫布寬＝0.970456 ⚠ 只差 3%，Canva 別設成同寬）。決定因素：
             09b 北盤要放得下整圈黃道（dec −23.4 → r 158）＋28 月站；08 南盤要收人馬（dec −17 → r 102）；
             11b 台北天頂（dec +25 → r 91）。|x_t|＋R_fill ≤ 180 ✓。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 rot＝lst_obs−lst（順時針＝時間前進）；北盤 rot＝−((lst_obs＋180−lst) mod 360)（逆時針）；每段 M&M < 170°。

鏡頭路線（逐字稿 16 鏡 → 本檔 19 鏡：06／09／11 各拆兩段，因為一鏡只能用一個圖層組或一組概念圖；秒數照字數分，總長 244 不變）
  01 長圖 Z 航海星路總覽（夏威夷綠→東加琥珀→阿努塔藍→布吉斯／曼達爾紅→阿拉伯紫依序淡入）→ 02 定格 C-X06-01 莎湖層
  → 03【換北盤】（自動插回中心／上移）希臘 38°N 面北、大熊（白）→ 03b 定格 C-X06-01（奧德賽、萍洲可談）
  → 04 北盤慢轉＋C-X06-01 南島層 → 05 夏威夷 19.6°N 面北：大角爬到天頂；起格疊 C-A09-01 星羅盤（沿用 A-09）
  → 06 北盤滑到北冕（ʻUvea 的圓環）→ 06a【硬切】南盤：野鴨＋指南線 → 07 南盤轉向天蠍＋C-X06-05 星路
  → 08 南盤 斜屋→魟魚→鯊魚四段 → 08b 定格 → 09【硬切】北盤 北緯 20° 地平線：北極星→東方升起點＋C-X06-02
  → 09b 拉遠到整圈 28 月站 → 10 定格圖卡 C-X06-03 → 11 台北 20:30 面北：北極星 25° → 11a【硬切】南盤台北面南：南十字
  → 11b【硬切】北盤台北 22:14：大角離天頂 6° → 12【換長圖】（自動插歸位／北盤轉長圖／下移）天蠍＋月亮＋C-X06-04
  → 13 拉遠到黃道帶、28 月站

逐字稿的畫面構想改了幾處（回報）：01 雙盤並排改成長圖一格（北盤、長圖帶、南盤本來就在同一張大畫布上，一格就看得到北極星到南十字）；
  04、07 改在盤上（04 留在北盤、07 留在南盤，省掉兩次長圖⇄盤換組＝少 6–8 頁）；07 的 C-A11-03 是「阿努塔往 Tikopia」
  （方向相反、標的是 Te Paka Poi Ika Tapu），本集改出 C-X06-05「星路」示意（Tikopia→阿努塔，不指認九顆星）；
  08 南十字在 dec −60，長圖帶放不下 → 08、08b 在南盤做。
"""
import os, sys, json, math, csv, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS, great_circle, horizon_points
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-06"
ROOT = os.path.join(BASE, "05_素材/X-06_星星導航總集")
OUT = os.path.join(ROOT, "_v4大畫布")
LST0 = 250.0
D_S, D_R, D_FILL = 45.0, 49.0, -35.0

TPE = (25.0330, 121.5654)
PHI_GR, PHI_HI, PHI_AR, PHI_T = 38.0, 19.6, 20.0, 25.03

WARN_OK = """
  03–11b R「起／迄格畫面含長圖側扇區」：盤⇄盤之間都是【硬切】新構圖（06→06a、08b→09、11→11a→11b），
  長圖→北盤（02→03）、北盤→長圖（11b→12）由 gen_canva_pages 自動插「回中心／上移」「歸位」（盤心 fov ≤ 50，盤緣圈內逐點重合）再換組，
  不會從 R 鏡頭的起訖格直接切回大畫布。
"""


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(when, lat=TPE[0], lon=TPE[1]):
    return math.degrees(_obs(lat, lon, 8, when).sidereal_time())


def rot_n(lst_obs):
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return round(r + 360.0 if r <= -180.0 else r, 2)


def rot_s(lst_obs):
    return round((lst_obs - LST0 + 180.0) % 360.0 - 180.0, 2)


def altaz(radec, when, where=TPE):
    import ephem
    o = _obs(*where, 8, when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(radec[0]), math.radians(radec[1])
    s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


def moon_radec(when):
    """月亮的站心位置（台北），換回 J2000 才能和恆星（J2000）畫在一起；a_ra 是地心，差到 0.8°（視差）"""
    import ephem
    o = _obs(*TPE, 8, when)
    b = ephem.Moon(); b.compute(o)
    eq = ephem.Equatorial(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=ephem.J2000)
    return math.degrees(eq.ra), math.degrees(eq.dec), math.degrees(b.alt), math.degrees(b.az), b.phase


T = {"1130": "2027/5/21 20:30", "11b": "2027/5/21 22:14", "12": "2027/5/21 21:30"}
LST_AT = {k: lst_at(v) for k, v in T.items()}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, ARCTURUS, SPICA, VEGA, ALTAIR, CAPELLA, ALCYONE = 11767, 69673, 65474, 91262, 97649, 24608, 17702
DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]
ACRUX, MIMOSA, GACRUX, IMAI, DEL_CEN = 60718, 62434, 61084, 59747, 59196
CRUX = [GACRUX, ACRUX, MIMOSA, IMAI]
RIGIL, HADAR = 71683, 68702
ANTARES, TAU_SCO, BET_SCO = 80763, 81266, 78820
G_SCO, THE_SCO, ARA_A, ARA_B, ARA_T, TEL_A, EPS_SGR, SIG_SGR = 87261, 86228, 85792, 85258, 88714, 90422, 90185, 92855
ALPHECCA = 76267
SCP = (0.0, -89.999)
NCP = (0.0, 89.999)

SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_old(cu):
    d = json.load(open(os.path.join(SC_OLD, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"].split()[-1]] = [s for s in segs if len(set(s)) >= 2]
    return out


def sc_new(cu, cid):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    for c in d.get("constellations", []):
        if c["id"].split()[-1] == cid:
            return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])
                    if l and not isinstance(l[0], list)]
    raise KeyError(cu + " " + cid)


HW, TG, AN, MD = load_old("hawaiian_starlines"), load_old("tongan"), load_old("anutan"), load_old("mandar")
SEG_MAN = HW["MAN"]                                   # 夏威夷 Manaiakalani 魚鉤（天蠍）
SEG_IWI = HW["IWI"]                                   # 脊椎骨：北極星—天樞、搖光—大角—角宿一
SEG_TOLOA = TG["001"]                                 # 南方野鴨（Collocott：Toloa）＝南十字 γ–α、β–δ
SEG_RING = TG["010"]                                  # ʻAo ʻo ʻUvea（Stellarium 推測北冕）
SEG_FUNG = TG["006"]                                  # 南門二＋馬腹一
SEG_ANFISH = AN["009"]                                # Te Paka Poi Ika Tapu（人馬）
SEG_HOUSE, SEG_SHARK, SEG_RAY = MD["001"], MD["002"], MD["003"]
_sh = SEG_SHARK[0]
assert len(set(_sh)) == 17 and _sh[0] == _sh[-1] == G_SCO, _sh
_i = {h: i for i, h in enumerate(_sh[:-1])}
SEG_SH_FIN = [_sh[:_i[THE_SCO] + 1]]
SEG_SH_HEAD = [_sh[_i[THE_SCO]:_i[ARA_T] + 1]]
SEG_SH_BELLY = [_sh[_i[ARA_T]:_i[EPS_SGR] + 1]]
SEG_SH_TAIL = [_sh[_i[EPS_SGR]:]]
SEG_UMA = sc_new("greek_almagest", "UMa")             # 托勒密大熊全形


def stars_of(segs):
    return sorted({h for s in segs for h in s})


HOUSE, RAY, SHARK = stars_of(SEG_HOUSE), stars_of(SEG_RAY), stars_of(SEG_SHARK)
UMA = stars_of(SEG_UMA)
RING = stars_of(SEG_RING)

LG = {
    "夏": [(SEG_MAN, "green", 1.0), (SEG_IWI, "green", 1.0)],
    "東": [(SEG_TOLOA, "amber", 1.1), (SEG_RING, "amber", 1.0), (SEG_FUNG, "amber", 1.0)],
    "努": [(SEG_ANFISH, "blue", 1.1)],
    "曼": [(SEG_HOUSE, "red", 1.0), (SEG_RAY, "red", 1.0), (SEG_SHARK, "red", 1.0)],
    "熊": [(SEG_UMA, "#E8ECF5", 1.0)],
    "環": [(SEG_RING, "amber", 1.2)],
    "鴨": [(SEG_TOLOA, "amber", 1.2)],
    "屋": [(SEG_HOUSE, "amber", 1.2)],
    "魟": [(SEG_RAY, "purple", 1.1)],
    "鰭": [(SEG_SH_FIN, "red", 1.0)], "頭": [(SEG_SH_HEAD, "red", 1.0)],
    "肚": [(SEG_SH_BELLY, "red", 1.0)], "尾": [(SEG_SH_TAIL, "red", 1.0)],
}
LNAME = {"夏": "連線-夏威夷", "東": "連線-東加", "努": "連線-阿努塔", "曼": "連線-布吉斯曼達爾",
         "熊": "連線-大熊座", "環": "連線-Uvea圓環", "鴨": "連線-野鴨", "屋": "連線-斜屋", "魟": "連線-魟魚",
         "鰭": "連線-鯊魚背鰭", "頭": "連線-鯊魚頭", "肚": "連線-鯊魚肚子", "尾": "連線-鯊魚尾"}
SHARK_ALL = ["鰭", "頭", "肚", "尾"]
CUSTOM_KEYS = {"指南": "指南線", "阿地": "阿拉伯地平線", "極高": "北極星高度", "十度": "十度線",
               "天頂": "天頂", "月": "月亮", "暈": "單星光暈", "站": "月站標記", "阿極": "阿拉伯-北極星"}

# 28 月站（A-32 本土序；每站取最亮的星當標記，昴宿取昴宿六；空地 al-Baldah 沒有星 → 取 Stellarium 區域的中心）
import make_a32_v4 as A32
ST_MARK = []
for k, *_ in A32.STATIONS:
    hs = [h for h in A32.ST_HIPS[k] if h in A32.S0]
    if k == "Thur":
        ST_MARK.append(ALCYONE)                       # 昴宿在 Stellarium 是星團（沒有連線星）→ 昴宿六
    elif hs:
        ST_MARK.append(min(hs, key=lambda h: A32.S0[h][2]))
BALDAH_C = (float(np.mean([p[0] for p in A32.BALDAH])), float(np.mean([p[1] for p in A32.BALDAH])))
BALDAH_ID = 9300001
ST_MARK.append(BALDAH_ID)
assert len(ST_MARK) == 28, len(ST_MARK)

MAINS = sorted({h for g in LG.values() for segs, *_ in g for s in segs for h in s}
               | {POLARIS, ARCTURUS, ANTARES, VEGA, ALTAIR, CAPELLA, ALCYONE})


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


def _uv(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return np.array([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])


def _rd(v):
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(float(v[2])))


def sep(a, b):
    return math.degrees(math.acos(float(np.clip(_uv(*a) @ _uv(*b), -1, 1))))


def pointer_path(S, n=90):
    """南十字長軸 γ→α 沿大圓往南延長到最靠近南天極處（A-10 同法）"""
    g, a = _uv(*S[GACRUX][:2]), _uv(*S[ACRUX][:2])
    ang = math.acos(float(np.clip(g @ a, -1, 1)))
    w = a - g * (g @ a); w /= np.linalg.norm(w)
    s = np.array([0.0, 0.0, -1.0])
    t_star = math.atan2(float(s @ w), float(s @ g))
    seg1 = [_rd(g * math.cos(ang * i / 12) + w * math.sin(ang * i / 12)) for i in range(13)]
    seg2 = [_rd(g * math.cos(ang + (t_star - ang) * i / n) + w * math.sin(ang + (t_star - ang) * i / n))
            for i in range(n + 1)]
    p = g * math.cos(t_star) + w * math.sin(t_star)
    miss = 90.0 - math.degrees(math.asin(-float(p[2])))
    return seg1, seg2, t_star / ang, miss


def altaz_to_radec(alt, az, phi, lst):
    """地平座標 → 赤道（不含折射；方位 0＝北、90＝東）"""
    p, h, A = math.radians(phi), math.radians(alt), math.radians(az)
    sd = math.sin(p) * math.sin(h) + math.cos(p) * math.cos(h) * math.cos(A)
    d = math.asin(sd)
    cH = (math.sin(h) - math.sin(p) * sd) / (math.cos(p) * math.cos(d))
    H = math.degrees(math.acos(max(-1, min(1, cH))))
    if math.sin(A) > 0:
        H = -H
    return (lst - H) % 360.0, math.degrees(d)


def rise_set(dec, phi, lst):
    """赤緯 dec 的星在北緯 phi 的升起點／落下點（地平線上的天球位置，恆星時 lst 那一刻）"""
    c = -math.tan(math.radians(phi)) * math.tan(math.radians(dec))
    H0 = math.degrees(math.acos(max(-1, min(1, c))))
    return ((lst + H0) % 360.0, dec), ((lst - H0) % 360.0, dec)


L09 = LST_AT["1130"]                  # 09 鏡的地平線恆星時（與 11 鏡同角度，10→11 才滑得過去）
RISERS = [(CAPELLA, "五車二"), (VEGA, "織女"), (ALCYONE, "昴宿"), (ARCTURUS, "大角"), (ALTAIR, "牛郎")]


# ══════════════════════════════════════════════════════════════════
# 二、自訂圖層
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    red, pur, amb, wht, blu = COLORS["red"], COLORS["purple"], COLORS["amber"], COLORS["white"], COLORS["blue"]

    def pointer(s, pos, runs):
        seg1, seg2, ratio, miss = pointer_path(S)
        s.polylines(runs(seg1), stroke=red, w=0.16, opacity=0.9)
        s.polylines(runs(seg2), stroke=red, w=0.14, opacity=0.85, dash="0.9,0.6")
        for p in pos(*SCP):
            s.circle(p[0], p[1], 0.9, stroke=red, w=0.12, opacity=0.95)
            s.polylines([[(p[0] - 1.6, p[1]), (p[0] + 1.6, p[1])], [(p[0], p[1] - 1.6), (p[0], p[1] + 1.6)]],
                        stroke=red, w=0.08, opacity=0.9)

    def arab(s, pos, runs):
        hz = horizon_points(PHI_AR, L09, n=721)
        s.polylines(runs(hz), stroke=wht, w=0.16, opacity=0.75)
        for h, _ in RISERS:
            for rd in rise_set(S[h][1], PHI_AR, L09):
                for p in pos(*rd):
                    s.circle(p[0], p[1], 1.3, stroke=pur, w=0.16, opacity=0.95)
                    s.circle(p[0], p[1], 0.45, fill=pur, opacity=0.9)
        north = altaz_to_radec(0.0, 0.0, PHI_AR, L09)
        for p in pos(*north):
            s.polylines([[(p[0], p[1] - 1.6), (p[0], p[1] + 1.6)]], stroke=pur, w=0.18, opacity=0.95)

    def polaris_alt(s, pos, runs):
        L = LST_AT["1130"]
        npt = altaz_to_radec(0.0, 0.0, PHI_T, L)
        pol = S[POLARIS][:2]
        s.polylines(runs(great_circle(*npt, *pol)), stroke=amb, w=0.20, opacity=0.95)
        for p in pos(*npt):
            s.polylines([[(p[0] - 1.4, p[1]), (p[0] + 1.4, p[1])]], stroke=amb, w=0.16, opacity=0.95)

    def ten_deg(s, pos, runs):
        L = LST_AT["1130"]
        pts = [altaz_to_radec(10.0, az, PHI_T, L) for az in np.arange(120.0, 240.01, 1.0)]
        s.polylines(runs(pts), stroke=amb, w=0.14, opacity=0.85, dash="0.9,0.6")

    def zenith(s, pos, runs):
        L = LST_AT["11b"]
        z = (L % 360.0, PHI_T)
        zc = _uv(*z)
        e1 = np.cross(zc, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(zc, e1)
        r = math.radians(6.0)
        ring = [_rd(zc * math.cos(r) + math.sin(r) * (e1 * math.cos(t) + e2 * math.sin(t)))
                for t in np.linspace(0, 2 * math.pi, 121)]
        s.polylines(runs(ring), stroke=wht, w=0.12, opacity=0.8, dash="0.7,0.5")
        s.polylines(runs(great_circle(*z, *S[ARCTURUS][:2])), stroke=amb, w=0.16, opacity=0.95)
        for p in pos(*z):
            s.polylines([[(p[0] - 1.2, p[1]), (p[0] + 1.2, p[1])], [(p[0], p[1] - 1.2), (p[0], p[1] + 1.2)]],
                        stroke=wht, w=0.12, opacity=0.95)

    def moon(s, pos, runs):
        ra, dec = MOON12[:2]
        for p in pos(ra, dec):
            for rr, op in ((2.6, 0.06), (1.8, 0.10), (1.2, 0.18)):
                s.circle(p[0], p[1], rr, fill=wht, opacity=op)
            s.circle(p[0], p[1], 0.78, fill="#F4F1E6", opacity=0.97)

    return [("指南線", pointer), ("阿拉伯地平線", arab), ("北極星高度", polaris_alt), ("十度線", ten_deg),
            ("天頂", zenith), ("月亮", moon)]


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


def disc_xy(m, ra, dec, rot, north):
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；外文照逐字稿配音提示的音節數）
# ══════════════════════════════════════════════════════════════════
SYL = {"Hōkūleʻa": 4, "Mau Piailug": 4, "ʻUvea": 3, "Toloa": 3, "Tikopia": 4, "Ibn Mājid": 5}


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
# 四、名詞總表（＝標籤對照表）：key: (錨點, 原文, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "夏威夷": ([ARCTURUS], "夏威夷", "Hawaiʻi", "夏威夷：魚鉤、脊椎骨", "green", "hawaiian_starlines MAN、IWI；A-09"),
    "東加": (RING, "東加", "Tonga", "東加：野鴨、ʻUvea 的圓環", "amber", "tongan 001、010；Collocott 1922；A-10"),
    "阿努塔": (stars_of(SEG_ANFISH), "阿努塔", "Anuta", "阿努塔：星路上的魚", "blue", "anutan 009；A-11"),
    "布吉斯曼達爾": (CRUX, "布吉斯・曼達爾", "Bugis & Mandar", "斜屋、魟魚、鯊魚", "red",
                 "mandar 001–003；Rasyid et al. 2021；A-26、A-27"),
    "阿拉伯": ([POLARIS], "阿拉伯", "Arab navigators", "北極星＝正北（al-Jāh）", "purple", "Tibbetts 1971（未親核）"),
    "大熊": (UMA, "Ἄρκτος", "the Bear (Ursa Major)", "大熊（又叫車）", "white", "Odyssey 5.273；greek_almagest UMa"),
    "北極星": ([POLARIS], "北極星", "Polaris", "北極星", "white", ""),
    "Hōkūleʻa": ([ARCTURUS], "Hōkūleʻa", "Star of Gladness", "大角星", "green", "hawaiian_starlines；A-09"),
    "ʻUvea": (RING, "ʻAo ʻo ʻUvea", "Cloud/Ring of ʻUvea", "ʻUvea 的圓環", "amber",
              "tongan 010；拼法照 A-10（待查核 17）；Stellarium 推測北冕座"),
    "Toloa": (CRUX, "Toloa", "wild duck", "野鴨（南十字）", "amber", "Collocott 1922；tongan 001"),
    "南天極": (SCP, "南天極", "South Celestial Pole", "南天極", "red", ""),
    "Sapo Kepang": (HOUSE, "Sapo Kepang", "Slanted House", "斜屋", "amber", "mandar 001；布吉斯 bola képpang（瘸腿的房子）"),
    "Lambaru": (RAY, "Lambaru", "Stingray", "魟魚", "purple", "mandar 003；11 月底清晨升起"),
    "Mangiwang": (SHARK, "Mangiwang", "Shark", "鯊魚", "red", "mandar 002；12 月底清晨升起"),
    "心宿二": ([ANTARES], "心宿二", "Antares", "心宿二", "red", ""),
    "月亮": ((0.0, 0.0), "月亮", "Moon", "月亮", "white", "PyEphem 台北 5/21 21:30 站心；圖示放大約 3 倍"),
}


# ══════════════════════════════════════════════════════════════════
# 五、建置
# ══════════════════════════════════════════════════════════════════
MOON12 = None


def build():
    global MOON12
    S = dict(G.load_stars(BASE))
    S[BALDAH_ID] = (BALDAH_C[0], BALDAH_C[1], 99.0)
    MOON12 = moon_radec(T["12"])
    TERMS["月亮"] = ((round(MOON12[0], 3), round(MOON12[1], 3)),) + TERMS["月亮"][1:]
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    _orig = m._mark_parts

    def _mark_parts(hips, positions, style):
        out = []
        for h in hips:
            if h == BALDAH_ID:
                r = m.sz_star(3.0) * 1.5
                out += [(p[0], p[1], r if style == "dot" else max(1.1, r * 4.0)) for p in positions(h)]
            else:
                out += _orig([h], positions, style)
        return out
    m._mark_parts = _mark_parts

    # ── 構圖工具 ──
    def dpts(hips, rot, north):
        return [disc_xy(m, *(S[h][:2] if isinstance(h, int) else h), rot, north) for h in hips]

    def safe(cx, cy, f, north):
        yc = yp if north else -yp
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yc)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(hips, rot, north, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None):
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while not safe(cx, cy, f, north):
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def hfit(hips, rot, north, phi, fov, fh=0.20, dx=0.0, top=0.13):
        """有地平線的盤構圖：地平線（北／南點）放在離畫面下緣 fh 的高度，目標星水平置中"""
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        y_h = (yp - k * phi) if north else (-yp + k * phi)
        f = fov
        cx = (max(xs) + min(xs)) / 2 + dx
        cy = y_h + (0.5 - fh) * f * 16 / 9
        while not safe(cx, cy, f, north):
            f *= 0.99
            cy = y_h + (0.5 - fh) * f * 16 / 9
        if max(ys) > cy + (0.5 - top) * f * 16 / 9:
            print(f"  ⚠ hfit：最高的星超出上緣安全區 {max(ys) - cy - (0.5 - top) * f * 16 / 9:+.1f}（fov {f:.1f}）")
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def zfit(cx, cy, fov):
        """大畫布 Z：四角都要有內容（covered），不行就縮小 fov"""
        f = fov
        while not all(m.covered(cx + sx * f / 2, cy + sy * f * 8 / 9) for sx in (-1, 1) for sy in (-1, 1)):
            f -= 0.5
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    def bestrot(hips, north, pad=0.06):
        best = None
        for r in np.arange(-179.0, 180.0, 1.0):
            fr = dfit(hips, round(float(r), 1), north, pad=pad, minfov=10.0)
            if best is None or fr[2] < best[2]:
                best = fr
        return best[3]

    # ── 長圖 ──
    yP = disc_xy(m, *S[POLARIS][:2], 0.0, True)[1]
    yC = min(disc_xy(m, *S[h][:2], 0.0, False)[1] for h in CRUX)
    cy01 = round((yP + yC) / 2, 2)
    F01a = zfit(8.0, cy01, 140.0)
    F01b = zfit(8.0, cy01, F01a[2] - 6.0)
    ax_ = x_of(S[ANTARES][0])
    F12 = zfit(round(ax_ - 1.0, 2), -29.0, 46.0)
    F13 = zfit(-8.0, -6.0, 120.0)

    # ── 北盤 ──
    ROT = {}
    ROT["03"] = rot_n(165.0)                    # 希臘：北斗在北極星上方（上中天附近）
    ROT["04"] = rot_n(165.0 + 30.0)             # 04：天空繼續轉兩個鐘頭（時間在走，配南島概念圖）
    ARC_RA = S[ARCTURUS][0]
    ROT["05a"] = rot_n(ARC_RA - 45.0)           # 夏威夷：大角離上中天還有 3 小時
    ROT["05b"] = rot_n(ARC_RA)                  # 大角上中天＝夏威夷天頂
    ROT["06"] = ROT["05b"]
    ROT["09"] = rot_n(L09)
    ROT["11"] = rot_n(LST_AT["1130"])
    ROT["11b"] = rot_n(LST_AT["11b"])
    F03 = hfit(UMA + [POLARIS], ROT["03"], True, PHI_GR, 116.0, fh=0.10, top=0.10)
    F04 = hfit(UMA + [POLARIS], ROT["04"], True, PHI_GR, 116.0, fh=0.10, top=0.10)
    F05a = hfit([POLARIS, ARCTURUS], ROT["05a"], True, PHI_HI, 106.0, fh=0.14)
    F05b = hfit([POLARIS, ARCTURUS], ROT["05b"], True, PHI_HI, 106.0, fh=0.14)
    F06 = dfit(RING + [ARCTURUS], ROT["06"], True, pad=0.25, minfov=44.0, dy=-2.0)
    pn = disc_xy(m, *altaz_to_radec(0.0, 0.0, PHI_AR, L09), ROT["09"], True)
    F09a = (round(pn[0], 2), round(pn[1] + 0.30 * 64.0 * 16 / 9, 2), 64.0, ROT["09"])
    rp = [disc_xy(m, *rise_set(S[h][1], PHI_AR, L09)[0], ROT["09"], True) for h, _ in RISERS]
    xs_, ys_ = [p[0] for p in rp], [p[1] for p in rp]
    cxb, cyb = (min(xs_) + max(xs_)) / 2 - 4.0, (min(ys_) + max(ys_)) / 2 + 22.0
    fb = 108.0
    while not safe(cxb, cyb, fb, True):
        fb -= 1.0
    F09b = (round(cxb, 2), round(cyb, 2), fb, ROT["09"])
    fc = 172.0
    while not safe(0.0, yp, fc, True):
        fc -= 0.5
    F09c = (0.0, round(yp, 2), fc, ROT["09"])
    F11 = hfit([POLARIS], ROT["11"], True, PHI_T, 64.0, fh=0.22)
    F11b = hfit([ARCTURUS, POLARIS], ROT["11b"], True, PHI_T, 112.0, fh=0.10, top=0.10)

    # ── 南盤 ──
    ROT["06a"] = rot_s(S[ACRUX][0])             # 南十字上中天：頭（γ）在上、指南線朝下
    ROT["08"] = bestrot(HOUSE + RAY + SHARK, False, pad=0.10)
    ROT["11a"] = rot_s(LST_AT["1130"])
    F06a = dfit(CRUX + [SCP, RIGIL, HADAR], ROT["06a"], False, pad=0.20, minfov=44.0)
    F07 = dfit(HOUSE + RAY[:4], ROT["08"], False, pad=0.30, minfov=60.0)
    F08a = dfit(HOUSE + [RIGIL, HADAR], ROT["08"], False, pad=0.25, minfov=44.0)
    F08b = dfit(HOUSE + RAY + SHARK, ROT["08"], False, pad=0.10)
    F11a = hfit(CRUX + [RIGIL, HADAR], ROT["11a"], False, PHI_T, 60.0, fh=0.16)

    FR = dict(F01a=F01a, F01b=F01b, F03=F03, F04=F04, F05a=F05a, F05b=F05b, F06=F06, F06a=F06a, F07=F07,
              F08a=F08a, F08b=F08b, F09a=F09a, F09b=F09b, F09c=F09c, F11=F11, F11a=F11a, F11b=F11b,
              F12=F12, F13=F13)
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

    def term(key, fov, px1=60, px2=44, dx=0.0, dy=0.0, zh=None, one=False, disc=False, col=None, a=None):
        a0, orig, en, zh0, c, _ = TERMS[key]
        a = a if a is not None else a0
        if one:
            return [item(a, zh or orig, col or c, px1, fov, dx, dy, key, disc)]
        g = (px1 + px2) * 0.62 * fov / 1080.0
        return [item(a, orig, col or c, px1, fov, dx, dy + g / 2, key, disc),
                item(a, zh or zh0, "white", px2, fov, dx, dy - g / 2, key + "-zh", disc)]

    LB = {}
    f1 = F01b[2]
    LB["總覽"] = (term("夏威夷", f1, 52, 0, dx=0.0, dy=-6.0, one=True)
                + term("東加", f1, 52, 0, dx=0.0, dy=6.0, one=True)
                + term("阿努塔", f1, 52, 0, dx=0.0, dy=-9.0, one=True)
                + term("布吉斯曼達爾", f1, 52, 0, dx=0.0, dy=-11.0, one=True)
                + term("阿拉伯", f1, 52, 0, dx=0.0, dy=-6.0, one=True))
    f3 = F03[2]
    LB["大熊"] = (term("大熊", f3, 60, 44, dx=0.0, dy=22.0, disc=True)
                + term("北極星", f3, 44, 0, dx=0.0, dy=-3.6, one=True, disc=True)
                + [item([POLARIS], "約前 700：整個北斗整晚不落（歲差）", "white", 38, f3, 0.0, -9.0, "歲差", disc=True)])
    f5 = F05b[2]
    LB["夏威夷"] = (term("Hōkūleʻa", f5, 60, 44, dx=0.0, dy=-6.5, disc=True)
                  + term("北極星", f5, 44, 0, dy=-3.6, one=True, disc=True))
    f6 = F06[2]
    LB["圓環"] = (term("ʻUvea", f6, 60, 44, dx=0.0, dy=8.5, disc=True)
                + [item(RING, "Stellarium 推測：北冕座", "white", 36, f6, 0.0, -6.0, "北冕", disc=True)])
    f6a = F06a[2]
    seg1, seg2, ratio, miss = pointer_path(S)
    mid = seg2[len(seg2) // 2]
    LB["野鴨"] = (term("Toloa", f6a, 60, 44, dx=-11.0, dy=2.0, disc=True)
                + term("南天極", f6a, 44, 0, dx=0.0, dy=-3.2, one=True, disc=True)
                + [item(mid, "今天的找法：延長約 4.4 倍", "red", 36, f6a, -9.0, 0.0, "指南線", disc=True)])
    f8a, f8 = F08a[2], F08b[2]
    LB["斜屋"] = (term("Sapo Kepang", f8a, 60, 44, dx=0.0, dy=-10.0, zh="曼達爾：斜屋", disc=True)
                + [item(HOUSE, "布吉斯：瘸腿的房子", "white", 44, f8a, 0.0, -14.2, "布吉斯", disc=True)])
    LB["魟鯊"] = (term("Sapo Kepang", f8, 52, 40, dx=-2.0, dy=-9.0, zh="斜屋・南方", disc=True)
                + term("Lambaru", f8, 52, 40, dx=4.0, dy=7.0, zh="魟魚・11 月底", disc=True)
                + term("Mangiwang", f8, 52, 40, dx=-9.0, dy=-2.0, zh="鯊魚・12 月底", disc=True)
                + [item([G_SCO], "背鰭", "red", 38, f8, 3.0, 1.6, "背鰭", disc=True),
                   item([ARA_B], "頭", "red", 38, f8, 3.0, 0.0, "頭", disc=True),
                   item([TEL_A], "肚子", "red", 38, f8, -3.0, -1.6, "肚子", disc=True),
                   item([SIG_SGR], "尾", "red", 38, f8, -2.4, 1.6, "尾", disc=True)])
    f9a, f9b, f9c = F09a[2], F09b[2], F09c[2]
    npt = altaz_to_radec(0.0, 0.0, PHI_AR, L09)
    LB["阿拉伯-北"] = ([item([POLARIS], "北極星＝正北", "purple", 52, f9a, 0.0, -4.0, "al-Jāh", disc=True),
                     item([POLARIS], "al-Jāh", "white", 40, f9a, 0.0, -7.6, "al-Jāh-tr", disc=True),
                     item(npt, "北緯 20° 的地平線", "white", 38, f9a, 14.0, -3.0, "地平線", disc=True)])
    LB["阿拉伯-升起"] = ([item(rise_set(S[h][1], PHI_AR, L09)[0], nm, "purple", 44, f9b,
                             (-4.0 if i % 2 == 0 else 4.0), (3.4 if i % 2 == 0 else -3.4), "升" + nm, disc=True) for i, (h, nm) in enumerate(RISERS)]
                       + [item(rise_set(S[ARCTURUS][1], PHI_AR, L09)[0], "亮星升起的地方", "white", 40, f9b, -14.0, 16.0,
                               "升起說明", disc=True)])
    LB["月站"] = [item((0.0, 90.0), "28 月站（manāzil al-qamar）", "purple", 56, f9c, 0.0, 0.0, "月站", disc=True)]
    f11, f11a, f11b = F11[2], F11a[2], F11b[2]
    alt_pol = altaz(S[POLARIS][:2], T["1130"])[0]
    LB["台北-北"] = ([item([POLARIS], f"北極星 {alt_pol:.0f}°", "amber", 56, f11, 0.0, 4.0, "北極星高度", disc=True),
                    item([POLARIS], "＝台北的緯度", "white", 42, f11, 0.0, -4.0, "緯度", disc=True)])
    # 中文星名：十字架一＝γ Cru（Gacrux）、十字架二＝α Cru（Acrux）
    a_1, a_2 = altaz(S[GACRUX][:2], T["1130"])[0], altaz(S[ACRUX][:2], "2027/5/21 20:26")[0]
    LB["台北-南"] = ([item([GACRUX], f"十字架一 {a_1:.1f}°", "amber", 44, f11a, 7.0, 0.8, "十字架一", disc=True),
                    item([ACRUX], f"十字架二 {a_2:.1f}°", "amber", 44, f11a, 7.0, -1.2, "十字架二", disc=True),
                    item(altaz_to_radec(10.0, 200.0, PHI_T, LST_AT["1130"]), "高 10°（墾丁：十字架一 10.9°）",
                         "white", 36, f11a, 0.0, 2.2, "十度", disc=True)])
    a_arc = altaz(S[ARCTURUS][:2], T["11b"])[0]
    LB["台北-大角"] = ([item([ARCTURUS], f"大角星 {a_arc:.1f}°", "amber", 56, f11b, 14.0, 3.5, "大角高度", disc=True),
                     item((LST_AT["11b"] % 360, PHI_T), "天頂", "white", 44, f11b, -8.0, 1.0, "天頂", disc=True),
                     item([ARCTURUS], "離頭頂 6°", "white", 44, f11b, 14.0, -4.0, "6度", disc=True)])
    f12 = F12[2]
    LB["滿月"] = (term("心宿二", f12, 52, 0, dx=7.0, dy=2.5, one=True)
                + term("月亮", f12, 52, 0, dx=5.0, dy=-2.5, one=True)
                + term("Lambaru", f12, 52, 40, dx=-10.0, dy=8.0, zh="魟魚"))
    f13 = F13[2]
    LB["下集"] = [item((x_to_ra(-8.0), 30.0), "下集：阿拉伯月站", "purple", 60, f13, 0.0, 0.0, "下集")]
    label_sets = [(v, k2) for k2, v in LB.items()]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    LG_MAIN = LG["夏"] + LG["東"] + LG["努"] + LG["曼"]
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), ([POLARIS, ARCTURUS, ANTARES, ACRUX], "單星光暈", "ring"),
             ([POLARIS], "阿拉伯-北極星", "ring"), (ST_MARK, "月站標記", "ring")]
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
    OVERVIEW = ["夏", "東", "努", "曼", "阿極"]

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=11, north=True, frames=[F01a, F01b], layers=OVERVIEW,
             labels=[], labels_end=ls("總覽"),
             vo="上週，認錯一個十字，南方就偏掉二十度以上。今晚是航海季的總集篇：同一片星空，航海的人看見——一張不用羅盤的地圖。",
             card="一張不用羅盤的地圖",
             note=f"長圖一格看到北極星（北盤）到南十字（南盤）：Z fov {F01a[2]:.0f}→{F01b[2]:.0f} 微推；航海星路總覽五層依序淡入"
                  "（夏威夷綠：魚鉤＋脊椎骨；東加琥珀：野鴨、ʻUvea 的圓環、南門二＋馬腹一；阿努塔藍：星路上的魚＝人馬；"
                  "布吉斯／曼達爾紅：斜屋、魟魚、鯊魚；阿拉伯紫：北極星圈）；迄格開「總覽」標籤；開場字卡"),
        dict(code="02", kind="Z", sec=19, north=True, frames=[F01b], layers=OVERVIEW, labels=[],
             overlay="C-X06-01_時間軸", overlay_layers=["莎湖層"],
             vo="常有人說，人類不用羅盤、靠星星航海，已經一萬年。我們查了：這句話證明不了。人類至少五萬年前就渡海到了澳洲，"
                "可是沿途的島，多半一座看得見下一座；那時有沒有用星星，沒有人知道。",
             card="「一萬年」證明不了",
             note="長圖定格；疊 C-X06-01 莎湖層（時間軸＋五萬年前：巽他→莎湖，島與島看得見、問號）"),
        dict(code="03", kind="R", sec=14, north=True, horizon=[PHI_GR], frames=[F03], layers=["熊"],
             labels=ls("大熊"),
             vo="現存最早寫下來的紀錄，在兩千七百年前的《奧德賽》：女神交代奧德修斯，讓大熊座一直留在左手邊。"
                "大熊在北邊，留在左手邊，就是往東開。",
             card="大熊在左手邊＝往東",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤，再 Match & Move 到這格）：希臘 38°N 面北（{ROT['03']:+.1f}°，"
                  "山＝北方地平線；北斗在北極星上方）；托勒密大熊全形（白）；角落小字「約前 700：整個北斗整晚不落（歲差）」；"
                  "船頭箭頭指東、左手邊標「北」由美宣在 Canva 畫（原生箭頭）"),
        dict(code="03b", kind="R", sec=11, north=True, horizon=[PHI_GR], frames=[F03], layers=["熊"], labels=[],
             overlay="C-X06-01_時間軸", overlay_layers=["莎湖層", "奧德賽層", "萍洲層"],
             vo="中國書裡第一次寫到船上用指南針，是九百年前，而且是陰天才用：「夜則觀星，晝則觀日，陰晦觀指南針。」",
             card="夜則觀星，晝則觀日",
             note="北盤定格；疊 C-X06-01（莎湖層→奧德賽層→萍洲層：《萍洲可談》三句，「陰晦觀指南針」最後亮）"),
        dict(code="04", kind="R", sec=18, north=True, horizon=[PHI_GR], frames=[F03, F04], layers=["熊"], labels=[],
             overlay="C-X06-01_時間軸", overlay_layers=["前情層", "南島層"],
             vo="而在沒有留下文字的太平洋，一般認為，大約四千年前，南島語族的祖先從台灣南下；將近三千年前，他們的船已經越過看不見陸地的大海，"
                "到了東加；大約八百到一千年前，才抵達夏威夷。",
             card="從台灣出發",
             note=f"北盤慢轉（{ROT['03']:+.1f}°→{ROT['04']:+.1f}°＝時間在走）；迄格疊 C-X06-01（前情層＝前三層合成 → 南島層：時間軸補上"
                  "四千年前／約 2,900 年前／800–1,000 年前，下半是點狀示意地圖：台灣→菲律賓→蘇拉威西→俾斯麥→萬那杜→斐濟→東加→夏威夷，"
                  "看不見陸地的航段畫虛線）；地圖是依經緯度自繪的點與箭頭，不臨摹已出版遷徙圖，美宣可換成自繪地圖"),
        dict(code="05", kind="R", sec=27, north=True, horizon=[PHI_HI], frames=[F05a, F05b], layers=["暈"],
             labels=[], labels_end=ls("夏威夷"), overlay="C-A09-01_星羅盤", overlay_layers=["羅盤層"], overlay_at="start",
             vo="這幾個月，我們追著這些船走了一圈。夏威夷：一九七六年，密克羅尼西亞的航海師 Mau Piailug，帶著獨木舟 Hōkūleʻa 不靠儀器開到大溪地。"
                "後來夏威夷人把地平線切成三十二間房子：目的地在哪一間，就對準從那間升起或落下的星；大角星掛在正頭頂，就到了北緯十九度的夏威夷。",
             card="夏威夷：星羅盤",
             note=f"北盤夏威夷 19.6°N 面北（山＝北方地平線）：{ROT['05a']:+.1f}° 大角在東方 → {ROT['05b']:+.1f}° 大角上中天＝天頂；"
                  "起格後疊 A-09 的 C-A09-01 星羅盤（羅盤層，沿用 A-09 檔案，已複製到本集 _概念圖/）；「大角星」起收掉星羅盤、"
                  "Match & Move 到迄格，大角光暈＋標籤 Hōkūleʻa／大角星；Hōkūleʻa 獨木舟照片美宣另尋授權圖"),
        dict(code="06", kind="R", sec=10, north=True, frames=[F05b, F06], layers=["環"],
             labels=ls("圓環"), labels_start=ls("夏威夷"),
             vo="東加：星名本身就是指令——一圈星叫「ʻUvea 的圓環」，要等它像頭環一樣戴在 ʻUvea 島的上空，才拿來駕船。",
             card="東加：星名就是指令",
             note="北盤滑到北冕（大角東邊 20°）：ʻUvea 的圓環（琥珀，tongan 010）＋小字「Stellarium 推測：北冕座」；山離開畫面（不放地平線）"),
        dict(code="06a", kind="R", sec=9, north=False, cut=True, frames=[F06a], layers=["鴨", "指南"],
             labels=ls("野鴨"),
             vo="南十字在東加是一隻野鴨 Toloa；今天的人把它頭尾延長四倍半，就到南天極附近。",
             card="野鴨 Toloa",
             note=f"【硬切】北盤→南盤（旁白換主角「南十字」）：南盤 {ROT['06a']:+.1f}°（南十字上中天，頭在上）；野鴨（琥珀，tongan 001）"
                  f"＋指南線（紅，γ→α 延長 {ratio - 1:.1f} 倍，在南天極旁 {miss:.1f}° 通過）；指南線旁小字「今天的找法」"),
        dict(code="07", kind="R", sec=12, north=False, frames=[F06a, F07], layers=["鴨"], labels=[], labels_start=ls("野鴨"),
             overlay="C-X06-05_星路", overlay_layers=["海面層", "星路層"],
             vo="所羅門群島的阿努塔：鄰島 Tikopia 的酋長說，往阿努塔要靠九顆星——一顆貼著海面時，對準船頭；升高了，就換下一顆。",
             card="往阿努塔：九顆星的路",
             note=f"南盤轉向天蠍（{ROT['06a']:+.1f}°→{ROT['08']:+.1f}°，夜在走）；迄格疊 C-X06-05 星路（海面層→星路層；Tikopia→阿努塔 134 km，"
                  "Firth 1954 沒記九顆星的名字，圖上不指認）。逐字稿原寫沿用 C-A11-03，那張是阿努塔往 Tikopia、方向相反，改用本集新圖"),
        dict(code="08", kind="R", sec=20, north=False, frames=[F08a, F08b], layers=["屋", "魟"] + SHARK_ALL,
             labels_start=ls("斜屋"), labels=ls("魟鯊"),
             vo="印尼蘇拉威西的布吉斯人和曼達爾人是鄰居，星座也很像：南十字是一間房子，指著南方，五月傍晚就看得到。"
                "天蠍的魟魚十一月底在清晨升起，十二月底換一路連到人馬座的鯊魚——西北季風就要來了。",
             card="布吉斯、曼達爾：季風的星",
             note=f"南盤 {ROT['08']:+.1f}°（不綁時刻，選直式最省的角度）：起格斜屋（琥珀，mandar 001）兩行標籤「曼達爾：斜屋／布吉斯：瘸腿的房子」"
                  f"→ 拉遠 fov {F08a[2]:.0f}→{F08b[2]:.0f}：魟魚（紫，mandar 003）→ 鯊魚四段依旁白順序亮（背鰭→頭（天壇）→肚子→尾（人馬），紅）；不畫寡婦"),
        dict(code="08b", kind="R", sec=9, north=False, frames=[F08b], layers=["屋", "魟"] + SHARK_ALL,
             labels=ls("魟鯊"),
             vo="可是這份研究訪問的，都是七十歲以上的老漁夫；年輕一輩，多半只看羅盤和海圖。",
             card="七十歲以上的老漁夫",
             note="南盤定格；連線各層在 Canva 慢慢調到透明度 30%，只留星點（標籤一起淡）"),
        dict(code="09", kind="R", sec=18, north=True, cut=True, frames=[F09a, F09b], layers=["阿地"],
             labels_start=ls("阿拉伯-北"), labels=ls("阿拉伯-北"), labels_end=ls("阿拉伯-升起"),
             overlay="C-X06-02_兩個三十二", overlay_layers=["夏威夷層", "阿拉伯層"],
             vo="再往西，到印度洋。十五世紀，阿拉伯航海家 Ibn Mājid 的船上已經有了磁針，可是羅盤的三十二個方位，還是用星星命名："
                "大多是某顆亮星升起或落下的地方——剛好跟夏威夷一樣，也是三十二。",
             card="阿拉伯：三十二個星位",
             note=f"【硬切】南盤→北盤（旁白換地方「再往西」）：北盤 {ROT['09']:+.1f}°，北緯 20° 地平線（白線，示意，不指定港口）："
                  "起格北極星＝正北（紫短線＋標籤 al-Jāh）→ 滑到東方地平線，五顆亮星的升起點（紫圈：五車二、織女、昴宿、大角、牛郎；"
                  "西方同名落下點也畫了）依序亮；「也是三十二」起定格疊 C-X06-02（夏威夷層→阿拉伯層）"),
        dict(code="09b", kind="R", sec=4, north=True, frames=[F09b, F09c], layers=["阿地", "站"],
             labels_start=ls("阿拉伯-升起"), labels=ls("月站"),
             vo="他還要記熟月亮每晚住的那二十八站。",
             card="28 月站",
             note=f"北盤拉遠到整圈黃道（fov {F09c[2]:.0f}，盤心置中）：28 月站標記（細圈，A-32 的本土序，每站最亮的星；空地 al-Baldah 取區域中心）淡入"),
        dict(code="10", kind="R", sec=15, north=True, frames=[F09c], layers=["阿地", "站"], labels=[],
             overlay="C-X06-03_星星航海的三件事",
             vo="不管在哪片海，星星航海術都在問三件事：星從哪裡升起、落下，告訴你方向；北極星有多高、哪顆星過頭頂，告訴你緯度；"
                "星什麼時候出現，告訴你季節和季風。",
             card="方向・緯度・季節",
             note="北盤定格；疊 9:16 圖卡 C-X06-03（可存圖），停 12 秒以上"),
        dict(code="11", kind="R", sec=8, north=True, horizon=[PHI_T], frames=[F11], layers=["極高"],
             labels=ls("台北-北"),
             vo="今晚在台北，自己試試看：往正北看，北極星整晚都在二十五度上下，剛好是台北的緯度。",
             card="北極星高度＝緯度",
             note=f"北盤台北 5/21 20:30 面北（{ROT['11']:+.1f}°，與 09／10 同角度，Match & Move 推近；山＝台北北方地平線）："
                  f"北極星高度弧（琥珀，北點→北極星）＋「北極星 {alt_pol:.0f}°＝台北的緯度」"),
        dict(code="11a", kind="R", sec=9, north=False, cut=True, horizon=[PHI_T], frames=[F11a], layers=["鴨", "十度"],
             labels=ls("台北-南"),
             vo="八點半，南十字直立在正南方，可是在台北最高不到八度；要到墾丁的海邊，才有十度左右。",
             card="南十字：不到 8°",
             note=f"【硬切】北盤→南盤（轉身面南）：台北 20:30 面南（{ROT['11a']:+.1f}°；山＝南方地平線）南十字直立（十字架一 {a_1:.1f}°、"
                  f"十字架二 {a_2:.1f}°（20:26 上中天））；地平線上 10° 虛線＋小字「墾丁：十字架一 10.9°」"),
        dict(code="11b", kind="R", sec=10, north=True, cut=True, horizon=[PHI_T], frames=[F11b], layers=["天頂", "暈"],
             labels=ls("台北-大角"),
             vo="十點多，大角星爬到最高，離頭頂只差六度：它正好經過北緯十九度、夏威夷的正上方，台北在它北邊六度。",
             card="大角星：離頭頂 6°",
             note=f"【硬切】南盤→北盤（再轉回北方、抬頭）：台北 22:14 面北（{ROT['11b']:+.1f}°）：大角上中天 {a_arc:.1f}°；"
                  "天頂十字＋半徑 6° 虛線圈＋天頂→大角（琥珀）"),
        dict(code="12", kind="Z", sec=12, north=True, frames=[F12], layers=["魟", "月", "暈"],
             labels=ls("滿月"), overlay="C-X06-04_今晚自己導航",
             vo="九點以後，東南方剛過滿月的月亮，就停在心宿二旁邊。月光太亮，曼達爾漁夫的那條魟魚，今晚只認得出最亮的心宿二。",
             card="滿月旁的心宿二",
             note=f"【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）；長圖天蠍＋月亮（台北 21:30 站心，離心宿二 "
                  f"{sep(MOON12[:2], S[ANTARES][:2]):.1f}°；圖示放大約 3 倍＝示意）；魟魚連線（紫）先亮再在 Canva 淡掉，只留心宿二光暈；"
                  "迄格疊 9:16 圖卡 C-X06-04（5/21 對時，可存圖）"),
        dict(code="13", kind="Z", sec=8, north=True, frames=[F12, F13], layers=["站", "暈"], labels=ls("下集"),
             vo="下週五，跟著 Ibn Mājid 回到月亮的路上：阿拉伯人替月亮蓋的二十八間旅店。",
             card="下集見｜阿拉伯月站：月亮每晚的下榻處",
             note=f"長圖拉遠 fov {F12[2]:.0f}→{F13[2]:.0f} 到黃道帶，28 月站標記（細圈）淡入；端卡「下集見｜阿拉伯月站：月亮每晚的下榻處」＋追蹤 CTA"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"]
        print(f"  {sh['code']:>3}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u/tot_s:.2f} 字/秒")
    m.check_shots(shots)
    print("  判斷後接受的 ⚠：" + WARN_OK)
    for sh in shots:
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 170.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° ≥ 170°")
    for sh in shots:
        if sh["kind"] == "R" and abs(sh["frames"][-1][3]) >= 170:
            print(f"  ⚠ {sh['code']} 迄格旋轉 {sh['frames'][-1][3]:+.1f}°（若接換組，歸位會被拆頁）")

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
    print(f"  指南線：γ→α 延長 {ratio:.2f} 倍（從 α 往外 {ratio - 1:.2f} 倍），離南天極 {miss:.2f}°")
    for nm, when in (("20:30", T["1130"]), ("22:14", T["11b"])):
        print(f"  台北 {nm}：北極星 {altaz(S[POLARIS][:2], when)}、大角 {altaz(S[ARCTURUS][:2], when)}、"
              f"十字架一 γ {altaz(S[GACRUX][:2], when)}、十字架二 α {altaz(S[ACRUX][:2], when)}")
    for when in ("2027/5/21 21:00", "2027/5/21 22:00"):
        mr = moon_radec(when)
        print(f"  月亮 {when}：高 {mr[2]:.1f}° 方位 {mr[3]:.0f}°、相位 {mr[4]:.1f}%、離心宿二 {sep(mr[:2], S[ANTARES][:2]):.1f}°")
    print(f"  大角赤緯 {S[ARCTURUS][1]:+.2f}（J2000）；台北天頂距 {PHI_T - S[ARCTURUS][1]:.1f}°（J2000 近似）")
    for h, nm in RISERS:
        print(f"  {nm} 赤緯 {S[h][1]:+.1f} → 北緯 20° 升起方位 {math.degrees(math.acos(math.sin(math.radians(S[h][1])) / math.cos(math.radians(PHI_AR)))):.1f}°")
    print(f"  y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}；x：心宿二 {x_of(S[ANTARES][0]):+.1f}、大角 {x_of(S[ARCTURUS][0]):+.1f}、"
          f"北冕 {x_of(S[ALPHECCA][0]):+.1f}、南十字 {x_of(S[ACRUX][0]):+.1f}")

    terms = {}
    for key, (a, orig, en, zh, col, note) in TERMS.items():
        terms[key] = dict(hips=a if isinstance(a, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                          顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="bola képpang", 中譯="瘸腿的房子（布吉斯，A-26）", 英文="Incomplete house", 顏色="amber")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": ROT, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV = LG_MAIN + LG["熊"]
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

    # 沿用 A-09 的星羅盤：複製到本集 _概念圖/（gen_canva_pages 只找本集資料夾）
    cd = os.path.join(ROOT, "_概念圖")
    os.makedirs(cd, exist_ok=True)
    src = os.path.join(BASE, "05_素材/A-09_夏威夷星線/_概念圖")
    for fn in ("C-A09-01_星羅盤_羅盤層_透明.png", "C-A09-01_星羅盤_預覽_黑底.png"):
        shutil.copy2(os.path.join(src, fn), os.path.join(cd, fn))
    print("\n完成 →", OUT)


def x_to_ra(x):
    return (LST0 - x) % 360.0


if __name__ == "__main__":
    build()
