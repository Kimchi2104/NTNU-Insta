# -*- coding: utf-8 -*-
"""X-01 昴宿環球之旅：七姊妹的一百個名字｜大畫布 v4.6

論點：同一團小星星，全世界都替它取了名字，而且名字會「分家族」——
  ① 女孩／姊妹（希臘七姊妹、澳洲 Miyay Miyay、滿族七少女、阿拉伯 al-Thurayya），常常伴著一齣追逐戲：
     腰帶三星追七姊妹、畢宿五守著（卡米拉羅伊）；畢宿五是她們的獵人丈夫（那馬）；畢宿五＝「跟在後面的人」（阿拉伯）；
  ② 太平洋的同一個字 *mata-liki：Matariki／Matariʻi／Matāliʻi／Mataliki／Makaliʻi（小眼睛？首領的眼睛？）；
  ③ 母雞與窩：羅馬尼亞、馬其頓、白俄羅斯的母雞，中國二十八禽的昴日雞；西伯利亞鴨巢、圖皮黃蜂窩、提庫納烏龜群；
  ④ 一束／一群：日本すばる（統ばる）、薩丁尼亞「一串」、阿茲特克「市集」；
  ⑤ 一撮毛髮：昴曰髦頭（《史記》）、巴比倫 zappu（鬃毛）、布吉斯 Worong-mpolong（一撮毛）。
  它也是全世界的日曆：六月初黎明重現（紐西蘭 Matariki 新年、洛科諾新年、祖魯人翻土），
  十一月中黃昏升起（夏威夷 Makahiki、大溪地豐收季、薩摩亞新年）；赫西俄德：昴清晨升起收割、清晨西沉犁田。
來源：Stellarium skycultures（舊版 stellarium-skycultures-master 與新版 stellarium-master/skycultures 兩套 index.json
      與 description）；《史記．天官書》；Hesiod《工作與時日》383–384；其餘見逐字稿考據備忘。

鏡頭路線：獵戶→畢→昴開場 → 找到昴宿 → 推近：七還是六（概念圖）→ 拉遠：三段追逐（澳洲／南部非洲／阿拉伯）
→ 推近：太平洋的同一個字（圖卡）→ 母雞 → 窩 → 一束 → 一撮毛髮（圖卡：一百個名字）
→ 拉遠：黎明重現（概念圖）→ 黃昏升起（概念圖）→ 真身（概念圖）→ すばる望遠鏡 → 週末往東看（圖卡）→ 下集白虎。

參數
  lst = 57 → 走廊（x=0）＝RA 57°：昴宿星團 x ≈ +0.3（Alcyone +0.13）；畢宿五 x −12、腰帶 x −26…−28、參宿四 x −32。
  D_s = 52、D_r = 56 → 追逐的大框（fov 46、cy 9）上下緣 −32…+50 都在帶內；盤組照規定生成，本集不用 R 鏡頭。
  D_fill = 0、x_tN = x_tS = 0。
執行：python3 make_x01_v4.py
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-01"
OUT = os.path.join(BASE, "05_素材/X-01_昴宿環球/_v4大畫布")
LST0 = 57.0
TPE = (25.0330, 121.5654)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


LST_AT = {"台北 11/27 19:00": lst_at(*TPE, 8, "2026/11/27 19:00")}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
BETELGEUSE, RIGEL, BELLATRIX, SAIPH = 27989, 24436, 25336, 27366
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
ALDEBARAN = 21421
ALCYONE, ATLAS, ELECTRA, MAIA, MEROPE, TAYGETA = 17702, 17847, 17499, 17573, 17608, 17531
PLEIONE, CELAENO, ASTEROPE = 17851, 17489, 17579
PLEIADS = [ALCYONE, ATLAS, ELECTRA, MAIA, MEROPE, TAYGETA, PLEIONE, CELAENO, ASTEROPE]
MAINS = [BETELGEUSE, RIGEL, MINTAKA, ALNILAM, ALNITAK, ALDEBARAN]

M42 = (83.82, -5.39)
M45 = (56.75, 24.12)
SWORD = (83.82, -5.0)


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


def ra_of(x):
    return (LST0 - x) % 360.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium 舊版＋新版 skycultures）
# ══════════════════════════════════════════════════════════════════
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def sc_lines(culture, new=False):
    p = os.path.join(SC_NEW if new else SC_OLD, culture, "index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
            for c in d["constellations"]}


W = sc_lines("western")
FIG = {   # 文化 → (連線, 顏色, 圖層名)
    "昴宿": (sc_lines("chinese")["015"], "amber", "連線-昴宿（中國）"),
    "MUL": (sc_lines("babylonian_mulapin", True)["034"], "red", "連線-MUL.MUL（巴比倫）"),
    "七少女": (sc_lines("chinese_manchu", True)["Narhu"], "purple", "連線-七少女（滿族）"),
    "大溪地": (sc_lines("ruanui_sky_tahiti_and_society_islands", True)["001"], "blue", "連線-Matariʻi（大溪地）"),
    "母雞": (sc_lines("romanian")["Ccp"], "green", "連線-母雞（羅馬尼亞）"),
    "鴨巢": (sc_lines("siberian")["DNe"], "green", "連線-鴨巢（西伯利亞）"),
    "蜂窩": (sc_lines("tupi")["006"], "green", "連線-黃蜂窩（圖皮）"),
    "すばる": (sc_lines("japanese_moon_stations")["18"], "amber", "連線-すばる（日本）"),
}
_PLE = {17702, 17847, 17499, 17573, 17608, 17531, 17851, 17489, 17579}
# 定位連線：去掉伸進昴宿的那一段（特寫時會變成一條粗線）
LG_LOC = [([sg for sg in W["Ori"]], "white", 0.75),
          ([sg for sg in W["Tau"] if not (set(sg) & _PLE)], "white", 0.75)]
# 文化連線只在星團特寫（fov 2.6–3）用：線寬 0.08 倍 ≈ 0.024 單位 ≈ 9 px
LG_FIG = {k: [(segs, col, 0.08)] for k, (segs, col, _) in FIG.items()}
LG_ALL = LG_LOC + [g for k in FIG for g in LG_FIG[k]]
LINE_SETS = [(LG_LOC, "連線-定位（獵戶、金牛）")] + [(LG_FIG[k], FIG[k][2]) for k in FIG]
LINES_KEY = {"L4": "星座連線", "定位": "連線-定位（獵戶、金牛）", "深空": "深空天體"}
LINES_KEY.update({k: FIG[k][2] for k in FIG})
LINE_GROUPS = {"L4": LG_ALL, "定位": LG_LOC}
LINE_GROUPS.update(LG_FIG)


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋假名＋外文音節；與 A 系列同一套算法，另計假名與〇）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻ]+|[α-ω]|\d+|[㐀-鿿〇぀-ゟ゠-ヿ]", t):
        if re.match(r"[㐀-鿿〇぀-ゟ゠-ヿ]", w):
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
# 四、自訂圖層：深空天體（M45 星雲光＋暗星、M42）
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


def cluster_stars(S, ra0, dec0, rad, vmax):
    out = []
    c = math.cos(math.radians(dec0))
    for h, (ra, dec, v) in S.items():
        if v > vmax or abs(dec - dec0) > rad:
            continue
        if math.hypot((ra - ra0) * c, dec - dec0) > rad:
            continue
        out.append((ra, dec, v))
    return out


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*M42, 0.5, 0.45, 0.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.15), (0.42, 0.24), (0.2, 0.36)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        # 昴宿反射星雲（梅洛普星雲一帶）：中心偏南，三層淡光
        for (dra, ddec, a, op) in ((0.0, 0.0, 1.1, 0.06), (0.0, 0.0, 0.7, 0.08),
                                   (-0.12, -0.12, 0.32, 0.10), (0.15, 0.25, 0.25, 0.08)):
            s.poly_fill(runs(ellipse(M45[0] + dra, M45[1] + ddec, a, a * 0.8, 20.0)), fill=mw, opacity=op)
        dots = []
        for ra, dec, v in cluster_stars(S, *M45, 1.3, 8.5):
            if v <= m.maglim:
                continue
            for p in pos(ra, dec):
                dots.append((p[0], p[1], 0.03 + 0.016 * (8.5 - v)))
        if dots:
            s.dots(dots, fill="#FFFFFF", opacity=0.85)

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
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=52, D_r=56, D_fill=0,
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

    def item(a, text, color, size, dx, dy, key, side=0):
        """side=±1：標籤放在錨點右／左邊，dx 自動加半個字寬（東在左）"""
        if side:
            w, _ = MC.label_box(text, size, m.fu)
            dx = side * (abs(dx) + w / 2)
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 3),
                    dy=round(dy, 3), key=key)

    BELT = [MINTAKA, ALNILAM, ALNITAK]
    PLE = PLEIADS

    # ── 定位（中景 fov 14–28）──
    LOC = [item(BELT, "獵戶的腰帶", "white", 1.2, 2.0, 0.0, "腰帶", side=-1),
           item([ALDEBARAN], "畢宿五", "white", 1.2, 1.2, 0.0, "HIP 21421", side=-1),
           item(M45, "昴宿星團", "amber", 1.4, 0.0, 1.9, "M45")]
    NEAR = [item(M45, "昴宿星團", "amber", 0.7, 0.0, 1.05, "M45-near")]   # fov 12

    # ── 星等（特寫 fov ≈ 4.6；標在星的旁邊）──
    # 特寫 fov 3 時星點半徑 ≈ (6.5−V)^1.7×0.016 單位（Alcyone 0.14 ≈ 51 px），
    # 標籤要讓開整顆星盤，不然白字壓白盤看不見：(星, 字, 左右, 橫移, 縱移)
    MAG = [(ALCYONE, "2.9", 0, 0.0, -0.217), (ATLAS, "3.6", -1, 0.125, 0.0), (ELECTRA, "3.7", 1, 0.12, 0.0),
           (MAIA, "3.9", -1, 0.11, 0.0), (MEROPE, "4.2", 0, 0.0, -0.15), (TAYGETA, "4.3", 1, 0.09, 0.0),
           (PLEIONE, "5.1", 0, 0.0, 0.111), (CELAENO, "5.5", 1, 0.04, 0.0), (ASTEROPE, "5.8", 0, 0.0, 0.095)]
    XD = [item([h], t, "white" if float(t) < 4.5 else "blue", 0.06, dx, dy, f"mag-{h}", side=sd)
          for h, t, sd, dx, dy in MAG]

    # ── 三段追逐（大框 fov 40–46）──
    TITLE = (ra_of(-14.0), 33.0)          # 標題放上方（下方是 Reels 字幕區）
    AU = [item(PLE, "Miyay Miyay　七姊妹", "purple", 1.4, -4.5, 2.8, "Miyay"),
          item(BELT, "Birray Birray　三個男孩", "purple", 1.4, 1.6, 0.8, "Birray", side=1),
          item([ALDEBARAN], "Old Dthillar　守著她們的老人", "purple", 1.3, 0.0, -2.6, "Dthillar"),
          item(TITLE, "澳洲・卡米拉羅伊", "purple", 1.8, 0.0, 0.0, "AU-title")]
    NA = [item(PLE, "天神的女兒（獵人的妻子）", "green", 1.4, -6.0, 2.8, "Khoi-wives"),
          item([ALDEBARAN], "獵人", "green", 1.5, 0.0, -2.6, "Khoi-hunter"),
          item(BELT, "三匹斑馬", "green", 1.4, 1.6, 0.8, "Khoi-zebras", side=1),
          item(SWORD, "射偏的箭", "green", 1.3, 1.2, -0.3, "Khoi-arrow", side=1),
          item([BETELGEUSE], "獅子", "green", 1.3, 1.4, 0.0, "Khoi-lion", side=1),
          item(TITLE, "南部非洲・那馬人", "green", 1.8, 0.0, 0.0, "NA-title")]
    AR = [item(PLE, "al-Thurayya　一位女子", "amber", 1.4, -4.5, 2.8, "Thurayya"),
          item(PLE, G.rtl("الثريا"), "amber", 1.4, -4.5, 5.0, "Thurayya-ar"),
          item([ALDEBARAN], "al-Dabaran　跟在後面的人", "amber", 1.3, 0.0, -2.6, "Dabaran"),
          item([ALDEBARAN], G.rtl("الدبران"), "amber", 1.3, 0.0, -4.6, "Dabaran-ar"),
          item(TITLE, "阿拉伯", "amber", 1.8, 0.0, 0.0, "AR-title")]

    # ── 特寫的跨文化堆疊（fov ≈ 4.0–4.6；整疊放在星團下方空天區）──
    def stack(rows, color, x0, y0, step=0.13, size=0.065, gap=(-0.62, 0.55), key=""):
        """兩欄：左欄原文、右欄中譯（各自置中），整疊放在星團下方空天區"""
        out = []
        for i, (nat, zh, k) in enumerate(rows):
            y = y0 - i * step
            out.append(item((ra_of(x0 + gap[0]), y), nat, color, size, 0.0, 0.0, f"{key}-{k}"))
            out.append(item((ra_of(x0 + gap[1]), y), zh, color, size, 0.0, 0.0, f"{key}-{k}-zh"))
        return out

    SX, SY = x_of(M45[0]), 23.78          # 星團正下方（Merope 23.95 再往下 0.17）
    PAC = stack([("Matariki", "毛利、阿努塔", "mao"), ("Matariʻi", "大溪地", "tah"),
                 ("Matāliʻi", "薩摩亞", "sam"), ("Mataliki", "東加", "ton"), ("Makaliʻi", "夏威夷", "haw")],
                "blue", SX, SY, key="pac")
    HEN = stack([("Cloșca cu pui", "母雞帶小雞（羅馬尼亞）", "rom"), ("Квачка", "母雞（馬其頓）", "mac"),
                 ("Куркі", "母雞（白俄羅斯）", "bel"), ("昴日雞", "中國二十八禽", "chn")],
                "green", SX, SY, key="hen")
    NEST = stack([("Утиное гнездо", "鴨巢（西伯利亞）", "sib"), ("Eixu", "黃蜂窩（巴西圖皮）", "tup"),
                  ("Baweta", "一群烏龜（亞馬遜提庫納）", "tik")],
                 "green", SX, SY, key="nest")
    BUN = stack([("すばる", "統ばる：束成一把（日本）", "jap"), ("S'Udrone", "一串（薩丁尼亞）", "sar"),
                 ("Tianquiztli", "市集（阿茲特克）", "azt")],
                "amber", SX, SY, key="bun")
    HAIR = stack([("昴曰髦頭", "《史記．天官書》", "chn"), ("zappu", "鬃毛（巴比倫）", "bab"),
                  ("Worong-mpolong", "一撮毛（印尼布吉斯）", "bug")],
                 "red", SX, SY, key="hair")
    SUB = [item(M45, "すばる", "amber", 0.30, 0.0, 0.85, "sub-jp"),
           item(M45, "Makaliʻi", "blue", 0.24, 0.0, -0.80, "sub-haw")]

    label_sets = [(LOC, "定位"), (NEAR, "近看"), (XD, "星等"), (AU, "澳洲"), (NA, "南非"), (AR, "阿拉伯"),
                  (PAC, "太平洋"), (HEN, "母雞"), (NEST, "窩"), (BUN, "一束"), (HAIR, "一撮毛"),
                  (SUB, "すばる")]

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
    write_custom(m, S, custom)
    m.L_marks(MAINS, "主角星白點", "dot")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot")])
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    PX = x_of(M45[0])
    F_OPEN = (-14.0, 8.0, 46.0, 0.0)          # 獵戶到昴宿
    F_TAU = (-7.0, 17.0, 26.0, 0.0)           # 畢宿＋昴宿
    F_PLE = (PX - 1.0, 22.5, 12.0, 0.0)       # 昴宿與四周
    F_Z = (PX, 24.05, 3.0, 0.0)               # 昴宿特寫（星團寬 1.1 單位≈畫面 37%）
    F_Z2 = (PX, 24.05, 2.6, 0.0)              # 再推近一點
    F_CHASE = (-12.0, 9.0, 46.0, 0.0)         # 追逐：參宿四到昴宿
    F_CHASE_B = (-12.0, 9.0, 42.0, 0.0)
    F_CHASE_C = (-10.0, 11.0, 40.0, 0.0)
    F_WIDE = (-10.0, 12.0, 50.0, 0.0)
    F_TONIGHT = (-8.0, 16.0, 30.0, 0.0)
    F_TIGER = (-14.0, 10.0, 44.0, 0.0)        # 下集：白虎（參到昴）

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=13, north=True,
             frames=[F_OPEN, F_TAU], layers=["定位", "深空"], labels=[],
             vo="上週在阿努塔，這一小團星叫 Matariki——小小的臉、小小的眼睛。今晚跟著它繞地球一圈："
                "同一片星空，全世界都看見——這一小團星。",
             card="同一片星空，全世界都看見——這一小團星。",
             note="開場字卡；從獵戶拉到畢、昴（定位連線淡淡的）"),
        dict(code="02", kind="Z", sec=15, north=True,
             frames=[F_TAU, F_PLE], layers=["定位", "深空"], labels_start=[], labels=ls("近看"),
             vo="找它不難：從獵戶的腰帶，順著三顆星的方向延伸出去，先經過紅色的畢宿五，再過去一點，"
                "一小團擠在一起的星星——昴宿星團。西方叫它 Pleiades，七姊妹。",
             note="推向昴宿；迄格開「昴宿星團」"),
        dict(code="03", kind="Z", sec=25, north=True,
             frames=[F_PLE, F_Z], layers=["深空"], labels_start=ls("近看"), labels=ls("星等"),
             overlay="C-X01-01_七還是六", overlay_layers=["星點層", "星等層", "傳說層"],
             vo="它叫七姊妹，但大多數人只數得到六顆：最亮的六顆都在四點三等以內，第七亮的只有五點一等，"
                "城市裡幾乎看不到。澳洲的卡米拉羅伊人說，七姊妹裡有一個害羞，躲起來了；"
                "北美的黑腳族乾脆說，那是六個沒人照顧的孩子。",
             note="推近星團；迄格開星等；結束後疊概念圖 七還是六（星點層→星等層→傳說層）"),
        dict(code="04", kind="Z", sec=12, north=True,
             frames=[F_Z, F_CHASE], layers=["定位", "深空"], labels_start=ls("星等"), labels=ls("澳洲"),
             vo="七姊妹的故事，常常是一場追逐。卡米拉羅伊人說：腰帶三星是三個男孩，一直追著她們；"
                "畢宿五是守在中間的老人。",
             note="從星團拉遠到參宿四～昴宿；迄格開澳洲標籤"),
        dict(code="05", kind="Z", sec=13, north=True,
             frames=[F_CHASE, F_CHASE_B], layers=["定位", "深空"], labels_start=ls("澳洲"), labels=ls("南非"),
             vo="南部非洲的那馬人說：她們是天神的女兒，嫁給了獵人畢宿五；獵人朝腰帶的三匹斑馬射了一箭，"
                "沒射中，箭還插在那裡——就是獵戶的劍。",
             note="緩推；澳洲標籤換南非標籤"),
        dict(code="06", kind="Z", sec=11, north=True,
             frames=[F_CHASE_B, F_CHASE_C], layers=["定位", "深空"], labels_start=ls("南非"),
             labels=ls("阿拉伯"),
             vo="阿拉伯人說，昴是一位女子，叫 al-Thurayya；畢宿五叫 al-Dabaran——「跟在後面的人」，"
                "跟了幾千年，還沒追上。",
             note="緩推；南非標籤換阿拉伯標籤"),
        dict(code="07", kind="Z", sec=24, north=True,
             frames=[F_CHASE_C, F_Z], layers=["大溪地", "深空"], labels_start=ls("阿拉伯"),
             labels=ls("太平洋"),
             overlay="C-X01-02_太平洋的同一個字",
             vo="到了太平洋，它幾乎是同一個字：毛利和阿努塔叫 Matariki，大溪地叫 Matariʻi，薩摩亞叫 Matāliʻi，"
                "東加叫 Mataliki，夏威夷叫 Makaliʻi。語言學家把它們還原成同一個古字 mata-liki，「小小的眼睛」；"
                "毛利的老傳說則說，那是天神的眼睛。",
             note="推回星團；大溪地 Matariʻi 連線；迄格開太平洋堆疊；結束後疊 9:16 圖卡 太平洋的同一個字"),
        dict(code="08", kind="Z", sec=14, north=True,
             frames=[F_Z, F_Z2], layers=["母雞", "深空"], labels_start=ls("太平洋"), labels=ls("母雞"),
             vo="往東歐走，它變成一隻母雞：羅馬尼亞是母雞帶小雞，馬其頓叫 Kvachka，白俄羅斯叫 Kurki——"
                "都是母雞。中國的二十八禽，昴也是一隻雞：昴日雞。",
             note="緩推；羅馬尼亞母雞連線；母雞堆疊"),
        dict(code="09", kind="Z", sec=11, north=True,
             frames=[F_Z2, F_Z], layers=["鴨巢", "深空"], labels_start=ls("母雞"), labels=ls("窩"),
             vo="也有人看見一個窩：西伯利亞是鴨巢，巴西的圖皮人看成黃蜂窩；亞馬遜的提庫納人說，"
                "那是一群烏龜。",
             note="緩拉；西伯利亞鴨巢連線；窩堆疊"),
        dict(code="10", kind="Z", sec=12, north=True,
             frames=[F_Z, F_Z2], layers=["すばる", "深空"], labels_start=ls("窩"), labels=ls("一束"),
             vo="也有人只說它是一束：日本的すばる，來自「統ばる」——把散的東西束成一把；"
                "薩丁尼亞叫它「一串」，阿茲特克叫它「市集」，人擠人。",
             note="緩推；日本すばる連線；一束堆疊"),
        dict(code="11", kind="Z", sec=18, north=True,
             frames=[F_Z2, F_Z], layers=["昴宿", "MUL", "深空"], labels_start=ls("一束"),
             labels=ls("一撮毛"),
             overlay="C-X01-06_七姊妹的一百個名字",
             vo="最遠的巧合在這裡：司馬遷說「昴曰髦頭」，髦，是長長的頭髮；三、四千年前的巴比倫人叫它 zappu，"
                "意思是鬃毛；印尼的布吉斯人叫它 Worong-mpolong，一撮毛。三個地方，都看見一撮毛髮。",
             note="輕拉；中國昴宿＋巴比倫 MUL.MUL 連線；一撮毛堆疊；結束後疊 9:16 圖卡 七姊妹的一百個名字（可存圖）"),
        dict(code="12", kind="Z", sec=24, north=True,
             frames=[F_Z, F_WIDE], layers=["定位", "深空"], labels_start=ls("一撮毛"), labels=[],
             overlay="C-X01-03_黎明重現", overlay_layers=["年輪層", "黎明層"],
             vo="為什麼全世界都盯著它？因為它是日曆。每年六月，它在黎明前重新出現：紐西蘭把這叫 Matariki 新年，"
                "二〇二二年起還放國定假日；南美的洛科諾人從這一天開始新的一年；南非的祖魯人叫它 isiLimela——"
                "挖土的星，清晨看見它，就該下田翻土了。",
             note="拉遠；結束後疊概念圖 黎明重現（年輪層→黎明層）"),
        dict(code="13", kind="Z", sec=20, north=True,
             frames=[F_WIDE, F_TONIGHT], layers=["定位", "深空"], labels_start=[], labels=ls("定位"),
             overlay="C-X01-04_黃昏升起", overlay_layers=["年輪層", "黃昏層"],
             vo="十一月中，它換成在黃昏升起：夏威夷的 Makahiki 新年、大溪地的豐收季，都從這時候開始。"
                "兩千七百年前，希臘的赫西俄德寫：昴清晨升起就收割，清晨西沉就犁田。"
                "這個星期，台北日落時，它已經掛在東方低空。",
             note="輕推；結束後疊概念圖 黃昏升起（年輪層→黃昏層）"),
        dict(code="14", kind="Z", sec=20, north=True,
             frames=[F_TONIGHT, F_Z], layers=["深空"], labels_start=ls("定位"), labels=[],
             overlay="C-X01-05_昴宿的真身", overlay_layers=["數字層", "距離層", "年齡層"],
             vo="它真正的樣子：一千多顆星，一億歲左右——恐龍還在的時候才誕生。距離吵了十幾年："
                "依巴谷衛星量到三百九十光年，其他方法都說更遠；後來電波望遠鏡和蓋亞衛星先後量到約四百四十光年，"
                "才算定案。",
             note="推回星團（不開連線）；結束後疊概念圖 昴宿的真身（數字層→距離層→年齡層）"),
        dict(code="15", kind="Z", sec=14, north=True,
             frames=[F_Z, F_Z2], layers=["深空"], labels_start=[], labels=ls("すばる"),
             vo="日本人把它的名字印在車頭上，還把它送到夏威夷：茂納凱亞山頂那座八點二公尺的大望遠鏡，"
                "就叫すばる——蓋在 Makaliʻi 的故鄉。",
             note="緩推；迄格開 すばる／Makaliʻi 兩個大字"),
        dict(code="16", kind="Z", sec=21, north=True,
             frames=[F_Z2, F_TONIGHT], layers=["定位", "深空"], labels_start=ls("すばる"), labels=ls("定位"),
             overlay="C-X01-07_週末往東看",
             vo="這個週末就去看：天黑以後朝東北東，八點它已經四十幾度高。月亮週六九點、週日十點才升起，"
                "趁它出來之前看最清楚；半夜十一點多，它會經過頭頂。對了，三天前的滿月，才剛從七姊妹面前走過，"
                "擋住了其中好幾顆。",
             note="拉遠；結束後疊 9:16 圖卡 週末往東看（台北 11/28 20:00）"),
        dict(code="17", kind="Z", sec=8, north=True,
             frames=[F_TONIGHT, F_TIGER], layers=["定位", "深空"], labels_start=ls("定位"), labels=[],
             vo="下週五回到中國：昴，就長在白虎的身上。",
             card="下集見｜白虎：參宿與西羌的冬夜",
             note="拉遠到參～昴（白虎的身體）；端卡＋追蹤 CTA"),
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
            ew = 360.0 / fov * 1080
            off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "大畫布圖層組", "元素寬px": round(ew), "位移X px": off[0],
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

    mags = {h: S[h][2] for h in PLEIADS}
    print("\n  昴宿星等：", ", ".join(f"{h}:{v:.2f}" for h, v in sorted(mags.items(), key=lambda kv: kv[1])))

    def T(hips, 中文, 英文, 顏色, 備註, 原文=None):
        return dict(hips=hips, 原文=原文 or 中文.split("（")[0], 拼音="", 英文翻譯=英文, 中文=中文,
                    顏色=顏色, 來源備註=備註)

    terms = {
        "昴宿": T(PLEIADS[:7], "昴宿（髦頭）", "Hairy Head", "amber", "《史記．天官書》昴曰髦頭，胡星也；Stellarium chinese 015"),
        "Pleiades": T(PLEIADS, "七姊妹（希臘）", "Pleiades / Seven Sisters", "white", "Stellarium modern／greek"),
        "Miyay Miyay": T(PLEIADS, "七姊妹（澳洲卡米拉羅伊）", "Seven sisters", "purple", "kamilaroi Miy；一個害羞所以只見六顆"),
        "Birray Birray": T([MINTAKA, ALNILAM, ALNITAK], "三個男孩（卡米拉羅伊：腰帶）", "Uninitiated boys", "purple", "kamilaroi Bir"),
        "Old Dthillar": T([ALDEBARAN], "守護的老人（卡米拉羅伊：畢宿五）", "Old Dthillar", "purple", "kamilaroi Ald"),
        "Nadan Narhū": T(PLEIADS[:7], "七少女（滿族）", "Seven Maidens", "purple", "chinese_manchu Narhu；黃昏東升＝入冬"),
        "al-Thurayya": T(PLEIADS, "al-Thurayya（阿拉伯：一位女子）", "Al-Thurayya", "amber", "arabic_ancient 2604", 原文="الثريا"),
        "al-Dabaran": T([ALDEBARAN], "al-Dabaran（跟在後面的人）", "The Follower", "amber", "arabic_lunar_stations", 原文="الدبران"),
        "Matariki": T(PLEIADS, "Matariki（毛利、阿努塔）", "Small Eyes / Small Face", "blue", "maori M45；anutan M45"),
        "Matariʻi": T(PLEIADS[:7], "Matariʻi（大溪地）", "Small eyes", "blue", "ruanui 001；Matariʻi i niʻa 11–5 月豐收季"),
        "Matāliʻi": T(PLEIADS, "Matāliʻi（薩摩亞）", "Face of Liʻi", "blue", "samoan M45；黃昏升起＝新年"),
        "Mataliki": T([ELECTRA], "Mataliki（東加）", "Pleiades", "blue",
                      "tongan：description 寫 Mataliki，名稱表寫 Motuliki（Stellarium 自相矛盾）"),
        "Makaliʻi": T([CELAENO, ELECTRA], "Makaliʻi（夏威夷）", "The Chief's Eyes", "blue", "hawaiian_starlines MAK；黃昏升起＝Makahiki"),
        "Cloșca cu pui": T(PLEIADS[:5], "母雞帶小雞（羅馬尼亞）", "The Hen with Her Chicks", "green", "romanian Ccp"),
        "Kvachka": T(PLEIADS[:6], "母雞（馬其頓）", "Mother Hen", "green", "macedonian 002", 原文="Квачка"),
        "Kurki": T(PLEIADS[:7], "母雞（白俄羅斯）", "The Hens", "green", "belarusian 003", 原文="Куркі"),
        "Utinoe gnezdo": T(PLEIADS, "鴨巢（西伯利亞）", "Duck Nest", "green", "siberian DNe", 原文="Утиное гнездо"),
        "Eixu": T(PLEIADS[:7], "黃蜂窩（圖皮）", "Wasp nest", "green", "tupi 006（Vespeiro）"),
        "Baweta": T([ALCYONE], "一群烏龜（提庫納）", "Turtle Collective", "green", "tikuna 001；11 月底黃昏重現→雨"),
        "すばる": T(PLEIADS[:4], "すばる（日本：統ばる）", "Subaru", "amber", "japanese_moon_stations 18；A-05"),
        "S'Udrone": T(PLEIADS[:7], "一串（薩丁尼亞）", "The Bunch", "amber", "sardinian 002"),
        "Tianquiztli": T(PLEIADS[:7], "市集（阿茲特克）", "Market", "amber", "aztec 002；新火祭看它過天頂"),
        "zappu": T(PLEIADS[:5], "鬃毛（巴比倫 MUL.MUL）", "Bristle", "red", "babylonian_mulapin 034"),
        "Worong-mpolong": T(PLEIADS, "一撮毛（布吉斯）", "Tuft", "red", "bugis NAME Pleiades"),
        "isiLimela": T([ELECTRA, MAIA], "挖土的星（祖魯、科薩）", "Digging Stars", "white", "zulu／xhosa 001；清晨重現＝翻土"),
        "Yôkoro wiwa": T(PLEIADS[:6], "一大群星（洛科諾）", "Scores of stars", "white", "lokono 003；六月東方首見＝新年"),
        "Sakiattiak": T(PLEIADS[:6], "胸骨（因紐特）", "Breastbone", "white", "inuit 008"),
        "Lost Children": T(PLEIADS[:6], "迷途的孩子（黑腳族）", "Lost Children", "white", "blackfoot NAME Pleiades；六顆"),
    }
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "mains": MAINS, "lines": LINES_KEY,
               "line_groups": {k: v for k, v in LINE_GROUPS.items()},
               "lst_at": LST_AT, "pleiad_mags": mags},
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
              labels=[dict(it, pt=5) for it in LOC + AU + NA + AR],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
