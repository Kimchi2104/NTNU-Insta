# -*- coding: utf-8 -*-
"""進度板：從 repo 裡的檔案算出每一集走到哪一步、下一步要貼什麼，寫成 06_發布月曆/進度板.md。

用法（在 repo 裡任何地方）：
  python3 02_製作流程SOP/進度.py          # 印出並寫檔
  python3 02_製作流程SOP/進度.py --print  # 只印不寫檔

判斷規則＝開工指令/README.md 第二節（看檔案，不看記憶）；步驟編號＝開工指令/00_循環.md。
改這個檔沒有用：它每次都從檔案重算。
"""
import csv, datetime, glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
TODAY = datetime.date.today()


def read_csv(path):
    rows = list(csv.reader(io.StringIO(open(path, encoding="utf-8-sig").read())))
    return rows[0], [r for r in rows[1:] if r and r[0].strip()]


def col(h, prefix):
    for i, c in enumerate(h):
        if c.startswith(prefix):
            return i
    raise KeyError(prefix)


def date_of(s):
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", s or "")
    return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def script_ver(ep):
    vs = []
    for f in glob.glob(P("04_腳本庫", f"{ep}-*-逐字稿-v*.md")):
        m = re.search(r"-v(\d+)\.md$", f)
        if m:
            vs.append(int(m.group(1)))
    return max(vs) if vs else None


def reviews(ep):
    kao = bool(glob.glob(P("04_腳本庫", "_審稿", f"{ep}_考據_*.md")))
    n = len(glob.glob(P("04_腳本庫", "_審稿", f"{ep}_審稿-*.md")))
    return kao, n


def asset_dir(ep):
    d = sorted(glob.glob(P("05_素材", f"{ep}_*")))
    return d[0] if d else None


def media(ep):
    d = asset_dir(ep)
    if not d:
        return None
    for f in glob.glob(os.path.join(d, "**", f"{ep}_Canva媒體ID.json"), recursive=True):
        try:
            return json.load(open(f, encoding="utf-8"))
        except Exception:
            return None
    return None


def short_name(ep, title):
    d = asset_dir(ep)
    if d:
        base = os.path.basename(d)
        if "_" in base:
            return base.split("_", 1)[1]
    t = title.split("｜")[-1]
    return re.split(r"[：:]", t)[0].strip()


def en_ver(en):
    vs = []
    for f in glob.glob(P("04_腳本庫", "_英文版", f"{en}-*-v*.md")):
        m = re.search(r"-v(\d+)\.md$", f)
        if m:
            vs.append(int(m.group(1)))
    return max(vs) if vs else None


# ---------- 中文 ----------
def zh_row(ep, title, date_s, status):
    v = script_ver(ep)
    kao, n = reviews(ep)
    ad = asset_dir(ep)
    m = media(ep)
    canva = bool(m and m.get("design_id")) or bool(re.search(r"Canva\s*(完成|「)", status))
    d = date_of(date_s)
    short = "" if ep.startswith("H-") else short_name(ep, title)
    missing = []
    if v is None:
        step, nxt = "①", f"卡 01｜Opus high｜`集號：{ep}`"
    elif v == 0:
        need = []
        if not kao:
            need.append(f"考據：對 Antigravity 說「做 {ep} 考據」")
        missing = [r for r in ROLES
                   if not glob.glob(P("04_腳本庫", "_審稿", f"{ep}_審稿-{r}_*.md"))]
        if missing:
            need.append("還差審稿角色 " + "、".join(f"{ROLES.index(r) + 1} {r}" for r in missing)
                        + f"：各開一個對話說「做 {ep}，角色 N」")
        if need:
            step, nxt = "②③", "送審：" + "；".join(need) + "；Antigravity 交件後自動 push"
        else:
            step, nxt = "⑤", f"卡 02｜Opus high｜`集號：{ep}`"
    elif not ad:
        step, nxt = "⑥", f"卡 03｜Opus medium｜`集號：{ep}`"
    elif not canva:
        name = f"{ep} {short}".strip()
        step, nxt = "⑦⑧", f"你：複製上一集中文設計 → 「{name}」；卡 04｜Sonnet medium｜`集號：{ep}　Canva 設計名：{name}`"
    else:
        step, nxt = "⑨", "收尾、發布（手工）"
    hold = re.search(r"【暫緩[^】]*】", status)          # 節目表狀態欄寫【暫緩…】＝先不要照進度板開卡
    if hold:
        step, nxt = "暫緩", hold.group(0)
    published = d is not None and d < TODAY          # 過了發布日就當作已播，不管節目表狀態欄有沒有更新
    return dict(ep=ep, title=title, date=d, date_s=d.strftime("%Y/%m/%d") if d else date_s[:12], v=v, kao=kao, n=n,
                assets=bool(ad), canva=canva, step=step, nxt=nxt, short=short, published=published, status=status,
                missing=missing, need_kao=(v == 0 and not kao))


ROLES = ("天文", "文化", "敘事", "語言")


def missing_md(zh):
    """送審缺件：每一行就是要貼給 Antigravity 的一句話（一句一個對話）。"""
    far = datetime.date(2100, 1, 1)
    rows = sorted([r for r in zh.values() if not r["published"] and r["step"] == "②③"], key=lambda r: r["date"] or far)
    out = ["## 送審缺件（每一行貼給 Antigravity 一個新對話；句型見根目錄 `AGENTS.md`）", ""]
    if not rows:
        out.append("沒有缺件。")
        return out
    for r in rows:
        if r["need_kao"]:
            out.append(f"- 做 {r['ep']} 考據")
    out.append("")
    for i, role in enumerate(ROLES, 1):
        eps = [r["ep"] for r in rows if role in r["missing"]]
        if not eps:
            continue
        out.append(f"**角色 {i} {role}**（缺 {len(eps)} 集；一個對話最多三集）")
        for k in range(0, len(eps), 3):
            out.append(f"- 做 {'、'.join(eps[k:k + 3])}，角色 {i}")
        out.append("")
    return out


# ---------- 英文 ----------
def en_row(en, zh, date_s, note, zh_rows):
    v = en_ver(en)
    rev = os.path.exists(P("04_腳本庫", "_審稿", f"{en}_審稿_gemini.md"))
    m = media(zh)
    encanva = bool(m and m.get("en", {}).get("design_id"))
    z = zh_rows.get(zh)
    zhname = f"{zh} {z['short']}".strip() if z else zh
    paused = "暫緩" in (note or "")
    if v is None:
        if z and (z["v"] or 0) >= 1 and z["assets"]:
            step, nxt = "Ⓐ", f"卡 05｜Opus medium｜`中文集號：{zh}`"
        else:
            step, nxt = "等中文", "等中文到 ⑤⑥"
    else:
        todo = []
        if not rev:
            todo.append("Ⓑ 送 Gemini：`04_英文審稿.md`＋EN v0＋中文定稿（Antigravity 做會自動 push）")
        elif v == 0:
            todo.append(f"Ⓕ 卡 06｜Sonnet medium｜`英文集號：{en}`")
        if not encanva:
            todo.append(f"ⒹⒺ 你：中文 ⑨ 後複製 → 「{en} {zhname}」；卡 07｜Sonnet medium｜`英文集號：{en}　Canva 設計名：{en} {zhname}`")
        if todo:
            step, nxt = "進行中", "；".join(todo)
        else:
            step, nxt = "Ⓖ", "收尾、發布（手工）"
    return dict(en=en, zh=zh, date_s=date_s[:10], date=date_of(date_s), v=v, rev=rev, encanva=encanva,
                step=step, nxt=nxt, paused=paused, started=v is not None or encanva)


def build():
    h, rows = read_csv(P("06_發布月曆", "節目表_萬國星空_全年.csv"))
    i_t, i_d, i_s = col(h, "標題"), col(h, "建議發布"), col(h, "狀態")
    zh = {}
    for r in rows:
        ep = r[0].strip()
        if not re.match(r"^(A|X|H|B|C)-", ep):
            continue
        zh[ep] = zh_row(ep, r[i_t], r[i_d], r[i_s])
    h2, rows2 = read_csv(P("06_發布月曆", "節目表_萬國星空_英文版.csv"))
    i_zh, i_date, i_note = col(h2, "對應中文集"), col(h2, "發布日"), col(h2, "備註")
    en = [en_row(r[0].strip(), r[i_zh].strip(), r[i_date], r[i_note], zh) for r in rows2 if r[0].startswith("EN")]
    return zh, en


def md(zh, en):
    out = []
    out.append(f"# 進度板（{TODAY.isoformat()} 由 `02_製作流程SOP/進度.py` 從檔案算出）")
    out.append("")
    out.append("> 步驟編號見 `02_製作流程SOP/開工指令/00_循環.md`；每張卡結束、每次交件 push 之後重跑就會更新。改這個檔沒有用。")
    out.append("")
    far = datetime.date(2100, 1, 1)
    active = sorted([r for r in zh.values() if not r["published"]], key=lambda r: r["date"] or far)
    # 現在先做
    out.append("## 現在先做")
    out.append("")
    claude = [r for r in active if r["step"] in ("①", "⑤", "⑥", "⑦⑧")]
    send = [r for r in active if r["step"] == "②③"]
    human = [r for r in active if r["step"] == "⑨"]
    for r in claude[:2]:
        out.append(f"- **下一個 Claude 對話**：{r['ep']} {r['short']}（{r['date_s']}）→ {r['nxt']}")
    for r in [r for r in active if r["step"] == "暫緩"]:
        out.append(f"- **暫緩（不要開卡）**：{r['ep']} {r['short']} → {r['nxt']}")
    if send:
        out.append("- **送審**：" + "、".join(f"{r['ep']}（{r['step']}）" for r in send[:4]) + " → 照 `外包任務書/README.md`，Antigravity 交件後自動 push")
    if human:
        out.append("- **你收尾／發布**：" + "、".join(f"{r['ep']}（{r['date_s']}）" for r in human[:6]))
    en_now = [r for r in en if r["started"] and r["step"] not in ("Ⓖ",)]
    if en_now:
        out.append("- **英文（只收尾巴）**：" + "；".join(f"{r['en']} → {r['nxt']}" for r in en_now[:3]))
    out.append("")
    out.extend(missing_md(zh))
    out.append("")
    # 中文表
    out.append("## 中文集（未播出的）")
    out.append("")
    out.append("| 集 | 發布 | 稿 | 審稿 | 素材 | Canva | 步 | 下一步 |")
    out.append("|---|---|---|---|---|---|---|---|")
    for r in active:
        v = "—" if r["v"] is None else f"v{r['v']}"
        rv = ("考據✓" if r["kao"] else "考據—") + f"／審{r['n']}"
        out.append(f"| {r['ep']} {r['short']} | {r['date_s']} | {v} | {rv} | {'✓' if r['assets'] else '—'} | {'✓' if r['canva'] else '—'} | {r['step']} | {r['nxt']} |")
    done = [r for r in zh.values() if r["published"]]
    out.append("")
    out.append(f"已過發布日（不列）：{len(done)} 集（{'、'.join(r['ep'] for r in sorted(done, key=lambda r: r['date'] or far))}）。")
    out.append("")
    # 英文表
    out.append("## 英文集")
    out.append("")
    out.append("| EN | 中文 | 發布 | 英文稿 | Gemini | EN Canva | 步 | 下一步 |")
    out.append("|---|---|---|---|---|---|---|---|")
    shown = [r for r in en if r["started"] or not r["paused"]]
    for r in shown:
        v = "—" if r["v"] is None else f"v{r['v']}"
        out.append(f"| {r['en']} | {r['zh']} | {r['date_s']} | {v} | {'✓' if r['rev'] else '—'} | {'✓' if r['encanva'] else '—'} | {r['step']} | {r['nxt']} |")
    paused = [r for r in en if r["paused"] and not r["started"]]
    if paused:
        out.append("")
        out.append(f"暫緩（中文優先）：{paused[0]['en']}～{paused[-1]['en']} 共 {len(paused)} 集，中文做到 A-22 後重排。")
    out.append("")
    return "\n".join(out)


def main():
    zh, en = build()
    if "--missing" in sys.argv:                      # 只印送審缺件（給 Antigravity 的「缺什麼」）
        print("\n".join(missing_md(zh)))
        return
    text = md(zh, en)
    print(text)
    if "--print" not in sys.argv:
        open(P("06_發布月曆", "進度板.md"), "w", encoding="utf-8").write(text + "\n")
        print(f"\n✓ 寫入 06_發布月曆/進度板.md", file=sys.stderr)


if __name__ == "__main__":
    main()
