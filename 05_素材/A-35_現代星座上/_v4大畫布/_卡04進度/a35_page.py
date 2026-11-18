# -*- coding: utf-8 -*-
"""卡04 A-35：印出某一頁的 ops（給子代理用）
用法：/usr/bin/python3 a35_page.py 5            → 第 5 頁的 step1 ops（一個 JSON 陣列，整段貼進 edit-design.operations）
      /usr/bin/python3 a35_page.py 5 --formats → step2 要用的格式表（text→formatting）與山的 crop 範本
"""
import sys, os, json, csv, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '02_製作流程SOP'))
import canva_ops as C
EP = 'A-35'
d = C.folder(EP)
pages = {p['page']: p for p in json.load(open(os.path.join(d, 'A-35_Canva頁面參數.json'), encoding='utf-8'))}
media = json.load(open(os.path.join(d, 'A-35_Canva媒體ID.json'), encoding='utf-8'))
labs = list(csv.DictReader(open(os.path.join(d, 'A-35_逐頁標籤座標.csv'), encoding='utf-8-sig')))
ids = dict(l.split() for l in open(os.path.join(HERE, 'page_ids.txt'), encoding='utf-8') if l.strip())
# 逐字稿：鏡 → 字卡
card = {}
for l in open(glob.glob(os.path.join(ROOT, '04_腳本庫', 'A-35-*-逐字稿-v1.md'))[0], encoding='utf-8'):
    m = re.match(r'\|\s*\*\*(\d+[a-z]?)\*\*\s*\w?\s*\|[^|]*\|[^|]*\|([^|]*)\|', l)
    if m:
        card[m.group(1)] = m.group(2).strip()
subs = {}
for r in csv.DictReader(open(os.path.join(HERE, 'A-35_逐鏡字幕.csv'), encoding='utf-8-sig')):
    subs[r['鏡'].split()[0]] = r['字幕（已斷行）']


def text_items(pg):
    t = pg['title']
    if '概念圖' in t or t.startswith('長圖轉') or t.startswith('南盤轉'):
        return []
    m = re.search(r'鏡頭(\d+[a-z]?)', t)
    if not m:
        return []
    shot = m.group(1)
    out = []
    c = card.get(shot, '')
    if c:
        out.append(dict(kind='card', text=c.replace('／', '\n'), left=60, top=300, width=960,
                        fmt=dict(font_size=72, color='#ffffff', text_align='center', line_height=1.2)))
    if pg.get('notes'):
        s = subs.get(shot, '')
        if s:
            n = s.count('\n') + 1
            out.append(dict(kind='sub', text=s, left=60, top=round(max(250, 1600 - n * 44 * 1.3)), width=960,
                            fmt=dict(font_size=44, color='#ffffff', text_align='center', line_height=1.3)))
    return out


def build(n):
    pg = pages[n]
    pid = ids[str(n)]
    lb = [x for x in labs if int(x['頁']) == n]
    ops = C.page_ops(pg, pid, media, lb)
    notes_op = ops.pop()                      # 備註放最後
    ti = text_items(pg)
    for it in ti:
        ops.append({"type": "add_text", "page_id": pid, "text": it['text'], "left": it['left'],
                    "top": it['top'], "width": it['width']})
    ops.append(notes_op)
    fm = [dict(text=i['text'], formatting=C.label_format('X', i)['formatting']) for i in C.label_items(lb)]
    fm += [dict(text=i['text'], formatting=i['fmt']) for i in ti]
    return pid, ops, fm


if __name__ == '__main__':
    n = int(sys.argv[1])
    pid, ops, fm = build(n)
    if '--formats' in sys.argv:
        print(json.dumps(dict(page_id=pid, mountain_crop=dict(type='crop_media', locator_id='<山的locator>', left=0, top=0,
                                                         width=C.MOUNT['width'], height=C.MOUNT['height']),
                              formats=fm), ensure_ascii=False))
    else:
        print(json.dumps(ops, ensure_ascii=False))
