---
name: video-produto
description: Produz vídeo de anúncio para empresa de tecnologia — SaaS, app, plataforma, hardware — de 20 a 30s, em 16:9, 9:16 e 1:1. Imagem e vídeo com Grok Imagine, trilha com Suno e locução opcional, tudo no kie.ai; a logo e as telas do produto entram como imagens de referência que o modelo reproduz; só frase e claim são compostos em pós, porque o modelo troca letra. Use quando pedirem vídeo de produto, anúncio, peça institucional, vídeo de lançamento, hero video, demo, vídeo para landing page, criativo para tráfego pago, ou quando mandarem um roteiro de anúncio pedindo "faz o vídeo".
---

# Vídeo de produto

Peça publicitária de tecnologia: **apresenta uma plataforma, não conta uma história**.
A identidade é de cada cliente — logo, cores e referências entram como imagens que o
modelo usa para construir a cena.

Comparta a base técnica com a skill `filme-de-la` (mesmo kie.ai, mesmo Grok, mesmas
armadilhas de ffmpeg). O que muda é a intenção, o ritmo, o som e — principalmente —
a camada de marca.

## Como a marca entra

**Dois modelos, dois papéis. Não misture.**

| | Faz | Não faz |
|---|---|---|
| **GPT Image 2** (`gpt-image-2-image-to-image`) | monta o keyframe **já com o material real dentro da cena** — o post na tela do celular, o dashboard no laptop, a interface do Instagram ao redor | animar |
| **Grok** (`grok-imagine/image-to-video`) | anima o keyframe pronto | inserir conteúdo, desenhar tela, colocar logo |

O prompt do Grok descreve **só o movimento**, e diz explicitamente que a interface
fica parada e legível: *"the interface stays perfectly still and legible, nothing
inside it scrolls, changes or animates"*. Sem isso ele "melhora" a tela e destrói o
screenshot.

**Nunca peça ao Grok para acrescentar coisas.** Frases como "more phones appear" ou
"the feed fills up" fazem ele multiplicar objetos e inventar conteúdo que não
existe. Quando precisar de repetição, escreva o oposto: *"the same five phones
rotate in unison. No new phones appear, nothing is added or duplicated."*

**Uma keyframe nova a cada mudança de composição.** É mais barato e mais previsível
que pedir ao vídeo uma transformação grande.

### O que a IA reproduz bem, e o que ela erra

Testado, não suposto:

| Elemento | Resultado |
|---|---|
| Logo por referência | **fiel** — mas diga a cor, senão ele recoloriza |
| Palavra única, URL curta | costuma sair certa |
| Screenshot real de produto | **fiel**, quando passado como referência ao GPT |
| **Frase inteira** | **erra letra** — `"piloto"` voltou `"piloot"` |

Frase, claim e métrica vão por `cartela.py`, compostos em pós. O resto entra por
referência.

### Filtro de propriedade intelectual

O **nano-banana bloqueia** reproduzir várias peças de marca de terceiro — recusa o
prompt ou filtra a saída. O **Grok e o GPT Image 2 não**. Testei os três: um post
sozinho passa em qualquer um; o conjunto só passa nos dois últimos.

Se um modelo recusar, **teste outro antes de concluir que o caminho é impossível** —
foi assim que eu quase parti para composição manual sem necessidade.

**Confira sempre.** `marca.py conferir quadro.png marca.json` monta o comparativo
entre o original e o que saiu.

**Nunca invente logo, nome, número ou depoimento.** Se faltar, pergunte — e antes de
pedir ao cliente, veja `reference/materiais.md`: quase tudo dá para levantar do site
e das redes sozinho.

## Antes de começar

1. **Chave** em `$KIE_KEY` ou `~/.config/kie/key`.
2. **ffmpeg** disponível. Os scripts caem para `./ffmpeg` na pasta de trabalho — se
   estiver noutro lugar, `ln -sf <caminho>/ffmpeg ffmpeg`.
3. **Briefing.** Leia `reference/briefing.md` e faça as perguntas **antes de gerar
   qualquer coisa**. A identidade visual é de cada empresa: sem as respostas você
   inventa um visual e erra. A pergunta que mais rende: *"me manda de 2 a 5 imagens
   que representem o visual de vocês"* — uma referência vale mais que dez adjetivos.
4. **Kit de marca.** Sem isso não comece — peça:

```
logo.png / logo.svg   fundo transparente, na maior resolução que tiverem
cor primária          hex
cor de fundo          hex
fonte                 arquivo .ttf/.otf (ou o nome, para eu buscar equivalente)
screenshots           telas reais do produto, se o roteiro pedir
claim + CTA           o texto exato, aprovado por eles
URL                   o que vai no fim
```

Monte o kit com tudo junto:

```bash
python3 scripts/marca.py kit \
  --logo logo.png --tela dashboard.png --estilo ref1.jpg --estilo ref2.jpg \
  --primaria "#0B5FFF" --fundo "#0B0D10" \
  --direcao "Dark near-black environment with deep blue volumetric light, abstract
             dimensional glass forms, slow contemplative camera, generous negative space" \
  --evitar "stock-photo office people, holographic UI clichés, rising bar charts" \
  --claim "..." --cta "..." --url "..."
```

Ele apara a moldura transparente da logo, assenta num cartão limpo, avisa se a
resolução é baixa demais, mede contraste, sobe tudo e imprime **o bloco de referências
pronto para colar no início do prompt** — com o mapeamento `@image1`, `@image2`.

`--direcao` e `--evitar` saem do briefing, em inglês descritivo. São eles que fazem a
peça parecer daquela empresa.

## Regras de conteúdo — anúncio tem lei

- **Métrica exige origem.** "Reduz 40% do tempo" só entra com estudo, benchmark ou
  dado do próprio cliente, e com a fonte na tela em corpo menor. Sem origem, troque
  por benefício qualitativo.
- **Nada de comparativo com concorrente nomeado** sem base documental — é o caminho
  mais curto para notificação.
- **Logo de cliente só com autorização.** Peça a confirmação por escrito antes de
  colocar marca de terceiro na peça.
- **Depoimento é de pessoa real** que consentiu. Não gere rosto e frase de "cliente
  satisfeito": é fabricação, e some com a credibilidade da peça.
- **Resultado individual pede ressalva.** "Resultados variam" em corpo pequeno
  resolve.
- Se o cliente insistir numa alegação que você não pode sustentar, **entregue a peça
  sem ela** e diga por quê.

## Estrutura

Anúncio não tem arco narrativo: tem **promessa, prova e chamada**. Uma abertura que
prende, o produto, duas ou três capacidades, uma prova e o fecho.

**Quantos planos e de que tamanho, quem decide é o roteiro** — não uma tabela. Conte
as mudanças de composição que a peça exige e dimensione cada plano pela fala que ele
carrega. A ordem é: escrever a narração, gravar, medir, e **só então** dimensionar
os planos. Fixar o número antes de medir é o que produz fala sobrando ou silêncio
morto.

Ver `reference/planos.md`.

**Máximo três mensagens.** Peça de 30s que tenta dizer cinco coisas não diz nenhuma.
Se o cliente mandar sete bullets, escolha três e diga que os outros quatro viram
outra peça.

O fecho é **estático e legível por dois segundos inteiros**. É o único frame que
alguém vai fotografar.

## Direção visual — escolha uma, não misture

| Direção | Quando serve | O que pedir ao Grok |
|---|---|---|
| **Abstrata dimensional** | infraestrutura, API, dados, segurança | vidro, luz volumétrica, gradientes, geometria flutuando, profundidade |
| **Macro material** | hardware, dispositivo, produto físico | textura em close, reflexo, foco raso, giro lento |
| **Contexto humano** | RH, saúde, educação, vendas | pessoa real trabalhando, luz natural, escritório sem estardalhaço |
| **UI no espaço** | app, dashboard, SaaS | superfícies limpas e vazias onde o screenshot será composto |

Misturar as quatro numa peça de 30s é o erro mais comum e o mais visível.

## Movimento

Anúncio de tecnologia pede **câmera calma e confiante**. Nos prompts:

- "slow deliberate camera push, smooth and steady, cinematic, no shake, no jitter"
- "shallow depth of field, soft volumetric light, clean negative space on the right
  for text"
- **Peça o espaço negativo explicitamente**, do lado onde a cartela vai entrar. É a
  diferença entre texto que assenta e texto que atropela a imagem.
- Nunca peça "stop-motion", "handmade", "felt" — é a linguagem da outra skill.

## Produção por etapas — pare antes de cada salto de custo

**Nunca produza o filme inteiro de uma vez.** Imagem custa 4 a 6 créditos; animar
custa 27. Errar antes de animar é barato, errar depois é caro — então cada ponto de
parada fica imediatamente antes de um salto de custo.

| Parada | Entrega | Protege |
|---|---|---|
| 1 | roteiro com fatos e fontes | a peça inteira, custo zero |
| 2 | voz: uma frase em 2–3 timbres | o tom de tudo |
| 3 | **o primeiro** keyframe | a direção visual, por ~5 cr |
| 4 | **todas** as keyframes, sem animar | 27 cr por plano ruim |
| 5 | **o primeiro** clipe animado | a linguagem de movimento |
| 6 | corte completo | — |

Publique um artifact em cada parada, **no mesmo caminho de arquivo**, para a pessoa
acompanhar num link só. E diga o que você quer que ela olhe: o que está sendo
decidido, o que você já verificou, e **o que você não consegue julgar** — timbre de
voz e naturalidade de sotaque são dela, não suas.

Não é obrigatório parar nas seis. Agrupe pelo risco: cliente novo ou direção
indefinida pede todas; peça curta com direção aprovada pede 1, 4 e 6. Roteiro com
fatos sobre pessoas reais: a parada 1 nunca se agrupa.

**Silêncio não é aprovação.** Detalhes em `reference/etapas.md`.

## Vídeo — mesmas cadeias, mesmos limites

```bash
python3 scripts/kie.py base <cena_url> "<prompt>" --ref <logo_url> --ref <tela_url> \
       --dur 6 --ar 16:9                                                       # 27 cr
python3 scripts/kie.py extend <task_id> 6 10 "<prompt>"                        # 45 cr
```

- **Sempre 720p.** 1080p falha em clipe longo.
- **Só se estende uma geração original**, nunca uma extensão.
- **`extend` não aceita imagem de referência.** Feche o plano depois, com
  `cortar.sh`.
- Cadeia nova começa no último frame real: `ffmpeg -sseof -0.08 -i a.mp4 -frames:v 1 -q:v 2 u.jpg`
- Para 9:16, gere separado com `--ar 9:16`. **Não recorte o 16:9** — o assunto sai do
  quadro e o espaço negativo, que você pediu à direita, deixa de existir.

## Cartelas e composição em pós

Frase, claim e métrica **não** vão pelo modelo — vão por cartela tipográfica, onde
cada letra sai exata:

```bash
python3 scripts/cartela.py texto "Implante em minutos" --marca marca.json --out c1.png
python3 scripts/cartela.py fecho --marca marca.json --claim "Sua infra, no piloto automático" \
        --cta "comece grátis" --url "exemplo.com" --out fecho.png
python3 scripts/montar.sh base.mp4 marca.json saida.mp4 --cartelas c1.png:7:13 --fecho fecho.png:24
```

- Logo em **6% da altura** do quadro, margem de segurança de 5%.
- Cartela entra com fade de 0,3s, **nunca com voo ou giro** — movimento de texto em
  peça de tecnologia envelhece rápido.
- Contraste mínimo 4.5:1 contra o ponto do quadro onde ela assenta. `marca.py` mede;
  se reprovar, use a variante clara ou ponha um véu (`colorchannelmixer` escurecendo
  a área) atrás do texto.
- Screenshot de produto entra com `montar.sh --tela shot.png:8:14:x,y,w` — sempre com
  um leve arredondamento e sombra, senão parece colado.

## Áudio — som macio

Peça de tecnologia **não tem trilha dramática**. Nem tensão, nem épico.

**Música** — `python3 scripts/kie.py musica "<descrição>"`:
- Peça: "calm minimal electronic bed, warm analog pad, soft pulse, gentle arpeggio,
  optimistic but restrained, no drums build, no drop, no vocals, product film
  underscore".
- Evite: "epic", "cinematic trailer", "inspiring corporate" — devolvem clichê.
- Escolha o trecho com `scripts/medir.py musica faixa.mp3`: aqui você quer **menor
  variação**, cama estável. Crescimento dramático é da outra skill.

**Efeitos** — `scripts/efeitos.sh` sintetiza o vocabulário certo: transição suave,
clique de interface, brilho de revelação, subida de pad. Sempre discretos: efeito de
UI que se anuncia soa amador.

**Locução — opcional, e no motor certo.** Só entra se o roteiro pedir.

**Não use o TTS da ElevenLabs no kie.ai para português.** Das 49 vozes daquele
modelo, **nenhuma é nativa em português** — são todas anglófonas lendo com sotaque,
e o resultado soa estrangeiro por mais que se ajuste `language_code`.

Use o **Gemini TTS**, que é multilíngue de verdade e custa **0,66 crédito** por
bloco contra 6 do ElevenLabs:

```json
{"model":"google/gemini-3-1-flash-tts","callBackUrl":"https://example.com/cb",
 "input":{"temperature":1,
  "scene":"Locucao publicitaria em portugues do Brasil.",
  "sample_context":"Narracao brasileira, natural, locutor nativo. Todo o texto e em portugues brasileiro.",
  "speakers":[{"speaker_id":"Speaker 1","voice_name":"Algieba",
    "audio_profile":"Locutor brasileiro, voz calorosa e segura",
    "accent":"Neutral","style":"Vocal Smile","pace":"Natural"}],
  "dialogue_turns":[{"speaker_id":"Speaker 1","text":"..."}]}}
```

- `accent` só aceita variantes do inglês. Use **`Neutral`** e deixe o idioma vir do
  texto — é assim que o modelo acerta o português.
- `style` e `pace` são enums fechados: `Vocal Smile`, `Newscaster`, `Whisper`,
  `Empathetic`, `Promo/Hype`, `Deadpan` · `Natural`, `Rapid Fire`, `The Drift`,
  `Staccato`. Valor fora da lista devolve 422.
- Vozes: `Algieba`, `Charon`, `Orus`, `Kore`, `Puck`, `Fenrir` e outras. **Gere o
  mesmo bloco em duas ou três e deixe quem pediu escolher de ouvido** — você não
  consegue julgar timbre, e diga isso.
- Uma tomada por bloco, mesma voz em todos.

**Mixagem****Mixagem** — `scripts/mixar.sh`:

| | com locução | sem locução |
|---|---|---|
| música | ×0.30, ducking ratio 5 | ×1.0, sem ducking |
| efeitos | ×0.7 | ×0.8 |
| voz | ×1.7 | — |

Sem locução a música é a peça inteira e pode ocupar o primeiro plano. Com locução,
vale a mesma regra da outra skill: **corte o ganho estático antes de contar com o
ducking**, e confira com `medir.py balanco` que a voz fica 10 a 15 dB acima da cama,
**medindo antes do `loudnorm`**.

Fechar em **−14 LUFS / −1,5 dBTP**. Peça publicitária pode ser um pouco mais alta que
documentário, mas acima de −1,0 dBTP distorce nas redes.

## Entrega

Três formatos, do mesmo master:

```bash
scripts/montar.sh exportar master.mp4 --formatos 16:9,9:16,1:1
```

- **16:9** — site, YouTube, apresentação
- **9:16** — Reels, TikTok, Stories. Confira que a cartela não cai atrás da interface
  do app: margem inferior de 15% livre.
- **1:1** — feed

Além dos arquivos: guarde `marca.json`, os prompts e os stems. Publique como artifact
com o vídeo web (`-crf 27`, ~4 MB), a decupagem por tempo e as fontes de cada métrica.
Republique no **mesmo caminho** para manter a URL.

## Custos

| item | créditos |
|---|---|
| imagem | 4 |
| Grok base 6s | 27 |
| Grok extend +10s | 45 |
| voz (por bloco) | 6 |
| Suno | ~10 |
| **peça de 30s, 3 formatos** | **~250** |

O 9:16 gerado à parte soma ~70. Vale: recorte de 16:9 estraga o enquadramento.

## Armadilhas

`reference/etapas.md` traz os pontos de parada e como entregar cada um.

`reference/planos.md` explica como o roteiro determina a quantidade e a duração dos
planos — leia antes de gerar a primeira imagem.

`reference/materiais.md` mostra como levantar logo, cores, prints do site e artes
das redes sociais sem depender do cliente mandar arquivo — e por que captura real
do produto ganha de qualquer geração.

`reference/armadilhas.md` traz o catálogo — inclui as de composição de marca, que são
específicas desta skill. `reference/briefing.md` tem o questionário para arrancar do
cliente tudo que falta antes de gastar o primeiro crédito.
