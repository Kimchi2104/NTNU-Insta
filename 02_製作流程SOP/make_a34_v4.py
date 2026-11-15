# -*- coding: utf-8 -*-
"""A-34 蘇菲之書：一千多年前的星圖手稿｜大畫布 v4.6（整集在北盤圖層組上）

論點：蘇菲（al-Ṣūfī，約 964 年）的《恆星圖像之書》一次收進兩層天空——托勒密的 48 個希臘星座，
加上古代阿拉伯人的老星名（一顆顆對到希臘星上）；有些阿拉伯星座（仙女座身上的大魚）也一起畫進圖，
魚嘴邊的「一小抹像雲的光斑」就是仙女座大星系。兩層星名後來都流進歐洲：Algol、Vega、Altair。

來源：Stellarium arabic_al-sufi（stellarium-master 桌面版；Khalid al-Ajaji）：
  constellations Boo、Vir、And、Per、Lyr、Aql（蘇菲書的托勒密星座連線）、SFA 大魚；
  asterisms NasW（俯衝的老鷹＝織女）、NasT（飛翔的老鷹＝牛郎）；common_names 的 Boo_a_01（大角＝
  「兩腿之間的星，稱為拿矛的高舉者」）、Vir_14（角宿一＝沒拿武器的高舉者）、Per_12（戈爾貢頭中的亮星）。
  天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，UTC+8；1010 hPa、20°C）。
逐字稿：04_腳本庫/A-34-蘇菲之書一千多年前的星圖手稿-逐字稿-v1.md。

參數（依本集逐字稿重新評估，不照抄範例）
  整集都在北盤圖層組上（逐字稿 07、10、15 原寫長圖＋換組；改的理由寫在回報）：
    要上畫面的星跨了半個天空——大角、角宿一（RA 201–214）在今晚八點的南方，仙女座、大魚、M31、英仙座
    （RA 2–62）在對面、八點還在北方地平線下。長圖帶只能讓其中一邊靠近走廊，另一邊會落在走廊外的下緣洞，
    兩次換組（長圖⇄北盤）還要每次多 3–4 頁「歸位／換組／下移」；北盤是完整圓，兩邊都在盤上，
    鏡頭之間直接 Match & Move 滑過去（穿過北極），一頁換組頁都不用。
  lst = 14.27 → 台北 2027/6/4 20:00 的 LST 194.27＋180：北盤「面向北方」在 20:00 剛好是 0°
             （rot＝−((LST＋180−lst) mod 360)），22:00 為 −30.1°（13 鏡）；而 RA 14 也正好是仙女座＋大魚
             （RA 2–25）的中間，長圖走廊 x=0 落在大魚上（長圖本集不上畫面，留給 A-35 或日後重用）。
  D_s = 42、D_r = 46 → k = 1.3022。決定因素是角宿一（dec −11.2，離天北極 101.2°）：盤上 r＝131.8，
             06／12 鏡要把它和大角（r 92.2）放進同一格、畫面角落還得留在填滿圓裡；D_r 49（k 1.40）時
             角宿一 r 141.4，01 鏡 fov 140 的總覽就放不下。D_r 再降，北極附近（英仙、仙女）的星太擠。
  D_fill = −45 → R_fill = 175.79（盤寬 ÷ 畫布寬＝0.976 ⚠ 只差 2.4%，Canva 別設成同寬；本集不換組，
             只在盤圖層組上用）；|x_t|＋R_fill ≤ 180 ✓。01 鏡 fov 140：角落 ≤ 175.3 要求畫面中心離盤心 ≤ 36。
  x_tN = x_tS = 0
  北盤旋轉：01–12 全在 20:00（0°）；13 鏡 0°→−30.1°（20:00→22:00，逆時針＝時間前進）；
           14、15 停在 −30.1°。每段 M&M 旋轉 ≤ 30.1° < 170° ✓。

鏡頭路線（逐字稿 15 鏡，秒數照逐字稿，總長 223 秒）
  01 北盤 fov 140 總覽（台北 20:00 面北，山＝北方地平線）→ 推近南方天空 → 02–05 概念圖定格（01 迄格）
  → 06 推到牧夫＋室女（蘇菲的連線＋高舉者）→ 07 滑過北極到仙女座＋大魚 → 推近魚嘴 M31（fov 10）
  → 08 拉回仙女座＋C-A34-04 → 09 定格（手稿書影，美宣）→ 10 滑到英仙座＋大陵五 → 11 定格（杜勒星圖，美宣）
  → 12 滑回大角＋角宿一（標天頂）→ 13 面北東方：織女、牛郎升起（0°→−30.1°）→ 14 圖卡 C-A34-05 → 15 拉遠＋端卡

check_shots 的 ⚠（判斷後接受）：全部鏡頭都是 R（北盤圖層組），不與長圖互切；「切點」⚠ 不適用
  （gen_canva_pages：第一頁就在北盤上，整集沒有長圖頁，不插換組頁）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
from gen_projection import horizon_points

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "A-34"
OUT = os.path.join(BASE, "05_素材/A-34_蘇菲之書/_v4大畫布")
LST0 = 14.27
D_S, D_R, D_FILL = 42.0, 46.0, -45.0
TPE = (25.0330, 121.5654)
PHI = 25.033

WARN_OK = """
  全部 R：整集在北盤圖層組上，不換組 → 「切點」⚠ 不適用（沒有一格要與大畫布互切）。
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


def rot_n(lst_obs):
    """北盤轉到「該恆星時、面向北方」：逆時針＝時間前進（Canva 只收 ±180）"""
    r = -((lst_obs + 180.0 - LST0) % 360.0)
    r = r + 360.0 if r <= -180.0 else r
    return round(0.0 if abs(r) < 0.005 else r, 2)


T_TPE = {"2000": "2027/6/4 20:00", "2200": "2027/6/4 22:00"}
LST_AT = {k: lst_at(v) for k, v in T_TPE.items()}
ROT = {k: rot_n(v) for k, v in LST_AT.items()}
R20, R22 = ROT["2000"], ROT["2200"]


def altaz(ra, dec, when):
    import ephem
    o = _obs(when)
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


# ══════════════════════════════════════════════════════════════════
# 一、星與連線
# ══════════════════════════════════════════════════════════════════
ARC, SPI, VEGA, ALT = 69673, 65474, 91262, 97649
ALGOL, MIRFAK, NU_AND, POLARIS = 14576, 15863, 3881, 11767
M31, ZEN = 9300001, 9300002               # 假星（V=99，不進星點層）：仙女座大星系、20:00 天頂
M31_RADEC = (10.6846, 41.2692)            # 00h42m44.3s +41°16′09″（逐字稿星空對時表）
MARK_V = {M31: 3.4, ZEN: 2.0}

SC = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def sc_lines(cu, cid):
    d = json.load(open(os.path.join(SC, cu, "index.json"), encoding="utf-8"))
    for c in d.get("constellations", []) + d.get("asterisms", []):
        if c["id"].split()[-1] == cid:
            return [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
    raise KeyError(cu + " " + cid)


SUFI = "arabic_al-sufi"
SEG = {k: sc_lines(SUFI, k) for k in ("Boo", "Vir", "And", "SFA", "Per", "Lyr", "Aql", "NasW", "NasT")}
assert not any(ARC in l for l in SEG["Boo"]), "大角不在蘇菲牧夫座的連線上（index.json Boo）"
FISH = sorted({h for l in SEG["SFA"] for h in l})
assert len(FISH) == 11 and NU_AND in FISH
flat = lambda segs: sorted({h for l in segs for h in l})

LG = {
    "牧室": [(SEG["Boo"], "amber", 1.0), (SEG["Vir"], "amber", 1.0)],
    "仙女": [(SEG["And"], "amber", 1.0)],
    "大魚": [(SEG["SFA"], "green", 1.25)],
    "英仙": [(SEG["Per"], "amber", 1.0)],
    "琴鷹": [(SEG["Lyr"], "amber", 0.9), (SEG["Aql"], "amber", 0.9)],
    "老鷹": [(SEG["NasW"] + SEG["NasT"], "green", 1.3)],
}
LNAME = {"牧室": "連線-牧夫座＋室女座（蘇菲）", "仙女": "連線-仙女座（蘇菲）", "大魚": "連線-大魚（阿拉伯）",
         "英仙": "連線-英仙座（蘇菲）", "琴鷹": "連線-天琴座＋天鷹座（蘇菲）", "老鷹": "連線-兩隻老鷹（阿拉伯）"}


# ══════════════════════════════════════════════════════════════════
# 二、旁白字數（中文字＋外文音節；與 make_a19_v4.py 同一套算法）
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
# 三、名詞總表（＝標籤對照表）
#   key: (錨點, 原文（轉寫，片中寫法）, 英文, 中文, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "大角": ([ARC], "大角", "Arcturus (α Boo)", "大角", "amber", "chinese；中文名有「角」"),
    "角宿一": ([SPI], "角宿一", "Spica (α Vir)", "角宿一", "blue", "chinese 009；中文名有「角」"),
    "Rāmiḥ": ([ARC], "al-Simāk al-Rāmiḥ", "The high one with the spear", "拿矛的高舉者", "green",
              "arabic_al-sufi Boo_a_01：السماك الرامح（牧夫「兩腿之間」的星，不在牧夫連線上）"),
    "Aʿzal": ([SPI], "al-Simāk al-Aʿzal", "The armless high one", "沒拿武器的高舉者", "green",
              "arabic_al-sufi Vir_14：السماك الأعزل"),
    "牧夫座": (flat(SEG["Boo"]), "al-ʿAwwāʾ", "Boötes", "牧夫座", "amber",
             "arabic_al-sufi Boo العواء（吠叫者；沿用阿拉伯文《天文學大成》系統）"),
    "室女座": (flat(SEG["Vir"]), "al-ʿAdhrāʾ", "Virgo", "室女座", "amber", "arabic_al-sufi Vir العذراء（處女）"),
    "仙女座": (flat(SEG["And"]), "al-Musalsala", "Andromeda, the Chained Woman", "仙女座", "amber",
             "arabic_al-sufi And المسلسلة（被鎖鏈綁住的女子）"),
    "大魚": (FISH, "al-Ḥūt al-ʿAẓīm", "The great fish", "大魚（阿拉伯星座）", "green",
           "arabic_al-sufi SFA الحوت العظيم：仙女座 8 顆＋雙魚座 HIP 5454、6193、6706"),
    "M31": ((M31_RADEC[0], M31_RADEC[1]), "一小抹像雲的光斑", "laṭkha saḥābiyya", "仙女座大星系 M31", "white",
            "Kunitzsch 1987：魚嘴邊、ν And（仙女座第 14 星）旁的雲狀斑；約 250 萬光年"),
    "M31-近": ((M31_RADEC[0], M31_RADEC[1]), "laṭkha saḥābiyya", "a cloud-like smudge", "仙女座大星系・250 萬光年",
             "white", "Kunitzsch 1987；肉眼 3.4 等"),
    "魚嘴": ([NU_AND], "ν And", "And 14", "魚嘴（ν And）", "green", "arabic_al-sufi And_14；離 M31 1.3°"),
    "英仙座": (flat(SEG["Per"]), "Birshāwish", "Perseus", "英仙座", "amber", "arabic_al-sufi Per برشاوش（希臘名音譯）"),
    "Algol": ([ALGOL], "raʾs al-ghūl", "the ghoul's head → Algol", "妖怪的頭 → Algol（大陵五）", "red",
              "arabic_al-sufi Per_12 رأس الغول（托勒密「戈爾貢之頭」的阿拉伯譯名）；Kunitzsch & Smart"),
    "天頂": ((round(LST_AT["2000"], 2), PHI), "天頂（晚上 8 點）", "zenith 20:00", "天頂", "white",
           "台北 6/4 20:00 的天頂（J2000 近似）"),
    "Wāqiʿ": ([VEGA], "al-Nasr al-Wāqiʿ", "The landing eagle → Vega", "俯衝的老鷹 → Vega（織女）", "green",
              "arabic_al-sufi NasW النسر الواقع；Lyr_1"),
    "Ṭāʾir": ([ALT], "al-Nasr al-Ṭāʾir", "The flying eagle → Altair", "飛翔的老鷹 → Altair（牛郎）", "green",
              "arabic_al-sufi NasT النسر الطائر；Aql_3"),
    "北極星": ([POLARIS], "北極星", "Polaris", "北極星", "white", ""),
}


# ══════════════════════════════════════════════════════════════════
# 四、建置
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    S[M31] = (M31_RADEC[0], M31_RADEC[1], 99.0)
    S[ZEN] = (TERMS["天頂"][0][0], PHI, 99.0)
    T = TERMS
    MAINS = [ARC, SPI, VEGA, ALT, ALGOL, NU_AND]

    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=D_S, D_r=D_R, D_fill=D_FILL,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None, maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp, k = m.y_pole, m.k

    _orig = m._mark_parts

    def _mark_parts(hips, positions, style):
        out = []
        for h in hips:
            if h in MARK_V:
                r = m.sz_star(MARK_V[h]) * 1.5
                out += [(p[0], p[1], r if style == "dot" else max(1.1, r * 4.0)) for p in positions(h)]
            else:
                out += _orig([h], positions, style)
        return out
    m._mark_parts = _mark_parts

    # ── 構圖工具（北盤；畫布座標，盤心在 (0, yp)） ──
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
        """面北盤上、畫面 x 處的地平線 y（畫布座標）"""
        lst_obs = (LST0 - rot - 180.0) % 360.0
        best = None
        for ra, dec in horizon_points(PHI, lst_obs):
            p = disc_xy((ra, dec), rot)
            if p and (best is None or abs(p[0] - x) < abs(best[0] - x)) and p[1] < yp + 5:
                best = p
        return best[1]

    def hframe(cx, rot, fov, fh=0.17):
        """地平線（畫面中心那一點）放在離畫面下緣 fh 的高度"""
        cy = horizon_y(cx, rot) + (0.5 - fh) * fov * 16 / 9
        f = fov
        while far(cx, cy, f) > m.R_fill - 1.0:
            f *= 0.99
            cy = horizon_y(cx, rot) + (0.5 - fh) * f * 16 / 9
        return (round(cx, 2), round(cy, 2), round(f, 1), rot)

    P = {nm: disc_xy(h, R20) for nm, h in (("大角", ARC), ("角宿一", SPI), ("織女", VEGA), ("牛郎", ALT),
                                            ("M31", M31), ("ν And", NU_AND), ("大陵五", ALGOL),
                                            ("北極星", POLARIS), ("天頂", ZEN))}
    print("\n── 20:00 盤上位置（相對盤心） ──")
    for nm, (x, y) in P.items():
        print(f"  {nm:5s} ({x:+7.1f}, {y - yp:+7.1f})  r={math.hypot(x, y - yp):6.1f}")

    # ── 構圖 ──
    F01a = (0.0, round(yp + 34.0, 2), 140.0, R20)           # 總覽：北極（下）→ 天頂 → 角宿一（上）
    F01b = dfit([ARC, SPI, VEGA, POLARIS], R20, pad=0.08, minfov=112.0)
    # 06／12：大角＋角宿一＋牧夫座；室女座兩側出畫面沒關係（角宿一要離上緣安全區夠遠：畫面上 1/4 處）
    F06 = (14.0, round(yp + 92.0, 2), 80.0, R20)
    F07a = dfit(flat(SEG["And"]) + FISH, R20, pad=0.10)
    mx, my = disc_xy(M31, R20); nx, ny = disc_xy(NU_AND, R20)
    F07b = (round((mx + nx) / 2, 2), round((my + ny) / 2 - 0.6, 2), 14.0, R20)   # fov 10 時連線粗到 32 px，改 14
    F08 = F07a
    F10 = dfit(flat(SEG["Per"]), R20, pad=0.10)
    F12 = F06                                              # 回到 06 的構圖（天頂在畫面左側）
    F13a = hframe(80.0, R20, 86.0)
    F13b = hframe(80.0, R22, 86.0)
    assert abs(F13a[1] - F13b[1]) < 1e-6, "13 鏡：地平線固定在畫面上，兩格畫面中心應相同"
    F15 = (0.0, round(yp + 30.0, 2), 136.0, R22)
    FR = dict(F01a=F01a, F01b=F01b, F06=F06, F07a=F07a, F07b=F07b, F10=F10, F12=F12,
              F13a=F13a, F13b=F13b, F15=F15)
    print("\n── 構圖（cx, cy, fov, rot；cy 為畫布座標，盤心 yp=%.2f） ──" % yp)
    for kk, v in FR.items():
        print(f"  {kk} {v}  角落距盤心 {far(*v[:3]):.1f}")
    print("  旋轉：" + "、".join(f"{kk} {v:+.2f}°" for kk, v in ROT.items()))

    # ════════════════════ 標籤（全部 disc=True；dx/dy＝畫面方向） ════════════════════
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

    def lab(key, fov, dx=0.0, dy=0.0, px=48, zh=None, two=False, px2=38, gap=None, col=None, top=None, at=None):
        """一條標籤；px＝想要的 Canva 字級（1080 寬）。two＝上行 top（預設原文）＋下行中文；at＝改用別的錨點"""
        a, orig, en, zh0, c, _ = T[key]
        a = at or a
        s1 = px * fov / (m.fu * 1080)
        out = []
        if two:
            s2 = px2 * fov / (m.fu * 1080)
            g = gap if gap is not None else (s1 + s2) * m.fu * 0.62
            out.append(dict(anchor(a), text=top or orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy + g / 2, 2), key=key, disc=True))
            out.append(dict(anchor(a), text=zh or zh0, color="white", size=round(s2, 3), dx=round(dx, 2),
                            dy=round(dy - g / 2, 2), key=key + "-zh", disc=True))
        else:
            out.append(dict(anchor(a), text=zh or orig, color=col or c, size=round(s1, 3), dx=round(dx, 2),
                            dy=round(dy, 2), key=key, disc=True))
        return out

    LB = {}
    f6 = F06[2]
    LB["高舉者"] = (lab("Rāmiḥ", f6, dx=0.0, dy=10.0, px=48, two=True, px2=38)
                 + lab("Aʿzal", f6, dx=0.0, dy=7.0, px=48, two=True, px2=38)
                 + lab("牧夫座", f6, dx=-24.0, dy=-30.0, px=42, two=True, px2=34, col="amber", at=[ARC])
                 + lab("室女座", f6, dx=-21.0, dy=-37.0, px=42, two=True, px2=34, col="amber", at=[SPI]))
    f7 = F07a[2]
    LB["大魚"] = (lab("仙女座", f7, dx=15.0, dy=-17.0, px=44, two=True, px2=34)
                + lab("大魚", f7, dx=-8.0, dy=-17.5, px=48, two=True, px2=36)
                + lab("M31", f7, dx=8.0, dy=6.0, px=38, col="white"))
    f7b = F07b[2]
    LB["魚嘴"] = (lab("M31-近", f7b, dx=0.0, dy=2.6, px=50, two=True, px2=38)
                + lab("魚嘴", f7b, dx=-2.9, dy=-1.1, px=40, zh="魚嘴（ν And）"))
    f10 = F10[2]
    LB["英仙"] = (lab("英仙座", f10, dx=0.0, dy=14.0, px=46, two=True, px2=36)
                + lab("Algol", f10, dx=0.0, dy=-4.2, px=48, two=True, px2=38))
    f12 = F12[2]
    LB["今晚八點"] = (lab("Rāmiḥ", f12, dx=0.0, dy=10.0, px=46, two=True, px2=44, top="al-Simāk al-Rāmiḥ",
                         zh="大角")
                   + lab("Aʿzal", f12, dx=0.0, dy=7.0, px=46, two=True, px2=44, top="al-Simāk al-Aʿzal",
                         zh="角宿一")
                   + lab("天頂", f12, dx=0.0, dy=-3.6, px=36))
    f13 = F13a[2]
    LB["織女"] = lab("Wāqiʿ", f13, dx=0.0, dy=6.0, px=46, two=True, px2=36)
    LB["兩隻老鷹"] = LB["織女"] + lab("Ṭāʾir", f13, dx=2.0, dy=-9.0, px=46, two=True, px2=36)
    label_sets = [(v, k2) for k2, v in LB.items()]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    LG_MAIN = LG["牧室"] + LG["仙女"] + LG["英仙"] + LG["琴鷹"]
    LINE_SETS = [(LG[k2], LNAME[k2]) for k2 in LG]
    MARKS = [(MAINS, "主角星白點", "dot"), ([ARC], "大角光環", "ring"), ([M31], "仙女座大星系", "ring"),
             ([ZEN], "天頂", "ring")]
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_MAIN)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    for hips, name, style in MARKS:
        m.L_marks(hips, name, style)
    for items, name in label_sets:
        m.L_labels(items, name)
    m.build_discs(LG_MAIN, label_sets, mains=MAINS, line_sets=LINE_SETS, marks=MARKS)

    LINES_KEY = dict({"L4": "星座連線", "光": "大角光環", "雲": "仙女座大星系", "頂": "天頂"}, **LNAME)
    LINE_GROUPS = dict({"L4": LG_MAIN}, **LG)

    # ════════════════════ 鏡頭（全部在北盤圖層組上） ════════════════════
    ls = lambda *n: list(n)
    hold = lambda fr: [fr]
    shots = [
        dict(code="01", kind="R", sec=12, north=True, frames=[F01a, F01b], layers=[], labels=[],
             vo="上週，月亮在阿拉伯的二十八間旅店裡搬家。今晚翻開一本書：同一片星空，蘇菲看見——兩層天空。",
             card="同一片星空，／蘇菲看見——兩層天空。",
             note="開場：手稿書影淡入（若用 BnF Arabe 5036，角落標「1430 年代撒馬爾罕抄本」）→ 北盤（台北 6/4 20:00 面北，"
                  "北極在下、天頂在上）fov 140 推近到大角、角宿一、織女；開場字卡"),
        dict(code="02", kind="R", sec=17, north=True, frames=hold(F01b), layers=[], labels=[],
             overlay="C-A34-01_蘇菲是誰", overlay_layers=["生平層", "書名層"],
             vo="這本書叫《恆星圖像之書》，作者是波斯天文學家蘇菲，歐洲人叫他 Azophi。大約西元九百六十四年，"
                "他把書獻給當時的君主——到今年，已經一千零六十多年。",
             card="約 964 年・蘇菲",
             note="定格（01 迄格）疊 C-A34-01：生平時間軸（903 Rayy → 布伊王朝宮廷 → 約 964 獻書 ʿAḍud al-Dawla → 986 卒）"
                  "→ 書名 كتاب صور الكواكب الثابتة＋「al-Ṣūfī，波斯人，用阿拉伯文寫作」"),
        dict(code="03", kind="R", sec=15, north=True, frames=hold(F01b), layers=[], labels=[],
             overlay="C-A34-02_托勒密到蘇菲", overlay_layers=["星表層", "核對層"],
             vo="托勒密八百多年前寫下的四十八個希臘星座、一千多顆星，他一顆一顆重新對著天空看：亮度不對的，他改；"
                "托勒密漏掉的星，他在書裡點出來。",
             card="48 星座・1,000 多顆星",
             note="定格疊 C-A34-02：托勒密《天文學大成》星表（約 150 年，48 星座、1,022 顆）→ 蘇菲逐星核對：改亮度、點出漏掉的星"),
        dict(code="04", kind="R", sec=13, north=True, frames=hold(F01b), layers=[], labels=[],
             overlay="C-A34-03_歲差", overlay_layers=["黃道層", "平移層"],
             vo="星星的位置，他全部加上十二度四十二分：因為歲差，八百多年來，整片星空沿著黃道慢慢挪動，他得替自己的年代重算一次。",
             card="黃經＋12°42′",
             note="定格疊 C-A34-03：黃道上整份星表往東平移 12°42′（托勒密星表 → 964 年）"),
        dict(code="05", kind="R", sec=11, north=True, frames=hold(F01b), layers=[], labels=[],
             overlay="C-A34-03b_蘇菲的尺", overlay_layers=["單位層", "銀河層"],
             vo="他描述星的位置很有生活感，用「肘」來量距離，一肘大約是兩度二十分；有些星，他乾脆寫：這顆「碰到銀河」。",
             card="一肘≈2°20′",
             note="定格疊 C-A34-03b：指、拃、肘（約 2°20′）、矛（6 肘＝14°）比例尺 → 天鷹尾巴下「碰到銀河」那顆星"
                  "（HIP 93747，Aql_9）＋原文 مماس للمجرّة"),
        dict(code="06", kind="R", sec=19, north=True, frames=[F01b, F06], layers=["牧室", "光"],
             labels=ls("高舉者"), labels_start=[],
             vo="但這本書最特別的，是一次收進兩層天空。書裡每個希臘星座底下，他都附上古代阿拉伯人的老星名，"
                "再一顆顆對好：牧夫座的大角，叫「拿矛的高舉者」；室女座的角宿一，是「沒拿武器的高舉者」。",
             card="希臘星座×阿拉伯老星名",
             note="推近牧夫＋室女（蘇菲的連線，琥珀）；標籤 al-Simāk al-Rāmiḥ／al-Simāk al-Aʿzal＋中譯（綠）、"
                  "al-ʿAwwāʾ 牧夫座、al-ʿAdhrāʾ 室女座；大角不在蘇菲牧夫座的連線上（書中是「兩腿之間」的星）→ 大角光環層"),
        dict(code="07", kind="R", sec=20, north=True, frames=[F07a, F07b], layers=["仙女", "大魚", "雲"],
             labels=ls("魚嘴"), labels_start=ls("大魚"),
             vo="有些阿拉伯星座，他也一併畫進書裡：仙女座的身上，橫著一條阿拉伯人的大魚。就在大魚的嘴邊，他記下一小抹像雲的光斑"
                "——那是兩百五十萬光年外的仙女座大星系，也是目前所知最早寫下它的紀錄。",
             card="一小抹雲＝仙女座大星系",
             note="從 06 滑過北極到仙女座（北盤上直接 Match & Move，不換組）：仙女座（琥珀）＋大魚 al-Ḥūt al-ʿAẓīm"
                  "（綠，SFA 11 顆：仙女座 8＋雙魚座 3）＋M31 細圈；「就在大魚的嘴邊」起推近魚嘴 ν And＋M31（fov 10，標籤換成近景版）；"
                  "右上小框手稿仙女座圖（魚嘴上的點）由美宣放"),
        dict(code="08", kind="R", sec=13, north=True, frames=[F07b, F08], layers=["仙女", "大魚", "雲"],
             labels=ls("大魚"), labels_start=ls("魚嘴"),
             overlay="C-A34-04_天空與天球儀", overlay_layers=["天空層", "天球儀層"],
             vo="每個星座，他都畫兩次：一張是抬頭看到的天空，一張是天球儀上的樣子。天球儀是從外面看天，所以兩張圖剛好左右相反。",
             card="天空與天球儀：左右相反",
             note="拉回整個仙女座＋大魚；迄格定格疊 C-A34-04（用本集的仙女座＋大魚連線自繪：左＝天空中、右＝天球儀上，左右鏡像）"),
        dict(code="09", kind="R", sec=15, north=True, frames=hold(F08), layers=["仙女", "大魚"],
             labels=[],
             vo="牛津有一部有名的抄本，最後寫著：伊斯蘭曆四百年，由蘇菲的兒子抄寫。不過現代研究認為，這段題記是後人加上的，"
                "抄本本身大約是十二世紀末的。",
             card="牛津抄本・年代比題記晚",
             note="定格（08 迄格、星名標籤收掉）：手稿書影 MS. Marsh 144 題記頁（p.419；美宣下載，CC BY-NC 4.0，角落標"
                  "「MS. Marsh 144, Bodleian Libraries, University of Oxford」）＋小字「題記：400 H＝1009–10 年／抄本：約 12 世紀末」"),
        dict(code="10", kind="R", sec=15, north=True, frames=[F08, F10], layers=["英仙"],
             labels=ls("英仙"), labels_start=[],
             vo="抄本裡的希臘英雄，換上了伊斯蘭世界的衣著。例如英仙座：他手上提的那顆妖怪的頭，阿拉伯文叫 raʾs al-ghūl"
                "——今天大陵五的名字 Algol，就是這麼來的。",
             card="Algol＝妖怪的頭",
             note="滑到英仙座（蘇菲連線，琥珀）＋大陵五（紅）raʾs al-ghūl → Algol；右上小框 Marsh 144 的英仙圖（美宣；"
                  "用 BnF Arabe 5036 要標年代）"),
        dict(code="11", kind="R", sec=14, north=True, frames=hold(F10), layers=["英仙"], labels=[],
             vo="書裡的星圖，後來也傳進歐洲。德國畫家杜勒一五一五年的北天星圖，四個角落畫了四位天文學家；其中一位就是 Azophi"
                "——還被標成「阿拉伯人」。",
             card="杜勒 1515 星圖",
             note="定格（10 迄格）：杜勒 1515《北天星圖》（公版木刻；美宣找博物館公版高解析檔，滿版放在天空上）→ 推近右下角 Azophi Arabus"),
        dict(code="12", kind="R", sec=15, north=True, frames=[F10, F12], layers=["牧室", "光", "頂"],
             labels=ls("今晚八點"), labels_start=ls("英仙"),
             vo="今晚八點到十點，就能用蘇菲的眼睛看天：東方高處、快到頭頂的大角，和南方的角宿一，就是那兩位「高舉者」；"
                "巧的是，它們的中文名字，都有一個「角」字。",
             card="今晚 8 點：大角・角宿一",
             note="滑回大角＋角宿一（20:00 面北的盤：北極在下，所以天頂在大角旁邊、角宿一在更上面＝更南）；"
                  "標籤 阿拉伯名＋中文名，「角」字美宣在 Canva 加亮；天頂細圈＋「天頂（晚上 8 點）」"),
        dict(code="13", kind="R", sec=16, north=True, horizon=[PHI], frames=[F13a, F13b], layers=["琴鷹", "老鷹"],
             labels=ls("兩隻老鷹"), labels_start=ls("織女"),
             vo="還有七夕這一對：八點就在東北方的織女星，和十點以後在正東方升高的牛郎星，在阿拉伯是「俯衝的老鷹」和「飛翔的老鷹」；"
                "Vega、Altair 這兩個名字，就是從這裡來的。",
             card="兩隻老鷹",
             note=f"台北 6/4 面北、畫面移到東邊（山＝北方地平線，φ 25.03°）：20:00（{R20:+.1f}°）織女在東北 19°、牛郎還在地平線下"
                  f" → 22:00（{R22:+.1f}°，逆時針）織女 42°、牛郎正東 18.5°；天琴、天鷹（蘇菲連線，琥珀）＋兩隻老鷹（綠）"),
        dict(code="14", kind="R", sec=16, north=True, horizon=[PHI], frames=hold(F13b), layers=["琴鷹", "老鷹"],
             labels=ls("兩隻老鷹"), overlay="C-A34-05_用蘇菲的眼睛看天",
             vo="想找蘇菲的那一小抹雲？它過了午夜才升起，要等凌晨兩點半到三點半，往東北方看。這天剛好是新月，整夜沒有月光；"
                "找個遠離光害的暗處，肉眼就看得到。",
             card="2:30–3:30・東北方",
             note="定格（13 迄格）疊 9:16 圖卡 C-A34-05（可存圖）"),
        dict(code="15", kind="R", sec=12, north=True, horizon=[PHI], frames=[F13b, F15], layers=[], labels=[],
             vo="下週五，從蘇菲書裡的四十八個希臘星座，走到今天的八十八個：是誰把天空切成八十八塊、一點空隙都不留？",
             card="下集｜88 個星座誰說了算",
             note="同一片台北 22:00 的天空拉遠（連線、標籤收掉）；端卡「下集見｜現代星座（上）：88 個星座誰說了算」＋追蹤 CTA；"
                  "逐字稿寫的 IAU 星座邊界示意層屬 A-35 素材，本集不出"),
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
    print("  判斷後接受的 ⚠：" + WARN_OK)

    rows = []
    for sh in shots:
        for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
            ew = 2 * m.R_fill / fov * 1080
            off_ = (round(-cx / fov * 1080), round((cy - m.y_pole) / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"], "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "北盤圖層組（置中）", "元素寬px": round(ew), "位移X px": off_[0],
                         "位移Y px": off_[1], "旋轉度": round(rot, 1), "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[dict(s) for s in shots])

    # 數字核對（逐字稿星空對時表）
    print("\n── 數字核對 ──")
    for kk, v in LST_AT.items():
        print(f"  {T_TPE[kk]} LST {v:.2f} → 北盤 {ROT[kk]:+.2f}°")
    for nm, h in (("大角", ARC), ("角宿一", SPI), ("織女", VEGA), ("牛郎", ALT)):
        for t in ("2027/6/4 20:00", "2027/6/4 22:00"):
            a, z = altaz(*S[h][:2], t)
            print(f"  {t} {nm} 高 {a:5.1f}° 方位 {z:5.1f}°")
    for t in ("2027/6/5 02:00", "2027/6/5 02:30", "2027/6/5 03:30"):
        a, z = altaz(*M31_RADEC, t)
        print(f"  {t} M31 高 {a:5.1f}° 方位 {z:5.1f}°")
    d = math.degrees(math.acos(
        math.sin(math.radians(M31_RADEC[1])) * math.sin(math.radians(S[NU_AND][1])) +
        math.cos(math.radians(M31_RADEC[1])) * math.cos(math.radians(S[NU_AND][1])) *
        math.cos(math.radians(M31_RADEC[0] - S[NU_AND][0]))))
    print(f"  M31—ν And {d:.2f}°")

    terms = {}
    for key, (a, orig, en, zh, col, note) in T.items():
        terms[key] = dict(hips=a if isinstance(a, list) else [], 原文=orig, 拼音="", 英文翻譯=en, 中文=zh,
                          顏色=col, 來源備註=note)
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    PREV_LINES = LG_MAIN + LG["大魚"] + LG["老鷹"]
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
        g = [x for k2 in sh.get("layers", []) if k2 in LG for x in LG[k2]]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_end", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    A21.sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
                title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
