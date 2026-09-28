---
name: video-codigo
description: Produz vídeo feito inteiramente em código — HTML/CSS/JavaScript animado por uma timeline determinística, fotografado quadro a quadro pelo Playwright e montado no ffmpeg, com trilha e efeitos sintetizados em Web Audio. Custo zero de crédito, texto e números exatos, telas e gravações reais do produto, identidade da marca pixel a pixel. Serve para qualquer empresa e qualquer conteúdo — explicativo de 60s, filme de lançamento 16:9, kit de reels 9:16 para Instagram, vídeo de produto, tutorial, anúncio, animação de logo — e também para capas, thumbnails e plano de postagem. Use quando pedirem vídeo "feito com JavaScript", "em código", "sem IA", vídeo explicativo de um site ou sistema, lançamento de plataforma, reels de lançamento, vídeo a partir das telas do produto, ou quando o conteúdo depende de texto, números ou interface que um gerador de vídeo erraria.
---

# Vídeo em código

Cada quadro é HTML renderizado. Uma função `seek(t)` desenha o instante `t`; o
`render.mjs` chama `seek(0)`, `seek(1/30)`, … fotografa cada um e manda para o ffmpeg. O
áudio é sintetizado no próprio navegador (OfflineAudioContext) com os **mesmos tempos** da
imagem, então cada clique, ping e acorde cai no quadro certo.

**Por que escolher esta skill:** zero crédito; texto, preço e número saem exatamente como
escritos; as telas do produto são as reais; a marca entra por tokens (cor, fonte, logo
oficial); qualquer ajuste é uma edição e um novo render de 1 a 3 minutos; dá para produzir
várias peças em paralelo. **Quando não usar:** quando o pedido é cena filmada, pessoas,
ambiente fotográfico, produto físico em 3D realista. Aí é `video-produto`, `video-local` ou
`video-motion`, que geram imagem e vídeo com IA.

## Regras que não se negociam

1. **Um conceito próprio por cliente.** Nunca reaproveite a estrutura do vídeo anterior
   trocando só as cores. O cliente percebe na hora e reprova ("fez um vídeo exatamente
   igual"). O motor é compartilhado; a ideia, a estrutura, as transições, a tipografia e o
   desenho de som nascem do mundo daquele produto. Método em
   [reference/conceito.md](reference/conceito.md).
2. **Só fatos da fonte.** Cada afirmação, número, preço e recurso sai do site, do código
   ou do material do cliente. Números inventados para contar a história (placar, horário de
   uma cena, valores de exemplo) são marcados como ilustrativos na tela ("Exemplo:") ou
   declarados ao cliente na entrega. Não invente recurso nem promessa de resultado.
3. **Privacidade antes de tudo.** Prints e gravações reais do produto podem ter nome,
   telefone, CPF, e-mail e conversa de cliente. **Olhe cada quadro que entra no vídeo em
   tamanho cheio** antes de usar, e avise o cliente se o material público dele expõe dados.
   Detalhes em [reference/descoberta.md](reference/descoberta.md).
4. **O manual de marca manda.** Se existe manual ou guia, ele vence o gosto: logo só pelos
   arquivos oficiais, sem recolorir, sem sombra, sem degradê; cores, fontes e regras de
   movimento do manual. Se não existe manual, os tokens do site valem.
5. **Revisar parado antes de renderizar.** Stills nos momentos-chave, folha de contato,
   correção, e só então o render final. Na entrega, diga o que foi revisto e o que não foi
   (normalmente: "revisei quadros, não assisti inteiro com som").

## Fluxo

```
descoberta ─► conceito ─► motor da marca ─► peça-piloto ─► demais peças ─► revisão ─► entrega
(site, repo,   (metáfora    (tokens, logo,    (valida o      (em paralelo,   (stills,    (MP4, capas,
 manual, mídia) própria)     cartão final)     padrão)        subagentes)     folha)      plano)
```

Passo a passo com comandos em [reference/etapas.md](reference/etapas.md).

## O motor (`scripts/`)

| Arquivo | O que é |
|---|---|
| `lib.js` | timeline determinística, cenas, câmera virtual sobre prints e vídeos, legenda cinética, telestrador, transição, moldura, ícones de canal, cartão final, kit de áudio, preview com play |
| `lib.css` | base visual; **a marca entra redefinindo as variáveis** (`--bg`, `--accent`, `--font-display`…) |
| `render.mjs` | HTML → MP4 (quadros + áudio + loudnorm). `STILLS=1,5 node render.mjs peca.html` para revisão |
| `folha.py` | folha de contato dos stills |
| `foto.mjs` | página estática → PNG (capas, thumbnail) |
| `capa-no-video.sh` | embute a capa como 1º quadro e como miniatura do MP4 |
| `exemplo.html` | peça-modelo de 12 s que roda sem nenhum asset: copie e comece por ela |

API completa, padrões de animação e de áudio em [reference/motor.md](reference/motor.md).

**Pré-requisitos:** node 18+, ffmpeg, Python com Pillow e, na pasta do projeto,
`npm i playwright && npx playwright install chromium`.

## Referências

- [reference/etapas.md](reference/etapas.md): o passo a passo, do link do site à pasta de entrega.
- [reference/descoberta.md](reference/descoberta.md): como tirar marca, fatos e mídia de um site, repositório ou manual, e como checar privacidade.
- [reference/conceito.md](reference/conceito.md): como achar o conceito certo, o kit de lançamento (filme + 5 reels) e exemplos já produzidos.
- [reference/motor.md](reference/motor.md): API do `lib.js`, padrões de cena, câmera, texto, áudio.
- [reference/formatos.md](reference/formatos.md): 16:9, 9:16, 1:1, zonas seguras do Instagram, capas, thumbnail, bitrate e plano de postagem.
- [reference/subagentes.md](reference/subagentes.md): como dividir várias peças entre agentes em paralelo sem perder a unidade.
- [reference/armadilhas.md](reference/armadilhas.md): o que já deu errado e como evitar.
