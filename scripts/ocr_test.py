import pymupdf, asyncio, winocr, sys
from PIL import Image
import io
d=pymupdf.open(sys.argv[1]); p=d[int(sys.argv[2])]
pix=p.get_pixmap(dpi=200); img=Image.open(io.BytesIO(pix.tobytes("png")))
r=asyncio.run(winocr.recognize_pil(img,"ja"))
open("ocr_test.txt","w",encoding="utf8").write(r.text)
