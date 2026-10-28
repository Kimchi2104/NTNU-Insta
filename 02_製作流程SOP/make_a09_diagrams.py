# -*- coding: utf-8 -*-
"""A-09 夏威夷｜概念圖（方形透明分層：Reels 定格頁一頁疊一層）
  C-A09-01_星羅盤       → 逐字稿 04 鏡（羅盤層／參宿三層）
  C-A09-02_緯度尺       → 逐字稿 09 鏡（天頂星層／南十字層）
  C-A09-03_航線與三角   → 逐字稿 02 鏡（島嶼層／航線層）、11 鏡（島嶼層／三角層）
輸出：05_素材/A-09_夏威夷星線/_概念圖/
來源：星羅盤＝Nainoa Thompson（Polynesian Voyaging Society「The Star Compass」）：32 間房子、每間 11.25°；
      東西南北各一間（Hikina／Komohana／ʻĀkau／Hema），每個象限七間同名：Lā、ʻĀina、Noio、Manu、
      Nālani、Nā Leo、Haka（由地平線東西兩點往南北數）；象限名 Koʻolau（東北）、Malanai（東南）、
      Kona（西南）、Hoʻolua（西北）。
      緯度＝PVS「Estimating Position／Meridian pointers to south」：大角星赤緯 +19.05°（2026），
      南十字底星 Acrux −63.25°、Gacrux −57.26°（相距 6.0°）；在北緯 21.3° 上中天時 Acrux 高 5.5°（幾何）。
      地圖＝經緯度實際位置（等距圓柱投影，非地形圖）；距離為大圓距離（自算）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-09_夏威夷星線/_概念圖")
C.set_base(OUT)
RED, GREY, SEA = "#FF6B6B", "#7C8BA8", "#2A4A7A"

# ══════════════════════ C-A09-01 星羅盤 ══════════════════════
CX, CY, R = 0.0, -0.03, 0.55
HOUSES = ["Lā", "ʻĀina", "Noio", "Manu", "Nālani", "Nā Leo", "Haka"]


def az_xy(az, r):
    """方位角（0=北、90=東）→ 圖上座標（北在上、東在右）"""
    t = math.radians(90.0 - az)
    return CX + r * math.cos(t), CY + r * math.sin(t)


def canoe(ax, x, y, s=1.0):
    """雙體獨木舟（俯視示意）：兩條船身＋橫樑＋甲板"""
    for dx in (-0.045 * s, 0.045 * s):
        ax.add_patch(C.Ellipse((x + dx, y), 0.035 * s, 0.20 * s, fc=C.BG, ec=WHITE,
                               lw=2.0, zorder=8))
    for dy in (-0.05 * s, 0.0, 0.05 * s):
        ax.plot([x - 0.06 * s, x + 0.06 * s], [y + dy, y + dy], c=WHITE, lw=2.0, zorder=9)


def c01_compass(ax):
    T(ax, 0.0, 0.92, "夏威夷星羅盤", 34, WHITE)
    T(ax, 0.0, 0.84, "地平線一圈切成 32 間「房子」，一間 11.25°", 21, GREY, w="normal")
    ax.add_patch(C.Circle((CX, CY), R, fill=False, ec=WHITE, lw=2.2, alpha=.85, zorder=4))
    ax.add_patch(C.Circle((CX, CY), R * 0.80, fill=False, ec=WHITE, lw=1.0, alpha=.35, zorder=4))
    for i in range(32):                         # 房子的分界：中心在 0、11.25…，分界差半格
        az = i * 11.25 + 5.625
        a, b = az_xy(az, R * 0.80), az_xy(az, R)
        ax.plot([a[0], b[0]], [a[1], b[1]], c=WHITE, lw=1.0, alpha=.45, zorder=4)
    # 四個方位（各自一間房子）
    for az, haw, zh in ((0, "ʻĀkau", "北"), (90, "Hikina", "東"), (180, "Hema", "南"),
                        (270, "Komohana", "西")):
        x, y = az_xy(az, R + (0.085 if az in (0, 180) else 0.19))
        T(ax, x, y + 0.02, haw, 21, AMBER)
        T(ax, x, y - 0.035, zh, 18, AMBER, w="normal")
    # 東北象限的七間（其他三個象限同名、左右對稱）：寫在圈外、水平排
    for i, nm in enumerate(HOUSES, 1):
        az = 90.0 - 11.25 * i
        x, y = az_xy(az, R + 0.035)
        ax.text(x, y, nm, fontproperties=C.FP, fontsize=15, color=WHITE, ha="left",
                va="center", zorder=12)
        a, b = az_xy(az, R * 0.80), az_xy(az, R)
        ax.scatter([(a[0] + b[0]) / 2], [(a[1] + b[1]) / 2], s=18, c=WHITE, alpha=.7, zorder=5)
    for az, nm in ((45, "Koʻolau 東北"), (135, "Malanai 東南"), (225, "Kona 西南"),
                   (315, "Hoʻolua 西北")):
        x, y = az_xy(az, R * 0.58)
        T(ax, x, y, nm, 16, GREY, w="normal")
    canoe(ax, CX, CY, 1.0)
    T(ax, 0.0, -0.80, "東西南北各一間；四個象限各有同樣七間：Lā、ʻĀina、Noio、Manu、Nālani、Nā Leo、Haka",
      14.5, WHITE, w="normal")


def c01_mintaka(ax):
    e, w = az_xy(90, R), az_xy(270, R)
    for (x, y), nm in ((e, "升起"), (w, "落下")):
        ax.scatter([x], [y], s=520, c=AMBER, marker="*", zorder=10)
    # 天球上的路徑投到地平面：赤緯 0 的星往南偏一點（示意，北緯 21°）
    xs = [CX + R * math.cos(math.radians(t)) for t in range(0, 181, 3)]
    ys = [CY - 0.20 * math.sin(math.radians(t)) for t in range(0, 181, 3)]
    ax.plot(xs, ys, c=AMBER, lw=2.6, ls=(0, (7, 5)), zorder=6)
    C.arrow(ax, (xs[-4], ys[-4]), (xs[-9], ys[-9]), c=AMBER, lw=2.6, alpha=1, style="-|>")
    T(ax, e[0] - 0.24, e[1] + 0.075, "Mintaka 參宿三", 20, AMBER)
    T(ax, e[0] - 0.24, e[1] + 0.015, "正東升起", 17, AMBER, w="normal")
    T(ax, w[0] + 0.19, w[1] + 0.045, "正西落下", 17, AMBER, w="normal")
    ax.add_patch(C.FancyBboxPatch((-0.86, -0.995), 1.72, 0.10,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=AMBER, lw=1.4, zorder=2))
    T(ax, 0.0, -0.945, "從東邊哪一間升起，就從西邊同名的那一間落下", 19, WHITE)


# ══════════════════════ C-A09-02 緯度尺 ══════════════════════
DEC_ARC, DEC_ACR, DEC_GAC = 19.05, -63.25, -57.26


def c02_zenith(ax):
    T(ax, 0.0, 0.93, "到了沒？看頭頂，也看南方", 32, WHITE)
    T(ax, -0.46, 0.80, "Hōkūleʻa（大角星）＝夏威夷的天頂星", 19, GREEN)
    # 半圓天穹（側視；南在左、北在右）。角度放大 3 倍示意，否則 5°、10° 的差在畫面上看不出來
    ox, oy, r = -0.44, 0.08, 0.48
    ax.plot([ox - r - 0.04, ox + r + 0.04], [oy, oy], c=SEA, lw=3.0, zorder=3)
    th = [math.radians(t) for t in range(0, 181, 2)]
    ax.plot([ox + r * math.cos(t) for t in th], [oy + r * math.sin(t) for t in th],
            c=WHITE, lw=1.4, alpha=.45, zorder=3)
    ax.plot([ox, ox], [oy, oy + r], c=WHITE, lw=1.0, alpha=.5, ls=(0, (4, 4)), zorder=3)
    T(ax, ox - 0.07, oy + r - 0.06, "天頂", 15, WHITE, w="normal")
    T(ax, ox - r, oy - 0.05, "南", 16, GREY, w="normal")
    T(ax, ox + r, oy - 0.05, "北", 16, GREY, w="normal")
    canoe(ax, ox, oy + 0.035, 0.45)
    for lat, a, txt in ((9, .45, "北緯 9°：差 10°"), (14, .7, "北緯 14°：差 5°"),
                        (19, 1.0, "北緯 19°：正頭頂")):
        zd = (DEC_ARC - lat) * 3.0             # 偏北幾度（×3 示意）
        t = math.radians(90.0 - zd)
        x, y = ox + r * math.cos(t), oy + r * math.sin(t)
        ax.scatter([x], [y], s=420 if lat == 19 else 260, c=GREEN, marker="*", alpha=a, zorder=8)
        lx, ly = ox + (r + 0.07) * math.cos(t), oy + (r + 0.07) * math.sin(t)
        T(ax, lx + (0.14 if lat != 19 else 0.0), ly + (0.0 if lat != 19 else 0.02), txt,
          15 if lat != 19 else 17, GREEN, w="normal" if lat != 19 else "bold", alpha=max(a, .75))
    T(ax, ox, oy - 0.12, "船往北開，它一晚比一晚高", 17, WHITE, w="normal")
    T(ax, ox, oy - 0.19, "正好掛在頭頂＝到了夏威夷大島的緯度", 17, WHITE, w="normal")
    T(ax, ox, oy - 0.27, "（大角星赤緯 +19°；示意圖角度放大 3 倍）", 14, GREY, w="normal")


def c02_crux(ax):
    T(ax, 0.46, 0.80, "Hānaiakamalama（南十字）", 19, GREEN)
    ox, oy, k = 0.46, -0.10, 0.042             # 1° = 0.042 單位
    ax.plot([ox - 0.40, ox + 0.40], [oy, oy], c=SEA, lw=3.0, zorder=3)
    for i in range(3):
        xs = [ox - 0.40 + j * 0.02 for j in range(41)]
        ax.plot(xs, [oy - 0.03 - 0.025 * i + 0.008 * math.sin(j * 1.3 + i) for j in range(41)],
                c=SEA, lw=1.6, alpha=.6 - .15 * i, zorder=3)
    lat = 21.3
    h_acr = 90 - lat + DEC_ACR + 0.15          # 加大氣折射約 0.15°
    h_gac = 90 - lat + DEC_GAC + 0.08
    acr, gac = (ox, oy + h_acr * k), (ox, oy + h_gac * k)
    mim = (ox - 2.4 * k, oy + (90 - lat - 59.69) * k)   # Mimosa（東＝左）
    imai = (ox + 1.8 * k, oy + (90 - lat - 58.75) * k)  # Imai
    ax.plot([acr[0], gac[0]], [acr[1], gac[1]], c=GREEN, lw=2.6, zorder=6)
    ax.plot([mim[0], imai[0]], [mim[1], imai[1]], c=GREEN, lw=2.0, zorder=6)
    for p, s in ((acr, 330), (gac, 260), (mim, 230), (imai, 120)):
        ax.scatter([p[0]], [p[1]], s=s, c=WHITE, zorder=8)
    # 兩段一樣長
    bx = ox + 0.16
    for y0, y1, c in ((oy, acr[1], AMBER), (acr[1], gac[1], AMBER)):
        ax.plot([bx, bx], [y0 + 0.005, y1 - 0.005], c=c, lw=2.4, zorder=7)
        for yy in (y0 + 0.005, y1 - 0.005):
            ax.plot([bx - 0.02, bx + 0.02], [yy, yy], c=c, lw=2.4, zorder=7)
        T(ax, bx + 0.10, (y0 + y1) / 2, "≈ 6°", 19, AMBER)
    T(ax, ox - 0.13, acr[1], "十字底", 15, WHITE, w="normal")
    T(ax, ox - 0.13, gac[1], "十字頂", 15, WHITE, w="normal")
    T(ax, ox, oy - 0.12, "南十字直立時：", 17, WHITE, w="normal")
    T(ax, ox, oy - 0.19, "海面→十字底 ＝ 十字的長度", 17, WHITE, w="normal")
    T(ax, ox, oy - 0.27, "只發生在北緯約 21°（檀香山）", 17, AMBER)
    ax.add_patch(C.FancyBboxPatch((-0.88, -0.90), 1.76, 0.20,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=GREEN, lw=1.4, zorder=2))
    T(ax, 0.0, -0.75, "沒有六分儀，也量得出緯度", 21, WHITE)
    T(ax, 0.0, -0.84, "方向靠星羅盤，到了沒靠頭頂和南方這兩把尺", 17, GREY, w="normal")


# ══════════════════════ C-A09-03 航線與三角 ══════════════════════
LON0, SC = 197.0, 1.80 / 118.0               # 東經 138°～256°（西經 104°）→ 寬 1.8
LAT0 = -8.0
PLACES = {
    "夏威夷 Hawaiʻi": (21.31, -157.86), "大溪地 Tahiti": (-17.54, -149.57),
    "復活節島 Rapa Nui": (-27.12, -109.35), "紐西蘭 Aotearoa": (-36.85, 174.76),
    "Satawal": (7.37, 147.03),
}
MAUI = (21.01, -156.64)


def mp(lat, lon):
    lon = lon % 360.0
    return (lon - LON0) * SC, (lat - LAT0) * SC


def gc_pts(a, b, n=60):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    v1 = (math.cos(la1) * math.cos(lo1), math.cos(la1) * math.sin(lo1), math.sin(la1))
    v2 = (math.cos(la2) * math.cos(lo2), math.cos(la2) * math.sin(lo2), math.sin(la2))
    om = math.acos(sum(p * q for p, q in zip(v1, v2)))
    out = []
    for i in range(n + 1):
        t = i / n
        s1, s2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
        v = [s1 * p + s2 * q for p, q in zip(v1, v2)]
        out.append((math.degrees(math.asin(v[2])), math.degrees(math.atan2(v[1], v[0]))))
    return out


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371.0 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) *
                                            math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def c03_islands(ax):
    T(ax, 0.0, 0.92, "太平洋的正中間", 34, WHITE)
    T(ax, 0.0, 0.845, "島嶼位置依實際經緯度（等距圓柱投影）", 17, GREY, w="normal")
    x0, y0 = mp(-45, 138); x1, y1 = mp(28, 256)
    ax.add_patch(C.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=WHITE, lw=1.2,
                             alpha=.35, zorder=2))
    for lat in (-40, -20, 0, 20):
        a, b = mp(lat, 138), mp(lat, 256)
        ax.plot([a[0], b[0]], [a[1], a[1]], c=WHITE, lw=1.6 if lat == 0 else 0.8,
                alpha=.45 if lat == 0 else .2, ls="-" if lat == 0 else (0, (4, 5)), zorder=2)
        T(ax, b[0] - 0.06, a[1] + 0.025, "赤道" if lat == 0 else f"{abs(lat)}°{'N' if lat > 0 else 'S'}",
          12, GREY, w="normal")
    for lon in (150, 180, 210, 240):
        a, b = mp(-45, lon), mp(28, lon)
        ax.plot([a[0], a[0]], [a[1], b[1]], c=WHITE, lw=0.8, alpha=.2, ls=(0, (4, 5)), zorder=2)
    off = {"夏威夷 Hawaiʻi": (0.0, 0.065), "大溪地 Tahiti": (0.14, -0.05),
           "復活節島 Rapa Nui": (-0.12, -0.065), "紐西蘭 Aotearoa": (0.0, -0.065),
           "Satawal": (0.0, 0.06)}
    for nm, (lat, lon) in PLACES.items():
        x, y = mp(lat, lon)
        ax.scatter([x], [y], s=200, c=WHITE, zorder=8)
        T(ax, x + off[nm][0], y + off[nm][1], nm, 17 if nm != "Satawal" else 14,
          WHITE, w="bold" if nm != "Satawal" else "normal")
    xs, ys = mp(*PLACES["Satawal"])
    T(ax, xs, ys - 0.06, "Mau Piailug 的家鄉", 13, GREY, w="normal")


def c03_route(ax):
    pts = [mp(la, lo) for la, lo in gc_pts(MAUI, PLACES["大溪地 Tahiti"])]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], c=AMBER, lw=3.2, ls=(0, (8, 5)), zorder=6)
    C.arrow(ax, pts[-1], pts[-6], c=AMBER, lw=3.2, alpha=1, style="-|>")
    km = gc_km(MAUI, PLACES["大溪地 Tahiti"])
    rx = -0.20                                  # 文字放在航線左側（三角層不會同時出現）
    T(ax, rx, 0.05, "1976｜Hōkūleʻa", 19, AMBER, ha="right")
    T(ax, rx, -0.02, "茂宜 → 大溪地，34 天", 16, AMBER, w="normal", ha="right")
    T(ax, rx, -0.09, f"四千多公里（直線 {km:,.0f} km）", 16, AMBER, w="normal", ha="right")
    T(ax, rx, -0.16, "沒有羅盤、六分儀、地圖", 16, WHITE, w="normal", ha="right")


def c03_triangle(ax):
    H, RN, A = PLACES["夏威夷 Hawaiʻi"], PLACES["復活節島 Rapa Nui"], PLACES["紐西蘭 Aotearoa"]
    for a, b, dx, dy in ((H, RN, 0.17, 0.07), (RN, A, 0.0, -0.06), (A, H, 0.15, -0.02)):
        pts = [mp(la, lo) for la, lo in gc_pts(a, b)]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], c=BLUE, lw=3.0, zorder=6)
        mx, my = pts[int(len(pts) * (0.72 if a is H and b is RN else 0.5))]
        T(ax, mx + dx, my + dy, f"約 {round(gc_km(a, b), -2):,.0f} km", 16, BLUE)
    for (lat, lon), star, dx, dy in ((H, "Hawaiki 天津四", 0.0, 0.13), (RN, "Keoe 織女", -0.12, -0.13),
                                     (A, "Humu 牛郎", 0.0, -0.13)):
        x, y = mp(lat, lon)
        ax.scatter([x], [y], s=520, c=BLUE, marker="*", zorder=9)
        T(ax, x + dx, y + dy, star, 17, BLUE)
    ax.add_patch(C.FancyBboxPatch((-0.86, -0.95), 1.72, 0.13,
                                  boxstyle="round,pad=0.01,rounding_size=0.03",
                                  fc="#1B2240", ec=BLUE, lw=1.4, zorder=2))
    T(ax, 0.0, -0.885, "航海協會的象徵：引航三角的三顆星＝玻里尼西亞三角的三個角", 16.5, WHITE,
      w="normal")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    C.emit("", [("羅盤", c01_compass), ("參宿三", c01_mintaka)], title="C-A09-01_星羅盤")
    C.emit("", [("天頂星", c02_zenith), ("南十字", c02_crux)], title="C-A09-02_緯度尺")
    C.emit("", [("島嶼", c03_islands), ("航線", c03_route)], preview_name="預覽-航線",
           title="C-A09-03_航線與三角")          # 02 鏡：島嶼→航線
    C.emit("", [("島嶼", c03_islands), ("三角", c03_triangle)], preview_name="預覽-三角",
           title="C-A09-03_航線與三角")          # 11 鏡：島嶼→三角（航線層與三角層不同時出現）
