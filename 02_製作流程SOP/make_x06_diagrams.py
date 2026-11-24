# -*- coding: utf-8 -*-
"""X-06 星星導航總集｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-X06-01_時間軸          → 02 鏡（莎湖層）、03b 鏡（莎湖→奧德賽→萍洲層）、04 鏡（前情層＝前三層合成 → 南島層）
  C-X06-02_兩個三十二      → 09 鏡（夏威夷層 → 阿拉伯層）
  C-X06-03_星星航海的三件事 → 10 鏡（9:16 圖卡，可存圖）
  C-X06-04_今晚自己導航    → 12 鏡迄格（9:16 圖卡，可存圖）
  C-X06-05_星路            → 07 鏡（海面層 → 星路層）
  05 鏡沿用 A-09 的 C-A09-01_星羅盤（make_x06_v4.py 複製到本集 _概念圖/）
輸出：05_素材/X-06_星星導航總集/_概念圖/（--lang en → _概念圖/en/）

來源：逐字稿 v1 考據備忘；Homer, Odyssey 5.270–277；朱彧《萍洲可談》卷二；O'Connell et al. 2018；Kealy, Louys & O'Connor 2017、2018；
  Bellwood 2017、Rasyid et al. 2021 §18.4；Burley et al. 2012；Wilmshurst et al. 2011；Firth 1954（Tikopia→阿努塔星路九顆星）；
  A-09（夏威夷星羅盤，Nainoa Thompson）；阿拉伯 32 星位：二手整理（Tibbetts 1971 原書未核）→ 右盤只畫北極星、南天極與幾顆有把握的亮星，
  方位用北緯 20° 自算（與 09 鏡星圖同一條地平線）。地圖＝經緯度實際位置的點與箭頭（等距圓柱），不畫海岸線、不臨摹已出版遷徙圖。
  天象 PyEphem 4.2.1（make_x06_v4.py 與逐字稿星空對時表）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/X-06_星星導航總集/_概念圖")
C.set_base(OUT)
RED, GREY = "#FF6B6B", "#8A97B4"
LANG = "zh"
TXT = {
    "zh": {
        "c01_title": "在羅盤上船以前", "c01_sub": "時間軸不按比例",
        "now": "今天",
        "sahul_t": "5 萬年前", "sahul1": "渡海到莎湖", "sahul2": "（澳洲＋新幾內亞）",
        "sahul3": "沿途的島多半", "sahul4": "一座看得見下一座", "sahul_q": "有沒有用星星？沒有證據",
        "ody_t": "約 2,700 年前", "ody1": "《奧德賽》", "ody2": "讓大熊留在左手邊",
        "pz_t": "1119 年", "pz1": "《萍洲可談》", "q1": "夜則觀星，", "q2": "晝則觀日，", "q3": "陰晦觀指南針。",
        "an1_t": "約 4,000 年前", "an1": "從台灣南下",
        "an2_t": "約 2,900 年前", "an2": "到東加",
        "an3_t": "800–1,000 年前", "an3": "到夏威夷",
        "map_note": "實線＝沿途看得見島　虛線＝看不見陸地的航段（示意）",
        "Taiwan": "台灣", "Luzon": "菲律賓", "Sulawesi": "蘇拉威西", "Bismarck": "俾斯麥群島",
        "Vanuatu": "萬那杜", "Fiji": "斐濟", "Tonga": "東加", "Samoa": "薩摩亞", "Tahiti": "大溪地",
        "Hawaii": "夏威夷",
        "c02_haw": "夏威夷：32 間房子", "c02_haw2": "Nainoa Thompson 整理的星羅盤（A-09）",
        "c02_ara": "阿拉伯：32 個星位", "c02_ara2": "亮星升起（東）、落下（西）的方向",
        "N": "北", "E": "東", "S": "南", "W": "西",
        "jah": "北極星", "jah2": "al-Jāh", "scp": "南天極",
        "五車二": "五車二", "織女": "織女", "昴宿": "昴宿", "大角": "大角", "牛郎": "牛郎", "心宿二": "心宿二", "老人星": "老人星",
        "c02_mid": "兩套系統，各自發展", "c02_foot1": "右盤只畫有把握的幾顆（星位表見 Tibbetts 1971，原書未核）",
        "c02_foot2": "升落方位以北緯 20° 自算；西邊同名落下的點畫成小點",
        "c03_title": "星星航海的三件事", "c03_sub": "不管在哪片海，問的都是這三個",
        "c03_h1": "方向", "c03_q1": "星從哪裡升起、落下",
        "c03_e1": ["夏威夷：地平線切成 32 間房子", "阿拉伯：32 個星位，用亮星命名", "Tikopia→阿努塔：九顆星輪流對準船頭"],
        "c03_h2": "緯度", "c03_q2": "北極星多高、哪顆星過頭頂",
        "c03_e2": ["北極星的高度≈所在的緯度（台北約 25°）", "大角星過頭頂＝北緯 19° 的夏威夷"],
        "c03_h3": "季節", "c03_q3": "星什麼時候出現",
        "c03_e3": ["曼達爾：魟魚 11 月底、鯊魚 12 月底清晨升起", "＝西北季風要來了", "東加：ʻUvea 的圓環戴上島空，才拿來駕船"],
        "c03_foot": "萬國星空 EP41｜A-09 夏威夷・A-10 東加・A-11 阿努塔・A-26 布吉斯・A-27 曼達爾",
        "c04_title": "今晚自己導航", "c04_sub": "2027/5/21（五）台北",
        "c04_rows": [
            ("正北・整晚", "北極星 24.4°–25.1°", "＝台北的緯度（25.0°N）", AMBER),
            ("20:26–20:30・正南", "南十字上中天", "十字架一 7.8°、十字架二 2.0°；墾丁 10.9°／5.0°", AMBER),
            ("22:14・頭頂", "大角星 84.0°", "離頭頂 6°＝它過北緯 19° 的夏威夷頭頂", GREEN),
            ("21:00 後・東南", "月亮在心宿二旁 3–4.5°", "剛過滿月（98.7%），暗星都被月光蓋掉", PURPLE),
        ],
        "c04_sun": "日落 18:34　天全黑 19:59",
        "c04_foot": "PyEphem 計算，含大氣折射；南十字要找南方海面沒有遮蔽的地方",
        "tags": "#萬國星空　#師大天文社",
        "c05_title": "星路：一顆接一顆", "c05_sub": "Tikopia → 阿努塔　{km:.0f} km（往東北 {brg:.0f}°）",
        "c05_bow": "船頭", "c05_dest": "阿努塔在這個方向",
        "c05_s1": "升高了：換下一顆", "c05_s2": "貼著海面：對準船頭", "c05_s3": "下一顆（快升起）",
        "c05_box1": "Firth 1954：Tikopia 的酋長說，往阿努塔的星路有九顆星",
        "c05_box2": "一顆貼著海面時對準船頭；升高了，就換下一顆",
        "c05_box3": "圖中的星是示意，不是那九顆星的實際位置",
    },
    "en": {
        "c01_title": "Before the compass came aboard", "c01_sub": "timeline not to scale",
        "now": "today",
        "sahul_t": "50,000 years ago", "sahul1": "Crossing to Sahul", "sahul2": "(Australia + New Guinea)",
        "sahul3": "Most islands on the way", "sahul4": "could see the next one", "sahul_q": "Stars used? No evidence",
        "ody_t": "c. 2,700 years ago", "ody1": "The Odyssey", "ody2": "keep the Bear on your left",
        "pz_t": "AD 1119", "pz1": "Pingzhou Ketan", "q1": "By night, the stars;", "q2": "by day, the sun;",
        "q3": "overcast: the compass.",
        "an1_t": "4,000 yrs ago", "an1": "from Taiwan",
        "an2_t": "2,900 yrs ago", "an2": "to Tonga",
        "an3_t": "800–1,000 yrs ago", "an3": "to Hawaiʻi",
        "map_note": "solid = islands in sight   dashed = open-sea legs out of sight of land (schematic)",
        "Taiwan": "Taiwan", "Luzon": "Philippines", "Sulawesi": "Sulawesi", "Bismarck": "Bismarck Is.",
        "Vanuatu": "Vanuatu", "Fiji": "Fiji", "Tonga": "Tonga", "Samoa": "Samoa", "Tahiti": "Tahiti",
        "Hawaii": "Hawaiʻi",
        "c02_haw": "Hawaiʻi: 32 houses", "c02_haw2": "the star compass organised by Nainoa Thompson",
        "c02_ara": "Arabia: 32 star points", "c02_ara2": "where bright stars rise (E) and set (W)",
        "N": "N", "E": "E", "S": "S", "W": "W",
        "jah": "Polaris", "jah2": "al-Jāh", "scp": "S. pole",
        "五車二": "Capella", "織女": "Vega", "昴宿": "Pleiades", "大角": "Arcturus", "牛郎": "Altair", "心宿二": "Antares",
        "老人星": "Canopus",
        "c02_mid": "Two systems, developed separately",
        "c02_foot1": "Only a few certain points shown (star table: Tibbetts 1971, not checked in the original)",
        "c02_foot2": "Rising azimuths computed for 20°N; setting points in the west shown as dots",
        "c03_title": "Three things star navigators ask", "c03_sub": "whatever the ocean",
        "c03_h1": "Direction", "c03_q1": "where a star rises and sets",
        "c03_e1": ["Hawaiʻi: the horizon in 32 houses", "Arab: 32 points named after bright stars",
                   "Tikopia→Anuta: nine stars, one after another at the bow"],
        "c03_h2": "Latitude", "c03_q2": "how high Polaris is; which star passes overhead",
        "c03_e2": ["Polaris' altitude ≈ your latitude (Taipei ~25°)", "Arcturus overhead = Hawaiʻi at 19°N"],
        "c03_h3": "Season", "c03_q3": "when a star appears",
        "c03_e3": ["Mandar: Stingray (late Nov.), Shark (late Dec.) at dawn", "= the NW monsoon is coming",
                   "Tonga: sail when the Ring of ʻUvea crowns the island"],
        "c03_foot": "World Sky Cultures EP41",
        "c04_title": "Navigate tonight", "c04_sub": "Taipei, Fri 21 May 2027",
        "c04_rows": [
            ("due north, all night", "Polaris 24.4°–25.1°", "= Taipei's latitude (25.0°N)", AMBER),
            ("20:26–20:30, due south", "Southern Cross on the meridian", "γ 7.8°, α 2.0°; Kenting 10.9° / 5.0°", AMBER),
            ("22:14, overhead", "Arcturus at 84.0°", "6° from the zenith: it passes over Hawaiʻi at 19°N", GREEN),
            ("after 21:00, SE", "Moon 3–4.5° from Antares", "just past full (98.7%); faint stars washed out", PURPLE),
        ],
        "c04_sun": "sunset 18:34   full dark 19:59",
        "c04_foot": "PyEphem, with refraction; for the Cross you need a clear southern sea horizon",
        "tags": "#WorldSkyCultures",
        "c05_title": "A star path", "c05_sub": "Tikopia → Anuta  {km:.0f} km (bearing {brg:.0f}°)",
        "c05_bow": "bow", "c05_dest": "Anuta lies this way",
        "c05_s1": "risen too high: switch", "c05_s2": "low on the sea: steer by it", "c05_s3": "next one, about to rise",
        "c05_box1": "Firth 1954: a Tikopia chief said the path to Anuta has nine stars",
        "c05_box2": "steer by one while it is low; when it climbs, take the next",
        "c05_box3": "Stars drawn here are schematic, not the actual nine",
    },
}


def tx(k):
    return TXT[LANG][k]


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371.0 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) *
                                            math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


# ══════════════════════ C-X06-01 時間軸 ══════════════════════
AX_Y = 0.36
XP = {"sahul": -0.80, "an1": -0.36, "an2": -0.10, "ody": 0.06, "an3": 0.38, "pz": 0.66, "now": 0.90}


def dot(ax, x, col, s=260):
    ax.scatter([x], [AX_Y], s=s, c=col, zorder=6, lw=0)


def c01_sahul(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 32, WHITE)
    T(ax, 0.0, 0.855, tx("c01_sub"), 14, GREY, w="normal")
    ax.plot([-0.92, 0.92], [AX_Y, AX_Y], c=WHITE, lw=2.2, alpha=.65, zorder=3)
    for xb in (-0.60, -0.56):                                     # 斷軸記號
        ax.plot([xb - 0.015, xb + 0.015], [AX_Y - 0.03, AX_Y + 0.03], c=WHITE, lw=2.2, alpha=.8, zorder=4)
    ax.add_patch(C.Rectangle((-0.595, AX_Y - 0.012), 0.03, 0.024, fc=C.BG, ec="none", zorder=3.5))
    ax.annotate("", xy=(0.95, AX_Y), xytext=(0.90, AX_Y),
                arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=2.0, alpha=.7))
    T(ax, XP["now"], AX_Y + 0.06, tx("now"), 14, GREY, w="normal")
    dot(ax, XP["sahul"], WHITE)
    T(ax, XP["sahul"], AX_Y + 0.07, tx("sahul_t"), 19, WHITE)
    x0 = -0.95
    for i, (k, fs, col) in enumerate((("sahul1", 17, WHITE), ("sahul2", 13, GREY), ("sahul3", 14, WHITE),
                                      ("sahul4", 14, WHITE))):
        T(ax, x0, AX_Y - 0.08 - 0.055 * i, tx(k), fs, col, ha="left", w="bold" if i == 0 else "normal")
    T(ax, x0, AX_Y - 0.08 - 0.055 * 4 - 0.01, tx("sahul_q"), 15, AMBER, ha="left")


def c01_odyssey(ax):
    dot(ax, XP["ody"], AMBER)
    ax.plot([XP["ody"], XP["ody"]], [AX_Y, AX_Y + 0.12], c=AMBER, lw=1.6, alpha=.7)
    T(ax, XP["ody"], AX_Y + 0.17, tx("ody_t"), 17, AMBER)
    T(ax, XP["ody"], AX_Y + 0.235, tx("ody1"), 19, WHITE)
    T(ax, XP["ody"], AX_Y + 0.29, tx("ody2"), 14, WHITE, w="normal")


def c01_pz(ax):
    x = XP["pz"]
    dot(ax, x, BLUE)
    ax.plot([x, x], [AX_Y, AX_Y + 0.08], c=BLUE, lw=1.6, alpha=.7)
    T(ax, x, AX_Y + 0.12, tx("pz_t"), 17, BLUE)
    T(ax, x, AX_Y + 0.18, tx("pz1"), 19, WHITE)
    for i, k in enumerate(("q1", "q2", "q3")):
        T(ax, x, AX_Y + 0.25 + 0.06 * (2 - i) + 0.0, tx(k), 18 if k != "q3" else 21,
          AMBER if k == "q3" else WHITE, w="bold" if k == "q3" else "normal")


def c01_prev(ax):
    c01_sahul(ax); c01_odyssey(ax); c01_pz(ax)


P = {"Taiwan": (23.7, 121.0), "Luzon": (16.5, 121.0), "Sulawesi": (-2.0, 120.5), "Bismarck": (-5.5, 151.0),
     "Vanuatu": (-15.8, 167.0), "Fiji": (-17.8, 178.0), "Tonga": (-21.1, 184.8), "Samoa": (-13.8, 187.8),
     "Tahiti": (-17.6, 210.6), "Hawaii": (19.8, 204.5)}
LON0, LON1, LAT0, LAT1 = 116.0, 216.0, -25.0, 27.0
MX0, MX1, MY0 = -0.90, 0.90, -0.94
MS = (MX1 - MX0) / (LON1 - LON0)


def mp(lat, lon):
    return MX0 + (lon - LON0) * MS, MY0 + (lat - LAT0) * MS


def c01_austronesian(ax):
    for k, col in (("an1", GREEN), ("an2", GREEN), ("an3", GREEN)):
        x = XP[k]
        dot(ax, x, col, s=200)
        ax.plot([x, x], [AX_Y, AX_Y - 0.05], c=col, lw=1.6, alpha=.7)
        T(ax, x, AX_Y - 0.085, tx(k + "_t"), 14, col)
        T(ax, x, AX_Y - 0.135, tx(k), 14, WHITE, w="normal")
    # 點狀地圖
    ytop = mp(LAT1, LON0)[1]
    ax.add_patch(C.FancyBboxPatch((MX0 - 0.03, MY0 - 0.03), MX1 - MX0 + 0.06, ytop - MY0 + 0.06,
                                  boxstyle="round,pad=0.0,rounding_size=0.03", fc="#10172E", ec=GREY,
                                  lw=1.0, alpha=.9, zorder=2))
    y0 = mp(0, LON0)[1]
    ax.plot([MX0, MX1], [y0, y0], c=WHITE, lw=0.8, alpha=.18, ls=(0, (4, 5)), zorder=3)
    T(ax, MX1 - 0.01, y0 + 0.02, "0°", 10, GREY, w="normal", ha="right")
    legs = [("Taiwan", "Luzon", False), ("Luzon", "Sulawesi", False), ("Sulawesi", "Bismarck", False),
            ("Bismarck", "Vanuatu", True), ("Vanuatu", "Fiji", True), ("Fiji", "Tonga", True),
            ("Fiji", "Samoa", True), ("Samoa", "Tahiti", True), ("Tahiti", "Hawaii", True)]
    for a, b, dashed in legs:
        pa, pb = mp(*P[a]), mp(*P[b])
        ax.annotate("", xy=pb, xytext=pa, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.0, alpha=.9,
                                    linestyle=(0, (4, 3)) if dashed else "-", shrinkA=8, shrinkB=8))
    lab = {"Taiwan": (0.03, 0.0, "left", AMBER, 16), "Luzon": (-0.03, 0.0, "right", WHITE, 13),
           "Sulawesi": (-0.03, 0.0, "right", WHITE, 13), "Bismarck": (0.0, 0.045, "center", WHITE, 13),
           "Vanuatu": (-0.03, -0.01, "right", WHITE, 13), "Fiji": (0.0, -0.045, "center", WHITE, 13),
           "Tonga": (0.0, -0.045, "center", AMBER, 15), "Samoa": (0.0, 0.045, "center", WHITE, 13),
           "Tahiti": (0.0, -0.045, "center", WHITE, 13), "Hawaii": (0.0, 0.045, "center", AMBER, 16)}
    if LANG != "zh":                                        # 英文字較長：菲律賓標在右邊，免得出框
        lab["Luzon"] = (0.03, 0.0, "left", WHITE, 13)
    for nm, (lat, lon) in P.items():
        x, y = mp(lat, lon)
        col = lab[nm][3]
        ax.scatter([x], [y], s=110 if col == AMBER else 60, c=col, zorder=7, lw=0)
        dx, dy, ha, c, fs = lab[nm]
        T(ax, x + dx, y + dy, tx(nm), fs, c, ha=ha, w="bold" if c == AMBER else "normal")
    T(ax, 0.0, MY0 - 0.0, "", 1)
    T(ax, 0.10, mp(8.0, 0)[1], tx("map_note"), 12, GREY, w="normal")


# ══════════════════════ C-X06-02 兩個三十二 ══════════════════════
RC = 0.34
PHI = 20.0
STARS = [("五車二", 46.0), ("織女", 38.78), ("昴宿", 24.12), ("大角", 19.18), ("牛郎", 8.87), ("心宿二", -26.43),
         ("老人星", -52.70)]


def rose(ax, cx, cy, col, cards):
    ax.add_patch(C.Circle((cx, cy), RC, fc="none", ec=WHITE, lw=2.0, alpha=.85, zorder=4))
    ax.add_patch(C.Circle((cx, cy), RC * 0.80, fc="none", ec=WHITE, lw=0.8, alpha=.35, zorder=4))
    for i in range(32):
        a = math.radians(i * 11.25)
        r0 = RC * (0.80 if i % 8 == 0 else 0.86)
        ax.plot([cx + r0 * math.sin(a), cx + RC * math.sin(a)], [cy + r0 * math.cos(a), cy + RC * math.cos(a)],
                c=col if i % 8 == 0 else WHITE, lw=1.6 if i % 8 == 0 else 0.8, alpha=.9 if i % 8 == 0 else .5,
                zorder=5)
    if cards:
        for k, az in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
            a = math.radians(az)
            T(ax, cx + RC * 0.62 * math.sin(a), cy + RC * 0.62 * math.cos(a), tx(k), 15, col)


def c02_haw(ax):
    cx, cy = -0.52, 0.10
    T(ax, cx, 0.74, tx("c02_haw"), 24, GREEN)
    T(ax, cx, 0.675, tx("c02_haw2"), 12, GREY, w="normal")
    rose(ax, cx, cy, GREEN, True)
    T(ax, cx, cy - RC - 0.07, "32 × 11.25°", 14, WHITE, w="normal")


def c02_ara(ax):
    cx, cy = 0.36, 0.10
    ly = 0.0
    T(ax, cx, 0.74, tx("c02_ara"), 24, PURPLE)
    T(ax, cx, 0.675, tx("c02_ara2"), 12, GREY, w="normal")
    rose(ax, cx, cy, PURPLE, False)
    # 正北北極星、正南南天極
    ax.scatter([cx], [cy + RC], s=170, c=PURPLE, zorder=8, marker="*")
    T(ax, cx, cy + RC + 0.075, tx("jah") + "  " + tx("jah2"), 14, PURPLE)
    ax.scatter([cx], [cy - RC], s=80, c=PURPLE, zorder=8)
    T(ax, cx, cy - RC - 0.05, tx("scp"), 13, PURPLE)
    for i, (nm, dec) in enumerate(STARS):
        az = math.degrees(math.acos(math.sin(math.radians(dec)) / math.cos(math.radians(PHI))))
        for side in (1, -1):
            a = math.radians(az) * side
            x, y = cx + RC * math.sin(a), cy + RC * math.cos(a)
            ax.scatter([x], [y], s=60 if side > 0 else 22, c=PURPLE, zorder=8, lw=0,
                       alpha=1 if side > 0 else .7)
        a = math.radians(az)
        dx_, dy_ = cx + RC * math.sin(a), cy + RC * math.cos(a)
        ly = dy_ if i == 0 else min(dy_, ly - 0.075)            # 標籤排成一欄，由上往下至少隔 0.075
        lx = cx + RC + 0.09
        ax.plot([dx_ + 0.012, lx - 0.012], [dy_, ly], c=PURPLE, lw=0.8, alpha=.6)
        T(ax, lx, ly, tx(nm), 12.5, WHITE, ha="left", w="normal")
    T(ax, 0.0, -0.46, tx("c02_mid"), 22, AMBER)
    T(ax, 0.0, -0.56, tx("c02_foot1"), 11.5, GREY, w="normal")
    T(ax, 0.0, -0.61, tx("c02_foot2"), 11.5, GREY, w="normal")


# ══════════════════════ C-X06-05 星路 ══════════════════════
TIK, ANU = (-12.296, 168.832), (-11.611, 169.850)
HZ = -0.30


def c05_sea(ax):
    km, brg = gc_km(TIK, ANU), bearing(TIK, ANU)
    T(ax, 0.0, 0.90, tx("c05_title"), 30, WHITE)
    T(ax, 0.0, 0.83, tx("c05_sub").format(km=km, brg=brg), 17, AMBER)
    ax.plot([-0.95, 0.95], [HZ, HZ], c=WHITE, lw=2.0, alpha=.75, zorder=4)
    C.water(ax, y=HZ - 0.06, x0=-0.95, x1=0.95, c=BLUE, rows=3, amp=0.012, freq=26)
    # 船頭（船身剪影，畫在浪的下方＝近景）
    by = HZ - 0.27
    ax.add_patch(C.Polygon([(-0.16, by), (0.16, by), (0.11, by - 0.06), (-0.11, by - 0.06)], closed=True,
                           fc="#2A3B66", ec=WHITE, lw=1.4, zorder=6))
    C.arrow(ax, (0.0, HZ - 0.02), (0.0, by + 0.01), c=AMBER, lw=2.4, alpha=.95, style="-|>")
    T(ax, 0.20, by - 0.03, tx("c05_bow"), 15, AMBER, ha="left")
    ax.scatter([0.0], [HZ], s=90, c=AMBER, marker="^", zorder=7)
    T(ax, 0.0, HZ - 0.035 - 0.0, "", 1)
    T(ax, -0.05, HZ + 0.035, tx("c05_dest"), 13, AMBER, ha="right", w="normal")


def c05_path(ax):
    # 星從右下往左上斜升（示意）；同一條升起路徑上一顆接一顆
    kk = (0.42 - (HZ + 0.05)) / 0.28                        # 三顆星排在同一條斜升的路徑上
    pts = [(0.28, 0.42, GREY, 130, "c05_s1"), (0.0, HZ + 0.05, AMBER, 260, "c05_s2"),
           (-0.07, HZ + 0.05 - 0.07 * kk, WHITE, 90, "c05_s3")]
    xs = [-0.20, 0.45]
    ax.plot([-0.10, 0.36], [HZ + 0.05 - 0.10 * kk, HZ + 0.05 + 0.36 * kk], c=WHITE, lw=1.0, alpha=.35, ls=(0, (3, 4)), zorder=3)
    for x, y, col, s, k in pts:
        below = y < HZ
        ax.scatter([x], [y], s=s, c="none" if below else col, edgecolors=col, lw=1.6, zorder=8)
        if k == "c05_s2":
            ax.scatter([x], [y], s=s * 3.2, c=col, alpha=.18, zorder=7, lw=0)
        if below:
            T(ax, x - 0.05, y, tx(k), 14, col, ha="right", w="normal")
        else:
            T(ax, x + 0.06, y, tx(k), 15, col, ha="left", w="bold" if col == AMBER else "normal")
    C.arrow(ax, (0.30, 0.25), (0.15, HZ + 0.05 + 0.08 * kk), c=GREY, lw=1.4, alpha=.7, style="-|>")
    bx, by, bw, bh = -0.90, -0.97, 1.80, 0.25
    ax.add_patch(C.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.4, zorder=9))
    T(ax, 0.0, by + bh - 0.055, tx("c05_box1"), 14, WHITE, z=13)
    T(ax, 0.0, by + bh - 0.125, tx("c05_box2"), 16, AMBER, z=13)
    T(ax, 0.0, by + 0.045, tx("c05_box3"), 11.5, GREY, w="normal", z=13)


# ══════════════════════ 9:16 圖卡 ══════════════════════
def c03_card(ax):
    ax.text(0.5, 0.945, tx("c03_title"), fontproperties=C.FP, fontsize=27, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, tx("c03_sub"), fontproperties=C.FP, fontsize=14, color=GREY, ha="center", va="center")
    y = 0.865
    for h, q, e, col in (("c03_h1", "c03_q1", "c03_e1", AMBER), ("c03_h2", "c03_q2", "c03_e2", GREEN),
                         ("c03_h3", "c03_q3", "c03_e3", PURPLE)):
        n = len(tx(e))
        hh = 0.135 + 0.034 * n
        ax.add_patch(C.FancyBboxPatch((0.05, y - hh), 0.90, hh - 0.012, boxstyle="round,pad=0.0,rounding_size=0.02",
                                      fc="#141B36", ec=col, lw=1.6, zorder=2))
        ax.text(0.09, y - 0.045, tx(h), fontproperties=C.FP, fontsize=26, color=col, ha="left", va="center",
                weight="bold", zorder=3)
        ax.text(0.09, y - 0.092, tx(q), fontproperties=C.FP, fontsize=14.5, color=WHITE, ha="left", va="center",
                weight="bold", zorder=3)
        for i, line in enumerate(tx(e)):
            ax.text(0.11, y - 0.135 - 0.034 * i, ("　" if line.startswith(("＝", "=")) else ("・" if LANG == "zh" else "• ")) + line, fontproperties=C.FP, fontsize=12, color=WHITE,
                    ha="left", va="center", alpha=.88, zorder=3)
        y -= hh + 0.014
    ax.text(0.5, 0.062, tx("c03_foot"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.032, tx("tags"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")


def c04_card(ax):
    ax.text(0.5, 0.945, tx("c04_title"), fontproperties=C.FP, fontsize=28, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, tx("c04_sub"), fontproperties=C.FP, fontsize=16, color=AMBER, ha="center", va="center")
    ax.text(0.5, 0.872, tx("c04_sun"), fontproperties=C.FP, fontsize=12.5, color=GREY, ha="center", va="center")
    y = 0.840
    for when, what, detail, col in tx("c04_rows"):
        hh = 0.165
        ax.add_patch(C.FancyBboxPatch((0.05, y - hh), 0.90, hh - 0.014, boxstyle="round,pad=0.0,rounding_size=0.02",
                                      fc="#141B36", ec=col, lw=1.5, zorder=2))
        ax.text(0.09, y - 0.035, when, fontproperties=C.FP, fontsize=13.5, color=col, ha="left", va="center",
                weight="bold", zorder=3)
        ax.text(0.09, y - 0.080, what, fontproperties=C.FP, fontsize=19, color=WHITE, ha="left", va="center",
                weight="bold", zorder=3)
        ax.text(0.09, y - 0.122, detail, fontproperties=C.FP, fontsize=11.5, color=WHITE, ha="left", va="center",
                alpha=.85, zorder=3)
        y -= hh + 0.008
    ax.text(0.5, 0.090, tx("c04_foot"), fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.040, tx("tags"), fontproperties=C.FP, fontsize=13, color=WHITE, ha="center", va="center")


def run():
    C.emit("", [("莎湖", c01_sahul), ("奧德賽", c01_odyssey), ("萍洲", c01_pz), ("前情", c01_prev),
                ("南島", c01_austronesian)], title="C-X06-01_時間軸",
           preview_layers=["前情", "南島"])
    C.emit("", [("夏威夷", c02_haw), ("阿拉伯", c02_ara)], title="C-X06-02_兩個三十二")
    C.emit("", [("海面", c05_sea), ("星路", c05_path)], title="C-X06-05_星路")
    for fn, name in ((c03_card, "C-X06-03_星星航海的三件事"), (c04_card, "C-X06-04_今晚自己導航")):
        f, ax = C.newcard(dark=True)
        fn(ax)
        C.save(f, "", f"{name}_圖卡.png", transparent=False)


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print(f"  Tikopia→阿努塔 {gc_km(TIK, ANU):.0f} km、方位 {bearing(TIK, ANU):.1f}°")
    run()


if __name__ == "__main__":
    main()
