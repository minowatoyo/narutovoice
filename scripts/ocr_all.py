import pymupdf, asyncio, winocr, sys, os, io, re, glob
from PIL import Image
dirs=sys.argv[1:]
async def main():
    for d in dirs:
        os.makedirs(f"data/ocr/{d}",exist_ok=True)
        for f in sorted(glob.glob(f"data/raw/{d}/*.pdf")):
            out=f"data/ocr/{d}/"+os.path.basename(f)[:-4]+".txt"
            if os.path.exists(out): continue
            doc=pymupdf.open(f); pages=[]
            for i,p in enumerate(doc):
                pix=p.get_pixmap(dpi=200); img=Image.open(io.BytesIO(pix.tobytes("png")))
                r=await winocr.recognize_pil(img,"ja")
                lines=[re.sub(r'(?<=[^\x00-\x7f]) (?=[^\x00-\x7f])','',l.text) for l in r.lines]
                pages.append(f"\n=== page {i+1} ===\n"+"\n".join(lines))
            open(out,"w",encoding="utf8").write("".join(pages))
            print(out,len(doc),flush=True)
asyncio.run(main())
