# -*- coding: utf-8 -*-
"""卡 04 子代理用：依 _卡04進度/page_ids.txt 產生「某一頁」的 edit-design ops（含字卡、字幕、標籤、備註）

  python3 canva_batch_ops.py {EP} build {頁號}                      → 這一頁的 ops（JSON，直接貼進 edit-design）
  python3 canva_batch_ops.py {EP} fmt   {頁號} {山id} {文字id…}      → 該頁的 crop_media＋format_text（id 取自 build 回傳 document 裡的元素 id，
                                                                     山＝山的剪影那個 rect；文字依 add_text 的順序）
  python3 canva_batch_ops.py {EP} info  {頁號}                      → 設計頁序（page_index）、page id、頁名
page_ids.txt：每行  頁號<TAB>page_id<TAB>設計頁序(page_index)
"""
import os, sys, csv, json, re, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import canva_ops as C

def load(ep):
    d = C.folder(ep)
    P = {p["page"]: p for p in json.load(open(f"{d}/{ep}_Canva頁面參數.json", encoding="utf-8"))}
    media = json.load(open(f"{d}/{ep}_Canva媒體ID.json", encoding="utf-8"))
    labs = list(csv.DictReader(open(f"{d}/{ep}_逐頁標籤座標.csv", encoding="utf-8-sig")))
    tab = {int(r["頁"]): r for r in csv.DictReader(open(f"{d}/{ep}_Canva逐頁製作表.csv", encoding="utf-8-sig"))}
    ids = {}
    for ln in open(f"{d}/_卡04進度/page_ids.txt", encoding="utf-8"):
        t = ln.strip().split("\t")
        if len(t) >= 3 and t[0].isdigit(): ids[int(t[0])] = (t[1], int(t[2]))
    return P, media, labs, tab, ids

def sub_lines(t, n=16):
    parts = [x for x in re.split(r"(?<=[，。；：！？、])|(?<=——)", t) if x]
    out = []
    for s in parts:
        s = s.rstrip("，。；：、")
        if len(s) > n:
            k = math.ceil(len(s) / n); sz = math.ceil(len(s) / k)
            i = 0
            while i < len(s):            # 不在外文單字中間斷行（放置規格）
                j = min(i + sz, len(s))
                while 0 < j < len(s) and j > i + 1 and s[j - 1].isascii() and s[j - 1].isalnum() and s[j].isascii() and s[j].isalnum():
                    j -= 1
                if j <= i + 1: j = min(i + sz, len(s))
                out.append(s[i:j].strip()); i = j
        elif s: out.append(s)
    return "\n".join(out)

def build(ep, n):
    P, media, labs, tab, ids = load(ep)
    pg = P[n]; pid = ids[n][0]
    ops = C.page_ops(pg, pid, media, [l for l in labs if int(l["頁"]) == n])
    note = ops.pop(); r = tab[n]; conc = bool(pg.get("overlay"))
    if not conc and r["字卡"].strip():
        ops.append({"type": "add_text", "page_id": pid, "text": r["字卡"].strip(), "left": 60, "top": 300, "width": 960})
    if r["旁白（本頁起播）"].strip():
        ops.append({"type": "add_text", "page_id": pid, "text": sub_lines(r["旁白（本頁起播）"]), "left": 60, "top": 1330, "width": 960})
    ops.append(note); return ops

def fmt(ep, n, els):
    P, media, labs, tab, ids = load(ep)
    pg = P[n]; pid = ids[n][0]; r = tab[n]; conc = bool(pg.get("overlay"))
    items = [] if (pg.get("overlay") and pg.get("panel")) else C.label_items([l for l in labs if int(l["頁"]) == n])
    ops = [C.mountain_crop(f"{pid}-{els[0]}")]; k = 1
    for it in items: ops.append(C.label_format(f"{pid}-{els[k]}", it)); k += 1
    if not conc and r["字卡"].strip():
        ops.append({"type": "format_text", "locator_id": f"{pid}-{els[k]}", "formatting": {"font_size": 72, "color": "#ffffff", "text_align": "center", "line_height": 1.2, "font_weight": "bold"}}); k += 1
    if r["旁白（本頁起播）"].strip():
        ops.append({"type": "format_text", "locator_id": f"{pid}-{els[k]}", "formatting": {"font_size": 44, "color": "#ffffff", "text_align": "center", "line_height": 1.3}}); k += 1
    assert k == len(els), f"文字元素數不符：需要 {k - 1} 個文字 id（山 id 之後），給了 {len(els) - 1}"
    return ops

if __name__ == "__main__":
    ep, cmd, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if cmd == "build": out = build(ep, n)
    elif cmd == "fmt": out = fmt(ep, n, sys.argv[4:])
    else:
        P, _, _, _, ids = load(ep); out = {"page_id": ids[n][0], "page_index": ids[n][1], "title": P[n]["title"]}
    print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
