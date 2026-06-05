"""Regenerate WB QR with embedded WB.png logo."""
from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image

URL = "https://envilope1337.github.io/wb"
LOGO = Path(r"C:\Users\Roman.Gapancov\Downloads\WB.png")
OUT = Path(r"C:\Users\Roman.Gapancov\Desktop\QR_PWR_WB_LOGO.png")

LOGO_WIDTH_RATIO = 0.30
PAD_PX = 14

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=40, border=4)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

logo = Image.open(LOGO).convert("RGBA")
target_w = int(img.size[0] * LOGO_WIDTH_RATIO)
target_h = int(logo.size[1] * (target_w / logo.size[0]))
logo = logo.resize((target_w, target_h), Image.LANCZOS)

bg_w, bg_h = target_w + 2 * PAD_PX, target_h + 2 * PAD_PX
bg = Image.new("RGBA", (bg_w, bg_h), (255, 255, 255, 255))
bg_pos = ((img.size[0] - bg_w) // 2, (img.size[1] - bg_h) // 2)
img.paste(bg, bg_pos, bg)

logo_pos = ((img.size[0] - target_w) // 2, (img.size[1] - target_h) // 2)
img.paste(logo, logo_pos, logo)

img.convert("RGB").save(OUT, "PNG", optimize=True)
print(f"OK: {OUT}")
print(f"  QR size: {img.size}, logo: {target_w}x{target_h}, bg patch: {bg_w}x{bg_h}")
