# Motor — `lib.js`

## Estrutura de uma peça

```html
<link href="https://fonts.googleapis.com/css2?family=…&display=block" rel="stylesheet">  <!-- display=block -->
<link rel="stylesheet" href="lib.css">
<style>:root{ --bg:…; --accent:…; --font-display:…; }</style>        <!-- a marca -->
<div id="stage"></div>
<script>window.SIZE=[1920,1080]</script>                             <!-- só para 16:9 -->
<script src="lib.js"></script>
<script src="marca.js"></script>                                       <!-- opcional, do projeto -->
<script>
window.DUR = 25;                          // duração em segundos
const A = scene(0, 6);                    // camada visível só entre 0 e 6 s
…                                         // monte o DOM uma vez
on(t => { … });                           // e descreva cada propriedade como função de t
window.buildAudio = K => { … };           // sons nos mesmos tempos
boot();
</script>
```

**Regra de ouro:** tudo que muda com o tempo é recalculado a partir de `t` em cada `on()`,
inclusive o que "já terminou". Nada de `setTimeout`, `requestAnimationFrame` próprio ou
animação CSS: o render pula de quadro em quadro e o preview pode voltar no tempo.

## Tempo e curvas

| Função | Uso |
|---|---|
| `P(t, a, b)` | progresso 0→1 entre `a` e `b` (travado) |
| `lerp(a, b, k)`, `clamp` | interpolação |
| `E.out`, `E.out5`, `E.in`, `E.inOut` | curvas; `out5` = entrada cinematográfica |
| `E.back` | desacelera e assenta **sem quicar** (padrão seguro) |
| `E.overshoot` | "pop" com passagem do ponto; só se a marca permitir |
| `bump(t, a, d)` | sobe e desce (pulso, clique, flash) |
| `rng(seed)` | aleatório **com semente**: o quadro 812 é sempre igual |

## Elementos

| Função | O que faz |
|---|---|
| `scene(a, b, bg)` | camada com intervalo de visibilidade |
| `div(cls, pai, html)`, `$(tag, …)`, `place(el, x, y, w, h)` | DOM e posição absoluta |
| `T(el, x, y, s, r)`, `O(el, opacidade)`, `txt(el, html)` | transformar, opacidade (esconde abaixo de 0,001), trocar conteúdo só quando muda |
| `reveal(el, t, a, d, dist)` | sobe desfocado → nítido (título, logo) |
| `rise`, `inout` | sobe/entra e sai |
| `words(pai, texto, x, y, w, corpo)` → `.anim(t, a, b, ritmo)` | legenda palavra a palavra; `*x*` destaque, `_x_` amarelo, `~x~` vermelho, `|` quebra |
| `shot(pai, src, x, y, w, h, iw, ih)` → `.set(cx, cy, escala)` | janela sobre print ou vídeo com câmera virtual travada dentro da imagem |
| `glass(pai, src, …)` | o mesmo dentro de uma moldura de vidro com barra de navegador |
| `seekVideo(shot.m, segundos)` | quadro exato de vídeo (chamar dentro de `on`) |
| `tele(pai, d, espessura, cor)` → `(k)` | traço que se desenha (0→1): `wobble(cx,cy,rx,ry)` elipse à mão, `arrow(x0,y0,x1,y1)` |
| `tlabel(pai, texto, x, y)` → `(t, a, b)` | etiqueta de anotação |
| `sweeps([tempos])` | transição: barra na cor `--accent` + véu `--bg` |
| `chIcon(pai, nome, tamanho)` | ícone de canal (whatsapp, instagram, facebook, tiktok, x, threads, gmail, sms, email, call, bell) |
| `endCard(L, a, {logo, headline, cta, note})` | cartão final genérico (logo oficial + frase + botão) |
| classes CSS | `.hx` título (com `<em>` de destaque), `.eyebrow`, `.card`, `.pill`, `.mono` (números tabulares) |

## Padrões de cena que funcionaram

- **Câmera sobre print real**: `glass()` + `.set()` animado entre dois enquadramentos (Ken
  Burns). Mire em regiões com conteúdo, confira a folha: câmera em área vazia é o erro mais comum.
- **Congelar e anotar** (replay): pare o `t` do gráfico ou vídeo, flash branco de 0,25 s,
  círculo `tele(wobble())`, seta e etiqueta. Som: clack + risco de caneta.
- **Fio contínuo**: um `<path>` SVG longo com `stroke-dashoffset` = progresso e um marcador
  em `getPointAtLength()`. Conecta telas e cria continuidade entre cenas.
- **Mundo com câmera**: todas as cenas num `#world` grande; a câmera é
  `translate(W/2,H/2) scale(s) translate(-cx,-cy)`; zoom out final mostra tudo.
- **Contagem**: número `lerp` + `E.out` + `.mono`; bata um tick por passo e um sino no fim.
- **Cursor e clique**: seta SVG, posição por keyframes, `bump` na escala ao clicar e anel
  `.ripple`. Esconda o cursor (`opacity:0`) fora da cena; senão ele fica parado na origem.
- **Celular POV**: moldura de 64 px de raio, barra de status, teclado que acende a tecla digitada.
- **Animação de logo reutilizável**: se o cliente tem animação oficial em código, transforme
  em função `logoAnim(pai, t0, cx, cy, largura)` com o som (`logoSting(K, t0)`), para ela
  nascer da história (as mensagens viram o balão que vira o logo) em vez de ser colada.

## Áudio (`window.buildAudio = K => {…}`)

Sintetizado, sem arquivo e sem direito autoral. Principais: `K.kick, snare, clap, hat, crash,
tom, bass, sub, pad, stab, pluck, keys, bell` (música); `whoosh, riser, impact, thump, pop,
click, type, tick, clock, blip, success, buzz, squeak, clack, whistle, crowd, groan, cheer`
(efeitos); `K.endChord(t)` (fecho). `K.mf(nota MIDI)` → Hz.

- Grade: 120 BPM, compasso de 2 s. Alinhe as entradas de cena a compassos quando puder.
- Estrutura: tensão (drone, ticks) → impacto na revelação → groove nas demonstrações →
  pausa antes do CTA → acorde final no clique.
- **Todo evento visual importante tem um som** no mesmo `t`: aparição (pop), clique, digitação,
  sucesso, alerta, transição (whoosh).
- Volume: o `render.mjs` normaliza em −14 LUFS (Instagram). Não suba demais os kicks.
