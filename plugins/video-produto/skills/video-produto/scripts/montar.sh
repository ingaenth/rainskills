#!/bin/bash
# Compoe cartelas sobre o video e exporta os formatos.
#
#   montar.sh cartelas base.mp4 saida.mp4 c1.png:7:13 [c2.png:14:19 ...]
#       Cada cartela entra e sai com fade de 0.3s nos tempos dados.
#
#   montar.sh formatos master.mp4 prefixo
#       Gera prefixo_16x9.mp4, prefixo_9x16.mp4, prefixo_1x1.mp4.
#       O 9:16 aqui e recorte de emergencia - o certo e gerar com --ar 9:16.
set -e
FF=$(command -v ffmpeg || echo ./ffmpeg)
MODO=$1; shift

if [ "$MODO" = "cartelas" ]; then
  IN=$1; OUT=$2; shift 2
  FILTRO="[0:v]null[v0]"; i=0
  for spec in "$@"; do
    IMG="${spec%%:*}"; R="${spec#*:}"; A="${R%%:*}"; B="${R##*:}"
    FADE_OUT=$(python3 -c "print(round($B-0.3,2))")
    FILTRO="$FILTRO;[$((i+1)):v]format=rgba,fade=t=in:st=$A:d=0.3:alpha=1,fade=t=out:st=$FADE_OUT:d=0.3:alpha=1[c$i]"
    FILTRO="$FILTRO;[v$i][c$i]overlay=0:0:enable='between(t,$A,$B)'[v$((i+1))]"
    ENTRADAS="$ENTRADAS -loop 1 -i $IMG"
    i=$((i+1))
  done
  $FF -y -v error -i "$IN" $ENTRADAS -filter_complex "$FILTRO" -map "[v$i]" \
     -map 0:a? -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a copy -shortest "$OUT"
  echo -n "$OUT  "; $FF -i "$OUT" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p'

elif [ "$MODO" = "formatos" ]; then
  IN=$1; P=$2
  $FF -y -v error -i "$IN" -c copy "${P}_16x9.mp4"
  # 9:16 por recorte central, com o assunto puxado para cima
  $FF -y -v error -i "$IN" -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=720:1280" \
     -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy "${P}_9x16.mp4"
  $FF -y -v error -i "$IN" -vf "crop=ih:ih:(iw-ih)/2:0,scale=1080:1080" \
     -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy "${P}_1x1.mp4"
  for f in "${P}_16x9.mp4" "${P}_9x16.mp4" "${P}_1x1.mp4"; do
    printf "%-22s " "$f"; $FF -i "$f" 2>&1 | grep -oE '[0-9]{3,4}x[0-9]{3,4}' | head -1
  done
  echo
  echo "! o 9:16 saiu de recorte. Se o assunto ficou apertado, gere nativo:"
  echo "  kie.py base <img> <ref> \"<prompt>\" --ar 9:16"
else
  echo "modo desconhecido: use 'cartelas' ou 'formatos'"; exit 1
fi
