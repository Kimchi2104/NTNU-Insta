# -*- coding: utf-8 -*-
"""卡 04 子代理用：印出指定內容頁（第 n 頁＝逐頁製作表的頁號）要送的兩批 ops。
用法：/usr/bin/python3 gen_batch.py 7,8,9      （page id 讀 page_ids.txt：每行「頁號=PBxxxx」）
輸出 JSON：{頁號: {"page_index": 設計裡的頁序, "ops1": [...], "after": {"mountain": 山 crop op 樣板, "texts": [{"text":..., "formatting":{...}}...]}}}
ops1 一次送進 edit-design（page_index＝設計裡的頁序）；回傳後依 after 補 crop_media 與 format_text。"""
import os, sys, csv, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "02_製作流程SOP"))
import canva_ops as C

EP = "A-36"
D = os.path.dirname(HERE)
pages = {p["page"]: p for p in json.load(open(os.path.join(D, f"{EP}_Canva頁面參數.json"), encoding="utf-8"))}
rows = {int(r["頁"]): r for r in csv.DictReader(open(os.path.join(D, f"{EP}_Canva逐頁製作表.csv"), encoding="utf-8-sig"))}
labs = list(csv.DictReader(open(os.path.join(D, f"{EP}_逐頁標籤座標.csv"), encoding="utf-8-sig")))
media = json.load(open(os.path.join(D, f"{EP}_Canva媒體ID.json"), encoding="utf-8"))
ids = dict(l.strip().split("=") for l in open(os.path.join(HERE, "page_ids.txt")) if "=" in l)
OFFSET = 1   # 內容頁 n 在設計裡＝封面之後 → 頁序 n+1（reorder 完成後）


def subtitle_lines(t, n=16):
    parts = [s for s in re.split(r"(?<=[，。；：！？、])", t) if s]
    out = []
    for s in parts:
        s = s.strip()
        while len(s) > n:
            out.append(s[:n]); s = s[n:]
        if s: out.append(s)
    out = [re.sub(r"[，。、；：]$", "", l) for l in out]
    return out


def build(n):
    pg, pid, r = pages[n], ids[str(n)], rows[n]
    pl = [l for l in labs if int(l["頁"]) == n]
    ops = C.page_ops(pg, pid, media, pl)
    notes_op = ops.pop()                      # 備註放最後
    texts = [{"text": it["text"], "formatting": {"font_size": int(it["size"]), "color": it["color"],
              "text_align": it["align"], "line_height": 1.2}} for it in C.label_items(pl)]
    ov = bool(pg.get("overlay"))
    full = ov and pg["overlay"][0]["height"] > 1500
    card = (r["字卡"] or "").strip()
    vo = (r["旁白（本頁起播）"] or "").strip()
    if card and not ov:
        ops.append({"type": "add_text", "page_id": pid, "text": card, "left": 60, "top": 300, "width": 960})
        texts.append({"text": card, "formatting": {"font_size": 72, "color": "#ffffff", "text_align": "center", "line_height": 1.2}})
    if vo and not ov:
        big = len(vo) <= 48                      # 長旁白縮小字級（32px、每行 22 字），避免十幾行壓到標籤與山
        fs = 44 if big else 32
        lines = subtitle_lines(vo, 16 if big else 22)
        top = round(1600 - len(lines) * fs * 1.3, 1)
        ops.append({"type": "add_text", "page_id": pid, "text": "\n".join(lines), "left": 60, "top": top, "width": 960})
        texts.append({"text": "\n".join(lines), "formatting": {"font_size": fs, "color": "#ffffff", "text_align": "center", "line_height": 1.3}})
    ops.append(notes_op)
    return {"page_index": n + OFFSET, "page_id": pid, "ops1": ops,
            "after": {"mountain_crop": {"type": "crop_media", "locator_id": "<山的 locator>", "left": 0, "top": 0,
                                        "width": C.MOUNT["width"], "height": C.MOUNT["height"]},
                      "format_texts": texts}}

if __name__ == "__main__":
    print(json.dumps({n: build(n) for n in [int(x) for x in sys.argv[1].split(",")]}, ensure_ascii=False))
