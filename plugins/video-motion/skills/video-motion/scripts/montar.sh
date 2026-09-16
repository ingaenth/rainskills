#!/bin/bash
# Montagem do motion: corte no beat, tipografia por cima, logo, fundo, exportacao.
#
#   montar.sh cortar    clipe.mp4 <ini> <fim> saida.mp4        recorta (re-encode, corte exato)
#   montar.sh sequencia lista.txt saida.mp4 [LxA] [fps]        concatena clipes, tira o audio
#       lista.txt: um caminho por linha, opcionalmente "caminho ini fim" para cortar na hora
#   montar.sh tipo      base.mp4 roteiro.ass saida.mp4 [pasta_fontes]     aplica o .ass do tipo.py
#   montar.sh logo      base.mp4 logo.png saida.mp4 [ini] [fim] [altura%] [pos]   pos: td te bd be c
#   montar.sh logo-anim base.mp4 logo.png saida.mp4 <ini> <fim> [altura%] [pos] [flutua_px]
#       logo entra com pop e overshoot em <ini>, flutua devagar, encolhe e some em <fim>. pos: td te bd be c
#   montar.sh cartao  LxA raio saida.png                     cartao branco arredondado (PNG com alfa) para logo sobre fundo escuro
#   montar.sh gradiente LxA <dur> "#c0,#c1[,#c2]" saida.mp4     fundo em gradiente animado, custo zero
#   montar.sh audio     video.mp4 mix.wav saida.mp4             casa o master de audio com o video
#   montar.sh exportar  master.mp4 prefixo                       16x9 (copia), 1x1 (recorte central)
#   montar.sh web       master.mp4 saida.mp4                     ~4 MB para artifact
set -e
FF=$(command -v ffmpeg || echo ./ffmpeg)
MODO=$1; shift

dur_de() { "$FF" -i "$1" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p'; }

case "$MODO" in
cortar)
  IN=$1; A=$2; B=$3; OUT=$4
  "$FF" -y -v error -ss "$A" -to "$B" -i "$IN" -an -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "$OUT"
  echo "$OUT  $(dur_de "$OUT")";;
sequencia)
  LISTA=$1; OUT=$2; TAM=${3:-1920x1080}; FPS=${4:-30}
  W=${TAM%x*}; H=${TAM#*x}
  ENT=""; FILT=""; i=0
  while read -r arq a b; do
    [ -z "$arq" ] && continue
    if [ -n "$a" ]; then ENT="$ENT -ss $a -to $b -i $arq"; else ENT="$ENT -i $arq"; fi
    FILT="$FILT[$i:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=$FPS,format=yuv420p,setpts=PTS-STARTPTS[v$i];"
    i=$((i+1))
  done < "$LISTA"
  MAPS=""; for k in $(seq 0 $((i-1))); do MAPS="$MAPS[v$k]"; done
  "$FF" -y -v error $ENT -filter_complex "${FILT}${MAPS}concat=n=$i:v=1:a=0[v]" -map "[v]" \
     -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "$OUT"
  echo "$OUT  $i clipes  $(dur_de "$OUT")";;
tipo)
  IN=$1; ASS=$2; OUT=$3; FONTES=$4
  FD=""; [ -n "$FONTES" ] && FD=":fontsdir=$FONTES"
  "$FF" -y -v error -i "$IN" -vf "ass=$ASS$FD" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a copy "$OUT"
  echo "$OUT  $(dur_de "$OUT")";;
logo)
  IN=$1; LOGO=$2; OUT=$3; A=${4:-0}; B=${5:-9999}; PCT=${6:-8}; POS=${7:-td}
  read W H D < <("$FF" -i "$IN" 2>&1 | python3 -c "
import re,sys; s=sys.stdin.read()
m=re.search(r'(\d{3,4})x(\d{3,4})',s); d=re.search(r'Duration: (\d+):(\d+):([\d.]+)',s)
print(m.group(1),m.group(2),int(d.group(1))*3600+int(d.group(2))*60+float(d.group(3)))")
  LH=$(python3 -c "print(int($H*$PCT/100)//2*2)")
  [ "$B" = "9999" ] && B=$D
  case "$POS" in
    td) X="W-w-W*0.05"; Y="H*0.05";;  te) X="W*0.05"; Y="H*0.05";;
    bd) X="W-w-W*0.05"; Y="H-h-H*0.05";; be) X="W*0.05"; Y="H-h-H*0.05";;
    *)  X="(W-w)/2"; Y="(H-h)/2";;
  esac
  FO=$(python3 -c "print(round($B-0.3,2))")
  "$FF" -y -v error -i "$IN" -loop 1 -t "$D" -i "$LOGO" -filter_complex \
    "[1]format=rgba,scale=-1:$LH,fade=t=in:st=$A:d=0.3:alpha=1,fade=t=out:st=$FO:d=0.3:alpha=1[l];
     [0][l]overlay=x='$X':y='$Y':enable='between(t,$A,$B)'[v]" \
    -map "[v]" -map 0:a? -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a copy -t "$D" "$OUT"
  echo "$OUT  logo ${LH}px em $POS de $A a $B";;
logo-anim)
  IN=$1; LOGO=$2; OUT=$3; A=$4; B=$5; PCT=${6:-8}; POS=${7:-td}; FL=${8:-6}
  read W H D < <("$FF" -i "$IN" 2>&1 | python3 -c "
import re,sys; s=sys.stdin.read()
m=re.search(r'(\d{3,4})x(\d{3,4})',s); d=re.search(r'Duration: (\d+):(\d+):([\d.]+)',s)
print(m.group(1),m.group(2),int(d.group(1))*3600+int(d.group(2))*60+float(d.group(3)))")
  LH=$(python3 -c "print(int($H*$PCT/100)//2*2)")
  # escala por frame: 0 -> 1.15 -> 1.0 na entrada (0.32s); 1.0 -> 0 na saida (0.22s)
  SC="if(lt(t,$A),0.002,if(lt(t,$A+0.18),1.15*(t-$A)/0.18,if(lt(t,$A+0.32),1.15-0.15*(t-$A-0.18)/0.14,if(lt(t,$B-0.22),1,if(lt(t,$B),1-(t-($B-0.22))/0.22,0.002)))))"
  case "$POS" in
    td) X="W-w-W*0.045"; Y="H*0.06";;  te) X="W*0.045"; Y="H*0.06";;
    bd) X="W-w-W*0.045"; Y="H-h-H*0.06";; be) X="W*0.045"; Y="H-h-H*0.06";;
    *)  X="(W-w)/2"; Y="(H-h)/2";;
  esac
  "$FF" -y -v error -i "$IN" -loop 1 -t "$D" -i "$LOGO" -filter_complex \
    "[1]format=rgba,scale=-1:$LH[l0];[l0]scale=eval=frame:w='max(2,iw*($SC))':h='max(2,ih*($SC))'[l];
     [0][l]overlay=x='$X':y='$Y+$FL*sin(2*PI*t/3.2)':enable='between(t,$A,$B)':eval=frame[v]" \
    -map "[v]" -map 0:a? -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a copy -t "$D" "$OUT"
  echo "$OUT  logo animada ${LH}px em $POS, $A -> $B";;
cartao)
  TAM=$1; R=$2; OUT=$3; W=${TAM%x*}; H=${TAM#*x}
  "$FF" -y -v error -f lavfi -i "color=c=white:s=${W}x${H}" -vf "format=rgba,geq=r=255:g=255:b=255:a='255*min(1, lte(abs(X-W/2),W/2-$R)*lte(abs(Y-H/2),H/2) + lte(abs(Y-H/2),H/2-$R)*lte(abs(X-W/2),W/2) + lte(hypot(max(abs(X-W/2)-(W/2-$R),0),max(abs(Y-H/2)-(H/2-$R),0)),$R))'" -frames:v 1 -pix_fmt rgba "$OUT"
  echo "$OUT  cartao ${W}x${H} raio $R";;
gradiente)
  TAM=$1; D=$2; CORES=$3; OUT=$4
  IFS=',' read -r C0 C1 C2 <<< "$CORES"
  C0=${C0#\#}; C1=${C1#\#}; C2=${C2:-$C1}; C2=${C2#\#}
  "$FF" -y -v error -f lavfi -i "gradients=s=$TAM:c0=0x$C0:c1=0x$C1:c2=0x$C2:nb_colors=3:speed=0.015:type=spiral:d=$D:r=30" \
     -vf "gblur=sigma=40" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p "$OUT"
  echo "$OUT  $(dur_de "$OUT")";;
audio)
  V=$1; A=$2; OUT=$3
  "$FF" -y -v error -i "$V" -i "$A" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
  echo "$OUT  $(dur_de "$OUT")";;
exportar)
  IN=$1; P=$2
  "$FF" -y -v error -i "$IN" -c copy "${P}_16x9.mp4"
  "$FF" -y -v error -i "$IN" -vf "crop=ih:ih:(iw-ih)/2:0" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy "${P}_1x1.mp4"
  for f in "${P}_16x9.mp4" "${P}_1x1.mp4"; do printf "%-22s " "$f"; "$FF" -i "$f" 2>&1 | grep -oE '[0-9]{3,4}x[0-9]{3,4}' | head -1; done
  echo "! 9:16 nao sai de recorte: gere os clipes com --ar 9:16 e renderize o tipo.py em 1080x1920.";;
web)
  IN=$1; OUT=$2
  "$FF" -y -v error -i "$IN" -vf "scale='min(1280,iw)':-2" -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k "$OUT"
  ls -la "$OUT" | awk '{print $5/1024/1024 " MB"}';;
*) echo "modo desconhecido: $MODO"; exit 1;;
esac
