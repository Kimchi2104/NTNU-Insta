# -*- coding: utf-8 -*-
"""卡 04 X-03：產生每一頁要送的 ops（含字卡、字幕）。用法：python3 gen_page_json.py  → pages/Pxx.json"""
import os, sys, json, csv, re
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(D, "..", "..", "02_製作流程SOP"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(D))), "02_製作流程SOP"))
import canva_ops as C

EP = "X-03"
P = {p["page"]: p for p in json.load(open(f"{D}/{EP}_Canva頁面參數.json", encoding="utf-8"))}
media = json.load(open(f"{D}/{EP}_Canva媒體ID.json", encoding="utf-8"))
labs = list(csv.DictReader(open(f"{D}/{EP}_逐頁標籤座標.csv", encoding="utf-8-sig")))
ids = {}
for l in open(f"{HERE}/page_ids.txt", encoding="utf-8"):
    if l.startswith("#") or not l.strip():
        continue
    n, idx, pid = l.split()
    ids[int(n)] = (int(idx), pid)

# 字卡（逐字稿分鏡表「字卡」欄；一頁一張，不放概念圖頁）
CARD = {1: "全世界都看見——這把勺子", 2: "十種人生",
        3: "三千年前，它一顆都不落", 4: "三千年前，它一顆都不落", 7: "三千年前，它一顆都不落",
        8: "① 牛的前腿", 9: "② 車", 10: "② 車", 11: "② 車", 12: "② 車", 13: "② 車",
        14: "③ 熊", 15: "③ 熊", 18: "③ 熊",
        19: "④ 七個人", 20: "④ 七個人", 21: "④ 七個人",
        22: "⑤ 棺架", 23: "⑤ 棺架", 24: "⑥ 強盜", 25: "⑥ 強盜",
        26: "⑦ 吞魚的大蛇", 29: "⑦ 吞魚的大蛇",
        30: "⑧ 船", 31: "⑨ 漁網", 32: "⑩ 獵物", 33: "⑩ 獵物", 35: "⑩ 獵物",
        36: "今晚八點　東北方", 37: "今晚八點　東北方", 39: "今晚八點　東北方",
        40: "下集見｜春空導航術", 41: "下集見｜春空導航術"}


def sub_lines(t, maxc=16):
    """先依全形標點切句，超過 maxc 字再切開；行尾不留逗號句號"""
    parts = [s for s in re.split(r"(?<=[，。；：！？、])", t) if s]
    out = []
    for s in parts:
        s = s.strip()
        while len(s) > maxc:
            cut = maxc
            out.append(s[:cut]); s = s[cut:]
        if s:
            out.append(s)
    # 合併：相鄰短句湊到 ≤ maxc
    merged = []
    for s in out:
        if merged and len(merged[-1]) + len(s) <= maxc:
            merged[-1] += s
        else:
            merged.append(s)
    return [re.sub(r"[，。；、]+$", "", s) for s in merged]


os.makedirs(f"{HERE}/pages", exist_ok=True)
for n in sorted(P):
    pg = P[n]
    idx, pid = ids[n]
    pl = [lb for lb in labs if int(lb["頁"]) == n]
    ops = C.page_ops(pg, pid, media, pl)
    note_op = ops.pop()            # replace_speaker_notes 放最後
    texts = []
    for it in C.label_items(pl):
        texts.append({"role": "label", "text": it["text"],
                      "format": {"font_size": int(it["size"]), "color": it["color"],
                                 "text_align": it["align"], "line_height": 1.2}})
    concept = bool(pg.get("overlay"))
    if not concept and n in CARD:
        texts.append({"role": "card", "text": CARD[n], "left": 60, "top": 300, "width": 960,
                      "format": {"font_size": 72, "color": "#ffffff", "text_align": "center", "line_height": 1.2}})
    if not concept and pg.get("notes"):
        ls = sub_lines(pg["notes"])
        h = len(ls) * 44 * 1.3
        texts.append({"role": "sub", "text": "\n".join(ls), "left": 60, "top": round(1600 - h), "width": 960,
                      "format": {"font_size": 44, "color": "#ffffff", "text_align": "center", "line_height": 1.3}})
    # 字卡、字幕的 add_text 接在標籤後面（插在概念圖框之前）
    add = [{"type": "add_text", "page_id": pid, "text": t["text"], "left": t["left"], "top": t["top"], "width": t["width"]}
           for t in texts if t["role"] != "label"]
    first_panel = next((i for i, o in enumerate(ops) if o["type"] == "insert_shape" and o.get("opacity") == 0.75), None)
    if first_panel is None:
        first_fill = [i for i, o in enumerate(ops) if o["type"] == "insert_fill" and o.get("alt_text", "").startswith("C-X03")]
        first_panel = first_fill[0] if first_fill else len(ops)
    ops[first_panel:first_panel] = add
    ops.append(note_op)
    out = {"page": n, "title": pg["title"], "canva_index_before_reorder": idx, "page_id": pid,
           "mountain_crop": {"left": 0, "top": 0, "width": C.MOUNT["width"], "height": C.MOUNT["height"]},
           "concept_fills": [o["alt_text"] for o in ops if o["type"] == "insert_fill" and o["alt_text"].startswith("C-X03")],
           "texts_in_insert_order": [{"text": t["text"], "format": t["format"]} for t in texts],
           "ops": ops}
    json.dump(out, open(f"{HERE}/pages/P{n:02d}.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("ok", len(P))
