import re,glob,os,json,sys
MARK=re.compile(r'自由(記述|意見|回答)|主な意見|主な自由記述|への要望|ご意見|その他の意見|コメント|具体的に(ご記|教え)')
ATTR=re.compile(r'[（(]\s*([^()（）]{2,24}?)\s*[)）]\s*(他)?\s*$')
out=[]
for f in sorted(glob.glob("data/ocr/*/*.txt")):
    d=f.split(os.sep)[-2]
    if d in("council_minutes","gikai_dayori","gikai_resolutions"): continue
    txt=open(f,encoding="utf8").read()
    for pg in re.split(r'\n=== page (\d+) ===\n',txt)[1:] and zip(*[iter(re.split(r'\n=== page (\d+) ===\n',txt)[1:])]*2):
        n,body=pg
        if not MARK.search(body): continue
        lines=[l.strip() for l in body.split("\n") if l.strip()]
        cur=None; ctx=""
        for l in lines:
            if MARK.search(l) and len(l)<60: ctx=l
            if l.startswith("・") or l.startswith("●") or l.startswith("○") and len(l)>12:
                if cur: out.append(cur)
                cur={"file":os.path.basename(f),"dir":d,"page":int(n),"context":ctx,"text":l[1:].strip()}
            elif cur and not re.match(r'^[\d\s.%,]+$',l) and not l.startswith("==="):
                cur["text"]+=l
        if cur: out.append(cur); cur=None
res=[]
for r in out:
    t=r["text"]; m=ATTR.search(t)
    r["attr"]=m.group(1).replace(" ","") if m else ""
    if m: t=t[:m.start()]
    t=re.sub(r'\s+','',t)
    r["text"]=t
    if len(t)>=8: res.append(r)
os.makedirs("data/free_text",exist_ok=True)
with open("data/free_text/comments.jsonl","w",encoding="utf8") as o:
    for i,r in enumerate(res): r["id"]=i; o.write(json.dumps(r,ensure_ascii=False)+"\n")
from collections import Counter
print(len(res)); print(Counter(r["file"] for r in res))
