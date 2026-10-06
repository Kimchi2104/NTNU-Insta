# -*- coding: utf-8 -*-
"""A-12 白虎｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A12-01_參字          → 逐字稿 05 鏡（三星層→字形層→說明層）
  C-A12-02_參商          → 逐字稿 07 鏡（地平層→參宿層→心宿層→引文層）
  C-A12-03_西羌線索      → 逐字稿 12 鏡（墓葬層→字形層→彝族層→結論層）
  C-A12-04_天關客星      → 逐字稿 11 鏡（星圖層→客星層→引文層→今日層）
  C-A12-05_同一條腰帶    → 逐字稿 06 鏡（9:16 圖卡，可存圖）
  C-A12-06_白虎的鄰居    → 逐字稿 09 鏡（9:16 圖卡，可存圖）
  C-A12-07_今晚往東看    → 逐字稿 13 鏡（9:16 圖卡：台北 2026/12/4 20:00，PyEphem 自算）
輸出：05_素材/A-12_白虎/_概念圖/

來源：《史記．天官書》（唐張守節《正義》）、《晉書．天文志》、《左傳．昭公元年》、杜甫〈贈衛八處士〉、
      《禮記．月令》、《宋會要》、《宋史》、《後漢書．南蠻西南夷列傳》；濮陽西水坡 M45（1987 年發掘，
      距今約 6,400 年）；Stellarium chinese／bugis／anutan／romanian／belarusian／inuit／arabic／sardinian；
      師大天文社〈中國星座〉簡報 p.16–17（白虎＝西羌）。
      字形、墓葬、星雲都是自繪示意圖，不臨摹任何已出版的摹本、復原圖或照片。
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as CB
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, MW, T
import gen_ep_assets as G
import make_a12_v4 as A12

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-12_白虎/_概念圖")
CB.set_base(OUT)
RED, GREY, PANEL = "#FF6B6B", "#7C8BA8", "#1B2240"
S = None
C = A12.C
TPE = ("25.0330", "121.5654")


def ssize(v, k=22.0, lo=10.0):
    return max(lo, max(0.0, 6.0 - v) ** 2.2 * k)


def uniq(*keys):
    return sorted({h for k in keys for seg in C[k] for h in seg})


def segs(*keys):
    out = []
    for k in keys:
        for seg in C[k]:
            out += list(zip(seg, seg[1:]))
    return out


def box(ax, x0, y0, w, h, ec=WHITE, fc=PANEL, lw=1.4, z=3):
    ax.add_patch(CB.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=z))


def altaz_at(when_local, tz=8):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = TPE; o.pressure = 1010
    o.date = ephem.Date(ephem.Date(when_local) - tz * ephem.hour)

    def f(ra, dec):
        b = ephem.FixedBody(); b._ra = math.radians(ra); b._dec = math.radians(dec)
        b._epoch = ephem.J2000; b.compute(o)
        return math.degrees(b.alt), math.degrees(b.az)
    return f


# ══════════════════════ C-A12-01 參字 ══════════════════════
def c01_stars(ax):
    T(ax, 0.0, 0.92, "「參」：三顆星，加一個人", 31, WHITE)
    T(ax, 0.0, 0.845, "左：天上的參宿　右：金文字形（自繪示意，非摹本）", 16, GREY, w="normal")
    ra0, dec0, s, cx, cy = 83.9, 0.0, 0.031, -0.47, 0.16

    def p(h):
        ra, dec, _ = S[h]
        return cx - (ra - ra0) * math.cos(math.radians(dec0)) * s, cy + (dec - dec0) * s
    for a, b in segs("003", "069", "034"):
        (x1, y1), (x2, y2) = p(a), p(b)
        ax.plot([x1, x2], [y1, y2], c=AMBER, lw=2.0, alpha=.55, zorder=4)
    for h in uniq("003", "069", "034"):
        x, y = p(h)
        ax.scatter([x], [y], s=ssize(S[h][2]), c=WHITE, zorder=6, lw=0)
    for h in (A12.MINTAKA, A12.ALNILAM, A12.ALNITAK):
        x, y = p(h)
        ax.add_patch(CB.Circle((x, y), 0.032, fc="none", ec=AMBER, lw=2.4, zorder=7))
    xb, yb = p(A12.ALNILAM)
    T(ax, xb - 0.25, yb + 0.015, "參宿三星", 17, AMBER, ha="right")
    T(ax, xb - 0.25, yb - 0.045, "（獵戶腰帶）", 13, GREY, w="normal", ha="right")


def c01_glyph(ax):
    # 三顆星（圓圈＋中心點）
    for x, y in ((0.30, 0.55), (0.44, 0.62), (0.58, 0.55)):
        ax.add_patch(CB.Circle((x, y), 0.052, fc="none", ec=AMBER, lw=5.0, zorder=6))
        ax.scatter([x], [y], s=60, c=AMBER, zorder=7, lw=0)

    def quad(p0, p1, p2, n=40):
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                 (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
                for t in (i / n for i in range(n + 1))]
    head = [(0.405, 0.33), (0.41, 0.40), (0.445, 0.445), (0.49, 0.44), (0.515, 0.41), (0.505, 0.385),
            (0.52, 0.365), (0.50, 0.355), (0.495, 0.33), (0.47, 0.32)]     # 頭：額、鼻、口、頤（側面）
    ax.add_patch(CB.Polygon(head, closed=True, fc=AMBER, ec="none", zorder=6))
    body = quad((0.43, 0.33), (0.33, 0.12), (0.41, -0.17))           # 背：從後頸彎到腳
    arm = quad((0.42, 0.22), (0.55, 0.15), (0.56, -0.01))            # 手臂往前下
    for pts in (body, arm):
        ax.plot([q[0] for q in pts], [q[1] for q in pts], c=AMBER, lw=11, solid_capstyle="round",
                zorder=6)
    T(ax, 0.44, -0.27, "金文「參」（示意）", 15, AMBER, w="normal")
    CB.arrow(ax, (0.76, 0.17), (0.64, 0.17), c=WHITE, lw=2.2, alpha=.8, style="-|>")
    T(ax, 0.85, 0.17, "參", 64, WHITE)
    T(ax, 0.85, -0.03, "今天的字", 13, GREY, w="normal")


def c01_text(ax):
    box(ax, -0.92, -0.93, 1.84, 0.53, ec=AMBER)
    T(ax, 0.0, -0.48, "上面三顆星、底下一個人——很多學者認為，畫的就是參宿這三顆", 15.5, WHITE, w="normal")
    T(ax, 0.0, -0.565, "後來「參」被借去寫數字三。台灣的支票大寫：", 15.5, WHITE, w="normal")
    nums = "壹貳參肆伍陸柒捌玖拾"
    for i, ch in enumerate(nums):
        x = -0.72 + i * 0.16
        T(ax, x, -0.68, ch, 27, AMBER if ch == "參" else WHITE)
    T(ax, 0.0, -0.80, "例：新臺幣參仟元整", 16, GREY, w="normal")
    T(ax, 0.0, -0.875, "字形為自繪示意；金文「參」寫法不一，有的另加「彡」", 11.5, GREY, w="normal")


# ══════════════════════ C-A12-02 參商 ══════════════════════
WHEN2 = "2027/04/20 21:29"
HZ2, SD2 = -0.15, 0.88 / 30.0
PAN_L = (105.0, 135.0, -0.93)       # 方位起、迄、面板左緣 x
PAN_R = (255.0, 285.0, 0.05)


def pan_xy(alt, az):
    for a0, a1, x0 in (PAN_L, PAN_R):
        if a0 - 2 <= az <= a1 + 2:
            return x0 + (az - a0) * SD2, HZ2 + alt * SD2
    return None


def c02_horizon(ax):
    T(ax, 0.0, 0.92, "參商：一個升起，另一個落下", 31, WHITE)
    T(ax, 0.0, 0.845, "台北：參宿三星和心宿二同時在地平線上，一天大約 14 分鐘，而且都不到 2.5°", 15.5, GREY,
      w="normal")
    T(ax, 0.0, 0.775, "例：2027 年 4 月 20 日 21:29（PyEphem 自算，含大氣折射）", 13.5, GREY, w="normal")
    for a0, a1, x0 in (PAN_L, PAN_R):
        x1 = x0 + (a1 - a0) * SD2
        ax.add_patch(CB.Rectangle((x0, -0.40), x1 - x0, HZ2 + 0.40, fc="#141A2E", ec="none", zorder=2))
        ax.plot([x0, x1], [HZ2, HZ2], c=WHITE, lw=2.0, alpha=.75, zorder=5)
        for az in range(int(a0), int(a1) + 1, 5):
            x = x0 + (az - a0) * SD2
            ax.plot([x, x], [HZ2 - 0.012, HZ2 + 0.012], c=WHITE, lw=1.0, alpha=.5, zorder=5)
        for alt in (5, 10, 15, 20):
            ax.plot([x0, x0 + 0.02], [HZ2 + alt * SD2] * 2, c=WHITE, lw=1.0, alpha=.4)
            T(ax, x0 + 0.03, HZ2 + alt * SD2, f"{alt}°", 10.5, GREY, w="normal", ha="left")
    for az, lab in ((112.5, "東南偏東（112.5°）"), (270, "正西（270°）")):
        q = pan_xy(0, az)
        T(ax, q[0], HZ2 - 0.06, lab, 14, WHITE, w="normal")
    T(ax, 0.0, HZ2 - 0.06, "⋯", 16, GREY, w="normal")
    T(ax, 0.0, HZ2 - 0.13, "（中間隔著南方天空，約 120°）", 12, GREY, w="normal")
    T(ax, -0.49, 0.62, "東邊升起", 17, RED)
    T(ax, 0.49, 0.62, "西邊落下", 17, AMBER)


def _plot_group(ax, f, keys, col, label, sub, lab_dx=0.0):
    pts = {}
    for h in uniq(*keys):
        alt, az = f(*S[h][:2])
        q = pan_xy(alt, az)
        if q:
            pts[h] = (q, alt, az)
    for a, b in segs(*keys):
        if a in pts and b in pts:
            (x1, y1), (x2, y2) = pts[a][0], pts[b][0]
            low = pts[a][1] < 0 or pts[b][1] < 0
            ax.plot([x1, x2], [y1, y2], c=col, lw=2.2, alpha=.22 if low else .85, zorder=6,
                    ls=(0, (3, 3)) if low else "-")
    for h, ((x, y), alt, az) in pts.items():
        below = alt < 0
        ax.scatter([x], [y], s=ssize(S[h][2], 26), c=WHITE, alpha=.25 if below else 1.0, zorder=7, lw=0)
    xs = [q[0][0] for q in pts.values()]
    ys = [q[0][1] for q in pts.values() if q[1] > 0]
    T(ax, sum(xs) / len(xs) + lab_dx, max(ys) + 0.11, label, 19, col)
    T(ax, sum(xs) / len(xs) + lab_dx, max(ys) + 0.055, sub, 13, col, w="normal")
    return pts


def c02_shen(ax):
    f = altaz_at(WHEN2)
    pts = _plot_group(ax, f, ["003", "069", "034"], AMBER, "參宿（參星）", "實沈管的星", lab_dx=0.0)
    for h in (A12.MINTAKA, A12.ALNILAM, A12.ALNITAK):
        (x, y), _, _ = pts[h]
        ax.add_patch(CB.Circle((x, y), 0.022, fc="none", ec=AMBER, lw=1.8, zorder=8))
    T(ax, 0.68, -0.37, "虛線＝已經沉到地平線下（參宿七）", 11.5, GREY, w="normal")


def c02_shang(ax):
    f = altaz_at(WHEN2)
    pts = _plot_group(ax, f, ["026"], RED, "心宿（商星）", "閼伯管的星", lab_dx=0.0)
    (x, y), _, _ = pts[80763]
    ax.add_patch(CB.Circle((x, y), 0.026, fc="none", ec=RED, lw=1.8, zorder=8))
    T(ax, x + 0.04, y + 0.035, "心宿二", 13, RED, w="normal", ha="left")
    T(ax, -0.49, -0.37, "虛線＝還在地平線下（心宿三）", 11.5, GREY, w="normal")


def c02_quote(ax):
    box(ax, -0.92, -0.93, 1.84, 0.50, ec=AMBER)
    T(ax, 0.0, -0.49, "《左傳．昭公元年》", 15, AMBER)
    T(ax, 0.0, -0.565, "昔高辛氏有二子，伯曰閼伯，季曰實沈……日尋干戈，以相征討。", 15, WHITE, w="normal")
    T(ax, 0.0, -0.635, "后帝不臧，遷閼伯于商丘，主辰……遷實沈于大夏，主參。", 15, WHITE, w="normal")
    T(ax, 0.0, -0.70, "（辰＝心宿，故稱商星；后帝，杜預注：堯）", 12, GREY, w="normal")
    T(ax, 0.0, -0.79, "人生不相見，動如參與商。", 24, AMBER)
    T(ax, 0.0, -0.87, "——杜甫〈贈衛八處士〉", 13, GREY, w="normal")


# ══════════════════════ C-A12-03 西羌線索 ══════════════════════
def c03_tomb(ax):
    T(ax, 0.0, 0.92, "白虎有多老？從哪裡來？", 31, WHITE)
    box(ax, -0.92, 0.27, 1.84, 0.56, ec=AMBER)
    T(ax, 0.30, 0.74, "線索一：六千多年前的龍與虎", 17, AMBER)
    T(ax, 0.30, 0.66, "河南濮陽西水坡 M45（1987 年發掘）", 13.5, WHITE, w="normal")
    T(ax, 0.30, 0.60, "距今約 6,400 年（仰韶文化）", 13.5, WHITE, w="normal")
    T(ax, 0.30, 0.52, "墓主頭南腳北；身旁用蚌殼擺出", 13.5, WHITE, w="normal")
    T(ax, 0.30, 0.46, "東邊一條龍、西邊一隻虎", 15, AMBER)
    T(ax, 0.30, 0.37, "四象「左青龍、右白虎」的方位，", 12.5, GREY, w="normal")
    T(ax, 0.30, 0.32, "這時已經擺好了", 12.5, GREY, w="normal")
    # 平面示意（北在上、東在右）
    cx, cy = -0.52, 0.55
    ax.add_patch(CB.FancyBboxPatch((cx - 0.30, cy - 0.23), 0.60, 0.46,
                                   boxstyle="round,pad=0.0,rounding_size=0.05",
                                   fc="#141A2E", ec=GREY, lw=1.2, ls=(0, (4, 3)), zorder=4))
    # 墓主：頭在南（下）
    body = [(-0.035, -0.17), (0.035, -0.17), (0.045, -0.08), (0.04, 0.05), (0.03, 0.16),
            (-0.03, 0.16), (-0.04, 0.05), (-0.045, -0.08)]
    ax.add_patch(CB.Polygon([(cx + x, cy + y) for x, y in body], closed=True, fc="none", ec=WHITE,
                            lw=1.6, zorder=5))
    ax.add_patch(CB.Ellipse((cx, cy - 0.19), 0.06, 0.05, fc="none", ec=WHITE, lw=1.6, zorder=5))
    # 龍（東＝右）：側面、頭朝北、背朝墓主（西）、腳朝東
    t = np.linspace(0, 1, 80)
    dx = cx + 0.165 + 0.030 * np.sin(t * 2 * math.pi * 1.25)
    dy = cy - 0.19 + 0.33 * t
    ax.plot(dx, dy, c=BLUE, lw=7, solid_capstyle="round", zorder=5)
    ax.scatter(dx[::6], dy[::6], s=9, c=WHITE, zorder=6, lw=0, alpha=.8)          # 蚌殼的點
    for k in (20, 34, 52, 66):                                                      # 四足朝東
        x0, y0 = dx[k] + 0.012, dy[k]
        ax.plot([x0, x0 + 0.035, x0 + 0.045], [y0, y0 - 0.012, y0 - 0.002], c=BLUE, lw=2.6,
                solid_capstyle="round", zorder=5)
    hx, hy = dx[-1], dy[-1]
    ax.add_patch(CB.Polygon([(hx - 0.022, hy - 0.005), (hx - 0.018, hy + 0.030), (hx + 0.005, hy + 0.055),
                             (hx + 0.020, hy + 0.040), (hx + 0.022, hy + 0.005)], closed=True, fc=BLUE,
                            ec="none", zorder=5))
    # 虎（西＝左）：側面、頭朝北、背朝墓主（東）、腳朝西；身上有條紋
    tx = cx - 0.17
    bodyp = [(tx + 0.028, cy - 0.12), (tx + 0.032, cy + 0.02), (tx + 0.026, cy + 0.10),
             (tx - 0.026, cy + 0.10), (tx - 0.034, cy + 0.02), (tx - 0.028, cy - 0.12)]
    ax.add_patch(CB.Polygon(bodyp, closed=True, fc=AMBER, ec="none", zorder=5))
    headp = [(tx - 0.030, cy + 0.095), (tx - 0.034, cy + 0.150), (tx - 0.020, cy + 0.185),
             (tx - 0.012, cy + 0.172), (tx + 0.004, cy + 0.192), (tx + 0.026, cy + 0.165),
             (tx + 0.030, cy + 0.120), (tx + 0.026, cy + 0.095)]
    ax.add_patch(CB.Polygon(headp, closed=True, fc=AMBER, ec="none", zorder=5))
    ax.scatter([tx - 0.008], [cy + 0.150], s=14, c=CB.BG, zorder=6, lw=0)
    for yy in (cy - 0.08, cy - 0.01, cy + 0.06):
        ax.plot([tx - 0.028, tx + 0.004], [yy, yy + 0.012], c=CB.BG, lw=2.2, zorder=6)
    for y0, d in ((cy + 0.07, 0.0), (cy + 0.03, 0.006), (cy - 0.07, 0.0), (cy - 0.105, 0.006)):   # 四足朝西
        ax.plot([tx - 0.026, tx - 0.07, tx - 0.075], [y0, y0 - 0.010 - d, y0 - 0.030], c=AMBER, lw=4,
                solid_capstyle="round", zorder=5)
    tail = [(tx + 0.004, cy - 0.12), (tx + 0.02, cy - 0.16), (tx + 0.05, cy - 0.17), (tx + 0.065, cy - 0.15)]
    ax.plot([q[0] for q in tail], [q[1] for q in tail], c=AMBER, lw=3.5, solid_capstyle="round", zorder=5)
    T(ax, cx + 0.255, cy - 0.05, "龍", 16, BLUE)
    T(ax, cx - 0.265, cy - 0.05, "虎", 16, AMBER)
    T(ax, cx, cy + 0.205, "墓主", 11, WHITE, w="normal")
    T(ax, cx, cy - 0.27, "平面示意（非等比例）", 11, GREY, w="normal")
    ax.annotate("", xy=(cx + 0.27, cy + 0.20), xytext=(cx + 0.27, cy + 0.10),
                arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=1.6))
    T(ax, cx + 0.27, cy + 0.235, "北", 12, WHITE)


def c03_glyph(ax):
    box(ax, -0.92, -0.33, 0.89, 0.55, ec=GREEN)
    T(ax, -0.475, 0.14, "線索二：羊的部族", 17, GREEN)
    for y, a, b, c in ((0.03, "羌", "羊＋人", "西邊的牧羊人"), (-0.10, "姜", "羊＋女", "周人始祖母：姜嫄")):
        T(ax, -0.80, y, a, 34, WHITE)
        T(ax, -0.63, y + 0.02, b, 16, GREEN, ha="left")
        T(ax, -0.63, y - 0.035, c, 12.5, WHITE, w="normal", ha="left")
    T(ax, -0.475, -0.21, "周王室姬姓，世世代代娶姜姓", 13, WHITE, w="normal")
    T(ax, -0.475, -0.27, "（李學勤等：羌、姜同源）", 11.5, GREY, w="normal")


def c03_yi(ax):
    box(ax, 0.03, -0.33, 0.89, 0.55, ec=PURPLE)
    T(ax, 0.475, 0.14, "線索三：虎的族人", 17, PURPLE)
    T(ax, 0.475, 0.05, "彝族：不少學者認為源自古羌", 13.5, WHITE, w="normal")
    T(ax, 0.475, -0.03, "有的支系自稱「羅羅」", 15, PURPLE)
    T(ax, 0.475, -0.10, "＝虎族", 15, PURPLE)
    T(ax, 0.475, -0.19, "劉堯漢提出彝族的「虎宇宙觀」", 12.5, WHITE, w="normal")
    T(ax, 0.475, -0.25, "（田野與民族志，非天文文獻）", 11.5, GREY, w="normal")


def c03_end(ax):
    box(ax, -0.92, -0.93, 1.84, 0.53, ec=RED)
    T(ax, 0.0, -0.48, "線索很誘人，但這是推論，不是定論", 20, RED)
    T(ax, 0.0, -0.565, "「白虎＝西羌」是師大天文社簡報（p.17）的考據觀點；古書沒有直接寫", 13, WHITE, w="normal")
    T(ax, 0.0, -0.66, "另一說：巴人的祖先廩君，死後「魂魄世為白虎」", 15, AMBER)
    T(ax, 0.0, -0.725, "——《後漢書．南蠻西南夷列傳》", 12.5, GREY, w="normal")
    T(ax, 0.0, -0.82, "四象的來源，學界還在討論：圖騰說、星象說、方位與五行配色說……", 12.5, WHITE, w="normal")


# ══════════════════════ C-A12-04 天關客星 ══════════════════════
RA4, DEC4, S4, CX4, CY4 = 80.0, 13.0, 0.038, 0.0, -0.05


def p4(ra, dec):
    return CX4 - (ra - RA4) * math.cos(math.radians(DEC4)) * S4, CY4 + (dec - DEC4) * S4


def in4(x, y):
    return -0.92 < x < 0.92 and -0.50 < y < 0.42


def c04_chart(ax):
    T(ax, 0.0, 0.92, "一〇五四：天關客星", 31, WHITE)
    T(ax, 0.0, 0.845, "宋至和元年五月己丑（1054 年 7 月 4 日）", 16, GREY, w="normal")
    for h, (ra, dec, v) in S.items():
        if v > 5.2:
            continue
        x, y = p4(ra, dec)
        if in4(x, y):
            ax.scatter([x], [y], s=ssize(v, 16, 4), c=WHITE, zorder=5, lw=0, alpha=.95)
    for keys, col in ((["001", "034", "003"], AMBER), (["230"], BLUE)):
        for a, b in segs(*keys):
            (x1, y1), (x2, y2) = p4(*S[a][:2]), p4(*S[b][:2])
            if in4(x1, y1) and in4(x2, y2):
                ax.plot([x1, x2], [y1, y2], c=col, lw=1.8, alpha=.75, zorder=4)
    x, y = p4(*S[A12.ZETA_TAU][:2])
    ax.add_patch(CB.Circle((x, y), 0.03, fc="none", ec=BLUE, lw=2.0, zorder=6))
    T(ax, x - 0.05, y - 0.095, "天關（金牛座 ζ）", 15, BLUE, ha="right")
    for h, lab, dx, dy in ((A12.ALDEBARAN, "畢宿五", 0.0, -0.06), (A12.BETELGEUSE, "參宿四", 0.0, -0.06)):
        x, y = p4(*S[h][:2])
        T(ax, x + dx, y + dy, lab, 13, WHITE, w="normal")
    x, y = p4(*A12.centroid(uniq("001"), S))
    T(ax, x + 0.02, y + 0.15, "畢宿", 16, AMBER)
    x, y = p4(*A12.centroid(uniq("034"), S))
    T(ax, x, y + 0.06, "觜宿", 13, AMBER, w="normal")
    x, y = p4(*A12.centroid(uniq("230"), S))
    T(ax, x, y + 0.06, "天街", 13, BLUE, w="normal")
    T(ax, 0.86, -0.49, "西 →", 12, GREY, w="normal")
    T(ax, -0.86, -0.49, "← 東", 12, GREY, w="normal")


def c04_guest(ax):
    x, y = p4(*A12.M1)
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        r1 = 0.085 if i % 2 == 0 else 0.055
        ax.plot([x + 0.02 * math.cos(a), x + r1 * math.cos(a)], [y + 0.02 * math.sin(a), y + r1 * math.sin(a)],
                c=AMBER, lw=2.4, alpha=.95, zorder=8, solid_capstyle="round")
    ax.scatter([x], [y], s=260, c=AMBER, zorder=9, lw=0)
    ax.scatter([x], [y], s=1400, c=AMBER, zorder=7, lw=0, alpha=.18)
    T(ax, x + 0.10, y + 0.03, "客星", 20, AMBER, ha="left")
    T(ax, x + 0.10, y - 0.025, "（今天的蟹狀星雲 M1）", 12.5, AMBER, w="normal", ha="left")


def c04_quote(ax):
    box(ax, -0.92, -0.93, 1.84, 0.38, ec=AMBER)
    T(ax, 0.0, -0.60, "《宋會要》", 14, AMBER)
    T(ax, 0.0, -0.665, "晨出東方，守天關，晝見如太白，芒角四出，色赤白，凡見二十三日。", 15, WHITE, w="normal")
    T(ax, 0.0, -0.745, "《宋史》", 14, AMBER)
    T(ax, 0.0, -0.81, "至和元年五月己丑，出天關東南可數寸，歲餘稍沒。", 15, WHITE, w="normal")
    T(ax, 0.0, -0.88, "白天看得見 23 天；夜裡看得見一年多", 12, GREY, w="normal")


def c04_today(ax):
    import numpy as np
    cx, cy, r = -0.72, 0.625, 0.15
    ax.add_patch(CB.Circle((cx, cy), r, fc=CB.BG, ec=WHITE, lw=1.4, zorder=10))
    rng = np.random.default_rng(1054)
    for k in range(70):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0.25, 1.0)
        L = rng.uniform(0.15, 0.4)
        x0, y0 = cx + 0.11 * rr * math.cos(a), cy + 0.075 * rr * math.sin(a)
        x1, y1 = x0 + 0.02 * L * math.cos(a), y0 + 0.02 * L * math.sin(a)
        ax.plot([x0, x1], [y0, y1], c=RED if k % 3 else AMBER, lw=1.6, alpha=.75, zorder=11)
    ax.add_patch(CB.Ellipse((cx, cy), 0.22, 0.15, fc=MW, ec="none", alpha=.18, zorder=11))
    ax.add_patch(CB.Ellipse((cx, cy), 0.12, 0.08, fc=MW, ec="none", alpha=.22, zorder=11))
    ax.scatter([cx], [cy], s=30, c=WHITE, zorder=12, lw=0)
    T(ax, cx, cy - 0.185, "蟹狀星雲（示意）", 11.5, WHITE, w="normal")
    box(ax, -0.50, 0.49, 1.42, 0.27, ec=WHITE, z=10)
    for i, (s, sz, col) in enumerate((("今天：超新星的殘骸", 14, WHITE), ("距離約 6,500 光年", 12.5, WHITE),
                                      ("中心的中子星每秒轉約 30 圈", 12.5, WHITE),
                                      ("M1 在天關西北約 1°；史書寫「東南」", 11, GREY),
                                      ("方位怎麼對不上，學界仍在討論", 11, GREY))):
        ax.text(0.21, 0.735 - i * 0.051, s, fontproperties=CB.FP, fontsize=sz, color=col, ha="center",
                va="center", weight="bold" if i == 0 else "normal", zorder=12)


# ══════════════════════ C-A12-05 同一條腰帶（9:16 圖卡） ══════════════════════
ROWS5 = [  # (文化, 原文, 中譯, 顏色)
    ("中國", "參／衡石", "三（三顆星）／一桿秤", AMBER),
    ("布吉斯（印尼）", "Tanra Tèlluè", "三的記號", AMBER),
    ("阿努塔（所羅門群島）", "Ara Toru", "三星之路", AMBER),
    ("羅馬尼亞", "Trisfetitele", "三聖人", AMBER),
    ("薩丁尼亞", "Sas Tres Marias", "三個瑪利亞", AMBER),
    ("白俄羅斯", "Касцы", "割草的人（一個接一個割草）", GREEN),
    ("因紐特", "Ullaktut", "三個獵北極熊時迷路的獵人", GREEN),
    ("阿拉伯（古）", "an-Niẓām", "一串（珠子）", BLUE),
]


def c05_card(ax):
    ax.text(0.5, 0.947, "同一條腰帶", fontproperties=CB.FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, "獵戶腰帶三顆星，全世界都數得出「三」", fontproperties=CB.FP, fontsize=14,
            color=GREY, ha="center", va="center")
    # 三顆星
    ys = 0.835
    for i, (x, v, nm) in enumerate(((0.32, 1.77, "參宿一"), (0.5, 1.69, "參宿二"), (0.68, 2.41, "參宿三"))):
        ax.scatter([x], [ys - 0.010 + 0.010 * i], s=(6.5 - v) ** 2.4 * 14, c=WHITE, lw=0, zorder=5)
        ax.text(x, ys - 0.046 + 0.010 * i, nm, fontproperties=CB.FP, fontsize=10.5, color=GREY, ha="center",
                va="center")
    ax.text(0.10, ys - 0.010, "← 東", fontproperties=CB.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.90, ys + 0.010, "西 →", fontproperties=CB.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.770, "間距 1.39°、1.36°；亮度 1.7–2.4 等——差不多亮、差不多等距", fontproperties=CB.FP,
            fontsize=11.5, color=WHITE, ha="center", va="center")
    ax.plot([0.03, 0.97], [0.745, 0.745], c=WHITE, lw=1.0, alpha=.4)
    ax.text(0.5, 0.722, "用「三」取名", fontproperties=CB.FP, fontsize=15, color=AMBER, ha="center",
            va="center", weight="bold")
    y = 0.695
    for i, (cul, nat, zh, col) in enumerate(ROWS5):
        if i == 5:
            y -= 0.012
            ax.plot([0.03, 0.97], [y + 0.010, y + 0.010], c=WHITE, lw=1.0, alpha=.4)
            ax.text(0.5, y - 0.012, "看成人", fontproperties=CB.FP, fontsize=15, color=GREEN, ha="center",
                    va="center", weight="bold")
            y -= 0.040
        if i == 7:
            y -= 0.012
            ax.plot([0.03, 0.97], [y + 0.010, y + 0.010], c=WHITE, lw=1.0, alpha=.4)
            ax.text(0.5, y - 0.012, "看成東西", fontproperties=CB.FP, fontsize=15, color=BLUE, ha="center",
                    va="center", weight="bold")
            y -= 0.040
        ax.text(0.05, y - 0.012, cul, fontproperties=CB.FP, fontsize=12, color=GREY, ha="left", va="center")
        ax.text(0.95, y - 0.012, nat, fontproperties=CB.FP, fontsize=13, color=col, ha="right", va="center",
                weight="bold")
        ax.text(0.05, y - 0.040, zh, fontproperties=CB.FP, fontsize=13.5, color=WHITE, ha="left", va="center",
                weight="bold")
        y -= 0.062
        ax.plot([0.03, 0.97], [y + 0.008, y + 0.008], c=WHITE, lw=0.6, alpha=.18)
    ax.text(0.5, 0.085, "Stellarium skycultures：chinese／bugis／anutan／romanian／sardinian／",
            fontproperties=CB.FP, fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.065, "belarusian／inuit／arabic；《史記．天官書》", fontproperties=CB.FP, fontsize=10,
            color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=CB.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


# ══════════════════════ C-A12-06 白虎的鄰居（9:16 圖卡） ══════════════════════
SEC6 = [
    ("往南：糧倉與牧場", GREEN, [("天倉", "方的糧倉"), ("天囷", "圓的糧倉"), ("天廩", "存祭祀用的黍稷"),
                                ("天庾", "露天的穀堆"), ("芻藁", "草料堆"), ("天苑", "天子養禽獸的園囿")]),
    ("往北：墳墓與刑罰", RED, [("大陵", "墳墓（大陵五＝Algol，西方說是梅杜莎的頭）"), ("積尸", "大陵裡的屍堆"),
                                ("卷舌", "管口舌、讒言"), ("礪石", "磨刀石")]),
    ("腳下", PURPLE, [("廁", "茅廁"), ("屎", "廁的南邊一顆")]),
    ("昴畢之間", BLUE, [("天街", "街南華夏、街北夷狄（《史記正義》）")]),
]


def c06_card(ax):
    ax.text(0.5, 0.947, "白虎的鄰居", fontproperties=CB.FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.905, "西方屬金、主秋：收成與肅殺，都寫在天上", fontproperties=CB.FP, fontsize=14,
            color=GREY, ha="center", va="center")
    y = 0.872
    for title, col, items in SEC6:
        ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=1.0, alpha=.4)
        ax.text(0.05, y - 0.024, title, fontproperties=CB.FP, fontsize=15, color=col, ha="left",
                va="center", weight="bold")
        y -= 0.048
        for nm, gl in items:
            ax.text(0.07, y - 0.010, nm, fontproperties=CB.FP, fontsize=15, color=col, ha="left",
                    va="center", weight="bold")
            ax.text(0.24, y - 0.010, gl, fontproperties=CB.FP, fontsize=12, color=WHITE, ha="left",
                    va="center")
            y -= 0.034
        y -= 0.006
    ax.plot([0.03, 0.97], [y, y], c=WHITE, lw=1.0, alpha=.4)
    y -= 0.034
    ax.text(0.5, y, "《禮記．月令》孟秋之月", fontproperties=CB.FP, fontsize=13, color=AMBER, ha="center",
            va="center", weight="bold")
    ax.text(0.5, y - 0.036, "「農乃登穀」　　「戮有罪，嚴斷刑」", fontproperties=CB.FP, fontsize=15,
            color=WHITE, ha="center", va="center", weight="bold")
    ax.text(0.5, y - 0.068, "同一個月：收成，也處決", fontproperties=CB.FP, fontsize=12, color=GREY,
            ha="center", va="center")
    ax.text(0.5, 0.065, "星官釋義：《晉書．天文志》；連線：Stellarium chinese", fontproperties=CB.FP,
            fontsize=10, color=GREY, ha="center", va="center")
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=CB.FP, fontsize=13, color=WHITE,
            ha="center", va="center")


# ══════════════════════ C-A12-07 今晚往東看（9:16 圖卡） ══════════════════════
WHEN7 = "2026/12/04 20:00"
AZ7, ALT7, K7, XC7, YC7 = 90.0, 45.0, 0.47 / (2 * math.tan(math.radians(25))), 0.5, 0.455
ASP = 1215 / 2160


def proj7(alt, az):
    """以（方位 90°、高度 45°）為中心的立體投影；東在畫面中央、北在左、南在右"""
    a, z = math.radians(alt), math.radians(az)
    v = (math.cos(a) * math.sin(z), math.cos(a) * math.cos(z), math.sin(a))     # 東、北、上
    a0, z0 = math.radians(ALT7), math.radians(AZ7)
    c = (math.cos(a0) * math.sin(z0), math.cos(a0) * math.cos(z0), math.sin(a0))
    e = (math.cos(z0), -math.sin(z0), 0.0)                                       # 畫面右＝南
    u = (-math.sin(a0) * math.sin(z0), -math.sin(a0) * math.cos(z0), math.cos(a0))
    d = sum(p * q for p, q in zip(v, c))
    if d <= -0.2:
        return None
    X = sum(p * q for p, q in zip(v, e)) * 2 / (1 + d)
    Y = sum(p * q for p, q in zip(v, u)) * 2 / (1 + d)
    return XC7 + X * K7, YC7 + Y * K7 * ASP


def c07_card(ax):
    f = altaz_at(WHEN7)
    ax.text(0.5, 0.955, "今晚往東看", fontproperties=CB.FP, fontsize=30, color=WHITE, ha="center",
            va="center", weight="bold")
    ax.text(0.5, 0.918, "台北　2026/12/4（五）晚上 8:00", fontproperties=CB.FP, fontsize=14, color=GREY,
            ha="center", va="center")
    ok = lambda q: q and 0.02 < q[0] < 0.98 and 0.205 < q[1] < 0.89
    # 地平線與方位
    hz = [proj7(0, az) for az in range(20, 161, 2)]
    hz = [q for q in hz if q]
    ax.plot([q[0] for q in hz], [q[1] for q in hz], c=WHITE, lw=2.0, alpha=.8, zorder=5)
    y_h = min(q[1] for q in hz)
    ax.add_patch(CB.Rectangle((0, 0), 1, y_h, fc="#141A2E", ec="none", zorder=4))
    poly = [(q[0], q[1]) for q in hz] + [(hz[-1][0], 0), (hz[0][0], 0)]
    ax.add_patch(CB.Polygon(poly, closed=True, fc="#141A2E", ec="none", zorder=4))
    for az, lab in ((45, "東北"), (67.5, "東北偏東"), (90, "東"), (112.5, "東南偏東"), (135, "東南")):
        q = proj7(0, az)
        if q and 0.03 < q[0] < 0.97:
            ax.text(q[0], q[1] - 0.018, lab, fontproperties=CB.FP, fontsize=12 if az != 90 else 15,
                    color=WHITE, ha="center", va="center", weight="bold", zorder=6)
    for alt in (30, 60):
        arc = [proj7(alt, az) for az in range(20, 161, 2)]
        arc = [q for q in arc if ok(q)]
        ax.plot([q[0] for q in arc], [q[1] for q in arc], c=WHITE, lw=0.8, alpha=.25, ls=(0, (3, 4)), zorder=3)
        if arc:
            ax.text(arc[-1][0] - 0.01, arc[-1][1] + 0.008, f"{alt}°", fontproperties=CB.FP, fontsize=9,
                    color=GREY, ha="right", va="bottom", zorder=3)
    zq = proj7(90, 0)
    ax.scatter([zq[0]], [zq[1]], s=40, marker="+", c=WHITE, zorder=6)
    ax.text(zq[0] + 0.015, zq[1] + 0.008, "天頂", fontproperties=CB.FP, fontsize=11, color=GREY, ha="left",
            va="bottom", zorder=6)
    # 星
    pos = {}
    for h, (ra, dec, v) in S.items():
        if v > 4.4:
            continue
        alt, az = f(ra, dec)
        if alt < 0:
            continue
        q = proj7(alt, az)
        if ok(q):
            pos[h] = q
            ax.scatter([q[0]], [q[1]], s=ssize(v, 3.2, 1.2), c=WHITE, zorder=7, lw=0)
    for a, b in segs(*A12.SEVEN):
        if a in pos and b in pos:
            ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], c=AMBER, lw=1.6, alpha=.85, zorder=6)
    for k, nm, dx, dy in (("012", "奎宿", 0.0, 0.03), ("014", "婁宿", 0.04, -0.02), ("025", "胃宿", 0.04, 0.0),
                          ("015", "昴宿", 0.05, 0.0), ("001", "畢宿", 0.05, -0.01), ("034", "觜宿", -0.05, 0.0),
                          ("003", "參宿", 0.11, 0.012)):
        hs = [h for h in uniq(k) if h in pos]
        if not hs:
            continue
        x = sum(pos[h][0] for h in hs) / len(hs); y = sum(pos[h][1] for h in hs) / len(hs)
        ax.text(x + dx, y + dy, nm, fontproperties=CB.FP, fontsize=15, color=AMBER, ha="center", va="center",
                weight="bold", zorder=8)
    for h, lab, dx, dy in ((A12.ALDEBARAN, "畢宿五（紅）", 0.0, -0.016), (A12.BETELGEUSE, "參宿四（紅）", 0.0, -0.016)):
        if h in pos:
            ax.text(pos[h][0] + dx, pos[h][1] + dy, lab, fontproperties=CB.FP, fontsize=11, color=WHITE,
                    ha="center", va="center", zorder=8)
    # 說明
    lines = [("獵戶（參宿）18:29–18:43 從正東升起，8 點高約 17–19°", WHITE),
             ("昴宿 8 點高 52°；10:49 幾乎從頭頂正上方經過（高 89°）", WHITE),
             ("月亮 12/5 凌晨 2:51 才升起（殘月 17%）——前半夜沒有月光", AMBER),
             ("方位、高度：PyEphem 自算（含大氣折射）", GREY)]
    for i, (s, col) in enumerate(lines):
        ax.text(0.5, 0.165 - i * 0.033, s, fontproperties=CB.FP, fontsize=11.5 if col != GREY else 10,
                color=col, ha="center", va="center", zorder=9)
    ax.text(0.5, 0.030, "#萬國星空　#師大天文社", fontproperties=CB.FP, fontsize=13, color=WHITE,
            ha="center", va="center", zorder=9)


def main():
    global S
    os.makedirs(OUT, exist_ok=True)
    S = dict(G.load_stars(BASE))
    f = altaz_at(WHEN2)
    for h, nm in ((A12.MINTAKA, "參宿三"), (A12.ALNILAM, "參宿二"), (A12.ALNITAK, "參宿一"),
                  (A12.BETELGEUSE, "參宿四"), (A12.RIGEL, "參宿七"), (80763, "心宿二")):
        alt, az = f(*S[h][:2])
        print(f"  {WHEN2} {nm}: 高 {alt:.2f}°、方位 {az:.1f}°")
    print(f"  腰帶星等：{[S[h][2] for h in (A12.MINTAKA, A12.ALNILAM, A12.ALNITAK)]}")
    CB.emit("", [("三星", c01_stars), ("字形", c01_glyph), ("說明", c01_text)], title="C-A12-01_參字")
    CB.emit("", [("地平", c02_horizon), ("參宿", c02_shen), ("心宿", c02_shang), ("引文", c02_quote)],
            title="C-A12-02_參商")
    CB.emit("", [("墓葬", c03_tomb), ("字形", c03_glyph), ("彝族", c03_yi), ("結論", c03_end)],
            title="C-A12-03_西羌線索")
    CB.emit("", [("星圖", c04_chart), ("客星", c04_guest), ("引文", c04_quote), ("今日", c04_today)],
            title="C-A12-04_天關客星")
    for fn, name in ((c05_card, "C-A12-05_同一條腰帶"), (c06_card, "C-A12-06_白虎的鄰居"),
                     (c07_card, "C-A12-07_今晚往東看")):
        fig, ax = CB.newcard(dark=True)
        fn(ax)
        CB.save(fig, "", f"{name}_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
