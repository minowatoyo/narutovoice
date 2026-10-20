import pymupdf, asyncio, winocr, sys, io
from PIL import Image
d=pymupdf.open(sys.argv[1]); p=d[int(sys.argv[2])-1]
async def m():
    for dpi in (200,300,400):
        img=Image.open(io.BytesIO(p.get_pixmap(dpi=dpi).tobytes("png")))
        r=await winocr.recognize_pil(img,"ja")
        print(dpi, "|".join(l.text.replace(" ","") for l in r.lines[:12]))
asyncio.run(m())
