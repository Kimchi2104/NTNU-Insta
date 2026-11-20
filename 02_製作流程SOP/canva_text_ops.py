# -*- coding: utf-8 -*-
"""萬國星空｜Canva 逐頁「字卡＋字幕」的 add_text ops（規格見 Canva逐頁文字放置規格.md，版型 A）

用法：
  python3 canva_text_ops.py X-08 --pages 2,3 --ids 2=PBxxx,3=PByyy
輸出 JSON：{頁: {"add": [add_text ops…], "format": [{"after": 第幾個 add, "formatting": {…}}…]}}
add_text 送出後，用回傳的 locator 依序補 format_text（"after" 是 add 的序號，從 0 起）。

字卡：鏡頭清單 card 欄，放在該鏡「第一次出現」的那一頁（頁名含「鏡頭NN」）。上方 Y 300、寬 960、白字 72 置中。
字幕：該頁 Canva頁面參數.json 的 notes（旁白），斷行 ≤16 字，下方 Y 1330、寬 960、白字 44、行高 1.3 置中。
概念圖頁（有 overlay）只放字卡，不放字幕。
"""
import os, re, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canva_ops
from gen_subtitles import wrap

CODE = re.compile(r"鏡頭(\d+[a-z]?(?:\.\d+)?)")


def plan(ep):
    d = canva_ops.folder(ep)
    pages = json.load(open(os.path.join(d, f"{ep}_Canva頁面參數.json"), encoding="utf-8"))
    shots = {s["code"]: s for s in json.load(open(os.path.join(d, f"{ep}_鏡頭清單.json"), encoding="utf-8"))}
    seen, cards = set(), {}
    for p in pages:
        for c in CODE.findall(p["title"]):
            if c not in seen:
                seen.add(c)
                if shots.get(c, {}).get("card") and p["page"] not in cards:
                    cards[p["page"]] = shots[c]["card"]
    return pages, cards


def text_ops(pg, pid, card):
    add, fmt = [], []
    if card:
        add.append({"type": "add_text", "page_id": pid, "text": card, "left": 60, "top": 300, "width": 960})
        fmt.append({"font_size": 72, "color": "#FFFFFF", "text_align": "center", "line_height": 1.2})
    if pg.get("notes") and not pg.get("overlay"):
        lines = wrap(pg["notes"], 16)
        add.append({"type": "add_text", "page_id": pid, "text": "\n".join(lines), "left": 60, "top": 1330, "width": 960})
        fmt.append({"font_size": 44, "color": "#FFFFFF", "text_align": "center", "line_height": 1.3})
    return {"add": add, "format": [dict(after=i, formatting=f) for i, f in enumerate(fmt)]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--pages", default="")
    ap.add_argument("--ids", default="")
    a = ap.parse_args()
    pages, cards = plan(a.ep)
    by = {p["page"]: p for p in pages}
    ids = dict(kv.split("=") for kv in a.ids.split(",") if kv)
    out = {}
    for n in [int(x) for x in a.pages.split(",") if x]:
        out[n] = text_ops(by[n], ids.get(str(n), f"<page {n}>"), cards.get(n))
    print(json.dumps(out, ensure_ascii=False))
