# -*- coding: utf-8 -*-
"""A-12 白虎：參宿與西羌的冬夜｜大畫布 v4.6

論點：獵戶的腰帶，是白虎的三顆星。西方屬金、色白、主秋；秋天主肅殺，所以白虎七宿四周
是一整個秋天——南邊是糧倉、草料、牧場（天倉、天囷、天廩、天庾、芻藁、天苑），
北邊是墳墓、屍堆、磨刀石（大陵、積尸、礪石）；《禮記．月令》孟秋同一個月「農乃登穀」
又「戮有罪，嚴斷刑」。參＝三（金文三星在人頭上；台灣支票大寫三寫「參」），
全世界都替這三顆星數「三」；參商永不相見；天街分華夏與夷狄；1054 年天關客星＝蟹狀星雲；
白虎與西羌（羌＝羊＋人、姜＝羊＋女、彝族「羅羅」或為虎族）是推論、不是定論。
來源：《史記．天官書》（含唐張守節《正義》）、《晉書．天文志》、《左傳．昭公元年》、
《禮記．月令》、《詩經》〈召南．小星〉〈小雅．漸漸之石〉、《宋會要》《宋史．天文志》、
《西遊記》第 28–31、55 回；Stellarium chinese（星官連線）；師大天文社〈中國星座〉簡報 p.16–17。

鏡頭路線：腰帶開場 → 長圖往西滑過七宿（參→奎）→ 二十八禽往回滑到昴 → 參宿特寫（天官書）
→ 參字（概念圖）→ 同一條腰帶（圖卡）→ 參商（概念圖）→ 南：糧倉、牧場、廁 → 北：大陵、礪石（圖卡）
→ 天街 → 天關客星（概念圖）→ 拉遠：白虎與西羌（概念圖）→ 今晚往東看（概念圖）→ 昴宿：下集預告。

輸出：L1銀河 L2星點 L3經緯線 L4星座連線（白虎一帶全部星官）
      連線-七宿／倉／刑／廁／天街天關／其他星官；深空天體（M42、M45、M1）、客星（1054）、主角星白點
      標籤（長圖）：宿名／二十八禽／天官書／倉／刑／廁／天街／天關／星名
執行：python3 make_a12_v4.py

參數
  lst = 50 → 走廊（x=0）＝RA 50°：在胃宿（x +8）與昴宿（x −7）之間，七宿 x +41（奎）… −39（參）左右對稱；
             接縫 x=±180 在 RA 230（天秤），整集不會碰到。
  D_s = 52、D_r = 56 → 七宿（dec −9.7…+41.1）、倉（−28.2…+12.9）、廁屎（−32.3）、礪石卷舌（+42.6）都在帶內；
             大陵頂端（+55.8）落在縫合帶，北邊那格（09）上緣到 +61，只在走廊內（|x|≤20）。
  D_fill = 0 → k=1.685、R_fill=151.7（盤組照規定生成，本集不用 R 鏡頭）。
  x_tN = x_tS = 0（Canva 可水平置中）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-12"
OUT = os.path.join(BASE, "05_素材/A-12_白虎/_v4大畫布")
LST0 = 50.0
TPE = (25.0330, 121.5654)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


LST_AT = {"台北 12/04 20:00": lst_at(*TPE, 8, "2026/12/04 20:00")}


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
BETELGEUSE, RIGEL, BELLATRIX, SAIPH = 27989, 24436, 25336, 27366
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
ALDEBARAN, ALCYONE, HAMAL, ZETA_TAU = 21421, 17702, 9884, 26451
ALGOL = 14576
MAINS = [BETELGEUSE, RIGEL, BELLATRIX, SAIPH, MINTAKA, ALNILAM, ALNITAK,
         ALDEBARAN, ALCYONE, HAMAL, ZETA_TAU]

M42 = (83.82, -5.39)
M45 = (56.75, 24.12)
M1 = (83.633, 22.015)           # 蟹狀星雲（1054 年天關客星的殘骸），6′×4′


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


def ra_of(x):
    return (LST0 - x) % 360.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium chinese index.json）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


C = sc_lines("chinese")
SEVEN = ["012", "014", "025", "015", "001", "034", "003", "069"]       # 奎婁胃昴畢觜參＋伐
GRAN = ["210", "242", "238", "250", "053", "253"]                     # 天倉 天囷 天廩 天庾 芻藁 天苑
DEATH = ["062", "105", "122", "211", "139"]                           # 大陵 積尸 卷舌 天讒 礪石
TOILET = ["047", "188"]                                               # 廁 屎
STREET = ["230", "222"]                                               # 天街 天關
OTHER = ["046", "118", "123", "291", "215", "286", "233", "225", "074", "293"]
# 參旗 九斿 軍井 玉井 天大將軍 右更 天廄 天溷 鈇鑕 月

LG_SEVEN = [(C[k], "amber", 1.0) for k in SEVEN]
LG_GRAN = [(C[k], "green", 1.0) for k in GRAN]
LG_DEATH = [(C[k], "red", 1.0) for k in DEATH]
LG_TOILET = [(C[k], "purple", 1.0) for k in TOILET]
LG_STREET = [(C[k], "blue", 1.0) for k in STREET]
LG_OTHER = [(C[k], "white", 0.7) for k in OTHER]
LG_ALL = LG_SEVEN + LG_GRAN + LG_DEATH + LG_TOILET + LG_STREET + LG_OTHER
LINE_SETS = [(LG_SEVEN, "連線-七宿"), (LG_GRAN, "連線-倉"), (LG_DEATH, "連線-刑"),
             (LG_TOILET, "連線-廁"), (LG_STREET, "連線-天街天關"), (LG_OTHER, "連線-其他星官")]
LINES_KEY = {"L4": "星座連線", "七": "連線-七宿", "倉": "連線-倉", "刑": "連線-刑", "廁": "連線-廁",
             "街": "連線-天街天關", "他": "連線-其他星官", "深空": "深空天體", "客": "客星"}
LINE_GROUPS = {"L4": LG_ALL, "七": LG_SEVEN, "倉": LG_GRAN, "刑": LG_DEATH, "廁": LG_TOILET,
               "街": LG_STREET, "他": LG_OTHER}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


def sep(S, a, b):
    ra1, d1 = (math.radians(x) for x in S[a][:2])
    ra2, d2 = (math.radians(x) for x in S[b][:2])
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A-10/A-11 同一套算法）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouy]+", w.lower().replace("ʻ", " "))))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層：深空天體、1054 客星（大畫布＋南北盤同步出）
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
        for (ra0, dec0, a, b, pa) in [(*M42, 0.5, 0.45, 0.0), (*M1, 0.12, 0.08, 135.0)]:
            for k, op in ((1.0, 0.10), (0.7, 0.15), (0.42, 0.24), (0.2, 0.36)):
                s.poly_fill(runs(ellipse(ra0, dec0, a * k, b * k, pa)), fill=mw, opacity=op)
        for k, op in ((1.0, 0.07), (0.6, 0.10)):
            s.poly_fill(runs(ellipse(*M45, 1.1 * k, 1.1 * k, 0.0)), fill=mw, opacity=op)
        dots = []
        for ra, dec, v in cluster_stars(S, *M45, 1.1, 8.5):
            if v <= m.maglim:
                continue
            for p in pos(ra, dec):
                dots.append((p[0], p[1], 0.05 + 0.028 * (8.5 - v)))
        if dots:
            s.dots(dots, fill="#FFFFFF", opacity=0.85)

    def guest(s, pos, runs):
        """1054 客星：M1 位置的八芒光＋圈（琥珀）"""
        amber = COLORS["amber"]
        for p in pos(*M1):
            x0, y0 = p[0], p[1]
            rays = []
            for i in range(8):
                a = math.radians(22.5 + 45 * i)
                r0, r1 = (0.55, 1.75) if i % 2 == 0 else (0.55, 1.15)
                rays.append([(x0 + r0 * math.cos(a), y0 + r0 * math.sin(a)),
                             (x0 + r1 * math.cos(a), y0 + r1 * math.sin(a))])
            s.polylines(rays, stroke=amber, w=0.16, opacity=0.95)
            s.circle(x0, y0, 0.32, fill=amber, opacity=0.9)
            s.circle(x0, y0, 2.3, stroke=amber, w=0.12, opacity=0.8, dash="0.5 0.35")

    return [("深空天體", deep), ("客星", guest)]


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
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                    dy=round(dy, 2), key=key)

    H = {k: uniq([C[k]]) for k in SEVEN + GRAN + DEATH + TOILET + STREET + OTHER}
    BELT = [MINTAKA, ALNILAM, ALNITAK]

    # ── 宿名＋二十八禽（禽名在宿名下方 2.6 單位）──
    SU = [("012", "奎宿", "奎木狼", 0.0, 0.0),
          ("014", "婁宿", "婁金狗", 0.0, -4.2),
          ("025", "胃宿", "胃土雉", 0.0, 5.4),
          ("015", "昴宿", "昴日雞", 0.0, 4.4),
          ("001", "畢宿", "畢月烏", 1.0, -5.6),
          ("034", "觜宿", "觜火猴", 0.0, 5.2),
          ("003", "參宿", "參水猿", 9.5, -3.0)]
    XIU = [item(H[k], nm, "amber", 2.0, dx, dy, nm) for k, nm, _, dx, dy in SU]
    QIN = [item(H[k], q, "white", 1.4, dx, dy - 2.7, q) for k, _, q, dx, dy in SU]

    # ── 天官書（參宿特寫）──
    TG = [item(BELT, "衡石", "amber", 1.3, 2.4, 0.9, "衡石", side=1),
          item(H["069"], "罰", "amber", 1.3, 0.0, -4.6, "罰"),
          item([BETELGEUSE], "左肩", "amber", 1.3, 1.4, 0.0, "左肩", side=-1),
          item([BELLATRIX], "右肩", "amber", 1.3, 1.4, 0.0, "右肩", side=1),
          item([SAIPH], "左股", "amber", 1.3, 1.4, 0.0, "左股", side=-1),
          item([RIGEL], "右股", "amber", 1.3, 1.4, 0.0, "右股", side=1),
          item(H["034"], "觜觿（虎首）", "amber", 1.3, 0.0, 2.2, "觜觿"),
          item((ra_of(-34.0), -14.6), "參為白虎", "amber", 2.0, 0.0, 0.0, "參為白虎")]

    # ── 白虎的鄰居：南＝倉、北＝刑、腳下＝廁 ──
    GR = [("210", "天倉", "方的糧倉", 6.0, -3.0),
          ("242", "天囷", "圓的糧倉", 0.0, 4.6),
          ("238", "天廩", "祭祀的穀子", 2.5, 4.4),
          ("250", "天庾", "露天穀堆", 0.0, -2.6),
          ("053", "芻藁", "草料", 4.6, 0.6),
          ("253", "天苑", "天子的牧場", 0.0, -9.0)]
    CANG = []
    for k, nm, gl, dx, dy in GR:
        CANG += [item(H[k], nm, "green", 1.7, dx, dy, nm),
                 item(H[k], gl, "green", 1.1, dx, dy - 2.2, nm + "-zh")]
    DT = [("062", "大陵", "墳墓", 4.6, 3.2),
          ("105", "積尸", "屍堆", 2.2, 3.7),
          ("122", "卷舌", "管口舌", -5.6, 1.0),
          ("139", "礪石", "磨刀石", -3.9, 1.2)]
    XING = []
    for k, nm, gl, dx, dy in DT:
        XING += [item(H[k], nm, "red", 1.7, dx, dy, nm),
                 item(H[k], gl, "red", 1.1, dx, dy - 2.2, nm + "-zh")]
    XING.append(item([ALGOL], "大陵五", "red", 1.1, 1.0, 0.0, "Algol", side=-1))
    CE = [item(H["047"], "廁", "purple", 2.0, -4.6, 0.6, "廁"),
          item(H["047"], "茅廁", "purple", 1.1, -4.6, -1.8, "廁-zh"),
          item(H["188"], "屎", "purple", 2.0, 1.4, 0.0, "屎", side=1)]

    # ── 天街：昴畢之間；街北夷狄、街南華夏 ──
    JIE = [item(H["230"], "天街", "blue", 1.8, 1.5, 0.0, "天街", side=1),
           item(H["230"], "街北：夷狄", "blue", 1.2, -4.8, 4.9, "街北"),
           item(H["230"], "街南：華夏", "blue", 1.2, 3.2, -12.6, "街南"),
           item([ALCYONE], "胡星", "amber", 1.3, 0.0, 2.6, "胡星"),
           item([ALDEBARAN], "罕車", "amber", 1.3, 0.0, -2.8, "罕車"),
           item([ALDEBARAN], "邊兵、弋獵", "amber", 1.0, 0.0, -4.6, "罕車-zh")]
    GUAN = [item([ZETA_TAU], "天關", "blue", 1.6, 1.2, -1.0, "天關", side=-1),
            item(M1, "客星 1054", "amber", 1.4, 0.0, 3.4, "客星"),
            item(M1, "蟹狀星雲 M1", "white", 1.0, 0.0, 5.4, "M1")]
    NAMES = [item([BETELGEUSE], "參宿四", "white", 1.1, 0.0, -2.2, "HIP 27989"),
             item([RIGEL], "參宿七", "white", 1.1, 0.0, -2.2, "HIP 24436"),
             item([ALDEBARAN], "畢宿五", "white", 1.1, 0.0, -2.2, "HIP 21421"),
             item([HAMAL], "婁宿三", "white", 1.1, 0.0, -2.2, "HIP 9884")]

    label_sets = [(XIU, "宿名"), (QIN, "二十八禽"), (TG, "天官書"), (CANG, "倉"), (XING, "刑"),
                  (CE, "廁"), (JIE, "天街"), (GUAN, "天關"), (NAMES, "星名")]

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
    BELT0 = (-34.0, 0.0, 24.0, 0.0)          # 腰帶＋伐＋觜
    ORI_W = (-32.0, 4.0, 48.0, 0.0)          # 獵戶全身＋畢、昴（S 上限 |cy|+42.7 ≤ 52）
    WEST = (28.0, 8.0, 48.0, 0.0)            # 奎、婁、胃、天倉
    BIRD = (-8.0, 10.0, 48.0, 0.0)           # 胃、昴、畢（觜在左緣外）
    ORI = (-34.0, 1.0, 30.0, 0.0)            # 參宿＋觜＋伐（天官書）
    ORI_C = (-34.0, 0.0, 18.0, 0.0)          # 參字
    ORI_M = (-32.0, 4.0, 44.0, 0.0)          # 參商（拉遠）
    SOUTH = (15.0, -6.0, 52.0, 0.0)          # 倉：底邊 −52.2（縫合帶內）
    LOW = (-30.0, -16.0, 30.0, 0.0)          # 腳下：廁、屎
    NORTH = (-3.0, 31.0, 34.0, 0.0)          # 大陵、積尸、卷舌、礪石（上緣 +61.2，走廊內）
    JIE_F = (-12.0, 20.0, 26.0, 0.0)         # 天街
    GUAN_F = (-31.0, 17.0, 22.0, 0.0)        # 天關＋M1
    WIDE = (-16.0, 8.0, 52.0, 0.0)           # 拉遠：參到胃
    TONIGHT = (-17.0, 10.0, 48.0, 0.0)
    PLEI = (-6.6, 24.0, 14.0, 0.0)           # 昴宿特寫

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=10, north=True,
             frames=[BELT0, ORI_W], layers=["深空"], labels=[],
             vo="上週在阿努塔，獵戶的腰帶是三星之路。今晚回到中國：同一片星空，古代中國人看見——一隻白虎。",
             card="同一片星空，古代中國人看見——一隻白虎。",
             note="開場字卡；從腰帶拉遠到整個獵戶（先不開連線）"),
        dict(code="02", kind="S", sec=24, north=True,
             frames=[ORI_W, WEST], layers=["七", "深空"], labels_start=[], labels=ls("宿名"),
             vo="古人把天分成四方：東方青龍、北方玄武、南方朱雀、西方白虎，每方七宿，一共二十八宿。"
                "照五行，西方屬金，顏色是白，季節是秋；秋天主肅殺，西方的神獸就是一隻白虎。"
                "牠的七宿從獵戶往西數：參、觜、畢、昴、胃、婁、奎。",
             note="長圖往西（右）滑過七宿：參 → 觜 → 畢 → 昴 → 胃 → 婁 → 奎；迄格開宿名"),
        dict(code="03", kind="Z", sec=24, north=True,
             frames=[WEST, BIRD], layers=["七", "深空"], labels_start=ls("宿名", "二十八禽"),
             labels=ls("宿名", "二十八禽"),
             vo="每一宿還配一隻動物：奎木狼、婁金狗、胃土雉、昴日雞、畢月烏、觜火猴、參水猿。"
                "《西遊記》的黃袍怪，就是奎木狼下凡；昴日星官現出原形是一隻大公雞，叫兩聲就收了蠍子精——"
                "天上的昴宿和蠍子，也正好在天空的兩頭。巧的是，羅馬尼亞人把昴宿看成一隻母雞帶著小雞。",
             note="起格就開宿名＋二十八禽（奎木狼在畫面裡）；往東（左）滑回昴宿（昴日雞）"),
        dict(code="04", kind="Z", sec=19, north=True,
             frames=[BIRD, ORI], layers=["七", "深空"], labels_start=ls("宿名", "二十八禽"),
             labels=ls("天官書"),
             vo="司馬遷在《史記．天官書》寫：「參為白虎。三星直者，是為衡石。」中間一排三顆，是一桿秤；"
                "下面三顆叫「罰」，管斬殺；外圍四顆，是老虎的左右肩、左右腿；上面小小的三角叫觜觿，是虎頭。",
             note="往東推近參宿；迄格開天官書（衡石、罰、左右肩股、觜觿＝虎首）"),
        dict(code="05", kind="Z", sec=14, north=True,
             frames=[ORI, ORI_C], layers=["七", "深空"], labels_start=ls("天官書"), labels=[],
             overlay="C-A12-01_參字", overlay_layers=["三星層", "字形層", "說明層"],
             vo="「參」這個字，金文畫的是三顆星，底下一個人——很多學者認為，畫的就是這三顆。"
                "後來「參」被借去寫數字三：今天在台灣開支票，三還是寫這個參。",
             note="推近腰帶；結束後疊概念圖 參字（三星層→字形層→說明層）"),
        dict(code="06", kind="Z", sec=20, north=True,
             frames=[ORI_C, ORI], layers=["深空"], labels_start=[], labels=[],
             overlay="C-A12-05_同一條腰帶",
             vo="用「三」替它取名的，不只中國：印尼的布吉斯人叫它「三的記號」，阿努塔叫「三星之路」，"
                "羅馬尼亞叫「三聖人」。也有人看成三個人：白俄羅斯是三個割草的人，因紐特是三個迷路的獵人。",
             note="關掉連線、只留星點拉遠；結束後疊 9:16 圖卡 同一條腰帶（可存圖）"),
        dict(code="07", kind="Z", sec=27, north=True,
             frames=[ORI, ORI_M], layers=["七", "深空"], labels_start=[], labels=ls("宿名", "星名"),
             overlay="C-A12-02_參商", overlay_layers=["地平層", "參宿層", "心宿層", "引文層"],
             vo="參宿還有一個死對頭：心宿，古人叫商星。《左傳》說，高辛氏的兩個兒子天天動刀動槍，"
                "帝堯把哥哥閼伯遷到商丘，管商星；把弟弟實沈遷到大夏，管參星——從此兄弟不再相見。"
                "一個升起，另一個就落下；照計算，在台北兩邊同時露出地平線，一天只有十幾分鐘。"
                "杜甫說：「人生不相見，動如參與商。」",
             note="拉遠；結束後疊概念圖 參商（地平層→參宿層→心宿層→引文層）"),
        dict(code="08", kind="Z", sec=22, north=True,
             frames=[ORI_M, SOUTH, LOW], layers=["七", "倉", "廁", "深空"], labels_start=[],
             labels=ls("倉", "廁"),
             vo="白虎四周，是一整個秋天的農場。往南：方的糧倉天倉、圓的糧倉天囷，存祭祀穀子的天廩、"
                "露天穀堆天庾、草料堆芻藁，還有天子養牲口的天苑。老虎腳下，甚至有一間廁所——廁星，"
                "底下那顆就叫「屎」。",
             note="三格：往南下方滑到倉（開倉標籤）→ 再往東（左）滑到參宿腳下的廁、屎；倉＋廁標籤全程開"),
        dict(code="09", kind="Z", sec=22, north=True,
             frames=[LOW, NORTH], layers=["七", "刑", "深空"], labels_start=ls("廁"),
             labels=ls("刑"),
             overlay="C-A12-06_白虎的鄰居",
             vo="往北，是另一種秋天：大陵是墳墓，中間那顆叫積尸；不遠處還有磨刀的礪石。大陵五在西方，"
                "是梅杜莎的頭。《禮記．月令》說，秋天第一個月「農乃登穀」，同一個月「戮有罪，嚴斷刑」——"
                "收成和處決，古人都放在秋天。",
             note="長距離往北（上）滑到大陵；迄格開刑標籤；結束後疊 9:16 圖卡 白虎的鄰居（可存圖）"),
        dict(code="10", kind="Z", sec=21, north=True,
             frames=[NORTH, JIE_F], layers=["七", "街", "深空"], labels_start=ls("刑"),
             labels=ls("天街"),
             vo="昴宿和畢宿之間這兩顆，叫天街。《史記》說昴是「胡星」，畢管邊境的軍隊和打獵；"
                "唐代的注解說得更直接：天街以南是華夏，以北是夷狄。黃道正好穿過這條街，月亮每個月都會走過；"
                "《詩經》說「月離于畢，俾滂沱矣」——月亮靠近畢宿，就要下大雨。",
             note="往下推近天街；迄格開天街標籤（街北夷狄／街南華夏、胡星、罕車）"),
        dict(code="11", kind="Z", sec=22, north=True,
             frames=[JIE_F, GUAN_F], layers=["七", "街", "客", "深空"], labels_start=ls("天街"),
             labels=ls("天關"),
             overlay="C-A12-04_天關客星", overlay_layers=["星圖層", "客星層", "引文層", "今日層"],
             vo="畢宿東邊這顆，叫天關。一〇五四年七月四日，宋朝的天文官記下：一顆客星出現在天關旁，"
                "白天也看得到，亮得像金星，一連二十三天。今天望遠鏡對準那裡，是蟹狀星雲——"
                "一顆超新星的殘骸，中間的中子星，每秒轉三十圈。",
             note="往東（左）推近天關；客星圖層（M1 八芒光＋虛線圈）；結束後疊概念圖 天關客星"),
        dict(code="12", kind="Z", sec=28, north=True,
             frames=[GUAN_F, WIDE], layers=["七", "深空"], labels_start=ls("天關"), labels=ls("宿名"),
             overlay="C-A12-03_西羌線索", overlay_layers=["墓葬層", "字形層", "彝族層", "結論層"],
             vo="白虎有多老？河南濮陽西水坡，六千多年前的一座墓，東邊用蚌殼擺了一條龍，西邊擺了一隻虎。"
                "為什麼西邊是虎？有一種推論：西邊住著羌人。「羌」是羊加人，「姜」是羊加女，"
                "周人的始祖母就叫姜嫄；西南的彝族，不少學者認為源自古羌，有的支系自稱「羅羅」，意思可能是虎族。"
                "線索很誘人，但這是推論，不是定論。",
             note="拉遠到白虎身體（參到胃）；迄格開宿名；結束後疊概念圖 西羌線索（墓葬層→字形層→彝族層→結論層）"),
        dict(code="13", kind="Z", sec=20, north=True,
             frames=[WIDE, TONIGHT], layers=["七", "深空"], labels_start=ls("宿名"), labels=ls("宿名"),
             overlay="C-A12-07_今晚往東看",
             vo="今晚就看得到：十二月初，晚上八點朝東方。頭頂附近是奎宿，昴宿在東方半天高，"
                "紅色的畢宿五在它下面；獵戶剛爬上東方地平線，大約二十度。十二月四日這晚，"
                "月亮要到隔天凌晨快三點才升起，正好看白虎。",
             note="輕推；結束後疊概念圖 今晚往東看（台北 12/4 20:00）"),
        dict(code="14", kind="Z", sec=7, north=True,
             frames=[TONIGHT, PLEI], layers=["深空"], labels_start=ls("宿名"), labels=[],
             vo="下週五，我們跟著昴宿到阿拉伯：沙漠裡的人看它，就知道雨季快來了。",
             card="下集見｜阿拉伯半島：Thurayya 與沙漠的雨季",
             note="推近昴宿；端卡＋追蹤 CTA"),
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

    belt_gap = (sep(S, MINTAKA, ALNILAM), sep(S, ALNILAM, ALNITAK))
    print(f"\n  腰帶間距 參三–參二 {belt_gap[0]:.2f}°、參二–參一 {belt_gap[1]:.2f}°；"
          f"昴宿–心宿二 赤經差 {abs(S[80763][0] - S[ALCYONE][0]):.1f}°；"
          f"天關–M1 {math.hypot((M1[0]-S[ZETA_TAU][0])*math.cos(math.radians(22)), M1[1]-S[ZETA_TAU][1]):.2f}°"
          f"（M1 在天關的{'西北' if M1[0] < S[ZETA_TAU][0] and M1[1] > S[ZETA_TAU][1] else '其他方向'}）")

    def T(hips, 中文, 英文, 顏色, 備註, 原文=None):
        return dict(hips=hips, 原文=原文 or 中文.split("（")[0], 拼音="", 英文翻譯=英文, 中文=中文,
                    顏色=顏色, 來源備註=備註)

    terms = {
        "參宿": T(H["003"], "參宿（三星；白虎之身）", "Three Stars", "amber",
                "《史記．天官書》參為白虎；三星直者是為衡石；其外四星左右肩股"),
        "伐": T(H["069"], "伐／罰（參宿下的三顆）", "Punishment", "amber",
               "《史記．天官書》下有三星，兌，曰罰，為斬艾事"),
        "觜宿": T(H["034"], "觜宿（觜觿＝虎首）", "Turtle Beak", "amber",
                "《史記．天官書》小三星隅置，曰觜觿，為虎首，主葆旅事"),
        "畢宿": T(H["001"], "畢宿（罕車）", "Net", "amber", "《史記．天官書》畢曰罕車，為邊兵，主弋獵"),
        "昴宿": T(H["015"], "昴宿（髦頭、胡星）", "Hairy Head", "amber", "《史記．天官書》昴曰髦頭，胡星也"),
        "胃宿": T(H["025"], "胃宿", "Stomach", "amber", "白虎七宿"),
        "婁宿": T(H["014"], "婁宿", "Bond", "amber", "白虎七宿"),
        "奎宿": T(H["012"], "奎宿", "Legs", "amber", "白虎七宿"),
        "天倉": T(H["210"], "天倉（方的糧倉）", "Square Celestial Granary", "green", "《晉書．天文志》倉穀所藏"),
        "天囷": T(H["242"], "天囷（圓的糧倉）", "Circular Celestial Granary", "green", "囷＝圓形穀倉"),
        "天廩": T(H["238"], "天廩（存祭祀的黍稷）", "Celestial Granary", "green", "主蓄黍稷，以供饗祀"),
        "天庾": T(H["250"], "天庾（露天穀堆）", "Ricks of Grain", "green", "主露積"),
        "芻藁": T(H["053"], "芻藁（草料堆）", "Hay", "green", "主積藁草"),
        "天苑": T(H["253"], "天苑（天子的牧場）", "Celestial Meadows", "green", "天子之苑囿，養獸之所"),
        "大陵": T(H["062"], "大陵（墳墓）", "Mausoleum", "red", "陵者，墓也；大陵五＝Algol（西方：梅杜莎的頭）"),
        "積尸": T(H["105"], "積尸（屍堆）", "Heap of Corpses", "red", "大陵中一星曰積尸"),
        "卷舌": T(H["122"], "卷舌（主口舌）", "Rolled Tongue", "red", "主口語，以知佞讒"),
        "礪石": T(H["139"], "礪石（磨刀石）", "Whetstone", "red", "磨礪鋒刃"),
        "廁": T(H["047"], "廁（茅廁）", "Toilet", "purple", "天廁；屎一星在其南"),
        "屎": T(H["188"], "屎", "Excrement", "purple", "Stellarium chinese 188"),
        "天街": T(H["230"], "天街（華夏與夷狄的國界）", "Celestial Street", "blue",
                "《史記．天官書》昴畢間為天街；《正義》街南為華夏之國，街北為夷狄之國"),
        "天關": T(H["222"], "天關（金牛座 ζ）", "Celestial Pass", "blue",
                "1054 年客星（《宋會要》晝見如太白，凡見二十三日）＝蟹狀星雲 M1"),
    }
    for k, nm, q, _, _ in SU:
        terms[q] = T(H[k], q, "", "white", f"二十八禽：{nm}")
    for items, name in label_sets:
        for it in items:
            if it["key"].startswith("HIP"):
                terms.setdefault(it["key"], dict(hips=[int(it["key"][4:])], 原文=it["text"], 拼音="",
                                                 英文翻譯="", 中文=it["text"], 顏色=it["color"],
                                                 來源備註="台灣通行星名"))
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Tanra Tèlluè", 中譯="三的記號（布吉斯：獵戶腰帶）", 英文="Sign of Three",
                              顏色="white"),
                         dict(原文="Ara Toru", 中譯="三星之路（阿努塔）", 英文="Path of Three", 顏色="white"),
                         dict(原文="Trisfetitele", 中譯="三聖人（羅馬尼亞）", 英文="The Three Saints",
                              顏色="white"),
                         dict(原文="Касцы", 中譯="割草的人（白俄羅斯）", 英文="The Mowers", 顏色="white"),
                         dict(原文="Ullaktut", 中譯="三個迷路的獵人（因紐特）", 英文="Runners", 顏色="white"),
                         dict(原文="Cloșca cu pui", 中譯="母雞帶小雞（羅馬尼亞：昴宿）",
                              英文="The Hen with Her Chicks", 顏色="amber")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "belt_gap_deg": belt_gap},
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
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_SEVEN + LG_GRAN + LG_DEATH
              + LG_TOILET + LG_STREET,
              labels=[dict(it, pt=5) for it in XIU + TG + CANG + XING + CE + JIE + GUAN],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
