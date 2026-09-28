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

## 2. Conceito (a etapa que mais importa)

Ache a **metáfora nativa do público** e desenhe a estrutura a partir dela. Método,
checklist e exemplos em `conceito.md`. Apresente o plano ao usuário em uma tabela curta
(peça, papel, gancho) e siga. Se o usuário costuma delegar, não espere aprovação. Se
algo é caro de refazer (ex.: vários filmes longos), confirme o conceito antes.

## 3. Motor da marca

1. Copie `lib.css` e redefina as variáveis com os tokens da marca, num `<style>` da peça ou
   num `marca.css`.
2. Se a marca tem regras de movimento (ex.: "nada quica"), ajuste no `lib.js` do projeto:
   `E.back` já desacelera sem quicar; `E.overshoot` existe para marcas que aceitam "pop".
3. Crie um `marca.js` do projeto quando precisar: logo oficial como função, animação do
   logo reutilizável, elementos gráficos do manual, variantes de cartão final.
4. **Smoke test**: uma página com título, moldura com print real, ícones e cartão final.
   Renderize 2 stills e olhe.

## 4. Peça-piloto

Faça **uma peça inteira você mesmo** antes de paralelizar: ela valida o motor, o tom e o
padrão de qualidade, e vira a referência que os agentes vão copiar.

Loop de produção de cada peça:

```bash
STILLS=0.8,3,6,9,12,15 node render.mjs peca.html   # 5–8 momentos-chave
python folha.py peca 0.8,3,6,9,12,15               # out/peca-folha.png → leia
# corrija o HTML, repita; só então:
node render.mjs peca.html                          # out/peca.mp4
```

Na folha, confira: texto cortado ou encostando na borda, zona segura, contraste, câmera
mostrando área vazia do print, dado pessoal legível, elemento "fantasma" parado na tela
(ex.: cursor esquecido na origem), timing (legenda que ainda não entrou no instante escolhido).

## 5. Demais peças em paralelo

Com o piloto aprovado, divida as outras peças entre subagentes (`subagentes.md`). Enquanto
eles trabalham, faça capas, thumbnail e o plano de postagem.

## 6. Revisão das peças recebidas

Para cada peça: stills em 6 momentos, folha, leitura. Corrija pequenos detalhes você mesmo
(tamanho de fonte, posição); devolva ao agente o que for estrutural. Um alerta que um agente
levanta (ex.: dado pessoal num vídeo) vai **na hora** para os outros agentes que usam o mesmo
material.

## 7. Entrega

- `entrega/` com nomes legíveis (`01-nome-da-peca.mp4`), capas em `entrega/capas/`,
  thumbnail, e o `POSTAGEM.md` (`formatos.md`).
- Reels com a capa embutida (`capa-no-video.sh`) e bitrate alto (16 Mb/s).
- Abra a pasta para o usuário (`explorer.exe` no Windows).
- Mensagem final: tabela das peças (tempo, ideia), o que ele precisa conferir (números
  ilustrativos, telas com cores antigas, dados sensíveis encontrados no material público) e
  o que não foi revisado.
