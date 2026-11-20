# -*- coding: utf-8 -*-
"""X-07 卡 04：印出某一頁要送 edit-design 的 ops。
用法：/usr/bin/python3 x07_page.py N      （N＝逐頁製作表的頁號 1–36；新頁 N 在設計裡是第 32+N 頁）
輸出 JSON：{"page_index":…, "ops":[…第一次送…], "after":[…第二次要送的 format／crop 說明…]}
"""
import sys, os, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "02_製作流程SOP"))
import canva_ops as co
import gen_subtitles as gs

EP = "X-07"
d = co.folder(EP)
pages = {p["page"]: p for p in json.load(open(os.path.join(d, f"{EP}_Canva頁面參數.json"), encoding="utf-8"))}
media = json.load(open(os.path.join(d, f"{EP}_Canva媒體ID.json"), encoding="utf-8"))
labs = list(csv.DictReader(open(os.path.join(d, f"{EP}_逐頁標籤座標.csv"), encoding="utf-8-sig")))
tab = {int(r["頁"]): r for r in csv.DictReader(open(os.path.join(d, f"{EP}_Canva逐頁製作表.csv"), encoding="utf-8-sig"))}
ids = open(os.path.join(HERE, "page_ids.txt")).read().split()

n = int(sys.argv[1])
pg, pid = pages[n], ids[n - 1]
page_labels = [lb for lb in labs if int(lb["頁"]) == n]
ops = co.page_ops(pg, pid, media, page_labels)
notes_op = ops.pop()                       # replace_speaker_notes 放最後
after = [{"what": "mountain", "do": "crop_media 0/0/1939.0832424885327×300.5579025857226（locator＝fill 是 MAD4KTwSGtw 的那個）"}]
for it in co.label_items(page_labels):
    after.append({"what": "label", "text": it["text"],
                  "format_text": {"font_size": int(it["size"]), "color": it["color"],
                                  "text_align": it["align"], "line_height": 1.2}})
has_overlay = bool(pg.get("overlay"))
card = tab[n]["字卡"].strip()
vo = tab[n]["旁白（本頁起播）"].strip()
if card and not has_overlay:
    text = "\n".join(card.split("／"))
    ops.append({"type": "add_text", "page_id": pid, "text": text, "left": 60, "top": 300, "width": 960})
    after.append({"what": "card", "text": text,
                  "format_text": {"font_size": 72, "color": "#FFFFFF", "text_align": "center", "line_height": 1.2}})
if vo and not has_overlay:
    lines = gs.wrap(vo, 16)
    h = len(lines) * 44 * 1.3
    top = round(max(250, 1600 - h), 1)
    text = "\n".join(lines)
    ops.append({"type": "add_text", "page_id": pid, "text": text, "left": 60, "top": top, "width": 960})
    after.append({"what": "subtitle", "text": text,
                  "format_text": {"font_size": 44, "color": "#FFFFFF", "text_align": "center", "line_height": 1.3}})
ops.append(notes_op)
print(json.dumps({"page_index": 32 + n, "page_id": pid, "ops": ops, "after": after}, ensure_ascii=False))
