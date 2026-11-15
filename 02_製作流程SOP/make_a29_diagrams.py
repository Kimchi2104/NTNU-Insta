# -*- coding: utf-8 -*-
"""A-29 薩丁尼亞：地中海島嶼的農牧星空｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A29-01 薩丁尼亞（地圖層、數字層）→ 02 鏡
C-A29-02 夏夜牧羊鐘（葡萄層、牧杖層、晨光層）→ 08 鏡
C-A29-07 吃晚飯的星（傍晚層、清晨層）→ 10 鏡（素材時新增：逐字稿原寫「疊金星圖示＋兩個名字」）
C-A29-03 賽馬之夜（地平層、爬升層）→ 14 鏡
C-A29-04 麥稈之路（9:16 圖卡）→ 17 鏡
C-A29-05 薩丁尼亞星名小辭典（9:16 圖卡）→ 18 鏡
C-A29-06 這週末抬頭看（9:16 圖卡；台北 2027/4/23 20:00）→ 19 鏡

做法：地圖是手描示意海岸線（經緯度大致對，非精確）；Sedilo 40.183°N 8.917°E；Barbagia＝Gennargentu 山區（範圍示意）。
羊與人：ISTAT 2024 年報告（綿羊約 307 萬）、人口 2023 年底約 157 萬。夏夜牧羊鐘、S'Ardia 之夜、這週末的星位一律
PyEphem 4.2.1 自算（含折射 1010 hPa、20°C；恆星 J2000）。不畫人物、不臨摹照片；pinnetu 與 S'Ardia 照片美宣另尋授權。

執行：python3 make_a29_diagrams.py            （中文，輸出 05_素材/A-29_薩丁尼亞/_概念圖/）
      python3 make_a29_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-29_薩丁尼亞/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND, SEA = "#FF6B6B", "#7C8BA8", "#2A3350", "#0E1A33"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "薩丁尼亞：地中海第二大島", "c01_sub": "手描示意，非精確海岸線",
        "italy": "義大利", "france": "法國", "spain": "西班牙", "africa": "北非", "corsica": "科西嘉",
        "sicily": "西西里（第一大）", "sardinia": "薩丁尼亞", "sea": "地中海", "tyr": "第勒尼安海",
        "inset": "放大", "sedilo": "Sedilo", "sedilo2": "這套星名用的方言",
        "barbagia": "Barbagia 山區", "c01_foot": "Sedilo 40.18°N 8.92°E；Barbagia 範圍示意",
        "num_title": "島上的羊，大約是人的兩倍",
        "sheep": "綿羊　約 307 萬頭", "people": "人　約 157 萬",
        "num_foot": "ISTAT 2024 年報告（綿羊）；人口 2023 年底；只算綿羊",
        "c02_title": "夏夜的牧羊鐘", "c02_sub": "Sedilo，8 月 16 日深夜到 17 日清晨・面向東方",
        "east": "東", "ene": "東北東", "ese": "東南東",
        "t1": "00:00", "t1b": "S'Udrone（昴宿）升起", "t2": "03:22", "t2b": "Sos Bacheddos 露臉（腰帶升起）",
        "t3": "04:55", "t3b": "天文晨光：參宿二 {:.0f}°、參宿六 {:.0f}°", "home": "→ 把羊趕回圈",
        "grape": "一串葡萄", "stick": "牧杖", "dawn": "天快亮",
        "c02_foot": "地平升起時刻（0°）；Sedilo 東邊是山，實際看見再晚一些。PyEphem 4.2.1 自算",
        "c02_src": "Bussu 2013：Barbagia 的牧人，看昴宿之後獵戶升起，就把夜牧的羊趕回圈",
        "c07_title": "金星也是時鐘", "eve": "傍晚・西方", "morn": "清晨・東方",
        "eve_n": "Isteddu Chenadorzu", "eve_zh": "吃晚飯的星", "eve_d": "chena＝晚餐",
        "morn_n": "S'Isteddu 'e Impuddile", "morn_zh": "晨星", "morn_d": "Stellarium 譯 Morning Star",
        "venus": "金星", "c07_foot": "這兩個名字只在新版 Stellarium 26.x（sardinian）",
        "c03_title": "S'Ardia 之夜", "c03_sub": "Sedilo，7 月 6 日深夜 → 7 日凌晨・面向東北",
        "c03_sub2": "日落 20:56、天全黑 22:58", "zenith": "頭頂", "ne": "東北",
        "at23": "23:00　天津四 {:.0f}°", "at02": "02:00　天津四 {:.0f}°", "almost": "快到頭頂",
        "town": "Sedilo", "legend": "傳說：君士坦丁看見的是白天、太陽上方的光十字",
        "legend2": "（Eusebius《君士坦丁傳》1.28）",
        "c03_foot": "PyEphem 4.2.1 自算（含折射）；十字星名與傳說的關係，資料沒有說",
        "c04_title": "麥稈之路", "c04_sub": "好多地方都說：銀河是一路灑落的麥稈",
        "c04_rows": [("薩丁尼亞", "Sa Via de sa Paza", "麥稈之路", AMBER),
                     ("土耳其", "Samanyolu", "麥稈路（saman 麥稈＋yol 路）", WHITE),
                     ("波斯", "Kahkashān", "拖麥稈的（路）", WHITE),
                     ("亞美尼亞", "Hardagoghi Chanaparh", "偷麥稈賊之路", WHITE)],
        "c04_src": "Bussu《L'incanto del cielo stellato》書介；ASE 作 s'andaina 'e paza",
        "c05_title": "薩丁尼亞星名小辭典", "c05_sub": "Sedilo 方言（Stellarium sardinian；Bussu、Puddu 的研究）",
        "c05_rows": [("Su Pinnetu", "牧人石屋", "畢宿 V＋畢宿五", AMBER),
                     ("S'Udrone", "一串葡萄", "昴宿（Barbagia：Su Gurdone）", PURPLE),
                     ("Sos Bacheddos", "牧杖", "獵戶", BLUE),
                     ("Sas Tres Marias", "三個瑪利亞", "獵戶腰帶", AMBER),
                     ("Su Trubadore de sos Bacheddos", "趕牧杖的人", "大犬（Bussu）", RED),
                     ("S'Isteddu de Atzarzu", "鋼鐵之星", "天狼星", WHITE),
                     ("Isteddu Chenadorzu", "吃晚飯的星", "傍晚的金星", WHITE),
                     ("S'Isteddu 'e Impuddile", "晨星", "清晨的金星", WHITE),
                     ("Sa Mandra", "羊圈", "御夫", GREEN),
                     ("Sa Frache", "鐮刀", "獅子座的鐮刀", GREEN),
                     ("Sos Sette Frades", "七兄弟", "北斗七星", AMBER),
                     ("Sa Rughe de Santu Antinu", "聖君士坦丁的十字", "天鵝", RED),
                     ("Su Ballu de sas Fiudas", "寡婦之舞", "北冕", PURPLE),
                     ("Su Corru 'e Chervu", "鹿角", "英仙", AMBER),
                     ("Sa Trona", "寶座", "仙后（片中沒講）", BLUE),
                     ("Sa Via de sa Paza", "麥稈之路", "銀河（Bussu）", WHITE)],
        "c05_note": "每個村子說法不同：Stellarium 的 Sa Frache，Bussu 書裡寫 Sa Farche",
        "c05_src": "Stellarium sardinian（Putzolu 2017）＋po/sc.po；Bussu 2023",
        "c06_title": "這週末抬頭看", "c06_sub": "台北，4 月 23 日（五）晚上 8 點",
        "N": "北", "E": "東", "S": "南", "W": "西", "zen": "頭頂",
        "sky_frache": "鐮刀", "sky_bro": "七兄弟", "sky_hut": "小屋", "sky_stick": "牧杖", "sky_dance": "寡婦之舞",
        "sky_fold": "羊圈", "mars": "火星", "jup": "木星",
        "c06_rows": [("19:39", "天全黑（天文昏影終）", WHITE),
                     ("頭頂", "Sa Frache 鐮刀（軒轅十四 {reg:.0f}°）", GREEN),
                     ("北方", "Sos Sette Frades 七兄弟（天樞 {dub:.0f}°）", AMBER),
                     ("西方", "小屋、牧杖：畢宿五 20:13、腰帶 20:40\n就低於 10°，天一黑就要看", BLUE),
                     ("東北東", "Su Ballu 寡婦之舞（貫索四 {alp:.0f}°）\n20:46 月出（93%）前看", PURPLE),
                     ("4/24 清晨", "04:50 後正東：金星（−3.8）\nS'Isteddu 'e Impuddile", WHITE)],
        "c06_tip": "週六、週日每晚提早約 4 分鐘",
        "c06_src": "PyEphem 4.2.1 自算（台北 25.03°N 121.57°E；含折射）",
    },
    "en": {
        "c01_title": "Sardinia: 2nd-largest Mediterranean island", "c01_sub": "Hand-drawn sketch, not exact coastlines",
        "italy": "Italy", "france": "France", "spain": "Spain", "africa": "North Africa", "corsica": "Corsica",
        "sicily": "Sicily (largest)", "sardinia": "Sardinia", "sea": "Mediterranean", "tyr": "Tyrrhenian Sea",
        "inset": "Zoom", "sedilo": "Sedilo", "sedilo2": "dialect of these star names",
        "barbagia": "Barbagia highlands", "c01_foot": "Sedilo 40.18°N 8.92°E; Barbagia extent schematic",
        "num_title": "About twice as many sheep as people",
        "sheep": "Sheep  ~3.07 million", "people": "People  ~1.57 million",
        "num_foot": "ISTAT 2024 report (sheep); population end of 2023; sheep only",
        "c02_title": "The shepherds' summer clock", "c02_sub": "Sedilo, night of 16–17 August · facing east",
        "east": "E", "ene": "ENE", "ese": "ESE",
        "t1": "00:00", "t1b": "S'Udrone (Pleiades) rises", "t2": "03:22", "t2b": "Sos Bacheddos appear (Belt rises)",
        "t3": "04:55", "t3b": "Dawn twilight: Alnilam {:.0f}°, Saiph {:.0f}°", "home": "→ bring the flock home",
        "grape": "the Bunch", "stick": "the Sticks", "dawn": "dawn",
        "c02_foot": "Times are 0° horizon risings; hills east of Sedilo delay them. Computed with PyEphem 4.2.1",
        "c02_src": "Bussu 2013: in Barbagia, when Orion rises after the Pleiades, the night flock goes back to the fold",
        "c07_title": "Venus is a clock too", "eve": "Evening · west", "morn": "Morning · east",
        "eve_n": "Isteddu Chenadorzu", "eve_zh": "the supper star", "eve_d": "chena = supper",
        "morn_n": "S'Isteddu 'e Impuddile", "morn_zh": "Morning Star", "morn_d": "Stellarium: Morning Star",
        "venus": "Venus", "c07_foot": "Both names only in the newer Stellarium 26.x (sardinian)",
        "c03_title": "The night of S'Ardia", "c03_sub": "Sedilo, late 6 July → early 7 July · facing NE",
        "c03_sub2": "Sunset 20:56, full dark 22:58", "zenith": "zenith", "ne": "NE",
        "at23": "23:00  Deneb {:.0f}°", "at02": "02:00  Deneb {:.0f}°", "almost": "nearly overhead",
        "town": "Sedilo", "legend": "Legend: Constantine saw a cross of light above the sun, by day",
        "legend2": "(Eusebius, Life of Constantine 1.28)",
        "c03_foot": "Computed with PyEphem 4.2.1 (with refraction); no source links the star name to the legend",
        "c04_title": "The Straw Road", "c04_sub": "In many lands the Milky Way is spilled straw",
        "c04_rows": [("Sardinia", "Sa Via de sa Paza", "the straw road", AMBER),
                     ("Turkey", "Samanyolu", "straw road (saman + yol)", WHITE),
                     ("Persia", "Kahkashān", "straw-dragger('s road)", WHITE),
                     ("Armenia", "Hardagoghi Chanaparh", "the straw thief's way", WHITE)],
        "c04_src": "Blurb of Bussu, L'incanto del cielo stellato; ASE: s'andaina 'e paza",
        "c05_title": "Sardinian star names", "c05_sub": "Sedilo dialect (Stellarium sardinian; research by Bussu, Puddu)",
        "c05_rows": [("Su Pinnetu", "shepherd's stone hut", "Hyades + Aldebaran", AMBER),
                     ("S'Udrone", "a bunch of grapes", "Pleiades (Barbagia: Su Gurdone)", PURPLE),
                     ("Sos Bacheddos", "the sticks", "Orion", BLUE),
                     ("Sas Tres Marias", "three Marys", "Orion's Belt", AMBER),
                     ("Su Trubadore de sos Bacheddos", "driver of the sticks", "Canis Major (Bussu)", RED),
                     ("S'Isteddu de Atzarzu", "steel star", "Sirius", WHITE),
                     ("Isteddu Chenadorzu", "supper star", "evening Venus", WHITE),
                     ("S'Isteddu 'e Impuddile", "morning star", "morning Venus", WHITE),
                     ("Sa Mandra", "the sheepfold", "Auriga", GREEN),
                     ("Sa Frache", "the sickle", "Sickle of Leo", GREEN),
                     ("Sos Sette Frades", "seven brothers", "Big Dipper", AMBER),
                     ("Sa Rughe de Santu Antinu", "St Constantine's cross", "Cygnus", RED),
                     ("Su Ballu de sas Fiudas", "dance of the widows", "Corona Borealis", PURPLE),
                     ("Su Corru 'e Chervu", "the deer's antler", "Perseus", AMBER),
                     ("Sa Trona", "the throne", "Cassiopeia (not in video)", BLUE),
                     ("Sa Via de sa Paza", "the straw road", "Milky Way (Bussu)", WHITE)],
        "c05_note": "Every village differs: Stellarium's Sa Frache is Sa Farche in Bussu",
        "c05_src": "Stellarium sardinian (Putzolu 2017) + po/sc.po; Bussu 2023",
        "c06_title": "Look up this weekend", "c06_sub": "Taipei, Fri 23 April, 8 pm",
        "N": "N", "E": "E", "S": "S", "W": "W", "zen": "zenith",
        "sky_frache": "Sickle", "sky_bro": "Brothers", "sky_hut": "Hut", "sky_stick": "Sticks", "sky_dance": "Widows",
        "sky_fold": "Fold", "mars": "Mars", "jup": "Jupiter",
        "c06_rows": [("19:39", "Full dark (end of astronomical twilight)", WHITE),
                     ("Overhead", "Sa Frache, the sickle (Regulus {reg:.0f}°)", GREEN),
                     ("North", "Sos Sette Frades (Dubhe {dub:.0f}°)", AMBER),
                     ("West", "Hut & Sticks: Aldebaran 20:13, Belt 20:40\nbelow 10° — look right after dark", BLUE),
                     ("ENE", "Su Ballu, widows' dance (Alphecca {alp:.0f}°)\nbefore moonrise 20:46 (93%)", PURPLE),
                     ("24 Apr dawn", "After 04:50, due east: Venus (−3.8)\nS'Isteddu 'e Impuddile", WHITE)],
        "c06_tip": "Sat & Sun: about 4 minutes earlier each night",
        "c06_src": "Computed with PyEphem 4.2.1 (Taipei 25.03°N 121.57°E; with refraction)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 天象 ══════════════════════
_S = None


def stars():
    global _S
    if _S is None:
        _S = G.load_stars(BASE)
    return _S


def obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


def altaz(h, o):
    import ephem
    S = stars()
    s = ephem.FixedBody(); s._ra, s._dec = math.radians(S[h][0]), math.radians(S[h][1]); s._epoch = ephem.J2000
    s.compute(o)
    return math.degrees(s.alt), math.degrees(s.az)


SED = (40.183, 8.917)
TPE = (25.0330, 121.5654)
PLEI = [17851, 17847, 17702, 17573, 17531, 17499, 17608]
STICK = [[27989, 26207, 25336, 25930, 24436, 27366, 26727, 27989]]
BELT = [26727, 26311, 25930]
CROSS = [[102098, 100453, 98110, 95947], [102488, 100453, 97165]]


# ══════════════════════ C-A29-01 薩丁尼亞 ══════════════════════
SARD = [(41.25, 9.23), (41.12, 9.52), (40.92, 9.70), (40.55, 9.80), (40.25, 9.65), (39.85, 9.70), (39.40, 9.62),
        (39.12, 9.52), (39.20, 9.10), (38.90, 8.85), (38.86, 8.64), (39.05, 8.40), (39.40, 8.42), (39.70, 8.45),
        (39.90, 8.55), (40.25, 8.47), (40.55, 8.30), (40.90, 8.20), (41.07, 8.25), (40.92, 8.60), (41.05, 8.90),
        (41.22, 9.10)]
CORS = [(43.00, 9.40), (42.70, 9.45), (42.30, 9.55), (41.90, 9.40), (41.60, 9.30), (41.38, 9.20), (41.60, 8.80),
        (41.90, 8.62), (42.25, 8.60), (42.55, 8.75), (42.70, 9.10)]
SICI = [(38.25, 15.62), (37.50, 15.10), (36.68, 15.08), (36.95, 14.40), (37.30, 13.55), (37.60, 12.60),
        (38.05, 12.55), (38.12, 13.36), (38.03, 14.00)]
EUROPE = [(50.0, -1.0), (43.4, -1.8), (43.3, 3.3), (42.5, 3.15), (41.38, 2.17), (40.6, 0.6), (39.47, -0.35),
          (38.75, 0.20), (37.6, -0.98), (36.72, -4.42), (36.0, -5.6), (36.0, -7.0), (50.0, -7.0)]
FRIT = [(50.0, -1.0), (43.4, -1.8), (43.3, 3.3), (43.5, 4.0), (43.30, 5.37), (43.10, 6.0), (43.55, 7.0),
        (43.78, 7.53), (44.40, 8.93), (44.10, 9.82), (43.55, 10.30), (42.93, 10.50), (42.40, 11.20),
        (42.09, 11.80), (41.70, 12.30), (41.25, 13.10), (40.83, 14.25), (40.40, 14.95), (40.00, 15.65),
        (39.40, 16.05), (38.90, 16.20), (38.20, 15.65), (37.95, 16.05), (38.45, 16.55), (38.95, 17.15),
        (39.50, 17.05), (40.05, 16.60), (40.45, 17.20), (39.85, 18.37), (40.20, 18.50), (40.65, 17.95),
        (41.15, 16.85), (41.60, 15.95), (41.95, 15.70), (42.40, 14.40), (43.60, 13.50), (44.10, 12.40),
        (45.20, 12.35), (45.65, 13.75), (45.3, 14.3), (44.2, 15.3), (43.0, 17.0), (42.0, 19.0), (41.3, 19.5),
        (40.0, 19.9), (39.0, 20.5), (38.0, 21.2), (37.0, 21.6), (36.5, 22.5), (50.0, 24.0)]
AFR = [(35.8, -5.9), (35.2, -2.9), (35.7, -0.6), (36.75, 3.05), (36.9, 7.75), (37.25, 9.85), (37.05, 11.05),
       (36.4, 10.6), (35.8, 10.8), (34.7, 10.75), (33.5, 10.9), (32.9, 13.2), (32.3, 15.3), (31.0, 17.5),
       (30.5, 19.5), (27.0, 25.0), (27.0, -7.0)]
LANDS1 = [EUROPE, FRIT, AFR, SICI, CORS]
LON0, LAT0, SC1 = 11.5, 39.4, 0.088
CLIP1 = (-1.0, 1.0, -0.80, 0.80)
COS40 = math.cos(math.radians(40))


def m1(lat, lon):
    return (lon - LON0) * SC1 * COS40, (lat - LAT0) * SC1


def lands(ax, polys, f, clip, fc=LAND, ec=GREY, z=2):
    from matplotlib.patches import Rectangle
    rect = Rectangle((clip[0], clip[2]), clip[1] - clip[0], clip[3] - clip[2], transform=ax.transData)
    for poly in polys:
        p = CB.Polygon([f(*q) for q in poly], closed=True, fc=fc, ec=ec, lw=1.3, zorder=z)
        ax.add_patch(p); p.set_clip_path(rect)


INS1 = (-0.97, -0.34, -0.40, 0.66)        # 放大框（x0, y0, x1, y1）：薩丁尼亞（蓋在法國—西班牙上）
IC, ISC = (40.05, 9.0), 0.27


def mi(lat, lon):
    x0, y0, x1, y1 = INS1
    return ((x0 + x1) / 2 + (lon - IC[1]) * ISC * COS40, 0.23 + (lat - IC[0]) * ISC)


def c01_map(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 28, WHITE)
    T(ax, 0.0, 0.855, tx("c01_sub"), 14, GREY, w="normal")
    lands(ax, LANDS1, m1, CLIP1)
    lands(ax, [SARD], m1, CLIP1, fc=AMBER, ec=AMBER, z=3)
    for k, lat, lon, fs, c in (("italy", 42.6, 13.6, 16, GREY), ("africa", 33.3, 1.5, 16, GREY),
                               ("corsica", 42.2, 10.6, 12, GREY), ("sicily", 36.3, 14.0, 12, GREY),
                               ("sea", 36.5, 19.0, 16, BLUE), ("tyr", 39.6, 12.6, 11, BLUE),
                               ("france", 46.5, 12.0, 14, GREY)):
        T(ax, *m1(lat, lon), tx(k), fs, c, w="normal")
    sx, sy = m1(40.1, 9.75)
    T(ax, sx + 0.04, sy + 0.10, tx("sardinia"), 15, AMBER, ha="left")
    x0, y0, x1, y1 = INS1
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.03",
                                   fc="#10172E", ec=AMBER, lw=1.4, zorder=8))
    lx, ly = m1(40.1, 8.2)
    ax.plot([lx, x1], [ly, 0.23], c=AMBER, lw=1.0, alpha=.6, zorder=7, ls=(0, (4, 3)))
    T(ax, x0 + 0.03, y1 - 0.045, tx("inset"), 12, GREY, w="normal", ha="left", z=13)
    ax.add_patch(CB.Polygon([mi(*q) for q in SARD], closed=True, fc=LAND, ec=AMBER, lw=1.6, zorder=9))
    bx, by = mi(40.02, 9.30)
    ax.add_patch(CB.Ellipse((bx, by), 0.15, 0.12, fc=GREEN, ec=GREEN, alpha=.30, lw=1.2, zorder=10))
    dx, dy = mi(*SED)
    ax.scatter([dx], [dy], s=420, c=PURPLE, alpha=.25, zorder=11, lw=0)
    ax.scatter([dx], [dy], s=80, c=PURPLE, zorder=12, lw=0)
    xm = (x0 + x1) / 2
    ax.plot([dx, xm - 0.12], [dy, y0 + 0.155], c=PURPLE, lw=0.9, alpha=.7, zorder=12)
    ax.plot([bx, xm + 0.12], [by - 0.06, y0 + 0.155], c=GREEN, lw=0.9, alpha=.7, zorder=12)
    T(ax, xm - 0.12, y0 + 0.125, tx("sedilo"), 14, PURPLE, z=13)
    T(ax, xm - 0.12, y0 + 0.08, tx("sedilo2"), 9.5, PURPLE, w="normal", z=13)
    T(ax, xm + 0.13, y0 + 0.125, tx("barbagia"), 12, GREEN, z=13)
    T(ax, 0.0, -0.93, tx("c01_foot"), 11, GREY, w="normal")


def sheep(ax, x, y, s=0.05, c=WHITE):
    ax.add_patch(CB.Ellipse((x, y), 1.6 * s, 1.0 * s, fc=c, ec="none", zorder=12))
    ax.add_patch(CB.Ellipse((x - 0.85 * s, y + 0.15 * s), 0.55 * s, 0.42 * s, fc=GREY, ec="none", zorder=12))
    for d in (-0.45, 0.45):
        ax.plot([x + d * s, x + d * s], [y - 0.4 * s, y - 0.85 * s], c=GREY, lw=2.0, zorder=11)


def person(ax, x, y, s=0.05, c=AMBER):
    ax.add_patch(CB.Circle((x, y + 0.55 * s), 0.25 * s, fc=c, ec="none", zorder=12))
    ax.add_patch(CB.FancyBboxPatch((x - 0.30 * s, y - 0.75 * s), 0.6 * s, 1.0 * s,
                                   boxstyle="round,pad=0.0,rounding_size=0.008", fc=c, ec="none", zorder=12))


def c01_num(ax):
    x0, y0, x1, y1 = -0.14, -0.84, 0.96, -0.36
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.03",
                                   fc="#10172E", ec=WHITE, lw=1.0, alpha=1.0, zorder=10))
    T(ax, (x0 + x1) / 2, y1 - 0.06, tx("num_title"), 15, WHITE, z=13)
    for i in range(6):                                 # 1 隻＝約 50 萬
        sheep(ax, x0 + 0.10 + i * 0.105, -0.55)
    for i in range(3):
        person(ax, x0 + 0.10 + i * 0.105, -0.71)
    T(ax, x0 + 0.72, -0.55, tx("sheep"), 13, WHITE, ha="left", z=13)
    T(ax, x0 + 0.72, -0.71, tx("people"), 13, AMBER, ha="left", z=13)
    T(ax, (x0 + x1) / 2, y0 + 0.035, tx("num_foot"), 9.5, GREY, w="normal", z=13)


# ══════════════════════ C-A29-02 夏夜牧羊鐘 ══════════════════════
AZ0, AZ1, SC2, HY2 = 45.0, 125.0, 0.021, -0.42


def p2(alt, az):
    return -0.84 + (az - AZ0) * SC2, HY2 + alt * SC2


def sky2(when):
    o = obs(*SED, 2, when)
    return {h: altaz(h, o) for h in set(PLEI + BELT + [h for s in STICK for h in s])}


def draw_plei(ax, P, alpha=1.0):
    for h in PLEI:
        x, y = p2(*P[h])
        ax.scatter([x], [y], s=26, c=WHITE, alpha=alpha, zorder=8, lw=0)
    x, y = p2(*P[17702])
    ax.scatter([x], [y], s=900, c=PURPLE, alpha=.18 * alpha, zorder=7, lw=0)


def draw_orion(ax, P, alpha=1.0):
    for seg in STICK:
        pts = [p2(*P[h]) for h in seg]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            ax.plot([xa, xb], [ya, yb], c=BLUE, lw=2.2, alpha=.9 * alpha, zorder=6,
                    ls="-" if min(ya, yb) >= HY2 else (0, (3, 3)))
    for h in set(h for s in STICK for h in s) | set(BELT):
        x, y = p2(*P[h])
        if y >= HY2 - 0.01:
            ax.scatter([x], [y], s=40, c=WHITE, alpha=alpha, zorder=8, lw=0)


def timeline2(ax, hl):
    y = -0.70
    ax.plot([-0.80, 0.80], [y, y], c=WHITE, lw=1.4, alpha=.4, zorder=3)
    for i, (k, x, c) in enumerate((("t1", -0.70, PURPLE), ("t2", 0.0, BLUE), ("t3", 0.70, AMBER))):
        on = i <= hl
        ax.scatter([x], [y], s=150 if on else 70, c=c if on else GREY, zorder=6, lw=0)
        if on:                                     # 之後的時刻由各層自己寫（疊層時才不會兩個字重影）
            T(ax, x, y - 0.06, tx(k), 15, c)


def c02_grape(ax):
    T(ax, 0.0, 0.92, tx("c02_title"), 30, WHITE)
    T(ax, 0.0, 0.855, tx("c02_sub"), 14, GREY, w="normal")
    ax.add_patch(CB.Rectangle((-0.84, HY2 - 0.22), 1.68, 0.22, fc=SEA, ec="none", zorder=4))
    ax.plot([-0.84, 0.84], [HY2, HY2], c=WHITE, lw=1.6, alpha=.7, zorder=5)
    for a in (10, 20, 30, 40, 50):
        ax.plot([-0.84, 0.84], [HY2 + a * SC2] * 2, c=WHITE, lw=0.6, alpha=.12, zorder=3)
        T(ax, -0.86, HY2 + a * SC2, f"{a}°", 9, GREY, ha="right", w="normal")
    for az, k in ((67.5, "ene"), (90.0, "east"), (112.5, "ese")):
        T(ax, p2(0, az)[0], HY2 - 0.05, tx(k), 12, GREY, w="normal", z=13)
    P = sky2("2027/8/17 00:00")
    draw_plei(ax, P)
    x, y = p2(*P[17702])
    T(ax, x + 0.02, y + 0.13, tx("t1b"), 13, PURPLE, ha="left")
    timeline2(ax, 0)
    T(ax, 0.0, -0.93, tx("c02_foot"), 10.5, GREY, w="normal")


def c02_stick(ax):
    P0, P1 = sky2("2027/8/17 00:00"), sky2("2027/8/17 03:22")
    a, b = p2(*P0[17702]), p2(*P1[17702])
    ax.plot([a[0], b[0]], [a[1], b[1]], c=PURPLE, lw=1.2, alpha=.5, ls=(0, (2, 4)), zorder=5)
    draw_plei(ax, P1, alpha=.8)
    draw_orion(ax, P1)
    x, y = p2(*P1[26311])
    T(ax, x - 0.02, y + 0.10, tx("t2b"), 13, BLUE, ha="center")
    ax.scatter([0.0], [-0.70], s=150, c=BLUE, zorder=7, lw=0)
    T(ax, 0.0, -0.76, tx("t2"), 15, BLUE)


def c02_dawn(ax):
    for i, a in enumerate((.20, .14, .09, .05)):
        ax.add_patch(CB.Rectangle((-0.84, HY2), 1.68, 0.06 * (i + 1), fc=AMBER, ec="none", alpha=a, zorder=2))
    P1, P2 = sky2("2027/8/17 03:22"), sky2("2027/8/17 04:55")
    draw_orion(ax, P2)
    draw_plei(ax, P2)
    a, b = p2(*P1[26311]), p2(*P2[26311])
    ax.plot([a[0], b[0]], [a[1], b[1]], c=BLUE, lw=1.2, alpha=.5, ls=(0, (2, 4)), zorder=5)
    al, sa = P2[26311][0], P2[27366][0]
    x, y = p2(*P2[27989])
    T(ax, 0.45, 0.52, tx("t3b").format(al, sa), 13.5, AMBER)
    T(ax, 0.45, 0.45, tx("home"), 17, AMBER)
    ax.scatter([0.70], [-0.70], s=150, c=AMBER, zorder=7, lw=0)
    T(ax, 0.70, -0.76, tx("t3"), 15, AMBER)
    T(ax, 0.0, -0.86, tx("c02_src"), 10.5, WHITE, w="normal", alpha=.85)


# ══════════════════════ C-A29-07 吃晚飯的星 ══════════════════════
def venus(ax, x, y):
    ax.scatter([x], [y], s=1600, c=WHITE, alpha=.10, zorder=6, lw=0)
    ax.scatter([x], [y], s=450, c="#FFF6D8", alpha=.25, zorder=6, lw=0)
    ax.scatter([x], [y], s=110, c=WHITE, zorder=7, lw=0)


def half(ax, x0, x1, key, col, sun_left):
    hy = -0.12
    xc = (x0 + x1) / 2
    T(ax, xc, 0.68, tx(key), 16, GREY, w="normal")
    for r, a in ((0.30, .08), (0.20, .12), (0.12, .18)):
        ax.add_patch(CB.Circle((xc + (-0.18 if sun_left else 0.18), hy - 0.05), r, fc=AMBER, ec="none",
                               alpha=a, zorder=3))
    ridge = [(x0, hy - 0.01), (x0 + 0.20, hy + 0.06), (x0 + 0.36, hy + 0.02), (x0 + 0.55, hy + 0.08),
             (x1, hy), (x1, hy - 0.36), (x0, hy - 0.36)]
    ax.add_patch(CB.Polygon(ridge, closed=True, fc="#1F2A44", ec=GREY, lw=1.3, zorder=4))
    venus(ax, xc + (0.10 if sun_left else -0.10), hy + 0.26)
    T(ax, xc + (0.10 if sun_left else -0.10), hy + 0.35, tx("venus"), 12, WHITE, w="normal")
    k = "eve" if key == "eve" else "morn"
    T(ax, xc, 0.52, tx(k + "_n"), 17, col)
    T(ax, xc, 0.44, tx(k + "_zh"), 19, WHITE)
    T(ax, xc, -0.60, tx(k + "_d"), 13, WHITE, w="normal")


def c07_eve(ax):
    T(ax, 0.0, 0.88, tx("c07_title"), 30, WHITE)
    half(ax, -0.94, -0.04, "eve", AMBER, sun_left=True)


def c07_morn(ax):
    half(ax, 0.04, 0.94, "morn", BLUE, sun_left=False)
    T(ax, 0.0, -0.82, tx("c07_foot"), 11.5, GREY, w="normal")


# ══════════════════════ C-A29-03 賽馬之夜 ══════════════════════
AZC3, SC3, ZY3 = 62.0, 0.0150, 0.60            # 以頭頂為心的等距圖；東北方朝下


def p3(alt, az):
    r = (90.0 - alt) * SC3
    a = math.radians(az - AZC3)
    return -r * math.sin(a), ZY3 - r * math.cos(a)


def cross3(ax, when, alpha, lw):
    o = obs(*SED, 2, when)
    P = {h: altaz(h, o) for s in CROSS for h in s}
    for seg in CROSS:
        pts = [p3(*P[h]) for h in seg]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=RED, lw=lw, alpha=alpha, zorder=7)
    for h in P:
        x, y = p3(*P[h])
        ax.scatter([x], [y], s=55 if h == 102098 else 30, c=WHITE, alpha=alpha, zorder=8, lw=0)
    return P


def c03_ground(ax):
    T(ax, 0.0, 0.93, tx("c03_title"), 30, WHITE)
    T(ax, 0.0, 0.865, tx("c03_sub"), 14, GREY, w="normal")
    T(ax, 0.0, 0.815, tx("c03_sub2"), 12, GREY, w="normal")
    from matplotlib.patches import Rectangle
    clip = Rectangle((-0.95, -0.95), 1.9, 1.70, transform=ax.transData)
    R = 90 * SC3
    for alt in (30, 60):
        c = CB.Circle((0, ZY3), (90 - alt) * SC3, fc="none", ec=WHITE, lw=0.6, alpha=.15, zorder=3)
        ax.add_patch(c); c.set_clip_path(clip)
    ax.scatter([0], [ZY3], s=30, c=GREY, zorder=5, lw=0)
    T(ax, 0.06, ZY3, tx("zenith"), 11, GREY, ha="left", w="normal")
    hz = CB.Circle((0, ZY3), R, fc="none", ec=WHITE, lw=1.6, alpha=.7, zorder=5)
    ax.add_patch(hz); hz.set_clip_path(clip)
    # 地面（地平圈外）＋小鎮剪影（東北方地平附近）
    import numpy as np
    th = np.linspace(-math.pi, math.pi, 361)
    ring = [(R * math.sin(t), ZY3 - R * math.cos(t)) for t in th]
    outer = [(1.4 * math.sin(t), ZY3 - 1.4 * math.cos(t)) for t in th[::-1]]
    g = CB.Polygon(ring + outer, closed=True, fc="#141A2C", ec="none", zorder=4)
    ax.add_patch(g); g.set_clip_path(clip)
    by = ZY3 - R
    for x, w, h in ((-0.30, 0.10, 0.06), (-0.18, 0.08, 0.05), (0.12, 0.09, 0.055), (0.24, 0.07, 0.045)):
        ax.add_patch(CB.Rectangle((x, by - 0.005 + abs(x) * 0.01), w, h, fc="#2A3350", ec=GREY, lw=0.8, zorder=6))
    ax.add_patch(CB.Rectangle((-0.04, by), 0.08, 0.10, fc="#2A3350", ec=GREY, lw=0.8, zorder=6))
    ax.add_patch(CB.Polygon([(-0.05, by + 0.10), (0.0, by + 0.16), (0.05, by + 0.10)], closed=True,
                            fc="#2A3350", ec=GREY, lw=0.8, zorder=6))
    T(ax, 0.0, by - 0.06, tx("town") + "・" + tx("ne"), 13, WHITE, w="normal", z=13)
    P = cross3(ax, "2027/7/6 23:00", .55, 2.2)
    x, y = p3(*P[102098])
    T(ax, x + 0.05, y - 0.04, tx("at23").format(P[102098][0]), 13, RED, ha="left", alpha=.8)
    T(ax, 0.0, -0.93, tx("c03_foot"), 10.5, GREY, w="normal")


def c03_rise(ax):
    import ephem
    pts = [None] * 13
    for i in range(13):                                  # 天津四 23:00→02:00 每 15 分鐘
        o = obs(*SED, 2, "2027/7/6 23:00")
        o.date = ephem.Date(o.date + i * 0.25 * ephem.hour)
        pts[i] = p3(*altaz(102098, o))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=WHITE, lw=1.4, alpha=.6, ls=(0, (3, 3)), zorder=6)
    CB.arrow(ax, pts[-1], pts[-3], c=WHITE, lw=1.6, alpha=.8, style="-|>")
    P = cross3(ax, "2027/7/7 02:00", 1.0, 3.2)
    x, y = p3(*P[102098])
    T(ax, x + 0.05, y + 0.02, tx("at02").format(P[102098][0]), 15, RED, ha="left")
    T(ax, x + 0.05, y - 0.04, tx("almost"), 12, RED, ha="left", w="normal")
    T(ax, 0.0, -0.42, tx("legend"), 12.5, AMBER, w="normal")
    T(ax, 0.0, -0.47, tx("legend2"), 10.5, AMBER, w="normal")


# ══════════════════════ C-A29-04 麥稈之路（9:16） ══════════════════════
def c04_card(ax):
    import random
    FP = CB.FP
    rnd = random.Random(29)
    for i in range(900):                              # 斜向銀河帶：一根根麥稈
        t = rnd.random()
        x = -0.1 + 1.2 * t
        y = 0.92 - 0.55 * t + rnd.gauss(0, 0.045)
        a = math.radians(rnd.uniform(0, 180))
        l = rnd.uniform(0.006, 0.018)
        ax.plot([x - l * math.cos(a), x + l * math.cos(a)], [y - l * math.sin(a) * 0.56, y + l * math.sin(a) * 0.56],
                c=AMBER if rnd.random() < 0.35 else CB.MW, lw=0.9, alpha=rnd.uniform(.15, .45), zorder=0.5)
    ax.text(0.5, 0.950, tx("c04_title"), fontproperties=FP, fontsize=32, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.912, tx("c04_sub"), fontproperties=FP, fontsize=13, color=GREY, ha="center", va="center")
    y = 0.60
    for place, nat, zh, c in tx("c04_rows"):
        hl = c == AMBER
        ax.add_patch(CB.FancyBboxPatch((0.06, y - 0.055), 0.88, 0.105, boxstyle="round,pad=0.0,rounding_size=0.015",
                                       fc="#1B2240" if hl else "#121933", ec=c, lw=1.4 if hl else 0.6, alpha=1.0, zorder=3))
        ax.text(0.10, y + 0.022, place, zorder=4, fontproperties=FP, fontsize=13, color=GREY, ha="left", va="center")
        ax.text(0.10, y - 0.018, nat, zorder=4, fontproperties=FP, fontsize=17 if hl else 15, color=c, ha="left",
                va="center", weight="bold")
        ax.text(0.90, y - 0.018, zh, zorder=4, fontproperties=FP, fontsize=13.5, color=WHITE, ha="right", va="center")
        y -= 0.13
    ax.text(0.5, 0.068, tx("c04_src"), fontproperties=FP, fontsize=8.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A29-05 星名小辭典（9:16） ══════════════════════
def c05_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.950, tx("c05_title"), fontproperties=FP, fontsize=27, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.913, tx("c05_sub"), fontproperties=FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.plot([0.04, 0.96], [0.892, 0.892], c=WHITE, lw=1.0, alpha=.4)
    y, dy = 0.862, 0.0455
    for nat, zh, west, c in tx("c05_rows"):
        ax.text(0.05, y + 0.009, nat, fontproperties=FP, fontsize=11.5, color=c, ha="left", va="center",
                weight="bold")
        ax.text(0.05, y - 0.012, west, fontproperties=FP, fontsize=8.8, color=GREY, ha="left", va="center")
        ax.text(0.95, y, zh, fontproperties=FP, fontsize=13, color=WHITE, ha="right", va="center")
        y -= dy
        ax.plot([0.04, 0.96], [y + dy / 2, y + dy / 2], c=WHITE, lw=0.5, alpha=.15)
    ax.text(0.5, y - 0.005, tx("c05_note"), fontproperties=FP, fontsize=10, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.068, tx("c05_src"), fontproperties=FP, fontsize=8.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center", va="center")


# ══════════════════════ C-A29-06 這週末抬頭看（9:16） ══════════════════════
SKYLINES = {  # 連線、顏色、標籤 key
    "frache": ([[49669, 49583, 50583, 50335, 48455, 47908]], GREEN, "sky_frache"),
    "bro": ([[67301, 65378, 62956, 59774, 58001, 53910, 54061, 59774]], AMBER, "sky_bro"),
    "hut": ([[20889, 20648, 20455, 20205, 20885, 21421, 20889]], AMBER, "sky_hut"),
    "stick": (STICK, BLUE, "sky_stick"),
    "fold": ([[25428, 28380, 28360, 24608, 23453, 23015, 25428]], GREEN, "sky_fold"),
    "dance": ([[76127, 75695, 76267, 76952, 77512, 78159, 78493]], PURPLE, "sky_dance"),
}
LBL6 = {"frache": (-0.06, 0.0), "bro": (0.0, 0.035), "hut": (0.0, -0.03), "stick": (-0.045, 0.0),
        "fold": (0.0, 0.03), "dance": (-0.02, 0.035)}


def c06_card(ax):
    import ephem
    FP = CB.FP
    S = stars()
    o = obs(*TPE, 8, "2027/4/23 20:00")
    CX, CY, R = 0.5, 0.665, 0.40 * 9 / 16 / (9 / 16)       # 圓心（軸座標）；x 方向 R、y 方向 R·9/16
    rx, ry = 0.38, 0.38 * 9 / 16

    def pp(alt, az):                                     # 頭頂等距；北上、東左（抬頭看）
        r = (90 - alt) / 90
        a = math.radians(az)
        return CX - r * rx * math.sin(a), CY + r * ry * math.cos(a)
    ax.text(0.5, 0.955, tx("c06_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center", va="center",
            weight="bold")
    ax.text(0.5, 0.920, tx("c06_sub"), fontproperties=FP, fontsize=14, color=GREY, ha="center", va="center")
    ax.add_patch(CB.Ellipse((CX, CY), 2 * rx, 2 * ry, fc="#10172E", ec=WHITE, lw=1.4, alpha=1.0, zorder=1))
    for alt in (30, 60):
        f = (90 - alt) / 90
        ax.add_patch(CB.Ellipse((CX, CY), 2 * rx * f, 2 * ry * f, fc="none", ec=WHITE, lw=0.5, alpha=.15, zorder=2))
    for h, (ra, dec, v) in S.items():
        if v > 4.3:
            continue
        al, az = altaz(h, o)
        if al < 0:
            continue
        x, y = pp(al, az)
        ax.scatter([x], [y], s=max(0.6, (5.0 - v)) ** 1.8 * 1.6, c=WHITE, alpha=.85, zorder=4, lw=0)
    for k, (segs, c, lk) in SKYLINES.items():
        allp = []
        for seg in segs:
            pts = [(altaz(h, o)) for h in seg]
            xy = [pp(*p) for p in pts]
            for (a, b), (pa, pb) in zip(zip(xy, xy[1:]), zip(pts, pts[1:])):
                if pa[0] < 0 or pb[0] < 0:
                    continue
                ax.plot([a[0], b[0]], [a[1], b[1]], c=c, lw=1.6, alpha=.95, zorder=5)
            allp += [q for q, p in zip(xy, pts) if p[0] >= 0]
        if allp:
            mx = sum(p[0] for p in allp) / len(allp) + LBL6[k][0]
            my = sum(p[1] for p in allp) / len(allp) + LBL6[k][1]
            ax.text(mx, my, tx(lk), fontproperties=FP, fontsize=11, color=c, ha="center", va="center",
                    weight="bold", zorder=7)
    for body, k, c in ((ephem.Mars(), "mars", "#FF8A6B"), (ephem.Jupiter(), "jup", "#FFF3D6")):
        body.compute(o)
        x, y = pp(math.degrees(body.alt), math.degrees(body.az))
        ax.scatter([x], [y], s=40, c=c, zorder=6, lw=0)
        ax.text(x, y - 0.014, tx(k), fontproperties=FP, fontsize=8.5, color=c, ha="center", va="center", zorder=7)
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = pp(-7, az)
        ax.text(x, y, tx(k), fontproperties=FP, fontsize=14, color=AMBER, ha="center", va="center", weight="bold")
    reg, dub, alp = altaz(49669, o)[0], altaz(54061, o)[0], altaz(76267, o)[0]
    y = 0.418
    for t, body, col in tx("c06_rows"):
        body = body.format(reg=reg, dub=dub, alp=alp)
        n = body.count("\n") + 1
        h = 0.014 + 0.021 * n
        ax.text(0.05, y - h / 2, t, fontproperties=FP, fontsize=11.5, color=col, ha="left", va="center",
                weight="bold")
        ax.text(0.30, y - h / 2, body, fontproperties=FP, fontsize=11, color=WHITE, ha="left", va="center",
                linespacing=1.45)
        y -= h
        ax.plot([0.04, 0.96], [y, y], c=WHITE, lw=0.5, alpha=.18)
    ax.text(0.5, y - 0.020, tx("c06_tip"), fontproperties=FP, fontsize=10.5, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.068, tx("c06_src"), fontproperties=FP, fontsize=8.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center", va="center")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    CB.emit("", [("地圖", c01_map), ("數字", c01_num)], title="C-A29-01_薩丁尼亞")
    CB.emit("", [("葡萄", c02_grape), ("牧杖", c02_stick), ("晨光", c02_dawn)], title="C-A29-02_夏夜牧羊鐘")
    CB.emit("", [("傍晚", c07_eve), ("清晨", c07_morn)], title="C-A29-07_吃晚飯的星")
    CB.emit("", [("地平", c03_ground), ("爬升", c03_rise)], title="C-A29-03_賽馬之夜")
    for fn, name in ((c04_card, "C-A29-04_麥稈之路"), (c05_card, "C-A29-05_薩丁尼亞星名小辭典"),
                     (c06_card, "C-A29-06_這週末抬頭看")):
        f, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(f, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
