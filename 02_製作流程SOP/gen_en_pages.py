# -*- coding: utf-8 -*-
"""英文版：從英文稿的「Beats」與「Page sequence」兩張表，產生每頁英文文字表＋SRT。

用法：
  python3 02_製作流程SOP/gen_en_pages.py 04_腳本庫/_英文版/EN01-A-11-Anuta-v0.md
輸出（到 05_素材/{集}/_英文版/，集名從英文稿檔名的中文集號找 05_素材/{集號}_*）：
  EN{nn}_Canva逐頁文字.csv   一列＝一頁：頁號、頁名、停留秒、英文字卡、英文字幕（斷好行）、位置、處理
  EN{nn}_字幕.srt            每則文字依它第一頁到最後一頁的時間

英文稿的表格格式：
  Beats:    | # | Sec | On pages | Pos | Headline | Text | w/s |
  Sequence: | Canva page | Chinese page name | Sec to next | Note |
斷行：每行 ≤ 40 個字母、不在單字中間斷；≤ 3 行塞不下就標「拆成 2 頁」。
"""
import csv, glob, os, re, sys

MAXCH, MAXLINES = 40, 3


def tables(md):
    """回傳 {表頭第一欄: [rows]}；row 是 dict"""
    out, cur, hdr = {}, None, None
    for ln in md.split("\n"):
        if not ln.startswith("|"):
            cur = hdr = None
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if hdr is None:
            hdr = cells; cur = out.setdefault(hdr[0], []); continue
        if set("".join(cells)) <= set("-: "):
            continue
        cur.append(dict(zip(hdr, cells)))
    return out


def clean(s):
    s = re.sub(r"\*\([^)]*\)\*|\*\(.*?\)\*", "", s)          # *(stage note)*
    s = re.sub(r"\*(?!manuk)", "", s)                        # markdown italics; keep *manuk
    return s.strip()


def wrap(text, maxch=MAXCH):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxch:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def srt_time(t):
    h, m = divmod(int(t), 3600); m, s = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{int(round((t - int(t)) * 1000)):03d}"


def main(path):
    md = open(path, encoding="utf-8").read()
    tb = tables(md)
    beats = [{k.split(" ")[0]: v for k, v in b.items()} for b in (tb.get("#") or [])]   # "Headline (≤ 6 words)" → "Headline"
    seq = tb.get("Canva page") or []
    if not beats or not seq:
        sys.exit("找不到 Beats（| # |）或 Page sequence（| Canva page |）表")
    name = os.path.basename(path)
    en = re.match(r"(EN\d+)-([A-Z]-\d+|H-[^-]+|X-\d+|C-\d+)", name)
    if not en:
        sys.exit("檔名要像 EN01-A-11-…")
    enid, zh = en.group(1), en.group(2)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hit = glob.glob(os.path.join(base, "05_素材", f"{zh}_*"))
    if not hit:
        sys.exit(f"找不到 05_素材/{zh}_*")
    out = os.path.join(hit[0], "_英文版"); os.makedirs(out, exist_ok=True)

    # 時間軸：每頁的起始秒
    t, start, pages = 0.0, {}, []
    for r in seq:
        p = int(r["Canva page"]); start[p] = t; pages.append(p)
        t += float(r["Sec to next"]) if re.match(r"^\d", r["Sec to next"] or "") else 0.0
    total = t
    # 每則文字 → 頁
    per_page = {p: {"頁名": r["Chinese page name"], "停留秒": r["Sec to next"], "字卡": [], "字幕": [],
                    "位置": [], "處理": r.get("Note", "")} for p, r in zip(pages, seq)}
    srt = []
    for b in beats:
        ps = [int(x) for x in re.findall(r"\d+", b.get("On", ""))]
        txt, head = clean(b["Text"]), clean(b["Headline"])
        if not ps or not (txt or head):
            continue
        lines = wrap(txt) if txt else []
        flag = "；拆成 2 頁" if len(lines) > MAXLINES else ""
        for p in ps:
            if p not in per_page:
                print(f"  ⚠ {b['#']} 用到的第 {p} 頁不在 Page sequence 裡"); continue
            if head: per_page[p]["字卡"].append(head)
            if lines: per_page[p]["字幕"].append("\n".join(lines))
            per_page[p]["位置"].append(b["Pos"])
            if flag and flag not in per_page[p]["處理"]:
                per_page[p]["處理"] += flag
        t0 = start.get(ps[0], 0.0)
        last = ps[-1]; sec = per_page.get(last, {}).get("停留秒") or ""
        t1 = start.get(last, t0) + (float(sec) if re.match(r"^\d", sec) else 3.0)
        if txt:
            srt.append((t0, t1, "\n".join(lines)))
    rows = []
    for p in pages:
        d = per_page[p]
        rows.append({"Canva頁": p, "頁名": d["頁名"], "停留秒": d["停留秒"],
                     "英文字卡": " ｜ ".join(d["字卡"]), "英文字幕": "\n\n".join(d["字幕"]),
                     "位置": "、".join(d["位置"]), "處理": d["處理"]})
    fcsv = os.path.join(out, f"{enid}_Canva逐頁文字.csv")
    with open(fcsv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
    fsrt = os.path.join(out, f"{enid}_字幕.srt")
    with open(fsrt, "w", encoding="utf-8") as f:
        for i, (a, b, s) in enumerate(srt, 1):
            f.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{s}\n\n")
    words = sum(len(clean(b["Text"]).split()) for b in beats if not b["Text"].startswith("*("))
    print(f"  ✓ {fcsv}\n  ✓ {fsrt}\n  {len(pages)} 頁、{total:.0f} 秒、約 {words} 字（{words / total:.2f} words/sec）")
    for p in pages:
        d = per_page[p]
        if "拆成" in d["處理"]:
            print(f"  ⚠ 第 {p} 頁字幕超過 {MAXLINES} 行，要拆頁")


if __name__ == "__main__":
    main(sys.argv[1])
