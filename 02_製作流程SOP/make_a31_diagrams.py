# -*- coding: utf-8 -*-
"""A-31 卡米拉羅伊與尤瓦萊｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A31-01_地圖          → 02 鏡（澳洲層→標點層）
  C-A31-02_亮星與暗帶    → 04 鏡（亮星層→暗帶層）
  C-A31-03_鴯鶓曆        → 06–09 鏡（四五月／六到八月／八月底／十一十二月，各層獨立，一鏡一層）
  C-A31-04_bora場地      → 10 鏡（場地層→天空層）
  C-A31-05_同一塊黑      → 12 鏡（9:16 圖卡，可存圖）
  C-A31-06_這週抬頭看    → 15 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-31_卡米拉羅伊/_概念圖/（--lang en → _概念圖/en/，只出方形四組）

來源：Fuller, Anderson, Norris & Trudgett 2014（JAHH 17:171，鴯鶓曆；圖取當地晚上九點）；
      Fuller, Hamacher & Norris 2013（Australian Archaeology 77:30，68 處 bora，偏好朝南與西南）；
      Stellarium kamilaroi／boorong／bugis／tupi；Urton 1981（克丘亞，未親核）。
做法：鴯鶓的形狀一律用 make_a31_v4.py 自畫的暗帶多邊形（不描 Stellarium 插圖／多邊形：CC BY-NC-ND）；
      鴯鶓曆、這週抬頭看的姿勢＝把多邊形每個頂點用 PyEphem（含折射、J2000 星表座標）算地平座標，
      再以面向南方的立體投影畫出（地平線因此是弧線）。地圖＝手描示意海岸線（幾十個經緯度點），
      台灣用同一比例尺畫在澳洲西北外海做對照；bora 場地＝示意，不標任何真實場地、不臨摹已出版平面圖。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, BG, T
from matplotlib.patches import Polygon as MPoly, Ellipse, Circle, Wedge
import gen_ep_assets as G
import make_a31_v4 as A

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-31_卡米拉羅伊/_概念圖")
C.set_base(OUT)
RED, GREY, LAND = "#FF6B6B", "#7C8BA8", "#1E2A4A"
LANG = "zh"
S = None
GOOD = (-29.11, 147.45)

TXT = {
    "zh": {
        "c01_title": "卡米拉羅伊與尤瓦萊", "c01_sub": "澳洲・新南威爾斯北部（海岸線示意）",
        "nsw": "新南威爾斯", "sydney": "雪梨", "taiwan": "台灣（同比例）", "km": "500 公里",
        "zoom": "放大", "region": "卡米拉羅伊與尤瓦萊的家鄉", "Goodooga": "Goodooga",
        "Lightning Ridge": "Lightning Ridge", "Walgett": "Walgett",
        "c01_foot": "論文共同作者 Ghillar Michael Anderson：尤瓦萊長老（Goodooga）",
        "c02_title": "大多數星座連亮星；這隻鴯鶓由暗帶組成", "c02_l": "連亮星（例：天蠍、南十字）",
        "c02_r": "由暗帶組成：Gawarrgay", "sco": "天蠍", "cru": "南十字", "head": "頭＝煤袋",
        "c02_foot": "同一片天（南十字—天蠍—人馬），左右同比例；紫色＝本片自繪的暗帶示意",
        "c03_place": "Goodooga（29°S）晚上 {}・面向南方",
        "c03_1": "① 四、五月：在跑", "c03_1s": "整隻露出來，兩條腿都在地平線上",
        "c03_2": "② 六到八月：坐在巢上", "c03_2s": "腳看不見了；公鴯鶓孵蛋＝去撿蛋的時候",
        "c03_3": "③ 八月底：直立成兩顆蛋", "c03_3s": "頭＝小蛋、身體＝大蛋：小鴯鶓快孵出來了，別撿",
        "c03_4": "④ 十一月：坐在水坑裡", "c03_4s": "貼著地平線＝水坑滿了",
        "c03_5": "十二月：沉到地平線下＝地上的黑鴯鶓", "date1": "5/25 21:00", "date2": "7/1 21:00",
        "date3": "8/25 19:30", "date4": "11/15 21:00", "date5": "12/20",
        "E": "東", "SE": "東南", "S": "南", "SW": "西南", "W": "西",
        "c03_foot": "姿勢＝依 Fuller et al. 2014 與 Stellarium kamilaroi；位置 PyEphem 自算（AEST）",
        "headl": "頭", "legl": "腳", "egg_s": "小蛋（頭）", "egg_b": "大蛋（身體）",
        "c04_title": "bora：地上的兩個圓圈", "big": "大圈（公開）", "small": "小圈（只限受禮者與長老）",
        "path": "小徑：從大圈走向小圈", "fan": "68 處場地：方向多半朝南到西南",
        "fan2": "Fuller, Hamacher & Norris 2013", "sky": "八月傍晚：鴯鶓在南南西直立",
        "map_b": "身體 ↔ 大圈", "map_s": "頭 ↔ 小圈", "guess": "研究者推測（Fuller et al. 2014）",
        "c04_foot": "示意圖：不是任何真實場地", "N": "北",
    },
    "en": {
        "c01_title": "Kamilaroi and Euahlayi", "c01_sub": "Northern New South Wales, Australia (coast schematic)",
        "nsw": "New South Wales", "sydney": "Sydney", "taiwan": "Taiwan (same scale)", "km": "500 km",
        "zoom": "Zoom", "region": "Kamilaroi and Euahlayi Country", "Goodooga": "Goodooga",
        "Lightning Ridge": "Lightning Ridge", "Walgett": "Walgett",
        "c01_foot": "Co-author Ghillar Michael Anderson: Euahlayi Law Man, Goodooga",
        "c02_title": "Most constellations join bright stars; this emu is made of dark lanes",
        "c02_l": "Joining bright stars (Scorpius, Crux)", "c02_r": "Made of dark lanes: Gawarrgay",
        "sco": "Scorpius", "cru": "Crux", "head": "head = Coalsack",
        "c02_foot": "The same sky (Crux–Scorpius–Sagittarius) at the same scale; purple = our own sketch",
        "c03_place": "Goodooga (29°S), {} · facing south",
        "c03_1": "① April–May: running", "c03_1s": "the whole emu is up, both legs above the horizon",
        "c03_2": "② June–August: on the nest", "c03_2s": "no legs; the male sits on the eggs — time to collect them",
        "c03_3": "③ Late August: upright, two eggs", "c03_3s": "head = small egg, body = big egg: chicks hatching, stop",
        "c03_4": "④ November: in the waterhole", "c03_4s": "lying on the horizon = the waterholes are full",
        "c03_5": "December: below the horizon = the Black Emu on Earth", "date1": "25 May 21:00",
        "date2": "1 Jul 21:00", "date3": "25 Aug 19:30", "date4": "15 Nov 21:00", "date5": "20 Dec",
        "E": "E", "SE": "SE", "S": "S", "SW": "SW", "W": "W",
        "c03_foot": "Poses after Fuller et al. 2014 and Stellarium kamilaroi; positions computed (AEST)",
        "headl": "head", "legl": "legs", "egg_s": "small egg (head)", "egg_b": "big egg (body)",
        "c04_title": "Bora: two circles on the ground", "big": "large circle (public)",
        "small": "small circle (initiates and Elders only)", "path": "path from the large to the small circle",
        "fan": "68 grounds: mostly facing south to south-west", "fan2": "Fuller, Hamacher & Norris 2013",
        "sky": "August evening: the emu stands in the SSW", "map_b": "body ↔ large circle",
        "map_s": "head ↔ small circle", "guess": "a researchers' interpretation (Fuller et al. 2014)",
        "c04_foot": "Schematic — not any real site", "N": "N",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 共用：地平座標與立體投影 ══════════════════════
def altaz_fn(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)

    def f(ra, dec):
        b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
        b.compute(o)
        return math.degrees(b.alt), math.degrees(b.az)
    return f


def stereo(az0, alt0, sc, oy):
    def v(alt, az):
        a, z = math.radians(alt), math.radians(az)
        return (math.sin(z) * math.cos(a), math.cos(z) * math.cos(a), math.sin(a))
    c = v(alt0, az0)
    r = (c[1], -c[0], 0.0); n = math.hypot(r[0], r[1]); r = (r[0] / n, r[1] / n, 0.0)
    u = (r[1] * c[2] - 0.0, 0.0 - r[0] * c[2], r[0] * c[1] - r[1] * c[0])

    def P(alt, az):
        w = v(alt, az)
        k = 1.0 / (1.0 + sum(p * q for p, q in zip(w, c)))
        return sc * k * sum(p * q for p, q in zip(w, r)), oy + sc * k * sum(p * q for p, q in zip(w, u))
    return P


def sky_panel(ax, P, f, parts=("頭", "脖子", "身體", "腳"), faint=(), ground=True, az_rng=(80, 280),
              stars=True, xlim=(-1, 1), ylo=-1.0, dashed_below=False):
    """f(ra,dec)→(alt,az)；P(alt,az)→(x,y)。畫星、鴯鶓暗帶、地面、地平線"""
    if stars:
        for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 4.2 and S[h][1] < 10]:
            alt, az = f(ra, dec)
            if alt < -2:
                continue
            x, y = P(alt, az)
            if xlim[0] < x < xlim[1]:
                ax.scatter([x], [y], s=max(0.6, (4.6 - vm)) ** 1.8 * 3.0, c=WHITE, lw=0, zorder=4, alpha=.9)
    for key in parts:
        for poly in A.DARK[key]:
            q = [P(*f(ra, dec)) for ra, dec in poly[::2]]
            al = 0.16 if key in faint else 0.42
            ax.add_patch(MPoly(q, closed=True, fc=PURPLE, alpha=al, ec=PURPLE, lw=1.6 if key not in faint else 1.0,
                               ls="--" if key in faint else "-", zorder=5))
    hz = [P(0.0, az) for az in range(az_rng[0], az_rng[1] + 1)]
    if ground:
        g = hz + [(hz[-1][0], ylo), (hz[0][0], ylo)]
        ax.add_patch(MPoly(g, closed=True, fc=BG, ec="none", alpha=1.0, zorder=6))
    ax.plot([p[0] for p in hz], [p[1] for p in hz], c=GREEN, lw=2.2, alpha=.9, zorder=7)
    return hz


# ══════════════════════ C-A31-01 地圖 ══════════════════════
AUS = [(-10.7, 142.5), (-12.5, 143.3), (-14.0, 143.8), (-15.5, 145.3), (-17.0, 146.1), (-19.2, 146.9),
       (-20.0, 148.5), (-22.0, 149.8), (-23.5, 151.0), (-25.0, 152.6), (-26.5, 153.1), (-28.2, 153.6),
       (-30.0, 153.2), (-32.0, 152.5), (-33.8, 151.3), (-35.5, 150.4), (-37.5, 149.9), (-37.8, 148.0),
       (-38.5, 146.4), (-39.1, 146.3), (-38.3, 144.9), (-38.4, 144.0), (-38.8, 143.5), (-38.3, 141.5),
       (-38.0, 140.6), (-37.0, 139.7), (-35.6, 138.1), (-35.0, 138.5), (-34.2, 138.1), (-33.0, 137.8),
       (-34.9, 135.9), (-34.0, 135.2), (-32.5, 134.0), (-32.0, 132.5), (-31.6, 131.0), (-31.7, 129.0),
       (-32.3, 126.0), (-33.9, 123.6), (-33.9, 121.5), (-34.5, 119.5), (-35.0, 117.8), (-34.4, 115.3),
       (-33.5, 115.0), (-31.9, 115.8), (-30.0, 115.0), (-28.0, 114.2), (-26.0, 113.5), (-24.0, 113.5),
       (-22.0, 113.9), (-21.0, 115.5), (-20.3, 118.5), (-19.0, 121.3), (-17.5, 122.2), (-16.4, 123.0),
       (-15.0, 124.5), (-14.0, 126.0), (-14.9, 128.0), (-15.0, 129.5), (-13.5, 129.8), (-12.4, 130.8),
       (-11.3, 132.0), (-12.0, 133.8), (-12.2, 136.0), (-13.0, 136.6), (-14.8, 135.5), (-16.0, 136.8),
       (-17.5, 139.5), (-17.6, 140.8), (-16.5, 141.3), (-14.5, 141.6), (-12.5, 141.7)]
TAS = [(-40.8, 144.7), (-41.0, 146.6), (-40.9, 148.3), (-42.2, 148.3), (-43.6, 147.0), (-43.2, 145.9),
       (-41.8, 145.2)]
NSW = [(-28.17, 153.55), (-28.6, 152.0), (-28.9, 151.0), (-29.0, 149.0), (-29.0, 141.0), (-34.0, 141.0),
       (-35.0, 143.3), (-35.8, 144.9), (-36.0, 146.5), (-36.4, 148.1), (-37.5, 149.97)]
TAIWAN = [(25.3, 121.6), (24.9, 121.9), (24.5, 121.85), (23.5, 121.5), (22.75, 121.15), (21.9, 120.85),
          (22.3, 120.6), (22.6, 120.3), (23.0, 120.1), (23.5, 120.15), (24.2, 120.5), (24.8, 120.95), (25.1, 121.3)]
TOWNS = {"Goodooga": (-29.11, 147.45), "Lightning Ridge": (-29.43, 147.98), "Walgett": (-30.02, 148.12)}
LONC, LATC, SC = 134.0, -25.5, 0.040
COSL = math.cos(math.radians(26.0))


def mp(lat, lon):
    return (lon - LONC) * COSL * SC, (lat - LATC) * SC - 0.05


def km_deg():
    return 1.0 / 111.2


def c01_aus(ax):
    T(ax, 0.0, 0.90, tx("c01_title"), 32, WHITE)
    T(ax, 0.0, 0.82, tx("c01_sub"), 16, GREY, w="normal")
    for poly in (AUS, TAS):
        ax.add_patch(MPoly([mp(*p) for p in poly], closed=True, fc=LAND, ec=WHITE, lw=1.6, alpha=1.0, zorder=3))
    q = [mp(*p) for p in NSW]
    ax.plot([p[0] for p in q], [p[1] for p in q], c=GREY, lw=1.4, ls=(0, (4, 3)), zorder=4)
    x, y = mp(-32.3, 146.3)
    T(ax, x, y, tx("nsw"), 15, GREY, w="normal")
    x, y = mp(-33.87, 151.21)
    ax.scatter([x], [y], s=40, c=GREY, zorder=6)
    T(ax, x + 0.03, y - 0.035, tx("sydney"), 13, GREY, w="normal", ha="left")
    # 台灣：同比例，平移到澳洲西北外海
    dlat, dlon = -36.5, -5.0
    tw = [mp(la + dlat, lo + dlon) for la, lo in TAIWAN]
    ax.add_patch(MPoly(tw, closed=True, fc=AMBER, ec=AMBER, lw=1.2, alpha=.85, zorder=5))
    x, y = mp(-11.5, 116.0)
    T(ax, x, y + 0.11, tx("taiwan"), 15, AMBER)
    # 比例尺 500 km
    x0, y0 = mp(-41.5, 117.0)
    L = 500 * km_deg() * COSL * SC / COSL           # 經度方向 500 km（以 26°S 計）
    L = 500 / (111.2 * math.cos(math.radians(26.0))) * COSL * SC
    ax.plot([x0, x0 + L], [y0, y0], c=WHITE, lw=2.4, zorder=6)
    for xx in (x0, x0 + L):
        ax.plot([xx, xx], [y0 - 0.012, y0 + 0.012], c=WHITE, lw=2.0, zorder=6)
    T(ax, x0 + L / 2, y0 + 0.04, tx("km"), 13, WHITE, w="normal")


def c01_marks(ax):
    x, y = mp(*GOOD)
    ax.add_patch(Circle((x + 0.01, y - 0.005), 0.055, fc="none", ec=AMBER, lw=2.2, zorder=8))
    # 放大框（右上）
    bx, by, bw, bh = 0.30, 0.16, 0.66, 0.56
    ax.add_patch(C.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#10172E", ec=AMBER, lw=1.4, zorder=10))
    ax.plot([x + 0.06, bx], [y + 0.02, by + 0.05], c=AMBER, lw=1.0, alpha=.6, zorder=9)
    T(ax, bx + 0.03, by + bh - 0.045, tx("zoom"), 12, GREY, w="normal", ha="left", z=12)
    c0 = (-29.55, 147.85); k = 0.30
    mi = lambda la, lo: (bx + bw / 2 + (lo - c0[1]) * math.cos(math.radians(29.5)) * k,
                         by + bh / 2 + 0.04 + (la - c0[0]) * k)
    lab = {"Goodooga": (0.0, 0.055, "center"), "Lightning Ridge": (0.0, -0.05, "center"),
           "Walgett": (-0.03, 0.0, "right")}
    for nm, (la, lo) in TOWNS.items():
        px, py = mi(la, lo)
        ax.scatter([px], [py], s=90, c=AMBER, zorder=12)
        dx, dy, ha = lab[nm]
        T(ax, px + dx, py + dy, tx(nm), 15, WHITE, ha=ha, z=12)
    T(ax, bx + bw / 2, by + 0.05, tx("region"), 15, AMBER, z=12)
    T(ax, 0.0, -0.88, tx("c01_foot"), 15, WHITE, w="normal")


# ══════════════════════ C-A31-02 亮星與暗帶 ══════════════════════
SCO_W = [[78820, 78401, 78265], [78401, 80112, 80763, 81266, 82396, 82514, 82671, 84143, 86228, 87073, 86670,
                                  85927, 85696]]
CRU_W = [[61084, 60718], [62434, 59747]]


def _c02_proj(cx):
    m = _M()
    sc = 0.0096
    def P(ra, dec):
        x, y = A.disc_xy(m, ra, dec, ROT_UP)
        return cx + 0.07 + (x + 38.3) * sc, -0.05 + (y + 152.0) * sc
    return P


def _panel_stars(ax, P):
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 5.0 and S[h][1] < -5]:
        x, y = P(ra, dec)
        if -0.78 < y < 0.68 and abs(x - (P(240, -45)[0] - 0.07)) < 0.43:
            ax.scatter([x], [y], s=max(0.4, (5.2 - vm)) ** 1.8 * 2.2, c=WHITE, lw=0, zorder=4, alpha=.9)


def _panel_box(ax, cx):
    ax.add_patch(C.FancyBboxPatch((cx - 0.45, -0.80), 0.90, 1.50, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#0F1428", ec=GREY, lw=1.0, alpha=1.0, zorder=1))


def c02_bright(ax):
    T(ax, 0.0, 0.88, tx("c02_title"), 22, WHITE)
    cx = -0.48
    _panel_box(ax, cx)
    P = _c02_proj(cx)
    _panel_stars(ax, P)
    for segs, col in ((SCO_W, BLUE), (CRU_W, BLUE)):
        for seg in segs:
            q = [P(*S[h][:2]) for h in seg if h in S]
            ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=2.0, alpha=.9, zorder=5)
    x, y = P(*S[80763][:2]); T(ax, x + 0.02, y - 0.09, tx("sco"), 16, BLUE)
    x, y = P(*S[60718][:2]); T(ax, x - 0.15, y + 0.03, tx("cru"), 16, BLUE)
    T(ax, cx, 0.77, tx("c02_l"), 17, BLUE)


def c02_dark(ax):
    cx = 0.48
    _panel_box(ax, cx)
    P = _c02_proj(cx)
    pts = [P(ra, dec) for ra, dec, s in A.mw_dark_samples(26000)]
    pts = [p for p in pts if abs(p[0] - cx) < 0.44 and -0.79 < p[1] < 0.69]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=1.2, c=MW, alpha=.45, lw=0, zorder=3)
    _panel_stars(ax, P)
    for key in ("頭", "脖子", "身體", "腳"):
        for poly in A.DARK[key]:
            ax.add_patch(MPoly([P(*q) for q in poly[::2]], closed=True, fc=PURPLE, alpha=.40, ec=PURPLE, lw=1.6,
                               zorder=5))
    x, y = P(*A.COALSACK); T(ax, x + 0.20, y + 0.03, tx("head"), 15, PURPLE)
    T(ax, cx, 0.77, tx("c02_r"), 17, PURPLE)
    T(ax, 0.0, -0.88, tx("c02_foot"), 13, GREY, w="normal")


# ══════════════════════ C-A31-03 鴯鶓曆 ══════════════════════
CAL = {1: ("2027/5/25 21:00", "date1"), 2: ("2027/7/1 21:00", "date2"), 3: ("2027/8/25 19:30", "date3"),
       4: ("2027/11/15 21:00", "date4"), 5: ("2027/12/20 21:00", "date5")}
PC = stereo(180.0, 0.0, 0.90, -0.40)          # 投影中心在南方地平線上 → 地平線是直線


def cal_frame(ax, n, key_t, key_s, date_key):
    T(ax, 0.0, 0.90, tx(key_t), 28, AMBER)
    T(ax, 0.0, 0.82, tx(key_s), 16, WHITE, w="normal")
    T(ax, 0.0, -0.80, tx("c03_place").format(tx(date_key)), 15, GREY, w="normal")
    T(ax, 0.0, -0.90, tx("c03_foot"), 11, GREY, w="normal")
    for az, k in ((90, "E"), (135, "SE"), (180, "S"), (225, "SW"), (270, "W")):
        x, y = PC(0.0, az)
        ax.plot([x, x], [y, y - 0.025], c=GREEN, lw=1.6, zorder=8)
        T(ax, x, y - 0.06, tx(k), 14, GREEN, z=12)


def _f(n):
    return altaz_fn(*GOOD, 10, CAL[n][0])


def c03_1(ax):
    f = _f(1)
    sky_panel(ax, PC, f)
    cal_frame(ax, 1, "c03_1", "c03_1s", "date1")
    for (ra, dec), k, dx, dy in ((A.COALSACK, "headl", 0.06, 0.05), ((274.2, -49.1), "legl", -0.07, -0.02)):
        x, y = PC(*f(ra, dec)); T(ax, x + dx, y + dy, tx(k), 15, PURPLE)


def c03_2(ax):
    f = _f(2)
    sky_panel(ax, PC, f, faint=("腳",))
    cal_frame(ax, 2, "c03_2", "c03_2s", "date2")
    x, y = PC(*f(*A.COALSACK)); T(ax, x + 0.10, y, tx("headl"), 15, PURPLE)


def c03_3(ax):
    f = _f(3)
    sky_panel(ax, PC, f, faint=("腳",))
    cal_frame(ax, 3, "c03_3", "c03_3s", "date3")
    hx, hy = PC(*f(*A.COALSACK))
    bx, by = PC(*f(256.0, -36.0))
    ax.add_patch(Ellipse((hx, hy), 0.17, 0.12, fc="none", ec=AMBER, lw=2.2, ls="--", zorder=8))
    ax.add_patch(Ellipse((bx, by), 0.36, 0.24, fc="none", ec=AMBER, lw=2.2, ls="--", zorder=8))
    T(ax, hx + 0.24, hy, tx("egg_s"), 15, AMBER, ha="left" if hx < 0.4 else "right")
    T(ax, bx + 0.21, by + 0.05, tx("egg_b"), 15, AMBER, ha="left")


def c03_4(ax):
    f4, f5 = _f(4), _f(5)
    sky_panel(ax, PC, f4)
    # 十二月：沉下去的身體（虛線，畫在地面之上）
    for key in ("脖子", "身體", "腳"):
        for poly in A.DARK[key]:
            q = [PC(*f5(ra, dec)) for ra, dec in poly[::2]]
            ax.add_patch(MPoly(q, closed=True, fc="none", ec=PURPLE, lw=1.4, ls=(0, (3, 3)), alpha=.8, zorder=9))
    cal_frame(ax, 4, "c03_4", "c03_4s", "date4")
    x, y = PC(*f5(256.0, -36.0))
    T(ax, x, y - 0.13, tx("c03_5"), 15, PURPLE, z=12)
    T(ax, x, y - 0.20, f"（{tx('date5')}）", 13, GREY, w="normal", z=12)


# ══════════════════════ C-A31-04 bora 場地 ══════════════════════
PB = stereo(213.0, 0.0, 0.62, -0.10)
BORA_AZ = 213.0


def c04_site(ax):
    T(ax, 0.0, 0.92, tx("c04_title"), 28, WHITE)
    hz = [PB(0.0, az) for az in range(150, 277)]
    ax.plot([p[0] for p in hz], [p[1] for p in hz], c=GREEN, lw=2.0, alpha=.9, zorder=3)
    # 地面：透視示意（遠＝小圈在上、近＝大圈在下），「往上」＝方位 213°
    big = (0.0, -0.66); small = (0.0, -0.27)
    # 方向扇形：南（180°）到西南（225°）＝相對「往上」−33°…+12°
    ax.add_patch(Wedge(big, 0.55, 90 - 12, 90 + 33, fc=AMBER, alpha=.12, ec="none", zorder=2))
    T(ax, -0.42, -0.30, tx("fan"), 13, AMBER, w="normal")
    T(ax, -0.42, -0.36, tx("fan2"), 11, GREY, w="normal")
    ax.add_patch(Ellipse(big, 0.46, 0.15, fc="none", ec=WHITE, lw=3.0, zorder=5))
    ax.add_patch(Ellipse(small, 0.17, 0.055, fc="none", ec=WHITE, lw=3.0, zorder=5))
    ax.plot([0.0, 0.0], [big[1] + 0.075, small[1] - 0.0275], c=WHITE, lw=1.8, ls=(0, (2, 3)), zorder=5)
    T(ax, 0.30, big[1] - 0.06, tx("big"), 15, WHITE, ha="left")
    T(ax, 0.12, small[1], tx("small"), 14, WHITE, ha="left")
    T(ax, 0.06, (big[1] + small[1]) / 2, tx("path") + f"（{BORA_AZ:.0f}°）", 12, GREY, w="normal", ha="left")
    # 指北：方位 0° 相對「往上」順時針 −213° → 畫面角度 90+213
    cx, cy, r = 0.78, -0.75, 0.08
    a = math.radians(90 + BORA_AZ)
    ax.add_patch(Circle((cx, cy), r, fc="none", ec=GREY, lw=1.0, zorder=5))
    C.arrow(ax, (cx + r * math.cos(a), cy + r * math.sin(a)), (cx, cy), c=WHITE, lw=2.0, alpha=.9, style="-|>")
    T(ax, cx + 1.6 * r * math.cos(a), cy + 1.6 * r * math.sin(a), tx("N"), 13, WHITE)
    T(ax, 0.0, -0.93, tx("c04_foot"), 12, GREY, w="normal")


def c04_sky(ax):
    f = altaz_fn(*GOOD, 10, "2027/8/25 19:30")
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 3.6 and S[h][1] < 10]:
        alt, az = f(ra, dec)
        if alt > 1:
            x, y = PB(alt, az)
            if abs(x) < 0.95 and y < 0.84:
                ax.scatter([x], [y], s=max(0.6, (4.0 - vm)) ** 1.8 * 3.0, c=WHITE, lw=0, zorder=4, alpha=.85)
    for key in ("頭", "脖子", "身體", "腳"):
        for poly in A.DARK[key]:
            q = [PB(*f(ra, dec)) for ra, dec in poly[::2]]
            ax.add_patch(MPoly(q, closed=True, fc=PURPLE, alpha=.40 if key != "腳" else .15, ec=PURPLE,
                               lw=1.5, ls="-" if key != "腳" else "--", zorder=5))
    hx, hy = PB(*f(*A.COALSACK)); bx, by = PB(*f(256.0, -36.0))
    ax.add_patch(Ellipse((hx, hy), 0.13, 0.10, fc="none", ec=AMBER, lw=2.0, ls="--", zorder=7))
    ax.add_patch(Ellipse((bx, by), 0.30, 0.22, fc="none", ec=AMBER, lw=2.0, ls="--", zorder=7))
    ax.plot([hx, 0.0], [hy - 0.05, -0.27 + 0.03], c=AMBER, lw=1.4, ls=(0, (2, 3)), alpha=.8, zorder=6)
    ax.plot([bx - 0.1, -0.12], [by - 0.11, -0.66 + 0.07], c=AMBER, lw=1.4, ls=(0, (2, 3)), alpha=.8, zorder=6)
    T(ax, bx + 0.18, by + 0.02, tx("map_b"), 15, AMBER, ha="left")
    T(ax, hx + 0.10, hy + 0.01, tx("map_s"), 15, AMBER, ha="left")
    T(ax, 0.0, 0.83, tx("sky"), 16, PURPLE)
    T(ax, 0.55, 0.10, tx("guess"), 12, GREY, w="normal")


# ══════════════════════ 9:16 圖卡 ══════════════════════
ROWS5 = [  # (原文, 民族／地點, 看見什麼, 顏色)
    ("Gawarrgay", "卡米拉羅伊／尤瓦萊（澳洲新南威爾斯）", "鴯鶓的頭；脖子、身體、腳沿暗帶伸到人馬", PURPLE),
    ("Yarran", "卡米拉羅伊／尤瓦萊", "Yarran 樹的樹洞；南門二、馬腹一＝兩隻鸚鵡 Muraay", GREEN),
    ("Tchingal", "Boorong（澳洲維多利亞，1857 年的記錄）", "鴯鶓（「高個子」）", AMBER),
    ("Bembé'é", "布吉斯（印尼南蘇拉威西，水手）", "山羊", BLUE),
    ("Yutu", "克丘亞（祕魯安地斯）", "像鷓鴣的鳥（tinamou）", RED),
    ("Yacana", "克丘亞（祕魯安地斯）", "駱馬；眼睛＝南門二、馬腹一", RED),
]


def c05_card(ax):
    ax.text(0.5, 0.945, "同一塊黑", fontproperties=C.FP, fontsize=30, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.905, "南十字旁的煤袋：幾百光年外的塵埃雲", fontproperties=C.FP, fontsize=14, color=GREY,
            ha="center", va="center")
    # 小星圖：南十字＋煤袋＋南門二、馬腹一（ROT_UP 方向）
    m = _M()
    cx0, cy0 = -42.0, -108.0
    sc = 0.0125

    def P(ra, dec):
        x, y = A.disc_xy(m, ra, dec, ROT_UP)
        return 0.5 + (x - cx0) * sc * 1920 / 1080 * 0.5, 0.735 + (y - cy0) * sc * 0.5

    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 5.0 and -75 < S[h][1] < -45]:
        x, y = P(ra, dec)
        if 0.12 < x < 0.88 and 0.62 < y < 0.875:
            ax.scatter([x], [y], s=max(0.5, (5.2 - vm)) ** 1.8 * 1.6, c=WHITE, lw=0, zorder=4)
    from matplotlib.patches import Rectangle
    clip = Rectangle((0.03, 0.615), 0.94, 0.27, transform=ax.transData, fc="none", ec="none")
    ax.add_patch(clip)
    for poly in A.DARK["頭"] + A.DARK["脖子"]:
        q = [P(*p) for p in poly]
        pp = MPoly(q, closed=True, fc=PURPLE, alpha=.35, ec=PURPLE, lw=1.2, zorder=3)
        ax.add_patch(pp); pp.set_clip_path(clip)
    for seg in CRU_W:
        q = [P(*S[h][:2]) for h in seg]
        ax.plot([p[0] for p in q], [p[1] for p in q], c=WHITE, lw=1.0, alpha=.6, zorder=3)
    x, y = P(*A.COALSACK)
    ax.text(x + 0.10, y + 0.005, "煤袋", fontproperties=C.FP, fontsize=12, color=PURPLE, ha="left", va="center")
    x, y = P(*S[60718][:2])
    ax.text(x + 0.05, y + 0.012, "南十字", fontproperties=C.FP, fontsize=11, color=WHITE, ha="left", va="center")
    for hip, nm in ((71683, "南門二"), (68702, "馬腹一")):
        x, y = P(*S[hip][:2])
        ax.text(x - 0.03, y, nm, fontproperties=C.FP, fontsize=10.5, color=WHITE, ha="right", va="center")
    ax.plot([0.03, 0.97], [0.605, 0.605], c=WHITE, lw=1.0, alpha=.4)
    y = 0.595
    for nat, who, what, col in ROWS5:
        ax.text(0.04, y - 0.022, nat, fontproperties=C.FP, fontsize=15, color=col, ha="left", va="center",
                weight="bold")
        ax.text(0.96, y - 0.022, who, fontproperties=C.FP, fontsize=10.5, color=GREY, ha="right", va="center")
        ax.text(0.04, y - 0.054, what, fontproperties=C.FP, fontsize=12.5, color=WHITE, ha="left", va="center")
        y -= 0.068
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.text(0.5, y - 0.030, "同一段天的亮星版：瓜拉尼的美洲鴕 Guirá Nhandu", fontproperties=C.FP, fontsize=13,
            color=AMBER, ha="center", va="center", weight="bold")
    ax.text(0.5, y - 0.058, "（頭＝圍著煤袋的星，一路連到天蠍）", fontproperties=C.FP, fontsize=11.5, color=WHITE,
            ha="center", va="center")
    ax.text(0.5, 0.090, "Fuller et al. 2014；Stellarium kamilaroi／boorong／bugis／tupi", fontproperties=C.FP,
            fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.068, "Stanbridge 1857；Ammarell 1999；Urton 1981", fontproperties=C.FP, fontsize=10,
            color=GREY, ha="center", va="center")
    ax.text(0.5, 0.032, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE, ha="center",
            va="center")


def _card_sky(ax, y0, when, lat, lon, labels):
    """圖卡上的小天空（面向南、立體投影）：中心 x=0.5、地平線南點約在 y0"""
    f = altaz_fn(lat, lon, 8, when)
    P0 = stereo(180.0, 0.0, 1.0, 0.0)
    P = lambda alt, az: (0.5 + P0(alt, az)[0] * 0.44, y0 + P0(alt, az)[1] * 0.44 * 1080 / 1920)
    for h, (ra, dec, vm) in [(h, S[h][:3]) for h in S if S[h][2] < 4.0 and S[h][1] < 10]:
        alt, az = f(ra, dec)
        if alt > 0.5:
            x, y = P(alt, az)
            if 0.05 < x < 0.95 and y < y0 + 0.21:
                ax.scatter([x], [y], s=max(0.5, (4.2 - vm)) ** 1.8 * 1.4, c=WHITE, lw=0, zorder=4)
    for key in ("頭", "脖子", "身體", "腳"):
        for poly in A.DARK[key]:
            q = [P(*f(ra, dec)) for ra, dec in poly[::2]]
            ax.add_patch(MPoly(q, closed=True, fc=PURPLE, alpha=.42, ec=PURPLE, lw=1.2, zorder=5))
    hz = [P(0.0, az) for az in range(95, 266)]
    ax.add_patch(MPoly(hz + [(hz[-1][0], y0 - 0.07), (hz[0][0], y0 - 0.07)], closed=True, fc=BG, ec="none",
                       zorder=6))
    ax.plot([p[0] for p in hz], [p[1] for p in hz], c=GREEN, lw=1.6, zorder=7)
    for az, k in ((135, "東南"), (180, "南"), (225, "西南")):
        x, y = P(0.0, az)
        ax.text(x, y - 0.012, k, fontproperties=C.FP, fontsize=11, color=GREEN, ha="center", va="center", zorder=8)
    for (ra, dec), txt, dx, dy in labels:
        x, y = P(*f(ra, dec))
        ax.text(x + dx, y + dy, txt, fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center",
                zorder=8)


def c06_card(ax):
    ax.text(0.5, 0.950, "這週抬頭看：南方的鴯鶓", fontproperties=C.FP, fontsize=25, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.915, "2027/5/7（五）起　新月剛過，整晚沒有月光", fontproperties=C.FP, fontsize=13.5,
            color=AMBER, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.890, 0.890], c=WHITE, lw=1.0, alpha=.4)
    ax.text(0.04, 0.865, "南台灣海邊　23:00 前後　朝正南", fontproperties=C.FP, fontsize=15, color=AMBER,
            ha="left", va="center", weight="bold")
    _card_sky(ax, 0.625, "2027/5/7 23:00", *A.KT,
              [(A.COALSACK, "頭 4°", 0.02, 0.030), ((256.0, -36.0), "身體 12–16°", -0.02, 0.045)])
    ax.text(0.04, 0.535, "鴯鶓橫躺在海面上：頭在右（南南西），貼著海面幾乎看不見；", fontproperties=C.FP,
            fontsize=11.5, color=WHITE, ha="left", va="center")
    ax.text(0.04, 0.512, "身體往左上（東南）伸。地點：南方海平線開闊、沒有光害", fontproperties=C.FP,
            fontsize=11.5, color=WHITE, ha="left", va="center")
    ax.plot([0.03, 0.97], [0.488, 0.488], c=WHITE, lw=0.8, alpha=.3)
    ax.text(0.04, 0.463, "全台灣　01:00–03:00　朝南", fontproperties=C.FP, fontsize=15, color=AMBER,
            ha="left", va="center", weight="bold")
    _card_sky(ax, 0.225, "2027/5/8 02:00", *A.TPE,
              [((256.0, -36.0), "身體", 0.07, 0.0), (A.GAL_C, "銀河中心 35°", -0.10, 0.035)])
    ax.text(0.04, 0.133, "身體和腳爬到最高（台北：尾宿八 25–28°、銀河中心 31–36°）；", fontproperties=C.FP,
            fontsize=11.5, color=WHITE, ha="left", va="center")
    ax.text(0.04, 0.110, "頭（煤袋）已經沉下去了。天文晨光 03:50 前看", fontproperties=C.FP, fontsize=11.5,
            color=WHITE, ha="left", va="center")
    ax.text(0.5, 0.068, "高度：PyEphem 自算（含大氣折射）；紫色＝暗帶示意", fontproperties=C.FP, fontsize=10,
            color=GREY, ha="center", va="center")
    ax.text(0.5, 0.032, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE, ha="center",
            va="center")


# ══════════════════════ 主程式 ══════════════════════
_MM = {}
ROT_UP = None


def _M():
    if "m" not in _MM:
        from gen_master_canvas import Master
        _MM["m"] = Master("A-31", S, os.path.join(OUT, "_tmp"), lst=A.LST0, D_s=48, D_r=52, D_fill=-24.0,
                          w_c=34, feather=8, x_tN=0.0, x_tS=0.0, maglim=5.5)
        try:
            os.rmdir(os.path.join(OUT, "_tmp"))
        except OSError:
            pass
    return _MM["m"]


def check_calendar():
    """核對逐字稿「鴯鶓曆」表與「這週」數字（印出來比對）"""
    for n, (when, _) in CAL.items():
        f = altaz_fn(*GOOD, 10, when)
        row = [f(*A.COALSACK), f(*S[71683][:2]), f(240.0, -52.0), f(*S[86228][:2]), f(*A.GAL_C)]
        print(f"  Goodooga {when}: " + "　".join(f"{a:.1f}°/{z:.0f}°" for a, z in row))
    for when, ll in (("2027/5/7 23:00", A.KT), ("2027/5/8 01:00", A.TPE), ("2027/5/8 02:00", A.TPE),
                     ("2027/5/8 03:00", A.TPE)):
        f = altaz_fn(*ll, 8, when)
        print(f"  {ll} {when}: 煤袋 {f(*A.COALSACK)[0]:.1f}° 尾宿八 {f(*S[85927][:2])[0]:.1f}° 銀心 {f(*A.GAL_C)[0]:.1f}°")


def main():
    global S, LANG, ROT_UP
    S = dict(G.load_stars(BASE))
    ROT_UP = json_rot()
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    else:
        os.makedirs(OUT, exist_ok=True)
        check_calendar()
    C.emit("", [("澳洲", c01_aus), ("標點", c01_marks)], title="C-A31-01_地圖")
    C.emit("", [("亮星", c02_bright), ("暗帶", c02_dark)], title="C-A31-02_亮星與暗帶")
    C.emit("", [("四五月", c03_1)], title="C-A31-03_鴯鶓曆", preview_name="預覽-四五月")
    C.emit("", [("六到八月", c03_2)], title="C-A31-03_鴯鶓曆", preview_name="預覽-六到八月")
    C.emit("", [("八月底", c03_3)], title="C-A31-03_鴯鶓曆", preview_name="預覽-八月底")
    C.emit("", [("十一十二月", c03_4)], title="C-A31-03_鴯鶓曆", preview_name="預覽-十一十二月")
    C.emit("", [("場地", c04_site), ("天空", c04_sky)], title="C-A31-04_bora場地")
    if LANG != "zh":
        return
    f, ax = C.newcard(dark=True); c05_card(ax)
    C.save(f, "", "C-A31-05_同一塊黑_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True); c06_card(ax)
    C.save(f, "", "C-A31-06_這週抬頭看_圖卡.png", transparent=False)


def json_rot():
    import json
    p = os.path.join(BASE, "05_素材/A-31_卡米拉羅伊/_v4大畫布/A-31_標籤資料.json")
    return json.load(open(p, encoding="utf-8"))["rot"]["UP"]


if __name__ == "__main__":
    main()
