# -*- coding: utf-8 -*-
"""萬國星空｜把 {EP}_Canva頁面參數.json 轉成 Canva 連接器（edit-design）的操作清單

給 Claude 用：每一頁輸出一批 operations，照順序送進 edit-design 即可。
媒體 ID 記在 05_素材/{集}/_v4大畫布/{EP}_Canva媒體ID.json（上傳一次、之後都讀這份）：

  {"long": [L1..L4 的 media id], "north": [...], "south": [...],
   "mountain": "MAD4KTwSGtw", "background": "MAHWs5D_MpY",
   "concept": {"C-A05-01_六連星_星點層_透明.png": "MAHW...", ...}}

用法：
  python3 canva_ops.py A-05 --pages 3,4,5 --ids 3=PBxxx,4=PByyy    # 印出這幾頁的 ops（JSON）
  python3 canva_ops.py A-05 --list                                  # 列出頁序＋每頁要放什麼

注意（Canva 連接器的脾氣，見 每集製作SOP.md 五）：
  - insert_fill 放山的剪影後，Canva 會把內圖框多裁 1px；要再送一次 crop_media（mountain_crop）
  - update_fill 換圖後內圖框會被放大；要再送一次 crop_media（fill_crop）
  - add_text 之後要用回傳的 locator 再送 format_text（label_format）
"""
import os, sys, csv, json, glob, argparse, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MOUNT = dict(left=-212.30305796440007, top=1622.4420974142777,
             width=1939.0832424885327, height=300.5579025857226)   # 團隊模板的山（全集共用）
LABEL_MIN, LABEL_MAX = 36, 96          # 原生標籤字級上下限（大特寫時標籤會算到幾百 px）


def folder(ep):
    base = os.path.dirname(HERE)
    hit = glob.glob(os.path.join(base, "05_素材", "*", "_v4大畫布", f"{ep}_畫布資訊.json"))
    if not hit:
        sys.exit(f"找不到 {ep} 的 _v4大畫布")
    return os.path.dirname(hit[0])


def text_w(t, f):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.62 for c in t) * f + 0.6 * f


def page_ops(pg, pid, media, labels=()):
    """一頁的完整 ops：背景 → 天空四層 → 山 → 原生標籤 → 概念圖框 → 概念圖 → 備註"""
    grp = {"長圖": "long", "北盤": "north", "南盤": "south"}[pg["group"]]
    ops = [{"type": "update_fill", "locator_id": pid, "asset_type": "image",
            "asset_id": media["background"], "alt_text": "背景漸層"}]
    for i, a in enumerate(media[grp], 1):
        ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image", "asset_id": a,
                    "alt_text": f"{pg['group']} L{i}", "left": pg["left"], "top": pg["top"],
                    "width": pg["width"], "height": pg["height"], "rotation": pg["rotation"]})
    ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image",
                "asset_id": media["mountain"], "alt_text": "山的剪影", **MOUNT})
    for lb in labels:
        f = min(max(int(lb["字級px"]), LABEL_MIN), LABEL_MAX)
        X, Y = int(lb["中心X px"]), int(lb["中心Y px"])
        w = round(text_w(lb["文字"], f))
        if X - w / 2 < -0.3 * w or X + w / 2 > 1080 + 0.3 * w:     # 大半在畫面外就不放
            continue
        ops.append({"type": "add_text", "page_id": pid, "text": lb["文字"],
                    "left": X - w / 2, "top": Y - 0.6 * f, "width": w})
    ov = pg.get("overlay") or []
    if ov and pg.get("panel"):
        P = pg["panel"]
        h = round(P["height"], 1)
        ops.append({"type": "insert_shape", "page_id": pid, "left": P["left"],
                    "top": round(P["top"], 1), "width": P["width"], "height": h,
                    "path": f"M0 0H{P['width']}V{h}H0Z", "view_box_width": P["width"],
                    "view_box_height": h, "color": P["color"], "opacity": P["opacity"],
                    "corner_rounding": P["radius"], "stroke_weight": 0})
    for o in ov:
        ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image",
                    "asset_id": media["concept"][o["file"]], "alt_text": o["file"][:-4],
                    "left": o["left"], "top": o["top"], "width": o["width"], "height": o["height"]})
    note = [pg["title"], f"圖層組：{pg['group']}｜W {pg['width']:.0f} H {pg['height']:.0f} "
                         f"X {pg['left']:.0f} Y {pg['top']:.0f} 旋轉 {pg['rotation']:+.1f}°",
            f"與上一頁：{pg.get('trans', '')}"]
    if pg.get("notes"):
        note.append("旁白：" + pg["notes"])
    if ov:
        note.append("概念圖：" + "＋".join(o["file"].replace("_透明.png", "") for o in ov))
    ops.append({"type": "replace_speaker_notes", "page_id": pid, "notes": "\n".join(note)})
    return ops


def mountain_crop(locator):
    return {"type": "crop_media", "locator_id": locator, "left": 0, "top": 0,
            "width": MOUNT["width"], "height": MOUNT["height"]}


def fill_crop(locator, width, height):
    return {"type": "crop_media", "locator_id": locator, "left": 0, "top": 0,
            "width": width, "height": height}


def label_format(locator, size, color):
    return {"type": "format_text", "locator_id": locator,
            "formatting": {"font_size": min(max(int(size), LABEL_MIN), LABEL_MAX),
                           "color": color, "text_align": "center", "line_height": 1.2}}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--pages", default="")
    ap.add_argument("--ids", default="", help="頁=Canva page id，逗號分隔")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    d = folder(a.ep)
    pages = {p["page"]: p for p in json.load(open(os.path.join(d, f"{a.ep}_Canva頁面參數.json"),
                                                 encoding="utf-8"))}
    if a.list:
        for n, p in pages.items():
            ov = "＋".join(o["file"] for o in p.get("overlay") or [])
            print(n, p["title"], p["group"], p.get("trans", ""), ov)
        sys.exit()
    media = json.load(open(os.path.join(d, f"{a.ep}_Canva媒體ID.json"), encoding="utf-8"))
    labs = list(csv.DictReader(open(os.path.join(d, f"{a.ep}_逐頁標籤座標.csv"),
                                    encoding="utf-8-sig")))
    ids = dict(kv.split("=") for kv in a.ids.split(",") if kv)
    out = {}
    for n in [int(x) for x in a.pages.split(",") if x]:
        out[n] = page_ops(pages[n], ids.get(str(n), f"<page {n}>"), media,
                          [lb for lb in labs if int(lb["頁"]) == n])
    print(json.dumps(out, ensure_ascii=False))
