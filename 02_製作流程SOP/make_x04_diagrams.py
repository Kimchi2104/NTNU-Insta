# -*- coding: utf-8 -*-
"""X-04 春空導航術｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-X04-01_弧線是真的         → 04 鏡（星點層→圓層→偏差層）
  C-X04-02_斗柄鐘面           → 06 鏡（鐘面層→四季層）
  C-X04-03_赫西俄德的黃昏     → 08 鏡（前700層→阿斯克拉2027層→台北層）
  C-X04-04_大角在走路         → 11 鏡（星點層→軌跡層）
  C-X04-05_春季大三角與大鑽石 → 13 鏡（9:16 圖卡，可存圖）
  C-X04-06_今晚抬頭看         → 14 鏡（9:16 圖卡，可存圖）
  C-X04-07_兩顆星同時升起     → 10 鏡（檀香山層→台北層）
輸出：05_素材/X-04_春空導航/_概念圖/（--lang en → _概念圖/en/，這次只出 zh）

來源：Stellarium modern（RH1、SpT、GDi）；Hipparcos 新歸算（van Leeuwen 2007）視差與自行
（大角 μα* −1093.4、μδ −1999.4 mas/yr）；Hesiod, Works and Days 564–570；Halley 1718, Phil. Trans. 30;
《鶡冠子・環流》。天象一律 PyEphem 4.2.1 自算（逐字稿「星空對時」表）；圖上的數字由本檔重算後印出核對。
星點位置＝以弧線圓心（或圖中心）為切點的方位等距投影，東在左、北在上（星圖方向）；
斗柄鐘面＝面北看的天空（東在右）。不臨摹任何已出版圖。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-04_春空導航/_概念圖")
C.set_base(OUT)
RED, GREY, SUN = "#FF6B6B", "#7C8BA8", "#FF9E5E"
S = None
LANG = "zh"
TPE = (25.0330, 121.5654)
POLARIS, ARCTURUS, SPICA = 11767, 69673, 65474
DUB, MER, PHE, MEG, ALI, MIZ, ALK = 54061, 53910, 58001, 59774, 62956, 65378, 67301
DIPPER = [DUB, MER, PHE, MEG, ALI, MIZ, ALK]
DENEBOLA, COR_CAROLI, REGULUS = 57632, 63125, 49669

TXT = {
    "zh": {
        "c01_title": "四顆星，同一個圓", "c01_sub": "過搖光、大角、角宿一的圓：半徑 {:.1f}°（星圖方向：東在左）",
        "開陽": "開陽", "搖光": "搖光", "玉衡": "玉衡", "天權": "天權", "天璣": "天璣", "天璇": "天璇", "天樞": "天樞",
        "大角": "大角", "角宿一": "角宿一", "center": "圓心",
        "off_miz": "開陽：離圓 {:.2f}°", "off_ali": "玉衡：離圓 {:.1f}°",
        "c01_foot": "斗柄三顆自己的弧半徑只有 {:.1f}°——照它畫會彎回去；要看的是這道大弧",
        "c02_title": "斗柄鐘面", "c02_sub": "黃昏・面向北方・北極星＝鐘心",
        "spring": "三點鐘＝東\n春", "summer": "十二點＝南\n夏", "autumn": "九點＝西\n秋", "winter": "六點＝北\n冬",
        "winter_note": "今天台灣冬天黃昏，搖光在地平線下", "hand": "斗柄末端（搖光）", "pole": "北極星",
        "quote": "「斗柄東指，天下皆春」——《鶡冠子・環流》",
        "c03_title": "赫西俄德的黃昏", "c03_sub": "太陽剛下山，大角從東方地平線冒出來",
        "r1a": "前 700 年・阿斯克拉（希臘）", "r1b": "冬至後 62 天：大角黃昏升起 → 修剪葡萄藤",
        "r2a": "2027 年・阿斯克拉", "r2b": "4 月 1 日前後（地軸在晃）",
        "r3a": "2027 年・台北", "r3b": "4 月 9 日：日落 18:13，大角 18:20 升起",
        "ene": "東北東 68.5°", "east": "東", "horizon": "地平線",
        "c04_title": "大角在走路", "c04_sub": "每 821 年移動一個月亮寬（0.52°）・東在左、北在上",
        "y150": "托勒密時代（約 150 年）", "y2027": "今天", "y3000": "西元 3000 年",
        "moon": "月亮直徑 0.52°", "halley": "1718 年哈雷比對古希臘星表：星星自己會走",
        "右攝提": "右攝提（牧夫 η τ υ）",
        "c05_title": "春季大三角・春季大鑽石", "c05_sub": "大角＋角宿一＋五帝座一，再補常陳一",
        "tri": "春季大三角", "dia": "春季大鑽石", "五帝座一": "五帝座一", "常陳一": "常陳一", "軒轅十四": "軒轅十四",
        "tri_note": "三邊 {:.1f}°・{:.1f}°・{:.1f}°：幾乎正三角形",
        "alt_note": "虛線：有的星圖（含 Stellarium）用軒轅十四代替五帝座一",
        "c05_r1": "大角", "c05_r1b": "橘色・北半天球最亮的恆星・37 光年",
        "c05_r2": "角宿一", "c05_r2b": "藍白・約 250 光年（乾隆年間出發的光）",
        "c05_r3": "五帝座一", "c05_r3b": "獅子座尾巴・36 光年",
        "c05_r4": "常陳一", "c05_r4b": "獵犬座・113 光年",
        "c05_how": "找法：北斗斗柄 → 大弧 → 大角 → 角宿一",
        "c06_title": "今晚抬頭看", "c06_sub": "台北・2027 年 4 月 9 日（五）",
        "c06_w": "19:30　往西北西看", "c06_w2": "一彎很細的月牙，高 13°（19:45 以後就太低）",
        "c06_e": "21:00　往東看", "c06_e2": "北斗在北方偏東，順著斗柄畫大弧",
        "c06_top": "頭頂偏西南：木星、火星（行星，別算進三角）",
        "N": "北", "NE": "東北", "E": "東", "SE": "東南", "W": "西", "NW": "西北",
        "月牙": "月牙", "北斗": "北斗", "木星": "木星", "火星": "火星",
        "c07_title": "兩顆星，同時升起", "c07_sub": "2027 年 4 月 9 日・東方地平線",
        "hnl": "檀香山", "hnl2": "角宿一 19:01、大角 19:02——只差 1.3 分鐘",
        "tpe": "台北", "tpe2": "大角 18:20、角宿一 18:28——差 8 分鐘",
        "canoe": "Hōkūleʻa（大角）與 Hikianalia（角宿一）：近代復航的兩艘航海獨木舟",
        "foot": "#萬國星空　#師大天文社",
        "src05": "Stellarium modern：Spring Triangle（軒轅十四版）、Great Diamond；距離：Hipparcos 2007",
        "src06": "PyEphem 自算（台北 25.03°N；高度含大氣折射）",
    },
    "en": {
        "c01_title": "Four stars, one circle", "c01_sub": "Circle through Alkaid, Arcturus, Spica: radius {:.1f}° (east left)",
        "開陽": "Mizar", "搖光": "Alkaid", "玉衡": "Alioth", "天權": "Megrez", "天璣": "Phecda", "天璇": "Merak",
        "天樞": "Dubhe", "大角": "Arcturus", "角宿一": "Spica", "center": "centre",
        "off_miz": "Mizar: {:.2f}° off", "off_ali": "Alioth: {:.1f}° off",
        "c01_foot": "The handle's own curve has a radius of only {:.1f}° — follow the big arc instead",
        "c02_title": "The handle clock", "c02_sub": "Dusk · facing north · Polaris at the centre",
        "spring": "3 o'clock = east\nspring", "summer": "12 = south\nsummer", "autumn": "9 = west\nautumn",
        "winter": "6 = north\nwinter", "winter_note": "Winter dusk in Taiwan: Alkaid is below the horizon",
        "hand": "end of the handle (Alkaid)", "pole": "Polaris",
        "quote": "\"Handle points east: spring everywhere\" — Heguanzi",
        "c03_title": "Hesiod's dusk", "c03_sub": "Sun just set; Arcturus clears the eastern horizon",
        "r1a": "700 BC · Ascra, Greece", "r1b": "60 days after the solstice: Arcturus rises at dusk → prune the vines",
        "r2a": "2027 · Ascra", "r2b": "around 1 April (Earth's axis wobbles)",
        "r3a": "2027 · Taipei", "r3b": "9 April: sunset 18:13, Arcturus rises 18:20",
        "ene": "ENE 68.5°", "east": "E", "horizon": "horizon",
        "c04_title": "Arcturus on the move", "c04_sub": "One Moon-width (0.52°) every 821 years · east left",
        "y150": "Ptolemy (c. AD 150)", "y2027": "today", "y3000": "AD 3000",
        "moon": "Moon 0.52°", "halley": "1718: Halley compared Greek catalogues — stars move",
        "右攝提": "η τ υ Boo",
        "c05_title": "Spring Triangle · Great Diamond", "c05_sub": "Arcturus + Spica + Denebola, then Cor Caroli",
        "tri": "Spring Triangle", "dia": "Great Diamond", "五帝座一": "Denebola", "常陳一": "Cor Caroli",
        "軒轅十四": "Regulus", "tri_note": "Sides {:.1f}° · {:.1f}° · {:.1f}°: nearly equilateral",
        "alt_note": "Dashed: some charts (and Stellarium) use Regulus instead of Denebola",
        "c05_r1": "Arcturus", "c05_r1b": "orange · brightest star north of the equator · 37 ly",
        "c05_r2": "Spica", "c05_r2b": "blue-white · ~250 ly",
        "c05_r3": "Denebola", "c05_r3b": "the Lion's tail · 36 ly",
        "c05_r4": "Cor Caroli", "c05_r4b": "Canes Venatici · 113 ly",
        "c05_how": "Dipper handle → big arc → Arcturus → Spica",
        "c06_title": "Look up tonight", "c06_sub": "Taipei · Friday 9 April 2027",
        "c06_w": "19:30  look WNW", "c06_w2": "thin crescent Moon, 13° up (too low after 19:45)",
        "c06_e": "21:00  look east", "c06_e2": "Dipper in the north-east; follow the arc",
        "c06_top": "Overhead, to the SW: Jupiter, Mars (planets — not in the triangle)",
        "N": "N", "NE": "NE", "E": "E", "SE": "SE", "W": "W", "NW": "NW",
        "月牙": "Moon", "北斗": "Dipper", "木星": "Jupiter", "火星": "Mars",
        "c07_title": "Two stars, rising together", "c07_sub": "9 April 2027 · eastern horizon",
        "hnl": "Honolulu", "hnl2": "Spica 19:01, Arcturus 19:02 — 1.3 min apart",
        "tpe": "Taipei", "tpe2": "Arcturus 18:20, Spica 18:28 — 8 min apart",
        "canoe": "Hōkūleʻa (Arcturus) and Hikianalia (Spica): the two voyaging canoes",
        "foot": "#WorldSkyCultures  #NTNUAstro",
        "src05": "Stellarium modern: Spring Triangle (Regulus), Great Diamond; distances Hipparcos 2007",
        "src06": "PyEphem (Taipei 25.03°N; refraction included)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 共用：天球幾何 ══════════════════════
def vec(ra, dec):
    r, d = math.radians(ra), math.radians(dec)
    return (math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def unit(a):
    n = math.sqrt(dot(a, a)); return tuple(x / n for x in a)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sep(a, b):
    return math.degrees(math.acos(max(-1, min(1, dot(vec(*S[a][:2]), vec(*S[b][:2]))))))


def aeqd(ra, dec, ra0, dec0):
    """方位等距投影（度）：x 往東為負（星圖方向，東在左）、y 往北為正"""
    v, c = vec(ra, dec), vec(ra0, dec0)
    rho = math.degrees(math.acos(max(-1, min(1, dot(v, c)))))
    e = unit(cross((0, 0, 1), c))           # 東
    n = cross(c, e)                          # 北
    th = math.atan2(dot(v, e), dot(v, n))
    return -rho * math.sin(th), rho * math.cos(th)


def circle_of(a, b, c):
    A, B, Cc = (vec(*S[h][:2]) for h in (a, b, c))
    cc = unit(cross(tuple(B[i] - A[i] for i in range(3)), tuple(Cc[i] - A[i] for i in range(3))))
    if dot(cc, A) < 0:
        cc = tuple(-x for x in cc)
    rho = math.degrees(math.acos(dot(cc, A)))
    ra = math.degrees(math.atan2(cc[1], cc[0])) % 360
    dec = math.degrees(math.asin(cc[2]))
    return ra, dec, rho, cc


def dist_off(cc, rho, h):
    return abs(math.degrees(math.acos(dot(cc, vec(*S[h][:2])))) - rho)


def star_size(v, k=1.0):
    return k * 22 * max(0.4, 6.0 - v) ** 1.8


def altaz(hip_or_radec, when, lat=TPE[0], lon=TPE[1], tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    ra, dec = S[hip_or_radec][:2] if isinstance(hip_or_radec, int) else hip_or_radec
    b = ephem.FixedBody(); b._ra, b._dec, b._epoch = math.radians(ra), math.radians(dec), ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def body_altaz(name, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(TPE[0]), str(TPE[1]); o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    b = getattr(ephem, name)(); b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


# ══════════════════════ C-X04-01 弧線是真的 ══════════════════════
ARC = {}


def c01_setup():
    ra, dec, rho, cc = circle_of(ALK, ARCTURUS, SPICA)
    ARC.update(ra=ra, dec=dec, rho=rho, cc=cc, sc=0.82 / (rho + 12))
    a3 = circle_of(ALI, MIZ, ALK)[2]
    ARC["handle_r"] = a3
    print(f"  C-X04-01：圓心 RA {ra:.1f} Dec {dec:+.1f}、半徑 {rho:.2f}°；開陽 {dist_off(cc, rho, MIZ):.2f}°、"
          f"玉衡 {dist_off(cc, rho, ALI):.2f}°；斗柄三顆的弧半徑 {a3:.1f}°")


def p01(h):
    x, y = aeqd(*S[h][:2], ARC["ra"], ARC["dec"])
    sc = ARC["sc"]
    return x * sc + 0.10, y * sc - 0.02


def c01_stars(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 34, WHITE)
    T(ax, 0.0, 0.85, tx("c01_sub").format(ARC["rho"]), 16, GREY, w="normal")
    for a, b in ((DUB, MER), (MER, PHE), (PHE, MEG), (MEG, DUB), (MEG, ALI), (ALI, MIZ), (MIZ, ALK)):
        (x1, y1), (x2, y2) = p01(a), p01(b)
        ax.plot([x1, x2], [y1, y2], c=WHITE, lw=1.6, alpha=.55, zorder=5)
    for h in DIPPER + [ARCTURUS, SPICA]:
        x, y = p01(h)
        col = AMBER if h == ARCTURUS else BLUE if h == SPICA else WHITE
        ax.scatter([x], [y], s=star_size(S[h][2]), c=col, zorder=8, lw=0)
    lab = {MIZ: ("開陽", -0.10, 0.012), ALK: ("搖光", -0.10, -0.012), ALI: ("玉衡", 0.02, 0.065),
           ARCTURUS: ("大角", 0.085, 0.0), SPICA: ("角宿一", 0.10, -0.01)}
    for h, (k, dx, dy) in lab.items():
        x, y = p01(h)
        col = AMBER if h == ARCTURUS else BLUE if h == SPICA else WHITE
        T(ax, x + dx, y + dy, tx(k), 20, col)


def c01_circle(ax):
    sc, rho = ARC["sc"], ARC["rho"]
    cx, cy = 0.10, -0.02
    th = [i * math.pi / 180 for i in range(361)]
    ax.plot([cx + rho * sc * math.cos(t) for t in th], [cy + rho * sc * math.sin(t) for t in th],
            c=AMBER, lw=1.4, alpha=.35, ls=(0, (5, 5)), zorder=3)
    # 實線：開陽→角宿一那一段
    (mx, my), (sx, sy) = p01(MIZ), p01(SPICA)
    t0, t1 = math.atan2(my - cy, mx - cx), math.atan2(sy - cy, sx - cx)
    if t1 < t0:
        t1 += 2 * math.pi
    if t1 - t0 > math.pi:
        t0, t1 = t1 - 2 * math.pi, t0
    ts = [t0 + (t1 - t0) * i / 200 for i in range(201)]
    ax.plot([cx + rho * sc * math.cos(t) for t in ts], [cy + rho * sc * math.sin(t) for t in ts],
            c=AMBER, lw=4.0, alpha=.9, zorder=4)
    ax.scatter([cx], [cy], s=40, c=GREY, zorder=6, lw=0)
    ax.plot([cx, sx], [cy, sy], c=GREY, lw=1.0, alpha=.5, ls=(0, (2, 3)))
    T(ax, (cx + sx) / 2 + 0.06, (cy + sy) / 2 + 0.02, f"{rho:.1f}°", 18, GREY, w="normal")
    T(ax, cx, cy - 0.05, tx("center"), 15, GREY, w="normal")


def c01_offset(ax):
    mx, my = p01(MIZ)
    ax.add_patch(C.Circle((mx, my), 0.032, fill=False, ec=AMBER, lw=2.0, zorder=9))
    T(ax, mx - 0.26, my + 0.17, tx("off_miz").format(dist_off(ARC["cc"], ARC["rho"], MIZ)), 18, AMBER)
    ax_, ay_ = p01(ALI)
    ax.add_patch(C.Circle((ax_, ay_), 0.032, fill=False, ec=GREY, lw=2.0, zorder=9))
    T(ax, ax_ + 0.30, ay_ + 0.17, tx("off_ali").format(dist_off(ARC["cc"], ARC["rho"], ALI)), 18, GREY)
    T(ax, 0.0, -0.90, tx("c01_foot").format(ARC["handle_r"]), 16, WHITE, w="normal", alpha=.85)


# ══════════════════════ C-X04-02 斗柄鐘面（面北：東在右） ══════════════════════
def c02_face(ax):
    T(ax, 0.0, 0.92, tx("c02_title"), 34, WHITE)
    T(ax, 0.0, 0.85, tx("c02_sub"), 17, GREY, w="normal")
    R = 0.56
    cy = -0.02
    th = [i * math.pi / 180 for i in range(361)]
    ax.plot([R * math.cos(t) for t in th], [cy + R * math.sin(t) for t in th], c=WHITE, lw=2.0, alpha=.5)
    for i in range(12):
        a = math.radians(90 - 30 * i)
        r0 = R - (0.06 if i % 3 == 0 else 0.03)
        ax.plot([r0 * math.cos(a), R * math.cos(a)], [cy + r0 * math.sin(a), cy + R * math.sin(a)],
                c=WHITE, lw=2.5 if i % 3 == 0 else 1.2, alpha=.6)
    ax.scatter([0], [cy], s=160, c=WHITE, zorder=8, lw=0)
    T(ax, 0.0, cy - 0.07, tx("pole"), 17, WHITE, w="normal")
    # 指針＝鐘心→搖光（三點鐘）；北斗畫在指針外側（搖光朝外的方向示意：斗身在搖光之上）
    hx, hy = R * 0.80, cy
    ax.plot([0, hx], [cy, hy], c=AMBER, lw=4.0, alpha=.9, zorder=7)
    # 北斗示意（相對位置取自盤上台北 4/9 黃昏）
    pts = DIP02
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)):
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=WHITE, lw=1.6, alpha=.7, zorder=6)
    for i, (x, y) in enumerate(pts):
        ax.scatter([x], [y], s=110 if i == 6 else 70, c=AMBER if i == 6 else WHITE, zorder=8, lw=0)
    T(ax, pts[6][0] + 0.01, pts[6][1] - 0.075, tx("hand"), 15, AMBER, w="normal")
    T(ax, 0.0, -0.93, tx("quote"), 19, WHITE, w="normal")


def c02_seasons(ax):
    R, cy = 0.56, -0.02
    pos = {"spring": (R + 0.21, cy, AMBER), "summer": (0.0, cy + R + 0.12, WHITE),
           "autumn": (-R - 0.21, cy, WHITE), "winter": (0.0, cy - R - 0.11, GREY)}
    for k, (x, y, col) in pos.items():
        T(ax, x, y, tx(k), 20, col)
    ax.plot([0, 0], [cy - 0.08, cy - R + 0.07], c=GREY, lw=2.0, ls=(0, (3, 3)), alpha=.8)
    T(ax, 0.0, cy - R - 0.22, tx("winter_note"), 14, GREY, w="normal")


DIP02 = []


def c02_setup():
    """台北 4/9 黃昏面北：搖光在鐘心正右方；北斗其他星依實際方位角差縮放"""
    when = "2027/4/9 18:37"
    pal, paz = altaz(POLARIS, when)
    pts = []
    for h in DIPPER:
        al, az = altaz(h, when)
        dx = ((az - paz + 180) % 360 - 180) * math.cos(math.radians((al + pal) / 2))
        pts.append((dx, al - pal))
    ax_, ay_ = pts[-1]
    s = 0.45 / math.hypot(ax_, ay_)
    ang = math.atan2(ay_, ax_)
    ca, sa = math.cos(-ang), math.sin(-ang)          # 把搖光轉到正右方（＝三點鐘）
    out = []
    for x, y in pts:
        X, Y = x * ca - y * sa, x * sa + y * ca
        out.append((X * s, -0.02 + Y * s))
    DIP02[:] = out
    print(f"  C-X04-02：台北 4/9 18:37 搖光相對北極星 方位差 {pts[-1][0]:+.1f}°、高度差 {pts[-1][1]:+.1f}°"
          f"（示意圖已轉正到三點鐘，旋轉 {math.degrees(ang):+.1f}°）")


# ══════════════════════ C-X04-03 赫西俄德的黃昏／C-X04-07 同時升起 ══════════════════════
def horizon_row(ax, y0, title, sub, items, col=WHITE, az0=30, az1=115):
    """一列東方地平線：items＝[(方位, 高度, 顏色, 標籤)]；x＝方位（北在左、南在右：面東）"""
    x0, x1 = -0.82, 0.82
    X = lambda az: x0 + (az - az0) / (az1 - az0) * (x1 - x0)
    ax.plot([x0, x1], [y0, y0], c=GREEN, lw=2.2, alpha=.8)
    for az, lb in ((45, "NE"), (90, "E")):
        if az0 <= az <= az1:
            ax.plot([X(az), X(az)], [y0, y0 - 0.02], c=GREEN, lw=1.5, alpha=.7)
            T(ax, X(az), y0 - 0.05, tx(lb), 14, GREEN, w="normal")
    T(ax, -0.84, y0 + 0.19, title, 20, col, ha="left")
    T(ax, -0.84, y0 + 0.125, sub, 16, WHITE, ha="left", w="normal", alpha=.9)
    for az, alt, c, lb in items:
        x, y = X(az), y0 + max(alt, 0.4) * 0.012
        ax.scatter([x], [y], s=150, c=c, zorder=8, lw=0)
        if lb:
            T(ax, x, y + 0.05, lb, 15, c)


def c03_r1(ax):
    T(ax, 0.0, 0.92, tx("c03_title"), 34, WHITE)
    T(ax, 0.0, 0.85, tx("c03_sub"), 17, GREY, w="normal")
    horizon_row(ax, 0.42, tx("r1a"), tx("r1b"), [(rise_az(34.8, 38.35), 0.5, AMBER, tx("大角") + f" {rise_az(34.8, 38.35):.0f}°")])


def c03_r2(ax):
    d = S[ARCTURUS][1] - 0.14              # 2027 年的赤緯（歲差＋自行，約 −0.14°）
    horizon_row(ax, -0.08, tx("r2a"), tx("r2b"), [(rise_az(d, 38.35), 0.5, AMBER, tx("大角") + f" {rise_az(d, 38.35):.0f}°")])


def c03_r3(ax):
    horizon_row(ax, -0.58, tx("r3a"), tx("r3b"), [(68.5, 0.5, AMBER, tx("大角") + "　" + tx("ene"))])


def c07_hnl(ax):
    T(ax, 0.0, 0.92, tx("c07_title"), 34, WHITE)
    T(ax, 0.0, 0.85, tx("c07_sub"), 17, GREY, w="normal")
    horizon_row(ax, 0.30, tx("hnl"), tx("hnl2"), [(69.3, 0.4, AMBER, tx("大角")), (101.9, 0.4, BLUE, tx("角宿一"))])


def c07_tpe(ax):
    a = altaz(ARCTURUS, "2027/4/9 18:28")
    horizon_row(ax, -0.32, tx("tpe"), tx("tpe2"), [(a[1], a[0], AMBER, tx("大角") + f" {a[0]:.0f}°"),
                                                   (101.9, 0.4, BLUE, tx("角宿一"))])
    T(ax, 0.0, -0.80, tx("canoe"), 15, WHITE, w="normal", alpha=.85)


def rise_az(dec, lat):
    """升起方位（幾何地平，度）"""
    return math.degrees(math.acos(math.sin(math.radians(dec)) / math.cos(math.radians(lat))))


# ══════════════════════ C-X04-04 大角在走路 ══════════════════════
PM = (-1093.39, -1999.40)          # mas/yr（μα*、μδ），Hipparcos 2007


def c04_xy(dra_cos, ddec):
    s = 0.105                       # 每度
    return -dra_cos * s, ddec * s - 0.05


def c04_stars(ax):
    T(ax, 0.0, 0.92, tx("c04_title"), 34, WHITE)
    T(ax, 0.0, 0.85, tx("c04_sub"), 17, GREY, w="normal")
    ra0, dec0 = S[ARCTURUS][:2]
    for h, (ra, dec, v) in S.items():
        if v > 5.6 or h == ARCTURUS:
            continue
        dx = (ra - ra0 + 180) % 360 - 180
        dx *= math.cos(math.radians(dec0))
        dy = dec - dec0
        if abs(dx) < 7.6 and abs(dy) < 6.5:
            x, y = c04_xy(dx, dy)
            ax.scatter([x], [y], s=star_size(v, .6), c=WHITE, alpha=.8, zorder=5, lw=0)
    x, y = c04_xy(0, 0)
    ax.scatter([x], [y], s=star_size(-0.05, .9), c=AMBER, zorder=8, lw=0)
    T(ax, x + 0.10, y + 0.06, tx("y2027"), 17, AMBER)
    # 右攝提三顆（大角西側，右邊）
    T(ax, 0.62, 0.0, tx("右攝提"), 14, GREY, w="normal")


def c04_track(ax):
    tot = math.hypot(*PM) / 3.6e6                      # 度/年
    ux, uy = PM[0] / math.hypot(*PM), PM[1] / math.hypot(*PM)
    pts = {}
    for yr in (150, 2027, 3000):
        d = (yr - 2000) * tot
        pts[yr] = c04_xy(ux * d, uy * d)
    xs = [pts[150][0], pts[3000][0]]; ys = [pts[150][1], pts[3000][1]]
    ax.annotate("", xy=(pts[3000][0], pts[3000][1]), xytext=(pts[150][0], pts[150][1]),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.4, alpha=.8, mutation_scale=22))
    for yr, k, dx, dy in ((150, "y150", 0.0, 0.07), (3000, "y3000", 0.0, -0.08)):
        x, y = pts[yr]
        ax.scatter([x], [y], s=120, facecolors="none", edgecolors=AMBER, lw=2.0, zorder=8)
        T(ax, x + dx, y + dy, tx(k), 16, AMBER)
    # 月亮直徑比例尺
    r = 0.26 * 0.105
    mx, my = -0.62, 0.55
    ax.add_patch(C.Circle((mx, my), r, fill=False, ec=WHITE, lw=2.0, alpha=.9))
    T(ax, mx + 0.06, my, tx("moon"), 15, WHITE, ha="left", w="normal")
    T(ax, 0.0, -0.86, tx("halley"), 17, WHITE, w="normal")
    print(f"  C-X04-04：自行 {tot * 3600:.2f}″/年 → 一個月亮寬 {0.52 / tot:.0f} 年；150→2027 移動 {(2027 - 150) * tot:.2f}°")


# ══════════════════════ C-X04-05 春季大三角＋大鑽石（9:16 圖卡） ══════════════════════
def c05_card(ax):
    ax.text(0.5, 0.947, tx("c05_title"), fontproperties=C.FP, fontsize=27, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.906, tx("c05_sub"), fontproperties=C.FP, fontsize=14, color=GREY, ha="center", va="center")
    hs = [ARCTURUS, SPICA, DENEBOLA, COR_CAROLI, REGULUS]
    ra0, dec0 = 185.0, 15.0
    P = {h: aeqd(*S[h][:2], ra0, dec0) for h in hs}
    sc = 0.0105
    cx, cy = 0.50, 0.62
    xy = {h: (cx + P[h][0] * sc, cy + P[h][1] * sc * 0.5625) for h in hs}
    L = lambda a, b, c, lw, ls, al: ax.plot([xy[a][0], xy[b][0]], [xy[a][1], xy[b][1]], c=c, lw=lw, ls=ls, alpha=al)
    for a, b in ((ARCTURUS, COR_CAROLI), (COR_CAROLI, DENEBOLA)):
        L(a, b, BLUE, 2.0, "-", .85)
    for a, b in ((ARCTURUS, SPICA), (SPICA, DENEBOLA), (DENEBOLA, ARCTURUS)):
        L(a, b, AMBER, 2.6, "-", .95)
    for a, b in ((SPICA, REGULUS), (REGULUS, ARCTURUS)):
        L(a, b, PURPLE, 1.5, (0, (4, 3)), .8)
    col = {ARCTURUS: AMBER, SPICA: BLUE, DENEBOLA: WHITE, COR_CAROLI: WHITE, REGULUS: PURPLE}
    nm = {ARCTURUS: "大角", SPICA: "角宿一", DENEBOLA: "五帝座一", COR_CAROLI: "常陳一", REGULUS: "軒轅十四"}
    off = {ARCTURUS: (-0.07, 0.0), SPICA: (0.0, -0.022), DENEBOLA: (0.08, 0.0), COR_CAROLI: (0.0, 0.022),
           REGULUS: (0.0, -0.022)}
    for h in hs:
        x, y = xy[h]
        ax.scatter([x], [y], s=star_size(S[h][2], .45), c=col[h], zorder=8, lw=0)
        T(ax, x + off[h][0], y + off[h][1], tx(nm[h]), 13, col[h])
    cxx = sum(xy[h][0] for h in (ARCTURUS, SPICA, DENEBOLA)) / 3
    cyy = sum(xy[h][1] for h in (ARCTURUS, SPICA, DENEBOLA)) / 3
    T(ax, cxx, cyy, tx("tri"), 13, AMBER)
    T(ax, (xy[ARCTURUS][0] + xy[COR_CAROLI][0] + xy[DENEBOLA][0]) / 3,
      (xy[ARCTURUS][1] + xy[COR_CAROLI][1] + xy[DENEBOLA][1]) / 3 + 0.012, tx("dia"), 13, BLUE)
    s1, s2, s3 = sep(ARCTURUS, SPICA), sep(SPICA, DENEBOLA), sep(DENEBOLA, ARCTURUS)
    y = 0.395
    ax.text(0.5, y, tx("tri_note").format(s1, s2, s3), fontproperties=C.FP, fontsize=12.5, color=AMBER,
            ha="center", va="center")
    ax.text(0.5, y - 0.03, tx("alt_note"), fontproperties=C.FP, fontsize=11, color=PURPLE, ha="center", va="center")
    ax.plot([0.05, 0.95], [y - 0.055, y - 0.055], c=WHITE, lw=0.8, alpha=.3)
    y -= 0.09
    for k, c in (("c05_r1", AMBER), ("c05_r2", BLUE), ("c05_r3", WHITE), ("c05_r4", WHITE)):
        ax.text(0.07, y, tx(k), fontproperties=C.FP, fontsize=14, color=c, ha="left", va="center", weight="bold")
        ax.text(0.30, y, tx(k + "b"), fontproperties=C.FP, fontsize=11.5, color=WHITE, ha="left", va="center", alpha=.9)
        y -= 0.045
    ax.text(0.5, y - 0.01, tx("c05_how"), fontproperties=C.FP, fontsize=13, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.058, tx("src05"), fontproperties=C.FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, tx("foot"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")
    print(f"  C-X04-05：三邊 {s1:.1f}／{s2:.1f}／{s3:.1f}°")


# ══════════════════════ C-X04-06 今晚抬頭看（9:16 圖卡） ══════════════════════
def panorama(ax, y0, h, az0, az1, items, ticks):
    """全景條：x＝方位、y＝高度（0–60°），地平線在 y0"""
    x0, x1 = 0.06, 0.94
    X = lambda az: x0 + ((az - az0) % 360) / ((az1 - az0) % 360) * (x1 - x0)
    Y = lambda alt: y0 + alt / 60.0 * h
    ax.plot([x0, x1], [y0, y0], c=GREEN, lw=2.0, alpha=.85)
    ax.add_patch(C.Rectangle((x0, y0 - 0.02), x1 - x0, 0.02, fc="#0E2A1A", ec="none", alpha=.9))
    for az, k in ticks:
        T(ax, X(az), y0 - 0.03, tx(k), 12, GREEN, w="normal")
    for it in items:
        if it[0] == "line":
            pts = [(X(az), Y(alt)) for az, alt in it[1]]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], c=it[2], lw=1.4, alpha=.8, zorder=6)
            continue
        az, alt, c, s, lb, dx, dy = it
        ax.scatter([X(az)], [Y(alt)], s=s, c=c, zorder=8, lw=0)
        if lb:
            T(ax, X(az) + dx, Y(alt) + dy, lb, 12.5, c)


def c06_card(ax):
    ax.text(0.5, 0.947, tx("c06_title"), fontproperties=C.FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.906, tx("c06_sub"), fontproperties=C.FP, fontsize=14, color=GREY, ha="center", va="center")
    # 19:30 往西北西
    ma, mz = body_altaz("Moon", "2027/4/9 19:30")
    ax.text(0.06, 0.855, tx("c06_w"), fontproperties=C.FP, fontsize=16, color=AMBER, ha="left", va="center",
            weight="bold")
    ax.text(0.06, 0.825, tx("c06_w2"), fontproperties=C.FP, fontsize=11.5, color=WHITE, ha="left", va="center")
    panorama(ax, 0.66, 0.14, 250, 340, [(mz, ma, WHITE, 120, tx("月牙") + f" {ma:.0f}°", 0.0, 0.022)],
             [(270, "W"), (315, "NW")])
    # 21:00 往東
    when = "2027/4/9 21:00"
    ax.text(0.06, 0.585, tx("c06_e"), fontproperties=C.FP, fontsize=16, color=AMBER, ha="left", va="center",
            weight="bold")
    ax.text(0.06, 0.555, tx("c06_e2"), fontproperties=C.FP, fontsize=11.5, color=WHITE, ha="left", va="center")
    dip = [altaz(h, when) for h in DIPPER]
    arc = [altaz(h, when) for h in (MIZ, ALK, ARCTURUS, SPICA)]
    aa, az_a = altaz(ARCTURUS, when)
    sa, az_s = altaz(SPICA, when)
    items = [("line", [(az, al) for al, az in [dip[0], dip[1], dip[2], dip[3], dip[0]]], WHITE),
             ("line", [(az, al) for al, az in dip[3:]], WHITE),
             ("line", [(az, al) for al, az in arc], AMBER)]
    items += [(az, al, WHITE, 30, "", 0, 0) for al, az in dip]
    items += [(az_a, aa, AMBER, 150, tx("大角") + f" {aa:.0f}°", 0.0, 0.025),
              (az_s, sa, BLUE, 110, tx("角宿一") + f" {sa:.0f}°", 0.0, -0.025)]
    nb = sum(az for al, az in dip) / 7, sum(al for al, az in dip) / 7
    items.append((nb[0], nb[1] + 9, WHITE, 0, tx("北斗"), 0.0, 0.0))
    panorama(ax, 0.30, 0.22, 330, 140, items, [(0, "N"), (45, "NE"), (90, "E"), (135, "SE")])
    # 頭頂的行星
    ja, jz = body_altaz("Jupiter", when)
    mra, mrz = body_altaz("Mars", when)
    ax.text(0.5, 0.215, tx("c06_top"), fontproperties=C.FP, fontsize=12, color=RED, ha="center", va="center")
    ax.text(0.5, 0.185, f"{tx('木星')} {ja:.0f}°／{jz:.0f}°　{tx('火星')} {mra:.0f}°／{mrz:.0f}°",
            fontproperties=C.FP, fontsize=11, color=WHITE, ha="center", va="center", alpha=.85)
    ax.text(0.5, 0.058, tx("src06"), fontproperties=C.FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, tx("foot"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")
    print(f"  C-X04-06：月 {ma:.1f}°／{mz:.1f}°；21:00 大角 {aa:.1f}°／{az_a:.1f}°、角宿一 {sa:.1f}°／{az_s:.1f}°；"
          f"木星 {ja:.1f}°／{jz:.1f}°、火星 {mra:.1f}°／{mrz:.1f}°")


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    c01_setup(); c02_setup()
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    C.emit("", [("星點", c01_stars), ("圓", c01_circle), ("偏差", c01_offset)], title="C-X04-01_弧線是真的")
    C.emit("", [("鐘面", c02_face), ("四季", c02_seasons)], title="C-X04-02_斗柄鐘面")
    C.emit("", [("前700", c03_r1), ("阿斯克拉2027", c03_r2), ("台北", c03_r3)], title="C-X04-03_赫西俄德的黃昏")
    C.emit("", [("星點", c04_stars), ("軌跡", c04_track)], title="C-X04-04_大角在走路")
    C.emit("", [("檀香山", c07_hnl), ("台北", c07_tpe)], title="C-X04-07_兩顆星同時升起")
    for fn, name in ((c05_card, "C-X04-05_春季大三角與大鑽石"), (c06_card, "C-X04-06_今晚抬頭看")):
        f, ax = C.newcard(dark=True)
        fn(ax)
        C.save(f, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
