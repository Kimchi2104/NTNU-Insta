# -*- coding: utf-8 -*-
"""A-31 卡米拉羅伊與尤瓦萊：由黑暗組成的鴯鶓｜大畫布 v4.6

論點：大多數星座連的是亮星；卡米拉羅伊／尤瓦萊的鴯鶓 Gawarrgay 卻是由銀河的暗帶組成——
頭＝南十字旁的煤袋，脖子順著暗帶經過南門二、馬腹一，身體與腳一路伸到天蠍、人馬。牠的姿勢
是一份日曆（4–5 月在跑、6–8 月坐在巢上、8 月底直立成兩顆蛋、11 月坐在水坑裡），bora 場地的
方向對著 8 月傍晚直立的牠。同一塊黑：Boorong 的鴯鶓 Tchingal、布吉斯的山羊、克丘亞的 Yutu
與黑駱馬 Yacana；同一段天：瓜拉尼的美洲鴕 Guirá Nhandu。台灣：頭貼著地平線，身體和腳看得清楚。

來源：Stellarium kamilaroi（Fuller；CC BY-NC-ND——插圖與多邊形一律不描，暗帶示意層自畫）、
Fuller, Anderson, Norris & Trudgett 2014（JAHH 17:171）、Fuller, Hamacher & Norris 2013、
Stellarium tupi 001（Guira-nhandu，42 顆）。逐字稿：04_腳本庫/A-31-…-逐字稿-v1.md。天象 PyEphem 自算。

【為什麼整集都在南盤圖層組上（逐字稿 v1 寫「長圖帶狀為主」，素材改成南盤）】
  鴯鶓從煤袋（dec −62.8）到人馬（dec −20…−25）、赤經 RA 185–287 跨 100°。長圖帶的鏡頭要
  |cy|+fov·8/9 ≤ D_s，D_s 要開到 66 以上才容得下煤袋；D_r 跟著到 70，k＝R_RIM/20＝2.86，
  R_fill ≤ 180 ⇒ D_fill ≥ 27——南盤只剩 dec ≤ −27，14–15 鏡墾丁地平線（南點 dec −68，身體在 −25…−40）
  就整片落在盤外。長圖本身在 dec −60 一帶橫向拉長 2 倍，鴯鶓也會被壓扁。南盤（極方位等距）
  整隻放得進一個 9:16 畫面、形狀不變形，又能直接轉到墾丁的時刻。所以 01–17 全部在南盤圖層組，
  **整集不換組**（沒有長圖⇄盤的轉場頁）；分鏡表的 Z/T/S 動作都在盤上做（平移＝改 cx/cy）。

參數（依本集逐字稿重新評估）
  lst = 240 → 鴯鶓的中點（RA 192.9 煤袋 … RA 287 人馬東腿端，中間＝RA 240 豺狼 η）在 x=0。
              本集不用長圖，lst 只決定南盤 0° 的方向；ROT_UP（鴯鶓頭在上、身體與腳往下）另算。
  D_s = 48、D_r = 52 → 盤本體（r ≤ R_RIM）＝dec ≤ −52：煤袋、南十字、南門二、馬腹一、脖子都在盤本體。
              D_r 不再往上提：k＝1.5078 時整隻鴯鶓（離盤心 r 41…107）放得進一格 fov ≈ 110 的直立畫面。
  D_fill = −24 → R_fill＝171.9（盤寬 ÷ 畫布寬＝0.955）；|x_t|+R_fill ≤ 180 ✓。南盤收到 dec +24：
              墾丁南點在盤心上方 kφ＝33.1，14–15 鏡的畫面角落離盤心 ≤ 170 ✓。
  x_tN = x_tS = 0。
  南盤 R：Canva 正角＝順時針＝時間前進；rot＝lst_obs − lst（面向南方，gen_canva_pages.view_lst）。

自訂圖層（大畫布＋南北盤同步出；盤檔才是本集用的）
  銀河暗帶版：與 L1 不同的獨立取樣（seed 31，不動 L1 的 seed 42），沿銀道面加密＋銀心凸起，
             把鴯鶓暗帶裡的點抽掉 → 疊在 L1 上，暗帶就看得出來（04 鏡「暗帶對比加強版」）。
  暗帶-頭／脖子／身體／腳（紫 #B78AFF 半透明填色＋細外框）：依逐字稿畫面欄的描述自畫——頭＝煤袋
             （12h52m −62.8°，約 7°×5°）；脖子經過馬腹一、南門二到矩尺 γ²；身體在矩尺變寬，北緣經豺狼 η、
             天蠍 ε、蛇夫 36、人馬 3，南緣經天蠍 λ，止於人馬 μ；兩條腿＝人馬東側（到 19h09m −25.7°）
             與南冕—望遠鏡（到 18h16m −49.1°）。Stellarium 多邊形只拿來核對位置（腳端座標），不描。
             大畫布版只畫外框（填色在長圖帶與盤的交界會被切開，大畫布本集不用）。
  暗帶外框：四段的外框（虛線），01 鏡迄格、13 鏡用。

check_shots 的 ⚠（判斷後接受）
  全部 R「畫面含長圖側扇區／切點」：本集全程在南盤圖層組上，不跟大畫布互切，切點檢查不適用。
"""
import os, sys, json, math, csv, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS, horizon_points

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-31"
OUT = os.path.join(BASE, "05_素材/A-31_卡米拉羅伊/_v4大畫布")
LST0 = 240.0
TPE = (25.0330, 121.5654)
KT = (21.95, 120.80)
PHI_K = 21.95
PURPLE = COLORS["purple"]


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(lat, lon, tz, when):
    return math.degrees(_obs(lat, lon, tz, when).sidereal_time())


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return round((lst_obs - LST0 + 180.0) % 360.0 - 180.0, 2)


LST_AT = {"墾丁 5/7 23:00": lst_at(*KT, 8, "2027/5/7 23:00"),
          "墾丁 5/8 02:30": lst_at(*KT, 8, "2027/5/8 02:30")}
ROT_K1 = rot_s(LST_AT["墾丁 5/7 23:00"])
ROT_K2 = rot_s(LST_AT["墾丁 5/8 02:30"])


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", []) if isinstance(l, list)]
        out[c["id"]] = [s for s in segs if len(set(s)) >= 2]
    return out


TP = load_sc("tupi")
KM = load_sc("kamilaroi")
SEG_OST = TP["CON tupi 001"]
SEG_YAR = KM["CON kamilaroi Yar"]                 # Yarran 樹的根（十字架二→其他三顆）
hips_of = lambda segs: sorted({h for s in segs for h in s})
OST = hips_of(SEG_OST)
assert len(OST) == 42, len(OST)

ACRUX, MIMOSA, GACRUX, IMAI = 60718, 62434, 61084, 59747
CRUX = [ACRUX, MIMOSA, GACRUX, IMAI]
SEG_CRUX = [[GACRUX, ACRUX], [MIMOSA, IMAI]]
RIGIL, HADAR = 71683, 68702
ANTARES, SHAULA, SARGAS = 80763, 85927, 86228
EPS_SCO = 82396
COALSACK = (192.9, -62.8)
GAL_C = (266.40, -28.94)
MAINS = sorted(set(CRUX + [RIGIL, HADAR, ANTARES, SHAULA, SARGAS, EPS_SCO]))


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、暗帶示意（自畫；RA, dec 度）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    dec = dec0 + y
    return (ra0 + x / max(0.05, math.cos(math.radians(dec)))) % 360, dec


def ellipse(ra0, dec0, a, b, n=72, tilt=0.0):
    t = math.radians(tilt)
    out = []
    for i in range(n + 1):
        u = 2 * math.pi * i / n
        x, y = a * math.cos(u), b * math.sin(u)
        out.append(tangent_pt(ra0, dec0, x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)))
    return out


def densify(pts, step=0.8):
    out = []
    for (r0, d0), (r1, d1) in zip(pts, pts[1:]):
        dr = ((r1 - r0 + 180) % 360) - 180
        n = max(1, int(math.hypot(dr * math.cos(math.radians((d0 + d1) / 2)), d1 - d0) / step))
        for i in range(n):
            out.append(((r0 + dr * i / n) % 360, d0 + (d1 - d0) * i / n))
    out.append(pts[-1])
    return out


def ribbon(spine):
    """spine＝[(ra, dec, 半寬°)] → 閉合多邊形（切平面上左右各推半寬）"""
    L, R = [], []
    for i, (ra, dec, w) in enumerate(spine):
        a = spine[max(0, i - 1)]; b = spine[min(len(spine) - 1, i + 1)]
        c = math.cos(math.radians(dec))
        tx, ty = ((b[0] - a[0] + 180) % 360 - 180) * c, b[1] - a[1]
        n = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / n, tx / n
        L.append(tangent_pt(ra, dec, nx * w, ny * w)); R.append(tangent_pt(ra, dec, -nx * w, -ny * w))
    return densify(L + R[::-1] + [L[0]])


HEAD = ellipse(*COALSACK, 3.4, 2.5, tilt=-12.0)
NECK = densify([(198.5, -60.9), (205, -60.1), (214, -59.3), (222, -58.4), (230, -55.6), (236.5, -52.0),
                (240.5, -48.0), (244.5, -53.2), (236, -56.8), (229, -59.7), (221, -62.0), (212, -63.2),
                (204, -63.6), (198.5, -63.9), (198.5, -60.9)])
BODY = densify([(240.5, -48.0), (240.3, -42.5), (241.0, -38.4), (245.5, -34.5), (251.0, -31.6), (255.5, -28.4),
                (259.0, -26.1), (263.0, -25.0), (267.0, -23.6), (271.0, -21.8), (273.6, -20.6),
                (274.6, -22.6), (270.5, -27.0), (266.8, -32.0), (264.6, -37.8), (260.5, -42.4), (255.0, -46.2),
                (249.5, -50.0), (244.5, -53.2), (240.5, -48.0)])
LEG_E = ribbon([(269.0, -25.2, 1.1), (273.5, -24.6, 1.0), (278.0, -24.0, 0.95), (282.5, -23.7, 0.9),
                (286.0, -24.4, 0.85), (287.3, -25.7, 0.8)])
LEG_S = ribbon([(270.0, -29.5, 1.2), (272.3, -33.5, 1.1), (273.6, -38.5, 1.0), (274.6, -43.5, 0.95),
                (274.9, -47.0, 0.9), (274.2, -49.1, 0.8)])
DARK = {"頭": [HEAD], "脖子": [NECK], "身體": [BODY], "腳": [LEG_E, LEG_S]}
DARK_ALL = [p for v in DARK.values() for p in v]


def in_dark(ra, dec, polys=None):
    from matplotlib.path import Path
    if not hasattr(in_dark, "_P"):
        in_dark._P = [Path([(((r - 240 + 180) % 360) - 180, d) for r, d in p]) for p in DARK_ALL]
    return any(P.contains_point((((ra - 240 + 180) % 360) - 180, dec)) for P in in_dark._P)


def mw_dark_samples(n=26000, seed=31):
    """銀河暗帶版：獨立取樣（不動 L1 的 seed 42）；銀道面加密＋銀心凸起；暗帶內抽掉"""
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        if rng.random() < 0.35:
            l = rng.gauss(0, 18); b = rng.gauss(0, 8.5)          # 銀心凸起
        else:
            l = rng.uniform(-180, 180); b = rng.gauss(0, 4.6)
        ra, dec = G.gal2eq(l % 360, b)
        sz = rng.uniform(.07, .30)
        if dec > 10 and rng.random() < 0.7:                      # 北天少給一點（本集看不到）
            continue
        if in_dark(ra, dec):
            if rng.random() > 0.04:
                continue
        out.append((ra, dec, sz))
    return out


# ══════════════════════════════════════════════════════════════════
# 三、連線
# ══════════════════════════════════════════════════════════════════
LG_OST = [(SEG_OST, "amber", 1.0)]
LG_YAR = [(SEG_YAR, "green", 1.0)]
LG_CRUX = [(SEG_CRUX, "white", 1.0)]
LG_ALL = LG_OST
LINE_SETS = [(LG_OST, "連線-GuiráNhandu美洲鴕"), (LG_YAR, "連線-Yarran樹根"), (LG_CRUX, "連線-南十字")]
LINES_KEY = {"L4": "星座連線", "鴕": "連線-GuiráNhandu美洲鴕", "樹": "連線-Yarran樹根", "十": "連線-南十字",
             "亮": "銀河暗帶版", "頭": "暗帶-頭", "脖": "暗帶-脖子", "身": "暗帶-身體", "腳": "暗帶-腳",
             "框": "暗帶外框"}
LINE_GROUPS = {"L4": LG_ALL, "鴕": LG_OST, "樹": LG_YAR, "十": LG_CRUX,
               "亮": [], "頭": [], "脖": [], "身": [], "腳": [], "框": []}
EMU = ["頭", "脖", "身", "腳"]


def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    v = [sum(vec(*S[h][:2])[i] for h in hs) for i in range(3)]
    return radec(v)


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層
# ══════════════════════════════════════════════════════════════════
def custom_layers(m):
    def mw(s, pos, runs, disc):
        pts = []
        for ra, dec, sz in mw_dark_samples():
            for p in pos(ra, dec):
                pts.append((p[0], p[1], sz * m.ss))
        s.dots(pts, fill=COLORS["mw"], opacity=0.48, prec=1)

    def part(key):
        def fn(s, pos, runs, disc):
            for poly in DARK[key]:
                rs = runs(poly)
                if disc is not None:
                    s.poly_fill(rs, fill=PURPLE, opacity=0.30)
                s.polylines(rs, stroke=PURPLE, w=m.lw * 0.45, opacity=0.85)
        return fn

    def frame(s, pos, runs, disc):
        for poly in DARK_ALL:
            s.polylines(runs(poly), stroke=PURPLE, w=m.lw * 0.5, opacity=0.9, dash="1.0 0.7")

    return [("銀河暗帶版", mw), ("暗帶-頭", part("頭")), ("暗帶-脖子", part("脖子")),
            ("暗帶-身體", part("身體")), ("暗帶-腳", part("腳")), ("暗帶外框", frame)]


def write_custom(m, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all, None)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n),
                   lambda pts, n=north: m._runs_disc(pts, n), north)
                m._write_disc(s, north, name)


# ══════════════════════════════════════════════════════════════════
# 五、旁白字數（中文字＋外文音節；外文照逐字稿「配音提示」的唸法）
# ══════════════════════════════════════════════════════════════════
SYL = {"gawarrgay": 3, "ghillar": 2, "michael": 2, "anderson": 3, "yarran": 2, "muraay": 2, "bora": 2,
       "boorong": 2, "tchingal": 2, "yutu": 2}


def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.lower() in SYL:
            n += SYL[w.lower()]
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyáéíóúãõ]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 六、名詞總表（錨點, 原文, Stellarium 寫法, 英文, 中文, 顏色, 來源）
# ══════════════════════════════════════════════════════════════════
TERMS = [
    ([COALSACK], "Gawarrgay", "Gawaargay", "the Emu in the Sky", "天上的鴯鶓", "purple",
     "Fuller et al. 2014（Gawarrgay／Gawarghoo；地上的鴯鶓叫 dhinawan）；Stellarium kamilaroi 拼 Gawaargay"),
    ([COALSACK], "頭（煤袋）", "—", "Head (the Coalsack)", "頭（煤袋）", "purple", "Fuller et al. 2014"),
    ([(226.0, -58.5)], "脖子", "—", "Neck", "脖子", "purple", "經過馬腹一、南門二到矩尺 γ²"),
    ([(256.0, -36.0)], "身體", "—", "Body", "身體", "purple", "矩尺—天蠍（ε、λ 最寬）—人馬"),
    ([(280.0, -36.0)], "腳", "—", "Legs", "腳", "purple", "人馬東側／南冕—望遠鏡（Stellarium 新版 Emu2 位置）"),
    (CRUX, "南十字", "—", "Southern Cross (Crux)", "南十字", "white", "—"),
    ([RIGIL], "南門二", "—", "α Centauri", "南門二", "white", "—"),
    ([HADAR], "馬腹一", "—", "β Centauri", "馬腹一", "white", "—"),
    ([COALSACK], "Yarran", "Yarran", "Yarran tree (roots and hollow)", "Yarran 樹的樹洞", "green",
     "Stellarium kamilaroi（又叫 mingga；中心在煤袋）"),
    ([RIGIL, HADAR], "Muraay／Muyaay", "Muraay/Muyaay", "Sulphur-crested cockatoos", "葵花鳳頭鸚鵡", "green",
     "Stellarium kamilaroi（卡米拉羅伊語／尤瓦萊語）"),
    ([COALSACK], "Tchingal", "Tchingal", "the tall one; emu (Boorong)", "鴯鶓（Boorong，1857）", "amber",
     "Stanbridge 1857；Stellarium boorong「Dark space near Cross」"),
    ([COALSACK], "Bembé'é", "Bembé'é", "goat (Bugis)", "山羊（布吉斯）", "blue",
     "Ammarell 1999（經 Ohashi & Orchiston 2021）；Stellarium bugis"),
    ([COALSACK], "Yutu", "—", "tinamou (Quechua)", "像鷓鴣的鳥（克丘亞）", "red", "Urton 1981（⚠ 未親核）"),
    ([(228.0, -55.0)], "Yacana", "—", "llama (Quechua)", "黑駱馬（克丘亞）", "red",
     "Urton 1981（⚠ 未親核）：眼睛＝南門二、馬腹一"),
    (OST, "Guirá Nhandu", "Guira-nhandu", "White Ostrich (a rhea)", "美洲鴕（瓜拉尼）", "amber",
     "Stellarium tupi 001（42 顆）；Afonso"),
    ([ANTARES, SHAULA], "天蠍", "—", "Scorpius", "天蠍", "white", "—"),
    ([GAL_C], "人馬", "—", "Sagittarius", "人馬", "white", "—"),
]


# ══════════════════════════════════════════════════════════════════
# 七、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def disc_xy(m, ra, dec, rot, north=False):
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


def rot_up(m):
    """鴯鶓直立：頭（煤袋）在上、身體末端（人馬 μ 一帶）在正下方"""
    best = None
    for i in range(-1800, 1800):
        r = i / 10.0
        hx, hy = disc_xy(m, *COALSACK, r)
        bx, by = disc_xy(m, 271.0, -24.0, r)
        ang = math.degrees(math.atan2(by - hy, bx - hx))
        d = abs(((ang + 90) + 180) % 360 - 180)
        if best is None or d < best[0]:
            best = (d, r)
    return round(best[1], 1)


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=48, D_r=52, D_fill=-24.0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole
    ROT_UP = rot_up(m)

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]} if isinstance(a[0], int) else {"ra": a[0][0], "dec": a[0][1]}
        if all(isinstance(h, int) for h in a):
            ra, dec = centroid(a, S)
        else:
            vs = [vec(*h) if isinstance(h, tuple) else vec(*S[h][:2]) for h in a]
            ra, dec = radec([sum(v[i] for v in vs) for i in range(3)])
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key,
                    disc=True)

    T = {t[1]: t for t in TERMS}

    def term(name, dx=0.0, dy=0.0, s1=1.6, s2=1.2, gap=2.4, zh_only=False, a=None, zh=None, col=None,
             orig=None):
        a0, orig0, _, _, zh0, col0, _ = T[name]
        a = a if a is not None else a0
        zh = zh or zh0
        col = col or col0
        orig = orig or orig0
        if zh_only:
            return [item(a, zh, col, s1, dx, dy, name)]
        return [item(a, orig, col, s1, dx, dy + gap / 2, name),
                item(a, zh, "white", s2, dx, dy - gap / 2, name + "-zh")]

    sz = lambda f: dict(s1=round(f * 0.030, 2), s2=round(f * 0.024, 2), gap=round(f * 0.046, 2))
    zs = lambda f, k=0.024: round(f * k, 2)

    # ════════════════════ 構圖（先算，字級跟 fov 走） ════════════════════
    def fit(pts, rot, pad=0.10, minfov=30.0, dy=0.0, dx=0.0, fov=None):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        far = lambda f: max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 + yp)
                            for sx in (-1, 1) for sy in (-1, 1))
        while far(f) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    dpts = lambda objs, rot: [disc_xy(m, *(S[h][:2] if isinstance(h, int) else h), rot) for h in objs]
    emu_pts = [p for poly in DARK_ALL for p in poly[::4]]

    def hz_pts(phi, L, rot, az0, az1):
        pts = horizon_points(phi, L, n=721)
        return [disc_xy(m, ra, dec, rot) for ra, dec in pts[int(az0 * 2):int(az1 * 2) + 1] if dec < -m.Dfill]

    EMUF = fit(dpts(emu_pts, ROT_UP), ROT_UP, pad=0.06)                     # 整隻（直立）
    WIDE = (EMUF[0], EMUF[1], round(min(EMUF[2] * 1.35, 150.0), 1), ROT_UP)
    WIDE = fit([(WIDE[0], WIDE[1])], ROT_UP, fov=WIDE[2])
    HEADF = fit(dpts(HEAD + [S[ACRUX][:2], S[RIGIL][:2], S[HADAR][:2]], ROT_UP), ROT_UP, pad=0.12, minfov=44.0)
    BODYF = fit(dpts(BODY[::3] + LEG_E[::3] + LEG_S[::3], ROT_UP), ROT_UP, pad=0.10, minfov=44.0)
    CRUXF = fit(dpts(CRUX + [COALSACK, RIGIL, HADAR], ROT_UP), ROT_UP, pad=0.14, minfov=30.0)
    OSTF0 = fit(dpts(CRUX + [COALSACK, RIGIL, HADAR] + OST[:0], ROT_UP), ROT_UP, pad=0.10, minfov=60.0)
    OSTF1 = fit(dpts(OST + emu_pts, ROT_UP), ROT_UP, pad=0.05)
    L1, L2 = LST_AT["墾丁 5/7 23:00"], LST_AT["墾丁 5/8 02:30"]
    K1 = fit(dpts(emu_pts, ROT_K1) + hz_pts(PHI_K, L1, ROT_K1, 110, 250), ROT_K1, pad=0.04)
    hy = sum(p[1] for p in hz_pts(PHI_K, L1, ROT_K1, 175, 185)) / 21
    hx = [disc_xy(m, *COALSACK, ROT_K1)[0], disc_xy(m, *GAL_C, ROT_K1)[0]]      # 頭（右）…銀心（左）置中
    K1 = (round(sum(hx) / 2, 2), round(hy + 0.40 * K1[2] * 8 / 9, 2), K1[2], ROT_K1)  # 地平線落在畫面 70% 高處
    while max(math.hypot(K1[0] + sx * K1[2] / 2, K1[1] + sy * K1[2] * 8 / 9 + yp)
              for sx in (-1, 1) for sy in (-1, 1)) > m.R_fill - 1.0:
        K1 = (K1[0], K1[1], round(K1[2] * 0.98, 1), ROT_K1)
    K1 = (round(hx[0] + 7.0 - K1[2] / 2, 2), K1[1], K1[2], ROT_K1)          # fov 縮小後：頭留在右緣內 7°
    K2 = (K1[0], K1[1], K1[2], ROT_K2)
    NEXT = fit(dpts(CRUX, ROT_UP), ROT_UP, pad=0.30, minfov=24.0, fov=24.0)
    print(f"\n── 構圖 ── ROT_UP {ROT_UP:+.1f}°、墾丁 23:00 {ROT_K1:+.1f}°、02:30 {ROT_K2:+.1f}°\n"
          f"  整隻 {EMUF}\n  拉遠 {WIDE}\n  頭 {HEADF}\n  身體 {BODYF}\n  十字 {CRUXF}\n"
          f"  美洲鴕 {OSTF0}→{OSTF1}\n  墾丁 {K1}→{K2}\n  下集 {NEXT}")

    # ════════════════════ 標籤（盤＝畫面方向，+dx 右、+dy 上） ════════════════════
    def shift(items, key, dx, dy):
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

    F05 = 53.0                                     # 05 鏡 fov 44→62
    LB_EMU = (term("Gawarrgay", **sz(44.0))
              + term("頭（煤袋）", zh_only=True, s1=zs(F05))
              + term("脖子", zh_only=True, s1=zs(F05))
              + term("身體", zh_only=True, s1=zs(F05))
              + term("腳", zh_only=True, s1=zs(F05))
              + term("南十字", zh_only=True, s1=zs(F05, 0.020))
              + term("南門二", zh_only=True, s1=zs(F05, 0.020))
              + term("馬腹一", zh_only=True, s1=zs(F05, 0.020)))
    F11 = CRUXF[2]
    LB_YAR = (term("Yarran", **sz(F11))
              + term("Muraay／Muyaay", **sz(F11))
              + [item([RIGIL, HADAR], "卡米拉羅伊語／尤瓦萊語", "white", zs(F11, 0.018), 0.0, 0.0, "Muraay-註")])
    LB_CROSS = (term("Tchingal", **sz(F11))
                + term("Bembé'é", zh_only=True, s1=zs(F11, 0.026), zh="山羊（布吉斯）")
                + term("Yutu", **sz(F11))
                + term("Yacana", zh_only=True, s1=zs(F11, 0.026), zh="黑駱馬（克丘亞）")
                + [item([(228.0, -55.0)], "Yacana", "red", zs(F11, 0.018), 0.0, 0.0, "Yacana-註")])
    F13 = 70.0
    LB_OST = (term("Guirá Nhandu", a=[COALSACK], **sz(F13))
              + term("Gawarrgay", zh="鴯鶓（暗帶）", **sz(F13)))
    F14 = K1[2]
    LB_KT = (term("頭（煤袋）", zh_only=True, s1=zs(F14, 0.024), col="white")
             + [item([COALSACK], "墾丁最高 5.5°", "white", zs(F14, 0.020), 0.0, 0.0, "頭高度")]
             + term("脖子", zh_only=True, s1=zs(F14, 0.022), a=[RIGIL], col="white")
             + term("身體", zh="身體和腳（天蠍—人馬）", zh_only=True, s1=zs(F14, 0.024), col="white"))
    LB_KT2 = (term("身體", zh="身體和腳爬到最高", zh_only=True, s1=zs(F14, 0.022), col="white", a=[SHAULA])
              + term("頭（煤袋）", zh="頭已經落下", zh_only=True, s1=zs(F14, 0.022), col="white"))
    LB_NEXT = term("南十字", zh="南十字", zh_only=True, s1=zs(NEXT[2], 0.040))

    label_sets = [(LB_EMU, "Gawarrgay鴯鶓"), (LB_YAR, "Yarran與Muraay"), (LB_CROSS, "同一塊黑"),
                  (LB_OST, "GuiráNhandu美洲鴕"), (LB_KT, "墾丁23時"), (LB_KT2, "凌晨兩點半"),
                  (LB_NEXT, "南十字")]

    # 位置依 ROT_UP／墾丁的螢幕座標逐條放（盤＝畫面方向，+dx 右、+dy 上；
    # ROT_UP：煤袋 (−40,−102)、南門二 (−43,−122)、馬腹一 (−44,−115)、身體 (−51,−174)、腳 (−21,−189)）
    shift(LB_EMU, "Gawarrgay", 5.0, -40.0); shift(LB_EMU, "頭（煤袋）", 11.0, 2.0)
    shift(LB_EMU, "脖子", 10.0, 5.0); shift(LB_EMU, "身體", 19.0, 0.0); shift(LB_EMU, "腳", 8.0, 5.0)
    shift(LB_EMU, "南十字", -9.0, 2.0); shift(LB_EMU, "南門二", -8.0, 0.0); shift(LB_EMU, "馬腹一", -8.0, 0.5)
    shift(LB_YAR, "Yarran", -9.0, 0.0); shift(LB_YAR, "Muraay／Muyaay", 3.0, -4.5)
    shift(LB_YAR, "Muraay-註", 3.0, -7.6)
    shift(LB_CROSS, "Tchingal", -11.0, 15.0); shift(LB_CROSS, "Bembé'é", -11.0, 12.2)
    shift(LB_CROSS, "Yutu", -11.0, 8.4); shift(LB_CROSS, "Yacana", -2.0, 5.0); shift(LB_CROSS, "Yacana-註", -2.0, 3.0)
    shift(LB_OST, "Guirá Nhandu", -8.0, -22.0); shift(LB_OST, "Gawarrgay", 12.0, -40.0)
    shift(LB_KT, "頭（煤袋）", -6.0, 12.0); shift(LB_KT, "頭高度", -6.0, 8.6)
    shift(LB_KT, "脖子", -4.0, 5.0); shift(LB_KT, "身體", 14.0, 13.0)
    shift(LB_KT2, "身體", -6.0, 20.0); shift(LB_KT2, "頭（煤袋）", -36.0, 26.0)
    shift(LB_NEXT, "南十字", 0.0, 5.0)

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    NS = dict(north=False, kind="R")
    E = ["亮"] + EMU
    shots = [
        dict(code="01", sec=11, **NS, frames=[WIDE, EMUF], layers=["亮", "框"], labels=[],
             vo="上週在巴黎，星座被畫成一條條直線。今晚往南半球：同一片星空，卡米拉羅伊人看見——一隻由黑暗組成的鴯鶓。",
             card="由黑暗組成的鴯鶓",
             note="第一頁就在南盤圖層組（整集不換組）：銀河南段（南十字—半人馬—天蠍—人馬）直立；先只開銀河＋銀河暗帶版"
                  "＋星點（暗帶要清楚），推近；迄格「暗帶外框」（紫虛線）淡入"),
        dict(code="02", sec=19, **NS, frames=[EMUF], layers=["亮", "框"], labels=[],
             overlay="C-A31-01_地圖", overlay_layers=["澳洲層", "標點層"],
             vo="卡米拉羅伊人和鄰近的尤瓦萊人，住在澳洲新南威爾斯北部。他們的天文，十九世紀就有人記下；今天講的，主要來自尤瓦萊長老 Ghillar Michael Anderson 的公開分享，以及他跟研究者一起發表的論文。",
             card="卡米拉羅伊與尤瓦萊",
             note="畫面不動；疊 C-A31-01：澳洲輪廓（台灣同比例對照）→ 標點層（Goodooga、Lightning Ridge、Walgett 依旁白亮起）"),
        dict(code="03", sec=6, **NS, frames=[EMUF], layers=["亮", "框"], labels=[],
             vo="還有很多知識只屬於族人；這裡只講他們願意公開的部分。",
             card="只講公開的部分",
             note="字卡置中（尊重聲明）；地圖收掉，背景淡回銀河"),
        dict(code="04", sec=16, **NS, frames=[EMUF, WIDE], layers=["亮"], labels=[],
             overlay="C-A31-02_亮星與暗帶", overlay_layers=["亮星層", "暗帶層"],
             vo="先看銀河。它不是一條均勻的光帶：中間一道道黑色的「裂縫」，其實是幾百光年外的塵埃雲，擋住了後面的星光。大多數的星座連的是亮星；這隻鴯鶓，卻是由這些黑組成的。",
             card="這隻鴯鶓由黑組成",
             note="拉遠；只開銀河＋銀河暗帶版（外框收掉）；迄格疊 C-A31-02（左：亮星連線；右：同一片天的暗帶填色）"),
        dict(code="05", sec=15, **NS, frames=[HEADF, BODYF], layers=E, labels=ls("Gawarrgay鴯鶓"),
             vo="這隻鴯鶓叫 Gawarrgay。牠的頭，就是南十字旁邊這塊黑——西方叫它「煤袋」；長長的脖子順著暗帶，經過南門二和馬腹一；身體和腳，一路伸到天蠍、人馬。",
             card="天上的鴯鶓",
             note="從煤袋沿暗帶往下（往天蠍、人馬）平移；暗帶四層依序淡入：頭→脖子→身體→腳（Canva 動畫，同一頁）"),
        dict(code="06", sec=11, **NS, frames=[EMUF], layers=E, labels=[],
             overlay="C-A31-03_鴯鶓曆", overlay_layers=["四五月層"], overlay_at="start",
             vo="牠的姿勢，就是一份日曆。四、五月的晚上，鴯鶓整隻露出來，看得到腳，正在奔跑，那是母鴯鶓追著公鴯鶓的季節。",
             card="四、五月：在跑",
             note="拉遠到整隻；疊 C-A31-03 第 1 層（Goodooga 5/25 21:00：東南升起、兩條腿都在地平線上）"),
        dict(code="07", sec=10, **NS, frames=[EMUF], layers=E, labels=[],
             overlay="C-A31-03_鴯鶓曆", overlay_layers=["六到八月層"], overlay_at="start",
             vo="六到八月，腳看不見了，像一隻坐在巢上的鴯鶓——真的鴯鶓，是爸爸負責孵蛋。這時候，可以去撿蛋。",
             card="六到八月：孵蛋",
             note="C-A31-03 第 2 層（7/1 21:00：高掛、腳淡掉＝坐在巢上）"),
        dict(code="08", sec=11, **NS, frames=[EMUF], layers=E, labels=[],
             overlay="C-A31-03_鴯鶓曆", overlay_layers=["八月底層"], overlay_at="start",
             vo="八月底的傍晚，牠在西南方整個直立起來，頭和身體像兩顆蛋。這時候小鴯鶓快孵出來了，蛋就不能再撿了。",
             card="八月底：別撿蛋",
             note="C-A31-03 第 3 層（8/25 19:30：西南偏南直立；頭＝小蛋、身體＝大蛋）"),
        dict(code="09", sec=11, **NS, frames=[EMUF], layers=E, labels=[],
             overlay="C-A31-03_鴯鶓曆", overlay_layers=["十一十二月層"], overlay_at="start",
             vo="到了十一月，牠貼著地平線，像坐在水坑裡，代表水坑都滿了。沉到地平線下，牠就回到地上，成了很少人見過的黑鴯鶓。",
             card="十一月：水坑滿了",
             note="C-A31-03 第 4 層（11/15 21:00 貼西南地平線＝坐在水坑；虛線＝12/20 身體沉到地平線下＝黑鴯鶓）"),
        dict(code="10", sec=19, **NS, frames=[EMUF], layers=E, labels=[],
             overlay="C-A31-04_bora場地", overlay_layers=["場地層", "天空層"],
             vo="研究者還測量了澳洲東南部六十八處 bora，也就是成年禮場地的方向：多半朝向南到西南——正是八月傍晚，鴯鶓站起來的方向。研究者推測，場地上一大一小兩個圓圈，對應的就是鴯鶓的身體和頭。",
             card="地上的兩個圓圈",
             note="疊 C-A31-04：場地層（大圈在北、小圈在南南西、小徑 213°；68 處的方向扇形）→ 天空層（8 月傍晚直立的鴯鶓："
                  "身體＝大圈、頭＝小圈；小字「研究者推測」）；不用照片、不標真實場地"),
        dict(code="11", sec=13, **NS, frames=[EMUF, CRUXF], layers=["亮", "頭", "脖", "樹"],
             labels=ls("Yarran與Muraay"),
             vo="同一塊黑，在他們的天上還有別的故事：它也是 Yarran 樹的樹洞；南門二和馬腹一，是兩隻葵花鳳頭鸚鵡 Muraay，一直追著這棵被帶上天的樹。",
             card="Yarran 樹與兩隻鸚鵡",
             note="推近南十字＋煤袋＋南門二、馬腹一；Yarran 樹根（綠，Stellarium kamilaroi Yar：十字架二→其他三顆）；"
                  "標籤 Yarran、Muraay／Muyaay（小字「卡米拉羅伊語／尤瓦萊語」）"),
        dict(code="12", sec=22, **NS, frames=[CRUXF], layers=["亮", "頭", "脖"], labels=ls("同一塊黑"),
             overlay="C-A31-05_同一塊黑",
             vo="把這塊黑看成動物的，不只他們。一八五七年的記錄裡，澳洲維多利亞的 Boorong 人說，南十字旁的黑是鴯鶓 Tchingal。印尼的布吉斯水手叫它山羊；祕魯安地斯山的克丘亞人，則在這裡看見一隻像鷓鴣的鳥 Yutu，旁邊還有一頭黑色的駱馬。",
             card="同一塊黑的名字",
             note="同框；跨文化標籤照旁白順序逐一淡入（Tchingal→山羊→Yutu→黑駱馬 Yacana，Canva 動畫）；"
                  "迄格疊 9:16 圖卡 C-A31-05「同一塊黑」（可存圖）"),
        dict(code="13", sec=17, **NS, frames=[OSTF0, OSTF1], layers=["亮", "鴕", "框"],
             labels=ls("GuiráNhandu美洲鴕"),
             vo="南美洲的瓜拉尼人，則用星星把南十字到天蠍這一大片天，連成一隻美洲鴕，頭就圍著煤袋——跟鴯鶓一樣，是不會飛的大鳥。他們說，南十字抓著牠的頭，不然牠會把地上的水喝光。",
             card="兩隻不會飛的大鳥",
             note="從南十字拉到整隻：瓜拉尼美洲鴕連線（琥珀，Stellarium tupi 001）＋鴯鶓暗帶外框（紫虛線）同時開"
                  "＝一個用亮星勾輪廓（頭圍著煤袋），一個整隻由暗帶組成"),
        dict(code="14", sec=17, **NS, horizon=[PHI_K], frames=[OSTF1, K1], layers=E, labels=[], labels_end=ls("墾丁23時"),
             vo="從台灣看呢？鴯鶓的頭，在台北最高只有兩度半，到了墾丁也才五度半；脖子也一樣貼著地平線，幾乎看不出形狀。可是身體和腳，天蠍到人馬那一段，台灣倒是看得很清楚。",
             card="台灣：頭貼著地平線",
             note=f"盤轉 {ROT_UP:+.1f}°→{ROT_K1:+.1f}°（墾丁 5/7 23:00 面南）；山＝墾丁南方地平線（21.95°N）；"
                  "標籤寫高度（頭 台北 2.6°／墾丁 5.5°、脖子 7°）"),
        dict(code="15", sec=21, **NS, horizon=[PHI_K], frames=[K1, K2], layers=E, labels=ls("墾丁23時"),
             labels_end=ls("凌晨兩點半"), overlay="C-A31-06_這週抬頭看",
             vo="這週剛過新月，整晚沒有月光。在南台灣的海邊，晚上十一點前後往南看，鴯鶓橫躺在海面上：頭在右邊，貼著海面幾乎看不見；身體往左上伸。凌晨一點到三點，全台灣往南都看得到牠的身體和腳爬到最高，頭已經沉下去了。",
             card="這週：深夜到凌晨朝南",
             note=f"南盤順時針 23:00→02:30（{ROT_K1:+.1f}°→{ROT_K2:+.1f}°；頭沉入山後、身體爬升）；"
                  "迄格疊 9:16 圖卡 C-A31-06「這週抬頭看」（可存圖）"),
        dict(code="16", sec=8, **NS, frames=[K2, WIDE], layers=["亮", "框"], labels=[],
             vo="下次看銀河，別只找亮的星，也看看那些黑——有人在那裡，讀出了一整年的季節。",
             card="也看看那些黑",
             note=f"盤轉回直立（{ROT_K2:+.1f}°→{ROT_UP:+.1f}°）並拉遠到整條銀河南段；山降出畫面；"
                  "轉場在旁白前 1 秒完成，金句時畫面靜止"),
        dict(code="17", sec=11, **NS, frames=[WIDE, NEXT], layers=["亮", "十"], labels=[], labels_end=ls("南十字"),
             vo="下週五，回到煤袋旁邊那個十字：南天其實有三個十字——真的、假的、鑽石的。認錯了，你找到的南方會偏掉二十度以上。",
             card="下集見｜南天的十字路口",
             note="推近南十字（白線）；端卡「下集見｜南天的十字路口」＋追蹤 CTA"),
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
    for sh in shots:
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 170.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° ≥ 170°（Canva 可能反轉）")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            yc = -m.y_pole
            ew = 2 * m.R_fill / fov * 1080
            off = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "南盤圖層組（置中）", "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])
    print(f"  LST：" + "、".join(f"{k} {v:.1f}" for k, v in LST_AT.items()) +
          f"；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=[h for h in hips if isinstance(h, int)], 原文=orig, 拼音="", 英文翻譯=en,
                           中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Tchingal", 中譯="鴯鶓（Boorong）", 英文="emu", 顏色="amber"),
                         dict(原文="Bembé'é", 中譯="山羊（布吉斯）", 英文="goat", 顏色="blue"),
                         dict(原文="Yutu", 中譯="像鷓鴣的鳥（克丘亞）", 英文="tinamou", 顏色="red"),
                         dict(原文="Yacana", 中譯="駱馬（克丘亞）", 英文="llama", 顏色="red"),
                         dict(原文="Guirá Nhandu", 中譯="美洲鴕（瓜拉尼）", 英文="rhea", 顏色="amber")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": dict(UP=ROT_UP, K1=ROT_K1, K2=ROT_K2), "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    dark_wall(m, shots, label_sets)
    print("\n完成 →", OUT)


def dark_wall(m, shots, label_sets):
    """QA 用：鏡頭牆不畫自訂圖層 → 另出一張「暗帶＋銀河暗帶版＋地平線」逐格縮圖（盤＝畫面方向）"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MP
    S = dict(G.load_stars(BASE))
    mw = mw_dark_samples(12000)
    LS = {n: it for it, n in label_sets}
    cells = [(sh, i, f) for sh in shots for i, f in enumerate(sh["frames"])]
    cols = 8
    rows = (len(cells) + cols - 1) // cols
    fig = plt.figure(figsize=(cols * 2.0, rows * 3.7), dpi=90)
    fig.patch.set_facecolor("#0B0F1E")
    for k, (sh, i, (cx, cy, fov, rot)) in enumerate(cells):
        ax = fig.add_subplot(rows, cols, k + 1)
        ax.set_facecolor("#0B0F1E"); ax.set_xticks([]); ax.set_yticks([])
        hw, hh = fov / 2, fov * 8 / 9
        ax.set_xlim(cx - hw, cx + hw); ax.set_ylim(cy - hh, cy + hh)
        P = lambda ra, dec: disc_xy(m, ra, dec, rot)
        xs = [P(r, d) for r, d, s in mw]
        ax.scatter([p[0] for p in xs], [p[1] for p in xs], s=0.4, c="#C9DAF5", alpha=0.35, lw=0)
        for h, (ra, dec, v) in [(h, S[h][:3]) for h in S if S[h][2] < 4.6 and S[h][1] < 25]:
            p = P(ra, dec)
            ax.scatter([p[0]], [p[1]], s=max(0.3, (5 - v)) ** 1.6 * 1.2, c="white", lw=0)
        if set(sh["layers"]) & set(EMU + ["框"]):
            for poly in DARK_ALL:
                ax.add_patch(MP([P(*q) for q in poly], closed=True, fc=PURPLE, alpha=0.28, ec=PURPLE, lw=0.6))
        if "鴕" in sh["layers"]:
            for seg in SEG_OST:
                q = [P(*S[h][:2]) for h in seg if h in S]
                ax.plot([a[0] for a in q], [a[1] for a in q], c=COLORS["amber"], lw=0.6)
        if sh.get("horizon"):
            L = (rot + LST0)
            hp = horizon_points(sh["horizon"][0], L, n=721)
            q = [P(ra, dec) for ra, dec in hp if dec < 24]
            ax.plot([a[0] for a in q], [a[1] for a in q], c="#7BD88F", lw=0.8)
        labs = sh.get("labels_end", []) if (i == len(sh["frames"]) - 1 and sh.get("labels_end")) else sh.get("labels", [])
        for n in labs:
            for it in LS[n]:
                ra, dec = (S[it["hip"]][:2] if "hip" in it else (it["ra"], it["dec"]))
                p = P(ra, dec)
                ax.text(p[0] + it["dx"], p[1] + it["dy"], it["text"], color=COLORS.get(it["color"], it["color"]),
                        fontsize=max(3.5, it["size"] * 1.7 * 72 * 2.0 / fov / 1.0), ha="center", va="center",
                        fontproperties=_fp(), clip_on=True)
        ax.set_title(f"{sh['code']} {'起迄'[min(i,1)]}  fov {fov:.0f} rot {rot:+.0f}", color="white", fontsize=6,
                     fontproperties=_fp())
    fig.savefig(os.path.join(OUT, f"{EP}_QA-暗帶鏡頭牆.png"), facecolor="#0B0F1E")
    plt.close(fig)
    print(f"  ✓ {EP}_QA-暗帶鏡頭牆.png")


def _fp():
    from matplotlib.font_manager import FontProperties
    return FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


if __name__ == "__main__":
    build()
