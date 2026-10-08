# -*- coding: utf-8 -*-
"""A-14 因紐特：極夜裡的星鐘｜大畫布 v4.6

論點：北緯 69° 的 Igloolik，太陽 11 月底沉下去、一個半月後才回來（Tauvikjuaq 大黑暗）。
沒有太陽、沒有時鐘，獵人從冰屋的小洞看星星報時（qausiut「天亮的指標」）：
北極星 Nuutuittuq 高得幾乎在頭頂、魚叉對準它一整夜不動；北斗＝馴鹿 Tukturjuit，
半夜用後腳站起來；御夫＋雙子兩對亮星＝鎖骨 Quturjuuk，傍晚斜一邊、後半夜擺平、天快亮斜另一邊；
仙后座＝燈架／海豹油袋。最重要的是 Aagjuuk（牛郎星＋河鼓三）：十二月第二週第一次在東北方
黎明露臉＝報曉的鬧鐘，也＝冬至的日曆（1990/12/19 社區廣播）。阿拉斯加叫它「兩道陽光」，
往南走卻常常是扁擔（中國牛郎、阿努塔、羅馬尼亞）。長夜裡的故事：腰帶＝奔跑的人 Ullaktut
追北極熊（畢宿五）與狗群（畢宿），掉手套的那位＝參宿七；天狼星在這裡最高 4°，閃個不停
（Singuuriq），跟著它走的人沒回來、跟著織女星的人回到岸邊。太陽回來：吹熄油燈、從同一把
新火點亮、半邊臉笑。「明天」＝qauppat「如果天亮的話」。

來源：John MacDonald《The Arctic Sky: Inuit Astronomy, Star Lore, and Legend》（1998，
Royal Ontario Museum／Nunavut Research Institute；Igloolik 長老口述，頁碼見逐字稿）；
Stellarium inuit（Karrie Berglund 據 MacDonald 改編；新舊兩版 index.json 相同 11＋3 個）；
跨文化：Stellarium chinese／anutan／romanian；PyEphem 自算（Igloolik 69.37°N 81.80°W，UTC−5）。

拼字：片中一律用 MacDonald 的 Igloolik 拼法（Stellarium 另有 Akkuttujuuk、Qimmiitt、
Uqsuutaattiaq、Nuuttuittuq、Sikuliaqsiujuittuq 等寫法）。

鏡頭路線：Igloolik 北方地平線（北盤＋山＝地平線，傍晚 16:00 起）→ 極夜（概念圖）→ 冰屋的小洞
→ 北極星＋魚叉 → 盤逆時針轉一整夜：馴鹿站起來（＋狼群）→ 鎖骨傾斜（概念圖）→ 魚叉還指著它
→ 仙后座（家當）→ 盤轉回 0° 同框換長圖 → 沿走廊往下到 Aagjuuk（T）→ 初見（概念圖）→ 鬧鐘
→ 日曆 → 跨文化（扁擔）→【硬切】獵戶：奔跑的人追北極熊 → 掉手套（參宿七）→ 往下到天狼星
→ 星名小辭典（圖卡）→ 太陽回來（概念圖）→ qauppat → 這週末（圖卡）→ 下集預告。

參數
  lst = 300 → 走廊（x=0）＝RA 300：Aagjuuk（牛郎 x +2.3、河鼓三 +3.4）就在走廊上，
             從北極星沿走廊往下會經過天津四（x −10）、織女星（x +21）。
             獵戶在 x −139…−149、畢宿五 −129、昴宿 −117、天狼 −161（接縫 x=±180 在 RA 120，
             北河三 −176、南河三 −175 貼著接縫：本集長圖不標它們）。
             北盤旋轉角＝lst − Igloolik 地方恆星時 − 180（北盤面向北方）：
             12/18 16:00 +159.3°、18:00 +129.2°、20:00 +99.1°、00:00 +39.0°、06:00 −51.3°——
             整夜都在 ±180° 之內，每一步逆時針（時間往前），Canva 不會繞反方向。
  D_s = 45、D_r = 49 → 北斗最南 Alkaid +49.31 在北盤本體；織女 +38.8 在帶內。
  D_fill = −25 → k=1.397、R_fill=160.71（盤寬 ÷ 畫布寬 ＝ 0.892822）：Igloolik 的南方地平線
             在 dec −20.6，整片 Igloolik 天空都在盤裡；面北的 R 鏡頭 fov 140 才放得進
             「北方地平線＋頭頂」（角落 155.1 < 160.2）。|x_t|＋R_fill ＝ 160.7 ≤ 180 ✓
  x_tN = x_tS = 0
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-14"
OUT = os.path.join(BASE, "05_素材/A-14_因紐特/_v4大畫布")
LST0 = 300.0
IGL = (69.3667, -81.8)          # Igloolik 69°22'N 81°48'W，EST（UTC−5）
PHI = 69.37                     # 面北 R 鏡頭的地平線緯度
TPE = (25.0330, 121.5654)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）：Igloolik 的地方恆星時 → 北盤旋轉角
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


def rot_at(when):
    """北盤面向北方：盤心正下方＝下中天（lst_obs＝lst_view−180）；Canva 正角＝順時針。
    rot＝lst − lst_obs − 180，收在 (−180, 180]。"""
    L = lst_at(*IGL, -5, when)
    return round((LST0 - L - 180.0 + 180.0) % 360.0 - 180.0, 2)


T_IGL = {"16:00": "2026/12/18 16:00", "18:00": "2026/12/18 18:00", "20:00": "2026/12/18 20:00",
         "22:00": "2026/12/18 22:00", "00:00": "2026/12/19 00:00", "03:00": "2026/12/19 03:00",
         "06:00": "2026/12/19 06:00"}
ROT = {k: rot_at(v) for k, v in T_IGL.items()}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALTAIR, TARAZED, ALSHAIN, VEGA, DENEB = 97649, 97278, 98036, 91262, 102098
POLARIS, KOCHAB, PHERKAD = 11767, 72607, 75097
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
CAPELLA, MENKALINAN, CASTOR, POLLUX = 24608, 28360, 36850, 37826
CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN, ETA_CAS = 746, 3179, 4427, 6686, 8886, 3821
SEGINUS, NEKKAR, DEL_BOO = 71075, 73555, 74666
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BETELGEUSE, BELLATRIX, RIGEL, SAIPH = 27989, 25336, 24436, 27366
ALDEBARAN, ALCYONE = 21421, 17702
SIRIUS, PROCYON, ARCTURUS, MUPHRID = 32349, 37279, 69673, 67927
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
BELT = [MINTAKA, ALNILAM, ALNITAK]
CAS_W = [CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN]
MAINS = ([ALTAIR, TARAZED, POLARIS, CAPELLA, MENKALINAN, CASTOR, POLLUX, ALDEBARAN, RIGEL,
          SIRIUS, VEGA] + DIPPER + BELT + [CAPH, SCHEDAR, NAVI])


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium inuit，新版 index.json；鎖骨依 MacDonald 拆成兩對）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
IDX = json.load(open(os.path.join(SC_NEW, "inuit", "index.json"), encoding="utf-8"))
IN = {}
for c in IDX["constellations"]:
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    IN[c["common_name"]["native"]] = [s for s in segs if len(set(s)) >= 2]

SEG_AAG = IN["Aagjuuk"]                              # 牛郎＋河鼓三
SEG_TUK = IN["Tukturjuit"]                           # 北斗（含回天權那一段）
SEG_QUT = [[CAPELLA, MENKALINAN], [CASTOR, POLLUX]]  # MacDonald：兩對、各兩顆（Stellarium 連成一串）
SEG_PIT = IN["Pituaq"]                               # 仙后三顆亮星的三角＝燈架
SEG_URS = IN["Uqsuutaattiaq"]                        # 仙后 W（含 η Cas）＝海豹油袋
SEG_ULL = IN["Ullaktut"]                             # 腰帶三顆＝奔跑的人
SEG_QIM = IN["Qimmiitt"]                             # 畢宿五＋畢宿 V 字＝熊與狗群
SEG_SAK = IN["Sakiattiak"]                           # 昴宿＝胸骨（本集只在 L4 總層）
SEG_AKU = IN["Akkuttujuuk"]                          # 參宿四＋參宿五（本集只在 L4 總層）
SEG_SIV = IN["Sivulliik"]                            # 大角＋牧夫 η（本集只在 L4 總層）
SEG_WOLF = [[SEGINUS, NEKKAR, DEL_BOO]]              # Pelly Bay 的狼群 Amaruqjuit（MacDonald：牧夫 γ、β、δ「可能」）
SEG_POLE = [[TARAZED, ALTAIR, ALSHAIN]]              # 跨文化：河鼓三星＝扁擔（中國／阿努塔／羅馬尼亞）

LG_NORTH = [(SEG_TUK, "amber", 1.0), (SEG_QUT, "green", 1.0)]
LG_WOLF = [(SEG_WOLF, "red", 0.9)]
LG_LAMP = [(SEG_URS, "blue", 0.9), (SEG_PIT, "purple", 1.0)]
LG_AAG = [(SEG_AAG, "amber", 1.0)]
LG_POLE = [(SEG_POLE, "green", 0.9)]
LG_HUNT = [(SEG_ULL, "blue", 1.0), (SEG_QIM, "red", 1.0)]
LG_ALL = (LG_NORTH + LG_WOLF + LG_LAMP + LG_AAG + LG_HUNT +
          [(SEG_SAK, "purple", 0.8), (SEG_AKU, "green", 0.8), (SEG_SIV, "blue", 0.8)])
LINE_SETS = [(LG_NORTH, "連線-馴鹿與鎖骨"), (LG_WOLF, "連線-狼群"), (LG_LAMP, "連線-燈架與油袋"),
             (LG_AAG, "連線-Aagjuuk"), (LG_POLE, "連線-扁擔"), (LG_HUNT, "連線-追熊")]
LINES_KEY = {"L4": "星座連線", "北": "連線-馴鹿與鎖骨", "狼": "連線-狼群", "燈": "連線-燈架與油袋",
             "晨": "連線-Aagjuuk", "擔": "連線-扁擔", "獵": "連線-追熊"}
LINE_GROUPS = {"L4": LG_ALL, "北": LG_NORTH, "狼": LG_WOLF, "燈": LG_LAMP, "晨": LG_AAG,
               "擔": LG_POLE, "獵": LG_HUNT}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A 系列同一套算法）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōū]+", w.lower().replace("ʻ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、名詞總表（＝標籤對照表；給組員直接複製貼上）
#   (錨點 HIP 群, 原文（MacDonald 拼法）, Stellarium 拼法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ([POLARIS], "Nuutuittuq", "Nuuttuittuq", "Never Moves", "從來不動的（北極星）", "amber",
     "MacDonald p.59–62：在 Igloolik 快 70° 高、幾乎在頭頂，太高不好定方向；Ulayuruluk 的魚叉實驗（IE-211）"),
    (DIPPER, "Tukturjuit", "Tukturjuit", "Caribou", "馴鹿（北斗）", "amber",
     "MacDonald p.80–82、200：時鐘；Iqqaqsaq「快到半夜，馴鹿用後腳站起來，頭愈抬愈高」（IE-257）"),
    ([SEGINUS, NEKKAR, DEL_BOO], "Amaruqjuit", "—", "Wolves", "狼群（Pelly Bay）", "red",
     "MacDonald p.82：Pelly Bay 的 Quttiutuqu 夫婦：追馴鹿的三匹狼；Paatsi Qaggutaq 指認為牧夫座（可能是 γ、β、δ）"),
    ([CAPELLA, MENKALINAN, CASTOR, POLLUX], "Quturjuuk", "Quturjuuk", "Collarbones", "鎖骨（御夫＋雙子）", "green",
     "MacDonald p.65–67、200：兩對各兩顆；Amaaq「傍晚斜向左、後來擺平、天快亮斜向右」（IE-073）"),
    ([SCHEDAR, CAPH, NAVI], "Pituaq", "Pituaq", "Lamp Stand", "燈架（仙后三顆亮星）", "purple",
     "MacDonald p.62–63：放海豹油燈 qulliq 的三根立柱"),
    ([CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN, ETA_CAS], "Ursuutaattiaq", "Uqsuutaattiaq",
     "Seal-skin Oil Container", "海豹油袋（仙后 W）", "blue",
     "MacDonald p.88–89：另一派長老把整個 W 叫這個名字（和 Pituaq 是兩種分法）"),
    ([ALTAIR, TARAZED], "Aagjuuk", "Aagjuuk", "(Two Sunbeams)", "牛郎星＋河鼓三", "amber",
     "MacDonald p.44–51：最重要的星座；十二月第二週首次在東北方黎明出現；aagjuliqtuq＝一天開始；"
     "1990/12/19 Jacobie Avingnaq 社區廣播宣布冬至；Stellarium 英文名取自阿拉斯加 Noatak 傳說"),
    ([VEGA], "Kingullialuk", "Kingulliq", "The (Big) One Behind", "後面那顆大的（織女星）", "white",
     "MacDonald p.55、75：漂流海冰的故事，跟著它的人回到岸冰"),
    (BELT, "Ullaktut", "Ullaktut", "Runners", "奔跑的人（腰帶）", "blue",
     "MacDonald p.226–228：追北極熊上了天；掉手套的第四人"),
    ([ALDEBARAN], "Nanurjuk", "—", "Spirit of a Polar Bear", "北極熊（畢宿五）", "red",
     "MacDonald p.57–58：「像北極熊的／有北極熊之靈的」；有些長老說是昴宿六"),
    ([20894, 20205, 20455, 20889], "Qimmiit", "Qimmiitt", "Dogs", "狗群（畢宿）", "red",
     "MacDonald p.58：熊是畢宿五時，狗群＝畢宿星團"),
    ([RIGEL], "Kingulliq", "—", "The One Behind", "落在後面的（參宿七）", "white",
     "MacDonald p.56、226：回頭撿手套、落在三兄弟後面的獵人（Aqatsiaq 版）"),
    ([SIRIUS], "Singuuriq", "—", "Flickering", "閃個不停的（天狼星）", "white",
     "MacDonald p.73–75：Igloolik 最高約 4°、只出來 5 個多小時；跟著它走的人沒回來"),
]
CROSS = [("Two Sunbeams", "兩道陽光（阿拉斯加 Noatak 傳說）"),
         ("Peggittyn", "帶來新年的光（楚科奇）"),
         ("河鼓", "牛郎挑著兩個孩子（中國）"),
         ("Te Aamonga", "扁擔（阿努塔）"),
         ("Fata de împărat", "挑擔的公主（羅馬尼亞）")]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-25,
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
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True               # 帶內星（dec<49）也進北盤標籤（R 鏡頭要看得到）
        return it

    def pair(a, orig, zh, color, dx, dy, key, disc=False, s1=1.5, s2=1.1, gap=2.3):
        """原文在上、中文在下（同一錨點）"""
        return [item(a, orig, color, s1, dx, dy + gap / 2, key, disc),
                item(a, zh, "white", s2, dx, dy - gap / 2, key + "-zh", disc)]

    T = {t[1]: t for t in TERMS}

    def term(name, dx, dy, disc=False, s1=1.5, s2=1.1, gap=2.3):
        a, orig, _, _, zh, col, _ = T[name]
        return pair(a, orig, zh, col, dx, dy, name, disc, s1, s2, gap)

    # ── 北天（R 鏡頭，fov 140）：盤上的字不跟著轉，dx/dy 是畫面方向；字級 4.4／3.6 ≈ Canva 43／36 px ──
    LB_POLE = term("Nuutuittuq", 0.0, -8.0, s1=4.4, s2=3.6, gap=4.6)
    # 北斗整夜在轉，字放哪一邊要看時刻（逐頁算過不壓線、不碰山稜）
    LB_TUK_U = term("Tukturjuit", -14.0, 11.0, s1=4.4, s2=3.6, gap=4.6)     # 20:00：斗柄上方
    LB_TUK_L = term("Tukturjuit", -24.0, 1.5, s1=4.4, s2=3.6, gap=4.6)     # 22:00、00:00：北斗左邊
    LB_TUK_D = term("Tukturjuit", 0.0, -13.0, s1=4.4, s2=3.6, gap=4.6)     # 06:00：北斗下方
    LB_WOLF = term("Amaruqjuit", 0.0, -9.0, True, s1=3.9, s2=3.4, gap=4.3)
    LB_QUT = term("Quturjuuk", 0.0, 0.0, True, s1=4.4, s2=3.6, gap=4.6)
    LB_CAS = term("Pituaq", 0.0, -6.5, s1=1.9, s2=1.4) + term("Ursuutaattiaq", 10.0, 7.0, s1=1.9, s2=1.4)
    # ── 長圖 ──
    LB_AAG = term("Aagjuuk", -9.0, 2.5, s1=1.6, s2=1.15)
    LB_VEGA = term("Kingullialuk", 0.0, -3.4, s1=1.4, s2=1.0)
    LB_CROSS = []
    for i, (orig, zh) in enumerate(CROSS):
        y0 = 10.0 - 4.4 * i
        LB_CROSS.append(item([ALTAIR], orig, "green", 1.2, 15.0, y0 + 1.0, f"跨-{i}"))
        LB_CROSS.append(item([ALTAIR], zh, "white", 0.95, 15.0, y0 - 1.2, f"跨-{i}-zh"))
    LB_HUNT = (term("Ullaktut", 0.0, -4.0, s1=1.5, s2=1.1) + term("Nanurjuk", 0.0, 4.2, s1=1.5, s2=1.1)
               + term("Qimmiit", 0.0, -5.5, s1=1.3, s2=1.0))
    LB_RIGEL = term("Kingulliq", 0.0, -3.6, s1=1.4, s2=1.05)
    LB_SIR = term("Singuuriq", 2.5, -3.8, s1=1.6, s2=1.15)

    label_sets = [(LB_POLE, "北極星"), (LB_TUK_U, "馴鹿-上"), (LB_TUK_L, "馴鹿-左"), (LB_TUK_D, "馴鹿-下"),
                  (LB_WOLF, "狼群"), (LB_QUT, "鎖骨"), (LB_CAS, "家當"),
                  (LB_AAG, "Aagjuuk"), (LB_VEGA, "織女星"), (LB_CROSS, "跨文化-扁擔"),
                  (LB_HUNT, "追熊"), (LB_RIGEL, "參宿七"), (LB_SIR, "天狼星")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    m.L_marks(MAINS, "主角星白點", "dot")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot")])

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole

    def P(h):
        return m.pos_primary(*S[h][:2])

    def disc_on(hips, rot, fov, dy=0.0):
        """北盤上讓 hips 的質心落在畫面中心（rot＝Canva 旋轉角）"""
        ra, dec = centroid(hips, S)
        q = m.to_disc_local(m.p_disc(m.xw(ra), dec, True), True)
        a = math.radians(-rot)
        x, y = q[0] * math.cos(a) - q[1] * math.sin(a), q[0] * math.sin(a) + q[1] * math.cos(a)
        return (round(x, 2), round(yp + y + dy, 2), fov, rot)

    def FN(t):                                   # Igloolik 面北：地平線北點約在畫面 Y≈1600
        return (0.0, round(yp - 14.0, 2), 140.0, ROT[t])

    HAND = (0.0, yp, 48.0, 0.0)                  # 北盤⇄長圖同框換組（盤心置中、旋轉 0）
    CAS = disc_on(CAS_W, ROT["06:00"], 46.0)
    AAG0 = (0.0, 16.0, 48.0, 0.0)
    AAG1 = (2.0, 12.0, 36.0, 0.0)
    AAG2 = (2.5, 11.0, 30.0, 0.0)
    AAG3 = (2.5, 10.5, 27.0, 0.0)
    AAGX = (10.0, 9.0, 44.0, 0.0)                # 跨文化：右邊（西）留給名稱表
    ORI1 = (-133.0, 7.5, 42.0, 0.0)              # 獵戶＋畢宿＋昴宿
    ORI2 = (-136.0, 4.0, 34.0, 0.0)
    ORI3 = (-140.0, 0.0, 32.0, 0.0)              # 參宿七入鏡
    SIR = (-152.0, -8.0, 36.0, 0.0)
    WIDE = (-140.0, 0.0, 48.0, 0.0)
    END = (-143.0, -1.0, 30.0, 0.0)

    def ls(*names):
        return list(names)

    HZ = [PHI]
    shots = [
        dict(code="01", kind="R", sec=12, north=True, horizon=HZ,
             frames=[FN("16:00"), FN("18:00")], layers=["北"], labels=[],
             vo="上週在沙漠，星星是日曆。今晚往北，進北極圈，到加拿大的 Igloolik："
                "同一片星空，因紐特人拿它——在極夜裡讀時間。",
             card="同一片星空，因紐特人拿它——在極夜裡讀時間。",
             note=f"開場字卡；Igloolik 面北（山＝北方地平線），盤逆時針 16:00→18:00（{ROT['16:00']:+.1f}°→{ROT['18:00']:+.1f}°）"),
        dict(code="02", kind="R", sec=19, north=True, horizon=HZ,
             frames=[FN("18:00")], layers=["北"], labels=[],
             overlay="C-A14-01_極夜", overlay_layers=["地平層", "台北層", "Igloolik層", "極夜層"],
             vo="Igloolik 在北緯六十九度。十一月底，太陽一沉下去就不再升起，要等一個半月、到一月中才回來。"
                "冬至中午，台北的太陽有四十一度高；在這裡，它還躲在地平線下快三度。"
                "這段日子叫 Tauvikjuaq：大黑暗。",
             note="畫面停在 18:00；定格疊概念圖 C-A14-01 極夜（地平 → 台北 → Igloolik → 極夜日曆）"),
        dict(code="03", kind="R", sec=13, north=True, horizon=HZ,
             frames=[FN("18:00"), FN("20:00")], layers=["北"], labels=[],
             vo="沒有太陽，也沒有時鐘，什麼時候該起床、出門打獵？獵人會在冰屋上留個小洞，從裡面看星星。"
                "這些報時的星，叫 qausiut——「天亮的指標」。",
             note=f"盤逆時針 18:00→20:00（{ROT['20:00']:+.1f}°）"),
        dict(code="04", kind="R", sec=18, north=True, horizon=HZ,
             frames=[FN("20:00"), FN("20:00")], layers=["北"], labels=ls("北極星"),
             vo="先看北極星：Nuutuittuq，「從來不動的那顆」。在這裡它快七十度高，幾乎在頭頂，"
                "太高了，反而不好拿來認方向。有位長老回憶：他第一次聽說這顆星很好奇，"
                "晚上就把一支魚叉對準它，架在擋風的雪牆邊。",
             note="盤不動；迄格（唸到「魚叉」）疊上魚叉（C-A14-魚叉_透明.png，滿版，對準盤心＝北極星），一直留到 06 迄格"),
        dict(code="05", kind="R", sec=15, north=True, horizon=HZ,
             frames=[FN("20:00"), FN("22:00"), FN("00:00")], layers=["北", "狼"],
             labels=ls("馴鹿-左"), labels_start=ls("北極星", "馴鹿-上"),   # 起格＝04 迄格：北極星的字留著
             vo="天空開始轉。北斗七星叫 Tukturjuit，馴鹿，是時鐘的指針。老獵人說："
                "「快到半夜，馴鹿會用後腳站起來，頭愈抬愈高。」在更西邊的 Pelly Bay，牠後面還追著三匹狼。",
             note=f"盤逆時針 20:00→22:00→00:00（{ROT['22:00']:+.1f}°、{ROT['00:00']:+.1f}°）；魚叉不動"),
        dict(code="06", kind="R", sec=17, north=True, horizon=HZ,
             frames=[FN("00:00"), FN("03:00"), FN("06:00")], layers=["北"], labels=ls("鎖骨"),
             labels_start=ls("馴鹿-左", "狼群", "鎖骨"),   # 起格＝05 迄格（00:00）：旁白剛唸到狼群，狼群這時才離開山稜
             labels_end=ls("馴鹿-下"),                   # 06:00：唸到「馴鹿整個換了位置」；鎖骨這時貼著左緣
             overlay="C-A14-02_星鐘", overlay_layers=["傍晚層", "後半夜層", "清晨層"],
             vo="再看御夫和雙子的兩對亮星：Quturjuuk，一對鎖骨。傍晚它斜向一邊，後半夜擺平，"
                "天快亮時，又斜向另一邊。早上他去看：馴鹿整個換了位置——魚叉，還指著那顆星。",
             note=f"盤逆時針 00:00→03:00→06:00（{ROT['03:00']:+.1f}°、{ROT['06:00']:+.1f}°）；"
                  "迄格魚叉還指著北極星；之後定格疊概念圖 C-A14-02 星鐘（三層，鎖骨在地平線上的傾斜）"),
        dict(code="07", kind="R", sec=13, north=True,
             frames=[FN("06:00"), CAS, HAND], layers=["燈"], labels=ls("家當"),
             vo="北極星的另一邊是仙后座：有人說三顆亮星是油燈的燈架 Pituaq，也有人說整個 W 是裝海豹油的皮袋。"
                "天上掛的，都是冰屋裡的家當。",
             note="推近仙后座（燈架紫、油袋藍）→ 盤轉回 0° 回到盤心（＝08 起格，同框換長圖）；"
                  "起格接 06（同在北盤）、迄格是換組頁：check_shots 的「起格切點」⚠ 可接受"),
        dict(code="08", kind="T", sec=11, north=True,
             frames=[HAND, AAG0], layers=["晨"], labels=[], labels_end=ls("Aagjuuk"),
             vo="天亮前最重要的報時星，在東北方的地平線上：牛郎星和旁邊的河鼓三，叫 Aagjuuk。",
             note="北盤→長圖同框換組（畫面完全相同）；沿走廊往下，經過天津四、織女星，到 Aagjuuk"),
        dict(code="09", kind="Z", sec=15, north=True,
             frames=[AAG0, AAG1], layers=["晨"], labels=ls("Aagjuuk"),
             overlay="C-A14-03_Aagjuuk初見", overlay_layers=["地平層", "十二月初層", "第二週層", "冬至層"],
             vo="奇怪的是，秋天傍晚它就掛在西南天，大家卻當作沒看見。一定要等十二月第二週的某個清晨，"
                "它第一次從東北方冒出來，Aagjuuk 才算「出來了」。",
             note="推近 Aagjuuk；之後定格疊概念圖 C-A14-03（同一個黎明時刻，牛郎星一天比一天高）"),
        dict(code="10", kind="Z", sec=12, north=True,
             frames=[AAG1, AAG2], layers=["晨"], labels=ls("Aagjuuk"),
             vo="從那天起，孩子們天沒亮就被叫出門看：Aagjuuk 出來了沒？只要大人說一聲 aagjuliqtuq——"
                "Aagjuuk 出來了——一天的活就開始了。",
             note="緩推"),
        dict(code="11", kind="Z", sec=16, north=True,
             frames=[AAG2, AAG3], layers=["晨"], labels=ls("Aagjuuk"),
             vo="它也是日曆：Aagjuuk 第一次在清晨露臉，就是一年最短的那幾天。一九九〇年十二月十九號，"
                "一位老人家在 Igloolik 的社區廣播宣布：冬至到了——因為他看見了 Aagjuuk。",
             note="緩推"),
        dict(code="12", kind="Z", sec=19, north=True,
             frames=[AAG3, AAGX], layers=["晨", "擔"], labels=ls("Aagjuuk", "跨文化-扁擔"),
             labels_start=ls("Aagjuuk"),          # 起格＝11 迄格（fov 27）：名稱表會被右緣切掉，迄格才開
             vo="在阿拉斯加，這兩顆星是「兩道陽光」：太陽回來時射出的頭兩道光。往南走，同一排星卻常常是一根扁擔："
                "中國的牛郎挑著兩個孩子；阿努塔島民、羅馬尼亞人，也都看見有人挑著擔子。",
             note="拉遠；扁擔線（綠：河鼓三—牛郎—河鼓一）淡入；跨文化名稱表在右邊（西）"),
        dict(code="13", kind="Z", sec=17, north=True, cut=True,
             frames=[ORI1, ORI2], layers=["獵"], labels=ls("追熊"),
             vo="漫長的夜裡，天上也有故事。獵戶的腰帶叫 Ullaktut，「奔跑的人」：他們在夜裡追一頭北極熊——"
                "紅色的畢宿五是熊 Nanurjuk，旁邊那群 V 字是狗 Qimmiit。追著追著，人、狗和熊，一起跑上了天。",
             note="【硬切】獵戶＋畢宿＋昴宿；奔跑的人（藍）、熊與狗群（紅）"),
        dict(code="14", kind="Z", sec=17, north=True,
             frames=[ORI2, ORI3], layers=["獵"], labels=ls("追熊"), labels_end=ls("追熊", "參宿七"),
             vo="跑到一半，有人的手套掉了。哥哥說：「月亮正圓，沒什麼好怕的，回去撿吧！」他一回頭就落後了——"
                "有人說，他成了腰帶下面的參宿七；也有人說，他就這樣回到地上，把故事帶回了營地。",
             note="往下推到參宿七；迄格加「Kingulliq 落在後面的」"),
        dict(code="15", kind="S", sec=18, north=True,
             frames=[ORI3, SIR], layers=["獵"], labels=ls("天狼星"),
             overlay="C-A14-05_因紐特星名小辭典",
             vo="再往下是天狼星。在 Igloolik，它最高只爬到四度，貼著地平線閃個不停，所以叫 Singuuriq。"
                "老人說，有人困在漂走的海冰上：一個跟著天狼星走，再也沒回來；其他人跟著北邊的織女星，回到了岸邊。",
             note="往東南（左下）滑到天狼星；結束後疊 9:16 圖卡 因紐特星名小辭典（可存圖）"),
        dict(code="16", kind="Z", sec=18, north=True,
             frames=[SIR], layers=["獵"], labels=[],
             overlay="C-A14-04_太陽回來", overlay_layers=["油燈層", "半邊笑層"],
             vo="一月中，太陽終於回來。孩子們挨家挨戶，把每一盞海豹油燈吹熄，換上新燈芯，再從同一把新火點亮。"
                "第一個看見太陽的人，只能用半邊臉笑：一邊歡迎溫暖，另一邊知道——冷，還沒過完。",
             note="畫面不動；定格疊概念圖 C-A14-04 太陽回來（油燈 → 半邊笑）"),
        dict(code="17", kind="Z", sec=12, north=True,
             frames=[SIR, WIDE], layers=["獵"], labels=ls("追熊", "天狼星"),
             vo="在很多因紐特方言裡，「明天」叫 qauppat，字面上是「如果天亮的話」。"
                "在極夜裡，天亮從來不是理所當然——所以他們抬頭，讀星星。",
             note="拉遠到整片冬季星空"),
        dict(code="18", kind="Z", sec=19, north=True,
             frames=[WIDE], layers=["獵"], labels=[],
             overlay="C-A14-06_這週末抬頭看",
             vo="這週末在台灣：天黑後往西看，牛郎和河鼓三還有二十幾度高，八點多才落下；回頭往東，"
                "奔跑的獵人正追著畢宿五爬上來，東北方的一對鎖骨也斜斜地升起。下週二冬至，抬頭讀讀看。",
             note="定格疊 9:16 圖卡 這週末抬頭看（台北 12/19；可存圖）"),
        dict(code="19", kind="Z", sec=7, north=True,
             frames=[WIDE, END], layers=["獵"], labels=[],
             vo="下週五是聖誕節，我們去北歐：Yule 之夜的狼與神駒。",
             card="下集見｜北歐：Yule 之夜的狼與神駒",
             note="推近腰帶；端卡＋追蹤 CTA"),
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
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  北盤旋轉角（Igloolik 12/18–19，面向北方）：" +
          "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  x：牛郎 {x_of(S[ALTAIR][0]):+.1f}、織女 {x_of(S[VEGA][0]):+.1f}、參宿四 {x_of(S[BETELGEUSE][0]):+.1f}、"
          f"參宿七 {x_of(S[RIGEL][0]):+.1f}、畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、天狼 {x_of(S[SIRIUS][0]):+.1f}；"
          f"仙后框 {CAS}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips, 原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 拼法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [dict(原文=o, 中譯=z, 顏色="green") for o, z in CROSS],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_igloolik": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL,
              labels=[dict(it, pt=5) for items, _ in label_sets for it in items],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
