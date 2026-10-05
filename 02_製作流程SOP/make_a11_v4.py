# -*- coding: utf-8 -*-
"""A-11 阿努塔：半平方公里小島的星空智慧｜大畫布 v4.6

論點：阿努塔（所羅門群島東端，0.37 km²、約三百人）把整座島的生活掛到天上——
扁擔 Te Aamonga（河鼓三星，和台灣民間的「扁擔星」同一組）、火鉗 Te Angaanga（畢宿）、
竹子 Te Kope（天鶴）、章魚腳 Kaavei（白羊）、芋頭 Taro（天蠍）、漁網 Te Kupenga（南十字＋南門二、馬腹一）；
天上最大的是一隻鳥 Manu（天狼＝身體、老人星＝東翼、南河三＝北翼）。北翼較短（25.7° 對 36.2°），
傳說是跟 Motikitiki 爭 Taro（心宿二）時被打斷的。老人星旁的 α Pic 叫「東翼的領路星」：
在阿努塔的緯度，它確實比老人星早約六分鐘升起（赤道上反過來）。
來源：Feinberg 1988《Polynesian Seafaring and Navigation》（Stellarium anutan＝Bucur 2021 依此書數位化）、
Feinberg 1995 JPS〈Christian Polynesians and Pagan Spirits〉（Manu 的斷翼）、Firth 1954 JPS（Tikopia→阿努塔星路九顆星）。

鏡頭路線：長圖（十一月阿努塔晚空）→ 西天：扁擔、竹子 → 東天：章魚腳、火鉗、三人之路（生活星空圖卡）
→ Manu（斷翼概念圖）→ 往東到 Taro → 回走廊：領路星 → 沿鳥身往南 → 南盤（阿努塔地平線）：
領路星與東翼升起 → 奔跑的雲／靜止的雲 → 轉到清晨：漁網升起、改名「神聖的木頭」
→ 回長圖：星路 kaavenga（概念圖）、Manu＝布吉斯的 Manu'＝*manuk（圖卡）→ 南盤：今晚台灣 → 端卡。

輸出：L1銀河 L2星點 L3經緯線 L4星座連線（阿努塔 11 組全開）
      連線-Manu／漁網／芋頭／生活（扁擔、竹子、石錛、章魚腳、火鉗、三人之路、領路星、魚）
      深空天體（大小麥哲倫雲、昴宿、獵戶座大星雲）、主角星白點、領路星白圈
      標籤（長圖）：阿努塔名／中譯／Manu／Manu譯／芋頭／領路／布吉斯／星名
      標籤（南盤）：領路-南盤／雲-南盤／網-南盤／十字-南盤／星名-南盤／台灣-南盤
執行：python3 make_a11_v4.py

參數
  lst = 100 → 走廊（x=0）＝RA 100°：正好穿過 Manu 的身體——往南是天狼（x −1）、老人星（+4）、
             α Pic（−2）、大麥哲倫雲，一路到南天極；鳥身就是進出南盤的走廊。
             接縫 x=±180 在 RA 280（人馬座）：人馬座（Te Paka Poi Ika Tapu）不上長圖，改放星路概念圖。
  D_s = 53、D_r = 57 → 老人星（−52.7）、天鶴 ε（−51.3）都在帶內；走廊外的帶一直延伸到 −57，
             長圖畫面底邊落在山的剪影後面時，帶外的填滿圓內容不會從山谷露出來
             （fov ≤ 56 時，底邊 y_b 可取 −57−0.10·fov ～ −51.3−0.20·fov）。
             南十字（γ −57.1 起）、南門二、馬腹一、α Pic、大小麥哲倫雲都進南盤本體。
  D_fill = −13 → k=1.736、R_fill=178.8；南盤收到 dec +13：天狼（r 127）、南河三（r 165）都在南盤上，
             台灣面向南方的畫面（老人星貼海面、天狼高 48°）可以在南盤上做。
  x_tN = x_tS = 0（Canva 可水平置中）
  南盤 R：Canva 正角＝順時針＝時間前進；rot＝lst_obs−lst（gen_canva_pages.view_lst）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-11"
OUT = os.path.join(BASE, "05_素材/A-11_阿努塔/_v4大畫布")
LST0 = 100.0
ANUTA = (-11.611, 169.850)          # 阿努塔（11°36′40″S、169°51′E），UTC+11
PHI_A = ANUTA[0]
PHI_TPE = 25.03                     # 台北


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）
# ══════════════════════════════════════════════════════════════════
def lst_at(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return math.degrees(o.sidereal_time())


LST_AT = {
    "阿努塔 11/20 18:45": lst_at(*ANUTA, 11, "2026/11/20 18:45"),
    "阿努塔 11/20 21:00": lst_at(*ANUTA, 11, "2026/11/20 21:00"),
    "阿努塔 11/21 04:00": lst_at(*ANUTA, 11, "2026/11/21 04:00"),
    "台北 11/21 02:00": lst_at(25.0330, 121.5654, 8, "2026/11/21 02:00"),
    "台北 11/21 02:20": lst_at(25.0330, 121.5654, 8, "2026/11/21 02:20"),
}


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」：順時針＝時間前進"""
    return (lst_obs - LST0 + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SIRIUS, CANOPUS, PROCYON, APIC = 32349, 30438, 37279, 32607
GACRUX, ACRUX, MIMOSA, IMAI = 61084, 60718, 62434, 59747
RIGIL, HADAR = 71683, 68702
ANTARES = 80763
ALTAIR, TARAZED, ALSHAIN = 97649, 97278, 98036
ALDEBARAN, ALCYONE = 21421, 17702
HAMAL = 9884
MINTAKA, ALNILAM, ALNITAK = 25930, 26311, 26727
BETELGEUSE, RIGEL = 27989, 24436
ACHERNAR = 7588
BETA_GRU, GAMMA_GRU = 112122, 108085
MARKAB, SCHEAT, ALPHERATZ = 113963, 113881, 677

MAINS = [SIRIUS, CANOPUS, PROCYON, APIC, GACRUX, ACRUX, MIMOSA, IMAI, RIGIL, HADAR, ANTARES,
         ALTAIR, TARAZED, ALSHAIN, ALDEBARAN, ALCYONE, HAMAL, MINTAKA, ALNILAM, ALNITAK,
         BETA_GRU, GAMMA_GRU, MARKAB, SCHEAT, ACHERNAR]

LMC = (80.894, -69.756)      # 645′×550′，PA 170
SMC = (13.187, -72.829)      # 320′×185′，PA 45
M42 = (83.82, -5.39)
M45 = (56.75, 24.12)
SCP = (0.0, -89.999)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium anutan index.json＝Feinberg 1988 的 11 組）
# ══════════════════════════════════════════════════════════════════
def sc_lines(culture):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/"
                           f"{culture}/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: c["lines"] for c in d["constellations"]}


A = sc_lines("anutan")
LG_MANU = [(A["003"], "amber", 1.0)]                    # Manu 鳥
LG_NET = [(A["011"], "blue", 1.0)]                      # Te Kupenga 漁網（南十字＋網柄）
LG_TARO = [(A["010"], "green", 1.0)]                    # Taro 芋頭
LG_LIFE = [(A["008"], "green", 1.0),                    # Te Aamonga 扁擔
           (A["004"], "red", 1.0),                      # Te Angaanga 火鉗
           (A["001"], "blue", 1.0),                     # Te Kope 竹子
           (A["007"], "blue", 0.9),                     # Toki 石錛
           (A["005"], "purple", 1.0),                   # Kaavei 章魚腳
           (A["002"], "white", 1.0),                    # Ara Toru 三人之路
           (A["006"], "white", 0.8)]                    # Taki Mua 前面的領路星
LG_ALL = LG_MANU + LG_NET + LG_TARO + LG_LIFE
LINE_SETS = [(LG_MANU, "連線-Manu"), (LG_NET, "連線-漁網"), (LG_TARO, "連線-芋頭"),
             (LG_LIFE, "連線-生活")]
LINES_KEY = {"L4": "星座連線", "鳥": "連線-Manu", "網": "連線-漁網", "芋": "連線-芋頭",
             "活": "連線-生活", "深空": "深空天體", "領": "領路星白圈"}
LINE_GROUPS = {"L4": LG_ALL, "鳥": LG_MANU, "網": LG_NET, "芋": LG_TARO, "活": LG_LIFE}


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
# 三、旁白字數（中文字＋外文音節；與 A-10 同一套算法）
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
# 四、自訂圖層：深空天體（大畫布＋南北盤同步出）
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


def disc_xy(m, ra, dec, rot, north=False):
    """天體在「轉 rot 之後的盤」上的位置（畫面方向的畫布單位，盤心＝(0, ±y_pole)）"""
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 五、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=53, D_r=57, D_fill=-13,
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

    STICK = uniq([A["008"]])
    TONGS = uniq([A["004"]])
    BAMBOO = uniq([A["001"]])
    ADZE = uniq([A["007"]])
    OCTO = uniq([A["005"]])
    BELT = uniq([A["002"]])
    TAKIMUA = uniq([A["006"]])
    TARO = uniq([A["010"]])
    NET = uniq([A["011"]])
    CRUX = [GACRUX, ACRUX, MIMOSA, IMAI]
    MANU = [SIRIUS, CANOPUS, PROCYON]

    # ── 長圖：生活星空 ──
    # 上下疊的兩行：中心距 ≥ (字級1＋字級2)×0.85＋0.4，原生字放大後才不會壓在一起
    LIFE = [
        item(STICK, "Te Aamonga", "green", 1.5, -5.0, -3.6, "Te Aamonga"),           # 扁擔左下（右邊貼畫面邊）
        item(BAMBOO, "Te Kope", "blue", 1.5, 3.0, 1.4, "Te Kope", side=1),
        item(ADZE, "Toki", "blue", 1.3, 0.0, 5.4, "Toki"),
        item(OCTO, "Kaavei", "purple", 1.5, 0.0, 4.2, "Kaavei"),
        item([ALCYONE], "Matariki", "amber", 1.4, 0.0, 3.2, "Matariki"),
        item(TONGS, "Te Angaanga", "red", 1.5, 0.0, -3.6, "Te Angaanga"),
        item(BELT, "Ara Toru", "white", 1.4, 2.6, 1.0, "Ara Toru", side=1),
    ]
    LIFE_ZH = [
        item(STICK, "扁擔", "green", 1.3, -5.0, -6.6, "Te Aamonga-zh"),
        item(BAMBOO, "竹子", "blue", 1.3, 3.0, -1.6, "Te Kope-zh", side=1),
        item(ADZE, "石錛", "blue", 1.1, 0.0, 2.8, "Toki-zh"),
        item(OCTO, "章魚腳", "purple", 1.3, 0.0, 1.0, "Kaavei-zh"),
        item([ALCYONE], "小臉（昴宿）", "amber", 1.1, 0.0, 0.6, "Matariki-zh"),
        item(TONGS, "火鉗（畢宿）", "red", 1.3, 0.0, -6.6, "Te Angaanga-zh"),
        item(BELT, "三人之路", "white", 1.2, 2.6, -1.8, "Ara Toru-zh", side=1),
    ]
    MANU_L = [item(MANU, "Manu", "amber", 2.4, 6.0, -5.0, "Manu", side=-1),        # 鳥身左下的空天區
              item(MANU, "飛翔的鳥", "amber", 1.6, 6.0, -8.8, "Manu-zh", side=-1)]
    PARTS = [item([SIRIUS], "身體", "amber", 1.4, 2.0, 0.0, "Te Tino a Manu", side=1),
             item([CANOPUS], "東翼", "amber", 1.4, 2.0, 0.0, "Te Kapakau Tonga", side=1),
             item([PROCYON], "北翼", "amber", 1.4, 2.0, 0.0, "Te Kapakau Pakatokerau", side=-1)]
    NAMES = [item([SIRIUS], "天狼星", "white", 1.1, 0.0, -2.6, "HIP 32349"),
             item([CANOPUS], "老人星", "white", 1.1, 0.0, -2.6, "HIP 30438"),
             item([PROCYON], "南河三", "white", 1.1, 0.0, -2.6, "HIP 37279"),
             item([ALTAIR], "牛郎星", "white", 1.0, 0.0, -2.2, "HIP 97649"),
             item([ANTARES], "心宿二", "white", 1.1, 0.0, -2.6, "HIP 80763")]
    TARO_L = [item(TARO, "Taro", "green", 2.0, 0.0, 8.6, "Taro"),
              item(TARO, "芋頭", "green", 1.5, 0.0, 5.0, "Taro-zh"),
              item([ANTARES], "Na Kau 它的莖", "green", 1.2, 0.0, -5.2, "Na Kau")]          # 心宿二標籤下方
    LEAD = [item([APIC], "東翼的領路星", "white", 1.2, 2.0, 0.0, "Te Taki o te Kapakau Tonga", side=1)]
    BUGIS = [item(MANU, "Manu'", "white", 1.6, 3.0, -10.0, "Manu'", side=1),
             item(MANU, "（布吉斯：雞）", "white", 1.2, 3.0, -12.8, "Manu'-zh", side=1)]

    # ── 南盤（原生文字不跟著盤轉：dx/dy＝畫面方向）──
    LEAD_S = [item([APIC], "Te Taki o te Kapakau Tonga", "white", 1.6, 2.6, 1.4, "Te Taki", disc=True, side=1),
              item([APIC], "東翼的領路星", "white", 1.4, 2.6, -1.6, "Te Taki-zh", disc=True, side=1),
              item([CANOPUS], "東翼（老人星）", "amber", 1.5, 0.0, 3.0, "Te Kapakau Tonga", disc=True)]
    CLOUD_S = [item(LMC, "Te Ao Rere", "white", 2.0, 0.0, 10.0, "LMC", disc=True),
               item(LMC, "奔跑的雲", "white", 1.6, 0.0, 6.4, "LMC-zh", disc=True),
               item(SMC, "Te Ao Toka", "white", 2.0, 0.0, 7.6, "SMC", disc=True),
               item(SMC, "靜止的雲", "white", 1.6, 0.0, 4.0, "SMC-zh", disc=True)]
    NAMES_S = [item(LMC, "大麥哲倫雲", "white", 1.4, 0.0, -8.0, "LMC-n", disc=True),
               item(SMC, "小麥哲倫雲", "white", 1.4, 0.0, -5.6, "SMC-n", disc=True)]
    NET_S = [item(CRUX, "Te Kupenga", "blue", 2.2, 0.0, 9.6, "Te Kupenga", disc=True),
             item(CRUX, "漁網", "blue", 1.7, 0.0, 5.8, "Te Kupenga-zh", disc=True),
             item([RIGIL, HADAR], "網柄", "blue", 1.5, 3.0, 1.6, "Te Kau o te Kupenga", disc=True, side=1),
             item([RIGIL, HADAR], "Te Rua Tangata 兩個人", "red", 1.3, 3.0, -1.4, "Te Rua Tangata",
                  disc=True, side=1)]
    CROSS_S = [item(CRUX, "Te Rakau Tapu", "amber", 2.0, 0.0, 9.6, "Te Rakau Tapu", disc=True),
               item(CRUX, "神聖的木頭（1916 年後）", "amber", 1.4, 0.0, 6.0, "Te Rakau Tapu-zh",
                    disc=True)]
    TPE_S = [item(MANU, "Manu", "amber", 2.4, 8.0, 2.0, "Manu", disc=True, side=1),
             item([SIRIUS], "天狼星", "white", 1.6, 2.0, 0.0, "Sirius-tpe", disc=True, side=1),
             item([CANOPUS], "老人星", "white", 1.6, 2.0, 0.0, "Canopus-tpe", disc=True, side=1)]

    label_sets = [
        (LIFE, "阿努塔名"), (LIFE_ZH, "中譯"), (MANU_L, "Manu"), (PARTS, "部位"), (NAMES, "星名"),
        (TARO_L, "芋頭"), (LEAD, "領路"), (BUGIS, "布吉斯"),
        (LEAD_S, "領路-南盤"), (CLOUD_S, "雲-南盤"), (NAMES_S, "星名-南盤"), (NET_S, "網-南盤"),
        (CROSS_S, "十字-南盤"), (TPE_S, "台灣-南盤"),
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
    m.L_marks([APIC], "領路星白圈", "ring")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot"), ([APIC], "領路星白圈", "ring")])
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, S, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    yp = m.y_pole
    ROT_E0 = round(rot_s(LST_AT["阿努塔 11/20 18:45"]), 2)       # 領路星、老人星都還在海面下
    ROT_E1 = round(rot_s(LST_AT["阿努塔 11/20 21:00"]), 2)       # 兩顆都升到山的剪影上方
    ROT_DAWN = round(rot_s(LST_AT["阿努塔 11/21 04:00"]), 2)     # 漁網升起（天文晨光 03:49 剛過，天仍暗）
    ROT_TPE = round(rot_s(LST_AT["台北 11/21 02:00"]), 2)        # 台北面向南方
    ROT_TPE2 = round(rot_s(LST_AT["台北 11/21 02:20"]), 2)
    for nm, r in (("ROT_E0", ROT_E0), ("ROT_E1", ROT_E1), ("ROT_DAWN", ROT_DAWN),
                  ("ROT_TPE", ROT_TPE), ("ROT_TPE2", ROT_TPE2)):
        print(f"  {nm} = {r:+.2f}°")
    for nm, hip in (("α Pic", APIC), ("Canopus", CANOPUS), ("Sirius", SIRIUS), ("Procyon", PROCYON),
                    ("γ Cru", GACRUX), ("α Cen", RIGIL)):
        print(f"  {nm:8s} E1 {tuple(round(v, 1) for v in disc_xy(m, *S[hip][:2], ROT_E1))}"
              f"  DAWN {tuple(round(v, 1) for v in disc_xy(m, *S[hip][:2], ROT_DAWN))}"
              f"  TPE {tuple(round(v, 1) for v in disc_xy(m, *S[hip][:2], ROT_TPE))}")
    for nm, p in (("LMC", LMC), ("SMC", SMC)):
        print(f"  {nm:8s} E1 {tuple(round(v, 1) for v in disc_xy(m, *p, ROT_E1))}")
    print(f"  南點（阿努塔）y={-yp - m.k * abs(PHI_A):.1f}；南點（台北）y={-yp + m.k * PHI_TPE:.1f}")

    OPEN0 = (64.0, 6.0, 50.0, 0.0)
    OPEN1 = (46.0, 6.0, 50.0, 0.0)
    ISL = (46.0, 6.0, 46.0, 0.0)
    LIFE_W = (141.0, -12.9, 56.0, 0.0)               # 扁擔＋石錛＋竹子；底邊 −62.7：帶緣 −57 落在山後（1810 px）、天鶴 ε 在 1700 px
    LIFE_E = (42.0, 0.0, 62.0, 0.0)                  # 章魚腳、昴宿、火鉗、三人之路（上下緣 ±55，不出帶）
    MANU_F = (-6.0, -29.0, 50.0, 0.0)                # 整隻鳥（走廊上）
    WING = (-6.0, -27.0, 44.0, 0.0)
    TARO_F = (-145.0, -24.0, 34.0, 0.0)
    LEAD_F = (0.0, -44.0, 44.0, 0.0)                 # 走廊出發點：老人星＋領路星（α Pic −67 在山的剪影上方）
    SW_S = (0.0, -yp, 44.0, 0.0)                     # 長圖 ⇄ 南盤 換組格（T 半寬 22）
    SW_S2 = (0.0, -yp, 46.0, 0.0)                    # 第二次換組（＝15 鏡迄格的 fov，換組頁才能一頁兩用）

    # R 畫面：依 disc_xy 印出的位置取景（見上）
    E0 = (-46.0, round(-yp + 36.0, 2), 100.0, ROT_E0)
    E1 = (-46.0, round(-yp + 36.0, 2), 100.0, ROT_E1)
    lx, ly = disc_xy(m, *LMC, ROT_E1)
    sx, sy = disc_xy(m, *SMC, ROT_E1)
    CLOUD = (round((lx + sx) / 2, 2), round((ly + sy) / 2 - 6.0, 2), 66.0, ROT_E1)
    cx_c, cy_c = disc_xy(m, *centroid(CRUX + [RIGIL, HADAR], S), ROT_DAWN)
    NET_F = (round(cx_c, 2), round(cy_c + 8.0, 2), 76.0, ROT_DAWN)
    cx_x, cy_x = disc_xy(m, *centroid(CRUX, S), ROT_DAWN)
    CROSS_F = (round(cx_x, 2), round(cy_x + 2.0, 2), 40.0, ROT_DAWN)
    PATH_F = (-6.0, -27.0, 50.0, 0.0)
    BUG_F = (-6.0, -25.0, 46.0, 0.0)
    tx, ty = disc_xy(m, *centroid([SIRIUS, CANOPUS], S), ROT_TPE)
    TPE_F = (round(tx, 2), round(ty - 4.0, 2), 74.0, ROT_TPE)
    END_F = (round(tx, 2), round(ty - 4.0, 2), 76.0, ROT_TPE2)

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="S", sec=11, north=True,
             frames=[OPEN0, OPEN1], layers=["深空"], labels=[],
             vo="上週在東加。今晚往西北一千九百公里，到所羅門群島東端的小島阿努塔。"
                "同一片星空，阿努塔人看見——一隻大鳥。",
             card="同一片星空，阿努塔人看見——一隻大鳥。",
             note="開場字卡；十一月阿努塔晚空（21:30 子午線＝RA 27°，x +73）往東緩慢平移，先不開連線"),
        dict(code="02", kind="Z", sec=21, north=True,
             frames=[OPEN1, ISL], layers=["深空"], labels=[],
             overlay="C-A11-01_阿努塔地圖", overlay_layers=["島嶼層", "祖先層"],
             vo="阿努塔不到零點四平方公里，住了大約三百人，是太平洋有人長住的島裡，最小的之一。"
                "人在所羅門群島，說的卻是玻里尼西亞語。島上的傳說，祖先大約十五代以前，"
                "從東加和 ʻUvea 划船過來——就是上集那個要等「圓環」戴上頭的 ʻUvea。",
             note="輕推近；結束後疊概念圖 阿努塔地圖（島嶼層→祖先層）"),
        dict(code="03", kind="Z", sec=19, north=True,
             frames=[ISL, LIFE_W], layers=["活", "深空"], labels_start=[],
             labels=ls("阿努塔名", "中譯"),
             vo="先看西邊。阿努塔人的星座，很多是每天手上的東西：牛郎星和兩旁的兩顆，是一根扁擔 Te Aamonga，"
                "挑芋頭、挑椰子——跟台灣民間的「扁擔星」是同一根。下面彎彎的五顆是 Te Kope，竹子，"
                "做釣竿、桅杆的那種竹子。",
             note="往西（右）滑到天鷹、海豚、天鶴；迄格開阿努塔名＋中譯（扁擔、石錛、竹子）"),
        dict(code="04", kind="Z", sec=20, north=True,
             frames=[LIFE_W, LIFE_E], layers=["活", "深空"], labels_start=ls("阿努塔名", "中譯"),
             labels=ls("阿努塔名", "中譯"),
             overlay="C-A11-04_阿努塔的生活星空",
             vo="往東：白羊座三顆彎成一隻章魚腳 Kaavei；畢宿的 V 是火鉗 Te Angaanga，"
                "在地爐裡夾燒紅的石頭。獵戶腰帶是 Ara Toru，三人之路。整片天，就是一座小島的一天：挑芋頭、"
                "烤地爐、削獨木舟、出海撒網。",
             note="往東（左）滑過飛馬、白羊、昴宿到畢宿、獵戶腰帶；結束後疊 9:16 生活星空圖卡（可存圖）"),
        dict(code="05", kind="Z", sec=16, north=True,
             frames=[LIFE_E, MANU_F], layers=["鳥", "深空"], labels_start=ls("阿努塔名", "中譯"),
             labels=ls("Manu", "部位"),
             vo="但天上最大的，是一隻鳥：Manu。天狼星是牠的身體；老人星那片叫 Kapakau Tonga，東翼——"
                "tonga 也是他們東南信風的名字；南河三是北翼。一年到頭，幾乎每晚都看得到牠。",
             note="往東下方滑到 Manu（天狼＝身體、老人星＝東翼、南河三＝北翼）；迄格開 Manu＋部位"),
        dict(code="06", kind="Z", sec=24, north=True,
             frames=[MANU_F, WING], layers=["鳥", "芋", "深空"], labels_start=ls("Manu", "部位"),
             labels=ls("Manu", "星名"),
             overlay="C-A11-02_Manu的翅膀", overlay_layers=["星點層", "翅膀層", "傳說層"],
             vo="仔細看，兩片翅膀不一樣長：北翼二十六度，東翼三十六度。阿努塔的傳說，Manu 跟半神 Motikitiki"
                "——就是把阿努塔從海底拉上來的那位——為了女神 Taro 打了一架，北邊的翅膀被打斷，所以比較短。"
                "上週東加的野鴨，也有一片受傷的翅膀。",
             note="推近；結束後疊概念圖 Manu 的翅膀（星點層→翅膀層→傳說層）"),
        dict(code="07", kind="Z", sec=16, north=True,
             frames=[WING, TARO_F], layers=["芋", "鳥", "深空"], labels_start=ls("Manu", "星名"),
             labels=ls("芋頭", "星名"),
             vo="Taro 就是心宿二，紅紅的那顆；天蠍的頭這一片是一整株芋頭，心宿二是它的莖。"
                "十一月下旬的阿努塔，Taro 傍晚六點四十沉進西南的海；二十分鐘後，Manu 的翅膀才從東南升起。",
             note="長距離往東（左）滑到天蠍（x −145）；迄格開芋頭＋星名"),
        dict(code="08", kind="Z", sec=14, north=True,
             frames=[TARO_F, LEAD_F], layers=["鳥", "領", "深空"], labels_start=ls("芋頭", "星名"),
             labels=ls("領路"),
             vo="阿努塔人把領路的星叫 Taki：秋天的飛馬座那組叫 Taki Mua，前面的領路星。老人星旁邊有一顆小星，"
                "名字很長：Te Taki o te Kapakau Tonga，東翼的領路星。",
             note="滑回走廊（老人星、領路星）；領路星白圈＝α Pic"),
        dict(code="09", kind="T", sec=10, north=False,
             frames=[LEAD_F, SW_S], layers=["鳥", "領", "深空"], labels_start=ls("領路"), labels=[],
             vo="沿著鳥身往南飛，越過大小麥哲倫雲，就是南天極。阿努塔在南緯十一度半，南天極只比海面高十一度半。",
             note="沿走廊往南：天狼 → 老人星 → α Pic → 大麥哲倫雲 →（迄格＝10 起格：長圖轉南盤）"),
        dict(code="10", kind="R", sec=16, north=False,
             frames=[SW_S, E0, E1], layers=["鳥", "領", "深空"], labels_start=[],
             labels=[], labels_end=ls("領路-南盤"), horizon=[PHI_A],
             vo="十一月下旬、傍晚七點前：領路星先從東南的海面冒出頭；六分鐘後，東翼老人星才跟上。"
                "往北到赤道，順序就反過來——這個名字，是在這個緯度取的。",
             note=f"長圖轉南盤 → 南盤轉到 {ROT_E0:+.1f}°（18:45，兩顆都在海面下）→ {ROT_E1:+.1f}°（21:00，"
                  "兩顆都升到 14–17°，在山的剪影上方）；山升到阿努塔地平線（南緯 11.6°）；迄格開領路標籤"),
        dict(code="11", kind="R", sec=16, north=False,
             frames=[E1, CLOUD], layers=["深空"], labels_start=ls("領路-南盤"),
             labels=ls("雲-南盤", "星名-南盤"), horizon=[PHI_A],
             vo="南方天上這兩團光，阿努塔人叫 Te Ao Rere，奔跑的雲，和 Te Ao Toka，靜止的雲。"
                "上週東加說它們是兩團火：一團跑、一團躺著——rere 和 lele、兩邊的 toka，是同一個字。",
             note="同角度推近大小麥哲倫雲"),
        dict(code="12", kind="R", sec=20, north=False,
             frames=[CLOUD, NET_F], layers=["網", "深空"], labels_start=ls("雲-南盤", "星名-南盤"),
             labels=ls("網-南盤"), horizon=[PHI_A],
             vo="把時間往前轉。過了半夜，東南的海面升起一張網：南十字是網，南門二和馬腹一是網柄——"
                "Te Kupenga，漁網。這兩顆也有人叫 Te Rua Tangata，兩個人；上週在東加，他們也是「兩個人」，"
                "丟石頭砸傷了野鴨。",
             note=f"南盤順時針轉到 {ROT_DAWN:+.1f}°（＝11/21 04:00 阿努塔面向南方，天文晨光 03:49 剛過；"
                  "南十字 00:28 起升、此時高 23–24°，網柄南門二 02:51 才升起、此時高 7.5°）；旋轉中不放原生標籤；迄格開網標籤"),
        dict(code="13", kind="R", sec=15, north=False,
             frames=[NET_F, CROSS_F], layers=["網", "深空"], labels_start=ls("網-南盤"),
             labels=ls("十字-南盤"), horizon=[PHI_A],
             vo="一九一六年，聖公會的傳教士到了阿努塔，全島改信基督教。這張網後來改了名：Te Rakau Tapu，"
                "神聖的木頭——十字架。Stellarium 的中文版，還把漁網翻成「互聯網」。",
             note="同角度推近南十字；迄格開十字標籤"),
        dict(code="14", kind="Z", sec=22, north=True,
             frames=[LEAD_F, PATH_F], layers=["鳥", "深空"], labels_start=[], labels=ls("Manu"),
             overlay="C-A11-03_星路", overlay_layers=["海面層", "星路層"],
             vo="阿努塔人航海，靠一串星，叫 kaavenga——「載著船走的」。Tikopia 的酋長告訴人類學家 Firth："
                "往阿努塔的星路有九顆星，一顆貼著海面時對準船頭，升高了就換下一顆。"
                "反過來往 Tikopia，西南方快落下的那條魚 Te Paka Poi Ika Tapu，可能就是人馬座。",
             note="南盤轉長圖（歸位、換組、沿走廊上移回出發點）；結束後疊概念圖 星路（海面層→星路層）"),
        dict(code="15", kind="Z", sec=23, north=True,
             frames=[PATH_F, BUG_F], layers=["鳥", "深空"], labels_start=ls("Manu"),
             labels=ls("Manu", "布吉斯"),
             overlay="C-A11-05_同一個字",
             vo="難怪天上最大的是鳥：阿努塔人說，船就是鳥，船上的人是「海上的鳥」。更妙的是，往西五千六百公里，"
                "印尼蘇拉威西的布吉斯人，也把老人星、天狼星、南河三連成一隻 Manu'——雞。這個字，語言學家一路"
                "追回台灣：南島語的祖先說 manuk，北台灣的巴賽語也說 manuk。",
             note="推近 Manu；迄格開 Manu＋布吉斯；結束後疊 9:16 圖卡 同一個字"),
        dict(code="16", kind="R", sec=21, north=False,
             frames=[SW_S2, TPE_F], layers=["鳥", "深空"], labels_start=[],
             labels=ls("台灣-南盤"), horizon=[PHI_TPE],
             vo="今晚在台灣也看得到 Manu：九點多，天狼星和南河三從東方升起；十點四十五，老人星才貼著東南的海面"
                "出來。凌晨兩點朝正南看：天狼星高掛，東翼老人星只抬到十二度，要找南方沒有遮蔽的海邊；北翼南河三在更高的地方。",
             note=f"長圖轉南盤 → 南盤轉到 {ROT_TPE:+.1f}°（＝11/21 02:00 台北面向南方）；"
                  "山移到台北地平線（北緯 25.0°）——南天極在地平線下 25°"),
        dict(code="17", kind="R", sec=9, north=False,
             frames=[TPE_F, END_F], layers=["鳥", "深空"], labels_start=ls("台灣-南盤"),
             labels=ls("台灣-南盤"), horizon=[PHI_TPE],
             vo="下週五，同一條三人之路回到中國：獵戶的腰帶，是白虎的三顆星。",
             card="下集見｜白虎：參宿與西羌的冬夜",
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

    wing_n, wing_e = sep(S, SIRIUS, PROCYON), sep(S, SIRIUS, CANOPUS)
    print(f"\n  Manu 北翼（天狼–南河三）{wing_n:.2f}°、東翼（天狼–老人星）{wing_e:.2f}°")
    terms = {
        "Manu": dict(hips=MANU + [APIC], 原文="Manu", 拼音="", 英文翻譯="bird (Bird of Flight)",
                     中文="鳥（飛翔的鳥）", 顏色="amber",
                     來源備註="Feinberg 1988；Feinberg 1995：男性神靈，天狼＝身體、老人星＝東翼、南河三＝北翼；"
                          "北翼較短，是和 Motikitiki 爭 Taro（心宿二）時被打斷"),
        "Te Tino a Manu": dict(hips=[SIRIUS], 原文="Te Tino a Manu", 拼音="", 英文翻譯="the bird's body",
                               中文="鳥的身體（天狼星）", 顏色="amber", 來源備註="Feinberg 1988"),
        "Te Kapakau Tonga": dict(hips=[CANOPUS], 原文="Te Kapakau Tonga", 拼音="", 英文翻譯="the east wing",
                                 中文="東翼（老人星）", 顏色="amber",
                                 來源備註="Feinberg 1988 譯 east wing；tonga 在阿努塔也是東南信風（四月中到十月中）"),
        "Te Kapakau Pakatokerau": dict(hips=[PROCYON], 原文="Te Kapakau Pakatokerau", 拼音="",
                                       英文翻譯="the north wing", 中文="北翼（南河三）", 顏色="amber",
                                       來源備註="Feinberg 1988"),
        "Te Taki o te Kapakau Tonga": dict(hips=[APIC], 原文="Te Taki o te Kapakau Tonga", 拼音="",
                                           英文翻譯="the east wing's precursor", 中文="東翼的領路星（繪架座 α）",
                                           顏色="white",
                                           來源備註="Feinberg 1988；在 11.6°S 比老人星早約 6 分鐘升起（PyEphem 自算）"),
        "Te Aamonga": dict(hips=STICK, 原文="Te Aamonga", 拼音="", 英文翻譯="the carrying stick", 中文="扁擔（河鼓三星）",
                           顏色="green", 來源備註="Feinberg 1988：挑芋頭、椰子等食物；中國民間也稱河鼓三星為扁擔星"),
        "Te Angaanga": dict(hips=TONGS, 原文="Te Angaanga", 拼音="", 英文翻譯="the tongs", 中文="火鉗（畢宿）",
                            顏色="red", 來源備註="Feinberg 1988：在地爐裡夾熱石、炭和食物"),
        "Te Kope": dict(hips=BAMBOO, 原文="Te Kope", 拼音="", 英文翻譯="the bamboo", 中文="竹子（天鶴座）",
                        顏色="blue", 來源備註="Feinberg 1988：做釣竿、桅杆、帆桁、舷外浮桿支架"),
        "Toki": dict(hips=ADZE, 原文="Toki", 拼音="", 英文翻譯="adze", 中文="石錛（海豚座）", 顏色="blue",
                     來源備註="Feinberg 1988／Stellarium＝海豚座；另有資料作大角星"),
        "Kaavei": dict(hips=OCTO, 原文="Kaavei", 拼音="", 英文翻譯="octopus tentacle", 中文="章魚腳（白羊座）",
                       顏色="purple", 來源備註="Feinberg 1988"),
        "Te Paka Poi Ika Tapu": dict(hips=uniq([A["009"]]), 原文="Te Paka Poi Ika Tapu", 拼音="",
                                     英文翻譯="crevalle-like fish", 中文="像鰺魚的魚（人馬座，不確定）",
                                     顏色="purple", 來源備註="Feinberg 1988：往 Tikopia 星路上的星座之一；指認不確定"),
        "Ara Toru": dict(hips=BELT, 原文="Ara Toru", 拼音="", 英文翻譯="path of three", 中文="三人之路（獵戶腰帶）",
                         顏色="white", 來源備註="Feinberg 1988"),
        "Taki Mua": dict(hips=TAKIMUA, 原文="Taki Mua", 拼音="", 英文翻譯="forward precursor",
                         中文="前面的領路星（飛馬座）", 顏色="white", 來源備註="Feinberg 1988"),
        "Taro": dict(hips=TARO, 原文="Taro", 拼音="", 英文翻譯="taro plant", 中文="芋頭（天蠍座頭部）",
                     顏色="green", 來源備註="Feinberg 1988；Feinberg 1995：女性神靈 Taro＝心宿二"),
        "Na Kau": dict(hips=[ANTARES], 原文="Na Kau", 拼音="", 英文翻譯="its stem", 中文="它的莖（心宿二）",
                       顏色="green", 來源備註="Feinberg 1988"),
        "Te Kupenga": dict(hips=NET, 原文="Te Kupenga", 拼音="", 英文翻譯="the net", 中文="漁網（南十字＋南門二、馬腹一）",
                           顏色="blue", 來源備註="Feinberg 1988：基督教以前的名字；Stellarium zh_TW 誤譯「互聯網」"),
        "Te Kau o te Kupenga": dict(hips=[RIGIL, HADAR], 原文="Te Kau o te Kupenga", 拼音="",
                                    英文翻譯="the net's handle", 中文="網柄（南門二、馬腹一）", 顏色="blue",
                                    來源備註="Feinberg 1988"),
        "Te Rua Tangata": dict(hips=[RIGIL, HADAR], 原文="Te Rua Tangata", 拼音="", 英文翻譯="the double man",
                               中文="兩個人（南門二、馬腹一）", 顏色="red",
                               來源備註="Feinberg 1988；東加 Ongo Tangata（Collocott 1922）同一組星、同一個意思"),
        "Te Rakau Tapu": dict(hips=CRUX, 原文="Te Rakau Tapu", 拼音="", 英文翻譯="sacred wood / timber",
                              中文="神聖的木頭（南十字，1916 年改信基督教後）", 顏色="amber",
                              來源備註="Feinberg 1988"),
        "Matariki": dict(hips=[ALCYONE], 原文="Matariki", 拼音="", 英文翻譯="small face / small eyes",
                         中文="小臉（昴宿）", 顏色="amber", 來源備註="Feinberg 1988；東加 Mataliki、毛利 Matariki"),
        "Te Ao Rere": dict(hips=[], 原文="Te Ao Rere", 拼音="", 英文翻譯="the running cloud", 中文="奔跑的雲（大麥哲倫雲）",
                           顏色="white", 來源備註="Feinberg 1988"),
        "Te Ao Toka": dict(hips=[], 原文="Te Ao Toka", 拼音="", 英文翻譯="the restrained cloud（英譯不確定）",
                           中文="靜止的雲（小麥哲倫雲）", 顏色="white", 來源備註="Feinberg 1988"),
        "Manu'": dict(hips=MANU, 原文="Manu'", 拼音="", 英文翻譯="chicken", 中文="雞（布吉斯）", 顏色="white",
                      來源備註="Stellarium bugis（Ammarell 等）：老人星、天狼星、南河三"),
    }
    for items, name in label_sets:
        for it in items:
            if it["key"].startswith("HIP"):
                terms.setdefault(it["key"], dict(hips=[int(it["key"][4:])], 原文=it["text"], 拼音="",
                                                 英文翻譯="", 中文=it["text"], 顏色=it["color"],
                                                 來源備註="台灣通行星名"))
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Manu'", 中譯="雞（布吉斯：老人星、天狼星、南河三）", 英文="Chicken",
                              顏色="amber"),
                         dict(原文="Ongo Tangata", 中譯="兩個人（東加：南門二、馬腹一）", 英文="The two men",
                              顏色="red"),
                         dict(原文="Maʻafulele／Maʻafutoka", 中譯="跑動的火／躺著不動的火（東加：麥哲倫雲）",
                              英文="Running fire / lying fire", 顏色="white"),
                         dict(原文="扁擔星", 中譯="河鼓三星（台灣、中國民間）", 英文="Carrying pole",
                              顏色="green")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT,
               "rot": dict(E0=ROT_E0, E1=ROT_E1, DAWN=ROT_DAWN, TPE=ROT_TPE, TPE2=ROT_TPE2),
               "manu_wings_deg": dict(north=wing_n, east=wing_e)},
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
              labels=[dict(it, pt=5) for it in LIFE + MANU_L + TARO_L + LEAD_S + CLOUD_S + NET_S + TPE_S],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
