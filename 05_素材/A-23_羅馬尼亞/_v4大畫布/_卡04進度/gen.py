import sys, json, csv, re, glob, os
sys.path.insert(0,"/home/user/NTNU-Insta/02_製作流程SOP")
import canva_ops as C
SP="/tmp/claude-0/-home-user-NTNU-Insta/c957ca03-36ef-5eb4-8eac-a76252d9bc32/scratchpad/"
d=C.folder("A-23")
P=json.load(open(d+"/A-23_Canva頁面參數.json"))
media=json.load(open(d+"/A-23_Canva媒體ID.json"))
labs=list(csv.DictReader(open(d+"/A-23_逐頁標籤座標.csv",encoding="utf-8-sig")))
ids=open(SP+"ids.txt").read().split()
assert len(ids)==104
idsB=open(SP+"idsB.txt").read().split()
ids=ids[:36]+idsB
# cards
md=open(glob.glob("/home/user/NTNU-Insta/04_腳本庫/A-23-*逐字稿-v1.md")[0],encoding="utf-8").read()
cards={}
for l in md.splitlines():
    m=re.match(r"\|\s*\*\*(\d+)\*\*\s*\w\s*\|([^|]*)\|([^|]*)\|([^|]*)\|",l)
    if m and int(m.group(1)) not in cards: cards[int(m.group(1))]=m.group(4).strip()
def subtitle(t,w=16):
    out=[]
    for s in re.split(r"(?<=[，。；：！？、])",t):
        s=s.strip()
        if not s: continue
        while s:
            if len(s)<=w: out.append(s); break
            k=w
            while k>1 and s[k-1].isascii() and s[k].isascii() and s[k-1].isalnum() and s[k].isalnum(): k-=1
            if k<=1: k=w
            out.append(s[:k]); s=s[k:]
    # merge short fragments
    lines=[];cur=""
    for s in out:
        if len(cur)+len(s)<=w: cur+=s
        else:
            if cur: lines.append(cur)
            cur=s
    if cur: lines.append(cur)
    res=[x.rstrip('，。；、：') for x in lines]
    return [x for x in res if x]
def plan(n):
    pg=P[n-1]; pid=ids[n-1]
    ops=C.page_ops(pg,pid,media,[lb for lb in labs if int(lb["頁"])==n])
    items=C.label_items([lb for lb in labs if int(lb["頁"])==n])
    extra=[]
    if pg.get("notes"):
        shots=re.findall(r"鏡頭(\d+)開始",pg["title"]); shot=int(shots[-1])
        card=cards.get(shot,"")
        if card:
            extra.append(dict(text=card,left=60,top=300,width=960,size=72,color="#ffffff",align="center",lh=1.2))
        lines=subtitle(pg["notes"])
        top=max(900,round(1600-len(lines)*44*1.3))
        extra.append(dict(text="\n".join(lines),left=60,top=top,width=960,size=44,color="#ffffff",align="center",lh=1.3))
    # insert extra add_text before replace_speaker_notes
    nt=ops.pop()
    for e in extra: ops.append({"type":"add_text","page_id":pid,"text":e["text"],"left":e["left"],"top":e["top"],"width":e["width"]})
    ops.append(nt)
    return ops,items+extra
def compact(ops):
    out=[]
    for o in ops:
        o=dict(o)
        if o["type"]=="insert_fill":
            o["alt_text"]=o["alt_text"].split("-")[0][:12]
            if o.get("rotation")==0.0: o.pop("rotation")
        for k in ("left","top","width","height"):
            if isinstance(o.get(k),float): o[k]=round(o[k],1)
        out.append(o)
    return out

if __name__=="__main__":
    a,b=int(sys.argv[1]),int(sys.argv[2])
    allops=[];meta={}
    for n in range(a,b+1):
        o,it=plan(n); allops+=o; meta[n]=it
    allops=compact(allops); json.dump(allops,open(SP+f"ops_{a}_{b}.json","w"),ensure_ascii=False,separators=(",",":"))
    json.dump(meta,open(SP+f"meta_{a}_{b}.json","w"),ensure_ascii=False)
    print(len(allops),"ops;", sum(len(v) for v in meta.values()),"texts")
