# -*- coding: utf-8 -*-
"""C-03 麒麟與倮獸：消失的第五象
依《大戴禮記・易本命》五蟲說、曾侯乙墓漆箱（戰國早期，約前 433 年）、
《考工記》、中國星座（師大天文社）.pptx p.13–21。
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_series_base import *

set_base("/sessions/funny-kind-mayer/mnt/Downloads--NTNU Insta/05_素材/C-03_麒麟與倮獸")

TIGER = "#E8ECF5"          # 白虎（近白，與 WHITE 區隔）

# ══════════════════════════════════════════════════════════════
# 獸形符號：折線描輪廓，小尺寸下仍可辨識（戰國漆器圖案化風格）
# 局部座標約 x∈[-1.3,1.1]、y∈[-0.6,0.8]，乘 s 後平移；rot 可轉向
# ══════════════════════════════════════════════════════════════
def _xf(pts, x, y, s, rot=0.0, flip=False):
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    f = -1.0 if flip else 1.0
    return [(x + s*(f*px*ca - py*sa), y + s*(f*px*sa + py*ca)) for px, py in pts]

def _draw(ax, pts, x, y, s, rot, c, lw, z=6, close=False, fill=False, alpha=1.0,
          flip=False):
    p = _xf(pts, x, y, s, rot, flip)
    if fill:
        ax.add_patch(Polygon(p, closed=True, fc=c, ec=c, lw=lw, alpha=alpha, zorder=z))
    else:
        if close: p = p + [p[0]]
        ax.plot([q[0] for q in p], [q[1] for q in p], c=c, lw=lw, alpha=alpha,
                zorder=z, solid_capstyle="round", solid_joinstyle="round")

def dragon_glyph(ax, x, y, s=0.20, c=GREEN, rot=0.0, lw=2.6, flip=False):
    """龍：尖吻大頭＋後掠角＋平滑 S 形身軀＋雙足＋卷尾（戰國漆器風格）"""
    n = 26
    body = []
    for k in range(n + 1):
        t = k / n
        bx = -1.02 + 1.58 * t
        body.append((bx, 0.17 * math.sin(2.1 * math.pi * t)))
    _draw(ax, body, x, y, s, rot, c, lw + 1.2, flip=flip)              # 身軀
    hx, hy = body[-1]
    _draw(ax, [(hx, hy + 0.04), (hx + 0.48, hy + 0.02), (hx + 0.04, hy - 0.16)],
          x, y, s, rot, c, lw + 0.2, close=True, flip=flip)            # 尖吻頭部
    _draw(ax, [(hx + 0.30, hy + 0.02), (hx + 0.42, hy - 0.02)], x, y, s, rot,
          c, lw - 1.2, alpha=.8, flip=flip)                            # 口縫
    _draw(ax, [(hx + 0.02, hy + 0.06), (hx - 0.14, hy + 0.44)], x, y, s, rot,
          c, lw, flip=flip)                                            # 角（後掠）
    _draw(ax, [(hx - 0.14, hy + 0.44), (hx - 0.02, hy + 0.56)], x, y, s, rot,
          c, lw - 1.0, flip=flip)
    _draw(ax, [(hx - 0.14, hy + 0.44), (hx - 0.30, hy + 0.52)], x, y, s, rot,
          c, lw - 1.0, flip=flip)
    _draw(ax, [(hx + 0.10, hy - 0.14), (hx + 0.22, hy - 0.32)], x, y, s, rot,
          c, lw - 1.2, alpha=.85, flip=flip)                           # 鬚
    for bx in (-0.66, 0.14):                                           # 雙足
        by = 0.17 * math.sin(2.1 * math.pi * (bx + 1.02) / 1.58)
        _draw(ax, [(bx, by), (bx - 0.08, by - 0.38), (bx + 0.10, by - 0.46)],
              x, y, s, rot, c, lw - 0.4, flip=flip)
    _draw(ax, [(-1.02, 0.0), (-1.32, 0.10), (-1.28, 0.36)], x, y, s, rot,
          c, lw, flip=flip)                                            # 卷尾
    _draw(ax, [(-1.32, 0.10), (-1.44, -0.06)], x, y, s, rot, c, lw - 1.2,
          alpha=.8, flip=flip)

def beast_glyph(ax, x, y, s=0.20, c=TIGER, rot=0.0, lw=2.6, horn=False, stripes=False, flip=False):
    """四足獸：虎／麒麟／鹿。horn=True 加分叉角"""
    back = [(-0.86,0.10),(-0.46,0.24),(0.04,0.22),(0.42,0.32)]
    _draw(ax, back, x, y, s, rot, c, lw+0.6, flip=flip)
    _draw(ax, [(0.42,0.32),(0.76,0.38),(0.84,0.22),(0.50,0.14)], x, y, s, rot,
          c, lw, close=True)                                   # 頭
    _draw(ax, [(-0.80,-0.10),(0.34,-0.12)], x, y, s, rot, c, lw, flip=flip)     # 腹
    _draw(ax, [(-0.86,0.10),(-0.80,-0.10)], x, y, s, rot, c, lw, flip=flip)     # 臀
    _draw(ax, [(0.50,0.14),(0.34,-0.12)], x, y, s, rot, c, lw, flip=flip)       # 前胸
    for bx in (-0.70,-0.50, 0.08, 0.28):
        _draw(ax, [(bx,-0.11),(bx-0.03,-0.42),(bx+0.07,-0.50)], x, y, s, rot,
              c, lw-0.4)                                       # 四足
    _draw(ax, [(-0.86,0.10),(-1.10,0.36),(-1.04,0.50)], x, y, s, rot, c, lw-0.4, flip=flip)
    _draw(ax, [(0.44,0.38),(0.50,0.54)], x, y, s, rot, c, lw-0.8, flip=flip)    # 耳
    if horn:
        _draw(ax, [(0.62,0.40),(0.70,0.66)], x, y, s, rot, c, lw, flip=flip)
        _draw(ax, [(0.70,0.66),(0.84,0.76)], x, y, s, rot, c, lw-0.8, flip=flip)
        _draw(ax, [(0.70,0.66),(0.60,0.80)], x, y, s, rot, c, lw-0.8, flip=flip)
    if stripes:
        for bx in (-0.60,-0.34,-0.08, 0.18):
            _draw(ax, [(bx,0.18),(bx+0.04,-0.04)], x, y, s, rot, c, lw-1.2, alpha=.7, flip=flip)

def bird_glyph(ax, x, y, s=0.20, c=AMBER, rot=0.0, lw=2.6, flip=False):
    """朱雀：身＋頭＋喙＋冠羽＋展翅＋三尾羽"""
    ax.add_patch(Ellipse(_xf([(0,0)], x, y, s, rot, flip)[0], 0.86*s, 0.48*s,
                         angle=rot, fill=False, ec=c, lw=lw+0.4, zorder=6))
    ax.add_patch(Circle(_xf([(0.44,0.22)], x, y, s, rot, flip)[0], 0.15*s,
                        fill=False, ec=c, lw=lw, zorder=7))
    _draw(ax, [(0.57,0.25),(0.84,0.20),(0.57,0.15)], x, y, s, rot, c, lw, close=True, flip=flip)
    _draw(ax, [(0.46,0.37),(0.56,0.66)], x, y, s, rot, c, lw-0.4, flip=flip)     # 冠羽
    _draw(ax, [(0.38,0.36),(0.40,0.60)], x, y, s, rot, c, lw-1.0, flip=flip)
    _draw(ax, [(0.06,0.20),(-0.10,0.52),(-0.34,0.68)], x, y, s, rot, c, lw, flip=flip)  # 翅
    _draw(ax, [(0.02,0.14),(-0.16,0.40),(-0.38,0.50)], x, y, s, rot, c, lw-1.0, flip=flip)
    for tp in [(-1.10,0.26),(-1.16,0.00),(-1.04,-0.26)]:              # 三尾羽
        _draw(ax, [(-0.42,0.02), tp], x, y, s, rot, c, lw-0.4, flip=flip)
    _draw(ax, [(0.12,-0.24),(0.14,-0.50),(0.28,-0.54)], x, y, s, rot, c, lw-0.6, flip=flip)
    _draw(ax, [(0.14,-0.50),(0.02,-0.56)], x, y, s, rot, c, lw-1.0, flip=flip)

# ══════════════════════════════════════════════════════════════
# 1. 四象方位盤：大家熟悉的版本（中央刻意留空）
# ══════════════════════════════════════════════════════════════
R_IN, R_OUT = 0.30, 0.66
FOUR = [                   # (方位角, 方位, 名稱, 色)
    (0.0,   "東", "青龍", GREEN),
    (90.0,  "北", "玄武", BLUE),
    (180.0, "西", "白虎", TIGER),
    (270.0, "南", "朱雀", AMBER),
]

def _sector(ax, a0, a1, c, alpha, z=3):
    pts = [(0,0)]
    for k in range(31):
        a = math.radians(a0 + (a1-a0)*k/30)
        pts.append((R_OUT*math.cos(a), R_OUT*math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=c, ec="none", alpha=alpha, zorder=z))

def four_ring(ax):
    """四象扇區（東在右、北在上——依天文圖慣例，非公文左右）"""
    for ang, pos, nm, c in FOUR:
        _sector(ax, ang-45, ang+45, c, .16)
        a = math.radians(ang)
        ax.plot([R_OUT*math.cos(math.radians(ang+45)), 0],
                [R_OUT*math.sin(math.radians(ang+45)), 0],
                c=WHITE, lw=1.0, alpha=.28, zorder=4)
        rr = (R_IN + R_OUT) / 2
        T(ax, rr*math.cos(a), rr*math.sin(a)+0.035, nm, 24, c, alpha=.95)
        T(ax, rr*math.cos(a), rr*math.sin(a)-0.055, pos, 15, c, alpha=.7)
    ax.add_patch(Circle((0,0), R_OUT, fill=False, ec=WHITE, lw=2.2, alpha=.65, zorder=5))

def four_center_empty(ax):
    """中央：空的（第五象的懸念）"""
    ax.add_patch(Circle((0,0), R_IN*0.62, fc=BG, ec="none", alpha=1.0, zorder=4))
    ax.add_patch(Circle((0,0), R_IN*0.62, fill=False, ec=WHITE, lw=1.8,
                        ls=(0,(5,4)), alpha=.55, zorder=5))
    T(ax, 0, 0.012, "？", 40, WHITE, alpha=.55)
    T(ax, 0, -0.075, "中央", 14, WHITE, alpha=.45)

def four_center_filled(ax, name="倮獸", sub="人・聖人", c=PURPLE):
    ax.add_patch(Circle((0,0), R_IN*0.62, fc=BG, ec="none", alpha=1.0, zorder=4))
    ax.add_patch(Circle((0,0), R_IN*0.62, fc=c, ec=c, lw=2.4, alpha=.22, zorder=5))
    ax.add_patch(Circle((0,0), R_IN*0.62, fill=False, ec=c, lw=2.4, zorder=6))
    T(ax, 0, 0.025, name, 24, c, alpha=.98)
    T(ax, 0, -0.062, sub, 13, WHITE, alpha=.75)

def four_title(ax):
    T(ax, 0, 0.90, "四象", 32, WHITE)
    T(ax, 0, 0.80, "東青龍、南朱雀、西白虎、北玄武", 16, WHITE, alpha=.75)
    T(ax, 0, -0.82, "四個方位，四隻神獸——那中間呢？", 20, WHITE)
    T(ax, 0, -0.92, "※ 方位依天文圖慣例（東在右、北在上）", 13, WHITE, alpha=.5)

def five_title(ax):
    T(ax, 0, 0.90, "五象", 32, WHITE)
    T(ax, 0, 0.80, "四象＋中央倮獸（人）", 16, WHITE, alpha=.75)
    T(ax, 0, -0.82, "五蟲說裡，人是「倮之蟲」的長", 20, WHITE)
    T(ax, 0, -0.92, "《大戴禮記・易本命》", 13, WHITE, alpha=.5)

print("── 四象盤／五象盤 ──")
emit("四象與五象",
     [("四象環", four_ring), ("中央留空", four_center_empty), ("題辭", four_title)],
     title="四象盤")
emit("四象與五象",
     [("四象環", four_ring), ("中央倮獸", four_center_filled), ("題辭", five_title)],
     title="五象盤")

# ── 1b. 民族來源對照（pptx p.13/15/19/21）──
ETHNIC = [
    (0.0,   "青龍", GREEN, "—"),
    (90.0,  "玄武", BLUE,  "夏越民族"),
    (180.0, "白虎", TIGER, "—"),
    (270.0, "朱雀", AMBER, "帝舜後裔・南蠻"),
]

def ethnic_ring(ax):
    for ang, nm, c, eth in ETHNIC:
        _sector(ax, ang-45, ang+45, c, .13)
        ax.plot([R_OUT*math.cos(math.radians(ang+45)), 0],
                [R_OUT*math.sin(math.radians(ang+45)), 0],
                c=WHITE, lw=1.0, alpha=.28, zorder=4)
        a = math.radians(ang); rr = (R_IN + R_OUT)/2
        T(ax, rr*math.cos(a), rr*math.sin(a)+0.035, nm, 21, c, alpha=.95)
        if eth != "—":
            T(ax, rr*math.cos(a), rr*math.sin(a)-0.055, eth, 13, WHITE, alpha=.72)
    ax.add_patch(Circle((0,0), R_OUT, fill=False, ec=WHITE, lw=2.2, alpha=.6, zorder=5))
    four_center_filled(ax, "倮獸", "中土・人", PURPLE)

def ethnic_deer(ax):
    """北方那一格的另一個候選：東胡的神鹿／麒麟"""
    a = math.radians(90); rr = (R_IN + R_OUT)/2
    x, y = rr*math.cos(a), rr*math.sin(a)
    arrow(ax, (x+0.26, y+0.20), (x+0.06, y+0.055), AMBER, 2.0, .85)
    T(ax, x+0.52, y+0.28, "或：神鹿／麒麟", 18, AMBER)
    T(ax, x+0.52, y+0.20, "東胡民族", 14, WHITE, alpha=.75)
    ax.add_patch(Circle((x, y), 0.145, fill=False, ec=AMBER, lw=2.2,
                        ls=(0,(4,3)), alpha=.9, zorder=6))

def ethnic_title(ax):
    T(ax, 0, 0.90, "四象是誰的神獸？", 30, WHITE)
    T(ax, 0, 0.80, "每一格背後，可能是一個不同的族群", 16, WHITE, alpha=.75)
    T(ax, 0, -0.84, "北方那一格，換過人", 22, WHITE)
    T(ax, 0, -0.93, "※ 族群對應為社團考據觀點，學界尚無定論", 13, WHITE, alpha=.5)

print("── 民族來源 ──")
emit("民族來源",
     [("方位環", ethnic_ring), ("東胡神鹿", ethnic_deer), ("題辭", ethnic_title)],
     title="民族來源")

# ══════════════════════════════════════════════════════════════
# 2. 曾侯乙墓漆箱（戰國早期，約前 433 年，湖北隨州擂鼓墩）
#    蓋面：中央篆文「斗」＋環列二十八宿全名（順時針）＋圈外龍虎
# ══════════════════════════════════════════════════════════════
XIU = ["角","亢","氐","房","心","尾","箕","斗","牛","女","虛","危","室","壁",
       "奎","婁","胃","昴","畢","觜","參","井","鬼","柳","星","張","翼","軫"]

def box_lid(ax):
    """漆箱蓋面：橢圓形二十八宿環（依文物為橢圓、順時針排列）"""
    A, B = 0.455, 0.305
    ts = [2*math.pi*i/400 for i in range(401)]
    for rr in (1.0, 0.72):
        ax.plot([A*rr*math.cos(t) for t in ts], [B*rr*math.sin(t) for t in ts],
                c=WHITE, lw=1.6, alpha=.55, zorder=4)
    for i, nm in enumerate(XIU):
        t = -2*math.pi*i/28 + math.pi/2          # 順時針，自上方起
        rr = 0.86
        ax.text(A*rr*math.cos(t), B*rr*math.sin(t), nm, fontproperties=FP,
                fontsize=12, color=WHITE, ha="center", va="center",
                weight="bold", alpha=.88, zorder=5)

def box_dou(ax):
    """中央「斗」字（北斗天極）"""
    T(ax, 0, 0.0, "斗", 50, AMBER, alpha=.98)
    ax.add_patch(Circle((0,0), 0.125, fill=False, ec=AMBER, lw=1.6, alpha=.45, zorder=4))

def box_dragon_tiger(ax):
    """圈外：右青龍、左白虎（依文物描述，觀者視角；獸首朝上）"""
    dragon_glyph(ax, 0.72, 0.0, s=0.185, c=GREEN, lw=2.4, flip=True)   # 首朝中心
    beast_glyph(ax, -0.72, 0.0, s=0.185, c=TIGER, lw=2.4, stripes=True)
    T(ax, 0.72, -0.20, "青龍", 19, GREEN)
    T(ax, -0.72, -0.20, "白虎", 19, TIGER)
    T(ax, 0.72, 0.235, "右", 13, WHITE, alpha=.45)
    T(ax, -0.72, 0.235, "左", 13, WHITE, alpha=.45)

def box_note(ax):
    T(ax, 0, 0.90, "曾侯乙墓漆箱蓋面", 28, WHITE)
    T(ax, 0, 0.80, "戰國早期・約公元前 433 年・湖北隨州擂鼓墩", 15, WHITE, alpha=.75)
    T(ax, 0, -0.62, "現存最早的二十八宿全部名稱記錄", 20, AMBER)
    T(ax, 0, -0.74, "中央篆文「斗」，環列二十八宿，圈外右青龍、左白虎", 15, WHITE, alpha=.8)
    T(ax, 0, -0.88, "※ 蓋面只有兩象——朱雀與玄武並不在蓋上", 16, WHITE, alpha=.85)

print("── 曾侯乙漆箱蓋面 ──")
emit("曾侯乙漆箱",
     [("宿環", box_lid), ("斗字", box_dou), ("龍虎", box_dragon_tiger), ("題辭", box_note)],
     title="漆箱蓋面")

# ── 2b. 側面圖案的兩種判讀（本集的核心爭議）──
#  每種判讀畫成「箱子的兩個立面」：上格＝南面、下格＝北面
PANEL = {"S": (0.42, 0.14), "N": (-0.06, -0.34)}      # (上緣 y, 下緣 y)

def _panel(ax, cx, key, ec=WHITE, a=.5):
    y1, y0 = PANEL[key]
    ax.add_patch(Rectangle((cx-0.33, y0), 0.66, y1-y0, fc=BG, ec="none", zorder=3))
    ax.add_patch(Rectangle((cx-0.33, y0), 0.66, y1-y0, fill=False, ec=ec,
                           lw=1.6, alpha=a, zorder=4))
    return (y0 + y1) / 2

def side_frames(ax):
    for cx, lab in [(-0.46, "說法一"), (0.46, "說法二")]:
        T(ax, cx, 0.55, lab, 21, WHITE, alpha=.9)
        for key, nm in [("S", "南面"), ("N", "北面")]:
            _panel(ax, cx, key)
            T(ax, cx-0.28, PANEL[key][0]+0.045, nm, 13, WHITE, ha="left", alpha=.55)
    ax.plot([0, 0],[-0.44, 0.60], c=WHITE, lw=1.4, alpha=.28)

def side_read1(ax):
    """南面朱雀；北面整面塗黑＝玄武"""
    cx = -0.46
    ymS = sum(PANEL["S"]) / 2
    bird_glyph(ax, cx+0.02, ymS-0.025, s=0.128, c=AMBER, lw=2.2)
    T(ax, cx+0.16, PANEL["S"][0]-0.045, "朱雀", 16, AMBER)
    y1, y0 = PANEL["N"]
    ax.add_patch(Rectangle((cx-0.325, y0+0.005), 0.65, y1-y0-0.01, fc=BLUE,
                           ec="none", alpha=.38, zorder=5))
    T(ax, cx, (y0+y1)/2+0.030, "整面塗黑", 17, WHITE)
    T(ax, cx, (y0+y1)/2-0.048, "＝玄武（黑色主北）", 13, WHITE, alpha=.8)

def side_read2(ax):
    """北面兩隻麒麟（一有角、一無角）；南面缺朱雀"""
    cx = 0.46
    ym = sum(PANEL["S"]) / 2
    for d in (-1, 1):
        ax.plot([cx-0.085*d, cx+0.085*d],[ym-0.055, ym+0.055], c=WHITE, lw=2.0,
                alpha=.30, zorder=5)
    T(ax, cx+0.155, ym-0.005, "缺", 16, WHITE, alpha=.6)
    ymN = sum(PANEL["N"]) / 2
    beast_glyph(ax, cx-0.150, ymN+0.012, s=0.098, c=PURPLE, lw=2.0, horn=True)
    beast_glyph(ax, cx+0.150, ymN+0.012, s=0.098, c=PURPLE, lw=2.0, horn=False)
    T(ax, cx, PANEL["N"][1]+0.042, "一有角、一無角", 14, PURPLE)

def side_title(ax):
    T(ax, 0, 0.90, "側面畫的是什麼？兩種判讀", 28, WHITE)
    T(ax, 0, 0.80, "同一件文物，學界讀出不同的答案", 15, WHITE, alpha=.75)
    T(ax, 0, -0.60, "如果北面是麒麟——四象的北方，本來不是玄武？", 20, WHITE)
    T(ax, 0, -0.76, "※ 漆箱蓋面（斗＋二十八宿＋青龍白虎）各家一致；", 13, WHITE, alpha=.55)
    T(ax, 0, -0.845, "側面圖案的辨識與命名則有分歧，本集並列呈現，不採定論。",
      13, WHITE, alpha=.55)

print("── 側面兩種判讀 ──")
emit("側面判讀",
     [("外框", side_frames), ("說法一", side_read1), ("說法二", side_read2),
      ("題辭", side_title)],
     title="側面判讀")

# ══════════════════════════════════════════════════════════════
# 3. 五蟲說（《大戴禮記・易本命》）
# ══════════════════════════════════════════════════════════════
WU = [   # (分類, 之長, 色, 對應四象, 是否衝突)
    ("有羽之蟲", "鳳皇", AMBER,  "南・朱雀", False),
    ("有毛之蟲", "麒麟", PURPLE, "西・白虎？", True),
    ("有甲之蟲", "神龜", BLUE,   "北・玄武", False),
    ("有鱗之蟲", "蛟龍", GREEN,  "東・青龍", False),
    ("倮之蟲",   "聖人", TIGER,  "中央・無此格", True),
]

def wu_rows(ax):
    y0, dy = 0.46, 0.205
    for i, (cat, chief, c, four, clash) in enumerate(WU):
        y = y0 - i*dy
        ax.add_patch(Rectangle((-0.88, y-0.075), 1.76, 0.15, fc=c, ec="none",
                               alpha=.10, zorder=3))
        T(ax, -0.80, y, cat, 19, WHITE, ha="left", alpha=.9)
        T(ax, -0.16, y, "三百六十", 14, WHITE, ha="left", alpha=.5)
        T(ax, 0.26, y, chief, 22, c, ha="left")
        T(ax, 0.60, y, four, 15, (AMBER if clash else WHITE), ha="left",
          alpha=(.95 if clash else .6))
        if clash:
            ax.add_patch(Rectangle((-0.88, y-0.075), 1.76, 0.15, fill=False,
                                   ec=AMBER, lw=1.6, alpha=.55, zorder=4))

def wu_head(ax):
    T(ax, 0, 0.90, "五蟲說", 32, WHITE)
    T(ax, 0, 0.80, "《大戴禮記・易本命》把生物分成五類，各有一位「長」", 15, WHITE, alpha=.78)
    T(ax, -0.80, 0.60, "分類", 14, WHITE, ha="left", alpha=.5)
    T(ax, 0.26, 0.60, "之長", 14, WHITE, ha="left", alpha=.5)
    T(ax, 0.60, 0.60, "對應四象", 14, WHITE, ha="left", alpha=.5)
    ax.plot([-0.88, 0.88],[0.555, 0.555], c=WHITE, lw=1.2, alpha=.35)

def wu_note(ax):
    T(ax, 0, -0.66, "白虎不在名單裡，多出來的是人", 22, AMBER)
    T(ax, 0, -0.78, "毛蟲之長是麒麟；而「倮之蟲」的長是聖人——也就是人", 15, WHITE, alpha=.82)
    T(ax, 0, -0.90, "原文：「有毛之蟲三百六十，而麒麟為之長……倮之蟲三百六十，而聖人為之長。」",
      13, WHITE, alpha=.55)

print("── 五蟲說 ──")
emit("五蟲說", [("表列", wu_rows), ("表頭", wu_head), ("結語", wu_note)], title="五蟲說")

# ── 3b. 四象 vs 五蟲 對位圖 ──
def cmp_cols(ax):
    T(ax, -0.52, 0.78, "四象", 26, WHITE)
    T(ax,  0.52, 0.78, "五蟲之長", 26, WHITE)
    ax.plot([-0.52, -0.52],[-0.66, 0.68], c=WHITE, lw=1.0, alpha=.2)
    ax.plot([ 0.52,  0.52],[-0.66, 0.68], c=WHITE, lw=1.0, alpha=.2)

LEFT  = [("青龍", GREEN), ("朱雀", AMBER), ("白虎", TIGER), ("玄武", BLUE), (None, None)]
RIGHT = [("蛟龍", GREEN), ("鳳皇", AMBER), ("麒麟", PURPLE), ("神龜", BLUE), ("聖人", TIGER)]

def cmp_items(ax):
    y0, dy = 0.52, 0.26
    for i in range(5):
        y = y0 - i*dy
        ln, lc = LEFT[i]; rn, rc = RIGHT[i]
        if ln:
            ax.add_patch(Circle((-0.52, y), 0.092, fc=BG, ec="none", zorder=3))
            ax.add_patch(Circle((-0.52, y), 0.092, fc=lc, ec=lc, lw=2.0, alpha=.20, zorder=4))
            ax.add_patch(Circle((-0.52, y), 0.092, fill=False, ec=lc, lw=2.0, zorder=5))
            T(ax, -0.52, y, ln, 16, WHITE, alpha=.95)
        else:
            ax.add_patch(Circle((-0.52, y), 0.092, fill=False, ec=WHITE, lw=1.6,
                                ls=(0,(4,3)), alpha=.45, zorder=5))
            T(ax, -0.52, y, "無", 16, WHITE, alpha=.45)
        ax.add_patch(Circle((0.52, y), 0.092, fc=BG, ec="none", zorder=3))
        ax.add_patch(Circle((0.52, y), 0.092, fc=rc, ec=rc, lw=2.0, alpha=.20, zorder=4))
        ax.add_patch(Circle((0.52, y), 0.092, fill=False, ec=rc, lw=2.0, zorder=5))
        T(ax, 0.52, y, rn, 16, WHITE, alpha=.95)

def cmp_links(ax):
    y0, dy = 0.52, 0.26
    for i in range(5):
        y = y0 - i*dy
        clash = (i == 2) or (i == 4)
        c = AMBER if clash else WHITE
        ax.plot([-0.435, 0.435],[y, y], c=c, lw=(2.2 if clash else 1.4),
                ls=((0,(5,4)) if clash else "-"), alpha=(.9 if clash else .35), zorder=3)
        if i == 2:
            T(ax, 0.0, y+0.065, "毛獸的位置對不上", 14, AMBER)
        if i == 4:
            T(ax, 0.0, y+0.065, "四象沒有這一格", 14, AMBER)

def cmp_title(ax):
    T(ax, 0, 0.90, "兩套體系，對不上兩格", 28, WHITE)
    T(ax, 0, -0.76, "第五象，可能一直都在——只是被留在名單之外", 20, WHITE)
    T(ax, 0, -0.88, "※ 四象與五蟲屬不同來源的分類系統，此圖為對照示意，非古人明確對應表",
      13, WHITE, alpha=.5)

print("── 四象 vs 五蟲 ──")
emit("四象五蟲對照",
     [("欄位", cmp_cols), ("兩欄項目", cmp_items), ("連線", cmp_links), ("題辭", cmp_title)],
     title="四象五蟲對照")

# ══════════════════════════════════════════════════════════════
# 4. 倮獸主星的三個候選（並列，明說未解）
# ══════════════════════════════════════════════════════════════
CAND = [
    (-0.60, "軒轅", "十七顆星", GREEN,
     "星數正好十七", "獅子座一帶"),
    ( 0.00, "牛郎織女", "河鼓三星＋織女三星", AMBER,
     "蒙古人的「三鹿」", "夏季大三角一帶"),
    ( 0.60, "弧矢", "九顆星", BLUE,
     "《考工記》弧旌枉矢", "大犬・船尾座一帶"),
]

def cand_boxes(ax):
    for cx, nm, sub, c, why, where in CAND:
        ax.add_patch(Rectangle((cx-0.28, -0.34), 0.56, 0.72, fc=c, ec="none",
                               alpha=.10, zorder=3))
        ax.add_patch(Rectangle((cx-0.28, -0.34), 0.56, 0.72, fill=False, ec=c,
                               lw=2.0, alpha=.75, zorder=4))
        T(ax, cx, 0.28, nm, 23, c)
        T(ax, cx, 0.185, sub, 13, WHITE, alpha=.72)
        T(ax, cx, 0.06, "？", 44, c, alpha=.45)
        ax.plot([cx-0.20, cx+0.20],[-0.06, -0.06], c=WHITE, lw=1.0, alpha=.28)
        T(ax, cx, -0.135, why, 14, WHITE, alpha=.88)
        T(ax, cx, -0.225, where, 12, WHITE, alpha=.55)

def cand_stars(ax):
    """各候選的星點示意（僅示意數量與大致排列，精確星圖見星圖層素材）"""
    import random
    layouts = {
        "軒轅": [(-0.20,0.42),(-0.14,0.46),(-0.07,0.44),(-0.01,0.47),(0.05,0.43),
                 (0.11,0.47),(0.17,0.44),(-0.17,0.38),(-0.10,0.39),(-0.03,0.37),
                 (0.04,0.39),(0.10,0.37),(0.16,0.39),(-0.06,0.33),(0.01,0.32),
                 (0.08,0.34),(0.14,0.31)],
        "牛郎織女": [(-0.14,0.46),(-0.11,0.42),(-0.17,0.42),
                     (0.13,0.36),(0.16,0.32),(0.10,0.32)],
        "弧矢": [(-0.18,0.45),(-0.10,0.47),(-0.02,0.44),(0.06,0.40),(0.13,0.35),
                 (0.17,0.29),(0.09,0.30),(0.01,0.33),(-0.07,0.37)],
    }
    for cx, nm, sub, c, why, where in CAND:
        for dx, dy in layouts[nm]:
            ax.scatter([cx+dx*0.88],[dy+0.075], s=32, c=c, alpha=.85, zorder=6)

def cand_title(ax):
    T(ax, 0, 0.90, "倮獸的主星是哪一組？", 28, WHITE)
    T(ax, 0, 0.80, "師大天文社的考據列出三個候選——三個都還帶著問號", 15, WHITE, alpha=.78)
    T(ax, 0, -0.52, "這一題還沒有答案", 24, WHITE)
    T(ax, 0, -0.64, "沒有任何傳世文獻明確指定「中央倮獸」對應哪一個星官", 15, WHITE, alpha=.8)
    T(ax, 0, -0.80, "※ 星點為數量與排列示意，非精確星圖；", 13, WHITE, alpha=.5)
    T(ax, 0, -0.885, "軒轅十七星之數依 Stellarium 中國星官資料核算為 17 顆。",
      13, WHITE, alpha=.5)

print("── 倮獸主星三候選 ──")
emit("倮獸主星候選",
     [("方框", cand_boxes), ("星點示意", cand_stars), ("題辭", cand_title)],
     title="倮獸主星候選")

# ══════════════════════════════════════════════════════════════
# 5. 9:16 圖卡
# ══════════════════════════════════════════════════════════════
def card():
    f, ax = newcard()
    def t(x, y, s, size=15, c=WHITE, ha="left", w="normal", a=1.0):
        ax.text(x, y, s, fontproperties=FP, fontsize=size, color=c, ha=ha,
                va="center", weight=w, alpha=a)
    t(0.5, 0.955, "麒麟與倮獸", 31, WHITE, "center", "bold")
    t(0.5, 0.920, "四象，可能本來是五象", 14, WHITE, "center", a=.75)

    t(0.5, 0.875, "五蟲說《大戴禮記・易本命》", 16, AMBER, "center", "bold")
    rows = [("有羽之蟲", "鳳皇", AMBER), ("有毛之蟲", "麒麟", PURPLE),
            ("有甲之蟲", "神龜", BLUE), ("有鱗之蟲", "蛟龍", GREEN),
            ("倮之蟲",   "聖人（人）", WHITE)]
    y = 0.835
    for cat, chief, c in rows:
        t(0.13, y, cat, 14, WHITE, a=.8); t(0.62, y, chief, 16, c, w="bold")
        y -= 0.038
    y -= 0.012
    ax.plot([0.10, 0.90],[y, y], c=WHITE, lw=1.0, alpha=.3); y -= 0.032
    t(0.5, y, "白虎不在名單裡，多出來的是人", 15, AMBER, "center", "bold"); y -= 0.055

    t(0.5, y, "曾侯乙墓漆箱（約前 433 年）", 16, BLUE, "center", "bold"); y -= 0.036
    t(0.5, y, "蓋面：篆文「斗」＋二十八宿全名", 13, WHITE, "center", a=.82); y -= 0.030
    t(0.5, y, "圈外右青龍、左白虎——只有兩象", 13, WHITE, "center", a=.82); y -= 0.030
    t(0.5, y, "側面判讀有分歧：南朱雀／北玄武？還是北麒麟？", 13, AMBER, "center", a=.9)
    y -= 0.042
    ax.plot([0.10, 0.90],[y, y], c=WHITE, lw=1.0, alpha=.3); y -= 0.032

    t(0.5, y, "中央倮獸的主星？三個候選", 16, PURPLE, "center", "bold"); y -= 0.038
    for nm, why in [("軒轅十七星", "星數正好十七"),
                    ("牛郎織女", "＝蒙古人的「三鹿」"),
                    ("弧矢九星", "《考工記》弧旌枉矢")]:
        t(0.15, y, "・" + nm, 14, WHITE, w="bold"); t(0.60, y, why, 12, WHITE, a=.7)
        y -= 0.034
    y -= 0.014
    t(0.5, y, "三個都還帶著問號——這題沒有答案", 15, WHITE, "center", "bold")

    y -= 0.055
    t(0.5, y, "※ 四象與五蟲屬不同來源的分類系統；", 12, WHITE, "center", a=.62)
    y -= 0.028
    t(0.5, y, "族群對應與主星候選為社團考據觀點，學界尚無定論。",
      12, WHITE, "center", a=.62)
    t(0.5, 0.042, "萬國星空 EP11・師大天文社", 11, WHITE, "center", a=.5)
    save(f, "_圖卡", "麒麟與倮獸_圖卡_黑底.png", transparent=False)

print("── 圖卡 ──")
card()
print("all done")
