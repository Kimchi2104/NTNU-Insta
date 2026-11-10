# -*- coding: utf-8 -*-
"""A-18 古埃及｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A18-01_尼羅河的一年     → 02 鏡（漲水層→淹沒層→黑土層）
  C-A18-02_消失與晨出       → 03 鏡（西沉層→消失層→晨出層→漲水層；漲水層配 04 鏡前半）
  C-A18-03_曆法的漂移       → 05 鏡（三季層→五天層→漂移層）
  C-A18-04_晚了一個多月     → 07 鏡（古代層→今天層）
  C-A18-05_河已經不等了     → 08 鏡（高壩層）
  C-A18-06_星星時刻表       → 10 鏡（格子層→十二小時層）
  C-A18-07_北面的入口       → 12 鏡（剖面層）
  C-A18-08_拉繩定位         → 14 鏡（木樁層→牛腿層）
  C-A18-09_兩千五百年       → 17 鏡（年表層）
  C-A18-10_今晚十點半       → 18 鏡（9:16 圖卡，可存圖）
  ── v2（2026-11-10 加回刪減；編號接在後面，舊圖的媒體 ID 不變）──
  C-A18-11_一千四百六十年   → 06 鏡（一圈層）
  C-A18-12_對正北           → 13 鏡（方框層；標「推測」）
  C-A18-13_以為有好幾千年   → 16 鏡（年表層：1799 → 1821 → 1822）
  15 鏡的丹德拉圓形黃道圖不在這裡：美宣另尋授權圖（羅浮宮原件照片或 1802 年版畫）。
輸出：05_素材/A-18_古埃及/_概念圖/（--lang en → _概念圖/en/）

來源（數字一律與逐字稿 v1「星空對時」一致，今晚圖卡的高度方位由 PyEphem 現算）：
  天狼星晨出：PyEphem 4.2.1 自算（太陽在地平線下 9.5–10.5° 時天狼星高 1°；Censorinus 139 年校準）；
  曆法：12 個月 × 30 天＋5 天，三季 Akhet／Peret／Shemu；對角星鐘：Neugebauer & Parker《Egyptian
  Astronomical Texts》的格式（自繪示意，不臨摹文物）；拉繩：Edfu／丹德拉神廟奠基銘文（pḏ šs）；
  丹德拉年代：Cauville & Aubourg 1995（BIFAO 95）；大金字塔剖面：示意（下降通道約 26.5°）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Polygon, Circle, Rectangle, Wedge, FancyBboxPatch
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-18_古埃及/_概念圖")
C.set_base(OUT)
RED, GREY, SOIL, SAND = "#FF6B6B", "#7C8BA8", "#4A3B2C", "#C9A66B"
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "尼羅河的一年", "c01_sub": "河谷剖面示意",
        "desert": "沙漠：幾乎不下雨", "river": "尼羅河", "rise": "夏天：河水上漲",
        "flood": "淹過兩岸的田", "soil": "退去後留下黑色的沃土",
        "kemet": "Kemet＝黑土地", "kemet2": "埃及人這樣叫自己的國家",
        "c02_title": "Sopdet 的消失與回來", "c02_sub": "天狼星；在埃及看",
        "west": "西方", "east": "東方", "dusk": "春天・黃昏", "dusk2": "沉進夕陽的光裡",
        "gone": "大約七十天看不見", "dawn": "夏天・清晨（日出之前）", "dawn2": "第一次在地平線上閃一下",
        "peret": "peret Sopdet「Sopdet 出來了」",
        "nile_rise": "差不多同時：河水開始漲", "newyear": "一年從這天開始（wepet renpet 年的開啟）",
        "c03_title": "一年 365 天", "c03_sub": "12 個月 × 30 天＋5 天；沒有閏年",
        "akhet": "漲水季", "peret_s": "生長季", "shemu": "收成季", "m4": "4 個月",
        "plus5": "＋5 天", "year1": "新年",
        "drift": "天狼星晨出", "drift2": "每 4 年晚 1 天",
        "drift3": "差滿一整圈：約 1,460 年",
        "c04_title": "天狼星重新出現的日子", "c04_sub": "公曆（古代外推）；PyEphem 自算",
        "solstice": "夏至 6/24", "old": "前 2500 年・孟斐斯", "old2": "6/28–29",
        "old3": "正好趕上漲水", "now": "2027 年・開羅", "now2": "8/5–6",
        "late": "晚了約 38 天", "jun": "6 月", "jul": "7 月", "aug": "8 月",
        "c04_note": "條件：太陽在地平線下約 10°、天狼星高 1°",
        "c05_title": "1970：亞斯文高壩", "before": "以前：每年夏天漲水", "after": "1970 年以後：水位幾乎不動",
        "dam": "高壩", "lake": "納瑟湖（水庫）", "down": "下游的尼羅河", "flood_held": "大水被攔在這裡",
        "yr": "一年",
        "c06_title": "星星時刻表（示意）", "c06_sub": "棺蓋上的「對角星鐘」：每 10 天換一欄",
        "col": "第 {} 旬", "hour": "第 {} 小時",
        "c06_12": "一夜數 12 組升起的星", "c06_12b": "＝夜晚的 12 個小時",
        "c06_diag": "同一組星每 10 天往上移一格",
        "c06_note": "自繪示意，依 Neugebauer & Parker 整理的格式；不是文物照片",
        "c07_title": "大金字塔的入口：開在北面", "c07_sub": "南北向剖面示意",
        "north": "北", "south": "南", "entrance": "入口", "passage": "下降通道",
        "sky": "北天：不知毀滅的星", "ground": "地面",
        "c08_title": "拉繩定位（奠基儀式）", "c08_sub": "神廟俯視示意",
        "king": "國王", "goddess": "女神 Seshat", "rope": "繩",
        "corners": "立下神廟的四個角", "leg": "眼睛看著 Meskhetyu（牛腿）",
        "c08_note": "依 Edfu、丹德拉神廟的拉繩銘文；自繪，不臨摹浮雕",
        "c09_title": "丹德拉星圖有多老？", "khufu": "古夫金字塔", "khufu2": "約前 2560 年",
        "dend": "丹德拉星圖", "dend2": "約前 50 年", "cleo": "埃及豔后在位",
        "cleo2": "前 51–前 30 年", "gap": "相隔約 2,500 年", "now9": "今天", "ad": "西元元年",
        "c09_note": "丹德拉年代：Cauville & Aubourg 1995（依圖上的行星位置與兩次食推算）",
        "c10_title": "今晚十點半，往正南", "c10_date": "2027/1/22（五）台北",
        "S": "南", "SE": "東南", "SW": "西南", "NE": "東北", "N": "北", "E": "東",
        "sirius": "天狼星 48°", "betel": "參宿四", "rigel": "參宿七", "orion": "獵戶（Sah）",
        "canopus": "老人星 12°", "dub": "天樞 33°", "alk": "搖光 9°", "leg10": "牛的前腿（北斗）",
        "moon": "滿月 66°（東方）", "jup": "木星",
        "c10_n1": "滿月，天狼星和獵戶仍然很清楚",
        "c10_n2": "老人星只有 12°，要找南方沒有遮擋的地方",
        "c10_n3": "回頭往東北：牛腿已經整條爬出地平線",
        "c10_src": "PyEphem 自算（含大氣折射）；天狼星 22:33 中天",
        "south_view": "面向正南", "ne_view": "面向東北",
        "c11_title": "差滿一整圈", "c11_sub": "每 4 年差 1 天 × 365 ＝ 約 1,460 年",
        "c11_139": "西元 139 年", "c11_after": "繞了 1,460 年", "c11_139b": "新年又落在天狼星晨出（7/20 前後）",
        "c11_src": "羅馬作家 Censorinus《論生日》（西元 238 年）記下",
        "c12_title": "大金字塔：對正東西南北", "c12_sub": "俯視示意（上＝北）",
        "c12_err": "誤差只有約 1/20 度（3–4 角分）", "c12_pole": "北天極",
        "c12_q": "怎麼找到正北？", "c12_guess": "推測：看繞著北極轉的星",
        "c12_note": "定北的方法有好幾種推測，沒有定論",
        "c13_title": "以為有好幾千年？", "c13_1799": "1799", "c13_1799b": "拿破崙遠征的學者看到它",
        "c13_1799c": "以為比聖經的創世還早", "c13_1821": "1821", "c13_1821b": "被炸下來，運到巴黎",
        "c13_1822": "1822", "c13_1822b": "Champollion 讀出王名框裡", "c13_1822c": "羅馬時代的頭銜 autokrator",
    },
    "en": {
        "c01_title": "A year of the Nile", "c01_sub": "Valley cross-section (schematic)",
        "desert": "Desert: almost no rain", "river": "Nile", "rise": "Summer: the river rises",
        "flood": "Fields on both banks flooded", "soil": "Receding water leaves black silt",
        "kemet": "Kemet = the Black Land", "kemet2": "what Egyptians called their country",
        "c02_title": "Sopdet vanishes and returns", "c02_sub": "Sirius, seen from Egypt",
        "west": "West", "east": "East", "dusk": "Spring · dusk", "dusk2": "sinks into the sunset glow",
        "gone": "About 70 days unseen", "dawn": "Summer · before sunrise", "dawn2": "first glint above the horizon",
        "peret": "peret Sopdet, “Sopdet goes forth”",
        "nile_rise": "Around the same time: the river begins to rise",
        "newyear": "The year begins (wepet renpet, “opening of the year”)",
        "c03_title": "A 365-day year", "c03_sub": "12 months × 30 days + 5; no leap year",
        "akhet": "Inundation", "peret_s": "Growing", "shemu": "Harvest", "m4": "4 months",
        "plus5": "+5 days", "year1": "New Year",
        "drift": "Rising of Sirius", "drift2": "1 day later every 4 years",
        "drift3": "A full circle: about 1,460 years",
        "c04_title": "When Sirius reappears", "c04_sub": "Gregorian (proleptic); computed with PyEphem",
        "solstice": "Solstice 6/24", "old": "2500 BCE · Memphis", "old2": "6/28–29",
        "old3": "just as the flood arrived", "now": "2027 · Cairo", "now2": "8/5–6",
        "late": "about 38 days later", "jun": "Jun", "jul": "Jul", "aug": "Aug",
        "c04_note": "Criterion: Sun about 10° below the horizon, Sirius 1° high",
        "c05_title": "1970: the Aswan High Dam", "before": "Before: a flood every summer",
        "after": "After 1970: the level barely moves",
        "dam": "Dam", "lake": "Lake Nasser (reservoir)", "down": "Nile downstream",
        "flood_held": "the flood is held back here", "yr": "one year",
        "c06_title": "A star timetable (schematic)", "c06_sub": "“Diagonal star clock” on coffin lids: a new column every 10 days",
        "col": "Week {}", "hour": "Hour {}",
        "c06_12": "12 rising star groups per night", "c06_12b": "= the 12 hours of the night",
        "c06_diag": "Each group climbs one row every 10 days",
        "c06_note": "Our schematic, after the format in Neugebauer & Parker; not an artefact photo",
        "c07_title": "The Great Pyramid opens to the north", "c07_sub": "North–south cross-section (schematic)",
        "north": "N", "south": "S", "entrance": "Entrance", "passage": "Descending passage",
        "sky": "Northern sky: the Imperishable Stars", "ground": "Ground",
        "c08_title": "Stretching the cord (foundation rite)", "c08_sub": "Temple plan (schematic)",
        "king": "King", "goddess": "Goddess Seshat", "rope": "cord",
        "corners": "the temple’s four corners", "leg": "eyes on Meskhetyu (the Foreleg)",
        "c08_note": "After the cord-stretching texts at Edfu and Dendera; our drawing",
        "c09_title": "How old is the Dendera zodiac?", "khufu": "Pyramid of Khufu", "khufu2": "c. 2560 BCE",
        "dend": "Dendera zodiac", "dend2": "c. 50 BCE", "cleo": "Cleopatra VII reigns",
        "cleo2": "51–30 BCE", "gap": "about 2,500 years apart", "now9": "Today", "ad": "1 CE",
        "c09_note": "Dendera date: Cauville & Aubourg 1995 (from planets and two eclipses on the ceiling)",
        "c10_title": "Tonight 10:30, face south", "c10_date": "Fri 22 Jan 2027, Taipei",
        "S": "S", "SE": "SE", "SW": "SW", "NE": "NE", "N": "N", "E": "E",
        "sirius": "Sirius 48°", "betel": "Betelgeuse", "rigel": "Rigel", "orion": "Orion (Sah)",
        "canopus": "Canopus 12°", "dub": "Dubhe 33°", "alk": "Alkaid 9°", "leg10": "the Foreleg (Big Dipper)",
        "moon": "Full Moon 66° (east)", "jup": "Jupiter",
        "c10_n1": "Full Moon, but Sirius and Orion stay bright",
        "c10_n2": "Canopus is only 12° up: find a clear southern horizon",
        "c10_n3": "Turn northeast: the whole Foreleg has risen",
        "c10_src": "PyEphem (with refraction); Sirius transits at 22:33",
        "south_view": "Facing south", "ne_view": "Facing northeast",
        "c11_title": "A full circle", "c11_sub": "1 day every 4 years × 365 = about 1,460 years",
        "c11_139": "139 CE", "c11_after": "after 1,460 years", "c11_139b": "New Year again at the rising of Sirius (about 20 July)",
        "c11_src": "recorded by the Roman writer Censorinus (De Die Natali, 238 CE)",
        "c12_title": "The Great Pyramid: squared to the compass", "c12_sub": "Plan view (north up)",
        "c12_err": "off by only about 1/20° (3–4 arcminutes)", "c12_pole": "North celestial pole",
        "c12_q": "How did they find north?", "c12_guess": "One guess: the stars circling the pole",
        "c12_note": "Several methods have been proposed; none is settled",
        "c13_title": "Thousands of years old?", "c13_1799": "1799", "c13_1799b": "Napoleon’s scholars see it",
        "c13_1799c": "and date it before the biblical Creation", "c13_1821": "1821", "c13_1821b": "blasted out, shipped to Paris",
        "c13_1822": "1822", "c13_1822b": "Champollion reads the cartouche:", "c13_1822c": "a Roman title, autokrator",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ C-A18-01 尼羅河的一年 ══════════════════════
# 河谷剖面：x＝東西向，y＝高度（示意）
VALLEY = [(-0.95, 0.10), (-0.80, 0.10), (-0.70, -0.16), (-0.18, -0.20), (-0.10, -0.34),
          (0.10, -0.34), (0.18, -0.20), (0.70, -0.16), (0.80, 0.10), (0.95, 0.10)]


def c01_rise(ax):
    T(ax, 0, 0.86, tx("c01_title"), 32)
    T(ax, 0, 0.77, tx("c01_sub"), 17, GREY, w="normal")
    xs, ys = zip(*VALLEY)
    ax.plot(xs, ys, c=SAND, lw=3.2, alpha=.9, solid_joinstyle="round", zorder=5)
    for x0 in (-0.66, 0.66):
        T(ax, x0, 0.32, tx("desert"), 16, SAND, w="normal")
    # 平常的河
    ax.add_patch(Polygon([(-0.10, -0.34), (0.10, -0.34), (0.15, -0.25), (-0.15, -0.25)],
                         closed=True, fc=BLUE, ec="none", alpha=.85, zorder=3))
    T(ax, 0, -0.43, tx("river"), 18, BLUE)
    C.arrow(ax, (0.0, -0.06), (0.0, -0.23), c=BLUE, lw=3.0, alpha=.95, style="-|>")
    T(ax, 0, 0.02, tx("rise"), 20, BLUE)


def c01_flood(ax):
    ax.add_patch(Polygon([(-0.70, -0.16), (-0.18, -0.20), (-0.10, -0.34), (0.10, -0.34),
                          (0.18, -0.20), (0.70, -0.16), (0.73, -0.09), (-0.73, -0.09)],
                         closed=True, fc=BLUE, ec="none", alpha=.45, zorder=2))
    T(ax, -0.42, 0.06, tx("flood"), 18, WHITE, w="normal")
    C.arrow(ax, (-0.42, -0.11), (-0.42, 0.01), c=WHITE, lw=1.6, alpha=.7)


def c01_soil(ax):
    for a, b in (((-0.70, -0.16), (-0.18, -0.20)), ((0.18, -0.20), (0.70, -0.16))):
        ax.add_patch(Polygon([a, b, (b[0], b[1] - 0.05), (a[0], a[1] - 0.05)], closed=True,
                             fc=SOIL, ec=AMBER, lw=1.6, alpha=1.0, zorder=6))
    T(ax, 0.44, -0.30, tx("soil"), 17, AMBER, w="normal")
    C.arrow(ax, (0.44, -0.22), (0.44, -0.27), c=AMBER, lw=1.6, alpha=.8)
    T(ax, 0, -0.60, tx("kemet"), 30, AMBER)
    T(ax, 0, -0.70, tx("kemet2"), 17, WHITE, w="normal", alpha=.85)


# ══════════════════════ C-A18-02 消失與晨出 ══════════════════════
def _horizon(ax, y, glow_side, label_side, col):
    ax.plot([-0.88, 0.88], [y, y], c=WHITE, lw=2.0, alpha=.6)
    gx = -0.55 if glow_side == "left" else 0.55
    for k, a in enumerate((.10, .16, .24)):
        ax.add_patch(Wedge((gx, y), 0.38 - 0.10 * k, 0, 180, fc=col, ec="none", alpha=a, zorder=2))
    T(ax, -0.80 if label_side == "left" else 0.80, y - 0.05, tx("west") if label_side == "left" else tx("east"),
      15, GREY, w="normal")


def _star(ax, x, y, s=420, a=1.0):
    ax.scatter([x], [y], s=s, c=WHITE, alpha=a, zorder=9, lw=0, marker="*")


def c02_set(ax):
    T(ax, 0, 0.88, tx("c02_title"), 30)
    T(ax, 0, 0.80, tx("c02_sub"), 16, GREY, w="normal")
    y = 0.42
    _horizon(ax, y, "left", "left", AMBER)
    _star(ax, -0.30, y + 0.10)
    C.arrow(ax, (-0.36, y + 0.02), (-0.31, y + 0.08), c=WHITE, lw=1.6, alpha=.7)
    T(ax, 0.38, y + 0.17, tx("dusk"), 19, AMBER)
    T(ax, 0.38, y + 0.08, tx("dusk2"), 16, WHITE, w="normal")


def c02_gone(ax):
    y = 0.10
    n = 70
    for i in range(n):
        x = -0.80 + 1.60 * i / (n - 1)
        ax.scatter([x], [y], s=26, c=GREY, alpha=.45, lw=0, zorder=4)
    T(ax, 0, y + 0.08, tx("gone"), 21, WHITE)


def c02_dawn(ax):
    y = -0.30
    _horizon(ax, y, "right", "right", PURPLE)
    _star(ax, 0.30, y + 0.06)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        ax.plot([0.30 + 0.035 * math.cos(a), 0.30 + 0.065 * math.cos(a)],
                [y + 0.06 + 0.035 * math.sin(a), y + 0.06 + 0.065 * math.sin(a)], c=WHITE, lw=1.4, alpha=.8)
    T(ax, -0.38, y + 0.17, tx("dawn"), 19, AMBER)
    T(ax, -0.38, y + 0.08, tx("dawn2"), 16, WHITE, w="normal")
    T(ax, 0, y - 0.11, tx("peret"), 18, AMBER, w="normal")


def c02_nile(ax):
    C.water(ax, y=-0.60, x0=-0.70, x1=0.70, c=BLUE, rows=2)
    T(ax, 0, -0.73, tx("nile_rise"), 18, BLUE)
    T(ax, 0, -0.82, tx("newyear"), 16, WHITE, w="normal", alpha=.9)


# ══════════════════════ C-A18-03 曆法的漂移 ══════════════════════
R0, R1 = 0.48, 0.62


def _ang(day):           # 第 day 天 → 角度（12 點鐘方向起、順時針）
    return 90.0 - 360.0 * day / 365.0


def _arc(ax, d0, d1, col, alpha=.85):
    a0, a1 = _ang(d1), _ang(d0)
    ax.add_patch(Wedge((0, -0.05), R1, a0, a1, width=R1 - R0, fc=col, ec="#0B0F1E", lw=1.2, alpha=alpha,
                       zorder=3))


def _at(day, r):
    a = math.radians(_ang(day))
    return r * math.cos(a), -0.05 + r * math.sin(a)


def c03_seasons(ax):
    T(ax, 0, 0.88, tx("c03_title"), 32)
    T(ax, 0, 0.80, tx("c03_sub"), 16, GREY, w="normal")
    for k, (col, key) in enumerate(((BLUE, "akhet"), (GREEN, "peret_s"), (AMBER, "shemu"))):
        _arc(ax, 120 * k, 120 * (k + 1), col)
        for mth in range(1, 4):            # 月界
            x0, y0 = _at(120 * k + 30 * mth, R0)
            x1, y1 = _at(120 * k + 30 * mth, R1)
            ax.plot([x0, x1], [y0, y1], c="#0B0F1E", lw=2.0, zorder=4)
        x, y = _at(120 * k + 60, R1 + 0.11)
        T(ax, x, y, tx(key), 19, col)
        x, y = _at(120 * k + 60, R1 + 0.04)
    T(ax, 0, 0.0, "365", 44, WHITE)
    T(ax, 0, -0.12, tx("m4") + " × 3", 16, GREY, w="normal")


def c03_five(ax):
    _arc(ax, 360, 365, RED, alpha=1.0)
    x, y = _at(362.5, R1 + 0.09)
    T(ax, x - 0.10, y, tx("plus5"), 18, RED)


def c03_drift(ax):
    for i, d in enumerate((0, 6, 12)):
        x, y = _at(d, (R0 + R1) / 2)
        ax.scatter([x], [y], s=520 if i == 0 else 360, c=WHITE, alpha=1.0 if i == 0 else .55 - .15 * i,
                   marker="*", lw=0, zorder=8)
    x0, y0 = _at(2, R1 + 0.07)
    x1, y1 = _at(16, R1 + 0.07)
    C.arrow(ax, (x1, y1), (x0, y0), c=WHITE, lw=2.0, alpha=.85, style="-|>")
    T(ax, 0.55, 0.76, tx("drift"), 18, AMBER)
    T(ax, 0.55, 0.69, tx("drift2"), 18, WHITE)
    T(ax, 0, -0.92, tx("drift3"), 17, GREY, w="normal")


# ══════════════════════ C-A18-04 晚了一個多月 ══════════════════════
D0 = 166            # 6/15（day of year，平年）
D1 = 228            # 8/16


def _dx(doy):
    return -0.84 + 1.68 * (doy - D0) / (D1 - D0)


def c04_old(ax):
    T(ax, 0, 0.86, tx("c04_title"), 30)
    T(ax, 0, 0.78, tx("c04_sub"), 16, GREY, w="normal")
    y = 0.05
    ax.plot([-0.86, 0.86], [y, y], c=WHITE, lw=2.4, alpha=.7, zorder=3)
    for doy in range(D0, D1 + 1):
        tall = doy in (182, 213)          # 7/1、8/1
        ax.plot([_dx(doy)] * 2, [y, y + (0.06 if tall else 0.022)], c=WHITE, lw=1.6 if tall else 0.8,
                alpha=.7 if tall else .35, zorder=3)
    for doy, key in ((171, "jun"), (197, "jul"), (221, "aug")):
        T(ax, _dx(doy), y - 0.06, tx(key), 16, GREY, w="normal")
    xs = _dx(175)                                         # 夏至 6/24
    ax.plot([xs, xs], [y, y + 0.30], c=WHITE, lw=1.4, alpha=.6, ls=(0, (4, 4)))
    T(ax, xs, y + 0.35, tx("solstice"), 16, WHITE, w="normal")
    xo = (_dx(179) + _dx(180)) / 2                        # 6/28–29
    ax.add_patch(Rectangle((_dx(179) - 0.008, y - 0.015), _dx(180) - _dx(179) + 0.016, 0.20,
                           fc=AMBER, ec="none", alpha=.95, zorder=5))
    T(ax, xo + 0.03, y + 0.55, tx("old"), 18, AMBER, ha="left")
    T(ax, xo + 0.03, y + 0.47, tx("old2"), 22, AMBER, ha="left")
    T(ax, xo + 0.03, y + 0.39, tx("old3"), 15, WHITE, ha="left", w="normal")
    ax.plot([xo, xo], [y + 0.19, y + 0.36], c=AMBER, lw=1.4, alpha=.7)


def c04_now(ax):
    y = 0.05
    x2 = (_dx(217) + _dx(218)) / 2                        # 8/5–6
    ax.add_patch(Rectangle((_dx(217) - 0.008, y - 0.015), _dx(218) - _dx(217) + 0.016, 0.20,
                           fc=RED, ec="none", alpha=.95, zorder=5))
    T(ax, x2, y - 0.20, tx("now"), 18, RED)
    T(ax, x2, y - 0.28, tx("now2"), 22, RED)
    xo = (_dx(179) + _dx(180)) / 2
    yb = -0.44
    ax.plot([xo, xo, x2, x2], [yb + 0.04, yb, yb, yb + 0.04], c=WHITE, lw=1.8, alpha=.8)
    T(ax, (xo + x2) / 2, yb - 0.07, tx("late"), 24, WHITE)
    T(ax, 0, -0.80, tx("c04_note"), 14, GREY, w="normal")


# ══════════════════════ C-A18-05 河已經不等了 ══════════════════════
def c05_dam(ax):
    T(ax, 0, 0.86, tx("c05_title"), 30)
    # 上：兩個小圖（一年水位）
    for k, (key, col, flat) in enumerate((("before", BLUE, False), ("after", GREY, True))):
        x0 = -0.84 + 0.92 * k
        ax.plot([x0, x0 + 0.76], [0.42, 0.42], c=WHITE, lw=1.0, alpha=.4)
        xs = [x0 + 0.76 * i / 100 for i in range(101)]
        if flat:
            ys = [0.48 + 0.004 * math.sin(i / 8) for i in range(101)]
        else:
            ys = [0.46 + 0.20 * math.exp(-((i - 55) / 16) ** 2) for i in range(101)]
        ax.plot(xs, ys, c=col if not flat else WHITE, lw=3.0, alpha=.9)
        T(ax, x0 + 0.38, 0.73, tx(key), 16, col if not flat else WHITE, w="normal")
        T(ax, x0 + 0.38, 0.37, tx("yr"), 13, GREY, w="normal")
    # 下：壩的縱剖面（左＝上游、右＝下游）
    g = -0.62
    ax.plot([-0.90, 0.90], [g, g], c=SAND, lw=2.4, alpha=.8)
    ax.add_patch(Polygon([(-0.90, g), (-0.08, g), (-0.08, -0.06), (-0.90, -0.06)], closed=True,
                         fc=BLUE, ec="none", alpha=.55, zorder=2))
    ax.add_patch(Polygon([(-0.08, g), (0.12, g), (0.02, -0.02), (-0.04, -0.02)], closed=True,
                         fc=WHITE, ec="none", alpha=.85, zorder=4))
    ax.add_patch(Polygon([(0.12, g), (0.90, g), (0.90, g + 0.10), (0.12, g + 0.10)], closed=True,
                         fc=BLUE, ec="none", alpha=.55, zorder=2))
    T(ax, -0.49, -0.24, tx("lake"), 18, WHITE)
    T(ax, -0.49, -0.33, tx("flood_held"), 15, WHITE, w="normal", alpha=.85)
    T(ax, 0.02, 0.04, tx("dam"), 18, WHITE)
    T(ax, 0.51, g + 0.18, tx("down"), 16, BLUE, w="normal")


# ══════════════════════ C-A18-06 星星時刻表 ══════════════════════
NC, NR = 8, 12
GX0, GX1, GY0, GY1 = -0.56, 0.86, -0.68, 0.56


def _cell(c, r):
    w = (GX1 - GX0) / NC
    h = (GY1 - GY0) / NR
    return GX0 + w * (c + 0.5), GY1 - h * (r + 0.5), w, h


def c06_grid(ax):
    T(ax, 0, 0.86, tx("c06_title"), 30)
    T(ax, 0, 0.77, tx("c06_sub"), 15, GREY, w="normal")
    for c in range(NC + 1):
        x = GX0 + (GX1 - GX0) * c / NC
        ax.plot([x, x], [GY0, GY1], c=WHITE, lw=0.8, alpha=.3)
    for r in range(NR + 1):
        y = GY1 - (GY1 - GY0) * r / NR
        ax.plot([GX0, GX1], [y, y], c=WHITE, lw=0.8, alpha=.3)
    for c in range(NC):
        for r in range(NR):
            d = c + r + 1                                  # 第 c 旬第 r 小時＝第 c+r+1 組星
            x, y, w, h = _cell(c, r)
            hi = d == 12
            T(ax, x, y, str(d), 17, AMBER if hi else WHITE, w="bold" if hi else "normal",
              alpha=1.0 if hi else .6)
    for c in (0, NC - 1):
        x, _, _, _ = _cell(c, 0)
        T(ax, x, GY1 + 0.04, tx("col").format(c + 1), 14, GREY, w="normal")
    T(ax, 0.10, GY0 - 0.08, tx("c06_diag"), 15, AMBER, w="normal")
    T(ax, 0, -0.88, tx("c06_note"), 14, GREY, w="normal")


def c06_hours(ax):
    w = (GX1 - GX0) / NC
    ax.add_patch(Rectangle((GX0, GY0), w, GY1 - GY0, fc="none", ec=BLUE, lw=3.0, zorder=6))
    for r in range(NR):
        _, y, _, _ = _cell(0, r)
        T(ax, GX0 - 0.03, y, tx("hour").format(r + 1), 14, BLUE, ha="right", w="normal")
    T(ax, 0.10, GY1 + 0.11, tx("c06_12") + tx("c06_12b"), 16, BLUE)


# ══════════════════════ C-A18-07 北面的入口 ══════════════════════
def c07_section(ax):
    T(ax, 0, 0.86, tx("c07_title"), 30)
    T(ax, 0, 0.78, tx("c07_sub"), 16, GREY, w="normal")
    g = -0.40
    half, hgt = 0.62, 0.62 * math.tan(math.radians(51.84))
    s = 0.62 / half
    ax.plot([-0.95, 0.95], [g, g], c=SAND, lw=2.0, alpha=.7)
    T(ax, -0.84, g - 0.05, tx("ground"), 13, SAND, w="normal")
    ax.add_patch(Polygon([(-half, g), (half, g), (0, g + hgt * 0.62)], closed=True, fc="none",
                         ec=SAND, lw=3.0, zorder=4))
    top = g + hgt * 0.62
    # 北面＝右側斜面；入口在北面離地約 1/8 高處
    ex = half - (half / (top - g)) * 0.10
    ey = g + 0.10
    ax.scatter([ex], [ey], s=180, c=AMBER, zorder=8, lw=0)
    ang = math.radians(26.5)
    L = 0.75
    px, py = ex - L * math.cos(ang), ey - L * math.sin(ang)
    ax.plot([ex, px], [ey, py], c=AMBER, lw=3.0, zorder=7)
    T(ax, ex + 0.06, ey + 0.08, tx("entrance"), 19, AMBER, ha="left")
    T(ax, (ex + px) / 2 + 0.04, (ey + py) / 2 - 0.09, tx("passage"), 15, AMBER, w="normal")
    T(ax, 0.88, g + 0.10, tx("north"), 22, WHITE)
    T(ax, -0.88, g + 0.10, tx("south"), 22, GREY)
    C.arrow(ax, (0.80, 0.55), (0.55, 0.20), c=WHITE, lw=1.8, alpha=.6, style="-|>")
    T(ax, 0.42, 0.64, tx("sky"), 17, WHITE, w="normal")


# ══════════════════════ C-A18-08 拉繩定位 ══════════════════════
def c08_stakes(ax):
    T(ax, 0, 0.86, tx("c08_title"), 30)
    T(ax, 0, 0.78, tx("c08_sub"), 16, GREY, w="normal")
    # 神廟外框（俯視；上＝北）
    x0, x1, y0, y1 = -0.42, 0.42, -0.70, -0.06
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec=WHITE, lw=1.6, ls=(0, (6, 5)),
                           alpha=.6, zorder=3))
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        ax.scatter([x], [y], s=150, c=AMBER, marker="s", lw=0, zorder=6)
    T(ax, 0, y0 - 0.08, tx("corners"), 17, AMBER, w="normal")
    # 兩根木樁＋繩（南北向）
    sx, sy0, sy1 = 0.0, -0.58, -0.18
    ax.plot([sx, sx], [sy0, sy1], c=AMBER, lw=3.2, zorder=7)
    for y in (sy0, sy1):
        ax.add_patch(Circle((sx, y), 0.025, fc=WHITE, ec="none", zorder=8))
    T(ax, sx + 0.05, (sy0 + sy1) / 2, tx("rope"), 15, AMBER, ha="left", w="normal")
    C.human_figure(ax, -0.22, -0.38, s=0.40, c=WHITE, alpha=.9)
    C.human_figure(ax, 0.22, -0.38, s=0.40, c=WHITE, alpha=.9)
    T(ax, -0.22, -0.55, tx("king"), 15, WHITE, w="normal")
    T(ax, 0.22, -0.55, tx("goddess"), 15, WHITE, w="normal")
    T(ax, 0, -0.88, tx("c08_note"), 14, GREY, w="normal")


def c08_leg(ax):
    # 北斗示意（真實相對位置，等距方位投影到天極附近；北在上、東在左）
    hips = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
    pts = []
    for h in hips:
        ra, dec = S[h][:2]
        r = (90.0 - dec) / 90.0
        a = math.radians(ra - 180.0)
        pts.append((r * math.sin(a), r * math.cos(a)))
    cxs, cys = sum(p[0] for p in pts) / 7, sum(p[1] for p in pts) / 7
    sc = 2.2
    P = [((x - cxs) * sc, 0.36 + (y - cys) * sc) for x, y in pts]
    order = [0, 1, 2, 3, 0, 3, 4, 5, 6]
    ax.plot([P[i][0] for i in order], [P[i][1] for i in order], c=AMBER, lw=2.4, alpha=.9, zorder=5)
    for x, y in P:
        ax.scatter([x], [y], s=120, c=WHITE, lw=0, zorder=6)
    ax.plot([0.0, 0.0], [-0.14, 0.16], c=WHITE, lw=1.6, ls=(0, (3, 4)), alpha=.7)
    T(ax, 0.0, 0.68, tx("leg"), 18, AMBER)


# ══════════════════════ C-A18-09 兩千五百年 ══════════════════════
Y0, Y1 = -2800, 2200


def _yx(yr):
    return -0.86 + 1.72 * (yr - Y0) / (Y1 - Y0)


def c09_line(ax):
    T(ax, 0, 0.82, tx("c09_title"), 30)
    y = 0.0
    ax.plot([_yx(Y0), _yx(Y1)], [y, y], c=WHITE, lw=2.4, alpha=.6)
    for yr in range(-2500, 2001, 500):
        ax.plot([_yx(yr)] * 2, [y, y + 0.025], c=WHITE, lw=1.0, alpha=.4)
    ax.plot([_yx(1)] * 2, [y - 0.03, y + 0.05], c=WHITE, lw=1.4, alpha=.6)
    for yr, k1, k2, col, up in ((-2560, "khufu", "khufu2", AMBER, True), (-50, "dend", "dend2", BLUE, True)):
        x = _yx(yr)
        ax.scatter([x], [y], s=260, c=col, zorder=6, lw=0)
        dy = 0.20 if up else -0.20
        ax.plot([x, x], [y, y + dy * 0.7], c=col, lw=1.6, alpha=.7)
        T(ax, x, y + dy + 0.06, tx(k1), 20, col)
        T(ax, x, y + dy - 0.02, tx(k2), 16, col, w="normal")
    ax.add_patch(Rectangle((_yx(-51), y - 0.07), _yx(-30) - _yx(-51), 0.05, fc=RED, ec="none", zorder=5))
    T(ax, _yx(-40), y - 0.15, tx("cleo"), 16, RED)
    T(ax, _yx(-40), y - 0.23, tx("cleo2"), 14, RED, w="normal")
    xa, xb = _yx(-2560), _yx(-50)
    yb = -0.40
    ax.plot([xa, xa, xb, xb], [yb + 0.04, yb, yb, yb + 0.04], c=WHITE, lw=1.8, alpha=.8)
    T(ax, (xa + xb) / 2, yb - 0.08, tx("gap"), 24, WHITE)
    ax.scatter([_yx(2027)], [y], s=160, c=WHITE, zorder=6, lw=0)
    T(ax, _yx(2027), y + 0.09, tx("now9"), 15, WHITE, w="normal")
    T(ax, 0, -0.80, tx("c09_note"), 14, GREY, w="normal")


# ══════════════════════ v2：C-A18-11 一千四百六十年（06 鏡） ══════════════════════
def c11_circle(ax):
    T(ax, 0, 0.88, tx("c11_title"), 32)
    T(ax, 0, 0.80, tx("c11_sub"), 16, GREY, w="normal")
    for k, col in enumerate((BLUE, GREEN, AMBER)):
        _arc(ax, 120 * k, 120 * (k + 1), col, alpha=.45)
    _arc(ax, 360, 365, RED, alpha=.6)
    # 天狼星晨出的標記繞完一整圈（順時針外圈箭頭）
    r = R1 + 0.07
    pts = [_at(d, r) for d in range(4, 357, 4)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=WHITE, lw=2.2, alpha=.8, zorder=6)
    C.arrow(ax, _at(0.5, r), pts[-1], c=WHITE, lw=2.2, alpha=.9, style="-|>")
    x, y = _at(0, (R0 + R1) / 2)
    ax.scatter([x], [y], s=620, c=WHITE, marker="*", lw=0, zorder=8)
    T(ax, 0, 0.06, tx("c11_139"), 30, AMBER)
    T(ax, 0, -0.06, tx("c11_after"), 24, WHITE)
    T(ax, 0, -0.80, tx("c11_139b"), 18, AMBER)
    T(ax, 0, -0.90, tx("c11_src"), 14, GREY, w="normal")


# ══════════════════════ v2：C-A18-12 對正北（13 鏡） ══════════════════════
def c12_square(ax):
    T(ax, 0, 0.88, tx("c12_title"), 28)
    T(ax, 0, 0.80, tx("c12_sub"), 16, GREY, w="normal")
    h = 0.30
    cy = -0.22
    ax.add_patch(Polygon([(-h, cy - h), (h, cy - h), (h, cy + h), (-h, cy + h)], closed=True,
                         fc="none", ec=SAND, lw=3.0, zorder=4))
    for (a, b) in (((-h, cy - h), (h, cy + h)), ((h, cy - h), (-h, cy + h))):
        ax.plot([a[0], b[0]], [a[1], b[1]], c=SAND, lw=1.2, alpha=.6, zorder=4)
    # 南北線延伸到北天極
    ax.plot([0, 0], [cy + h, 0.50], c=WHITE, lw=1.6, ls=(0, (4, 4)), alpha=.8, zorder=5)
    ax.scatter([0], [0.55], s=260, c=WHITE, marker="+", lw=2.4, zorder=7)
    T(ax, 0.16, 0.55, tx("c12_pole"), 15, WHITE, ha="left", w="normal")
    for t, (x, y) in (("north", (0, cy + h + 0.07)), ("south", (0, cy - h - 0.07))):
        T(ax, x + 0.06, y, tx(t), 18, WHITE if t == "north" else GREY)
    T(ax, 0, cy - h - 0.17, tx("c12_err"), 18, AMBER)
    T(ax, -0.62, 0.40, tx("c12_q"), 18, WHITE, w="normal")
    T(ax, -0.62, 0.31, tx("c12_guess"), 16, AMBER, w="normal")
    ax.add_patch(FancyBboxPatch((-0.95, 0.24), 0.66, 0.24, boxstyle="round,pad=0.01", fc="none",
                                ec=AMBER, lw=1.2, ls=(0, (3, 3)), alpha=.7, zorder=3))
    T(ax, 0, -0.90, tx("c12_note"), 14, GREY, w="normal")


# ══════════════════════ v2：C-A18-13 以為有好幾千年（16 鏡） ══════════════════════
def c13_line(ax):
    T(ax, 0, 0.84, tx("c13_title"), 32)
    xs = (-0.62, 0.0, 0.62)
    y = 0.05
    ax.plot([-0.85, 0.85], [y, y], c=WHITE, lw=2.4, alpha=.6)
    rows = (("c13_1799", "c13_1799b", "c13_1799c", AMBER), ("c13_1821", "c13_1821b", None, RED),
            ("c13_1822", "c13_1822b", "c13_1822c", BLUE))
    for x, (k0, k1, k2, col) in zip(xs, rows):
        ax.scatter([x], [y], s=260, c=col, lw=0, zorder=6)
        T(ax, x, y + 0.13, tx(k0), 26, col)
        T(ax, x, y - 0.14, tx(k1), 15, WHITE, w="normal")
        if k2:
            T(ax, x, y - 0.23, tx(k2), 15, WHITE, w="normal")


# ══════════════════════ C-A18-10 今晚十點半（9:16 圖卡） ══════════════════════
TPE = ("25.0330", "121.5654")


def altaz(hip=None, body=None):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = TPE; o.temp, o.pressure = 15, 1010
    o.date = ephem.Date("2027/1/22 14:30")              # 22:30 UTC+8
    if hip is not None:
        ra, dec = S[hip][:2]
        b = ephem.FixedBody(); b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    else:
        b = body
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def c10_card(ax):
    import ephem
    ax.text(0.5, 0.945, tx("c10_title"), fontproperties=C.FP, fontsize=27, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, tx("c10_date"), fontproperties=C.FP, fontsize=14, color=GREY, ha="center", va="center")
    # 上：面向正南（方位 150–240、高度 0–75）
    X0, X1, Yb, Yt = 0.06, 0.94, 0.42, 0.86
    AZ0, AZ1, AL1 = 145.0, 235.0, 75.0

    def P(alt, az):
        return X0 + (X1 - X0) * (az - AZ0) / (AZ1 - AZ0), Yb + (Yt - Yb) * alt / AL1
    ax.plot([X0, X1], [Yb, Yb], c=WHITE, lw=1.6, alpha=.7)
    ax.add_patch(Rectangle((X0, Yb - 0.02), X1 - X0, 0.02, fc="#1B2240", ec="none"))
    for az, k in ((157.5, "SE"), (180, "S"), (202.5, "SW")):
        x, _ = P(0, az)
        ax.text(x, Yb - 0.035, tx(k), fontproperties=C.FP, fontsize=13, color=GREY, ha="center", va="center")
    for alt in (15, 30, 45, 60):
        _, y = P(alt, AZ0)
        ax.plot([X0, X1], [y, y], c=WHITE, lw=0.6, alpha=.12)
        ax.text(X0 - 0.01, y, f"{alt}°", fontproperties=C.FP, fontsize=9, color=GREY, ha="right", va="center")
    ori = {27989: "betel", 24436: "rigel", 25336: None, 27366: None, 25930: None, 26311: None, 26727: None}
    pos = {h: P(*altaz(h)) for h in ori}
    for a, b in ((27989, 25336), (25336, 25930), (25930, 26311), (26311, 26727), (26727, 27366), (27366, 24436),
                 (24436, 25930), (27989, 26727)):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=BLUE, lw=1.4, alpha=.8)
    for h, k in ori.items():
        ax.scatter(*pos[h], s=70 if k else 40, c=WHITE, lw=0, zorder=5)
        if k:
            ax.text(pos[h][0] + 0.02, pos[h][1], tx(k), fontproperties=C.FP, fontsize=11, color=WHITE,
                    ha="left", va="center")
    xo = sum(p[0] for p in pos.values()) / 7
    yo = max(p[1] for p in pos.values()) + 0.025
    ax.text(xo, yo, tx("orion"), fontproperties=C.FP, fontsize=13, color=BLUE, ha="center", va="center",
            weight="bold")
    xs, ys = P(*altaz(32349))
    ax.scatter([xs], [ys], s=260, c=WHITE, marker="*", lw=0, zorder=6)
    ax.text(xs - 0.03, ys, tx("sirius"), fontproperties=C.FP, fontsize=15, color=AMBER, ha="right",
            va="center", weight="bold")
    xc, yc = P(*altaz(30438))
    ax.scatter([xc], [yc], s=110, c=WHITE, lw=0, zorder=6)
    ax.text(xc - 0.03, yc, tx("canopus"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="right",
            va="center", weight="bold")
    ax.plot([xs, xc], [ys - 0.015, yc + 0.012], c=WHITE, lw=0.8, alpha=.35, ls=(0, (3, 3)))
    ax.text(0.5, Yt + 0.012, tx("south_view"), fontproperties=C.FP, fontsize=12, color=GREY, ha="center",
            va="center")
    # 下：面向東北（方位 0–75、高度 0–45）
    X0b, X1b, Yb2, Yt2 = 0.10, 0.90, 0.17, 0.315
    AZa, AZb, ALb = 0.0, 75.0, 45.0

    def Q(alt, az):
        return X0b + (X1b - X0b) * (az - AZa) / (AZb - AZa), Yb2 + (Yt2 - Yb2) * alt / ALb
    ax.text(0.5, 0.348, tx("ne_view"), fontproperties=C.FP, fontsize=12, color=GREY, ha="center", va="center")
    ax.plot([X0b, X1b], [Yb2, Yb2], c=WHITE, lw=1.6, alpha=.7)
    for az, k in ((0, "N"), (45, "NE")):
        x, _ = Q(0, az)
        ax.text(x, Yb2 - 0.018, tx(k), fontproperties=C.FP, fontsize=13, color=GREY, ha="center", va="center")
    dip = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
    q = [Q(*altaz(h)) for h in dip]
    order = [0, 1, 2, 3, 0, 3, 4, 5, 6]
    ax.plot([q[i][0] for i in order], [q[i][1] for i in order], c=AMBER, lw=1.6, alpha=.9)
    for p in q:
        ax.scatter(*p, s=40, c=WHITE, lw=0, zorder=5)
    ax.text(q[0][0] - 0.02, q[0][1], tx("dub"), fontproperties=C.FP, fontsize=11, color=WHITE, ha="right",
            va="center")
    ax.text(q[6][0] + 0.02, q[6][1], tx("alk"), fontproperties=C.FP, fontsize=11, color=WHITE, ha="left",
            va="center")
    ax.text((q[3][0] + q[0][0]) / 2, max(p[1] for p in q) + 0.022, tx("leg10"), fontproperties=C.FP,
            fontsize=13, color=AMBER, ha="center", va="center", weight="bold")
    # 月亮（東方，在兩張圖之外，文字註記）
    ma, mz = altaz(body=ephem.Moon())
    for i, (s_, col) in enumerate(((tx("moon") + f"；{tx('jup')}在旁" if LANG == "zh" else tx("moon") + f"; {tx('jup')} nearby", WHITE),
                                  (tx("c10_n1"), WHITE), (tx("c10_n2"), AMBER), (tx("c10_n3"), WHITE))):
        ax.text(0.5, 0.128 - 0.019 * i, s_, fontproperties=C.FP, fontsize=12, color=col, ha="center", va="center")
    ax.text(0.5, 0.045, tx("c10_src"), fontproperties=C.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.028, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE, ha="center",
            va="center")
    print(f"  今晚 22:30 月亮 {ma:.1f}°／{mz:.0f}°；天狼星 {altaz(32349)[0]:.1f}°／{altaz(32349)[1]:.0f}°；"
          f"老人星 {altaz(30438)[0]:.1f}°；天樞 {altaz(54061)[0]:.1f}°；搖光 {altaz(67301)[0]:.1f}°")


S = None


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    C.emit("", [("漲水", c01_rise), ("淹沒", c01_flood), ("黑土", c01_soil)], title="C-A18-01_尼羅河的一年")
    C.emit("", [("西沉", c02_set), ("消失", c02_gone), ("晨出", c02_dawn), ("漲水", c02_nile)],
           title="C-A18-02_消失與晨出")
    C.emit("", [("三季", c03_seasons), ("五天", c03_five), ("漂移", c03_drift)], title="C-A18-03_曆法的漂移")
    C.emit("", [("古代", c04_old), ("今天", c04_now)], title="C-A18-04_晚了一個多月")
    C.emit("", [("高壩", c05_dam)], title="C-A18-05_河已經不等了")
    C.emit("", [("格子", c06_grid), ("十二小時", c06_hours)], title="C-A18-06_星星時刻表")
    C.emit("", [("剖面", c07_section)], title="C-A18-07_北面的入口")
    C.emit("", [("木樁", c08_stakes), ("牛腿", c08_leg)], title="C-A18-08_拉繩定位")
    C.emit("", [("年表", c09_line)], title="C-A18-09_兩千五百年")
    C.emit("", [("一圈", c11_circle)], title="C-A18-11_一千四百六十年")
    C.emit("", [("方框", c12_square)], title="C-A18-12_對正北")
    C.emit("", [("年表", c13_line)], title="C-A18-13_以為有好幾千年")
    f, ax = C.newcard(dark=True)
    c10_card(ax)
    C.save(f, "", "C-A18-10_今晚十點半_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
