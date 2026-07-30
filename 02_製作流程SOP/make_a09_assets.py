# -*- coding: utf-8 -*-
"""A-09 夏威夷星線：觀測者長條星圖素材
核心創新：x 軸 = 時角（LST − RA），故
  ① 星圖橫向平移 ＝ 周日運動（數學嚴格成立，可 Canva Match & Move 無縫循環）
  ② 觀測地的地平線在此座標下是一條**固定不動**的曲線
兩者疊加即可模擬「從夏威夷看出去、整夜的星空流轉」。
"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_strip_chart as SC
from gen_strip_chart import (Strip, xw, gcirc, plot_path,
                             hour_angle_at_horizon, rise_azimuth,
                             AMBER, BLUE, WHITE, GREEN, PURPLE, MW, BG)
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE, "05_素材/A-09_夏威夷星線")
SKY  = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/hawaiian_starlines")
PHI  = 19.7          # 夏威夷島（Hilo）緯度；Hōkūleʻa 為其天頂星

segs, _ = G.culture_lines(BASE, "hawaiian_starlines")
_cn = json.load(open(os.path.join(SKY, "index.json"), encoding="utf-8"))["common_names"]
NAMES = {int(k.split()[1]): (v[0].get("native") or v[0].get("english") or "")
         for k, v in _cn.items() if k.startswith("HIP")}

# 四大星線與其附屬星群
FOUR = {
    "Ke Ka o Makaliʻi": dict(color=AMBER,  season="十一月～四月", zh="Makaliʻi 的舀水杓",
        keys=["Ke Ka o Makali’i", "Ka Hei-Hei o Na Keiki", "Makali`i"]),
    "Ka Iwikuamoʻo":    dict(color=GREEN,  season="四月～七月",   zh="脊骨",
        keys=["Ka Iwikuamo’o", "Na Hiku", "Me`e", "Hanaiakamalama", "Nakuhikuhi",
              "Ka`ohiweliweli"]),
    "Manaiakalani":     dict(color=BLUE,   season="五月～十月",   zh="酋長的釣線",
        keys=["Manaiakalani", "Navigator's Triangle"]),
    "Ka Lupe o Kawelo": dict(color=PURPLE, season="九月～二月",   zh="Kawelo 的風箏",
        keys=["Ka Lupe o Kawelo", "`Iwa Keli`i"]),
}
# 各星線的關鍵星（片中會唸到的，標籤只上這些，避免 70 個名字擠成一團）
KEY = {
    "Ke Ka o Makaliʻi": [24608, 36850, 37826, 37279, 32349, 30438, 25930],
    "Ka Iwikuamoʻo":    [11767, 54061, 62956, 67301, 69673, 65474, 60718],
    "Manaiakalani":     [102098, 91262, 97649, 82396, 78401, 80763, 86228],
    "Ka Lupe o Kawelo": [3179, 746, 677, 113881, 1067, 113963, 113368, 3419],
}

def nm(h):
    return NAMES.get(h, "")

def save_layer(s, fn, name, dark=False):
    f, ax = s.fig(dark=dark); fn(ax)
    s.save(f, OUT + "/_長條全天", name, transparent=not dark)


# ═══════════ 組 1：全天長條圖（3600 × 1800 px）═══════════
def build_strip():
    s = Strip(BASE, phi=PHI, lst=0.0, dec_lo=-72, dec_hi=72,
              maglim=5.4, width_in=24.0, dpi=150, margin=18.0)
    d = OUT + "/_長條全天"

    def L_base(ax):   s.d_mw(ax); s.d_stars(ax, mains=[h for v in KEY.values() for h in v])
    def L_grid(ax):   s.d_grid(ax)
    def L_refs(ax):   s.d_refs(ax)
    def L_hor(ax):    s.d_horizon(ax); s.d_horizon_labels(ax)
    def L_line(key):
        def _f(ax):
            cfg = FOUR[key]
            for k in cfg["keys"]:
                if k in segs: s.d_lines(ax, segs[k], cfg["color"], lw=3.2)
        return _f
    def L_names(key):
        def _f(ax):
            cfg = FOUR[key]
            for h in KEY[key]:
                if h in s.S and s.lo <= s.S[h][1] <= s.hi and nm(h):
                    s.d_label(ax, h, nm(h), dy=3.6, c=cfg["color"], size=16)
        return _f
    def L_title(ax):
        s.d_title(ax, "Ka Lani Hōkū", None, WHITE)
        ax.text(0, s.hi + s.margin*0.22, "從夏威夷（北緯 19.7°）看出去的整片天空",
                fontproperties=SC.FP, fontsize=17, color=WHITE, ha="center",
                va="center", alpha=.82, zorder=14)
        ax.text(0, s.hi + s.margin*(-0.02), "星圖向右捲動＝時間前進　｜　綠色地平線固定不動",
                fontproperties=SC.FP, fontsize=14, color=WHITE, ha="center",
                va="center", alpha=.6, zorder=14)

    layers = [("底圖", L_base), ("網格", L_grid), ("參考線", L_refs),
              ("地平線", L_hor), ("題辭", L_title)]
    for k in FOUR:
        layers.append((f"星線_{k}", L_line(k)))
        layers.append((f"星名_{k}", L_names(k)))

    print("\n── 組1 全天長條圖 ──")
    for nmm, fn in layers:
        f, ax = s.fig(); fn(ax); s.save(f, d, f"長條全天_{nmm}層_透明.png")

    # 合成預覽（三種）
    def compose(name, use, horizon=True):
        f, ax = s.fig(dark=True)
        L_base(ax); L_grid(ax)
        for k in use:
            L_line(k)(ax)
        L_refs(ax)
        if horizon: L_hor(ax)
        for k in use: L_names(k)(ax)
        L_title(ax)
        s.save(f, d, name, transparent=False)
    compose("長條全天_預覽_黑底.png", list(FOUR))
    compose("長條全天_預覽_無地平線_黑底.png", list(FOUR), horizon=False)
    for k in FOUR:
        compose(f"長條全天_預覽_{k}_黑底.png", [k])
    return s


# ═══════════ 組 2：各星線 9:16 特寫（Reels 實際視窗）═══════════
def build_closeups(s):
    import matplotlib.pyplot as plt
    d = OUT + "/_星線特寫"; os.makedirs(d, exist_ok=True)
    VIS = 108.0                                     # 一屏可見赤經跨度
    print("\n── 組2 星線 9:16 特寫 ──")
    for key, cfg in FOUR.items():
        hs = [h for k in cfg["keys"] if k in segs for sg in segs[k] for h in sg if h in s.S]
        if not hs: continue
        # 令該星線中天（x=0）：物理上就是「這條線當令的那個時刻」
        mean_ra = math.degrees(math.atan2(
            sum(math.sin(math.radians(s.S[h][0])) for h in hs),
            sum(math.cos(math.radians(s.S[h][0])) for h in hs))) % 360
        old_lst, s.lst = s.lst, mean_ra
        mx = 0.0
        ds = [d for d in (s.S[h][1] for h in hs) if -70 <= d <= 70]
        cy = max(-34, min(34, (max(ds)+min(ds))/2)) if ds else 0.0
        f = plt.figure(figsize=(5.4, 9.6), dpi=200); f.patch.set_facecolor(BG)
        fa = f.add_axes([0,0,1,1]); fa.set_xlim(0,1); fa.set_ylim(0,1); fa.axis("off")
        ca = f.add_axes([0, 0.24, 1, 0.52]); ca.axis("off"); ca.patch.set_alpha(0)
        vy = VIS * (0.52*9.6) / (1.0*5.4)           # 依 axes 實際長寬比推 Dec 跨度
        ca.set_xlim(mx-VIS/2, mx+VIS/2); ca.set_ylim(cy-vy/2, cy+vy/2)
        s.d_mw(ca); s.d_grid(ca); s.d_stars(ca, mains=KEY[key])
        s.d_refs(ca, labels=False)
        for k in cfg["keys"]:
            if k in segs: s.d_lines(ca, segs[k], cfg["color"], lw=3.6)
        for h in KEY[key]:
            if h in s.S and nm(h):
                x = xw(s.S[h][0], s.lst)
                if abs(((x-mx+180) % 360)-180) < VIS/2-5 and abs(s.S[h][1]-cy) < vy/2-4:
                    s.d_label(ca, h, nm(h), dy=vy*0.035, c=cfg["color"], size=15)
        fa.text(.5,.945,key,fontproperties=SC.FP,fontsize=32,color=cfg["color"],
                ha="center",va="center",weight="bold")
        fa.text(.5,.900,cfg["zh"],fontproperties=SC.FP,fontsize=17,color=WHITE,
                ha="center",va="center",alpha=.85)
        fa.text(.5,.865,f"當令季節　{cfg['season']}",fontproperties=SC.FP,fontsize=15,
                color=WHITE,ha="center",va="center",alpha=.65)
        fa.text(.5,.205,"畫面向右捲動 ＝ 時間前進",fontproperties=SC.FP,fontsize=15,
                color=WHITE,ha="center",va="center",alpha=.55)
        span = max(s.S[h][1] for h in hs) - min(s.S[h][1] for h in hs)
        if span > vy:
            fa.text(.5,.165,"本星線南北跨度超出單屏，此為中段；完整走向見全天盤",
                    fontproperties=SC.FP,fontsize=13,color=cfg["color"],
                    ha="center",va="center",alpha=.7)
        fa.text(.5,.055,f"此刻為本星線中天（赤經 {mean_ra/15:.1f}h 過子午線）",
                fontproperties=SC.FP,fontsize=12,color=WHITE,
                ha="center",va="center",alpha=.42)
        f.savefig(os.path.join(d, f"星線特寫_{key}_黑底.png")); plt.close(f)
        s.lst = old_lst
        print("  ✓", f"星線特寫_{key}_黑底.png")


# ═══════════ 組 3：無縫捲動版（540° = 360° + 半圈重複）═══════════
def build_seamless():
    """投影週期為 360°，故把同一張圖水平接一份再裁 540%，
    左右接縫必定無縫。Canva 只要把圖從右拉到左即可循環播放。
    題辭層不做（文字會重複），其餘各層皆可。"""
    from PIL import Image
    d = OUT + "/_長條全天"
    o = OUT + "/_長條無縫捲動"; os.makedirs(o, exist_ok=True)
    print("\n── 組3 無縫捲動版 ──")
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".png") or "題辭" in fn or "預覽" in fn: continue
        im = Image.open(os.path.join(d, fn))
        w, h = im.size
        cv = Image.new("RGBA", (int(w*1.5), h), (0, 0, 0, 0))
        cv.paste(im, (0, 0)); cv.paste(im, (w, 0))
        cv.crop((0, 0, int(w*1.5), h)).save(
            os.path.join(o, fn.replace("_透明.png", "_無縫540度_透明.png")))
        print("  ✓", fn.replace("_透明.png", "_無縫540度_透明.png"))


if __name__ == "__main__":
    st = build_strip()
    build_closeups(st)
    build_seamless()
    print("\nA-09 長條圖組完成")
