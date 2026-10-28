# -*- coding: utf-8 -*-
"""萬國星空 影集素材引擎（manifest 驅動）
用法: python3 gen_ep_assets.py <manifest.json> [--base "<NTNU Insta 路徑>"]

manifest 結構（範例見 examples/）:
{
  "episode": "A-01",                      # 檔名前綴用
  "outdir": "05_素材/A-01_青龍",          # 相對 base
  "prefix": "青龍",                        # 檔名主體
  "field": {"center": "auto"|[ra,dec], "radius": "auto"|度數, "maglim": 5.6},
  "layers": [
    {"type":"stars", "mains":[HIP,...]},                       # 星點層（mains 加光暈）
    {"type":"milkyway"},                                       # 銀河帶
    # 任一圖層加 "optional": true → 只單獨輸出，不併入預設「合成／預覽_黑底」
    #（用於對比層、彩蛋層等只在特定鏡頭出現的內容；仍可在 previews 指名使用）
    {"type":"lines", "name":"全龍", "color":"amber",
       "source":{"culture":"chinese","names":["角宿","亢宿"]}   # 依文化星座名抓連線
       或 "hips":[[hip,hip,...],...],                           # 或直接 HIP 折線
       "split": true},                                         # 每個星座另存一檔
    {"type":"labels", "name":"標籤",
       "auto_from":"全龍",                                      # 自動在各星座質心放宿名
       "items":[{"hip":65474,"zh":"角宿一","en":"Spica","dx":0,"dy":-4,"size":15},
                 {"ra":56.75,"dec":24.12,"zh":"昴宿星團","dx":0,"dy":2}]},
    {"type":"dso", "items":[{"id":"M 45","zh":"昴宿星團"}]}     # 深空天體圈標
  ],
  "disc_overlay": {"lines":[同上 source/hips], "labels":[items], "disc":"auto"|"north"|"south"},
  "previews": [{"name":"中西對比","layers":["stars","milkyway","全龍","天蠍座","標籤"]}]
}
所有圖層輸出透明 PNG；另自動輸出: 合成_透明、預覽_黑底、SVG、星盤疊加對齊驗證。
"""
import json, math, os, sys, glob, pickle, struct, re, argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.font_manager import FontProperties

# ───────────────────────── 常數（全案統一） ─────────────────────────
COLORS = {"amber":"#FFC94A", "blue":"#6FA8FF", "white":"#FFFFFF", "red":"#FF6B6B",
          "green":"#7BD88F", "purple":"#B78AFF", "mw":"#C9DAF5", "bg":"#0B0F1E"}
CANVAS_IN, DPI, PREVIEW_DPI = 10.8, 190, 190
DISC_DPI, DISC_LIM = 380, (4/3)*1.02
FONT_CANDIDATES = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                   "/System/Library/Fonts/PingFang.ttc"]
DSO_POS = {"M 45":(56.75,24.12),"M 44":(130.10,19.67),"M 7":(268.45,-34.79),
 "M 42":(83.82,-5.39),"M 31":(10.68,41.27),"NGC 869":(34.75,57.13),"NGC 884":(35.60,57.15),
 "LMC":(80.89,-69.76),"SMC":(13.16,-72.80),"Coalsack":(186.9,-63.7),
 "Carina Nebula":(161.27,-59.87),"omega Cen":(201.70,-47.48),"Hyades":(66.75,15.87)}
GAL2EQ_M = [[-0.0548755604, 0.4941094279, -0.8676661490],
            [-0.8734370902, -0.4448296300, -0.1980763734],
            [-0.4838350155, 0.7469822445, 0.4559837762]]

def find_font():
    """字型 fallback 鏈：CJK 字型缺梵文變音符號(ṛṣś)與阿拉伯文，DejaVu 補足；
    DejaVu 無漢字，由 CJK 字型補足。matplotlib 3.6+ 支援 family list fallback。"""
    from matplotlib import font_manager
    fams = []
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            try:
                font_manager.fontManager.addfont(f)
                fams.append(font_manager.FontProperties(fname=f).get_name())
            except Exception: pass
    for extra in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(extra):
            try:
                font_manager.fontManager.addfont(extra)
                fams.append(font_manager.FontProperties(fname=extra).get_name())
            except Exception: pass
    fams.append("DejaVu Sans")
    return FontProperties(family=fams)
FP = find_font()

# ── RTL 文字整形（阿拉伯文／希伯來文）────────────────────────────────
# 舊版 matplotlib 不做 Arabic shaping 與 bidi：字母會是分離形態且由左寫到右，
# 所以先用 arabic_reshaper 轉成連寫的 presentation form，python-bidi 反轉為 RTL 視覺順序。
# matplotlib 3.11 起內建 libraqm（ft2font.__libraqm_version__），自己就會整形＋RTL；
# 這時再先整形一次＝反轉兩次（字序顛倒、連寫錯形），所以偵測到 libraqm 就原樣交給它。
try:
    import arabic_reshaper as _ar
    from bidi.algorithm import get_display as _bidi
    _RTL_OK = True
except ImportError:
    _RTL_OK = False


def _mpl_shapes_text():
    try:
        import matplotlib.ft2font as _ft
        return bool(getattr(_ft, "__libraqm_version__", ""))
    except Exception:
        return False


MPL_SHAPES = _mpl_shapes_text()

_RTL_RANGES = ((0x0590,0x05FF), (0x0600,0x06FF), (0x0750,0x077F), (0x08A0,0x08FF))
def rtl(s):
    """含阿拉伯／希伯來字元時做連寫整形＋RTL 排序；其餘原樣返回。
    matplotlib 有 libraqm（3.11 起）時原樣返回：讓 matplotlib 自己整形，才不會反轉兩次。"""
    if not s or not _RTL_OK or MPL_SHAPES: return s
    if not any(any(a <= ord(c) <= b for a,b in _RTL_RANGES) for c in s): return s
    try: return _bidi(_ar.reshape(s))
    except Exception: return s

# ───────────────────────── 星表快取 ─────────────────────────
def build_star_cache(base):
    d = os.path.join(base, "07_資料來源/Stellarium/stellarium-master/stars/hip_gaia3/")
    import numpy as np
    dt = np.dtype([("gaia","<i8"),("x0","<i4"),("x1","<i4"),("x2","<i4"),
                   ("dx0","<i4"),("dx1","<i4"),("dx2","<i4"),
                   ("bv","<i2"),("vmag","<i2"),("plx","<u2"),("plx_err","<u2"),
                   ("rv","<i2"),("sp","<u2"),("objtype","u1"),("hip3","3u1")])
    stars = {}
    for f in ["stars_0_0v0_21.cat","stars_1_0v0_16.cat","stars_2_0v0_17.cat","stars_3_0v0_10.cat"]:
        with open(d+f, "rb") as fh:
            _m,_t,_ma,_mi,level,_mm = struct.unpack("<6I", fh.read(24)); fh.read(4)
            nz = 20*4**level + 1
            zs = np.frombuffer(fh.read(4*nz), dtype="<u4")
            rec = np.frombuffer(fh.read(48*int(zs.sum())), dtype=dt)
        h3 = rec["hip3"].astype(np.uint32)
        comb = h3[:,0]|(h3[:,1]<<8)|(h3[:,2]<<16); hip=comb>>5; comp=comb&0x1F
        x0,x1,x2 = rec["x0"]/2e9, rec["x1"]/2e9, rec["x2"]/2e9
        r = np.sqrt(x0**2+x1**2+x2**2); r[r==0]=1
        ra = np.degrees(np.arctan2(x1,x0))%360
        dec = np.degrees(np.arcsin(np.clip(x2/r,-1,1)))
        v = rec["vmag"]/1000.0
        for i in np.where(hip>0)[0]:
            h=int(hip[i])
            if h not in stars or (comp[i]<=1 and v[i]<stars[h][2]):
                stars[h]=(float(ra[i]),float(dec[i]),float(v[i]))
    return stars

def load_stars(base):
    cache = os.path.join(base, "07_資料來源/_cache")
    os.makedirs(cache, exist_ok=True)
    p = os.path.join(cache, "hip_stars.pkl")
    if os.path.exists(p): return pickle.load(open(p,"rb"))
    print("首次執行：解析 Stellarium 星表建立快取…")
    s = build_star_cache(base); pickle.dump(s, open(p,"wb")); return s

# ───────────────────────── 文化資料解析 ─────────────────────────
def sc_dir(base):
    return os.path.join(base, "07_資料來源/Stellarium/stellarium-skycultures-master")

def culture_lines(base, culture, names=None, iau=None):
    """回傳 ({name: segs}, {name: common_name dict})；names=None 時回傳整文化"""
    idx = json.load(open(os.path.join(sc_dir(base), culture, "index.json"), encoding="utf-8"))
    out, meta, want2key = {}, {}, {}
    for c in idx.get("constellations", []):
        cn = c.get("common_name", {}) or {}
        key_nat, key_en = cn.get("native",""), cn.get("english","")
        if iau and c.get("iau") != iau: continue
        hit = None
        if names is not None:
            if key_nat in names: hit = key_nat
            elif key_en in names: hit = key_en
            else: continue
        segs = [[e for e in seg if isinstance(e,int)] for seg in c.get("lines",[])]
        segs = [s for s in segs if len(s) >= 2]
        if segs:
            k = key_nat or key_en or c["id"]
            out[k] = segs; meta[k] = cn
            if hit: want2key[hit] = k          # manifest 寫的名 → 實際 key（可能是 native）
    missing = [n for n in (names or []) if n not in want2key and not iau]
    if missing: raise SystemExit(f"[錯誤] {culture} 找不到星座: {missing}")
    if names:                                   # 依 manifest 順序，且 key 用 manifest 寫的名
        out = {n: out[want2key[n]] for n in names if n in want2key}
        meta = {n: meta[want2key[n]] for n in names if n in want2key}
    return out, meta

def parse_po(path):
    """極簡 .po 解析：msgid → msgstr"""
    if not os.path.exists(path): return {}
    ent, mid, mstr, mode = {}, None, None, None
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if s.startswith("msgid "):
            if mid is not None and mstr: ent[mid] = mstr
            mode="i"; mid=json.loads(s[6:]); mstr=None
        elif s.startswith("msgstr "): mode="s"; mstr=json.loads(s[7:])
        elif s.startswith('"'):
            v=json.loads(s)
            if mode=="i" and mid is not None: mid+=v
            elif mode=="s" and mstr is not None: mstr+=v
        elif not s:
            if mid is not None and mstr: ent[mid]=mstr
            mid=mstr=mode=None
    if mid is not None and mstr: ent[mid]=mstr
    return ent

def culture_po(base, culture, lang):
    """該文化 po 檔：english → 該語言譯名（用於取原文名，如 korean/ko.po）"""
    return parse_po(os.path.join(sc_dir(base), culture, "po", f"{lang}.po"))

# ───────────────────────── 投影 ─────────────────────────
def stereo(ra, dec, ra0, dec0):
    ra,dec,ra0,dec0 = map(math.radians,(ra,dec,ra0,dec0))
    k = 2/(1+math.sin(dec0)*math.sin(dec)+math.cos(dec0)*math.cos(dec)*math.cos(ra-ra0))
    return (-math.degrees(k*math.cos(dec)*math.sin(ra-ra0)),
            math.degrees(k*(math.cos(dec0)*math.sin(dec)-math.sin(dec0)*math.cos(dec)*math.cos(ra-ra0))))

def disc_proj(ra, dec, north=True):
    t = math.radians(ra)
    if north: r=(90-dec)/90.0; return r*math.sin(t), r*math.cos(t)
    r=(90+dec)/90.0; return -r*math.sin(t), r*math.cos(t)

def gal2eq(l,b):
    l,b = math.radians(l), math.radians(b)
    g=(math.cos(b)*math.cos(l), math.cos(b)*math.sin(l), math.sin(b))
    x,y,z = (sum(GAL2EQ_M[i][j]*g[j] for j in range(3)) for i in range(3))
    return math.degrees(math.atan2(y,x))%360, math.degrees(math.asin(z))

def ang_dist(ra1,dec1,ra2,dec2):
    c=(math.sin(math.radians(dec1))*math.sin(math.radians(dec2))+
       math.cos(math.radians(dec1))*math.cos(math.radians(dec2))*math.cos(math.radians(ra1-ra2)))
    return math.degrees(math.acos(max(-1,min(1,c))))

# ───────────────────────── 引擎 ─────────────────────────
class Engine:
    def __init__(self, base, mani):
        self.base, self.m = base, mani
        self.S = load_stars(base)
        self.out = os.path.join(base, mani["outdir"]); os.makedirs(self.out, exist_ok=True)
        self.prefix = mani.get("prefix", mani["episode"])
        self.line_groups, self.line_meta, self.line_src = {}, {}, {}
        for L in mani.get("layers", []):
            if L["type"]=="lines":
                g, m = self.resolve_lines(L)
                self.line_groups[L["name"]] = g; self.line_meta[L["name"]] = m
                self.line_src[L["name"]] = (L.get("source") or {}).get("culture")
        ov = mani.get("disc_overlay") or {}
        pairs = [self.resolve_lines(L) for L in ov.get("lines", [])]
        self.ov_groups = [p[0] for p in pairs]
        self.ov_meta   = [p[1] for p in pairs]
        self.ov_src    = [(L.get("source") or {}).get("culture") for L in ov.get("lines", [])]
        self.setup_field()

    def resolve_lines(self, spec):
        if "hips" in spec: return {spec.get("name","lines"): spec["hips"]}, {}
        src = spec["source"]
        return culture_lines(self.base, src["culture"], src.get("names"), src.get("iau"))

    def label_text(self, culture, key, meta, mode):
        """mode: english / native / pronounce / po:<lang>"""
        cn = meta.get(key, {}) or {}
        if mode == "pronounce": return cn.get("pronounce") or cn.get("english") or key
        if mode == "native":    return cn.get("native") or cn.get("english") or key
        if mode == "english":   return cn.get("english") or key
        if mode.startswith("po:") and culture:
            lang = mode[3:]
            if (culture, lang) not in getattr(self, "_po_cache", {}):
                if not hasattr(self, "_po_cache"): self._po_cache = {}
                self._po_cache[(culture, lang)] = culture_po(self.base, culture, lang)
            return self._po_cache[(culture, lang)].get(cn.get("english",""), "") or cn.get("english") or key
        return key

    def all_hips(self):
        hips=set()
        for g in list(self.line_groups.values())+self.ov_groups:
            for segs in g.values():
                for s in segs: hips.update(s)
        for L in self.m.get("layers", []):
            if L["type"]=="labels":
                for it in L.get("items", []):
                    if "hip" in it: hips.add(it["hip"])
            if L["type"]=="stars": hips.update(L.get("mains",[]))
        return hips

    def setup_field(self):
        f = self.m.get("field", {})
        hips = self.all_hips()
        pts = [self.S[h][:2] for h in hips if h in self.S]
        if f.get("center","auto")=="auto":
            xs=[math.cos(math.radians(d))*math.cos(math.radians(r)) for r,d in pts]
            ys=[math.cos(math.radians(d))*math.sin(math.radians(r)) for r,d in pts]
            zs=[math.sin(math.radians(d)) for r,d in pts]
            cx,cy,cz = sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)
            self.ra0 = math.degrees(math.atan2(cy,cx))%360
            self.dec0 = math.degrees(math.atan2(cz, math.hypot(cx,cy)))
        else: self.ra0, self.dec0 = f["center"]
        if f.get("radius","auto")=="auto":
            self.radius = max(12, max(ang_dist(self.ra0,self.dec0,r,d) for r,d in pts)*1.25)
        else: self.radius = f["radius"]
        self.maglim = f.get("maglim", 5.8)
        self.lim = self.radius*1.12
        self.field = []
        for h,(ra,dec,v) in self.S.items():
            if v<=self.maglim and ang_dist(self.ra0,self.dec0,ra,dec)<=self.radius:
                self.field.append((h,*stereo(ra,dec,self.ra0,self.dec0),v))
        print(f"視場 center=({self.ra0:.1f},{self.dec0:.1f}) r={self.radius:.1f}° 星數={len(self.field)}")

    # ── 繪圖底層 ──
    def fig(self, dark=False, disc=False, dpi=None):
        lim = DISC_LIM if disc else self.lim
        f = plt.figure(figsize=(CANVAS_IN,CANVAS_IN), dpi=dpi or (DISC_DPI if disc else DPI))
        ax = f.add_axes([0,0,1,1]); ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
        ax.set_aspect("equal"); ax.axis("off")
        if dark: f.patch.set_facecolor(COLORS["bg"])
        else: f.patch.set_alpha(0); ax.patch.set_alpha(0)
        return f, ax
    def sz(self, v): return max(0.4,(6.3-v))**1.8*2.6
    def save(self, f, name, transparent=True):
        f.savefig(os.path.join(self.out, name), transparent=transparent); plt.close(f)
        print("  ✓", name)

    # ── 各圖層 ──
    def d_stars(self, ax, mains=()):
        ms=set(mains)
        ax.scatter([p[1] for p in self.field if p[0] not in ms],
                   [p[2] for p in self.field if p[0] not in ms],
                   s=[self.sz(p[3]) for p in self.field if p[0] not in ms],
                   c=COLORS["white"], lw=0, zorder=2)
        for h in mains:
            ra,dec,v=self.S[h]; x,y=stereo(ra,dec,self.ra0,self.dec0)
            ax.scatter([x],[y],s=self.sz(v)*7,c=COLORS["white"],alpha=.18,lw=0,zorder=3)
            ax.scatter([x],[y],s=self.sz(v)*2.4,c=COLORS["white"],lw=0,zorder=4)
    def d_mw(self, ax):
        import random; random.seed(42)
        xs,ys,ss=[],[],[]
        for _ in range(20000):
            l=random.uniform(0,360); b=random.gauss(0,6.2)
            ra,dec=gal2eq(l,b)
            if ang_dist(self.ra0,self.dec0,ra,dec)<=self.radius*1.1:
                x,y=stereo(ra,dec,self.ra0,self.dec0)
                xs.append(x);ys.append(y);ss.append(random.uniform(.5,2.4))
        ax.scatter(xs,ys,s=ss,c=COLORS["mw"],alpha=.34,lw=0,zorder=1)
    def d_lines(self, ax, groups, color, lw=2.8, only=None):
        for name, segs in groups.items():
            if only and name!=only: continue
            for seg in segs:
                pts=[stereo(*self.S[h][:2],self.ra0,self.dec0) for h in seg if h in self.S]
                if len(pts)>=2:
                    ax.plot([p[0] for p in pts],[p[1] for p in pts],c=COLORS.get(color,color),
                            lw=lw,solid_capstyle="round",alpha=.95,zorder=5)
    def d_labels(self, ax, L):
        items=list(L.get("items",[]))
        if L.get("auto_from"):
            gname=L["auto_from"]; g=self.line_groups[gname]
            rn=L.get("rename",{})          # 星官名 → 顯示名／自訂偏移
            mode=L.get("auto_text")        # english / native / pronounce / po:<lang>
            meta=self.line_meta.get(gname,{}); cul=self.line_src.get(gname)
            for name,segs in g.items():
                hs={h for s in segs for h in s if h in self.S}
                pts=[stereo(*self.S[h][:2],self.ra0,self.dec0) for h in hs]
                cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
                base_txt = self.label_text(cul, name, meta, mode) if mode else name
                r=rn.get(name, base_txt)
                if isinstance(r,dict) and "zh" not in r: r={**r,"zh":base_txt}
                if isinstance(r,dict):
                    items.append({"xy":(cx+r.get("dx",0), cy+r.get("dy",self.radius*.10)),
                                  "zh":r.get("zh",name), "size":r.get("size",19)})
                elif r:                     # 空字串＝不標
                    items.append({"xy":(cx,cy+self.radius*.10),"zh":r,"size":19})
        for it in items:
            if "xy" in it: x,y=it["xy"]
            elif "hip" in it: x,y=stereo(*self.S[it["hip"]][:2],self.ra0,self.dec0)
            else: x,y=stereo(it["ra"],it["dec"],self.ra0,self.dec0)
            x+=it.get("dx",0); y+=it.get("dy",0); size=it.get("size",18)
            ax.text(x,y,rtl(it.get("zh") or it.get("en","")),fontproperties=FP,fontsize=size,color=COLORS["white"],
                    ha="center",weight="bold",zorder=6)
            if it.get("en"):
                ax.text(x,y-self.lim*.045,rtl(it["en"]),fontproperties=FP,fontsize=size*.62,
                        color=COLORS["white"],alpha=.85,ha="center",zorder=6)
    def d_dso(self, ax, L):
        for it in L.get("items",[]):
            ra,dec = DSO_POS.get(it["id"], (it.get("ra"),it.get("dec")))
            x,y=stereo(ra,dec,self.ra0,self.dec0)
            ax.scatter([x],[y],s=650,facecolors="none",edgecolors=COLORS["amber"],lw=2,zorder=5)
            ax.scatter([x],[y],s=1500,c=COLORS["amber"],alpha=.12,lw=0,zorder=4)
            if it.get("zh"):
                ax.text(x,y-self.radius*.09,rtl(it["zh"]),fontproperties=FP,fontsize=15,
                        color=COLORS["white"],ha="center",weight="bold",zorder=6)

    # ── 主流程 ──
    def run(self):
        drawn = {}      # layer name -> callable（全部圖層）
        default = {}    # 預設合成/預覽用（排除 optional: true 的圖層）
        for L in self.m.get("layers", []):
            t=L["type"]
            if t=="stars":
                fn=lambda ax,L=L: self.d_stars(ax,L.get("mains",[])); nm="星點層"
            elif t=="milkyway": fn=lambda ax: self.d_mw(ax); nm="銀河層"
            elif t=="lines":
                col=L.get("color","amber"); g=self.line_groups[L["name"]]
                fn=lambda ax,g=g,col=col,L=L: self.d_lines(ax,g,col,L.get("lw",2.8)); nm=f"連線層_{L['name']}"
                if L.get("split"):
                    for i,sub in enumerate(g,1):
                        f2,ax2=self.fig(); self.d_lines(ax2,g,col,L.get("lw",2.8),only=sub)
                        self.save(f2, f"{self.prefix}_連線層_{i}{sub}_透明.png")
            elif t=="labels": fn=lambda ax,L=L: self.d_labels(ax,L); nm=f"標籤層_{L.get('name','標籤')}"
            elif t=="dso": fn=lambda ax,L=L: self.d_dso(ax,L); nm=f"天體標記層_{L.get('name','DSO')}"
            else: continue
            key = L.get("name", nm)
            drawn[key] = fn
            if not L.get("optional"): default[key] = fn
            f,ax=self.fig(); fn(ax); self.save(f, f"{self.prefix}_{nm}_透明.png")
        # 合成＋黑底預覽（不含 optional 圖層）
        f,ax=self.fig()
        for fn in default.values(): fn(ax)
        self.save(f, f"{self.prefix}_合成_透明.png")
        f,ax=self.fig(dark=True, dpi=PREVIEW_DPI)
        for fn in default.values(): fn(ax)
        self.save(f, f"{self.prefix}_預覽_黑底.png", transparent=False)
        for pv in self.m.get("previews", []):
            f,ax=self.fig(dark=True, dpi=PREVIEW_DPI)
            for k in pv["layers"]:
                if k in drawn: drawn[k](ax)
            self.save(f, f"{self.prefix}_預覽_{pv['name']}_黑底.png", transparent=False)
        self.disc_overlay()
        self.svg(drawn)

    def disc_clip(self, ax):
        """裁切到星盤邊界圓（dec ∓30，r=4/3），避免線條溢出盤外"""
        from matplotlib.patches import Circle
        c = Circle((0,0), 4/3, transform=ax.transData)
        return c

    def disc_draw_lines(self, ax, north, lw_scale=1.0):
        """畫星盤連線。規則：**兩端都在盤外的線段一律不畫**——否則盤外星官
        （例如南盤上的北極星官）會因兩端分居盤兩側而拉出橫跨全盤的假線。
        只有一端在盤外時保留，由 clip 裁到盤緣（該星官確實延伸出盤）。"""
        RB = 4/3
        clip = self.disc_clip(ax)
        col = COLORS.get(self.m["disc_overlay"].get("color","amber"))
        for g,L in zip(self.ov_groups, self.m["disc_overlay"].get("lines",[])):
            c = COLORS.get(L.get("color","amber")); lw = L.get("lw",2.4)*lw_scale
            for name,segs in g.items():
                for seg in segs:
                    pts=[disc_proj(*self.S[h][:2],north) for h in seg if h in self.S]
                    for p,q in zip(pts, pts[1:]):
                        if math.hypot(*p) > RB and math.hypot(*q) > RB:
                            continue                      # 兩端皆盤外 → 假線，捨棄
                        ln,=ax.plot([p[0],q[0]],[p[1],q[1]], c=c, lw=lw,
                                    solid_capstyle="round", alpha=.95)
                        ln.set_clip_path(clip)

    def disc_label_items(self, north, spec):
        """回傳該標籤組的 items（含 auto 質心）。盤外的星官自動略過。"""
        items=list(spec.get("labels",[]))
        if spec.get("auto_labels") or spec.get("auto_text"):
            mode=spec.get("auto_text"); rn=spec.get("rename",{})
            # lines_index：只標某一組連線（多套系統對照時必用，否則各組標籤會互相疊上）
            li = spec.get("lines_index")
            trio = list(zip(self.ov_groups, self.ov_meta, self.ov_src))
            if li is not None: trio = [trio[li]]
            for g,meta,cul in trio:
                for name,segs in g.items():
                    hs=[h for s in segs for h in s if h in self.S]
                    if not hs: continue
                    decs=[self.S[h][1] for h in hs]
                    inside = (min(decs)>=-30) if north else (max(decs)<=30)
                    if not inside: continue            # 盤外星官不標
                    pts=[disc_proj(*self.S[h][:2],north) for h in set(hs)]
                    cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
                    if math.hypot(cx,cy) > 4/3*0.97: continue
                    txt = self.label_text(cul, name, meta, mode) if mode else name
                    r = rn.get(name, txt)
                    if isinstance(r,dict):
                        items.append({"xy":(cx+r.get("dx",0), cy+r.get("dy",.06)),
                                      "zh":r.get("zh",txt), "size":r.get("size",11)})
                    elif r:
                        items.append({"xy":(cx,cy+.06),"zh":r,"size":spec.get("size",11)})
        return items

    def disc_overlay(self):
        ov=self.m.get("disc_overlay")
        if not ov: return
        hips={h for g in self.ov_groups for segs in g.values() for s in segs for h in s}
        decs=[self.S[h][1] for h in hips if h in self.S]
        disc=ov.get("disc","auto")
        if disc=="auto": disc = "north" if min(decs)>=-30 else ("south" if max(decs)<=30 else "both")
        # 標籤組：新式 label_sets（多版本），或舊式單組
        lsets = ov.get("label_sets")
        if lsets is None:
            lsets = [{"name":"標籤", "labels":ov.get("labels",[]),
                      "auto_labels":ov.get("auto_labels"), "auto_text":ov.get("auto_text"),
                      "rename":ov.get("rename",{})}] if (ov.get("labels") or ov.get("auto_labels")) else []
        fn_base = "05_素材/全天星盤"
        for side in (["north","south"] if disc=="both" else [disc]):
            north = side=="north"; tag = "北盤" if north else "南盤"
            # 無標示連線層
            f,ax=self.fig(disc=True); self.disc_draw_lines(ax,north)
            self.save(f, f"{self.prefix}_星盤疊加_{tag}_連線層_無標示_透明.png")
            # 各標籤版本
            for spec in lsets:
                nm=spec.get("name","標籤")
                f,ax=self.fig(disc=True)
                for it in self.disc_label_items(north, spec):
                    x,y = it["xy"] if "xy" in it else disc_proj(*self.S[it["hip"]][:2],north)
                    ax.text(x+it.get("dx",0),y+it.get("dy",0),rtl(it["zh"]),fontproperties=FP,
                            fontsize=it.get("size",11),color=COLORS["white"],ha="center",weight="bold")
                self.save(f, f"{self.prefix}_星盤疊加_{tag}_標籤層_{nm}_透明.png")
            # 預覽（黑底星盤＋連線＋各標籤版本）
            fn_disc=f"{'北天星盤' if north else '南天星盤'}_mag5_星點層_透明.png"
            discfile=next((p for p in
                (os.path.join(self.base,fn_base,fn_disc),
                 os.path.join(self.base,"07_資料來源/_星圖示範/全天星盤",fn_disc))
                if os.path.exists(p)), None)
            if not discfile:
                print("  ! 找不到全天星盤，略過星盤預覽"); continue
            img = mpimg.imread(discfile)
            for nm, spec in [("無標示", None)] + [(s.get("name","標籤"), s) for s in lsets]:
                f,ax=self.fig(dark=True, disc=True, dpi=PREVIEW_DPI)
                ax.imshow(img, extent=[-DISC_LIM,DISC_LIM,-DISC_LIM,DISC_LIM])
                self.disc_draw_lines(ax, north, lw_scale=.9)
                if spec:
                    for it in self.disc_label_items(north, spec):
                        x,y = it["xy"] if "xy" in it else disc_proj(*self.S[it["hip"]][:2],north)
                        ax.text(x+it.get("dx",0),y+it.get("dy",0),rtl(it["zh"]),fontproperties=FP,
                                fontsize=it.get("size",11),color=COLORS["white"],ha="center",weight="bold")
                self.save(f, f"{self.prefix}_星盤預覽_{tag}_{nm}_黑底.png", transparent=False)

    def svg(self, drawn):
        lim=self.lim
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-lim:.2f} {-lim:.2f} {2*lim:.2f} {2*lim:.2f}" font-family="Noto Sans CJK TC, sans-serif">']
        svg.append('<g id="stars" fill="#FFFFFF">')
        for h,x,y,v in self.field:
            svg.append(f'<circle cx="{x:.2f}" cy="{-y:.2f}" r="{math.sqrt(self.sz(v))*0.055:.3f}"/>')
        svg.append('</g>')
        for name,g in self.line_groups.items():
            svg.append(f'<g id="lines_{name}" stroke="#FFC94A" stroke-width="{lim*0.006:.3f}" fill="none" stroke-linecap="round">')
            for sub,segs in g.items():
                for seg in segs:
                    pts=[stereo(*self.S[h][:2],self.ra0,self.dec0) for h in seg if h in self.S]
                    if len(pts)>=2:
                        svg.append('<path d="M '+" L ".join(f"{x:.2f} {-y:.2f}" for x,y in pts)+'"/>')
            svg.append('</g>')
        svg.append('</svg>')
        open(os.path.join(self.out,f"{self.prefix}_可編輯.svg"),"w",encoding="utf-8").write("\n".join(svg))
        print("  ✓", f"{self.prefix}_可編輯.svg")

def find_base(start):
    p=os.path.abspath(start)
    while p!="/":
        if os.path.isdir(os.path.join(p,"07_資料來源")): return p
        p=os.path.dirname(p)
    raise SystemExit("[錯誤] 找不到含 07_資料來源 的專案資料夾，請用 --base 指定")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("manifest"); ap.add_argument("--base", default=None)
    a=ap.parse_args()
    mani=json.load(open(a.manifest, encoding="utf-8"))
    base=a.base or find_base(os.path.dirname(a.manifest) or ".")
    Engine(base, mani).run()
    print("完成。")
