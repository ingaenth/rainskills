# Direção de arte — de "correto" a "profissional"

A revisão técnica (texto cortado, zona segura, dado pessoal) garante que a peça está
**certa**. Esta página garante que ela está **boa**. Os princípios valem para qualquer
marca; os valores concretos (cores, fontes, o quanto de cor, o ritmo) saem sempre do
`BRIEFING.md` daquela marca.

> Origem: a 1ª versão de um vídeo de spa passou em toda a revisão técnica e foi reprovada
> em uma frase: *"ficou muito simples, tudo muito pequeno, e tudo com uma cor só"*. Os três
> defeitos são os mais comuns de vídeo feito em código, porque o código nasce com cara de
> página web.

## 1. Escala de cartaz, não de página

Se parece certo como página web, está pequeno para vídeo. O vídeo é visto no celular, de
passagem, às vezes na miniatura. Valores de referência num quadro de 1080 px de largura
(9:16); no 16:9 1080p para TV, some ~30%:

| Papel | Tamanho | Observação |
|---|---|---|
| Display (título de abertura, palavra-herói) | 180–280 px | uma a três palavras por linha |
| Título de seção | 150–220 px | pode sangrar/sobrepor a foto |
| Número herói (nota, preço-destaque, contador) | 300–480 px | sozinho na cena |
| Linha de item (nome de serviço/recurso) | 64–90 px | |
| Preço / número de apoio | 80–120 px | maior que o nome que ele acompanha |
| Rótulo em caixa alta | 24–30 px, espaçamento 0,2–0,35em | nunca é o único texto da cena |
| Corpo mínimo | 28 px (9:16) · 36 px (16:9) · 48 px (TV a 3 m) | |

- **Contraste de tamanho ≥ 3×** entre o maior e o menor texto da cena: é o que cria hierarquia.
- **Menos texto, maior.** Reels: até ~12 palavras legíveis por cena. Se não cabe, divida a cena.
- Tamanhos do site (h1 de 56–72 px, corpo de 16–18 px) **não** servem.

## 2. Ritmo de cor

Planeje a **sequência de fundos antes de animar** e escreva no briefing (seção 6). Uma cor
só do início ao fim vira monotonia, mesmo com boas animações.

- Alterne **valor** (escuro ↔ claro) entre cenas vizinhas.
- A cada 2–3 cenas, uma cena de **cor de destaque** da marca como fundo inteiro, se o
  manual permitir (pergunta 8 da entrevista). Numa marca dourada, um bloco dourado; numa
  marca azul, um bloco azul.
- Foto conta como cor: uma foto quente ou um céu azul quebram a paleta sem sair da marca.
- **Marca monocromática ou manual restritivo**: o ritmo vem de valor, foto, escala e
  textura, nunca de uma cor que a marca não usa.
- Mostre a sequência ao usuário como uma fileira de amostras (uma por cena) antes do render.

## 3. Um herói por cena

Cada cena tem **um** elemento dominante que se lê numa miniatura de 270 px: uma foto, uma
tela, um número gigante, uma palavra. O resto serve a ele. Lista de itens em fundo liso não
é cena, é slide.

## 4. Camadas e profundidade

De trás para frente: **fundo** (cor com degradê sutil, ou foto) → **sombreamento** (degradê
que garante contraste para o texto) → **herói** → **texto** → **textura** (grão 5–8%,
vinheta) → **logo**. Cena com uma camada só parece plana.

- **Tudo se move um pouco**: câmera lenta nas fotos (escala 1,15 → 1,02 ao longo da cena),
  deriva de 10–20 px nos títulos. Nada totalmente parado por mais de 1 s, exceto o quadro final.

## 5. Transições que parecem da marca

Escolha **2 ou 3 tipos** e varie entre eles: cortina com filete na cor de destaque, abertura
em arco ou círculo, corte seco no beat, máscara que sobe. Uma transição por cena, sempre
igual, fica mecânica; sete tipos diferentes viram vitrine de efeitos.

## 6. Modos visuais — o material decide, não o setor

| Modo | Quando | Gramática | Cuidado |
|---|---|---|---|
| **Interface** | há telas, prints, gravações do produto | moldura de vidro, câmera virtual sobre o print, cursor e clique, anotação, fio contínuo | privacidade em cada quadro; câmera em área vazia |
| **Editorial / fotográfico** | há fotos aprovadas (spa, clínica, restaurante, hotel, imóvel, moda, varejo) | foto em tela cheia com sombreamento; foto em moldura (arco, retângulo com filete); tipografia de cartaz sobre a foto; cardápio com pontilhado entre nome e preço; faixa de preços; número herói | recorte 16:9 → 9:16 perde o assunto; texto nunca sobre rosto |
| **Tipográfico / dados** | não há mídia, ou a mensagem é um número | tipografia cinética, número herói que conta, formas e ícones da marca, blocos de cor | risco de ficar "slide": capriche em escala e ritmo de cor |
| **Misto** | há um pouco de tudo | um modo por capítulo, com o mesmo sistema de tipografia e cor costurando | não misturar modos dentro da mesma cena |

Os modos são gramática, não modelo: o conceito continua nascendo do cliente ([conceito.md](conceito.md)).

## 7. Fotos

- **Redimensione** para ~2400 px no lado maior antes de usar (render mais rápido, sem perda visível).
- Foto 16:9 em tela cheia no 9:16 mostra só ~1/3 da largura e corta o assunto. Saídas:
  foto numa **caixa parcial** (60–65% da altura) com fundo sólido embaixo; versão 9:16 da
  imagem (outpaint, outra foto); ou `photo()` com **ponto focal** no assunto.
- Texto sobre foto sempre com sombreamento; confirme o contraste na folha.
- Só fotos **aprovadas** pelo cliente (entrevista, pergunta 9).

## 8. Checklist do diretor de arte

Rode na folha de contato, **olhando pequeno** (miniaturas de ~270 px), depois da revisão técnica:

1. As cenas são **diferentes entre si** em cor e composição? (miniaturas iguais = monotonia)
2. Cada quadro tem **um herói** que se lê na miniatura?
3. Os textos principais **se leem na miniatura**?
4. O primeiro segundo **pararia o scroll** sem som?
5. Parece peça **desta marca** (compare lado a lado com as referências da entrevista) ou template?
6. Há **hierarquia** (tamanhos contrastando ≥ 3×) e respiro?
7. Algo encostado em borda ou em zona coberta pela interface?
8. A sequência de fundos bate com o ritmo de cor do briefing?

**Duas ou mais respostas ruins: redesenhe a cena, não ajuste pixels.**
