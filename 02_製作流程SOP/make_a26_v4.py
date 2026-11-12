# -*- coding: utf-8 -*-
"""A-26 布吉斯：帆船民族的星羅盤｜大畫布 v4.6（南盤開場＋北盤＋長圖，南島雙聯集・上）

論點：布吉斯船員的天空是一座羅盤（Ammarell 1999 的說法）：南方是寡婦（南門二＋馬腹一）、瘸腿的房子
（南十字）、山羊（煤袋）；北方看不到北極星，指北的是北斗＝船星；天上還住著鄰居（曼達爾的寡婦、
巴瑤人的記號）；東方的星＝牛郎星；天蠍是魟魚＋鯊魚。上了岸：犁（獵戶）、三的記號（腰帶）、雞（老人星—
天狼—南河三）＝阿努塔的 Manu。

來源：Stellarium bugis（Doina Bucur 2021；12 組連線）；Ôhashi & Orchiston 2021（Ammarell 1999 A–M、
Pelras 1987 1–9）；Rasyid et al. 2021；跨文化 Stellarium tupi（上集美洲鴕）、mandar（下集漁網）。
逐字稿：04_腳本庫/A-26-布吉斯帆船民族的星羅盤-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線：照 Stellarium bugis 001–010（船用 006：北斗七星＋ψ UMa＋小熊 β、γ，10 顆）。自訂層：
  深空天體（煤袋暗區虛框、大小麥哲倫雲；Stellarium 只給大麥哲倫雲名，小麥哲倫雲自己補）、
  往 Bima 的方位線（Balobaloang 7/31 18:28，方位 184.5°，地平高度 0–40°）、
  望加錫東方地平線（牛郎星升起那一刻，方位 0–180° 半圈）、月亮木星火星（台北 3/19 19:30，J2000 astrometric、站心）。
  上集回顧：圖皮 Guirá Nhandu 美洲鴕（Stellarium tupi 001，白，01 鏡淡出）；
  下集預告：曼達爾 Bittoéng Panjala 漁網（Stellarium mandar 004，白虛線，16 鏡）。
  標籤一律用拉丁字母 é（Stellarium 的 Bintoѐng 是西里爾 е＋組合抑音符，不用）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 190 → 走廊 x＝0 在 RA 190：往南正好經過南十字（RA 184–194），往北正好經過北斗的斗身（天權 RA 184 x＋6）。
             長圖的切口（x＝±180）在 RA 10（雙魚—仙女南邊）：本集上長圖的 獵戶 x＋101…＋112、天狼＋89、老人星＋94、
             南河三＋75、月亮木星火星（台北 3/19）＋40…＋60、天蠍 −49…−77、天壇 α −73、牛郎星 −108，都離切口很遠。
  D_s = 66、D_r = 70 → 決定因素是 12、14b 鏡的「雞」：老人星 −52.7 到南河三 +5.2 高 58°，要整隻放進一格、
             老人星還要高過山的剪影（離畫面下緣 ≥ 16%）：fov 46、cy −25 ⇒ |cy|＋fov·8/9＝65.9 ≤ D_s。
             D_s 62 時老人星只離下緣 12%，會被山擋住（試過）。
             代價：k＝2.865，盤只收到 |dec| ≥ D_fill；南十字、南門二、北斗都不在盤本體（|dec|<70），
             盤上的標籤一律 disc=True（同 A-24 做法），換組格都在盤心 fov ≤ 50（盤緣圈內逐點重合）。
  D_fill = 28 → R_fill＝177.6（盤寬 ÷ 畫布寬＝0.9867；Canva 別設成同寬）；|x_t|＋R_fill ≤ 180 ✓。
             南盤收到 dec −28：天蠍尾、天壇 α（−49.9）都在盤內；天蠍頭（−20…−26）不在，01 鏡美洲鴕只露出尾巴那段。
             北盤收到 dec +28：08 鏡望加錫北方地平線方位 ±62° 以內都有星；14 鏡台北東北方地平線（方位 45°、dec 40）有星，
             更靠東的地平線附近是空的（被山擋住，鏡頭牆看過）。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 rot＝lst_obs−lst（順時針＝時間前進）；北盤 rot＝−((lst_obs＋180−lst) mod 360)（逆時針＝時間前進），
  每段 M&M 旋轉 < 180°（v4.6 第四節）。

鏡頭路線
  01 R 南盤（無地平線）順時針慢轉：美洲鴕（上集）淡出 → 南十字—半人馬 → 02、03 定格疊 C-A26-01、02
  → 04 R 同角度推近寡婦 → 05 R 轉到 Balobaloang 7/31 18:28 面南（山升到南緯 6.6°）＋Bima 方位線 → 06 定格 C-A26-03
  → 07 R 同角度滑到南十字＋煤袋
  → 08【硬切】北盤：望加錫面北（山＝南緯 5.1° 北方地平線，北極星在山下）→ 09 R 推近斗口
  → 09b【硬切】南盤：望加錫面南、大小麥哲倫雲上中天 → 定格疊 C-A26-04
  → 10【硬切】長圖：牛郎星＋望加錫東方地平線 → 11 S 往右（西）滑到天蠍：魟魚＋鯊魚 → 定格 C-A26-05 圖卡
  → 12【硬切】長圖：獵戶（犁、三的記號）→ 往左下滑到雞 → 13 定格 C-A26-06
  → 14【換北盤】（自動插回中心／上移／長圖轉北盤）台北 3/19 19:30 面北 → 14b【換長圖】（自動插歸位／北盤轉長圖／下移）
     雞 → 月亮木星火星 → 定格 C-A26-07 圖卡
  → 15【換南盤】（自動插回中心／下移／長圖轉南盤）墾丁 3/20 00:40 → 02:30 面南
  → 16【硬切】北盤：望加錫面北推近北斗，船淡出、曼達爾漁網虛線淡入＋端卡

  逐字稿的 09、14 鏡各跨兩個圖層組（北盤→南盤、北盤→長圖），一鏡只能用一組 → 拆成 09／09b、14／14b，
  旁白照原文切開；秒數 18＝7＋11、18＝6＋12（總長不變 226 秒）。

硬切（判斷後接受）：07→08「往北呢？」、09→09b「轉回南邊」、09b→10「往東」、11→12「上了岸」、15→16「下週五」
  ——都是旁白明講轉頭／換地方；南盤⇄北盤沒有共用的畫面，滑不過去。
check_shots 的 ⚠（判斷後接受；跑完逐條看過）
  01–09b、15、16 R「起／迄格畫面含長圖側扇區」：這些鏡頭都不直接切回大畫布——
  南盤⇄北盤之間是旁白明講轉頭的【硬切】；回長圖時由 gen_canva_pages 插「歸位」（盤轉回 0°、盤心 fov ≤ 50，
  盤緣圈內逐點重合）再換組；15 鏡從長圖進來也是自動插「回中心／下移／長圖轉南盤」。14 ✓ 無 ⚠。
  hfit 的「最高的星超出上緣安全區」已靠調 fov／fh 消掉（最後一輪 0 則）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-26"
OUT = os.path.join(BASE, "05_素材/A-26_布吉斯/_v4大畫布")
LST0 = 190.0
D_S, D_R, D_FILL = 66.0, 70.0, 28.0

BALO = (-6.5935, 118.8615)        # Balobaloang Lompo（OpenStreetMap）
BIMA = (-8.4480, 118.7126)        # Pelabuhan Bima
MKS = (-5.14, 119.42)             # 望加錫
TPE = (25.0330, 121.5654)
KTG = (21.95, 120.80)             # 墾丁
BIMA_AZ = 184.5


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when, refr=True):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure = 1010 if refr else 0
    o.temp = 15
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(lat, lon, tz, when):
    return math.degrees(_obs(lat, lon, tz, when).sidereal_time())


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return round((lst_obs - LST0 + 180.0) % 360.0 - 180.0, 2)


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return round(r + 360.0 if r <= -180.0 else r, 2)


T = {
    "05": ("Balobaloang 7/31 18:28", BALO, "2027/7/31 18:28"),
    "08": ("望加錫 5/15 20:00", MKS, "2027/5/15 20:00"),
    "09b": ("望加錫 2/10 20:00", MKS, "2027/2/10 20:00"),
    "14": ("台北 3/19 19:30", TPE, "2027/3/19 19:30"),
    "15a": ("墾丁 3/20 00:40", KTG, "2027/3/20 00:40"),
    "15b": ("墾丁 3/20 02:30", KTG, "2027/3/20 02:30"),
}
LST_AT = {k: lst_at(*v[1], 8, v[2]) for k, v in T.items()}
ROT = {"05": rot_s(LST_AT["05"]), "08": rot_n(LST_AT["08"]), "09b": rot_s(LST_AT["09b"]),
       "14": rot_n(LST_AT["14"]), "15a": rot_s(LST_AT["15a"]), "15b": rot_s(LST_AT["15b"])}


def radec_of(lat, lon, tz, when, az, alt):
    """地平座標 → J2000 赤道座標（與星表同框；不加折射，畫幾何線用）"""
    import ephem
    o = _obs(lat, lon, tz, when, refr=False)
    o.epoch = ephem.J2000
    ra, dec = o.radec_of(str(az), str(alt))
    return math.degrees(ra), math.degrees(dec)


def bodies():
    """月亮、木星、火星：台北 3/19 19:30，J2000 astrometric（與星表同框）、站心"""
    import ephem
    o = _obs(*TPE, 8, "2027/3/19 19:30")
    out = {}
    for nm, b in (("月亮", ephem.Moon()), ("木星", ephem.Jupiter()), ("火星", ephem.Mars())):
        b.compute(o)
        # a_ra 是地心座標（月亮差了視差 ~0.5°，月—木會變 1.5°）→ 用站心視位置 ra/dec 歲差回 J2000
        eq = ephem.Equatorial(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=ephem.J2000)
        out[nm] = dict(ra=math.degrees(eq.ra), dec=math.degrees(eq.dec),
                       alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                       phase=round(getattr(b, "moon_phase", 0) * 100, 1) if nm == "月亮" else None,
                       mag=round(b.mag, 1))
    return out


PL = bodies()


def altair_rise():
    """望加錫：牛郎星升起那一刻的 LST 與方位（幾何、無折射；與 PyEphem 含折射 81.1° 差 < 0.2°）"""
    phi, dec, ra = math.radians(MKS[0]), math.radians(8.868), 297.695
    H0 = math.degrees(math.acos(-math.tan(phi) * math.tan(dec)))
    az = math.degrees(math.acos(math.sin(dec) / math.cos(phi)))
    return (ra - H0) % 360.0, az


LST_ALT, AZ_ALT = altair_rise()


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ACRUX, MIMOSA, GACRUX, IMAI, MU_CRU = 60718, 62434, 61084, 59747, 63003
RIGIL, HADAR = 71683, 68702
DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID = 54061, 53910, 58001, 59774, 62956, 65378, 67301
PSI_UMA, KOCHAB, PHERKAD, POLARIS = 54539, 72607, 75097, 11767
ALTAIR, ANTARES, SHAULA, ARA_A = 97649, 80763, 85927, 85792
BELLATRIX, MINTAKA, ALNILAM, ALNITAK, SAIPH, RIGEL, BETEL = 25336, 25930, 26311, 26727, 27366, 24436, 27989
CANOPUS, SIRIUS, PROCYON, ALDEBARAN, REGULUS = 30438, 32349, 37279, 21421, 49669
BELT = [MINTAKA, ALNILAM, ALNITAK]
CRUX = [ACRUX, MIMOSA, GACRUX, IMAI, MU_CRU]
WIDOW = [RIGIL, HADAR]
DIPPER = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]

LMC = (80.894, -69.756)
SMC = (13.187, -72.829)
COALSACK = (192.5, -62.8)
SCP = (0.0, -89.999)


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium bugis／tupi／mandar index.json）
# ══════════════════════════════════════════════════════════════════
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_sc(cu):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"].split()[-1]] = [s for s in segs if len(set(s)) >= 2]
    return out


BG = load_sc("bugis")
SEG_HOUSE, SEG_SHARK, SEG_RAY, SEG_MWID = BG["001"], BG["002"], BG["003"], BG["004"]
SEG_SHIP, SEG_THREE, SEG_PLOUGH, SEG_WIDOW, SEG_CHICK = BG["006"], BG["007"], BG["008"], BG["009"], BG["010"]
SEG_STALK, SEG_PUSH = BG["011"], BG["012"]
SEG_RHEA = load_sc("tupi")["001"]                     # 上集：Guirá Nhandu 美洲鴕
SEG_NET = load_sc("mandar")["004"]                    # 下集：Bittoéng Panjala 漁網
assert sorted({h for s in SEG_SHIP for h in s}) == sorted(DIPPER + [PSI_UMA, KOCHAB, PHERKAD])
assert BETEL not in {h for s in SEG_PLOUGH for h in s}
assert sorted({h for s in SEG_HOUSE for h in s}) == sorted(CRUX)

LG_WIDOW = [(SEG_WIDOW, "amber", 1.2)]
LG_HOUSE = [(SEG_HOUSE, "green", 1.0)]
LG_SHIP = [(SEG_SHIP, "blue", 1.0)]
LG_MWID = [(SEG_MWID, "purple", 1.6)]
LG_RAY = [(SEG_RAY, "red", 1.0)]
LG_SHARK = [(SEG_SHARK, "red", 0.6)]                  # 形狀不確定（Stellarium 自註）→ 細線
LG_PLOUGH = [(SEG_PLOUGH, "green", 1.0)]
LG_THREE = [(SEG_THREE, "amber", 1.4)]
LG_CHICK = [(SEG_CHICK, "amber", 1.0)]
LG_OTHER = [(SEG_STALK, "green", 0.8), (SEG_PUSH, "green", 0.8)]   # 薏苡的莖、推犁（片中不用，只進 L4）
LG_RHEA = [(SEG_RHEA, "#E8ECF5", 0.8)]
LG_NET = [(SEG_NET, "#E8ECF5", 0.9)]
LG_ALL = (LG_WIDOW + LG_HOUSE + LG_SHIP + LG_MWID + LG_RAY + LG_SHARK + LG_PLOUGH + LG_THREE
          + LG_CHICK + LG_OTHER)
LINE_SETS = [(LG_WIDOW, "連線-寡婦"), (LG_HOUSE, "連線-瘸腿的房子"), (LG_SHIP, "連線-船星"),
             (LG_MWID, "連線-曼達爾的寡婦"), (LG_RAY, "連線-魟魚"), (LG_SHARK, "連線-鯊魚"),
             (LG_PLOUGH, "連線-犁"), (LG_THREE, "連線-三的記號"), (LG_CHICK, "連線-雞"),
             (LG_RHEA, "連線-美洲鴕（圖皮，上集）"), (LG_NET, "連線-漁網（曼達爾，下集）")]
LINES_KEY = {"L4": "星座連線", "寡": "連線-寡婦", "房": "連線-瘸腿的房子", "船": "連線-船星",
             "曼": "連線-曼達爾的寡婦", "魟": "連線-魟魚", "鯊": "連線-鯊魚", "犁": "連線-犁",
             "三": "連線-三的記號", "雞": "連線-雞", "鴕": "連線-美洲鴕（圖皮，上集）",
             "網": "連線-漁網（曼達爾，下集）",
             "深空": "深空天體", "Bima": "往Bima的方位線", "東": "望加錫東方地平線（牛郎星升起時）",
             "行": "月亮木星火星-3月19日", "暈": "單星光暈"}
LINE_GROUPS = {"L4": LG_ALL, "寡": LG_WIDOW, "房": LG_HOUSE, "船": LG_SHIP, "曼": LG_MWID,
               "魟": LG_RAY, "鯊": LG_SHARK, "犁": LG_PLOUGH, "三": LG_THREE, "雞": LG_CHICK,
               "鴕": LG_RHEA, "網": LG_NET, "深空": [], "Bima": [], "東": [], "行": [], "暈": []}

MAINS = sorted({h for g in LG_ALL for s in g[0] for h in s if g[0] not in (SEG_STALK, SEG_PUSH)}
               | {ALTAIR, BETEL, ALDEBARAN, POLARIS})


def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    v = [sum(vec(*S[h][:2])[i] for h in hs) for i in range(3)]
    return radec(v)


def stars_of(segs):
    return sorted({h for s in segs for h in s})


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（大畫布＋南北盤同步出）
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


BIMA_LINE = [radec_of(*BALO, 8, "2027/7/31 18:28", BIMA_AZ, a) for a in np.linspace(0, 40, 41)]
BIMA_LBL = radec_of(*BALO, 8, "2027/7/31 18:28", BIMA_AZ, 3.0)
EAST_LINE = []
for A in np.linspace(5, 175, 171):                     # 望加錫東方半圈地平線（牛郎星升起那一刻）
    p, a = math.radians(MKS[0]), math.radians(A)
    dec = math.asin(math.cos(p) * math.cos(a))
    H = math.atan2(-math.sin(a) / math.cos(dec), -math.sin(dec) * math.sin(p) / (math.cos(dec) * math.cos(p)))
    EAST_LINE.append(((LST_ALT - math.degrees(H)) % 360.0, math.degrees(dec)))
EAST_PT = ((LST_ALT + 90.0) % 360.0, 0.0)             # 正東（方位 90°、高度 0）


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs, disc):
        for (ra0, dec0, a, b, pa) in [(*LMC, 5.4, 4.6, 170.0), (*SMC, 2.65, 1.55, 45.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.15), (0.42, 0.24), (0.2, 0.36)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        s.polylines(runs(ellipse(*COALSACK, 3.4, 2.5, 30.0)), stroke=mw, w=0.12, opacity=0.55,
                    dash="0.6,0.5")

    def bima(s, pos, runs, disc):
        s.polylines(runs(BIMA_LINE), stroke=COLORS["amber"], w=0.22, opacity=0.9, dash="1.2,0.8")

    def east(s, pos, runs, disc):
        s.polylines(runs(EAST_LINE), stroke=COLORS["green"], w=0.20, opacity=0.85, dash="1.0,0.7")
        for p in pos(*EAST_PT):
            s.circle(p[0], p[1], 0.55, fill=COLORS["green"], opacity=0.95)

    def planets(s, pos, runs, disc):
        for nm in ("月亮", "木星", "火星"):
            col, r = {"月": ("#FFF6D8", 1.15), "木": ("#FFFFFF", 0.62), "火": (COLORS["red"], 0.48)}[nm[0]]
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.6, fill=col, opacity=0.14)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    return [("深空天體", deep), ("往Bima的方位線", bima), ("望加錫東方地平線（牛郎星升起時）", east),
            ("月亮木星火星-3月19日", planets)]


def write_custom(m, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all, None)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n),
                   lambda pts, n=north: m._runs_disc(pts, n), north)
                m._write_disc(s, north, name)


def disc_xy(m, ra, dec, rot, north):
    """天體在「轉 rot 之後的盤」上的位置（畫面方向的畫布單位，盤心＝(0, ±y_pole)）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；外文照母音組算，é 算母音）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyáéíóúèàâêîôû]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (WIDOW, "bintoéng balué", "Bintoѐng Baluѐ (009)", "Widow-before-marriage", "未婚就守寡的女子（南門二、馬腹一）",
     "amber", "Ammarell A（另作 balué sallatang）；Pelras 7 walu"),
    (CRUX, "bola képpang", "Bintoѐng Bola Kѐppang (001)", "Incomplete (lame) house", "瘸腿的房子（南十字）", "green",
     "Ammarell B；Pelras 6 éppang「瘸」；望加錫 balla' képpang；Ôhashi 列表拼 képang；含 μ Cru"),
    (COALSACK, "bembé'é", "Bembé'é", "The Goat", "山羊（煤袋）", "white", "Ammarell B.1"),
    (stars_of(SEG_SHARK), "bale mangngiweng", "Bintoѐng Balѐ Mangiwѐng (002)", "The Shark", "鯊魚（天蠍尾末＋天壇 α）",
     "red", "Ammarell C；Stellarium 自註連線不確定"),
    (stars_of(SEG_RAY), "lambarué", "Bintoѐng Lambaruѐ (003)", "The Stingray", "魟魚（天蠍頭到尾巴的彎）", "red",
     "Ammarell D；Pelras 8 lambaru；_整理CSV 原譯「雷魚」已改"),
    (stars_of(SEG_SHIP), "bintoéng kappala'é", "Bintoѐng Kappala'ѐ (005/006)", "The Ship Star", "船星（北斗＋ψ UMa＋小熊 β γ）",
     "blue", "Ammarell E、F（Ôhashi Fig. 24.22）；Jaafar & Khairuddin 2021"),
    (WIDOW[:0] + [MERAK, DUBHE], "balu Mandara'", "Bintoѐng Balu Mandara' (004)", "The Mandar Widow",
     "曼達爾的寡婦（天璇、天樞）", "purple", "Ammarell G"),
    ([ALTAIR], "bintoéng timoro'", "Bintoéng Timoro'", "The Eastern Star", "東方的星（牛郎星）", "white", "Ammarell H"),
    (LMC, "tanra Bajoé", "Tanra Bajoé（只標大麥哲倫雲）", "Sign of the Bajau", "巴瑤人的記號（大小麥哲倫雲）", "white",
     "Ammarell M"),
    (stars_of(SEG_PLOUGH), "rakkalaé", "Bintoéng Rakkalaé (008)", "The Plough", "犁（獵戶）", "green",
     "Ammarell J；望加錫 pajjékoé（Stellarium 誤標在參宿七）；連線不含參宿四"),
    (BELT, "tanra tellué", "Tanra Tѐlluѐ (007)", "Sign of Three", "三的記號（腰帶）", "amber",
     "Ammarell J.1；Pelras 3 tanra tellu"),
    (stars_of(SEG_CHICK), "manu'", "Manu' (010)", "The Chicken", "雞（老人星、天狼星、南河三）", "amber",
     "Pelras 4；望加錫 jangang；阿努塔 Manu（A-11）"),
    (stars_of(SEG_RHEA), "Guirá Nhandu", "Guirá Nhandu (tupi 001)", "White Rhea (Tupi)", "美洲鴕（圖皮，上集）", "white",
     "A-25"),
    (stars_of(SEG_NET), "Bittoéng Panjala", "Bittoéng Panjala (mandar 004)", "Fishing Net (Mandar)", "漁網（曼達爾，下集）",
     "white", "A-27；船＝天樞、天璇＋天龍 λ κ α＋牧夫 θ，漁夫＝δ ε ζ UMa"),
    ([POLARIS], "北極星", "—", "Polaris", "北極星", "white", ""),
    ([CANOPUS], "老人星", "—", "Canopus", "老人星", "white", ""),
    ([SIRIUS], "天狼星", "—", "Sirius", "天狼星", "white", ""),
    ([PROCYON], "南河三", "—", "Procyon", "南河三", "white", ""),
    ([RIGIL], "南門二", "—", "Alpha Centauri", "南門二", "white", "4.37 光年"),
    ([HADAR], "馬腹一", "—", "Hadar", "馬腹一", "white", "三百多光年"),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key, disc=False):
        it = dict(anchor(a), text=text, color=color, size=round(size, 2), dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    TT = {t[1]: t for t in TERMS}

    def sz(px, fov):
        """標籤字級：Canva 上 px 大小 → 畫布單位 size（fpx＝size·1.7·1080/fov）"""
        return px * fov / (m.fu * 1080.0)

    def term(name, fov, px1=64, px2=48, dx=0.0, dy=0.0, zh=None, zh_only=False, orig_only=False,
             a=None, disc=False, col=None):
        a0, orig, _, _, zh0, col0, _ = TT[name]
        a = a if a is not None else a0
        col = col or col0
        zh = zh or zh0.split("（")[0]
        s1, s2 = sz(px1, fov), sz(px2, fov)
        gap = (px1 + px2) * 0.62 * fov / 1080.0
        if zh_only:
            out = [item(a, zh, col, s1, dx, dy, name, disc)]
        elif orig_only:
            out = [item(a, orig, col, s1, dx, dy, name, disc)]
        else:
            out = [item(a, orig, col, s1, dx, dy + gap / 2, name, disc),
                   item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh", disc)]
        return out

    # ════════════════════ 構圖 ════════════════════
    def dpts(hips, rot, north):
        out = []
        for h in hips:
            ra, dec = (S[h][:2] if isinstance(h, int) else h)
            out.append(disc_xy(m, ra, dec, rot, north))
        return out

    def safe(cx, cy, fov, north):
        yc = yp if north else -yp
        return max(math.hypot(cx + sx * fov / 2, cy + sy * fov * 8 / 9 - yc)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(hips, rot, north, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None):
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while not safe(cx, cy, f, north):
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def hfit(hips, rot, north, phi, fov, fh=0.22, dx=0.0):
        """有地平線的盤構圖：地平線（北／南點）放在離畫面下緣 fh 的高度，目標星水平置中"""
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        y_h = (yp - k * phi) if north else (-yp + k * phi)
        H = fov * 16 / 9
        cx, cy = (max(xs) + min(xs)) / 2 + dx, y_h + (0.5 - fh) * H
        top = cy + 0.5 * H - 0.13 * H
        if max(ys) > top:
            print(f"  ⚠ hfit：最高的星 {max(ys) - top:+.1f} 超出上緣安全區（fov {fov}）")
        f = fov
        while not safe(cx, cy, f, north):
            f *= 0.99
            cy = y_h + (0.5 - fh) * f * 16 / 9
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def sfit(hips, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, extra=(), fov=None):
        pts = [(x_of(S[h][0]), S[h][1]) for h in hips] + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        lim = m.Ds - f * 8 / 9 - 0.5                 # S：|cy|+fov·8/9 ≤ D_s
        cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    R01b = round(ROT["05"] - 22.0, 2)
    R01a = round(R01b - 24.0, 2)
    F01a = dfit(CRUX + WIDOW + [SHAULA, ARA_A, 86228], R01a, False, pad=0.08, dy=-6.0)
    F01b = dfit(CRUX + WIDOW + [COALSACK], R01b, False, pad=0.25, minfov=62.0)
    F04 = dfit(WIDOW, R01b, False, fov=40.0, dy=-3.0)
    PHI_B, PHI_M, PHI_T, PHI_K = BALO[0], MKS[0], TPE[0], KTG[0]
    F05 = hfit(WIDOW + CRUX, ROT["05"], False, PHI_B, 96.0, fh=0.22)
    F07 = dfit(CRUX + WIDOW + [COALSACK], ROT["05"], False, pad=0.14, dy=-4.0)   # 地平線落到畫面下方（山移出頁外）
    F08a = hfit(stars_of(SEG_SHIP) + [POLARIS], ROT["08"], True, PHI_M, 118.0, fh=0.20)
    F08b = hfit(stars_of(SEG_SHIP) + [POLARIS], round(ROT["08"] - 6.0, 2), True, PHI_M, 112.0, fh=0.20)
    F09 = dfit([DUBHE, MERAK, PHECDA, MEGREZ], F08b[3], True, pad=0.10, fov=62.0, dy=-2.0)
    F09b = hfit([LMC, SMC, CANOPUS], ROT["09b"], False, PHI_M, 104.0, fh=0.20)
    ALT_X = x_of(S[ALTAIR][0])
    F10a = (round(ALT_X + 6.0, 2), 4.0, 44.0, 0.0)
    F10b = (round(ALT_X, 2), 4.0, 32.0, 0.0)
    F11a = sfit(stars_of(SEG_RAY) + stars_of(SEG_SHARK), pad=0.06, fov=46.0)
    F11b = (F11a[0], F11a[1], 40.0, 0.0)
    F12a = sfit(stars_of(SEG_PLOUGH) + [BETEL], pad=0.12, fov=30.0)
    F12b = sfit(stars_of(SEG_CHICK), fov=46.0, dy=0.0)
    F12b = (F12b[0], round(-m.Ds + 46.0 * 8 / 9 + 0.6, 2), 46.0, 0.0)   # 壓到 S 下限：老人星離下緣最高
    F14 = hfit(DIPPER, ROT["14"], True, PHI_T, 108.0, fh=0.12, dx=-4.0)
    F14b1 = F12b
    PLAN = [(x_of(PL[n]["ra"]), PL[n]["dec"]) for n in ("月亮", "木星", "火星")]
    F14b2 = sfit([REGULUS], fov=40.0, extra=PLAN)
    F15a = hfit(CRUX, ROT["15a"], False, PHI_K, 64.0, fh=0.24)
    F15b = hfit(WIDOW + CRUX, ROT["15b"], False, PHI_K, 78.0, fh=0.24)
    F16a = dfit(stars_of(SEG_SHIP), F08b[3], True, pad=0.10, minfov=60.0)
    F16b = dfit(stars_of(SEG_NET), F08b[3], True, pad=0.08, minfov=60.0)
    print("\n── 構圖 ──")
    for nm in ("F01a F01b F04 F05 F07 F08a F08b F09 F09b F10a F10b F11a F11b F12a F12b F14 F14b2 "
               "F15a F15b F16a F16b").split():
        print(f"  {nm} {locals()[nm]}")
    print("  旋轉：" + "、".join(f"{kk} {T[kk][0]} LST {LST_AT[kk]:.1f} → {v:+.1f}°" for kk, v in ROT.items()))

    # ════════════════════ 標籤 ════════════════════
    # 長圖：dx/dy＝畫布方向（東在左，+dx＝往右＝往西）；盤：畫面方向（原生字不跟著盤轉）
    LB_RHEA = term("Guirá Nhandu", F01a[2], 56, 44, dx=12.0, dy=-18.0, zh="上集：圖皮的美洲鴕", disc=True)  # 起格左緣會切到 → 往右推
    LB_WID = term("bintoéng balué", F04[2], 72, 0, dy=-7.0, orig_only=True, disc=True)
    LB_WIDW = (term("bintoéng balué", F05[2], 60, 46, dy=-9.0, zh="寡婦", disc=True)
               + [item(BIMA_LBL, "往 Bima 港 184.5°", "amber", sz(46, F05[2]), 0.0, 9.0, "Bima", disc=True)])
    LB_HOUSE = (term("bola képpang", F07[2], 60, 46, dx=0.0, dy=10.0, zh="瘸腿的房子", disc=True)
                + term("bembé'é", F07[2], 52, 44, dx=0.0, dy=-6.5, zh="山羊（煤袋）", disc=True))
    LB_SHIP = (term("bintoéng kappala'é", F08b[2], 60, 46, dy=14.0, zh="船星（北斗）", disc=True)
               + [item([POLARIS], "↓ 北極星：地平線下 5°", "white", sz(44, F08b[2]), 0.0, 24.0, "北極星", disc=True)])
    LB_MWID = term("balu Mandara'", F09[2], 64, 48, dx=-9.0, dy=4.0, zh="曼達爾的寡婦", disc=True)
    LB_BAJAU = (term("tanra Bajoé", F09b[2], 64, 48, a=(46.0, -72.0), dy=16.0, zh="巴瑤人的記號", disc=True)
                + [item(LMC, "大麥哲倫雲", "white", sz(40, F09b[2]), 0.0, -10.0, "LMC", disc=True),
                   item(SMC, "小麥哲倫雲", "white", sz(40, F09b[2]), 0.0, -8.0, "SMC", disc=True)])
    LB_EAST = (term("bintoéng timoro'", F10b[2], 64, 48, dx=-6.5, dy=4.0, zh="東方的星")
               + [item(EAST_PT, "正東", "green", sz(44, F10b[2]), -3.2, -1.6, "正東"),
                  item(EAST_PT, f"牛郎星從東偏北 {90 - AZ_ALT:.0f}° 升起", "green", sz(40, F10b[2]), 0.0, -5.2, "東偏北")])
    LB_FISH = (term("lambarué", F11a[2], 64, 48, dx=-9.0, dy=2.0, zh="魟魚")
               + term("bale mangngiweng", F11a[2], 60, 46, dx=15.0, dy=-7.0, zh="鯊魚"))
    LB_PLOUGH = (term("rakkalaé", F12a[2], 72, 54, dx=0.0, dy=-11.5, zh="犁")
                 + term("tanra tellué", F12a[2], 60, 46, dx=-7.5, dy=3.2, zh="三的記號"))
    LB_CHICK = (term("manu'", F12b[2], 72, 54, dx=-9.0, dy=-2.0, zh="雞")
                + [item([ACRUX][:0] + [CANOPUS], "阿努塔：Manu 大鳥", "white", sz(44, F12b[2]), -12.0, 1.2, "Manu"),
                   item([SIRIUS], "天狼星", "white", sz(40, F12b[2]), 4.8, 0.0, "天狼星"),
                   item([PROCYON], "南河三", "white", sz(40, F12b[2]), 4.8, 0.0, "南河三"),
                   item([CANOPUS], "老人星", "white", sz(40, F12b[2]), 5.2, -0.4, "老人星")])
    LB_TPE_N = (term("bintoéng kappala'é", F14[2], 60, 46, dx=-8.0, dy=14.0, zh="船星（北斗）", disc=True)
                + [item([POLARIS], "北極星", "white", sz(40, F14[2]), 0.0, -4.0, "北極星", disc=True)])
    LB_TPE_S = [item([SIRIUS], "天狼星", "white", sz(44, F12b[2]), 4.8, 0.0, "天狼星"),
                item([PROCYON], "南河三", "white", sz(44, F12b[2]), 4.8, 0.0, "南河三"),
                item([CANOPUS], "老人星（台北 11°）", "white", sz(44, F12b[2]), -10.5, 0.0, "老人星"),
                item(stars_of(SEG_CHICK), "雞 manu'", "amber", sz(60, F12b[2]), -9.0, -2.0, "manu'")]
    LB_PLAN = [item((PL["月亮"]["ra"], PL["月亮"]["dec"]), f"月亮（{PL['月亮']['phase']:.0f}%）", "white",
                    sz(44, F14b2[2]), 0.0, 3.4, "月亮"),
               item((PL["木星"]["ra"], PL["木星"]["dec"]), "木星", "white", sz(44, F14b2[2]), 3.6, 0.0, "木星"),
               item((PL["火星"]["ra"], PL["火星"]["dec"]), "火星", "red", sz(44, F14b2[2]), 0.0, -2.6, "火星")]
    LB_KTG1 = term("bola képpang", F15a[2], 56, 44, dy=9.0, zh="瘸腿的房子（5–11°）", disc=True)
    LB_KTG = LB_KTG1 + term("bintoéng balué", F15b[2], 56, 44, dy=-7.0, zh="寡婦（7–8°）", disc=True)
    LB_NET = (term("bintoéng kappala'é", F16a[2], 56, 44, dy=12.0, zh="船星", disc=True))
    LB_NET2 = term("Bittoéng Panjala", F16b[2], 60, 46, dx=19.0, dy=-44.0, zh="曼達爾：漁網（下集）", disc=True)  # 放到漁網右下、不壓船

    label_sets = [(LB_RHEA, "上集-美洲鴕"), (LB_WID, "寡婦"), (LB_WIDW, "寡婦與Bima"), (LB_HOUSE, "房子與山羊"),
                  (LB_SHIP, "船星-望加錫"), (LB_MWID, "曼達爾的寡婦"), (LB_BAJAU, "巴瑤人的記號"),
                  (LB_EAST, "東方的星"), (LB_FISH, "魟魚與鯊魚"), (LB_PLOUGH, "犁與三的記號"),
                  (LB_CHICK, "雞"), (LB_TPE_N, "台北-北斗"), (LB_TPE_S, "台北-雞"), (LB_PLAN, "月亮木星火星"),
                  (LB_KTG1, "墾丁-南十字"), (LB_KTG, "墾丁"), (LB_NET, "船星-推近"), (LB_NET2, "漁網-下集")]
    _place_labels(locals())

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
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot"), ([POLARIS, ALTAIR, CANOPUS, RIGIL, HADAR], "單星光暈", "ring")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="R", sec=11, north=False, frames=[F01a, F01b], layers=["鴕", "深空"],
             labels_start=ls("上集-美洲鴕"), labels=[], labels_end=[],
             vo="上週在巴西，天蠍是鴕鳥的身體。今晚橫越半個地球，到印尼的蘇拉威西：同一片星空，布吉斯水手看見——一座羅盤。",
             card="布吉斯：一座羅盤",
             note=f"南盤（無地平線）順時針慢轉 {R01a:+.1f}°→{R01b:+.1f}°、拉近：起格開上集美洲鴕（圖皮 Guirá Nhandu，白；"
                  "南盤只收到 dec −28，天蠍頭不在盤上，露出的是尾巴與身體那段）＋標籤，迄格前連線與標籤都淡出 → "
                  "停在南十字—半人馬（不開布吉斯連線）；開場字卡"),
        dict(code="02", kind="R", sec=20, north=False, frames=[F01b], layers=["深空"], labels=[],
             overlay="C-A26-01_航線地圖", overlay_layers=["地圖層", "航線層"],
             vo="布吉斯人住在蘇拉威西南部，是出了名的商人和水手。南蘇拉威西的木造帆船，跑遍印尼群島，往西到馬來半島，往南遠到澳洲北岸；這裡的造船技藝，二〇一七年列入聯合國教科文組織的非物質文化遺產。",
             card="造船技藝列入 UNESCO",
             note="南盤定格；疊 C-A26-01（地圖層：蘇拉威西南部、望加錫、布吉斯地區 → 航線層：印尼群島、馬來半島／新加坡、澳洲北岸）；"
                  "帆船照片美宣另尋授權圖（UNESCO 名錄「Pinisi, art of boatbuilding in South Sulawesi」2017）"),
        dict(code="03", kind="R", sec=19, north=False, frames=[F01b], layers=["深空"], labels=[],
             overlay="C-A26-02_星羅盤", overlay_layers=["港口層", "星路層"],
             vo="一九九一年起，人類學家 Gene Ammarell 在弗洛勒斯海的小島 Balobaloang，跟布吉斯船員住了一年多。船員告訴他：哪顆星會在哪座島、哪個港口的上方升起、停住或落下。Ammarell 說，這是一座星羅盤。",
             card="星從哪座島升起",
             note="畫面不動；C-A26-02 星羅盤（港口層：以 Balobaloang 為圓心的港口方位線，方位自算 → 星路層：一顆星升起、停住、落下）"),
        dict(code="04", kind="R", sec=13, north=False, frames=[F01b, F04], layers=["寡", "暈"],
             labels=ls("寡婦"), labels_start=[],
             vo="他們最常用的，是南方兩顆並排的亮星：南門二和馬腹一。布吉斯人叫它 bintoéng balué，還沒出嫁就守寡的女子——未婚夫在婚禮前死了。",
             card="未婚就守寡的女子",
             note="南盤同角度推近南門二＋馬腹一（fov 44）：Bintoéng Balué（琥珀，bugis 009）；標籤只放原文（中文在字卡）"),
        dict(code="05", kind="R", sec=9, north=False, horizon=[PHI_B], frames=[F04, F05],
             layers=["寡", "Bima", "暈"], labels=ls("寡婦與Bima"), labels_start=ls("寡婦"),
             vo="七月底、八月初的黃昏，從 Balobaloang 往南看，她就站在 Bima 港的方向。水手靠她，定下出發的航向。",
             card="7 月底黃昏＝往 Bima",
             note=f"南盤順時針轉到 {ROT['05']:+.1f}°（＝Balobaloang 7/31 18:28 民用昏影、面南）並拉遠；山升到南緯 6.6° 的南方地平線；"
                  f"Bima 方位線（琥珀虛線，方位 {BIMA_AZ}°）正好從南門二（182.5°）與馬腹一（187.9°）中間穿過"),
        dict(code="06", kind="R", sec=10, north=False, horizon=[PHI_B], frames=[F05], layers=["寡", "Bima", "暈"],
             labels=ls("寡婦與Bima"),
             overlay="C-A26-03_並肩的寡婦", overlay_layers=["距離層"],
             vo="這兩顆星看起來並肩，其實一顆離我們四點四光年，是離太陽最近的恆星系；另一顆遠在三百多光年外。",
             card="4.4 vs 300 多光年",
             note="畫面不動；疊 C-A26-03（側視距離：地球→南門二 4.37 光年→馬腹一 三百多光年，比例尺斷開處加波浪）"),
        dict(code="07", kind="R", sec=12, north=False, horizon=[PHI_B], frames=[F05, F07],
             layers=["寡", "房", "深空"], labels=ls("房子與山羊"), labels_start=ls("寡婦與Bima"),
             vo="她旁邊的南十字，是 bola képpang，一間瘸腿的房子：一根柱子比另一根短，整間歪一邊。一旁那塊黑黑的暗星雲「煤袋」，是一隻山羊。",
             card="瘸腿的房子・山羊",
             note="同角度推近南十字（fov 70）：Bola Képpang（綠，bugis 001：十字架二、三、一、四＋μ Cru）；"
                  "煤袋（Bembé'é，深空天體層的虛線框；山羊剪影不畫）"),
        dict(code="08", kind="R", sec=13, north=True, cut=True, horizon=[PHI_M], frames=[F08a, F08b],
             layers=["船", "暈"], labels=ls("船星-望加錫"), labels_start=[],
             vo="往北呢？在南緯五度，北極星永遠在地平線下。指北的是北斗，布吉斯人叫它 bintoéng kappala'é，船星——就像他們自己的木造帆船。",
             card="北斗＝船星",
             note=f"【硬切】南盤→北盤（往北轉頭）：望加錫面北（{T['08'][0]}，{ROT['08']:+.1f}°→{F08b[3]:+.1f}°，北斗剛過上中天前）；"
                  "山＝南緯 5.1° 的北方地平線，盤心（北天極）在山下 5°；北極星細圈藏在山後，標籤「↓ 北極星：地平線下 5°」放在山上；"
                  "Bintoéng Kappala'é（藍，bugis 006：北斗七星＋ψ UMa＋小熊 β、γ，共 10 顆）"),
        dict(code="09", kind="R", sec=7, north=True, horizon=[PHI_M], frames=[F08b, F09],
             layers=["船", "曼"], labels=ls("曼達爾的寡婦"), labels_start=ls("船星-望加錫"),
             vo="斗口這兩顆，另叫「曼達爾的寡婦」——曼達爾是隔壁的另一個航海民族。",
             card="天上住著鄰居",
             note="北盤同角度推近斗口（fov 62）：天樞、天璇＝Balu Mandara'（紫，bugis 004）"),
        dict(code="09b", kind="R", sec=11, north=False, cut=True, horizon=[PHI_M], frames=[F09b],
             layers=["深空"], labels=ls("巴瑤人的記號"),
             overlay="C-A26-04_天上的鄰居", overlay_layers=["鄰居層"],
             vo="轉回南邊，大小麥哲倫雲叫「巴瑤人的記號」——巴瑤是傳統上以船為家的海上民族。布吉斯人的天上，住著他們的鄰居。",
             card="天上住著鄰居",
             note=f"【硬切】北盤→南盤（轉回南邊）：望加錫面南（{T['09b'][0]}，{ROT['09b']:+.1f}°，大麥哲倫雲上中天、高 27°）；"
                  "大小麥哲倫雲（深空天體層）＋Tanra Bajoé（Stellarium 只標大麥哲倫雲，小麥哲倫雲依 Ammarell M 補）；"
                  "最後一句疊 C-A26-04（布吉斯、曼達爾、巴瑤的位置小地圖）"),
        dict(code="10", kind="S", sec=7, north=True, cut=True, frames=[F10a, F10b], layers=["東", "暈"],
             labels=ls("東方的星"), labels_start=[],
             vo="往東，牛郎星叫東方的星：在蘇拉威西，它差不多從正東方升起。",
             card="牛郎星＝東方的星",
             note=f"【硬切】南盤→長圖（往東）：牛郎星（Bintoéng Timoro'，白細圈＋標籤）；綠虛線＝望加錫的東方地平線"
                  f"（牛郎星升起那一刻，自訂層），綠點＝正東；升起方位 {AZ_ALT:.1f}°（PyEphem 含折射 81.1°）"),
        dict(code="11", kind="S", sec=16, north=True, frames=[F10b, F11a, F11b], layers=["魟", "鯊"],
             labels=ls("魟魚與鯊魚"), labels_start=ls("東方的星"),
             overlay="C-A26-05_同一個S形",
             vo="天蠍在這裡變成兩條魚：從頭到尾巴的彎是一條魟魚，最末那一鉤是一條鯊魚。連續三週，同一個 S 形：亞馬遜看到毒蛇，巴西海岸看到鴕鳥，這片海看到魟魚和鯊魚。",
             card="魟魚＋鯊魚",
             note="長圖往右（西）滑到天蠍 fov 46→40：Lambarué 魟魚（紅，bugis 003：頭、身體到尾巴的彎，10 顆）、"
                  "Bale Mangngiweng 鯊魚（紅細線，bugis 002：尾末＋天壇座 α，Stellarium 自註不確定）；"
                  "「連續三週」起定格疊 9:16 圖卡 C-A26-05（圖卡諾毒蛇／圖皮美洲鴕／布吉斯魟魚＋鯊魚），停 8 秒"),
        dict(code="12", kind="S", sec=15, north=True, cut=True, frames=[F12a, F12b], layers=["犁", "三", "雞", "暈"],
             labels_start=ls("犁與三的記號"), labels=ls("犁與三的記號"), labels_end=ls("雞"),
             vo="上了岸，布吉斯人也種稻：獵戶是一把犁，腰帶三顆叫三的記號。老人星、天狼星、南河三連成一隻雞，叫 manu'——跟太平洋小島阿努塔的大鳥 Manu，同三顆星，同一個字。",
             card="manu'＝雞＝Manu",
             note="【硬切】（從天蠍 x −60 到獵戶 x +105，滑過去要橫越大半張長圖；旁白「上了岸」）獵戶 fov 30："
                  "犁 Bintoéng Rakkalaé（綠，bugis 008，不含參宿四）＋腰帶 Tanra Tellué（琥珀，bugis 007）→"
                  "「老人星」起往左下滑到雞 Manu'（琥珀，bugis 010）fov 46；角落可放 A-11 圖卡 C-A11-05「同一個字」縮圖"
                  "（從 05_素材/A-11_阿努塔/_概念圖/ 插入，callback）"),
        dict(code="13", kind="S", sec=18, north=True, frames=[F12b], layers=["雞"], labels=ls("雞"),
             overlay="C-A26-06_南島語族擴散", overlay_layers=["台灣層", "擴散層"],
             vo="同一個字，不是巧合。主流的看法是：南島語族的祖先，大約四千年前從台灣出海，往南到菲律賓，再到蘇拉威西，帶著稻米，還有航海的本事。至於星座是不是也一起帶來的，還沒有定論。",
             card="4,000 年前・從台灣出海",
             note="長圖定格；疊 C-A26-06（台灣層 → 擴散層：台灣→菲律賓 約 4,000 年前→蘇拉威西 約 3,500 年前→太平洋；"
                  "角落小字「主流說法（Bellwood 等）」）"),
        dict(code="14", kind="R", sec=6, north=True, horizon=[PHI_T], frames=[F14], layers=["船", "暈"],
             labels=ls("台北-北斗"),
             vo="這週末晚上七點半，台灣往東北看，北斗這艘船斗柄朝下。",
             card="週末 19:30 抬頭看",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）；轉到台北 3/19 19:30 面北（{ROT['14']:+.1f}°）；"
                  "東北方北斗斗柄朝下（天樞 38°、搖光 15°）；山＝台北北方地平線"),
        dict(code="14b", kind="S", sec=12, north=True, frames=[F14b1, F14b2], layers=["雞", "行", "暈"],
             labels_start=ls("台北-雞"), labels=ls("台北-雞"), labels_end=ls("月亮木星火星"),
             overlay="C-A26-07_這週末抬頭看",
             vo="往南，天狼星、南河三，加上貼著地平線的老人星，就是那隻雞——老人星八點後就太低了。東邊高處的木星和火星，今晚就貼在月亮旁邊。",
             card="月亮只有 3/19 在木星火星旁邊",
             note="【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）→ 雞（琥珀：南河三 70°、天狼 47°、老人星 11°）"
                  f"→往右上滑到月亮（{PL['月亮']['phase']:.0f}%）＋木星（約 2°）＋火星（約 4°）；迄格疊 9:16 圖卡 C-A26-07（停 5 秒以上）"),
        dict(code="15", kind="R", sec=14, north=False, horizon=[PHI_K], frames=[F15a, F15b],
             layers=["房", "寡", "深空"], labels_start=ls("墾丁-南十字"), labels=ls("墾丁"),
             vo="南十字和寡婦呢？要過了半夜，到墾丁往正南看：南十字最高五到十一度，寡婦凌晨兩點多也只有七、八度。要等四到六月、沒有月亮的晚上，才比較好找。",
             card="墾丁凌晨・不到 11°｜月落 04:15",
             note=f"【換組】長圖→南盤（自動插回中心／下移／長圖轉南盤）→ 墾丁 3/20 00:40 面南（{ROT['15a']:+.1f}°，山＝21.95°N）"
                  f"→ 轉到 02:30（{ROT['15b']:+.1f}°）：南十字 5–11°（只有十字架一過 10°）、寡婦 7–8°"),
        dict(code="16", kind="R", sec=13, north=True, cut=True, horizon=[PHI_M], frames=[F16a, F16b],
             layers=["船", "網"], labels_start=ls("船星-推近"), labels=ls("漁網-下集"),
             vo="下週五，去看住在隔壁的曼達爾人。同一片海，鯊魚、魟魚、瘸腿的房子都在——但北斗那一帶在他們眼裡，是一張漁網，連著一艘船和三個漁夫。",
             card="下集見｜曼達爾：同一片海的另一套星圖（南島雙聯集・下）",
             note="【硬切】南盤→北盤（下集預告）：望加錫面北（同 08 鏡角度），推近北斗；船（藍）淡出、"
                  "曼達爾漁網 Bittoéng Panjala（白虛線，Stellarium mandar 004：天樞、天璇＋天龍 λ κ α＋牧夫 θ；"
                  "漁夫＝δ ε ζ UMa，細節留給 A-27）淡入；端卡＋追蹤 CTA"),
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
    for sh in shots:                                   # Canva M&M：單段旋轉 < 180°
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 178.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° 太接近 180°（Canva 可能反轉）")
    for nm in ("14",):
        print(f"  {nm} 換組→{ROT[nm]:+.1f}°、歸位 {ROT[nm]:+.1f}°→0°（< 180° ✓）" if abs(ROT[nm]) < 178
              else f"  ✗ {nm} 旋轉 {ROT[nm]}")

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
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1),
                         "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{kk: v for kk, v in s.items()} for s in shots])

    print("  天體（台北 3/19 19:30，J2000）：" + "、".join(
        f"{kk} RA {v['ra']:.1f} Dec {v['dec']:+.1f} 高 {v['alt']}° 方位 {v['az']}°" for kk, v in PL.items()))
    print(f"  牛郎星升起（望加錫）：LST {LST_ALT:.1f}、方位 {AZ_ALT:.1f}°；Bima 線標籤點 RA {BIMA_LBL[0]:.1f} Dec {BIMA_LBL[1]:+.1f}")
    print(f"  x：南十字 {x_of(S[ACRUX][0]):+.1f}、南門二 {x_of(S[RIGIL][0]):+.1f}、天權 {x_of(S[MEGREZ][0]):+.1f}、"
          f"牛郎 {ALT_X:+.1f}、心宿二 {x_of(S[ANTARES][0]):+.1f}、天壇 α {x_of(S[ARA_A][0]):+.1f}、"
          f"參宿二 {x_of(S[ALNILAM][0]):+.1f}、老人星 {x_of(S[CANOPUS][0]):+.1f}、南河三 {x_of(S[PROCYON][0]):+.1f}、"
          f"月亮 {x_of(PL['月亮']['ra']):+.1f}；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Guirá Nhandu", 中譯="美洲鴕（圖皮，A-25）", 英文="White Rhea", 顏色="white"),
                         dict(原文="Manu", 中譯="大鳥（阿努塔，A-11）", 英文="Bird", 顏色="amber"),
                         dict(原文="Bittoéng Panjala", 中譯="漁網（曼達爾，A-27）", 英文="Fishing Net", 顏色="white")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": ROT, "lst0": LST0, "bodies": PL,
               "altair_rise": dict(lst=LST_ALT, az=AZ_ALT), "bima_az": BIMA_AZ},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for kk in sh.get("layers", []) for x in LINE_GROUPS[kk]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


def _place_labels(L):
    """標籤位置第二輪微調（看過 SB-鏡頭牆與對位參考後逐條調；dx/dy 單位＝畫布單位）"""
    pass


if __name__ == "__main__":
    build()
