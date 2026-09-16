#!/bin/bash
# Efeitos de motion graphics sintetizados no ffmpeg: whoosh, pop, hit, clique, riser, ding.
# Nada dramatico: whoosh curto e pop seco sao o vocabulario de After Effects.
#
#   efeitos.sh gerar [pasta]                       cria os .wav
#   efeitos.sh timeline <dur> "<nome@t nome@t ...>" saida.wav [pasta]
#       coloca cada efeito no instante pedido (segundos) e mixa numa faixa unica.
#       Ex.: efeitos.sh timeline 20 "pop@0.5 whoosh@1.2 pop@1.5 hit@3.0" fx.wav
set -e
FF=$(command -v ffmpeg || echo ./ffmpeg)
MODO=$1; shift

gerar() {
  OUT="${1:-.}"; mkdir -p "$OUT"
  N() { "$FF" -y -v error -f lavfi -i "anoisesrc=duration=$1:color=$5:amplitude=0.9:sample_rate=48000:seed=$4" \
        -af "$2,alimiter=limit=0.5:level=false,aformat=channel_layouts=stereo" "$OUT/$3"; }
  T() { "$FF" -y -v error -f lavfi -i "sine=frequency=$1:duration=$2:sample_rate=48000" \
        -af "$3,alimiter=limit=0.5:level=false,aformat=channel_layouts=stereo" "$OUT/$4"; }
  # whoosh: ruido rosa com filtro varrendo e envelope em sino (0,45s)
  N 0.45 "bandpass=frequency=900:width_type=h:width=1400,volume='0.9*sin(3.14159*t/0.45)^2':eval=frame" whoosh.wav 11 pink
  # pop: seno curto com queda de tom - o som do 'pop' de escala
  T 520 0.12 "volume='0.9*exp(-22*t)':eval=frame,asetrate=48000*1.0,aformat=sample_fmts=fltp" pop.wav
  # hit: impacto grave seco para corte de fundo
  T 95 0.35 "volume='1.0*exp(-9*t)':eval=frame,lowpass=frequency=400" hit.wav
  # clique: transiente curtissimo de interface
  N 0.06 "bandpass=frequency=2200:width_type=h:width=1200,volume='0.8*exp(-40*t)':eval=frame" clique.wav 33 white
  # riser: ruido subindo em 1,2s, para antes de uma revelacao
  N 1.20 "highpass=frequency=600,volume='0.7*(t/1.2)^2':eval=frame" riser.wav 44 pink
  # ding: brilho de revelacao com cauda
  T 1760 0.9 "volume='0.5*exp(-4*t)':eval=frame,aecho=0.7:0.5:40:0.3" ding.wav
  # normaliza cada efeito para pico de -3 dBFS: o balanco entre eles se faz na timeline
  for f in whoosh pop hit clique riser ding; do
    PK=$("$FF" -i "$OUT/$f.wav" -af volumedetect -f null - 2>&1 | grep -oE 'max_volume: [-0-9.]+' | grep -oE '[-0-9.]+$')
    G=$(python3 -c "print(round(-3.0-($PK),2))")
    "$FF" -y -v error -i "$OUT/$f.wav" -af "volume=${G}dB" "$OUT/$f.n.wav" && mv "$OUT/$f.n.wav" "$OUT/$f.wav"
    printf "%-8s pico %s dB -> -3 dB\n" "$f" "$PK"
  done
}

timeline() {
  DUR=$1; LISTA=$2; OUT=$3; PASTA="${4:-.}"
  ENT=""; FILT=""; i=0; MIX=""
  for item in $LISTA; do
    nome="${item%@*}"; t="${item#*@}"
    ms=$(python3 -c "print(int(round(float('$t')*1000)))")
    ENT="$ENT -i $PASTA/$nome.wav"
    FILT="$FILT[$i]adelay=${ms}:all=1[s$i];"
    MIX="$MIX[s$i]"; i=$((i+1))
  done
  [ $i -eq 0 ] && { echo "nenhum efeito na lista"; exit 1; }
  "$FF" -y -v error $ENT -f lavfi -i "anullsrc=r=48000:cl=stereo:d=$DUR" -filter_complex \
    "${FILT}${MIX}[$i]amix=inputs=$((i+1)):normalize=0:duration=longest,atrim=0:$DUR[out]" \
    -map "[out]" -ar 48000 "$OUT"
  echo -n "$OUT  "; "$FF" -i "$OUT" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p'
}

case "$MODO" in
  gerar) gerar "$@";;
  timeline) timeline "$@";;
  *) echo "uso: efeitos.sh gerar [pasta] | efeitos.sh timeline <dur> \"<nome@t ...>\" saida.wav [pasta]"; exit 1;;
esac
