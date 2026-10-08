# -*- coding: utf-8 -*-
"""A-15 北歐：Yule 之夜的狼與神駒｜大畫布 v4.6

論點：維京人沒有留下星圖。今天知道的北歐星名少得可憐——一本十二世紀冰島手抄本（GKS 1812 4to，
Beckman & Kålund《Alfræði íslenzk II: Rímtöl》）最古老部分（約 1190–1200 年）一份拉丁文—冰島文詞彙表裡註的幾個名字，加上 Edda 裡
明說被丟上天的兩樣東西（巨人 Þjazi 的眼睛、Aurvandil 的腳趾）。其中最有畫面的是畢宿的 V 字：
Úlfs kjaptr「狼嘴」。北歐神話的天空一直在逃命：太陽被狼 Sköll 追、月亮被 Hati 追，太陽車由
Árvakr、Alsviðr 兩匹神駒拉，黑夜騎 Hrímfaxi「霜鬃」；而狼嘴正好張在日月走的路（黃道）旁邊。
把這個 V 看成嘴的不只北歐：巴比倫「公牛的下顎」、Tikuna「鱷魚的嘴」、圖皮與洛科諾「貘的下巴」。
聖誕節在北歐叫 jul（Yule）：十世紀挪威國王 Hákon 立法把 Yule 挪到跟聖誕節同一天。
奧丁有個名字叫 Jólnir；聖誕老人的八隻馴鹿＝Sleipnir 是近代的說法（八隻馴鹿最早見於 1823 年的詩）。

來源：Stellarium norse（Jonas Persson；Rímtöl 的五個星座＋三個星名）、norse_edda（Eyermann／
Hoffmann：Úlfs Keptr 在月亮的路上、Þjazi 的眼睛＝北河二三的推測）；跨文化：babylonian_mulapin、
tikuna、tupi、lokono、egyptian、chinese、inuit；Snorri《Gylfaginning》10–12、51、《Skáldskaparmál》
（Þjazi、Aurvandil）、《Vafþrúðnismál》14、《Heimskringla・Hákonar saga góða》；PyEphem 自算。

鏡頭路線：長圖（畢宿＝狼嘴）→ Yule 變聖誕（概念圖）→ 奧丁與八隻馴鹿（概念圖）→ 拉遠：手抄本與
Edda → 推近狼嘴 → 天上的追逐（概念圖）→ 拉遠：黃道＝日月之路 → 跨文化「同一個 V 字」（標籤疊＋
圖卡）→ 往下：漁夫（腰帶）→ 往東：巨人的眼睛（雙子）→【自動換組】北盤：特隆赫姆面北、山＝地平線，
12/24 傍晚 16:00→22:00 → 兩輛車 → 引路星一千年前（概念圖）→ 小辭典（圖卡）→【自動換組】長圖：
這週末（圖卡）→ 下集預告：腰帶（X-02 獵戶環球）。

參數
  lst = 79 → 走廊（x=0）＝RA 79（五車二 x≈0）：畢宿五 x +10、畢宿 V +12…+13、昴宿 +22、
             腰帶 −4、參宿四 −10、北河二 −35、北河三 −37、天狼 −22。
             北盤旋轉角＝lst − 特隆赫姆地方恆星時 − 180（北盤面向北方）：
             12/24 16:00 −70°、18:00 −100°、20:00 −130°、22:00 −160°（23:20 會跨過 ±180，
             所以北盤只轉到 22:00；每一步都逆時針＝時間往前）。
  D_s = 47、D_r = 51 → 五車二 +46.0、北河二 +31.9 都在帶內；北斗只在北盤鏡頭出現（盤檔是完整等距圓，
             天權以外 Alkaid +49.3 在縫合帶也沒關係：換組那格 fov 48 只看得到 dec≥57）。
  D_fill = −25 → k=1.469、R_fill=168.95（盤寬 ÷ 畫布寬 ＝ 0.938608）；特隆赫姆面北：
             北方地平線在 dec +26.6（盤心下方 93.2 單位），fov 140 角落 151.8 < 168.4 ✓
  x_tN = x_tS = 0
  check_shots 對 11–14（北盤 R）報「起、迄格含長圖側扇區」⚠：這四鏡前後都由 gen_canva_pages 自動補
  換組頁（盤轉回 0°、fov 30 回到盤心再同框換組），不會從面北的大框直接切回大畫布——可接受。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-15"
OUT = os.path.join(BASE, "05_素材/A-15_北歐/_v4大畫布")
LST0 = 79.0
TRD = (63.4305, 10.3951)        # 特隆赫姆（Niðaróss），CET（UTC+1）
PHI = 63.43                     # 面北 R 鏡頭的地平線緯度
TPE = (25.0330, 121.5654)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）：特隆赫姆的地方恆星時 → 北盤旋轉角
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


def rot_at(when):
    """北盤面向北方：盤心正下方＝下中天（lst_obs＝lst_view−180）；Canva 正角＝順時針。
    rot＝lst − lst_obs − 180，收在 (−180, 180]。"""
    L = lst_at(*TRD, 1, when)
    return round((LST0 - L) % 360.0 - 180.0, 2)


T_TRD = {"16:00": "2026/12/24 16:00", "18:00": "2026/12/24 18:00", "20:00": "2026/12/24 20:00",
         "22:00": "2026/12/24 22:00"}
ROT = {k: rot_at(v) for k, v in T_TRD.items()}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALDEBARAN, THETA2_TAU, GAMMA_TAU, DELTA1_TAU, EPS_TAU = 21421, 20894, 20205, 20455, 20889
HYADES = [ALDEBARAN, THETA2_TAU, GAMMA_TAU, DELTA1_TAU, EPS_TAU]
ALCYONE = 17702
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BELT = [MINTAKA, ALNILAM, ALNITAK]
BETELGEUSE, BELLATRIX, RIGEL, SAIPH = 27989, 25336, 24436, 27366
CASTOR, POLLUX = 36850, 37826
CAPELLA, MENKALINAN, ELNATH = 24608, 28360, 25428
POLARIS, KOCHAB, PHERKAD = 11767, 72607, 75097
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
SIRIUS, PROCYON, ARCTURUS, VEGA = 32349, 37279, 69673, 91262
MAINS = HYADES + BELT + [CASTOR, POLLUX, CAPELLA, POLARIS, KOCHAB, PHERKAD, BETELGEUSE, RIGEL,
                         ALCYONE] + DIPPER


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium norse：Rímtöl 詞彙表的星座；巨人之眼取 norse_edda）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
NO = {}
for c in json.load(open(os.path.join(SC_NEW, "norse", "index.json"), encoding="utf-8"))["constellations"]:
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    NO[c["common_name"]["english"]] = [s for s in segs if len(set(s)) >= 2]
ED = {}
for c in json.load(open(os.path.join(SC_NEW, "norse_edda", "index.json"), encoding="utf-8"))["constellations"]:
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    ED[c["common_name"]["english"]] = [s for s in segs if len(set(s)) >= 2]

SEG_WOLF = NO["Wolf's Mouth"]                        # 畢宿五—θ2—γ—δ1—ε（V 字）
SEG_FISH = NO["The Fishermen"]                       # 腰帶三顆
SEG_KARL = NO["Man's Cart"]                          # 北斗
SEG_KVEN = NO["Woman's Cart"]                        # 小熊
SEG_ASAR = NO["The Asar Battlefield"]                # 御夫（只在 L4 總層）
SEG_TOE = NO["Aurvandil's Toe"]                      # 北冕（Persson 的推測；只在 L4 總層）
SEG_EYES = ED["Thiazi's Eyes"]                       # 北河三—北河二（norse_edda 的推測）

# 黃道＝日月之路：用 v=99 的假星（不會畫成星點）串成大圓
ECL_HIPS = []


def add_ecliptic(S):
    eps = math.radians(23.4393)
    for i, lam in enumerate(range(0, 362, 2)):
        L = math.radians(lam % 360)
        ra = math.degrees(math.atan2(math.sin(L) * math.cos(eps), math.cos(L))) % 360
        dec = math.degrees(math.asin(math.sin(eps) * math.sin(L)))
        h = 990000 + i
        S[h] = (ra, dec, 99.0)
        ECL_HIPS.append(h)


LG_WOLF = [(SEG_WOLF, "red", 1.1)]
LG_ECL = [([ECL_HIPS], "#9FB4D9", 0.55)]
LG_FISH = [(SEG_FISH, "blue", 1.0)]
LG_EYES = [(SEG_EYES, "amber", 1.0)]
LG_CART = [(SEG_KARL, "amber", 1.0), (SEG_KVEN, "green", 1.0)]
LG_ALL = (LG_WOLF + LG_FISH + LG_EYES + LG_CART +
          [(SEG_ASAR, "purple", 0.8), (SEG_TOE, "purple", 0.8)])
LINE_SETS = [(LG_WOLF, "連線-狼嘴"), (LG_ECL, "連線-日月之路"), (LG_FISH, "連線-漁夫"),
             (LG_EYES, "連線-巨人之眼"), (LG_CART, "連線-兩輛車")]
LINES_KEY = {"L4": "星座連線", "狼": "連線-狼嘴", "路": "連線-日月之路", "漁": "連線-漁夫",
             "眼": "連線-巨人之眼", "車": "連線-兩輛車"}
LINE_GROUPS = {"L4": LG_ALL, "狼": LG_WOLF, "路": LG_ECL, "漁": LG_FISH, "眼": LG_EYES, "車": LG_CART}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A 系列同一套算法，補上北歐字母）
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
            n += max(1, len(re.findall(r"[aeiouyāēīōūáéíóúýǫöæø]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、名詞總表（＝標籤對照表；給組員直接複製貼上）
#   (錨點 HIP 群, 原文（古北歐語正規化拼法）, Stellarium 拼法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (HYADES, "Úlfs kjaptr", "Ulf's Keptr", "Wolf's Mouth", "狼嘴（畢宿）", "red",
     "GKS 1812 4to 最古老部分（約 1190–1200 年）的拉丁文—冰島文詞彙表寫 Ulfs keptr（Beckman & Kålund "
     "1914–16《Alfræði íslenzk II: Rímtöl》p.72）；同一本手抄本十四世紀的星座篇另寫 Vlfs kiopt（Etheridge）；"
     "kjaptr＝嘴、顎（現代冰島語 kjaftur）"),
    (BELT, "Fiskikarlar", "Fiskikarlar", "Fishermen", "漁夫（獵戶腰帶）", "blue",
     "GKS 1812 4to 詞彙表（Rímtöl p.72）；三顆＝三個漁夫"),
    (BELT, "Friggerock", "—", "Frigg's Distaff", "Frigg 的紡紗桿（瑞典民間）", "purple",
     "瑞典民間名（Grimm《Teutonic Mythology》；Schön 2004《Asa-Tors hammare》p.228 另記 Frejerock）"),
    ([CASTOR, POLLUX], "Þjaza augu", "Þjázis augu", "Thiazi's Eyes", "巨人 Þjazi 的眼睛（推測）", "amber",
     "《Skáldskaparmál》：奧丁把 Þjazi 的眼睛丟上天成兩顆星（《Hárbarðsljóð》19 說是 Thor）；"
     "哪兩顆不知道，北河二三是 norse_edda 的推測"),
    (DIPPER, "Karlvagn", "Karlvagn", "Man's Cart", "男人的車（北斗）", "amber",
     "GKS 1812 4to 詞彙表（Rímtöl p.72）；今天瑞典語 Karlavagnen"),
    ([POLARIS, KOCHAB, PHERKAD], "Kvennavagn", "Kvennavagn", "Woman's Cart", "女人的車（小熊）", "green",
     "GKS 1812 4to 詞彙表（Rímtöl p.72）"),
    ([POLARIS], "Leiðarstjarna", "Leidarstjarna", "Guide Star", "引路的星（北極星）", "amber",
     "Stellarium norse：Leidarstjarna＝Polaris（引 Rímtöl pp.48–53，不確定在 12 世紀的詞彙表裡）；1000 年時離北天極 6.2°（PyEphem）"),
    ([CAPELLA, MENKALINAN, ELNATH], "Asar bardagi", "Asar Bardagi", "The Asar Battlefield", "眾神之戰（御夫）",
     "purple", "Rímtöl p.72；Asar bardagi 是 Stellarium／Persson 的寫法（正規化應作 Ása bardagi？），字義有爭議，片中不唸"),
]
# 跨文化：同一個 V 字（畢宿）＝嘴
CROSS = [("Is lê", "公牛的下顎（巴比倫）", "Stellarium babylonian_mulapin 036 Jaw of the Bull；MUL.APIN I（Anu 之路）"),
         ("Coyatchicüra", "鱷魚的嘴（Tikuna）", "Stellarium tikuna 003 Cayman’s Jaw"),
         ("Tapi'i rainhyka", "貘的下巴（圖皮）", "Stellarium tupi 007 Tapir's Jawbone"),
         ("Kama tâla", "貘的下巴（洛科諾）", "Stellarium lokono 005 Jaw of the tapir（Rybka 2018）"),
         ("Qimmiit", "狗群（因紐特）", "MacDonald《The Arctic Sky》p.58；A-14")]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    add_ecliptic(S)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=47, D_r=51, D_fill=-25,
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
            it["disc"] = True
        return it

    def pair(a, orig, zh, color, dx, dy, key, disc=False, s1=1.5, s2=1.1, gap=2.3):
        """原文在上、中文在下（同一錨點）"""
        return [item(a, orig, color, s1, dx, dy + gap / 2, key, disc),
                item(a, zh, "white", s2, dx, dy - gap / 2, key + "-zh", disc)]

    T = {t[1]: t for t in TERMS}

    def term(name, dx, dy, disc=False, s1=1.5, s2=1.1, gap=2.3):
        a, orig, _, _, zh, col, _ = T[name]
        return pair(a, orig, zh, col, dx, dy, name, disc, s1, s2, gap)

    # ── 長圖 ──
    LB_WOLF = term("Úlfs kjaptr", 1.0, -5.2, s1=1.5, s2=1.1)          # V 字下方
    LB_CROSS = []
    for i, (orig, zh, _src) in enumerate(CROSS):
        y0 = 0.0 - 4.4 * i
        LB_CROSS.append(item(HYADES, orig, "red", 1.25, 18.0, y0 + 1.0, f"跨-{i}"))
        LB_CROSS.append(item(HYADES, zh, "white", 0.95, 18.0, y0 - 1.25, f"跨-{i}-zh"))
    LB_FISH = term("Fiskikarlar", 0.0, -3.4, s1=1.4, s2=1.05) + term("Friggerock", 0.0, 4.4, s1=1.2, s2=0.95)
    LB_EYES = term("Þjaza augu", 0.0, -4.2, s1=1.2, s2=0.9, gap=1.9)
    # ── 北天（R 鏡頭，fov 140）：盤上的字不跟著轉，dx/dy 是畫面方向；字級 4.4／3.6 ≈ Canva 43／36 px ──
    # 位置逐頁算過（畫面 px：山稜最高約 Y 1435，字一律放在 Y 1300 以上；fov 140 時 1 單位＝7.71 px）
    LB_POLE = term("Leiðarstjarna", -26.8, 10.8, s1=4.4, s2=3.6, gap=4.6)   # 22:00：北極星左上（仙后 W 下方的空處）
    LB_KARL_18 = term("Karlvagn", 47.9, 4.4, s1=4.4, s2=3.6, gap=4.6)       # 18:00：北斗躺在北方低空，字放斗口右邊
    LB_KARL_20 = term("Karlvagn", -45.9, -2.7, s1=4.4, s2=3.6, gap=4.6)     # 20:00：北斗爬到東北，字放斗柄左邊
    LB_KVEN = term("Kvennavagn", -32.6, 2.6, s1=4.4, s2=3.6, gap=4.6)       # 20:00：小熊掛在北極星下方，字放左邊

    label_sets = [(LB_WOLF, "狼嘴"), (LB_CROSS, "跨文化-同一個V字"), (LB_FISH, "漁夫"),
                  (LB_EYES, "巨人之眼"), (LB_POLE, "引路星"), (LB_KARL_18, "男人的車-18"),
                  (LB_KARL_20, "男人的車-20"), (LB_KVEN, "女人的車")]

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
    kphi = m.k * PHI

    def FN(t):                                   # 特隆赫姆面北：地平線北點約在畫面 Y≈1600
        return (0.0, round(yp - (kphi - 82.9), 2), 140.0, ROT[t])

    xa, ya = m.pos_primary(*centroid(HYADES, S))
    WIDE0 = (4.0, 8.0, 40.0, 0.0)                # 開場：金牛＋獵戶＋御夫
    WOLF1 = (round(xa, 1), round(ya, 1), 24.0, 0.0)          # 狼嘴特寫
    WOLF2 = (round(xa, 1), round(ya - 1.0, 1), 30.0, 0.0)    # 追逐：概念圖底
    ECL = (round(xa - 2.0, 1), 8.0, 44.0, 0.0)               # 黃道＝日月之路
    CROSSF = (round(xa + 10.0, 1), 3.0, 42.0, 0.0)            # 右邊（西）留給名稱表
    xb, yb = m.pos_primary(*centroid(BELT, S))
    FISH = (round(xb, 1), round(yb + 1.0, 1), 30.0, 0.0)
    xg, yg = m.pos_primary(*centroid([CASTOR, POLLUX], S))
    GEM = (round(xg, 1), 20.0, 30.0, 0.0)         # fov 30：換北盤時「上移」那一段才不會太快（f_sw＝這一格的 fov）
    WEEKA = (round(xa - 8.0, 1), 6.0, 40.0, 0.0)  # 這週末：畢宿＋腰帶（9:16 框裝不下雙子，往東北滑過去）
    WEEKB = (-30.0, 14.0, 36.0, 0.0)             # 雙子（聖誕節的月亮在北河三旁 4.5°）
    END = (round(xb, 1), round(yb, 1), 24.0, 0.0)  # 下集：腰帶

    def ls(*names):
        return list(names)

    HZ = [PHI]
    shots = [
        dict(code="01", kind="Z", sec=11, north=True,
             frames=[WIDE0, WOLF1], layers=["狼"], labels=[], labels_end=ls("狼嘴"),
             vo="上週在北極圈，這群星是一群狗。今晚聖誕節，我們往東到北歐："
                "同一片星空，維京人看見的——是一張狼嘴。",
             card="同一片星空，維京人看見——一張狼嘴。",
             note="開場字卡；從金牛—獵戶—御夫推近畢宿，狼嘴（紅）淡入"),
        dict(code="02", kind="Z", sec=23, north=True,
             frames=[WOLF1], layers=["狼"], labels=ls("狼嘴"),
             overlay="C-A15-01_Yule變聖誕", overlay_layers=["仲冬層", "立法層", "今天層"],
             vo="北歐人到今天還把聖誕節叫 jul，英文的古字是 Yule。這個節比基督教更早到北方："
                "從仲冬那一夜開始，一連過三晚。十世紀，挪威國王 Hákon 立了法：Yule 改跟基督徒的聖誕節同一天，"
                "每個人都得備好一份啤酒，不然就罰錢——酒喝多久，節就過多久。",
             note="畫面不動；定格疊概念圖 C-A15-01（仲冬三夜 → Hákon 立法 → 今天的 jul）"),
        dict(code="03", kind="Z", sec=20, north=True,
             frames=[WOLF1], layers=["狼"], labels=ls("狼嘴"),
             overlay="C-A15-02_八隻馴鹿", overlay_layers=["神駒層", "一頭層", "八隻層"],
             vo="這個節日跟奧丁有關：他有個名字就叫 Jólnir，「Yule 的那位」。常聽人說，聖誕老人的八隻馴鹿，"
                "來自奧丁那匹八條腿的神駒 Sleipnir——其實八隻馴鹿是 1823 年美國紐約一首詩寫出來的，"
                "古書裡找不到這層關係。",
             note="畫面不動；定格疊概念圖 C-A15-02（Sleipnir 八條腿 → 1821 一頭馴鹿 → 1823 八隻）"),
        dict(code="04", kind="Z", sec=23, north=True,
             frames=[WOLF1, WIDE0], layers=["狼"], labels=[],
             vo="那維京人的天上，有哪些星座？說實話，留下來的很少。一本十二世紀末的冰島手抄本，"
                "在一份拉丁文詞彙表裡，替幾個星座註上北歐名字；神話集 Edda 說，天空是巨人的頭蓋骨，"
                "星星是火之國飛出來的火花——但明說被丟上天、變成某顆星的，只有兩樣。",
             note="拉遠到整片冬季星空"),
        dict(code="05", kind="Z", sec=10, north=True,
             frames=[WIDE0, WOLF1], layers=["狼"], labels=ls("狼嘴"), labels_start=[],
             vo="手抄本裡最有畫面的一個，就在這裡：畢宿的 V 字，叫 Úlfs kjaptr——狼嘴。兩排星，就像張開的上下顎。",
             note="推近畢宿，狼嘴標籤"),
        dict(code="06", kind="Z", sec=28, north=True,
             frames=[WOLF1, WOLF2], layers=["狼"], labels=ls("狼嘴"),
             overlay="C-A15-03_天上的追逐", overlay_layers=["太陽層", "月亮層", "神駒層"],
             vo="是哪一匹狼？書上沒寫。但北歐神話裡的天空，一直在逃命：太陽被狼 Sköll 追，月亮被狼 Hati 追，"
                "所以它們一刻都不能停；到了諸神的黃昏，狼會把太陽吞下去。拉著太陽跑的，是兩匹神駒："
                "Árvakr「早起」、Alsviðr「飛快」；黑夜也騎一匹馬，叫 Hrímfaxi「霜鬃」——每天早上，"
                "牠嚼子上滴下的白沫，就是山谷裡的露水。",
             note="微拉；定格疊概念圖 C-A15-03（太陽與 Sköll → 月亮與 Hati → 神駒：Árvakr、Alsviðr、Hrímfaxi）"),
        dict(code="07", kind="Z", sec=13, north=True,
             frames=[WOLF2, ECL], layers=["狼", "路"], labels=ls("狼嘴"),
             vo="再看這條線：太陽和月亮走的路。狼嘴就張在路邊：月亮每個月、太陽每年初夏，"
                "都要從它附近經過。所以有人猜，它等著咬的，就是日月。",
             note="拉遠；黃道（日月之路，淡藍灰）淡入，從昴宿和畢宿之間穿過"),
        dict(code="08", kind="Z", sec=19, north=True,
             frames=[ECL, CROSSF], layers=["狼"], labels=ls("狼嘴", "跨文化-同一個V字"),
             labels_start=ls("狼嘴"),
             overlay="C-A15-05_同一個V字",
             vo="把這個 V 看成一張嘴的，不只北歐人：古巴比倫叫它「公牛的下顎」；亞馬遜的 Tikuna 人說是鱷魚的嘴；"
                "巴西的圖皮人、南美北岸的洛科諾人，都說是貘的下巴。上週的因紐特人，看到的則是一群狗。",
             note="往右（西）移，跨文化名稱表；結束後疊 9:16 圖卡 C-A15-05 同一個 V 字（可存圖）"),
        dict(code="09", kind="S", sec=10, north=True,
             frames=[CROSSF, FISH], layers=["漁"], labels=ls("漁夫"),
             vo="往下是獵戶的腰帶。冰島的手抄本叫它 Fiskikarlar：三個漁夫；瑞典民間卻說，那是女神 Frigg 的紡紗桿。",
             note="往左下滑到腰帶；漁夫（藍）"),
        dict(code="10", kind="S", sec=22, north=True,
             frames=[FISH, GEM], layers=["眼"], labels=ls("巨人之眼"), labels_start=ls("漁夫"),
             vo="Edda 明說的那兩樣呢？巨人 Þjazi 被眾神殺死，奧丁把他的兩隻眼睛丟上天，成了兩顆星；"
                "雷神 Thor 背著 Aurvandil 渡過結冰的河，凍僵的一根腳趾被他折下來，也丟上了天。是哪幾顆？沒人知道；"
                "有人猜，那雙眼睛就是雙子座並排的這兩顆。",
             note="往左上（東北）滑到雙子；北河二—北河三（琥珀）＝巨人之眼（推測）"),
        dict(code="11", kind="R", sec=12, north=True, horizon=HZ,
             frames=[FN("16:00"), FN("18:00")], layers=["車"], labels=ls("男人的車-18"),
             labels_start=[],
             vo="轉身向北，到挪威中部的特隆赫姆。冬至前後，這裡的太陽下午兩點半就下山，隔天早上十點才出來——"
                "一天有十九個多鐘頭是夜。",
             note=f"【自動換組】長圖→北盤；特隆赫姆 12/24 面北（山＝北方地平線），盤逆時針 16:00→18:00"
                  f"（{ROT['16:00']:+.1f}°→{ROT['18:00']:+.1f}°）"),
        dict(code="12", kind="R", sec=12, north=True, horizon=HZ,
             frames=[FN("18:00"), FN("20:00")], layers=["車"], labels=ls("男人的車-20", "女人的車"),
             labels_start=ls("男人的車-18"),
             vo="這麼長的夜，就看兩輛車慢慢繞：北斗叫 Karlvagn，男人的車——今天的瑞典人還叫它 Karlavagnen；"
                "小熊叫 Kvennavagn，女人的車。",
             note=f"盤逆時針 18:00→20:00（{ROT['20:00']:+.1f}°）；北斗爬向東北"),
        dict(code="13", kind="R", sec=12, north=True, horizon=HZ,
             frames=[FN("20:00"), FN("22:00")], layers=["車"], labels=ls("引路星"),
             labels_start=ls("男人的車-20", "女人的車"),
             overlay="C-A15-04_引路星一千年", overlay_layers=["今天層", "一千年前層"],
             vo="它們繞著的北極星，叫 Leiðarstjarna，「引路的星」。不過一千年前，它離北天極還有六度，"
                "自己也繞著小圈在轉。",
             note=f"盤逆時針 20:00→22:00（{ROT['22:00']:+.1f}°）；之後定格疊概念圖 C-A15-04（今天 0.6° → 一千年前 6.2°）"),
        dict(code="14", kind="R", sec=6, north=True, horizon=HZ,
             frames=[FN("22:00")], layers=["車"], labels=ls("引路星"),
             overlay="C-A15-06_北歐星名小辭典",
             vo="這集的北歐星名，整理成一張小辭典，可以存起來。",
             note="畫面不動；疊 9:16 圖卡 C-A15-06 北歐星名小辭典（可存圖）"),
        dict(code="15", kind="S", sec=17, north=True,
             frames=[WEEKA, WEEKB], layers=["狼", "漁", "眼"], labels=ls("狼嘴", "漁夫", "巨人之眼"),
             overlay="C-A15-07_這週末抬頭看",
             vo="這週末在台灣：天黑後往東看，八點左右，畢宿五和狼嘴已經爬到半天高，腰帶在它右下方；"
                "東北東，雙子座的兩顆亮星旁邊，就是聖誕節的月亮——今晚去找找那雙巨人的眼睛。",
             note="【自動換組】北盤→長圖；畢宿＋腰帶 → 往東北滑到雙子；之後疊 9:16 圖卡 這週末抬頭看（台北 12/25；可存圖）"),
        dict(code="16", kind="S", sec=8, north=True,
             frames=[WEEKB, END], layers=["漁"], labels=ls("漁夫"), labels_start=ls("巨人之眼"),
             vo="下週五元旦，我們從這三個漁夫出發，繞地球一圈：全世界都認得的獵戶腰帶。",
             card="下集見｜獵戶環球：全世界都認得的三顆星",
             note="推近腰帶（X-02 獵戶環球）；端卡＋追蹤 CTA"),
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

    print("  北盤旋轉角（特隆赫姆 12/24，面向北方）：" +
          "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  x：畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、昴宿六 {x_of(S[ALCYONE][0]):+.1f}、參宿二 {x_of(S[ALNILAM][0]):+.1f}、"
          f"北河二 {x_of(S[CASTOR][0]):+.1f}、北河三 {x_of(S[POLLUX][0]):+.1f}、五車二 {x_of(S[CAPELLA][0]):+.1f}；"
          f"狼嘴框 {WOLF1}、雙子框 {GEM}、面北 16:00 {FN('16:00')}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips, 原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 拼法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [dict(原文=o, 中譯=z, 顏色="red", 來源=src) for o, z, src in CROSS],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_trondheim": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL + LG_ECL,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL + LG_ECL,
              labels=[dict(it, pt=5) for items, _ in label_sets for it in items],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
