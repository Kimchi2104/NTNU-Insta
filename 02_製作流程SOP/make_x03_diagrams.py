# -*- coding: utf-8 -*-
"""X-03 北斗環球：一個勺子的十種人生｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-X03-01 三千年前不落下（孟斐斯層、長安層）→ 逐字稿 02 鏡：北斗在最低處（最南那顆星下中天）的樣子，
         前 1000 年（琥珀）整把都在地平線上；2027 年（灰虛線）沉到地平線下
C-X03-02 熊不下海洗澡（前750年層、2027年層）→ 05 鏡：雅典面北的海平線；前 750 年（荷馬）搖光最低 +12.3°，
         2027 年 −2.7°（尾巴尖沾到海面）
C-X03-03 赤道邊的北斗（地平線層、大蛇層）→ 09 鏡：Mitú（1.25°N）2027/9/1 黃昏 18:30（太陽 −12°）面北北西
C-X03-04 十種人生（9:16 圖卡；可存圖）→ 11b 鏡
C-X03-05 今晚抬頭看（9:16 圖卡；台北 2027/4/2 20:00、23:00＋開陽與輔放大框；可存圖）→ 12 鏡

計算：歲差用 PyEphem 把 J2000 座標換到該年代的分點（不計自行；北斗自行三千年約 5′）；
      01、02 的「最低高度」是幾何高度（不計折射），與逐字稿「星空對時」表同一套；
      03、05 的地平高度含大氣折射（1010 hPa、20°C）。
執行：/usr/bin/python3 make_x03_diagrams.py            （中文，輸出 05_素材/X-03_北斗環球/_概念圖/）
      /usr/bin/python3 make_x03_diagrams.py --lang en  （英文，輸出 _概念圖/en/）
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G
import matplotlib.patheffects as PE

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-03_北斗環球/_概念圖")
SC_NEW = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-master/skycultures")
CB.set_base(OUT)
RED, GREY, PANEL, GROUND = "#FF6B6B", "#7C8BA8", "#1B2240", "#141A30"
S = None
LANG = "zh"

DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID = 54061, 53910, 58001, 59774, 62956, 65378, 67301
ALCOR = 65477
DIPPER = [DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]
DSEG = [[DUBHE, MERAK, PHECDA, MEGREZ, DUBHE], [MEGREZ, ALIOTH, MIZAR, ALKAID]]
SITES = {"memphis": (29.85, 31.25), "changan": (34.3, 108.9), "athens": (38.0, 23.7)}
TPE = (25.0330, 121.5654, 8)
MITU = (1.25, -70.24, -5)

TXT = {
    "zh": {
        "c01_title": "三千年前，它一顆都不落下",
        "c01_sub": "北斗轉到最低的時候（最南那顆星在正北方下中天）",
        "memphis": "孟斐斯（埃及北部）", "changan": "長安（中國）",
        "lat": "北緯 {:.1f}°", "north": "正北",
        "bc1000": "前 1000 年：最低 {:+.1f}°", "y2027": "2027 年：最低 {:+.1f}°",
        "set_no": "整夜不落", "set_yes": "會落到地平線下",
        "c01_foot": "歲差：地軸指向慢慢改變，北斗離北天極愈來愈遠（PyEphem 自算，幾何高度）",
        "c02_title": "熊不下海洗澡", "c02_sub": "雅典（北緯 38.0°）面向北方的海平線",
        "c02_quote": "「只有它不分享大洋的沐浴」——荷馬《伊利亞德》18.489",
        "bc750": "前 750 年（荷馬）：搖光最低 {:+.1f}°", "now": "2027 年：搖光最低 {:+.1f}°",
        "c02_dip": "尾巴尖沾到海面", "alkaid": "搖光", "sea": "愛琴海",
        "c02_foot": "幾何高度（不計折射；加折射 2027 年約 −1.7°）；北斗在最低處的樣子",
        "c03_title": "赤道邊的北斗", "c03_sub": "亞馬遜 Tiquié 河一帶（以 Mitú 北緯 1.25° 計算）",
        "c03_when": "9 月 1 日黃昏 18:30（太陽在地平線下 12°）面向北北西",
        "nw": "西北", "nnw": "北北西", "n": "北",
        "c03_snake": "Sipé Phairó：吞魚的大蛇",
        "c03_note1": "大蛇的頭碰到地平線的那段日子，",
        "c03_note2": "河裡的魚幾乎都被它吞光",
        "c03_foot": "Stellarium tukano（Cardoso 2007、2016）；高度含大氣折射，PyEphem 自算",
        "天樞": "天樞", "天璇": "天璇", "天璣": "天璣", "天權": "天權", "玉衡": "玉衡", "開陽": "開陽", "搖光": "搖光",
        "c04_title": "一個勺子的十種人生", "c04_sub": "同一把北斗七星，世界各地看成什麼？",
        "outside": "十種之外",
        "c04_foot1": "Stellarium 各文化星空；荷馬《伊利亞德》18.487；《百道梵書》2.1.2.4；《史記・天官書》；MUL.APIN",
        "c04_foot2": "埃文基見 A-08、因紐特見 A-14、布吉斯見 A-26、曼達爾見 A-27",
        "tag": "#萬國星空　#師大天文社",
        "c05_title": "今晚抬頭看北斗", "c05_sub": "台北　2027/4/2（五）",
        "p20": "晚上 8 點　往東北方", "p23": "晚上 11 點　正北方高處",
        "ne": "東北", "e": "東", "nne": "北北東", "nnw2": "北北西", "nw2": "西北", "n2": "北",
        "zoom": "開陽與輔（放大）", "suha": "輔（al-Suhā）{:.1f} 等", "mizar": "開陽 {:.1f} 等",
        "sep": "相距 {:.1f}′：考考眼力",
        "l1": "從天黑到天亮（19:27–04:27）七顆都在 10° 以上",
        "l2": "8 點斗口在左上、斗柄在右下，天樞 {:.0f}°、搖光 {:.0f}°",
        "l3": "11 點前後升到北方最高處、整個倒掛（天樞 {:.0f}°）",
        "l4": "月亮 4/3 凌晨 {} 才升起，之前都沒有月光",
        "l5": "方位、高度、時刻：PyEphem 自算（含大氣折射）",
    },
    "en": {
        "c01_title": "3,000 years ago, not one star set",
        "c01_sub": "The Dipper at its lowest (southernmost star crossing due north, below the pole)",
        "memphis": "Memphis (northern Egypt)", "changan": "Chang'an (China)",
        "lat": "{:.1f}° N", "north": "N",
        "bc1000": "1000 BCE: lowest {:+.1f}°", "y2027": "2027: lowest {:+.1f}°",
        "set_no": "never sets", "set_yes": "dips below the horizon",
        "c01_foot": "Precession slowly moves the pole; the Dipper drifts away from it (PyEphem; geometric altitude)",
        "c02_title": "The Bear that never bathes", "c02_sub": "Athens (38.0° N), the sea horizon to the north",
        "c02_quote": "“alone has no share in the baths of Ocean” — Homer, Iliad 18.489",
        "bc750": "750 BCE (Homer): Alkaid lowest {:+.1f}°", "now": "2027: Alkaid lowest {:+.1f}°",
        "c02_dip": "the tail tip touches the sea", "alkaid": "Alkaid", "sea": "Aegean",
        "c02_foot": "Geometric altitude (with refraction 2027 ≈ −1.7°); the Dipper at its lowest",
        "c03_title": "The Dipper at the equator", "c03_sub": "Tiquié River, Amazon (computed for Mitú, 1.25° N)",
        "c03_when": "1 Sept, dusk 18:30 (Sun 12° below horizon), facing NNW",
        "nw": "NW", "nnw": "NNW", "n": "N",
        "c03_snake": "Sipé Phairó: the fish-swallowing snake",
        "c03_note1": "In the days when the snake's head touches the horizon,",
        "c03_note2": "it swallows almost all the fish in the river",
        "c03_foot": "Stellarium tukano (Cardoso 2007, 2016); altitudes with refraction, PyEphem",
        "天樞": "Dubhe", "天璇": "Merak", "天璣": "Phecda", "天權": "Megrez", "玉衡": "Alioth", "開陽": "Mizar",
        "搖光": "Alkaid",
        "c04_title": "Ten lives of one ladle", "c04_sub": "The same seven stars — what does the world see?",
        "outside": "Beyond the ten",
        "c04_foot1": "Stellarium sky cultures; Homer Il. 18.487; Śatapatha Brāhmaṇa 2.1.2.4; Shiji; MUL.APIN",
        "c04_foot2": "Evenki: A-08 · Inuit: A-14 · Bugis: A-26 · Mandar: A-27",
        "tag": "#WorldSkyCultures  #NTNUAstro",
        "c05_title": "Find the Dipper tonight", "c05_sub": "Taipei · Fri 2 Apr 2027",
        "p20": "8 pm · facing northeast", "p23": "11 pm · high in the north",
        "ne": "NE", "e": "E", "nne": "NNE", "nnw2": "NNW", "nw2": "NW", "n2": "N",
        "zoom": "Mizar and Alcor (zoom)", "suha": "Alcor (al-Suhā) mag {:.1f}", "mizar": "Mizar mag {:.1f}",
        "sep": "{:.1f}′ apart: an eye test",
        "l1": "All seven stay above 10° from dark to dawn (19:27–04:27)",
        "l2": "8 pm: bowl upper left, handle lower right; Dubhe {:.0f}°, Alkaid {:.0f}°",
        "l3": "Around 11 pm: highest in the north, upside down (Dubhe {:.0f}°)",
        "l4": "The Moon rises at {} on 3 Apr — no moonlight before then",
        "l5": "Directions, altitudes and times: PyEphem (with refraction)",
    },
}
# 十種＋十種之外（原文, 文化, 意思, 顏色）
TEN = {
    "zh": [("① 牛的前腿", [("Meskhetyu", "古埃及", "牛的前腿")], RED),
           ("② 車", [("Karlvagn", "北歐", "男人的車"), ("Іллёў воз", "白俄羅斯", "以利亞的車"),
                    ("帝車", "中國", "天帝的車"), ("MUL.MAR.GÍD.DA", "巴比倫", "車"),
                    ("Pědati Suung", "峇里", "空馬車")], BLUE),
           ("③ 熊", [("Ἄρκτος", "希臘（荷馬）", "熊，也叫車"), ("ṛkṣa", "印度（梵文）", "熊")], PURPLE),
           ("④ 七個人", [("Saptarṣi", "印度", "七位仙人"), ("Долоон өвгөн", "蒙古", "七位老人"),
                       ("Seven Brothers", "黑腳族", "七兄弟和小妹")], GREEN),
           ("⑤ 棺架", [("بنات نعش", "阿拉伯", "大棺架的女兒們")], AMBER),
           ("⑥ 強盜", [("арамии", "馬其頓", "一夥強盜")], RED),
           ("⑦ 大蛇", [("Sipé Phairó", "圖卡諾（亞馬遜）", "吞魚的大蛇")], GREEN),
           ("⑧ 船", [("bintoéng kappala'é", "布吉斯（蘇拉威西）", "木造帆船")], AMBER),
           ("⑨ 漁網", [("Bittoéng Panjala", "曼達爾（蘇拉威西）", "漁網星")], BLUE),
           ("⑩ 獵物", [("Хэглэн／Манги", "埃文基（西伯利亞）", "駝鹿的腳／獵人"),
                      ("Tukturjuit", "因紐特", "馴鹿")], PURPLE)],
    "en": [("① Bull's foreleg", [("Meskhetyu", "Ancient Egypt", "foreleg of the bull")], RED),
           ("② Cart", [("Karlvagn", "Norse", "the man's cart"), ("Іллёў воз", "Belarus", "Elijah's cart"),
                       ("帝車", "China", "the Emperor's chariot"), ("MUL.MAR.GÍD.DA", "Babylon", "wagon"),
                       ("Pědati Suung", "Bali", "an empty horse cart")], BLUE),
           ("③ Bear", [("Ἄρκτος", "Greece (Homer)", "bear, also the Wagon"), ("ṛkṣa", "India (Sanskrit)", "bear")],
            PURPLE),
           ("④ Seven people", [("Saptarṣi", "India", "seven sages"), ("Долоон өвгөн", "Mongolia", "seven old men"),
                               ("Seven Brothers", "Blackfoot", "seven brothers and their sister")], GREEN),
           ("⑤ Bier", [("بنات نعش", "Arabia", "daughters of the great bier")], AMBER),
           ("⑥ Robbers", [("арамии", "Macedonia", "a band of robbers")], RED),
           ("⑦ Great snake", [("Sipé Phairó", "Tukano (Amazon)", "fish-swallowing snake")], GREEN),
           ("⑧ Ship", [("bintoéng kappala'é", "Bugis (Sulawesi)", "wooden sailing ship")], AMBER),
           ("⑨ Fishing net", [("Bittoéng Panjala", "Mandar (Sulawesi)", "fishing-net star")], BLUE),
           ("⑩ Prey", [("Хэглэн／Манги", "Evenki (Siberia)", "elk's legs / hunter"),
                       ("Tukturjuit", "Inuit", "caribou")], PURPLE)],
}
OUTSIDE = {
    "zh": ["英國：the Plough 犁", "峇里：Larung Paglangan 把骨灰撒進海裡（天權到搖光）",
           "洛科諾：Anorhâkoya 鷺鷥的靈", "塞里（墨西哥）：Cohamc 女人們與丈夫",
           "薩米：Fávdna 的弓", "納瓦荷：Náhookǫs bikąʼii 旋轉的男人", "夏威夷：Nā Hiku 七"],
    "en": ["Britain: the Plough", "Bali: Larung Paglangan, scattering ashes at sea (Megrez–Alkaid)",
           "Lokono: Anorhâkoya, spirit of the heron", "Seri (Mexico): Cohamc, the women and the husband",
           "Sámi: Fávdna's bow", "Navajo: Náhookǫs bikąʼii, Revolving Male", "Hawaiʻi: Nā Hiku, the Seven"],
}


def tx(k):
    return TXT[LANG][k]


def ctext(ax, x, y, s, size, col, w="bold", ha="center", z=9, va="center", alpha=1.0, halo=False):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=col, ha=ha, va=va, weight=w,
            zorder=z, alpha=alpha, linespacing=1.25,
            path_effects=[PE.withStroke(linewidth=4, foreground=CB.BG)] if halo else None)


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3, alpha=1.0):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))


def star_r(v, k=1.0):
    return max(2.0, (5.6 - v) ** 2.2 * 2.6 * k)


# ───────── 天文計算 ─────────
def radec_at(h, year):
    """J2000 → 該年代分點（PyEphem 歲差；不計自行）"""
    import ephem
    ra, dec = S[h][:2]
    e = ephem.Equatorial(math.radians(ra), math.radians(dec), epoch=ephem.J2000)
    q = ephem.Equatorial(e, epoch=f"{year}/1/1")
    return math.degrees(float(q.ra)), math.degrees(float(q.dec))


def altaz_geo(ra, dec, lst, lat):
    """幾何地平座標（不計折射）：回 (alt, az)，az 北＝0、東＝90"""
    H, d, p = map(math.radians, ((lst - ra) % 360, dec, lat))
    sa = math.sin(d) * math.sin(p) + math.cos(d) * math.cos(p) * math.cos(H)
    alt = math.asin(sa)
    y = -math.cos(d) * math.sin(H)
    x = math.sin(d) * math.cos(p) - math.cos(d) * math.sin(p) * math.cos(H)
    return math.degrees(alt), math.degrees(math.atan2(y, x)) % 360


def lowest_pose(year, lat):
    """北斗最南那顆星下中天的時刻（LST＝RA+180），回各星 (alt, az) 與最低高度"""
    co = {h: radec_at(h, year) for h in DIPPER}
    low = min(DIPPER, key=lambda h: co[h][1])
    lst = (co[low][0] + 180.0) % 360
    pose = {h: altaz_geo(*co[h], lst, lat) for h in DIPPER}
    return pose, low, lat - (90.0 - co[low][1])


def observer(lat, lon, tz, local):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure = 1010; o.temp = 20
    o.date = ephem.Date(ephem.Date(local) - tz * ephem.hour)
    return o


def altaz_now(h, site, local):
    import ephem
    o = observer(*site, local)
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(S[h][0]), math.radians(S[h][1]); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(float(b.alt)), math.degrees(float(b.az))


def signed_az(az):
    return (az + 180.0) % 360 - 180.0


def draw_dipper(ax, pts, col, lw=2.6, ls="-", alpha=1.0, dots=True, z=7):
    for seg in DSEG:
        for a, b in zip(seg, seg[1:]):
            ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=col, lw=lw, ls=ls, alpha=alpha, zorder=z)
    if dots:
        for h in DIPPER:
            ax.scatter([pts[h][0]], [pts[h][1]], s=star_r(S[h][2], 1.4), c=WHITE if ls == "-" else GREY,
                       zorder=z + 1, lw=0, alpha=alpha)


# ══════════════════ C-X03-01 三千年前不落下 ══════════════════
LOG = {}


def c01_panel(ax, key, y0, show_title):
    lat = SITES[key][0]
    sc_, yh = 0.015, y0                        # 1° ＝ 0.015 單位；yh＝地平線
    if show_title:
        ctext(ax, 0.0, 0.93, tx("c01_title"), 30, WHITE)
        ctext(ax, 0.0, 0.865, tx("c01_sub"), 15, GREY, w="normal")
    box(ax, -0.95, yh - 0.17, 1.9, 0.80, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ax.add_patch(CB.Rectangle((-0.95, yh - 0.17), 1.9, 0.17, fc=GROUND, ec="none", zorder=2))
    ax.plot([-0.95, 0.95], [yh, yh], c=WHITE, lw=1.6, alpha=.85, zorder=6)
    ctext(ax, 0.0, yh - 0.035, tx("north"), 13, WHITE, w="normal", z=9)
    ctext(ax, -0.91, yh + 0.58, tx(key), 18, AMBER, ha="left")
    ctext(ax, -0.91, yh + 0.525, tx("lat").format(lat), 13, GREY, w="normal", ha="left")
    # 北天極（前 1000 年與今天的高度都＝緯度）
    ax.scatter([0], [yh + lat * sc_], s=40, marker="+", c=GREY, zorder=5)
    out = {}
    for year, col, ls, xo in ((-1000, AMBER, "-", -0.42), (2027, GREY, (0, (4, 3)), 0.42)):
        pose, low, lmin = lowest_pose(year, lat)
        pts = {h: (xo + signed_az(az) * sc_ * 1.0, yh + alt * sc_) for h, (alt, az) in pose.items()}
        # 以搖光（最低星）為中心水平放：左右兩組並排
        dx = xo - pts[low][0]
        pts = {h: (x + dx, y) for h, (x, y) in pts.items()}
        draw_dipper(ax, pts, col, ls=ls, lw=2.4 if ls == "-" else 1.8)
        lab = tx("bc1000" if year < 0 else "y2027").format(lmin)
        ly = yh + (0.58 if year < 0 else 0.525)
        ctext(ax, 0.91, ly, lab + "　" + tx("set_no" if lmin > 0 else "set_yes"), 13,
              AMBER if year < 0 else WHITE, ha="right", z=9)
        out[year] = lmin
    LOG[key] = out


def c01_memphis(ax):
    c01_panel(ax, "memphis", 0.12, True)


def c01_changan(ax):
    c01_panel(ax, "changan", -0.73, False)
    ctext(ax, 0.0, -0.955, tx("c01_foot"), 11.5, GREY, w="normal")


# ══════════════════ C-X03-02 熊不下海洗澡 ══════════════════
def c02_base(ax):
    ctext(ax, 0.0, 0.92, tx("c02_title"), 32, WHITE)
    ctext(ax, 0.0, 0.855, tx("c02_sub"), 15, GREY, w="normal")
    ctext(ax, 0.0, 0.79, tx("c02_quote"), 14, PURPLE, w="normal")
    yh = -0.35
    ax.add_patch(CB.Rectangle((-0.95, -0.80), 1.9, yh + 0.80, fc="#10284A", ec="none", zorder=2, alpha=.9))
    CB.water(ax, y=yh - 0.03, x0=-0.95, x1=0.95, c=BLUE, rows=3, amp=0.012, freq=26)
    ax.plot([-0.95, 0.95], [yh, yh], c=WHITE, lw=1.6, alpha=.85, zorder=6)
    ctext(ax, 0.0, -0.70, tx("sea"), 14, BLUE, w="normal", z=9)
    ctext(ax, 0.0, yh - 0.20, tx("north"), 13, WHITE, w="normal", z=9)
    ctext(ax, 0.0, -0.93, tx("c02_foot"), 11.5, GREY, w="normal")
    return yh


def c02_pose(year, yh):
    pose, low, lmin = lowest_pose(year, SITES["athens"][0])
    sc_ = 0.022
    return {h: (signed_az(az) * sc_, yh + alt * sc_) for h, (alt, az) in pose.items()}, lmin


def c02_old(ax):
    yh = c02_base(ax)
    pts, lmin = c02_pose(-750, yh)
    draw_dipper(ax, pts, PURPLE, lw=3.0)
    x, y = pts[ALKAID]
    ctext(ax, x + 0.05, y - 0.01, tx("alkaid"), 14, PURPLE, ha="left", z=10)
    ctext(ax, -0.9, 0.66, tx("bc750").format(lmin), 15, PURPLE, ha="left")
    LOG["athens"] = {-750: lmin}


def c02_now(ax):
    yh = -0.35
    pts, lmin = c02_pose(2027, yh)
    draw_dipper(ax, pts, AMBER, lw=2.4, ls=(0, (4, 3)))
    x, y = pts[ALKAID]
    ax.add_patch(CB.Circle((x, y), 0.06, fc="none", ec=RED, lw=2.0, zorder=9))
    ctext(ax, x + 0.08, y - 0.02, tx("c02_dip"), 14, RED, ha="left", z=10, halo=True)
    ctext(ax, -0.9, 0.60, tx("now").format(lmin), 15, AMBER, ha="left")
    LOG.setdefault("athens", {})[2027] = lmin


# ══════════════════ C-X03-03 赤道邊的北斗 ══════════════════
C03_WHEN = "2027/9/1 18:30"
AZ0, AZ1, ALT1 = 296.0, 352.0, 34.0


def c03_q(alt, az):
    x = -0.86 + (az - AZ0) / (AZ1 - AZ0) * 1.72
    return x, -0.30 + alt / ALT1 * 0.95


def c03_horizon(ax):
    ctext(ax, 0.0, 0.92, tx("c03_title"), 32, WHITE)
    ctext(ax, 0.0, 0.855, tx("c03_sub"), 15, GREY, w="normal")
    ctext(ax, 0.0, 0.80, tx("c03_when"), 14, AMBER, w="normal")
    y0 = -0.30
    for alt in (10, 20, 30):
        _, y = c03_q(alt, AZ0)
        ax.plot([-0.86, 0.86], [y, y], c=WHITE, lw=0.6, alpha=.18, ls=(0, (3, 4)), zorder=2)
        ctext(ax, -0.88, y, f"{alt}°", 10, GREY, w="normal", ha="right")
    # 河岸樹林剪影＋河面
    import numpy as np
    xs = np.linspace(-0.95, 0.95, 400)
    rng = np.random.RandomState(7)
    tops = y0 + 0.012 + 0.03 * np.abs(np.sin(xs * 23)) * rng.uniform(0.4, 1.0, xs.size) + 0.01 * np.sin(xs * 61)
    ax.fill_between(xs, y0 - 0.07, tops, color="#0A0F1E", zorder=4)
    ax.add_patch(CB.Rectangle((-0.95, -0.62), 1.9, y0 - 0.07 + 0.62, fc="#10284A", ec="none", zorder=3, alpha=.9))
    CB.water(ax, y=y0 - 0.12, x0=-0.95, x1=0.95, c=BLUE, rows=3, amp=0.010, freq=30)
    ax.plot([-0.95, 0.95], [y0, y0], c=WHITE, lw=1.4, alpha=.8, zorder=6)
    for az, k in ((315, "nw"), (337.5, "nnw")):
        x, _ = c03_q(0, az)
        ctext(ax, x, -0.68, tx(k), 13, WHITE, w="normal")
    ctext(ax, 0.0, -0.93, tx("c03_foot"), 11.5, GREY, w="normal")


def c03_snake(ax):
    pos = {}
    for h in DIPPER:
        alt, az = altaz_now(h, MITU, C03_WHEN)
        pos[h] = (alt, az)
    LOG["mitu"] = pos
    pts = {h: c03_q(*pos[h]) for h in DIPPER}
    segs = [[DUBHE, MERAK, PHECDA, MEGREZ, ALIOTH, MIZAR, ALKAID]]      # tukano 011 的連法
    for seg in segs:
        for a, b in zip(seg, seg[1:]):
            ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=GREEN, lw=3.0, alpha=.95, zorder=7)
    for h in DIPPER:
        alt = pos[h][0]
        ax.scatter([pts[h][0]], [pts[h][1]], s=star_r(S[h][2], 1.6), c=WHITE, zorder=8, lw=0,
                   alpha=1.0 if alt > 0 else 0.45)
    names = {DUBHE: "天樞", MERAK: "天璇", PHECDA: "天璣", MEGREZ: "天權", ALKAID: "搖光"}
    offs = {DUBHE: (0.04, -0.06), MERAK: (-0.04, -0.06), PHECDA: (-0.05, 0.03), MEGREZ: (0.05, 0.02),
            ALKAID: (0.05, 0.0)}
    for h, nm in names.items():
        x, y = pts[h]
        dx, dy = offs[h]
        ctext(ax, x + dx, y + dy, f"{tx(nm)} {pos[h][0]:+.1f}°", 12, WHITE, ha="left" if dx > 0 else "right",
              z=10, halo=True, w="normal")
    ctext(ax, 0.0, 0.70, tx("c03_snake"), 18, GREEN)
    ctext(ax, 0.0, 0.64, tx("c03_note1"), 13, WHITE, w="normal")
    ctext(ax, 0.0, 0.595, tx("c03_note2"), 13, WHITE, w="normal")


# ══════════════════ C-X03-04 十種人生（圖卡） ══════════════════
def c04_card(ax):
    ctext(ax, 0.5, 0.962, tx("c04_title"), 28, WHITE)
    ctext(ax, 0.5, 0.932, tx("c04_sub"), 12, GREY, w="normal")
    y = 0.893
    for head, rows, col in TEN[LANG]:
        ctext(ax, 0.05, y, head, 13, col, ha="left")
        for orig, cul, mean in rows:
            ctext(ax, 0.29, y, orig, 10.5, col, ha="left", w="normal")
            ctext(ax, 0.555, y, cul, 10, WHITE, ha="left", w="normal")
            ctext(ax, 0.78, y, mean, 10, WHITE, ha="left", w="normal")
            y -= 0.0255
        ax.plot([0.05, 0.95], [y + 0.0115, y + 0.0115], c=col, lw=0.8, alpha=.35)
        y -= 0.0125
    y -= 0.004
    ctext(ax, 0.05, y, tx("outside"), 12, GREY, ha="left")
    y -= 0.026
    for s_ in OUTSIDE[LANG]:
        ctext(ax, 0.07, y, s_, 9.5, GREY, ha="left", w="normal")
        y -= 0.0205
    LOG["c04_bottom"] = y
    ctext(ax, 0.5, 0.058, tx("c04_foot1"), 7.6, GREY, w="normal")
    ctext(ax, 0.5, 0.040, tx("c04_foot2"), 7.6, GREY, w="normal")
    ctext(ax, 0.5, 0.016, tx("tag"), 11.5, WHITE, w="normal")


# ══════════════════ C-X03-05 今晚抬頭看（圖卡） ══════════════════
def sky_panel(ax, y0, y1, az0, az1, alt1, when, title, dirs):
    xa, xb = 0.08, 0.92

    def q(alt, az):
        a = (az - az0) % 360
        return xa + a / ((az1 - az0) % 360) * (xb - xa), y0 + alt / alt1 * (y1 - y0)
    box(ax, 0.04, y0 - 0.05, 0.92, (y1 - y0) + 0.085, ec=GREY, fc="#0E1428", lw=1.0, z=1)
    ctext(ax, 0.07, y1 + 0.012, title, 13, AMBER, ha="left", z=10)
    ax.plot([xa, xb], [y0, y0], c=WHITE, lw=1.5, alpha=.8, zorder=5)
    for az, k in dirs:
        x, _ = q(0, az)
        ctext(ax, x, y0 - 0.02, tx(k), 10.5, WHITE, w="normal", z=12)
    for alt in (20, 40, 60):
        if alt < alt1:
            _, y = q(alt, az0)
            ax.plot([xa, xb], [y, y], c=WHITE, lw=0.6, alpha=.18, ls=(0, (3, 4)), zorder=2)
            ax.text(xa - 0.005, y, f"{alt}°", fontproperties=CB.FP, fontsize=8, color=GREY, zorder=3,
                    ha="right", va="center")
    pos, pts = {}, {}
    for h in DIPPER + [ALCOR]:
        pos[h] = altaz_now(h, TPE[:2] + (8,), when)
        pts[h] = q(*pos[h])
    for seg in DSEG:
        for a, b in zip(seg, seg[1:]):
            ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=WHITE, lw=1.4, alpha=.55, zorder=6)
    for h in DIPPER:
        ax.scatter([pts[h][0]], [pts[h][1]], s=star_r(S[h][2], 1.2), c=WHITE, zorder=7, lw=0)
    for h, nm, dx in ((DUBHE, "天樞", -0.025), (ALKAID, "搖光", 0.025)):
        x, y = pts[h]
        ctext(ax, x + dx, y, f"{tx(nm)} {pos[h][0]:.0f}°", 10.5, WHITE, ha="right" if dx < 0 else "left",
              w="normal", z=10, halo=True)
    x, y = pts[MIZAR]
    ax.scatter([x], [y], s=260, facecolors="none", edgecolors=AMBER, linewidths=1.4, zorder=8)
    return pos, pts[MIZAR]


def c05_card(ax):
    import ephem
    ctext(ax, 0.5, 0.962, tx("c05_title"), 30, WHITE)
    ctext(ax, 0.5, 0.930, tx("c05_sub"), 13, GREY, w="normal")
    p20, m20 = sky_panel(ax, 0.69, 0.865, 345.0, 90.0, 62.0, "2027/4/2 20:00", tx("p20"),
                         [(0, "n2"), (22.5, "nne"), (45, "ne"), (90, "e")])
    p23, m23 = sky_panel(ax, 0.40, 0.575, 315.0, 60.0, 72.0, "2027/4/2 23:00", tx("p23"),
                         [(315, "nw2"), (337.5, "nnw2"), (0, "n2"), (22.5, "nne"), (45, "ne")])
    # 開陽＋輔 放大框
    bx, by, bw, bh = 0.20, 0.17, 0.60, 0.15
    box(ax, bx, by, bw, bh, ec=AMBER, fc="#0E1428", lw=1.2, z=3)
    ctext(ax, 0.5, by + bh - 0.016, tx("zoom"), 11, AMBER, z=10)
    sep = math.degrees(math.acos(min(1.0, sum(a * b for a, b in zip(
        *[(math.cos(math.radians(S[h][1])) * math.cos(math.radians(S[h][0])),
           math.cos(math.radians(S[h][1])) * math.sin(math.radians(S[h][0])),
           math.sin(math.radians(S[h][1]))) for h in (MIZAR, ALCOR)]))))) * 60
    # 23:00 面北的方向：輔在開陽的哪一邊（照 23:00 高度方位換算）
    (am, zm), (aa, za) = p23[MIZAR], p23[ALCOR]
    vx = (za - zm) * math.cos(math.radians(am)); vy = aa - am
    n = math.hypot(vx, vy)
    cx, cy, L = 0.43, by + 0.095, 0.085
    ax_, ay_ = cx + vx / n * L, cy + vy / n * L * 9 / 16          # 圖卡 9:16：y 方向換算成等比例
    ax.scatter([cx], [cy], s=star_r(S[MIZAR][2], 2.2), c=WHITE, zorder=8, lw=0)
    ax.scatter([ax_], [ay_], s=star_r(S[ALCOR][2], 2.6), c=WHITE, zorder=8, lw=0)
    ctext(ax, cx - 0.025, cy - 0.022, tx("mizar").format(S[MIZAR][2]), 9.5, WHITE, ha="right", w="normal", z=10)
    ctext(ax, ax_ + 0.025, ay_, tx("suha").format(S[ALCOR][2]), 9.5, AMBER, ha="left", w="normal", z=10)
    ctext(ax, 0.5, by + 0.014, tx("sep").format(sep), 10, WHITE, w="normal", z=10)
    o = observer(*TPE, "2027/4/2 20:00")
    mr = ephem.Date(o.next_rising(ephem.Moon()) + 8 * ephem.hour).tuple()
    lines = [(tx("l1"), WHITE), (tx("l2").format(p20[DUBHE][0], p20[ALKAID][0]), WHITE),
             (tx("l3").format(p23[DUBHE][0]), WHITE), (tx("l4").format(f"{mr[3]}:{mr[4]:02d}"), WHITE),
             (tx("l5"), GREY)]
    for i, (s, col) in enumerate(lines):
        ctext(ax, 0.5, 0.145 - i * 0.025, s, 10.5 if col != GREY else 8.5, col, w="normal")
    ctext(ax, 0.5, 0.016, tx("tag"), 11.5, WHITE, w="normal")
    LOG["tonight"] = dict(p20=p20, p23=p23, moonrise=mr, sep=sep)


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print(f"── C-X03 概念圖（{LANG}）──")
    CB.emit("", [("孟斐斯", c01_memphis), ("長安", c01_changan)], title="C-X03-01_三千年前不落下")
    CB.emit("", [("前750年", c02_old), ("2027年", c02_now)], title="C-X03-02_熊不下海洗澡")
    CB.emit("", [("地平線", c03_horizon), ("大蛇", c03_snake)], title="C-X03-03_赤道邊的北斗")
    for name, fn in [("C-X03-04_十種人生", c04_card), ("C-X03-05_今晚抬頭看", c05_card)]:
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)
    print("  · 最低高度：" + "；".join(f"{k} {v}" for k, v in LOG.items() if k in ("memphis", "changan", "athens")))
    print("  · Mitú 9/1 18:30：" + "、".join(f"{h} {a:+.1f}°/{z:.0f}°" for h, (a, z) in LOG["mitu"].items()))
    t = LOG["tonight"]
    print(f"  · 台北 20:00 天樞 {t['p20'][DUBHE][0]:.1f}°、搖光 {t['p20'][ALKAID][0]:.1f}°；23:00 天樞 "
          f"{t['p23'][DUBHE][0]:.1f}°；月出 {t['moonrise']}；開陽—輔 {t['sep']:.1f}′；圖卡 04 底 y={LOG['c04_bottom']:.3f}")


if __name__ == "__main__":
    main()
