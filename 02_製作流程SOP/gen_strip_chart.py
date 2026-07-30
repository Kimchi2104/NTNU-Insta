# -*- coding: utf-8 -*-
"""觀測者長條星圖（Observer Strip Chart）
等距圓柱投影：x = LST − RA（東在左、西在右，面南視角），y = Dec。
橫向平移 = 周日運動（數學上嚴格成立），可在 Canva 用 Match & Move 做無縫捲動。
疊加觀測地參考線：天頂緯線、天赤道、拱極界線。
"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AMBER, BLUE, WHITE = "#FFC94A", "#6FA8FF", "#FFFFFF"
GREEN, PURPLE, MW, BG = "#7BD88F", "#B78AFF", "#C9DAF5", "#0B0F1E"
FP = None

# ── 投影 ──
def xw(ra, lst=0.0):
    """x = LST − RA，正規化到 (−180, 180]；東在左、西在右"""
    return (lst - ra + 180.0) % 360.0 - 180.0

def gcirc(ra1, dec1, ra2, dec2, n=40):
    """大圓插值：長線在圓柱投影上必須畫成曲線，否則失真"""
    p1 = (math.cos(math.radians(dec1))*math.cos(math.radians(ra1)),
          math.cos(math.radians(dec1))*math.sin(math.radians(ra1)),
          math.sin(math.radians(dec1)))
    p2 = (math.cos(math.radians(dec2))*math.cos(math.radians(ra2)),
          math.cos(math.radians(dec2))*math.sin(math.radians(ra2)),
          math.sin(math.radians(dec2)))
    dot = max(-1.0, min(1.0, sum(a*b for a, b in zip(p1, p2))))
    om = math.acos(dot)
    if om < 1e-9: return [(ra1, dec1), (ra2, dec2)]
    out = []
    for i in range(n+1):
        t = i/n
        s1, s2 = math.sin((1-t)*om)/math.sin(om), math.sin(t*om)/math.sin(om)
        v = [s1*p1[k] + s2*p2[k] for k in range(3)]
        out.append((math.degrees(math.atan2(v[1], v[0])) % 360,
                    math.degrees(math.asin(max(-1, min(1, v[2]))))))
    return out

def plot_path(ax, pts, lst, **kw):
    """畫大圓路徑，遇到 ±180 邊界自動斷開（避免橫貫全圖的假線）"""
    run = []
    prev = None
    for ra, dec in pts:
        x = xw(ra, lst)
        if prev is not None and abs(x - prev) > 180:
            if len(run) >= 2:
                ax.plot([p[0] for p in run], [p[1] for p in run], **kw)
            run = []
        run.append((x, dec)); prev = x
    if len(run) >= 2:
        ax.plot([p[0] for p in run], [p[1] for p in run], **kw)


# ── 地平線幾何：本圖 x 軸即時角，故某地的地平線是一條固定不動的曲線 ──
def hour_angle_at_horizon(phi, dec):
    """該赤緯與地平線相交的時角（度）。None=永不升；180=永不落"""
    t = -math.tan(math.radians(phi)) * math.tan(math.radians(dec))
    if t > 1: return None
    if t < -1: return 180.0
    return math.degrees(math.acos(t))

def rise_azimuth(phi, dec):
    """升起方位角（自正北順時針，度）。None=永不升或永不落"""
    c = math.sin(math.radians(dec)) / math.cos(math.radians(phi))
    if abs(c) > 1: return None
    return math.degrees(math.acos(c))


class Strip:
    def __init__(self, base, phi=19.7, lst=0.0, dec_lo=-72, dec_hi=72,
                 maglim=5.4, width_in=24.0, dpi=150, margin=10.0):
        global FP
        self.base, self.phi, self.lst = base, phi, lst
        self.lo, self.hi = dec_lo, dec_hi          # 內容範圍
        self.margin = margin                        # 上下留白（放標題與註記）
        self.ylo, self.yhi = dec_lo - margin, dec_hi + margin
        self.maglim = maglim
        self.S = G.load_stars(base)
        FP = G.find_font()
        self.w = width_in
        self.h = width_in * (self.yhi - self.ylo) / 360.0
        self.dpi = dpi
        print(f"長條圖 {int(self.w*dpi)}×{int(self.h*dpi)} px  "
              f"Dec {dec_lo}~{dec_hi}（含留白 {self.ylo}~{self.yhi}）φ={phi}")

    def fig(self, dark=False):
        f = plt.figure(figsize=(self.w, self.h), dpi=self.dpi)
        ax = f.add_axes([0, 0, 1, 1])
        ax.set_xlim(-180, 180); ax.set_ylim(self.ylo, self.yhi)
        ax.axis("off")
        if dark: f.patch.set_facecolor(BG)
        else: f.patch.set_alpha(0); ax.patch.set_alpha(0)
        return f, ax

    def d_horizon(self, ax, shade=.62, c="#48E39B", lw=2.6, n=900):
        """地平線遮罩：遮住地平線以下（本圖上為固定不動的曲線）"""
        import numpy as np
        decs = np.linspace(self.lo, self.hi, n)
        dd, ex, wx, never = [], [], [], []
        for d in decs:
            h = hour_angle_at_horizon(self.phi, float(d))
            if h is None: never.append(float(d)); continue
            dd.append(float(d)); ex.append(-h); wx.append(h)
        if dd:
            ax.fill_betweenx(dd, [-180]*len(dd), ex, color="#000000", alpha=shade, zorder=7)
            ax.fill_betweenx(dd, wx, [180]*len(dd), color="#000000", alpha=shade, zorder=7)
            ax.plot(ex, dd, c=c, lw=lw, zorder=9)
            ax.plot(wx, dd, c=c, lw=lw, zorder=9)
        if never:
            ax.fill_betweenx(never, [-180]*len(never), [180]*len(never),
                             color="#000000", alpha=shade, zorder=7)
        ax.plot([0, 0], [self.lo, self.hi], c=WHITE, lw=1.6, ls=(0, (6, 5)),
                alpha=.5, zorder=8)

    def sz(self, v): return max(0.4, (6.3 - v))**1.8 * 1.5

    def save(self, f, out, name, transparent=True):
        os.makedirs(out, exist_ok=True)
        f.savefig(os.path.join(out, name), transparent=transparent); plt.close(f)
        print("  ✓", name)

    # ── 圖層 ──
    def d_stars(self, ax, mains=()):
        ms = set(mains)
        xs, ys, ss = [], [], []
        for h, (ra, dec, v) in self.S.items():
            if v > self.maglim or not (self.lo <= dec <= self.hi) or h in ms: continue
            xs.append(xw(ra, self.lst)); ys.append(dec); ss.append(self.sz(v))
        ax.scatter(xs, ys, s=ss, c=WHITE, lw=0, zorder=2)
        for h in mains:
            if h not in self.S: continue
            ra, dec, v = self.S[h]
            x = xw(ra, self.lst)
            ax.scatter([x], [dec], s=self.sz(v)*7, c=WHITE, alpha=.18, lw=0, zorder=3)
            ax.scatter([x], [dec], s=self.sz(v)*2.4, c=WHITE, lw=0, zorder=4)

    def d_mw(self, ax):
        random.seed(42)
        xs, ys, ss = [], [], []
        for _ in range(42000):
            l = random.uniform(0, 360); b = random.gauss(0, 6.2)
            ra, dec = G.gal2eq(l, b)
            if self.lo <= dec <= self.hi:
                xs.append(xw(ra, self.lst)); ys.append(dec)
                ss.append(random.uniform(.4, 2.0))
        ax.scatter(xs, ys, s=ss, c=MW, alpha=.30, lw=0, zorder=1)

    def d_lines(self, ax, segs, color, lw=3.0, alpha=.95, max_distort=2.5,
                report=None):
        """畫星線。等距圓柱在高緯嚴重橫向拉伸，故加入失真守門：
        圖上長度 / 真實角距 > max_distort 的線段一律不畫
        （例如北極星→北斗真實 27°，圖上會被拉成 130°，畫出來是假的）。"""
        for seg in segs:
            hs = [h for h in seg if h in self.S]
            for a, b in zip(hs, hs[1:]):
                ra1, dec1, _ = self.S[a]; ra2, dec2, _ = self.S[b]
                dtrue = G.ang_dist(ra1, dec1, ra2, dec2)
                dx = abs(((xw(ra1, self.lst) - xw(ra2, self.lst) + 180) % 360) - 180)
                dmap = math.hypot(dx, dec1 - dec2)
                if dtrue > 0.1 and dmap / dtrue > max_distort:
                    if report is not None:
                        report.append((a, b, dtrue, dmap))
                    continue
                plot_path(ax, gcirc(ra1, dec1, ra2, dec2), self.lst,
                          c=color, lw=lw, solid_capstyle="round",
                          alpha=alpha, zorder=5)

    def d_refs(self, ax, labels=True):
        """觀測地參考線：天赤道、天頂緯線、拱極界線
        註：CJK 與含 ʻokina 的夏威夷語**不可放進同一個 text 物件**，
            matplotlib 會為整串選單一字型，導致中文變成豆腐。"""
        cp = 90 - self.phi
        for dec, c, lab, ls in [
            (0.0,   WHITE, "天赤道", (0, (7, 5))),
            (self.phi, AMBER, f"天頂線　Dec +{self.phi:.1f}°　此線上的星直接過頂", (0, (2, 3))),
            (+cp,  "#48E39B", f"Dec +{cp:.1f}° 以北　永不落（拱極）", (0, (10, 6))),
            (-cp,  "#48E39B", f"Dec −{cp:.1f}° 以南　永不升（隱圈）", (0, (10, 6))),
        ]:
            if not (self.lo <= dec <= self.hi): continue
            ax.plot([-180, 180], [dec, dec], c=c, lw=1.8, ls=ls, alpha=.55, zorder=6)
            if labels:
                ax.text(-176, dec + 2.6, lab, fontproperties=FP, fontsize=14, color=c,
                        ha="left", va="bottom", alpha=.88, zorder=12, clip_on=True)

    def d_horizon_labels(self, ax):
        """地平線相關文字（放在留白區，不壓內容）"""
        y = self.lo - self.margin*0.42
        for x, t1, t2, c in [(-96, "東地平線", "星星在此升起", "#48E39B"),
                             (0,   "子午線・中天", "此刻的最高點", WHITE),
                             (96,  "西地平線", "星星在此落下", "#48E39B")]:
            ax.text(x, y, t1, fontproperties=FP, fontsize=19, color=c,
                    ha="center", va="center", weight="bold", zorder=13)
            ax.text(x, y - self.margin*0.30, t2, fontproperties=FP, fontsize=13,
                    color=WHITE, ha="center", va="center", alpha=.72, zorder=13)
        ax.text(-176, self.lo - self.margin*0.82, "※ 黑色遮罩＝該時刻在地平線以下",
                fontproperties=FP, fontsize=13, color=WHITE, ha="left",
                va="center", alpha=.5, zorder=13)

    def d_title(self, ax, main, sub=None, c=WHITE):
        ax.text(0, self.hi + self.margin*0.55, main, fontproperties=FP, fontsize=27,
                color=c, ha="center", va="center", weight="bold", zorder=14)
        if sub:
            ax.text(0, self.hi + self.margin*0.22, sub, fontproperties=FP, fontsize=16,
                    color=WHITE, ha="center", va="center", alpha=.8, zorder=14)

    def d_grid(self, ax):
        """赤經刻度（每 2h）＋ 赤緯刻度"""
        for hh in range(0, 24, 2):
            ra = hh * 15.0
            x = xw(ra, self.lst)
            ax.plot([x, x], [self.lo, self.hi], c=WHITE, lw=0.8, alpha=.13, zorder=0)
            ax.text(x, self.lo + 2.0, f"{hh}h", fontproperties=FP, fontsize=12,
                    color=WHITE, ha="center", va="bottom", alpha=.42, zorder=12,
                    clip_on=True)
        for dd in range(-60, 61, 30):
            if dd == 0: continue
            ax.plot([-180, 180], [dd, dd], c=WHITE, lw=0.8, alpha=.10, zorder=0)

    def d_dirs(self, ax):
        """面南視角的方位提示"""
        ax.text(-172, self.hi - 5, "← 東（先升起）", fontproperties=FP, fontsize=15,
                color=WHITE, ha="left", va="top", alpha=.6, zorder=12)
        ax.text(172, self.hi - 5, "（後落下）西 →", fontproperties=FP, fontsize=15,
                color=WHITE, ha="right", va="top", alpha=.6, zorder=12)
        ax.text(0, self.hi - 5, "面南視角｜畫面向右移動 ＝ 時間前進",
                fontproperties=FP, fontsize=15, color=WHITE, ha="center",
                va="top", alpha=.55, zorder=12)

    def d_label(self, ax, hip, text, dx=0, dy=3.0, c=WHITE, size=15):
        if hip not in self.S: return
        ra, dec, _ = self.S[hip]
        ax.text(xw(ra, self.lst) + dx, dec + dy, text, fontproperties=FP,
                fontsize=size, color=c, ha="center", va="center",
                weight="bold", zorder=13, clip_on=True)
