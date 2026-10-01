# -*- coding: utf-8 -*-
"""萬國星空｜星圖投影與向量輸出引擎 v2

解決 v1 的三個結構性問題：
  ① 極盤與長條圖接不起來 —— 兩者「朝北極」的螢幕方向不同（盤上朝盤心、
     長條圖上朝畫面正上方），只有盤緣某一個方位同向，正對面差 180°，
     人眼看星座折線就讀成「鏡像」。幾何上不可能靠旋轉接合（環面攤不平）。
     → 解法：低緯↔高緯的視線轉移不再拼接，改用「一張」以路徑中點為中心的
       立體投影（Stereographic）橋接盤，全程只需一次 Match & Move 平移＋縮放。
  ② PNG 放大出現鋸齒 → 全部圖層改輸出向量 SVG（含銀河）。
  ③ 沒有拼接預覽 → 見 gen_camera.py（分鏡預覽圖＋鏡頭清單）。

三種投影（每一種只允許一種物理正確的 Canva 動畫）：
  Equirect  x = LST − RA, y = Dec   → 水平平移 ＝ 時間（周日運動），嚴格成立
  Stereo    以任意點為中心的立體投影 → 平移／縮放 ＝ 視線轉移。正形投影，
                                       星座形狀不變形、絕不鏡像
  Stereo(dec0=±90) ＝ 極盤            → 繞盤心旋轉 ＝ 時間，物理精確

座標單位一律是「盤度」(plate degree)：在投影參考點上 1 單位 ＝ 天空 1 度。
"""
import os, sys, math, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G

D2R, R2D = math.pi / 180.0, 180.0 / math.pi

COLORS = {"amber": "#FFC94A", "blue": "#6FA8FF", "white": "#FFFFFF", "red": "#FF6B6B",
          "green": "#7BD88F", "purple": "#B78AFF", "mw": "#C9DAF5", "bg": "#0B0F1E",
          "horizon": "#48E39B"}


# ════════════════════════════════════════════════════════════════════
#  投影
# ════════════════════════════════════════════════════════════════════
def _uvec(ra, dec):
    a, d = ra * D2R, dec * D2R
    return (math.cos(d) * math.cos(a), math.cos(d) * math.sin(a), math.sin(d))


def _radec(v):
    x, y, z = v
    return math.degrees(math.atan2(y, x)) % 360.0, math.degrees(math.asin(max(-1, min(1, z))))


def great_circle(ra1, dec1, ra2, dec2, n=None):
    """大圓插值。長線在任何投影上都必須畫成曲線，直線一律是假的。"""
    p1, p2 = _uvec(ra1, dec1), _uvec(ra2, dec2)
    dot = max(-1.0, min(1.0, sum(a * b for a, b in zip(p1, p2))))
    om = math.acos(dot)
    if om < 1e-9:
        return [(ra1, dec1), (ra2, dec2)]
    if n is None:
        n = max(6, min(96, int(math.degrees(om) * 1.6)))
    out = []
    s = math.sin(om)
    for i in range(n + 1):
        t = i / n
        k1, k2 = math.sin((1 - t) * om) / s, math.sin(t * om) / s
        out.append(_radec([k1 * p1[j] + k2 * p2[j] for j in range(3)]))
    return out


def horizon_points(phi, lst=0.0, n=721):
    """觀測地地平線（alt = 0 的大圓），以方位角參數化 → 連續閉合、無假斷點。
    回傳 [(ra, dec), ...]。在 x=時角 的等距圓柱盤上，這條線固定不動。"""
    p = phi * D2R
    out = []
    for i in range(n):
        A = 2 * math.pi * i / (n - 1)
        dec = math.asin(math.cos(p) * math.cos(A))
        sH = -math.sin(A) / max(1e-9, math.cos(dec))
        cH = -math.sin(dec) * math.sin(p) / max(1e-9, math.cos(dec) * math.cos(p))
        H = math.atan2(sH, cH)
        out.append(((lst - math.degrees(H)) % 360.0, math.degrees(dec)))
    return out


class Proj:
    kind = "?"
    tag = "?"

    def fwd(self, ra, dec):
        raise NotImplementedError

    def mag(self, ra, dec):
        """局部放大率（正形投影為純量；非正形回傳 (徑向, 切向) 的幾何平均）"""
        return 1.0

    def inside(self, ra, dec):
        return self.fwd(ra, dec) is not None

    # ── 折線 → 螢幕多段（自動處理越界斷開）──
    def runs(self, pts):
        out, run = [], []
        for ra, dec in pts:
            p = self.fwd(ra, dec)
            if p is None or (run and self._break(run[-1], p)):
                if len(run) >= 2:
                    out.append(run)
                run = [] if p is None else [p]
                continue
            run.append(p)
        if len(run) >= 2:
            out.append(run)
        return out

    def _break(self, a, b):
        return False

    def line(self, ra1, dec1, ra2, dec2):
        return self.runs(great_circle(ra1, dec1, ra2, dec2))


class Equirect(Proj):
    """等距圓柱．x ＝ 時角（LST − RA），東在左、西在右，面南視角。
    水平平移 ＝ 周日運動（數學上嚴格），可無縫循環。"""
    kind, tag = "equirect", "帶"

    def __init__(self, lst=0.0, dec_lo=-72.0, dec_hi=72.0, tile=3, margin=0.0):
        self.lst, self.lo, self.hi = lst, dec_lo, dec_hi
        self.tile = tile                      # 水平重複次數（3 ＝ 左中右，可捲 ±360°）
        self.margin = margin
        self.half = 180.0 * tile
        self.extent = (-self.half, dec_lo - margin, self.half, dec_hi + margin)

    def x0(self, ra):
        return ((self.lst - ra + 180.0) % 360.0) - 180.0

    def offsets(self):
        return [(i - (self.tile - 1) / 2.0) * 360.0 for i in range(self.tile)]

    def xs(self, ra):
        """回傳此赤經在拼接盤上的所有 x（tile 份）"""
        x = self.x0(ra)
        return [x + o for o in self.offsets()]

    def fwd(self, ra, dec):
        if not (self.lo <= dec <= self.hi):
            return None
        return (self.x0(ra), dec)

    def mag(self, ra, dec):
        return 1.0 / max(1e-6, math.cos(dec * D2R))     # 水平拉伸倍率

    def mag_v(self, ra, dec):
        return 1.0

    def _break(self, a, b):
        return abs(a[0] - b[0]) > 180.0

    def runs_tiled(self, pts):
        """把一條折線畫在所有拼接位上"""
        base = self.runs(pts)
        return [[(x + off, y) for x, y in r] for off in self.offsets() for r in base]


class Stereo(Proj):
    """立體投影（正形）．r ＝ 2·tan(θ/2)，換算成盤度。
    ＊正形＝局部形狀完全不變形，星座折線絕不鏡像、絕不歪斜。
    ＊dec0 = ±90 時就是極盤，繞盤心旋轉 ＝ 周日運動（物理精確）。
    ＊放大率 2/(1+cosθ)：θ=45° →1.17×，60° →1.33×，75° →1.61×，90° →2.0×"""
    kind, tag = "stereo", "盤"

    def __init__(self, ra0, dec0, radius=75.0, roll=0.0, ra_top=None,
                 half_w=None, half_h=None):
        self.ra0, self.dec0, self.radius = ra0 % 360.0, dec0, radius
        self._ra_top = ra_top if ra_top is not None else ra0 % 360.0
        if ra_top is not None:                    # 指定哪個赤經朝畫面正上方
            roll = self._roll_for_top(ra_top)
        self.roll = roll
        r = self.r_of(radius)
        hw = half_w if half_w is not None else r
        hh = half_h if half_h is not None else r
        self.extent = (-hw, -hh, hw, hh)
        self._c0, self._s0 = math.cos(dec0 * D2R), math.sin(dec0 * D2R)
        self._cr, self._sr = math.cos(roll * D2R), math.sin(roll * D2R)

    # ── 依鏡頭路徑自動決定盤的大小（保證畫面永遠不會露出黑邊）──
    @classmethod
    def fit(cls, ra0, dec0, path, fov_true, aspect=16 / 9, ra_top=None, pad=1.05):
        """path = [(ra,dec), ...] 畫面中心會走過的天球點；fov_true = 畫面寬度（真實天度）
        回傳一張剛好夠大的 Stereo：內容半徑蓋得住所有畫面角落，外框不留多餘空白。"""
        probe = cls(ra0, dec0, radius=178.0, ra_top=ra_top)
        need_r, xs, ys = 0.0, [], []
        for ra, dec in path:
            q = probe.fwd(ra, dec)
            if q is None:
                continue
            hw = fov_true * probe.mag(ra, dec) / 2.0 * pad
            hh = hw * aspect
            xs += [q[0] - hw, q[0] + hw]; ys += [q[1] - hh, q[1] + hh]
            for sx in (-1, 1):
                for sy in (-1, 1):
                    need_r = max(need_r, math.hypot(q[0] + sx * hw, q[1] + sy * hh))
        theta = min(178.0, 2.0 * math.degrees(math.atan(need_r * D2R / 2.0)))
        return cls(ra0, dec0, radius=theta, ra_top=ra_top,
                   half_w=max(abs(min(xs)), abs(max(xs))),
                   half_h=max(abs(min(ys)), abs(max(ys))))

    @staticmethod
    def r_of(theta_deg):
        return math.degrees(2.0 * math.tan(min(theta_deg, 179.0) * D2R / 2.0))

    def _roll_for_top(self, ra_top):
        """ra_top ＝ 要朝畫面正上方的赤經子午線。
        非極盤：該子午線的「北」（赤緯增加方向）朝上 —— 就是一般星圖的北上東左。
        極盤：極點在盤心，改用該子午線往外一度的方向朝上。"""
        if self.dec0 >= 89.9:
            probe = (ra_top, 89.0)
        elif self.dec0 <= -89.9:
            probe = (ra_top, -89.0)
        else:
            probe = (ra_top, min(89.9, self.dec0 + 1.0))
        p = self.fwd_raw(*probe)
        if p is None or math.hypot(*p) < 1e-12:
            return 0.0
        return 90.0 - math.degrees(math.atan2(p[1], p[0]))

    def theta(self, ra, dec):
        return G.ang_dist(self.ra0, self.dec0, ra, dec)

    def fwd_raw(self, ra, dec):
        d, da = dec * D2R, (ra - self.ra0) * D2R
        c0 = math.cos(self.dec0 * D2R); s0 = math.sin(self.dec0 * D2R)
        den = 1.0 + s0 * math.sin(d) + c0 * math.cos(d) * math.cos(da)
        if den < 1e-9:
            return None
        k = 2.0 / den
        xe = k * math.cos(d) * math.sin(da)                       # 東
        yn = k * (c0 * math.sin(d) - s0 * math.cos(d) * math.cos(da))
        return (-math.degrees(xe), math.degrees(yn))              # 東在左＝裸眼視角

    def fwd(self, ra, dec):
        if self.theta(ra, dec) > self.radius:
            return None
        p = self.fwd_raw(ra, dec)
        if p is None:
            return None
        x, y = p
        return (x * self._cr - y * self._sr, x * self._sr + y * self._cr)

    def mag(self, ra, dec):
        return 2.0 / (1.0 + math.cos(self.theta(ra, dec) * D2R))

    mag_v = mag


class PolarEquidistant(Proj):
    """等距方位（＝舊版 05_素材/全天星盤 的投影）。只為相容舊素材保留。
    切向在赤道處已拉伸 1.57×、Dec −30 處 2.4×，新素材請一律改用 Stereo。"""
    kind, tag = "polar_eq", "盤"

    def __init__(self, north=True, dec_edge=-30.0, ra_top=0.0):
        self.north, self.ra_top = north, ra_top
        self.edge = dec_edge
        self.R = (90 - dec_edge) if north else (90 + dec_edge)
        self.extent = (-self.R, -self.R, self.R, self.R)

    def fwd(self, ra, dec):
        t = (ra - self.ra_top) * D2R
        if self.north:
            r = 90.0 - dec
            if r > self.R: return None
            return (r * math.sin(t), r * math.cos(t))
        r = 90.0 + dec
        if r > self.R: return None
        return (-r * math.sin(t), r * math.cos(t))

    def mag(self, ra, dec):
        th = (90.0 - dec if self.north else 90.0 + dec) * D2R
        return th / max(1e-6, math.sin(th))


# ════════════════════════════════════════════════════════════════════
#  向量 SVG 輸出（自寫，只用 circle / path / polyline —— 相容性最高）
# ════════════════════════════════════════════════════════════════════
class SVG:
    """盤度座標直接當 SVG 使用者座標；y 在寫檔時翻轉（SVG 的 y 向下）。
    同一張盤的所有圖層共用 viewBox，匯入 Canva 後等比放到同尺寸即完全對齊。"""

    def __init__(self, extent, bg=None, title=""):
        self.x0, self.y0, self.x1, self.y1 = extent
        self.w, self.h = self.x1 - self.x0, self.y1 - self.y0
        self.parts = []
        self.bg, self.title = bg, title
        self._open = 0

    # ── 基本圖元 ──
    def group(self, gid, **attr):
        a = "".join(f' {k.replace("_","-")}="{v}"' for k, v in attr.items())
        self.parts.append(f'<g id="{gid}"{a}>')
        self._open += 1
        return self

    def end(self):
        if self._open:
            self.parts.append("</g>")
            self._open -= 1
        return self

    def dots(self, pts, fill="#FFFFFF", opacity=None, prec=2):
        """pts = [(x, y, r), ...]．prec 降到 1 可再省 ~15% 檔案大小（銀河用）"""
        op = f' opacity="{opacity:.3f}"' if opacity is not None else ""
        self.parts.append(f'<g fill="{fill}"{op}>')
        ap = self.parts.append
        for x, y, r in pts:
            ap(f'<circle cx="{x:.{prec}f}" cy="{-y:.{prec}f}" r="{r:.3f}"/>')
        ap("</g>")
        self.n_nodes = getattr(self, "n_nodes", 0) + len(pts)
        return self

    def polylines(self, runs, stroke="#FFFFFF", w=1.0, opacity=1.0, dash=None,
                  cap="round"):
        if not runs:
            return self
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<g fill="none" stroke="{stroke}" stroke-width="{w:.3f}" '
            f'stroke-opacity="{opacity:.3f}" stroke-linecap="{cap}" '
            f'stroke-linejoin="round"{d}>')
        for r in runs:
            if len(r) < 2:
                continue
            self.parts.append('<path d="M ' +
                              " L ".join(f"{x:.2f} {-y:.2f}" for x, y in r) + '"/>')
        self.parts.append("</g>")
        return self

    def circle(self, cx, cy, r, stroke=None, w=1.0, fill="none", opacity=1.0, dash=None):
        s = f' stroke="{stroke}" stroke-width="{w:.3f}"' if stroke else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<circle cx="{cx:.2f}" cy="{-cy:.2f}" r="{r:.3f}" '
                          f'fill="{fill}" opacity="{opacity:.3f}"{s}{d}/>')
        return self

    def rect(self, x, y, w, h, stroke=None, sw=1.0, fill="none", opacity=1.0, dash=None):
        s = f' stroke="{stroke}" stroke-width="{sw:.3f}"' if stroke else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x:.2f}" y="{-(y+h):.2f}" width="{w:.2f}" '
                          f'height="{h:.2f}" fill="{fill}" opacity="{opacity:.3f}"{s}{d}/>')
        return self

    def poly_fill(self, runs, fill="#000000", opacity=1.0):
        self.parts.append(f'<g fill="{fill}" fill-opacity="{opacity:.3f}" stroke="none">')
        for r in runs:
            if len(r) < 3:
                continue
            self.parts.append('<path d="M ' +
                              " L ".join(f"{x:.2f} {-y:.2f}" for x, y in r) + ' Z"/>')
        self.parts.append("</g>")
        return self

    def save(self, path):
        while self._open:
            self.end()
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
                f'viewBox="{self.x0:.2f} {-self.y1:.2f} {self.w:.2f} {self.h:.2f}" '
                f'width="{self.w:.2f}" height="{self.h:.2f}">')
        body = [head]
        if self.title:
            body.append(f"<title>{self.title}</title>")
        if self.bg:
            body.append(f'<rect x="{self.x0:.2f}" y="{-self.y1:.2f}" '
                        f'width="{self.w:.2f}" height="{self.h:.2f}" fill="{self.bg}"/>')
        body += self.parts
        body.append("</svg>")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write("\n".join(body))
        return os.path.getsize(path)


# ════════════════════════════════════════════════════════════════════
#  盤（Plate）＝ 一種投影 ＋ 一組圖層
# ════════════════════════════════════════════════════════════════════
class Plate:
    """一張盤。所有圖層共用 extent，各自存成一個 SVG（Canva 疊圖用）。
    檔名格式  {EP}_P{n}-{盤名}_L{k}-{層名}.svg
      P 編號 ＝ 拼接／出場順序，L 編號 ＝ 由下往上的堆疊順序（照字母排序即正確）"""

    LAYER_ORDER = ["銀河", "星點", "網格", "參考線", "地平線", "星線", "星名", "題辭"]

    def __init__(self, ep, idx, name, proj, stars, outdir, maglim=5.6,
                 mw_n=16000, star_scale=1.0, line_w=None, seed=42):
        self.ep, self.idx, self.name = ep, idx, name
        self.p, self.S, self.out = proj, stars, outdir
        self.maglim, self.mw_n, self.seed = maglim, mw_n, seed
        self.k = 0
        os.makedirs(outdir, exist_ok=True)
        x0, y0, x1, y1 = proj.extent
        self.extent = proj.extent
        self.span = max(x1 - x0, y1 - y0)
        # ref ＝ 盤高（≈ 一屏視野的量級）；所有筆畫尺寸都以它為基準，
        # 這樣長條圖拼 3 份也不會讓星點跟著變成 3 倍大。
        self.ref = y1 - y0
        self.ss = star_scale * self.ref / 180.0
        self.lw = line_w if line_w is not None else self.ref * 0.010
        self.files = []
        self.manifest = {"plate": name, "idx": idx, "proj": proj.kind,
                         "extent": list(proj.extent), "layers": []}

    # ── 檔名 ──
    def _fn(self, layer, ext="svg"):
        self.k += 1
        return f"{self.ep}_P{self.idx}-{self.name}_L{self.k}-{layer}.{ext}"

    def _new(self, bg=None):
        return SVG(self.extent, bg=bg, title=f"{self.ep} {self.name}")

    def _write(self, svg, layer, moves=True, skip_empty=True):
        if skip_empty and not svg.parts:
            print(f"  ·  {layer}：此盤上沒有內容，略過")
            return None
        fn = self._fn(layer)
        sz = svg.save(os.path.join(self.out, fn))
        self.files.append(fn)
        self.manifest["layers"].append({"n": self.k, "layer": layer, "file": fn,
                                        "bytes": sz, "moves": moves})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB)")
        return fn

    # ── 幾何工具 ──
    def _runs(self, pts):
        if isinstance(self.p, Equirect):
            return self.p.runs_tiled(pts)
        return self.p.runs(pts)

    def _pos(self, ra, dec):
        """回傳此天體在盤上的所有位置（Equirect 拼接時有多份）"""
        if isinstance(self.p, Equirect):
            if not (self.p.lo <= dec <= self.p.hi):
                return []
            return [(x, dec) for x in self.p.xs(ra)]
        q = self.p.fwd(ra, dec)
        return [q] if q else []

    def sz(self, v):
        return max(0.4, (6.3 - v)) ** 1.8 * 0.040 * self.ss

    # ── 圖層 ──
    def L_milkyway(self, color=None, opacity=0.34):
        random.seed(self.seed)
        pts = []
        for _ in range(self.mw_n):
            l = random.uniform(0, 360); b = random.gauss(0, 6.2)
            ra, dec = G.gal2eq(l, b)
            for x, y in self._pos(ra, dec):
                pts.append((x, y, random.uniform(.10, .42) * self.ss))
        s = self._new()
        s.dots(pts, fill=color or COLORS["mw"], opacity=opacity, prec=1)
        return self._write(s, "銀河")

    def L_stars(self, mains=(), glow=True):
        ms = set(mains)
        pts, gl = [], []
        for h, (ra, dec, v) in self.S.items():
            if v > self.maglim:
                continue
            for x, y in self._pos(ra, dec):
                r = self.sz(v)
                if h in ms:
                    pts.append((x, y, r * 1.55))
                    if glow:
                        gl.append((x, y, r * 2.7))
                else:
                    pts.append((x, y, r))
        s = self._new()
        if gl:
            s.dots(gl, fill=COLORS["white"], opacity=0.18)
        s.dots(pts, fill=COLORS["white"])
        return self._write(s, "星點")

    def L_grid(self, ra_step=30, dec_step=15, opacity=0.13):
        s = self._new()
        runs = []
        for h in range(0, 360, ra_step):
            runs += self._runs([(h, d) for d in range(-88, 89, 2)])
        for d in range(-75, 76, dec_step):
            if d == 0:
                continue
            runs += self._runs([(a, d) for a in range(0, 361, 3)])
        s.polylines(runs, stroke=COLORS["white"], w=self.lw * 0.28, opacity=opacity)
        return self._write(s, "網格")

    def L_refs(self, phi=None, opacity=0.55):
        """天赤道／天頂線／拱極界線"""
        s = self._new()
        eq = self._runs([(a, 0.0) for a in range(0, 361, 2)])
        s.polylines(eq, stroke=COLORS["white"], w=self.lw * 0.55, opacity=opacity,
                    dash=f"{self.lw*2.2:.2f},{self.lw*1.6:.2f}")
        if phi is not None:
            cp = 90.0 - abs(phi)
            for d, c in [(phi, COLORS["amber"]), (cp, COLORS["horizon"]),
                         (-cp, COLORS["horizon"])]:
                r = self._runs([(a, d) for a in range(0, 361, 2)])
                s.polylines(r, stroke=c, w=self.lw * 0.5, opacity=opacity * .9,
                            dash=f"{self.lw*3.2:.2f},{self.lw*2.0:.2f}")
        return self._write(s, "參考線")

    def L_horizon(self, phi, lst=None, shade=0.62, fill_below=True):
        """觀測地地平線（一個大圓，以方位角參數化＝連續閉合曲線，不會有假斷點）。
        在 Equirect 上它是一條固定不動的曲線 → 星圖捲動、地平線不動，完全正確。"""
        lst = self.p.lst if (lst is None and isinstance(self.p, Equirect)) else (lst or 0.0)
        s = self._new()
        if fill_below and isinstance(self.p, Equirect):
            s.poly_fill(self._below_horizon_polys(phi, lst), fill="#000000",
                        opacity=shade)
        runs = self._runs(horizon_points(phi, lst))
        s.polylines(runs, stroke=COLORS["horizon"], w=self.lw * 0.85, opacity=.95)
        s.polylines(self._runs([(lst, d) for d in range(-88, 89, 2)]),
                    stroke=COLORS["white"], w=self.lw * 0.4, opacity=.5,
                    dash=f"{self.lw*2.4:.2f},{self.lw*2.0:.2f}")
        # ★ 地平線在「時角」座標裡是固定的 → 這一層在 Canva 裡不可以跟著星圖移動
        return self._write(s, "地平線", moves=not isinstance(self.p, Equirect))

    def _below_horizon_polys(self, phi, lst):
        """Equirect 專用：地平線以下的遮罩多邊形（東側、西側、永不升帶）"""
        pr = self.p
        east, west, never = [], [], []
        d = pr.lo
        while d <= pr.hi + 1e-9:
            t = -math.tan(phi * D2R) * math.tan(min(89.9, max(-89.9, d)) * D2R)
            if t > 1:
                never.append(d)
            elif t >= -1:
                H = math.degrees(math.acos(t))
                east.append((-H, d)); west.append((H, d))
            d += 0.5
        out = []
        k = (pr.tile - 1) // 2
        for off in [360.0 * i for i in range(-k, k + 1)]:
            if east:
                out.append([(-180 + off, east[0][1])] +
                           [(x + off, y) for x, y in east] +
                           [(-180 + off, east[-1][1])])
                out.append([(180 + off, west[0][1])] +
                           [(x + off, y) for x, y in west] +
                           [(180 + off, west[-1][1])])
            if never:
                out.append([(-180 + off, never[0]), (180 + off, never[0]),
                            (180 + off, never[-1]), (-180 + off, never[-1])])
        return out

    def L_lines(self, segs, color="amber", name="星線", lw_scale=1.0,
                max_distort=None):
        """畫星線。max_distort：圖上長度/真實角距 超過此值一律不畫
        （Equirect 高緯必用；Stereo 為正形投影，預設不需要）"""
        if max_distort is None:
            max_distort = 2.5 if isinstance(self.p, Equirect) else 6.0
        c = COLORS.get(color, color)
        runs, dropped = [], 0
        for seg in segs:
            hs = [h for h in seg if h in self.S]
            for a, b in zip(hs, hs[1:]):
                ra1, dec1, _ = self.S[a]; ra2, dec2, _ = self.S[b]
                dtrue = G.ang_dist(ra1, dec1, ra2, dec2)
                rr = self._runs(great_circle(ra1, dec1, ra2, dec2))
                if dtrue > 0.1 and rr:
                    dmap = max(math.hypot(r[-1][0] - r[0][0], r[-1][1] - r[0][1])
                               for r in rr)
                    if dmap / dtrue > max_distort:
                        dropped += 1
                        continue
                runs += rr
        s = self._new()
        s.polylines(runs, stroke=c, w=self.lw * lw_scale, opacity=.95)
        fn = self._write(s, name)
        if dropped:
            print(f"      （失真守門捨棄 {dropped} 段）")
        return fn

    # ── 文字層：交由 matplotlib 轉成路徑（不依賴 Canva 有無中文字型）──
    def L_text(self, items, name="星名", color="white", size=None):
        """items = [{"ra":,"dec":,"text":,"dy":,"color":,"size":} 或 {"hip":...}]
        以 svg.fonttype='path' 輸出：文字變成向量路徑，任何機器都不會掉字。"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams["svg.fonttype"] = "path"
        FP = G.find_font()
        x0, y0, x1, y1 = self.extent
        W = 12.0
        f = plt.figure(figsize=(W, W * (y1 - y0) / (x1 - x0)), dpi=100)
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
        ax.axis("off"); f.patch.set_alpha(0); ax.patch.set_alpha(0)
        base = size or self.ref * 0.040          # 文字高度 ≈ 盤高的 4%
        n = 0
        for it in items:
            if "hip" in it:
                if it["hip"] not in self.S:
                    continue
                ra, dec, _ = self.S[it["hip"]]
            else:
                ra, dec = it["ra"], it["dec"]
            for x, y in self._pos(ra, dec):
                fs = (it.get("size", 1.0) * base) / (x1 - x0) * W * 72
                ax.text(x + it.get("dx", 0.0), y + it.get("dy", self.ref * 0.045),
                        G.rtl(it["text"]), fontproperties=FP, fontsize=fs,
                        color=COLORS.get(it.get("color", color), it.get("color", color)),
                        ha="center", va="center", weight="bold", clip_on=True)
                n += 1
        fn = self._fn(name)
        f.savefig(os.path.join(self.out, fn), format="svg", transparent=True)
        plt.close(f)
        sz = os.path.getsize(os.path.join(self.out, fn))
        self.files.append(fn)
        self.manifest["layers"].append({"n": self.k, "layer": name, "file": fn,
                                        "bytes": sz, "text": True})
        print(f"  ✓ {fn}  ({sz/1024:.0f} KB, {n} 個標籤)")
        return fn

    # ── 黑底合成預覽（PNG，給人看的，不進 Canva）──
    def draw_mpl(self, ax, line_groups=(), maglim=None, mw_n=9000, phi=None,
                 labels=(), lw=1.6, star_k=1.0):
        """把盤的內容畫到 matplotlib axes（給預覽圖與分鏡圖用，不是交付素材）"""
        maglim = maglim or self.maglim
        random.seed(self.seed)
        xs, ys, ss = [], [], []
        for _ in range(mw_n):
            l = random.uniform(0, 360); b = random.gauss(0, 6.2)
            ra, dec = G.gal2eq(l, b)
            for x, y in self._pos(ra, dec):
                xs.append(x); ys.append(y); ss.append(random.uniform(.3, 1.7))
        ax.scatter(xs, ys, s=ss, c=COLORS["mw"], alpha=.28, lw=0, zorder=1)
        xs, ys, ss = [], [], []
        for h, (ra, dec, v) in self.S.items():
            if v > maglim:
                continue
            for x, y in self._pos(ra, dec):
                xs.append(x); ys.append(y)
                ss.append(max(.3, (6.3 - v)) ** 1.8 * .55 * star_k)
        ax.scatter(xs, ys, s=ss, c=COLORS["white"], lw=0, zorder=2)
        if phi is not None:
            for r in self.runs_of([(a, 0.0) for a in range(0, 361, 2)]):
                ax.plot([p[0] for p in r], [p[1] for p in r], c=COLORS["white"],
                        lw=1.0, ls=(0, (7, 5)), alpha=.35, zorder=3)
            for r in self.runs_of(horizon_points(phi, getattr(self.p, "lst", 0.0))):
                ax.plot([p[0] for p in r], [p[1] for p in r], c=COLORS["horizon"],
                        lw=1.8, alpha=.85, zorder=6)
        for segs, col in line_groups:
            for seg in segs:
                hs = [h for h in seg if h in self.S]
                for a, b in zip(hs, hs[1:]):
                    for r in self.runs_of(great_circle(*self.S[a][:2], *self.S[b][:2])):
                        ax.plot([p[0] for p in r], [p[1] for p in r],
                                c=COLORS.get(col, col), lw=lw, alpha=.9, zorder=5)
        FP = G.find_font()
        for it in labels:
            ra, dec = ((self.S[it["hip"]][:2]) if "hip" in it else (it["ra"], it["dec"]))
            for x, y in self._pos(ra, dec):
                ax.text(x, y + self.ref * 0.045, G.rtl(it["text"]), fontproperties=FP,
                        fontsize=it.get("pt", 11),
                        color=COLORS.get(it.get("color", "white"), it.get("color")),
                        ha="center", va="center", weight="bold", zorder=9)

    def runs_of(self, pts):
        return self._runs(pts)

    def preview(self, path, line_groups=(), phi=None, labels=(), dpi=120,
                width_in=20.0, title=""):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        x0, y0, x1, y1 = self.extent
        f = plt.figure(figsize=(width_in, width_in * (y1 - y0) / (x1 - x0)), dpi=dpi)
        f.patch.set_facecolor(COLORS["bg"])
        ax = f.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
        ax.set_aspect("equal"); ax.axis("off")
        self.draw_mpl(ax, line_groups, phi=phi, labels=labels)
        if title:
            ax.text(x0 + (x1 - x0) * .01, y1 - (y1 - y0) * .04, title,
                    fontproperties=G.find_font(), fontsize=22, color="#FFFFFF",
                    ha="left", va="top", weight="bold", zorder=12)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f.savefig(path, facecolor=COLORS["bg"]); plt.close(f)
        print(f"  ✓ {os.path.basename(path)}")
        return path

    def save_manifest(self):
        p = os.path.join(self.out, f"{self.ep}_P{self.idx}-{self.name}_盤資訊.json")
        json.dump(self.manifest, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return p


# ════════════════════════════════════════════════════════════════════
#  鏡像自測：三種投影的手性必須與天球一致
# ════════════════════════════════════════════════════════════════════
def selftest(base=None, verbose=True):
    """對觀測者（球內）而言，det[a,b,c] > 0 的三顆星在圖上必須是「順時針」。
    2D 有號面積（y 向上、逆時針為正）故須 sign(area) == -sign(det)。
    任何一張圖不合＝鏡像，回傳 False。"""
    base = base or G.find_base(os.path.dirname(os.path.abspath(__file__)))
    S = G.load_stars(base)
    TRIOS = {
        "北斗（Dubhe-Merak-Phecda）": [54061, 53910, 58001],
        "獵戶腰帶（δ-ε-ζ）":          [26311, 26727, 25930],
        "南十字（α-β-γ）":            [60718, 62434, 61084],
        "仙后 W（β-α-γ）":            [746, 3179, 4427],
    }
    projs = [("等距圓柱 lst=0", Equirect(0.0, -85, 85, tile=1)),
             ("等距圓柱 lst=120", Equirect(120.0, -85, 85, tile=1)),
             ("立體 北極盤", Stereo(0, 90, radius=110, ra_top=0)),
             ("立體 南極盤", Stereo(0, -90, radius=110, ra_top=0)),
             ("立體 赤道盤", Stereo(80, 0, radius=80)),
             ("立體 中緯盤 dec45", Stereo(180, 45, radius=80)),
             ("等距方位 北盤(舊)", PolarEquidistant(True, -30)),
             ("等距方位 南盤(舊)", PolarEquidistant(False, 30))]
    ok = True
    for tname, hips in TRIOS.items():
        if any(h not in S for h in hips):
            continue
        vs = [_uvec(*S[h][:2]) for h in hips]
        det = (vs[0][0] * (vs[1][1] * vs[2][2] - vs[1][2] * vs[2][1])
               - vs[0][1] * (vs[1][0] * vs[2][2] - vs[1][2] * vs[2][0])
               + vs[0][2] * (vs[1][0] * vs[2][1] - vs[1][1] * vs[2][0]))
        want = -1 if det > 0 else 1
        for pname, pr in projs:
            ps = [pr.fwd(*S[h][:2]) for h in hips]
            if any(p is None for p in ps):
                continue
            a = 0.5 * sum(ps[i][0] * ps[(i + 1) % 3][1] - ps[(i + 1) % 3][0] * ps[i][1]
                          for i in range(3))
            good = (a > 0) == (want > 0)
            ok &= good
            if verbose and not good:
                print(f"  ✗ 鏡像！{tname} @ {pname}")
    if verbose:
        print("  ✓ 鏡像自測全數通過" if ok else "  ✗ 鏡像自測失敗")
    return ok


def handoff_zoom(proj_a, pt_a, proj_b, pt_b):
    """兩張盤在同一片天空接手時，B 盤要用多少倍率才會與 A 盤等大。
    pt_* = (ra, dec)。回傳 zoom_B / zoom_A。"""
    return proj_a.mag(*pt_a) / proj_b.mag(*pt_b)


if __name__ == "__main__":
    print("── 投影引擎自測 ──")
    selftest()
    print("\n立體投影放大率表（距盤心角距 → 倍率）")
    for t in (0, 15, 30, 45, 60, 75, 90):
        print(f"   {t:3d}°  {2/(1+math.cos(t*D2R)):.3f}×")
    print("\n等距圓柱水平拉伸表（赤緯 → 倍率）")
    for d in (0, 30, 45, 60, 70, 80):
        print(f"   {d:3d}°  {1/math.cos(d*D2R):.3f}×")
