# -*- coding: utf-8 -*-
"""A-25 圖皮-瓜拉尼：1614 年傳教士抄下的星空｜大畫布 v4.6

論點：1612 年法國嘉布遣會士 Claude d'Abbeville 在巴西北岸馬拉尼昂島住了四個月，1614 年在巴黎出書，
抄下圖皮南巴人的 28 個星名（大多跟雨季有關），最後寫「還有很多，我就不寫了」。將近四百年後，
巴西天文學家 Germano Afonso 比對今天巴西南部瓜拉尼人的星空，認回了幾個：
白鴕鳥 Yandoutin（美洲鴕，南十字—蒼蠅—半人馬—天蠍）、兩顆蛋 Ouyra-Oupia（γ、δ Mus）、
拿棍子的老人 Tuyvaé（獵戶＋金牛）、羽毛 Seichou（昴宿）。

來源：Claude d'Abbeville 1614（07_資料來源/Tupi-Guarani in America/histoiredelamiss00clau.pdf）；
Afonso〈As Constelações Indígenas Brasileiras〉（同資料夾 indigenas.pdf）；Stellarium tupi（Paulo Marcelo Pontes）。
逐字稿：04_腳本庫/A-25-圖皮-瓜拉尼1614年傳教士抄下的星空-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線：照 Stellarium tupi 001（Guira-nhandu 美洲鴕，白）、002（Tuivae 老人，綠）、006（Eixu＝昴宿＝羽毛，藍）。
  不畫 003 北方的貘、004 鹿、005 Joykexo、007 貘的下巴（Afonso 的瓜拉尼田野，不是這本書；逐字稿明訂）。
  自訂層：南十字（紅＝10 鏡「抓住鴕鳥的頭」；白＝15 鏡 Crussa）、煤袋淡框（鴕鳥的頭）、
  蛋（γ、δ Mus 黃圈）、吞下的蛋（南門二、馬腹一橘圈）、狗的候選（畢宿五、心宿二紅圈＋2027/3/12 火星）、
  黃道（虛線，14 鏡沿黃道滑）、月牙（台北 3/12–14 20:00）、台灣看不到（嘴＋兩顆蛋的虛線圈，16 鏡）。

鏡頭路線（南盤主秀＋長圖兩段）
  01 R 南盤（第一頁就在南盤上）：美洲鴕直立（頭＝盤心側在上）慢慢順時針轉 20° → 02–07 概念圖（定格在 01 迄格）
  → 08 整隻美洲鴕＋部位 → 09 推近嘴與蛋 → 10 南十字＋煤袋 → 11 轉到 São Luís 六月中黃昏（山＝São Luís 地平線）
  →【南盤轉長圖】（歸位 −／換組／沿走廊往北：南天極→大麥哲倫雲→老人星→天鴿→天兔，正好接到獵戶）
  → 12 老人 → 13 推近昴宿＋概念圖 → 14 沿黃道從畢宿五滑到心宿二（經過獅子座的火星）
  →【長圖轉南盤】（回中心／下移到南天極／換組）→ 15 南十字 Crussa → 16 墾丁 3/13 01:00 面南
  →【南盤轉長圖】→ 17 台北 3/12 20:00 往西：老人＋昴宿＋月牙 → 9:16 圖卡
  →【長圖轉南盤】→ 18 推近天蠍＝美洲鴕的身體＋端卡。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 95 → 走廊（x=0）＝RA 95：從南天極往北穿過大麥哲倫雲（x +14）、老人星（x −1）、天鴿、天兔，
             一路接到獵戶（參宿四 x +6、參宿七 +16）——三次南盤⇄長圖換組都沿這條走廊上下，不必橫移。
             14 鏡要從畢宿五（x +26）沿黃道滑到心宿二（x −152）：兩顆赤經差 178°，任何 lst 都得滑這麼遠；
             lst 95 讓兩端都離長圖切口（x=±180，RA 275 人馬座，本集長圖用不到）≥ 26°（心宿二格 fov ≤ 50）。
             x：昴宿 +38、畢宿五 +26、π⁵ Ori +22、β Eri +18、獵戶 +6…+16、火星 2027/3/12 −52、心宿二 −152；
             月亮 3/12 +58.5、3/13 +44.6、3/14 +29.7。
  D_s = 48、D_r = 52 → 長圖要放的是老人（獵戶＋金牛，dec −9.7…+24.1）與 17 鏡的月牙（+19.9…+26.5）：
             12 鏡 fov 42、cy +7：|cy|+fov·8/9＝44.3；17 鏡 fov 52、cy −1：47.2 —— D_s 48 剛好都容得下。
             南方：美洲鴕 dec −19.5…−69.1（蛋 −72.1）全部只在南盤上出現（盤檔完整圓，不受縫合帶影響），
             標籤一律 disc=True。D_r 52 → 南十字（−57…−63）、南門二／馬腹一（−60.8／−60.4）、蒼蠅在盤本體。
             D_r 不再往上提：k 會變大，整隻美洲鴕（離盤心 r 31…107）就放不進一個 9:16 畫面。
  D_fill = −20 → k＝1.5078、R_fill＝165.86（盤寬 ÷ 畫布寬＝0.9214）；|x_t|+R_fill ≤ 180 ✓。
             南盤收到 dec +20：16 鏡墾丁南點在盤心上方 kφ＝33.1、心宿二 r 95.9，畫面角落離盤心 ≤ 150 ✓。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 R：Canva 正角＝順時針＝時間前進；rot＝lst_obs − lst（gen_canva_pages.view_lst）。
         美洲鴕「站好」（頭在右上、兩條腿朝下）＝lst_obs 160 → rot +65；São Luís 6/15 18:50（太陽 −12° 前後）＝+92
         （剛好就是牠在東方升起的姿勢）；
         墾丁 3/13 01:00／01:20＝+90.9／+95.9。每段 M&M 旋轉 < 180° ✓（最大一段＝歸位 +96→0°）。

check_shots 的 ⚠（判斷後接受；跑完逐條看過，見檔尾註記）
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS, horizon_points

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-25"
OUT = os.path.join(BASE, "05_素材/A-25_圖皮瓜拉尼/_v4大畫布")
LST0 = 95.0
TPE = (25.0330, 121.5654)
KT = (21.95, 120.80)                  # 墾丁
SL = (-2.53, -44.30)                  # São Luís
PHI_T, PHI_K, PHI_S = 25.033, 21.95, -2.53
ORANGE = "#FF9F43"


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(lat, lon, tz, when):
    return math.degrees(_obs(lat, lon, tz, when).sidereal_time())


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return round((lst_obs - LST0 + 180.0) % 360.0 - 180.0, 2)


LST_AT = {
    "São Luís 6/15 18:50": lst_at(*SL, -3, "2027/6/15 18:50"),
    "墾丁 3/13 01:00": lst_at(*KT, 8, "2027/3/13 01:00"),
    "墾丁 3/13 01:20": lst_at(*KT, 8, "2027/3/13 01:20"),
    "台北 3/12 20:00": lst_at(*TPE, 8, "2027/3/12 20:00"),
}
ROT_UP = 65.0                                   # 美洲鴕站好：頭在右上、身體居中、兩條腿朝下（lst_obs 160）
ROT_SL = rot_s(LST_AT["São Luís 6/15 18:50"])
ROT_K1 = rot_s(LST_AT["墾丁 3/13 01:00"])
ROT_K2 = rot_s(LST_AT["墾丁 3/13 01:20"])


def bodies():
    """J2000 astrometric（與星表同框）：台北 3/12–14 20:00 的月亮、3/12 的火星"""
    import ephem
    out = {}
    for d in (12, 13, 14):
        o = _obs(*TPE, 8, f"2027/3/{d} 20:00")
        mo = ephem.Moon(o)
        out[f"月亮3/{d}"] = dict(ra=math.degrees(mo.a_ra), dec=math.degrees(mo.a_dec),
                               alt=round(math.degrees(mo.alt), 1), phase=round(mo.phase, 1))
    o = _obs(*TPE, 8, "2027/3/12 20:00")
    ma = ephem.Mars(o)
    out["火星2027"] = dict(ra=math.degrees(ma.a_ra), dec=math.degrees(ma.a_dec),
                         alt=round(math.degrees(ma.alt), 1), mag=round(float(ma.mag), 2))
    return out


PL = bodies()


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"]] = [s for s in segs if len(set(s)) >= 2]
    return out


TP = load_sc("tupi")
SEG_OST, SEG_OLD, SEG_PLE = TP["CON tupi 001"], TP["CON tupi 002"], TP["CON tupi 006"]
hips_of = lambda segs: sorted({h for s in segs for h in s})
OST = hips_of(SEG_OST)
OLD = hips_of(SEG_OLD)
PLE = hips_of(SEG_PLE)
assert len(OST) == 42 and len(OLD) == 22, (len(OST), len(OLD))

ACRUX, MIMOSA, GACRUX, IMAI = 60718, 62434, 61084, 59747
CRUX = [ACRUX, MIMOSA, GACRUX, IMAI]
SEG_CRUX = [[GACRUX, ACRUX], [MIMOSA, IMAI]]
ALPHA_MUS, BETA_MUS, GAMMA_MUS, DELTA_MUS = 61585, 62322, 61199, 63613
BEAK = [ALPHA_MUS, BETA_MUS]
EGGS = [GAMMA_MUS, DELTA_MUS]
RIGIL, HADAR = 71683, 68702
SWALLOWED = [RIGIL, HADAR]
ANTARES, ALDEBARAN, BETELGEUSE, RIGEL, ALCYONE, ATLAS = 80763, 21421, 27989, 24436, 17702, 17847
BETA_ERI, PI5_ORI = 23875, 22797
COALSACK = (192.9, -62.8)                       # 煤袋中心（約 7°×5°）
# 部位（全部依 Afonso；逐字稿 08 鏡畫面欄）
NECK = [62268, 64094, 65387, 70264, 72131, 74824]           # 南十字旁—圓規 β／蒼蠅 β—南三角 β 一帶
BODY = [77952, 79664, 82363, 83081, 83153, 85792, 76297, 74395, 77634, 80763, 81266, 82396, 82514]
TAIL = [78401, 78820, 78933, 79374]                         # 天蠍的螯（δ、β¹、ω、ν Sco）＝尾巴
LEG1 = [84143, 86228, 87073, 86670, 85927, 87261, 86698]    # 天蠍的尾巴＝一條腿
LEG2 = [89096, 87936, 87846, 88726]                         # 天壇—望遠鏡（＋南冕）＝另一條腿
ORION = [27989, 26207, 25336, 25930, 26311, 26727, 27366, 24436]
HYADES = [21421, 20894, 20889, 20455, 20205]
MAINS = sorted(set(CRUX + BEAK + EGGS + SWALLOWED + [ANTARES, ALDEBARAN, BETELGEUSE, RIGEL, ALCYONE,
                                                      ATLAS, BETA_ERI] + TAIL + LEG1[:5]))


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
LG_OST = [(SEG_OST, "white", 1.0)]
LG_OLD = [(SEG_OLD, "green", 1.0)]
LG_PLE = [(SEG_PLE, "blue", 1.0)]
LG_CRUX_R = [(SEG_CRUX, "red", 1.0)]
LG_CRUX_W = [(SEG_CRUX, "white", 1.0)]
LG_ALL = LG_OST + LG_OLD + LG_PLE
LINE_SETS = [(LG_OST, "連線-Yandoutin美洲鴕"), (LG_OLD, "連線-Tuyvaé老人"), (LG_PLE, "連線-Seichou昴宿"),
             (LG_CRUX_R, "連線-南十字紅"), (LG_CRUX_W, "連線-Crussa南十字白")]
LINES_KEY = {"L4": "星座連線", "鴕": "連線-Yandoutin美洲鴕", "老": "連線-Tuyvaé老人", "昴": "連線-Seichou昴宿",
             "十紅": "連線-南十字紅", "十白": "連線-Crussa南十字白", "煤": "煤袋淡框", "蛋": "蛋（黃圈）",
             "吞": "吞下的蛋（橘圈）", "狗": "狗的候選（紅圈）", "黃道": "黃道（虛線）", "月": "月牙3月12–14日",
             "看不到": "台灣看不到（虛線圈）"}
LINE_GROUPS = {"L4": LG_ALL, "鴕": LG_OST, "老": LG_OLD, "昴": LG_PLE, "十紅": LG_CRUX_R, "十白": LG_CRUX_W,
               "煤": [], "蛋": [], "吞": [], "狗": [], "黃道": [], "月": [], "看不到": []}


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


def sep(S, a, b):
    va, vb = vec(*S[a][:2]), vec(*S[b][:2])
    return math.degrees(math.acos(max(-1.0, min(1.0, sum(p * q for p, q in zip(va, vb))))))


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    dec = dec0 + y
    return (ra0 + x / max(0.05, math.cos(math.radians(dec)))) % 360, dec


def ellipse(ra0, dec0, a, b, n=60):
    return [tangent_pt(ra0, dec0, a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n))
            for i in range(n + 1)]


def custom_layers(m, S):
    RED, AMB = COLORS["red"], COLORS["amber"]

    def coal(s, pos, runs, disc):
        s.polylines(runs(ellipse(*COALSACK, 3.6, 2.6)), stroke="#FFFFFF", w=m.lw * 0.5, opacity=0.55,
                    dash="0.9 0.6")

    def rings(hips, col, r, op=0.95, dash=None):
        def fn(s, pos, runs, disc):
            for h in hips:
                for p in pos(*S[h][:2]):
                    s.circle(p[0], p[1], r, fill="none", stroke=col, w=m.lw * 0.55, opacity=op, dash=dash)
        return fn

    def mars(s, pos, runs, disc):
        rings([ALDEBARAN, ANTARES], RED, 1.5)(s, pos, runs, disc)
        for p in pos(PL["火星2027"]["ra"], PL["火星2027"]["dec"]):
            s.circle(p[0], p[1], 1.4, fill=RED, opacity=0.16)
            s.circle(p[0], p[1], 0.55, fill=RED, opacity=0.98)

    def ecl(s, pos, runs, disc):
        eps = math.radians(23.4393)
        pts = []
        for i in range(721):
            lam = math.radians(i / 2.0)
            ra = math.degrees(math.atan2(math.sin(lam) * math.cos(eps), math.cos(lam))) % 360
            dec = math.degrees(math.asin(math.sin(eps) * math.sin(lam)))
            pts.append((ra, dec))
        s.polylines(runs(pts), stroke=AMB, w=m.lw * 0.5, opacity=0.45, dash="1.2 0.9")

    def moons(s, pos, runs, disc):
        for k, op in (("月亮3/12", 0.98), ("月亮3/13", 0.55), ("月亮3/14", 0.55)):
            for p in pos(PL[k]["ra"], PL[k]["dec"]):
                s.circle(p[0], p[1], 1.6, fill="#FFF6D8", opacity=0.12 * op / 0.98)
                s.circle(p[0], p[1], 0.62, fill="#FFF6D8", opacity=op)

    return [("煤袋淡框", coal), ("蛋（黃圈）", rings(EGGS, AMB, 1.25)),
            ("吞下的蛋（橘圈）", rings(SWALLOWED, ORANGE, 1.4)),
            ("狗的候選（紅圈）", mars), ("黃道（虛線）", ecl), ("月牙3月12–14日", moons),
            ("台灣看不到（虛線圈）", rings(BEAK + EGGS, "#FFFFFF", 1.9, 0.7, "0.8 0.6"))]


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


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；外文照逐字稿「配音提示」的唸法）
# ══════════════════════════════════════════════════════════════════
SYL = {"claude": 3, "d": 1, "abbeville": 3, "germano": 3, "afonso": 3, "yandoutin": 3, "ouyra": 3,
       "oupia": 3, "tuyvaé": 4, "seichou": 2, "iaouare": 3, "crussa": 3}


def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.lower() in SYL:
            n += SYL[w.lower()]
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyáéíóúãõ]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (OST, "Yandoutin", "Guira-nhandu", "White Ostrich (a rhea)", "白色的鴕鳥（美洲鴕）", "white",
     "Abbeville 1614 fol. 319r「l'Autruche blanche」；辨認（南十字—天蠍）＝Afonso；Stellarium tupi 001 用瓜拉尼名 Guira-nhandu"),
    ([COALSACK], "頭（煤袋）", "—", "Head (the Coalsack)", "頭（煤袋）", "white", "Afonso：頭＝煤袋周圍的星"),
    (BEAK, "嘴", "—", "Beak (α, β Mus)", "嘴（蒼蠅座 α、β）", "white", "Afonso"),
    (NECK, "脖子", "—", "Neck", "脖子", "white", "Afonso：南門二、馬腹一夾在脖子裡"),
    (BODY, "身體", "—", "Body", "身體（南三角—天壇—天蠍身）", "white", "Afonso"),
    (TAIL, "尾巴（天蠍的螯）", "—", "Tail (Scorpius' claws)", "尾巴（天蠍的螯）", "white", "Afonso"),
    (LEG1, "腿（天蠍的尾巴）", "—", "Leg (Scorpius' tail)", "腿（天蠍的尾巴）", "white", "Afonso"),
    (LEG2, "腿", "—", "Leg (Ara–Telescopium)", "腿（天壇—望遠鏡）", "white", "Afonso；含南冕 HIP 88726"),
    (EGGS, "Ouyra-Oupia", "Quira-Rupia", "the two eggs", "兩顆蛋（蒼蠅座 γ、δ）", "amber",
     "Abbeville fol. 319r「les deux œufs」；辨認＝Afonso；Stellarium 星名 Quira-Rupia（瓜拉尼）"),
    (SWALLOWED, "吞下的蛋", "—", "the two swallowed eggs", "已經吞下的兩顆蛋（南門二、馬腹一）", "amber",
     "Afonso：在脖子裡（dentro do pescoço）"),
    (CRUX, "南十字", "—", "Southern Cross", "南十字（抓住鴕鳥的頭）", "red",
     "瓜拉尼的說法（Cardoso 2007 p. 196 轉引 Afonso）"),
    (CRUX, "Crussa", "—", "Cross", "十字", "white",
     "Abbeville fol. 318r；古圖皮語 kurusá 一般認為借自葡萄牙文 cruz（推論）"),
    (OLD, "Tuyvaé", "Tuivae", "the old man (holding a stick)", "拿著棍子的老人（獵戶＋金牛）", "green",
     "Abbeville fol. 318v；辨認與斷腿神話＝Afonso；Stellarium tupi 002（22 顆，含 β Eri）"),
    ([BETELGEUSE], "斷腿處（參宿四）", "—", "Where the leg was cut (Betelgeuse)", "斷腿處（參宿四）", "green", "Afonso"),
    ([PI5_ORI, BETA_ERI, RIGEL], "棍子", "—", "Stick", "棍子", "green",
     "Stellarium 002：π⁵ Ori→β Eri→參宿七；Afonso 文字是 π⁵ Ori 直連參宿七"),
    (PLE, "Seichou", "Eixu", "Pleiades", "羽毛（昴宿）", "blue",
     "Abbeville fol. 316v 作 Seycou、320v 作 Seichou；羽毛＝Afonso；Stellarium 006 用瓜拉尼名 Eixu"),
    ([ALDEBARAN], "畢宿五？", "—", "Aldebaran?", "畢宿五？", "red", "Iaouare 候選（書未說）"),
    ([ANTARES], "心宿二？", "—", "Antares?", "心宿二？", "red", "Iaouare 候選（書未說）"),
    ((PL["火星2027"]["ra"], PL["火星2027"]["dec"]), "火星？", "—", "Mars?", "火星？", "red",
     f"Iaouare 候選（書未說）；畫的是 2027/3/12 的火星（台北 20:00 高 {PL['火星2027']['alt']}°）"),
    ([ALDEBARAN], "Iaouare", "—", "Dog", "狗", "red", "Abbeville fol. 317r：很紅、常緊跟月亮"),
    ((PL["月亮3/12"]["ra"], PL["月亮3/12"]["dec"]), "月牙 3/12", "—", "Moon, Mar 12", "月牙 3/12", "white",
     f"台北 20:00 高 {PL['月亮3/12']['alt']}°、{PL['月亮3/12']['phase']}%"),
    ((PL["月亮3/13"]["ra"], PL["月亮3/13"]["dec"]), "3/13", "—", "Moon, Mar 13", "3/13", "white",
     f"台北 20:00 高 {PL['月亮3/13']['alt']}°、{PL['月亮3/13']['phase']}%"),
    ((PL["月亮3/14"]["ra"], PL["月亮3/14"]["dec"]), "3/14", "—", "Moon, Mar 14", "3/14", "white",
     f"台北 20:00 高 {PL['月亮3/14']['alt']}°、{PL['月亮3/14']['phase']}%"),
    ([ANTARES], "心宿二", "—", "Antares", "心宿二", "white", "墾丁 3/13 01:00 高 13°"),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def disc_xy(m, ra, dec, rot, north=False):
    """天體在「轉 rot 之後的盤」上的位置（畫面方向的畫布單位，盤心＝(0, ±y_pole)）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=48, D_r=52, D_fill=-20.0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]} if isinstance(a[0], int) else {"ra": a[0][0], "dec": a[0][1]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key, disc=False):
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    T = {t[1]: t for t in TERMS}

    def term(name, dx=0.0, dy=0.0, s1=1.6, s2=1.2, gap=2.4, zh_only=False, a=None, disc=False, zh=None,
             col=None):
        a0, orig, _, _, zh0, col0, _ = T[name]
        a = a if a is not None else a0
        zh = zh or zh0
        col = col or col0
        if zh_only:
            return [item(a, zh, col, s1, dx, dy, name, disc)]
        return [item(a, orig, col, s1, dx, dy + gap / 2, name, disc),
                item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh", disc)]

    # 字級：Canva px ≈ size×1.7×1080/fov；主名 ~55 px、譯名 ~45 px（Canva 夾在 36–96）
    sz = lambda f: dict(s1=round(f * 0.030, 2), s2=round(f * 0.024, 2), gap=round(f * 0.046, 2))
    zs = lambda f, k=0.024: round(f * k, 2)
    DS = dict(disc=True)
    # 08 鏡整隻（fov ~F08）；部位只寫中文
    F08 = 96.0
    LB_OST = (term("Yandoutin", zh="白色的鴕鳥（美洲鴕）", **sz(F08), **DS)
              + term("頭（煤袋）", zh_only=True, s1=zs(F08), **DS)
              + term("嘴", zh_only=True, s1=zs(F08), **DS)
              + term("脖子", zh_only=True, s1=zs(F08), **DS)
              + term("身體", zh_only=True, s1=zs(F08), zh="身體", **DS)
              + term("尾巴（天蠍的螯）", zh_only=True, s1=zs(F08), **DS)
              + term("腿（天蠍的尾巴）", zh_only=True, s1=zs(F08), **DS)
              + term("腿", zh_only=True, s1=zs(F08), zh="腿", **DS)
              + [item(OST, "辨認：Afonso", "white", zs(F08, 0.018), 0.0, 0.0, "Yandoutin-註", True)])
    F09 = 40.0
    LB_EGG = (term("Ouyra-Oupia", zh="兩顆蛋", **sz(F09), **DS)
              + term("吞下的蛋", zh_only=True, s1=zs(F09), zh="已經吞下的兩顆蛋", col="amber", **DS)
              + term("嘴", zh_only=True, s1=zs(F09), **DS))
    F10 = 34.0
    LB_GRIP = (term("南十字", zh="抓住鴕鳥的頭", **sz(F10), **DS)
               + term("頭（煤袋）", zh_only=True, s1=zs(F10), **DS))
    F11 = 110.0
    LB_JUNE = term("Yandoutin", zh="六月黃昏・東方升起", **sz(F11), **DS)
    F12 = 42.0
    LB_OLD = (term("Tuyvaé", zh="拿著棍子的老人", **sz(F12))
              + term("斷腿處（參宿四）", zh_only=True, s1=zs(F12))
              + term("棍子", zh_only=True, s1=zs(F12))
              + [item(OLD, "辨認與斷腿神話：Afonso", "white", zs(F12, 0.018), 0.0, 0.0, "Tuyvaé-註")])
    F13 = 24.0
    LB_PLE = term("Seichou", zh="羽毛（昴宿）", **sz(F13))
    F14 = 40.0
    LB_DOG = (term("Iaouare", zh="狗", **sz(F14))
              + term("畢宿五？", zh_only=True, s1=zs(F14, 0.028))
              + term("心宿二？", zh_only=True, s1=zs(F14, 0.028))
              + term("火星？", zh_only=True, s1=zs(F14, 0.028)))
    F15 = 30.0
    LB_CRU = (term("Crussa", zh="十字", **sz(F15), **DS)
              + [item(CRUX, "葡萄牙文 cruz？", "white", zs(F15, 0.020), 0.0, 0.0, "Crussa-註", True)])
    F16 = 100.0
    LB_KT = (term("南十字", zh="南十字＝鴕鳥的頭", zh_only=True, s1=zs(F16, 0.026), col="white", **DS)
             + term("心宿二", zh_only=True, s1=zs(F16, 0.024), **DS)
             + [item(BEAK + EGGS, "嘴和兩顆蛋：台灣看不到", "white", zs(F16, 0.022), 0.0, 0.0, "看不到", True)])
    F17 = 52.0
    LB_WEEK = (term("Tuyvaé", zh="拿棍子的老人", zh_only=True, s1=zs(F17, 0.028), col="green")
               + term("Seichou", zh="羽毛（昴宿）", zh_only=True, s1=zs(F17, 0.026), col="blue")
               + term("月牙 3/12", zh_only=True, s1=zs(F17, 0.026))
               + term("3/13", zh_only=True, s1=zs(F17, 0.022))
               + term("3/14", zh_only=True, s1=zs(F17, 0.022)))
    F18 = 48.0
    LB_BODY = term("身體", zh="鴕鳥的身體（天蠍）", zh_only=True, s1=zs(F18, 0.030), **DS)

    label_sets = [(LB_OST, "Yandoutin美洲鴕"), (LB_EGG, "Ouyra-Oupia兩顆蛋"), (LB_GRIP, "南十字抓頭"),
                  (LB_JUNE, "六月黃昏"), (LB_OLD, "Tuyvaé老人"), (LB_PLE, "Seichou羽毛"), (LB_DOG, "Iaouare狗"),
                  (LB_CRU, "Crussa十字"), (LB_KT, "墾丁"), (LB_WEEK, "這週末"), (LB_BODY, "鴕鳥的身體")]

    # ── 標籤偏移（長圖＝畫布方向、東在左；盤＝畫面方向，字不跟著盤轉） ──
    def shift(items, key, dx, dy):
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

    # （看過鏡頭牆放大格後逐條調；盤＝畫面方向，+dx 右、+dy 上）
    shift(LB_OST, "Yandoutin", 0.0, 26.0); shift(LB_OST, "Yandoutin-註", 0.0, 19.0)
    shift(LB_OST, "身體", 0.0, -4.0); shift(LB_OST, "尾巴（天蠍的螯）", 9.0, -5.0)
    shift(LB_OST, "嘴", -11.0, -4.0); shift(LB_OST, "脖子", 9.0, -12.0)
    shift(LB_OST, "腿", 8.0, 0.0); shift(LB_OST, "頭（煤袋）", 0.0, 2.0)
    shift(LB_EGG, "嘴", -5.0, -5.0); shift(LB_EGG, "吞下的蛋", 4.0, 0.0)
    shift(LB_GRIP, "南十字", -9.0, 1.0)
    shift(LB_OLD, "Tuyvaé", 8.0, -12.0); shift(LB_OLD, "Tuyvaé-註", 8.0, -16.5)
    shift(LB_OLD, "斷腿處（參宿四）", 6.0, 2.5)
    shift(LB_PLE, "Seichou", 0.0, -2.6)
    shift(LB_DOG, "Iaouare", -4.0, 6.0); shift(LB_DOG, "畢宿五？", 0.0, -2.2)
    shift(LB_DOG, "心宿二？", 0.0, -2.2); shift(LB_DOG, "火星？", 0.0, -2.0)
    shift(LB_CRU, "Crussa", -9.0, 1.0); shift(LB_CRU, "Crussa-註", -9.0, 5.5)
    shift(LB_KT, "南十字", 0.0, 6.0); shift(LB_KT, "心宿二", 4.0, 3.5); shift(LB_KT, "看不到", -4.0, 7.0)
    shift(LB_WEEK, "Seichou", 0.0, 3.0); shift(LB_WEEK, "3/13", 0.0, -2.6)
    shift(LB_WEEK, "月牙 3/12", -3.0, 3.0); shift(LB_WEEK, "Tuyvaé", 6.0, -10.0)

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 構圖 ════════════════════
    def fit(pts, rot, pad=0.10, minfov=30.0, dy=0.0, dx=0.0, fov=None):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        far = lambda f: max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 + yp)
                            for sx in (-1, 1) for sy in (-1, 1))
        while far(f) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    dpts = lambda hips, rot: [disc_xy(m, *(S[h][:2] if isinstance(h, int) else h), rot) for h in hips]

    def hz_pts(phi, L, rot, az0, az1):
        pts = horizon_points(phi, L, n=721)
        return [disc_xy(m, ra, dec, rot) for ra, dec in pts[int(az0 * 2):int(az1 * 2) + 1]
                if dec < -m.Dfill]

    def sfit(hips, pad=0.12, minfov=30.0, dx=0.0, dy=0.0, extra=(), fov=None):
        pts = [(x_of(S[h][0]), S[h][1]) for h in hips] + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        lim = m.Ds - f * 8 / 9 - 0.5                     # S：|cy|+fov·8/9 ≤ D_s
        cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    # 01／08：整隻美洲鴕直立（頭在上、身體在下）
    OSTF = fit(dpts(OST + EGGS, ROT_UP), ROT_UP, pad=0.08, dy=-2.0)
    F08 = OSTF[2]
    OPEN0 = (OSTF[0], OSTF[1], round(OSTF[2] * 1.12, 1), ROT_UP - 20.0)
    MOUTH = fit(dpts(BEAK + EGGS + SWALLOWED + [ACRUX], ROT_UP), ROT_UP, pad=0.10, minfov=36.0)
    GRIP = fit(dpts(CRUX + [COALSACK] + BEAK, ROT_UP), ROT_UP, pad=0.18, minfov=30.0)
    L_SL = LST_AT["São Luís 6/15 18:50"]
    SLF = fit(dpts(OST + EGGS, ROT_SL) + hz_pts(PHI_S, L_SL, ROT_SL, 90, 200), ROT_SL, pad=0.04, dy=-4.0)
    CRUF = fit(dpts(CRUX, ROT_K1), ROT_K1, pad=0.30, minfov=30.0)
    L_K1, L_K2 = LST_AT["墾丁 3/13 01:00"], LST_AT["墾丁 3/13 01:20"]
    KT1 = fit(dpts(CRUX + SWALLOWED + [ANTARES], ROT_K1) + hz_pts(PHI_K, L_K1, ROT_K1, 160, 200),
              ROT_K1, pad=0.06, minfov=90.0)
    hy = sum(p[1] for p in hz_pts(PHI_K, L_K1, ROT_K1, 175, 185)) / 21      # 南點附近地平線 y
    kx = disc_xy(m, *S[ACRUX][:2], ROT_K1)[0]
    KT1 = (round(kx - 8.0, 2), KT1[1], KT1[2], ROT_K1)                    # 南十字（鴕鳥的頭）略偏右，身體往左延伸
    KT1 = (KT1[0], round(hy + 0.44 * KT1[2] * 8 / 9, 2), KT1[2], ROT_K1)    # 地平線落在畫面 72% 高處（再低 fov 會被 R_fill 壓小）
    while max(math.hypot(KT1[0] + sx * KT1[2] / 2, KT1[1] + sy * KT1[2] * 8 / 9 + yp)
              for sx in (-1, 1) for sy in (-1, 1)) > m.R_fill - 1.0:
        KT1 = (KT1[0], KT1[1], round(KT1[2] * 0.98, 1), ROT_K1)
    KT2 = (KT1[0], KT1[1], KT1[2], ROT_K2)
    BODYF = fit(dpts(BODY + TAIL + LEG1, ROT_UP), ROT_UP, pad=0.06, minfov=44.0)
    BODY2 = (BODYF[0], BODYF[1], round(BODYF[2] * 0.82, 1), ROT_UP)
    # 長圖
    OLDF = sfit(OLD, pad=0.10, minfov=40.0)
    OLD0 = (OLDF[0], OLDF[1], round(OLDF[2] * 1.15, 1), 0.0)
    OLD0 = sfit(OLD, pad=0.10, fov=OLD0[2])
    PLEF = sfit(PLE, pad=0.14, minfov=24.0, dy=-2.0)
    ALDF = sfit([ALDEBARAN, ALCYONE], pad=0.1, fov=40.0)
    ANTF = sfit([ANTARES], fov=40.0)
    mx = [(x_of(PL[k]["ra"]), PL[k]["dec"]) for k in ("月亮3/12", "月亮3/13", "月亮3/14")]
    WK1 = sfit(ORION + PLE, fov=52.0, dx=-2.0)
    WK2 = (round(mx[0][0] - 24.0, 2), WK1[1], 52.0, 0.0)          # 3/12 月牙在畫面右緣內 2°
    print(f"\n── 構圖 ──\n  01 {OPEN0}→{OSTF}\n  09 {MOUTH}\n  10 {GRIP}\n  11 {SLF}\n  12 {OLD0}→{OLDF}\n"
          f"  13 {PLEF}\n  14 {ALDF}→{ANTF}\n  15 {CRUF}\n  16 {KT1}→{KT2}\n  17 {WK1}→{WK2}\n  18 {BODYF}→{BODY2}")

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    NS = dict(north=False)
    shots = [
        dict(code="01", kind="R", sec=11, **NS, frames=[OPEN0, OSTF], layers=["鴕", "蛋"], labels=[],
             vo="上週在亞馬遜，星座一落下，河水就漲。今晚往東，到巴西北岸的海邊：同一片星空，圖皮南巴人看見——一隻想吃蛋的鴕鳥。",
             card="圖皮南巴：想吃蛋的鴕鳥",
             note=f"第一頁就在南盤圖層組（盤心＝南天極）：美洲鴕（白）淡入、兩顆蛋黃圈；盤順時針轉 {ROT_UP - 20:+.0f}°→{ROT_UP:+.0f}°"
                  "（轉完美洲鴕站好：頭在右上、身體居中、兩條腿朝下），同時推近一點；開場字卡"),
        dict(code="02", kind="R", sec=12, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-01_馬拉尼昂島", overlay_layers=["地圖層", "航線層"],
             vo="一六一二年，法國人在巴西北岸的馬拉尼昂島上建了一座堡壘，後來成了今天的聖路易斯。跟著船來的，有四位嘉布遣會士。",
             card="1612・馬拉尼昂島",
             note="畫面不動；疊 C-A25-01（自繪示意：大西洋兩岸＋巴西北岸馬拉尼昂島、São Luís 2.5°S、法國→巴西航線、"
                  "Saint-Louis 堡 1612/9/8）；人物剪影美宣另做（不用真人肖像）"),
        dict(code="03", kind="R", sec=13, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-02_1614年的書", overlay_layers=["扉頁層"],
             vo="其中一位叫 Claude d'Abbeville，在島上只待了四個月，年底就回法國；一六一四年，他在巴黎出了一本書，記下島上圖皮南巴人的生活。",
             card="1614 年，巴黎出版",
             note="畫面不動；疊 C-A25-02 扉頁層（histoiredelamiss00clau.pdf 第 5 頁，1614 年出版物＝公有領域；"
                  "片尾註明「掃描：Internet Archive histoiredelamiss00clau」）"),
        dict(code="04", kind="R", sec=12, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-02_1614年的書", overlay_layers=["原文層"],
             vo="書裡有一段寫星星。他說：當地幾乎人人都認得那半邊天大部分的星，而且每一顆都叫得出名字——那是祖先取的。",
             card="每一顆都叫得出名字",
             note="畫面不動；疊 C-A25-02 原文層（PDF 第 649 頁 fol. 316r 局部，框出 nom propre；不另疊中譯）"),
        dict(code="05", kind="R", sec=13, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-03_二十八個名字", overlay_layers=["名單層", "九個層"],
             vo="接著他抄了二十八個名字：會下雨的下巴、九顆星排成的烤架、螯蝦、猴子、螃蟹、長籃子、圓圓的蜂蜜、燒起來的火，還有一個喝湯的小男孩。",
             card="28 個名字",
             note="畫面不動；疊 C-A25-03：28 個原拼法淡字鋪底 → 依旁白順序亮 9 個（原拼法＋中譯；烤架、螯蝦、猴子、"
                  "喝湯的小男孩放大）；名字一律不放上星圖（書上沒寫是哪幾顆）"),
        dict(code="06", kind="R", sec=13, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-03_二十八個名字", overlay_layers=["結尾原文層", "問號層"],
             vo="名單最後他寫：還有很多，我就不寫了，免得太囉嗦。可惜他大多沒寫是哪幾顆；島上那群圖皮南巴人，後來也在戰爭、疫病和奴役裡消失了。",
             card="還有很多，我就不寫了",
             note="畫面不動；疊 C-A25-03 結尾原文層（PDF 第 656 頁 fol. 319v「& plusieurs autres que ie laisse…」）"
                  "→ 問號層（名字卡變成問號）；最後一句前留半秒空白"),
        dict(code="07", kind="R", sec=15, **NS, frames=[OSTF], layers=["鴕", "蛋"], labels=[],
             overlay="C-A25-04_兩千五百公里", overlay_layers=["地圖層", "時間軸層"],
             vo="將近四百年後，巴西天文學家 Germano Afonso 跟南部的瓜拉尼人一起看天。兩邊是遠親，隔了兩千五百公里，星座竟然很像；他這才把好幾個認了回來。",
             card="2,500 公里・快 400 年",
             note="畫面不動；疊 C-A25-04：巴西示意圖 São Luís ↔ 南部瓜拉尼地區「約 2,500 公里」→ 時間軸 1612 → 2000 年代"
                  "＋小字「同屬圖皮-瓜拉尼語族」"),
        dict(code="08", kind="R", sec=15, **NS, frames=[OSTF], layers=["鴕", "煤"], labels=ls("Yandoutin美洲鴕"),
             vo="最壯觀的一個叫 Yandoutin，傳教士寫成白色的鴕鳥，其實是美洲鴕。Afonso 認出牠從南十字一路伸到天蠍：頭在南十字旁那片暗星雲——煤袋，嘴是蒼蠅座的兩顆星。",
             card="白鴕鳥＝美洲鴕",
             note="同一格（07 的概念圖收掉後）：美洲鴕（白）＋煤袋淡框＋部位標籤（全依 Afonso：頭＝煤袋、嘴＝α β Mus、"
                  "脖子、身體、尾巴＝天蠍的螯、腿＝天蠍的尾巴、腿＝天壇—望遠鏡）；小字「辨認：Afonso」"),
        dict(code="09", kind="R", sec=11, **NS, frames=[OSTF, MOUTH], layers=["鴕", "蛋", "吞"],
             labels=ls("Ouyra-Oupia兩顆蛋"), labels_start=ls("Yandoutin美洲鴕"),
             vo="傳教士寫：牠的嘴，想吃旁邊兩顆星，叫 Ouyra-Oupia：兩顆蛋。Afonso 說，南門二和馬腹一，是牠已經吞下的另外兩顆蛋。",
             card="嘴邊兩顆・吞下兩顆",
             note="同角度推近嘴：γ、δ Mus 黃圈＝Ouyra-Oupia；南門二、馬腹一橘圈＝已經吞下的兩顆（在脖子裡）"),
        dict(code="10", kind="R", sec=9, **NS, frames=[MOUTH, GRIP], layers=["鴕", "十紅", "煤"],
             labels=ls("南十字抓頭"), labels_start=ls("Ouyra-Oupia兩顆蛋"),
             vo="瓜拉尼人還說：南十字緊緊抓著鴕鳥的頭；要是放開，牠會把地上的水全部喝光，大家都會渴死。",
             card="南十字抓住鴕鳥頭",
             note="同角度移到南十字（紅）＋煤袋（頭）；小動畫（南十字鬆手→河湖乾涸）可省"),
        dict(code="11", kind="R", sec=8, **NS, horizon=[PHI_S], frames=[(SLF[0], SLF[1], SLF[2], ROT_UP), SLF], layers=["鴕"],
             labels=ls("六月黃昏"), labels_start=ls("南十字抓頭"),
             vo="Afonso 記下：六月的黃昏，整隻鴕鳥從東方升起，南部就入冬，北部的乾季也開始了。",
             card="六月黃昏＝乾季開始",
             note=f"先拉遠（山升到 São Luís 地平線），再順時針轉 {ROT_UP:+.0f}°→{ROT_SL:+.1f}°（São Luís 6/15 18:50 面南，太陽約 −12°）；山＝São Luís 地平線"
                  "（南天極在南方地平線上 2.5°，地平線幾乎穿過盤心）；美洲鴕在左邊＝東方；"
                  "地圖角標小字（不是字卡）「巴西南部：冬天／北部：乾季」"),
        dict(code="12", kind="Z", sec=14, north=True, frames=[OLD0, OLDF], layers=["老"], labels=ls("Tuyvaé老人"),
             vo="另一個也找回來了：Tuyvaé，拿著棍子的老人，就是獵戶加金牛。獵戶環球那集講過他斷腿的故事；十二月黃昏他從東方升起，北部的雨季就要來。",
             card="拿著棍子的老人",
             note="【換組】南盤→長圖（自動插歸位／南盤轉長圖／沿走廊往北：南天極→大麥哲倫雲→老人星→天兔→獵戶）；"
                  "老人 Tuyvaé（綠，Stellarium 002 共 22 顆；棍子＝π⁵ Ori→β Eri→參宿七）；參宿四＝斷腿處；"
                  "最後 4 秒角落疊 X-02 圖卡「一條腿」縮圖（05_素材/X-02_獵戶環球/_概念圖/C-X02-02_一條腿_預覽_黑底.png，美宣手動放）"),
        dict(code="13", kind="Z", sec=15, north=True, frames=[OLDF, PLEF], layers=["老", "昴"],
             labels=ls("Seichou羽毛"), labels_start=ls("Tuyvaé老人"),
             overlay="C-A25-05_昴宿與雨", overlay_layers=["原文層", "年環層"],
             vo="Afonso 說，老人頭上那撮羽毛是昴宿；傳教士記成 Seichou。他寫：昴宿一出現，雨就來；雨季結束，它就不見；等它再出現，又是下一年的雨——所以他們很清楚一年有多長。",
             card="昴宿＝一年的刻度",
             note="推近昴宿（藍＝羽毛）；結束後疊 C-A25-05：fol. 320v 原文局部 → 一年的環（黃昏東方出現→雨季→黃昏西方消失→再出現）"),
        dict(code="14", kind="S", sec=14, north=True, frames=[ALDF, ANTF], layers=["老", "昴", "狗", "黃道"],
             labels=ls("Iaouare狗"),
             vo="還有一顆很紅的星叫 Iaouare：狗。傳教士說它常緊跟著月亮；月亮要落下時，他們說是這隻狗追著吠，想把月亮吃掉。是心宿二、畢宿五，還是火星？書上沒說。",
             card="Iaouare＝狗",
             note="畢宿五（紅圈）起格，沿黃道（虛線）往東（左）一路滑到心宿二（紅圈）：中途經過獅子座的火星（2027/3/12 的位置，"
                  "標「火星？」）；赤經差 178°，Canva 用 --seg 拆頁；不定案"),
        dict(code="15", kind="R", sec=7, **NS, frames=[CRUF], layers=["十白", "鴕"], labels=ls("Crussa十字"),
             vo="南十字他們也認得，叫 Crussa；這個字，很可能是從葡萄牙文的「十字」借來的。",
             card="Crussa＝十字",
             note=f"【換組】長圖→南盤（自動插回中心／下移到南天極／長圖轉南盤）；盤轉到 {ROT_K1:+.1f}°（＝16 鏡墾丁 01:00 的角度）；"
                  "南十字（白）＋Crussa；小字「葡萄牙文 cruz？」"),
        dict(code="16", kind="R", sec=15, **NS, horizon=[PHI_K], frames=[KT1, KT2],
             layers=["鴕", "看不到"], labels=ls("墾丁"), labels_start=ls("Crussa十字"),
             vo="台灣找得到這隻鴕鳥嗎？三月要等過半夜：凌晨一點在墾丁朝正南看，南十字只比海平面高五到十一度，那是牠的頭；牠的嘴和想吃的那兩顆蛋，在台灣都看不到。",
             card="墾丁 01:00 往正南",
             note=f"拉遠到墾丁 3/13 01:00 面南（山＝墾丁南方地平線，北緯 21.95°）→ 01:20（{ROT_K1:+.1f}°→{ROT_K2:+.1f}°）："
                  "南十字 5–11°、心宿二 13°；嘴與兩顆蛋虛線圈「台灣看不到」（在地平線下）；天蠍尾巴、天壇、望遠鏡還沒升起；"
                  "小字「南方海面無遮蔽、很晴才看得到」"),
        dict(code="17", kind="S", sec=11, north=True, frames=[WK1, WK2], layers=["老", "昴", "月"],
             labels=ls("這週末"),
             overlay="C-A25-06_這週末抬頭看",
             vo="今晚到週日，天黑到十點往西看：拿棍子的老人斜躺在半空，頭上的羽毛是昴宿；細細的月牙，這幾晚都在羽毛附近。",
             card="3/12–14 天黑後往西看",
             note="【換組】南盤→長圖（自動插歸位／南盤轉長圖／沿走廊往北）；獵戶＋金牛（綠）往西（右）滑到月牙："
                  "3/12 月牙（亮）、3/13、3/14（淡）；長圖是赤道座標，畫面不呈現台北西方的「斜躺」姿勢（旁白講）；"
                  "最後 2 秒疊 9:16 圖卡 C-A25-06「這週末抬頭看」（旁白已讀完）"),
        dict(code="18", kind="R", sec=11, **NS, frames=[BODYF, BODY2], layers=["鴕"], labels=[],
             labels_start=ls("鴕鳥的身體"),
             vo="下週五，橫越半個地球到印尼的蘇拉威西：這隻鴕鳥的身體，在帆船民族布吉斯人眼裡，是一條魟魚和一條鯊魚。",
             card="下集見｜布吉斯：帆船民族的星羅盤",
             note="【換組】長圖→南盤（自動插回中心／下移／長圖轉南盤）；盤轉回 01 鏡的直立角度，推近天蠍＝美洲鴕的身體；"
                  "起格開「鴕鳥的身體」→ 迄格標籤淡出；「魟魚＋鯊魚」剪影美宣另做；端卡＋追蹤 CTA"),
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
    for sh in shots:                                   # Canva M&M：單段旋轉 < 180°
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 178.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° 太接近 180°（Canva 可能反轉）")
    for r in {f[3] for sh in shots if sh["kind"] == "R" for f in sh["frames"]}:
        if abs(r) >= 178.0:
            print(f"  ✗ 盤角 {r:+.1f}°：換組歸位（→0°）會超過 180°")

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
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  南盤旋轉角：" + "、".join(f"{k} {v:+.1f}°" for k, v in
                                  (("直立", ROT_UP), ("São Luís", ROT_SL), ("墾丁01:00", ROT_K1), ("墾丁01:20", ROT_K2))))
    print("  LST：" + "、".join(f"{k} {v:.1f}" for k, v in LST_AT.items()))
    print(f"  x：昴宿 {x_of(S[ALCYONE][0]):+.1f}、畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、參宿四 {x_of(S[BETELGEUSE][0]):+.1f}、"
          f"老人星 {x_of(S[30438][0]):+.1f}、心宿二 {x_of(S[ANTARES][0]):+.1f}、火星 {x_of(PL['火星2027']['ra']):+.1f}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")
    print(f"  美洲鴕 嘴（α Mus）→尾巴（ν Sco）{sep(S, ALPHA_MUS, 79374):.1f}°；十字架二→尾宿八 {sep(S, ACRUX, 85927):.1f}°")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=[h for h in hips if isinstance(h, int)] if isinstance(hips, list) else [],
                           原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Aña", 中譯="毒蛇（圖卡諾：天蠍＋人馬，A-24）", 英文="Fer-de-lance", 顏色="red"),
                         dict(原文="魟魚＋鯊魚", 中譯="布吉斯：天蠍一帶（A-26）", 英文="Ray and shark", 顏色="white")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": dict(UP=ROT_UP, SL=ROT_SL, K1=ROT_K1, K2=ROT_K2),
               "lst0": LST0, "bodies": PL},
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
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
