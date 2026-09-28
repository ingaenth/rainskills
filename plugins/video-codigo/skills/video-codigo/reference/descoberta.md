# Descoberta — marca, fatos e mídia

## Texto do site

```bash
curl -sL https://site.com/ -o site.html
PYTHONIOENCODING=utf-8 python -c "
import re,html; s=open('site.html',encoding='utf8',errors='ignore').read()
s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>','\n',s)); print('\n'.join(l.strip() for l in t.split('\n') if l.strip())[:10000])"
```

- `PYTHONIOENCODING=utf-8` evita o erro `charmap` do Python no Windows com setas e acentos.
- Contadores animados ("0+ canais", "+0 mil") vêm zerados no HTML. O número real está no
  código (`content.ts`, `data/*.json`) ou no site renderizado; nunca publique o zero.

## Visual renderizado

Playwright, 1440×900, role a página inteira devagar (lazy-load) e tire a foto da página
inteira. Corte em faixas e leia. Pegue também o estilo computado do `body` e do `h1` (fonte,
cor), e as variáveis CSS (`--primary`, `--background`…) do CSS principal.

## Repositório (quando existe)

Procure: `SPEC.md`, `CLAUDE.md`, `tailwind.config.*`, `globals.css`, `src/data/content.ts`,
`public/media`, `public/brand`. Copie a pasta de mídia inteira para `assets/` do projeto.
**Não rode build nem dev server** num repositório que serve ambiente ao vivo.

## Manual de marca (quando existe)

Leia o texto inteiro e anote: arquivos oficiais do logo e suas versões, cor principal e
neutros (com HEX), o que é proibido (degradê, azul antigo, sombra, recolorir), fontes de
título e texto, elementos gráficos permitidos, regras de movimento e tom de voz. **O manual
vence o site** quando os dois divergem, e o usuário pode ter trocado a marca depois do site.

## Mídia oficial

- Otimizadores (`/_next/image?url=…`) costumam recusar download direto
  (`INVALID_IMAGE_OPTIMIZE_REQUEST`). Pegue o **caminho original** (`/images/x.webp`) ou
  capture as respostas de rede com Playwright (`page.on('response')`).
- Arquivos `.webp` que na verdade são AVIF (`ftyp`): converta com ffmpeg para PNG.
- Vídeos MP4 H.264 **não tocam no Chromium do Playwright** (build sem codecs proprietários):
  converta para WebM VP9 (`ffmpeg -i x.mp4 -c:v libvpx-vp9 -b:v 0 -crf 26 -an x.webm`).
- Ícones de canais (WhatsApp, Instagram…): `https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<nome>.svg`.
- Folha de contato de todas as imagens e de quadros de cada vídeo (1 a cada 5 s) antes de
  planejar.

## Checagem de privacidade (obrigatória)

Prints e gravações reais vazam dado de cliente com frequência, **inclusive os que já estão
publicados no site do próprio cliente**. Já encontrados em produção:

- inbox de atendimento com **telefones legíveis e mensagens de cunho político**;
- tela de importação com **nomes, CPFs e datas de nascimento** sem borrão;
- exemplos de campo mostrando **e-mails parciais**;
- gráficos com caixas de borrão improvisadas.

Regra: todo quadro de print ou vídeo que entra na peça é olhado em **tamanho cheio**. Se há
dado legível, troque por outro momento, outro print já borrado, ou borre localmente (PIL
`GaussianBlur` na região). Nunca faça de um dado borrado o foco de um zoom. Na entrega,
**avise o usuário** que o material público dele expõe dados e ofereça corrigir na fonte.
