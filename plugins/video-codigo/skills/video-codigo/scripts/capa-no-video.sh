#!/usr/bin/env bash
# Embute a capa no vídeo de dois jeitos:
#   1) como 1º quadro (1/30 s) — o Instagram já sugere essa capa ao subir;
#   2) como miniatura do arquivo (attached_pic) — aparece no Windows, WhatsApp, Drive.
# Reencoda em bitrate alto para o Instagram recomprimir a partir de uma fonte limpa.
#
#   bash capa-no-video.sh reel.mp4 capa.png saida.mp4
set -euo pipefail
in="$1"; capa="$2"; out="$3"
tmp="$(mktemp -d)"
ffmpeg -v error -y -loop 1 -framerate 30 -i "$capa" -i "$in" -filter_complex \
 "[0:v]trim=end_frame=1,format=yuv420p,setsar=1[c];anullsrc=r=48000:cl=stereo,atrim=duration=0.0333333[s];[1:v]setsar=1[v];[c][s][v][1:a]concat=n=2:v=1:a=1[vo][ao]" \
 -map "[vo]" -map "[ao]" -c:v libx264 -preset slow -b:v 16M -maxrate 20M -bufsize 32M -tune film -profile:v high -pix_fmt yuv420p -r 30 \
 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$tmp/v.mp4"
ffmpeg -v error -y -i "$capa" -q:v 2 -vf scale=720:-1 "$tmp/c.jpg"
ffmpeg -v error -y -i "$tmp/v.mp4" -i "$tmp/c.jpg" -map 0 -map 1 -c copy -disposition:v:1 attached_pic "$out"
rm -rf "$tmp"
echo "$out"
