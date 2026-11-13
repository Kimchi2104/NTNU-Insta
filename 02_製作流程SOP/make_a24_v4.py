# -*- coding: utf-8 -*-
"""A-24 圖卡諾：亞馬遜的星空雨季曆｜大畫布 v4.6

論點：Tiquié 河中游（巴西亞馬遜州西北，北緯約 0.2°）的圖卡諾人看「黃昏時哪個星座正在西方落下」：
一個星座（或它的一段）落下，常常就跟著幾天雨、河水漲一次（poero），漲水就用星座命名。
主循環九個星座排成一年：小魚與蝦（寶瓶，二月）→ 美洲豹（仙后＋英仙，三～四月）→ 一群星（昴宿，四月底＝新年）
→ 放魚的木架（畢宿）→ 錛柄（獵戶腰帶＋兩肩，五月）→ 白鷺（后髮，八～九月）→ 毒蛇（天蠍＋人馬，九～十一月）
→ 犰狳（天鷹＋海豚，十二月）。天上寫的幾乎就是一條河。

來源：Stellarium tukano（Walmir Thomazi Cardoso；11 組連線）；Cardoso 2007 博士論文（PUC-SP）。
逐字稿：04_腳本庫/A-24-圖卡諾亞馬遜的星空雨季曆-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

連線：全部照 Stellarium tukano（CON tukano 001–011）。另有自訂層：
  烏鴉座蛇頭（紅虛線；Stellarium 001 沒有收烏鴉座，Cardoso p. 160、165「頭被砍斷，掉在烏鴉座」）、
  心宿二紅色光暈（毒囊）、siõka 候選（β Lib、α² Lib 白細圈＝L_marks ring）、
  木星 2006/8/3（Tiquié 站心，J2000 astrometric；琥珀圈）、木星與火星 2027/3/5 20:00（台北站心）。
  Pamõ 只畫 Stellarium 002（Cardoso 公開的天鷹三星「骨」＋海豚），不畫任何笛子造型。
  Yai 的鬍鬚（ρ、τ Cas、HIP 43）細線（寬 0.5 倍），不強調。

鏡頭路線（長圖帶狀為主＋北盤一段）
  01 Z 台北 3/5 20:00 西半天（獵戶—金牛—英仙）緩推到昴宿—畢宿—獵戶 → 02、03 概念圖（定格）
  → 04 S 往右（西）滑到寶瓶—雙魚（Tiquié 3/5 黃昏西方地平線在長圖 x≈+155，正好在這裡），
     鏡頭往東移＝星往西漂＝時間往前 → 05、06 概念圖 → 07 回到寶瓶開小魚與蝦（紫）＋年曆環
  → 08 昴宿 → 09 畢宿→錛柄 → 10 推近腰帶 → 11 長距離往東捲到后髮 → 12 烏鴉座→天蠍＋人馬
  → 13 天鷹＋海豚（犰狳）→ 14 年曆環 → 15 回天秤（siõka、2006 木星）→ 16 概念圖
  → 17【換北盤】（gen_canva_pages 自動插回中心／上移／長圖轉北盤）台北 3/5 19:00→20:00 面北，
     美洲豹在北點左邊（西北）低空 → 18【換長圖】（自動插歸位／北盤轉長圖／下移）昴宿—畢宿—獵戶→獅子座木星火星
  → 19 Z 推近獵戶＋金牛＋端卡。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 147 → 長圖的切口（x=±180）在 RA 327（海豚 RA 309～寶瓶 RA 345 之間的空天區）：
             本集要上長圖的星座 RA 從昴宿 57 一路往東到海豚 312，再加上寶瓶 345～鯨魚 5（04、07 鏡），
             只有 312→345 這段沒用到，切口放這裡，所有鏡頭都在一張連續的長圖上滑。
             x：昴宿 +90、畢宿五 +78、腰帶 +63、木星 2027 +5、軒轅十四 −5、后髮 −38～−50、烏鴉 −37～−42、
             β Lib −82、心宿二 −100、人馬 −137～−141、河鼓二 −151、海豚 −160～−165、寶瓶小魚 +158、蝦 +142～+170。
             台北 3/5 20:00 子午線（LST 104.6）在 x＝+42（01 鏡：x>42 是西半天）。
             北盤旋轉角 rot＝lst − LST台北 − 180：19:00 −122.5°、20:00 −137.6°（單段 < 180° ✓；
             歸位 −137.6°→0° 也 < 180°）。
  D_s = 62、D_r = 66 → 決定因素是 12 鏡的毒蛇（天蠍＋人馬＋南冕，dec −19.8…−43.4、橫跨 x −94…−141）：
             要整條放進一格，fov 至少 ~54；S 鏡頭 |cy|+fov·8/9 ≤ D_s ⇒ D_s 62 時 cy ≥ −14，
             畫面下緣 −62、南冕尾巴 −43 還在山的剪影之上。D_s 60 時尾巴會貼到山頂。
             北方：美洲豹（仙后 +56…+64、英仙 +47…+50）只在 17 鏡北盤上出現（盤檔完整圓，不受縫合帶影響），
             標籤一律 disc=True。
  D_fill = 20 → k＝2.3873、R_fill＝167.11（盤寬 ÷ 畫布寬＝0.9284，與 A-01 相同）；|x_t|+R_fill ≤ 180 ✓。
             17 鏡要放進台北北點（盤心下方 kφ＝59.8）與仙后（離盤心 ~70）：畫面角落離盤心 ≤ 120，遠在 R_fill 內。
  x_tN = x_tS = 0

check_shots 的 ⚠（判斷後接受；跑完逐條看過）
  17 R「畫面含長圖側扇區／切點」：全程在北盤圖層組上；換組由 gen_canva_pages 插「回中心／上移／長圖轉北盤」
  （盤心 0°、fov ≤ 50，盤緣圈內逐點重合）與「歸位／北盤轉長圖／下移」。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-24"
OUT = os.path.join(BASE, "05_素材/A-24_圖卡諾/_v4大畫布")
LST0 = 147.0
TPE = (25.0330, 121.5654)
TIQ = (0.22, -69.61)
PHI_T = 25.033


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


def rot_at(lat, lon, tz, when):
    """北盤面向北方：rot＝lst − LST − 180，收在 (−180, 180]；負＝逆時針＝時間前進"""
    L = lst_at(lat, lon, tz, when)
    return round((LST0 - L - 180.0 + 180.0) % 360.0 - 180.0, 2)


T_TPE = {"19:00": "2027/3/5 19:00", "20:00": "2027/3/5 20:00"}
ROT = {k: rot_at(*TPE, 8, v) for k, v in T_TPE.items()}
LST_TIQ = lst_at(*TIQ, -4, "2027/3/5 19:14")            # Tiquié 太陽 −6° 時


def bodies():
    """J2000 astrometric（與星表同框）"""
    import ephem
    out = {}
    o = _obs(*TPE, 8, "2027/3/5 20:00")
    for nm, b in (("木星2027", ephem.Jupiter()), ("火星2027", ephem.Mars())):
        b.compute(o)
        out[nm] = dict(ra=math.degrees(b.a_ra), dec=math.degrees(b.a_dec),
                       alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                       mag=round(float(b.mag), 2))
    o = _obs(*TIQ, -4, "2006/8/3 19:00")
    j = ephem.Jupiter(); j.compute(o)
    out["木星2006"] = dict(ra=math.degrees(j.a_ra), dec=math.degrees(j.a_dec), mag=round(float(j.mag), 2))
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


TK = load_sc("tukano")
T_ = lambda n: TK[f"CON tukano {n:03d}"]
SEG_ANA, SEG_PAMO, SEG_DAHSI, SEG_MHUA = T_(1), T_(2), T_(3), T_(4)
SEG_YAI, SEG_NOH, SEG_WAI, SEG_SIO = T_(5), T_(6), T_(7), T_(8)
SEG_YHE, SEG_YUR, SEG_SIPE = T_(9), T_(10), T_(11)
hips_of = lambda segs: sorted({h for s in segs for h in s})

WHISK = [117863, 117301, 43]                              # 鬍鬚 ρ、τ Cas、HIP 43
SEG_YAI_W = [s for s in SEG_YAI if len(s) == 2 and s[0] == 746 and s[1] in WHISK]
SEG_YAI_B = [s for s in SEG_YAI if s not in SEG_YAI_W]
assert len(SEG_YAI_W) == 3
CORVUS = [59803, 60965, 61359, 59316]                     # γ δ β ε Crv（四邊形）
SEG_CRV = [[59803, 60965, 61359, 59316, 59803]]
ANTARES, LAM_SCO, UPS_SCO = 80763, 85927, 85696
BETA_LIB, ALPHA2_LIB = 74785, 72622
CAPH, SCHEDAR, GAM_CAS, RUCHBAH, SEGIN, MIRFAK = 746, 3179, 4427, 6686, 8886, 15863
REGULUS = 49669
PLEIADES = hips_of(SEG_NOH)
HYADES = hips_of(SEG_WAI)
SIOY = hips_of(SEG_SIO)
BELT = [26727, 26311, 25930]
YHE = hips_of(SEG_YHE)
ANA = hips_of(SEG_ANA)
PAMO = hips_of(SEG_PAMO)
BONES = [98036, 97649, 97278]
MHUA = hips_of(SEG_MHUA)
DAHSI = hips_of(SEG_DAHSI)
YAI = hips_of(SEG_YAI)
HEAD = [CAPH, SCHEDAR, GAM_CAS]                            # W 西半邊＝頭
LEGS = [RUCHBAH, SEGIN]
ORION = [27989, 26207, 25336, 25930, 24436, 26727, 27366]
MAINS = ([ANTARES, BETA_LIB, ALPHA2_LIB, REGULUS, MIRFAK] + HEAD + LEGS + PLEIADES + HYADES + SIOY
         + BONES + CORVUS + [24436])


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
LG_YAI = [(SEG_YAI_B, "amber", 1.0), (SEG_YAI_W, "amber", 0.5)]
LG_FISH = [(SEG_MHUA, "purple", 1.0), (SEG_DAHSI, "purple", 0.8)]
LG_NOH = [(SEG_NOH, "blue", 1.0)]
LG_WAI = [(SEG_WAI, "blue", 1.0)]
LG_SIO = [(SEG_SIO, "blue", 1.0)]
LG_YHE = [(SEG_YHE, "purple", 0.7)]
LG_ANA = [(SEG_ANA, "red", 1.0)]
LG_PAMO = [(SEG_PAMO, "green", 1.0)]
LG_OTHER = [(SEG_SIPE, "red", 0.6), (SEG_YUR, "green", 0.6)]       # 主循環以外（只在總覽 L4）
LG_ALL = LG_YAI + LG_FISH + LG_NOH + LG_WAI + LG_SIO + LG_YHE + LG_ANA + LG_PAMO + LG_OTHER
LINE_SETS = [(LG_YAI, "連線-Yai美洲豹"), (LG_FISH, "連線-小魚與蝦"), (LG_NOH, "連線-Ñohkoatero一群星"),
             (LG_WAI, "連線-Waikhasa魚架"), (LG_SIO, "連線-Sioyahpʉ錛柄"), (LG_YHE, "連線-Yhé白鷺"),
             (LG_ANA, "連線-Aña毒蛇"), (LG_PAMO, "連線-Pamõ犰狳")]
LINES_KEY = {"L4": "星座連線", "豹": "連線-Yai美洲豹", "魚": "連線-小魚與蝦", "昴": "連線-Ñohkoatero一群星",
             "架": "連線-Waikhasa魚架", "錛": "連線-Sioyahpʉ錛柄", "鷺": "連線-Yhé白鷺",
             "蛇": "連線-Aña毒蛇", "狳": "連線-Pamõ犰狳", "頭": "烏鴉座蛇頭（虛線）",
             "囊": "心宿二紅色光暈", "光": "siõka候選", "木06": "木星2006年8月", "行": "木星與火星2027"}
LINE_GROUPS = {"L4": LG_ALL, "豹": LG_YAI, "魚": LG_FISH, "昴": LG_NOH, "架": LG_WAI, "錛": LG_SIO,
               "鷺": LG_YHE, "蛇": LG_ANA, "狳": LG_PAMO, "頭": [(SEG_CRV, "red", 0.8)],
               "囊": [], "光": [], "木06": [], "行": []}


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
def custom_layers(m, S):
    RED, AMB = COLORS["red"], COLORS["amber"]

    def crv(s, pos, runs, disc):
        rr = []
        for seg in SEG_CRV:
            for a, b in zip(seg, seg[1:]):
                rr += runs(great_circle(*S[a][:2], *S[b][:2]))
        s.polylines(rr, stroke=RED, w=m.lw * 0.8, opacity=0.92, dash="1.1 0.7")

    def antares(s, pos, runs, disc):
        for p in pos(*S[ANTARES][:2]):
            s.circle(p[0], p[1], 2.4, fill=RED, opacity=0.14)
            s.circle(p[0], p[1], 1.3, fill=RED, opacity=0.30)

    def jup06(s, pos, runs, disc):
        for p in pos(PL["木星2006"]["ra"], PL["木星2006"]["dec"]):
            s.circle(p[0], p[1], 2.2, fill=AMB, opacity=0.14)
            s.circle(p[0], p[1], 0.75, fill=AMB, opacity=0.98)

    def planets(s, pos, runs, disc):
        for nm, col, r in (("木星2027", "#FFFFFF", 0.80), ("火星2027", RED, 0.60)):
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.6, fill=col, opacity=0.16)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    return [("烏鴉座蛇頭（虛線）", crv), ("心宿二紅色光暈", antares), ("木星2006年8月", jup06),
            ("木星與火星2027", planets)]


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
# 四、旁白字數（中文字＋外文音節；外文照逐字稿「配音提示」的音節數）
# ══════════════════════════════════════════════════════════════════
SYL = {"tiquié": 3, "ñohkoatero": 5, "pamõ": 2, "poero": 3, "siõka": 3, "cardoso": 3, "walmir": 2,
       "seribhi": 3, "hó": 1, "w": 1, "aña": 2}


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
    (MHUA, "Mhʉã", "Mhua", "jacundá (a small cichlid)", "小魚（jacundá）", "purple",
     "Stellarium tukano 004；Cardoso 2007 p. 169：小魚被蝦追；二月落下"),
    (DAHSI, "Dahsiʉ", "Dahsiaw", "Shrimp", "蝦", "purple",
     "Stellarium tukano 003；線延伸到鯨魚座 6 顆（不是雙魚）；二月落下"),
    (YAI, "Yai", "Yai", "Jaguar", "美洲豹", "amber",
     "Stellarium tukano 005；仙后＋仙女＋英仙＋鹿豹；三～四月落下（Cardoso pp. 172–174）"),
    (HEAD, "頭", "—", "Head (west half of the W)", "頭（W 的西半邊）", "amber",
     "王良一 Caph＝口鼻、王良四 Schedar＝耳、γ Cas＝後頸"),
    (LEGS, "前腿", "—", "Forelegs", "前腿（δ、ε Cas）", "amber", "閣道三 Ruchbah、閣道二 Segin"),
    (WHISK, "鬍鬚", "—", "Whiskers", "鬍鬚（ρ、τ Cas）", "amber", "4.6–6.2 等，市區低空肉眼難見"),
    ([MIRFAK], "尾巴起點", "—", "Start of the tail (Mirfak)", "尾巴起點（天船三）", "amber", "英仙 α Mirfak"),
    (PLEIADES, "Ñohkoatero", "Nhorkoatero", "Group of Stars", "一群星（昴宿）", "blue",
     "Stellarium tukano 006；Cardoso 也作 Ñhorkoatero；圖卡諾以它落下為新年（p. 128 註 60）"),
    (HYADES, "Waikhasa", "Waikasa", "Fish rack (jirau de peixes)", "放魚的木架（畢宿）", "blue",
     "Stellarium tukano 007 英譯 Moquém（烤魚架）；Cardoso p. 179：捕魚陷阱或放魚的木架"),
    (SIOY, "Sioyahpʉ", "Sioyahpu", "Adze Handle", "錛柄（獵戶）", "blue",
     "Stellarium tukano 008：腰帶＋參宿四＋參宿五"),
    (YHE, "Yhé", "Yhé", "Egret", "白鷺（后髮）", "purple",
     "Stellarium tukano 009：后髮座 20 顆 4.3–6.4 等；Cardoso 清單裡的 M 星系不畫"),
    (ANA, "Aña", "Aña", "Fer-de-lance (water jararaca)", "毒蛇（天蠍＋人馬）", "red",
     "Stellarium tukano 001（43 顆）；九～十一月落下；Stellarium 說它落下是新年＝Tuyuka 的說法"),
    (CORVUS, "頭（烏鴉座）", "—", "Head (Corvus), cut off", "頭（烏鴉座）", "red", "dʉhpoa；Cardoso p. 160、165"),
    ([ANTARES], "毒囊（心宿二）", "—", "Venom sac (Antares)", "毒囊（心宿二）", "red", "nimaga；Cardoso p. 161"),
    ([LAM_SCO, UPS_SCO], "蛋", "—", "Eggs", "蛋（尾宿八、九一帶）", "red", "diepa"),
    (None, "尾巴", "—", "Tail (Sagittarius)", "尾巴（人馬）", "red", "pihkorõ"),
    (PAMO, "Pamõ", "Pamõ", "Armadillo", "犰狳（天鷹＋海豚）", "green",
     "Stellarium tukano 002；也是男性的聖笛；只畫公開的星（Cardoso p. 169）"),
    (BONES, "骨", "—", "Bones (Altair, Tarazed, Alshain)", "骨（河鼓二、三、一）", "green", "oãdʉka"),
    ([BETA_LIB], "β Lib", "—", "beta Librae", "siõka（2005）", "white", "Cardoso p. 155、註 95"),
    ([ALPHA2_LIB], "α² Lib", "—", "alpha-2 Librae", "也可能是它（表 3.02）", "white", "Cardoso 傾向 α²"),
    ((PL["木星2006"]["ra"], PL["木星2006"]["dec"]), "木星 2006", "—", "Jupiter, Aug 2006", "毒蛇的光（2006）",
     "amber", f"PyEphem：2006/8/3 Tiquié，{PL['木星2006']['mag']} 等"),
    ((PL["木星2027"]["ra"], PL["木星2027"]["dec"]), "木星", "—", "Jupiter", "木星", "white",
     f"台北 3/5 20:00 高 {PL['木星2027']['alt']}°、方位 {PL['木星2027']['az']}°"),
    ((PL["火星2027"]["ra"], PL["火星2027"]["dec"]), "火星", "—", "Mars", "火星", "red",
     f"台北 3/5 20:00 高 {PL['火星2027']['alt']}°、方位 {PL['火星2027']['az']}°"),
    ([REGULUS], "軒轅十四", "—", "Regulus", "軒轅十四", "white", ""),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=62, D_r=66, D_fill=20.0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole
    SGR_ = [h for h in ANA if S[h][0] > 270.0 and S[h][1] > -37.0]

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                    dy=round(dy, 2), key=key)

    T = {t[1]: t for t in TERMS}

    def term(name, dx=0.0, dy=0.0, s1=1.6, s2=1.2, gap=2.4, zh_only=False, a=None, disc=False, zh=None):
        a0, orig, _, _, zh0, col, _ = T[name]
        a = a if a is not None else a0
        zh = zh or zh0.split("（")[0]
        if zh_only:
            out = [item(a, zh, col, s1, dx, dy, name)]
        else:
            out = [item(a, orig, col, s1, dx, dy + gap / 2, name),
                   item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh")]
        if disc:
            for it in out:
                it["disc"] = True
        return out

    # 字級：Canva px ≈ size×1.7×1080/fov；主名 ~55 px、譯名 ~45 px（Canva 夾在 36–96）
    sz = lambda fov: dict(s1=round(fov * 0.030, 2), s2=round(fov * 0.024, 2), gap=round(fov * 0.046, 2))
    LB_FISH = term("Mhʉã", **sz(30)) + term("Dahsiʉ", **sz(30))
    LB_NOH = term("Ñohkoatero", **sz(30))
    LB_WS = term("Waikhasa", **sz(34)) + term("Sioyahpʉ", **sz(34))
    LB_SIO = term("Sioyahpʉ", **sz(22))
    LB_YHE = term("Yhé", **sz(34))
    f12 = 54.0
    LB_ANA = (term("Aña", **sz(f12))
              + term("頭（烏鴉座）", zh_only=True, s1=round(f12 * 0.026, 2), zh="頭（烏鴉座）")
              + term("毒囊（心宿二）", zh_only=True, s1=round(f12 * 0.026, 2), zh="毒囊")
              + term("蛋", zh_only=True, s1=round(f12 * 0.026, 2))
              + term("尾巴", zh_only=True, s1=round(f12 * 0.026, 2), a=SGR_))
    LB_PAMO = (term("Pamõ", **sz(30)) + term("骨", zh_only=True, s1=0.75)
               + [item(PAMO, "只畫公開描述的星", "white", 0.6, 0.0, 0.0, "Pamõ-註")])
    LB_SIOKA = (term("β Lib", s1=1.0, s2=0.9, gap=1.6, zh="siõka（2005）")
                + term("α² Lib", s1=0.9, s2=0.8, gap=1.4, zh="也可能是它")
                + term("木星 2006", s1=1.1, s2=0.95, gap=1.7, zh="毒蛇的光（2006）")
                + term("Aña", s1=1.3, s2=1.05, gap=1.9))
    # 盤（台北 3/5 面北）：字不跟著盤轉，dx/dy＝畫面方向；17 鏡 fov ~110
    DS = dict(disc=True)
    f17 = 110.0
    LB_YAI = (term("Yai", s1=round(f17 * 0.032, 2), s2=round(f17 * 0.026, 2), gap=round(f17 * 0.05, 2), **DS)
              + term("頭", zh_only=True, s1=round(f17 * 0.026, 2), zh="頭", **DS)
              + term("前腿", zh_only=True, s1=round(f17 * 0.022, 2), **DS)
              + term("鬍鬚", zh_only=True, s1=round(f17 * 0.020, 2), **DS)
              + term("尾巴起點", zh_only=True, s1=round(f17 * 0.020, 2), **DS))
    f18 = 52.0
    LB_WEEK = (term("Ñohkoatero", zh_only=True, s1=round(f18 * 0.026, 2), zh="昴宿・四月")
               + term("Waikhasa", zh_only=True, s1=round(f18 * 0.026, 2), zh="畢宿・五月")
               + term("Sioyahpʉ", zh_only=True, s1=round(f18 * 0.026, 2), zh="獵戶・五月")
               + term("木星", zh_only=True, s1=round(f18 * 0.026, 2))
               + term("火星", zh_only=True, s1=round(f18 * 0.026, 2))
               + term("軒轅十四", zh_only=True, s1=round(f18 * 0.021, 2)))

    label_sets = [(LB_FISH, "小魚與蝦"), (LB_NOH, "Ñohkoatero"), (LB_WS, "魚架與錛柄"), (LB_SIO, "錛柄-近"),
                  (LB_YHE, "Yhé白鷺"), (LB_ANA, "Aña毒蛇"), (LB_PAMO, "Pamõ犰狳"), (LB_SIOKA, "siõka"),
                  (LB_YAI, "Yai美洲豹"), (LB_WEEK, "這週末")]

    # ── 標籤偏移（長圖＝畫布方向、東在左；盤＝畫面方向） ──
    def shift(items, key, dx, dy):
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

    shift(LB_FISH, "Mhʉã", 0.0, 3.0); shift(LB_FISH, "Dahsiʉ", 0.0, -4.5)
    shift(LB_NOH, "Ñohkoatero", 0.0, 3.2)
    shift(LB_WS, "Waikhasa", 0.0, -4.0); shift(LB_WS, "Sioyahpʉ", 0.0, -12.5)
    shift(LB_SIO, "Sioyahpʉ", 0.0, -8.0)
    shift(LB_YHE, "Yhé", 0.0, -9.0)
    shift(LB_ANA, "Aña", 6.0, 20.0); shift(LB_ANA, "頭（烏鴉座）", 0.0, -5.0)
    shift(LB_ANA, "毒囊（心宿二）", 4.5, 0.0); shift(LB_ANA, "蛋", 0.0, -3.0); shift(LB_ANA, "尾巴", 0.0, 6.0)
    shift(LB_PAMO, "Pamõ", 0.0, 6.0); shift(LB_PAMO, "骨", 3.0, -1.5); shift(LB_PAMO, "Pamõ-註", 0.0, -8.0)
    shift(LB_SIOKA, "β Lib", 0.0, 2.2); shift(LB_SIOKA, "α² Lib", -6.0, -1.0)
    shift(LB_SIOKA, "木星 2006", 1.0, -3.4); shift(LB_SIOKA, "Aña", 0.0, -8.0)
    shift(LB_YAI, "Yai", 14.0, 4.0); shift(LB_YAI, "頭", -15.0, 1.0); shift(LB_YAI, "前腿", 15.0, 0.0)
    shift(LB_YAI, "鬍鬚", 0.0, -5.0); shift(LB_YAI, "尾巴起點", 0.0, 4.5)
    shift(LB_WEEK, "Ñohkoatero", 0.0, 2.6); shift(LB_WEEK, "Waikhasa", 0.0, -3.0)
    shift(LB_WEEK, "Sioyahpʉ", 0.0, -9.0); shift(LB_WEEK, "木星", 0.0, 2.6)
    shift(LB_WEEK, "火星", 0.0, -2.6); shift(LB_WEEK, "軒轅十四", 0.0, -2.4)

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 構圖 ════════════════════
    def disc_xy(h, rot):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        keep = m.lst
        m.lst = LST0 - rot
        p = m.pos_disc(ra, dec, True)
        m.lst = keep
        return (p[0][0], p[0][1] + yp) if p else None

    def fit(hips, rot, pad=0.12, minfov=30.0, dy=0.0, dx=0.0, extra=(), fov=None):
        pts = [disc_xy(h, rot) for h in hips] + [(x, y + yp) for x, y in extra]
        pts = [p for p in pts if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        far = lambda f: max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yp)
                            for sx in (-1, 1) for sy in (-1, 1))
        while far(f) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def sfit(hips, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, extra=(), clamp=True):
        pts = [(x_of(S[h][0]), S[h][1]) for h in hips] + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        if clamp:
            lim = m.Ds - f * 8 / 9 - 0.5                 # S：|cy|+fov·8/9 ≤ D_s
            cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    R19, R20 = ROT["19:00"], ROT["20:00"]
    HZ = m.k * PHI_T                                  # 台北北點在盤心下方 kφ
    # 01 Z：台北 20:00 的西半天（子午線 x=+42 以西）→ 推到昴宿—畢宿—獵戶（同一中心）
    F01b = sfit(PLEIADES + HYADES + ORION, pad=0.08, minfov=34.0, dy=-2.0)
    F01b = (F01b[0], F01b[1], 34.0, 0.0)
    F01a = (F01b[0], F01b[1], 60.0, 0.0)
    # 04 S：寶瓶—鯨魚（Tiquié 黃昏西方地平線 x≈+155）→ 往東到雙魚—白羊（星往西漂）
    F04a = sfit(MHUA + DAHSI, pad=0.10, minfov=40.0, dy=4.0)
    F04b = (round(F04a[0] - 12.0, 2), F04a[1], F04a[2], 0.0)
    F07 = sfit(MHUA + DAHSI, pad=0.12, minfov=36.0)
    F08 = sfit(PLEIADES, pad=0.10, minfov=30.0, dy=-2.0)
    F09a = sfit(HYADES, pad=0.10, minfov=30.0, dy=-2.0)
    F09b = sfit(SIOY, pad=0.10, minfov=36.0, dy=-1.0)
    F10 = (F09b[0], F09b[1], 22.0, 0.0)
    F11 = sfit(YHE, pad=0.10, minfov=34.0, dy=-3.0)
    F12a = sfit(CORVUS + [59199], pad=0.10, minfov=40.0, dy=-2.0)
    F12b = sfit(ANA, pad=0.04, minfov=f12)
    F13 = sfit(PAMO, pad=0.10, minfov=30.0, dy=-2.0)
    F15 = sfit([BETA_LIB, ALPHA2_LIB, ANTARES, 78401, 78265, 78820],
               pad=0.08, minfov=40.0, extra=[(x_of(PL["木星2006"]["ra"]), PL["木星2006"]["dec"])])
    F15 = (-82.0, F15[1], 40.0, 0.0)
    from gen_projection import horizon_points
    YAI_VIS = HEAD + LEGS + WHISK

    def hz_nw(key):                                   # 台北地平線方位 300°–360°（美洲豹下方那一段）
        L = lst_at(*TPE, 8, T_TPE[key])
        pts = horizon_points(PHI_T, L, n=721)
        return [pts[i] for i in range(600, 721)]
    F17a = fit(YAI_VIS + hz_nw("19:00"), R19, pad=0.08, dy=-4.0)
    F17b = fit(YAI_VIS + hz_nw("20:00"), R20, pad=0.08, dy=-4.0)
    F18a = sfit(PLEIADES + HYADES + ORION, pad=0.06, minfov=f18)
    F18b = sfit([REGULUS, 50583, 54872], pad=0.10, minfov=f18,
                extra=[(x_of(PL[k]["ra"]), PL[k]["dec"]) for k in ("木星2027", "火星2027")])
    F19a = sfit(ORION + [21421], pad=0.04, minfov=34.0)      # 獵戶＋畢宿五：fov 24 時兩者都還在畫面裡
    F19a = (F19a[0], F19a[1], 34.0, 0.0)
    F19b = (F19a[0], F19a[1], 24.0, 0.0)
    print(f"\n── 構圖 ──\n  01 {F01a}→{F01b}\n  04 {F04a}→{F04b}\n  07 {F07}\n  08 {F08}\n  09 {F09a}→{F09b}\n"
          f"  10 {F10}\n  11 {F11}\n  12 {F12a}→{F12b}\n  13 {F13}\n  15 {F15}\n  17 {F17a}→{F17b}\n"
          f"  18 {F18a}→{F18b}\n  19 {F19a}→{F19b}")

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot"), ([BETA_LIB, ALPHA2_LIB], "siõka候選", "ring")]
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
        dict(code="01", kind="Z", sec=11, north=True, frames=[F01a, F01b], layers=[], labels=[],
             vo="上週我們在羅馬尼亞的牧場，今晚飛到赤道上的亞馬遜，看星座在黃昏落下：同一片星空，圖卡諾人看見——一整年的漲水。",
             card="圖卡諾：一整年的漲水",
             note="大畫布 fov 60→34：台北 3/5 20:00 的西半天（子午線在 x=+42，以西＝畫面右側）緩推到昴宿—畢宿—獵戶；"
                  "不開連線；開場字卡（A-23 端卡背景是天蠍—人馬，硬切即可）"),
        dict(code="02", kind="Z", sec=16, north=True, frames=[F01b], layers=[], labels=[],
             overlay="C-A24-01_Tiquié河在哪", overlay_layers=["南美層", "河流層"],
             vo="巴西西北角，靠近哥倫比亞的雨林裡，有一條河叫 Tiquié。河邊住著圖卡諾人和他們的鄰居，餐桌上最重要的肉，是河裡的魚。河水什麼時候漲、什麼時候退，他們看得很重。",
             card="巴西西北・Tiquié 河",
             note="畫面不動；疊 C-A24-01（自繪示意：南美洲輪廓→亞馬遜州西北 Tiquié 河，標赤道；不是精確國界）；"
                  "河景照片美宣另尋授權圖（不用族人肖像）"),
        dict(code="03", kind="Z", sec=14, north=True, frames=[F01b], layers=[], labels=[],
             overlay="C-A24-02_用手量天", overlay_layers=["拳頭層", "手掌層"],
             vo="二〇〇五、二〇〇六年，巴西天文老師 Walmir Cardoso 受邀兩度來到河邊的村子。他和長老、原住民學校的學生一起看天、用手量角度，把星座一個一個畫下來。",
             card="2005–06・河邊看星",
             note="畫面不動；疊 C-A24-02（自繪示意：伸直手臂，拳頭約 10°、張開手掌約 20°；不翻拍論文照片）"),
        dict(code="04", kind="S", sec=10, north=True, frames=[F04a, F04b], layers=[], labels=[],
             vo="他們最看重的，不是星座升起，而是它落下。太陽一下山，就往西邊看：哪個星座正要沉進地平線？",
             card="看星座「落下」",
             note=f"長圖往右（西）滑到寶瓶—鯨魚，再往東移 12°（星往西漂＝時間往前）；不開連線。"
                  f"Tiquié 3/5 19:14 的西方地平線在長圖 x≈{x_of(LST_TIQ - 90):+.0f}（赤道上地平線在長圖上是一條直的經線），"
                  "就在起格畫面右側（再往右的已經落下）——這片天正是這幾天 Tiquié 黃昏落下的地方。Canva 的山剪影換成雨林樹冠線（美宣）"),
        dict(code="05", kind="S", sec=13, north=True, frames=[F04b], layers=[], labels=[],
             overlay="C-A24-03_poero漲水", overlay_layers=["落下層", "雨層", "漲水層"],
             vo="一個星座或星座的一段落下，常常就跟著幾天雨，河水漲一次。所以漲水直接用星座取名：犰狳落下時的那次，就叫 pamõ poero——犰狳的漲水。",
             card="poero＝漲水",
             note="畫面不動；疊 C-A24-03 三層：星座一段碰到西方地平線 → 雨 → 河水刻度上升＋pamõ poero"),
        dict(code="06", kind="S", sec=11, north=True, frames=[F04b], layers=[], labels=[],
             overlay="C-A24-04_赤道與台北的星軌", overlay_layers=["赤道層", "台北層"],
             vo="赤道上看星，有個好處：滿天每一顆星都會升起、落下，而且直直地往下沉。一整圈星座輪流落下，剛好排成一年。",
             card="赤道直直落，台灣斜斜轉",
             note="畫面不動；疊 C-A24-04：左＝赤道（星軌垂直地平線、兩極都在地平線上）、右＝台北（斜、北天拱極、南天一圈看不到）"),
        dict(code="07", kind="S", sec=11, north=True, frames=[F07], layers=["魚"], labels=ls("小魚與蝦"),
             overlay="C-A24-05_漲水年曆環", overlay_layers=["二月層", "三四月層"],
             vo="二月落下的，是一條小魚和追著牠的蝦，都是很暗的星；三、四月換美洲豹：鬍鬚、頭、身體、尾巴，一段一段沉下去。",
             card="二月 小魚與蝦／三～四月 美洲豹",
             note="長圖回到寶瓶：Mhʉã（小魚）＋Dahsiʉ（蝦）紫線淡入；迄格疊 C-A24-05 年曆環前兩層（二月紫、三～四月琥珀）"),
        dict(code="08", kind="S", sec=10, north=True, frames=[F08], layers=["昴"], labels=ls("Ñohkoatero"),
             labels_start=[],
             vo="四月底輪到昴宿，他們叫 Ñohkoatero，意思就是一群星。這裡的圖卡諾人說：昴宿落下，新的一年就開始了。",
             card="昴宿落下＝新年",
             note="長圖往東（左）滑到昴宿 fov 30；Ñohkoatero（藍）；字卡下小字「圖卡諾的新年（Cardoso）」"),
        dict(code="09", kind="S", sec=8, north=True, frames=[F08, F09a, F09b], layers=["架", "錛"],
             labels=ls("魚架與錛柄"), labels_start=ls("Ñohkoatero"),
             vo="接著是畢宿的 V 字，一個放魚的木架；五月，獵戶的腰帶加上兩肩，是一把錛子的木柄。",
             card="魚架・錛柄",
             note="fov 30→36：往左下（東南）滑 Waikhasa（畢宿 V，藍）→ Sioyahpʉ（腰帶＋參宿四＋參宿五，藍）"),
        dict(code="10", kind="Z", sec=15, north=True, frames=[F09b, F10], layers=["錛"],
             labels=ls("魚架與錛柄"), labels_end=ls("錛柄-近"),
             vo="鄰近民族的神話說：天上三個男人排成一排，中間那個人的腿被蛇咬了，又彎又乾枯，彎成一把錛的樣子。元旦那集說過，南美洲好幾個民族，都在這裡看見一條腿。",
             card="一條被蛇咬彎的腿",
             note="fov 36→22 推近腰帶；Sioyahpʉ（藍）；最後 4 秒在角落疊 X-02 的 C-X02-02「一條腿」預覽縮圖"
                  "（05_素材/X-02_獵戶環球/_概念圖/C-X02-02_一條腿_預覽_黑底.png；callback，美宣手動放）"),
        dict(code="11", kind="S", sec=9, north=True, frames=[F10, F11], layers=["鷺"], labels=ls("Yhé白鷺"),
             labels_start=[],
             vo="八、九月落下的，是一隻白鷺，由后髮座一帶很暗的星連成。那段時間常常很乾：河水退了，魚也少了。",
             card="白鷺落下，魚變少",
             note="長距離往東（左）捲到后髮座：Yhé（紫細線；只畫 Stellarium 009 后髮座 20 顆，不畫任何 M 星系）"),
        dict(code="12", kind="S", sec=14, north=True, frames=[F11, F12a, F12b], layers=["頭", "蛇", "囊"],
             labels=ls("Aña毒蛇"), labels_start=ls("Yhé白鷺"),
             vo="九月到十一月，是最長的一條：毒蛇 Aña，從天蠍連到人馬。牠的頭被砍斷，掉在烏鴉座；紅色的心宿二，是牠的毒囊。頭、身體、蛋、尾巴，每落下一段，就漲一次水。",
             card="心宿二＝毒蛇的毒囊",
             note="往南下到烏鴉座四邊形（蛇頭，紅虛線）→ 往東滑到天蠍＋人馬＋南冕（Aña，紅；Stellarium 001 43 顆）；"
                  "心宿二紅色光暈；標籤 頭、毒囊、蛋、尾巴"),
        dict(code="13", kind="S", sec=15, north=True, frames=[F12b, F13], layers=["狳"], labels=ls("Pamõ犰狳"),
             labels_start=ls("Aña毒蛇"),
             vo="十二月，犰狳落下，雷聲大作，魚群往上游。犰狳也是神聖的笛子：這個星座在天上真正的樣子，只有男人才知道。Cardoso 沒有寫出來，我們也只畫公開的那幾顆星。",
             card="犰狳落下，魚群上游",
             note="往東（左）滑到天鷹＋海豚 fov 30：Pamõ（綠）只開 Stellarium 002＝河鼓二、三、一「骨」＋海豚，"
                  "不畫任何笛子形狀；字卡下小字「只畫公開描述的星」"),
        dict(code="14", kind="S", sec=9, north=True, frames=[F13], layers=["狳"], labels=ls("Pamõ犰狳"),
             overlay="C-A24-05_漲水年曆環", overlay_layers=["二月層", "三四月層", "全年層"],
             vo="回頭看這一整圈：小魚、蝦、魚架、白鷺、毒蛇、美洲豹——天上寫的，幾乎就是一條河。",
             card="天上寫的，幾乎是一條河",
             note="畫面不動；疊 C-A24-05 年曆環三層到全亮；之後可接 9:16 圖卡 C-A24-07「圖卡諾的漲水曆」（首留言／可存圖）"),
        dict(code="15", kind="Z", sec=15, north=True, frames=[F15, (F15[0], F15[1], 36.0, 0.0)],
             layers=["蛇", "光", "木06"], labels=ls("siõka"),
             vo="大多數星座前面，還有一道亮光帶路，叫 siõka，通常是一顆亮星。二〇〇六年，木星剛好停在毒蛇前頭，大家就說：那是毒蛇的光。是恆星還是行星不要緊，位置才要緊。",
             card="siõka＝帶路的光",
             note="長圖往西（右）回到天秤＋天蠍頭 fov 40→36：β Lib（2005 的 siõka）、α² Lib（表 3.02，Cardoso 傾向它）"
                  "白細圈＝siõka候選層；2006/8 木星（約 −1.9 等；離 α² Lib 約 5°）琥珀點＝木星2006年8月層淡入；Aña（紅）"),
        dict(code="16", kind="Z", sec=14, north=True, frames=[(F15[0], F15[1], 36.0, 0.0)],
             layers=["蛇", "光", "木06"], labels=[],
             overlay="C-A24-06_流星與名字", overlay_layers=["流星層", "晨星層"],
             vo="流星呢？是「星星人」偷偷跑去約會，大家看到都會笑。二〇〇六年，長老替 Cardoso 辦了三天的命名儀式，給他一個圖卡諾名字：Seribhi Hó——晨星，胖胖的。",
             card="晨星，胖胖的",
             note="畫面不動；疊 C-A24-06：流星劃過（星星人去約會）→ 黎明東方的金星＋名字「Seribhi Hó」"),
        dict(code="17", kind="R", sec=15, north=True, horizon=[PHI_T],
             frames=[F17a, F17b], layers=["豹"], labels=ls("Yai美洲豹"),
             overlay="C-A24-08_這週末抬頭看",
             vo="這週末天黑後到八點半，在台灣往西北低空看：仙后座 W 的西半邊，就是美洲豹的頭。這幾天在 Tiquié，牠正碰到地平線；照圖卡諾的日曆，這正是美洲豹的漲水。",
             card="20:30 前・西北低空",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）；台北 3/5 面北（山＝台北北方地平線），"
                  f"19:00→20:00（{R19:+.1f}°→{R20:+.1f}°）；Yai（琥珀）：W 西半邊＝頭、δ ε＝前腿、鬍鬚細線、Mirfak＝尾巴起點；"
                  "最後疊 9:16 圖卡 C-A24-08「這週末抬頭看」"),
        dict(code="18", kind="S", sec=11, north=True, frames=[F18a, F18b], layers=["昴", "架", "錛", "行"],
             labels=ls("這週末"),
             vo="往西，昴宿、畢宿、獵戶排成一列，就是圖卡諾人接下來三個月的日曆。東方兩顆不閃的亮點，是木星和火星。",
             card="昴宿→畢宿→獵戶",
             note="【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）；fov 52：先停在昴宿、畢宿、獵戶三組藍線，"
                  "再往東（左）滑到獅子座的木星、火星（昴宿與獅子座赤經差約 90°，一個畫面框不下）"),
        dict(code="19", kind="Z", sec=11, north=True, frames=[F19a, F19b], layers=["錛", "架", "昴"], labels=[],
             vo="下週五，往東到巴西海岸。一六一二年，一位法國傳教士在那裡抄下二十八個星名，兩年後寫進書裡：「其他的，我就不寫了。」",
             card="下集見｜圖皮-瓜拉尼：1614 年傳教士抄下的星空",
             note="長圖往西（右）回到獵戶＋金牛 fov 34→24（下一集圖皮的老人 Tuyvaé 在這裡）；端卡＋追蹤 CTA"),
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
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  北盤旋轉角（台北 3/5，面向北方）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  Tiquié 3/5 19:14 LST {LST_TIQ:.1f} → 西方地平線 x {x_of(LST_TIQ - 90):+.1f}")
    print("  天體（J2000）：" + "、".join(f"{k} RA {v['ra']:.1f} Dec {v['dec']:+.1f}" for k, v in PL.items()))
    print(f"  x：昴宿 {x_of(S[17702][0]):+.1f}、腰帶 {x_of(S[26311][0]):+.1f}、軒轅十四 {x_of(S[REGULUS][0]):+.1f}、"
          f"心宿二 {x_of(S[ANTARES][0]):+.1f}、河鼓二 {x_of(S[97649][0]):+.1f}、小魚 {x_of(S[114855][0]):+.1f}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if isinstance(hips, list) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI_T, "bodies": PL},
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
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
