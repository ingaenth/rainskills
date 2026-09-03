#!/usr/bin/env bash
# Roda no SessionStart. Só fala se faltar algo; o que imprimir vai para o contexto do Claude.
falta=()
command -v ffmpeg >/dev/null 2>&1 || [ -x "$HOME/.local/bin/ffmpeg" ] || falta+=("ffmpeg não encontrado")
[ -s "$HOME/.config/kie/key" ] || falta+=("chave do kie.ai ausente em ~/.config/kie/key")
[ ${#falta[@]} -eq 0 ] && exit 0
echo "rainskills: pré-requisitos das skills de vídeo faltando nesta máquina:"
for f in "${falta[@]}"; do echo "  - $f"; done
echo "Resolva com:  curl -fsSL https://raw.githubusercontent.com/ingaenth/rainskills/main/setup.sh | bash"
echo "Avise o usuário antes de usar video-produto, video-local ou filme-de-la."
exit 0
