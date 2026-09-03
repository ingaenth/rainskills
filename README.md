# rainskills

Máquina nova, um comando (instala ffmpeg, pede a chave do kie.ai, registra o marketplace e os plugins):

```
curl -fsSL https://raw.githubusercontent.com/ingaenth/rainskills/main/setup.sh | bash
```

Ou à mão, dentro do Claude Code:

```
/plugin marketplace add ingaenth/rainskills
/plugin install video-produto@rainskills
/plugin install video-local@rainskills
/plugin install filme-de-la@rainskills
/plugin install rainskills-setup@rainskills
```

Atualizar: `/plugin marketplace update rainskills`.

A chave do kie.ai fica fora do repositório, em `~/.config/kie/key`.
