# -*- coding: utf-8 -*-
"""A-21 薩米：馴鹿獵人的星空狩獵圖｜概念圖（C 系列骨架；方形透明分層＋9:16 圖卡）

C-A21-01 薩米在哪裡（地圖、神鼓）→ 02 鏡
C-A21-02 馴鹿回到星圖（1736、1743、2025）→ 04 鏡（只留年份＋星名，不放說明句）
C-A21-03 不能射的那一箭（狩獵、箭）→ 06 鏡
C-A21-07 天狼星貼地平線（地平線、Kautokeino）→ 08 鏡
C-A21-04 同一把北斗（9:16 圖卡，可存圖）→ 10 鏡
C-A21-05 這週末抬頭看（9:16 圖卡，可存圖；台北 2027/2/12 20:00、23:00）→ 11 鏡
C-A21-06 薩米星名小辭典（9:16 圖卡，可存圖）→ 12 鏡

尊重文化的做法：神鼓只畫自繪的抽象示意（橢圓框鼓＋幾條分隔線＋太陽符號），不臨摹任何館藏神鼓的圖像；
要用實物照片由美宣另尋授權來源。地圖是手描的示意輪廓（非精確海岸線）。
天象 PyEphem 4.2.1 自算（台北 25.033°N 121.565°E UTC+8 15°C／1010 hPa；Kautokeino 69.01°N 23.04°E CET −15°C）。

執行：python3 make_a21_diagrams.py            （中文，輸出 05_素材/A-21_薩米/_概念圖/）
      python3 make_a21_diagrams.py --lang en  （英文，輸出 _概念圖/en/；本次只出 zh）
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-21_薩米/_概念圖")
CB.set_base(OUT)
RED, GREY, EARTH, LAND, SEA = "#FF6B6B", "#7C8BA8", "#3A2E22", "#2A3350", "#0B0F1E"
LANG = "zh"

TXT = {
    "zh": {
        "c01_title": "薩米人的家：Sápmi", "c01_sub": "手描示意，非精確地圖",
        "norway": "挪威", "sweden": "瑞典", "finland": "芬蘭", "russia": "俄羅斯", "kola": "科拉半島",
        "sapmi": "Sápmi（薩米地區）", "arctic": "北極圈 66.6°N", "kauto": "Kautokeino",
        "drum": "神鼓", "drum2": "自繪示意，不臨摹館藏", "drum_y1": "1609　丹麥—挪威列為巫術",
        "drum_y2": "十八世紀　大量沒收、燒毀", "drum_y3": "今天留存約 70 面",
        "c02_title": "馴鹿回到星圖", "y1736": "1736–37", "y1736b": "拉普蘭",
        "y1743": "1743", "y1743b": "Le Monnier：馴鹿座 le Renne",
        "y2025": "2025", "y2025b": "IAU",
        "polaris": "北極星", "cas": "仙后座", "per": "英仙座",
        "s_sarvvis": "Sarvvis（δ Per）", "s_aldu": "Áldu（ε Per）",
        "s_rang": "Rangifer（49 Cas）", "s_tar": "Tarandus（2 UMi）",
        "c03_title": "不能射的那一箭", "c03_sub": "Stellarium sami；Turi 1910 星圖說明",
        "hunter": "Fávdna 獵人（大角星）", "bow": "弓（北斗）",
        "pole": "Boahjenásti", "pole2": "撐住天空的星（北極星）",
        "deer": "Sarvvis（仙后—英仙—御夫）", "hit": "射中它＝天塌、世界結束", "still": "所以弓拉滿，遲遲沒放",
        "c07_title": "天狼星在薩米地區有多高？", "south": "南",
        "kplace": "Kautokeino（69°N）", "kwhen": "2027/2/12 20:43　天狼星過子午線",
        "kalt": "最高 4.3°", "c07_foot": "幾何高度（PyEphem 自算，含大氣折射）；貼地平線，很難看見",
        "c04_title": "同一把北斗", "c04_sub": "Stellarium 各文化的連線",
        "sib": "西伯利亞", "sib2": "Лось　駝鹿", "inu": "因紐特", "inu2": "Tukturjuit　馴鹿",
        "sam": "薩米", "sam2": "Fauna davgge", "sam3": "Fávdna 的弓：弓弧＋一支箭",
        "same": "勺形（兩個文化連線完全相同）",
        "arc_t": "大角星也拿著武器", "arc1": "薩米：Fávdna　獵人", "arc2": "古阿拉伯：al-Simāk al-Rāmiḥ　拿長矛的人",
        "c05_title": "這週末抬頭看", "c05_date": "2027/2/12（五）・台北・往北看",
        "p20": "20:00　鹿最完整（20:00–22:00）", "p23": "23:00　獵人、弓、北極星、鹿都在天上",
        "N": "北", "NE": "東北", "NW": "西北", "E": "東",
        "Polaris": "北極星", "Dipper": "弓（北斗）", "Cas": "仙后座", "Capella": "五車二", "Mirfak": "天船三",
        "Arcturus": "獵人（大角星）",
        "tip1": "大角星 22:01 從東北東升起，22:50 才過 10°", "tip2": "23:00 仙后座只剩 5–18°：北方與東北方要開闊",
        "tip3": "月亮 22:49 落下", "tip4": "高度：PyEphem 自算（含大氣折射）",
        "c06_title": "薩米星名小辭典", "c06_sub": "拼法照 Stellarium（Persson，據 Lundmark 1982）",
        "col1": "名字", "col2": "意思", "col3": "星",
        "rows": [
            ("Sarvvis", "公馴鹿（一說駝鹿）", "仙后＋英仙＋御夫"),
            ("Sarvvis／Áldu", "公／母馴鹿（IAU 2025）", "英仙 δ／ε"),
            ("Fávdna", "獵人", "大角星"),
            ("Fauna davgge", "Fávdna 的弓與箭", "北斗七星"),
            ("Boahjenásti", "撐住天空的星", "北極星"),
            ("Gállá", "老 Gállá（幫手）", "南河三（一說天狼、參宿七）"),
            ("Gallabarneck", "Gállá 的兒子們", "獵戶腰帶"),
            ("Cuoigahægjek", "滑雪的人", "北河二、北河三"),
            ("—", "獵犬群", "昴宿"),
            ("Miese-cora", "小鹿群", "昴宿"),
            ("—", "奔跑的人", "織女星"),
            ("Guovso-naste", "晨星", "牛郎星（或金星）"),
            ("Lodde-raiddaras", "鳥的路", "銀河"),
            ("Jakke-mærka", "年的記號", "銀河"),
        ],
        "say_t": "近似唸法（待母語者確認）",
        "say": "Sarvvis 薩爾-維斯　Áldu 阿爾-杜　Fávdna 法夫-德納　Boahjenásti 博阿-耶-納斯-提　Gállá 嘎-拉",
        "c06_foot": "Sarvvis、Áldu、Rangifer、Tarandus：IAU WGSN 2025/12/25",
        "tags": "#萬國星空　#師大天文社",
    },
    "en": {
        "c01_title": "Home of the Sámi: Sápmi", "c01_sub": "Hand-drawn sketch, not an exact map",
        "norway": "Norway", "sweden": "Sweden", "finland": "Finland", "russia": "Russia", "kola": "Kola Peninsula",
        "sapmi": "Sápmi", "arctic": "Arctic Circle 66.6°N", "kauto": "Kautokeino",
        "drum": "Sacred drum", "drum2": "our own sketch, not a museum drum", "drum_y1": "1609  Denmark–Norway: drums = sorcery",
        "drum_y2": "1700s  mass confiscation, burning", "drum_y3": "about 70 survive today",
        "c02_title": "The reindeer returns to the star map", "y1736": "1736–37", "y1736b": "Lapland",
        "y1743": "1743", "y1743b": "Le Monnier: le Renne",
        "y2025": "2025", "y2025b": "IAU",
        "polaris": "Polaris", "cas": "Cassiopeia", "per": "Perseus",
        "s_sarvvis": "Sarvvis (δ Per)", "s_aldu": "Áldu (ε Per)",
        "s_rang": "Rangifer (49 Cas)", "s_tar": "Tarandus (2 UMi)",
        "c03_title": "The arrow that must not fly", "c03_sub": "Stellarium sami; Turi 1910",
        "hunter": "Fávdna the Hunter (Arcturus)", "bow": "Bow (Big Dipper)",
        "pole": "Boahjenásti", "pole2": "the Sky Support (Polaris)",
        "deer": "Sarvvis (Cas–Per–Aur)", "hit": "Hit it = the sky falls, the world ends", "still": "So the bow stays drawn",
        "c07_title": "How high does Sirius get in Sápmi?", "south": "S",
        "kplace": "Kautokeino (69°N)", "kwhen": "Feb 12, 2027 20:43  Sirius on the meridian",
        "kalt": "max 4.3°", "c07_foot": "Altitude incl. refraction (PyEphem); hugging the horizon, hard to see",
        "c04_title": "One Big Dipper", "c04_sub": "Stellarium line figures",
        "sib": "Siberia", "sib2": "Лось  Elk", "inu": "Inuit", "inu2": "Tukturjuit  Caribou",
        "sam": "Sámi", "sam2": "Fauna davgge", "sam3": "Fávdna's bow: an arc + one arrow",
        "same": "Ladle (identical figures)",
        "arc_t": "Arcturus is armed too", "arc1": "Sámi: Fávdna, the hunter", "arc2": "Ancient Arabic: al-Simāk al-Rāmiḥ, the spear bearer",
        "c05_title": "Look up this weekend", "c05_date": "Fri Feb 12, 2027 · Taipei · facing north",
        "p20": "20:00  the reindeer at its best (20:00–22:00)", "p23": "23:00  hunter, bow, Polaris, reindeer all up",
        "N": "N", "NE": "NE", "NW": "NW", "E": "E",
        "Polaris": "Polaris", "Dipper": "Bow (Big Dipper)", "Cas": "Cassiopeia", "Capella": "Capella", "Mirfak": "Mirfak",
        "Arcturus": "Hunter (Arcturus)",
        "tip1": "Arcturus rises ENE at 22:01, above 10° only at 22:50", "tip2": "At 23:00 Cassiopeia is 5–18° up: clear N–NE horizon",
        "tip3": "Moonset 22:49", "tip4": "Altitudes: PyEphem (with refraction)",
        "c06_title": "Sámi star names", "c06_sub": "Spellings from Stellarium (Persson, after Lundmark 1982)",
        "col1": "Name", "col2": "Meaning", "col3": "Star",
        "rows": [
            ("Sarvvis", "bull reindeer (or elk)", "Cas + Per + Aur"),
            ("Sarvvis / Áldu", "bull / cow reindeer (IAU 2025)", "δ / ε Per"),
            ("Fávdna", "the hunter", "Arcturus"),
            ("Fauna davgge", "Fávdna's bow and arrow", "Big Dipper"),
            ("Boahjenásti", "the Sky Support", "Polaris"),
            ("Gállá", "old Gállá (a helper)", "Procyon (or Sirius, Rigel)"),
            ("Gallabarneck", "Gállá's sons", "Orion's Belt"),
            ("Cuoigahægjek", "the ski runners", "Castor, Pollux"),
            ("—", "pack of hunting dogs", "Pleiades"),
            ("Miese-cora", "calf herd", "Pleiades"),
            ("—", "the runner", "Vega"),
            ("Guovso-naste", "morning star", "Altair (or Venus)"),
            ("Lodde-raiddaras", "bird path", "Milky Way"),
            ("Jakke-mærka", "year mark", "Milky Way"),
        ],
        "say_t": "Approximate pronunciation (to be checked)",
        "say": "Sarvvis SAR-vis　Áldu AHL-du　Fávdna FAHV-dna　Boahjenásti BWAH-ye-nahs-ti　Gállá GAHL-lah",
        "c06_foot": "Sarvvis, Áldu, Rangifer, Tarandus: IAU WGSN, Dec 25, 2025",
        "tags": "#WorldSkyCultures #NTNUAstro",
    },
}


def tx(k):
    return TXT[LANG][k]


def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0, z=12, va="center"):
    ax.text(x, y, s, fontproperties=CB.FP, fontsize=size, color=c, ha=ha, va=va, weight=w,
            alpha=alpha, zorder=z)


def head(ax, title, sub=None):
    T(ax, 0, 0.90, title, 30, WHITE)
    if sub:
        T(ax, 0, 0.80, sub, 15, GREY, w="normal")


def star(ax, x, y, s=60, c=WHITE, z=8, glow=True, alpha=1.0):
    if glow:
        ax.scatter([x], [y], s=s * 5, c=c, alpha=0.15 * alpha, zorder=z - 1, lw=0)
    ax.scatter([x], [y], s=s, c=c, zorder=z, lw=0, alpha=alpha)


S = dict(G.load_stars(BASE))


# ══════════════════ C-A21-01 薩米在哪裡 ══════════════════
LON0, LAT0, KX, KY = 24.0, 64.0, 0.040, 0.085      # 手描示意：經度×cos65° 壓扁
COAST = [(41.4, 67.9), (39.0, 68.2), (36.0, 69.0), (33.5, 69.3), (31.0, 69.9), (28.5, 70.9), (25.8, 71.1),
         (23.5, 70.7), (19.0, 70.1), (16.0, 69.0), (13.5, 68.1), (14.5, 67.3), (12.5, 66.0), (11.0, 64.9),
         (10.0, 63.6), (8.0, 63.0), (5.5, 62.4), (5.0, 61.0), (5.1, 60.0), (5.6, 59.0), (7.0, 58.0),
         (8.5, 58.3), (10.5, 59.2), (11.2, 58.9), (12.0, 57.7), (12.8, 56.2), (14.2, 55.4), (16.4, 56.6),
         (16.6, 57.8), (18.0, 59.3), (17.2, 60.7), (17.4, 62.3), (19.0, 63.5), (21.2, 64.5), (22.2, 65.6),
         (24.2, 65.8), (25.4, 65.0), (24.5, 64.2), (21.5, 63.2), (21.4, 61.5), (22.3, 60.4), (25.0, 60.2),
         (27.8, 60.5), (30.0, 60.0), (36.0, 60.0), (36.0, 64.5), (34.8, 64.5), (32.5, 66.5), (36.0, 66.4),
         (40.5, 66.3)]
SAPMI = [(10.5, 63.5), (12.5, 62.0), (14.5, 62.0), (16.5, 64.5), (20.5, 65.8), (24.5, 66.8), (28.5, 67.0),
         (30.5, 67.0), (33.0, 66.6), (40.5, 66.3), (41.4, 67.9), (39.0, 68.2), (36.0, 69.0), (33.5, 69.3),
         (31.0, 69.9), (28.5, 70.9), (25.8, 71.1), (23.5, 70.7), (19.0, 70.1), (16.0, 69.0), (13.5, 68.1),
         (14.5, 67.3), (12.5, 66.0), (11.0, 64.9)]


def P(lon, lat):
    return (lon - LON0) * KX - 0.18, (lat - LAT0) * KY - 0.02


def c01_map(ax):
    head(ax, tx("c01_title"), tx("c01_sub"))
    ax.add_patch(CB.Polygon([P(*q) for q in COAST], closed=True, fc=LAND, ec="#9FB3D9", lw=1.6, zorder=2))
    ax.add_patch(CB.Polygon([P(*q) for q in SAPMI], closed=True, fc=AMBER, ec=AMBER, lw=1.2, alpha=.28, zorder=3))
    xs = [P(l, 66.56)[0] for l in (4, 43)]
    ax.plot(xs, [P(0, 66.56)[1]] * 2, c=BLUE, lw=1.6, ls=(0, (6, 5)), alpha=.85, zorder=4)
    T(ax, -0.97, P(0, 66.56)[1] + 0.035, tx("arctic"), 13, BLUE, ha="left", w="normal")
    kx, ky = P(23.04, 69.01)
    star(ax, kx, ky, 90, WHITE, glow=False, z=6)
    T(ax, kx - 0.03, ky - 0.04, tx("kauto"), 14, WHITE, ha="right", w="normal")
    T(ax, *P(9.5, 61.3), tx("norway"), 16, WHITE)
    T(ax, *P(15.5, 60.2), tx("sweden"), 16, WHITE)
    T(ax, *P(26.5, 62.6), tx("finland"), 16, WHITE)
    T(ax, *P(33.5, 62.0), tx("russia"), 16, WHITE)
    T(ax, *P(37.0, 67.45), tx("kola"), 13, WHITE, w="normal")
    T(ax, *P(19.0, 67.8), tx("sapmi"), 19, AMBER)


def c01_drum(ax):
    cx, cy, rx, ry = 0.60, -0.36, 0.15, 0.20
    ax.add_patch(CB.Ellipse((cx, cy), 2 * rx, 2 * ry, fc=SEA, ec="#D9B48A", lw=5, zorder=6))
    ax.add_patch(CB.Ellipse((cx, cy), 2 * rx - 0.03, 2 * ry - 0.03, fc="#C8A070", ec="none", alpha=.35, zorder=6))
    for dy in (0.07, -0.08):                        # 抽象分隔線（不臨摹任何鼓面圖案）
        w = rx * math.sqrt(max(0, 1 - (dy / ry) ** 2)) - 0.015
        ax.plot([cx - w, cx + w], [cy + dy, cy + dy], c="#8C4A2A", lw=2.2, zorder=7)
    ax.add_patch(CB.Circle((cx, cy), 0.035, fc="none", ec="#8C4A2A", lw=2.2, zorder=7))
    for k in range(8):
        a = math.radians(45 * k)
        ax.plot([cx + 0.045 * math.cos(a), cx + 0.07 * math.cos(a)],
                [cy + 0.045 * math.sin(a), cy + 0.07 * math.sin(a)], c="#8C4A2A", lw=2, zorder=7)
    # 火焰（燒毀）
    fl = [(-0.06, 0), (-0.045, 0.06), (-0.02, 0.03), (0.0, 0.10), (0.02, 0.03), (0.045, 0.07), (0.06, 0)]
    ax.add_patch(CB.Polygon([(cx + 0.12 + a, cy - ry - 0.02 + b) for a, b in fl], closed=True, fc=RED,
                            alpha=.75, ec="none", zorder=8))
    T(ax, cx, cy + ry + 0.05, tx("drum"), 18, "#D9B48A", z=13)
    T(ax, cx, cy - ry - 0.06, tx("drum2"), 10.5, GREY, w="normal", z=13)
    for i, k in enumerate(("drum_y1", "drum_y2", "drum_y3")):
        T(ax, cx, -0.78 - i * 0.065, tx(k), 13, WHITE if i < 2 else AMBER, w="normal", z=13)


# ══════════════════ C-A21-02 馴鹿回到星圖 ══════════════════
def polar_xy(hip, c=(0.38, -0.12), s=0.0125, rot=-30):
    """以北極為心的極方位等距小星圖（東在左），每度 s；rot 讓仙后、英仙落在右下"""
    ra, dec = S[hip][:2]
    r = (90 - dec) * s
    a = math.radians(ra + rot)
    return c[0] - r * math.sin(a), c[1] - r * math.cos(a)


CAS = [8886, 6686, 4427, 3179, 746]
PER = [14328, 15863, 17358, 18532]


def c02_base(ax):
    head(ax, tx("c02_title"))
    # 時間軸（左欄，直的）
    ax.plot([-0.70, -0.70], [0.60, -0.62], c=WHITE, lw=2, alpha=.5, zorder=3)
    # 小星圖
    for ring in (10, 20, 30, 40, 50):
        ax.add_patch(CB.Circle((0.38, -0.12), ring * 0.0125, fc="none", ec=WHITE, lw=.8, alpha=.12, zorder=2))
    star(ax, *polar_xy(11767), 90, WHITE)
    T(ax, polar_xy(11767)[0] + 0.03, polar_xy(11767)[1] + 0.055, tx("polaris"), 13, WHITE, w="normal", ha="left")
    for grp, lab, dxy in ((CAS, tx("cas"), (0.0, 0.07)), (PER, tx("per"), (-0.06, 0.08))):
        pts = [polar_xy(h) for h in grp]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=AMBER, lw=1.6, alpha=.6, zorder=4)
        for p in pts:
            star(ax, *p, 26, WHITE, glow=False)
        mx, my = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        T(ax, mx + dxy[0], my + dxy[1], lab, 12, GREY, w="normal")


def _year(i, y, k1, k2, col):
    def f(ax):
        yy = [0.52, 0.0, -0.52][i]
        ax.scatter([-0.70], [yy], s=220, c=col, zorder=6)
        T(ax, -0.62, yy + 0.03, tx(k1), 22, col, ha="left")
        T(ax, -0.62, yy - 0.05, tx(k2), 13, WHITE, ha="left", w="normal")
        if i == 1:                                  # 馴鹿座：北極星旁、仙后與北極之間（示意範圍）
            a, b = polar_xy(9763), polar_xy(5372)
            ax.add_patch(CB.Ellipse(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), 0.36, 0.17,
                                    angle=math.degrees(math.atan2(a[1] - b[1], a[0] - b[0])),
                                    fc=GREEN, alpha=.12, ec=GREEN, lw=1.4, ls=(0, (4, 4)), zorder=3))
        if i == 2:
            for hip, k, dx, dy, ha in ((17358, "s_sarvvis", 0.03, -0.035, "left"), (18532, "s_aldu", 0.03, -0.03, "left"),
                                       (9763, "s_rang", 0.0, 0.05, "center"), (5372, "s_tar", -0.05, -0.01, "right")):
                x, yv = polar_xy(hip)
                star(ax, x, yv, 70, AMBER)
                T(ax, x + dx, yv + dy, tx(k), 12.5, AMBER, ha=ha)
    return f


# ══════════════════ C-A21-03 不能射的那一箭 ══════════════════
PO = (0.0, 0.0)


def c03_hunt(ax):
    head(ax, tx("c03_title"), tx("c03_sub"))
    # 撐天：北極星往上一根柱子撐著天穹弧
    xs = [-0.9 + 1.8 * i / 100 for i in range(101)]
    ax.plot(xs, [0.60 - 0.12 * (x / 0.9) ** 2 for x in xs], c=BLUE, lw=2, alpha=.45, zorder=3)
    ax.plot([0, 0], [0.05, 0.60], c=WHITE, lw=3, alpha=.35, zorder=3)
    for r, al in ((0.10, .10), (0.06, .18)):
        ax.add_patch(CB.Circle(PO, r, fc=WHITE, ec="none", alpha=al, zorder=4))
    star(ax, *PO, 200, WHITE)
    T(ax, 0.0, -0.12, tx("pole"), 18, WHITE)
    T(ax, 0.0, -0.19, tx("pole2"), 13, GREY, w="normal")
    # 獵人（左下）＋弓
    hx, hy = -0.72, -0.40
    star(ax, hx, hy, 180, RED)
    T(ax, hx + 0.02, hy - 0.10, tx("hunter"), 14, RED)
    bx, by = -0.48, -0.20
    th = [math.radians(-70 + 140 * i / 40) for i in range(41)]
    a0 = math.radians(40)
    arc = [(bx + 0.16 * math.cos(t + a0) - 0.10, by + 0.16 * math.sin(t + a0) - 0.10) for t in th]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], c=GREEN, lw=4, zorder=6)
    ax.plot([arc[0][0], arc[-1][0]], [arc[0][1], arc[-1][1]], c=GREEN, lw=1.2, alpha=.7, zorder=6)
    T(ax, -0.62, -0.03, tx("bow"), 14, GREEN)
    # 鹿（右上）：Sarvvis 示意星點
    deer = [(0.42, 0.26), (0.50, 0.33), (0.58, 0.28), (0.66, 0.35), (0.74, 0.30), (0.62, 0.18), (0.70, 0.08),
            (0.80, 0.12), (0.76, -0.02)]
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 7), (6, 8)):
        ax.plot([deer[a][0], deer[b][0]], [deer[a][1], deer[b][1]], c=AMBER, lw=2.2, zorder=5)
    for p in deer:
        star(ax, *p, 40, WHITE, glow=False)
    T(ax, 0.62, 0.45, tx("deer"), 14, AMBER)


def c03_arrow(ax):
    x0, y0 = -0.40, -0.17
    x1, y1 = 0.55, 0.22
    n = 14
    for i in range(n):
        if i % 2:
            continue
        t0, t1 = i / n, (i + 1) / n
        ax.plot([x0 + (x1 - x0) * t0, x0 + (x1 - x0) * t1], [y0 + (y1 - y0) * t0, y0 + (y1 - y0) * t1],
                c=RED, lw=3, zorder=7)
    ax.annotate("", xy=(x1 + 0.03, y1 + 0.012), xytext=(x1 - 0.05, y1 - 0.02),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=3, mutation_scale=28), zorder=7)
    for s in (1, -1):
        ax.plot([-0.05, 0.05], [-0.05 * s, 0.05 * s], c=RED, lw=4, zorder=9)
    T(ax, 0.0, -0.50, tx("hit"), 19, RED)
    T(ax, 0.0, -0.60, tx("still"), 16, WHITE, w="normal")


# ══════════════════ C-A21-07 天狼星貼地平線 ══════════════════
HY7, KD = -0.30, 0.06


def c07_horizon(ax):
    head(ax, tx("c07_title"))
    ax.fill_between([-0.95, 0.95], [HY7, HY7], [HY7 - 0.07, HY7 - 0.07], color=EARTH, alpha=.9, zorder=3)
    ax.plot([-0.95, 0.95], [HY7, HY7], c="#D9B48A", lw=2.4, zorder=4)
    T(ax, 0.0, HY7 - 0.13, tx("south"), 22, "#D9B48A")
    for d in (5, 10, 15):
        y = HY7 + d * KD
        ax.plot([-0.95, 0.95], [y, y], c=WHITE, lw=0.8, alpha=.15, ls=(0, (3, 6)), zorder=2)
        T(ax, -0.92, y + 0.025, f"{d}°", 11, GREY, ha="left", w="normal")
    T(ax, 0.0, -0.74, tx("c07_foot"), 12, GREY, w="normal")


def c07_kauto(ax):
    y = HY7 + 4.3 * KD
    ax.plot([0, 0], [HY7, y], c=RED, lw=1.4, alpha=.6, zorder=4)
    star(ax, 0, y, 170, "#E8F0FF")
    T(ax, 0.0, y + 0.11, tx("kalt"), 22, RED)
    T(ax, 0.0, HY7 - 0.25, tx("kplace"), 17, WHITE)
    T(ax, 0.0, HY7 - 0.33, tx("kwhen"), 12, GREY, w="normal")


# ══════════════════ 星曆 ══════════════════
def altaz(hips, when, lat="25.0330", lon="121.5654", tz=8, temp=15, pres=1010):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = lat, lon; o.pressure, o.temp = pres, temp
    o.date = ephem.Date(ephem.Date(when) - tz * ephem.hour)
    out = {}
    for h in hips:
        b = ephem.FixedBody(); b._ra, b._dec, b._epoch = math.radians(S[h][0]), math.radians(S[h][1]), ephem.J2000
        b.compute(o)
        out[h] = (math.degrees(b.alt), math.degrees(b.az))
    return out


# ══════════════════ C-A21-04 同一把北斗（圖卡） ══════════════════
DIP = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
LADLE = [[67301, 65378, 62956, 59774, 58001, 53910, 54061, 59774]]
BOW = [[67301, 65378, 62956, 59774, 53910], [54061, 58001]]


def dip_xy(h, cx, cy, s):
    """北斗周圍的切平面投影（東在左），手柄朝右"""
    ra0, de0 = 193.0, 56.0
    ra, de = S[h][:2]
    a, d, a0, d0 = map(math.radians, (ra, de, ra0, de0))
    c = math.sin(d0) * math.sin(d) + math.cos(d0) * math.cos(d) * math.cos(a - a0)
    x = math.cos(d) * math.sin(a - a0) / c
    y = (math.cos(d0) * math.sin(d) - math.sin(d0) * math.cos(d) * math.cos(a - a0)) / c
    return cx - x * s, cy + y * s * 9 / 16          # 圖卡座標 x、y 單位不等長（9:16）


def dipper(ax, cx, cy, segs, col, s=0.62):
    for seg in segs:
        pts = [dip_xy(h, cx, cy, s) for h in seg]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=col, lw=2.6, zorder=5)
    for h in DIP:
        star(ax, *dip_xy(h, cx, cy, s), 34, WHITE, glow=False)


def c04_card(ax):
    T(ax, 0.5, 0.955, tx("c04_title"), 30, WHITE)
    T(ax, 0.5, 0.915, tx("c04_sub"), 13, GREY, w="normal")
    rows = [(0.80, "sib", "sib2", BLUE, LADLE), (0.62, "inu", "inu2", BLUE, LADLE), (0.42, "sam", "sam2", GREEN, BOW)]
    for y, k1, k2, col, segs in rows:
        ax.add_patch(CB.FancyBboxPatch((0.06, y - 0.075), 0.88, 0.15, boxstyle="round,pad=0.0,rounding_size=0.02",
                                       fc="#10162C", ec=col, lw=1.0, alpha=1, zorder=1))
        dipper(ax, 0.30, y - 0.005, segs, col)
        T(ax, 0.60, y + 0.025, tx(k1), 17, col, ha="left")
        T(ax, 0.60, y - 0.020, tx(k2), 12.5, WHITE, ha="left", w="normal")
        if k1 == "sam":
            T(ax, 0.60, y - 0.052, tx("sam3"), 11, GREY, ha="left", w="normal")
    T(ax, 0.5, 0.71, tx("same"), 11, GREY, w="normal")
    # 大角星
    T(ax, 0.5, 0.265, tx("arc_t"), 19, WHITE)
    star(ax, 0.5, 0.205, 150, RED)
    T(ax, 0.5, 0.155, tx("arc1"), 13, WHITE, w="normal")
    T(ax, 0.5, 0.125, tx("arc2"), 13, WHITE, w="normal")
    T(ax, 0.5, 0.040, tx("tags"), 12, WHITE, w="normal")


# ══════════════════ C-A21-05 這週末抬頭看（圖卡） ══════════════════
CASW = [8886, 6686, 4427, 3179, 746]
SARVA_LINES = [[8886, 6686, 4427, 3179, 746], [6686, 14328, 15863, 14576], [15863, 17358, 18532, 18246],
               [17358, 24608, 25428], [24608, 23767, 23015]]


def sky_panel(ax, y0, y1, az0, az1, alt1, title, A, labels, lines, dirs):
    x0, x1 = 0.05, 0.95
    ax.add_patch(CB.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.0,rounding_size=0.02",
                                   fc="#10162C", ec=WHITE, lw=1.0, alpha=1, zorder=1))
    gy = y0 + 0.035

    def Pp(alt, az):
        d = (az - az0) % 360
        return x0 + (x1 - x0) * d / ((az1 - az0) % 360), gy + (y1 - 0.03 - gy) * alt / alt1

    ax.fill_between([x0 + 0.003, x1 - 0.003], [y0 + 0.003] * 2, [gy] * 2, color=EARTH, zorder=2)
    ax.plot([x0, x1], [gy, gy], c="#D9B48A", lw=1.6, zorder=3)
    for lab, az in dirs:
        x, _ = Pp(0, az)
        T(ax, x, gy - 0.017, lab, 11, "#D9B48A")
    T(ax, 0.5, y1 + 0.020, title, 14, WHITE)
    inside = lambda h: -0.5 <= A[h][0] <= alt1 and (A[h][1] - az0) % 360 <= (az1 - az0) % 360
    for seg, col in lines:                       # 出框（太高或方位超出）的點把線段切斷，不畫跨框假線
        for a, b in zip(seg, seg[1:]):
            if inside(a) and inside(b):
                pa, pb = Pp(*A[a]), Pp(*A[b])
                ax.plot([pa[0], pb[0]], [pa[1], pb[1]], c=col, lw=1.6, zorder=4)
    for h, (alt, az) in A.items():
        if not inside(h):
            continue
        x, y = Pp(alt, az)
        star(ax, x, y, 30 if h not in labels else 60, WHITE, glow=h in labels)
    for h, (lab, col, dx, dy, ha) in labels.items():
        alt, az = A[h]
        if alt < -0.5:
            continue
        x, y = Pp(alt, az)
        T(ax, x + dx, y + dy, lab, 11.5, col, ha=ha)
        T(ax, x + dx, y + dy - 0.016, f"{alt:.0f}°", 9.5, GREY, ha=ha, w="normal")


def c05_card(ax):
    T(ax, 0.5, 0.955, tx("c05_title"), 30, WHITE)
    T(ax, 0.5, 0.920, tx("c05_date"), 14, GREY, w="normal")
    hips = set(h for seg in SARVA_LINES + BOW for h in seg) | {11767, 69673}
    dirs = [(tx("NW"), 315), (tx("N"), 0), (tx("NE"), 45), (tx("E"), 90)]
    for (y0, y1, when, key, extra) in ((0.52, 0.875, "2027/2/12 20:00", "p20", False),
                                       (0.13, 0.485, "2027/2/12 23:00", "p23", True)):
        A = altaz(sorted(hips), when)
        lab = {11767: (tx("Polaris"), WHITE, 0.0, 0.03, "center"),
               54061: (tx("Dipper"), GREEN, 0.0, 0.032, "center"),
               3179: (tx("Cas"), AMBER, 0.0, -0.040, "center"),
               24608: (tx("Capella"), AMBER, 0.0, 0.030, "center"),
               15863: (tx("Mirfak"), AMBER, 0.035, 0.0, "left")}
        if extra:
            lab[69673] = (tx("Arcturus"), RED, -0.02, 0.03, "right")
        if extra:
            lab[3179] = (tx("Cas"), AMBER, 0.05, 0.012, "left")
        sky_panel(ax, y0, y1, 290, 100, 78, tx(key), A, lab,
                  [(s, AMBER) for s in SARVA_LINES] + [(s, GREEN) for s in BOW], dirs)
    for i, (k, col) in enumerate((("tip1", WHITE), ("tip2", WHITE), ("tip3", WHITE), ("tip4", GREY))):
        T(ax, 0.5, 0.100 - i * 0.019, tx(k), 11 if col == WHITE else 9.5, col, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 12, WHITE, w="normal")


# ══════════════════ C-A21-06 薩米星名小辭典（圖卡） ══════════════════
def c06_card(ax):
    T(ax, 0.5, 0.955, tx("c06_title"), 30, WHITE)
    T(ax, 0.5, 0.921, tx("c06_sub"), 11.5, GREY, w="normal")
    xs = (0.06, 0.38, 0.66)
    y = 0.875
    for x, k in zip(xs, ("col1", "col2", "col3")):
        T(ax, x, y, tx(k), 13, AMBER, ha="left")
    ax.plot([0.05, 0.95], [y - 0.017, y - 0.017], c=AMBER, lw=1, alpha=.6)
    rows = tx("rows")
    dy = 0.047
    for i, (a, b, c) in enumerate(rows):
        yy = y - 0.048 - i * dy
        if i % 2 == 0:
            ax.add_patch(CB.Rectangle((0.05, yy - dy / 2), 0.90, dy, fc="#10162C", ec="none", zorder=0))
        T(ax, xs[0], yy, a, 12.5, WHITE, ha="left")
        T(ax, xs[1], yy, b, 11.5, WHITE, ha="left", w="normal")
        T(ax, xs[2], yy, c, 11.0 if len(c) < 10 else 9.0, GREY, ha="left", w="normal")
    yb = y - 0.048 - len(rows) * dy - 0.010
    T(ax, 0.5, yb, tx("say_t"), 12, AMBER)
    say = tx("say").split("　")
    T(ax, 0.5, yb - 0.030, "　".join(say[:3]), 10, WHITE, w="normal")
    T(ax, 0.5, yb - 0.055, "　".join(say[3:]), 10, WHITE, w="normal")
    T(ax, 0.5, yb - 0.088, tx("c06_foot"), 9.5, GREY, w="normal")
    T(ax, 0.5, 0.018, tx("tags"), 12, WHITE, w="normal")


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        CB.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    print("── C-A21 概念圖 ──")
    CB.emit("", [("地圖", c01_map), ("神鼓", c01_drum)], title="C-A21-01_薩米在哪裡")
    CB.emit("", [("1736", lambda ax: (c02_base(ax), _year(0, 0, "y1736", "y1736b", WHITE)(ax))),
                 ("1743", _year(1, 0, "y1743", "y1743b", GREEN)),
                 ("2025", _year(2, 0, "y2025", "y2025b", AMBER))], title="C-A21-02_馴鹿回到星圖")
    CB.emit("", [("狩獵", c03_hunt), ("箭", c03_arrow)], title="C-A21-03_不能射的那一箭")
    CB.emit("", [("地平線", c07_horizon), ("Kautokeino", c07_kauto)], title="C-A21-07_天狼星貼地平線")
    for fn, name in ((c04_card, "C-A21-04_同一把北斗_圖卡.png"), (c05_card, "C-A21-05_這週末抬頭看_圖卡.png"),
                     (c06_card, "C-A21-06_薩米星名小辭典_圖卡.png")):
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", name, transparent=False)


if __name__ == "__main__":
    main()
