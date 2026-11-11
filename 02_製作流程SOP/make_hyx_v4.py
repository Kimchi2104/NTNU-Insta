# -*- coding: utf-8 -*-
"""H-元宵：天官賜福與紫微大帝｜大畫布 v4.6（45 秒特別短鉤子）

論點：元宵＝上元節、天官賜福；天官又稱紫微大帝，跟北天正中央的星區「紫微垣」同名——
  一個是信仰裡的神、一個是古人分的星區（同名，兩回事）。宮牆外的北斗＝帝車（《史記・天官書》），
  接昨天 A-22 白俄羅斯的以利亞之車。今晚往東：月亮夾在木星、火星之間，十五的月亮十六圓。

來源：Stellarium 新版 skycultures chinese（紫微右垣 CON 032、紫微左垣 033、北斗 039、北極 041、勾陳 083）、
  belarusian（Elias's Cart，片中拼法 Illioŭ voz 照 A-22）；天象 PyEphem 4.2.1 自算
  （台北 25.033°N 121.565°E，UTC+8）。逐字稿：04_腳本庫/H-元宵-…-v1.md。

鏡頭路線（全部在北盤圖層組上，沒有換組）：
  01–05 台北 2/20 面北（山＝北方地平線，φ 25.03°）：20:00 fov 140 → 80（定格疊 C-HYX-01）→ 推近紫微垣 fov 55
  → 逆時針 20:00→21:00（開頭疊 C-HYX-02 分欄字卡）→ 拉遠到北斗、續轉到 22:00。
  06 轉身面東（20:00 的東方天空）：同一個北盤再順時針轉約 120°、滑到月亮—木星—火星，畫面的「上」＝
  月亮所在方位的天頂方向——木星在上、月亮下偏右、火星在左下，和旁白一致。
  ※ v1 原寫「換組到東方長圖」：長圖北在上，木星與火星都會在月亮上方（木星 +15.7°、火星 +15.6°、月亮 +12.9°），
    和旁白「月亮上方是木星、左下是火星」對不上，所以改在盤上轉到面東的方位（盤可任意角旋轉、零斷層）。
  07 微拉遠，端卡（A-02 縮圖＋下集）。

參數
  lst = 272 → 由旋轉角決定：rot＝(lst − LST台北 − 180)，2/20 20:00 LST 91.77 → +0.2°、21:00 −14.8°、
             22:00 −29.8°；面東（20:00）約 +90°。整集落在 (−180, 180] 內，每段 M&M < 180°
             （05→06 的轉身 ≈ +120°，是「轉頭」不是時間倒流）。長圖帶本集不用（照規定生成）。
  D_s = 45、D_r = 49 → 北斗最南的搖光 +49.31 在盤本體；紫微垣牆星最南的上宰 +58.6。
  D_fill = −38.7 → k = 1.3975、R_fill = 179.85（＝A-21；盤寬 ÷ 畫布寬 ＝ 0.999183 ⚠ 只差 0.08%，Canva 千萬別設成同寬）：
             01 鏡 fov 140 面北、畫面往上挪讓地平線落在下方 1/4，角落距盤心 ≈168；06 鏡月亮在 dec +12.9（r≈108），
             畫面角落 ≈132；D_fill 0（R_fill 125.8）兩個都放不下。
  x_tN = x_tS = 0

check_shots 的 ⚠（判斷後接受）
  全部 R 鏡頭「畫面含長圖側扇區」：整集都在北盤圖層組上，從頭到尾不換回大畫布（沒有切點）。
"""
import os, sys, json, math, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "H-元宵"
OUT = os.path.join(BASE, "05_素材/H-元宵_紫微垣/_v4大畫布")
LST0 = 272.0
TPE = (25.0330, 121.5654)
PHI = 25.03
DATE = "2027/2/20"

import ephem


def obs(when):
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.elevation = 10
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    return o


def lst_at(when):
    return math.degrees(obs(when).sidereal_time())


def rot_north(when):
    """北盤面向北方：rot＝lst − lst_obs − 180，收在 (−180, 180]；Canva 正角＝順時針"""
    return round((LST0 - lst_at(when) - 180.0 + 180.0) % 360.0 - 180.0, 2)


T = {k: f"{DATE} {k}" for k in ("20:00", "21:00", "22:00")}
ROT = {k: rot_north(v) for k, v in T.items()}


def body(b, when):
    o = obs(when); o.pressure = 0
    b.compute(o)
    return (round(math.degrees(float(b.a_ra)), 3), round(math.degrees(float(b.a_dec)), 3),
            round(math.degrees(float(b.alt)), 1), round(math.degrees(float(b.az)), 1))


MOON = body(ephem.Moon(), T["20:00"])
JUP = body(ephem.Jupiter(), T["20:00"])
MARS = body(ephem.Mars(), T["20:00"])
_m = ephem.Moon(); _m.compute(obs(T["20:00"]))
MOON_PHASE = round(_m.phase, 1)

# ══════════════════════════════════════════════════════════════════
# 一、星
# ══════════════════════════════════════════════════════════════════
POLARIS, KOCHAB, REGULUS = 11767, 72607, 49669
RIGHT = [68756, 61281, 56211, 46977, 33104, 22783, 15520]           # 紫微右垣（右樞→上丞）
LEFT = [75458, 78527, 80331, 83895, 92782, 101260, 114222, 3721]    # 紫微左垣（左樞→少丞）
POLE5 = [75097, 72607, 70692, 69112, 62572]                         # 北極五星（太子、帝、庶子、后宮、紐星）
DIPPER = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
WALLS = RIGHT + LEFT
MAINS = WALLS + POLE5 + [POLARIS] + DIPPER + [REGULUS]


def x_of(ra):
    return ((LST0 - ra) + 180.0) % 360.0 - 180.0


# ══════════════════════════════════════════════════════════════════
# 二、連線（Stellarium 新版 skycultures）
# ══════════════════════════════════════════════════════════════════
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")


def load_sc(cu, key="english"):
    d = json.load(open(os.path.join(SC_NEW, cu, "index.json"), encoding="utf-8"))
    out = {}
    for c in d["constellations"]:
        segs = [[h for h in l if isinstance(h, int)] for l in c.get("lines", [])]
        out[c["common_name"][key]] = [s for s in segs if len(set(s)) >= 2]
    return out


CH = load_sc("chinese")
SEG_WALLS = CH["Purple Forbidden Right Wall"] + CH["Purple Forbidden Left Wall"]
SEG_POLE = CH["Northern Pole"]
SEG_GOU = CH["Curved Array"]
SEG_DIPPER = CH["Northern Dipper"]
assert [h for s in SEG_WALLS for h in s] == WALLS and SEG_DIPPER == [DIPPER]

LG_WALLS = [(SEG_WALLS, "amber", 1.0)]
LG_POLE = [(SEG_POLE, "purple", 1.0), (SEG_GOU, "green", 1.0)]
LG_DIPPER = [(SEG_DIPPER, "amber", 1.0)]
LG_ALL = LG_WALLS + LG_POLE + LG_DIPPER
LINE_SETS = [(LG_WALLS, "連線-紫微垣"), (LG_POLE, "連線-北極勾陳"), (LG_DIPPER, "連線-北斗")]
LINES_KEY = {"L4": "星座連線", "垣": "連線-紫微垣", "極": "連線-北極勾陳", "斗": "連線-北斗",
             "月": "月亮與行星（2-20 20-00）"}
LINE_GROUPS = {"L4": LG_ALL, "垣": LG_WALLS, "極": LG_POLE, "斗": LG_DIPPER}


def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def radec(v):
    n = math.sqrt(sum(c * c for c in v))
    x, y, z = (c / n for c in v)
    return math.degrees(math.atan2(y, x)) % 360, math.degrees(math.asin(z))


def centroid(hips, S):
    hs = [h for h in hips if h in S]
    return radec([sum(vec(*S[h][:2])[i] for h in hs) for i in range(3)])


# ══════════════════════════════════════════════════════════════════
# 三、旁白字數（中文字＋外文音節；與 A 系列同一套算法）
# ══════════════════════════════════════════════════════════════════
def vo_units(t):
    n = 0
    for w in re.findall(r"[A-Za-zÀ-ɏʻʿʾʼ]+|[α-ω]|\d+|[㐀-鿿〇]", t):
        if re.match(r"[㐀-鿿〇]", w):
            n += 1
        elif re.match(r"[α-ω]", w):
            n += 2
        elif w.isdigit():
            n += len(w)
        elif w.isupper() and len(w) <= 4:
            n += len(w)
        else:
            n += max(1, len(re.findall(r"[aeiouyáéíóúŭ]+", w.lower())))
    return n


# ══════════════════════════════════════════════════════════════════
# 四、自訂圖層：月亮＋木星＋火星（台北 2/20 20:00 的位置）
# ══════════════════════════════════════════════════════════════════
def tangent_pt(ra0, dec0, x, y):
    dec = dec0 + y
    ra = ra0 + x / max(0.05, math.cos(math.radians(dec0)))
    return ra % 360, dec


def circle(ra0, dec0, r, n=48):
    return [tangent_pt(ra0, dec0, r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n))
            for i in range(n + 1)]


def custom_layers():
    def sky(s, pos, runs):
        for (ra, dec), r, col, glow in ((MOON[:2], 0.27, "#FFF6D8", (2.6, 1.8, 1.25)),
                                        (JUP[:2], 0.20, "#FFF3E0", (2.6, 1.6)),
                                        (MARS[:2], 0.16, "#FFB38A", (2.6, 1.6))):
            for k, op in zip(glow, (0.06, 0.10, 0.18)):
                s.poly_fill(runs(circle(ra, dec, r * k)), fill=col, opacity=op)
            s.poly_fill(runs(circle(ra, dec, r)), fill=col, opacity=1.0)

    return [("月亮與行星（2-20 20-00）", sky)]


def write_custom(m, layers, discs=False):
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


# ══════════════════════════════════════════════════════════════════
# 五、名詞總表（＝標籤對照表）
#   key：(錨點, 片中文字, 拼音／原文, 英文, 中文說明, 顏色, 來源／備註)
# ══════════════════════════════════════════════════════════════════
TERMS = {
    "紫微垣": (WALLS, "紫微垣", "Zǐ Wēi Yuán", "Purple Forbidden Enclosure", "紫微左垣 8 星＋右垣 7 星", "amber",
            "Stellarium chinese CON 032／033；《史記・天官書》稱紫宮，《晉書・天文志》「一曰紫微，大帝之坐也」"),
    "北極星": ([POLARIS], "北極星", "Gōu Chén Yī", "Polaris (α UMi)", "勾陳一（今天的北極星）", "white",
            "Stellarium chinese CON 083 勾陳；定位小字（「帝＝北極二」留給首留言）"),
    "帝車": (DIPPER, "帝車", "Dì Chē", "The Emperor's Chariot (Northern Dipper)", "北斗", "amber",
           "《史記・天官書》「斗為帝車，運于中央，臨制四鄉」；Stellarium chinese CON 039"),
    "Illioŭ voz": (DIPPER, "Illioŭ voz", "Іллёў воз（Stellarium: Illyouo voz）", "Elias's Cart (Belarusian)",
                   "以利亞的車（白俄羅斯）", "red", "Stellarium belarusian 001；拼法照 A-22（昨天那集），旁白不唸"),
    "月亮": (MOON[:2], f"月亮 {MOON_PHASE}%", "", "Moon", "月亮（台北 2/20 20:00）", "white",
           "PyEphem 自算：高 35.7°、方位 92.4°；望在 2/21 07:23"),
    "木星": (JUP[:2], "木星", "", "Jupiter", "木星（−2.55 等）", "white", "PyEphem 自算：高 40.8°、方位 90.7°；Mallama & Hilton 2018"),
    "火星": (MARS[:2], "火星", "", "Mars", "火星（−1.28 等）", "white", "PyEphem 自算：高 31.2°、方位 86.5°；2/19 23:51 衝日"),
    "軒轅十四": ([REGULUS], "軒轅十四", "Xuān Yuán Shí Sì", "Regulus (α Leo)", "軒轅十四（1.4 等，緊鄰滿月、市區難見）",
             "white", "Stellarium chinese；只放小字"),
    "望": (MOON[:2], "最圓（望）2/21 07:23", "", "Full moon 2027-02-21 07:23 (UTC+8)", "望", "white",
          "PyEphem；USNO 23:23 UT（Gemini 核過）"),
}


# ══════════════════════════════════════════════════════════════════
# 六、標籤與鏡頭
# ══════════════════════════════════════════════════════════════════
def build():
    S = dict(G.load_stars(BASE))
    os.makedirs(OUT, exist_ok=True)
    m = Master(EP, S, OUT, lst=LST0, D_s=45, D_r=49, D_fill=-38.7,
               w_c=34, feather=8, x_tN=0.0, x_tS=0.0, phi=None,
               maglim=5.5, mw_n=15000)
    if not MC.selftest(m):
        sys.exit("幾何自測失敗，中止")
    yp = m.y_pole
    kk = m.k

    def anchor(a):
        if isinstance(a, tuple):
            return {"ra": a[0], "dec": a[1]}
        if len(a) == 1:
            return {"hip": a[0]}
        ra, dec = centroid(a, S)
        return {"ra": ra, "dec": dec}

    def item(a, text, color, size, dx, dy, key):
        return dict(anchor(a), text=text, color=color, size=size, dx=round(dx, 2),
                    dy=round(dy, 2), key=key, disc=True)

    def lone(key, size, dx, dy, text=None, color=None, a=None):
        a0, t, _, _, _, col, _ = TERMS[key]
        return [item(a if a is not None else a0, text or t, color or col, size, dx, dy, key)]

    # ════════════════════ 構圖（盤上：照旋轉角算星在畫面上的位置） ════════════════════
    def disc_xy(hip_or_radec, rot):
        ra, dec = (S[hip_or_radec][:2] if isinstance(hip_or_radec, int) else hip_or_radec[:2])
        keep = m.lst
        m.lst = LST0 - rot                      # 北盤：rot ≡ lst 平移（與 sb_grid 相同）
        p = m.pos_disc(ra, dec, True)
        m.lst = keep
        return (p[0][0], p[0][1] + yp) if p else None

    def far(cx, cy, fov):
        return max(math.hypot(cx + sx * fov / 2, cy + sy * fov * 8 / 9 - yp)
                   for sx in (-1, 1) for sy in (-1, 1))

    # 面北：地平線北點在盤心正下方 k·φ；fov 越大畫面越往上挪，讓地平線落在畫面下方約 1/4（y_px ≈ 1440）
    def north_frame(fov, rot, horizon_px=1440.0, dx=0.0):
        u = 1080.0 / fov
        cy = (yp - kk * PHI) + (horizon_px - 960.0) / u
        f = (round(dx, 2), round(cy, 2), fov, rot)
        assert far(f[0], f[1], fov) <= m.R_fill - 0.5, (f, far(f[0], f[1], fov))
        return f

    F01a = north_frame(140.0, ROT["20:00"])
    F01b = north_frame(80.0, ROT["20:00"])
    F03 = north_frame(68.0, ROT["20:00"], horizon_px=1700.0, dx=4.0)
    F04 = north_frame(68.0, ROT["21:00"], horizon_px=1700.0, dx=4.0)
    F05 = north_frame(100.0, ROT["22:00"], horizon_px=1500.0, dx=16.0)

    # 面東：畫面的「上」＝月亮所在方位的天頂方向
    o = obs(T["20:00"]); o.pressure = 0

    def up_angle(rot):
        a = disc_xy(MOON[:2], rot)
        ra2, dec2 = o.radec_of(math.radians(MOON[3]), math.radians(MOON[2] + 1.0))
        b = disc_xy((math.degrees(float(ra2)), math.degrees(float(dec2))), rot)
        return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))

    rot_e = ROT["20:00"] + 90.0
    for _ in range(30):                           # 解 up_angle(rot) = 90°
        err = ((up_angle(rot_e) - 90.0 + 180) % 360) - 180
        if abs(err) < 0.01:
            break
        rot_e += err * 0.9
    rot_e = round(rot_e, 1)
    GROUP = [MOON[:2], JUP[:2], MARS[:2], REGULUS]
    pts = [disc_xy(p, rot_e) for p in GROUP]
    gx = (max(p[0] for p in pts) + min(p[0] for p in pts)) / 2
    gy = (max(p[1] for p in pts) + min(p[1] for p in pts)) / 2
    F06 = (round(gx, 2), round(gy - 2.0, 2), 44.0, rot_e)
    F07 = (round(gx, 2), round(gy - 4.0, 2), 60.0, rot_e)
    ROT["面東 20:00"] = rot_e
    for f in (F06, F07):
        assert far(f[0], f[1], f[2]) <= m.R_fill - 0.5, f

    def screen(p, fr):                            # 畫布座標 → 1080×1920 頁面 px（檢查用）
        u = 1080.0 / fr[2]
        return (540 + (p[0] - fr[0]) * u, 960 - (p[1] - fr[1]) * u)

    print("\n── 構圖 ──")
    for nm, f in (("01a", F01a), ("01b", F01b), ("03", F03), ("04", F04), ("05", F05), ("06", F06), ("07", F07)):
        print(f"  {nm} {f}  角落距盤心 {far(f[0], f[1], f[2]):.1f}")
    print("  06 畫面位置（px）：" + "、".join(
        f"{n} ({screen(disc_xy(p, rot_e), F06)[0]:.0f},{screen(disc_xy(p, rot_e), F06)[1]:.0f})"
        for n, p in zip(("月", "木", "火", "軒轅十四"), GROUP)))
    for nm, fr, hips in (("03迄", F03, WALLS), ("04迄", F04, WALLS), ("05迄", F05, DIPPER + WALLS)):
        sp = [screen(disc_xy(h, fr[3]), fr) for h in hips]
        print(f"  {nm} 畫面 x {min(p[0] for p in sp):.0f}…{max(p[0] for p in sp):.0f}、"
              f"y {min(p[1] for p in sp):.0f}…{max(p[1] for p in sp):.0f}")
    print("  05迄 北斗：" + "、".join(f"({screen(disc_xy(h, F05[3]), F05)[0]:.0f},{screen(disc_xy(h, F05[3]), F05)[1]:.0f})" for h in DIPPER))

    # ════════════════════ 標籤（dx/dy＝畫面方向，單位＝畫布單位；看過 SB-鏡頭牆後調） ════════════════════
    LB_ZW = (lone("紫微垣", 2.6, 0.0, 0.0, a=(0.0, 90.0)) + lone("北極星", 1.9, 3.2, 1.6))
    # 05 迄格 fov 100（u≈10.8 px）：北斗在畫面右側、斗杓朝右下；三行疊在斗口上方的空天區
    # Canva 字級 ≈ size × 18.4 px（帝車 66 px、下兩行 52 px）；行距 ≥ 1.2 倍字級
    LB_DC = (lone("帝車", 3.6, 2.7, 29.5) +
             lone("Illioŭ voz", 2.8, 2.7, 23.0) + lone("Illioŭ voz", 2.8, 2.7, 17.2, text="以利亞的車", color="white"))
    LB_DC[-1]["key"] = "Illioŭ voz-zh"
    # 06 迄格 fov 44：Canva 字級 ≈ size × 41.8 px（1.4≈59 px、1.0≈42 px）；標籤 ha=center，左右放要加半個字寬，
    # 「最圓（望）…」約 460 px 寬，中心不能超過 x≈840（右緣 1080）
    LB_EAST = (lone("木星", 1.4, 0.0, 2.0) + lone("月亮", 1.4, 6.8, 0.0) +
               lone("火星", 1.4, -2.9, 0.0) + lone("軒轅十四", 1.1, 4.3, 0.0) +
               lone("望", 1.0, 4.9, -2.3))

    # 紫微垣：字放在盤心（北極）上方空天區；帝車：北斗質心旁（依 22:00 迄格的畫面方向）
    zw = disc_xy((0.0, 90.0), ROT["20:00"])
    LB_ZW[0]["dy"] = 13.0
    dc = disc_xy(centroid(DIPPER, S), ROT["22:00"])
    label_sets = [(LB_ZW, "紫微垣"), (LB_DC, "帝車"), (LB_EAST, "今晚東方")]

    print("\n── 防豆腐預檢 ──")
    MC.glyph_audit([it["text"] for items, _ in label_sets for it in items])

    print("\n── 大畫布圖層 ──")
    m.L_milkyway()
    m.L_stars(mains=MAINS)
    m.L_grid()
    m.L_lines(LG_ALL)
    for g, name in LINE_SETS:
        m.L_lines(g, name=name)
    custom = custom_layers()
    write_custom(m, custom)
    m.L_marks(MAINS, "主角星白點", "dot")
    for items, name in label_sets:
        m.L_labels(items, name)

    m.build_discs(LG_ALL, label_sets, mains=MAINS, line_sets=LINE_SETS,
                  marks=[(MAINS, "主角星白點", "dot")])
    write_custom(m, custom, discs=True)

    # ════════════════════ 鏡頭 ════════════════════
    ls = lambda *n: list(n)
    shots = [
        dict(code="01", kind="R", sec=5, north=True, horizon=[PHI],
             frames=[F01a, F01b], layers=["垣"], labels=[], labels_start=[],
             vo="同一片星空，元宵這一晚——人們拜天官。",
             card="元宵拜天官",
             note=f"開場字卡；北盤＝台北 2/20 20:00 面北（山＝北方地平線，φ 25.03°，盤 {ROT['20:00']:+.1f}°）；"
                  "fov 140→80 推近；紫微左右垣（琥珀）淡入。左樞貼地平線、上宰少宰還在山下＝真的（首留言說明）"),
        dict(code="02", kind="R", sec=4, north=True, horizon=[PHI],
             frames=[F01b], layers=["垣"], labels=[], labels_start=[],
             overlay="C-HYX-01_上元天官", overlay_layers=["上元層", "三元層"],
             vo="元宵是上元節，天官大帝的生日——天官賜福。",
             card="上元・天官賜福",
             note="畫面不動；定格疊 C-HYX-01（先放大「上元 正月十五｜天官賜福」，再淡入中元、下元的淡色小字）"),
        dict(code="03", kind="R", sec=6, north=True, horizon=[PHI],
             frames=[F01b, F03], layers=["垣", "極"], labels=ls("紫微垣"), labels_start=[],
             vo="天官又稱紫微大帝，跟北天正中央那片星區同名：紫微垣。",
             card="紫微大帝｜紫微垣",
             note="推近紫微垣 fov 80→68；紫微左右垣（琥珀）＋北極五星（紫）＋勾陳（綠）；"
                  "標籤只放「紫微垣」＋北極星定位小字"),
        dict(code="04", kind="R", sec=8, north=True, horizon=[PHI],
             frames=[F03, F04], layers=["垣", "極"], labels=ls("紫微垣"),
             overlay="C-HYX-02_同名兩回事", overlay_layers=["天官層", "紫微垣層"], overlay_at="start",
             vo="一個是信仰裡的神，一個是古人分的星區——紫微垣是天帝的宮城，整片天繞著它轉。",
             card="同名，兩回事",
             note=f"開始頁後疊 C-HYX-02 左右分欄（左「三官信仰：天官」→ 右「古代星官：紫微垣」）；"
                  f"破折號後分欄淡出，盤逆時針 20:00→21:00（{ROT['20:00']:+.1f}°→{ROT['21:00']:+.1f}°）"),
        dict(code="05", kind="R", sec=8, north=True, horizon=[PHI],
             frames=[F04, F05], layers=["垣", "極", "斗"], labels=ls("紫微垣", "帝車"), labels_start=ls("紫微垣"),
             vo="宮牆外就是北斗，司馬遷說「斗為帝車」；昨天白俄羅斯那集，它是以利亞的火焰馬車。",
             card="北斗＝天帝的車",
             note=f"拉遠 fov 68→100、續轉 21:00→22:00（{ROT['21:00']:+.1f}°→{ROT['22:00']:+.1f}°）；"
                  "垣外的北斗（琥珀）亮起＋標籤「帝車」；跨文化標籤（紅）Illioŭ voz／以利亞的車（旁白不唸）"),
        dict(code="06", kind="R", sec=8, north=True,
             frames=[F05, F06], layers=["月"], labels=ls("今晚東方"), labels_start=ls("紫微垣", "帝車"),
             vo="晚上七到十點往東看：月亮上方是木星、左下是火星；十五的月亮，明早七點多才最圓。",
             card="十五的月亮十六圓",
             note=f"轉身面東：同一個北盤順時針轉到 {rot_e:+.1f}°、滑到台北 2/20 20:00 的東方天空"
                  "（畫面上＝天頂方向：木星在上、月亮下偏右、火星左下、軒轅十四在月亮正下方小字）；"
                  "月亮與行星＝自訂層；山留在模板位置（真的地平線在畫面下方約 31°）"),
        dict(code="07", kind="R", sec=6, north=True,
             frames=[F06, F07], layers=["月"], labels=ls("今晚東方"),
             vo="想看整座紫微垣，回頭看《三垣》；下週五，去羅馬尼亞找牧羊人。",
             card="下集：牧羊人的星空農場",
             note="微拉遠；端卡：A-02（EP2）《三垣：天上的紫禁城》縮圖＋「2/26 羅馬尼亞：牧羊人的星空農場」＋追蹤 CTA"),
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
            xt, yc = m.xtN, m.y_pole
            ew = 2 * m.R_fill / fov * 1080
            off = (round(-(cx - xt) / fov * 1080), round((cy - yc) / fov * 1080))
            rows.append({"鏡頭": sh["code"], "原型": sh["kind"],
                         "秒數": sh["sec"] if i == 0 else "",
                         "格": "起" if i == 0 else ("迄" if i == len(sh["frames"]) - 1 else "中"),
                         "用檔": "北盤圖層組（置中）", "元素寬px": round(ew), "位移X px": off[0],
                         "位移Y px": off[1], "旋轉度": round(rot, 1),
                         "說明": sh["note"] if i == 0 else ""})
    with open(os.path.join(OUT, f"{EP}_鏡頭清單.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(shots, open(os.path.join(OUT, f"{EP}_鏡頭清單.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ {EP}_鏡頭清單.csv / .json（總長 {tot_s} 秒）")
    m.save_manifest(shots=[{k: v for k, v in s.items()} for s in shots])

    print("  北盤旋轉角（台北 2/20）：" + "、".join(f"{k} {v:+.1f}°" for k, v in ROT.items()))
    print(f"  月亮 RA {MOON[0]} Dec {MOON[1]:+.2f}（{MOON_PHASE}%）、木星 {JUP[:2]}、火星 {MARS[:2]}；"
          f"y_pole {yp:.2f}、R_fill {m.R_fill:.2f}、k {kk:.4f}")

    terms = {k: dict(hips=(v[0] if isinstance(v[0], list) else []), 原文=v[1], 拼音=v[2], 英文翻譯=v[3],
                     中文=v[4], 顏色=v[5], 來源備註=v[6]) for k, v in TERMS.items()}
    json.dump({"ep": EP, "label_sets": [{"name": n, "items": it} for it, n in label_sets],
               "terms": terms, "cross": [], "mains": MAINS, "lines": LINES_KEY, "line_groups": LINE_GROUPS,
               "rot_taipei": ROT, "lst0": LST0, "phi": PHI},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    print("\n── 預覽與分鏡 ──")
    for items, name in label_sets:
        m.preview(os.path.join(OUT, f"{EP}_預覽黑底-{name}.png"), line_groups=LG_ALL,
                  labels=[dict(it, pt=6) for it in items], title=f"{EP}　大畫布 v4.6（{name}標籤）")
    import make_a07_v4 as A7
    A7.EP, A7.OUT = EP, OUT
    A7.storyboard(m, shots, LG_ALL)
    # 鏡頭牆看得到月亮與行星：只在畫縮圖時當成亮星塞進 m.S（SVG 圖層已經寫完，不受影響）
    for i, (b, v) in enumerate(((MOON, -6.0), (JUP, -2.6), (MARS, -1.3))):
        m.S[9000001 + i] = (b[0], b[1], v)
    import make_a21_v4 as A21
    LS = {n: it for it, n in label_sets}
    walls = []
    for sh in shots:
        g = [x for k in sh.get("layers", []) for x in LINE_GROUPS.get(k, [])]
        labs = sorted(set(sh.get("labels", []) + sh.get("labels_start", [])))
        walls.append((sh, g, [dict(it, pt=5) for n in labs for it in LS[n]]))
    A21.sb_wall(m, os.path.join(OUT, f"{EP}_SB-鏡頭牆.png"), walls,
                title=f"{EP}　逐鏡頭 9:16 縮圖牆（紅框＝起格・暗框＝迄格）　總長 {tot_s} 秒")
    print("\n完成 →", OUT)


if __name__ == "__main__":
    build()
