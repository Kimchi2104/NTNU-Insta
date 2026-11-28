# -*- coding: utf-8 -*-
"""萬國星空｜發布文案：檢查、列待辦、組成 docx

一集一個 .md（06_發布月曆/文案/{中文IG｜聯盟FB｜英文IG}/{集號}.md），這支腳本把它們
依發文日排好，組成三份 Word 檔，放在 06_發布月曆/文案/：
  萬國星空_中文IG文案.docx、萬國星空_FB聯盟文案.docx、萬國星空_英文IG文案.docx

用法：
  python3 02_製作流程SOP/gen_caption_docx.py                    # 檢查全部＋重出三份 docx
  python3 02_製作流程SOP/gen_caption_docx.py --check A-22 EN16  # 只檢查這幾集，不出 docx
  python3 02_製作流程SOP/gen_caption_docx.py --missing          # 列出還是初稿的集數（一行一句，可直接貼給代理）

每個 .md 的格式（任務書 外包任務書/05_發布文案.md 有說明）：
  # {集號}｜{標題}
  > 狀態：初稿／已潤稿（誰、哪天）
  > 來源：…
  > 發文：2026/11/29（日）20:00      ← 選填；發文日跟節目表不同時才寫（聯盟舊片補貼）
  ## 文案      可以整段複製貼上的純文字
  ## 首留言    選填；沒有就寫「無」
  ## 備註      選填；給發文的人看，不會貼出去

初稿由 gen_caption_seed.py 從逐字稿整理出來。需要 python-docx：pip install python-docx
"""
import csv, datetime, io, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
DIR = P("06_發布月曆", "文案")
KINDS = {
    "zh": dict(folder="中文IG", docx="萬國星空_中文IG文案.docx", title="萬國星空｜中文版 Instagram 文案", en=False),
    "fb": dict(folder="聯盟FB", docx="萬國星空_FB聯盟文案.docx", title="萬國星空｜臺灣業餘天文聯盟（Facebook 社團）文案", en=False),
    "en": dict(folder="英文IG", docx="萬國星空_英文IG文案.docx", title="World Sky Cultures｜English Instagram captions", en=True),
}
NO_FB = {"B-01"}                 # 秋觀行前預報不發聯盟
IG_LIMIT = 2200                  # Instagram 文案與留言的字數上限
BATCH = 4                        # --missing 一句列幾集
FAR = datetime.date(2100, 1, 1)

# 不該出現在貼文裡的字：製作過程、內部用語
BANNED = [r"PyEphem", r"Skyfield", r"\bephem\b", r"自算", r"重算", r"程式算", r"經計算", r"Python",
          r"calculated with", r"computed with", r"逐字稿", r"鏡頭\s*\d", r"圖層", r"Canva", r"待查核", r"⚠",
          r"\bv[0-9]\b", r"C-[A-Z]\d{2}-\d{2}", r"Mallama", r"⟪"]
SOFT = [r"我們算", r"算了一下", r"我們用.{0,12}算"]      # 提醒：看一下是不是在講怎麼算的


def read_csv(path):
    rows = list(csv.reader(io.StringIO(open(path, encoding="utf-8-sig", newline="").read())))
    return {c: i for i, c in enumerate(rows[0])}, rows[1:]


def date_of(s):
    m = re.match(r"\s*(\d{4})/(\d{1,2})/(\d{1,2})", s or "")
    return datetime.date(int(m[1]), int(m[2]), int(m[3])) if m else None


def episodes():
    """回傳 {kind: [dict(id, title, when, date)]}，依節目表發布日排序（沒有日期的排最後）"""
    h, rows = read_csv(P("06_發布月曆", "節目表_萬國星空_全年.csv"))
    zh = [dict(id=r[0].strip(), title=r[h["標題（工作名）"]].strip(), when=r[h["建議發布"]].strip(),
               date=date_of(r[h["建議發布"]])) for r in rows if r and re.match(r"[A-Z]-", r[0])]
    h2, rows2 = read_csv(P("06_發布月曆", "節目表_萬國星空_英文版.csv"))
    en = [dict(id=r[0].strip(), title=f"{r[h2['英文標題（工作名）']].strip()}（{r[h2['對應中文集']].strip()}）",
               when=f"{r[h2['發布日（台灣）']].strip()} {r[h2['時間（台灣）']].strip()}",
               date=date_of(r[h2["發布日（台灣）"]])) for r in rows2 if r and r[0].startswith("EN")]
    key = lambda e: (e["date"] or FAR, e["id"])
    return {"zh": sorted(zh, key=key), "fb": sorted([dict(e) for e in zh if e["id"] not in NO_FB], key=key),
            "en": sorted(en, key=key)}


def path_of(kind, ep):
    return os.path.join(DIR, KINDS[kind]["folder"], f"{ep}.md")


def parse(path):
    t = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    sec = {"文案": "", "首留言": "", "備註": ""}
    head = re.search(r"^# (.+)$", t, re.M)
    for name in sec:
        m = re.search(rf"^## {name}[^\n]*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
        if m:
            sec[name] = m.group(1).strip("\n").rstrip()
    for name in ("首留言", "備註"):
        if sec[name].strip() in ("無", "（無）", "none", "None", "-"):
            sec[name] = ""
    sec["標題"] = head.group(1).strip() if head else ""
    for name in ("狀態", "來源", "發文"):
        m = re.search(rf"^> {name}：(.+)$", t, re.M)
        sec[name] = m.group(1).strip() if m else ""
    return sec


def is_draft(kind, ep):
    p = path_of(kind, ep)
    return not os.path.exists(p) or parse(p)["狀態"].startswith("初稿")


def check(kind, ep, sec):
    """回傳 [(級別, 訊息)]；級別 ✗＝要改、△＝提醒"""
    out, cap, fc = [], sec["文案"], sec["首留言"]
    both = cap + "\n" + fc
    if not sec["標題"]:
        out.append(("✗", "第一行要有「# 集號｜標題」"))
    if not sec["狀態"]:
        out.append(("✗", "少了「> 狀態：…」那一行"))
    if not cap.strip():
        return out + [("✗", "「## 文案」是空的")]
    if kind != "fb":
        for name, txt in (("文案", cap), ("首留言", fc)):
            if len(txt) > IG_LIMIT:
                out.append(("✗", f"{name} {len(txt)} 字，超過 Instagram 上限 {IG_LIMIT}"))
            elif len(txt) > IG_LIMIT - 100:
                out.append(("△", f"{name} {len(txt)} 字，快到上限 {IG_LIMIT}"))
    tags = re.findall(r"#[^\s#]+", cap)
    if kind == "fb":
        if fc.strip():
            out.append(("✗", "聯盟版沒有首留言，內容全部放文案"))
        if sorted(tags) != ["#師大天文社", "#萬國星空"]:
            out.append(("✗", f"聯盟版的 hashtag 只留 #萬國星空 #師大天文社（現在是 {' '.join(tags) or '沒有'}）"))
        if re.match(r"\s*(?:師大天文社|我們|本社|大家好)", cap):
            out.append(("✗", "聯盟版第一句要講天空，不講社團"))
    else:
        if not 5 <= len(tags) <= 12:
            out.append(("✗", f"hashtag 有 {len(tags)} 個，要 5–12 個"))
        for n in (["#WorldSkyCultures"] if kind == "en" else ["#萬國星空", "#師大天文社"]):
            if n not in tags:
                out.append(("✗", f"少了 {n}"))
    if not re.search(r"Sources?:" if kind == "en" else r"資料來源|出處|資料：", both):
        out.append(("✗", "沒有資料來源（英文寫 Sources:，中文寫「資料來源：」）"))
    for pat in BANNED:
        m = re.search(pat, both)
        if m:
            out.append(("✗", f"出現不該貼出去的字「{m.group(0)}」（製作過程或內部用語）"))
    for pat in SOFT:
        m = re.search(pat, both)
        if m:
            out.append(("△", f"「{m.group(0)}」：如果是在講怎麼算的，改成直接講結果"))
    if re.search(r"^\s*>", both, re.M) or "**" in both or "`" in both or re.search(r"^\s*[-*] ", both, re.M):
        out.append(("✗", "還有 Markdown 記號（>、**、`、行首的 - ），貼文要純文字"))
    if kind == "en" and re.search(r"[一-鿿]", cap):
        out.append(("△", "英文文案裡有中文字（星名原文可以留，其餘要翻）"))
    return out


def order_missing(eps, ids):
    """還沒潤的集數：還沒發的排前面（照發布日），已經發過的排後面"""
    today = datetime.date.today()
    by = {e["id"]: e for e in eps}
    up = [i for i in ids if (by[i]["date"] or FAR) >= today]
    return up, [i for i in ids if i not in up]


def missing_cmds(eps):
    out = []
    zh = [e["id"] for e in eps["zh"] if is_draft("zh", e["id"]) or (e["id"] not in NO_FB and is_draft("fb", e["id"]))]
    en = [e["id"] for e in eps["en"] if is_draft("en", e["id"])]
    for label, ids, lst, unit in (("中文集", zh, eps["zh"], "每集潤中文 IG＋聯盟 FB 兩個檔"), ("英文集", en, eps["en"], "每集一個檔")):
        up, past = order_missing(lst, ids)
        out.append(f"## {label}：還有 {len(ids)}／{len(lst)} 集是初稿（{unit}）")
        if up:
            out.append("還沒發的（照發布日，先做前面的）：")
            out += [f"- 做文案 {'、'.join(up[i:i + BATCH])}" for i in range(0, len(up), BATCH)]
        if past:
            out.append("已經發過的（補檔用，不急）：")
            out += [f"- 做文案 {'、'.join(past[i:i + BATCH])}" for i in range(0, len(past), BATCH)]
        out.append("")
    return out


def stable_zip(data, out):
    """重新打包成固定時間戳的 zip：內容沒變，檔案就一個位元組都不變（git 不會每次都說有改）"""
    src = zipfile.ZipFile(io.BytesIO(data))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for name in src.namelist():
            zi = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            dst.writestr(zi, src.read(name))


def build_docx(kind, eps):
    from docx import Document
    from docx.shared import Cm, Pt, RGBColor
    from docx.enum.text import WD_BREAK
    from docx.oxml.ns import qn
    cfg = KINDS[kind]
    L = dict(cap="Caption（文案）", fc="First comment（首留言）", note="備註（不貼出去）", pub="發布", n="字元",
             draft="初稿", done="已潤稿") if cfg["en"] else \
        dict(cap="文案", fc="首留言", note="備註（不貼出去）", pub="發文", n="字", draft="初稿", done="已潤稿")
    doc = Document()
    fixed = datetime.datetime(2026, 1, 1)
    doc.core_properties.created = doc.core_properties.modified = fixed
    doc.core_properties.author, doc.core_properties.title = "NTNU Astronomy Club", cfg["title"]
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft JhengHei")
    items, todo = [], []
    for e in eps[kind]:
        p = path_of(kind, e["id"])
        if not os.path.exists(p):
            todo.append(e["id"])
            continue
        sec = parse(p)
        items.append((date_of(sec["發文"]) or e["date"] or FAR, e["id"], sec["發文"] or e["when"], sec))
    items.sort(key=lambda x: (x[0], x[1]))
    drafts = [i[1] for i in items if i[3]["狀態"].startswith("初稿")]
    doc.add_heading(cfg["title"], 0)
    doc.add_paragraph(f"共 {len(eps[kind])} 集，這份檔裡有 {len(items)} 集（{L['done']} {len(items) - len(drafts)}、{L['draft']} {len(drafts)}），依發文日排序。")
    doc.add_paragraph("用法：每一集的「" + L["cap"] + "」整段複製貼上；有「" + L["fc"] + "」的，發布後立刻貼在第一則留言。"
                      "「初稿」是從逐字稿現成的段落整理的，可以直接用；「已潤稿」是再順過一次的版本。"
                      "要改字請改 06_發布月曆/文案/ 裡對應的 .md，再重出這份檔。")
    if todo:
        doc.add_paragraph("還沒有檔：" + "、".join(todo))
    state_of = lambda sec: L["draft"] if sec["狀態"].startswith("初稿") else L["done"]
    table = doc.add_table(rows=1, cols=3)
    table.style = "Light Grid Accent 1"
    for c, txt in zip(table.rows[0].cells, (L["pub"], "集數", "狀態")):
        c.text = txt
    for _, ep, when, sec in items:
        cells = table.add_row().cells
        cells[0].text, cells[1].text, cells[2].text = when, sec["標題"] or ep, state_of(sec)
    table.autofit = False
    for row in table.rows:
        for cell, cm in zip(row.cells, (4.6, 9.4, 1.8)):
            cell.width = Cm(cm)
    for _, ep, when, sec in items:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading(sec["標題"] or ep, 1)
        tags = len(re.findall(r"#[^\s#]+", sec["文案"]))
        meta = doc.add_paragraph(f"{L['pub']}：{when}　｜　{len(sec['文案'])} {L['n']}　｜　hashtag {tags}　｜　{state_of(sec)}")
        meta.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        for name, label in (("文案", L["cap"]), ("首留言", L["fc"]), ("備註", L["note"])):
            if not sec[name].strip():
                continue
            doc.add_heading(label, 2)
            for line in sec[name].split("\n"):
                p = doc.add_paragraph(line)
                if name == "備註" and p.runs:
                    p.runs[0].italic = True
                    p.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    buf = io.BytesIO()
    doc.save(buf)
    out = os.path.join(DIR, cfg["docx"])
    stable_zip(buf.getvalue(), out)
    return out, len(items), len(drafts)


def main():
    eps = episodes()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--missing" in sys.argv:
        print("\n".join(missing_cmds(eps)))
        return 0
    bad = 0
    for kind in KINDS:
        for e in eps[kind]:
            if args and e["id"] not in args:
                continue
            p = path_of(kind, e["id"])
            if not os.path.exists(p):
                if args:
                    print(f"✗ {KINDS[kind]['folder']}/{e['id']}.md 還沒有")
                    bad += 1
                continue
            for lv, msg in check(kind, e["id"], parse(p)):
                print(f"{lv} {KINDS[kind]['folder']}/{e['id']}.md：{msg}")
                bad += lv == "✗"
    print(f"檢查完：{bad} 個要改的問題" if bad else "檢查完：沒有要改的問題")
    if "--check" in sys.argv:
        return 1 if bad else 0
    try:
        import docx  # noqa: F401
    except ImportError:
        print("沒有 python-docx，先跑：pip install python-docx", file=sys.stderr)
        return 1
    os.makedirs(DIR, exist_ok=True)
    for kind in KINDS:
        out, n, d = build_docx(kind, eps)
        print(f"✓ {os.path.relpath(out, ROOT)}（{n} 集，其中初稿 {d}）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
