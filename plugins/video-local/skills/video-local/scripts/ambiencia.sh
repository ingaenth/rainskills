#!/usr/bin/env bash
# Ambiencia sintetizada para peca de negocio local sensorial.
# Nao e biblioteca de efeito de UI: aqui o som E o produto.
# Uso: ambiencia.sh <nome> [segundos] [saida.wav]
set -euo pipefail
FF=$(command -v ffmpeg || echo ./ffmpeg)
N=${1:-listar}; D=${2:-8}; OUT=${3:-$N.wav}
R=44100

case "$N" in
listar)
  cat <<'L'
  agua        agua corrente continua, cama de fundo
  gota        gotas isoladas em bacia, com cauda
  vapor       sopro largo e grave, sem chiado agudo
  tecido      atrito curto de linho, para corte e transicao
  tigela      tigela tibetana, ressonancia longa
  respiracao  ciclo lento de respiracao
  fogo        vela/lareira baixa, crepitar esparso
  sala        room tone quase silencioso, da presenca ao silencio
L
  exit 0 ;;

# ruido rosa filtrado: continuo, sem picos, senta atras de tudo
agua) $FF -y -v error -f lavfi -i "anoisesrc=c=pink:r=$R:d=$D" \
      -af "highpass=f=700,lowpass=f=6500,tremolo=f=0.7:d=0.25,volume=0.28" \
      -ar $R -ac 1 "$OUT" ;;

# impulsos curtos com cauda: uma gota e um clique passado por ressonador
gota) $FF -y -v error -f lavfi -i "anoisesrc=c=white:r=$R:d=$D" \
      -af "highpass=f=1200,lowpass=f=4000,\
adeclick,\
tremolo=f=0.45:d=0.95,\
aecho=0.8:0.85:60|130:0.35|0.2,\
volume=0.22" -ar $R -ac 1 "$OUT" ;;

# grave largo, sem sibilancia: vapor mal se ouve, mas da peso
vapor) $FF -y -v error -f lavfi -i "anoisesrc=c=brown:r=$R:d=$D" \
      -af "lowpass=f=1800,highpass=f=120,tremolo=f=0.25:d=0.4,volume=0.30" \
      -ar $R -ac 1 "$OUT" ;;

# atrito curto para assentar um corte
tecido) $FF -y -v error -f lavfi -i "anoisesrc=c=pink:r=$R:d=$D" -af "highpass=f=1500,lowpass=f=9000,afade=t=in:st=0:d=0.05,areverse,afade=t=in:st=0:d=0.35,areverse,volume=0.35" -ar $R -ac 1 "$OUT" ;;

# fundamental + parciais nao inteiras, com batimento: e isso que soa a metal
tigela) $FF -y -v error \
      -f lavfi -i "sine=frequency=214:r=$R:d=$D" \
      -f lavfi -i "sine=frequency=573:r=$R:d=$D" \
      -f lavfi -i "sine=frequency=1046:r=$R:d=$D" \
      -f lavfi -i "sine=frequency=217:r=$R:d=$D" \
      -filter_complex "[0]volume=0.5[a];[1]volume=0.22[b];[2]volume=0.10[c];[3]volume=0.28[d];\
[a][b][c][d]amix=inputs=4:normalize=0,\
afade=t=in:st=0:d=0.012,volume='exp(-1.1*t)':eval=frame,\
aecho=0.9:0.9:220:0.25,volume=0.45" -ar $R -ac 1 "$OUT" ;;

# ciclo de ~5s: inspira mais curta que expira
respiracao) $FF -y -v error -f lavfi -i "anoisesrc=c=pink:r=$R:d=$D" \
      -af "highpass=f=250,lowpass=f=2600,\
tremolo=f=0.2:d=0.9,volume=0.20" -ar $R -ac 1 "$OUT" ;;

fogo) $FF -y -v error -f lavfi -i "anoisesrc=c=brown:r=$R:d=$D" \
      -af "highpass=f=300,lowpass=f=5000,tremolo=f=6:d=0.55,volume=0.18" \
      -ar $R -ac 1 "$OUT" ;;

# quase nada, mas sem isto o silencio soa a arquivo morto
sala) $FF -y -v error -f lavfi -i "anoisesrc=c=brown:r=$R:d=$D" \
      -af "lowpass=f=400,volume=0.06" -ar $R -ac 1 "$OUT" ;;

*) echo "desconhecido: $N — use 'ambiencia.sh listar'" >&2; exit 1 ;;
esac

echo "$OUT  ($($FF -i "$OUT" 2>&1 | grep -o 'Duration: [0-9:.]*'))"
