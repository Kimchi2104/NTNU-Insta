# -*- coding: utf-8 -*-
"""C-02 地有四游｜Canva 逐頁表（C 系列：概念圖定格頁，一頁多疊一層）

輸出：05_素材/C-02_地有四游/_canva/C-02_Canva頁面參數.json、C-02_逐頁製作表.md
每頁：團隊漸層背景＋山（沿用舊頁就保留原本的）＋概念圖圖層（方形 1080×1080，left 0、top 420）。
  - 地有四游：地塊俯視層／地塊側視層畫在正中，逐頁位移到冬至（−135, −135／0, −108）、夏至（反向）；
    Match & Move 會把大地沿對角線、上下來回推。
  - 舟行不覺：船、閉牖、人三層同位移（−60 → +60 px），整艘船往前走，水不動。
  - 開場回顧沿用 C-01 的「論天三家」四層（媒體 ID 在 C-01_Canva媒體ID.json）。
  - 9:16 圖卡：滿版 1080×1920。
旁白與秒數同 04_腳本庫/C-02-…-逐字稿-v2.md（語速約 4.3 字/秒）。
"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "C-02"
ROOT = os.path.join(BASE, "05_素材/C-02_地有四游")
OUT = os.path.join(ROOT, "_canva")

SQ = dict(left=0, top=420, width=1080, height=1080)
CARD = dict(left=0, top=0, width=1080, height=1920)


def L(path, box=SQ, rot=0.0, dx=0, dy=0, back=False):
    b = dict(box)
    b["left"] += dx; b["top"] += dy
    return dict(file=path, rotation=rot, back=back, **b)


def c01(n): return f"../C-01_論天三家/_三家並置/論天三家_{n}層_透明.png"
def sy(n): return f"地有四游/地有四游_{n}層_透明.png"
def rg(n): return f"日影推演/日影推演_{n}層_透明.png"
def bt(n): return f"舟行不覺/舟行不覺_{n}層_透明.png"
def rv(n): return f"兩種視角/兩種視角_{n}層_透明.png"
def tl(n): return f"時間軸/時間軸_{n}層_透明.png"
def yx(n): return f"姚信人形比天/人形比天_{n}層_透明.png"


VO = {
    "02": "上一集，三家在吵天長什麼樣。這一集換個問題：地，會不會動？漢代的緯書《尚書・考靈曜》給了一個大膽的答案——「地有四游」。",
    "03": "冬至，大地往上、往北、往西，移動三萬里；",
    "04": "夏至反過來，往下、往南、往東，也是三萬里；",
    "05": "春分、秋分，就停在正中間。一年來回一趟。",
    "06": "照這個方向推：冬至大地北移，太陽就顯得偏南、偏低，影子拉長；夏至大地南移，太陽偏高，影子變短。",
    "07": "同樣的影子變化，可以說是太陽在動，也可以說是地在動。那為什麼我們一點感覺都沒有？",
    "08": "書裡接著說：「地恆動不止，而人不知。」",
    "09": "「譬如人在大舟中閉牖而坐，舟行而人不覺也。」就像坐在大船的船艙裡，窗戶關上，船在走，你卻一點感覺也沒有。",
    "10": "從岸上看，船在動；從艙裡看，一切都靜止。誰在動？關在艙裡，你判斷不出來。",
    "11": "大約一千六百年後，伽利略在一六三二年的《關於兩大世界體系的對話》裡，也把人關進大船的船艙，用來說明：我們感覺不到地球在動。",
    "12": "但要說清楚：兩者講的「地動」不一樣。四游是大地一年來回平移，天照樣繞著地轉；伽利略講的，是地球自轉、又繞著太陽公轉。",
    "13": "結論不同；但「身在其中，就察覺不到自己在動」——這個洞見，是同一個。所以別說成「中國比伽利略更早發現地動」。",
    "14": "到了三國，吳國的姚信換了一種想法：「人為靈蟲，形最似天。」",
    "15": "人的下巴往前伸、蓋到胸口，後頸卻蓋不到背——前低後高。「近取諸身」，所以天也是南邊低、沒入地下，北邊偏高。",
    "16": "他還用這個傾斜解釋寒暑：冬至北極低，太陽離人遠，所以冷；夏至北極升起，太陽離人近，所以熱。",
    "17": "一個拿船來比，一個拿身體來比——在沒有望遠鏡的年代，古人就是這樣想事情的。",
}
OPEN_VO = "同一片星空，漢朝人說——大地一直在動，只是你不知道。"
NEXT_VO = "下週五：古人數過五隻神獸——其中一隻，不見了。"

# 四游：地塊位移（px）
STN = {"中": (0, 0, 0), "冬至": (-135, -135, -108), "夏至": (135, 135, 108)}


def sy_pg(where, quotes=(), track=False):
    dx, dy, sdy = STN[where]
    ls = [sy("題辭"), sy("框"), sy("站位")] + ([sy("軌跡")] if track else [])
    return [L(p) for p in ls] + [L(sy("地塊俯視"), dx=dx, dy=dy), L(sy("地塊側視"), dy=sdy)] + \
        [L(sy(q)) for q in quotes]


def boat_pg(dx, extra_top=(), parts=("船", "閉牖", "人")):
    return [L(bt("題辭")), L(bt("水"))] + [L(bt(p), dx=dx) for p in parts] + [L(bt(p)) for p in extra_top]


Q3 = ("冬至", "夏至", "春秋分")
YAO = [yx("題辭"), yx("人形")]

# (鏡頭, 頁名, 秒數, 圖層)
PAGES = [
    ("02", "上一集", 4.0, [L(c01(n)) for n in ("題辭", "蓋天", "渾天", "宣夜")]),
    ("02", "地有四游", 8.0, [L(sy("題辭")), L(sy("框"))]),
    ("03", "＋地塊", 1.0, sy_pg("中")),
    ("03", "冬至", 3.0, sy_pg("冬至", Q3[:1])),
    ("04", "夏至", 4.0, sy_pg("夏至", Q3[:2])),
    ("05", "春秋分", 2.5, sy_pg("中", Q3)),
    ("05", "＋軌跡→冬至", 1.0, sy_pg("冬至", Q3, True)),
    ("05", "→夏至", 1.0, sy_pg("夏至", Q3, True)),
    ("05", "→回中", 0.8, sy_pg("中", Q3, True)),
    ("06", "日影推演", 1.5, [L(rg("題辭")), L(rg("日"))]),
    ("06", "＋冬至", 4.0, [L(rg(n)) for n in ("題辭", "日", "冬至")]),
    ("06", "＋夏至", 4.0, [L(rg(n)) for n in ("題辭", "日", "冬至", "夏至")]),
    ("07", "＋結論", 8.5, [L(rg(n)) for n in ("題辭", "日", "冬至", "夏至", "結論")]),
    ("08", "地恆動不止", 4.0, [L(bt("恆動"))]),
    ("09", "大舟", 1.5, [L(bt("題辭")), L(bt("水"))]),
    ("09", "＋船", 2.0, boat_pg(-60, parts=("船",))),
    ("09", "＋閉牖", 2.0, boat_pg(-60, parts=("船", "閉牖"))),
    ("09", "＋人", 2.5, boat_pg(-60)),
    ("09", "舟行", 3.5, boat_pg(60, extra_top=("行進",))),
    ("10", "兩種視角", 2.5, [L(rv("分隔")), L(rv("艙外"))]),
    ("10", "＋艙內", 2.0, [L(rv(n)) for n in ("分隔", "艙外", "艙內")]),
    ("10", "＋結論", 3.0, [L(rv(n)) for n in ("分隔", "艙外", "艙內", "結論")]),
    ("11", "時間軸", 6.5, [L(tl(n)) for n in ("題辭", "軸")]),
    ("11", "＋間隔", 6.0, [L(tl(n)) for n in ("題辭", "軸", "間隔")]),
    ("12", "＋差異", 12.0, [L(tl(n)) for n in ("題辭", "軸", "間隔", "差異")]),
    ("13", "＋相同", 10.5, [L(tl(n)) for n in ("題辭", "軸", "間隔", "差異", "相同")]),
    ("14", "姚信", 3.0, [L(p) for p in YAO]),
    ("14", "＋天", 2.5, [L(p) for p in YAO + [yx("天")]]),
    ("15", "＋人形標註", 4.0, [L(p) for p in YAO + [yx("天"), yx("人形標註")]]),
    ("15", "＋傾斜軸", 2.5, [L(p) for p in YAO + [yx("天"), yx("人形標註"), yx("傾斜軸")]]),
    ("15", "＋極軸", 4.5, [L(p) for p in YAO + [yx("天"), yx("人形標註"), yx("傾斜軸"), yx("極軸"),
                                                yx("類比箭頭"), yx("近取諸身")]]),
    ("16", "寒暑・冬至", 4.5, [L(p) for p in YAO + [yx("天"), yx("人形標註"), yx("傾斜軸"), yx("極軸_冬至"),
                                                    yx("寒暑")]]),
    ("16", "寒暑・夏至", 4.5, [L(p) for p in YAO + [yx("天"), yx("人形標註"), yx("傾斜軸"), yx("極軸_夏至"),
                                                    yx("寒暑")]]),
    ("17", "圖卡", 7.5, [L("_圖卡/地有四游_圖卡_黑底.png", CARD)]),
]


def nchar(s):
    return len(re.findall(r"[一-鿿0-9A-Za-z]", s))


def build():
    out, t, seen = [], 5.0, set()
    for i, (shot, name, sec, layers) in enumerate(PAGES):
        first = shot not in seen
        seen.add(shot)
        out.append(dict(page=i + 2, shot=shot, title=f"鏡頭{shot}-{name}", start=round(t, 1), dur=sec,
                        trans="Match & Move", vo=VO[shot] if first else "", layers=layers))
        t += sec
    return out, t


def shot_check():
    """每個鏡頭：旁白字數 ÷ 秒數，太快（> 4.8 字/秒）就印出來"""
    secs = {}
    for shot, _, sec, _ in PAGES:
        secs[shot] = secs.get(shot, 0) + sec
    for shot, sec in secs.items():
        n = nchar(VO[shot]); r = n / sec
        print(f"  鏡頭{shot}: {n:3d} 字 / {sec:4.1f}s = {r:.2f} 字/秒" + ("  ⚠️ 太快" if r > 4.8 else ""))
    tot = sum(nchar(v) for v in VO.values()) + nchar(OPEN_VO) + nchar(NEXT_VO)
    return tot


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages, end = build()
    for pg in pages:
        for ly in pg["layers"]:
            assert os.path.exists(os.path.normpath(os.path.join(ROOT, ly["file"]))), ly["file"]
    tot = shot_check()
    json.dump(pages, open(os.path.join(OUT, f"{EP}_Canva頁面參數.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    md = [f"# {EP} 地有四游｜Canva 逐頁製作表", "",
          "p1＝統一開頭（沿用複製來的開頭頁，只改字卡：同一片星空，漢朝人說——大地一直在動，只是你不知道。）；"
          f"最後接「下集見」（{end:.0f}s 起，麒麟與倮獸）→「追蹤我們」→「參考文獻」。", "",
          "位移欄：(dx, dy) px，相對方形圖層原位（left 0、top 420）。", "",
          "| 頁 | 頁名 | 起 | 秒 | 與上一頁 | 圖層（由下到上） | 旁白 |", "|---|---|---|---|---|---|---|"]
    for pg in pages:
        lay = "＋".join(os.path.basename(l["file"]).replace("_透明.png", "").replace(".png", "")
                       + (f"（{l['left']:+.0f}, {l['top'] - 420:+.0f}）" if (l["left"], l["top"]) != (0, 420)
                          and l["width"] == 1080 and l["height"] == 1080 else "")
                       + ("〔滿版〕" if l["height"] == 1920 else "")
                       for l in pg["layers"])
        md.append(f"| {pg['page']} | {pg['title']} | {pg['start']:.1f}s | {pg['dur']} | {pg['trans']} | {lay} | {pg['vo']} |")
    md += ["", f"合計 {len(pages)} 頁內容頁，{end:.0f} 秒（含開頭 5 秒）；下集見約 7 秒 → 全片約 {end+7:.0f} 秒；"
               f"旁白約 {tot} 字。"]
    open(os.path.join(OUT, f"{EP}_逐頁製作表.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(len(pages), "pages, end", end, "chars", tot)
