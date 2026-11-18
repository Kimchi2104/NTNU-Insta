# -*- coding: utf-8 -*-
"""X-05 南天的十字路口：真十字、假十字、鑽石十字｜大畫布 v4.6（全片在南盤圖層組）

論點：南天有一整串「看起來像十字的四顆星」，從船帆座一路排到南十字，只有南十字的長軸指向南天極。
真十字：小、十字裡有第五顆小星、有兩顆指針（南門二、馬腹一）和煤袋；延長四倍半 → 南天極旁 2.7°。
假十字：大、整體暗一點、沒有指針；照同法延長，離南天極 22°、28° → 南方偏東 24° 或偏西 42°。
鑽石十字：現代業餘天文圈的星群名，在台灣湊不齊（南船五、南船四在墾丁不升起）。
台灣：三月底九點假十字立在正南、南十字才剛升起；四月中九點半兩個並排（右假左真）；5/14 九點南十字直立正南。
逐字稿：04_腳本庫/X-05-南天的十字路口真十字假十字鑽石十字-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

【為什麼整集在南盤圖層組（不換組）】
  三個十字都在 dec −54.7…−70.0、RA 125–193；指針南門二／馬腹一 −60.4…−60.8。長圖帶要容下 −70，
  D_s 至少 72 → k 變大、R_fill ≤ 180 逼 D_fill ≥ 30，08、12 鏡的墾丁／台北南方地平線（南點 dec −68／−65，
  兩側升到 −40 以北）就落到盤外。南盤（極方位等距）上三個十字形狀不變形、能直接轉到墾丁的時刻。
  所以 01–14 全部在南盤圖層組，**整集不換組**；分鏡表的 Z／T 動作都在盤上做（改 cx/cy/fov）。

參數（依本集逐字稿重新評估，不照抄 A-31）
  lst = 188.0 → 墾丁 2027/5/14 21:00 的恆星時 187.85（南十字直立在正南方）。南盤 rot＝lst_obs − lst，
              所以 rot≈0 就是「今晚九點面向南方」；假十字上中天（墾丁 3/26 21:00，LST 139.55）＝rot −48.5；
              4/15 21:30 ＝ −21.2。全片旋轉都在 ±50° 以內（單段 < 170° ✓）。
  D_s = 50、D_r = 54 → 盤本體（r ≤ R_RIM）＝dec ≤ −54：三個十字全部 12 顆（最北 δ Vel −54.71）、
              指針、煤袋都在盤本體（逐點重合區）。D_r 不再往上提：天社的 γ Vel（−47.3）、曼達爾屋頂 δ Cen
              （−50.7）在填滿環也照畫（盤檔畫滿整圈），只是不在逐點重合區——本集不跟大畫布互切，不影響。
  D_fill = −20 → k＝R_RIM/36＝1.5916，R_fill＝175.07（盤寬 ÷ 畫布寬＝0.9726）；|x_t|+R_fill ≤ 180 ✓。
              南盤收到 dec +20：台北南點在盤心上方 kφ＝39.8、兩側地平線升到 dec −30 以北，
              08、12 鏡畫面角落離盤心 ≤ 110 ✓。
  x_tN = x_tS = 0。

自訂圖層（大畫布＋南北盤同步出；盤檔才是本集用的）
  指南線（白虛線）：十字架一→十字架二延長 4.5 倍；南門二—馬腹一中垂線；兩線交點的 3° 圈；南天極十字記號。
  假十字延長線（紅虛線）：δ Vel→ι Car、κ Vel→ε Car 各延長 4.5 倍（離南天極最近 22.1°、27.9°）。
  煤袋（白虛線橢圓，形狀同 A-31 頭）。
  墾丁永不升起圈（綠虛線）：dec −68.6（= −(90−21.95) − 折射 0.57）；圈內的星在墾丁永遠不升起。
  各文化連線（照 Stellarium 實際的星）：漁網（阿努塔，含網柄南門二、馬腹一）、歪房子（曼達爾，含 δ Cen 屋頂）、
  瘸腿的房子（布吉斯，含 μ Cru）、中國星官（十字架／天社／海石／南船）。

check_shots 的 ⚠（判斷後接受）
  全部 R「畫面含長圖側扇區／切點」：本集全程在南盤圖層組上，不跟大畫布互切，切點檢查不適用。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS, horizon_points

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-05"
OUT = os.path.join(BASE, "05_素材/X-05_南天十字/_v4大畫布")
LST0 = 188.0
TPE = (25.0330, 121.5654)
KT = (21.95, 120.80)
PHI_K, PHI_TPE = 21.95, 25.0330
NEVER_K = -(90.0 - PHI_K) - 0.57        # 墾丁永不升起圈（含折射）


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


LST_AT = {"墾丁 3/26 21:00": lst_at(*KT, 8, "2027/3/26 21:00"),
          "墾丁 4/15 21:30": lst_at(*KT, 8, "2027/4/15 21:30"),
          "台北 5/14 21:00": lst_at(*TPE, 8, "2027/5/14 21:00"),
          "墾丁 5/14 21:00": lst_at(*KT, 8, "2027/5/14 21:00")}
ROT_F = rot_s(LST_AT["墾丁 3/26 21:00"])       # 假十字上中天
ROT_A = rot_s(LST_AT["墾丁 4/15 21:30"])       # 兩個十字並排
ROT_T = rot_s(LST_AT["台北 5/14 21:00"])
ROT_K = rot_s(LST_AT["墾丁 5/14 21:00"])       # 今晚：南十字直立正南（≈0）
ROT_C = ROT_K


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_sc(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", []) if isinstance(l, list)]
        out[c["id"]] = [s for s in segs if len(set(s)) >= 2]
    return out


ACRUX, MIMOSA, GACRUX, IMAI, EPS_CRU, MU_CRU = 60718, 62434, 61084, 59747, 60260, 63003
CRUX = [GACRUX, ACRUX, MIMOSA, IMAI]
RIGIL, HADAR, DEL_CEN = 71683, 68702, 59196
DEL_VEL, KAP_VEL, EPS_CAR, IOT_CAR = 42913, 45941, 41037, 45556
FCR = [DEL_VEL, KAP_VEL, EPS_CAR, IOT_CAR]
BET_CAR, THE_CAR, UPS_CAR, OME_CAR = 45238, 52419, 48002, 50099
DCR = [BET_CAR, THE_CAR, UPS_CAR, OME_CAR]
COALSACK = (192.9, -62.8)
POLE = (0.0, -90.0)

SEG_CRUX = [[GACRUX, ACRUX], [MIMOSA, IMAI]]
SEG_FCR = [[DEL_VEL, IOT_CAR], [KAP_VEL, EPS_CAR]]           # Stellarium modern FCr（＝東加 Toloalahi）
SEG_DCR = [[BET_CAR, THE_CAR], [UPS_CAR, OME_CAR]]           # Stellarium modern DCr
AN = load_sc("anutan"); MD = load_sc("mandar"); BG_ = load_sc("bugis"); CN = load_sc("chinese")
SEG_NET = AN["CON anutan 011"]          # Te Kupenga 漁網（南門二、馬腹一＝網柄）
SEG_SAPO = MD["CON mandar 001"]         # Bittoéng Sapo Kepang 歪房子（δ Cen 屋頂）
SEG_BOLA = BG_["CON bugis 001"]         # Bintoéng Bola Képpang 瘸腿的房子（μ Cru）
SEG_SZJ = CN["CON chinese 187"]         # 十字架
SEG_TS = CN["CON chinese 244"]          # 天社
SEG_HS = CN["CON chinese 091"]          # 海石
SEG_NC = CN["CON chinese 148"]          # 南船
assert set(sum(SEG_SAPO, [])) >= {DEL_CEN} and set(sum(SEG_BOLA, [])) >= {MU_CRU}
assert set(sum(SEG_NET, [])) >= {RIGIL, HADAR}
MAINS = sorted(set(CRUX + FCR + DCR + [RIGIL, HADAR]))


# ══════════════════════════════════════════════════════════════════
# 二、球面幾何（指南線、延長線）
# ══════════════════════════════════════════════════════════════════
def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(max(-1, min(1, z))))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(v):
    n = math.sqrt(sum(c * c for c in v)); return tuple(c / n for c in v)


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def sep(p, q):
    return math.degrees(math.acos(max(-1, min(1, dot(vec(*p), vec(*q))))))


def gc_arc(p, q, t0, t1, step=0.5):
    """從 p 經 q 的大圓，取 p 起算 t0…t1 倍 |pq| 的弧（(ra,dec) 點列）"""
    a, b = vec(*p), vec(*q)
    n = unit(cross(a, b)); u = unit(cross(n, a))
    d = math.radians(sep(p, q))
    out = []
    k = max(2, int(abs(t1 - t0) * math.degrees(d) / step))
    for i in range(k + 1):
        s = (t0 + (t1 - t0) * i / k) * d
        out.append(radec(tuple(math.cos(s) * a[j] + math.sin(s) * u[j] for j in range(3))))
    return out


def gc_min_pole(p, q):
    """大圓 pq 離南天極最近的角距"""
    n = unit(cross(vec(*p), vec(*q)))
    return 90.0 - math.degrees(math.acos(abs(n[2])))


def bisector(p, q, s0, s1, step=0.5):
    """pq 的中垂線（大圓），從中點往南天極方向 s0…s1 度"""
    a, b = vec(*p), vec(*q)
    M = unit(tuple(x + y for x, y in zip(a, b)))
    n = unit(cross(a, b))
    if n[2] > 0:
        n = tuple(-c for c in n)
    out = []
    k = max(2, int((s1 - s0) / step))
    for i in range(k + 1):
        s = math.radians(s0 + (s1 - s0) * i / k)
        out.append(radec(tuple(math.cos(s) * M[j] + math.sin(s) * n[j] for j in range(3))))
    return out, M, n


def small_circle(c, r, n=120):
    a = vec(*c)
    e = unit(cross(a, (0, 0, 1)) if abs(a[2]) < 0.99 else cross(a, (1, 0, 0)))
    f = cross(a, e)
    rr = math.radians(r)
    return [radec(tuple(math.cos(rr) * a[j] + math.sin(rr) * (math.cos(t) * e[j] + math.sin(t) * f[j])
                        for j in range(3))) for t in [2 * math.pi * i / n for i in range(n + 1)]]


def ellipse(ra0, dec0, a, b, n=72, tilt=0.0):
    t = math.radians(tilt)
    out = []
    for i in range(n + 1):
        u = 2 * math.pi * i / n
        x, y = a * math.cos(u), b * math.sin(u)
        xx, yy = x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)
        dec = dec0 + yy
        out.append(((ra0 + xx / max(0.05, math.cos(math.radians(dec)))) % 360, dec))
    return out


def geometry(S):
    P = lambda h: tuple(S[h][:2])
    g = {}
    g["crux_ext"] = gc_arc(P(GACRUX), P(ACRUX), 0.0, 5.5)        # 過十字架二再延長 4.5 倍（逐字稿 4.45 倍）
    g["crux_min"] = gc_min_pole(P(GACRUX), P(ACRUX))
    bis, M, nb = bisector(P(RIGIL), P(HADAR), -2.0, 33.0)
    g["bis"] = bis
    g["bis_min"] = gc_min_pole(radec(M), radec(nb))
    n1 = unit(cross(vec(*P(GACRUX)), vec(*P(ACRUX))))
    n2 = unit(cross(M, nb))
    X = unit(cross(n1, n2))
    if X[2] > 0:
        X = tuple(-c for c in X)
    g["X"] = radec(X)
    g["X_pole"] = sep(g["X"], POLE)
    g["X_circle"] = small_circle(g["X"], 3.0)
    g["f1"] = gc_arc(P(DEL_VEL), P(IOT_CAR), 0.0, 5.5)
    g["f2"] = gc_arc(P(KAP_VEL), P(EPS_CAR), 0.0, 5.5)
    for k, (a, b) in (("f1", (DEL_VEL, IOT_CAR)), ("f2", (KAP_VEL, EPS_CAR))):
        n = unit(cross(vec(*P(a)), vec(*P(b))))
        z = (0.0, 0.0, -1.0)
        foot = unit(tuple(z[j] - dot(z, n) * n[j] for j in range(3)))
        g[k + "_foot"] = radec(foot)
        g[k + "_gap"] = gc_arc(POLE, radec(foot), 0.0, 1.0)       # 南天極 → 延長線最近點（虛線）
    g["f1_min"] = gc_min_pole(P(DEL_VEL), P(IOT_CAR))
    g["f2_min"] = gc_min_pole(P(KAP_VEL), P(EPS_CAR))
    g["f1_end"], g["f2_end"] = g["f1"][-1], g["f2"][-1]
    g["coal"] = ellipse(*COALSACK, 3.4, 2.5, tilt=-12.0)
    g["never"] = [(ra, NEVER_K) for ra in [i * 2.0 for i in range(181)]]
    g["pole_x"] = [[(0.0, -88.8), (180.0, -88.8)], [(90.0, -88.8), (270.0, -88.8)]]
    return g


# ══════════════════════════════════════════════════════════════════
# 三、連線
# ══════════════════════════════════════════════════════════════════
LG_ALL = [(SEG_CRUX, "amber", 1.0), (SEG_FCR, "red", 1.0), (SEG_DCR, "blue", 1.0)]
LG_CRUX = [(SEG_CRUX, "amber", 1.0)]
LG_NET = [(SEG_NET, "green", 1.0)]
LG_SAPO = [(SEG_SAPO, "blue", 1.0)]
LG_BOLA = [(SEG_BOLA, "purple", 1.0)]
LG_CN = [(SEG_SZJ, "amber", 1.0), (SEG_TS, "red", 1.0), (SEG_HS, "green", 1.0), (SEG_NC, "blue", 1.0)]
LINE_SETS = [(LG_CRUX, "連線-南十字"), (LG_NET, "連線-漁網"), (LG_SAPO, "連線-歪房子"),
             (LG_BOLA, "連線-瘸腿的房子"), (LG_CN, "連線-中國星官")]
MARKS = [(MAINS, "主角星白點", "dot"), ([EPS_CRU], "第五顆星圈", "ring")]
LINES_KEY = {"L4": "星座連線", "十": "連線-南十字", "網": "連線-漁網", "歪": "連線-歪房子", "瘸": "連線-瘸腿的房子",
             "中": "連線-中國星官", "圈": "第五顆星圈", "指": "指南線", "延": "假十字延長線", "煤": "煤袋",
             "墾": "墾丁永不升起圈"}
LINE_GROUPS = {"L4": LG_ALL, "十": LG_CRUX, "網": LG_NET, "歪": LG_SAPO, "瘸": LG_BOLA, "中": LG_CN,
               "圈": [], "指": [], "延": [], "煤": [], "墾": []}


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, g):
    W = COLORS["white"]

    def guide(s, pos, runs, disc):
        s.polylines(runs(g["crux_ext"]), stroke=W, w=m.lw * 0.45, opacity=0.9, dash="1.2 0.8")
        s.polylines(runs(g["bis"]), stroke=W, w=m.lw * 0.45, opacity=0.9, dash="1.2 0.8")
        s.polylines(runs(g["X_circle"]), stroke=W, w=m.lw * 0.40, opacity=0.85)
        for arm in g["pole_x"]:
            s.polylines(runs(arm), stroke=W, w=m.lw * 0.55, opacity=0.95)

    def fext(s, pos, runs, disc):
        for k in ("f1", "f2"):
            s.polylines(runs(g[k]), stroke=COLORS["red"], w=m.lw * 0.45, opacity=0.9, dash="1.2 0.8")
            s.polylines(runs(g[k + "_gap"]), stroke=W, w=m.lw * 0.30, opacity=0.6, dash="0.5 0.6")
        for arm in g["pole_x"]:
            s.polylines(runs(arm), stroke=W, w=m.lw * 0.55, opacity=0.95)

    def coal(s, pos, runs, disc):
        s.polylines(runs(g["coal"]), stroke=W, w=m.lw * 0.40, opacity=0.8, dash="0.8 0.6")

    def never(s, pos, runs, disc):
        s.polylines(runs(g["never"]), stroke=COLORS["green"], w=m.lw * 0.45, opacity=0.9, dash="1.2 0.8")

    return [("指南線", guide), ("假十字延長線", fext), ("煤袋", coal), ("墾丁永不升起圈", never)]


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
# 五、旁白字數（中文字＋外文音節；Stellarium 照配音提示唸 4 音節）
# ══════════════════════════════════════════════════════════════════
SYL = {"stellarium": 4}


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
        else:
            n += max(1, len(re.findall(r"[aeiouyáéíóúāēīōū]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 六、名詞總表（錨點, 原文, Stellarium 寫法, 英文, 中文, 顏色, 來源）
# ══════════════════════════════════════════════════════════════════
TERMS = [
    (CRUX, "南十字", "Crux", "Southern Cross (Crux)", "南十字", "amber", "IAU"),
    (FCR, "假十字", "False Cross", "False Cross", "假十字", "red", "Stellarium modern（AST modern FCr）"),
    (DCR, "鑽石十字", "Diamond Cross", "Diamond Cross", "鑽石十字", "blue",
     "Stellarium modern（AST modern DCr）；現代業餘天文圈的星群名"),
    ([GACRUX], "十字架一", "Cross I", "γ Cru (Gacrux)", "十字架一", "amber", "Stellarium chinese"),
    ([ACRUX], "十字架二", "Cross II", "α Cru (Acrux)", "十字架二", "amber", "Stellarium chinese"),
    ([MIMOSA], "十字架三", "Cross III", "β Cru (Mimosa)", "十字架三", "amber", "Stellarium chinese"),
    ([IMAI], "十字架四", "Cross IV", "δ Cru", "十字架四", "amber", "Stellarium chinese"),
    ([EPS_CRU], "第五顆星", "—", "ε Cru", "第五顆星（ε Cru，3.6 等）", "white", "—"),
    ([COALSACK], "煤袋", "—", "Coalsack", "煤袋", "white", "暗星雲（A-31 鴯鶓的頭）"),
    ([RIGIL], "南門二", "Southern Gate II", "α Cen", "南門二", "white", "Stellarium chinese"),
    ([HADAR], "馬腹一", "Horse's Abdomen I", "β Cen", "馬腹一", "white", "Stellarium chinese"),
    ([RIGIL, HADAR], "指針", "—", "the Pointers", "指針", "white", "—"),
    ([POLE], "南天極", "—", "South Celestial Pole", "南天極", "white", "—"),
    ([DEL_VEL], "天社三", "Celestial Earth God's Temple III", "δ Vel", "天社三", "red", "Stellarium chinese"),
    ([KAP_VEL], "天社五", "Celestial Earth God's Temple V", "κ Vel", "天社五", "red", "Stellarium chinese"),
    ([EPS_CAR], "海石一", "Sea Rock I", "ε Car (Avior)", "海石一", "red", "Stellarium chinese"),
    ([IOT_CAR], "海石二", "Sea Rock II", "ι Car (Aspidiske)", "海石二", "red", "Stellarium chinese"),
    ([BET_CAR], "南船五", "Southern Boat V", "β Car (Miaplacidus)", "南船五", "blue", "Stellarium chinese；IAU 星名"),
    ([THE_CAR], "南船三", "Southern Boat III", "θ Car", "南船三", "blue", "Stellarium chinese"),
    ([UPS_CAR], "海石五", "Sea Rock V", "υ Car", "海石五", "blue", "Stellarium chinese"),
    ([OME_CAR], "南船四", "Southern Boat IV", "ω Car", "南船四", "blue", "Stellarium chinese"),
    (CRUX, "Toloa", "Toloatonga", "wild duck (Tonga)", "野鴨（東加）", "amber",
     "Collocott 1922（Toloa）；Stellarium tongan 作 Toloatonga「南方的野鴨」"),
    (CRUX, "Hānaiakamalama", "Hanaiakamalama", "cared for by the Moon (Hawaiʻi)", "月亮照看的孩子（夏威夷）",
     "amber", "PVS；Stellarium hawaiian_starlines"),
    (CRUX + [RIGIL, HADAR], "Te Kupenga", "Te Kupenga", "the Net (Anuta)", "漁網（阿努塔）", "green",
     "Feinberg 1988；Stellarium anutan 011（含網柄南門二、馬腹一）"),
    (CRUX + [DEL_CEN], "Sapo Kepang", "Bittoéng Sapo Kepang", "Slanted House (Mandar)", "歪房子（曼達爾）", "blue",
     "Rasyid, Hidayat & Orchiston 2021；Stellarium mandar 001（含 δ Cen 屋頂）"),
    (CRUX + [MU_CRU], "Bola Képpang", "Bintoѐng Bola Kѐppang", "Lame / Incomplete House (Bugis)",
     "瘸腿的房子（布吉斯）", "purple",
     "Ôhashi & Orchiston 2021 p. 706（引 Ammarell 1999、Pelras 1987）；Stellarium bugis 001（含 μ Cru；"
     "Stellarium 用西里爾字母 ѐ，本片照 A-26 寫 é）"),
    (CRUX, "十字架", "Shízìjià", "Cross", "十字架", "amber", "明末近南極 23 星官；Stellarium chinese 187"),
    ([DEL_VEL, KAP_VEL], "天社", "Tiānshè", "Celestial Earth God's Temple", "天社", "red",
     "Stellarium chinese 244（今天的星表）；陳卓體系的天社不含 δ、κ Vel"),
    ([EPS_CAR, IOT_CAR, UPS_CAR], "海石", "Hǎishí", "Sea Rock", "海石", "green", "明末；Stellarium chinese 091"),
    ([BET_CAR, THE_CAR, OME_CAR], "南船", "Nánchuán", "Southern Boat", "南船", "blue",
     "明末；Stellarium chinese 148"),
    (CRUX, "Toloatonga", "Toloatonga", "Southern Wild Duck (Tonga)", "南方的野鴨", "amber",
     "Stellarium tongan 001（Dan Smale；據 Velt 1990、Fale 1990）"),
    (FCR, "Toloalahi", "Toloalahi", "Big Wild Duck (Tonga)", "大野鴨", "red",
     "Stellarium tongan 005（據 Velt 1990、Fale 1990；Collocott 1922 沒有這一條）"),
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


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=50, D_r=54, D_fill=-20.0,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole
    g = geometry(S)
    print(f"\n── 幾何核對（逐字稿：長軸延長最近 2.68°、中垂線 2.94°、交點 2.95°、假十字 22.1°／27.9°）──\n"
          f"  南十字長軸大圓離南天極 {g['crux_min']:.2f}°；中垂線 {g['bis_min']:.2f}°；交點 {g['X_pole']:.2f}°"
          f"（{g['X'][0]:.1f}, {g['X'][1]:.2f}）\n  假十字 δVel–ιCar {g['f1_min']:.2f}°、κVel–εCar {g['f2_min']:.2f}°")
    for nm, a, b in (("長軸", GACRUX, ACRUX), ("δVel–ιCar", DEL_VEL, IOT_CAR), ("κVel–εCar", KAP_VEL, EPS_CAR),
                     ("β–θCar", BET_CAR, THE_CAR), ("υ–ωCar", UPS_CAR, OME_CAR), ("十字架二–海石一", ACRUX, EPS_CAR)):
        print(f"  {nm} {sep(S[a][:2], S[b][:2]):.2f}°")
    end1 = sep(S[GACRUX][:2], g["crux_ext"][-1])
    print(f"  延長 4.5 倍的端點離南天極 {sep(g['crux_ext'][-1], POLE):.2f}°（弧長 {end1:.2f}°）")

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]} if isinstance(a[0], int) else {"ra": a[0][0], "dec": a[0][1]}
        vs = [vec(*h) if isinstance(h, tuple) else vec(*S[h][:2]) for h in a]
        ra, dec = radec([sum(v[i] for v in vs) for i in range(3)])
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key,
                    disc=True)

    T = {t[1]: t for t in TERMS}

    def term(name, dx=0.0, dy=0.0, s1=1.6, s2=1.2, gap=2.4, zh_only=False, a=None, zh=None, col=None,
             orig=None, key=None):
        a0, orig0, _, _, zh0, col0, _ = T[name]
        a = a if a is not None else a0
        zh = zh or zh0
        col = col or col0
        orig = orig or orig0
        key = key or name
        if zh_only:
            return [item(a, zh, col, s1, dx, dy, key)]
        return [item(a, orig, col, s1, dx, dy + gap / 2, key),
                item(a, zh, "white", s2, dx, dy - gap / 2, key + "-zh")]

    sz = lambda f: dict(s1=round(f * 0.030, 2), s2=round(f * 0.024, 2), gap=round(f * 0.046, 2))
    zs = lambda f, k=0.042: round(f * k / 1.7, 2)          # → Canva 原生字 ≈ k×1080 px（font_u＝1.7）

    # ════════════════════ 構圖 ════════════════════
    def far(cx, cy, f):
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 + yp) for sx in (-1, 1) for sy in (-1, 1))

    def fit(pts, rot, pad=0.10, minfov=24.0, dy=0.0, dx=0.0, fov=None):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while far(cx, cy, f) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def P(obj, rot):
        return disc_xy(m, *(S[obj][:2] if isinstance(obj, int) else obj), rot)

    dpts = lambda objs, rot: [P(h, rot) for h in objs]

    def hz_pts(phi, L, rot, az0, az1):
        pts = horizon_points(phi, L, n=721)
        return [disc_xy(m, ra, dec, rot) for ra, dec in pts[int(az0 * 2):int(az1 * 2) + 1] if dec < -m.Dfill]

    def on_hz(phi, L, rot, frac, fov, x=0.0):
        """地平線南點落在畫面下緣往上 frac 處（地平線在盤上是弧，取南點）"""
        hy = sum(p[1] for p in hz_pts(phi, L, rot, 178, 182)) / 9
        return (round(x, 2), round(hy + fov * 8 / 9 - frac * fov * 16 / 9, 2), fov, rot)

    ALL = fit(dpts(CRUX + FCR + DCR, ROT_C), ROT_C, pad=0.10)
    WIDE = fit([(ALL[0], ALL[1])], ROT_C, fov=round(ALL[2] * 1.30, 1))
    CRUXF = fit(dpts(CRUX + [EPS_CRU, MU_CRU] + g["coal"][::6], ROT_C), ROT_C, pad=0.14)
    POINT = fit(dpts(CRUX + [RIGIL, HADAR, POLE, g["X"]] + g["X_circle"][::10], ROT_C), ROT_C, pad=0.16)
    cc = [sum(p[i] for p in dpts(CRUX, ROT_C)) / 4 for i in (0, 1)]; fN = 56.0
    NAMES = (round(cc[0] - 0.02 * fN, 2), round(cc[1] + 0.25 * fN, 2), fN, ROT_C)   # 南十字在下方、上方留給名字疊
    FALSEF = fit(dpts(FCR + [45080], ROT_F), ROT_F, pad=0.22)
    FALSEX = fit(dpts(FCR + [POLE, g["f1_foot"], g["f2_foot"]], ROT_F), ROT_F, pad=0.16)
    ROT_D = round(ROT_C - 38.0, 2)                 # 鑽石十字轉到盤心正上方
    DIAF = fit(dpts(DCR, ROT_D) + dpts(g["never"][::6], ROT_D), ROT_D, pad=0.05)
    ALL9 = fit(dpts(CRUX + FCR + DCR + [39953, 46701, 50371, 51576, 47854], ROT_C), ROT_C, pad=0.06)
    ALL9W = (ALL9[0], ALL9[1], round(ALL9[2] * 1.12, 1), ROT_C)
    T10 = fit(dpts(CRUX + FCR, ROT_C), ROT_C, pad=0.14)
    # 08 墾丁面南：3/26 假十字立在正南；4/15 兩個十字並排（畫面不動、只轉盤）
    LF, LA = LST_AT["墾丁 3/26 21:00"], LST_AT["墾丁 4/15 21:30"]
    span = [p[0] for p in dpts(CRUX + FCR, ROT_A)] + [p[0] for p in dpts(CRUX + FCR, ROT_F)]
    F08 = round(max(abs(min(span)), abs(max(span))) * 2 * 1.22, 1)
    K1 = on_hz(PHI_K, LF, ROT_F, 0.34, F08)
    K2 = (K1[0], K1[1], K1[2], ROT_A)
    # 12 台北→墾丁 5/14 21:00：南十字直立正南＋左下指針
    span = [p[0] for p in dpts(CRUX + [RIGIL, HADAR], ROT_T)]
    F12 = round(max(abs(min(span)), abs(max(span))) * 2 * 1.35, 1)
    T1 = on_hz(PHI_TPE, LST_AT["台北 5/14 21:00"], ROT_T, 0.36, F12)
    K3 = (T1[0], T1[1], T1[2], ROT_K)
    K3b = (K3[0], round(K3[1] + 0.03 * K3[2], 2), round(K3[2] * 0.94, 1), ROT_K)   # 13 鏡微推近（自己的頁）
    NEXT = ALL
    print(f"\n── 構圖 ── ROT_F {ROT_F:+.2f}°、ROT_A {ROT_A:+.2f}°、ROT_T {ROT_T:+.2f}°、ROT_K {ROT_K:+.2f}°\n"
          f"  全部 {ALL}／{WIDE}\n  南十字 {CRUXF}\n  指南 {POINT}\n  假十字 {FALSEF}→{FALSEX}\n"
          f"  鑽石 {DIAF}\n  中國 {ALL9}\n  墾丁春 {K1}→{K2}\n  今晚 {T1}→{K3}")

    def scr(frame, obj):
        cx, cy, fov, rot = frame
        x, y = P(obj, rot)
        return round((x - cx) / fov, 3), round((y - cy) / fov, 3)

    # ════════════════════ 標籤（盤＝畫面方向，+dx 右、+dy 上；單位＝盤座標） ════════════════════
    def shift(items, key, dx, dy):
        for it in items:
            if it["key"].split("-zh")[0] == key:
                it["dx"] = round(it["dx"] + dx, 2); it["dy"] = round(it["dy"] + dy, 2)

    # 字級：Canva 原生字 36–96 px；size/fov×1080 ≈ px → k＝px/1080（0.040≈43px、0.050≈54px、0.060≈65px）
    F01 = ALL[2]
    LB_ALL = (term("南十字", zh_only=True, s1=zs(F01, 0.055))
              + term("假十字", zh_only=True, s1=zs(F01, 0.055))
              + term("鑽石十字", zh_only=True, s1=zs(F01, 0.055)))
    f02 = CRUXF[2]
    LB_CRUX = (term("十字架一", zh_only=True, s1=zs(f02, 0.045)) + term("十字架二", zh_only=True, s1=zs(f02, 0.045))
               + term("十字架三", zh_only=True, s1=zs(f02, 0.045)) + term("十字架四", zh_only=True, s1=zs(f02, 0.045))
               + term("第五顆星", zh_only=True, s1=zs(f02, 0.040), zh="第五顆星")
               + term("煤袋", zh_only=True, s1=zs(f02, 0.050)))
    f03 = POINT[2]
    LB_POINT = (term("南天極", zh_only=True, s1=zs(f03, 0.045))
                + [item([g["X"]], "差不到 3°", "white", zs(f03, 0.042), 0.0, 0.0, "差")]
                + term("指針", zh_only=True, s1=zs(f03, 0.050))
                + term("南門二", zh_only=True, s1=zs(f03, 0.040)) + term("馬腹一", zh_only=True, s1=zs(f03, 0.040))
                + [item([g["crux_ext"][len(g["crux_ext"]) * 2 // 3]], "延長 4.5 倍", "white", zs(f03, 0.042),
                        0.0, 0.0, "延")])
    fN = NAMES[2]
    NM = ("Toloa", "Hānaiakamalama", "Te Kupenga", "Sapo Kepang", "Bola Képpang")
    LB_NAMES = []
    for nm in NM:
        LB_NAMES += term(nm, a=CRUX, key=nm, s1=zs(fN, 0.045), s2=zs(fN, 0.036), gap=zs(fN, 0.072))
    f05 = FALSEF[2]
    LB_FALSE = (term("天社三", zh_only=True, s1=zs(f05, 0.045)) + term("天社五", zh_only=True, s1=zs(f05, 0.045))
                + term("海石一", zh_only=True, s1=zs(f05, 0.045)) + term("海石二", zh_only=True, s1=zs(f05, 0.045))
                + term("假十字", zh_only=True, s1=zs(f05, 0.060)))
    f06 = FALSEX[2]
    LB_FEXT = (term("南天極", zh_only=True, s1=zs(f06, 0.042))
               + [item([g["f1_foot"]], f"差 {g['f1_min']:.0f}°", "red", zs(f06, 0.045), 0, 0, "f1"),
                  item([g["f2_foot"]], f"差 {g['f2_min']:.0f}°", "red", zs(f06, 0.045), 0, 0, "f2")]
               + term("假十字", zh_only=True, s1=zs(f06, 0.050)))
    f07 = DIAF[2]
    LB_DIA = (term("南船五", orig="Miaplacidus", zh="南船五", s1=zs(f07, 0.040), s2=zs(f07, 0.036), gap=zs(f07, 0.045))
              + term("南船四", zh_only=True, s1=zs(f07, 0.038))
              + [item([POLE], "圈內：墾丁永遠看不到", "green", zs(f07, 0.042), 0, 0, "never")]
              + term("鑽石十字", zh_only=True, s1=zs(f07, 0.050)))
    f08 = K1[2]
    LB_K1 = (term("假十字", zh="假十字（正南）", zh_only=True, s1=zs(f08, 0.048), key="假")
             + term("南十字", zh="南十字（剛升起）", zh_only=True, s1=zs(f08, 0.042), key="真"))
    LB_K2 = (term("假十字", zh="右：假十字", zh_only=True, s1=zs(f08, 0.048), key="假")
             + term("南十字", zh="左：南十字", zh_only=True, s1=zs(f08, 0.048), key="真"))
    f09 = ALL9[2]
    LB_CN = (term("十字架", zh_only=True, s1=zs(f09, 0.050)) + term("天社", zh_only=True, s1=zs(f09, 0.050))
             + term("海石", zh_only=True, s1=zs(f09, 0.050)) + term("南船", zh_only=True, s1=zs(f09, 0.050)))
    f10 = T10[2]
    LB_TONGA = (term("Toloatonga", s1=zs(f10, 0.050), s2=zs(f10, 0.042), gap=zs(f10, 0.055))
                + term("Toloalahi", s1=zs(f10, 0.050), s2=zs(f10, 0.042), gap=zs(f10, 0.055))
                + [item([GACRUX], "Stellarium 版（據 1990 年資料）", "white", zs(f10, 0.036), 0, 0, "註1"),
                   item([GACRUX], "Collocott 1922 只有 Toloa＝南十字", "white", zs(f10, 0.036), 0, 0, "註2")])
    f12 = T1[2]
    LB_TPE = ([item([GACRUX], "十字架一 7.8°", "amber", zs(f12, 0.042), 0, 0, "γ"),
               item([ACRUX], "十字架二 2.0°", "amber", zs(f12, 0.042), 0, 0, "α")]
              + term("南門二", zh_only=True, s1=zs(f12, 0.038)) + term("馬腹一", zh_only=True, s1=zs(f12, 0.038))
              + [item([GACRUX], "台北・今晚 21:00", "white", zs(f12, 0.050), 0, 0, "地")])
    LB_KT = ([item([GACRUX], "十字架一 10.9°", "amber", zs(f12, 0.042), 0, 0, "γ"),
              item([ACRUX], "十字架二 5.0°", "amber", zs(f12, 0.042), 0, 0, "α")]
             + term("南門二", zh_only=True, s1=zs(f12, 0.038)) + term("馬腹一", zh_only=True, s1=zs(f12, 0.038))
             + [item([GACRUX], "墾丁、蘭嶼・今晚 21:00", "white", zs(f12, 0.050), 0, 0, "地")])
    LB_MOON = [item([GACRUX], "月光從右上方來", "white", zs(f12, 0.045), 0, 0, "月"),
               item([GACRUX], "（西南方、高 57°）", "white", zs(f12, 0.038), 0, 0, "月2")]

    label_sets = [(LB_ALL, "三個十字"), (LB_CRUX, "南十字"), (LB_POINT, "指南"), (LB_NAMES, "南十字的名字"),
                  (LB_FALSE, "假十字"), (LB_FEXT, "假十字延長"), (LB_DIA, "鑽石十字"), (LB_K1, "墾丁3月底"),
                  (LB_K2, "墾丁4月中"), (LB_CN, "中國星官"), (LB_TONGA, "東加兩隻野鴨"), (LB_TPE, "今晚台北"),
                  (LB_KT, "今晚墾丁"), (LB_MOON, "月光")]

    # 錨點螢幕位置（frame 內相對座標：x∈±0.5、y∈±0.89）→ 依此放 dx/dy
    if "--where" in sys.argv:
        for nm, fr, objs in (("ALL", ALL, CRUX[:1] + FCR[:1] + DCR[:1]), ("CRUXF", CRUXF, CRUX + [EPS_CRU, COALSACK]),
                             ("POINT", POINT, CRUX + [RIGIL, HADAR, POLE, g["X"]]), ("NAMES", NAMES, CRUX + [RIGIL]),
                             ("FALSEF", FALSEF, FCR), ("FALSEX", FALSEX, FCR + [POLE, g["f1_foot"], g["f2_foot"]]),
                             ("DIAF", DIAF, DCR + [POLE]), ("ALL9", ALL9, CRUX + FCR + DCR),
                             ("T10", T10, CRUX + FCR),
                             ("K1", K1, CRUX + FCR), ("K2", K2, CRUX + FCR), ("T1", T1, CRUX + [RIGIL, HADAR]),
                             ("K3", K3, CRUX + [RIGIL, HADAR])):
            print(nm, [(o if isinstance(o, int) else tuple(round(c, 1) for c in o), scr(fr, o)) for o in objs])

    u = lambda fr, k: round(fr[2] * k, 2)           # 畫面寬的 k 倍（盤座標）
    shift(LB_ALL, "南十字", u(ALL, 0.02), u(ALL, 0.10)); shift(LB_ALL, "假十字", 0, u(ALL, 0.15))
    shift(LB_ALL, "鑽石十字", -u(ALL, 0.17), -u(ALL, 0.02))
    shift(LB_CRUX, "十字架一", 0, u(CRUXF, 0.06)); shift(LB_CRUX, "十字架二", 0, -u(CRUXF, 0.06))
    shift(LB_CRUX, "十字架三", -u(CRUXF, 0.15), 0); shift(LB_CRUX, "十字架四", u(CRUXF, 0.15), 0)
    shift(LB_CRUX, "第五顆星", u(CRUXF, 0.12), -u(CRUXF, 0.06)); shift(LB_CRUX, "煤袋", 0, 0)
    shift(LB_POINT, "南天極", u(POINT, 0.0), -u(POINT, 0.06)); shift(LB_POINT, "差", -u(POINT, 0.0), u(POINT, 0.13))
    shift(LB_POINT, "指針", u(POINT, 0.02), u(POINT, 0.10)); shift(LB_POINT, "南門二", 0, -u(POINT, 0.05))
    shift(LB_POINT, "馬腹一", 0, -u(POINT, 0.05)); shift(LB_POINT, "延", -u(POINT, 0.13), 0)
    for i, nm in enumerate(NM):
        shift(LB_NAMES, nm, u(NAMES, 0.0), u(NAMES, 0.87) - i * u(NAMES, 0.13))
    shift(LB_FALSE, "天社三", 0, u(FALSEF, 0.06)); shift(LB_FALSE, "天社五", 0, u(FALSEF, 0.06))
    shift(LB_FALSE, "海石一", 0, -u(FALSEF, 0.06)); shift(LB_FALSE, "海石二", 0, -u(FALSEF, 0.06))
    shift(LB_FALSE, "假十字", 0, u(FALSEF, 0.36))
    shift(LB_FEXT, "南天極", 0, -u(FALSEX, 0.05)); shift(LB_FEXT, "f1", u(FALSEX, 0.10), u(FALSEX, 0.04))
    shift(LB_FEXT, "f2", -u(FALSEX, 0.10), u(FALSEX, 0.04)); shift(LB_FEXT, "假十字", 0, u(FALSEX, 0.12))
    shift(LB_DIA, "南船五", u(DIAF, 0.15), -u(DIAF, 0.02)); shift(LB_DIA, "南船四", -u(DIAF, 0.13), -u(DIAF, 0.02))   # 南船三、海石五不標（太擠；旁白只點名這兩顆）
    shift(LB_DIA, "never", 0, u(DIAF, 0.05)); shift(LB_DIA, "鑽石十字", 0, u(DIAF, 0.13))
    shift(LB_K1, "假", 0, u(K1, 0.12)); shift(LB_K1, "真", u(K1, 0.17), u(K1, 0.07))
    shift(LB_K2, "假", 0, u(K1, 0.18)); shift(LB_K2, "真", 0, u(K1, 0.10))
    shift(LB_CN, "十字架", 0, u(ALL9, 0.10)); shift(LB_CN, "天社", 0, u(ALL9, 0.10))
    shift(LB_CN, "海石", 0, -u(ALL9, 0.10)); shift(LB_CN, "南船", 0, -u(ALL9, 0.10))
    shift(LB_TONGA, "Toloatonga", u(T10, 0.10), u(T10, 0.15)); shift(LB_TONGA, "Toloalahi", 0, u(T10, 0.15))
    shift(LB_TONGA, "註1", u(T10, 0.33), -u(T10, 0.50)); shift(LB_TONGA, "註2", u(T10, 0.33), -u(T10, 0.56))
    for LB in (LB_TPE, LB_KT):
        shift(LB, "γ", u(T1, 0.20), 0); shift(LB, "α", u(T1, 0.20), 0)
        shift(LB, "南門二", 0, -u(T1, 0.05)); shift(LB, "馬腹一", 0, u(T1, 0.05)); shift(LB, "地", 0, u(T1, 0.36))
    shift(LB_MOON, "月", u(T1, 0.10), u(T1, 0.28)); shift(LB_MOON, "月2", u(T1, 0.10), u(T1, 0.23))

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, g)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for gg, name in LINE_SETS:
        m.L_lines(gg, name=name)
    write_custom(m, custom)
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文；分鏡表 Z/T 都在南盤上做，一律寫 R） ════════════════════
    ls = lambda *n: list(n)
    NS = dict(north=False, kind="R")
    shots = [
        dict(code="01", sec=10, **NS, frames=[WIDE, ALL], layers=["L4"], labels=[], labels_end=ls("三個十字"),
             vo="上週，鴯鶓的頭就靠在南十字旁邊。今晚來認十字：同一片星空，找南方的人看見——三個十字。",
             card="南天的三個十字",
             note="第一頁就在南盤圖層組（整集不換組；rot≈0＝5/14 21:00 面南：南十字直立在上、假十字在右）；"
                  "三組連線（琥珀／紅／藍）同時亮起，推近"),
        dict(code="02", sec=15, **NS, frames=[ALL, CRUXF], layers=["十", "圈", "煤"], labels=[], labels_start=ls("三個十字"),
             labels_end=ls("南十字"),
             vo="先看真的：南十字是全天最小的星座。四顆亮星排成風箏形，十字裡還有第五顆小星；最上面的十字架一偏橘紅，旁邊還貼著一塊黑——上週的煤袋。",
             card="真十字：小、第五星、一塊黑",
             note="推近南十字（分鏡表 T，盤上做）；ε Cru 白圈；煤袋白虛線；標籤 十字架一～四"),
        dict(code="03", sec=21, **NS, frames=[CRUXF, POINT], layers=["十", "指"], labels=[], labels_start=ls("南十字"),
             labels_end=ls("指南"),
             overlay="C-X05-01_找南方的兩條線", overlay_layers=["延長層", "中垂線層", "地平線層"],
             vo="它最好用的地方，是會指路：從十字架一往十字架二，延長大約四倍半，就到南天極附近，差不到三度；再從那裡垂直落到地平線，就是正南。旁邊這兩顆亮星叫「指針」：南門二和馬腹一，畫一條中垂線，也指到同一帶。",
             card="延長四倍半→南天極附近",
             note=f"拉遠到南天極（盤心）；指南線（白虛線）：γ→α 延長 4.5 倍、南門二—馬腹一中垂線；"
                  f"交點（離南天極 {g['X_pole']:.2f}°）畫 3° 圈、標「差不到 3°」，盤心十字記號標「南天極」；"
                  "迄格疊 C-X05-01（延長層→中垂線層→地平線層，旁白「垂直落到地平線」時出第三層）"),
        dict(code="04", sec=16, **NS, frames=[NAMES], layers=["十", "網", "歪", "瘸"], labels=ls("南十字的名字"),
             overlay="C-X05-02_南十字的名字",
             vo="南十字這一帶，各地都有名字：東加叫它野鴨，夏威夷叫它「月亮照看的孩子」，阿努塔人以前叫它漁網；印尼的曼達爾漁夫說是歪房子，布吉斯人說是瘸腿的房子。",
             card="同一個十字的名字",
             note="同框；跨文化標籤整疊在南十字右側，照旁白順序逐條淡入（Canva 動畫）；連線照 Stellarium 實際的星："
                  "漁網（綠，含網柄南門二、馬腹一）→ 歪房子（藍，含 δ Cen 屋頂）→ 瘸腿的房子（紫，含 μ Cru）依旁白淡入；"
                  "迄格疊 9:16 圖卡 C-X05-02（可存圖）"),
        dict(code="05", sec=12, **NS, frames=[NAMES, FALSEF], layers=["L4"], labels=[], labels_start=[], labels_end=ls("假十字"),
             vo="再往西大約三十度，有一個更大、整體暗一點的十字：假十字。它旁邊沒有那兩顆亮晶晶的指針，也沒有煤袋。",
             card="假十字：大、沒有指針",
             note=f"盤逆時針轉 {ROT_C:+.1f}°→{ROT_F:+.1f}°（往西＝倒轉時間）到假十字（紅）置中＝墾丁 3/26 21:00 的方向"),
        dict(code="06", sec=22, **NS, frames=[FALSEF, FALSEX], layers=["L4", "延"], labels=ls("假十字"), labels_start=ls("假十字"),
             labels_end=ls("假十字延長"),
             overlay="C-X05-03_認錯十字", overlay_layers=["真南層", "假十字層"],
             vo="最要命的是方向：照南十字的方法延長出去，根本不會經過南天極，離它二十度以上。在南緯二十度左右的海上，假十字站到最高時算一次：看你取哪一條對角線，「南方」會偏東二十幾度，或偏西四十多度。",
             card="偏東 24° 或偏西 42°",
             note=f"拉遠到南天極；前半：假十字兩條對角線延長 4.5 倍（紅虛線），盤心「南天極」不在線上"
                  f"（大圓最近 {g['f1_min']:.1f}°、{g['f2_min']:.1f}°）；後半疊 C-X05-03（真南層→假十字層）"),
        dict(code="07", sec=17, **NS, frames=[FALSEX, DIAF], layers=["L4", "墾"], labels=[], labels_start=[], labels_end=ls("鑽石十字"),
             vo="第三個是鑽石十字，這是現代觀星的人取的名字。它更靠近南天極，四顆星都在船底座，長軸大約十度。在台灣，它永遠湊不齊：最亮的南船五，還有南船四，連在墾丁都不會升起。",
             card="鑽石十字：台灣湊不齊",
             note=f"盤轉 {ROT_F:+.1f}°→{DIAF[3]:+.1f}° 到鑽石十字（藍）；墾丁永不升起圈（綠虛線，dec {NEVER_K:.1f}）："
                  "南船五、南船四在圈內；南船三、海石五在圈外但只擦過地平線 3–4°"),
        dict(code="08", sec=21, **NS, horizon=[PHI_K], frames=[K1, K2], layers=["L4"], labels=ls("墾丁3月底"),
             labels_end=ls("墾丁4月中"), overlay="C-X05-04_台灣怎麼分",
             vo="在台灣，最容易認錯的時候是春天。三月底晚上九點，假十字正好立在正南方，在墾丁離地平線八到十三度——真的南十字，這時才剛要升起。到了四月中晚上九點半，兩個十字同時在南方低空：右邊大的是假的，左邊小的才是真的。",
             card="右邊大的是假的",
             note=f"山＝墾丁南方地平線（21.95°N）；盤 {ROT_F:+.1f}°（3/26 21:00）→{ROT_A:+.1f}°（4/15 21:30），"
                  "畫面不動、只轉盤；迄格疊 9:16 圖卡 C-X05-04（可存圖）"),
        dict(code="09", sec=15, **NS, frames=[ALL9W, ALL9], layers=["中"], labels=ls("中國星官"),
             vo="中國的星官，把這三個十字拆得很散：南十字是明朝末年才補上的「十字架」；假十字上半截，後來的星表算進古老的「天社」，下半截叫「海石」；鑽石十字大多屬於「南船」。",
             card="十字架・天社・海石・南船",
             note=f"切回無地平線的南盤（山回模板位置；盤 {ROT_A:+.1f}°→{ROT_C:+.1f}°）；三個十字完整；"
                  "連線換成中國星官（十字架琥珀／天社紅／海石綠／南船藍，Stellarium chinese）"),
        dict(code="10", sec=12, **NS, frames=[ALL9, T10], layers=["L4"], labels=[], labels_start=ls("中國星官"),
             labels_end=ls("東加兩隻野鴨"),
             vo="東加後來的資料，也把兩隻分開了：星空軟體 Stellarium 收的東加版本裡，南十字是「南方的野鴨」，假十字是另一隻「大野鴨」。",
             card="東加：兩隻野鴨",
             note="同框；Toloatonga（南十字）、Toloalahi（假十字＝同 Stellarium modern 假十字兩條對角線）；"
                  "小字「Stellarium 版（據 1990 年資料）／Collocott 1922 只有 Toloa＝南十字」"),
        dict(code="11", sec=17, **NS, frames=[T10], layers=["十"], labels=[], labels_start=ls("東加兩隻野鴨"),
             overlay="C-X05-05_歲差", overlay_layers=["軌跡層", "高度層"],
             vo="在台灣看南十字這麼低，也不是一直如此。地軸像陀螺一樣慢慢晃，兩千年前，台北看南十字比現在高了十一度。托勒密在埃及編星表時，也看得到它，只是把它當成半人馬的後腳。",
             card="兩千年前高了十一度",
             note="定格疊 C-X05-05（軌跡層：南天極繞黃南極的圓與 0 年、1000 年、2027 年位置 → 高度層：台北上中天高度"
                  "12.9°→7.4°→1.7°，以十字架二計、幾何高度）"),
        dict(code="12", sec=22, **NS, horizon=[PHI_TPE, PHI_K], frames=[T1, K3], layers=["十"],
             labels=ls("今晚台北"), labels_end=ls("今晚墾丁"),
             vo="今晚九點，南十字正好直立在正南方。在台北，整個十字都在八度以下，最下面的十字架二只有兩度，很難看到。到了墾丁、蘭嶼，它離地平線五到十一度，八點到十點最高，左下方還有南門二和馬腹一；記得找南方海面開闊的地方。",
             card="今晚九點，正南方",
             note=f"山＝台北南方地平線（25.03°N，rot {ROT_T:+.2f}°）→ 墾丁（21.95°N，{ROT_K:+.2f}°）：山往下降、"
                  "十字跟著露出來；高度標籤（含折射）照逐字稿星空對時"),
        dict(code="13", sec=8, **NS, horizon=[PHI_K], frames=[K3, K3b], layers=["十"], labels=[], labels_start=ls("今晚墾丁"),
             labels_end=ls("月光"),
             overlay="C-X05-06_今晚看南十字",
             vo="月亮今晚有六成多亮，掛在西南方高處；往南看時，記得找個東西擋住月光。",
             card="六成月光，記得遮",
             note="同框（墾丁）；月光標籤在右上（月亮在畫面外：西南 237°、高 57°）；迄格疊 9:16 圖卡 C-X05-06（可存圖）"),
        dict(code="14", sec=11, **NS, frames=[K3b, NEXT], layers=["L4"], labels=[], labels_start=[], labels_end=ls("三個十字"),
             vo="下週五是航海季的總集篇：從台灣出發的南島語族、印度洋的阿拉伯水手——在羅盤上船以前，人類怎麼看著星星過海。",
             card="下集見｜星星導航總集：在羅盤上船以前",
             note="南盤歸位、拉遠回三個十字（山回模板位置）；端卡「下集見｜星星導航總集：在羅盤上船以前」＋追蹤 CTA"),
    ]
    print("\n── 旁白字數 ──")
    tot_u = 0
    for sh in shots:
        u_ = vo_units(sh["vo"]); tot_u += u_
        r = u_ / sh["sec"]
        print(f"  {sh['code']}  {u_:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u_
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
    print(f"  LST：" + "、".join(f"{k} {v:.2f}" for k, v in LST_AT.items()) +
          f"；y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {m.k:.4f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=[h for h in hips if isinstance(h, int)], 原文=orig, 拼音="", 英文翻譯=en,
                           中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms,
               "cross": [dict(原文="Toloa", 中譯="野鴨（東加）", 英文="wild duck", 顏色="amber"),
                         dict(原文="Hānaiakamalama", 中譯="月亮照看的孩子（夏威夷）", 英文="cared for by the Moon",
                              顏色="amber"),
                         dict(原文="Te Kupenga", 中譯="漁網（阿努塔）", 英文="the Net", 顏色="green"),
                         dict(原文="Sapo Kepang", 中譯="歪房子（曼達爾）", 英文="Slanted House", 顏色="blue"),
                         dict(原文="Bola Képpang", 中譯="瘸腿的房子（布吉斯）", 英文="Lame House", 顏色="purple")],
               "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": dict(F=ROT_F, A=ROT_A, T=ROT_T, K=ROT_K, D=DIAF[3]), "lst0": LST0,
               "geometry": {k: g[k] for k in ("crux_min", "bis_min", "X", "X_pole", "f1_min", "f2_min")}},
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
        gl = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, gl, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    qa_wall(m, g, shots, label_sets)
    print("\n完成 →", OUT)


def qa_wall(m, g, shots, label_sets):
    """QA：鏡頭牆不畫自訂圖層與地平線 → 另出「自訂層＋地平線＋逐格標籤（起格／迄格各自的層）」縮圖牆"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    S = dict(G.load_stars(BASE))
    LS = {n: it for it, n in label_sets}
    cells = [(sh, i, f) for sh in shots for i, f in enumerate(sh["frames"])]
    cols = 6
    rows = (len(cells) + cols - 1) // cols
    fig = plt.figure(figsize=(cols * 2.6, rows * 4.8), dpi=100)
    fig.patch.set_facecolor("#0B0F1E")
    col = lambda c: COLORS.get(c, c)
    for k, (sh, i, (cx, cy, fov, rot)) in enumerate(cells):
        ax = fig.add_subplot(rows, cols, k + 1)
        ax.set_facecolor("#0B0F1E"); ax.set_xticks([]); ax.set_yticks([])
        hw, hh = fov / 2, fov * 8 / 9
        ax.set_xlim(cx - hw, cx + hw); ax.set_ylim(cy - hh, cy + hh)
        Pp = lambda ra, dec: disc_xy(m, ra, dec, rot)
        for h, (ra, dec, v) in [(h, S[h][:3]) for h in S if S[h][2] < 5.0 and S[h][1] < 20]:
            p = Pp(ra, dec)
            if abs(p[0] - cx) < hw and abs(p[1] - cy) < hh:
                ax.scatter([p[0]], [p[1]], s=max(0.3, (5.4 - v)) ** 1.6 * 1.3, c="white", lw=0)
        for key in sh["layers"]:
            for segs, c, _ in LINE_GROUPS[key]:
                for seg in segs:
                    q = [Pp(*S[h][:2]) for h in seg if h in S]
                    ax.plot([a[0] for a in q], [a[1] for a in q], c=col(c), lw=0.8)
        cus = {"指": [("crux_ext", "white"), ("bis", "white"), ("X_circle", "white")],
               "延": [("f1", "red"), ("f2", "red")], "煤": [("coal", "white")], "墾": [("never", "green")]}
        for key in sh["layers"]:
            for nm, c in cus.get(key, []):
                q = [Pp(*p) for p in g[nm]]
                ax.plot([a[0] for a in q], [a[1] for a in q], c=col(c), lw=0.7, ls="--")
        if "圈" in sh["layers"]:
            p = Pp(*S[EPS_CRU][:2]); ax.scatter([p[0]], [p[1]], s=40, facecolors="none", edgecolors="white", lw=0.6)
        hz = sh.get("horizon") or []
        if hz:
            phi = hz[0] if i == 0 else hz[-1]
            hp = horizon_points(phi, rot + LST0, n=721)
            q = [Pp(ra, dec) for ra, dec in hp if dec < 20]
            ax.plot([a[0] for a in q], [a[1] for a in q], c="#7BD88F", lw=1.0)
            ax.fill_between([cx - hw, cx + hw], cy - hh, cy - hh, color="k")
        last = i == len(sh["frames"]) - 1
        labs = (sh.get("labels_end") if (last and "labels_end" in sh and len(sh["frames"]) > 1) else
                sh.get("labels_start") if (i == 0 and "labels_start" in sh) else sh.get("labels", []))
        for n in labs:
            for it in LS[n]:
                ra, dec = (S[it["hip"]][:2] if "hip" in it else (it["ra"], it["dec"]))
                p = Pp(ra, dec)
                px = min(96.0, max(36.0, it["size"] * 1.7 / fov * 1080))     # Canva 原生字 36–96 px
                ax.text(p[0] + it["dx"], p[1] + it["dy"], it["text"], color=col(it["color"]),
                        fontsize=px * 2.6 * 72 * 0.78 / 1080, ha="center",
                        va="center", fontproperties=_fp(), clip_on=True)
        ax.set_title(f"{sh['code']} {'起迄'[min(i, 1)] if len(sh['frames']) > 1 else '定'}  fov {fov:.0f} rot {rot:+.0f}",
                     color="white", fontsize=7, fontproperties=_fp())
    fig.savefig(os.path.join(OUT, f"{EP}_QA-自訂層鏡頭牆.png"), facecolor="#0B0F1E")
    plt.close(fig)
    print(f"  ✓ {EP}_QA-自訂層鏡頭牆.png")


def _fp():
    from matplotlib.font_manager import FontProperties
    return FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


if __name__ == "__main__":
    build()
