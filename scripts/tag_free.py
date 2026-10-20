import json,re,csv
SRC={"tyosa-15-29":"若者(15-29歳)","tyosa-syoutyuu":"小中学生","tyosa-jigyosyo":"こども支援事業所","hokoku_r4":"障がい福祉(R4)","00138864_hokoku":"障がい福祉(H28)","00445719":"地域福祉","2026042300029_2":"教育振興計画","ishikityosa":"市民意識調査","public_kekka":"PC結果","dai4":"その他","questionary":"給食アンケート(児童生徒)","vision_2025":"人口ビジョン2025(転入転出・高校生)","0029_2":"教育振興計画"}
TOP={"交通・移動":"バス|電車|汽車|鉄道|交通|移動|道路|通学路|駐車","遊び場・商業施設":"遊べる|公園|ショッピング|モール|遊園地|プール|お店|カフェ|店|施設|体育館|イベント|祭り","相談・居場所":"相談|居場所|子ども食堂|見守り|孤立","教育・学校":"学校|校則|いじめ|教育|学習|先生|奨学|給食","経済支援":"支援金|経済|補助|税金|奨学金|賃金|収入|お金|費用","福祉・障がい":"障が|障害|福祉|療育|グループホーム|手帳|サービス|介護","防災":"災害|避難|防災|地震|津波","就労・定住":"就労|就業|仕事|就職|地元|定住|人口|働","行政対応・情報":"情報|周知|広報|窓口|アンケート|反映|行政|市役所","観光・まちの魅力":"観光|渦潮|魅力|PR|盛り上"}
rows=[json.loads(l) for l in open("data/free_text/comments.jsonl",encoding="utf8")]
out=[]
for r in rows:
    t=r["text"]
    if re.search(r'数字を記|^[\d\s()（）]+$',t) or len(t)<6: continue
    r["source_group"]=next((v for k,v in SRC.items() if k in r["file"]),"その他")
    r["topics"]=[k for k,p in TOP.items() if re.search(p,t)]
    out.append(r)
json.dump(out,open("data/free_text/comments_tagged.json","w",encoding="utf8"),ensure_ascii=False,indent=1)
with open("data/free_text/comments_tagged.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f); w.writerow(["id","source_group","file","page","question","text","topics","attr"])
    for r in out: w.writerow([r["id"],r["source_group"],r["file"],r["page"],r["context"],r["text"],";".join(r["topics"]),r.get("attr","")])
from collections import Counter
print(len(out),Counter(r["source_group"] for r in out)); print(Counter(t for r in out for t in r["topics"]))
