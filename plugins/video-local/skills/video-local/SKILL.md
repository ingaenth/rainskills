---
name: video-local
description: Produz vídeo de anúncio para negócio local presencial — spa, clínica de estética, salão, barbearia, restaurante, academia, studio, hotel, consultório. De 15 a 30s, priorizando 9:16. O produto é invisível e sensorial, a prova é social (avaliações, anos, número de clientes) e a conversão é agendamento. Use quando pedirem vídeo para um negócio com endereço físico e horário de funcionamento, peça para tráfego local, Reels de serviço, ou anúncio de spa, estética, beleza, bem-estar, saúde e hospitalidade.
---

# Vídeo de negócio local

Divide o motor técnico com `video-produto` e `filme-de-la` — mesmo kie.ai, mesmo Grok,
mesmo ffmpeg, mesmas etapas de custo. `reference/planos.md` e `reference/etapas.md`
são **o mesmo arquivo** das outras skills, via link para `_comum/`.

O que muda é tudo o que decide se a peça funciona.

## As três diferenças que mandam

**1. O produto é invisível.** Não existe screenshot de uma massagem. Numa peça de
SaaS a tela real é a prova; aqui não há tela. Você vende **uma sensação**, e o
espectador precisa senti-la em três segundos: calor, peso, silêncio, mãos, água,
tecido. Se a peça descreve o serviço em vez de fazer sentir, ela falhou.

**2. A prova é social, não técnica.** Ninguém pede benchmark de um spa. Pede
reputação — e ela é pública e verificável: **a nota do Google com o número de
avaliações**, anos de operação, quantidade de clientes atendidos, o nome do lugar
onde fica. É o ativo de conversão mais forte do gênero e quase sempre já existe.

**3. A conversão é agendar, não assinar.** O fecho não leva a uma URL de cadastro:
leva a **um horário**. Nome, bairro ou marco geográfico, como se agenda, e o horário
de funcionamento. Geografia converte: quem vê o anúncio precisa saber, sem pensar,
se aquilo fica perto.

## Antes de qualquer coisa: fixe o mercado

**Pergunta zero, e ela muda a peça inteira:** em que país e em que idioma o anúncio
vai rodar?

Isso não é detalhe de produção. Define **a locução** (voz e enum de sotaque), **as
regras do que pode ser prometido** (jurisdição), e **o que serve de prova** (Google
Reviews nos EUA, Google e Instagram no Brasil).

Foi o erro que quase entrou numa peça real: o cliente tinha nome francês, o
interlocutor era brasileiro, e o spa ficava na Flórida. Pesquisei a regra errada
(CONAR/ANVISA) antes de abrir o site. **Abra o site do cliente antes de pesquisar
qualquer regra.**

Ver `reference/prova.md` para as duas jurisdições.

## Direção visual

Uma direção por peça, como nas outras skills. As quatro que servem aqui:

| Direção | Quando serve | O que pedir |
|---|---|---|
| **Macro tátil** | massagem, estética, spa, barbearia | mãos em close, óleo escorrendo, vapor, linho, pedra, água; foco raso extremo, movimento mínimo |
| **O espaço real** | hotel, restaurante, studio, academia | a sala como ela é, luz da janela, profundidade, ninguém posando |
| **Rosto em repouso** | bem-estar, terapia, sono, relaxamento | olhos fechados, respiração visível, luz lateral suave, sem sorriso de catálogo |
| **Ritual** | preparo, gastronomia, cuidado | as mãos preparando — dobrar a toalha, acender, servir, misturar; o gesto inteiro sem corte |

**Os clichês do gênero, que envelhecem a peça na hora:** pétalas boiando na água,
pedras empilhadas, toalha enrolada com orquídea, pepino no olho, modelo de sorriso
largo em roupão branco, flauta de bambu na trilha. Coloque todos em `--evitar`.

## Ritmo — mais lento do que você acha

O erro mais comum é montar isso com ritmo de anúncio de tecnologia. **Corte rápido
destrói exatamente a sensação que a peça vende.**

- Plano de 6 a 9 segundos, não de 3.
- Numa peça de 20s cabem **três planos**, não sete.
- Transição por corte seco ou por dissolve lento. Nunca por movimento de câmera
  agressivo, nunca por whip pan.
- O gancho é sensorial e vem no primeiro segundo: água caindo, mão tocando pele,
  vapor subindo. Não é uma pergunta na tela.

## Som — aqui a ambiência É o produto

Numa peça de tecnologia o som acompanha. Numa peça de spa o som **demonstra**. É a
única forma de o espectador sentir o lugar.

**Grave a ambiência antes de pensar na trilha.** `scripts/ambiencia.sh` sintetiza o
vocabulário do gênero: água corrente, gota em bacia, vapor, tecido, tigela tibetana,
respiração, passos em madeira, fogo baixo.

```bash
scripts/ambiencia.sh agua 8      # cama de água, 8 segundos
scripts/ambiencia.sh tigela 6    # ressonância única, longa cauda
scripts/ambiencia.sh tecido 3
scripts/ambiencia.sh vapor 8
scripts/ambiencia.sh respiracao 10
scripts/ambiencia.sh listar
```

**Música:** peça a Suno cama orgânica e acústica, não eletrônica.

> "sparse acoustic ambient, felt piano, warm room tone, slow sustained strings, no
> percussion, no build, no drop, no vocals, intimate and unhurried"

Evite as palavras que devolvem o clichê: *"spa music"*, *"zen"*, *"meditation"*,
*"pan flute"*, *"healing"*. Elas produzem exatamente a trilha de elevador que o
gênero já cansou.

**Mixagem** — a proporção é outra:

| | com locução | sem locução |
|---|---|---|
| ambiência | ×0.9 | ×1.0 — é a peça |
| música | ×0.25, ducking ratio 5 | ×0.5 |
| voz | ×1.6 | — |

Uma peça de spa **pode não ter locução nenhuma**, e frequentemente é melhor assim:
ambiência, uma cartela de texto e o fecho. Proponha essa versão junto com a narrada.

Fechar em **−14 LUFS / −1,5 dBTP**.

## Locução, quando houver

Mesmo motor da outra skill: **Gemini TTS** (`google/gemini-3-1-flash-tts`), 0,66
crédito por bloco.

- **Em português:** `accent: "Neutral"` e deixe o idioma vir do texto. O enum de
  sotaque só tem variantes do inglês.
- **Em inglês: o enum continua não servindo.** Testado — `accent: "American"` devolve
  **422 "The accent parameter is invalid"**. Use `"Neutral"` sempre, em qualquer
  idioma, e deixe o idioma vir do texto. O sotaque você escolhe pela **voz**, não
  pelo parâmetro.
- `style` para este gênero: `Empathetic` ou `Whisper`. **Nunca `Promo/Hype`** — ele
  destrói a calma que a peça inteira construiu.
- `pace`: `Natural`, ou `The Drift` para peça sem pressa.
- Gere o mesmo bloco em duas ou três vozes e **deixe quem pediu escolher**. Timbre
  você não julga, e diga isso.
- **A API devolve erro no corpo com HTTP 200.** `try/except HTTPError` não pega nada:
  cheque `r["code"] == 200 and r["data"]`, senão o `["data"]["taskId"]` estoura com
  `NoneType` e você perde o lote inteiro.

## Texto — o que converte num negócio local

Três blocos, nesta ordem, e nada mais:

1. **A sensação** — o que a pessoa vai sentir, em cinco palavras.
2. **A prova** — a nota real com o número de avaliações, ou os anos, ou o número de
   clientes. Um só. Verificado, nunca arredondado para cima.
3. **O agendamento** — nome, onde fica, como agenda.

O que **não** entra: lista de serviços. Um spa com seis categorias tenta caber as
seis e não comunica nenhuma. Escolha **uma** e diga que as outras viram outras peças
— a segmentação por serviço, aliás, converte melhor no tráfego pago.

### Condição de benefício: diga pelo lado bom, não pela negativa

Quando um benefício tem limite, **não esconda e não negue** — reformule para o lado
verdadeiro que soa generoso.

| Impreciso | Negativo | Certo |
|---|---|---|
| "Acesso ao resort" | "Só nos dias de atendimento" | **"Fique o dia — a cada visita"** |
| "Aulas ilimitadas" | "Máximo 3 por semana" | "Três aulas por semana, toda semana" |
| "Estacionamento grátis" | "Só 2 horas" | "As duas primeiras horas por nossa conta" |

A frequência é quase sempre a formulação boa: *a cada visita*, *toda semana*, *todo
mês*. Ela informa o limite sem usar "só", "apenas" ou "máximo" — e converte melhor
que a promessa vaga, porque a pessoa consegue imaginar quando vai usar.

**Nunca resolva isso com asterisco.** Ressalva em corpo pequeno é confissão de que a
promessa grande está errada; e num vídeo vertical ninguém lê.

Preço só entra se for âncora clara e verdadeira. "A partir de" sem o "a partir de"
disponível na agenda é propaganda enganosa nas duas jurisdições.

## Regras de conteúdo — o gênero mais regulado dos três

**Leia `reference/prova.md` inteiro antes de escrever a primeira linha.** Resumo do
que nunca passa, em nenhum país:

- **Antes e depois é território minado.** Nos EUA, o FTC trata a imagem como
  endosso que promete resultado típico, e "results not typical" em corpo pequeno
  **não** resolve. No Brasil, o Código de Ética Médica proíbe para médico mesmo com
  autorização do paciente. Regra prática: **não use.**
- **Pessoa real exige autorização por escrito.** Já houve condenação de R$ 25 mil
  por clínica que usou foto de paciente em anúncio pago sem termo assinado.
- **Pessoa gerada por IA nunca é apresentada como cliente.** Ilustrar o serviço com
  figura gerada é publicidade normal. Pôr uma frase de depoimento na boca dela é
  fabricação — e some com a credibilidade da peça no dia em que alguém perceber.
- **Alegação de resultado corporal exige comprovação** e, dependendo do que promete,
  vira alegação medicamentosa: emagrecimento, celulite, estria e flacidez são
  proibidos para cosmético pela ANVISA, e nos EUA exigem substanciação prévia.
- **Nota do Google é prova; "o melhor da cidade" não é.** Superlativo sem base
  documental é o caminho curto para notificação.

Quando o cliente insistir numa promessa que você não sustenta, **entregue a peça sem
ela** e diga por quê.

## Material — quase tudo dá para levantar sozinho

Ver `reference/materiais.md`. A ordem que rende:

1. **O site do cliente** — fotos reais dos ambientes, nomes exatos dos serviços,
   horário, forma de agendar, as frases que eles já usam.
2. **Google Meu Negócio** — a nota, o número de avaliações, e as **fotos de
   clientes**, que mostram o lugar como ele realmente é.
3. **Instagram** — o que já performou. Ver `reference/materiais.md` para a checagem
   de engajamento: número de seguidores não é prova de nada, curtidas por post são.
4. **Só então pergunte** — e peça poucas coisas, específicas.

O **GPT Image 2** monta o quadro com as fotos reais como referência; o **Grok** só
anima. Mesma divisão da outra skill, e vale igual: o Grok não acrescenta nada, só
move o que já está lá.

## Formatos — 9:16 primeiro

Invertido em relação à skill de produto. Tráfego local vive em Reels e Stories.

- **9:16** é o master. Gere nativo, `--ar 9:16`. Não recorte do 16:9.
- **1:1** para feed.
- **16:9** só se houver site ou tela em recepção que peça.
- Margem inferior de 15% livre de texto: a interface do app come essa faixa.

## Produção por etapas

Idêntica às outras — `reference/etapas.md`. Para negócio local, agrupe assim:

| Parada | Entrega |
|---|---|
| 1 | **roteiro + o que pode ser dito**, com a prova verificada e a jurisdição fixada |
| 3 | o primeiro quadro, para validar se o lugar parece aquele lugar |
| 4 | todos os quadros |
| 6 | corte completo, nas duas versões: com locução e só com ambiência |

A parada 1 aqui **nunca se agrupa**: é onde mora o risco jurídico.

## Custos

| item | créditos |
|---|---|
| imagem | 4 a 6 |
| Grok base 6s | 27 |
| voz por bloco | 0,66 |
| Suno | ~10 |
| **peça de 20s, 9:16 + 1:1** | **~130** |

Peça de negócio local é mais barata que a de produto: menos planos, mais longos.
