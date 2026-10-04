# -*- coding: utf-8 -*-
"""萬國星空｜盤圖層組 ↔ 大畫布「完全重疊」檢驗與對位表（v4.5）

要回答的問題：北盤／南盤圖層組能不能和大畫布上的同一個盤完全重疊？

答案分兩區，這支工具把兩區分開量：
  ① 盤本體＝距盤心 ≤ R_RIM（＝ dec ±D_r 那圈盤緣緯線圈）
     → 必須 100% 逐點重合。這是 T迄→R起 硬切不穿幫的依據。
  ② 填滿環＝R_RIM < r ≤ R_fill
     → 大畫布只畫「非長圖帶側」的扇區，盤檔畫滿整圈。
       盤檔多出來的星是設計要的（旋轉任何角度都不露黑），不是錯位。

對位公式（跨圖層組時「同寬」不成立）：
    盤元素寬 = 大畫布元素寬 × (2·R_fill / 360)
    盤心位置 = 畫布左上 + (x_t + 180, y_hi ∓ y_pole) × (畫布寬/360)

用法：
    python3 check_disc_align.py                 # 跑全部有素材的集數
    python3 check_disc_align.py A-04 A-02       # 只跑指定集數
"""
import os, re, sys, csv, math, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
MAT = os.path.join(BASE, "05_素材")
R_RIM = 180.0 / math.pi

CIRC = re.compile(r'<circle cx="(-?[\d.]+)" cy="(-?[\d.]+)" r="([\d.]+)"')


def circles(path):
    if not os.path.exists(path):
        return None
    return [(float(a), float(b), float(r))
            for a, b, r in CIRC.findall(open(path, encoding="utf-8").read())]


def registration(cL, cD, cx, cy, tol=0.02):
    """cL＝大畫布圓、cD＝盤檔圓（皆 SVG 座標）。(cx,cy)＝盤心的畫布數學座標。
    回傳 (盤本體總數, 盤本體對不上數, 盤本體最大偏差,
          填滿環總數, 填滿環大畫布無對應數)"""
    g = {}
    for x, y, r in cL:
        lx, ly = x - cx, y + cy          # SVG y 已翻轉 → 平移量取 +cy
        g.setdefault((int(math.floor(lx)), int(math.floor(ly))), []).append((lx, ly, r))
    n_in = bad_in = n_out = bad_out = 0
    worst = 0.0
    for x, y, r in cD:
        best = 9e9
        gx, gy = int(math.floor(x)), int(math.floor(y))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for px, py, pr in g.get((gx + dx, gy + dy), []):
                    if abs(pr - r) > 0.002:
                        continue
                    best = min(best, math.hypot(px - x, py - y))
        if math.hypot(x, y) <= R_RIM:
            n_in += 1
            if best > tol:
                bad_in += 1
            else:
                worst = max(worst, best)
        else:
            n_out += 1
            if best > tol:
                bad_out += 1
    return n_in, bad_in, worst, n_out, bad_out


def placement(P, ext, north, W):
    x0, y0, x1, y1 = ext
    u = W / (x1 - x0)
    H = (y1 - y0) * u
    cx = P["x_tN"] if north else P["x_tS"]
    cy = P["y_pole"] if north else -P["y_pole"]
    w = 2 * P["R_fill"] * u
    px, py = (cx - x0) * u, (y1 - cy) * u
    return dict(盤=("北盤" if north else "南盤"),
                畫布寬px=round(W, 1), 畫布高px=round(H, 1),
                盤寬px=round(w, 1), 盤寬佔畫布寬=round(2 * P["R_fill"] / (x1 - x0), 6),
                盤心X_px=round(px, 1), 盤心Y_px=round(py, 1),
                中心位移X_px=round(px - W / 2, 1), 中心位移Y_px=round(py - H / 2, 1),
                左上X_px=round(px - w / 2, 1), 左上Y_px=round(py - w / 2, 1),
                盤緣圈半徑px=round(R_RIM * u, 1), 填滿圈半徑px=round(P["R_fill"] * u, 1))


def verify_png(ep, folder, P, ext, north, out):
    """對位驗證圖：紅空心圈＝大畫布、綠實心點＝盤檔。
    綠點正中紅圈＝對位正確。左：整個盤方框；右：×14 放大，看得出零偏差。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    key = "北盤" if north else "南盤"
    cL = circles(os.path.join(folder, f"{ep}_L2-星點.svg"))
    cD = circles(os.path.join(folder, f"{ep}_{key}L2-星點.svg"))
    if cL is None or cD is None:
        return None
    cx = P["x_tN"] if north else P["x_tS"]
    cy = P["y_pole"] if north else -P["y_pole"]
    Rf, Dr, wc, yp = P["R_fill"], P["D_r"], P["w_c"], P["y_pole"]

    def is_disc(xm, ym):
        """畫布數學座標的這一點，是不是「該盤的內容」（而不是長圖帶）"""
        r = math.hypot(xm - cx, ym - cy)
        if r <= R_RIM:
            return True
        if r > Rf:
            return False
        yy = ym if north else -ym
        return (yy > Dr) if abs(xm - cx) > wc else (yy > (yp if north else -yp))

    disc_pts, band_pts = [], []
    for x, y, r in cL:                      # SVG → 盤局部；同時取回數學座標
        lx, ly = x - cx, y + cy
        if max(abs(lx), abs(ly)) > Rf * 1.05:
            continue
        (disc_pts if is_disc(x, -y) else band_pts).append((lx, ly, r))

    f = plt.figure(figsize=(13.2, 7.3), dpi=135)
    f.patch.set_facecolor("#05070F")
    FP = _font()
    # ── 左：整個盤方框 ──
    axA = f.add_axes([0.005, 0.02, 0.485, 0.86])
    axB = f.add_axes([0.505, 0.02, 0.485, 0.86])
    for ax in (axA, axB):
        ax.set_facecolor("#05070F"); ax.set_aspect("equal"); ax.axis("off")
    axA.set_xlim(-Rf * 1.03, Rf * 1.03); axA.set_ylim(Rf * 1.03, -Rf * 1.03)
    if band_pts:
        axA.scatter([p[0] for p in band_pts], [p[1] for p in band_pts],
                    s=[(p[2] * 26) ** 2 for p in band_pts], c="#3A4356",
                    lw=0, zorder=1)
    axA.scatter([p[0] for p in disc_pts], [p[1] for p in disc_pts],
                s=[(p[2] * 40) ** 2 + 9 for p in disc_pts], facecolors="none",
                edgecolors="#FF4B3E", lw=.55, zorder=3)
    axA.scatter([p[0] for p in cD], [p[1] for p in cD],
                s=[(p[2] * 26) ** 2 + 1.2 for p in cD], c="#34E36B", lw=0,
                zorder=4)
    axA.add_patch(plt.Circle((0, 0), R_RIM, fill=False, ec="#6FA8FF", lw=1.5,
                             zorder=6))
    axA.add_patch(plt.Circle((0, 0), Rf, fill=False, ec="#FFC94A", lw=1.2,
                             ls="--", zorder=6))
    axA.plot([0], [0], marker="+", ms=14, mew=1.5, c="#FFFFFF", zorder=7)
    bb = dict(fc="#05070F", ec="none", pad=1.6)
    axA.text(0, -R_RIM - 2.5, "盤緣圈 R_RIM＝57.30　此圈內必須逐點重合",
             color="#6FA8FF", ha="center", va="bottom", fontsize=9,
             fontproperties=FP, zorder=8, bbox=bb)
    axA.text(0, -Rf * .995, f"填滿圈 R_fill＝{Rf:.1f}", color="#FFC94A",
             ha="center", va="bottom", fontsize=9, fontproperties=FP,
             zorder=8, bbox=bb)
    # ── 右：找一個星多的地方放大 ×14 ──
    best, bxy = -1, (0.0, 0.0)
    for ang in range(0, 360, 12):
        for rad in (R_RIM * .35, R_RIM * .65, R_RIM * .92):
            ox = rad * math.cos(math.radians(ang))
            oy = rad * math.sin(math.radians(ang))
            n = sum(1 for x, y, r in cD if abs(x - ox) < 4 and abs(y - oy) < 4)
            if n > best:
                best, bxy = n, (ox, oy)
    zx, zy, ZW = bxy[0], bxy[1], 4.2
    axB.set_xlim(zx - ZW, zx + ZW); axB.set_ylim(zy + ZW, zy - ZW)
    axB.scatter([p[0] for p in disc_pts], [p[1] for p in disc_pts],
                s=[(p[2] * 300) ** 2 + 40 for p in disc_pts], facecolors="none",
                edgecolors="#FF4B3E", lw=1.5, zorder=3)
    axB.scatter([p[0] for p in cD], [p[1] for p in cD],
                s=[(p[2] * 190) ** 2 + 6 for p in cD], c="#34E36B", lw=0,
                zorder=4)
    axB.add_patch(plt.Rectangle((zx - ZW, zy - ZW), 2 * ZW, 2 * ZW, fill=False,
                                ec="#2B3550", lw=1.2))
    axA.add_patch(plt.Rectangle((zx - ZW, zy - ZW), 2 * ZW, 2 * ZW, fill=False,
                                ec="#FFFFFF", lw=1.8, zorder=9))
    axA.annotate("放大處", xy=(zx + ZW, zy - ZW), xytext=(zx + ZW + 14,
                 zy - ZW - 14), color="#FFFFFF", fontsize=9,
                 fontproperties=FP, zorder=10,
                 arrowprops=dict(arrowstyle="-", color="#FFFFFF", lw=1.0))
    axB.text(zx, zy + ZW * .96,
             f"×{Rf/ZW:.0f} 放大（右圖框＝左圖白框）：綠點必須在紅圈正中央",
             color="#9FB3D9", ha="center", va="bottom", fontsize=9,
             fontproperties=FP)

    f.text(.5, .985, f"{ep}　{key}圖層組 ↔ 大畫布盤區　對位驗證",
           color="#FFFFFF", ha="center", va="top", fontsize=15,
           fontproperties=FP, weight="bold")
    f.text(.5, .952,
           f"紅空心圈＝大畫布　綠實心點＝盤檔　灰＝大畫布的長圖帶（不屬於盤）"
           f"　｜　盤元素寬 ＝ 大畫布元素寬 × {2*Rf/360:.6f}"
           f"，盤心置於畫布 (x={(P['x_tN'] if north else P['x_tS'])+180:.0f}, "
           f"y={ext[3]-(cy):.1f}) / 360 處",
           color="#9FB3D9", ha="center", va="top", fontsize=9.2,
           fontproperties=FP)
    f.text(.5, .922,
           "藍圈內＝100% 逐點重合（T迄→R起 硬切的依據）；"
           "藍圈與黃虛線圈之間的綠點是盤檔獨有的『填滿環』——"
           "大畫布那一側被長圖帶佔用，故意的，不是錯位",
           color="#7C8BA8", ha="center", va="top", fontsize=8.6,
           fontproperties=FP)
    f.savefig(out, facecolor="#05070F"); plt.close(f)
    return out


_FP = None


def _font():
    global _FP
    if _FP is None:
        sys.path.insert(0, HERE)
        import gen_ep_assets as G
        _FP = G.find_font()
    return _FP


def run(ep, folder):
    info = json.load(open(os.path.join(folder, f"{ep}_畫布資訊.json"),
                          encoding="utf-8"))
    P, ext = info["params"], info["canvas"]
    # y_pole 在 JSON 是三位小數 → 用參數重算，避免捨入污染
    P = dict(P)
    P["y_pole"] = P["D_s"] + (P["D_r"] - P["D_s"]) * (1 + P["k"]) / 2.0 + R_RIM
    print(f"\n══════ {ep} ══════")
    print(f"  R_fill={P['R_fill']:.3f}　y_pole={P['y_pole']:.4f}　"
          f"x_tN={P['x_tN']}　x_tS={P['x_tS']}")
    print(f"  盤寬 ÷ 畫布寬 = {2*P['R_fill']/360:.6f}"
          + ("　← 只差 1%，最容易誤以為『同寬』" if 2*P['R_fill']/360 > 0.97 else ""))
    print(f"  Canva 兩步：① 盤寬＝畫布寬×{2*P['R_fill']/360:.6f}　"
          f"② 北盤水平置中＋對齊上緣／南盤水平置中＋對齊下緣"
          + ("" if abs(P['x_tN']) < 1e-9 else "（本集 x_t≠0，水平不可置中）"))
    cL = circles(os.path.join(folder, f"{ep}_L2-星點.svg"))
    rows, allok = [], True
    for north in (True, False):
        key = "北盤" if north else "南盤"
        cD = circles(os.path.join(folder, f"{ep}_{key}L2-星點.svg"))
        if cD is None:
            continue
        cx = P["x_tN"] if north else P["x_tS"]
        cy = P["y_pole"] if north else -P["y_pole"]
        n_in, bad_in, worst, n_out, bad_out = registration(cL, cD, cx, cy)
        allok = allok and bad_in == 0
        print(f"  {'✓' if bad_in == 0 else '✗'} {key}　盤本體(r≤{R_RIM:.1f}) "
              f"{n_in} 圓：對不上 {bad_in}，最大偏差 {worst:.4f} 單位"
              f"（＝{worst*60:.2f} 角分）")
        print(f"      填滿環 {n_out} 圓：大畫布無對應 {bad_out} 個"
              f"（{100*bad_out/max(1,n_out):.0f}%，設計上就該多）")
        for W in (1080.0, 2400.0):
            rows.append(placement(P, ext, north, W))
        png = os.path.join(folder, f"{ep}_盤對位驗證_{key}.png")
        if verify_png(ep, folder, P, ext, north, png):
            print(f"      ✓ {os.path.basename(png)}")
    if rows:
        p = os.path.join(folder, f"{ep}_盤對位.csv")
        with open(p, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print(f"      ✓ {ep}_盤對位.csv")
        info["盤對位"] = {"說明": "同寬只在同一圖層組內成立；跨組必須按此縮放位移",
                        "Canva 兩步對齊": [
                            f"① 盤圖層組寬度設為「大畫布寬度 × "
                            f"{2 * P['R_fill'] / 360:.6f}」",
                            "② 北盤：水平置中＋『對齊上緣』；南盤：水平置中＋"
                            "『對齊下緣』。因為畫布高＝2(y_pole+R_fill)，"
                            "北盤上緣天生就等於畫布上緣、南盤下緣等於畫布下緣，"
                            f"誤差為 0（本集 x_t={P['x_tN']}，非 0 時水平不可置中，"
                            "要改用左上X_px）"],
                        "盤寬佔畫布寬": round(2 * P["R_fill"] / 360, 6),
                        "盤心X佔畫布寬": round((P["x_tN"] + 180) / 360, 6),
                        "北盤心Y佔畫布高": round((ext[3] - P["y_pole"]) /
                                            (ext[3] - ext[1]), 6),
                        "南盤心Y佔畫布高": round((ext[3] + P["y_pole"]) /
                                            (ext[3] - ext[1]), 6),
                        "逐點相同區": "距盤心 ≤ R_RIM=57.2958（dec ±D_r 盤緣圈）",
                        "表": rows}
        json.dump(info, open(os.path.join(folder, f"{ep}_畫布資訊.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=2)
    return allok


if __name__ == "__main__":
    want = sys.argv[1:]
    found = sorted(glob.glob(os.path.join(MAT, "*", "*", "*_畫布資訊.json")) +
                   glob.glob(os.path.join(MAT, "*", "*_畫布資訊.json")))
    ok = True
    for p in found:
        ep = os.path.basename(p).replace("_畫布資訊.json", "")
        if want and ep not in want:
            continue
        ok = run(ep, os.path.dirname(p)) and ok
    print("\n" + ("✓ 全部集數：盤本體 100% 逐點重合"
                  if ok else "✗ 有集數對不上，見上"))
