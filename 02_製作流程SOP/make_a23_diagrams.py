# -*- coding: utf-8 -*-
"""A-23 羅馬尼亞：牧羊人的星空農場｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A23-01 Otescu 的星圖與回信（星圖、回信 → 02 鏡；一年 → 03 鏡，單獨成立）
C-A23-02 換了性別的牛郎織女（9:16 圖卡）→ 13 鏡
C-A23-03 Miorița（山坡、流星 → 16 鏡；婚禮 → 17 鏡，單獨成立）
C-A23-04 羅馬尼亞星名小辭典（9:16 圖卡，可存圖）→ 18 鏡
C-A23-05 這週末抬頭看（9:16 圖卡，可存圖；台北 2027/2/26 20:00 全天＋2/27 05:00 往東）→ 19 鏡
C-A23-06 19:10 往西看：井沉了一半（地平線、井）→ 14 鏡迄格（長圖沒有地平線，改用地平座標示意）

做法：地圖是手描示意輪廓（1896 年羅馬尼亞王國：瓦拉幾亞＋摩爾達維亞＋多布羅加，不含特蘭西瓦尼亞；非精確國界）；
回信只標英譯序言點名的三個縣份份數（Neamț 13、Prahova 5、Argeș 3），其餘 18 份不畫點（沒有逐縣資料，不編造位置）。
不臨摹 Otescu 書影、不畫寫實兇殺；Miorița 為簡筆。星圖縮圖＝切平面投影（東在左、北在上），連線照 Stellarium romanian。
引文：〈Miorița〉Alecsandri 版（ro.wikisource，現代拼法）。天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E UTC+8，15°C／1013 hPa）。

執行：python3 make_a23_diagrams.py            （中文，輸出 05_素材/A-23_羅馬尼亞/_概念圖/）
      python3 make_a23_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-23_羅馬尼亞/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND, HILL, BG = "#FF6B6B", "#7C8BA8", "#2A3350", "#26324F", "#0B0F1E"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "1896：一張星圖寄到全國", "c01_sub": "Ion Otescu，《羅馬尼亞農民的天與星》（1907）",
        "chart": "以布加勒斯特為準的星圖", "send": "寄給鄉村老師", "ask": "去問村裡最老的農民",
        "map_note": "1896 年的羅馬尼亞王國（手描示意，非精確國界；不含特蘭西瓦尼亞）",
        "buc": "布加勒斯特", "neamt": "Neamț 13 份", "prahova": "Prahova 5 份", "arges": "Argeș 3 份",
        "others": "其餘 18 份來自其他縣份", "total": "39 份有用的回信",
        "src01": "Otescu 1907，SARM 英譯序言 p.1；書末來源表 39 處",
        "c01y_title": "農民什麼時候看星星？", "c01y_sub": "Otescu 1907（SARM 英譯 p.1）",
        "months": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], "mo": "月",
        "farm": "六—九月：農忙，農民拿星星報時", "shep": "其他月份：只有牧羊人還在看",
        "shep2": "所以那些星，農民叫「牧羊人的星」",
        "c02_title": "換了性別的牛郎織女", "c02_sub": "同一排星，兩地各自的故事",
        "cn": "中國", "ro": "羅馬尼亞",
        "cn1": "牛郎（河鼓二）挑扁擔", "cn2": "擔著兩個孩子（河鼓一、三）", "cn3": "織女（織女一）在對岸織布",
        "ro1": "公主（牛郎星）挑扁擔", "ro2": "桶裡是水，給亡魂解渴", "ro3": "織女星＝牧羊人，四顆星是羊",
        "vega": "織女星", "altair": "牛郎星",
        "c02_foot1": "不是同一個故事傳過去：兩邊各自把這排星看成扁擔",
        "c02_foot2": "Otescu 1907（SARM 英譯 p.6–7）；CRT；H-七夕",
        "c03_title": "〈Miorița〉小母羊", "c03_sub": "羅馬尼亞民謠（Alecsandri 版，1850／1852）",
        "c03_q": "「婚禮上，掉下一顆星」", "c03_ro": "Că la nunta mea / A căzut o stea",
        "c03_n1": "牧羊人知道同伴要殺害他，", "c03_n2": "交代小母羊：跟羊群說，我結婚了",
        "c03_belief": "每個人在天上都有一顆星；人走了，星就掉下來（Otescu p.25）",
        "c03w_title": "他說給羊群聽的婚禮", "c03w_sub": "〈Miorița〉Alecsandri 版（ro.wikisource，現代拼法）",
        "sunmoon": "太陽和月亮：捧著婚冠", "trees": "冷杉和楓樹：賓客", "mount": "高山：神父",
        "birds": "鳥：樂師", "torch": "星星：火把",
        "c03w_ro": "Soarele și luna / Mi-au ținut cununa … Și stele făclii!",
        "c04_title": "羅馬尼亞星名小辭典", "c04_sub": "Otescu 1907（SARM 英譯）；Stellarium romanian；片中補上變音符號",
        "col1": "羅馬尼亞文", "col2": "意思", "col3": "星",
        "rows": [("Capra", "母山羊（帶三隻小羊）", "五車二"), ("Țarcul", "羊圈", "御夫座"),
                 ("Dulăul", "看羊的大狗", "大犬"), ("Zorilă", "天亮的星", "天狼星"),
                 ("Cățelul", "小狗", "小犬"), ("Cloșca cu pui", "母雞帶小雞", "昴宿"),
                 ("Vierii", "公豬", "畢宿"), ("Luceafărul porcesc", "豬的亮星", "畢宿五"),
                 ("Deșteptătorul", "鬧鐘", "畢宿五"), ("Rarița", "小犁", "獵戶"),
                 ("Sfredelul mare", "大鑽子", "腰帶＋參宿四"), ("Secera", "鐮刀", "獵戶"),
                 ("Trisfetitele", "三聖人", "獵戶腰帶"), ("Carul Mare", "大車", "北斗＋大熊"),
                 ("Carul mic", "小車", "小熊"), ("Candela cerului", "天上的長明燈", "北極星"),
                 ("Romulus／Remus", "建立羅馬的兄弟", "北河二／三"), ("Comoara", "寶藏", "北河三"),
                 ("Ciobanul cu oile", "牧羊人和他的羊", "天琴"), ("Fata de împărat", "挑扁擔的公主", "牛郎星一排"),
                 ("Puțul cu jgheab", "井和水槽", "飛馬＋仙女"), ("Calul", "馬", "獅子"),
                 ("Văcarul", "放牛的人", "牧夫"), ("Balaurul", "龍", "天龍"),
                 ("Tronul", "神的寶座", "仙后"), ("Crucea mare／mică", "大／小十字架", "天鵝／海豚"),
                 ("Hora", "圍圈舞", "北冕"), ("Coasa", "長柄大鐮刀", "仙王"), ("Barda", "斧頭", "英仙"),
                 ("Calea Robilor", "奴隸之路", "銀河")],
        "c04_foot1": "頁碼與說法見首留言；Stellarium 原檔沒有變音符號（ă â î ș ț）",
        "c04_foot2": "Otescu 1907；SARM 英譯 2009（Gheorghe & McBeath）；CRT 計畫（Baia Mare）",
        "c05_title": "這週末抬頭看", "c05_p1": "2/26（五）–28 晚上 8 點・台北・全天",
        "c05_p2": "清晨 5 點・往東北看", "N": "北", "S": "南", "E": "東", "W": "西",
        "NE": "東北", "ENE": "東北東", "E2": "東", "zen": "天頂",
        "sirius": "天狼星（大狗）", "capella": "五車二（母山羊）", "jup": "木星", "mars": "火星",
        "reg": "軒轅十四（馬）", "belt": "腰帶（三聖人）", "pollux": "北河三", "procyon": "南河三",
        "aldeb": "畢宿五（鬧鐘）", "vega5": "織女星（牧羊人）", "altair5": "牛郎星（公主）",
        "t1": "05:00 天還全黑，羊群那四顆暗星也看得到；05:30 起天開始亮",
        "t2": "火星 2/19 衝日；月亮 23:17 才升起，前半夜沒有月光",
        "t3": "PyEphem 自算；高度含大氣折射",
        "tags": "#萬國星空　#師大天文社",
        "c06_title": "2/26 19:10 往西看", "c06_sub": "天一黑（天文昏影終），井已經沉了一半",
        "W2": "西", "WNW": "西北西", "WSW": "西南西", "NW": "西北",
        "markab": "室宿一：19:06 已落", "scheat": "室宿二", "algenib": "壁宿一", "alph": "壁宿二",
        "trough": "水槽（仙女座）", "well": "井口四角", "c06_src": "台北；PyEphem 自算，高度含大氣折射",
    },
    "en": {
        "c01_title": "1896: a star chart sent across the country", "c01_sub": "Ion Otescu, Romanian Peasants' Beliefs in Stars and Sky (1907)",
        "chart": "a chart for Bucharest", "send": "sent to village teachers", "ask": "ask the oldest peasants",
        "map_note": "Kingdom of Romania, 1896 (schematic; Transylvania not included)",
        "buc": "Bucharest", "neamt": "Neamț 13", "prahova": "Prahova 5", "arges": "Argeș 3",
        "others": "18 more from other counties", "total": "39 useful replies",
        "src01": "Otescu 1907, SARM transl. preface p.1; 39 places in the source list",
        "c01y_title": "When did peasants watch the stars?", "c01y_sub": "Otescu 1907 (SARM transl. p.1)",
        "months": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], "mo": "",
        "farm": "Jun–Sep: farm work, stars tell the time", "shep": "Rest of the year: only the shepherds",
        "shep2": "so peasants called them “the shepherds' stars”",
        "c02_title": "The Cowherd and the Weaver, swapped", "c02_sub": "Same row of stars, two stories",
        "cn": "China", "ro": "Romania",
        "cn1": "The Cowherd (Altair) carries a yoke", "cn2": "with his two children", "cn3": "the Weaver (Vega) across the river",
        "ro1": "A princess (Altair) carries the yoke", "ro2": "water for the thirsty souls", "ro3": "Vega = the Shepherd, four stars = sheep",
        "vega": "Vega", "altair": "Altair",
        "c02_foot1": "Not one story travelling: each saw the row as a yoke on its own",
        "c02_foot2": "Otescu 1907 (SARM transl. p.6–7); CRT",
        "c03_title": "“Miorița”, the little ewe", "c03_sub": "Romanian ballad (Alecsandri, 1850/1852)",
        "c03_q": "“At my wedding a star fell”", "c03_ro": "Că la nunta mea / A căzut o stea",
        "c03_n1": "The shepherd knows his companions will kill him;", "c03_n2": "tell the flock, he says, that I got married",
        "c03_belief": "Everyone has a star in the sky; when you die it falls (Otescu p.25)",
        "c03w_title": "The wedding he describes to his flock", "c03w_sub": "“Miorița”, Alecsandri version (ro.wikisource)",
        "sunmoon": "Sun and Moon held the crown", "trees": "firs and maples: guests", "mount": "mountains: priests",
        "birds": "birds: musicians", "torch": "stars: torches",
        "c03w_ro": "Soarele și luna / Mi-au ținut cununa … Și stele făclii!",
        "c04_title": "Romanian star names", "c04_sub": "Otescu 1907 (SARM transl.); Stellarium romanian; diacritics restored",
        "col1": "Romanian", "col2": "Meaning", "col3": "Stars",
        "rows": [("Capra", "she-goat (with 3 kids)", "Capella"), ("Țarcul", "goat fold", "Auriga"),
                 ("Dulăul", "sheepdog", "Canis Major"), ("Zorilă", "dawn star", "Sirius"),
                 ("Cățelul", "little dog", "Canis Minor"), ("Cloșca cu pui", "hen and chicks", "Pleiades"),
                 ("Vierii", "boars", "Hyades"), ("Luceafărul porcesc", "the pig's bright star", "Aldebaran"),
                 ("Deșteptătorul", "alarm clock", "Aldebaran"), ("Rarița", "little plough", "Orion"),
                 ("Sfredelul mare", "great auger", "Belt + Betelgeuse"), ("Secera", "sickle", "Orion"),
                 ("Trisfetitele", "Three Saints", "Orion's Belt"), ("Carul Mare", "great cart", "Big Dipper + UMa"),
                 ("Carul mic", "little cart", "Ursa Minor"), ("Candela cerului", "the sky's votive lamp", "Polaris"),
                 ("Romulus／Remus", "founders of Rome", "Castor / Pollux"), ("Comoara", "the treasure", "Pollux"),
                 ("Ciobanul cu oile", "shepherd and sheep", "Lyra"), ("Fata de împărat", "princess with a yoke", "Altair's row"),
                 ("Puțul cu jgheab", "well and trough", "Peg + And"), ("Calul", "horse", "Leo"),
                 ("Văcarul", "cowherd", "Boötes"), ("Balaurul", "dragon", "Draco"),
                 ("Tronul", "God's throne", "Cassiopeia"), ("Crucea mare／mică", "great / little cross", "Cyg / Del"),
                 ("Hora", "ring dance", "Corona Bor."), ("Coasa", "scythe", "Cepheus"), ("Barda", "axe", "Perseus"),
                 ("Calea Robilor", "the slaves' road", "Milky Way")],
        "c04_foot1": "Stellarium's file drops the diacritics (ă â î ș ț)",
        "c04_foot2": "Otescu 1907; SARM transl. 2009 (Gheorghe & McBeath); CRT project (Baia Mare)",
        "c05_title": "Look up this weekend", "c05_p1": "Feb 26–28, 8 p.m., Taipei, whole sky",
        "c05_p2": "5 a.m., facing northeast", "N": "N", "S": "S", "E": "E", "W": "W",
        "NE": "NE", "ENE": "ENE", "E2": "E", "zen": "zenith",
        "sirius": "Sirius (sheepdog)", "capella": "Capella (she-goat)", "jup": "Jupiter", "mars": "Mars",
        "reg": "Regulus (horse)", "belt": "Belt (Three Saints)", "pollux": "Pollux", "procyon": "Procyon",
        "aldeb": "Aldebaran (alarm clock)", "vega5": "Vega (shepherd)", "altair5": "Altair (princess)",
        "t1": "At 5:00 it is still fully dark; twilight begins about 5:30",
        "t2": "Mars at opposition Feb 19; Moon rises 23:17",
        "t3": "Computed with PyEphem; altitudes include refraction",
        "tags": "#WorldSkyCultures　#NTNUAstronomy",
        "c06_title": "Feb 26, 19:10, facing west", "c06_sub": "At full dark the well is already half set",
        "W2": "W", "WNW": "WNW", "WSW": "WSW", "NW": "NW",
        "markab": "Markab: set at 19:06", "scheat": "Scheat", "algenib": "Algenib", "alph": "Alpheratz",
        "trough": "trough (Andromeda)", "well": "the well's four corners", "c06_src": "Taipei; PyEphem, refraction included",
    },
}


def tx(k):
    return TXT[LANG][k]


def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12, va="center", rot=0):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=c, ha=ha, va=va, weight=w,
            alpha=alpha, zorder=z, rotation=rot)


def head(ax, title, sub=None, y=0.90):
    T(ax, 0, y, title, 30, WHITE)
    if sub:
        T(ax, 0, y - 0.085, sub, 14, GREY, w="normal")


def star(ax, x, y, s=60, c=WHITE, z=8, glow=True, alpha=1.0):
    if glow:
        ax.scatter([x], [y], s=s * 5, c=c, alpha=0.15 * alpha, zorder=z - 1, lw=0)
    ax.scatter([x], [y], s=s, c=c, zorder=z, lw=0, alpha=alpha)


S = dict(G.load_stars(BASE))


def tangent(h, ra0, de0):
    ra, de = S[h][:2]
    a, d, a0, d0 = map(math.radians, (ra, de, ra0, de0))
    c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / c
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / c
    return -math.degrees(x), math.degrees(y)          # 東在左


def mini_chart(ax, segs, cx, cy, size, cols, extra=(), lw=2.6, sq=1.0, rot=0.0):
    """星群縮圖：segs＝[(線段組, 色)]；以全部星的中心切平面投影，縮放到 size（最大邊）"""
    hs = sorted({h for g, _ in segs for s in g for h in s} | set(extra))
    ra0 = math.degrees(math.atan2(sum(math.sin(math.radians(S[h][0])) for h in hs),
                                  sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    de0 = sum(S[h][1] for h in hs) / len(hs)
    P = {h: tangent(h, ra0, de0) for h in hs}
    if rot:
        c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        P = {h: (x * c - y * s_, x * s_ + y * c) for h, (x, y) in P.items()}
    xs, ys = [p[0] for p in P.values()], [p[1] for p in P.values()]
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    k = size / max(max(xs) - min(xs), (max(ys) - min(ys)) * sq, 1e-6)
    Q = {h: (cx + (x - mx) * k, cy + (y - my) * k * sq) for h, (x, y) in P.items()}
    for g, col in segs:
        for seg in g:
            ax.plot([Q[h][0] for h in seg], [Q[h][1] for h in seg], c=col, lw=lw, zorder=5,
                    solid_capstyle="round")
    for h in hs:
        v = S[h][2]
        star(ax, *Q[h], max(10, max(0.3, 6.5 - v) ** 1.7 * 9), WHITE, glow=v < 2.5)
    return Q


VEGA, ALTAIR = 91262, 97649
FATA = [[97278, 97649, 98036]]
CIO = [[91262, 91971, 92791, 93194, 92420, 91971]]
ZHINU = [[91262, 91919, 91971, 91262]]                 # 中國 織女三星


# ══════════════════ C-A23-01 Otescu 的星圖與回信 ══════════════════
RO1896 = [(22.4, 44.6), (22.7, 45.2), (23.5, 45.4), (24.5, 45.6), (25.4, 45.4), (26.0, 45.6), (26.6, 45.9),
          (26.2, 46.4), (25.9, 47.0), (25.4, 47.5), (25.2, 47.9), (26.1, 48.0), (26.6, 48.2), (27.4, 47.7),
          (28.0, 47.0), (28.2, 46.4), (28.1, 45.5), (28.7, 45.2), (29.7, 45.2), (29.6, 44.8), (28.8, 44.4),
          (28.6, 43.7), (28.0, 43.8), (27.3, 44.1), (26.1, 43.7), (25.0, 43.7), (24.0, 43.8), (23.0, 43.8),
          (22.6, 44.2)]
LON0, LAT0, KX, KY, MX, MY = 26.05, 45.95, 0.165, 0.235, 0.24, -0.28


def P(lon, lat):
    return (lon - LON0) * KX + MX, (lat - LAT0) * KY + MY


def c01_chart(ax):
    head(ax, tx("c01_title"), tx("c01_sub"))
    cx, cy, r = -0.56, 0.38, 0.24
    ax.add_patch(CB.Circle((cx, cy), r, fc="#10162C", ec=WHITE, lw=2.0, zorder=3))
    import random
    rnd = random.Random(23)
    for _ in range(46):
        a, rr = rnd.uniform(0, 2 * math.pi), r * math.sqrt(rnd.uniform(0, 0.92))
        star(ax, cx + rr * math.cos(a), cy + rr * math.sin(a), rnd.choice((6, 9, 14, 24)), WHITE, glow=False)
    for seg in ([(-0.10, 0.08), (-0.02, 0.12), (0.06, 0.07), (0.12, 0.10)], [(-0.05, -0.12), (0.02, -0.05), (0.10, -0.10)]):
        ax.plot([cx + p[0] for p in seg], [cy + p[1] for p in seg], c=AMBER, lw=1.8, zorder=4)
    T(ax, cx, cy - r - 0.05, tx("chart"), 14, AMBER)
    CB.arrow(ax, (-0.18, 0.30), (-0.30, 0.38), c=WHITE, lw=2.2, alpha=.8, style="-|>")
    T(ax, -0.05, 0.42, tx("send"), 14, WHITE, ha="left")
    T(ax, -0.05, 0.35, tx("ask"), 14, WHITE, ha="left", w="normal")


def c01_reply(ax):
    ax.add_patch(CB.Polygon([P(*q) for q in RO1896], closed=True, fc=LAND, ec="#9FB3D9", lw=2.0, zorder=3))
    bx, by = P(26.10, 44.43)
    star(ax, bx, by, 90, WHITE)
    T(ax, bx, by - 0.045, tx("buc"), 12, WHITE, w="normal")
    import random
    rnd = random.Random(5)
    for (lon, lat), n, k, off in (((26.2, 47.0), 13, "neamt", (-0.26, 0.02)), ((26.0, 45.15), 5, "prahova", (0.02, 0.055)),
                                   ((24.9, 45.0), 3, "arges", (-0.20, -0.06))):
        x0, y0 = P(lon, lat)
        for i in range(n):
            a, rr = 2.39996 * i, 0.012 * math.sqrt(i + 0.5)
            star(ax, x0 + rr * math.cos(a) * 1.6, y0 + rr * math.sin(a) * 1.6, 26, AMBER, glow=False)
        T(ax, x0 + off[0], y0 + off[1], tx(k), 13, AMBER, ha="center")
    T(ax, 0.62, 0.47, tx("total"), 20, AMBER)
    T(ax, 0.62, 0.40, tx("others"), 12, WHITE, w="normal")
    T(ax, 0, -0.84, tx("map_note"), 11, GREY, w="normal")
    T(ax, 0, -0.90, tx("src01"), 11, GREY, w="normal")


def c01_year(ax):
    head(ax, tx("c01y_title"), tx("c01y_sub"), y=0.42)
    x0, w, y0, h = -0.84, 0.14, 0.02, 0.16
    for i, mn in enumerate(tx("months")):
        farm = 5 <= i <= 8
        col = AMBER if farm else BLUE
        ax.add_patch(CB.FancyBboxPatch((x0 + i * w + 0.006, y0), w - 0.012, h, boxstyle="round,pad=0,rounding_size=0.015",
                                       fc=col, ec="none", alpha=0.85 if farm else 0.45, zorder=3))
        T(ax, x0 + i * w + w / 2, y0 + h / 2, mn + tx("mo"), 13, BG if farm else WHITE)
    T(ax, x0 + 5 * w + 2 * w, -0.08, tx("farm"), 16, AMBER)
    T(ax, 0, -0.20, tx("shep"), 20, BLUE)
    T(ax, 0, -0.29, tx("shep2"), 13, WHITE, w="normal")


# ══════════════════ C-A23-02 換了性別的牛郎織女（圖卡） ══════════════════
def c02_card(ax):
    T(ax, 0.5, 0.955, tx("c02_title"), 28, WHITE)
    T(ax, 0.5, 0.920, tx("c02_sub"), 14, GREY, w="normal")
    for i, (k, vseg, vcol, fcol, lines) in enumerate(
            (("cn", ZHINU, AMBER, AMBER, ("cn1", "cn2", "cn3")),
             ("ro", CIO, AMBER, GREEN, ("ro1", "ro2", "ro3")))):
        y0, y1 = (0.505, 0.885) if i == 0 else (0.105, 0.485)
        ax.add_patch(CB.FancyBboxPatch((0.06, y0), 0.88, y1 - y0, boxstyle="round,pad=0,rounding_size=0.02",
                                       fc="#10162C", ec=fcol, lw=1.4, zorder=1))
        T(ax, 0.12, y1 - 0.030, tx(k), 20, fcol, ha="left")
        # 織女在左上、牛郎在右下（各自放大；中間一道銀河示意，距離不按比例）
        Qv = mini_chart(ax, [(vseg, vcol)], 0.20, y1 - 0.15, 0.13, None, sq=9 / 16)
        Qa = mini_chart(ax, [(FATA, fcol)], 0.36, y0 + 0.11, 0.16, None, sq=9 / 16, rot=-20)
        T(ax, Qv[VEGA][0] + 0.035, Qv[VEGA][1] - 0.022, tx("vega"), 11, GREY, ha="left", w="normal")
        T(ax, Qa[ALTAIR][0] + 0.035, Qa[ALTAIR][1] - 0.028, tx("altair"), 11, GREY, ha="left", w="normal")
        for j, kk in enumerate(lines):
            T(ax, 0.52, (y0 + y1) / 2 + 0.05 - j * 0.05, tx(kk), 12.5, fcol if j == 0 else WHITE, ha="left",
              w="bold" if j == 0 else "normal")
    T(ax, 0.5, 0.072, tx("c02_foot1"), 11, WHITE, w="normal")
    T(ax, 0.5, 0.047, tx("c02_foot2"), 9.5, GREY, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 11, WHITE, w="normal")


# ══════════════════ C-A23-03 Miorița ══════════════════
def _hills(ax, y=-0.30):
    xs = [i / 100 - 1 for i in range(201)]
    ys = [y + 0.10 * math.sin(2.2 * x + 0.6) + 0.05 * math.sin(5.3 * x) for x in xs]
    ax.fill_between(xs, [-0.62] * len(xs), ys, color=HILL, zorder=2, lw=0)
    ax.plot(xs, ys, c="#5C6E96", lw=1.6, zorder=3)
    return xs, ys


def c03_hill(ax):
    head(ax, tx("c03_title"), tx("c03_sub"))
    _hills(ax)
    for x, y, s in ((-0.42, -0.36, 1.0), (-0.30, -0.40, 0.9), (-0.18, -0.35, 1.1), (-0.05, -0.42, 0.9),
                    (0.08, -0.37, 1.0), (-0.36, -0.48, 0.8), (-0.12, -0.50, 0.9)):
        ax.add_patch(CB.Ellipse((x, y), 0.085 * s, 0.050 * s, fc="#E8ECF5", ec="none", zorder=4))
        ax.add_patch(CB.Ellipse((x - 0.045 * s, y + 0.008), 0.030 * s, 0.024 * s, fc="#3A3F4F", ec="none", zorder=5))
    # 牧羊人：持杖的簡筆側影
    px, py = 0.38, -0.30
    ax.add_patch(CB.Circle((px, py + 0.17), 0.028, fc=WHITE, ec="none", zorder=5))
    ax.add_patch(CB.Polygon([(px - 0.045, py - 0.10), (px + 0.045, py - 0.10), (px + 0.025, py + 0.14),
                             (px - 0.025, py + 0.14)], closed=True, fc=WHITE, ec="none", zorder=5))
    ax.plot([px + 0.07, px + 0.07], [py - 0.11, py + 0.20], c=WHITE, lw=3, zorder=5)
    ax.add_patch(CB.Arc((px + 0.05, py + 0.20), 0.04, 0.04, theta1=0, theta2=180, ec=WHITE, lw=3, zorder=5))
    T(ax, 0, -0.68, tx("c03_n1"), 15, WHITE, w="normal")
    T(ax, 0, -0.75, tx("c03_n2"), 15, WHITE, w="normal")
    T(ax, 0, -0.86, tx("c03_belief"), 11, GREY, w="normal")


def c03_star(ax):
    x1, y1, x0, y0 = 0.10, 0.12, 0.62, 0.58
    for i in range(30):
        t0, t1 = i / 30, (i + 1) / 30
        ax.plot([x0 + (x1 - x0) * t0, x0 + (x1 - x0) * t1], [y0 + (y1 - y0) * t0, y0 + (y1 - y0) * t1],
                c=AMBER, lw=1 + 4 * t1, alpha=0.15 + 0.8 * t1, zorder=6, solid_capstyle="round")
    star(ax, x1, y1, 160, "#FFF3B0", z=7)
    T(ax, -0.30, 0.30, tx("c03_q"), 24, AMBER)
    T(ax, -0.30, 0.21, tx("c03_ro"), 13, WHITE, w="normal")


def c03_wed(ax):
    head(ax, tx("c03w_title"), tx("c03w_sub"), y=0.86)
    # 日月與婚冠
    ax.add_patch(CB.Circle((-0.50, 0.42), 0.075, fc=AMBER, ec="none", zorder=4))
    for k in range(12):
        a = math.radians(30 * k)
        ax.plot([-0.50 + 0.095 * math.cos(a), -0.50 + 0.125 * math.cos(a)],
                [0.42 + 0.095 * math.sin(a), 0.42 + 0.125 * math.sin(a)], c=AMBER, lw=2.5, zorder=4)
    ax.add_patch(CB.Circle((-0.22, 0.42), 0.070, fc="#FFF6D8", ec="none", zorder=4))
    ax.add_patch(CB.Circle((-0.19, 0.44), 0.062, fc=BG, ec="none", zorder=5))
    crown = [(-0.43, 0.24), (-0.43, 0.30), (-0.395, 0.27), (-0.36, 0.32), (-0.325, 0.27), (-0.29, 0.30), (-0.29, 0.24)]
    ax.add_patch(CB.Polygon(crown, closed=True, fc="none", ec=AMBER, lw=2.4, zorder=5))
    T(ax, -0.36, 0.15, tx("sunmoon"), 14, AMBER)
    # 星星＝火把
    import random
    rnd = random.Random(11)
    for _ in range(14):
        x, y = rnd.uniform(0.12, 0.85), rnd.uniform(0.28, 0.62)
        star(ax, x, y, rnd.choice((20, 35, 60)), "#FFF3B0")
        ax.plot([x, x], [y - 0.02, y - 0.07], c="#D9B48A", lw=2, alpha=.7, zorder=6)
    T(ax, 0.48, 0.20, tx("torch"), 14, "#FFF3B0")
    # 高山＝神父
    ax.add_patch(CB.Polygon([(-0.95, -0.40), (-0.62, 0.02), (-0.45, -0.14), (-0.25, 0.06), (0.02, -0.40)], closed=True,
                            fc="#3A4A6E", ec="#9FB3D9", lw=1.6, zorder=3))
    T(ax, -0.47, -0.30, tx("mount"), 14, WHITE)
    # 冷杉與楓樹＝賓客
    for i, x in enumerate((0.15, 0.27, 0.39, 0.51, 0.63, 0.75)):
        if i % 2 == 0:
            ax.add_patch(CB.Polygon([(x - 0.045, -0.36), (x + 0.045, -0.36), (x, -0.14)], closed=True,
                                    fc=GREEN, ec="none", alpha=.9, zorder=4))
        else:
            ax.plot([x, x], [-0.36, -0.26], c="#8B6B4A", lw=3, zorder=4)
            ax.add_patch(CB.Circle((x, -0.22), 0.055, fc="#C9763C", ec="none", alpha=.9, zorder=4))
    T(ax, 0.45, -0.44, tx("trees"), 14, GREEN)
    # 鳥＝樂師
    for x, y in ((0.05, 0.02), (0.15, 0.06), (0.25, 0.01)):
        ax.add_patch(CB.Arc((x - 0.02, y), 0.04, 0.03, theta1=0, theta2=180, ec=WHITE, lw=2, zorder=5))
        ax.add_patch(CB.Arc((x + 0.02, y), 0.04, 0.03, theta1=0, theta2=180, ec=WHITE, lw=2, zorder=5))
    T(ax, 0.40, 0.04, tx("birds"), 14, WHITE, ha="left")
    ax.plot([-0.95, 0.95], [-0.40, -0.40], c="#5C6E96", lw=1.4, zorder=3)
    T(ax, 0, -0.60, tx("c03w_ro"), 13, GREY, w="normal")


# ══════════════════ C-A23-04 小辭典（圖卡） ══════════════════
def c04_card(ax):
    T(ax, 0.5, 0.958, tx("c04_title"), 28, WHITE)
    T(ax, 0.5, 0.926, tx("c04_sub"), 9.5, GREY, w="normal")
    xs = (0.06, 0.47, 0.73)
    y = 0.895
    for x, k in zip(xs, ("col1", "col2", "col3")):
        T(ax, x, y, tx(k), 12, AMBER, ha="left")
    ax.plot([0.05, 0.95], [y - 0.014, y - 0.014], c=AMBER, lw=1, alpha=.6)
    rows = tx("rows")
    dy = 0.0262
    for i, (a, b, c) in enumerate(rows):
        yy = y - 0.036 - i * dy
        if i % 2 == 0:
            ax.add_patch(CB.Rectangle((0.05, yy - dy / 2), 0.90, dy, fc="#10162C", ec="none", zorder=0))
        T(ax, xs[0], yy, a, 10.0 if len(a) < 16 else 9.0, WHITE, ha="left")
        T(ax, xs[1], yy, b, 9.5 if len(b) < 9 else 8.3, WHITE, ha="left", w="normal")
        T(ax, xs[2], yy, c, 9.0 if len(c) < 7 else 8.0, GREY, ha="left", w="normal")
    yb = y - 0.036 - len(rows) * dy
    T(ax, 0.5, yb - 0.004, tx("c04_foot1"), 8.8, GREY, w="normal")
    T(ax, 0.5, yb - 0.024, tx("c04_foot2"), 8.3, GREY, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 11, WHITE, w="normal")


# ══════════════════ 地平座標 ══════════════════
def altaz(when, hips=(), planets=(), lat="25.0330", lon="121.5654", tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = lat, lon; o.pressure, o.temp, o.elevation = 1013, 15, 10
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    out = {}
    for k, b in planets:
        b.compute(o)
        out[k] = (math.degrees(b.alt), math.degrees(b.az))
    for k, h in hips:
        f = ephem.FixedBody(); f._ra, f._dec, f._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        f.compute(o)
        out[k] = (math.degrees(f.alt), math.degrees(f.az))
    return out


# ══════════════════ C-A23-05 這週末抬頭看（圖卡） ══════════════════
SKY20 = [("sirius", 32349), ("capella", 24608), ("reg", 49669), ("belt", 26311), ("pollux", 37826),
         ("procyon", 37279), ("aldeb", 21421)]


def c05_card(ax):
    import ephem
    T(ax, 0.5, 0.958, tx("c05_title"), 28, WHITE)
    # 全天圖（天頂在中心；北上、東左＝抬頭看）
    cx, cy, R = 0.5, 0.665, 0.30
    sq = 9 / 16
    T(ax, 0.5, 0.915, tx("c05_p1"), 13, GREY, w="normal")
    ax.add_patch(CB.Ellipse((cx, cy), 2 * R, 2 * R * sq, fc="#10162C", ec=WHITE, lw=1.2, zorder=1))
    Pz = lambda alt, az: (cx - R * (90 - alt) / 90 * math.sin(math.radians(az)),
                          cy + R * (90 - alt) / 90 * math.cos(math.radians(az)) * sq)
    for alt in (30, 60):
        ax.add_patch(CB.Ellipse((cx, cy), 2 * R * (90 - alt) / 90, 2 * R * (90 - alt) / 90 * sq,
                                fc="none", ec=GREY, lw=0.6, alpha=.5, zorder=2))
    for k, az, dx, dy in (("N", 0, 0, 0.018), ("S", 180, 0, -0.018), ("E", 90, -0.03, 0), ("W", 270, 0.03, 0)):
        x, y = Pz(0, az)
        T(ax, x + dx, y + dy, tx(k), 13, "#D9B48A")
    A = altaz("2027/2/26 20:00", hips=SKY20, planets=(("jup", ephem.Jupiter()), ("mars", ephem.Mars())))
    sty = {"sirius": (WHITE, 120, (0.0, -0.018)), "capella": (AMBER, 90, (0.0, 0.016)),
           "reg": (WHITE, 45, (0.02, -0.016)), "belt": (PURPLE, 30, (0.025, -0.008)),
           "pollux": (BLUE, 40, (0.0, 0.014)), "procyon": (GREEN, 50, (-0.02, -0.010)),
           "aldeb": (RED, 50, (0.025, 0.0)), "jup": (WHITE, 110, (0.0, 0.016)), "mars": (RED, 80, (-0.02, 0.011))}
    for k, (alt, az) in A.items():
        col, s, (dx, dy) = sty[k]
        x, y = Pz(alt, az)
        star(ax, x, y, s, col)
        ha = "left" if dx > 0.01 else ("right" if dx < -0.01 else "center")
        T(ax, x + dx, y + dy, tx(k), 10, col, ha=ha)
    # 清晨往東北
    x0, x1, y0, y1, alt1 = 0.08, 0.92, 0.155, 0.385, 56.0
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#10162C", ec=WHITE, lw=1.0, zorder=1))
    T(ax, 0.5, y1 + 0.020, tx("c05_p2"), 13, WHITE)
    gy = y0 + 0.030
    sy = (y1 - 0.03 - gy) / alt1
    sx = sy * 16 / 9
    az0 = 70.0 - (x1 - x0) / sx / 2
    Pp = lambda alt, az: (x0 + (az - az0) * sx, gy + alt * sy)
    ax.fill_between([x0 + 0.003, x1 - 0.003], [y0 + 0.003] * 2, [gy] * 2, color="#3A2E22", zorder=2)
    ax.plot([x0, x1], [gy, gy], c="#D9B48A", lw=1.6, zorder=3)
    for lab, az in ((tx("NE"), 45), (tx("ENE"), 67.5), (tx("E2"), 90)):
        T(ax, Pp(0, az)[0], gy - 0.015, lab, 10.5, "#D9B48A")
    B = altaz("2027/2/27 05:00", hips=(("vega5", VEGA), ("altair5", ALTAIR)))
    Qv = None
    for k, (alt, az) in B.items():
        x, y = Pp(alt, az)
        star(ax, x, y, 110 if k == "vega5" else 80, AMBER if k == "vega5" else GREEN)
        T(ax, x + 0.03, y + 0.008, tx(k), 11, AMBER if k == "vega5" else GREEN, ha="left")
        T(ax, x + 0.03, y - 0.011, f"{alt:.0f}°", 9, GREY, ha="left", w="normal")
    for i, (k, col, sz) in enumerate((("t1", WHITE, 9.5), ("t2", WHITE, 9.5), ("t3", GREY, 8.5))):
        T(ax, 0.5, 0.118 - i * 0.024, tx(k), sz, col, w="normal")
    T(ax, 0.5, 0.025, tx("tags"), 11, WHITE, w="normal")


# ══════════════════ C-A23-06 19:10 往西看 ══════════════════
WELL = [("markab", 113963), ("scheat", 113881), ("algenib", 1067), ("alph", 677)]
TROUGH = [5447, 9640, 3092]
X0, X1, GY, KAZ, AZC = -0.88, 0.88, -0.30, 0.0255, 282.0


def Pw(alt, az):
    return (az - AZC) * KAZ, GY + alt * KAZ


def c06_horizon(ax):
    head(ax, tx("c06_title"), tx("c06_sub"), y=0.80)
    ax.fill_between([X0, X1], [-0.62, -0.62], [GY, GY], color="#2A2418", zorder=2, lw=0)
    ax.plot([X0, X1], [GY, GY], c="#D9B48A", lw=2.0, zorder=3)
    for alt in (10, 20, 30):
        ax.plot([X0, X1], [GY + alt * KAZ] * 2, c=GREY, lw=0.6, alpha=.4, zorder=2, ls=(0, (4, 6)))
        T(ax, X1 + 0.01, GY + alt * KAZ, f"{alt}°", 10, GREY, ha="left", w="normal")
    for k, az in (("WSW", 247.5), ("W2", 270), ("WNW", 292.5), ("NW", 315)):
        x = Pw(0, az)[0]
        if X0 <= x <= X1:
            T(ax, x, GY - 0.05, tx(k), 14, "#D9B48A")
    T(ax, 0, -0.70, tx("c06_src"), 11, GREY, w="normal")


def c06_well(ax):
    A = altaz("2027/2/26 19:10", hips=WELL + [(f"t{h}", h) for h in TROUGH])
    pts = {}
    for k, (alt, az) in A.items():
        pts[k] = Pw(max(alt, -1.6), az), alt
    for a, b in (("alph", "scheat"), ("scheat", "markab"), ("markab", "algenib"), ("algenib", "alph")):
        (pa, aa), (pb, ab) = pts[a], pts[b]
        below = aa < 0 or ab < 0
        ax.plot([pa[0], pb[0]], [pa[1], pb[1]], c=BLUE, lw=2.6, alpha=.45 if below else 1.0,
                ls=(0, (3, 3)) if below else "-", zorder=5)
    seq = ["alph"] + [f"t{h}" for h in (3092, 5447, 9640)]
    ax.plot([pts[k][0][0] for k in seq], [pts[k][0][1] for k in seq], c=BLUE, lw=2.0, alpha=.8, zorder=5)
    for k, ((x, y), alt) in pts.items():
        star(ax, x, y, 60 if alt > 0 else 30, WHITE, alpha=1.0 if alt > 0 else 0.35, glow=alt > 0)
    lab = {"markab": (0.0, -0.13, RED), "scheat": (0.10, 0.03, WHITE), "algenib": (0.0, -0.065, WHITE),
           "alph": (0.11, 0.0, WHITE)}
    for k, (dx, dy, col) in lab.items():
        (x, y), alt = pts[k]
        T(ax, x + dx, y + dy, tx(k) + ("" if k == "markab" else f" {alt:.0f}°"), 12, col, w="normal")
    x, y = pts["t5447"][0]
    T(ax, x - 0.06, y, tx("trough"), 14, BLUE, ha="right")
    sq4 = [pts[k][0] for k in ("markab", "scheat", "algenib", "alph")]
    T(ax, min(p[0] for p in sq4) - 0.06, sum(p[1] for p in sq4) / 4, tx("well"), 14, BLUE, ha="right")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A23 概念圖 ──")
    t1 = "C-A23-01_Otescu的星圖與回信"
    CB.emit("", [("星圖", c01_chart), ("回信", c01_reply)], title=t1)
    CB.emit("", [("一年", c01_year)], title=t1, preview_name="一年預覽")
    t3 = "C-A23-03_Miorița"
    CB.emit("", [("山坡", c03_hill), ("流星", c03_star)], title=t3)
    CB.emit("", [("婚禮", c03_wed)], title=t3, preview_name="婚禮預覽")
    CB.emit("", [("地平線", c06_horizon), ("井", c06_well)], title="C-A23-06_19點10分往西看")
    for fn, name in ((c02_card, "C-A23-02_換了性別的牛郎織女_圖卡.png"),
                     (c04_card, "C-A23-04_羅馬尼亞星名小辭典_圖卡.png"),
                     (c05_card, "C-A23-05_這週末抬頭看_圖卡.png")):
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", name, transparent=False)


if __name__ == "__main__":
    main()
