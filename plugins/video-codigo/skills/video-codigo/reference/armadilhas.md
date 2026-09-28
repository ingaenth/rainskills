# Armadilhas — vídeo em código

## Processo e cliente

| Sintoma | Causa | Solução |
|---|---|---|
| "Fez um vídeo exatamente igual" | reaproveitou a estrutura do cliente anterior trocando as cores | conceito novo por cliente (`conceito.md`); o motor é compartilhado, a ideia não |
| "Quando enviei ficou ruim" (capa cortada) | texto da capa fora do quadrado central | todo conteúdo em y 420–1500; folha com recortes 1:1 e 4:5 |
| Blocos e faixas depois do upload | MP4 de ~2,5 Mb/s recomprimido pelo Instagram | 16 Mb/s; "upload em alta qualidade" |
| Logo "azul" quando o site parece roxo | o logo usa uma cor e o site aplica degradê/tons diferentes | olhar o site renderizado, não só o código; perguntar ou seguir o manual |
| Logo recolorido/degradê reprovado | manual proíbe | logo só pelos arquivos oficiais; degradê é recurso de página, não de logo |
| Dado de cliente no vídeo | print ou gravação real sem borrão | checar cada quadro em tamanho cheio; borrar local; avisar o cliente |
| Número "0" no vídeo | contador animado do site lido do HTML estático | pegar o valor do código (`content.ts`) ou do site renderizado |
| "Ficou simples, tudo pequeno, uma cor só" | tamanhos de página web, um fundo do início ao fim, cena sem herói | escala de cartaz, ritmo de cor planejado no briefing, um herói por cena (`direcao-de-arte.md`); revisão de diretor de arte na folha |
| Vídeo genérico, "podia ser de qualquer empresa" | produziu sem entrevista; nenhuma referência do cliente | entrevista (`entrevista.md`): referências + anti-referência + personalidade antes do conceito |
| Vídeo no idioma errado | assumiu o idioma da conversa | perguntar/propor o idioma do público (negócio nos EUA → inglês) |
| Texto que o cliente não escreveu, sem aviso | título/slogan/fecho criados por nós | seção "Fatos e textos" do briefing marca "escrito por nós — aprovar" |
| "Diz que entregou mas não está lá" | README/relatório listou masters que nunca foram renderizados; entrega commitada numa branch do repositório | `ls` + `ffprobe` antes de anunciar; entregar na pasta do briefing, não em commit |

## Render e navegador

| Sintoma | Causa | Solução |
|---|---|---|
| Vídeo MP4 não aparece | Chromium do Playwright sem H.264 | converter para WebM VP9 |
| Quadro de vídeo errado/atrasado | seek assíncrono | `seekVideo()` dentro de `on()`; o `render.mjs` espera o `seeked` |
| Fonte errada nos primeiros quadros | fonte não carregada | `&display=block` no Google Fonts; o `boot()` espera `document.fonts.ready` |
| Imagem em branco no 1º quadro | não decodificada | o `boot()` espera `img.decode()`; imagens criadas depois do boot precisam de decode próprio |
| `page.goto ERR_FILE_NOT_FOUND` | caminho relativo errado ou arquivo não criado | rodar da pasta do projeto; `node render.mjs peca.html` |
| `setContent` não carrega assets locais | página `about:blank` sem acesso a `file://` | salve um `.html` e use `goto(file://…)` |
| Página não carrega depois de juntar scripts | nome global duplicado (`const halo` vs `function halo`) | renomear na peça |
| Elemento parado no canto superior esquerdo | cursor/ripple com opacidade padrão fora da cena | `opacity:0` por padrão (já no `lib.css`) |
| Número "dançando" ao contar | largura variável dos dígitos | `.mono` / `font-variant-numeric:tabular-nums` |
| Quadrado preto atrás de imagem | PNG/arte com fundo preto sobre fundo escuro | `mix-blend-mode:screen` ou versão com alfa |
| Câmera mostrando área vazia do print | alvo da câmera mal escolhido | ler o print antes; `shot.set` trava na imagem, mas escolha o centro com conteúdo |
| Texto longo quebrando feio em outra fonte | trocou a fonte do título (ex.: Inter → Montserrat) | revisar todas as quebras; `|` manual nas legendas |
| Metade dos textos grudada no topo esquerdo | elemento criado com `div()` sem classe de posição e sem `place()` | `place()` já define `position:absolute`; todo elemento de cena passa por `place()` |
| "g", "y", "p" cortados ou itálico cortado no fim | máscara com `overflow:hidden` justa na linha | `mline()` / `priceRow()` já têm folga; em máscara própria use `padding-bottom:.22em` |
| Assunto da foto sumiu no 9:16 | foto 16:9 em tela cheia mostra só ~1/3 da largura | `photo()` com ponto focal, caixa parcial (60–65% da altura) ou versão 9:16 da imagem |
| Título em cima do rosto | foto em tela cheia com texto na faixa do assunto | foto em caixa parcial ou foco deslocado; texto na área de sombreamento |
| Render lento com fotos 4K | imagem original enorme decodificada a cada quadro | redimensionar para ~2400 px no lado maior antes |

## Ambiente (Windows + Git Bash)

| Sintoma | Causa | Solução |
|---|---|---|
| `UnicodeEncodeError: 'charmap'` | stdout do Python em cp1252 | `PYTHONIOENCODING=utf-8` |
| heredoc/`python -` quebra com aspas e crases | parsing do shell | gravar o script num arquivo `.py` e rodar |
| `sed` com `#` ou `&` estraga a linha | delimitador/escape | usar Python para substituições com trechos longos |
| Download "ASCII text" em vez de imagem | otimizador de imagem recusou (`INVALID_IMAGE_OPTIMIZE_REQUEST`) | caminho original do arquivo ou captura de rede no Playwright |
| Render em paralelo travando a máquina | muitos Chromium + ffmpeg | no máximo 3 renders simultâneos |
