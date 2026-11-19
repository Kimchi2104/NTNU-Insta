# -*- coding: utf-8 -*-
"""X-08 第一季完結｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-X08-01_世界地圖          → 逐字稿 10 鏡（陸地層→27點層→客人層）
  C-X08-02_勘誤卡            → 逐字稿 11 鏡（七夕層）、11b 鏡（三垣層）；兩張各自獨立
  C-X08-03_牛郎織女距離      → 逐字稿 11 鏡（三角形層→答案層）
  C-X08-04_第一季27個文化一覽 → 逐字稿 10 鏡（9:16 圖卡，可存圖）
  C-X08-05_七夕0808晚上九點   → 逐字稿 14 鏡（9:16 圖卡，可存圖）
輸出：05_素材/X-08_第一季完結/_概念圖/（--lang en → _概念圖/en/，這次只出 zh）

來源：陸地＝Natural Earth 1:110m land（public domain；07_資料來源/地圖/世界陸地_naturalearth_110m.json），
      只畫成點陣、不畫國界；文化的點＝大致區域（原住民族群不畫邊界）。
      距離＝Hipparcos 新歸算視差（van Leeuwen 2007）：織女 130.23 mas、牛郎 194.95 mas；角距由 03_星點座標表.csv 自算。
      七夕的天空＝PyEphem 4.2.1 自算（台北 25.033°N 121.565°E，2027/8/8 21:00 UTC+8，恆星 J2000）。
      27 個文化與集數＝逐字稿 v1「星名表」。
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import numpy as np

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-08_第一季完結/_概念圖")
C.set_base(OUT)
RED, GREY, LAND = "#FF6B6B", "#8A97B3", "#4A5A80"
LANG = "zh"

# ── 27 個文化（星名表）：key, 緯度, 經度, 集數 ──
CULT = [
    ("中國", 34.3, 108.9, "A-01、02、03、12、20；C-01～03；H 三支"), ("韓國", 37.6, 127.0, "A-04"),
    ("日本", 35.0, 136.0, "A-05"), ("印度", 22.0, 79.0, "A-28"), ("蒙古", 47.9, 106.9, "A-07"),
    ("西伯利亞", 61.0, 104.0, "A-08"), ("夏威夷", 19.9, -155.6, "A-09"), ("東加", -21.1, -175.2, "A-10"),
    ("阿努塔", -11.6, 169.85, "A-11"), ("阿拉伯", 24.0, 45.0, "A-13、19、32、34"), ("因紐特", 69.4, -81.8, "A-14"),
    ("北歐", 64.9, -18.0, "A-15"), ("納瓦荷", 36.1, -109.0, "A-16"), ("黑腳族", 48.6, -113.0, "A-17"),
    ("古埃及", 26.0, 32.6, "A-18"), ("薩米", 68.8, 23.0, "A-21"), ("白俄羅斯", 53.9, 27.6, "A-22"),
    ("羅馬尼亞", 45.9, 25.0, "A-23"), ("圖卡諾", 0.5, -69.5, "A-24"), ("圖皮—瓜拉尼", -2.5, -44.3, "A-25"),
    ("布吉斯", -4.6, 120.3, "A-26"), ("曼達爾", -3.0, 118.9, "A-27"), ("薩丁尼亞", 40.1, 9.0, "A-29"),
    ("呂埃勒", 48.85, 2.35, "A-30"), ("卡米拉羅伊／尤瓦萊", -30.0, 149.0, "A-31"), ("毛利", -39.0, 175.5, "A-33"),
    ("IAU", 41.9, 12.5, "A-35、36"),
]
# ── 跨文化客人（至少 19 個；只算旁白或圖卡上出現名字的） ──
GUEST = [
    ("大溪地", -17.6, -149.4), ("薩摩亞", -13.8, -172.0), ("布朗", -35.0, 142.5), ("那馬", -25.0, 17.0),
    ("ǀXam 桑人", -31.0, 21.0), ("滿洲", 43.8, 126.5), ("巴比倫", 32.5, 44.4), ("阿茲特克", 19.4, -99.1),
    ("馬雅", 20.5, -89.0), ("洛科諾", 5.5, -55.0), ("提庫納", -3.8, -70.0), ("馬其頓", 41.6, 21.7),
    ("祖魯", -28.5, 31.0), ("科薩", -32.5, 27.5), ("萬那杜", -16.0, 167.0), ("希臘", 37.9, 23.7),
    ("芬蘭", 62.0, 25.7), ("尤皮克", 63.5, -170.0), ("峇里", -8.4, 115.2),
]
assert len(CULT) == 27 and len(GUEST) == 19

# ── 圖卡：27 個文化一覽（星名表的一句話） ──
ROWS = [
    ("中國", "A-01 等", "青龍、紫禁城、玄武、白虎、朱雀；論天三家", "China", "Dragon, Forbidden City, Tiger…"),
    ("韓國", "A-04", "一萬韓元鈔票上的天象列次分野之圖", "Korea", "The star chart on the 10,000-won note"),
    ("日本", "A-05", "照抄格子、換上自己的名字", "Japan", "Same grid, new names"),
    ("印度", "A-28", "月亮的 27 位妻子", "India", "The Moon's 27 wives"),
    ("蒙古", "A-07", "天空拴在一根金樁上", "Mongolia", "The sky tethered to a golden stake"),
    ("西伯利亞", "A-08", "每晚重演的駝鹿追獵", "Siberia", "A moose hunt replayed every night"),
    ("夏威夷", "A-09", "四條回家的路", "Hawaiʻi", "Four starlines home"),
    ("東加", "A-10", "星星的名字就是航線", "Tonga", "Star names are sailing orders"),
    ("阿努塔", "A-11", "半平方公里小島的星空智慧", "Anuta", "Sky lore of a tiny island"),
    ("阿拉伯", "A-13 等", "昴宿與雨季、月亮的旅店、蘇菲之書", "Arabia", "Pleiades and rain, lunar mansions, al-Ṣūfī"),
    ("因紐特", "A-14", "極夜裡的星鐘", "Inuit", "A star clock in the polar night"),
    ("北歐", "A-15", "手抄本裡的狼嘴", "Norse", "The wolf's mouth in a manuscript"),
    ("納瓦荷", "A-16", "只在冬天說的星星故事", "Navajo", "Star stories told only in winter"),
    ("黑腳族", "A-17", "帳篷頂上的北斗與昴宿", "Blackfoot", "Dipper and Pleiades on the lodge"),
    ("古埃及", "A-18", "叫醒尼羅河的天狼星", "Egypt", "Sirius wakes the Nile"),
    ("薩米", "A-21", "一場還沒結束的狩獵", "Sámi", "A hunt that is not over yet"),
    ("白俄羅斯", "A-22", "以利亞的火焰馬車", "Belarus", "Elijah's fiery chariot"),
    ("羅馬尼亞", "A-23", "牧羊人的星空農場", "Romania", "A shepherd's farm in the sky"),
    ("圖卡諾", "A-24", "一整年的漲水", "Tukano", "A year of rising rivers"),
    ("圖皮—瓜拉尼", "A-25", "1614 年傳教士抄下的星空", "Tupi-Guarani", "A sky written down in 1614"),
    ("布吉斯", "A-26", "帆船民族的星羅盤", "Bugis", "A sailors' star compass"),
    ("曼達爾", "A-27", "同一個北斗：船與漁網", "Mandar", "One Dipper: boat or fishing net"),
    ("薩丁尼亞", "A-29", "天上的小屋、鐮刀與葡萄串", "Sardinia", "A hut, a sickle, grapes"),
    ("呂埃勒（法國，1786）", "A-30", "一張只有線的星圖", "Ruelle (France, 1786)", "A star map of lines only"),
    ("卡米拉羅伊／尤瓦萊", "A-31", "不只連星星，也連銀河裡的黑", "Kamilaroi/Euahlayi", "Joining the dark, not only stars"),
    ("毛利", "A-33", "Matariki 黎明重現就是新年", "Māori", "Matariki at dawn: New Year"),
    ("現代國際（IAU）", "A-35、36", "88 個星座、課本沒教的星群", "Modern (IAU)", "88 constellations and asterisms"),
]

TXT = {
    "zh": {
        "c01_title": "第一季：27 個文化＋十幾位客人", "c01_sub": "點＝大致區域（原住民族群不畫邊界）；Natural Earth 陸地",
        "c01_leg1": "● 有自己一整集的文化和星圖：27", "c01_leg2": "○ 跨文化專題請來的客人：至少 19",
        "c02_head": "勘誤", "c02a_no": "①", "c02a_ep": "七夕那集（H-七夕）說：", "c02a_old": "牛郎織女相距 16 光年",
        "c02a_new": "重算：14.6 光年", "c02a_src": "Hipparcos 衛星新歸算的距離（van Leeuwen 2007）＋餘弦定理",
        "c02b_no": "②", "c02b_ep": "三垣那集（A-02）說：", "c02b_old": "紫微垣裡連廁所都有星官",
        "c02b_new": "紫微垣沒有廁所；「廁」在參宿南邊", "c02b_src": "紫微垣有天床、天廚；廁＝天兔座四星，天溷在奎宿",
        "c03_title": "牛郎和織女，到底隔多遠？", "c03_sub": "俯視示意（長度照比例；地球在下）",
        "earth": "地球", "vega": "織女", "altair": "牛郎", "ly": "{:.2f} 光年", "ang": "夾角 {:.1f}°",
        "ans": "兩星相距 {:.1f} 光年", "ans2": "不是 16 光年",
        "c04_title": "第一季　27 個文化一覽", "c04_sub": "萬國星空 2026–2027・47 集正片＋3 支節日特輯",
        "c04_guest": "跨文化專題的客人（至少 19）：", "c04_guest2": "大溪地、薩摩亞、布朗、那馬、ǀXam 桑人、滿洲、巴比倫、",
        "c04_guest3": "阿茲特克、馬雅、洛科諾、提庫納、馬其頓、祖魯、科薩、萬那杜、希臘、芬蘭、尤皮克、峇里",
        "c05_title": "七夕 8/8 晚上九點的天空", "c05_sub": "2027/8/8（日）農曆七月初七　台北 21:00",
        "N": "北", "E": "東", "S": "南", "W": "西", "zen": "天頂",
        "c05_vega": "織女 {:.0f}°", "c05_altair": "牛郎 {:.0f}°", "c05_deneb": "天津四 {:.0f}°", "c05_moon": "初七的半月",
        "c05_note1": "織女幾乎就在頭頂；牛郎在東南", "c05_note2": "初七的半月在西南西 {:.0f}°，21:30 後低於 10°、22:25 落下",
        "c05_note3": "圓心＝天頂、外圈＝地平線；朝上躺著看，東在左",
        "tag": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Season 1: 27 cultures + a dozen-plus guests", "c01_sub": "Dots = approximate regions; land from Natural Earth",
        "c01_leg1": "● A full episode of their own: 27", "c01_leg2": "○ Guests in the cross-culture specials: 19+",
        "c02_head": "Correction", "c02a_no": "1", "c02a_ep": "In our Qixi episode we said:", "c02a_old": "Altair and Vega are 16 light-years apart",
        "c02a_new": "Recomputed: 14.6 light-years", "c02a_src": "Hipparcos new reduction (van Leeuwen 2007) + law of cosines",
        "c02b_no": "2", "c02b_ep": "In our Three Enclosures episode we said:", "c02b_old": "the Purple Palace even has a toilet",
        "c02b_new": "It doesn't — the Toilet lies south of Orion", "c02b_src": "Bed and Kitchen are in the Palace; the Toilet = four stars of Lepus",
        "c03_title": "How far apart are Altair and Vega?", "c03_sub": "Top view, to scale; Earth at the bottom",
        "earth": "Earth", "vega": "Vega", "altair": "Altair", "ly": "{:.2f} ly", "ang": "{:.1f}° apart",
        "ans": "{:.1f} light-years apart", "ans2": "not 16",
        "c04_title": "Season 1: 27 cultures", "c04_sub": "World Sky Cultures 2026–2027 · 47 episodes + 3 specials",
        "c04_guest": "Guests in the specials (19+):", "c04_guest2": "Tahiti, Samoa, Boorong, Nama, ǀXam, Manchu, Babylon,",
        "c04_guest3": "Aztec, Maya, Lokono, Tikuna, Macedonia, Zulu, Xhosa, Vanuatu, Greece, Finland, Yupik, Bali",
        "c05_title": "The Qixi sky, Aug 8, 9 pm", "c05_sub": "Sun Aug 8, 2027 (7th day, 7th lunar month) · Taipei 21:00",
        "N": "N", "E": "E", "S": "S", "W": "W", "zen": "Zenith",
        "c05_vega": "Vega {:.0f}°", "c05_altair": "Altair {:.0f}°", "c05_deneb": "Deneb {:.0f}°", "c05_moon": "Half Moon",
        "c05_note1": "Vega almost overhead; Altair to the southeast", "c05_note2": "Half Moon WSW at {:.0f}°, below 10° after 21:30, sets 22:25",
        "c05_note3": "Centre = zenith, rim = horizon; lie on your back, east on the left",
        "tag": "#WorldSkyCultures",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ C-X08-01 世界地圖 ══════════════════════
LON0 = 150.0                       # 太平洋置中：地圖左緣 −30°（大西洋中間）、右緣 330°
MW_, MH_ = 1.90, 0.95              # 地圖寬、高（軸座標）
MY0 = -0.06                        # 地圖中心 y


def mxy(lat, lon):
    l = (lon - (LON0 - 180.0)) % 360.0                 # 0..360，從 −30° 起算
    return -MW_ / 2 + l / 360.0 * MW_, MY0 + lat / 180.0 * MH_


def land_dots():
    from matplotlib.path import Path
    d = json.load(open(os.path.join(BASE, "07_資料來源/地圖/世界陸地_naturalearth_110m.json"), encoding="utf-8"))
    paths = [Path(np.array(p)) for p in d["polygons"] if len(p) > 3]
    pts = []
    step = 2.4
    for lat in np.arange(-56.0, 80.0, step):
        for lon in np.arange(-180.0 + step / 2, 180.0, step):
            if any(P.contains_point((lon, lat)) for P in paths):
                pts.append((lat, lon))
    return pts


LAND_PTS = None


def c01_land(ax):
    T(ax, 0.0, 0.60, tx("c01_title"), 30, WHITE)
    T(ax, 0.0, 0.53, tx("c01_sub"), 15, GREY, w="normal")
    xs, ys = zip(*[mxy(a, b) for a, b in LAND_PTS])
    ax.scatter(xs, ys, s=16, c=LAND, lw=0, zorder=3)
    for lat in (-60, -30, 0, 30, 60):
        a = mxy(lat, LON0 - 180.0 + 0.01); b = mxy(lat, LON0 + 179.99)
        ax.plot([a[0], b[0]], [a[1], a[1]], c=WHITE, lw=0.6, alpha=.10, zorder=2)


def c01_main(ax):
    xs, ys = zip(*[mxy(a, b) for _, a, b, _ in CULT])
    ax.scatter(xs, ys, s=150, c=AMBER, lw=1.2, edgecolors="#0B0F1E", zorder=8)
    T(ax, -0.93, -0.62, tx("c01_leg1"), 19, AMBER, ha="left")


def c01_guest(ax):
    xs, ys = zip(*[mxy(a, b) for _, a, b in GUEST])
    ax.scatter(xs, ys, s=120, facecolors="none", edgecolors=GREEN, lw=2.4, zorder=7)
    T(ax, -0.93, -0.70, tx("c01_leg2"), 19, GREEN, ha="left")


# ══════════════════════ C-X08-02 勘誤卡 ══════════════════════
def _errata(ax, no, ep, old, new, src):
    T(ax, 0.0, 0.40, f"{tx('c02_head')} {tx(no)}", 34, AMBER)
    T(ax, 0.0, 0.24, tx(ep), 21, GREY, w="normal")
    T(ax, 0.0, 0.10, tx(old), 30, WHITE, alpha=.75)
    w = 0.92 if LANG == "zh" else 0.95
    ax.plot([-w / 2 - 0.03, w / 2 + 0.03], [0.10, 0.10], c=RED, lw=5, alpha=.95, zorder=14)
    C.arrow(ax, (0.0, -0.10), (0.0, 0.01), c=WHITE, lw=2.4, alpha=.8, style="-|>")
    T(ax, 0.0, -0.22, tx(new), 32, AMBER)
    T(ax, 0.0, -0.38, tx(src), 15, GREY, w="normal")


def c02_qixi(ax):
    _errata(ax, "c02a_no", "c02a_ep", "c02a_old", "c02a_new", "c02a_src")


def c02_sanyuan(ax):
    _errata(ax, "c02b_no", "c02b_ep", "c02b_old", "c02b_new", "c02b_src")


# ══════════════════════ C-X08-03 牛郎織女距離 ══════════════════════
PLX_V, PLX_A = 130.23, 194.95                    # mas（van Leeuwen 2007）
LY = 3.26156
D_V, D_A = 1000.0 / PLX_V * LY, 1000.0 / PLX_A * LY
SEP = None
D_VA = None


def _tri():
    s = 0.034                                     # 每光年的軸長
    E = (0.0, -0.52)
    hv, ha = math.radians(90 + SEP / 2), math.radians(90 - SEP / 2)
    V = (E[0] + D_V * s * math.cos(hv), E[1] + D_V * s * math.sin(hv))      # 織女在左（東在左）
    A = (E[0] + D_A * s * math.cos(ha), E[1] + D_A * s * math.sin(ha))
    return E, V, A


def c03_tri(ax):
    T(ax, 0.0, 0.62, tx("c03_title"), 30, WHITE)
    T(ax, 0.0, 0.54, tx("c03_sub"), 15, GREY, w="normal")
    E, V, A = _tri()
    for P, col in ((V, BLUE), (A, BLUE)):
        ax.plot([E[0], P[0]], [E[1], P[1]], c=col, lw=2.6, alpha=.9, zorder=5)
    ax.add_patch(C.Arc(E, 0.36, 0.36, theta1=90 - SEP / 2, theta2=90 + SEP / 2, color=WHITE, lw=1.6, zorder=6))
    T(ax, 0.0, E[1] + 0.30, tx("ang").format(SEP), 15, WHITE, w="normal")
    ax.scatter([E[0]], [E[1]], s=180, c=BLUE, zorder=8)
    ax.scatter([V[0], A[0]], [V[1], A[1]], s=[420, 300], c=WHITE, zorder=8)
    T(ax, E[0], E[1] - 0.07, tx("earth"), 20, BLUE)
    T(ax, V[0] - 0.04, V[1] + 0.07, tx("vega"), 22, WHITE, ha="right")
    T(ax, A[0] + 0.04, A[1] + 0.07, tx("altair"), 22, WHITE, ha="left")
    mv = ((E[0] + V[0]) / 2 - 0.06, (E[1] + V[1]) / 2)
    ma = ((E[0] + A[0]) / 2 + 0.06, (E[1] + A[1]) / 2)
    T(ax, mv[0], mv[1], tx("ly").format(D_V), 18, BLUE, ha="right")
    T(ax, ma[0], ma[1], tx("ly").format(D_A), 18, BLUE, ha="left")


def c03_ans(ax):
    E, V, A = _tri()
    ax.plot([V[0], A[0]], [V[1], A[1]], c=AMBER, lw=4.2, zorder=7)
    mx, my = (V[0] + A[0]) / 2, (V[1] + A[1]) / 2
    dx, dy = A[0] - V[0], A[1] - V[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n                      # 線段的法向（往右上，離開三角形）
    T(ax, mx + nx * 0.17 + 0.10, my + ny * 0.17 + 0.03, tx("ans").format(D_VA), 24, AMBER)
    T(ax, mx + nx * 0.17 + 0.10, my + ny * 0.17 - 0.045, tx("ans2"), 17, RED)


# ══════════════════════ C-X08-04 27 個文化一覽（9:16 圖卡） ══════════════════════
def c04_card(ax):
    zh = LANG == "zh"
    ax.text(0.5, 0.955, tx("c04_title"), fontproperties=C.FP, fontsize=21, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.928, tx("c04_sub"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    y0, h = 0.900, 0.0272
    for i, (nz, ep, oz, ne, oe) in enumerate(ROWS):
        y = y0 - i * h
        if i % 2 == 0:
            ax.add_patch(C.Rectangle((0.03, y - h / 2), 0.94, h, fc="#151C36", ec="none", zorder=1))
        ax.text(0.045, y, f"{i + 1}", fontproperties=C.FP, fontsize=10, color=GREY, ha="left", va="center", zorder=3)
        ax.text(0.095, y, nz if zh else ne, fontproperties=C.FP, fontsize=11.5, color=AMBER, ha="left", va="center",
                weight="bold", zorder=3)
        ax.text(0.40, y, oz if zh else oe, fontproperties=C.FP, fontsize=10.5, color=WHITE, ha="left", va="center", zorder=3)
        ax.text(0.965, y, ep, fontproperties=C.FP, fontsize=9, color=GREY, ha="right", va="center", zorder=3)
    y = y0 - len(ROWS) * h - 0.012
    ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.8, alpha=.35)
    ax.text(0.045, y - 0.022, tx("c04_guest"), fontproperties=C.FP, fontsize=11.5, color=GREEN, ha="left", va="center", weight="bold")
    ax.text(0.045, y - 0.047, tx("c04_guest2"), fontproperties=C.FP, fontsize=10, color=WHITE, ha="left", va="center")
    ax.text(0.045, y - 0.069, tx("c04_guest3"), fontproperties=C.FP, fontsize=10, color=WHITE, ha="left", va="center")
    ax.text(0.5, 0.030, tx("tag"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")


# ══════════════════════ C-X08-05 七夕 8/8 21:00 的天空（9:16 圖卡） ══════════════════════
def sky_0808(S):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "25.0330", "121.5654"; o.elevation = 0; o.pressure, o.temp = 1010, 15
    o.date = ephem.Date(ephem.Date("2027/8/8 21:00") - 8 * ephem.hour)
    out = []
    for h, (ra, dec, v) in S.items():
        if v > 3.6:
            continue
        b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
        b.compute(o)
        if b.alt > 0:
            out.append((h, math.degrees(b.alt), math.degrees(b.az), v))
    m = ephem.Moon(); m.compute(o)
    return out, (math.degrees(m.alt), math.degrees(m.az), m.phase)


def c05_card(ax, S):
    stars, moon = sky_0808(S)
    cx, cy, R = 0.5, 0.50, 0.44
    ax.text(0.5, 0.955, tx("c05_title"), fontproperties=C.FP, fontsize=21, color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.925, tx("c05_sub"), fontproperties=C.FP, fontsize=11, color=GREY, ha="center", va="center")
    asp = C.CARD_W / C.CARD_H

    def p(alt, az):                               # 天頂等距；北上、東左（朝上躺著看）
        r = R * (90.0 - alt) / 90.0
        a = math.radians(az)
        return cx - r * math.sin(a), cy + r * math.cos(a) * asp

    ax.add_patch(C.Ellipse((cx, cy), 2 * R, 2 * R * asp, fc="#10172E", ec=GREY, lw=1.4, zorder=1))
    for alt in (30, 60):
        rr = R * (90 - alt) / 90
        ax.add_patch(C.Ellipse((cx, cy), 2 * rr, 2 * rr * asp, fc="none", ec=WHITE, lw=0.6, alpha=.15, zorder=2))
    for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = p(-6, az)
        ax.text(x, y, tx(k), fontproperties=C.FP, fontsize=15, color=AMBER, ha="center", va="center", weight="bold")
    ax.scatter([cx], [cy], marker="+", s=120, c=WHITE, alpha=.6, zorder=3)
    ax.text(cx + 0.015, cy - 0.012, tx("zen"), fontproperties=C.FP, fontsize=9, color=GREY, ha="left", va="center")
    pos = {}
    for h, alt, az, v in stars:
        x, y = p(alt, az)
        pos[h] = (x, y, alt)
        ax.scatter([x], [y], s=max(2.0, (4.2 - v) ** 2.2 * 6), c=WHITE, lw=0, zorder=4)
    V_, A_, D_ = 91262, 97649, 102098
    tri = [pos[h][:2] for h in (V_, D_, A_, V_)]
    ax.plot([q[0] for q in tri], [q[1] for q in tri], c=BLUE, lw=1.6, alpha=.9, zorder=3)
    for h, key, dx, dy, ha in ((V_, "c05_vega", 0.025, 0.006, "left"), (A_, "c05_altair", -0.025, -0.012, "right"),
                               (D_, "c05_deneb", -0.022, 0.016, "right")):
        x, y, alt = pos[h]
        ax.text(x + dx, y + dy, tx(key).format(alt), fontproperties=C.FP, fontsize=12.5, color=WHITE, ha=ha,
                va="center", weight="bold", zorder=6)
    mx, my = p(moon[0], moon[1])
    ax.scatter([mx], [my], s=260, c="#F4F1E6", zorder=6)
    ax.text(mx, my - 0.03, tx("c05_moon"), fontproperties=C.FP, fontsize=11, color=WHITE, ha="center", va="center", zorder=6)
    ax.text(0.5, 0.205, tx("c05_note1"), fontproperties=C.FP, fontsize=13.5, color=AMBER, ha="center", va="center", weight="bold")
    ax.text(0.5, 0.170, tx("c05_note2").format(moon[0]), fontproperties=C.FP, fontsize=10.5, color=WHITE, ha="center", va="center")
    ax.text(0.5, 0.140, tx("c05_note3"), fontproperties=C.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, tx("tag"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")
    return {h: pos[h][2] for h in (V_, A_, D_)}, moon


def main():
    global LANG, LAND_PTS, SEP, D_VA
    S = dict(G.load_stars(BASE))
    v, a = S[91262], S[97649]
    c = (math.sin(math.radians(v[1])) * math.sin(math.radians(a[1])) +
         math.cos(math.radians(v[1])) * math.cos(math.radians(a[1])) * math.cos(math.radians(v[0] - a[0])))
    SEP = math.degrees(math.acos(c))
    D_VA = math.sqrt(D_V ** 2 + D_A ** 2 - 2 * D_V * D_A * math.cos(math.radians(SEP)))
    print(f"  織女 {D_V:.2f} 光年、牛郎 {D_A:.2f} 光年、角距 {SEP:.2f}° → 相距 {D_VA:.2f} 光年")
    LAND_PTS = land_dots()
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    C.emit("", [("陸地", c01_land), ("27點", c01_main), ("客人", c01_guest)], title="C-X08-01_世界地圖")
    C.emit("", [("七夕", c02_qixi)], title="C-X08-02_勘誤卡", preview_name="預覽七夕")
    C.emit("", [("三垣", c02_sanyuan)], title="C-X08-02_勘誤卡", preview_name="預覽三垣")
    C.emit("", [("三角形", c03_tri), ("答案", c03_ans)], title="C-X08-03_牛郎織女距離")
    f, ax = C.newcard(dark=True)
    c04_card(ax)
    C.save(f, "", "C-X08-04_第一季27個文化一覽_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    alts, moon = c05_card(ax, S)
    C.save(f, "", "C-X08-05_七夕0808晚上九點_圖卡.png", transparent=False)
    print(f"  8/8 21:00：織女 {alts[91262]:.1f}°、牛郎 {alts[97649]:.1f}°、天津四 {alts[102098]:.1f}°；"
          f"月亮 {moon[0]:.1f}°／{moon[1]:.0f}°（{moon[2]:.0f}%）")


if __name__ == "__main__":
    main()
