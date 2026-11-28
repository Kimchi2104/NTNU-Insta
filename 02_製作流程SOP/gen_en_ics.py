# -*- coding: utf-8 -*-
"""萬國星空｜英文版節目表 → 行事曆檔（.ics）

讀 06_發布月曆/節目表_萬國星空_英文版.csv，每一集出一個活動（發布日 21:00 台灣時間，30 分鐘），
寫到 06_發布月曆/萬國星空_英文版發布月曆.ics。給 Google 日曆／Apple 行事曆匯入，再從那裡帶進 TimeTree。

用法：
  python3 02_製作流程SOP/gen_en_ics.py            # 重出 .ics
  python3 02_製作流程SOP/gen_en_ics.py --print    # 只印活動清單，不寫檔

英文節目表的日期有改，就重跑一次。每個活動的 UID 固定（wsc-en16@…），
Google 日曆重新匯入同一個檔會更新原本的活動，不會多出一份。
"""
import csv, datetime, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
SRC = P("06_發布月曆", "節目表_萬國星空_英文版.csv")
ZH = P("06_發布月曆", "節目表_萬國星空_全年.csv")
OUT = P("06_發布月曆", "萬國星空_英文版發布月曆.ics")
TZ_OFFSET = 8            # 台灣 UTC+8，沒有日光節約時間
MINUTES = 30


def read(path):
    rows = list(csv.reader(io.StringIO(open(path, encoding="utf-8-sig", newline="").read())))
    return {c: i for i, c in enumerate(rows[0])}, rows[1:]


def esc(s):
    """RFC 5545 TEXT：反斜線、分號、逗號、換行要跳脫"""
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    """每行最多 75 個位元組（UTF-8），超過就折行；不能切在多位元組字中間"""
    out, cur, n = [], "", 0
    for ch in line:
        b = len(ch.encode("utf-8"))
        if n + b > (75 if not out else 74):
            out.append(cur)
            cur, n = "", 0
        cur += ch
        n += b
    out.append(cur)
    return "\r\n ".join(out)


def short_name(ep, title):
    """短名：素材資料夾名底線後面那段（跟進度板一樣）；節慶集（H-）集號本身就是名字"""
    import glob
    if ep.startswith("H-"):
        return ""
    d = sorted(glob.glob(P("05_素材", f"{ep}_*")))
    if d and "_" in os.path.basename(d[0]):
        return os.path.basename(d[0]).split("_", 1)[1]
    return re.split(r"[：:｜]", title)[0] if title else ""


def build():
    h, rows = read(SRC)
    zh_h, zh_rows = read(ZH)
    zh_title = {r[0]: r[zh_h["標題（工作名）"]] for r in zh_rows if r and r[0]}
    stamp = datetime.date.today().strftime("%Y%m%dT000000Z")
    events, listing = [], []
    for r in rows:
        if not (r and r[0].startswith("EN")):
            continue
        en, zh = r[0].strip(), r[h["對應中文集"]].strip()
        m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", r[h["發布日（台灣）"]])
        hh, mm = (int(x) for x in (r[h["時間（台灣）"]] or "21:00").split(":"))
        start = datetime.datetime(int(m[1]), int(m[2]), int(m[3]), hh, mm) - datetime.timedelta(hours=TZ_OFFSET)
        end = start + datetime.timedelta(minutes=MINUTES)
        full = zh_title.get(zh, "")
        short = short_name(zh, full)
        title = f"萬國星空 {en}｜{zh} {short}".rstrip() + "（英文版發布）"
        hook = r[h["英文鉤子（第一張字卡）"]].strip()
        desc = [r[h["英文標題（工作名）"]].strip()]
        if hook and not hook.startswith("（"):
            desc.append(f"Hook: {hook}")
        desc += [f"對應中文集：{zh} {full}".strip(),
                 f"長度：{r[h['長度目標']].strip()}　發布時間：{hh:02d}:{mm:02d}（台灣）",
                 f"檔期：{r[h['檔期理由']].strip()}",
                 "平台：Facebook、Instagram、YouTube、Threads",
                 "日期以 GitHub 的英文節目表為準：06_發布月曆/節目表_萬國星空_英文版.csv"]
        ev = ["BEGIN:VEVENT",
              f"UID:wsc-{en.lower()}@ntnu-astro-wsc",
              f"DTSTAMP:{stamp}",
              f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
              f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
              f"SUMMARY:{esc(title)}",
              f"DESCRIPTION:{esc(chr(10).join(desc))}",
              "CATEGORIES:萬國星空,英文版",
              "TRANSP:TRANSPARENT",
              "END:VEVENT"]
        events.append((start, ev))
        listing.append((start + datetime.timedelta(hours=TZ_OFFSET), title))
    events.sort(key=lambda e: e[0])
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//NTNU Astronomy Club//World Sky Cultures EN//ZH-TW",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:萬國星空 英文版發布", "X-WR-TIMEZONE:Asia/Taipei"]
    for _, ev in events:
        lines += ev
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n", sorted(listing)


if __name__ == "__main__":
    text, listing = build()
    wd = "一二三四五六日"
    for t, title in listing:
        print(f"{t:%Y/%m/%d}（{wd[t.weekday()]}）{t:%H:%M}  {title}")
    if "--print" not in sys.argv:
        with open(OUT, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"\n✓ 寫入 {os.path.relpath(OUT, ROOT)}（{len(listing)} 個活動）", file=sys.stderr)
