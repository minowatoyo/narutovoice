import re, json, os, sys, urllib.request, urllib.parse
from html import unescape
H="https://www.city.naruto.lg.jp"
def get(u,raw=False):
    r=urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(u,safe=":/?=&%#"),headers={"User-Agent":"Mozilla/5.0"}),timeout=120)
    b=r.read(); return b if raw else b.decode("utf8","ignore")
d=json.load(open("docs.json",encoding="utf8"))
pat=re.compile('調査|アンケート|意識|意見|結果公表|統計|人口|満足|ニーズ|ふるさと納税|BOX|市民ガイド|総合計画|総合戦略|計画|ビジョン|こども|地域公共交通|広報アンケート|活用状況|過去に意見')
skip=re.compile('入札|音声|避難確保|水質|選挙|クロスカントリー|ゾーニング|農')
seeds=[u for u,t in d.items() if pat.search(t) and not skip.search(t)]
seeds+=["/docs/2025020100019/","/docs/2025120100070/"]
files={}; seen=set(); queue=list(dict.fromkeys(seeds))
while queue:
    u=queue.pop(0)
    if u in seen: continue
    seen.add(u)
    try: h=get(H+u)
    except Exception as e: continue
    title=(re.search(r'<title>(.*?)</title>',h,re.S) or [0,""])[1] if False else unescape(re.sub(r'\s+',' ',(re.search(r'<title>(.*?)</title>',h,re.S).group(1) if re.search(r'<title>',h) else "")))
    for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',h,re.S):
        l,t=m.group(1),unescape(re.sub(r'<[^>]+>','',m.group(2))).strip()
        if re.search(r'file_contents/.*\.(pdf|xlsx?|csv|docx?|zip)$',l,re.I):
            l=H+u.rstrip('/')+'/'+l
            files[l]={"text":t,"page":u,"pagetitle":title}
        elif re.match(r'/docs/\d+/?$',l) and len(seen)<200 and l not in seen and re.search('調査|アンケート|意識|結果|統計|人口|意見|ビジョン|計画',t) and not skip.search(t):
            queue.append(l)
json.dump(files,open("files.json","w",encoding="utf8"),ensure_ascii=False,indent=1)
print(len(seen),"pages",len(files),"files")
