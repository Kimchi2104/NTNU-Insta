# -*- coding: utf-8 -*-
"""A-26 布吉斯：帆船民族的星羅盤｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A26-01 航線地圖（地圖層、航線層）→ 02 鏡
C-A26-02 星羅盤（港口層、星路層）→ 03 鏡
C-A26-03 並肩的寡婦（距離層）→ 06 鏡
C-A26-04 天上的鄰居（鄰居層）→ 09b 鏡
C-A26-05 同一個 S 形（9:16 圖卡）→ 11 鏡
C-A26-06 南島語族擴散（台灣層、擴散層）→ 13 鏡
C-A26-07 這週末抬頭看（9:16 圖卡，可存圖；台北 2027/3/19–3/20）→ 14b 鏡

做法：地圖是手描示意輪廓（海岸線取幾十個經緯度點連起來，非精確國界）；航線是示意（Rasyid et al. 2021 p. 550：
印尼群島、往西到馬來半島與新加坡、遠到澳洲北岸），不是實際航跡。星羅盤的港口方位用 OpenStreetMap 座標自算大圓方位；
「星從哪座島升起」只畫一個例子——Ammarell 2008 摘要寫的「七月底、八月初黃昏，寡婦出現在 Bima 的方向」（PyEphem 自算
184.5°），不虛構 Ammarell 原表裡其他星與島的對應（原書本環境拿不到）。S 形圖卡的連線全部照 Stellarium
（tukano 001、tupi 001、bugis 002＋003），星點照 Hipparcos。不翻拍任何書影、不畫族人肖像、不畫 Pinisi 帆船（照片另尋授權）。

執行：python3 make_a26_diagrams.py            （中文，輸出 05_素材/A-26_布吉斯/_概念圖/）
      python3 make_a26_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-26_布吉斯/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND, SEA = "#FF6B6B", "#7C8BA8", "#2A3350", "#4F86C6"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "南蘇拉威西的帆船跑多遠", "c01_sub": "手描示意，非精確海岸線；航線是示意，不是實際航跡",
        "sulawesi": "蘇拉威西", "borneo": "婆羅洲", "java": "爪哇", "sumatra": "蘇門答臘", "malay": "馬來半島",
        "png": "新幾內亞", "aus": "澳洲", "phil": "菲律賓", "makassar": "望加錫", "bugis": "布吉斯人",
        "bugis2": "（蘇拉威西南部）", "r_arch": "跑遍印尼群島", "r_west": "往西：馬來半島、新加坡",
        "r_south": "往南：澳洲北岸", "flores": "弗洛勒斯海", "singapore": "新加坡",
        "c01_foot": "Rasyid, Hidayat & Orchiston 2021, p. 550；造船技藝：UNESCO 2017（Pinisi）",
        "c02_title": "星羅盤", "c02_sub": "從 Balobaloang 看出去：每個港口一個方位",
        "balo": "Balobaloang", "balo2": "（弗洛勒斯海的小島）",
        "ports": [("望加錫", -5.135, 119.42), ("Bima", -8.448, 118.713), ("Labuan Bajo", -8.497, 119.888),
                  ("Sumenep（馬都拉）", -7.010, 113.860), ("峇里 Benoa", -8.745, 115.210),
                  ("Bau-Bau（布頓）", -5.470, 122.600)],
        "N": "北", "E": "東", "S": "南", "W": "西",
        "rise": "升起", "stand": "停住", "set": "落下", "inset": "示意：一顆星從某座島的上方升起、停住、落下", "island": "島",
        "widow1": "七月底、八月初的黃昏", "widow2": "寡婦站在 Bima 的方向", "widow3": "（方位 184.5°）",
        "c02_foot": "港口方位：OpenStreetMap 座標自算大圓方位；寡婦方位：PyEphem 自算（2027/7/31 18:28）",
        "c02_foot2": "「星羅盤」一詞：Ammarell 2008",
        "c03_title": "並肩的寡婦", "c03_sub": "從地球看並排，其實一近一遠",
        "earth": "地球", "rigil": "南門二", "hadar": "馬腹一", "ly1": "4.37 光年", "ly1b": "離太陽最近的恆星系",
        "ly2": "三百多光年", "ly2b": "（Hipparcos 約 390；其他研究約 360）", "gap": "（中間省略約 90 倍的距離）",
        "apart": "相距 4.4°", "c03_foot": "南門二：Kervella et al. 2016 視差 747.17 mas；示意圖，不按比例",
        "c04_title": "天上住著鄰居", "mandar": "曼達爾人", "mandar2": "隔壁的航海民族",
        "bajau": "巴瑤人", "bajau2": "傳統上以船為家", "bugis_n": "布吉斯人",
        "sky1": "斗口兩顆（天樞、天璇）＝曼達爾的寡婦", "sky2": "大小麥哲倫雲＝巴瑤人的記號",
        "c04_foot": "Ammarell 1999（經 Ôhashi & Orchiston 2021）；地圖為手描示意",
        "c05_title": "同一個 S 形", "c05_sub": "天蠍座，連續三週、三個民族",
        "p1": "亞馬遜・圖卡諾", "p1b": "Aña 毒蛇（天蠍＋人馬）", "p2": "巴西海岸・圖皮", "p2b": "Guirá Nhandu 美洲鴕的身體",
        "p3": "蘇拉威西・布吉斯", "p3b": "lambarué 魟魚＋bale mangngiweng 鯊魚",
        "antares": "心宿二", "c05_src": "連線：Stellarium tukano 001、tupi 001、bugis 002＋003；星點：Hipparcos",
        "c06_title": "南島語族從台灣出海", "c06_sub": "主流說法（Bellwood 等）；年代為約數",
        "taiwan": "台灣", "k_bp1": "約 4,000 年前", "k_phil": "菲律賓", "k_bp2": "約 3,500 年前",
        "k_karama": "蘇拉威西 Karama 河谷", "k_pac": "→ 太平洋", "k_bring": "帶著稻米、航海的本事",
        "k_q": "星座有沒有一起帶來？還沒有定論", "c06_foot": "Rasyid et al. 2021 p. 560（引 Bellwood 2017）；Anggraeni et al. 2014",
        "c07_title": "這週末抬頭看", "c07_sub": "台北 2027/3/19（五）晚上",
        "c07_rows": [("19:20", "天黑（天文昏影結束）", WHITE),
                     ("19:30 東北", "北斗＝布吉斯的船星，斗柄朝下\n天樞 38°、搖光 15°", BLUE),
                     ("19:30 南方", "雞 manu'：南河三 70°、天狼星 47°\n老人星 11°（八點後低於 10°）", AMBER),
                     ("19:30 東方高空", "月亮（89%）旁 2° 木星、4° 火星\n只有 3/19 當晚貼在一起", WHITE),
                     ("3/20 凌晨 墾丁", "南十字 00:25–00:58 過正南，5–11°\n寡婦 02:14–02:50 過正南，7–8°", GREEN),
                     ("月光", "3/22 滿月；3/20 月落 04:15", GREY)],
        "c07_tip": "南十字和寡婦想看清楚：四到六月、沒有月亮的晚上",
        "c07_src": "PyEphem 4.2.1 自算（台北 25.033°N 121.565°E；墾丁 21.95°N 120.80°E）",
    },
    "en": {
        "c01_title": "How far South Sulawesi's sailing ships went", "c01_sub": "Hand-drawn sketch; routes are schematic",
        "sulawesi": "Sulawesi", "borneo": "Borneo", "java": "Java", "sumatra": "Sumatra", "malay": "Malay Peninsula",
        "png": "New Guinea", "aus": "Australia", "phil": "Philippines", "makassar": "Makassar", "bugis": "the Bugis",
        "bugis2": "(South Sulawesi)", "r_arch": "all over the Indonesian archipelago", "r_west": "west: Malay Peninsula, Singapore",
        "r_south": "south: northern Australia", "flores": "Flores Sea", "singapore": "Singapore",
        "c01_foot": "Rasyid, Hidayat & Orchiston 2021, p. 550; boatbuilding: UNESCO 2017 (Pinisi)",
        "c02_title": "A star compass", "c02_sub": "Seen from Balobaloang: one bearing per port",
        "balo": "Balobaloang", "balo2": "(a small island in the Flores Sea)",
        "ports": [("Makassar", -5.135, 119.42), ("Bima", -8.448, 118.713), ("Labuan Bajo", -8.497, 119.888),
                  ("Sumenep (Madura)", -7.010, 113.860), ("Benoa (Bali)", -8.745, 115.210),
                  ("Bau-Bau (Buton)", -5.470, 122.600)],
        "N": "N", "E": "E", "S": "S", "W": "W",
        "rise": "rises", "stand": "stands", "set": "sets", "inset": "Sketch: a star rises, stands and sets above an island", "island": "island",
        "widow1": "At dusk in late July / early August", "widow2": "the Widow stands toward Bima", "widow3": "(bearing 184.5°)",
        "c02_foot": "Port bearings: great-circle bearings from OpenStreetMap coordinates; Widow: PyEphem (2027-07-31 18:28)",
        "c02_foot2": "'Star compass': Ammarell 2008",
        "c03_title": "The Widow, side by side", "c03_sub": "Side by side from Earth — one near, one far",
        "earth": "Earth", "rigil": "Alpha Centauri", "hadar": "Hadar", "ly1": "4.37 ly", "ly1b": "the nearest star system to the Sun",
        "ly2": "over 300 ly", "ly2b": "(Hipparcos ~390; other studies ~360)", "gap": "(~90× the distance omitted)",
        "apart": "4.4° apart", "c03_foot": "Alpha Centauri: Kervella et al. 2016, parallax 747.17 mas; not to scale",
        "c04_title": "Neighbours in the sky", "mandar": "the Mandar", "mandar2": "the seafaring people next door",
        "bajau": "the Bajau", "bajau2": "traditionally living on boats", "bugis_n": "the Bugis",
        "sky1": "Two pointer stars of the Dipper = the Mandar Widow", "sky2": "Magellanic Clouds = Sign of the Bajau",
        "c04_foot": "Ammarell 1999 (via Ôhashi & Orchiston 2021); hand-drawn map",
        "c05_title": "The same S", "c05_sub": "Scorpius: three weeks, three peoples",
        "p1": "Amazon · Tukano", "p1b": "Aña, the pit viper (Sco + Sgr)", "p2": "Coastal Brazil · Tupi", "p2b": "body of Guirá Nhandu, the rhea",
        "p3": "Sulawesi · Bugis", "p3b": "lambarué stingray + bale mangngiweng shark",
        "antares": "Antares", "c05_src": "Lines: Stellarium tukano 001, tupi 001, bugis 002 + 003; stars: Hipparcos",
        "c06_title": "Austronesians set sail from Taiwan", "c06_sub": "Mainstream view (Bellwood et al.); dates approximate",
        "taiwan": "Taiwan", "k_bp1": "~4,000 years ago", "k_phil": "Philippines", "k_bp2": "~3,500 years ago",
        "k_karama": "Karama valley, Sulawesi", "k_pac": "→ Pacific", "k_bring": "bringing rice and seafaring skills",
        "k_q": "Did the constellations travel too? Still open", "c06_foot": "Rasyid et al. 2021 p. 560 (citing Bellwood 2017); Anggraeni et al. 2014",
        "c07_title": "Look up this weekend", "c07_sub": "Taipei, Friday 19 March 2027",
        "c07_rows": [("19:20", "Dark (end of astronomical twilight)", WHITE),
                     ("19:30 NE", "Big Dipper = the Bugis Ship Star, handle down\nDubhe 38°, Alkaid 15°", BLUE),
                     ("19:30 S", "manu' the chicken: Procyon 70°, Sirius 47°\nCanopus 11° (below 10° after 20:00)", AMBER),
                     ("19:30 high E", "Moon (89%) with Jupiter 2° and Mars 4° away\nonly on the 19th", WHITE),
                     ("20 Mar, Kenting", "Crux due south 00:25–00:58, 5–11°\nWidow due south 02:14–02:50, 7–8°", GREEN),
                     ("Moonlight", "Full Moon 22 Mar; moonset 04:15 on the 20th", GREY)],
        "c07_tip": "For Crux and the Widow: April–June, moonless nights",
        "c07_src": "Computed with PyEphem 4.2.1 (Taipei 25.033°N 121.565°E; Kenting 21.95°N 120.80°E)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 手描海岸線（lat, lon） ══════════════════════
SULAWESI = [(1.45, 125.2), (1.1, 124.6), (0.95, 123.5), (0.9, 122.5), (1.05, 121.5), (1.1, 120.8), (0.85, 120.2),
            (0.6, 119.85), (-0.5, 119.8), (-1.2, 119.45), (-2.6, 118.85), (-3.5, 118.9), (-4.2, 119.6), (-5.0, 119.4),
            (-5.6, 119.5), (-5.6, 119.9), (-5.45, 120.3), (-4.5, 120.35), (-3.5, 120.4), (-3.0, 120.25), (-2.6, 121.0),
            (-3.5, 121.2), (-4.1, 121.6), (-4.8, 121.7), (-5.5, 122.1), (-5.0, 122.5), (-4.0, 122.6), (-3.4, 122.4),
            (-2.6, 122.1), (-2.0, 121.6), (-1.5, 122.2), (-1.2, 122.9), (-0.95, 123.35), (-0.75, 122.8),
            (-0.8, 122.0), (-0.9, 121.5), (-1.4, 120.75), (-0.8, 120.2), (0.3, 120.15), (0.5, 121.0), (0.5, 122.3),
            (0.55, 123.3), (0.8, 124.3), (1.0, 124.9)]
BORNEO = [(7.0, 116.9), (6.0, 116.1), (4.9, 115.0), (4.6, 114.0), (3.2, 113.0), (2.0, 111.2), (1.6, 109.6),
          (0.0, 109.1), (-1.3, 110.0), (-2.9, 110.3), (-3.1, 111.6), (-3.5, 113.0), (-3.4, 114.6), (-4.0, 116.0),
          (-2.5, 116.5), (-1.2, 116.8), (0.2, 117.6), (1.2, 118.9), (2.0, 118.0), (3.0, 117.8), (4.3, 118.3),
          (5.0, 119.2), (5.8, 118.1), (6.9, 117.7)]
JAVA = [(-5.9, 106.0), (-6.1, 107.5), (-6.3, 108.4), (-6.7, 108.7), (-6.9, 110.4), (-6.5, 110.9), (-6.9, 112.6),
        (-7.4, 112.8), (-7.6, 114.4), (-8.6, 114.4), (-8.4, 112.7), (-8.2, 110.5), (-7.7, 108.7), (-7.4, 106.4),
        (-6.8, 105.2)]
SUMATRA = [(5.6, 95.3), (5.2, 97.5), (3.8, 98.7), (2.5, 100.0), (1.5, 101.5), (0.8, 103.0), (-0.5, 103.6),
           (-1.6, 104.5), (-3.0, 106.0), (-4.0, 105.9), (-5.9, 105.7), (-5.5, 104.4), (-4.0, 102.4), (-2.0, 100.9),
           (-0.5, 100.0), (1.0, 98.8), (2.5, 97.5), (4.2, 96.0)]
MALAY = [(6.5, 100.2), (5.5, 100.3), (4.0, 100.6), (2.6, 101.4), (1.4, 103.4), (1.4, 104.2), (2.8, 103.5),
         (4.2, 103.4), (5.6, 102.6), (6.5, 102.0), (6.9, 101.0), (8.5, 100.3), (10.5, 99.3), (12.0, 99.2),
         (12.0, 102.0), (8.5, 100.9)]
PNG = [(-0.8, 131.2), (-1.5, 134.0), (-2.5, 137.5), (-2.6, 141.0), (-3.5, 143.5), (-5.5, 146.0), (-7.5, 147.5),
       (-10.5, 150.5), (-9.0, 146.0), (-8.0, 143.5), (-9.0, 141.0), (-8.0, 138.5), (-5.0, 138.0), (-4.0, 135.0),
       (-3.8, 133.0), (-2.5, 132.0)]
AUS = [(-30.0, 115.0), (-22.0, 113.8), (-20.5, 117.0), (-18.0, 122.2), (-15.0, 124.5), (-14.0, 126.5),
       (-15.0, 129.0), (-12.5, 130.5), (-11.2, 132.5), (-12.0, 135.5), (-15.0, 135.5), (-17.5, 140.0),
       (-12.0, 141.6), (-10.7, 142.5), (-15.0, 145.3), (-19.0, 147.0), (-25.0, 153.0), (-30.0, 153.0)]
LUZON = [(18.5, 120.8), (17.0, 120.4), (15.5, 119.9), (14.3, 120.6), (13.8, 121.3), (12.6, 124.0), (14.0, 123.0),
         (15.5, 121.5), (17.5, 122.2), (18.4, 122.2)]
MINDANAO = [(9.8, 125.5), (8.5, 126.5), (6.0, 126.2), (5.6, 125.3), (6.8, 124.0), (7.2, 122.0), (8.1, 123.3),
            (8.6, 124.5)]
TAIWAN = [(25.3, 121.6), (24.5, 121.9), (23.0, 121.4), (22.0, 120.8), (22.6, 120.3), (23.5, 120.1), (24.6, 120.7)]
SMALL = [(-8.40, 115.15, 0.55, 0.30), (-8.60, 116.35, 0.40, 0.35), (-8.70, 117.80, 1.20, 0.30),
         (-8.60, 121.00, 1.80, 0.35), (-9.50, 124.80, 1.70, 0.40), (-3.40, 129.00, 1.40, 0.35),
         (1.00, 128.00, 0.60, 1.20), (-5.20, 122.85, 0.30, 0.60), (11.0, 123.5, 1.2, 0.5), (9.8, 118.6, 1.3, 0.25),
         (-3.30, 126.60, 0.55, 0.35), (-1.6, 125.0, 0.9, 0.25)]
LANDS = [SULAWESI, BORNEO, JAVA, SUMATRA, MALAY, PNG, AUS, LUZON, MINDANAO, TAIWAN]


class Map:
    def __init__(self, lon0, lat0, sc):
        self.lon0, self.lat0, self.sc = lon0, lat0, sc

    def __call__(self, lat, lon):
        return (lon - self.lon0) * self.sc, (lat - self.lat0) * self.sc

    def lands(self, ax, alpha=.95, clip=(-1.0, 1.0, -0.86, 0.80)):
        from matplotlib.patches import Rectangle
        rect = Rectangle((clip[0], clip[2]), clip[1] - clip[0], clip[3] - clip[2], transform=ax.transData)
        for poly in LANDS:
            p = CB.Polygon([self(*q) for q in poly], closed=True, fc=LAND, ec=GREY, lw=1.3, alpha=alpha, zorder=2)
            ax.add_patch(p); p.set_clip_path(rect)
        for lat, lon, a, b in SMALL:
            x, y = self(lat, lon)
            e = CB.Ellipse((x, y), 2 * a * self.sc, 2 * b * self.sc, fc=LAND, ec=GREY, lw=1.1, alpha=alpha, zorder=2)
            ax.add_patch(e); e.set_clip_path(rect)

    def dot(self, ax, lat, lon, c=WHITE, s=60):
        x, y = self(lat, lon)
        ax.scatter([x], [y], s=s, c=c, zorder=8, lw=0)
        return x, y


def curve(ax, a, b, bend=0.15, c=AMBER, lw=2.4, ls=(0, (7, 5)), arrow=True, alpha=.95):
    """a→b 的二次貝茲弧（示意航線）"""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    n = 40
    xs = [(1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1 for t in [i / n for i in range(n + 1)]]
    ys = [(1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1 for t in [i / n for i in range(n + 1)]]
    ax.plot(xs, ys, c=c, lw=lw, ls=ls, alpha=alpha, zorder=6)
    if arrow:
        CB.arrow(ax, (xs[-1], ys[-1]), (xs[-4], ys[-4]), c=c, lw=lw, alpha=alpha, style="-|>")


# ══════════════════════ C-A26-01 航線地圖 ══════════════════════
M1 = Map(120.0, -5.0, 0.042)
MKS = (-5.135, 119.42)


def c01_map(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 30, WHITE)
    T(ax, 0.0, 0.85, tx("c01_sub"), 15, GREY, w="normal")
    M1.lands(ax)
    for k, lat, lon, fs in (("sulawesi", -1.6, 120.6, 15), ("borneo", 0.8, 114.0, 16), ("java", -7.1, 110.0, 14),
                            ("sumatra", -1.0, 101.6, 14), ("png", -5.2, 141.0, 15), ("aus", -18.5, 132.0, 18),
                            ("malay", 4.6, 104.6, 13), ("flores", -7.25, 120.9, 12)):
        T(ax, *M1(lat, lon), tx(k), fs, GREY if k == "flores" else WHITE, w="normal", alpha=.85)
    x, y = M1.dot(ax, *MKS, c=AMBER, s=120)
    ax.scatter([x], [y], s=650, c=AMBER, alpha=.18, zorder=7, lw=0)
    T(ax, x - 0.03, y - 0.02, tx("makassar"), 14, AMBER, ha="right")
    lx, ly = M1(-10.6, 116.0)                       # 標在印度洋上，細線指到蘇拉威西西南半島
    ax.plot([lx + 0.02, M1(-4.4, 120.0)[0]], [ly + 0.04, M1(-4.4, 120.0)[1]], c=AMBER, lw=1.0, alpha=.6, zorder=6)
    T(ax, lx, ly, tx("bugis"), 17, AMBER, ha="right")
    T(ax, lx, ly - 0.045, tx("bugis2"), 12, AMBER, ha="right", w="normal")
    T(ax, 0.0, -0.93, tx("c01_foot"), 11.5, GREY, w="normal")


def c01_route(ax):
    a = M1(*MKS)
    for lat, lon, bend in ((-7.1, 112.6, 0.10), (-3.6, 128.2, -0.12), (1.3, 117.9, 0.10), (-8.4, 123.5, -0.18)):
        curve(ax, a, M1(lat, lon), bend=bend, c=AMBER, lw=2.0, alpha=.75)
    curve(ax, a, M1(1.30, 103.9), bend=0.06, c=BLUE, lw=2.8)
    curve(ax, a, M1(-12.0, 133.5), bend=0.12, c=GREEN, lw=2.8)
    x, y = M1.dot(ax, 1.29, 103.85, c=BLUE, s=60)
    T(ax, x - 0.02, y + 0.045, tx("singapore"), 12, BLUE, ha="center", w="normal")
    T(ax, *M1(-4.6, 108.6), tx("r_west"), 15, BLUE)
    T(ax, *M1(-13.3, 125.0), tx("r_south"), 15, GREEN)
    T(ax, *M1(2.6, 125.6), tx("r_arch"), 15, AMBER)


# ══════════════════════ C-A26-02 星羅盤 ══════════════════════
BALO = (-6.5935, 118.8615)
RC = 0.50
CY = 0.10                  # 羅盤圓心 y


def bearing(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1])
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360.0


def az_xy(az, r):
    a = math.radians(az)
    return r * math.sin(a), r * math.cos(a)


def c02_ports(ax):
    T(ax, 0.0, 0.93, tx("c02_title"), 32, WHITE)
    T(ax, 0.0, 0.865, tx("c02_sub"), 16, GREY, w="normal")
    ax.add_patch(CB.Circle((0, CY), RC, fc="none", ec=WHITE, lw=1.6, alpha=.55, zorder=3))
    for i in range(0, 360, 10):
        r0 = RC - (0.04 if i % 30 == 0 else 0.02)
        x0, y0 = az_xy(i, r0); x1, y1 = az_xy(i, RC)
        ax.plot([x0, x1], [y0 + CY, y1 + CY], c=WHITE, lw=1.2, alpha=.5, zorder=3)
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = az_xy(az, RC + 0.06)
        T(ax, x, y + CY, tx(k), 16, GREY)
    ax.scatter([0], [CY], s=110, c=AMBER, zorder=9, lw=0)
    T(ax, 0.0, CY + 0.055, tx("balo"), 15, AMBER)
    T(ax, 0.0, CY - 0.05, tx("balo2"), 11, GREY, w="normal")
    for name, lat, lon in tx("ports"):
        az = bearing(BALO, (lat, lon))
        if name.startswith("Bima"):
            continue
        x0, y0 = az_xy(az, 0.12); x1, y1 = az_xy(az, RC)
        ax.plot([x0, x1], [y0 + CY, y1 + CY], c=BLUE, lw=1.6, alpha=.7, zorder=4)
        xl, yl = az_xy(az, RC + 0.13)
        ha = "left" if xl > 0.15 else ("right" if xl < -0.15 else "center")
        T(ax, xl, yl + CY + 0.012, name, 13, BLUE, ha=ha)
        T(ax, xl, yl + CY - 0.032, f"{az:.0f}°", 11, GREY, ha=ha, w="normal")
    T(ax, 0.0, -0.935, tx("c02_foot"), 10, GREY, w="normal")
    T(ax, 0.0, -0.965, tx("c02_foot2"), 10, GREY, w="normal")


def c02_star(ax):
    bima = [p for p in tx("ports") if p[0].startswith("Bima")][0]
    az = bearing(BALO, bima[1:])
    x0, y0 = az_xy(az, 0.12); x1, y1 = az_xy(az, RC)
    ax.plot([x0, x1], [y0 + CY, y1 + CY], c=AMBER, lw=2.6, alpha=.95, zorder=5)
    xl, yl = az_xy(az, RC + 0.16)                   # 避開「南」
    T(ax, xl, yl + CY, f"{bima[0]}　{az:.1f}°", 15, AMBER)
    # 寡婦（兩顆星）在 Bima 方位線兩側：182.5°、187.9°
    for a in (182.5, 187.9):
        x, y = az_xy(a, RC - 0.12)
        ax.scatter([x], [y + CY], s=260, c=AMBER, alpha=.2, zorder=6, lw=0)
        ax.scatter([x], [y + CY], s=70, c=WHITE, zorder=7, lw=0)
    T(ax, -0.06, CY + 0.32, tx("widow1"), 13, WHITE, ha="right", w="normal")   # 西北象限沒有港口線
    T(ax, -0.06, CY + 0.27, tx("widow2"), 14, AMBER, ha="right")
    T(ax, -0.06, CY + 0.225, tx("widow3"), 11, GREY, ha="right", w="normal")
    # 小插圖：升起・停住・落下（示意，不對應特定星與島）
    hy = -0.80
    ax.plot([-0.62, 0.62], [hy, hy], c=WHITE, lw=1.4, alpha=.6, zorder=4)
    ax.add_patch(CB.Ellipse((0.0, hy), 0.30, 0.07, fc=LAND, ec=GREY, lw=1.2, zorder=5))
    T(ax, 0.0, hy - 0.035, tx("island"), 11, GREY, w="normal")
    for x, y, k in ((-0.05, hy + 0.035, "rise"), (0.0, hy + 0.13, "stand"), (0.05, hy + 0.035, "set")):
        ax.scatter([x], [y], s=60, c=WHITE, zorder=7, lw=0)
    ax.plot([-0.05, -0.02, 0.0, 0.02, 0.05], [hy + 0.035, hy + 0.105, hy + 0.13, hy + 0.105, hy + 0.035],
            c=WHITE, lw=1.2, ls=(0, (3, 3)), alpha=.6, zorder=6)
    T(ax, -0.09, hy + 0.04, tx("rise"), 12, WHITE, ha="right")
    T(ax, 0.0, hy + 0.17, tx("stand"), 12, WHITE)
    T(ax, 0.09, hy + 0.04, tx("set"), 12, WHITE, ha="left")
    T(ax, 0.0, hy - 0.08, tx("inset"), 11, GREY, w="normal")


# ══════════════════════ C-A26-03 並肩的寡婦 ══════════════════════
def c03_dist(ax):
    T(ax, 0.0, 0.90, tx("c03_title"), 32, WHITE)
    T(ax, 0.0, 0.82, tx("c03_sub"), 16, GREY, w="normal")
    y = 0.05
    ex, rx, bx, hx = -0.82, -0.40, 0.08, 0.72
    ax.plot([ex, bx - 0.05], [y, y], c=WHITE, lw=2.0, alpha=.7, zorder=3)
    ax.plot([bx + 0.13, hx], [y, y], c=WHITE, lw=2.0, alpha=.7, zorder=3)
    import numpy as np
    for dx in (0.0, 0.08):                        # 斷開處的波浪
        t = np.linspace(-0.07, 0.07, 30)
        ax.plot(bx + dx + 0.015 * np.sin(t * 90), y + t, c=WHITE, lw=2.0, alpha=.7, zorder=3)
    ax.add_patch(CB.Circle((ex, y), 0.045, fc=BLUE, ec="none", zorder=6))
    T(ax, ex, y - 0.10, tx("earth"), 16, BLUE)
    for x, c in ((rx, AMBER), (hx, AMBER)):
        ax.scatter([x], [y], s=900, c=c, alpha=.18, zorder=5, lw=0)
        ax.scatter([x], [y], s=200, c=WHITE, zorder=6, lw=0)
    T(ax, rx, y + 0.10, tx("rigil"), 19, AMBER)
    T(ax, rx, y - 0.10, tx("ly1"), 17, WHITE)
    T(ax, rx, y - 0.16, tx("ly1b"), 12, GREY, w="normal")
    T(ax, hx, y + 0.10, tx("hadar"), 19, AMBER)
    T(ax, hx, y - 0.10, tx("ly2"), 17, WHITE)
    T(ax, hx, y - 0.16, tx("ly2b"), 11.5, GREY, w="normal")
    T(ax, bx + 0.04, y + 0.12, tx("gap"), 11.5, GREY, w="normal")
    # 下：從地球看並排
    for x in (-0.06, 0.06):
        ax.scatter([x], [-0.48], s=260, c=AMBER, alpha=.2, zorder=5, lw=0)
        ax.scatter([x], [-0.48], s=70, c=WHITE, zorder=6, lw=0)
    ax.plot([-0.06, 0.06], [-0.48, -0.48], c=AMBER, lw=2.4, zorder=4)
    T(ax, 0.0, -0.58, "bintoéng balué", 16, AMBER)
    T(ax, 0.0, -0.41, tx("apart"), 13, GREY, w="normal")
    T(ax, 0.0, -0.88, tx("c03_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-A26-04 天上的鄰居 ══════════════════════
M4 = Map(121.0, -3.0, 0.16)


def boat(ax, x, y, s=1.0, c=GREEN):
    ax.add_patch(CB.Polygon([(x - 0.035 * s, y), (x + 0.035 * s, y), (x + 0.022 * s, y - 0.016 * s),
                             (x - 0.022 * s, y - 0.016 * s)], closed=True, fc=c, ec="none", alpha=.9, zorder=7))
    ax.plot([x, x], [y, y + 0.045 * s], c=c, lw=1.4, zorder=7)
    ax.add_patch(CB.Polygon([(x + 0.002, y + 0.045 * s), (x + 0.002, y + 0.008 * s), (x + 0.03 * s, y + 0.008 * s)],
                            closed=True, fc=c, ec="none", alpha=.75, zorder=7))


def c04_nb(ax):
    T(ax, 0.0, 0.92, tx("c04_title"), 32, WHITE)
    M4.lands(ax, clip=(-1.0, 1.0, -0.72, 0.84))
    x, y = M4.dot(ax, *MKS, c=AMBER, s=90)
    T(ax, x - 0.03, y, tx("makassar"), 13, AMBER, ha="right", w="normal")
    xb, yb = M4(-4.2, 120.1)
    ax.add_patch(CB.Ellipse((xb, yb), 0.24, 0.36, fc=AMBER, ec="none", alpha=.22, zorder=3))
    T(ax, xb + 0.16, yb + 0.02, tx("bugis_n"), 18, AMBER, ha="left")
    xm, ym = M4(-3.2, 119.0)
    ax.add_patch(CB.Ellipse((xm, ym), 0.16, 0.26, fc=PURPLE, ec="none", alpha=.30, zorder=3))
    T(ax, xm - 0.11, ym + 0.03, tx("mandar"), 18, PURPLE, ha="right")
    T(ax, xm - 0.11, ym - 0.03, tx("mandar2"), 12, PURPLE, ha="right", w="normal")
    for lat, lon in ((-0.3, 121.9), (-5.9, 121.9), (-1.0, 123.0), (-4.9, 123.4), (-6.5, 119.0), (0.7, 118.6)):
        boat(ax, *M4(lat, lon), s=1.1)
    T(ax, *M4(-6.6, 123.1), tx("bajau"), 18, GREEN, ha="left")
    xx, yy = M4(-6.6, 123.1)
    T(ax, xx, yy - 0.06, tx("bajau2"), 12, GREEN, ha="left", w="normal")
    T(ax, 0.0, -0.78, tx("sky1"), 15, PURPLE)
    T(ax, 0.0, -0.84, tx("sky2"), 15, GREEN)
    T(ax, 0.0, -0.92, tx("c04_foot"), 11, GREY, w="normal")


# ══════════════════════ C-A26-05 同一個 S 形（9:16 圖卡） ══════════════════════
def load_lines(cu, cid):
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master", cu, "index.json")
    d = json.load(open(p, encoding="utf-8"))
    for c in d["constellations"]:
        if c["id"].endswith(cid):
            return [[h for h in l if isinstance(h, int)] for l in c["lines"]]


def gnom(ra, dec, ra0=266.0, dec0=-31.0):
    r, d, r0, d0 = map(math.radians, (ra, dec, ra0, dec0))
    c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(r - r0)
    x = math.cos(d) * math.sin(r - r0) / c
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(r - r0)) / c
    return -math.degrees(x), math.degrees(y)          # 東在左


def c05_card(ax):
    FP = CB.FP
    S = G.load_stars(BASE)
    ax.text(0.5, 0.950, tx("c05_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.912, tx("c05_sub"), fontproperties=FP, fontsize=13, color=GREY, ha="center", va="center")
    panels = [(tx("p1"), tx("p1b"), [(load_lines("tukano", "001"), RED)]),
              (tx("p2"), tx("p2b"), [(load_lines("tupi", "001"), WHITE)]),
              (tx("p3"), tx("p3b"), [(load_lines("bugis", "003"), RED), (load_lines("bugis", "002"), RED)])]
    from matplotlib.patches import Rectangle
    PXD = 17.0                                       # 每度幾 px（卡寬 1215、高 2160）
    for i, (t1, t2, groups) in enumerate(panels):
        top = 0.885 - i * 0.270
        x0, x1, y0, y1 = 0.05, 0.95, top - 0.250, top - 0.030
        ax.text(0.05, top - 0.012, t1, fontproperties=FP, fontsize=15, color=AMBER, ha="left", va="center",
                weight="bold")
        ax.text(0.95, top - 0.012, t2, fontproperties=FP, fontsize=10.5, color=WHITE, ha="right", va="center")
        ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.015",
                                       fc="#05070F", ec="#2A3350", lw=1.0, zorder=1))
        clip = Rectangle((x0, y0), x1 - x0, y1 - y0, transform=ax.transData)
        sx = PXD / 1215.0
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

        for h, (ra, dec, v) in S.items():
            if v > 5.0:
                continue
            gx, gy = gnom(ra, dec)
            if abs(gx) > 40 or abs(gy) > 20:
                continue
            X, Y = cx + gx * sx, cy + gy * sx * 9 / 16    # 9:16 卡的 y 單位長＝x 的 16/9 倍 → 等角要乘 9/16
            if not (x0 < X < x1 and y0 < Y < y1):
                continue
            ax.scatter([X], [Y], s=max(1.5, (5.6 - v) ** 1.9 * 2.2), c=WHITE, alpha=.9, zorder=3, lw=0)
        for segs, col in groups:
            for seg in segs:
                pts = []
                for h in seg:
                    if h not in S:
                        continue
                    gx, gy = gnom(*S[h][:2])
                    pts.append((cx + gx * sx, cy + gy * sx * 9 / 16))
                ln, = ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=1.6, alpha=.9, zorder=4)
                ln.set_clip_path(clip)
        gx, gy = gnom(*S[80763][:2])
        X, Y = cx + gx * sx, cy + gy * sx * 9 / 16
        ax.scatter([X], [Y], s=60, c=RED, alpha=.35, zorder=3, lw=0)
        ax.text(X, Y + 0.016, tx("antares"), fontproperties=FP, fontsize=8.5, color=GREY, ha="center", va="center",
                zorder=6)
    ax.text(0.5, 0.068, tx("c05_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A26-06 南島語族擴散 ══════════════════════
M6 = Map(126.0, 8.5, 0.044)


def c06_tw(ax):
    T(ax, 0.0, 0.92, tx("c06_title"), 30, WHITE)
    T(ax, 0.0, 0.855, tx("c06_sub"), 14, GREY, w="normal")
    M6.lands(ax, clip=(-1.0, 1.0, -0.80, 0.82))
    x, y = M6(23.7, 121.0)
    ax.scatter([x], [y], s=900, c=AMBER, alpha=.25, zorder=7, lw=0)
    T(ax, x + 0.08, y + 0.02, tx("taiwan"), 20, AMBER, ha="left")
    for k, lat, lon in (("borneo", 1.0, 113.6), ("png", -6.0, 140.5)):
        T(ax, *M6(lat, lon), tx(k), 13, WHITE, w="normal", alpha=.8)


def c06_go(ax):
    tw, ph, su = M6(22.0, 121.0), M6(16.0, 121.3), M6(-2.6, 119.2)
    curve(ax, tw, ph, bend=0.0, c=AMBER, lw=3.0, ls="-")
    curve(ax, ph, M6(6.5, 124.0), bend=0.0, c=AMBER, lw=3.0, ls="-", arrow=False)
    curve(ax, M6(6.5, 124.0), su, bend=0.08, c=AMBER, lw=3.0, ls="-")
    curve(ax, M6(6.5, 124.0), M6(-1.0, 147.0), bend=-0.10, c=BLUE, lw=2.4)
    T(ax, ph[0] + 0.05, ph[1] + 0.03, tx("k_phil"), 15, WHITE, ha="left")
    T(ax, ph[0] + 0.05, ph[1] - 0.03, tx("k_bp1"), 14, AMBER, ha="left")
    x, y = M6.dot(ax, -2.6, 119.2, c=AMBER, s=90)
    T(ax, x - 0.04, y + 0.03, tx("k_karama"), 14, WHITE, ha="right")
    T(ax, x - 0.04, y - 0.03, tx("k_bp2"), 14, AMBER, ha="right")
    T(ax, *M6(1.5, 143.0), tx("k_pac"), 16, BLUE)
    T(ax, 0.0, -0.74, tx("k_bring"), 17, WHITE)
    T(ax, 0.0, -0.81, tx("k_q"), 16, AMBER)
    T(ax, 0.0, -0.92, tx("c06_foot"), 11, GREY, w="normal")


# ══════════════════════ C-A26-07 這週末抬頭看（9:16 圖卡） ══════════════════════
def c07_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.947, tx("c07_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.907, tx("c07_sub"), fontproperties=FP, fontsize=14, color=GREY, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.880, 0.880], c=WHITE, lw=1.0, alpha=.4)
    y = 0.865
    for t, body, col in tx("c07_rows"):
        n = body.count("\n") + 1
        h = 0.036 + 0.034 * n
        ax.text(0.04, y - 0.030, t, fontproperties=FP, fontsize=13, color=col, ha="left", va="center",
                weight="bold")
        ax.text(0.34, y - 0.014 - 0.017 * n, body, fontproperties=FP, fontsize=12, color=WHITE, ha="left",
                va="center", linespacing=1.5)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.add_patch(CB.FancyBboxPatch((0.05, y - 0.090), 0.90, 0.060, boxstyle="round,pad=0.005,rounding_size=0.02",
                                   fc="#1B2240", ec=AMBER, lw=1.2))
    ax.text(0.5, y - 0.060, tx("c07_tip"), fontproperties=FP, fontsize=12.5, color=AMBER, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.068, tx("c07_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center",
            va="center")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    CB.emit("", [("地圖", c01_map), ("航線", c01_route)], title="C-A26-01_航線地圖")
    CB.emit("", [("港口", c02_ports), ("星路", c02_star)], title="C-A26-02_星羅盤")
    CB.emit("", [("距離", c03_dist)], title="C-A26-03_並肩的寡婦")
    CB.emit("", [("鄰居", c04_nb)], title="C-A26-04_天上的鄰居")
    f, ax = CB.newcard(dark=True)
    c05_card(ax)
    CB.save(f, "", "C-A26-05_同一個S形_圖卡.png", transparent=False)
    CB.emit("", [("台灣", c06_tw), ("擴散", c06_go)], title="C-A26-06_南島語族擴散")
    f, ax = CB.newcard(dark=True)
    c07_card(ax)
    CB.save(f, "", "C-A26-07_這週末抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
