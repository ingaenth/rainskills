#!/bin/bash
# Mixagem final com VOZ DOMINANTE. A cama entra abaixo da voz por construcao
# (ganho estatico), nao apenas por ducking. Alvo: voz 10 a 15 dB acima da cama
# durante a fala. Verifique com 'medir.py balanco'.
# Uso: mixar.sh voz.wav musica.wav efeitos.wav ambiencia.wav saida.wav [dur]
set -e
V=$1; M=$2; E=$3; A=$4; O=$5; D=${6:-32}
FF=$(command -v ffmpeg || echo ./ffmpeg)
"$FF" -y -v error -i "$V" -i "$M" -i "$E" -i "$A" -filter_complex "
 [0]volume=1.7[vz];
 [1]atrim=0:$D,volume=0.30[mus];
 [2]atrim=0:$D,volume=0.85[fx];
 [3]atrim=0:$D,volume=0.10[amb];
 [vz]asplit=3[v][k1][k2];
 [mus][k1]sidechaincompress=threshold=0.045:ratio=5:attack=40:release=550[md];
 [amb][k2]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[ad];
 [md][ad][fx]amix=inputs=3:normalize=0[cama];
 [v][cama]amix=inputs=2:normalize=0,
 afade=t=in:d=0.8,afade=t=out:st=$(python3 -c "print($D-0.7)"):d=0.7,
 loudnorm=I=-15:TP=-1.5:LRA=9,alimiter=limit=0.82:level=false[out]" -map "[out]" "$O"
echo -n "$O  "
"$FF" -v info -i "$O" -af loudnorm=print_format=summary -f null - 2>&1 \
  | grep -E 'Input Integrated|Input True Peak' | tr '\n' ' '; echo
