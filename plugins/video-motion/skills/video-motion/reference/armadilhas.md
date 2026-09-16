# Armadilhas — vídeo de motion

As de plataforma (upload, polling, ffmpeg, áudio) valem das outras skills:
`video-produto/reference/armadilhas.md`. Aqui, o que só aparece com Omni e libass.

## Omni

| Sintoma | Causa | Solução |
|---|---|---|
| Código de cor escrito na tela (`#F1602E` no rodapé, ao lado das formas) | hex no prompt; o modelo o trata como texto a exibir — **2 de 2 testes** | paleta como imagem (`marca.py paleta` / `--paleta`), cores nomeadas no prompt, e `no colour codes` na trava |
| Texto miúdo da interface vira garatuja | tela densa em 720p/1080p | tela com elemento grande (check, número, ícone) ou print real composto em pós |
| Eco/fantasma na transição de texto | o modelo borra a saída de linha | texto por `tipo.py`; no Omni, uma entrada por clipe, sem saída pedida |
| Barra ou mancha por 1–2 frames | artefato transitório | folha de contato de todo clipe; se cair num beat visível, regere com `--seed` diferente ou corte o trecho |
| Objetos multiplicados | `more`, `many`, `fills up` no prompt | conte: `three small circles`; `nothing is added or duplicated` |
| Flat virou fotografia com brilho | `cinematic`, `lighting`, `depth of field` num prompt flat | `vector illustration look, no photorealism, no gradients` |
| Duração diferente da pedida | `--continua`: o modelo decide, `--dur` é ignorado | conte com ~6s e corte no beat |
| Continuação com os defeitos do original | `video_list` herda tudo | só continue clipe limpo; senão, corte seco |
| `flagged by Website as violating content policies`, 0 cr | `audio_ids` (voz Omni) com fala — 2 de 2 | locução por `kie.py tts` em pós |
| Cobrado, mas sem arquivo | queda na rede durante o download | `tarefas.jsonl` guarda o id; `kie.py status <id> --out clipe.mp4` |
| 4K sem ganho visível | composição idêntica, 2,3× o preço | 1080p, que custa o mesmo que 720p |
| Prompt com `@image2` mas só uma `--ref` | numeração é a ordem das refs | `marca.py prompt` imprime a ordem certa; confira antes |

## Keyframes e imagens

| Sintoma | Causa | Solução |
|---|---|---|
| `Internal Error` no nano-banana-pro, 0 cr | recorte WebP com extensão `.png` | `file x.png`; reconverta com ffmpeg (`kie.py imagem` faz sozinho) |
| Keyframe "fintech genérico", não parece a marca | sem post do cliente como referência | `--estilo post.png` no kit e `@image` de estilo em todo K |
| Cena muda entre K_n e K_n+1 | K gerado do zero | gere K_n+1 **a partir de K_n** ("NEXT keyframe of the same scene") |
| Logo ou texto apareceu no keyframe | prompt não vetou | "No text anywhere, no logo, no letters" em todo K; logo entra em pós |
| Título atropela o objeto | área do título não reservada | "the entire left half stays empty" no prompt do K |
| Peça reprovada: "ficou ruim" | identidade do código ≠ identidade dos posts | pergunte qual vale (briefing 2); refaça o kit com a paleta dos posts |

## Logo em pós

| Sintoma | Causa | Solução |
|---|---|---|
| Logo por cima da seta / do badge | canto escolhido sem olhar o plano | escolha o canto **por plano** na folha de contato; mude o canto, não a cena |
| Logo ilegível no fundo escuro | sem cartão | `montar.sh cartao` + logo dentro (`logo_cartao.png`) |
| Logo deformada no vídeo | passou pelo modelo | nunca gere a logo; `logo-anim` em pós |
| Overlay travou o ffmpeg | `-loop 1` sem `-t` | `logo`/`logo-anim` já limitam ao tempo do vídeo |

## libass / tipografia

| Sintoma | Causa | Solução |
|---|---|---|
| `No such filter: 'drawtext'` | build de ffmpeg sem drawtext (o estático do Linux) | é por isso que o texto vai por `.ass`; `cartela.py` da outra skill não roda aqui |
| Fonte errada (fallback) | nome de família não bate com o fontconfig | `fc-list \| grep -i nome`; ou `--fontes pasta/` com o `.ttf` dentro e o nome de família exato no JSON |
| Título mudou de peso sozinho | `peso`/`fonte` eram herdados da linha anterior (uma linha de apoio em regular) | corrigido: só `x, y, corpo, cor, fim, alinh` herdam |
| Linhas se cruzam na entrada | `slide-cima` atravessa a linha de cima | `slide-esq` ou `pop` para blocos empilhados |
| Texto entra enquanto o objeto ainda desliza | `t` na batida, sem olhar o clipe | folha do clipe; atrase o `t` até o objeto assentar |
| Texto pequeno demais no quadro | corpo de legenda | título 14% da altura (150 em 1080p), apoio 4% |
| Texto grande cortado nas bordas | `\pos` centraliza na âncora 5; corpo maior que o quadro | reduza `corpo` ou quebre em duas linhas (`\N` no texto) |
| `queda` passa por cima da linha anterior | é o comportamento: a palavra atravessa | ordene as linhas de cima para baixo, ou use `slide-baixo` |
| Máquina revela rápido demais | `por_letra` em segundos, padrão 0,06 | 0,04 para palavra gigante, 0,08 para frase |
| Cor errada no ASS | ASS é `&HAABBGGRR`, não RGB | `tipo.py` converte; escreva `#RRGGBB` no JSON |
| Fundo não troca | `fundos[0]` é a cor inicial; só os seguintes viram `drawbox` | ponha a cor inicial primeiro e as trocas depois, com `t` crescente |
| Painel some antes de cobrir | `ate` menor que `t + dur` | omita `ate` (padrão `t + dur + 0.05`) e emende um `fundos` na mesma cor em `t + dur` |
| Overlay de logo travou o ffmpeg | `-loop 1` sem `-t` | `montar.sh logo` já limita ao tempo do vídeo |

## Beat e música

- **O Suno ignora o BPM pedido** (pediu 110, veio 158 e 188). Meça e escolha: `atempo`
  até ±5% para casar com a grade, ou adote a grade da música.
- **Clipes encadeados não se cortam nas pontas**: 5 × 6s = 30s, a grade se adapta.

- **Batida detectada errada** (metade ou dobro): `batidas.py musica` acha o pulso mais
  forte; se der 60 onde você ouve 120, use o dobro. Confira de ouvido com cliques.
- **Texto "atrasado"** em relação ao som: o olho lê o pop no fim do overshoot, não no
  começo. Coloque a entrada **0,05–0,08s antes** da batida; `alinhar` aceita `--offset`.
- **Corte no meio da fala** (com locução): a grade manda no visual, não na voz. Deixe
  a frase atravessar o corte; nunca corte a palavra.
- **Dois sons no mesmo beat** viram um só, mais alto. Um evento, um som.

## Formato

- **9:16 não é recorte do 16:9**: a tipografia gigante sai do quadro. Clipes com
  `--ar 9:16`, `tipo.json` com `w:1080, h:1920`, mesmas batidas.
- **Margem inferior de 15% livre** no 9:16 (interface do Reels).
- **1:1** por recorte central serve para feed quando o assunto está no centro.
- O fecho: **2 segundos parados**, sem exceção.

## Conteúdo

- "EXAGERO" é bordão; "40% mais barato" é alegação. Motion empurra para o segundo
  porque cabe numa palavra gigante. Só entra com origem na tela.

## Referência sobrescrita por outro projeto

O upload da kie.ai grava em `images/motion/<nome>`; um nome fixo (`ref_logo.png`,
`ref_paleta.png`) é sobrescrito pelo próximo projeto da mesma conta, e o keyframe sai com a
logo e a paleta **de outra marca** sem nenhum erro. Aconteceu em 03/09/2026 (10 cr). `kie.py`
agora sufixa um hash do conteúdo no nome; mesmo assim, guarde as URLs no `marca.json` e,
se o quadro vier com marca estranha, confira a URL antes de mexer no prompt.

## Grok reescreve texto miúdo

Testado em 04/09/2026 com keyframes HTML (texto exato): em quadro fixo, título, logo e posts
grandes ficam parados; mas rótulos pequenos (nomes de cor sob amostras) foram **reescritos**
com palavras de outra parte do quadro. Grok serve para respiro de quadro fixo com corte seco,
27 cr; não para cartões com texto pequeno. O `extend` continua do último frame com prompt novo,
sem referência do próximo keyframe: não faz a emenda K_n → K_n+1 e inventaria o cartão seguinte.

## Remendo de texto no Grok: de onde tirar o recorte

Quando o Grok reescreve texto miúdo num plano de câmera travada, cubra a área em pós com
`overlay ... enable='gte(t,X)'`. O recorte tem de vir de um **quadro limpo do próprio clipe**
(antes da corrupção): o Grok desloca a geometria uns 25 px e muda o brilho em relação ao
keyframe, e um recorte do keyframe cria uma costura. Quando o clipe já nasce corrompido, use o
keyframe com **borda esfumada** (alfa em rampa nos 60 px do topo, via `geq`) numa área que não
cruze objeto animado. Se a corrupção cresce com o tempo, corte o plano num número inteiro de
batidas antes dela; a grade absorve.
