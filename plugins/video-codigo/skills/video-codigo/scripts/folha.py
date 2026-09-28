"""Folha de contato dos stills de revisão.

    python folha.py peca 1,5.5,12 [out]   ->  out/peca-folha.png

Junta out/peca-<t>.png numa grade (6 por linha no vertical, 3 no horizontal) e escreve o
tempo em cada quadro. Leia a folha, corrija, renderize de novo. Precisa de Pillow.
"""
import sys
from PIL import Image, ImageDraw

name, ts = sys.argv[1], sys.argv[2].split(',')
out = sys.argv[3] if len(sys.argv) > 3 else 'out'
ims = [Image.open(f'{out}/{name}-{t}.png').convert('RGB') for t in ts]
vert = ims[0].height > ims[0].width
w, h = (360, 640) if vert else (640, 360)
cols = min(6 if vert else 3, len(ims))
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (w * cols, h * rows), (0, 0, 0))
for i, (im, t) in enumerate(zip(ims, ts)):
    x = im.resize((w, h))
    d = ImageDraw.Draw(x)
    d.rectangle([0, 0, 70, 24], fill=(0, 0, 0))
    d.text((6, 5), f'{t}s', fill=(255, 255, 0))
    S.paste(x, ((i % cols) * w, (i // cols) * h))
S.save(f'{out}/{name}-folha.png')
print(f'{out}/{name}-folha.png')
