# -*- coding: utf-8 -*-
"""A-19 古阿拉伯：兩隻鴕鳥與擋路的老人星｜大畫布 v4.6

論點：九世紀希臘天文學傳入以前，阿拉伯人的天空是一座沙漠動物園（116 組裡二十多種動物）；
鴕鳥是園裡最大的家族（兩隻公鴕鳥、小鴕鳥、鴕鳥媽媽、鴕鳥窩、夏天的兩群）；南方低空的 Suhail（老人星）
有兩個姊妹：渡過銀河的天狼星 al-ʿAbūr、留在北岸哭花了眼的南河三 al-Ghumayṣāʾ。

來源：Stellarium arabic_indigenous（舊版 arabic_ancient；Khalid al-Ajaji，names_dictionary 附出處）；
逐字稿 v1 的「星空對時」（PyEphem 自算；本腳本另算台北 1/29 20:00／21:43 的地方恆星時）。

鏡頭路線：長圖（冬季南天：天狼星）→ 兩層阿拉伯星空（概念圖）→ 拉遠：動物園（全部動物星座）→
獅子（S）→ 沿北走廊往上：羚羊三跳（T）→【硬切】秋季南天：兩隻公鴕鳥、小鴕鳥、鴕鳥媽媽 → 波江座鴕鳥窩、Azha
（概念圖：抄錯一個字母）→【硬切】夏季人馬座兩群 →【硬切】南走廊：Suhail（概念圖：看得到 Suhail 的地方）→
三兄妹 → 擋路（概念圖）→ 310 光年＋南極老人（概念圖）→【自動換組】南盤：台北 1/29 面南 20:00→21:43（圖卡）→
長圖：長蛇頭—巨蟹（下集朱雀）。

參數
  lst = 138 → x＝±180 落在 RA 318（摩羯—寶瓶之間，本集沒有東西在那裡）：人馬座兩群 x −133…−149、
             北落師門 +153.6、土司空 +127.1、波江 η（Azha）+93.9、老人星 +42.0、天狼星 +36.7、南河三 +23.2、
             軒轅十四 −14.1、三跳 x −31.6／−17／+2.6。lst＝96（老人星 x=0）會讓人馬座正好跨在 x=±180 上，不能用。
  x_tS = 42.0 → 南走廊＝老人星（08–12 鏡用 T 沿走廊上下：老人星、天狼星、南河三同框）。
  x_tN = −15 → 北走廊從獅子頭（軒轅十四 x −14）往上穿過三跳（04B 鏡 T）。
             ※ x_t≠0 是第一集：gen_canva_pages.view_lst／gen_master_canvas.sb_grid 的地平線已改成扣掉 x_t
               （盤心正上方＝時角 x_tS），x_t＝0 的舊集結果不變。Canva 盤對位不能水平置中，用 check_disc_align 的左上 X。
  D_s = 48、D_r = 52 → 老人星（−52.7）在南盤本體；第三跳 ι／κ UMa（+48.0／+47.2）在縫合帶，只用 T（走廊）看。
  D_fill = −1 → k=1.508、R_fill=137.2；|x_tS|+R_fill=179.2 ≤ 180 ✓。南盤收到 dec +1：
             台北面南 fov 60 的框（南方地平線＝盤心上方 kφ=37.7、老人星 56.2、天狼星 110.5）都在填滿圓內。
  南盤旋轉（面向南方，順時針＝時間前進）：rot＝lst_obs＋x_tS−lst；台北 1/29 20:00 −25.9°、21:43 −0.1°。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-19"
OUT = os.path.join(BASE, "05_素材/A-19_古阿拉伯/_v4大畫布")
LST0 = 138.0
XTS, XTN = 42.0, -15.0
PHI = 25.03
TPE = (25.0330, 121.5654)


def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：盤心正上方＝時角 x_tS 的方向；順時針＝時間前進"""
    return round((lst_obs + XTS - LST0 + 180.0) % 360.0 - 180.0, 2)


T_TPE = {"20:00": "2027/1/29 20:00", "21:43": "2027/1/29 21:43"}
LSTS = {k: lst_at(*TPE, 8, v) for k, v in T_TPE.items()}
ROT = {k: rot_s(v) for k, v in LSTS.items()}

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
CANOPUS, SIRIUS, PROCYON = 30438, 32349, 37279
FOMALHAUT, DIPHDA, AZHA = 113368, 3419, 13701
REGULUS, CASTOR, POLLUX = 49669, 36850, 37826
BETELGEUSE, RIGEL = 27989, 24436
LEAP1, LEAP2, LEAP3 = [55219, 55203], [50372, 50801], [44127, 44471]
MAINS = [CANOPUS, SIRIUS, PROCYON, FOMALHAUT, DIPHDA, AZHA, REGULUS, CASTOR, POLLUX,
         BETELGEUSE, RIGEL] + LEAP1 + LEAP2 + LEAP3


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium arabic_indigenous）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
AR, AR_EN = {}, {}
for c in json.load(open(os.path.join(SC_NEW, "arabic_indigenous", "index.json"), encoding="utf-8"))["constellations"]:
    k = c["id"].split()[-1]
    segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    AR[k] = [s for s in segs if len(set(s)) >= 2]
    AR_EN[k] = c["common_name"].get("english", "")

# 動物星座（有連線的）：依英文名判斷，獅子的各部位一起算
ANIMAL_KEYS = ("Oryx", "Gazelle", "Leap", "Wolf", "Wolves", "Camel", "Hyena", "Eagle", "Lamb", "Dogs",
               "Lion", "Scorpion", "Ostrich", "Fish", "Ravens", "Shrikes", "Doves", "Larks", "Sandgrouse",
               "Wild Asses", "Caracal", "Horses", "Sheep", "Goats")
LION_PARTS = ("Asad", "Maqb", "Mabs", "Nath", "Tarf", "Jabh", "Zubr")
# SBhm「小羊的吉星」是月站名，不算動物星座
ANIMALS = sorted(k for k, segs in AR.items() if segs and k != "SBhm" and
                 (k in LION_PARTS or any(w.lower() in AR_EN[k].lower() for w in ANIMAL_KEYS)))

LG_LION = [(AR[k], "red", 1.0) for k in LION_PARTS if AR.get(k)]
LG_LEAP = [(AR["Qfz1"] + AR["Qfz2"] + AR["Qfz3"], "green", 1.3)]
LG_OST = [(AR["Rial"], "amber", 0.8), (AR["Nmat"], "purple", 1.0), (AR["BdQd"], "green", 1.0)]
LG_SUM = [(AR["NaaW"], "blue", 1.1), (AR["NaaS"], "green", 1.1)]
LG_ANIMAL = [(AR[k], "amber", 0.9) for k in ANIMALS]
USED = set(LION_PARTS) | {"Qfz1", "Qfz2", "Qfz3", "Rial", "Nmat", "BdQd", "NaaW", "NaaS"}
LG_ALL = LG_LION + LG_LEAP + LG_OST + LG_SUM + [(segs, "purple", 0.6) for k, segs in AR.items()
                                                if segs and k not in USED]
LINE_SETS = [(LG_ANIMAL, "連線-動物園"), (LG_LION, "連線-獅子"), (LG_LEAP, "連線-三跳"),
             (LG_OST, "連線-鴕鳥一家"), (LG_SUM, "連線-夏天的鴕鳥")]
LINES_KEY = {"L4": "星座連線", "動": "連線-動物園", "獅": "連線-獅子", "跳": "連線-三跳",
             "鴕": "連線-鴕鳥一家", "夏": "連線-夏天的鴕鳥"}
LINE_GROUPS = {"L4": LG_ALL, "動": LG_ANIMAL, "獅": LG_LION, "跳": LG_LEAP, "鴕": LG_OST, "夏": LG_SUM}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(segs):
    return sorted({h for s in segs for h in s})


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；補上阿拉伯文轉寫的長音與點下字母）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾḀ-ỿ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
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
# 四、名詞總表（＝標籤對照表）
#   (錨點, 原文（轉寫）, 阿拉伯文, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ([CANOPUS], "Suhayl", "سهيل", "Canopus", "老人星（Suhail）", "amber",
     "names_dictionary：男子名（a proper name of a man）；片中唸 Suhail"),
    ([SIRIUS], "al-Shiʿrā al-ʿAbūr", "الشعرى العبور", "The Crossing Shiʿrā", "渡河的（天狼星）", "blue",
     "names_dictionary；另名 al-Shiʿrā al-Yamāniya 也門的 Shiʿrā"),
    ([PROCYON], "al-Ghumayṣāʾ", "الشعرى الغميصاء", "The Tearful Shiʿrā", "淚眼模糊的（南河三）", "purple",
     "names_dictionary；字義＝眼睛有分泌物、淚眼模糊（不是「淚流滿面」）；另名 al-Shiʿrā al-Shāmiya"),
    ([REGULUS], "al-Asad", "الأسد", "The Lion", "獅子", "red",
     "Stellarium Asad：南河三、北河二三、M44、獅子座、后髮；錨點放軒轅十四"),
    (LEAP1, "Alula", "القفزة الأولى", "The First Leap", "第一跳", "green",
     "ν ξ UMa；Alula＜al-qafza al-ūlā（Kunitzsch & Smart）"),
    (LEAP2, "Tania", "القفزة الثانية", "The Second Leap", "第二跳", "green", "λ μ UMa；Tania＜al-thāniya"),
    (LEAP3, "Talitha", "القفزة الثالثة", "The Third Leap", "第三跳", "green", "ι κ UMa；Talitha＜al-thālitha"),
    ([FOMALHAUT], "al-Ẓalīmān", "الظليمان", "The Two Male Ostriches", "公鴕鳥（北落師門）", "amber",
     "兩隻公鴕鳥＝北落師門＋土司空（相距 26.8°），Stellarium 不連線"),
    ([DIPHDA], "al-Ẓalīmān", "الظليمان", "The Two Male Ostriches", "公鴕鳥（土司空）", "amber", "同上"),
    (uniq(AR["Rial"]), "al-Riʾāl", "الرئال", "The Young Ostriches", "小鴕鳥們", "amber", "寶瓶—鯨魚交界 12 顆暗星"),
    (uniq(AR["Nmat"]), "al-Naʿāmāt", "النعامات", "The Ostriches", "鴕鳥媽媽", "purple", "鯨魚 η θ ζ τ υ"),
    (uniq(AR["BdQd"]), "Udḥiyy al-Naʿām", "أدحي النعام", "Ostrich Nest, Eggs and Eggshells", "鴕鳥窩、蛋、蛋殼",
     "green", "波江座 8 顆（新版 BdQd）"),
    ([AZHA], "Azha", "أدحي", "Azha (η Eri)", "鴕鳥窩", "green",
     "IAU WGSN 2016 核定；Azha＜udḥiyy 抄寫訛誤（Kunitzsch & Smart）"),
    (uniq(AR["NaaW"]), "al-Naʿām al-Wārid", "النعام الوارد", "Ostriches Drinking at the River", "下河喝水的鴕鳥",
     "blue", "γ2 ε δ η Sgr（在銀河裡）"),
    (uniq(AR["NaaS"]), "al-Naʿām al-Ṣādir", "النعام الصادر", "Ostriches Leaving the River", "喝飽離開的鴕鳥",
     "green", "σ τ ζ φ Sgr（銀河外）"),
    ([CANOPUS], "南極老人", "—", "Old Man of the South Pole", "南極老人（中國）", "white",
     "《史記・天官書》：老人見，治安；不見，兵起"),
]


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=48, D_r=52, D_fill=-1,
               w_c=34, feather=8, x_tN=XTN, x_tS=XTS, phi=None,
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

    TM = {}
    for t in TERMS:
        TM.setdefault(t[1], []).append(t)

    def term(name, dx, dy, disc=False, s1=1.5, s2=1.1, gap=2.3, i=0, zh_only=False):
        a, orig, _, _, zh, col, _ = TM[name][i]
        key = f"{name}-{i}"
        if zh_only:
            return [item(a, zh, col, s1, dx, dy, key, disc)]
        return [item(a, orig, col, s1, dx, dy + gap / 2, key, disc),
                item(a, zh, "white", s2, dx, dy - gap / 2, key + "-zh", disc)]

    # ── 長圖（fov 20–54：字級 1.5／1.1）──
    LB_SIR = [item([SIRIUS], "天狼星", "white", 1.3, 0.0, -2.8, "天狼星")]
    LB_LION = term("al-Asad", 0.0, -4.2)
    LB_LEAP = (term("Alula", 0.0, -3.4, s1=1.4, s2=1.05) + term("Tania", 0.0, 3.6, s1=1.4, s2=1.05) +
               term("Talitha", 0.0, -3.4, s1=1.4, s2=1.05))
    LB_ZAL = term("al-Ẓalīmān", -5.0, -3.4, i=0) + term("al-Ẓalīmān", 5.0, -3.4, i=1)   # 北落師門往左、土司空往右（不出框）
    LB_RIAL = term("al-Riʾāl", 0.0, 4.0, s1=1.3, s2=1.0)
    LB_NMAT = term("al-Naʿāmāt", 0.0, -5.0, s1=1.3, s2=1.0)
    LB_NEST = term("Udḥiyy al-Naʿām", 4.0, -9.0, s1=1.3, s2=1.0)
    LB_AZHA = term("Azha", 0.0, 2.6, s1=1.1, s2=0.85, gap=1.8)
    LB_SUM = term("al-Naʿām al-Wārid", 4.0, 5.0, s1=1.3, s2=1.0) + term("al-Naʿām al-Ṣādir", 0.0, 5.4, s1=1.3, s2=1.0)
    LB_SUH = term("Suhayl", 0.0, -3.4, s1=1.5, s2=1.1)
    LB_SIS = (term("Suhayl", 0.0, 3.6, s1=1.5, s2=1.1) + term("al-Shiʿrā al-ʿAbūr", 0.0, -3.4, s1=1.5, s2=1.1) +
              term("al-Ghumayṣāʾ", 9.0, -3.4, s1=1.5, s2=1.1))      # 南河三在框左緣：字往右下
    LB_OLD = term("南極老人", 0.0, -3.0, s1=1.2, zh_only=True)
    # ── 南盤（台北面南，fov 60：字級 1.6 ≈ Canva 49 px）──
    LB_TPE0 = [item([CANOPUS], "老人星", "amber", 1.6, 7.0, 0.0, "台北-老人星-起", disc=True),
               item([SIRIUS], "天狼星", "white", 1.4, 0.0, -3.2, "台北-天狼星", disc=True)]
    LB_TPE = [item([CANOPUS], "老人星 12°", "amber", 1.6, 0.0, -3.4, "台北-老人星", disc=True),
              item([SIRIUS], "天狼星", "white", 1.4, 0.0, -3.2, "台北-天狼星", disc=True)]

    label_sets = [(LB_SIR, "天狼星"), (LB_LION, "獅子"), (LB_LEAP, "三跳"), (LB_ZAL, "公鴕鳥"),
                  (LB_RIAL, "小鴕鳥"), (LB_NMAT, "鴕鳥媽媽"), (LB_NEST, "鴕鳥窩"), (LB_AZHA, "Azha"),
                  (LB_SUM, "夏天的鴕鳥"), (LB_SUH, "Suhail"), (LB_SIS, "三兄妹"), (LB_OLD, "南極老人"),
                  (LB_TPE0, "台北面南-20時"), (LB_TPE, "台北面南")]

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
    xs_, ys_ = m.pos_primary(*S[SIRIUS][:2])
    xc_, yc_ = m.pos_primary(*S[CANOPUS][:2])
    xa_, ya_ = m.pos_primary(*S[AZHA][:2])
    SIR = (round(xs_, 1), -14.0, 20.0, 0.0)            # 天狼星特寫
    WIDE = (40.0, -4.0, 48.0, 0.0)                     # 冬季南天：獵戶、天狼星、南河三
    ZOO0 = (8.0, 0.0, 34.0, 0.0)                       # 動物園：巨蟹—獅子頭—雙子
    ZOO1 = (8.0, 0.0, 54.0, 0.0)
    LION0 = (8.0, 8.0, 44.0, 0.0)                      # 南河三＝縮起的前臂、北河二三、M44
    LION1 = (-18.0, 8.0, 44.0, 0.0)                    # 獅子頭與身體
    LEAP_A = (XTN, 12.0, 44.0, 0.0)                    # 北走廊（T）：從獅子頭往上
    LEAP_B = (XTN, 36.0, 44.0, 0.0)                    #   三跳全在框內（x −31.6…+3.2）
    AUT0 = (140.0, -8.5, 44.0, 0.0)                   # 秋季南天：北落師門＋土司空＋小鴕鳥
    AUT1 = (118.0, -12.0, 40.0, 0.0)                   # 土司空＋鴕鳥媽媽
    NEST = (90.0, -12.0, 40.0, 0.0)                    # 波江座鴕鳥窩
    AZ = (round(xa_, 1), round(ya_ - 1.0, 1), 20.0, 0.0)
    SGR0 = (-139.0, -16.0, 36.0, 0.0)                  # 夏季人馬座兩群＋銀河
    SGR1 = (-140.0, -16.0, 36.0, 0.0)
    SUH = (XTS, round(yc_ + 10.0, 1), 32.0, 0.0)       # 南走廊（T）：老人星＋天狼星在上方邊緣
    SIS = (XTS, -24.0, 48.0, 0.0)                      # 三兄妹同框
    SIS2 = (XTS, -24.5, 50.0, 0.0)
    OLD = (XTS, round(yc_ + 2.0, 1), 24.0, 0.0)        # 老人星特寫
    POLE = (XTS, -yp, 40.0, 0.0)                       # 南極（＝換組那一格）

    def FS(t):                                         # 台北面南：南方地平線在畫面 Y≈1650
        return (XTS, round(-yp + 76.0, 2), 60.0, ROT[t])
    END0 = (30.0, -8.0, 44.0, 0.0)
    END1 = (8.0, 6.0, 40.0, 0.0)                       # 長蛇頭—巨蟹（朱雀的柳、鬼）

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=10, north=True,
             frames=[SIR, WIDE], layers=[], labels=ls("天狼星"), labels_end=[],
             vo="上一集在古埃及，天狼星叫醒了尼羅河。往東渡過紅海：同一片星空，古阿拉伯人看見——一座沙漠動物園。",
             card="同一片星空，古阿拉伯人看見——一座沙漠動物園。",
             note="開場字卡；天狼星特寫（承接上集）→ 拉遠到冬季南天"),
        dict(code="02", kind="Z", sec=9, north=True,
             frames=[WIDE], layers=[], labels=[],
             overlay="C-A19-01_兩層阿拉伯星空", overlay_layers=["今日層", "古詩層"],
             vo="這次往回推一千多年：貝都因人的星名藏在古詩裡，八到十世紀的學者，一句一句抄下來。",
             card="星名藏在古詩裡",
             note="畫面不動；定格疊概念圖 C-A19-01（上：A-13 今日星曆／下：古詩 → 學者 → Stellarium）"),
        dict(code="03", kind="Z", sec=8, north=True,
             frames=[ZOO0, ZOO1], layers=["動"], labels=[],
             vo="這一百多組星座，很多是動物：羚羊、狼、鬣狗、駱駝、野驢、老鷹、烏鴉……加起來二十多種。",
             card="天上二十多種動物",
             note=f"拉遠；動物星座連線（琥珀，{len(ANIMALS)} 組）淡入；動物小圖示由美宣自繪（不用網路圖）"),
        dict(code="04A", kind="S", sec=6, north=True,
             frames=[LION0, LION1], layers=["獅"], labels=ls("獅子"),
             vo="最大的是一頭獅子，從雙子座一路躺到室女座。",
             card="羚羊的三個蹄印",
             note="從南河三、北河二三往左（東）滑到獅子頭；獅子 al-Asad（紅）"),
        dict(code="04B", kind="T", sec=13, north=True,
             frames=[LEAP_A, LEAP_B], layers=["獅", "跳"], labels=ls("三跳"), labels_start=ls("獅子"),
             vo="傳說牠尾巴往地上一甩，羚羊嚇得跳起來——大熊座腳下這三對星，就是三個蹄印。今天的星名 Alula、Tania、Talitha，意思就是第一跳、第二跳、第三跳。",
             note="沿北走廊（x −15）往上到大熊腳下：三跳（綠）逐對亮；標籤 Alula／Tania／Talitha＝第一跳／第二跳／第三跳"),
        dict(code="05", kind="S", sec=14, north=True,
             frames=[AUT0, AUT1], layers=["鴕"], labels=ls("公鴕鳥", "小鴕鳥", "鴕鳥媽媽"),
             labels_start=ls("公鴕鳥", "小鴕鳥"),
             vo="鴕鳥更是一整家。北落師門和土司空，是兩隻公鴕鳥，叫 al-Ẓalīmān；牠們中間一片暗暗的小星，是一群小鴕鳥；鯨魚座還有幾隻鴕鳥媽媽。",
             card="兩隻公鴕鳥",
             note="【硬切】秋季南天：北落師門、土司空（不連線）＋小鴕鳥（琥珀）→ 往左滑到鯨魚座鴕鳥媽媽（紫）"),
        dict(code="06", kind="S", sec=15, north=True,
             frames=[AUT1, NEST, AZ], layers=["鴕"], labels=ls("Azha"), labels_start=ls("鴕鳥媽媽"),
             overlay="C-A19-02_抄錯一個字母", overlay_layers=["原字層", "抄錯層"],
             vo="往旁邊的波江座，有一個鴕鳥窩，連蛋和蛋殼都有。其中一顆星，今天的正式名字叫 Azha——就是阿拉伯文的「鴕鳥窩」，中世紀抄書的人抄錯了一個字母。",
             card="抄錯一個字母",
             note="往左到波江座鴕鳥窩（綠）→ 推近 η Eri（Azha）；之後定格疊概念圖 C-A19-02（udḥiyy → azḥā → IAU 2016 Azha）"),
        dict(code="07", kind="S", sec=14, north=True,
             frames=[SGR0, SGR1], layers=["夏"], labels=ls("夏天的鴕鳥"),
             vo="到了夏天，人馬座還有兩群鴕鳥：四隻走下銀河這條大河喝水，四隻喝飽了往回走。地上的阿拉伯鴕鳥，二十世紀就滅絕了；天上的，還在。",
             card="地上滅絕，天上還在",
             note="【硬切】夏季人馬座＋銀河：下河喝水（藍，銀河裡）、喝飽離開（綠，銀河外）；角落小字「夏天的星空」"),
        dict(code="08", kind="T", sec=15, north=False,
             frames=[SUH], layers=[], labels=ls("Suhail"),
             overlay="C-A19-03_看得到Suhail的地方", overlay_layers=["緯度層", "城市層"],
             vo="再往南，地平線上這顆亮星，是 Suhail，老人星；在阿拉伯，這是一個男人的名字。大約北緯三十七度以北，它根本升不起來——所以詩人說，Suhail 是南方也門的星。",
             card="Suhail 老人星",
             note="【硬切】南走廊：老人星（標籤 Suhail）；之後定格疊概念圖 C-A19-03（37.3°N 界線與各地最高仰角）"),
        dict(code="09", kind="T", sec=19, north=False,
             frames=[SUH, SIS], layers=[], labels=ls("三兄妹"), labels_start=ls("Suhail"),
             vo="古書記著一個故事：天狼星和南河三，是 Suhail 的兩個姊妹。Suhail 往南走了，一個姊妹追上去，渡過了銀河，所以叫 al-ʿAbūr，「渡河的」；另一個留在北岸，哭到眼睛都花了，叫 al-Ghumayṣāʾ，「淚眼模糊的」。",
             card="渡河的・淚眼模糊的",
             note="沿南走廊往上：老人星、天狼星、南河三同框（不連線，只標名）；銀河從天狼星和南河三中間穿過"),
        dict(code="10", kind="T", sec=9, north=False,
             frames=[SIS, SIS2], layers=[], labels=ls("三兄妹"),
             vo="天上真的對得上：銀河從天狼星和南河三中間穿過；哭花了眼的南河三，也真的暗了一大截。",
             card="天狼星亮了五倍多",
             note="微拉；天狼星視亮度是南河三的 5.4 倍"),
        dict(code="11", kind="T", sec=12, north=False,
             frames=[SIS2], layers=[], labels=ls("三兄妹"),
             overlay="C-A19-04_擋路的Suhail", overlay_layers=["商道層", "星星層"],
             vo="那「擋路」呢？伊斯蘭時代的書裡另有一說：Suhail 原本是在也門攔路收稅的惡霸，被變成了星星——不過學者認為，這段傳述並不可靠。",
             card="收過路稅的 Suhail",
             note="畫面不動；定格疊概念圖 C-A19-04（商道 → 收稅 → 變成星星；小字：伊斯蘭時代的傳述・學者判為不可靠）"),
        dict(code="12", kind="T", sec=14, north=False,
             frames=[OLD, POLE], layers=[], labels=[], labels_start=ls("南極老人"),
             overlay="C-A19-05_310光年", overlay_layers=["距離層", "南極老人層"], overlay_at="start",
             vo="老人星其實離我們三百一十光年，看起來卻只比天狼星暗一點——它本身比天狼星亮好幾百倍。在中國，它叫「南極老人」：「老人見，治安；不見，兵起。」",
             card="310 光年",
             note="老人星特寫（標籤 南極老人）；定格疊概念圖 C-A19-05（8.6 vs 309 光年；南極老人引文）；"
                  "概念圖收的同時沿南走廊滑到南天極（下一鏡換南盤）；配音注意：兩個「見」都讀「現」"),
        dict(code="13", kind="R", sec=14, north=False, horizon=[PHI],
             frames=[FS("20:00"), FS("21:43")], layers=[], labels=ls("台北面南"), labels_start=ls("台北面南-20時"),
             overlay="C-A19-06_這週末抬頭看",
             vo="這週末在台灣：晚上九點四十分，老人星升到正南方最高，只有十二度，要找南方完全沒有遮擋的地方；墾丁可以到十五度。月亮半夜才升起。",
             card="21:43 正南 12°",
             note=f"【自動換組】長圖→南盤；台北 1/29 面南（山＝南方地平線），盤順時針 20:00→21:43"
                  f"（{ROT['20:00']:+.1f}°→{ROT['21:43']:+.1f}°）；之後疊 9:16 圖卡 C-A19-06（可存圖）；"
                  f"角落小貼紙「可存圖：沙漠動物園小辭典」（C-A19-07 圖卡，放 IG 輪播）"),
        dict(code="15", kind="S", sec=6, north=True,
             frames=[END0, END1], layers=[], labels=[],
             vo="下週五除夕，我們回到中國，看四象的最後一隻：朱雀。",
             card="下集｜春節特輯・朱雀",
             note="【自動換組】南盤→長圖；往東北到長蛇頭—巨蟹（朱雀的柳、鬼）；端卡＋追蹤 CTA"),
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

    print("  台北 1/29 地方恆星時：" + "、".join(f"{k} {v:.2f}°（rot {ROT[k]:+.2f}°）" for k, v in LSTS.items()))
    print(f"  x：老人星 {x_of(S[CANOPUS][0]):+.1f}、天狼星 {x_of(S[SIRIUS][0]):+.1f}、南河三 {x_of(S[PROCYON][0]):+.1f}、"
          f"北落師門 {x_of(S[FOMALHAUT][0]):+.1f}、土司空 {x_of(S[DIPHDA][0]):+.1f}、Azha {x_of(S[AZHA][0]):+.1f}；"
          f"動物星座 {len(ANIMALS)} 組：{' '.join(ANIMALS)}")

    terms = {}
    for hips, orig, nat, en, zh, col, note in TERMS:
        key = orig if orig not in terms else f"{orig}（{zh}）"
        terms[key] = dict(hips=hips, 原文=nat if nat != "—" else orig, 拼音=orig if nat != "—" else "",
                          英文翻譯=en, 中文=zh, 顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY,
               "line_groups": LINE_GROUPS, "lst0": LST0, "rot_taipei": ROT, "phi": PHI},
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
