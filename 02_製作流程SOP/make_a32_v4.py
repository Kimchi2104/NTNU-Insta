# -*- coding: utf-8 -*-
"""A-32 阿拉伯月站：月亮每晚的下榻處｜大畫布 v4.6（長圖帶狀為主・沿黃道 S 捲動；北盤只在 14 鏡做全環總覽）

論點：二十八間旅店的招牌，寫的是沙漠生活（大獅子、大蠍子、鴕鳥群、空地、四間吉星、一口井）；
本集的新東西＝跟著月亮走一週、招牌掛上今天的星圖（Aldebaran、Shaula、Zubenelgenubi）、跟中國二十八宿對照。

來源：Stellarium arabic_indigenous（新版 stellarium-master/skycultures；Khalid al-Ajaji；28 站連線、
  lunar_system＝28 等分、第 1 站中心＝昴宿六 Alcyone）、chinese（舊版；二十八宿連線）、western（仙女座）。
逐字稿：04_腳本庫/A-32-阿拉伯月站月亮每晚的下榻處-逐字稿-v1.md。天象 PyEphem 4.2.1 自算（台北站心，轉 J2000）。

自訂層（大畫布＋南北盤同步出）
  黃道（J2000，淡藍灰虛線）；單星站圈（昴宿、跟在後面的、轉變、高舉者、心臟——Stellarium 只有一顆星或星團，
  連線層畫不出來，改琥珀細圈）；al-Baldah 空地（Stellarium 新版的暗星圈，琥珀虛線，不畫星）；
  站界框（第 4、7、8、23、24 站：等分站界 ±12.86°/2、黃緯 ±8°，琥珀虛線）；
  月亮一週（5/25–5/28 清晨 04:30，01 鏡）、月亮週末（5/29、5/30 04:30，07 鏡）、眉月 6/6 19:10（13 鏡）——
  月相照 PyEphem 亮面比例與太陽方向畫，圖示放大約 3 倍（示意）；行星 5/28 20:00（木星、火星，12 鏡）；
  跟隨箭頭（畢宿五 → 昴宿，08 鏡）；兩環（北盤 r 36–44＝月站 28 等分、r 48–56＝二十八宿依距星赤經不等寬，14 鏡）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 220 → 長圖切口 x＝±180 在 RA 40（白羊 Hamal 與昴宿之間）：本集上長圖的天區從 仙女／白羊（x −142…−172）
             一路到 昴宿（x +163），只有 RA 33–55 那 22° 沒用到，切口放這裡。走廊 x=0＝RA 220（天秤 α 西邊）。
             x：昴宿 +163、畢宿五 +151、雙子 μ +124、軒轅十四 +68、角宿一 +19、氐宿一 −3、心宿二 −27、
             尾宿八 −43、鴕鳥群 −51…−66、空地 −71…−77、牛宿一 −85、帳篷的吉星 −115、飛馬大四方形 −126…−143。
  D_s = 60、D_r = 64 → 決定因素是 01 鏡的大全景（fov 60）：黃道在 Cap／Aqr 一帶 dec −20…−5，
             fov 60 時 |cy| ≤ 6.7（S／Z 長圖帶內不出界）。帶內也容得下大魚（ν And +41）、天蠍尾（−43）。
             北天沒有主角（14 鏡的兩環是示意層，畫在盤緣圈內 dec 64.6–73.7）。
  D_fill = 15 → k＝2.2037、R_fill＝165.276（盤寬 ÷ 畫布寬＝0.918200，與 H-七夕、A-03 相同）；|x_t|+R_fill ≤ 180 ✓。
  x_tN = x_tS = 0（Canva 可水平置中）。

鏡頭路線
  01 Z 摩羯—寶瓶全景 fov 60→40（月亮一週）→ 02 S 往東捲到 寶瓶—飛馬 → 03–05 定格疊 C-A32-01／02／03
  →【硬切】06 S 天秤→天蠍→人馬→空地（逐字稿換段「二十八間旅店，名字都很有畫面」；05→06 隔 120°，滑過去是甩鏡）
  → 07 S 摩羯→寶瓶→飛馬（四間吉星、月亮 5/29→5/30 跨站界）
  →【硬切】08 Z 畢宿＋昴宿 →【硬切】08b Z 天蠍尾（逐字稿 08 鏡在「；」拆成 08／08b：同鏡兩個構圖隔 194°）
  → 09 Z 天秤兩星推近＋圖卡 C-A32-04 →【硬切】10 Z 飛馬大四方形（室壁＝水桶）→【硬切】10b Z 心宿二＋C-A32-05
  （逐字稿 10 鏡同理拆 10／10b）→ 11 Z 摩羯 β／ν（牛宿一＝屠夫）→【硬切】12 S 獅子（木星、火星）→ 角宿一 → 天秤、心宿二
  ＋圖卡 C-A32-06 →【硬切】13 Z 雙子腳邊（6/6 眉月；12→13 隔 136°）→【換組】14 R 北盤兩環 0°→−30°＋圖卡 C-A32-07
  →【換組＋硬切】15 Z 仙女座＋大魚（北盤轉長圖下移到走廊後，隔 150°，硬切）＋端卡。

  逐字稿 08 鏡 16 秒＝08 12＋08b 4；10 鏡 19 秒＝10 14＋10b 5（照字數分，每格 ≤ 4.5；總長 259 不變）。
  逐字稿 01 鏡 fov 60→30 改 60→40：fov 30 裝不下四晚的月亮（5/25–5/28 跨 35°）。
  逐字稿 10 鏡「中國二十八宿（黃）」改紫：琥珀（月站）與黃色在小螢幕分不出來。

check_shots 判斷（⚠）
  14 R 起格 fov 40＝長圖轉北盤換組格（盤心置中、只在盤緣圈內）可無縫互切；中、迄格 fov 120 含長圖側扇區，
  回程由 gen_canva_pages 的「歸位」頁先轉回 0°、縮回 fov 40 換組，不會直接切到大畫布 → 可接受。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-32"
OUT = os.path.join(BASE, "05_素材/A-32_阿拉伯月站/_v4大畫布")
LST0 = 220.0
D_S, D_R, D_FILL = 60.0, 64.0, 15.0
TPE = (25.0330, 121.5654)
PURPLE = "purple"                       # 中國二十八宿


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem 4.2.1；台北站心；J2000 astrometric）
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.temp, o.pressure = 25.0, 1010.0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def _j2k(ra, dec, epoch):
    import ephem
    q = ephem.Equatorial(ephem.Equatorial(ra, dec, epoch=epoch), epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


def ecl_to_j2000(lon, lat=0.0):
    """J2000 黃道 → J2000 赤道（度）"""
    import ephem
    q = ephem.Equatorial(ephem.Ecliptic(math.radians(lon), math.radians(lat), epoch=ephem.J2000),
                         epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


def ecl_of(ra, dec):
    import ephem
    e = ephem.Ecliptic(ephem.Equatorial(math.radians(ra), math.radians(dec), epoch=ephem.J2000),
                       epoch=ephem.J2000)
    return math.degrees(e.lon), math.degrees(e.lat)


def bodies():
    import ephem
    out = {}
    moons = [("月5/25", "2027/5/25 04:30"), ("月5/26", "2027/5/26 04:30"), ("月5/27", "2027/5/27 04:30"),
             ("月5/28", "2027/5/28 04:30"), ("月5/29", "2027/5/29 04:30"), ("月5/30", "2027/5/30 04:30"),
             ("月5/31", "2027/5/31 04:30"), ("月6/1", "2027/6/1 04:30"), ("月6/6", "2027/6/6 19:10")]
    for key, when in moons:
        o = _obs(when); b = ephem.Moon(); b.compute(o); s = ephem.Sun(); s.compute(o)
        ra, dec = _j2k(b.ra, b.dec, o.date)
        sra, sdec = _j2k(s.ra, s.dec, o.date)
        out[key] = dict(ra=ra, dec=dec, sun=(sra, sdec), frac=b.phase / 100.0,
                        alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                        phase=round(b.phase, 1), lon_j2000=round(ecl_of(ra, dec)[0], 2))
    o = _obs("2027/5/28 20:00")
    for nm, b in (("木星", ephem.Jupiter()), ("火星", ephem.Mars())):
        b.compute(o)
        ra, dec = _j2k(b.ra, b.dec, o.date)
        out[nm] = dict(ra=ra, dec=dec, alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                       mag_pyephem=round(float(b.mag), 2))
    return out


PL = bodies()


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 一、星與連線
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_new(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        out[c["id"].split()[-1]] = c
    return d, out


def segs_of(c):
    return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])
            if l and not isinstance(l[0], list)]


def load_old(cu):
    d = json.load(open(os.path.join(SC_OLD, cu, "index.json"), encoding="utf-8"))
    return {c["id"].split()[-1]: [[h for h in l if isinstance(h, int)] for l in c["lines"]]
            for c in d["constellations"]}


AI_IDX, AI = load_new("arabic_indigenous")
CH = load_old("chinese")
WE = load_old("western")

# 28 站（本土序，從昴宿起算）：(Stellarium id, 阿拉伯文, 轉寫（片中寫法）, 中譯)
STATIONS = [
    ("Thur", "الثريا", "al-Thurayyā", "昴宿"),
    ("Dabr", "الدبران", "al-Dabarān", "跟在後面的"),
    ("Haqa", "الهقعة", "al-Haqʿah", "圓斑"),
    ("Hana", "الهنعة", "al-Hanʿah", "低彎"),
    ("Maqb", "الذراع", "al-Dhirāʿ", "前臂"),
    ("Nath", "النثرة", "al-Nathrah", "鼻尖"),
    ("Tarf", "الطرف", "al-Ṭarf", "眼睛"),
    ("Jabh", "الجبهة", "al-Jabhah", "額頭"),
    ("Zubr", "الزبرة", "al-Zubrah", "鬃毛"),
    ("Sarf", "الصرفة", "al-Ṣarfah", "轉變"),
    ("Awwa", "العوّاء", "al-ʿAwwāʾ", "彎曲處"),
    ("SmkA", "السماك", "al-Simāk", "高舉者"),
    ("Ghfr", "الغفر", "al-Ghafr", "遮蓋"),
    ("Zban", "الزبانى", "al-Zubānā", "兩隻螯"),
    ("Ikll", "الإكليل", "al-Iklīl", "冠冕"),
    ("Qalb", "القلب", "al-Qalb", "心臟"),
    ("Shwl", "الشولة", "al-Shawlah", "翹起的尾巴"),
    ("Naym", "النعائم", "al-Naʿāʾim", "鴕鳥群"),
    ("Blda", "البلدة", "al-Baldah", "空地"),
    ("SDab", "سعد الذابح", "Saʿd al-Dhābiḥ", "屠夫的吉星"),
    ("SBul", "سعد بلع", "Saʿd Bulaʿ", "吞嚥者的吉星"),
    ("SSud", "سعد السعود", "Saʿd al-Suʿūd", "吉中之吉"),
    ("SAkh", "سعد الأخبية", "Saʿd al-Akhbiyah", "帳篷的吉星"),
    ("Mqdm", "الفرغ المقدم", "al-Fargh al-Muqaddam", "水桶的前口"),
    ("Mkhr", "الفرغ المؤخر", "al-Fargh al-Muʾakhkhar", "水桶的後口"),
    ("Rsha", "الرشاء", "al-Rishāʾ", "水桶的繩子"),
    ("Shrt", "الشرطان", "al-Sharaṭān", "兩個記號"),
    ("Btyn", "البطين", "al-Buṭayn", "小肚子"),
]
ST_SEGS = {k: segs_of(AI[k]) for k, *_ in STATIONS}
ST_HIPS = {k: sorted({h for s in v for h in s}) for k, v in ST_SEGS.items()}
SINGLE = ["Dabr", "Sarf", "SmkA", "Qalb"]                # 只有一顆星的站（連線層畫不出來 → 單星站圈）
SEG_ST = [s for k, v in ST_SEGS.items() for s in v if len(set(s)) >= 2]
SEG_SCORP = segs_of(AI["Aqrb"])                            # 大蠍子（含兩隻螯＝天秤）
SEG_OSTR = segs_of(AI["Naym"])                             # 鴕鳥群（去河邊喝水的、喝完離開的）
SEG_LION = segs_of(AI["Asad"])                             # 大獅子
SEG_BUCKET = segs_of(AI["Mqdm"]) + segs_of(AI["Mkhr"])     # 水桶的前口（α β Peg）、後口（γ Peg α And）
SEG_FISH = segs_of(AI["Hoot"])                             # 大魚（＝水桶繩那一圈）
SEG_AND = WE["And"]
BALDAH = [(ra * 15.0, dec) for ra, dec in AI["Blda"]["lines"][0]]

# 中國二十八宿（舊版 chinese）＋距星（J2000；不等寬環用。參宿取 ζ Ori：取 δ Ori 時觜宿寬度變負）
XIU = [("角", "009", 65474), ("亢", "011", 69427), ("氐", "004", 72622), ("房", "006", 78265),
       ("心", "026", 80112), ("尾", "024", 82514), ("箕", "008", 88635), ("斗", "005", 92041),
       ("牛", "016", 100345), ("女", "017", 102618), ("虛", "028", 106278), ("危", "023", 109074),
       ("室", "018", 113963), ("壁", "002", 1067), ("奎", "012", 3693), ("婁", "014", 8903),
       ("胃", "025", 12719), ("昴", "015", 17499), ("畢", "001", 20889), ("觜", "034", 26207),
       ("參", "003", 26727), ("井", "010", 30343), ("鬼", "007", 41822), ("柳", "013", 42313),
       ("星", "027", 46390), ("張", "030", 48356), ("翼", "029", 53740), ("軫", "031", 59803)]
SEG_XIU = [s for _, k, _ in XIU for s in CH[k]]
SEG_SHI_BI = CH["018"] + CH["002"]
SEG_XIN = CH["026"]
SEG_NIU = CH["016"]

ALCYONE, ALDEBARAN, MU_GEM, ALHENA = 17702, 21421, 30343, 31681
REGULUS, ALGIEBA, SPICA = 49669, 50583, 65474
ZUBEN_G, ZUBEN_S, ANTARES, SHAULA = 72622, 74785, 80763, 85927
DABIH, ALSHAT, ALGEDI2 = 100345, 100310, 100064
MARKAB, SCHEAT, ALGENIB, ALPHERATZ, MIRACH = 113963, 113881, 1067, 677, 5447
GAMMA_AQR = 110395
M45 = (56.75, 24.12)
MAINS = [ALDEBARAN, ALCYONE, REGULUS, SPICA, ZUBEN_G, ZUBEN_S, ANTARES, SHAULA, DABIH, ALSHAT,
         MARKAB, SCHEAT, ALGENIB, ALPHERATZ, MU_GEM, ALHENA, GAMMA_AQR, MIRACH]


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


S0 = dict(G.load_stars(BASE))
LAM0 = ecl_of(*S0[ALCYONE][:2])[0]                          # 第 1 站中心（J2000 黃經；當日＝60.37°）
WST = 360.0 / 28.0


def station_of(lam):
    return int(((lam - LAM0 + WST / 2) % 360.0) // WST) + 1


def station_range(n):
    c = LAM0 + (n - 1) * WST
    return c - WST / 2, c + WST / 2


# ══════════════════════════════════════════════════════════════════
# 二、連線層
# ══════════════════════════════════════════════════════════════════
LG_ST = [(SEG_ST, "amber", 1.0)]
LG_SCORP = [(SEG_SCORP, "red", 1.0)]
LG_OSTR = [(SEG_OSTR, "green", 1.0)]
LG_LION = [(SEG_LION, "blue", 0.85)]
LG_BUCKET = [(SEG_BUCKET, "blue", 1.0)]
LG_XIU = [(SEG_XIU, PURPLE, 0.9)]
LG_FISH = [(SEG_FISH, "green", 0.9)]
LG_AND = [(SEG_AND, "blue", 0.8)]
LG_ALL = LG_ST + LG_XIU
LINE_SETS = [(LG_SCORP, "連線-大蠍子"), (LG_OSTR, "連線-鴕鳥群"), (LG_LION, "連線-大獅子"),
             (LG_BUCKET, "連線-水桶兩口"), (LG_XIU, "連線-二十八宿"), (LG_FISH, "連線-大魚"),
             (LG_AND, "連線-仙女座")]
LINES_KEY = {"L4": "星座連線", "站": "星座連線", "蠍": "連線-大蠍子", "鴕": "連線-鴕鳥群", "獅": "連線-大獅子",
             "桶": "連線-水桶兩口", "宿": "連線-二十八宿", "魚": "連線-大魚", "仙": "連線-仙女座",
             "黃": "黃道", "圈": "單星站圈", "空": "空地al-Baldah", "界": "站界框",
             "月週": "月亮一週5月25至28日", "月末": "月亮週末5月29與30日", "眉": "眉月6月6日",
             "行": "木星與火星5月28日", "隨": "跟隨箭頭", "環": "兩環（北盤總覽）"}
LINE_GROUPS = {"L4": LG_ST, "站": LG_ST, "蠍": LG_SCORP, "鴕": LG_OSTR, "獅": LG_LION, "桶": LG_BUCKET,
               "宿": LG_XIU, "魚": LG_FISH, "仙": LG_AND}
for _k in ("黃", "圈", "空", "界", "月週", "月末", "眉", "行", "隨", "環"):
    LINE_GROUPS[_k] = []


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


def toward(a, b, deg):
    """從 a 沿大圓往 b 走 deg 度"""
    va, vb = vec(*a), vec(*b)
    d = math.radians(sep(a, b))
    t = math.radians(deg)
    if d < 1e-9:
        return a
    k1, k2 = math.sin(d - t) / math.sin(d), math.sin(t) / math.sin(d)
    return radec([va[i] * k1 + vb[i] * k2 for i in range(3)])


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層
# ══════════════════════════════════════════════════════════════════
ECL_PTS = [ecl_to_j2000(float(l)) for l in range(0, 361, 1)]
BOX_ST = [4, 7, 8, 23, 24]
RING_ST = (36.0, 44.0)               # 北盤半徑（盤緣圈 57.3 以內＝與大畫布逐點一致）
RING_XIU = (48.0, 56.0)


def custom_layers(m, S):
    AMB, ECL, MOON = COLORS["amber"], "#A9B8D6", "#F4F1E6"
    dec_r = lambda r: 90.0 - r / m.k

    def ecliptic(s, pos, runs, disc):
        s.polylines(runs(ECL_PTS), stroke=ECL, w=m.lw * 0.5, opacity=0.5, dash="1.4 0.9")

    def singles(s, pos, runs, disc):
        pts = [S[ST_HIPS[k][0]][:2] for k in SINGLE] + [M45]
        for ra, dec in pts:
            for p in pos(ra, dec):
                s.circle(p[0], p[1], 1.25 if (ra, dec) != M45 else 1.6, stroke=AMB, w=0.16, opacity=0.92)

    def baldah(s, pos, runs, disc):
        s.polylines(runs(BALDAH), stroke=AMB, w=m.lw * 0.8, opacity=0.92, dash="0.9 0.6")

    def boxes(s, pos, runs, disc):
        rr = []
        for n in BOX_ST:
            a, b = station_range(n)
            edge = ([(a + (b - a) * i / 20, -8.0) for i in range(21)] +
                    [(b, -8.0 + 16.0 * i / 8) for i in range(1, 9)] +
                    [(b - (b - a) * i / 20, 8.0) for i in range(1, 21)] +
                    [(a, 8.0 - 16.0 * i / 8) for i in range(1, 9)])
            rr += runs([ecl_to_j2000(l, bb) for l, bb in edge])
        s.polylines(rr, stroke=AMB, w=m.lw * 0.45, opacity=0.75, dash="0.8 0.6")

    def moon_icon(s, pos, key, r=0.75, glow=True, dim=1.0):
        v = PL[key]
        c = (v["ra"], v["dec"])
        for p, q in zip(pos(*c), pos(*toward(c, v["sun"], 1.0))):
            ux, uy = q[0] - p[0], q[1] - p[1]
            n = math.hypot(ux, uy) or 1.0
            ux, uy = ux / n, uy / n                       # 亮邊方向（朝太陽）
            vx, vy = -uy, ux
            if glow:
                s.circle(p[0], p[1], r * 2.2, fill="#FFFFFF", opacity=0.10 * dim)
            s.circle(p[0], p[1], r, fill="#5A5F6E", opacity=0.55 * dim)       # 暗面（地照）
            k = v["frac"]
            poly = []
            for i in range(31):                          # 亮邊半圓
                t = math.radians(-90 + 180 * i / 30)
                a, b = r * math.cos(t), r * math.sin(t)
                poly.append((p[0] + a * ux + b * vx, p[1] + a * uy + b * vy))
            for i in range(31):                          # 晨昏線（橢圓）
                t = math.radians(90 - 180 * i / 30)
                a, b = r * (1 - 2 * k) * math.cos(t), r * math.sin(t)
                poly.append((p[0] + a * ux + b * vx, p[1] + a * uy + b * vy))
            s.poly_fill([poly + [poly[0]]], fill=MOON, opacity=0.98 * dim)

    def moon_week(s, pos, runs, disc):
        keys = ["月5/25", "月5/26", "月5/27", "月5/28"]
        pts = [(PL[k]["ra"], PL[k]["dec"]) for k in keys]
        arc = []
        for a, b in zip(pts, pts[1:]):
            arc += [toward(a, b, sep(a, b) * t / 20) for t in range(3, 18)] + [None]
        run = []
        for q in arc + [None]:
            if q is None:
                if len(run) > 1:
                    s.polylines(runs(run), stroke=MOON, w=m.lw * 0.35, opacity=0.55, dash="0.7 0.6")
                run = []
            else:
                run.append(q)
        for i, k in enumerate(keys):
            moon_icon(s, pos, k, dim=0.55 + 0.15 * i)

    def moon_weekend(s, pos, runs, disc):
        a = (PL["月5/29"]["ra"], PL["月5/29"]["dec"]); b = (PL["月5/30"]["ra"], PL["月5/30"]["dec"])
        s.polylines(runs([toward(a, b, sep(a, b) * t / 20) for t in range(3, 18)]),
                    stroke=MOON, w=m.lw * 0.35, opacity=0.6, dash="0.7 0.6")
        moon_icon(s, pos, "月5/29", dim=0.7)
        moon_icon(s, pos, "月5/30")

    def crescent(s, pos, runs, disc):
        moon_icon(s, pos, "月6/6", r=0.6)

    def planets(s, pos, runs, disc):
        for nm, col, r in (("木星", "#FFFFFF", 0.45), ("火星", COLORS["red"], 0.34)):
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.8, fill=col, opacity=0.16)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    def follow(s, pos, runs, disc):
        a, b = S[ALDEBARAN][:2], M45
        d = sep(a, b)
        pts = [toward(a, b, d * t / 30) for t in range(4, 25)]
        s.polylines(runs(pts), stroke=AMB, w=m.lw * 0.6, opacity=0.9, dash="0.9 0.6")
        for p, q in zip(pos(*pts[-1]), pos(*pts[-4])):
            dx, dy = p[0] - q[0], p[1] - q[1]
            n = math.hypot(dx, dy) or 1.0
            ux, uy = dx / n, dy / n
            for sg in (1, -1):
                s.polylines([[(p[0], p[1]), (p[0] - ux * 1.0 - sg * uy * 0.6, p[1] - uy * 1.0 + sg * ux * 0.6)]],
                            stroke=AMB, w=m.lw * 0.6, opacity=0.9)

    def rings(s, pos, runs, disc):
        if disc is False:                              # 南盤不收
            return
        circ = lambda r: [(float(ra), dec_r(r)) for ra in range(0, 361, 2)]
        # 月站環：28 等分（黃道等分線沿赤經圈投到盤上）
        r0, r1 = RING_ST
        for r in (r0, r1):
            s.polylines(runs(circ(r)), stroke=COLORS["amber"], w=m.lw * 0.7, opacity=0.9)
        rr = []
        for n in range(1, 29):
            ra = ecl_to_j2000(station_range(n)[0])[0]
            rr += runs([(ra, dec_r(r0)), (ra, dec_r(r1))])
        s.polylines(rr, stroke=COLORS["amber"], w=m.lw * 0.6, opacity=0.85)
        # 二十八宿環：距星赤經（不等寬）
        r0, r1 = RING_XIU
        for r in (r0, r1):
            s.polylines(runs(circ(r)), stroke=COLORS[PURPLE], w=m.lw * 0.7, opacity=0.9)
        rr = []
        for _, _, h in XIU:
            ra = S[h][0]
            rr += runs([(ra, dec_r(r0)), (ra, dec_r(r1))])
        s.polylines(rr, stroke=COLORS[PURPLE], w=m.lw * 0.6, opacity=0.85)

    return [("黃道", ecliptic), ("單星站圈", singles), ("空地al-Baldah", baldah), ("站界框", boxes),
            ("月亮一週5月25至28日", moon_week), ("月亮週末5月29與30日", moon_weekend),
            ("眉月6月6日", crescent), ("木星與火星5月28日", planets), ("跟隨箭頭", follow),
            ("兩環（北盤總覽）", rings)]


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
# 四、旁白字數（中文字＋外文音節；與逐字稿 vo_units 同一套）
# ══════════════════════════════════════════════════════════════════
VOW = "aeiouyāīūēōáéíóú"


def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏḀ-ỿʿʾ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(f"[{VOW}]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = S0
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
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

    def item(a, text, color, size, dx, dy, key, disc=False):
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    # 字級：Canva px ≈ size×1.7×1080/fov；主名 ~55 px、譯名 ~45 px（Canva 夾在 36–96）
    def lab(a, orig, zh, col, fov, dx=0.0, dy=0.0, key=None, zh_col="white", k1=0.030, k2=0.025):
        s1, s2, gap = round(fov * k1, 2), round(fov * k2, 2), round(fov * 0.048, 2)
        key = key or orig
        out = [item(a, orig, col, s1, dx, dy + gap / 2, key)]
        if zh:
            out.append(item(a, zh, zh_col, s2, dx, dy - gap / 2, key + "-zh"))
        return out

    def one(a, text, col, fov, dx=0.0, dy=0.0, key=None, k=0.026, disc=False):
        return [item(a, text, col, round(fov * k, 2), dx, dy, key or text, disc)]

    STA = {k: (nat, pr, zh) for k, nat, pr, zh in STATIONS}

    def sta_anchor(k):
        if k == "Thur":
            return M45
        if k == "Blda":
            ra, dec = centroid([], S) if False else (sum(p[0] for p in BALDAH) / len(BALDAH),
                                                     sum(p[1] for p in BALDAH) / len(BALDAH))
            return (ra, dec)
        h = ST_HIPS[k]
        return [h[0]] if len(h) == 1 else h

    moon = lambda k: (PL[k]["ra"], PL[k]["dec"])

    # ── 02 鏡：月站門牌（轉寫＋中譯），只標畫面會經過的 20–25 站 ──
    F02 = 40.0
    OFF02 = {"SDab": (0.0, -4.2), "SBul": (0.0, 4.0), "SSud": (0.0, -4.2), "SAkh": (1.0, 4.6),
             "Mqdm": (4.0, 0.0), "Mkhr": (-4.5, 0.0), "Blda": (0.0, -4.2), "Naym": (0.0, -5.6)}
    LB02 = []
    for k in ("Naym", "Blda", "SDab", "SBul", "SSud", "SAkh", "Mqdm", "Mkhr"):
        dx, dy = OFF02[k]
        nat, pr, zh = STA[k]
        LB02 += lab(sta_anchor(k), pr, zh, "amber", F02, dx=dx, dy=dy, key=f"門-{k}", k1=0.026, k2=0.024)

    # ── 06 鏡：大蠍子、鴕鳥群、空地（「冠冕」旁白沒唸，不標） ──
    F06 = 36.0
    LB06 = (lab(ST_HIPS["Zban"], "al-Zubānā", "螯", "red", F06, dx=-1.0, dy=-4.4)
            + lab([ANTARES], "al-Qalb", "心臟", "red", F06, dx=5.6, dy=-1.2)
            + lab(ST_HIPS["Shwl"], "al-Shawlah", "翹起的尾巴", "red", F06, dx=0.0, dy=-3.6)
            + lab(ST_HIPS["Naym"], "al-Naʿāʾim", "鴕鳥群", "green", F06, dx=0.0, dy=-8.6)
            + lab(sta_anchor("Blda"), "al-Baldah", "空地", "amber", F06, dx=0.0, dy=-4.8))

    # ── 07 鏡：四間吉星、水桶兩口、月亮 ──
    F07 = 40.0
    LB07 = (lab(ST_HIPS["SDab"], "Saʿd al-Dhābiḥ", "屠夫的", "amber", F07, dx=0.0, dy=-4.0, k1=0.025, k2=0.024)
            + lab(ST_HIPS["SBul"], "Saʿd Bulaʿ", "吞嚥者的", "amber", F07, dx=0.0, dy=3.6, k1=0.025, k2=0.024)
            + lab(ST_HIPS["SSud"], "Saʿd al-Suʿūd", "吉中之吉", "amber", F07, dx=0.0, dy=-4.0, k1=0.025, k2=0.024)
            + lab(ST_HIPS["SAkh"], "Saʿd al-Akhbiyah", "帳篷的", "amber", F07, dx=0.0, dy=3.8, k1=0.025, k2=0.024)
            + lab(ST_HIPS["Mqdm"], "前口", "", "blue", F07, dx=3.4, dy=0.0, k1=0.026)
            + lab(ST_HIPS["Mkhr"], "後口", "", "blue", F07, dx=-3.4, dy=0.0, k1=0.026)
            + one(ecl_to_j2000(station_range(24)[0], -9.6), "← 水桶的前口｜帳篷的吉星 →", "amber", F07,
                  key="站界2324", k=0.020))

    LB07M = (one(moon("月5/29"), "5/29 清晨", "white", F07, dy=-2.4, key="月529", k=0.024)
             + one(moon("月5/30"), "5/30 清晨", "white", F07, dy=-2.4, key="月530", k=0.024))

    # ── 08／08b ──
    F08 = 30.0
    LB08 = (lab([ALDEBARAN], "Aldebaran", "al-Dabarān・跟在後面的", "amber", F08, dx=0.0, dy=-3.0)
            + lab(M45, "al-Thurayyā", "昴宿", "amber", F08, dx=0.0, dy=3.4))
    F08b = 30.0
    LB08b = lab(ST_HIPS["Shwl"], "Shaula", "al-Shawlah・翹起的尾巴", "red", F08b, dx=-3.0, dy=3.8)

    # ── 09：天秤兩星 ──
    F09 = 18.0
    LB09 = (lab([ZUBEN_G], "Zubenelgenubi", "南邊的螯", "red", F09, dx=0.0, dy=-1.9)
            + lab([ZUBEN_S], "Zubeneschamali", "北邊的螯", "red", F09, dx=0.0, dy=1.9))

    # ── 10／10b：同一批星 ──
    F10 = 34.0
    LB10 = (lab(ST_HIPS["Mqdm"], "室宿", "水桶的前口", PURPLE, F10, dx=5.4, dy=0.0, zh_col="amber")
            + lab(ST_HIPS["Mkhr"], "壁宿", "水桶的後口", PURPLE, F10, dx=-5.4, dy=0.0, zh_col="amber"))
    F10b = 30.0
    LB10b = lab([ANTARES], "心宿二", "al-Qalb・心臟", PURPLE, F10b, dx=0.0, dy=-2.8, zh_col="amber")

    # ── 11：牛宿一＝屠夫 ──
    F11 = 10.0
    LB11 = (lab([DABIH], "牛宿一", "屠夫", PURPLE, F11, dx=1.6, dy=-0.9, zh_col="amber")
            + one([ALSHAT], "羊", "amber", F11, dx=-0.8, dy=0.5, key="羊", k=0.032)
            + one([ALGEDI2], "牛宿二", PURPLE, F11, dx=0.0, dy=0.8, key="牛宿二", k=0.024))

    # ── 12：今晚八點 ──
    F12 = 40.0
    j8, mars = (PL["木星"]["ra"], PL["木星"]["dec"]), (PL["火星"]["ra"], PL["火星"]["dec"])
    LB12 = (one([REGULUS], "軒轅十四", "white", F12, dy=-2.6, key="軒轅十四")
            + one(j8, "木星", "white", F12, dy=2.4, key="木星")
            + one(mars, "火星", "red", F12, dx=-1.5, dy=2.4, key="火星")
            + one(ecl_to_j2000(sum(station_range(7)) / 2, -10.5), "眼睛 al-Ṭarf", "amber", F12, key="眼睛", k=0.022)
            + one(ecl_to_j2000(sum(station_range(8)) / 2, -10.5), "額頭 al-Jabhah", "amber", F12, key="額頭", k=0.022)
            + lab([SPICA], "角宿一", "al-Simāk・高舉者", "amber", F12, dy=-3.0, zh_col="white")
            + lab(ST_HIPS["Zban"], "天秤兩螯", "al-Zubānā", "amber", F12, dx=-7.5, dy=1.5, zh_col="white")
            + lab([ANTARES], "心宿二", "al-Qalb", "red", F12, dy=-3.0, zh_col="white"))

    # ── 13：6/6 眉月 ──
    F13 = 26.0
    c66 = moon("月6/6")
    LB13 = (one(c66, "6/6 19:10 眉月", "white", F13, dx=0.0, dy=1.8, key="眉月")
            + one(ecl_to_j2000(sum(station_range(4)) / 2, 9.8), "低彎 al-Hanʿah", "amber", F13, key="低彎", k=0.026)
            + one([MU_GEM], "雙子 μ", "white", F13, dx=0.0, dy=-1.6, key="μGem", k=0.022)
            + one((c66[0], c66[1] - 13.5), "高 14°・西北偏西 292°", "white", F13, key="方位", k=0.022)
            + one((c66[0], c66[1] - 15.3), "19:30 約 10°｜天還有餘暉，先找月亮", "white", F13,
                  key="餘暉", k=0.019))

    # ── 14：北盤兩環（月站 28 等分／二十八宿不等寬） ──
    F14 = 120.0
    dec_r = lambda r: 90.0 - r / m.k
    LB14X, LB14A = [], []
    xr = [S[h][0] for _, _, h in XIU]
    for i, (nm, _, h) in enumerate(XIU):
        a, b = xr[i], xr[(i + 1) % 28]
        w = (b - a) % 360
        mid = (a + w / 2) % 360
        r = (RING_XIU[0] + RING_XIU[1]) / 2 + (6.5 if w < 6 else 0.0)
        LB14X += one((mid, dec_r(r)), nm, PURPLE, F14, key=f"環宿{nm}", k=0.030, disc=True)
    for n in range(1, 29):
        lam = sum(station_range(n)) / 2
        ra = ecl_to_j2000(lam)[0]
        LB14A += one((ra, dec_r((RING_ST[0] + RING_ST[1]) / 2)), str(n), "amber", F14,
                     key=f"環站{n}", k=0.026, disc=True)
    LB14T = (one((LST0, dec_r(13.0)), "二十八宿：依距星，寬窄不一", PURPLE, F14, key="環宿說明",
                 k=0.022, disc=True)
             + one((LST0, dec_r(5.0)), "月站：28 等分", "amber", F14, key="環站說明",
                   k=0.022, disc=True))

    # ── 15：下集 ──
    F15 = 34.0
    LB15 = (lab([MIRACH], "al-Ḥūt", "大魚", "green", F15, dx=-5.0, dy=3.0)
            + lab([ALPHERATZ], "仙女座", "", "blue", F15, dx=0.0, dy=2.8, k1=0.026))

    label_sets = [(LB02, "月站門牌"), (LB06, "大蠍子與鴕鳥"), (LB07, "吉星與水桶"), (LB07M, "月亮週末"), (LB08, "畢宿五"),
                  (LB08b, "Shaula"), (LB09, "天秤兩螯"), (LB10, "室壁＝水桶"), (LB10b, "心＝心臟"),
                  (LB11, "牛宿一＝屠夫"), (LB12, "今晚八點"), (LB13, "眉月"), (LB14X, "環-二十八宿"),
                  (LB14A, "環-月站序"), (LB14T, "環-說明"), (LB15, "下集")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 構圖 ════════════════════
    def P(h):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        return (x_of(ra), dec)

    def fr(x, y, fov):
        return (round(x, 2), round(y, 2), round(fov, 1), 0.0)

    yp = m.y_pole
    F01a = fr(-95.0, -6.0, 60.0)                    # 摩羯—寶瓶全景（5/25–5/28 月亮）
    F01b = fr(-95.0, -6.0, 40.0)
    F02b = fr(-122.0, 2.0, F02)                     # 往東捲到 寶瓶—飛馬
    F03 = F02b
    F06a = fr(-8.0, -14.0, F06)                     # 天秤（兩隻螯）
    F06b = fr(-32.0, -27.0, F06)                    # 天蠍（心臟、尾巴）
    F06c = fr(-65.0, -24.0, F06)                    # 鴕鳥群＋空地
    F07a = fr(-100.0, -9.0, F07)                    # 四間吉星
    F07b = fr(-127.0, 5.0, F07)                     # 帳篷的吉星 → 水桶的前口（月亮 5/29→5/30）
    F08 = fr(*P((63.5, 19.0)), F08)                 # 畢宿＋昴宿
    F08b = fr(*P((264.0, -33.0)), F08b)             # 天蠍尾
    F09a = fr(-6.0, -12.7, 30.0)
    F09b = fr(-6.0, -12.7, F09)
    F10 = fr(-134.5, 22.0, F10)                     # 飛馬大四方形
    F10b = fr(*P((246.0, -24.0)), F10b)             # 心宿二
    F11a = fr(*P((305.0, -13.6)), 24.0)             # 摩羯 β、ν、α²
    F11b = fr(*P((305.0, -13.6)), F11)
    F12a = fr(74.0, 12.0, F12)                      # 獅子頭：軒轅十四、木星、火星
    F12b = fr(20.0, -6.0, F12)                      # 角宿一
    F12c = fr(-14.0, -20.0, F12)                    # 天秤兩螯、心宿二
    F13a = fr(*P((97.0, 21.0)), F13)                # 雙子腳邊（6/6 眉月）
    F13b = fr(*P((97.0, 21.0)), 40.0)               # 拉遠到 fov 40＝長圖轉北盤換組格
    F14a = (0.0, yp, 40.0, 0.0)
    F14b = (0.0, yp, F14, -10.0)
    F14c = (0.0, yp, F14, -30.0)
    F15a = fr(-150.0, 27.0, 40.0)
    F15b = fr(-150.0, 27.0, F15)
    print("\n── 構圖 ──")
    for k, v in dict(F01a=F01a, F01b=F01b, F02b=F02b, F06a=F06a, F06b=F06b, F06c=F06c, F07a=F07a, F07b=F07b,
                     F08=F08, F08b=F08b, F09b=F09b, F10=F10, F10b=F10b, F11b=F11b, F12a=F12a, F12b=F12b,
                     F12c=F12c, F13a=F13a, F13b=F13b, F15b=F15b).items():
        print(f"  {k} {v}")

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ST)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ST, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    ST = ["站", "圈", "黃"]
    shots = [
        dict(code="01", kind="Z", sec=14, north=True, frames=[F01a, F01b], layers=ST + ["月週"], labels=[],
             vo="上週，阿拉伯航海家 Ibn Mājid 帶我們看星星過海。今晚回到月亮的路上，替「月站」這個系列收尾：同一片星空，阿拉伯人看見——月亮每晚住的旅店。",
             card="同一片星空，阿拉伯人看見——／月亮每晚住的旅店。",
             note="大畫布 fov 60→40（Z）：摩羯—寶瓶一帶的黃道（淡藍灰虛線）＋28 站連線（琥珀）＋單星站圈；"
                  "月亮一週層＝5/25–5/28 清晨 04:30 四個位置（由右往左一晚一格，越近越亮；圖示放大約 3 倍示意）；開場字卡"),
        dict(code="02", kind="S", sec=16, north=True, frames=[F01b, F02b], layers=ST, labels=ls("月站門牌"),
             labels_start=[],
             vo="中秋那集，我們數過四個文明替月亮蓋的二十八間房；阿拉伯半島那集，沙漠裡的人看黎明升起的星，把它們當成太陽的日曆。今晚換個方式：直接跟著月亮走。",
             card="今晚：直接跟著月亮走",
             note="長圖往左（東）捲：摩羯 → 寶瓶—飛馬；月站門牌（轉寫＋中譯）；右上角依序疊 A-06（中秋・四文明 28 間房）、"
                  "A-13（沙漠星曆）兩集封面縮圖（Canva 既有封面，美宣放）"),
        dict(code="03", kind="Z", sec=15, north=True, frames=[F03], layers=ST, labels=ls("月站門牌"),
             overlay="C-A32-01_每晚13度", overlay_layers=["月亮層", "尺度層"],
             vo="月亮每晚往東挪大約十三度，伸直手臂看，比一個拳頭再寬一點；二十七八個晚上，就繞天一圈。阿拉伯文把它每晚落腳的地方叫 manzil——下榻處。",
             card="每晚往東 13°",
             note="畫面停在寶瓶—飛馬；定格疊 C-A32-01 兩層：月亮層（5/26–6/1 清晨 04:30 七格）→ 尺度層（伸臂拳頭、13°、manzil／manāzil）"),
        dict(code="04", kind="Z", sec=19, north=True, frames=[F03], layers=ST, labels=[],
             overlay="C-A32-02_列宿", overlay_layers=["原文層", "直譯層", "馬堅層"],
             vo="《古蘭經》說：祂讓太陽發光、月亮明亮，又為月亮定下一站一站，好讓你們知道年數和曆算。「一站一站」原文是 manāzil；馬堅的中文譯本，把它譯成「列宿」——跟二十八宿，用的是同一個「宿」。",
             card="古蘭經 10:5／manāzil＝列宿",
             note="畫面不動；疊 C-A32-02 三層：10:5 原文（مَنَازِلَ 高亮）→ 本社直譯 → 馬堅譯本「並為月亮而定列宿」"),
        dict(code="05", kind="Z", sec=17, north=True, frames=[F03], layers=ST, labels=[],
             overlay="C-A32-03_月站與眉月", overlay_layers=["月站層", "眉月層"],
             vo="不過，伊斯蘭曆的月份，傳統上不看月亮住哪一站，而是看月初日落後，西邊低空第一次見到的細細眉月，叫 hilāl。月站告訴你月亮在哪裡；眉月告訴你，今天是幾號。",
             card="月站≠伊斯蘭曆",
             note="畫面不動；疊 C-A32-03 兩層：月站層（月亮在站與站之間）→ 眉月層（日落後西方低空 hilāl＋「今天幾號」）"),
        dict(code="06", kind="S", sec=20, north=True, cut=True, frames=[F06a, F06b, F06c], layers=["蠍", "鴕", "空", "黃"],
             labels=ls("大蠍子與鴕鳥"),
             vo="二十八間旅店，名字都很有畫面：天蠍那一帶是一隻大蠍子，有「螯」、有「心臟」，還有「翹起的尾巴」；今天的人馬座那一帶，是一群鴕鳥。再往東一間叫 al-Baldah，「空地」——那段天空沒有亮星，月亮那一晚，等於睡在野外。",
             card="大蠍子・鴕鳥群／al-Baldah＝空地",
             note="【硬切】（05→06 隔 120°，換段）長圖往左捲 天秤→天蠍→人馬：大蠍子（紅，含天秤兩螯）、鴕鳥群（綠）、"
                  "al-Baldah 虛線圈（Stellarium 的空地範圍，不畫星）；第二張字卡在唸到 al-Baldah 時換"),
        dict(code="07", kind="S", sec=19, north=True, frames=[F07a, F07b], layers=ST + ["桶", "界", "月末"],
             labels=ls("吉星與水桶", "月亮週末"), labels_start=ls("吉星與水桶"),
             vo="再過去是四間「吉星」：屠夫的、吞嚥者的、吉中之吉，還有帳篷的。這個週末清晨，下弦月剛好從「帳篷的吉星」搬進下一間「水桶的前口」——水桶是飛馬座的大四方形，月亮從它南邊經過。",
             card="5/29–30 月亮搬家",
             note="長圖續往左 摩羯→寶瓶→飛馬：四間吉星（琥珀）、水桶前口／後口（藍）；月亮 5/29、5/30 清晨 04:30 兩個位置"
                  "（同一層，5/29 較暗）；第 23／24 站等分站界框（虛線），月亮在大四方形正南方跨線"),
        dict(code="08", kind="Z", sec=12, north=True, cut=True, frames=[F08], layers=ST + ["隨"], labels=ls("畢宿五"),
             vo="這些旅店的招牌，後來傳到歐洲，掛上了今天的星圖：畢宿五 Aldebaran，就是 al-Dabarān，「跟在後面的」，因為它跟著昴宿；",
             card="畢宿五＝跟在後面的",
             note="【硬切】長圖 畢宿＋昴宿 fov 30：Aldebaran／al-Dabarān 標籤＋「跟著昴宿」虛線箭頭"),
        dict(code="08b", kind="Z", sec=4, north=True, cut=True, frames=[F08b], layers=["蠍"], labels=ls("Shaula"),
             vo="天蠍尾巴的 Shaula，是「翹起的尾巴」。",
             card="Shaula＝翹起的尾巴",
             note="【硬切】天蠍尾巴 fov 30（逐字稿 08 鏡在「；」拆出 08b）：Shaula／al-Shawlah 標籤，字卡同時換第二張"),
        dict(code="09", kind="Z", sec=18, north=True, frames=[F09a, F09b], layers=["蠍"], labels=ls("天秤兩螯"),
             labels_start=[],
             overlay="C-A32-04_星圖上的月站",
             vo="剛才那兩隻螯，就是今天天秤座這兩顆：Zubenelgenubi、Zubeneschamali，像繞口令，意思是「南邊的螯」「北邊的螯」。二十八間裡，超過一半的名字，今天還寫在國際天文聯合會的正式星名表上。",
             card="天秤兩星＝蠍子的螯／28 間裡，18 間還在星圖上",
             note=f"長圖推近天秤兩星 fov 30→{F09:g}：Zubenelgenubi／Zubeneschamali＋南邊的螯／北邊的螯；"
                  "唸到「二十八間裡」換第二張字卡，迄格後疊 9:16 圖卡 C-A32-04「星圖上的月站」（18 站、22 個 IAU 星名，可存圖）"),
        dict(code="10", kind="Z", sec=14, north=True, cut=True, frames=[F10], layers=ST + ["宿"], labels=ls("室壁＝水桶"),
             vo="跟中國的二十八宿對一對，常常連挑的星都一樣：飛馬座的大四方形，中國切成室宿、壁宿，阿拉伯切成「水桶的前口」「後口」，一樣兩顆一組；",
             card="室宿・壁宿＝水桶兩個口",
             note="【硬切】長圖 飛馬大四方形 fov 34，雙層連線：中國二十八宿（紫）＋阿拉伯月站（琥珀）；室＝前口、壁＝後口"),
        dict(code="10b", kind="Z", sec=5, north=True, cut=True, frames=[F10b], layers=ST + ["宿"], labels=ls("心＝心臟"),
             overlay="C-A32-05_同一批星", overlay_layers=["三組層", "更多層"],
             vo="天蠍的紅心，中國叫心宿二，阿拉伯叫 al-Qalb，也是「心臟」。",
             card="心宿二＝al-Qalb 心臟",
             note="【硬切】天蠍 心宿二 fov 30（逐字稿 10 鏡拆出 10b），字卡同時換第二張；結束疊 C-A32-05 兩層："
                  "三組層（室＝前口、壁＝後口、心＝心臟）→ 更多層（觜＝圓斑、胃＝小肚子、亢≈遮蓋、鬼≈鼻尖、房≈冠冕）"),
        dict(code="11", kind="Z", sec=12, north=True, frames=[F11a, F11b], layers=ST + ["宿"], labels=ls("牛宿一＝屠夫"),
             labels_start=[],
             vo="可是摩羯座這一顆，中國是牛宿一，一頭牛；阿拉伯人卻看見前面那位「屠夫」，旁邊那顆小星，是他要宰的羊。",
             card="牛宿一＝屠夫？",
             note=f"長圖推近摩羯 α²、β、ν Cap fov 24→{F11:g}：牛宿（紫）vs 屠夫的吉星（琥珀）；ν Cap 標「羊」"
                  "（10b 心宿二 → 摩羯滑 58°）"),
        dict(code="12", kind="S", sec=24, north=True, cut=True, frames=[F12a, F12b, F12c], layers=ST + ["獅", "行", "界"],
             labels=ls("今晚八點"),
             overlay="C-A32-06_今晚八點抬頭看",
             vo="今晚八點抬頭：西方高處，獅子座的軒轅十四兩旁，一邊木星、一邊火星，正好住在阿拉伯大獅子的「眼睛」和「額頭」；南南東的角宿一，也是一間旅店，叫「高舉者」；東南方半空是天秤的兩隻螯，低空還有天蠍的紅心，剛升起不久。",
             card="5/28 今晚八點抬頭看",
             note="【硬切】長圖＋行星層（5/28 20:00 台北）：獅子頭 軒轅十四、木星、火星，阿拉伯大獅子（藍）、"
                  "第 7「眼睛」第 8「額頭」站界框 → 往左捲到角宿一（高舉者）→ 天秤兩螯、心宿二；"
                  "結束疊 9:16 圖卡 C-A32-06「今晚八點抬頭看」（可存圖）"),
        dict(code="13", kind="Z", sec=21, north=True, cut=True, frames=[F13a, F13b], layers=ST + ["眉", "界", "環"],
             labels=ls("眉月"), labels_end=[],
             vo="想親眼看那彎決定月份的眉月？下週六凌晨是新月；六月六號星期天，是沙烏地官方曆的伊斯蘭新年。那天傍晚七點到七點半，往西北偏西的低空看，第一彎細細的眉月，住進「低彎」這一站——雙子座的腳邊。",
             card="6/6 傍晚・第一彎眉月",
             note=f"【硬切】（12→13 隔 136°）長圖 雙子座腳邊 fov {F13:g}→40：眉月 6/6 19:10（亮面 4%，離 μ Gem "
                  f"{sep(c66, S[MU_GEM][:2]):.1f}°）、第 4 站「低彎」站界框；方位小字（19:10 高 14°、292°；19:30 約 10°；"
                  "天還有餘暉，先找月亮）；迄格拉遠到 fov 40＝下一鏡長圖轉北盤的換組格大小（環層先開著：在畫面外，換組時才不會跳出來）"),
        dict(code="14", kind="R", sec=17, north=True, frames=[F14a, F14b, F14c], layers=["站", "宿", "環"],
             labels=ls("環-二十八宿", "環-月站序", "環-說明"), labels_start=[],
             overlay="C-A32-07_月站宇宙",
             vo="月站這個系列就到這裡：中國的二十八宿、印度的月站 Nakshatra、日本替星宿取的農具名字、沙漠的星曆，還有今晚的月亮旅店——同一條月亮的路，好幾種住法。",
             card="同一條路，好幾種住法",
             note="【換組】長圖→北盤（fov 40 盤心）→ 拉遠到 fov 120、盤逆時針 0°→−10°→−30°（2 小時）；兩環示意層："
                  "外環＝二十八宿依距星赤經畫不等寬（觜、鬼很窄，井很寬）、內環＝月站 28 等分（黃道等分線沿赤經圈投到盤上）；"
                  "結束疊 9:16 圖卡 C-A32-07「月站宇宙」（A-05 日本、A-06 四文明、A-13 沙漠星曆、A-32 月亮旅店，可存圖）"),
        dict(code="15", kind="Z", sec=12, north=True, cut=True, frames=[F15a, F15b], layers=["魚", "仙"],
             labels=ls("下集"), labels_start=[],
             vo="下週五，我們翻開一千多年前的星圖手稿：波斯天文學家蘇菲，把希臘星座和阿拉伯星名寫進了同一本書。",
             card="下集見｜蘇菲之書：一千多年前的星圖手稿",
             note="【換組】北盤→長圖（下移回走廊）後【硬切】仙女座 fov 40→34（隔 150°）：大魚 al-Ḥūt（綠）＋仙女座（藍）；"
                  "端卡「下集見｜蘇菲之書：一千多年前的星圖手稿」＋追蹤 CTA（停 2 秒以上）"),
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

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                which = "北盤圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-cx / fov * 1080), round((cy - m.y_pole) / fov * 1080))
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
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    # ── 天象核對（與逐字稿「星空對時」比對） ──
    print(f"\n── 天象核對 ──\n  第 1 站中心（昴宿六 J2000 黃經）＝{LAM0:.3f}°（當日 60.37°）")
    for k in ("月5/25", "月5/26", "月5/27", "月5/28", "月5/29", "月5/30", "月5/31", "月6/1", "月6/6"):
        v = PL[k]
        n = station_of(v["lon_j2000"])
        print(f"  {k}: RA {v['ra']:.2f} Dec {v['dec']:+.2f}（x {x_of(v['ra']):+.1f}）高 {v['alt']}° 方位 {v['az']}° "
              f"{v['phase']}%  第 {n} 站 {STATIONS[n - 1][3]}")
    print(f"  5/30 月亮—室宿一 {sep(moon('月5/30'), S[MARKAB][:2]):.1f}°；6/6 眉月—μ Gem {sep(c66, S[MU_GEM][:2]):.1f}°")
    for nm in ("木星", "火星"):
        v = PL[nm]
        lam = ecl_of(v["ra"], v["dec"])[0]
        print(f"  {nm}: 高 {v['alt']}° 方位 {v['az']}° 離軒轅十四 {sep((v['ra'], v['dec']), S[REGULUS][:2]):.1f}°"
              f"  第 {station_of(lam)} 站 {STATIONS[station_of(lam) - 1][3]}")
    xw = [((S[XIU[(i + 1) % 28][2]][0] - S[h][0]) % 360) for i, (_, _, h) in enumerate(XIU)]
    print("  二十八宿寬（距星赤經差 J2000）：" + "、".join(f"{n}{w:.1f}" for (n, _, _), w in zip(XIU, xw)))
    print(f"  k {m.k:.4f}、R_fill {m.R_fill:.3f}、盤寬比 {2 * m.R_fill / 360:.6f}")

    def T(hips, orig, pr, en, zh, col, note):
        return dict(hips=hips if isinstance(hips, list) else [], 原文=orig, 拼音=pr, 英文翻譯=en, 中文=zh,
                    顏色=col, 來源備註=note)

    eng = {s["symbol"]: s["english"] for s in AI_IDX["lunar_system"]["names"]}
    terms = {}
    for i, (k, nat, pr, zh) in enumerate(STATIONS, 1):
        a, b = station_range(i)
        terms[pr] = T(ST_HIPS.get(k, []), nat, pr, eng.get(str(i), ""), zh, "amber",
                      f"第 {i} 站（本土序）；等分站界 J2000 黃經 {a % 360:.1f}°–{b % 360:.1f}°；Stellarium arabic_indigenous {k}")
    for nm, key, h in XIU:
        terms[f"{nm}宿"] = T(sorted({x for s in CH[key] for x in s}), f"{nm}宿", "", "", f"{nm}宿", PURPLE,
                            f"Stellarium chinese {key}；距星 HIP {h}")
    for k, orig, en, zh, col, note in [
        ("Aldebaran", "Aldebaran", "Aldebaran", "畢宿五（跟在後面的）", "amber", "IAU；al-Dabarān"),
        ("Shaula", "Shaula", "Shaula", "尾宿八（翹起的尾巴）", "red", "IAU；al-Shawlah"),
        ("Zubenelgenubi", "Zubenelgenubi", "Zubenelgenubi", "氐宿一（南邊的螯）", "red", "IAU"),
        ("Zubeneschamali", "Zubeneschamali", "Zubeneschamali", "氐宿四（北邊的螯）", "red", "IAU"),
        ("al-Ḥūt", "الحوت", "The Fish", "大魚", "green", "Stellarium arabic_indigenous Hoot（下集預告）")]:
        terms[k] = T([], orig, k, en, zh, col, note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0, "lam0_j2000": LAM0, "bodies": {k: {kk: vv for kk, vv in v.items() if kk != "sun"}
                                                             for k, v in PL.items()}},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL + LG_SCORP + LG_OSTR,
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
