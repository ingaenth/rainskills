# BRIEFING.md — o prompt mestre da peça

Saída da entrevista ([entrevista.md](entrevista.md)). Fica na pasta do projeto e é a
**única fonte de verdade** da peça: o código segue o briefing, os subagentes recebem o
briefing, e todo ajuste do cliente entra primeiro aqui. Preencha tudo; o que não se aplica
é marcado "n/a", nunca apagado. Cada valor diz **de onde veio** (arquivo, resposta do
usuário ou "assumido por nós").

```markdown
# BRIEFING — <nome da peça> · <cliente>
Status: rascunho | aprovado em <data> por <quem>

## 1. Missão
<Uma frase: o que este vídeo faz, para quem, onde. Ex.: "Mostrar a carta de tratamentos
do spa com preços reais para quem rola o Reels sem som, e levar ao agendamento.">

## 2. Exibição
- Plataforma/lugar: …            - Formato(s): 9:16 1080×1920 | 16:9 … | 1:1 …
- Duração alvo: … s   · fps: 30  - Som: sim/não/opcional · legendas: sim/não
- Zonas seguras / loop / distância de leitura: …

## 3. Público e idioma
- Quem assiste, em que momento, o que já sabe: …
- Idioma: …  · formato de preço/telefone/data: …

## 4. Personalidade → movimento
- Eixos (calmo↔energético, luxo↔acessível, sério↔divertido, editorial↔tecnológico): …
- Duração média de cena: … s  · curvas: …  · BPM/trilha: …
- Transições permitidas (2–3 tipos): …   · Proibido: …

## 5. Identidade
| Token | Valor | Papel | Fonte |
|---|---|---|---|
| cor escura | #… | fundo, texto sobre claro | tailwind.config.ts:12 |
| cor clara | #… | papel, texto sobre foto | … |
| destaque | #… | filete, preço, CTA (fundo inteiro? sim/não) | manual p.4 / resposta 8 |
| fonte display | … pesos … | títulos, números | fonts.ts |
| fonte texto | … | rótulos, corpo | … |
| logo | arquivos (claro/escuro), largura mínima, pode animar? | … | … |
- Proibições do manual: …
- Referências (o que tirar de cada): 1. … 2. … 3. …   · Anti-referência: …

## 6. Direção de arte  (ver direcao-de-arte.md)
- Modo visual: interface | editorial/foto | tipográfico/dados | misto
- Escala tipográfica (px no quadro): display … · título de seção … · linha/nome … · número/preço … · rótulo … · corpo mínimo …
- Ritmo de cor (fundo de cada cena, em ordem): escuro-foto → claro → destaque → …
- Texturas/camadas: grão …% · vinheta · sombreamento sobre foto …

## 7. Conceito
- Frase-tese (da fonte): "…"
- Metáfora / ideia: … — por que só serve para este cliente: …
- Gancho (primeiro 1,5 s, sem som): …

## 8. Roteiro cena a cena
| # | t0–t1 | Fundo / cor | Herói (asset ou elemento) | Texto exato | Movimento / transição de entrada | Som |
|---|---|---|---|---|---|---|
| 1 | 0–3,7 | foto pôr do sol | logo grande | "Pompano Beach · Florida" … | câmera 1,2→1,04; logo desfoca→nítido | sino + pad |
| … |

## 9. Fatos e textos
| Texto na tela | Fonte | Aprovação |
|---|---|---|
| Signature Massage — from $139 | site/content/services.json | fato |
| "Your ritual awaits." | escrito por nós | aprovar |

## 10. Assets
| Arquivo | O que mostra | Foco/recorte | Aprovado? | Privacidade ok? |
|---|---|---|---|---|

## 11. Entregáveis
- Masters: <pasta>/<nome>.mp4 (formato, duração) · capas · thumbnail · POSTAGEM.md
- Versões: …

## 12. Aprovação e decisões assumidas
- Paradas de aprovação: …
- Decisões que tomamos sem perguntar (o cliente pode trocar): …
- Fora do escopo desta peça: …
```

## Como usar o briefing

- **Antes do primeiro render longo**: mostre o resumo (missão, formato, conceito, a
  sequência de fundos das cenas, as decisões assumidas) e peça OK.
- **Subagentes/execuções separadas** recebem o `BRIEFING.md` inteiro mais a peça-piloto;
  nada de repassar a marca "de memória" ([subagentes.md](subagentes.md)).
- **Ajuste do cliente** ("ficou pequeno", "troca a frase"): atualize o briefing (escala,
  texto, ritmo) e só então o código. Assim a próxima peça já nasce corrigida.
- **Na entrega**, o briefing vira a checklist: cada linha das seções 8, 9 e 11 conferida.
