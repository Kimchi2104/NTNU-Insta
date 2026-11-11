# -*- coding: utf-8 -*-
"""A-22 白俄羅斯：農民曆星空與以利亞的馬車｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A22-01 白俄羅斯在哪（地圖、森林湖泊）→ 02 鏡
C-A22-02 火車火馬（經文）→ 05 鏡
C-A22-03 雷聲車輪（車輪、閃電）→ 06 鏡
C-A22-04 白俄羅斯農民曆（年輪、節日、星）→ 07 鏡
C-A22-05 打乾草的一整套（割、耙、載；本片的串連）→ 10 鏡
C-A22-08 荊棘冠與十字架（北冕、天鵝縮圖）→ 13 鏡
C-A22-06 白俄羅斯星名小辭典（9:16 圖卡，可存圖）→ 16 鏡
C-A22-07 這幾天抬頭看（9:16 圖卡，可存圖；台北 2027/2/19、2/20 20:00）→ 17 鏡

做法：地圖是手描示意輪廓（非精確國界）；不畫聖像畫、不臨摹任何出版的插圖（要用聖像畫由美宣另尋授權）。
星圖縮圖＝以星群為中心的切平面投影（東在左、北在上），連線照 Stellarium belarusian。
經文：《列王紀下》2:11（和合本）。節日：Kaliady（冬天的節期，聖誕—主顯節）、Juraŭ（聖喬治節，舊曆 4/23＝5/6）、
Illia（以利亞節，舊曆 7/20＝8/2）。天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E UTC+8，15°C／1013 hPa）。

執行：python3 make_a22_diagrams.py            （中文，輸出 05_素材/A-22_白俄羅斯/_概念圖/）
      python3 make_a22_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-22_白俄羅斯/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND, FOREST, LAKE = "#FF6B6B", "#7C8BA8", "#2A3350", "#3E7A4E", "#4F86C6"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "白俄羅斯：東歐內陸", "c01_sub": "手描示意，非精確國界",
        "pl": "波蘭", "lt": "立陶宛", "lv": "拉脫維亞", "ru": "俄羅斯", "ua": "烏克蘭",
        "baltic": "波羅的海", "nosea": "沒有海岸線", "minsk": "明斯克 53.9°N",
        "forest": "四成是森林", "lakes": "上千座湖",
        "field1": "1994–2005 年的田野調查：", "field2": "村裡的老人還叫得出星星的名字",
        "field3": "Kanaplianikau 2008；Avilin 2008（Archaeologia Baltica 10）",
        "c02_title": "火車火馬", "c02_ref": "《列王紀下》2:11（和合本）",
        "c02_q1": "「他們正走著說話，", "c02_q2": "忽有火車火馬將二人隔開，", "c02_q3": "以利亞就乘旋風升天去了。」",
        "c02_note1": "經文是「乘旋風升天」；", "c02_note2": "「坐著火焰馬車升天」是民間與聖像畫的講法",
        "c03_title": "打雷＝以利亞駕車", "c03_wheel": "車輪滾過天空＝雷聲",
        "c03_bolt": "閃電＝他在追打魔鬼", "c03_src": "東斯拉夫民間說法（Ivanov & Toporov 1974 轉引）",
        "c04_title": "白俄羅斯農民曆", "c04_sub": "節日和天上的星",
        "months": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "f1": "Kaliady", "f1b": "冬天的節期", "f1s": "坐著大車 Voz 來",
        "f2": "聖喬治節", "f2b": "5 月初・趕牛上草地", "f2s": "天龍＝他殺的蛇 Zmiej",
        "f3": "以利亞節", "f3b": "8 月初・雷雨、收麥", "f3s": "北斗＝以利亞的車",
        "f3p": "更早：雷神 Perun（一說）",
        "c04_foot": "東正教舊曆 4/23＝5/6、7/20＝8/2",
        "c05_title": "本片的串連：割・耙・載", "c05_sub": "三個都是白俄羅斯星名；放在一起看是我們的串連",
        "mow": "割", "mow2": "Kastsy 割草的人", "rake": "耙", "rake2": "Hrabli 耙子", "cart": "載", "cart2": "Voz 大車",
        "c08_title": "後來蓋上的一層教堂", "crown": "Karona", "crown2": "荊棘冠（北冕）",
        "cross": "Piatroŭ krest", "cross2": "聖彼得的十字架（天鵝）",
        "c08_foot": "台北 20:00 兩個都還在地平線下",
        "c06_title": "白俄羅斯星名小辭典", "c06_sub": "Stellarium belarusian（Avilin 等）；片中拼法依白俄語讀音",
        "col1": "片中拼法", "col2": "意思", "col3": "星",
        "rows": [("Voz　Воз", "大車", "北斗"), ("Illioŭ voz　Іллёў воз", "以利亞的車", "北斗"),
                 ("Maly voz　Малы воз", "小車", "小熊"), ("Hvozdz　Гвоздзь", "釘子", "北極星"),
                 ("Kastsy　Касцы", "割草的人", "獵戶腰帶"), ("Hrabli　Граблі", "耙子", "獵戶的劍下方"),
                 ("Rataj　Ратай", "犁田的人", "牧夫"), ("Sita　Сіта", "篩子", "后髮*"),
                 ("Kurki　Куркі", "母雞", "昴宿"), ("Vuzhy　Вужы", "草蛇", "畢宿"),
                 ("Kaza　Каза", "母山羊", "五車二"), ("Baran　Баран", "公羊", "白羊"),
                 ("Kaziaroh　Казярог", "野山羊", "摩羯"), ("Husinaja daroha", "鵝之路", "銀河"),
                 ("Kreselca Pana Jezusa", "耶穌的椅子", "獵戶"), ("Karona　Карона", "荊棘冠", "北冕"),
                 ("Piatroŭ krest", "聖彼得的十字架", "天鵝"), ("Zmiej　Змей", "聖喬治殺的蛇", "天龍"),
                 ("Niaviesta　Нявеста", "新娘", "天琴"), ("Blizniuki　Блізнюкі", "雙胞胎", "雙子"),
                 ("（波蘭和立陶宛）", "兩個國家", "北河二、三")],
        "c06_foot1": "* Stellarium 標在后髮座；也有資料說篩子是昴宿",
        "c06_foot2": "Avilin 2008；Kanaplianikau 2008；Stellarium belarusian",
        "c07_title": "這幾天抬頭看", "c07_date": "台北・往東看・晚上 8 點",
        "p19": "2/19（五）20:00", "p20": "2/20（六・元宵）20:00",
        "moon": "月亮", "jup": "木星", "mars": "火星", "reg": "軒轅十四", "E": "東", "ENE": "東北東", "ESE": "東南東",
        "t1": "火星 2/19 23:51 衝日・2/20 上午 8 點前後最近（1.01 億公里）",
        "t2": "天一黑：割草的人（獵戶腰帶）在南方高空",
        "t3": "21:00 以後：北斗從東北方爬上來",
        "t4": "PyEphem 自算；高度含大氣折射",
        "tags": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Belarus: inland Eastern Europe", "c01_sub": "Schematic, not exact borders",
        "pl": "Poland", "lt": "Lithuania", "lv": "Latvia", "ru": "Russia", "ua": "Ukraine",
        "baltic": "Baltic Sea", "nosea": "no coastline", "minsk": "Minsk 53.9°N",
        "forest": "40% forest", "lakes": "thousands of lakes",
        "field1": "Fieldwork, 1994–2005:", "field2": "village elders still knew the star names",
        "field3": "Kanaplianikau 2008; Avilin 2008 (Archaeologia Baltica 10)",
        "c02_title": "Chariot of fire, horses of fire", "c02_ref": "2 Kings 2:11",
        "c02_q1": "“As they were still going on and talking,", "c02_q2": "a chariot of fire and horses of fire separated them,",
        "c02_q3": "and Elijah went up by a whirlwind into heaven.”",
        "c02_note1": "The text says “by a whirlwind”;", "c02_note2": "riding the fiery chariot up is folk and icon tradition",
        "c03_title": "Thunder = Elijah driving", "c03_wheel": "wheels rolling across the sky = thunder",
        "c03_bolt": "lightning = chasing the devil", "c03_src": "East Slavic folk belief (cited in Ivanov & Toporov 1974)",
        "c04_title": "A Belarusian farmer's calendar", "c04_sub": "feasts and their stars",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "f1": "Kaliady", "f1b": "the winter feast", "f1s": "arrives on the Cart, Voz",
        "f2": "St George's Day", "f2b": "early May · cattle out to pasture", "f2s": "Draco = his slain serpent",
        "f3": "St Elijah's Day", "f3b": "early Aug · storms, harvest", "f3s": "Big Dipper = Elijah's cart",
        "f3p": "earlier: the thunder god Perun (one view)",
        "c04_foot": "Old-calendar Apr 23 = May 6, Jul 20 = Aug 2",
        "c05_title": "Our reading: mow · rake · haul", "c05_sub": "Three Belarusian star names; putting them together is ours",
        "mow": "Mow", "mow2": "Kastsy, the Mowers", "rake": "Rake", "rake2": "Hrabli, the Rake",
        "cart": "Haul", "cart2": "Voz, the Cart",
        "c08_title": "A church built over the sky", "crown": "Karona", "crown2": "Crown of thorns (CrB)",
        "cross": "Piatroŭ krest", "cross2": "St Peter's cross (Cygnus)",
        "c08_foot": "Both still below Taipei's horizon at 8 p.m.",
        "c06_title": "Belarusian star names", "c06_sub": "Stellarium belarusian (Avilin et al.); spellings follow Belarusian",
        "col1": "Name", "col2": "Meaning", "col3": "Stars",
        "rows": [("Voz　Воз", "the Cart", "Big Dipper"), ("Illioŭ voz", "Elijah's cart", "Big Dipper"),
                 ("Maly voz", "the Small Cart", "Little Dipper"), ("Hvozdz", "the Nail", "Polaris"),
                 ("Kastsy", "the Mowers", "Orion's Belt"), ("Hrabli", "the Rake", "below Orion's sword"),
                 ("Rataj", "the Ploughman", "Boötes"), ("Sita", "the Sieve", "Coma Ber.*"),
                 ("Kurki", "the Hens", "Pleiades"), ("Vuzhy", "the Grass Snakes", "Hyades"),
                 ("Kaza", "the She-Goat", "Capella"), ("Baran", "the Ram", "Aries"),
                 ("Kaziaroh", "the Wild Goat", "Capricornus"), ("Husinaja daroha", "the Goose's Way", "Milky Way"),
                 ("Kreselca Pana Jezusa", "Jesus' chair", "Orion"), ("Karona", "crown of thorns", "Corona Bor."),
                 ("Piatroŭ krest", "St Peter's cross", "Cygnus"), ("Zmiej", "St George's serpent", "Draco"),
                 ("Niaviesta", "the Bride", "Lyra"), ("Blizniuki", "the Twins", "Gemini"),
                 ("(Poland and Lithuania)", "two countries", "Castor, Pollux")],
        "c06_foot1": "* Stellarium puts the Sieve in Coma; some sources say the Pleiades",
        "c06_foot2": "Avilin 2008; Kanaplianikau 2008; Stellarium belarusian",
        "c07_title": "Look up this week", "c07_date": "Taipei · facing east · 8 p.m.",
        "p19": "Fri Feb 19, 20:00", "p20": "Sat Feb 20 (Lantern Festival), 20:00",
        "moon": "Moon", "jup": "Jupiter", "mars": "Mars", "reg": "Regulus", "E": "E", "ENE": "ENE", "ESE": "ESE",
        "t1": "Mars at opposition Feb 19 23:51; closest Feb 20 ~8 a.m. (101 million km)",
        "t2": "At dusk: the Mowers (Orion's Belt) high in the south",
        "t3": "After 9 p.m.: the Big Dipper climbs in the northeast",
        "t4": "Computed with PyEphem; altitudes include refraction",
        "tags": "#WorldSkyCultures　#NTNUAstronomy",
    },
}


def tx(k):
    return TXT[LANG][k]


def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12, va="center"):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=c, ha=ha, va=va, weight=w,
            alpha=alpha, zorder=z)


def head(ax, title, sub=None, y=0.90):
    T(ax, 0, y, title, 30, WHITE)
    if sub:
        T(ax, 0, y - 0.09, sub, 15, GREY, w="normal")


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


def mini_chart(ax, segs, cx, cy, size, col, extra=(), lw=2.6, sq=1.0, rot=0.0):
    """星群縮圖：以星群中心切平面投影，縮放到 size（最大邊），sq＝y 軸比例（圖卡 9:16 用 9/16）"""
    hs = sorted({h for s in segs for h in s} | set(extra))
    ra0 = math.degrees(math.atan2(sum(math.sin(math.radians(S[h][0])) for h in hs),
                                  sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    de0 = sum(S[h][1] for h in hs) / len(hs)
    P = {h: tangent(h, ra0, de0) for h in hs}
    if rot:
        c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        P = {h: (x * c - y * s_, x * s_ + y * c) for h, (x, y) in P.items()}
    xs, ys = [p[0] for p in P.values()], [p[1] for p in P.values()]
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    k = size / max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
    Q = {h: (cx + (x - mx) * k, cy + (y - my) * k * sq) for h, (x, y) in P.items()}
    for seg in segs:
        ax.plot([Q[h][0] for h in seg], [Q[h][1] for h in seg], c=col, lw=lw, zorder=5, solid_capstyle="round")
    for h in hs:
        v = S[h][2]
        star(ax, *Q[h], max(10, max(0.3, 6.5 - v) ** 1.7 * 9), WHITE, glow=v < 2.5)
    return Q


# Stellarium belarusian 連線
CART = [[67301, 65378, 62956, 59774, 58001, 53910, 54061, 59774]]
MOW = [[26727, 26311, 25930]]
RAKE = [[26263, 26173, 26563], [26173, 25923]]
CROWN = [[76127, 75695, 76267, 76952, 77512, 78159, 78493]]
CROSS = [[102098, 100453, 97165], [100453, 102488], [100453, 95947]]


# ══════════════════ C-A22-01 白俄羅斯在哪 ══════════════════
LON0, LAT0, KX, KY = 28.0, 53.6, 0.090, 0.150        # 經度×cos54° 壓扁
BY = [(23.6, 51.5), (23.2, 52.2), (23.6, 52.7), (23.9, 53.2), (23.5, 53.9), (24.4, 53.9), (25.5, 54.2),
      (25.7, 54.8), (26.6, 55.2), (26.9, 55.7), (28.2, 56.1), (29.4, 55.8), (30.9, 55.6), (30.8, 55.1),
      (31.7, 54.3), (31.3, 53.8), (32.5, 53.3), (32.7, 52.9), (31.8, 52.1), (30.9, 52.0), (30.6, 51.3),
      (29.3, 51.4), (28.0, 51.6), (26.5, 51.8), (25.2, 51.9), (24.0, 51.6)]
COAST = [(18.5, 54.6), (19.6, 54.4), (21.0, 55.3), (21.1, 56.4), (21.0, 57.0), (21.9, 57.6), (23.0, 57.1),
         (24.2, 57.0), (24.4, 57.9)]          # 波蘭—立陶宛—拉脫維亞海岸（示意）


def P(lon, lat):
    return (lon - LON0) * KX + 0.10, (lat - LAT0) * KY - 0.05


def c01_map(ax):
    head(ax, tx("c01_title"), tx("c01_sub"))
    ax.add_patch(CB.Polygon([P(*q) for q in BY], closed=True, fc=LAND, ec="#9FB3D9", lw=2.0, zorder=3))
    cx = [P(*q) for q in COAST]
    ax.plot([p[0] for p in cx], [p[1] for p in cx], c=LAKE, lw=2.4, zorder=2)
    T(ax, P(19.0, 56.0)[0], P(19.0, 56.0)[1], tx("baltic"), 15, LAKE, w="normal")
    for k, lon, lat in (("pl", 21.6, 52.6), ("lt", 24.6, 55.5), ("lv", 25.8, 56.7), ("ru", 33.8, 55.2),
                        ("ua", 28.6, 50.95)):
        T(ax, *P(lon, lat), tx(k), 16, GREY)
    mx, my = P(27.57, 53.90)
    star(ax, mx, my, 110, AMBER)
    T(ax, mx, my - 0.06, tx("minsk"), 15, AMBER)


def c01_forest(ax):
    import random
    rnd = random.Random(7)
    from matplotlib.path import Path
    poly = Path([P(*q) for q in BY])
    n = 0
    while n < 70:
        x, y = rnd.uniform(-0.35, 0.55), rnd.uniform(-0.40, 0.30)
        if not poly.contains_point((x, y)) or math.hypot(x - P(27.57, 53.9)[0], y - P(27.57, 53.9)[1]) < 0.09:
            continue
        ax.add_patch(CB.Polygon([(x - 0.018, y - 0.02), (x + 0.018, y - 0.02), (x, y + 0.03)], closed=True,
                                fc=FOREST, ec="none", alpha=.85, zorder=4))
        n += 1
    m = 0
    while m < 14:
        x, y = rnd.uniform(-0.30, 0.50), rnd.uniform(-0.30, 0.30)
        if not poly.contains_point((x, y)):
            continue
        ax.add_patch(CB.Ellipse((x, y), 0.035, 0.018, fc=LAKE, ec="none", alpha=.9, zorder=4))
        m += 1
    T(ax, -0.66, -0.56, tx("forest"), 19, FOREST, ha="left")
    T(ax, 0.70, -0.56, tx("lakes"), 19, LAKE, ha="right")
    T(ax, 0, -0.64, tx("field1"), 16, WHITE, w="normal")
    T(ax, 0, -0.72, tx("field2"), 20, AMBER)
    T(ax, 0, -0.81, tx("field3"), 11, GREY, w="normal")


# ══════════════════ C-A22-02 火車火馬 ══════════════════
def c02_verse(ax):
    head(ax, tx("c02_title"), tx("c02_ref"), y=0.42)
    for i, k in enumerate(("c02_q1", "c02_q2", "c02_q3")):
        T(ax, 0, 0.12 - i * 0.14, tx(k), 22 if LANG == "zh" else 15, AMBER if i == 1 else WHITE)
    T(ax, 0, -0.36, tx("c02_note1"), 13, GREY, w="normal")
    T(ax, 0, -0.43, tx("c02_note2"), 13, GREY, w="normal")


# ══════════════════ C-A22-03 雷聲車輪 ══════════════════
def c03_wheel(ax):
    head(ax, tx("c03_title"), y=0.70)
    cx, cy, r = -0.25, 0.05, 0.26
    ax.add_patch(CB.Circle((cx, cy), r, fc="none", ec=AMBER, lw=6, zorder=5))
    ax.add_patch(CB.Circle((cx, cy), 0.045, fc=AMBER, ec="none", zorder=5))
    for k in range(10):
        a = math.radians(36 * k)
        ax.plot([cx, cx + r * math.cos(a)], [cy, cy + r * math.sin(a)], c=AMBER, lw=3, zorder=5)
    for i, rr in enumerate((0.34, 0.41, 0.48)):        # 聲波（雷聲）
        ax.add_patch(CB.Arc((cx, cy), 2 * rr, 2 * rr, theta1=150, theta2=210, ec=WHITE, lw=2.2,
                            alpha=.55 - i * 0.13, zorder=4))
    for dx in (0.06, 0.13, 0.20):                      # 速度線
        ax.plot([cx + r + dx - 0.02, cx + r + dx + 0.05], [cy - 0.10 + dx * 0.4, cy - 0.10 + dx * 0.4],
                c=WHITE, lw=2, alpha=.45, zorder=4)
    T(ax, cx, cy - r - 0.10, tx("c03_wheel"), 16, AMBER)


def c03_bolt(ax):
    pts = [(0.38, 0.42), (0.24, 0.10), (0.33, 0.10), (0.20, -0.25), (0.42, 0.05), (0.33, 0.05), (0.46, 0.42)]
    ax.add_patch(CB.Polygon(pts, closed=True, fc="#FFF3B0", ec=AMBER, lw=2, zorder=6))
    T(ax, 0.33, -0.33, tx("c03_bolt"), 16, "#FFF3B0")
    T(ax, 0, -0.55, tx("c03_src"), 11, GREY, w="normal")


# ══════════════════ C-A22-04 白俄羅斯農民曆 ══════════════════
R0 = 0.50


def mpos(month_float, r=R0):
    """月份 → 圓上位置（1 月 1 日在正上方，順時針）"""
    a = math.radians(90 - (month_float - 1) * 30)
    return r * math.cos(a), r * math.sin(a) - 0.06


def c04_ring(ax):
    head(ax, tx("c04_title"), tx("c04_sub"))
    ax.add_patch(CB.Circle((0, -0.06), R0, fc="none", ec=WHITE, lw=2.2, alpha=.7, zorder=3))
    for i, mn in enumerate(tx("months")):
        x, y = mpos(i + 1)
        x2, y2 = mpos(i + 1, R0 + 0.035)
        ax.plot([x, x2], [y, y2], c=WHITE, lw=1.6, alpha=.7, zorder=3)
        T(ax, *mpos(i + 1.5, R0 - 0.07), mn, 11, GREY, w="normal")
    T(ax, 0, -0.86, tx("c04_foot"), 11, GREY, w="normal")


FEASTS = [  # (月份, 名稱鍵, 說明鍵, 星鍵, 顏色, 外推方向)
    (1.2, "f1", "f1b", "f1s", AMBER, (-0.05, 0.0)),
    (5.2, "f2", "f2b", "f2s", RED, (0.0, 0.0)),
    (8.05, "f3", "f3b", "f3s", RED, (0.0, 0.0)),
]


def c04_feasts(ax):
    for mf, k1, k2, _, col, _ in FEASTS:
        x, y = mpos(mf)
        star(ax, x, y, 160, col)
        ox, oy = mpos(mf, R0 + 0.20)
        ha = "center" if abs(ox) < 0.1 else ("left" if ox > 0 else "right")
        if k1 == "f1":
            ox, oy, ha = x + 0.06, y + 0.06, "left"
        T(ax, ox, oy + 0.03, tx(k1), 17, col, ha=ha)
        T(ax, ox, oy - 0.03, tx(k2), 11.5, WHITE, ha=ha, w="normal")


def c04_stars(ax):
    for mf, _, _, ks, col, _ in FEASTS:
        x, y = mpos(mf, R0 - 0.27)
        T(ax, x * 0.9, y, tx(ks), 12, col, w="normal")
    x, y = mpos(8.05, R0 - 0.27)
    T(ax, x * 0.9 + 0.04, y - 0.06, tx("f3p"), 10.5, GREY, w="normal")


# ══════════════════ C-A22-05 打乾草的一整套 ══════════════════
PANELS = [(-0.62, "mow", "mow2", MOW, AMBER, (), 0.30),
          (0.0, "rake", "rake2", RAKE, GREEN, [26727, 26311, 25930], 0.30),
          (0.62, "cart", "cart2", CART, AMBER, (), 0.42)]


def _panel(i):
    x, k1, k2, segs, col, extra, size = PANELS[i]

    def f(ax):
        if i == 0:
            head(ax, tx("c05_title"), tx("c05_sub"), y=0.55)
        ax.add_patch(CB.FancyBboxPatch((x - 0.27, -0.42), 0.54, 0.75, boxstyle="round,pad=0.0,rounding_size=0.04",
                                       fc="#10162C", ec=col, lw=1.4, zorder=1))
        T(ax, x, 0.24, tx(k1), 30, col)
        mini_chart(ax, segs, x, -0.06, size, col, extra=extra)
        T(ax, x, -0.34, tx(k2), 13, WHITE, w="normal")
        if i < 2:
            CB.arrow(ax, (x + 0.36, -0.06), (x + 0.27, -0.06), c=GREY, lw=2, alpha=.8, style="-|>")
    return f


# ══════════════════ C-A22-08 荊棘冠與十字架 ══════════════════
def c08_crown(ax):
    head(ax, tx("c08_title"), y=0.62)
    x = -0.42
    ax.add_patch(CB.FancyBboxPatch((x - 0.36, -0.46), 0.72, 0.88, boxstyle="round,pad=0.0,rounding_size=0.04",
                                   fc="#10162C", ec=RED, lw=1.4, zorder=1))
    mini_chart(ax, CROWN, x, 0.02, 0.48, RED)
    T(ax, x, -0.28, tx("crown"), 20, RED)
    T(ax, x, -0.37, tx("crown2"), 13, WHITE, w="normal")


def c08_cross(ax):
    x = 0.42
    ax.add_patch(CB.FancyBboxPatch((x - 0.36, -0.46), 0.72, 0.88, boxstyle="round,pad=0.0,rounding_size=0.04",
                                   fc="#10162C", ec=BLUE, lw=1.4, zorder=1))
    mini_chart(ax, CROSS, x, 0.04, 0.50, BLUE, rot=-30)
    T(ax, x, -0.28, tx("cross"), 20, BLUE)
    T(ax, x, -0.37, tx("cross2"), 13, WHITE, w="normal")
    T(ax, 0, -0.56, tx("c08_foot"), 12, GREY, w="normal")


# ══════════════════ C-A22-06 小辭典（圖卡） ══════════════════
def c06_card(ax):
    T(ax, 0.5, 0.955, tx("c06_title"), 30, WHITE)
    T(ax, 0.5, 0.922, tx("c06_sub"), 10.5, GREY, w="normal")
    xs = (0.06, 0.56, 0.78)
    y = 0.885
    for x, k in zip(xs, ("col1", "col2", "col3")):
        T(ax, x, y, tx(k), 13, AMBER, ha="left")
    ax.plot([0.05, 0.95], [y - 0.015, y - 0.015], c=AMBER, lw=1, alpha=.6)
    rows = tx("rows")
    dy = 0.0365
    for i, (a, b, c) in enumerate(rows):
        yy = y - 0.040 - i * dy
        if i % 2 == 0:
            ax.add_patch(CB.Rectangle((0.05, yy - dy / 2), 0.90, dy, fc="#10162C", ec="none", zorder=0))
        T(ax, xs[0], yy, a, 11.0, WHITE, ha="left")
        T(ax, xs[1], yy, b, 10.5 if len(b) < 7 else 9.0, WHITE, ha="left", w="normal")
        T(ax, xs[2], yy, c, 10.0 if len(c) < 6 else 8.5, GREY, ha="left", w="normal")
    yb = y - 0.040 - len(rows) * dy
    T(ax, 0.5, yb - 0.005, tx("c06_foot1"), 9.5, GREY, w="normal")
    T(ax, 0.5, yb - 0.028, tx("c06_foot2"), 9.0, GREY, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 12, WHITE, w="normal")


# ══════════════════ C-A22-07 這幾天抬頭看（圖卡） ══════════════════
def altaz(when, lat="25.0330", lon="121.5654", tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = lat, lon; o.pressure, o.temp, o.elevation = 1013, 15, 10
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    out = {}
    for k, b in (("moon", ephem.Moon()), ("jup", ephem.Jupiter()), ("mars", ephem.Mars())):
        b.compute(o)
        out[k] = (math.degrees(b.alt), math.degrees(b.az))
    f = ephem.FixedBody(); f._ra, f._dec, f._epoch = math.radians(S[49669][0]), math.radians(S[49669][1]), ephem.J2000
    f.compute(o)
    out["reg"] = (math.degrees(f.alt), math.degrees(f.az))
    return out


def east_panel(ax, y0, y1, title, A):
    x0, x1, alt1 = 0.08, 0.92, 56.0
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#10162C", ec=WHITE, lw=1.0, zorder=1))
    gy = y0 + 0.035
    # 等角：方位 1° 與高度 1° 在圖卡上一樣長（圖卡 x:y＝9:16）
    sy = (y1 - 0.03 - gy) / alt1
    sx = sy * 16 / 9
    az0 = 90.0 - (x1 - x0) / sx / 2
    Pp = lambda alt, az: (x0 + (az - az0) * sx, gy + alt * sy)
    ax.fill_between([x0 + 0.003, x1 - 0.003], [y0 + 0.003] * 2, [gy] * 2, color="#3A2E22", zorder=2)
    ax.plot([x0, x1], [gy, gy], c="#D9B48A", lw=1.6, zorder=3)
    for lab, az in ((tx("ENE"), 67.5), (tx("E"), 90), (tx("ESE"), 112.5)):
        T(ax, Pp(0, az)[0], gy - 0.017, lab, 11, "#D9B48A")
    T(ax, 0.5, y1 + 0.020, title, 14, WHITE)
    sty = {"moon": ("#FFF6D8", 260, 0.055, 0.008), "jup": (WHITE, 110, -0.045, 0.0),
           "mars": (RED, 80, -0.045, 0.0), "reg": ("#CFE0FF", 45, 0.045, -0.012)}
    for k, (alt, az) in A.items():
        if alt > alt1 - 2:
            continue
        col, s, dx, dy = sty[k]
        x, y = Pp(alt, az)
        star(ax, x, y, s, col)
        ha = "left" if dx > 0 else ("right" if dx < 0 else "center")
        T(ax, x + dx, y + dy + 0.008, tx(k), 12, col, ha=ha)
        T(ax, x + dx, y + dy - 0.010, f"{alt:.0f}°", 9.5, GREY, ha=ha, w="normal")


def c07_card(ax):
    T(ax, 0.5, 0.955, tx("c07_title"), 30, WHITE)
    T(ax, 0.5, 0.918, tx("c07_date"), 14, GREY, w="normal")
    east_panel(ax, 0.545, 0.860, tx("p19"), altaz("2027/2/19 20:00"))
    east_panel(ax, 0.185, 0.500, tx("p20"), altaz("2027/2/20 20:00"))
    for i, (k, col, sz) in enumerate((("t1", RED, 11), ("t2", AMBER, 11), ("t3", AMBER, 11), ("t4", GREY, 9))):
        T(ax, 0.5, 0.150 - i * 0.026, tx(k), sz, col, w="normal")
    T(ax, 0.5, 0.025, tx("tags"), 12, WHITE, w="normal")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A22 概念圖 ──")
    CB.emit("", [("地圖", c01_map), ("森林湖泊", c01_forest)], title="C-A22-01_白俄羅斯在哪")
    CB.emit("", [("經文", c02_verse)], title="C-A22-02_火車火馬")
    CB.emit("", [("車輪", c03_wheel), ("閃電", c03_bolt)], title="C-A22-03_雷聲車輪")
    CB.emit("", [("年輪", c04_ring), ("節日", c04_feasts), ("星", c04_stars)], title="C-A22-04_白俄羅斯農民曆")
    CB.emit("", [("割", _panel(0)), ("耙", _panel(1)), ("載", _panel(2))], title="C-A22-05_打乾草的一整套")
    CB.emit("", [("北冕", c08_crown), ("天鵝", c08_cross)], title="C-A22-08_荊棘冠與十字架")
    for fn, name in ((c06_card, "C-A22-06_白俄羅斯星名小辭典_圖卡.png"), (c07_card, "C-A22-07_這幾天抬頭看_圖卡.png")):
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", name, transparent=False)


if __name__ == "__main__":
    main()
