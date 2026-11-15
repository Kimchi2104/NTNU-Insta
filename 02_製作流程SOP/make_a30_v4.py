# -*- coding: utf-8 -*-
"""A-30 呂埃勒：1786 年，一張只有線的星圖｜大畫布 v4.6（長圖帶狀為主；不用南北盤鏡頭）

論點：星星是天文，連線是文化。同一隻獅子，Stellarium 預設 10 條線、H. A. Rey 18 條、
Alexandre Ruelle《Nouvelle Uranographie》（1786）32 條。IAU 1922／1928 只定名字與邊界，沒有規定連線。

來源：Stellarium ruelle（Doina Bucur 數位化）、western（預設連線）、western_rey（H. A. Rey 1952）、
  western 的 edges（IAU 1928 Delporte 邊界，B1875，pbarbier edges_18）→ 精確歲差轉 J2000；
  sardinian 007 Sa Frache（A-29 接續）、indian N02 Bharaṇī（A-28 接續）。全部連線照原樣，沒有修改。
逐字稿：04_腳本庫/A-30-呂埃勒1786年一張只有線的星圖-逐字稿-v1.md。天象 PyEphem 4.2.1 自算（台北）。

圖層
  L4 星座連線＝Ruelle 全天 70 個星座（琥珀，638 段）
  額外連線：Stellarium 預設（白，674 段）、Rey（藍，911 段，含 Rey 的星群）、
           Sa Frache（綠，A-29）、Bharaṇī（藍，A-28）
  自訂層：IAU 邊界（淡灰虛線，全天）、IAU 邊界-小獅座（只有 LMi 那幾條）、小獅座五星紅圈、
          火星與木星 4/30 20:00（台北站心 J2000）

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 162 → 獅子座質心在 x≈0（軒轅十四 +10、五帝座一 −15）。長圖切口 x＝±180 在 RA 342（飛馬—雙魚之間），
             本集要上長圖的天區：白羊（北蒼蠅 +121）、金牛（昴宿 +105）…一路往東到人馬（−115）、地獄犬（−113），
             切口兩側 RA 290–20 都用不到，全片在一張連續長圖上。
  D_s = 65、D_r = 69 → 決定因素是 15 鏡的南十字（十字架二 −63.1）與 08b 鏡的南船（Ruelle Le Vaisseau 最南 −70.0）：
             D_s 62 時南十字落在走廊（x≈−25，走廊 ±26 全權混合）裡的縫合帶，十字會變形。
             北邊最高是牧夫 θ +51.8（13 鏡）、大熊 +63.1（06 鏡畫面上緣），都在帶內。
             S 鏡 |cy|＋fov·8/9 ≤ 65：08c fov 30 ✓；15 鏡改用 Z 驗證（見 note）；08c fov 30、cy +22 → 48.7 ✓。
  D_fill = 25 → k＝2.7284、R_fill＝177.35（|x_t|＋R_fill＝177.35 ≤ 180 ✓；D_fill 24 會到 180.1，超過）。
             盤寬 ÷ 畫布寬＝0.98528（⚠ 接近 1，跟 A-04 一樣「看起來像同寬」；本集沒有盤鏡頭，盤組只是備用）。
  x_tN = x_tS = 0。本集沒有 R 鏡頭；build_discs 照規定呼叫（盤組備用、亂數一致）。
  所有構圖的上下緣都在 |y| ≤ 69（D_r）以內：走廊外 D_r 以外是填滿圓（重複的天），會有錯位縫——
  逐字稿 02 鏡寫 fov 80、06 鏡寫 fov 100，改成 76（9:16 高 135°＝帶內最大），在 note 註明。

鏡頭路線（全部大畫布；逐字稿 15 鏡拆成 20 格，旁白照原文切開，秒數照字數分，總長 211 不變）
  01 Sa Frache（綠）fov 40 → 01b 換預設連線（白）推到 30 → 02 拉遠 76＋IAU 邊界（連線全關）
  → 03／03b／03c 推近獅子 76→34，每格換一層：預設（白）→ Rey（藍）→ Ruelle（琥珀）
  → 04、05 定格（Ruelle 獅子；授權圖由美宣疊）→ 06 拉遠 76：Ruelle 全天 → 07 推近 30：幾何獅子＋小獅座五星
  →【硬切】08 地獄犬（武仙手上，RA 18h）→【硬切】08b 南船 →【硬切】08c S 昴宿→白羊：北蒼蠅＋Bharaṇī
  →【硬切】09 回獅子 fov 60（C-A30-01）→ 10 同框（敦煌星圖授權圖）→ 11 同框 → 12 同框（C-A30-02）
  → 13 滑到 獅子—室女—牧夫 fov 72 三層同開 → 14 拉到 fov 70 這週末的南天（火星、巨爵；圖卡 C-A30-03）
  →【硬切】15 南十字＋煤袋 fov 30 → 往東滑到天蠍＋人馬 fov 40（下集鴯鶓）。

硬切（判斷後接受）：07→08（隔 113°，換段「還有幾個消失的星座」）、08→08b（隔 140°）、08b→08c（隔 88°）、
  08c→09（隔 122°，「可惜……太早了」換段）、14→15（圖卡收掉後換到下集預告）。其餘照預設 Match & Move（≤ 2.5 秒滑過，其餘時間停著）。
check_shots：全部 Z／S，沒有 R，沒有 ⚠ 需要接受。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-30"
OUT = os.path.join(BASE, "05_素材/A-30_呂埃勒/_v4大畫布")
LST0 = 162.0
D_S, D_R, D_FILL = 65.0, 69.0, 25.0
TPE = (25.0330, 121.5654)
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem 4.2.1；台北站心；J2000 astrometric）
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.temp, o.pressure = 20.0, 1010.0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def _topo_j2000(b, o):
    import ephem
    q = ephem.Equatorial(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


def bodies():
    import ephem
    out = {}
    o = _obs("2027/4/30 20:00")
    for nm, b in (("火星", ephem.Mars()), ("木星", ephem.Jupiter())):
        b.compute(o)
        ra, dec = _topo_j2000(b, o)
        out[nm] = dict(ra=ra, dec=dec, alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                       mag=round(float(b.mag), 2), con=ephem.constellation(b)[1])
    return out


PL = bodies()


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 一、連線資料
# ══════════════════════════════════════════════════════════════════
def load_sc(cu):
    d = json.load(open(os.path.join(SC_OLD, cu, "index.json"), encoding="utf-8"))
    return {c["id"]: c for c in d["constellations"]}, d


def segs_of(c):
    return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]


def n_edges(segs):
    return len({frozenset(p) for s in segs for p in zip(s, s[1:]) if p[0] != p[1]})


RU, _ = load_sc("ruelle")
WE, WE_D = load_sc("western")
RE, _ = load_sc("western_rey")
SEG_RU = [s for c in RU.values() for s in segs_of(c)]
SEG_WE = [s for c in WE.values() for s in segs_of(c)]
SEG_RE = [s for c in RE.values() for s in segs_of(c)]
SEG_RU_LEO = segs_of(RU["CON ruelle Leo"])
SEG_WE_LEO = segs_of(WE["CON western Leo"])
SEG_RE_LEO = segs_of(RE["CON western_rey Leo"])
SARD, _ = load_sc("sardinian")
SEG_FRACHE = segs_of(SARD["CON sardinian 007"])        # Sa Frache 鐮刀（A-29）
IND, _ = load_sc("indian")
SEG_BHARANI = segs_of(IND["CON indian N02"])           # Bharaṇī（A-28）
hips_of = lambda segs: sorted({h for s in segs for h in s})

REGULUS, ALGIEBA, DENEBOLA, ZOSMA = 49669, 50583, 57632, 54872
LMI5 = [49593, 51056, 51233, 52098, 53229]             # 21、30、31（β）、37、46 LMi
CRT_A, CRT_D, CRV_G, SPICA, ARCTURUS, THETA_BOO = 53740, 55282, 59803, 65474, 69673, 70497
MOUCHE = hips_of(segs_of(RU["CON ruelle MuB"]))         # 白羊 35、39、41
CERBERE = hips_of(segs_of(RU["CON ruelle Cer"]))
HERCULE = hips_of(segs_of(RU["CON ruelle Her"]))
VAISSEAU = hips_of(segs_of(RU["CON ruelle CarPupVel"]))
CANOPUS, ALCYONE, ACRUX, GACRUX, COALSACK = 30438, 17702, 60718, 61084, 62027
ANTARES, KAUS, RIGIL = 80763, 90185, 71683
LEO_RU = hips_of(SEG_RU_LEO)
MAINS = [REGULUS, ALGIEBA, DENEBOLA, ZOSMA, CRT_D, SPICA, ARCTURUS] + MOUCHE

assert n_edges(SEG_WE_LEO) == 10 and n_edges(SEG_RE_LEO) == 18 and n_edges(SEG_RU_LEO) == 32, "獅子線段數不符"
assert set(LMI5) <= set(LEO_RU), "小獅座五星不在 Ruelle 獅子裡"
assert MOUCHE == sorted(hips_of(SEG_BHARANI)), "北蒼蠅≠Bharaṇī"


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、IAU 邊界（B1875 → J2000）
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
    out = []
    for e in WE_D["edges"]:
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
# 三、自訂圖層
# ══════════════════════════════════════════════════════════════════
GREY = "#B8C2D6"


def custom_layers(m, S):
    RED = COLORS["red"]

    def iau(sel):
        def f(s, pos, runs, disc):
            rr = []
            for pts, a, b in EDGES:
                if sel(a, b):
                    rr += runs(pts)
            s.polylines(rr, stroke=GREY, w=m.lw * 0.45, opacity=0.55, dash="1.0 0.7")
        return f

    def lmi_rings(s, pos, runs, disc):
        for h in LMI5:
            for p in pos(*S[h][:2]):
                s.circle(p[0], p[1], 1.1, stroke=RED, w=0.14, opacity=0.95)

    def planets(s, pos, runs, disc):
        for nm, col, r in (("木星", "#FFFFFF", 0.42), ("火星", RED, 0.36)):
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.8, fill=col, opacity=0.16)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    return [("IAU邊界", iau(lambda a, b: True)),
            ("IAU邊界-小獅座", iau(lambda a, b: "LMI" in (a, b))),
            ("小獅座五星紅圈", lmi_rings),
            ("火星與木星4月30日", planets)]


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
# 四、連線分組
# ══════════════════════════════════════════════════════════════════
LG_RU = [(SEG_RU, "amber", 0.9)]
LG_WE = [(SEG_WE, "white", 0.8)]
LG_RE = [(SEG_RE, "blue", 0.8)]
LG_FR = [(SEG_FRACHE, "green", 1.1)]
LG_BH = [(SEG_BHARANI, "blue", 1.1)]
LINE_SETS = [(LG_WE, "連線-Stellarium預設"), (LG_RE, "連線-Rey"),
             (LG_FR, "連線-SaFrache（A-29）"), (LG_BH, "連線-Bharaṇī（A-28）")]
LINES_KEY = {"L4": "星座連線", "預": "連線-Stellarium預設", "Rey": "連線-Rey",
             "鐮": "連線-SaFrache（A-29）", "Bh": "連線-Bharaṇī（A-28）",
             "界": "IAU邊界", "界小": "IAU邊界-小獅座", "紅": "小獅座五星紅圈", "行": "火星與木星4月30日"}
LINE_GROUPS = {"L4": LG_RU, "預": LG_WE, "Rey": LG_RE, "鐮": LG_FR, "Bh": LG_BH,
               "界": [], "界小": [], "紅": [], "行": []}


# ══════════════════════════════════════════════════════════════════
# 五、旁白字數（中文字＋外文音節＋阿拉伯數字逐位；make_a28 同一套）
# ══════════════════════════════════════════════════════════════════
VOW = "aeiouyāīūṛṝḷēōáéíóúàèùâêîôûëïü"


def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏḀ-ỿ]+|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif w.isdigit():
            n += len(w)
        else:
            n += max(1, len(re.findall(f"[{VOW}]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 六、名詞總表（＝標籤對照表）(錨點, 片中寫法, Stellarium 寫法, 英文, 中文, 顏色, 備註)
# ══════════════════════════════════════════════════════════════════
def _ru(cid):
    return RU[f"CON ruelle {cid}"]["common_name"]["native"]


TERMS = [
    (LEO_RU, "Le Lion", _ru("Leo"), "Leo", "獅子座", "amber", "Ruelle 32 段／25 星；預設 10、Rey 18"),
    (hips_of(segs_of(RU["CON ruelle Vir"])), "La Vierge", _ru("Vir"), "Virgo", "室女座", "amber", "Ruelle 21 段"),
    (hips_of(segs_of(RU["CON ruelle Boo"])), "Le Bouvier", _ru("Boo"), "Boötes", "牧夫座", "amber", "Ruelle 20 段"),
    (hips_of(segs_of(RU["CON ruelle Crt"])), "La Coupe", _ru("Crt"), "Crater", "巨爵座", "amber",
     "Stellarium 為 ruelle 選的 highlight；最亮 δ 3.6 等"),
    (hips_of(segs_of(RU["CON ruelle Crv"])), "Le Corbeau", _ru("Crv"), "Corvus", "烏鴉座", "amber", ""),
    (hips_of(segs_of(RU["CON ruelle Hya"])), "L'Hydre Femelle", _ru("Hya"), "Hydra", "長蛇座", "amber",
     "法文用陰性／陽性區分兩條蛇"),
    (hips_of(segs_of(RU["CON ruelle Cnc"])), "L'ecrevisse", _ru("Cnc"), "Cancer", "巨蟹座", "amber",
     "照星圖拼法，不改成現代法文"),
    (hips_of(segs_of(RU["CON ruelle Com"])), "Chevelure de Berenice", _ru("Com"), "Coma Berenices", "后髮座",
     "amber", ""),
    (hips_of(segs_of(RU["CON ruelle UMa"])), "La Grande Ourse", _ru("UMa"), "Ursa Major", "大熊座", "amber",
     "原圖另連 M81、M82（Stellarium 未收）"),
    (hips_of(segs_of(RU["CON ruelle Gem"])), "Les Gemeaux", _ru("Gem"), "Gemini", "雙子座", "amber", ""),
    (CERBERE, "Cerbere", _ru("Cer"), "Cerberus (obsolete)", "地獄犬（已廢）", "amber", "Hevelius；武仙手上的三頭犬"),
    (HERCULE, "Hercule", _ru("Her"), "Hercules", "武仙座", "amber", ""),
    (VAISSEAU, "Le Vaisseau", _ru("CarPupVel"), "Argo Navis (obsolete)", "南船座（已廢）", "amber",
     "今分為船底、船尾、船帆"),
    (MOUCHE, "La Mouche", _ru("MuB"), "Musca Borealis (obsolete)", "北蒼蠅座（已廢）", "amber",
     "原圖只寫 La Mouche；「北蒼蠅」是後來的區分"),
    (MOUCHE, "Bharaṇī", "Bharani", "Bearer", "承載者（胃宿）", "blue", "A-28 印度第 2 宿；同三星"),
    (hips_of(SEG_FRACHE), "Sa Frache", "Sa Frache", "The Sickle", "鐮刀（A-29）", "green", "Stellarium sardinian 007"),
    (LMI5, "小獅座五星", "—", "five stars of today's Leo Minor", "21、30、31、37、46 LMi", "red",
     "HIP 49593、51056、51233、52098、53229"),
    ((PL["火星"]["ra"], PL["火星"]["dec"]), "火星", "—", "Mars", "火星", "red",
     f"台北 4/30 20:00 高 {PL['火星']['alt']}°、{PL['火星']['mag']} 等"),
    ((PL["木星"]["ra"], PL["木星"]["dec"]), "木星", "—", "Jupiter", "木星", "white",
     f"台北 4/30 20:00 高 {PL['木星']['alt']}°（14 鏡畫面外）"),
    ([COALSACK], "煤袋", "—", "Coalsack", "煤袋（A-31 鴯鶓的頭）", "white", "HIP 62027 一帶"),
]


# ══════════════════════════════════════════════════════════════════
# 七、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def radec_c(hips, S):
    v = [0.0, 0.0, 0.0]
    for h in hips:
        r, d = math.radians(S[h][0]), math.radians(S[h][1])
        v[0] += math.cos(d) * math.cos(r); v[1] += math.cos(d) * math.sin(r); v[2] += math.sin(d)
    n = math.sqrt(sum(c * c for c in v))
    return math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(v[2] / n))


def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = radec_c(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2), dy=round(dy, 2), key=key)

    def lab(a, orig, zh, col, fov, dx=0.0, dy=0.0, key=None, zh_col="white", k1=0.030, k2=0.024):
        s1, s2, gap = round(fov * k1, 2), round(fov * k2, 2), round(fov * 0.046, 2)
        key = key or orig
        out = [item(a, orig, col, s1, dx, dy + gap / 2, key)]
        if zh:
            out.append(item(a, zh, zh_col, s2, dx, dy - gap / 2, key + "-zh"))
        return out

    def one(a, text, col, fov, dx=0.0, dy=0.0, key=None, k=0.026):
        return [item(a, text, col, round(fov * k, 2), dx, dy, key or text)]

    # 字級：Canva px ≈ size×1.7×1080/fov；主名 ~55 px、譯名 ~45 px（Canva 夾在 36–96）
    # 長圖：東在左（dx<0＝畫面左）；dy>0＝畫面上
    T = {t[1]: t for t in TERMS}
    LEO_C = (radec_c(LEO_RU, S))
    F01 = 36.0
    LB_FR = lab(hips_of(SEG_FRACHE), "Sa Frache", "鐮刀（上週・薩丁尼亞）", "green", F01, dx=-9.0, dy=4.0)
    LB_WE = one(LEO_C, "Stellarium 預設的獅子", "white", F01, dx=0.0, dy=-12.0, key="預設獅子")
    F02 = 76.0
    IAU_ZH = [("Leo", "獅子"), ("LMi", "小獅"), ("Cnc", "巨蟹"), ("Sex", "六分儀"), ("Hya", "長蛇"), ("Crt", "巨爵"),
              ("Vir", "室女"), ("Com", "后髮"), ("UMa", "大熊"), ("Lyn", "天貓"), ("Crv", "烏鴉"), ("Ant", "唧筒"),
              ("CVn", "獵犬"), ("Boo", "牧夫"), ("CMi", "小犬"), ("Gem", "雙子"), ("Pyx", "羅盤"), ("Vel", "船帆"),
              ("Cen", "半人馬"), ("Mon", "麒麟"), ("Pup", "船尾")]
    LB_IAU = []
    for ab, zh in IAU_ZH:
        hs = hips_of(segs_of(WE[f"CON western {ab}"]))
        LB_IAU += one(hs, zh, "white", F02, key=f"IAU-{ab}", k=0.020)
    F03 = 60.0
    LB_N10 = one(LEO_C, "Stellarium 預設：10 條", "white", F03, dy=-13.0, key="10條", k=0.024)
    LB_N18 = one(LEO_C, "H. A. Rey：18 條", "blue", F03, dy=-13.0, key="18條", k=0.024)
    LB_N32 = one(LEO_C, "Ruelle 1786：32 條", "amber", F03, dy=-13.0, key="32條", k=0.024)
    F06 = 76.0
    LB_ALL = []
    for nm, dx, dy in (("Le Lion", 0, -10), ("La Vierge", 5, -6), ("La Coupe", 0, -8), ("Le Corbeau", 0, -6),
                       ("L'Hydre Femelle", 6, -6), ("L'ecrevisse", -6, -7), ("Chevelure de Berenice", 0, 5),
                       ("La Grande Ourse", 0, -8), ("Le Vaisseau", 0, 0), ("Les Gemeaux", 0, 6)):
        t = T[nm]
        LB_ALL += lab(t[0], nm, t[4].replace("（已廢）", ""), "amber", F06, dx=dx, dy=dy, k1=0.024, k2=0.019)
    F07 = 30.0
    LB_GEO = (lab(LMI5, "小獅座的五顆星", "今天屬於小獅座", "red", F07, dx=0.0, dy=4.2, zh_col="white")
              + one(LEO_C, "Le Lion", "amber", F07, dy=-12.5, key="LeLion07", k=0.030))
    F08 = 36.0
    LB_CER = (lab(CERBERE, "Cerbere", "地獄犬（已廢）", "amber", F08, dx=-1.0, dy=-5.0)
              + one(HERCULE, "Hercule 武仙", "white", F08, dx=2.0, dy=-2.0, key="Hercule", k=0.022))
    F08b = 56.0
    LB_ARGO = (lab(VAISSEAU, "Le Vaisseau", "南船座（已廢）", "amber", F08b, dx=0.0, dy=2.0)
               + one(VAISSEAU, "今分為 船底・船尾・船帆", "white", F08b, dy=-3.6, key="三分", k=0.020))
    F08c = 30.0
    LB_MOU = (lab(MOUCHE, "La Mouche", "北蒼蠅座（已廢）", "amber", F08c, dx=0.0, dy=3.6)
              + lab(MOUCHE, "Bharaṇī", "印度：月亮的一位妻子", "blue", F08c, dx=0.0, dy=-3.4))
    F09 = 60.0
    LB_SPR = []
    for nm, dx, dy in (("Le Lion", 0, -11), ("La Vierge", 0, -7), ("La Coupe", 0, -7), ("Le Corbeau", 0, -5),
                       ("Chevelure de Berenice", 9, 5)):
        t = T[nm]
        LB_SPR += lab(t[0], nm, t[4], "amber", F09, dx=dx, dy=dy, k1=0.026, k2=0.021)
    F13 = 72.0
    LB_3 = []
    for nm, zh, dx, dy in (("Le Lion", "獅子座", -7, -11), ("La Vierge", "室女座", 0, -7), ("Le Bouvier", "牧夫座", 0, -4)):
        LB_3 += one(T[nm][0], zh, "white", F13, dx=dx, dy=dy, key=f"三層-{zh}", k=0.026)
    LB_3 += one((LST0 + 26, -36.0), "白：Stellarium 預設", "white", F13, key="圖例白", k=0.020)
    LB_3 += one((LST0 + 26, -40.0), "藍：H. A. Rey", "blue", F13, key="圖例藍", k=0.020)
    LB_3 += one((LST0 + 26, -44.0), "琥珀：Ruelle 1786", "amber", F13, key="圖例琥珀", k=0.020)
    F14 = 70.0
    LB_WK = (one((PL["火星"]["ra"], PL["火星"]["dec"]), "火星（別連進去）", "red", F14, dx=1.0, dy=3.4, key="火星", k=0.022)
             + one([REGULUS], "軒轅十四", "white", F14, dx=3.0, dy=-2.8, key="軒轅十四", k=0.022)
             + one(LEO_C, "獅子座：頭頂", "amber", F14, dx=0.0, dy=17.0, key="獅子頭頂", k=0.026)
             + lab(T["La Coupe"][0], "巨爵座", "最亮 3.6 等・要暗處", "amber", F14, dx=0.0, dy=-8.0, k1=0.026, k2=0.020)
             + one([CRV_G], "烏鴉座", "white", F14, dx=-3.0, dy=-4.0, key="烏鴉", k=0.022)
             + one([SPICA], "角宿一", "white", F14, dx=3.0, dy=-2.6, key="角宿一", k=0.022))
    F15 = 34.0
    LB_NX = (lab((192.9, -62.5), "煤袋", "鴯鶓的頭（下集）", "white", F15, dx=7.5, dy=1.0, zh_col="purple")
             + one([GACRUX], "南十字", "white", F15, dx=0.0, dy=3.2, key="南十字", k=0.022)
             + one([ANTARES], "天蠍座", "white", F15, dx=-3.0, dy=3.2, key="天蠍", k=0.022)
             + one([KAUS], "人馬座", "white", F15, dx=0.0, dy=-3.4, key="人馬", k=0.022))

    label_sets = [(LB_FR, "SaFrache"), (LB_WE, "預設獅子"), (LB_IAU, "IAU星座名"), (LB_N10, "10條"),
                  (LB_N18, "18條"), (LB_N32, "32條"), (LB_ALL, "Ruelle全天"),
                  (LB_GEO, "幾何獅子"), (LB_CER, "地獄犬"), (LB_ARGO, "南船"), (LB_MOU, "北蒼蠅與Bharaṇī"),
                  (LB_SPR, "Ruelle春季"), (LB_3, "三層"), (LB_WK, "這週末"), (LB_NX, "下集")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 構圖 ════════════════════
    def P(h):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        return (x_of(ra), dec)

    def fr(pts, fov, dx=0.0, dy=0.0):
        pts = [P(h) for h in pts]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        lim = m.Dr - fov * 8 / 9 - 0.3                 # 上下緣不出 D_r（走廊外 D_r 以外是重複的填滿圓）
        cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), float(fov), 0.0)

    def fs(pts, fov, dx=0.0, dy=0.0):                  # S：|cy|+fov·8/9 ≤ D_s
        cx, cy, f, r = fr(pts, fov, dx, dy)
        lim = m.Ds - fov * 8 / 9 - 0.5
        return (cx, round(max(-lim, min(lim, cy)), 2), f, r)

    LEOH = [REGULUS, DENEBOLA] + LMI5
    F01a = fr(hips_of(SEG_FRACHE) + [DENEBOLA], 40.0, dy=-1.0)
    F01b = fr(LEOH, 30.0, dy=-3.0)
    F02b = fr(LEOH, 76.0, dx=-8.0)
    F03c = fr(LEOH, 34.0, dy=-3.0)
    F03a = fr(LEOH, 60.0, dy=-4.0)
    F03b = fr(LEOH, 46.0, dy=-3.5)
    F06 = fr(LEOH, 76.0, dx=0.0)
    F07 = fr(LEOH, 30.0, dy=-2.0)
    F08 = fr(CERBERE + HERCULE, 36.0, dx=-3.0, dy=-4.0)
    F08b = fr(VAISSEAU, 56.0, dy=6.0)
    F08ca = fs([ALCYONE], 30.0, dx=-8.0, dy=-2.0)
    F08cb = fs(MOUCHE, 30.0, dy=-4.0)
    F09 = fr([REGULUS, CRV_G, DENEBOLA, 61941], 60.0, dx=6.0, dy=2.0)
    F13 = fr([DENEBOLA, SPICA, THETA_BOO, ARCTURUS, 61941], 72.0, dx=4.0, dy=-2.0)
    F14 = fr(LEOH + [CRT_D, CRV_G, SPICA, (PL["火星"]["ra"], PL["火星"]["dec"])], 70.0, dx=4.0, dy=0.0)
    F15a = fr([ACRUX, GACRUX], 30.0, dx=-3.0, dy=0.0)
    F15b = fr([ANTARES, KAUS], 40.0, dx=-2.0)
    print("\n── 構圖 ──")
    for k, v in dict(F01a=F01a, F01b=F01b, F02b=F02b, F03a=F03a, F03b=F03b, F03c=F03c, F06=F06, F07=F07, F08=F08,
                     F08b=F08b, F08ca=F08ca, F08cb=F08cb, F09=F09, F13=F13, F14=F14, F15a=F15a, F15b=F15b).items():
        print(f"  {k} {v}")

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_RU)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_RU, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文；15 鏡拆成 20 格） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=4, north=True, frames=[F01a], layers=["鐮"], labels=ls("SaFrache"),
             vo="上週在薩丁尼亞，獅子座是一把鐮刀。",
             card="連線是誰畫的？",
             note="大畫布 fov 40：獅子座，先放 A-29 的 Sa Frache（綠，Stellarium sardinian 007）；開場字卡"),
        dict(code="01b", kind="Z", sec=10, north=True, frames=[F01a, F01b], layers=["預"], labels=ls("預設獅子"), labels_start=ls("SaFrache"),
             vo="今天換個問題：你手機上看到的星座連線，是誰畫的？同一片星空，一位巴黎天文學家看見——一張只有線的星圖。",
             card="連線是誰畫的？",
             note="綠線淡出、換成 Stellarium 預設連線（白）；推近 fov 40→30（Z）"),
        dict(code="02", kind="Z", sec=15, north=True, frames=[F01b, F02b], layers=["界"], labels=ls("IAU星座名"), labels_start=ls("預設獅子"),
             vo="先說答案：不是國際天文學聯合會。它在一九二〇年代定下八十八個星座，規定的只是天空裡的「邊界」，像地圖上的國界；裡面怎麼連線，從來沒規定。",
             card="只定邊界，不管連線",
             note="拉遠 fov 30→76（逐字稿寫 80；76＝畫面上下緣不出長圖帶的最大值）：連線層全部關掉，"
                  "只剩 IAU 星座邊界（淡灰虛線，1928 Delporte 邊界、B1875 轉 J2000）＋星座中文名；"
                  "角落小字「IAU 國際天文學聯合會」用原生文字"),
        dict(code="03", kind="Z", sec=7, north=True, frames=[F02b, F03a], layers=["預"], labels=ls("10條"), labels_start=ls("IAU星座名"),
             vo="所以同一隻獅子，可以有好多種畫法：星空軟體 Stellarium 預設的獅子，十條線；",
             card="同一隻獅子：10",
             note="推近 fov 76→60；邊界淡出、預設連線（白，獅子 10 段）淡入；右上角計數字卡「10」"),
        dict(code="03b", kind="Z", sec=4, north=True, frames=[F03a, F03b], layers=["Rey"], labels=ls("18條"), labels_start=ls("10條"),
             vo="畫《好奇猴喬治》的 H. A. Rey，用了十八條；",
             card="同一隻獅子：10／18",
             note="推近 fov 60→46；換 Rey 連線（藍，獅子 18 段）"),
        dict(code="03c", kind="Z", sec=4, north=True, frames=[F03b, F03c], layers=["L4"], labels=ls("32條"), labels_start=ls("18條"),
             vo="而一七八六年，有個人畫了三十二條。",
             card="同一隻獅子：10／18／32",
             note="推近 fov 46→34；換 Ruelle 連線（琥珀，獅子 32 段）"),
        dict(code="04", kind="Z", sec=14, north=True, frames=[F03c], layers=["L4"], labels=ls("32條"),
             vo="他叫 Alexandre Ruelle，三十歲，是巴黎天文台的「學生天文學家」。那年他出了一張近一公尺寬的星圖，標題就寫明：靠主要星星彼此的排列，輕鬆認星座。",
             card="呂埃勒 Ruelle",
             note="畫面不動（Ruelle 獅子 fov 34）；美宣另疊授權圖（BnF Gallica 公版掃描 GE C-4001，標題區特寫），"
                  "放在下半部、不要蓋住獅子"),
        dict(code="05", kind="Z", sec=8, north=True, frames=[F03c], layers=["L4"], labels=ls("32條"),
             vo="這張星圖，獻給當時十二三歲的少年公爵，也就是後來的法國國王路易－菲利普。",
             card="獻給少年公爵",
             note="畫面不動；授權圖定格在題獻區（小字照原圖逐字抄；KBR 作「à Son Altesse monseigneur le duc de Chartres」，"
                  "文化審稿說原圖有「Sérénissime」，以圖面為準）"),
        dict(code="06", kind="Z", sec=15, north=True, frames=[F03c, F06], layers=["L4"], labels=ls("Ruelle全天"), labels_start=ls("32條"),
             vo="當時的星圖，星座大多畫成神話人物和動物，星星藏在圖畫裡，不容易認。Ruelle 把圖畫全拿掉，只用直線把星星連起來——七十個星座，全變成幾何圖形。",
             card="七十個星座，只剩線",
             note="拉遠 fov 34→76（逐字稿寫 100；76＝帶內最大）：Ruelle 連線（琥珀）＋法文星座名；"
                  "前半疊美宣授權的同時代寓言圖星圖（Bode／Flamsteed 公版）對照，後半收掉"),
        dict(code="07", kind="Z", sec=12, north=True, frames=[F06, F07], layers=["L4", "紅", "界小"],
             labels=ls("幾何獅子"), labels_start=ls("Ruelle全天"),
             vo="看他的獅子：鐮刀、身體、後腿，被切成一個個三角形和多邊形；連今天屬於小獅座的五顆星，也一起畫進大獅子裡。",
             card="一隻幾何的獅子",
             note="推近獅子 fov 76→30；Ruelle 獅子（琥珀）；小獅座 21、30、31（β）、37、46 LMi 五星紅圈"
                  "（背上的五邊形）；IAU 小獅座邊界（淡灰虛線）"),
        dict(code="08", kind="Z", sec=5, north=True, frames=[F08], layers=["L4"], labels=ls("地獄犬"),
             vo="他的星圖上，還有幾個今天已經消失的星座：地獄犬、",
             card="消失的星座",
             note="【硬切】（隔 113°）武仙＋地獄犬 Cerbere（RA 18h，琥珀）fov 36"),
        dict(code="08b", kind="Z", sec=2, north=True, frames=[F08b], layers=["L4"], labels=ls("南船"),
             vo="南船座、",
             card="消失的星座",
             note="【硬切】南船 Le Vaisseau（琥珀，30 段）fov 56；小字「今分為船底・船尾・船帆」"),
        dict(code="08c", kind="S", sec=8, north=True, frames=[F08ca, F08cb], layers=["L4", "Bh"],
             labels=ls("北蒼蠅與Bharaṇī"),
             vo="北蒼蠅座。北蒼蠅座那三顆小星，在兩週前那集的印度，是月亮的一位妻子：Bharaṇī。",
             card="消失的星座",
             note="【硬切】長圖 S fov 30：從昴宿往西（畫面往右）捲到白羊座；北蒼蠅座 La Mouche（琥珀三角）"
                  "＋Bharaṇī（藍，同三顆星，A-28）同框，停到鏡尾"),
        dict(code="09", kind="Z", sec=14, north=True, frames=[F09], layers=["L4"], labels=ls("Ruelle春季"),
             overlay="C-A30-01_連線簡史",
             vo="可惜 Ruelle 這個點子太早了，當年沒有流行起來。歐洲的星圖要到十九世紀，才慢慢改畫連線；一九五二年，H. A. Rey 嫌那些線看不出形狀，又重畫了一次。",
             card="太早的點子",
             note="【硬切】回到獅子—室女 fov 60（Ruelle 春季星座）；迄格疊 C-A30-01「連線簡史」時間軸"
                  "（1786 Ruelle → 19 世紀慢慢普及 → 1922／1928 IAU → 1952 Rey）"),
        dict(code="10", kind="Z", sec=15, north=True, frames=[F09], layers=["L4"], labels=ls("Ruelle春季"),
             vo="其實在東亞，這件事一點也不新：現存最古老的完整星圖——七世紀的敦煌星圖，一千三百多顆星，就是用點和線，畫出兩百多個星官，比 Ruelle 早了一千一百年。",
             card="敦煌星圖・七世紀",
             note="畫面不動；美宣另疊授權圖（大英圖書館 Or.8210/S.3326 敦煌星圖，公版／館方授權版）"),
        dict(code="11", kind="Z", sec=14, north=True, frames=[F09], layers=["L4"], labels=ls("Ruelle春季"),
             vo="那 Ruelle 的星圖，怎麼會變成 Stellarium 的一套星空文化？因為二〇二一年，荷蘭特溫特大學的資訊學者 Doina Bucur，把它一條線一條線數位化。",
             card="Bucur・2021",
             note="畫面不動（Ruelle 春季星座 fov 60）；小字「Doina Bucur・University of Twente」（不放照片）"),
        dict(code="12", kind="Z", sec=18, north=True, frames=[F09], layers=["L4"], labels=ls("Ruelle春季"),
             overlay="C-A30-02_1802個連線", overlay_layers=["點陣層", "口音層"],
             vo="她拿五十六個星空文化、一千八百多個星座連線做比較，發現連線也有「口音」：源自中國的星座，多半用暗星連成簡單的形狀；源自美索不達米亞的，多半用亮星連成複雜的圖形。",
             card="連線也有口音",
             note="畫面不動；疊 C-A30-02 兩層：點陣（56 文化、1,802 個連線圖，示意）→ 口音（暗星＋簡單線／亮星＋三角網，"
                  "示意，不指認具體星官；不重繪論文圖）"),
        dict(code="13", kind="Z", sec=10, north=True, frames=[F13], layers=["預", "Rey", "L4"], labels=ls("三層"),
             vo="換句話說，你在 App 裡看到的線，是幾百年來很多人的選擇疊起來的——星星是天文，連線，是文化。",
             card="星星是天文，連線是文化",
             note="滑到 獅子—室女—牧夫 fov 72：預設（白）、Rey（藍）、Ruelle（琥珀）三層同時開（刻意疊起來）；"
                  "牧夫北端 θ Boo +51.8° 在長圖帶內（D_s 65）"),
        dict(code="14", kind="Z", sec=23, north=True, frames=[F14], layers=["L4", "行"], labels=ls("這週末"),
             overlay="C-A30-03_這週末抬頭看",
             vo="這週末在台灣：天黑到午夜前，獅子座高掛頭頂；鐮刀旁那顆橘紅色的亮星是火星，別連進去。往南看，半天高有一個小杯子，是巨爵座，要到暗一點的地方才看得到。月亮後半夜才升起，正好。拿張紙，照你的眼睛連連看——你的線，也是一種星空文化。",
             card="這週末抬頭看",
             note=f"拉遠 fov 70：獅子（上）＋火星（4/30 20:00 台北站心 J2000，離軒轅十四 "
                  f"{sep((PL['火星']['ra'], PL['火星']['dec']), S[REGULUS][:2]):.1f}°）、巨爵（下）、烏鴉、角宿一；"
                  "木星在畫面右外不標；「月亮後半夜」起疊 9:16 圖卡 C-A30-03「這週末抬頭看」（可存圖）"),
        dict(code="15", kind="Z", sec=9, north=True, frames=[F15a, F15b], layers=[], labels=ls("下集"),
             vo="下週五，我們飛到澳洲：那裡的人不只連星星，也連銀河裡的黑影——一隻由黑暗組成的鴯鶓。",
             card="下集見｜卡米拉羅伊與尤瓦萊：由黑暗組成的鴯鶓",
             note="長圖 fov 30→40：硬切到南十字＋煤袋（鴯鶓的頭），再往東（畫面往左）滑到天蠍、人馬（身體）；"
                  "（滑動＋拉遠，用 Z 驗證：畫面下緣到 −68.7°，走廊外 65°–69° 不混合＝與帶內同尺度；S 規則 ≤65° 太保守）"
                  "連線全關，只留銀河；不加地平線；端卡（EP39）＋追蹤 CTA"),
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
    for sh in shots:                                # 上下緣不出 D_r（本集自訂規則）
        for (cx, cy, fov, rot) in sh["frames"]:
            if abs(cy) + fov * 8 / 9 > m.Dr + 1e-6:
                print(f"  ✗ {sh['code']}：畫面上下緣出 D_r（會看到填滿圓的重複天區）")

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            ew = 360.0 / fov * 1080
            off = (round(-cx / fov * 1080), round(cy / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "大畫布圖層組", "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    # ── 天象與資料核對（與逐字稿比對） ──
    print("\n── 天象與資料核對 ──")
    for nm in ("火星", "木星"):
        v = PL[nm]
        print(f"  {nm}: RA {v['ra']/15:.4f}h ({int(v['ra']/15)}h{(v['ra']/15 % 1)*60:.1f}m) Dec {v['dec']:+.2f}° "
              f"高 {v['alt']}° 方位 {v['az']}° V {v['mag']} 在 {v['con']}")
    print(f"  火星—軒轅十四 {sep((PL['火星']['ra'], PL['火星']['dec']), S[REGULUS][:2]):.2f}°")
    print(f"  線段：Ruelle 全 {n_edges(SEG_RU)}、預設 {n_edges(SEG_WE)}、Rey {n_edges(SEG_RE)}；"
          f"獅子 {n_edges(SEG_WE_LEO)}／{n_edges(SEG_RE_LEO)}／{n_edges(SEG_RU_LEO)}；Ruelle 星座 {len(RU)}")
    print(f"  IAU 邊界 {len(EDGES)} 條；x：北蒼蠅 {x_of(S[MOUCHE[0]][0]):+.1f}、昴宿 {x_of(S[ALCYONE][0]):+.1f}、"
          f"軒轅十四 {x_of(S[REGULUS][0]):+.1f}、五帝座一 {x_of(S[DENEBOLA][0]):+.1f}、南十字 {x_of(S[ACRUX][0]):+.1f}、"
          f"心宿二 {x_of(S[ANTARES][0]):+.1f}、地獄犬 {x_of(radec_c(CERBERE, S)[0]):+.1f}；k {m.k:.4f}、R_fill {m.R_fill:.2f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if isinstance(hips, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                           顏色=col, 來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", "", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0, "bodies": PL},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        lg = LG_RU
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=lg,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_RU)
    from make_a21_v4 import sb_wall
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS[k]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
