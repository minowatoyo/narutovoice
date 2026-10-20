import re,glob,os,json
FILES=["tyosa-15-29","tyosa-syoutyuu","tyosa-jigyosyo","00445719_enquete","enquete_r7","dai2_enquate","kodomoseikatsu"]
FIX=[(r'[カ力]ヾ|カゞ','が'),(r'市ては','市では'),(r'町ては','町では'),(r'てす(?=[。、\s]|$)','です'),(r'ててす','ですです'),(r'(?<=[ぁ-んァ-ン一-龥])か、','が、'),(r'のて(?=[、。\s]|$)','ので'),(r'工アコン','エアコン'),(r'てき(?=[るなまた])','でき'),(r'ショッピンク','ショッピング')]
def clean(t):
    for a,b in FIX: t=re.sub(a,b,t)
    return t.replace('ですです','です')
rows=[]
for f in sorted(glob.glob("data/ocr/*/*.txt")):
    if not any(k in f for k in FILES): continue
    txt=open(f,encoding="utf8").read(); cap=False; ctx=""; q=[]; buf=[]; page=0; ent=[]
    def flush():
        global buf
        if buf: ent.append((page,ctx,"".join(buf))); buf=[]
    for l in txt.split("\n"):
        l=l.strip()
        m=re.match(r'=== page (\d+) ===',l)
        if m: page=int(m.group(1)); continue
        if not l: continue
        if re.search(r'調査票|ご協力ありがとう',l): flush(); cap=False; continue
        if re.match(r'^(問|Q)\s*\d+',l) or re.match(r'^[【\[]',l) and not '要望' in l:
            flush(); cap=False; q=[l]; ctx=l
        elif not cap: 
            if len(q)<4: q.append(l); ctx=" ".join(q)
        if re.search(r'[（(]\s*自由記述\s*[)）]|自由に(お)?書き|ご記入ください\s*$',l) and not re.search(r'☐|□',l):
            flush(); cap=True; ctx=" ".join(q)[:120]; continue
        if cap:
            if re.match(r'^[\d\s.,%\-~]+$',l) or len(l)<4 or re.match(r'^(n|N)\s*=',l): continue
            if re.match(r'^(・|●)',l): flush(); buf=[l[1:]]; continue
            buf.append(l)
            if len(l)<33 or l.endswith("。"): flush()
    flush()
    for p,c,t in ent:
        t=re.sub(r'\s+','',t); t=re.sub(r'[（(]\s*\d+\s*[)）]$','',t)
        if len(t)>=6: rows.append({"file":os.path.basename(f),"dir":f.split(os.sep)[-2],"page":p,"context":c,"text_raw":t,"text":clean(t)})
old=[json.loads(l) for l in open("data/free_text/comments.jsonl",encoding="utf8")] if os.path.exists("data/free_text/comments.jsonl") else []
old=[o for o in old if not any(k in o["file"] for k in FILES)]
for o in old: o["text_raw"]=o["text"]; o["text"]=clean(o["text"])
allr=old+rows
with open("data/free_text/comments.jsonl","w",encoding="utf8") as o:
    for i,r in enumerate(allr): r["id"]=i; o.write(json.dumps(r,ensure_ascii=False)+"\n")
from collections import Counter
print(len(allr),Counter(r["file"] for r in allr))
