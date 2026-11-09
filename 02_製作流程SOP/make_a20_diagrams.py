# -*- coding: utf-8 -*-
"""A-20 春節特輯｜朱雀｜概念圖（方形透明分層：Reels 定格頁一頁疊一層；9:16 圖卡＝滿版）
  C-A20-06_前朱鳥後玄武  → 02 鏡（三象層 → 引文層 → 朱雀層）
  C-A20-01_兩個火        → 05 鏡（柳宿層 → 心宿層 → 火正層）
  C-A20-02_一顆蛋        → 07 鏡（河邊層 → 蛋層 → 契層）；08 鏡換燕子層（單獨成頁）
  C-A20-03_紅鳥興周      → 09 鏡（火落屋頂層 → 赤烏層 → 歲在鶉火層）
  C-A20-05_除夕抬頭看    → 12 鏡（9:16 圖卡，可存圖）
  C-A20-04_四象總圖      → 15 鏡（9:16 圖卡，可存圖）
輸出：05_素材/A-20_朱雀/_概念圖/（--lang en → _概念圖/en/；這次只出 zh）

來源（數字與逐字稿 v1「星空對時」一致；圖卡的高度方位由 PyEphem 現算，含大氣折射 1010 hPa、15°C）：
  Stellarium chinese（二十八宿連線）；《禮記・曲禮上》；《左傳・襄公九年》（咮為鶉火，心為大火）；
  《詩經・商頌・玄鳥》、毛傳（玄鳥，鳦也）；《史記・殷本紀》（三人行浴，見玄鳥墮其卵，簡狄取吞之）；
  《史記・周本紀》（有火自上復于下，至于王屋，流為烏，其色赤）；《國語・周語下》（昔武王伐殷，歲在鶉火）；
  《晉書・天文志》十二次度數。人物、鳥、房子一律自繪示意（不用古畫或網路圖）。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c_series_base as C
from c_series_base import AMBER, BLUE, WHITE, GREEN, PURPLE, T
from matplotlib.patches import Rectangle, Polygon, Ellipse, Circle
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "05_素材/A-20_朱雀/_概念圖")
C.set_base(OUT)
RED, GREY, ORANGE, DARK = "#FF6B6B", "#7C8BA8", "#FF9A4A", "#2B3050"
TPE = ("25.0330", "121.5654")
LANG = "zh"
TXT = {
    "zh": {
        # C-A20-06／04 四象
        "q_li": "「前朱鳥而後玄武，左青龍而右白虎」", "q_li_src": "《禮記・曲禮上》：軍隊出發的陣式",
        "front": "前・南方朱雀", "back": "後・北方玄武", "left": "左・東方青龍", "right": "右・西方白虎",
        "pole": "北天極", "c04_title": "四象總圖", "c04_sub": "二十八宿・面向南方抬頭看（下南上北、左東右西）",
        "c04_eps": "青龍 A-01　玄武 A-03　白虎 A-12　朱雀 A-20",
        "c04_note": "四象各管七宿；東西南北四方各一隻神獸", "save": "可存圖",
        # C-A20-01 兩個火
        "c01_title": "兩個「火」", "c01_sub": "《左傳・襄公九年》",
        "liu": "柳宿", "chunhuo": "鶉火", "zhou": "咮＝鳥嘴＝柳宿", "zhou2": "朱雀的嘴",
        "xin": "心宿", "dahuo": "大火", "xin2": "青龍的心（A-01）", "xin3": "心宿二",
        "huozheng": "火正（上古管火的官）", "q_zuo": "「咮為鶉火，心為大火」",
        "c01_note": "看兩顆星隨季節出沒，決定一年什麼時候用火",
        "c01_src": "杜預注：火正死後配享於心星或咮星",
        # C-A20-02 一顆蛋
        "c02_title": "一顆蛋", "c02_sub": "《史記・殷本紀》",
        "jiandi": "簡狄", "bath": "三人去洗澡（三人行浴）", "egg": "玄鳥墮其卵，簡狄取吞之",
        "qi": "契", "qi_zy": "（ㄒㄧㄝˋ）", "qi2": "商朝的祖先", "q_shi": "「天命玄鳥，降而生商」",
        "q_shi_src": "《詩經・商頌・玄鳥》",
        "c02b_title": "下這顆蛋的不是朱雀", "c02b_sub": "「玄」＝黑色",
        "yan": "玄鳥＝鳦（燕子）", "yan2": "毛傳、鄭箋；《禮記・月令》仲春「玄鳥至」",
        "shang": "商朝看的星：大火（心宿二）", "shang2": "「商主大火」——《左傳・襄公九年》",
        # C-A20-03 紅鳥興周
        "c03_title": "紅鳥興周", "c03_sub": "《史記・周本紀》《國語・周語下》",
        "q_fire": "「有火自上復于下，至于王屋」", "fire2": "武王渡過黃河之後",
        "q_wu": "「流為烏，其色赤」", "wu2": "火變成一隻紅色的烏鴉",
        "q_guo": "「昔武王伐殷，歲在鶉火」", "guo2": "歲＝歲星（木星）；鶉火＝周的分野",
        "shou": "鶉首", "huo": "鶉火", "wei": "鶉尾", "sui": "歲星",
        "c03_note": "今日軌道回推：前 1046 年 1 月，木星在星宿（鶉火）",
        "c03_src": "前 1046 年＝夏商周斷代工程推定的克商年；這段記載是否當年實錄，學界看法不一",
        # C-A20-05 除夕抬頭看
        "c05_title": "除夕抬頭看：歲在鶉火", "c05_date": "2027/2/5（五・除夕）台北",
        "p1": "20:00　往東看", "p2": "00:00　往南看（守歲）",
        "E": "東", "ENE": "東北東", "ESE": "東南東", "S": "南", "SE": "東南", "SW": "西南",
        "jup": "木星", "reg": "軒轅十四", "mars": "火星", "liu1": "柳宿一", "xing1": "星宿一", "zhang1": "張宿一",
        "m44": "積尸氣（M44）",
        "n1": "朔在 2/6 23:56：整夜沒有月亮", "n2": "木星 2/11 衝、火星 2/19 衝：整夜都看得到",
        "n3": "柳宿 23:30、星宿 00:20、張宿 00:44 過正南",
        "c05_src": "PyEphem 自算（含大氣折射）；木星 −2.55 等（Mallama & Hilton 2018）",
    },
    "en": {
        "q_li": "\"Vermilion Bird in front, Black Tortoise behind,\nAzure Dragon on the left, White Tiger on the right\"",
        "q_li_src": "Book of Rites, Quli I: an army on the march",
        "front": "Front · Vermilion Bird (S)", "back": "Back · Black Tortoise (N)",
        "left": "Left · Azure Dragon (E)", "right": "Right · White Tiger (W)",
        "pole": "N pole", "c04_title": "The Four Symbols",
        "c04_sub": "28 lunar mansions · facing south, looking up (S down, E left)",
        "c04_eps": "Dragon A-01　Tortoise A-03　Tiger A-12　Bird A-20",
        "c04_note": "Seven mansions each; one guardian beast per direction", "save": "Save me",
        "c01_title": "Two \"Fires\"", "c01_sub": "Zuozhuan, Duke Xiang 9",
        "liu": "Willow", "chunhuo": "Quail Fire", "zhou": "zhou = beak = Willow", "zhou2": "the bird's beak",
        "xin": "Heart", "dahuo": "Great Fire", "xin2": "heart of the Dragon (A-01)", "xin3": "Antares",
        "huozheng": "Fire Officer (ancient)", "q_zuo": "\"The beak is Quail Fire, the Heart is Great Fire\"",
        "c01_note": "Their seasonal risings told people when to start and stop fires",
        "c01_src": "Du Yu: fire officers were honoured with these two stars after death",
        "c02_title": "One egg", "c02_sub": "Records of the Grand Historian: Yin Annals",
        "jiandi": "Jiandi", "bath": "three women go bathing", "egg": "a dark bird dropped its egg; Jiandi swallowed it",
        "qi": "Xie", "qi_zy": "(契)", "qi2": "ancestor of Shang", "q_shi": "\"Heaven bade the dark bird descend and give birth to Shang\"",
        "q_shi_src": "Book of Songs, Hymns of Shang",
        "c02b_title": "Not laid by the Vermilion Bird", "c02b_sub": "xuan = black",
        "yan": "dark bird = swallow", "yan2": "Mao and Zheng commentaries; Yueling: swallows return in mid-spring",
        "shang": "Shang's star: Great Fire (Antares)", "shang2": "\"Shang took the Great Fire\" — Zuozhuan",
        "c03_title": "A red bird for Zhou", "c03_sub": "Zhou Annals; Discourses of the States",
        "q_fire": "\"A fire came down onto the king's house\"", "fire2": "after King Wu crossed the Yellow River",
        "q_wu": "\"It became a crow, red in colour\"", "wu2": "the fire turned into a red crow",
        "q_guo": "\"When King Wu attacked Yin, Jupiter was in Quail Fire\"",
        "guo2": "sui = Jupiter; Quail Fire = Zhou's field",
        "shou": "Quail Head", "huo": "Quail Fire", "wei": "Quail Tail", "sui": "Jupiter",
        "c03_note": "Modern orbits: in Jan 1046 BCE Jupiter was in the Star mansion (Quail Fire)",
        "c03_src": "1046 BCE = Xia–Shang–Zhou Chronology Project date; whether the record is first-hand is debated",
        "c05_title": "New Year's Eve: Jupiter in Quail Fire", "c05_date": "Fri 5 Feb 2027 · Taipei",
        "p1": "20:00　look east", "p2": "00:00　look south",
        "E": "E", "ENE": "ENE", "ESE": "ESE", "S": "S", "SE": "SE", "SW": "SW",
        "jup": "Jupiter", "reg": "Regulus", "mars": "Mars", "liu1": "δ Hya", "xing1": "Alphard", "zhang1": "υ¹ Hya",
        "m44": "Beehive (M44)",
        "n1": "New moon 6 Feb 23:56: no moonlight all night", "n2": "Jupiter opposition 11 Feb, Mars 19 Feb",
        "n3": "Willow 23:30, Star 00:20, Extended Net 00:44 cross the meridian",
        "c05_src": "PyEphem (with refraction); Jupiter −2.55 (Mallama & Hilton 2018)",
    },
}


def tx(k):
    return TXT[LANG][k]


S = None
MANSIONS = [  # (Stellarium chinese id, 宿名, 象)
    ("009", "角", "龍"), ("011", "亢", "龍"), ("004", "氐", "龍"), ("006", "房", "龍"), ("026", "心", "龍"),
    ("024", "尾", "龍"), ("008", "箕", "龍"),
    ("005", "斗", "玄"), ("016", "牛", "玄"), ("017", "女", "玄"), ("028", "虛", "玄"), ("023", "危", "玄"),
    ("018", "室", "玄"), ("002", "壁", "玄"),
    ("012", "奎", "虎"), ("014", "婁", "虎"), ("025", "胃", "虎"), ("015", "昴", "虎"), ("001", "畢", "虎"),
    ("034", "觜", "虎"), ("003", "參", "虎"),
    ("010", "井", "朱"), ("007", "鬼", "朱"), ("013", "柳", "朱"), ("027", "星", "朱"), ("030", "張", "朱"),
    ("029", "翼", "朱"), ("031", "軫", "朱")]
XCOL = {"龍": GREEN, "玄": BLUE, "虎": WHITE, "朱": RED}
CN = None
NAME_ADJ = {"觜": (-0.15, 0.10), "參": (0.02, 0.0), "鬼": (0.05, 0.02), "心": (-0.02, 0.0)}


def cn_lines():
    import json
    p = os.path.join(BASE, "07_資料來源/Stellarium/stellarium-skycultures-master/chinese/index.json")
    d = json.load(open(p, encoding="utf-8"))
    return {c["id"].split()[-1]: [[h for h in l if isinstance(h, int)] for l in c["lines"]] for c in d["constellations"]}


def box(ax, x, y, w, h, col, a=1.0):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.012,rounding_size=0.03",
                                fc=C.BG, ec=col, lw=1.6, alpha=a, zorder=3))


# ══════════════════════ 四象極座標圖（C-A20-06 分層、C-A20-04 圖卡） ══════════════════════
DEC_MIN, RA_FRONT = -50.0, 140.0       # 正下方（前・南）＝RA 140（朱雀中段）


def polar(ra, dec, R):
    r = R * (90.0 - dec) / (90.0 - DEC_MIN)
    th = math.radians(-90.0 - (ra - RA_FRONT))      # 東（赤經大）在左
    return r * math.cos(th), r * math.sin(th)


def centroid(hips):
    hs = [h for h in hips if h in S]
    ra = math.degrees(math.atan2(sum(math.sin(math.radians(S[h][0])) for h in hs),
                                 sum(math.cos(math.radians(S[h][0])) for h in hs))) % 360
    return ra, sum(S[h][1] for h in hs) / len(hs)


def draw_xiang(ax, which, R=0.60, oy=-0.04, names=True, sz=17, big=26, ring=False):
    if ring:                                 # 天赤道（虛線）＋北天極
        xs, ys = zip(*[polar(a, 0.0, R) for a in range(0, 361, 3)])
        ax.plot(xs, [y + oy for y in ys], c=WHITE, lw=1.0, alpha=.25, ls=(0, (4, 4)))
        ax.scatter([0], [oy], s=40, c=WHITE, alpha=.6, lw=0)
        T(ax, 0, oy - 0.045, tx("pole"), 12, GREY, w="normal")
    for k, nm, x in MANSIONS:
        if x not in which:
            continue
        col = XCOL[x]
        segs = CN[k]
        hs = sorted({h for s in segs for h in s if h in S})
        for s in segs:
            pts = [polar(*S[h][:2], R) for h in s if h in S]
            ax.plot([p[0] for p in pts], [p[1] + oy for p in pts], c=col, lw=2.0, alpha=.9, zorder=4)
        for h in hs:
            p = polar(*S[h][:2], R)
            ax.scatter([p[0]], [p[1] + oy], s=max(4, max(0.3, 6.0 - S[h][2]) ** 1.9 * 3.2), c=WHITE, lw=0, zorder=5)
        if names:
            ra, dec = centroid(hs)
            r0 = R * (90.0 - dec) / (90.0 - DEC_MIN)
            p = polar(ra, dec, R)
            k_out = (r0 + 0.075) / max(r0, 1e-6)
            ax_, ay_ = NAME_ADJ.get(nm, (0.0, 0.0))
            T(ax, p[0] * k_out + ax_ * R / 0.6, p[1] * k_out + oy + ay_ * R / 0.6, nm, sz, col)
    lab = {"朱": ("front", 0.0, -R - 0.15), "玄": ("back", 0.0, R + 0.11),
           "龍": ("left", -R - 0.13, 0.0), "虎": ("right", R + 0.13, 0.0)}
    for x in which:
        key, lx, ly = lab[x]
        s_ = tx(key)
        if x in "龍虎":
            s_ = s_.replace("・", "\n") if LANG == "zh" else s_.replace(" · ", "\n")
        ax.text(lx, ly + oy, s_, fontproperties=C.FP, fontsize=big, color=XCOL[x], ha="center", va="center",
                weight="bold", linespacing=1.15, zorder=6)


def c06_three(ax):
    draw_xiang(ax, "龍玄虎", ring=True)


def c06_quote(ax):
    T(ax, 0, 0.90, tx("q_li"), 24, AMBER)
    T(ax, 0, 0.82, tx("q_li_src"), 14, GREY, w="normal")


def c06_bird(ax):
    draw_xiang(ax, "朱")


def c04_card(ax):
    f = ax.figure
    T(ax, 0.5, 0.945, tx("c04_title"), 28)
    T(ax, 0.5, 0.905, tx("c04_sub"), 12, GREY, w="normal")
    sub = f.add_axes([0.0, 0.30, 1.0, 1.0 * 6.075 / 10.8])
    sub.set_xlim(-1, 1); sub.set_ylim(-1, 1); sub.set_aspect("equal"); sub.axis("off"); sub.patch.set_alpha(0)
    draw_xiang(sub, "龍玄虎朱", R=0.56, oy=0.0, sz=13, big=17, ring=True)
    T(ax, 0.5, 0.255, tx("q_li"), 15, AMBER)
    T(ax, 0.5, 0.222, tx("q_li_src"), 10.5, GREY, w="normal")
    T(ax, 0.5, 0.17, tx("c04_note"), 12.5, WHITE, w="normal")
    T(ax, 0.5, 0.135, tx("c04_eps"), 12.5, WHITE, w="normal")
    box(ax, 0.86, 0.06, 0.16, 0.035, AMBER)
    T(ax, 0.86, 0.06, tx("save"), 11, AMBER)
    T(ax, 0.42, 0.06, "#萬國星空　#師大天文社", 13, WHITE, w="normal")


# ══════════════════════ C-A20-01 兩個火 ══════════════════════
def local(hips, cx, cy, s):
    ra0, dec0 = centroid(hips)
    c = math.cos(math.radians(dec0))
    out = []
    for h in hips:
        ra, dec, v = S[h]
        dra = ((ra - ra0 + 180) % 360) - 180
        out.append((cx - dra * c * s, cy + (dec - dec0) * s, v))
    return out


def star_group(ax, hips, segs, cx, cy, s, col, big=None):
    pts = dict(zip(hips, local(hips, cx, cy, s)))
    for sg in segs:
        q = [pts[h] for h in sg if h in pts]
        ax.plot([p[0] for p in q], [p[1] for p in q], c=col, lw=2.4, alpha=.9, zorder=3)
    for h, (x, y, v) in pts.items():
        ax.scatter([x], [y], s=max(14, max(0.3, 6.2 - v) ** 2.0 * 9), c=WHITE, lw=0, zorder=4)
    if big:
        x, y, _ = pts[big]
        ax.scatter([x], [y], s=900, c=ORANGE, alpha=.25, lw=0, zorder=3)
        ax.scatter([x], [y], s=230, c=ORANGE, lw=0, zorder=5)


def c01_liu(ax):
    T(ax, 0, 0.88, tx("c01_title"), 32)
    T(ax, 0, 0.79, tx("c01_sub"), 15, GREY, w="normal")
    segs = CN["013"]
    hips = sorted({h for s in segs for h in s if h in S})
    star_group(ax, hips, segs, -0.48, 0.12, 0.042, RED)
    T(ax, -0.48, -0.16, tx("liu"), 20, RED)
    T(ax, -0.48, -0.30, tx("chunhuo"), 36, RED)
    T(ax, -0.48, -0.43, tx("zhou"), 16, WHITE, w="normal")
    T(ax, -0.48, -0.52, tx("zhou2"), 14, GREY, w="normal")


def c01_xin(ax):
    segs = CN["026"]
    hips = sorted({h for s in segs for h in s if h in S})
    star_group(ax, hips, segs, 0.48, 0.12, 0.075, GREEN, big=80763)
    T(ax, 0.66, 0.12, tx("xin3"), 13, ORANGE, w="normal")
    T(ax, 0.48, -0.16, tx("xin"), 20, GREEN)
    T(ax, 0.48, -0.30, tx("dahuo"), 36, GREEN)
    T(ax, 0.48, -0.43, tx("xin2"), 16, WHITE, w="normal")


def c01_zheng(ax):
    T(ax, 0, 0.56, tx("huozheng"), 18, AMBER)
    C.arrow(ax, (-0.40, 0.36), (-0.12, 0.51), c=AMBER, lw=2.0, alpha=.8)
    C.arrow(ax, (0.40, 0.36), (0.12, 0.51), c=AMBER, lw=2.0, alpha=.8)
    T(ax, 0, -0.66, tx("q_zuo"), 26, AMBER)
    T(ax, 0, -0.76, tx("c01_note"), 15, WHITE, w="normal")
    T(ax, 0, -0.85, tx("c01_src"), 12, GREY, w="normal")


# ══════════════════════ 鳥的剪影（自繪） ══════════════════════
def bird_shape(kind, x0, y0, s):
    """仰望飛鳥的剪影（頭朝上、雙翼平展、尾朝下）：swallow＝剪刀尾；crow＝扇形尾；dark＝遠處小黑鳥（剪刀尾）"""
    half = [(0.0, 0.44), (-0.05, 0.40), (-0.07, 0.29), (-0.22, 0.37), (-0.40, 0.37), (-0.60, 0.27),
            (-0.82, 0.10), (-0.63, 0.15), (-0.46, 0.19), (-0.28, 0.15), (-0.10, 0.06), (-0.08, -0.08)]
    if kind == "crow":
        half += [(-0.15, -0.36), (-0.09, -0.44), (0.0, -0.46)]
    else:
        half += [(-0.17, -0.55), (-0.10, -0.55), (0.0, -0.22)]
    full = half + [(-x, y) for x, y in reversed(half[1:-1])]
    return [(x0 + x * s, y0 + y * s) for x, y in full]


def c02_river(ax):
    T(ax, 0, 0.88, tx("c02_title"), 32)
    T(ax, 0, 0.79, tx("c02_sub"), 15, GREY, w="normal")
    C.water(ax, y=-0.40, x0=-0.95, x1=0.05, c=BLUE, rows=3)
    for x in (-0.78, -0.52, -0.26):
        C.human_figure(ax, x, -0.12, s=0.62, c=WHITE if x != -0.52 else AMBER, alpha=.95)
    T(ax, -0.56, 0.20, tx("jiandi"), 20, AMBER)
    T(ax, -0.45, -0.62, tx("bath"), 16, WHITE, w="normal")


def c02_egg(ax):
    ax.add_patch(Polygon(bird_shape("dark", 0.0, 0.50, 0.26), closed=True, fc=DARK, ec=WHITE, lw=1.6, zorder=4))
    xs = [-0.03 - 0.39 * t for t in [i / 30 for i in range(31)]]
    ys = [0.40 - 0.31 * t ** 1.6 for t in [i / 30 for i in range(31)]]
    ax.plot(xs, ys, c=WHITE, lw=1.6, alpha=.6, ls=(0, (3, 3)))
    ax.add_patch(Ellipse((-0.42, 0.06), 0.06, 0.08, fc="#F4EFE2", ec="none", zorder=5))
    T(ax, 0.36, 0.30, tx("egg"), 15, WHITE, w="normal")


def c02_qi(ax):
    C.arrow(ax, (0.38, 0.06), (-0.10, 0.02), c=AMBER, lw=2.4, alpha=.8)
    T(ax, 0.58, 0.10, tx("qi"), 64, AMBER)
    T(ax, 0.58, -0.08, tx("qi_zy"), 15, GREY, w="normal")
    T(ax, 0.58, -0.19, tx("qi2"), 18, WHITE, w="normal")
    T(ax, 0, -0.76, tx("q_shi"), 26, AMBER)
    T(ax, 0, -0.86, tx("q_shi_src"), 13, GREY, w="normal")


def c02_swallow(ax):
    T(ax, 0, 0.88, tx("c02b_title"), 30)
    T(ax, 0, 0.79, tx("c02b_sub"), 18, AMBER)
    ax.add_patch(Polygon(bird_shape("swallow", 0.0, 0.26, 0.70), closed=True, fc=DARK, ec=WHITE, lw=2.0, zorder=4))
    T(ax, 0, -0.20, tx("yan"), 26, AMBER)
    T(ax, 0, -0.31, tx("yan2"), 13.5, GREY, w="normal")
    segs = CN["026"]
    hips = sorted({h for s in segs for h in s if h in S})
    star_group(ax, hips, segs, 0.0, -0.50, 0.05, GREEN, big=80763)
    T(ax, 0, -0.66, tx("shang"), 20, GREEN)
    T(ax, 0, -0.76, tx("shang2"), 14, WHITE, w="normal")


# ══════════════════════ C-A20-03 紅鳥興周 ══════════════════════
def c03_fire(ax):
    T(ax, 0, 0.88, tx("c03_title"), 32)
    T(ax, 0, 0.79, tx("c03_sub"), 15, GREY, w="normal")
    hx, hy = -0.58, -0.06                                  # 房子
    ax.add_patch(Rectangle((hx - 0.22, hy - 0.28), 0.44, 0.28, fc=C.BG, ec=WHITE, lw=2.0, zorder=3))
    ax.add_patch(Polygon([(hx - 0.32, hy), (hx + 0.32, hy), (hx + 0.20, hy + 0.12), (hx - 0.20, hy + 0.12)],
                         closed=True, fc=C.BG, ec=WHITE, lw=2.0, zorder=4))
    ax.add_patch(Rectangle((hx - 0.05, hy - 0.28), 0.10, 0.16, fc="none", ec=WHITE, lw=1.4, zorder=4))
    for k, a in ((1.0, .18), (0.6, .35), (0.32, .9)):     # 火球＋拖尾
        ax.add_patch(Circle((hx, 0.52), 0.07 * k / 0.32 * 0.32, fc=ORANGE, alpha=a, ec="none", zorder=5))
    for dx in (-0.03, 0.0, 0.03):
        ax.plot([hx + dx, hx + dx * 2], [0.58, 0.70], c=ORANGE, lw=2.0, alpha=.45)
    C.arrow(ax, (hx, 0.12), (hx, 0.44), c=ORANGE, lw=2.0, alpha=.7)
    T(ax, 0.25, 0.56, tx("q_fire"), 19, ORANGE)
    T(ax, 0.25, 0.47, tx("fire2"), 14, WHITE, w="normal")


def c03_crow(ax):
    ax.add_patch(Polygon(bird_shape("crow", -0.12, 0.26, 0.34), closed=True, fc=RED, ec=WHITE, lw=1.4, zorder=6))
    T(ax, 0.32, 0.22, tx("q_wu"), 22, RED)
    T(ax, 0.32, 0.13, tx("wu2"), 14, WHITE, w="normal")


def c03_sui(ax):
    T(ax, 0, -0.24, tx("q_guo"), 22, AMBER)
    T(ax, 0, -0.33, tx("guo2"), 14, WHITE, w="normal")
    y0, h = -0.56, 0.12
    segs = [("wei", -0.85, -0.30, .18), ("huo", -0.30, 0.30, .55), ("shou", 0.30, 0.85, .18)]   # 東在左
    for key, a, b, al in segs:
        ax.add_patch(Rectangle((a, y0 - h / 2), b - a, h, fc=RED, alpha=al, ec=RED, lw=1.2, zorder=3))
        T(ax, (a + b) / 2, y0 - h / 2 - 0.05, tx(key), 15 if key != "huo" else 18, RED if key == "huo" else WHITE)
    ax.scatter([-0.04], [y0], s=260, c=WHITE, lw=0, zorder=5)
    ax.scatter([-0.04], [y0], s=700, c=WHITE, alpha=.2, lw=0, zorder=4)
    T(ax, 0.10, y0, tx("sui"), 14, WHITE, ha="left")
    T(ax, 0, -0.80, tx("c03_note"), 14, WHITE, w="normal")
    T(ax, 0, -0.88, tx("c03_src"), 10.5, GREY, w="normal")


# ══════════════════════ C-A20-05 除夕抬頭看（9:16 圖卡） ══════════════════════
def altaz(target, local_time):
    import ephem
    o = ephem.Observer(); o.lat, o.lon = TPE; o.temp, o.pressure = 15, 1010; o.elevation = 0
    o.date = ephem.Date(ephem.Date(local_time) - 8 * ephem.hour)
    if isinstance(target, str):
        b = getattr(ephem, target)()
    else:
        b = ephem.FixedBody()
        ra, dec = (S[target][:2] if isinstance(target, int) else target)
        b._ra, b._dec = math.radians(ra), math.radians(dec); b._epoch = ephem.J2000
    b.compute(o)
    return math.degrees(b.alt), math.degrees(b.az)


def panel(ax, x0, x1, yb, yt, az0, az1, al1, title, ticks, objs, when):
    def P(alt, az):
        return x0 + (x1 - x0) * (az - az0) / (az1 - az0), yb + (yt - yb) * alt / al1

    def tt(x, y, s, size, col=WHITE, ha="center", w="normal"):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=col, ha=ha, va="center", weight=w)
    tt(x0, yt + 0.022, title, 15, AMBER, ha="left", w="bold")
    ax.plot([x0, x1], [yb, yb], c=WHITE, lw=1.6, alpha=.7)
    ax.add_patch(Rectangle((x0, yb - 0.015), x1 - x0, 0.015, fc="#1B2240", ec="none"))
    for az, k in ticks:
        tt(P(0, az)[0], yb - 0.03, tx(k), 12, GREY)
    step = 10 if al1 <= 50 else 20
    for alt in range(step, int(al1) + 1, step):
        y = P(alt, az0)[1]
        ax.plot([x0, x1], [y, y], c=WHITE, lw=0.6, alpha=.12)
        tt(x0 - 0.008, y, f"{alt}°", 8.5, GREY, ha="right")
    out = {}
    for key, tgt, col, s_, dx, dy in objs:
        al, az = altaz(tgt, when)
        out[key] = (al, az)
        x, y = P(al, az)
        ax.scatter([x], [y], s=s_, c=col, lw=0, zorder=6)
        tt(x + dx, y + dy, f"{tx(key)} {al:.0f}°", 12, col, ha="left" if dx > 0 else ("right" if dx < 0 else "center"))
    return out


def c05_card(ax):
    def tt(x, y, s, size, col=WHITE, ha="center", w="normal"):
        ax.text(x, y, s, fontproperties=C.FP, fontsize=size, color=col, ha=ha, va="center", weight=w)
    tt(0.5, 0.950, tx("c05_title"), 25, w="bold")
    tt(0.5, 0.913, tx("c05_date"), 13, GREY)
    a = panel(ax, 0.10, 0.92, 0.62, 0.86, 60.0, 120.0, 45.0, tx("p1"),
              [(67.5, "ENE"), (90.0, "E"), (112.5, "ESE")],
              [("jup", "Jupiter", WHITE, 160, 0.03, 0.0), ("reg", 49669, WHITE, 60, -0.03, 0.0),
               ("mars", "Mars", RED, 90, 0.03, 0.0), ("m44", (130.10, 19.67), GREY, 30, -0.03, 0.0),
               ("liu1", 42313, RED, 35, -0.03, 0.0), ("xing1", 46390, RED, 50, -0.03, 0.0),
               ("zhang1", 48356, RED, 35, -0.03, -0.012)], "2027/2/5 20:00")
    b = panel(ax, 0.10, 0.92, 0.22, 0.54, 105.0, 255.0, 90.0, tx("p2"),
              [(135.0, "SE"), (180.0, "S"), (225.0, "SW")],
              [("jup", "Jupiter", WHITE, 160, 0.03, 0.0), ("mars", "Mars", RED, 90, 0.03, 0.0),
               ("liu1", 42313, RED, 45, -0.03, 0.0), ("xing1", 46390, RED, 60, 0.03, 0.0),
               ("zhang1", 48356, RED, 45, 0.03, 0.0)], "2027/2/6 00:00")
    for i, s_ in enumerate((tx("n1"), tx("n2"), tx("n3"))):
        tt(0.5, 0.155 - 0.033 * i, s_, 12.5, AMBER if i == 0 else WHITE)
    tt(0.5, 0.062, tx("c05_src"), 9.5, GREY)
    tt(0.5, 0.030, "#萬國星空　#師大天文社", 13)
    print("  20:00 東：" + "、".join(f"{k} {v[0]:.1f}°／{v[1]:.1f}°" for k, v in a.items()))
    print("  00:00 南：" + "、".join(f"{k} {v[0]:.1f}°／{v[1]:.1f}°" for k, v in b.items()))


def main():
    global S, LANG, CN
    S = dict(G.load_stars(BASE))
    CN = cn_lines()
    if "--lang" in sys.argv:
        LANG = sys.argv[sys.argv.index("--lang") + 1]
        C.set_base(os.path.join(OUT, LANG))
    os.makedirs(C._BASE, exist_ok=True)
    C.emit("", [("三象", c06_three), ("引文", c06_quote), ("朱雀", c06_bird)], title="C-A20-06_前朱鳥後玄武")
    C.emit("", [("柳宿", c01_liu), ("心宿", c01_xin), ("火正", c01_zheng)], title="C-A20-01_兩個火")
    C.emit("", [("河邊", c02_river), ("蛋", c02_egg), ("契", c02_qi)], title="C-A20-02_一顆蛋")
    C.emit("", [("燕子", c02_swallow)], preview_name="燕子預覽", title="C-A20-02_一顆蛋")
    C.emit("", [("火落屋頂", c03_fire), ("赤烏", c03_crow), ("歲在鶉火", c03_sui)], title="C-A20-03_紅鳥興周")
    f, ax = C.newcard(dark=True)
    c05_card(ax)
    C.save(f, "", "C-A20-05_除夕抬頭看_圖卡.png", transparent=False)
    f, ax = C.newcard(dark=True)
    c04_card(ax)
    C.save(f, "", "C-A20-04_四象總圖_圖卡.png", transparent=False)


if __name__ == "__main__":
    main()
