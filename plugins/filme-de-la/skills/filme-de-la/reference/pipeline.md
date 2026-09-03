# PROMPT BASE — Curta em stop-motion de lã (kie.ai + Grok Imagine)

Você vai produzir um curta de ~32 segundos em stop-motion de lã, do zero, seguindo
exatamente este método. O roteiro vem depois deste prompt. Não pule etapas de
verificação: quase todo defeito deste pipeline só aparece quando medido.

---

## 0. Regras invioláveis

- **Nada de acusação sem fonte.** Se o vídeo trata de pessoa, empresa ou órgão real,
  cada afirmação precisa de documento verificável (tribunal de contas, decisão
  judicial, relatório oficial, registro de votação, matéria de imprensa). Cite a
  fonte na tela. Se não houver documento, o vídeo fala do **tema**, não da pessoa.
- **Não invente falas na boca de pessoa real.** Quem narra é uma personagem
  fictícia. Bonecos que representem pessoas reais aparecem em cena, mas não dizem
  frases que a pessoa nunca disse.
- **O que o modelo entrega precisa ser medido, não presumido.** Sincronia labial,
  contagem de personagens, presença de música — tudo se verifica com ffmpeg antes
  de entregar.

---

## 1. Pesquisa

1. Levante o registro público sobre o assunto. Busque tanto o que sustenta quanto o
   que contradiz a premissa.
2. Separe **fato apurado** de **fato julgado**. "Auditoria aponta" ≠ "contas
   rejeitadas". Escreva o roteiro na forma mais conservadora que o documento
   permite.
3. Anote para cada número: valor, órgão, ano, situação processual.
4. Se a pesquisa não sustentar a premissa, **diga isso** antes de produzir.

---

## 2. Roteiro e orçamento de tempo

- Duração alvo: **32s** (duas cadeias de 16s).
- Fala útil: **~23s**. Não tente encher os 32s de narração.
- Divida em **3 blocos de fala** de ~7,5s cada, separados por respiros.
- Abertura sem fala: 4 a 6s. É o que estabelece o mundo.
- Cada bloco carrega **um** fato. Número na fala e número na tela, iguais.
- Encerramento: uma imagem-tese que não conclui (uma balança que congela no meio,
  uma porta que não fecha). Peça que não afirma pesa mais que peça que grita.

---

## 3. Imagem de abertura (nano-banana)

Endpoint: `POST https://api.kie.ai/api/v1/playground/createTask`
Modelo: `google/nano-banana` · 4 créditos · `image_size: "16:9"`

No prompt da imagem, seja explícito sobre:

- **Contagem de elenco.** Escreva "EXACTLY TWO background puppets and no more — count
  them carefully: ONE man … and ONE woman …. Do not add any other puppet. No
  duplicates, no crowd." O modelo multiplica figuras se você não contar por ele.
- **Objetos que precisam estar desde o frame 1.** Se a balança tem que aparecer no
  final, ela tem que estar no começo. Coloque no quadro agora.
- **Paleta e cenário nomeados.** "warm knitted sky in horizontal stripes of
  terracotta, dusty rose and deep blue" + os marcos do lugar em feltro. Se você
  pedir só "somber", ele devolve azul frio e perde a identidade.
- **Sem texto.** "no text anywhere" — etiquetas viram rabisco ilegível.

Para ajustar sem perder a composição, use `google/nano-banana-edit` passando a
imagem anterior em `image_urls`. Editar preserva; gerar de novo recria tudo.

---

## 4. Referência de personagem

1. Recorte o retrato do personagem que fala, de um frame já aprovado:
   `ffmpeg -i frame.png -vf "crop=iw*0.30:ih*0.85:iw*0.06:ih*0.10" ref.png`
2. Converta para JPG e faça upload:
   `POST https://kieai.redpandaai.co/api/file-base64-upload`
   corpo: `{"base64Data":"data:image/jpeg;base64,…","uploadPath":"images/x","fileName":"ref.jpg"}`
   (endpoint fica em **outro host**; use `User-Agent` de navegador ou dá 403)
3. **Passe essa imagem em toda geração**, descrevendo o que travar: cor do cabelo,
   do chapéu, óculos, roupa. Sem isso o personagem muda de cor entre cenas.

---

## 5. Vídeo — Grok Imagine

Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
Consulta: `GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=…`

| Modelo | Uso | Custo |
|---|---|---|
| `grok-imagine/image-to-video` | base da cadeia | 27 cr (6s) · 135 cr (30s) |
| `grok-imagine/extend` | continuar a base | 45 cr (+10s) |

**Armadilhas confirmadas:**

- **1080p falha em clipe longo.** Acima de ~6s dá `internal error` sem cobrar. Use
  **720p** para qualquer coisa longa. *(Se um JSON herdar `resolution:"1080p"` de um
  arquivo anterior, você vai perseguir um fantasma. Confira antes de culpar o
  serviço.)*
- **Não existe first/last frame.** Só `image_urls` como referência.
- **Só se estende uma geração original**, nunca uma extensão. Logo: base + 1 extend
  por cadeia.
- `extend_times` é **string** (`"6"` ou `"10"`), não número.
- Monte o JSON com um serializador. Aspas dentro do prompt quebram heredoc.
- Em 720p cabem **até 7 imagens** de referência; o limite de uma só vale para 1080p.

**Estrutura de 32s:**

```
cadeia 1:  base 6s  →  extend +10s   (0–16s)
cadeia 2:  base 6s  →  extend +10s   (16–32s)
```

A cadeia 2 começa no **último frame realmente renderizado** da cadeia 1:
`ffmpeg -sseof -0.08 -i cadeia1.mp4 -frames:v 1 -q:v 2 ultimo.jpg`, upload, e use
como `image_urls[0]`. Emenda invisível por construção.

**No prompt de cada trecho, sempre:**

- O texto exato em português que ela diz, entre aspas.
- "TALKS NONSTOP for the entire N seconds, lips moving on every single frame, never
  holding her mouth closed."
- Atuação: "hard indignant face, brows drawn down, never smiling" — descreva o rosto,
  não a emoção. Nomear emoções ajuda menos que descrever músculos.
- A contagem de elenco, repetida.
- "nothing melts or morphs, the set stays solid to the last frame."

---

## 6. Áudio — sempre por fora

**Nunca use o áudio do vídeo gerado.** Ele traz uma voz diferente por clipe. Mute e
construa a trilha com quatro fontes próprias.

### Voz

kie.ai `/jobs/createTask`, modelo `elevenlabs/text-to-speech-turbo-2-5`, com
`language_code: "pt"` — via `scripts/kie.py voz`. 6 créditos por bloco.

O Higgsfield foi abandonado aqui: além de ser um segundo serviço para manter, o
crédito acabou no meio de um lote de quatro blocos e o filme foi entregue com uma
tomada faltando. Um serviço só, um saldo só para conferir.

- **Uma tomada por bloco de fala**, não uma leitura corrida. Tomada longa degrada no
  fim.
- Mesma `voice` em todos os blocos garante consistência.
- `language_code` não é opcional. Sem ele a leitura escorrega para português de
  Portugal justamente nos blocos longos do fim, que é onde ninguém revisa.
- Teste dois ou três presets no mesmo texto antes de fechar o filme; quem pediu
  escolhe de ouvido.
- Emoção por tags no texto: `[angry]`, `[indignant]`, `[frustrated]`, `[bitter]`,
  `[firm, accusatory]`. **Verifique que não foram faladas**: conte os segmentos de
  fala com `silencedetect` e compare com o número de frases esperado.
- Apare silêncio nas pontas:
  `silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05` aplicado
  também em reverso.
- Se faltar tempo, `atempo` até 1.18 é imperceptível numa leitura indignada, que sai
  naturalmente lenta.

### Música

Suno via `POST https://api.kie.ai/api/v1/generate` (`instrumental:true`,
`callBackUrl` é **obrigatório** — pode ser placeholder; consulte por
`/api/v1/generate/record-info`). Retorna duas faixas de ~4min.

- Descreva a **função**, não o gênero: "sits quietly under a narrator", "no build, no
  drop, no percussion, no vocals".
- **Escolha o trecho medindo**, não ouvindo: amostre `volumedetect` a cada 30s. Para
  cama neutra, pegue o trecho de menor variação; para tensão dramática, pegue o de
  maior **crescimento** de energia ao longo da janela.
- Normalize para `-23 LUFS` e deixe correr a duração inteira.

### Efeitos

`elevenlabs/sound-effect-v2` estava **fora do ar** (`internal error`, sem cobrar).
Teste antes; se falhar, sintetize — dá mais controle de posicionamento:

```bash
ffmpeg -f lavfi -i "anoisesrc=duration=0.75:color=pink:amplitude=0.9:sample_rate=48000" \
  -af "bandpass=frequency=2400:width_type=h:width=1600,volume='0.05+0.55*pow(t/0.75\,2)':eval=frame" fio.wav
```
Varie banda e envelope: agudo com ataque crescente = fio puxado; grave em senoide =
tecido roçando; ruído alto com decaimento = poeira; banda estreita com `vibrato` =
rangido.

### Mixagem

```
voz          → referência
música       → ducking LEVE (ratio 1.8–2.5) para baixar sem sumir
ambiência    → ducking FORTE (ratio 6) para sair da frente
efeitos      → sem ducking
```
Fechar em **−15 LUFS / −1,5 dBTP**, com `alimiter=limit=0.82` no final. Acima de
−1,0 dBTP não passa limpo nas redes.

---

## 7. Verificação obrigatória

### Boca contra voz

`scene_score` **não serve** — mede corte, não boca. Meça o pixel:

```bash
ffmpeg -i filme.mp4 -vf "crop=520:300:380:60,format=gray,scale=32:32,fps=12" -f rawvideo boca.raw
```
Some a diferença absoluta entre frames consecutivos, agregue em janelas de 0,5s e
cruze com as janelas em que a narração está tocando. Movimento abaixo de ~1,6 com voz
correndo = boca parada.

### Correção: corte para detalhe

Onde houver descompasso, **não regere** — desvie a câmera. Corte para um objeto da
cena com `crop` + `zoompan`, mantendo 16:9. Escolha um detalhe que a frase esteja
citando: o cofre arrombado, o novelo escondido, a balança. É montagem clássica, não
remendo — e costuma melhorar o ritmo.

### Elenco

Amostre 5 a 8 frames ao longo do filme e **conte os personagens**. Se o modelo
insistir em inserir figuras extras, remova pelo enquadramento: recorte a faixa onde
a intrusa aparece e reescale. Se o corte cair numa emenda de cadeia, lê como
aproximação de câmera.

### Cartões de texto

Meça o início real de cada frase com `silencedetect` na trilha de voz e entre com o
cartão **0,15s depois**. Nunca estime. Use `textfile=` no `drawtext` — `:` e `%` no
texto quebram o parser inline.

---

## 8. Custos de referência

| Item | Custo |
|---|---|
| Imagem (nano-banana) | 4 cr |
| Grok base 6s | 27 cr |
| Grok extend +10s | 45 cr |
| Grok 30s (720p) | 135 cr |
| Veo 3 8s 1080p | ~400 cr |
| Voz (por bloco) | ~1 cr |
| Suno (2 faixas) | ~10 cr |

Curta de 32s completo pelo método acima: **~200 créditos**. O mesmo filme em Veo 3
custou ~4.400. O Grok falha mais (erros intermitentes que não cobram), então
dispare duas tentativas em paralelo quando tiver pressa.

---

## 9. Entrega

- Master em `.mp4`, H.264, `-crf 17`, `yuv420p`.
- Guarde os **stems separados** (voz, música, efeitos, ambiência) e os JSONs de cada
  geração, para refazer um trecho sem tocar no resto.
- Publique como artifact com o vídeo embutido, a decupagem por tempo e a nota de
  base factual com as fontes.
- Versione: `v1-…`, `v2-…`. Nunca sobrescreva uma versão aprovada.

---

# ROTEIRO

*(cole abaixo o roteiro do vídeo desta vez)*
