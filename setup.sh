#!/usr/bin/env bash
# rainskills — prepara uma máquina nova: ffmpeg, chave do kie.ai, marketplace e plugins no Claude Code.
# uso:  curl -fsSL https://raw.githubusercontent.com/ingaenth/rainskills/main/setup.sh | bash
#   ou: bash setup.sh          (com KIE_KEY=... no ambiente para não perguntar)
set -euo pipefail
REPO="ingaenth/rainskills"; MKT="rainskills"; PLUGINS="video-produto video-local filme-de-la rainskills-setup"
ok(){ printf '  \033[32m✔\033[0m %s\n' "$*"; }; av(){ printf '  \033[33m•\033[0m %s\n' "$*"; }

# 1) ffmpeg estático em ~/.local/bin
BIN="$HOME/.local/bin"; mkdir -p "$BIN"
if command -v ffmpeg >/dev/null 2>&1; then ok "ffmpeg já existe: $(command -v ffmpeg)"
else
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64) A=ffmpeg-darwin-arm64;; Darwin-x86_64) A=ffmpeg-darwin-x64;;
    Linux-x86_64) A=ffmpeg-linux-x64;; Linux-aarch64|Linux-arm64) A=ffmpeg-linux-arm64;;
    MINGW*|MSYS*|CYGWIN*) A=ffmpeg-win32-x64;; *) A="";;
  esac
  if [ -n "$A" ]; then
    av "baixando ffmpeg ($A)…"
    curl -fsSL "https://github.com/eugeneware/ffmpeg-static/releases/latest/download/$A.gz" | gunzip > "$BIN/ffmpeg"
    chmod +x "$BIN/ffmpeg"; ok "ffmpeg instalado em $BIN/ffmpeg"
  else av "não sei baixar ffmpeg para $(uname -s)-$(uname -m); instale à mão"; fi
  case ":$PATH:" in *":$BIN:"*) ;; *)
    for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
      [ -f "$rc" ] && ! grep -q '.local/bin' "$rc" && printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$rc"
    done; av "adicionei ~/.local/bin ao PATH; abra um terminal novo";;
  esac
fi

# 2) chave do kie.ai
KF="$HOME/.config/kie/key"
if [ -s "$KF" ]; then ok "chave do kie.ai já existe"
else
  K="${KIE_KEY:-}"
  if [ -z "$K" ] && [ -t 0 ]; then printf '  chave da API do kie.ai (kie.ai → API Keys): '; read -rs K; echo; fi
  if [ -n "$K" ]; then mkdir -p "$(dirname "$KF")"; printf '%s' "$K" > "$KF"; chmod 600 "$KF"; ok "chave gravada em $KF"
  else av "sem chave: depois rode  mkdir -p ~/.config/kie && echo SUA_CHAVE > ~/.config/kie/key"; fi
fi

# 3) settings do Claude Code: marketplace e plugins obrigatórios
SET="$HOME/.claude/settings.json"; mkdir -p "$HOME/.claude"
python3 - "$SET" "$REPO" "$MKT" $PLUGINS <<'PY'
import json,sys,os
p,repo,mkt,*pl=sys.argv[1:]
d=json.load(open(p)) if os.path.exists(p) and os.path.getsize(p) else {}
d.setdefault("extraKnownMarketplaces",{})[mkt]={"source":{"source":"github","repo":repo}}
ep=d.setdefault("enabledPlugins",{})
for s in pl: ep[f"{s}@{mkt}"]=True
json.dump(d,open(p,"w"),indent=2,ensure_ascii=False); open(p,"a").write("\n")
PY
ok "settings.json com marketplace $MKT e plugins habilitados"

# 4) instala já, se o claude estiver no PATH
if command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add "$REPO" >/dev/null 2>&1 || claude plugin marketplace update "$MKT" >/dev/null 2>&1 || true
  for s in $PLUGINS; do claude plugin install "$s@$MKT" >/dev/null 2>&1 && ok "plugin $s" || av "plugin $s: será instalado ao abrir o Claude Code"; done
else av "claude não está no PATH; ao abrir o Claude Code os plugins entram pelo settings.json"; fi
echo; ok "pronto. Abra o Claude Code e use /video-produto, /video-local ou /filme-de-la"
