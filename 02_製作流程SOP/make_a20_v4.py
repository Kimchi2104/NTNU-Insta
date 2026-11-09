# -*- coding: utf-8 -*-
"""A-20 春節特輯｜朱雀：一顆蛋孵出一個王朝｜大畫布 v4.6

論點：除夕回中國看四象的最後一隻。七宿拼成一隻鳥（天官書：柳＝鳥嘴、星＝頸、張＝嗉、翼＝羽翮、軫＝車）；
十二次把這段天切成鶉首、鶉火、鶉尾；「咮為鶉火，心為大火」；朱雀身邊是一桌年夜飯（柳＝廚宰、張＝廚、
積薪、酒旗、天樽、鬼＝祠事）；玄鳥生商的玄鳥是黑燕、商主大火——紅鳥興周、歲在鶉火；
今年除夕木星、火星都在鶉火；午夜鶉火過中天；鬼宿積尸氣（M44）、鬼金羊；西方的烏鴉＝軫宿；四象到齊。
來源：逐字稿 v1（星空對時＝PyEphem 自算）；Stellarium chinese（星官連線）、western（Hya／Crt／Crv）。

鏡頭路線：南走廊 T：老人星（承上集）往上到井鬼柳 →【換組】北盤：四象方位（概念圖 C-A20-06）→
長圖 S 往東滑過七宿（鳥形）→ Z 拉遠：十二次三段 → 推近柳宿（概念圖 兩個火）→ 天上的年夜飯 →
定格：一顆蛋（概念圖，07 三層、08 換燕子層）→ 紅鳥興周（概念圖）滑到鶉火 → 今年除夕：木星、火星在鶉火 →
【換組】南盤：台北面南 20:00→00:00（圖卡 除夕抬頭看）→ 長圖：積尸氣、鬼金羊 → 西方的長蛇、巨爵、烏鴉 →
【換組】北盤：四象到齊（圖卡 四象總圖）→ 北盤轉向北斗／仙后：下集薩米。

參數
  lst = 116 → 走廊（x=0）＝RA 116（積薪、北河三、南河三一線）；七宿 x：井 +20、鬼 −12、柳 −13、星 −26、張 −32、
             翼 −49、軫 −68；老人星 x +20（南走廊 T 的起格看得到它）；接縫 x=±180＝RA 296（天鷹—摩羯），整集碰不到。
  D_s = 45、D_r = 49 → 七宿 dec −27.3（翼）…+25.1（井）、天樽 +25.1、積薪 +24.4、爟 +29.7、西方長蛇最南 −33.9
             都在帶內；03 鏡 S 的 |cy|+fov·8/9 ≤ 45（fov 48–49、cy −1）。老人星 −52.7 在南盤本體（01 鏡 T 起點）。
  D_fill = −35 → k=1.397、R_fill=174.6（|x_t|+R_fill ≤ 180 ✓）：
             北盤到 dec −35 → 02／15 鏡 fov 160 的全天方位（角落距盤心 163）；
             南盤到 dec +35 → 12 鏡台北面南（南方地平線 dec −65 到 dec +16）整格在填滿圓內。
  x_tN = x_tS = 0（Canva 可水平置中）。
  ⚠ 切點（02、12、15、16 的 R 起迄格含長圖側扇區）：判定可接受——這幾鏡都不是「同框接手」，
    gen_canva_pages 會自動插「長圖轉◯盤-上移」到盤心（fov ≤ 50、rot 0，整格在盤緣圈內＝逐點一致），
    在盤圖層組上 Match & Move 到 R 起格；回程同樣先「歸位」到盤心 rot 0 再換回長圖。
  南盤旋轉（面南，順時針＝時間前進）：rot＝lst_obs＋x_tS−lst；台北 2/5 22:00 −9.0°、2/6 00:00 +21.1°（30°，<180 ✓）；
        20:00 面南時鶉火還在東方低空、畫面空，起格改 22:00（柳宿已 61°）。
  北盤：rot 0 時盤心正下方＝RA 116；轉 −24°（逆時針）→ 正下方 RA 140＝朱雀中段在「前（南）」，
        玄武在上（後）、青龍在左（東）、白虎在右（西）＝《禮記》「前朱鳥而後玄武，左青龍而右白虎」。
  十二次邊界：《晉書・天文志》度數（鶉首 井十六度—柳八度、鶉火 柳九度—張十六度、鶉尾 張十七度—軫十一度），
        古度依《晉書》宿度（井33 柳15 張18 軫17）在今日距星間距上等比換算（J2000）：
        鶉首 110.4°–136.1°、鶉火 136.1°–163.0°、鶉尾 163.0°–195.2°。木星（J2000 145.1°）、火星（159.1°）都在鶉火。
        ※ 依這個換算，柳宿本身大半落在鶉首（柳九度才進鶉火）——旁白「柳、星、張是鶉火」是《爾雅》與通說的簡化，畫面照度數畫。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-20"
OUT = os.path.join(BASE, "05_素材/A-20_朱雀/_v4大畫布")
LST0 = 116.0
XTN = XTS = 0.0
PHI = 25.033
TPE = (25.0330, 121.5654)


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem）
# ══════════════════════════════════════════════════════════════════
def _obs(when, tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def lst_at(when):
    return math.degrees(_obs(when).sidereal_time())


def planets(when="2027/2/5 20:00"):
    """J2000（astrometric）位置＝與星表同一個框；另回傳當地高度、方位"""
    import ephem
    o = _obs(when)
    out = {}
    for nm, b in (("木星", ephem.Jupiter()), ("火星", ephem.Mars())):
        b.compute(o)
        out[nm] = dict(ra=math.degrees(b.a_ra), dec=math.degrees(b.a_dec),
                       alt=math.degrees(b.alt), az=math.degrees(b.az))
    return out


def rot_s(lst_obs):
    """南盤轉到「該恆星時、面向南方」（A-19 同式）；順時針＝時間前進"""
    return round((lst_obs + XTS - LST0 + 180.0) % 360.0 - 180.0, 2)


T_TPE = {"20:00": "2027/2/5 20:00", "22:00": "2027/2/5 22:00", "00:00": "2027/2/6 00:00"}
LSTS = {k: lst_at(v) for k, v in T_TPE.items()}
ROT = {k: rot_s(v) for k, v in LSTS.items()}
PL = planets()
ROT_N = -24.0                    # 北盤：朱雀（RA 140）轉到正下方＝「前」


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
MU_GEM, THETA_CNC, DELTA_HYA, ALPHARD = 30343, 41822, 42313, 46390
UPS_HYA, ALPHA_CRT, GAMMA_CRV, SPICA = 48356, 53740, 59803, 65474
CANOPUS, REGULUS, KAPPA_GEM, SIRIUS, PROCYON, POLLUX = 30438, 49669, 37740, 32349, 37279, 37826
POLARIS, DUBHE, ALKAID, CAPELLA, SCHEDAR, MIRFAK = 11767, 54061, 67301, 24608, 3179, 15863
MAINS = [MU_GEM, THETA_CNC, DELTA_HYA, ALPHARD, UPS_HYA, ALPHA_CRT, GAMMA_CRV, CANOPUS, REGULUS, KAPPA_GEM]
M44 = (130.10, 19.67)


def x_of(ra):
    return -(((ra - LST0) + 180.0) % 360.0 - 180.0)


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium chinese／western）
# ══════════════════════════════════════════════════════════════════
SKY = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def sc_lines(culture):
    d = json.load(open(os.path.join(SKY, culture, "index.json"), encoding="utf-8"))
    return {c["id"].split()[-1]: [[h for h in l if isinstance(h, int)] for l in c["lines"]]
            for c in d["constellations"]}


C = sc_lines("chinese")
W = sc_lines("western")
SEVEN = ["010", "007", "013", "027", "030", "029", "031"]          # 井 鬼 柳 星 張 翼 軫
SEVEN_ZH = ["井宿", "鬼宿", "柳宿", "星宿", "張宿", "翼宿", "軫宿"]
FEAST = ["107", "120", "256"]                                       # 積薪 酒旗 天樽（旁白講到的）
QINGLONG = ["009", "011", "004", "006", "026", "024", "008"]        # 角亢氐房心尾箕
XUANWU = ["005", "016", "017", "028", "023", "018", "002"]          # 斗牛女虛危室壁
BAIHU = ["012", "014", "025", "015", "001", "034", "003"]           # 奎婁胃昴畢觜參
OTHER = ["104", "261", "088", "278", "040", "149", "234", "097", "221", "247", "297", "181", "019", "020",
         "141", "147", "155", "268", "171", "172", "199", "193", "269", "125", "282", "195", "191", "115",
         "154", "190", "179", "235", "049", "132", "117", "175", "059", "099", "204", "276", "283", "114",
         "239", "163", "056", "303", "305", "280", "227", "130", "201", "311", "188", "306", "270", "131"]
WEST = ["Hya", "Crt", "Crv"]

LG_SEVEN = [(C[k], "red", 1.0) for k in SEVEN]
LG_FEAST = [(C[k], "amber", 1.0) for k in FEAST]
LG_QL = [(C[k], "green", 1.0) for k in QINGLONG]
LG_XW = [(C[k], "blue", 1.0) for k in XUANWU]
LG_BH = [(C[k], "white", 1.0) for k in BAIHU]
LG_OTHER = [(C[k], "white", 0.6) for k in OTHER if k in C]
LG_WEST = [(W[k], "blue", 1.0) for k in WEST]
LG_ALL = LG_SEVEN + LG_FEAST + LG_QL + LG_XW + LG_BH + LG_OTHER
LINE_SETS = [(LG_SEVEN, "連線-朱雀七宿"), (LG_FEAST, "連線-年夜飯"), (LG_QL, "連線-青龍"),
             (LG_XW, "連線-玄武"), (LG_BH, "連線-白虎"), (LG_OTHER, "連線-其他星官"),
             (LG_WEST, "連線-西方")]
LINES_KEY = {"L4": "星座連線", "朱": "連線-朱雀七宿", "飯": "連線-年夜飯", "龍": "連線-青龍",
             "玄": "連線-玄武", "虎": "連線-白虎", "他": "連線-其他星官", "西": "連線-西方",
             "次": "十二次", "鶉火": "鶉火", "鳥": "鳥形", "行": "行星", "深空": "深空天體"}
LINE_GROUPS = {"L4": LG_ALL, "朱": LG_SEVEN, "飯": LG_FEAST, "龍": LG_QL, "玄": LG_XW, "虎": LG_BH,
               "他": LG_OTHER, "西": LG_WEST}
SIX = ["朱", "龍", "玄", "虎"]          # 四象四色


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(
        sum(math.sin(math.radians(S[h][0])) for h in hs),
        sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def uniq(segs):
    return sorted({h for s in segs for h in s})


# ══════════════════════════════════════════════════════════════════
# 三、十二次（《晉書・天文志》度數 → 今日距星間距等比換算）
# ══════════════════════════════════════════════════════════════════
JIN_DU = {"井": 33, "柳": 15, "張": 18, "軫": 17}


def ci_bounds(S):
    ra = {k: S[h][0] for k, h in (("井", MU_GEM), ("鬼", THETA_CNC), ("柳", DELTA_HYA), ("星", ALPHARD),
                                   ("張", UPS_HYA), ("翼", ALPHA_CRT), ("軫", GAMMA_CRV), ("角", SPICA))}
    nxt = {"井": "鬼", "柳": "星", "張": "翼", "軫": "角"}

    def at(su, du):                        # 某宿第 du 度「之後」＝距星＋du／宿度×今日間距
        return ra[su] + du / JIN_DU[su] * ((ra[nxt[su]] - ra[su]) % 360)
    return {"鶉首": (at("井", 15), at("柳", 8)), "鶉火": (at("柳", 8), at("張", 16)),
            "鶉尾": (at("張", 16), at("軫", 11))}


# ══════════════════════════════════════════════════════════════════
# 四、旁白字數（中文字＋外文音節；A-12 同一套）
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
            n += max(1, len(re.findall(r"[aeiouy]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 五、自訂圖層：十二次、鶉火、鳥形、行星、深空天體（大畫布＋南北盤同步出）
# ══════════════════════════════════════════════════════════════════
RED = COLORS["red"]


def custom_layers(m, S):
    CI = ci_bounds(S)
    BAND = m.Ds - 1.0                      # 長圖帶內畫到 ±44（縫合帶不畫，換組不穿幫）

    def wedge(s, pos, ra1, ra2, op, disc):
        """赤經 ra1→ra2 的整條色帶。大畫布：只畫長圖帶（矩形，逐點精確）；
        盤：dec 從盤的填滿圓邊緣到 ±40（離盤心 >70，比換組格 r≤51 遠，換組不穿幫）"""
        if disc is None:
            x1, x2 = x_of(ra1), x_of(ra2)
            s.poly_fill([[(x1, -BAND), (x2, -BAND), (x2, BAND), (x1, BAND)]], fill=RED, opacity=op)
            for xx in (x1, x2):
                s.polylines([[(xx, -BAND), (xx, BAND)]], stroke=RED, w=0.14, opacity=0.55, dash="0.8 0.6")
            return
        lo, hi = ((-34.5, 40.0) if disc else (-40.0, 34.5))
        n = 40
        edge1 = [(ra1, lo + (hi - lo) * i / n) for i in range(n + 1)]
        top = [(ra1 + (ra2 - ra1) * i / n, hi) for i in range(n + 1)]
        edge2 = [(ra2, hi - (hi - lo) * i / n) for i in range(n + 1)]
        bot = [(ra2 - (ra2 - ra1) * i / n, lo) for i in range(n + 1)]
        poly = [pos(ra, dec)[0] for ra, dec in edge1 + top + edge2 + bot if pos(ra, dec)]
        s.poly_fill([poly], fill=RED, opacity=op)
        for e in (edge1, edge2):
            s.polylines([[pos(ra, dec)[0] for ra, dec in e if pos(ra, dec)]], stroke=RED, w=0.14,
                        opacity=0.55, dash="0.8 0.6")

    def ci12(s, pos, runs, disc):
        for nm, (a, b) in CI.items():
            wedge(s, pos, a, b, 0.24 if nm == "鶉火" else 0.10, disc)

    def chunhuo(s, pos, runs, disc):
        a, b = CI["鶉火"]
        wedge(s, pos, a, b, 0.22, disc)

    def bird(s, pos, runs, disc):
        """《天官書》的鳥：柳＝嘴、星＝頸、張＝嗉、翼＝羽翮、軫＝車（示意淡線）"""
        cen = {k: centroid(uniq(C[k]), S) for k in SEVEN}
        beak = (127.0, 6.6)
        body = [beak, cen["013"], cen["027"], cen["030"], (cen["029"][0] - 3, cen["029"][1] + 2), cen["031"]]
        wing1 = [cen["030"], (cen["029"][0], cen["029"][1] + 9.0), (cen["029"][0] + 6, cen["029"][1] + 5.0)]
        wing2 = [cen["030"], (cen["029"][0] - 1, cen["029"][1] - 7.0), (cen["029"][0] + 6, cen["029"][1] - 4.0)]
        for path, w_ in ((body, 0.5), (wing1, 0.42), (wing2, 0.42)):
            pts = []
            for (ra_a, de_a), (ra_b, de_b) in zip(path, path[1:]):
                for i in range(12):
                    t = i / 12
                    pts.append((ra_a + (ra_b - ra_a) * t, de_a + (de_b - de_a) * t))
            pts.append(path[-1])
            s.polylines(runs(pts), stroke="#FFFFFF", w=w_, opacity=0.45, dash="1.2 0.8")

    def planet(s, pos, runs, disc):
        for nm, col, r in (("木星", "#FFFFFF", 0.95), ("火星", COLORS["red"], 0.62)):
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.4, fill=col, opacity=0.18)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    def deep(s, pos, runs, disc):
        mw = COLORS["mw"]
        for k, op in ((1.0, 0.10), (0.65, 0.16), (0.35, 0.26)):
            pts = [(M44[0] + 0.75 * k * math.cos(2 * math.pi * i / 48) / math.cos(math.radians(M44[1])),
                    M44[1] + 0.75 * k * math.sin(2 * math.pi * i / 48)) for i in range(49)]
            s.poly_fill(runs(pts), fill=mw, opacity=op)
        dots = []
        c = math.cos(math.radians(M44[1]))
        for h, (ra, dec, v) in S.items():
            if m.maglim < v <= 8.0 and math.hypot((ra - M44[0]) * c, dec - M44[1]) < 0.8:
                for p in pos(ra, dec):
                    dots.append((p[0], p[1], 0.05 + 0.03 * (8.5 - v)))
        if dots:
            s.dots(dots, fill="#FFFFFF", opacity=0.85)

    return [("十二次", ci12), ("鶉火", chunhuo), ("鳥形", bird), ("行星", planet), ("深空天體", deep)]


def write_custom(m, S, layers, discs=False):
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
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-35,
               w_c=34, feather=8, x_tN=XTN, x_tS=XTS, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    CI = ci_bounds(S)

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key, disc=False):
        it = dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)
        if disc:
            it["disc"] = True
        return it

    H = {k: uniq(C[k]) for k in C}

    # ── 宿名（長圖；朱雀紅）＋《天官書》的鳥 ──
    SU_OFF = {"010": (0.0, -6.6), "007": (5.6, 2.6), "013": (-1.0, -3.6), "027": (-9.0, 1.0),
              "030": (0.0, -4.6), "029": (3.0, 11.0), "031": (2.0, -6.0)}
    XIU = [item(H[k], nm, "red", 1.8, *SU_OFF[k], nm) for k, nm in zip(SEVEN, SEVEN_ZH)]
    # 迄格把宿名換成「宿名：部位」（同位置，不上下疊兩行）
    TG = [item(H[k], f"{nm}：{part}" if part else nm, "red", 1.7, *SU_OFF[k], f"{nm}-天官書")
          for k, nm, part in (("010", "井宿", ""), ("007", "鬼宿", ""), ("013", "柳宿", "鳥嘴"),
                              ("027", "星宿", "脖子"), ("030", "張宿", "嗉囊"), ("029", "翼宿", "翅膀"),
                              ("031", "軫宿", "車"))]
    # ── 十二次（色帶下方 dec −36）──
    # 04 迄格（cy 0、fov 54）：dec −31 ＝ 畫面 Y≈1580，山稜線上方；鶉尾放在畫面內那一段（RA 168）
    CIL = [item((ra, -31.0), nm, "red", 2.0, 0.0, 0.0, nm)
           for nm, ra in (("鶉首", (CI["鶉首"][0] + CI["鶉首"][1]) / 2), ("鶉火", (CI["鶉火"][0] + CI["鶉火"][1]) / 2),
                          ("鶉尾", 168.0))]
    # ── 天上的年夜飯 ──
    FE = [item(H["013"], "柳宿：廚師", "amber", 1.4, -1.0, -3.6, "柳-廚宰"),
          item(H["030"], "張宿：廚房", "amber", 1.4, 3.0, -4.6, "張-廚"),
          item(H["107"], "積薪", "amber", 1.4, 0.0, 2.6, "積薪"),
          item(H["120"], "酒旗", "amber", 1.4, -4.0, 0.0, "酒旗"),
          item(H["256"], "天樽", "amber", 1.4, -3.0, -3.0, "天樽"),
          item(H["007"], "鬼宿：祭祀", "amber", 1.4, 7.4, 2.6, "鬼-祠事")]
    # ── 今年除夕（20:00）──
    PLB = [item((PL["木星"]["ra"], PL["木星"]["dec"]), "木星 −2.6 等", "white", 1.3, 0.0, 2.6, "木星"),
           item([REGULUS], "軒轅十四", "white", 1.1, 0.0, -2.2, "軒轅十四"),
           item((PL["火星"]["ra"], PL["火星"]["dec"]), "火星", "red", 1.3, 0.0, -2.4, "火星"),
           item((160.0, -6.0), "鶉火", "red", 1.8, 0.0, 0.0, "鶉火-11")]
    # ── 南盤：台北面南（fov 74；字級 1.8 ≈ Canva 45 px）──
    TPE_L = [item(H["013"], "柳宿", "red", 1.8, 0.0, -4.0, "台北-柳宿", disc=True),
             item(H["027"], "星宿", "red", 1.8, 0.0, -5.0, "台北-星宿", disc=True),
             item(H["030"], "張宿", "red", 1.8, 0.0, -4.4, "台北-張宿", disc=True),
             item(((CI["鶉火"][0] + CI["鶉火"][1]) / 2, -27.0), "鶉火", "red", 2.2, 0.0, 0.0, "台北-鶉火", disc=True),
             item((PL["木星"]["ra"], PL["木星"]["dec"]), "木星", "white", 1.6, 0.0, 3.0, "台北-木星", disc=True)]
    # ── 積尸氣、鬼金羊（fov 16：字級 0.65 ≈ Canva 75 px）──
    GUI = [item(M44, "積尸氣（M44）", "white", 0.6, 0.0, -3.0, "積尸氣"),
           item(H["007"], "鬼宿", "red", 0.75, 0.0, 2.5, "鬼宿-13"),
           item(H["007"], "鬼金羊", "amber", 0.75, 0.0, -5.0, "鬼金羊")]
    # ── 西方 ──
    WE = [item((158.0, -25.0), "長蛇座", "blue", 1.5, 0.0, 0.0, "Hya"),
          item(uniq(W["Crt"]), "巨爵座（杯子）", "blue", 1.3, 0.0, 9.5, "Crt"),
          item(uniq(W["Crv"]), "烏鴉座", "blue", 1.5, 0.0, 5.2, "Crv"),
          item(uniq(W["Crv"]), "＝軫宿", "red", 1.5, 0.0, -6.6, "Crv-軫")]
    # ── 開場 ──
    OPEN = [item([CANOPUS], "老人星", "white", 1.3, 0.0, -2.8, "老人星")]
    # ── 北盤：四象方位（fov 160：字級 4.2 ≈ Canva 48 px；rot −24 時南在下）──
    SX = [item((LST0 + 24.0, 25.0), "前・朱雀", "red", 4.2, 0.0, 0.0, "前朱雀", disc=True),
          item((LST0 + 24.0 + 180.0, 25.0), "後・玄武", "blue", 4.2, 0.0, 0.0, "後玄武", disc=True),
          item((LST0 + 24.0 + 90.0, 42.0), "左・青龍", "green", 4.2, 0.0, 0.0, "左青龍", disc=True),
          item((LST0 + 24.0 - 90.0, 42.0), "右・白虎", "white", 4.2, 0.0, 0.0, "右白虎", disc=True)]
    # ── 北盤：下集（fov 110）──
    NX = [item([POLARIS], "北極星", "white", 2.6, 0.0, -4.4, "北極星", disc=True),
          item([DUBHE, ALKAID, 53910, 58001, 59774, 62956, 65378], "北斗", "white", 2.8, 0.0, -7.0, "北斗", disc=True),
          item([SCHEDAR, 746, 4427, 6686, 8886], "仙后座", "white", 2.6, 0.0, 6.0, "仙后", disc=True),
          item([MIRFAK], "英仙座", "white", 2.6, 0.0, -4.6, "英仙", disc=True)]

    label_sets = [(OPEN, "開場"), (XIU, "宿名"), (TG, "天官書"), (CIL, "十二次"), (FE, "年夜飯"),
                  (PLB, "今年除夕"), (TPE_L, "台北面南"), (GUI, "積尸氣"), (WE, "西方"),
                  (SX, "四象方位"), (NX, "下集")]

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
    yp = m.y_pole
    xc_, yc_ = m.pos_primary(*S[CANOPUS][:2])
    OPEN0 = (0.0, round(yc_ + 8.0, 1), 44.0, 0.0)        # 南走廊：老人星在右下
    OPEN1 = (0.0, 2.0, 48.0, 0.0)                        # 井、鬼、柳（長蛇頭）、南河三、天狼星
    N4A = (0.0, round(yp, 3), 160.0, ROT_N + 10.0)        # 北盤全天方位（轉到 −24°：朱雀在下）
    N4B = (0.0, round(yp, 3), 160.0, ROT_N)
    S7A = (14.0, -5.0, 48.0, 0.0)                         # 井、鬼（cy −5：七宿偏南，畫面置中；底邊 −48.6 ≤ D_r）
    S7B = (-50.0, -5.0, 49.0, 0.0)                        # 星、張、翼、軫（柳在右緣）
    CI12 = (-30.0, 0.0, 54.0, 0.0)                        # 十二次：首（右）火（中）尾（左）
    LIU = (-18.0, 2.0, 36.0, 0.0)                         # 柳宿特寫（兩個火）
    FEAST_F = (-15.0, 2.0, 52.0, 0.0)                     # 年夜飯：天樽…張
    HUO = (-34.0, 0.0, 44.0, 0.0)                         # 鶉火段
    PLAN = (-36.0, 4.0, 30.0, 0.0)                        # 木星、軒轅十四、火星、星宿、張宿

    def FS(t):                                            # 台北面南：南方地平線在畫面 Y≈1650
        return (0.0, round(-yp + 82.3, 2), 74.0, ROT[t])
    GUI0 = (-12.0, 12.0, 36.0, 0.0)
    GUI1 = (-13.0, 19.2, 16.0, 0.0)                       # 鬼宿＋M44
    WEST0 = (-30.0, -5.0, 44.0, 0.0)
    WEST1 = (-58.0, -8.0, 40.0, 0.0)                      # 巨爵、烏鴉＝軫宿
    NX0 = (0.0, round(yp, 3), 110.0, -69.0)               # 北斗在下、仙后在上
    NX1 = (0.0, round(yp, 3), 110.0, -76.0)

    def ls(*names):
        return list(names)

    shots = [
        dict(code="01", kind="T", sec=8, north=False,
             frames=[OPEN0, OPEN1], layers=["朱"], labels=[], labels_start=ls("開場"),
             vo="上週在沙漠看老人星；今晚除夕，回到中國：同一片星空，古代中國人看見——一隻朱雀。",
             card="除夕・朱雀",
             note="開場字卡；南走廊 T：老人星（右下，承接上集）往上到井、鬼、柳（長蛇頭）；"
                  "逐字稿原寫 Z，帶↔盤之間的移動依規定改 T"),
        dict(code="02", kind="R", sec=12, north=True,
             frames=[N4A, N4B], layers=SIX, labels=ls("四象方位"),
             overlay="C-A20-06_前朱鳥後玄武", overlay_layers=["三象層", "引文層", "朱雀層"],
             vo="青龍、玄武、白虎之後，四象只差最後一隻。《禮記》說，軍隊出發，「前朱鳥而後玄武，左青龍而右白虎」——朱雀，走在最前面。",
             card="前朱鳥，後玄武",
             note=f"【自動換組】長圖→北盤；北盤拉遠到 fov 160、逆時針轉到 {ROT_N:+.0f}°（下南上北、左東右西＝面南仰看）；"
                  "四象四色連線；9:16 畫面左右只看得到青龍、白虎的內緣 → 結束後定格疊概念圖 C-A20-06"
                  "（三象層 → 引文層 → 朱雀層最後亮）"),
        dict(code="03", kind="Z", sec=12, north=True,
             frames=[S7A, S7B], layers=["朱", "鳥"], labels=ls("宿名"), labels_end=ls("天官書"),
             vo="牠的七宿是：井、鬼、柳、星、張、翼、軫。司馬遷這樣拼出一隻鳥：柳是鳥嘴，星宿是脖子，張是嗉囊，翼是翅膀；最後的軫，是一輛車。",
             card="柳嘴・星頸・張嗉・翼翅",
             note="【自動換組】北盤→長圖；由西往東（右→左）滑過七宿（紅；cy −5 讓七宿置中，底邊進縫合帶，依規定記為 Z）；鳥形淡線（白虛線）；"
                  "迄格宿名換成天官書標籤（柳宿：鳥嘴／星宿：脖子／張宿：嗉囊／翼宿：翅膀／軫宿：車）；柳宿在迄格右緣外（9:16 一格放不下 50° 寬的鳥：柳嘴在中段經過，迄格看星頸、張嗉、翼翅、軫車）"),
        dict(code="04", kind="Z", sec=13, north=True,
             frames=[S7B, CI12], layers=["朱", "次"], labels_start=ls("天官書"), labels=ls("宿名", "十二次"),
             vo="這隻鳥還有個名字：鶉，字面上就是鵪鶉。這段天空切成三塊：井、鬼是鶉首，柳、星、張是鶉火，翼、軫是鶉尾。《爾雅》說：「柳，鶉火也。」",
             card="鶉首・鶉火・鶉尾",
             note="拉遠；十二次色帶（鶉首淡紅、鶉火亮紅、鶉尾淡紅），邊界照《晉書・天文志》度數等比換算；"
                  "畫面右緣＝鶉首、中＝鶉火、左＝鶉尾（井宿在畫面右外）"),
        dict(code="05", kind="Z", sec=12, north=True,
             frames=[CI12, LIU], layers=["朱", "鶉火"], labels_start=ls("十二次"), labels=ls("宿名"),
             overlay="C-A20-01_兩個火", overlay_layers=["柳宿層", "心宿層", "火正層"],
             vo="為什麼叫火？《左傳》說，上古管火的官，有的看心宿，有的看柳宿：「咮為鶉火，心為大火」，看它們隨季節出沒，決定一年什麼時候用火。",
             card="咮為鶉火，心為大火",
             note="推近柳宿；結束後定格疊概念圖 C-A20-01（柳宿層 → 心宿層 → 火正層）"),
        dict(code="06", kind="Z", sec=14, north=True,
             frames=[LIU, FEAST_F], layers=["朱", "飯"], labels_start=ls("宿名"), labels=ls("年夜飯"),
             vo="除夕要吃年夜飯，朱雀身邊也有一桌：柳宿是廚師，張宿是廚房；旁邊有柴火堆叫積薪、酒官的旗子叫酒旗，還有盛粥的天樽。鬼宿管祭祀——先祭祖，再開飯。",
             card="天上的年夜飯",
             note="拉遠；七宿（紅）＋積薪、酒旗、天樽（琥珀）；迄格開年夜飯標籤（只標旁白講到的六個；外廚、爟不標）"),
        dict(code="07", kind="Z", sec=13, north=True,
             frames=[FEAST_F], layers=["朱", "飯"], labels=ls("年夜飯"),
             overlay="C-A20-02_一顆蛋", overlay_layers=["河邊層", "蛋層", "契層"],
             vo="標題的那顆蛋呢？《詩經》唱：「天命玄鳥，降而生商。」《史記》說，簡狄去洗澡，看見玄鳥掉下一顆蛋，吞下去就懷孕，生了契——商朝的祖先。",
             card="天命玄鳥，降而生商",
             note="畫面不動；定格疊概念圖 C-A20-02（河邊層 → 蛋層 → 契層）；「契」字幕加注音（ㄒㄧㄝˋ）"),
        dict(code="08", kind="Z", sec=13, north=True,
             frames=[FEAST_F], layers=["朱", "飯"], labels=ls("年夜飯"),
             overlay="C-A20-02_一顆蛋", overlay_layers=["燕子層"],
             vo="不過，下這顆蛋的不是朱雀。「玄」是黑色，古人注解說玄鳥就是燕子，春分前後飛回來。商朝人看重的星，也不是鶉火，而是青龍的心：大火。",
             card="玄鳥＝黑色的燕子",
             note="畫面不動；C-A20-02 換成燕子層（黑燕剪影＋「商主大火」＋心宿）"),
        dict(code="09", kind="Z", sec=16, north=True,
             frames=[FEAST_F, HUO], layers=["朱", "鶉火"], labels_start=ls("年夜飯"), labels=ls("宿名"),
             overlay="C-A20-03_紅鳥興周", overlay_layers=["火落屋頂層", "赤烏層", "歲在鶉火層"], overlay_at="start",
             vo="紅色的鳥，要等到周朝。《史記》說，周武王渡過黃河，一團火落到他的屋頂，變成一隻紅色的烏鴉。《國語》記著：武王伐紂那年，「歲在鶉火」——木星正停在鶉火，而鶉火，就是周的分野。",
             card="紅鳥興周・歲在鶉火",
             note="起格定格疊概念圖 C-A20-03（火落屋頂 → 赤烏 → 歲在鶉火）；收掉後滑到長圖鶉火段（鶉火色帶）"),
        dict(code="11", kind="Z", sec=17, north=True,
             frames=[HUO, PLAN], layers=["朱", "鶉火", "行"], labels_start=ls("宿名"), labels=ls("今年除夕"),
             vo="巧的是，今年除夕，木星也在鶉火。晚上八點往東看：最亮的那顆是木星，負二點六等；下面是軒轅十四，再下面偏紅的是火星，同樣落在鶉火。兩顆行星這個月都衝日，整夜看得到。",
             card="今年除夕・歲在鶉火",
             note="推近；鶉火色帶＋行星層（2/5 20:00 位置：木星 白大點、火星 紅點，都在黃道上、星宿張宿北方 24–28°）；"
                  "星圖上三顆左右排（東在左），實際東方天空是上下一直線 → 角落小字「實際天空：由上而下 木星・軒轅十四・火星」"
                  "＋「木星 −2.55 等（Mallama & Hilton 2018）」"),
        dict(code="12", kind="R", sec=13, north=False, horizon=[PHI],
             frames=[FS("22:00"), FS("00:00")], layers=["朱", "鶉火", "行"], labels=ls("台北面南"),
             overlay="C-A20-05_除夕抬頭看",
             vo="守歲到半夜十二點，抬頭往南：柳宿、星宿、張宿正好掛在最高處，整個鶉火跨過正南；木星也快到頭頂。新月在大年初一，今晚沒有月光。",
             card="午夜・鶉火過中天",
             note=f"【自動換組】長圖→南盤；台北面南（山＝南方地平線），盤順時針 22:00→00:00"
                  f"（{ROT['22:00']:+.1f}°→{ROT['00:00']:+.1f}°）；鶉火色帶跨過子午線（畫面中線）；"
                  "之後疊 9:16 圖卡 C-A20-05（可存圖）"),
        dict(code="13", kind="Z", sec=13, north=True,
             frames=[GUI0, GUI1], layers=["朱", "深空"], labels_start=[], labels=ls("積尸氣"),
             vo="鬼宿中間那團朦朧的光，叫積尸氣，今天叫蜂巢星團，暗處肉眼看得到。二十八宿各配一隻動物，鬼宿配的是羊：鬼金羊——明天，就是羊年。",
             card="積尸氣・鬼金羊",
             note="【自動換組】南盤→長圖；推近鬼宿＋M44（深空天體層）；迄格標籤 積尸氣（M44）、鬼宿、鬼金羊"),
        dict(code="14", kind="S", sec=12, north=True,
             frames=[WEST0, WEST1], layers=["朱", "西"], labels_start=ls("宿名"), labels=ls("西方"),
             vo="西方人在這段天空，看到一條長長的水蛇、一個杯子和一隻烏鴉。朱雀的尾巴軫宿，就是烏鴉座——繞了一圈，還是一隻鳥。",
             card="軫宿＝烏鴉座",
             note="拉遠；西方長蛇／巨爵／烏鴉（藍）疊在朱雀七宿（紅）上；S 往東到軫宿＝烏鴉座"),
        dict(code="15", kind="R", sec=4, north=True,
             frames=[N4B], layers=SIX, labels=ls("四象方位"),
             overlay="C-A20-04_四象總圖",
             vo="青龍、玄武、白虎、朱雀，四象到齊。",
             card="四象到齊",
             note="【自動換組】長圖→北盤（同 02 鏡方位），四象四色連線同時亮；後 2 秒疊 9:16 圖卡 C-A20-04（角落貼紙「可存圖」）"),
        dict(code="16", kind="R", sec=8, north=True,
             frames=[NX0, NX1], layers=["L4"], labels=ls("下集"),
             vo="新年快樂。下週五往北到北極圈：薩米人的整片星空，是一場還沒結束的狩獵。",
             card="下集｜薩米：星空狩獵圖",
             note="北盤拉近到 fov 110：北極星居中，仙后—英仙（御夫在畫面右緣外）在上、北斗在下，逆時針慢轉；端卡＋追蹤 CTA"),
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
            if sh["kind"] == "R":
                xt = m.xtN if sh["north"] else m.xtS
                yc0 = m.y_pole if sh["north"] else -m.y_pole
                which = ("北盤" if sh["north"] else "南盤") + "圖層組（置中）"
                ew = 2 * m.R_fill / fov * 1080
                off = (round(-(cx - xt) / fov * 1080), round((cy - yc0) / fov * 1080))
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
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  台北地方恆星時：" + "、".join(f"{k} {v:.2f}°（南盤 rot {ROT[k]:+.2f}°）" for k, v in LSTS.items()))
    print("  十二次（J2000 赤經）：" + "、".join(f"{k} {a:.1f}–{b:.1f}°" for k, (a, b) in CI.items()))
    print("  行星（2/5 20:00，J2000）：" + "、".join(
        f"{k} RA {v['ra']:.2f} Dec {v['dec']:+.2f}（高 {v['alt']:.1f}° 方位 {v['az']:.1f}°；x {x_of(v['ra']):+.1f}）"
        for k, v in PL.items()))
    print("  x：" + "、".join(f"{nm} {x_of(centroid(H[k], S)[0]):+.1f}" for k, nm in zip(SEVEN, SEVEN_ZH)))

    def T(hips, 中文, 英文, 顏色, 備註, 原文=None):
        return dict(hips=hips, 原文=原文 or 中文.split("（")[0], 拼音="", 英文翻譯=英文, 中文=中文,
                    顏色=顏色, 來源備註=備註)

    terms = {
        "井宿": T(H["010"], "井宿（東井；鶉首）", "Well", "red", "南方朱雀第一宿；距星 μ Gem"),
        "鬼宿": T(H["007"], "鬼宿（輿鬼；主祠事）", "Ghosts", "red", "《史記・天官書》輿鬼，鬼祠事；二十八禽 鬼金羊"),
        "柳宿": T(H["013"], "柳宿（鳥嘴；天之廚宰）", "Willow", "red",
                "《天官書》柳為鳥注；《爾雅》柳，鶉火也；《晉書》天之廚宰"),
        "星宿": T(H["027"], "星宿（七星；鳥頸）", "Star", "red", "《天官書》七星，頸；距星 α Hya 星宿一"),
        "張宿": T(H["030"], "張宿（嗉囊；為廚，主觴客）", "Extended Net", "red", "《天官書》張，素，為廚，主觴客"),
        "翼宿": T(H["029"], "翼宿（羽翮＝翅膀）", "Wings", "red", "《天官書》翼為羽翮"),
        "軫宿": T(H["031"], "軫宿（車）", "Chariot", "red", "《天官書》軫為車；西方烏鴉座"),
        "鶉首": T([], "鶉首（井十六度—柳八度）", "Quail's Head", "red", "十二次；未；秦之分野（《晉書・天文志》）"),
        "鶉火": T([], "鶉火（柳九度—張十六度）", "Quail Fire", "red", "十二次；午；周之分野"),
        "鶉尾": T([], "鶉尾（張十七度—軫十一度）", "Quail's Tail", "red", "十二次；巳；楚之分野"),
        "積薪": T(H["107"], "積薪（柴火堆）", "Pile of Firewood", "amber", "《晉書》供庖廚之正也"),
        "酒旗": T(H["120"], "酒旗（酒官之旗）", "Banner of Wine Shop", "amber", "《晉書》酒官之旗也，主宴饗飲食"),
        "天樽": T(H["256"], "天樽（盛粥的器）", "Celestial Wine Cup", "amber",
                "Stellarium 作天罇；《晉書》主盛饘粥（不是酒器）"),
        "積尸氣": T([], "積尸氣（M44 蜂巢星團）", "Praesepe (Beehive Cluster)", "white", "《步天歌》中央白者積尸氣"),
        "鬼金羊": T(H["007"], "鬼金羊", "", "amber", "二十八禽（唐宋以後定型）；2027 丁未羊年"),
        "木星": T([], "木星（歲星）", "Jupiter", "white", "2027/2/5 20:00 在星宿（鶉火）；−2.55 等（Mallama & Hilton 2018）"),
        "火星": T([], "火星（熒惑）", "Mars", "red", "2027/2/5 在張宿 11°（鶉火）；2/19 衝"),
        "軒轅十四": T([REGULUS], "軒轅十四", "Regulus", "white", "α Leo"),
        "長蛇座": T(uniq(W["Hya"]), "長蛇座", "Hydra", "blue", "西方"),
        "巨爵座": T(uniq(W["Crt"]), "巨爵座", "Crater", "blue", "西方：杯子"),
        "烏鴉座": T(uniq(W["Crv"]), "烏鴉座", "Corvus", "blue", "西方；＝軫宿"),
        "老人星": T([CANOPUS], "老人星", "Canopus", "white", "承接 A-19"),
    }
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY,
               "line_groups": LINE_GROUPS, "lst0": LST0, "rot_taipei": ROT, "rot_north": ROT_N, "phi": PHI,
               "ci_bounds_j2000": CI, "planets_20h": PL},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    sb_labels = XIU + TG + CIL + FE + PLB + TPE_L + GUI + WE + OPEN + SX + NX
    m.sb_grid(os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), shots,
              line_groups=LG_SEVEN + LG_FEAST + LG_QL + LG_XW + LG_BH + LG_WEST,
              labels=[dict(it, pt=5) for it in sb_labels],
              title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
