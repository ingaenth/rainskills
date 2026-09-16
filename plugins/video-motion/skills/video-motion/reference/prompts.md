# Prompts testados no Omni — com o que saiu de cada um

Todos em `gemini-omni-video`, 720p ou 1080p (mesmo preço), 24 fps. Cerca de um
minuto por clipe. Os resultados são de 03/09/2026; o modelo pode mudar.

## 1. Flat 2D, produto sem texto — EXCELENTE

> Flat 2D motion graphics advertisement, After Effects style, vector illustration look.
> Solid vivid orange background, no gradients, no photorealism. A tall orange soda can
> (plain, unbranded, no text on it) pops into the center of the frame with a snappy
> overshoot bounce, then orange slices, green leaves and small droplets fly in from the
> edges and settle around the can with elastic easing. At the end a bright juice splash
> bursts behind the can. Static camera, crisp edges, bold graphic shapes, drop shadows,
> fast punchy timing typical of social media food ads. No text, no letters, no logo
> anywhere.

6s, 84 cr. Lata pop com overshoot real, gomos entrando em órbita, splash no fim.
Indistinguível de peça feita em AE. (No original havia `#FF7A00` no prompt e **não**
apareceu — mas apareceu nos testes 4 e 5; não conte com sorte.)

## 2. Tipografia cinética, 3 palavras — LETRA CERTA

> Kinetic typography motion graphics, flat 2D, After Effects style. Solid bright green
> background. The words "ESTAMOS DE CARA NOVA" appear one word per beat in huge
> condensed bold black sans-serif capitals, stacked vertically and centered: first
> ESTAMOS pops in with an overshoot, then DE CARA slides in below it in light green,
> then NOVA drops in below in black. On the last beat the background hard-cuts to dark
> green and the text colors invert. Snappy, precise, no camera movement, no other
> objects, no extra letters.

4s, 63 cr. Exatamente o pedido, inclusive a inversão de cor. Fonte saiu bold
condensada. Vale para hero words. Para timing no beat exato, ainda assim `tipo.py`.

## 3. 3D, cartões em leque sobre gradiente fluido — BOM

> Premium 3D motion graphics product shot, brand film style. A fluid, soft-focus
> gradient background of vivid green and lime, slowly swirling like liquid. A single
> plain matte green payment card (no text, no logo, no numbers, blank surface with a
> subtle sheen) floats in the center, then spins on its vertical axis and fans out into
> eight identical cards arranged in a circle like a hand of playing cards, with smooth
> elastic easing, then they collapse back into one card. Studio lighting, soft shadows,
> shallow depth of field, clean render, no text anywhere.

6s, 84 cr. Leque de oito cartões girando, volta para um. O gradiente ficou mais
"mármore" que "seda" — para o líquido lento da referência 6 (`batidas.md`), peça `slow silky liquid
gradient, large soft blobs, no marbling`.

## 4. Frase longa em português, 9:16 1080p — LETRA CERTA, MAS…

> …Solid dark background (#1C1A20). Portuguese text appears line by line in bold white
> sans-serif, centered, one line per beat with snappy slide-up and overshoot: line 1
> "Você recebe na hora." — line 2 "Sem taxa escondida." — line 3, larger and in orange
> (#F1602E): "Menos taxa. Mais controle." Then all text exits upward and the single word
> "<nomedamarca>" appears in the center, lowercase, bold, white. Precise spelling with the
> accents exactly as written…

6s, 84 cr. Todas as linhas corretas, acento certo, "<nomedamarca>" certo. **Mas**:
`#1C1A20` apareceu escrito no rodapé o clipe inteiro, e houve eco/fantasma da linha
2 durante a transição. Lição dupla: hex vira texto; transição de texto no Omni
borra. Texto longo → `tipo.py`.

## 5. Logo por referência, flat reveal — LOGO FIEL, HEX NA TELA

> @image1 is the brand logo (...). Reproduce it EXACTLY: same letterforms, same colors,
> same proportions. Do not redraw, restyle or recolor it.
> Flat 2D motion graphics, After Effects style, brand reveal. Solid off-white
> background. First, a bold orange circle scales up from the center with an overshoot
> bounce and fills the whole frame. Then the logo from @image1 pops into the center of
> the orange frame with a snappy elastic scale-in, sitting on a clean white rounded
> rectangle card with a soft drop shadow. Then small flat geometric shapes in teal and
> amber — circles, a coin, a small arrow — fly in from the edges and settle around the
> card. Static camera, crisp vector edges, punchy timing. No other text, no extra letters.

6s, 84 cr. Logo idêntica (gradiente âmbar→vermelho, swoosh teal, "pay" fino). Wipe
circular perfeito. **Três códigos hex** (que estavam no prompt original) escritos
na tela como legendas das formas. É o teste que fixou a regra: paleta por imagem.

## 6. Produto por referência, 3D — FORMA FIEL, TELA MIÚDA EMBARALHA

> @image1 is the real product: a card payment terminal with a screen showing the
> brand logo and a green check mark. @image2 is a smartphone showing the real app
> interface. Reproduce both EXACTLY as given…
> Premium 3D motion graphics product film, brand style. Background: a fluid soft-focus
> gradient of orange, amber and teal slowly swirling like silk. The payment terminal
> from @image1 floats in from the right and rotates slowly to face the camera, its
> screen staying sharp and perfectly legible. Then the phone from @image2 slides in from
> the left and settles beside it, slightly tilted, screen perfectly still and readable…

6s, 84 cr em 720p. Maquininha perfeita (logo na moldura e na tela, check, contactless).
O app do celular: layout e cores certos, **texto miúdo virou garatuja** ("Rolancy
Balance"). Tela com elemento grande passa; tela com lista de transações não.

## 7. Continuação com `video_list` — EMENDA PERFEITA, 2×

> Continue this video seamlessly from its last frame, same flat 2D motion graphics
> style, same orange background, same white card with the brand logo… the shapes
> fly out of the frame one by one, then the white card with the logo shrinks with a
> snappy scale-down into the top-left corner…

`video_list: [{url, start:0, ends:6}]`, 168 cr, saiu 6s **novos** (não inclui a
origem). Emenda invisível, logo mantida, movimento pedido. Herdou os hex do clipe 5.

## 8. Paleta como imagem de amostras, 4K — CORES EXATAS, NADA DE CÓDIGO

> @image1 is the brand color palette: five swatches, from left to right amber, orange,
> red, teal and near-black ink. Use exactly these colors for everything in the scene.
> Never display the swatch image itself, never write any color name or code on screen.
> Flat 2D motion graphics, After Effects style. Background: solid ink (the fifth
> swatch). A flat vector coin in amber pops into the center with an overshoot bounce,
> spins once on its vertical axis, then a teal upward arrow draws itself in a single
> stroke from the bottom-left to the top-right behind the coin, and three small orange
> circles pop in along the arrow. Static camera, crisp edges, punchy timing. No text of
> any kind.

4s em 4K, 147 cr. Moeda pop + giro, seta se desenhando, três círculos — tudo nas
cores certas, tela limpa. Uma barra marrom apareceu por 2 frames durante o traço da
seta (artefato transitório). É o formato de prompt padrão da skill.

## 9. Narração por `audio_ids` — BARRADA

Voz criada em `/omni/audio/create` (base `algenib`, descrição em português), clipe
com fala em português no prompt. Duas tentativas, prompts limpos, sem marca na
segunda: `"Your prompt was flagged by Website as violating content policies"`. Não
cobrou. Locução vai por `kie.py tts` e entra na mixagem.

## 11. Keyframe K1 — produto + paleta + post do cliente

> @image1 is the real product: … Reproduce its shape, colours, materials and screen
> exactly. @image2 is the brand colour palette, swatches left to right: coral orange,
> turquoise, vivid red, dark navy, white; use only these colours. @image3 is a style
> reference for the brand's visual language: match its clean white background with a
> soft pale-blue light glow, its rounded soft 3D icons, its depth and its generous
> breathing room, not its content.
> Keyframe for a fintech motion graphics video, 16:9, premium clean design. Pure white
> background with a very soft pale-blue radial glow behind the subject… The product
> floats in the right half of the frame… Around it, three small rounded 3D icons float:
> … The entire left half of the frame is empty white space reserved for a headline. No
> text anywhere, no logo, no letters, no colour codes. Crisp, minimal, studio lit,
> high-end 3D render look.

`nano-banana-pro`, 2K, 18 cr. Saiu no nível do post: produto fiel, ícones 3D,
metade esquerda vazia. O post como `@image3` foi o que fez a diferença.

## 12. Keyframe seguinte — a partir do anterior

> @image1 is the current keyframe of a fintech motion graphics video. Produce the NEXT
> keyframe of the same scene, same camera, same white background with the soft
> pale-blue glow, same lighting and 3D render style. Changes: the terminal has rotated
> to face the camera straight on…; the three floating icons have spread out…; four
> small coral coins have appeared… The entire left half stays empty. No text, no logo.

Mesma cena garantida. Para trocar de ambiente, acrescente um post escuro como
referência e nomeie o elemento de transição ("a dark navy panel", "the bars").

## 13. Keyframe final — o cartão vazio para a logo

> …the bars, the arrow and all badges have faded away; in the exact center floats a
> large clean white rounded rectangle card, completely empty and blank (about 40
> percent of the frame width)… No text, no logo.

A logo entra em pós sobre esse cartão (`montar.sh logo … c`).

## 14. Keyframe completo, com título e logo na imagem — LETRA CERTA

> @image1 is the brand logo: … Reproduce it EXACTLY. @image2 is the real product… @image3
> is the brand colour palette… @image4 is a style reference for the brand's social media
> posts: match its clean white background…, its big bold geometric sans-serif headline in
> dark navy with one line in coral, its small thin support line, its rounded soft 3D
> icons…, not its content.
> Complete social media video keyframe, 16:9… LEFT HALF: a large headline in bold
> geometric sans-serif (Montserrat style), left aligned, three lines: "Transforme" in
> dark navy, "cada venda" in dark navy, "em lucro real" in coral orange; below it one
> short thin support line in dark navy: "…". RIGHT HALF: the product… BOTTOM RIGHT
> CORNER: the logo from @image1, medium size. Spell every word exactly as written, with
> the accents, no other text anywhere, no colour codes.

18 cr. Título, acento, apoio e logo perfeitos, no nível do post. O K seguinte da
mesma cena pede "EXACTLY the same headline… unchanged"; os planos pedem "IDENTICAL in
both frames, not a single letter changes" (parado) ou "old lines slide out to the
left, new lines slide in… no letter morphing" (troca). Dois erros vistos e corrigidos
com regeneração: logo cortada no cartão do fecho (pedir margem) e moeda com sigla
(pedir "plain, blank").

## 10. First frame + last frame por referência — OBEDECE

> @image1 is the FIRST frame of this shot and @image2 is the LAST frame. The video must
> start exactly on @image1 and end exactly on @image2, same camera, same 3D render style.
> Between them: the white dashboard card and its badges lift and fly out through the top
> of the frame; a deep navy panel sweeps in from the right edge and fills the entire
> frame with a clean straight wipe…; then five short glossy turquoise 3D bars rise…
> Static camera, snappy easing, premium motion graphics. No text, no letters, no
> numbers, no logo, no colour codes.

6s, 84 cr, 1080p. Cinco planos assim, encadeados por seis keyframes do
nano-banana-pro: todos começaram e terminaram nas imagens, com o movimento pedido no
meio. É o método da seção "Keyframes encadeados" da SKILL.md. O Veo 3.1
(`FIRST_AND_LAST_FRAMES_2_VIDEO`, 8s, 720p) faz o mesmo com mais "câmera" e menos
precisão nos ícones — e não é o motor desta skill.

## Vocabulário que funciona

| Quer | Escreva |
|---|---|
| pop com overshoot | `pops in with a snappy overshoot bounce` |
| entrar deslizando | `slides in from the right and settles with elastic easing` |
| cair | `drops in from above and lands with a bounce` |
| traço que se desenha | `draws itself in a single stroke from A to B` |
| giro | `spins once on its vertical axis` |
| leque | `fans out into eight identical copies arranged in a circle` |
| wipe circular | `a bold <cor> circle scales up from the center and fills the whole frame` |
| corte de cor | `the background hard-cuts to <cor> and the shapes invert colour` |
| encolher pro canto | `shrinks with a snappy scale-down into the top-left corner` |
| sair | `flies out of the frame to the left` |
| gradiente fluido | `fluid soft-focus gradient of <cores> slowly swirling like silk` |
| vidro 3D | `frosted glass card with soft inner glow, studio lighting from above` |
| travar | `Static camera, crisp vector edges, punchy timing.` |
| sem texto | `No text of any kind, no colour codes.` |

## O que evitar

- `more`, `many`, `fills up` → multiplica sem controle. Conte.
- hex, `RGB`, nome de fonte → vira texto na tela.
- `cinematic`, `epic`, `dramatic lighting` no flat → sai fotografia com brilho.
- Pedir dois movimentos de câmera. Motion é câmera parada; o movimento é dos objetos.
- Texto com número, cifrão, porcentagem → `tipo.py`.
