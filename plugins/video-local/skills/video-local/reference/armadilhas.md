# Armadilhas — vídeo de produto

As de plataforma valem igual para as duas skills; consulte também
`~/.claude/skills/filme-de-la/reference/armadilhas.md`. Aqui ficam as que só
aparecem quando há uma marca em jogo.

## Marca na imagem gerada

| Sintoma | Causa | Solução |
|---|---|---|
| Logo saiu com outra cor | "reproduce exactly" não trava cor | Diga a cor no prompt: "the logo in pure white" |
| Letras da logo deformadas | referência em baixa resolução | Mínimo 1024px no lado maior |
| Logo com halo escuro | PNG transparente lido com alfa preto | `marca.py kit` assenta num cartão opaco |
| Frase com letra trocada | modelo não soletra | Frase vai por `cartela.py`, sempre |
| Screenshot ilegível na cena | resolução baixa ou plano distante | Screenshot ≥1000px e enquadramento fechado |
| Marca de terceiro na peça | logo de cliente sem autorização | Confirmação por escrito antes |

**Verificado em teste:** logo reproduzida fielmente e URL curta correta, mas a
frase voltou com uma letra trocada (`piloot` no lugar de `piloto`). Palavra curta
passa; frase, não.

## Modelos e filtros

| Sintoma | Causa | Solução |
|---|---|---|
| Saída filtrada por política de IP | nano-banana recusa reproduzir várias marcas de terceiro | Use GPT Image 2 ou Grok — testei os três, só o nano-banana barra |
| Grok multiplica objetos / inventa telas | prompt pediu "more phones appear" | Escreva o oposto: "no new phones appear, nothing is added or duplicated" |
| Grok "melhora" o screenshot e destrói a UI | prompt não travou a interface | "the interface stays perfectly still and legible, nothing inside it scrolls or animates" |
| Locução com sotaque estrangeiro | ElevenLabs no kie.ai não tem voz pt-BR nativa | Gemini TTS com `accent: Neutral` |
| `422 The style parameter is invalid` | enum fechado no Gemini TTS | `Vocal Smile`, `Newscaster`, `Whisper`, `Empathetic`, `Promo/Hype`, `Deadpan` |
| `422 The accent parameter is invalid` | enum só tem variantes do inglês | `Neutral` — o idioma vem do texto |
| Trabalho gerado e cobrado, mas sem arquivo | queda de rede no download, `task_id` só em memória | **Grave o id em disco na criação**, antes do polling. Sem id não há recuperação: a API não lista tarefas |

## Captura e imagens

| Sintoma | Causa | Solução |
|---|---|---|
| `Browser is already in use` | Playwright e Chrome disputam o mesmo perfil | `--user-data-dir=/tmp/chr-$RANDOM` |
| Captura trava a sessão | Chrome headless em foreground | Rode em background e espere o arquivo aparecer |
| Seções internas do site vêm vazias | site animado por scroll | Capture o topo; peça o resto ao cliente |
| Splash às vezes some da captura | `--virtual-time-budget` pega momentos diferentes | Repita com outro valor |
| SVG horizontal sai cortado | `qlmanage` encaixa em quadrado | Renderize no Chrome com o SVG dentro de um HTML dimensionado |
| Instagram: API não devolve a imagem | os MCPs trazem métricas, não arte | `/p/CODIGO/embed/captioned/` no Chrome headless |
| Grid do perfil escurecido | modal de login | Use o embed do post, não a página de perfil |
| Chave por luminância come parte do logo | a parte colorida é mais escura que o fundo | `colorkey` na cor do fundo |

## Composição

| Sintoma | Causa | Solução |
|---|---|---|
| PNG transparente vira retângulo sólido | `pad` e `scale` achatam o alfa | Componha com `overlay`, que respeita |
| Variante monocromática sai chapada | `geq` com `a='alpha(X,Y)'` não lê o alfa | `alphaextract` + `alphamerge` sobre cor sólida |
| PNG salvo sem transparência | encoder caiu para rgb24 | `-pix_fmt rgba` na saída |
| `cropdetect` não devolve nada | precisa de várias passagens | `-loop 1 -t 0.3` na entrada |
| `Cannot write more than one file with the same name` | ler e gravar o mesmo arquivo | Passe por um temporário e `os.replace` |
| PNG estático só aparece no frame 0 | falta `-loop 1 -t <dur>` na entrada | Sempre `-loop 1 -t` ao sobrepor imagem em vídeo |
| `zoompan` demora minutos por clipe | o filtro é pesado em resolução alta | Use `crop` com expressão de tempo — mesma coisa, ~30x mais rápido |
| `height not divisible by 2` | escala com altura ímpar | Arredonde para par |
| Duas cartelas na mesma linha se sobrepõem | janelas de tempo cruzadas | Feche uma antes de abrir a outra |
| Mesma entrada usada duas vezes no filtro | falta `split` | `[0]split=2[a][b]` |
| Saída de imagem única reclama de muxer | filtro devolve mais de um frame | `-frames:v 1 -update 1` |

## Formato

- **9:16 por recorte estraga o enquadramento.** O espaço negativo que você pediu à
  direita some, e o assunto encosta na borda. Gere nativo com `--ar 9:16`; some ~70
  créditos e vale.
- **Margem inferior de 15% livre no 9:16** — é onde a interface do Reels/TikTok cobre.
- O fecho precisa de **dois segundos estáticos**. É o frame que as pessoas fotografam.

## Áudio

- Sem locução, a música é a peça: fica em primeiro plano, sem ducking.
- Com locução, corte o ganho estático da cama **antes** de contar com o ducking, e
  meça o balanço **antes do `loudnorm`** — depois dele os dois medem igual.
- Efeito de interface que se anuncia soa amador. Clique e transição existem para não
  serem notados.
- Evite pedir "epic", "cinematic trailer", "inspiring corporate" ao Suno: devolvem
  clichê. Peça função — "sits quietly under a narrator", "no build, no drop".

## Conteúdo

- **Métrica sem origem não entra.** Ou vem com fonte na tela, ou vira benefício
  qualitativo.
- **Comparativo com concorrente nomeado** sem base documental é notificação na certa.
- **Não gere depoimento.** Rosto e frase de "cliente satisfeito" é fabricação.
- Se o cliente insistir numa alegação insustentável, entregue sem ela e explique.

---

# Armadilhas específicas de negócio local

## Áudio

### `adelay` com um valor só atrasa APENAS o primeiro canal
A que mais custou. Ao montar a narração por posição:

```bash
# ERRADO — o canal 2 de cada fala fica em zero e todas tocam empilhadas na abertura
[0]adelay=900[a];[1]adelay=6900[b]
# CERTO
[0]adelay=900:all=1[a];[1]adelay=6900:all=1[b]
```

O sintoma que o cliente relata é **"áudio sobre áudio, várias falas ao mesmo tempo"**.
Converta tudo para mono e para a mesma taxa **antes** de atrasar — misturar blocos a
48 kHz com um novo a 44,1 kHz dá deriva de sincronia sem nenhum erro na tela.

**Confira medindo, não ouvindo o arquivo inteiro:** a narração isolada tem de dar
−91 dB em cada vão entre falas.

```bash
ffmpeg -ss 4.8 -t 1.9 -i voz.wav -af volumedetect -f null - 2>&1 | grep mean_volume
```

### O zsh come `:l` dentro do filtro
`offset=$OFF:linear=true` vira `0.66inear=true` — `:l` é modificador de parâmetro no
zsh. Use `${OFF}:linear=true` ou escreva o valor literal. O ffmpeg avisa, mas o
comando seguinte roda mesmo assim e o mix sai 1 LU baixo **sem erro visível**.

### `loudnorm` de uma passada erra ~1 LU
Meça com `print_format=json`, depois aplique com os `measured_*`. Numa peça de
ambiência isso importa mais que numa de tecnologia: a cama é quase toda a peça.

## Imagem

### Não invente um spa melhor que o do cliente
Ver `reference/materiais.md`. Eleve a sala real; não gere outra.

### Corpo e pele
O modelo tende a idealizar corpo e a clarear pele. Descreva a pessoa de forma neutra
e **confira o quadro** — uma peça de spa que só mostra um tipo de corpo comunica algo
que o cliente não pediu e não quer.

### Mão é o que mais falha
Mãos em close são o coração deste gênero e o ponto fraco dos modelos. Gere o quadro
de mão **primeiro**, antes de qualquer outro, e esteja pronto para refazer. Dedos a
mais aparecem em cerca de um a cada três.

## Ritmo

### Não monte com ritmo de anúncio de tecnologia
Corte a cada 3s destrói a calma que a peça vende. Plano de 6 a 9s. Se a peça parece
"parada" na revisão, o problema quase sempre é a **trilha**, não a duração do plano.

### `crop` anima x/y, nunca w/h
`crop=w='940*(1-0.035*t)':h=...` devolve *Error when evaluating the expression*: largura e
altura sao avaliadas **uma vez, na inicializacao**; so `x` e `y` sao reavaliados por quadro.
Ou seja, o crop animado da **panoramica, nao push in**. Para aproximar de verdade sem o
`zoompan` (lento demais), gere o plano ja com o movimento no modelo.
