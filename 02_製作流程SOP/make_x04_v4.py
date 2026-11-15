# -*- coding: utf-8 -*-
"""X-04 春空導航術：沿著斗柄找大角｜大畫布 v4.6（長圖＋北盤，跨文化專題）

論點：北斗是路標。開陽→搖光→大角→角宿一幾乎在同一個圓上（半徑 45.6°），英文口訣 arc to Arcturus、
spike to Spica；《史記》「直斗杓所指，以建時節」「杓攜龍角」、《鶡冠子》「斗柄東指，天下皆春」、
赫西俄德「冬至後六十天大角黃昏升起」——三個文化都拿這一帶的星報春。再加上薩米、圖卡諾、阿拉伯、
夏威夷、印度對大角／角宿一的說法，與春季大三角、大鑽石。

來源：Stellarium modern（RH1 搖光→大角→角宿一、Spring Triangle、Great Diamond）、chinese（039 北斗、060 大角、
317 左攝提、288 右攝提、009 角宿）、greek_almagest（Boo）、sami（002 弓、005 Fávdna）、tukano（011 Sipé Phairó）、
hawaiian_starlines（IWI 脊椎骨）、arabic_indigenous（ThSl／SmkA）、indian_nakshatras（月站）。
天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，UTC+8；1010 hPa、20°C）。
逐字稿：04_腳本庫/X-04-春空導航術沿著斗柄找大角-逐字稿-v1.md。

自訂連線（假星 HIP 91xxxxx，星等 99，不畫成星點，只當連線端點）：
  弧線＝過搖光、大角、角宿一的小圓（半徑 45.6°；開陽離圓 0.16°），每 1° 一點：
    「弧線-到大角」從開陽畫到大角（02 鏡）、「弧線-到角宿一」大角→角宿一（03 鏡）。
    Stellarium RH1 原樣是兩段直線（搖光—大角—角宿一）；片中照逐字稿改畫成圓弧。
  黃道（15 鏡）＝J2000 黃道 λ 140°–260° 每 2° 一點。
  月牙、木星、火星（14 鏡）＝台北 2027/4/9 的 J2000 視位置（月 19:30、行星 20:00；行星一晚只動 0.1°）。

參數（依本集逐字稿重新評估）
  lst = 200 → 弧線上的四顆星都在走廊裡：開陽 x −1.0、搖光 −6.9、大角 −13.9、角宿一 −1.3（T 鏡頭 fov 50 的
             半寬 25 放得下）；斗身天樞時角 +34 在盤上 x +22。春季大三角：五帝座一 x +22.7、常陳一 +6.0；
             軒轅十四 +47.9（13 鏡迄格要放寬到 fov 76）。
             北盤 R 鏡頭的旋轉（面北，rot＝−((LST＋180−lst) mod 360)）：台北 4/9 黃昏 −98.3°、
             3/21 黃昏 −77.3°、漢代長安春分黃昏（搖光 86°）−100.9°、14 鏡 19:30 −111.6°→21:00 −134.1°：
             每段 M&M 都 < 170°，從換組的 0° 出發也 < 170°（v4.6 第四節）。
  D_s = 45、D_r = 49 → 北斗最南的搖光 +49.31 在北盤本體；長圖帶要收：常陳一 +38.3（13 鏡）、牧夫座 β +40.4、
             大角 +19.2、角宿一 −11.2。k = 1.3975。
  D_fill = −35 → R_fill = 174.68（盤寬 ÷ 畫布寬＝0.970456 ⚠ 只差 3%，Canva 別設成同寬）。決定因素是 14、15 鏡：
             台北面北、畫面往東移到大角＋角宿一（盤上 x +86…+104、y +50…+96）還要放進東方地平線，
             fov 92 的畫面角落距盤心 171；D_fill −30（R_fill 167.7）放不下，D_fill 0（125.8）更不行。|x_t|＋R_fill ≤ 180 ✓。
  x_tN = x_tS = 0（Canva 可水平置中）

鏡頭路線（逐字稿 15 鏡 → 本檔 17 鏡：09 拆 09／09b／09c，因為薩米的弓與圖卡諾的大蛇是同七顆星的兩種連法，
  一鏡只能掛一組連線層；秒數照字數拆 6＋6＋8＝20，總長不變）
  01 長圖（盤緣圈內＝北盤逐點相同）Z 北斗 → 02 T 沿走廊下來、弧線到大角 → 03 T 續到角宿一 → 04 全弧＋C-X04-01
  → 05 Z 中國星官（北斗、大角＋左右攝提、角宿），迄格回到帶中央（0,0,50）＝換組出發點
  → 06【換北盤】（自動插上移／長圖轉北盤）盤轉到台北 4/9 黃昏、搖光在三點鐘 → C-X04-02
  → 07 R 漢代春分黃昏 → 台北 3/21 春分黃昏（還沒到三點鐘）→ 台北 4/9 黃昏
  → 08【換長圖】（自動插歸位／北盤轉長圖／下移）牧夫座＋C-X04-03 → 09 薩米 → 09b 圖卡諾 → 09c 阿拉伯
  → 10 夏威夷＋C-X04-07 → 11 推近大角＋C-X04-04 → 12 推近角宿一 → 13 春季大三角→大鑽石→軒轅十四版＋圖卡 C-X04-05
  → 14【換北盤】台北 4/9 面北：19:30 往西看月牙 → 21:00 往東看弧線＋圖卡 C-X04-06 → 15 北盤同框推近大角、角宿一（月站）

逐字稿的畫面構想改了三處（回報）：01 用長圖（不是北盤）：北斗在盤緣圈內，長圖與北盤逐點相同，
  02 才能直接沿走廊滑下來，不用先回盤心；07 加一格「台北今年春分的黃昏」，「晚三個星期」才看得出來；
  15 留在北盤（14 的台北東方天空），月站標記畫在黃道上，不再換回長圖。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-04"
OUT = os.path.join(BASE, "05_素材/X-04_春空導航/_v4大畫布")
LST0 = 200.0
D_S, D_R, D_FILL = 45.0, 49.0, -35.0
TPE = (25.0330, 121.5654)
PHI = 25.03

WARN_OK = """
  06、07、14、15 R「起／迄格畫面含長圖側扇區」：06 起格＝盤心 fov 50、0°（換組那一格，盤緣圈內逐點重合）；
  07 前後都在北盤；07→08、13→14 換組由 gen_canva_pages 自動插「歸位／回中心／上移」（盤心 fov 50、0°）。
  14 起格（台北 19:30 往西）是長圖→北盤換組後 Match & Move 過去的，不直接切回大畫布；14→15 都在北盤上，不回長圖。
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
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return round(r + 360.0 if r <= -180.0 else r, 2)


ALK_RA = 206.885
T_TPE = {"dusk0409": "2027/4/9 18:37", "dusk0321": "2027/3/21 18:28",
         "1930": "2027/4/9 19:30", "2000": "2027/4/9 20:00", "2100": "2027/4/9 21:00"}
LST_AT = {k: lst_at(v) for k, v in T_TPE.items()}
ROT = {k: rot_n(v) for k, v in LST_AT.items()}
# 漢代長安春分黃昏：搖光在天北極的 86° 方向（逐字稿星空對時表）＝時角 −86°；盤是 J2000，
# 只取「斗柄相對天北極的方向」，不畫當時的天極位置（當時勾陳一離天北極 12°，盤上不標北極星）
ROT["han"] = rot_n(ALK_RA - 86.0)


def body_radec(body, when):
    import ephem
    o = _obs(*TPE, 8, when)
    b = getattr(ephem, body)(); b.compute(o)
    return math.degrees(b.a_ra), math.degrees(b.a_dec), math.degrees(b.alt), math.degrees(b.az)


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, ARCTURUS, SPICA = 11767, 69673, 65474
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
DENEBOLA, COR_CAROLI, REGULUS, HENG2 = 57632, 63125, 49669, 66249
ZUO = [72125, 71762, 71795]        # 左攝提 牧夫 ο π ζ（大角東側）
YOU = [67927, 67275, 67459]        # 右攝提 牧夫 η τ υ（大角西側）
MAINS = DIPPER + [POLARIS, ARCTURUS, SPICA, DENEBOLA, COR_CAROLI, REGULUS, HENG2]
MOON, JUP, MARS, NCP = 9200001, 9200002, 9200003, 9200004
MARK_V = {MOON: -3.0, JUP: -2.1, MARS: -0.2}          # 標記用的亮度（假星本身 V=99，不進星點層）
ARC0, ECL0 = 9100000, 9150000


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def unit(a):
    n = math.sqrt(dot(a, a)); return tuple(x / n for x in a)


def sep(S, a, b):
    return math.degrees(math.acos(max(-1, min(1, dot(vec(*S[a][:2]), vec(*S[b][:2]))))))


def arc_points(S):
    """過搖光、大角、角宿一的小圓：圓心 c、半徑 ρ；回傳從開陽（投影到圓上）→大角→角宿一的點列"""
    a, b, s = (vec(*S[h][:2]) for h in (ALK, ARCTURUS, SPICA))
    c = unit(cross(tuple(b[i] - a[i] for i in range(3)), tuple(s[i] - a[i] for i in range(3))))
    if dot(c, a) < 0:
        c = tuple(-x for x in c)
    rho = math.degrees(math.acos(dot(c, a)))
    e1 = unit(tuple(a[i] - dot(a, c) * c[i] for i in range(3)))
    e2 = cross(c, e1)

    def ang(v):
        return math.degrees(math.atan2(dot(v, e2), dot(v, e1)))

    def pt(t):
        cr, sr = math.cos(math.radians(rho)), math.sin(math.radians(rho))
        ct, st = math.cos(math.radians(t)), math.sin(math.radians(t))
        return radec(tuple(c[i] * cr + sr * (e1[i] * ct + e2[i] * st) for i in range(3)))

    m = vec(*S[MIZ][:2])
    t_miz, t_arc, t_spi = ang(m), ang(b), ang(s)
    off = {h: abs(math.degrees(math.acos(dot(c, vec(*S[h][:2])))) - rho) for h in (MIZ, ALI, MEG)}
    sgn = 1 if t_arc > 0 else -1           # 從搖光（t=0）往大角的方向
    pts1 = [pt(t) for t in frange(t_miz, t_arc, sgn)]
    pts2 = [pt(t) for t in frange(t_arc, t_spi, sgn)]
    return pts1, pts2, rho, off, radec(c)


def frange(t0, t1, sgn, step=1.0):
    out, t = [], t0
    while (t - t1) * sgn < 0:
        out.append(t); t += step * sgn
    return out + [t1]


def ecliptic_points(l0=140, l1=262, step=2):
    eps = math.radians(23.4393)
    out = []
    for lam in range(l0, l1, step):
        L = math.radians(lam)
        ra = math.degrees(math.atan2(math.sin(L) * math.cos(eps), math.cos(L))) % 360
        dec = math.degrees(math.asin(math.sin(eps) * math.sin(L)))
        out.append((ra, dec))
    return out


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def sc_lines(cu, cid):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    for c in d.get("constellations", []) + d.get("asterisms", []):
        if c["id"].split()[-1] == cid:
            return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    raise KeyError(cu + " " + cid)


SEG_DIPPER = [[DUB, MER, PHE, MEG, DUB], [MEG, ALI, MIZ, ALK]]       # 標準北斗（斗口閉合）
SEG_CN_DOU = sc_lines("chinese", "039")
SEG_CN_SHE = sc_lines("chinese", "317") + sc_lines("chinese", "288")
SEG_CN_JIAO = sc_lines("chinese", "009")
SEG_BOO = sc_lines("greek_almagest", "Boo")
SEG_BOW = sc_lines("sami", "002")
SEG_SNAKE = sc_lines("tukano", "011")
SEG_HAW = [[ARCTURUS, SPICA]]          # hawaiian_starlines IWI 的 [搖光, 大角, 角宿一] 只取大角—角宿一段
assert [ALK, ARCTURUS, SPICA] in sc_lines("hawaiian_starlines", "IWI")
SEG_TRI = [[ARCTURUS, SPICA, DENEBOLA, ARCTURUS]]
SEG_DIA = sc_lines("modern", "GDi")    # 大角—角宿一—五帝座一—常陳一—大角
SEG_TRI_R = sc_lines("modern", "SpT")  # Stellarium：大角—角宿一—軒轅十四


def nakshatra_stars():
    d = json.load(open(os.path.join(SC, "indian_nakshatras", "index.json"), encoding="utf-8"))
    out = []
    for c in d["constellations"]:
        hs = [h for l in c["lines"] for h in l if isinstance(h, int)]
        if hs:
            out.append(hs[-1] if c["id"].endswith("Naks14") else hs[0])
    return out


NAKS = nakshatra_stars()


def build_lines(arc1, arc2, ecl):
    LG = {
        "斗": [(SEG_DIPPER, "white", 1.0)],
        "弧1": [([arc1], "amber", 1.25)],
        "弧2": [([arc2], "amber", 1.25)],
        "中": [(SEG_CN_DOU, "amber", 1.0), (SEG_CN_SHE, "green", 1.0), (SEG_CN_JIAO, "blue", 1.1)],
        "牧": [(SEG_BOO, "purple", 1.0)],
        "弓": [(SEG_BOW, "green", 1.1)],
        "蛇": [(SEG_SNAKE, "green", 1.1)],
        "夏": [(SEG_HAW, "blue", 1.2)],
        "三": [(SEG_TRI, "amber", 1.1)],
        "鑽": [(SEG_DIA, "blue", 1.0)],
        "軒": [(SEG_TRI_R, "purple", 0.8)],
        "黃": [([ecl], "white", 0.5)],
    }
    NAME = {"斗": "連線-北斗", "弧1": "連線-弧線到大角", "弧2": "連線-弧線到角宿一", "中": "連線-中國星官",
            "牧": "連線-牧夫座（希臘）", "弓": "連線-Fávdna的弓（薩米）", "蛇": "連線-大蛇（圖卡諾）",
            "夏": "連線-脊椎骨（夏威夷）", "三": "連線-春季大三角", "鑽": "連線-春季大鑽石",
            "軒": "連線-軒轅十四版三角", "黃": "連線-黃道"}
    return LG, NAME


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A 系列同一套算法）
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
            n += max(1, len(re.findall(r"[aeiouyáéíóúąęįǫāēīōū]+", w.lower().replace("ʼ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、名詞總表（＝標籤對照表）
#   key: (錨點, 原文（片中寫法）, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "北斗": (DIPPER, "北斗", "Big Dipper", "北斗七星", "white", "chinese 039；modern UMa 的一部分"),
    "開陽": ([MIZ], "開陽", "Mizar (ζ UMa)", "開陽", "white", "離弧線所在的圓 0.16°"),
    "搖光": ([ALK], "搖光", "Alkaid (η UMa)", "搖光（斗柄末端）", "white", "RH1 起點"),
    "大角": ([ARCTURUS], "大角", "Arcturus (α Boo)", "大角", "amber", "chinese 060；北半天球最亮的恆星"),
    "角宿一": ([SPICA], "角宿一", "Spica (α Vir)", "角宿一", "blue", "chinese 009"),
    "北斗-中": (DIPPER, "北斗", "Northern Dipper", "北斗（斗杓＝斗柄）", "amber", "chinese 039；《史記》杓攜龍角"),
    "左攝提": (ZUO, "左攝提", "Left Conductor", "大角東側三星（牧夫 ο π ζ）", "green", "chinese 317；《史記》"),
    "右攝提": (YOU, "右攝提", "Right Conductor", "大角西側三星（牧夫 η τ υ）", "green", "chinese 288；《史記》"),
    "角宿": ([SPICA, HENG2], "角宿", "Horn", "青龍的角（角宿一、角宿二）", "blue", "chinese 009"),
    "天北極": ((0.0, 90.0), "天北極", "North Celestial Pole", "天北極（鐘心）", "white",
            "07 鏡漢代那一格不標北極星（當時勾陳一離天北極 12°）"),
    "北極星": ([POLARIS], "北極星", "Polaris", "北極星（勾陳一）", "white", "今天的鐘心"),
    "Arktouros": ([ARCTURUS], "Ἀρκτοῦρος", "Arktouros, Bear-guard", "守熊的人", "purple",
                  "greek_almagest；Hesiod WD 566"),
    "牧夫座": (YOU + ZUO + [ARCTURUS], "Βοώτης", "Boötes, the Ploughman", "牧夫座", "purple", "greek_almagest Boo"),
    "Fávdna": ([ARCTURUS], "Fávdna", "Fávdna, the Hunter", "獵人（大角）", "green", "sami 005；A-21"),
    "弓": (DIPPER, "Fávdna 的弓", "Favdna's Bow", "弓（北斗）", "green", "sami 002"),
    "Sipé Phairó": (DIPPER, "Sipé Phairó", "Snake Large Anus", "大蛇（北斗）", "green", "tukano 011；Cardoso 2007 p.195"),
    "siõka": ([ARCTURUS], "siõka", "light (illuminates the snake)", "照亮大蛇的亮光（大角）", "amber",
              "Cardoso 2007 p.154、p.195"),
    "Rāmiḥ": ([ARCTURUS], "السماك الرامح", "al-Simāk al-Rāmiḥ", "拿長矛的 Simāk（大角）", "red",
              "arabic_indigenous ThSl『The Armed One』"),
    "Aʿzal": ([SPICA], "السماك الأعزل", "al-Simāk al-Aʿzal", "沒帶武器的 Simāk（角宿一）", "blue",
              "arabic_indigenous SmkA『The Unarmed One』"),
    "Hōkūleʻa": ([ARCTURUS], "Hōkūleʻa", "Star of Gladness", "喜悅之星（大角）", "amber", "hawaiian_starlines；A-09"),
    "Hikianalia": ([SPICA], "Hikianalia", "Hikianalia", "角宿一", "blue", "hawaiian_starlines"),
    "大角-距離": ([ARCTURUS], "大角", "Arcturus · 36.7 ly", "大角・37 光年", "amber", "Hipparcos 2007 視差 88.83 mas"),
    "角宿一-距離": ([SPICA], "角宿一", "Spica · ~250 ly", "角宿一・約 250 光年", "blue", "視差 13.06 mas"),
    "五帝座一": ([DENEBOLA], "五帝座一", "Denebola (β Leo)", "五帝座一（獅子尾巴）", "white", "chinese"),
    "常陳一": ([COR_CAROLI], "常陳一", "Cor Caroli (α² CVn)", "常陳一", "white", "chinese"),
    "軒轅十四": ([REGULUS], "軒轅十四", "Regulus (α Leo)", "軒轅十四", "purple", "Stellarium modern SpT 用它"),
    "春季大三角": ([ARCTURUS, SPICA, DENEBOLA], "春季大三角", "Spring Triangle", "春季大三角", "amber",
              "台灣、日本課本版（五帝座一）"),
    "春季大鑽石": ([ARCTURUS, SPICA, DENEBOLA, COR_CAROLI], "春季大鑽石", "Great Diamond", "春季大鑽石", "blue",
              "modern GDi"),
    "月牙": ((0, 0), "月牙", "crescent Moon (7%)", "月牙（19:30，13°）", "white", "PyEphem；4/9 19:30 台北"),
    "木星": ((0, 0), "木星", "Jupiter", "木星（行星）", "amber", "PyEphem；20:00"),
    "火星": ((0, 0), "火星", "Mars", "火星（行星）", "red", "PyEphem；20:00"),
    "Svātī": ([ARCTURUS], "Svātī", "Svati, the self-mover", "第十五月站（大角）", "amber",
              "indian／indian_nakshatras Naks15；梵文一律 IAST"),
    "Citrā": ([SPICA], "Citrā", "Chitra, the bright one", "第十四月站（角宿一）", "blue", "indian Naks14"),
}


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    arc1, arc2, rho, off, ctr = arc_points(S)
    for i, (ra, dec) in enumerate(arc1 + arc2):
        pass
    A1 = [ARC0 + i for i in range(len(arc1))]
    A2 = [ARC0 + 500 + i for i in range(len(arc2))]
    for h, (ra, dec) in zip(A1 + A2, arc1 + arc2):
        S[h] = (ra, dec, 99.0)
    ecl = ecliptic_points()
    EC = [ECL0 + i for i in range(len(ecl))]
    for h, (ra, dec) in zip(EC, ecl):
        S[h] = (ra, dec, 99.0)
    BODY = {MOON: body_radec("Moon", T_TPE["1930"]), JUP: body_radec("Jupiter", T_TPE["2000"]),
            MARS: body_radec("Mars", T_TPE["2000"])}
    for h, (ra, dec, _, _) in BODY.items():
        S[h] = (ra, dec, 99.0)
    S[NCP] = (0.0, 90.0, 99.0)
    T = TERMS
    for nm, h in (("月牙", MOON), ("木星", JUP), ("火星", MARS)):
        T[nm] = ((round(BODY[h][0], 3), round(BODY[h][1], 3)),) + T[nm][1:]
    LG, LNAME = build_lines(A1, A2, EC)

    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    # 標記層：假星的點大小用 MARK_V（本身 V=99 才不會進 L2 星點層）
    _orig = m._mark_parts

    def _mark_parts(hips, positions, style):
        out = []
        for h in hips:
            if h in MARK_V:
                r = m.sz_star(MARK_V[h]) * 1.5
                out += [(p[0], p[1], r if style == "dot" else max(1.1, r * 4.0)) for p in positions(h)]
            else:
                out += _orig([h], positions, style)
        return out
    m._mark_parts = _mark_parts

    # ── 構圖工具 ──
    def disc_xy(h, rot):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        keep = m.lst
        m.lst = LST0 - rot
        p = m.pos_disc(ra, dec, True)
        m.lst = keep
        return (p[0][0], p[0][1] + yp) if p else None

    def safe(cx, cy, f):
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yp)
                   for sx in (-1, 1) for sy in (-1, 1)) <= m.R_fill - 1.0

    def dfit(hips, rot, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None):
        pts = [p for p in (disc_xy(h, rot) for h in hips) if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while not safe(cx, cy, f):
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def hfit(hips, rot, fov, fh=0.16, dx=0.0):
        """面北＋地平線：北點（盤心正下方 kφ）放在離畫面下緣 fh 的高度，目標星水平置中"""
        pts = [p for p in (disc_xy(h, rot) for h in hips) if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        y_h = yp - k * PHI
        cx = (max(xs) + min(xs)) / 2 + dx
        f = fov
        cy = y_h + (0.5 - fh) * f * 16 / 9
        while not safe(cx, cy, f):
            f *= 0.99
            cy = y_h + (0.5 - fh) * f * 16 / 9
        top = cy + 0.5 * f * 16 / 9 * 0.87
        if max(ys) > top:
            print(f"  ⚠ hfit：最高的星超出上緣安全區 {max(ys) - top:+.1f}（fov {f:.1f}）")
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def bxy(h):                                # 長圖（帶內／盤本體）主位置
        ra, dec = S[h][:2] if isinstance(h, int) else h
        return m.pos_primary(ra, dec)

    def sfit(hips, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None, band=False):
        pts = [bxy(h) for h in hips]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        if band:                                # S：|cy|＋fov·8/9 ≤ D_s
            lim = m.Ds - f * 8 / 9 - 0.3
            cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    # ── 長圖構圖 ──
    F01a = sfit(DIPPER, fov=60.0)
    F01b = sfit(DIPPER, fov=44.0)
    F02a = F01b                                      # 02 起格＝01 迄格（同框，一頁兩用）
    F02b = (0.0, 36.0, 50.0, 0.0)                    # 開陽、搖光（上緣）→大角
    F03 = (0.0, 8.0, 50.0, 0.0)                      # 大角＋角宿一（T：只要 cx＝0）
    F04 = (0.0, 22.0, 50.0, 0.0)                     # 全弧：開陽 y 58、角宿一 −11
    F05a = (0.0, 31.0, 62.0, 0.0)                    # 北斗＋攝提＋角宿
    ORIGIN = (0.0, 0.0, 50.0, 0.0)                   # 換組出發點（gen_canva_pages：回中心＝(x_t, 0, f_sw)）
    HAND = (0.0, yp, 50.0, 0.0)                      # 盤心換組格（盤緣圈內，逐點重合）；yp 不取整才會併頁
    F08 = sfit(SEG_BOO[0] + [h for s in SEG_BOO for h in s], pad=0.10, fov=54.0, dy=-3.0)
    F09a = sfit(DIPPER + [ARCTURUS], pad=0.12, fov=58.0, dy=-2.0)
    F09b = sfit(DIPPER + [ARCTURUS], pad=0.12, fov=52.0, dy=-2.0)
    F09c = sfit([ARCTURUS, SPICA], fov=50.0, band=True)
    F10 = F09c
    ax_, ay_ = bxy(ARCTURUS); sx_, sy_ = bxy(SPICA)
    F11 = (round(ax_, 2), round(ay_, 2), 30.0, 0.0)
    F12 = (round(sx_, 2), round(sy_, 2), 30.0, 0.0)
    F13a = sfit([ARCTURUS, SPICA, DENEBOLA], pad=0.12, fov=52.0, band=True)
    F13b = sfit([ARCTURUS, SPICA, DENEBOLA, COR_CAROLI], pad=0.12, fov=54.0)
    F13c = sfit([ARCTURUS, SPICA, DENEBOLA, COR_CAROLI, REGULUS], pad=0.08)

    # ── 北盤構圖 ──
    R06 = ROT["dusk0409"]
    F06 = dfit(DIPPER + [POLARIS], R06, pad=0.30, minfov=56.0)
    F07a = dfit(DIPPER + [POLARIS], ROT["han"], fov=F06[2])
    F07b = dfit(DIPPER + [POLARIS], ROT["dusk0321"], fov=F06[2])
    F07c = dfit(DIPPER + [POLARIS], R06, fov=F06[2])
    # 14：面北的盤上，「往西／往東看」＝畫面往左／右移（地平線是往兩側翹的弧）。
    #   19:30 月牙（x −94，地平線上 13°）放在畫面左三分之一；21:00 大角（x +86）、角宿一（x +104，盤上 y 96）
    #   ＋東方地平線（x 80 一帶 y≈−22）要同框：fov 92、畫面中心 (80, +36)，角落距盤心 171 < R_fill 174.7。
    #   木星、火星在頭頂偏西南（盤上 x −26…−17、y +99），跟東方的弧不可能同框 → 只放在圖卡 C-X04-06。
    mx, my = disc_xy(MOON, ROT["1930"])
    F14a = (round(mx + 24.0, 2), round(yp - k * PHI + 0.32 * 84.0 * 16 / 9, 2), 84.0, ROT["1930"])
    F14b = (80.0, round(yp + 36.0, 2), 92.0, ROT["2100"])
    F15 = dfit([ARCTURUS, SPICA], ROT["2100"], pad=0.30, minfov=56.0, dx=-4.0, dy=-3.0)
    for nm_, fr_ in (("F14a", F14a), ("F14b", F14b)):
        assert safe(*fr_[:3]), nm_ + " 角落出了填滿圓"
    FR = dict(F01a=F01a, F01b=F01b, F02a=F02a, F02b=F02b, F03=F03, F04=F04, F05a=F05a, ORIGIN=ORIGIN,
              F06=F06, F07a=F07a, F07b=F07b, F08=F08, F09a=F09a, F09b=F09b, F09c=F09c, F11=F11, F12=F12,
              F13a=F13a, F13b=F13b, F13c=F13c, F14a=F14a, F14b=F14b, F15=F15)
    print("\n── 構圖 ──")
    for kk, v in FR.items():
        print(f"  {kk} {v}")
    print("  旋轉：" + "、".join(f"{kk} {v:+.1f}°" for kk, v in ROT.items()))

    # ════════════════════ 標籤 ════════════════════
    # 長圖：dx/dy＝畫布方向（東在左，+dx＝往右）；盤：畫面方向（原生字不跟著盤轉）
    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        v = [sum(vec(*S[h][:2])[i] for h in a) for i in range(3)]
        ra, dec = radec(v)
        return {"ra": round(ra, 3), "dec": round(dec, 3)}

    def lab(key, fov, dx=0.0, dy=0.0, px=48, zh=None, two=False, px2=38, gap=None, disc=False, col=None):
        """一條標籤；px＝想要的 Canva 字級（1080 寬）。two＝原文＋中譯兩行"""
        a, orig, en, zh0, c, _ = T[key]
        s1 = px * fov / (m.fu * 1080)
        out = []
        if two:
            s2 = px2 * fov / (m.fu * 1080)
            g = gap if gap is not None else (s1 + s2) * m.fu * 0.62
            out.append(dict(anchor(a), text=orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy + g / 2, 2), key=key))
            out.append(dict(anchor(a), text=zh or zh0, color="white", size=round(s2, 3), dx=round(dx, 2),
                            dy=round(dy - g / 2, 2), key=key + "-zh"))
        else:
            out.append(dict(anchor(a), text=zh or orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy, 2), key=key))
        if disc:
            for it in out:
                it["disc"] = True
        return out

    f1, f2, f4, f5 = F01b[2], F02b[2], F04[2], F05a[2]
    LB = {}
    LB["北斗"] = lab("北斗", f1, dx=4.0, dy=-9.0, zh="北斗七星", px=52)
    LB["弧線"] = (lab("開陽", f2, dx=6.5, dy=1.0, px=42) + lab("搖光", f2, dx=-6.5, dy=-1.5, px=42)
                + lab("大角", f2, dx=-1.0, dy=-4.5, px=52))
    LB["角宿一"] = lab("角宿一", F03[2], dx=0.0, dy=-4.5, px=52)
    LB["全弧"] = LB["弧線"] + LB["角宿一"]
    LB["中國"] = (lab("北斗-中", f5, dx=6.0, dy=-11.0, px=50)
                + lab("大角", f5, dx=0.0, dy=-4.5, px=50, col="green")
                + lab("左攝提", f5, dx=0.5, dy=4.5, px=42) + lab("右攝提", f5, dx=4.0, dy=-4.5, px=42)
                + lab("角宿", f5, dx=7.0, dy=-1.0, px=46) + lab("角宿一", f5, dx=0.0, dy=-4.5, px=42))
    # 盤（06、07）：字在畫面方向
    f6 = F06[2]
    LB["搖光-盤"] = lab("搖光", f6, dx=0.0, dy=-3.6, px=46, disc=True, zh="搖光（斗柄末端）")
    LB["天北極"] = lab("天北極", f6, dx=0.0, dy=-3.2, px=42, disc=True)
    LB["北極星"] = lab("北極星", f6, dx=0.0, dy=-3.2, px=42, disc=True)
    f8 = F08[2]
    LB["希臘"] = (lab("Arktouros", f8, dx=-1.0, dy=-5.0, px=50, two=True, px2=38)
                + lab("牧夫座", f8, dx=13.0, dy=12.0, px=46, two=True, px2=36))
    f9 = F09a[2]
    LB["薩米"] = (lab("Fávdna", f9, dx=0.0, dy=-5.5, px=50, two=True, px2=38)
                + lab("弓", f9, dx=6.0, dy=-11.5, px=46, zh="Fávdna 的弓（北斗）"))
    f9b = F09b[2]
    LB["圖卡諾"] = (lab("Sipé Phairó", f9b, dx=6.0, dy=-11.0, px=48, two=True, px2=36)
                 + lab("siõka", f9b, dx=0.0, dy=-5.0, px=46, two=True, px2=34))
    f9c = F09c[2]
    LB["阿拉伯"] = (lab("Rāmiḥ", f9c, dx=-1.0, dy=-5.0, px=52, two=True, px2=36)
                 + lab("Aʿzal", f9c, dx=0.0, dy=-5.0, px=52, two=True, px2=36))
    LB["夏威夷"] = (lab("Hōkūleʻa", f9c, dx=-1.0, dy=-5.0, px=52, two=True, px2=38)
                 + lab("Hikianalia", f9c, dx=0.0, dy=-4.5, px=52))
    LB["大角-近"] = lab("大角-距離", 30.0, dx=0.0, dy=-3.2, px=52, two=True, px2=40)
    LB["角宿一-近"] = lab("角宿一-距離", 30.0, dx=0.0, dy=-3.2, px=52, two=True, px2=40)
    f13a, f13b, f13c = F13a[2], F13b[2], F13c[2]
    LB["三角"] = (lab("大角", f13a, dx=-1.0, dy=-4.0, px=44) + lab("角宿一", f13a, dx=0.0, dy=-4.0, px=44)
                + lab("五帝座一", f13a, dx=1.0, dy=-4.0, px=44)
                + lab("春季大三角", f13a, dy=-2.0, px=52, col="amber"))
    LB["鑽石"] = (lab("大角", f13b, dx=-1.0, dy=-4.2, px=44) + lab("角宿一", f13b, dx=0.0, dy=-4.2, px=44)
                + lab("五帝座一", f13b, dx=1.0, dy=-4.2, px=44) + lab("常陳一", f13b, dx=0.0, dy=4.0, px=44)
                + lab("春季大鑽石", f13b, dx=0.0, dy=9.0, px=52))
    LB["軒轅十四"] = (lab("大角", f13c, dx=-1.0, dy=-5.6, px=44) + lab("角宿一", f13c, dx=0.0, dy=-5.6, px=44)
                  + lab("五帝座一", f13c, dx=1.0, dy=-5.6, px=44) + lab("常陳一", f13c, dx=0.0, dy=5.2, px=44)
                  + lab("軒轅十四", f13c, dx=-4.0, dy=-5.6, px=44))
    f14a, f14b, f15 = F14a[2], F14b[2], F15[2]
    LB["台北19:30"] = lab("月牙", f14a, dy=-4.5, px=52, disc=True)
    LB["台北21:00"] = (lab("大角", f14b, dx=0.0, dy=-4.8, px=50, disc=True)
                     + lab("角宿一", f14b, dx=0.0, dy=-4.8, px=50, disc=True))
    LB["月站"] = (lab("Svātī", f15, dx=0.0, dy=-4.6, px=54, two=True, px2=38, disc=True)
                + lab("Citrā", f15, dx=0.0, dy=-4.6, px=54, two=True, px2=38, disc=True))
    label_sets = [(v, k2) for k2, v in LB.items()]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    LG_MAIN = LG["斗"] + LG["弧1"] + LG["弧2"]
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), ([MOON, JUP, MARS], "月亮與行星", "dot"),
             (NAKS, "月站標記", "ring")]
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_MAIN, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)

    LINES_KEY = dict({"L4": "星座連線", "月": "月亮與行星", "站": "月站標記"}, **LNAME)
    LINE_GROUPS = dict({"L4": LG_MAIN}, **LG)

    # ════════════════════ 鏡頭 ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=12, north=True, frames=[F01a, F01b], layers=["斗"],
             labels=[], labels_end=ls("北斗"),
             vo="上週，北斗在全世界活出了十種人生。今天換個用法：把它當成路標。同一片星空，觀星的人看見——一條找星星的路。",
             card="一條找星星的路",
             note="開場字卡；長圖（北斗在盤緣圈內＝與北盤逐點相同）Z 推近北斗（白）；"
                  "X-03 的十種連線快速閃過一輪（0.3 秒一個，美宣從 X-03 素材取）後只留白線"),
        dict(code="02", kind="Z", sec=20, north=True, frames=[F02a, F02b], layers=["斗", "弧1"],
             labels=ls("弧線"), labels_start=ls("北斗"),
             vo="先找北斗：這幾天晚上八點，它在東北方半天高，斗柄朝右下。順著斗柄彎的方向，畫一道大弧出去——"
                "手臂伸直，大約三個拳頭遠，你會碰到一顆橘色的亮星：北半天球最亮的恆星，大角。英文口訣叫 arc to Arcturus。",
             card="arc to Arcturus",
             note="02 起格＝01 迄格；沿走廊從北斗滑下來到大角（Z：起格畫面中心 x +9.9 才放得下整個斗身，迄格回到走廊中線 x 0）；弧線（琥珀，過開陽、搖光、大角的圓弧，從開陽起畫）逐段淡入；"
                  "畫面角落「手臂伸直，三個拳頭＝約 30°」手勢示意（美宣 Canva 自繪，不另出圖）"),
        dict(code="03", kind="T", sec=12, north=True, frames=[F02b, F03], layers=["斗", "弧1", "弧2"],
             labels=ls("全弧"), labels_start=ls("弧線"),
             vo="再順著同一道弧，往南延伸差不多一樣遠，就會看到一顆藍白色的星：角宿一。口訣的下半句——spike to Spica，衝到角宿一。",
             card="spike to Spica",
             note="續往下；弧線第二段（琥珀）大角→角宿一淡入（星圖方向：實際天空裡角宿一跟大角差不多高、在它右邊）"),
        dict(code="04", kind="T", sec=14, north=True, frames=[F03, F04], layers=["斗", "弧1", "弧2"],
             labels=ls("全弧"), overlay="C-X04-01_弧線是真的", overlay_layers=["星點層", "圓層", "偏差層"],
             vo="這道弧不是硬湊的：斗柄尾端的開陽、搖光，加上大角、角宿一，幾乎就在同一個圓上。"
                "連天文軟體 Stellarium，都把這條線內建成指星的輔助線。",
             card="四顆星，同一個圓",
             note=f"拉遠到整道弧；迄格定格疊 C-X04-01（星點→圓 半徑 {rho:.1f}°→開陽 {off[MIZ]:.2f}°、玉衡 {off[ALI]:.1f}°）；"
                  "「連天文軟體」起切 Stellarium 介面截圖（RH1 原樣兩段直線；美宣自行截取，GPL 軟體畫面，不放商標）"),
        dict(code="05", kind="Z", sec=18, north=True, frames=[F05a, ORIGIN], layers=["中"],
             labels=ls("中國"),
             vo="兩千多年前，中國人也把它們連在一起。《史記》寫：大角旁邊的攝提，「直斗杓所指，以建時節」——"
                "斗柄指向哪裡，就靠它定季節；還說「杓攜龍角」：斗柄連著青龍的角——角宿，最亮的那顆，就是角宿一。",
             card="杓攜龍角",
             note="中國星官層：北斗（琥珀）、大角＋左右攝提（綠；左攝提在大角東側＝牧夫 ο π ζ，右攝提在西側＝η τ υ）、"
                  "角宿兩顆（藍，龍角）；迄格回到帶中央（＝換北盤的出發點）；青龍輪廓可從 A-01 素材淡淡帶出"),
        dict(code="06", kind="R", sec=17, north=True, frames=[HAND, F06], layers=["斗"],
             labels=ls("搖光-盤"), labels_start=[], labels_end=ls("搖光-盤", "北極星"),
             overlay="C-X04-02_斗柄鐘面", overlay_layers=["鐘面層", "四季層"],
             vo="另一本古書《鶡冠子》說得更乾脆：「斗柄東指，天下皆春；斗柄南指，天下皆夏。」"
                "今天可以這樣看：黃昏時，把北極星當鐘面中心，斗柄末端轉到三點鐘、也就是東邊，就是春天。",
             card="斗柄東指，天下皆春",
             note=f"【換組】長圖沿走廊上到北極→同框換北盤；盤逆時針轉到台北 4/9 黃昏面北（{R06:+.1f}°：搖光在北極星右邊＝三點鐘）；"
                  "迄格定格疊 C-X04-02（鐘面 9:16 圖卡式方形圖：三點＝春、十二點＝夏、九點＝秋、六點＝冬，"
                  "「北＝冬」虛線＋小字「今天台灣冬天黃昏，搖光在地平線下」）"),
        dict(code="07", kind="R", sec=14, north=True, frames=[F07a, F07b, F07c], layers=["斗"],
             labels=ls("搖光-盤"), labels_start=ls("搖光-盤", "天北極"), labels_end=ls("搖光-盤", "北極星"),
             vo="照這個看法，兩千年前，這發生在春分的黃昏；地軸慢慢晃，今天要晚大約三個星期——"
                "就是這幾天：黃昏時，斗柄末端剛好轉到北極星的正東邊。",
             card="晚了大約三個星期",
             note=f"北盤三格：漢代長安春分黃昏（搖光 86°，{ROT['han']:+.1f}°；圓心是天北極，盤上不標北極星）"
                  f"→ 台北今年春分 3/21 黃昏（110°＝還沒轉到東，{ROT['dusk0321']:+.1f}°）"
                  f"→ 台北 4/9 黃昏（89°，正東，{R06:+.1f}°；標北極星）"),
        dict(code="08", kind="Z", sec=21, north=True, frames=[F08], layers=["牧"],
             labels=ls("希臘"), overlay="C-X04-03_赫西俄德的黃昏",
             overlay_layers=["前700層", "阿斯克拉2027層", "台北層"],
             vo="希臘人叫大角 Arktouros，守熊的人。兩千七百年前，詩人赫西俄德寫：冬至後六十天，大角在黃昏升起，"
                "就該修剪葡萄藤。地軸在晃，台灣又比希臘偏南，今年這一幕就在這個星期：太陽一下山，大角就從東北東升起。",
             card="冬至後六十天",
             note="【換組】北盤歸位→同框換長圖→沿走廊下來（自動插頁）；大角＋希臘牧夫座（紫，greek_almagest）；"
                  "定格疊 C-X04-03（前 700 年阿斯克拉 冬至後 62 天 → 2027 阿斯克拉 4/1 → 2027/4/9 台北 日落 18:13、大角 18:20、方位 68.5°）"),
        dict(code="09", kind="Z", sec=6, north=True, frames=[F08, F09a], layers=["弓"],
             labels=ls("薩米"), labels_start=[],
             vo="北極圈的薩米人說：大角是獵人 Fávdna，北斗是他的弓。",
             card="北斗的搭檔",
             note="薩米 Fávdna＋弓（綠，Stellarium sami 002：搖光→天璇是弓弧、天樞—天璣是箭；同 A-21）"),
        dict(code="09b", kind="Z", sec=6, north=True, frames=[F09a, F09b], layers=["蛇"],
             labels=ls("圖卡諾"), labels_start=ls("薩米"),
             vo="亞馬遜的圖卡諾人說，大角是照亮北斗那條大蛇的亮光。",
             card="北斗的搭檔",
             note="弓淡出、圖卡諾大蛇 Sipé Phairó（綠，tukano 011：北斗七顆串成一條）淡入；大角光暈"),
        dict(code="09c", kind="Z", sec=8, north=True, frames=[F09b, F09c], layers=[],
             labels=ls("阿拉伯"), labels_start=ls("圖卡諾"),
             vo="阿拉伯人則把大角和角宿一配成一對：大角是「拿長矛的 Simāk」，角宿一是「沒帶武器的 Simāk」。",
             card="長矛 vs 空手",
             note="滑到大角—角宿一；阿拉伯標籤 السماك الرامح／السماك الأعزل（SVG 已整形；Canva 原生輸入時字型要支援阿拉伯文）"),
        dict(code="10", kind="S", sec=15, north=True, frames=[F10], layers=["夏"],
             labels=ls("夏威夷"), overlay="C-X04-07_兩顆星同時升起", overlay_layers=["檀香山層", "台北層"],
             vo="夏威夷人說大角是 Hōkūleʻa，喜悅之星；角宿一是 Hikianalia。在夏威夷，這兩顆星幾乎同時從東方升起；"
                "近代復航的兩艘航海獨木舟，就用它們命名。",
             card="同時升起的兩顆星",
             note="畫面不動；夏威夷脊椎骨星線只亮大角—角宿一段（藍）；定格疊 C-X04-07（檀香山 vs 台北 4/9 東方地平線，"
                  "升起時刻差 1.3 分 vs 8 分）；獨木舟照片美宣另尋授權圖"),
        dict(code="11", kind="Z", sec=20, north=True, frames=[F10, F11], layers=[],
             labels=ls("大角-近"), labels_start=ls("夏威夷"), overlay="C-X04-04_大角在走路",
             overlay_layers=["星點層", "軌跡層"],
             vo="大角離我們三十七光年，是一顆半徑膨脹到太陽二十五倍的橘色巨星。它跑得特別快：每八百多年，"
                "就在天上移動一個月亮那麼寬——一七一八年，哈雷拿它的位置跟古希臘的星表比對，才發現星星自己會走。",
             card="星星自己會走",
             note="推近大角；迄格定格疊 C-X04-04（托勒密時代 → 今天 → 西元 3000 年，月亮直徑當比例尺）"),
        dict(code="12", kind="Z", sec=12, north=True, frames=[F11, F12], layers=[],
             labels=ls("角宿一-近"), labels_start=ls("大角-近"),
             vo="角宿一更遠，大約兩百五十光年；它其實是兩顆藍色的大星，貼得很近，四天繞一圈。今晚看到的光，是乾隆年間出發的。",
             card="乾隆年間出發的光",
             note="滑到角宿一（藍白）；字卡"),
        dict(code="13", kind="Z", sec=14, north=True, frames=[F13a, F13b, F13c], layers=["三", "鑽", "軒"],
             labels=ls("鑽石"), labels_start=ls("三角"), labels_end=ls("軒轅十四"),
             overlay="C-X04-05_春季大三角與大鑽石",
             vo="大角、角宿一，再加上獅子座尾巴的五帝座一，是春季大三角；再補上獵犬座的常陳一，就是春季大鑽石。"
                "小提醒：有的星圖用軒轅十四代替五帝座一。",
             card="春季大三角＋大鑽石",
             note="三格：春季大三角（琥珀）→ 補常陳一成大鑽石（藍）→ 拉遠帶進軒轅十四版三角（紫，Canva 透明度 60%）；"
                  "連線層三層都開、照旁白依序淡入；迄格疊 9:16 圖卡 C-X04-05（可存圖）"),
        dict(code="14", kind="R", sec=22, north=True, horizon=[PHI], frames=[F14a, F14b], layers=["斗", "月"],
             labels=ls("台北21:00"), labels_start=ls("台北19:30"), overlay="C-X04-06_今晚抬頭看",
             vo="今晚怎麼看：七點半天全黑，西北西低空有一彎很細的月牙，七點四十五分以後就太低了。九點，北斗在北方偏東，"
                "大角在正東方三十多度高，角宿一在東南東。頭頂附近最亮的兩顆不是恆星，是木星和火星——別把它們算進春季大三角。",
             card="七點半看西｜九點往東",
             note=f"【換組】長圖回中心→上移→同框換北盤；台北 4/9 面北（山＝北方地平線，φ 25.03°）："
                  f"19:30（{ROT['1930']:+.1f}°）畫面偏西、月牙在左下 → 「九點」起 21:00（{ROT['2100']:+.1f}°）畫面移到東邊："
                  "大角（東，34°）、角宿一（東南東，31°）、北斗在左上角；木星與火星在頭頂偏西南，跟東方的弧放不進同一格，只在圖卡 C-X04-06 標「行星」；字卡前 7 秒「七點半看西」，之後「九點往東」；"
                  "迄格疊 9:16 圖卡 C-X04-06（可存圖）"),
        dict(code="15", kind="R", sec=12, north=True, horizon=[PHI], frames=[F14b, F15], layers=["黃", "站"],
             labels=ls("月站"), labels_start=ls("台北21:00"),
             vo="角宿一在印度叫 Citrā，大角叫 Svātī——它們都是月亮的妻子。下週五，去見見另外二十五位：印度，月亮的二十七位妻子。",
             card="下集見｜印度：月亮的 27 位妻子",
             note="同一片台北東方天空推近大角、角宿一；黃道（白細線）＋月站標記（細圈，indian_nakshatras 27 宿）淡入，"
                  "只標 Citrā、Svātī；端卡「下集見｜印度：月亮的 27 位妻子」＋追蹤 CTA"),
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

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                which = "北盤圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off_ = (round(-cx / fov * 1080), round((cy - m.y_pole) / fov * 1080))
            else:
                which = "大畫布圖層組"
                ew = 360.0 / fov * 1080
                off_ = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off_[0],
                         "位移Y px": off_[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    # 數字核對（逐字稿星空對時表）
    print("\n── 數字核對 ──")
    print(f"  弧：半徑 {rho:.2f}°，圓心 RA {ctr[0]:.1f} Dec {ctr[1]:+.1f}；離圓：開陽 {off[MIZ]:.2f}°、玉衡 {off[ALI]:.2f}°、天權 {off[MEG]:.2f}°")
    print(f"  角距：搖光—大角 {sep(S, ALK, ARCTURUS):.1f}°、大角—角宿一 {sep(S, ARCTURUS, SPICA):.1f}°、"
          f"搖光—角宿一 {sep(S, ALK, SPICA):.1f}°；三角 {sep(S, ARCTURUS, SPICA):.1f}／{sep(S, SPICA, DENEBOLA):.1f}／{sep(S, DENEBOLA, ARCTURUS):.1f}；"
          f"五帝座一—常陳一 {sep(S, DENEBOLA, COR_CAROLI):.1f}、常陳一—大角 {sep(S, COR_CAROLI, ARCTURUS):.1f}；"
          f"角宿一—軒轅十四 {sep(S, SPICA, REGULUS):.1f}、軒轅十四—大角 {sep(S, REGULUS, ARCTURUS):.1f}")
    for kk, v in LST_AT.items():
        print(f"  {T_TPE[kk]} LST {v:.2f} → 北盤 {ROT[kk]:+.1f}°；搖光方向 {(-(v - ALK_RA) + 180) % 360 - 180:.1f}°")
    for nm, h in (("月", MOON), ("木", JUP), ("火", MARS)):
        ra, dec, alt, az = BODY[h]
        print(f"  {nm} RA {ra:.2f} Dec {dec:+.2f}（高 {alt:.1f}° 方位 {az:.1f}°）")

    terms = {}
    for key, (a, orig, en, zh, col, note) in T.items():
        terms[key] = dict(hips=a if isinstance(a, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                          顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV_LINES = LG_MAIN + LG["中"] + LG["三"] + LG["鑽"]
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=PREV_LINES,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    import make_a21_v4 as A21
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_MAIN)
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k2 in sh.get("layers", []) if k2 in LG for x in LG[k2]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    A21.sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
                title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
