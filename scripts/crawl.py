import re, sys, json, time, urllib.request, urllib.parse
from html import unescape
H="https://www.city.naruto.lg.jp"
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(u,safe=":/?=&%#"),headers={"User-Agent":"Mozilla/5.0"}),timeout=60)
        return r.read().decode("utf8","ignore")
    except Exception as e:
        return ""
def links(html):
    out=[]
    for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',html,re.S):
        out.append((m.group(1),unescape(re.sub(r'<[^>]+>','',m.group(2))).strip()))
    return out
cats=sorted(set(re.findall(r'href="(/category/bunya/[^"]+/)"',get(H+"/"))))
docs={}
for c in cats:
    for u,t in links(get(H+c)):
        if re.match(r'/docs/\d+/?$',u) and t: docs[u]=t
print(len(cats),"cats",len(docs),"docs",file=sys.stderr)
json.dump(docs,open("docs.json","w",encoding="utf8"),ensure_ascii=False,indent=0)
