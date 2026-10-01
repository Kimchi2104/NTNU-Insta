# -*- coding: utf-8 -*-
"""C-03 麒麟與倮獸｜Canva 逐頁表（C 系列：概念圖＋星圖定格頁，一頁多疊一層）

輸出：05_素材/C-03_麒麟與倮獸/_canva/C-03_Canva頁面參數.json、C-03_逐頁製作表.md
每頁：團隊漸層背景＋山（沿用舊頁就保留原本的）＋圖層（方形 1080×1080，left 0、top 420）。
  - 四象盤：四方一頁亮一格，最後中央留空；回到中央時換成「中央倮獸」＋《月令》。
  - 五蟲說、考工記五旗：一列一頁。
  - 星圖（軒轅／牛郎織女／弧矢）跟概念圖同規格，直接疊；軒轅 17 顆星逐顆編號。
  - 9:16 圖卡：滿版 1080×1920。
旁白與秒數同 04_腳本庫/C-03-…-逐字稿-v2.md（語速約 4.3 字/秒）。
"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G

BASE = G.find_base(os.path.dirname(os.path.abspath(__file__)))
EP = "C-03"
ROOT = os.path.join(BASE, "05_素材/C-03_麒麟與倮獸")
OUT = os.path.join(ROOT, "_canva")

SQ = dict(left=0, top=420, width=1080, height=1080)
CARD = dict(left=0, top=0, width=1080, height=1920)


def L(path, box=SQ, rot=0.0, dx=0, dy=0, back=False):
    b = dict(box)
    b["left"] += dx; b["top"] += dy
    return dict(file=path, rotation=rot, back=back, **b)


def wh(n): return f"四象與五象/四象盤_{n}層_透明.png"
def wu(n): return f"五蟲說/五蟲說_{n}層_透明.png"
def cp(n): return f"四象五蟲對照/對照_{n}層_透明.png"
def ld(n): return f"曾侯乙漆箱/漆箱蓋面_{n}層_透明.png"
def sd(n): return f"側面判讀/側面判讀_{n}層_透明.png"
def et(n): return f"民族來源/民族來源_{n}層_透明.png"
def qi(n): return f"考工記五旗/五旗_{n}層_透明.png"
def xy(n): return f"軒轅十七星/軒轅_{n}層_透明.png"
def nn(n): return f"牛郎織女/牛郎織女_{n}層_透明.png"
def hs(n): return f"弧矢九星/弧矢_{n}層_透明.png"
def cd(n): return f"倮獸主星候選/候選_{n}層_透明.png"


VO = {
    "02": "東青龍、南朱雀、西白虎、北玄武——四象，大家都背得出來。但四個方位排完，中間那一格，是空的。",
    "03": "中間那一格，古人填過。《大戴禮記》把動物分成五類，每一類有一個「長」：羽蟲之長是鳳皇，毛蟲是麒麟，甲蟲是神龜，鱗蟲是蛟龍。",
    "04": "第五類叫「倮之蟲」——沒有羽毛，也沒有鱗甲。牠們的長，是「聖人」，也就是人。",
    "05": "把兩張名單並排：龍對蛟龍、鳥對鳳皇、龜對神龜，都對得上。但西方的白虎不在名單裡，毛蟲之長是麒麟；名單上還多了一個「人」。",
    "06": "四象是怎麼來的？看一件實物：曾侯乙墓的漆箱，約公元前四三三年。箱蓋正中一個「斗」字，繞著它寫滿二十八宿——這是目前所見最早的二十八宿全名。兩側各畫一隻神獸：青龍、白虎。",
    "07": "那另外兩方呢？箱子側面也有畫，但讀法不一：一說北面整面塗黑，黑色主北，就是玄武；一說那一面畫著兩隻相對的獸，中間夾三顆星，社團的簡報把牠們讀作麒麟。",
    "08": "如果北方原本是麒麟，四象就不是一開始就定好的。社團的考據認為，四方背後是不同族群：東夷的龍、西羌的虎、南蠻的鳥、夏越的龜——而麒麟，可能來自北方的東胡。",
    "09": "回到中間那一格。《禮記・月令》說：「中央土……其帝黃帝……其蟲倮。」中央，是人的位置。那人的星在哪？社團列了三個候選。",
    "10": "第一個：軒轅。線索在名字——黃帝就號軒轅；《史記》說「軒轅，黃龍體」。它在獅子座一帶，一條蜿蜒的星鏈，星數正好十七顆。",
    "11": "第二個：牛郎織女——天上少數有「人」的故事。這兩顆星加上天津四，就是蒙古那一集的「三鹿」。",
    "12": "第三個：弧矢。《考工記》寫車上的旗：龍、鳥、熊、龜蛇，各象一組星；第五面是「弧旌枉矢，以象弧也」——四面是動物，第五面，是人做的弓。而《史記》說「下有四星曰弧，直狼」：這把弓，對著天狼星。",
    "13": "三個候選，三個都還帶著問號。沒有任何傳世文獻明說，中央的倮獸對應哪一組星官——這一題，到今天還沒有答案。",
    "14": "",
}
OPEN_VO = "同一片星空，古人數過五隻神獸——其中一隻，不見了。"
NEXT_VO = "下週五：不用任何儀器，波里尼西亞人怎麼橫渡太平洋？"

SEC4 = ["青龍", "朱雀", "白虎", "玄武"]
WU5 = [f"列{i}" for i in range(1, 6)]
CENTER = [wh("題辭_中央"), wh("外圈")] + [wh(s) for s in SEC4] + [wh("中央倮獸")]


def lay(*paths):
    return [L(p) for p in paths]


# (鏡頭, 頁名, 秒數, 圖層)
PAGES = [
    ("02", "四象・青龍", 1.4, lay(wh("題辭_四象"), wh("外圈"), wh("青龍"))),
    ("02", "＋朱雀", 1.1, lay(wh("題辭_四象"), wh("外圈"), *[wh(s) for s in SEC4[:2]])),
    ("02", "＋白虎", 1.1, lay(wh("題辭_四象"), wh("外圈"), *[wh(s) for s in SEC4[:3]])),
    ("02", "＋玄武", 1.4, lay(wh("題辭_四象"), wh("外圈"), *[wh(s) for s in SEC4])),
    ("02", "＋中央留空", 4.0, lay(wh("題辭_四象"), wh("外圈"), *[wh(s) for s in SEC4], wh("中央留空"))),
    ("03", "五蟲說", 4.5, lay(wu("題辭"), wu("表頭"))),
    ("03", "＋羽", 2.0, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5[:1]])),
    ("03", "＋毛", 1.8, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5[:2]])),
    ("03", "＋甲", 1.8, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5[:3]])),
    ("03", "＋鱗", 2.4, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5[:4]])),
    ("04", "＋倮", 4.0, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5])),
    ("04", "＋結語", 3.5, lay(wu("題辭"), wu("表頭"), *[wu(r) for r in WU5], wu("結語"))),
    ("05", "對照", 2.3, lay(cp("題辭"), cp("欄位"), cp("項目"))),
    ("05", "＋對得上", 4.3, lay(cp("題辭"), cp("欄位"), cp("項目"), cp("對得上"))),
    ("05", "＋對不上", 5.9, lay(cp("題辭"), cp("欄位"), cp("項目"), cp("對得上"), cp("對不上"))),
    ("06", "漆箱", 4.3, lay(ld("題辭"), ld("箱蓋"))),
    ("06", "＋斗", 2.0, lay(ld("題辭"), ld("箱蓋"), ld("斗字"))),
    ("06", "＋二十八宿", 4.3, lay(ld("題辭"), ld("箱蓋"), ld("斗字"), ld("宿環"))),
    ("06", "＋龍虎", 3.2, lay(ld("題辭"), ld("箱蓋"), ld("斗字"), ld("宿環"), ld("龍虎"))),
    ("06", "＋結語", 3.0, lay(ld("題辭"), ld("箱蓋"), ld("斗字"), ld("宿環"), ld("龍虎"), ld("結語"))),
    ("07", "側面", 4.0, lay(sd("題辭"), sd("外框"))),
    ("07", "＋讀法一", 5.0, lay(sd("題辭"), sd("外框"), sd("讀法一"))),
    ("07", "＋讀法二", 7.3, lay(sd("題辭"), sd("外框"), sd("讀法一"), sd("讀法二"))),
    ("08", "四方族群", 5.0, lay(et("題辭"), et("外圈"), *[et(s) for s in SEC4])),
    ("08", "＋族群", 6.0, lay(et("題辭"), et("外圈"), *[et(s) for s in SEC4], et("族群"))),
    ("08", "＋東胡", 5.0, lay(et("題辭"), et("外圈"), *[et(s) for s in SEC4], et("族群"), et("東胡"))),
    ("09", "中央倮獸", 3.5, lay(*CENTER)),
    ("09", "＋月令", 5.0, lay(*CENTER, wh("月令"))),
    ("09", "三候選", 3.0, lay(cd("題辭"), cd("方框"))),
    ("10", "軒轅", 2.8, lay(xy("題辭"), xy("星點"), xy("連線"))),
    ("10", "＋名稱線索", 4.2, lay(xy("題辭"), xy("星點"), xy("連線"), xy("名稱"), xy("線索"))),
    ("10", "＋十七顆", 5.0, lay(xy("題辭"), xy("星點"), xy("連線"), xy("名稱"), xy("線索"), xy("編號"))),
    ("11", "牛郎織女", 4.5, lay(nn("題辭"), nn("星點"), nn("銀河"), nn("連線"), nn("名稱"))),
    ("11", "＋三鹿", 4.5, lay(nn("題辭"), nn("星點"), nn("銀河"), nn("連線"), nn("名稱"), nn("三鹿"))),
    ("12", "五旗・龍鳥", 2.8, lay(qi("題辭"), qi("旗1"), qi("旗2"))),
    ("12", "＋熊・龜蛇", 1.6, lay(qi("題辭"), *[qi(f"旗{i}") for i in range(1, 5)])),
    ("12", "＋弧旌枉矢", 3.0, lay(qi("題辭"), *[qi(f"旗{i}") for i in range(1, 6)])),
    ("12", "＋結語", 3.2, lay(qi("題辭"), *[qi(f"旗{i}") for i in range(1, 6)], qi("結語"))),
    ("12", "弧矢", 3.2, lay(hs("題辭"), hs("星點"), hs("銀河"), hs("連線"), hs("名稱"), hs("天狼"))),
    ("12", "＋直狼", 4.2, lay(hs("題辭"), hs("星點"), hs("銀河"), hs("連線"), hs("名稱"), hs("天狼"), hs("直狼"))),
    ("13", "三候選？", 4.0, lay(cd("題辭"), cd("方框"), cd("問號"))),
    ("13", "＋沒有答案", 7.5, lay(cd("題辭"), cd("方框"), cd("問號"), cd("結語"))),
    ("14", "圖卡", 3.0, [L("_圖卡/麒麟與倮獸_圖卡_黑底.png", CARD)]),
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
    md = [f"# {EP} 麒麟與倮獸｜Canva 逐頁製作表", "",
          f"p1＝統一開頭（沿用複製來的開頭頁，只改字卡：{OPEN_VO}）；"
          f"最後接「下集見」（{end:.0f}s 起，A-09 夏威夷星線）→「追蹤我們」→「參考文獻」。", "",
          "所有圖層都是方形 1080×1080、left 0、top 420（圖卡滿版）；本集沒有位移動畫，Match & Move 只負責淡入新層。", "",
          "| 頁 | 頁名 | 起 | 秒 | 與上一頁 | 圖層（由下到上） | 旁白 |", "|---|---|---|---|---|---|---|"]
    for pg in pages:
        lay_s = "＋".join(os.path.basename(l["file"]).replace("_透明.png", "").replace(".png", "")
                         + ("〔滿版〕" if l["height"] == 1920 else "") for l in pg["layers"])
        md.append(f"| {pg['page']} | {pg['title']} | {pg['start']:.1f}s | {pg['dur']} | {pg['trans']} | {lay_s} | {pg['vo']} |")
    md += ["", f"合計 {len(pages)} 頁內容頁，{end:.0f} 秒（含開頭 5 秒）；下集見約 7 秒 → 全片約 {end+7:.0f} 秒；"
               f"旁白約 {tot} 字。"]
    open(os.path.join(OUT, f"{EP}_逐頁製作表.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(len(pages), "pages, end", end, "chars", tot)
