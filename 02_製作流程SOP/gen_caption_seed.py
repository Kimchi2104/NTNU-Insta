# -*- coding: utf-8 -*-
"""萬國星空｜發布文案起稿：把逐字稿裡現成的 Caption／首留言／聯盟版三段，整理成一集一個 .md 初稿

來源：
  中文 IG  ← 04_腳本庫/{集}-…-逐字稿-v{最新}.md 的「Caption 建議」＋「首留言」
            （七夕、A-01–A-04、A-06 這六集舊片的原 Caption 有已知錯誤，改用 聯盟重貼文案.md 的更正版）
  聯盟 FB  ← 同一份逐字稿的「聯盟版文案」；舊片 11 篇 ← 06_發布月曆/聯盟重貼文案.md
  英文 IG  ← 04_腳本庫/_英文版/EN{nn}-…-v{最新}.md 的「Caption」

整理時做的事：去掉 Markdown 記號；拿掉講「怎麼算的」的字（軟體名、自算、行星亮度公式）；
知識點段落（📚）在字數內併進文案，放不下的留在首留言；資料來源一定留著。
寫到 06_發布月曆/文案/{中文IG｜聯盟FB｜英文IG}/{集號}.md，狀態標「初稿」。

用法：
  python3 02_製作流程SOP/gen_caption_seed.py            # 只補還沒有的檔
  python3 02_製作流程SOP/gen_caption_seed.py A-22 EN16  # 只做這幾集
  python3 02_製作流程SOP/gen_caption_seed.py --force    # 重寫所有「初稿」；已潤稿的不會動
之後跑 gen_caption_docx.py 檢查並組成 docx。
"""
import glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_caption_docx as C

P, ROOT = C.P, C.ROOT
BODY_MAX = 1900          # 中文 IG：知識點併進文案後的字數上限（留一點給發文的人加字）
OLD_FIXED = ["H-七夕", "A-01", "A-02", "A-03", "A-04", "A-06"]   # IG 文案改用聯盟更正版的舊集
# 聯盟重貼文案.md 的篇序 → 集號、原訂發文時間
BACKLOG = {1: ("H-七夕", "2026/11/01（日）20:00"), 2: ("A-01", "2026/11/03（二）20:00"),
           3: ("A-02", "2026/11/08（日）20:00"), 4: ("B-02", "2026/11/10（二）20:00"),
           5: ("A-03", "2026/11/15（日）20:00"), 6: ("A-04", "2026/11/17（二）20:00"),
           7: ("A-06", "2026/11/22（日）20:00"), 8: ("A-05", "2026/11/24（二）12:00"),
           9: ("A-07", "2026/11/29（日）20:00"), 10: ("B-03", "2026/12/01（二）20:00"),
           11: ("A-08", "2026/12/06（日）20:00")}

TOOL = r"(?:PyEphem(?:\s*[\d.]+)?|Skyfield|Python)"
HAS_METHOD = re.compile(rf"{TOOL}|自算|重算|Mallama")
# 整句照換（清除規則處理不了、要改寫的句子）；左邊是逐字稿原文
OVERRIDES = [
    ("📚 **1905 年的晨星，算的細節**：PyEphem 計算，", "📚 **1905 年的晨星**："),
    ("🔭 **我們自己算的**（PyEphem，Majene 3.54°S）：", "🔭 **在曼達爾看**（Majene 3.54°S）："),
    ("🔭 **計算**：最低那顆北斗星的下中天高度（PyEphem，歲差）——", "🔭 **數字**：最低那顆北斗星的下中天高度——"),
    ("（Hipparcos 視差以餘弦定理重算）", "（依 Hipparcos 視差）"),
    ("我們用 Stellarium 收錄的 Delporte 邊界表（B1875.0，357 段）重算了面積與台灣可見度：",
     "依 Stellarium 收錄的 Delporte 邊界表（B1875.0，357 段）："),
    ("我們用 PyEphem（計入大角自行）推算西元前 700 年的阿斯克拉：", "推算西元前 700 年的阿斯克拉（計入大角自行）："),
    ("——我們用 PyEphem 算，7/5 金星、木星清晨相距約 2.4°", "——那年 7/5 清晨，金星、木星相距約 2.4°"),
    ("四千五百年來在季節裡往後移了一個多月：PyEphem 算，前 2500 年", "四千五百年來在季節裡往後移了一個多月：前 2500 年"),
    ("（我們用 PyEphem 算，西元前 2500 年參宿一", "（西元前 2500 年參宿一"),
    ("2026–27 自算 11/29 → 1/12–14", "2026–27 年是 11/29 → 1/12–14"),
    ("片中登封的影長曲線是依北緯 34.4° 自算的", "片中登封的影長曲線依北緯 34.4° 畫"),
    ("自算 2026 年檀香山（PyEphem，含大氣折射）：", "2026 年檀香山："),
    ("以 PyEphem 計算 Sedilo 8 月中：", "Sedilo 8 月中："),
    ("我們用 PyEphem 算 Sedilo：", "在 Sedilo："),
    ("Mallama & Hilton (2018) 星等 −2.55", "星等 −2.55"),
    ("天象為 PyEphem 自算（台北 2027/4/16 20:00；恆星黃道用 Lahiri 值）", "天象依台北 2027/4/16 20:00"),
    ("（Stellarium 各版本自算；Ruelle 是", "（依 Stellarium 各版本的連線數；Ruelle 是"),
    ("📚 **我們怎麼算「晚了一個多月」**：用 PyEphem 找每年第一個「太陽在地平線下 9.5–10.5° 時，天狼星已經升到 1°」的早晨，"
     "這個標準先用 Censorinus 的 139 年校準（孟斐斯得 7/20–21）。結果：",
     "📚 **「晚了一個多月」怎麼來的**：以「太陽在地平線下約 10° 時，天狼星已經升到 1°」的第一個早晨為準"
     "（先用 Censorinus 記的 139 年校準，孟斐斯得 7/20–21）："),
    ("大圓距離自算 4,355 km", "大圓距離約 4,355 km"),
    ("（見 A-07 蒙古篇 v2）", "（見蒙古篇）"),
    ("⚠️ 但兩者說的「地動」不一樣", "📌 但兩者說的「地動」不一樣"),
    ("站名表見逐字稿。", ""),
    ("暗星都被月光蓋掉。PyEphem 計算，含大氣折射。", "暗星都被月光蓋掉。"),
    ("下一篇：⟪依當時 IG 進度填⟫", "下一篇（12/11 週五）：阿拉伯半島——Thurayya 與沙漠的雨季。"),
    ("距離依 Hipparcos 新歸算（van Leeuwen 2007）", "資料來源：距離依 Hipparcos 新歸算（van Leeuwen 2007）"),
    ("流星雨資料取自 IMO 2026 年曆。", "資料來源：流星雨取自 IMO 2026 年曆。"),
    ("；流星雨依 IMO 2026 年曆。實際場地不同會差幾分鐘。", "。實際場地不同會差幾分鐘。資料來源：流星雨依 IMO 2026 年曆。"),
    ("> 天象以 PyEphem 計算（台北）；星曆與星名取自 Stellarium 阿拉伯半島星空文化", "> 資料來源：星曆與星名取自 Stellarium 阿拉伯半島星空文化"),
]
# 首留言裡沒有獨立的出處段、聯盟版也借不到的集數：補一行（內容都取自該集現有的文字）
EXTRA_SRC = {
    "A-07": "資料來源：Stellarium mongolian 星空文化；蒙古語辭典與民俗文獻；J. Elverskog〈The Mongolian Big Dipper Sūtra〉（JIABS 29.1，2006）。",
    "A-08": "資料來源：Stellarium siberian 星空文化；А. Ф. Анисимов（埃文基宇宙觀）；Ю. Е. Березкин「宇宙追獵」母題索引；Hagar 1900（米克馬克）；S. T. Emlen 1970（Science 170）。",
}
DROP_PARA = re.compile(r"^(?:>\s*)?(?:📚\s*)?\*\*(?:今晚|今天)的數字\*\*[：:].*(?:自算|PyEphem)")   # 整段只在講「數字怎麼算的」
INTERNAL = re.compile(r"^(?:>\s*)?（以節目表發布日寫的時刻")       # 給發文的人看的提醒，移到備註
FILLER = re.compile(rf"{TOOL}|Mallama\s*&\s*Hilton|[（(]?2018[)）]?|自算|重算|計算|推算|大圓公式|含大氣折射|歲差|地心|"
                    r"日月行星與升落時刻|星曆與距離|天象與幾何|天象與農曆|升起時刻|掩星時刻|月亮位置|行星亮度|行星星等|木星星等|"
                    r"天象|星曆|方位|時刻|影長|座標|台北|以上|都|與|以|用|依|由|為|的|算|[，、；：:／\s※]")


def unmd(s):
    """Markdown → 可以直接貼的純文字"""
    s = re.sub(r"\\([#_+*~\-.\[\]()])", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\((?:https?://)?[^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"\*(?=\S)([^*\n]+?)(?<=\S)\*(?![A-Za-z])", r"\1", s)
    return s


def split_top(s, seps):
    """照 seps 切開，但不切括號裡面的；回傳 [(片段, 後面接的分隔符)]"""
    out, cur, depth = [], "", 0
    for ch in s:
        if ch in "（(":
            depth += 1
        elif ch in "）)":
            depth = max(0, depth - 1)
        if ch in seps and depth == 0:
            out.append((cur, ch))
            cur = ""
        else:
            cur += ch
    out.append((cur, ""))
    return out


def method_only(s):
    """拿掉軟體名、「計算」之類的字和括號之後什麼都不剩＝這一段只在講怎麼算"""
    t = s
    while re.search(r"[（(][^（）()]*[)）]", t):
        t = re.sub(r"[（(][^（）()]*[)）]", "", t)
    return not FILLER.sub("", t)


def clean_paren(m):
    """括號裡提到算法的：只拿掉那幾個字，其餘留著；全拿光就整個括號不要"""
    inner = m.group(1)
    if not HAS_METHOD.search(inner):
        return m.group(0)
    keep = []
    for tok in re.split(r"[，；]", inner):
        t = tok.strip()
        t = re.sub(rf"^{TOOL}\s*(?:自算|計算|歲差計算|地心)?\s*[：:]?\s*", "", t)
        t = re.sub(r"^(?:我們|大圓)?自算\s*[：:]?\s*", "", t)
        t = re.sub(r"(?:自算|重算)$", "", t).strip()
        if t and not method_only(t):
            keep.append(t)
    return f"（{'，'.join(keep)}）" if keep else ""


def clean_method(text):
    """回傳 (清過的文字, 移到備註的提醒)"""
    for a, b in OVERRIDES:
        text = text.replace(a, b)
    notes, out = [], []
    for line in text.split("\n"):
        if INTERNAL.match(line.strip()):
            notes.append("文中的日期與時刻是照節目表發布日寫的；改天發，請跟流程對話說一聲，換成當天的數字。")
            continue
        if DROP_PARA.match(line.strip()):
            continue
        if not HAS_METHOD.search(line):
            out.append(line)
            continue
        line = re.sub(r"（([^（）]*)）", clean_paren, line)
        line = re.sub(rf"我們用\s*{TOOL}\s*算了一下[：:，]\s*", "", line)
        line = re.sub(rf"我們用\s*{TOOL}\s*(?:算|計算)[，：:]\s*", "", line)
        line = re.sub(rf"(?<![\w]){TOOL}\s*(?:算|計算)，\s*", "", line)
        line = re.sub(r"(?:^|(?<=[。；\s]))(?:我們)?自算[：:]\s*", "", line)
        sents = []
        for sent, dot in split_top(line, "。"):
            if not HAS_METHOD.search(sent):
                sents.append(sent + dot)
                continue
            head = re.match(r"\s*(?:[📚🔭📌※]\s*)?(?:\*\*[^*]+\*\*\s*)?(?:[^：:；，。（）]{0,8}[：:])?", sent).group(0)
            body = sent[len(head):] if re.search(r"\*\*|^[\s]*[📚🔭📌]", head) or head.strip().endswith(("：", ":")) else sent
            if body is sent:
                head = ""
            parts = [(c, sep) for c, sep in split_top(body, "；") if not (HAS_METHOD.search(c) and method_only(c))]
            # 一個子句裡用逗號接的「…，行星亮度用 Mallama…」也拿掉
            kept = []
            for c, sep in parts:
                if HAS_METHOD.search(c):
                    sub = [x for x, _ in split_top(c, "，") if not (HAS_METHOD.search(x) and method_only(x))]
                    c = "，".join(sub)
                if c.strip():
                    kept.append(c)
            if kept:
                sents.append(head + "；".join(kept) + dot)
        line = "".join(sents).rstrip()
        if line.strip() and not re.fullmatch(r"\s*(?:[📚🔭📌※]\s*)?(?:\*\*[^*]+\*\*)?[：:]?\s*", line):
            out.append(line)
    return "\n".join(out), notes


def latest_zh(ep):
    fs = glob.glob(P("04_腳本庫", f"{ep}-*逐字稿-v*.md"))
    return sorted(fs, key=lambda f: int(re.search(r"-v(\d+)\.md$", f)[1]))[-1] if fs else None


def latest_en(en):
    fs = glob.glob(P("04_腳本庫", "_英文版", f"{en}-*-v*.md"))
    return sorted(fs, key=lambda f: int(re.search(r"-v(\d+)\.md$", f)[1]))[-1] if fs else None


def section(text, pat):
    hs = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r"^## (.+)$", text, re.M)]
    for i, (s, e, h) in enumerate(hs):
        if re.search(pat, h):
            return text[e:hs[i + 1][0] if i + 1 < len(hs) else len(text)]
    return ""


def paras(body):
    """一段 Markdown → 一行一段的清單。有引言（>）就只取引言，否則取全部非空行"""
    lines = [l.rstrip() for l in body.replace("\r\n", "\n").split("\n")]
    if any(l.lstrip().startswith(">") for l in lines):
        lines = [re.sub(r"^\s*>\s?", "", l) for l in lines if l.lstrip().startswith(">")]
    out = []
    for l in lines:
        l = l.strip()
        if not l or l == "---" or l.startswith("###"):
            continue
        out.append(re.sub(r"^[-*]\s+", "・", l))
    return out


def is_tags(l):
    return len(re.findall(r"#[^\s#]+", l)) >= 3 and not re.sub(r"#[^\s#]+", "", l).strip()


def is_source(l):
    return bool(re.match(r"\s*(?:[📚※]\s*)?(?:\*\*)?(?:本集)?(?:出處|資料來源|資料|來源|參考文獻|星名出處|星官資料|星名與故事出處)", l))


def is_footer(l):
    return bool(re.match(r"\s*(?:⭐\s*)?(?:明天|明晚|下週|下一集|下集|EP\s*\d+|8/21 首播)", l)) or "｜" in l and bool(re.search(r"EP\s*\d+\s*下週|下週[一二三四五六日]", l))


def write(kind, ep, title, cap, fc, notes, src, post=None, force=False):
    path = C.path_of(kind, ep)
    if os.path.exists(path):
        old = C.parse(path)
        if not old["狀態"].startswith("初稿") or not force:
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    head = [f"# {ep}｜{title}", "> 狀態：初稿（腳本從現有稿整理，還沒潤稿）", f"> 來源：{src}"]
    if post:
        head.append(f"> 發文：{post}")
    body = head + ["", "## 文案", "", cap.strip(), "", "## 首留言", "", fc.strip() or "無", "", "## 備註", ""]
    body += [f"・{n}" for n in dict.fromkeys(notes)] or ["無"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(body).rstrip() + "\n")
    return True


def backlog_sections():
    t = open(P("06_發布月曆", "聯盟重貼文案.md"), encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## 第 (\d+) 篇｜[^\n]*\n(.*?)(?=^## |\Z)", t, re.S | re.M):
        body = m.group(2)
        quoted = [re.sub(r"^\s*>\s?", "", l).strip() for l in body.split("\n") if l.lstrip().startswith(">")]
        extra = [l.strip() for l in body.split("\n") if l.strip() and not l.lstrip().startswith(">")]
        out[int(m.group(1))] = (quoted, extra)
    return out


def tidy_fb(lines):
    """聯盟文案：一行裡擠了好幾段的拆開；清單編號留著"""
    out, marks = [], "🪐🌌✨🔴🌅🌙☄"
    for l in lines:
        l = re.sub(r"\\([#_+])", r"\1", l)
        l = re.sub(r"\s+(?=(?:下一篇|「萬國星空」是師大天文社的科普系列|#萬國星空|補充：|時刻以|（台北計算))", "\n", l)
        if sum(l.count(m) for m in marks) >= 2:          # 一行裡排了好幾個時刻 → 一個一行
            l = re.sub(rf"\s+(?=[{marks}])", "\n", l)
        l = re.sub(r"\s+(?=・\d)", "\n", l)
        out += [x.strip() for x in l.split("\n") if x.strip()]
    return out


def seed_fb(e, backlog, force):
    ep = e["id"]
    num = next((n for n, (x, _) in BACKLOG.items() if x == ep), None)
    notes = []
    if num:
        quoted, extra = backlog[num]
        text, n2 = clean_method("\n".join(tidy_fb(quoted)))
        post = BACKLOG[num][1]
        notes += n2 + [f"舊片補貼：原訂 {post} 發。文中「現在抬頭看得到嗎」的日期與時刻是照這一天寫的；改天發要換數字（跟流程對話說一聲）。"]
        notes += [unmd(x) for x in extra]
        src = "06_發布月曆/聯盟重貼文案.md 第 %d 篇" % num
    else:
        f = latest_zh(ep)
        body = section(open(f, encoding="utf-8").read(), r"^聯盟版") if f else ""
        if not body.strip():
            return None
        text, n2 = clean_method("\n".join(paras(clean_method(body)[0])))
        n2 = clean_method(body)[1]
        notes += n2
        post, src = None, os.path.relpath(f, ROOT) + "「聯盟版文案」"
    lines = [l for l in unmd(text).split("\n") if l.strip()]
    if not any("#萬國星空" in l for l in lines):
        lines.append("#萬國星空 #師大天文社")
    return write("fb", ep, e["title"], "\n".join(lines), "", notes, src, post, force)


def seed_zh(e, backlog, force):
    ep = e["id"]
    f = latest_zh(ep)
    if not f:
        return None
    t = open(f, encoding="utf-8").read()
    cap_lines = paras(section(t, r"^Caption"))
    fc_lines = paras(section(t, r"^首留言|^考據備忘（首留言可用）"))
    notes, src = [], os.path.relpath(f, ROOT) + "「Caption 建議」「首留言」"
    tags = next((l for l in cap_lines if is_tags(l)), "#萬國星空 #師大天文社")
    if ep in OLD_FIXED:
        num = next(n for n, (x, _) in BACKLOG.items() if x == ep)
        quoted, _ = backlog[num]
        keep = []
        for l in tidy_fb(quoted):
            if re.match(r"現在抬頭看得到嗎|下一篇|「萬國星空」是師大天文社的科普系列|#萬國星空", l):
                continue
            keep.append(re.sub(r"\s*（本片原發布於師大天文社粉專；片中的「今晚」指原發布當晚。）", "", l))
        text = unmd(clean_method("\n".join(keep))[0])
        notes.append("這一集已經發過。原本的 IG 文案有錯（見文中「更正」），這裡是更正版，可以拿來編輯原貼文的文案。")
        src = "06_發布月曆/聯盟重貼文案.md 第 %d 篇（更正版）" % num
        return write("zh", ep, e["title"], text + "\n" + tags, "", notes, src, None, force)
    if not cap_lines:
        return None
    body = [l for l in cap_lines if not is_tags(l)]
    foot = [l for l in body if is_footer(l)]
    body = [l for l in body if l not in foot]
    know = [l for l in fc_lines if not is_source(l)]
    srcs = [l for l in fc_lines if is_source(l)]
    if not srcs:                                  # 首留言沒有出處段 → 借聯盟版的資料來源行
        srcs = [l for l in paras(clean_method(section(t, r"^聯盟版"))[0]) if is_source(l)][:1]
    if not srcs and ep in EXTRA_SRC:
        srcs = [EXTRA_SRC[ep]]
    clean = lambda ls: [x for x in unmd(clean_method("\n".join(ls))[0]).split("\n") if x.strip()]
    body, foot, know, srcs = clean(body), clean(foot), clean(know), clean(srcs)
    tail = srcs + foot + [tags]
    used = sum(len(x) + 1 for x in body + tail)
    inline, rest = [], []
    for k in know:
        if not rest and used + len(k) + 1 <= BODY_MAX:
            inline.append(k)
            used += len(k) + 1
        else:
            rest.append(k)
    cap = "\n".join(body + ([""] + inline if inline else []) + [""] + tail)
    return write("zh", ep, e["title"], cap, "\n".join(rest), notes, src, None, force)


def seed_en(e, force):
    en = e["id"]
    f = latest_en(en)
    if not f:
        return None
    lines = paras(section(open(f, encoding="utf-8").read(), r"^Caption"))
    cap, fc = [], []
    for l in lines:
        m = re.match(r"\(First comment:\s*(?:sources?\s*[:—–-]\s*)?(.*?)\)?\s*$", l, re.I)
        if m:
            items = [x.strip() for x in re.split(r";\s*|(?<=\.)\s+(?=[A-Z])", m.group(1).rstrip(".)"))]
            items = [x for x in items if x and not re.search(r"PyEphem|computed with|calculated with", x)]
            fc.append("Sources: " + "; ".join(items).rstrip(".") + ".")
        else:
            cap.append(l)
    text, notes = unmd("\n".join(cap)), []
    return write("en", en, e["title"], text, unmd("\n".join(fc)), notes, os.path.relpath(f, ROOT) + " “Caption”", None, force)


def main():
    eps = C.episodes()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    backlog = backlog_sections()
    n = {"zh": 0, "fb": 0, "en": 0}
    for kind, fn in (("zh", lambda e: seed_zh(e, backlog, force)), ("fb", lambda e: seed_fb(e, backlog, force)),
                     ("en", lambda e: seed_en(e, force))):
        for e in eps[kind]:
            if args and e["id"] not in args:
                continue
            r = fn(e)
            if r is None and not os.path.exists(C.path_of(kind, e["id"])):
                print(f"✗ {C.KINDS[kind]['folder']}/{e['id']}：逐字稿裡沒有可以用的段落，要人寫")
            n[kind] += bool(r)
    print(f"寫了 中文IG {n['zh']}、聯盟FB {n['fb']}、英文IG {n['en']} 個初稿")


if __name__ == "__main__":
    main()
