# -*- coding: utf-8 -*-
"""Генерация QR в форматах SVG(вектор)+EPS+JPG+PNG с WB/OZON лого
и сборка папки QR_АКТУАЛЬНЫЕ на рабочем столе с разбивкой по QR."""
import sys, shutil, base64
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

DESK = Path(r"C:\Users\Roman.Gapancov\Desktop")
WB_LOGO  = Path(r"C:\Users\Roman.Gapancov\Downloads\WB.png")
OZ_LOGO  = Path(r"C:\Users\Roman.Gapancov\Downloads\OZON.png")
ROOT = DESK / "QR_АКТУАЛЬНЫЕ"
LOGO_RATIO = 0.28

def _matrix(url):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url); qr.make(fit=True)
    return qr.get_matrix()

def _raster(url, logo_path):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=40, border=4)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        tw = int(img.size[0]*LOGO_RATIO)
        th = int(logo.size[1]*(tw/logo.size[0]))
        logo = logo.resize((tw, th), Image.LANCZOS)
        PAD = 14
        bw, bh = tw+2*PAD, th+2*PAD
        bg = Image.new("RGBA", (bw, bh), (255,255,255,255))
        img.paste(bg, ((img.size[0]-bw)//2, (img.size[1]-bh)//2), bg)
        img.paste(logo, ((img.size[0]-tw)//2, (img.size[1]-th)//2), logo)
    return img.convert("RGB")

def _svg(url, logo_path, out):
    m = _matrix(url); n = len(m); u = 10; b = 4; S = (n+2*b)*u
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
             f'viewBox="0 0 {S} {S}" shape-rendering="crispEdges">',
             f'<rect width="{S}" height="{S}" fill="#ffffff"/>']
    d = []
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                x = (c+b)*u; y = (r+b)*u
                d.append(f"M{x} {y}h{u}v{u}h-{u}z")
    parts.append(f'<path d="{"".join(d)}" fill="#000000"/>')
    if logo_path:
        lw, lh = Image.open(logo_path).size
        tw = LOGO_RATIO*S; th = lh*(tw/lw); pad = 0.02*S
        bx = (S-tw)/2-pad; by = (S-th)/2-pad
        parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{tw+2*pad:.1f}" '
                     f'height="{th+2*pad:.1f}" fill="#ffffff"/>')
        b64 = base64.b64encode(Path(logo_path).read_bytes()).decode()
        parts.append(f'<image x="{(S-tw)/2:.1f}" y="{(S-th)/2:.1f}" width="{tw:.1f}" '
                     f'height="{th:.1f}" href="data:image/png;base64,{b64}"/>')
    parts.append('</svg>')
    Path(out).write_text("\n".join(parts), encoding="utf-8")

def gen_all(url, logo_path, folder, base):
    img = _raster(url, logo_path)
    img.save(folder/f"{base}.png", "PNG", optimize=True)
    img.save(folder/f"{base}.jpg", "JPEG", quality=95)
    img.save(folder/f"{base}.eps")
    _svg(url, logo_path, folder/f"{base}.svg")

# folder, info, gen-spec (url, logo, base)  OR  copy-list
QRS = [
 ("1_PWR_Telegram_наклейка",
  {"Назначение":"PWR — Telegram-канал","Зашито в QR":"envilope1337.github.io/p",
   "Ведёт на":"t.me/pwr_supplements","Тип":"динамический","Трекинг":"Яндекс.Метрика 109286123",
   "Носитель":"наклейка","Статус":"НАПЕЧАТАН, в работе — путь не менять"},
  None, ["QR_PWR_FINAL.png","QR_PWR_FINAL.svg"]),
 ("2_Seauty_наклейка",
  {"Назначение":"Seauty — MAX","Зашито в QR":"envilope1337.github.io/s",
   "Ведёт на":"max.ru/id972710036798_biz/AZ6SY4muMEY (обновлено 05.06.2026)","Тип":"динамический",
   "Трекинг":"Яндекс.Метрика 109286123","Носитель":"наклейка","Статус":"НАПЕЧАТАН, в работе — путь не менять"},
  None, ["QR_SEAUTY_FINAL.png","QR_SEAUTY_FINAL.svg"]),
 ("3_PWR_Wildberries_наклейка",
  {"Назначение":"PWR — Wildberries","Зашито в QR":"envilope1337.github.io/wb",
   "Ведёт на":"pwr-wb.netlify.app -> WB","Тип":"динамический","Трекинг":"Яндекс.Метрика + Netlify",
   "Носитель":"наклейка","Статус":"в работе"},
  ("https://envilope1337.github.io/wb", WB_LOGO, "QR_PWR_wb"), None),
 ("4_PWR_Ozon_наклейка",
  {"Назначение":"PWR — Ozon","Зашито в QR":"envilope1337.github.io/oz",
   "Ведёт на":"ozon.by/.../pwr-ultimate-power-87319467","Тип":"динамический","Трекинг":"Яндекс.Метрика",
   "Носитель":"наклейка","Статус":"в работе"},
  ("https://envilope1337.github.io/oz", OZ_LOGO, "QR_PWR_oz"), None),
 ("5_PWR_WB_БАННЕР_спортзал",
  {"Назначение":"PWR — Wildberries (баннер в спортзале)","Зашито в QR":"envilope1337.github.io/pwr-wb",
   "Ведёт на":"pwr-wb.netlify.app -> каталог WB","Тип":"динамический (НОВЫЙ)","Трекинг":"Яндекс.Метрика",
   "Носитель":"баннер","Статус":"ПЕЧАТЬ ПН 08.06 — использовать ЭТИ файлы"},
  ("https://envilope1337.github.io/pwr-wb", WB_LOGO, "QR_PWR_wb_banner"), None),
 ("6_PWR_Магний_вкладыш",
  {"Назначение":"PWR — Магний цитрат (арт. 141931034)","Зашито в QR":"envilope1337.github.io/pwr-magnesium",
   "Ведёт на":"wildberries.ru/catalog/141931034","Тип":"динамический (НОВЫЙ)","Трекинг":"Яндекс.Метрика",
   "Носитель":"листовка-вкладыш + промокод",
   "Статус":"ПЕЧАТЬ до ПН 08.06 — ЭТИ файлы. Старый QR_WB_MAGNESIUM.png УСТАРЕЛ, НЕ печатать"},
  ("https://envilope1337.github.io/pwr-magnesium", WB_LOGO, "QR_PWR_magnesium"), None),
 ("7_PWR_WB_бренд_статический",
  {"Назначение":"PWR — бренд на WB","Зашито в QR":"wildberries.ru/brands/pwr-ultimate-power",
   "Ведёт на":"WB бренд напрямую","Тип":"СТАТИЧЕСКИЙ (не трекается, не меняется)","Трекинг":"нет",
   "Носитель":"print","Статус":"в работе; при перепечатке -> на динамику"},
  None, ["WB_PWR_QR_print.png","WB_PWR_QR_print.svg"]),
 ("8_Seauty_WB_бренд_статический",
  {"Назначение":"Seauty — бренд на WB","Зашито в QR":"wildberries.ru/brands/seauty",
   "Ведёт на":"WB бренд напрямую","Тип":"СТАТИЧЕСКИЙ (не трекается, не меняется)","Трекинг":"нет",
   "Носитель":"print","Статус":"в работе; при перепечатке -> на динамику"},
  None, ["WB_SEAUTY_QR_print.png","WB_SEAUTY_QR_print.svg"]),
]

if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)

for folder, info, gen, copies in QRS:
    d = ROOT / folder; d.mkdir(parents=True, exist_ok=True)
    (d/"info.txt").write_text("\n".join(f"{k}: {v}" for k,v in info.items())+"\n", encoding="utf-8")
    if gen:
        url, logo, base = gen
        gen_all(url, logo, d, base)
        print(f"  [GEN] {folder}: {base}.svg/.eps/.jpg/.png")
    if copies:
        for f in copies:
            src = DESK/f
            if src.exists():
                shutil.copy2(src, d/f)
            else:
                (d/f"НЕТ_{f}.txt").write_text(f"{f} не найден на рабочем столе\n", encoding="utf-8")
        print(f"  [COPY] {folder}: {copies}")

(ROOT/"00_ПРОЧТИ_МЕНЯ.txt").write_text(
"""QR_АКТУАЛЬНЫЕ — актуальные QR-коды (обновлено 05.06.2026)

Подпапка = один QR. Внутри: картинки (SVG+EPS+JPG+PNG) + info.txt.
Форматы: SVG — вектор (для печати/баннеров, масштаб без потери), EPS — для дизайнеров,
JPG — превью, PNG — универсальный.

ПЕЧАТЬ СЕЙЧАС:
  - Папка 5 (WB-баннер) и 6 (Магний) — печатать ИЗ ЭТИХ ПАПОК (динамические + Я.Метрика).
  - Старый QR_WB_MAGNESIUM.png на рабочем столе — УСТАРЕЛ, НЕ печатать.
  - Ozon-баннер ОТМЕНЁН (Антон) — тут его нет.

Типы:
  - динамический = через envilope1337.github.io, цель меняется без перепечатки, в Я.Метрике.
  - статический = прямо на маркетплейс, поменять нельзя, не трекается.

Папки 1,2,7,8 — копии существующих файлов (PNG/SVG). Папки 3,4,5,6 — свежесгенерированы во всех форматах.
Репо: github.com/envilope1337/envilope1337.github.io | Реестр: Google Sheet "QRs" -> лист "Итог QR".
""", encoding="utf-8")

print("\nГотово:", ROOT)
