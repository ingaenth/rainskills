# Armadilhas catalogadas

Cada uma custou tempo real. Consulte antes de concluir que algo "está fora do ar".

## Grok / kie.ai

| Sintoma | Causa | Solução |
|---|---|---|
| `internal error` em clipe longo, sem cobrar | `resolution: "1080p"` | **Sempre 720p.** O 1080p só funciona até ~6s |
| `internal error` no que funcionava antes | JSON herdou `resolution` de um arquivo anterior | Confira o payload **antes** de culpar o serviço |
| `422 record result error` no extend | tentativa de estender uma **extensão** | Só se estende geração original. Faça nova cadeia |
| `500 extend_times it must be a string` | passou número | `"6"` ou `"10"`, entre aspas |
| `500 syntax error, position at N, name prompt` | aspas do prompt quebraram o heredoc | Monte o JSON com `json.dump`, nunca com heredoc |
| `422 model not supported` | endpoint errado | Grok usa `/api/v1/jobs/createTask`, **não** `/playground/` |
| `403` no upload | falta User-Agent | Upload fica em `kieai.redpandaai.co`, exija UA de navegador |
| Personagem muda de cor entre cenas | referência não passada | Passe o retrato como 2ª imagem em toda geração |
| Aparecem figuras a mais | modelo multiplica elenco | Conte no prompt; se persistir, remova pelo enquadramento |
| Etiquetas e placas ilegíveis | modelo tentou escrever | "no text anywhere"; texto entra em pós |

### Limites reais

- **Não existe first/last frame** no Grok. Só `image_urls` como referência. Para
  encadear, use `extend` ou parta do último frame real.
- `extend_times`: apenas `6` ou `10`. `extend_at`: mínimo 2.
- Em 720p: até 7 imagens de referência. Em 1080p: apenas 1.
- `elevenlabs/sound-effect-v2` estava fora do ar (`internal error`, sem cobrar).
  Sintetize com `scripts/efeitos.sh`.
- Suno exige `callBackUrl` mesmo que você vá consultar por polling; placeholder serve.

## ffmpeg

| Sintoma | Causa | Solução |
|---|---|---|
| Trecho de áudio sai em silêncio (−91 dB) | `-ss` **depois** do `-i` | Seek na **entrada**: `-ss X -t D -i arq` |
| `Output file does not contain any stream` | `concat` sem rótulo de saída | `concat=n=N:v=0:a=1[a]` + `-map "[a]"` |
| `No option name near ...` no drawtext | `:` ou `%` dentro do texto | Use `textfile=arquivo.txt` |
| `Stray %` mesmo usando `textfile=` | drawtext ainda expande o conteúdo | Acrescente `expansion=none` |
| `FileNotFoundError: './ffmpeg'` | scripts procuram o binário na pasta de trabalho | `ln -sf <caminho>/ffmpeg ffmpeg` |
| `Either text, a valid file...` | cadeia de filtros montada por função de shell | Gere o filtro com Python e leia com `$(cat vf.txt)` |
| `Filter has output unconnected` | `split=N` com N maior que os ramos usados | Iguale o `split` ao número de segmentos |
| `Invalid duration for option ss` | `set --` com múltiplos campos no zsh | Passe um argumento por variável |
| `no such file or directory: python3 ...` | comando inteiro guardado em variável no zsh | Guarde só o **caminho**: `S=.../kie.py; python3 $S ...` |
| Arquivo baixado com ~111 bytes | curl salvou a página de erro | Confira o tamanho antes de usar; áudio de 10s tem centenas de KB |
| `moov atom not found` | leu o arquivo antes de o encode terminar | Encadeie com `&&`, não em comandos separados |
| `brew: command not found` mas exit 0 | shell não interativo | Baixe binário estático de evermeet.cx |

## Perda de trabalho ja pago

| Sintoma | Causa | Solução |
|---|---|---|
| Clipes cobrados mas sem arquivo local | queda de rede no download, com o `task_id` só em memória | **Grave o `task_id` em disco no instante da criação**, antes de qualquer polling |
| Nao da para recuperar o resultado | a API nao tem endpoint de listagem de tarefas | Sem o id salvo, o credito e perdido — nao ha como pedir de volta |
| Lote inteiro perdido por um erro no fim | o script so persiste o estado depois de terminar tudo | Persista item a item, nunca ao final do lote |

Regra: **um `json.dump` logo apos cada `createTask`**, com o id e o prompt. Baixar
e opcional e refazivel; perder o id nao e.

## Medição

- **`scene_score` não mede boca.** Detecta corte de cena, não movimento sutil. Para
  boca, recorte a região, converta para cinza 32×32 e some a diferença absoluta
  entre frames consecutivos.
- **O áudio nativo do clipe não indica quando a boca se mexe.** Ele continua depois
  que os lábios param. Meça o pixel.
- **Música por cima da narração é medível, não subjetivo.** Compare voz e cama com
  `medir.py balanco`, sempre **antes** do `loudnorm` — depois dele os dois medem
  igual e o defeito fica invisível. Diferença menor que 8 dB: a voz some.
- **Não estime tempo de fala.** Meça com `silencedetect` e crave os cartões 0,15s
  após o início real de cada frase.
- **Meça a boca sempre contra o vídeo cru.** Medir contra a versão já cortada aponta
  os próprios planos-detalhe, que são estáticos por natureza.
- **Voz off não é descompasso.** Trechos narrados sobre imagem sem locutor em quadro
  aparecem no relatório e devem ser ignorados.

## Voz

| Sintoma | Causa | Solução |
|---|---|---|
| Leitura escorrega para português de Portugal | faltou `language_code` | `"language_code": "pt"` em toda chamada |
| Cada cena com um locutor diferente | `voice` mudou entre blocos | Trave a mesma voz nos quatro blocos |
| `422` no TTS | `speed` fora de 0.7–1.2 | Ajuste o tempo com `atempo` na mixagem |
| Filme entregue com bloco mudo | crédito acabou no meio do lote | Confira o saldo antes: 6 cr por bloco |

## Vídeo

- **`extend` não aceita imagem de referência.** Só o `base` aceita. Close de rosto
  dentro de uma extensão faz o personagem derivar — perde o feltro e volta com outro
  rosto. Câmera aberta nas extensões; o close se faz depois, com `cortar.sh`.
- Uma geração descartada custa menos que um filme inconsistente. Se o boneco mudou,
  refaça o trecho em vez de tentar disfarçar no corte.

## Conteúdo

- Absolvição por falta de provas **é** absolvição. Peça construída sobre "foi
  absolvido, mas mesmo assim" não tem defesa.
- Antes de nomear alguém, cheque se o processo foi **concluído**. Parecer técnico não
  é conta rejeitada.
- No DF já houve cassação por campanha negativa (TRE-DF, 2024, revertida pelo TSE).
  A diferença entre crítica dura legítima e inelegibilidade está no detalhe do que a
  peça afirma.
- **Boneco de pessoa real entra mudo.** Ele aparece, reage, sorri — não fala. O
  silêncio dele diante de um número com fonte constrange mais que qualquer fala
  inventada, e não há o que contestar.
- **Procure o contrafato e coloque-o na peça.** Se o governo anunciou a obra, a
  licitação, a resposta — isso entra. Peça que omite o contra-argumento cai na
  primeira checagem; peça que o inclui e mesmo assim sustenta a crítica é blindada.
- **Feche em pergunta, não em veredito.** "Descaso ou projeto?" é atribuível a quem
  já disse isso publicamente. "Estão sucateando para vender" é afirmação sua, e você
  teria de prová-la.
