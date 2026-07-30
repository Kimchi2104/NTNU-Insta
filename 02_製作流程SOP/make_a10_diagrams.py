# -*- coding: utf-8 -*-
"""A-10 東加：星路導航原理概念圖
星圖以外的部分——「星路怎麼用來航行」與「星座名就是島名」，
連線圖表達不了，用幾何示意補足。共用 C 系列骨架（同規格、同色票）。
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_series_base import *

set_base("/sessions/funny-kind-mayer/mnt/Downloads--NTNU Insta/05_素材/A-10_東加")

HZ = -0.30                       # 海平線（水面）
DUCKS = [                        # (中文, 原名, 高於海平線, 色)
    ("野鴨",     "Toloa",      0.22, AMBER),
    ("大野鴨",   "Toloalahi",  0.48, GREEN),
    ("南部野鴨", "Toloatonga", 0.74, BLUE),
]
BX   = 0.24                      # 星升起的方位（垂線）
CX   = -0.46                     # 獨木舟中心

# ══════════════════════════════════════════════════════════════
# 1. 星路導航原理：三隻野鴨從同一方位接力升起
# ══════════════════════════════════════════════════════════════
def horizon(ax):
    ax.plot([-0.94, 0.94], [HZ, HZ], c=WHITE, lw=2.4, alpha=.65)
    for k in range(3):                                  # 近景波紋
        water(ax, y=HZ-0.11-k*0.004, x0=-0.94, x1=0.94, c=BLUE,
              rows=1, amp=0.013, freq=18+k*5, phase=k*1.7)
    T(ax, -0.88, HZ-0.055, "海平線", 13, WHITE, alpha=.45)

def bearing(ax):
    """固定方位：星升起的那一點，也是船頭要對的方向"""
    ax.plot([BX, BX], [HZ, HZ+0.86], c=WHITE, lw=1.4, ls=(0,(5,5)), alpha=.35)
    ax.add_patch(Polygon([(BX-0.09, HZ), (BX+0.09, HZ), (BX, HZ+0.055)],
                         closed=True, fc=AMBER, ec="none", alpha=.6, zorder=5))
    T(ax, BX+0.06, HZ-0.105, "同一個方位", 16, AMBER, ha="left")
    T(ax, BX+0.06, HZ-0.175, "星在這裡升起，船頭就對這裡", 13, WHITE,
      ha="left", alpha=.75)

def ducks(ax, upto=3):
    """三隻野鴨依序升起（upto 控制出現到第幾隻，供逐格動畫）"""
    for i, (zh, nat, h, c) in enumerate(DUCKS):
        if i >= upto: continue
        y = HZ + h
        for dx, dy, sz in [(-0.045, 0.012, 46), (0.0, 0.0, 78), (0.048, -0.014, 40)]:
            ax.scatter([BX+dx], [y+dy], s=sz, c=c, alpha=.95, zorder=6)
        ax.plot([BX-0.045, BX+0.048], [y+0.012, y-0.014], c=c, lw=2.0,
                alpha=.85, zorder=6)
        T(ax, BX+0.32, y+0.014, nat, 18, c, ha="left")
        T(ax, BX+0.32, y-0.062, zh, 13, WHITE, ha="left", alpha=.72)
        T(ax, BX-0.17, y, f"{i+1}", 16, c)
        if i:                                           # 升起順序箭頭
            ax.annotate("", xy=(BX-0.115, y-0.03),
                        xytext=(BX-0.115, HZ + DUCKS[i-1][2] + 0.03),
                        arrowprops=dict(arrowstyle="->", color=c, lw=1.6, alpha=.55))

def canoe(ax):
    """雙體獨木舟（側視），船頭朝右＝朝著星升起的方位；船底坐在海平線上"""
    hull = [(CX-0.28, HZ+0.085), (CX+0.26, HZ+0.085), (CX+0.20, HZ),
            (CX-0.22, HZ), (CX-0.26, HZ+0.04)]
    ax.add_patch(Polygon(hull, closed=True, fc=BG, ec="none", zorder=6))
    ax.add_patch(Polygon(hull, closed=True, fc=GREEN, ec=GREEN, lw=2.6,
                         alpha=.30, zorder=7))
    ax.plot([CX-0.04, CX-0.04], [HZ+0.085, HZ+0.40], c=GREEN, lw=2.6, zorder=8)
    ax.plot([CX-0.04, CX+0.16, CX-0.04], [HZ+0.40, HZ+0.20, HZ+0.20], c=GREEN,
            lw=2.2, zorder=8)                            # 三角帆
    ax.plot([CX-0.28, CX-0.44], [HZ+0.045, HZ+0.045], c=GREEN, lw=2.0,
            alpha=.7, zorder=7)                          # 支架（雙體）
    arrow(ax, (CX+0.46, HZ+0.045), (CX+0.30, HZ+0.045), GREEN, 2.4, .9)
    T(ax, CX, HZ+0.475, "獨木舟", 15, GREEN)

def path_title(ax):
    T(ax, 0.0, 0.92, "星路：三隻野鴨接力", 30, WHITE)
    T(ax, 0.0, 0.82, "Houmatoloa —— 野鴨的土地", 16, WHITE, alpha=.78)
    T(ax, 0.0, -0.66, "一隻沉下去，下一隻在同一個方位升起", 21, WHITE)
    T(ax, 0.0, -0.755, "整夜盯著同一個方向，就不會偏航", 15, WHITE, alpha=.82)
    T(ax, 0.0, -0.90, "※ 示意圖；實際星路由多顆星依序升落構成，非等比例高度",
      13, WHITE, alpha=.5)

print("── 星路導航原理 ──")
emit("星路原理",
     [("海與地平", horizon), ("方位", bearing), ("三隻野鴨", ducks),
      ("獨木舟", canoe), ("題辭", path_title)],
     title="星路原理")
emit_frames("星路原理", "星路原理_接力",
            lambda ax, i: (horizon(ax), bearing(ax), ducks(ax, upto=i+1), canoe(ax)), 3)

# ══════════════════════════════════════════════════════════════
# 2. 星座的名字就是島的名字（星名 ↔ 地名）
# ══════════════════════════════════════════════════════════════
#  左：北方天空剖面（星座在北方的最大高度）／右：島嶼由南到北
SKY = [   # (原名, 中文, 赤緯, 色)
    ("Kapakau'o'tafahi", "塔法希翼", 60.0, AMBER),
    ("ʻAo ʻo ʻUvea",     "烏韋阿雲", 29.0, GREEN),
]
LAT_TONGA = 21.0          # 東加本島約 21°S
ISLES = [ # (島名, 緯度°S, 色)
    ("ʻUvea（瓦利斯）", 13.3, GREEN),
    ("Tafahi",         15.9, AMBER),
    ("Tonga 本島",     21.0, WHITE),
]

def sky_panel(ax):
    """左半：從東加看北方天空，兩個星座的最大高度"""
    ox, R = -0.46, 0.40
    ax.plot([ox-R*1.15, ox+R*1.15], [-0.30, -0.30], c=WHITE, lw=2.2, alpha=.65)
    T(ax, ox, -0.375, "北方地平線", 13, WHITE, alpha=.5)
    ax.add_patch(Arc((ox, -0.30), R*2, R*2, theta1=0, theta2=180,
                     ec=WHITE, lw=1.2, ls=(0,(4,4)), alpha=.30))
    for nat, zh, dec, c in SKY:
        alt = 90.0 - LAT_TONGA - dec          # 上中天高度（北方）
        a = math.radians(alt)
        x, y = ox + R*math.cos(a)*0.0 + 0.0, -0.30 + R*math.sin(a)
        ax.scatter([ox], [y], s=150, c=c, zorder=6)
        ax.plot([ox-R*0.9, ox+R*0.9], [y, y], c=c, lw=1.2, ls=(0,(4,3)), alpha=.45)
        T(ax, ox+R*0.98, y+0.032, nat, 14, c, ha="left")
        T(ax, ox+R*0.98, y-0.036, f"高度 {alt:.0f}°", 12, WHITE, ha="left", alpha=.7)
    T(ax, ox, 0.30, "從東加看北方", 19, WHITE)
    T(ax, ox, 0.225, "（緯度 21°S）", 13, WHITE, alpha=.6)

def isle_panel(ax):
    """右半：島嶼由南到北排列"""
    ix = 0.48
    ax.plot([ix, ix], [-0.34, 0.20], c=WHITE, lw=2.0, alpha=.55)
    arrow(ax, (ix, 0.26), (ix, 0.14), WHITE, 2.0, .7)
    T(ax, ix, 0.32, "北", 16, WHITE, alpha=.7)
    for nm, lat, c in ISLES:
        y = -0.34 + (21.0 - lat) / (21.0 - 12.5) * 0.50
        ax.scatter([ix], [y], s=170, c=c, zorder=6)
        T(ax, ix+0.075, y+0.028, nm, 15, c, ha="left")
        T(ax, ix+0.075, y-0.038, f"{lat:.1f}°S", 12, WHITE, ha="left", alpha=.65)
    T(ax, ix, -0.50, "往北航行的島鏈", 15, WHITE, alpha=.75)

def name_links(ax):
    """星座 ↔ 同名島嶼"""
    ox = -0.46
    for nat, zh, dec, c in SKY:
        alt = 90.0 - LAT_TONGA - dec
        y1 = -0.30 + 0.40*math.sin(math.radians(alt))
        isle = "Tafahi" if "tafahi" in nat.lower() else "ʻUvea（瓦利斯）"
        lat = dict((n, l) for n, l, _ in ISLES)[isle]
        y2 = -0.34 + (21.0 - lat) / (21.0 - 12.5) * 0.50
        ax.annotate("", xy=(0.44, y2), xytext=(ox+0.30, y1),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.8, alpha=.6,
                                    connectionstyle="arc3,rad=-0.18"))
    T(ax, 0.02, 0.44, "同一個名字", 17, WHITE, alpha=.9)

def name_title(ax):
    T(ax, 0.0, 0.92, "星座的名字，就是要去的島", 28, WHITE)
    T(ax, 0.0, 0.82, "Kapakau'o'tafahi＝塔法希島之翼　ʻAo ʻo ʻUvea＝烏韋阿之雲",
      15, WHITE, alpha=.78)
    T(ax, 0.0, -0.60, "要去哪個島，就看那個島的星", 21, WHITE)
    T(ax, 0.0, -0.71, "兩個星座都在北方天空——而這兩個島，都在東加的北邊",
      15, WHITE, alpha=.82)
    T(ax, 0.0, -0.86, "※ 高度為上中天理論值（90°−緯度−赤緯），未計大氣折射與歲差；",
      13, WHITE, alpha=.5)
    T(ax, 0.0, -0.925, "星名與島名的關聯屬語源與航海傳統的推論，非古文獻明確記載。",
      13, WHITE, alpha=.5)

print("── 星名＝島名 ──")
emit("星名島名",
     [("北方天空", sky_panel), ("島鏈", isle_panel), ("同名連線", name_links),
      ("題辭", name_title)],
     title="星名島名")

# ══════════════════════════════════════════════════════════════
# 3. 9:16 圖卡
# ══════════════════════════════════════════════════════════════
def card():
    f, ax = newcard()
    def t(x, y, s, size=15, c=WHITE, ha="left", w="normal", a=1.0):
        ax.text(x, y, s, fontproperties=FP, fontsize=size, color=c, ha=ha,
                va="center", weight=w, alpha=a)
    t(0.5, 0.955, "東加：星星的名字", 30, WHITE, "center", "bold")
    t(0.5, 0.922, "就是航線", 30, WHITE, "center", "bold")
    t(0.5, 0.884, "Ko e ngaahi fetuʻu ʻo Tonga", 13, WHITE, "center", a=.7)

    y = 0.835
    t(0.5, y, "三隻野鴨串成一條星路", 17, AMBER, "center", "bold"); y -= 0.042
    for nat, zh, intl in [("Toloa", "野鴨", "獵戶座腰帶"),
                          ("Toloalahi", "大野鴨", "假十字"),
                          ("Toloatonga", "南部野鴨", "南十字")]:
        t(0.13, y, nat, 15, AMBER, w="bold")
        t(0.47, y, zh, 14, WHITE, a=.85); t(0.72, y, intl, 13, WHITE, a=.6)
        y -= 0.035
    y -= 0.008
    t(0.5, y, "Houmatoloa（野鴨的土地）＝這條路本身", 14, WHITE, "center", a=.88)
    y -= 0.030
    t(0.5, y, "橫跨天空 95°，一隻沉下、下一隻在同方位升起", 13, WHITE, "center", a=.72)

    y -= 0.048
    ax.plot([0.10, 0.90], [y, y], c=WHITE, lw=1.0, alpha=.3); y -= 0.036
    t(0.5, y, "星座名＝島名", 17, GREEN, "center", "bold"); y -= 0.040
    for nat, zh, isle in [("Kapakau'o'tafahi", "塔法希翼", "Tafahi 島（仙后座）"),
                          ("ʻAo ʻo ʻUvea", "烏韋阿雲", "ʻUvea 瓦利斯島（北冕座）")]:
        t(0.11, y, nat, 14, GREEN, w="bold"); y -= 0.030
        t(0.15, y, f"{zh}　→　{isle}", 13, WHITE, a=.8); y -= 0.036
    t(0.5, y, "兩個星座都在北方天空，兩個島都在東加北邊", 13, WHITE, "center", a=.75)

    y -= 0.050
    ax.plot([0.10, 0.90], [y, y], c=WHITE, lw=1.0, alpha=.3); y -= 0.036
    t(0.5, y, "具名亮星", 17, BLUE, "center", "bold"); y -= 0.038
    for nat, intl in [("Maʻafutoka", "Canopus 老人星"),
                      ("Maʻafulele", "Sirius 天狼星"),
                      ("Velitoa hififo / hahake", "Rigel 參宿七／Betelgeuse 參宿四"),
                      ("Hikuleʻo", "Arcturus 大角星"),
                      ("Motuliki", "Pleiades 昴宿星團")]:
        t(0.12, y, nat, 13, BLUE, w="bold"); t(0.52, y, intl, 12, WHITE, a=.72)
        y -= 0.031

    y -= 0.030
    t(0.5, y, "※ 星路由多顆星依序升落構成；星名與島名的關聯", 12, WHITE, "center", a=.6)
    y -= 0.026
    t(0.5, y, "屬語源與航海傳統的推論，非古文獻明確記載。", 12, WHITE, "center", a=.6)
    t(0.5, 0.042, "萬國星空 EP13・師大天文社", 11, WHITE, "center", a=.5)
    save(f, "_圖卡", "東加星路_圖卡_黑底.png", transparent=False)

print("── 圖卡 ──")
card()
print("all done")
