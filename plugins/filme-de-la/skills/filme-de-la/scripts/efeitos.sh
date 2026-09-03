#!/bin/bash
# Sintetiza efeitos de la a partir de ruido rosa filtrado + envelope.
# Uso: efeitos.sh [pasta_saida]   -> fio.wav 101
# tecido.wav 202 poeira.wav rangido.wav 404
set -e
OUT="${1:-.}"; mkdir -p "$OUT"
FF=$(command -v ffmpeg || echo ./ffmpeg)
N() { "$FF" -y -v error -f lavfi \
  -i "anoisesrc=duration=$1:color=pink:amplitude=0.9:sample_rate=48000:seed=$4" \
  -af "$2,alimiter=limit=0.35:level=false,aformat=channel_layouts=stereo" "$OUT/$3"; }

# fio esticando ate estalar: agudo com ataque crescente
N 0.75 "bandpass=frequency=2400:width_type=h:width=1600,volume='0.05+0.55*pow(t/0.75\,2)':eval=frame,afade=t=out:st=0.62:d=0.13" fio.wav 101
# tecido rocando: grave em senoide
N 0.90 "bandpass=frequency=520:width_type=h:width=700,volume='0.55*sin(3.14159*t/0.9)':eval=frame" tecido.wav 202
# poeira de feltro: agudo com decaimento
N 1.10 "highpass=frequency=3800,volume='0.40*exp(-3.2*t)':eval=frame" poeira.wav 303
# rangido: banda estreita com vibrato
N 1.30 "bandpass=frequency=880:width_type=h:width=260,vibrato=f=5.5:d=0.35,volume='0.42*sin(3.14159*t/1.3)':eval=frame" rangido.wav 404

for f in fio tecido poeira rangido; do
  printf "%-9s " "$f"
  "$FF" -i "$OUT/$f.wav" -af volumedetect -f null - 2>&1 | grep -oE 'max_volume: [-0-9.]+ dB'
done
echo
echo "posicione com adelay, ex:"
echo "  [0]adelay=3400|3400,volume=1.4[e1]"
