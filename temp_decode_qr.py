# -*- coding: utf-8 -*-
import sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

DESK = r"C:\Users\Roman.Gapancov\Desktop"
pngs = sorted(glob.glob(os.path.join(DESK, "*QR*.png")) +
              glob.glob(os.path.join(DESK, "*qr*.png")) +
              glob.glob(os.path.join(DESK, "WB_*_QR_print.png")))
pngs = sorted(set(pngs))

decoder = None
try:
    from pyzbar.pyzbar import decode as zbar_decode
    from PIL import Image
    def dec(p):
        res = zbar_decode(Image.open(p))
        return [r.data.decode('utf-8', 'replace') for r in res]
    decoder = "pyzbar"
except Exception:
    try:
        import cv2
        d = cv2.QRCodeDetector()
        def dec(p):
            img = cv2.imread(p)
            data, pts, _ = d.detectAndDecode(img)
            return [data] if data else []
        decoder = "cv2"
    except Exception as e:
        print("NO DECODER:", e); sys.exit(1)

print(f"decoder: {decoder}\n")
for p in pngs:
    try:
        urls = dec(p)
    except Exception as e:
        urls = [f"<error {e}>"]
    print(f"{os.path.basename(p):28s} -> {urls if urls else '<not decoded>'}")
