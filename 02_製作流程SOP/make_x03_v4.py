# -*- coding: utf-8 -*-
"""X-03 北斗環球：一個勺子的十種人生｜大畫布 v4.6（北盤主秀：一鏡一個文化）

論點：北斗七星六顆差不多亮、形狀好認，三千年前又比今天更靠近北天極——從埃及北部、希臘到中國整夜不落，
所以幾乎每個北半球文化都替它取了名字。片中依序唸十種：①牛的前腿（埃及）②車（北歐、東歐、中國、巴比倫、峇里）
③熊（荷馬、梵文）④七個人（印度七仙人、蒙古、黑腳族）⑤棺架（阿拉伯）⑥強盜（馬其頓）⑦大蛇（圖卡諾）
⑧船（布吉斯）⑨漁網（曼達爾）⑩獵物（埃文基、因紐特）。之後：今晚台北 4/2 → 下集斗柄找大角。

來源：Stellarium 兩份 skycultures（stellarium-master／stellarium-skycultures-master）的 index.json：
  egyptian 001、norse 005、belarusian 001、chinese 039、babylonian_mulapin 014、balinese PeSu、
  greek_almagest UMa、indian Sapt（只在 stellarium-master）、macedonian 001、tukano 011、bugis 006、
  mandar 004、inuit 006；埃文基照 A-08 v2（斗口＝駝鹿的腳、斗柄＝獵人）；阿拉伯棺架＝arabic_al-sufi 星群 SBNa。
逐字稿：04_腳本庫/X-03-北斗環球一個勺子的十種人生-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線（逐字稿考據備忘「連線」條）
  ①～⑩ 照 Stellarium 原樣；例外：
  - 布吉斯：照論文只畫北斗＋小熊 β γ —— bugis 006 的 天璣→ψ UMa→天璇 改成 天璣→天璇（ψ UMa 不畫）。
  - 阿拉伯：斗口四顆閉合框＝棺架（arabic_al-sufi SBNa）、天權→玉衡→開陽→搖光＝女兒（arabic_ancient 0399 的斗柄段）。
  - 埃文基：斗口閉合框（紫）＝駝鹿的腳、斗柄（綠）＝獵人（A-08 v2）。
  - 希臘：荷馬的熊＝北斗七星（紫）；托勒密大熊全形（greek_almagest UMa）畫成淡紫自訂層「大熊全形（托勒密）」，只當背景。
  - 定位：北斗白線＝斗口閉合＋斗柄（不屬任何一個文化）。
  - 曼達爾漁網：船身照 mandar 004 第一段（藍），漁夫三顆綠圈、漁具兩顆紅圈（自訂層「漁夫與漁具」，同 A-27）。
  - 白俄的紫線（連線-以利亞的車）與北歐藍線形狀相同，04 鏡只開北歐；白俄層留著，美宣要在 04 鏡後半換色可用。

參數（依本集逐字稿重新評估）
  lst = LST0 = 台北 2027/4/2 20:00 的恆星時＋180（取整數）→ 北盤 rot＝0 就是「台北 4/2 20:00 面北」：
             北斗在東北、斗口在左上、斗柄在右下（逐字稿 12 鏡「斗口在左上、斗柄在右下」）。
             整集不用長圖帶（全部是北盤），走廊 x＝0 在 RA ≈313（天鵝—飛馬之間），只照規定生成。
  D_s = 45、D_r = 49 → k＝1.3975：北斗最南的搖光 +49.3、輔 +54.9、θ Boo +51.9、λ Dra +69.3 都在盤本體；
             峇里空馬車的 κ UMa +47.2、ι UMa +48.0、托勒密熊腳 μ UMa +41.5 在填滿環（盤檔畫滿整圈，全片不回長圖，無影響）。
             ⚠ D_r 只能 ≤ 49（搖光）；k 不能再大，所以開陽—輔（11.8′＝0.27 單位）在任何 fov 都只隔一個星點直徑，
             06／07 鏡改用輔的細圈＋標籤指認（真正的雙星樣子放在 9:16 圖卡 C-X03-05 的放大框）；開陽不放進主角星，
             免得 ×1.5 星點＋光暈把輔整顆蓋掉。
  D_fill = −30 → R_fill＝167.7（盤寬 ÷ 畫布寬＝0.9316）：13 鏡 fov 70 從北斗拉到大角（+19.2）前，
             畫面下緣角落要收到 dec ≈ −10；D_fill 0（R_fill 125.8）放不下。|x_t|＋R_fill ≤ 180 ✓。
  x_tN = x_tS = 0（Canva 可水平置中）
  北盤 rot＝−((lst_obs＋180−lst) mod 360)（逆時針＝時間前進）；每段 M&M < 180°：
    02 鏡 20:00→04:00 −120.3°；08 鏡快轉 −60°；12 鏡 20:00→23:00 −45.1°。

鏡頭路線（全部北盤圖層組；原型欄照逐字稿寫在 note，kind 一律 R＝用盤檔）
  01 曼達爾漁網→北斗定位（rot 0）→ 02 繞北天極轉 20:00→04:00＋C-X03-01
  → 03【硬切】rot 0 牛腿 → 04／04b／04c／04d 車（北歐＋東歐 → 中國 → 巴比倫 → 峇里）
  → 05 熊＋C-X03-02 → 06 七個人（推近開陽—輔再拉回）→ 07 棺架（推近輔）
  → 08 強盜（快轉 −60°）→ 09 大蛇＋C-X03-03 → 10／10b 船、漁網 → 11／11b 獵物＋圖卡 C-X03-04
  → 12【硬切】台北 4/2 20:00→23:00 面北（山＝台北北方地平線）＋圖卡 C-X03-05
  → 13【硬切】rot 0 斗柄弧線往大角＋端卡
  逐字稿 04、10、11 鏡一鏡輪替好幾個文化；Canva 的連線／標籤層一頁一組，所以照旁白拆成
  04＋04b＋04c＋04d（5＋2＋4＋6＝17 秒）、10＋10b（5＋6）、11＋11b（7＋11），秒數合計不變（220 秒）。

硬切（判斷後接受）：02→03（02 轉到 04:00 的角度、03 回 20:00 角度開始第一種；倒轉 120° 會像時間倒流）、
  11b→12（圖卡之後換成「今晚」，起有地平線，同框接山會跳）、12→13（23:00 倒掛 → 回 20:00 畫弧線；「下週五」換段）。
check_shots 的 ⚠（判斷後接受；跑完逐條看過，寫在下方 WARN_OK）
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-03"
OUT = os.path.join(BASE, "05_素材/X-03_北斗環球/_v4大畫布")
D_S, D_R, D_FILL = 45.0, 49.0, -30.0
TPE = (25.0330, 121.5654)

WARN_OK = """
  全部 R「起／迄格畫面含長圖側扇區」：整集只用北盤圖層組，沒有任何一鏡切回大畫布（盤檔畫滿整圈），
  不會穿幫；不需要歸位／換組頁。
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


T = {
    "20": ("台北 4/2 20:00", TPE, "2027/4/2 20:00"),
    "23": ("台北 4/2 23:00", TPE, "2027/4/2 23:00"),
    "04": ("台北 4/3 04:00", TPE, "2027/4/3 04:00"),
}
LST_AT = {k: lst_at(*v[1], 8, v[2]) for k, v in T.items()}
LST0 = float(round(LST_AT["20"] + 180.0) % 360)


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    r = r + 360.0 if r <= -180.0 else r
    return round(r, 2)


ROT = {k: rot_n(v) for k, v in LST_AT.items()}
# 04:00 的角度要接在 20:00 之後「繼續逆時針」：rot_n 只回 ±180，這裡用連續值
ROT["04"] = round(ROT["20"] - (LST_AT["04"] - LST_AT["20"]) % 360.0, 2)
ROT["23"] = round(ROT["20"] - (LST_AT["23"] - LST_AT["20"]) % 360.0, 2)
R0 = ROT["20"]                   # 03–07 鏡的文化輪替角度＝台北今晚 20:00
R1 = round(R0 - 60.0, 2)         # 08 鏡快轉 60° 之後（09–11b 沿用）


def altaz(radec, where, when):
    import ephem
    o = _obs(*where, 8, when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(radec[0]), math.radians(radec[1])
    s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID = 54061, 53910, 58001, 59774, 62956, 65378, 67301
ALCOR = 65477
DIPPER = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]
BOWL, HANDLE = [DUBHE, MERAK, PHECDA, MEGREZ], [ALIOTH, MIZAR, ALKAID]
POLARIS, KOCHAB, PHERKAD = 11767, 72607, 75097
LAM_DRA, KAP_DRA, THUBAN, THE_BOO = 56211, 61281, 68756, 70497
PSI_UMA, CHI_UMA = 54539, 57399
ARCTURUS = 69673
BOAT = [MERAK, DUBHE, LAM_DRA, KAP_DRA, THUBAN, THE_BOO]
FISHERS, GEAR = [MEGREZ, ALIOTH, MIZAR], [PHECDA, ALKAID]
NET = BOAT + FISHERS + GEAR
# 開陽不進主角星（理由見上方「參數」）
MAINS = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, ALKAID, POLARIS]


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium index.json）
# ══════════════════════════════════════════════════════════════════
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def sc(root, culture, cid):
    d = json.load(open(os.path.join(root, culture, "index.json"), encoding="utf-8"))
    for c in d["constellations"]:
        if c["id"].split()[-1] == cid:
            segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
            return [s for s in segs if len(set(s)) >= 2]
    raise KeyError((culture, cid))


SEG_EGY = sc(SC_NEW, "egyptian", "001")
SEG_NORSE = sc(SC_NEW, "norse", "005")
SEG_BEL = sc(SC_NEW, "belarusian", "001")
SEG_CHN = sc(SC_NEW, "chinese", "039")
SEG_BAB = sc(SC_NEW, "babylonian_mulapin", "014")
SEG_BALI = sc(SC_NEW, "balinese", "PeSu")
SEG_ALMA = sc(SC_NEW, "greek_almagest", "UMa")
SEG_SAPT = sc(SC_NEW, "indian", "Sapt")
SEG_MAC = sc(SC_NEW, "macedonian", "001")
SEG_TUK = sc(SC_NEW, "tukano", "011")
SEG_INU = sc(SC_NEW, "inuit", "006")
_bug = sc(SC_OLD, "bugis", "006")[0]
assert _bug == [58001, 59774, 62956, 65378, 67301, 58001, 54539, 53910, 54061, 72607, 75097, 59774], _bug
SEG_BUGIS = [[h for h in _bug if h != PSI_UMA]]          # 天璣→天璇（不經 ψ UMa）
SEG_BOAT = [sc(SC_OLD, "mandar", "004")[0]]
assert SEG_BOAT[0] == BOAT, SEG_BOAT
SEG_DIPPER = [[DUBHE, MERAK, PHECDA, MEGREZ, DUBHE], [MEGREZ, ALIOTH, MIZAR, ALKAID]]
SEG_BIER = [[DUBHE, MERAK, PHECDA, MEGREZ, DUBHE]]
SEG_DAUGHTERS = [[MEGREZ, ALIOTH, MIZAR, ALKAID]]
assert {h for s in SEG_BALI for h in s} >= {PSI_UMA, CHI_UMA} and not ({ALIOTH, MIZAR, ALKAID} &
                                                                    {h for s in SEG_BALI for h in s})

LG_LOC = [(SEG_DIPPER, "#E8ECF5", 1.0)]
LG_BOAT = [(SEG_BOAT, "blue", 1.1)]
LG_EGY = [(SEG_EGY, "red", 1.1)]
LG_NORSE = [(SEG_NORSE, "blue", 1.1)]
LG_BEL = [(SEG_BEL, "purple", 1.1)]
LG_CHN = [(SEG_CHN, "amber", 1.1)]
LG_BAB = [(SEG_BAB, "amber", 1.1)]
LG_BALI = [(SEG_BALI, "green", 1.0)]
LG_GRK = [(SEG_DIPPER, "purple", 1.1)]
LG_SAPT = [(SEG_SAPT, "green", 0.8)]          # 細一點：推近開陽時不壓到輔
LG_BIER = [(SEG_BIER, "amber", 1.2)]
LG_DAU = [(SEG_DAUGHTERS, "amber", 0.8)]
LG_MAC = [(SEG_MAC, "red", 1.1)]
LG_TUK = [(SEG_TUK, "green", 1.1)]
LG_BUGIS = [(SEG_BUGIS, "amber", 1.0)]
LG_ELK = [(SEG_BIER, "purple", 1.1)]
LG_HUNT = [([[MEGREZ] + HANDLE], "green", 1.1)]
LG_INU = [(SEG_INU, "green", 1.1)]
LG_ALL = LG_LOC
LINE_SETS = [(LG_LOC, "連線-北斗（定位）"), (LG_BOAT, "連線-漁網星船身（曼達爾）"),
             (LG_EGY, "連線-牛的前腿（埃及）"), (LG_NORSE, "連線-男人的車（北歐）"),
             (LG_BEL, "連線-以利亞的車（白俄）"), (LG_CHN, "連線-北斗帝車（中國）"),
             (LG_BAB, "連線-車（巴比倫）"), (LG_BALI, "連線-空馬車（峇里）"),
             (LG_GRK, "連線-熊（荷馬）"), (LG_SAPT, "連線-七仙人（印度）"),
             (LG_BIER, "連線-棺架（阿拉伯）"), (LG_DAU, "連線-女兒（阿拉伯）"),
             (LG_MAC, "連線-強盜（馬其頓）"), (LG_TUK, "連線-大蛇（圖卡諾）"),
             (LG_BUGIS, "連線-船（布吉斯）"), (LG_ELK, "連線-駝鹿的腳（埃文基）"),
             (LG_HUNT, "連線-獵人（埃文基）"), (LG_INU, "連線-馴鹿（因紐特）")]
LINES_KEY = {"L4": "星座連線", "斗": "連線-北斗（定位）", "網": "連線-漁網星船身（曼達爾）",
             "漁": "漁夫與漁具", "埃": "連線-牛的前腿（埃及）", "北歐": "連線-男人的車（北歐）",
             "白俄": "連線-以利亞的車（白俄）", "中": "連線-北斗帝車（中國）", "巴": "連線-車（巴比倫）",
             "峇": "連線-空馬車（峇里）", "希": "連線-熊（荷馬）", "托": "大熊全形（托勒密）",
             "印": "連線-七仙人（印度）", "棺": "連線-棺架（阿拉伯）", "女": "連線-女兒（阿拉伯）",
             "馬": "連線-強盜（馬其頓）", "圖": "連線-大蛇（圖卡諾）", "布": "連線-船（布吉斯）",
             "鹿": "連線-駝鹿的腳（埃文基）", "獵": "連線-獵人（埃文基）", "因": "連線-馴鹿（因紐特）",
             "弧": "斗柄弧線（下集）"}
LINE_GROUPS = {"L4": LG_ALL, "斗": LG_LOC, "網": LG_BOAT, "漁": [], "埃": LG_EGY, "北歐": LG_NORSE,
               "白俄": LG_BEL, "中": LG_CHN, "巴": LG_BAB, "峇": LG_BALI, "希": LG_GRK,
               "托": [(SEG_ALMA, "#6E5A93", 0.8)], "印": LG_SAPT, "棺": LG_BIER, "女": LG_DAU,
               "馬": LG_MAC, "圖": LG_TUK, "布": LG_BUGIS, "鹿": LG_ELK, "獵": LG_HUNT, "因": LG_INU,
               "弧": []}


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


def arc_points(S, frac=0.86, n=60):
    """「順著斗柄畫一道弧」：從搖光出發、起點切線＝開陽→搖光，二次 Bézier（單位向量上）彎到大角；
    只畫到 frac（停在大角前）"""
    import numpy as np
    p0, pm, p2 = (np.array(vec(*S[h][:2])) for h in (ALKAID, MIZAR, ARCTURUS))
    t0 = p0 - pm
    t0 = t0 / np.linalg.norm(t0)
    d = np.linalg.norm(p2 - p0)
    c = p0 + t0 * d * 0.55
    out = []
    for i in range(n + 1):
        t = frac * i / n
        q = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t * t * p2
        out.append(radec(q))
    return out


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    from gen_master_canvas import great_circle

    def fishers(s, pos, runs, disc):
        for hips, col in ((FISHERS, COLORS["green"]), (GEAR, COLORS["red"])):
            for h in hips:
                for p in pos(*S[h][:2]):
                    s.circle(p[0], p[1], 1.05, stroke=col, w=0.16, opacity=0.95)
                    s.circle(p[0], p[1], 0.55, fill=col, opacity=0.35)

    def almagest(s, pos, runs, disc):
        rr = []
        for seg in SEG_ALMA:
            for a, b in zip(seg, seg[1:]):
                rr += runs(great_circle(*S[a][:2], *S[b][:2]))
        s.polylines(rr, stroke=COLORS["purple"], w=m.lw * 0.8, opacity=0.38)

    def arc(s, pos, runs, disc):
        s.polylines(runs(arc_points(S)), stroke=COLORS["white"], w=m.lw * 0.9, opacity=0.9,
                    dash="1.4 1.0")

    return [("漁夫與漁具", fishers), ("大熊全形（托勒密）", almagest), ("斗柄弧線（下集）", arc)]


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


def disc_xy(m, ra, dec, rot, north=True):
    """天體在「轉 rot 之後的盤」上的位置（畫面方向的畫布單位，盤心＝(0, ±y_pole)）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；與 A-27 同一套算法）
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
            n += max(1, len(re.findall(r"[aeiouyáéíóúèàâêîôûāīū]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (DIPPER, "北斗", "北斗 (chinese 039)", "Northern Dipper", "北斗", "white", "《史記・天官書》"),
    (DIPPER, "Big Dipper", "Big Dipper (Plough) (modern)", "Big Dipper", "大水杓（北美）", "white", "Stellarium modern"),
    (NET, "Bittoéng Panjala", "Bittoéng Panjala (mandar 004)", "Fishing Net Star", "漁網星（曼達爾）", "blue",
     "Rasyid et al. 2021；A-27"),
    (DIPPER, "Meskhetyu", "Bull's Foreleg (egyptian 001)", "Bull's Foreleg", "牛的前腿（古埃及）", "red",
     "msḫtjw；egyptian_dendera 001「Seth's Thigh」；中王國棺蓋對角星鐘"),
    (DIPPER, "Karlvagn", "Man's Cart (norse 005)", "Man's Cart", "男人的車（北歐）", "blue", "GKS 1812；A-15"),
    (DIPPER, "Іллёў воз", "Іллёў воз (belarusian 001)", "Elias's Cart", "以利亞的車（白俄羅斯）", "purple",
     "Illioŭ voz；A-22"),
    (DIPPER, "帝車", "—", "Emperor's Chariot", "天帝的車（中國）", "amber", "《史記・天官書》「斗為帝車，運於中央」"),
    (DIPPER, "MUL.MAR.GÍD.DA", "MAR.GID2.DA (Ereqqu) (babylonian_mulapin 014)", "Wagon", "車（巴比倫）", "amber",
     "MUL.APIN；ereqqu「車」"),
    (stars_of(SEG_BALI), "Pědati Suung", "Pědati Suung (balinese PeSu)", "An Empty Horse Cart", "空馬車（峇里）",
     "green", "斗口四顆＋大熊頭、前腳、ψ χ UMa；Stellarium 貢獻者依文字與圖重建"),
    (DIPPER, "Ἄρκτος", "—", "Bear", "熊（荷馬）", "purple", "Il. 18.487–489＝Od. 5.273–275；也叫 Ἅμαξα 車"),
    (DIPPER, "ṛkṣa", "R̥kṣa (indian)", "Bear", "熊（梵文）", "green", "Śatapatha Brāhmaṇa 2.1.2.4；與 ἄρκτος 同源"),
    (DIPPER, "Saptarṣi", "Saptarṣi (indian Sapt)", "7 Sages", "七位仙人（印度）", "green", "stellarium-master 版才有連線"),
    ([ALCOR], "Arundhatī", "Arundhati (indian)", "Arundhatī", "仙人的妻子（輔）", "green",
     "Stellarium 寫 Arundhati，IAST 改 Arundhatī"),
    (DIPPER, "Долоон өвгөн", "Doloon Burkhan (mongolian 003)", "Seven Old Men", "七位老人（蒙古）", "amber",
     "也叫 Долоон бурхан 七尊佛；A-07"),
    (DIPPER, "Seven Brothers", "Seven Brothers and Their Sister (blackfoot 001)", "Seven Brothers and Their Sister",
     "七兄弟和小妹（黑腳族）", "blue", "小妹 Sinopa＝輔；A-17 v2"),
    (BOWL, "Naʿsh", "SBNa (arabic_al-sufi)", "Bier", "棺架（阿拉伯）", "amber", "Banāt Naʿsh al-Kubrā；A-13"),
    (HANDLE, "Banāt", "بنات نعش (arabic_ancient 0399)", "Daughters", "女兒（抬棺）", "amber", "斗柄三顆"),
    (DIPPER, "بنات نعش", "بنات نعش (arabic_ancient 0399)", "Daughters of Naʿsh", "大棺架的女兒們", "amber",
     "Banāt Naʿsh al-Kubrā"),
    ([ALCOR], "al-Suhā", "السها", "al-Suhā", "被忽略的那顆（輔）", "amber", "俗語：我指給她看 al-Suhā，她指給我看月亮"),
    ([ALCOR], "السها", "السها (arabic_ancient)", "al-Suhā", "輔（阿拉伯文）", "amber", "Canva 原生輸入"),
    (DIPPER, "арамии", "арамии Aramii (macedonian 001)", "Thieves", "一夥強盜（馬其頓）", "red", "Cenev 2008"),
    (DIPPER, "Sipé Phairó", "Sipé Phairó (tukano 011)", "Snake", "大蛇（圖卡諾）", "green",
     "Cardoso 2007、2016；新版英文「Snake Large Anus」只說大蛇"),
    (stars_of(SEG_BUGIS), "bintoéng kappala'é", "Bintoѐng Kappala'ѐ (bugis 006)", "Ship", "船（布吉斯）", "amber",
     "Ôhashi & Orchiston 2021；不畫 bugis 006 的 ψ UMa；A-26"),
    (BOWL, "Хэглэн", "—", "Cosmic Elk", "駝鹿的腳（埃文基）", "purple", "A-08 v2（Анисимов）"),
    (HANDLE, "Манги", "—", "Hunter", "追牠的獵人", "green", "A-08 v2"),
    (DIPPER, "Tukturjuit", "Tukturjuit (inuit 006)", "Caribou", "馴鹿（因紐特）", "green", "MacDonald p. 200；A-14"),
    ([ARCTURUS], "大角", "—", "Arcturus", "大角（下集揭曉）", "white", "X-04"),
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

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=round(size, 2), dx=round(dx, 2),
                    dy=round(dy, 2), key=key, disc=True)

    TT = {t[1]: t for t in TERMS}

    def sz(px, fov):
        """標籤字級：Canva 上 px 大小 → 畫布單位 size（fpx＝size·1.7·1080/fov）"""
        return px * fov / (m.fu * 1080.0)

    def term(name, fov, px1=64, px2=48, dx=0.0, dy=0.0, zh=None, zh_only=False, orig_only=False,
             a=None, col=None, sub=None, key=None):
        a0, orig, _, _, zh0, col0, _ = TT[name]
        a = a if a is not None else a0
        col = col or col0
        zh = zh or zh0.split("（")[0]
        kk = key or name
        s1, s2 = sz(px1, fov), sz(px2, fov)
        gap = (px1 + px2) * 0.62 * fov / 1080.0
        if zh_only:
            out = [item(a, zh, col, s1, dx, dy, kk)]
        elif orig_only:
            out = [item(a, orig, col, s1, dx, dy, kk)]
        else:
            out = [item(a, orig, col, s1, dx, dy + gap / 2, kk),
                   item(a, zh, "white", s2, dx, dy - gap / 2, kk + "-zh")]
        if sub:                                       # 第三行（小字唸法）
            out.append(item(a, sub, "white", sz(40, fov), dx, dy - gap / 2 - (48 + 40) * 0.62 * fov / 1080.0,
                            kk + "-sub"))
        return out

    # ════════════════════ 構圖 ════════════════════
    def dpts(hips, rot):
        out = []
        for h in hips:
            ra, dec = (S[h][:2] if isinstance(h, int) else h)
            out.append(disc_xy(m, ra, dec, rot))
        return out

    def safe(cx, cy, fov):
        return max(math.hypot(cx + sx * fov / 2, cy + sy * fov * 8 / 9 - yp)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(hips, rot, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None, at=None):
        pts = dpts(hips, rot)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        if at is not None:
            cx, cy = disc_xy(m, *S[at][:2], rot)
        else:
            cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        cx, cy = cx + dx, cy + dy
        while not safe(cx, cy, f):
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def hfit(hips, rot, phi, fov, fh=0.22, dx=0.0):
        """有地平線的盤構圖：地平線北點放在離畫面下緣 fh 的高度，目標星水平置中"""
        pts = dpts(hips, rot)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        y_h = yp - k * phi
        H = fov * 16 / 9
        cx, cy = (max(xs) + min(xs)) / 2 + dx, y_h + (0.5 - fh) * H
        top = cy + 0.5 * H - 0.13 * H
        if max(ys) > top:
            print(f"  ⚠ hfit：最高的星 {max(ys) - top:+.1f} 超出上緣安全區（fov {fov}）")
        f = fov
        while not safe(cx, cy, f):
            f *= 0.99
            cy = y_h + (0.5 - fh) * f * 16 / 9
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    PHI_T = TPE[0]
    R04, R23 = ROT["04"], ROT["23"]
    F01a = dfit(NET, R0, pad=0.10, fov=60.0)
    F01b = dfit(DIPPER, R0, pad=0.12, minfov=30.0, dy=-3.0)
    xp, ypp = disc_xy(m, *S[POLARIS][:2], R0)
    F02a = (0.0, round(yp + 14.0, 2), 124.0, R0)                # 盤心偏上：北斗 20:00 在右、04:00 在左
    F02b = (0.0, round(yp + 14.0, 2), 124.0, R04)
    F03 = dfit(DIPPER, R0, pad=0.12, minfov=30.0, dy=-3.0)
    def zf(F, d):
        """同框輪替的文化：每鏡 fov 微縮 d（Canva 一個文化一頁、頁間 Match & Move 慢慢推近；
        完全同框的鏡頭會被 gen_canva_pages 併成一頁，換不了連線層）"""
        return (F[0], F[1], round(F[2] - d, 1), F[3])
    F04, F04b, F04c, F04dS = zf(F03, 0.8), zf(F03, 1.6), zf(F03, 2.4), zf(F03, 3.2)
    F04d = dfit(stars_of(SEG_BALI) + [ALKAID], R0, pad=0.08, fov=40.0, dy=-2.0)
    F05a = F03
    F05b = dfit(stars_of(SEG_ALMA), R0, pad=0.06, fov=50.0, dy=-3.0)
    F06a = dfit(DIPPER, R0, pad=0.10, fov=44.0, dx=-3.0, dy=-3.0)
    F06b = dfit([MIZAR, ALCOR], R0, fov=12.0, at=MIZAR, dx=0.4, dy=-1.0)
    F06c = dfit(DIPPER, R0, pad=0.10, fov=40.0, dy=-8.0)
    F07a = dfit(DIPPER, R0, pad=0.12, minfov=30.0, dy=-3.0)
    F07b = dfit([MIZAR, ALCOR], R0, fov=12.0, at=MIZAR, dx=0.4, dy=-1.0)
    F08a = dfit(DIPPER, R0, pad=0.10, fov=40.0, dy=-2.0)
    F08b = dfit(DIPPER, R1, pad=0.10, fov=40.0, dy=-2.0)
    F09 = F08b
    F10a = dfit(stars_of(SEG_BUGIS), R1, pad=0.08, fov=48.0)
    F10b = dfit(NET, R1, pad=0.08, fov=56.0)
    F11a = dfit(DIPPER, R1, pad=0.10, fov=36.0, dy=-2.0)
    F11b = F11a
    F12a = hfit(DIPPER, R0, PHI_T, 76.0, fh=0.14)
    F12b = hfit(DIPPER, R23, PHI_T, 76.0, fh=0.14)
    F13a = dfit(DIPPER, R0, pad=0.10, fov=40.0, dy=-2.0)
    arc_end = arc_points(S)[-1]
    F13b = dfit(DIPPER + [arc_end], R0, pad=0.08, fov=70.0)
    FR = dict(F01a=F01a, F01b=F01b, F02a=F02a, F02b=F02b, F03=F03, F04d=F04d, F05b=F05b, F06a=F06a,
              F06b=F06b, F06c=F06c, F07a=F07a, F07b=F07b, F08a=F08a, F08b=F08b, F10a=F10a, F10b=F10b,
              F11a=F11a, F12a=F12a, F12b=F12b, F13a=F13a, F13b=F13b)
    print("\n── 構圖 ──")
    for nm, v in FR.items():
        print(f"  {nm} {v}")
    print("  旋轉：" + "、".join(f"{kk} {T[kk][0]} LST {LST_AT[kk]:.1f} → {v:+.1f}°" for kk, v in ROT.items())
          + f"；LST0 {LST0:.0f}；R0 {R0:+.1f}、R1 {R1:+.1f}")

    # ════════════════════ 標籤 ════════════════════
    # 盤：dx/dy＝畫面方向（原生字不跟著盤轉；+dx 往右、+dy 往上）
    f1a, f1b = F01a[2], F01b[2]
    LB_NET = term("Bittoéng Panjala", f1a, 60, 46, dx=4.0, dy=-24.0, zh="上集：曼達爾的漁網")
    LB_OPEN = (term("北斗", f1b, 72, 0, dx=-9.5, dy=-7.0, zh_only=True)
               + term("Big Dipper", f1b, 52, 40, dx=-9.5, dy=-10.4, zh="北美：大水杓"))
    LB_POLE = [item([POLARIS], "北極星", "white", sz(44, F02a[2]), 0.0, -4.5, "北極星")]
    f3 = F03[2]
    LB_EGY = term("Meskhetyu", f3, 64, 48, dx=-5.0, dy=-8.0, zh="牛的前腿", sub="梅斯克提烏")
    LB_CART = (term("Karlvagn", f3, 56, 42, dx=-6.0, dy=-6.5, zh="北歐：男人的車")
               + term("Іллёў воз", f3, 56, 42, dx=-6.0, dy=-11.2, zh="白俄：以利亞的車"))
    LB_CHN = term("帝車", f3, 72, 48, dx=-5.5, dy=-8.0, zh="中國：天帝的車")
    LB_BAB = term("MUL.MAR.GÍD.DA", f3, 52, 44, dy=-8.0, zh="巴比倫：車", dx=-8.0)
    f4d = F04d[2]
    LB_BALI = term("Pědati Suung", f4d, 60, 46, dx=-2.0, dy=-12.0, zh="峇里：空馬車", a=BOWL)
    f5 = F05b[2]
    LB_BEAR = (term("Ἄρκτος", f5, 64, 46, dx=-7.0, dy=-6.0, zh="希臘：熊", a=DIPPER)
               + term("ṛkṣa", f5, 64, 46, dx=-7.0, dy=-12.5, zh="梵文：熊", a=DIPPER)
               + [item(DIPPER, "大熊全形：托勒密（2 世紀）", "white", sz(34, f5), -4.0, -18.0, "托勒密1"),
                  item(DIPPER, "熊腳在荷馬時代的雅典就已貼著地平線", "white", sz(34, f5), -4.0, -20.1, "托勒密2")])
    f6a, f6b, f6c = F06a[2], F06b[2], F06c[2]
    SAGES = [(DUBHE, "Kratu"), (MERAK, "Pulaha"), (PHECDA, "Pulastya"), (MEGREZ, "Atri"),
             (ALIOTH, "Aṅgiras"), (MIZAR, "Vasiṣṭha"), (ALKAID, "Marīci")]
    SAGE_D = {DUBHE: (0.0, -2.2), MERAK: (0.0, 2.0), PHECDA: (3.8, 1.2), MEGREZ: (3.0, 0.4),
              ALIOTH: (-3.4, -0.6), MIZAR: (-1.5, -2.0), ALKAID: (-2.0, -2.2)}
    LB_SAGES = (term("Saptarṣi", f6a, 60, 46, dx=-7.0, dy=-11.0, zh="印度：七位仙人")
                + [item([h], n, COLORS["green"], sz(40, f6a), *SAGE_D[h], "仙-" + n) for h, n in SAGES])
    LB_ARUN = ([item([MIZAR], "開陽 Vasiṣṭha", "white", sz(48, f6b), -2.4, -0.9, "開陽")]
               + term("Arundhatī", f6b, 60, 46, dx=2.2, dy=1.8, zh="輔：仙人的妻子", sub="阿倫達提"))
    LB_SEVEN = (term("Saptarṣi", f6c, 52, 40, dx=-4.0, dy=-11.0, zh="七位仙人（印度）", key="七-印")
                + term("Долоон өвгөн", f6c, 52, 40, dx=-4.0, dy=-16.0, zh="七位老人（蒙古）", key="七-蒙")
                + term("Seven Brothers", f6c, 52, 40, dx=-4.0, dy=-21.0, zh="七兄弟和小妹（黑腳族）", key="七-黑"))
    f7a, f7b = F07a[2], F07b[2]
    LB_BIER = (term("Naʿsh", f7a, 60, 46, dx=-1.0, dy=11.0, zh="棺架", a=BOWL)
               + term("Banāt", f7a, 60, 46, dx=1.0, dy=-8.0, zh="抬棺的女兒", a=HANDLE)
               + term("بنات نعش", f7a, 56, 0, dx=-5.0, dy=-10.0, orig_only=True, key="阿-原文"))
    LB_SUHA = ([item([MIZAR], "開陽", "white", sz(48, f7b), -1.8, -0.9, "開陽7")]
               + term("al-Suhā", f7b, 64, 46, dx=2.2, dy=1.8, zh="輔", sub="阿蘇哈")
               + term("السها", f7b, 56, 0, dx=2.2, dy=-1.6, orig_only=True, a=[ALCOR], key="السها"))
    f8 = F08a[2]
    LB_MAC = term("арамии", f8, 64, 48, dx=0.0, dy=-9.0, zh="馬其頓：一夥強盜")
    f9 = F09[2]
    LB_TUK = term("Sipé Phairó", f9, 64, 48, dx=0.0, dy=-9.0, zh="圖卡諾：吞魚的大蛇")
    f10a, f10b = F10a[2], F10b[2]
    LB_BUG = term("bintoéng kappala'é", f10a, 56, 44, dx=-6.0, dy=-30.0, zh="⑧ 布吉斯：船", a=DIPPER, )
    LB_MAN = term("Bittoéng Panjala", f10b, 60, 46, dx=2.0, dy=-27.0, zh="⑨ 曼達爾：漁網星", a=DIPPER)
    f11 = F11a[2]
    LB_EVE = (term("Хэглэн", f11, 60, 46, dx=1.0, dy=-14.0, zh="駝鹿的腳")
              + term("Манги", f11, 60, 46, dx=0.0, dy=-4.5, zh="追牠的獵人"))
    LB_INU = term("Tukturjuit", f11, 64, 48, dx=0.0, dy=-9.0, zh="因紐特：馴鹿")
    f12 = F12a[2]

    def alt20(h, when="2027/4/2 20:00"):
        return altaz(S[h][:2], TPE, when)[0]
    LB_TPE20 = ([item([DUBHE], f"天樞 {alt20(DUBHE):.0f}°", "white", sz(40, f12), -5.0, 1.0, "天樞20"),
                 item([ALKAID], f"搖光 {alt20(ALKAID):.0f}°", "white", sz(40, f12), 4.4, -0.8, "搖光20")]
                + [item(DIPPER, "台北 20:00", "amber", sz(56, f12), -4.0, -16.0, "台北20")])
    LB_TPE23 = ([item([DUBHE], f"天樞 {alt20(DUBHE, '2027/4/2 23:00'):.0f}°", "white", sz(40, f12), -4.0, -2.0,
                      "天樞23"),
                 item([ALKAID], f"搖光 {alt20(ALKAID, '2027/4/2 23:00'):.0f}°", "white", sz(40, f12), 3.0, 2.0,
                      "搖光23")]
                + [item(DIPPER, "23:00 整個倒掛", "amber", sz(56, f12), 0.0, 10.0, "台北23")])
    f13 = F13b[2]
    LB_NEXT = [item(DIPPER, "下集：順著斗柄", "white", sz(56, f13), 8.0, 14.0, "下集")]

    label_sets = [(LB_NET, "上集-漁網星"), (LB_OPEN, "北斗-開場"), (LB_POLE, "北極星"), (LB_EGY, "①牛的前腿"),
                  (LB_CART, "②車-北歐東歐"), (LB_CHN, "②車-帝車"), (LB_BAB, "②車-巴比倫"), (LB_BALI, "②車-峇里"),
                  (LB_BEAR, "③熊"), (LB_SAGES, "④七仙人"), (LB_ARUN, "④Arundhatī"), (LB_SEVEN, "④七個人"),
                  (LB_BIER, "⑤棺架"), (LB_SUHA, "⑤al-Suhā"), (LB_MAC, "⑥強盜"), (LB_TUK, "⑦大蛇"),
                  (LB_BUG, "⑧船"), (LB_MAN, "⑨漁網"), (LB_EVE, "⑩埃文基"), (LB_INU, "⑩因紐特"),
                  (LB_TPE20, "今晚-20點"), (LB_TPE23, "今晚-23點"), (LB_NEXT, "下集")]

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
    MARKS = [(MAINS, "主角星白點", "dot"), ([ALCOR], "輔細圈", "ring"), ([ARCTURUS], "大角細圈", "ring")]
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
        dict(code="01", kind="R", sec=17, north=True, frames=[F01a, F01b], layers=["網", "漁", "斗"],
             labels_start=ls("上集-漁網星"), labels=ls("北斗-開場"),
             vo="上週，它是曼達爾漁夫的漁網。七顆星排成一把勺子，中國叫它北斗，北美叫它大水杓。"
                "同一片星空，全世界都看見——這把勺子。可是在世界各地，它活出了十種人生。",
             card="全世界都看見——這把勺子｜十種人生",
             note=f"北盤（rot {R0:+.1f}°＝台北 4/2 20:00 面北的角度，不放地平線）Z fov {F01a[2]:.0f}→{F01b[2]:.0f}："
                  "起格開曼達爾漁網星（船身藍＋漁夫綠圈、漁具紅圈；上集收尾）→ 淡出；北斗定位線（白）淡入；"
                  "字卡前半格「全世界都看見——這把勺子」，唸到「十種人生」換副字卡「十種人生」"),
        dict(code="02", kind="R", sec=19, north=True, frames=[F02a, F02b], layers=["斗"], labels=ls("北極星"),
             overlay="C-X03-01_三千年前不落下", overlay_layers=["孟斐斯層", "長安層"],
             vo="為什麼大家都認得它？七顆星有六顆差不多亮，形狀好認。更重要的是，三千年前，地軸指的方向跟今天不一樣，"
                "它離北天極更近。從埃及北部、希臘到中國，七顆星整夜繞著轉，一顆都不落下。",
             card="三千年前，它一顆都不落",
             note=f"北盤 R 盤心偏上 fov {F02a[2]:.0f}：{T['20'][0]} → {T['04'][0]}（{R0:+.1f}°→{R04:+.1f}°，逆時針）"
                  "北斗從右邊繞過北極星上方到左邊；唸到「從埃及北部」定格疊 C-X03-01（孟斐斯層 → 長安層：前 1000 年最低 "
                  "+5.5°／+10.0° → 2027 年 −10.9°／−6.4°；雅典留給 05 鏡的 C-X03-02）"),
        dict(code="03", kind="R", sec=10, north=True, cut=True, frames=[F03], layers=["埃"], labels=ls("①牛的前腿"),
             vo="第一種：牛的前腿。古埃及人叫它 Meskhetyu。四千年前的棺材蓋上，就畫著這條牛腿。",
             card="① 牛的前腿",
             note=f"【硬切】（02 轉到 04:00 的角度；回 20:00 角度開始第一種）北盤 fov {F03[2]:.0f}：埃及「公牛的前腿」"
                  "（紅，egyptian 001）；標籤 Meskhetyu／牛的前腿＋小字「梅斯克提烏」；唸到「棺材蓋」切中王國棺蓋"
                  "（Asyut 一帶，約前 2000 年）對角星鐘照片——美宣另尋授權圖，不要拿新王國王陵或 Dendera（前一世紀）的圖代替"),
        dict(code="04", kind="R", sec=5, north=True, frames=[F04], layers=["北歐"], labels=ls("②車-北歐東歐"),
             vo="第二種：車。從北歐、東歐到中國，都把它看成一輛車，",
             card="② 車",
             note="北盤同框：北歐「男人的車」（藍，norse 005）；標籤兩組疊在斗柄下：Karlvagn／北歐、Іллёў воз／白俄"
                  "（白俄紫線與北歐同形，要換色可開「連線-以利亞的車（白俄）」）"),
        dict(code="04b", kind="R", sec=2, north=True, frames=[F04b], layers=["中"], labels=ls("②車-帝車"),
             vo="中國叫它「帝車」。",
             card="② 車",
             note="北盤同框：中國北斗（琥珀，chinese 039）；標籤 帝車／天帝的車；「北斗帝車」畫像石照片美宣另尋授權圖"),
        dict(code="04c", kind="R", sec=4, north=True, frames=[F04c], layers=["巴"], labels=ls("②車-巴比倫"),
             vo="大約三千年前，巴比倫的星表就已經叫它「車」。",
             card="② 車",
             note="北盤同框：巴比倫 MAR.GÍD.DA（琥珀，babylonian_mulapin 014：七顆一條線，斗口不閉合）"),
        dict(code="04d", kind="R", sec=6, north=True, frames=[F04dS, F04d], layers=["峇"], labels=ls("②車-峇里"),
             labels_start=[],
             vo="往南到峇里島，斗口四顆連上熊身，還是一輛車——一輛空的馬車。",
             card="② 車",
             note=f"北盤 Z fov {F04dS[2]:.0f}→{F04d[2]:.0f} 往斗口那頭拉開：峇里 Pědati Suung（綠，balinese PeSu：斗口四顆連到"
                  "大熊的頭、前腳與 ψ、χ UMa，不含斗柄）；峇里這段停 6 秒（≥ 4 秒）"),
        dict(code="05", kind="R", sec=22, north=True, frames=[F05a, F05b], layers=["希", "托"], labels=ls("③熊"),
             labels_start=[],
             overlay="C-X03-02_熊不下海洗澡", overlay_layers=["前750年層", "2027年層"],
             vo="第三種：熊。荷馬的史詩寫，大熊——人們也叫它車——在原地打轉，望著獵戶，只有它不下海洗澡。"
                "今天在希臘，熊尾巴的尖端已經會沾到海面。印度的古書也說，七位仙人從前就叫「熊」。"
                "梵文的熊跟希臘文的熊，是同一個字的後代。",
             card="③ 熊",
             note=f"北盤 Z fov {F05a[2]:.0f}→{F05b[2]:.0f}：主視覺是北斗七星（紫，荷馬的 Ἄρκτος／Ἅμαξα）；托勒密大熊全形"
                  "（自訂層「大熊全形（托勒密）」淡紫）疊在後面；迄格標籤 Ἄρκτος／ṛkṣa＋角落小字兩行；"
                  "「今天在希臘」起定格疊 C-X03-02（前 750 年層 → 2027 年層：雅典北方地平線，搖光最低 +12.3° → −2.7°），"
                  "疊圖收起後再開迄格標籤（overlay_at 預設＝結束頁後）"),
        dict(code="06", kind="R", sec=24, north=True, frames=[F06a, F06b, F06c], layers=["印"],
             labels_start=ls("④七仙人"), labels=ls("④Arundhatī"), labels_end=ls("④七個人"),
             vo="第四種：七個人。在印度，他們是七位仙人。斗柄中間那顆叫開陽，它旁邊的小星，是仙人的妻子 Arundhatī；"
                "到今天，有些婚禮還會在夜裡把她指給新娘看。蒙古說是七位老人，北美的黑腳族說是七兄弟和小妹——"
                "都是一群人，一起繞著北天極轉。",
             card="④ 七個人",
             note=f"北盤 fov {F06a[2]:.0f}→{F06b[2]:.0f}→{F06c[2]:.0f}：印度七仙人（綠，indian Sapt，stellarium-master 版）"
                  "＋七個仙人名逐顆亮 → 推近開陽—輔（輔細圈；標 開陽 Vasiṣṭha／Arundhatī＋小字「阿倫達提」）→ 拉回，"
                  "跨文化標籤堆疊（七仙人／七位老人／七兄弟和小妹）在北斗下方空天區"),
        dict(code="07", kind="R", sec=19, north=True, frames=[F07a, F07b], layers=["棺", "女"],
             labels_start=ls("⑤棺架"), labels=ls("⑤al-Suhā"),
             vo="第五種：棺架。阿拉伯人說，斗口四顆是一副棺架，斗柄三顆是抬棺的女兒。開陽旁邊那顆小星，這裡叫 al-Suhā，"
                "據說從前用來考眼力；有句俗話說：「我指給她看 al-Suhā，她指給我看月亮」——答非所問。",
             card="⑤ 棺架",
             note=f"北盤 fov {F07a[2]:.0f}→{F07b[2]:.0f}：阿拉伯 Banāt Naʿsh（琥珀；斗口四顆閉合框＝棺架 arabic_al-sufi SBNa，"
                  "斗柄三顆細線＝女兒）→ 推近開陽—輔，同一個細圈從 06 鏡的 Arundhatī 換成 al-Suhā（小字「阿蘇哈」）；"
                  "阿拉伯文 بنات نعش／السها 用 Canva 原生輸入（標籤資料已有）"),
        dict(code="08", kind="R", sec=12, north=True, frames=[F08a, F08b], layers=["馬"], labels=ls("⑥強盜"),
             vo="第六種：強盜。馬其頓民間說，這七顆星是一夥強盜，整夜在天上兜圈子——就像小偷繞著人家的房子打轉。",
             card="⑥ 強盜",
             note=f"北盤 R：馬其頓 арамии（紅，macedonian 001）；盤快轉 {R0:+.1f}°→{R1:+.1f}°（−60°，示意整夜繞圈；"
                  "畫面跟著北斗走）；標籤 арамии／一夥強盜"),
        dict(code="09", kind="R", sec=17, north=True, frames=[zf(F09, 1.0)], layers=["圖"], labels=ls("⑦大蛇"),
             overlay="C-X03-03_赤道邊的北斗", overlay_layers=["地平線層", "大蛇層"],
             vo="第七種：大蛇。到了赤道邊的亞馬遜，北斗跟其他星一樣，每天升起又落下。圖卡諾人說，那是一條大蛇："
                "每年，它在黃昏碰到地平線的那段日子，河裡的魚，幾乎都被它吞光了。",
             card="⑦ 吞魚的大蛇",
             note="北盤定格（08 鏡迄格）：圖卡諾大蛇（綠，tukano 011）；開始頁後就疊 C-X03-03「赤道邊的北斗」"
                  "（地平線層：Mitú 1.25°N 面北北西 9/1 黃昏 18:30、河面剪影 → 大蛇層：天樞、天璇剛沒入地平線，"
                  "天璣、天權貼著地平線）；收起後留盤上的大蛇與標籤"),
        dict(code="10", kind="R", sec=5, north=True, frames=[F10a], layers=["布"], labels=ls("⑧船"),
             vo="第八、第九種，前兩集見過：布吉斯人看見一艘木造帆船；",
             card="⑧ 船　⑨ 漁網",
             note="北盤：布吉斯船（琥珀；照論文只畫北斗＋小熊 β γ，不畫 bugis 006 多連的 ψ UMa）停 5 秒"),
        dict(code="10b", kind="R", sec=6, north=True, frames=[F10b], layers=["網", "漁"], labels=ls("⑨漁網"),
             vo="曼達爾漁夫把它一路連進天龍座，看成一張漁網。",
             card="⑧ 船　⑨ 漁網",
             note=f"北盤：從 10 鏡 Match & Move 拉開到 fov {F10b[2]:.0f}（不硬切）：曼達爾漁網星（船身藍＋漁夫綠圈、漁具紅圈，"
                  "北斗＋天龍＋牧夫 θ）停 6 秒"),
        dict(code="11", kind="R", sec=7, north=True, frames=[F11a], layers=["鹿", "獵"], labels=ls("⑩埃文基"),
             vo="第十種：獵物。西伯利亞的埃文基人說，斗口是駝鹿的腳，斗柄是追牠的獵人；",
             card="⑩ 獵物",
             note="北盤：埃文基駝鹿（斗口紫）＋獵人（斗柄綠）；標籤 Хэглэн／駝鹿的腳、Манги／追牠的獵人"),
        dict(code="11b", kind="R", sec=11, north=True, frames=[zf(F11b, 1.0)], layers=["因"], labels=ls("⑩因紐特"),
             overlay="C-X03-04_十種人生",
             vo="因紐特人看見馴鹿：冬天快到半夜，馴鹿會用後腳站起來。十種人生，我們整理成一張圖卡，存起來慢慢看。",
             card="⑩ 獵物",
             note="北盤同框：因紐特馴鹿（綠，inuit 006）；唸到「十種人生」疊 9:16 圖卡 C-X03-04「一個勺子的十種人生」"
                  "（①～⑩＋下方「十種之外」；可存圖），圖卡停 5 秒以上"),
        dict(code="12", kind="R", sec=25, north=True, cut=True, horizon=[PHI_T], frames=[F12a, F12b], layers=["斗"],
             labels_start=ls("今晚-20點"), labels=ls("今晚-23點"),
             overlay="C-X03-05_今晚抬頭看",
             vo="今晚從天黑到天亮，北斗都看得到。八點往東北方抬頭：它已經爬到半天高，斗口在左上、斗柄在右下；"
                "十一點前後，它升到北方最高處，整個倒掛。月亮到清晨三點多才升起，在那之前都沒有月光。"
                "找個光害少的地方考考眼力：開陽旁邊，你看得到 al-Suhā 嗎？",
             card="今晚八點　東北方",
             note=f"【硬切】（圖卡之後換「今晚」，起有地平線）北盤 {T['20'][0]} → {T['23'][0]} 面北（{R0:+.1f}°→{R23:+.1f}°；"
                  "山＝台北北方地平線）：北斗從東北爬到正北上方倒掛；標籤 天樞／搖光 高度；之後疊 9:16 圖卡 "
                  "C-X03-05「今晚抬頭看」（台北 4/2 20:00、23:00；開陽＋輔放大框；可存圖）"),
        dict(code="13", kind="R", sec=9, north=True, cut=True, frames=[F13a, F13b], layers=["斗", "弧"],
             labels=ls("下集"), labels_start=[],
             vo="下週五《春空導航術》：順著斗柄畫一道弧，去找北半天球最亮的恆星。",
             card="下集見｜春空導航術：沿著斗柄找大角",
             note=f"【硬切】（「下週五」換段）北盤 rot {R0:+.1f}° Z fov {F13a[2]:.0f}→{F13b[2]:.0f}：自訂層「斗柄弧線（下集）」"
                  "白虛線從搖光往畫面右下延伸、停在大角前；不開大角細圈、不標名字（大角在端卡揭曉，"
                  "要揭曉時才開「大角細圈」層）；端卡＋追蹤 CTA"),
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
    for a, b in zip(shots, shots[1:]):                 # 鏡頭之間（非硬切）的旋轉也要 < 180
        if not b.get("cut") and abs(b["frames"][0][3] - a["frames"][-1][3]) >= 178.0:
            print(f"  ✗ {a['code']}→{b['code']} 旋轉 {b['frames'][0][3] - a['frames'][-1][3]:+.1f}°")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            which = "北盤圖層組（置中）"
            ew = 2 * m.R_fill / fov * 1080
            off = (round(-cx / fov * 1080), round((cy - yp) / fov * 1080))
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

    for when in ("2027/4/2 20:00", "2027/4/2 23:00"):
        print(f"  台北 {when[5:]}：" + "、".join(f"{n} {altaz(S[h][:2], TPE, when)}" for n, h in
                                              (("天樞", DUBHE), ("天璇", MERAK), ("天璣", PHECDA), ("天權", MEGREZ),
                                               ("玉衡", ALIOTH), ("開陽", MIZAR), ("搖光", ALKAID))))
    print(f"  大角 20:00 {altaz(S[ARCTURUS][:2], TPE, '2027/4/2 20:00')}；弧線終點 {tuple(round(v, 1) for v in arc_end)}")
    print(f"  y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {k:.4f}")

    terms = {}
    for hips, orig, scn, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {scn}；" if scn not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文=o, 中譯=z, 英文=e, 顏色=c) for _, o, _, e, z, c, _ in TERMS],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": ROT, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        g = []
        for sh in shots:
            if name in sh.get("labels", []) + sh.get("labels_start", []) + sh.get("labels_end", []):
                g += [x for kk in sh["layers"] for x in LINE_GROUPS[kk] if x not in g]
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=g or LG_LOC,
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


if __name__ == "__main__":
    build()
