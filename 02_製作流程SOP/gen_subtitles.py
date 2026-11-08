# -*- coding: utf-8 -*-
"""從逐字稿的「逐字稿＋分鏡」表產生字幕（SRT）與逐鏡字幕斷行。

用法：
  python3 gen_subtitles.py 04_腳本庫/A-15-北歐Yule之夜的狼與神駒-逐字稿-v1.md
  python3 gen_subtitles.py <逐字稿.md> --width 16 --out 輸出資料夾

輸出（預設與逐字稿同資料夾的 _字幕/）：
  {編號}_字幕.srt        依每鏡秒數、按字數比例分配時間
  {編號}_逐鏡字幕.csv    每鏡一列：鏡號、起訖秒、斷好行的字幕（給 Canva 逐頁放字用）

支援的表格寫法：
  | 鏡頭 | 秒 | 旁白（逐字） | …        秒＝數字
  | **01** S | 0–12s（12） | 旁白 | …    秒＝括號內數字
  | 時間 | 旁白（逐字） | …             時間＝「00–04s」
  | 鏡 | 秒數 | 旁白（逐字） | 字卡 | …  v0 初稿格式
"""
import argparse, csv, os, re, unicodedata

PUNCT_BREAK = '，。；：！？、'


def disp_len(s):
    """CJK 與全形算 1，其餘（拉丁字母、數字、空白）算 0.55。"""
    n = 0.0
    for ch in s:
        n += 1.0 if unicodedata.east_asian_width(ch) in 'WF' else 0.55
    return n


def clean(cell):
    s = re.sub(r'\*\*|〔[^〕]*〕', '', cell)
    s = re.sub(r'<[^>]+>', '', s)
    return s.strip()


def parse_secs(cell):
    c = clean(cell)
    m = re.search(r'[（(](\d+(?:\.\d+)?)[)）]', c)
    if m:
        return float(m.group(1))
    m = re.match(r'^(\d+(?:\.\d+)?)\s*[–\-~～]\s*(\d+(?:\.\d+)?)\s*s?', c)
    if m:
        return float(m.group(2)) - float(m.group(1))
    m = re.match(r'^(\d+(?:\.\d+)?)', c)
    return float(m.group(1)) if m else None


def find_table(md):
    lines = md.split('\n')
    start = next((i for i, l in enumerate(lines) if l.startswith('## 逐字稿')), None)
    if start is None:
        raise SystemExit('找不到「## 逐字稿」段落')
    rows = []
    for l in lines[start + 1:]:
        if l.startswith('## '):
            break
        if l.startswith('|'):
            rows.append([c.strip() for c in l.strip().strip('|').split('|')])
    if len(rows) < 3:
        raise SystemExit('逐字稿表格太短')
    head, body = rows[0], [r for r in rows[2:] if len(r) >= len(rows[0]) - 1]
    vo = next(i for i, h in enumerate(head) if '旁白' in h)
    sec = next((i for i, h in enumerate(head) if h in ('秒', '秒數') or '秒' in h and '字/秒' not in h), None)
    if sec is None:
        sec = next(i for i, h in enumerate(head) if '時間' in h)
    shot = 0
    return head, body, vo, sec, shot


def wrap(text, width):
    """先依標點切句，再把過長的句子切成 ≤ width 的行；不在拉丁單字中間斷。"""
    parts, buf = [], ''
    for ch in text:
        buf += ch
        if ch in PUNCT_BREAK:
            parts.append(buf)
            buf = ''
    if buf.strip():
        parts.append(buf)
    lines = []
    for p in parts:
        p = p.strip()
        p = p.rstrip('，、；：。') if len(p) > 1 else p  # 字幕慣例：行尾不留逗號句號
        while disp_len(p) > width:
            cut, acc = 0, 0.0
            for i, ch in enumerate(p):
                acc += disp_len(ch)
                if acc > width:
                    break
                cut = i + 1
            # 往回找空白，避免切斷外文單字
            sp = p.rfind(' ', 0, cut)
            if sp > cut * 0.5 and re.match(r'[A-Za-z]', p[cut:cut + 1] or ' '):
                cut = sp
            lines.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            lines.append(p)
    return [l for l in lines if l and l not in ('——',)]


def fmt_ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('md')
    ap.add_argument('--width', type=int, default=16, help='每行最多幾個全形字（預設 16）')
    ap.add_argument('--lines', type=int, default=2, help='每張字幕最多幾行（預設 2）')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    md = open(a.md, encoding='utf-8').read()
    ep = '-'.join(os.path.basename(a.md).split('-')[:2])  # A-15、H-七夕、B-03
    head, body, vo, sec, shot = find_table(md)
    out = a.out or os.path.join(os.path.dirname(a.md), '_字幕')
    os.makedirs(out, exist_ok=True)
    t, n, srt, rows = 0.0, 0, [], []
    for r in body:
        text = clean(r[vo])
        d = parse_secs(r[sec]) if sec < len(r) else None
        if not text or d is None:
            continue
        lines = wrap(text, a.width)
        cards = [lines[i:i + a.lines] for i in range(0, len(lines), a.lines)]
        total = sum(disp_len(''.join(c)) for c in cards) or 1
        t0 = t
        for c in cards:
            dur = d * disp_len(''.join(c)) / total
            n += 1
            srt.append(f'{n}\n{fmt_ts(t)} --> {fmt_ts(t + dur)}\n' + '\n'.join(c) + '\n')
            t += dur
        t = t0 + d
        rows.append([clean(r[shot]), f'{t0:.1f}', f'{t:.1f}', '\n'.join(lines)])
    with open(os.path.join(out, f'{ep}_字幕.srt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt))
    with open(os.path.join(out, f'{ep}_逐鏡字幕.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['鏡', '起(秒)', '迄(秒)', '字幕（已斷行）'])
        w.writerows(rows)
    print(f'{ep}: {len(rows)} 鏡、{n} 張字幕、總長 {t:.1f} 秒 → {out}')


if __name__ == '__main__':
    main()
