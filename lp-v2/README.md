# LP Blue Bolt Agency — layout da Blue Bolt AI

Duplicado da landing page da **Blue Bolt AI** com o design intacto — mesmas
fontes, cores, efeitos e animações — mas a vender a **Blue Bolt Agency**
(Sistema Previsível de Aquisição de Clientes). Leva a VSL a cavalo entre a
primeira e a segunda dobra.

## Duas páginas, uma para cada canal

A mesma página em dois endereços, para o tráfego e as conversões de cada
plataforma se medirem em separado:

```
public_html/
  index.html          ← a página solta, se for precisa
  meta/index.html     ← Meta Ads
  google/index.html   ← Google Ads
  img/  assets/  archia-regular.woff2  archia-regular.woff
```

**Não são duas cópias.** São geradas da mesma construção pelo `build.py`, e as
imagens, o CSS e as fontes ficam uma só vez na raiz — as duas páginas apontam
para `../img/` e `../assets/`. São 8MB que não se duplicam, e trocar uma imagem
serve as duas. Editar uma página à mão é o erro a evitar: da próxima vez que o
build correr, é reescrita.

Cada uma leva o seu `canonical`, o seu `og:url`, e empurra o canal para o
`dataLayer` **antes de o GTM arrancar** — assim a primeira visualização já o traz
e o GA4 separa os dois sem depender de a UTM ter sido posta no anúncio:

```js
dataLayer.push({canal:'meta', canal_nome:'Meta Ads'})
```

Verificado a servir a estrutura como ela fica na Hostinger: os 20 recursos que
cada página pede respondem todos 200 a partir da subpasta, a Archia carrega, não
há transbordo nem erros de consola.

**Sobre o Google:** duas páginas iguais em dois endereços são conteúdo duplicado.
Enquanto o `robots` estiver em `noindex` não há problema — e é assim que se
costuma deixar uma página de campanha paga, que não se quer a competir nos
resultados orgânicos. Se alguma vez for para indexar, uma delas tem de levar
`canonical` a apontar para a outra.

**O domínio é `sessaoestrategica.bluebolt.pt`**, num subdomínio próprio de segundo
nível. Não é o `agencia.bluebolt.pt` porque esse já tem um WordPress em cima, e
não é `lp.agencia.bluebolt.pt` porque um wildcard `*.bluebolt.pt` não chega a
terceiro nível e o certificado dava trabalho — uma página de tráfego pago com
aviso de segurança no browser queima orçamento depressa.

A verificação de domínio do Meta Business Manager abrange subdomínios: se o
`bluebolt.pt` já está verificado, este herda-o, o que importa para a Aggregated
Event Measurement em iOS. Um domínio novo teria de ser verificado de raiz.

Está numa constante só, `DOMINIO` no `build.py`; se mudar, muda-se aí e o build
trata do resto.

## No ar

**https://blueboltai.github.io/lp-blueboltagency/**

Publicada pelo GitHub Pages a partir do workflow `.github/workflows/pages.yml`:
cada push neste ramo volta a pôr a `lp-v2/` no ar. Vai só o que a página precisa
— o `build.py`, este README e o export original do Elementor ficam no
repositório e devolvem 404 no site.

Ligar as Pages exigiu um passo à mão, uma vez só (*Settings → Pages → Source:
GitHub Actions*), e vale a pena registar porquê, porque não é óbvio: nem a API
das Pages é alcançável do ambiente onde a página é construída, nem o token com
que a Action corre tem direito a criar o site (`Resource not accessible by
integration`). Não era o plano nem a visibilidade — o mesmo erro apareceu com o
repositório já público.

O repositório passou a público para as Pages funcionarem no plano gratuito.
Antes disso foi varrido todo o histórico à procura de chaves, tokens,
credenciais, caminhos internos e endereços reais: nada. O único email em todo o
export do Elementor é `exemplo@email.com`.

Verificado no site vivo: o HTML servido é byte a byte igual ao construído aqui,
e os 16 recursos que a página pede respondem todos 200.

## Ver a página

```bash
cd lp-v2 && python3 -m http.server 8000
# abrir http://localhost:8000
```

## Como foi feito

O `index.html` é **gerado**: o `build.py` parte de `source/bluebolt-ai-ads.html`
(o original, intocado) e troca só o conteúdo. Nenhuma regra de CSS do original
foi alterada — só foi acrescentado o bloco da VSL no fim do `<style>`. Cada
substituição confirma quantas ocorrências esperava encontrar, por isso uma
alteração no original que parta o script dá erro em vez de passar despercebida.

```bash
python3 build.py     # reescreve index.html a partir do original
```

Para mudar a copy, edita-se o `build.py`, não o `index.html`.

## Sem barra de menu

A barra fixa do topo foi removida — marcação e JS. Numa página de anúncios só
oferecia saídas, e além disso tapava o título do hero. O CTA que lá vivia
("Diagnóstico gratuito") já existe no hero e repete-se no fim da página. As
regras de CSS do `#nav` ficaram na folha, por não se mexer no CSS original;
não têm efeito nenhum.

## A secção do Ricardo

`#autoridade` ficou **palavra por palavra** como estava, incluindo o título
"Quem está por trás da Blue Bolt AI", o cargo "Cofundador da Blue Bolt AI" e as
duas frases sobre IA. Foi pedido assim. Se um dia quiser adaptá-la à agência,
são as únicas três menções a "Blue Bolt AI" que sobraram na página.

## Primeira e segunda dobra

**Hero** com o tratamento dos heros de SaaS modernos: uma pílula com a oferta
por cima do título, o título a desvanecer para baixo até 58% de branco, o
subtítulo em cinzento e um botão claro em degradê. O véu por cima do vídeo
fica escuro: é o contraste entre o hero escuro e o halo aceso por trás do topo
da VSL que dá o efeito — cheguei a acender o hero todo e perdeu-se. O botão só é claro aqui — no CTA final, que está sobre fundo claro, o
azul continua a ser o que salta. Por trás da VSL há um halo azul, que é o que
faz o vídeo ler-se como um ecrã aceso em vez de um retângulo colado ao fundo.

Em azul Blue Bolt (`#000122`) com o vídeo do modelo do Elementor
(`img/hero-video.webm`) a correr ao fundo, por baixo de um véu que garante o
contraste do texto.

O véu estava a tapar o vídeo quase por completo — não se percebia o que lá se
passava. Medido no browser, a luminância média por trás do título era **0,011**,
praticamente preto, e dava 17:1 contra o branco, muito acima do que é preciso.
Abriu-se até onde o contraste deixa, e quem manda não é o branco: é o azul do
título. A `#2fa1ff` precisa de 3:1, o mínimo para texto grande, o que põe o teto
da luminância em 0,075; o subtítulo, a 17px, precisa de 4,5:1 e tolera até 0,10.

| Por trás do título | Antes | Agora |
| --- | --- | --- |
| Luminância média | 0,011 | **0,024** |
| Pior pixel | 0,023 | **0,066** (teto: 0,075) |
| Contraste do azul, pior caso | 5,2:1 | **3,3:1** |
| Contraste do branco, pior caso | 14,3:1 | **9,1:1** |

Numa segunda passagem, para o vídeo ler mais, corrigiu-se um erro de desenho:
**o ponto mais claro do véu estava exatamente onde está o título**. O sítio que
precisava de mais proteção era o que tinha menos, e por isso qualquer tentativa
de acender o fotograma batia logo no limite do contraste.

O véu passou a ter três camadas com papéis separados:

1. **Uma faixa que protege o texto** — escurece só a altura em que há letras,
   esbatida nas duas pontas para não deixar aresta.
2. **A base**, que fecha no `#000122` sólido em baixo. É ela que faz o halo azul
   da VSL ler-se como um ecrã aceso.
3. **O halo radial**, agora largo e quase limpo ao centro: com a faixa a tratar
   do texto, só lhe resta fechar os cantos.

A faixa tem de mudar com o ecrã. Medido no browser: no computador as letras vão
dos 8% aos 57% da altura do véu; no telemóvel, dos 6% aos 72% — o herói é mais
estreito, o texto quebra em mais linhas e desce. Com um valor só, o subtítulo do
telemóvel caía fora da faixa e ia parar a uma zona clara do fotograma.

Resultado medido, com as zonas tiradas da posição real do texto em cada largura:

| Pior pixel por trás de… | 1440px | 390px | Mínimo exigido |
| --- | --- | --- | --- |
| Título (azul, texto grande) | **3,13:1** | **3,26:1** | 3:1 |
| Subtítulo (cinzento, 17px) | **6,26:1** | **7,03:1** | 4,5:1 |

Por cima disto há ainda dois halos, que a medição do fundo não conta: o do
título é `filter:drop-shadow` e não `text-shadow`, porque o título se pinta com
`background-clip:text` e um `text-shadow` ficaria por cima do degradê em vez de
por trás dele; o do subtítulo é `text-shadow`, que ali não há degradê recortado
para estragar. O subtítulo é o texto mais exposto do herói — cinzento, a 17px, e
sem o corpo de letra do título para aguentar. A tipografia é a da própria página — Archia no título,
Manrope no corpo — e só a medida e a cor foram ajustadas, que o hero centrado
e o vídeo por trás obrigam. A faixa deslizante de provas que vinha
da página de IA saiu; os três selos — Google Partner, Meta Business Partner e
Scoring Top 5% PME 2025 — passaram para o rodapé. O hero fica com um caminho
só: o título, a promessa e o botão.

O selo da Scoring vinha num SVG de 542 KB que era, na verdade, um PNG de
1527×1527 embrulhado num `<pattern>` — o embrulho reenquadrava o desenho e
tirava-lhe nitidez. Extraí o bitmap, recortei a margem transparente e reduzi-o
para 420×382 (`img/selo-top5.png`, 123 KB). É o selo da Blue Bolt, NIF
516 751 808, com a menção "2.º ano consecutivo".

## O que implementamos, em continuidade com "O problema"

A linha do tempo ("Como funciona") saiu — marcação, JS e a copy que lhe
pertencia. O bloco do "o que implementamos" ficou com o lugar dela.

Chegou a ficar sobre o fundo escuro do diagnóstico. Passou para o `#f6f7f9` da
secção de cima: **sem filete, sem halo e sem mudança de cor entre as duas**, o
problema e o que fazemos por ele leem-se como uma superfície só. Medida a
emenda no browser, não há nada que a marque. E a passagem para escuro passa a
acontecer uma vez, à entrada do bloco da oferta, em vez de duas — a página
alterna menos e o bloco claro ganha peso.

O halo azul do topo da secção saiu com a mudança: era para fundo escuro, e sobre
claro só sujava. O do `.ig-cta-wrap` voltou — agora que se chega ali vindo de
claro, é ele que dá ao bloco escuro uma entrada acesa, como a do hero.

### Os cartões, com as medidas da referência

O sistema já era o pedido, herdado da página de IA: invólucro exterior, cartão
interior, e um aro que acende com a aproximação do cursor — um
`repeating-conic-gradient` fixo, revelado por uma máscara cónica que segue o
ângulo do rato, em CSS e um punhado de JS, sem React nem `motion`. O que faltava
eram as medidas e o movimento:

| | Antes | Agora (referência) |
| --- | --- | --- |
| Folga do invólucro | 8px | **6px** (`p-1.5`) |
| Aro exterior | `rgba(255,255,255,.17)` | **`#cfd8e3`** |
| Borda do cartão | `rgba(255,255,255,.75)` | **`#f1f5f9`** (`slate-100`) |
| Fundo do cartão | degradê `#fbfcfe→#eef2f8` | **`#fff`**, `#f8fafc` no hover |
| Altura mínima | — | **260px**, conteúdo centrado |
| Pastilha do ícone | branca, azul no hover | **`slate-100`**, acento no hover |
| Ícone | cinzento, azul no hover | **azul de origem** (`#1183e0`) |
| Flutuação do ícone | −6px, 3,5s | **−12px + escala 1,1, 3s** |
| Título | degradê azul, 17px | **`slate-800` 20px**, acento no hover |
| Corpo | 13,5px | **15px**, `slate-600` |

O ícone está azul de origem, não só ao passar o rato — um tom abaixo do acento
da página. A `#2fa1ff` dava 2,5:1 contra a pastilha, e um desenho de traço a
1,5px precisa de 3:1 para se ler; a `#1183e0` dá 3,6:1 e continua a ser o azul
da marca. Ao passar o rato acende para o acento, com a pastilha e a borda a
acompanhar.

O aro exterior é o único valor que não é o da referência: ela usa `slate-200`
sobre página branca, e aqui a secção é `#f6f7f9` — a `slate-200` o aro
desaparecia no fundo e a nuance das duas bordas, que foi pedida, perdia-se. Um
tom acima chega.

O título deixou de estar sempre em degradê azul. Com nove cartões, nove títulos
azuis ao mesmo tempo tiravam o destaque a todos; agora o azul é o que distingue
o cartão sob o cursor. A pastilha do ícone fez o caminho inverso, de azul para
clara, pela mesma razão: com o cartão já branco, o quadrado azul puxava o olho
para o canto em vez de para o título.

A flutuação desfasa-se `.4s` por cartão, como no `motion` do original. O
`--delay` que a página já trazia serve a entrada e repete-se de seis em seis —
punha dois ícones da mesma coluna a subir ao mesmo tempo. A fase vem do
`nth-child`, um valor por cartão, e desliga-se inteira com
`prefers-reduced-motion`: nove ícones a subir e a descer sem parar são movimento
a mais para quem o pediu de menos.

Com uma altura mínima, o conteúdo tem de se centrar na vertical, senão os
cartões de uma linha de título ficam com a folga toda em baixo ao lado de um de
duas linhas que a não tem. Na referência o `justify-center` não tem exceção por
tamanho de ecrã; o alinhamento horizontal é que muda — ao centro no telemóvel,
onde o cartão ocupa a largura toda, e à esquerda a partir dos 768px.

A grelha leva `z-index:0` e o conteúdo `z-index:1`: um `::before` absoluto pinta
por cima do conteúdo em fluxo, e sem isso ficava sobre o texto.

Ao retirar a folha de estilo da linha do tempo levei à frente a dos testemunhos
e a do hero, que viviam no mesmo bloco — a secção dos testemunhos passou de 880
para 5282px de altura antes de eu dar por isso. Ficam registadas aqui porque a
folha (`SECOES_CSS`) é acrescentada num bloco só: quando se corta um pedaço, é
preciso ver o que está entre as marcas, não só as marcas.

## A medida dos títulos

Os títulos de secção vinham da página de IA cada um com a largura do bloco onde
calharam ficar — 680, 786, 980 e 1100px — e por isso nenhum começava nem acabava
no mesmo sítio. Passaram todos a partilhar uma medida só, `--medida-titulo`
(1020px), e cada um centra-se sozinho com uma margem calculada, o que lhe permite
sair de um bloco mais estreito sem precisar de saber a largura do pai. Medido no
browser: hero, problema, trajetória, o que implementamos e CTA final ocupam agora
exatamente a mesma faixa, 210→1230px.

Ficam de fora os títulos de `#guia` e `#autoridade`: ali o título é uma das duas
colunas da secção, e forçar-lhe a mesma medida partia a grelha.

## A medida dos subtítulos

O mesmo problema, um andar abaixo. Cada subtítulo tinha a largura do bloco onde
calhou ficar — **500, 560, 570, 600, 601 e 634px** — e por baixo de títulos todos
com a mesma medida isso lia-se como desalinho.

Passaram a partilhar **a medida do título** — a mesma, não uma fração dela:
`--medida-sub` é `var(--medida-titulo)`. O subtítulo começa e acaba onde o título
começa e acaba.

Foi pedido assim, sabendo o que custa: 1020px de texto a 17px são cerca de 126
caracteres por linha, mais do que o olho costuma seguir sem perder o sítio onde
ia ao mudar de linha. O que se podia fazer para o compensar está feito — a
entrelinha subiu para 1,85 em todos, que é a folga que ajuda a apanhar o início
da linha seguinte numa medida larga.

`max-width` sozinho não chegava, e é aí que estava a diferença que continuava a
ver depois da primeira tentativa. O `.hero-content` tem 836px e o `.cta-inner`
680: o subtítulo parava aí enquanto o título, que já levava a margem calculada,
chegava aos 1020. Eram **184 e 340px** de diferença. Os subtítulos passaram a
levar a mesma margem dos títulos — metade da caixa menos metade da medida — que
os deixa sair do pai sem precisar de saber a largura dele, e dá zero quando o pai
já é da medida.

Essa regra fica no fim da folha de propósito: declarada mais acima, o
`margin:2rem auto 0` do `.prob-callout` e o `margin-inline:auto` do `.prob-bio`
ganhavam-lhe por ordem de leitura. E a caixa do `.prob-head`, que tinha 980px,
subiu para a medida do título — era ela que cortava 20px de cada lado ao corpo
do texto.

Ficam de fora `#guia` e `#autoridade`, como os títulos: ali o subtítulo é uma das
duas colunas. Por isso a regra é `#hero .hero-sub` e não `.hero-sub` — a secção
do diagnóstico usa a mesma classe.

Dois corpos de letra subiram para os 17px dos restantes — o do bloco do problema
(estava a 16) e o do "o que implementamos" (a 15,8, o único abaixo dos 17 da
página). Uma medida comum só se lê como comum se o corpo de letra também for.

Medido no browser: a 1440px as caixas de título e subtítulo são as duas de
1020px em hero, problema, o que implementamos e CTA final, e o texto composto
chega aos 998–1010. A 390px todos os títulos e subtítulos da página assentam nas
mesmas arestas, 24→366px.

**Segunda dobra** passou a branco/cinza (`#f6f7f9`), com o texto e a grelha de
fundo invertidos para tom escuro. É isso que faz a VSL ler como na referência:
metade sobre o azul, metade sobre o claro.

O conteúdo dessa secção foi todo refeito à volta do **funil em ampulheta**: em
cima o texto centrado (o problema de sistema), e por baixo o funil, ladeado por
duas notas — uma para a metade que estreita até à venda, outra para a que alarga
depois dela. O funil tradicional saiu; só fica a ampulheta.

O funil é o desenho da própria Blue Bolt, feito na Canva. Cheguei a
redesenhá-lo em SVG — o link público da Canva só serve uma miniatura de
400×500 — mas o pedido foi usar o original, e o PNG de 1080×1350 chegou
depois. Já vinha com fundo transparente: só foi recortada a margem vazia e
reduzido para 703px de largura, cerca do dobro dos ~380 a que aparece, para
ficar nítido em ecrã retina. Em webp com alfa passa de 1,1MB a 83KB.

Está na terceira versão do desenho — a segunda tinha perdido o rótulo
**Indicação** na fatia de baixo, que é justamente a etapa que fecha o ciclo e dá
sentido à metade que alarga. A troca é só o ficheiro: `img/funil-canva.webp`.
Como o desenho é uma imagem e não SVG, trocá-lo não mexe em código nenhum.

Ao lado do funil ficam as seis etapas, partidas nas duas metades que a ampulheta
desenha: três que estreitam **até à venda** e três que alargam **depois dela**,
com a venda marcada entre elas. Uma lista corrida de 1 a 6 não dizia nada disso
— o desenho explicava a ampulheta e o texto ao lado não. Abaixo dos 860px as
etapas passam para baixo do desenho.

## O vão entre secções

> **A medida mudou.** Contava texto e imagens como tinta — mas a secção do
> diagnóstico passou a começar com um cartão cheio, que o olho lê como tinta a
> partir da borda e a medida não via. Media 258 onde o olho via 212. Agora conta
> também caixas com fundo ou moldura visíveis (`vao3.mjs`), e foi com essa que se
> afinou o que vem abaixo.
>
> Com a medida corrigida apareceram três vãos fora de compasso que estavam
> escondidos: o do diagnóstico (50px até ao cartão, contra 269 até ao texto da
> coluna ao lado), o da secção do Ricardo (−43) e o do CTA final (−55, que era a
> folga que a pílula removida levou consigo).
>
> Resultado medido: **amplitude de 18px a 1440, 19px a 1024 e 6px a 390.**

### As duas colunas do diagnóstico alinham pelo topo

Estavam centradas. Com o formulário do CRM — bem mais alto do que o nosso era —
isso dava uma secção apertada de um lado e larga do outro: o cartão arrancava a
**50px** da emenda com a secção clara (23px a 1024), e o texto da esquerda
afundava para **269px**. Alinhados pelo topo, os dois começam na mesma linha e é
a margem da secção que manda, como em todas as outras.



Padding igual não dá intervalos iguais. Cada secção tem folga própria por dentro
— a moldura dos cartões, a barra de rolagem dos testemunhos, a sombra do funil,
a pílula que abre cada secção. Medido de tinta a tinta (o primeiro e o último
pixel com texto ou imagem, não a caixa), os vãos iam de **148 a 297px**.

As correcções tiram a folga onde ela existe, e estão separadas por breakpoint
porque a folga interna também é outra: em grelha os cartões trazem moldura e
sombra ao lado, em coluna única empilham-se. Tentei uma fórmula só, proporcional
a `--ritmo`, e o que arrumava o desktop desarrumava o telemóvel.

Medido: **1440px** vai de 211 a 219 (amplitude 8), **390px** de 170 a 186 (16),
**768px** de 144 a 186 (42).

## O ritmo vertical

As secções vinham da página de IA cada uma com o seu número — 120, 128 e 140px
em cima e em baixo — o que dava até 290px de intervalo entre duas e deixava a
dobra meia vazia. Passaram a partilhar `--ritmo`, uma medida só que encolhe com
o ecrã (`clamp(64px, 6.6vw, 98px)`). O topo de `#quem` fica de fora: é ele que
compensa a VSL a cavalo. O diagnóstico e a secção do Ricardo levam um intervalo
mais curto entre si, por serem duas metades da mesma conversa. Medido no
browser, a página passa de ~8700px para 8098px sem perder nada.

## O botão

É o mesmo nos três sítios — herói, formulário e CTA final — gerado por uma
função só no `build.py`, para não voltarem a divergir. No formulário ocupa a
linha toda; no resto ajusta-se ao texto.

Réplica do componente *liquid metal* pedido, sem WebGL. Onde o original monta um
fragment shader do `@paper-design/shaders`, aqui há um `repeating-conic-gradient`
de quatro repetições a rodar por trás de uma pastilha preta com 2px de folga — e
é essa folga que se vê como o aro metálico. As paragens quentes e frias ao lado
do branco fazem a franja cromática que no shader vinha do `shiftRed`/`shiftBlue`,
e uma segunda camada a rodar ao contrário e mais devagar tira-lhe o ar de disco a
girar.

A rotação é conduzida por JS, não por `animation-duration`: assim a velocidade
aproxima-se da meta em vez de saltar, e o metal acelera ao passar o rato e leva um
impulso no clique — o equivalente ao `setSpeed` do original. Com
`prefers-reduced-motion` fica parado num ângulo fixo.

A pastilha é azul-marinho e não preta: sobre o azul do hero o preto lia-se como
um buraco. Continua escura que baste para o aro metálico saltar, mas pertence à
página.

O original usa `#666666` no texto. Num CTA isso dá 2,4:1 contra o preto da
pastilha, abaixo do mínimo legível; aqui o cinzento é mais claro e passa os
4,5:1, mantendo o ar discreto. É um valor só, se preferir o original.

## Telemóvel

O vídeo de fundo do herói tem 7,7MB e estava a ser descarregado no telemóvel —
era **94% do peso da página** para um fundo que o véu quase tapa. O `<source>`
saiu da marcação e a origem passa a ser posta por JS, depois do `load`, e nunca
com `prefers-reduced-motion`.

No telemóvel deixou de haver vídeo nenhum, e isso foi longe demais: ficava um
retângulo preto onde devia estar o escritório. Passou a haver uma cópia própria
— **720×405 a 24fps, sem faixa de som, 768KB** contra os 7,7MB da de secretária.
Atrás de um véu a 70% o detalhe que se perde não se vê, e o peso deixa de ser
razão para não o ter. Medido no browser, a 390px:

| | Original | Sem vídeo | Com a cópia de telemóvel |
| --- | --- | --- | --- |
| Primeira pintura | 8,20 MB | 0,47 MB | **0,49 MB** |
| Página toda percorrida | 8,34 MB | 0,81 MB | **1,58 MB** |

A primeira pintura não muda: o vídeo só começa a descarregar depois do `load`,
como no computador. E há duas portas antes disso — com `prefers-reduced-motion`
ou com o Poupar Dados ligado (ou em 2G/3G, pela Network Information API), fica o
fotograma. Pedir 768KB de enfeite a quem está a contar megabytes seria abusar.

O retrato do Ricardo (202KB) também vinha no arranque, apesar de estar muito
abaixo da dobra; passou a `loading="lazy"`.

Os alvos de toque abaixo dos 44px foram corrigidos: os ícones das redes no
rodapé (34px) e as ligações de contacto e políticas, que sendo texto corrido
tinham 15px de altura tocável. E o miúdo que ninguém lê num ecrã pequeno subiu:
os rótulos dos casos estavam a 8px, o selo do CTA e o copyright a 9px.

O formulário fazia o iOS aproximar a página. O Safari do iPhone amplia sempre
que um campo recebe foco com corpo de letra abaixo de 16px — e não volta a
afastar sozinho. Os três campos estavam a 15px; num formulário de recolha de
contactos isso é a diferença entre preencher e desistir. Passaram a 16px abaixo
dos 768px, e só aí: no computador continuam a 15px.

As sete imagens que faltavam declarar (`width`/`height`) passaram a declará-lo.
Os contentores já reservavam o espaço por `aspect-ratio`, mas sem os atributos o
browser não o sabe antes do CSS aplicar.

No rodapé, a folga que faz de cada contacto um alvo de toque de 44px empurrava o
texto para baixo e deixava o ícone a flutuar acima da linha. O ícone passou a
descer com ele: `margin-top: calc(.85rem + .15em)`.

A ampulheta ocupava **61% do ecrã**: tinha um teto de 320px fixos, o que dava
518px de altura — e os mesmos 518px num telemóvel de 360 ou num de 430. Passou a
acompanhar a largura do aparelho com teto, `min(62vw, 250px)`, o que a 390px dá
242×391 — pouco menos de metade do ecrã. Os rótulos das seis fatias continuam a
ler-se; abaixo disto começavam a apertar.

Sem transbordo horizontal a 320, 360, 390, 414, 430 e 768px. Sem `100vh`, sem
alvos de toque abaixo dos 44px, sem imagens servidas acima do dobro do tamanho
a que são mostradas, sem erros de consola e sem pedidos falhados.

## A pílula do CTA final

Saiu. "Vagas limitadas este mês" numa pastilha com aro e letra espaçada é a forma
mais gasta que uma landing page tem — e, pior, dizia o que a frase logo abaixo já
diz melhor: *"O diagnóstico é grátis, mas só aceitamos um número limitado de
novos projetos por mês."* Uma era a versão de modelo da outra. Ficou a humana.

## O rodapé

Quatro colunas, como no site: marca e redes, contactos, informações úteis e
parcerias. As moradas são as reais — `geral@bluebolt.pt`, `+351 927 135 702` com
a menção de chamada para rede móvel nacional, e as ligações para a política de
privacidade, a de cookies e o Livro de Reclamações. O logótipo é o lockup
completo (`img/bluebolt-lockup.webp`, recortado e reduzido do `LOGO-PRATA`): a
40px o símbolo sozinho era ilegível.

Falta a barra de financiamento (PRR · República Portuguesa · Financiado pela
União Europeia). O `bluebolt.pt` recusa ligações deste ambiente, por isso o
ficheiro não pôde ser descarregado. O `build.py` já a espera: basta pôr o
ficheiro em `img/barra-logos.webp` e voltar a correr o build — se não existir, a
barra simplesmente não é emitida, em vez de ficar uma imagem partida.

## A VSL

Vídeo do YouTube `v4o2YB1vPjI` — o VSL da Blue Bolt, o mesmo da LP do Elementor.
Fica a cavalo entre as duas dobras com a mesma técnica da LP de referência: o
hero ganha folga em baixo, o bloco do vídeo sobe com margem negativa em cima e
em baixo, e a secção seguinte ganha folga em cima. Medido no browser: 216px dos
438px de altura ficam sobre o hero — praticamente a meio.

Em vez de um `<iframe>` sempre carregado, o player mostra a capa e só insere o
iframe ao clicar. Fica igual à vista, mas a página não arrasta o YouTube em cada
visita — numa LP de anúncios isso conta.

## Imagens

A página de IA está em `blueboltai.online` — daí vieram o retrato do Ricardo
(`img/ricardo.webp`, reduzido de 1440×1800 para 1000px de largura, 432KB → 202KB)
e o logótipo. Faltou só um ficheiro, substituído por um equivalente do
repositório:

| Original | Substituto | Nota |
| --- | --- | --- |
| `bluebolt-logo.webp` | `img/bluebolt-logo.webp` | Logótipo Blue Bolt |
| `bluebolt-ai-brand.png` | `img/equipa.webp` | A foto do robô era da oferta de IA; entra a foto da equipa |

Do modelo do Elementor vieram ainda `img/hero-video.webm` (o vídeo de fundo),
`img/hero-poster.jpg` (o fotograma que aparece enquanto o vídeo não arranca) e
os três selos em `img/google-partner.webp`, `img/meta-partner.webp` e
`img/selo-top5.svg`.

Se enviar os ficheiros originais, é só substituí-los em `img/` com os mesmos
nomes.

## Marcação

**Google Tag Manager** `GTM-WG4ZH4LF` — o script no topo do `<head>`, o `<iframe>`
de recurso a abrir o `<body>`. O snippet do Google Analytics que a página trazia
tinha ficado com um `GA_MEASUREMENT_ID` por preencher e saiu: se for preciso GA,
é o GTM que o deve carregar. Dois carregadores a fazer o mesmo trabalho é a
receita para eventos contados a dobrar.

**Meta Pixel** `260575891666892` — `PageView` ao carregar, e `Lead` ao submeter o
formulário, com `content_name` e `content_category`. O mesmo momento empurra
`lead_enviada` para o `dataLayer`, para o GTM poder disparar o que lá estiver
configurado sem ter de adivinhar o clique.

### O `eventID`, e porque é que já existe

Cada submissão gera um identificador próprio, que vai ao mesmo tempo para o
evento do pixel, para o `dataLayer` e para um campo escondido do formulário.

Hoje não serve para nada. Serve para quando a Conversions API entrar: o mesmo
evento vai chegar ao Meta por dois caminhos — o browser e o servidor — e é por
este identificador que ele percebe que são o mesmo em vez de contar a lead duas
vezes. Sem isto, ligar a CAPI duplica tudo o que o pixel já mandou.

O cliente recolhe também os cookies `_fbp` e `_fbc`. A seguir ao email, são o que
mais melhora a correspondência do lado do Meta. Se o pixel tiver sido bloqueado o
`_fbc` não existe, mas o `fbclid` vem no endereço à mesma e é reconstruído a
partir dele — que é precisamente o caso para o qual a CAPI existe.

### O formulário é o do CRM

Era nosso, era bonito e não servia para nada: mostrava "Obrigado!" e deitava a
lead fora. Passou a ser o formulário do **Go High Level**
(`api.leadconnectorhq.com/widget/form/LsucMnYcVBLHJseC8oUQ`), e as submissões
caem no CRM.

Já vem estilizado para fundo escuro — campos a `#FFFFFF0D`, texto branco,
marcador a `#D5D5D5`, botão a `#188bf6` — que é quase o que a nossa caixa tinha,
por isso encaixa na secção sem parecer colado. E traz **campo de telefone**, que
o nosso não tinha; para a correspondência do Meta é o segundo melhor sinal
depois do email.

O título e o subtítulo ficam fora do iframe: são texto nosso, e lá dentro não os
podíamos compor nem traduzir. O `form_embed.js` ajusta a altura ao conteúdo —
sem ele o iframe fica com os 640px fixos e corta o botão em ecrãs pequenos.

Como o formulário passou a ser o único caminho de conversão da página, e vive
num domínio que não é nosso, há uma saída alternativa por baixo: se o iframe não
carregar, fica o `geral@bluebolt.pt` em vez de uma caixa vazia.

### Um formulário só, e é o novo

Ficou um formulário partilhado pelas duas páginas, não um por canal. Dois
formulários só se justificariam para dar tratamento diferente às leads de cada
canal — outro email de seguimento, outro pipeline, outro responsável. Para
*saber* de onde veio a lead já chega o campo abaixo, e duplicar traria cinco
campos, o consentimento e o CSS próprio a manter em sincronia: o mesmo problema
que evitámos ao gerar as duas páginas da mesma fonte.

O `LsucMnYcVBLHJseC8oUQ` é novo, criado para não misturar com as leads da LP
antiga. Verificado antes de trocar: mesmos campos, o CSS escuro lá, e o campo
`landingpage` já sem o valor predefinido que dava problemas.

### A origem da lead no CRM

O formulário tem um campo escondido "LandingPage" com a chave de query
`landingpage` — visto no HTML do próprio widget: `data-q="landingpage"`. Sem lhe
passar nada, o campo vai vazio e o CRM mostra o **texto de exemplo** do campo,
`Formulário [lp.blueboltagency.pt]`, que ainda por cima traz um domínio que já
não existe. Era isso que fazia todas as leads chegarem com a mesma origem.

Cada página passa a levar a sua no endereço do iframe:

| Página | Origem no CRM |
| --- | --- |
| `/meta/` | `Meta Ads` |
| `/google/` | `Google Ads` |
| `/` | (nenhuma — é a cópia sem canal) |

### As UTMs chegam sozinhas

O `form_embed.js` do GHL lê o `window.top.location.search` da página e injeta-o
no formulário (confirmado no código deles: `postMessage(["query-params", …])`).
As UTMs que estiverem no endereço do anúncio chegam ao CRM sem código nenhum
deste lado.

O `landingpage` responde "Meta ou Google". As UTMs respondem "que campanha, que
anúncio, que palavra-chave" — que é o que diz onde pôr o dinheiro. As duas coisas
não competem: uma funciona mesmo em visitas diretas, a outra dá o detalhe.

### A página de obrigado, e porque é que ela resolve o evento de Lead

O formulário do CRM **redireciona ao submeter**. Estava a mandar para
`lp.blueboltagency.pt/obrigado/` — existe e funciona, mas é outro domínio, e isso
custa duas coisas:

**O evento de Lead.** O ouvinte da página espera uma mensagem do iframe, mas a
página navega para fora antes — é uma corrida que se perde. Era esta a razão de o
evento nunca se confirmar.

**A atribuição.** Saltar de domínio faz o GA4 abrir sessão nova com origem
"referral", e perde-se a campanha que gerou a conversão.

A página `/obrigado/` resolve as duas: o `Lead` dispara no carregamento dela.

É uma cópia da que estava em `lp.blueboltagency.pt/obrigado/` — mesmo retrato de
fundo, mesmo véu (`#000000C4`, preto a 77%, tirado do CSS do Elementor deles),
mesmo texto e as mesmas três redes. O fundo veio de um PNG de 1920×1080 com
817KB; reduzido para 1600px e em webp, ficou em **33KB**.

O véu é que mudou. A original punha preto a **77%** uniforme e a foto quase
desaparecia — é uma imagem clara, não escura, e o véu é que a apagava.

Mas o véu não tem de ser igual em toda a largura: **o Ricardo está à esquerda e o
texto ao centro.** Um gradiente na horizontal deixa entrar luz onde está ele e
fecha onde estão as letras, e assim ganha-se dos dois lados. Medido no próprio
fotograma, contra um véu uniforme a 58%:

| | Uniforme 58% | Gradiente 28%→66% |
| --- | --- | --- |
| Luz na zona do Ricardo | 0,016 | **0,048** (3×) |
| Branco, pior caso no texto | 6,7:1 | **8,8:1** |

O texto fica com *mais* contraste, não menos. Num ecrã em pé isto não serve: o
`cover` corta mais de mil pixels de largura, o Ricardo passa a ocupar o
fotograma todo e o texto assenta por cima dele — sem lados para separar, volta a
ser um véu uniforme, a 62%.

O enquadramento também: com `cover`, o `center` cortava-o de fora. Está a `38%`
no computador e a `25%` no telemóvel.
Determinístico, sem depender de mensagens que o GHL não documenta. Verificado no
browser:

| | `fbq` | Evento `Lead` | `dataLayer` |
| --- | --- | --- | --- |
| Sem consentimento | não carrega | não dispara | `lead_enviada` ✓ |
| Com marketing aceite | carrega | `init` + `PageView` + `Lead` ✓ | `lead_enviada` ✓ |

O `dataLayer` recebe o evento nos dois casos — o GTM conta a conversão, e o pixel
só entra com consentimento. A escolha de cookies é lida do mesmo domínio, por
isso viaja da página de campanha para esta.

**Falta apontar o redirecionamento do formulário**, nas definições do GHL:
`Ao enviar → Redirecionar para URL` passa a
`https://sessaoestrategica.bluebolt.pt/obrigado/`.

### O ouvinte do iframe, quando já não for preciso

O formulário é um iframe de outro domínio: não se lhe pode pendurar um
`onsubmit`. O que dá é ouvir o que ele grita para a página ao submeter — e **o
formato dessa mensagem não está documentado e o script do GHL vem minificado**.
Não o adivinhei em silêncio: o ouvinte aceita várias formas conhecidas e escreve
na consola tudo o que chega do domínio deles, para se ver o que aparece de facto.
Confirmar no *Test Events* do Events Manager, com uma submissão a sério.

### A origem permitida, quando o domínio mudar

O `ORIGEM_PERMITIDA` que o servidor da CAPI usava apontava ao
`blueboltai.github.io`. Com o site em `sessaoestrategica.bluebolt.pt`, é esse o valor a
pôr — e a mesma nota vale para qualquer lista de domínios permitidos que o CRM ou
o Meta venham a pedir.

### O token da Conversions API: vai para o CRM, não para aqui

O Go High Level tem integração própria com a Conversions API do Meta. É lá que o
token deve ser colado — não num servidor à parte, que deixou de fazer sentido
assim que o formulário passou a ser deles.

E não podia estar neste repositório de qualquer maneira. É uma credencial de
servidor: quem a tiver pode escrever conversões na conta de anúncios da Blue Bolt
e estragar a otimização das campanhas. O repositório é público, e o que lá
entrasse ficava no histórico do Git para sempre, mesmo depois de apagado.

**Atenção à contagem a dobrar.** Se ligarem o pixel *dentro* do CRM, o ouvinte
desta página tem de ser desligado — senão cada lead é contada duas vezes, uma
por cada lado. As duas coisas não convivem.

## Consentimento de cookies

O Pixel do Meta em Portugal precisa de consentimento prévio, e o rodapé já
apontava para uma Política de Cookies que a página não cumpria.

| | Antes da escolha | "Rejeitar" | "Aceitar" |
| --- | --- | --- | --- |
| Meta Pixel | não carrega | não carrega | carrega |
| GTM | carrega, tudo `denied` | tudo `denied` | tudo `granted` |
| Formulário do CRM | carrega | carrega | carrega |

**O Pixel não carrega de todo antes do "sim."** Não há meio-termo: ou o
`fbevents.js` entra, ou não entra. O `<noscript>` que a página trazia saiu de
vez — disparava um pedido ao Meta para quem tem o JavaScript desligado, e a esses
não há como perguntar nada.

**O GTM carrega, mas com o Consent Mode v2 tudo em `denied` antes de o fazer.** É
o modelo da própria Google: o contentor corre, não põe cookies nem envia
identificadores enquanto não houver consentimento. Sem isto, o Google Ads deixa
de medir seja o que for no EEE.

**O formulário do CRM continua a carregar.** É o serviço que a pessoa veio
buscar, não rastreio, e bloqueá-lo era deixar a página sem o único caminho de
conversão que tem. Fica dito no texto do aviso.

Rejeitar tem o mesmo tamanho, a mesma altura e o mesmo peso visual que aceitar, e
custa um clique tanto como ele. Um "Aceitar" grande e colorido ao lado de um
"Rejeitar" a cinzento é o que a CNPD e o EDPB chamam padrão enganoso, e invalida
o consentimento que se julga ter obtido.

A escolha fica em `localStorage` por seis meses, com número de versão — se a
política mudar, sobe-se a versão e volta a perguntar-se. O rodapé tem
**Definições de cookies**, que reabre o painel com as opções como ficaram.

Verificado no browser, os quatro caminhos: sem escolha e com "Rejeitar" não sai
um único pedido ao Meta e o Consent Mode fica todo negado; com "Aceitar" o
`fbevents.js` carrega e tudo passa a `granted`; com só "Análise" ligada, o
`analytics_storage` passa a `granted` e o resto fica negado, sem Pixel.

### O bug que isto destapou

O ouvinte do formulário e a lógica do aviso estavam a ser injetados antes do
último `</script>` da página — mas o último passou a ser o
`<script src="…form_embed.js">` do CRM, **e um `<script>` com `src` ignora o que
tenha lá dentro**. O código ficava no ficheiro, visível no código-fonte, e nunca
corria. O evento de `Lead` nunca teria disparado. Agora tudo o que acrescentamos
vai numa tag própria, no fim, que tira a dúvida de vez.

## Velocidade

O PageSpeed dava **85 no telemóvel**, com CLS a 0 e TBT a 160ms — os dois já bons
— e o LCP a **3,4s**, quando bom é até 2,5.

Chegar a 100 não é objetivo. O grosso do custo não é nosso: **476KB de JavaScript
por usar e 7,6s de thread principal** vêm do formulário do CRM e do GTM, e esses
não se tiram sem tirar o formulário e a medição. O que se tirou foi o que era
nosso:

| | |
| --- | --- |
| **GSAP** | 70KB de biblioteca, **a bloquear o desenho**, para cinco fades no hero. E estavam dentro de um `if(typeof gsap!=='undefined')` — se não carregasse, a página nem animava. Passou a CSS: mesma animação, zero pedidos. |
| **Google Fonts** | A folha bloqueava. Carrega como `media="print"` e promove-se a `all` no `onload`; o `<noscript>` cobre quem não tem JS. |
| **Archia** | É a letra do título, o provável LCP, e só se descobre depois de o CSS ser lido. Um `preload` adianta-a. |
| **Formulário do CRM** | Está abaixo da dobra e carregava logo, trazendo uma aplicação inteira atrás. `loading="lazy"`. |

Pedidos a bloquear o desenho: eram três, ficou **um** — a nossa própria folha, 24KB
local.

O `.htaccess` trata dos 904KB que o relatório apontava como pedidos repetidos por
falta de validade declarada: um ano para imagens, fontes e vídeo, um mês para CSS
e JS, e **nada para o HTML**, que é ele que traz as alterações.

## Por ligar antes de publicar

- **O formulário não envia nada.** O `handleLeadSubmit` mostra a mensagem de
  obrigado e descarta os dados — é assim no original ("placeholder — sem backend
  ligado"). Numa página de anúncios isto significa perder todas as leads.
- **Os IDs de tracking são placeholders**: `GA_MEASUREMENT_ID`,
  `META_PIXEL_ID` e `GOOGLE_SITE_VERIFICATION_CODE`.
- **`robots` está em `noindex, nofollow`**, herdado do original.
- O conteúdo é servido do Google Fonts (Manrope e Inter) e do cdnjs (GSAP),
  como no original. A Archia é auto-alojada.
