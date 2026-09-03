# Decomposição em planos — o roteiro decide, não a tabela

Vale para as duas skills de vídeo. É a etapa que mais dá errado quando se pula.

## A ordem certa

Errado, e caro:

> escolher "6 planos de 6s" → gerar as imagens → gerar os vídeos → gravar a
> narração → descobrir que a fala tem 45s e o filme tem 36s

Certo:

1. **Leia o roteiro e liste as batidas.** Uma batida é uma **mudança de
   composição** — cenário novo, personagem que entra, câmera que muda de lugar.
   Não é uma frase nem um parágrafo: é um quadro.
2. **Escreva a narração de cada batida.**
3. **Grave a narração e MEÇA.** Só aí você sabe quanto tempo cada batida precisa.
4. **Dimensione cada plano pela fala que ele carrega**, com respiro.
5. Gere as imagens, confira todas, e só então anime.

A narração é o que manda no tempo. A imagem se ajusta a ela, nunca o contrário.

## Quantos planos

**O roteiro decide.** Conte as mudanças de composição que a história exige — não
force um número redondo.

Sinais de que faltam planos:
- a fala de um bloco passa de ~8s e o quadro fica parado esperando
- duas ideias diferentes disputam o mesmo enquadramento
- você escreveu "e então" no meio de uma batida

Sinais de que sobram planos:
- um plano existe só para "dar movimento", sem carregar informação
- dois planos seguidos dizem a mesma coisa com ângulos diferentes

Numa peça política de lã, 5 a 8 planos deram conta de 45 a 60 segundos. Numa peça
de produto, 10 planos de 6s deram um minuto com corte a cada batida. **Os dois
números saíram do roteiro, não de uma regra.**

## Quanto tempo cada plano

```
duração do plano = fala que ele carrega + 0,6s a 1,5s de respiro
```

- Plano **sem fala** (imagem que trabalha sozinha: engrenagem parada, cofre
  trancado, balança congelada) pede 4 a 6s. Menos que isso não se lê.
- Plano com **uma frase** curta: 5 a 7s.
- Plano com **duas frases**: 8 a 12s — e aí vale considerar dividir em dois.
- Plano de **fecho estático**: 2s parados no mínimo. É o frame que fotografam.

Uma fala pode **atravessar um corte** — é normal em documentário e costuma
melhorar o ritmo. O que não pode é a fala acabar muito antes do plano, deixando
silêncio morto no meio.

## Como conseguir a duração no Grok

| Precisa | Como |
|---|---|
| 6s | `base --dur 6` |
| 16s contínuos | `base --dur 6` + `extend 6 10` |
| 6 a 30s num clipe | `base --dur N` |
| mais que isso, contínuo | não dá — só se estende **uma geração original**, nunca uma extensão |
| segurar um quadro parado | `crop` com expressão de tempo sobre a imagem (rápido; `zoompan` é lento demais) |

Quando um plano precisar durar mais do que o modelo entrega bem, **prefira dois
planos a um clipe esticado** — o Grok degrada no fim das gerações longas.

## Quando o orçamento aperta

Cada plano custa imagem + animação. Se o saldo não cobre o roteiro inteiro:

- **corte batidas, não a narração** — peça curta com explicação inteira vence peça
  longa com explicação pela metade;
- ou entregue um **animatic**: as imagens com movimento de câmera por `crop`,
  narração, música e cartelas. Custa quase nada, mostra o filme inteiro e serve
  para aprovar roteiro e locução antes de gastar na animação.

Diga qual dos dois você fez, e por quê.
