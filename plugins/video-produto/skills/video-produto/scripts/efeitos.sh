#!/bin/bash
# Efeitos macios para peca de tecnologia: transicao, clique, brilho, pad.
# Nada de impacto dramatico - isso e da outra skill.
# Uso: efeitos.sh [pasta]
set -e
OUT="${1:-.}"; mkdir -p "$OUT"
FF=$(command -v ffmpeg || echo ./ffmpeg)
N() { "$FF" -y -v error -f lavfi \
  -i "anoisesrc=duration=$1:color=pink:amplitude=0.9:sample_rate=48000:seed=$4" \
  -af "$2,alimiter=limit=0.30:level=false,aformat=channel_layouts=stereo" "$OUT/$3"; }
T() { "$FF" -y -v error -f lavfi -i "sine=frequency=$1:duration=$2:sample_rate=48000" \
  -af "$3,alimiter=limit=0.30:level=false,aformat=channel_layouts=stereo" "$OUT/$4"; }

# transicao: sopro suave subindo e saindo
N 1.20 "bandpass=frequency=1200:width_type=h:width=2200,volume='0.5*sin(3.14159*t/1.2)':eval=frame" transicao.wav 11
# revelacao: brilho agudo com cauda longa
N 1.60 "highpass=frequency=2600,volume='0.45*exp(-2.2*t)':eval=frame" brilho.wav 22
# clique de interface: muito curto, sem cauda
N 0.09 "bandpass=frequency=1800:width_type=h:width=900,volume='0.7*exp(-28*t)':eval=frame" clique.wav 33
# pad: nota morna que abre e fecha, para assentar sob a cartela
T 220 2.40 "volume='0.30*sin(3.14159*t/2.4)':eval=frame,aecho=0.8:0.7:60:0.3,lowpass=frequency=3000" pad.wav

for f in transicao brilho clique pad; do
  printf "%-11s " "$f"
  "$FF" -i "$OUT/$f.wav" -af volumedetect -f null - 2>&1 | grep -oE 'max_volume: [-0-9.]+ dB'
done
