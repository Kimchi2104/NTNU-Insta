# -*- coding: utf-8 -*-
"""A-23 羅馬尼亞：牧羊人的星空農場｜大畫布 v4.6

論點：羅馬尼亞農民的天空是一座牧羊人的農場——母山羊帶三隻小羊（五車二＋ε、ζ、η Aur）、看羊的大狗
（大犬）、小狗（小犬）、母雞帶小雞（昴宿）、公豬（畢宿；畢宿五＝豬的亮星／鬧鐘）、獵戶一塊天疊四個
星座（小犁、大鑽子、鐮刀、三聖人）、大車與長明燈、Romulus 與 Remus、牧羊人和他的羊（天琴）、
挑水的公主（天鷹）、井和水槽（飛馬＋仙女）、馬（獅子）、放牛的人（牧夫）。

來源：Stellarium romanian（Baia Mare 天文館 CRT 計畫 2012–2013，主要根據 Otescu 1907）；
Ion Otescu 1907 的 SARM 英譯（頁碼＝英譯本）；跨文化：拉丁 Capella／Haedi、白俄 Kaza、Kastsy、
「波蘭和立陶宛」（A-22）、中國 天狼、牛郎織女（H-七夕）。天象 PyEphem 4.2.1 自算。
逐字稿：04_腳本庫/A-23-羅馬尼亞牧羊人的星空農場-逐字稿-v1.md。

連線：照 Stellarium romanian，三處依 Otescu 改：
  ① Sfredelul mare 大鑽子：Stellarium 連腰帶＋參宿七；Otescu p.14／CRT 說腰帶是握柄、參宿四是鑽頭
     → 自繪 腰帶 26727–26311–25930＋26311→27989（參宿四）；鑽頭方向另加淡虛線指向北河三「寶藏」（自訂層）。
  ② Puțul cu jgheab 井和水槽：Stellarium 兩版都少 113963（室宿一）—1067（壁宿一）那一邊；
     Otescu p.8 說四顆星是井口四角 → 補上，四邊形閉合。
  ③ Haedi（拉丁「兩隻小羊」ζ、η Aur）：不是羅馬尼亞星座，05 鏡跨文化用，藍色小段。
  白俄 Kastsy（01 鏡淡出）＝腰帶三星，琥珀；與 Trisfetitele 同星、不同層。
  木星、火星（台北 2/26 20:00）、金星（2/27 05:30）：自訂層，J2000 astrometric（與星表同框）、台北站心。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 145 → 長圖 x＝wrap(145−RA)。這集的鏡頭幾乎繞了整個天球一圈（冬季星空、獅子、牧夫、天琴、天鷹、
             飛馬—仙女、天蠍—人馬），畫布左右邊（x＝±180）只能放在沒有鏡頭的天區：
             空檔只有 巨蟹（RA 117–146）、白羊—三角（31–56）、摩羯—寶瓶（299–340）三段。
             lst 145 把邊放在 RA 325（寶瓶）：金星（RA 298.7）x −153.7、牛郎 −152.7、織女 −133.6；
             飛馬—仙女 x +114（天大將軍一）…+159（室宿二），fov 54 的畫面左右邊 ≤ 164；
             冬季：參宿四 +56、天狼星 +44、五車二 +66、昴宿 +88、北河三 +29；
             獅子：軒轅十四 −7、五帝座一 −32（木星 −2.6、火星 −6.5）；牧夫：大角 −69。
             台北 2/26 20:00 的子午線（LST 97.7）在 x ＝ +47.3；走廊 x＝0 在獅子座西緣（RA 145），
             09 鏡往北走廊上去正好經過小獅—大熊，北斗就在獅子正上方。
             試過 lst 98（台北 20:00 子午線置中）：畫布邊落在 RA 278＝織女星上（✗）；
             lst 220（邊在 RA 40）：昴宿 x +163 貼邊、09 鏡要先橫移 136° 才到走廊（不用）。
  D_s = 56、D_r = 60 → 決定因素是 04 鏡的五車二（+46.0）與 14 鏡的天大將軍一（+42.3）：
             S 鏡頭 |cy|+fov·8/9 ≤ D_s，而且上緣要留 Reels 安全區（13%）。D_s 56 時 fov 25 的畫面上緣 55.5，
             五車二離上緣 9.5 ≥ 安全區 5.8；fov 54 的 14 鏡上緣 55.5，天大將軍一離上緣 13 ≥ 12.5。
             北斗（+49…+62）、大熊身體、小熊都只在 09 鏡出現，那一鏡整個在北盤圖層組（完整圓）上。
  D_fill = 0 → k＝1.9099、R_fill＝171.89（盤寬 ÷ 畫布寬＝0.9549；Canva 別設成同寬）。
             09 鏡要放進北極星、大車（台北 20:00 在東北方低空）和台北北方地平線（盤心下方 kφ＝47.8），
             畫面角落離盤心 ≤ 120，R_fill 172 綽綽有餘；|x_t|＋R_fill ≤ 180 ✓。
  x_tN = x_tS = 0
  北盤旋轉角：rot＝(lst − LST台北 − 180) 收在 (−180,180]；台北 2/26 20:00 LST 97.68 → rot −132.7°
             （單段 < 180°，v4.6 第四節 ✓）。

鏡頭路線（長圖為主＋北盤一鏡）
  01 台北 20:00 子午線冬季全景 fov 64→50（Kastsy 淡出）→ 02、03 定格疊 C-A23-01（星圖＋回信／一年）
  → 04 往上滑到御夫 → 05 定格跨文化 → 06 往下到大犬 → 07 往右（西）到昴宿—畢宿
  → 08 回獵戶 fov 30（四層），迄格拉到 fov 46 帶進北河三「寶藏」
  → 09【換北盤】（gen_canva_pages 自動插回中心／上移／長圖轉北盤）轉到台北 20:00 面北：大車、小車、長明燈
  → 10【換長圖】（自動插歸位／北盤轉長圖／下移）滑到雙子 → 11 往左（東）一路滑到天琴（＝時間往後，過半夜）
  → 12 天琴→天鷹→金星（2/27 05:30 東方）→ 13 定格跨文化＋圖卡 C-A23-02
  → 14【硬切】飛馬—仙女（從 x −150 到 +136，滑過去要橫越整張畫布）＋迄格疊 C-A23-06（19:10 西方地平線）
  → 15【硬切】獅子（木星、火星）→ 往左滑到牧夫 → 16 往左滑回天琴（Miorița，C-A23-03）→ 17、18 定格
  → 19【硬切】天狼星→五車二→獅子（這週末）＋圖卡 C-A23-05 → 20 往左滑到天蠍—人馬（端卡）

逐字稿要改的地方（素材時發現；已改進 v1 分鏡表）
  12 鏡「織女到金星相距 61°，一個 fov 45 裝不下，用平移」：長圖上織女（x −133.6, +38.8）到金星
     （−153.7, −19.9）寬 20、高 59，fov 45 的直式畫面（高 80）裝得下 → 迄格三個一起同框；
     平移照留（織女 fov 30 → 拉遠往右下帶出公主、金星）。
  14 鏡「結尾切 19:10 西方地平線框」：長圖沒有地平線（gen_canva_pages 只在盤頁畫地平線）
     → 改成迄格疊方形概念圖 C-A23-06「19:10 往西看：井沉了一半」（PyEphem 地平座標）。
  11、14、15、16、19 鏡：v1 標 Z／S 與實際動作不一致，依實際動作改成 S（有平移）。

check_shots 的 ⚠（判斷後接受；跑完逐條看過）
  09 R 鏡頭「迄格畫面含長圖側扇區」：迄格是轉到 −132.7° 的面北構圖，不直接切回大畫布；
  回程由 gen_canva_pages 插「北盤轉長圖1-歸位」（轉回 0°、盤心 fov 46，盤緣圈內逐點重合）再換組。
  歸位是 −132.7° → 0°＝順時針 133°（時間倒流），只發生在拉近盤心那一段（fov ~110→46）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-23"
OUT = os.path.join(BASE, "05_素材/A-23_羅馬尼亞/_v4大畫布")
LST0 = 145.0
TPE = (25.0330, 121.5654)
PHI_T = 25.03                     # 09 鏡台北面北的地平線緯度


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 10
    o.pressure, o.temp = 1013, 15
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(lat, lon, tz, when):
    return math.degrees(_obs(lat, lon, tz, when).sidereal_time())


def rot_at(lat, lon, tz, when):
    """北盤面向北方：rot＝lst − LST − 180，收在 (−180, 180]；負＝逆時針＝時間前進"""
    L = lst_at(lat, lon, tz, when)
    return round((LST0 - L - 180.0 + 180.0) % 360.0 - 180.0, 2)


ROT20 = rot_at(*TPE, 8, "2027/2/26 20:00")


def bodies():
    """J2000 astrometric（與星表同框）、台北站心"""
    import ephem
    out = {}
    for tag, when, objs in (("2/26", "2027/2/26 20:00", (("木星", ephem.Jupiter()), ("火星", ephem.Mars()))),
                            ("2/27", "2027/2/27 05:30", (("金星", ephem.Venus()),))):
        o = _obs(*TPE, 8, when)
        for nm, b in objs:
            b.compute(o)
            out[f"{nm}{tag}"] = dict(ra=math.degrees(b.a_ra), dec=math.degrees(b.a_dec),
                                     alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1))
    return out


PL = bodies()


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, CAPELLA, SIRIUS, PROCYON, ALDEBARAN = 11767, 24608, 32349, 37279, 21421
BETEL, RIGEL, CASTOR, POLLUX = 27989, 24436, 36850, 37826
VEGA, ALTAIR, REGULUS, ARCTURUS = 91262, 97649, 49669, 69673
KIDS = [23416, 23453, 23767]                # ε、ζ、η Aur
HAEDI = [23453, 23767]
BELT = [26727, 26311, 25930]
SHEEP = [91971, 92791, 93194, 92420]
DIPPER = [54061, 53910, 58001, 59774, 62956, 65378, 67301]


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"]] = [s for s in segs if len(set(s)) >= 2]
    return out


RO = load_sc("romanian")
R = lambda k: RO[f"CON romanian {k}"]
SEG_CART, SEG_SMALL = R("UMa"), R("UMi")
SEG_CAPRA, SEG_DOG, SEG_PUP = R("C3i"), R("Cma"), R("Ctl")
SEG_HEN, SEG_BOAR = R("Ccp"), R("Vri")
SEG_RAR, SEG_SEC, SEG_TRI = R("Rar"), R("Sec"), R("Trf")
SEG_SFR = [[26727, 26311, 25930], [26311, BETEL]]            # 自繪（Otescu p.14）：腰帶＝握柄、參宿四＝鑽頭
SEG_FRA, SEG_SHEP, SEG_FATA = R("Gem"), R("Cio"), R("Fap")
SEG_WELL = R("Jgb") + [[113963, 1067]]                       # 補上室宿一—壁宿一（Otescu p.8：井口四角）
SEG_HORSE, SEG_VAC = R("Cal"), R("Vca")
SEG_HAEDI = [HAEDI]
SEG_KAST = [BELT]                                            # 白俄 Kastsy（A-22）
assert R("Sfm") == [[26727, 26311, 25930], [24436, 26311]]   # Stellarium 原連線（不用）
assert sorted({h for s in SEG_WELL for h in s}) == sorted([9640, 5447, 3092, 677, 113881, 113963, 1067])
assert SEG_TRI == [BELT]

LG_KAST = [(SEG_KAST, "amber", 1.0)]
LG_CAPRA = [(SEG_CAPRA, "amber", 1.0)]
LG_HAEDI = [(SEG_HAEDI, "blue", 1.1)]
LG_DOG = [(SEG_DOG, "amber", 1.0), (SEG_PUP, "green", 1.0)]
LG_FARM = [(SEG_HEN, "green", 0.9), (SEG_BOAR, "red", 1.0)]
LG_RAR = [(SEG_RAR, "amber", 1.0)]
LG_SFR = [(SEG_SFR, "blue", 1.1)]
LG_SEC = [(SEG_SEC, "green", 0.9)]
LG_TRI = [(SEG_TRI, "purple", 1.3)]
LG_CART = [(SEG_CART, "amber", 1.0), (SEG_SMALL, "green", 1.0)]
LG_FRA = [(SEG_FRA, "blue", 1.0)]
LG_SHEP = [(SEG_SHEP, "amber", 1.0)]
LG_FATA = [(SEG_FATA, "green", 1.1)]
LG_WELL = [(SEG_WELL, "blue", 1.0)]
LG_HORSE = [(SEG_HORSE, "amber", 1.0)]
LG_VAC = [(SEG_VAC, "green", 1.0)]
LG_ALL = (LG_CAPRA + LG_DOG + LG_FARM + LG_RAR + LG_SFR + LG_SEC + LG_TRI + LG_CART + LG_FRA
          + LG_SHEP + LG_FATA + LG_WELL + LG_HORSE + LG_VAC)
LINE_SETS = [(LG_KAST, "連線-Kastsy（白俄）"), (LG_CAPRA, "連線-Capra母山羊"), (LG_HAEDI, "連線-Haedi（拉丁）"),
             (LG_DOG, "連線-大狗與小狗"), (LG_FARM, "連線-母雞與公豬"),
             (LG_RAR, "連線-Rarița小犁"), (LG_SFR, "連線-Sfredelul大鑽子"), (LG_SEC, "連線-Secera鐮刀"),
             (LG_TRI, "連線-Trisfetitele三聖人"), (LG_CART, "連線-大車與小車"), (LG_FRA, "連線-Frații兄弟"),
             (LG_SHEP, "連線-牧羊人和羊"), (LG_FATA, "連線-挑扁擔的公主"), (LG_WELL, "連線-井和水槽"),
             (LG_HORSE, "連線-Calul馬"), (LG_VAC, "連線-Văcarul放牛人")]
LINES_KEY = {"L4": "星座連線", "白": "連線-Kastsy（白俄）", "羊": "連線-Capra母山羊", "拉": "連線-Haedi（拉丁）",
             "狗": "連線-大狗與小狗", "豬": "連線-母雞與公豬", "犁": "連線-Rarița小犁", "鑽": "連線-Sfredelul大鑽子",
             "鐮": "連線-Secera鐮刀", "聖": "連線-Trisfetitele三聖人", "車": "連線-大車與小車",
             "兄": "連線-Frații兄弟", "牧": "連線-牧羊人和羊", "公": "連線-挑扁擔的公主", "井": "連線-井和水槽",
             "馬": "連線-Calul馬", "牛": "連線-Văcarul放牛人", "寶": "寶藏（虛線）",
             "行": "木星與火星-2月26日", "金": "金星-2月27日清晨", "暈": "單星光暈"}
LINE_GROUPS = {"L4": LG_ALL, "白": LG_KAST, "羊": LG_CAPRA, "拉": LG_HAEDI, "狗": LG_DOG, "豬": LG_FARM,
               "犁": LG_RAR, "鑽": LG_SFR, "鐮": LG_SEC, "聖": LG_TRI, "車": LG_CART, "兄": LG_FRA,
               "牧": LG_SHEP, "公": LG_FATA, "井": LG_WELL, "馬": LG_HORSE, "牛": LG_VAC,
               "寶": [([[BETEL, POLLUX]], "#A9C8FF", 0.5)], "行": [], "金": [], "暈": []}

MAINS = sorted({CAPELLA, SIRIUS, PROCYON, ALDEBARAN, BETEL, RIGEL, CASTOR, POLLUX, VEGA, ALTAIR, REGULUS,
                ARCTURUS, POLARIS} | set(KIDS) | set(BELT) | set(SHEEP)
               | {h for g in LG_ALL for s in g[0] for h in s if g[0] not in (SEG_CART, SEG_VAC)}
               | set(DIPPER))


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
# 三、自訂圖層：寶藏虛線、木星火星、金星（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    def treasure(s, pos, runs, disc):
        rr = runs(great_circle(*S[BETEL][:2], *S[POLLUX][:2]))
        s.polylines(rr, stroke="#A9C8FF", w=m.lw * 0.6, opacity=0.6, dash="1.0 0.8")

    def body(names):
        def f(s, pos, runs, disc):
            for nm in names:
                col, r = {"木": ("#FFFFFF", 0.80), "火": (COLORS["red"], 0.60), "金": ("#FFF6D8", 0.95)}[nm[0]]
                for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                    s.circle(p[0], p[1], r * 2.6, fill=col, opacity=0.16)
                    s.circle(p[0], p[1], r, fill=col, opacity=0.98)
        return f

    return [("寶藏（虛線）", treasure), ("木星與火星-2月26日", body(["木星2/26", "火星2/26"])),
            ("金星-2月27日清晨", body(["金星2/27"]))]


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
# 四、旁白字數（中文字＋外文音節；與 A 系列同一套算法，母音加上羅馬尼亞文 ă â î）
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
            n += max(1, len(re.findall(r"[aeiouyáéíóúąęįǫāēīōūŭăâî]+", w.lower().replace("ʼ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
def _pl(k):
    return (PL[k]["ra"], PL[k]["dec"])


TERMS = [
    (BELT, "Kastsy", "Kastsy", "The Mowers (Belarusian)", "割草的人（白俄）", "amber",
     "Stellarium belarusian 009：Касцы（A-22）"),
    ([CAPELLA], "Capra", "Capra", "The She-Goat", "母山羊（五車二）", "amber",
     "Stellarium romanian C3i；Otescu p.8：旁邊三顆星是她的小羊"),
    (KIDS, "Iezii", "—", "The three kids", "三隻小羊", "amber",
     "Otescu p.8 Iezii Caprei；三隻是 ε、ζ、η Aur（依 Stellarium／CRT 連線；英譯沒寫是哪三顆）"),
    ([CAPELLA], "Capella", "—", "Little she-goat (Latin)", "小母山羊（拉丁）", "blue",
     "拉丁 capra「母山羊」的指小詞"),
    (HAEDI, "Haedi", "—", "The Kids (Latin)", "兩隻小羊（拉丁）", "blue", "ζ、η Aur 的古名"),
    ([CAPELLA], "Kaza", "Kaza", "The She-Goat (Belarusian)", "母山羊（白俄）", "purple",
     "Stellarium belarusian 006：Каза（A-22）"),
    (stars_of(SEG_DOG), "Dulăul", "Dulaul", "The Mastiff", "看羊的大狗（大犬）", "amber",
     "Stellarium romanian Cma；dulău＝大型牧羊犬（DLRLC、Șăineanu）；天狼星本身叫 Zorilă（p.15）"),
    ([PROCYON, 36188], "Cățelul", "Catelul", "The Little Dog", "小狗（小犬）", "green",
     "Stellarium romanian Ctl；神話裡是「院子的小狗」（p.19）"),
    ([SIRIUS], "天狼", "—", "The Wolf (Chinese)", "天狼（中國）", "red", "Stellarium chinese 天狼"),
    (stars_of(SEG_HEN), "Cloșca cu pui", "Closca cu pui", "The Hatching Hen with Her Chicks",
     "母雞帶小雞（昴宿）", "green", "Stellarium romanian Ccp；冬夜的夜鐘（p.10）"),
    (stars_of(SEG_BOAR), "Vierii", "Vierii", "The Boars", "公豬（畢宿）", "red",
     "Stellarium romanian Vri；Taurul 公牛與它同連線，片中只講公豬（p.10）"),
    ([ALDEBARAN], "Luceafărul porcesc", "—", "The Bright Star of the Pig", "豬的亮星（畢宿五）", "red",
     "Otescu p.10：它升起時豬就醒來哼叫"),
    ([ALDEBARAN], "Deșteptătorul", "—", "The Alarm Clock", "鬧鐘", "white",
     "Otescu p.10、CRT：它升起時公雞開始啼"),
    (stars_of(SEG_RAR), "Rarița", "Rarita", "The Little Plough", "小犁", "amber",
     "Stellarium romanian Rar：腰帶＋參宿五、六、七（p.14）"),
    ([26727, 26311, 25930, BETEL], "Sfredelul mare", "Sfredelul mare", "The Great Auger", "大鑽子", "blue",
     "自繪：腰帶＝握柄、參宿四＝鑽頭（Otescu p.14、CRT）；Stellarium 連到參宿七"),
    (stars_of(SEG_SEC), "Secera", "Secera", "The Sickle", "鐮刀", "green",
     "Stellarium romanian Sec（6 顆；Otescu／CRT 說 7 顆星的弧）"),
    (BELT, "Trisfetitele", "Trisfetitele", "The Three Saints", "三聖人（腰帶）", "purple",
     "Stellarium romanian Trf；三位聖師（大巴西略、神學家格里高利、金口約翰）"),
    ([POLLUX], "Comoara", "—", "The Treasure", "寶藏（北河三）", "#A9C8FF",
     "Otescu p.11、p.14：大鑽子鑽穿它時世界末日"),
    (stars_of(SEG_CART), "Carul Mare", "Carul Mare", "The Great Chariot", "大車（北斗＋大熊）", "amber",
     "Stellarium romanian UMa（18 顆）"),
    (stars_of(SEG_SMALL), "Carul mic", "Carul mic", "The Little Chariot", "小車（小熊）", "green",
     "Stellarium romanian UMi"),
    ([POLARIS], "Candela cerului", "—", "The Sky's Votive Light", "天上的長明燈（北極星）", "white",
     "Otescu p.3：也叫 Împăratul 皇帝、Stâlpul 柱子"),
    ([CASTOR], "Romulus", "Romulus", "Romulus", "Romulus（北河二）", "blue", "Otescu p.11、CRT"),
    ([POLLUX], "Remus", "Remus", "Remus", "Remus（北河三）", "blue", "Otescu p.11、CRT"),
    ([CASTOR, POLLUX], "波蘭和立陶宛", "—", "Poland and Lithuania (Belarusian)", "波蘭和立陶宛（白俄）", "purple",
     "Stellarium belarusian 008（A-22）"),
    ([VEGA], "Ciobanul", "Ciobanul cu oile", "The Shepherd", "牧羊人（織女星）", "amber",
     "Stellarium romanian Cio；Otescu p.6"),
    (SHEEP, "oile", "—", "his sheep", "他的羊", "amber", "Otescu p.6：四顆星排成四邊形，是羊"),
    (stars_of(SEG_FATA), "Fata de împărat", "Fata de imparat", "The Emperor's Daughter with a Yoke",
     "挑扁擔的公主（牛郎星）", "green", "Stellarium romanian Fap；Otescu p.7：挑水給地獄裡的亡魂解渴"),
    ([ALTAIR], "牛郎", "—", "The Cowherd (Chinese)", "牛郎挑孩子（中國）", "amber", "H-七夕"),
    ([VEGA], "織女", "—", "The Weaver (Chinese)", "織女（中國）", "amber", "H-七夕"),
    ([9640, 5447, 3092], "Jgheabul", "Jgheabul si putul", "The Trough", "水槽（仙女座）", "blue",
     "Otescu p.8：仙女座＝井的水槽"),
    ([677, 113881, 113963, 1067], "Puțul", "Jgheabul si putul", "The Well", "井（飛馬大四邊形）", "blue",
     "Otescu p.8：四顆星是井口四角（補上 113963—1067 一邊）"),
    (stars_of(SEG_HORSE), "Calul", "Calul", "The Horse", "馬（獅子）", "amber", "Otescu p.11：也叫 Gavădul Mare"),
    (_pl("木星2/26"), "木星", "—", "Jupiter", "木星", "white", "台北 2/26 20:00；PyEphem"),
    (_pl("火星2/26"), "火星", "—", "Mars", "火星", "red", "2/19 衝日；台北 2/26 20:00"),
    ([REGULUS], "軒轅十四", "—", "Regulus", "軒轅十四", "white", ""),
    (stars_of(SEG_VAC), "Văcarul", "Vacarul", "The Herdsman", "放牛的人（牧夫）", "green",
     "Stellarium romanian Vca（15 顆，不含大角）；Otescu p.9"),
    ([ARCTURUS], "大角", "—", "Arcturus", "大角", "white", "不在 Văcarul 的連線上，只標星點"),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=56, D_r=60, D_fill=0.0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole

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

    NEAR = dict(s1=1.25, s2=1.0, gap=1.8)          # fov 25–30
    MID = dict(s1=1.6, s2=1.25, gap=2.4)           # fov 40–46
    WIDE = dict(s1=2.1, s2=1.6, gap=3.0)           # fov 50–64
    LB_KAST = term("Kastsy", **WIDE, zh="割草的人（白俄）")
    LB_CAPRA = term("Capra", **NEAR) + term("Iezii", **NEAR)
    LB_CAPX = (term("Capella", s1=0.9, s2=0.8, gap=1.3, zh="小母山羊（拉丁）")
               + term("Haedi", s1=0.9, s2=0.8, gap=1.3, zh="兩隻小羊（拉丁）")
               + term("Kaza", s1=0.9, s2=0.8, gap=1.3, zh="母山羊（白俄）"))
    LB_CAPW = term("Capra", **MID, zh="母山羊")                 # 19 鏡 fov 50：標在五車二左下（上方是安全區）
    LB_DOG = term("Dulăul", **MID, zh="看羊的大狗") + term("Cățelul", **MID)
    LB_WOLF = term("天狼", zh_only=True, s1=1.4, zh="中國：天狼")
    LB_FARM = term("Cloșca cu pui", **NEAR, zh="母雞帶小雞") + term("Vierii", **NEAR)
    LB_PIG = (term("Luceafărul porcesc", s1=1.05, s2=0.9, gap=1.5)
              + term("Deșteptătorul", s1=1.05, s2=0.9, gap=1.5))
    LB_RAR = term("Rarița", **NEAR)
    LB_SFR = term("Sfredelul mare", **NEAR)
    LB_SEC = term("Secera", **NEAR)
    LB_TRI = term("Trisfetitele", **NEAR, zh="三聖人")
    LB_TREAS = term("Comoara", s1=1.25, s2=1.0, gap=1.8, zh="寶藏")
    DSC = dict(s1=2.6, s2=2.0, gap=3.4, disc=True)  # 09 鏡 fov ~110
    LB_CART = term("Carul Mare", **DSC, zh="大車") + term("Carul mic", **DSC) + \
        term("Candela cerului", s1=2.2, s2=1.8, gap=3.0, disc=True, zh="天上的長明燈")
    LB_ROM = term("Romulus", **NEAR, zh="北河二") + term("Remus", **NEAR, zh="北河三")
    LB_POLLIT = term("波蘭和立陶宛", zh_only=True, s1=1.05, zh="白俄：波蘭和立陶宛")
    LB_SHEP = term("Ciobanul", **NEAR, zh="牧羊人") + term("oile", zh_only=True, s1=1.0, zh="他的羊")
    LB_SHEPW = term("Ciobanul", **MID, zh="牧羊人")             # 12 鏡 fov 45：織女上方是安全區，標在左邊
    LB_FATA = term("Fata de împărat", **MID, zh="挑扁擔的公主")
    LB_YOKE = (term("牛郎", zh_only=True, s1=1.45, zh="中國：牛郎挑孩子")
               + term("織女", zh_only=True, s1=1.45, zh="中國：織女")
               + [item([ALTAIR], "羅馬尼亞：公主挑水", "green", 1.45, 0.0, 0.0, "公主挑水"),
                  item([VEGA], "羅馬尼亞：牧羊人", "amber", 1.45, 0.0, 0.0, "牧羊人")])
    LB_WELL = term("Puțul", **WIDE, zh="井") + term("Jgheabul", **WIDE, zh="水槽")
    LB_HORSE = (term("Calul", **MID, zh="馬") + term("木星", zh_only=True, s1=1.4)
                + term("火星", zh_only=True, s1=1.4) + term("軒轅十四", zh_only=True, s1=1.1))
    LB_VAC = term("Văcarul", **MID, zh="放牛的人") + term("大角", zh_only=True, s1=1.1)
    LB_SIR = [item([SIRIUS], "天狼星", "white", 1.6, 0.0, 0.0, "天狼星")]

    label_sets = [(LB_KAST, "Kastsy（白俄）"), (LB_CAPRA, "Capra母山羊"), (LB_CAPX, "跨文化-母山羊"),
                  (LB_DOG, "大狗與小狗"), (LB_WOLF, "跨文化-天狼"), (LB_FARM, "母雞與公豬"),
                  (LB_PIG, "豬的亮星與鬧鐘"), (LB_RAR, "Rarița"), (LB_SFR, "Sfredelul"), (LB_SEC, "Secera"),
                  (LB_TRI, "Trisfetitele"), (LB_TREAS, "寶藏"), (LB_CART, "大車與長明燈"),
                  (LB_ROM, "Romulus與Remus"), (LB_POLLIT, "跨文化-波蘭和立陶宛"), (LB_SHEP, "牧羊人"), (LB_SHEPW, "牧羊人-遠景"), (LB_CAPW, "Capra-遠景"),
                  (LB_FATA, "挑扁擔的公主"), (LB_YOKE, "跨文化-扁擔"), (LB_WELL, "井和水槽"),
                  (LB_HORSE, "馬與行星"), (LB_VAC, "Văcarul"), (LB_SIR, "天狼星")]

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

    def sfit(hips, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, extra=(), fov=None):
        pts = [(x_of(S[h][0]), S[h][1]) for h in hips] + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        lim = m.Ds - f * 8 / 9 - 0.5                 # S：|cy|+fov·8/9 ≤ D_s
        cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    XM = x_of(lst_at(*TPE, 8, "2027/2/26 20:00"))      # 台北 2/26 20:00 子午線
    F01a = (round(XM, 2), 0.0, 64.0, 0.0)
    F01b = (round(XM + 4.0, 2), 2.0, 50.0, 0.0)
    F04 = sfit([CAPELLA] + KIDS, pad=0.10, fov=25.0, dy=-4.0)
    F05 = (F04[0], F04[1], 23.5, 0.0)                 # 05 鏡微推（單格會跟 04 迄格併頁，標籤就開不出來）
    F06 = sfit(stars_of(SEG_DOG) + [PROCYON, 36188], pad=0.08, minfov=45.0)
    F07 = sfit(stars_of(SEG_HEN) + stars_of(SEG_BOAR), pad=0.12, minfov=30.0)
    F08a = sfit(stars_of(SEG_RAR) + [BETEL] + stars_of(SEG_SEC), pad=0.12, fov=30.0)
    F08b = sfit(stars_of(SEG_RAR) + [BETEL, POLLUX], pad=0.08, fov=52.0, dx=1.5)
    F_SW = min(F08b[2], 50.0)                         # 08→09 換組格的 fov（＝gen_canva_pages 的 f_sw）
    SW = (0.0, yp, F_SW, 0.0)
    HZ = m.k * PHI_T
    F09 = fit(stars_of(SEG_CART) + stars_of(SEG_SMALL), ROT20, pad=0.10, extra=[(0, -HZ - 10)], dx=-8.0)
    ORIGIN10 = (0.0, 0.0, F_SW, 0.0)                  # 10 起格＝「北盤轉長圖-下移」那一格
    F10 = sfit(stars_of(SEG_FRA), pad=0.10, fov=30.0)
    F11 = sfit([VEGA] + SHEEP, pad=0.10, fov=25.0, dy=-2.0)
    F12a = sfit([VEGA] + SHEEP, pad=0.10, fov=30.0)
    F12b = sfit([VEGA, ALTAIR, 97278, 98036], pad=0.10, fov=45.0)
    F12c = sfit([VEGA, ALTAIR], pad=0.10, fov=45.0, extra=[(x_of(PL["金星2/27"]["ra"]), PL["金星2/27"]["dec"])])
    F14a = sfit(stars_of(SEG_WELL), pad=0.04, fov=54.0, dx=3.0)
    F14b = sfit(stars_of(SEG_WELL), pad=0.04, fov=54.0)
    PLAN = [(x_of(PL[k]["ra"]), PL[k]["dec"]) for k in ("木星2/26", "火星2/26")]
    F15a = sfit(stars_of(SEG_HORSE), pad=0.10, fov=42.0, extra=PLAN, dx=2.0)
    F15b = sfit(stars_of(SEG_VAC) + [ARCTURUS], pad=0.08, fov=42.0)
    F16 = sfit([VEGA] + SHEEP, pad=0.10, fov=30.0)
    F19a = sfit(stars_of(SEG_DOG), pad=0.10, fov=45.0)
    F19b = sfit([CAPELLA, SIRIUS], pad=0.10, fov=50.0)
    F19c = sfit(stars_of(SEG_HORSE), pad=0.10, fov=45.0, extra=PLAN)
    SCO = stars_of(RO["CON romanian Sco"]) + stars_of(RO["CON romanian Arc"])
    F20 = sfit(SCO, pad=0.06, fov=50.0)
    print(f"\n── 構圖 ──\n  01 {F01a}→{F01b}\n  04 {F04}\n  06 {F06}\n  07 {F07}\n  08 {F08a}→{F08b}\n"
          f"  09 {SW}→{F09}\n  10 {F10}\n  11 {F11}\n  12 {F12a}→{F12b}→{F12c}\n  14 {F14a}→{F14b}\n"
          f"  15 {F15a}→{F15b}\n  16 {F16}\n  19 {F19a}→{F19b}→{F19c}\n  20 {F20}")

    # ── 標籤畫面方向偏移（依各鏡實際方位；看過 SB-鏡頭牆後調） ──
    def shift(items, key, dx, dy):
        n = 0
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2); n += 1
        assert n, key

    # 長圖：dx/dy＝畫布方向（東在左，+dx＝往右＝往西）；盤：畫面方向（字不跟著盤轉）
    shift(LB_KAST, "Kastsy", 0.0, -6.0)
    shift(LB_CAPRA, "Capra", 0.0, 2.6); shift(LB_CAPRA, "Iezii", 0.0, -4.4)
    shift(LB_CAPX, "Capella", -3.8, -4.4); shift(LB_CAPX, "Kaza", -5.5, -8.0)   # 五車二左下（東），兩行一疊
    shift(LB_CAPX, "Haedi", 5.6, 0.0)                                          # ζ、η 右邊（西）
    shift(LB_CAPW, "Capra", -7.5, -1.5)
    shift(LB_DOG, "Dulăul", 7.0, -13.0); shift(LB_DOG, "Cățelul", 0.0, 4.0)
    shift(LB_WOLF, "天狼", -6.5, 1.5)
    shift(LB_FARM, "Cloșca cu pui", 0.0, 2.6); shift(LB_FARM, "Vierii", 6.0, 2.0)
    shift(LB_PIG, "Luceafărul porcesc", 0.0, -3.6); shift(LB_PIG, "Deșteptătorul", 0.0, -8.4)
    shift(LB_RAR, "Rarița", 0.0, -12.5); shift(LB_SFR, "Sfredelul mare", -4.0, -5.5)
    shift(LB_SEC, "Secera", 7.5, -6.0); shift(LB_TRI, "Trisfetitele", 6.5, -0.5)
    shift(LB_TREAS, "Comoara", 0.0, 2.6)
    shift(LB_CART, "Carul Mare", -34.0, -22.0); shift(LB_CART, "Carul mic", 0.0, -14.0)
    shift(LB_CART, "Candela cerului", 15.0, -6.0)
    shift(LB_ROM, "Romulus", 0.0, 1.0); shift(LB_ROM, "Remus", 0.0, -4.0)
    shift(LB_POLLIT, "波蘭和立陶宛", 6.0, 5.5)
    shift(LB_SHEP, "Ciobanul", 0.0, 2.0); shift(LB_SHEP, "oile", 4.5, -0.5)
    shift(LB_FATA, "Fata de împărat", 0.0, -5.0)
    shift(LB_YOKE, "牛郎", 0.0, -4.0); shift(LB_YOKE, "公主挑水", 0.0, -6.0)
    shift(LB_YOKE, "織女", -8.0, -9.0); shift(LB_YOKE, "牧羊人", -8.0, -11.5)   # 織女上方是安全區
    shift(LB_SHEPW, "Ciobanul", -9.0, -0.5)
    shift(LB_WELL, "Puțul", 0.0, 0.0); shift(LB_WELL, "Jgheabul", 3.0, 4.5)
    shift(LB_HORSE, "Calul", 0.0, 7.0); shift(LB_HORSE, "木星", 0.0, 2.4)
    shift(LB_HORSE, "火星", 0.0, -2.4); shift(LB_HORSE, "軒轅十四", 3.0, -2.2)
    shift(LB_VAC, "Văcarul", -12.0, -8.0); shift(LB_VAC, "大角", 0.0, -2.2)
    shift(LB_SIR, "天狼星", -6.0, 0.0)
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
    MARKS = [(MAINS, "主角星白點", "dot"), ([POLARIS, SIRIUS, ALDEBARAN, VEGA, ALTAIR, ARCTURUS], "單星光暈", "ring")]
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
        dict(code="01", kind="Z", sec=11, north=True, frames=[F01a, F01b], layers=["白"],
             labels=ls("Kastsy（白俄）"), labels_end=[],
             vo="上週在白俄羅斯，天上有割草的人和以利亞的車。往南到喀爾巴阡山：同一片星空，羅馬尼亞的牧羊人看見——一座農場。",
             card="羅馬尼亞：星空農場",
             note="長圖（台北 2/26 20:00 子午線）fov 64→50；冬季星空全景；腰帶 Kastsy（白俄，琥珀）起格開、迄格標籤收、"
                  "連線淡出→開場字卡"),
        dict(code="02", kind="Z", sec=12, north=True, frames=[F01b], layers=[], labels=[],
             overlay="C-A23-01_Otescu的星圖與回信", overlay_layers=["星圖層", "回信層"],
             vo="一八九六年，羅馬尼亞的數學教育家 Ion Otescu，把星圖寄給全國的鄉村老師，請他們去問村裡最老的農民：天上的星星叫什麼？",
             card="1896 年寄出星圖",
             note="長圖定格；疊 C-A23-01（星圖示意→羅馬尼亞王國 1896 年國界示意＋39 處回信；自繪，不臨摹書影）"),
        dict(code="03", kind="Z", sec=10, north=True, frames=[F01b], layers=[], labels=[],
             overlay="C-A23-01_Otescu的星圖與回信", overlay_layers=["一年層"],
             vo="他發現，農民看星星，多半是在夏天農忙，拿星星報時；一年其他時候，還一直盯著星星的，只有牧羊人。",
             card="只有牧羊人還在看",
             note="畫面不動；C-A23-01 一年層（12 個月：六—九月農民報時、其餘月份只有牧羊人；Otescu p.1）"),
        dict(code="04", kind="S", sec=9, north=True, frames=[F01b, F04], layers=["羊"],
             labels=ls("Capra母山羊"), labels_start=[],
             vo="冬夜的天，就是牧羊人的農場。北邊高空的五車二，是母山羊 Capra，旁邊三顆小星，是她的三隻小羊。",
             card="母山羊和三隻小羊",
             note="長圖往上（北）滑到御夫 fov 25；Capra（琥珀：五車二＋ε、ζ、η Aur）"),
        dict(code="05", kind="Z", sec=11, north=True, frames=[F04, F05], layers=["羊", "拉"],
             labels=ls("Capra母山羊", "跨文化-母山羊"),
             vo="古羅馬人也叫它小母山羊，旁邊只有兩隻小羊；羅馬尼亞多了一隻，剛好跟羅馬尼亞童話〈山羊和三隻小羊〉一樣。",
             card="Capella＝小母山羊",
             note="fov 25 不動；跨文化標籤：拉丁 Capella、Haedi（ζ、η，藍色小段）／白俄 Kaza（A-22）；"
                  "角落小字「童話：Ion Creangă，1875」（原生文字）"),
        dict(code="06", kind="S", sec=9, north=True, frames=[F05, F06], layers=["狗", "暈"],
             labels=ls("大狗與小狗"), labels_start=ls("Capra母山羊", "跨文化-母山羊"), labels_end=ls("大狗與小狗", "跨文化-天狼"),
             vo="往南，最亮的天狼星，在看羊的大狗 Dulăul 身上——中國人卻說它是狼；左上方的南河三，是一隻小狗。",
             card="天狼星＝看羊大狗身上",
             note="長圖往下（南）滑到大犬 fov 45；Dulăul（琥珀，6 星，天狼星在其中）、Cățelul（綠）；迄格小標 中國「天狼」"),
        dict(code="07", kind="S", sec=8, north=True, frames=[F06, F07], layers=["豬", "暈"],
             labels=ls("母雞與公豬"), labels_start=ls("大狗與小狗", "跨文化-天狼"), labels_end=ls("母雞與公豬", "豬的亮星與鬧鐘"),
             vo="西邊，昴宿是母雞帶小雞；畢宿是一群公豬，畢宿五叫「豬的亮星」，也有人叫它「鬧鐘」。",
             card="豬的亮星＝鬧鐘",
             note="長圖往右（西）滑：Cloșca cu pui（綠）、Vierii（紅，畢宿 V）；迄格 Luceafărul porcesc／豬的亮星、"
                  "Deșteptătorul／鬧鐘"),
        dict(code="08", kind="Z", sec=17, north=True, frames=[F07, F08a, F08b],
             layers=["犁", "鑽", "鐮", "聖", "寶"],
             labels_start=ls("母雞與公豬", "豬的亮星與鬧鐘"), labels=ls("Rarița", "Sfredelul", "Secera"),
             labels_end=ls("Rarița", "Sfredelul", "Secera", "Trisfetitele", "寶藏"),
             vo="獵戶座最熱鬧：同一塊天，疊了四個羅馬尼亞星座——腰帶連上周圍幾顆星，是一把小犁 Rarița；腰帶當握柄、參宿四當鑽頭，是一支大鑽子；下面那彎小星是鐮刀；腰帶三顆星，又是三位聖人。",
             card="一個獵戶，四個星座",
             note="長圖回獵戶 fov 30；四層連線依旁白一層一層進（Canva 裡各層分頁淡入）：Rarița（琥珀，Stellarium）→"
                  "Sfredelul mare（藍，自繪：腰帶握柄＋參宿二→參宿四鑽桿；Otescu p.14、CRT）→Secera（綠，Stellarium 6 星）"
                  "→Trisfetitele（紫）；迄格拉遠 fov 46 帶進北河三，鑽頭方向淡虛線（寶藏層）＋小字「寶藏」"),
        dict(code="09", kind="R", sec=7, north=True, horizon=[PHI_T], frames=[SW, F09],
             layers=["車", "暈"], labels=ls("大車與長明燈"), labels_start=[],
             vo="北邊爬上來的北斗，也是一輛大車 Carul Mare；北極星，是天上的長明燈。",
             card="北斗＝大車",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）；轉到台北 2/26 20:00 面北（{ROT20:+.1f}°）"
                  "並拉遠；Carul Mare（琥珀，18 星大車）、Carul mic（綠）；北極星細圈＋Candela cerului／長明燈；"
                  "搖光 20:00 才 7°（山剪影下緣）"),
        dict(code="10", kind="S", sec=9, north=True, frames=[ORIGIN10, F10], layers=["兄"],
             labels=ls("Romulus與Remus"), labels_start=[],
             labels_end=ls("Romulus與Remus", "跨文化-波蘭和立陶宛"),
             vo="雙子座兩顆亮星，叫 Romulus 和 Remus——建立羅馬的那對兄弟；上週在白俄羅斯，這兩顆叫波蘭和立陶宛。",
             card="雙子＝羅馬兄弟",
             note="【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）；滑到雙子 fov 30：Frații（藍）；"
                  "Romulus（北河二）、Remus（北河三）；迄格小標 白俄「波蘭和立陶宛」（A-22）"),
        dict(code="11", kind="S", sec=12, north=True, frames=[F10, F11], layers=["牧"],
             labels=ls("牧羊人"), labels_start=ls("Romulus與Remus", "跨文化-波蘭和立陶宛"),
             vo="那牧羊人在哪？天琴座的織女星，就是牧羊人 Ciobanul，旁邊四顆小星是他的羊。這個季節，他要過了半夜，才從東北方升起。",
             card="牧羊人＝織女星",
             note="長圖往左（東）一路滑到天琴 fov 25（往東＝時間往後）；Ciobanul cu oile（琥珀：織女＋四邊形）；"
                  "角落時鐘角標「00:34 升起・01:36 高過 10°」（原生文字）"),
        dict(code="12", kind="S", sec=11, north=True, frames=[F11, F12b, F12c], layers=["牧", "公", "金", "暈"],
             labels=ls("牧羊人-遠景", "挑扁擔的公主"), labels_start=ls("牧羊人"),
             vo="天快亮時，牧羊人已經爬到半天高；他右下方，牛郎星和兩旁的小星，是挑著扁擔的公主——挑的是水，要給亡魂解渴。",
             card="牛郎星＝挑水公主",
             note="長圖（台北 2/27 05:30 東方）從織女拉遠到 fov 45、往右下帶出 Fata de împărat（綠：河鼓三—牛郎—河鼓一）；"
                  "迄格再往下帶進東南低空金星（自訂層，不加標籤）——長圖上三者 fov 45 同框"),
        dict(code="13", kind="Z", sec=9, north=True, frames=[F12c], layers=["牧", "公", "金"],
             labels=ls("跨文化-扁擔"),
             overlay="C-A23-02_換了性別的牛郎織女",
             vo="在中國，挑扁擔的是牛郎，擔著兩個孩子；到了羅馬尼亞，挑扁擔的換成公主，牧羊的反而是織女星。",
             card="牛郎挑孩子，公主挑水",
             note="fov 45 不動；跨文化標籤層（中國 牛郎、織女／羅馬尼亞 公主、牧羊人）；迄格疊 9:16 圖卡 C-A23-02"),
        dict(code="14", kind="S", sec=13, north=True, cut=True, frames=[F14a, F14b], layers=["井"],
             labels=ls("井和水槽"),
             overlay="C-A23-06_19點10分往西看", overlay_layers=["地平線層", "井層"],
             vo="羊要喝水，天上也有井：飛馬座的大四邊形是一口井 Puțul，仙女座那一串，是接出來的水槽。這幾天天一黑，這口井已經有一半沉到西邊地平線下。",
             card="井和水槽",
             note="【硬切】（從 x −150 到 +136，滑過去要橫越整張畫布）飛馬—仙女 fov 54：Puțul cu jgheab（藍；補上室宿一—壁宿一，"
                  "Otescu p.8）；迄格疊 C-A23-06「19:10 往西看」（地平座標：室宿一已落、室宿二 4.6°）"),
        dict(code="15", kind="S", sec=9, north=True, cut=True, frames=[F15a, F15b], layers=["馬", "牛", "行", "暈"],
             labels_start=ls("馬與行星"), labels=ls("Văcarul"), labels_end=ls("Văcarul"),
             vo="東方的獅子座，在羅馬尼亞是一匹馬 Calul；十點過後，牧夫座爬上東北方低空——他叫 Văcarul，放牛的人。",
             card="獅子座＝一匹馬",
             note="【硬切】長圖獅子 fov 42：Calul（琥珀）＋木星、火星（自訂層；木星在獅子座西緣、連線外；火星貼著軒轅十三）"
                  "→往左（東）滑到牧夫：Văcarul（綠；連線沒有大角，大角只標星點）"),
        dict(code="16", kind="S", sec=17, north=True, frames=[F15b, F16], layers=["牧"],
             labels=ls("牧羊人"), labels_start=ls("Văcarul"),
             overlay="C-A23-03_Miorița", overlay_layers=["山坡層", "流星層"],
             vo="羅馬尼亞人相信，每個人在天上都有一顆自己的星；人走了，星就掉下來。最有名的民謠〈Miorița〉裡，牧羊人知道自己要被同伴殺害，交代小母羊：跟羊群說，我結婚了——「婚禮上，掉下一顆星」。",
             card="婚禮上，掉下一顆星",
             note="長圖往左滑回天琴（牧羊人）fov 30；迄格疊 C-A23-03（山坡羊群→一顆流星；簡筆，不畫兇殺）"),
        dict(code="17", kind="Z", sec=8, north=True, frames=[F16], layers=["牧"], labels=ls("牧羊人"),
             overlay="C-A23-03_Miorița", overlay_layers=["婚禮層"],
             vo="太陽和月亮替他捧著婚冠，冷杉和楓樹是賓客，高山是神父，鳥是樂師，星星是火把。",
             card="星星是火把",
             note="畫面不動；C-A23-03 婚禮層（日月、冷杉、楓樹、高山、鳥、星）"),
        dict(code="18", kind="Z", sec=6, north=True, frames=[F16], layers=["牧"], labels=ls("牧羊人"),
             overlay="C-A23-04_羅馬尼亞星名小辭典",
             vo="這集的羅馬尼亞星名，整理成一張小辭典，可以存起來。",
             card="羅馬尼亞星名小辭典",
             note="畫面不動；疊 9:16 圖卡 C-A23-04（可存圖）"),
        dict(code="19", kind="S", sec=15, north=True, cut=True, frames=[F19a, F19b, F19c],
             layers=["狗", "羊", "馬", "行", "暈"],
             labels_start=ls("天狼星"), labels=ls("天狼星", "Capra-遠景"), labels_end=ls("馬與行星"),
             overlay="C-A23-05_這週末抬頭看",
             vo="這週末在台灣：晚上八點，大狗天狼星在正南方，母山羊在北邊高空；木星和剛衝日的火星，在東方那匹馬的身旁。清晨五點往東北看，牧羊人已經在等天亮。",
             card="這週末抬頭看",
             note="【硬切】長圖（台北 2/26 20:00）：天狼星→五車二→往左滑到獅子座（木星、火星）；迄格疊 9:16 圖卡 C-A23-05"),
        dict(code="20", kind="S", sec=8, north=True, frames=[F19c, F20], layers=[], labels=[],
             vo="下週五，我們飛到亞馬遜：圖卡諾人看哪個星座在黃昏落下，就知道哪一次漲水要來。",
             card="下集見｜3/5 圖卡諾：亞馬遜的星空雨季曆",
             note="長圖往左（東）滑到天蠍—人馬（圖卡諾 Aña 大蛇所在；不開羅馬尼亞連線）；端卡＋追蹤 CTA"),
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

    print(f"  北盤旋轉角（台北 2/26 20:00，面向北方）：{ROT20:+.1f}°")
    print("  天體（台北，J2000）：" + "、".join(f"{k} RA {v['ra']:.1f} Dec {v['dec']:+.1f} 高 {v['alt']}°"
                                          for k, v in PL.items()))
    print(f"  x：參宿四 {x_of(S[BETEL][0]):+.1f}、天狼 {x_of(S[SIRIUS][0]):+.1f}、五車二 {x_of(S[CAPELLA][0]):+.1f}、"
          f"昴宿 {x_of(S[17702][0]):+.1f}、北河三 {x_of(S[POLLUX][0]):+.1f}、軒轅十四 {x_of(S[REGULUS][0]):+.1f}、"
          f"大角 {x_of(S[ARCTURUS][0]):+.1f}、織女 {x_of(S[VEGA][0]):+.1f}、牛郎 {x_of(S[ALTAIR][0]):+.1f}、"
          f"金星 {x_of(PL['金星2/27']['ra']):+.1f}、室宿二 {x_of(S[113963][0]):+.1f}、天大將軍一 {x_of(S[9640][0]):+.1f}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT20, "lst0": LST0, "phi": PHI_T, "bodies": PL},
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


def _place_labels(L):
    """標籤畫面方向偏移（第二輪起依 SB-鏡頭牆／對位參考逐條調；dx/dy 單位＝畫布單位）"""
    pass


if __name__ == "__main__":
    build()
