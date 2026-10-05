# -*- coding: utf-8 -*-
"""A-11 阿努塔｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A11-01_阿努塔地圖       → 逐字稿 02 鏡（島嶼層→祖先層）
  C-A11-02_Manu的翅膀       → 逐字稿 06 鏡（星點層→翅膀層→傳說層）
  C-A11-03_星路             → 逐字稿 14 鏡（海面層→星路層）
  C-A11-04_阿努塔的生活星空 → 逐字稿 04 鏡（9:16 圖卡，可存圖）
  C-A11-05_同一個字         → 逐字稿 15 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-11_阿努塔/_概念圖/

來源：Feinberg, R. 1988. Polynesian Seafaring and Navigation: Ocean Travel in Anutan Culture and Society
      （Stellarium skycultures/anutan＝Bucur 2021 依此書數位化）；Feinberg, R. 1995. Christian Polynesians
      and Pagan Spirits: Anuta, Solomon Islands. JPS 104(3):267–302（Manu 的斷翼、Taro＝心宿二）；
      Firth, R. 1954. Anuta and Tikopia: Symbiotic Elements in Social Organization. JPS 63(2):87–132（星路九顆星）；
      Stellarium skycultures/bugis（Ohashi & Orchiston 2021：Manu'＝雞＝老人星、天狼星、南河三）；
      Blust, Austronesian Comparative Dictionary：*manuk（雞；巴賽語 manuk）。
      地圖＝經緯度實際位置（等距圓柱投影，島形示意）；距離為大圓距離（自算）；
      星的方位、仰角以 PyEphem 自算（阿努塔 11.611°S、169.850°E，UTC+11）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-11_阿努塔/_概念圖")
C.set_base(OUT)
RED, GREY, SEA = "#FF6B6B", "#7C8BA8", "#2A4A7A"
S = None


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371.0 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) *
                                            math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


# ══════════════════════ C-A11-01 阿努塔地圖 ══════════════════════
P = {   # (lat, lon)；經度一律用 0–360（東經）
    "Anuta": (-11.611, 169.850), "Tikopia": (-12.296, 168.832), "Patutaka": (-11.917, 170.200),
    "Nendo": (-10.72, 165.95), "Vanikoro": (-11.64, 166.90),
    "Honiara": (-9.43, 159.95), "Espiritu Santo": (-15.40, 166.90), "Efate": (-17.73, 168.32),
    "Viti Levu": (-17.80, 178.00), "Vanua Levu": (-16.60, 179.30),
    "ʻUvea": (-13.28, 183.83), "Futuna": (-14.29, 181.88),
    "Tongatapu": (-21.14, 184.80), "Vavaʻu": (-18.65, 186.02), "Savaiʻi": (-13.62, 187.55),
}
LONC, LATC, SC = 174.0, -14.0, 0.056
COSL = math.cos(math.radians(14.0))


def mp(lat, lon):
    return (lon - LONC) * COSL * SC, (lat - LATC) * SC


def c01_islands(ax):
    T(ax, 0.0, 0.92, "阿努塔：所羅門群島東端", 31, WHITE)
    T(ax, 0.0, 0.845, "島的位置依實際經緯度；島形示意", 17, GREY, w="normal")
    for lat in (-8, -12, -16, -20):
        a, b = mp(lat, 160.0), mp(lat, 189.0)
        ax.plot([a[0], b[0]], [a[1], a[1]], c=WHITE, lw=0.8, alpha=.18, ls=(0, (4, 5)), zorder=2)
        T(ax, b[0] - 0.01, a[1] + 0.022, f"{abs(lat)}°S", 11, GREY, w="normal", ha="right")
    big = {"Anuta": 120, "Tikopia": 90, "Patutaka": 40, "Nendo": 260, "Vanikoro": 160,
           "Honiara": 300, "Espiritu Santo": 480, "Efate": 260, "Viti Levu": 650, "Vanua Levu": 520,
           "ʻUvea": 120, "Futuna": 90, "Tongatapu": 200, "Vavaʻu": 150, "Savaiʻi": 380}
    for nm, (lat, lon) in P.items():
        x, y = mp(lat, lon)
        col = AMBER if nm == "Anuta" else GREY
        ax.scatter([x], [y], s=big[nm], c=col, alpha=1 if nm == "Anuta" else .7, zorder=8, lw=0)
    lab = {  # 名稱, dx, dy, 字級, 顏色, ha
        "Anuta": ("阿努塔", 0.025, 0.04, 22, AMBER, "left"),
        "Tikopia": ("", 0, 0, 1, GREY, "left"),
        "Nendo": ("聖克魯斯群島", 0.0, 0.06, 14, GREY, "center"),
        "Honiara": ("所羅門群島（Honiara）", 0.0, 0.055, 14, GREY, "center"),
        "Espiritu Santo": ("萬那杜", 0.0, -0.07, 15, GREY, "center"),
        "Viti Levu": ("斐濟", 0.0, -0.07, 15, GREY, "center"),
        "ʻUvea": ("ʻUvea", 0.035, 0.0, 15, WHITE, "left"),
        "Tongatapu": ("東加", 0.035, -0.02, 16, WHITE, "left"),
        "Savaiʻi": ("薩摩亞", 0.0, 0.06, 14, GREY, "center"),
    }
    for nm, (txt, dx, dy, fs, col, ha) in lab.items():
        if not txt:
            continue
        x, y = mp(*P[nm])
        T(ax, x + dx, y + dy, txt, fs, col, ha=ha, w="bold" if col != GREY else "normal")
    # 放大框：阿努塔、Tikopia、Patutaka
    bx, by, bw, bh = -0.92, -0.86, 0.80, 0.62
    ax.add_patch(C.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.0,rounding_size=0.03",
                                  fc="#10172E", ec=GREY, lw=1.2, alpha=1.0, zorder=10))
    T(ax, bx + 0.03, by + bh - 0.045, "放大", 13, GREY, w="normal", ha="left")
    ic, kx = (-11.95, 169.70), 0.0035                  # 放大框中心經緯度、每公里
    cx0, cy0 = bx + bw / 2, by + bh / 2 - 0.02

    def mi(lat, lon):
        dx = (lon - ic[1]) * 111.32 * math.cos(math.radians(lat))
        dy = (lat - ic[0]) * 110.57
        return cx0 + dx * kx, cy0 + dy * kx
    for nm, s_, col in (("Anuta", 70, AMBER), ("Tikopia", 160, WHITE), ("Patutaka", 30, GREY)):
        x, y = mi(*P[nm])
        ax.scatter([x], [y], s=s_, c=col, zorder=12, lw=0)
    ax_, ay_ = mi(*P["Anuta"]); tx_, ty_ = mi(*P["Tikopia"]); px_, py_ = mi(*P["Patutaka"])
    ax.plot([ax_, tx_], [ay_, ty_], c=WHITE, lw=1.2, alpha=.5, ls=(0, (3, 3)), zorder=11)
    ax.plot([ax_, px_], [ay_, py_], c=WHITE, lw=1.2, alpha=.5, ls=(0, (3, 3)), zorder=11)
    T(ax, ax_ - 0.02, ay_ + 0.045, "阿努塔 0.37 km²・約 300 人", 13.5, AMBER, ha="center")
    T(ax, tx_, ty_ - 0.05, "Tikopia", 13, WHITE)
    T(ax, (ax_ + tx_) / 2 - 0.02, (ay_ + ty_) / 2 + 0.03,
      f"{gc_km(P['Anuta'], P['Tikopia']):.0f} km", 12, WHITE, w="normal", ha="right")
    T(ax, px_, py_ - 0.045, "Patutaka（無人島）", 12, GREY, w="normal", ha="center")
    T(ax, px_, py_ - 0.085, "一年划去一兩趟抓海鳥", 11, GREY, w="normal", ha="center")
    T(ax, (ax_ + px_) / 2 + 0.035, (ay_ + py_) / 2 + 0.02,
      f"{gc_km(P['Anuta'], P['Patutaka']):.0f} km", 12, WHITE, w="normal", ha="left")
    # 比例尺（主圖）
    sx0, sy = 0.30, -0.80
    L = 1000 / 111.2 * SC
    ax.plot([sx0, sx0 + L], [sy, sy], c=WHITE, lw=2.0, alpha=.7)
    T(ax, sx0 + L / 2, sy + 0.035, "1000 km", 12, GREY, w="normal")
    T(ax, 0.0, -0.93, "人在美拉尼西亞的所羅門群島，說的是玻里尼西亞語", 15, GREY, w="normal")


def c01_ancestors(ax):
    a = mp(*P["Anuta"])
    for nm, col in (("Tongatapu", GREEN), ("ʻUvea", GREEN)):
        b = mp(*P[nm])
        C.arrow(ax, (a[0] + 0.02, a[1] - 0.005), b, c=col, lw=3.0, alpha=.95, style="-|>")
        km = gc_km(P["Anuta"], P[nm])
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = (-0.13, -0.03) if nm == "Tongatapu" else (0.03, 0.05)
        T(ax, mx + dx, my + dy, f"{km:,.0f} km", 15, col)
    ax.add_patch(C.FancyBboxPatch((0.05, 0.40), 0.86, 0.27, boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=GREEN, lw=1.4, zorder=4))
    T(ax, 0.48, 0.60, "島上的口傳：", 16, GREEN)
    T(ax, 0.48, 0.535, "大約十五代以前，", 16, WHITE, w="normal")
    T(ax, 0.48, 0.47, "祖先從東加和 ʻUvea 駕船過來", 16, WHITE, w="normal")


# ══════════════════════ C-A11-02 Manu 的翅膀 ══════════════════════
MANU = {"天狼星": 32349, "老人星": 30438, "南河三": 37279, "α Pic": 32607}


def sep(a, b):
    ra1, d1 = (math.radians(x) for x in S[a][:2])
    ra2, d2 = (math.radians(x) for x in S[b][:2])
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def proj(h, c0=(104.0, -28.3), k=0.0172):
    """以 (RA, Dec) c0 為中心的方位等距投影；東在左、北在上"""
    ra, dec = math.radians(S[h][0]), math.radians(S[h][1])
    r0, d0 = math.radians(c0[0]), math.radians(c0[1])
    cosc = math.sin(d0) * math.sin(dec) + math.cos(d0) * math.cos(dec) * math.cos(ra - r0)
    c = math.acos(max(-1.0, min(1.0, cosc)))
    kk = c / math.sin(c) if c > 1e-9 else 1.0
    x = kk * math.cos(dec) * math.sin(ra - r0)
    y = kk * (math.cos(d0) * math.sin(dec) - math.sin(d0) * math.cos(dec) * math.cos(ra - r0))
    return -math.degrees(x) * k, math.degrees(y) * k + 0.13


def c02_stars(ax):
    T(ax, 0.0, 0.92, "Manu：天上最大的鳥", 31, AMBER)
    T(ax, 0.0, 0.845, "Feinberg 1988；東在左、北在上", 17, GREY, w="normal")
    for nm, h in MANU.items():
        x, y = proj(h)
        v = S[h][2]
        ax.scatter([x], [y], s=max(40, (6.0 - v) ** 2.2 * 26), c=WHITE, zorder=9, lw=0)
        ax.scatter([x], [y], s=max(40, (6.0 - v) ** 2.2 * 26) * 4, c=WHITE, alpha=.12, zorder=8, lw=0)
    lab = {"天狼星": (0.07, 0.0, "left"), "老人星": (0.07, 0.0, "left"), "南河三": (-0.07, 0.0, "right"),
           "α Pic": (-0.05, -0.01, "right")}
    for nm, (dx, dy, ha) in lab.items():
        x, y = proj(MANU[nm])
        T(ax, x + dx, y + dy, nm, 16, WHITE, ha=ha, w="normal")


def c02_wings(ax):
    s_, c_, p_, a_ = (proj(MANU[n]) for n in ("天狼星", "老人星", "南河三", "α Pic"))
    ax.plot([p_[0], s_[0], c_[0], a_[0]], [p_[1], s_[1], c_[1], a_[1]], c=AMBER, lw=3.4, alpha=.95,
            zorder=7)
    wn, we = sep(MANU["天狼星"], MANU["南河三"]), sep(MANU["天狼星"], MANU["老人星"])
    for (a, b), txt in (((s_, p_), f"北翼 {wn:.1f}°"), ((s_, c_), f"東翼 {we:.1f}°")):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        T(ax, mx + 0.06, my, txt, 20, AMBER, ha="left")
    T(ax, s_[0] + 0.07, s_[1] + 0.07, "身體", 18, AMBER, ha="left")
    T(ax, c_[0] + 0.07, c_[1] - 0.055, "Te Kapakau Tonga", 14, AMBER, ha="left", w="normal")
    T(ax, p_[0] - 0.07, p_[1] - 0.055, "Te Kapakau Pakatokerau", 14, AMBER, ha="right", w="normal")
    T(ax, a_[0] - 0.05, a_[1] - 0.06, "東翼的領路星", 14, WHITE, ha="right", w="normal")


def c02_legend(ax):
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.93), 1.76, 0.25,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.4, zorder=4))
    T(ax, 0.0, -0.75, "為了女神 Taro（心宿二），Manu 和 Motikitiki 打了一架，", 17, WHITE)
    T(ax, 0.0, -0.82, "北翼被打斷——所以比東翼短", 17, WHITE)
    T(ax, 0.0, -0.89, "Feinberg 1995；Motikitiki＝把阿努塔從海底拉上來的半神", 12.5, GREY, w="normal")


# ══════════════════════ C-A11-03 星路 ══════════════════════
SGR = {"γ": 88635, "λ": 90496, "σ": 92855, "π": 94141, "ρ": 95865, "ε": 90185}   # Stellarium anutan 009 的六顆
HZ, SD = -0.05, 0.026           # 地平線 y、每度
AZ0 = 235.0                      # 畫面中心方位（Tikopia）
WHEN = "2026/11/20 20:00"


def sgr_altaz(when=WHEN):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = "-11.611", "169.850"; o.pressure = 0
    o.date = ephem.Date(ephem.Date(when) - 11 * ephem.hour)
    out = {}
    for nm, h in SGR.items():
        ra, dec, v = S[h]
        b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec)
        b._epoch = ephem.J2000; b.compute(o)
        out[nm] = (math.degrees(b.alt), math.degrees(b.az), v)
    return out


def axy(alt, az):
    return (az - AZ0) * SD, HZ + alt * SD


def c03_sea(ax):
    T(ax, 0.0, 0.92, "從阿努塔往 Tikopia", 32, WHITE)
    T(ax, 0.0, 0.845, f"11 月 20 日晚上八點・面向西南", 18, GREY, w="normal")
    ax.add_patch(C.Rectangle((-0.95, -0.95), 1.9, HZ + 0.95, fc=C.BG, ec="none", zorder=3))
    ax.plot([-0.94, 0.94], [HZ, HZ], c=WHITE, lw=2.2, alpha=.7, zorder=5)
    for k in range(2):
        C.water(ax, y=HZ - 0.28 - k * 0.06, x0=-0.94, x1=0.94, c=BLUE, rows=1,
                amp=0.010, freq=16 + 5 * k, phase=k * 1.3)
    for az in (210, 225, 240, 255, 270):
        x = (az - AZ0) * SD
        ax.plot([x, x], [HZ - 0.018, HZ + 0.018], c=WHITE, lw=1.4, alpha=.6, zorder=6)
        lab = {225: "西南", 270: "正西"}.get(az, f"{az}°")
        T(ax, x, HZ - 0.12, lab, 15 if az in (225, 270) else 13, WHITE if az in (225, 270) else GREY,
          w="bold" if az in (225, 270) else "normal")
    br = bearing(P["Anuta"], P["Tikopia"])
    x = (br - AZ0) * SD
    ax.plot([x, x], [HZ, HZ + 0.62], c=AMBER, lw=1.4, ls=(0, (5, 5)), alpha=.55, zorder=6)
    ax.add_patch(C.Polygon([(x - 0.03, HZ - 0.005), (x + 0.03, HZ - 0.005), (x, HZ + 0.035)],
                           closed=True, fc=AMBER, ec="none", alpha=.9, zorder=7))
    T(ax, x, HZ - 0.20, f"▲ Tikopia 在這個方向（{gc_km(P['Anuta'], P['Tikopia']):.0f} 公里外）", 15, AMBER)
    for alt in (10, 20, 30):
        y = HZ + alt * SD
        ax.plot([-0.93, -0.90], [y, y], c=WHITE, lw=1.2, alpha=.5)
        T(ax, -0.885, y, f"{alt}°", 12, GREY, w="normal", ha="left")


def c03_path(ax):
    A = sgr_altaz()
    pts = {nm: axy(alt, az) for nm, (alt, az, v) in A.items()}
    for a, b in (("γ", "λ"), ("λ", "σ"), ("σ", "π"), ("σ", "ρ"), ("σ", "ε"), ("ε", "γ")):
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], c=PURPLE, lw=2.2, alpha=.85, zorder=8)
    for nm, (alt, az, v) in A.items():
        x, y = pts[nm]
        ax.scatter([x], [y], s=max(30, (6.0 - v) ** 2.2 * 22), c=WHITE, zorder=9, lw=0)
    # 落下的軌跡（每 15 分鐘）：σ 星
    import ephem
    tr = [sgr_altaz(ephem.Date(ephem.Date(WHEN) + i * 15 * ephem.minute))["σ"] for i in range(0, 5)]
    xs = [axy(a, z)[0] for a, z, _ in tr]; ys = [axy(a, z)[1] for a, z, _ in tr]
    ax.plot(xs, ys, c=PURPLE, lw=1.2, ls=(0, (2, 4)), alpha=.6, zorder=7)
    top = max(p[1] for p in pts.values())
    cx = sum(p[0] for p in pts.values()) / len(pts)
    T(ax, cx, top + 0.16, "Te Paka Poi Ika Tapu", 22, PURPLE)
    T(ax, cx, top + 0.085, "星路上的一條魚（可能是人馬座）", 16, PURPLE, w="normal")
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.93), 1.76, 0.36, boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=PURPLE, lw=1.4, zorder=4))
    T(ax, 0.0, -0.635, "星路：一顆接一顆的領路星", 18, WHITE)
    T(ax, 0.0, -0.71, "船頭對準貼著海面的星；它升高（或沉下）了，就換下一顆", 14.5, WHITE, w="normal")
    T(ax, 0.0, -0.78, "Firth 1954：Tikopia 往阿努塔的星路（Kavenga）共九顆星", 14.5, WHITE, w="normal")
    T(ax, 0.0, -0.85, "阿努塔叫主要的領路星 kaavenga（載著船走的）；Feinberg 1988：往 Tikopia 的星路上有這條魚", 12, GREY, w="normal")
    T(ax, 0.0, -0.90, "（星的位置：PyEphem 自算）", 11.5, GREY, w="normal")


# ══════════════════════ C-A11-04 阿努塔的生活星空（9:16 圖卡） ══════════════════════
ROWS4 = [  # (原文, 意思, 第二行：星｜用途, 顏色)
    ("Manu", "飛翔的鳥", "天狼＝身體、老人星＝東翼、南河三＝北翼｜天上最大；北翼被打斷", AMBER),
    ("Te Aamonga", "扁擔", "河鼓三星（華人民間也叫扁擔星）｜挑芋頭、椰子", GREEN),
    ("Taro", "芋頭", "天蠍座頭部｜心宿二＝它的莖 Na Kau", GREEN),
    ("Te Angaanga", "火鉗", "畢宿｜在地爐裡夾熱石、炭和食物", RED),
    ("Te Kope", "竹子", "天鶴座｜做釣竿、桅杆、帆桁、舷外浮桿", BLUE),
    ("Toki", "石錛", "海豚座（另說大角星）｜削獨木舟、蓋房子", BLUE),
    ("Te Kupenga", "漁網", "南十字＋網柄（南門二、馬腹一）\n其中的十字 1916 年後改叫 Te Rakau Tapu，神聖的木頭", BLUE),
    ("Te Rua Tangata", "兩個人", "南門二、馬腹一｜網柄的另一個名字", RED),
    ("Kaavei", "章魚腳", "白羊座三顆", PURPLE),
    ("Te Paka Poi Ika Tapu", "像鰺魚的魚", "人馬座（不確定）｜往 Tikopia 的星路上", PURPLE),
    ("Ara Toru", "三星之路", "獵戶腰帶", WHITE),
    ("Taki Mua／Taki Roto", "前面／中間的領路星", "飛馬座／壁宿二一帶", WHITE),
    ("Matariki", "小臉（小眼睛）", "昴宿", AMBER),
    ("Te Ao Rere／Te Ao Toka", "奔跑的雲／靜止的雲", "大／小麥哲倫雲", WHITE),
]


def c04_card(ax):
    ax.text(0.5, 0.947, "阿努塔的生活星空", fontproperties=C.FP, fontsize=28, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.907, "0.37 km² 的島，天上掛著整座島的一天", fontproperties=C.FP,
            fontsize=14, color=GREY, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.880, 0.880], c=WHITE, lw=1.0, alpha=.4)
    y = 0.872
    for nat, zh, line2, col in ROWS4:
        n2 = line2.count("\n") + 1
        h = 0.026 + 0.019 * n2 + 0.006
        ax.text(0.04, y - 0.016, nat, fontproperties=C.FP, fontsize=13, color=col, ha="left",
                va="center", weight="bold")
        ax.text(0.96, y - 0.016, zh, fontproperties=C.FP, fontsize=13, color=col, ha="right",
                va="center", weight="bold")
        ax.text(0.04, y - 0.031 - 0.0095 * n2, line2, fontproperties=C.FP, fontsize=11, color=WHITE,
                ha="left", va="center", linespacing=1.25, alpha=.9)
        y -= h
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
    ax.text(0.5, 0.078, "Feinberg 1988《Polynesian Seafaring and Navigation》（Stellarium 依此數位化）",
            fontproperties=C.FP, fontsize=10.5, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.058, "Manu 的斷翼：Feinberg 1995", fontproperties=C.FP, fontsize=10.5, color=GREY,
            ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


# ══════════════════════ C-A11-05 同一個字（9:16 圖卡） ══════════════════════
ROWS5 = [  # (星, 阿努塔, 東加（上集）, 說明)
    ("昴宿", "Matariki", "Mataliki", "毛利 Matariki、夏威夷 Makaliʻi"),
    ("獵戶腰帶", "Ara Toru\n三星之路", "ʻAlotolu\n一船三人", "toru＝tolu＝三"),
    ("南門二＋馬腹一", "Te Rua Tangata\n兩個人", "Ongo Tangata\n兩個人", "同一對星、同一個意思"),
    ("翅膀", "Kapakau\n（Manu 的翅膀）", "Kapakau ʻo Tafahi\n（Tafahi 的翅膀）", "kapakau＝翅膀"),
    ("麥哲倫雲", "Te Ao Rere／Te Ao Toka\n奔跑的雲／靜止的雲", "Maʻafulele／Maʻafutoka\n跑動的火／躺著的火",
     "rere＝lele（跑、飛）；兩邊的 toka（躺著、不動）"),
]


def c05_card(ax):
    ax.text(0.5, 0.947, "同一個字", fontproperties=C.FP, fontsize=30, color=WHITE,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.905, "老人星＋天狼星＋南河三", fontproperties=C.FP, fontsize=15, color=GREY,
            ha="center", va="center")
    # 上半：Manu 樹
    boxes = [(0.5, 0.835, "南島語祖語  *manuk", "雞；鳥", AMBER),
             (0.20, 0.715, "巴賽語（北台灣）", "manuk", WHITE),
             (0.50, 0.715, "布吉斯語（蘇拉威西）", "manuʼ 雞", WHITE),
             (0.80, 0.715, "玻里尼西亞語", "manu 鳥", WHITE)]
    for x, y, t1, t2, col in boxes:
        ax.add_patch(C.FancyBboxPatch((x - 0.14, y - 0.035), 0.28, 0.07,
                                      boxstyle="round,pad=0.005,rounding_size=0.015",
                                      fc="#1B2240", ec=col, lw=1.2, zorder=3))
        ax.text(x, y + 0.012, t1, fontproperties=C.FP, fontsize=11.5, color=col, ha="center",
                va="center", zorder=4)
        ax.text(x, y - 0.015, t2, fontproperties=C.FP, fontsize=13, color=WHITE, ha="center",
                va="center", weight="bold", zorder=4)
    for x in (0.20, 0.50, 0.80):
        C.arrow(ax, (x, 0.752), (0.5, 0.799), c=GREY, lw=1.4, alpha=.8, style="-|>")
    ax.text(0.5, 0.640, "布吉斯人：Manu'＝雞", fontproperties=C.FP, fontsize=15, color=AMBER,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.612, "阿努塔人：Manu＝飛翔的鳥", fontproperties=C.FP, fontsize=15, color=AMBER,
            ha="center", va="center", weight="bold")
    ax.text(0.5, 0.584, "兩地相隔 5,600 公里，同三顆星、同一個字", fontproperties=C.FP, fontsize=12.5,
            color=GREY, ha="center", va="center")
    # 下半：阿努塔 vs 東加
    ax.plot([0.03, 0.97], [0.555, 0.555], c=WHITE, lw=1.0, alpha=.4)
    ax.text(0.5, 0.530, "阿努塔的祖先從東加和 ʻUvea 來（口傳）：星名裡很多字相通", fontproperties=C.FP,
            fontsize=14, color=GREEN, ha="center", va="center", weight="bold")
    X0, X1, X2 = 0.035, 0.26, 0.625
    y = 0.495
    for x, txt in ((X0, "星"), (X1, "阿努塔"), (X2, "東加（上集）")):
        ax.text(x, y, txt, fontproperties=C.FP, fontsize=12.5, color=GREY, ha="left", va="center",
                weight="bold")
    y = 0.475
    for star, an, to, note in ROWS5:
        n = max(an.count("\n"), to.count("\n")) + 1
        h = 0.021 * n + 0.034
        yc = y - 0.008 - 0.0105 * n
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=0.6, alpha=.18)
        ax.text(X0, yc, star, fontproperties=C.FP, fontsize=12, color=WHITE, ha="left", va="center")
        ax.text(X1, yc, an, fontproperties=C.FP, fontsize=11.5, color=AMBER, ha="left", va="center",
                linespacing=1.2)
        ax.text(X2, yc, to, fontproperties=C.FP, fontsize=11.5, color=GREEN, ha="left", va="center",
                linespacing=1.2)
        ax.text(X1, y - h + 0.013, note, fontproperties=C.FP, fontsize=10.5, color=GREY, ha="left",
                va="center")
        y -= h
    ax.text(0.5, 0.078, "Blust《Austronesian Comparative Dictionary》*manuk；Ohashi & Orchiston 2021",
            fontproperties=C.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.058, "Feinberg 1988（阿努塔）；Collocott 1922（東加）", fontproperties=C.FP, fontsize=10,
            color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=C.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


def main():
    global S
    os.makedirs(OUT, exist_ok=True)
    S = G.load_stars(BASE)
    S = dict(S)
    print(f"  阿努塔→Tikopia {gc_km(P['Anuta'], P['Tikopia']):.0f} km、{bearing(P['Anuta'], P['Tikopia']):.1f}°；"
          f"→Patutaka {gc_km(P['Anuta'], P['Patutaka']):.0f} km；→東加 {gc_km(P['Anuta'], P['Tongatapu']):.0f} km；"
          f"→ʻUvea {gc_km(P['Anuta'], P['ʻUvea']):.0f} km")
    for nm, (alt, az, v) in sgr_altaz().items():
        print(f"  人馬 {nm}: 高 {alt:.1f}°、方位 {az:.1f}°")
    C.emit("", [("島嶼", c01_islands), ("祖先", c01_ancestors)], title="C-A11-01_阿努塔地圖")
    C.emit("", [("星點", c02_stars), ("翅膀", c02_wings), ("傳說", c02_legend)], title="C-A11-02_Manu的翅膀")
    C.emit("", [("海面", c03_sea), ("星路", c03_path)], title="C-A11-03_星路")
    f, ax = C.newcard(dark=True)
    c04_card(ax)
    C.save(f, "", "C-A11-04_阿努塔的生活星空_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    c05_card(ax)
    C.save(f, "", "C-A11-05_同一個字_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
