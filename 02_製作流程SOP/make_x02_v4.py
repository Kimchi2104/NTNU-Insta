# -*- coding: utf-8 -*-
"""X-02 獵戶環球：全世界都認得的三顆星｜大畫布 v4.6

論點：獵戶的腰帶三顆星（參宿三、二、一）差不多一樣亮、排成一直線、前後不到三度，又剛好躺在天赤道上
——從北極圈到紐西蘭，全世界都看到它們從正東升起、正西落下（南半球看到的獵戶是倒過來的）。所以幾乎
每個文化都替它取了名字。前幾集已經講過「三」「犁」「三個人」（A-05、A-12、A-15、X-01），這集走
三條沒講過的線：
  ① 巨人：埃及的星神 Sah（金字塔經文：「你是那顆大星，Sah 的同伴」）、巴比倫「安努的忠實牧人」、
     希臘獵人俄里翁（被蠍子螫死，蠍子升起他就落下）、阿拉伯的女子 al-Jawzā。
  ② 一條腿（南美）：圖皮的老人（妻子砍斷他膝下的腿；腰帶是他好腿的膝蓋，參宿四標出斷處）、
     洛科諾的 Mabukuli「沒有大腿的人」（打不到獵物的獵人切下自己的腿騙家人是貘肉；身體＝畢宿
     「貘的下巴」，上週 A-15 講過）、Tikuna「Wücütcha 的腿」（腰帶是腳趾）。
  ③ 火：卡米拉羅伊的三個男孩 Birray Birray（參宿七是營火、劍是撥火棍）、馬雅的三塊爐石（參宿一、
     參宿六、參宿七；獵戶座大星雲是創世之火的煙）、阿茲特克的鑽火棍 Mamalhuaztli（每 52 年的新火）。
之後：這半年腰帶的名字（圖卡）→ 年輕的藍色巨星 → 今晚（元旦）台北往東南東 → 下集納瓦荷「第一個瘦長的人」。

來源：Stellarium 新版 skycultures：modern、chinese、egyptian、babylonian_mulapin、tupi、lokono
（Rybka 2018）、tikuna、kamilaroi、maya、aztec、navajo（Childrey《Star Trails Navajo》）；
Afonso（圖皮老人的故事）；Pyramid Texts §882（Faulkner Utt. 466）；Aratus《Phaenomena》634–646；
PyEphem 自算。

參數
  lst = 84 → 走廊（x=0）＝RA 84：腰帶中間的參宿二 x≈0；參宿四 −4.8、參宿七 +5.4、天狼 −17.3、
             畢宿五 +15、昴宿 +27。
  D_s = 45、D_r = 49、D_fill = 0（與 A-05 相同；盤寬 ÷ 畫布寬 ＝ 0.698729）：埃及 Sah 最南到
             dec −35.5，圖皮老人最北到昴宿 +24.1，都在帶內。本集不用盤（照規定生成）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-02"
OUT = os.path.join(BASE, "05_素材/X-02_獵戶環球/_v4大畫布")
LST0 = 84.0

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BELT = [MINTAKA, ALNILAM, ALNITAK]
BETELGEUSE, BELLATRIX, RIGEL, SAIPH, MEISSA = 27989, 25336, 24436, 27366, 26207
HATYSA = 26241                      # ι Ori（劍尖）
SWORD_HIPS = [26241, 26221, 26237]  # ι、θ1、42 Ori
ALDEBARAN = 21421
HYADES = [21421, 20885, 20205, 20455, 20889]
ALCYONE = 17702
SIRIUS = 32349
MAINS = BELT + [BETELGEUSE, RIGEL, SAIPH, BELLATRIX, ALDEBARAN, SIRIUS]

M42 = (83.82, -5.39)


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium 新版 skycultures）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def sc(culture, english):
    d = json.load(open(os.path.join(SC_NEW, culture, "index.json"), encoding="utf-8"))
    for c in d["constellations"]:
        if c["common_name"].get("english") == english:
            segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
            return [s for s in segs if len(set(s)) >= 2]
    raise KeyError((culture, english))


SEG_ORI = sc("modern", "Orion")
SEG_BELT = [[MINTAKA, ALNILAM, ALNITAK]]
SEG_SAH = sc("egyptian", "Sah")
SEG_SHEP = sc("babylonian_mulapin", "Faithful Shepherd of Anu")
SEG_TUPI = sc("tupi", "Old Man")
SEG_LOKO = sc("lokono", "Man without a thigh") + sc("lokono", "Jaw of the tapir")
SEG_TIKU = sc("tikuna", "Wücütcha's leg")
SEG_MAYA = sc("maya", "Primordial Fire")
SEG_AZTEC = sc("aztec", "The New fire")
SEG_NAV = sc("navajo", "First Slim One")

LG_LOC = [(SEG_ORI, "white", 0.5)]
LG_BELT = [(SEG_BELT, "amber", 0.6)]
LG_SAH = [(SEG_SAH, "amber", 1.0)]
LG_SHEP = [(SEG_SHEP, "purple", 1.0)]
LG_TUPI = [(SEG_TUPI, "green", 1.0)]
LG_LOKO = [(SEG_LOKO, "blue", 1.0)]
LG_TIKU = [(SEG_TIKU, "purple", 1.0)]
LG_MAYA = [(SEG_MAYA, "red", 0.45)]          # fov 14 特寫：線要細
LG_AZTEC = [(SEG_AZTEC, "amber", 0.3)]       # fov 9 特寫
LG_NAV = [(SEG_NAV, "blue", 1.0)]
LINE_SETS = [(LG_LOC, "連線-獵戶（定位）"), (LG_BELT, "連線-腰帶"), (LG_SAH, "連線-Sah（埃及）"),
             (LG_SHEP, "連線-安努的牧人（巴比倫）"), (LG_TUPI, "連線-老人（圖皮）"),
             (LG_LOKO, "連線-沒有大腿的人（洛科諾）"), (LG_TIKU, "連線-Wücütcha的腿（Tikuna）"),
             (LG_MAYA, "連線-三塊爐石（馬雅）"), (LG_AZTEC, "連線-鑽火棍（阿茲特克）"),
             (LG_NAV, "連線-第一個瘦長的人（納瓦荷）")]
LG_ALL = LG_LOC + LG_BELT
LINES_KEY = {"L4": "星座連線", "定位": "連線-獵戶（定位）", "腰帶": "連線-腰帶", "Sah": "連線-Sah（埃及）",
             "牧人": "連線-安努的牧人（巴比倫）", "老人": "連線-老人（圖皮）",
             "洛科諾": "連線-沒有大腿的人（洛科諾）", "腿": "連線-Wücütcha的腿（Tikuna）",
             "爐石": "連線-三塊爐石（馬雅）", "鑽火": "連線-鑽火棍（阿茲特克）",
             "納瓦荷": "連線-第一個瘦長的人（納瓦荷）", "深空": "深空天體"}
LINE_GROUPS = {"L4": LG_ALL, "定位": LG_LOC, "腰帶": LG_BELT, "Sah": LG_SAH, "牧人": LG_SHEP,
               "老人": LG_TUPI, "洛科諾": LG_LOKO, "腿": LG_TIKU, "爐石": LG_MAYA, "鑽火": LG_AZTEC,
               "納瓦荷": LG_NAV}


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
    for w in re.findall(r"[A-Za-zÀ-ɏʻʼʿʾ']+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōūáéíóúýü]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層：深空天體（獵戶座大星雲 M42 的淡光）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    dec = dec0 + y
    ra = ra0 + x / max(0.05, math.cos(math.radians(dec0)))
    return ra % 360, dec


def ellipse(ra0, dec0, a, b, pa, n=48):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        u, v = a * math.cos(t), b * math.sin(t)
        th = math.radians(pa)
        x = u * math.sin(th) + v * math.cos(th)
        y = u * math.cos(th) - v * math.sin(th)
        pts.append(tangent_pt(ra0, dec0, x, y))
    return pts


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for k, op in ((1.0, 0.10), (0.7, 0.15), (0.42, 0.24), (0.2, 0.36)):
            s.poly_fill(runs(ellipse(M42[0], M42[1], 0.55 * k, 0.5 * k, 0.0)), fill=mw, opacity=op)

    return [("深空天體", deep)]


def write_custom(m, S, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n),
                   lambda pts, n=north: m._runs_disc(pts, n))
                m._write_disc(s, north, name)


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ("參", "中國", "amber", "《史記．天官書》「參為白虎。三星直者，是為衡石」；A-12"),
    ("Sah", "埃及", "amber", "Stellarium egyptian 005 Sah（Belmonte 重建）；Pyramid Texts §882（Faulkner Utt. 466，Pepi II 金字塔）"),
    ("Birray Birray", "澳洲（卡米拉羅伊）", "amber", "Stellarium kamilaroi：三個男孩；參宿七是營火、劍是撥火棍"),
    ("SIPA.ZI.AN.NA", "安努的忠實牧人（巴比倫）", "purple", "MUL.APIN I；Stellarium babylonian_mulapin"),
    ("Ὠρίων", "獵人俄里翁（希臘）", "white", "Aratus《Phaenomena》634–646：蠍子升起，他就落下"),
    ("al-Jawzā", "一位女子（阿拉伯）", "blue", "Kunitzsch；Stellarium arabic_arabian_peninsula（女子的名字）；A-13"),
    ("Tuivaé", "老人（圖皮）", "green", "Afonso 2006：妻子砍斷他膝下的腿；腰帶＝好腿的膝蓋、參宿六＝腳、參宿四＝斷處"),
    ("Mabukuli", "沒有大腿的人（洛科諾）", "blue", "Stellarium lokono 004（Rybka 2018；Penard、de Goeje）"),
    ("Kama tâla", "貘的下巴（畢宿）", "blue", "Stellarium lokono 005；同一個故事裡獵人的身體；A-15"),
    ("Wücütcha", "神獸的腿（Tikuna）", "purple", "Stellarium tikuna（Faulhaber、Vieira）：Wücütcha's Leg，腰帶是腳趾"),
    ("Oxib' Xk'ub'", "三塊爐石（馬雅）", "red", "Stellarium maya：Alnitak、Saiph、Rigel；M42＝創世之火的煙"),
    ("Mamalhuaztli", "鑽火棍（阿茲特克）", "amber", "Stellarium aztec：每 52 年的新火 toxiuh molpilia"),
    ("ʼAtséʼetsʼózí", "第一個瘦長的人（納瓦荷）", "blue", "Childrey《Star Trails Navajo》pp.58–60"),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=0,
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

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)

    T = {t[0]: t for t in TERMS}

    def pair(a, orig, dx, dy, s1, s2, gap, key=None, zh=None, color=None):
        _, z, col, _ = T[orig]
        k = key or orig
        return [item(a, orig, color or col, s1, dx, dy + gap / 2, k),
                item(a, zh or z, "white", s2, dx, dy - gap / 2, k + "-zh")]

    def lone(a, text, color, size, dx, dy, key):
        return [item(a, text, color, size, dx, dy, key)]

    # ── 開場（迄格 fov 30）：三個名字橫排在腰帶下方 ──
    LB_OPEN = (pair(BELT, "參", -10.5, -14.0, 1.5, 1.0, 2.4, key="開-參") +
               pair(BELT, "Sah", -3.5, -14.0, 1.5, 1.0, 2.4, key="開-Sah") +
               pair(BELT, "Birray Birray", 7.0, -14.0, 1.05, 1.0, 2.4, key="開-Bir", zh="澳洲"))
    # ── 巨人 ──
    LB_SAH = pair(BELT, "Sah", -10.5, -17.0, 2.0, 1.25, 2.9, key="埃-Sah")
    # 三對疊在人形正下方（左側被巴比倫牧人的長線佔滿）
    LB_GIANT = (pair(BELT, "SIPA.ZI.AN.NA", -3.0, -11.0, 1.05, 0.75, 1.6) +
                pair(BELT, "Ὠρίων", -3.0, -14.5, 1.05, 0.75, 1.6) +
                pair(BELT, "al-Jawzā", -3.0, -18.0, 1.05, 0.75, 1.6))
    # ── 一條腿 ──
    LB_TUPI = pair(BELT, "Tuivaé", 2.0, -12.5, 1.9, 1.3, 2.8)
    LB_LOKO = (pair(BELT, "Mabukuli", 2.0, -6.0, 1.5, 0.9, 2.2) +
               pair(HYADES, "Kama tâla", -2.5, -5.5, 1.4, 1.0, 2.2))
    LB_TIKU = pair(BELT, "Wücütcha", -8.3, -5.5, 1.3, 0.85, 2.0)
    # ── 火 ──
    LB_KAMI = (pair(BELT, "Birray Birray", 1.0, 4.5, 1.25, 0.85, 1.9, key="澳-Bir", zh="三個男孩（澳洲）") +
               lone([RIGEL], "營火", "red", 1.1, 3.6, -1.6, "澳-火") +
               lone(SWORD_HIPS, "撥火棍", "red", 0.95, -3.6, -0.6, "澳-棍"))
    LB_MAYA = (pair([ALNITAK, SAIPH, RIGEL], "Oxib' Xk'ub'", 0.0, -5.5, 1.0, 0.72, 1.55) +
               lone(M42, "煙", "white", 0.6, 1.0, 0.0, "馬-煙") +
               lone(M42, "獵戶座大星雲", "white", 0.3, 0.0, -1.25, "馬-M42"))
    LB_AZT = pair(BELT, "Mamalhuaztli", 0.0, 2.4, 0.6, 0.42, 0.95)        # 腰帶上方的空天區
    # ── 星名（物理）──
    LB_STARS = (lone([MINTAKA], "參宿三", "white", 0.32, 1.4, -0.2, "星-3") +
                lone([ALNILAM], "參宿二", "white", 0.32, 1.3, -0.55, "星-2") +
                lone([ALNITAK], "參宿一", "white", 0.32, 1.3, -0.5, "星-1") +
                lone(M42, "獵戶座大星雲", "white", 0.32, 0.0, -1.15, "星-M42"))
    # ── 今晚 ──
    LB_TONIGHT = (lone([BETELGEUSE], "參宿四", "red", 1.3, -4.2, 0.0, "今-4") +
                  lone([RIGEL], "參宿七", "blue", 1.3, 3.8, -1.5, "今-7") +
                  lone(BELT, "腰帶", "amber", 1.3, 3.9, 1.0, "今-帶") +
                  lone([SIRIUS], "天狼星", "white", 1.3, 0.0, -2.4, "今-狼"))
    # ── 下集 ──
    LB_NAV = pair(BELT, "ʼAtséʼetsʼózí", 1.0, -12.0, 1.45, 0.85, 2.2)

    label_sets = [(LB_OPEN, "開場"), (LB_SAH, "埃及"), (LB_GIANT, "巨人"), (LB_TUPI, "圖皮"),
                  (LB_LOKO, "洛科諾"), (LB_TIKU, "Tikuna"), (LB_KAMI, "澳洲的火"), (LB_MAYA, "馬雅"),
                  (LB_AZT, "阿茲特克"), (LB_STARS, "星名"), (LB_TONIGHT, "今晚"), (LB_NAV, "納瓦荷")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    custom = custom_layers(m, S)
    write_custom(m, S, custom)
    m.L_marks(MAINS, "主角星白點", "dot")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot")])
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    xb, yb = m.pos_primary(*centroid(BELT, S))
    xb, yb = round(xb, 1), round(yb, 1)
    WIDE = (-2.0, 0.0, 46.0, 0.0)                        # 開場：整片冬季星空
    ORI = (xb, yb - 2.0, 30.0, 0.0)                      # 整個獵戶
    SAHF = (-1.0, -13.0, 32.0, 0.0)                      # 埃及 Sah（往南到天鴿）
    GIANT = (xb - 3.0, yb, 30.0, 0.0)                    # 巨人：左邊留給三個名字
    TUPI = (11.0, 6.0, 36.0, 0.0)                        # 圖皮老人：獵戶＋金牛＋昴宿
    LOKO = (7.5, 5.0, 30.0, 0.0)                         # 腰帶＋畢宿
    TIKU = (-3.0, -9.0, 26.0, 0.0)                       # Tikuna 的腿（往南到天兔）
    FIRE = (xb + 1.0, yb - 4.0, 22.0, 0.0)               # 腰帶＋參宿七＋劍
    xm, ym = m.pos_primary(*centroid([ALNITAK, SAIPH, RIGEL], S))
    MAYA = (round(xm, 1), round(ym, 1), 14.0, 0.0)       # 三塊爐石＋M42
    AZT = (xb, round(yb - 2.0, 1), 9.0, 0.0)             # 腰帶＋劍
    BELTC = (xb, round(yb - 1.8, 1), 7.5, 0.0)           # 星名＋M42
    xs, ys = m.pos_primary(*S[SIRIUS][:2])
    TONIGHT = (-5.5, -4.0, 40.0, 0.0)                   # 獵戶（含盾牌）＋天狼
    NAV = (xb + 1.0, yb + 1.5, 30.0, 0.0)                # 納瓦荷

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=14, north=True,
             frames=[WIDE, ORI], layers=["定位", "腰帶"], labels=ls("開場"), labels_start=[],
             vo="上週在北歐，它們是三個漁夫。今天元旦，跟著這三顆星繞地球一圈：中國叫它參，埃及叫它 Sah，"
                "澳洲叫它 Birray Birray——同一片星空，全世界都認得這三顆星。",
             card="同一片星空，全世界都認得——這三顆星。",
             note="開場字卡；整片冬季星空推近獵戶，腰帶（琥珀）；迄格開三個名字"),
        dict(code="02", kind="Z", sec=23, north=True,
             frames=[ORI], layers=["定位", "腰帶"], labels=[], labels_start=ls("開場"),
             overlay="C-X02-01_正東升起", overlay_layers=["北方層", "台北層", "南方層"],
             vo="為什麼全世界都認得？三顆差不多亮的星，排成一直線，前後不到三度——滿天很難再找到第二組這麼整齊的。"
                "它們又差不多就躺在天赤道上：不管你在北極圈、台灣，還是紐西蘭，都看到它們從正東方升起、正西方落下。"
                "只是到了南半球，整個獵戶是倒過來的。",
             note="畫面不動；定格疊概念圖 C-X02-01（北緯 69.6°→台北→南緯 41.3°，三地都從正東升起）"),
        dict(code="03", kind="Z", sec=20, north=True,
             frames=[ORI, SAHF], layers=["Sah"], labels=ls("埃及"), labels_start=[],
             vo="最古老的紀錄之一在埃及：整個獵戶是星神 Sah，後來跟冥神歐西里斯合為一體。"
                "四千多年前刻在金字塔裡的經文，對死去的法老說：你是那顆大星，是 Sah 的同伴，跟 Sah 一起走過天空。",
             note="拉遠往南；埃及 Sah（琥珀，往南延伸到天兔、天鴿）"),
        dict(code="04", kind="Z", sec=19, north=True,
             frames=[SAHF, GIANT], layers=["牧人"], labels=ls("巨人"), labels_start=ls("埃及"),
             vo="兩河流域叫它「天神安努的忠實牧人」；希臘人說，他是獵人俄里翁，被一隻蠍子螫死——"
                "所以蠍子一從東方升起，他就往西邊落下。同一個巨人，到了阿拉伯，卻是一位女子，叫 al-Jawzā。",
             note="推回獵戶；巴比倫的牧人（紫）；左邊三個名字"),
        dict(code="05", kind="S", sec=20, north=True,
             frames=[GIANT, TUPI], layers=["老人"], labels=ls("圖皮"), labels_start=ls("巨人"),
             vo="到了南美洲，它變成一條腿。巴西的圖皮人說：一位老人的妻子愛上了他的弟弟，"
                "砍斷了他膝蓋以下的腿；眾神可憐他，把他放上天——腰帶是他那條好腿的膝蓋，紅色的參宿四，標出斷掉的地方。",
             note="往右上（西北）滑；圖皮老人（綠，獵戶＋金牛＋昴宿）"),
        dict(code="06", kind="S", sec=19, north=True,
             frames=[TUPI, LOKO], layers=["洛科諾"], labels=ls("洛科諾"), labels_start=ls("圖皮"),
             vo="南美北岸的洛科諾人說：一個打不到獵物的獵人，切下自己的腿，騙家人說是貘肉，後來上了天——"
                "他的身體變成畢宿，就是上週說的「貘的下巴」；腰帶，叫「沒有大腿的人」。",
             note="推近；洛科諾（藍）：腰帶＋畢宿的 V"),
        dict(code="07", kind="S", sec=15, north=True,
             frames=[LOKO, TIKU], layers=["腿"], labels=ls("Tikuna"), labels_start=ls("洛科諾"),
             overlay="C-X02-02_一條腿", overlay_layers=["圖皮層", "洛科諾層", "提庫納層"],
             vo="亞馬遜的 Tikuna 人也說，這裡是一條腿——天上神獸 Wücütcha 的腿，腰帶是牠的腳趾。"
                "三個民族，隔著上千公里，都在這三顆星上看見一條腿。",
             note="往左下滑；Tikuna 的腿（紫）；之後定格疊概念圖 C-X02-02（圖皮 → 洛科諾 → Tikuna）"),
        dict(code="08", kind="Z", sec=13, north=True,
             frames=[TIKU, FIRE], layers=["腰帶"], labels=ls("澳洲的火"), labels_start=[],
             vo="另一條線索是火。澳洲卡米拉羅伊人的三個男孩 Birray Birray，就是腰帶；"
                "他們的營火是參宿七，下面那把劍，是撥火的棍子。",
             note="推近；腰帶（琥珀）；營火＝參宿七、撥火棍＝劍"),
        dict(code="09", kind="Z", sec=14, north=True,
             frames=[FIRE, MAYA], layers=["爐石", "深空"], labels=ls("馬雅"), labels_start=ls("澳洲的火"),
             vo="中美洲的馬雅人，看見的是創世的那一把火：參宿一、參宿六、參宿七，是火爐的三塊石頭，"
                "中間那團獵戶座大星雲，是火冒出來的煙。",
             note="推近三角；馬雅三塊爐石（紅）＋M42 淡光"),
        dict(code="10", kind="Z", sec=15, north=True,
             frames=[MAYA, AZT], layers=["鑽火", "深空"], labels=ls("阿茲特克"), labels_start=ls("馬雅"),
             overlay="C-X02-03_三地的火", overlay_layers=["澳洲層", "馬雅層", "阿茲特克層"],
             vo="阿茲特克人說，這裡是鑽火的木棍。每五十二年，曆法走完一輪，所有的火都要熄掉，"
                "祭司在山頂鑽出新的火；鑽不出來，太陽就不會再升起。",
             note="推近腰帶＋劍；阿茲特克鑽火棍（琥珀）；之後定格疊概念圖 C-X02-03（澳洲 → 馬雅 → 阿茲特克）"),
        dict(code="11", kind="Z", sec=20, north=True,
             frames=[AZT, ORI], layers=["腰帶"], labels=[], labels_start=[],
             overlay="C-X02-05_腰帶的名字",
             vo="這幾個月，我們在這三顆星上看過：日本的犁、蒙古的三頭母鹿、西伯利亞打穀的人、那馬人的三匹斑馬、"
                "因紐特奔跑的人、北歐的三個漁夫。全世界的名字，我們整理成一張圖卡，可以存起來。",
             note="拉遠；之後疊 9:16 圖卡 C-X02-05 腰帶的名字（可存圖）"),
        dict(code="12", kind="Z", sec=20, north=True,
             frames=[ORI, BELTC], layers=["深空"], labels=ls("星名"), labels_start=[],
             overlay="C-X02-04_年輕的巨星", overlay_layers=["亮度層", "年齡層"],
             vo="它們其實是一群年輕的藍色巨星，每一顆都比太陽亮十幾萬倍以上，離我們大約一千兩百多光年。"
                "它們才幾百萬歲——恐龍滅絕的時候，它們還沒出生；底下那團星雲，現在還在生出新的星星。",
             note="推近腰帶＋M42（不開連線）；之後定格疊概念圖 C-X02-04（亮度 → 年齡）"),
        dict(code="13", kind="Z", sec=22, north=True,
             frames=[BELTC, TONIGHT], layers=[], labels=ls("今晚"), labels_start=[],
             overlay="C-X02-06_今晚往東南東看",
             vo="今晚八點，往東南東看：獵戶已經爬到半天高，整個橫躺著——左邊紅的是參宿四，右邊藍白的是參宿七，"
                "中間就是腰帶；腰帶正下方最亮的那顆，是天狼星。月亮要到半夜一點多才升起，整晚都很暗。",
             note="拉遠到獵戶＋天狼（不開連線：起格 fov 7.5 的連線會粗到 20px 以上）；之後疊 9:16 圖卡 今晚往東南東看（台北 1/1 20:00；可存圖）"),
        dict(code="14", kind="Z", sec=13, north=True,
             frames=[TONIGHT, NAV], layers=["納瓦荷"], labels=ls("納瓦荷"), labels_start=[],
             vo="下週五，我們去北美的納瓦荷：他們叫這個人「第一個瘦長的人」，看見他在黃昏落下，就該播種了——"
                "而他的故事，只能在冬天講。",
             card="下集見｜納瓦荷：只在冬天說的星星故事",
             note="推回獵戶；納瓦荷「第一個瘦長的人」（藍）；端卡＋追蹤 CTA"),
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

    print(f"  x：參宿二 {x_of(S[ALNILAM][0]):+.1f}、參宿四 {x_of(S[BETELGEUSE][0]):+.1f}、參宿七 {x_of(S[RIGEL][0]):+.1f}、"
          f"天狼 {x_of(S[SIRIUS][0]):+.1f}、畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、昴宿六 {x_of(S[ALCYONE][0]):+.1f}；"
          f"爐石框 {MAYA}、今晚框 {TONIGHT}")

    EN = {"參": "Three (Shen)", "Sah": "Sah", "Birray Birray": "Uninitiated boys",
          "SIPA.ZI.AN.NA": "Faithful Shepherd of Anu", "Ὠρίων": "Orion", "al-Jawzā": "al-Jawzā'",
          "Tuivaé": "Old Man", "Mabukuli": "Man without a thigh", "Kama tâla": "Jaw of the tapir",
          "Wücütcha": "Wücütcha's leg", "Oxib' Xk'ub'": "Three hearthstones (Primordial Fire)",
          "Mamalhuaztli": "The New Fire (fire drill)", "ʼAtséʼetsʼózí": "First Slim One"}
    terms = {o: dict(原文=o, 拼音="", 英文翻譯=EN.get(o, ""), 中文=z, 顏色=c, 來源備註=n) for o, z, c, n in TERMS}
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)

    print("\n── 預覽與分鏡 ──")
    def shot_groups(sh):
        g = []
        for k in sh.get("layers", []):
            g += LINE_GROUPS.get(k, [])
        return g

    # 預覽：每組標籤只配「用到它的鏡頭」的連線層（全部疊上會糊成一團）
    for items, name in label_sets:
        g = []
        for sh in shots:
            if name in sh.get("labels", []):
                g += [x for x in shot_groups(sh) if x not in g]
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=g or LG_LOC,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)

    # 鏡頭牆：每格只畫該鏡頭開的連線層與標籤（起格用 labels_start）
    LSD = {n: it for it, n in label_sets}
    panels = iter([(sh, i) for sh in shots for i in range(len(sh["frames"]))])
    draw0 = m.draw_mpl

    def draw_per_shot(ax, line_groups, **kw):
        sh, i = next(panels)
        last = i == len(sh["frames"]) - 1
        names = sh.get("labels", []) if last else sh.get("labels_start", sh.get("labels", []))
        kw["labels"] = [dict(it, pt=5) for n in names for it in LSD[n]]
        return draw0(ax, shot_groups(sh), **kw)
    m.draw_mpl = draw_per_shot
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=[],
              labels=[],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
