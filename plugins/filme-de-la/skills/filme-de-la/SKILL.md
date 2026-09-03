---
name: filme-de-la
description: Produz um curta narrado em stop-motion de lã (~32s, 720p) do roteiro ao master. Imagens com nano-banana, vídeo com Grok Imagine (image-to-video + extend) voz com ElevenLabs Turbo e trilha com Suno — tudo no kie.ai. O áudio é sempre montado por fora do vídeo. Use quando pedirem um vídeo de bonecos de lã, um filme de feltro, um curta em stop-motion, uma peça narrada com bonecos, ou quando mandarem um roteiro pedindo "faz o vídeo".
---

# Filme de lã

Pipeline completo: roteiro → imagem de abertura → cadeias de vídeo no Grok → voz,
música e efeitos por fora → mixagem → verificação medida → master + artifact.

**Um serviço só.** Imagem, vídeo, voz e música vêm todos do **kie.ai**. Não use o
Higgsfield: a conta esgota o crédito no meio de um lote e o filme fica com blocos
faltando. O TTS do kie.ai (`elevenlabs/text-to-speech-turbo-2-5`) é estável e aceita
`language_code`, que é o que evita a voz escorregar para português de Portugal.

**Sempre 720p.** O 1080p do Grok falha em clipes longos.

## Antes de qualquer coisa

1. **Chave.** `echo $KIE_KEY` — se vazio, procure em `~/.config/kie/key`. Se não
   houver, peça ao usuário. Nunca escreva a chave em arquivo do projeto nem a repita
   na conversa.
2. **ffmpeg.** `which ffmpeg` — se faltar, baixe o estático:
   `curl -sL -o ff.zip https://evermeet.cx/ffmpeg/getrelease/zip && unzip -oq ff.zip`
   Os scripts procuram `./ffmpeg` **na pasta de trabalho**. Se o binário estiver em
   outro lugar, faça `ln -sf <caminho>/ffmpeg ffmpeg` dentro da pasta, ou eles falham
   com `FileNotFoundError: './ffmpeg'` no meio da medição.
3. **Pasta de trabalho** versionada: `~/filme-la/<slug>-v1/`. Nunca sobrescreva uma
   versão aprovada.

## Regras de conteúdo — valem sempre

- Afirmação sobre pessoa, empresa ou órgão real exige **documento verificável**, com
  a fonte creditada na tela. Sem documento, o filme trata do **tema**, não da pessoa.
- Distinga **apurado** de **julgado**. "Auditoria aponta" ≠ "contas rejeitadas".
  Escreva na forma mais conservadora que o documento permite.
- Quem narra é **personagem fictícia**. Bonecos podem representar pessoas reais em
  cena, mas nunca dizem frases que a pessoa não disse.
- Se a pesquisa não sustentar a premissa, **diga isso antes de produzir**.

## Decomposição em planos — o roteiro decide

**Não existe número fixo de planos nem duração fixa de plano.** Leia o roteiro,
liste as **mudanças de composição** que a história exige, e é isso que vira a
quantidade de planos.

E a ordem importa: **escreva a narração, grave, meça — e só então dimensione os
planos.** Fixar "6 planos de 6s" antes de medir a fala é o erro que produz 45
segundos de narração dentro de 36 segundos de imagem.

```
duração do plano = fala que ele carrega + 0,6s a 1,5s de respiro
```

Plano sem fala, em que a imagem trabalha sozinha, pede 4 a 6s. Plano de fecho
estático pede 2s parados no mínimo. Uma fala pode atravessar um corte — o que não
pode é sobrar silêncio morto no meio do plano.

**A cauda preta é onde a peça fecha.** Concatene alguns segundos de preto ao fim e
faça a última pergunta cair sobre ele, junto do cartão. A imagem acaba, a voz
continua, e o espectador fica com a pergunta.

Cada bloco carrega **um** fato: o número na fala é o mesmo da tela. O encerramento é
uma imagem-tese que **não conclui** — uma balança que congela no meio pesa mais que
uma que tomba.

O detalhamento está em `reference/planos.md`, inclusive como conseguir cada duração
no Grok e o que fazer quando o orçamento não cobre o roteiro inteiro.

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

## Etapas

### 1. Imagem de abertura

`scripts/kie.py imagem "<prompt>" --out abertura.png`

No prompt, obrigatoriamente:
- **Conte o elenco**: "EXACTLY TWO background puppets and no more — ONE man …, ONE
  woman …. Do not add any other puppet. No duplicates." O modelo multiplica figuras.
- **Coloque agora tudo que precisa existir no fim.** Se a balança aparece no
  encerramento, ela tem que estar no primeiro frame.
- **Nomeie a paleta e o cenário**: "warm knitted sky in horizontal stripes of
  terracotta, dusty rose and deep blue" + marcos do lugar em feltro. Pedir só
  "somber" devolve azul frio sem identidade.
- **"no text anywhere"** — texto gerado vira rabisco.

Para ajustar sem perder a composição: `scripts/kie.py editar abertura.png "<mudança>"`.
Editar preserva; gerar de novo recria tudo.

### 2. Referência de personagem

Recorte o retrato de quem fala e trave a aparência:

```bash
ffmpeg -i abertura.png -vf "crop=iw*0.30:ih*0.85:iw*0.06:ih*0.10" -q:v 2 ref.jpg
python3 scripts/kie.py upload ref.jpg          # devolve a URL
```

**Passe essa URL em toda geração**, descrevendo o que travar: cor do cabelo, do
chapéu, óculos, roupa. Sem isso o personagem troca de cor entre cenas.
Em 720p cabem até 7 imagens de referência (o limite de uma só vale para 1080p).

### 3. Vídeo — tantos planos quantos o roteiro pedir

Dois arranjos, escolhidos pela duração que cada plano precisa ter:

```
planos curtos e independentes   base --dur 6, um por batida, corte seco entre eles
trecho contínuo mais longo      base 6s  →  extend +10s   (16s sem corte)
```

O primeiro dá ritmo e é o que serve para peça com muitas batidas. O segundo serve
quando a ação precisa correr sem corte. **Misture os dois na mesma peça se o
roteiro pedir** — não há obrigação de usar um só.

```bash
python3 scripts/kie.py base  <img_url> <ref_url> "<prompt>" --dur 6   # 27 cr
python3 scripts/kie.py extend <task_id> 6 10 "<prompt>"               # 45 cr
```

**Só se estende uma geração original, nunca uma extensão.** Por isso duas cadeias.

**Nunca planeje close de rosto num `extend`.** O `extend` não aceita imagem de
referência — só o `base` aceita. Quando a câmera fecha num personagem durante uma
extensão, ele deriva: perde a textura de feltro e volta com outro rosto. Mantenha a
câmera aberta nas extensões e **conquiste o close depois**, recortando com
`cortar.sh` um trecho em que o boneco ainda está no modelo certo. Sai mais barato
que refazer e a montagem fica melhor.

A cadeia 2 começa no **último frame realmente renderizado** da cadeia 1:

```bash
ffmpeg -sseof -0.08 -i cadeia1.mp4 -frames:v 1 -q:v 2 ultimo.jpg
python3 scripts/kie.py upload ultimo.jpg
```

Emenda invisível por construção — não por aproximação.

**Em todo prompt de trecho falado:**
- O texto exato em português, entre aspas.
- "TALKS NONSTOP for the entire N seconds, lips moving on every single frame, never
  holding her mouth closed."
- Atuação **descrita como músculo, não como emoção**: "hard indignant face, brows
  drawn down, mouth turned down, jaw tight, never smiling".
- A contagem de elenco, repetida.
- "nothing melts or morphs, the set stays solid to the last frame."

### 4. Áudio — sempre por fora

**Nunca use o áudio do vídeo gerado.** Ele traz uma voz diferente por clipe. Mute e
monte quatro fontes próprias: voz, música, efeitos, ambiência.

**Voz — kie.ai, um bloco por chamada:**

```bash
python3 scripts/kie.py voz "<texto do bloco>" --voz Daniel --out b2.mp3   # 6 cr
```

Usa `elevenlabs/text-to-speech-turbo-2-5` em `/jobs/createTask`, com
`language_code: "pt"` fixo. Sem esse campo a leitura escorrega para português de
Portugal nos blocos longos — foi assim que um filme inteiro precisou ser refeito.

- **Escolha a voz antes de gerar o filme todo.** Gere o mesmo bloco em dois ou três
  timbres, mande para quem pediu e deixe escolher de ouvido. Português brasileiro
  convincente é sorte de preset, não de parâmetro.
- Mesma `--voz` em todos os blocos, senão cada cena ganha um locutor.
- `--vel` aceita 0.7 a 1.2. Fora disso o serviço recusa.
- `style` alto deixa a leitura mais dramática e menos previsível em duração; o padrão
  do script (0.35) é o meio-termo que mede bem.

Regras que valem para qualquer motor:
- **Uma tomada por bloco**, nunca uma leitura corrida — tomada longa degrada no fim.
  Foi isso que produziu a voz ruim no encerramento na primeira tentativa.
- Emoção por tags no texto: `[angry]`, `[indignant]`, `[frustrated]`, `[bitter]`,
  `[firm, accusatory]`.
- **Verifique que as tags não foram faladas**: `scripts/medir.py frases voz.wav` e
  compare a contagem de frases com o esperado. Se bater, foram interpretadas.
- **Apare as pontas antes de calcular o tempo.** Silêncio de entrada e saída some
  com `silenceremove` nos dois sentidos, e muda a conta em mais de um segundo.
- **Meça, some, e só então distribua.** Some as quatro tomadas já aparadas; se
  passarem da duração do filme, ache o fator com uma divisão e aplique `atempo` igual
  em todos. Até 1.18 passa despercebido numa leitura indignada, que sai naturalmente
  lenta. Acima disso, corte texto — não acelere mais.
- Distribua com `adelay` deixando de 0,15s a 0,5s entre blocos, e confira com
  `medir.py frases` que a última frase cai onde você quer.

**Música** — Suno (`scripts/kie.py musica "<descrição>"`):
- Descreva a **função**, não o gênero: "sits quietly under a narrator", "no build,
  no drop, no percussion, no vocals".
- **Diga o registro emocional.** Peça política pede drama, não travessura: cordas
  graves sustentadas, pulso baixo, piano esparso, tensão que sobe. Uma cama alegre
  de pizzicato faz a peça soar como pegadinha, não como denúncia.
- **Escolha o trecho medindo, não ouvindo.** `scripts/medir.py musica faixa.mp3`
  amostra a energia: menor variação para cama neutra, maior **crescimento** para
  tensão dramática.
- Normalize para −23 LUFS e deixe correr a duração inteira.

**Efeitos** — `elevenlabs/sound-effect-v2` estava fora do ar. Teste; se falhar,
sintetize com `scripts/efeitos.sh`, que dá mais controle de posicionamento.

**Mixagem** — `scripts/mixar.sh voz.wav musica.wav efeitos.wav ambiencia.wav saida.wav`

| fonte | ganho estático | ducking |
|---|---|---|
| voz | ×1.7 | — |
| música | ×0.30 | ratio 5 |
| ambiência | ×0.10 | ratio 8 |
| efeitos | ×0.85 | nenhum |

**A cama entra abaixo da voz por construção, não por ducking.** Ducking sozinho não
resolve: se a música já começa acima da narração, abaixá-la um pouco durante a fala
ainda deixa a música por cima. Corte o ganho estático primeiro.

**Meça o balanço, e meça antes do `loudnorm`:**

```bash
python3 scripts/medir.py balanco voz.wav musica.wav efeitos.wav ambiencia.wav
```

Alvo: **voz 10 a 15 dB acima da cama** durante a fala. Medir o master já normalizado
não serve — o `loudnorm` iguala tudo e apaga exatamente a diferença que interessa.

Fechar em **−15 LUFS / −1,5 dBTP** com `alimiter=limit=0.82`. Acima de −1,0 dBTP não
passa limpo nas redes.

### 5. Verificação — obrigatória

**Boca contra voz.** `scene_score` não serve: mede corte, não boca.

```bash
python3 scripts/medir.py boca filme.mp4 voz.wav
```

Lista os trechos em que a narração corre com a boca parada.

**Meça no vídeo cru, antes dos cortes.** Um plano-detalhe é estático por natureza e
dispara o alarme sozinho — se você medir a versão já cortada, vai perseguir um
problema que você mesmo resolveu. Esse erro é fácil de cometer duas vezes no mesmo
filme: depois de trocar a narração, meça de novo **contra o cru**, nunca contra o
corte anterior.

**Narração sobre imagem sem locutor em quadro também é apontada, e é falso positivo.**
O medidor não sabe distinguir voz off de descompasso. Antes de corrigir, confira se
há alguém falando naquele plano; se não há, ignore.

Onde houver descompasso maior que ~1s, **não regere** — corte para detalhe:

```bash
scripts/cortar.sh filme.mp4 9.6 12.7 600:338:420:300 saida.mp4
```

Escolha um objeto que a frase esteja citando. É montagem clássica, não remendo, e
costuma melhorar o ritmo.

**Elenco.** `python3 scripts/medir.py elenco filme.mp4` extrai frames ao longo do
filme para você contar. Se o modelo insistir em inserir figura extra, remova pelo
enquadramento — recorte a faixa onde ela aparece e reescale. Se o corte cair numa
emenda de cadeia, lê como aproximação de câmera.

**Cartões.** Meça o início real de cada frase com `scripts/medir.py frases voz.wav` e
entre com o cartão **0,15s depois**. Nunca estime. Use `textfile=` no `drawtext` e
acrescente **`expansion=none`** — sem isso o `%` do texto quebra o filtro mesmo vindo
de arquivo (`Stray %`).

**Cada cartão sincroniza com o bloco de fala que o cita**, e sai quando o bloco
termina. Cartão de fato pede a fonte embaixo, em corpo menor e opacidade reduzida:
o número sozinho é alegação, o número com origem é apuração.

### 6. Entrega

- Master H.264, `-crf 17`, `yuv420p`, 1280×720.
- Guarde os **stems separados** e os JSONs de cada geração, para refazer um trecho
  sem tocar no resto.
- Publique como artifact com o vídeo embutido, a decupagem por tempo e a nota de base
  factual com as fontes.
- **O master não cabe no artifact.** O limite é 16 MB *depois* do base64, que infla o
  arquivo em 4/3. Gere uma cópia web com `-crf 27 -preset slow` — 35s a 720p ficam
  em ~4 MB, ou ~5,4 MB embutidos — e mantenha o master em CRF 17 no disco.
- Monte o HTML **por script**, substituindo um marcador pelo data URI. Não tente
  escrever megabytes de base64 à mão.
- A página serve para aprovar: abra no vídeo, declare qualquer pendência logo abaixo
  dele, e só então a decupagem com a fonte de cada afirmação ao lado da batida em que
  ela aparece.
- Republique no **mesmo caminho de arquivo** para manter a URL entre versões.

## Quando revisarem

Mudança de áudio quase nunca pede vídeo novo. Antes de gastar crédito, separe o que
é imagem do que é trilha: troca de voz, buraco de narração, sotaque errado e
sincronia de cartão se resolvem só remontando o áudio sobre o mesmo `base35`.

Se a voz precisar ser refeita, **refaça todos os blocos**, nunca só o defeituoso —
dois timbres no mesmo filme soam pior que o problema original.

Você não consegue ouvir o resultado. Diga isso a quem pediu, entregue o corte, e
peça o julgamento de ouvido em vez de afirmar que o sotaque ficou bom.

## Custos

| item | créditos |
|---|---|
| imagem (nano-banana) | 4 |
| Grok base 6s | 27 |
| Grok extend +10s | 45 |
| voz (por bloco) | 6 |
| Suno (2 faixas) | ~10 |
| **curta de 32s completo** | **~220** |

O Grok falha por `internal error` de vez em quando **sem cobrar**. Quando tiver
pressa, dispare duas tentativas em paralelo — a 27 créditos, redundância sai mais
barato que esperar.

## Armadilhas

Leia `reference/armadilhas.md` antes de debugar qualquer falha — quase todo erro
deste pipeline já está catalogado lá, incluindo o `resolution` herdado que faz
parecer que o serviço caiu.

`reference/etapas.md` traz os pontos de parada e como entregar cada um.

`reference/planos.md` explica como o roteiro determina a quantidade e a duração dos
planos — leia antes de gerar a primeira imagem.

O playbook longo, com o racional de cada decisão, está em `reference/pipeline.md`.
