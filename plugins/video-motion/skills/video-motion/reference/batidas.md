# A grade de batidas — o beat decide, não a narração

Em motion, o tempo é musical. Cada evento visual cai numa batida; cada plano dura um
número inteiro de batidas; a música é pedida no andamento que a peça precisa, ou a
peça se alinha ao andamento que a música tem.

## A grade

```
batida = 60 / BPM      compasso = 4 batidas      frase = 8 batidas (2 compassos)
```

| Andamento | BPM | batida | compasso | serve para |
|---|---|---|---|---|
| calmo | 90 | 0,67s | 2,7s | SaaS, fintech B2B, reveal 3D |
| médio | 110 | 0,55s | 2,2s | promo, marca, produto |
| rápido | 125 | 0,48s | 1,9s | comida, varejo, oferta, Reels |

`batidas.py grade --bpm 110 --dur 20` imprime os instantes. `--sub 2` acrescenta as
colcheias, que são onde entram as palavras rápidas.

## Como as seis referências gastam os beats

Decupadas frame a frame (`ffmpeg -vf "fps=3,tile=5x5"` sobre o download). O padrão
se repete em todas:

**Pizza (8s, 9:16, flat).** 0–1,5s: painel amarelo entra em diagonal, título sai letra
a letra (máquina) + "IN TOWN" em pill. 1,5–3s: a pizza **voa** de baixo e assenta com
overshoot, tomates e pimentas entram atrás, vapor sobe. 3–4s: selo de preço pop.
4–5s: botão "ORDER NOW" desliza. 5–6s: nome e telefone em máquina. 6–8s: **parado**.
→ 6 eventos em 8s; 2s finais estáticos.

**Fanta (10s, 1:1, flat).** 0–0,5: mancha preta/branca (transição orgânica). 0,5–2:
lata desce, gomos e folhas orbitam. 2–3,5: logo pop no canto, splash de suco. 3,5–4:
**círculo laranja escala do centro e vira o fundo** (o wipe circular). 4–5,5: copo
de suco + gomo. 5,5–6: painel diagonal preto/vermelho (wipe de painel). 6–10:
lata dentro de círculo com letras gigantes girando atrás, "Visit More" em pill.
→ cada bloco ≈ 1,5s (≈ 3 batidas a 120); dois wipes de cor, um circular e um diagonal.

**Burger King (15s, flat, tipografia como cenário).** 0–2: "EXAGEEEERO" **rola** da
direita para a esquerda em letras que ocupam a altura toda. 2–4: fundo troca
vermelho → verde → creme **a cada batida**, o hambúrguer com mãos-ilustração no
centro, texto repetido atrás como padrão. 4–5: faixas horizontais + "de SABOR!"
distorcido pop. 5–7: "REFRIIIII" em máquina com o copo, fundo vermelho → verde. 7–9:
padrão de batatas em repetição atravessando em diagonal. 9–11: Whopper embrulhado
sobre ilustração de ingredientes. 11–13: "Whopper" máquina, hambúrgueres voando
desfocados (profundidade). 13–15: logo no creme, **parado**.
→ ~94 BPM medido; a troca de fundo por batida é o motor do ritmo.

**Dexatel (22s, flat, produto de tecnologia).** 0–4: "Bots are getting smarter" uma
palavra por beat, notificações falsas empilhando ao redor. 4–7: fundo escuro,
celular em wireframe, "Fake users? / accounts? / everything" trocando por beat. 7–8:
**flash branco** e o logo desenha (o "D" primeiro, depois o nome, depois "Verify"
em máquina). 8–13: "Verify humans across any channel" com nuvem de ícones e palavras
em cinza flutuando; celular com notificação real, fundo tingido pela cor do canal
(verde SMS, roxo Viber, verde WhatsApp, rosa chamada). 13–17: "Deny fakes" →
itálico → "Instantly" em azul chapado (**inversão de cor no beat**). 17–22: logo +
pill com pergunta, **parado**.
→ dor em 3 beats, virada com flash, prova por canais, promessa em 2 palavras.

**NeuraFlow (20s, 3D com gradiente).** Logo com glow, painel de UI de vidro que
desliza e ganha camadas (percentual sobe no canto), o nome gigante atrás desfocado,
"New Updates" num anel com ícones orbitando, chat com bolhas entrando, cards em
carrossel 3D, transição por **forma da marca** (a estrela quatro pontas vira o wipe)
e fecho com logo. Tudo lento: ~2,5s por bloco, câmera quase parada, luz de cima.
→ é o 3D do Omni: `Premium 3D motion graphics product film, fluid gradient...`.

**Stone (57s, híbrido).** Ato 1 (0–12s): flat cinético puro — "ESTAMOS / DE CARA /
NOVA" empilhando por beat em verde, letras densas condensadas, inversão de cor;
"EVOLUÍMOS / JUNTO COM O / EMPREENDEDOR". Ato 2 (12–20s): o símbolo se **desenha em
grade** (linhas de construção) e vira o logo sólido sobre gradiente fluido verde.
Ato 3 (20–35s): "CORES MAIS VIBRANTES", paleta em faixas, nome repetido em lista
(máquina). Ato 4 (35–57s): **3D** — cartão gira, abre em leque de oito, caixa da
maquininha, celular com app, tudo flutuando no gradiente. ~79 BPM medido.
→ o modelo de peça longa: **tipografia em pós no ato 1, Omni 3D no ato 4**.

## O padrão que sai daí

```
gancho     2–4 beats   palavra gigante ou produto pop        tipo.py / Omni
dor/tese   4–8 beats   3 palavras, uma por beat, fundo trocando   tipo.py
virada     1 beat      flash, wipe circular ou painel         tipo.py (painel) / Omni (forma da marca)
produto    8–16 beats  o objeto: entra, gira, mostra a tela   Omni
prova      4–8 beats   3 capacidades, ícone + palavra         Omni (ícone) + tipo.py
fecho      4 beats     logo + claim + CTA, PARADO 2s          montar.sh logo + tipo.py
```

Máximo três mensagens. Se o cliente mandar sete, três viram esta peça e quatro viram
a próxima.

## Keyframes encadeados: o clipe manda no corte

Quando os planos são animados entre keyframes, **cada clipe entra inteiro** (6s): o
último frame de um é o primeiro do seguinte. Não escolha a duração do plano pela
batida — escolha a grade pela música e encaixe os eventos de texto e som nela.
Exemplo real: música a 160 BPM (batida 0,375s), 5 planos × 6s = 30s, cada plano
16 batidas; títulos entram em múltiplos de 0,375s.

## Dimensionar os clipes do Omni (cenas geradas do texto)

O Omni entrega 4, 6, 8 ou 10s. O roteiro pede durações em batidas, que raramente
batem nisso. **Peça o tamanho imediatamente acima e corte no beat**:

```
batidas.py cortes "4,2,2,8,8,4" --bpm 110 --dur 20
```

Ele imprime início e fim de cada plano, e qual duração pedir ao Omni. Um plano de
mais de 10s: dois clipes com corte seco, ou `--continua` (2×, só quando a emenda
tem de ser invisível).

**Quais planos vão ao Omni:** os que têm objeto — produto, logo animada, ilustração,
fundo fluido, 3D. Plano só de palavra sobre fundo chapado **não gasta crédito**: é
`tipo.py` sobre `tipo.py fundo`. Numa peça de 20s típica, 3 a 4 planos vão ao Omni.

## Quando o orçamento aperta

- Reduza os planos de Omni, não a peça: mais beats de tipografia, menos de objeto.
- Produto por recorte estático (`montar.sh logo` com o PNG do produto, entrando com
  fade) em vez de clipe animado — funciona para o plano de prova, não para o hero.
- Entregue o animatic como peça: para Stories e teaser, tipografia + fundo + som
  **já é um vídeo de motion**.

Diga qual dos três você fez, e por quê.
