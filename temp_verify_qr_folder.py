# -*- coding: utf-8 -*-
import sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
import cv2, numpy as np

root = r'C:\Users\Roman.Gapancov\Desktop\QR_АКТУАЛЬНЫЕ'
d = cv2.QRCodeDetector()

def imread_u(path):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

for p in sorted(glob.glob(root + r'\**\*.png', recursive=True)):
    try:
        img = imread_u(p)
        txt, _, _ = d.detectAndDecode(img)
    except Exception as e:
        txt = f"<err {e}>"
    rel = os.path.relpath(p, root)
    print(f'{rel:58s} -> {txt or "<NOT DECODED>"}')
