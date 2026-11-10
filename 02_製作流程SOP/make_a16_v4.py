# -*- coding: utf-8 -*-
"""A-16 納瓦荷：只在冬天說的星星故事｜大畫布 v4.6

論點：天空是一本寫著規矩的書（黑神 Haashchʼééshzhiní 用鹿皮袋裡的晶石一顆一顆排好），
郊狼 Máʼii 在書上潑了墨（把剩下的晶石吹上天）；而這本書只在冬天打開（初霜到春雷）。
北火＝北極星；旋轉的男人＝北斗、旋轉的女人＝仙后座，繞著爐火轉＝一家人住在 hooghan 裡；
第一個瘦長的人＝獵戶（冬天、黃昏西沉＝播種）；Dilyéhé＝昴宿（儀式季的時鐘）；
郊狼的星＝老人星（一說）。

來源：Don Childrey《Star Trails: Navajo》（2004；創星故事 pp.29–39、星座 pp.42–73）；
Stellarium navajo（Karrie Berglund，據 Childrey；新舊兩版各 8 個星座）；
天象 PyEphem 自算（台北 25.033°N 121.565°E，UTC+8）。逐字稿：04_腳本庫/A-16-…-v2.md
（2026-11-10 加回刪減：04、13、17 鏡＋01／02／03／07／09／11／16 鏡原句，236 秒）。

連線：
  旋轉的男人／女人 不用 Stellarium 的連線（新版連到 7.5–10 等暗星、新版漏了王良四；
  舊版的男人還帶著大熊座身體的 4–5 等星）：照旁白「七顆」「五顆」只連北斗七星＋仙后 W 五顆亮星。
  第一個瘦長的人、Dilyéhé、眺望的人、兔子的足跡：Stellarium 新版（與舊版相同或只差肉眼看不到的星）。
  第一個高大的人：舊版（新版多了 80248、80840、80862 等 7 等以下暗星）。
  Lizard（蜥蜴，仙女—英仙）Childrey 書裡沒有、出處不明：本集不畫（L4 總層＝7 個星座）。

鏡頭路線：01 長圖獵戶拉遠 → 02–06 定格概念圖（冬天才說、版本說明、黑神的晶石）→ 07【換北盤】北火（金樁、引路的星）
→ 08 旋轉的男人／女人 → 09 繞火（hooghan 輪廓）→【換長圖】10 瘦長的人 → 11 快捲到天蠍（第一個高大的人）再回獵戶西沉＝播種
→ 12 昴宿 Dilyéhé → 13 拉遠：銀河＝等待黎明的 → 14 郊狼（概念圖）→ 15 整片星空＋全部連線 → 16 沿走廊往南到老人星
→ 17 回整片星空：規矩與混亂（概念圖）→ 18【換北盤】台北 1/8 21:00→23:00 面北 → 19【換長圖】天狼＋老人星、圖卡、推到昴宿收尾。

參數
  lst = 100 → 走廊（x=0）＝RA 100：天狼 x −1.3、老人星 +4.0 都在走廊上（16 鏡 T 直接往南）；
             獵戶 x +11…+21、畢宿五 +31、昴宿 +43（全部在長圖帶）。
             選 100 而不是 85（獵戶置中）是為了 18 鏡：rot＝(lst−LST台北)%360−180，
             1/8 21:00 LST 64.4 → −144.4°、23:00 LST 94.5 → −174.5°，整段在 (−180,180] 內單向逆時針；
             lst=85 時 23:00 會變成 −189°（＝+171°），Canva 讀成另一邊（v4.6 第四節）。
  D_s = 45、D_r = 49 → 北斗最南的搖光 +49.31 在北盤本體；仙后、北極星在北盤；
             昴宿 +24、獵戶、天狼 −16.7 在長圖帶；老人星 −52.7 在南盤本體。（逐字稿 v1 建議值）
  D_fill = −27 → k=1.3975、R_fill=163.51（盤寬 ÷ 畫布寬＝0.908）：18 鏡台北面北 fov 124
             （北斗在東北、仙后在西北，兩邊都要進畫面）、畫面中心在北極星上方 38.6 單位
             （地平線北點 kφ＝35.0 → Y≈1600），角落距盤心 160.9 < 163.0。
             |x_t|＋R_fill＝163.5 ≤ 180 ✓
  x_tN = x_tS = 0

check_shots 的 ⚠（判斷後接受）
  07–09、18「畫面含長圖側扇區」：R 鏡頭全程在北盤圖層組上；長圖⇄北盤的換組只發生在
  gen_canva_pages 插的「長圖轉北盤／北盤轉長圖」頁（盤心置中、0°、fov 48／40，在盤緣圈內逐點重合），
  不會從 fov 124 的格子直接切回大畫布。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-16"
OUT = os.path.join(BASE, "05_素材/A-16_納瓦荷/_v4大畫布")
LST0 = 100.0
TPE = (25.0330, 121.5654)
PHI = 25.03                     # 18 鏡台北面北的地平線緯度


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


T_TPE = {"21:00": "2027/1/8 21:00", "22:00": "2027/1/8 22:00", "23:00": "2027/1/8 23:00"}
ROT = {k: rot_at(v) for k, v in T_TPE.items()}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS = 11767
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN = 746, 3179, 4427, 6686, 8886
BETELGEUSE, BELLATRIX, RIGEL, SAIPH = 27989, 25336, 24436, 27366
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
ALCYONE, ALDEBARAN, SIRIUS, CANOPUS, PROCYON = 17702, 21421, 32349, 30438, 37279
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
CAS_W = [CAPH, SCHEDAR, NAVI, RUCHBAH, SEGIN]
ORION = [BETELGEUSE, BELLATRIX, RIGEL, SAIPH, MINTAKA, ALNILAM, ALNITAK]
PLEIADES = [17702, 17847, 17851, 17608, 17499, 17531]
MAINS = [POLARIS] + DIPPER + CAS_W + ORION + [ALCYONE, SIRIUS, CANOPUS]


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_nv(path):
    d = json.load(open(os.path.join(path, "navajo", "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["common_name"]["english"]] = [s for s in segs if len(set(s)) >= 2]
    return out


NV, NV_OLD = load_nv(SC_NEW), load_nv(SC_OLD)

SEG_MALE = [[DUB, MER, PHE, MEG, DUB], [MEG, ALI, MIZ, ALK]]      # 北斗七星
SEG_FEMALE = [[SEGIN, RUCHBAH, NAVI, SCHEDAR, CAPH]]               # 仙后 W
SEG_SLIM = NV["First Slim One"]                                    # 獵戶（新舊相同）
SEG_DIL = NV["Dilyehe"]                                            # 昴宿
SEG_FEET = NV["Man with Feet Apart"]                               # 烏鴉座一帶
SEG_BIG = NV_OLD["First Big One"]                                  # 天蠍頭＋蛇夫（舊版：無暗星）
SEG_RAB = NV["Rabbit Tracks"]                                      # 天蠍尾

LG_HOME = [(SEG_MALE, "amber", 1.0), (SEG_FEMALE, "green", 1.0)]
LG_SLIM = [(SEG_SLIM, "blue", 1.0)]
LG_DIL = [(SEG_DIL, "amber", 1.0)]
LG_ALL = (LG_HOME + LG_SLIM + LG_DIL +
          [(SEG_FEET, "purple", 0.9), (SEG_BIG, "red", 0.9), (SEG_RAB, "purple", 0.9)])
LINE_SETS = [(LG_HOME, "連線-旋轉的男女"), (LG_SLIM, "連線-瘦長的人"), (LG_DIL, "連線-Dilyéhé")]
LINES_KEY = {"L4": "星座連線", "家": "連線-旋轉的男女", "瘦": "連線-瘦長的人", "昴": "連線-Dilyéhé"}
LINE_GROUPS = {"L4": LG_ALL, "家": LG_HOME, "瘦": LG_SLIM, "昴": LG_DIL}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


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
#   (錨點 HIP 群, 原文（片中寫法）, Childrey 拼法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ([POLARIS], "Náhookǫs Bikǫʼ", "North Fire（只寫英文）", "North Fire", "北火（北極星）", "amber",
     "Childrey pp.33、44：唯一不動的星，其他的星都繞著它；納瓦荷語寫法取自迪內族天文課程（另作 Náhookòs Bikò'）"),
    (DIPPER, "Náhookǫs Bikąʼ", "Náhookǫs bikąʼii", "Revolving Male", "旋轉的男人（北斗）", "amber",
     "Childrey pp.33、44–47：七顆、躺在火邊的男人；連線只連北斗七星（Stellarium 新版連到 8–9 等暗星）"),
    (CAS_W, "Náhookǫs Baʼáadii", "Náhookǫs baʼáadii", "Revolving Female", "旋轉的女人（仙后座）", "green",
     "Childrey pp.33、48–51：五顆、對面的女人；連線只連 W 五顆亮星（Stellarium 新版漏了王良四）"),
    (ORION, "ʼAtséʼetsʼózí", "ʼÁtséʼetsʼózí", "First Slim One", "第一個瘦長的人（獵戶）", "blue",
     "Childrey pp.36、58–61：冬天的人；五月初黃昏西沉＝種玉米、豆、南瓜、菸草；月份的守護者"),
    (PLEIADES, "Dilyéhé", "Dilyéhé", "Dilyehe", "昴宿", "amber",
     "Childrey pp.37、54–57：照黑神太陽穴上那團晶石做的七顆；十月中黃昏東升＝儀式季開始，春雷＝結束"),
    ([CANOPUS], "Máʼii Bizǫʼ", "Mąʼii bizǫ", "Coyote Star", "郊狼的星（老人星？）", "red",
     "Childrey p.72：「可能是老人星」；又叫「沒有月份的星」；IAU astro4edu、Navajo Skies 也作老人星——片中「很多人認為」"),
    ([SIRIUS], "天狼星", "—", "Sirius", "天狼星", "white", "19 鏡：台北 1/8 23:00 47.7°（方位 170°）"),
    ([59199, 59316, 60965, 61359], "Hastiin Sikʼaiʼí", "Hastiin Sikʼaiʼí", "Man with Feet Apart",
     "雙腳張開的人（烏鴉座）", "purple", "Childrey pp.34、52–53：東方眺望的人（本集只在 L4 總層）"),
    ([79593, 78401, 78265, 78104], "ʼAtséʼetsoh", "ʼÁtséʼetsoh", "First Big One", "第一個高大的人（天蠍＋蛇夫）",
     "red", "Childrey pp.35、62–65：夏天的人；與瘦長的人成對（11 鏡快捲帶過＋L4 總層，連線用舊版）"),
    ([85927, 86670, 87073, 85696], "Gah Heetʼeʼii", "Gah heetʼeʼii", "Rabbit Tracks", "兔子的足跡（天蠍尾）",
     "purple", "Childrey pp.35、66–67：獵人不在母羚羊生產時打獵（本集只在 L4 總層）"),
    ((96.0, 8.0), "Yikáísdáhí", "Yikáísdáhí", "Awaiting the Dawn", "等待黎明的（銀河）", "white",
     "Childrey p.38：黑神抓起千萬顆細晶石一揮＝銀河（13 鏡；錨點在麒麟—雙子之間的銀河上）"),
]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-27,
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

    T = {t[1]: t for t in TERMS}

    def term(name, dx, dy, disc=False, s1=1.6, s2=1.2, gap=2.4, zh_only=False):
        a, orig, _, _, zh, col, _ = T[name]
        if zh_only:
            return [item(a, zh, col, s1, dx, dy, name, disc)]
        return [item(a, orig, col, s1, dx, dy + gap / 2, name, disc),
                item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh", disc)]

    # ── 北盤（R 鏡頭 fov 124）：字不跟著盤轉，dx/dy＝畫面方向 ──
    RS = dict(s1=3.9, s2=3.2, gap=4.3)
    LB_FIRE = term("Náhookǫs Bikǫʼ", 0.0, -7.0, **RS)
    # 故事段（07–09，rot −20…−110）：位置看 對位參考/ 逐頁調過
    LB_MALE = term("Náhookǫs Bikąʼ", 0.0, -12.0, **RS)
    LB_FEMALE = term("Náhookǫs Baʼáadii", 0.0, 11.0, **RS)
    # 台北面北（18，rot −144…−175）：三組都擠在地平線上方 → 北斗、仙后的字都放上方（北斗的字略偏左）、北火的字放左邊（逐頁對位參考看過 21:00、23:00 兩格）
    RT = dict(s1=3.0, s2=2.6, gap=3.4)            # 三組擠在一起：字縮到 Canva 下限附近
    LB_FIRE_T = term("Náhookǫs Bikǫʼ", -17.0, 1.5, **RT)
    LB_MALE_T = term("Náhookǫs Bikąʼ", -10.0, 24.0, **RT)
    LB_FEMALE_T = term("Náhookǫs Baʼáadii", 4.0, 15.0, **RT)
    # ── 長圖 ──
    LB_SLIM = term("ʼAtséʼetsʼózí", 2.0, -13.0)
    LB_DIL = term("Dilyéhé", 0.0, -4.0)
    LB_COY = term("Máʼii Bizǫʼ", 0.0, -4.2)
    LB_SIR = term("天狼星", 3.0, -2.6, zh_only=True, s1=1.4)
    LB_ALL = (term("ʼAtséʼetsʼózí", 2.0, -13.0, s1=1.4, s2=1.05) + term("Dilyéhé", 0.0, -4.0, s1=1.4, s2=1.05)
              + term("Hastiin Sikʼaiʼí", 0.0, -9.0, s1=1.4, s2=1.05)
              + term("ʼAtséʼetsoh", 0.0, 15.0, s1=1.4, s2=1.05)
              + term("Gah Heetʼeʼii", 0.0, -5.0, s1=1.4, s2=1.05))

    # ── v2 加回（排在最後：前面各層的 L 編號、Canva 媒體 ID 不變）──
    LB_CROSS = [item([POLARIS], "蒙古：金樁", "white", 3.0, -17.0, 11.0, "北火-金樁"),
                item([POLARIS], "北歐：引路的星", "white", 3.0, 17.0, 11.0, "北火-引路")]   # 07 鏡迄格（rot −20）
    LB_BIG = term("ʼAtséʼetsoh", 0.0, 22.0)                                             # 11 鏡中格（天蠍）
    LB_MW = term("Yikáísdáhí", 6.0, 8.0)                                                # 13 鏡迄格（銀河）

    label_sets = [(LB_FIRE, "北火"), (LB_MALE, "旋轉的男人"), (LB_FEMALE, "旋轉的女人"),
                  (LB_FIRE_T, "北火-台北"), (LB_MALE_T, "旋轉的男人-台北"), (LB_FEMALE_T, "旋轉的女人-台北"),
                  (LB_SLIM, "瘦長的人"), (LB_DIL, "Dilyéhé"), (LB_COY, "郊狼的星"),
                  (LB_SIR, "天狼星"), (LB_ALL, "七個星座"),
                  (LB_CROSS, "北火-跨文化"), (LB_BIG, "第一個高大的人"), (LB_MW, "等待黎明的")]

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
    can = m.pos_primary(*S[CANOPUS][:2])
    sir = m.pos_primary(*S[SIRIUS][:2])

    def FN(t):                                   # 台北面北：畫面中心在北極星上方 38.6 單位，地平線北點 Y≈1600
        return (0.0, round(yp + 38.6, 2), 124.0, ROT[t])

    def ST(rot):                                 # 故事段：盤心置中（北斗最外的搖光 r=57，fov 124 半寬 62 放得下）
        return (0.0, round(yp, 2), 124.0, rot)

    HAND = (0.0, round(yp, 2), 48.0, 0.0)        # 長圖⇄北盤同框換組
    ORI0 = (16.0, 0.0, 24.0, 0.0)
    WIDE = (20.0, 0.0, 50.0, 0.0)                # 整片冬季星空：天狼 x −1、獵戶、畢宿五、昴宿 +43
    WIDE_N = (20.0, 4.0, 44.0, 0.0)              # 04 鏡：往北緩推再退回（|cy|+hh＝43.1 ≤ 45）
    ORIGIN = (0.0, 0.0, 48.0, 0.0)               # 下移回到的出發點（07 的「回中心」）
    ORI1 = (16.0, 0.0, 40.0, 0.0)
    ORI2 = (6.0, -2.0, 40.0, 0.0)                # 畫面往東移＝獵戶往西（右）沉
    PLE = (36.0, 14.0, 34.0, 0.0)                # |cy|+hh＝44.2 ≤ 45
    BIG = (-140.0, -9.0, 40.0, 0.0)              # 11 鏡中格：第一個高大的人（天蠍頭＋蛇夫，RA 240 → x −140）
    SOUTH0 = (0.0, -4.0, 48.0, 0.0)
    CAN = (0.0, round(can[1] + 8.0, 2), 40.0, 0.0)
    SC = (0.0, round((sir[1] + can[1]) / 2, 2), 48.0, 0.0)   # 天狼＋老人星同框

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=13, north=True,
             frames=[ORI0, WIDE], layers=["瘦"], labels=[],
             vo="上週，我們跟著獵戶腰帶繞了地球一圈。今天到美國西南的沙漠高原，納瓦荷人的家：同一片星空，"
                "納瓦荷人看見——郊狼撒了一地的星星。",
             card="同一片星空，納瓦荷人看見——郊狼撒了一地的星星。",
             note="開場字卡；從獵戶（第一個瘦長的人，藍）拉遠到整片冬季星空"),
        dict(code="02", kind="Z", sec=13, north=True,
             frames=[WIDE], layers=[], labels=[],
             overlay="C-A16-01_冬天才說的故事", overlay_layers=["日曆環層", "今天層", "睡層"],
             vo="開始之前，先說一件事。納瓦荷的長輩說：天上的故事，只在冬天講——從秋天第一次結霜，到春天第一聲雷。"
                "今天是一月，正好在故事的季節裡。",
             card="初霜到春雷",
             note="畫面不動；定格疊 C-A16-01（日曆環 → 今天 → 睡）：「睡」層對 03 鏡旁白，"
                  "三層一路疊到 03 結束（03 是同一格，不另疊）"),
        dict(code="03", kind="Z", sec=13, north=True,
             frames=[WIDE], layers=[], labels=[],
             vo="如果你在夏天才滑到這支影片，可以先收藏，等天冷了再回來聽。為什麼？一種說法是："
                "冬天蛇和蜘蛛都睡了，雷也不打，故事不會驚動它們。",
             card="夏天看到？先收藏",
             note="同 02 的畫面；C-A16-01 睡層（蛇、蜘蛛、閃電＋月亮）在 02 的概念圖頁；右上角書籤圖示輕跳一下"),
        dict(code="04", kind="Z", sec=10, north=True,
             frames=[WIDE, WIDE_N, WIDE], layers=[], labels=[],
             vo="這個故事，每個家族、每種儀式都有不同的版本；我們講的，是一本公開出版的書裡整理的那一個。",
             card="版本很多，這是其一",
             note="v2 加回；長圖往北緩推再退回原格（05–06 的格不變）；角落小字「Childrey 2004，依 Nightway 傳統」"),
        dict(code="05", kind="Z", sec=13, north=True,
             frames=[WIDE], layers=[], labels=[],
             overlay="C-A16-02_黑神的晶石",
             overlay_layers=["hooghan層", "腳踝層", "膝層", "腰層", "肩層", "太陽穴層"],
             vo="很久以前，神聖的人們在第一座泥土屋 hooghan 裡造世界，用彩色的沙畫出大地母親、"
                "天空父親。白天有了太陽，夜裡的天空卻一片黑。",
             card="大地母親・天空父親",
             note="畫面不動；定格疊 C-A16-02：hooghan 層對 05 旁白，腳踝→膝→腰→肩→太陽穴五層對 06 旁白"
                  "（06 是同一格，不另疊）；不畫人形、不用沙畫"),
        dict(code="06", kind="Z", sec=15, north=True,
             frames=[WIDE], layers=[], labels=[],
             vo="黑神走了進來，腳踝上掛著一小團閃亮的晶石。他跺一下腳，晶石跳到膝蓋；再跺，跳到腰、跳到肩膀，"
                "最後停在他的太陽穴上。大家問：那是什麼？他說：這叫星星。",
             card="這叫星星",
             note="同 05 的畫面；晶石五層在 05 的概念圖頁"),
        dict(code="07", kind="R", sec=14, north=True,
             frames=[HAND, ST(-20.0)], layers=[], labels=ls("北火", "北火-跨文化"),
             labels_start=[],                     # 起格 fov 48：字太大會被左緣切掉，拉遠後才開
             vo="黑神打開一個鹿皮袋，先拿出一顆，放在北方：北火。「只有它不動，其他的星都要繞著它走。」"
                "蒙古人說它是金樁，北歐人說它引路；在納瓦荷，它是一盆爐火。",
             card="北火：唯一不動的星",
             note="【換北盤】長圖回中心、沿走廊上到北極（同框換組）；拉遠到 fov 124、盤逆時針轉 20°；"
                  "迄格北火兩側疊跨文化小標（蒙古：金樁／北歐：引路的星，v2 加回）。迄格含長圖側扇區（check_shots ⚠）可接受：換組在 fov 48、0° 的起格（＝逐頁表「長圖轉北盤」頁）"),
        dict(code="08", kind="R", sec=13, north=True,
             frames=[ST(-20.0), ST(-50.0)], layers=["家"], labels=ls("北火", "旋轉的男人", "旋轉的女人"),
             labels_start=ls("北火", "北火-跨文化"),     # 07 迄格＝08 起格：跨文化小標在 07 淡入、08 淡出
             vo="他在北火旁邊擺了七顆：一個躺在火邊的男人，叫 Náhookǫs Bikąʼ，「旋轉的男人」，就是北斗；"
                "對面再擺五顆，一個女人：「旋轉的女人」，就是仙后座。",
             card="旋轉的男人・旋轉的女人",
             note="盤繼續逆時針轉；旋轉的男人（琥珀，北斗七星）先淡入，再淡入旋轉的女人（綠，仙后 W 五顆）"),
        dict(code="09", kind="R", sec=12, north=True,
             frames=[ST(-50.0), ST(-110.0)], layers=["家"], labels=ls("北火", "旋轉的男人", "旋轉的女人"),
             overlay="C-A16-hooghan",
             vo="兩個人繞著火爐轉，就像一家人住在圓圓的 hooghan 裡，爐火在正中央。"
                "他們提醒人要顧好家：兩對夫妻，不該共用一個爐火。",
             card="一個家，一盆火",
             note="盤再轉 60°（兩個人明顯繞火）；迄格定格疊 C-A16-hooghan_透明.png（1080×1920 滿版，"
                  "八角形 hooghan 輪廓圓心＝畫面中心＝北極星，門朝東）；v2 加回「兩對夫妻」一句（岳母一句不加回）"),
        dict(code="10", kind="S", sec=12, north=True,
             frames=[ORIGIN, ORI1], layers=["瘦"], labels=ls("瘦長的人"),
             vo="黑神又在西邊放了一個瘦長的人：ʼAtséʼetsʼózí，「第一個瘦長的人」，就是獵戶。"
                "他只在冬天的夜裡出現——那是食物少、人都變瘦的季節。",
             card="第一個瘦長的人",
             note="【換長圖】盤轉回 0°、同框換回長圖、沿走廊下到出發點（＝07 上移的倒放）→ 滑到獵戶"),
        dict(code="11", kind="S", sec=14, north=True,
             frames=[ORI1, BIG, ORI2], layers=["瘦", "L4"],
             labels_start=ls("瘦長的人"), labels=ls("第一個高大的人"), labels_end=ls("瘦長的人"),
             overlay="C-A16-06_播種", overlay_layers=["地平線層", "作物層"],
             vo="天空另一邊，夏天的天蠍，是「第一個高大的人」；一個升起，另一個就落下。"
                "五月初，黃昏時看見瘦長的人沉向西方，就該種玉米、豆子、南瓜和菸草了。",
             card="他沉向西方＝播種",
             note="v2 加回前半：快捲往東（左）約 156° 到天蠍（第一個高大的人，紅，L4 總層裡的那段）再捲回獵戶；"
                  "後半畫面往東（左）移＝獵戶往西（右）沉；迄格定格疊 C-A16-06（西方地平線＋玉米、豆、南瓜、菸草）"),
        dict(code="12", kind="S", sec=15, north=True,
             frames=[ORI2, PLE], layers=["昴"], labels=ls("Dilyéhé"),
             overlay="C-A16-01_冬天才說的故事", overlay_layers=["日曆環層", "昴宿層"],
             vo="接著，黑神照著太陽穴上那團晶石，做了七顆小的放上天：Dilyéhé，昴宿。秋天黃昏它從東方升起，"
                "冬天的儀式就開始；春雷一響就結束——正好是說故事的季節。",
             card="昴宿＝儀式的時鐘",
             note="往右上（西北）滑到昴宿；Dilyéhé（琥珀）；迄格定格疊回 C-A16-01（日曆環＋昴宿層）"),
        dict(code="13", kind="Z", sec=7, north=True,
             frames=[PLE, WIDE], layers=["昴"], labels_start=[], labels=ls("等待黎明的"),
             vo="最後，他抓起一大把細碎的晶石，一揮手，撒過整片天：「等待黎明的」，銀河。",
             card="等待黎明的",
             note="v2 加回；拉遠回整片星空，L1 銀河層由暗轉亮（不透明度 40%→100%，從御夫、雙子一路到麒麟）；迄格標籤 Yikáísdáhí"),
        dict(code="14", kind="Z", sec=11, north=True,
             frames=[WIDE], layers=["昴"], labels=ls("等待黎明的"),   # 13 迄格＝14 起格：銀河標籤在這頁
             overlay="C-A16-03_郊狼吹散星星", overlay_layers=["郊狼層", "吹散層"],
             vo="黑神正要休息，郊狼 Máʼii 晃了過來：「你們在做什麼？怎麼沒問我！」他一把搶過鹿皮袋，"
                "呼——把剩下的晶石，全吹上了天。",
             card="郊狼搶走了鹿皮袋",
             note="畫面不動（13 已拉遠到整片星空）；定格疊 C-A16-03（郊狼剪影 → 袋口噴出的星點）"),
        dict(code="15", kind="Z", sec=12, north=True,
             frames=[WIDE], layers=["L4"], labels=ls("七個星座"),
             overlay="C-A16-04_規矩與混亂", overlay_layers=["混亂層", "規矩層"],
             vo="所以天上大部分的星，都沒有名字，亂成一片。黑神罵他：這樣人們更難找到我們放的規矩了。"
                "郊狼笑著說：「可是，天空變漂亮了啊！」",
             card="「可是天空變漂亮了！」",
             note="全部連線（L4＝7 個星座；畫面內看得到瘦長的人、Dilyéhé）淡入；定格疊 C-A16-04（混亂 → 規矩）"),
        dict(code="16", kind="T", sec=15, north=False,
             frames=[SOUTH0, CAN], layers=[], labels=ls("郊狼的星"),
             overlay="C-A16-07_郊狼的星", overlay_layers=["地平線層", "WindowRock層", "台北層"],
             vo="袋子裡還剩一顆。郊狼把它放到很南的地方：「這是我的星。」很多人認為，就是老人星："
                "在納瓦荷的家鄉，它最高離地平線不到兩度，只在冬夜貼著南方露一下臉。",
             card="郊狼的星＝老人星？",
             note="沿走廊往南到老人星（南盤本體 dec −52.7）；迄格定格疊 C-A16-07（Window Rock 最高 1.6° vs 台北 12.3°）"),
        dict(code="17", kind="Z", sec=9, north=True,
             frames=[CAN, WIDE], layers=["L4"], labels_start=[], labels=ls("七個星座"),
             vo="一邊是黑神排好的規矩，一邊是郊狼撒出來的混亂。納瓦荷人說，世界本來就是這兩樣的平衡。",
             card="規矩與混亂的平衡",
             note="v2 加回；從老人星沿走廊回到整片星空，七個星座的連線（規矩）亮在滿天亂星（混亂）裡；"
                  "C-A16-04 留在 15 鏡（Canva 已排），這裡不再疊"),
        dict(code="18", kind="R", sec=11, north=True, horizon=[PHI],
             frames=[FN("21:00"), FN("23:00")], layers=["家"],
             labels=ls("北火-台北", "旋轉的男人-台北", "旋轉的女人-台北"),
             vo="今晚剛好新月。十一點往北看：北斗剛從東北爬上來、仙后座在西北，中間是北極星——"
                "旋轉的男人和女人，正繞著北火轉。",
             card="今晚十一點，往北看",
             note=f"【換北盤】台北 1/8 面北（山＝北方地平線，φ 25.03°）；盤逆時針 21:00→23:00"
                  f"（{ROT['21:00']:+.1f}°→{ROT['23:00']:+.1f}°）。起格切點 ⚠ 可接受：換組由逐頁表的「長圖轉北盤」"
                  f"橋接頁做（盤心置中、0°），18 起格是新構圖"),
        dict(code="19", kind="Z", sec=14, north=True,
             frames=[SC, PLE], layers=["昴"], labels=ls("天狼星", "郊狼的星"), labels_end=ls("Dilyéhé"),
             overlay="C-A16-05_今晚十一點", overlay_at="start",
             vo="回頭往正南，天狼星下面低低的那顆，就是郊狼的星；在台北，它有十二度高。"
                "下週五，到北方大平原的黑腳族：他們把北斗和昴宿，畫在帳篷頂上。",
             card="下集見｜黑腳族：留在天上的六個孩子",
             note="【換長圖】往南：天狼＋老人星同框；起格後疊 9:16 圖卡 C-A16-05（可存圖）；"
                  "最後推到昴宿（北斗在北盤，長圖上推不到：只推昴宿）；端卡＋追蹤 CTA"),
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

    print("  北盤旋轉角（台北 1/8，面向北方）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  x：參宿四 {x_of(S[BETELGEUSE][0]):+.1f}、參宿七 {x_of(S[RIGEL][0]):+.1f}、昴宿 {x_of(S[ALCYONE][0]):+.1f}、"
          f"天狼 {x_of(S[SIRIUS][0]):+.1f}、老人 {x_of(S[CANOPUS][0]):+.1f}；老人星畫布 {can}、天狼 {sir}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips, 原文=orig, 拼音="", 英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Childrey 拼法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI},
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
