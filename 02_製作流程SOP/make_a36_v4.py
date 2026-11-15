# -*- coding: utf-8 -*-
"""A-36 現代星座（下）：課本沒教的星群 Asterisms｜大畫布 v4.6（北盤主秀＋長圖帶狀）

論點：大家最先認得的圖案（北斗、夏季大三角、茶壺……）多半不是 IAU 星座，而是「星群」，而且常常跨星座；
同一批星在別的文化又是別的圖案（中國北斗星官、南斗、室壁；阿拉伯的兩隻鷹、鴕鳥）。星群沒有官方名字，
星星卻有：IAU 星名工作小組（2016 起），台灣命名的 Formosa／Sazum（2019）。

來源（全部照原樣，沒有修改連線）：
  07_資料來源/_整理CSV/02_星群Asterisms.csv（Stellarium modern 星群：BDr 北斗、STr 夏季大三角、GSP 飛馬大四邊形、
  Tea 茶壺、CoH 衣架、QuM 牆象限儀、RoC 查理的橡樹、RH1 春季大曲線；arabic_al-sufi：NasW、NasT）；
  Stellarium stellarium-master：modern_iau（UMa 19 星連線、Leo 連線、IAU 1875 邊界 edges、IAU-CSN 星名）、
  chinese（039 北斗、005 斗宿、018 室宿、002 壁宿）、arabic_indigenous（NaaW 下河喝水的鴕鳥，A-19）。
  天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，UTC+8；1010 hPa、20°C）。
逐字稿：04_腳本庫/A-36-現代星座下課本沒教的星群Asterisms-逐字稿-v1.md。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 278 → 長圖走廊 x=0 落在人馬座茶壺（γ +6.5 … ζ −8.7、銀心 +11.6），07 鏡的茶壺＋銀河蒸氣可以用 T 沿走廊取景，
             畫面下緣伸進南縫合帶也有內容（走廊內縫合帶＝連續天空）；走廊往上經過織女（x −1.2）進北盤。
             衣架 x −13.6（08 鏡，帶內）；飛馬大四邊形 x −68…−85（06 鏡，帶內 Z）。
  D_s = 41、D_r = 45 → k = 1.2732。決定因素是 12 鏡要在北盤上看到東南低空的茶壺＋滿月（dec −25…−34，r 147–158）：
             D_r 49（k 1.40）時茶壺 r 168–176，貼著填滿圓邊緣、畫面角落放不下；D_r 45 剛好。
             北斗（Alkaid +49.3）、牆象限儀（+49.6…+57.9）都 ≥ D_r，在盤本體。
             長圖帶 41 對 06 鏡（飛馬 +15…+29）太緊：06 用 Z 驗證、上下緣不出 D_r（本集自訂規則，A-30 同法）。
  D_fill = −45 → R_fill = 171.89（盤寬 ÷ 畫布寬 0.955，不是同寬）；|x_t|＋R_fill ≤ 180 ✓。
             D_fill −51 可到 179.5，但盤寬比 0.997 幾乎等於同寬（A-04 的坑），而且 12 鏡用不到那一圈。
  x_tN = x_tS = 0
  北盤旋轉：rot＝−((LST＋180−278) mod 360)；台北 6/18 20:00 = −110.1°、22:00 = −140.2°。
           01–02 停在 20:00（天黑後），03 鏡 20:00 → 22:00 逆時針 30.1°（斗柄繞北極），之後北盤都停在 22:00；
           13 鏡從 22:00 逆時針轉一整圈（每段 ≤60°＜170° ✓；Canva 旋轉只收 ±180，−180→+180 那一頁同畫面硬切，
           拆成 13（1 秒）＋13b（7 秒，旁白全在這裡）。
           換組頁（盤⇄長圖）盤要轉回 0°：05→06「歸位」+140.2°、08→09 回北盤後 0°→−140.2°（都＜170° ✓）。

鏡頭路線（逐字稿 13 鏡，秒數照逐字稿，總長 197 秒）
  01 北盤 20:00 fov 140 總覽（IAU 邊界＋北斗）→ 推近北斗 → 02 推近大熊（19 星）＋C-A36-01
  → 03 中國北斗星官（青）＋大熊邊界，盤轉到 22:00 → 04 滑到東方夏季大三角（三座邊界）＋C-A36-02
  → 05 兩隻鷹（綠）＋阿拉伯原文 →【換組】長圖 06 飛馬大四邊形（壁宿二、室宿＋壁宿）
  → 07 走廊上的茶壺（鴕鳥、南斗＋斗宿三）→ 08 衣架（放大星點）＋C-A36-03 →【換組】北盤 09 牆象限儀＋C-A36-04（查理的橡樹）
  → 10 拉遠：IAU 星名 → 11 獅子座 Formosa → 12 今晚十點（大三角＋北斗→大曲線）＋圖卡 C-A36-05（茶壺＋滿月在圖卡上）
  → 13／13b 北盤快轉一圈（跨 ±180° 那一格同畫面硬切）＋端卡

check_shots 的 ⚠（判斷後接受）：見 WARN_OK。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import horizon_points, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-36"
OUT = os.path.join(BASE, "05_素材/A-36_現代星群/_v4大畫布")
LST0 = 278.0
D_S, D_R, D_FILL = 41.0, 45.0, -45.0
TPE = (25.0330, 121.5654)
PHI = 25.033
TEAL = "#3D8B7D"          # 中國星官（逐字稿指定；團隊色票外的第 7 色，只用在中國）
GREY = "#B8C2D6"

WARN_OK = """
  01–05、09–13b（R，北盤）：與長圖互切的只有 05 迄 → 換組、09 起 ← 換組；換組格由 gen_canva_pages 自動插在盤心
  （fov ≤ 50、0°），這兩鏡本身的起訖格都是新構圖、不直接與大畫布硬切 → 「切點」⚠ 可接受。
"""


# ══════════════════════════════════════════════════════════════════
# 〇、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(when):
    return math.degrees(_obs(when).sidereal_time())


def norm180(r):
    r = (r + 180.0) % 360.0 - 180.0
    return round(180.0 if abs(r + 180.0) < 1e-9 else (0.0 if abs(r) < 0.005 else r), 2)


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    return norm180(-((lst_obs + 180.0 - LST0) % 360.0))


T_TPE = {"2000": "2027/6/18 20:00", "2200": "2027/6/18 22:00"}
LST_AT = {k: lst_at(v) for k, v in T_TPE.items()}
ROT = {k: rot_n(v) for k, v in LST_AT.items()}
R20, R22 = ROT["2000"], ROT["2200"]


def altaz(ra, dec, when):
    import ephem
    o = _obs(when)
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def moon_at(when):
    import ephem
    o = _obs(when)
    mo = ephem.Moon(); mo.compute(o)
    q = ephem.Equatorial(ephem.Equatorial(mo.ra, mo.dec, epoch=o.date), epoch=ephem.J2000)
    return dict(ra=math.degrees(q.ra), dec=math.degrees(q.dec), alt=math.degrees(mo.alt), az=math.degrees(mo.az),
                phase=float(mo.phase), con=ephem.constellation(mo)[1])


MOON = moon_at("2027/6/18 22:00")


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 一、連線資料
# ══════════════════════════════════════════════════════════════════
SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
AST_CSV = os.path.join(BASE, "07_資料來源/_整理CSV/02_星群Asterisms.csv")


def ast_lines(aid):
    """02_星群Asterisms.csv：同一 ID 的每一列＝一筆畫（重複列只取一次）"""
    out, seen = [], set()
    for r in csv.DictReader(open(AST_CSV, encoding="utf-8-sig")):
        if r["ID"].split()[-1] == aid and r["HIP 順序"] not in seen:
            seen.add(r["HIP 順序"])
            out.append([int(h) for h in r["HIP 順序"].split("→")])
    assert out, aid
    return out


def sc_lines(cu, cid):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    for c in d.get("constellations", []) + d.get("asterisms", []):
        if c["id"].split()[-1] == cid:
            return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    raise KeyError(cu + " " + cid)


flat = lambda segs: sorted({h for l in segs for h in l})

SEG = {k: ast_lines(k) for k in ("BDr", "STr", "GSP", "Tea", "CoH", "QuM", "RoC", "RH1", "NasW", "NasT", "Mlk")}
SEG["UMa"] = sc_lines("modern_iau", "UMa")
SEG["Leo"] = sc_lines("modern_iau", "Leo")
SEG["北斗"] = sc_lines("chinese", "039")
SEG["斗宿"] = sc_lines("chinese", "005")
SEG["室宿"] = sc_lines("chinese", "018")
SEG["壁宿"] = sc_lines("chinese", "002")
SEG["NaaW"] = sc_lines("arabic_indigenous", "NaaW")

DUBHE, MERAK, ALKAID, POLARIS = 54061, 53910, 67301, 11767
VEGA, ALTAIR, DENEB = 91262, 97649, 102098
ALPHERATZ, MARKAB, SCHEAT, ALGENIB = 677, 113963, 113881, 1067
ARCT, SPICA = 69673, 65474
MU_SGR, LAM_SGR, ETA_SGR, KAUS = 89341, 90496, 89642, 90185
FORMOSA = 56508
COH = flat(SEG["CoH"])
GC = (266.417, -29.008)                         # 銀心（Sgr A*，J2000）
assert len(flat(SEG["UMa"])) == 19, "modern_iau 大熊座應為 19 星"
assert flat(SEG["北斗"]) == flat(SEG["BDr"]), "中國北斗＝西方北斗同七星"
assert len(COH) == 10 and len(flat(SEG["Tea"])) == 8
assert set(flat(SEG["斗宿"])) == set(flat(SEG["Mlk"])) | {MU_SGR}, "南斗＝奶勺＋斗宿三"
assert flat(SEG["NaaW"]) == sorted([88635, 89931, 90185, ETA_SGR])
assert set(flat(SEG["室宿"]) + flat(SEG["壁宿"])) == set(flat(SEG["GSP"]))

LG = {
    "北斗": [(SEG["BDr"], "amber", 1.15)],
    "大熊": [(SEG["UMa"], "white", 0.8)],
    "北斗星官": [(SEG["北斗"], TEAL, 1.5)],
    "夏三角": [(SEG["STr"], "blue", 1.15)],
    "兩隻鷹": [(SEG["NasW"] + SEG["NasT"], "green", 1.3)],
    "四邊形": [(SEG["GSP"], "amber", 1.0)],
    "室壁": [(SEG["室宿"] + SEG["壁宿"], TEAL, 1.6)],
    "茶壺": [(SEG["Tea"], "amber", 1.0)],
    "鴕鳥": [(SEG["NaaW"], "green", 1.4)],
    "南斗": [(SEG["斗宿"], TEAL, 1.6)],
    "衣架": [(SEG["CoH"], "purple", 0.12)],
    "大曲線": [(SEG["RH1"], "green", 1.15)],
    "獅子": [(SEG["Leo"], "white", 0.55)],
}
LNAME = {"北斗": "連線-北斗七星（星群）", "大熊": "連線-大熊座（IAU 19 星）", "北斗星官": "連線-北斗（中國星官）",
         "夏三角": "連線-夏季大三角", "兩隻鷹": "連線-兩隻鷹（阿拉伯）", "四邊形": "連線-飛馬大四邊形",
         "室壁": "連線-室宿＋壁宿（中國）", "茶壺": "連線-茶壺", "鴕鳥": "連線-下河喝水的鴕鳥（阿拉伯）",
         "南斗": "連線-南斗六星（中國）", "衣架": "連線-衣架（細線）", "大曲線": "連線-春季大曲線",
         "獅子": "連線-獅子座（IAU）"}
LG_MAIN = LG["北斗"] + LG["夏三角"] + LG["四邊形"] + LG["茶壺"] + LG["大曲線"]     # L4＝本集的現代星群


# ══════════════════════════════════════════════════════════════════
# 二、IAU 邊界（modern_iau edges，B1875 → J2000）
# ══════════════════════════════════════════════════════════════════
def _hms(s):
    h, m_, x = (float(t) for t in s.split(":"))
    return (h + m_ / 60 + x / 3600) * 15.0


def _dms(s):
    sg = -1 if s.startswith("-") else 1
    d, m_, x = (float(t) for t in s.lstrip("+-").split(":"))
    return sg * (d + m_ / 60 + x / 3600)


def iau_edges():
    import ephem
    B1875 = ephem.Date(2405889.258550475 - 2415020.0)
    d = json.load(open(os.path.join(SC, "modern_iau", "index.json"), encoding="utf-8"))
    out = []
    for e in d["edges"]:
        p = e.split()
        typ = p[1][0]
        r1, d1, r2, d2 = _hms(p[2]), _dms(p[3]), _hms(p[4]), _dms(p[5])
        if typ == "M":
            n = max(2, int(abs(d2 - d1) / 1.0) + 2)
            pts = [(r1, d1 + (d2 - d1) * i / (n - 1)) for i in range(n)]
        else:
            dr = ((r2 - r1) + 180) % 360 - 180
            n = max(2, int(abs(dr) / 1.0) + 2)
            pts = [(r1 + dr * i / (n - 1), d1) for i in range(n)]
        q = []
        for ra, dec in pts:
            a = ephem.Equatorial(math.radians(ra % 360), math.radians(dec), epoch=B1875)
            b = ephem.Equatorial(a, epoch=ephem.J2000)
            q.append((math.degrees(b.ra), math.degrees(b.dec)))
        out.append((q, p[6], p[7]))
    return out


EDGES = iau_edges()


# ══════════════════════════════════════════════════════════════════
# 三、自訂圖層（大畫布與南北盤同一支函式畫 → 逐點一致）
# ══════════════════════════════════════════════════════════════════
def custom_layers(m, S):
    RED, PUR = COLORS["red"], COLORS["purple"]

    def iau(sel, col=GREY, w=0.45, op=0.55, dash="1.0 0.7"):
        def f(s, pos, runs, disc):
            rr = []
            for pts, a, b in EDGES:
                if sel(a, b):
                    rr += runs(pts)
            s.polylines(rr, stroke=col, w=m.lw * w, opacity=op, dash=dash)
        return f

    def three(s, pos, runs, disc):
        """天琴、天鷹、天鵝三座的邊界（各一色；逐字稿寫「各填淡色」——SVG 邊界是分段的，改用彩色邊界線）"""
        for abbr, col in (("LYR", "#9CC2FF"), ("AQL", "#6FA8FF"), ("CYG", "#B9D3FF")):
            rr = []
            for pts, a, b in EDGES:
                if abbr in (a, b):
                    rr += runs(pts)
            s.polylines(rr, stroke=col, w=m.lw * 0.55, opacity=0.8, dash="1.2 0.6")

    def qum(s, pos, runs, disc):
        rr = []
        for seg in SEG["QuM"]:
            for a, b in zip(seg, seg[1:]):
                from gen_projection import great_circle
                rr += runs(great_circle(*S[a][:2], *S[b][:2]))
        s.polylines(rr, stroke=RED, w=m.lw * 0.9, opacity=0.95, dash="1.1 0.7")

    def coh_dots(s, pos, runs, disc):
        """衣架 10 星（V 5.2–7.2，低於 maglim 不進星點層）：放大的星點，給 fov 6 的特寫用"""
        for h in COH:
            r = 0.040 + 0.020 * max(0.0, 7.3 - S[h][2])
            for p in pos(*S[h][:2]):
                s.circle(p[0], p[1], r * 2.6, fill="#FFFFFF", opacity=0.18)
                s.circle(p[0], p[1], r, fill="#FFFFFF", opacity=1.0)

    def formosa(s, pos, runs, disc):
        for p in pos(*S[FORMOSA][:2]):
            s.circle(p[0], p[1], 0.9, fill="#FFC94A", opacity=0.14)
            s.circle(p[0], p[1], 0.30, fill="#FFFFFF", opacity=1.0)
            s.circle(p[0], p[1], 1.6, stroke="#FFC94A", w=0.10, opacity=0.9)

    def moon(s, pos, runs, disc):
        for p in pos(MOON["ra"], MOON["dec"]):
            s.circle(p[0], p[1], 2.6, fill="#FFF6D8", opacity=0.10)
            s.circle(p[0], p[1], 1.5, fill="#FFF6D8", opacity=0.18)
            s.circle(p[0], p[1], 0.75, fill="#FFF6D8", opacity=1.0)

    return [("IAU邊界", iau(lambda a, b: True)),
            ("IAU邊界-大熊座", iau(lambda a, b: "UMA" in (a, b), col="#FFFFFF", w=0.6, op=0.85)),
            ("IAU邊界-天琴天鷹天鵝", three),
            ("IAU邊界-飛馬仙女", iau(lambda a, b: "PEG" in (a, b) or "AND" in (a, b), col="#FFFFFF", w=0.6, op=0.8)),
            ("連線-牆象限儀（虛線）", qum),
            ("衣架放大星點", coh_dots),
            ("Formosa光暈", formosa),
            ("滿月6月18日22時", moon)]


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
# 四、旁白字數（中文字＋外文音節；與 make_a34_v4.py 同一套算法）
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
# 五、名詞總表（＝標籤對照表）  key: (錨點, 原文, 英文, 中文, 顏色, 來源)
# ══════════════════════════════════════════════════════════════════
IAU_CN = {57399: ("Taiyangshou", "太陽守"), 69732: ("Xuange", "玄戈"), 77233: ("Zhou", "周")}

TERMS = {
    "北斗": (flat(SEG["BDr"]), "Big Dipper", "Big Dipper (Plough)", "北斗七星", "amber",
           "02_星群Asterisms.csv AST modern BDr（星群）"),
    "大熊座": (flat(SEG["UMa"]), "Ursa Major", "Ursa Major", "大熊座", "white",
            "Stellarium modern_iau UMa（19 星；01_星座連線筆畫.csv 的 western UMa 18 星不用）"),
    "星群": ([DUBHE], "asterism", "asterism", "星群", "amber", "逐字稿 02 鏡字卡"),
    "北斗星官": (flat(SEG["北斗"]), "北斗", "Northern Dipper", "北斗（星官）", TEAL,
             "Stellarium chinese 039 北斗；《史記・天官書》「北斗七星」"),
    "北極星": ([POLARIS], "Polaris", "Polaris", "北極星", "white", ""),
    "織女": ([VEGA], "Vega", "Vega (α Lyr)", "織女・天琴座", "blue", "距離 25.0 光年（Hipparcos 新歸算 130.23 mas）"),
    "牛郎": ([ALTAIR], "Altair", "Altair (α Aql)", "牛郎・天鷹座", "blue", "16.7 光年（194.95 mas）"),
    "天津四": ([DENEB], "Deneb", "Deneb (α Cyg)", "天津四・天鵝座", "blue", "Hipparcos 2.31 mas（約 1,400 光年）；"
                                                                    "大氣模型 802 pc（約 2,600 光年）"),
    "夏三角": (flat(SEG["STr"]), "Summer Triangle", "Summer Triangle", "夏季大三角", "blue", "AST modern STr"),
    "Wāqiʿ": ([VEGA], "النسر الواقع", "al-nasr al-wāqiʿ → Vega", "俯衝的鷹 → Vega", "green",
              "arabic_al-sufi NasW（織女一＋ε¹、ζ¹ Lyr）"),
    "Ṭāʾir": ([ALTAIR], "النسر الطائر", "al-nasr al-ṭāʾir → Altair", "飛翔的鷹 → Altair", "green",
              "arabic_al-sufi NasT（河鼓二＋β、γ Aql）"),
    "Dajāja": ([DENEB], "ذنب الدجاجة", "dhanab al-dajāja → Deneb", "母雞的尾巴 → Deneb", "green",
               "阿拉伯文譯托勒密「鳥」座；本土名 al-Ridf「後騎」（arabic_indigenous）"),
    "四邊形": (flat(SEG["GSP"]), "Great Square of Pegasus", "Great Square of Pegasus", "飛馬大四邊形", "amber",
            "AST modern GSP"),
    "壁宿二": ([ALPHERATZ], "Alpheratz", "Alpheratz (α And, 舊稱 δ Peg)", "壁宿二・仙女座", "white",
            "1930 Delporte 邊界只劃進仙女座"),
    "飛馬座": ([SCHEAT, MARKAB, ALGENIB], "Pegasus", "Pegasus", "飛馬座", "white", "IAU"),
    "仙女座": ([ALPHERATZ], "Andromeda", "Andromeda", "仙女座", "white", "IAU"),
    "室宿": (flat(SEG["室宿"]), "室宿", "Encampment", "室宿（營室）", TEAL, "chinese 018"),
    "壁宿": (flat(SEG["壁宿"]), "壁宿", "Wall", "壁宿（東壁）", TEAL, "chinese 002"),
    "茶壺": (flat(SEG["Tea"]), "Teapot", "Teapot", "茶壺", "amber", "AST modern Tea（人馬 8 星）"),
    "蒸氣": (GC, "銀河中心", "Galactic Centre", "蒸氣＝銀河中心", "white", "Sgr A*"),
    "鴕鳥": (flat(SEG["NaaW"]), "النعام الوارد", "al-Naʿām al-wārid", "下河喝水的鴕鳥（A-19）", "green",
           "arabic_indigenous NaaW（γ、δ、ε、η Sgr＝中國箕宿）"),
    "南斗": (flat(SEG["斗宿"]), "南斗", "Dipper (Dou)", "南斗六星（斗宿）", TEAL, "chinese 005"),
    "斗宿三": ([MU_SGR], "μ Sgr", "μ Sgr", "斗宿三（壺外）", TEAL, "λ 西北 5.5°"),
    "衣架": (COH, "Coathanger", "Coathanger (Brocchi's Cluster, Cr 399)", "衣架", "purple", "AST modern CoH（10 星）"),
    "雙筒": (COH, "雙筒望遠鏡", "binoculars", "要用雙筒望遠鏡", "white", ""),
    "象限儀": (flat(SEG["QuM"]), "Quadrans Muralis", "Mural Quadrant", "牆上的象限儀", "red",
            "AST modern QuM；Lalande 1795，象限儀座流星雨的名字由來"),
    "Formosa": ([FORMOSA], "Formosa", "Formosa (HD 100655)", "Formosa", "amber",
                "NameExoWorlds 2019；HIP 56508，獅子座，V 6.45"),
    "Sazum": ([FORMOSA], "Sazum", "HD 100655 b", "行星 Sazum：邵族語的「水」", "white", "NameExoWorlds 2019"),
    "獅子座": ([49669, 57632, 54872], "Leo", "Leo", "獅子座", "white", "IAU"),
    "大角": ([ARCT], "Arcturus", "Arcturus", "大角", "green", ""),
    "角宿一": ([SPICA], "Spica", "Spica", "角宿一", "green", ""),
    "大曲線": (flat(SEG["RH1"]), "Arc to Arcturus", "Arc to Arcturus", "春季大曲線", "green", "AST modern RH1"),
    "滿月": ((MOON["ra"], MOON["dec"]), "滿月", "Moon (99.7%)", "月亮（明早滿月）", "white",
           "PyEphem：6/18 22:00 高 32.6° 方位 155°，99.7%"),
}


# ══════════════════════════════════════════════════════════════════
# 六、建置
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    T = TERMS
    MAINS = [VEGA, ALTAIR, DENEB, DUBHE, ALKAID, ALPHERATZ, MU_SGR, ARCT, SPICA]

    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    x_of = lambda ra: ((LST0 - ra) + 180.0) % 360.0 - 180.0

    # ── 北盤構圖工具（畫布座標，盤心在 (0, yp)） ──
    def disc_xy(h, rot):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        keep = m.lst
        m.lst = LST0 - rot
        p = m.pos_disc(ra, dec, True)
        m.lst = keep
        return (p[0][0], p[0][1] + yp) if p else None

    def far(cx, cy, f):
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yp) for sx in (-1, 1) for sy in (-1, 1))

    def dfit(hips, rot, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None):
        pts = [p for p in (disc_xy(h, rot) for h in hips) if p]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        while far(cx, cy, f) > m.R_fill - 1.0:
            f *= 0.98
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    def horizon_y(x, rot):
        lst_obs = (LST0 - rot - 180.0) % 360.0
        best = None
        for ra, dec in horizon_points(PHI, lst_obs):
            p = disc_xy((ra, dec), rot)
            if p and (best is None or abs(p[0] - x) < abs(best[0] - x)) and p[1] < yp + 5:
                best = p
        return best[1]

    def hframe(cx, rot, fov, fh=0.17):
        cy = horizon_y(cx, rot) + (0.5 - fh) * fov * 16 / 9
        f = fov
        while far(cx, cy, f) > m.R_fill - 1.0:
            f *= 0.99
            cy = horizon_y(cx, rot) + (0.5 - fh) * f * 16 / 9
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    # ── 長圖構圖工具 ──
    def sfit(pts, fov, dx=0.0, dy=0.0, lim=None):
        xs = [x_of(S[h][0] if isinstance(h, int) else h[0]) for h in pts]
        ys = [(S[h][1] if isinstance(h, int) else h[1]) for h in pts]
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        L = (lim if lim is not None else m.Dr) - fov * 8 / 9 - 0.3
        cy = max(-L, min(L, cy))
        return (round(cx, 2), round(cy, 2), float(fov), 0.0)

    PP = {nm: disc_xy(h, R22) for nm, h in (("北極星", POLARIS), ("天樞", DUBHE), ("搖光", ALKAID),
                                            ("織女", VEGA), ("牛郎", ALTAIR), ("天津四", DENEB),
                                            ("大角", ARCT), ("角宿一", SPICA), ("箕宿三", KAUS),
                                            ("Formosa", FORMOSA), ("月亮", (MOON["ra"], MOON["dec"])))}
    print("\n── 22:00 北盤上位置（相對盤心） ──")
    for nm, (x, y) in PP.items():
        print(f"  {nm:7s} ({x:+7.1f}, {y - yp:+7.1f})  r={math.hypot(x, y - yp):6.1f}")
    print("── 長圖 x ──  " + "、".join(f"{nm} {x_of(S[h][0]):+.1f}" for nm, h in
                                    (("織女", VEGA), ("γ Sgr", 88635), ("ζ Sgr", 93506), ("衣架", 95487),
                                     ("室宿一", MARKAB), ("壁宿二", ALPHERATZ))) + f"、銀心 {x_of(GC[0]):+.1f}")

    # ── 構圖 ──
    F01a = (0.0, round(yp + 20.0, 2), 140.0, R20)
    F01b = dfit(flat(SEG["BDr"]) + [POLARIS], R20, pad=0.30, minfov=70.0)
    F02 = dfit(flat(SEG["UMa"]), R20, pad=0.17)
    F03 = dfit(flat(SEG["BDr"]) + [POLARIS], R22, pad=0.22, minfov=70.0)
    F04 = dfit(flat(SEG["STr"]), R22, pad=0.32)
    F05 = dfit(flat(SEG["NasW"] + SEG["NasT"]) + [DENEB], R22, pad=0.30)
    F06a = sfit(flat(SEG["GSP"]), 30.0, dy=0.0)
    F06b = sfit(flat(SEG["GSP"]), 24.0, dy=0.0)
    F07a = (0.0, -24.0, 40.0, 0.0)                        # T：走廊上，茶壺＋銀心＋斗宿三
    F07b = (0.0, -27.5, 28.0, 0.0)
    F08a = sfit(COH, 26.0, dx=-2.0)
    F08b = sfit(COH, 7.0)
    F09 = dfit(flat(SEG["QuM"]), R22, pad=0.25, minfov=40.0)
    F10 = dfit([VEGA, ALTAIR, DENEB, ARCT, DUBHE, ALKAID], R22, pad=0.08, minfov=110.0)
    F11 = dfit(flat(SEG["Leo"]) + [FORMOSA], R22, pad=0.10)
    F12a = hframe(PP["織女"][0] + 20.0, R22, 90.0)
    F12m = hframe(PP["天樞"][0] + 5.0, R22, 80.0)
    F12b = dfit([ALKAID, ARCT, SPICA], R22, pad=0.10, minfov=80.0)
    # 13 快轉一圈：Canva 旋轉只收 ±180，跨過 −180 那一格用「同畫面硬切」換成 +180（兩頁畫面完全相同），
    # 其餘每段 60°（＜170°，gen_canva_pages 不再拆頁、方向不會反）
    F13a = [(0.0, round(yp + 25.0, 2), 130.0, r) for r in (R22, -180.0)]
    F13b = [(0.0, round(yp + 25.0, 2), 130.0, r) for r in (180.0, 120.0, 60.0, 0.0, -60.0, -120.0, R22)]
    FR = dict(F01a=F01a, F01b=F01b, F02=F02, F03=F03, F04=F04, F05=F05, F06a=F06a, F06b=F06b, F07a=F07a,
              F07b=F07b, F08a=F08a, F08b=F08b, F09=F09, F10=F10, F11=F11, F12a=F12a, F12m=F12m, F12b=F12b, F13=F13a[0])
    print("\n── 構圖（cx, cy, fov, rot；盤 cy 為畫布座標，盤心 yp=%.2f） ──" % yp)
    for kk, v in FR.items():
        extra = f"角落距盤心 {far(*v[:3]):.1f}" if v[1] > m.Dr + 5 else f"上下緣 {v[1] - v[2]*8/9:+.1f}…{v[1] + v[2]*8/9:+.1f}"
        print(f"  {kk} {v}  {extra}")
    print("  旋轉：" + "、".join(f"{kk} {v:+.2f}°" for kk, v in ROT.items()))

    # ════════════════════ 標籤 ════════════════════
    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        v = [0.0, 0.0, 0.0]
        for h in a:
            r, d = math.radians(S[h][0]), math.radians(S[h][1])
            v[0] += math.cos(d) * math.cos(r); v[1] += math.cos(d) * math.sin(r); v[2] += math.sin(d)
        n = math.sqrt(sum(c * c for c in v))
        return {"ra": round(math.degrees(math.atan2(v[1], v[0])) % 360, 3),
                "dec": round(math.degrees(math.asin(v[2] / n)), 3)}

    def lab(key, fov, dx=0.0, dy=0.0, px=48, zh=None, two=False, px2=38, gap=None, col=None, top=None, at=None,
            disc=True):
        """一條標籤；px＝想要的 Canva 字級（1080 寬）。two＝上行 top（預設原文）＋下行中文；at＝改用別的錨點"""
        a, orig, en, zh0, c, _ = T[key]
        a = at or a
        s1 = px * fov / (m.fu * 1080)
        out = []
        ex = {"disc": True} if disc else {}
        if two:
            s2 = px2 * fov / (m.fu * 1080)
            g = gap if gap is not None else (s1 + s2) * m.fu * 0.62
            out.append(dict(anchor(a), text=top or orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy + g / 2, 2), key=key, **ex))
            out.append(dict(anchor(a), text=zh or zh0, color="white", size=round(s2, 3), dx=round(dx, 2),
                            dy=round(dy - g / 2, 2), key=key + "-zh", **ex))
        else:
            out.append(dict(anchor(a), text=zh or orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy, 2), key=key, **ex))
        return out

    LB = {}
    f = F01b[2]
    LB["北斗"] = lab("北斗", f, dx=0.0, dy=-9.0, px=50, two=True, px2=40, zh="北斗七星") \
        + lab("北極星", f, dx=0.0, dy=-4.0, px=36)
    f = F02[2]
    LB["大熊座"] = lab("大熊座", f, dx=0.0, dy=-18.0, px=48, two=True, px2=38) \
        + lab("星群", f, dx=-7.0, dy=6.0, px=44, two=True, px2=36, at=[ALKAID], top="北斗七星＝星群", zh="asterism")
    f = F03[2]
    LB["北斗星官"] = lab("北斗星官", f, dx=15.0, dy=-4.0, px=50, two=True, px2=36, top="北斗（中國星官）",
                     zh="管四季、定方向") + lab("大熊座", f, dx=7.0, dy=18.0, px=40, zh="IAU：大熊座（白框）",
                                          col="white")
    f = F04[2]
    LB["夏三角"] = (lab("織女", f, dx=0.0, dy=4.5, px=44, two=True, px2=34, top="織女 25 光年", zh="天琴座")
                 + lab("牛郎", f, dx=-2.0, dy=4.5, px=44, two=True, px2=34, top="牛郎 17 光年", zh="天鷹座")
                 + lab("天津四", f, dx=0.0, dy=-4.5, px=44, two=True, px2=34, top="天津四 1000＋光年", zh="天鵝座")
                 + lab("夏三角", f, dx=0.0, dy=0.0, px=46, col="blue"))
    f = F05[2]
    LB["兩隻鷹"] = (lab("Wāqiʿ", f, dx=0.0, dy=5.5, px=46, two=True, px2=36)
                 + lab("Ṭāʾir", f, dx=-2.0, dy=5.5, px=46, two=True, px2=36)
                 + lab("Dajāja", f, dx=0.0, dy=-5.5, px=46, two=True, px2=36))
    f = F06b[2]
    LB["四邊形"] = (lab("四邊形", f, dx=0.0, dy=-3.0, px=46, disc=False)
                 + lab("壁宿二", f, dx=0.0, dy=2.2, px=40, two=True, px2=32, top="壁宿二（仙女座）",
                       zh="1930 年起只屬仙女座", disc=False)
                 + lab("飛馬座", f, dx=0.0, dy=-9.0, px=36, zh="飛馬座", disc=False)
                 + lab("室宿", f, dx=-3.6, dy=0.0, px=40, two=True, px2=30, zh="營室", disc=False)
                 + lab("壁宿", f, dx=3.6, dy=0.0, px=40, two=True, px2=30, zh="東壁", disc=False))
    f = F07b[2]
    LB["茶壺"] = (lab("茶壺", f, dx=0.0, dy=-8.5, px=48, disc=False)
                + lab("蒸氣", f, dx=0.0, dy=5.0, px=36, disc=False)
                + lab("鴕鳥", f, dx=1.0, dy=-5.0, px=40, two=True, px2=32, disc=False)
                + lab("南斗", f, dx=-3.5, dy=6.5, px=42, disc=False, zh="南斗六星")
                + lab("斗宿三", f, dx=0.0, dy=1.6, px=34, disc=False))
    f = F08b[2]
    LB["衣架"] = (lab("衣架", f, dx=0.0, dy=1.3, px=50, two=True, px2=36, zh="倒掛的衣架（狐狸座）", disc=False)
                + lab("雙筒", f, dx=0.0, dy=-1.4, px=36, zh="雙筒望遠鏡才看得到", col="white", disc=False))
    f = F09[2]
    LB["象限儀"] = lab("象限儀", f, dx=0.0, dy=-8.0, px=44, two=True, px2=36, zh="牆上的象限儀（已退休）")
    f = F10[2]
    big = [h for h in S if S[h][2] < 2.2 and S[h][1] > -25 and h not in (VEGA, ALTAIR, DENEB)]
    iau = json.load(open(os.path.join(SC, "modern_iau", "index.json"), encoding="utf-8"))["common_names"]
    iau_name = lambda h: (iau.get(f"HIP {h}") or [{}])[0].get("english")
    LB["三個星名"] = [dict(hip=h, text=t, color="blue", size=round(44 * f / (m.fu * 1080), 3), dx=0.0,
                         dy=round(dyy, 2), key=t, disc=True)
                    for h, t, dyy in ((VEGA, "Vega", 3.6), (ALTAIR, "Altair", -3.6), (DENEB, "Deneb", 3.6))]
    LB["IAU星名"] = [dict(hip=h, text=iau_name(h), color="white", size=round(34 * f / (m.fu * 1080), 3), dx=0.0,
                        dy=3.0, key=iau_name(h), disc=True) for h in sorted(big) if iau_name(h)]
    LB["中國來源星名"] = [dict(hip=h, text=f"{p} {c}", color=TEAL, size=round(36 * f / (m.fu * 1080), 3), dx=7.0,
                         dy=-4.5, key=p, disc=True) for h, (p, c) in IAU_CN.items()]
    f = F11[2]
    LB["Formosa"] = (lab("Formosa", f, dx=0.0, dy=4.0, px=50, two=True, px2=36, zh="6.4 等・要用望遠鏡")
                     + lab("Sazum", f, dx=0.0, dy=-3.6, px=38)
                     + lab("獅子座", f, dx=0.0, dy=10.0, px=38))
    f = F12a[2]
    LB["今晚-大三角"] = lab("夏三角", f, dx=4.0, dy=6.0, px=46, zh="東方：夏季大三角", at=[VEGA])
    f = F12m[2]
    LB["今晚-北斗"] = lab("北斗", f, dx=0.0, dy=-21.0, px=46, zh="西北：北斗（斗柄朝上）")
    f = F12b[2]
    LB["今晚-大曲線"] = (lab("大曲線", f, dx=10.0, dy=0.0, px=46, zh="春季大曲線")
                     + lab("大角", f, dx=0.0, dy=3.5, px=40) + lab("角宿一", f, dx=0.0, dy=-3.5, px=40))
    label_sets = [(v, k2) for k2, v in LB.items()]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), ([ALPHERATZ], "壁宿二細圈", "ring"), ([MU_SGR], "斗宿三細圈", "ring")]
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_MAIN, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    LINES_KEY = dict({"L4": "星座連線", "界": "IAU邊界", "界熊": "IAU邊界-大熊座", "界三": "IAU邊界-天琴天鷹天鵝",
                      "界馬": "IAU邊界-飛馬仙女", "象": "連線-牆象限儀（虛線）", "衣點": "衣架放大星點",
                      "光": "Formosa光暈", "月": "滿月6月18日22時", "壁圈": "壁宿二細圈", "斗三": "斗宿三細圈"},
                     **LNAME)
    LINE_GROUPS = dict({"L4": LG_MAIN, "界": [], "界熊": [], "界三": [], "界馬": [], "象": [(SEG["QuM"], "red", 0.9)],
                        "衣點": [], "光": [], "月": [], "壁圈": [], "斗三": []}, **LG)

    # ════════════════════ 鏡頭 ════════════════════
    ls = lambda *n: list(n)
    hold = lambda fr: [fr]
    shots = [
        dict(code="01", kind="R", sec=11, north=True, frames=[F01a, F01b], layers=["界", "北斗"], labels=ls("北斗"),
             labels_start=[],
             vo="上週，天空被切成八十八塊；可是你最先認得的圖案，很多根本不在名單上。同一片星空，北斗七星——其實不是星座。",
             card="北斗七星不是星座？",
             note=f"北盤（台北 6/18 20:00 面北，{R20:+.1f}°；北極在下）fov 140 總覽：IAU 邊界（淡灰虛線，modern_iau 1875 邊界轉 J2000）"
                  "＋北斗（琥珀）→ 推近北斗；開場字卡"),
        dict(code="02", kind="R", sec=13, north=True, frames=[F01b, F02], layers=["北斗", "大熊", "界熊"],
             labels=ls("大熊座"), labels_start=ls("北斗"),
             overlay="C-A36-01_星座與星群", overlay_layers=["大熊層", "北斗層"],
             vo="北斗七星，只是大熊座的後半身和尾巴；星圖上的大熊，加上熊頭、熊腳要畫十幾顆星。這種大家都認得、卻不是正式星座的圖案，叫星群。",
             card="星群 asterism",
             note="推近大熊：大熊座連線（白，modern_iau 19 星）淡入、北斗（琥珀）不變、IAU 大熊座邊界（白虛線）；"
                  "迄格定格疊 C-A36-01（大熊座邊界裡的北斗：先大熊、再北斗＋「星群」）"),
        dict(code="03", kind="R", sec=13, north=True, frames=[F02, F03], layers=["北斗星官", "界熊"],
             labels=ls("北斗星官"), labels_start=ls("大熊座"),
             vo="有意思的是，在中國，北斗本來就是一個獨立的星官，管四季、定方向；到了 IAU，它只是星群。什麼算星座，要看你用誰的規則。",
             card="算不算星座，看規則",
             note=f"中國北斗星官（青 {TEAL}，只畫連線，不畫框）＋IAU 大熊座邊界同框；盤 20:00 → 22:00 逆時針 30.1°"
                  "（斗柄繞北極）；角落小字「IAU 國際天文學聯合會」用原生文字"),
        dict(code="04", kind="R", sec=18, north=True, frames=[F03, F04], layers=["夏三角", "界三"],
             labels=ls("夏三角"), labels_start=ls("北斗星官"),
             overlay="C-A36-02_夏季大三角的距離", overlay_layers=["近處層", "天津四層"],
             vo="夏天晚上最好認的星群，是夏季大三角：織女、牛郎、天津四，分屬天琴、天鷹、天鵝三個星座。看起來排在一起，距離卻差很多："
                "織女二十五光年、牛郎十七光年，天津四遠在一千光年以外。",
             card="25・17・1000＋光年",
             note="北盤（22:00）滑到東方：夏季大三角（藍）；天琴、天鷹、天鵝三座的 IAU 邊界各一色淡藍虛線（逐字稿寫「填淡色」，"
                  "SVG 改用邊界線）；迄格定格疊 C-A36-02（側視：織女、牛郎近處，天津四遠到畫面外）"),
        dict(code="05", kind="R", sec=19, north=True, frames=[F04, F05], layers=["夏三角", "兩隻鷹"],
             labels=ls("兩隻鷹"), labels_start=ls("夏三角"),
             vo="織女的英文 Vega，來自阿拉伯文「俯衝的鷹」；牛郎 Altair，是「飛翔的鷹」——在阿拉伯，它們各帶兩顆小星，本身就是兩個星群。"
                "天津四 Deneb，是「母雞的尾巴」。三個英文名字，全都源自阿拉伯文。",
             card="英文星名源自阿拉伯文",
             note="推近大三角：蘇菲星群 NasW（織女＋ε¹、ζ¹ Lyr）、NasT（河鼓二＋β、γ Aql）（綠，各 2 筆）隨「兩個星群」亮起；"
                  "標籤 النسر الواقع／النسر الطائر／ذنب الدجاجة（RTL 整形）＋中譯"),
        dict(code="06", kind="Z", sec=16, north=True, frames=[F06a, F06b], layers=["四邊形", "界馬", "室壁", "壁圈"],
             labels=ls("四邊形"),
             vo="星群常常跨好幾個星座。秋天的飛馬大四邊形，有一個角其實歸仙女座：壁宿二以前兩邊都算，一九三〇年劃界時，只分給了仙女。"
                "在中國，這個四邊形是室宿和壁宿。",
             card="四邊形一角屬仙女座",
             note="【換組】北盤 → 長圖（gen_canva_pages 自動插歸位／換組／下移頁）；長圖往東捲到飛馬座（S 動作；上緣 +43°＞D_s 41，"
                  "用 Z 驗證、不出 D_r）；角落小標「秋季星空（6/18 晚上 22:11 起才陸續升起）」；大四邊形（琥珀）、飛馬與仙女邊界（白虛線）、"
                  "壁宿二細圈閃一下；中國室宿＋壁宿（青）疊上"),
        dict(code="07", kind="T", sec=17, north=True, frames=[F07a, F07b], layers=["茶壺", "鴕鳥", "南斗", "斗三"],
             labels=ls("茶壺"),
             vo="人馬座裡還有一把茶壺，壺嘴冒出的蒸氣，就是銀河中心那一段。在古阿拉伯，壺嘴一帶是幾隻下河喝水的鴕鳥；"
                "茶壺的把手和壺蓋，再加上壺外一顆星，在中國就是南斗六星。",
             card="茶壺＝鴕鳥＋南斗",
             note="長圖走廊 x=0（lst 278）上的茶壺：茶壺（琥珀，8 星）＋銀河層（Canva 把 L1 透明度調高）；壺嘴一帶 A-19 鴕鳥（綠，γ δ ε η）；"
                  "把手＋壺蓋頂（φ σ τ ζ λ）疊中國斗宿（青），「壺外一顆星」時點亮斗宿三 μ Sgr 細圈，連成六星；"
                  "畫面下緣伸進走廊內的南縫合帶（南冕座一帶，連續天空）"),
        dict(code="08", kind="Z", sec=14, north=True, frames=[F08a, F08b], layers=["衣架", "衣點"],
             labels=ls("衣架"), labels_start=[],
             overlay="C-A36-03_衣架的真實距離",
             vo="有些星群要用雙筒望遠鏡：狐狸座裡有一個倒掛的衣架，六顆星一根橫桿，四顆星一個鉤——它們其實遠近不一，只是從地球看過去，剛好排在一起。",
             card="倒掛的衣架",
             note="長圖：滑到天箭—狐狸 fov 26 → 推近衣架 fov 7（衣架 10 星 V 5.2–7.2 不在星點層，用「衣架放大星點」層；連線紫色細線）；"
                  "「遠近不一」時疊 C-A36-03（側視，Gaia DR3 視差）"),
        dict(code="09", kind="R", sec=11, north=True, frames=[F09], layers=["象"], labels=ls("象限儀"),
             overlay="C-A36-04_查理的橡樹",
             vo="上週那些被淘汰的星座，有的也退休成了星群：牆上的象限儀、查理的橡樹，在星空軟體裡還找得到。",
             card="退休的星座",
             note="【換組】長圖 → 北盤（22:00）：牆象限儀 Quadrans Muralis（紅虛線，CSV QuM 16 星，牧夫—天龍—武仙之間）；"
                  "「查理的橡樹」時疊 C-A36-04（南天小窗：船底—船帆—半人馬 Robur Carolinum，紅虛線；台北地平線以下的部分標「台灣看不全」）"),
        dict(code="10", kind="R", sec=20, north=True, frames=[F09, F10], layers=["夏三角"],
             labels=ls("三個星名", "IAU星名", "中國來源星名"), labels_start=[],
             vo="星群沒有官方名字，但星星有：前面的 Vega、Altair、Deneb，都是 IAU 核定的正式星名。二〇一六年，IAU 成立星名工作小組，"
                "開始有系統地核定星名；第二年，就收進了中國、澳洲原住民、玻里尼西亞的名字。",
             card="2016：IAU 替星星命名",
             note="北盤拉遠：Vega、Altair、Deneb 三個標籤先亮（回扣 05 鏡）→ IAU 星名層（白，Stellarium modern_iau，2.2 等以上）→ "
                  "中國來源的 IAU 星名（青：Taiyangshou 太陽守、Xuange 玄戈、Zhou 周）。批次（2016／2017）本環境沒有 WGSN 公告日期表，不分批"),
        dict(code="11", kind="R", sec=15, north=True, frames=[F10, F11], layers=["獅子", "光"],
             labels=ls("Formosa"), labels_start=ls("三個星名", "IAU星名", "中國來源星名"),
             vo="其中有一顆和台灣有關：二〇一九年，獅子座一顆帶著行星的恆星，被命名為 Formosa；它的行星叫 Sazum——邵族語的「水」，也是日月潭一帶的老地名。",
             card="Formosa・Sazum",
             note="北盤滑到獅子座（IAU 連線，白細）；Formosa＝HIP 56508（V 6.45，光暈標記）；角落小字「6.4 等，要用望遠鏡」；"
                  "日月潭照片需美宣另尋授權圖（或只用文字）"),
        dict(code="12", kind="R", sec=22, north=True, horizon=[PHI], frames=[F12a, F12m, F12b],
             layers=["北斗", "夏三角", "大曲線"],
             labels=ls("今晚-北斗"), labels_start=ls("今晚-大三角"), labels_end=ls("今晚-大曲線"),
             overlay="C-A36-05_六月晚上的五個星群",
             vo="今晚十點：東方的夏季大三角正在升高；西北方，北斗斗柄朝上，順著斗柄的弧線拉過去，先是大角、再到角宿一，這條春季大曲線掛在西邊；"
                "東南方低空是茶壺，滿月就在旁邊。月光很亮，銀河和衣架，等兩週後新月再看。",
             card="今晚 10 點・明早滿月",
             note=f"北盤台北 6/18 22:00 面北（{R22:+.1f}°，山＝北方地平線）：東方大三角 → 西北北斗 → 往上滑到大角—角宿一（大曲線，綠）"
                  "（盤上北極在下，南方的天在畫面上方）；「東南方低空是茶壺」起疊 9:16 圖卡 C-A36-05（台北 22:00 全天，"
                  "五個星群＋滿月，可存圖）——茶壺（r 147–158）＋月亮（r 150）在填滿圓邊緣，盤上框不進同一格，改由圖卡呈現"),
        dict(code="13", kind="R", sec=1, north=True, horizon=[PHI], frames=F13a, layers=[], labels=[],
             vo="",
             card="下集｜毛利 Matariki",
             note=f"北盤拉遠到 fov 130，從 22:00（{R22:+.1f}°）開始逆時針快轉：先轉到 −180°（逐字稿 13 鏡的第 1 秒；旁白在 13b）"),
        dict(code="13b", kind="R", sec=7, north=True, horizon=[PHI], frames=F13b, layers=[], labels=[], cut=True,
             vo="下週五，紐西蘭放 Matariki 假：昴宿在黎明升起，就是新年。",
             card="下集｜毛利 Matariki",
             note="【同畫面硬切】−180° 與 +180° 是同一個畫面（Canva 旋轉只收 ±180），換頁不設轉場；之後每頁 −60° 逆時針轉完一整圈"
                  "回到 22:00（連線、標籤收掉）；端卡「下集見｜毛利 Matariki：星星升起就是新年」＋追蹤 CTA"),
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
    for sh in shots:                                # 長圖鏡頭上下緣不出 D_r（本集自訂規則；T 在走廊內除外）
        if sh["kind"] in ("Z", "S"):
            for (cx, cy, fov, rot) in sh["frames"]:
                if abs(cy) + fov * 8 / 9 > m.Dr + 1e-6:
                    print(f"  ✗ {sh['code']}：畫面上下緣出 D_r（會看到填滿圓的重複天區）")
    print("  判斷後接受的 ⚠：" + WARN_OK)

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            if sh["kind"] == "R":
                ew = 2 * m.R_fill / fov * 1080
                off_ = (round(-cx / fov * 1080), round((cy - m.y_pole) / fov * 1080))
                use = "北盤圖層組（置中）"
            else:
                ew = 360.0 / fov * 1080
                off_ = (round(-cx / fov * 1080), round(cy / fov * 1080))
                use = "大畫布圖層組"
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": use, "元素寬px": round(ew), "位移X px": off_[0],
                         "位移Y px": off_[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    # ── 數字核對（逐字稿星空對時表、考據備忘） ──
    print("\n── 數字核對 ──")
    for kk, v in LST_AT.items():
        print(f"  {T_TPE[kk]} LST {v:.2f} → 北盤 {ROT[kk]:+.2f}°")
    for nm, h in (("織女", VEGA), ("牛郎", ALTAIR), ("天津四", DENEB), ("天樞", DUBHE), ("搖光", ALKAID),
                  ("大角", ARCT), ("角宿一", SPICA), ("箕宿三", KAUS), ("斗宿四", 92855), ("ζ Sgr", 93506),
                  ("衣架 HIP95487", 95487), ("Formosa", FORMOSA), ("π Her", 84380)):
        a, z = altaz(*S[h][:2], "2027/6/18 22:00")
        print(f"  22:00 {nm} 高 {a:5.1f}° 方位 {z:5.1f}°")
    print(f"  22:00 月亮 高 {MOON['alt']:.1f}° 方位 {MOON['az']:.1f}° 月相 {MOON['phase']:.1f}% 在 {MOON['con']}；"
          f"J2000 RA {MOON['ra']:.2f} Dec {MOON['dec']:+.2f}；離箕宿三 {sep((MOON['ra'], MOON['dec']), S[KAUS][:2]):.1f}°")
    m21 = moon_at("2027/6/18 21:00")
    print(f"  21:00 月亮在 {m21['con']}，離銀心 {sep((m21['ra'], m21['dec']), GC):.1f}°、離箕宿三 "
          f"{sep((m21['ra'], m21['dec']), S[KAUS][:2]):.1f}°")
    print(f"  邊長：織女—牛郎 {sep(S[VEGA][:2], S[ALTAIR][:2]):.1f}°、織女—天津四 {sep(S[VEGA][:2], S[DENEB][:2]):.1f}°、"
          f"牛郎—天津四 {sep(S[ALTAIR][:2], S[DENEB][:2]):.1f}°；天樞—搖光 {sep(S[DUBHE][:2], S[ALKAID][:2]):.1f}°；"
          f"搖光→大角 {sep(S[ALKAID][:2], S[ARCT][:2]):.1f}°、大角→角宿一 {sep(S[ARCT][:2], S[SPICA][:2]):.1f}°；"
          f"μ—λ Sgr {sep(S[MU_SGR][:2], S[LAM_SGR][:2]):.2f}°")
    gs = flat(SEG["GSP"])
    print("  四邊形邊長：" + "、".join(f"{sep(S[a][:2], S[b][:2]):.1f}°" for a, b in zip(SEG["GSP"][0], SEG["GSP"][0][1:])))
    print(f"  Formosa（HIP 56508）RA {S[FORMOSA][0]:.2f} Dec {S[FORMOSA][1]:+.2f} V {S[FORMOSA][2]:.2f}；"
          f"衣架 V {min(S[h][2] for h in COH):.2f}–{max(S[h][2] for h in COH):.2f}")

    terms = {}
    for key, (a, orig, en, zh, col, note) in T.items():
        terms[key] = dict(hips=a if isinstance(a, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                          顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI, "moon": MOON},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV_LINES = LG_MAIN + LG["兩隻鷹"] + LG["南斗"] + LG["鴕鳥"] + LG["室壁"] + LG["北斗星官"]
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=PREV_LINES,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    import make_a21_v4 as A21
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_MAIN)
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k2 in sh.get("layers", []) for x in LINE_GROUPS.get(k2, [])]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])
))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    A21.sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
                title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    qa = os.environ.get("QA_DIR")                   # QA 用放大牆（不進 repo）
    if qa:
        for sh, g, labs in walls:
            m.sb_grid(os.path.join(qa, f"qa_{sh['code']}.png"), [sh], line_groups=g, labels=labs,
                      cols=len(sh["frames"]), cell_in=4.2, dpi=90, title="")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
