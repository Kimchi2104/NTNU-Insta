# -*- coding: utf-8 -*-
"""A-10 東加：星星的名字就是航線｜大畫布 v4.6（第一集用到「南盤 R 鏡頭＋南方地平線」）

論點：東加的星空幾乎只留在一份航海指南裡——大酋長 Siaosi Tukuʻaho（1890–93 任首相）寫的
sailing directions，傳教士 E. E. V. Collocott 1922 年整理成〈Tongan Astronomy and Calendar〉
（Bishop Museum Occasional Papers 8(4)）。所以東加的星座大多是一句航海指令：
「Tuʻulalupe 要等它像鴿子的棲架一樣直直站起來才能用」、「ʻAo ʻo ʻUvea 要等它像頭環一樣戴在 ʻUvea 上空」、
「Kapakau ʻo Tafahi 像母雞張開翅膀孵在 Tafahi 島上」——名字裡就是要去的島、要等的姿勢。

鏡頭路線：長圖（十一月的東加晚空）→ 沿走廊往南 → 南盤：Maʻafu 兩團火（麥哲倫雲）→ 轉到五月：
野鴨 Toloa（南十字）、兩個人 Ongo Tangata（南門二、馬腹一）丟的石頭 Maka（十字架增一 ε）、指南
→ 回長圖、沿走廊往北 → 北盤（Vavaʻu 地平線）：Tafahi 的翅膀 → 七月（東加本島）：ʻUvea 的圓環
→ 回長圖：鴿子的棲架、一船三人＋一串魚（Hina 的船）、Mataliki、Stellarium 版對照 → 北盤：今晚台北。

輸出：L1銀河 L2星點 L3經緯線 L4星座連線（Collocott 版全開）
      連線-野鴨／兩個人／一船三人／一串魚／鴿子棲架／Uvea圓環／Tafahi翅膀／Stellarium版
      深空天體（大小麥哲倫雲、獵戶座大星雲、昴宿星團、煤袋）、指南線、主角星白點、石頭白圈
      標籤（長圖）：東加名／中譯／星名／Stellarium／北極星
      標籤（盤）：火／火譯／星名-南盤／鴨／部位／指南／翅膀／仙后／圓環／台北／台北譯
      ＋ 南北盤圖層組 / 預覽黑底 / SB-分鏡 / SB-鏡頭牆 / 鏡頭清單 / 標籤資料
執行：python3 make_a10_v4.py

參數
  lst = 15 → 走廊（x=0）＝RA 15：往北是仙后座 W（Kapakau ʻo Tafahi，x −14～+13）一路到北極星；
             往南是水委一（x −9）、小麥哲倫雲（x +2）一路到南天極——兩個盤都從走廊進出。
             RA 15 也正好是 11/13 晚上 22:10 東加的子午線：長圖就是「十一月的東加晚空」，
             左（東）是剛升起的昴宿（x −42）、畢宿（−54）、獵戶（−64～−74）、天狼（−86）。
  D_s = 48、D_r = 52 → 南十字、南門二、馬腹一、假十字、老人星（−52.7）都進南盤本體；
             仙后座（王良四 +56.5 起）進北盤本體；五車二 +46 在帶內。
  D_fill = −25 → k=1.508、R_fill=173.4；南盤收到 dec +25（面向南方的東加星空一路到天頂 −21°都有），
             北盤收到 dec −25（北冕、昴宿、畢宿都在北盤填滿圓內，台北的北方星空一次看完）。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 R：Canva 正角＝順時針＝時間前進（北盤相反）；rot＝lst_obs−lst（gen_canva_pages.view_lst）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS
from gen_projection import great_circle
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-10"
OUT = os.path.join(BASE, "05_素材/A-10_東加/_v4大畫布")
LST0 = 15.0
PHI_T = -21.14            # 東加本島 Nukuʻalofa（21.14°S, 175.20°W）
PHI_V = -18.65            # Vavaʻu 的 Neiafu（18.65°S, 173.98°W）
PHI_TPE = 25.03           # 台北


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）：各時刻的地方恆星時
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


LST_AT = {
    "東加 11/13 22:00": lst_at(-21.1393, -175.2018, 13, "2026/11/13 22:00"),
    "Vavaʻu 11/13 21:48": lst_at(-18.6508, -173.9832, 13, "2026/11/13 21:48"),
    "東加 7/1 21:39": lst_at(-21.1393, -175.2018, 13, "2026/7/1 21:39"),
    "台北 11/13 20:00": lst_at(25.0330, 121.5654, 8, "2026/11/13 20:00"),
}


def crux_may_date():
    """東加晚上九點、南十字（RA 187.2）正好上中天的日期"""
    import ephem
    best = None
    for d in range(1, 32):
        l = lst_at(-21.1393, -175.2018, 13, f"2026/5/{d} 21:00")
        dd = abs((l - 187.2 + 180) % 360 - 180)
        if best is None or dd < best[0]:
            best = (dd, d)
    return best[1]


CRUX_DAY = crux_may_date()
LST_AT[f"東加 5/{CRUX_DAY} 21:00"] = lst_at(-21.1393, -175.2018, 13, f"2026/5/{CRUX_DAY} 21:00")


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return (lst_obs - LST0 + 180.0) % 360.0 - 180.0


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    return r + 360.0 if r <= -180.0 else r


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
GACRUX, ACRUX, MIMOSA, IMAI, GINAN = 61084, 60718, 62434, 59747, 60260   # γ α β δ ε Cru
RIGIL, HADAR = 71683, 68702                                             # α β Cen
ACHERNAR, CANOPUS, SIRIUS = 7588, 30438, 32349
ALSEPHINA, ASPIDISKE, AVIOR, MARKEB = 42913, 45556, 41037, 45941
MINTAKA, ALNILAM, ALNITAK, C_ORI, IOTA_ORI = 25930, 26311, 26727, 26237, 26241
BETELGEUSE, RIGEL, BELLATRIX, MEISSA = 27989, 24436, 25336, 26207
ALDEBARAN, ALCYONE, ELECTRA = 21421, 17702, 17499
HYADES = [21421, 20885, 20205, 20455, 20889]
CASTOR, POLLUX = 36850, 37826
ALPHECCA, ARCTURUS = 76267, 69673
SCHEDAR, CAPH, NAVI, RUCHBAH, SEGIN = 3179, 746, 4427, 6686, 8886
POLARIS = 11767

MAINS = [GACRUX, ACRUX, MIMOSA, IMAI, RIGIL, HADAR, ACHERNAR, CANOPUS, SIRIUS,
         MINTAKA, ALNILAM, ALNITAK, BETELGEUSE, RIGEL, ALDEBARAN, ALCYONE,
         ALPHECCA, SCHEDAR, CAPH, NAVI, RUCHBAH, SEGIN, POLARIS, CASTOR, POLLUX]

# 深空天體（J2000；SIMBAD 常用值）
LMC = (80.894, -69.756)      # 645′×550′，PA 170
SMC = (13.187, -72.829)      # 320′×185′，PA 45
M42 = (83.82, -5.39)
M45 = (56.75, 24.12)
COALSACK = (192.5, -62.8)    # Humu：約 7°×5° 的暗星雲
SCP = (0.0, -89.999)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium tongan index.json；Collocott 版另組）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


T = sc_lines("tongan")
# Collocott 1922 版（L4＝這幾組全開）
LG_DUCK = [([[GACRUX, ACRUX], [MIMOSA, IMAI]], "amber", 1.0)]        # Toloa 野鴨＝南十字
LG_MEN = [([[RIGIL, HADAR]], "red", 1.0)]                             # Ongo Tangata 兩個人
LG_BOAT = [([[MINTAKA, ALNILAM, ALNITAK]], "blue", 1.0)]              # ʻAlotolu 一船三人
LG_FISH = [([[C_ORI, IOTA_ORI]], "blue", 0.8)]                        # Tuinga ika 一串魚（獵戶之劍）
LG_PERCH = [(T["004"], "green", 1.0)]                                 # Tuʻulalupe（Stellarium＝畢宿）
LG_UVEA = [(T["010"], "green", 1.0)]                                  # ʻAo ʻo ʻUvea（Stellarium＝北冕）
LG_WING = [(T["011"], "green", 1.0)]                                  # Kapakau ʻo Tafahi（Stellarium＝仙后）
LG_ALL = LG_DUCK + LG_MEN + LG_BOAT + LG_FISH + LG_PERCH + LG_UVEA + LG_WING
# Stellarium 版和 Collocott 對不上的幾組（紫）
LG_STEL = [(T["003"], "purple", 1.0),      # Toloa＝獵戶腰帶
           (T["005"], "purple", 1.0),      # Toloalahi＝假十字
           (T["008"], "purple", 0.8),      # Houmatoloa＝串起三隻鴨
           (T["002"], "purple", 1.0),      # Lua tangata＝北河二、北河三
           (T["009"], "purple", 1.0)]      # Fatanalua＝后髮座
LINE_SETS = [(LG_DUCK, "連線-野鴨"), (LG_MEN, "連線-兩個人"), (LG_BOAT, "連線-一船三人"),
             (LG_FISH, "連線-一串魚"), (LG_PERCH, "連線-鴿子棲架"), (LG_UVEA, "連線-Uvea圓環"),
             (LG_WING, "連線-Tafahi翅膀"), (LG_STEL, "連線-Stellarium版")]
LINES_KEY = {"L4": "星座連線", "鴨": "連線-野鴨", "人": "連線-兩個人", "船": "連線-一船三人",
             "魚": "連線-一串魚", "鴿": "連線-鴿子棲架", "環": "連線-Uvea圓環",
             "翼": "連線-Tafahi翅膀", "St": "連線-Stellarium版",
             "深空": "深空天體", "指南": "指南線", "石": "石頭白圈"}
LINE_GROUPS = {"L4": LG_ALL, "鴨": LG_DUCK, "人": LG_MEN, "船": LG_BOAT, "魚": LG_FISH,
               "鴿": LG_PERCH, "環": LG_UVEA, "翼": LG_WING, "St": LG_STEL}


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(seglists):
    return sorted({h for segs in seglists for seg in segs for h in seg})


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻ]+|[α-ω]|\d+|[㐀-鿿]", t):
        if re.match(r"[㐀-鿿]", w):
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
# 四、自訂圖層：深空天體、指南線（大畫布＋南北盤同步出）
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


def _uv(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return np.array([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])


def _rd(v):
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(v[2]))


def pointer_path(S, n=90):
    """南十字長軸（γ→α）沿大圓往南延長到最靠近南天極處：回傳 (γ→α 段, 延長段, 延長倍數, 離極角距)"""
    g, a = _uv(*S[GACRUX][:2]), _uv(*S[ACRUX][:2])
    ang = math.acos(float(np.clip(g @ a, -1, 1)))
    w = a - g * (g @ a); w /= np.linalg.norm(w)
    s = np.array([0.0, 0.0, -1.0])
    t_star = math.atan2(float(s @ w), float(s @ g))
    seg1 = [_rd(g * math.cos(ang * i / 12) + w * math.sin(ang * i / 12)) for i in range(13)]
    seg2 = [_rd(g * math.cos(ang + (t_star - ang) * i / n) + w * math.sin(ang + (t_star - ang) * i / n))
            for i in range(n + 1)]
    p = g * math.cos(t_star) + w * math.sin(t_star)
    miss = 90.0 - math.degrees(math.asin(-float(p[2])))
    return seg1, seg2, t_star / ang, miss


def custom_layers(m, S):
    mw = COLORS["mw"]

    def deep(s, pos, runs):
        for (ra0, dec0, a, b, pa) in [(*LMC, 5.4, 4.6, 170.0), (*SMC, 2.65, 1.55, 45.0),
                                      (*M42, 0.5, 0.45, 0.0)]:
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
        s.polylines(runs(ellipse(*COALSACK, 3.4, 2.5, 30.0)), stroke=mw, w=0.10, opacity=0.45,
                    dash="0.6,0.5")

    def pointer(s, pos, runs):
        seg1, seg2, ratio, miss = pointer_path(S)
        s.polylines(runs(seg1), stroke=COLORS["red"], w=0.16, opacity=0.9)
        s.polylines(runs(seg2), stroke=COLORS["red"], w=0.14, opacity=0.85, dash="0.9,0.6")
        for p in pos(*SCP):
            s.circle(p[0], p[1], 0.9, stroke=COLORS["red"], w=0.12, opacity=0.95)
            s.polylines([[(p[0] - 1.6, p[1]), (p[0] + 1.6, p[1])],
                         [(p[0], p[1] - 1.6), (p[0], p[1] + 1.6)]],
                        stroke=COLORS["red"], w=0.08, opacity=0.9)

    return [("深空天體", deep), ("指南線", pointer)]


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


def disc_xy(m, ra, dec, rot, north):
    """天體在「轉 rot 之後的盤」上的位置（畫面方向的畫布單位，盤心＝(0, ±y_pole)）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 五、標籤
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=48, D_r=52, D_fill=-25,
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

    def item(a, text, color, size, dx, dy, key, disc=False, side=0):
        """side=±1：標籤放在錨點右／左邊，dx 自動加半個字寬（東在左）"""
        if side:
            w, _ = MC.label_box(text, size, m.fu)
            dx = side * (abs(dx) + w / 2)
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                  dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    BELT = [MINTAKA, ALNILAM, ALNITAK]
    SWORD = [C_ORI, IOTA_ORI]
    CRB = uniq([T["010"]])
    CAS = uniq([T["011"]])
    CRUX = [GACRUX, ACRUX, MIMOSA, IMAI]
    GEM = [CASTOR, POLLUX]

    # ── 長圖 ──
    TONGAN = [
        item(BELT, "ʻAlotolu", "blue", 1.5, 3.2, 1.6, "ʻAlotolu", side=1),
        item(SWORD, "Tuinga ika", "blue", 1.3, 2.4, -0.8, "Tuinga ika", side=1),
        item(HYADES, "Tuʻulalupe", "green", 1.5, 0.0, -4.4, "Tuʻulalupe"),
        item([ALCYONE], "Mataliki", "amber", 1.5, 0.0, 3.4, "Mataliki"),
        item(CRB, "ʻAo ʻo ʻUvea", "green", 1.5, 0.0, -4.6, "ʻAo ʻo ʻUvea"),
    ]
    TONGAN_ZH = [
        item(BELT, "一船三人", "blue", 1.2, 3.2, -0.9, "ʻAlotolu", side=1),
        item(SWORD, "一串魚", "blue", 1.1, 2.4, -3.0, "Tuinga ika", side=1),
        item(HYADES, "鴿子的棲架", "green", 1.2, 0.0, -6.8, "Tuʻulalupe"),
        item([ALCYONE], "昴宿星團", "amber", 1.2, 0.0, 1.4, "Mataliki"),
        item(CRB, "ʻUvea 的圓環", "green", 1.2, 0.0, -7.0, "ʻAo ʻo ʻUvea"),
    ]
    PERCH = [
        item(HYADES, "Tuʻulalupe", "green", 1.5, 0.0, -4.4, "Tuʻulalupe"),
        item(HYADES, "鴿子的棲架", "green", 1.2, 0.0, -6.8, "Tuʻulalupe-zh"),
        item([ALCYONE], "Mataliki", "amber", 1.5, 0.0, 4.6, "Mataliki"),
        item([ALCYONE], "昴宿星團", "amber", 1.2, 0.0, 2.5, "Mataliki-zh"),
    ]
    BOAT = [
        item(BELT, "ʻAlotolu", "blue", 1.0, 2.0, 1.0, "ʻAlotolu", side=1),
        item(BELT, "一船三人", "blue", 0.8, 2.0, -0.6, "ʻAlotolu-zh", side=1),
        item(SWORD, "Tuinga ika", "blue", 0.9, 1.6, -0.2, "Tuinga ika", side=-1),
        item(SWORD, "一串魚", "blue", 0.75, 1.6, -1.6, "Tuinga ika-zh", side=-1),
    ]
    PLEI = [
        item([ALCYONE], "Mataliki", "amber", 1.1, 0.0, 3.3, "Mataliki"),
        item([ALCYONE], "昴宿星團", "amber", 0.85, 0.0, 1.9, "Mataliki-zh"),
        item([ALCYONE], "Makaliʻi（夏威夷）", "white", 0.8, 0.0, -2.0, "Makaliʻi"),
        item([ALCYONE], "Matariki（毛利）", "white", 0.8, 0.0, -3.2, "Matariki"),
    ]
    NAMES = [
        item([BETELGEUSE], "參宿四", "white", 1.0, 2.0, 0.0, "HIP 27989", side=-1),
        item([RIGEL], "參宿七", "white", 1.0, 2.0, 0.0, "HIP 24436", side=1),
        item([ALDEBARAN], "畢宿五", "white", 1.0, 2.0, 0.0, "HIP 21421", side=-1),
        item([SIRIUS], "天狼星", "white", 1.0, 0.0, -2.4, "HIP 32349"),
    ]
    STEL = [
        item(BELT, "Toloa 野鴨", "purple", 1.4, 0.0, 3.6, "St-Toloa"),
        item(GEM, "Lua tangata 兩個人", "purple", 1.4, 2.4, 0.0, "St-Lua tangata", side=1),
        item([BETELGEUSE], "Velitoa hahake", "purple", 1.1, 2.0, 0.6, "St-Velitoa hahake", side=-1),
        item([RIGEL], "Velitoa hihifo", "purple", 1.1, -3.5, -3.8, "St-Velitoa hihifo"),   # 參宿七正下方、靠右對齊，不壓 Houmatoloa 紫線
        item([ALCYONE], "Motuliki", "purple", 1.2, 0.0, 2.6, "St-Motuliki"),
        item(HYADES, "Tuʻulalupe 畢宿", "purple", 1.2, 0.0, -4.4, "St-Tuʻulalupe"),
    ]
    POLE = [item([POLARIS], "北極星", "white", 1.2, 0.0, -2.6, "HIP 11767")]

    # ── 南盤（原生文字不跟著盤轉：dx/dy＝畫面方向）──
    FIRE = [item(LMC, "Maʻafulele？", "white", 2.0, 0.0, 9.6, "LMC", disc=True),
            item(SMC, "Maʻafutoka？", "white", 2.0, 0.0, 7.6, "SMC", disc=True)]
    FIRE_ZH = [item(LMC, "跑動的火？", "white", 1.6, 0.0, 5.4, "LMC", disc=True),
               item(SMC, "躺著不動的火？", "white", 1.6, 0.0, 3.4, "SMC", disc=True)]
    NAMES_S = [item(LMC, "大麥哲倫雲", "white", 1.5, 0.0, -7.6, "LMC-zh", disc=True),
               item(SMC, "小麥哲倫雲", "white", 1.5, 0.0, -4.4, "SMC-zh", disc=True),
               item([CANOPUS], "老人星", "white", 1.5, 0.0, -3.0, "HIP 30438", disc=True),
               item([ACHERNAR], "水委一", "white", 1.5, 0.0, -3.0, "HIP 7588", disc=True)]
    DUCK = [item(CRUX, "Toloa", "amber", 2.3, 0.0, 9.6, "Toloa", disc=True),
            item(CRUX, "野鴨（南十字）", "amber", 1.7, 0.0, 6.6, "Toloa-zh", disc=True)]
    PARTS = [item([GACRUX], "頭", "amber", 1.3, 0.0, 2.0, "γ", disc=True),
             item([ACRUX], "尾", "amber", 1.3, 0.0, -2.1, "α", disc=True),
             item([MIMOSA], "翅膀", "amber", 1.3, 1.6, 0.0, "β", disc=True, side=-1),
             item([IMAI], "受傷的翅膀", "amber", 1.3, 5.2, 1.7, "δ", disc=True),
             item([GINAN], "石頭 Maka", "red", 1.2, 1.2, -1.7, "ε", disc=True, side=1),
             item([RIGIL, HADAR], "Ongo Tangata", "red", 1.4, 3.0, -4.0, "Ongo Tangata", disc=True),
             item([RIGIL, HADAR], "兩個人", "red", 1.2, 3.0, -6.3, "Ongo Tangata-zh", disc=True),
             item([RIGIL], "南門二", "white", 1.1, 0.0, 2.0, "HIP 71683", disc=True),
             item([HADAR], "馬腹一", "white", 1.1, 0.0, 2.0, "HIP 68702", disc=True)]
    seg1, seg2, ratio, miss = pointer_path(S)
    mid = seg2[len(seg2) // 2]
    POINT = [item(SCP, "南天極", "red", 1.6, 4.0, 0.0, "SCP", disc=True, side=1),
             item(mid, f"往下延長 {ratio - 1:.1f} 倍", "red", 1.4, 2.6, 0.0, "指南線", disc=True, side=1)]
    # ── 北盤 ──
    WING = [item(CAS, "Kapakau ʻo Tafahi", "green", 2.0, 0.0, 11.2, "Kapakau ʻo Tafahi", disc=True),
            item(CAS, "Tafahi 的翅膀", "green", 1.6, 0.0, 8.4, "Kapakau-zh", disc=True)]   # 避開 W 頂點王良四
    CAS_Q = [item(CAS, "仙后座？", "white", 1.4, 9.0, 0.0, "Cas", disc=True, side=1)]
    RING = [item(CRB, "ʻAo ʻo ʻUvea", "green", 2.2, 0.0, 10.8, "ʻAo ʻo ʻUvea", disc=True),
            item(CRB, "ʻUvea 的圓環", "green", 1.7, 0.0, 6.0, "ʻAo-zh", disc=True),
            item(CRB, "北冕座？", "white", 1.5, 10.0, 0.0, "CrB", disc=True, side=1)]   # 放圓環右側，不壓左腳
    # 台北頁 fov 118：原生字夾到 36px 後會往兩側變寬，橫向間距要留大一點
    TPE = [item(CAS, "Kapakau ʻo Tafahi", "green", 2.0, 9.0, 2.6, "Kapakau ʻo Tafahi", disc=True, side=1),
           item([ALCYONE], "Mataliki", "amber", 2.0, 0.0, 4.4, "Mataliki", disc=True),
           item(HYADES, "Tuʻulalupe", "green", 2.0, 10.0, 1.8, "Tuʻulalupe", disc=True, side=-1)]
    TPE_ZH = [item(CAS, "仙后座", "white", 1.5, 9.0, -2.4, "Cas-zh", disc=True, side=1),
              item([ALCYONE], "昴宿", "white", 1.5, 0.0, -4.4, "Pleiades-zh", disc=True),
              item(HYADES, "畢宿", "white", 1.5, 10.0, -3.2, "Hyades-zh", disc=True, side=-1)]

    label_sets = [
        (TONGAN, "東加名"), (TONGAN_ZH, "中譯"), (PERCH, "鴿"), (BOAT, "船"), (PLEI, "昴"),
        (NAMES, "星名"), (STEL, "Stellarium"),
        (POLE, "北極星"),
        (FIRE, "火-南盤"), (FIRE_ZH, "火譯-南盤"), (NAMES_S, "星名-南盤"), (DUCK, "鴨-南盤"),
        (PARTS, "部位-南盤"), (POINT, "指南-南盤"),
        (WING, "翅膀-北盤"), (CAS_Q, "仙后-北盤"), (RING, "圓環-北盤"), (TPE, "台北-北盤"),
        (TPE_ZH, "台北譯-北盤"),
    ]

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
    m.L_marks([GINAN], "石頭白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot"), ([GINAN], "石頭白圈", "ring")])
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole
    ROT_S22 = round(rot_s(LST_AT["東加 11/13 22:00"]), 2)            # 11/13 22:00 東加面向南方
    ROT_CRUX = round(rot_s(LST_AT[f"東加 5/{CRUX_DAY} 21:00"]), 2)    # 5 月晚上九點：野鴨直立
    ROT_VAV = round(rot_n(LST_AT["Vavaʻu 11/13 21:48"]), 2)          # 11/13 21:48 Vavaʻu 面向北方
    ROT_UVEA = round(rot_n(LST_AT["東加 7/1 21:39"]), 2)              # 7/1 21:39 東加本島面向北方
    ROT_TPE = round(rot_n(LST_AT["台北 11/13 20:00"]), 2)             # 11/13 20:00 台北面向北方
    for nm, r in (("ROT_S22", ROT_S22), ("ROT_CRUX", ROT_CRUX), ("ROT_VAV", ROT_VAV),
                  ("ROT_UVEA", ROT_UVEA), ("ROT_TPE", ROT_TPE)):
        print(f"  {nm} = {r:+.2f}°")

    OPEN0 = (-18.0, 0.0, 52.0, 0.0)
    OPEN1 = (-34.0, 0.0, 52.0, 0.0)
    COR0 = (0.0, -8.0, 44.0, 0.0)                    # 走廊出發點（往南、往北都從這裡）
    COR_S = (0.0, -60.0, 44.0, 0.0)                  # 水委一
    SW_S = (0.0, -yp, 44.0, 0.0)            # 長圖 ⇄ 南盤 換組格
    MAF = (-22.0, -105.0, 84.0, ROT_S22)             # 麥哲倫雲＋老人星＋南方地平線
    cx_c, cy_c = disc_xy(m, *centroid(CRUX, S), ROT_CRUX, False)
    cx_m, cy_m = disc_xy(m, *centroid([RIGIL, HADAR], S), ROT_CRUX, False)
    CRUX_UP = (round(cx_c - 8.0, 2), round(cy_c - 33.0, 2), 70.0, ROT_CRUX)
    DUCK_F = (round(cx_c - 8.0, 2), round(cy_c - 2.0, 2), 44.0, ROT_CRUX)
    POINTER = (round(cx_c * 0.5, 2), round(-yp + 10.0, 2), 62.0, ROT_CRUX)
    COR_N = (0.0, 60.0, 44.0, 0.0)                   # 仙后 W（走廊上）
    SW_N = (0.0, yp, 44.0, 0.0)             # 長圖 ⇄ 北盤 換組格
    cx_w, cy_w = disc_xy(m, *centroid(CAS, S), ROT_VAV, True)
    VAV = (round(cx_w, 2), round(cy_w + 6.0, 2), 60.0, ROT_VAV)
    VAV_Z = (round(cx_w, 2), round(cy_w + 2.0, 2), 46.0, ROT_VAV)
    cx_u, cy_u = disc_xy(m, *centroid(CRB, S), ROT_UVEA, True)
    UVEA = (round(cx_u, 2), round(cy_u - 18.0, 2), 84.0, ROT_UVEA)
    HYA = (-48.0, 16.0, 36.0, 0.0)
    ORI_Z = (-68.5, -1.5, 24.0, 0.0)
    PLE = (-43.0, 21.0, 24.0, 0.0)
    STEL_F = (-84.0, 2.0, 54.0, 0.0)
    SW_N2 = (0.0, yp, 50.0, 0.0)
    TPE_F = (52.0, round(yp + 16.0, 2), 118.0, ROT_TPE)
    END_F = (52.0, round(yp + 16.0, 2), 120.0, round(ROT_TPE - 5.0, 2))

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="S", sec=11, north=True,
             frames=[OPEN0, OPEN1], layers=["深空"], labels=[],
             vo="上週，我們跟著夏威夷的四條星線回家。今晚再往南五千公里，到東加。"
                "同一片星空，東加人看見——一條條航線。",
             card="同一片星空，東加人看見——一條條航線。",
             note="開場字卡；十一月東加晚空（RA 15°（1h）在子午線＝11/13 22:10）往東緩慢平移，先不開連線"),
        dict(code="02", kind="Z", sec=22, north=True,
             frames=[OPEN1, COR0], layers=["深空"], labels=[],
             overlay="C-A10-01_東加地圖", overlay_layers=["島嶼層"],
             vo="東加有一百七十座左右的島，東加人把天文當成航海的一部分。他們的星空，幾乎只留在一份航海指南裡："
                "一八九〇年代的首相、大酋長 Tukuʻaho 寫下，一九二二年傳教士 Collocott 整理出版。"
                "所以有些東加星名，本身就是一句航海指令。",
             note="滑回走廊；結束後疊概念圖 東加地圖（島嶼層）"),
        dict(code="03", kind="T", sec=10, north=False,
             frames=[COR0, COR_S, SW_S], layers=["深空"], labels=[],
             vo="先往南看。東加本島在南緯二十一度，南方天空的軸心是南天極——"
                "那裡沒有亮星，只有兩團淡淡的光。",
             note="沿走廊往南：鯨魚 → 水委一 →（迄格＝04 起格：長圖轉南盤）"),
        dict(code="04", kind="R", sec=16, north=False,
             frames=[SW_S, MAF], layers=["深空"], labels_start=[],
             labels=ls("火-南盤", "火譯-南盤"), horizon=[PHI_T],
             vo="東加人叫它們 Maʻafu，火：一團是 Maʻafulele，跑動的火；一團是 Maʻafutoka，"
                "躺著不動的火。哪團是哪團，紀錄互相矛盾。Baker 的辭典說，這兩團光就是麥哲倫雲，在台灣永遠看不到。",
             note=f"長圖轉南盤（同框換組）→ 南盤轉到 {ROT_S22:+.1f}°（＝11/13 22:00 東加面向南方）、拉遠；"
                  "山升到東加地平線（南緯 21.1°）。名字後面的「？」＝兩種紀錄對應相反"),
        dict(code="05", kind="R", sec=12, north=False,
             frames=[MAF, CRUX_UP], layers=["深空", "鴨"], labels_start=ls("火-南盤", "火譯-南盤"),
             labels=ls("鴨-南盤"), horizon=[PHI_T],
             vo="把時間往前轉：十一月，這隻鳥要過了半夜才升起；到了五月的晚上，"
                "它直直站在南方——南十字，東加人叫它 Toloa，野鴨。",
             note=f"南盤順時針轉到 {ROT_CRUX:+.1f}°（＝5/{CRUX_DAY} 21:00 東加面向南方，南十字上中天）；"
                  "旋轉中不放原生標籤；迄格開野鴨標籤"),
        dict(code="06", kind="R", sec=19, north=False,
             frames=[CRUX_UP, DUCK_F], layers=["深空", "鴨", "人", "石"], labels_start=ls("鴨-南盤"),
             labels=ls("部位-南盤"), horizon=[PHI_T],
             vo="頭是最上面那顆，尾巴是最亮的底星，左右兩顆是翅膀。右邊這片翅膀暗了四倍——"
                "傳說是被石頭砸傷的。丟石頭的，是旁邊的兩個人 Ongo Tangata，南門二和馬腹一；"
                "那顆石頭 Maka，還卡在十字裡。",
             note="同角度推近南十字＋南門二、馬腹一；迄格開部位標籤（頭 γ、尾 α、翅膀 β、受傷的翅膀 δ、石頭 ε）"),
        dict(code="07", kind="R", sec=17, north=False,
             frames=[DUCK_F, POINTER], layers=["深空", "鴨", "人", "指南"],
             labels_start=ls("部位-南盤"), labels=ls("鴨-南盤", "指南-南盤"), horizon=[PHI_T],
             vo="這隻野鴨也是指南針：把頭和尾巴連起來，往下延長四倍半，就是南天極；"
                "從那裡垂直落到地平線，就是正南。旁邊這兩個人，在夏威夷叫『指針』，在毛利是一艘船的纜繩。",
             note=f"拉遠；指南線（紅）從 γ 經 α 往下再延長 {ratio - 1:.1f} 倍，在南天極旁 {miss:.1f}° 通過"),
        dict(code="08", kind="T", sec=13, north=True,
             frames=[COR0, COR_N, SW_N], layers=["深空"], labels=[], labels_end=ls("北極星"),
             vo="那往北呢？Stellarium 的東加資料寫著：奇怪，東加人沒有幫北極星取名。"
                "其實一點也不奇怪——從東加本島看，北極星永遠在地平線下二十度以上。",
             note="南盤轉長圖（盤轉回 0°、換組、沿走廊上移回出發點）→ 沿走廊往北經過仙后 W 到北極星"
                  "（迄格＝09 起格：長圖轉北盤）"),
        dict(code="09", kind="R", sec=11, north=True,
             frames=[SW_N, VAV], layers=["翼"], labels_start=ls("北極星"),
             labels=ls("翅膀-北盤"), horizon=[PHI_V],
             vo="往北的路，要看別的星。十一月中、晚上十點，站在北邊的 Vavaʻu 島往北看："
                "海面上方十度上下，蹲著一個 W。",
             note=f"長圖轉北盤 → 北盤逆時針轉到 {ROT_VAV:+.1f}°（＝11/13 21:48 Vavaʻu 面向北方）；"
                  "山升到 Vavaʻu 地平線（南緯 18.7°）——地平線在北極星「上方」，北極星藏在山後"),
        dict(code="10", kind="R", sec=23, north=True,
             frames=[VAV, VAV_Z], layers=["翼"], labels_start=ls("翅膀-北盤"),
             labels=ls("翅膀-北盤", "仙后-北盤"), horizon=[PHI_V],
             overlay="C-A10-02_Tafahi的翅膀", overlay_layers=["地平層", "母雞層"],
             vo="東加人叫它 Kapakau ʻo Tafahi，Tafahi 的翅膀。指南說，它像一隻母雞，"
                "張開翅膀孵在 Tafahi 島上；Tafahi 在 Vavaʻu 幾乎正北、三百多公里外，遠到看不見島，只看得見星。"
                "是哪八顆星，各家說法不同，Stellarium 猜是仙后座。",
             note="推近；結束後疊概念圖 Tafahi 的翅膀（地平層→母雞層）"),
        dict(code="11", kind="R", sec=20, north=True,
             frames=[VAV_Z, UVEA], layers=["環"], labels_start=ls("翅膀-北盤", "仙后-北盤"),
             labels=ls("圓環-北盤"), horizon=[PHI_V, PHI_T],
             overlay="C-A10-01_東加地圖", overlay_layers=["島嶼層", "航線層"],
             vo="另一句更直接：一圈小星叫 ʻAo ʻo ʻUvea，ʻUvea 的圓環。要等它像頭環一樣戴在 ʻUvea 的上空，"
                "才拿來駕船。ʻUvea 在東加本島北方八百八十公里；Stellarium 推測它是北冕座——"
                "七月的晚上，北冕座正好升到北方最高。",
             note=f"北盤轉到 {ROT_UVEA:+.1f}°（＝7/1 21:39 東加本島面向北方，北冕座上中天、高 42°）；"
                  "山移到東加本島地平線；結束後疊概念圖 東加地圖（島嶼→航線）"),
        dict(code="12", kind="Z", sec=15, north=True,
             frames=[COR0, HYA], layers=["鴿", "深空"], labels_start=[],
             labels=ls("鴿"),
             vo="還有一句：Tuʻulalupe，鴿子的棲架，要等它像棲架一樣直直站起來才能用——"
                "捉鴿子，是古代東加酋長的運動。Stellarium 把它放在畢宿，也有學者猜是天鵝座。",
             note="北盤轉長圖（歸位、換組、沿走廊下移）→ 往東（左）滑到畢宿；迄格開東加名＋中譯"),
        dict(code="13", kind="Z", sec=19, north=True,
             frames=[HYA, ORI_Z], layers=["船", "魚", "深空"], labels_start=ls("鴿"),
             labels=ls("船"),
             vo="旁邊的獵戶腰帶叫 ʻAlotolu，一條船上三個人。傳說女孩 Hina 養的小鯊魚游走了，"
                "她和爸爸媽媽划船出海找；最後 Hina 留在海上，變成一座礁，那條船到了天上。"
                "船旁邊那串小星，叫 Tuinga ika，一串魚。",
             note="往下移到獵戶腰帶與獵戶之劍（一串魚）；獵戶座大星雲在劍上"),
        dict(code="14", kind="Z", sec=23, north=True,
             frames=[ORI_Z, PLE], layers=["深空"], labels_start=ls("船"),
             labels=ls("昴"),
             vo="上面那一小團是昴宿 Mataliki，跟夏威夷的 Makaliʻi、毛利的 Matariki 是同一個字。"
                "東加的一年大約跟西曆同時開始，Collocott 拿 Mangaia 島比，猜可能跟昴宿黃昏東升這類天象有關。閏月更妙：新月那天去看山藥，"
                "還沒長成第一個月該有的樣子，就多插一個月。",
             note="往上滑到昴宿並推近"),
        dict(code="15", kind="Z", sec=21, north=True,
             frames=[PLE, STEL_F], layers=["St", "深空"], labels_start=ls("昴"),
             labels=ls("Stellarium"),
             overlay="C-A10-03_兩份東加星圖",
             vo="要老實說：Stellarium 的東加星空，跟 Collocott 的紀錄很多地方對不上——"
                "野鴨飛到了獵戶腰帶，兩個人搬去雙子座，還多了一條線把三隻鴨子串起來。"
                "它另外參考了兩本一九九〇年的書；東加各群島的叫法，本來就不一樣。",
             note="拉遠：Stellarium 版連線（紫）與名字；結束後疊 9:16 對照表（可存圖）"),
        dict(code="16", kind="R", sec=21, north=True,
             frames=[SW_N2, TPE_F], layers=["翼", "鴿", "深空"], labels_start=[],
             labels=ls("台北-北盤", "台北譯-北盤"), horizon=[PHI_TPE],
             vo="今晚八點在台北抬頭：北方高高掛著仙后座——Stellarium 版的 Tafahi 翅膀，比在東加高了四十多度；"
                "東方，昴宿和畢宿已經升起。台灣看不到 Maʻafu 的兩團火；野鴨和兩個人，"
                "要等春天到南部海邊，才貼著地平線露臉。",
             note=f"長圖回中心、上移、轉北盤 → 逆時針轉到 {ROT_TPE:+.1f}°（＝11/13 20:00 台北面向北方）；"
                  "山升到台北地平線"),
        dict(code="17", kind="R", sec=9, north=True,
             frames=[TPE_F, END_F], layers=["翼", "鴿", "深空"],
             labels_start=ls("台北-北盤", "台北譯-北盤"), labels=ls("台北-北盤", "台北譯-北盤"),
             horizon=[PHI_TPE],
             vo="下週五，去一座不到半平方公里的小島，阿努塔：南十字和這兩個人，在那裡變成一張漁網。",
             card="下集見｜阿努塔：半平方公里小島的星空智慧",
             note="盤再轉 20 分鐘；端卡＋追蹤 CTA"),
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
    for sh in shots:                                   # Canva M&M：單段旋轉 < 180°
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 178.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° 太接近 180°（Canva 可能反轉）")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                yc = m.y_pole if sh["north"] else -m.y_pole
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
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

    terms = {
        "Toloa": dict(hips=CRUX, 原文="Toloa", 拼音="", 英文翻譯="wild duck", 中文="野鴨（南十字）",
                      顏色="amber", 來源備註="Collocott 1922：頭 γ、尾 α、翅 β δ；Stellarium 另把 Toloa 給獵戶腰帶、南十字叫 Toloatonga"),
        "Ongo Tangata": dict(hips=[RIGIL, HADAR], 原文="Ongo Tangata", 拼音="", 英文翻譯="the two men",
                             中文="兩個人（南門二、馬腹一）", 顏色="red",
                             來源備註="Collocott 1922：丟石頭砸傷野鴨 δ 翅；Stellarium 的 Lua tangata 在雙子座、α β Cen 叫 Fungasia"),
        "Maka": dict(hips=[GINAN], 原文="Maka", 拼音="", 英文翻譯="stone", 中文="石頭（南十字 ε 星）",
                     顏色="red", 來源備註="Collocott 1922"),
        "Maʻafulele": dict(hips=[], 原文="Maʻafulele", 拼音="", 英文翻譯="running fire", 中文="跑動的火",
                           顏色="white", 來源備註="Collocott 1922：南天兩團亮斑；Baker 指小麥哲倫雲，Stellarium 指大麥哲倫雲（另給天狼星）"),
        "Maʻafutoka": dict(hips=[], 原文="Maʻafutoka", 拼音="", 英文翻譯="lying (stationary) fire",
                           中文="躺著不動的火", 顏色="white",
                           來源備註="Collocott 1922；Baker 指大麥哲倫雲，Stellarium 指小麥哲倫雲（另給老人星）"),
        "Kapakau ʻo Tafahi": dict(hips=CAS, 原文="Kapakau ʻo Tafahi", 拼音="", 英文翻譯="wing of Tafahi",
                                  中文="Tafahi 的翅膀", 顏色="green",
                                  來源備註="Collocott 1922：八顆星，像母雞張開翅膀孵在 Tafahi 上；Stellarium 推測仙后座"),
        "ʻAo ʻo ʻUvea": dict(hips=CRB, 原文="ʻAo ʻo ʻUvea", 拼音="", 英文翻譯="circlet of ʻUvea",
                             中文="ʻUvea 的圓環", 顏色="green",
                             來源備註="Collocott 1922：圓形星群，等它像頭環戴在 ʻUvea 上空才用；Stellarium 譯 Cloud、推測北冕座"),
        "Tuʻulalupe": dict(hips=HYADES, 原文="Tuʻulalupe", 拼音="", 英文翻譯="pigeon roost / perch",
                           中文="鴿子的棲架", 顏色="green",
                           來源備註="Collocott 1922：北方五顆星，像棲架直立才用；Stellarium＝畢宿，Makemson 猜天鵝座"),
        "ʻAlotolu": dict(hips=BELT, 原文="ʻAlotolu", 拼音="", 英文翻譯="three in a boat", 中文="一船三人",
                         顏色="blue", 來源備註="Collocott 1922；Gifford 1924〈The Origin of the Reef Matahina〉"),
        "Tuinga ika": dict(hips=SWORD, 原文="Tuinga ika", 拼音="", 英文翻譯="string of fish", 中文="一串魚",
                           顏色="blue", 來源備註="Collocott 1922；Stellarium 版連成腰帶＋劍"),
        "Mataliki": dict(hips=[ALCYONE], 原文="Mataliki", 拼音="", 英文翻譯="the Pleiades", 中文="昴宿星團",
                         顏色="amber", 來源備註="Collocott 1922、Churchward 辭典；Stellarium 星名檔寫 Motuliki"),
    }
    for items, name in label_sets:
        for it in items:
            if it["key"].startswith("HIP"):
                terms.setdefault(it["key"], dict(hips=[int(it["key"][4:])], 原文=it["text"], 拼音="",
                                                 英文翻譯="", 中文=it["text"], 顏色=it["color"],
                                                 來源備註="台灣通行星名"))
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Te Kupenga", 中譯="漁網（南十字＋南門二、馬腹一）", 英文="The Net",
                              顏色="amber"),
                         dict(原文="Nā Kuhikuhi", 中譯="指針（南門二、馬腹一）", 英文="The Pointers",
                              顏色="red"),
                         dict(原文="Hānaiakamalama", 中譯="月亮照看的孩子（南十字）",
                              英文="Cared for by Moon", 顏色="amber")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "crux_day": CRUX_DAY,
               "rot": dict(S22=ROT_S22, CRUX=ROT_CRUX, VAV=ROT_VAV, UVEA=ROT_UVEA, TPE=ROT_TPE),
               "pointer": dict(ratio=ratio, miss_deg=miss)},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL + LG_STEL,
                  labels=[dict(it, pt=6) for it in items],
                  title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots, line_groups=LG_ALL,
              labels=[dict(it, pt=5) for it in TONGAN + DUCK + WING + RING + FIRE],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
