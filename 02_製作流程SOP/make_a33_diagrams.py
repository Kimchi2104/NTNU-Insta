# -*- coding: utf-8 -*-
"""A-33 毛利 Matariki｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A33-01_Matariki假日       → 逐字稿 02 鏡（年份層→今年層）
  C-A33-02_怎麼挑日子         → 逐字稿 04 鏡（月曆層→放假層）
  C-A33-03_兩個季節           → 逐字稿 05 鏡（單層）
  C-A33-04_黎明重現           → 逐字稿 06 鏡（地平線層→三地層）
  C-A33-05_Matariki九星小辭典 → 逐字稿 10 鏡（9:16 圖卡，可存圖）
  C-A33-06_hautapu            → 逐字稿 11 鏡（爐火層→熱氣層→名字層；不畫人物、不仿既有插畫）
  C-A33-07_這週抬頭看         → 逐字稿 13 鏡（9:16 圖卡，可存圖）
  C-A33-08_北島示意           → 逐字稿 12 鏡（單層；海岸線為自繪示意，約 40 個經緯度點連成）
輸出：05_素材/A-33_毛利Matariki/_概念圖/（--lang en → 只出 EN33 用的 C-A33-01、02 到 _概念圖/en/）

來源：MBIE／employment.govt.nz（2022/6/24 第一次放假；「the first public holiday to recognise Te Ao Māori」）；
      Matariki Advisory Group 日期表、Te Papa（2027 Tangaroa 期 6/27–30、假日 6/25；九星的領域）；
      Rangi Mātāmua《Matariki: The Star of the Year》2017（九星、1933 手稿、hautapu）；Te Ara（Puanga 部族）；
      RNZ 2025（Puanga 是西岸的天氣星）。天象全部 PyEphem 4.2.1 自算（恆星 J2000、1010 hPa、20°C），
      與逐字稿「星空對時」逐條相同（main() 會重算一次並印出）。
"""
import os, sys, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from matplotlib.patches import Wedge
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-33_毛利Matariki/_概念圖")
C.set_base(OUT)
RED, GREY, DARK = "#FF6B6B", "#8C9AB8", "#1B2240"
LANG = "zh"
S = None

TXT = {
    "zh": {
        # 01
        "c01_title": "Matariki：紐西蘭的國定假日", "c01_sub": "Te Kāhui o Matariki Public Holiday Act 2022",
        "y2022": "2022/6/24（五）", "y2022b": "第一次放假", "y2026": "2026/7/10（五）", "y2027": "2027/6/25（五）",
        "quote_en": "“the first public holiday to recognise Te Ao Māori”",
        "quote_zh": "第一個承認毛利世界觀的國定假日",
        "quote_src": "紐西蘭政府 employment.govt.nz",
        "this_year": "今年：6 月 25 日（五）", "every_year": "每年日期都不一樣——由天上決定",
        # 02
        "c02_title": "怎麼挑日子：Pipiri 月（2027）", "c02_sub": "紐西蘭時間；月相 PyEphem 自算，Tangaroa 期據 Te Papa",
        "wk": ["日", "一", "二", "三", "四", "五", "六"],
        "new": "新月", "full": "滿月", "lq": "下弦", "tangaroa": "Tangaroa 期 6/27–30",
        "holiday": "假日", "rule1": "規則：Pipiri 月裡，離 Tangaroa 期最近的星期五",
        "rule2": "6/27 是星期日 → 6/25（五）放假",
        # 03
        "c03_title": "同一天，兩個季節", "c03_sub": "2027/6/21 的白天（日出到日落，各地當地時間）",
        "tpe": "台北 25°N", "wlg": "威靈頓 41°S", "summer": "北半球：快到夏至", "winter": "南半球：冬至（紐西蘭 6/22）",
        "hrs": "{:.1f} 小時", "rise": "日出 {}", "set": "日落 {}",
        # 04
        "c04_title": "黎明重現：昴宿第一次露臉", "c04_sub": "太陽在地平下 12° 那一刻（天快亮），昴宿六高 3° 以上的第一天",
        "east": "東", "ene": "東北東", "ne": "東北",
        "city_tpe": "台北", "city_akl": "奧克蘭", "city_wlg": "威靈頓",
        "first": "{}　{}", "alt": "高 {:.1f}°・方位 {:.0f}°",
        "easy": "高度 10° 以上才好找：台北 6/16、奧克蘭 6/22、威靈頓 6/25",
        # 05
        "c05_title": "Matariki 九星小辭典", "c05_sub": "名字與領域：Rangi Mātāmua 2017；Te Papa",
        "c05_cols": ["毛利名", "照看的領域", "西方星名", "星等"],
        "c05_note1": "最暗的兩顆：Hiwa-i-te-rangi、Pōhutukawa——要在很黑的地方才看得到",
        "c05_note2": "很多較早的說法只數七顆；九顆星據 1933 年完成的家族手稿",
        "c05_note3": "西方星名對應照 Stellarium／Wikipedia；網路上也有對調的版本",
        # 06
        "c06_title": "hautapu：天亮前獻給星群", "umu": "地爐（umu）煮食物",
        "steam": "熱氣升上天，獻給 Matariki", "name1": "念出過去一年離開的人", "name1b": "→ Pōhutukawa",
        "name2": "說出新年的願望", "name2b": "→ Hiwa-i-te-rangi",
        "like": "有點像我們過年：送走舊的一年、想念親人、許下新願", "c06_src": "據 Mātāmua 2017；示意圖，不畫人物",
        # 07
        "c07_title": "這週抬頭看", "c07_sub": "台北；6/25（五）晚上 → 6/26（六）清晨",
        "tonight": "今晚 20:00", "tonight1": "心宿二 Rehua：南偏東、高約 30°",
        "tonight2": "天黑到半夜兩點都看得到", "tonight3": "昴宿、參宿七下午就西沉了，今晚看不到",
        "dawn": "明晨 03:30–04:00", "dawn1": "昴宿 Matariki：東北東低空，高 10°→17°",
        "dawn2": "04:10 天色變亮前最好找", "dawn3": "月亮在南偏東高處（64%），離昴宿很遠，不擋",
        "dawn4": "最暗的兩顆（5.5、5.8 等）要到光害少的地方",
        "nz": "同一天早上 06:40，威靈頓也在東北方看見它——一起迎新年",
        "c07_src": "PyEphem 自算；台北 25.03°N、121.57°E",
        "south": "南", "se": "東南", "ene_s": "東北東", "e_s": "東",
        # 08
        "c08_title": "北島西岸看 Puanga", "c08_sub": "自繪示意；只標本集提到的地方",
        "taranaki": "Taranaki", "whanganui": "Whanganui", "rangitikei": "Rangitīkei",
        "wellington": "威靈頓", "auckland": "奧克蘭", "west": "新年看 Puanga（參宿七）", "west2": "Te Ara、RNZ",
        "puaka": "南島 Kāi Tahu 叫它 Puaka", "why1": "有的地方被山擋住，\n看不清 Matariki",
        "why2": "Puanga 也是\n西岸的天氣星", "north": "北",
        "foot": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Matariki: a New Zealand public holiday", "c01_sub": "Te Kāhui o Matariki Public Holiday Act 2022",
        "y2022": "Fri 24 Jun 2022", "y2022b": "first holiday", "y2026": "Fri 10 Jul 2026", "y2027": "Fri 25 Jun 2027",
        "quote_en": "“the first public holiday to recognise Te Ao Māori”",
        "quote_zh": "(the Māori world view)", "quote_src": "NZ Government, employment.govt.nz",
        "this_year": "This year: Friday 25 June", "every_year": "A different date every year — set by the sky",
        "c02_title": "Picking the day: Pipiri 2027", "c02_sub": "NZ time; moon phases by PyEphem, Tangaroa period per Te Papa",
        "wk": ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
        "new": "new", "full": "full", "lq": "last qtr", "tangaroa": "Tangaroa 27–30 Jun",
        "holiday": "holiday", "rule1": "Official rule: the Friday closest to Tangaroa in Pipiri",
        "rule2": "27 Jun is a Sunday → holiday on Fri 25 Jun",
        "c03_title": "Same day, two seasons", "c03_sub": "Daylight on 21 June 2027 (local times)",
        "tpe": "Taipei 25°N", "wlg": "Wellington 41°S", "summer": "North: almost midsummer",
        "winter": "South: winter solstice (22 Jun in NZ)",
        "hrs": "{:.1f} h", "rise": "rise {}", "set": "set {}",
        "c04_title": "Dawn return of the Pleiades", "c04_sub": "First day Alcyone stands ≥3° high when the Sun is 12° below the horizon",
        "east": "E", "ene": "ENE", "ne": "NE",
        "city_tpe": "Taipei", "city_akl": "Auckland", "city_wlg": "Wellington",
        "first": "{}  {}", "alt": "alt {:.1f}° · az {:.0f}°",
        "easy": "Easy to spot (≥10°): Taipei 16 Jun, Auckland 22 Jun, Wellington 25 Jun",
        "c05_title": "The nine stars of Matariki", "c05_sub": "Names and domains: Rangi Mātāmua 2017; Te Papa",
        "c05_cols": ["Māori name", "Domain", "Western name", "mag"],
        "c05_note1": "Faintest two: Hiwa-i-te-rangi and Pōhutukawa — you need a dark sky",
        "c05_note2": "Many older accounts list seven; the nine come from a family manuscript finished in 1933",
        "c05_note3": "Western names per Stellarium/Wikipedia; some posters swap pairs",
        "c06_title": "Hautapu: an offering before dawn", "umu": "food cooked in an earth oven (umu)",
        "steam": "steam rises to feed Matariki", "name1": "the names of those who died this year", "name1b": "→ Pōhutukawa",
        "name2": "wishes for the new year", "name2b": "→ Hiwa-i-te-rangi",
        "like": "Like Lunar New Year: farewell the old year, remember family, make a wish",
        "c06_src": "After Mātāmua 2017; schematic, no figures",
        "c07_title": "Look up this week", "c07_sub": "Taipei; Fri 25 Jun evening → Sat 26 Jun dawn",
        "tonight": "Tonight 20:00", "tonight1": "Antares (Rehua): SSE, about 30° up",
        "tonight2": "visible from dark until 2 a.m.", "tonight3": "the Pleiades and Rigel set in the afternoon",
        "dawn": "Tomorrow 03:30–04:00", "dawn1": "Pleiades (Matariki): low in the ENE, 10°→17°",
        "dawn2": "best before the sky brightens at 04:10", "dawn3": "the Moon (64%) is high in the SSE, far away",
        "dawn4": "the two faintest (mag 5.5, 5.8) need a dark site",
        "nz": "Same morning, 06:40 in Wellington: Matariki in the NE — a shared new year",
        "c07_src": "PyEphem; Taipei 25.03°N, 121.57°E",
        "south": "S", "se": "SE", "ene_s": "ENE", "e_s": "E",
        "c08_title": "The west coast follows Puanga", "c08_sub": "Schematic; only places named in the episode",
        "taranaki": "Taranaki", "whanganui": "Whanganui", "rangitikei": "Rangitīkei",
        "wellington": "Wellington", "auckland": "Auckland", "west": "New year by Puanga (Rigel)", "west2": "Te Ara; RNZ",
        "puaka": "South Island Kāi Tahu: Puaka", "why1": "hills hide Matariki\nin some places",
        "why2": "Puanga is also the\nwest-coast weather star", "north": "N",
        "foot": "#WorldSkyCultures  #NTNUAstronomy",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ 天象（自算） ══════════════════════
def _star(h):
    import ephem
    b = ephem.FixedBody(); b._ra = math.radians(S[h][0]); b._dec = math.radians(S[h][1]); b._epoch = ephem.J2000
    return b


def _obs(lat, lon, tz, when):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.pressure, o.temp = 1010, 20
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    return o


CITY = {"tpe": (25.033, 121.565, 8), "akl": (-36.85, 174.76, 12), "wlg": (-41.29, 174.78, 12)}


def heliacal(key):
    """太陽 −12° 時昴宿六 ≥3° 的第一天：(日, 當地時刻, 高度, 方位)；≥10° 的第一天"""
    import ephem
    la, lo, tz = CITY[key]
    first = ten = None
    for d in range(1, 31):
        o = _obs(la, lo, tz, f"2027/6/{d} 00:00"); o.horizon = "-12"
        t = o.next_rising(ephem.Sun(), use_center=True); o.date = t; o.horizon = "0"
        b = _star(17702); b.compute(o)
        alt, az = math.degrees(b.alt), math.degrees(b.az)
        lt = str(ephem.Date(t + tz * ephem.hour))[-8:-3]
        if first is None and alt >= 3:
            first = (d, lt, alt, az)
        if ten is None and alt >= 10:
            ten = d
    return first, ten


def daylight(key):
    import ephem
    la, lo, tz = CITY[key]
    o = _obs(la, lo, tz, "2027/6/21 00:00"); s = ephem.Sun()
    r, st = o.next_rising(s), o.next_setting(s)
    f = lambda t: str(ephem.Date(t + tz * ephem.hour))[-8:-3]
    return f(r), f(st), (st - r) * 24


# ══════════════════════ C-A33-01 假日 ══════════════════════
def c01_years(ax):
    T(ax, 0.0, 0.80, tx("c01_title"), 34, WHITE)
    T(ax, 0.0, 0.70, tx("c01_sub"), 19, GREY, w="normal")
    ax.plot([-0.82, 0.82], [0.30, 0.30], c=WHITE, lw=2.4, alpha=.55)
    for x, a, b, col in ((-0.62, tx("y2022"), tx("y2022b"), GREEN), (0.0, tx("y2026"), "", GREY)):
        ax.scatter([x], [0.30], s=420, c=col, zorder=5, lw=0)
        T(ax, x, 0.44, a, 24, col)
        if b:
            T(ax, x, 0.17, b, 22, WHITE, w="normal")
    T(ax, 0.0, -0.06, tx("quote_en"), 21, MW, w="normal")
    T(ax, 0.0, -0.18, tx("quote_zh"), 27, AMBER)
    T(ax, 0.0, -0.28, tx("quote_src"), 17, GREY, w="normal")


def c01_this(ax):
    x = 0.62
    ax.scatter([x], [0.30], s=900, c=AMBER, zorder=6, lw=0)
    ax.scatter([x], [0.30], s=2600, c=AMBER, zorder=5, lw=0, alpha=.25)
    T(ax, x, 0.44, tx("y2027"), 24, AMBER)
    ax.add_patch(C.FancyBboxPatch((-0.66, -0.68), 1.32, 0.26, boxstyle="round,pad=0.0,rounding_size=0.05",
                                  fc=DARK, ec=AMBER, lw=2.4, zorder=3))
    T(ax, 0.0, -0.55, tx("this_year"), 36, AMBER)
    T(ax, 0.0, -0.80, tx("every_year"), 24, WHITE, w="normal")


# ══════════════════════ C-A33-02 怎麼挑日子 ══════════════════════
D0 = datetime.date(2027, 5, 30)                   # 週日開頭
CX0, CW, CY0, CH = -0.84, 0.24, 0.62, 0.215


def cell(d):
    i = (d - D0).days
    return CX0 + (i % 7) * CW, CY0 - (i // 7) * CH


def c02_cal(ax):
    T(ax, 0.0, 0.86, tx("c02_title"), 32, WHITE)
    T(ax, 0.0, 0.775, tx("c02_sub"), 17, GREY, w="normal")
    for i, w in enumerate(tx("wk")):
        T(ax, CX0 + i * CW + CW / 2, 0.68, w, 20, AMBER if i == 5 else GREY)
    tang = [datetime.date(2027, 6, d) for d in range(27, 31)]
    for k in range(35):
        d = D0 + datetime.timedelta(days=k)
        x, y = cell(d)
        inside = d.month == 6 or (d.month == 7 and d.day <= 3)
        fc = "#244C8A" if d in tang else DARK
        ax.add_patch(C.FancyBboxPatch((x + 0.008, y - CH + 0.012), CW - 0.016, CH - 0.024,
                                      boxstyle="round,pad=0.0,rounding_size=0.02", fc=fc,
                                      ec=BLUE if d in tang else "#2E3A60", lw=1.4, alpha=1.0 if inside else .45, zorder=2))
        T(ax, x + 0.035, y - 0.045, f"{d.month}/{d.day}" if d.day == 1 or k == 0 else str(d.day), 17,
          WHITE if inside else GREY, ha="left", w="normal", z=4)
    for (m, dd, key, kind) in ((6, 5, "new", 0), (6, 19, "full", 1), (6, 27, "lq", 2)):
        x, y = cell(datetime.date(2027, m, dd))
        mx, my, r = x + CW / 2, y - CH * 0.47, 0.034
        if kind == 0:
            ax.add_patch(C.Circle((mx, my), r, fc="#0B0F1E", ec=MW, lw=1.6, zorder=5))
        elif kind == 1:
            ax.add_patch(C.Circle((mx, my), r, fc=MW, ec=MW, lw=1.6, zorder=5))
        else:                                    # 下弦：左半亮（南半球看是右半亮；這裡只當記號）
            ax.add_patch(C.Circle((mx, my), r, fc="#0B0F1E", ec=MW, lw=1.6, zorder=5))
            ax.add_patch(Wedge((mx, my), r, 90, 270, fc=MW, ec="none", zorder=6))
        T(ax, mx, y - CH + 0.036, tx(key), 15, MW, w="normal", z=6)
    x0, y0 = cell(tang[0]); x1, _ = cell(tang[-1])
    T(ax, (x0 + x1 + CW) / 2, y0 - CH - 0.045, tx("tangaroa"), 20, BLUE)


def c02_holiday(ax):
    x, y = cell(datetime.date(2027, 6, 25))
    ax.add_patch(C.FancyBboxPatch((x + 0.002, y - CH + 0.006), CW - 0.004, CH - 0.012,
                                  boxstyle="round,pad=0.0,rounding_size=0.025", fc=AMBER, ec=AMBER, lw=3.0,
                                  alpha=.30, zorder=7))
    ax.add_patch(C.FancyBboxPatch((x + 0.002, y - CH + 0.006), CW - 0.004, CH - 0.012,
                                  boxstyle="round,pad=0.0,rounding_size=0.025", fc="none", ec=AMBER, lw=4.0, zorder=8))
    T(ax, x + CW / 2, y - CH * 0.62, tx("holiday"), 22, AMBER, z=9)
    T(ax, 0.0, -0.66, tx("rule1"), 21, WHITE, w="normal")
    T(ax, 0.0, -0.77, tx("rule2"), 24, AMBER)


# ══════════════════════ C-A33-03 兩個季節 ══════════════════════
def c03(ax):
    T(ax, 0.0, 0.70, tx("c03_title"), 34, WHITE)
    T(ax, 0.0, 0.60, tx("c03_sub"), 19, GREY, w="normal")
    X0, X1 = -0.80, 0.80
    hx = lambda h: X0 + (X1 - X0) * h / 24.0
    for i, (key, lab, cap, col) in enumerate((("tpe", "tpe", "summer", AMBER), ("wlg", "wlg", "winter", BLUE))):
        r, s, hrs = daylight(key)
        y = 0.25 - i * 0.55
        T(ax, X0, y + 0.15, tx(lab), 26, col, ha="left")
        T(ax, X1, y + 0.15, tx(cap), 19, WHITE, ha="right", w="normal")
        ax.add_patch(C.Rectangle((X0, y - 0.06), X1 - X0, 0.12, fc="#141B33", ec="#2E3A60", lw=1.2, zorder=2))
        a, b = [int(t[:2]) + int(t[3:]) / 60 for t in (r, s)]
        ax.add_patch(C.Rectangle((hx(a), y - 0.06), hx(b) - hx(a), 0.12, fc=col, ec="none", alpha=.85, zorder=3))
        T(ax, (hx(a) + hx(b)) / 2, y, tx("hrs").format(hrs), 24, "#0B0F1E", z=5)
        T(ax, hx(a), y - 0.12, tx("rise").format(r), 17, WHITE, w="normal")
        T(ax, hx(b), y - 0.12, tx("set").format(s), 17, WHITE, w="normal")
    for h in (0, 6, 12, 18, 24):
        ax.plot([hx(h), hx(h)], [-0.50, -0.47], c=GREY, lw=1.2)
        T(ax, hx(h), -0.55, f"{h:02d}:00", 15, GREY, w="normal")


# ══════════════════════ C-A33-04 黎明重現 ══════════════════════
PAN = [("tpe", "city_tpe", AMBER), ("akl", "city_akl", BLUE), ("wlg", "city_wlg", BLUE)]
AZ0, AZ1, ALT1 = 35.0, 100.0, 12.0
PW_, PH_ = 0.54, 0.62


def pan_xy(i, az, alt):
    x0 = -0.84 + i * 0.58
    return x0 + (az - AZ0) / (AZ1 - AZ0) * PW_, -0.30 + alt / ALT1 * PH_


def c04_horizon(ax):
    T(ax, 0.0, 0.80, tx("c04_title"), 32, WHITE)
    T(ax, 0.0, 0.71, tx("c04_sub"), 16, GREY, w="normal")
    for i, (key, nm, col) in enumerate(PAN):
        x0 = -0.84 + i * 0.58
        ax.add_patch(C.Rectangle((x0, -0.30), PW_, PH_, fc="#16244A", ec="none", alpha=.55, zorder=1))
        ax.add_patch(C.Rectangle((x0, -0.30), PW_, PH_ * 0.35, fc="#3A4E7E", ec="none", alpha=.35, zorder=1))
        ax.add_patch(C.Rectangle((x0, -0.42), PW_, 0.12, fc="#05070F", ec="none", zorder=2))
        ax.plot([x0, x0 + PW_], [-0.30, -0.30], c=WHITE, lw=1.4, alpha=.7, zorder=3)
        for az, k in ((45, "ne"), (67.5, "ene"), (90, "east")):
            x, _ = pan_xy(i, az, 0)
            ax.plot([x, x], [-0.30, -0.33], c=WHITE, lw=1.2, alpha=.6, zorder=4)
            T(ax, x, -0.37, tx(k), 14, GREY, w="normal")
        T(ax, x0 + PW_ / 2, 0.42, tx(nm), 26, col)
        _, y10 = pan_xy(i, AZ0, 10.0)
        ax.plot([x0, x0 + PW_], [y10, y10], c=WHITE, lw=1.0, alpha=.35, ls=(0, (4, 4)), zorder=3)
        T(ax, x0 + PW_ - 0.01, y10 + 0.025, "10°", 13, GREY, ha="right", w="normal")


def c04_cities(ax):
    for i, (key, nm, col) in enumerate(PAN):
        (d, lt, alt, az), ten = heliacal(key)
        x, y = pan_xy(i, az, alt)
        for dx, dy in ((0, 0), (-0.012, 0.010), (0.012, 0.012), (0.004, -0.010), (-0.006, 0.020), (0.016, -0.004)):
            ax.scatter([x + dx], [y + dy], s=26, c=WHITE, lw=0, zorder=6)
        ax.scatter([x], [y], s=900, c=WHITE, alpha=.12, lw=0, zorder=5)
        x0 = -0.84 + i * 0.58
        T(ax, x0 + PW_ / 2, 0.24, tx("first").format(f"6/{d}", lt), 22, WHITE)
        T(ax, x0 + PW_ / 2, 0.16, tx("alt").format(alt, az), 15, GREY, w="normal")
    T(ax, 0.0, -0.58, tx("easy"), 19, WHITE, w="normal")


# ══════════════════════ C-A33-05 九星小辭典（9:16 圖卡）══════════════════════
NINE = [(17702, "Matariki", "母親・健康", "Alcyone", AMBER), (17851, "Tupuānuku", "土裡長的食物", "Pleione", GREEN),
        (17847, "Tupuārangi", "樹上的果實和鳥", "Atlas", GREEN), (17573, "Waitī", "淡水與河裡的食物", "Maia", BLUE),
        (17531, "Waitā", "大海與海裡的食物", "Taygeta", BLUE), (17499, "Waipuna-ā-rangi", "雨", "Electra", BLUE),
        (17608, "Ururangi", "風", "Merope", WHITE), (17489, "Hiwa-i-te-rangi", "新年的願望", "Celaeno", PURPLE),
        (17579, "Pōhutukawa", "過去一年離開的人", "Asterope", PURPLE)]
DOM_EN = {17702: "mother · health", 17851: "food in the ground", 17847: "fruit and birds",
          17573: "fresh water", 17531: "the ocean", 17499: "rain", 17608: "wind",
          17489: "wishes for the year", 17579: "those who died this year"}


def c05_card(ax):
    T(ax, 0.5, 0.955, tx("c05_title"), 23, WHITE)
    T(ax, 0.5, 0.925, tx("c05_sub"), 11.5, GREY, w="normal")
    # 小星圖：真實位置（東在左），星點照星等
    cx, cy, sc = 0.5, 0.79, 0.40
    ra0, de0 = 56.75, 24.25
    for i, (h, nm, dom, west, col) in enumerate(NINE):
        ra, dec, v = S[h]
        x = cx - (ra - ra0) * math.cos(math.radians(de0)) * sc
        y = cy + (dec - de0) * sc * (6.075 / 10.8)          # 圖卡 x、y 軸都是 0–1，但寬高比 9:16
        r = max(0.6, (6.5 - v)) ** 1.6 * 9
        ax.scatter([x], [y], s=r * 3.0, c=WHITE, alpha=.15, lw=0, zorder=2)
        ax.scatter([x], [y], s=r, c=WHITE, lw=0, zorder=3)
        T(ax, x + 0.022, y + 0.012, str(i + 1), 10, col, ha="left", z=4)
    y = 0.665
    cols = [0.06, 0.40, 0.70, 0.93]
    for x, c in zip(cols, tx("c05_cols")):
        T(ax, x, y, c, 11.5, GREY, ha="left" if x < 0.9 else "center")
    ax.plot([0.04, 0.96], [y - 0.017, y - 0.017], c=WHITE, lw=0.8, alpha=.35)
    for i, (h, nm, dom, west, col) in enumerate(NINE):
        yy = y - 0.053 - i * 0.056
        dim = h in (17489, 17579)
        if dim:
            ax.add_patch(C.FancyBboxPatch((0.035, yy - 0.024), 0.93, 0.048, boxstyle="round,pad=0.0,rounding_size=0.01",
                                          fc="#2A2350", ec="none", zorder=1))
        T(ax, 0.025, yy, str(i + 1), 11, col, ha="left")
        T(ax, 0.06, yy, nm, 13.5, col, ha="left")
        T(ax, 0.40, yy, dom if LANG == "zh" else DOM_EN[h], 12.5, WHITE, ha="left", w="normal")
        T(ax, 0.70, yy, west, 12, MW, ha="left", w="normal")
        T(ax, 0.93, yy, f"{S[h][2]:.1f}", 12.5, AMBER if dim else WHITE, w="bold" if dim else "normal")
    T(ax, 0.5, 0.115, tx("c05_note1"), 11.5, PURPLE)
    T(ax, 0.5, 0.088, tx("c05_note2"), 10.5, WHITE, w="normal")
    T(ax, 0.5, 0.064, tx("c05_note3"), 10, GREY, w="normal")
    T(ax, 0.5, 0.030, tx("foot"), 12.5, WHITE)


# ══════════════════════ C-A33-06 hautapu ══════════════════════
def TB(ax, x, y, s, size, c, ha="center", w="bold"):
    """有深色底框的文字（壓在熱氣線上也讀得到）"""
    ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=c, ha=ha, va="center", weight=w, zorder=12,
            bbox=dict(boxstyle="round,pad=0.35,rounding_size=0.6", fc="#0B0F1E", ec="none", alpha=.88))


def c06_fire(ax):
    T(ax, 0.0, 0.88, tx("c06_title"), 32, WHITE)
    ax.add_patch(C.Ellipse((0.0, -0.62), 1.10, 0.20, fc="#2B2118", ec="none", zorder=2))
    ax.add_patch(C.Ellipse((0.0, -0.58), 0.70, 0.16, fc="#3A2A1C", ec="none", zorder=3))
    import random
    rd = random.Random(3)
    for _ in range(14):
        x = rd.uniform(-0.28, 0.28)
        ax.add_patch(C.Ellipse((x, -0.55 + rd.uniform(-0.02, 0.03)), 0.09, 0.05, fc="#6B5A4A", ec="none", zorder=4))
    for k, a in ((0.36, .18), (0.24, .30), (0.13, .50)):
        ax.add_patch(C.Ellipse((0.0, -0.52), k * 2, k * 0.55, fc=AMBER, ec="none", alpha=a * .6, zorder=3))
    T(ax, 0.0, -0.80, tx("umu"), 22, AMBER, w="normal")


def c06_steam(ax):
    for j, x0 in enumerate((-0.16, -0.05, 0.06, 0.17)):
        ys = [-0.45 + 0.012 * i for i in range(90)]
        xs = [x0 * (1 - (y + 0.45) / 1.6) + 0.035 * math.sin((y + j) * 9) for y in ys]
        ax.plot(xs, ys, c=MW, lw=3.0 - 0.3 * j, alpha=.55, zorder=3)
    for dx, dy, s in ((0, 0, 120), (-0.05, 0.02, 60), (0.04, 0.03, 70), (0.06, -0.01, 50), (-0.02, 0.05, 45),
                      (0.02, -0.03, 40), (-0.07, -0.01, 30), (0.09, 0.03, 25), (-0.04, 0.07, 22)):
        ax.scatter([dx], [0.66 + dy], s=s * 1.6, c=WHITE, lw=0, zorder=5)
        ax.scatter([dx], [0.66 + dy], s=s * 7, c=WHITE, alpha=.10, lw=0, zorder=4)
    TB(ax, 0.0, 0.50, tx("steam"), 22, WHITE, w="normal")


def c06_names(ax):
    for y, a, b, col in ((0.22, "name1", "name1b", PURPLE), (-0.02, "name2", "name2b", PURPLE)):
        TB(ax, -0.36, y, tx(a), 22, WHITE, w="normal", ha="right")
        TB(ax, -0.30, y, tx(b), 24, col, ha="left")
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.36), 1.76, 0.16, boxstyle="round,pad=0.0,rounding_size=0.04",
                                  fc=DARK, ec=AMBER, lw=1.6, zorder=10))
    T(ax, 0.0, -0.28, tx("like"), 21, AMBER)
    T(ax, 0.0, -0.94, tx("c06_src"), 15, GREY, w="normal")


# ══════════════════════ C-A33-07 這週抬頭看（9:16）══════════════════════
def mini_sky(ax, y0, pts, ticks):
    """小地平圖：pts＝[(方位, 高度, 名字, 色, 大小)]；橫軸方位、縱軸高度（0–40°）"""
    x0, x1, h = 0.08, 0.92, 0.16
    lo, hi = ticks[0][0], ticks[-1][0]
    fx = lambda az: x0 + (az - lo) / (hi - lo) * (x1 - x0)
    fy = lambda alt: y0 + alt / 40.0 * h
    ax.add_patch(C.Rectangle((x0, y0), x1 - x0, h, fc="#16244A", ec="none", alpha=.6, zorder=1))
    ax.add_patch(C.Rectangle((x0, y0 - 0.025), x1 - x0, 0.025, fc="#05070F", ec="none", zorder=2))
    ax.plot([x0, x1], [y0, y0], c=WHITE, lw=1.0, alpha=.7, zorder=3)
    for az, k in ticks:
        T(ax, fx(az), y0 - 0.013, tx(k), 10, GREY, w="normal")
    for az, alt, nm, col, s in pts:
        ax.scatter([fx(az)], [fy(alt)], s=s, c=col, lw=0, zorder=5)
        ax.scatter([fx(az)], [fy(alt)], s=s * 5, c=col, alpha=.18, lw=0, zorder=4)
        T(ax, fx(az), fy(alt) + 0.022, nm, 11, col)


def c07_card(ax):
    import ephem
    T(ax, 0.5, 0.955, tx("c07_title"), 24, WHITE)
    T(ax, 0.5, 0.925, tx("c07_sub"), 11.5, GREY, w="normal")
    o = _obs(25.033, 121.565, 8, "2027/6/25 20:00"); a = _star(80763); a.compute(o)
    T(ax, 0.08, 0.875, tx("tonight"), 17, RED, ha="left")
    mini_sky(ax, 0.70, [(math.degrees(a.az), math.degrees(a.alt), "Rehua", RED, 60)],
             [(90, "e_s"), (135, "se"), (180, "south")])
    for k, (key, col) in enumerate((("tonight1", WHITE), ("tonight2", WHITE), ("tonight3", GREY))):
        T(ax, 0.08, 0.645 - k * 0.032, tx(key), 12.5, col, ha="left", w="normal")
    pts = []
    for t in ("2027/6/26 03:30", "2027/6/26 04:00"):
        o = _obs(25.033, 121.565, 8, t); b = _star(17702); b.compute(o)
        pts.append((math.degrees(b.az), math.degrees(b.alt), t[-5:], AMBER, 40))
    ax.plot([0.04, 0.96], [0.535, 0.535], c=WHITE, lw=0.8, alpha=.3)
    T(ax, 0.08, 0.505, tx("dawn"), 17, AMBER, ha="left")
    mini_sky(ax, 0.32, pts, [(45, "ne"), (67.5, "ene_s"), (90, "e_s")])
    for k, (key, col) in enumerate((("dawn1", WHITE), ("dawn2", WHITE), ("dawn3", GREY), ("dawn4", GREY))):
        T(ax, 0.08, 0.265 - k * 0.032, tx(key), 12.5, col, ha="left", w="normal")
    ax.add_patch(C.FancyBboxPatch((0.05, 0.085), 0.90, 0.05, boxstyle="round,pad=0.0,rounding_size=0.012",
                                  fc=DARK, ec=BLUE, lw=1.2, zorder=1))
    T(ax, 0.5, 0.11, tx("nz"), 11.5, BLUE)
    T(ax, 0.5, 0.058, tx("c07_src"), 10, GREY, w="normal")
    T(ax, 0.5, 0.030, tx("foot"), 12.5, WHITE)


# ══════════════════════ C-A33-08 北島示意 ══════════════════════
COAST = [(-34.43, 172.68), (-34.40, 173.00), (-34.95, 173.60), (-35.20, 174.20), (-35.85, 174.55), (-36.30, 174.80),
         (-36.60, 174.80), (-36.50, 175.50), (-36.90, 175.90), (-37.40, 175.95), (-37.65, 176.17), (-37.95, 177.00),
         (-38.00, 177.30), (-37.69, 178.55), (-38.20, 178.35), (-38.67, 178.02), (-39.08, 177.90), (-39.49, 176.92),
         (-39.64, 177.09), (-40.30, 176.65), (-40.90, 176.23), (-41.61, 175.29), (-41.35, 174.80), (-40.98, 174.95),
         (-40.47, 175.22), (-39.95, 174.98), (-39.76, 174.47), (-39.28, 173.75), (-39.05, 174.07), (-38.70, 174.60),
         (-38.07, 174.80), (-37.80, 174.85), (-37.39, 174.71), (-37.05, 174.55), (-36.83, 174.42), (-36.40, 174.15),
         (-35.90, 173.75), (-35.53, 173.37), (-35.17, 173.15), (-34.70, 172.90), (-34.43, 172.68)]
LAT0, LON0, KM = -38.3, 175.4, 0.205


def nz(lat, lon):
    return (lon - LON0) * math.cos(math.radians(38.3)) * KM, (lat - LAT0) * KM


def c08(ax):
    T(ax, 0.0, 0.90, tx("c08_title"), 32, WHITE)
    T(ax, 0.0, 0.82, tx("c08_sub"), 16, GREY, w="normal")
    xy = [nz(*p) for p in COAST]
    ax.add_patch(C.Polygon(xy, closed=True, fc="#1E2B4D", ec=MW, lw=1.8, alpha=.95, zorder=2))
    ax.add_patch(C.Ellipse(nz(-39.7, 174.75), 0.36, 0.62, angle=-28, fc=AMBER, ec=AMBER, lw=2.0,
                           alpha=.22, zorder=3))
    ax.add_patch(C.Ellipse(nz(-39.7, 174.75), 0.36, 0.62, angle=-28, fc="none", ec=AMBER, lw=2.2,
                           ls=(0, (5, 4)), zorder=4))
    tm = nz(-39.30, 174.06)
    ax.add_patch(C.Polygon([(tm[0] - 0.035, tm[1] - 0.02), (tm[0], tm[1] + 0.04), (tm[0] + 0.035, tm[1] - 0.02)],
                           closed=True, fc=WHITE, ec="none", alpha=.8, zorder=5))
    for (lat, lon), key, dx, col in (((-39.06, 174.08), "taranaki", -0.05, AMBER), ((-39.93, 175.05), "whanganui", -0.09, AMBER),
                                     ((-40.15, 175.45), "rangitikei", 0.05, AMBER), ((-41.29, 174.78), "wellington", 0.05, WHITE),
                                     ((-36.85, 174.76), "auckland", -0.05, WHITE)):
        x, y = nz(lat, lon)
        ax.scatter([x], [y], s=70, c=col, zorder=6, lw=0)
        T(ax, x + dx, y, tx(key), 20, col, ha="right" if dx < 0 else "left")
    T(ax, -0.95, -0.52, tx("west"), 22, AMBER, ha="left")
    T(ax, -0.95, -0.60, tx("west2"), 15, GREY, ha="left", w="normal")
    ax.text(0.44, 0.62, tx("why1"), fontproperties=C.FP, fontsize=19, color=WHITE, ha="left", va="center",
            linespacing=1.4, zorder=12)
    ax.text(0.44, 0.40, tx("why2"), fontproperties=C.FP, fontsize=19, color=WHITE, ha="left", va="center",
            linespacing=1.4, zorder=12)
    T(ax, 0.95, -0.92, tx("puaka"), 17, GREY, ha="right", w="normal")
    C.arrow(ax, (0.85, 0.72), (0.85, 0.58), c=WHITE, lw=1.6, style="-|>")
    T(ax, 0.85, 0.77, tx("north"), 16, WHITE)


def main():
    global S, LANG
    S = dict(G.load_stars(BASE))
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── 天象重算 ──")
    for k in CITY:
        print(f"  {k} 黎明重現 {heliacal(k)}；6/21 白天 {daylight(k)}")
    C.emit("", [("年份", c01_years), ("今年", c01_this)], title="C-A33-01_Matariki假日")
    C.emit("", [("月曆", c02_cal), ("放假", c02_holiday)], title="C-A33-02_怎麼挑日子")
    if LANG == "en":                     # 英文版 EN33 只用 C-A33-01、02（其餘頁在英文版刪掉）
        return
    for nm, fn in (("C-A33-03_兩個季節", c03), ("C-A33-08_北島示意", c08)):
        f, ax = C.newfig(); fn(ax); C.save(f, "", f"{nm}_透明.png")
        f, ax = C.newfig(dark=True); fn(ax); C.save(f, "", f"{nm}_預覽_黑底.png", transparent=False)
    C.emit("", [("地平線", c04_horizon), ("三地", c04_cities)], title="C-A33-04_黎明重現")
    C.emit("", [("爐火", c06_fire), ("熱氣", c06_steam), ("名字", c06_names)], title="C-A33-06_hautapu")
    f, ax = C.newcard(dark=True); c05_card(ax); C.save(f, "", "C-A33-05_Matariki九星小辭典_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True); c07_card(ax); C.save(f, "", "C-A33-07_這週抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
