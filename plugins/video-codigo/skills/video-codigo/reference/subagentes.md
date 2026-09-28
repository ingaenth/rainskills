# Produzir várias peças em paralelo

Um kit (filme + 5 reels) sai em ~1 h com subagentes, contra várias horas em série. A unidade
vem do **motor compartilhado + peça-piloto + briefing padronizado**.

## Ordem

1. Você faz o motor da marca e **uma peça-piloto inteira** (valida qualidade e padrões).
2. Um agente por peça restante, todos disparados na mesma mensagem, em segundo plano.
3. Enquanto trabalham: capas, thumbnail, `POSTAGEM.md`.
4. Cada peça que chega: stills + folha + leitura. Pequenos ajustes você mesmo; estruturais
   voltam para o agente (SendMessage) com o que mudar.
5. Render final de tudo (as que dependem de um ajuste no motor são renderizadas de novo) e
   pasta de entrega.

## Briefing de cada agente (modelo)

```
Você vai produzir UMA peça (<formato>) para <cliente> (<o que é, 1 linha>).
Pasta: <caminho>. Ferramentas: node, ffmpeg, playwright prontos. Texto em pt-BR com acentos.

## Motor (leia primeiro; NÃO edite lib.js / lib.css / marca.js / render.mjs)
<lista das funções e classes que importam, 6–10 linhas>
Peça de referência aprovada: <arquivo> — copie estrutura e estilo.

## Marca
<tokens, fontes, logo oficial, regras do manual em 5–8 linhas>

## Assets reais (olhe antes de enquadrar)
<lista com o que tem em cada arquivo; momentos úteis dos vídeos; o que EVITAR por privacidade>

## Regras de formato
<zonas seguras, duração, cartão final e variante>

## Fatos permitidos (não invente outros)
<frases e números do site, copiados literalmente>

## SUA PEÇA: <arquivo>.html — "<título>"
<conceito em 1 linha> + roteiro por tempo (gancho 0–1,5 s, cenas, fecho) + desenho de som.

## Fluxo
STILLS=… node render.mjs <peça> → python folha.py … → leia → itere → render final.

Responda curto: arquivo final, duração, 4 linhas do que tem, o que não fez.
```

## Cuidados

- **Não deixe agentes editarem arquivos compartilhados.** Se precisarem de algo, que façam
  localmente na peça e avisem; você decide se sobe para o motor.
- **Nomes globais**: `lib.js`/`marca.js` declaram funções globais (`halo`, `logo`, `FB`…).
  Avise os agentes para não criarem variáveis com os mesmos nomes (a página nem carrega).
- **Alertas se propagam**: se um agente descobre dado pessoal num vídeo, mande
  imediatamente para os agentes que usam o mesmo material.
- **Troca de marca no meio do caminho**: atualize motor + `marca.js` primeiro, faça um smoke
  test e só então dispare um agente de "rebrand" por peça, com a ordem de manter história,
  tempo e texto e trocar só a camada de marca. Guarde a versão anterior em `_v1/`.
- Peça sempre que o agente **diga o que não fez** e o que mudou em relação ao briefing:
  é ali que aparecem os problemas reais (privacidade, telas enganosas, limites do motor).
