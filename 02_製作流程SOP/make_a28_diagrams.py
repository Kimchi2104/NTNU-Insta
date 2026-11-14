# -*- coding: utf-8 -*-
"""A-28 印度：月亮的 27 位妻子｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A28-02_二十七位妻子        → 03 鏡「妻子」層；04 鏡「回娘家」層（獨立一張，不與「妻子」疊）
  C-A28-03_盈虧                → 05 鏡「消瘦」；06 鏡「消瘦」＋「盈虧」（上下分區，可疊）
  C-A28-04_Somnāth在哪         → 07 鏡「印度」＋「古吉拉特」
  C-A28-05_33到27              → 08 鏡「三十三」；09 鏡「二十七」（各自獨立一張）
  C-A28-06_月亮與Rohiṇī的距離  → 11b 鏡（單層）
  C-A28-07_十二個月名          → 14 鏡（9:16 圖卡，可存圖）
  C-A28-08_起點搬家            → 15 鏡「春分點」＋「起點」
  C-A28-09_兩條黃道            → 16 鏡「兩尺」＋「十二宮」
  C-A28-10_今晚抬頭看          → 17 鏡（9:16 圖卡，可存圖）
  （C-A28-01 恆星黃道 27 格做成星圖層，見 make_a28_v4.py「恆星黃道27格」＋「27宿門牌」）
輸出：05_素材/A-28_印度/_概念圖/（--lang en → _概念圖/en/）

來源：《泰帝利耶本集》2.3.5（33 個女兒、Soma 王、rājayakṣma）；《摩訶婆羅多・沙利耶篇》（Ganguli 譯 9.35：
      Dakṣa 27 個女兒、Prabhāsa 沐浴）；《薄伽梵往世書》6.6.2、6.6.23；《濕婆往世書》Koṭirudra Saṃhitā 14。
      地圖：Natural Earth 1:110m（公有領域；07_資料來源/地圖/南亞陸地_naturalearth_110m.json），只畫陸地不畫國界。
      距離、天象：PyEphem 4.2.1 自算（地心；台北 25.033°N、121.565°E）。
      恆星黃道：Lahiri 近似＝角宿一當日黃經 − 180°；歲差 50.29″／年。
版權：不臨摹任何已出版的圖；Somnath 神廟照片由美宣另尋授權。
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Circle, Polygon, Wedge, FancyBboxPatch
import gen_ep_assets as G
from matplotlib.font_manager import FontProperties
# Noto Sans CJK 的 ś（U+015B）重音位置錯（看起來像 s＋r 上的重音）→ 拉丁字先用 DejaVu Sans，漢字逐字退回 Noto CJK
C.FP = FontProperties(family=["DejaVu Sans", C.FP.get_family()[0]])

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-28_印度/_概念圖")
C.set_base(OUT)
RED, GREY, DIM, LAND = "#FF6B6B", "#7C8BA8", "#3A4560", "#2E3D5C"
MOON = "#F4F1E6"
LANG = "zh"
TXT = {
    "zh": {
        "c02_title": "月神 Soma 的二十七位妻子", "c02_sub": "Dakṣa 的女兒＝天上的二十七個月站",
        "soma": "Soma", "rohini": "Rohiṇī", "rohini2": "紅色的那位（畢宿五）",
        "c02b_title": "偏心的丈夫", "c02b_1": "其他二十六位：回娘家告狀",
        "c02b_2": "Dakṣa：「一視同仁！」", "c02b_3": "Soma 照樣偏心 → 岳父詛咒：消瘦病",
        "c03_title": "一天比一天瘦", "c03_1": "眾神求情：平等對待每一位妻子，",
        "c03_2": "再去海邊的聖地 Prabhāsa 沐浴",
        "c03_wane": "半個月消瘦", "c03_wax": "半個月復原", "c03_c1": "月亮的盈虧", "c03_c2": "約 29.5 天一輪",
        "c03_foot": "後來的《濕婆往世書》改說：是濕婆救了他",
        "c04_title": "Somnāth：「月神之主」", "c04_sub": "印度西岸・古吉拉特（只畫陸地，不畫國界）",
        "india": "印度次大陸", "arab": "阿拉伯海", "bay": "孟加拉灣",
        "som": "Somnāth（Prabhas Patan）", "som2": "傳說的 Prabhāsa 海邊",
        "guj": "古吉拉特", "map_src": "地圖：Natural Earth（公有領域）",
        "c05_title": "最早的版本：三十三個女兒", "c05_src": "《泰帝利耶本集》2.3.5",
        "c05_1": "嫁女兒的是生主 Prajāpati", "c05_2": "Soma 是一位王，違背誓言",
        "c05_3": "rājayakṣma＝「國王的消瘦病」",
        "c05b_title": "後來的史詩：二十七個女兒", "c05b_src": "《摩訶婆羅多》・往世書",
        "c05b_1": "Dakṣa 的女兒 ＝ 天上的二十七個月站", "c05b_2": "33 → 27",
        "c06_title": "月亮離 Rohiṇī（畢宿五）多近？", "c06_sub": "每年最接近的一次（地心角距，PyEphem 自算）",
        "c06_y": "最近距離（度）", "c06_occ": "＜1.3°：地球上某處看得到掩星",
        "c06_last": "2018：上次擋住", "c06_next": "2033：下次", "c06_now": "2027：隔 9.6°",
        "c06_r": "Rohiṇī 畢宿五", "c06_j": "Jyeṣṭhā 心宿二",
        "c06_foot": "月亮的路 18.6 年擺一輪", "c06_a": "（2015–2018 一整輪）",
        "c07_title": "十二個月名＝十二位妻子", "c07_sub": "滿月住哪一家，就用她的名字當月名",
        "c07_h1": "月名", "c07_h2": "來自哪一宿", "c07_h3": "約當",
        "c07_now": "2027/4/21 滿月在 Citrā → 現在是 Caitra 月",
        "c07_f1": "原則是該月滿月落在（或靠近）那一宿；實際曆法以《印度天文曆》為準",
        "c08_title": "第一位妻子換人了", "c08_sub": "星空不動，春分點沿黃道往西挪（歲差，約 72 年 1°）",
        "c08_east": "← 東", "c08_west": "西 →",
        "c08_v1": "約前 2300 年", "c08_v2": "約公元 300 年", "c08_v3": "今天",
        "c08_vp": "春分點", "c08_s1": "最早：從 Kṛttikā（昴宿）排起", "c08_s2": "後來：從 Aśvinī（婁宿）排起",
        "c08_s3": "有一種說法：起點跟著春分點走",
        "c09_title": "兩條黃道", "c09_trop": "回歸黃道：春分點＝0°（西洋占星）",
        "c09_sid": "恆星黃道：Citrā（角宿一）＝180°（印度宗教曆）",
        "c09_diff": "差 24.2°（2027）＝歲差", "c09_vp": "春分點", "c09_spica": "Citrā 180°",
        "c09_sun": "4/10 的太陽", "c09_sun2": "西洋：白羊座　印度：雙魚座（退後一格）",
        "c09_foot": "兩套都是約定，不是誰算錯",
        "signs": ["白羊", "金牛", "雙子", "巨蟹", "獅子", "處女", "天秤", "天蠍", "人馬", "摩羯", "寶瓶", "雙魚"],
        "c10_title": "今晚八點抬頭看", "c10_sub": "2027/4/16（五）20:00・台北・頭頂在圓心",
        "N": "北", "S": "南", "E": "東", "W": "西",
        "moon": "月亮（78%）", "reg": "軒轅十四 Maghā", "mars": "火星", "jup": "木星",
        "ald": "畢宿五 Rohiṇī", "ald2": "西 19°，20:40 前看", "arc": "大角 Svātī", "spi": "角宿一 Citrā",
        "ple": "昴宿 Kṛttikā", "c10_n1": "月亮離軒轅十四 1.7°：用手遮住月亮再找",
        "c10_n2": "心宿二 Jyeṣṭhā 21:38 才升起", "c10_tag": "#萬國星空　#師大天文社",
    },
    "en": {
        "c02_title": "The 27 wives of Soma, the Moon", "c02_sub": "Dakṣa's daughters = the 27 lunar mansions",
        "soma": "Soma", "rohini": "Rohiṇī", "rohini2": "the Red One (Aldebaran)",
        "c02b_title": "A partial husband", "c02b_1": "The other 26 went home to complain",
        "c02b_2": "Dakṣa: “Treat them all alike!”", "c02b_3": "Soma didn't → cursed with a wasting disease",
        "c03_title": "Thinner every day", "c03_1": "The gods pleaded: treat every wife equally,",
        "c03_2": "then bathe at Prabhāsa by the sea",
        "c03_wane": "half a month waning", "c03_wax": "half a month waxing", "c03_c1": "phases of the Moon",
        "c03_c2": "about 29.5 days", "c03_foot": "The later Śiva Purāṇa: Śiva saved him",
        "c04_title": "Somnāth: “Lord of the Moon”", "c04_sub": "West coast of India, Gujarat (land only, no borders)",
        "india": "Indian subcontinent", "arab": "Arabian Sea", "bay": "Bay of Bengal",
        "som": "Somnāth (Prabhas Patan)", "som2": "the Prabhāsa shore of the legend",
        "guj": "Gujarat", "map_src": "Map: Natural Earth (public domain)",
        "c05_title": "The oldest version: 33 daughters", "c05_src": "Taittirīya Saṃhitā 2.3.5",
        "c05_1": "The father is Prajāpati", "c05_2": "Soma is a king who broke his oath",
        "c05_3": "rājayakṣma = “the king's consumption”",
        "c05b_title": "The later epic: 27 daughters", "c05b_src": "Mahābhārata, Purāṇas",
        "c05b_1": "Dakṣa's daughters = the 27 lunar mansions", "c05b_2": "33 → 27",
        "c06_title": "How close does the Moon get to Rohiṇī?", "c06_sub": "Closest pass each year (geocentric, PyEphem)",
        "c06_y": "closest distance (°)", "c06_occ": "< 1.3°: occulted somewhere on Earth",
        "c06_last": "2018: last occultation", "c06_next": "2033: the next", "c06_now": "2027: 9.6° away",
        "c06_r": "Rohiṇī (Aldebaran)", "c06_j": "Jyeṣṭhā (Antares)",
        "c06_foot": "The Moon's path swings over 18.6 years", "c06_a": "(a full series 2015–2018)",
        "c07_title": "Twelve months, twelve wives", "c07_sub": "Each month is named for the mansion of its full moon",
        "c07_h1": "Month", "c07_h2": "from the mansion", "c07_h3": "about",
        "c07_now": "Full moon 21 Apr 2027 is in Citrā → this is Caitra",
        "c07_f1": "Rule of thumb; the official calendar is the Indian Astronomical Ephemeris",
        "c08_title": "The first wife changed", "c08_sub": "The stars stay; the equinox slides west (precession, ~1° per 72 years)",
        "c08_east": "← east", "c08_west": "west →",
        "c08_v1": "c. 2300 BCE", "c08_v2": "c. 300 CE", "c08_v3": "today",
        "c08_vp": "equinox", "c08_s1": "Oldest lists start at Kṛttikā (Pleiades)", "c08_s2": "Later lists start at Aśvinī",
        "c08_s3": "One view: the start followed the equinox",
        "c09_title": "Two zodiacs", "c09_trop": "Tropical: equinox = 0° (Western astrology)",
        "c09_sid": "Sidereal: Citrā (Spica) = 180° (Indian religious calendar)",
        "c09_diff": "24.2° apart (2027) = precession", "c09_vp": "equinox", "c09_spica": "Citrā 180°",
        "c09_sun": "Sun on 10 April", "c09_sun2": "Western: Aries · Indian: Pisces (one sign back)",
        "c09_foot": "Both are conventions; neither is a mistake",
        "signs": ["Ari", "Tau", "Gem", "Cnc", "Leo", "Vir", "Lib", "Sco", "Sgr", "Cap", "Aqr", "Psc"],
        "c10_title": "Look up tonight at 8", "c10_sub": "Fri 16 Apr 2027, 20:00, Taipei; zenith at centre",
        "N": "N", "S": "S", "E": "E", "W": "W",
        "moon": "Moon (78%)", "reg": "Regulus · Maghā", "mars": "Mars", "jup": "Jupiter",
        "ald": "Aldebaran · Rohiṇī", "ald2": "19° in the west; before 20:40", "arc": "Arcturus · Svātī",
        "spi": "Spica · Citrā", "ple": "Pleiades · Kṛttikā",
        "c10_n1": "Moon 1.7° from Regulus: block the Moon with your hand",
        "c10_n2": "Antares (Jyeṣṭhā) rises only at 21:38", "c10_tag": "#WorldSkyCultures",
    },
}
MONTHS = [("Caitra", "Citrā", "角", "3–4 月"), ("Vaiśākha", "Viśākhā", "氐", "4–5 月"),
          ("Jyaiṣṭha", "Jyeṣṭhā", "心", "5–6 月"), ("Āṣāḍha", "Āṣāḍhā", "箕・斗", "6–7 月"),
          ("Śrāvaṇa", "Śravaṇa", "女", "7–8 月"), ("Bhādrapada", "Bhādrapadā", "室・壁", "8–9 月"),
          ("Āśvina", "Aśvinī", "婁", "9–10 月"), ("Kārttika", "Kṛttikā", "昴", "10–11 月"),
          ("Mārgaśīrṣa", "Mṛgaśiras", "觜", "11–12 月"), ("Pauṣa", "Puṣya", "鬼", "12–1 月"),
          ("Māgha", "Maghā", "星", "1–2 月"), ("Phālguna", "Phalgunī", "張・翼", "2–3 月")]
MONTHS_EN = ["Mar–Apr", "Apr–May", "May–Jun", "Jun–Jul", "Jul–Aug", "Aug–Sep", "Sep–Oct", "Oct–Nov",
             "Nov–Dec", "Dec–Jan", "Jan–Feb", "Feb–Mar"]


def tx(k):
    return TXT[LANG][k]


S = None


# ══════════════════════ 共用：月相 ══════════════════════
def moon_phase(ax, x, y, r, k, waxing=True, z=6, rim=True):
    """k＝亮面比例 0..1；waxing＝右半亮（北半球）"""
    ax.add_patch(Circle((x, y), r, fc="#20283E", ec=GREY if rim else "none", lw=1.0, zorder=z))
    if k <= 0.005:
        return
    c = 1 - 2 * k                                  # 晨昏線橢圓半軸（帶號）
    n = 60
    side = 1 if waxing else -1
    pts = [(x + side * r * math.sin(math.pi * i / n), y + r * math.cos(math.pi * i / n)) for i in range(n + 1)]
    pts += [(x + side * c * r * math.sin(math.pi * i / n), y - r * math.cos(math.pi * i / n)) for i in range(n + 1)]
    ax.add_patch(Polygon(pts, closed=True, fc=MOON, ec="none", zorder=z + 1))


def ring_pos(n, R, cx=0.0, cy=0.0, start=90.0):
    return [(cx + R * math.cos(math.radians(start - 360 * i / n)),
             cy + R * math.sin(math.radians(start - 360 * i / n))) for i in range(n)]


# ══════════════════════ C-A28-02 二十七位妻子 ══════════════════════
RI = 3                                             # Rohiṇī＝第 4 位（ring index 3）


def c02_wives(ax):
    T(ax, 0, 0.90, tx("c02_title"), 31)
    T(ax, 0, 0.82, tx("c02_sub"), 17, GREY, w="normal")
    moon_phase(ax, 0, -0.05, 0.16, 1.0)
    T(ax, 0, -0.27, tx("soma"), 20, MOON)
    pos = ring_pos(27, 0.56, 0, -0.05)
    for i, (x, y) in enumerate(pos):
        col = RED if i == RI else BLUE
        ax.add_patch(Circle((x, y), 0.045 if i == RI else 0.035, fc=col, ec="none", alpha=1 if i == RI else .85, zorder=5))
        if i == RI:
            ax.add_patch(Circle((x, y), 0.085, fc=RED, ec="none", alpha=.22, zorder=4))
    x, y = pos[RI]
    ax.plot([0.12, x - 0.06], [0.03, y - 0.03], c=RED, lw=1.6, alpha=.6, ls=(0, (4, 3)), zorder=3)
    T(ax, x + 0.10, y + 0.08, tx("rohini"), 22, RED, ha="left")
    T(ax, x + 0.10, y + 0.01, tx("rohini2"), 15, WHITE, ha="left", w="normal")


def c02_home(ax):
    T(ax, 0, 0.90, tx("c02b_title"), 31)
    moon_phase(ax, -0.10, 0.18, 0.13, 1.0)
    T(ax, -0.10, 0.0, tx("soma"), 18, MOON)
    ax.add_patch(Circle((0.13, 0.22), 0.07, fc=RED, ec="none", alpha=.22, zorder=4))
    ax.add_patch(Circle((0.13, 0.22), 0.04, fc=RED, ec="none", zorder=5))
    T(ax, 0.23, 0.22, tx("rohini"), 18, RED, ha="left")
    pos = ring_pos(26, 0.80, 0, 0.12, start=90 - 360 / 52)
    for x, y in pos:
        if y > 0.72 or y < -0.48:
            continue
        ax.add_patch(Circle((x, y), 0.032, fc=GREY, ec="none", alpha=.75, zorder=5))
    for ang in (35, 145, 215, 325, 255, 285):
        a = math.radians(ang)
        C.arrow(ax, (0.68 * math.cos(a), 0.12 + 0.68 * math.sin(a)), (0.40 * math.cos(a), 0.12 + 0.40 * math.sin(a)),
                c=GREY, lw=1.6, alpha=.6)
    T(ax, 0, -0.62, tx("c02b_1"), 19, GREY)
    T(ax, 0, -0.72, tx("c02b_2"), 19, AMBER)
    T(ax, 0, -0.82, tx("c02b_3"), 17, WHITE, w="normal")


# ══════════════════════ C-A28-03 盈虧 ══════════════════════
def c03_wane(ax):
    T(ax, 0, 0.90, tx("c03_title"), 31)
    for i, k in enumerate([1.0, 0.85, 0.65, 0.45, 0.25, 0.08]):
        moon_phase(ax, -0.70 + i * 0.28, 0.66, 0.10, k, waxing=False)
    C.arrow(ax, (0.82, 0.50), (-0.82, 0.50), c=GREY, lw=1.6, alpha=.6)
    T(ax, 0, 0.41, tx("c03_1"), 17, WHITE, w="normal")
    T(ax, 0, 0.34, tx("c03_2"), 17, AMBER)


def c03_cycle(ax):
    cx, cy, R = 0, -0.33, 0.43
    for i in range(30):
        a = math.radians(90 - 360 * i / 30)          # 從頂端順時針：滿→虧→新→盈
        age = i / 30.0
        k = (1 + math.cos(2 * math.pi * age)) / 2
        moon_phase(ax, cx + R * math.cos(a), cy + R * math.sin(a), 0.036, k, waxing=age > 0.5, rim=False)
    T(ax, cx + 0.66, cy + 0.10, tx("c03_wane"), 16, GREY, ha="center")
    T(ax, cx - 0.66, cy + 0.10, tx("c03_wax"), 16, AMBER, ha="center")
    T(ax, cx, cy + 0.04, tx("c03_c1"), 20, WHITE)
    T(ax, cx, cy - 0.05, tx("c03_c2"), 15, GREY, w="normal")
    T(ax, 0, -0.88, tx("c03_foot"), 14, GREY, w="normal")


# ══════════════════════ C-A28-04 Somnāth ══════════════════════
MAP = json.load(open(os.path.join(BASE, "07_資料來源/地圖/南亞陸地_naturalearth_110m.json"), encoding="utf-8"))
LON0, LAT0, MSC = 80.0, 20.0, 0.042
SOM = (20.888, 70.401)


def mpp(lon, lat):
    return (lon - LON0) * math.cos(math.radians(LAT0)) * MSC, (lat - LAT0) * MSC - 0.05


def c04_india(ax):
    T(ax, 0, 0.90, tx("c04_title"), 31)
    T(ax, 0, 0.82, tx("c04_sub"), 16, GREY, w="normal")
    clip = Circle((0.0, -0.05), 0.74, transform=ax.transData)
    ax.add_patch(Circle((0.0, -0.05), 0.74, fc="none", ec=GREY, lw=1.0, alpha=.5, zorder=3))
    for p in MAP["polygons"]:
        pts = [mpp(x, y) for x, y in p["ring"]]
        poly = Polygon(pts, closed=True, fc=LAND, ec=LAND, lw=0.6, zorder=2)
        ax.add_patch(poly); poly.set_clip_path(clip)
    T(ax, *mpp(79.5, 22.5), tx("india"), 18, GREY)
    T(ax, *mpp(65.5, 15.0), tx("arab"), 16, BLUE, w="normal")
    T(ax, *mpp(88.5, 15.5), tx("bay"), 16, BLUE, w="normal")
    T(ax, 0, -0.86, tx("map_src"), 11, GREY, w="normal")


def c04_som(ax):
    x, y = mpp(SOM[1], SOM[0])
    ax.add_patch(Circle((x, y), 0.055, fc=RED, ec="none", alpha=.25, zorder=6))
    ax.add_patch(Circle((x, y), 0.022, fc=RED, ec="none", zorder=7))
    T(ax, x - 0.04, y - 0.10, tx("som"), 18, RED, ha="left")
    T(ax, x - 0.04, y - 0.17, tx("som2"), 14, WHITE, ha="left", w="normal")
    T(ax, *mpp(71.8, 24.2), tx("guj"), 15, AMBER)


# ══════════════════════ C-A28-05 33→27 ══════════════════════
def crown(ax, x, y, s=0.08):
    pts = [(x - s, y), (x - s, y + s * 0.8), (x - s / 2, y + s * 0.35), (x, y + s), (x + s / 2, y + s * 0.35),
           (x + s, y + s * 0.8), (x + s, y)]
    ax.add_patch(Polygon(pts, closed=True, fc=AMBER, ec="none", zorder=8))


def c05_33(ax):
    T(ax, 0, 0.90, tx("c05_title"), 31)
    T(ax, 0, 0.82, tx("c05_src"), 17, AMBER, w="normal")
    moon_phase(ax, 0, 0.36, 0.13, 1.0)
    crown(ax, 0, 0.50, 0.07)
    for i in range(33):
        r, c = divmod(i, 11)
        x, y = -0.70 + c * 0.14, 0.02 - r * 0.13
        col = RED if i == 3 else BLUE
        ax.add_patch(Circle((x, y), 0.038, fc=col, ec="none", alpha=.9, zorder=5))
    T(ax, 0.82, -0.12, "33", 26, BLUE, ha="center")
    T(ax, 0, -0.44, tx("c05_1"), 18, WHITE, w="normal")
    T(ax, 0, -0.55, tx("c05_2"), 18, WHITE, w="normal")
    T(ax, 0, -0.68, tx("c05_3"), 20, AMBER)


def c05_27(ax):
    T(ax, 0, 0.90, tx("c05b_title"), 31)
    T(ax, 0, 0.82, tx("c05b_src"), 17, AMBER, w="normal")
    moon_phase(ax, 0, 0.0, 0.13, 1.0)
    ax.add_patch(Circle((0, 0), 0.55, fc="none", ec=GREY, lw=1.2, ls=(0, (5, 4)), alpha=.6, zorder=3))
    for i, (x, y) in enumerate(ring_pos(27, 0.55)):
        ax.add_patch(Circle((x, y), 0.035, fc=RED if i == RI else BLUE, ec="none", zorder=5))
    T(ax, 0, -0.70, tx("c05b_1"), 19, WHITE, w="normal")
    T(ax, 0, -0.80, tx("c05b_2"), 22, AMBER)


# ══════════════════════ C-A28-06 距離折線 ══════════════════════
def min_dist_by_year(hip, y0=2014, y1=2035):
    import ephem
    ra, dec = map(math.radians, S[hip][:2])
    star = ephem.FixedBody(); star._ra, star._dec, star._epoch = ra, dec, ephem.J2000
    moon = ephem.Moon()
    out = {}
    d = ephem.Date(f"{y0}/1/1"); end = ephem.Date(f"{y1 + 1}/1/1")
    step = 2 * ephem.hour
    while d < end:
        moon.compute(d); star.compute(d)
        s = math.degrees(ephem.separation(moon, star))
        if s < 15:                                 # 細算
            for k in range(-12, 13):
                dd = d + k * 10 * ephem.minute
                moon.compute(dd); star.compute(dd)
                s = min(s, math.degrees(ephem.separation(moon, star)))
        y = int(str(ephem.Date(d)).split("/")[0])
        out[y] = min(out.get(y, 99), s)
        d += step
    return out


DIST = {}


def c06_chart(ax):
    T(ax, 0, 0.90, tx("c06_title"), 29)
    T(ax, 0, 0.82, tx("c06_sub"), 15, GREY, w="normal")
    X0, X1, Y0, Y1 = -0.72, 0.84, -0.55, 0.62
    yr0, yr1, vmax = 2014, 2035, 11.0
    fx = lambda yr: X0 + (yr - yr0) / (yr1 - yr0) * (X1 - X0)
    fy = lambda v: Y0 + v / vmax * (Y1 - Y0)
    ax.plot([X0, X1], [Y0, Y0], c=WHITE, lw=1.2, alpha=.5)
    ax.plot([X0, X0], [Y0, Y1], c=WHITE, lw=1.2, alpha=.5)
    for v in (0, 2, 4, 6, 8, 10):
        ax.plot([X0 - 0.015, X0], [fy(v), fy(v)], c=WHITE, lw=1, alpha=.5)
        T(ax, X0 - 0.03, fy(v), f"{v}°", 12, GREY, ha="right", w="normal")
    for yr in range(2015, 2036, 5):
        T(ax, fx(yr), Y0 - 0.05, str(yr), 12, GREY, w="normal")
    T(ax, X0 - 0.10, Y1 + 0.06, tx("c06_y"), 12, GREY, ha="left", w="normal")
    occ = 1.3
    ax.fill_between([X0, X1], [Y0, Y0], [fy(occ), fy(occ)], color=AMBER, alpha=.12, lw=0)
    ax.plot([X0, X1], [fy(occ), fy(occ)], c=AMBER, lw=1.0, alpha=.6, ls=(0, (4, 3)))
    T(ax, fx(2030.2), Y0 + 0.045, tx("c06_occ"), 10.5, AMBER, w="normal")
    for hip, col, lw, al in ((80763, GREY, 2.0, .65), (21421, RED, 3.2, 1.0)):
        ys = sorted(DIST[hip])
        ax.plot([fx(y) for y in ys], [fy(DIST[hip][y]) for y in ys], c=col, lw=lw, alpha=al, zorder=5)
        ax.scatter([fx(y) for y in ys], [fy(DIST[hip][y]) for y in ys], s=22, c=col, alpha=al, zorder=6, lw=0)
    R = DIST[21421]
    for yr, key, dy, ha in ((2018, "c06_last", 0.14, "right"), (2033, "c06_next", 0.06, "left"),
                            (2027, "c06_now", 0.0, "left")):
        ax.scatter([fx(yr)], [fy(R[yr])], s=150, facecolors="none", edgecolors=AMBER, lw=2, zorder=7)
        T(ax, fx(yr) + (0.035 if ha == "left" else -0.03), fy(R[yr]) + dy, tx(key), 13.5, AMBER, ha=ha)
    T(ax, fx(2019.4), fy(5.6), tx("c06_r"), 15, RED, ha="right")
    T(ax, fx(2016.0), fy(10.4), tx("c06_j"), 13, GREY, w="normal")
    T(ax, 0, -0.74, tx("c06_foot"), 17, WHITE, w="normal")


# ══════════════════════ C-A28-07 十二個月名（圖卡） ══════════════════════
def c07_card(ax):
    ax.text(0.5, 0.925, tx("c07_title"), fontproperties=C.FP, fontsize=24, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.885, tx("c07_sub"), fontproperties=C.FP, fontsize=13.5, color=GREY, ha="center", va="center")
    X = (0.08, 0.42, 0.78)
    y = 0.835
    for x, k in zip(X, ("c07_h1", "c07_h2", "c07_h3")):
        ax.text(x, y, tx(k), fontproperties=C.FP, fontsize=12.5, color=GREY, ha="left", va="center", weight="bold")
    y -= 0.022
    for i, (mo, nak, cn, when) in enumerate(MONTHS):
        y -= 0.052
        hi = i == 0
        if hi:
            ax.add_patch(FancyBboxPatch((0.05, y - 0.022), 0.90, 0.044, boxstyle="round,pad=0.004,rounding_size=0.012",
                                        fc="#3A3420", ec=AMBER, lw=1.2, zorder=2))
        ax.plot([0.05, 0.95], [y + 0.026, y + 0.026], c=WHITE, lw=0.5, alpha=.15)
        ax.text(X[0], y, mo, fontproperties=C.FP, fontsize=16, color=AMBER if hi else WHITE, ha="left", va="center", weight="bold", zorder=3)
        ax.text(X[1], y, nak + (f"（{cn}）" if LANG == "zh" else ""), fontproperties=C.FP, fontsize=14,
                color=AMBER if hi else BLUE, ha="left", va="center", zorder=3)
        ax.text(X[2], y, when if LANG == "zh" else MONTHS_EN[i], fontproperties=C.FP, fontsize=13,
                color=GREY, ha="left", va="center", zorder=3)
    ax.text(0.5, y - 0.065, tx("c07_now"), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.075, tx("c07_f1"), fontproperties=C.FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.035, tx("c10_tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A28-08 起點搬家 ══════════════════════
AYAN27 = 24.222
PREC = 50.29 / 3600.0


def c08_axis(lam):                                 # 恆星黃經 → x（東在左；中心 15°）
    return -(((lam - 6.0) + 180) % 360 - 180) * 0.022


def c08_vp(ax):
    T(ax, 0, 0.90, tx("c08_title"), 31)
    T(ax, 0, 0.82, tx("c08_sub"), 14.5, GREY, w="normal")
    yb = 0.25
    ax.plot([-0.92, 0.92], [yb, yb], c="#A9B8D6", lw=2, alpha=.6)
    T(ax, -0.86, yb + 0.06, tx("c08_east"), 13, GREY, ha="left", w="normal")
    T(ax, 0.86, yb + 0.06, tx("c08_west"), 13, GREY, ha="right", w="normal")
    import ephem
    stars = [(17702, "Kṛttikā", 7), (8903, "Aśvinī", 1), (8832, None, 1), (5737, "Revatī", 2)]
    for hip, nm, _ in stars:
        ra, dec = S[hip][:2]
        q = ephem.Equatorial(math.radians(ra), math.radians(dec), epoch=ephem.J2000)
        e = ephem.Ecliptic(ephem.Equatorial(q, epoch="2027/4/16"))
        lam = math.degrees(e.lon) - AYAN27
        x = c08_axis(lam)
        if abs(x) > 0.9:
            continue
        col = RED if hip == 21421 else WHITE
        ax.scatter([x], [yb + math.degrees(e.lat) * 0.012], s=60 if hip != 5737 else 25, c=col, zorder=6, lw=0)
        if nm:
            T(ax, x, yb + math.degrees(e.lat) * 0.012 + 0.07, nm, 14, BLUE)
    for yr, key, col in ((-2300, "c08_v1", GREY), (300, "c08_v2", GREY), (2027, "c08_v3", AMBER)):
        lam_vp = -(AYAN27 - PREC * (2027 - yr))      # 春分點的恆星黃經
        x = c08_axis(lam_vp)
        ax.plot([x, x], [yb - 0.10, yb + 0.02], c=col, lw=2.2, alpha=.9)
        ax.scatter([x], [yb - 0.12], s=90, marker="v", c=col, zorder=6)
        T(ax, x, yb - 0.19, tx("c08_vp"), 13, col, w="normal")
        T(ax, x, yb - 0.25, tx(key), 14, col)
    C.arrow(ax, (c08_axis(-24.0), yb - 0.36), (c08_axis(36.0), yb - 0.36), c=AMBER, lw=2.2, alpha=.8, style="-|>")


def c08_start(ax):
    T(ax, -0.45, -0.38, tx("c08_s1"), 16, WHITE, w="normal")
    T(ax, 0.40, -0.50, tx("c08_s2"), 16, WHITE, w="normal")
    T(ax, 0, -0.68, tx("c08_s3"), 18, AMBER)


# ══════════════════════ C-A28-09 兩條黃道 ══════════════════════
RO, RI2 = 0.62, 0.44


def pol(r, lam, rot=0.0):                         # λ 逆時針、春分點在左（東在左的星圖慣例：0° 朝左）
    a = math.radians(180 - (lam + rot))
    return r * math.cos(a), r * math.sin(a) - 0.06


def c09_rulers(ax):
    T(ax, 0, 0.90, tx("c09_title"), 31)
    for r, col in ((RO, AMBER), (RI2, BLUE)):
        ax.add_patch(Circle((0, -0.06), r, fc="none", ec=col, lw=2.0, alpha=.8, zorder=3))
    for d in range(0, 360, 30):
        ax.plot(*zip(pol(RO - 0.03, d), pol(RO + 0.03, d)), c=AMBER, lw=1.6, alpha=.8)
        ax.plot(*zip(pol(RI2 - 0.03, d + AYAN27), pol(RI2 + 0.03, d + AYAN27)), c=BLUE, lw=1.6, alpha=.8)
    x, y = pol(RO + 0.19, 0)
    T(ax, x, y, tx("c09_vp") + " 0°", 14, AMBER)
    sx, sy = pol(RI2, 180 + AYAN27)
    ax.scatter([sx], [sy], s=80, c=WHITE, zorder=7)
    lx, ly = pol(RI2 + 0.085, 180 + AYAN27)
    T(ax, lx, ly, tx("c09_spica"), 13, WHITE)
    a0, a1 = pol(RO + 0.05, 0), pol(RO + 0.05, AYAN27)
    T(ax, 0, -0.77, tx("c09_diff"), 20, AMBER)
    T(ax, 0, 0.80, tx("c09_trop"), 14, AMBER, w="normal")
    T(ax, 0, 0.73, tx("c09_sid"), 14, BLUE, w="normal")
    from matplotlib.patches import Arc
    ax.add_patch(Arc((0, -0.06), 2 * (RO + 0.07), 2 * (RO + 0.07), theta1=180 - AYAN27, theta2=180,
                     ec=WHITE, lw=2, zorder=5))


def c09_signs(ax):
    signs = tx("signs")
    for i, nm in enumerate(signs):
        x, y = pol(RO - 0.075, i * 30 + 15)
        T(ax, x, y, nm, 12, AMBER, w="normal")
        x, y = pol(RI2 - 0.075, i * 30 + 15 + AYAN27)
        T(ax, x, y, nm, 11, BLUE, w="normal")
    lam_sun = 20.0                                  # 4/10 太陽回歸黃經 ≈ 20°（PyEphem 20.0）
    x0, y0 = pol(RI2 - 0.02, lam_sun)
    x1, y1 = pol(RO + 0.02, lam_sun)
    ax.plot([x0, x1], [y0, y1], c=RED, lw=2, alpha=.85, zorder=6)
    ax.scatter([x1], [y1], s=140, c=RED, zorder=7)
    T(ax, 0, -0.86, tx("c09_sun") + "：" + tx("c09_sun2") if LANG == "zh" else tx("c09_sun") + ": " + tx("c09_sun2"),
      13.5, RED, w="normal")
    T(ax, 0, -0.06, tx("c09_foot"), 14, WHITE, w="normal")


# ══════════════════════ C-A28-10 今晚抬頭看（圖卡） ══════════════════════
def c10_card(ax):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.033", "121.5654"; o.elevation = 0
    o.date = ephem.Date("2027/4/16 12:00"); o.pressure = 0
    ax.text(0.5, 0.925, tx("c10_title"), fontproperties=C.FP, fontsize=25, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.885, tx("c10_sub"), fontproperties=C.FP, fontsize=12.5, color=GREY, ha="center", va="center")
    cx, cy, R = 0.5, 0.53, 0.43
    asp = 9 / 16                                    # 卡片座標 x 單位是 y 的 16/9 倍
    def xy(alt, az):
        r = (90 - alt) / 90 * R
        a = math.radians(az)
        return cx - r * math.sin(a), cy + r * math.cos(a) * asp     # 北上、東左（仰望）
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((cx, cy), 2 * R, 2 * R * asp, fc="#0E1530", ec=GREY, lw=1.2, zorder=1))
    for alt in (30, 60):
        ax.add_patch(Ellipse((cx, cy), 2 * R * (90 - alt) / 90, 2 * R * (90 - alt) / 90 * asp, fc="none", ec=GREY,
                             lw=0.6, alpha=.35, ls=(0, (3, 3)), zorder=2))
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = xy(-7, az)
        ax.text(x, y, tx(k), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center", weight="bold")
    lst = o.sidereal_time()
    for h, (ra, dec, v) in ((h, S[h][:3]) for h in S):
        if v > 3.6:
            continue
        st = ephem.FixedBody(); st._ra, st._dec, st._epoch = math.radians(ra), math.radians(dec), ephem.J2000
        st.compute(o)
        alt, az = math.degrees(st.alt), math.degrees(st.az)
        if alt < 0:
            continue
        x, y = xy(alt, az)
        ax.scatter([x], [y], s=max(1.5, (4.2 - v) ** 2.2 * 2.2), c=WHITE, lw=0, zorder=4)
    def body(b):
        b.compute(o); return math.degrees(b.alt), math.degrees(b.az)
    def star(h):
        st = ephem.FixedBody(); st._ra, st._dec, st._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        st.compute(o); return math.degrees(st.alt), math.degrees(st.az)
    marks = [(body(ephem.Moon()), "moon", MOON, 160, (-0.035, -0.030)), (star(49669), "reg", BLUE, 0, (0.0, 0.024)),
             (body(ephem.Mars()), "mars", RED, 70, (0.030, -0.017)), (body(ephem.Jupiter()), "jup", WHITE, 90, (0.042, 0.0)),
             (star(21421), "ald", RED, 50, (0.0, 0.040)), (star(17702), "ple", BLUE, 0, (0.0, 0.020)),
             (star(69673), "arc", AMBER, 50, (0.0, 0.020)), (star(65474), "spi", AMBER, 50, (0.0, -0.020))]
    for (alt, az), key, col, s, (dx, dy) in marks:
        x, y = xy(alt, az)
        if s:
            ax.scatter([x], [y], s=s, c=col, lw=0, zorder=6)
        ax.text(x + dx, y + dy, tx(key), fontproperties=C.FP, fontsize=11.5, color=col, ha="center", va="center",
                weight="bold", zorder=7)
        if key == "ald":
            ax.text(x + dx, y + dy - 0.018, tx("ald2"), fontproperties=C.FP, fontsize=9.5, color=WHITE,
                    ha="center", va="center", zorder=7)
    ax.text(0.5, 0.235, tx("c10_n1"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.200, tx("c10_n2"), fontproperties=C.FP, fontsize=12, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.035, tx("c10_tag"), fontproperties=C.FP, fontsize=12, color=WHITE, ha="center", va="center")


# ══════════════════════ 輸出 ══════════════════════
def emit_alone(title, layers):
    """每層各自獨立（不互疊）：每層一張透明＋一張黑底預覽"""
    for nm, fn in layers:
        f, ax = C.newfig(); fn(ax); C.save(f, "", f"{title}_{nm}層_透明.png")
        f, ax = C.newfig(dark=True); fn(ax); C.save(f, "", f"{title}_預覽-{nm}_黑底.png", transparent=False)


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    for hip in (21421, 80763):
        DIST[hip] = min_dist_by_year(hip)
        print("  ", hip, {y: round(v, 2) for y, v in DIST[hip].items()})
    emit_alone("C-A28-02_二十七位妻子", [("妻子", c02_wives), ("回娘家", c02_home)])
    C.emit("", [("消瘦", c03_wane), ("盈虧", c03_cycle)], title="C-A28-03_盈虧")
    C.emit("", [("印度", c04_india), ("古吉拉特", c04_som)], title="C-A28-04_Somnāth在哪")
    emit_alone("C-A28-05_33到27", [("三十三", c05_33), ("二十七", c05_27)])
    f, ax = C.newfig(); c06_chart(ax); C.save(f, "", "C-A28-06_月亮與Rohiṇī的距離_透明.png")
    f, ax = C.newfig(dark=True); c06_chart(ax); C.save(f, "", "C-A28-06_月亮與Rohiṇī的距離_預覽_黑底.png", transparent=False)
    f, ax = C.newcard(dark=True); c07_card(ax); C.save(f, "", "C-A28-07_十二個月名_圖卡.png", transparent=False)
    C.emit("", [("春分點", c08_vp), ("起點", c08_start)], title="C-A28-08_起點搬家")
    C.emit("", [("兩尺", c09_rulers), ("十二宮", c09_signs)], title="C-A28-09_兩條黃道")
    f, ax = C.newcard(dark=True); c10_card(ax); C.save(f, "", "C-A28-10_今晚抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
