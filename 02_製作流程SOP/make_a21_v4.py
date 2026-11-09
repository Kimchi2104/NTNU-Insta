# -*- coding: utf-8 -*-
"""A-21 薩米：馴鹿獵人的星空狩獵圖｜大畫布 v4.6

論點：薩米的 10 個星座全部屬於同一場狩獵。獵物 Sarvvis（公馴鹿，一說駝鹿）從仙后 W 經英仙到
五車二與御夫；獵人 Fávdna＝大角星，弓＝北斗（搖光→開陽→玉衡→天權→天璇是弓弧，天樞—天璣是箭）；
北極星 Boahjenásti 撐住天空，箭射中它世界就結束——所以這把弓每晚拉滿卻遲遲沒放。
幫手：Gállá 的兒子們（腰帶）、滑雪的人（北河二、三）、獵犬群（昴宿）；Gállá 本人說法不一。
IAU 2025：δ Per＝Sarvvis、ε Per＝Áldu；Le Monnier 1743 的馴鹿座。

來源：Stellarium sami（Jonas Persson，據 Lundmark 1982；新舊兩版 index.json 相同，10 個星座）；
跨文化：Stellarium russian_siberian／inuit／belarusian（北斗標準勺形）、arabic_ancient（大角星）；
天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，UTC+8）。逐字稿：04_腳本庫/A-21-…-v1.md。

連線：全部照 Stellarium sami（Sarva 15 顆 5 段、弓弧＋箭）；Gállá 的兒子們＝腰帶三顆；
  滑雪的人 Stellarium 是兩個單點，本集把北河二—北河三連一條短線（紫）讓「兩個人」看得出是一組。
  06 鏡紅色箭頭（連線-箭頭）：天璇→天樞→北極星的指極線再往前 22°（停在仙后 W 與英仙之間），
  終點與箭頭兩翼是假星（HIP 9000001–9000003，星等 99，不畫成星點），只當連線端點用。
  10 鏡勺形（西伯利亞 Лось／因紐特 Tukturjuit：兩份 Stellarium 連線完全相同）、13 鏡以利亞的車
  （白俄羅斯，也同一個勺形）各一層。

鏡頭路線：01–06 北盤（R，盤順著故事一路逆時針轉：+125°→+98°→+62°→+52°→+36°→−84°（06 拉遠成「大角星在下、
  北極星在中、鹿在上」的直幅）；06 最後推進盤心 fov 48、0°＝唯一一段順時針（84°，盤心附近星少、幾乎看不出））
  → 07【換長圖】同框換組（＝A-14 的做法：盤上的最後一格就是換組那一格）、沿走廊下來到腰帶→雙子→昴宿
  → 08 Gállá 的三個候選 → 09【換北盤】（gen_canva_pages 自動插回中心／上移／長圖轉北盤）銀河
  → 10 北斗三種說法 → 11 台北 2/12 20:00→23:00 面北 → 12 小辭典 → 13 推近北斗、下集。

參數
  lst = 135 → 決定因素是 11 鏡：rot＝(lst−LST台北)%360−180，2/12 20:00 LST 83.9 → −128.9°、
             23:00 LST 129.0 → −173.9°（v4.6 第四節：整段在 (−180,180] 內、單向逆時針）；
             而且 09–10 可以從換組的 0° 一路逆時針轉過去（0→−40→−80→−129），整集後半不倒轉。
             lst=75～84（獵戶置中）時台北是 +171→+126，09–10 得先順時針轉 170°（時間倒流），不用。
             長圖上：北河二 x +21、北河三 +19、南河三 +20、天狼 +34、腰帶 +51、參宿七 +56、昴宿 +78。
  D_s = 45、D_r = 49 → 北斗最南的搖光 +49.31 在北盤本體；北河二三 +28/+32、昴宿 +24、天狼 −16.7 在長圖帶。
             Sarvvis 的 15 顆 dec +28.6（五車五）…+63.7：dec < 49 那幾顆在大畫布落在縫合帶，
             但 Sarvvis 的鏡頭（01–06、09–13）全在北盤圖層組上（完整圓、逐點等距），不受影響。
  D_fill = −38.7 → k=1.3975、R_fill=179.85（盤寬 ÷ 畫布寬＝0.999183 ⚠ 只差 0.08%，Canva 千萬別設成同寬）：
             11 鏡台北面北 fov 162，23:00 要同時放進五車二／英仙（左，x −47…−55）、仙后和剛升起的大角星
             （右，x +99）＝畫面中心右移 22、角落距盤心 177.0 < 178.9。D_fill −35（R_fill 174.7）時 fov 150
             放不下五車二＋大角星，只好把盤撐到 |x_t|＋R_fill＝179.85 ≤ 180 的上限。
  x_tN = x_tS = 0

check_shots 的 ⚠（判斷後接受）
  01、03–05、11–13 R 鏡頭「畫面含長圖側扇區」：全程在北盤圖層組上。換組只有兩處：
  06 迄格＝盤心 fov 48、0°（在盤緣圈內，逐點重合）→ 07 起格同一格；
  08→09 由 gen_canva_pages 插「回中心／上移／長圖轉北盤」（盤心置中、0°），09 起格就是那一格。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-21"
OUT = os.path.join(BASE, "05_素材/A-21_薩米/_v4大畫布")
LST0 = 135.0
TPE = (25.0330, 121.5654)
PHI = 25.03                     # 11 鏡台北面北的地平線緯度


# ══════════════════════════════════════════════════════════════════
# 〇、星曆：台北地方恆星時 → 北盤旋轉角（面向北方）
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


def rot_at(when):
    """北盤面向北方：rot＝lst − lst_obs − 180，收在 (−180, 180]；Canva 正角＝順時針"""
    L = lst_at(*TPE, 8, when)
    return round((LST0 - L - 180.0 + 180.0) % 360.0 - 180.0, 2)


T_TPE = {"20:00": "2027/2/12 20:00", "22:00": "2027/2/12 22:00", "23:00": "2027/2/12 23:00"}
ROT = {k: rot_at(v) for k, v in T_TPE.items()}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, ARCTURUS = 11767, 69673
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
SARVA_HIPS = [8886, 6686, 4427, 3179, 746, 14328, 15863, 14576, 17358, 18532, 18246,
              24608, 25428, 23767, 23015]
D_PER, E_PER, A_PER, CAPELLA, CAPH = 17358, 18532, 15863, 24608, 746
CAS_W = [8886, 6686, 4427, 3179, 746]
BELT = [26727, 26311, 25930]
CASTOR, POLLUX = 36850, 37826
PROCYON, RIGEL, SIRIUS = 37279, 24436, 32349
VEGA, ALTAIR = 91262, 97649
PLEIADES = [17702, 17847, 17851, 17608, 17499, 17531]
ALCYONE = 17702
MAINS = [POLARIS, ARCTURUS] + DIPPER + SARVA_HIPS + BELT + [CASTOR, POLLUX, ALCYONE, PROCYON,
                                                            RIGEL, SIRIUS, VEGA, ALTAIR]
ARROW_END, ARROW_W1, ARROW_W2 = 9000001, 9000002, 9000003      # 假星（只當連線端點）


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu, key="english"):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["common_name"][key]] = [s for s in segs if len(set(s)) >= 2]
    return out


SM = load_sc("sami")
SEG_SARVA = SM["Sarva the Elk"]                      # 15 顆 5 段
SEG_BOW = SM["Favdna's Bow and Arrow"]               # 弓弧 5 顆＋箭 2 顆
SEG_SONS = SM["Galla's Sons"]                        # 腰帶
SEG_SKI = [[CASTOR, POLLUX]]                         # Stellarium 是兩個單點：本集連一條短線
SEG_LADLE = load_sc("russian_siberian")["Elk"]       # 標準勺形（＝inuit Tukturjuit＝belarusian 以利亞的車）
assert SEG_LADLE == load_sc("inuit")["Caribou"] == load_sc("belarusian")["Elias's Cart"]
SEG_ARROW = [[MER, DUB, POLARIS, ARROW_END], [ARROW_W1, ARROW_END, ARROW_W2]]

LG_SARVA = [(SEG_SARVA, "amber", 1.0)]
LG_BOW = [(SEG_BOW, "green", 1.1)]
LG_HUNT = LG_SARVA + LG_BOW
LG_ARROW = [(SEG_ARROW, "red", 1.0)]
LG_HELP = [(SEG_SONS, "blue", 1.0), (SEG_SKI, "purple", 1.0)]
LG_LADLE = [(SEG_LADLE, "blue", 0.9)]
LG_CART = [(SEG_LADLE, "amber", 1.0)]
LG_ALL = LG_HUNT + LG_HELP
LINE_SETS = [(LG_SARVA, "連線-Sarvvis"), (LG_BOW, "連線-弓與箭"), (LG_ARROW, "連線-箭頭"),
             (LG_HELP, "連線-幫手"), (LG_LADLE, "連線-勺形（西伯利亞・因紐特）"),
             (LG_CART, "連線-以利亞的車（白俄羅斯）")]
LINES_KEY = {"L4": "星座連線", "鹿": "連線-Sarvvis", "弓": "連線-弓與箭", "箭": "連線-箭頭",
             "幫": "連線-幫手", "勺": "連線-勺形（西伯利亞・因紐特）", "車": "連線-以利亞的車（白俄羅斯）"}
LINE_GROUPS = {"L4": LG_ALL, "鹿": LG_SARVA, "弓": LG_BOW, "箭": LG_ARROW, "幫": LG_HELP,
               "勺": LG_LADLE, "車": LG_CART}


def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def arrow_points(S):
    """天璇→天樞大圓的延長線：過北極星（離 0.7°）後再走 22° 當箭尖；兩翼往回 3.5°、偏 ±2.2°"""
    a, b = vec(*S[MER][:2]), vec(*S[DUB][:2])
    nrm = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    nn = math.sqrt(sum(c * c for c in nrm)); nrm = tuple(c / nn for c in nrm)
    t = (nrm[1] * b[2] - nrm[2] * b[1], nrm[2] * b[0] - nrm[0] * b[2], nrm[0] * b[1] - nrm[1] * b[0])

    def along(deg):                         # 從天樞沿大圓往前 deg 度
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return tuple(b[i] * c + t[i] * s for i in range(3))

    p = vec(*S[POLARIS][:2])
    d_pol = math.degrees(math.acos(max(-1, min(1, sum(b[i] * p[i] for i in range(3))))))
    tip = along(d_pol + 22.0)
    base = along(d_pol + 18.5)
    off = math.tan(math.radians(2.2))
    w1 = tuple(base[i] + nrm[i] * off for i in range(3))
    w2 = tuple(base[i] - nrm[i] * off for i in range(3))
    return radec(tip), radec(w1), radec(w2)


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    v = [sum(vec(*S[h][:2])[i] for h in hs) for i in range(3)]
    return radec(v)


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
#   (錨點 HIP 群, 原文（片中寫法）, Stellarium 轉寫, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (SARVA_HIPS, "Sarvvis", "Sarva／Sarvvis", "Sarva the Elk (bull reindeer)", "公馴鹿（一說駝鹿）", "amber",
     "Stellarium sami 001：elk、另名 Sarvvis『bull elk』；北薩米語 sarvvis＝公馴鹿（sarvva＝駝鹿）；仙后＋英仙＋御夫 15 顆"),
    ([D_PER], "Sarvvis ", "—", "Sarvvis (IAU 2025, δ Per A)", "公馴鹿（英仙 δ）", "amber",
     "IAU WGSN 2025/12/25；字尾空白只為與星座名區分 key"),
    ([E_PER], "Áldu", "—", "Áldu (IAU 2025, ε Per A)", "母馴鹿（英仙 ε）", "amber",
     "IAU WGSN 2025/12/25（reindeer cow）"),
    ([ARCTURUS], "Fávdna", "Favdna（Favtna）", "Favdna, the Hunter", "獵人（大角星）", "red",
     "Stellarium sami 005；Turi 作 Fávtna"),
    (DIPPER, "Fauna davgge", "Fauna davgge", "Favdna's Bow and Arrow", "Fávdna 的弓（北斗）", "green",
     "Stellarium sami 002：搖光→開陽→玉衡→天權→天璇＝弓弧，天樞—天璣＝箭；審稿建議拼法 Fávnna dávgi（未核）"),
    ([POLARIS], "Boahjenásti", "Boahjenaste", "Sky Support", "撐住天空的星（北極星）", "white",
     "Stellarium sami 004；箭射中它世界就結束（Stellarium；Turi 1910 星圖說明，DuBois 2011 p.167，未親核）"),
    (BELT, "Gallabarneck", "Gallabarneck", "Galla's Sons", "Gállá 的兒子們（獵戶腰帶）", "blue",
     "Stellarium sami 003；審稿建議拼法 Gállábártnit（未核）"),
    ([CASTOR, POLLUX], "Cuoigahægjek", "Cuoigahægjek", "The Ski Runners", "滑雪的人（北河二、三）", "purple",
     "Stellarium sami 010；審稿建議拼法 Čuoiggaheaddjit（未核）"),
    (PLEIADES, "獵犬群", "Rougot", "Pack of Dogs", "獵犬群（昴宿）", "amber",
     "Stellarium 把 dog pack 配給 Rougot，但這個字不是『狗群』（審稿）：片中只寫中文"),
    ([PROCYON], "Gállá？", "Galla", "Galla", "南河三", "white", "Stellarium sami 009 選南河三；一說參宿七、天狼星"),
    ([RIGEL], "Gállá？ ", "—", "Galla?", "參宿七", "white", "候選（字尾空白只為區分 key）"),
    ([SIRIUS], "Gállá？  ", "—", "Galla?", "天狼星", "white", "候選；Kautokeino 最高 4.3°（自算）"),
    ((95.0, 24.0), "Lodde-raiddaras", "Lodde-raiddaras", "Bird Path (Milky Way)", "鳥的路（銀河）", "white",
     "Stellarium description；錨點＝御夫—雙子之間的銀河（RA 95、Dec +24），09 迄格畫面內、避開 Sarvvis 連線"),
    ((95.0, 24.0), "Jakke-mærka", "Jakke-mærka", "Year Mark (Milky Way)", "年的記號（銀河）", "white",
     "Stellarium description：名字跟著季節換"),
    (DIPPER, "Лось", "Los'", "Elk (Siberian)", "駝鹿（西伯利亞）", "blue", "Stellarium russian_siberian（A-08）"),
    (DIPPER, "Tukturjuit", "Tukturjuit", "Caribou (Inuit)", "馴鹿（因紐特）", "blue", "Stellarium inuit 006（A-14）"),
    (DIPPER, "Fávdna 的弓", "Fauna davgge", "Favdna's Bow (Sami)", "弓（薩米）", "green", "10 鏡跨文化疊"),
    ([ARCTURUS], "al-Simāk al-Rāmiḥ", "ذو السلاح", "The High One with the Spear", "拿長矛的人（古阿拉伯）", "red",
     "arabic_ancient 1199『The armed one』；al-Simāk al-Rāmiḥ「拿長矛的高個子」（A-19）"),
    (DIPPER, "Іллёў воз", "Illyouo voz", "Elias's Cart (Belarusian)", "以利亞的車（白俄羅斯）", "amber",
     "Stellarium belarusian 001；下集 A-22"),
]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    tip, w1, w2 = arrow_points(S)
    S[ARROW_END], S[ARROW_W1], S[ARROW_W2] = (*tip, 99.0), (*w1, 99.0), (*w2, 99.0)
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-38.7,
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

    def term(name, dx, dy, s1=1.6, s2=1.2, gap=2.4, zh_only=False, a=None, disc=False):
        a0, orig, _, _, zh, col, _ = T[name]
        a = a if a is not None else a0
        if zh_only:
            out = [item(a, zh, col, s1, dx, dy, name)]
        else:
            out = [item(a, orig.strip(), col, s1, dx, dy + gap / 2, name),
                   item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh")]
        if disc:                                 # 盤專用（R 鏡頭）：dec < D_r 的星（大角星、英仙 ε…）也要上盤
            for it in out:
                it["disc"] = True
        return out

    # ── 盤上（fov 90–150）：字不跟著盤轉，dx/dy＝畫面方向；位置看 SB-鏡頭牆／對位參考 逐格調 ──
    BIG = dict(s1=3.6, s2=2.9, gap=4.4, disc=True)            # fov 120–150
    MID = dict(s1=2.6, s2=2.1, gap=3.2, disc=True)            # fov 80–100
    SM_ = dict(s1=1.5, s2=1.2, gap=1.9, disc=True)            # fov 40–50
    # 故事段的方位隨盤轉而變：每組標籤只在它那幾格用，dx/dy 照那幾格的畫面方向
    LB_SARVA = term("Sarvvis", 8.0, -12.0, **BIG)                # 01–03：鹿在畫面下方，字放鹿身右下
    LB_BOW = term("Fauna davgge", 16.0, 6.0, **BIG)              # 01、05–06：弓在大角星與北極星之間
    LB_FAV = term("Fávdna", 0.0, 0.0, **BIG)                     # 05–06：字放大角星右邊
    LB_FAV_L = term("Fávdna", 0.0, 0.0, **BIG)                   # 01–02：大角星在右上角，字放左邊
    LB_POL = term("Boahjenásti", 15.0, -3.0, **BIG)               # 06
    LB_SARVA_D = term("Sarvvis", 0.0, 0.0, **BIG)                # 06：鹿在畫面上緣，字放鹿身下方
    LB_SARVA_M = term("Sarvvis", 0.0, -13.0, **MID)               # 03 迄格（fov 90）
    LB_IAU = (term("Sarvvis ", -6.0, 4.5, **SM_) + term("Áldu", 11.0, -2.5, **SM_))   # 04 迄格（fov 44）
    # ── 長圖（fov 40–54） ──
    LB_SONS = term("Gallabarneck", 0.0, -5.0)
    LB_SKI = term("Cuoigahægjek", 0.0, 5.0)
    LB_DOGS = term("獵犬群", 0.0, -4.5, zh_only=True, s1=1.5)
    LB_GALLA = (term("Gállá？", 0.0, 3.6, s1=1.6, s2=1.3, gap=2.6) +
                term("Gállá？ ", 0.0, -3.6, s1=1.6, s2=1.3, gap=2.6) +
                term("Gállá？  ", 0.0, -3.8, s1=1.6, s2=1.3, gap=2.6))
    # ── 銀河兩個名字（09，fov 140）：同一錨點、兩層交替 ──
    LB_MW1 = term("Lodde-raiddaras", 0.0, 0.0, **BIG)
    LB_MW2 = term("Jakke-mærka", 0.0, 0.0, **BIG)
    # ── 10 鏡：北斗三種說法（整疊推到北斗外側空天區）＋大角星 ──
    CROSS = dict(s1=2.7, s2=2.2, gap=3.3, disc=True)
    LB_CROSS = (term("Лось", 0.0, 0.0, **CROSS) + term("Tukturjuit", 0.0, 0.0, **CROSS)
                + term("Fávdna 的弓", 0.0, 0.0, **CROSS))
    LB_ARAB = term("al-Simāk al-Rāmiḥ", 0.0, 0.0, **CROSS)
    # ── 11 台北面北（fov 150）：字縮到 Canva 下限附近 ──
    TP = dict(s1=3.0, s2=2.5, gap=3.6, disc=True)
    LB_TP = (term("Sarvvis", 0.0, 0.0, **TP) + term("Fauna davgge", 0.0, 0.0, **TP)
             + term("Boahjenásti", 0.0, 0.0, **TP))
    LB_TP_F = term("Fávdna", 0.0, 0.0, **TP)                    # 22:01 才升起：只在 23:00 那格開
    LB_CART = term("Іллёў воз", 0.0, 0.0, **MID)

    # dx/dy 由 place()（下）依鏡頭實際畫面算好再填：同一組標籤在不同旋轉角的畫面方向不同
    label_sets = [(LB_SARVA, "Sarvvis"), (LB_BOW, "弓"), (LB_FAV, "Fávdna"), (LB_FAV_L, "Fávdna-左"), (LB_POL, "Boahjenásti"),
                  (LB_SARVA_D, "Sarvvis-下"), (LB_SARVA_M, "Sarvvis-近"), (LB_IAU, "IAU2025"),
                  (LB_SONS, "Gállá的兒子們"), (LB_SKI, "滑雪的人"), (LB_DOGS, "獵犬群"), (LB_GALLA, "Gállá是誰"),
                  (LB_MW1, "銀河-鳥的路"), (LB_MW2, "銀河-年的記號"),
                  (LB_CROSS, "跨文化-北斗"), (LB_ARAB, "跨文化-大角星"),
                  (LB_TP, "台北面北"), (LB_TP_F, "台北-Fávdna"), (LB_CART, "以利亞的車")]

    # ════════════════════ 構圖（盤上：照旋轉角算星在畫面上的位置，自動取景） ════════════════════
    def disc_xy(hip_or_radec, rot):
        ra, dec = (S[hip_or_radec][:2] if isinstance(hip_or_radec, int) else hip_or_radec)
        keep = m.lst
        m.lst = LST0 - rot                      # 北盤：rot ≡ lst 平移（與 sb_grid 相同）
        p = m.pos_disc(ra, dec, True)
        m.lst = keep
        return (p[0][0], p[0][1] + yp) if p else None

    def fit(hips, rot, pad=0.12, minfov=30.0, dy=0.0, dx=0.0):
        pts = [disc_xy(h, rot) for h in hips]
        pts = [p for p in pts if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        fov = max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        far = lambda f: max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yp)
                            for sx in (-1, 1) for sy in (-1, 1))
        while far(fov) > m.R_fill - 1.0:         # 角落不能出填滿圓：縮 fov
            fov *= 0.98
        return (round(cx, 2), round(cy, 2), round(fov, 1), rot)

    HUNT = [ARCTURUS] + DIPPER + [POLARIS] + SARVA_HIPS
    R01a, R01b, R03, R04, R05, R06 = 125.0, 98.0, 62.0, 52.0, 36.0, -84.0
    F01a = fit(HUNT, R01a, pad=0.10)
    F01b = fit(HUNT, R01b, pad=0.10)
    F03 = fit(SARVA_HIPS, R03, pad=0.14)
    F04 = fit([D_PER, E_PER, A_PER, 18246], R04, pad=0.45, minfov=40.0)
    F05 = fit([ARCTURUS] + DIPPER, R05, pad=0.22)
    F06 = fit(HUNT + [ARROW_END], R06, pad=0.08, dy=-16.0)   # 大角星在下緣：畫面往下挪，讓它離開下方安全區
    HAND = (0.0, yp, 48.0, 0.0)                  # 盤⇄長圖同框換組（盤緣圈內，逐點重合）；yp 不取整：與 gen_canva_pages 的換組格逐位相同才會併頁
    # 長圖（lst 135）
    BELT_F = (round(x_of(S[25930][0]) - 1, 1), 1.0, 40.0, 0.0)
    GEM_F = (21.0, 20.0, 40.0, 0.0)
    PLE_F = (72.0, 18.0, 40.0, 0.0)
    GAL_F = (39.0, -5.0, 56.0, 0.0)
    DOWN = (12.0, 22.0, 48.0, 0.0)                # 沿走廊下來（|x|≤26 才有內容）
    # 後半（盤一路逆時針）
    R09, R10 = -40.0, -80.0
    F09 = fit(SARVA_HIPS + [POLARIS, 21421, 9884], R09, pad=0.10)     # 鹿＋銀河（往外到畢宿五）
    F09M = fit(SARVA_HIPS + [POLARIS, 21421, 9884], -20.0, pad=0.10)   # 09 中格：「鳥的路」
    F10 = fit([ARCTURUS] + DIPPER + [POLARIS], R10, pad=0.14, dy=-14.0)   # 大角星在下緣：畫面往下挪
    FN20 = (5.0, round(yp, 2), 162.0, ROT["20:00"])
    FN23 = (22.0, round(yp, 2), 162.0, ROT["23:00"])
    R13 = ROT["23:00"] - 3.0
    F13 = fit(DIPPER, R13, pad=0.30, minfov=60.0)
    print(f"\n── 構圖 ──\n  01 {F01a}→{F01b}\n  03 {F03}\n  04 {F04}\n  05 {F05}\n  06 {F06}\n"
          f"  09 {F09}\n  10 {F10}\n  11 {FN20}→{FN23}\n  13 {F13}")

    # ── 標籤畫面方向偏移（依各鏡迄格的實際方位；看過 SB-鏡頭牆後調） ──
    LAB_POS = {
        # 名稱：(dx, dy) 畫面單位；整組（原文＋中譯兩行）一起推
        "Sarvvis": (6.0, 15.0), "弓": (-40.0, 0.0), "Fávdna": (19.0, 0.0), "Fávdna-左": (-22.0, -14.0), "Boahjenásti": (16.0, -2.0),
        "Sarvvis-近": (0.0, -14.0), "Sarvvis-下": (4.0, -17.0), "銀河-鳥的路": (-17.0, -6.0), "銀河-年的記號": (-17.0, -6.0),
        "跨文化-北斗": (0.0, 0.0), "跨文化-大角星": (12.0, 8.0), "以利亞的車": (-9.0, -13.0),
    }
    for items, name in label_sets:
        if name in LAB_POS:
            dx, dy = LAB_POS[name]
            for it in items:
                it["dx"] = round(it["dx"] + dx, 2)
                it["dy"] = round(it["dy"] + dy, 2)
    # 跨文化北斗：三條垂直堆疊（每條兩行），整疊放在北斗下方
    for i, key in enumerate(["Лось", "Tukturjuit", "Fávdna 的弓"]):
        for it in LB_CROSS:
            if it["key"].split("-zh")[0] == key:
                it["dy"] = round(it["dy"] - 16.0 - i * 8.5, 2)
    # 台北面北：各自放在星群旁的空天區（畫面方向）
    TP_POS = {"Sarvvis": (26.0, 10.0), "Fauna davgge": (6.0, 14.0), "Boahjenásti": (0.0, -8.0),
              "Fávdna": (-24.0, 9.0)}
    for it in LB_TP + LB_TP_F:
        dx, dy = TP_POS[it["key"].split("-zh")[0]]
        it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

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
    m.L_marks([PROCYON, RIGEL, SIRIUS], "Gállá候選圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot"), ([PROCYON, RIGEL, SIRIUS], "Gállá候選圈", "ring")])

    # ════════════════════ 鏡頭 ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="R", sec=10, north=True,
             frames=[F01a, F01b], layers=["鹿", "弓"], labels=ls("Sarvvis", "弓", "Fávdna-左"),
             labels_start=[],
             vo="上週除夕，我們看了朱雀。今晚往北，進北極圈：同一片星空，薩米人看見——一場還沒結束的狩獵。",
             card="同一片星空，薩米人看見——一場還沒結束的狩獵。",
             note="開場字卡；北盤（盤心＝北極星）緩慢逆時針；Sarvvis（琥珀）、弓（綠）、Fávdna 淡入"),
        dict(code="02", kind="R", sec=17, north=True,
             frames=[F01b], layers=["鹿", "弓"], labels=ls("Sarvvis", "弓", "Fávdna-左"),
             overlay="C-A21-01_薩米在哪裡", overlay_layers=["地圖層", "神鼓層"],
             vo="薩米人住在挪威、瑞典、芬蘭的北部，一直到俄羅斯的科拉半島，有些人到今天還在放牧馴鹿。"
                "十七、十八世紀，教會打壓傳統信仰、燒掉大量神鼓，很多星空故事也跟著失傳了。",
             card="神鼓被燒，故事失傳",
             note="畫面不動；定格疊 C-A21-01（地圖 → 神鼓；神鼓是自繪示意、不臨摹館藏）"),
        dict(code="03", kind="R", sec=16, north=True,
             frames=[F01b, F03], layers=["鹿"], labels=ls("Sarvvis"), labels_end=ls("Sarvvis-近"),
             vo="留下來的星座不多，卻都在同一個故事裡。獵物是一頭巨大的鹿，Sarvvis：公馴鹿，也有人說是駝鹿。"
                "牠從仙后座的 W，經過英仙座，一直延伸到御夫座的五車二。",
             card="Sarvvis 公馴鹿",
             note="盤續逆時針、推近仙后—英仙—御夫；Sarvvis 連線（琥珀，15 顆）由仙后往五車二逐段淡入"),
        dict(code="04", kind="R", sec=19, north=True,
             frames=[F03, F04], layers=["鹿"], labels=ls("Sarvvis-近"), labels_end=ls("IAU2025"),
             overlay="C-A21-02_馴鹿回到星圖", overlay_layers=["1736層", "1743層", "2025層"],
             vo="二〇二五年底，國際天文聯合會把英仙座的兩顆星，正式命名為 Sarvvis 和 Áldu：公馴鹿、母馴鹿。"
                "其實將近三百年前，法國的測量隊到拉普蘭量地球的形狀，回去以後就在北極星旁邊畫了一個馴鹿座。",
             card="2025 IAU 正式命名",
             note="推近英仙 δ、ε（白點＋標籤 Sarvvis／Áldu）；迄格定格疊 C-A21-02（1736 → 1743 → 2025，只留年份＋星名）"),
        dict(code="05", kind="R", sec=10, north=True,
             frames=[F04, F05], layers=["鹿", "弓"], labels=ls("Fávdna", "弓"),
             vo="獵人在天空另一頭：大角星，叫 Fávdna。他手上有一把弓，就是北斗七星，弓朝著北方的那頭鹿。",
             card="獵人 Fávdna＝大角星",
             note="盤續逆時針、畫面滑到大角星那一側；弓照 Stellarium：搖光→天璇弓弧、天樞—天璣是箭（不畫勺子）"),
        dict(code="06", kind="R", sec=18, north=True,
             frames=[F05, F06, HAND], layers=["鹿", "弓", "箭"], labels=ls("Fávdna", "弓", "Boahjenásti", "Sarvvis-下"),
             labels_end=[],
             overlay="C-A21-03_不能射的那一箭", overlay_layers=["狩獵層", "箭層"],
             vo="麻煩在中間：北極星。薩米人叫它 Boahjenásti，撐住天空的那顆星。傳說 Fávdna 的箭要是射中它，"
                "天就會塌下來，世界就結束了。所以這把弓每天晚上都拉滿，卻遲遲沒放——這場狩獵，到今天還沒結束。",
             card="射中北極星，世界就結束",
             note="拉遠到整場狩獵（大角星→北斗→北極星→英仙）＋紅色箭頭（天璇→天樞指極線穿過北極星指向仙后）；"
                  "再推進盤心（fov 48、0°＝換組那一格）；迄格定格疊 C-A21-03。"
                  "迄格是盤緣圈內的盤心構圖：07 起格同一格，同框換回長圖"),
        dict(code="07", kind="Z", sec=15, north=True,
             frames=[HAND, DOWN, BELT_F, GEM_F, PLE_F], layers=["幫"],
             labels=ls("Gállá的兒子們", "滑雪的人", "獵犬群"),
             vo="幫手也不少：獵戶座的腰帶，是 Gállá 的兒子們，有個說法是，滑雪板就是他們發明的；"
                "雙子座的兩顆亮星，是兩個滑雪的人；昴宿，是一群獵犬。",
             card="滑雪的人・一群獵犬",
             note="【換組】盤心同框換長圖（06 迄格＝這一格）；沿走廊下來→腰帶（藍）→雙子（紫）→往西到昴宿（獵犬群）；"
                  "旁白每個分號對一段平移"),
        dict(code="08", kind="Z", sec=12, north=True,
             frames=[PLE_F, GAL_F], layers=["幫"], labels=ls("Gállá是誰"), labels_start=ls("獵犬群"),
             overlay="C-A21-07_天狼星貼地平線", overlay_layers=["地平線層", "Kautokeino層"],
             vo="至於 Gállá 本人是哪顆星，說法不一：南河三、參宿七、天狼星都有人說。"
                "不過在挪威北部的薩米地區，天狼星最高只有四度，很難看見。",
             card="Gállá 是誰？說法不一",
             note="滑回南河三、參宿七、天狼星（細圈＋「Gállá？」）；迄格定格疊 C-A21-07（Kautokeino 2/12 20:43 面南，天狼星 4.3°）"),
        dict(code="09", kind="R", sec=11, north=True,
             frames=[HAND, F09M, F09], layers=["鹿"], labels=ls("銀河-鳥的路"), labels_start=[], labels_end=ls("銀河-年的記號"),
             vo="穿過鹿身的銀河，名字會跟著季節換：有時叫「鳥的路」，有時叫「年的記號」，看它在天上的位置，"
                "就知道一年走到哪了。",
             card="鳥的路・年的記號",
             note="【換組】長圖回中心→上到北極→同框換北盤；拉遠＋逆時針；銀河層（L1）在 Canva 把透明度拉高到 60%；"
                  "兩個名字交替（中格鳥的路、迄格年的記號；迄格＝10 起格，由 10 的 labels_start 開年的記號）"),
        dict(code="10", kind="R", sec=17, north=True,
             frames=[F09, F10], layers=["勺", "弓"], labels=ls("跨文化-北斗", "跨文化-大角星"), labels_start=ls("銀河-年的記號"),
             overlay="C-A21-04_同一把北斗",
             vo="同一把北斗，北方的民族各有說法：西伯利亞的獵人說是一頭駝鹿，因紐特人說是馴鹿，到了薩米，"
                "卻是獵人的弓。大角星手上有武器，阿拉伯人也這麼想，叫它「拿長矛的人」。",
             card="北斗：駝鹿、馴鹿、弓",
             note="北斗疊勺形（藍：西伯利亞＝因紐特，Stellarium 連線完全相同）與弓弧＋箭（綠：薩米）；"
                  "大角星標 al-Simāk al-Rāmiḥ；最後疊 9:16 圖卡 C-A21-04（可存圖）"),
        dict(code="11", kind="R", sec=21, north=True, horizon=[PHI],
             frames=[FN20, FN23], layers=["鹿", "弓"], labels=ls("台北面北"),
             labels_end=ls("台北面北", "台北-Fávdna"),
             overlay="C-A21-05_這週末抬頭看",
             vo="這週末在台灣：晚上八點，這頭鹿在西北方半天高，五車二高掛北方；北斗這把弓，從東北方升起。"
                "十點，獵人大角星才從東北東冒出地平線；十一點前後，獵人、弓、北極星和鹿都在天上，"
                "北極星在正中間，只是仙后座已經很低。",
             card="23:00 整場狩獵",
             note=f"台北 2/12 面北（山＝北方地平線，φ 25.03°）；盤逆時針 20:00→23:00"
                  f"（{ROT['20:00']:+.1f}°→{ROT['23:00']:+.1f}°），畫面中心右移跟著大角星；"
                  f"22:01 大角星從右下冒出；迄格疊 9:16 圖卡 C-A21-05（可存圖）"),
        dict(code="12", kind="R", sec=5, north=True, horizon=[PHI],
             frames=[FN23], layers=["鹿", "弓"], labels=ls("台北面北", "台北-Fávdna"),
             overlay="C-A21-06_薩米星名小辭典",
             vo="這集的薩米星名，整理成一張小辭典，可以存起來。",
             card="",
             note="畫面不動；疊 9:16 圖卡 C-A21-06（可存圖；字卡留空）"),
        dict(code="13", kind="R", sec=8, north=True, horizon=[PHI],
             frames=[FN23, F13], layers=["弓", "車"], labels=[], labels_end=ls("以利亞的車"),
             vo="下週五往南，到白俄羅斯：北斗不再是弓，又變回一輛車——先知以利亞那輛著火的車。",
             card="下集見｜白俄羅斯：農民曆星空與以利亞的馬車",
             note="推近北斗；迄格弓（綠）淡出、以利亞的車（琥珀，連線-以利亞的車）淡入；端卡＋追蹤 CTA"),
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

    print("  北盤旋轉角（台北 2/12，面向北方）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  x：北河二 {x_of(S[CASTOR][0]):+.1f}、北河三 {x_of(S[POLLUX][0]):+.1f}、南河三 {x_of(S[PROCYON][0]):+.1f}、"
          f"天狼 {x_of(S[SIRIUS][0]):+.1f}、腰帶 {x_of(S[26311][0]):+.1f}、參宿七 {x_of(S[RIGEL][0]):+.1f}、"
          f"昴宿 {x_of(S[ALCYONE][0]):+.1f}；箭尖 RA {tip[0]:.1f} Dec {tip[1]:+.1f}；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig.strip() + ("" if orig == orig.strip() else f"（{zh}）")] = dict(
            hips=hips if not isinstance(hips, tuple) else [], 原文=orig.strip(), 拼音="", 英文翻譯=en, 中文=zh,
            顏色=col, 來源備註=(f"Stellarium 轉寫 {sc}；" if sc not in ("—", orig.strip()) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV_LINES = LG_ALL + LG_ARROW
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=PREV_LINES,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    # 鏡頭牆：每格只畫該鏡的連線層與標籤層（全部疊在一起會誤判重疊）
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


def sb_wall(m, path, walls, title=""):
    """m.sb_grid 一次只能給一組連線／標籤：這裡每鏡各畫一次再拼起來（每格只看到該鏡實際開的層）"""
    import matplotlib
    matplotlib.use("Agg")
    from PIL import Image
    tmp = []
    for i, (sh, g, labs) in enumerate(walls):
        p = path.replace(".png", f"_tmp{i:02d}.png")
        m.sb_grid(p, [sh], line_groups=g, labels=labs, cols=len(sh["frames"]), title="")
        tmp.append(p)
    ims = [Image.open(p).convert("RGB") for p in tmp]
    cols, cw = 4, max(im.size[0] for im in ims)
    rows = []
    for i in range(0, len(ims), cols):
        rows.append(ims[i:i + cols])
    ch = max(im.size[1] for im in ims)
    W = sum(sorted((im.size[0] for im in ims), reverse=True)[:cols]) + 10 * cols
    out = Image.new("RGB", (W, len(rows) * (ch + 10) + 40), (11, 15, 30))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(out)
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    except Exception:
        fnt = None
    d.text((10, 6), title, fill=(255, 255, 255), font=fnt)
    y = 40
    for r in rows:
        x = 0
        for im in r:
            out.paste(im, (x, y)); x += im.size[0] + 10
        y += ch + 10
    out.save(path)
    for p in tmp:
        os.remove(p)
    print(f"  ✓ {os.path.basename(path)}（{len(walls)} 鏡）")


if __name__ == "__main__":
    build()
