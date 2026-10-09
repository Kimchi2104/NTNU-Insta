# -*- coding: utf-8 -*-
"""H-冬至：一根棍子如何量出一年｜大畫布 v4.6

論點：「觀象授時」——白天看影子，晚上看星星。
  ① 影子：立八尺的表、平放一把圭，每天正午量影子；最長的那天就是冬至（《周髀算經》冬至晷長
     一丈三尺五寸、夏至一尺六寸）。從這次最長數到下次最長＝一年＝365¼ 日，所以周天也分成
     365¼ 度：太陽一天走一度。
  ② 越量越準：冬至前後影長幾乎不變 → 祖沖之（南朝宋，大明五年 461）量冬至前後影長相同的兩天、
     折取其中（《宋書．律曆志》）→ 郭守敬（元）四丈高表＋景符；授時曆（1281）歲實 365.2425 日，
     與 1582 年格里曆同值（此值沿用南宋統天曆）。
  ③ 星星：《尚書．堯典》「日短星昴，以正仲冬」——冬至黃昏昴宿在正南。東晉虞喜（330）：
     「堯時冬至日短星昴，今二千七百餘年，乃東壁中」（《宋史．律曆志》引）→ 歲差。
     今晚台北：18:00 正南方是東壁（飛馬座大四邊形東邊），昴宿 21:38 才到頭頂（高度 89°）。
之後：今天怎麼看（圖卡）→ 下集 A-15 北歐：畢宿的狼嘴 Úlfs kjaptr；導流 C-01 論天三家。

來源：《周髀算經》、《宋書．律曆志》、《元史．天文志》、《尚書．堯典》、《宋史．律曆志》、
Stellarium 新版 skycultures：chinese（室宿、壁宿、昴宿、畢宿）、norse（Wolf's Mouth）；PyEphem 自算。

參數
  lst = 2.5 → 走廊（x=0）＝RA 2.5＝台北 2026/12/22 18:00 的子午線（LST 0h10m）：壁宿 x≈0，
             室宿 +16，昴宿 −54.4（＝3.6 小時後，21:38 到頭頂），畢宿 −64，月亮（21:38）−64.7。
  D_s = 45、D_r = 49、D_fill = 0（與 A-05、X-02 相同；盤寬 ÷ 畫布寬 ＝ 0.698729）：本集只用長圖帶
             （室壁 +15…+29、昴宿 +24、畢宿 +15…+19），盤照規定生成、不使用。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "H-冬至"
OUT = os.path.join(BASE, "05_素材/H-冬至_圭表/_v4大畫布")
LST0 = 2.5

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
ALCYONE = 17702
ALDEBARAN = 21421
HYADES = [21421, 20885, 20205, 20455, 20889]
SHI = [113963, 113881]                 # 室宿一 α Peg、室宿二 β Peg
BI = [1067, 677]                       # 壁宿一 γ Peg、壁宿二 α And（東壁）
SQUARE = SHI + BI
MAINS = [ALCYONE, ALDEBARAN] + SHI + BI

# 月亮：台北 2026/12/22 21:38（昴宿過子午線的時刻）的位置（PyEphem，J2000 天體測量座標）
try:
    import ephem
    _tp = ephem.Observer(); _tp.lat, _tp.lon = "25.0330", "121.5654"; _tp.pressure = 0; _tp.elevation = 10
    _tp.date = ephem.Date("2026/12/22 21:38") - 8 * ephem.hour
    _mo = ephem.Moon(); _mo.compute(_tp)
    MOON = (round(math.degrees(float(_mo.a_ra)), 2), round(math.degrees(float(_mo.a_dec)), 2))
    MOON_PHASE = round(_mo.phase)
except ImportError:
    MOON, MOON_PHASE = (66.9, 26.7), 96


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


SEG_SHIBI = sc("chinese", "Encampment") + sc("chinese", "Wall")     # 室宿＋壁宿（古時合稱營室）
SEG_MAO = sc("chinese", "Hairy Head")                                 # 昴宿
SEG_NET = sc("chinese", "Net")                                        # 畢宿
SEG_WOLF = sc("norse", "Wolf's Mouth")                                # 北歐：狼嘴（畢宿的 V）
SEG_SQ = [[113963, 113881, 677, 1067, 113963]]                        # 定位：飛馬座大四邊形

LG_SQ = [(SEG_SQ, "white", 0.4)]
LG_SHIBI = [(SEG_SHIBI, "amber", 0.6)]
LG_MAO = [(SEG_MAO, "amber", 0.6)]
LG_NET = [(SEG_NET, "white", 0.5)]
LG_WOLF = [(SEG_WOLF, "red", 1.0)]
LINE_SETS = [(LG_SQ, "連線-大四邊形（定位）"), (LG_SHIBI, "連線-室宿壁宿"), (LG_MAO, "連線-昴宿"), (LG_NET, "連線-畢宿"),
             (LG_WOLF, "連線-狼嘴（北歐）")]
LG_ALL = LG_SHIBI + LG_MAO
LINES_KEY = {"L4": "星座連線", "定位": "連線-大四邊形（定位）", "室壁": "連線-室宿壁宿", "昴": "連線-昴宿", "畢": "連線-畢宿",
             "狼": "連線-狼嘴（北歐）", "月": "月亮（12-22 21-38）"}
LINE_GROUPS = {"L4": LG_ALL, "定位": LG_SQ, "室壁": LG_SHIBI, "昴": LG_MAO, "畢": LG_NET, "狼": LG_WOLF}


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
# 四、自訂圖層：月亮（12/22 21:38 的位置，快滿月）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    dec = dec0 + y
    ra = ra0 + x / max(0.05, math.cos(math.radians(dec0)))
    return ra % 360, dec


def circle(ra0, dec0, r, n=48):
    return [tangent_pt(ra0, dec0, r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n))
            for i in range(n + 1)]


def custom_layers(m, S):
    def moon(s, pos, runs):
        for k, op in ((2.6, 0.06), (1.8, 0.10), (1.25, 0.18)):
            s.poly_fill(runs(circle(MOON[0], MOON[1], 0.28 * k)), fill="#FFF6D8", opacity=op)
        s.poly_fill(runs(circle(MOON[0], MOON[1], 0.28)), fill="#FFF6D8", opacity=1.0)

    return [("月亮（12-22 21-38）", moon)]


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
#   (原文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ("昴宿", "日短星昴（《堯典》）", "amber",
     "《尚書．堯典》「日短，星昴，以正仲冬」：白天最短、黃昏昴宿在正南，就是仲冬"),
    ("東壁", "壁宿", "amber",
     "虞喜（東晉，330）：「堯時冬至日短星昴，今二千七百餘年，乃東壁中」（《宋史．律曆志》引）"),
    ("室宿", "營室", "white", "室宿一 α Peg、室宿二 β Peg；室、壁古時合稱營室（飛馬座大四邊形）"),
    ("21:38", "昴宿到頭頂（台北今晚）", "amber", "PyEphem：台北 2026/12/22 21:38 昴宿六過子午線，高度 89.2°"),
    ("Úlfs kjaptr", "狼嘴（北歐）", "red", "Stellarium norse：Wolf's Mouth＝畢宿的 V；A-15"),
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

    PLEI = [ALCYONE]
    # ── 堯典：昴宿（上方空天區；左下是畢宿與月亮）──
    LB_MAO = pair(PLEI, "昴宿", 0.0, 5.0, 1.7, 1.0, 2.6)
    # ── 虞喜：東壁（大四邊形東邊）；說明放在四邊形下方 ──
    LB_WALL = (lone(BI, "東壁", "amber", 1.6, -3.4, 0.0, "壁") +
               lone(SHI, "室宿", "white", 1.1, 3.2, 0.0, "室") +
               lone(SQUARE, "虞喜：冬至黃昏的正南方", "white", 0.8, 0.0, -10.5, "壁-註"))
    # ── 今晚：21:38 昴宿到頭頂；月亮在它東邊（左）約 9°（月亮標籤放下方，避開昴宿的中譯）──
    LB_NOW = (pair(PLEI, "21:38", 0.0, 5.0, 1.7, 0.9, 2.6) +
              lone(MOON, f"月亮（{MOON_PHASE}%）", "white", 0.9, 0.0, -2.6, "今-月"))
    # ── 下集：北歐的狼嘴（畢宿）──
    LB_WOLF = pair(HYADES, "Úlfs kjaptr", 0.0, -5.5, 1.4, 1.0, 2.3)

    label_sets = [(LB_MAO, "堯典"), (LB_WALL, "虞喜"), (LB_NOW, "今晚"), (LB_WOLF, "北歐")]

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
    WALL0 = (8.0, 15.0, 33.0, 0.0)          # 開場：台北 18:00 的正南方（室宿＋壁宿＝大四邊形）
    WALL = (7.0, 16.0, 30.0, 0.0)           # 定格頁的底；虞喜「東壁中」
    MAO = (-57.0, 18.0, 30.0, 0.0)          # 昴宿＋畢宿＋月亮（21:38 的正上方）
    WOLF = (-62.0, 14.0, 26.0, 0.0)         # 畢宿的狼嘴（下集 A-15）

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="Z", sec=9, north=True,
             frames=[WALL0, WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             vo="今天冬至，白天最短、影子最長的一天。沒有日曆的年代，古人怎麼知道「就是今天」？"
                "靠一根棍子。",
             card="同一片星空，冬至這一天——影子最長；古人用一根棍子——量出一年。",
             note="開場字卡；台北 12/22 18:00 的正南方（室宿＋壁宿）微推近"),
        dict(code="02", kind="Z", sec=10, north=True,
             frames=[WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             overlay="C-HDZ-01_圭表", overlay_layers=["表與圭層", "夏至層", "冬至層"],
             vo="立一根八尺高的竿子，叫「表」；地上平放一把尺，叫「圭」。每天正午量影子：夏天短、冬天長，"
                "最長的那天，就是冬至。",
             note="畫面不動；定格疊概念圖 C-HDZ-01（表與圭 → 夏至一尺六寸 → 冬至一丈三尺五寸）"),
        dict(code="03", kind="Z", sec=13, north=True,
             frames=[WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             overlay="C-HDZ-02_一年的影子", overlay_layers=["影長層", "一年層", "一度層"],
             vo="從這次最長，數到下次最長，就是一年：三百六十五又四分之一天。"
                "所以古人把天空也分成三百六十五又四分之一度——太陽一天走一度。",
             note="畫面不動；定格疊概念圖 C-HDZ-02（兩年的正午影長 → 365¼ 日 → 周天 365¼ 度）"),
        dict(code="04", kind="Z", sec=10, north=True,
             frames=[WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             overlay="C-HDZ-03_折取其中", overlay_layers=["平頂層", "兩天層", "取中層"],
             vo="可是冬至前後，影子幾乎不變，看不出哪天最長。南朝的祖沖之改量冬至前後影子一樣長的兩天，"
                "再取正中間。",
             note="畫面不動；定格疊概念圖 C-HDZ-03（平頂 → 大明五年的三次實測 → 折取其中＝十一月三日）"),
        dict(code="05", kind="Z", sec=9, north=True,
             frames=[WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             overlay="C-HDZ-04_四丈高表", overlay_layers=["八尺層", "四丈層", "景符層"],
             vo="元朝的郭守敬，把竿子加高到四丈，影子拉長五倍；再用一片有小孔的「景符」，對準模糊的影子邊緣。",
             note="畫面不動；定格疊概念圖 C-HDZ-04（八尺表 → 四丈高表 → 景符）"),
        dict(code="06", kind="Z", sec=12, north=True,
             frames=[WALL], layers=["定位", "室壁"], labels=[], labels_start=[],
             overlay="C-HDZ-05_一年有多長",
             vo="授時曆一年取三百六十五點二四二五天——三百年後歐洲訂的公曆，用的是同一個數字，"
                "跟今天量到的一年，差不到半分鐘。",
             note="畫面不動；之後疊 9:16 圖卡 C-HDZ-05 一年有多長（可存圖）"),
        dict(code="07", kind="S", sec=10, north=True,
             frames=[WALL, MAO], layers=["昴"], labels=ls("堯典"), labels_start=[],
             vo="影子管白天，星星管晚上。《尚書．堯典》說：「日短星昴，以正仲冬」——白天最短、"
                "黃昏時昴宿在正南方，就是仲冬。",
             note="往左（東）滑到昴宿；昴宿（琥珀）"),
        dict(code="08", kind="S", sec=11, north=True,
             frames=[MAO, WALL], layers=["定位", "室壁"], labels=ls("虞喜"), labels_start=ls("堯典"),
             vo="東晉的虞喜發現：到了他那時，冬至黃昏的正南方，已經從昴宿換成東壁。"
                "星星跟季節，每年都錯開一點點——這就是「歲差」。",
             note="往右（西）滑回大四邊形；室宿＋壁宿（琥珀）"),
        dict(code="09", kind="S", sec=10, north=True,
             frames=[WALL, MAO], layers=["昴", "畢", "月"], labels=ls("今晚"), labels_start=ls("虞喜"),
             vo="今晚在台北，昴宿要到九點半過後，才爬到頭頂正上方——比《堯典》說的黃昏，晚了好幾個鐘頭。",
             note="往左滑 64°＝4.2 小時（18:00 正南 → 21:38 頭頂）；昴宿、畢宿、月亮（12/22 21:38 的位置）"),
        dict(code="10", kind="Z", sec=12, north=True,
             frames=[MAO], layers=["昴", "畢", "月"], labels=[], labels_start=ls("今晚"),
             overlay="C-HDZ-06_今天怎麼看",
             vo="今天中午十一點五十二分，立一根一公尺的棍子，影子大約一點一三公尺，是今年最長的。"
                "今晚月亮快滿了，昴宿就在它旁邊。",
             note="畫面不動；之後疊 9:16 圖卡 C-HDZ-06 今天怎麼看（台北 12/22；可存圖）"),
        dict(code="11", kind="Z", sec=11, north=True,
             frames=[MAO, WOLF], layers=["狼", "月"], labels=ls("北歐"), labels_start=[],
             vo="影子還能量出太陽多遠？可以回頭看《論天三家》那集。三天後聖誕節，我們去北歐："
                "聖誕節以前，北歐人過的仲冬節，叫 Yule。",
             card="下集見｜北歐：Yule 之夜的狼與神駒",
             note="推近畢宿；北歐狼嘴（紅）；端卡＋追蹤 CTA"),
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

    print(f"  x：壁宿 {x_of(centroid(BI, S)[0]):+.1f}、室宿 {x_of(centroid(SHI, S)[0]):+.1f}、"
          f"昴宿六 {x_of(S[ALCYONE][0]):+.1f}、畢宿五 {x_of(S[ALDEBARAN][0]):+.1f}、"
          f"月亮 {x_of(MOON[0]):+.1f}（dec {MOON[1]:+.1f}，{MOON_PHASE}%）")

    EN = {"昴宿": "Hairy Head (Pleiades)", "東壁": "Eastern Wall", "室宿": "Encampment",
          "21:38": "Pleiades at the zenith", "Úlfs kjaptr": "Wolf's Mouth"}
    PY = {"昴宿": "Mǎo Xiù", "東壁": "Dōng Bì", "室宿": "Shì Xiù"}
    terms = {o: dict(原文=o, 拼音=PY.get(o, ""), 英文翻譯=EN.get(o, ""), 中文=z, 顏色=c, 來源備註=n)
             for o, z, c, n in TERMS}
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

    for items, name in label_sets:
        g = []
        for sh in shots:
            if name in sh.get("labels", []):
                g += [x for x in shot_groups(sh) if x not in g]
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=g or LG_ALL,
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
