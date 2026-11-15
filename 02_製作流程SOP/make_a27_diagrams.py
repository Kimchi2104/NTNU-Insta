# -*- coding: utf-8 -*-
"""A-27 曼達爾：同一片海的另一套星圖｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A27-01 曼達爾的海（地圖層、航線層、季風層）→ 02 鏡
C-A27-02 資料從哪來（書目層）→ 03 鏡
C-A27-03 季風漁汛曆（月環層、魟鯊層；四月層、六月層＝合成層，08、09 鏡單獨疊一張）→ 06、08、09 鏡
C-A27-04 金星兩個名字（海上層、山上層）→ 10 鏡
C-A27-05 兩份星圖對照（9:16 圖卡）→ 11 鏡
C-A27-06 Karama 河谷（擴散層、河谷層）→ 12 鏡
C-A27-07 同一刻，兩個地方（台北層、蘇拉威西層）→ 13 鏡
C-A27-08 今晚抬頭看（9:16 圖卡，可存圖；台北 2027/3/26–27）→ 13b 鏡

做法：地圖沿用 A-26 的手描海岸線（make_a26_diagrams 的 LANDS，非精確國界）；航線照 Rasyid et al. 2021 §18.2.3 的四個方向，
是示意不是航跡；季風只畫在西航線上（論文主詞是往西的船）。季風漁汛曆的月份全照論文（漁夫的說法），不是自算的晨見日期。
Karama 河谷的河道與遺址位置是示意（論文只說在 Mamuju 縣）。C-A27-07 的星位用 PyEphem 自算（地平座標，含折射）。
不翻拍書封、不畫族人肖像、不畫帆船與紅衣陶（照片美宣另尋授權）。

執行：python3 make_a27_diagrams.py            （中文，輸出 05_素材/A-27_曼達爾/_概念圖/）
      python3 make_a27_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G
import make_a26_diagrams as A26                       # 手描海岸線、Map、curve（import 時會 set_base 到 A-26，下面改回）

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-27_曼達爾/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND = "#FF6B6B", "#7C8BA8", "#2A3350"
LANG = "zh"
Map, curve = A26.Map, A26.curve

TXT = {
    "zh": {
        "c01_title": "曼達爾的海", "c01_sub": "手描示意，非精確海岸線；航線是示意，不是實際航跡",
        "mandar": "曼達爾人", "mandar2": "（西蘇拉威西沿海）", "majene": "Majene", "strait": "望加錫海峽",
        "sulawesi": "蘇拉威西", "borneo": "婆羅洲", "java": "爪哇", "sumatra": "蘇門答臘", "png": "新幾內亞",
        "aus": "澳洲",
        "e1": "摩鹿加", "e2": "巴布亞", "e3": "澳洲北岸（海參）", "w1": "爪哇", "w2": "麻六甲",
        "n1": "北：菲律賓", "s1": "南：努沙登加拉",
        "east": "往東：香料、椰乾、海參", "west": "往西：把東邊的貨賣出去",
        "m_go": "6–9 月　東南季風 → 出發", "m_back": "12–3 月　西北季風 → 回家",
        "c01_foot": "Rasyid, Hidayat & Orchiston 2021 §18.2.3",
        "c02_title": "資料從哪來", "c02_auth": "Rasyid, Hidayat & Orchiston（2021）",
        "c02_paper": "〈Star Patterns in Mandar Navigation〉",
        "c02_book": "《Exploring the History of Southeast Asian Astronomy》第 18 章，Springer",
        "c02_rows": [("誰去問", "萬隆理工學院（ITB）天文系、Bosscha 天文台的天文學家"),
                     ("問了誰", "七十歲以上的退休漁夫"),
                     ("怎麼認星", "用 Stellarium 模擬 1900 年的 Majene 天空，再到野外驗證"),
                     ("記下多少", "11 個天體圖樣，6 個是導航用的星座"),
                     ("年輕一輩", "出海已經不看星星了")],
        "c02_foot": "論文沒寫訪談年份與受訪人數",
        "c03_title": "季風漁汛曆", "c03_sub": "老漁夫說的月份（論文原話）",
        "months": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "nw": "西北季風", "nw2": "漁船不出海・商船回家", "se": "東南季風", "se2": "往西的船出發",
        "cool": "涼季",
        "ray": "魟魚升起", "ray2": "11 月底清晨", "shark": "鯊魚升起", "shark2": "12 月底清晨",
        "net": "漁網星", "net2": "4 月半夜・涼季、bambang 魚", "plei": "昴宿回到東方", "plei2": "6 月清晨・飛魚季",
        "c03_foot": "Rasyid et al. 2021；月份是漁夫的說法，不是自算的晨見日期",
        "c04_title": "金星的兩個名字",
        "sea": "海上・清晨東方", "sea_n": "Pambawa Allo", "sea_zh": "帶著太陽的星", "sea_d": "看見它，約一小時後日出",
        "mtn": "山上", "mtn_n": "Bawi", "mtn_zh": "豬星", "mtn_d": "看見它要小心：豬要出來找東西吃",
        "sun": "太陽（地平線下）", "venus": "金星",
        "c04_foot": "Rasyid et al. 2021；論文沒說豬星是晨星還是昏星",
        "c05_title": "兩份星圖對照", "c05_sub": "同一片海、同一片天",
        "bg": "布吉斯（上週）", "md": "曼達爾（本週）",
        "bg_rows": [("寡婦", "sea", "寡"), ("瘸腿的房子", "sea", "房"), ("魟魚", "sea", "魟"), ("鯊魚", "sea", "鯊"),
                    ("船（北斗）", "sea", ""), ("曼達爾的寡婦", "sea", ""), ("三的記號（腰帶）", "sea", ""),
                    ("龍（銀河）", "sea", "龍"), ("豬（金星）", "land", "豬"),
                    ("犁（獵戶）", "land", ""), ("雞", "land", ""), ("薏苡稈", "land", "")],
        "md_rows": [("寡婦", "sea", "寡"), ("斜屋", "sea", "房"), ("魟魚", "sea", "魟"), ("鯊魚（17 星）", "sea", "鯊"),
                    ("漁網星（北斗＋天龍＋牧夫）", "sea", ""), ("三星一組", "sea", ""), ("昴宿（飛魚季）", "sea", ""),
                    ("龍（銀河）", "sea", "龍"), ("豬星（金星）", "land", "豬"), ("帶著太陽的星（金星）", "sea", "")],
        "k_sea": "海上・航海與捕魚", "k_land": "岸上・農事與山上", "k_same": "同名同形",
        "c05_note": "布吉斯：航海（Ammarell）＋農事（Pelras）兩份研究\n曼達爾：只有海邊漁夫的訪談，內陸種稻的人還沒人問",
        "c05_src": "Stellarium bugis、mandar；Rasyid et al. 2021 表 18.6；Ôhashi & Orchiston 2021",
        "c06_title": "為什麼這麼像？", "c06_sub": "研究者認為：都承自南島先民（主流說法，年代為約數）",
        "taiwan": "台灣", "k_bp1": "約 4,000 年前", "k_phil": "菲律賓", "k_sul": "蘇拉威西",
        "k_pac": "→ 太平洋",
        "inset": "西蘇拉威西", "karama": "Karama 河谷", "karama2": "約 3,500 年前的聚落・紅衣陶",
        "mamuju": "Mamuju", "inset_note": "河道與遺址位置為示意",
        "c06_foot": "Rasyid et al. 2021 §18.4（引 Bellwood 2017；Anggraeni et al. 2014）",
        "c07_title": "同一刻，兩個地方", "c07_sub": "2027/3/26 晚上 8 點（台灣與西蘇拉威西同一個時區）",
        "tpe": "台北・面向東北", "maj": "Majene・面向北方", "below": "還在海面下",
        "dubhe": "天樞", "merak": "天璇", "thuban": "右樞", "boo": "牧夫 θ",
        "c07_foot": "PyEphem 4.2.1 自算（含大氣折射）", "legend": "藍線＝船　綠＝漁夫　紅＝漁具　空心＝地平線下",
        "c08_title": "今晚抬頭看", "c08_sub": "台北 2027/3/26（五）晚上 → 3/27 清晨",
        "c08_rows": [("19:23", "天黑（天文昏影結束）", WHITE),
                     ("20:00 東北", "北斗＝曼達爾漁網的那一頭\n天樞 44°、天璇 47°（天龍、牧夫那幾顆較暗）", BLUE),
                     ("22:01", "月出（81%，虧凸月）", GREY),
                     ("23:16–01:11\n鵝鑾鼻 正南", "斜屋（南十字＋δ Cen）中天前後\n只有十字架一、屋頂 δ Cen 過 10°", AMBER),
                     ("3/27 05:00–05:40\n東方", "金星（−4.0 等）＝帶著太陽的星\n04:09 升起、05:51 日出", AMBER)],
        "c08_tip": "同一刻的蘇拉威西：斗口只有二十度上下，船尾還在海面下",
        "c08_src": "PyEphem 4.2.1 自算（台北 25.033°N 121.565°E；鵝鑾鼻 21.90°N）",
    },
    "en": {
        "c01_title": "The Mandar's sea", "c01_sub": "Hand-drawn sketch; routes are schematic",
        "mandar": "the Mandar", "mandar2": "(coastal West Sulawesi)", "majene": "Majene", "strait": "Makassar Strait",
        "sulawesi": "Sulawesi", "borneo": "Borneo", "java": "Java", "sumatra": "Sumatra", "png": "New Guinea",
        "aus": "Australia",
        "e1": "Moluccas", "e2": "Papua", "e3": "N. Australia (trepang)", "w1": "Java", "w2": "Malacca",
        "n1": "N: Philippines", "s1": "S: Nusa Tenggara",
        "east": "East: spices, copra, trepang", "west": "West: selling the eastern goods",
        "m_go": "Jun–Sep  SE monsoon → set out", "m_back": "Dec–Mar  NW monsoon → home",
        "c01_foot": "Rasyid, Hidayat & Orchiston 2021 §18.2.3",
        "c02_title": "Where the data come from", "c02_auth": "Rasyid, Hidayat & Orchiston (2021)",
        "c02_paper": "'Star Patterns in Mandar Navigation'",
        "c02_book": "Exploring the History of Southeast Asian Astronomy, ch. 18, Springer",
        "c02_rows": [("Who asked", "Astronomers from ITB and Bosscha Observatory"),
                     ("Whom", "Retired fishermen aged over 70"),
                     ("How", "Stellarium sky of Majene in 1900, then field checks"),
                     ("Found", "11 sky patterns, 6 used for navigation"),
                     ("Young fishers", "no longer use the stars")],
        "c02_foot": "Interview year and number of informants not stated",
        "c03_title": "Monsoon & fishing calendar", "c03_sub": "Months as the old fishermen tell it",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "nw": "NW monsoon", "nw2": "no fishing; traders sail home", "se": "SE monsoon", "se2": "westbound ships leave",
        "cool": "cool season",
        "ray": "Stingray rises", "ray2": "late Nov, dawn", "shark": "Shark rises", "shark2": "late Dec, dawn",
        "net": "Fishing Net", "net2": "April midnight · bambang fish", "plei": "Pleiades back in the east",
        "plei2": "June dawn · flying fish",
        "c03_foot": "Rasyid et al. 2021; fishermen's months, not computed dates",
        "c04_title": "Two names for Venus",
        "sea": "At sea · dawn, east", "sea_n": "Pambawa Allo", "sea_zh": "the star carrying the Sun",
        "sea_d": "sunrise about an hour later",
        "mtn": "In the hills", "mtn_n": "Bawi", "mtn_zh": "the Pig", "mtn_d": "beware: pigs come out to feed",
        "sun": "Sun (below horizon)", "venus": "Venus",
        "c04_foot": "Rasyid et al. 2021; morning or evening star for 'Pig' not stated",
        "c05_title": "Two star maps", "c05_sub": "Same sea, same sky",
        "bg": "Bugis (last week)", "md": "Mandar (this week)",
        "bg_rows": [("Widow", "sea", "寡"), ("Lame house", "sea", "房"), ("Stingray", "sea", "魟"), ("Shark", "sea", "鯊"),
                    ("Ship (Dipper)", "sea", ""), ("Mandar Widow", "sea", ""), ("Sign of Three", "sea", ""),
                    ("Dragon (Milky Way)", "sea", "龍"), ("Pig (Venus)", "land", "豬"),
                    ("Plough (Orion)", "land", ""), ("Chicken", "land", ""), ("Job's tears stalk", "land", "")],
        "md_rows": [("Widow", "sea", "寡"), ("Slanted house", "sea", "房"), ("Stingray", "sea", "魟"),
                    ("Shark (17 stars)", "sea", "鯊"), ("Fishing Net (Dipper+Dra+Boo)", "sea", ""),
                    ("Group of three", "sea", ""), ("Pleiades (flying fish)", "sea", ""),
                    ("Dragon (Milky Way)", "sea", "龍"), ("Pig (Venus)", "land", "豬"),
                    ("Star carrying the Sun", "sea", "")],
        "k_sea": "At sea · sailing & fishing", "k_land": "Ashore · farming & hills", "k_same": "same name & shape",
        "c05_note": "Bugis: sailing (Ammarell) + farming (Pelras) studies\nMandar: only coastal fishermen interviewed so far",
        "c05_src": "Stellarium bugis, mandar; Rasyid et al. 2021 Table 18.6; Ôhashi & Orchiston 2021",
        "c06_title": "Why so alike?", "c06_sub": "Researchers: shared Austronesian ancestors (mainstream view; dates approx.)",
        "taiwan": "Taiwan", "k_bp1": "~4,000 years ago", "k_phil": "Philippines", "k_sul": "Sulawesi",
        "k_pac": "→ Pacific",
        "inset": "West Sulawesi", "karama": "Karama valley", "karama2": "settlements ~3,500 yrs ago · red-slipped pottery",
        "mamuju": "Mamuju", "inset_note": "river and sites schematic",
        "c06_foot": "Rasyid et al. 2021 §18.4 (citing Bellwood 2017; Anggraeni et al. 2014)",
        "c07_title": "Same moment, two places", "c07_sub": "26 Mar 2027, 8 pm (same time zone)",
        "tpe": "Taipei · facing NE", "maj": "Majene · facing N", "below": "still below the sea",
        "dubhe": "Dubhe", "merak": "Merak", "thuban": "Thuban", "boo": "θ Boo",
        "c07_foot": "Computed with PyEphem 4.2.1 (with refraction)", "legend": "blue = boat · green = fishermen · red = gear · hollow = below horizon",
        "c08_title": "Look up tonight", "c08_sub": "Taipei, Fri 26 Mar 2027 → dawn 27 Mar",
        "c08_rows": [("19:23", "Dark (end of astronomical twilight)", WHITE),
                     ("20:00 NE", "Big Dipper = the Mandar Fishing Net\nDubhe 44°, Merak 47°", BLUE),
                     ("22:01", "Moonrise (81%, waning gibbous)", GREY),
                     ("23:16–01:11\nEluanbi, due S", "Slanted House (Crux + δ Cen)\nonly γ Cru and δ Cen above 10°", AMBER),
                     ("27 Mar 05:00–05:40\nEast", "Venus (−4.0) = star carrying the Sun\nrises 04:09, sunrise 05:51", AMBER)],
        "c08_tip": "Same moment in Sulawesi: the Dipper's bowl only ~20° up",
        "c08_src": "Computed with PyEphem 4.2.1 (Taipei 25.033°N 121.565°E; Eluanbi 21.90°N)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ C-A27-01 曼達爾的海 ══════════════════════
M1 = Map(121.0, -4.0, 0.042)
MAJ = (-3.54, 118.97)
DEST_E = [("e1", -3.0, 128.2, 0.10), ("e2", -4.5, 137.5, -0.08), ("e3", -12.0, 132.5, -0.12)]
DEST_W = [("w1", -6.9, 110.4, 0.12), ("w2", 2.2, 102.25, 0.10)]


def c01_map(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 30, WHITE)
    T(ax, 0.0, 0.855, tx("c01_sub"), 14, GREY, w="normal")
    M1.lands(ax)
    for k, lat, lon, fs in (("sulawesi", -1.4, 121.4, 14), ("borneo", 0.5, 114.0, 15),
                            ("sumatra", -1.6, 101.4, 13), ("png", -6.2, 141.5, 14), ("aus", -19.5, 133.0, 17)):
        T(ax, *M1(lat, lon), tx(k), fs, GREY, w="normal", alpha=.9)
    T(ax, *M1(0.3, 118.6), tx("strait"), 10, GREY, w="normal")
    x, y = M1.dot(ax, *MAJ, c=PURPLE, s=120)
    ax.scatter([x], [y], s=650, c=PURPLE, alpha=.22, zorder=7, lw=0)
    T(ax, x + 0.03, y - 0.035, tx("majene"), 12, PURPLE, ha="left", w="normal")
    lx, ly = M1(3.6, 121.2)
    ax.plot([lx, x + 0.01], [ly - 0.03, y + 0.02], c=PURPLE, lw=1.0, alpha=.6, zorder=6)
    T(ax, lx, ly + 0.015, tx("mandar"), 18, PURPLE)
    T(ax, lx, ly - 0.035, tx("mandar2"), 12, PURPLE, w="normal")
    T(ax, 0.0, -0.93, tx("c01_foot"), 11.5, GREY, w="normal")


def c01_route(ax):
    a = M1(*MAJ)
    for k, lat, lon, bend in DEST_E:
        b = M1(lat, lon)
        curve(ax, a, b, bend=bend, c=GREEN, lw=2.6)
        T(ax, b[0], b[1] - 0.045, tx(k), 13, GREEN)
    for k, lat, lon, bend in DEST_W:
        b = M1(lat, lon)
        curve(ax, a, b, bend=bend, c=AMBER, lw=2.6)
        T(ax, b[0] + (0.0 if k == "w1" else 0.02), b[1] + 0.045, tx(k), 13, AMBER)
    for k, lat, lon, bend, dy in (("n1", 8.5, 124.0, -0.10, 0.04), ("s1", -9.0, 121.0, 0.10, -0.045)):
        b = M1(lat, lon)
        curve(ax, a, b, bend=bend, c=WHITE, lw=1.3, alpha=.55)
        T(ax, b[0] + 0.02, b[1] + dy, tx(k), 11, WHITE, w="normal", alpha=.8)
    T(ax, *M1(-15.6, 135.0), tx("east"), 14, GREEN)
    T(ax, *M1(-10.4, 107.0), tx("west"), 14, AMBER)


def c01_monsoon(ax):
    # 只畫在西航線上：兩條平行粗箭頭（出發／回家）＋標籤，放在爪哇海上方
    # 圖例式：放在西航線下方的印度洋空白處（往西＝向左的箭頭、回家＝向右）
    xa, xb = -0.92, -0.62
    for y, c, k, (p, q) in ((-0.56, AMBER, "m_go", (xb, xa)), (-0.68, BLUE, "m_back", (xa, xb))):
        CB.arrow(ax, (q, y), (p, y), c=c, lw=4.0, alpha=.95, style="-|>")
        T(ax, xb + 0.04, y, tx(k), 14, c, ha="left")


# ══════════════════════ C-A27-02 資料從哪來 ══════════════════════
def c02_bib(ax):
    T(ax, 0.0, 0.80, tx("c02_title"), 32, WHITE)
    T(ax, 0.0, 0.66, tx("c02_auth"), 19, AMBER)
    T(ax, 0.0, 0.59, tx("c02_paper"), 16, WHITE, w="normal")
    T(ax, 0.0, 0.535, tx("c02_book"), 12, GREY, w="normal")
    ax.plot([-0.82, 0.82], [0.47, 0.47], c=WHITE, lw=1.0, alpha=.35)
    y = 0.37
    for i, (k, v) in enumerate(tx("c02_rows")):
        col = AMBER if i == 1 else (RED if i == 4 else BLUE)
        T(ax, -0.80, y, k, 16, col, ha="left")
        T(ax, -0.42, y, v, 14.5, WHITE, ha="left", w="normal")
        y -= 0.13
    T(ax, 0.0, -0.40, tx("c02_foot"), 12, GREY, w="normal")


# ══════════════════════ C-A27-03 季風漁汛曆 ══════════════════════
R0, R1 = 0.50, 0.66                                    # 月環內外半徑
CY3 = -0.04


def m_ang(mon):
    """月份（1–12，可小數；1＝一月初）→ 角度：一月初在正上方，順時針"""
    return math.radians(90.0 - (mon - 1) * 30.0)


def m_xy(mon, r):
    a = m_ang(mon)
    return r * math.cos(a), CY3 + r * math.sin(a)


def arc(ax, m0, m1, r, c, lw, alpha=.9):
    ts = [m0 + (m1 - m0) * i / 60 for i in range(61)]
    ax.plot([m_xy(t, r)[0] for t in ts], [m_xy(t, r)[1] for t in ts], c=c, lw=lw, alpha=alpha,
            solid_capstyle="butt", zorder=4)


MARKS = [("ray", 11.85, PURPLE, (-0.52, 0.70), "right"), ("shark", 12.85, RED, (0.10, 0.76), "left"),
         ("net", 4.5, BLUE, (0.97, -0.60), "right"), ("plei", 6.3, WHITE, (0.10, -0.83), "right")]


def c03_ring(ax):
    T(ax, 0.0, 0.93, tx("c03_title"), 30, WHITE)
    T(ax, 0.0, 0.865, tx("c03_sub"), 14, GREY, w="normal")
    ax.add_patch(CB.Circle((0, CY3), R1, fc="none", ec=WHITE, lw=1.4, alpha=.45, zorder=3))
    ax.add_patch(CB.Circle((0, CY3), R0, fc="none", ec=WHITE, lw=1.0, alpha=.30, zorder=3))
    for i in range(12):
        a0 = m_xy(i + 1, R0); a1 = m_xy(i + 1, R1)
        ax.plot([a0[0], a1[0]], [a0[1], a1[1]], c=WHITE, lw=1.0, alpha=.35, zorder=3)
        x, y = m_xy(i + 1.5, (R0 + R1) / 2)
        T(ax, x, y, tx("months")[i], 13, WHITE, w="normal", alpha=.9)
    # 季風（月環內側）：西北季風 12–3 月、東南季風 6–9 月
    arc(ax, 12.0, 16.0, R0 - 0.07, BLUE, 9)
    arc(ax, 6.0, 10.0, R0 - 0.07, AMBER, 9)
    arc(ax, 4.0, 6.0, R0 - 0.07, GREY, 4, alpha=.6)
    T(ax, 0.0, CY3 + 0.25, tx("nw"), 16, BLUE)
    T(ax, 0.0, CY3 + 0.19, tx("nw2"), 11.5, BLUE, w="normal")
    T(ax, 0.0, CY3 - 0.19, tx("se"), 16, AMBER)
    T(ax, 0.0, CY3 - 0.25, tx("se2"), 11.5, AMBER, w="normal")
    x, y = m_xy(5.0, R0 - 0.17)
    T(ax, x, y, tx("cool"), 11.5, GREY, w="normal")
    for k, mon, col, _, _ in MARKS:                       # 四格先灰階
        x, y = m_xy(mon, R1 + 0.035)
        ax.scatter([x], [y], s=130, c=GREY, alpha=.5, zorder=6, lw=0)
    T(ax, 0.0, -0.92, tx("c03_foot"), 11, GREY, w="normal")


def mark(ax, k):
    _, mon, col, (lx, ly), ha = next(m for m in MARKS if m[0] == k)
    x, y = m_xy(mon, R1 + 0.035)
    ax.scatter([x], [y], s=700, c=col, alpha=.22, zorder=7, lw=0)
    ax.scatter([x], [y], s=160, c=col, zorder=8, lw=0)
    T(ax, lx, ly + 0.025, tx(k), 15, col, ha=ha)
    T(ax, lx, ly - 0.025, tx(k + "2"), 11.5, col, ha=ha, w="normal")


def c03_fish(ax):
    mark(ax, "ray"); mark(ax, "shark")


def c03_apr(ax):
    c03_ring(ax); c03_fish(ax); mark(ax, "net")


def c03_jun(ax):
    c03_apr(ax); mark(ax, "plei")


# ══════════════════════ C-A27-04 金星兩個名字 ══════════════════════
def venus(ax, x, y):
    ax.scatter([x], [y], s=1600, c=WHITE, alpha=.10, zorder=6, lw=0)
    ax.scatter([x], [y], s=450, c="#FFF6D8", alpha=.25, zorder=6, lw=0)
    ax.scatter([x], [y], s=110, c=WHITE, zorder=7, lw=0)


def c04_sea(ax):
    T(ax, 0.0, 0.88, tx("c04_title"), 32, WHITE)
    x0, x1, hy = -0.92, -0.04, -0.12
    T(ax, (x0 + x1) / 2, 0.68, tx("sea"), 16, GREY, w="normal")
    ax.add_patch(CB.Rectangle((x0, hy - 0.40), x1 - x0, 0.40, fc="#0E1A33", ec="none", zorder=4))
    for r, a in ((0.16, .10), (0.12, .18), (0.09, .55)):      # 地平線下的太陽（透過海面的暖光，示意）
        ax.add_patch(CB.Circle(((x0 + x1) / 2, hy - 0.13), r, fc=AMBER, ec="none", alpha=a, zorder=4.5))
    T(ax, (x0 + x1) / 2, hy - 0.13, tx("sun"), 11, AMBER, w="normal", z=13)
    CB.water(ax, y=hy - 0.04, x0=x0, x1=x1, c=BLUE, rows=2, amp=0.012)
    ax.plot([x0, x1], [hy, hy], c=WHITE, lw=1.6, alpha=.7, zorder=5)
    venus(ax, (x0 + x1) / 2 + 0.05, hy + 0.22)
    T(ax, (x0 + x1) / 2 + 0.05, hy + 0.30, tx("venus"), 12, WHITE, w="normal")
    T(ax, (x0 + x1) / 2, 0.50, tx("sea_n"), 18, AMBER)
    T(ax, (x0 + x1) / 2, 0.43, tx("sea_zh"), 17, WHITE)
    T(ax, (x0 + x1) / 2, -0.62, tx("sea_d"), 13, WHITE, w="normal")


def pig(ax, x, y, s=1.0, c=GREY):
    ax.add_patch(CB.Ellipse((x, y), 0.20 * s, 0.11 * s, fc=c, ec="none", zorder=6))
    ax.add_patch(CB.Ellipse((x - 0.105 * s, y + 0.012 * s), 0.075 * s, 0.065 * s, fc=c, ec="none", zorder=6))
    ax.add_patch(CB.Ellipse((x - 0.145 * s, y + 0.004 * s), 0.025 * s, 0.032 * s, fc=c, ec="none", zorder=6))
    ax.add_patch(CB.Polygon([(x - 0.10 * s, y + 0.04 * s), (x - 0.085 * s, y + 0.075 * s),
                             (x - 0.075 * s, y + 0.035 * s)], closed=True, fc=c, ec="none", zorder=6))
    for dx in (-0.06, -0.03, 0.04, 0.07):
        ax.plot([x + dx * s, x + dx * s], [y - 0.04 * s, y - 0.085 * s], c=c, lw=4.0 * s, zorder=6,
                solid_capstyle="round")
    ax.plot([x + 0.10 * s, x + 0.125 * s], [y + 0.01 * s, y + 0.03 * s], c=c, lw=1.6 * s, zorder=6)


def c04_mtn(ax):
    x0, x1, hy = 0.04, 0.92, -0.12
    T(ax, (x0 + x1) / 2, 0.68, tx("mtn"), 16, GREY, w="normal")
    ridge = [(x0, hy - 0.02), (0.18, hy + 0.10), (0.30, hy + 0.04), (0.46, hy + 0.17), (0.60, hy + 0.06),
             (0.74, hy + 0.12), (x1, hy + 0.01), (x1, hy - 0.40), (x0, hy - 0.40)]
    ax.add_patch(CB.Polygon(ridge, closed=True, fc="#1F2A44", ec=GREY, lw=1.4, zorder=4))
    venus(ax, 0.62, hy + 0.36)
    T(ax, 0.62, hy + 0.44, tx("venus"), 12, WHITE, w="normal")
    pig(ax, 0.48, hy - 0.20, s=1.0)
    T(ax, (x0 + x1) / 2, 0.50, tx("mtn_n"), 18, GREEN)
    T(ax, (x0 + x1) / 2, 0.43, tx("mtn_zh"), 17, WHITE)
    T(ax, (x0 + x1) / 2, -0.62, tx("mtn_d"), 13, WHITE, w="normal")
    T(ax, 0.0, -0.84, tx("c04_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-A27-05 兩份星圖對照（9:16 圖卡） ══════════════════════
def c05_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.950, tx("c05_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.913, tx("c05_sub"), fontproperties=FP, fontsize=13, color=GREY, ha="center", va="center")
    xl, xr = 0.06, 0.94
    ax.text(0.27, 0.870, tx("bg"), fontproperties=FP, fontsize=16, color=AMBER, ha="center", va="center",
            weight="bold")
    ax.text(0.73, 0.870, tx("md"), fontproperties=FP, fontsize=16, color=PURPLE, ha="center", va="center",
            weight="bold")
    col = {"sea": BLUE, "land": GREEN}
    pos = {}
    for side, rows, x, ha in (("L", tx("bg_rows"), xl, "left"), ("R", tx("md_rows"), xr, "right")):
        y = 0.825
        for name, kind, key in rows:
            ax.add_patch(CB.FancyBboxPatch((x - (0 if ha == "left" else 0.40), y - 0.020), 0.40, 0.040,
                                           boxstyle="round,pad=0.0,rounding_size=0.01", fc=col[kind], alpha=.16,
                                           ec=col[kind], lw=1.0))
            ax.text(x + (0.015 if ha == "left" else -0.015), y, name, fontproperties=FP, fontsize=11.5,
                    color=WHITE, ha=ha, va="center")
            if key:
                pos.setdefault(key, {})[side] = y
            y -= 0.047
    for key, d in pos.items():
        if "L" in d and "R" in d:
            ax.plot([xl + 0.40, xr - 0.40], [d["L"], d["R"]], c=AMBER, lw=1.6, alpha=.85)
            for xx, yy in ((xl + 0.40, d["L"]), (xr - 0.40, d["R"])):
                ax.scatter([xx], [yy], s=22, c=AMBER, zorder=5, lw=0)
    y = 0.145
    for k, c in (("k_sea", BLUE), ("k_land", GREEN)):
        ax.add_patch(CB.FancyBboxPatch((0.08 if k == "k_sea" else 0.52, y - 0.012), 0.03, 0.024,
                                       boxstyle="round,pad=0.0,rounding_size=0.005", fc=c, alpha=.5, ec=c))
        ax.text(0.12 if k == "k_sea" else 0.56, y, tx(k), fontproperties=FP, fontsize=10.5, color=WHITE,
                ha="left", va="center")
    ax.plot([0.30, 0.36], [0.112, 0.112], c=AMBER, lw=1.6)
    ax.text(0.38, 0.112, tx("k_same"), fontproperties=FP, fontsize=10.5, color=WHITE, ha="left", va="center")
    ax.text(0.5, 0.218, tx("c05_note"), fontproperties=FP, fontsize=11.5, color=AMBER, ha="center",
            va="center", linespacing=1.6)
    ax.text(0.5, 0.068, tx("c05_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A27-06 Karama 河谷 ══════════════════════
M6 = Map(126.0, 8.5, 0.044)
INS = (-0.97, -0.84, -0.37, -0.16)                       # 插圖框 x0, y0, x1, y1
M6i = Map(119.3, -2.8, 0.20)


def c06_go(ax):
    T(ax, 0.0, 0.92, tx("c06_title"), 30, WHITE)
    T(ax, 0.0, 0.855, tx("c06_sub"), 14, GREY, w="normal")
    M6.lands(ax, clip=(-1.0, 1.0, -0.80, 0.82))
    tw, ph, su = M6(22.0, 121.0), M6(16.0, 121.3), M6(-2.4, 119.6)
    x, y = M6(23.7, 121.0)
    ax.scatter([x], [y], s=900, c=AMBER, alpha=.25, zorder=7, lw=0)
    T(ax, x + 0.08, y + 0.02, tx("taiwan"), 20, AMBER, ha="left")
    curve(ax, tw, ph, bend=0.0, c=AMBER, lw=3.0, ls="-")
    curve(ax, ph, M6(6.5, 124.0), bend=0.0, c=AMBER, lw=3.0, ls="-", arrow=False)
    curve(ax, M6(6.5, 124.0), su, bend=0.08, c=AMBER, lw=3.0, ls="-")
    curve(ax, M6(6.5, 124.0), M6(-1.0, 147.0), bend=-0.10, c=BLUE, lw=2.4)
    T(ax, ph[0] + 0.05, ph[1] + 0.03, tx("k_phil"), 15, WHITE, ha="left")
    T(ax, ph[0] + 0.05, ph[1] - 0.03, tx("k_bp1"), 14, AMBER, ha="left")
    T(ax, su[0] + 0.05, su[1] - 0.02, tx("k_sul"), 15, WHITE, ha="left")
    T(ax, *M6(1.5, 143.0), tx("k_pac"), 16, BLUE)
    T(ax, 0.0, -0.92, tx("c06_foot"), 11, GREY, w="normal")


def c06_valley(ax):
    from matplotlib.patches import Rectangle
    x0, y0, x1, y1 = INS
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#0B0F1E", ec=AMBER, lw=1.6, zorder=8))
    clip = Rectangle((x0, y0), x1 - x0, y1 - y0, transform=ax.transData)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for poly in A26.LANDS[:1]:
        p = CB.Polygon([(cx + M6i(*q)[0], cy + M6i(*q)[1]) for q in poly], closed=True, fc=LAND, ec=GREY, lw=1.2,
                       zorder=9)
        ax.add_patch(p); p.set_clip_path(clip)
    river = [(-2.62, 119.85), (-2.50, 119.62), (-2.40, 119.45), (-2.25, 119.33), (-2.12, 119.26)]
    ax.plot([cx + M6i(*q)[0] for q in river], [cy + M6i(*q)[1] for q in river], c=BLUE, lw=2.2, zorder=10)
    kx, ky = cx + M6i(-2.48, 119.58)[0], cy + M6i(-2.48, 119.58)[1]
    ax.scatter([kx], [ky], s=500, c=AMBER, alpha=.3, zorder=11, lw=0)
    ax.scatter([kx], [ky], s=80, c=AMBER, zorder=12, lw=0)
    for nm, lat, lon, c in ((tx("mamuju"), -2.68, 118.89, WHITE), (tx("majene"), -3.54, 118.97, PURPLE)):
        xx, yy = cx + M6i(lat, lon)[0], cy + M6i(lat, lon)[1]
        ax.scatter([xx], [yy], s=40, c=c, zorder=12, lw=0)
        T(ax, xx - 0.02, yy, nm, 11, c, ha="right", w="normal", z=13)
    T(ax, cx, y1 - 0.04, tx("inset"), 13, AMBER, z=13)
    T(ax, kx - 0.06, ky + 0.075, tx("karama"), 14, AMBER, z=13)
    T(ax, cx, y0 + 0.075, tx("karama2"), 11.5, WHITE, w="normal", z=13)
    T(ax, cx, y0 + 0.03, tx("inset_note"), 10, GREY, w="normal", z=13)
    sx, sy = M6(-2.4, 119.6)                              # 大圖上的位置 → 插圖框
    ax.plot([sx, x1], [sy, y1 - 0.10], c=AMBER, lw=1.0, alpha=.6, zorder=7, ls=(0, (4, 3)))


# ══════════════════════ C-A27-07 同一刻，兩個地方 ══════════════════════
TPE = (25.0330, 121.5654)
MAJS = (-3.54, 118.97)
NETH = [53910, 54061, 56211, 61281, 68756, 70497]
FISH = [59774, 62956, 65378]
GEARH = [58001, 67301]


def altaz_all(where, when):
    import ephem
    S = G.load_stars(BASE)
    o = ephem.Observer(); o.lat, o.lon = str(where[0]), str(where[1]); o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - 8 * ephem.hour)
    out = {}
    for h in NETH + FISH + GEARH:
        s = ephem.FixedBody(); s._ra, s._dec = math.radians(S[h][0]), math.radians(S[h][1]); s._epoch = ephem.J2000
        s.compute(o)
        out[h] = (math.degrees(s.az), math.degrees(s.alt))
    return out


def panel(ax, x0, x1, where, az0, title, keys):
    P = altaz_all(where, "2027/3/26 20:00")
    hy, sc = -0.30, 0.0105                                # 地平線 y、每度長
    xc = (x0 + x1) / 2

    def xy(h):
        az, alt = P[h]
        d = (az - az0 + 180) % 360 - 180
        return xc + d * sc, hy + alt * sc
    ax.add_patch(CB.Rectangle((x0, hy - 0.40), x1 - x0, 0.40, fc="#0E1A33", ec="none", zorder=4))
    ax.plot([x0, x1], [hy, hy], c=WHITE, lw=1.6, alpha=.7, zorder=5)
    for a in (10, 20, 30, 40, 50):
        ax.plot([x0, x1], [hy + a * sc] * 2, c=WHITE, lw=0.6, alpha=.12, zorder=3)
        T(ax, x0 + 0.01, hy + a * sc + 0.012, f"{a}°", 9, GREY, ha="left", w="normal")
    pts = [xy(h) for h in NETH]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        ax.plot([xa, xb], [ya, yb], c=BLUE, lw=2.0, alpha=.9, zorder=6,
                ls="-" if min(ya, yb) >= hy else (0, (3, 3)))
    for hs, c in ((FISH, GREEN), (GEARH, RED)):
        for h in hs:
            x, y = xy(h)
            ax.scatter([x], [y], s=60, facecolors="none" if y < hy else c, edgecolors=c, lw=1.4, zorder=7)
    for h in NETH:
        x, y = xy(h)
        ax.scatter([x], [y], s=55, facecolors=WHITE if y >= hy else "none", edgecolors=WHITE, lw=1.3, zorder=8)
    for h, k, dx, dy in keys:
        x, y = xy(h)
        alt = P[h][1]
        T(ax, x + dx, y + dy, f"{tx(k)} {alt:.0f}°", 12, WHITE if alt >= 0 else GREY, w="normal", z=13)
    T(ax, xc, 0.66, title, 16, AMBER)
    return P


def c07_tpe(ax):
    T(ax, 0.0, 0.90, tx("c07_title"), 30, WHITE)
    T(ax, 0.0, 0.83, tx("c07_sub"), 13, GREY, w="normal")
    panel(ax, -0.96, -0.04, TPE, 35.0, tx("tpe"), [(54061, "dubhe", -0.09, 0.0), (53910, "merak", 0.0, 0.04)])
    T(ax, 0.0, -0.90, tx("c07_foot"), 11, GREY, w="normal")


def c07_maj(ax):
    panel(ax, 0.04, 0.96, MAJS, 15.0, tx("maj"),
          [(54061, "dubhe", -0.09, -0.01), (53910, "merak", 0.03, 0.045), (68756, "thuban", 0.0, -0.045),
           (70497, "boo", 0.0, -0.045)])
    T(ax, 0.50, -0.56, tx("below"), 12, GREY, w="normal", z=13)
    T(ax, 0.0, -0.80, tx("legend"), 12, WHITE, w="normal", z=13)


# ══════════════════════ C-A27-08 今晚抬頭看（9:16 圖卡） ══════════════════════
def c08_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.947, tx("c08_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.907, tx("c08_sub"), fontproperties=FP, fontsize=14, color=GREY, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.880, 0.880], c=WHITE, lw=1.0, alpha=.4)
    y = 0.865
    for t, body, col in tx("c08_rows"):
        n = max(body.count("\n"), t.count("\n")) + 1
        h = 0.036 + 0.034 * n
        ax.text(0.04, y - 0.014 - 0.017 * n, t, fontproperties=FP, fontsize=12.5, color=col, ha="left",
                va="center", weight="bold", linespacing=1.5)
        ax.text(0.40, y - 0.014 - 0.017 * n, body, fontproperties=FP, fontsize=12, color=WHITE, ha="left",
                va="center", linespacing=1.5)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.add_patch(CB.FancyBboxPatch((0.05, y - 0.090), 0.90, 0.060, boxstyle="round,pad=0.005,rounding_size=0.02",
                                   fc="#1B2240", ec=PURPLE, lw=1.2))
    ax.text(0.5, y - 0.060, tx("c08_tip"), fontproperties=FP, fontsize=11.5, color=PURPLE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.068, tx("c08_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center",
            va="center")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        A26.LANG = LANG
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    CB.emit("", [("地圖", c01_map), ("航線", c01_route), ("季風", c01_monsoon)], title="C-A27-01_曼達爾的海")
    CB.emit("", [("書目", c02_bib)], title="C-A27-02_資料從哪來")
    CB.emit("", [("月環", c03_ring), ("魟鯊", c03_fish)], title="C-A27-03_季風漁汛曆")
    CB.emit("", [("四月", c03_apr)], title="C-A27-03_季風漁汛曆", preview_name="預覽四月")
    CB.emit("", [("六月", c03_jun)], title="C-A27-03_季風漁汛曆", preview_name="預覽六月")
    CB.emit("", [("海上", c04_sea), ("山上", c04_mtn)], title="C-A27-04_金星兩個名字")
    f, ax = CB.newcard(dark=True)
    c05_card(ax)
    CB.save(f, "", "C-A27-05_兩份星圖對照_圖卡.png", transparent=False)
    CB.emit("", [("擴散", c06_go), ("河谷", c06_valley)], title="C-A27-06_Karama河谷")
    CB.emit("", [("台北", c07_tpe), ("蘇拉威西", c07_maj)], title="C-A27-07_同一刻兩個地方")
    f, ax = CB.newcard(dark=True)
    c08_card(ax)
    CB.save(f, "", "C-A27-08_今晚抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
