# Levantar o kit de marca sem esperar pelo cliente

Vale tudo de `video-produto/reference/materiais.md` (site, captura headless, SVG,
Instagram, transparência por `colorkey`). Aqui, o que é específico de motion.

## Posts do cliente são a referência principal

Um post real vale mais que qualquer descrição. Peça 2 ou 3; se não vierem, capture
do Instagram (`/p/CODIGO/embed/captioned/`). Separe um **claro** e um **escuro**:
cada keyframe usa o post do seu ambiente como `@image` de estilo. Suba com o kit
(`--estilo`).

## Projeto no disco

```bash
find ~ -maxdepth 3 -iname "*<cliente>*" -not -path "*/node_modules/*"
find <projeto> -path "*/brand/*" -o -iname "*theme*.css" -o -iname "*tokens*" | grep -v node_modules
```

`theme.css`/`tokens.ts` trazem hex, fonte, raios e easings; `brand/assets` traz logo
e recortes. **Mas confirme com o cliente se essa identidade é a dos posts** — em
produção, os tokens do site eram de uma versão anterior da marca.

## Recortes de produto

- PNG com alfa → `marca.py kit --produto x.png`.
- **Verifique se é PNG de verdade**: `file x.png`. WebP renomeado devolve
  `Internal Error` no nano-banana-pro; `kie.py imagem` converte sozinho, `marca.py`
  não. `ffmpeg -i x.png y.png` resolve.
- Sem recorte: `kie.py imagem "product cutout of <descrição>, isolated on plain white,
  studio lighting, no text" --ref logo_url` (18 cr) e `colorkey`.

## Fontes

- `fc-scan --format "%{family} | %{style}\n" arquivo.ttf` dá o nome que vai no JSON.
- **Google Fonts**: o repositório `google/fonts` só tem a variável; a API CSS entrega
  instâncias com nomes de família errados. Pegue as estáticas no repositório da
  fundição (Montserrat: `JulietaUla/Montserrat`, pasta `fonts/ttf/`) ou peça o arquivo
  ao cliente.
- Sem a fonte: `Liberation Sans Narrow` (bold condensada) ou `DejaVu Sans` (bold).
  Diga que é substituta.

## O que não levantar sozinho

Métrica, autorização de marca de terceiro, depoimento, e **qual identidade vale**.
