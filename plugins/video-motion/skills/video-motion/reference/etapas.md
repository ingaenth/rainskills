# Produção por etapas — a imagem aprova antes do vídeo

O custo aqui tem dois degraus: **18** por keyframe e **84** por plano. Tudo o mais é
zero. Por isso a peça inteira é aprovada **parada, como imagens**, antes do primeiro
clipe — e o cliente responde às perguntas do briefing antes da primeira imagem.

## As paradas

### 1. Perguntas respondidas + roteiro de planos + kit — custo zero
As doze perguntas de `briefing.md` respondidas e registradas. O roteiro de planos:
para cada K, o que a imagem mostra e onde fica a área vazia do título; para cada S,
o que se move entre K_n e K_n+1; para cada plano, o texto (e se ele vai na imagem ou
em pós, conforme a resposta 7). O kit com a paleta-imagem e os posts como estilo.
Diga o custo total antes de seguir.

### 2. K1 — 18 cr
A primeira imagem valida estilo, luz, fidelidade do produto e se "parece o post".
Se não parecer, é a referência de estilo que muda, não o adjetivo do prompt.

### 3. Todos os keyframes + roteiro — ~108 cr — PARADA OBRIGATÓRIA
Não existe atalho aqui: nenhum plano é gerado sem o cliente ter visto os frames e o
roteiro e ter dito "pode gerar". É a regra que mais economiza crédito.
Folha de contato com os seis. **É a parada mais valiosa:** o cliente vê o filme
inteiro parado, quadro a quadro, e aponta o que muda. Confira você mesmo: continuidade
de cena entre K_n e K_n+1, cores da paleta e — com Omni — **cada palavra, acento e a
logo inteira** em cada quadro (com Veo/Grok: área do título livre, nada de texto nem
logo gerados).

### 4. Primeiro plano animado — 84 cr
S1 valida que o Omni respeita os dois frames, a velocidade do movimento e a ausência
de artefatos. Folha de contato do clipe inteiro.

### 5. Corte completo — ~340 cr
Todos os planos, texto, logo animada, efeitos no beat, trilha, master e artifact.

## Como agrupar

- **Cliente conhecido, posts em mãos** → 1, 3, 5 (K1 dentro da 3).
- **Cliente novo ou identidade em dúvida** → todas, e a 2 com duas direções.
- **Reprovação do tipo "ficou ruim"** → pergunte o que; volte à parada 1 com posts
  novos como referência. Não regere planos antes de regerar keyframes.

## O que nunca fazer

- Animar antes dos keyframes aprovados: mudar um K depois custa 18 + 84.
- Com Veo ou Grok, gerar texto ou logo no modelo; com Omni, deixar o keyframe sem eles.
- Trocar de motor por conta própria.
- Cortar as pontas dos clipes encadeados: quebra a emenda entre keyframes.
- Seguir sem resposta. Silêncio não é aprovação.
