# Etapas — do link à pasta de entrega

Crie uma pasta de projeto (`~/projects/<cliente>-video` ou `-launch`) e copie para ela os
arquivos de `scripts/`. Instale o Playwright ali: `npm i playwright && npx playwright
install chromium`.

## 1. Descoberta (30–60 min)

Objetivo: saber **o que o produto é, como a marca se veste e que material real existe**.
Detalhes em `descoberta.md`.

- Texto do site (curl + limpeza) e **screenshot de página inteira** com Playwright.
- Tokens: cores, fontes, raio, sombras (CSS do site, `tailwind.config`, `globals.css`,
  `SPEC.md`, manual de marca).
- Conteúdo com números oficiais (no código, ex. `content.ts`: contadores do site aparecem
  como "0" no HTML estático porque animam no cliente).
- Mídia oficial: logos (SVG), prints do produto, gravações de tela, imagens de ambientação.
  Baixe os **originais** (caminho direto do arquivo), não a versão do otimizador de imagem.
- Faça uma folha de contato com tudo e olhe.

Diga ao usuário, em uma ou duas linhas, o que achou ("6 telas reais, 3 vídeos, logo em SVG,
paleta X"). Isso também mostra que você entendeu o produto.

## 2. Entrevista e BRIEFING.md

Com a descoberta na mão, entreviste o usuário em rodadas curtas (até 4 perguntas por
rodada, cada uma com uma proposta concreta tirada da descoberta): objetivo e onde vai
rodar, idioma, referências e anti-referência, personalidade, regras de marca, material
aprovado, fatos com fonte, CTA, formatos, som e aprovação. Método em `entrevista.md`.

Registre tudo no `BRIEFING.md` (modelo em `briefing-prompt.md`): missão, exibição,
identidade com a fonte de cada token, direção de arte (modo visual, escala tipográfica,
**sequência de fundos das cenas**), conceito, roteiro cena a cena, fatos e textos, assets,
entregáveis e decisões assumidas. Mostre o resumo e peça OK antes do primeiro render longo.

## 3. Conceito (a etapa que mais importa)

Ache a **metáfora nativa do público** e desenhe a estrutura a partir dela. Método,
checklist e exemplos em `conceito.md`; a gramática visual do modo escolhido em
`direcao-de-arte.md`. O conceito entra no briefing (seções 7 e 8).

## 4. Motor da marca

1. Copie `lib.css` e redefina as variáveis com os tokens da marca, num `<style>` da peça ou
   num `marca.css`.
2. Se a marca tem regras de movimento (ex.: "nada quica"), ajuste no `lib.js` do projeto:
   `E.back` já desacelera sem quicar; `E.overshoot` existe para marcas que aceitam "pop".
3. Crie um `marca.js` do projeto quando precisar: logo oficial como função, animação do
   logo reutilizável, elementos gráficos do manual, variantes de cartão final.
4. **Smoke test**: uma página com título, moldura com print real, ícones e cartão final.
   Renderize 2 stills e olhe.

## 5. Peça-piloto

Faça **uma peça inteira você mesmo** antes de paralelizar: ela valida o motor, o tom e o
padrão de qualidade, e vira a referência que os agentes vão copiar.

Loop de produção de cada peça:

```bash
STILLS=0.8,3,6,9,12,15 node render.mjs peca.html   # 5–8 momentos-chave
python folha.py peca 0.8,3,6,9,12,15               # out/peca-folha.png → leia
# corrija o HTML, repita; só então:
node render.mjs peca.html                          # out/peca.mp4
```

Na folha, faça **duas leituras**:

1. **Técnica**: texto cortado ou encostando na borda, zona segura, contraste, câmera
   mostrando área vazia, dado pessoal legível, elemento "fantasma" parado na tela (ex.:
   cursor esquecido na origem), elemento sem posição caído no canto superior esquerdo,
   timing (legenda que ainda não entrou no instante escolhido).
2. **Diretor de arte**, olhando as miniaturas pequenas: as cenas são diferentes entre si?
   cada uma tem um herói legível? a escala é de cartaz? o ritmo de cor bate com o briefing?
   parece desta marca? (checklist completo em `direcao-de-arte.md`). Duas respostas ruins:
   redesenhe a cena, não ajuste pixels.

Revise também **o meio das transições** (extraia quadros do MP4 com
`ffmpeg -ss <t> -i peca.mp4 -frames:v 1`): é onde vídeo em código costuma quebrar.

## 6. Demais peças em paralelo

Com o piloto aprovado, divida as outras peças entre subagentes (`subagentes.md`). Enquanto
eles trabalham, faça capas, thumbnail e o plano de postagem.

## 7. Revisão das peças recebidas

Para cada peça: stills em 6 momentos, folha, leitura. Corrija pequenos detalhes você mesmo
(tamanho de fonte, posição); devolva ao agente o que for estrutural. Um alerta que um agente
levanta (ex.: dado pessoal num vídeo) vai **na hora** para os outros agentes que usam o mesmo
material.

## 8. Entrega

- **Confira antes de anunciar**: `ls -la` e `ffprobe` de cada master (dimensão, duração,
  faixa de áudio). Nenhum README ou mensagem lista arquivo que você não conferiu.
- A pasta de entrega é a do briefing. Não commite vídeo no repositório do site do cliente.
- Versões anteriores ficam com sufixo (`-v1`) e o código delas numa pasta `v1/`.

- `entrega/` com nomes legíveis (`01-nome-da-peca.mp4`), capas em `entrega/capas/`,
  thumbnail, e o `POSTAGEM.md` (`formatos.md`).
- Reels com a capa embutida (`capa-no-video.sh`) e bitrate alto (16 Mb/s).
- Abra a pasta para o usuário (`explorer.exe` no Windows).
- Mensagem final: tabela das peças (tempo, ideia), o que ele precisa conferir (números
  ilustrativos, telas com cores antigas, dados sensíveis encontrados no material público) e
  o que não foi revisado.
