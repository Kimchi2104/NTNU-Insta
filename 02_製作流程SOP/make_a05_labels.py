# -*- coding: utf-8 -*-
"""A-05 日本｜補 v4.6 欄位（不重畫任何圖層）

A-05 是 v4.5 做的，沒有 {EP}_標籤資料.json、鏡頭也沒有 vo／labels 欄，
所以 gen_canva_pages.py 出的逐頁表沒有旁白、描圖紙沒有標籤。
這支只做兩件事：
  1. 在 A-05_鏡頭清單.json 每一鏡補上 vo（逐字稿 v2）、labels、overlay、card
  2. 寫出 A-05_標籤資料.json：原生打字用的標籤（和名／語意／宿名／跨文化原文＋中譯）
     與名詞總表（原文／羅馬字／英文翻譯／中文），給不會中文的組員複製貼上

標籤位置沿用 make_a05_v4.py 的錨點與避讓結果；原生打字時原文、中譯分兩行
（跨文化：原文在列中心上方 0.75°、中譯在下方 0.95°，字級 1.0／0.8），可同時開。
圖層 SVG 一個位元組都不動（團隊已上傳 Canva）。

執行：python3 make_a05_labels.py && python3 gen_canva_pages.py A-05
"""
import os, sys, json, re, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ep_assets as G
import gen_master_canvas as MC
from gen_master_canvas import Master
import make_a05_v4 as A

BASE = A.BASE
EP = A.EP
OUT = A.OUT
SCRIPT = os.path.join(BASE, "04_腳本庫", "A-05-日本一整座天空的農具-逐字稿-v2.md")

# 和名羅馬字（Hepburn）與語意英譯；語意欄空白＝至今無公認語意（逐字稿第 10 鏡）
ROMAJI = ["Suboshi", "Amiboshi", "Tomoboshi", "Soiboshi", "Nakagoboshi", "Ashitareboshi",
          "Miboshi", "Hitsukiboshi", "Inamiboshi", "Urukiboshi", "Tomiteboshi",
          "Umiyameboshi", "Hatsuiboshi", "Namameboshi", "Tokakiboshi", "Tataraboshi",
          "Ekieboshi", "Subaruboshi", "Amefuriboshi", "Torokiboshi", "Karasukiboshi",
          "Chichiriboshi", "Tamaonoboshi", "Nurikoboshi", "Hotooriboshi", "Chirikoboshi",
          "Tasukiboshi", "Mitsukakeboshi"]
MEAN_EN = {
    "亢": "Net? (Nojiri: meaning unknown)",
    "房": "Attendant star (beside the Heart)",
    "心": "The one in the middle",
    "尾": "Dangling legs",
    "箕": "Winnowing basket",
    "牛": "Rice-watching (season when rice is seen)",
    "奎": "Tokaki: stick for levelling a rice measure",
    "婁": "Tatara: foot-bellows of an iron furnace (conjecture)",
    "昴": "Subaru: to gather into one bundle",
    "畢": "Rain-falling (borrowed from Chinese classics)",
    "參": "Karasuki: a plough",
    "鬼": "Star of the soul-cord",
    "柳": "Nurigome? (inner storeroom)",
    "星": "Heat (conjecture)",
    "翼": "Tasuki: cord for tying back sleeves",
}
# 跨文化英文（Stellarium 各文化 index.json 的 english；日本三條依逐字稿）
CROSS_EN = {
    "からすきぼし 唐鋤星": "Plough star (Japan)",
    "Bintoéng Rakkalaé": "Plough", "Rarița": "The Little Plough",
    "Sfredelul mare": "The Great Auger", "Касцы Kastsy": "The Mowers",
    "Kichigi": "Threshers", "Sioyahpu": "Adze Handle", "Sos Bacheddos": "The Sticks",
    "النظم al-Naẓm": "The String", "Ullaktut": "Runners",
    "すばる 統ばる": "Subaru: gathered into one bundle (Japan)",
    "S'Udrone": "The Bunch", "الثريا al-Thurayyā": "Al-Thurayya",
    "Куркі Kurki": "The Hens", "Cloșca cu pui": "The Hatching Hen with Her Chicks",
    "Sakiattiak": "Breastbone", "Eixu": "Hornet", "Makaliʻi": "The Chief's Eyes",
    "Kṛttikā": "Nurses of Kartikeya",
    "あめふりぼし 雨降り星": "Rain-falling star (Japan, borrowed from Chinese classics)",
    "Wolf's Mouth": "Wolf's Mouth", "Jaw": "Jaw", "Tapi'i rainhyka": "Tapir's Jaw",
    "Qimmiitt": "Dogs", "釣鐘星 つりがねぼし": "Temple-bell star (true Japanese folk name)",
    "たまおのぼし 魂緒の星": "Star of the soul-cord (Japan)",
    "النثرة al-Nathrah": "Nostrils [of the lion]", "Puṣyā": "The Nourisher",
    "Racul": "The Crayfish",
}
GROUPS = [(A.BELT, "腰帶"), (A.PLEIADES, "昴"), (A.HYADES, "畢"), (A.BEEHIVE, "鬼")]
# 第 11 鏡旁白講的是畢宿的日本民間名（不是跨文化那一欄）：三個民間名＋一個漢籍移植名
HYADES_JA = [
    ("雨降り星 あめふりぼし", "下雨（借自《詩經》）",
     "Rain-falling star (borrowed from the Chinese Book of Songs)"),
    ("釣鐘星 つりがねぼし", "吊鐘（民間名）", "Temple-bell star (folk name)"),
    ("稲叢星 いなむらぼし", "稻堆（民間名）", "Rice-stack star (folk name)"),
    ("扇星 おうぎぼし", "扇子（民間名）", "Folding-fan star (folk name)"),
]

# 每鏡要開的原生標籤層、概念圖、字卡（依逐字稿 v2「用檔／圖層」欄）
# 概念圖＝_概念圖/ 裡的檔名前綴；分層圖用 overlay_layers 依序一層一頁疊上去，
# gen_canva_pages 會在該鏡迄格後插「定格頁」（畫面不動，只加概念圖），overlay_at="start" 改放起格後
SHOT_EXTRA = {
    "01": dict(labels=["和名"], overlay="C-A05-01_六連星",
               overlay_layers=["星點層", "束線層", "標籤層"]),
    "03": dict(overlay="C-A05-02_キトラ四圈", overlay_layers=["圈層", "尺寸層", "算式層"]),
    "05": dict(overlay="C-A05-02_キトラ四圈_爭議層"),
    "06": dict(labels=["繁中宿名", "和名"]),
    "07": dict(labels=["繁中宿名", "和名", "和名語意"]),
    "08": dict(labels=["繁中宿名", "和名", "和名語意"],
               card="左右對照：韓國＝官職名冊（心宿＝天王正位、房宿＝明堂）／"
                    "日本＝量米的棒子、煉鐵的風箱、下雨、一把犁"),
    "09": dict(labels=["繁中宿名", "和名", "和名語意"]),
    "10": dict(labels=["和名"], card="江戸の訳名／十一個意味不明"),
    "11": dict(labels=["畢宿和名", "畢宿和名中譯"]),
    "12": dict(labels=["和名", "和名語意"],
               card="《古事記》美須麻流之珠／《和名類聚抄》昴星 和名須八流／"
                    "《枕草子》星は、すばる"),
    "13": dict(overlay="C-A05-01_六連星_方言層",
               note_add="車廠徽章請美宣另尋授權圖，本專案不自繪商標"),
    "14": dict(labels=["跨文化原文-腰帶", "跨文化中譯-腰帶"]),
    "17": dict(labels=["和名"], card="EP6 中秋｜二十八宿：月亮的 28 間驛站"),
}


def read_vo():
    """逐字稿 v2 分鏡表：| **01** Z | 16 | 旁白 | 用檔 | 動作 |"""
    vo = {}
    for line in open(SCRIPT, encoding="utf-8"):
        mm = re.match(r"^\|\s*\*\*(\d\d)\*\*\s*[A-Z]\s*\|\s*\d+\s*\|\s*(.+?)\s*\|", line)
        if mm:
            vo[mm.group(1)] = mm.group(2).replace("**", "")
    return vo


def main():
    S = G.load_stars(BASE)
    tmp = tempfile.mkdtemp()
    m = Master(EP, S, tmp, lst=A.LST0, D_s=45, D_r=49, D_fill=0, w_c=34, feather=8,
               x_tN=0.0, x_tS=0.0, phi=A.PHI, maglim=5.5, mw_n=15000)
    shutil.rmtree(tmp, ignore_errors=True)
    key2color = {k: c for c, ks in A.XIANG.items() for k in ks}

    # ── 二十八宿：和名錨點與避讓照 make_a05_v4.py（同參數同順序） ──
    base_items, rows = [], []
    for i, (key, zh, kana, mean) in enumerate(A.SHUKU):
        cc = A.centroid(A.hips_of(key, A.jsegs), S)
        if not cc:
            continue
        col = key2color.get(key, "white")
        base_items.append(dict(ra=cc[0], dec=cc[1], color=col, size=1.5, dx=0.0, dy=3.2,
                               text=kana, key=f"{i + 1:02d}{zh}"))
        rows.append((i, key, zh, kana, mean, col))
    ja = MC.spread_labels(m, base_items, pad=1.4, pull=0.05, verbose=False)
    zh_items, mean_items = [], []
    for it, (i, key, zh, kana, mean, col) in zip(ja, rows):
        zh_items.append(dict(it, text=f"{zh}宿", size=1.3, dy=it["dy"] + 2.75))
        if mean:
            mean_items.append(dict(it, text=mean, size=1.2, dy=it["dy"] - 6.4))

    # ── 跨文化：原文在上、中譯在下，兩行一組（列距 3.6° 不變） ──
    cross_sets = {}
    for hips, gname in GROUPS:
        cc = A.centroid(hips, S)
        nat, zh = [], []
        for native, zh_t, grp, color, dx, dy in A.CROSS:
            if grp is not hips:
                continue
            common = dict(ra=cc[0], dec=cc[1], color=color, dx=dx, key=native)
            nat.append(dict(common, text=native, size=1.0, dy=dy + 0.75))
            zh.append(dict(common, text=zh_t, size=0.8, dy=dy - 0.95))
        cross_sets[gname] = (nat, zh)

    # 畢宿民間名：畢宿上方一欄，列距 2.9°、字級 0.85／0.65（第 11 鏡 fov 26 仍在安全區內）
    hc = A.centroid(A.HYADES, S)
    hy_nat, hy_zh = [], []
    for k, (native, zh_t, _en) in enumerate(HYADES_JA):
        dy = 5.5 + 2.9 * (len(HYADES_JA) - 1 - k)
        common = dict(ra=hc[0], dec=hc[1], color="white" if k == 0 else "red", dx=0.0,
                      key=native)
        hy_nat.append(dict(common, text=native, size=0.85, dy=dy + 0.6))
        hy_zh.append(dict(common, text=zh_t, size=0.65, dy=dy - 0.8))

    label_sets = [{"name": "和名", "items": ja}, {"name": "繁中宿名", "items": zh_items},
                  {"name": "畢宿和名", "items": hy_nat}, {"name": "畢宿和名中譯", "items": hy_zh},
                  {"name": "和名語意", "items": mean_items}]
    for g, (nat, zh) in cross_sets.items():
        label_sets += [{"name": f"跨文化原文-{g}", "items": nat},
                       {"name": f"跨文化中譯-{g}", "items": zh}]

    terms = {}
    for i, key, zh, kana, mean, col in rows:
        terms[f"{i + 1:02d} {zh}宿"] = {
            "hips": A.hips_of(key, A.jsegs), "原文": kana, "拼音": ROMAJI[i],
            "英文翻譯": MEAN_EN.get(zh, f"(no agreed meaning) — Stellarium: {key}"),
            "中文": f"{zh}宿" + (f"｜{mean}" if mean else "｜至今無公認語意"),
            "顏色": col, "來源備註": "野尻抱影《日本星名辞典》；逐字稿 v2 和名對照表"}
    cross = [{"原文": c[0], "中譯": c[1], "顏色": c[3], "英文": CROSS_EN.get(c[0], "")}
             for c in A.CROSS]
    cross += [{"原文": n, "中譯": z, "顏色": "red", "英文": e} for n, z, e in HYADES_JA[2:]]

    json.dump({"ep": EP, "label_sets": label_sets, "terms": terms, "cross": cross,
               "mains": A.MAINS, "lines": {"L4": "星座連線"}},
              open(os.path.join(OUT, f"{EP}_標籤資料.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # ── 鏡頭清單補欄位（原有欄位不動） ──
    sp = os.path.join(OUT, f"{EP}_鏡頭清單.json")
    shots = json.load(open(sp, encoding="utf-8"))
    vo = read_vo()
    for sh in shots:
        ex = SHOT_EXTRA.get(sh["code"], {})
        sh["vo"] = vo.get(sh["code"], "")
        sh["labels"] = ex.get("labels", [])
        for k in ("overlay", "overlay_layers", "overlay_at", "card"):
            if k in ex:
                sh[k] = ex[k]
        if "note_add" in ex and ex["note_add"] not in sh.get("note", ""):
            sh["note"] = sh.get("note", "") + "；" + ex["note_add"]
    json.dump(shots, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    missing = [s["code"] for s in shots if not s["vo"]]
    print(f"  ✓ {EP}_標籤資料.json（{sum(len(s['items']) for s in label_sets)} 條標籤、"
          f"{len(terms)} 宿、{len(cross)} 條跨文化）")
    print(f"  ✓ {EP}_鏡頭清單.json 補上 vo／labels（{len(shots)} 鏡"
          + (f"；缺旁白：{missing}" if missing else "") + "）")


if __name__ == "__main__":
    main()
