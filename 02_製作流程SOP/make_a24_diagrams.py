# -*- coding: utf-8 -*-
"""A-24 圖卡諾：亞馬遜的星空雨季曆｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A24-01 Tiquié 河在哪（南美、河流）→ 02 鏡
C-A24-02 用手量天（拳頭、手掌）→ 03 鏡
C-A24-03 poero 漲水（落下、雨、漲水）→ 05 鏡
C-A24-04 赤道與台北的星軌（赤道、台北）→ 06 鏡
C-A24-05 漲水年曆環（二月、三四月、全年）→ 07 鏡（前兩層）、14 鏡（三層）
C-A24-06 流星與名字（流星、晨星）→ 16 鏡
C-A24-07 圖卡諾的漲水曆（9:16 圖卡，可存圖）→ 14 鏡之後／首留言
C-A24-08 這週末抬頭看（9:16 圖卡，可存圖；台北 2027/3/5）→ 17 鏡

做法：地圖是手描示意輪廓（海岸線取十幾個經緯度點連起來，非精確國界）；河道是示意（Manaus、São Gabriel da
Cachoeira、Tiquié 河口 0°05′N 68°25′W、São José II 0.22°N 69.61°W）。不翻拍 Cardoso 論文的照片與插圖、
不用 Stellarium tukano 附圖（CC BY-SA）、不畫族人肖像；犰狳不畫任何「笛子」造型。
年曆環的月份＝Cardoso 2007 表 3.01（Tiquié 中游黃昏落下的時節）；天象 PyEphem 4.2.1 自算。

執行：python3 make_a24_diagrams.py            （中文，輸出 05_素材/A-24_圖卡諾/_概念圖/）
      python3 make_a24_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-24_圖卡諾/_概念圖")
CB.set_base(OUT)
RED, GREY, LAND, RIVER, CANOPY = "#FF6B6B", "#7C8BA8", "#2A3350", "#4F86C6", "#2E5E3E"
LANG = "zh"

MONTHS_ZH = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TXT = {
    "zh": {
        "c01_title": "Tiquié 河：巴西西北角", "c01_sub": "手描示意，非精確國界與河道",
        "sa": "南美洲", "br": "巴西", "co": "哥倫比亞", "pe": "秘魯", "ve": "委內瑞拉",
        "eq": "赤道 0°", "amazon": "亞馬遜河", "negro": "Rio Negro", "manaus": "Manaus",
        "zoom": "放大：亞馬遜州西北角", "uaupes": "Uaupés 河", "tiquie": "Tiquié 河",
        "sj": "São José II（Cardoso 去的村子）", "sj2": "北緯約 0.2°", "sg": "São Gabriel da Cachoeira",
        "c01_foot1": "圖卡諾人和 Tuyuka、Dessano 等鄰居住在河邊", "c01_foot2": "餐桌上最重要的肉：河裡的魚",
        "c02_title": "用手量天", "c02_sub": "手臂伸直，閉一隻眼",
        "fist": "拳頭 ≈ 10°", "palm": "張開手掌 ≈ 20°",
        "c02_foot1": "Cardoso 和 Yupuri 學校的學生、長老一起量星座的角度",
        "c02_foot2": "Cardoso 2007，3.3 節；示意圖，不按比例",
        "c03_title": "星座落下，河水漲一次", "west": "黃昏・西方地平線",
        "setting": "一個星座（或它的一段）落下", "rain": "幾天雨", "gauge": "河水",
        "poero": "poero＝漲水", "pamo": "pamõ poero＝犰狳的漲水",
        "c03_foot": "也有落下時反而乾的：白鷺 Yhé（Cardoso 2007 pp. 128、151、181）",
        "c04_title": "面向西方看星星落下", "eqp": "赤道（Tiquié）", "tpp": "台北 25°N",
        "eq1": "直直地往下沉", "eq2": "每顆星都會升起、落下", "tp1": "斜斜地落下", "tp2": "北天有拱極星，",
        "tp3": "南天有一圈看不到", "c04_foot": "星軌與地平線的夾角＝90° − 緯度",
        "c05_title": "圖卡諾的漲水年曆", "c05_center1": "黃昏落下的月份", "c05_center2": "Cardoso 2007 表 3.01",
        "c05_center3": "天上寫的，", "c05_center4": "幾乎是一條河",
        "newyear": "新年", "fish": "小魚與蝦", "yai": "美洲豹", "noh": "一群星（昴宿）", "wai": "魚架（畢宿）",
        "sio": "錛柄（獵戶）", "yhe": "白鷺（后髮）", "ana": "毒蛇（天蠍＋人馬）", "pamo2": "犰狳（天鷹＋海豚）",
        "dry": "乾、魚少", "c06_title": "流星與名字",
        "meteor1": "流星＝「星星人」ñhorkoá mahsã", "meteor2": "偷偷跑去約會——大家看到都會笑",
        "east": "黎明・東方", "venus": "金星", "seribhi": "Seribhi＝晨星", "ho": "Hó＝胖",
        "name1": "2006 年三天的命名儀式", "name2": "Cardoso 的圖卡諾名字",
        "c06_foot": "Cardoso 2007 pp. 27–28、186–187",
        "c07_title": "圖卡諾的漲水曆", "c07_sub": "Tiquié 河中游：黃昏時正在西方落下的星座",
        "col1": "落下", "col2": "原文", "col3": "意思", "col4": "星",
        "rows": [("2月", "Mhʉã", "小魚（jacundá）", "寶瓶座的暗星", PURPLE),
                 ("2月", "Dahsiʉ", "蝦（追著小魚）", "寶瓶＋鯨魚的暗星", PURPLE),
                 ("3–4月", "Yai", "美洲豹", "仙后（頭）＋仙女＋英仙＋鹿豹", AMBER),
                 ("4月底", "Ñohkoatero", "一群星・新年", "昴宿", BLUE),
                 ("4–5月", "Waikhasa", "放魚的木架", "畢宿", BLUE),
                 ("5月", "Sioyahpʉ", "錛柄", "獵戶腰帶＋兩肩", BLUE),
                 ("8–9月", "Yhé", "白鷺（乾、魚少）", "后髮座的暗星", PURPLE),
                 ("9–11月", "Aña", "毒蛇・心宿二＝毒囊", "天蠍＋人馬（頭在烏鴉）", RED),
                 ("12月", "Pamõ", "犰狳・也是聖笛", "天鷹三星＝骨＋海豚", GREEN)],
        "c07_extra": "不在主循環：北斗＝Sipé Phairó（吞魚的蛇）、南十字＝Uphaigʉ（龜）",
        "c07_src1": "Cardoso, W. T. 2007《O Céu dos Tukano na escola Yupuri》表 3.01",
        "c07_src2": "Stellarium tukano（Cardoso）；落下的星座常伴隨幾天雨與一次漲水 poero",
        "c08_title": "這週末抬頭看", "c08_sub": "台北 2027/3/5（五）–3/7（日）",
        "c08_rows": [("19:13", "天黑（天文昏影結束）", WHITE),
                     ("20:00 西北低空", "仙后座 W：西半邊＝美洲豹的頭\n王良一 15.6°、王良四 18.6°、γ 21.7°", AMBER),
                     ("", "東半邊＝前腿：閣道三 25.2°、閣道二 28.7°\n英仙 Mirfak（尾巴起點）42°", AMBER),
                     ("20:30 前", "頭還在 10° 以上（20:50 起陸續低於 10°）", AMBER),
                     ("20:00 往西", "昴宿 47°（西）、畢宿五 56°（西偏南）\n獵戶在西南高空＝接下來三個月的日曆", BLUE),
                     ("20:00 往東", "木星 54°、火星 48°，都在獅子座", WHITE),
                     ("月亮", "3/8 新月，週末晚上都沒有月光", GREY)],
        "c08_tq1": "同一時間在 Tiquié（赤道）：", "c08_tq2": "美洲豹的鬍鬚正碰到西北的地平線——美洲豹的漲水",
        "c08_src": "PyEphem 4.2.1 自算（台北 25.033°N 121.565°E；Tiquié 0.22°N 69.61°W）",
    },
    "en": {
        "c01_title": "The Tiquié River: NW Brazil", "c01_sub": "Hand-drawn sketch; borders and rivers schematic",
        "sa": "South America", "br": "Brazil", "co": "Colombia", "pe": "Peru", "ve": "Venezuela",
        "eq": "Equator 0°", "amazon": "Amazon", "negro": "Rio Negro", "manaus": "Manaus",
        "zoom": "Zoom: NW Amazonas state", "uaupes": "Uaupés", "tiquie": "Tiquié",
        "sj": "São José II (Cardoso's village)", "sj2": "about 0.2°N", "sg": "São Gabriel da Cachoeira",
        "c01_foot1": "Home of the Tukano and neighbours (Tuyuka, Dessano…)", "c01_foot2": "The most important meat: river fish",
        "c02_title": "Measuring the sky by hand", "c02_sub": "Arm straight, one eye closed",
        "fist": "fist ≈ 10°", "palm": "open hand ≈ 20°",
        "c02_foot1": "Cardoso measured constellations with Yupuri students and elders",
        "c02_foot2": "Cardoso 2007, §3.3; schematic, not to scale",
        "c03_title": "A constellation sets, the river rises", "west": "Dusk · western horizon",
        "setting": "a constellation (or part of it) sets", "rain": "a few days of rain", "gauge": "river",
        "poero": "poero = flood", "pamo": "pamõ poero = the armadillo's flood",
        "c03_foot": "Some settings bring dry spells instead: the egret Yhé (Cardoso 2007 pp. 128, 151, 181)",
        "c04_title": "Facing west as stars set", "eqp": "Equator (Tiquié)", "tpp": "Taipei 25°N",
        "eq1": "they sink straight down", "eq2": "every star rises and sets", "tp1": "they set at a slant", "tp2": "circumpolar stars in the north,",
        "tp3": "a southern cap never rises", "c04_foot": "angle of star trails to the horizon = 90° − latitude",
        "c05_title": "The Tukano flood calendar", "c05_center1": "month of setting at dusk", "c05_center2": "Cardoso 2007, Table 3.01",
        "c05_center3": "The sky reads", "c05_center4": "almost like a river",
        "newyear": "New Year", "fish": "fish & shrimp", "yai": "jaguar", "noh": "group of stars (Pleiades)", "wai": "fish rack (Hyades)",
        "sio": "adze handle (Orion)", "yhe": "egret (Coma)", "ana": "fer-de-lance (Sco + Sgr)", "pamo2": "armadillo (Aql + Del)",
        "dry": "dry, few fish", "c06_title": "Meteors and a name",
        "meteor1": "Meteors = ñhorkoá mahsã, 'star people'", "meteor2": "sneaking off on a date — everyone laughs",
        "east": "Dawn · east", "venus": "Venus", "seribhi": "Seribhi = morning star", "ho": "Hó = chubby",
        "name1": "A three-day naming ceremony, 2006", "name2": "Cardoso's Tukano name",
        "c06_foot": "Cardoso 2007 pp. 27–28, 186–187",
        "c07_title": "The Tukano flood calendar", "c07_sub": "Middle Tiquié: constellations setting in the west at dusk",
        "col1": "Sets", "col2": "Name", "col3": "Meaning", "col4": "Stars",
        "rows": [("Feb", "Mhʉã", "small fish (jacundá)", "faint stars of Aquarius", PURPLE),
                 ("Feb", "Dahsiʉ", "shrimp (chasing the fish)", "faint stars of Aqr + Cet", PURPLE),
                 ("Mar–Apr", "Yai", "jaguar", "Cas (head) + And + Per + Cam", AMBER),
                 ("late Apr", "Ñohkoatero", "group of stars · New Year", "Pleiades", BLUE),
                 ("Apr–May", "Waikhasa", "fish rack", "Hyades", BLUE),
                 ("May", "Sioyahpʉ", "adze handle", "Orion's Belt + shoulders", BLUE),
                 ("Aug–Sep", "Yhé", "egret (dry, few fish)", "faint stars of Coma", PURPLE),
                 ("Sep–Nov", "Aña", "fer-de-lance · Antares = venom sac", "Sco + Sgr (head in Corvus)", RED),
                 ("Dec", "Pamõ", "armadillo · also a sacred flute", "Altair trio = bones + Delphinus", GREEN)],
        "c07_extra": "Outside the main cycle: Big Dipper = Sipé Phairó (fish-eating snake), Crux = Uphaigʉ (tortoise)",
        "c07_src1": "Cardoso, W. T. 2007, O Céu dos Tukano na escola Yupuri, Table 3.01",
        "c07_src2": "Stellarium tukano (Cardoso); each setting often brings rain and a flood, poero",
        "c08_title": "Look up this weekend", "c08_sub": "Taipei, Fri 5 – Sun 7 Mar 2027",
        "c08_rows": [("19:13", "Dark (end of astronomical twilight)", WHITE),
                     ("20:00 low NW", "Cassiopeia's W: west half = the jaguar's head\nCaph 15.6°, Schedar 18.6°, γ 21.7°", AMBER),
                     ("", "East half = forelegs: Ruchbah 25.2°, Segin 28.7°\nMirfak (start of the tail) 42°", AMBER),
                     ("before 20:30", "Head still above 10° (drops below from 20:50)", AMBER),
                     ("20:00 west", "Pleiades 47° (W), Aldebaran 56° (WSW)\nOrion high in the SW = the next three months", BLUE),
                     ("20:00 east", "Jupiter 54°, Mars 48°, both in Leo", WHITE),
                     ("Moon", "New Moon 8 Mar: no moonlight all weekend", GREY)],
        "c08_tq1": "Same moment at Tiquié (equator):", "c08_tq2": "the jaguar's whiskers touch the NW horizon — the jaguar's flood",
        "c08_src": "Computed with PyEphem 4.2.1 (Taipei 25.033°N 121.565°E; Tiquié 0.22°N 69.61°W)",
    },
}


def tx(k):
    return TXT[LANG][k]


# ══════════════════════ C-A24-01 Tiquié 河在哪 ══════════════════════
COAST = [(12.4, -71.7), (11.0, -74.8), (9.5, -76.0), (8.7, -77.4), (7.0, -77.8), (4.0, -77.4), (1.5, -79.0),
         (-1.0, -80.5), (-3.5, -80.3), (-5.0, -81.2), (-6.5, -79.9), (-9.5, -78.5), (-12.5, -76.7),
         (-15.5, -75.0), (-18.3, -70.4), (-23.5, -70.5), (-27.0, -70.9), (-30.0, -71.4), (-33.0, -71.7),
         (-37.0, -73.6), (-41.5, -73.8), (-46.0, -75.5), (-50.0, -75.4), (-53.0, -74.0), (-55.0, -69.0),
         (-54.0, -67.5), (-52.3, -68.4), (-50.0, -68.9), (-47.0, -65.8), (-45.0, -67.2), (-42.5, -63.8),
         (-40.8, -62.2), (-38.8, -62.3), (-36.3, -56.8), (-34.9, -56.2), (-33.7, -53.4), (-30.0, -50.3),
         (-28.0, -48.6), (-25.5, -48.4), (-23.0, -43.2), (-22.0, -41.0), (-18.5, -39.7), (-13.0, -38.5),
         (-8.0, -34.9), (-5.2, -35.5), (-3.0, -40.0), (-2.5, -44.3), (-0.5, -48.5), (1.8, -50.0),
         (4.0, -51.6), (5.8, -55.0), (6.8, -58.2), (8.6, -60.6), (10.7, -61.9), (10.6, -64.3),
         (10.4, -67.0), (11.5, -69.8), (12.4, -71.7)]
AMAZON = [(-0.5, -50.5), (-1.9, -54.5), (-2.4, -56.5), (-3.1, -59.9), (-3.4, -64.7), (-4.0, -67.0),
          (-4.25, -69.9), (-3.75, -73.25)]
NEGRO = [(-3.1, -59.9), (-1.9, -61.5), (-0.97, -62.93), (-0.41, -65.02), (-0.13, -67.09), (1.2, -66.85)]
UAUPES = [(0.05, -67.25), (0.12, -68.0), (0.30, -68.9), (0.60, -69.2), (1.0, -69.7), (1.25, -70.23)]
TIQUIE = [(0.08, -68.42), (0.10, -68.9), (0.22, -69.61), (0.25, -70.0), (0.35, -70.5)]
SJ2 = (0.22, -69.61)
SC, LONC, LATC = 0.024, -60.0, -18.0


def mp(lat, lon):
    return -0.30 + (lon - LONC) * SC, (lat - LATC) * SC


def c01_sa(ax):
    T(ax, 0.0, 0.92, tx("c01_title"), 31, WHITE)
    T(ax, 0.0, 0.845, tx("c01_sub"), 16, GREY, w="normal")
    xy = [mp(*p) for p in COAST]
    ax.add_patch(CB.Polygon(xy, closed=True, fc=LAND, ec=GREY, lw=1.6, alpha=.95, zorder=2))
    a, b = mp(0, -84), mp(0, -46)
    ax.plot([a[0], b[0]], [a[1], a[1]], c=AMBER, lw=1.4, ls=(0, (6, 5)), alpha=.8, zorder=3)
    T(ax, a[0] + 0.01, a[1] + 0.035, tx("eq"), 14, AMBER, ha="left", w="normal")
    for path, w in ((AMAZON, 3.2), (NEGRO, 2.4)):
        p = [mp(*q) for q in path]
        ax.plot([q[0] for q in p], [q[1] for q in p], c=RIVER, lw=w, alpha=.95, zorder=4, solid_capstyle="round")
    T(ax, *mp(-6.2, -57.0), tx("amazon"), 14, RIVER, w="normal")
    x, y = mp(-3.1, -59.9)
    ax.scatter([x], [y], s=40, c=WHITE, zorder=6, lw=0)
    T(ax, x + 0.02, y - 0.04, tx("manaus"), 12, GREY, ha="left", w="normal")
    T(ax, *mp(-12.0, -51.0), tx("br"), 24, WHITE, w="normal", alpha=.8)
    T(ax, *mp(4.5, -73.5), tx("co"), 15, GREY, w="normal")
    T(ax, *mp(-8.5, -75.5), tx("pe"), 15, GREY, w="normal")
    T(ax, *mp(7.2, -65.0), tx("ve"), 15, GREY, w="normal")
    T(ax, *mp(-30.0, -64.0), tx("sa"), 15, GREY, w="normal")
    x, y = mp(*SJ2)
    ax.scatter([x], [y], s=150, c=AMBER, zorder=8, lw=0)
    ax.scatter([x], [y], s=700, c=AMBER, alpha=.18, zorder=7, lw=0)
    # 放大框的索引框
    bx0, by0 = mp(-1.2, -71.2); bx1, by1 = mp(1.8, -66.2)
    ax.add_patch(CB.Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fc="none", ec=AMBER, lw=1.4, zorder=9))


ZC, ZK = (0.4, -68.6), 0.13          # 放大框中心經緯度、每度


def c01_river(ax):
    bx, by, bw, bh = 0.08, -0.36, 0.86, 0.66
    ax.add_patch(CB.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.0,rounding_size=0.03",
                                   fc="#10172E", ec=AMBER, lw=1.4, zorder=10))
    T(ax, bx + 0.03, by + bh - 0.045, tx("zoom"), 14, AMBER, w="normal", ha="left")
    cx0, cy0 = bx + bw / 2, by + bh / 2 - 0.03

    def mi(lat, lon):
        return cx0 + (lon - ZC[1]) * ZK, cy0 + (lat - ZC[0]) * ZK
    a, b = mi(0, -71.5), mi(0, -65.9)
    ax.plot([a[0], b[0]], [a[1], a[1]], c=AMBER, lw=1.2, ls=(0, (6, 5)), alpha=.7, zorder=11)
    T(ax, a[0] + 0.01, a[1] - 0.03, tx("eq"), 12, AMBER, ha="left", w="normal", z=13)
    for path, w, col in ((NEGRO, 3.0, RIVER), (UAUPES, 2.4, RIVER), (TIQUIE, 3.4, "#8FC1FF")):
        p = [mi(*q) for q in path if abs(q[1] - ZC[1]) < 2.9 and abs(q[0] - ZC[0]) < 2.2]
        ax.plot([q[0] for q in p], [q[1] for q in p], c=col, lw=w, alpha=.95, zorder=12, solid_capstyle="round")
    T(ax, *mi(0.75, -66.45), tx("negro"), 12, RIVER, w="normal", z=13)
    T(ax, *mi(1.25, -69.0), tx("uaupes"), 13, RIVER, w="normal", z=13)
    T(ax, *mi(-0.2, -68.8), tx("tiquie"), 16, "#8FC1FF", z=13)
    x, y = mi(-0.13, -67.09)
    ax.scatter([x], [y], s=30, c=WHITE, zorder=13, lw=0)
    T(ax, x + 0.01, y - 0.075, tx("sg"), 10.5, GREY, w="normal", ha="center", z=13)
    x, y = mi(*SJ2)
    ax.scatter([x], [y], s=120, c=AMBER, zorder=14, lw=0)
    T(ax, x - 0.02, y + 0.105, tx("sj"), 14, AMBER, z=14)
    T(ax, x - 0.02, y + 0.065, tx("sj2"), 12, AMBER, w="normal", z=14)
    T(ax, 0.51, -0.47, tx("c01_foot1"), 15, WHITE, w="normal")
    T(ax, 0.51, -0.53, tx("c01_foot2"), 15, WHITE, w="normal")


# ══════════════════════ C-A24-02 用手量天 ══════════════════════
EYE = (-0.70, -0.10)
ARM = 1.25


def _ray(deg):
    r = math.radians(deg)
    return EYE[0] + ARM * math.cos(r), EYE[1] + ARM * math.sin(r)


def _wedge(ax, a0, a1, col, label, lab_r, text_r=1.36):
    p0, p1 = _ray(a0), _ray(a1)
    for p in (p0, p1):
        ax.plot([EYE[0], p[0]], [EYE[1], p[1]], c=col, lw=1.6, ls=(0, (4, 4)), alpha=.8, zorder=5)
    ax.add_patch(CB.Polygon([EYE, p0, p1], closed=True, fc=col, ec="none", alpha=.10, zorder=4))
    ax.add_patch(CB.Arc(EYE, 2 * lab_r, 2 * lab_r, theta1=a0, theta2=a1, color=col, lw=2.4, zorder=6))
    mid = math.radians((a0 + a1) / 2)
    T(ax, EYE[0] + text_r * math.cos(mid), EYE[1] + text_r * math.sin(mid), label, 22, col)


def c02_fist(ax):
    T(ax, 0.0, 0.92, tx("c02_title"), 31, WHITE)
    T(ax, 0.0, 0.845, tx("c02_sub"), 17, GREY, w="normal")
    ax.add_patch(CB.Circle((EYE[0] - 0.09, EYE[1] + 0.02), 0.11, fc="none", ec=WHITE, lw=2.4, zorder=6))
    ax.scatter([EYE[0]], [EYE[1]], s=50, c=WHITE, zorder=7, lw=0)
    hx = EYE[0] + 0.85
    ax.plot([EYE[0] - 0.05, hx], [EYE[1] - 0.18, EYE[1] - 0.07], c=WHITE, lw=7, alpha=.85, solid_capstyle="round", zorder=6)
    # 拳頭（10°）：在手臂端點，視角 −2°…+8°
    a0, a1 = -2.0, 8.0
    r = hx - EYE[0]
    y0, y1 = EYE[1] + r * math.tan(math.radians(a0)), EYE[1] + r * math.tan(math.radians(a1))
    ax.add_patch(CB.FancyBboxPatch((hx - 0.03, y0), 0.07, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.025",
                                   fc=WHITE, ec="none", alpha=.9, zorder=7))
    _wedge(ax, a0, a1, AMBER, tx("fist"), 0.62)
    for i, (dx, dy) in enumerate(((0.55, 0.36), (0.72, 0.05), (0.62, -0.30))):
        ax.scatter([EYE[0] + 1.2 + dx * 0.2 - 0.1], [EYE[1] + dy * 0.6], s=28, c=WHITE, alpha=.7, zorder=3, lw=0)
    T(ax, 0.0, -0.80, tx("c02_foot1"), 16, WHITE, w="normal")
    T(ax, 0.0, -0.87, tx("c02_foot2"), 13, GREY, w="normal")


def c02_palm(ax):
    _wedge(ax, 12.0, 32.0, GREEN, tx("palm"), 0.80)
    hx = EYE[0] + 0.85
    r = hx - EYE[0]
    y0, y1 = EYE[1] + r * math.tan(math.radians(12)), EYE[1] + r * math.tan(math.radians(32))
    ax.plot([hx, hx], [y0, y1], c=GREEN, lw=5, alpha=.85, solid_capstyle="round", zorder=7)
    ax.scatter([hx, hx], [y0, y1], s=60, c=GREEN, zorder=8, lw=0)


# ══════════════════════ C-A24-03 poero 漲水 ══════════════════════
HZ3 = 0.05


def _canopy(ax, y, x0=-0.92, x1=0.92):
    xs = [x0 + (x1 - x0) * i / 300 for i in range(301)]
    ys = [y + 0.035 * abs(math.sin(x * 9.0)) + 0.02 * abs(math.sin(x * 23.0 + 1)) for x in xs]
    ax.fill_between(xs, [y - 0.06] * len(xs), ys, color=CANOPY, alpha=.95, zorder=5, lw=0)


def c03_set(ax):
    T(ax, 0.0, 0.92, tx("c03_title"), 31, WHITE)
    _canopy(ax, HZ3)
    T(ax, 0.62, HZ3 - 0.11, tx("west"), 14, GREY, w="normal")
    pts = [(-0.30, 0.55), (-0.18, 0.40), (-0.05, 0.30), (0.05, 0.16), (0.12, 0.07)]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=AMBER, lw=2.4, alpha=.9, zorder=6)
    for i, (x, y) in enumerate(pts):
        ax.scatter([x], [y], s=70 if i else 50, c=WHITE, zorder=7, lw=0)
    CB.arrow(ax, (0.24, 0.08), (0.24, 0.40), c=AMBER, lw=2.2, alpha=.8, style="-|>")
    T(ax, -0.30, 0.70, tx("setting"), 18, AMBER)


def c03_rain(ax):
    cx, cy = 0.55, 0.62
    for dx, dy, r in ((-0.12, 0.0, 0.10), (0.0, 0.05, 0.13), (0.13, 0.0, 0.10)):
        ax.add_patch(CB.Circle((cx + dx, cy + dy), r, fc=GREY, ec="none", alpha=.55, zorder=4))
    for i in range(9):
        x = cx - 0.20 + i * 0.05
        ax.plot([x, x - 0.03], [cy - 0.10, cy - 0.30], c=BLUE, lw=2.0, alpha=.75, zorder=4)
    T(ax, cx, cy + 0.22, tx("rain"), 18, BLUE)


def c03_flood(ax):
    gx, top, bot = -0.55, -0.20, -0.62
    ax.add_patch(CB.Rectangle((-0.90, bot), 1.80, 0.10, fc=RIVER, ec="none", alpha=.35, zorder=3))
    ax.add_patch(CB.Rectangle((-0.90, bot + 0.10), 1.80, 0.14, fc=RIVER, ec="none", alpha=.55, zorder=3))
    CB.water(ax, y=bot + 0.24, x0=-0.90, x1=0.90, c="#8FC1FF", rows=1, amp=0.010, freq=18)
    ax.plot([gx, gx], [bot, top], c=WHITE, lw=2.0, alpha=.8, zorder=6)
    for k in range(6):
        y = bot + k * 0.08
        ax.plot([gx - 0.025, gx + 0.025], [y, y], c=WHITE, lw=1.4, alpha=.8, zorder=6)
    CB.arrow(ax, (gx + 0.10, bot + 0.24), (gx + 0.10, bot + 0.08), c="#8FC1FF", lw=2.4, alpha=.9, style="-|>")
    T(ax, gx - 0.08, top + 0.04, tx("gauge"), 14, GREY, w="normal")
    T(ax, 0.10, -0.71, tx("poero"), 24, "#8FC1FF")
    T(ax, 0.10, -0.79, tx("pamo"), 20, GREEN)
    T(ax, 0.0, -0.89, tx("c03_foot"), 13, GREY, w="normal")


# ══════════════════════ C-A24-04 赤道與台北的星軌 ══════════════════════
def _trails(ax, cx, tilt, col):
    """面向西方：星軌與地平線夾角＝90°−緯度；向右下（北在右）"""
    hz = -0.30
    ax.plot([cx - 0.40, cx + 0.40], [hz, hz], c=WHITE, lw=2.0, alpha=.8, zorder=6)
    ax.add_patch(CB.Rectangle((cx - 0.40, hz - 0.22), 0.80, 0.22, fc=CANOPY, ec="none", alpha=.6, zorder=5))
    a = math.radians(tilt)
    for k in range(5):
        x0 = cx - 0.32 + k * 0.16
        L = 0.62
        xs, ys = x0 + L * math.cos(a) * 0.0, hz
        top = (x0 - L * math.cos(a), hz + L * math.sin(a))
        ax.plot([top[0], x0], [top[1], hz], c=col, lw=2.2, alpha=.85, zorder=4)
        CB.arrow(ax, (x0, hz + 0.01), (x0 - 0.12 * math.cos(a), hz + 0.12 * math.sin(a)), c=col, lw=2.2,
                 alpha=.95, style="-|>")
        ax.scatter([top[0]], [top[1]], s=40, c=WHITE, zorder=7, lw=0)
    T(ax, cx, hz - 0.08, "W", 14, GREY, w="normal")


def c04_eq(ax):
    T(ax, 0.0, 0.92, tx("c04_title"), 31, WHITE)
    T(ax, -0.48, 0.62, tx("eqp"), 22, AMBER)
    _trails(ax, -0.48, 90.0, AMBER)
    T(ax, -0.48, -0.66, tx("eq1"), 17, AMBER)
    T(ax, -0.48, -0.73, tx("eq2"), 15, WHITE, w="normal")
    T(ax, 0.0, -0.88, tx("c04_foot"), 13, GREY, w="normal")


def c04_tp(ax):
    T(ax, 0.48, 0.62, tx("tpp"), 22, BLUE)
    _trails(ax, 0.48, 65.0, BLUE)
    T(ax, 0.48, -0.66, tx("tp1"), 17, BLUE)
    T(ax, 0.48, -0.73, tx("tp2"), 15, WHITE, w="normal")
    T(ax, 0.48, -0.79, tx("tp3"), 15, WHITE, w="normal")


# ══════════════════════ C-A24-05 漲水年曆環 ══════════════════════
R0 = 0.50                                         # 月份環半徑


def mang(m):
    """月份（1.0＝1 月 1 日，13.0＝年底）→ 角度：1 月在正上方、順時針"""
    return math.radians(90.0 - (m - 1.0) * 30.0)


def _arc(ax, m0, m1, r, col, lw=9):
    n = 40
    xs = [r * math.cos(mang(m0 + (m1 - m0) * i / n)) for i in range(n + 1)]
    ys = [r * math.sin(mang(m0 + (m1 - m0) * i / n)) for i in range(n + 1)]
    ax.plot(xs, ys, c=col, lw=lw, alpha=.92, solid_capstyle="round", zorder=6)


def _lab(ax, m, r, s1, s2, col, fs=15):
    a = mang(m)
    x, y = r * math.cos(a), r * math.sin(a)
    ha = "left" if x > 0.05 else ("right" if x < -0.05 else "center")
    T(ax, x, y + 0.025, s1, fs, col, ha=ha)
    if s2:
        T(ax, x, y - 0.022, s2, fs - 3, WHITE, ha=ha, w="normal")


# (起月, 迄月, 環半徑, 色, 原文, 中文鍵, 標籤位置月, 標籤半徑)
CAL = {   # (起月, 迄月, 環半徑, 色, 原文, 中文鍵, 標籤 x, y, ha)
    "二月": [(2.0, 2.6, 0.43, PURPLE, "Mhʉã・Dahsiʉ", "fish", 0.36, 0.66, "left")],
    "三四月": [(3.0, 4.9, 0.43, AMBER, "Yai", "yai", 0.62, 0.16, "left")],
    "全年": [(4.45, 5.0, 0.36, BLUE, "Ñohkoatero", "noh", 0.60, -0.26, "left"),
             (4.8, 5.5, 0.29, BLUE, "Waikhasa", "wai", 0.60, -0.42, "left"),
             (5.45, 6.0, 0.36, BLUE, "Sioyahpʉ", "sio", 0.60, -0.58, "left"),
             (8.0, 9.9, 0.43, PURPLE, "Yhé", "yhe", -0.60, -0.40, "right"),
             (9.0, 12.0, 0.36, RED, "Aña", "ana", -0.62, 0.20, "right"),
             (12.4, 12.9, 0.43, GREEN, "Pamõ", "pamo2", -0.30, 0.66, "right")],
}


def _cal_layer(key):
    def f(ax):
        if key == "二月":
            T(ax, 0.0, 0.94, tx("c05_title"), 30, WHITE)
            ax.add_patch(CB.Circle((0, 0), R0, fc="none", ec=WHITE, lw=1.4, alpha=.45, zorder=3))
            mn = MONTHS_ZH if LANG == "zh" else MONTHS_EN
            for i in range(12):
                a = mang(i + 1.0)
                ax.plot([R0 * math.cos(a), (R0 + 0.03) * math.cos(a)], [R0 * math.sin(a), (R0 + 0.03) * math.sin(a)],
                        c=WHITE, lw=1.4, alpha=.6, zorder=4)
                am = mang(i + 1.5)
                T(ax, 0.555 * math.cos(am), 0.555 * math.sin(am), mn[i], 12, GREY, w="normal")
            T(ax, 0.0, 0.035, tx("c05_center1"), 15, WHITE, w="normal")
            T(ax, 0.0, -0.025, tx("c05_center2"), 11.5, GREY, w="normal")
        for m0, m1, r, col, nat, k, lx, ly, ha in CAL[key]:
            _arc(ax, m0, m1, r, col)
            T(ax, lx, ly + 0.025, nat, 16, col, ha=ha)
            T(ax, lx, ly - 0.025, tx(k), 13, WHITE, ha=ha, w="normal")
        if key == "全年":
            a = mang(4.6)
            x, y = 0.30 * math.cos(a), 0.30 * math.sin(a)
            T(ax, x - 0.02, y - 0.06, "★ " + tx("newyear"), 13, AMBER, ha="right")
            T(ax, -0.60, -0.475, tx("dry"), 12, GREY, w="normal", ha="right")
            T(ax, 0.0, -0.80, tx("c05_center3") + tx("c05_center4"), 20, BLUE)
    return f


# ══════════════════════ C-A24-06 流星與名字 ══════════════════════
def c06_meteor(ax):
    T(ax, 0.0, 0.92, tx("c06_title"), 31, WHITE)
    import random
    rnd = random.Random(7)
    for _ in range(40):
        ax.scatter([rnd.uniform(-0.9, 0.9)], [rnd.uniform(0.15, 0.78)], s=rnd.uniform(4, 24), c=WHITE,
                   alpha=.6, zorder=3, lw=0)
    for (x0, y0), L in (((0.55, 0.72), 0.55), ((0.10, 0.62), 0.28)):
        n = 30
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            ax.plot([x0 - L * t0, x0 - L * t1], [y0 - 0.45 * L * t0, y0 - 0.45 * L * t1], c=WHITE,
                    lw=0.6 + 2.6 * t1, alpha=.15 + .8 * t1, zorder=5, solid_capstyle="round")
    T(ax, 0.0, 0.26, tx("meteor1"), 19, WHITE)
    T(ax, 0.0, 0.19, tx("meteor2"), 16, WHITE, w="normal")


def c06_venus(ax):
    hz = -0.30
    for k in range(10):
        ax.add_patch(CB.Rectangle((-0.92, hz + k * 0.025), 1.84, 0.025, fc=AMBER, ec="none",
                                  alpha=.10 * (1 - k / 10), zorder=2))
    _canopy(ax, hz)
    T(ax, 0.70, hz - 0.11, tx("east"), 14, GREY, w="normal")
    vx, vy = -0.30, -0.05
    ax.scatter([vx], [vy], s=900, c=WHITE, alpha=.15, zorder=6, lw=0)
    ax.scatter([vx], [vy], s=160, c=WHITE, zorder=7, lw=0)
    T(ax, vx + 0.07, vy, tx("venus"), 15, WHITE, ha="left", w="normal")
    ax.add_patch(CB.FancyBboxPatch((-0.62, -0.88), 1.24, 0.40, boxstyle="round,pad=0.01,rounding_size=0.04",
                                   fc="#1B2240", ec=AMBER, lw=1.6, zorder=8))
    T(ax, 0.0, -0.53, tx("name2"), 14, GREY, w="normal", z=9)
    T(ax, 0.0, -0.62, "Seribhi Hó", 34, AMBER, z=9)
    T(ax, 0.0, -0.71, tx("seribhi") + "　" + tx("ho"), 16, WHITE, w="normal", z=9)
    T(ax, 0.0, -0.78, tx("name1"), 13, GREY, w="normal", z=9)
    T(ax, 0.0, -0.84, tx("c06_foot"), 11, GREY, w="normal", z=9)


# ══════════════════════ C-A24-07 圖卡諾的漲水曆（9:16 圖卡） ══════════════════════
def c07_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.947, tx("c07_title"), fontproperties=FP, fontsize=28, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.909, tx("c07_sub"), fontproperties=FP, fontsize=12.5, color=GREY, ha="center", va="center")
    X = (0.04, 0.20, 0.43, 0.96)
    y = 0.872
    for x, k, ha in ((X[0], "col1", "left"), (X[1], "col2", "left"), (X[2], "col3", "left")):
        ax.text(x, y, tx(k), fontproperties=FP, fontsize=11.5, color=GREY, ha=ha, va="center", weight="bold")
    ax.plot([0.03, 0.97], [0.858, 0.858], c=WHITE, lw=1.0, alpha=.4)
    y = 0.850
    for mon, nat, zh, stars, col in tx("rows"):
        h = 0.072
        ax.text(X[0], y - 0.022, mon, fontproperties=FP, fontsize=12, color=col, ha="left", va="center",
                weight="bold")
        ax.text(X[1], y - 0.022, nat, fontproperties=FP, fontsize=14, color=col, ha="left", va="center",
                weight="bold")
        ax.text(X[2], y - 0.022, zh, fontproperties=FP, fontsize=12.5, color=WHITE, ha="left", va="center")
        ax.text(X[2], y - 0.050, stars, fontproperties=FP, fontsize=10.5, color=GREY, ha="left", va="center")
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.text(0.5, y - 0.030, tx("c07_extra"), fontproperties=FP, fontsize=10.5, color=WHITE, ha="center",
            va="center", alpha=.9)
    ax.text(0.5, 0.090, tx("c07_src1"), fontproperties=FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.068, tx("c07_src2"), fontproperties=FP, fontsize=9.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center",
            va="center")


# ══════════════════════ C-A24-08 這週末抬頭看（9:16 圖卡） ══════════════════════
def c08_card(ax):
    FP = CB.FP
    ax.text(0.5, 0.947, tx("c08_title"), fontproperties=FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.907, tx("c08_sub"), fontproperties=FP, fontsize=14, color=GREY, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.880, 0.880], c=WHITE, lw=1.0, alpha=.4)
    y = 0.865
    for t, body, col in tx("c08_rows"):
        n = body.count("\n") + 1
        h = 0.030 + 0.030 * n
        if t:
            ax.text(0.04, y - 0.026, t, fontproperties=FP, fontsize=13, color=col, ha="left", va="center",
                    weight="bold")
        ax.text(0.30, y - 0.012 - 0.015 * n, body, fontproperties=FP, fontsize=12, color=WHITE, ha="left",
                va="center", linespacing=1.45)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.add_patch(CB.FancyBboxPatch((0.05, y - 0.130), 0.90, 0.100, boxstyle="round,pad=0.005,rounding_size=0.02",
                                   fc="#1B2240", ec=AMBER, lw=1.2))
    ax.text(0.5, y - 0.058, tx("c08_tq1"), fontproperties=FP, fontsize=12.5, color=AMBER, ha="center",
            va="center", weight="bold")
    ax.text(0.5, y - 0.095, tx("c08_tq2"), fontproperties=FP, fontsize=11.5, color=WHITE, ha="center",
            va="center")
    ax.text(0.5, 0.068, tx("c08_src"), fontproperties=FP, fontsize=9.0, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=FP, fontsize=13, color=WHITE, ha="center",
            va="center")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    CB.emit("", [("南美", c01_sa), ("河流", c01_river)], title="C-A24-01_Tiquié河在哪")
    CB.emit("", [("拳頭", c02_fist), ("手掌", c02_palm)], title="C-A24-02_用手量天")
    CB.emit("", [("落下", c03_set), ("雨", c03_rain), ("漲水", c03_flood)], title="C-A24-03_poero漲水")
    CB.emit("", [("赤道", c04_eq), ("台北", c04_tp)], title="C-A24-04_赤道與台北的星軌")
    CB.emit("", [(k, _cal_layer(k)) for k in ("二月", "三四月", "全年")], title="C-A24-05_漲水年曆環")
    CB.emit("", [("流星", c06_meteor), ("晨星", c06_venus)], title="C-A24-06_流星與名字")
    f, ax = CB.newcard(dark=True)
    c07_card(ax)
    CB.save(f, "", "C-A24-07_圖卡諾的漲水曆_圖卡.png", transparent=False)
    f, ax = CB.newcard(dark=True)
    c08_card(ax)
    CB.save(f, "", "C-A24-08_這週末抬頭看_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
