# -*- coding: utf-8 -*-
"""A-27 曼達爾：同一片海的另一套星圖｜大畫布 v4.6（北盤＋南盤雙主秀＋長圖，南島雙聯集・下）

論點：曼達爾漁夫的星座幾乎都在報季風與魚（Rasyid, Hidayat & Orchiston 2021）。跟隔壁的布吉斯大半相同
（斜屋／瘸腿的房子、寡婦、魟魚、鯊魚、銀河的龍、金星的豬），真正分家的是北斗：布吉斯看成船、
把斗口叫「曼達爾的寡婦」；曼達爾把斗口放進一艘一路拉進天龍、接到牧夫的船，加上三個漁夫、兩件漁具＝漁網星。

來源：Stellarium mandar（舊版 stellarium-skycultures-master；Doina Bucur，依 Rasyid et al. 2021；6 組連線）、
bugis（同作者）。逐字稿：04_腳本庫/A-27-曼達爾同一片海的另一套星圖-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線：斜屋 001、鯊魚 002、魟魚 003、漁網船身 004 第一段、三星一組 005、寡婦 006 照 Stellarium mandar。
  例外（照論文 Fig. 18.7）：漁網星的漁夫 δ ε ζ UMa、漁具 γ η UMa 畫成獨立的點（自訂層「漁夫與漁具」），
  不畫 Stellarium 加的 γ–δ、ζ–η 短線。鯊魚依旁白順序拆成背鰭／頭／肚子／尾四層（同一條閉合線切開，點不變）。
  布吉斯「船」照 bugis 006（北斗七星＋ψ UMa＋小熊 β γ）、「曼達爾的寡婦」照 bugis 004（天樞—天璇）。
  14 鏡下集預告的北斗（白）＝標準北斗七星連線（不屬任何一個文化，X-03 會換成各文化）。
  自訂層：銀河龍加亮（銀道 l −50…+30、|b| ≤ 7 的半透明帶，09b 鏡）、漁夫與漁具（綠／紅圈點）。

參數（依本集逐字稿重新評估，不照抄 A-26）
  lst = 180 → 走廊 x＝0 在 RA 180：往北經過北斗斗身（天權 RA 184、x −4），往南經過南十字（RA 183–188）。
             長圖只用在 09、09b 鏡：昴宿 x +123、π Ori +107、腰帶 +96、銀心 RA 266 → x −86；
             切口 x＝±180 在 RA 0（雙魚—鯨魚），離兩段都很遠。
  D_s = 45、D_r = 49 → 決定因素是北盤：漁網星 11 顆最南是搖光 +49.3、θ Boo +51.9，D_r 49 讓整張漁網都在盤本體；
             斜屋（δ Cen −50.7…γ Cru −57.1…α Cru −63.1）、寡婦（−60.4、−60.8）也都在南盤本體。
             長圖帶 |dec| < 45 只要容下昴宿 +24、獵戶、人馬—天蠍銀河段（09b 構圖 |cy|＋fov·8/9 ≤ 45）。
             k＝1.3975。
  D_fill = −30 → R_fill＝167.7（盤寬 ÷ 畫布寬＝0.9316；Canva 別設成同寬）；|x_t|＋R_fill ≤ 180 ✓。
             南盤要收到天蠍頭（β¹ Sco −19.8）＋04 鏡 fov 80 的畫面角落，D_fill 0（R_fill 125.8）放不下；
             −30 讓南盤收到 dec +30、北盤收到 dec −30。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 rot＝lst_obs−lst（順時針＝時間前進）；北盤 rot＝−((lst_obs＋180−lst) mod 360)（逆時針），每段 M&M < 180°。
  北盤主角度＝Majene 4/15 00:00 面北（LST 201.6 → +158.4°；「四月半夜看見它」），01、07、08、14 鏡共用；
  08→09 換長圖時「歸位」轉回 0° 是 158.4°（< 180 ✓）。

鏡頭路線
  01 北盤 Z（布吉斯船淡出 → 漁網星淡入）→ 02、03 定格疊 C-A27-01、02
  → 04【硬切】南盤（選直式最省的角度：南十字在上、天蠍在下；不放地平線）魟魚、鯊魚、斜屋、寡婦＋布吉斯對照
  → 05【硬切】南盤 Majene 3/26 21:00→23:45 面南（山＝3.54°S），推近南十字
  → 06【硬切】南盤天蠍頭→天壇、人馬（轉到 3/27 04:00）（鯊魚四段）→ 定格 C-A27-03（月環＋魟鯊）
  → 07【硬切】北盤（往北）→ 08 推近北斗 → 定格 C-A27-03（亮四月）
  → 09【換長圖】（自動插歸位／北盤轉長圖／下移）昴宿→獵戶 → 定格 C-A27-03（亮六月）
  → 09b【硬切】長圖 人馬—天蠍銀河段＝龍 → 10 定格 C-A27-04 → 11 圖卡 C-A27-05 → 12 定格 C-A27-06
  → 13【換北盤】（自動插回中心／上移／長圖轉北盤）台北 3/26 20:00 面東北 → 定格 C-A27-07 → 13b 圖卡 C-A27-08
  → 14【硬切】北盤 Majene 角度 北斗（白）＋端卡

  逐字稿 09 鏡跨兩段長圖（昴宿—獵戶 x +96…+123、銀河 x −86），中間滑過去要橫越半張長圖 → 拆 09／09b，旁白照原文切；
  13 鏡要疊一張方形概念圖再換一張 9:16 圖卡，一鏡只能掛一組概念圖 → 拆 13／13b。秒數 17＝11＋6、28＝15＋13（照字數分，每格 ≤ 4.5）（總長 244 不變）。

硬切（判斷後接受）：05→06（中間是空天）、03→04（定格概念圖後換南盤新構圖）、04→05（04 不放地平線、05 起有 Majene 地平線，同框接會讓山跳一下；
  旁白換主角「南十字加上…」）、06→07「真正不一樣的，在北方」、09→09b「銀河是一條龍」、13b→14「下週五」
  ——北盤⇄南盤沒有共用的畫面，滑不過去。
check_shots 的 ⚠（判斷後接受；跑完逐條看過，寫在下方 WARN_OK）
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-27"
OUT = os.path.join(BASE, "05_素材/A-27_曼達爾/_v4大畫布")
LST0 = 180.0
D_S, D_R, D_FILL = 45.0, 49.0, -30.0

MAJ = (-3.54, 118.97)             # Majene（西蘇拉威西）
TPE = (25.0330, 121.5654)

WARN_OK = """
  01–08、13、13b、14 R「起／迄格畫面含長圖側扇區」：都不直接同框切回大畫布——01–03→04、06→07 北盤⇄南盤是【硬切】；
  08→09、12→13 換組由 gen_canva_pages 自動插「歸位／回中心」（盤心 fov ≤ 50，盤緣圈內逐點重合）再換組。
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


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return round((lst_obs - LST0 + 180.0) % 360.0 - 180.0, 2)


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return round(r + 360.0 if r <= -180.0 else r, 2)


T = {
    "N": ("Majene 4/15 00:00", MAJ, "2027/4/15 00:00"),
    "05a": ("Majene 3/26 21:00", MAJ, "2027/3/26 21:00"),
    "05b": ("Majene 3/26 23:45", MAJ, "2027/3/26 23:45"),
    "06": ("Majene 3/27 04:00", MAJ, "2027/3/27 04:00"),
    "13": ("台北 3/26 20:00", TPE, "2027/3/26 20:00"),
}
LST_AT = {k: lst_at(*v[1], 8, v[2]) for k, v in T.items()}
ROT = {"N": rot_n(LST_AT["N"]), "05a": rot_s(LST_AT["05a"]),
       "05b": rot_s(LST_AT["05b"]), "06": rot_s(LST_AT["06"]), "13": rot_n(LST_AT["13"])}


def altaz(hip_radec, where, when):
    import ephem
    o = _obs(*where, 8, when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(hip_radec[0]), math.radians(hip_radec[1])
    s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID = 54061, 53910, 58001, 59774, 62956, 65378, 67301
LAM_DRA, KAP_DRA, THUBAN, THE_BOO = 56211, 61281, 68756, 70497
POLARIS = 11767
ACRUX, MIMOSA, GACRUX, IMAI, DEL_CEN = 60718, 62434, 61084, 59747, 59196
RIGIL, HADAR = 71683, 68702
ANTARES, PI_SCO, DEL_SCO, BET_SCO = 80763, 78265, 78401, 78820
G_SCO, THE_SCO, ARA_A, ARA_B, ARA_T, TEL_A, EPS_SGR = 87261, 86228, 85792, 85258, 88714, 90422, 90185
DEL_SGR, GAM_SGR, SIG_SGR = 89931, 88635, 92855
ALCYONE, MINTAKA, ALNILAM, ALNITAK = 17702, 25930, 26311, 26727
PI3, PI4, PI5 = 22449, 22549, 22797
BETEL, RIGEL, ALDEBARAN = 27989, 24436, 21421
DIPPER = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]
BOAT = [MERAK, DUBHE, LAM_DRA, KAP_DRA, THUBAN, THE_BOO]
FISHERS = [MEGREZ, ALIOTH, MIZAR]
GEAR = [PHECDA, ALKAID]
NET = BOAT + FISHERS + GEAR
HOUSE = [DEL_CEN, GACRUX, IMAI, ACRUX, MIMOSA]
WIDOW = [RIGIL, HADAR]
BELT = [MINTAKA, ALNILAM, ALNITAK]
SHIELD = [PI3, PI4, PI5]
GC = (266.42, -29.01)              # 銀心（人馬 A*）


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium mandar／bugis index.json）
# ══════════════════════════════════════════════════════════════════
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_sc(cu):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"].split()[-1]] = [s for s in segs if len(set(s)) >= 2]
    return out


MD = load_sc("mandar")
BG = load_sc("bugis")
SEG_HOUSE, SEG_SHARK, SEG_RAY, SEG_NET, SEG_THREE, SEG_WIDOW = (MD["001"], MD["002"], MD["003"], MD["004"],
                                                                  MD["005"], MD["006"])
SEG_BOAT = [SEG_NET[0]]                                  # 船身；其餘兩段（γ–δ、ζ–η）是 Stellarium 加的，不畫
assert SEG_BOAT[0] == BOAT, SEG_BOAT
SEG_BSHIP, SEG_BMWID = BG["006"], BG["004"]
assert sorted({h for s in SEG_BMWID for h in s}) == sorted([DUBHE, MERAK])
_sh = SEG_SHARK[0]                                       # 17 星閉合線：G Sco 起，背鰭→頭→肚子→尾→回 G Sco
assert len(set(_sh)) == 17 and _sh[0] == _sh[-1] == G_SCO, _sh
_i = {h: i for i, h in enumerate(_sh[:-1])}
SEG_SH_FIN = [_sh[:_i[THE_SCO] + 1]]                     # G λ υ κ ι¹ θ Sco
SEG_SH_HEAD = [_sh[_i[THE_SCO]:_i[ARA_T] + 1]]           # θ Sco→α β θ Ara
SEG_SH_BELLY = [_sh[_i[ARA_T]:_i[EPS_SGR] + 1]]          # θ Ara→α Tel→ε Sgr
SEG_SH_TAIL = [_sh[_i[EPS_SGR]:]]                        # ε Sgr→δ σ φ λ μ δ γ² Sgr→G Sco
SEG_DIPPER = [[DUBHE, MERAK, PHECDA, MEGREZ, DUBHE], [MEGREZ, ALIOTH, MIZAR, ALKAID]]

LG_BOAT = [(SEG_BOAT, "blue", 1.2)]
LG_HOUSE = [(SEG_HOUSE, "amber", 1.2)]
LG_WIDOW = [(SEG_WIDOW, "green", 1.2)]
LG_RAY = [(SEG_RAY, "purple", 1.0)]
LG_SH_FIN, LG_SH_HEAD = [(SEG_SH_FIN, "red", 1.0)], [(SEG_SH_HEAD, "red", 1.0)]
LG_SH_BELLY, LG_SH_TAIL = [(SEG_SH_BELLY, "red", 1.0)], [(SEG_SH_TAIL, "red", 1.0)]
LG_SHARK = LG_SH_FIN + LG_SH_HEAD + LG_SH_BELLY + LG_SH_TAIL
LG_THREE = [(SEG_THREE, "amber", 1.3)]
LG_BSHIP = [(SEG_BSHIP, "amber", 1.0)]
LG_BMWID = [(SEG_BMWID, "red", 1.6)]
LG_DIPPER = [(SEG_DIPPER, "#E8ECF5", 1.0)]
LG_ALL = LG_BOAT + LG_HOUSE + LG_WIDOW + LG_RAY + LG_SHARK + LG_THREE
LINE_SETS = [(LG_BOAT, "連線-漁網星船身"), (LG_HOUSE, "連線-斜屋"), (LG_WIDOW, "連線-寡婦"),
             (LG_RAY, "連線-魟魚"), (LG_SH_FIN, "連線-鯊魚背鰭"), (LG_SH_HEAD, "連線-鯊魚頭"),
             (LG_SH_BELLY, "連線-鯊魚肚子"), (LG_SH_TAIL, "連線-鯊魚尾"), (LG_THREE, "連線-三星一組"),
             (LG_BSHIP, "連線-布吉斯的船"), (LG_BMWID, "連線-曼達爾的寡婦（布吉斯）"),
             (LG_DIPPER, "連線-北斗（下集）")]
LINES_KEY = {"L4": "星座連線", "船": "連線-漁網星船身", "屋": "連線-斜屋", "寡": "連線-寡婦", "魟": "連線-魟魚",
             "鰭": "連線-鯊魚背鰭", "頭": "連線-鯊魚頭", "肚": "連線-鯊魚肚子", "尾": "連線-鯊魚尾",
             "三": "連線-三星一組", "布船": "連線-布吉斯的船", "布寡": "連線-曼達爾的寡婦（布吉斯）",
             "斗": "連線-北斗（下集）", "漁": "漁夫與漁具", "龍": "銀河龍加亮", "暈": "單星光暈"}
LINE_GROUPS = {"L4": LG_ALL, "船": LG_BOAT, "屋": LG_HOUSE, "寡": LG_WIDOW, "魟": LG_RAY, "鰭": LG_SH_FIN,
               "頭": LG_SH_HEAD, "肚": LG_SH_BELLY, "尾": LG_SH_TAIL, "三": LG_THREE, "布船": LG_BSHIP,
               "布寡": LG_BMWID, "斗": LG_DIPPER, "漁": [], "龍": [], "暈": []}
SHARK_ALL = ["鰭", "頭", "肚", "尾"]

MAINS = sorted({h for g in LG_ALL for s in g[0] for h in s} | set(NET) | {ALCYONE, ANTARES, PI_SCO, DEL_SCO})


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
def gal2eq(l, b):
    """銀道座標 → J2000 赤道座標（IAU 1958 定義的 J2000 常數）"""
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

    def dragon(s, pos, runs, disc):
        for w, op in ((7.0, 0.08), (4.5, 0.11), (2.5, 0.15), (1.2, 0.18)):
            ls = np.linspace(-50, 30, 81)
            poly = [gal2eq(l, w) for l in ls] + [gal2eq(l, -w) for l in ls[::-1]]
            s.poly_fill(runs(poly), fill=mw, opacity=op)

    def fishers(s, pos, runs, disc):
        for hips, col in ((FISHERS, COLORS["green"]), (GEAR, COLORS["red"])):
            for h in hips:
                for p in pos(*S[h][:2]):
                    s.circle(p[0], p[1], 1.05, stroke=col, w=0.16, opacity=0.95)
                    s.circle(p[0], p[1], 0.55, fill=col, opacity=0.35)

    return [("銀河龍加亮", dragon), ("漁夫與漁具", fishers)]


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
    (NET, "Bittoéng Panjala", "Bittoéng Panjala (mandar 004)", "Fishing Net Star", "漁網星", "blue",
     "Rasyid et al. 2021 Fig. 18.7；船＋漁夫＋漁具"),
    (BOAT, "船", "—", "Boat (of the Fishing Net)", "船（漁網星的船身）", "blue",
     "論文只說 boat，沒給曼達爾語，片中只寫中文"),
    (FISHERS, "漁夫", "—", "Fishermen", "漁夫（天權、玉衡、開陽）", "green", "Rasyid et al. 2021"),
    (GEAR, "漁具", "—", "Fishing gear", "漁具（天璣、搖光）", "red", "Rasyid et al. 2021"),
    (HOUSE, "Sapo Kepang", "Bittoéng Sapo Kepang (mandar 001)", "Slanted House", "斜屋（南十字＋δ Cen）", "amber",
     "布吉斯 bola képpang（A-26 譯「瘸腿的房子」）"),
    (WIDOW, "Tuwallu", "Bittoéng Tuwallu (mandar 006)", "Widow", "寡婦（南門二、馬腹一）", "green",
     "老漁夫說紅寡婦 α Cen、綠寡婦 β Cen；布吉斯 bintoéng balué"),
    (stars_of(SEG_RAY), "Lambaru", "Bittoéng Lambaru (mandar 003)", "Stingray", "魟魚（天蠍頭到尾巴的彎）", "purple",
     "眼睛 δ、π Sco（論文誤植 η）；布吉斯 lambarué"),
    (stars_of(SEG_SHARK), "Mangiwang", "Bittoéng Mangiwang (mandar 002)", "Shark", "鯊魚（17 顆星）", "red",
     "背鰭 G Sco（論文誤植 ς）；布吉斯 bale mangngiweng"),
    ([ALCYONE], "Malunus", "Bittoéng Malunus", "Pleiades", "昴宿", "white", "名字沒有特別意思；飛魚季"),
    (BELT + SHIELD, "Tallu-tallu", "Bittoéng Tallu-tallu (mandar 005)", "Group of Three Stars", "三星一組",
     "amber", "腰帶＋π³ π⁴ π⁵ Ori；布吉斯 tanra tellué（只有腰帶）"),
    (GC, "Naga", "Bittoéng Naga", "Dragon (Milky Way)", "龍（銀河）", "white", "布吉斯 bintoéng nagaé"),
    (stars_of(SEG_BSHIP), "bintoéng kappala'é", "Bintoѐng Kappala'ѐ (bugis 006)", "Ship (Bugis)",
     "船（布吉斯，上集）", "amber", "A-26"),
    ([MERAK, DUBHE], "balu Mandara'", "Bintoѐng Balu Mandara' (bugis 004)", "The Mandar Widow (Bugis)",
     "曼達爾的寡婦（布吉斯）", "red", "Ammarell G；A-26 09 鏡"),
    (HOUSE[:0] + [DUBHE], "天樞", "—", "Dubhe", "天樞", "white", ""),
    ([MERAK], "天璇", "—", "Merak", "天璇", "white", ""),
    ([RIGIL], "紅寡婦", "—", "Alpha Centauri (red widow)", "紅寡婦（南門二）", "amber", "光譜 G2V＋K1V，偏黃"),
    ([HADAR], "綠寡婦", "—", "Hadar (green widow)", "綠寡婦（馬腹一）", "blue", "光譜 B1III，藍白"),
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
            out.append(item(a, sub, "white", sz(40, fov), dx, dy - gap / 2 - (48 + 40) * 0.62 * fov / 1080.0,
                            name + "-sub", disc))
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

    RN = ROT["N"]
    PHI_M, PHI_T = MAJ[0], TPE[0]
    F01a = dfit(NET + stars_of(SEG_BSHIP), RN, True, pad=0.12)
    F01b = dfit(NET, RN, True, pad=0.10)

    def bestrot(hips, north, pad=0.06):
        """直式畫面最省的盤角度（04 鏡不綁時刻：南十字與天蠍上下排）"""
        best = None
        for r in np.arange(-179.0, 180.0, 1.0):
            f = dfit(hips, round(float(r), 1), north, pad=pad, minfov=10.0)
            if best is None or f[2] < best[2]:
                best = f
        return best
    SOUTH4 = HOUSE + WIDOW + stars_of(SEG_RAY) + stars_of(SEG_SHARK)
    ROT["04"] = bestrot(SOUTH4, False, pad=0.10)[3]    # 先挑角度，再放寬留邊
    F04a = dfit(SOUTH4, ROT["04"], False, pad=0.28, dy=-2.5)   # 內容略往上：下緣 16% 是山
    F04b = dfit(SOUTH4, ROT["04"], False, pad=0.16, dy=-2.0)
    F05a = hfit(HOUSE + WIDOW, ROT["05a"], False, PHI_M, 84.0, fh=0.22)
    F05b = hfit(HOUSE + WIDOW, ROT["05b"], False, PHI_M, 84.0, fh=0.22)
    F05c = dfit(HOUSE + WIDOW, ROT["05b"], False, pad=0.10, fov=44.0, dy=-2.0)
    F06a = dfit(stars_of(SEG_RAY), round((ROT["05b"] + ROT["06"]) / 2, 2), False, pad=0.12, minfov=46.0)
    F06b = dfit(stars_of(SEG_SHARK) + stars_of(SEG_RAY), ROT["06"], False, pad=0.14)
    F07 = dfit(NET, RN, True, pad=0.16)
    F07b = dfit(NET, RN, True, pad=0.10)                     # 07 鏡慢慢推近：起格布吉斯、迄格曼達爾的船
    F08 = dfit(DIPPER, RN, True, pad=0.10, fov=34.0, dy=-1.0)
    F09a = sfit([ALCYONE, ALDEBARAN], fov=36.0, dy=-4.0)
    F09b = sfit(BELT + SHIELD + [BETEL, RIGEL], fov=36.0)
    G_X = x_of(GC[0])
    F09c = (round(G_X + 2.0, 2), round(-(m.Ds - 36.0 * 8 / 9 - 0.6), 2), 36.0, 0.0)
    F09c0 = (round(G_X + 6.0, 2), round(-(m.Ds - 38.0 * 8 / 9 - 0.6), 2), 38.0, 0.0)   # 09b 起格：略遠、往西一點
    F13 = hfit(NET, ROT["13"], True, PHI_T, 62.0, fh=0.14)
    F14a = dfit(DIPPER, RN, True, pad=0.10, fov=36.0)
    F14b = dfit(DIPPER, RN, True, pad=0.10, fov=60.0, dy=-3.0)
    print("\n── 構圖 ──")
    for nm in "F01a F01b F04a F04b F05a F05b F05c F06a F06b F07 F07b F08 F09a F09b F09c0 F09c F13 F14a F14b".split():
        print(f"  {nm} {locals()[nm]}")
    print("  旋轉：" + "、".join(f"{kk} {T[kk][0]} LST {LST_AT[kk]:.1f} → {v:+.1f}°" for kk, v in ROT.items() if kk in T)
          + f"、04（不綁時刻）{ROT['04']:+.1f}°")

    # ════════════════════ 標籤 ════════════════════
    # 長圖：dx/dy＝畫布方向（東在左，+dx＝往右＝往西）；盤：畫面方向（原生字不跟著盤轉）
    f1a, f1b = F01a[2], F01b[2]
    LB_BSHIP = term("bintoéng kappala'é", f1a, 60, 46, dy=-12.0, zh="上集：布吉斯的船", disc=True)
    LB_NET1 = term("Bittoéng Panjala", f1b, 64, 48, dy=-7.5, zh="漁網星", disc=True)
    f4 = F04b[2]
    LB_SOUTH = (term("Lambaru", f4, 56, 42, dx=-7.0, dy=4.0, zh="魟魚・布吉斯 lambarué", disc=True)
                + term("Mangiwang", f4, 56, 42, dx=-8.0, dy=-9.0, zh="鯊魚・布吉斯 bale mangngiweng", disc=True)
                + term("Sapo Kepang", f4, 56, 42, dx=-12.0, dy=0.0, zh="斜屋・布吉斯 bola képpang", disc=True)
                + term("Tuwallu", f4, 56, 42, dx=0.0, dy=-5.5, zh="寡婦・布吉斯 balué", disc=True))
    f5 = F05b[2]
    LB_HOUSE = (term("Sapo Kepang", f5, 60, 46, dy=9.0, zh="斜屋", disc=True)
                + term("Tuwallu", f5, 60, 46, dy=-9.0, zh="寡婦", disc=True))
    f5c = F05c[2]
    LB_HOUSE2 = (term("Sapo Kepang", f5c, 60, 46, dy=7.0, zh="斜屋", disc=True)
                 + [item([RIGIL], "紅寡婦", "amber", sz(52, f5c), -3.4, -2.6, "紅寡婦", disc=True),
                    item([HADAR], "綠寡婦", COLORS["blue"], sz(52, f5c), 3.0, -2.6, "綠寡婦", disc=True),
                    item(WIDOW, "老漁夫說：一紅一綠（光譜：偏黃／藍白）", "white", sz(38, f5c), 7.0, -6.6, "一紅一綠",
                         disc=True)])
    f6 = F06b[2]
    LB_FISH = (term("Lambaru", f6, 60, 46, dx=-8.0, dy=3.0, zh="魟魚", disc=True)
               + term("Mangiwang", f6, 60, 46, dx=0.0, dy=-11.0, zh="鯊魚・17 顆星", disc=True)
               + [item([G_SCO], "背鰭", "red", sz(40, f6), 2.6, 1.6, "背鰭", disc=True),
                  item([ARA_B], "頭", "red", sz(40, f6), 2.4, 0.0, "頭", disc=True),
                  item([TEL_A], "肚子", "red", sz(40, f6), -2.4, -1.6, "肚子", disc=True),
                  item([SIG_SGR], "尾", "red", sz(40, f6), -2.0, 1.6, "尾", disc=True)])
    f7 = F07[2]
    LB_BUGIS_N = (term("bintoéng kappala'é", f7, 56, 44, dx=6.0, dy=-9.0, zh="布吉斯：船", disc=True)
                  + term("balu Mandara'", f7, 56, 44, dx=6.0, dy=5.0, zh="布吉斯：曼達爾的寡婦", disc=True))
    LB_BOAT = (term("船", f7, 60, 0, dx=0.0, dy=5.5, zh="曼達爾：船", zh_only=True, disc=True)
               + [item([THE_BOO], "牧夫座 θ", "white", sz(40, f7), 0.0, -2.6, "θ Boo", disc=True),
                  item([THUBAN], "天龍座", "white", sz(40, f7), 0.0, 2.4, "天龍", disc=True)])
    f8 = F08[2]
    LB_NET = (term("Bittoéng Panjala", f8, 64, 48, dx=5.0, dy=8.0, zh="漁網星", a=[MERAK, DUBHE, PHECDA, MEGREZ], disc=True)
              + term("漁夫", f8, 56, 0, dy=-3.0, zh_only=True, disc=True)
              + [item([PHECDA], "漁具", "red", sz(48, f8), 0.0, -2.4, "漁具1", disc=True),
                 item([ALKAID], "漁具", "red", sz(48, f8), 0.0, -2.4, "漁具2", disc=True)])
    f9 = F09b[2]
    LB_PLEI = term("Malunus", F09a[2], 64, 48, dx=0.0, dy=-3.4, zh="昴宿・飛魚季")
    LB_THREE = (term("Tallu-tallu", f9, 64, 48, dx=-8.0, dy=-4.0, a=BELT, zh="三星一組")
                + [item(BELT, "腰帶", "amber", sz(40, f9), 3.2, -1.6, "腰帶"),
                   item(SHIELD, "盾牌", "amber", sz(40, f9), 3.2, 0.0, "盾牌")])
    f9c = F09c[2]
    LB_NAGA = term("Naga", f9c, 64, 48, dx=0.0, dy=9.0, zh="龍＝銀河")
    f13 = F13[2]
    LB_TPE = ([item([DUBHE], f"天樞 {altaz(S[DUBHE][:2], TPE, '2027/3/26 20:00')[0]:.0f}°", "white", sz(44, f13),
                    3.6, 0.0, "天樞"),
               item([MERAK], f"天璇 {altaz(S[MERAK][:2], TPE, '2027/3/26 20:00')[0]:.0f}°", "white", sz(44, f13),
                    3.6, 0.0, "天璇")]
              + term("Bittoéng Panjala", f13, 56, 44, dx=9.0, dy=-9.0, zh="台北 20:00・漁網星", disc=True))
    LB_TPE[0]["disc"] = LB_TPE[1]["disc"] = True
    f14 = F14b[2]
    LB_NEXT = [item(DIPPER, "北斗", "white", sz(64, f14), 0.0, 8.0, "北斗", disc=True)]

    label_sets = [(LB_BSHIP, "上集-布吉斯的船"), (LB_NET1, "漁網星-開場"), (LB_SOUTH, "南天-兩族對照"),
                  (LB_HOUSE, "斜屋與寡婦"), (LB_HOUSE2, "斜屋與一紅一綠"), (LB_FISH, "魟魚與鯊魚"),
                  (LB_BUGIS_N, "布吉斯的北斗"), (LB_BOAT, "曼達爾的船"), (LB_NET, "漁網星"),
                  (LB_PLEI, "昴宿"), (LB_THREE, "三星一組"), (LB_NAGA, "龍"), (LB_TPE, "台北-漁網星"),
                  (LB_NEXT, "北斗-下集")]
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
    MARKS = [(MAINS, "主角星白點", "dot"), ([RIGIL, HADAR, ALCYONE, POLARIS], "單星光暈", "ring")]
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
        dict(code="01", kind="R", sec=13, north=True, frames=[F01a, F01b], layers=["布船", "船", "漁"],
             labels_start=ls("上集-布吉斯的船"), labels=ls("漁網星-開場"), labels_end=ls("漁網星-開場"),
             vo="上週，布吉斯人在北斗上看見一艘船。今天沿著海岸往北，到蘇拉威西西岸：同一片星空，曼達爾漁夫看見——一張漁網。",
             card="同一個北斗：船，還是漁網",
             note=f"北盤（{T['N'][0]} 面北的角度 {RN:+.1f}°，不放地平線）Z fov {F01a[2]:.0f}→{F01b[2]:.0f}：起格開布吉斯「船」（琥珀，bugis 006）＋標籤 → "
                  "淡出；曼達爾漁網星淡入：船身（藍，天璇—天樞—λ Dra—κ Dra—右樞—θ Boo）、漁夫（綠圈：天權、玉衡、開陽）、"
                  "漁具（紅圈：天璣、搖光）；迄格標籤 Bittoéng Panjala／漁網星；開場字卡"),
        dict(code="02", kind="R", sec=22, north=True, frames=[F01b], layers=["船", "漁"], labels=[],
             overlay="C-A27-01_曼達爾的海", overlay_layers=["地圖層", "航線層", "季風層"],
             vo="曼達爾人住在蘇拉威西西岸，面對望加錫海峽。他們是漁夫，也是商人：東邊遠到摩鹿加、巴布亞，還有人一路開到澳洲北岸撈海參；西邊到爪哇、麻六甲。往西的船，六到九月乘東南季風出發，十二到三月，再乘西北季風回家。",
             card="乘著季風來回",
             note="北盤定格；疊 C-A27-01（地圖層：蘇拉威西西岸、望加錫海峽、Majene → 航線層：東到摩鹿加、巴布亞、澳洲北岸；"
                  "西到爪哇、麻六甲；北、南兩條細線 → 季風層：只畫在西航線上，6–9 月東南季風去、12–3 月西北季風回）；"
                  "傳統帆船照片美宣另尋授權圖"),
        dict(code="03", kind="R", sec=15, north=True, frames=[F01b], layers=["船", "漁"], labels=[],
             overlay="C-A27-02_資料從哪來", overlay_layers=["書目層"],
             vo="這套星圖，來自印尼萬隆理工學院的天文學家：他們訪問了一群七十歲以上的退休漁夫，二〇二一年發表。他們也發現，年輕一輩出海，已經不看星星了。",
             card="七十歲以上的老漁夫",
             note="北盤定格；疊 C-A27-02（書目文字卡：作者三人、2021、Springer 書名、受訪者七十歲以上；不翻拍書封）"),
        dict(code="04", kind="R", sec=18, north=False, cut=True, frames=[F04a, F04b],
             layers=["魟"] + SHARK_ALL + ["屋", "寡"], labels=ls("南天-兩族對照"),
             vo="說是另一套，其實跟鄰居很像：天蠍座從頭到尾巴的彎是一條魟魚，尾巴最末連螫針是鯊魚的背鰭；南十字是一間房子，旁邊兩顆亮星是寡婦——從名字到形狀，幾乎都跟布吉斯一樣。",
             card="鄰居的星座，大半相同",
             note=f"【硬切】北盤→南盤（定格概念圖之後的新構圖）：南盤 {ROT['04']:+.1f}°（＝面南、恆星時 {(ROT['04'] + LST0) % 360:.0f}° 的天空；"
                  f"選成直式畫面最省的角度：南十字在上、天蠍在下；不綁時刻、不放地平線）Z fov {F04a[2]:.0f}→{F04b[2]:.0f}：魟魚（紫，mandar 003）、鯊魚（紅，mandar 002 四段）、斜屋（琥珀，001）、"
                  "寡婦（綠，006）；每組標籤兩行：曼達爾原文（色）＋「中譯・布吉斯名」（白）"),
        dict(code="05", kind="R", sec=15, north=False, cut=True, horizon=[PHI_M], frames=[F05a, F05b, F05c],
             layers=["屋", "寡", "暈"], labels_start=ls("斜屋與寡婦"), labels=ls("斜屋與寡婦"),
             labels_end=ls("斜屋與一紅一綠"),
             vo="南十字加上半人馬座的一顆星，是一間「斜屋」：屋頂在上，兩根柱子一長一短。旁邊那兩顆亮星是「寡婦」，老漁夫說，一顆紅、一顆綠。看見它們，就找到南方。",
             card="斜屋＋寡婦＝南方",
             note=f"【硬切】（04 不放地平線，05 起有 Majene 地平線；同框接山會跳）南盤 Majene 面南 {T['05a'][0]}→{T['05b'][0]}"
                  f"（{ROT['05a']:+.1f}°→{ROT['05b']:+.1f}°；斜屋從東南爬到接近正南、α Cen 6.8°→24.7°；山＝3.54°S 南方地平線）"
                  "→ 推近南十字 fov 44：屋頂 δ Cen—γ Cru—δ Cru、短柱 β—γ Cru、長柱 α—δ Cru；迄格標籤換「紅寡婦／綠寡婦」"
                  "＋小字「老漁夫說：一紅一綠（光譜：偏黃／藍白）」"),
        dict(code="06", kind="R", sec=21, north=False, cut=True, horizon=[PHI_M], frames=[F06a, F06b],
             layers=["魟"] + SHARK_ALL, labels=ls("魟魚與鯊魚"),
             overlay="C-A27-03_季風漁汛曆", overlay_layers=["月環層", "魟鯊層"],
             vo="曼達爾的鯊魚畫得特別完整：背鰭、頭、肚子、尾巴，一共十七顆星。這兩條魚，是季風的預報。老漁夫說：十一月底，魟魚在清晨升起；十二月底，鯊魚跟著出來——西北季風要來了。這時漁船不出海，跑西邊的商船，乘風回家。",
             card="魟魚、鯊魚＝西北季風",
             note=f"【硬切】（斜屋→天蠍頭中間是空天，滑過去會有 6 秒空畫面；旁白換主角「曼達爾的鯊魚」）南盤天蠍頭 → 往下到天壇與人馬，同時轉到 {T['06'][0]}（{ROT['06']:+.1f}°，天蠍—人馬高掛、"
                  "山移出頁外）；鯊魚四段連線層照旁白順序依頁打開（背鰭→頭→肚子→尾，Canva 裡各層透明度 0→100）；"
                  "「季風的預報」起定格疊 C-A27-03（月環層：12 個月＋兩種季風 → 魟鯊層：亮 11 月底魟魚、12 月底鯊魚；漁網、昴宿兩格灰階）"),
        dict(code="07", kind="R", sec=20, north=True, cut=True, frames=[F07, F07b], layers=["布船", "布寡", "船"],
             labels_start=ls("布吉斯的北斗"), labels=ls("布吉斯的北斗"), labels_end=ls("曼達爾的船"),
             vo="真正不一樣的，在北方。上週說過，布吉斯人把北斗看成一艘船，還把斗口這兩顆叫「曼達爾的寡婦」。曼達爾人自己看呢？這兩顆也在一艘船上——只是船身不往斗柄走，而是一路拉進天龍座，接到牧夫座。",
             card="斗口兩顆：寡婦，還是船？",
             note=f"【硬切】南盤→北盤（往北）：北盤 {RN:+.1f}° fov {F07[2]:.0f}→{F07b[2]:.0f}（慢推）：布吉斯「船」（琥珀）＋「曼達爾的寡婦」（天樞—天璇，紅）→ "
                  "「曼達爾人自己看呢」起淡出；曼達爾船身（藍）沿天璇→天樞→λ Dra→κ Dra→右樞→θ Boo 依序畫出"
                  "（Canva：船身層用「擦除／線條」動畫或分兩頁淡入）；「接到牧夫座」落在 θ Boo"),
        dict(code="08", kind="R", sec=16, north=True, frames=[F07b, F08], layers=["船", "漁"],
             labels_start=ls("曼達爾的船"), labels=ls("漁網星"),
             overlay="C-A27-03_季風漁汛曆", overlay_layers=["四月層"],
             vo="北斗剩下的五顆：中間三顆是漁夫，兩頭各一顆是漁具。合起來叫 Bittoéng Panjala——漁網星。老漁夫說，四月半夜看見它，涼季就要來了，一種叫 bambang 的魚也會出現。",
             card="漁網＝船＋漁夫＋漁具",
             note=f"北盤推近北斗 fov {F07b[2]:.0f}→{F08[2]:.0f}：漁夫（綠圈）、漁具（紅圈）、船（藍）全開；漁夫／漁具是獨立的點（照論文 Fig. 18.7，"
                  "不畫 Stellarium 的 γ–δ、ζ–η 短線）；迄格標籤「Bittoéng Panjala／漁網星」；最後 3 秒定格疊 C-A27-03 四月層"
                  "（＝月環＋魟鯊＋亮 4 月漁網格的合成層）"),
        dict(code="09", kind="S", sec=11, north=True, frames=[F09a, F09b], layers=["三", "暈"],
             labels_start=ls("昴宿"), labels=ls("昴宿", "三星一組"), labels_end=ls("三星一組"),
             overlay="C-A27-03_季風漁汛曆", overlay_layers=["六月層"],
             vo="六月的清晨，昴宿回到東方，海峽裡的飛魚就多了；接著獵戶升上來，腰帶和盾牌各有三顆排成一線，叫「三星一組」。",
             card="昴宿＝飛魚季",
             note="【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）；長圖 S 從昴宿（Malunus，白細圈）滑到獵戶："
                  "三星一組（琥珀，mandar 005：腰帶＋π³ π⁴ π⁵ Ori 兩排；「盾牌」時亮 π 那排標籤）；"
                  "迄格定格疊 C-A27-03 六月層（月環＋魟鯊＋漁網＋亮 6 月昴宿格的合成層）"),
        dict(code="09b", kind="S", sec=6, north=True, cut=True, frames=[F09c0, F09c], layers=["龍"], labels=ls("龍"),
             vo="銀河是一條龍：漁夫靠它找漁場；龍不見了，就怕要起大風。",
             card="銀河＝龍",
             note="【硬切】（從獵戶 x +96 到人馬 x −86，要橫越半張長圖）長圖 人馬—天蠍銀河段：「銀河龍加亮」層（銀道 l −50…+30）"
                  "淡入＝Bittoéng Naga；不在金牛—獵戶那段（反銀心、最暗）加亮"),
        dict(code="10", kind="S", sec=15, north=True, frames=[F09c], layers=["龍"], labels=[],
             overlay="C-A27-04_金星兩個名字", overlay_layers=["海上層", "山上層"],
             vo="金星有兩個名字。清晨東方那顆，海上叫它「帶著太陽的星」：看見它，大約再一個鐘頭，太陽就到了。山上的人叫它「豬星」：看見它要小心，豬要出來找東西吃了。",
             card="帶著太陽的星｜豬星",
             note="長圖定格（銀河段當底）；疊 C-A27-04（海上層：海平線＋金星＋地平線下的太陽、Pambawa Allo → "
                  "山上層：山稜線＋金星＋豬的剪影、Bawi；不畫太陽、不標晨昏）"),
        dict(code="11", kind="S", sec=19, north=True, frames=[F09c], layers=["龍"], labels=[],
             overlay="C-A27-05_兩份星圖對照",
             vo="比一比兩份星圖：上週的布吉斯，上了岸還有犁、有雞、有薏苡稈；曼達爾記下來的星座，幾乎都在海上。不過研究者也提醒：他們只問了海邊的漁夫——內陸種稻的曼達爾人看見什麼，還沒有人去問。",
             card="只問了海邊的漁夫",
             note="長圖定格；疊 9:16 圖卡 C-A27-05（左布吉斯、右曼達爾；同名者連線；海上／岸上分色；可存圖），停 15 秒以上"),
        dict(code="12", kind="S", sec=16, north=True, frames=[F09c], layers=["龍"], labels=[],
             overlay="C-A27-06_Karama河谷", overlay_layers=["擴散層", "河谷層"],
             vo="兩族的星座這麼像，研究者認為，是因為都承自南島先民：大約四千年前從台灣南下。在西蘇拉威西的 Karama 河谷，考古學家挖到三千五百年前的聚落，和紅衣陶。",
             card="為什麼這麼像？南島先民",
             note="長圖定格；疊 C-A27-06（擴散層：台灣→菲律賓→蘇拉威西，同 A-26 C-A26-06 的路線 → 河谷層：推近西蘇拉威西，"
                  "Karama 河谷約 3,500 年前、Mamuju 內陸；Majene、曼達爾沿海）；紅衣陶照片美宣另尋授權圖"),
        dict(code="13", kind="R", sec=15, north=True, horizon=[PHI_T], frames=[F13], layers=["船", "漁"],
             labels=ls("台北-漁網星"),
             overlay="C-A27-07_同一刻兩個地方", overlay_layers=["台北層", "蘇拉威西層"],
             vo="今晚在台灣：八點往東北看，北斗——曼達爾漁網的那一頭——已經爬到四十多度高；同一個時間、同一個時區，蘇拉威西的漁夫看，斗口只有二十度上下，船尾還在海面下。",
             card="今晚：八點北斗",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）→ 台北 3/26 20:00 面北（{ROT['13']:+.1f}°；山＝台北北方地平線）："
                  "東北方漁網星（天樞 44°、天璇 47°、右樞 24°、θ Boo 19°）；「同一個時間」起定格疊 C-A27-07"
                  "（台北層：台北 20:00 面東北 → 蘇拉威西層：Majene 20:00 面北，天樞 17°、天璇 21°，右樞、θ Boo 在海平線下）"),
        dict(code="13b", kind="R", sec=13, north=True, horizon=[PHI_T], frames=[F13], layers=["船", "漁"],
             labels=ls("台北-漁網星"), overlay="C-A27-08_今晚抬頭看",
             vo="想看斜屋，要等到半夜，去墾丁往正南方找，而且大半不到十度；清晨五點到天亮前，東方最亮的那顆，就是帶著太陽的金星。",
             card="今晚：半夜斜屋、清晨金星",
             note="北盤定格（同 13 鏡）；疊 9:16 圖卡 C-A27-08「今晚抬頭看」（台北 3/26 20:00 北斗；23:16–01:11 鵝鑾鼻斜屋；"
                  "3/27 05:00–05:40 東方金星；可存圖），停 10 秒以上"),
        dict(code="14", kind="R", sec=9, north=True, cut=True, frames=[F14a, F14b], layers=["斗"],
             labels=ls("北斗-下集"),
             vo="下週五：同一把勺子，有人看成牛腿，有人看成棺架，還有人看成一夥強盜——北斗環球。",
             card="下集見｜北斗環球：一個勺子的十種人生",
             note=f"【硬切】（下集預告）北盤 {RN:+.1f}° Z fov 36→60，北斗七星（白）；「牛腿／棺架／強盜」三個剪影美宣依序閃過"
                  "（不畫）；端卡＋追蹤 CTA"),
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
    for nm in ("N", "13"):
        print(f"  {nm} 換組歸位 {ROT[nm]:+.1f}°→0°（< 180° ✓）" if abs(ROT[nm]) < 178 else f"  ✗ {nm} 旋轉 {ROT[nm]}")

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

    print("  台北 3/26 20:00：" + "、".join(f"{n} {altaz(S[h][:2], TPE, '2027/3/26 20:00')}" for n, h in
                                         (("天樞", DUBHE), ("天璇", MERAK), ("右樞", THUBAN), ("θ Boo", THE_BOO))))
    print("  Majene 3/26 21:00／23:45 α Cen：" + f"{altaz(S[RIGIL][:2], MAJ, '2027/3/26 21:00')}／"
          f"{altaz(S[RIGIL][:2], MAJ, '2027/3/26 23:45')}；十字架二 23:45 {altaz(S[GACRUX][:2], MAJ, '2027/3/26 23:45')}")
    print(f"  x：天權 {x_of(S[MEGREZ][0]):+.1f}、南十字 {x_of(S[ACRUX][0]):+.1f}、昴宿 {x_of(S[ALCYONE][0]):+.1f}、"
          f"參宿二 {x_of(S[ALNILAM][0]):+.1f}、銀心 {G_X:+.1f}；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="bintoéng kappala'é", 中譯="船（布吉斯，A-26）", 英文="Ship", 顏色="amber"),
                         dict(原文="balu Mandara'", 中譯="曼達爾的寡婦（布吉斯，A-26）", 英文="The Mandar Widow", 顏色="red"),
                         dict(原文="bola képpang", 中譯="瘸腿的房子（布吉斯，A-26）", 英文="Incomplete house", 顏色="amber")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": ROT, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL + LG_BSHIP + LG_BMWID,
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
