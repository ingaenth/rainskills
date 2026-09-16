---
name: video-tv-espera
description: Produz o vídeo institucional em loop para a TV do lobby, recepção ou sala de espera de um negócio local — spa, clínica, consultório, salão, academia, hotel, restaurante. 16:9, 1:10 a 1:45, sem locução, com trilha + ambiência, cartela em todo plano e fecho com endereço/telefone. Quadros de fotos reais elevados por IA e animados (kie.ai), texto e logo sempre em pós. Use quando pedirem vídeo para TV do estabelecimento, loop de recepção, vídeo de pendrive para TV, "vídeo institucional para passar na loja", ou a versão TV de um Reel que já existe.
---

# Vídeo de TV de espera

Divide o motor com `video-local` — mesmo kie.ai, mesmo ffmpeg. O que muda: o público
é **cativo** (está sentado esperando, vai assistir ao loop 2–3 vezes), o formato é
**16:9 mudo com música**, e a conversão é *"book at the front desk"* — a recepção
está a três metros da TV.

## O formato

- **1:10 a 1:45 em loop.** 8 a 11 planos de ~9s + fecho estático de 5–6s. O loop
  não pode ter fade final: o fecho corta de volta para a abertura.
- **Plano = clipe de 6s (Grok/i2v) desacelerado a 0,65×** (~9,2s). Movimento quase
  estático: micro-push, drift, chama de vela. Dissolves de 0,7–0,8s.
- **Arco fixo:** chegada (logo) → prova social (nota Google) → ambientes → serviços
  (um plano por serviço, cartela sobre imagem DO assunto) → respiro → fecho com
  logo escura, endereço, telefone, horário e "Book your next visit at the front desk".
- **Nenhum plano fica sem texto.** Plano de ambiente ganha cartela de ambiente
  ("Designed for Calm", "Your Treatment Awaits"). Regra dada por cliente real e ela
  melhora qualquer peça: texto é o que a pessoa lê enquanto espera.
- **Multi-unidade:** o desenho aprovado uma vez vira o padrão; cada unidade nova
  troca só fotos, endereço e trilha (dê uma música diferente por unidade). Espelhe
  o MESMO shot list no Reel 9:16 — uma pauta, duas peças.

## Pessoas em cena — a lição mais cara

**GPT Image deforma gente em cena de tratamento.** Caso real, aprovado e depois
rejeitado pelo cliente: massagem com **duas mãos direitas**, terapeutas com cara de
manequim. Não é fixável por prompt; é o modelo.

A cadeia que funciona:

1. **Gente = nano-banana-2** (Gemini), sempre com **as fotos reais do lugar como
   `image_input`** — ele preserva sala, uniforme e até tatuagem da cliente. No
   prompt, peça literalmente: *"anatomically perfect hands, one left and one right
   hand, five fingers each; natural serene faces"*.
2. **GPT Image 2.5 (Flare/Sunburst, set/2026) corrigiu a anatomia** — testado:
   mãos e rostos perfeitos a 6 cr. **Mas no mesmo teste ele redesenhou a sala**
   (spa genérico bonito no lugar da sala real das referências). A escolha vira:
   fidelidade ao lugar = **nano-banana-2** (12 cr, preserva sala/uniforme/tatuagem);
   cena que pode ser "um spa bonito" = **gpt-image-2-5-flare** (6 cr). O gpt-image-2
   antigo segue proibido para gente.
3. **Animar com trava:** no prompt do i2v, *"hands keep exactly five fingers each
   and never deform; faces stay natural"* + movimento mínimo.
4. **QC obrigatório em todo clipe com gente:** extraia frame do início, meio e fim
   e olhe as mãos. É onde o Grok escorrega, e o cliente vê na TV grande.

**E nunca resolva gente com foto parada.** Ken Burns numa peça em que tudo se move
lê como erro — cliente real devolveu na hora ("imagem parada sem nada"). Se a foto é
boa, gere a versão nano-banana dela e anime.

## Material do cliente vale mais que geração

Vídeo de WhatsApp 480p da equipe fazendo um facial vale mais que qualquer plano
gerado — é prova. O tratamento que o deixa apresentável em Full HD:

- `hqdn3d=3:2:6:4,unsharp=5:5:0.4` (tira o ruído de compressão, devolve borda).
- **Slow motion de verdade é 0,2–0,3× com `minterpolate` (mci/aobmc).** 0,5× não
  parece slow motion, parece vídeo lento — cliente reclama duas vezes até você
  chegar a 0,22×. Interpolar é obrigatório abaixo de 0,5× ou engasga.
- **Vertical em peça horizontal = díptico ou tríptico**, painéis lado a lado com
  filete e rótulos na identidade (BEFORE / AFTER rende muito para estética — cheque
  a jurisdição em `video-local reference/prova.md` antes). Painel de foto no meio
  ganha zoom+pan visível; os de vídeo, o slow motion.

## Som — três camadas

Peça de TV é "muda" mas nunca silenciosa:

| camada | volume | o quê |
|---|---|---|
| música | ×0.5 | a trilha (Suno, cama orgânica — ver video-local) |
| ambiência | ×1.0 | room tone de spa/loja contínuo, em loop pela peça inteira |
| SFX pontual | ×0.3 | UM efeito no plano certo (vapor no plano da massagem), fade in/out |

`amix normalize=0` e **loudnorm −14 LUFS / −1,5 dBTP** no fim. A ambiência por baixo
de tudo é o que faz a TV "estar" no lugar; só música soa institucional velho.

## Identidade sempre em pós

Logo e texto **nunca** saem do gerador: PIL/Pillow por cima, com a logo real e as
fontes da marca. Se as fontes são de outro sistema (Didot/Futura do macOS num
servidor Linux), os equivalentes livres do Google Fonts passam em teste A/B com o
cliente: **GFS Didot ≈ Didot, Jost ≈ Futura, Playfair Display Italic ≈ Didot
itálico.** Cartela: título serifado grande + subtítulo sans dourado espaçado
(`" ".join(texto)`), véu preto suave borrado atrás (rounded rect + GaussianBlur),
sempre no mesmo canto e na mesma altura em todos os planos.

## Portões de aprovação — o dinheiro para nos quadros

Imagem custa 6–12 créditos; animação custa 27. O fluxo que não queima crédito:

1. Quadros + mock das cartelas → **gere o "Roteiro do vídeo"** com
   `scripts/roteiro.py` e publique numa URL que o cliente abre do celular. Não é uma
   grade de imagens: é o plano completo, plano a plano — **de que segundo a que
   segundo**, o que acontece em cada imagem (movimento), a transição para o próximo,
   a cartela e o áudio. O cliente aprova o FILME, não as fotos.
2. Só anima o que foi aprovado. **Nunca anime sem OK explícito** — é a regra número
   um, escrita depois de refazer uma peça inteira.
3. Montagem é ffmpeg local: trocar texto, ordem, trilha ou ritmo custa zero. Diga
   isso ao cliente — ele pede mais ajustes quando sabe que ajuste é grátis.

## Custos (kie.ai, peça de ~10 planos)

| item | créditos |
|---|---|
| quadro (nano-banana-2, padrão) | 12 |
| animação Grok 6s 720p | 27 |
| upscale Topaz 2× (opcional — 720p já serve para TV) | 48 |
| **peça completa, sem Topaz** | **~300–450** |

Iterações de gente (regenerar quadro + reanimar) são o estouro típico: orce +30%.

Receita de montagem, QC e organização de entrega: `reference/producao.md`.
