# -*- coding: utf-8 -*-
"""萬國星空｜大畫布引擎 v4（一集一張畫布，圖層依內容分）

畫布結構（單一座標系，長圖上 1 單位＝1°）：

  ┌────────────────────────────┐ y=+y_pole+R_RIM
  │  北盤（完整360°圓盤）        │
  │  ＋整帶填滿（盤投影延伸）     │   ← 盤的左右與上方全部有星，畫布內零黑區
  ├─ 縫合帶 dec +D_s..+D_r ────┤   ← 走廊內：長圖幾何→盤緣幾何連續變形
  │  長圖帶（等距圓柱 x=時角）    │
  ├─ 縫合帶 dec −D_s..−D_r ────┤
  │  南盤＋整帶填滿              │
  └────────────────────────────┘ y=−y_pole−R_RIM

圖層（每層一個 SVG、同 viewBox、疊一次就能剪）：
  {EP}_L1-銀河.svg
  {EP}_L2-星點.svg
  {EP}_L3-經緯線.svg          （含 ±D_r 盤緣緯線圈＝R 鏡頭裁切基準）
  {EP}_L4-星座連線.svg        （一層全含）
  {EP}_L5-標籤-英文.svg
  {EP}_L6-標籤-繁中.svg
  {EP}_L7-標籤-原文{語言}.svg （每語言一層，可多個）
  另出：{EP}_預覽黑底.png、{EP}_SB-分鏡.png、{EP}_鏡頭清單.csv/.json、
        {EP}_畫布資訊.json

動畫語法（Canva，全程 Match & Move，禁溶解／疊影）：
  S 捲動＝整疊水平平移（畫面限長圖帶內）
  T 抬頭＝畫面沿走廊中線平移＋縮放（全疊靜止）
  R 旋轉＝把整疊裁切(Crop)到盤緣緯線圈的外接正方形 → 元素中心＝盤心
          → 直接旋轉（北盤負角、南盤正角，1 小時=15.041°）
  Z 特寫＝純縮放（整帶填滿保證四周不露黑）

幾何鎖定：
  盤緣半徑恆 R_RIM=180/π（盤緣 1° 時角弧長＝長圖水平尺）；
  盤＝均勻極方位等距 r=k(90−|dec|)，k=R_RIM/(90−D_r)；徑向對稱 ⇒
  全盤（含填滿區）繞盤心旋轉＝周日運動，嚴格成立。
  縫合帶＝唯一犧牲準確度處；下緣與長圖、上緣（走廊內）與盤緣逐點重合。
  填滿區＝盤投影往盤緣外延伸（跨過極點後是反面天空倒轉延續 → 畫布內建
  「垂直穿極路徑」，物理正確）；與長圖帶重複收錄同一片天，屬設計取捨，
  重複內容永遠在鏡頭畫面外（驗證器擋）。
  垂直方向無縫拼接在拓撲上不存在（球面≠環面），以整帶填滿＋穿極路徑取代；
  水平方向長圖帶左右邊界天然無縫，Canva 內複製並排即可延長。
"""
import os, sys, re, math, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
from gen_projection import SVG, great_circle, COLORS, horizon_points

D2R = math.pi / 180.0
R_RIM = 180.0 / math.pi

SERIF_CANDIDATES = ["/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
                    "/System/Library/Fonts/Hiragino Mincho ProN.ttc",
                    "/System/Library/Fonts/Supplemental/Songti.ttc"]


def find_serif():
    """標籤字型鏈：明朝體（近似 Canva 筑紫Aオールド明朝）＋西文/符號後備。
    覆蓋：CJK（中日韓）、拉丁含 ʻokina/IAST 變音、西里爾、希臘。
    阿拉伯/希伯來由 DejaVu Sans 後備＋G.rtl() 整形；梵文 Devanagari 沙盒無字型，
    印度文化一律用 pronounce（IAST 轉寫）。"""
    from matplotlib import font_manager
    from matplotlib.font_manager import FontProperties
    fams = []
    for f in SERIF_CANDIDATES + ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            try:
                font_manager.fontManager.addfont(f)
                fams.append(FontProperties(fname=f).get_name())
            except Exception:
                pass
    return FontProperties(family=fams) if fams else G.find_font()


# ═══════════ 防豆腐：字元覆蓋檢查 ═══════════
_GLYPH_FONTS = None
_FONT_FILES = SERIF_CANDIDATES + [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]


def _glyph_fonts():
    global _GLYPH_FONTS
    if _GLYPH_FONTS is None:
        from matplotlib.ft2font import FT2Font
        _GLYPH_FONTS = []
        for f in _FONT_FILES:
            if os.path.exists(f):
                try:
                    _GLYPH_FONTS.append(FT2Font(f))
                except Exception:
                    pass
    return _GLYPH_FONTS


def missing_glyphs(text):
    """回傳 text 中整條字型鏈都畫不出來的字元（先做 RTL 整形＝實際繪製字串）。
    空清單＝安全。任何非空結果都代表會出現豆腐，該標籤必須改寫或換轉寫。"""
    miss = []
    for ch in G.rtl(text):
        if ch.isspace() or ord(ch) < 32:
            continue
        if not any(f.get_char_index(ord(ch)) for f in _glyph_fonts()):
            miss.append(ch)
    return miss


def glyph_audit(texts, verbose=True):
    """IDE 預檢用：批次檢查一組字串。回傳 [(text, [缺字...]), ...]（只含有問題的）"""
    bad = []
    for t in texts:
        m = missing_glyphs(t)
        if m:
            bad.append((t, m))
            if verbose:
                print(f"  ✗ 缺字：「{t}」→ " +
                      "、".join(f"{c}(U+{ord(c):04X})" for c in m))
    if verbose and not bad:
        print(f"  ✓ 防豆腐：{len(texts)} 條標籤全部可繪")
    return bad


def label_box(text, size, font_u=1.7):
    """估算標籤在畫布單位下的寬高（CJK 全形 1.0em、半形 0.55em）"""
    em = size * font_u
    w = em * sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in text)
    return w, em * 1.25


def spread_labels(m, items, iters=90, pad=0.8, pull=0.06, max_shift=12.0,
                  verbose=True):
    """標籤自動避讓（v4.4）：在畫布座標上把互相重疊的標籤推開，只改 dx/dy。

    星官密集的集數（三垣有 60+ 個標籤）純手調 dx/dy 不切實際。作法＝
    質點鬆弛：重疊者沿重疊較小的軸互推，同時有一條彈簧把標籤拉回原始偏移，
    避免飄太遠而認不出屬於哪顆星。回傳新的 items（原 list 不變）。
    """
    out = [dict(it) for it in items]
    P, B, base = [], [], []
    for it in out:
        ra, dec = (m.S[it["hip"]][:2] if "hip" in it else (it["ra"], it["dec"]))
        P.append(m.pos_primary(ra, dec))
        B.append(label_box(it["text"], it.get("size", 1.0), m.fu))
        base.append((it.get("dx", 0.0), it.get("dy", 1.4)))
    d = [list(b) for b in base]
    n = len(out)
    for _ in range(iters):
        moved = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                xi, yi = P[i][0] + d[i][0], P[i][1] + d[i][1]
                xj, yj = P[j][0] + d[j][0], P[j][1] + d[j][1]
                ox = (B[i][0] + B[j][0]) / 2 + pad - abs(xi - xj)
                oy = (B[i][1] + B[j][1]) / 2 + pad - abs(yi - yj)
                if ox <= 0 or oy <= 0:
                    continue
                if oy <= ox:                       # 垂直推開較省距離
                    s = math.copysign(oy / 2 * 0.5, (yi - yj) or 1.0)
                    d[i][1] += s; d[j][1] -= s; moved += abs(s)
                else:
                    s = math.copysign(ox / 2 * 0.5, (xi - xj) or 1.0)
                    d[i][0] += s; d[j][0] -= s; moved += abs(s)
        for i in range(n):                          # 彈簧拉回原偏移
            d[i][0] += (base[i][0] - d[i][0]) * pull
            d[i][1] += (base[i][1] - d[i][1]) * pull
            for k in (0, 1):
                lim = max_shift + abs(base[i][k])
                d[i][k] = max(-lim, min(lim, d[i][k]))
        if moved < 0.01:
            break
    bad = 0
    for i in range(n):
        out[i]["dx"], out[i]["dy"] = round(d[i][0], 2), round(d[i][1], 2)
        for j in range(i + 1, n):
            xi, yi = P[i][0] + d[i][0], P[i][1] + d[i][1]
            xj, yj = P[j][0] + d[j][0], P[j][1] + d[j][1]
            if (abs(xi - xj) < (B[i][0] + B[j][0]) / 2 and
                    abs(yi - yj) < (B[i][1] + B[j][1]) / 2):
                bad += 1
    if verbose:
        print(f"  ·  標籤避讓：{n} 條，殘餘重疊 {bad} 組"
              + ("（可接受）" if bad <= n // 12 else "　⚠ 仍偏多，建議減少標籤"))
    return out


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def wrap(a):
    return (a + 180.0) % 360.0 - 180.0


class Master:
    """一集一張大畫布（v4）。"""

    def __init__(self, ep, stars, outdir, lst=0.0, D_s=45.0, D_r=49.0,
                 w_c=34.0, feather=8.0, x_tN=0.0, x_tS=0.0, phi=None,
                 D_fill=0.0, maglim=5.6, mw_n=15000, seed=42,
                 star_scale=1.0, line_w=0.30, font_u=1.7):
        self.ep, self.S, self.out = ep, stars, outdir
        self.lst, self.Ds, self.Dr = lst, D_s, D_r
        self.wc, self.fe = w_c, feather
        self.xtN, self.xtS, self.phi = x_tN, x_tS, phi
        self.maglim, self.mw_n, self.seed = maglim, mw_n, seed
        self.k = R_RIM / (90.0 - D_r)
        self.Dfill = D_fill
        self.R_fill = self.k * (90.0 - D_fill)   # 填滿圓半徑（完整圓＝旋轉不變邊界）
        band_h = (D_r - D_s) * (1 + self.k) / 2.0
        self.y_pole = D_s + band_h + R_RIM
        hy = self.y_pole + self.R_fill           # 畫布加高：填滿圓不被邊緣切
        self.extent = (-180.0, -hy, 180.0, hy)
        self.ss, self.lw, self.fu = star_scale, line_w, font_u
        self.layers = []
        self.n = 0
        os.makedirs(outdir, exist_ok=True)
        print(f"大畫布 360×{2*hy:.0f} 單位｜盤尺度 k={self.k:.3f}｜盤心 y=±{self.y_pole:.2f}"
              f"｜縫合帶 |dec| {D_s}–{D_r}｜填滿圓至 dec {D_fill:+.0f}（r={self.R_fill:.1f}）"
              f"｜走廊 N@{x_tN} S@{x_tS}")
        for xt, tag in ((x_tN, "北"), (x_tS, "南")):
            if abs(xt) + self.R_fill > 180.0:
                print(f"  ⚠ {tag}盤填滿圓左右會被畫布邊裁到"
                      f"（|x_t|+R_fill={abs(xt)+self.R_fill:.0f}>180）")

    # ═══════════ 座標映射 ═══════════
    def xw(self, ra):
        return wrap(self.lst - ra)

    def p_disc(self, h, d, north):
        xt = self.xtN if north else self.xtS
        dl = math.radians(wrap(h - xt))
        r = self.k * ((90.0 - d) if north else (90.0 + d))
        if north:
            return (xt + r * math.sin(dl), self.y_pole - r * math.cos(dl))
        return (xt + r * math.sin(dl), -self.y_pole + r * math.cos(dl))

    def s_of(self, h, d, north):
        xt = self.xtN if north else self.xtS
        a = abs(wrap(h - xt))
        sd = _smooth((abs(d) - self.Ds) / (self.Dr - self.Ds))
        th = 1.0 if a <= self.wc - self.fe else \
            (0.0 if a >= self.wc else _smooth((self.wc - a) / self.fe))
        return sd * th

    def p_band(self, h, d):
        """長圖帶＋縫合帶（|dec| < D_r）"""
        if abs(d) <= self.Ds:
            return (h, d)
        s = self.s_of(h, d, d > 0)
        pd = self.p_disc(h, d, d > 0)
        return (h * (1 - s) + pd[0] * s, d * (1 - s) + pd[1] * s)

    def disc_ok(self, h, d, north):
        """此天球點是否畫在該盤空間（盤本體＋填滿圓）。
        填滿圓＝r ≤ R_fill 的完整圓（旋轉不變邊界），只避開長圖帶已佔的畫布區。"""
        dd = d if north else -d
        if dd >= self.Dr:
            return True
        r = self.k * (90.0 - dd)
        if r > self.R_fill + 1e-9:
            return False
        p = self.p_disc(h, d, north)
        if abs(p[0]) > 183.0:
            return False
        yy = p[1] if north else -p[1]
        xt = self.xtN if north else self.xtS
        a = abs(wrap(h - xt))
        return (yy > self.Dr) if a > self.wc else (yy > self.y_pole)

    def fill_ok_canvas(self, x, y, north):
        """畫布點是否為該盤（本體＋填滿）內容——旋轉安全掃描用"""
        xt = self.xtN if north else self.xtS
        yc = self.y_pole if north else -self.y_pole
        r = math.hypot(x - xt, y - yc)
        if r <= R_RIM:
            return True
        if r > self.R_fill:
            return False
        yy = y if north else -y
        a = abs(x - xt)
        return (yy > self.Dr) if a > self.wc else (yy > self.y_pole)

    def pos_all(self, ra, dec):
        """該天體在畫布上的所有位置（長圖帶 1 份＋南北盤空間各至多 1 份）"""
        h = self.xw(ra)
        out = []
        if abs(dec) < self.Dr:
            out.append(self.p_band(h, dec))
        for north in (True, False):
            if self.disc_ok(h, dec, north):
                out.append(self.p_disc(h, dec, north))
        return out

    def pos_primary(self, ra, dec):
        """主要位置（標籤只標這裡）：帶內→帶；|dec|≥D_r→該盤本體"""
        h = self.xw(ra)
        if abs(dec) < self.Dr:
            return self.p_band(h, dec)
        return self.p_disc(h, dec, dec > 0)

    # ═══════════ 折線 ═══════════
    def _walk(self, pts, allowed, mapper):
        out, run, prev = [], [], None
        for ra, dec in pts:
            h = self.xw(ra)
            ok = allowed(h, dec)
            p = mapper(h, dec) if ok else None
            if prev is not None and ok != prev[2]:
                d0 = prev[1]
                for b in (self.Dr, -self.Dr):
                    if (d0 - b) * (dec - b) < 0:
                        t = (b - d0) / (dec - d0)
                        hb = prev[0] + wrap(h - prev[0]) * t
                        pb = mapper(hb, b)
                        if prev[2]:
                            run.append(pb)
                        else:
                            if len(run) >= 2:
                                out.append(run)
                            run = [pb]
                        break
            if ok:
                if run and math.hypot(p[0] - run[-1][0], p[1] - run[-1][1]) > 30:
                    if len(run) >= 2:
                        out.append(run)
                    run = []
                run.append(p)
            else:
                if len(run) >= 2:
                    out.append(run)
                run = []
            prev = (h, dec, ok)
        if len(run) >= 2:
            out.append(run)
        return out

    def runs_all(self, pts):
        out = self._walk(pts, lambda h, d: abs(d) < self.Dr, self.p_band)
        for north in (True, False):
            out += self._walk(pts, lambda h, d, n=north: self.disc_ok(h, d, n),
                              lambda h, d, n=north: self.p_disc(h, d, n))
        return out

    # ═══════════ 檔案 ═══════════
    def _new(self):
        return SVG(self.extent, title=f"{self.ep} 大畫布")

    def _write(self, svg, name):
        self.n += 1
        fn = f"{self.ep}_L{self.n}-{name}.svg"
        sz = svg.save(os.path.join(self.out, fn))
        self.layers.append({"n": self.n, "layer": name, "file": fn, "bytes": sz})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB)")
        return fn

    def sz_star(self, v):
        return max(0.05, (6.5 - v)) ** 1.7 * 0.016 * self.ss

    # ═══════════ 圖層 ═══════════
    def _mw_samples(self):
        """銀河取樣：每顆先抽定大小再算位置 → 大畫布與盤檔逐點一致的關鍵"""
        random.seed(self.seed)
        out = []
        for _ in range(self.mw_n):
            l = random.uniform(0, 360); b = random.gauss(0, 6.2)
            ra, dec = G.gal2eq(l, b)
            out.append((ra, dec, random.uniform(.06, .26) * self.ss))
        return out

    def L_milkyway(self, opacity=0.32):
        pts = []
        for ra, dec, sz in self._mw_samples():
            for p in self.pos_all(ra, dec):
                pts.append((p[0], p[1], sz))
        s = self._new()
        s.dots(pts, fill=COLORS["mw"], opacity=opacity, prec=1)
        return self._write(s, "銀河")

    def L_stars(self, mains=()):
        ms = set(mains)
        pts, gl = [], []
        for hip, (ra, dec, v) in self.S.items():
            if v > self.maglim:
                continue
            for p in self.pos_all(ra, dec):
                r = self.sz_star(v)
                if hip in ms:
                    pts.append((p[0], p[1], r * 1.5)); gl.append((p[0], p[1], r * 2.6))
                else:
                    pts.append((p[0], p[1], r))
        s = self._new()
        if gl:
            s.dots(gl, fill=COLORS["white"], opacity=0.18)
        s.dots(pts, fill=COLORS["white"])
        return self._write(s, "星點")

    # ── v4.6：主角星標記（疊在連線「上面」）──────────────────────────
    # 美宣原本手點白點，因為連線 0.30 單位會把 2 等星（r≈0.31）整顆蓋掉。
    # 這層＝主角星的同位置、同大小白點（style="dot"）或指認用細圈（"ring"），
    # 放在連線層之上、標籤層之下；與 L2 星點逐點一致，盤檔也同步出。
    def _mark_parts(self, hips, positions, style):
        dots, rings = [], []
        for h in hips:
            if h not in self.S:
                continue
            v = self.S[h][2]
            r = self.sz_star(v) * 1.5
            for p in positions(h):
                dots.append((p[0], p[1], r))
                rings.append((p[0], p[1], max(1.1, r * 4.0)))
        return dots if style == "dot" else rings

    def _mark_svg(self, s, parts, style):
        if style == "dot":
            s.dots(parts, fill=COLORS["white"])
        else:
            for x, y, r in parts:
                s.circle(x, y, r, stroke=COLORS["white"], w=0.07, opacity=0.85)
        return s

    def L_marks(self, hips, name="主角星白點", style="dot"):
        parts = self._mark_parts(
            hips, lambda h: self.pos_all(*self.S[h][:2]), style)
        if not parts:
            return None
        return self._write(self._mark_svg(self._new(), parts, style), name)

    def D_marks(self, north, hips, name="主角星白點", style="dot"):
        parts = self._mark_parts(
            hips, lambda h: self.pos_disc(*self.S[h][:2], north), style)
        if not parts:
            return None
        return self._write_disc(self._mark_svg(self._new_disc(), parts, style),
                                north, name)

    def L_grid(self, ra_step=30, dec_step=15):
        s = self._new()
        # 緯線
        faint, rim, eq = [], [], []
        for d in range(-75, 76, dec_step):
            pts = [(float(a), float(d)) for a in range(0, 361, 2)]
            (eq if d == 0 else faint).extend(self.runs_all(pts))
        for d in (self.Dr, -self.Dr):        # 盤緣緯線圈＝R 鏡頭裁切基準
            rim += self.runs_all([(float(a), float(d)) for a in range(0, 361, 2)])
        # 經線
        for ra in range(0, 360, ra_step):
            faint += self.runs_all([(float(ra), dd / 2.0) for dd in range(-179, 180)])
        s.polylines(faint, stroke=COLORS["white"], w=0.10, opacity=0.13)
        s.polylines(rim, stroke=COLORS["white"], w=0.14, opacity=0.22)
        s.polylines(eq, stroke=COLORS["white"], w=0.16, opacity=0.38, dash="1.6,1.2")
        return self._write(s, "經緯線")

    def L_lines(self, groups, name="星座連線"):
        """groups = [(segs, color, lw_scale)]，全部進同一層。
        name 可改 → 同一集可出多層連線（例：背景全星官一層＋前景重點一層）。"""
        s = self._new()
        for segs, color, lws in groups:
            runs = []
            for seg in segs:
                hs = [h for h in seg if h in self.S]
                for a, b in zip(hs, hs[1:]):
                    runs += self.runs_all(great_circle(*self.S[a][:2], *self.S[b][:2]))
            s.polylines(runs, stroke=COLORS.get(color, color),
                        w=self.lw * lws, opacity=.92)
        return self._write(s, name)

    def L_labels(self, items, name, serif=True):
        """一個語言一層。items: {hip|ra,dec, text, color, size, dx, dy}
        只標主要位置（帶內＋盤本體），填滿區不標（避免重複標籤）。"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams["svg.fonttype"] = "path"
        FP = find_serif() if serif else G.find_font()
        x0, y0, x1, y1 = self.extent
        W = 13.0
        f = plt.figure(figsize=(W, W * (y1 - y0) / (x1 - x0)), dpi=100)
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
        ax.axis("off"); f.patch.set_alpha(0); ax.patch.set_alpha(0)
        n, skipped = 0, []
        for it in items:
            if "hip" in it:
                if it["hip"] not in self.S:
                    continue
                ra, dec = self.S[it["hip"]][:2]
            else:
                ra, dec = it["ra"], it["dec"]
            m = missing_glyphs(it["text"])
            if m:                                  # 防豆腐：缺字標籤絕不輸出
                skipped.append((it["text"], m))
                continue
            p = self.pos_primary(ra, dec)
            fs = it.get("size", 1.0) * self.fu / (x1 - x0) * W * 72
            ax.text(p[0] + it.get("dx", 0), p[1] + it.get("dy", 1.3),
                    G.rtl(it["text"]), fontproperties=FP, fontsize=fs,
                    color=COLORS.get(it.get("color", "white"), it.get("color", "white")),
                    ha="center", va="center", clip_on=True)
            n += 1
        for t, mm in skipped:
            print(f"  ✗ 防豆腐：「{t}」含缺字 " +
                  "、".join(f"{c}(U+{ord(c):04X})" for c in mm) +
                  "，已跳過——請改轉寫（如 IAST）或修正文字")
        if n == 0:
            plt.close(f)
            print(f"  ·  標籤-{name}：沒有內容，略過")
            return None
        self.n += 1
        fn = f"{self.ep}_L{self.n}-標籤-{name}.svg"
        f.savefig(os.path.join(self.out, fn), format="svg", transparent=True)
        plt.close(f)
        sz = os.path.getsize(os.path.join(self.out, fn))
        self.layers.append({"n": self.n, "layer": f"標籤-{name}", "file": fn,
                            "bytes": sz, "text": True})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB, {n} 標籤)")
        return fn

    # ═══════════ 完整南北星盤圖層組（v4.2） ═══════════
    # 大畫布完全不變；另出每盤一組同結構圖層（L1銀河…L7標籤），內容規則：
    #   ＝大畫布盤區內容的「逐點相同」拷貝（同投影、同尺寸、同亂數序列），
    #   只補上大畫布中被長圖帶佔掉的扇區（同一盤投影延伸到完整圓 r ≤ R_fill）。
    # 切換瞬間（大畫布 ↔ 盤圖層組）畫面內星點/經緯線/標籤零變化；
    # 旋轉在盤圖層組上做，任何角度都連續（完整圓＝旋轉不變）。

    def disc_center(self, north):
        return (self.xtN if north else self.xtS,
                self.y_pole if north else -self.y_pole)

    # ── v4.5：盤圖層組疊回大畫布的精確擺放 ──────────────────────────
    # 常見錯誤：把盤檔跟大畫布「設同寬」。同寬只在「同一個圖層組內」成立
    # （大畫布各層彼此同寬、盤各層彼此同寬）；跨組時盤必須縮到
    #     盤寬 ÷ 畫布寬 = 2·R_fill / 360
    # 且盤心要移到 (x_t, ±y_pole)，不是畫布中心。A-04 這個比值是 0.9903，
    # 只差 1%，肉眼看起來「幾乎對了」但每顆星都差一點——最難抓的情況。
    def disc_placement(self, north=True, canvas_w_px=1080.0):
        """回傳把該盤圖層組疊到大畫布上所需的全部數字（Canva 位置面板可直接用）。

        canvas_w_px＝大畫布元素在版面上的寬度（px）。回傳值：
          盤寬px / 盤心X_px / 盤心Y_px（相對版面左上；假設畫布左上在 (0,0)）
          中心位移X/Y_px（相對畫布中心，Y 向下為正）
          左上X/Y_px（Canva「位置」面板填的就是這兩個）
        """
        x0, y0, x1, y1 = self.extent
        u = canvas_w_px / (x1 - x0)                  # px / 畫布單位
        canvas_h_px = (y1 - y0) * u
        cx, cy = self.disc_center(north)
        w = 2.0 * self.R_fill * u                    # 盤元素寬（＝高，正方形）
        px = (cx - x0) * u                           # 盤心相對畫布左上
        py = (y1 - cy) * u
        return {
            "盤": "北盤" if north else "南盤",
            "畫布寬px": round(canvas_w_px, 2), "畫布高px": round(canvas_h_px, 2),
            "盤寬px": round(w, 2),
            "盤寬佔畫布寬": round(2.0 * self.R_fill / (x1 - x0), 6),
            "盤心X_px": round(px, 2), "盤心Y_px": round(py, 2),
            "盤心X佔畫布寬": round((cx - x0) / (x1 - x0), 6),
            "盤心Y佔畫布高": round((y1 - cy) / (y1 - y0), 6),
            "中心位移X_px": round(px - canvas_w_px / 2.0, 2),
            "中心位移Y_px": round(py - canvas_h_px / 2.0, 2),
            "左上X_px": round(px - w / 2.0, 2), "左上Y_px": round(py - w / 2.0, 2),
            "盤緣圈半徑px": round(R_RIM * u, 2),
            "填滿圈半徑px": round(self.R_fill * u, 2),
            "逐點相同區": "距盤心 ≤ 盤緣圈半徑（dec ±D_r 那圈）；"
                       "圈外的填滿環大畫布只畫非長圖帶側，盤檔畫滿整圈，"
                       "兩者本來就不會一樣（設計如此）",
        }

    def disc_placement_all(self, canvas_w_px=1080.0):
        return [self.disc_placement(True, canvas_w_px),
                self.disc_placement(False, canvas_w_px)]

    def to_disc_local(self, p, north):
        cx, cy = self.disc_center(north)
        return (p[0] - cx, p[1] - cy)

    def pos_disc(self, ra, dec, north):
        """完整盤：r ≤ R_fill 全圓收錄（不再避開長圖帶）。回傳盤內局部座標。"""
        dd = dec if north else -dec
        if self.k * (90.0 - dd) > self.R_fill + 1e-9:
            return []
        return [self.to_disc_local(self.p_disc(self.xw(ra), dec, north), north)]

    def _runs_disc(self, pts, north):
        def allowed(h, d):
            dd = d if north else -d
            return self.k * (90.0 - dd) <= self.R_fill + 1e-9
        def mapper(h, d):
            return self.to_disc_local(self.p_disc(h, d, north), north)
        return self._walk(pts, allowed, mapper)

    def _new_disc(self):
        # v4.5：把「疊回大畫布」的縮放比例寫進 SVG <title>，數字跟著檔案走
        r = 2.0 * self.R_fill / 360.0
        return SVG((-self.R_fill, -self.R_fill, self.R_fill, self.R_fill),
                   title=f"{self.ep} 盤｜盤寬 = 大畫布寬 × {r:.6f}"
                         f"（R_fill={self.R_fill:.3f}，盤緣圈半徑 = 大畫布寬 × "
                         f"{R_RIM / 360.0:.6f}）")

    def _write_disc(self, svg, north, name):
        key = "北盤" if north else "南盤"
        cnt = getattr(self, "_dc", {})
        cnt[key] = cnt.get(key, 0) + 1
        self._dc = cnt
        fn = f"{self.ep}_{key}L{cnt[key]}-{name}.svg"
        sz = svg.save(os.path.join(self.out, fn))
        self.layers.append({"n": f"{key}{cnt[key]}", "layer": f"{key}-{name}",
                            "file": fn, "bytes": sz})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB)")
        return fn

    def D_milkyway(self, north, opacity=0.32):
        pts = []
        for ra, dec, sz in self._mw_samples():     # 同 seed 同序 → 與大畫布逐點一致
            for p in self.pos_disc(ra, dec, north):
                pts.append((p[0], p[1], sz))
        s = self._new_disc()
        s.dots(pts, fill=COLORS["mw"], opacity=opacity, prec=1)
        return self._write_disc(s, north, "銀河")

    def D_stars(self, north, mains=()):
        ms = set(mains)
        pts, gl = [], []
        for hip, (ra, dec, v) in self.S.items():
            if v > self.maglim:
                continue
            for p in self.pos_disc(ra, dec, north):
                r = self.sz_star(v)
                if hip in ms:
                    pts.append((p[0], p[1], r * 1.5)); gl.append((p[0], p[1], r * 2.6))
                else:
                    pts.append((p[0], p[1], r))
        s = self._new_disc()
        if gl:
            s.dots(gl, fill=COLORS["white"], opacity=0.18)
        s.dots(pts, fill=COLORS["white"])
        return self._write_disc(s, north, "星點")

    def D_grid(self, north, ra_step=30, dec_step=15):
        s = self._new_disc()
        faint, rim, eq = [], [], []
        sgn = 1 if north else -1
        for d in range(-75, 76, dec_step):
            pts = [(float(a), float(d)) for a in range(0, 361, 2)]
            (eq if d == 0 else faint).extend(self._runs_disc(pts, north))
        rim += self._runs_disc([(float(a), sgn * self.Dr) for a in range(0, 361, 2)],
                               north)
        if abs(self.Dfill) > 1e-9:                 # 填滿圓外邊界（D_fill≠0 時另畫）
            eq += self._runs_disc([(float(a), sgn * self.Dfill)
                                   for a in range(0, 361, 2)], north)
        for ra in range(0, 360, ra_step):
            faint += self._runs_disc([(float(ra), dd / 2.0)
                                      for dd in range(-179, 180)], north)
        s.polylines(faint, stroke=COLORS["white"], w=0.10, opacity=0.13)
        s.polylines(rim, stroke=COLORS["white"], w=0.14, opacity=0.22)
        s.polylines(eq, stroke=COLORS["white"], w=0.16, opacity=0.38, dash="1.6,1.2")
        return self._write_disc(s, north, "經緯線")

    def D_lines(self, north, groups, name="星座連線"):
        s = self._new_disc()
        for segs, color, lws in groups:
            runs = []
            for seg in segs:
                hs = [h for h in seg if h in self.S]
                for a, b in zip(hs, hs[1:]):
                    runs += self._runs_disc(
                        great_circle(*self.S[a][:2], *self.S[b][:2]), north)
            s.polylines(runs, stroke=COLORS.get(color, color),
                        w=self.lw * lws, opacity=.92)
        return self._write_disc(s, north, name)

    def D_labels(self, north, items, name, serif=True):
        """與大畫布同規則：只標 |dec| ≥ D_r（該盤本體）的標籤，位置逐點相同
        → 切換瞬間標籤零變化。帶內標籤本來就在長圖上，不進盤檔。"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams["svg.fonttype"] = "path"
        FP = find_serif() if serif else G.find_font()
        R = self.R_fill
        W = 13.0
        f = plt.figure(figsize=(W, W), dpi=100)
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(-R, R); ax.set_ylim(-R, R)
        ax.axis("off"); f.patch.set_alpha(0); ax.patch.set_alpha(0)
        n, skipped = 0, []
        for it in items:
            if "hip" in it:
                if it["hip"] not in self.S:
                    continue
                ra, dec = self.S[it["hip"]][:2]
            else:
                ra, dec = it["ra"], it["dec"]
            dd = dec if north else -dec
            if dd < self.Dr and not it.get("disc"):  # 帶內標籤不進盤檔（與大畫布一致）；
                continue                             # disc=True＝盤專用標籤組（B-01：盤上導覽英仙、御夫）
            m = missing_glyphs(it["text"])
            if m:
                skipped.append((it["text"], m))
                continue
            p = self.to_disc_local(self.p_disc(self.xw(ra), dec, north), north)
            fs = it.get("size", 1.0) * self.fu / (2 * R) * W * 72
            ax.text(p[0] + it.get("dx", 0), p[1] + it.get("dy", 1.3),
                    G.rtl(it["text"]), fontproperties=FP, fontsize=fs,
                    color=COLORS.get(it.get("color", "white"), it.get("color", "white")),
                    ha="center", va="center", clip_on=True)
            n += 1
        for t, mm in skipped:
            print(f"  ✗ 防豆腐：「{t}」含缺字 " +
                  "、".join(f"{c}(U+{ord(c):04X})" for c in mm) + "，已跳過")
        key = "北盤" if north else "南盤"
        if n == 0:
            plt.close(f)
            print(f"  ·  {key}標籤-{name}：此盤無標籤，略過")
            return None
        cnt = getattr(self, "_dc", {})
        cnt[key] = cnt.get(key, 0) + 1
        self._dc = cnt
        fn = f"{self.ep}_{key}L{cnt[key]}-標籤-{name}.svg"
        f.savefig(os.path.join(self.out, fn), format="svg", transparent=True)
        plt.close(f)
        sz = os.path.getsize(os.path.join(self.out, fn))
        self.layers.append({"n": f"{key}{cnt[key]}", "layer": f"{key}-標籤-{name}",
                            "file": fn, "bytes": sz, "text": True})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB, {n} 標籤)")
        return fn

    def build_discs(self, groups, label_sets, mains=(), line_sets=(), marks=()):
        """一次產出南北兩盤的完整圖層組。label_sets=[(items, name), ...]
        v4.6：line_sets=[(groups, name), ...] 對應大畫布額外的 L_lines(name=…)；
              marks=[(hips, name, style), ...] 對應 L_marks。順序與大畫布相同：
              星點→連線→（額外連線）→標記→標籤。"""
        for north in (True, False):
            print(f"\n── {'北盤' if north else '南盤'}圖層組（完整圓 r≤{self.R_fill:.1f}）──")
            self.D_milkyway(north)
            self.D_stars(north, mains=mains)
            self.D_grid(north)
            self.D_lines(north, groups)
            for extra, name in line_sets:
                self.D_lines(north, extra, name=name)
            for hips, name, style in marks:
                self.D_marks(north, hips, name=name, style=style)
            for items, name in label_sets:
                self.D_labels(north, items, name)
            self.print_disc_placement(north)

    def print_disc_placement(self, north):
        """v4.5：盤檔一寫完就把「疊回長圖大畫布」要用的縮放比例印出來。
        美宣最常踩的坑＝把盤跟大畫布設同寬（同寬只在同一圖層組內成立）。"""
        p = self.disc_placement(north, 1080.0)
        key = "北盤" if north else "南盤"
        edge = "上緣" if north else "下緣"
        ctr = abs(self.xtN if north else self.xtS) < 1e-9
        print(f"  ▸ {key}疊回大畫布：盤寬 ＝ 大畫布寬 × "
              f"**{p['盤寬佔畫布寬']:.6f}**"
              f"（畫布 1080px → 盤 {p['盤寬px']:.1f}px）")
        if ctr:
            print(f"    然後「水平置中 ＋ 對齊{edge}」即可，誤差 0"
                  f"（畫布高＝2(y_pole+R_fill)，{key}{edge}天生等於畫布{edge}）")
        else:
            print(f"    x_t≠0，不可水平置中：左上角 ＝ ({p['左上X_px']:.1f}, "
                  f"{p['左上Y_px']:.1f}) px @畫布寬1080")
        print(f"    盤心在畫布 ({p['盤心X佔畫布寬']*100:.1f}%, "
              f"{p['盤心Y佔畫布高']*100:.1f}%)；盤緣圈半徑 {p['盤緣圈半徑px']:.1f}px"
              f"（此圈內與大畫布逐點重合）")

    def L_horizon(self):
        """（可選）觀測地地平線。唯一必須獨立、永不移動的層：
        用它時 S 捲動只能移其他層、此層固定。預設不生成。"""
        if self.phi is None:
            return None
        s = self._new()
        s.polylines(self.runs_all(horizon_points(self.phi, self.lst)),
                    stroke=COLORS["horizon"], w=0.30, opacity=.9)
        return self._write(s, "地平線-靜態")

    # ═══════════ 資訊、預覽 ═══════════
    def save_manifest(self, shots=None):
        crop_w = 2 * R_RIM
        info = {"ep": self.ep, "canvas": list(self.extent),
                "unit": "長圖 1 單位＝1°",
                "params": dict(lst=self.lst, D_s=self.Ds, D_r=self.Dr,
                               D_fill=self.Dfill, R_fill=round(self.R_fill, 3),
                               w_c=self.wc, feather=self.fe,
                               x_tN=self.xtN, x_tS=self.xtS,
                               k=round(self.k, 5), y_pole=round(self.y_pole, 3),
                               R_RIM=round(R_RIM, 4), phi=self.phi,
                               maglim=self.maglim),
                "crop": {"小裁切": "盤緣緯線圈（dec ±D_r，稍亮）外接正方形；"
                                 "盤心置中旋轉用，fov≤50",
                         "大裁切": "填滿圓＝天赤道圈（dec ±D_fill 虛線）外接正方形；"
                                 "遠側旋轉用，旋轉角度依驗證器安全範圍",
                         "小裁切寬佔畫布比": round(crop_w / 360.0, 5),
                         "大裁切寬佔畫布比": round(2 * self.R_fill / 360.0, 5),
                         "北盤中心y佔比": round((self.extent[3] - self.y_pole) /
                                            (self.extent[3] - self.extent[1]), 5),
                         "南盤中心y佔比": round((self.extent[3] + self.y_pole) /
                                            (self.extent[3] - self.extent[1]), 5)},
                "盤對位": {"說明": "把盤圖層組疊回大畫布時用；同寬只在同一圖層組"
                                 "內成立，跨組必須按此縮放與位移",
                          "Canva 兩步對齊": [
                              f"① 盤圖層組寬度設為「大畫布寬度 × "
                              f"{2 * self.R_fill / 360.0:.6f}」",
                              "② 北盤：水平置中＋對齊上緣；南盤：水平置中＋"
                              "對齊下緣（畫布高＝2(y_pole+R_fill)，"
                              "故北盤上緣天生等於畫布上緣，誤差 0）"
                              + ("" if abs(self.xtN) < 1e-9 and
                                 abs(self.xtS) < 1e-9 else
                                 "；⚠ 本集 x_t≠0，水平不可置中，改用 左上X_px")],
                          "1080px基準": self.disc_placement_all(1080.0),
                          "2400px基準": self.disc_placement_all(2400.0)},
                "layers": self.layers}
        if shots:
            info["shots"] = shots
        p = os.path.join(self.out, f"{self.ep}_畫布資訊.json")
        json.dump(info, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return p

    def draw_mpl(self, ax, line_groups=(), maglim=None, mw_n=9000, labels=(), disc=None):
        """disc=None：畫大畫布；disc=True／False：畫完整北／南盤（盤心放在大畫布盤心位置），
        縮圖牆的 R 鏡頭用——偏離盤心的取景才看得到長圖側扇區的盤內容（B-01 起）"""
        maglim = maglim or min(self.maglim, 5.2)
        FP = find_serif()
        if disc is None:
            pos_all, runs_all, pos_primary = self.pos_all, self.runs_all, self.pos_primary
        else:
            xt, yc = self.disc_center(disc)
            pos_all = lambda ra, dec: [(p[0] + xt, p[1] + yc)
                                       for p in self.pos_disc(ra, dec, disc)]
            runs_all = lambda pts: [[(x + xt, y + yc) for x, y in r]
                                    for r in self._runs_disc(pts, disc)]
            pos_primary = lambda ra, dec: (pos_all(ra, dec) or [(1e9, 1e9)])[0]
        random.seed(7)
        xs, ys, ss = [], [], []
        for _ in range(mw_n):
            l = random.uniform(0, 360); b = random.gauss(0, 6.2)
            ra, dec = G.gal2eq(l, b)
            for p in pos_all(ra, dec):
                xs.append(p[0]); ys.append(p[1]); ss.append(random.uniform(.2, 1.1))
        ax.scatter(xs, ys, s=ss, c=COLORS["mw"], alpha=.26, lw=0, zorder=1)
        xs, ys, ss = [], [], []
        for hip, (ra, dec, v) in self.S.items():
            if v > maglim:
                continue
            for p in pos_all(ra, dec):
                xs.append(p[0]); ys.append(p[1])
                ss.append(max(.3, (6.3 - v)) ** 1.8 * .38)
        ax.scatter(xs, ys, s=ss, c="#FFFFFF", lw=0, zorder=2)
        for segs, col, _ in line_groups:
            for seg in segs:
                hs = [h for h in seg if h in self.S]
                for a, b in zip(hs, hs[1:]):
                    for r in runs_all(great_circle(*self.S[a][:2], *self.S[b][:2])):
                        ax.plot([p[0] for p in r], [p[1] for p in r],
                                c=COLORS.get(col, col), lw=0.9, alpha=.9, zorder=5)
        for it in labels:
            ra, dec = (self.S[it["hip"]][:2] if "hip" in it else (it["ra"], it["dec"]))
            p = pos_primary(ra, dec)
            # 預覽必須與 L_labels/D_labels 的 dx/dy 一致，否則肉眼 QA 會誤判重疊
            ax.text(p[0] + it.get("dx", 0.0), p[1] + it.get("dy", 1.4),
                    G.rtl(it["text"]), fontproperties=FP,
                    fontsize=it.get("pt", 7),
                    color=COLORS.get(it.get("color", "white"), it.get("color")),
                    ha="center", va="center", zorder=9, clip_on=True)
                                                # v4.6：縮圖牆不裁切會漏字到隔壁格

    def preview(self, path, line_groups=(), labels=(), dpi=105, width_in=15, title=""):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        x0, y0, x1, y1 = self.extent
        f = plt.figure(figsize=(width_in, width_in * (y1 - y0) / (x1 - x0)), dpi=dpi)
        f.patch.set_facecolor(COLORS["bg"])
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
        ax.set_aspect("equal"); ax.axis("off")
        self.draw_mpl(ax, line_groups, labels=labels)
        if title:
            ax.text(x0 + 3, y1 - 3, title, fontproperties=G.find_font(), fontsize=15,
                    color="#FFFFFF", ha="left", va="top", weight="bold", zorder=12)
        f.savefig(path, facecolor=COLORS["bg"]); plt.close(f)
        print(f"  ✓ {os.path.basename(path)}")

    def sb_grid(self, path, shots, line_groups=(), labels=(), cols=8,
                cell_in=1.9, dpi=125, title=""):
        """逐鏡頭 9:16 縮圖牆（v4.3）。疊圖式分鏡在鏡頭數 >8 時會糊成一團，
        美宣真正需要的是「每一格長什麼樣」。每個鏡頭出起／迄兩張。

        R 鏡頭：盤的旋轉在數學上等價於 lst 平移（極方位等距＋徑向對稱），
        故直接以 lst→lst−rot 重繪盤心附近，畫面與 Canva 旋轉逐點相同。"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        FP = G.find_font()
        panels = []
        for sh in shots:
            for i, fr in enumerate(sh["frames"]):
                panels.append((sh, i, fr))
        rows = (len(panels) + cols - 1) // cols
        f = plt.figure(figsize=(cols * cell_in, rows * cell_in * 16 / 9 + 0.5),
                       dpi=dpi)
        f.patch.set_facecolor(COLORS["bg"])
        lst0 = self.lst
        for j, (sh, i, (cx, cy, fov, rot)) in enumerate(panels):
            r, c = divmod(j, cols)
            w, h = 1.0 / cols, 1.0 / rows
            ax = f.add_axes([c * w + .004, 1 - (r + 1) * h + .004,
                             w - .008, h - .008])
            ax.set_facecolor("#05070F")
            for s in ax.spines.values():
                s.set_color("#FF6B6B" if i == 0 else "#8A5A5A"); s.set_lw(1.2)
            ax.set_xticks([]); ax.set_yticks([])
            disc = None
            if sh["kind"] == "R":
                self.lst = lst0 - rot          # 盤旋轉 ≡ lst 平移
                disc = sh.get("north", True)   # v4.7：畫完整盤、照 frame 的 cx,cy 取景（原本一律盤心置中）
            else:
                self.lst = lst0
            hw, hh = fov / 2, fov * 8 / 9
            ax.set_xlim(cx - hw, cx + hw); ax.set_ylim(cy - hh, cy + hh)
            ax.set_aspect("equal")
            self.draw_mpl(ax, line_groups, maglim=min(self.maglim, 5.0),
                          mw_n=4500, labels=labels, disc=disc)
            for phi in (sh.get("horizon") or []) if disc else []:
                # 地平線固定在畫面上：盤轉 rot ≡ lst 平移後，北點在盤心正下方 kφ
                xt, yc = self.disc_center(True)
                pts = []
                for ra, dec in horizon_points(phi, (self.lst - 180.0) % 360.0, n=361):
                    q = self.pos_disc(ra, dec, True)
                    pts.append((q[0][0] + xt, q[0][1] + yc) if q else None)
                run = []
                for q in pts + [None]:
                    if q is None:
                        if len(run) > 1:
                            ax.plot([a for a, b in run], [b for a, b in run], c="#48E39B",
                                    lw=1.2, alpha=.9, zorder=8)
                        run = []
                    else:
                        run.append(q)
            ax.text(.03, .975, f"{sh['code']}{'起' if i == 0 else '迄'}"
                    f"　{sh['kind']}　{sh['sec'] if i == 0 else ''}"
                    + ("s" if i == 0 else ""),
                    transform=ax.transAxes, fontproperties=FP, fontsize=7.5,
                    color="#FFC94A", ha="left", va="top", weight="bold")
            ax.text(.03, .022, f"fov {fov:.0f}"
                    + (f"　rot {rot:+.0f}°" if sh["kind"] == "R" else ""),
                    transform=ax.transAxes, fontproperties=FP, fontsize=6.5,
                    color="#9FB3D9", ha="left", va="bottom")
        self.lst = lst0
        if title:
            f.text(.005, .998, title, fontproperties=FP, fontsize=11,
                   color="#FFFFFF", ha="left", va="top", weight="bold")
        f.savefig(path, facecolor=COLORS["bg"]); plt.close(f)
        print(f"  ✓ {os.path.basename(path)}（{len(panels)} 格）")

    # ═══════════ 覆蓋測試與鏡頭驗證 ═══════════
    def rim_y(self, dx):
        return math.sqrt(max(0.0, R_RIM ** 2 - dx ** 2))

    def covered(self, x, y):
        if abs(y) <= self.Ds:
            return True
        north = y > 0
        xt = self.xtN if north else self.xtS
        yy = abs(y)
        a = abs(x - xt)
        r = math.hypot(x - xt, yy - self.y_pole)
        if r <= R_RIM:
            return True
        if a <= self.wc and yy <= self.y_pole - self.rim_y(min(a, R_RIM - 1e-6)) + 0.1:
            return True                                    # 縫合帶曲面
        if yy <= self.Dr:
            return True                                    # 縫合帶（走廊外水平段）
        if r > self.R_fill:
            return False
        return (yy > self.Dr and a > self.wc) or yy > self.y_pole   # 填滿圓

    def _cut_frames_ok(self, sh):
        """R 鏡頭切點檢查（v4.2）：旋轉本身在完整盤圖層組上做，任何角度都連續；
        唯獨「與大畫布互切」的起訖兩格，畫面內容必須落在大畫布也有顯示的盤區
        （否則硬切瞬間會看到長圖側扇區 ↔ 盤內容的差異）。回傳 (ok, 訊息)。"""
        north = sh.get("north", True)
        xt = self.xtN if north else self.xtS
        yc = self.y_pole if north else -self.y_pole
        bad_ends = []
        for which, (cx, cy, fov, rot) in (("起", sh["frames"][0]),
                                          ("迄", sh["frames"][-1])):
            hw, hh = fov / 2, fov * 8 / 9
            pts = []
            for t in [i / 8 for i in range(9)]:
                pts += [(cx - hw + 2 * hw * t, cy - hh),
                        (cx - hw + 2 * hw * t, cy + hh),
                        (cx - hw, cy - hh + 2 * hh * t),
                        (cx + hw, cy - hh + 2 * hh * t)]
            c, s = math.cos(rot * D2R), math.sin(rot * D2R)
            for px, py in pts:
                dx, dy = px - xt, py - yc
                oxx = xt + dx * c + dy * s          # 該旋轉角時畫面顯示的原內容位置
                oyy = yc - dx * s + dy * c
                if not self.fill_ok_canvas(oxx, oyy, north):
                    bad_ends.append(which)
                    break
        if not bad_ends:
            return True, "起訖切點皆可與大畫布無縫互切"
        return False, (f"{'、'.join(bad_ends)}格畫面含長圖側扇區——該切點不可直接"
                       f"切回大畫布（改切點角度，或前後鏡頭都留在盤圖層組上）")

    def check_shots(self, shots):
        """shots: [{code,kind(S/T/R/Z),north,sec,frames:[(cx,cy,fov,rot)],note}]
        fov＝畫布單位畫面寬（9:16）。R 鏡頭 cx,cy＝畫面在大畫布上的中心
        （盤心置中或遠側皆可，驗證器自動掃旋轉安全角）。"""
        print("\n── 鏡頭驗證 ──")
        ok = True
        for sh in shots:
            for i, (cx, cy, fov, rot) in enumerate(sh["frames"]):
                hw, hh = fov / 2, fov * 8 / 9
                tag = f"{sh['code']}第{i+1}格"
                if sh["kind"] == "S":
                    if abs(cy) + hh > self.Ds:
                        print(f"  ✗ {tag}：S 畫面超出長圖帶（|y|+{hh:.0f}>{self.Ds}）")
                        ok = False
                elif sh["kind"] == "R":
                    north = sh.get("north", True)
                    xt = self.xtN if north else self.xtS
                    yc = self.y_pole if north else -self.y_pole
                    far = max(math.hypot(cx + sx * hw - xt, cy + sy * hh - yc)
                              for sx in (-1, 1) for sy in (-1, 1))
                    if far > self.R_fill - 0.5:
                        print(f"  ✗ {tag}：R 畫面角落距盤心 {far:.1f} 超出填滿圓 "
                              f"{self.R_fill:.1f}")
                        ok = False
                else:
                    for sx in (-1, 1):
                        for sy in (-1, 1):
                            if not self.covered(cx + sx * hw, cy + sy * hh):
                                print(f"  ✗ {tag}：角落 ({cx+sx*hw:.0f},{cy+sy*hh:.0f}) "
                                      f"無內容")
                                ok = False
                if sh["kind"] == "T":
                    xt = self.xtN if sh.get("north", True) else self.xtS
                    if abs(cx - xt) > 2:
                        print(f"  ✗ {tag}：T 應沿走廊中線 x={xt}")
                        ok = False
                    if hw > self.wc - self.fe - 1:
                        print(f"  ⚠ {tag}：T 半寬 {hw:.0f} 逼近走廊全權區 "
                              f"{self.wc-self.fe:.0f}")
            if sh["kind"] == "R":
                good, info = self._cut_frames_ok(sh)
                if good:
                    print(f"  ✓ {sh['code']}：旋轉 {sh['frames'][0][3]:+.0f}°→"
                          f"{sh['frames'][-1][3]:+.0f}°（盤圖層組上任意角皆連續；{info}）")
                else:
                    print(f"  ⚠ {sh['code']}：{info}")
        print("  ✓ 全部鏡頭在安全範圍" if ok else "  ✗ 有鏡頭超界，請修正")
        return ok


# ═══════════ 幾何自測 ═══════════
def seam_test(m, n=200):
    import random as rd
    rd.seed(1)
    lo = hi = 0.0
    for north in (True, False):
        sgn = 1 if north else -1
        xt = m.xtN if north else m.xtS
        for _ in range(n):
            h = xt + rd.uniform(-m.wc + m.fe, m.wc - m.fe)
            a = m.p_band(h, sgn * (m.Ds - 1e-9)); b = (h, sgn * m.Ds)
            lo = max(lo, math.hypot(a[0] - b[0], a[1] - b[1]))
            a = m.p_band(h, sgn * (m.Dr - 1e-7))
            b = m.p_disc(h, sgn * m.Dr, north)
            hi = max(hi, math.hypot(a[0] - b[0], a[1] - b[1]))
    ok = lo < 1e-6 and hi < 1e-4
    print(f"  {'✓' if ok else '✗'} 縫合帶重合：下緣 {lo:.2e}、上緣 {hi:.2e}")
    return ok


def chirality_test(m):
    import numpy as np
    def sho(tri, north):
        ps = [m.p_disc(m.xw(m.S[h][0]), m.S[h][1], north) for h in tri]
        return sum(ps[i][0] * ps[(i + 1) % 3][1] - ps[(i + 1) % 3][0] * ps[i][1]
                   for i in range(3)) / 2
    def det(tri):
        vs = [(math.cos(m.S[h][1] * D2R) * math.cos(m.S[h][0] * D2R),
               math.cos(m.S[h][1] * D2R) * math.sin(m.S[h][0] * D2R),
               math.sin(m.S[h][1] * D2R)) for h in tri]
        return np.linalg.det(np.array(vs))
    ok = True
    for tri, north, nm in [([54061, 53910, 58001], True, "北斗"),
                           ([60718, 62434, 61084], False, "南十字")]:
        if any(h not in m.S for h in tri):
            continue
        good = (sho(tri, north) > 0) == (det(tri) < 0)
        ok &= good
        print(f"  {'✓' if good else '✗'} {nm} 手性（{'北' if north else '南'}盤）")
    return ok


def suture_jacobian_test(m, n=400):
    import random as rd
    rd.seed(2)
    bad = 0
    for north in (True, False):
        xt = m.xtN if north else m.xtS
        sgn = 1 if north else -1
        for _ in range(n):
            h = xt + rd.uniform(-m.wc, m.wc)
            d = sgn * rd.uniform(m.Ds + .01, m.Dr - .01)
            e = 0.05
            p0 = m.p_band(h, d); ph = m.p_band(h + e, d); pd = m.p_band(h, d + e * sgn)
            J = (ph[0] - p0[0]) * (pd[1] - p0[1]) - (ph[1] - p0[1]) * (pd[0] - p0[0])
            if J * sgn <= 0:
                bad += 1
    print(f"  {'✓' if bad == 0 else '✗'} 縫合帶無摺疊（{bad}/{2*n} 異常）")
    return bad == 0


def disc_identity_test(m, n=400):
    """大畫布盤區 ↔ 完整盤檔 逐點一致性：凡大畫布有畫的盤內容，
    盤檔在同一天球點的（局部座標＋盤心）必須完全相同。銀河亂數序列亦驗證。"""
    import random as rd
    rd.seed(9)
    worst = 0.0
    for _ in range(n):
        ra = rd.uniform(0, 360); dec = rd.uniform(-89, 89)
        h = m.xw(ra)
        for north in (True, False):
            if not m.disc_ok(h, dec, north):
                continue
            pm = m.p_disc(h, dec, north)
            pl = m.pos_disc(ra, dec, north)
            if not pl:
                worst = 99; continue
            cx, cy = m.disc_center(north)
            worst = max(worst, math.hypot(pl[0][0] + cx - pm[0],
                                          pl[0][1] + cy - pm[1]))
    # 銀河：同一取樣序列在兩邊的大小必須一致（_mw_samples 共用即保證，抽查前 50 顆）
    a = [(round(r, 6), round(d, 6), round(s, 6)) for r, d, s in m._mw_samples()[:50]]
    b = [(round(r, 6), round(d, 6), round(s, 6)) for r, d, s in m._mw_samples()[:50]]
    ok = worst < 1e-9 and a == b
    print(f"  {'✓' if ok else '✗'} 盤檔與大畫布逐點一致（最大偏差 {worst:.2e}；"
          f"銀河序列{'一致' if a == b else '不一致'}）")
    return ok


def disc_svg_registration_test(m, layer="L2-星點", tol=0.02, verbose=True):
    """v4.5：直接讀「已寫出的 SVG」驗證盤圖層組能不能疊回大畫布盤區。

    disc_identity_test 驗的是幾何函式；這一支驗的是**檔案**——把大畫布的圓
    平移 −盤心 之後，盤本體（距盤心 ≤ R_RIM）的每一個圓都必須在盤檔找到
    同半徑、同位置的圓（容差＝SVG 兩位小數的捨入）。
    盤緣圈外的填滿環不列入：大畫布只畫非長圖帶側，盤檔畫滿整圈，本來就不同。
    """
    circ = re.compile(r'<circle cx="(-?[\d.]+)" cy="(-?[\d.]+)" r="([\d.]+)"')

    def load(fn):
        p = os.path.join(m.out, fn)
        if not os.path.exists(p):
            return None
        return [(float(a), float(b), float(r))
                for a, b, r in circ.findall(open(p, encoding="utf-8").read())]

    cL = load(f"{m.ep}_{layer}.svg")
    if cL is None:
        if verbose:
            print(f"  – 盤檔對位：找不到 {m.ep}_{layer}.svg，略過")
        return True
    ok, worst_all = True, 0.0
    for north in (True, False):
        key = "北盤" if north else "南盤"
        cD = load(f"{m.ep}_{key}{layer}.svg")
        if cD is None:
            continue
        cx, cy = m.disc_center(north)
        conv, cell = {}, 1.0
        for x, y, r in cL:                        # 大畫布 → 盤局部 SVG 座標
            lx, ly = x - cx, y + cy               # SVG y 已翻轉，故是 +cy
            conv.setdefault((int(math.floor(lx)), int(math.floor(ly))),
                            []).append((lx, ly, r))
        bad, worst, n_in = 0, 0.0, 0
        for x, y, r in cD:
            if math.hypot(x, y) > R_RIM:          # 填滿環不比
                continue
            n_in += 1
            best = 9e9
            gx, gy = int(math.floor(x)), int(math.floor(y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for px, py, pr in conv.get((gx + dx, gy + dy), []):
                        if abs(pr - r) > 0.002:
                            continue
                        best = min(best, math.hypot(px - x, py - y))
            if best > tol:
                bad += 1
            else:
                worst = max(worst, best)
        worst_all = max(worst_all, worst)
        good = bad == 0
        ok = ok and good
        if verbose:
            if good:
                print(f"  ✓ {key}檔可疊回大畫布：盤本體 {n_in} 圓全部命中")
            else:
                print(f"  ✗ {key}檔 {bad}/{n_in} 圓對不上大畫布")
    if verbose and ok:
        print(f"    （最大偏差 {worst_all:.3f} 單位＝SVG 兩位小數捨入；"
              f"盤寬須設為畫布寬×{2*m.R_fill/360.0:.6f}）")
    return ok


def selftest(m):
    print("── 幾何自測 ──")
    return (seam_test(m) and chirality_test(m) and suture_jacobian_test(m)
            and disc_identity_test(m))


if __name__ == "__main__":
    BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
    S = G.load_stars(BASE)
    m = Master("TEST", S, "/tmp/master_v4", lst=195, D_s=45, D_r=49, phi=19.7)
    selftest(m)
    print("── 防豆腐自測（全專案文字系統） ──")
    glyph_audit(["角宿一", "みなみのうお", "삼태성", "Hōkūleʻa ʻokina",
                 "Kṛttikā ṛṣi", "Долоон бурхан", "الثريا", "רָקִיעַ",
                 "Śravaṇā", "Ke Ka o Makaliʻi", "कृत्तिका"])
