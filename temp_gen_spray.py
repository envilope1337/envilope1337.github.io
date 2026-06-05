# -*- coding: utf-8 -*-
import sys, base64
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

URL = "https://envilope1337.github.io/seauty-spray"
WB_LOGO = Path(r"C:\Users\Roman.Gapancov\Downloads\WB.png")
DEST = Path(r"C:\Users\Roman.Gapancov\Desktop\QR_АКТУАЛЬНЫЕ\9_Seauty_спрей_листовка")
BASE = "QR_Seauty_spray"
RATIO = 0.28

DEST.mkdir(parents=True, exist_ok=True)

def raster(url, logo):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=40, border=4)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    lg = Image.open(logo).convert("RGBA")
    tw = int(img.size[0]*RATIO); th = int(lg.size[1]*(tw/lg.size[0]))
    lg = lg.resize((tw, th), Image.LANCZOS)
    PAD = 14; bw, bh = tw+2*PAD, th+2*PAD
    bg = Image.new("RGBA",(bw,bh),(255,255,255,255))
    img.paste(bg,((img.size[0]-bw)//2,(img.size[1]-bh)//2),bg)
    img.paste(lg,((img.size[0]-tw)//2,(img.size[1]-th)//2),lg)
    return img.convert("RGB")

def svg(url, logo, out):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url); qr.make(fit=True)
    m = qr.get_matrix(); n=len(m); u=10; b=4; S=(n+2*b)*u
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}" shape-rendering="crispEdges">',
       f'<rect width="{S}" height="{S}" fill="#ffffff"/>']
    d=[]
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                d.append(f"M{(c+b)*u} {(r+b)*u}h{u}v{u}h-{u}z")
    p.append(f'<path d="{"".join(d)}" fill="#000000"/>')
    lw,lh=Image.open(logo).size; tw=RATIO*S; th=lh*(tw/lw); pad=0.02*S
    p.append(f'<rect x="{(S-tw)/2-pad:.1f}" y="{(S-th)/2-pad:.1f}" width="{tw+2*pad:.1f}" height="{th+2*pad:.1f}" fill="#ffffff"/>')
    b64=base64.b64encode(Path(logo).read_bytes()).decode()
    p.append(f'<image x="{(S-tw)/2:.1f}" y="{(S-th)/2:.1f}" width="{tw:.1f}" height="{th:.1f}" href="data:image/png;base64,{b64}"/>')
    p.append('</svg>')
    Path(out).write_text("\n".join(p), encoding="utf-8")

img = raster(URL, WB_LOGO)
img.save(DEST/f"{BASE}.png","PNG",optimize=True)
img.save(DEST/f"{BASE}.jpg","JPEG",quality=95)
img.save(DEST/f"{BASE}.eps")
svg(URL, WB_LOGO, DEST/f"{BASE}.svg")

(DEST/"info.txt").write_text(
"Назначение: Seauty — Спрей для волос термозащита 200мл (арт. 252141724)\n"
"Зашито в QR: envilope1337.github.io/seauty-spray\n"
"Ведёт на: открывает приложение WB на товаре wildberries.ru/catalog/252141724 (intent:// + Smart App Banner)\n"
"Тип: динамический\n"
"Трекинг: Яндекс.Метрика 109286123\n"
"Носитель: бумажная листовка\n"
"Особенность: QR сразу открывает ПРИЛОЖЕНИЕ Wildberries, не браузер (требование Марии)\n"
"Заказ: Мария -> Костя\n"
"Статус: сделано 05.06.2026\n", encoding="utf-8")

print("OK:", DEST)
print("файлы:", BASE+".svg/.eps/.jpg/.png + info.txt")
