# -*- coding: utf-8 -*-
"""A-28 印度：月亮的 27 位妻子｜大畫布 v4.6（長圖帶狀為主・沿黃道 S 捲動；不用南北盤鏡頭）

論點：印度把月亮的路寫成一門親事——27 宿＝月神 Soma 的 27 位妻子，一晚住一家；
偏心 Rohiṇī（畢宿五）→ 岳父詛咒 → 盈虧。天文上月亮真的一家家拜訪：全天一等星裡只有
畢宿五、軒轅十四、角宿一、心宿二會被月亮掩住，剛好是 Rohiṇī、Maghā、Citrā、Jyeṣṭhā。

來源：Stellarium indian（舊版 stellarium-skycultures-master；28 組連線＝27 宿＋Abhijit）。
  連線照原樣，唯一修正：Uttara Bhādrapadā 1067→667（8.32 等暗星）改 677（壁宿二），見逐字稿資料來源 ⑤④。
  片中 IAST 一律照逐字稿星名表（Stellarium 拼法錯的已改）。
逐字稿：04_腳本庫/A-28-印度月亮的27位妻子-逐字稿-v1.md。天象 PyEphem 4.2.1 自算。

自訂層（大畫布＋南北盤同步出；盤檔只是備用，本集沒有盤鏡頭）
  黃道（2027.3 當日黃道轉 J2000，淡藍灰虛線）、恆星黃道 27 格（Lahiri：角宿一＝180°；
  每格 13°20′ 邊界刻度，宿名＝標籤層「27宿門牌」）＝逐字稿 C-A28-01 的內容，做成星圖層才會跟著捲動、
  不會跟星點錯位（概念圖定格頁做不到 02 鏡的 S 捲動）；月亮軌道帶（黃緯 ±6.5° 淡帶，10 鏡）；
  四顆一等星琥珀圈（10 鏡）；畢宿五紅色光暈（03–05、11b、18 鏡）；斗柄弧線（01 鏡，X-04 接續；
  開陽—搖光—大角—角宿一，琥珀）；月亮 4/16 20:00＋明晚箭頭（13、17 鏡）；月亮 4/20 20:00（14 鏡）；
  火星、木星 4/16 20:00（17 鏡）；A-29 Su Pinnetu 預覽（18 鏡，琥珀虛線，Stellarium sardinian 001）。
  月亮與行星都用台北站心、J2000 astrometric（與星表同框）；月亮圖示放大約 2 倍（示意）。

參數（依本集逐字稿重新評估，不照抄範例）
  lst = 135 → 長圖切口 x＝±180 在 RA 315（摩羯—寶瓶之間）：本集要上長圖的天區從 雙魚 ζ（Revatī，RA 18）
             一路往東到人馬（Uttara Āṣāḍhā，RA 284），只有 RA 285–15 沒用到，切口放這裡，全片在一張連續長圖上。
             x：Revatī +117、Aśvinī +106、昴宿 +78、畢宿五 +66、軒轅十四 −17、角宿一 −66、大角 −79、
             心宿二 −112、Pūrva Āṣāḍhā −141、Uttara Āṣāḍhā −149。
  D_s = 62、D_r = 66 → 決定因素是 01 鏡接 X-04 的斗柄弧線：玉衡 +56.0、開陽 +54.9 要留在長圖帶內
             （D_s 40 時斗柄掉進縫合帶，弧線會折）。黃道 ±23.4°＋月亮軌道帶 ±6.5° 遠在帶內；
             S 鏡 fov 44 時 |cy| ≤ 22.9（02 鏡尾端人馬 cy −22 剛好）。
  D_fill = 20 → k＝2.3873、R_fill＝167.11（盤寬 ÷ 畫布寬＝0.9284，與 A-01、A-24 相同）；|x_t|+R_fill ≤ 180 ✓。
  x_tN = x_tS = 0。本集沒有 R 鏡頭；build_discs 照規定呼叫（盤組備用、亂數一致）。

鏡頭路線（全部大畫布）
  01 Z 斗柄弧線→大角、角宿一 → 02 S 沿黃道往東（月亮前進方向）捲 Citrā→Uttara Āṣāḍhā 約 80°，開 27 格門牌
  →【硬切】03 Z 畢宿五 fov 36→20 → 04 同框 → 05 拉遠 fov 40 → 06、07、08、09 定格疊概念圖
  → 10 S 畢宿五→軒轅十四→角宿一→心宿二（四個構圖，每段 ≤ 2.5 秒滑過，其餘時間停著）
  → 11 Z 心宿二 fov 24 →【硬切】11b 畢宿五 fov 24＋C-A28-06
  →【硬切】12 Z 獅子座 fov 40 → 13 Z 推近軒轅十四＋月亮 → 14 S 往東到角宿一（月亮 4/20）＋圖卡 C-A28-07
  → 15 S 往西 角宿一→昴宿→婁宿 ＋C-A28-08 →【硬切】16 Z 角宿一 fov 60＋C-A28-09
  →【硬切】17 Z 頭頂（月亮＋軒轅十四＋火星＋木星）＋圖卡 C-A28-10 →【硬切】18 Z 畢宿＋Su Pinnetu 預覽＋端卡。

  逐字稿 11 鏡要從心宿二跳到畢宿五（隔 178°），同一鏡裡滑過去會是 2.5 秒的甩鏡 → 拆 11／11b，旁白照原文在
  「；」切開，秒數 19＝7＋12（照字數分，每格 ≤ 4.5；總長 256 不變）。
  02 鏡方向：逐字稿畫面構想寫「沿黃道由西往東約 90°」——從 01 的角宿一往東（月亮前進方向）走到人馬約 80°
  就到切口前，03 再硬切回畢宿五（「故事是這樣的」換段）。

硬切（判斷後接受）：02→03（隔 210°）、11→11b、11b→12（83°，換段「月站在《梨俱吠陀》裡」）、
  15→16（隔 172°）、16→17（85°，從概念圖收回到今晚頭頂）、17→18（83°，圖卡後的下集預告）。
  其餘鏡頭之間照預設 Match & Move（10 鏡四段、14、15 鏡都是 ≤ 2.5 秒的滑動）。
check_shots：全部 Z／S，沒有 R，沒有 ⚠ 需要接受。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import great_circle, COLORS

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-28"
OUT = os.path.join(BASE, "05_素材/A-28_印度/_v4大畫布")
LST0 = 135.0
D_S, D_R, D_FILL = 62.0, 66.0, 20.0
TPE = (25.0330, 121.5654)
EPOCH = "2027/4/16"                          # 當日春分點（黃道、Lahiri 換算用）


# ══════════════════════════════════════════════════════════════════
# 〇、星曆（PyEphem 4.2.1；台北站心；J2000 astrometric）
# ══════════════════════════════════════════════════════════════════
def _obs(when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.temp, o.pressure = 20.0, 1010.0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def ecl_to_j2000(lon, lat=0.0, epoch=EPOCH):
    """當日黃道座標 → J2000 赤道（度）"""
    import ephem
    e = ephem.Ecliptic(math.radians(lon), math.radians(lat), epoch=epoch)
    q = ephem.Equatorial(e, epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


def ecl_of(ra, dec, epoch=EPOCH):
    """J2000 赤道 → 當日黃道（度）"""
    import ephem
    q = ephem.Equatorial(math.radians(ra), math.radians(dec), epoch=ephem.J2000)
    e = ephem.Ecliptic(ephem.Equatorial(q, epoch=epoch))
    return math.degrees(e.lon), math.degrees(e.lat)


def _topo_j2000(b, o):
    """站心視位置（當日春分點）→ J2000（月亮站心視差 ~0.5°，逐字稿 13、14 鏡要站心）"""
    import ephem
    q = ephem.Equatorial(ephem.Equatorial(b.ra, b.dec, epoch=o.date), epoch=ephem.J2000)
    return math.degrees(q.ra), math.degrees(q.dec)


def bodies():
    import ephem
    out = {}
    for key, when in (("月亮4/16", "2027/4/16 20:00"), ("月亮4/17", "2027/4/17 20:00"),
                      ("月亮4/20", "2027/4/20 20:00")):
        o = _obs(when); b = ephem.Moon(); b.compute(o)
        ra, dec = _topo_j2000(b, o)
        out[key] = dict(ra=ra, dec=dec,
                        alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                        phase=round(b.phase, 1))
    o = _obs("2027/4/16 20:00")
    for nm, b in (("火星", ephem.Mars()), ("木星", ephem.Jupiter())):
        b.compute(o)
        ra, dec = _topo_j2000(b, o)
        out[nm] = dict(ra=ra, dec=dec,
                       alt=round(math.degrees(b.alt), 1), az=round(math.degrees(b.az), 1),
                       mag=round(float(b.mag), 2))
    return out


PL = bodies()


def sep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
SC_OLD = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master")


def load_sc(cu):
    d = json.load(open(os.path.join(SC_OLD, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["id"]] = segs
    return out


IN = load_sc("indian")
NAK_IAST = ["Aśvinī", "Bharaṇī", "Kṛttikā", "Rohiṇī", "Mṛgaśiras", "Ārdrā", "Punarvasu", "Puṣya",
            "Āśleṣā", "Maghā", "Pūrva Phalgunī", "Uttara Phalgunī", "Hasta", "Citrā", "Svātī",
            "Viśākhā", "Anurādhā", "Jyeṣṭhā", "Mūla", "Pūrva Āṣāḍhā", "Uttara Āṣāḍhā", "Śravaṇa",
            "Dhaniṣṭhā", "Śatabhiṣaj", "Pūrva Bhādrapadā", "Uttara Bhādrapadā", "Revatī"]
NAK_SEGS = {}
for i in range(1, 29):
    segs = [list(s) for s in IN[f"CON indian N{i:02d}"]]
    if i == 26:                                   # 1067→667 是 8.32 等暗星，改 677（壁宿二）
        segs = [[677 if h == 667 else h for h in s] for s in segs]
    NAK_SEGS[i] = segs
hips_of = lambda segs: sorted({h for s in segs for h in s})
SEG_NAK = [s for i in range(1, 28) for s in NAK_SEGS[i] if len(set(s)) >= 2]
SEG_ABH = NAK_SEGS[28]

ROHINI, MAGHA, CITRA, SVATI, JYESTHA = 21421, 49669, 65474, 69673, 80763
ALIOTH, MIZAR, ALKAID = 62956, 65378, 67301
FOUR = [ROHINI, MAGHA, CITRA, JYESTHA]
KRTTIKA = hips_of(NAK_SEGS[3])
ASVINI = hips_of(NAK_SEGS[1])
REVATI = [5737]
PPHAL, UPHAL = hips_of(NAK_SEGS[11]), hips_of(NAK_SEGS[12])
SEG_ARC = [[MIZAR, ALKAID, SVATI, CITRA]]           # 斗柄弧線（X-04 接續）；玉衡—開陽是 X-04 的斗柄
SEG_ARC_H = [[ALIOTH, MIZAR]]
SARD = load_sc("sardinian")
SEG_PINNETU = SARD["CON sardinian 001"]              # Su Pinnetu 石頭小屋（A-29）
HYADES = hips_of(SEG_PINNETU)
MAINS = FOUR + [SVATI] + KRTTIKA[:4] + ASVINI + REVATI + PPHAL + UPHAL


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# 恆星黃道（Lahiri 近似：角宿一當日黃經 − 180°）
S0 = dict(G.load_stars(BASE))
AYAN = ecl_of(*S0[CITRA][:2])[0] - 180.0


def sid_to_j2000(lam_sid, beta=0.0):
    return ecl_to_j2000(lam_sid + AYAN, beta)


# ══════════════════════════════════════════════════════════════════
# 二、連線
# ══════════════════════════════════════════════════════════════════
LG_NAK = [(SEG_NAK, "blue", 0.8), (SEG_ABH, "blue", 0.5)]
LG_ARC = [(SEG_ARC_H, "amber", 0.7), (SEG_ARC, "amber", 1.0)]
LG_ALL = LG_NAK + LG_ARC
LINE_SETS = [(LG_ARC, "連線-斗柄弧線")]
LINES_KEY = {"L4": "星座連線", "弧": "連線-斗柄弧線", "黃": "黃道", "格": "恆星黃道27格",
             "帶": "月亮軌道帶", "圈": "四顆一等星琥珀圈", "紅": "畢宿五紅色光暈",
             "月16": "月亮4月16日", "月20": "月亮4月20日", "行": "火星與木星4月16日",
             "屋": "SuPinnetu預覽（A-29）"}
LINE_GROUPS = {"L4": LG_NAK, "弧": LG_ARC, "屋": [(SEG_PINNETU, "amber", 0.8)],
               "黃": [], "格": [], "帶": [], "圈": [], "紅": [], "月16": [], "月20": [], "行": []}


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
# 三、自訂圖層
# ══════════════════════════════════════════════════════════════════
ECL_PTS = [ecl_to_j2000(float(l)) for l in range(0, 361, 1)]


def custom_layers(m, S):
    RED, AMB, ECL = COLORS["red"], COLORS["amber"], "#A9B8D6"

    def ecliptic(s, pos, runs, disc):
        s.polylines(runs(ECL_PTS), stroke=ECL, w=m.lw * 0.55, opacity=0.55, dash="1.4 0.9")

    def ticks(s, pos, runs, disc):
        rr = []
        for n in range(27):
            lam = n * 40.0 / 3.0
            rr += runs([sid_to_j2000(lam, b) for b in (-3.0, -1.5, 0.0, 1.5, 3.0)])
        s.polylines(rr, stroke=ECL, w=m.lw * 0.7, opacity=0.75)
        rr = []                                   # 每格中點小刻度
        for n in range(27):
            lam = n * 40.0 / 3.0 + 20.0 / 3.0
            rr += runs([sid_to_j2000(lam, b) for b in (-0.8, 0.0, 0.8)])
        s.polylines(rr, stroke=ECL, w=m.lw * 0.45, opacity=0.45)

    def band(s, pos, runs, disc):
        if disc is not None:                      # 盤檔不收（|β|≤6.5 全在長圖帶內）
            return
        for l in range(0, 360, 2):
            q = [ecl_to_j2000(l, -6.5), ecl_to_j2000(l + 2, -6.5), ecl_to_j2000(l + 2, 6.5), ecl_to_j2000(l, 6.5)]
            pp = [m.p_band(m.xw(ra), dec) for ra, dec in q]
            if max(p[0] for p in pp) - min(p[0] for p in pp) > 20:   # 跨切口
                continue
            s.poly_fill([pp + [pp[0]]], fill="#A9B8D6", opacity=0.10)
        for b in (-6.5, 6.5):
            s.polylines(runs([ecl_to_j2000(float(l), b) for l in range(0, 361)]),
                        stroke="#A9B8D6", w=m.lw * 0.35, opacity=0.35, dash="0.8 0.8")

    def rings(s, pos, runs, disc):
        for h in FOUR:
            for p in pos(*S[h][:2]):
                s.circle(p[0], p[1], 1.9, stroke=AMB, w=0.16, opacity=0.95)

    def rohini_glow(s, pos, runs, disc):
        for p in pos(*S[ROHINI][:2]):
            s.circle(p[0], p[1], 1.6, fill=RED, opacity=0.14)
            s.circle(p[0], p[1], 0.8, fill=RED, opacity=0.30)

    def moon_at(key):
        def f(s, pos, runs, disc):
            for p in pos(PL[key]["ra"], PL[key]["dec"]):
                s.circle(p[0], p[1], 1.5, fill="#FFFFFF", opacity=0.12)
                s.circle(p[0], p[1], 0.55, fill="#F4F1E6", opacity=0.98)
        return f

    def moon16(s, pos, runs, disc):
        moon_at("月亮4/16")(s, pos, runs, disc)
        a, b = PL["月亮4/16"], PL["月亮4/17"]
        pts = [radec([vec(a["ra"], a["dec"])[i] * (1 - t) + vec(b["ra"], b["dec"])[i] * t for i in range(3)])
               for t in [k / 40 for k in range(4, 37)]]
        s.polylines(runs(pts), stroke="#F4F1E6", w=m.lw * 0.5, opacity=0.7, dash="0.9 0.7")
        # 箭頭（終點往回 1.2° 的兩翼）
        for p, q in zip(pos(*pts[-1]), pos(*pts[-5])):
            dx, dy = p[0] - q[0], p[1] - q[1]
            n = math.hypot(dx, dy) or 1.0
            ux, uy = dx / n, dy / n
            for sgn in (1, -1):
                wx, wy = -ux * 1.0 - sgn * uy * 0.6, -uy * 1.0 + sgn * ux * 0.6
                s.polylines([[(p[0], p[1]), (p[0] + wx, p[1] + wy)]], stroke="#F4F1E6", w=m.lw * 0.5, opacity=0.8)
        for p in pos(b["ra"], b["dec"]):
            s.circle(p[0], p[1], 0.55, stroke="#F4F1E6", w=0.08, opacity=0.6, dash="0.3 0.25")

    def planets(s, pos, runs, disc):
        for nm, col, r in (("木星", "#FFFFFF", 0.42), ("火星", RED, 0.32)):
            for p in pos(PL[nm]["ra"], PL[nm]["dec"]):
                s.circle(p[0], p[1], r * 2.8, fill=col, opacity=0.16)
                s.circle(p[0], p[1], r, fill=col, opacity=0.98)

    def pinnetu(s, pos, runs, disc):
        rr = []
        for seg in SEG_PINNETU:
            for a, b in zip(seg, seg[1:]):
                rr += runs(great_circle(*S[a][:2], *S[b][:2]))
        s.polylines(rr, stroke=AMB, w=m.lw * 0.8, opacity=0.92, dash="0.9 0.6")

    return [("黃道", ecliptic), ("恆星黃道27格", ticks), ("月亮軌道帶", band), ("四顆一等星琥珀圈", rings),
            ("畢宿五紅色光暈", rohini_glow), ("月亮4月16日", moon16), ("月亮4月20日", moon_at("月亮4/20")),
            ("火星與木星4月16日", planets), ("SuPinnetu預覽（A-29）", pinnetu)]


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
# 四、旁白字數（中文字＋外文音節；IAST 長母音、ṛ 都算母音，ai／au 連寫算一個）
# ══════════════════════════════════════════════════════════════════
VOW = "aeiouāīūṛṝḷēōáéíóú"


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
# 五、名詞總表（＝標籤對照表）
#   (錨點, 原文（片中寫法 IAST）, Stellarium 寫法, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
ST_OLD = {i: json.load(open(os.path.join(SC_OLD, "indian/index.json"), encoding="utf-8"))
          ["constellations"][i - 1]["common_name"] for i in range(1, 29)}
NAK_EN = ["belonging to the Aśvins", "Bearer", "Cutter (the Pleiades)", "Red one", "Deer's head", "Moist one",
          "Good again", "Nourisher", "Embrace", "Bountiful", "Former Phalgunī", "Latter Phalgunī", "Hand",
          "Bright, brilliant", "(etymology uncertain)", "Forked", "Following Rādhā", "Eldest", "Root",
          "Former Unconquered", "Latter Unconquered", "Hearing", "Wealthiest", "Having a hundred healers",
          "Former Auspicious Feet", "Latter Auspicious Feet", "Prosperous"]
NAK_ZH = ["雙馬童的", "承載者", "割者", "紅色的那位", "鹿頭", "潮濕的", "再度美好", "滋養者", "纏抱", "豐饒的",
          "前 Phalgunī", "後 Phalgunī", "手", "明亮的", "字源無定說", "分叉的", "跟隨 Rādhā 的", "最年長的", "根",
          "前「不可勝」", "後「不可勝」", "聽聞", "最富有的", "有百位醫者的", "前「吉祥之足」", "後「吉祥之足」", "富饒的"]
NAK_CN = ["婁", "胃", "昴", "畢", "觜", "參", "井", "鬼", "柳", "星", "張", "翼", "軫", "角", "亢", "氐", "房",
          "心", "尾", "箕", "斗", "女", "虛", "危", "室", "壁", "奎"]
TERMS = [(hips_of(NAK_SEGS[i + 1]), NAK_IAST[i], ST_OLD[i + 1].get("pronounce", ""), NAK_EN[i],
          f"{NAK_ZH[i]}（{NAK_CN[i]}宿）", "blue",
          f"第 {i + 1} 宿；恆星黃道 {i * 40 / 3:.2f}°–{(i + 1) * 40 / 3:.2f}°（Lahiri）")
         for i in range(27)]
TERMS += [
    ([SVATI], "Svātī·大角", "Svātī", "Arcturus", "大角", "amber", "01 鏡：上週 X-04 沿斗柄找到的"),
    ([CITRA], "Citrā·角宿一", "Chitrā", "Spica", "角宿一", "amber", "01 鏡"),
    ((PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"]), "月亮 4/16", "—", "Moon, 16 Apr 2027 20:00", "今晚的月亮",
     "white", f"台北站心 J2000；{PL['月亮4/16']['phase']}%；高 {PL['月亮4/16']['alt']}°"),
    ((PL["月亮4/17"]["ra"], PL["月亮4/17"]["dec"]), "明晚 4/17", "—", "Moon, 17 Apr", "明晚（Pūrva Phalgunī）",
     "white", "4/17 20:00 台北站心"),
    ((PL["月亮4/20"]["ra"], PL["月亮4/20"]["dec"]), "月亮 4/20", "—", "Moon, 20 Apr 2027 20:00", "下週二的月亮",
     "white", f"台北站心 J2000；{PL['月亮4/20']['phase']}%"),
    ((PL["火星"]["ra"], PL["火星"]["dec"]), "火星", "—", "Mars", "火星", "red",
     f"台北 4/16 20:00 高 {PL['火星']['alt']}°、{PL['火星']['mag']} 等"),
    ((PL["木星"]["ra"], PL["木星"]["dec"]), "木星", "—", "Jupiter", "木星", "white",
     f"台北 4/16 20:00 高 {PL['木星']['alt']}°"),
    (HYADES, "Su Pinnetu", "Su Pinnetu", "The Hut", "石頭小屋（A-29）", "amber", "Stellarium sardinian 001"),
]


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = S0
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
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
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                    dy=round(dy, 2), key=key)

    T = {t[1]: t for t in TERMS}

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
    # 長圖＝畫布方向、東在左（dx<0＝往東＝畫面左）
    F01 = 36.0
    LB_01 = (lab([SVATI], "Svātī", "大角", "amber", F01, dx=-1.0, dy=3.6)
             + lab([CITRA], "Citrā", "角宿一", "amber", F01, dx=0.0, dy=-3.6))
    # 27 宿門牌：格子中點、黃緯 −6.2°（黃道南側；主星不一定在門牌正上方，見逐字稿表下註）
    F02 = 44.0
    LB_DOOR = []
    for i in range(27):
        ra, dec = sid_to_j2000(i * 40.0 / 3.0 + 20.0 / 3.0, -6.2)
        LB_DOOR += one((ra, dec), f"{i + 1} {NAK_IAST[i]}", "blue", F02, key=f"門{i + 1}", k=0.024)
    F03 = 20.0
    LB_ROH_N = lab([ROHINI], "Rohiṇī", "紅色的那位", "red", F03, dx=0.0, dy=-2.0, zh_col="white")
    F05 = 40.0
    LB_ROH = lab([ROHINI], "Rohiṇī", "畢宿五", "red", F05, dx=0.0, dy=-3.8)
    F10 = 40.0
    LB_FOUR = (lab([ROHINI], "Rohiṇī", "畢宿五", "amber", F10, dy=-3.8)
               + lab([MAGHA], "Maghā", "軒轅十四", "amber", F10, dy=-3.8)
               + lab([CITRA], "Citrā", "角宿一", "amber", F10, dy=-3.8)
               + lab([JYESTHA], "Jyeṣṭhā", "心宿二", "amber", F10, dy=-3.8))
    F11 = 24.0
    LB_JYE = lab([JYESTHA], "Jyeṣṭhā", "最年長的", "amber", F11, dy=-2.4)
    LB_ROH11 = lab([ROHINI], "Rohiṇī", "最受寵的", "red", F11, dy=-2.4)
    F12 = 40.0
    LB_WED = (lab([MAGHA], "Maghā", "婚禮詩作 Aghā", "blue", F12, dy=-3.8)
              + lab(PPHAL, "Pūrva Phalgunī", "西上相・西次相", "blue", F12, dx=0.0, dy=5.2)
              + lab(UPHAL, "Uttara Phalgunī", "五帝座一", "blue", F12, dx=4.0, dy=-3.8)
              + one((168.0, 4.0), "兩個 Arjunī＝兩個 Phalgunī", "white", F12, key="Arjunī", k=0.022))
    F13 = 18.0
    LB_TON = (lab([MAGHA], "Maghā", "軒轅十四", "blue", F13, dx=0.0, dy=1.7, k1=0.032, k2=0.026)
              + one((PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"]), "今晚的月亮", "white", F13,
                    dx=1.5, dy=-1.5, key="月16", k=0.030)
              + one((PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"]), "← 明晚搬進 Phalgunī", "white", F13,
                    dx=-4.6, dy=-3.3, key="月17", k=0.024))
    F14 = 40.0
    LB_FULL = (lab([CITRA], "Citrā", "角宿一", "amber", F14, dy=3.8)
               + one((PL["月亮4/20"]["ra"], PL["月亮4/20"]["dec"]), "下週二 4/20 的月亮", "white", F14,
                     dy=-2.6, key="月20", k=0.024))
    F15 = 40.0
    LB_START = (lab(KRTTIKA, "Kṛttikā", "昴宿・最早的第一位", "blue", F15, dy=3.6)
                + lab(ASVINI, "Aśvinī", "婁宿・後來的第一位", "blue", F15, dy=3.6)
                + lab(REVATI, "Revatī", "奎宿・最後一位", "blue", F15, dy=-3.6))
    F16 = 60.0
    LB_C180 = lab([CITRA], "Citrā", "恆星黃道 180°", "amber", F16, dy=-4.4, k1=0.026, k2=0.021)
    F17 = 50.0
    LB_HEAD = (one((PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"]), "月亮", "white", F17, dy=-2.4, key="月")
               + one([MAGHA], "軒轅十四", "blue", F17, dy=2.4, key="Maghā")
               + one((PL["火星"]["ra"], PL["火星"]["dec"]), "火星", "red", F17, dy=-2.4, key="火星")
               + one((PL["木星"]["ra"], PL["木星"]["dec"]), "木星", "white", F17, dy=-2.6, key="木星"))
    F18 = 30.0
    LB_NEXT = (lab(HYADES, "Su Pinnetu", "石頭小屋（下集）", "amber", F18, dx=0.0, dy=6.0)
               + lab([ROHINI], "Rohiṇī", "畢宿五", "red", F18, dx=1.0, dy=-2.6))

    label_sets = [(LB_01, "Svātī與Citrā"), (LB_DOOR, "27宿門牌"), (LB_ROH_N, "Rohiṇī-近"), (LB_ROH, "Rohiṇī"),
                  (LB_FOUR, "四位妻子"), (LB_JYE, "Jyeṣṭhā-近"), (LB_ROH11, "Rohiṇī-最受寵"),
                  (LB_WED, "婚禮詩"), (LB_TON, "今晚Maghā"), (LB_FULL, "滿月Citrā"), (LB_START, "第一位"),
                  (LB_C180, "Citrā180°"), (LB_HEAD, "今晚頭頂"), (LB_NEXT, "下集")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    # ════════════════════ 構圖 ════════════════════
    def P(h):
        ra, dec = (S[h][:2] if isinstance(h, int) else h)
        return (x_of(ra), dec)

    def sfit(pts, pad=0.14, minfov=30.0, dx=0.0, dy=0.0, clamp=True, fov=None):
        pts = [P(h) for h in pts]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        f = fov or max(minfov, w * (1 + 2 * pad), h * (1 + 2 * pad) * 9 / 16)
        cx, cy = (max(xs) + min(xs)) / 2 + dx, (max(ys) + min(ys)) / 2 + dy
        if clamp:
            lim = m.Ds - f * 8 / 9 - 0.5                 # S：|cy|+fov·8/9 ≤ D_s
            cy = max(-lim, min(lim, cy))
        return (round(cx, 2), round(cy, 2), round(f, 1), 0.0)

    E = lambda lam, b=0.0: sid_to_j2000(lam, b)          # 恆星黃經 → J2000（tuple 錨點）
    F01a = sfit([MIZAR, ALKAID, SVATI, CITRA], fov=50.0, clamp=False, dy=-1.0)
    F01b = sfit([SVATI, CITRA], fov=F01, dy=-1.5)
    F02a = sfit([E(183.0), E(200.0)], fov=F02, dy=0.0)
    F02b = sfit([E(258.0), E(270.0)], fov=F02, dy=0.0)
    F03a = sfit([ROHINI], fov=36.0)
    F03b = sfit([ROHINI], fov=F03, dy=-0.8)
    FR05 = sfit([ROHINI], fov=F05, dx=-2.0)
    FR10 = [sfit([ROHINI], fov=F10), sfit([MAGHA], fov=F10), sfit([CITRA], fov=F10, dy=2.0),
           sfit([JYESTHA], fov=F10, dy=2.0)]
    FR11 = sfit([JYESTHA], fov=F11, dy=-0.5)
    FR11b = sfit([ROHINI], fov=F11, dy=-0.5)
    FR12 = sfit([MAGHA] + PPHAL + UPHAL, fov=F12, dx=-2.0, dy=-1.0)
    F13a = sfit([MAGHA, (PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"])], fov=40.0, dx=-4.0)
    F13b = sfit([MAGHA, (PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"])], fov=F13, dx=-1.5)
    F14a = sfit([MAGHA], fov=F14, dx=-6.0)
    F14b = sfit([CITRA, (PL["月亮4/20"]["ra"], PL["月亮4/20"]["dec"])], fov=F14)
    F15a = F14b
    F15b = sfit(KRTTIKA + [ROHINI], fov=F15)
    F15c = sfit(ASVINI + REVATI, fov=F15, dx=-2.0)
    FR16 = sfit([CITRA], fov=F16, dy=4.0)
    FR17 = sfit([MAGHA, (PL["火星"]["ra"], PL["火星"]["dec"]), (PL["木星"]["ra"], PL["木星"]["dec"]),
                (PL["月亮4/16"]["ra"], PL["月亮4/16"]["dec"])], fov=F17)
    F18a = sfit(HYADES, fov=36.0)
    F18b = sfit(HYADES, fov=F18)
    print("\n── 構圖 ──")
    for k, v in dict(F01a=F01a, F01b=F01b, F02a=F02a, F02b=F02b, F03a=F03a, F03b=F03b, F05=FR05, F10=FR10,
                     F11=FR11, F11b=FR11b, F12=FR12, F13a=F13a, F13b=F13b, F14a=F14a, F14b=F14b, F15b=F15b,
                     F15c=F15c, F16=FR16, F17=FR17, F18a=F18a, F18b=F18b).items():
        print(f"  {k} {v}")

    custom = custom_layers(m, S)
    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_NAK)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    write_custom(m, custom)
    MARKS = [(MAINS, "主角星白點", "dot")]
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_NAK, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)
    print("\n── 盤：自訂圖層 ──")
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭（vo＝逐字稿 v1 原文） ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="Z", sec=14, north=True, frames=[F01a, F01b], layers=["弧", "黃"],
             labels=ls("Svātī與Citrā"),
             vo="上週沿著斗柄找到的大角和角宿一，在印度叫 Svātī 和 Citrā，是同一位丈夫的兩位妻子。同一片星空，印度人看見——月亮的二十七位妻子。",
             card="月亮的二十七位妻子",
             note="大畫布 fov 50→36（Z）：接 X-04 的斗柄弧線（琥珀：開陽—搖光—大角—角宿一）；"
                  "Svātī、Citrā 標籤（IAST）；黃道（淡藍灰虛線）淡入；開場字卡"),
        dict(code="02", kind="S", sec=12, north=True, frames=[F02a, F02b], layers=["L4", "黃", "格"],
             labels=ls("27宿門牌"), labels_start=ls("27宿門牌"),
             vo="月亮繞天一圈要二十七天多，印度把它走的路切成二十七段月站，叫 Nakṣatra。每一段住著一位妻子，月亮每晚換一家住。",
             card="一晚，住一家",
             note="長圖 S：沿黃道往東（畫面往左＝月亮前進方向）從 Citrā 捲到 Uttara Āṣāḍhā 約 80°；"
                  "27 宿連線（藍）＋恆星黃道 27 格刻度＋門牌（＝逐字稿的 C-A28-01，做成星圖層跟著捲動）。"
                  "門牌是黃道分段，主星不一定在格子正上下方（大角在 Citrā 格北方 30°）"),
        dict(code="03", kind="Z", sec=14, north=True, frames=[F03a, F03b], layers=["紅"],
             labels=ls("Rohiṇī-近"),
             overlay="C-A28-02_二十七位妻子", overlay_layers=["妻子層"],
             vo="故事是這樣的：始祖神 Dakṣa 有一群女兒，其中二十七個，全嫁給月神 Soma。可是 Soma 只愛一個——Rohiṇī，「紅色的那位」，就是金牛座的畢宿五。",
             card="Rohiṇī＝紅色的那位",
             note="【硬切】回到畢宿五（隔 210°）fov 36→20；紅色光暈；Rohiṇī 標籤；迄格疊 C-A28-02「妻子」層"),
        dict(code="04", kind="Z", sec=14, north=True, frames=[F03b], layers=["紅"], labels=ls("Rohiṇī-近"),
             overlay="C-A28-02_二十七位妻子", overlay_layers=["回娘家層"],
             vo="他天天住在 Rohiṇī 家，其他二十六位獨守空閨，回娘家告狀。Dakṣa 要女婿一視同仁，Soma 嘴上答應，照樣偏心——岳父一怒，詛咒他染上消瘦病。",
             card="偏心的丈夫",
             note="畫面不動（畢宿五 fov 20）；疊 C-A28-02「回娘家」層（獨立一張：26 顆轉灰、往外移開；不跟「妻子」層疊）"),
        dict(code="05", kind="Z", sec=13, north=True, frames=[F03b, FR05], layers=["紅"],
             labels=ls("Rohiṇī-近"), labels_end=ls("Rohiṇī"),
             overlay="C-A28-03_盈虧", overlay_layers=["消瘦層"],
             vo="月亮一天比一天瘦，地上的草藥也跟著枯萎。眾神出面求情，Dakṣa 才鬆口：要他平等對待每一位妻子，再去海邊的聖地 Prabhāsa 沐浴。",
             card="求情：去 Prabhāsa 沐浴",
             note="畫面拉遠 fov 20→40；迄格疊 C-A28-03「消瘦」層（滿月逐格變細 6 格＋Prabhāsa）"),
        dict(code="06", kind="Z", sec=12, north=True, frames=[FR05], layers=["紅"], labels=ls("Rohiṇī"),
             overlay="C-A28-03_盈虧", overlay_layers=["消瘦層", "盈虧層"],
             vo="命是保住了，但詛咒收不回：從此月亮半個月消瘦、半個月復原——這就是月亮的盈虧。後來的《濕婆往世書》改說，是濕婆救了他。",
             card="半月消瘦，半月復原",
             note="畫面不動；C-A28-03 兩層：消瘦→盈虧（朔望月一圈＋末句小字《濕婆往世書》）"),
        dict(code="07", kind="Z", sec=8, north=True, frames=[FR05], layers=["紅"], labels=ls("Rohiṇī"),
             overlay="C-A28-04_Somnāth在哪", overlay_layers=["印度層", "古吉拉特層"],
             vo="那片海邊，今天還有一座濕婆神廟，叫 Somnāth——「月神之主」，就在印度西岸的古吉拉特。",
             card="Somnāth 月神之主",
             note="畫面不動；疊 C-A28-04（Natural Earth 海岸線，只畫陸地不畫國界）印度→古吉拉特海岸紅點；"
                  "有授權的 Somnath 神廟照片（Prabhas Patan）時美宣改放照片"),
        dict(code="08", kind="Z", sec=20, north=True, frames=[FR05], layers=["紅"], labels=ls("Rohiṇī"),
             overlay="C-A28-05_33到27", overlay_layers=["三十三層"],
             vo="這個故事最早的版本，寫在吠陀祭祀經《泰帝利耶本集》裡：嫁女兒的是生主 Prajāpati，女兒不是二十七個，是三十三個。Soma 在這裡是一位王，他違背誓言，病就找上門，所以叫 rājayakṣma，「國王的消瘦病」。",
             card="最早的版本：33 個女兒",
             note="畫面不動；疊 C-A28-05「三十三」層（33 個小圓；《泰帝利耶本集》2.3.5；Prajāpati；月亮戴小王冠；rājayakṣma）"),
        dict(code="09", kind="Z", sec=8, north=True, frames=[FR05], layers=["紅"], labels=ls("Rohiṇī"),
             overlay="C-A28-05_33到27", overlay_layers=["二十七層"],
             vo="到了後來的史詩，才變成 Dakṣa 的二十七個女兒，剛好跟天上的月站一樣多。",
             card="33 → 27",
             note="畫面不動；疊 C-A28-05「二十七」層（獨立一張：27 個排上黃道環；Dakṣa；《摩訶婆羅多》）"),
        dict(code="10", kind="S", sec=17, north=True, frames=FR10, layers=["L4", "黃", "帶", "圈"],
             labels=ls("四位妻子"), labels_start=ls("四位妻子"),
             vo="天文上，月亮真的一家一家拜訪。全天的一等星裡，只有畢宿五、軒轅十四、角宿一、心宿二貼著月亮的路，會被月亮整個擋住，剛好是 Rohiṇī、Maghā、Citrā、Jyeṣṭhā 四位妻子的主星。",
             card="月亮擋得住的四顆一等星",
             note="長圖 S fov 40：畢宿五→軒轅十四→角宿一→心宿二（往東 178°，四個構圖、每段 ≤ 2.5 秒滑過）；"
                  "四星琥珀圈＋IAST 標籤；月亮軌道帶（黃緯 ±6.5° 淡帶）淡入"),
        dict(code="11", kind="Z", sec=7, north=True, frames=[FR11], layers=["L4", "黃", "帶", "圈"],
             labels=ls("Jyeṣṭhā-近"),
             vo="這幾年，反而是名字叫「最年長的」那位 Jyeṣṭhā，每個月都被月亮擋住；",
             card="Jyeṣṭhā：每個月被擋住",
             note="心宿二 fov 40→24（接 10 鏡迄格推近）；Jyeṣṭhā「最年長的」"),
        dict(code="11b", kind="Z", sec=12, north=True, frames=[FR11b], layers=["黃", "帶", "紅"],
             labels=ls("Rohiṇī-最受寵"),
             overlay="C-A28-06_月亮與Rohiṇī的距離",
             vo="最受寵的 Rohiṇī，月亮經過都隔著將近十度。月亮的路十八年多擺一輪：上次擋住她是二〇一八年，下次要等到二〇三三年。",
             card="掩 Rohiṇī：2018→2033",
             note="【硬切】跳回畢宿五 fov 24（隔 178°；逐字稿 11 鏡拆成 11／11b）；月亮軌道帶看得出畢宿五在帶的南緣；"
                  "迄格疊 C-A28-06（2014–2035 每年最近距離折線，2018／2033 標點）"),
        dict(code="12", kind="Z", sec=15, north=True, frames=[FR12], layers=["L4", "黃"], labels=ls("婚禮詩"),
             vo="月站在《梨俱吠陀》裡就出現了，而且是在一首婚禮詩裡：在 Aghā，也就是 Maghā，牛被趕上路，也有人譯作宰殺；在兩個 Arjunī，也就是 Phalgunī，新娘被迎進門。",
             card="婚禮詩裡的月站",
             note="【硬切】長圖 fov 40：獅子座；Maghā（軒轅十四）、Pūrva Phalgunī（西上相＋西次相）、"
                  "Uttara Phalgunī（五帝座一）；小字「兩個 Arjunī＝兩個 Phalgunī」"),
        dict(code="13", kind="Z", sec=10, north=True, frames=[F13a, F13b], layers=["L4", "黃", "月16"],
             labels=ls("今晚Maghā"), labels_start=[],
             vo="說到 Maghā：今晚月亮正好住在她家，就在獅子座軒轅十四旁邊，不到兩度。明天晚上，就搬進 Phalgunī。",
             card="今晚：月亮在 Maghā",
             note=f"推近軒轅十四 fov 40→{F13:g}；月亮圖示＝4/16 20:00 台北站心 J2000（RA {PL['月亮4/16']['ra']/15:.3f}h、"
                  f"Dec {PL['月亮4/16']['dec']:+.2f}°；放大約 2 倍示意）；虛線箭頭＝明晚 4/17 20:00 位置（畫面左外）"),
        dict(code="14", kind="S", sec=13, north=True, frames=[F14a, F14b], layers=["L4", "黃", "月20"],
             labels=ls("滿月Citrā"),
             overlay="C-A28-07_十二個月名",
             vo="印度曆的月份，也用妻子命名：滿月住哪一家，就用她的名字當月名。下週二晚上的滿月在 Citrā 旁邊，所以現在這個月叫 Caitra。",
             card="滿月定月名：Caitra",
             note=f"長圖 S 往東到角宿一；月亮圖示＝4/20 20:00 台北站心 J2000（離角宿一 "
                  f"{sep((PL['月亮4/20']['ra'], PL['月亮4/20']['dec']), S[CITRA][:2]):.1f}°）；"
                  "迄格後疊 9:16 圖卡 C-A28-07「十二個月名＝十二位妻子」（可存圖；圖卡定格不捲動）"),
        dict(code="15", kind="S", sec=17, north=True, frames=[F15a, F15b, F15c], layers=["L4", "黃", "格"],
             labels=ls("第一位"),
             overlay="C-A28-08_起點搬家", overlay_layers=["春分點層", "起點層"],
             vo="名單的第一位也換過人：最早從昴宿星團 Kṛttikā 排起，後來改從白羊座的 Aśvinī 開始。有一種說法是：起點跟著春分點走，而春分點在星空裡慢慢往西挪，這就是歲差。",
             card="第一位妻子換人了",
             note="長圖 S 往西（畫面往右）：角宿一→昴宿→婁宿（144°＋29°，兩段各 ≤ 2.5 秒）；"
                  "迄格疊 C-A28-08 兩層：春分點三個年代 → 宿表起點（箭頭向西）"),
        dict(code="16", kind="Z", sec=24, north=True, frames=[FR16], layers=["L4", "黃", "格"],
             labels=ls("Citrā180°"),
             overlay="C-A28-09_兩條黃道", overlay_layers=["兩尺層", "十二宮層"],
             vo="今天印度的占星和宗教曆，還把黃道固定在星星上。一九五〇年代，天體物理學家 Meghnad Saha 主持改曆，替宗教曆統一了起點：讓 Citrā 落在一百八十度。所以印度的星座，常比西洋退後一格；差的二十四度，就是歲差。兩套都是約定，不是誰算錯。",
             card="差 24°＝歲差",
             note="【硬切】長圖 fov 60 停在角宿一（Citrā 恆星黃道 180°）；疊 C-A28-09 兩層："
                  "兩尺（回歸／恆星黃道錯開 24.2°）→「所以印度的星座」起加十二宮＋同一天的太陽"),
        dict(code="17", kind="Z", sec=17, north=True, frames=[FR17], layers=["L4", "黃", "月16", "行"],
             labels=ls("今晚頭頂"),
             overlay="C-A28-10_今晚抬頭看",
             vo="今晚八點在台灣：月亮高掛頭頂，軒轅十四就在旁邊，附近最亮的是木星，偏紅的是火星；西邊低空，紅色的 Rohiṇī 畢宿五，要趁八點半前看；東邊，大角和角宿一正往上爬。",
             card="今晚八點抬頭看",
             note="【硬切】長圖 fov 50：頭頂一帶（月亮＋軒轅十四＋火星＋木星）；"
                  "「西邊低空」起疊 9:16 圖卡 C-A28-10「今晚抬頭看」（台北 4/16 20:00 全天圖，含東西地平線；可存圖）"),
        dict(code="18", kind="Z", sec=9, north=True, frames=[F18a, F18b], layers=["L4", "屋", "紅"],
             labels=ls("下集"),
             vo="下週五，我們往西到地中海的薩丁尼亞：連著 Rohiṇī 這顆紅星，牧人看見了一間石頭小屋。",
             card="下集見｜薩丁尼亞：地中海島嶼的農牧星空",
             note="【硬切】推近畢宿 fov 36→30；A-29 Su Pinnetu 連線預覽（琥珀虛線，連到畢宿五）；端卡（EP37）＋追蹤 CTA"),
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
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    # ── 天象核對（與逐字稿「星空對時」比對） ──
    print(f"\n── 天象核對 ──\n  Lahiri（角宿一當日黃經−180）＝{AYAN:.3f}°")
    for k in ("月亮4/16", "月亮4/17", "月亮4/20"):
        v = PL[k]
        lam = ecl_of(v["ra"], v["dec"])[0] - AYAN
        print(f"  {k}: RA {v['ra']/15:.4f}h ({int(v['ra']/15)}h{(v['ra']/15 % 1)*60:.1f}m) Dec {v['dec']:+.3f}° "
              f"高 {v['alt']}° 方位 {v['az']}° {v['phase']}%  恆星黃經 {lam % 360:.1f}°＝{NAK_IAST[int((lam % 360) // (40/3))]}")
    print(f"  4/16 月亮—軒轅十四 {sep((PL['月亮4/16']['ra'], PL['月亮4/16']['dec']), S[MAGHA][:2]):.2f}°；"
          f"4/20 月亮—角宿一 {sep((PL['月亮4/20']['ra'], PL['月亮4/20']['dec']), S[CITRA][:2]):.2f}°；"
          f"火星—軒轅十四 {sep((PL['火星']['ra'], PL['火星']['dec']), S[MAGHA][:2]):.1f}°")
    for nm in ("火星", "木星"):
        print(f"  {nm}: 高 {PL[nm]['alt']}° 方位 {PL[nm]['az']}° V {PL[nm]['mag']}")
    print(f"  x：Revatī {x_of(S[5737][0]):+.1f}、Aśvinī {x_of(S[8903][0]):+.1f}、昴宿 {x_of(S[17702][0]):+.1f}、"
          f"畢宿五 {x_of(S[ROHINI][0]):+.1f}、軒轅十四 {x_of(S[MAGHA][0]):+.1f}、角宿一 {x_of(S[CITRA][0]):+.1f}、"
          f"大角 {x_of(S[SVATI][0]):+.1f}、心宿二 {x_of(S[JYESTHA][0]):+.1f}；k {m.k:.4f}、R_fill {m.R_fill:.2f}")

    terms = {}
    for hips, orig, sc, en, zh, col, note in TERMS:
        terms[orig] = dict(hips=hips if isinstance(hips, list) else [], 原文=orig, 拼音="",
                           英文翻譯=en, 中文=zh, 顏色=col,
                           來源備註=(f"Stellarium 寫法 {sc}；" if sc not in ("—", "", orig) else "") + note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "lst0": LST0, "ayanamsa": AYAN, "bodies": PL},
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
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
            title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
