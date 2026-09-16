# Briefing — as perguntas que decidem a peça

Pergunte tudo de uma vez, em linguagem de cliente. Cada pergunta existe porque a
resposta errada, assumida, custou uma rodada inteira em produção.

## Bloco 1 — referências e identidade

1. **"Me manda 2 ou 3 posts ou vídeos que representem a marca."** É a pergunta que
   resolve o briefing: o post vira `--estilo` no kit e o modelo copia a linguagem
   (fundo, luz, ícones, profundidade). Sem post, sai fintech genérico.
2. **"Se o site e os posts diferem, qual vale?"** Projetos no disco têm tokens
   (`theme.css`, `tokens.ts`); o time de marca costuma ter outra paleta e outra fonte
   nos posts. Assumir a do código produziu uma peça "de outra marca".
3. **Paleta em hex** e **nomes das cores** (viram a imagem de amostras).
4. **Fonte**: o arquivo. Sem ele, qual substituta aceita.
5. **Logo**: PNG transparente ≥ 1024px.

## Bloco 2 — como produzir

6. **"Prefere que eu desenhe cada quadro antes e anime entre eles, ou que o modelo
   invente a cena a partir do texto?"** O primeiro é o método da skill (keyframes
   encadeados, first → last frame): mais controle, cena contínua, o cliente aprova as
   imagens antes de animar.
7. **Texto e logo — informe, não pergunte:** com Omni vão **dentro da imagem** (é o
   melhor resultado da skill: parece o post, letra parada no plano); com Veo ou Grok
   vão **em pós**. Diga o custo de mudança em cada caso (18 + 84 por quadro/plano na
   imagem; zero em pós) e siga a regra, salvo pedido explícito do cliente.
8. **"A logo aparece o tempo todo ou só no fecho? Em que posição? Sobre cartão branco
   nos fundos escuros?"** Manual de marca costuma exigir sempre. A logo nunca é gerada
   pelo modelo: entra em pós, animada.
9. **"Qual motor: Omni, Veo ou Grok?"** Rode antes `scripts/kie.py motores --planos N
   --formatos F` e mostre o resultado (saldo, custo por motor, se cabe). Resumo: Omni (padrão,
   first/last por referência, 84 cr/6s, 1080p), Veo 3.1 (first/last nativo, 8s, ~65 cr,
   mais "cinema"), Grok (só primeiro frame, 27 cr/6s, sem emenda invisível). Registre
   a resposta; não troque de motor por conta própria.
10. **Formato e duração**: 16:9, 9:16, os dois? A duração sai de planos × 6s.
11. **Locução**: com ou sem. Se com, TTS Gemini em pós; a voz Omni é barrada.
12. **Energia**: calmo / médio / rápido → 90 / 110 / 125 BPM.

12b. **Gerador de imagens**: nano-banana-pro (Google) ou GPT Image 2 (ChatGPT)? Os dois
    obedecem logo, paleta e acento; o GPT Image 2 saiu a 10 créditos por quadro 2K contra 18,
    e devolve 1152×2048 em 9:16 (normalize para 1080×1920 antes de animar). O cliente que
    já usa um dos dois costuma querer o mesmo; registre no `marca.json`.

## Bloco 3 — o que dizer

13. **As três mensagens.** Mais que três é outra peça.
14. **Chamada e destino**: texto exato do CTA, site ou WhatsApp.
15. **Números**: de onde vêm? Sem origem, não entram. Um número lido dos tokens do
    site ainda precisa de "pode ir ao ar".
16. **Marca de terceiro, alegação vetada, ressalva** necessária.

## Bloco 4 — dinheiro

17. **Orçamento.** Diga antes: ~530 créditos por 30s em um formato; 9:16 dobra. E
    diga o que é grátis (texto, logo, som, montagem) para o cliente pedir ajuste sem
    medo.

## Como ler uma referência de vídeo

```bash
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 --write-info-json -o "%(id)s.%(ext)s" "<url>"
ffmpeg -i ref.mp4 -vf "fps=3,scale=400:-1,tile=5x5:padding=4:color=gray" -frames:v 1 folha_a.png
ffmpeg -ss 8.33 -i ref.mp4 -vf "fps=3,scale=400:-1,tile=5x5:padding=4:color=gray" -frames:v 1 folha_b.png
python3 scripts/batidas.py musica ref.mp4
```

Três frames por segundo, 25 por folha. Anote por bloco: fundo, texto, objeto,
transição, duração. É o roteiro de planos da referência; o seu nasce dele com as
palavras e as cores do cliente.

## Como ler um post

Abra os posts lado a lado e anote: fundo (claro com luz suave? escuro com textura?),
onde a logo fica e sobre o quê, proporção título/apoio, ícones (3D macios? flat?),
profundidade (sombra, brilho). Isso vira a `--direcao` e escolhe qual post é
referência de cada keyframe (um claro, um escuro).

## De resposta a prompt

> *"Posts claros com luz azulada e ícones 3D, título navy + coral, logo no canto"*
>
> `--direcao "Clean modern fintech motion graphics, bright white background with a soft
> pale-blue light glow, rounded soft 3D icons with subtle depth, coral and turquoise
> accents, minimal, lots of breathing room"`
> `--evitar "photorealism, stock people, near-black backgrounds, harsh gradients, lens
> flares, clutter"`

**Se o cliente não souber responder**, mostre K1 em duas direções (36 créditos) e
deixe apontar.
