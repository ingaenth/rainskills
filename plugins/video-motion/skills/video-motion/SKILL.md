---
name: video-motion
description: Produz vídeo de motion graphics para anúncio no nível de post de marca — keyframes desenhados na identidade do cliente e animados entre first frame e last frame pelo Gemini Omni Video (kie.ai), logo sempre em cena, títulos com letra exata, trilha e efeitos no beat. De 15 a 40s, 16:9 e 9:16. Antes de gastar crédito, pergunta cada decisão de produção (texto na imagem ou em pós, logo, motor, formato, referências). Use quando pedirem vídeo de motion, motion graphics, animação de logo, vídeo institucional "estilo After Effects", promo de produto, reveal de marca, vídeo a partir de posts ou de uma identidade visual, ou quando mandarem referências pedindo "faz igual".
---

# Vídeo de motion

Peça gráfica, não filmada: tudo é desenhado, encadeado e cortado no beat. O padrão de
qualidade é **o post de marca do cliente em movimento** — não "um vídeo de IA".

**Um serviço só: kie.ai.** Imagens com `nano-banana-pro`, vídeo com
`gemini-omni-video`, trilha com Suno. O Omni é o motor padrão porque obedece ao
first/last frame; qualquer outro motor só entra se o cliente pedir por nome.

## Duas regras que não se negociam

1. **Nenhum vídeo antes de o cliente ver o roteiro e os frames.** A peça inteira é
   aprovada parada — tabela de planos + folha de contato dos keyframes — num artifact.
   Só depois do "pode gerar" explícito entra o primeiro plano. Vídeo custa 84 por plano
   e não se corrige; quadro custa 18 e se refaz. Silêncio não é aprovação.
2. **O motor é perguntado, com o que a conta tem na hora.** Rode
   `kie.py motores --planos N --formatos F`: ele mostra o saldo, os três motores, o
   custo da peça em cada um e se cabe. Mostre a tabela ao cliente e pergunte. O
   motor escolhido define onde o texto nasce (Omni → na imagem; Veo/Grok → em pós).

## Pergunte antes de gastar o primeiro crédito

Cada item abaixo mudou o resultado em produção. **Pergunte todos, de uma vez, em
linguagem de cliente**, e registre as respostas no `marca.json` / no roteiro. Não
assuma: o padrão da skill está entre parênteses, mas a decisão é do cliente.

1. **Referências.** *"Me manda 2 ou 3 posts ou vídeos que representem a marca."*
   Sem isso o modelo inventa um genérico. (Obrigatório.)
2. **Identidade que vale.** Quando o projeto no disco tem tokens e os posts têm outra
   paleta ou fonte: *"vale a do site ou a dos posts?"* (posts).
3. **Método.** *"Quer que eu desenhe cada quadro antes e anime entre eles, ou que o
   modelo invente a cena?"* (keyframes encadeados, first → last frame).
4. **Texto e logo: quem decide é o motor** (pergunta 11). O gerador dos quadros é a
   pergunta 12. **Omni → dentro da
   imagem**, gerados no keyframe junto com a cena — é o resultado mais próximo do post
   e o melhor já obtido com esta skill. **Veo ou Grok → em pós**, com `tipo.py` e
   `logo-anim`, porque esses motores não seguram a letra parada. Diga isso ao cliente
   junto com a escolha do motor; só mude a regra se ele pedir por escrito.
5. **Quais textos.** As três mensagens, o CTA exato, a URL ou o WhatsApp, e **cada
   número ou métrica com origem** — ou não entra. (máximo três mensagens)
6. **Logo.** *"A logo aparece o vídeo inteiro ou só no fecho? Em que canto? Sobre
   cartão branco no fundo escuro?"* (sempre em cena, canto livre por plano, cartão no
   escuro, animada em pós — nunca gerada pelo modelo)
7. **Fonte.** O arquivo `.ttf`/`.otf` da marca. Sem ele, qual substituta aceita.
8. **Formato e duração.** 16:9, 9:16, os dois? 15, 20, 30s? (16:9 primeiro; a
   duração sai do número de planos × 6s)
9. **Locução.** Com ou sem? (sem; se com, TTS em pós)
10. **Energia.** Calmo, médio, rápido → 90 / 110 / 125 BPM. (médio)
11. **Motor.** *"Omni, Veo ou Grok?"* — depois de rodar `kie.py motores`, com o
    saldo real e o custo da peça em cada um. O padrão recomendado é Omni; a escolha é
    do cliente e fica registrada no roteiro.
12. **Gerador de imagens.** *"Os quadros saem do nano-banana-pro (Google) ou do
    GPT Image 2 (o do ChatGPT)?"* Os dois escrevem português com acento e obedecem
    referência de logo e paleta; o GPT Image 2 custou 10 créditos por quadro 2K contra 18
    (testado, 4/4 limpos, logo exata). `kie.py imagem --modelo gpt-image-2`. (nano-banana-pro)
13. **Orçamento.** Diga o custo antes: ~530 créditos por 30s em um formato.

Se o cliente responder "faz como achar melhor", use os padrões **e diga quais usou**
no artifact da primeira parada.

## Os três motores

| | Gemini Omni (`kie.py omni`) | Veo 3.1 (`kie.py veo`) | Grok Imagine (`kie.py grok`) |
|---|---|---|---|
| first + last frame | por referência (`@image1`/`@image2`) — **obedece, 5/5** | nativo (`FIRST_AND_LAST_FRAMES_2_VIDEO`) — obedece, com mais "câmera" e menos precisão nos ícones | **não tem** last frame: só image-to-video do primeiro |
| clipe | 4/6/8/10s, 1080p nativo | 8s fixos, 720p (1080p por pedido depois) | 6s, 720p (+ extend 10s) |
| custo por plano | 84 (6s) | ~65 (8s) | 27 (6s) |
| som embutido | cama genérica | sim, com efeitos | não |
| texto e logo | **na imagem** (keyframe), ficam parados no plano | em pós (`tipo.py`, `logo-anim`) | em pós (`tipo.py`, `logo-anim`) |
| quando | **padrão** — o melhor resultado obtido: keyframes completos, letra parada, cores exatas | cliente pede "mais cinema", aceita 40s | orçamento curto e cena sem continuidade obrigatória |

Com Grok, a continuidade entre planos se faz por **corte seco no beat** e keyframes
que compartilham a composição; não prometa emenda invisível.

## O método: keyframes encadeados

O melhor resultado desta skill até hoje: **keyframes completos** (cena, título, apoio e
logo dentro da imagem, no estilo dos posts do cliente) animados entre first e last
frame pelo Omni. Texto em pós só quando o motor é Veo ou Grok.

```
K1 ──► K2 ──► K3 ──► K4 ──► K5 ──► K6        6 keyframes, 18 cr cada
 └ S1 ┘└ S2 ┘└ S3 ┘└ S4 ┘└ S5 ┘              5 planos Omni de 6s, 84 cr cada
```

1. **Kit** (`marca.py kit`): logo, recortes de produto (**PNG de verdade** — WebP com
   extensão `.png` devolve `Internal Error`), **paleta como imagem** e os posts do
   cliente em `--estilo`.
2. **K1** com `kie.py imagem` (2K): logo + produto + paleta + um post como `@image`.
   Com Omni, descreva **a cena e o texto**: cada linha do título entre aspas com a sua
   cor, a linha de apoio, e a posição da logo ("bottom right corner", ou "on a white
   rounded card at the bottom" em fundo escuro). Com Veo ou Grok, descreva só a cena e
   **a área vazia para o título**, sem texto e sem logo.
3. **Cada K nasce do anterior**: `--ref K_n` + *"Produce the NEXT keyframe of the same
   scene, same camera, same lighting, same render style. Changes: …"*. Para trocar de
   ambiente (claro → escuro) use um post escuro como referência e nomeie o elemento
   que carrega a transição.
4. **Folha de contato dos K** e parada. Trocar um K custa 18.
5. **Planos** no motor escolhido. Omni: `kie.py omni --ref K_n --ref K_n+1`, prompt
   começando por *"@image1 is the FIRST frame of this shot and @image2 is the LAST
   frame. The video must start exactly on @image1 and end exactly on @image2, same
   camera, same render style. Between them: …"*, 6s, 1080p. Veo: `kie.py veo "<prompt>"
   --primeiro K_n --ultimo K_n+1`. Grok: `kie.py grok K_n "<prompt>"`, e o K_n+1 vira
   o primeiro frame do plano seguinte.
6. **Concatene os clipes inteiros**: o último frame de S_n é o primeiro de S_n+1. A
   grade de beats se ajusta ao clipe, nunca o contrário.
7. Títulos, logo, efeitos e mixagem em pós, custo zero.

## Keyframes em HTML — quando o conteúdo é real

Se o que aparece nos cards são **posts, telas, dados ou fotos reais** do cliente (calendário da
semana, Brand Kit, estratégia, produto com texto), não peça ao gerador de imagem para
reproduzi-los: ele aproxima e inventa. Monte o keyframe em **HTML/CSS** com os tokens da marca,
a fonte real e os arquivos reais, e renderize a 1080×1920 (DSF 2) no Chromium do Playwright
(`playwright-core` + `~/.cache/ms-playwright`). Identidade pixel a pixel, texto exato, custo zero
por quadro e por troca; o Omni anima entre eles do mesmo jeito. O gerador de imagem fica para
cena, objeto e ambiente. Peça de referência: Find Business v3 (`~/projects/find/deliverables/
motion-conteudo-ia/keyframes/html`). Alterne, como a mLabs, **frase-tese → demonstração real**.

## Logo em cena

Com **Omni**, a logo está no keyframe (a pergunta 6 define onde) e o prompt do plano
diz que ela fica parada: *"the logo stays perfectly still and sharp the whole time"*.
No fecho, o K final já desenha o cartão com a logo (peça margem, senão sai cortada).

Com **Veo ou Grok**, a logo entra em pós, animada:

```bash
scripts/montar.sh cartao 1500x520 60 cartao.png            # cartão branco arredondado com alfa
ffmpeg -i cartao.png -i logo.png -filter_complex "[1]scale=1222:-1[l];[0][l]overlay=(W-w)/2:(H-h)/2" -pix_fmt rgba logo_cartao.png
scripts/montar.sh logo-anim base.mp4 logo.png        s1.mp4 0.4  14.25 9  td 5   # trechos claros
scripts/montar.sh logo-anim s1.mp4   logo_cartao.png s2.mp4 14.45 25.6 10 te 4   # trechos escuros
scripts/montar.sh logo      s2.mp4   logo.png        s3.mp4 26.6 30 11 c        # fecho, no cartão da cena
```

- `logo-anim`: pop com overshoot, flutuação lenta, encolhe na saída.
- **Canto escolhido por plano, olhando a folha de contato**: precisa estar livre de
  objeto, seta e badge o plano inteiro. Um canto que serve no plano claro pode colidir
  com a cena no plano escuro — mude o canto, não a cena.
- Fundo escuro → cartão branco atrás. Fecho → o keyframe final já desenha o cartão
  vazio no centro; a logo assenta nele.

## Texto — quem decide é o motor

### Omni: texto na imagem (padrão)

Testado, 5/5 planos limpos, o resultado mais próximo do post de marca:

- No keyframe: cada linha do título entre aspas com a cor de cada linha, a linha de
  apoio, e *"Spell every word exactly as written, with the accents"*. O
  nano-banana-pro escreve português com acento; o post do cliente como referência dá
  a fonte e a hierarquia (título grande, apoio fino).
- No K seguinte da mesma cena: *"EXACTLY the same headline text, support line,
  fonts, colours and positions … unchanged"*.
- No plano, texto que **fica**: *"the headline and the logo are IDENTICAL in both
  frames: they stay perfectly still, sharp and legible, not a single letter changes"*.
  Texto que **muda**: *"the old headline lines slide out to the left one by one, then
  the new lines slide in from the left, each arriving crisp and exactly as in
  @image2, with no letter morphing"*. Sai um slide com motion blur, estilo After
  Effects.
- Logo: *"reproduce it EXACTLY, complete, never cropped"*; no cartão do fecho, peça
  margem (*"about 60 percent of the card's width, generous margin, the whole word
  including the final letter visible"*).
- Objetos com superfície (moedas, cartões): *"plain, blank, no letters or symbols"*.
- Cada erro custa 18 (quadro) + 84 (plano): **aprove os seis quadros antes de animar**.

### Veo ou Grok: texto em pós (`tipo.py`, libass)

- Keyframes **sem texto e sem logo**, com a área do título vazia.
- **Título em 14% da altura** (corpo 150 em 1080p), apoio em 4%. Fonte real da marca
  em `fontes/` (`fc-scan` dá o nome; Montserrat estática vem do repositório da
  fundição, não do `google/fonts`).
- **Uma linha por evento**; entrada `slide-esq` ou `pop`; saída `fade`. Só depois do
  objeto assentar — olhe a folha do clipe e atrase o `t`.
- `fonte` e `peso` não são herdados entre linhas; `x, y, corpo, cor, fim, alinh` são.
  Um JSON por formato.

## O que o Omni faz — testado

| Pedido | Resultado |
|---|---|
| **First + last frame por `@image1`/`@image2`** | **obedece** — 5/5, inclusive wipe claro → escuro |
| Flat 2D: pop, overshoot, fly-in, splash | excelente |
| Texto e logo vindos do keyframe | **parados e nítidos** quando iguais nos dois frames; slide com blur quando mudam (5/5) |
| Texto pedido só no prompt, sem keyframe | letra certa até 4 linhas; **eco na saída** — não use |
| Logo/produto por referência | fiel; **texto miúdo de tela embaralha** |
| Paleta como imagem | cores exatas, nada de código |
| **Hex no prompt** | **vira texto na tela** (2/2) |
| `--continua` | emenda perfeita; 2×; herda defeitos |
| Narração por `audio_ids` | barrada por política (2/2) → TTS em pós |
| 1080p | mesmo preço do 720p — sempre 1080p |
| Áudio embutido | cama genérica; descarte |

~1 min por clipe. Artefatos de 1–2 frames existem: folha de contato de **todo** clipe.

## Custos

| item | créditos |
|---|---|
| keyframe `nano-banana-pro` 2K | 18 |
| keyframe `gpt-image-2` 2K (`--modelo gpt-image-2`) | 10 — testado, 4/4 limpos |
| Omni 4 / 6 / 8 / 10s | 63 / 84 / 105 / 126 |
| Omni 4K / `--continua` | ×2,3 / ×2 |
| Suno / TTS por bloco | 10 / 0,66 |
| pós (texto, logo, efeitos, mix) | 0 |
| **30s em um formato** | **~530** |

## O beat manda — mas a música manda no beat

O Suno **ignora o BPM pedido**. Meça (`batidas.py musica`) e escolha: esticar a música
até ±5% com `atempo`, ou adotar a grade da música (ex.: 160 BPM → batida 0,375s, 6s =
16 batidas). Texto e efeitos caem em múltiplos da batida; cortes de plano caem no fim
do clipe inteiro. `efeitos.sh timeline` põe um som por evento; `mixar.sh sem-voz`
fecha em −14 LUFS.

## Produção por etapas

| Parada | Entrega | Custa |
|---|---|---|
| 1 | respostas às 12 perguntas + roteiro de planos (o que cada K mostra, o que move, o que o texto diz) + kit | 0 |
| 2 | **K1** | 18 |
| 3 | **todos os K** em folha de contato + roteiro de planos — **parada obrigatória, espera o "pode gerar"** | ~108 |
| 4 | **S1** animado | 84 |
| 5 | corte completo com texto, logo e som | ~340 |

Artifact em cada parada, no mesmo caminho, dizendo o que olhar. Se o cliente reprovar
com "ficou ruim", pergunte **o que**: quase sempre é "não parece o meu post" — volte
às referências, não ao prompt.

## Montagem

```bash
scripts/montar.sh sequencia lista.txt corte.mp4 1920x1080 30
scripts/montar.sh tipo corte.mp4 tipo.ass corte_tipo.mp4 fontes/
scripts/montar.sh logo-anim … / cartao … / logo …
scripts/montar.sh audio corte_logo.mp4 mix.wav master_16x9.mp4
scripts/montar.sh web master_16x9.mp4 web.mp4
```

Guarde `marca.json`, `keyframes/`, `tipo*.json`, `tarefas.jsonl`, prompts e stems.
Entregue o artifact com o vídeo, a tira dos keyframes, a decupagem e o custo real.

## Regras de conteúdo

Métrica só com origem; concorrente nomeado só com documento; logo de terceiro só com
autorização; depoimento só de pessoa real; ressalva quando o resultado varia.

## Referência

- `reference/briefing.md` — as perguntas, com o porquê de cada uma, e como ler referências.
- `reference/prompts.md` — prompts testados: keyframes, first/last, flat, 3D.
- `reference/batidas.md` — grade, decupagem de referências, estrutura de planos.
- `reference/etapas.md` — paradas. `reference/armadilhas.md` — catálogo.
- `reference/materiais.md` — kit a partir do projeto, fontes, posts.
