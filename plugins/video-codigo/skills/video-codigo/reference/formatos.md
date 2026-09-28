# Formatos, capas e entrega

## Tamanhos

| Formato | `window.SIZE` | Uso | Duração |
|---|---|---|---|
| 16:9 | `[1920,1080]` | site, YouTube, LinkedIn, apresentação | 45–60 s |
| 9:16 | padrão (1080×1920) | Reels, Stories, TikTok, Shorts | 18–28 s |
| 1:1 | `[1080,1080]` | feed, anúncio | 15–30 s |

30 fps é o padrão (reels); 60 fps deixa panorâmicas longas mais suaves no 16:9.

## Zonas seguras do Instagram (9:16, 1080×1920)

A interface cobre partes do vídeo. Nada importante em:

- topo, **0–220 px** (cabeçalho "Reels", câmera);
- base, **1500–1920 px** (nome, legenda, música);
- coluna direita, **x > 940 entre y 1000 e 1500** (curtir, comentar, compartilhar).

Legendas entre y ≈ 250 e 1450, largura útil de 80 a 960. O preview tem a caixa "zonas IG"
para ver essas áreas em vermelho.

## Capas de reel

O Instagram recorta a mesma capa de formas diferentes: **3:4 no grid do perfil, 4:5 no
feed e quadrado em algumas telas**. Coloque **todo o conteúdo no quadrado central
1080×1080 (y 420–1500)**. Assim nenhum recorte corta nada. Capas cortadas foram motivo de
retrabalho.

- Faça as capas como uma página HTML só (`capas.html?n=1…5`) e fotografe com
  `node foto.mjs capas.html?n=1 out/capa-1.png 1080x1920`.
- Mesmo sistema visual nas 5 (o grid vira uma vitrine), com título grande, um elemento real
  (print ou número) e o logo.
- Faça uma folha com os retângulos de recorte (1:1 e 4:5) desenhados para conferir.
- `capa-no-video.sh reel.mp4 capa.png saida.mp4` embute a capa como 1º quadro (o
  Instagram já sugere) e como miniatura do arquivo. Diga ao usuário que também pode subir a
  capa por "Editar capa → Adicionar da galeria".

Thumbnail do YouTube: 1280×720, título curto grande, logo e um elemento; confira se
imagens com fundo preto usam `mix-blend-mode:screen` (senão aparece um quadrado preto).

## Qualidade de entrega

- H.264 High, **16 Mb/s** (o `render.mjs` já faz). Arquivo pequeno (≈2,5 Mb/s) vira blocos
  e faixas quando o Instagram recomprime fundo escuro com degradê.
- Áudio AAC 192k, 48 kHz, **−14 LUFS**, pico −1,5 dB.
- Ao postar: ativar "Upload em alta qualidade" (Configurações → Uso de dados e qualidade
  da mídia).

## Pasta de entrega

```
entrega/
  00-filme-lancamento-16x9.mp4
  01-<nome-curto>.mp4 … 05-<nome-curto>.mp4      (com capa embutida)
  capas/01-…-capa.png …  00-filme-thumbnail-youtube.png
  POSTAGEM.md
```

## `POSTAGEM.md` (modelo)

1. **Calendário**: o grid mostra o mais novo primeiro, então no dia 1 publique 3 reels em
   sequência (o manifesto por último, para ficar em 1º no grid). Depois um reel a cada 2 dias.
   Fixe o manifesto e o de conversão. Público B2B: dias úteis, 11h30–13h ou 18h–19h.
   O filme 16:9 vai nativo no LinkedIn e no YouTube no dia 1.
2. **Bio sugerida** (4–5 linhas, CTA no fim).
3. **Legenda de cada peça**: gancho na 1ª linha, 2–4 linhas de valor, CTA ("link na
   bio"), uma pergunta para comentário e 8–10 hashtags do nicho. Sem inventar dado.
4. **Depois de publicar**: responder comentários na primeira hora, repost nos stories com
   enquete, comparar salvamentos/compartilhamentos em 7 dias e transformar o melhor formato em série.
