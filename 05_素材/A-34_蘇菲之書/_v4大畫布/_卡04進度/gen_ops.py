import sys,json,csv,re,glob
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..','02_製作流程SOP'))
import canva_ops as co, gen_subtitles as gs
d=co.folder('A-34')
pages={p['page']:p for p in json.load(open(d+'/A-34_Canva頁面參數.json',encoding='utf-8'))}
media=json.load(open(d+'/A-34_Canva媒體ID.json',encoding='utf-8'))
labs=list(csv.DictReader(open(d+'/A-34_逐頁標籤座標.csv',encoding='utf-8-sig')))
ids={int(a):b for a,b in (l.split() for l in open(d+'/_卡04進度/page_ids.txt',encoding='utf-8') if l[0].isdigit())}
md=open(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","04_腳本庫","A-34-*v1.md"))[0],encoding='utf-8').read()
cards={}
for l in md.splitlines():
    m=re.match(r'\| \*\*(\d\d)\*\* \w \|[^|]*\|[^|]*\|([^|]*)\|',l)
    if m: cards[m.group(1)]=m.group(2).strip().replace('／','\n')
def card_for(name):
    s=re.findall(r'鏡頭(\d\d)開始',name) or re.findall(r'鏡頭(\d\d)',name)
    return cards.get(s[0],'')
def build(n):
    pg=pages[n]; pid=ids[n]
    lab=[l for l in labs if int(l['頁'])==n]
    ops=co.page_ops(pg,pid,media,lab)
    items=co.label_items(lab)
    # text extras (after notes op is fine)
    extra=[];fmt=[]
    if not pg.get('overlay'):
        c=card_for(pg['title'])
        if c: extra.append(dict(t=c,left=60,top=300,w=960,size=72,lh=1.2,bold=False))
        if pg.get('notes'):
            ls=gs.wrap(pg['notes'],16); h=57.2*len(ls)
            extra.append(dict(t='\n'.join(ls),left=60,top=round(max(1000,min(1330,1650-h))),w=960,size=44,lh=1.3))
    for e in extra:
        ops.append({"type":"add_text","page_id":pid,"text":e['t'],"left":e['left'],"top":e['top'],"width":e['w']})
    # format list in add_text order: labels then extras
    fm=[co.label_format('<LOC>',it) for it in items]+[{"type":"format_text","locator_id":"<LOC>","formatting":{"font_size":e['size'],"color":"#ffffff","text_align":"center","line_height":e['lh']}} for e in extra]
    return ops,fm
if __name__=='__main__':
    n=int(sys.argv[1]); ops,fm=build(n)
    print(json.dumps(ops,ensure_ascii=False,separators=(',',':')))
    print('FORMAT',json.dumps(fm,ensure_ascii=False,separators=(',',':')))
