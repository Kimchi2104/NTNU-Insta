# -*- coding: utf-8 -*-
"""A-29 薩丁尼亞：地中海島嶼的農牧星空｜大畫布 v4.6（長圖帶狀為主＋北盤 R）

論點：整片天是一座薩丁尼亞山村——牧人的石屋（Su Pinnetu＝畢宿 V＋畢宿五）、一串葡萄（S'Udrone＝昴宿）、
牧杖（Sos Bacheddos＝獵戶）、羊圈（Sa Mandra＝御夫）、農人的鐮刀（Sa Frache＝獅子座鐮刀）、七兄弟（北斗）、
聖人的十字（Sa Rughe de Santu Antinu＝天鵝）、寡婦之舞（北冕）、鹿角（英仙）、麥稈之路（銀河）。

來源：Stellarium sardinian（舊版 stellarium-skycultures-master：11 星座＋5 具名星，Giuseppe Putzolu，
據 Tonino Bussu、Marco Puddu 的研究，Sedilo 方言；po/sc.po 補原文）；新版 26.2（stellarium-master）只用在
金星兩個名字（10 鏡，概念圖 C-A29-07）。Su Trubadore de sos Bacheddos（大犬）＝Bussu／ASE，Stellarium 沒有，
只標星點與標籤、不畫連線。逐字稿：04_腳本庫/A-29-薩丁尼亞地中海島嶼的農牧星空-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線：11 個星座照 Stellarium sardinian 原樣（Sos Bacheddos 跳過參宿二；北冕名照 sc.po 寫 Fiudas；
  仙后 Sa Trona 照 sc.po，片中不講，只在 L4 全部連線裡）。20 鏡下集預告＝Stellarium ruelle 的獅子座（A-30），琥珀細線。
  自訂層：銀河加亮（銀道 |b| ≤ 8 的半透明帶，17 鏡）、單星光暈（天狼、五車二、軒轅十四、天津四、北極星）。

參數（依本集逐字稿重新評估，不照抄 A-23／A-27）
  lst = 150 → 長圖 x＝wrap(150−RA)：獅子座鐮刀 x −5…+3.5（軒轅十四 −2.1）＝走廊 x＝0；
             12 鏡從鐮刀沿走廊往上（T）就直接到北盤盤心，不必先橫移回中心。
             冬季群在右（西）：獵戶 +61…+71、大犬 +45…+55、御夫 +60…+76、畢宿 +81…+85、昴宿 +93；
             切口 x＝±180 在 RA 330（寶瓶），長圖鏡頭都離它 ≥ 80。
             台北 4/23 20:00 LST 152.9 → 子午線 x −2.9：鐮刀正好在頭頂（19 鏡）。
  D_s = 56、D_r = 60 → 決定因素是 11 鏡的五車二（+46.0）：S 鏡頭 |cy|＋fov·8/9 ≤ D_s，fov 34 時 cy ≤ 25.3、
             畫面上緣 55.5，五車二離上緣 9.5 ≥ Reels 上緣安全區 13%（7.9）。節目表建議的 D_s 47 會讓五車二
             貼在畫面最上 1°（安全區裡）。代價：北斗（+49.3…+61.8）大半在縫合帶／填滿環，
             長圖上看不完整 → 12 鏡拆成 12（T：鐮刀→沿走廊上到盤心）＋12b（北盤 R：盤不轉、往盤心左下推到北斗）。
  D_fill = 0 → k＝1.9099、R_fill＝171.89（盤寬 ÷ 畫布寬＝0.954930；Canva 別設成同寬）；|x_t|＋R_fill ≤ 180 ✓。
             天鵝（+28…+45）、北冕（+26…+31）、英仙（+32…+56）都在盤的填滿環上（dec ≥ 0 都畫得到）。
  x_tN = x_tS = 0（Canva 可水平置中）
  北盤 rot：Sedilo 7/6 23:00 面北 +81.5°、7/7 02:00 +36.3°（13→14 鏡，逆時針＝時間前進）；
            北冕在上 +94°、英仙在上 −81°（15→16 鏡 −175°，gen_canva_pages 自動拆兩段，每段 < 170°）；
            17 鏡停在 −81° → 換回長圖「歸位」轉 81°（< 180 ✓）。12b 不轉（0°）：北斗就在鐮刀上方偏左（東）。

鏡頭路線
  01 長圖 金牛—獵戶 fov 40 → 畢宿 24（Su Pinnetu）→ 02 定格 C-A29-01 → 03 緩推 22
  → 04 拉遠 fov 46：小屋＋葡萄 → 往左（東）滑到獅子座鐮刀（fov 110 裝不下，見下）
  → 05 滑回畢宿 fov 22 → 06 往右（西）到昴宿 fov 16 → 07 往左下到獵戶 fov 30 → 08 定格 C-A29-02
  → 09 往左下到大犬 fov 30 → 10 定格 C-A29-07（金星兩個名字）→ 11 往上到御夫 fov 34
  → 12（T）鐮刀 fov 40 → 沿走廊上到北盤盤心 fov 50 →【換北盤】12b 北盤 0° 推到北斗
  → 13 轉到 Sedilo 7/6 23:00（天鵝）→ 14 轉到 7/7 02:00（天津四 45°→77°）＋C-A29-03
  → 15 轉到北冕在上 fov 30 → 16 再轉 175°（拆兩段）到英仙在上 fov 34 → 17 拉遠 fov 120（銀河加亮）＋圖卡 C-A29-04
  →【換長圖】（自動插歸位／北盤轉長圖／下移回鐮刀）18 滑到冬季群 fov 60（全部連線）＋圖卡 C-A29-05
  → 19 滑到獅子座 fov 60＋圖卡 C-A29-06 → 20 推近獅子座 fov 44（Ruelle 獅子連線，下集）

逐字稿要改的地方（素材時發現；已改進 v1 分鏡表）
  04 鏡「fov 22→110（昴宿到獅子座）」：直式畫面 fov 110 的高是 196，遠超出長圖帶 ±56（上下會露出縫合帶與空洞）
     → 改 S：拉遠到 fov 46 帶出小屋＋葡萄 → 往左滑到鐮刀；05 鏡滑回畢宿。
  12 鏡拆 12／12b（旁白照原文切開：「……就是農人的記號。」／「再往北……七個兄弟。」，12＝7＋5 秒）：
     北斗在縫合帶與填滿環，長圖上不完整（同 A-27 的 09／09b 拆法）。
  17 鏡「Z」→R（在北盤圖層組上拉遠）；18 鏡 fov 70→60、19 鏡背景 fov 80→60（S 鏡頭 fov ≤ 62 才不出長圖帶）。
  10 鏡「疊金星圖示＋兩個名字」做成概念圖 C-A29-07「吃晚飯的星」（傍晚層、清晨層）。
  01、03、05 標 Z 的實際是移動（S）；kind 依實際動作。

check_shots 的 ⚠（判斷後接受；寫在下方 WARN_OK）
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-29"
OUT = os.path.join(BASE, "05_素材/A-29_薩丁尼亞/_v4大畫布")
LST0 = 150.0
D_S, D_R, D_FILL = 56.0, 60.0, 0.0

SED = (40.183, 8.917)             # Sedilo（夏令時 UTC+2）
TPE = (25.0330, 121.5654)

WARN_OK = """
  13–17 R「起／迄格畫面含長圖側扇區」：13–17 都留在北盤圖層組上，不直接同框切回大畫布；
  12b 起格＝盤心 fov 50（盤緣圈內逐點重合），17→18 由 gen_canva_pages 自動插「歸位」（盤心 fov 50、0°）再換組。
"""


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when, refr=True):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure = 1010 if refr else 0
    o.temp = 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(lat, lon, tz, when):
    return math.degrees(_obs(lat, lon, tz, when).sidereal_time())


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return round(r + 360.0 if r <= -180.0 else r, 2)


T = {
    "13": ("Sedilo 7/6 23:00", SED, 2, "2027/7/6 23:00"),
    "14": ("Sedilo 7/7 02:00", SED, 2, "2027/7/7 02:00"),
    "19": ("台北 4/23 20:00", TPE, 8, "2027/4/23 20:00"),
}
LST_AT = {k: lst_at(*v[1], v[2], v[3]) for k, v in T.items()}
ROT = {k: rot_n(LST_AT[k]) for k in T}


def altaz(radec, where, tz, when):
    import ephem
    o = _obs(*where, tz, when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(radec[0]), math.radians(radec[1])
    s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, CAPELLA, SIRIUS, ALDEBARAN, REGULUS, DENEB, MIRFAK = 11767, 24608, 32349, 21421, 49669, 102098, 15863
ALCYONE, ALPHECCA, DENEBOLA = 17702, 76267, 57632
BELT = [26727, 26311, 25930]
CMA = [32349, 30324, 34045, 34444, 33579, 35904, 30122]   # 西方大犬座主星（只標星點，不畫連線）


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium sardinian 舊版 index.json；ruelle 獅子＝下集）
# ══════════════════════════════════════════════════════════════════
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_sc(cu):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"].split()[-1]] = [s for s in segs if len(set(s)) >= 2]
    return out


SD = load_sc("sardinian")
RU = load_sc("ruelle")
SEG_HUT, SEG_BUNCH, SEG_BRO, SEG_STICK, SEG_FOLD, SEG_DANCE = (SD["001"], SD["002"], SD["003"], SD["004"],
                                                               SD["005"], SD["006"])
SEG_SICKLE, SEG_DEER, SEG_CROSS, SEG_THRONE, SEG_MARIAS = SD["007"], SD["008"], SD["009"], SD["010"], SD["011"]
SEG_RLEO = RU["Leo"]
assert SEG_MARIAS == [BELT]
assert 26311 not in {h for s in SEG_STICK for h in s}            # 牧杖跳過參宿二（Stellarium 原樣）


def stars_of(segs):
    return sorted({h for s in segs for h in s})


HUT, BUNCH, BRO, STICK, FOLD, DANCE = map(stars_of, (SEG_HUT, SEG_BUNCH, SEG_BRO, SEG_STICK, SEG_FOLD, SEG_DANCE))
SICKLE, DEER, CROSS, RLEO = map(stars_of, (SEG_SICKLE, SEG_DEER, SEG_CROSS, SEG_RLEO))

LG_HUT = [(SEG_HUT, "amber", 1.2)]
LG_BUNCH = [(SEG_BUNCH, "purple", 1.0)]
LG_STICK = [(SEG_STICK, "blue", 1.1)]
LG_MARIAS = [(SEG_MARIAS, "amber", 1.4)]
LG_FOLD = [(SEG_FOLD, "green", 1.1)]
LG_SICKLE = [(SEG_SICKLE, "green", 1.2)]
LG_BRO = [(SEG_BRO, "amber", 1.1)]
LG_CROSS = [(SEG_CROSS, "red", 1.2)]
LG_DANCE = [(SEG_DANCE, "purple", 1.2)]
LG_DEER = [(SEG_DEER, "amber", 1.1)]
LG_THRONE = [(SEG_THRONE, "blue", 1.0)]
LG_RLEO = [(SEG_RLEO, "amber", 0.6)]
LG_ALL = (LG_HUT + LG_BUNCH + LG_STICK + LG_MARIAS + LG_FOLD + LG_SICKLE + LG_BRO + LG_CROSS + LG_DANCE
          + LG_DEER + LG_THRONE)
LINE_SETS = [(LG_HUT, "連線-Su Pinnetu石屋"), (LG_BUNCH, "連線-S'Udrone葡萄"), (LG_STICK, "連線-Sos Bacheddos牧杖"),
             (LG_MARIAS, "連線-Sas Tres Marias"), (LG_FOLD, "連線-Sa Mandra羊圈"), (LG_SICKLE, "連線-Sa Frache鐮刀"),
             (LG_BRO, "連線-Sos Sette Frades七兄弟"), (LG_CROSS, "連線-Sa Rughe十字"),
             (LG_DANCE, "連線-Su Ballu寡婦之舞"), (LG_DEER, "連線-Su Corru鹿角"), (LG_RLEO, "連線-Ruelle獅子（下集）")]
LINES_KEY = {"L4": "星座連線", "屋": "連線-Su Pinnetu石屋", "葡": "連線-S'Udrone葡萄", "杖": "連線-Sos Bacheddos牧杖",
             "瑪": "連線-Sas Tres Marias", "圈": "連線-Sa Mandra羊圈", "鐮": "連線-Sa Frache鐮刀",
             "兄": "連線-Sos Sette Frades七兄弟", "十": "連線-Sa Rughe十字", "舞": "連線-Su Ballu寡婦之舞",
             "角": "連線-Su Corru鹿角", "下": "連線-Ruelle獅子（下集）", "銀": "銀河加亮", "暈": "單星光暈"}
LINE_GROUPS = {"L4": LG_ALL, "屋": LG_HUT, "葡": LG_BUNCH, "杖": LG_STICK, "瑪": LG_MARIAS, "圈": LG_FOLD,
               "鐮": LG_SICKLE, "兄": LG_BRO, "十": LG_CROSS, "舞": LG_DANCE, "角": LG_DEER, "下": LG_RLEO,
               "銀": [], "暈": []}

MAINS = sorted({h for g in LG_ALL for s in g[0] for h in s} | set(CMA) | {POLARIS, CAPELLA, REGULUS})
HALO = [SIRIUS, CAPELLA, REGULUS, DENEB, POLARIS]


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


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def gal2eq(l, b):
    """銀道座標 → J2000 赤道座標"""
    l, b = math.radians(l), math.radians(b)
    ra_gp, dec_gp, l_ncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    sd = math.sin(b) * math.sin(dec_gp) + math.cos(b) * math.cos(dec_gp) * math.cos(l_ncp - l)
    dec = math.asin(sd)
    y = math.cos(b) * math.sin(l_ncp - l)
    x = math.sin(b) * math.cos(dec_gp) - math.cos(b) * math.sin(dec_gp) * math.cos(l_ncp - l)
    ra = (math.degrees(math.atan2(y, x)) + math.degrees(ra_gp)) % 360
    return ra, math.degrees(dec)


def custom_layers(m, S):
    mw = COLORS["mw"]

    def straw(s, pos, runs, disc):
        """17 鏡「麥稈之路」：銀道 |b| ≤ 8 的半透明帶（l 0–360 分四段，跨 RA 0 不會連錯）"""
        for l0 in (0, 90, 180, 270):
            ls = np.linspace(l0, l0 + 90, 46)
            for w, op in ((8.0, 0.07), (5.0, 0.10), (2.8, 0.13), (1.3, 0.16)):
                poly = [gal2eq(l, w) for l in ls] + [gal2eq(l, -w) for l in ls[::-1]]
                s.poly_fill(runs(poly), fill=mw, opacity=op)

    return [("銀河加亮", straw)]


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


def rot_top(m, ra, dec):
    """把 (ra, dec) 轉到北盤盤心正上方的角度（0.5° 解析度，收在 (−180, 180]）"""
    best = min((r / 2.0 for r in range(-359, 361)),
               key=lambda r: abs(math.atan2(disc_xy(m, ra, dec, r, True)[0],
                                            disc_xy(m, ra, dec, r, True)[1] - m.y_pole)))
    return round(best, 1)


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；外文照母音組算）
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
            n += max(1, len(re.findall(r"[aeiouyáéíóúèàâêîôûăș]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (HUT, "Su Pinnetu", "Su Pinnetu (sardinian 001)", "The Hut", "牧人石屋（畢宿 V＋畢宿五）", "amber",
     "石砌圓牆、木枝尖頂的牧人屋；Bussu 書介用複數 Pinnetos"),
    (BUNCH, "S'Udrone", "S'Udrone (sardinian 002)", "The Bunch", "一串葡萄（昴宿）", "purple",
     "Barbagia 叫 Su Gurdone（Bussu）"),
    (BUNCH, "Su Gurdone", "—", "The Bunch (Barbagia)", "也是一串（Barbagia）", "purple", "Bussu 2013；書介"),
    (BUNCH, "Cloșca cu pui", "Closca cu pui (romanian Ccp)", "The Hatching Hen with Her Chicks",
     "母雞帶小雞（羅馬尼亞）", "green", "A-23"),
    (STICK, "Sos Bacheddos", "Sos Bacheddos (sardinian 004)", "The Sticks", "牧杖（獵戶）", "blue",
     "Stellarium、ASE 都譯 The Sticks；連線跳過參宿二；「小牛」一說未親核，不用"),
    (BELT, "Sas Tres Marias", "Sas Tres Marias (sardinian 011)", "Three Marias", "三個瑪利亞（腰帶）", "amber",
     "西班牙、葡萄牙、拉丁美洲同名"),
    (CMA[1:], "Su Trubadore de sos Bacheddos", "—", "The Driver of the Sticks", "趕牧杖的人（大犬）", "red",
     "Bussu、ASE；Stellarium 沒有這個星座 → 只標星點與標籤、不畫連線"),
    ([SIRIUS], "S'Isteddu de Atzarzu", "Steel Star（po/sc.po）", "Steel Star", "鋼鐵之星（天狼星）", "white",
     "sc.po；ASE 另記 s'isteddu mannu（大星）"),
    (FOLD, "Sa Mandra", "Sa Mandra (sardinian 005)", "The Fence for Sheep", "羊圈（御夫）", "green",
     "sc.po：Sa Mandra / Su Achile；6 星閉合，五車五今屬金牛座 β"),
    ([CAPELLA], "Capella", "—", "Little she-goat (Latin)", "小母山羊（拉丁）", "blue", "希臘—羅馬：抱著母山羊的御夫"),
    (SICKLE, "Sa Frache", "Sa Frache (sardinian 007)", "The Sickle", "鐮刀（獅子座）", "green",
     "Bussu 書寫 Sa Farche；書介：代表農人"),
    (BRO, "Sos Sette Frades", "Sos Sette Frades (sardinian 003)", "The Seven Brothers", "七兄弟（北斗）", "amber",
     "sarabu 另記 Bòes「牛」"),
    (CROSS, "Sa Rughe de Santu Antinu", "Sa Rughe de Santu Antinu (sardinian 009)", "The Cross of St. Constantine",
     "聖君士坦丁的十字（天鵝）", "red", "Santu Antinu＝Sedilo 守護聖人；S'Ardia 7/6 傍晚、7/7 清晨"),
    (DANCE, "Su Ballu de sas Fiudas", "Su Ballu de sas Fiuda (sardinian 006；sc.po 作 Fiudas)", "The Dance of Widows",
     "寡婦之舞（北冕）", "purple", "index.json 漏 s，照 sc.po"),
    (DANCE, "Hora", "Hora (romanian)", "The Ring Dance (Romanian)", "圍圈舞（羅馬尼亞）", "green", "A-23"),
    (DEER, "Su Corru 'e Chervu", "Su Corru 'e Chervu (sardinian 008)", "The Deer Horn", "鹿角（英仙）", "amber",
     "薩丁尼亞紅鹿 Cervus elaphus corsicanus 只並列，不說星名由來"),
    (gal2eq(122.0, 1.0), "Sa Via de sa Paza", "—（Bussu 書介；ASE：s'andaina 'e paza）", "The Straw Road (Milky Way)",
     "麥稈之路（銀河）", "white", "Stellarium 沒有；paza＝麥稈（待親核辭典）"),
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
        it = dict(anchor(a), text=text, color=color, size=round(size, 3), dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    TT = {t[1]: t for t in TERMS}

    def sz(px, fov):
        """標籤字級：Canva 上 px 大小 → 畫布單位 size（fpx＝size·1.7·1080/fov）"""
        return px * fov / (m.fu * 1080.0)

    def term(name, fov, px1=64, px2=48, dx=0.0, dy=0.0, zh=None, zh_only=False, orig_only=False,
             a=None, disc=False, col=None, sub=None):
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
        if sub:                                       # 第三行（小字）
            out.append(item(a, sub, "white", sz(38, fov), dx, dy - gap / 2 - (48 + 38) * 0.62 * fov / 1080.0,
                            name + "-sub", disc))
        return out

    # ════════════════════ 構圖 ════════════════════
    def dpts(hips, rot, north=True):
        out = []
        for h in hips:
            ra, dec = (S[h][:2] if isinstance(h, int) else h)
            out.append(disc_xy(m, ra, dec, rot, north))
        return out

    def safe(cx, cy, fov, north=True):
        yc = yp if north else -yp
        return max(math.hypot(cx + sx * fov / 2, cy + sy * fov * 8 / 9 - yc)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(hips, rot, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None, north=True):
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while not safe(cx, cy, f, north):
            f *= 0.98
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

    ROT["15"] = rot_top(m, *centroid(DANCE, S))
    ROT["16"] = rot_top(m, *centroid(DEER, S))
    F01a = sfit(HUT + STICK, fov=40.0, dy=2.0)
    F01b = sfit(HUT, fov=24.0, dy=-1.5)
    F03 = sfit(HUT, fov=22.0, dy=-1.5)
    F04a = sfit(HUT + BUNCH, fov=46.0, dy=-2.0)
    F04b = sfit(SICKLE, fov=46.0, dy=-2.0)
    F05 = sfit(HUT, fov=22.0, dy=-2.5)
    F06 = sfit(BUNCH, fov=16.0, dy=-2.0)
    F07 = sfit(STICK, fov=30.0, dy=-1.0)
    F09 = sfit(CMA, fov=30.0, dy=-1.0)
    F11 = sfit(FOLD, fov=34.0, dy=-4.0)
    _sx, _sy = zip(*[(x_of(S[h][0]), S[h][1]) for h in SICKLE])
    F12a = (0.0, round((max(_sy) + min(_sy)) / 2 - 1.5, 2), 40.0, 0.0)     # T 起格：鐮刀在走廊上（x −5…+3.5）
    SW = (0.0, round(yp, 6), 50.0, 0.0)                                   # T 迄格＝北盤盤心（換組格）
    F12b = dfit(BRO, 0.0, pad=0.12, minfov=34.0)
    F13 = dfit(CROSS, ROT["13"], pad=0.10, fov=60.0)
    F14 = dfit(CROSS, ROT["14"], pad=0.10, fov=60.0)
    F15 = dfit(DANCE, ROT["15"], pad=0.10, fov=30.0, dy=-2.0)
    F16 = dfit(DEER, ROT["16"], pad=0.10, fov=34.0)
    F17 = (0.0, round(yp + 8.0, 2), 120.0, ROT["16"])
    while not safe(*F17[:3]):
        F17 = (F17[0], F17[1], round(F17[2] * 0.98, 1), F17[3])
    F18 = sfit(STICK + FOLD + HUT + CMA, fov=60.0, dx=-2.0)
    F19 = sfit(SICKLE + [DENEBOLA], fov=60.0, dy=-2.0)
    F20 = sfit(RLEO, fov=44.0, pad=0.08)
    print("\n── 構圖 ──")
    for nm in "F01a F01b F03 F04a F04b F05 F06 F07 F09 F11 F12a SW F12b F13 F14 F15 F16 F17 F18 F19 F20".split():
        print(f"  {nm} {locals()[nm]}")
    print("  旋轉：" + "、".join(f"{kk} {T[kk][0]} LST {LST_AT[kk]:.1f} → {ROT[kk]:+.1f}°" for kk in T)
          + f"、15 北冕在上 {ROT['15']:+.1f}°、16 英仙在上 {ROT['16']:+.1f}°")

    # ════════════════════ 標籤 ════════════════════
    # 長圖：dx/dy＝畫布方向（東在左，+dx＝往右＝往西）；盤：畫面方向（原生字不跟著盤轉）
    LB_HUT1 = term("Su Pinnetu", F01b[2], 60, 46, dy=-5.2)
    f4 = F04a[2]
    LB_HUT_W = term("Su Pinnetu", f4, 54, 42, dy=-7.0, zh="牧人的小屋")
    LB_BUNCH_W = term("S'Udrone", f4, 54, 42, dy=6.5, zh="一串葡萄")
    LB_SICKLE_W = term("Sa Frache", f4, 54, 42, dx=7.0, dy=-9.0, zh="農夫的鐮刀")
    LB_HUT = term("Su Pinnetu", F05[2], 64, 48, dy=-5.0, zh="牧人石屋", sub="石牆＋木枝尖頂")
    f6 = F06[2]
    LB_BUNCH = term("S'Udrone", f6, 64, 48, dy=2.6, zh="一大串葡萄")
    LB_BUNCHX = (term("Su Gurdone", f6, 48, 38, dx=0.0, dy=-2.9, zh="Barbagia：也是一串")
                 + term("Cloșca cu pui", f6, 44, 36, dx=0.0, dy=-4.9, zh="羅馬尼亞：母雞帶小雞"))
    f7 = F07[2]
    LB_STICK = (term("Sos Bacheddos", f7, 64, 48, dx=0.0, dy=12.0, zh="牧杖")
                + term("Sas Tres Marias", f7, 52, 42, dx=-8.5, dy=-3.5, zh="三個瑪利亞"))
    f9 = F09[2]
    LB_DRIVER = (term("Su Trubadore de sos Bacheddos", f9, 52, 46, dx=0.0, dy=-11.5, zh="趕牧杖的人",
                      sub="依 Bussu，非 Stellarium")
                 + term("S'Isteddu de Atzarzu", f9, 48, 40, a=[SIRIUS], dx=0.0, dy=3.2, zh="鋼鐵之星"))
    f11 = F11[2]
    LB_FOLD = (term("Sa Mandra", f11, 64, 48, dx=0.0, dy=-15.5, zh="羊圈")
               + term("Capella", f11, 44, 36, dx=7.5, dy=-2.0, zh="小母山羊（拉丁）"))
    LB_SICKLE = term("Sa Frache", F12a[2], 64, 48, dx=9.5, dy=-7.0, zh="鐮刀・農人的記號")
    f12b = F12b[2]
    LB_BRO = term("Sos Sette Frades", f12b, 64, 48, dx=0.0, dy=-16.0, zh="七兄弟", disc=True)
    f13 = F13[2]
    LB_CROSS = term("Sa Rughe de Santu Antinu", f13, 56, 48, dx=0.0, dy=-25.0, zh="聖君士坦丁的十字", disc=True)
    f15 = F15[2]
    LB_DANCE = (term("Su Ballu de sas Fiudas", f15, 60, 46, dx=0.0, dy=6.8, zh="寡婦們在跳舞", disc=True)
                + term("Hora", f15, 44, 36, dx=0.0, dy=-6.2, zh="羅馬尼亞：圍圈舞", disc=True))
    f16 = F16[2]
    LB_DEER = term("Su Corru 'e Chervu", f16, 64, 48, dx=8.0, dy=-22.0, zh="一支鹿角", disc=True)
    f17 = F17[2]
    LB_STRAW = term("Sa Via de sa Paza", f17, 64, 48, dx=14.0, dy=0.0, zh="麥稈之路", disc=True)
    f18 = F18[2]
    LB_ALL_W = [item(a, zh.split("（")[0], col, sz(46, f18), dx, dy, nm)
                for a, nm, zh, col, dx, dy in (
                    (HUT, "Su Pinnetu", "牧人石屋", "amber", -3.0, -5.0),
                    (BUNCH, "S'Udrone", "一串葡萄", "purple", 0.0, 3.0),
                    (STICK, "Sos Bacheddos", "牧杖", "blue", 9.5, 0.0),
                    (FOLD, "Sa Mandra", "羊圈", "green", 0.0, -9.5),
                    (CMA[1:], "Su Trubadore", "趕牧杖的人", "red", 3.0, 4.5))]

    label_sets = [(LB_HUT1, "小屋-開場"), (LB_HUT_W, "小屋-遠景"), (LB_BUNCH_W, "葡萄-遠景"),
                  (LB_SICKLE_W, "鐮刀-遠景"), (LB_HUT, "小屋"), (LB_BUNCH, "葡萄"), (LB_BUNCHX, "葡萄-跨文化"),
                  (LB_STICK, "牧杖與三個瑪利亞"), (LB_DRIVER, "趕牧杖的人與鋼鐵之星"), (LB_FOLD, "羊圈"),
                  (LB_SICKLE, "鐮刀"), (LB_BRO, "七兄弟"), (LB_CROSS, "聖君士坦丁的十字"),
                  (LB_DANCE, "寡婦之舞"), (LB_DEER, "鹿角"), (LB_STRAW, "麥稈之路"), (LB_ALL_W, "星名-遠景")]
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
    MARKS = [(MAINS, "主角星白點", "dot"), (HALO, "單星光暈", "ring")]
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
        dict(code="01", kind="S", sec=11, north=True, frames=[F01a, F01b], layers=["屋"],
             labels_start=[], labels=[], labels_end=ls("小屋-開場"),
             vo="上週在印度，畢宿五是月亮最愛的妻子。往西到地中海的薩丁尼亞：同一片星空，牧人看見——一間石頭小屋。",
             card="一間石頭小屋",
             note=f"長圖 金牛—獵戶 fov {F01a[2]:.0f} → 推近畢宿 fov {F01b[2]:.0f}；Su Pinnetu（琥珀，畢宿 V＋畢宿五閉合一圈）淡入；"
                  "迄格標籤 Su Pinnetu／牧人石屋；開場字卡"),
        dict(code="02", kind="S", sec=12, north=True, frames=[F01b], layers=["屋"], labels=ls("小屋-開場"),
             overlay="C-A29-01_薩丁尼亞", overlay_layers=["地圖層", "數字層"],
             vo="薩丁尼亞在義大利西邊，是地中海第二大島；到今天，島上的羊大約是人的兩倍。這套星座，用的是島中部小鎮 Sedilo 的方言。",
             card="羊比人多的島",
             note="長圖定格；疊 C-A29-01（地圖層：地中海手描示意、薩丁尼亞、Sedilo、Barbagia → 數字層：綿羊約 307 萬／人約 157 萬）"),
        dict(code="03", kind="S", sec=13, north=True, frames=[F01b, F03], layers=["屋"], labels=ls("小屋-開場"),
             vo="這些星名，由 Tonino Bussu 與 Marco Puddu 整理自民間；二〇一七年，Sedilo 的業餘天文家 Giuseppe Putzolu，把它們放進 Stellarium。",
             card="三個人，留下一套星名",
             note=f"畢宿緩推 fov {F01b[2]:.0f}→{F03[2]:.0f}（避免 25 秒靜止）；三個名字以原生小字條列（無照片）"),
        dict(code="04", kind="S", sec=12, north=True, frames=[F03, F04a, F04b], layers=["屋", "葡", "鐮"],
             labels_start=[], labels=ls("小屋-遠景", "葡萄-遠景"), labels_end=ls("鐮刀-遠景"),
             vo="Bussu 的書，把這些星名讀成島上的生活：牧人的小屋、葡萄農的一串葡萄、農夫的鐮刀；三種營生，都寫在天上。",
             card="小屋・葡萄・鐮刀",
             note=f"長圖拉遠 fov {F03[2]:.0f}→{F04a[2]:.0f}：Su Pinnetu（琥珀）＋S'Udrone（紫）→ 往左（東）滑到獅子座 Sa Frache（綠）；"
                  "（原寫 fov 110 一次裝下：直式畫面高 196，超出長圖帶 ±56，改平移）；三個小圖示（屋、葡萄、鐮）美宣原生元素"),
        dict(code="05", kind="S", sec=11, north=True, frames=[F04b, F05], layers=["屋"],
             labels_start=ls("鐮刀-遠景"), labels=ls("小屋"),
             vo="先看小屋：金牛座的 V 字，連上畢宿五，叫 Su Pinnetu：牧人用石頭疊起圓牆、再搭上木枝尖頂的小屋。",
             card="石牆、木枝尖頂",
             note=f"長圖滑回畢宿 fov {F05[2]:.0f}；Su Pinnetu 標籤（原文＋中譯＋小字「石牆＋木枝尖頂」）；"
                  "pinnetu 牧人屋照片／線稿美宣另尋授權圖"),
        dict(code="06", kind="S", sec=14, north=True, frames=[F05, F06], layers=["葡"],
             labels_start=ls("小屋"), labels=ls("葡萄"), labels_end=ls("葡萄", "葡萄-跨文化"),
             vo="旁邊的昴宿，叫 S'Udrone：一大串葡萄；島中東部的山區 Barbagia，叫它 Su Gurdone，也是一串。羅馬尼亞人在這裡看見母雞帶小雞，薩丁尼亞結的是葡萄。",
             card="一串葡萄，不是母雞",
             note=f"長圖往右（西）到昴宿 fov {F06[2]:.0f}；S'Udrone（紫）；迄格跨文化小字：Barbagia Su Gurdone、羅馬尼亞 Cloșca cu pui"),
        dict(code="07", kind="S", sec=11, north=True, frames=[F06, F07], layers=["杖", "瑪"],
             labels=ls("牧杖與三個瑪利亞"),
             vo="再往下，獵戶座叫 Sos Bacheddos：一根根牧杖；腰帶三顆另有名字：Sas Tres Marias，三個瑪利亞，跟西班牙和拉丁美洲一樣。",
             card="牧杖與三個瑪利亞",
             note=f"長圖往左下滑到獵戶 fov {F07[2]:.0f}；Sos Bacheddos（藍，7 星：跳過參宿二）＋Sas Tres Marias（琥珀，腰帶）"),
        dict(code="08", kind="S", sec=13, north=True, frames=[F07], layers=["杖", "瑪"], labels=ls("牧杖與三個瑪利亞"),
             overlay="C-A29-02_夏夜牧羊鐘", overlay_layers=["葡萄層", "牧杖層", "晨光層"],
             vo="這幾根牧杖，是牧人的夜間時鐘。夏天，羊群在夜裡吃草；後半夜，先看到那串葡萄爬上來，接著 Sos Bacheddos 露臉，就該把羊趕回圈了。",
             card="夏夜的牧羊鐘",
             note="長圖定格；疊 C-A29-02（Sedilo 8/16–17 夜，東方地平：葡萄層 00:00 昴宿升 → 牧杖層 03:22 腰帶升 → "
                  "晨光層 04:55 天文晨光，參宿二 17°、參宿六 9°；標「地平升起時刻，實際看見再晚一些」）"),
        dict(code="09", kind="S", sec=10, north=True, frames=[F07, F09], layers=["暈"],
             labels=ls("趕牧杖的人與鋼鐵之星"),
             vo="跟在後頭的大犬座，叫 Su Trubadore de sos Bacheddos：趕牧杖的人；最亮的天狼星，叫「鋼鐵之星」。",
             card="趕牧杖的人",
             note=f"長圖往左下（東南）滑到大犬 fov {F09[2]:.0f}；只標星點與標籤、不畫連線（小字「依 Bussu，非 Stellarium」）；"
                  "天狼星光暈＋S'Isteddu de Atzarzu／鋼鐵之星"),
        dict(code="10", kind="S", sec=12, north=True, frames=[F09], layers=["暈"], labels=ls("趕牧杖的人與鋼鐵之星"),
             overlay="C-A29-07_吃晚飯的星", overlay_layers=["傍晚層", "清晨層"],
             vo="金星也是時鐘：傍晚的金星叫 Isteddu Chenadorzu，字面是「吃晚飯的星」；清晨的那顆，叫 S'Isteddu 'e Impuddile，就是晨星。",
             card="吃晚飯的星",
             note="長圖定格（大犬）；疊 C-A29-07（傍晚層：西方地平＋金星、Isteddu Chenadorzu／吃晚飯的星 → "
                  "清晨層：東方地平＋金星、S'Isteddu 'e Impuddile／晨星；小字「新版 Stellarium 26.x 才收」）"),
        dict(code="11", kind="S", sec=12, north=True, frames=[F09, F11], layers=["圈", "暈"], labels=ls("羊圈"),
             labels_start=ls("趕牧杖的人與鋼鐵之星"),
             vo="往北，御夫座叫 Sa Mandra，羊圈。希臘人在這裡看見抱著母山羊和小羊的御夫；薩丁尼亞人看見的，是圈羊的柵欄。",
             card="不是山羊，是羊圈",
             note=f"長圖往右上（西北）滑到御夫 fov {F11[2]:.0f}；Sa Mandra（綠，6 星閉合）；小字 Capella＝小母山羊（拉丁）"),
        dict(code="12", kind="T", sec=7, north=True, frames=[F12a, SW], layers=["鐮"],
             labels_start=ls("鐮刀"), labels=ls("鐮刀"), labels_end=[],
             vo="春夜頭頂上的獅子座，那把反寫問號的鐮刀，叫 Sa Frache，就是農人的記號。",
             card="農人的鐮刀",
             note=f"長圖（鏡頭間滑到獅子座，鐮刀在走廊 x＝0）Sa Frache（綠）fov {F12a[2]:.0f} → T 沿走廊往上到北盤盤心 fov {SW[2]:.0f}"
                  "（換組格；迄格不開標籤）"),
        dict(code="12b", kind="R", sec=5, north=True, frames=[SW, F12b], layers=["鐮", "兄"],
             labels_start=[], labels=ls("七兄弟"),
             vo="再往北，北斗七星叫 Sos Sette Frades：七個兄弟。",
             card="北斗＝七兄弟",
             note=f"【換組】長圖→北盤（同框換組：12 迄格＝盤心 fov 50）；北盤不轉（0°），往盤心左下推到北斗 fov {F12b[2]:.0f}："
                  "Sos Sette Frades（琥珀）"),
        dict(code="13", kind="R", sec=16, north=True, frames=[F12b, F13], layers=["十", "暈"],
             labels_start=ls("七兄弟"), labels=ls("聖君士坦丁的十字"),
             vo="天鵝座的大十字，叫 Sa Rughe de Santu Antinu：聖君士坦丁的十字。他是 Sedilo 的守護聖人，每年七月六日傍晚、七日清晨，鎮上都為他辦賽馬，叫 S'Ardia。",
             card="聖君士坦丁的十字",
             note=f"北盤轉到 {T['13'][0]} 面北（{ROT['13']:+.1f}°）、移到天鵝座 fov {F13[2]:.0f}：Sa Rughe（紅，十字）；"
                  "S'Ardia 賽馬照片美宣另尋授權圖"),
        dict(code="14", kind="R", sec=13, north=True, frames=[F13, F14], layers=["十", "暈"],
             labels=ls("聖君士坦丁的十字"),
             overlay="C-A29-03_賽馬之夜", overlay_layers=["地平層", "爬升層"],
             vo="傳說君士坦丁打仗前，大白天在太陽上方，看見一個光的十字。七月的深夜，天鵝座這座十字，正好高掛在賽馬小鎮的頭頂。",
             card="天上的十字",
             note=f"北盤 {T['13'][0]}→{T['14'][0]}（{ROT['13']:+.1f}°→{ROT['14']:+.1f}°，逆時針＝時間前進；天津四 45°→77°）；"
                  "迄格疊 C-A29-03（地平層：Sedilo 東北方地平線剪影＋23:00 天鵝 → 爬升層：02:00 天鵝＋軌跡；"
                  "角落小字「傳說：白天、太陽上方的光十字」）"),
        dict(code="15", kind="R", sec=11, north=True, frames=[F14, F15], layers=["舞"],
             labels=ls("寡婦之舞"),
             vo="北冕座那半圈小星，叫 Su Ballu de sas Fiudas：寡婦們在跳舞；羅馬尼亞人也說，那是一場圍成圈的 Hora 舞。",
             card="寡婦之舞",
             note=f"北盤轉到北冕在上（{ROT['15']:+.1f}°）fov {F15[2]:.0f}（北冕在盤的填滿環上）：Su Ballu（紫，半圓）；"
                  "跨文化小字 羅馬尼亞 Hora（A-23）"),
        dict(code="16", kind="R", sec=10, north=True, frames=[F15, F16], layers=["角"],
             labels_start=ls("寡婦之舞"), labels=ls("鹿角"),
             vo="英仙座叫 Su Corru 'e Chervu：一支鹿角。到今天，山裡還住著體型偏小的薩丁尼亞紅鹿。",
             card="英仙座：一支鹿角",
             note=f"北盤再轉 {ROT['16'] - ROT['15']:+.1f}°（逆時針；逐頁表自動拆兩段，每段 < 170°）到英仙在上（{ROT['16']:+.1f}°）"
                  f"fov {F16[2]:.0f}：Su Corru 'e Chervu（琥珀，分叉線）"),
        dict(code="17", kind="R", sec=13, north=True, frames=[F16, F17], layers=["角", "十", "銀"],
             labels_start=ls("鹿角"), labels=ls("麥稈之路"),
             overlay="C-A29-04_麥稈之路",
             vo="銀河呢？叫 Sa Via de sa Paza：麥稈之路。從土耳其、波斯到亞美尼亞，好多地方都說銀河是一路灑落的麥稈；薩丁尼亞，也是其中之一。",
             card="（留空：圖卡自帶標題）",
             note=f"北盤 {ROT['16']:+.1f}° 拉遠 fov {F16[2]:.0f}→{F17[2]:.0f}（銀河加亮層淡入：天鵝—仙后—英仙一路）；"
                  "迄格疊 9:16 圖卡 C-A29-04「麥稈之路」（可存圖）"),
        dict(code="18", kind="S", sec=15, north=True, frames=[F18], layers=["L4"], labels=ls("星名-遠景"),
             overlay="C-A29-05_薩丁尼亞星名小辭典",
             vo="這些星名，每個村子的說法都不一樣，很多只剩老人家記得。二〇二六年，有位薩丁尼亞天文學家，還公開請島民幫忙，把快被忘掉的星座找回來。",
             card="幫忙找回星座",
             note=f"【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移回鐮刀）→ 滑到冬季群 fov {F18[2]:.0f}（全部連線＋中文星名）；"
                  "前 11 秒只放字卡；最後 4 秒疊 9:16 圖卡 C-A29-05「薩丁尼亞星名小辭典」（可存圖；旁白講完才出）"),
        dict(code="19", kind="S", sec=16, north=True, frames=[F19], layers=["鐮"], labels=[],
             overlay="C-A29-06_這週末抬頭看",
             vo="這週末在台灣：天黑後抬頭，鐮刀 Sa Frache 就在頭頂，北方高掛七兄弟；西邊的小屋和牧杖，天一黑就很低了，要趁早看；東邊，寡婦之舞已經升起，趁月亮出來前看。",
             card="（留空：圖卡自帶標題）",
             note=f"長圖滑到獅子座 fov {F19[2]:.0f}（背景）；主畫面＝9:16 圖卡 C-A29-06「這週末抬頭看」"
                  "（台北 4/23 20:00 地平全天圖＋時刻表；可存圖）"),
        dict(code="20", kind="S", sec=9, north=True, frames=[F19, F20], layers=["下"], labels=[],
             vo="下週五，我們去一七八六年的巴黎：一位年輕天文學家，把星座的圖畫全拿掉，只留下線。",
             card="下集：一張只有線的星圖",
             note=f"長圖推近獅子座 fov {F19[2]:.0f}→{F20[2]:.0f}：Ruelle 獅子連線（琥珀細線，Stellarium ruelle，A-30 預覽）；端卡＋追蹤 CTA"),
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
    prev = None
    for sh in shots:                                   # Canva M&M：單段旋轉 < 180°（鏡頭內與鏡頭間）
        rs = [f[3] for f in sh["frames"]]
        if prev is not None and sh["kind"] == "R" and prev["kind"] == "R":
            rs = [prev["frames"][-1][3]] + rs
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 178.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° 太接近 180°（Canva 可能反轉）")
            elif abs(b - a) >= 170.0:
                print(f"  ·  {sh['code']}：單段旋轉 {b - a:+.1f}° ≥ 170°，gen_canva_pages 會自動拆頁")
        prev = sh
    print(f"  17→18 換組歸位 {ROT['16']:+.1f}°→0°（{'< 180° ✓' if abs(ROT['16']) < 170 else '✗'}）")

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

    print("  Sedilo 天津四：" + "、".join(f"{T[kk][0]} {altaz(S[DENEB][:2], SED, 2, T[kk][3])}" for kk in ("13", "14")))
    print("  台北 4/23 20:00：" + "、".join(f"{n} {altaz(S[h][:2], TPE, 8, '2027/4/23 20:00')}" for n, h in
                                         (("軒轅十四", REGULUS), ("天樞", 54061), ("畢宿五", ALDEBARAN),
                                          ("貫索四", ALPHECCA))))
    print(f"  x：昴宿 {x_of(S[ALCYONE][0]):+.1f}、畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、參宿二 {x_of(S[26311][0]):+.1f}、"
          f"天狼 {x_of(S[SIRIUS][0]):+.1f}、五車二 {x_of(S[CAPELLA][0]):+.1f}、軒轅十四 {x_of(S[REGULUS][0]):+.1f}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Cloșca cu pui", 中譯="母雞帶小雞（羅馬尼亞，A-23）", 英文="The Hatching Hen", 顏色="green"),
                         dict(原文="Hora", 中譯="圍圈舞（羅馬尼亞，A-23）", 英文="The Ring Dance", 顏色="green"),
                         dict(原文="Capella", 中譯="小母山羊（拉丁）", 英文="Little she-goat", 顏色="blue")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": ROT, "lst0": LST0},
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
