import json,time,urllib.request
B="https://opendata.pref.tokushima.lg.jp"
ids=json.load(open("data/tokushima_opendata/pl.json",encoding="utf8"))["result"]
out=[]
for i in ids:
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(f"{B}/api/package_show?id={i}",headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
        r=d.get("result",d)
        out.append({"id":i,"title":r.get("title"),"org":(r.get("organization") or {}).get("title"),"tags":[t.get("name") for t in r.get("tags",[])],"resources":[{"name":x.get("name"),"format":x.get("format"),"url":x.get("url")} for x in r.get("resources",[])]})
    except Exception as e: out.append({"id":i,"error":str(e)})
    time.sleep(0.7)
    if len(out)%100==0: json.dump(out,open("data/tokushima_opendata/catalog.json","w",encoding="utf8"),ensure_ascii=False)
json.dump(out,open("data/tokushima_opendata/catalog.json","w",encoding="utf8"),ensure_ascii=False)
