# -*- coding: utf-8 -*-
"""A-22 白俄羅斯：農民曆星空與以利亞的馬車｜大畫布 v4.6

論點：白俄羅斯的 20 個星座是一本掛在天上的農民曆——①農具與農活（大車、小車、割草的人、耙子、
犁田的人、篩子、釘子）②院子裡的動物（母雞、草蛇、母山羊、公羊）③後來蓋上的一層教堂（以利亞的車、
耶穌的椅子、荊棘冠、聖彼得的十字架、聖喬治的蛇）。北斗一個星群就同時有兩層：大車 Voz → 以利亞的
火焰馬車 Illioŭ voz。天龍＝聖喬治的蛇，15 顆裡有 7 顆是中國紫微左右垣的牆星（導流 H-元宵）。

來源：Stellarium belarusian（Alexander Wolf、Tsimafei Avilin、Johan Meuris；20 個星座＋2 顆具名星）；
跨文化：Stellarium mongolian（金樁，A-07）、sami（Boahjenásti，A-21）、norse（Karlvagn，A-15）、
romanian（Carul Mare，A-23）、chinese（紫微左右垣 CON 032／033）；《史記・天官書》「斗為帝車」。
天象 PyEphem 4.2.1 自算。逐字稿：04_腳本庫/A-22-…-逐字稿-v1.md。

連線：全部照 Stellarium belarusian；北斗兩層（Voz 琥珀、Illioŭ voz 紅＝同一組線、換色）；
  紫微左右垣照 chinese CON 032／033，琥珀「虛線」自訂層（L_lines 不能畫虛線），
  左樞 HIP 75458 與右樞 HIP 68756 之間是宮門、不連（Zmiej 的紅線在這裡直接連過去）。
  月亮（2/19、2/20 兩個位置）、木星、火星：自訂層，J2000 astrometric（與星表同框）、台北站心。

鏡頭路線：01–08 北盤（明斯克 53.9°N 面北；01–07 山＝明斯克北方地平線）
  → 08 迄格推進盤心、轉回 0°（＝換組格）→ 09【換長圖】沿走廊下來、往西（右）滑到獵戶
  → 10 拉遠 → 11 往東（左）到牧夫—后髮 → 12 往西到昴宿／畢宿／五車二 → 白羊 → 13 回獵戶
  → 14【換北盤】（gen_canva_pages 自動插回中心／上移／長圖轉北盤）天龍＋紫微垣
  → 15【換長圖】（自動插歸位／北盤轉長圖／下移）雙子 → 16 小辭典 → 17 獵戶→獅子（月、木、火）
  → 18【換北盤】紫微垣（左半）＋端卡。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 180 → 北盤旋轉角：rot＝(lst − LST明斯克 − 180) 收在 (−180,180]；
             明斯克 2/19 LST：18:00 41.9°、20:00 72.0°、22:00 102.1° → rot −41.9／−72.0／−102.1。
             lst 愈靠近 252（明斯克 20:00 的 rot＝0）盤愈少轉，但長圖右端的白羊（RA 28–32）會出畫布；
             lst=180 時白羊 x +148…+152，12 鏡迄格右緣 ≤ 172（|x| ≤ 180）。
             長圖上：獵戶腰帶 x +96、五車二 +101、畢宿五 +111、昴宿 +123、雙子 +64～+67、軒轅十四 +28、
             后髮 −6～−17、大角星 −34、牧夫 β −45。台北 2/19 20:00 的子午線（LST 90.8）在 x ＝ +89.2。
  D_s = 56、D_r = 60 → 決定因素是 12 鏡的五車二（Kaza，+46.0）：S 鏡頭 |cy|+fov·8/9 ≤ D_s，
             而五車二要離畫面上緣 ≥ 上方安全區（250/1920＝13%）。D_s 45 時五車二根本進不了長圖畫面；
             D_s 56 時 fov 40 的畫面上緣 56、五車二離上緣 10 單位 ≥ 安全區 9.2。
             北斗（+49.3…+61.8）、小熊、天龍在 dec < 60 的部分全在北盤圖層組上（完整圓），
             北斗的鏡頭（01–08）不用大畫布，不受縫合帶影響；北斗的標籤一律 disc=True。
  D_fill = −4 → k=1.9099、R_fill=179.53（盤寬 ÷ 畫布寬＝0.997 ⚠ 只差 0.3%，Canva 千萬別設成同寬）：
             01 鏡要同時放進北極星、兩輛車（明斯克 20:00 北斗在右下，x +66）和明斯克北方地平線
             （盤心下方 kφ＝103），畫面角落離盤心 ~170；R_fill 用到 |x_t|+R_fill ≤ 180 的上限附近。
  x_tN = x_tS = 0

逐字稿要改的地方（素材時發現；已改進 v1 分鏡表的畫面欄）
  04 鏡「明斯克 18:00→20:00」：18:00 明斯克天還亮（日落 18:27），而且 01–03 已經停在 20:00、
     要先倒轉 30° 才轉得回 18:00 → 改 20:00→22:00（同樣 −30.1°）；05–08 停在 22:00。

check_shots 的 ⚠（判斷後接受；跑完逐條看過）
  01–08、14、18 R 鏡頭「畫面含長圖側扇區」：全程在北盤圖層組上；換組只有：
  08 迄格＝盤心 fov 48、0°（盤緣圈內，逐點重合）→ 09 起格同一格（同框換長圖）；
  14、18 由 gen_canva_pages 插「回中心／上移／長圖轉北盤」（盤心 0°），15 由它插「歸位／北盤轉長圖／下移」。
  08 迄格轉回 0° 是 −102.1° → 0°＝順時針 102°（時間倒流）：只發生在推進盤心那一段（fov 80→48），
  盤心附近只有小熊在轉；14→15、18 的歸位頁同理（−72° → 0°）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-22"
OUT = os.path.join(BASE, "05_素材/A-22_白俄羅斯/_v4大畫布")
LST0 = 180.0
TPE = (25.0330, 121.5654)
MSQ = (53.90, 27.57)
PHI_M = 53.90                   # 01–07 明斯克面北的地平線緯度


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


T_MSQ = {"20:00": "2027/2/19 20:00", "22:00": "2027/2/19 22:00"}
ROT = {k: rot_at(*MSQ, 3, v) for k, v in T_MSQ.items()}


def bodies():
    """J2000 astrometric（與星表同框）、台北站心"""
    import ephem
    out = {}
    for tag, when in (("2/19", "2027/2/19 20:00"), ("2/20", "2027/2/20 20:00")):
        o = _obs(*TPE, 8, when)
        for nm, b in (("月亮", ephem.Moon()), ("木星", ephem.Jupiter()), ("火星", ephem.Mars())):
            b.compute(o)
            out[f"{nm}{tag}"] = dict(ra=math.degrees(b.a_ra), dec=math.degrees(b.a_dec),
                                     alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1))
    return out


PL = bodies()


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, CAPELLA, REGULUS, CASTOR, POLLUX = 11767, 24608, 49669, 36850, 37826
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
UMI = [11767, 85822, 82080, 77055, 79822, 75097, 72607]
BELT = [26727, 26311, 25930]
RAKE = [26263, 26173, 26563, 25923]
BOO = [74666, 73555, 71075, 71053, 69673, 67927, 72105, 67459]
ARCTURUS = 69673
COMA = [64241, 64394, 60742]
PLEIADES = [17847, 17702, 17573, 17531, 17489, 17499, 17608]
HYADES = [20205, 20455, 20648, 20889, 20894, 21421]
ARIES = [13209, 9884, 8903, 8832]
ORION = [27989, 26207, 25336, 25930, 24436, 26727, 27366]
DRACO = [87585, 87833, 85670, 85829, 94376, 97433, 94648, 89937, 83895, 80331, 78527, 75458,
         68756, 61281, 56211]
SHARED7 = [75458, 78527, 80331, 83895, 68756, 61281, 56211]     # 天龍＝紫微左右垣的牆星
ZW_L = [75458, 78527, 80331, 83895, 92782, 101260, 114222, 3721]
ZW_R = [68756, 61281, 56211, 46977, 33104, 22783, 15520]
MAINS = ([POLARIS, CAPELLA, REGULUS, CASTOR, POLLUX, ARCTURUS] + DIPPER + UMI[1:] + BELT + RAKE
         + PLEIADES + HYADES + ARIES + COMA + [27989, 24436])


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu, key="id"):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c[key] if key == "id" else c["common_name"][key]] = [s for s in segs if len(set(s)) >= 2]
    return out


BY = load_sc("belarusian")
B = lambda n: BY[f"CON belarusian {n:03d}"]
SEG_CART, SEG_SMALL = B(1), B(16)
SEG_MOW, SEG_RAKE = B(9), B(12)
SEG_PLOUGH, SEG_SIEVE = B(11), B(15)
SEG_HENS, SEG_SNAKES, SEG_RAM = B(3), B(7), B(13)
SEG_THRONE, SEG_CROWN, SEG_CROSS = B(17), B(5), B(4)
SEG_SERPENT, SEG_TWINS, SEG_PL = B(14), B(18), B(8)
CH = load_sc("chinese")
SEG_ZW = CH["CON chinese 032"] + CH["CON chinese 033"]
assert sorted({h for s in SEG_SERPENT for h in s}) == sorted(DRACO)
assert [h for s in SEG_RAKE for h in s] == [26263, 26173, 26563, 26173, 25923]

LG_CART = [(SEG_CART, "amber", 1.0)]
LG_SMALL = [(SEG_SMALL, "green", 1.0)]
LG_FIRE = [(SEG_CART, "red", 1.1)]
LG_FARM = [(SEG_MOW, "amber", 1.0), (SEG_RAKE, "green", 0.9)]
LG_PS = [(SEG_PLOUGH, "blue", 1.0), (SEG_SIEVE, "purple", 1.0)]
LG_YARD = [(SEG_HENS, "green", 0.9), (SEG_SNAKES, "red", 1.0), (SEG_RAM, "blue", 1.0)]
LG_THRONE = [(SEG_THRONE, "purple", 1.0)]
LG_CHURCH = [(SEG_CROWN, "red", 1.0), (SEG_CROSS, "blue", 1.0)]
LG_SERPENT = [(SEG_SERPENT, "red", 1.0)]
LG_TWINS = [(SEG_TWINS, "#A9C8FF", 0.8), (SEG_PL, "amber", 1.2)]
LG_ALL = LG_CART + LG_SMALL + LG_FARM + LG_PS + LG_YARD + LG_THRONE + LG_CHURCH + LG_SERPENT + LG_TWINS
LINE_SETS = [(LG_CART, "連線-Voz大車"), (LG_SMALL, "連線-Maly voz小車"), (LG_FIRE, "連線-以利亞的車"),
             (LG_FARM, "連線-割與耙"), (LG_PS, "連線-犁與篩"), (LG_YARD, "連線-院子"),
             (LG_THRONE, "連線-耶穌的椅子"), (LG_CHURCH, "連線-荊棘冠與十字架"),
             (LG_SERPENT, "連線-聖喬治的蛇"), (LG_TWINS, "連線-雙胞胎")]
LINES_KEY = {"L4": "星座連線", "車": "連線-Voz大車", "小": "連線-Maly voz小車", "火": "連線-以利亞的車",
             "割": "連線-割與耙", "犁": "連線-犁與篩", "院": "連線-院子", "椅": "連線-耶穌的椅子",
             "冠": "連線-荊棘冠與十字架", "蛇": "連線-聖喬治的蛇", "雙": "連線-雙胞胎",
             "紫": "紫微垣（虛線）", "行": "木星與火星", "月19": "月亮-2月19日", "月20": "月亮-2月20日",
             "暈": "單星光暈", "圈": "共用七星圈"}
LINE_GROUPS = {"L4": LG_ALL, "車": LG_CART, "小": LG_SMALL, "火": LG_FIRE, "割": LG_FARM, "犁": LG_PS,
               "院": LG_YARD, "椅": LG_THRONE, "冠": LG_CHURCH, "蛇": LG_SERPENT, "雙": LG_TWINS,
               "紫": [(SEG_ZW, "amber", 0.8)], "行": [], "月19": [], "月20": [], "暈": [], "圈": []}


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
# 三、自訂圖層：紫微垣虛線、月亮、木星、火星（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    AMB = COLORS["amber"]

    def ziwei(s, pos, runs, disc):
        rr = []
        for seg in SEG_ZW:
            for a, b in zip(seg, seg[1:]):
                rr += runs(great_circle(*S[a][:2], *S[b][:2]))
        s.polylines(rr, stroke=AMB, w=m.lw * 0.8, opacity=0.92, dash="1.1 0.7")

    def body(names):
        def f(s, pos, runs, disc):
            for nm in names:
                col, r = {"月": ("#FFF6D8", 1.25), "木": ("#FFFFFF", 0.80), "火": (COLORS["red"], 0.60)}[nm[0]]
                for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                    s.circle(p[0], p[1], r * 2.6, fill=col, opacity=0.16)
                    s.circle(p[0], p[1], r, fill=col, opacity=0.98)
        return f

    return [("紫微垣（虛線）", ziwei), ("木星與火星", body(["木星2/19", "火星2/19"])),
            ("月亮-2月19日", body(["月亮2/19"])), ("月亮-2月20日", body(["月亮2/20"]))]


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
# 四、旁白字數（中文字＋外文音節；與 A 系列同一套算法）
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
            n += max(1, len(re.findall(r"[aeiouyáéíóúąęįǫāēīōūŭ]+", w.lower().replace("ʼ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (DIPPER, "Voz", "（無）", "The Cart", "大車（北斗）", "amber",
     "白俄文 Воз＝運貨的大車；Stellarium 只收 Іллёў воз，Voz 見 Avilin 2008 與作者部落格「Вялікая Мядзведзіца」篇"),
    (UMI, "Maly voz", "Maly Vos", "The Small Cart", "小車（小熊）", "green", "Stellarium belarusian 016：Малы воз"),
    ([POLARIS], "Hvozdz", "Gvozd", "The Nail", "釘子（北極星）", "white",
     "Stellarium belarusian 010：Гвоздзь「天空繞著它轉」；Г 讀 [ɣ]，片中寫 H（嚴格轉寫 Hvozdź）"),
    ([POLARIS], "Altan gadas", "Altan Hadaas", "Golden Stake (Mongolian)", "金樁（蒙古）", "blue",
     "蒙古 Алтан гадас（A-07）；片中只放拉丁轉寫，西里爾留在小辭典"),
    ([POLARIS], "Boahjenásti", "Boahjenaste", "Sky Support (Sami)", "撐住天空的星（薩米）", "white",
     "Stellarium sami 004（A-21）"),
    (DIPPER, "Illioŭ voz", "Illyouo voz", "Elias's Cart", "以利亞的車（北斗）", "red",
     "Stellarium belarusian 001：Іллёў воз；Stellarium 拼法 Illyouo voz 不是標準轉寫"),
    (DIPPER, "Karlvagn", "Karlvagn", "Man's Cart (Norse)", "男人的車（北歐）", "amber", "Stellarium norse（A-15）"),
    (DIPPER, "Carul Mare", "Carul Mare", "The Great Chariot (Romanian)", "大車（羅馬尼亞）", "amber",
     "Stellarium romanian UMa（18 顆，比北斗大；A-23）"),
    (DIPPER, "斗為帝車", "—", "The Dipper is the Emperor's chariot", "天帝的車（《史記》）", "amber",
     "《史記・天官書》「斗為帝車，運于中央，臨制四鄉」"),
    (BELT, "Kastsy", "Kastsy", "The Mowers", "割草的人（腰帶）", "amber", "Stellarium belarusian 009：Касцы"),
    (RAKE, "Hrabli", "Grabli", "The Rake", "耙子", "green",
     "Stellarium belarusian 012：Граблі；柄 HIP 26263→26173（6.4、6.7 等）、橫桿 υ Ori—26173—49 Ori；不是 M42"),
    (BOO, "Rataj", "Rataj", "The Ploughman", "犁田的人（牧夫）", "blue", "Stellarium belarusian 011：Ратай（古詞）"),
    (COMA, "Sita", "Sito", "The Sieve", "篩子（后髮）", "purple",
     "Stellarium belarusian 015：Сіта「上帝拿它篩過 жыта 黑麥」；位置待查核（另有資料說是昴宿）"),
    (PLEIADES, "Kurki", "Kurki", "The Hens", "母雞（昴宿）", "green",
     "Stellarium belarusian 003：Куркі；主程式版譯 The Chicks，куркі 是母雞（複數）"),
    (HYADES, "Vuzhy", "Vuzhy", "The Grass Snakes", "草蛇（畢宿）", "red", "Stellarium belarusian 007：Вужы"),
    ([CAPELLA], "Kaza", "Kaza", "The She-Goat", "母山羊（五車二）", "amber", "Stellarium belarusian 006：Каза"),
    (ARIES, "Baran", "Baran", "The Ram", "公羊（白羊）", "blue", "Stellarium belarusian 013：Баран"),
    (ORION, "Kreselca Pana Jezusa", "Kreselca Pana Jezusa", "The Throne of Jesus", "耶穌的椅子（獵戶）", "purple",
     "Stellarium belarusian 017：Крэсельца Пана Езуса"),
    (DRACO, "Zmiej", "Zmej", "The Serpent", "聖喬治殺的蛇（天龍）", "red",
     "Stellarium belarusian 014：Змей；15 顆裡 7 顆＝紫微左右垣（自算）"),
    (ZW_L, "紫微左垣", "Zǐwēi Zuǒyuán", "Purple Forbidden Left Wall", "紫微左垣", "amber", "Stellarium chinese 033"),
    (ZW_R, "紫微右垣", "Zǐwēi Yòuyuán", "Purple Forbidden Right Wall", "紫微右垣", "amber", "Stellarium chinese 032"),
    ([CASTOR, POLLUX], "波蘭和立陶宛", "Poland and Lithuania", "Poland and Lithuania", "波蘭和立陶宛（北河二、三）",
     "amber", "Stellarium belarusian 008（無白俄文；舊版 description：立陶宛大公國與波蘭王國的象徵）；不分哪顆是哪國"),
    ([35550, 34088, 32362, 31681], "Blizniuki", "Blizniuki", "The Twins", "雙胞胎（雙子）", "#A9C8FF",
     "Stellarium belarusian 018：Блізнюкі"),
    ((PL["月亮2/19"]["ra"], PL["月亮2/19"]["dec"]), "月亮 2/19", "—", "Moon, Feb 19 20:00", "月亮（2/19）", "white",
     f"台北 2/19 20:00：97%、高 {PL['月亮2/19']['alt']}°（PyEphem 自算）"),
    ((PL["月亮2/20"]["ra"], PL["月亮2/20"]["dec"]), "月亮 2/20 元宵", "—", "Moon, Feb 20 20:00", "月亮（2/20 元宵）",
     "white", f"台北 2/20 20:00：99.7%、高 {PL['月亮2/20']['alt']}°"),
    ((PL["木星2/19"]["ra"], PL["木星2/19"]["dec"]), "木星", "—", "Jupiter", "木星", "white", "2/11 上午衝日；−2.55 等"),
    ((PL["火星2/19"]["ra"], PL["火星2/19"]["dec"]), "火星（衝日）", "—", "Mars (opposition)", "火星", "red",
     "2/19 23:51 衝日；−1.28 等"),
    ([REGULUS], "軒轅十四", "—", "Regulus", "軒轅十四", "white", ""),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=56, D_r=60, D_fill=-4.0,
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

    # ── 盤上（明斯克面北）：字不跟著盤轉，dx/dy＝畫面方向（Canva 原生文字） ──
    WIDE = dict(s1=3.0, s2=2.4, gap=3.8, disc=True)      # fov 90–110：3.0×1.7×1080/100 ≈ 55 px
    MID = dict(s1=2.0, s2=1.6, gap=2.6, disc=True)       # fov 60–80
    NEAR = dict(s1=1.3, s2=1.05, gap=1.7, disc=True)     # fov 40
    LB_VOZ = term("Voz", **WIDE) + term("Maly voz", **WIDE)
    LB_NAIL = term("Hvozdz", **NEAR)
    LB_NAIL_X = (term("Altan gadas", s1=0.95, s2=0.85, gap=1.3, disc=True)
                 + term("Boahjenásti", s1=0.95, s2=0.85, gap=1.3, disc=True, zh="撐住天空的星"))
    LB_FIRE = term("Illioŭ voz", **MID)
    LB_CARTX = (term("Karlvagn", **MID, zh="男人的車（北歐）") + term("Carul Mare", **MID, zh="大車（羅馬尼亞）")
                + term("斗為帝車", **MID, zh="天帝的車（《史記》）"))
    LB_ZMIEJ = term("Zmiej", **WIDE, zh="聖喬治殺的蛇")
    LB_ZW = (term("紫微左垣", zh_only=True, s1=2.4, disc=True, a=ZW_L[:4])
             + term("紫微右垣", zh_only=True, s1=2.4, disc=True, a=ZW_R[:3]))
    LB_ZW_END = [item(centroid(SHARED7, S), "紫微垣", "amber", 3.2, 0.0, 0.0, "紫微垣")]
    for it in LB_ZW_END:
        it["disc"] = True
    # ── 長圖 ──
    LB_MOW = term("Kastsy", s1=1.3, s2=1.0, gap=1.8)
    LB_RAKE = term("Hrabli", s1=1.1, s2=0.9, gap=1.5)
    LB_PS = (term("Rataj", s1=1.6, s2=1.25, gap=2.4) + term("Sita", s1=1.6, s2=1.25, gap=2.4)
             + [item(COMA, "Stellarium 標在后髮座", "white", 0.95, 0.0, 0.0, "Sita-註")])
    LB_YARD = (term("Kurki", s1=1.8, s2=1.4, gap=2.6) + term("Vuzhy", s1=1.8, s2=1.4, gap=2.6)
               + term("Kaza", s1=1.8, s2=1.4, gap=2.6) + term("Baran", s1=1.8, s2=1.4, gap=2.6))
    LB_THRONE = term("Kreselca Pana Jezusa", s1=1.7, s2=1.4, gap=2.6)
    LB_TWINS = term("Blizniuki", s1=1.3, s2=1.0, gap=1.9) + term("波蘭和立陶宛", zh_only=True, s1=1.4)
    LB_SKY = (term("月亮 2/19", zh_only=True, s1=1.9, zh="月亮 2/19") + term("木星", zh_only=True, s1=1.9)
              + term("火星（衝日）", zh_only=True, s1=1.9, zh="火星") + term("軒轅十四", zh_only=True, s1=1.5)
              + term("月亮 2/20 元宵", zh_only=True, s1=1.7, zh="元宵的月亮"))

    label_sets = [(LB_VOZ, "Voz與Maly voz"), (LB_NAIL, "Hvozdz釘子"), (LB_NAIL_X, "北極星-跨文化"),
                  (LB_FIRE, "Illioŭ voz"), (LB_CARTX, "跨文化-北斗是車"),
                  (LB_MOW, "Kastsy"), (LB_RAKE, "Hrabli"), (LB_PS, "Rataj與Sita"), (LB_YARD, "院子"),
                  (LB_THRONE, "耶穌的椅子"), (LB_ZMIEJ, "Zmiej"), (LB_ZW, "紫微左右垣"), (LB_ZW_END, "紫微垣"),
                  (LB_TWINS, "雙胞胎"), (LB_SKY, "這幾天")]

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

    R20, R22 = ROT["20:00"], ROT["22:00"]
    HZ = m.k * PHI_M                                  # 明斯克北點在盤心下方 kφ
    CARTS = DIPPER + UMI
    F01a = fit(CARTS, R20, pad=0.10, extra=[(0, -HZ - 12)], dx=2.0)
    F01b = fit(CARTS, R20, pad=0.04, extra=[(0, -HZ + 2)])
    F03 = (0.0, round(yp - 4.0, 2), 40.0, R20)        # 推近北極星（小熊在畫面上半）
    F04a = fit(CARTS, R20, pad=0.06, extra=[(0, -HZ - 6)])
    F04b = fit(CARTS, R22, pad=0.06, extra=[(0, -HZ - 6)])
    F05 = fit(DIPPER, R22, pad=0.18, minfov=60.0)
    F08 = (F05[0], F05[1], 68.0, R22)                  # 08：只拉遠一點，跨文化三行留在北斗左邊
    HAND = (0.0, yp, 48.0, 0.0)                       # 盤⇄長圖同框換組（盤緣圈內，逐點重合）
    R14 = R20
    F14a = fit(DRACO + ZW_L[:4] + ZW_R[:3], R14, pad=0.10)
    F14b = fit(DRACO + ZW_L[:4] + ZW_R[:3], R14, pad=0.04)
    ZW_IN = [h for h in ZW_L + ZW_R if S[h][1] > 55.0]
    F18 = fit(ZW_IN + [POLARIS], R20, pad=0.06, minfov=70.0)
    F18 = (round(F18[0] + F18[2] / 6.0, 2), F18[1], F18[2], R20)   # 紫微垣放左半，右半留給端卡

    # 長圖（lst 180）
    def sfit(hips, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, extra=()):
        pts = [(x_of(S[h][0]), S[h][1]) for h in hips] + list(extra)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        lim = m.Ds - f * 8 / 9 - 0.5                 # S：|cy|+fov·8/9 ≤ D_s
        cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    DOWN = (0.0, 12.0, 48.0, 0.0)                     # 沿走廊下來（|x| ≤ 26 才有內容）
    F09 = sfit(BELT + RAKE + [26727], pad=0.25, minfov=30.0, dy=-1.0)
    F10 = sfit(BELT + RAKE + ORION, pad=0.10, minfov=60.0)
    F11 = sfit(BOO + COMA, pad=0.10, minfov=40.0)
    F12a = sfit(PLEIADES + HYADES + [CAPELLA], pad=0.06, minfov=40.0)
    F12b = sfit(ARIES + PLEIADES[:2], pad=0.10, minfov=40.0)
    F13 = sfit(ORION, pad=0.20, minfov=40.0)
    F15 = sfit([CASTOR, POLLUX] + [h for s in SEG_TWINS for h in s], pad=0.08, minfov=30.0)
    F17a = sfit(BELT + [27989, 24436], pad=0.30, minfov=40.0)
    SKY = [(x_of(PL[k]["ra"]), PL[k]["dec"]) for k in ("月亮2/19", "月亮2/20", "木星2/19", "火星2/19")]
    F17b = sfit([REGULUS], pad=0.14, minfov=40.0, extra=SKY)
    F_SW = min(F13[2], F14a[2], 50.0)                # 13→14 換組格的 fov（＝gen_canva_pages 的 f_sw）
    ORIGIN15 = (0.0, 0.0, F_SW, 0.0)                  # 15 起格＝「北盤轉長圖-下移」那一格
    print(f"\n── 構圖 ──\n  01 {F01a}→{F01b}\n  03 {F03}\n  04 {F04a}→{F04b}\n  05 {F05}\n  08 {F08}\n"
          f"  09 {F09}\n  10 {F10}\n  11 {F11}\n  12 {F12a}→{F12b}\n  13 {F13}\n  14 {F14a}→{F14b}\n"
          f"  15 {F15}\n  17 {F17a}→{F17b}\n  18 {F18}")

    # ── 標籤畫面方向偏移（依各鏡實際方位；看過 SB-鏡頭牆後調） ──
    def shift(items, key, dx, dy):
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

    # 盤：dx/dy＝畫面方向（字不跟著盤轉）；長圖：畫布方向（東在左）
    shift(LB_VOZ, "Voz", -12.0, -6.0); shift(LB_VOZ, "Maly voz", 0.0, 7.0)   # 04 迄格：斗柄左下、小車上方
    shift(LB_NAIL, "Hvozdz", 6.5, 1.0)                                        # 03 迄格：北極星右邊
    shift(LB_NAIL_X, "Altan gadas", -7.5, 2.5); shift(LB_NAIL_X, "Boahjenásti", -7.5, -2.5)   # 左邊兩行一疊
    shift(LB_FIRE, "Illioŭ voz", -11.0, -2.0)                                 # 斗柄左邊的空天區
    for i, k in enumerate(["Karlvagn", "Carul Mare", "斗為帝車"]):
        shift(LB_CARTX, k, -17.0, 6.0 - i * 6.0)                               # 08：整疊推到北斗左邊
    shift(LB_MOW, "Kastsy", 6.5, 1.5); shift(LB_RAKE, "Hrabli", 5.5, -1.5)    # 放到腰帶／耙子西側（右）
    shift(LB_PS, "Rataj", -8.5, -8.0); shift(LB_PS, "Sita", 0.0, 6.0); shift(LB_PS, "Sita-註", 1.5, -8.5)
    shift(LB_YARD, "Kaza", 0.0, -4.0); shift(LB_YARD, "Vuzhy", 0.0, -6.0)
    shift(LB_YARD, "Kurki", 0.0, 3.0); shift(LB_YARD, "Baran", 0.0, 4.0)
    shift(LB_THRONE, "Kreselca Pana Jezusa", 0.0, -14.0)                       # 獵戶下方
    shift(LB_ZMIEJ, "Zmiej", 0.0, 10.0)                                        # U 形裡面的空處
    shift(LB_ZW, "紫微左垣", 0.0, -4.0); shift(LB_ZW, "紫微右垣", -7.0, 0.0)   # 離開琥珀虛線
    shift(LB_TWINS, "Blizniuki", 0.0, -4.0); shift(LB_TWINS, "波蘭和立陶宛", 4.5, 3.5)
    shift(LB_SKY, "月亮 2/19", 0.0, 2.8); shift(LB_SKY, "木星", 0.0, 2.4)
    shift(LB_SKY, "火星（衝日）", -3.5, 1.6); shift(LB_SKY, "軒轅十四", 0.0, -2.8)
    shift(LB_SKY, "月亮 2/20 元宵", 8.5, -1.0)
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
    MARKS = [(MAINS, "主角星白點", "dot"), ([POLARIS, CAPELLA], "單星光暈", "ring"),
             (SHARED7, "共用七星圈", "ring")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    HZ_M = [PHI_M]
    shots = [
        dict(code="01", kind="R", sec=10, north=True, horizon=HZ_M,
             frames=[F01a, F01b], layers=["車", "小", "暈"], labels=[],
             vo="上週，薩米人說北極星撐著整片天空。今晚往南到白俄羅斯：同一片星空，白俄羅斯的農民看見——一本農民曆。",
             card="白俄羅斯：一本農民曆",
             note=f"北盤（明斯克 53.9°N，2/19 20:00 面北，rot {R20:+.1f}°；山＝明斯克北方地平線）緩慢推近；"
                  "北極星光暈＋Voz（琥珀）、Maly voz（綠）淡入；開場字卡"),
        dict(code="02", kind="R", sec=12, north=True, horizon=HZ_M,
             frames=[F01b], layers=["車", "小", "暈"], labels=[],
             overlay="C-A22-01_白俄羅斯在哪", overlay_layers=["地圖層", "森林湖泊層"],
             vo="白俄羅斯在東歐內陸，沒有海，四成是森林，還有上千座湖。研究者發現，到了二十一世紀，村裡的老人還叫得出星星的名字。",
             card="村裡老人還叫得出星名",
             note="北盤定格；疊 C-A22-01（自繪示意輪廓：內陸國、森林、湖；不是精確國界）"),
        dict(code="03", kind="R", sec=10, north=True, horizon=HZ_M,
             frames=[F01b, F03], layers=["小", "暈"], labels=ls("Hvozdz釘子"),
             labels_end=ls("Hvozdz釘子", "北極星-跨文化"),
             vo="先往北看。北極星叫 Hvozdz——釘子，整片天空就繞著這根釘子轉。蒙古人也說它是一根金樁。",
             card="北極星＝釘子 Hvozdz",
             note="推近北極星（fov 40）；北極星細圈＝單星光暈層；迄格小標：蒙古 Altan gadas 金樁（A-07）、"
                  "薩米 Boahjenásti（A-21，只放小標）"),
        dict(code="04", kind="R", sec=11, north=True, horizon=HZ_M,
             frames=[F03, F04a, F04b], layers=["車", "小", "暈"], labels=ls("Voz與Maly voz"), labels_start=ls("Hvozdz釘子", "北極星-跨文化"),
             vo="繞著釘子轉的，是一輛車：北斗七星叫 Voz，大車；小熊座是 Maly voz，小車。冬天的節日 Kaliady，傳說就是坐著這輛大車來的。",
             card="北斗＝大車 Voz",
             note=f"拉遠到兩輛車；逆時針旋轉（明斯克 20:00→22:00，{R20:+.1f}°→{R22:+.1f}°；v1 寫 18:00→20:00，"
                  "18:00 明斯克天還亮，改）；Voz（琥珀）、Maly voz（綠）"),
        dict(code="05", kind="R", sec=13, north=True, horizon=HZ_M,
             frames=[F04b, F05], layers=["車"], labels=ls("Voz與Maly voz"),
             overlay="C-A22-02_火車火馬", overlay_layers=["經文層"],
             vo="基督教傳進來以後，這輛車有了主人：先知以利亞。聖經說他沒有死——「忽有火車火馬將二人隔開，以利亞就乘旋風升天去了」。",
             card="火車火馬：火焰的車與馬",
             note="推近北斗 fov 60；迄格定格疊 C-A22-02（列王紀下 2:11 經文卡；不放聖像畫，美宣要用另尋授權）"),
        dict(code="06", kind="R", sec=12, north=True, horizon=HZ_M,
             frames=[F05], layers=["火"], labels=ls("Illioŭ voz"),
             overlay="C-A22-03_雷聲車輪", overlay_layers=["車輪層", "閃電層"],
             vo="所以北斗又叫 Illioŭ voz，以利亞的車——一輛火焰馬車。東斯拉夫民間說，夏天打雷，就是他駕著車在天上跑，閃電是他在追打魔鬼。",
             card="以利亞的火焰馬車",
             note="畫面不動；北斗連線琥珀→紅（連線-以利亞的車）；疊 C-A22-03（簡筆：車輪＝雷聲、閃電）"),
        dict(code="07", kind="R", sec=10, north=True, horizon=HZ_M,
             frames=[F05], layers=["火"], labels=ls("Illioŭ voz"),
             overlay="C-A22-04_白俄羅斯農民曆", overlay_layers=["年輪層", "節日層", "星層"],
             vo="他的節日在八月初，正是雷雨多、麥子收割的時候。也有人認為，更早以前駕這輛車的，是雷神 Perun。",
             card="雷雨的節日：八月初",
             note="畫面不動；疊 C-A22-04（圓形年曆：Kaliady／Juraŭ dzień／以利亞節；「雷神 Perun」加註「一說」）"),
        dict(code="08", kind="R", sec=10, north=True,
             frames=[F05, F08, HAND], layers=["車", "小"], labels=ls("跨文化-北斗是車"), labels_end=[],
             vo="把北斗看成車的，不只白俄羅斯：北歐叫「男人的車」，羅馬尼亞叫「大車」；司馬遷也說「斗為帝車」——天帝的車。",
             card="北斗是一輛車",
             note=f"拉遠；跨文化標籤層「北斗＝車」；最後推進盤心 fov 48、轉回 0°（{R22:+.1f}°→0°，換組格；"
                  "盤心附近只有小熊在轉）"),
        dict(code="09", kind="Z", sec=11, north=True,
             frames=[HAND, DOWN, F09], layers=["割", "小"], labels=ls("Kastsy", "Hrabli"), labels_start=[],
             vo="往南看獵戶座。腰帶三顆星，一顆接一顆斜斜排開，像田裡一排割草的人，叫 Kastsy。下面那串小星，是耙草的耙子 Hrabli。",
             card="割草的人 Kastsy",
             note="【換組】盤心同框換長圖（08 迄格＝這一格）；沿走廊下來、往西（右）滑到獵戶；Kastsy（琥珀）、Hrabli（綠：柄沿獵戶的劍往下、"
                  "橫桿在劍南方 υ Ori—49 Ori；6.4–6.7 等，郊外才勉強看得到；M42 不要標成耙子）"),
        dict(code="10", kind="S", sec=9, north=True,
             frames=[F09, F10], layers=["割", "車"], labels=ls("Kastsy", "Hrabli"),
             overlay="C-A22-05_打乾草的一整套", overlay_layers=["割層", "耙層", "載層"],
             vo="我們把它們放在一起看：割草、耙草，再用北邊的大車載回家——夏天打乾草的一整套，冬天全掛在天上。",
             card="割・耙・載（本片的串連）",
             note="拉遠；迄格定格疊 C-A22-05（割→耙→載三格；標題列「本片的串連」）"),
        dict(code="11", kind="S", sec=11, north=True,
             frames=[F10, F11], layers=["犁"], labels=ls("Rataj與Sita"), labels_start=ls("Kastsy", "Hrabli"),
             vo="春天的天上還有更多農具：牧夫座是犁田的人 Rataj；后髮座那幾顆暗星是篩子 Sita——老人說，上帝曾經拿它篩黑麥。",
             card="犁田的人・篩子",
             note="長圖往左（東）滑到牧夫—后髮；Rataj（藍）、Sita（紫，α／β／γ Com 三角）；角落小字「台北 21:30 後東北東升起」"
                  "（20:00 牧夫還在地平線下）"),
        dict(code="12", kind="S", sec=10, north=True,
             frames=[F11, F12a, F12b], layers=["院", "暈"], labels=ls("院子"), labels_start=ls("Rataj與Sita"),
             vo="還有一院子的動物：昴宿是一群母雞 Kurki，畢宿是幾條草蛇，五車二是母山羊 Kaza，白羊座，就是院子裡的公羊。",
             card="母雞・草蛇・母山羊",
             note="長圖往右（西）滑：五車二 Kaza（琥珀細圈）、畢宿 Vuzhy（紅）、昴宿 Kurki（綠）同一格 → 白羊 Baran（藍）"),
        dict(code="13", kind="S", sec=11, north=True,
             frames=[F12b, F13], layers=["椅"], labels=ls("耶穌的椅子"), labels_start=ls("院子"),
             overlay="C-A22-08_荊棘冠與十字架", overlay_layers=["北冕層", "天鵝層"],
             vo="同一片天，後來也慢慢變成一座教堂：整個獵戶座是耶穌的椅子；北冕座是荊棘冠，天鵝座是聖彼得的十字架。",
             card="耶穌的椅子",
             note="長圖回獵戶；Kreselca Pana Jezusa（紫）；迄格疊 C-A22-08（北冕、天鵝兩張星圖縮圖：台北 20:00 都在地平線下）"),
        dict(code="14", kind="R", sec=12, north=True,
             frames=[F14a, F14b], layers=["蛇", "紫", "圈"], labels=ls("Zmiej"), labels_end=ls("Zmiej", "紫微左右垣"),
             vo="天龍座，是聖喬治殺死的那條蛇，被他掛在那顆「永遠不動的星」旁邊——巧的是，這條蛇的身體，正好疊在中國紫微垣的城牆上。",
             card="聖喬治的蛇＝紫微垣的牆",
             note=f"【換組】長圖→北盤（自動插回中心／上移／長圖轉北盤）；轉到明斯克 20:00（{R14:+.1f}°）；"
                  "Zmiej（紅）＋紫微左右垣（琥珀虛線）；共用 7 顆（共用七星圈）閃一次；左樞—右樞是宮門、虛線不連"),
        dict(code="15", kind="S", sec=9, north=True,
             frames=[ORIGIN15, F15], layers=["雙"], labels=ls("雙胞胎"), labels_start=[],
             vo="雙子座的兩顆亮星，代表幾百年前的兩個國家：波蘭和立陶宛——白俄羅斯這塊地，就在立陶宛那一邊。",
             card="波蘭和立陶宛",
             note="【換組】北盤→長圖（自動插歸位／北盤轉長圖／下移）；滑到雙子：Blizniuki（淡藍）＋北河二—北河三（琥珀）；"
                  "標籤不分哪顆是哪國"),
        dict(code="16", kind="S", sec=6, north=True,
             frames=[F15], layers=["雙"], labels=ls("雙胞胎"),
             overlay="C-A22-06_白俄羅斯星名小辭典",
             vo="這集的白俄羅斯星名，整理成一張小辭典，可以存起來。",
             card="白俄羅斯星名小辭典",
             note="畫面不動；疊 9:16 圖卡 C-A22-06（可存圖）"),
        dict(code="17", kind="S", sec=15, north=True,
             frames=[F15, F17a, F17b], layers=["割", "行", "月19"], labels=ls("這幾天"), labels_start=ls("Kastsy"),
             overlay="C-A22-07_這幾天抬頭看",
             vo="這幾天在台灣：天一黑，割草的人就在南方高空；九點以後，北斗從東北方爬上來。今晚東方，月亮下面是木星和衝日的火星；明晚元宵，月亮就停在它們中間。",
             card="這幾天抬頭看",
             note="長圖：腰帶（琥珀）→往左滑到獅子座：月亮（2/19 20:00）、木星、火星、軒轅十四；"
                  "「明晚元宵」時把月亮-2月19日層換成月亮-2月20日層（同框）；最後 4 秒疊 9:16 圖卡 C-A22-07"),
        dict(code="18", kind="R", sec=11, north=True,
             frames=[F18], layers=["紫"], labels=ls("紫微垣"),
             vo="明天元宵，我們就去看這座紫微垣，和元宵拜的天官；下週五去羅馬尼亞：天上有牧羊人、看羊的大狗，還有一口井。",
             card="下集見｜2/20 元宵：天官賜福與紫微大帝｜2/26 羅馬尼亞：牧羊人的星空農場",
             note="【換組】長圖→北盤；紫微垣（琥珀虛線）放左半、右半端卡；追蹤 CTA"),
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

    print("  北盤旋轉角（明斯克 2/19，面向北方）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print("  天體（台北，J2000）：" + "、".join(f"{k} RA {v['ra']:.1f} Dec {v['dec']:+.1f} 高 {v['alt']}°"
                                          for k, v in PL.items() if "2/19" in k or k == "月亮2/20"))
    print(f"  x：腰帶 {x_of(S[26311][0]):+.1f}、五車二 {x_of(S[CAPELLA][0]):+.1f}、昴宿 {x_of(S[17702][0]):+.1f}、"
          f"白羊 {x_of(S[9884][0]):+.1f}、北河三 {x_of(S[POLLUX][0]):+.1f}、軒轅十四 {x_of(S[REGULUS][0]):+.1f}、"
          f"大角 {x_of(S[ARCTURUS][0]):+.1f}；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if not isinstance(hips, tuple) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_minsk": ROT, "lst0": LST0, "phi": PHI_M, "bodies": PL},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV_LINES = LG_ALL
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=PREV_LINES,
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
