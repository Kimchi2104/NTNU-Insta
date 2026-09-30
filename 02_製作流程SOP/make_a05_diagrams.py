# -*- coding: utf-8 -*-
"""A-05 日本｜概念示意圖（星圖以外的三件事）

星圖引擎畫不出來、但逐字稿要講的三件事，用 C 系列概念圖引擎補：
  1. 六連星 すばる     鏡頭 01／12／13：昴星團六顆真實位置＋「統ばる＝束成一把」
  2. キトラ四個圈      鏡頭 03／05：內規・赤道・外規・黃道的實測直徑，
                       以及兩個圈給出差七度的緯度 → 圖是憑感覺畫的
  3. 二十八宿和名一覽  9:16 輪播圖卡：28 宿 × 和名 × 可信度

版權提醒：**本檔不繪製任何企業商標。** 逐字稿提到的汽車廠徽由美宣另尋
授權圖像，或整段只用星圖表現；C-A05-01 畫的是昴星團本身。

輸出：透明分層 PNG（2052px 方形）＋黑底預覽＋9:16 輪播圖卡
執行：python3 make_a05_diagrams.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import (AMBER, BLUE, WHITE, GREEN, PURPLE, MW, BG,
                           newfig, newcard, save, T, arrow, emit)
from matplotlib.patches import Circle, Arc, FancyBboxPatch
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-05_日本")
C.set_base(OUT)
S = G.load_stars(BASE)

R_RIM_DEG = 180.0 / math.pi          # 只用來標註；本檔為示意圖

# ══════════════════════════════════════════════════════════════════
# C-A05-01　六連星 すばる
#   昴星團九顆亮星的真實相對位置（以 Alcyone 為原點，單位：角分）
# ══════════════════════════════════════════════════════════════════
PLE = [
    (17702, "Alcyone",  "昴宿六", 2.87, "すばる的中心"),
    (17573, "Maia",     "昴宿四", 3.87, ""),
    (17499, "Electra",  "昴宿一", 3.70, ""),
    (17847, "Atlas",    "昴宿七", 3.62, ""),
    (17608, "Merope",   "昴宿五", 4.14, ""),
    (17531, "Taygeta",  "昴宿二", 4.30, ""),
    (17851, "Pleione",  "昴宿增十六", 5.05, ""),
    (17579, "Celaeno",  "昴宿增九", 5.44, ""),
    (17608, "", "", 99, ""),          # 佔位，過濾掉
]


def _ple_xy():
    """以星團質心為原點、自動縮放到半徑 0.62 的切平面座標（東在左＝仰望視角）"""
    rows = []
    seen = set()
    for hip, en, zh, v, note in PLE:
        if hip not in S or v > 6 or hip in seen:
            continue
        seen.add(hip)
        rows.append((S[hip][0], S[hip][1], en, zh, v))
    ra0 = sum(r[0] for r in rows) / len(rows)
    dec0 = sum(r[1] for r in rows) / len(rows)
    raw = [(-(ra - ra0) * math.cos(math.radians(dec0)) * 60.0,
            (dec - dec0) * 60.0, en, zh, v) for ra, dec, en, zh, v in rows]
    rmax = max(math.hypot(x, y) for x, y, *_ in raw)
    k = 0.62 / rmax
    return [(x * k, y * k, en, zh, v) for x, y, en, zh, v in raw]


def ple_stars(ax):
    for x, y, en, zh, v in _ple_xy():
        r = max(0.016, (6.6 - v) ** 1.55 * 0.0105)
        ax.add_patch(Circle((x, y), r * 3.0, fc=WHITE, ec="none", alpha=.15,
                            zorder=3))
        ax.add_patch(Circle((x, y), r, fc=WHITE, ec="none", zorder=4))


def ple_bundle(ax):
    """「統ばる＝把散的束成一把」：繞質心一圈把星串起來"""
    pts = sorted(_ple_xy(), key=lambda p: math.atan2(p[1], p[0]))
    xy = [(p[0], p[1]) for p in pts]
    xy.append(xy[0])
    ax.plot([p[0] for p in xy], [p[1] for p in xy], c=AMBER, lw=2.2,
            alpha=.85, zorder=5, solid_capstyle="round",
            solid_joinstyle="round")
    T(ax, 0.0, -0.85, "統（す）ばる＝把散的東西束成一把", 28, AMBER)
    T(ax, 0.0, -0.94, "《和名類聚抄》（934）「昴星…和名須波流」", 19, MW)


def ple_labels(ax):
    """標籤沿質心→星的方向往外推；和已放好的標籤重疊就改試別的角度／推距
    （昴宿二、昴宿四方位角幾乎一樣，只靠推距錯開會疊在一起）"""
    pts = sorted(_ple_xy(), key=lambda p: math.atan2(p[1], p[0]))
    boxes = [(x, y, r + 0.012, r + 0.012)       # 星點本身也是障礙物（實心圓的外接框）
             for x, y, *_, v in pts
             for r in [max(0.016, (6.6 - v) ** 1.55 * 0.0105)]]

    def hit(cx, cy, hw, hh):
        if abs(cx) + hw > 0.98 or cy + hh > 0.80 or cy - hh < -0.74:
            return True
        return any(abs(cx - bx) < hw + bw and abs(cy - by) < hh + bh
                   for bx, by, bw, bh in boxes)

    for x, y, en, zh, v in pts:
        d = math.hypot(x, y) or 1e-6
        a0 = math.atan2(y, x)
        hw, hh = max(len(zh) * 0.042, len(en) * 0.022) + 0.02, 0.085
        for dd in (0.17, 0.26, 0.36):
            for da in (0, 25, -25, 50, -50, 80, -80):
                a = a0 + math.radians(da)
                lx, ly = x + math.cos(a) * dd, y + math.sin(a) * dd
                if not hit(lx, ly - 0.005, hw, hh):
                    break
            else:
                continue
            break
        boxes.append((lx, ly - 0.005, hw, hh))
        ux, uy = math.cos(a), math.sin(a)
        T(ax, lx, ly + 0.032, zh, 20, WHITE)
        T(ax, lx, ly - 0.042, en, 15, MW)
        ax.plot([x + ux * 0.055, x + ux * (dd - 0.06)],
                [y + uy * 0.055, y + uy * (dd - 0.06)], c=MW, lw=.9,
                alpha=.5, zorder=2)
    T(ax, 0.0, 0.93, "六連星（むつらぼし）", 34, WHITE)
    T(ax, 0.0, 0.855, "昴星團・肉眼可見六到七顆", 20, MW)


def ple_dialect(ax):
    """方言分布：同一群星，日本各地叫法不同"""
    rows = [("すばる", "近畿", AMBER),
            ("六連星 むつらぼし", "靜岡〜東北", BLUE),
            ("羽子板星 はごいたぼし", "九州〜關東", GREEN),
            ("一升星 いっしょうぼし", "靜岡〜信越", PURPLE),
            ("ムリカブシ", "沖繩八重山", MW)]
    y = 0.62
    for name, area, c in rows:
        T(ax, -0.90, y, name, 22, c, ha="left")
        T(ax, 0.90, y, area, 20, MW, ha="right")
        ax.plot([-0.90, 0.90], [y - 0.055, y - 0.055], c=c, lw=.8, alpha=.3)
        y -= 0.15


# ══════════════════════════════════════════════════════════════════
# C-A05-02　キトラ古墳天文図的四個圈
#   奈文研實測直徑：內規 16.8／赤道 40.3／外規 60.6／黃道 40.5 cm
#   規則：內規:赤道:外規 = φ : 90 : (180−φ)
# ══════════════════════════════════════════════════════════════════
D_IN, D_EQ, D_OUT, D_ECL = 16.8, 40.3, 60.6, 40.5
PHI_IN = D_IN / D_EQ * 90.0                    # 37.6°
PHI_OUT = 180.0 - D_OUT / D_EQ * 90.0          # 44.3°
SC = 0.62 / (D_OUT / 2)                        # 把外規畫到半徑 0.62（下方留給算式框）


def kitora_circles(ax):
    for d, c, lw, ls, lab in ((D_OUT, AMBER, 2.4, "-", "外規"),
                              (D_EQ, WHITE, 2.0, "-", "赤道"),
                              (D_IN, BLUE, 2.2, "-", "內規")):
        ax.add_patch(Circle((0, 0), d / 2 * SC, fill=False, ec=c, lw=lw,
                            ls=ls, zorder=4))
    # 黃道：直徑幾與赤道同，圓心偏離（キトラ把它畫錯了邊，此處只示意偏心）
    ax.add_patch(Circle((-0.075, 0.075), D_ECL / 2 * SC, fill=False, ec=GREEN,
                        lw=1.8, ls=(0, (7, 5)), zorder=4))
    ax.plot([0], [0], marker="+", ms=16, mew=2.0, c=WHITE, zorder=6)


def kitora_dims(ax):
    """三條半徑線各走不同方位角，標註不互相壓"""
    for d, c, lab, ang in ((D_OUT, AMBER, f"外規　徑 {D_OUT} cm", 38),
                           (D_EQ, WHITE, f"赤道　徑 {D_EQ} cm", -20),
                           (D_IN, BLUE, f"內規　徑 {D_IN} cm", -125)):
        r = d / 2 * SC
        a = math.radians(ang)
        ax.plot([0, r * math.cos(a)], [0, r * math.sin(a)], c=c, lw=1.2,
                alpha=.55, zorder=3)
        ax.plot([r * math.cos(a)], [r * math.sin(a)], marker="o", ms=5, c=c,
                zorder=5)
        left = math.cos(a) < 0                   # 左半邊的標註往左長，不壓到右邊的線
        T(ax, r * math.cos(a) + (-0.03 if left else 0.03),
          r * math.sin(a) + (-0.05 if left else 0.045), lab, 19, c,
          ha="right" if left else "left")
    T(ax, -0.075, 0.075 + D_ECL / 2 * SC + 0.05,
      f"黃道　徑 {D_ECL} cm（キトラ把它畫在錯的一側）", 17, GREEN)


def kitora_math(ax):
    T(ax, 0.0, 0.94, "キトラ古墳天文図　四個圈", 34, WHITE)
    T(ax, 0.0, 0.865, "內規 : 赤道 : 外規 ＝ φ : 90 : (180−φ)　（φ＝觀測緯度）",
      20, MW)
    box = FancyBboxPatch((-0.96, -0.97), 1.92, 0.34,
                         boxstyle="round,pad=0.015", fc="#12182C", ec=AMBER,
                         lw=1.4, zorder=8)
    ax.add_patch(box)
    T(ax, -0.90, -0.70, f"由內規：{D_IN}/{D_EQ}×90 ＝ {PHI_IN:.1f}°",
      22, BLUE, ha="left", z=10)
    T(ax, -0.90, -0.815,
      f"由外規：180 − {D_OUT}/{D_EQ}×90 ＝ {PHI_OUT:.1f}°",
      22, AMBER, ha="left", z=10)
    T(ax, -0.90, -0.925,
      f"兩個圈差 {PHI_OUT - PHI_IN:.1f} 度 → 不可能同時對，圈是憑感覺畫的",
      20, WHITE, ha="left", z=10)


def kitora_debate(ax):
    rows = [("宮島一彥", "37–38°N・平壤・前 65 年", BLUE),
            ("相馬　充", "33.9±0.7°N・長安／洛陽・後 300±90 年", AMBER),
            ("奈良文化財研究所", "圖的精度不足，兩邊都量不出來", WHITE)]
    y = 0.56
    for who, what, c in rows:
        T(ax, -0.92, y, who, 23, c, ha="left")
        T(ax, -0.92, y - 0.09, what, 19, MW, ha="left")
        y -= 0.26


# ══════════════════════════════════════════════════════════════════
# C-A05-03　二十八宿和名一覽（9:16 輪播圖卡）
# ══════════════════════════════════════════════════════════════════
WAMEI = [
    ("15 奎", "とかきぼし", "斗掻き・刮平米斗的棒", "★"),
    ("16 婁", "たたらぼし", "蹈鞴・腳踏煉鐵風箱", "△"),
    ("17 胃", "えきえぼし", "—", "？"),
    ("18 昴", "すばるぼし", "統ばる・束成一把", "★"),
    ("19 畢", "あめふりぼし", "雨降り・下雨（借自漢籍）", "△"),
    ("20 觜", "とろきぼし", "—", "？"),
    ("21 參", "からすきぼし", "唐鋤・一把犁", "★"),
    ("07 箕", "みぼし", "箕・簸箕", "✓"),
    ("04 房", "そいぼし", "添星・依著心宿", "✓"),
    ("05 心", "なかごぼし", "中子・正中的那顆", "✓"),
    ("06 尾", "あしたれぼし", "足垂れ・垂下的腳", "✓"),
    ("09 牛", "いなみぼし", "稲見・看得見稻子的時節", "✓"),
    ("23 鬼", "たまおのぼし", "魂緒の星・繫住魂的繩", "✓"),
    ("27 翼", "たすきぼし", "襷・綁袖子的帶", "△"),
    ("25 星", "ほとおりぼし", "熱り・熱（推測）", "△"),
    ("02 亢", "あみぼし", "網（野尻：意味不明）", "？"),
]
COLOR_OF = {"★": AMBER, "✓": WHITE, "△": BLUE, "？": "#7C8BA8"}


def card_wamei():
    f, ax = newcard()
    T(ax, .5, .965, "二十八宿・和名", 34, WHITE)
    T(ax, .5, .938, "同一片天，日本人叫回自己的話", 18, MW)
    y = .895
    for shu, kana, mean, mark in WAMEI:
        c = COLOR_OF[mark]
        T(ax, .055, y, shu, 19, c, ha="left")
        T(ax, .265, y, kana, 19, c, ha="left")
        T(ax, .545, y, mean, 15, MW, ha="left")
        T(ax, .955, y, mark, 16, c, ha="right")
        y -= .0455
    T(ax, .5, .125, "★ 確有古老根據　✓ 語意通順　△ 推測或借自漢籍　？ 意味不明",
      14, MW)
    T(ax, .5, .092, "這套訓讀是江戶中期學者配的，不是自古的民間星名", 15, AMBER)
    T(ax, .5, .062, "（野尻抱影《日本星名辞典》「二十八宿の江戸訳名」）", 13, MW)
    T(ax, .5, .028, "萬國星空 EP5｜師大天文社", 14, MW)
    save(f, "_概念圖", "C-A05-03_和名一覽_圖卡.png", transparent=False)


def card_kitora():
    f, ax = newcard()
    T(ax, .5, .965, "キトラ古墳天文図", 34, WHITE)
    T(ax, .5, .938, "奈良・明日香村　七世紀末", 18, MW)
    rows = [("星點", "360 顆以上・金箔徑約 6 mm"),
            ("星官", "74 個・朱線相連"),
            ("圓", "內規／赤道／外規／黃道"),
            ("二十八宿", "有（可量測 25 宿的距星）"),
            ("三垣", "部分（紫微・太微・天市的蕃）"),
            ("北斗", "有"),
            ("日月", "東＝金箔日像／西＝銀箔月像"),
            ("銀河", "無"),
            ("赤經線", "無"),
            ("發現", "1983 玄武／1998 天文図／2001 朱雀"),
            ("揭取", "2004–2010・共 1,143 片"),
            ("国宝", "2019.07.23（五面）")]
    y = .865
    for k, v in rows:
        T(ax, .06, y, k, 19, AMBER, ha="left")
        T(ax, .40, y, v, 16, WHITE, ha="left")
        y -= .052
    T(ax, .5, .215, "「現存最古」要加限定詞：", 18, AMBER)
    T(ax, .5, .183, "具備那四個圈的完整中國式圓形星圖中，現存世界最古", 15, WHITE)
    T(ax, .5, .152, "（文化廳作「東亞現存最古之例」）", 14, MW)
    T(ax, .5, .112, "敦煌星圖（約 649–684）比它更早，但不是同一類物件", 14, MW)
    T(ax, .5, .075, "常見錯誤數字：68 星座／277 顆星（皆為舊統計）", 14, "#FF6B6B")
    T(ax, .5, .028, "萬國星空 EP5｜師大天文社", 14, MW)
    save(f, "_概念圖", "C-A05-02_キトラ規格_圖卡.png", transparent=False)


def card_tools():
    f, ax = newcard()
    T(ax, .5, .965, "同一排星，各家的工具", 32, WHITE)
    T(ax, .5, .936, "獵戶腰帶三星（＋小三星）", 18, MW)
    rows = [("日本", "からすきぼし 唐鋤星", "犁"),
            ("布吉（蘇拉威西）", "Bintoéng Rakkalaé", "犁"),
            ("羅馬尼亞", "Rarița", "小犁"),
            ("羅馬尼亞", "Sfredelul mare", "大螺旋鑽"),
            ("白俄羅斯", "Касцы Kastsy", "割草的人"),
            ("西伯利亞", "Kichigi", "打穀的人"),
            ("圖卡諾（亞馬遜）", "Sioyahpu", "錛子的柄"),
            ("薩丁尼亞", "Sos Bacheddos", "手杖"),
            ("日本四國", "桛星 かせぼし", "繞紗的線框"),
            ("阿拉伯", "النظم al-Naẓm", "一串珠"),
            ("因紐特", "Ullaktut", "奔跑的人"),
            ("東加", "Toloa", "野鴨")]
    y = .865
    for area, name, mean in rows:
        T(ax, .06, y, area, 16, MW, ha="left")
        T(ax, .43, y, name, 17, AMBER, ha="left")
        T(ax, .955, y, mean, 17, WHITE, ha="right")
        y -= .054
    T(ax, .5, .175, "沒有人互相抄。", 24, WHITE)
    T(ax, .5, .135, "每一個靠天吃飯的地方，", 20, MW)
    T(ax, .5, .103, "都把那排星星看成自己手裡的那件工具。", 20, MW)
    T(ax, .5, .055, "⚠ 英國 the Plough 是大熊座，不是獵戶腰帶；", 13, "#FF6B6B")
    T(ax, .5, .030, "　中國從未把參宿當犁（中國的犁星是畢宿）", 13, "#FF6B6B")
    save(f, "_概念圖", "C-A05-04_工具的天空_圖卡.png", transparent=False)


if __name__ == "__main__":
    print("── C-A05-01 六連星 すばる ──")
    emit("_概念圖", [("星點", ple_stars), ("束線", ple_bundle),
                    ("標籤", ple_labels)],
         preview_name="預覽", title="C-A05-01_六連星")
    f, ax = newfig(1.0); ple_dialect(ax)
    T(ax, 0.0, 0.86, "同一群星，日本各地的叫法", 30, WHITE)
    save(f, "_概念圖", "C-A05-01_六連星_方言層_透明.png")

    print("── C-A05-02 キトラ四個圈 ──")
    emit("_概念圖", [("圈", kitora_circles), ("尺寸", kitora_dims),
                    ("算式", kitora_math)],
         preview_name="預覽", title="C-A05-02_キトラ四圈")
    f, ax = newfig(1.0); kitora_debate(ax)
    T(ax, 0.0, 0.86, "觀測緯度與年代：三方並陳", 30, WHITE)
    save(f, "_概念圖", "C-A05-02_キトラ四圈_爭議層_透明.png")

    print("── 9:16 輪播圖卡 ──")
    card_wamei(); card_kitora(); card_tools()
    print("\n完成：", os.path.join(OUT, "_概念圖"))
