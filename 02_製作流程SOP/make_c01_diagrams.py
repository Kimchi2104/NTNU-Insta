# -*- coding: utf-8 -*-
"""C-01 論天三家：概念示意圖（幾何精確部分）
輸出與星圖素材同規格：10.8in × 190dpi（2052px）、透明 PNG 分層＋黑底預覽。
色票沿用全案標準。幾何依《周髀算經》《晉書・天文志》《靈憲》。
"""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Arc
from matplotlib.font_manager import FontProperties, fontManager

BASE = "/sessions/funny-kind-mayer/mnt/Downloads--NTNU Insta/05_素材/C-01_論天三家"
AMBER, BLUE, WHITE, GREEN, PURPLE = "#FFC94A", "#6FA8FF", "#FFFFFF", "#7BD88F", "#B78AFF"
MW, BG = "#C9DAF5", "#0B0F1E"
CANVAS, DPI = 10.8, 190

def font():
    fams=[]
    for f in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            fontManager.addfont(f); fams.append(FontProperties(fname=f).get_name())
    fams.append("DejaVu Sans"); return FontProperties(family=fams)
FP = font()

def newfig(lim=1.0, dark=False):
    f = plt.figure(figsize=(CANVAS,CANVAS), dpi=DPI)
    ax = f.add_axes([0,0,1,1]); ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_aspect("equal"); ax.axis("off")
    if dark: f.patch.set_facecolor(BG)
    else: f.patch.set_alpha(0); ax.patch.set_alpha(0)
    return f, ax

def save(f, sub, name, transparent=True):
    d = os.path.join(BASE, sub); os.makedirs(d, exist_ok=True)
    f.savefig(os.path.join(d, name), transparent=transparent); plt.close(f)
    print("  ✓", sub+"/"+name)

def T(ax, x, y, s, size=20, c=WHITE, ha="center", w="bold", alpha=1.0):
    ax.text(x, y, s, fontproperties=FP, fontsize=size, color=c, ha=ha,
            va="center", weight=w, alpha=alpha)

# ══════════════════════════════════════════════════════════════
# 1. 蓋天說：七衡六間（俯視）
#    《周髀算經》：內衡（夏至日道）半徑 119000 里、外衡（冬至）238000 里，
#    七衡等差、間距 19833⅓ 里。內:中:外 = 1 : 1.5 : 2
# ══════════════════════════════════════════════════════════════
R_IN, R_OUT = 119000.0, 238000.0
STEP = (R_OUT - R_IN) / 6
HENG = [R_IN + i*STEP for i in range(7)]          # 第一衡…第七衡
SCALE = 0.86 / R_OUT
NAMES = ["內衡（夏至）", "二衡", "三衡", "中衡（春秋分）", "五衡", "六衡", "外衡（冬至）"]

def qiheng_rings(ax, only=None, faint=False):
    th = [math.radians(t) for t in range(361)]
    for i, r in enumerate(HENG):
        if only is not None and i != only:
            if not faint: continue
            c, lw, a = WHITE, 1.0, .18
        else:
            key = i in (0, 3, 6)
            c  = AMBER if key else WHITE
            lw = 3.0 if key else 1.4
            a  = .95 if key else .45
        rr = r*SCALE
        ax.plot([rr*math.cos(t) for t in th], [rr*math.sin(t) for t in th], c=c, lw=lw, alpha=a)

def qiheng_center(ax):
    ax.scatter([0],[0], s=180, c=AMBER, zorder=5)
    T(ax, 0, -0.075, "北極（璿璣）", 17, AMBER)

def qiheng_labels(ax):
    for i, r in enumerate(HENG):
        rr = r*SCALE
        key = i in (0, 3, 6)
        T(ax, 0, rr+0.035, NAMES[i], 19 if key else 14,
          AMBER if key else WHITE, alpha=1.0 if key else .75)
    T(ax, 0.60, -0.80, "內衡 : 外衡 ＝ 1 : 2", 17, WHITE, alpha=.9)
    T(ax, 0.60, -0.87, "七衡等差・間距 19833⅓ 里", 14, WHITE, alpha=.7)

def qiheng_sun_path(ax):
    """太陽在各衡上的位置（示意）"""
    for i, r in enumerate(HENG):
        rr = r*SCALE; a = math.radians(35 - i*4)
        ax.scatter([rr*math.cos(a)], [rr*math.sin(a)], s=150 if i in (0,3,6) else 70,
                   c=AMBER, alpha=.95 if i in (0,3,6) else .5, zorder=6)

print("── 蓋天說：七衡六間 ──")
for nm, fn in [("環", lambda ax: qiheng_rings(ax)),
               ("中心", qiheng_center),
               ("標籤", qiheng_labels),
               ("日位", qiheng_sun_path)]:
    f, ax = newfig(); fn(ax); save(f, "蓋天說", f"七衡六間_{nm}層_透明.png")
for i in range(7):
    f, ax = newfig(); qiheng_rings(ax, only=i, faint=True); qiheng_center(ax)
    save(f, "蓋天說", f"七衡六間_逐衡_{i+1}_{NAMES[i].split('（')[0]}_透明.png")
f, ax = newfig(dark=True)
qiheng_rings(ax); qiheng_center(ax); qiheng_sun_path(ax); qiheng_labels(ax)
save(f, "蓋天說", "七衡六間_預覽_黑底.png", transparent=False)

# ══════════════════════════════════════════════════════════════
# 2. 蓋天說：側視（天似蓋笠、地法覆槃）
#    《晉書・天文志》：天中高於外衡六萬里、北極下地高於外衡下地六萬里、
#    外衡高於北極下地二萬里、日去地恆八萬里
# ══════════════════════════════════════════════════════════════
def gaitian_side(ax, annotate=True):
    xs = [x/100 for x in range(-90, 91)]
    sky   = [0.42 - 0.42*(x/0.9)**2 + 0.30 for x in xs]   # 天蓋（笠）
    earth = [0.42 - 0.42*(x/0.9)**2 - 0.28 for x in xs]   # 地槃
    ax.plot(xs, sky,   c=AMBER, lw=3.2)
    ax.plot(xs, earth, c=GREEN, lw=3.0)
    ax.plot([0,0],[earth[90], sky[90]], c=WHITE, lw=1.2, ls=(0,(4,4)), alpha=.5)
    ax.scatter([0],[sky[90]], s=150, c=AMBER, zorder=5)
    ax.scatter([0],[earth[90]], s=110, c=GREEN, zorder=5)
    if annotate:
        T(ax, 0, sky[90]+0.075, "天中（北極之下）", 17, AMBER)
        T(ax, 0, earth[90]-0.075, "地中（其地最高）", 16, GREEN)
        T(ax, -0.62, 0.60, "天似蓋笠", 22, AMBER)
        T(ax,  0.62, -0.44, "地法覆槃", 22, GREEN)
        T(ax, 0, -0.86, "天地各中高外下・日去地恆八萬里", 16, WHITE, alpha=.85)

def gaitian_sun(ax):
    """日麗天而平轉：太陽貼著天蓋平行移動"""
    for k, x in enumerate([-0.66, -0.33, 0.0, 0.33, 0.66]):
        y = 0.42 - 0.42*(x/0.9)**2 + 0.30 - 0.055
        ax.scatter([x],[y], s=170 if k==2 else 90, c=AMBER, alpha=.95 if k==2 else .45, zorder=6)
    ax.annotate("", xy=(0.72,0.52), xytext=(-0.72,0.52),
                arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.6, alpha=.6))
    T(ax, 0, 0.585, "日麗天而平轉", 16, WHITE, alpha=.85)

print("── 蓋天說：側視 ──")
f, ax = newfig(); gaitian_side(ax, annotate=False); save(f, "蓋天說", "側視_天地層_透明.png")
f, ax = newfig(); gaitian_side(ax); save(f, "蓋天說", "側視_天地含標籤_透明.png")
f, ax = newfig(); gaitian_sun(ax); save(f, "蓋天說", "側視_日行層_透明.png")
f, ax = newfig(dark=True); gaitian_side(ax); gaitian_sun(ax)
save(f, "蓋天說", "側視_預覽_黑底.png", transparent=False)

# ══════════════════════════════════════════════════════════════
# 3. 蓋天說：圭表日影（《周髀算經》八尺之表，夏至影一尺六寸、冬至一丈三尺五寸）
# ══════════════════════════════════════════════════════════════
def guibiao(ax, season="both"):
    GY = -0.42
    ax.plot([-0.95,0.95],[GY,GY], c=WHITE, lw=2.0, alpha=.7)         # 地平
    ax.plot([0,0],[GY, GY+0.52], c=WHITE, lw=5.0)                     # 八尺之表
    T(ax, -0.075, GY+0.26, "表\n八尺", 15, WHITE, ha="right")
    S = 0.52/8.0                                                      # 一尺的畫布長度
    cases = [("夏至", 1.6, AMBER, 1), ("冬至", 13.5, BLUE, 1)]
    for nm, shadow, col, sgn in cases:
        if season != "both" and season != nm: continue
        L = shadow*S*sgn
        ax.plot([0, L],[GY, GY], c=col, lw=6.0, alpha=.9,
                solid_capstyle="butt", zorder=4)
        ax.plot([L, 0],[GY, GY+0.52], c=col, lw=1.8, ls=(0,(6,4)), alpha=.8)
        ax.scatter([L*1.30],[GY+0.52*(1.30 if nm=="夏至" else 0.55)], s=260, c=col, zorder=6)
        T(ax, L/2, GY-0.075, f"{nm}影長 {shadow} 尺", 16, col)
    T(ax, 0, 0.72, "圭表測影", 26, WHITE)
    T(ax, 0, 0.62, "以日影長短推日道遠近", 16, WHITE, alpha=.8)

print("── 蓋天說：圭表日影 ──")
for s, tag in [("both","雙至"), ("夏至","夏至"), ("冬至","冬至")]:
    f, ax = newfig(); guibiao(ax, s); save(f, "蓋天說", f"圭表日影_{tag}_透明.png")
f, ax = newfig(dark=True); guibiao(ax); save(f, "蓋天說", "圭表日影_預覽_黑底.png", transparent=False)

# ══════════════════════════════════════════════════════════════
# 4. 渾天說：天球（天如雞子、地如中黃）
#    黃赤交角 23.44°
# ══════════════════════════════════════════════════════════════
EPS = 23.44
def hun_sphere(ax):
    th=[math.radians(t) for t in range(361)]
    ax.plot([0.82*math.cos(t) for t in th],[0.82*math.sin(t) for t in th], c=WHITE, lw=2.6, alpha=.85)

def hun_equator(ax):
    ax.add_patch(Ellipse((0,0), 1.64, 0.44, fill=False, ec=BLUE, lw=2.6, alpha=.95))
    T(ax, 0.66, 0.16, "赤道", 18, BLUE)

def hun_ecliptic(ax):
    ax.add_patch(Ellipse((0,0), 1.64, 0.44, angle=EPS, fill=False, ec=AMBER, lw=2.6, alpha=.95))
    T(ax, -0.60, 0.44, "黃道", 18, AMBER)
    ax.add_patch(Arc((0,0), 0.60, 0.60, theta1=0, theta2=EPS, color=WHITE, lw=1.4, alpha=.7))
    T(ax, 0.40, 0.08, f"{EPS}°", 13, WHITE, alpha=.8)

def hun_earth(ax):
    ax.scatter([0],[0], s=900, c=GREEN, zorder=6)
    T(ax, 0, -0.115, "地在天中", 17, GREEN)

def hun_poles(ax):
    ax.plot([0,0],[-0.95,0.95], c=WHITE, lw=1.2, ls=(0,(4,4)), alpha=.5)
    ax.scatter([0,0],[0.82,-0.82], s=90, c=WHITE, zorder=6)
    T(ax, 0.14, 0.735, "北天極", 15, WHITE, ha="left")
    T(ax, 0.12, -0.86, "南天極", 15, WHITE, ha="left")

def hun_xiu(ax):
    """二十八宿沿赤道帶分佈（示意）"""
    for i in range(28):
        a = math.radians(i*360/28)
        x, y = 0.82*math.cos(a), 0.22*math.sin(a)
        ax.scatter([x],[y], s=40, c=WHITE, alpha=.8, zorder=5)
    T(ax, 0, -0.72, "二十八宿沿天球環布", 16, WHITE, alpha=.85)

def hun_egg(ax):
    T(ax, 0, 0.93, "天如雞子，地如中黃", 24, WHITE)
    T(ax, 0, 0.845, "張衡《渾天儀注》", 15, WHITE, alpha=.7)

print("── 渾天說：天球 ──")
for nm, fn in [("天球", hun_sphere), ("赤道", hun_equator), ("黃道", hun_ecliptic),
               ("地", hun_earth), ("極軸", hun_poles), ("二十八宿", hun_xiu), ("題辭", hun_egg)]:
    f, ax = newfig(); fn(ax); save(f, "渾天說", f"天球_{nm}層_透明.png")
f, ax = newfig(dark=True)
for fn in (hun_sphere, hun_poles, hun_equator, hun_ecliptic, hun_xiu, hun_earth, hun_egg): fn(ax)
save(f, "渾天說", "天球_預覽_黑底.png", transparent=False)

# ══════════════════════════════════════════════════════════════
# 5. 宣夜說：無天殼，日月星辰浮於氣中
# ══════════════════════════════════════════════════════════════
def xuanye_qi(ax):
    import random; random.seed(7)
    for _ in range(1400):
        x, y = random.uniform(-1,1), random.uniform(-1,1)
        d = math.hypot(x,y)
        ax.scatter([x],[y], s=random.uniform(2,26), c=MW,
                   alpha=max(0.03, 0.30-0.22*d), lw=0, zorder=1)

def xuanye_stars(ax):
    import random; random.seed(11)
    for _ in range(150):
        x, y = random.uniform(-.95,.95), random.uniform(-.95,.95)
        ax.scatter([x],[y], s=random.uniform(6,60), c=WHITE,
                   alpha=random.uniform(.45,1.0), lw=0, zorder=3)

def xuanye_bodies(ax):
    for x, y, s, c, lab in [(-0.42, 0.34, 900, AMBER, "日"),
                            ( 0.40, 0.44, 620, WHITE, "月"),
                            ( 0.10,-0.36, 300, PURPLE, "五星"),
                            (-0.52,-0.30, 260, PURPLE, ""),
                            ( 0.62,-0.12, 240, PURPLE, "")]:
        ax.scatter([x],[y], s=s, c=c, zorder=5)
        if lab: T(ax, x, y-0.10, lab, 18, c)
        ax.annotate("", xy=(x+0.16, y+0.07), xytext=(x, y),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.6, alpha=.65))

def xuanye_text(ax):
    T(ax, 0, 0.90, "天了無質，仰而瞻之，高遠無極", 22, WHITE)
    T(ax, 0, 0.815, "日月眾星，自然浮生虛空之中", 17, WHITE, alpha=.85)
    T(ax, 0, -0.88, "無固定天殼・各依其性運行", 16, WHITE, alpha=.7)

print("── 宣夜說 ──")
for nm, fn in [("氣", xuanye_qi), ("眾星", xuanye_stars), ("日月五星", xuanye_bodies), ("題辭", xuanye_text)]:
    f, ax = newfig(); fn(ax); save(f, "宣夜說", f"宣夜_{nm}層_透明.png")
f, ax = newfig(dark=True)
for fn in (xuanye_qi, xuanye_stars, xuanye_bodies, xuanye_text): fn(ax)
save(f, "宣夜說", "宣夜_預覽_黑底.png", transparent=False)

# ══════════════════════════════════════════════════════════════
# 6. 三家並置對照（一圖三格，剪輯用）
# ══════════════════════════════════════════════════════════════
def trio(ax):
    for cx, title, sub in [(-0.62,"蓋天","天圓如蓋笠"), (0.0,"渾天","天如雞子"), (0.62,"宣夜","天了無質")]:
        T(ax, cx, -0.62, title, 24, AMBER)
        T(ax, cx, -0.70, sub, 14, WHITE, alpha=.75)
    # 蓋天（左）
    xs=[x/100 for x in range(-28,29)]
    ax.plot([-0.62+x for x in xs], [0.10-0.55*(x/0.28)**2*0.35+0.10 for x in xs], c=AMBER, lw=2.6)
    ax.plot([-0.62+x for x in xs], [0.10-0.55*(x/0.28)**2*0.35-0.16 for x in xs], c=GREEN, lw=2.4)
    # 渾天（中）
    th=[math.radians(t) for t in range(361)]
    ax.plot([0.26*math.cos(t) for t in th],[0.26*math.sin(t)+0.05 for t in th], c=WHITE, lw=2.4)
    ax.add_patch(Ellipse((0,0.05), 0.52, 0.15, fill=False, ec=BLUE, lw=1.8))
    ax.add_patch(Ellipse((0,0.05), 0.52, 0.15, angle=EPS, fill=False, ec=AMBER, lw=1.8))
    ax.scatter([0],[0.05], s=180, c=GREEN, zorder=5)
    # 宣夜（右）
    import random; random.seed(3)
    for _ in range(90):
        a=random.uniform(0,2*math.pi); r=random.uniform(0,0.30)
        ax.scatter([0.62+r*math.cos(a)],[0.05+r*math.sin(a)], s=random.uniform(6,70),
                   c=WHITE, alpha=random.uniform(.4,1), lw=0)
    T(ax, 0, 0.82, "論天三家", 34, WHITE)
    T(ax, 0, 0.72, "春秋戰國—漢：同一片天空，三種宇宙", 16, WHITE, alpha=.8)

print("── 三家並置 ──")
f, ax = newfig(); trio(ax); save(f, "_三家並置", "論天三家_對照_透明.png")
f, ax = newfig(dark=True); trio(ax); save(f, "_三家並置", "論天三家_對照_預覽_黑底.png", transparent=False)
print("done")
