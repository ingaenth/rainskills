---
name: video-codigo
description: Produz vídeo feito inteiramente em código — HTML/CSS/JavaScript animado por uma timeline determinística, fotografado quadro a quadro pelo Playwright e montado no ffmpeg, com trilha e efeitos sintetizados em Web Audio. Totalmente personalizado — antes de produzir, descobre a marca e entrevista o usuário em rodadas curtas (objetivo, onde vai rodar, referências, personalidade, material, fatos, aprovação) e monta um BRIEFING.md que é o prompt mestre da peça. Custo zero de crédito, texto, preços e números exatos, telas reais do produto ou fotos aprovadas da empresa, identidade da marca pixel a pixel. Serve para qualquer empresa — SaaS, e-commerce, spa, clínica, restaurante, hotel, imobiliária, varejo — e qualquer conteúdo: explicativo, filme de lançamento 16:9, kit de reels 9:16, carta de serviços com preços, vídeo de TV de recepção, anúncio, tutorial, animação de logo, além de capas, thumbnails e plano de postagem. Use quando pedirem vídeo "feito com JavaScript", "em código", "sem IA", vídeo a partir das telas do produto ou das fotos da empresa, menu/carta/tabela de preços animada, ou quando o conteúdo depende de texto, números ou interface que um gerador de vídeo erraria.
---

# Vídeo em código

Cada quadro é HTML renderizado. Uma função `seek(t)` desenha o instante `t`; o
`render.mjs` chama `seek(0)`, `seek(1/30)`, … fotografa cada um e manda para o ffmpeg. O
áudio é sintetizado no próprio navegador (OfflineAudioContext) com os **mesmos tempos** da
imagem, então cada clique, ping e acorde cai no quadro certo.

**Por que escolher esta skill:** zero crédito; texto, preço e número saem exatamente como
escritos; as telas do produto e as fotos da empresa são as reais; a marca entra por tokens
(cor, fonte, logo oficial); qualquer ajuste é uma edição e um novo render de 1 a 3 minutos;
dá para produzir várias peças em paralelo. Funciona com **qualquer material**: telas do
sistema (modo interface), fotos aprovadas da empresa (modo editorial, com câmera lenta,
molduras e tipografia de cartaz), ou nenhuma mídia (modo tipográfico/dados).
**Quando não usar:** quando a peça precisa de movimento filmado que não existe (pessoas se
mexendo, câmera andando pelo ambiente, produto girando em 3D). Aí é `video-local`,
`video-produto` ou `video-motion`, que geram vídeo com IA. Fotos paradas não são motivo
para trocar de skill.

**Nada aqui tem estética padrão.** Cor, fonte, ritmo, tom, quantidade de texto, formato e
modo visual saem da descoberta e da entrevista de cada cliente, registradas no
`BRIEFING.md`. Duas marcas nunca recebem o mesmo vídeo com cores trocadas.

## Regras que não se negociam

0. **Entreviste antes de produzir.** Descubra o que der (site, repositório, manual, redes,
   mídia) e pergunte o resto em rodadas curtas, sempre com uma proposta concreta tirada da
   descoberta. As respostas viram o `BRIEFING.md` (o prompt mestre), que o usuário aprova
   antes do primeiro render longo. Método em [reference/entrevista.md](reference/entrevista.md),
   modelo em [reference/briefing-prompt.md](reference/briefing-prompt.md).
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
5. **Revisar parado antes de renderizar — duas vezes.** Stills nos momentos-chave e folha
   de contato; primeiro a revisão técnica (corte, zona segura, dado pessoal), depois a
   **revisão de diretor de arte**: escala de cartaz, ritmo de cor, um herói por cena
   ([reference/direcao-de-arte.md](reference/direcao-de-arte.md)). Vídeo correto e sem graça
   é reprovado igual. Na entrega, diga o que foi revisto e o que não foi.
6. **Entrega só depois de conferir o arquivo.** `ls` e `ffprobe` de cada master (duração,
   tamanho, faixa de áudio) antes de dizer "entregue". README, relatório ou mensagem nunca
   listam arquivo que não existe. A entrega vai para a pasta combinada no briefing, nunca
   como commit no repositório do site do cliente.

## Fluxo

```
descoberta ─► entrevista ─► BRIEFING.md ─► conceito ─► motor da marca ─► peça-piloto ─► demais peças ─► revisão ─► entrega
(site, repo,   (rodadas com   (prompt mestre,  (metáfora    (tokens, logo,    (valida o      (em paralelo,   (técnica +   (ffprobe,
 manual, mídia) propostas)     aprovado)        própria)     helpers)          padrão)        subagentes)     diretor de   MP4, capas)
                                                                                                             arte)
```

Passo a passo com comandos em [reference/etapas.md](reference/etapas.md).

## O motor (`scripts/`)

| Arquivo | O que é |
|---|---|
| `lib.js` | timeline determinística, cenas, câmera virtual sobre prints e vídeos, **foto com ponto focal e câmera lenta, linha com máscara, cortina de cena, linha de preço com pontilhado**, legenda cinética, telestrador, transição, moldura, ícones de canal, cartão final, kit de áudio, preview com play |
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
- [reference/entrevista.md](reference/entrevista.md): as rodadas de perguntas, com o porquê de cada uma e como cada resposta vira decisão técnica.
- [reference/briefing-prompt.md](reference/briefing-prompt.md): o modelo do `BRIEFING.md`, o prompt mestre da peça.
- [reference/direcao-de-arte.md](reference/direcao-de-arte.md): escala de cartaz, ritmo de cor, um herói por cena, camadas, modos visuais (interface, editorial/foto, tipográfico, misto) e o checklist do diretor de arte.
- [reference/descoberta.md](reference/descoberta.md): como tirar marca, fatos e mídia de um site, repositório ou manual, e como checar privacidade.
- [reference/conceito.md](reference/conceito.md): como achar o conceito certo, o kit de lançamento (filme + 5 reels) e exemplos já produzidos.
- [reference/motor.md](reference/motor.md): API do `lib.js`, padrões de cena, câmera, texto, áudio.
- [reference/formatos.md](reference/formatos.md): 16:9, 9:16, 1:1, zonas seguras do Instagram, capas, thumbnail, bitrate e plano de postagem.
- [reference/subagentes.md](reference/subagentes.md): como dividir várias peças entre agentes em paralelo sem perder a unidade.
- [reference/armadilhas.md](reference/armadilhas.md): o que já deu errado e como evitar.
