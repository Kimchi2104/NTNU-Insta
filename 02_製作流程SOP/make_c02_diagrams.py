# -*- coding: utf-8 -*-
"""C-02 地有四游：概念示意圖
依《尚書・考靈曜》（漢代緯書）、《晉書・天文志》載姚信說。
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_series_base import *

set_base("/sessions/funny-kind-mayer/mnt/Downloads--NTNU Insta/05_素材/C-02_地有四游")

# ══════════════════════════════════════════════════════════════
# 1. 地有四游：大地一年在四個位置間移動
#    《尚書・考靈曜》：地有四游，冬至地上，北而西三萬里；
#                      夏至地下，南而東復三萬里；春秋二分其中矣。
# ══════════════════════════════════════════════════════════════
#  俯視圖：x = 東西、y = 南北；「上／下」另以升降符號與側視插圖表示
#  （二維俯視無法同時畫「上下」，故分開處理，避免與「南北」混淆）
D = 0.34                      # 三萬里在畫布上的長度
BW, BH = 0.19, 0.13           # 大地方塊半寬半高
POS = {
    "冬至": (-D, +D, AMBER, "地上・北而西", "冬至 ↑上"),
    "春秋分": (0.0, 0.0, WHITE, "其中矣", "春秋分"),
    "夏至": (+D, -D, BLUE,  "地下・南而東", "夏至 ↓下"),
}

def frame(ax):
    """參考框：中心十字與四方位"""
    ax.plot([-0.80, 0.80],[0,0], c=WHITE, lw=1.0, ls=(0,(5,5)), alpha=.28)
    ax.plot([0,0],[-0.66, 0.66], c=WHITE, lw=1.0, ls=(0,(5,5)), alpha=.28)
    for x, y, s in [(0.86,0,"東"), (-0.86,0,"西"), (0.075,0.70,"北"), (0.075,-0.70,"南")]:
        T(ax, x, y, s, 18, WHITE, alpha=.55)
    T(ax, -0.86, 0.90, "俯視", 14, WHITE, alpha=.45)

def track(ax):
    """四游軌跡：冬至 ↔ 春秋分 ↔ 夏至 的來回（線段避開方塊）"""
    for sx, sy, ex, ey in [(-D+BW*0.9, D-BH*1.3, -BW*0.9, BH*1.3),
                           (BW*0.9, -BH*1.3, D-BW*0.9, -D+BH*1.3)]:
        ax.plot([sx, ex],[sy, ey], c=WHITE, lw=1.8, ls=(0,(6,4)), alpha=.40, zorder=1)
    arrow(ax, (D-BW*0.75, -D+BH*1.1), (BW*0.75, -BH*1.1), WHITE, 1.8, .5)
    arrow(ax, (-D+BW*0.75, D-BH*1.1), (-BW*0.75, BH*1.1), WHITE, 1.8, .5)

def earth_at(ax, key):
    """大地方塊在某個節氣位置（其餘位置淡顯，附小標）"""
    for k, (x, y, c, sub, updown) in POS.items():
        on = (k == key)
        a = 1.0 if on else .22
        ax.add_patch(Rectangle((x-BW, y-BH), BW*2, BH*2, fc=c, ec="none",
                               alpha=a*0.30, zorder=3))
        ax.add_patch(Rectangle((x-BW, y-BH), BW*2, BH*2, fill=False, ec=c,
                               lw=3.0 if on else 1.4, alpha=a, zorder=4))
        T(ax, x, y, "地", 26 if on else 19, WHITE, alpha=(.95 if on else .45))
        T(ax, x, y+BH+0.065, updown, 22 if on else 15, c, alpha=1.0 if on else .6)
        if sub:
            T(ax, x, y-BH-0.065, sub, 15 if on else 12, c, alpha=(.9 if on else .5))

def measure(ax):
    """三萬里：沿位移方向標註"""
    ax.annotate("", xy=(-D+BW*0.5, D-BH*0.8), xytext=(-BW*0.5, BH*0.8),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.8, alpha=.9))
    T(ax, -0.085, 0.255, "三萬里", 17, AMBER)

def side_inset(ax):
    """右上角小側視圖：解決『上下』無法在俯視表現的問題"""
    ox, oy, w = 0.60, 0.62, 0.26
    ax.add_patch(Rectangle((ox-w, oy-w*0.78), w*2, w*1.56, fc=BG, ec=WHITE,
                           lw=1.2, alpha=.45, zorder=6))
    ax.plot([ox-w*0.8, ox+w*0.8],[oy, oy], c=WHITE, lw=1.0, ls=(0,(3,3)),
            alpha=.45, zorder=7)
    for dy, c, lab in [(+w*0.44, AMBER, "冬至 上"), (-w*0.44, BLUE, "夏至 下")]:
        ax.add_patch(Rectangle((ox-w*0.42, oy+dy-w*0.10), w*0.84, w*0.20,
                               fc=c, ec="none", alpha=.30, zorder=7))
        ax.add_patch(Rectangle((ox-w*0.42, oy+dy-w*0.10), w*0.84, w*0.20,
                               fill=False, ec=c, lw=1.6, zorder=8))
        T(ax, ox, oy+dy, lab, 11, WHITE, alpha=.95)
    T(ax, ox, oy+w*0.92, "側視（上下）", 12, WHITE, alpha=.6)

def title_note(ax):
    T(ax, -0.02, 0.92, "地有四游", 32, WHITE)
    T(ax, 0.0, -0.80, "地恆動不止，而人不知", 24, WHITE)
    T(ax, 0.0, -0.90, "《尚書・考靈曜》（漢代緯書）", 15, WHITE, alpha=.6)

print("── 地有四游 ──")
emit("地有四游",
     [("方位框", frame), ("軌跡", track), ("四游位置", lambda ax: earth_at(ax, "春秋分")),
      ("尺度", measure), ("側視插圖", side_inset), ("題辭", title_note)],
     title="地有四游")
for k in POS:
    f, ax = newfig(); frame(ax); track(ax); earth_at(ax, k); measure(ax); side_inset(ax)
    save(f, "地有四游", f"地有四游_位置_{k}_透明.png")
f, ax = newfig(dark=True)
for fn in (frame, track, lambda a: earth_at(a, "冬至"), measure, side_inset, title_note):
    fn(ax)
save(f, "地有四游", "地有四游_預覽_黑底.png", transparent=False)

# ── 1b. 四游要解釋什麼：日影與寒暑（呼應 C-01 圭表）──
def why_frame(ax):
    ax.plot([-0.90, 0.90],[-0.20, -0.20], c=WHITE, lw=2.0, alpha=.6)
    T(ax, 0, 0.92, "四游要解釋的是什麼？", 28, WHITE)
    T(ax, 0, 0.82, "大地移動 → 與日的相對位置改變 → 日影長短、寒暑遞嬗", 16, WHITE, alpha=.78)
    T(ax, 0, -0.62, "同一根八尺之表，冬至影長、夏至影短", 20, WHITE)
    T(ax, 0, -0.72, "四游說用「地在動」來解釋這件事", 15, WHITE, alpha=.78)
    T(ax, 0, -0.88, "※ 這是四游說的用途：把季節變化歸因於「地動」而非「日動」",
      14, WHITE, alpha=.55)

def why_pair(ax):
    GY, GH = -0.20, 0.34                      # 地平線、表高
    for cx, c, lab, sh in [(-0.44, AMBER, "冬至　地在上／北", 0.42),
                           (+0.42, BLUE,  "夏至　地在下／南", 0.14)]:
        tx, ty = cx, GY + GH                  # 表頂
        ex = cx + sh                          # 影端
        vx, vy = ex - tx, GY - ty
        n = math.hypot(vx, vy); ux, uy = vx/n, vy/n
        sx, sy = tx - 0.42*ux, ty - 0.42*uy   # 日（在入射光的反向延長線上）
        ax.scatter([sx],[sy], s=560, c=c, alpha=.92, zorder=5)
        T(ax, sx, sy+0.105, "日", 15, c)
        for off in (-0.075, 0.0, 0.075):      # 平行光束
            ox_, oy_ = -uy*off, ux*off
            ax.annotate("", xy=(tx+ox_*1.0+ux*0.02, ty+oy_*1.0+uy*0.02),
                        xytext=(sx+ox_, sy+oy_),
                        arrowprops=dict(arrowstyle="->", color=c, lw=1.4, alpha=.45))
        ax.plot([tx, ex],[ty, GY], c=c, lw=1.6, ls=(0,(5,4)), alpha=.75, zorder=4)
        ax.plot([cx, cx],[GY, ty], c=WHITE, lw=5.0, solid_capstyle="round", zorder=6)
        ax.plot([cx, ex],[GY, GY], c=c, lw=6.0, alpha=.9,
                solid_capstyle="butt", zorder=7)
        ang = math.degrees(math.atan2(ty-GY, tx-ex))     # 光線與 +x 軸夾角（鈍角）
        alt = 180.0 - ang                                 # 太陽高度角
        r = min(0.24, sh*0.85)
        ax.add_patch(Arc((ex, GY), r*2, r*2, theta1=ang, theta2=180,
                         ec=c, lw=1.4, alpha=.7, zorder=6))
        th = math.radians((180.0 + ang) / 2.0)
        lx, ly = ex + r*1.42*math.cos(th), GY + r*1.42*math.sin(th)
        if sh < 0.25:                       # 影短時弧太小，標籤改放右外側
            lx, ly = ex + 0.13, GY + r*1.25
        T(ax, lx, ly, f"{alt:.0f}°", 14, c)
        if sh > 0.3:
            T(ax, cx-0.045, GY + GH*0.45, "八尺之表", 13, WHITE, ha="right", alpha=.6)
        T(ax, cx+sh/2, GY-0.085, "影長" if sh > 0.3 else "影短", 16, c)
        T(ax, cx, -0.42, lab, 18, c)

print("── 四游解釋什麼 ──")
emit("四游與寒暑", [("框", why_frame), ("冬夏對照", why_pair)], title="四游與寒暑")

# ══════════════════════════════════════════════════════════════
# 2. 舟行而人不覺（相對運動）
#    《尚書・考靈曜》：譬如人在大舟中閉牖而坐，舟行而人不覺也
# ══════════════════════════════════════════════════════════════
WL = -0.34                                   # 水線
DECK = WL + 0.14                             # 甲板

def sea(ax, phase=0.0):
    water(ax, y=WL, c=BLUE, rows=3, amp=0.024, freq=15, phase=phase)

def hull(ax, dx=0.0, s=1.0, z=3):
    """船體：淺弧底＋平頂船樓（不是尖屋頂的房子）"""
    g, d = GREEN, DECK
    body = [(-0.60*s+dx, d), (0.66*s+dx, d), (0.58*s+dx, d-0.14*s),
            (0.30*s+dx, d-0.22*s), (-0.42*s+dx, d-0.22*s), (-0.52*s+dx, d-0.13*s)]
    ax.add_patch(Polygon(body, closed=True, fc=BG, ec="none", alpha=1.0, zorder=z))
    ax.add_patch(Polygon(body, closed=True, fc=g, ec="none", alpha=.24, zorder=z))
    ax.add_patch(Polygon(body, closed=True, fill=False, ec=g, lw=3.2, zorder=z+1))
    ax.add_patch(Rectangle((-0.40*s+dx, d), 0.80*s, 0.44*s, fc=BG, ec=g,
                           lw=2.8, alpha=.92, zorder=z+1))          # 船樓（艙）
    ax.plot([-0.46*s+dx, 0.46*s+dx],[d+0.44*s, d+0.44*s], c=g, lw=3.2, zorder=z+2)
    ax.plot([-0.46*s+dx, -0.40*s+dx],[d+0.44*s, d+0.50*s], c=g, lw=2.2, zorder=z+2)
    ax.plot([0.46*s+dx, 0.40*s+dx],[d+0.44*s, d+0.50*s], c=g, lw=2.2, zorder=z+2)

def window_shut(ax):
    """閉牖：兩扇關上的窗（板條）"""
    for x in (-0.22, 0.22):
        ax.add_patch(Rectangle((x-0.095, DECK+0.14), 0.19, 0.20, fc=BG, ec=WHITE,
                               lw=2.2, alpha=1.0, zorder=6))
        for k in range(3):
            yy = DECK + 0.185 + k*0.055
            ax.plot([x-0.075, x+0.075],[yy, yy], c=WHITE, lw=1.8, alpha=.65, zorder=7)
    T(ax, 0.0, DECK + 0.60, "閉牖而坐", 22, WHITE)
    arrow(ax, (-0.22, DECK+0.355), (-0.32, DECK+0.53), WHITE, 1.4, .5)

def person_inside(ax):
    """艙中坐者（側面，面朝右）"""
    c, x0, y0 = AMBER, -0.05, DECK + 0.06
    ax.add_patch(Circle((x0, y0+0.26), 0.052, fc=c, ec="none", zorder=8))     # 頭
    ax.plot([x0, x0+0.012],[y0+0.215, y0+0.075], c=c, lw=8.0,
            solid_capstyle="round", zorder=8)                                 # 軀幹
    ax.plot([x0+0.012, x0+0.16],[y0+0.075, y0+0.065], c=c, lw=7.0,
            solid_capstyle="round", zorder=8)                                 # 大腿
    ax.plot([x0+0.16, x0+0.165],[y0+0.065, y0-0.055], c=c, lw=6.5,
            solid_capstyle="round", zorder=8)                                 # 小腿
    ax.plot([x0+0.165, x0+0.215],[y0-0.055, y0-0.055], c=c, lw=5.0,
            solid_capstyle="round", zorder=8)                                 # 腳
    ax.plot([x0+0.01, x0+0.115],[y0+0.175, y0+0.085], c=c, lw=5.0,
            solid_capstyle="round", zorder=9)                                 # 手臂
    ax.plot([x0-0.06, x0+0.20],[y0-0.055, y0-0.055], c=WHITE, lw=2.0,
            alpha=.35, zorder=7)                                              # 艙板

def boat_motion(ax):
    arrow(ax, (0.90, DECK-0.10), (0.60, DECK-0.10), GREEN, 3.0, .9)
    T(ax, 0.76, DECK-0.19, "舟行", 18, GREEN)
    T(ax, 0.0, -0.66, "舟行而人不覺也", 26, WHITE)
    T(ax, 0.0, -0.76, "船在動，艙裡的人卻感覺不到——大地也是如此", 16, WHITE, alpha=.82)

def boat_title(ax):
    T(ax, 0.0, 0.90, "譬如人在大舟中閉牖而坐", 24, WHITE)

print("── 舟行而人不覺 ──")
emit("舟行不覺",
     [("水", sea), ("船", hull), ("閉牖", window_shut), ("人", person_inside),
      ("行進", boat_motion), ("題辭", boat_title)],
     title="舟行不覺")
emit_frames("舟行不覺", "舟行不覺_水波", lambda ax, i: sea(ax, phase=i*1.55), 4)
# 船身位移逐格（配合水波做「舟在行」的循環）
emit_frames("舟行不覺", "舟行不覺_船位移",
            lambda ax, i: hull(ax, dx=-0.06 + i*0.04), 4)
f, ax = newfig(dark=True)
for fn in (sea, hull, window_shut, person_inside, boat_motion, boat_title): fn(ax)
save(f, "舟行不覺", "舟行不覺_預覽_黑底.png", transparent=False)

# ── 2b. 兩種視角對照：外看船在動／艙內一切靜止 ──
def rel_split(ax):
    ax.plot([0, 0],[-0.46, 0.70], c=WHITE, lw=1.4, alpha=.35)
    T(ax, -0.46, 0.56, "艙外", 23, GREEN)
    T(ax,  0.46, 0.56, "艙內", 23, AMBER)
    T(ax, 0.0, 0.92, "同一艘船，兩種視角", 27, WHITE)

def rel_outside(ax):
    ox = -0.46
    water(ax, y=-0.06, x0=-0.94, x1=-0.03, c=BLUE, rows=2, amp=0.014, freq=26)
    b = [(ox-0.30, 0.08), (ox+0.32, 0.08), (ox+0.27, -0.02),
         (ox-0.24, -0.02), (ox-0.28, 0.04)]
    ax.add_patch(Polygon(b, closed=True, fc=BG, ec="none", zorder=3))
    ax.add_patch(Polygon(b, closed=True, fc=GREEN, ec=GREEN, lw=2.4, alpha=.28, zorder=4))
    ax.add_patch(Rectangle((ox-0.18, 0.08), 0.36, 0.17, fc=BG, ec=GREEN,
                           lw=2.2, zorder=5))
    ax.plot([ox-0.22, ox+0.22],[0.25, 0.25], c=GREEN, lw=2.4, zorder=6)
    arrow(ax, (ox+0.44, 0.02), (ox+0.36, 0.02), GREEN, 2.4, .9)
    for k, dxx in enumerate([0.04, 0.10, 0.16]):
        ax.plot([ox-0.32-dxx, ox-0.26-dxx],[0.03, 0.03], c=GREEN, lw=2.0,
                alpha=.55-0.14*k)                                    # 尾流速度線
    T(ax, ox, -0.24, "船在動", 21, GREEN)
    T(ax, ox, -0.335, "岸、水面都在後退", 14, WHITE, alpha=.75)

def rel_inside(ax):
    ix = 0.46
    ax.add_patch(Rectangle((ix-0.30, -0.14), 0.60, 0.50, fc=BG, ec=AMBER,
                           lw=2.6, alpha=.95, zorder=5))
    for x in (ix-0.17, ix+0.17):                                     # 兩扇閉窗
        ax.add_patch(Rectangle((x-0.055, 0.12), 0.11, 0.13, fc=BG, ec=WHITE,
                               lw=1.6, zorder=6))
        for k in range(2):
            ax.plot([x-0.042, x+0.042],[0.15+k*0.05, 0.15+k*0.05], c=WHITE,
                    lw=1.2, alpha=.6, zorder=7)
    c, x0, y0 = AMBER, ix-0.03, -0.06
    ax.add_patch(Circle((x0, y0+0.20), 0.040, fc=c, ec="none", zorder=8))
    ax.plot([x0, x0+0.01],[y0+0.165, y0+0.055], c=c, lw=6.5, solid_capstyle="round", zorder=8)
    ax.plot([x0+0.01, x0+0.12],[y0+0.055, y0+0.048], c=c, lw=5.5, solid_capstyle="round", zorder=8)
    ax.plot([x0+0.12, x0+0.125],[y0+0.048, y0-0.042], c=c, lw=5.0, solid_capstyle="round", zorder=8)
    ax.plot([x0+0.005, x0+0.085],[y0+0.13, y0+0.065], c=c, lw=4.0, solid_capstyle="round", zorder=9)
    T(ax, ix, -0.24, "一切靜止", 21, AMBER)
    T(ax, ix, -0.335, "沒有任何線索告訴你在動", 14, WHITE, alpha=.75)

def rel_note(ax):
    T(ax, 0.0, -0.62, "誰在動？從艙內無法判斷", 26, WHITE)
    T(ax, 0.0, -0.735, "這正是「相對運動」——地在動而人不知，同一個道理", 16, WHITE, alpha=.82)

print("── 兩種視角 ──")
emit("兩種視角",
     [("分隔", rel_split), ("艙外", rel_outside), ("艙內", rel_inside), ("題辭", rel_note)],
     title="兩種視角")

# ══════════════════════════════════════════════════════════════
# 3. 姚信：人為靈蟲，形最似天（近取諸身）
#    《晉書・天文志》載姚信：人為靈蟲，形最似天。今人頤前侈臨胸，
#    而項不能覆背。近取諸身，故知天之體南低入地，北則偏高。
# ══════════════════════════════════════════════════════════════
CX, CY, S = -0.46, 0.20, 1.10       # 人像基準（面朝右＝南）

def _pl(ax, pts, c, lw=3.6, z=5, a=1.0):
    ax.plot([p[0]*S+CX for p in pts], [p[1]*S+CY for p in pts],
            c=c, lw=lw, alpha=a, zorder=z, solid_capstyle="round",
            solid_joinstyle="round")

def head_profile(ax):
    """人的頭頸胸側影（面朝右）：前緣＝頤下垂覆胸，後緣＝項不覆背"""
    front = [(0.00,0.34),(0.11,0.32),(0.17,0.24),(0.185,0.14),(0.175,0.075),
             (0.245,0.035),(0.195,0.005),(0.215,-0.035),(0.185,-0.065),
             (0.235,-0.115),(0.215,-0.185),(0.155,-0.245),(0.105,-0.315),
             (0.085,-0.40)]                                    # 額→鼻→唇→頤→覆胸
    back  = [(0.00,0.34),(-0.11,0.32),(-0.175,0.24),(-0.19,0.13),(-0.165,0.03),
             (-0.125,-0.045),(-0.115,-0.115),(-0.135,-0.185),(-0.195,-0.265),
             (-0.265,-0.34),(-0.30,-0.40)]                     # 後腦→項→肩背
    _pl(ax, front, AMBER, 4.0)
    _pl(ax, back,  BLUE,  4.0)
    _pl(ax, [(0.085,-0.40),(-0.30,-0.40)], WHITE, 2.4, 4, .45)   # 胸背基線
    ax.scatter([0.055*S+CX],[0.135*S+CY], s=40, c=WHITE, zorder=6, alpha=.8)  # 眼
    T(ax, CX, CY+0.50, "人", 24, WHITE)
    T(ax, CX, CY+0.42, "側面（面朝南）", 13, WHITE, alpha=.55)

def head_labels(ax):
    """標籤置於人像下方左右，避免壓到天球"""
    T(ax, CX+0.24, CY-0.52, "頤前侈臨胸", 17, AMBER)
    T(ax, CX+0.24, CY-0.60, "下巴前伸、向下覆胸", 12, WHITE, alpha=.72)
    arrow(ax, (CX+0.19, CY-0.30), (CX+0.24, CY-0.47), AMBER, 1.6, .8)
    T(ax, CX-0.26, CY-0.52, "項不能覆背", 17, BLUE)
    T(ax, CX-0.26, CY-0.60, "後頸內縮、蓋不到背", 12, WHITE, alpha=.72)
    arrow(ax, (CX-0.20, CY-0.28), (CX-0.26, CY-0.47), BLUE, 1.6, .8)

def head_tilt(ax):
    """由人形讀出的『前低後高』傾斜軸"""
    ax.plot([CX-0.26, CX+0.20],[CY-0.32, CY-0.44], c=WHITE, lw=2.2,
            ls=(0,(6,4)), alpha=.75, zorder=6)
    T(ax, CX-0.02, CY-0.70, "前低　後高", 17, WHITE, alpha=.9)

def sky_tilt(ax):
    """天體南低北高：同一條傾斜軸套到天球上"""
    cx, cy, R = 0.47, 0.16, 0.29
    ax.add_patch(Circle((cx, cy), R, fill=False, ec=WHITE, lw=2.6, alpha=.85))
    ang = -14.5
    ax.add_patch(Ellipse((cx, cy), R*2, R*0.62, angle=ang, fill=False,
                         ec=WHITE, lw=1.6, alpha=.45))
    ar = math.radians(90 + ang)
    px, py = cx + R*math.cos(ar), cy + R*math.sin(ar)
    ax.plot([cx-(px-cx), px],[cy-(py-cy), py], c=WHITE, lw=1.6,
            ls=(0,(5,4)), alpha=.7)                                # 極軸
    ax.scatter([px],[py], s=140, c=AMBER, zorder=6)
    ax.scatter([cx-(px-cx)],[cy-(py-cy)], s=140, c=BLUE, zorder=6)
    ax.plot([cx-R*1.25, cx+R*1.25],[cy-R*0.72, cy-R*0.72], c=GREEN, lw=2.2, alpha=.7)
    T(ax, cx+R*1.25, cy-R*0.86, "地平", 13, GREEN, ha="right")
    T(ax, px-0.10, py+0.10, "北　偏高", 16, AMBER)
    T(ax, cx-(px-cx)+0.16, cy-(py-cy)-0.09, "南　低入地", 16, BLUE)
    T(ax, cx, cy+R+0.20, "天", 24, WHITE)

def yao_bridge(ax):
    arrow(ax, (0.08, 0.16), (-0.10, 0.16), WHITE, 2.4, .8)
    T(ax, -0.01, 0.25, "近取諸身", 15, WHITE, alpha=.85)

def yao_text(ax):
    T(ax, 0.0, 0.90, "人為靈蟲，形最似天", 26, WHITE)
    T(ax, 0.0, -0.70, "近取諸身，故知天之體南低入地，北則偏高", 18, WHITE, alpha=.92)
    T(ax, 0.0, -0.80, "《晉書・天文志》載三國吳・姚信", 14, WHITE, alpha=.6)
    T(ax, 0.0, -0.90, "※ 這是「以人體類比天體」的推論方式，非現代意義的觀測證據",
      13, WHITE, alpha=.5)

print("── 姚信：人形比天 ──")
emit("姚信人形比天",
     [("人形", head_profile), ("人形標註", head_labels), ("傾斜軸", head_tilt),
      ("天", sky_tilt), ("類比箭頭", yao_bridge), ("題辭", yao_text)],
     title="人形比天")

# ══════════════════════════════════════════════════════════════
# 4. 時間軸：考靈曜 vs 伽利略（相對運動的比喻早了約 1600 年）
# ══════════════════════════════════════════════════════════════
def tl_axis(ax):
    timeline(ax, [
        (0.10, "約公元 1 世紀", "《尚書・考靈曜》\n舟行而人不覺", AMBER),
        (0.88, "1632 年", "伽利略《關於兩大\n世界體系的對話》\n船艙論證", BLUE),
    ], y=0.24)

def tl_gap(ax):
    ax.plot([-0.70, 0.66],[-0.10, -0.10], c=WHITE, lw=1.6, alpha=.5)
    for x in (-0.70, 0.66):
        ax.plot([x, x],[-0.14, -0.06], c=WHITE, lw=1.6, alpha=.5)
    T(ax, -0.02, -0.21, "相隔約一千六百年", 24, WHITE)
    T(ax, -0.02, -0.32, "同一個比喻：在密閉的船艙裡，你察覺不到船在動", 16, WHITE, alpha=.82)
    T(ax, -0.02, -0.52, "但兩者說的「地動」不一樣", 18, GREEN)
    T(ax, -0.02, -0.62, "四游說：大地週期性平移（仍是地心）", 14, WHITE, alpha=.72)
    T(ax, -0.02, -0.71, "伽利略：地球自轉與公轉（日心）", 14, WHITE, alpha=.72)
    T(ax, -0.02, -0.86, "※ 相對運動的洞見相同，宇宙結構的結論不同——不宜逕稱「中國更早發現地動」",
      13, WHITE, alpha=.5)

def tl_title(ax):
    T(ax, 0, 0.86, "同一個思想實驗", 30, WHITE)
    T(ax, 0, 0.76, "中國緯書 vs 伽利略", 16, WHITE, alpha=.75)

print("── 時間軸對照 ──")
emit("時間軸",
     [("軸", tl_axis), ("間隔", tl_gap), ("題辭", tl_title)],
     title="時間軸")

# ══════════════════════════════════════════════════════════════
# 5. 圖卡：地有四游一頁看懂（9:16 輪播用）
# ══════════════════════════════════════════════════════════════
def card():
    f, ax = newcard()
    def t(x,y,s,size=15,c=WHITE,ha="left",w="normal",a=1.0):
        ax.text(x,y,s,fontproperties=FP,fontsize=size,color=c,ha=ha,va="center",
                weight=w,alpha=a)
    t(0.5, 0.945, "地有四游", 32, WHITE, "center", "bold")
    t(0.5, 0.905, "漢代緯書說：大地一直在動", 14, WHITE, "center", a=.75)
    rows = [
        ("冬至", "地上升，向北而西 三萬里", AMBER),
        ("夏至", "地下降，向南而東 三萬里", BLUE),
        ("春分・秋分", "居其中", WHITE),
    ]
    y = 0.82
    for k, v, c in rows:
        t(0.09, y, k, 20, c, w="bold"); t(0.09, y-0.035, v, 14, WHITE, a=.85)
        y -= 0.10
    ax.plot([0.08, 0.92],[y+0.03, y+0.03], c=WHITE, lw=1.0, alpha=.3)
    y -= 0.04
    t(0.5, y, "「地恆動不止，而人不知」", 20, AMBER, "center", "bold"); y -= 0.055
    t(0.5, y, "譬如人在大舟中閉牖而坐，舟行而人不覺也", 14, WHITE, "center", a=.85)
    y -= 0.09
    ax.plot([0.08, 0.92],[y+0.03, y+0.03], c=WHITE, lw=1.0, alpha=.3)
    y -= 0.04
    t(0.5, y, "比伽利略早約一千六百年", 20, BLUE, "center", "bold"); y -= 0.05
    t(0.5, y, "伽利略 1632 年《關於兩大世界體系的對話》\n用完全相同的船艙比喻論證相對運動",
      13, WHITE, "center", a=.8)
    y -= 0.10
    t(0.5, y, "※ 四游說的「地動」是週期性平移，", 13, WHITE, "center", a=.7); y -= 0.035
    t(0.5, y, "並非地球自轉或公轉；但相對運動的洞見是真的。", 13, WHITE, "center", a=.7)
    t(0.5, 0.045, "萬國星空 EP10・師大天文社", 11, WHITE, "center", a=.5)
    save(f, "_圖卡", "地有四游_圖卡_黑底.png", transparent=False)

print("── 圖卡 ──")
card()
print("all done")
