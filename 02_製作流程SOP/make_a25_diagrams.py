# -*- coding: utf-8 -*-
"""A-25 圖皮-瓜拉尼：1614 年傳教士抄下的星空｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A25-01 馬拉尼昂島（地圖、航線）→ 02 鏡
C-A25-02 1614年的書（扉頁 → 03 鏡；原文 fol. 316r → 04 鏡）
C-A25-03 二十八個名字（名單、九個 → 05 鏡；結尾原文 fol. 319v、問號 → 06 鏡）
C-A25-04 兩千五百公里（地圖、時間軸）→ 07 鏡
C-A25-05 昴宿與雨（原文 fol. 320v、年環）→ 13 鏡
C-A25-06 這週末抬頭看（9:16 圖卡，可存圖；台北 2027/3/12–14、墾丁 3/13 凌晨）→ 17 鏡

做法：地圖是手描示意輪廓（海岸線取幾十個經緯度點連起來，非精確國界）。原書頁面＝
07_資料來源/Tupi-Guarani in America/histoiredelamiss00clau.pdf（Internet Archive 掃描；1614 年出版物＝公有領域），
用 pdftoppm 現場轉圖裁切，框線位置取 PDF 文字層的字框（pdftotext -bbox）。不畫人物肖像、不臨摹出版的復原圖。
28 個名字照原書順序與拼法（ſ 改 s），中譯照逐字稿星名表 A。

執行：python3 make_a25_diagrams.py            （中文，輸出 05_素材/A-25_圖皮瓜拉尼/_概念圖/）
      python3 make_a25_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math, re, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-25_圖皮瓜拉尼/_概念圖")
PDF = os.path.join(BASE, "07_資料來源/Tupi-Guarani in America/histoiredelamiss00clau.pdf")
CB.set_base(OUT)
RED, GREY, LAND, SEA_LINE, ORANGE = "#FF6B6B", "#7C8BA8", "#2A3350", "#4F86C6", "#FF9F43"
LANG = "zh"

# 原書 28 個名字（順序、拼法照 fol. 316v–319v）；hi＝05 鏡亮起的順序（0＝不亮）、big＝放大
NAMES = [
    ("Simbiare raieuboire", 1, 0), ("Ouroubou", 0, 0), ("Seichou-ioura", 2, 1), ("Seycou", 0, 0),
    ("Tingassou", 0, 0), ("Souanran", 0, 0), ("Ouégnonmoin", 3, 1), ("Iaouare", 0, 0),
    ("Yasseuhtata Ouassou", 0, 0), ("Pira-panen", 0, 0), ("Yapouykan", 0, 0), ("Crussa", 0, 0),
    ("Yanday", 0, 0), ("Yassatin", 0, 0), ("Cay", 4, 1), ("Potin", 5, 0),
    ("Tuyvaé", 0, 0), ("Conomy Manipoère Ouaré", 9, 1), ("Yandoutin", 0, 0), ("Ouyra-Oupia", 0, 0),
    ("Eyre apouâ", 7, 0), ("Pannacon", 6, 0), ("Yasseuh tata oué", 0, 0), ("Tapity", 0, 0),
    ("Toucon", 0, 0), ("Tataendeuh", 8, 0), ("Gnaepouëon", 0, 0), ("Carana yue", 0, 0),
]
assert len(NAMES) == 28
KNOWN = {3: "昴宿", 8: "晨星", 11: "十字"}          # 書上直接說出是哪顆的（index → 中文）
KNOWN_EN = {3: "Pleiades", 8: "morning star", 11: "a cross"}

TXT = {
    "zh": {
        "c01_title": "1612：馬拉尼昂島", "c01_sub": "手描示意，非精確海岸線",
        "fr": "法國", "eu": "歐洲", "af": "非洲", "sa": "南美洲", "atl": "大西洋", "eq": "赤道 0°",
        "sl1": "馬拉尼昂島", "sl2": "今天的聖路易斯・南緯 2.5°",
        "route": "1612 年從法國出航", "fort1": "Saint-Louis 堡", "fort2": "1612/9/8 命名",
        "c01_foot": "法國在巴西北岸的殖民地「赤道法蘭西」（France Équinoxiale），1615 年被葡萄牙奪回",
        "c02_title": "1614 年，巴黎出版", "c02_cap1": "Claude d'Abbeville（嘉布遣會士）",
        "c02_cap2": "《Histoire de la mission des pères Capucins en l'Isle de Maragnan》",
        "c02_src": "掃描：Internet Archive histoiredelamiss00clau（公有領域）",
        "c02b_title": "每一顆都叫得出名字", "c02b_ref": "第 51 章 fol. 316r", "c02b_hi": "nom propre：自己的名字",
        "c03_title": "他抄下的 28 個名字", "c03_sub": "照原書順序與拼法",
        "zh9": {0: "會下雨的下巴", 2: "九顆星的烤架", 6: "螯蝦", 14: "猴子", 15: "螃蟹", 21: "長籃子",
                20: "圓圓的蜂蜜", 25: "燒起來的火", 17: "喝湯的小男孩"},
        "c03b_title": "「還有很多，我就不寫了」", "c03b_ref": "fol. 319v",
        "c03b_hi": "…plusieurs autres que ie laisse pour euiter la plus grande prolixité",
        "c03q_title": "可惜，大多沒寫是哪幾顆", "c03q_foot": "書上直接說出是哪顆的：昴宿、十字、晨星",
        "c04_title": "隔了 2,500 公里、快 400 年", "c04_sub": "手描示意，非精確國界",
        "br": "巴西", "slz": "São Luís", "slz2": "圖皮南巴（1612）", "gua": "巴西南部的瓜拉尼人",
        "dist": "直線超過 2,500 公里", "lang": "圖皮南巴語、瓜拉尼語同屬圖皮-瓜拉尼語族",
        "tl": [(0.03, "1612", "四個月", AMBER), (0.20, "1614", "巴黎出書", AMBER),
               (0.36, "1615", "葡萄牙奪回", GREY), (0.92, "2000 年代", "Afonso 認回", GREEN)],
        "c04_foot": "Afonso：兩邊的星空很像，雖然隔了語言、空間和時間",
        "c05_title": "昴宿＝一年的刻度", "c05_ref": "fol. 320v", "c05_hi": "Seichou＝昴宿",
        "ring_c1": "一年", "ring_c2": "（雨季到雨季）",
        "ring": [(90, "出現", "雨季前幾天", BLUE), (0, "雨季", "", BLUE), (-90, "不見", "雨季結束", GREY),
                 (180, "再出現", "＝下一年的雨", AMBER)],
        "c05_foot": "傳教士：他們就這樣清楚知道一整年有多長",
        "c06_title": "這週末抬頭看", "c06_sub": "台北 2027/3/12（五）–3/14（日）",
        "c06_rows": [("18:01", "日落；19:17 天黑（天文昏影結束）", WHITE),
                     ("20:00 往西", "拿棍子的老人（獵戶＋金牛）斜躺在西到西南的半空\n"
                                    "斷腿處參宿四 62° 最高；畢宿五 50°、昴宿 41°（西偏北）", GREEN),
                     ("", "頭上的羽毛＝昴宿；市區光害下，棍子（π Ori）要雙筒", BLUE),
                     ("十點前", "22:24 昴宿、22:58 畢宿五陸續低於 10°", GREEN),
                     ("月牙", "3/12 20:00：18% 眉月 21°，在昴宿正下方約 20°\n"
                              "3/13 到昴宿旁；3/14 在昴宿與畢宿五之間", WHITE),
                     ("東方高空", "火星 56°、木星 61°，都在獅子座", RED),
                     ("美洲鴕的頭", "3/13 凌晨 1 點，墾丁朝正南：南十字 5–11°\n"
                                  "要南方海面無遮蔽、很晴才看得到", WHITE)],
        "c06_box1": "台灣看不到的：", "c06_box2": "鴕鳥的嘴（蒼蠅座 α、β）和兩顆蛋（蒼蠅座 γ、δ）",
        "c06_src": "PyEphem 4.2.1 自算（台北 25.033°N 121.565°E；墾丁 21.95°N 120.80°E）",
    },
    "en": {
        "c01_title": "1612: the Isle of Maragnan", "c01_sub": "Hand-drawn sketch; coastlines schematic",
        "fr": "France", "eu": "Europe", "af": "Africa", "sa": "South America", "atl": "Atlantic", "eq": "Equator 0°",
        "sl1": "Isle of Maragnan", "sl2": "today's São Luís · 2.5°S",
        "route": "sailed from France, 1612", "fort1": "Fort Saint-Louis", "fort2": "named 8 Sep 1612",
        "c01_foot": "France's colony on Brazil's north coast, France Équinoxiale, retaken by Portugal in 1615",
        "c02_title": "Published in Paris, 1614", "c02_cap1": "Claude d'Abbeville (Capuchin friar)",
        "c02_cap2": "Histoire de la mission des pères Capucins en l'Isle de Maragnan",
        "c02_src": "Scan: Internet Archive histoiredelamiss00clau (public domain)",
        "c02b_title": "A name for every star", "c02b_ref": "Ch. 51, fol. 316r", "c02b_hi": "nom propre: its own name",
        "c03_title": "The 28 names he wrote down", "c03_sub": "in the book's order and spelling",
        "zh9": {0: "rainy jaw", 2: "grill of nine stars", 6: "crayfish", 14: "monkey", 15: "crab", 21: "long basket",
                20: "round honey", 25: "blazing fire", 17: "boy eating porridge"},
        "c03b_title": "“Many others I leave out”", "c03b_ref": "fol. 319v",
        "c03b_hi": "…plusieurs autres que ie laisse pour euiter la plus grande prolixité",
        "c03q_title": "Mostly, he never said which stars", "c03q_foot": "Identified in the book itself: Pleiades, a cross, the morning star",
        "c04_title": "2,500 km and almost 400 years apart", "c04_sub": "Hand-drawn sketch; borders schematic",
        "br": "Brazil", "slz": "São Luís", "slz2": "Tupinambá (1612)", "gua": "Guarani of southern Brazil",
        "dist": "over 2,500 km in a straight line", "lang": "Tupinambá and Guarani: both Tupi-Guarani languages",
        "tl": [(0.03, "1612", "four months", AMBER), (0.20, "1614", "book in Paris", AMBER),
               (0.36, "1615", "Portugal retakes", GREY), (0.92, "2000s", "Afonso", GREEN)],
        "c04_foot": "Afonso: the two skies are very alike, despite language, distance and time",
        "c05_title": "The Pleiades mark the year", "c05_ref": "fol. 320v", "c05_hi": "Seichou = Pleiades",
        "ring_c1": "one year", "ring_c2": "(rains to rains)",
        "ring": [(90, "appears", "days before the rains", BLUE), (0, "rains", "", BLUE),
                 (-90, "gone", "rains end", GREY), (180, "appears again", "= next year's rains", AMBER)],
        "c05_foot": "The friar: that is how they know exactly how long a year is",
        "c06_title": "Look up this weekend", "c06_sub": "Taipei, Fri 12 – Sun 14 Mar 2027",
        "c06_rows": [("18:01", "Sunset; dark at 19:17", WHITE),
                     ("20:00 west", "The Old Man with a stick (Orion + Taurus) lies tilted, W to SW\n"
                                    "Betelgeuse 62° highest; Aldebaran 50°, Pleiades 41° (WNW)", GREEN),
                     ("", "Feathers on his head = Pleiades; binoculars for the stick (π Ori)", BLUE),
                     ("before 22:00", "Pleiades below 10° at 22:24, Aldebaran at 22:58", GREEN),
                     ("Moon", "12 Mar 20:00: 18% crescent at 21°, ~20° below the Pleiades\n"
                              "13 Mar beside the Pleiades; 14 Mar between Pleiades and Aldebaran", WHITE),
                     ("high east", "Mars 56°, Jupiter 61°, both in Leo", RED),
                     ("Rhea's head", "13 Mar 01:00 from Kenting, due south: Crux at 5–11°\n"
                                     "needs a clear sea horizon", WHITE)],
        "c06_box1": "Never visible from Taiwan:", "c06_box2": "the rhea's beak (α, β Mus) and the two eggs (γ, δ Mus)",
        "c06_src": "Computed with PyEphem 4.2.1 (Taipei 25.033°N 121.565°E; Kenting 21.95°N 120.80°E)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 原書頁面 ══════════════════════
_TMP = tempfile.mkdtemp(prefix="a25pdf_")
PAGE_PT = (320.3446, 489.9323)                       # PDF 頁面（點）


def page_img(p, dpi=220):
    from PIL import Image
    out = os.path.join(_TMP, f"p{p}")
    if not os.path.exists(out + f"-{p:03d}.png") and not os.path.exists(out + f"-{p}.png"):
        subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(dpi), "-png", PDF, out], check=True)
    f = next(os.path.join(_TMP, n) for n in os.listdir(_TMP) if n.startswith(f"p{p}-"))
    return Image.open(f).convert("RGB")


def words(p):
    r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-bbox", PDF, "-"], capture_output=True,
                       text=True, check=True).stdout
    return [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in
            re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', r)]


def place_crop(ax, p, crop, x0, y_top, width, boxes=(), unders=(), box_col=AMBER):
    """把 PDF 第 p 頁的 crop（頁面比例 x0,y0,x1,y1）放到畫布：左上 (x0, y_top)、寬 width。
    boxes／unders＝要框／畫底線的字（PDF 點座標的字框）"""
    import numpy as np
    im = page_img(p)
    W, H = im.size
    a, b, c, d = crop
    cr = im.crop((int(a * W), int(b * H), int(c * W), int(d * H)))
    h = width * cr.size[1] / cr.size[0]
    ax.add_patch(CB.Rectangle((x0 - 0.012, y_top - h - 0.012), width + 0.024, h + 0.024, fc="#EAD9B5",
                              ec=GREY, lw=1.0, zorder=3))
    ax.imshow(np.asarray(cr), extent=(x0, x0 + width, y_top - h, y_top), zorder=4, interpolation="lanczos")

    def tr(px, py):
        py -= 4.5                                        # 掃描的文字層比影像低約半行（逐張預覽對過）
        u = (px / PAGE_PT[0] - a) / (c - a)
        v = (py / PAGE_PT[1] - b) / (d - b)
        return x0 + u * width, y_top - v * h
    for (bx0, by0, bx1, by1) in boxes:
        (X0, Y0), (X1, Y1) = tr(bx0 - 1.5, by0 - 1.0), tr(bx1 + 1.5, by1 + 1.0)
        ax.add_patch(CB.FancyBboxPatch((X0, Y1), X1 - X0, Y0 - Y1, boxstyle="round,pad=0.0,rounding_size=0.008",
                                       fc="none", ec=box_col, lw=3.0, zorder=6))
    for (bx0, by0, bx1, by1) in unders:
        (X0, _), (X1, Y1) = tr(bx0, by0), tr(bx1, by1 + 0.8)
        ax.plot([X0, X1], [Y1, Y1], c=box_col, lw=3.0, alpha=.95, zorder=6, solid_capstyle="round")
    return h


def span(ws, first, last, after=0.0):
    """從字 first 到 last（含）的每一行字框（同一行合併）"""
    i = next(k for k, w in enumerate(ws) if w[4] == first and w[1] >= after)
    j = next(k for k in range(i, len(ws)) if ws[k][4] == last)
    lines = {}
    for w in ws[i:j + 1]:
        key = round(w[1] / 6)
        l = lines.setdefault(key, [w[0], w[1], w[2], w[3]])
        l[0], l[1], l[2], l[3] = min(l[0], w[0]), min(l[1], w[1]), max(l[2], w[2]), max(l[3], w[3])
    return [tuple(v) for v in lines.values()]


# ══════════════════════ C-A25-01 馬拉尼昂島 ══════════════════════
COAST_SA = [(12.4, -71.7), (11.0, -74.8), (9.5, -76.0), (8.7, -77.4), (7.0, -77.8), (4.0, -77.4), (1.5, -79.0),
            (-1.0, -80.5), (-3.5, -80.3), (-5.0, -81.2), (-6.5, -79.9), (-9.5, -78.5), (-12.5, -76.7),
            (-15.5, -75.0), (-18.3, -70.4), (-23.5, -70.5), (-27.0, -70.9), (-30.0, -71.4), (-33.0, -71.7),
            (-37.0, -73.6), (-41.5, -73.8), (-46.0, -75.5), (-50.0, -75.4), (-53.0, -74.0), (-55.0, -69.0),
            (-54.0, -67.5), (-52.3, -68.4), (-50.0, -68.9), (-47.0, -65.8), (-45.0, -67.2), (-42.5, -63.8),
            (-40.8, -62.2), (-38.8, -62.3), (-36.3, -56.8), (-34.9, -56.2), (-33.7, -53.4), (-30.0, -50.3),
            (-28.0, -48.6), (-25.5, -48.4), (-23.0, -43.2), (-22.0, -41.0), (-18.5, -39.7), (-13.0, -38.5),
            (-8.0, -34.9), (-5.2, -35.5), (-3.0, -40.0), (-2.5, -44.3), (-0.5, -48.5), (1.8, -50.0),
            (4.0, -51.6), (5.8, -55.0), (6.8, -58.2), (8.6, -60.6), (10.7, -61.9), (10.6, -64.3),
            (10.4, -67.0), (11.5, -69.8), (12.4, -71.7)]
COAST_EA = [(56.0, -6.0), (58.5, -3.0), (57.5, -1.8), (55.0, -1.5), (53.0, 0.3), (51.3, 1.4), (50.8, 1.6),
            (49.7, 0.2), (49.3, -1.2), (48.6, -1.4), (48.7, -4.6), (47.8, -4.3), (47.3, -2.5), (46.2, -1.2),
            (44.6, -1.2), (43.4, -1.7), (43.6, -5.6), (43.4, -8.3), (42.2, -8.8), (40.0, -8.9), (38.7, -9.5),
            (37.0, -8.9), (36.2, -6.0), (35.8, -5.9), (34.0, -6.8), (32.3, -9.3), (30.4, -9.6), (28.0, -12.5),
            (26.0, -14.5), (23.7, -15.9), (21.0, -17.0), (17.0, -16.3), (14.7, -17.4), (12.5, -16.7),
            (10.8, -15.0), (9.5, -13.7), (8.0, -13.2), (6.3, -10.8), (4.4, -7.6), (5.0, -4.0), (5.2, -1.0),
            (6.3, 2.5), (6.4, 4.5), (4.3, 6.0), (4.5, 8.5), (2.0, 9.8), (-1.0, 9.0), (-4.5, 11.8), (-8.8, 13.2),
            (-15.0, 12.2), (-22.0, 14.4)]
FRANCE = (47.6, -2.5)                                   # 法國西岸（示意）
SLZ = (-2.53, -44.30)
LON0, LAT0, SC1 = -34.0, 10.0, 0.0175


def m1(lat, lon):
    return (lon - LON0) * SC1, (lat - LAT0) * SC1 - 0.02


def c01_map(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 31, WHITE)
    T(ax, 0.0, 0.845, tx("c01_sub"), 16, GREY, w="normal")
    xy = [m1(*p) for p in COAST_SA]
    ax.add_patch(CB.Polygon(xy, closed=True, fc=LAND, ec=GREY, lw=1.6, alpha=.95, zorder=2))
    ea = [m1(*p) for p in COAST_EA] + [m1(-22.0, 30.0), m1(56.0, 30.0)]
    ax.add_patch(CB.Polygon(ea, closed=True, fc=LAND, ec=GREY, lw=1.6, alpha=.95, zorder=2))
    a, b = m1(0, -80), m1(0, 8)
    ax.plot([a[0], b[0]], [a[1], a[1]], c=AMBER, lw=1.3, ls=(0, (6, 5)), alpha=.7, zorder=3)
    T(ax, *m1(1.8, -78.0), tx("eq"), 13, AMBER, ha="left", w="normal")
    T(ax, *m1(-14.0, -60.0), tx("sa"), 20, WHITE, w="normal", alpha=.8)
    T(ax, *m1(14.0, -1.0), tx("af"), 20, WHITE, w="normal", alpha=.8)
    T(ax, *m1(44.0, 12.0), tx("eu"), 18, WHITE, w="normal", alpha=.7)
    T(ax, *m1(28.0, -58.0), tx("atl"), 18, SEA_LINE, w="normal", alpha=.9)
    x, y = m1(*FRANCE)
    ax.scatter([x], [y], s=120, c=WHITE, zorder=8, lw=0)
    T(ax, x + 0.06, y + 0.035, tx("fr"), 17, WHITE, ha="left")
    x, y = m1(*SLZ)
    ax.scatter([x], [y], s=170, c=AMBER, zorder=8, lw=0)
    ax.scatter([x], [y], s=800, c=AMBER, alpha=.18, zorder=7, lw=0)
    T(ax, x + 0.05, y - 0.06, tx("sl1"), 18, AMBER, ha="left")
    T(ax, x + 0.05, y - 0.115, tx("sl2"), 14, AMBER, ha="left", w="normal")
    ax.add_patch(CB.FancyBboxPatch((-0.72, -0.905), 1.44, 0.09, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#0B0F1E", ec="none", alpha=.85, zorder=10))
    T(ax, 0.0, -0.86, tx("c01_foot"), 13, WHITE, w="normal")


def c01_route(ax):
    (x0, y0), (x1, y1) = m1(*FRANCE), m1(*SLZ)
    pts = []
    for i in range(61):
        t = i / 60
        x = x0 + (x1 - x0) * t - 0.30 * math.sin(math.pi * t)
        y = y0 + (y1 - y0) * t - 0.05 * math.sin(math.pi * t)
        pts.append((x, y))
    ax.plot([p[0] for p in pts[:-3]], [p[1] for p in pts[:-3]], c=AMBER, lw=2.6, ls=(0, (7, 5)), alpha=.95, zorder=6)
    CB.arrow(ax, pts[-1], pts[-6], c=AMBER, lw=2.6, alpha=.95, style="-|>")
    xm, ym = pts[30]
    T(ax, xm - 0.04, ym + 0.05, tx("route"), 16, AMBER, ha="right")
    x, y = m1(*SLZ)
    ax.add_patch(CB.Polygon([(x - 0.035, y + 0.10), (x + 0.035, y + 0.10), (x + 0.035, y + 0.155),
                             (x, y + 0.185), (x - 0.035, y + 0.155)], closed=True, fc=WHITE, ec="none",
                            alpha=.9, zorder=9))
    T(ax, x - 0.06, y + 0.16, tx("fort1"), 15, WHITE, ha="right")
    T(ax, x - 0.06, y + 0.11, tx("fort2"), 13, GREY, ha="right", w="normal")


# ══════════════════════ C-A25-02 1614 年的書 ══════════════════════
def c02_title(ax):
    T(ax, 0.0, 0.92, tx("c02_title"), 31, WHITE)
    h = place_crop(ax, 5, (0.05, 0.03, 0.95, 0.97), -0.40, 0.84, 0.80)
    T(ax, 0.0, 0.84 - h - 0.07, tx("c02_cap1"), 16, AMBER)
    T(ax, 0.0, 0.84 - h - 0.125, tx("c02_cap2"), 12.5, WHITE, w="normal")
    T(ax, 0.0, -0.94, tx("c02_src"), 11, GREY, w="normal")


def c02_text(ax):
    T(ax, 0.0, 0.62, tx("c02b_title"), 31, WHITE)
    ws = words(649)
    nom = [w for w in ws if w[4] in ("nom", "propre") and 360 < w[1] < 370]
    box = (min(w[0] for w in nom), min(w[1] for w in nom), max(w[2] for w in nom), max(w[3] for w in nom))
    h = place_crop(ax, 649, (0.03, 0.662, 0.80, 0.812), -0.90, 0.50, 1.80, boxes=[box])
    T(ax, 0.90, 0.50 - h - 0.06, tx("c02b_ref"), 13, GREY, ha="right", w="normal")
    T(ax, -0.90, 0.50 - h - 0.06, tx("c02b_hi"), 17, AMBER, ha="left")


# ══════════════════════ C-A25-03 二十八個名字 ══════════════════════
GX = (-0.67, 0.0, 0.67)
GY0, GDY = 0.70, -0.148


def _cell(i):
    return GX[i % 3], GY0 + GDY * (i // 3)


def c03_list(ax):
    T(ax, 0.0, 0.92, tx("c03_title"), 31, WHITE)
    T(ax, 0.0, 0.845, tx("c03_sub"), 15, GREY, w="normal")
    for i, (nm, hi, big) in enumerate(NAMES):
        x, y = _cell(i)
        T(ax, x, y, nm, 13.5, GREY, w="normal", alpha=.55, z=2)


def c03_nine(ax):
    zh = tx("zh9")
    for i, (nm, hi, big) in enumerate(NAMES):
        if not hi:
            continue
        x, y = _cell(i)
        w, hgt = (0.62, 0.130) if big else (0.56, 0.118)
        ax.add_patch(CB.FancyBboxPatch((x - w / 2, y - 0.072), w, hgt, boxstyle="round,pad=0.0,rounding_size=0.02",
                                       fc="#0B0F1E", ec=AMBER if big else WHITE, lw=2.2 if big else 1.2,
                                       alpha=1.0, zorder=8))
        T(ax, x, y, nm, 15 if big else 13.5, AMBER if big else WHITE, z=9)
        T(ax, x, y - 0.040, zh[i], 17 if big else 14, WHITE, w="bold" if big else "normal", z=9)
        T(ax, x - w / 2 + 0.03, y - 0.040, str(hi), 11, GREY, w="normal", z=9)


def c03_end(ax):
    T(ax, 0.0, 0.92, tx("c03b_title"), 29, WHITE)
    # 「& plusieurs autres que ie laisse pour euiter la plus grande prolixité」三行（PDF 文字層字框，pdftotext -bbox）
    lines = [(248, 231, 314, 242), (149, 244, 312, 255), (148, 256, 188, 267)]
    h = place_crop(ax, 656, (0.05, 0.44, 1.0, 0.655), -0.78, 0.82, 1.56, unders=lines)
    T(ax, 0.78, 0.82 - h - 0.05, tx("c03b_ref"), 13, GREY, ha="right", w="normal")


def c03_q(ax):
    T(ax, 0.0, 0.05, tx("c03q_title"), 24, WHITE)
    kn = KNOWN if LANG == "zh" else KNOWN_EN
    for i, (nm, hi, big) in enumerate(NAMES):
        c, r = i % 7, i // 7
        x, y = -0.78 + c * 0.26, -0.10 - r * 0.17
        known = i in kn
        ax.add_patch(CB.FancyBboxPatch((x - 0.11, y - 0.07), 0.22, 0.14, boxstyle="round,pad=0.0,rounding_size=0.02",
                                       fc="#0B0F1E", ec=AMBER if known else GREY, lw=1.6 if known else 1.0,
                                       zorder=8))
        T(ax, x, y + 0.012, kn[i] if known else "？", 15 if known else 22, AMBER if known else GREY, z=9)
        T(ax, x, y - 0.048, nm if len(nm) <= 12 else nm[:11] + "…", 8.5, GREY, w="normal", z=9)
    T(ax, 0.0, -0.86, tx("c03q_foot"), 14, AMBER, w="normal")


# ══════════════════════ C-A25-04 兩千五百公里 ══════════════════════
GUA = (-25.5, -53.0)
LON4, LAT4, SC4 = -58.0, -20.0, 0.020


def m4(lat, lon):
    return (lon - LON4) * SC4 - 0.05, (lat - LAT4) * SC4 + 0.14


def c04_map(ax):
    T(ax, 0.0, 0.92, tx("c04_title"), 30, WHITE)
    T(ax, 0.0, 0.85, tx("c04_sub"), 15, GREY, w="normal")
    xy = [m4(*p) for p in COAST_SA]
    ax.add_patch(CB.Polygon(xy, closed=True, fc=LAND, ec=GREY, lw=1.6, alpha=.95, zorder=2))
    T(ax, *m4(-10.0, -52.0), tx("br"), 22, WHITE, w="normal", alpha=.7)
    (x0, y0), (x1, y1) = m4(*SLZ), m4(*GUA)
    ax.add_patch(CB.Ellipse((x1, y1), 0.26, 0.20, fc=GREEN, ec="none", alpha=.22, zorder=4))
    ax.plot([x0, x1], [y0, y1], c=WHITE, lw=2.4, ls=(0, (6, 4)), alpha=.9, zorder=5)
    for (x, y), col in (((x0, y0), AMBER), ((x1, y1), GREEN)):
        ax.scatter([x], [y], s=150, c=col, zorder=7, lw=0)
    T(ax, x0 + 0.05, y0 + 0.05, tx("slz"), 18, AMBER, ha="left")
    T(ax, x0 + 0.05, y0 - 0.005, tx("slz2"), 14, AMBER, ha="left", w="normal")
    T(ax, x1 - 0.17, y1 - 0.02, tx("gua"), 16, GREEN, ha="right")
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    T(ax, xm + 0.05, ym + 0.02, tx("dist"), 17, WHITE, ha="left")


def c04_time(ax):
    y = -0.66
    ax.plot([-0.88, 0.88], [y, y], c=WHITE, lw=2.0, alpha=.6)
    ax.plot([0.10, 0.70], [y, y], c="#0B0F1E", lw=4.0, zorder=3)
    for xx in (0.30, 0.40, 0.50):
        ax.scatter([xx], [y], s=10, c=GREY, zorder=4)
    for px, era, ev, col in tx("tl"):
        x = -0.88 + 1.76 * px
        ax.scatter([x], [y], s=180, c=col, zorder=5, lw=0)
        T(ax, x, y + 0.075, era, 16, col)
        T(ax, x, y - 0.075, ev, 13, WHITE, w="normal", alpha=.85)
    T(ax, 0.0, -0.86, tx("lang"), 14, GREY, w="normal")


# ══════════════════════ C-A25-05 昴宿與雨 ══════════════════════
def c05_text(ax):
    T(ax, 0.0, 0.92, tx("c05_title"), 30, WHITE)
    ws = words(658)
    sei = [w for w in ws if "eichou" in w[4]]
    boxes = [sei[0][:4]] if sei else []
    h = place_crop(ax, 658, (0.05, 0.10, 1.0, 0.335), -0.62, 0.83, 1.24, boxes=boxes, box_col=BLUE)
    T(ax, 0.62, 0.83 - h - 0.045, tx("c05_ref"), 12, GREY, ha="right", w="normal")
    T(ax, -0.62, 0.83 - h - 0.045, tx("c05_hi"), 15, BLUE, ha="left")


def c05_ring(ax):
    cx, cy, R = 0.0, -0.46, 0.30
    th = [math.radians(a) for a in range(0, 361, 3)]
    ax.plot([cx + R * math.cos(t) for t in th], [cy + R * math.sin(t) for t in th], c=GREY, lw=2.0, alpha=.5)
    # 雨季＝從「出現」(上) 順時針到「不見」(下) 的右半圈
    th2 = [math.radians(a) for a in range(90, -91, -3)]
    ax.plot([cx + R * math.cos(t) for t in th2], [cy + R * math.sin(t) for t in th2], c=BLUE, lw=9, alpha=.75,
            solid_capstyle="round")
    for k in range(3):                                  # 雨點
        a = math.radians(45 - k * 45)
        x, y = cx + (R + 0.07) * math.cos(a), cy + (R + 0.07) * math.sin(a)
        ax.plot([x, x - 0.012], [y + 0.02, y - 0.02], c=BLUE, lw=2.2, alpha=.8)
    CB.arrow(ax, (cx - R * math.cos(math.radians(80)), cy + R * math.sin(math.radians(80))),
             (cx - R * math.cos(math.radians(60)), cy + R * math.sin(math.radians(60))), c=AMBER, lw=2.4,
             alpha=.9, style="-|>")
    for ang, s1, s2, col in tx("ring"):
        a = math.radians(ang)
        if ang == 0:
            T(ax, cx + R + 0.16, cy, s1, 18, col)
            continue
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        ax.scatter([x], [y], s=150, c=col, zorder=6, lw=0)
        if ang == 180:
            T(ax, x - 0.04, y + 0.03, s1, 17, col, ha="right")
            T(ax, x - 0.04, y - 0.03, s2, 13, WHITE, ha="right", w="normal")
        else:
            dy = 0.065 if ang > 0 else -0.065
            T(ax, x, y + dy + (0.0 if ang > 0 else -0.0), s1, 17, col)
            T(ax, x, y + dy * 1.85, s2, 13, WHITE, w="normal")
    T(ax, cx, cy + 0.02, tx("ring_c1"), 19, WHITE)
    T(ax, cx, cy - 0.035, tx("ring_c2"), 12, GREY, w="normal")
    T(ax, 0.0, -0.94, tx("c05_foot"), 14, WHITE, w="normal")


# ══════════════════════ C-A25-06 這週末抬頭看（9:16 圖卡） ══════════════════════
def c06_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.947, tx("c06_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.907, tx("c06_sub"), fontproperties=FP, fontsize=14, color=GREY, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.880, 0.880], c=WHITE, lw=1.0, alpha=.4)
    y = 0.865
    for t, body, col in tx("c06_rows"):
        n = body.count("\n") + 1
        h = 0.030 + 0.030 * n
        if t:
            ax.text(0.04, y - 0.026, t, fontproperties=FP, fontsize=13, color=col, ha="left", va="center",
                    weight="bold")
        ax.text(0.27, y - 0.012 - 0.015 * n, body, fontproperties=FP, fontsize=11.5, color=WHITE, ha="left",
                va="center", linespacing=1.45)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.add_patch(CB.FancyBboxPatch((0.05, y - 0.130), 0.90, 0.100, boxstyle="round,pad=0.005,rounding_size=0.02",
                                   fc="#1B2240", ec=AMBER, lw=1.2))
    ax.text(0.5, y - 0.058, tx("c06_box1"), fontproperties=FP, fontsize=12.5, color=AMBER, ha="center",
            va="center", weight="bold")
    ax.text(0.5, y - 0.095, tx("c06_box2"), fontproperties=FP, fontsize=11.5, color=WHITE, ha="center",
            va="center")
    ax.text(0.5, 0.068, tx("c06_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center",
            va="center")


def emit_groups(title, layers, previews):
    """每層一張透明 PNG；預覽依鏡頭分組（同一鏡實際會同時出現的層才疊在一起）"""
    for nm, fn in layers:
        f, ax = CB.newfig(); fn(ax); CB.save(f, "", f"{title}_{nm}層_透明.png")
    for pv, names in previews:
        f, ax = CB.newfig(dark=True)
        for nm, fn in layers:
            if nm in names:
                fn(ax)
        CB.save(f, "", f"{title}_{pv}_黑底.png", transparent=False)


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    CB.emit("", [("地圖", c01_map), ("航線", c01_route)], title="C-A25-01_馬拉尼昂島")
    emit_groups("C-A25-02_1614年的書", [("扉頁", c02_title), ("原文", c02_text)],
                [("預覽", ["扉頁"]), ("原文預覽", ["原文"])])
    emit_groups("C-A25-03_二十八個名字", [("名單", c03_list), ("九個", c03_nine), ("結尾原文", c03_end), ("問號", c03_q)],
                [("預覽", ["名單", "九個"]), ("結尾預覽", ["結尾原文", "問號"])])
    CB.emit("", [("地圖", c04_map), ("時間軸", c04_time)], title="C-A25-04_兩千五百公里")
    CB.emit("", [("原文", c05_text), ("年環", c05_ring)], title="C-A25-05_昴宿與雨")
    f, ax = CB.newcard(dark=True)
    c06_card(ax)
    CB.save(f, "", "C-A25-06_這週末抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
