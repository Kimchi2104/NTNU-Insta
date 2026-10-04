# -*- coding: utf-8 -*-
"""萬國星空 C 系列共用：背景星空（給 Canva 每頁墊底、用 Match & Move 緩慢旋轉）

畫面：以北天極為中心的真實星空（Stellarium hip_gaia3 星表，≤5.8 等）＋淡銀河。
投影：方位等距（同北盤，RA 順時針遞增＝仰望北天的樣子），
      所以 Canva 裡逆時針轉（rotation 遞減）＝時間往前走。
中央變暗：以圖心為圓心的徑向遮罩，旋轉時不變；概念圖都在中央 1080 方框裡，
      星點在中央只留約 35% 亮度，避免干擾圖上的細線與小字。

Canva 擺法（每頁同一位置，只改 rotation）：
  left −660, top −240, 寬高 2400 → 圖心落在頁面中心 (540, 960)；
  半徑 1200 > 頁面半對角線 1101，所以轉到任何角度都蓋滿整頁。
"""
import math, os, random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import gen_ep_assets as Gx

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = Gx.find_base(HERE)
OUT = os.path.join(BASE, "05_素材", "_C系列共用", "背景星空")

DISP = 2400            # Canva 顯示尺寸（px）
SS = 1.5               # 輸出解析度倍率 → 3600 px
N = int(DISP * SS)
K = 12.0               # 每度幾個顯示 px：赤緯 90° 在圓心，−10° 在圖邊
MAG = 6.5
DIM_IN, DIM_OUT, DIM_MIN = 460, 820, 0.45   # 徑向遮罩（顯示 px）

# Canva 擺放參數（給 Canva 腳本共用）
CANVA = dict(left=-660, top=-240, width=DISP, height=DISP)
FILE = "C系列_背景星空_透明.png"


def xy(ra, dec):
    """方位等距、北極在圖心；回傳顯示 px（數學座標，y 向上）"""
    r = (90.0 - dec) * K
    t = math.radians(ra)
    return r * math.sin(t), r * math.cos(t)


def star_layer():
    S = Gx.load_stars(BASE)
    pts = [(ra, dec, v) for ra, dec, v in S.values() if v <= MAG and dec >= -12]
    xs, ys, ss, al = [], [], [], []
    for ra, dec, v in pts:
        x, y = xy(ra, dec)
        d = min(10.0, max(1.7, (7.0 - v) * 1.45)) * SS      # 直徑（輸出 px）
        xs.append(x * SS); ys.append(y * SS)
        ss.append((d * 72 / 100) ** 2)                      # scatter 的 s 以 pt² 計（dpi=100）
        al.append(min(1.0, 0.55 + (6.5 - v) * 0.12))
    f = plt.figure(figsize=(N / 100, N / 100), dpi=100)
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(-N / 2, N / 2); ax.set_ylim(-N / 2, N / 2)
    ax.axis("off"); f.patch.set_alpha(0); ax.patch.set_alpha(0)
    col = np.ones((len(xs), 4)); col[:, :3] = (0.93, 0.96, 1.0); col[:, 3] = al
    # 亮星加一圈柔光
    big = [i for i, (_, _, v) in enumerate(pts) if v < 3.0]
    ax.scatter([xs[i] for i in big], [ys[i] for i in big], s=[ss[i] * 9 for i in big],
               c=[(0.85, 0.9, 1.0, 0.14)] * len(big), lw=0)
    ax.scatter(xs, ys, s=ss, c=col, lw=0)
    p = os.path.join(OUT, "_tmp_stars.png")
    f.savefig(p, transparent=True); plt.close(f)
    im = Image.open(p).convert("RGBA"); os.remove(p)
    print("  星點", len(pts), "顆")
    return im


def mw_layer():
    random.seed(7)
    G = 900
    h = np.zeros((G, G))
    for _ in range(260000):
        l = random.uniform(0, 360); b = random.gauss(0, 6.5)
        ra, dec = Gx.gal2eq(l, b)
        if dec < -12: continue
        x, y = xy(ra, dec)
        i = int((x / DISP + 0.5) * G); j = int((0.5 - y / DISP) * G)
        if 0 <= i < G and 0 <= j < G: h[j, i] += 1
    g = Image.fromarray((h / h.max() * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))
    a = np.asarray(g).astype(float) / 255.0
    a = np.clip(a / max(a.max(), 1e-6), 0, 1) ** 0.75 * 0.34 * 255
    mw = np.zeros((G, G, 4), np.uint8)
    mw[..., 0], mw[..., 1], mw[..., 2] = 0xC9, 0xDA, 0xF5
    mw[..., 3] = a.astype(np.uint8)
    glow = Image.fromarray(mw, "RGBA").resize((N, N), Image.BICUBIC)
    # 顆粒：沿銀河撒細點（同開頭北盤的質感）
    f = plt.figure(figsize=(N / 100, N / 100), dpi=100)
    ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(-N / 2, N / 2); ax.set_ylim(-N / 2, N / 2)
    ax.axis("off"); f.patch.set_alpha(0); ax.patch.set_alpha(0)
    xs, ys, ss = [], [], []
    for _ in range(45000):
        l = random.uniform(0, 360); b = random.gauss(0, 5.0)
        ra, dec = Gx.gal2eq(l, b)
        if dec < -12: continue
        x, y = xy(ra, dec)
        xs.append(x * SS); ys.append(y * SS); ss.append(random.uniform(0.6, 2.6) * SS)
    ax.scatter(xs, ys, s=ss, c=[(0.79, 0.85, 0.96, 0.42)], lw=0)
    p = os.path.join(OUT, "_tmp_mw.png")
    f.savefig(p, transparent=True); plt.close(f)
    grain = Image.open(p).convert("RGBA"); os.remove(p)
    return Image.alpha_composite(glow, grain)


def radial_mask():
    c = (np.arange(N) + 0.5) / SS - DISP / 2
    r = np.hypot(c[None, :], c[:, None])
    t = np.clip((r - DIM_IN) / (DIM_OUT - DIM_IN), 0, 1)
    t = t * t * (3 - 2 * t)                                 # smoothstep
    return DIM_MIN + (1 - DIM_MIN) * t


def main():
    os.makedirs(OUT, exist_ok=True)
    im = Image.alpha_composite(mw_layer(), star_layer())
    arr = np.asarray(im).astype(float)
    arr[..., 3] *= radial_mask()
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")
    out.save(os.path.join(OUT, FILE), optimize=True)
    print("  ✓", FILE, out.size)


RATE = 1.0          # 每秒轉幾度（逆時針＝時間往前）
DIM_OP = 0.4        # 本身就是星圖的頁（有「星點層」）把背景星空壓暗，避免和主角星混在一起


def page_plan(params):
    """依 _canva/*頁面參數.json 算每頁背景星空的 rotation／opacity。
    卡片頁（全頁黑底圖卡）不放；rotation 以整集中點為 0，隨起始秒數遞減。"""
    pages = [p for p in params if not any("黑底" in L["file"] for L in p["layers"])]
    mid = (pages[0]["start"] + pages[-1]["start"]) / 2
    out = []
    for p in pages:
        star_map = any("星點層" in L["file"] for L in p["layers"])
        out.append(dict(page=p["page"], rotation=round(RATE * (mid - p["start"]), 1),
                        opacity=DIM_OP if star_map else 1.0))
    return out


if __name__ == "__main__":
    main()
