#!/usr/bin/env bash
# Foto real -> plano vertical. Sem modelo generativo: so recorte, panoramica e nitidez.
# uso: foto2video.sh <foto> <dur> <x0_frac> <x1_frac> <saida>
set -euo pipefail
FF=$(command -v ffmpeg || echo ../ffmpeg)
FOTO=$1; DUR=$2; X0=$3; X1=$4; OUT=$5
read W H < <(python3 -c "from PIL import Image;im=Image.open('$FOTO');print(im.width,im.height)")
CW=$(python3 -c "print(int($H*9/16)//2*2)")
# x animado; w/h sao fixos porque o crop so reavalia x/y por quadro
XA=$(python3 -c "print(round(($W-$CW)*$X0))")
XB=$(python3 -c "print(round(($W-$CW)*$X1))")
$FF -y -v error -loop 1 -t "$DUR" -i "$FOTO" -vf \
"crop=$CW:$H:x='$XA+($XB-$XA)*t/$DUR':y=0,\
scale=720:1280:flags=lanczos,\
unsharp=5:5:0.55:5:5:0.0,\
eq=saturation=1.04:contrast=1.03,\
fps=24,format=yuv420p" -c:v libx264 -crf 15 -preset medium "$OUT"
echo "$OUT  ${CW}x${H} -> 720x1280  pan ${XA}->${XB}px"
