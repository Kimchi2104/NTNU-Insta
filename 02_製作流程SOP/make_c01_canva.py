# -*- coding: utf-8 -*-
"""C-01 論天三家｜Canva 逐頁表（C 系列：概念圖定格頁，一頁多疊一層）

輸出：05_素材/C-01_論天三家/_canva/C-01_Canva頁面參數.json、C-01_逐頁製作表.md
每頁：團隊漸層背景＋山（沿用舊頁就保留原本的）＋概念圖圖層（方形 1080×1080 置中）。
  - 方形圖層：left 0、top 420、1080×1080（與 A 系列概念圖不同：C 系列不墊黑框，圖就是主角）
  - 宣夜的氣與眾星：放大到 1920×1920 蓋滿整頁，送到最底層（山的後面），前後兩頁位移做緩慢飄移
  - 9:16 對照表圖卡：滿版 1080×1920
  - 蟻行磨石：磨盤、螞蟻兩層都以畫布中心為圓心，逐頁改旋轉角（負＝逆時針＝左旋），Match & Move 轉動
旁白與秒數同 04_腳本庫/C-01-…-逐字稿-v2.md。
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "C-01"
ROOT = os.path.join(BASE, "05_素材/C-01_論天三家")
OUT = os.path.join(ROOT, "_canva")

SQ = dict(left=0, top=420, width=1080, height=1080)
BIG = dict(left=-420, top=0, width=1920, height=1920)
CARD = dict(left=0, top=0, width=1080, height=1920)


def L(path, box=SQ, rot=0.0, dx=0, dy=0, back=False):
    b = dict(box)
    b["left"] += dx; b["top"] += dy
    return dict(file=path, rotation=rot, back=back, **b)


def gai(n): return f"蓋天說/{n}_透明.png"
def hun(n): return f"渾天說/天球_{n}層_透明.png"
def xy(n): return f"宣夜說/{n}_透明.png"
def trio(n): return f"_三家並置/論天三家_{n}層_透明.png"


TRIO = [trio("題辭"), trio("蓋天"), trio("渾天"), trio("宣夜")]
GAI2 = [gai("蓋天兩版_題辭層")]
SIDE = [gai("側視_題辭層"), gai("側視_天地層")]
QH_C = gai("七衡六間_中心層")
GB = [gai("圭表日影_表層")]
MILL_T = gai("蟻行磨石_題辭層")
HUN = [hun("題辭"), hun("天球")]


def qi(dx=(0, 0, 0), dy=(0, 0, 0)):
    """宣夜三層氣＋眾星：滿版、送到最底層；dx/dy 給每層不同的位移（飄移）"""
    out = [L(xy(f"宣夜_氣_第{k+1}層"), BIG, dx=dx[k], dy=dy[k], back=True) for k in range(3)]
    return out + [L(xy("宣夜_眾星層"), BIG, back=True)]


DRIFT = dict(dx=(-45, 35, -20), dy=(10, -25, 18))

VO = {
    "02": "從西漢落下閎造渾儀，吵到唐朝一行實地量影子，足足八百年。《晉書》說：古言天者有三家——",
    "03": "蓋天、渾天、宣夜。天是一把傘、一顆蛋，還是根本沒有殼？",
    "04": "先說蓋天。它其實有兩版。早期說「天員如張蓋，地方如棋局」：天是一把撐開的傘，地是一張方棋盤。",
    "05": "可是連曾子都不信：真的天圓地方，四個角就蓋不住了。",
    "06": "到了《周髀算經》，改成「天象蓋笠，地法覆槃」：天像斗笠，地像倒扣的盤子，都是中間高、四邊低。",
    "07": "而且有數字：北極底下的地，比最外圈高六萬里；天和地，處處相隔八萬里。",
    "08": "太陽黏在天上，水平地繞著北極轉：夏天走內圈，冬天走外圈。",
    "09": "從上往下看，一年在七個同心圓之間來回，這叫「七衡六間」。外圈直徑四十七萬六千里，剛好是內圈的兩倍。",
    "10": "這些數字哪來的？立一根八尺的桿子，量正午的影子：夏至一尺六寸，冬至一丈三尺五寸。用影子長短，反推太陽多遠。",
    "11": "但這套算法有個前提：往南走一千里，影子就短一寸。直到唐朝一行派人實地去量——兩百多里就差一寸。",
    "12": "那太陽明明東升西落，怎麼會是平轉？蓋天家說：像螞蟻在磨盤上爬。",
    "13": "磨往左轉得快，螞蟻往右爬得慢，結果還是被磨帶著往左走。",
    "14": "第二家，渾天。傳為張衡所作的《渾天儀注》說：「渾天如雞子，天體圓如彈丸，地如雞子中黃。」",
    "15": "天是蛋殼，地是蛋黃；天表裡有水，大地浮在水上。",
    "16": "北極高出地面三十六度，赤道、黃道斜斜交叉，二十八宿繞天一圈，一半在地上、一半在地下——「半見半隱」。",
    "17": "這顆球能直接做成儀器、算出曆法。所以東漢蔡邕評三家：蓋天「考驗天狀，多所違失」，只有渾天「近得其情」。",
    "18": "第三家最大膽：宣夜。書早就失傳，只剩東漢郗萌記下的老師說法：「天了無質，仰而瞻之，高遠無極。」",
    "19": "那天為什麼是藍的？遠方的黃山看起來是青的，千仞深谷看起來是黑的——「青非真色，而黑非有體」。",
    "20": "日月眾星，自然浮在虛空裡，靠氣推動，各走各的，所以行星時快時慢、忽進忽退。",
    "21": "宣夜做不成儀器，也算不出曆法，蔡邕說它「絕無師法」。它說的氣當然不是今天的物理；但它拆掉了那層硬殼——這一步，比另外兩家都更接近今天的宇宙。",
}

# (鏡頭, 頁名, 秒數, 圖層)
PAGES = [
    ("02", "論天三家", 8.0, [L(p) for p in TRIO[:1]]),
    ("03", "＋蓋天", 2.0, [L(p) for p in TRIO[:2]]),
    ("03", "＋渾天", 2.0, [L(p) for p in TRIO[:3]]),
    ("03", "＋宣夜", 2.0, [L(p) for p in TRIO]),
    ("04", "蓋天兩版", 2.0, [L(p) for p in GAI2]),
    ("04", "＋第一版", 7.0, [L(p) for p in GAI2 + [gai("蓋天兩版_第一版層")]]),
    ("05", "＋曾子四角", 5.0, [L(p) for p in GAI2 + [gai("蓋天兩版_第一版層"), gai("蓋天兩版_四角層")]]),
    ("06", "＋第二版", 8.0, [L(p) for p in GAI2 + [gai("蓋天兩版_第一版層"), gai("蓋天兩版_四角層"),
                                                  gai("蓋天兩版_第二版層")]]),
    ("07", "側視", 3.0, [L(p) for p in SIDE]),
    ("07", "＋數值", 4.0, [L(p) for p in SIDE + [gai("側視_數值層")]]),
    ("08", "＋日行", 6.0, [L(p) for p in SIDE + [gai("側視_數值層"), gai("側視_日行層")]]),
    ("09", "七衡", 2.0, [L(p) for p in [gai("七衡六間_環層"), QH_C]]),
    ("09", "內衡", 1.5, [L(p) for p in [gai("七衡六間_逐衡_1_內衡"), QH_C]]),
    ("09", "中衡", 1.5, [L(p) for p in [gai("七衡六間_逐衡_4_中衡"), QH_C]]),
    ("09", "外衡", 1.5, [L(p) for p in [gai("七衡六間_逐衡_7_外衡"), QH_C]]),
    ("09", "七衡＋標籤", 4.5, [L(p) for p in [gai("七衡六間_環層"), QH_C, gai("七衡六間_標籤層"),
                                             gai("七衡六間_日位層")]]),
    ("10", "圭表", 4.0, [L(p) for p in GB]),
    ("10", "＋夏至", 3.0, [L(p) for p in GB + [gai("圭表日影_夏至層")]]),
    ("10", "＋冬至", 4.0, [L(p) for p in GB + [gai("圭表日影_夏至層"), gai("圭表日影_冬至層")]]),
    ("11", "＋寸差千里", 10.0, [L(p) for p in GB + [gai("圭表日影_夏至層"), gai("圭表日影_冬至層"),
                                                   gai("圭表日影_寸差千里層")]]),
    ("12", "蟻行磨石", 3.0, [L(gai("蟻行磨石_磨盤層")), L(MILL_T)]),
    ("12", "＋螞蟻", 3.0, [L(gai("蟻行磨石_磨盤層")), L(gai("蟻行磨石_蟻層")), L(MILL_T)]),
] + [
    ("13", f"轉{k}" if k else "＋旋向", 1.0 if k == 0 else 2.0,
     [L(gai("蟻行磨石_磨盤層"), rot=-45*k), L(gai("蟻行磨石_蟻層"), rot=-30*k), L(MILL_T),
      L(gai("蟻行磨石_旋向層"))])
    for k in range(4)
] + [
    ("14", "天球", 4.0, [L(p) for p in HUN]),
    ("14", "＋地", 4.0, [L(p) for p in HUN + [hun("地")]]),
    ("15", "＋載水而浮", 5.0, [L(p) for p in HUN + [hun("載水而浮"), hun("地")]]),
]
_h = HUN + [hun("載水而浮"), hun("地")]
for nm, sec in [("極軸", 2.5), ("赤道", 2.0), ("黃道", 2.0), ("二十八宿", 2.0), ("半見半隱", 1.5)]:
    _h = _h + [hun(nm)]
    PAGES.append(("16", "＋" + nm, sec, [L(p) for p in _h]))
_t = TRIO + [trio("評_出處"), trio("評_蓋天")]
PAGES += [
    ("17", "蔡邕評蓋天", 6.0, [L(p) for p in _t]),
    ("17", "＋評渾天", 4.0, [L(p) for p in _t + [trio("評_渾天")]]),
    ("18", "宣夜", 4.0, qi()),
    ("18", "＋題辭", 5.0, qi(**DRIFT) + [L(xy("宣夜_題辭層"))]),
    ("19", "青非真色", 2.0, [L(xy("青非真色_題辭層"))]),
    ("19", "＋山", 3.5, [L(xy("青非真色_山層")), L(xy("青非真色_題辭層"))]),
    ("19", "＋標籤", 3.5, [L(xy("青非真色_山層")), L(xy("青非真色_題辭層")), L(xy("青非真色_標籤層"))]),
    ("20", "日月五星", 4.0, qi() + [L(xy(n)) for n in ["宣夜_題辭層", "宣夜_日月五星層", "宣夜_題辭2層"]]),
    ("20", "飄移", 4.0, qi(**DRIFT) + [L(xy(n)) for n in ["宣夜_題辭層", "宣夜_日月五星層", "宣夜_題辭2層"]]),
    ("21", "三家評語", 6.0, [L(p) for p in _t + [trio("評_渾天"), trio("評_宣夜")]]),
    ("21", "＋宣夜高亮", 5.0, [L(p) for p in _t + [trio("評_渾天"), trio("評_宣夜"), trio("宣夜高亮")]]),
    ("21", "對照表", 4.0, [L("_三家並置/三家對照表_圖卡_黑底.png", CARD)]),
]


def build():
    out, t, seen = [], 5.0, set()
    for i, (shot, name, sec, layers) in enumerate(PAGES):
        first = shot not in seen
        seen.add(shot)
        out.append(dict(page=i + 2, shot=shot, title=f"鏡頭{shot}-{name}", start=round(t, 1), dur=sec,
                        trans="Match & Move", vo=VO[shot] if first else "", layers=layers))
        t += sec
    return out, t


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages, end = build()
    for pg in pages:
        for ly in pg["layers"]:
            assert os.path.exists(os.path.join(ROOT, ly["file"])), ly["file"]
    json.dump(pages, open(os.path.join(OUT, f"{EP}_Canva頁面參數.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    md = [f"# {EP} 論天三家｜Canva 逐頁製作表", "",
          "p1＝統一開頭（沿用複製來的開頭頁，只改字卡：同一片星空，古人吵了八百年——天到底長什麼樣？）；"
          f"最後接「下集見」（{end:.0f}s 起）→「追蹤我們」→「參考文獻」。", "",
          "| 頁 | 頁名 | 起 | 秒 | 與上一頁 | 圖層（由下到上） | 旁白 |", "|---|---|---|---|---|---|---|"]
    for pg in pages:
        lay = "＋".join(os.path.basename(l["file"]).replace("_透明.png", "").replace(".png", "")
                       + (f"（{l['rotation']:+.0f}°）" if l["rotation"] else "")
                       + ("〔滿版〕" if l["width"] == 1920 and l["height"] == 1920 else "")
                       for l in sorted(pg["layers"], key=lambda l: not l["back"]))
        md.append(f"| {pg['page']} | {pg['title']} | {pg['start']:.0f}s | {pg['dur']} | {pg['trans']} | {lay} | {pg['vo']} |")
    md += ["", f"合計 {len(pages)} 頁內容頁，{end:.0f} 秒（含開頭 5 秒）；下集見約 7 秒 → 全片約 {end+7:.0f} 秒。"]
    open(os.path.join(OUT, f"{EP}_逐頁製作表.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(len(pages), "pages, end", end)
