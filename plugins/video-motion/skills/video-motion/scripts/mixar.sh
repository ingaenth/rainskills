#!/bin/bash
# Mixagem de peca publicitaria. Dois regimes: com e sem locucao.
#   mixar.sh sem-voz musica.wav efeitos.wav saida.wav [dur]
#   mixar.sh com-voz voz.wav musica.wav efeitos.wav saida.wav [dur]
set -e
FF=$(command -v ffmpeg || echo ./ffmpeg)
MODO=$1; shift
if [ "$MODO" = "sem-voz" ]; then
  M=$1; E=$2; O=$3; D=${4:-30}
  # sem narracao a musica e a peca: fica em primeiro plano
  $FF -y -v error -i "$M" -i "$E" -filter_complex "
   [0]atrim=0:$D,volume=1.0[mus];[1]atrim=0:$D,volume=0.8[fx];
   [mus][fx]amix=inputs=2:normalize=0,
   afade=t=in:d=1.0,afade=t=out:st=$(python3 -c "print($D-1.2)"):d=1.2,
   loudnorm=I=-14:TP=-1.5:LRA=8,alimiter=limit=0.82:level=false[out]" -map "[out]" "$O"
else
  V=$1; M=$2; E=$3; O=$4; D=${5:-30}
  # com narracao: corte o ganho estatico da cama ANTES de contar com o ducking
  $FF -y -v error -i "$V" -i "$M" -i "$E" -filter_complex "
   [1]atrim=0:$D,volume=0.30[mus];[2]atrim=0:$D,volume=0.7[fx];
   [0]volume=1.7,asplit=2[v][k];
   [mus][k]sidechaincompress=threshold=0.10:ratio=5:attack=30:release=450[md];
   [md][fx]amix=inputs=2:normalize=0[cama];
   [v][cama]amix=inputs=2:normalize=0,
   afade=t=in:d=0.8,afade=t=out:st=$(python3 -c "print($D-1.0)"):d=1.0,
   loudnorm=I=-14:TP=-1.5:LRA=8,alimiter=limit=0.82:level=false[out]" -map "[out]" "$O"
fi
echo -n "$O  "
$FF -v info -i "$O" -af loudnorm=print_format=summary -f null - 2>&1 \
  | grep -E 'Input Integrated|Input True Peak' | tr '\n' ' '; echo
