import pymupdf,json,os,re,csv,unicodedata,glob
m=json.load(open("manifest.json",encoding="utf8"))
os.makedirs("data/statistics_csv",exist_ok=True)
N=lambda s: unicodedata.normalize("NFKC",s or "").strip()
idx=[]
for k,v in m.items():
    if "統計年報" not in v["pagetitle"] or not v.get("local"): continue
    yr=re.search(r'統計年報(\d{4})',v["pagetitle"]).group(1)
    base=os.path.basename(v["local"])[:-4]
    try: doc=pymupdf.open(v["local"])
    except Exception as e: continue
    rows_out=[]; txt=[]
    for pi,p in enumerate(doc):
        txt.append(p.get_text())
        for t in p.find_tables().tables:
            data=t.extract()
            # expand multiline cells into rows when line counts align
            nl=[max((len(N(c).split("\n")) if c else 1) for c in r) for r in data]
            for r,n in zip(data,nl):
                cells=[N(c).split("\n") if c is not None else [""] for c in r]
                if n>1 and sum(1 for c in cells if len(c)==n)>=2:
                    for i in range(n): rows_out.append([pi+1]+[c[i] if len(c)==n else (c[0] if len(c)==1 else " ".join(c)) for c in cells])
                else: rows_out.append([pi+1]+[" ".join(c).strip() for c in cells])
    fixed=[]
    for r in rows_out:
        d=r[2:]
        if len(d)>1 and d[0] and not any(d[1:]) and len(d[0].split())>1 and re.fullmatch(r'[△▲\-\d.,%\s—―－]+',d[0]):
            r=r[:2]+re.sub(r'[△▲]\s*','-',d[0]).split()
        fixed.append(r)
    rows_out=fixed
    name=f"{yr}_{base.split('_',1)[-1]}"
    if rows_out:
        w=csv.writer(open(f"data/statistics_csv/{name}.csv","w",encoding="utf-8-sig",newline=""))
        w.writerows(rows_out)
    open(f"data/statistics_csv/{name}.txt","w",encoding="utf8").write("\n".join(txt))
    idx.append((yr,v["text"],name,len(rows_out)))
w=csv.writer(open("data/statistics_csv/_index.csv","w",encoding="utf-8-sig",newline="")); w.writerow(["year","table","file","rows"]); w.writerows(idx)
print(len(idx),sum(1 for i in idx if i[3]==0),"without tables")
