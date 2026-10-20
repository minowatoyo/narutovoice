import json,re,os,urllib.request,urllib.parse
sel=json.load(open("sel.json",encoding="utf8"))
def cat(v):
    t=v["pagetitle"]+v["text"]
    if "統計年報" in t: return "statistics_yearbook"
    if "総合計画審議会" in t: return "council_minutes"
    if re.search("全国学力",t): return "school_achievement"
    if "給食" in t: return "school_lunch_survey"
    if re.search("アンケート|調査報告|意識調査|ワークショップ|ニーズ|生活調査|実態調査",t): return "surveys"
    if re.search("パブリックコメント|意見募集|結果公表",t): return "public_comments"
    return "plans_context"
n=0
for k,v in sel.items():
    sz=re.search(r'([\d.]+)MB',v["text"])
    if sz and float(sz.group(1))>12: continue
    c=cat(v); os.makedirs("data/raw/"+c,exist_ok=True)
    pid=re.search(r'/docs/(\d+)/',k).group(1)
    fn=os.path.basename(k).split("__files_")[-1]
    p=f"data/raw/{c}/{pid}_{fn}"
    if os.path.exists(p): continue
    try:
        b=urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(k,safe=":/%"),headers={"User-Agent":"Mozilla/5.0"}),timeout=120).read()
        open(p,"wb").write(b); n+=1
        v["local"]=p
    except Exception as e: print("ERR",k,e)
print(n)
json.dump(sel,open("manifest.json","w",encoding="utf8"),ensure_ascii=False,indent=1)
