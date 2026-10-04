# -*- coding: utf-8 -*-
"""萬國星空｜把 {EP}_Canva頁面參數.json 轉成 Canva 連接器（edit-design）的操作清單

給 Claude 用：每一頁輸出一批 operations，照順序送進 edit-design 即可。
媒體 ID 記在 05_素材/{集}/_v4大畫布/{EP}_Canva媒體ID.json（上傳一次、之後都讀這份）：

  {"layers": {"L1-銀河": id, …, "北盤L1-銀河": id, …}   ← A-07 起（每層一個）
   或 "long": [L1..L4 的 media id], "north": [...], "south": [...]   ← A-05
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
LIST_MIN = 30                          # 名稱表（同一欄疊好幾行，例：跨文化對照）最小那一行的字級
SAFE_X = 48                            # 名稱表靠左排時的左邊界


def folder(ep):
    base = os.path.dirname(HERE)
    hit = glob.glob(os.path.join(base, "05_素材", "*", "_v4大畫布", f"{ep}_畫布資訊.json"))
    if not hit:
        sys.exit(f"找不到 {ep} 的 _v4大畫布")
    return os.path.dirname(hit[0])


def text_w(t, f):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.62 for c in t) * f + 0.6 * f


def _wrap(t, f, maxw):
    """太寬就在最靠近中間的空白折成兩行（中文名稱不折）"""
    if text_w(t, f) <= maxw or " " not in t:
        return [t]
    cut = min((i for i, c in enumerate(t) if c == " "), key=lambda i: abs(i - len(t) / 2))
    return [t[:cut], t[cut + 1:]]


def label_items(labels):
    """每個原生標籤的位置、字級、顏色、對齊（page_ops 打字、之後 format_text 都用這份）。

    一般標籤：字級夾在 36–96，以中心點置中。
    名稱表（同一個中心 X 疊 3 行以上、且原字級有小於 36 的）：直接夾到 36 會一行壓一行，
    所以整欄等比放大到最小那行 = LIST_MIN、行距跟著放大，改成靠左一欄；
    太長的（例 Seven Brothers and Their Sister）折兩行，欄的右緣不碰到它指的星。
    每行的文字框只包住自己的字：阿拉伯文等右到左的字在「靠左」框裡會貼右邊，框太寬就會跑離整欄。
    """
    by_x = {}
    for lb in labels:
        by_x.setdefault(lb["中心X px"], []).append(lb)
    stacks = {x for x, g in by_x.items()
              if len(g) >= 3 and min(int(lb["字級px"]) for lb in g) < LABEL_MIN}
    items = []
    for lb in labels:                                    # 照 CSV 順序（打字順序＝之後對 locator 的順序）
        x = lb["中心X px"]
        if x in stacks:
            if lb is by_x[x][0]:
                items += _stack(by_x[x])
            continue
        f = min(max(int(lb["字級px"]), LABEL_MIN), LABEL_MAX)
        X, Y = int(lb["中心X px"]), int(lb["中心Y px"])
        w = round(text_w(lb["文字"], f))
        if X - w / 2 < -0.3 * w or X + w / 2 > 1080 + 0.3 * w:     # 大半在畫面外就不放
            continue
        items.append(dict(text=lb["文字"], left=X - w / 2, top=Y - 0.6 * f, width=w,
                          size=f, color=lb["顏色"], align="center"))
    _unstack(items)
    return items


def _unstack(items):
    """同一錨點上下疊的兩三行（例：盤上的「星線原文／中譯」）：原字級太小、夾到 LABEL_MIN 之後
    行距不夠會一行壓一行。依中心 X 分組，行距撐到 1.2 倍字級，整組以原本的中點為中心上下攤開。"""
    groups = {}
    for it in items:
        if it["align"] != "center":
            continue
        groups.setdefault(round((it["left"] + it["width"] / 2) / 4), []).append(it)
    runs = []
    for g in groups.values():
        g.sort(key=lambda it: it["top"])
        run = [g[0]]
        for a, b in zip(g, g[1:]):          # 只攤開真的貼在一起的那幾行；同一直線上遠處的標籤不動
            if b["top"] - a["top"] < 1.5 * max(a["size"], b["size"]):
                run.append(b)
            else:
                runs.append(run)
                run = [b]
        runs.append(run)
    for g in runs:
        if len(g) < 2:
            continue
        need = [max(1.2 * a["size"], b["top"] - a["top"]) for a, b in zip(g, g[1:])]
        if all(abs(n - (b["top"] - a["top"])) < 0.5 for n, a, b in zip(need, g, g[1:])):
            continue
        mid = (g[0]["top"] + g[-1]["top"]) / 2
        tops = [0.0]
        for n in need:
            tops.append(tops[-1] + n)
        off = mid - tops[-1] / 2
        for it, t in zip(g, tops):
            it["top"] = off + t


def _stack(grp):
    grp = sorted(grp, key=lambda lb: int(lb["中心Y px"]))
    s = LIST_MIN / min(int(lb["字級px"]) for lb in grp)
    X = int(grp[0]["中心X px"])
    ref = min((int(float(lb.get("對應星X") or 1080)) for lb in grp), default=1080)
    maxw = max(min(ref - 120, 1080 - SAFE_X) - SAFE_X, 320)
    rows = []
    for lb in grp:
        f = min(round(int(lb["字級px"]) * s), LABEL_MAX)
        lines = _wrap(lb["文字"], f, maxw)
        rows.append((lb, f, lines))
    colw = max(text_w(t, f) for _, f, ls in rows for t in ls)
    left = max(SAFE_X, X - colw / 2)
    ys = [int(lb["中心Y px"]) for lb, _, _ in rows]
    yc = (ys[0] + ys[-1]) / 2
    # 行距等比放大；折行的那一格多出來的高度，上下各讓一半
    cy = [0.0]
    for i in range(1, len(rows)):
        h0 = (len(rows[i - 1][2]) - 1) * rows[i - 1][1] * 1.2 / 2
        h1 = (len(rows[i][2]) - 1) * rows[i][1] * 1.2 / 2
        cy.append(cy[-1] + (ys[i] - ys[i - 1]) * s + h0 + h1)
    off = yc - (cy[0] + cy[-1]) / 2
    out = []
    for (lb, f, lines), c in zip(rows, cy):
        Y = c + off
        out.append(dict(text="\n".join(lines), left=round(left, 1),
                        top=round(Y - len(lines) * f * 1.2 / 2, 1),
                        width=round(max(text_w(t, f) for t in lines)),
                        size=f, color=lb["顏色"], align="start"))
    return out


def page_ops(pg, pid, media, labels=()):
    """一頁的完整 ops：背景 → 天空四層 → 山 → 原生標籤 → 概念圖框 → 概念圖 → 備註"""
    ops = [{"type": "update_fill", "locator_id": pid, "asset_type": "image",
            "asset_id": media["background"], "alt_text": "背景漸層"}]
    if "layers" in media:                       # 每層各自的 media id（A-07 起：L5/L6/L7 也要放）
        sky = [(n, media["layers"][n]) for n in pg["layers"] if "標籤" not in n]
    else:                                       # A-05：只有 L1–L4
        grp = {"長圖": "long", "北盤": "north", "南盤": "south"}[pg["group"]]
        sky = [(f"{pg['group']} L{i}", a) for i, a in enumerate(media[grp], 1)]
    for nm, a in sky:
        ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image", "asset_id": a,
                    "alt_text": nm, "left": pg["left"], "top": pg["top"],
                    "width": pg["width"], "height": pg["height"], "rotation": pg["rotation"]})
    mt = pg.get("mountain_top")
    gt = mt + MOUNT["height"] - 20 if mt is not None else None
    if gt is not None and gt < 1920:            # 地平線升高：山上移，下面補地面（黑）；山在頁底以下就不用補
        ops.append({"type": "insert_shape", "page_id": pid, "left": MOUNT["left"], "top": round(gt, 1),
                    "width": MOUNT["width"], "height": round(1940 - gt, 1),
                    "path": f"M0 0H{MOUNT['width']:.1f}V{1940 - gt:.1f}H0Z",
                    "view_box_width": round(MOUNT["width"], 1), "view_box_height": round(1940 - gt, 1),
                    "color": "#000000", "stroke_weight": 0})
    ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image",
                "asset_id": media["mountain"], "alt_text": "山的剪影",
                **dict(MOUNT, top=mt if mt is not None else MOUNT["top"])})
    for it in label_items(labels):
        ops.append({"type": "add_text", "page_id": pid, "text": it["text"],
                    "left": it["left"], "top": it["top"], "width": it["width"]})
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


def c_page_ops(pg, pid, media, dels=(), new=False):
    """C 系列（概念圖定格頁）一頁的 ops：清舊元素 →（新頁才要）背景＋山 → 概念圖圖層 → 備註
    pg 來自 make_cXX_canva.py 的 {EP}_Canva頁面參數.json；沿用舊頁時保留它原本的背景與山。
    圖層 back=True（宣夜的氣、眾星）要等插入後拿到 locator，再依反序 layer_element back（見 SOP 七）。"""
    ops = [{"type": "delete_element", "locator_id": l} for l in dels]
    if new:
        ops.append({"type": "update_fill", "locator_id": pid, "asset_type": "image",
                    "asset_id": media["background"], "alt_text": "背景漸層"})
        ops.append({"type": "insert_fill", "page_id": pid, "asset_type": "image",
                    "asset_id": media["mountain"], "alt_text": "山的剪影", **MOUNT})
    for ly in pg["layers"]:
        op = {"type": "insert_fill", "page_id": pid, "asset_type": "image",
              "asset_id": media["concept"][ly["file"]],
              "alt_text": os.path.basename(ly["file"]).replace("_透明.png", "").replace(".png", ""),
              "left": ly["left"], "top": ly["top"], "width": ly["width"], "height": ly["height"]}
        if ly.get("rotation"):
            op["rotation"] = ly["rotation"]
        ops.append(op)
    names = "＋".join(os.path.basename(l["file"]).replace("_透明.png", "").replace(".png", "")
                     + (f"（{l['rotation']:+.0f}°）" if l.get("rotation") else "") for l in pg["layers"])
    note = [pg["title"], f"起 {pg['start']:.0f}s｜{pg['dur']} 秒｜與上一頁：{pg['trans']}"]
    if pg.get("vo"):
        note.append("旁白：" + pg["vo"])
    note.append("圖層：" + names)
    ops.append({"type": "replace_speaker_notes", "page_id": pid, "notes": "\n".join(note)})
    return ops


def mountain_crop(locator):
    return {"type": "crop_media", "locator_id": locator, "left": 0, "top": 0,
            "width": MOUNT["width"], "height": MOUNT["height"]}


def fill_crop(locator, width, height):
    return {"type": "crop_media", "locator_id": locator, "left": 0, "top": 0,
            "width": width, "height": height}


def label_format(locator, item):
    """add_text 之後補字級、顏色、對齊、行高（item 來自 label_items）"""
    return {"type": "format_text", "locator_id": locator,
            "formatting": {"font_size": int(item["size"]), "color": item["color"],
                           "text_align": item["align"], "line_height": 1.2}}


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
