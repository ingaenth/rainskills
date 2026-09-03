# Levantar o material do cliente sem esperar por ele

O cliente demora a mandar arquivo. Quase tudo dá para levantar sozinho, e o que
você levanta do produto real vale mais do que qualquer geração.

## A regra que vale acima de todas

**Captura real do produto ganha de qualquer imagem gerada.** Numa peça de dez
planos, três frames que a IA tinha inventado foram substituídos por prints do
dashboard do cliente — e foram os três melhores do filme. Sempre que a tela
existir, ela entra no lugar do que a IA imaginaria.

Peça explicitamente: **"me manda print da tela que faz isso"**. É a pergunta que
mais melhora a peça, e quase nunca é feita.

## Do site

```bash
curl -s -L "https://site.com" -o home.html
grep -oiE '<title>[^<]*</title>|<meta[^>]*(description|og:image)[^>]*>' home.html
grep -oiE '(src|href)="[^"]*\.(svg|png|jpg|webp)"' home.html | sed 's/.*="//;s/"//' | sort -u
grep -oiE '#[0-9a-f]{6}' home.html | sort | uniq -c | sort -rn | head
```

- O `og:image` costuma apontar para o domínio de produção, mesmo num site de
  homologação — é uma pista de qual é o endereço público.
- As cores mais repetidas no CSS são a paleta real. Não pergunte o hex se dá para
  ler.
- O texto visível da home é o melhor insumo de copy que existe: são as palavras
  que o cliente já aprovou.

## Captura de tela

`ffmpeg` não renderiza HTML nem SVG. Use o Chrome em headless:

```bash
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless --disable-gpu --hide-scrollbars --window-size=1600,1000 \
  --virtual-time-budget=9000 --screenshot="$PWD/tela.png" \
  --user-data-dir=/tmp/chr-$RANDOM "https://site.com" &
P=$!; for i in $(seq 1 45); do [ -f tela.png ] && break; sleep 2; done; kill $P
```

- **Rode em background e espere o arquivo aparecer.** Em foreground o processo
  trava a sessão e estoura o tempo.
- `--user-data-dir` próprio evita conflito com o Chrome do usuário e com o
  Playwright, que reclama `Browser is already in use`.
- **Site animado por scroll não renderiza em headless.** As seções internas voltam
  vazias. Capture o que aparece sem rolagem e peça o resto ao cliente.
- **Splash tem timing instável**: o mesmo `--virtual-time-budget` ora pega a
  animação, ora já passou. Se a captura vier vazia, repita com outro valor.
- Para logo maior, `--force-device-scale-factor=2` em vez de ampliar depois.

## Rasterizar SVG

`qlmanage` encaixa o SVG num quadrado e **corta** o que passa — logo horizontal
sai mutilado. Renderize no Chrome, com o SVG dentro de um HTML no tamanho certo:

```html
<html><body style="margin:0;background:#fff;display:flex;
  align-items:center;justify-content:center;height:700px">
<img src="logo.svg" style="width:1900px"></body></html>
```

## Transparência do logo

Se o logo veio chapado num print, **não chaveie por luminância** — a parte
colorida da marca some junto com o fundo. Chaveie pela cor do fundo:

```bash
ffmpeg -i logo.png -vf "format=rgba,colorkey=0x0A0A16:similarity=0.34:blend=0.08" \
  -pix_fmt rgba logo_alpha.png
```

Sobre fundo escuro o resíduo é invisível. Para conferir, componha com `overlay` —
`pad` e `scale` achatam o alfa e mentem sobre o resultado.

## Redes sociais

Perfil e métricas saem dos MCPs de Instagram (`datalikers`, `hikerapi`), mas eles
**não devolvem a URL da imagem** do post. Para a arte:

```bash
"$CH" --headless --window-size=700,900 --virtual-time-budget=8000 \
  --force-device-scale-factor=2 --screenshot="$PWD/post.png" \
  "https://www.instagram.com/p/CODIGO/embed/captioned/"
```

O **endpoint `/embed/captioned/` serve o post sem login** e em boa resolução. A
página de perfil, ao contrário, abre um modal que escurece o grid inteiro.

Depois, corte o cabeçalho e o rodapé do embed:
`ffmpeg -i post.png -vf "crop=iw:iw:0:120" arte.png`

**Antes de usar como case, olhe o engajamento.** Um perfil com 1.188 seguidores e
1 a 8 curtidas por post não sustenta uma peça que promete resultado — nesse caso o
resultado a mostrar é o **conteúdo em si**: volume, consistência, qualidade
editorial. Prometer alcance que o número desmente destrói a peça na primeira
checagem.

E confirme **autorização por escrito** para usar a marca do cliente do cliente em
material comercial.
