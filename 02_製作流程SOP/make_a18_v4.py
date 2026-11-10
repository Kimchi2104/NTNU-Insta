# -*- coding: utf-8 -*-
"""A-18 古埃及：叫醒尼羅河的天狼星｜大畫布 v4.6

論點：北方是永不落下、拴住混亂的天（Meskhetyu 牛的前腿＝北斗，拴在繫船柱上，由河馬看守；
「不知毀滅的星」）；南方是會消失又回來的天（Sopdet＝天狼星消失約七十天後晨出，河水上漲、新年開始）。
365 天沒有閏年的曆法每四年差一天；金字塔時代孟斐斯的晨出在夏至後幾天（公曆 6/28–29），
2027 年開羅要到 8/5–6——晚了一個多月；1970 年亞斯文高壩完工後，河也不漲了。

來源：Stellarium egyptian（Karrie Berglund 依 Belmonte〈A Map of the Ancient Egyptian Firmament〉；
28 個星座只有英文名，連線是 Belmonte 依圖像重建）；逐字稿 v2 的「星空對時」（PyEphem 自算）。
逐字稿：04_腳本庫/A-18-…-v2.md（2026-11-10 加回刪減：06、09、13、16 鏡＋02、14、15 鏡原句，236 秒）。

鏡頭路線：長圖（獵戶＋天狼星）推近天狼星 → 定格概念圖（尼羅河的一年、消失與晨出、曆法的漂移、
一千四百六十年、晚了一個多月、河已經不等了）→ 往西捲到獵戶（Sah 與 Sopdet）→ 往東捲（旬星＝星星時刻表）→【自動換組】北盤：牛的前腿、繫船柱、河馬，
北盤逆時針轉 → 北面的入口、對正北（推測）、拉繩定位（概念圖）→【自動換組】長圖：丹德拉星圖（美宣另尋授權圖）、
以為有好幾千年（1799→1822 年表）、兩千五百年（年表）→ 今晚十點半（台北 1/22，圖卡）→ 沿走廊往南到老人星（下集預告：古阿拉伯）。

參數
  lst = 101.3 → 天狼星（RA 101.28）在走廊 x=0；獵戶腰帶 x≈+16、參宿四 +12.5、參宿七 +22.7；
             老人星 x≈+4.8（在南盤盤緣圈內，r=52.1＜57.3），所以 19 鏡用 T 沿走廊往南就到得了。
  D_s = 45、D_r = 49 → Sah（dec −35.5…+7.4）、天狼星 −16.7 都在帶內；北斗（+49.3…+61.8）整組 ≥ D_r。
             北盤是今天的星空（逐字稿 v1：不畫今天的拱極圈）；不設地平線（12 鏡講的是「那時」的北天）。
  D_fill = −35 → k=1.397、R_fill=174.68（盤寬 ÷ 畫布寬 ＝ 0.970457）；|x_t|+R_fill=174.7 ≤ 180 ✓。
             北盤 R 鏡頭用 fov 140：繫船柱的大角（dec +19.2，r=99）與河馬（dec +19…+52）都在填滿圓內。
  x_tN = x_tS = 0
  北盤旋轉：11 鏡 0°（換組那格）→ 拉遠；12 鏡 0°→−60°（逆時針＝時間往前，約 4 小時；畫面中心在北極左邊 40 單位，
             轉到 −90° 以上繫船柱、河馬會沉到山的剪影後面，所以只轉 60°；
             單段 < 180°，Canva M&M 不會反轉）；14 鏡停在 −60° 疊拉繩概念圖；
             之後 gen_canva_pages 自動補「北盤轉長圖-歸位」（盤轉回 0°）再同框換回長圖——與 A-15 同做法。
  check_shots 對 11–14 的 ⚠（起迄格含長圖側扇區）：前後都由 gen_canva_pages 自動補換組頁
             （fov 40 回到盤心再同框換組），不會從 fov 140 的大框直接切回大畫布——可接受。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-18"
OUT = os.path.join(BASE, "05_素材/A-18_古埃及/_v4大畫布")
LST0 = 101.3

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SIRIUS, CANOPUS, PROCYON = 32349, 30438, 37279
BETELGEUSE, BELLATRIX, RIGEL, SAIPH = 27989, 25336, 24436, 27366
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BELT = [MINTAKA, ALNILAM, ALNITAK]
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
ARCTURUS, ETA_BOO = 69673, 67927
THUBAN, POLARIS, VEGA = 68756, 11767, 91262
MAINS = [SIRIUS, CANOPUS, BETELGEUSE, RIGEL, BELLATRIX, SAIPH] + BELT + DIPPER + \
        [ARCTURUS, ETA_BOO, THUBAN, POLARIS]


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium egyptian：Belmonte 重建；28 個星座只有英文名）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
EG = {}
for c in json.load(open(os.path.join(SC_NEW, "egyptian", "index.json"), encoding="utf-8"))["constellations"]:
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    EG[c["common_name"]["english"]] = [s for s in segs if len(set(s)) >= 2]

SEG_LEG = EG["Bull's Foreleg"]          # 001 北斗
SEG_POST = EG["Mooring Post"]           # 023 搖光—牧夫 η—大角
SEG_HIPPO = EG["Hippopotamus"]          # 017 天龍—武仙—北冕一帶
SEG_SAH = EG["Sah"]                     # 005 獵戶（延伸到天兔、天鴿）
MAIN_NAMES = ("Bull's Foreleg", "Mooring Post", "Hippopotamus", "Sah")

LG_LEG = [(SEG_LEG, "amber", 1.1)]
LG_POST = [(SEG_POST, "green", 1.0)]
LG_HIPPO = [(SEG_HIPPO, "red", 1.0)]
LG_SAH = [(SEG_SAH, "blue", 1.0)]
LG_OTHER = [(segs, "purple", 0.7) for nm, segs in EG.items() if nm not in MAIN_NAMES]
LG_ALL = LG_LEG + LG_POST + LG_HIPPO + LG_SAH + LG_OTHER
LINE_SETS = [(LG_LEG, "連線-牛的前腿"), (LG_POST, "連線-繫船柱"), (LG_HIPPO, "連線-河馬"),
             (LG_SAH, "連線-Sah")]
LINES_KEY = {"L4": "星座連線", "腿": "連線-牛的前腿", "柱": "連線-繫船柱", "馬": "連線-河馬",
             "獵": "連線-Sah"}
LINE_GROUPS = {"L4": LG_ALL, "腿": LG_LEG, "柱": LG_POST, "馬": LG_HIPPO, "獵": LG_SAH}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(segs):
    return sorted({h for s in segs for h in s})


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
            n += max(1, len(re.findall(r"[aeiouyāēīōū]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、名詞總表（＝標籤對照表；給組員直接複製貼上）
#   (錨點 HIP 群, 原文（埃及學常用拼法）, 轉寫, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ([SIRIUS], "Sopdet", "spdt", "Sirius (Sothis)", "天狼星", "amber",
     "埃及學通用名（希臘文 Sothis）；Stellarium egyptian 只寫英文 Sirius"),
    (BELT + [BETELGEUSE, RIGEL], "Sah", "sꜣḥ", "Orion", "獵戶", "blue",
     "Stellarium egyptian 005 Sah（Belmonte：延伸到天兔、天鴿）；後與歐西里斯合一"),
    (DIPPER, "Meskhetyu", "msḫtjw", "Bull's Foreleg", "牛的前腿（北斗）", "amber",
     "Stellarium egyptian 001；賽特的腿；「開口儀式」的錛子也叫這個名字（Roth 1993，JEA 79）"),
    ([ALK, ETA_BOO, ARCTURUS], "Mooring Post", "—", "Mooring Post", "繫船柱", "green",
     "Stellarium egyptian 023（大角＋牧夫 η＋搖光）；Stellarium 只有英文名，片中不唸原文"),
    (uniq(SEG_HIPPO), "Hippopotamus", "rrt（一說）", "Hippopotamus", "河馬（女神）", "red",
     "Stellarium egyptian 017（天龍—武仙—北冕一帶）；女神名 Reret／Taweret 為一說，片中只說「化身河馬的女神」"),
    ([POLARIS], "ikhemu-sek", "jḫmw-sk", "the Imperishable Stars", "不知毀滅的星", "white",
     "金字塔經文：拱極星；錨點放在北天極（字放在盤心上方），不是指北極星"),
    ([CANOPUS], "Canopus", "—", "Canopus", "老人星", "white", "下集預告（古阿拉伯 Suhayl）；Stellarium egyptian 無埃及名"),
]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-35,
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

    def term(name, dx, dy, disc=False, s1=1.5, s2=1.1, gap=2.3, anc=None):
        a, orig, _, _, zh, col, _ = T[name]
        return pair(anc or a, orig, zh, col, dx, dy, name, disc, s1, s2, gap)

    def zh_only(name, dx, dy, disc=False, s=1.1, anc=None):
        a, orig, _, _, zh, col, _ = T[name]
        return [item(anc or a, zh, col if col != "white" else "white", s, dx, dy, name, disc)]

    # ── 長圖（fov 18–40）──
    LB_SOP = term("Sopdet", 0.0, -3.0, s1=1.5, s2=1.1)                     # 天狼星正下方
    LB_SAH = term("Sah", 1.5, 6.4, s1=1.5, s2=1.1, anc=BELT)               # 腰帶上方（參宿四、參宿五之間）
    LB_CAN = term("Canopus", 0.0, -3.2, s1=1.4, s2=1.05)                   # 老人星下方
    # ── 北盤（R 鏡頭 fov 140：1 單位＝7.71 px；字級 4.4／3.6 ≈ Canva 43／36 px）──
    # 盤上的字不跟著轉（dx/dy＝畫面方向），所以起格（0°）和迄格（−60°）各一套
    def disc_set(sfx, d):
        out = []
        for nm, (dx, dy) in d.items():
            anc = {"ikhemu-sek": (0.0, 90.0)}.get(nm)
            out += term(nm, dx, dy, disc=True, s1=4.4, s2=3.6, gap=4.6, anc=anc)
        return out, sfx
    LB_N0 = disc_set("北天-起", {"Meskhetyu": (8.0, -30.0), "Mooring Post": (0.0, -22.0),
                                  "Hippopotamus": (-2.0, 26.0)})
    LB_N120 = disc_set("北天-轉後", {"Meskhetyu": (18.0, 18.0), "Mooring Post": (34.0, -4.0),
                                      "Hippopotamus": (50.0, 40.0)})
    LB_POLE = disc_set("不知毀滅的星", {"ikhemu-sek": (0.0, 10.0)})

    label_sets = [(LB_SOP, "Sopdet"), (LB_SAH, "Sah"), (LB_CAN, "老人星"),
                  (LB_N0[0], LB_N0[1]), (LB_N120[0], LB_N120[1]), (LB_POLE[0], LB_POLE[1])]

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
    xs, ys = m.pos_primary(*S[SIRIUS][:2])
    xc, yc = m.pos_primary(*S[CANOPUS][:2])
    WIDE0 = (8.0, -6.0, 40.0, 0.0)                      # 獵戶＋天狼星
    SIR1 = (round(xs, 1), -13.0, 26.0, 0.0)             # 天狼星（概念圖定格的底）
    SIR2 = (round(xs, 1), round(ys + 2.0, 1), 18.0, 0.0)  # 天狼星特寫
    DEC0 = (16.0, -6.0, 40.0, 0.0)                      # 旬星：從獵戶—天狼星往東（左）捲＝時間往前
    DEC1 = (-12.0, -8.0, 40.0, 0.0)                     # 天狼星在右、南河三在上（x −24 以東只剩空天，不用）
    N_SW = (0.0, yp, 40.0, 0.0)               # 換組那一格（＝長圖沿走廊上到北極）
    N_WIDE = (-40.0, yp + 5.0, 140.0, 0.0)    # 北天：牛腿、繫船柱、河馬都入鏡（北極在畫面右側）
    N_ROT = (-40.0, yp + 5.0, 140.0, -60.0)   # 逆時針 60°（約 4 小時）：整群還在山稜線以上
    TON0 = (10.0, -4.0, 40.0, 0.0)                      # 今晚：天狼星正南，獵戶在右上
    TON1 = (0.0, -8.0, 36.0, 0.0)
    CAN = (0.0, round(yc + 4.0, 1), 30.0, 0.0)          # 老人星（南盤盤緣圈內）

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=11, north=True,
             frames=[WIDE0, SIR1], layers=["獵"], labels=[], labels_end=ls("Sopdet"),
             vo="上週在大平原，北斗是七兄妹。今天往東，到非洲的尼羅河邊：同一片星空，古埃及人看見——一顆叫醒尼羅河的星。",
             card="同一片星空，古埃及人看見——一顆叫醒尼羅河的星。",
             note="開場字卡；從獵戶＋天狼星推近天狼星；Sah（藍）連線"),
        dict(code="02", kind="Z", sec=15, north=True,
             frames=[SIR1], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-01_尼羅河的一年", overlay_layers=["漲水層", "淹沒層", "黑土層"],
             vo="埃及幾乎不下雨，活命全靠尼羅河。每年夏天，上游的雨季讓河水從六月開始漲，淹過兩岸；退去時留下一層黑色的沃土——埃及人就叫自己的國家「黑土地」。",
             card="黑土地 Kemet",
             note="畫面不動；定格疊概念圖 C-A18-01（河水上漲 → 淹過兩岸 → 退去留下黑土 Kemet）"),
        dict(code="03", kind="Z", sec=13, north=True,
             frames=[SIR1, SIR2], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-02_消失與晨出", overlay_layers=["西沉層", "消失層", "晨出層", "漲水層"],
             vo="天狼星，埃及人叫 Sopdet。每年春天，它沉進夕陽的光裡，消失大約七十天。然後某個夏天的清晨，日出之前，它第一次在東方地平線上閃一下。",
             card="消失七十天",
             note="推近天狼星（Sopdet）；之後定格疊概念圖 C-A18-02（黃昏西沉 → 七十天 → 清晨晨出；第 4 層「河水開始漲」配 04 鏡前半）"),
        dict(code="04", kind="Z", sec=8, north=True,
             frames=[SIR2], layers=["獵"], labels=ls("Sopdet"),
             vo="這叫「Sopdet 出來了」。差不多就在這時候，河水開始漲——埃及的一年，原本就從這一天開始。",
             card="新年＝天狼星晨出",
             note="畫面不動（03 鏡概念圖收掉後的天狼星特寫）；字卡 peret Sopdet"),
        dict(code="05", kind="Z", sec=13, north=True,
             frames=[SIR2, SIR1], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-03_曆法的漂移", overlay_layers=["三季層", "五天層", "漂移層"],
             vo="埃及的曆法，一年三百六十五天：十二個月、每月三十天，再加五天；分成漲水、生長、收成三季。可是沒有閏年，每四年就跟天狼星差一天。",
             card="365 天，沒有閏年",
             note="微拉；之後定格疊概念圖 C-A18-03（三季 12 個月 → 加五天 → 每四年差一天）"),
        dict(code="06", kind="Z", sec=13, north=True,
             frames=[SIR1], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-11_一千四百六十年", overlay_layers=["一圈層"],
             vo="要差滿一整圈，得一千四百六十年。羅馬作家 Censorinus 記下：西元一三九年，埃及的新年又剛好落在天狼星升起的日子——七月二十日前後。",
             card="1460 年繞一圈",
             note="v2 加回；畫面不動；定格疊概念圖 C-A18-11（晨出標記繞完一整圈 → 西元 139 年 7/20 前後）"),
        dict(code="07", kind="Z", sec=14, north=True,
             frames=[SIR1], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-04_晚了一個多月", overlay_layers=["古代層", "今天層"],
             vo="那今天呢？我們算了一下：金字塔時代，天狼星在孟斐斯重新出現，大約在夏至後幾天，正好趕上漲水；今天在開羅，要等到八月五日前後——晚了一個多月。",
             card="晚了一個多月",
             note="畫面不動；定格疊概念圖 C-A18-04（前 2500 年孟斐斯 6/28 ↔ 夏至 6/24 → 2027 開羅 8/5，差約 38 天）"),
        dict(code="08", kind="Z", sec=10, north=True,
             frames=[SIR1], layers=["獵"], labels=ls("Sopdet"),
             overlay="C-A18-05_河已經不等了", overlay_layers=["高壩層"],
             vo="而且尼羅河也不漲了：一九七〇年亞斯文高壩完工，每年的大水就被攔進水庫。等天狼星的河，已經不等了。",
             card="河已經不等了",
             note="畫面不動；定格疊概念圖 C-A18-05（河的剖面加一道壩，水位線變平；自繪，不用照片）"),
        dict(code="09", kind="S", sec=12, north=True,
             frames=[SIR1, DEC0], layers=["獵"], labels=ls("Sopdet", "Sah"), labels_start=ls("Sopdet"),
             vo="在天上，天狼星總是跟在獵戶後面升起。獵戶是 Sah，後來成了冥神歐西里斯；天狼星 Sopdet，成了他的妻子伊西斯，一直跟在他身後。",
             card="Sah 與 Sopdet",
             note="v2 加回；從天狼星往右上（西）捲、拉遠到獵戶＋天狼星（終點＝10 鏡起點）；角落小字「連線：Belmonte 重建」"),
        dict(code="10", kind="S", sec=17, north=True,
             frames=[DEC0, DEC1], layers=["獵"], labels=ls("Sopdet", "Sah"),
             overlay="C-A18-06_星星時刻表", overlay_layers=["格子層", "十二小時層"],
             vo="埃及人還把天狼星和其他三十五組星，排成夜裡的時鐘：一組一組輪流升起，一夜數十二組——夜晚分成十二個小時，就是這樣來的。四千年前的棺材蓋上，就畫著這張星星時刻表。",
             card="夜晚的十二小時",
             note="從獵戶—天狼星往東（左）慢慢捲＝後面升起的星（示意旬星帶）；之後定格疊概念圖 C-A18-06（棺蓋對角星鐘示意，自繪表格）"),
        dict(code="11", kind="R", sec=13, north=True,
             frames=[N_SW, N_WIDE], layers=["腿", "柱", "馬"], labels=ls("北天-起"), labels_start=[],
             vo="北方的北斗，在埃及是一條牛的前腿，叫 Meskhetyu。神話說，那是惡神賽特的腿，被金鍊拴在北天的繫船柱上，由化身河馬的女神看守。",
             card="拴在北天的牛腿",
             note="【自動換組】長圖→北盤（盤心＝北天極）；拉遠到 fov 140：牛的前腿（琥珀）、繫船柱（綠）、河馬（紅）"),
        dict(code="12", kind="R", sec=12, north=True,
             frames=[N_WIDE, N_ROT], layers=["腿", "柱", "馬"], labels=ls("不知毀滅的星"),
             labels_start=ls("北天-起"), labels_end=ls("北天-轉後", "不知毀滅的星"),
             overlay="C-A18-07_北面的入口", overlay_layers=["剖面層"],
             vo="那時北斗和北極附近的星都不會落下，埃及人叫它們「不知毀滅的星」。法老死後，希望到那裡去；大金字塔的入口，也開在北面。",
             card="不知毀滅的星",
             note="北盤逆時針轉 60°（北斗繞北極轉）；不畫今天的拱極圈；角落小字「金字塔時代」；"
                  "之後定格疊概念圖 C-A18-07（金字塔剖面，北面入口通道）"),
        dict(code="13", kind="R", sec=12, north=True,
             frames=[N_ROT], layers=["腿", "柱", "馬"], labels=ls("北天-轉後"),
             overlay="C-A18-12_對正北", overlay_layers=["方框層"],
             vo="大金字塔的四邊，對正東西南北，誤差只有大約二十分之一度。他們怎麼找到正北？一種推測是：看北方這些繞著北極轉的星。",
             card="對正北，誤差約 1/20°",
             note="v2 加回；畫面不動（北盤 −60°）；定格疊概念圖 C-A18-12（金字塔俯視方框、南北線指向北天極；標「推測」）"),
        dict(code="14", kind="R", sec=11, north=True,
             frames=[N_ROT], layers=["腿"], labels=ls("北天-轉後"),
             overlay="C-A18-08_拉繩定位", overlay_layers=["木樁層", "牛腿層"],
             vo="兩千多年後的神廟牆上寫得更清楚：國王跟女神拉起繩子定位，說他的眼睛看著那條牛腿，然後立下神廟的四個角。",
             card="看著牛腿，立下四角",
             note="畫面不動（北盤 −60°，只留牛的前腿）；定格疊概念圖 C-A18-08（兩根木樁、一條繩、繩指向牛腿；自繪）"),
        dict(code="15", kind="Z", sec=10, north=True,
             frames=[WIDE0], layers=["獵"], labels=ls("Sopdet", "Sah"),
             vo="丹德拉的哈索爾神廟，天花板上就刻著一張圓形的星圖：黃道十二宮、牛腿、河馬、Sah 和 Sopdet，全在上面。",
             card="丹德拉星圖",
             note="【自動換組】北盤→長圖；畫面不動；疊丹德拉圓形黃道圖（羅浮宮原件照片或 1802 年版畫，"
                  "美宣另尋授權圖，依序圈出牛腿、河馬、獵戶、天狼星）"),
        dict(code="16", kind="Z", sec=15, north=True,
             frames=[WIDE0], layers=["獵"], labels=ls("Sopdet", "Sah"),
             overlay="C-A18-13_以為有好幾千年", overlay_layers=["年表層"],
             vo="拿破崙的學者看到它，以為有好幾千年，甚至比聖經的創世還早。一八二一年，它被炸下來運到巴黎；後來 Champollion 從旁邊的王名框裡，讀出了羅馬時代的頭銜。",
             card="以為有好幾千年？",
             note="v2 加回；畫面不動（丹德拉星圖淡出）；定格疊概念圖 C-A18-13（1799 遠征 → 1821 取下 → 1822 Champollion）"),
        dict(code="17", kind="Z", sec=13, north=True,
             frames=[WIDE0], layers=["獵"], labels=ls("Sopdet", "Sah"),
             overlay="C-A18-09_兩千五百年", overlay_layers=["年表層"],
             vo="今天的研究推算，它設計在西元前五十年左右，跟埃及豔后同一個時代——比大金字塔晚了兩千五百年。原件在羅浮宮，神廟裡的是複製品。",
             card="埃及豔后的時代",
             note="畫面不動；定格疊概念圖 C-A18-09（前 2560 古夫金字塔 …2500 年… 前 50 丹德拉星圖）"),
        dict(code="18", kind="S", sec=13, north=True,
             frames=[TON0, TON1], layers=["獵"], labels=ls("Sopdet", "Sah"),
             overlay="C-A18-10_今晚十點半",
             vo="今晚是滿月，月亮高掛東方。十點半往正南看：天狼星爬到最高，四十八度；獵戶在它右上方。回頭往東北，那條牛腿，已經爬出地平線了。",
             card="今晚十點半，往正南",
             note="台北 1/22 22:30：天狼星 48°（正南）、獵戶在右上；之後疊 9:16 圖卡 C-A18-10（可存圖）"),
        dict(code="19", kind="T", sec=11, north=False,
             frames=[TON1, CAN], layers=["獵"], labels=ls("老人星"), labels_start=ls("Sopdet"),
             vo="下週五，我們去古阿拉伯的沙漠：今晚天狼星正下方，那顆低低的老人星，在那裡有自己的故事；天上還有兩群鴕鳥。",
             card="下集見｜古阿拉伯：兩隻鴕鳥與擋路的老人星",
             note="沿走廊往南到老人星（南盤盤緣圈內）；端卡＋追蹤 CTA"),
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
                yc0 = m.y_pole if sh["north"] else -m.y_pole
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-(cx - xt) / fov * 1080), round((cy - yc0) / fov * 1080))
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

    print(f"  x：天狼星 {x_of(S[SIRIUS][0]):+.1f}、老人星 {x_of(S[CANOPUS][0]):+.1f}（畫布 {xc:+.1f},{yc:+.1f}）、"
          f"參宿四 {x_of(S[BETELGEUSE][0]):+.1f}、參宿七 {x_of(S[RIGEL][0]):+.1f}、參宿二 {x_of(S[ALNILAM][0]):+.1f}")

    terms = {}
    for hips, orig, tr, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips, 原文=orig, 拼音=tr if tr != "—" else "", 英文翻譯=en, 中文=zh,
                           顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY,
               "line_groups": LINE_GROUPS, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)

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
