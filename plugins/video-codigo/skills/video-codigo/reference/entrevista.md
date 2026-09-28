# Entrevista — perguntar para personalizar

Nenhuma marca é igual, nenhum vídeo é igual. A skill não tem estética padrão: tudo o que
define a peça sai da **descoberta** e desta **entrevista**, e é registrado no
`BRIEFING.md` (o prompt mestre, [briefing-prompt.md](briefing-prompt.md)). Pular a
entrevista produz o vídeo "correto e sem graça" que o cliente reprova.

## Como perguntar

1. **Descubra antes de perguntar.** Site, repositório, manual, redes e mídia primeiro
   ([descoberta.md](descoberta.md)). Só pergunte o que a descoberta não resolve ou onde ela
   encontrou conflito. Nunca pergunte algo que o usuário já disse na conversa.
2. **Toda pergunta traz uma proposta concreta**, tirada do que você achou:
   *"O site usa Cormorant + dourado #B08D57; os posts do Instagram usam fundo creme. Qual
   identidade vale para o vídeo?"* Pergunta vaga ("qual o tom?") gera resposta vaga.
3. **Rodadas curtas e adaptativas**: até 4 perguntas por rodada, de 2 a 4 rodadas. A
   rodada seguinte depende das respostas anteriores (quem respondeu "TV da recepção" não
   precisa ouvir falar de zonas do Instagram).
4. **Múltipla escolha**, com a opção recomendada primeiro, marcada "(recomendado)", e o
   porquê em meia linha. Sempre deixe espaço para "outro". Use a ferramenta de perguntas
   da interface (AskUserQuestion) quando existir; senão, pergunte em texto numerado.
5. **Linguagem de cliente**, não de motor: "o vídeo vai passar sem som?" e não
   "OfflineAudioContext on/off".
6. **"Faz como achar melhor"** é resposta válida: siga as propostas e registre no
   briefing, na seção *Decisões assumidas*, quais foram suas. Se o usuário pedir para não
   perguntar nada, faça uma rodada só com as 3 perguntas que mais mudam a peça (objetivo e
   lugar, material visual, referências) e assuma o resto.
7. **Anote na hora.** Cada resposta entra no `BRIEFING.md` assim que chega. É ele, e não
   a sua memória da conversa, que vai guiar o render e os subagentes.

## Rodada 1 — para que serve (sempre)

| # | Pergunta | Por que muda a peça |
|---|---|---|
| 1 | **Objetivo**: vender/agendar, apresentar a marca, lançar produto, explicar como funciona, anunciar oferta, recrutar, relatório/apresentação interna | define o fecho (CTA × assinatura), a quantidade de informação e o gancho |
| 2 | **Onde vai rodar**: Reels/Stories/TikTok, anúncio pago, feed, YouTube/site (hero), TV da recepção ou loja, evento/apresentação, WhatsApp | formato, duração, se o som existe, zonas seguras, loop, distância de leitura |
| 3 | **Quem assiste e em que momento**: rolando o feed sem som, esperando na recepção, numa reunião, já é cliente ou nunca ouviu falar | ritmo, quanto texto cabe, nível de explicação |
| 4 | **Idioma e mercado** (proponha o do site/público: um negócio nos EUA fala inglês mesmo que a conversa seja em português) | todo o texto, formato de preço, data e telefone |

## Rodada 2 — identidade e gosto

| # | Pergunta | Por que muda a peça |
|---|---|---|
| 5 | **Referências**: "Me mostra 2 ou 3 vídeos, posts ou marcas cujo visual você admira, e 1 que você **não** quer parecer" | é a pergunta que mais personaliza; sem ela, você chuta. Leia cada referência e anote o que tirar dela (cor, ritmo, tipografia, transição) |
| 6 | **Qual identidade vale** quando site, manual e redes divergem | evita "vídeo de outra marca" |
| 7 | **Personalidade**, em pares com proposta: calmo ↔ energético · luxuoso ↔ acessível · sério ↔ divertido · editorial ↔ tecnológico · minimalista ↔ exuberante | vira parâmetros: duração de cena, curvas, BPM, tamanho e peso da tipografia, quantidade de cor ([direcao-de-arte.md](direcao-de-arte.md)) |
| 8 | **Regras de marca que a descoberta não respondeu**: pode usar a cor de destaque como **fundo inteiro**? Há versão clara e escura do logo? O logo pode animar? Movimento com "pop"/quique é aceito? Arquivo da fonte oficial? | decide o ritmo de cor, o cartão final e as curvas; manual vence o gosto |

## Rodada 3 — material e conteúdo

| # | Pergunta | Por que muda a peça |
|---|---|---|
| 9 | **Material visual** — mostre a folha de contato do que achou e pergunte: quais estão **aprovados para uso**? Há mais (fotos reais, banco de imagens, gravações de tela, vídeos)? Pessoas nas fotos têm autorização? | escolhe o modo visual (interface, editorial/foto, tipográfico, misto) e evita usar imagem vetada |
| 10 | **A mensagem**: a UMA ideia que o espectador precisa lembrar, e até 3 de apoio | estrutura e hierarquia; mais de 3 mensagens é outra peça |
| 11 | **Fatos que entram** — proponha a lista com fonte ("Signature Massage $139 — services.json; 4.9 / 754 — business.ts") e peça confirmação. Pergunte por oferta, validade e ressalvas | só fato com fonte vai ao ar |
| 12 | **CTA e destino**: texto exato e para onde leva (site, agendamento, WhatsApp, link na bio, telefone) | o fecho |
| 13 | **Textos escritos por nós** (título, slogan, frase de fecho): pode? precisam de aprovação? | tudo que não veio da fonte é sinalizado no briefing |

## Rodada 4 — produção e entrega (só o que ainda estiver aberto)

| # | Pergunta | Por que muda a peça |
|---|---|---|
| 14 | **Formatos, duração e versões**: 9:16 / 16:9 / 1:1; versões por unidade, idioma, público ou oferta | quantos masters, como parametrizar os dados |
| 15 | **Som**: trilha sintetizada (grátis, no beat) · música do cliente · trilha gerada (Suno, custa crédito) · locução · legendas para ver sem som | desenho de som e legenda |
| 16 | **Aprovação**: quem aprova, em que paradas (conceito? quadros? corte final?), se nada pode ir ao ar sem OK | onde parar e mostrar |
| 17 | **Entrega**: pasta, nomes, capas, thumbnail, plano de postagem | pasta final |

## Da resposta à decisão técnica

As respostas não ficam só registradas: elas configuram a produção. Exemplos:

| Resposta | Vira |
|---|---|
| Reels / TikTok | 9:16, 18–30 s, gancho em 1,5 s sem som, zonas seguras, capa 1:1 central, 16 Mb/s |
| TV da recepção | 16:9, 60–105 s, **loop sem fade no fim**, sem depender de som, corpo mínimo 48 px em 1080p (leitura a 3 m), endereço/telefone no fecho |
| Site (hero) | 16:9, loop curto e silencioso, poucas palavras, sem CTA dentro do vídeo |
| Apresentação/evento | 16:9, capítulos com pausa, texto maior, som opcional |
| Calmo / luxuoso | cenas de 4–5 s, `E.out5`/`E.inOut`, revelação por máscara, câmera lenta nas fotos, pad 60–80 BPM, muito respiro |
| Energético / jovem | cortes de 1–2 s no beat, 120–128 BPM, tipografia pesada, `E.overshoot` se a marca aceitar pop, cor saturada |
| Tecnológico / SaaS | telas reais em moldura, cursor e clique, dados que contam, som de interface |
| Só fotos disponíveis | modo editorial: foto em tela cheia ou em moldura, tipografia de cartaz por cima |
| Telas/gravações | modo interface: câmera virtual sobre print, anotação, fio contínuo |
| Nenhuma mídia | modo tipográfico/dados: tipografia cinética, números heróis, formas da marca |
| "Pode usar a cor de destaque como fundo" | ritmo de cor com cena de destaque a cada 2–3 cenas |
| "Manual proíbe" | ritmo por valor (claro/escuro), foto e escala, nunca pela cor proibida |

## Fechando a entrevista

Monte o `BRIEFING.md` completo, **mostre um resumo curto** (missão, formato, conceito em
uma linha, sequência de cenas com a cor de fundo de cada uma, o que foi assumido) e peça
OK antes do primeiro render longo. A partir daí, qualquer pedido de ajuste do cliente
entra primeiro no briefing e depois no código.
