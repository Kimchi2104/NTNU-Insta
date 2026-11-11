# -*- coding: utf-8 -*-
"""H-元宵｜概念圖（方形透明分層：Reels 定格頁一頁疊一層）
  C-HYX-01_上元天官     → 逐字稿 02 鏡（上元層→三元層）：4 秒讀得完——只放大「上元 正月十五｜天官賜福」，
                          中元、下元縮成淡色小字
  C-HYX-02_同名兩回事   → 逐字稿 04 鏡開頭（天官層→紫微垣層）：左右分欄，中間只連一個「紫微」
輸出：05_素材/H-元宵_紫微垣/_概念圖/（--lang en → _概念圖/en/）

來源：三元日與三官職掌——後世道教通說（上元天官賜福、中元地官赦罪、下元水官解厄）；
      天官封號「上元一品賜福天官紫微大帝」見《元始天尊說三官寶號經》（《正統道藏》，未親核）；
      紫微垣——Stellarium chinese CON 032／033（右垣 7 星、左垣 8 星）、《晉書・天文志》「一曰紫微，大帝之坐也」。
版權：純文字與幾何，不用廟宇照片（照片美宣另尋授權）。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, WHITE, PURPLE, T
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/H-元宵_紫微垣/_概念圖")
C.set_base(OUT)
GREY, RED = "#7C8BA8", "#FF6B6B"
LANG = "zh"
TXT = {
    "zh": {
        "san": "三官大帝",
        "shang": "上元", "shang_d": "正月十五", "shang_g": "天官賜福",
        "zhong": "中元　七月十五　地官赦罪", "xia": "下元　十月十五　水官解厄",
        "l_head": "三官信仰", "l_name": "天官", "l_sub1": "上元一品賜福天官", "l_sub2": "紫微大帝",
        "l_foot": "道教・民間信仰的神",
        "r_head": "古代星官", "r_name": "紫微垣", "r_sub1": "北天極周圍的星區", "r_sub2": "左垣 8 星・右垣 7 星",
        "r_foot": "《晉書》：一曰紫微，大帝之坐",
        "same": "同名「紫微」",
    },
    "en": {
        "san": "The Three Officials",
        "shang": "Upper Yuan", "shang_d": "1st month, 15th day", "shang_g": "Heaven Official grants blessings",
        "zhong": "Middle Yuan · 7th month, 15th · Earth Official pardons",
        "xia": "Lower Yuan · 10th month, 15th · Water Official averts disaster",
        "l_head": "Folk religion", "l_name": "Heaven Official", "l_sub1": "Tianguan of the Upper Yuan",
        "l_sub2": "a.k.a. Ziwei Dadi", "l_foot": "a god of Daoist and folk worship",
        "r_head": "Ancient star map", "r_name": "Ziwei Enclosure", "r_sub1": "the sky region around the north pole",
        "r_sub2": "8 + 7 wall stars", "r_foot": "Book of Jin: \"seat of the Great Emperor\"",
        "same": "same name: Ziwei",
    },
}


def tx(k):
    return TXT[LANG][k]


def box(ax, x0, y0, w, h, ec, lw=2.4, fc="#10172E", alpha=1.0, z=3):
    ax.add_patch(C.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.0,rounding_size=0.05",
                                  fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z))


# ══════════════════════ C-HYX-01 上元天官 ══════════════════════
def c01_shang(ax):
    T(ax, 0.0, 0.50, tx("san"), 34, GREY, w="normal")
    box(ax, -0.80, -0.30, 1.60, 0.68, AMBER, lw=3.2)
    T(ax, 0.0, 0.215, tx("shang") + "　" + tx("shang_d"), 46, AMBER)
    T(ax, 0.0, -0.075, tx("shang_g"), 84 if LANG == "zh" else 40, WHITE)


def c01_rest(ax):
    T(ax, 0.0, -0.46, tx("zhong"), 26 if LANG == "zh" else 17, GREY, w="normal")
    T(ax, 0.0, -0.60, tx("xia"), 26 if LANG == "zh" else 17, GREY, w="normal")


# ══════════════════════ C-HYX-02 同名兩回事 ══════════════════════
def c02_col(ax, x, col, head, name, s1, s2, foot):
    box(ax, x - 0.44, -0.52, 0.88, 1.06, col, lw=2.8)
    T(ax, x, 0.40, head, 28 if LANG == "zh" else 20, GREY, w="normal")
    T(ax, x, 0.17, name, 70 if LANG == "zh" else 30, col)
    T(ax, x, -0.07, s1, 24 if LANG == "zh" else 15, WHITE, w="normal")
    T(ax, x, -0.18, s2, 30 if LANG == "zh" else 17, WHITE)
    T(ax, x, -0.40, foot, 18 if LANG == "zh" else 12, GREY, w="normal")


def c02_left(ax):
    c02_col(ax, -0.48, AMBER, tx("l_head"), tx("l_name"), tx("l_sub1"), tx("l_sub2"), tx("l_foot"))


def c02_right(ax):
    c02_col(ax, 0.48, PURPLE, tx("r_head"), tx("r_name"), tx("r_sub1"), tx("r_sub2"), tx("r_foot"))
    # 兩欄底下一個括號：只連「同名」——兩邊都帶「紫微」，其他各是各的
    ax.plot([-0.48, -0.48, -0.25], [-0.55, -0.66, -0.66], c=WHITE, lw=1.8, alpha=.7, zorder=6)
    ax.plot([0.25, 0.48, 0.48], [-0.66, -0.66, -0.55], c=WHITE, lw=1.8, alpha=.7, zorder=6)
    T(ax, 0.0, -0.66, tx("same"), 30 if LANG == "zh" else 20, WHITE)


def main():
    global LANG
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(OUT, exist_ok=True)
    C.emit("", [("上元", c01_shang), ("三元", c01_rest)], title="C-HYX-01_上元天官")
    C.emit("", [("天官", c02_left), ("紫微垣", c02_right)], title="C-HYX-02_同名兩回事")


if __name__ == "__main__":
    main()
