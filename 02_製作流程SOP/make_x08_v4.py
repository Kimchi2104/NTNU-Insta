# -*- coding: utf-8 -*-
"""X-08 第一季完結：同一片星空的 27 種目光｜大畫布 v4.6（全天北盤大混剪＋南盤三段，收官集）

論點：每個文化都把自己的日子寫上天。02–08 鏡每 1–2 句換一個文化的連線層（照各集定稿的那一層，
不重畫、不改連線）；09 四趟環球；10 算一算（概念圖）；11、11b 兩則勘誤；12 一片彩色網；13 今晚；14 第二季七夕。

來源（全部沿用各集 make 腳本的連線資料，import 進來，不另抄 HIP）：
  中國 青龍＝Stellarium 新版 chinese 角亢氐房心尾箕；紫微垣＝H-元宵（make_hyx_v4）；白虎＝A-12；天床 214、天廚 212、
  參宿 003、廁 047、屎 188＝Stellarium 新版 chinese。韓國＝Stellarium 新版 korean 全部 312 星官（天象列次分野之圖）。
  日本和名＝A-05 SHUKU（奎 とかきぼし、婁 たたらぼし、參 からすきぼし，只標 A-05 v2 07 鏡講過的三宿）。
  蒙古 金樁＝A-07；埃文基 駝鹿的腳／獵人＝X-03（照 A-08 v2）；因紐特 馴鹿與鎖骨＝A-14；夏威夷 Manaiakalani＝A-09；
  東加 Toloa＝A-10；阿努塔 Manu＝A-11；毛利 Matariki＝昴宿（A-33）；阿拉伯 月站＝A-32；印度 Nakṣatra＝A-28；
  埃及 Sopdet＝A-18；蘇菲 仙女座＋大魚＝A-34；呂埃勒＝A-30；納瓦荷＝A-16（只放名字）；黑腳族＝A-17；
  圖卡諾 Yai＝A-24；白俄 Іллёў воз＝A-22；羅馬尼亞 牧羊人和羊、井和水槽＝A-23；北歐 狼嘴＝A-15；
  卡米拉羅伊／尤瓦萊 鴯鶓暗帶＝A-31 自繪暗帶多邊形（不描 Stellarium 插圖）；布吉斯／曼達爾 魟魚＝A-26／A-27；
  北斗 船＝A-27（布吉斯的船）、漁網＝A-26（mandar 漁網，連進天龍）。
  天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，UTC+8；1010 hPa、15°C；恆星 J2000）。
逐字稿：04_腳本庫/X-08-第一季完結同一片星空的27種目光-逐字稿-v1.md。

參數（依本集逐字稿重新評估，不照抄範例）
  D_s = 41、D_r = 45、D_fill = −45 → k 1.2732、R_fill 171.89（盤寬 ÷ 畫布寬 0.955，不是同寬）。決定因素：
    逐字稿「盤面設定」要北盤畫到赤緯 −45°（同 A-35／A-36）：參宿南緣、天狼 −16.7、廁（天兔）−17.8…−22.4、
    月站 al-Shawla −37 都在北盤上；|x_t|＋R_fill ≤ 180 ✓。南盤本體 ≤ −45：南十字、煤袋、老人星；
    南盤填滿圈到 +45：天蠍、人馬、南河三（阿努塔 Manu）都在南盤上。
  lst = 70 → 北盤 0° 時，赤經 70°（金牛—獵戶）在盤心正下方＝與長圖同一個正立方向；
    台北 7/9 20:00 = +21.2°、22:40 = −18.9°、8/8 21:00 = −23.4°（北盤 rot＝−((LST＋180−70) mod 360)），
    整集北盤旋轉都落在 ±180 內，只有 12 鏡「慢轉一整圈」跨 ±180（拆 12／12b，那一頁同畫面硬切，同 A-36 13 鏡）。
  x_tN = x_tS = 0（Canva 可水平置中）。

鏡頭路線（逐字稿 17 鏡 → 本檔 38 鏡：一鏡只能開一組連線層，所以每換一個文化拆一鏡；秒數照字數分，
  每一個逐字稿鏡頭的秒數總和不變，總長 234 秒）
  整集只用盤：北盤為主，南盤三段（02 青龍、04 太平洋、08 鴯鶓＋魟魚），盤⇄盤一律【硬切】（換文化＝換一個地方）。
  逐字稿畫面欄原寫長圖的 04 末–05（昴宿、月站、天狼）、09（昴宿→腰帶→銀河）、11（大三角）、11b（參宿、廁）
  全部改在全天北盤上做：這些星都在北盤 −45° 以內，盤⇄長圖每換一次要多 3–4 頁轉場；09 鏡的北斗也因此直接在盤上
  （逐字稿原寫「北斗不在長圖帶內，疊 X-03 縮圖」）。02 鏡青龍尾宿 −43° 在北盤只能貼著盤緣、形狀被拉長 2 倍，
  改在南盤（尾宿離南天極 47°，正立不變形）。13 鏡月亮與大三角照逐字稿在北盤。
"""
import os, sys, json, math, csv, re, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import COLORS
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "X-08"
ROOT = os.path.join(BASE, "05_素材/X-08_第一季完結")
OUT = os.path.join(ROOT, "_v4大畫布")
LST0 = 70.0
D_S, D_R, D_FILL = 41.0, 45.0, -45.0
TPE = (25.0330, 121.5654)
PHI = 25.03
TEAL = "#3D8B7D"          # 青龍（逐字稿指定，同 A-01）
WHITE2 = "#E8ECF5"        # 白虎（同 A-36 灰白）

WARN_OK = """
  全集都是盤（R）：與大畫布互切的頁不存在（整集不換長圖），「切點」⚠ 不影響；盤⇄盤（北⇄南）都是【硬切】新構圖。
"""

# ══════════════════════════════════════════════════════════════════
# 〇、各集連線（import 各集 make 腳本的模組層資料；不執行它們的 build）
# ══════════════════════════════════════════════════════════════════
with contextlib.redirect_stdout(io.StringIO()):
    import make_a05_v4 as A05, make_a07_v4 as A07, make_a09_v4 as A09, make_a10_v4 as A10, make_a11_v4 as A11
    import make_a12_v4 as A12, make_a14_v4 as A14, make_a15_v4 as A15, make_a16_v4 as A16, make_a17_v4 as A17
    import make_a18_v4 as A18, make_a22_v4 as A22, make_a23_v4 as A23, make_a24_v4 as A24, make_a26_v4 as A26
    import make_a27_v4 as A27, make_a28_v4 as A28, make_a30_v4 as A30, make_a31_v4 as A31, make_a32_v4 as A32
    import make_a34_v4 as A34, make_x03_v4 as X03, make_hyx_v4 as HYX

SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_new(cu):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", []) if l and not isinstance(l[0], list)]
        out[c["id"].split()[-1]] = dict(segs=[s for s in segs if len(set(s)) >= 2], name=c["common_name"])
    return out


S0 = dict(G.load_stars(BASE))
CH = load_new("chinese")
KO = load_new("korean")
CH_BY_NATIVE = {v["name"].get("native"): k for k, v in CH.items()}
QL = [CH_BY_NATIVE[n] for n in ("角宿", "亢宿", "氐宿", "房宿", "心宿", "尾宿", "箕宿")]


def recolor(lg, col, w=None):
    """各集的 (segs, 顏色, 線寬) 換成本集的顏色（逐字稿畫面欄指定）；線寬沿用，除非另給"""
    return [(g[0], col, w if w is not None else (g[2] if len(g) > 2 else 1.0)) for g in lg]


def segs_of(lg):
    return [s for g in lg for s in g[0]]


def stars_of(lg):
    return sorted({h for s in segs_of(lg) for h in s})


POLARIS, VEGA, ALTAIR, DENEB, SIRIUS, ALCYONE, ANTARES, ALDEBARAN = 11767, 91262, 97649, 102098, 32349, 17702, 80763, 21421
DIPPER = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
BELT = [25930, 26311, 26727]
PLEIADES = [17499, 17531, 17573, 17579, 17608, 17702, 17847, 17851]
CAS_W = [746, 3179, 4427, 6686, 8886]
CRUX = [61084, 60718, 62434, 59747]

LG = {
    "大三角": [([[VEGA, DENEB, ALTAIR, VEGA]], "blue", 1.1)],
    "青龍": [(CH[k]["segs"], TEAL, 1.1) for k in QL],
    "紫微": recolor(HYX.LG_WALLS, "amber"),
    "白虎": recolor(A12.LG_SEVEN, WHITE2),
    "韓國": [([s for v in KO.values() for s in v["segs"]], "blue", 0.7)],
    "駝鹿": recolor(X03.LG_ELK, "green") + recolor(X03.LG_HUNT, "green"),
    "因紐特": recolor(A14.LG_NORTH, "amber"),
    # A-09 Manaiakalani 有兩段：天蠍的魚鉤＋往北穿過夏季大三角的長線；本集只要南天的魚鉤（04 鏡在南盤）
    "夏威夷": [([sg for sg in A09.SL["MAN"] if max(S0[h][1] for h in sg if h in S0) < -10.0], "amber", 1.1)],
    "東加": recolor(A10.LG_DUCK, "green", 1.1),
    "阿努塔": recolor(A11.LG_MANU, "blue", 1.1),
    "月站": recolor(A32.LG_ST, "amber"),
    "印度": recolor(A28.LG_NAK, "blue"),
    "蘇菲": recolor(A34.LG["仙女"], "blue") + recolor(A34.LG["大魚"], "green"),
    "呂埃勒": recolor(A30.LG_RU, "white", 0.8),
    "黑腳": recolor(A17.LG_SEVEN, "amber"),
    "圖卡諾": recolor(A24.LG_YAI, "amber"),
    "白俄": recolor(A22.LG_FIRE, "amber"),
    "羅馬尼亞": recolor(A23.LG_SHEP, "green") + recolor(A23.LG_WELL, "green"),
    "北歐": recolor(A15.LG_WOLF, "red", 1.1),
    "魟魚": recolor(A26.LG_RAY, "amber", 2.2) + recolor(A27.LG_RAY, "blue", 0.9),
    "船網": recolor(A27.LG_BSHIP, "amber", 1.1) + recolor(A26.LG_NET, "blue", 1.1),
    "腰帶": [([BELT], WHITE2, 1.0)],
    "北斗": [([DIPPER], WHITE2, 1.0)],
    "床廚": [(CH["214"]["segs"] + CH["212"]["segs"], "red", 1.1)],
    "參廁": [(CH["003"]["segs"], "amber", 1.0), (CH["047"]["segs"] + CH["188"]["segs"], "purple", 1.1)],
}
LNAME = {k: f"連線-{v}" for k, v in {
    "大三角": "夏季大三角", "青龍": "青龍（中國）", "紫微": "紫微垣（中國）", "白虎": "白虎（中國）",
    "韓國": "天象列次分野之圖（韓國）", "駝鹿": "駝鹿與獵人（埃文基）", "因紐特": "馴鹿與鎖骨（因紐特）",
    "夏威夷": "Manaiakalani（夏威夷）", "東加": "Toloa野鴨（東加）", "阿努塔": "Manu大鳥（阿努塔）",
    "月站": "28月站（阿拉伯）", "印度": "Nakshatra（印度）", "蘇菲": "仙女座與大魚（蘇菲）", "呂埃勒": "呂埃勒1786",
    "黑腳": "七兄弟（黑腳族）", "圖卡諾": "Yai美洲豹（圖卡諾）", "白俄": "以利亞的車（白俄）",
    "羅馬尼亞": "牧羊人與井（羅馬尼亞）", "北歐": "狼嘴（北歐）", "魟魚": "魟魚（布吉斯＋曼達爾）",
    "船網": "船與漁網（布吉斯／曼達爾）", "腰帶": "獵戶腰帶", "北斗": "北斗", "床廚": "天床天廚",
    "參廁": "參宿與廁"}.items()}
# 12 鏡：一片彩色網（各文化連線同時疊上；不疊納瓦荷、韓國全圖太密也不疊；圖卡諾只用 Stellarium 公開連線＝A-24 Yai）
WEB_KEYS = ["青龍", "紫微", "白虎", "駝鹿", "因紐特", "夏威夷", "東加", "阿努塔", "月站", "印度", "蘇菲", "黑腳",
            "圖卡諾", "白俄", "羅馬尼亞", "北歐", "魟魚", "船網", "大三角"]
LG["網"] = [g for k in WEB_KEYS for g in LG[k]]
LNAME["網"] = "連線-一片彩色網（12鏡）"
CUSTOM_KEYS = {"鴯鶓": "暗帶-鴯鶓（卡米拉羅伊）", "月": "月亮0709-2000", "暈": "單星光暈"}

MAINS = sorted({h for k, g in LG.items() if k not in ("韓國", "呂埃勒", "網") for h in stars_of(g)}
               | {POLARIS, SIRIUS, ALCYONE, ANTARES, ALDEBARAN})
HALO = [POLARIS, VEGA, ALTAIR, DENEB, SIRIUS, ALCYONE, ANTARES]


# ══════════════════════════════════════════════════════════════════
# 一、星曆
# ══════════════════════════════════════════════════════════════════
def _obs(when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.elevation = 0
    o.pressure, o.temp = 1010, 15
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    return o


def lst_at(when):
    return math.degrees(_obs(when).sidereal_time())


def norm(r):
    r = (r + 180.0) % 360.0 - 180.0
    return 180.0 if abs(r + 180.0) < 1e-9 else r


def rot_n(lst_obs):
    """北盤面北：rot＝−((LST＋180−lst) mod 360)"""
    return round(norm(-((lst_obs + 180.0 - LST0) % 360.0)), 2)


def rot_s(lst_obs):
    """南盤面南：上中天在盤心正上方，順時針＝時間前進"""
    return round(norm(lst_obs - LST0), 2)


def altaz(radec, when):
    import ephem
    o = _obs(when)
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(radec[0]), math.radians(radec[1]); s._epoch = ephem.J2000
    s.compute(o)
    return round(math.degrees(s.alt), 1), round(math.degrees(s.az), 1)


def moon_radec(when):
    import ephem
    o = _obs(when)
    b = ephem.Moon(); b.compute(o)
    eq = ephem.Equatorial(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=ephem.J2000)
    return math.degrees(eq.ra), math.degrees(eq.dec), math.degrees(b.alt), math.degrees(b.az), b.phase


T = {"0709": "2027/7/9 20:00", "0709b": "2027/7/9 22:40", "0808": "2027/8/8 21:00"}
LST_AT = {k: lst_at(v) for k, v in T.items()}
MOON = None


def _uv(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return np.array([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])


def _rd(v):
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(float(v[2])))


def mean_ra(S, hips):
    return _rd(sum(_uv(*S[h][:2]) for h in hips if h in S))[0]


# ══════════════════════════════════════════════════════════════════
# 二、自訂圖層
# ══════════════════════════════════════════════════════════════════
def custom_layers(m):
    pur, wht = COLORS["purple"], COLORS["white"]

    def emu(s, pos, runs, disc):
        for poly in A31.DARK_ALL:
            rs = runs(poly)
            if disc is not None:
                s.poly_fill(rs, fill=pur, opacity=0.30)
            s.polylines(rs, stroke=pur, w=m.lw * 0.45, opacity=0.85)

    def moon(s, pos, runs, disc):
        ra, dec = MOON[:2]
        for p in pos(ra, dec):
            for rr, op in ((3.4, 0.06), (2.4, 0.10), (1.6, 0.18)):
                s.circle(p[0], p[1], rr, fill=wht, opacity=op)
            s.circle(p[0], p[1], 1.05, fill="#F4F1E6", opacity=0.97)

    return [("暗帶-鴯鶓（卡米拉羅伊）", emu), ("月亮0709-2000", moon)]


def write_custom(m, layers, discs=False):
    for name, fn in layers:
        if not discs:
            s = m._new()
            fn(s, lambda ra, dec: m.pos_all(ra, dec), m.runs_all, None)
            m._write(s, name)
        else:
            for north in (True, False):
                s = m._new_disc()
                fn(s, lambda ra, dec, n=north: m.pos_disc(ra, dec, n), lambda pts, n=north: m._runs_disc(pts, n), north)
                m._write_disc(s, north, name)


def disc_xy(m, ra, dec, rot, north):
    q = m.to_disc_local(m.p_disc(m.xw(ra), dec, north), north)
    a = math.radians(-rot)
    x = q[0] * math.cos(a) - q[1] * math.sin(a)
    y = q[0] * math.sin(a) + q[1] * math.cos(a)
    return x, (m.y_pole if north else -m.y_pole) + y


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋數字；本集旁白沒有外文）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyāēīōū]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、建置
# ══════════════════════════════════════════════════════════════════
def build():
    global MOON
    S = dict(G.load_stars(BASE))
    MOON = moon_radec(T["0709"])
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k, RF = m.y_pole, m.k, m.R_fill

    def pt(h):
        return S[h][:2] if isinstance(h, int) else h

    def dpts(hips, rot, north):
        return [disc_xy(m, *pt(h), rot, north) for h in hips]

    def safe(cx, cy, f, north):
        yc = yp if north else -yp
        return max(math.hypot(cx + sx * f / 2, cy + sy * f * 8 / 9 - yc)
                   for sx in (-1, 1) for sy in (-1, 1)) <= RF - 1.0

    def fit(hips, rot, north, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, fov=None, noshrink=False):
        """框住 hips；出了填滿圓就先往盤心挪（主角仍在框內），挪不動才縮 fov（noshrink：不准縮，直接失敗）"""
        pts = dpts(hips, rot, north)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        # 山的剪影蓋住頁面下緣約 16%：主角放在上面 84% 的中間（畫面中心往下挪 7% 畫面高）
        f = fov or max(minfov, (max(xs) - min(xs)) * (1 + 2 * pad), (max(ys) - min(ys)) * (1 + 2 * pad) / 0.84 * 9 / 16)
        yc = yp if north else -yp
        for _ in range(400):
            cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy - 0.07 * f * 16 / 9
            for _ in range(80):
                if safe(cx, cy, f, north):
                    return (round(cx, 2), round(cy, 2), round(f, 1), rot)
                d = math.hypot(cx, cy - yc)
                ncx, ncy = cx - cx / d, cy - (cy - yc) / d
                inside = (min(xs) >= ncx - f / 2 and max(xs) <= ncx + f / 2 and
                          min(ys) >= ncy - f * 8 / 9 * 0.70 and max(ys) <= ncy + f * 8 / 9)
                if not inside:
                    break
                cx, cy = ncx, ncy
            if noshrink:
                raise RuntimeError("fit 要縮 fov")
            f *= 0.98
        raise RuntimeError("fit 失敗")

    def wide(rot, north, fov=None, dy=0.0):
        f = fov or 170.0
        while not safe(0.0, (yp if north else -yp) + dy, f, north):
            f -= 0.5
        return (0.0, round((yp if north else -yp) + dy, 2), f, rot)

    def bottom_n(hips):           # 北盤：主角轉到盤心正下方（與長圖同一個正立方向）
        return rot_n(mean_ra(S, hips) + 180.0)

    def top_s(hips):              # 南盤：主角轉到盤心正上方（正立）
        return rot_s(mean_ra(S, hips))

    def bestrot(hips, north, near, span=80.0, pad=0.10):
        best = None
        for r in np.arange(max(-178.0, near - span), min(178.0, near + span) + 0.1, 2.0):   # 不跨 ±180（Canva 會反轉）
            r = float(r)
            try:
                fr = fit(hips, round(r, 1), north, pad=pad, minfov=10.0, noshrink=True)
            except RuntimeError:
                continue
            if best is None or fr[2] < best[2] - 0.5:
                best = fr
        return best[3]

    # ── 旋轉 ──
    R = {}
    R["0709"], R["0709b"], R["0808"] = rot_n(LST_AT["0709"]), rot_n(LST_AT["0709b"]), rot_n(LST_AT["0808"])
    R["白虎"] = bestrot(stars_of(LG["白虎"]), True, bottom_n(stars_of(LG["白虎"])), span=100.0)
    R["青龍"] = bestrot(stars_of(LG["青龍"]), False, top_s(stars_of(LG["青龍"])), span=100.0)
    R["金樁"] = round(R["白虎"] + 15.0, 2)
    R["駝鹿"] = bestrot(DIPPER, True, R["金樁"] + 20.0, span=50.0)
    R["因紐特"] = bestrot(stars_of(LG["因紐特"]), True, R["駝鹿"] + 20.0, span=50.0)
    R["太平洋"] = rot_s(mean_ra(S, CRUX + stars_of(LG["夏威夷"])))
    R["昴宿"] = bottom_n(PLEIADES)
    R["天狼"] = bottom_n([SIRIUS] + BELT)
    R["蘇菲"] = bottom_n(stars_of(LG["蘇菲"]))
    R["納瓦荷"] = bestrot(DIPPER + CAS_W + [POLARIS], True, R["蘇菲"] - 20.0)
    R["黑腳"] = bestrot(DIPPER + PLEIADES, True, R["納瓦荷"] - 15.0)
    R["圖卡諾"] = bestrot(stars_of(LG["圖卡諾"]), True, R["黑腳"] - 15.0)
    R["白俄"] = bestrot(DIPPER, True, R["圖卡諾"] - 15.0)
    R["羅馬尼亞"] = bestrot(stars_of(LG["羅馬尼亞"]), True, R["白俄"] - 15.0)
    R["北歐"] = bottom_n(stars_of(LG["北歐"]))
    R["魟魚"] = top_s(stars_of(LG["魟魚"]))
    R["船網"] = bestrot(stars_of(LG["船網"]), True, R["北歐"] - 20.0)
    R["腰帶"] = bottom_n(BELT)
    R["北斗09"] = bestrot(DIPPER, True, R["腰帶"] - 30.0)
    R["銀河"] = bestrot([DENEB, VEGA, ALTAIR, 90185, 89931], True, R["北斗09"] - 30.0)
    R["大三角"] = bestrot([DENEB, VEGA, ALTAIR], True, R["銀河"])
    R["床廚"] = bestrot(stars_of(LG["床廚"]) + stars_of(LG["紫微"]), True, R["大三角"] + 20.0)
    R["參廁"] = bottom_n(stars_of(LG["參廁"]))

    # ── 構圖 ──
    F = {}
    F["01a"] = wide(R["0709"], True, 160.0, dy=10.0)
    F["01b"] = fit([VEGA, ALTAIR, DENEB], R["0709"], True, pad=0.30, minfov=60.0)
    F["02a"] = fit(stars_of(LG["青龍"]), R["青龍"], False, pad=0.08)
    F["02b"] = fit(stars_of(LG["紫微"]), R["白虎"], True, pad=0.10)
    F["02b2"] = fit(stars_of(LG["白虎"]), R["白虎"], True, pad=0.10)
    F["02c"] = wide(R["白虎"], True, 168.0)
    ja = [h for k2 in ("奎宿", "娄宿", "参宿") for h in stars_of([(CH[CH_BY_NATIVE[k2]]["segs"], "", 1)])]
    F["02d"] = fit(ja, R["白虎"], True, pad=0.18)
    F["03a"] = fit([POLARIS, 72607, 75097], R["金樁"], True, pad=0.6, minfov=44.0)
    F["03b"] = fit(stars_of(LG["駝鹿"]), R["駝鹿"], True, pad=0.18)
    F["03c"] = fit(stars_of(LG["因紐特"]), R["因紐特"], True, pad=0.08)
    F["04a"] = fit(CRUX + stars_of(LG["夏威夷"]), R["太平洋"], False, pad=0.10)
    F["04b"] = fit(stars_of(LG["阿努塔"]) + CRUX, R["太平洋"], False, pad=0.08)
    F["04c"] = fit(PLEIADES, R["昴宿"], True, pad=1.2, minfov=26.0)
    st_near = [h for h in stars_of(LG["月站"]) if h in S and -60 <= ((S[h][0] - 60 + 180) % 360 - 180) <= 60]
    F["05a"] = fit(st_near + PLEIADES, R["昴宿"], True, pad=0.06)
    F["05c"] = fit([SIRIUS, ALDEBARAN] + BELT, R["天狼"], True, pad=0.22)
    F["05ba"] = fit(stars_of(LG["蘇菲"]), R["蘇菲"], True, pad=0.10)
    F["05bb"] = wide(R["蘇菲"], True, 168.0)
    F["06a"] = fit(DIPPER + CAS_W + [POLARIS], R["納瓦荷"], True, pad=0.10)
    F["06b"] = fit(DIPPER + PLEIADES, R["黑腳"], True, pad=0.08)
    F["06c"] = fit(stars_of(LG["圖卡諾"]), R["圖卡諾"], True, pad=0.14)
    F["07a"] = fit(DIPPER, R["白俄"], True, pad=0.20)
    F["07b"] = fit(stars_of(LG["羅馬尼亞"]), R["羅馬尼亞"], True, pad=0.10)
    F["07c"] = fit(stars_of(LG["北歐"]), R["北歐"], True, pad=0.9, minfov=30.0)
    emu_pts = [p for poly in A31.DARK_ALL for p in poly[::4]]
    R["鴯鶓"] = rot_s(_rd(sum(_uv(*p) for p in emu_pts))[0])
    F["08a"] = fit(emu_pts, R["鴯鶓"], False, pad=0.06)
    F["08b"] = fit(stars_of(LG["魟魚"]), R["魟魚"], False, pad=0.22)
    F["08c"] = fit(stars_of(LG["船網"]), R["船網"], True, pad=0.10)
    F["09a"] = fit(PLEIADES + [ALDEBARAN], R["腰帶"], True, pad=0.4)
    F["09a2"] = fit(BELT + [27989, 24436], R["腰帶"], True, pad=0.35)
    F["09b"] = fit(DIPPER, R["北斗09"], True, pad=0.25)
    F["09b2"] = fit([DENEB, VEGA, ALTAIR, 90185, 89931], R["銀河"], True, pad=0.10)
    F["10"] = wide(R["銀河"], True, 168.0)
    F["11"] = fit([VEGA, ALTAIR, DENEB], R["大三角"], True, pad=0.35, minfov=60.0)
    F["11ba"] = fit(stars_of(LG["床廚"]) + stars_of(LG["紫微"]), R["床廚"], True, pad=0.06)
    F["11bb"] = fit(stars_of(LG["參廁"]), R["參廁"], True, pad=0.16)
    r12 = R["參廁"]
    # 12：一整圈（北盤逆時針＝時間往前）。每段 ≤ 60°；跨 −180→+180 那一頁同畫面硬切（拆 12／12b，同 A-36）
    F12a = [(0.0, round(yp + 20.0, 2), 150.0, r) for r in
            [r12] + [x for x in (-60.0, -120.0) if x < r12 - 1.0] + [-180.0]]
    F12b = [(0.0, round(yp + 20.0, 2), 150.0, r) for r in
            [180.0, 120.0, 60.0] + [x for x in (0.0,) if x > r12 + 1.0] + [r12]]
    # 13：台北 7/9 20:00 面北（西邊有月亮）→ 22:40（月落後，頭頂附近的大三角、正南的銀心＝盤心上方遠處）
    mx, my = disc_xy(m, MOON[0], MOON[1], R["0709"], True)
    F["13a"] = fit([MOON[:2], (S[VEGA][0], S[VEGA][1]), POLARIS], R["0709"], True, pad=0.10, dy=-6.0)
    gc = (266.40, -28.94)                                  # 銀心（J2000）
    F["13b"] = fit([VEGA, ALTAIR, DENEB, gc, (LST_AT["0709b"] % 360, PHI)], R["0709b"], True, pad=0.06)
    F["14"] = fit([VEGA, ALTAIR, DENEB, POLARIS, (LST_AT["0808"] % 360, PHI)], R["0808"], True, pad=0.08)
    F["15"] = wide(R["0808"], True, 150.0, dy=20.0)

    print("\n── 旋轉 ──\n  " + "、".join(f"{a} {b:+.1f}°" for a, b in R.items()))
    print("── 構圖 ──")
    for a, b in F.items():
        print(f"  {a} {b}")

    # ════════════════════ 標籤 ════════════════════
    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": round(a[0], 3), "dec": round(a[1], 3)}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = _rd(sum(_uv(*S[h][:2]) for h in a if h in S))
        return {"ra": round(ra, 3), "dec": round(dec, 3)}

    def L(a, text, color, px, fr, dxp=0.0, dyp=0.0, key=None):
        """px＝Canva 字級；dxp/dyp＝離錨點的螢幕位移（px，右／上為正）"""
        f = fr[2]
        return dict(anchor(a), text=text, color=color, size=round(px * f / (m.fu * 1080.0), 3),
                    dx=round(dxp * f / 1080.0, 2), dy=round(dyp * f / 1080.0, 2), key=key or text, disc=True)

    LB = {}
    f = F["01b"]
    LB["大三角"] = [L([VEGA], "織女", "white", 52, f, 0, 60), L([ALTAIR], "牛郎", "white", 52, f, 0, -60),
                  L([DENEB], "天津四", "white", 44, f, 0, 56)]
    f = F["02a"]
    LB["青龍"] = [L(stars_of(LG["青龍"]), "青龍", TEAL, 64, f, 0, 260), L(stars_of(LG["青龍"]), "中國", "white", 44, f, 0, 196)]
    f = F["02b2"]
    LB["紫微白虎"] = [L(stars_of(LG["紫微"]), "紫微垣", "amber", 56, F["02b"], 0, -40),
                   L(stars_of(LG["白虎"]), "白虎", WHITE2, 64, f, 0, -330)]
    f = F["02c"]
    LB["韓國"] = [L([POLARIS], "天象列次分野之圖", "blue", 56, f, 0, -560), L([POLARIS], "韓國・1395 年石刻", "white", 40, f, 0, -630)]
    f = F["02d"]
    ja_lab = []
    for nat, (wa, yi) in {"奎宿": ("斗掻き星", "刮平米斗的棒子"), "娄宿": ("蹈鞴星", "煉鐵的風箱"),
                          "参宿": ("唐鋤星", "一把犁")}.items():
        hs = stars_of([(CH[CH_BY_NATIVE[nat]]["segs"], "", 1)])
        ja_lab += [L(hs, wa, "amber", 52, f, 0, 120, key=wa), L(hs, yi, "white", 40, f, 0, 60, key=yi + "-zh")]
    LB["和名"] = ja_lab
    f = F["03a"]
    LB["金樁"] = [L([POLARIS], "金樁 Altan Gadas", "blue", 52, f, 0, 60), L([POLARIS], "蒙古：拴住天空的樁", "white", 40, f, 0, -60)]
    f = F["03b"]
    LB["駝鹿"] = [L(stars_of(X03.LG_ELK), "駝鹿的腳", "green", 48, f, 0, -70), L(stars_of(X03.LG_HUNT), "獵人", "green", 48, f, 0, 60),
                L(DIPPER, "埃文基：每晚重演的追獵", "white", 40, f, 0, -230)]
    f = F["03c"]
    LB["因紐特"] = [L(DIPPER, "Tukturjuit 馴鹿", "amber", 48, f, 300, 40), L([24608, 28360, 36850, 37826], "Quturjuuk 鎖骨", "amber", 48, f, 0, -70),
                 L([POLARIS], "因紐特：極夜的星鐘", "white", 40, f, 0, -60)]
    f = F["04a"]
    LB["夏東"] = [L(stars_of(LG["夏威夷"]), "夏威夷：Manaiakalani 魚鉤", "amber", 44, f, 0, 120),
                L(CRUX, "東加：Toloa 野鴨", "green", 44, f, -170, -90)]
    f = F["04b"]
    LB["阿努塔"] = [L(stars_of(LG["阿努塔"]), "阿努塔：Manu 大鳥", "blue", 48, f, 0, 0)]
    f = F["04c"]
    LB["Matariki"] = [L(PLEIADES, "Matariki", "amber", 60, f, 0, 120), L(PLEIADES, "毛利：昴宿＝新年", "white", 44, f, 0, -120)]
    f = F["05a"]
    LB["阿拉伯"] = [L(PLEIADES, "al-Thurayyā 昴宿", "green", 48, f, 0, 60), L(PLEIADES, "阿拉伯：28 月站", "amber", 44, f, 0, -70)]
    LB["印度"] = [L(PLEIADES, "Kṛttikā", "blue", 44, f, 0, 60), L([ALDEBARAN], "Rohiṇī", "blue", 44, f, 0, -60),
                L([27989], "Ārdrā", "blue", 44, f, 90, 60), L([36850, 37826], "Punarvasu", "blue", 44, f, 0, 60),
                L(PLEIADES, "印度：月亮的 27 位妻子", "white", 40, f, 0, 160)]
    f = F["05c"]
    LB["Sopdet"] = [L([SIRIUS], "Sopdet 天狼星", "amber", 56, f, 170, 70), L([SIRIUS], "古埃及：尼羅河漲水", "white", 40, f, 170, -70)]
    f = F["05ba"]
    LB["蘇菲"] = [L(stars_of(A34.LG["仙女"]), "仙女座（希臘）", "blue", 44, f, 0, 70),
                L(stars_of(A34.LG["大魚"]), "大魚（阿拉伯）", "green", 44, f, 0, -70),
                L(stars_of(LG["蘇菲"]), "蘇菲《恆星圖像之書》", "white", 40, f, 0, -330)]
    f = F["05bb"]
    LB["呂埃勒"] = [L([POLARIS], "呂埃勒 1786：只留下線", "white", 52, f, 0, -560)]
    f = F["06a"]
    LB["納瓦荷"] = [L(DIPPER, "Náhookǫs Bikąʼ", "amber", 44, f, 0, 70), L(CAS_W, "Náhookǫs Baʼáadii", "green", 44, f, 170, 70),
                 L([POLARIS], "Náhookǫs Bikǫʼ", "amber", 40, f, 0, -55), L(DIPPER, "納瓦荷：故事只在冬天講", "white", 40, f, 0, -70)]
    f = F["06b"]
    LB["黑腳"] = [L(DIPPER, "Seven Brothers 七兄弟", "amber", 44, f, 0, 70), L(PLEIADES, "Lost Children 昴宿", "amber", 44, f, 170, 70),
                L(DIPPER, "黑腳族：畫在帳篷頂上", "white", 40, f, 0, -70)]
    f = F["06c"]
    LB["圖卡諾"] = [L(stars_of(LG["圖卡諾"]), "Yai 美洲豹", "amber", 52, f, 230, 120),
                 L(stars_of(LG["圖卡諾"]), "圖卡諾：用落下的星座替漲水取名", "white", 40, f, 0, -520)]
    f = F["07a"]
    LB["白俄"] = [L(DIPPER, "Іллёў воз", "amber", 52, f, -200, 80), L(DIPPER, "白俄：以利亞的火焰馬車", "white", 40, f, -200, 20)]
    f = F["07b"]
    LB["羅馬尼亞"] = [L(stars_of(A23.LG_SHEP), "Ciobanul cu oile 牧羊人和羊", "green", 40, f, 120, -70),
                   L(stars_of(A23.LG_WELL), "Jgheabul și puțul 井和水槽", "green", 40, f, -60, -150)]
    f = F["07c"]
    LB["北歐"] = [L(stars_of(LG["北歐"]), "Úlfs kjaptr", "red", 56, f, 0, 110), L(stars_of(LG["北歐"]), "北歐手抄本：狼嘴", "white", 44, f, 0, -110)]
    f = F["08a"]
    LB["鴯鶓"] = [L(CRUX, "鴯鶓的頭（煤袋）", "purple", 44, f, -220, -70),
                L([ANTARES], "卡米拉羅伊／尤瓦萊：用黑暗畫成的鴯鶓", "white", 40, f, 0, 90)]
    f = F["08b"]
    LB["魟魚"] = [L(stars_of(LG["魟魚"]), "Lambaru 魟魚", "amber", 52, f, -170, 330), L(stars_of(LG["魟魚"]), "布吉斯＝曼達爾", "blue", 44, f, -170, 270)]
    f = F["08c"]
    LB["船網"] = [L(stars_of(A27.LG_BSHIP), "布吉斯：船", "amber", 48, f, 170, -330), L(stars_of(A26.LG_NET), "曼達爾：漁網", "blue", 48, f, -260, 260)]
    f = F["09a"]
    LB["昴宿09"] = [L(PLEIADES, "昴宿：幾十個名字", "white", 48, f, 0, 70)]
    f = F["09a2"]
    LB["腰帶09"] = [L(BELT, "獵戶腰帶", "white", 48, f, 0, 70)]
    f = F["09b"]
    LB["北斗09"] = [L(DIPPER, "北斗：十種人生", "white", 48, f, 0, 70)]
    f = F["09b2"]
    LB["銀河09"] = [L([DENEB, VEGA, ALTAIR], "銀河：河、路、一道縫", "white", 48, f, 0, 0)]
    f = F["11"]
    LB["勘誤1"] = [L([VEGA], "織女 25.04 光年", "white", 44, f, 0, 60), L([ALTAIR], "牛郎 16.73 光年", "white", 44, f, 0, -60)]
    f = F["11ba"]
    LB["床廚"] = [L(stars_of(LG["紫微"]), "紫微垣", "amber", 52, f, 0, 0),
                L(CH["214"]["segs"][0], "天床", "red", 44, f, 0, 55), L(CH["212"]["segs"][0], "天廚", "red", 44, f, 0, 55)]
    f = F["11bb"]
    LB["廁"] = [L(stars_of([(CH["003"]["segs"], "", 1)]), "參宿", "amber", 52, f, 0, 200),
               L(stars_of([(CH["047"]["segs"], "", 1)]), "廁（天兔座）", "purple", 48, f, -120, 80)]
    f = F["13a"]
    ph = MOON[4]
    a_v = altaz(S[VEGA][:2], T["0709"])
    LB["今晚八點"] = [L(MOON[:2], f"月亮 {MOON[2]:.0f}°（{ph:.0f}%）", "white", 44, f, 220, 60),
                   L([VEGA], f"織女 {a_v[0]:.0f}°", "white", 40, f, 0, 50)]
    f = F["13b"]
    alt = {h: altaz(S[h][:2], T["0709b"]) for h in (VEGA, ALTAIR, DENEB)}
    agc = altaz(gc, T["0709b"])
    LB["月落後"] = [L([VEGA], f"織女 {alt[VEGA][0]:.0f}°", "white", 40, f, 0, 50),
                 L([DENEB], f"天津四 {alt[DENEB][0]:.0f}°", "white", 40, f, 0, 50),
                 L([ALTAIR], f"牛郎 {alt[ALTAIR][0]:.0f}°", "white", 40, f, 0, -50),
                 L(gc, f"銀河中心 {agc[0]:.0f}°（正南）", "white", 40, f, 170, -80),
                 L((LST_AT["0709b"] % 360, PHI), "天頂", "white", 36, f, 0, 40)]
    f = F["14"]
    a8 = {h: altaz(S[h][:2], T["0808"]) for h in (VEGA, ALTAIR)}
    LB["七夕"] = [L([VEGA], f"織女 {a8[VEGA][0]:.0f}°", "white", 48, f, 0, 55), L([ALTAIR], f"牛郎 {a8[ALTAIR][0]:.0f}°", "white", 44, f, 0, -55),
                L((LST_AT["0808"] % 360, PHI), "天頂", "white", 36, f, 0, 40)]
    label_sets = [(v, k2) for k2, v in LB.items()]
    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    custom = custom_layers(m)
    print("\n── 大畫布圖層 ──")
    LG_MAIN = LG["大三角"]
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), (HALO, "單星光暈", "ring")]
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

    LINES_KEY = dict({"L4": "星座連線"}, **LNAME, **CUSTOM_KEYS)
    LINE_GROUPS = dict({"L4": LG_MAIN}, **LG, **{kk: [] for kk in CUSTOM_KEYS})

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文，依句切） ════════════════════
    N, Sd = True, False

    def R_(code, sec, north, frames, layers, labels, vo, note, **kw):
        return dict(code=code, kind="R", sec=sec, north=north, frames=frames, layers=layers, labels=labels,
                    vo=vo, note=note, **kw)

    shots = [
        R_("01", 13, N, [F["01a"], F["01b"]], ["大三角", "暈"], [], labels_end=["大三角"],
           vo="上週，我們沿著銀河繞了地球一圈。今晚第一季最後一集，從去年七夕的牛郎和織女算起：同一片星空，我們看見了——二十七種目光。",
           card="第一季完結｜27 種目光",
           note=f"北盤台北 7/9 20:00 面北（{R['0709']:+.1f}°；整集北盤畫到 −45°、不放地平線）：fov {F['01a'][2]:.0f} 全天＋銀河 → "
                f"推近夏季大三角（藍，迄格開織女／牛郎／天津四）；H-七夕素材回放一格由剪輯插在起格後；開場字卡"),
        R_("02", 3, Sd, [F["02a"]], ["青龍"], ["青龍"], cut=True,
           vo="在中國的天上，我們看見一條龍、",
           note=f"【硬切】北盤→南盤：青龍七宿（青 {TEAL}，Stellarium 新版 chinese 角亢氐房心尾箕；南盤 {R['青龍']:+.1f}° 龍身正立）。"
                "逐字稿原寫北盤，尾宿 −43° 在北盤貼著盤緣、被拉長 2 倍，改南盤"),
        R_("02.2", 3, N, [F["02b"], F["02b2"]], ["紫微", "白虎"], ["紫微白虎"], cut=True,
           vo="一座紫禁城、一隻白虎；",
           note=f"【硬切】南盤→北盤 {R['白虎']:+.1f}°：起格紫微垣兩垣（琥珀，H-元宵同一層）→ 滑到白虎七宿（灰白，A-12）"),
        R_("02.3", 3, N, [F["02b2"], F["02c"]], ["韓國"], ["韓國"],
           vo="韓國把星圖刻上石碑、印上鈔票；",
           note="北盤拉遠到全天（fov 168）：天象列次分野之圖層＝Stellarium korean 全部 312 星官（藍，線寬 0.7）；一萬韓元鈔票照片不放（版權）"),
        R_("02.4", 7, N, [F["02c"], F["02d"]], ["白虎"], ["和名"],
           vo="日本照抄了二十八宿的格子，卻替好幾宿取了農具和家用品的名字。",
           note="推近奎、婁、參三宿：日本和名標籤（琥珀）＋語意（白）——只標 A-05 v2 07 鏡講過的三宿，不暗示二十八宿全是農具"),
        R_("03", 4, N, [F["02d"], F["03a"]], ["暈"], ["金樁"],
           vo="草原上，蒙古人把天空拴在一根金樁上；",
           note=f"北盤 {R['金樁']:+.1f}°（盤繼續逆時針轉）推到北極星：金樁 Altan Gadas（A-07）"),
        R_("03.2", 7, N, [F["03a"], F["03b"]], ["駝鹿"], ["駝鹿"],
           vo="西伯利亞的針葉林裡，埃文基獵人追著一頭駝鹿，每天晚上重演一次；",
           note=f"北盤轉到 {R['駝鹿']:+.1f}°：北斗＝駝鹿的腳（斗口）＋獵人（斗柄）（綠，X-03 照 A-08 v2）"),
        R_("03.3", 4, N, [F["03b"], F["03c"]], ["因紐特"], ["因紐特"],
           vo="北極圈的因紐特人，在極夜裡用星星報時。",
           note=f"北盤 {R['因紐特']:+.1f}°：Tukturjuit 馴鹿（北斗）＋Quturjuuk 鎖骨（御夫＋雙子）（琥珀，A-14）"),
        R_("04", 6, Sd, [F["04a"], F["04b"]], ["夏威夷", "東加", "阿努塔"], ["夏東"], labels_end=["阿努塔"], cut=True,
           vo="太平洋上，夏威夷、東加、阿努塔的人不用儀器，靠星星回家；",
           note=f"【硬切】北盤→南盤 {R['太平洋']:+.1f}°：夏威夷 Manaiakalani 魚鉤（琥珀，A-09）＋東加 Toloa 野鴨＝南十字（綠，A-10）"
                "→ 滑到阿努塔 Manu 大鳥（藍，A-11：南河三—天狼—老人星）"),
        R_("04.2", 5, N, [F["04c"]], ["暈"], ["Matariki"], cut=True,
           vo="紐西蘭的毛利人，等昴宿在六月的黎明重現，過新年。",
           note=f"【硬切】南盤→北盤 {R['昴宿']:+.1f}°：昴宿特寫，毛利 Matariki 標籤（A-33）。逐字稿原寫換長圖；昴宿 +24° 在北盤上，不換組"),
        R_("05", 6, N, [F["04c"], F["05a"]], ["月站"], ["阿拉伯"],
           vo="沙漠裡，阿拉伯人看昴宿等雨季，替月亮蓋了二十八間旅店；",
           note="北盤拉遠：al-Thurayyā（昴宿，綠標）→ 月站沿黃道（琥珀，A-32 的 28 站連線）"),
        R_("05.2", 3, N, [F["05a"]], ["印度"], ["印度"],
           vo="印度人說，月亮有二十七位妻子；",
           note="同一格換層：印度 Nakṣatra（藍，A-28）＋Kṛttikā、Rohiṇī、Ārdrā、Punarvasu 標籤（IAST，不用天城文）"),
        R_("05.3", 5, N, [F["05a"], F["05c"]], ["暈"], ["Sopdet"],
           vo="尼羅河邊，古埃及人等天狼星回來，河水就要漲了。",
           note=f"北盤轉到 {R['天狼']:+.1f}°（＝逐字稿的「S 捲到天狼星」）：天狼星光暈＋Sopdet（A-18）"),
        R_("05b", 8, N, [F["05c"], F["05ba"]], ["蘇菲"], ["蘇菲"],
           vo="一千多年前，波斯天文學家蘇菲，把希臘星座和阿拉伯的老星名，寫進同一本書；",
           note=f"北盤轉到 {R['蘇菲']:+.1f}°：仙女座（藍）＋阿拉伯大魚（綠）（A-34 同兩層）；書影由美宣放 BnF Arabe 5036（標來源；"
                "Marsh 144 是 CC BY-NC 4.0，不是公版）"),
        R_("05b.2", 6, N, [F["05ba"], F["05bb"]], ["呂埃勒"], ["呂埃勒"],
           vo="一七八六年，一位巴黎天文學家，把星座的圖畫拿掉，只留下線。",
           note="北盤拉遠到全天：呂埃勒 1786 連線層（白，A-30）"),
        R_("06", 4, N, [F["05bb"], F["06a"]], [], ["納瓦荷"],
           vo="在美洲，納瓦荷的星星故事只在冬天講；",
           note=f"北盤 {R['納瓦荷']:+.1f}°：納瓦荷只放名稱標籤（A-16），不放連線、不放故事畫面（今天是七月）"),
        R_("06.2", 4, N, [F["06a"], F["06b"]], ["黑腳"], ["黑腳"],
           vo="黑腳族把北斗和昴宿，畫在帳篷頂上；",
           note=f"北盤 {R['黑腳']:+.1f}°：七兄弟（北斗，琥珀，A-17）＋走失的孩子（昴宿）；不重現任何真實彩繪帳篷的圖案"),
        R_("06.3", 6, N, [F["06b"], F["06c"]], ["圖卡諾"], ["圖卡諾"],
           vo="亞馬遜的圖卡諾人，用黃昏落下的星座，替每一次漲水取名字。",
           note=f"北盤 {R['圖卡諾']:+.1f}°：Yai 美洲豹（仙后＋英仙，琥珀，A-24 同一層）"),
        R_("07", 5, N, [F["06c"], F["07a"]], ["白俄"], ["白俄"],
           vo="白俄羅斯的農民，把北斗看成先知以利亞的火焰馬車；",
           note=f"北盤 {R['白俄']:+.1f}°：Іллёў воз（琥珀，A-22）"),
        R_("07.2", 6, N, [F["07a"], F["07b"]], ["羅馬尼亞"], ["羅馬尼亞"],
           vo="羅馬尼亞的天上，有牧羊人、羊群和一口給羊喝水的井；",
           note=f"北盤 {R['羅馬尼亞']:+.1f}°：Ciobanul cu oile、Jgheabul și puțul（綠，A-23）"),
        R_("07.3", 4, N, [F["07b"], F["07c"]], ["北歐"], ["北歐"],
           vo="北歐的古老手抄本，把畢宿看成一張狼嘴。",
           note=f"北盤 {R['北歐']:+.1f}°：畢宿 Úlfs kjaptr（紅，A-15）"),
        R_("08", 7, Sd, [F["08a"]], ["鴯鶓"], ["鴯鶓"], cut=True,
           vo="南半球的卡米拉羅伊和尤瓦萊人，不只連星星，也連銀河裡的黑暗；",
           note=f"【硬切】北盤→南盤 {R['鴯鶓']:+.1f}°：鴯鶓暗帶（紫半透明填色＋描邊，沿用 A-31 自繪多邊形，不改作 Stellarium 原圖）"),
        R_("08.2", 6, Sd, [F["08a"], F["08b"]], ["魟魚"], ["魟魚"],
           vo="印尼的布吉斯和曼達爾水手共用一片海，天上也有同一條魟魚；",
           note=f"南盤 {R['魟魚']:+.1f}°：魟魚 Lambaru（天蠍頭與身 10 星）兩層完全重疊：布吉斯寬線琥珀（A-26）＋曼達爾細線藍（A-27）"),
        R_("08.3", 4, N, [F["08c"]], ["船網"], ["船網"], cut=True,
           vo="同一個北斗，一邊看成船，一邊看成漁網。",
           note=f"【硬切】南盤→北盤 {R['船網']:+.1f}°：布吉斯的船（琥珀，A-27）／曼達爾漁網（藍，A-26，連進天龍）"),
        R_("09", 7, N, [F["09a"], F["09a2"]], ["腰帶", "暈"], ["昴宿09"], labels_end=["腰帶09"],
           vo="我們也繞了地球好幾圈：昴宿有幾十個名字，獵戶腰帶到處有人認得，",
           note=f"北盤 {R['腰帶']:+.1f}°：昴宿（X-01）→ 獵戶腰帶（X-02）。逐字稿原寫長圖 S；在北盤上一路轉過去，北斗也就在盤上"),
        R_("09.2", 7, N, [F["09b"], F["09b2"]], ["北斗", "大三角"], ["北斗09"], labels_end=["銀河09"],
           vo="北斗有十種人生，銀河是河、是路，也是一道縫；還學了不用羅盤，看星星找路。",
           note=f"北盤 {R['北斗09']:+.1f}°→{R['銀河']:+.1f}°：北斗（X-03）→ 銀河天鵝—人馬段（X-07）；最後一句疊 X-04～X-06 縮圖（剪輯從各集匯出）"),
        R_("10", 12, N, [F["09b2"], F["10"]], [], [], overlay="C-X08-01_世界地圖", overlay_layers=["陸地層", "27點層", "客人層"],
           vo="算一算：有自己一整集的文化和星圖，二十七個；跨文化那幾集，又請來十幾位客人——從北極圈到南非、從亞馬遜到太平洋的小島。",
           card="27 個文化＋十幾位客人",
           note="北盤拉遠全天定格；疊 C-X08-01（陸地點陣 → 27 個實心點 → 19 個空心點；原住民族群只標大致區域）"),
        R_("10.2", 4, N, [F["10"]], [], [], overlay="C-X08-04_第一季27個文化一覽",
           vo="四十七集正片，加三支節日特輯。",
           note="同一格；疊 9:16 圖卡 C-X08-04「第一季 27 個文化一覽」（可存圖）"),
        R_("11", 6, N, [F["10"], F["11"]], ["大三角", "暈"], ["勘誤1"], overlay="C-X08-03_牛郎織女距離",
           overlay_layers=["三角形層", "答案層"],
           vo="這一年，我們也講錯過。七夕那集說牛郎織女相距十六光年；",
           card="勘誤①：14.6 光年",
           note="推近夏季大三角（藍）＋距離標籤；疊 C-X08-03（三角形層：地球—織女 25.04—牛郎 16.73、夾角 34.2° → 答案層：14.6 光年）"),
        R_("11.2", 5, N, [F["11"]], ["大三角"], [], overlay="C-X08-02_勘誤卡", overlay_layers=["七夕層"],
           vo="用衛星新量的距離重算，是十四點六光年。",
           note="同一格；疊 C-X08-02 勘誤卡第 1 張（舊說「16 光年」劃線＋新說 14.6）"),
        R_("11b", 5, N, [F["11"], F["11ba"]], ["紫微", "床廚"], ["床廚"],
           vo="三垣那集說，紫微垣裡連上廁所的地方都有星官——",
           note=f"北盤 {R['床廚']:+.1f}°：紫微垣（琥珀）＋天床、天廚亮一下（紅）"),
        R_("11b.2", 6, N, [F["11ba"], F["11bb"]], ["參廁"], ["廁"], overlay="C-X08-02_勘誤卡", overlay_layers=["三垣層"],
           vo="其實紫微垣沒有；天上的廁所，在參宿南邊。講錯了，就改。",
           card="勘誤②：廁所在參宿",
           note=f"北盤轉到 {R['參廁']:+.1f}°（＝逐字稿的「長圖 S 捲到參宿」）：參宿（琥珀）→ 往南「廁」四星（天兔 α β γ δ）＋屎（紫）；迄格疊勘誤卡第 2 張"),
        R_("12", 8, N, F12a, ["網"], [],
           vo="同一片星空，大家看見的不一樣：有人看見皇宮，有人看見農具，有人看見回家的路。",
           note="北盤拉遠、慢轉一整圈（逆時針＝時間往前，每段 ≤ 60°）：「一片彩色網」層＝各集連線同時疊上（在 Canva 把這一層透明度調到 30%）；"
                "不疊納瓦荷（七月不放）、圖卡諾只用 Stellarium 公開連線"),
        R_("12.2", 7, N, F12b, ["網"], [], cut=True,
           vo="可是幾乎每個文化都在做同一件事——抬頭，把自己的日子寫上天。",
           note="第一頁與 12 鏡最後一頁畫面相同（−180°＝+180°），【硬切】接上（Canva 旋轉只收 ±180）；繼續轉完一圈，最後一頁彩色網淡掉、只留星點"),
        R_("13", 5, N, [F["13a"]], ["月", "大三角"], ["今晚八點"], horizon=[PHI], cut=True,
           vo="今晚八點抬頭：西南西有快半個的月亮，十點半就下山。",
           note=f"【硬切】北盤台北 7/9 20:00 面北（{R['0709']:+.1f}°，山＝北方地平線）：月亮（站心位置，圖示放大約 3 倍＝示意）在右手邊西南西"),
        R_("13.2", 12, N, [F["13a"], F["13b"]], ["大三角", "暈"], ["月落後"], horizon=[PHI],
           vo="月亮下山後，夏季大三角高高掛在東邊天上；到沒有光害的地方，銀河中心就在正南方。織女和牛郎，又回來了。",
           note=f"北盤轉到 22:40（{R['0709b']:+.1f}°，月落後）抬頭：大三角在天頂附近、銀心在盤心上方遠處＝正南；角落小字「市區看不到銀河」（剪輯原生字）"),
        R_("14", 15, N, [F["13b"], F["14"]], ["大三角", "暈"], ["七夕"], horizon=[PHI], overlay="C-X08-05_七夕0808晚上九點",
           vo="第二季，從今年七夕出發：八月八日、星期天，剛好也是父親節；從去年七夕算起，正好滿一個農曆年。那天晚上九點多，織女幾乎就在頭頂。",
           card="第二季｜8/8 七夕出發",
           note=f"北盤轉到 8/8 21:00（{R['0808']:+.1f}°）：織女幾乎在天頂；迄格疊 9:16 圖卡 C-X08-05「七夕 8/8 晚上九點的天空」（可存圖）"),
        R_("15", 6, N, [F["14"], F["15"]], [], [],
           vo="謝謝你這一年，陪我們抬頭。我們七夕見。",
           card="萬國星空 第一季完結｜第二季 2027/8/8 七夕首播",
           note="北盤拉遠；星點層在 Canva 慢慢淡出；端卡＋追蹤 CTA"),
    ]
    # 一頁兩用（上一鏡迄格＝這一鏡起格）時，那一頁留上一鏡的標籤（字級是照那一格算的）；
    # 會動的鏡頭，自己的標籤到迄格才開（標籤字級照迄格的 fov 算）
    #（鏡頭本身另寫了 labels_end 的＝起格那組標籤是照起格算的，新構圖時就用自己的）
    for p, q in zip([None] + shots[:-1], shots):
        if len(q["frames"]) < 2:
            continue
        own_start = "labels_end" in q
        q.setdefault("labels_end", list(q["labels"]))
        same = p is not None and p["north"] == q["north"] and \
            all(abs(a - b) < 1e-6 for a, b in zip(p["frames"][-1], q["frames"][0]))
        if "labels_start" not in q:
            q["labels_start"] = (list(p.get("labels_end", p["labels"])) if same
                                 else list(q["labels"]) if own_start else [])
    # 逐字稿鏡號（拆鏡後加總用）
    for sh in shots:
        sh["src"] = sh["code"].split(".")[0]          # 「05b.2」→ 05b、「12.2」→ 12
    print("\n── 旁白字數 ──")
    tot_u = 0
    by_src = {}
    for sh in shots:
        u = vo_units(sh["vo"]); tot_u += u
        r = u / sh["sec"]
        print(f"  {sh['code']:>5}  {u:3d} 字 / {sh['sec']:2d} 秒 ＝ {r:.2f}{'  ✗ 超過 4.5' if r > 4.5 else ''}")
        sh["vo_units"] = u
        a = by_src.setdefault(sh["src"], [0, 0]); a[0] += u; a[1] += sh["sec"]
    tot_s = sum(s["sec"] for s in shots)
    print(f"  合計 {tot_u} 字 / {tot_s} 秒 ＝ {tot_u/tot_s:.2f} 字/秒")
    print("  逐字稿鏡頭：" + "、".join(f"{k} {v[1]}s/{v[0]}字" for k, v in by_src.items()))
    m.check_shots(shots)
    print("  判斷後接受的 ⚠：" + WARN_OK)
    for sh in shots:
        rs = [f[3] for f in sh["frames"]]
        for a, b in zip(rs, rs[1:]):
            if abs(b - a) >= 170.0:
                print(f"  ✗ {sh['code']}：單段旋轉 {b - a:+.1f}° ≥ 170°")
    for p, q in zip(shots, shots[1:]):
        if not q.get("cut") and p["north"] == q["north"]:
            d = abs(q["frames"][0][3] - p["frames"][-1][3])
            if d >= 170:
                print(f"  ✗ {p['code']}→{q['code']}：鏡頭間旋轉 {d:.1f}° ≥ 170°")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
            yc = m.y_pole if sh["north"] else -m.y_pole
            ew = 2 * m.R_fill / fov * 1080
            off = (round(-cx / fov * 1080), round((cy - yc) / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": which, "元素寬px": round(ew), "位移X px": off[0], "位移Y px": off[1],
                         "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    print("\n── 數字核對 ──")
    for nm, when in T.items():
        mr = moon_radec(when)
        print(f"  {when}：LST {LST_AT[nm]:.2f}、北盤 {R[nm]:+.1f}°；月亮 高 {mr[2]:.1f}° 方位 {mr[3]:.0f}° 相位 {mr[4]:.0f}%；"
              + "、".join(f"{n} {altaz(S[h][:2], when)}" for n, h in (("織女", VEGA), ("牛郎", ALTAIR), ("天津四", DENEB)))
              + f"、銀心 {altaz(gc, when)}")
    print(f"  y_pole {yp:.2f}、R_fill {RF:.2f}、k {k:.4f}；月亮 20:00 盤上 ({mx:.1f}, {my - yp:.1f})")

    terms = {}
    for key, items in LB.items():
        for it in items:
            terms.setdefault(it["key"], dict(hips=[it["hip"]] if "hip" in it else [], 原文=it["text"], 拼音="",
                                              英文翻譯="", 中文=it["text"], 顏色=it["color"], 來源備註=key))
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst_at": LST_AT, "rot": R, "lst0": LST0},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV = LG["網"]
    m.preview(os.path.join(OUT, f"{EP}_預覽黑底-全部連線.png"), line_groups=PREV,
              labels=[dict(it, pt=5) for items, _ in label_sets for it in items], title=f"{EP}　大畫布 v4.6（各文化連線＋全部標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_MAIN)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for kk in sh.get("layers", []) for x in LINE_GROUPS.get(kk, [])]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
