# Produção — receitas testadas

## Montagem (ffmpeg, grafo único)

Um script Python gera o filtro inteiro; remontar é grátis e leva ~1 min:

1. **Desacelerar cada clipe uma vez** e cachear:
   `scale=1920:1080:flags=lanczos,setpts=PTS/0.65,framerate=fps=24` → `slow_N.mp4`.
2. **Corrente de xfade**: `offset = t + SL - XF` acumulando (SL = 6/0.65 ≈ 9.23s,
   XF = 0.7). Último xfade entra no fecho (`-loop 1 -t 5.7 -i fecho.png`).
3. **Cartelas**: um PNG 1920×1080 RGBA por plano, overlay com
   `fade=in:st=A:d=0.5:alpha=1,fade=out:...` e `enable='between(t,A,B)'`,
   com A = início do plano + 1.2 e B = fim − 1.3.
4. **Áudio**: música com `-ss` no ponto bom + ambiência `-stream_loop` + SFX com
   `adelay` no timestamp do plano; `amix=inputs=3:normalize=0` e
   `loudnorm=I=-14:TP=-1.5:LRA=11`.
5. Master H.264 CRF 18 + prévia web 720p CRF 28 num só passe.

## Slow motion de material real

```
setpts=PTS/0.22,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1,
scale=642:-2,crop=640:1080,hqdn3d=3:2:6:4,unsharp=5:5:0.4
```

- 0,5× parece vídeo lento, não slow motion. Cliente pediu "mais devagar" DUAS vezes:
  0,65× → 0,5× → 0,3× → **0,22×** foi o aprovado.
- `minterpolate` é caro (minutos) — rode em background e cacheie.

## Díptico / tríptico de verticais

`hstack` de painéis 640×1080 (tríptico) ou 960×1080 (díptico). Rótulos e filete num
único overlay PNG por cima do stack. Painel central de foto:
`zoompan=z='1+0.0009*on':y='...-0.8*on'` — zoom tem de ser VISÍVEL (≥15% no total),
micro-zoom em painel pequeno lê como parado.

## QC antes de mostrar qualquer coisa

- **Grade início/meio/fim** de cada clipe animado (3 frames × N clipes numa imagem).
  Olhe: mãos, dedos, rostos, letras de placas, objetos que nascem ou somem.
- **ebur128** no master: I entre −14.5 e −13.5 LUFS.
- Frame do fecho e da abertura lado a lado: o loop precisa emendar sem susto.
- Publique a prévia numa URL (o cliente vê do celular) e SÓ substitua o master
  oficial depois do OK — mantenha o anterior em `_anteriores/`.

## Organização de entrega (padrão que o cliente pediu)

```
videos/            finais aprovados, por canal: tv/<unidade>/, instagram/<unidade>/
materia-prima/     brutos do cliente, nunca editados
producao/<peça>/   quadros, clipes, cartelas, scripts, PDFs de aprovação, _anteriores/
analises/          tudo que não é produção
```

Os scripts de montagem escrevem o master direto em `videos/...` — remontou,
o oficial atualizou. Guarde TODO quadro/clipe reserva: a iteração seguinte
quase sempre reaproveita.

## Armadilhas de API (kie.ai)

- `createTask` devolve erro no corpo com HTTP 200 — cheque `data` antes de indexar.
- Tarefa de imagem presa em `generating` >15 min: dispare uma duplicata e fique com
  a primeira que voltar (6 cr a mais, meia hora a menos).
- URLs de resultado expiram em ~24h — baixe na hora.
- Upload de referência: endpoint `file-base64-upload` com `uploadPath` fixo por
  projeto; guarde as URLs num `refs.json` para reusar entre gerações.
