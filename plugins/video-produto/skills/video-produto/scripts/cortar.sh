#!/bin/bash
# Corta para detalhe numa janela, mantendo 16:9 e a duracao total.
# Use onde a boca fica parada com a voz correndo; escolha um objeto que a frase cite.
# Uso: cortar.sh entrada.mp4 inicio fim L:A:X:Y saida.mp4 [dur_total]
set -e
IN=$1; A=$2; B=$3; CROP=$4; OUT=$5; D=${6:-32}
FF=$(command -v ffmpeg || echo ./ffmpeg)
"$FF" -y -v error -i "$IN" -filter_complex "
 [0:v]split=3[a][b][c];
 [a]trim=0:$A,setpts=PTS-STARTPTS,scale=1280:720,setsar=1[s1];
 [b]trim=$A:$B,setpts=PTS-STARTPTS,crop=$CROP,scale=1280:720,setsar=1,
    zoompan=z='min(zoom+0.0008,1.10)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24[s2];
 [c]trim=$B:$D,setpts=PTS-STARTPTS,scale=1280:720,setsar=1[s3];
 [s1][s2][s3]concat=n=3:v=1:a=0[v]" -map "[v]" -an \
 -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "$OUT"
echo -n "$OUT  "; "$FF" -i "$OUT" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p'
