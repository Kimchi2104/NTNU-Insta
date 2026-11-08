# -*- coding: utf-8 -*-
"""A-19 古阿拉伯｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A19-01_兩層阿拉伯星空       → 02 鏡（今日層→古詩層）
  C-A19-02_抄錯一個字母         → 06 鏡（原字層→抄錯層）
  C-A19-03_看得到Suhail的地方   → 08 鏡（緯度層→城市層）
  C-A19-04_擋路的Suhail         → 11 鏡（商道層→星星層）
  C-A19-05_310光年              → 12 鏡（距離層→南極老人層）
  C-A19-06_這週末抬頭看         → 13 鏡（9:16 圖卡，可存圖）
  C-A19-07_沙漠動物園小辭典     → IG 輪播（13 鏡角落小貼紙提示；9:16 圖卡）
輸出：05_素材/A-19_古阿拉伯/_概念圖/（--lang en → _概念圖/en/）

來源（數字與逐字稿 v1「星空對時」一致；圖卡的高度方位由 PyEphem 現算）：
  Stellarium arabic_indigenous（al-Ajaji；names_dictionary）；Kunitzsch & Smart《A Dictionary of Modern Star
  Names》（Azha＜udḥiyy、Alula／Tania／Talitha）；IAU WGSN 2016；Hipparcos（van Leeuwen 2007）視差：
  老人星 309 光年、天狼星 8.6 光年；絕對星等 −5.62 vs +1.43 → 約 660 倍；《史記・天官書》；
  「Suhail 收過路稅」：Ibn al-Jawzī《al-Mawḍūʿāt》收為偽託的傳述。地圖不畫海岸線，只畫緯度（自繪示意）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-19_古阿拉伯/_概念圖")
C.set_base(OUT)
RED, GREY, SAND = "#FF6B6B", "#7C8BA8", "#C9A66B"
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "兩層阿拉伯星空", "now": "今天：納季德的星曆", "now2": "A-13：農牧時令（Thurayya、Suhail⋯）",
        "old": "這一集：更古老的那一層", "s1": "貝都因古詩", "s1b": "伊斯蘭以前", "s2": "學者抄錄",
        "s2b": "8–10 世紀\nIbn Qutayba（卒約 889）\nal-Ṣūfī（約 964）", "s3": "Stellarium", "s3b": "arabic_indigenous\nal-Ajaji 整理",
        "c02_title": "抄錯一個字母", "orig": "udḥiyy　鴕鳥窩", "copy": "中世紀抄本　azḥā", "dz": "d → z",
        "iau": "IAU 2016 正式名：Azha（η Eri）",
        "c03_title": "看得到 Suhail 的地方", "c03_sub": "老人星的最高仰角（自繪示意，只畫緯度）",
        "limit": "37.3°N 以北：老人星升不起來", "arab": "阿拉伯", "tw": "台灣",
        "Damascus": "大馬士革", "Riyadh": "利雅德", "Mecca": "麥加", "Sanaa": "沙那（也門）",
        "Taipei": "台北", "Kenting": "墾丁", "lat": "北緯",
        "c04_title": "「擋路的 Suhail」", "road": "也門的商道", "toll": "攔路收稅",
        "star": "被變成了星星", "c04_note": "出自伊斯蘭時代的傳述・學者判為不可靠",
        "c05_title": "老人星有多遠？", "sun": "太陽", "sir": "天狼星 8.6 光年", "can": "老人星 309 光年",
        "far": "遠 36 倍", "bright": "本身亮度：老人星約是天狼星的 660 倍", "bright2": "所以看起來只暗一點",
        "old_cn": "在中國：南極老人（壽星）", "quote": "「老人見，治安；不見，兵起。」", "src": "《史記・天官書》",
        "xian": "見＝現", "ly": "光年",
        "c06_title": "這週末抬頭看：Suhail", "c06_date": "2027/1/29（五）台北・面向正南",
        "S": "南", "SE": "東南", "SW": "西南", "c06_can": "老人星", "c06_sir": "天狼星",
        "c06_t": "21:43 正南 12°", "n1": "要找南方完全沒有遮擋的地方", "n2": "墾丁鵝鑾鼻：15°（21:47）",
        "n3": "月亮 1/30 00:31 才升起，整晚沒有月光", "n4": "一月中到三月初，晚上 8–11 點最好找",
        "c06_src": "PyEphem 自算（含大氣折射）",
        "c07_title": "沙漠動物園小辭典", "c07_sub": "古阿拉伯星名（Stellarium arabic_indigenous）",
        "c07_src": "al-Ajaji《names_dictionary》；Kunitzsch & Smart（Azha、Alula／Tania／Talitha）",
    },
    "en": {
        "c01_title": "Two layers of the Arabian sky", "now": "Today: the Najdi star calendar",
        "now2": "A-13: seasons for herding and farming (Thurayya, Suhail…)",
        "old": "This episode: the older layer", "s1": "Bedouin poetry", "s1b": "before Islam", "s2": "Scholars write it down",
        "s2b": "8th–10th c.\nIbn Qutayba (d. c. 889)\nal-Ṣūfī (c. 964)", "s3": "Stellarium", "s3b": "arabic_indigenous\ncompiled by al-Ajaji",
        "c02_title": "One letter miscopied", "orig": "udḥiyy  ostrich nest", "copy": "medieval copy  azḥā", "dz": "d → z",
        "iau": "IAU 2016 official name: Azha (η Eri)",
        "c03_title": "Where Suhail can be seen", "c03_sub": "Highest altitude of Canopus (schematic, latitudes only)",
        "limit": "North of 37.3°N: Canopus never rises", "arab": "Arabia", "tw": "Taiwan",
        "Damascus": "Damascus", "Riyadh": "Riyadh", "Mecca": "Mecca", "Sanaa": "Sanaa (Yemen)",
        "Taipei": "Taipei", "Kenting": "Kenting", "lat": "Lat.",
        "c04_title": "“Suhail who blocked the road”", "road": "Trade road in Yemen", "toll": "levying tolls",
        "star": "turned into a star", "c04_note": "From an Islamic-era report that scholars judge unreliable",
        "c05_title": "How far is Canopus?", "sun": "Sun", "sir": "Sirius 8.6 ly", "can": "Canopus 309 ly",
        "far": "36× farther", "bright": "Intrinsically about 660× brighter than Sirius", "bright2": "so it looks only a little fainter",
        "old_cn": "In China: the Old Man of the South Pole", "quote": "“When the Old Man appears, there is peace; when not, war.”",
        "src": "Shiji, Treatise on the Celestial Offices", "xian": "", "ly": "ly",
        "c06_title": "This weekend: Suhail", "c06_date": "Fri 29 Jan 2027, Taipei · facing south",
        "S": "S", "SE": "SE", "SW": "SW", "c06_can": "Canopus", "c06_sir": "Sirius",
        "c06_t": "21:43 due south, 12°", "n1": "Find a clear southern horizon", "n2": "Kenting (Eluanbi): 15° (21:47)",
        "n3": "Moonrise 00:31 on 1/30: a dark evening", "n4": "Mid-January to early March, 8–11 pm is best",
        "c06_src": "PyEphem (with refraction)",
        "c07_title": "A desert-zoo glossary", "c07_sub": "Old Arabic star names (Stellarium arabic_indigenous)",
        "c07_src": "al-Ajaji, names_dictionary; Kunitzsch & Smart (Azha, Alula/Tania/Talitha)",
    },
}


def tx(k):
    return TXT[LANG][k]


def box(ax, x, y, w, h, col, a=1.0):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                fc="#1B2240", ec=col, lw=2.0, alpha=a, zorder=3))


# ══════════════════════ C-A19-01 兩層阿拉伯星空 ══════════════════════
def c01_now(ax):
    T(ax, 0, 0.86, tx("c01_title"), 32)
    box(ax, 0, 0.55, 1.6, 0.26, GREY, a=.6)
    T(ax, 0, 0.60, tx("now"), 21, GREY)
    T(ax, 0, 0.50, tx("now2"), 16, GREY, w="normal")


def c01_old(ax):
    T(ax, 0, 0.26, tx("old"), 21, AMBER)
    xs = (-0.62, 0.0, 0.62)
    for x, k1, k2, col in zip(xs, ("s1", "s2", "s3"), ("s1b", "s2b", "s3b"), (AMBER, WHITE, BLUE)):
        box(ax, x, -0.20, 0.54, 0.62, col)
        T(ax, x, 0.02, tx(k1), 19, col)
        ax.text(x, -0.25, tx(k2), fontproperties=C.FP, fontsize=14, color=WHITE, ha="center", va="center",
                linespacing=1.5, zorder=12)
    for a, b in ((xs[0], xs[1]), (xs[1], xs[2])):
        C.arrow(ax, (b - 0.29, -0.20), (a + 0.29, -0.20), c=WHITE, lw=2.0, alpha=.8, style="-|>")


# ══════════════════════ C-A19-02 抄錯一個字母 ══════════════════════
def c02_orig(ax):
    T(ax, 0, 0.82, tx("c02_title"), 32)
    T(ax, 0, 0.45, G.rtl("أدحي"), 64, GREEN, w="normal")
    T(ax, 0, 0.22, tx("orig"), 22, GREEN)


def c02_copy(ax):
    C.arrow(ax, (0, -0.02), (0, 0.12), c=WHITE, lw=2.4, alpha=.8, style="-|>")
    T(ax, 0, -0.22, G.rtl("ازحى"), 64, WHITE, w="normal")
    T(ax, 0, -0.45, tx("copy"), 22, WHITE)
    T(ax, -0.22, -0.62, G.rtl("د"), 40, GREEN, w="normal")
    T(ax, 0.0, -0.62, "→", 30, WHITE)
    T(ax, 0.22, -0.62, G.rtl("ز"), 40, RED, w="normal")
    T(ax, 0, -0.74, tx("dz"), 18, RED)
    T(ax, 0, -0.88, tx("iau"), 19, AMBER)


# ══════════════════════ C-A19-03 看得到 Suhail 的地方 ══════════════════════
L0, L1 = 12.0, 40.0


def _ly(lat):
    return -0.70 + 1.30 * (lat - L0) / (L1 - L0)


ARAB = [("Damascus", 33.51, 3.8), ("Riyadh", 24.71, 12.6), ("Mecca", 21.42, 15.9), ("Sanaa", 15.35, 22.0)]
TW = [("Taipei", 25.03, 12.3), ("Kenting", 21.90, 15.4)]


def c03_lat(ax):
    T(ax, 0, 0.86, tx("c03_title"), 30)
    T(ax, 0, 0.78, tx("c03_sub"), 15, GREY, w="normal")
    for lat in range(15, 41, 5):
        y = _ly(lat)
        ax.plot([-0.80, 0.86], [y, y], c=WHITE, lw=0.8, alpha=.15)
        T(ax, -0.86, y, f"{lat}°", 13, GREY, w="normal", ha="right")
    y = _ly(37.3)
    ax.plot([-0.80, 0.86], [y, y], c=RED, lw=2.4, ls=(0, (6, 4)))
    T(ax, 0.03, y + 0.05, tx("limit"), 18, RED)
    T(ax, -0.40, -0.80, tx("arab"), 18, AMBER)
    T(ax, 0.48, -0.80, tx("tw"), 18, BLUE)


def c03_city(ax):
    for col, rows, x0 in ((AMBER, ARAB, -0.40), (BLUE, TW, 0.48)):
        for nm, lat, alt in rows:
            y = _ly(lat)
            ax.scatter([x0], [y], s=140, c=col, zorder=6, lw=0)
            T(ax, x0 - 0.04, y, tx(nm), 16, WHITE, w="normal", ha="right")
            T(ax, x0 + 0.04, y, f"{alt:.1f}°", 18, col, ha="left")


# ══════════════════════ C-A19-04 擋路的 Suhail ══════════════════════
def c04_road(ax):
    T(ax, 0, 0.86, tx("c04_title"), 30)
    g = -0.40
    xs = [-0.9 + 1.8 * i / 60 for i in range(61)]
    ax.plot(xs, [g + 0.03 * math.sin(3 * x) for x in xs], c=SAND, lw=3.0, ls=(0, (8, 6)), alpha=.9)
    T(ax, -0.55, g - 0.10, tx("road"), 17, SAND, w="normal")
    ax.add_patch(Rectangle((0.02, g), 0.06, 0.30, fc=WHITE, ec="none", alpha=.85, zorder=4))
    ax.plot([0.08, 0.50], [g + 0.22, g + 0.22], c=RED, lw=5.0, zorder=4)
    C.human_figure(ax, -0.12, g + 0.12, s=0.50, c=WHITE, alpha=.9)
    T(ax, 0.30, g + 0.33, tx("toll"), 18, RED)


def c04_star(ax):
    C.arrow(ax, (-0.12, 0.32), (-0.12, -0.08), c=WHITE, lw=2.0, alpha=.7, style="-|>")
    ax.scatter([-0.12], [0.45], s=900, c=WHITE, marker="*", lw=0, zorder=8)
    T(ax, 0.22, 0.45, tx("star"), 20, AMBER, ha="left")
    T(ax, 0, -0.82, tx("c04_note"), 16, GREY, w="normal")


# ══════════════════════ C-A19-05 310 光年 ══════════════════════
def _dx(ly):
    return -0.82 + 1.64 * ly / 320.0


def c05_dist(ax):
    T(ax, 0, 0.86, tx("c05_title"), 30)
    y = 0.42
    ax.plot([_dx(0), _dx(320)], [y, y], c=WHITE, lw=1.6, alpha=.5)
    for ly in range(0, 301, 100):
        ax.plot([_dx(ly)] * 2, [y - 0.02, y + 0.02], c=WHITE, lw=1.2, alpha=.5)
        T(ax, _dx(ly), y - 0.06, f"{ly}", 13, GREY, w="normal")
    T(ax, _dx(320), y - 0.06, tx("ly"), 13, GREY, w="normal", ha="right")
    ax.scatter([_dx(0)], [y], s=200, c=AMBER, lw=0, zorder=6)
    T(ax, _dx(0), y + 0.07, tx("sun"), 15, AMBER)
    ax.scatter([_dx(8.6)], [y], s=160, c=BLUE, lw=0, zorder=6)
    T(ax, _dx(8.6) + 0.02, y + 0.17, tx("sir"), 17, BLUE, ha="left")
    ax.plot([_dx(8.6)] * 2, [y + 0.02, y + 0.13], c=BLUE, lw=1.2, alpha=.7)
    ax.scatter([_dx(309)], [y], s=260, c=WHITE, lw=0, zorder=6)
    T(ax, _dx(309), y + 0.17, tx("can"), 19, WHITE, ha="right")
    ax.plot([_dx(309)] * 2, [y + 0.02, y + 0.13], c=WHITE, lw=1.2, alpha=.7)
    T(ax, _dx(160), y - 0.16, tx("far"), 22, WHITE)
    T(ax, 0, 0.06, tx("bright"), 19, AMBER)
    T(ax, 0, -0.03, tx("bright2"), 16, WHITE, w="normal")


def c05_old(ax):
    box(ax, 0, -0.48, 1.62, 0.56, AMBER)
    T(ax, 0, -0.29, tx("old_cn"), 20, AMBER)
    T(ax, 0, -0.44, tx("quote"), 22 if LANG == "zh" else 15, WHITE)
    T(ax, 0, -0.58, tx("src"), 15, GREY, w="normal")
    if tx("xian"):
        T(ax, 0, -0.69, tx("xian"), 14, GREY, w="normal")


# ══════════════════════ C-A19-06 這週末抬頭看（9:16 圖卡） ══════════════════════
TPE = ("25.0330", "121.5654")


def altaz(hip, utc):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = TPE; o.temp, o.pressure = 15, 1010
    o.date = ephem.Date(utc)
    ra, dec = S[hip][:2]
    b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def c06_card(ax):
    def tt(x, y, s, size, col=WHITE, ha="center", w="normal"):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=col, ha=ha, va="center", weight=w)
    tt(0.5, 0.945, tx("c06_title"), 26, w="bold")
    tt(0.5, 0.905, tx("c06_date"), 13, GREY)
    X0, X1, Yb, Yt = 0.08, 0.94, 0.36, 0.84
    AZ0, AZ1, AL1 = 135.0, 225.0, 55.0

    def P(alt, az):
        return X0 + (X1 - X0) * (az - AZ0) / (AZ1 - AZ0), Yb + (Yt - Yb) * alt / AL1
    ax.plot([X0, X1], [Yb, Yb], c=WHITE, lw=1.6, alpha=.7)
    ax.add_patch(Rectangle((X0, Yb - 0.02), X1 - X0, 0.02, fc="#1B2240", ec="none"))
    for az, k in ((157.5, "SE"), (180, "S"), (202.5, "SW")):
        tt(P(0, az)[0], Yb - 0.035, tx(k), 13, GREY)
    for alt in (10, 20, 30, 40, 50):
        y = P(alt, AZ0)[1]
        ax.plot([X0, X1], [y, y], c=WHITE, lw=0.6, alpha=.12)
        tt(X0 - 0.01, y, f"{alt}°", 9, GREY, ha="right")
    # 老人星的路徑 19:00–24:00（每小時一點）與 21:43 位置
    pts = [P(*altaz(30438, f"2027/1/29 {h - 8}:00")) for h in range(19, 25)]
    for i, (x, y) in enumerate(pts):
        ax.scatter([x], [y], s=26, c=AMBER, alpha=.6, lw=0, zorder=4)
        tt(x, y - 0.018, f"{19 + i}:00", 8.5, GREY)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=AMBER, lw=1.0, alpha=.4)
    xc, yc = P(*altaz(30438, "2027/1/29 13:43"))
    ax.scatter([xc], [yc], s=200, c=WHITE, lw=0, zorder=6)
    tt(xc, yc + 0.03, tx("c06_can") + "  " + tx("c06_t"), 15, AMBER, w="bold")
    xs, ys = P(*altaz(32349, "2027/1/29 13:43"))
    ax.scatter([xs], [ys], s=240, c=WHITE, marker="*", lw=0, zorder=6)
    tt(xs + 0.03, ys, tx("c06_sir") + f" {altaz(32349, '2027/1/29 13:43')[0]:.0f}°", 13, WHITE, ha="left")
    notes = [(tx("n1"), AMBER), (tx("n2"), WHITE), (tx("n3"), WHITE), (tx("n4"), WHITE)]
    for i, (s_, col) in enumerate(notes):
        tt(0.5, 0.25 - 0.035 * i, s_, 13, col)
    tt(0.5, 0.075, tx("c06_src"), 10, GREY)
    tt(0.5, 0.040, "#萬國星空　#師大天文社", 13)
    print(f"  台北 1/29 21:43 老人星 {altaz(30438, '2027/1/29 13:43')[0]:.1f}°、天狼星 {altaz(32349, '2027/1/29 13:43')[0]:.1f}°")


# ══════════════════════ C-A19-07 沙漠動物園小辭典（9:16 圖卡） ══════════════════════
ROWS = [  # (轉寫, 中文, 哪裡)
    ("al-Asad", "獅子", "雙子—巨蟹—獅子—室女"),
    ("al-Qafza ×3", "羚羊的三跳", "大熊腳下：Alula／Tania／Talitha"),
    ("al-Ẓalīmān", "兩隻公鴕鳥", "北落師門＋土司空"),
    ("al-Riʾāl", "小鴕鳥們", "寶瓶—鯨魚交界的暗星"),
    ("al-Naʿāmāt", "鴕鳥媽媽", "鯨魚座"),
    ("Udḥiyy al-Naʿām", "鴕鳥窩、蛋、蛋殼", "波江座（Azha＝η Eri）"),
    ("al-Naʿām al-Wārid", "下河喝水的鴕鳥", "人馬座（銀河裡）"),
    ("al-Naʿām al-Ṣādir", "喝飽離開的鴕鳥", "人馬座（銀河外）"),
    ("Suhayl", "Suhail（男子名）", "老人星"),
    ("al-Shiʿrā al-ʿAbūr", "渡河的 Shiʿrā", "天狼星"),
    ("al-Ghumayṣāʾ", "淚眼模糊的 Shiʿrā", "南河三"),
    ("al-Nasr al-wāqiʿ／al-ṭāʾir", "降落的鷹／飛翔的鷹", "織女星／牛郎星"),
    ("al-Aghriba", "烏鴉們", "天鴿座"),
]


def c07_card(ax):
    def tt(x, y, s, size, col=WHITE, ha="center", w="normal"):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=col, ha=ha, va="center", weight=w)
    tt(0.5, 0.945, tx("c07_title"), 27, w="bold")
    tt(0.5, 0.905, tx("c07_sub"), 12, GREY)
    ax.plot([0.04, 0.96], [0.88, 0.88], c=WHITE, lw=1.0, alpha=.4)
    y = 0.865
    h = 0.058
    for i, (tr, zh, where) in enumerate(ROWS):
        col = (AMBER, GREEN, BLUE)[0 if i < 2 else (1 if i < 8 else 2)] if i < 11 else PURPLE
        tt(0.05, y - 0.018, tr, 12, col, ha="left", w="bold")
        tt(0.95, y - 0.018, zh, 12, col, ha="right", w="bold")
        tt(0.05, y - 0.040, where, 10.5, WHITE, ha="left")
        y -= h
        ax.plot([0.04, 0.96], [y, y], c=WHITE, lw=0.6, alpha=.18)
    tt(0.5, 0.080, tx("c07_src"), 9.5, GREY)
    tt(0.5, 0.040, "#萬國星空　#師大天文社", 13)


S = None


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    C.emit("", [("今日", c01_now), ("古詩", c01_old)], title="C-A19-01_兩層阿拉伯星空")
    C.emit("", [("原字", c02_orig), ("抄錯", c02_copy)], title="C-A19-02_抄錯一個字母")
    C.emit("", [("緯度", c03_lat), ("城市", c03_city)], title="C-A19-03_看得到Suhail的地方")
    C.emit("", [("商道", c04_road), ("星星", c04_star)], title="C-A19-04_擋路的Suhail")
    C.emit("", [("距離", c05_dist), ("南極老人", c05_old)], title="C-A19-05_310光年")
    f, ax = C.newcard(dark=True)
    c06_card(ax)
    C.save(f, "", "C-A19-06_這週末抬頭看_圖卡.png", transparent=False)
    if LANG == "zh":                    # 小辭典的表格是中文版專用（英文版另做）
        f, ax = C.newcard(dark=True)
        c07_card(ax)
        C.save(f, "", "C-A19-07_沙漠動物園小辭典_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
