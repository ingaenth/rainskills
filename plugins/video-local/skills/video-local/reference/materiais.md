# Material — levante sozinho antes de pedir

Negócio local publica muito e organiza pouco. Quase todo o material existe em
público; pedir antes de procurar queima a paciência do cliente com coisas que você
resolveria em dez minutos.

## A ordem que rende

### 1. O site — sempre primeiro
Diz **onde fica**, e isso decide a jurisdição, o idioma e a regra. Também entrega:
nomes exatos dos serviços, horário, forma de agendar, e as frases que eles já usam
sobre si mesmos — que costumam ser melhores que as que você escreveria.

Sites em Next.js e Squarespace servem as imagens em caminhos previsíveis. Puxe o
HTML, colete os `src`, e baixe direto com User-Agent de navegador:

```bash
curl -sS -A "Mozilla/5.0" -o massagem.jpeg "https://cliente.com/services/massage-2.jpeg"
```

No Next.js, ignore o embrulho `/_next/image?url=%2F...&w=2048` e baixe o caminho
original: `/services/massage-2.jpeg` devolve o arquivo em resolução cheia.

**Logo:** procure `logo-white`, `logo.svg`, `logo@2x`. Anote a resolução — abaixo de
1024px no lado maior, o modelo deforma a letra e você vai compor em pós.

### 2. Google Meu Negócio
De onde sai **a prova que converte**: nota, número de avaliações, anos, e as fotos
*de clientes*, que mostram o lugar como ele é de verdade — não como o fotógrafo
contratado enquadrou.

### 3. Instagram — para identidade, não para prova
Serve para ver a paleta, o tom e o que já performou.

**Meça o engajamento antes de citar a rede como prova.** Seguidor não é audiência:

```
get_user_by_username → pk
get_user_engagement  → avg_likes, engagement_rate
```

Um perfil com 1.184 seguidores e média de 7 curtidas tem alcance real perto de zero.
Nesse caso a peça mostra **qualidade de serviço**, nunca popularidade — e você avisa
quem pediu, porque provavelmente ninguém mediu isso antes.

Provedores testados: `datalikers` funciona; `hikerapi` cobra por consulta e devolve
**402 quando o saldo acaba** — se der 402, troque de provedor em vez de concluir que
o perfil não existe.

### 4. Só então pergunte
Poucas coisas, específicas, e só o que não dá para levantar:

```
autorização de imagem   das pessoas que aparecem — por escrito
o que NÃO pode dizer    alegação que o jurídico ou o conselho já vetou
o serviço da peça       um só, e por quê
a oferta                se houver: valor exato, validade, condição
o link de agendamento   o mesmo que vai no anúncio
```

## Cuidado com a distância entre a foto e a realidade

As fotos reais de um negócio local costumam ser honestas e pouco cinematográficas —
luz de teto, celular, enquadramento apertado. A tentação é gerar um ambiente de
resort de luxo no lugar.

**Não faça isso.** Se a peça promete um spa que o cliente não tem, quem chega se
sente enganado e a avaliação cai — o oposto do que a peça foi contratada para fazer.

O caminho certo é **elevar a sala real**: os mesmos objetos, a mesma paleta, a mesma
marca na parede, com luz e lente melhores. É o que um diretor de fotografia faria
com aquele espaço num dia de filmagem — não outro espaço.

Monte a folha de contato e olhe antes de escrever o roteiro:

```bash
ffmpeg -i a.jpg -vf "scale=440:248:force_original_aspect_ratio=increase,crop=440:248" t_a.png
# ...e depois hstack/vstack
```

Anote da folha: paleta, materiais (mármore, madeira, linho, macramê), o emblema da
marca e onde ele aparece, o tipo de luz, e **o que destoa** — um detalhe fora de tom
numa foto é um detalhe que não deve entrar na peça.
