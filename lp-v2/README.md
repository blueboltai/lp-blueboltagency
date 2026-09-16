# LP Blue Bolt Agency — layout da Blue Bolt AI

Duplicado da landing page da **Blue Bolt AI** com o design intacto — mesmas
fontes, cores, efeitos e animações — mas a vender a **Blue Bolt Agency**
(Sistema Previsível de Aquisição de Clientes). Leva a VSL a cavalo entre a
primeira e a segunda dobra.

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

A 3,3:1 o azul passa o mínimo, mas sem folga. O título ganhou por isso um halo
escuro com a forma das letras — `filter:drop-shadow`, e não `text-shadow`,
porque o título se pinta com `background-clip:text` e um `text-shadow` ficaria
por cima do degradê em vez de por trás dele. Nas zonas escuras do fotograma não
se vê; onde as palavras a azul passam por cima da zona clara, é ele que segura
a leitura.

A rampa vertical fecha na mesma até ao `#000122` sólido em baixo: é essa base
escura que faz o halo azul da VSL ler-se como um ecrã aceso. A tipografia é a da própria página — Archia no título,
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

O vídeo de fundo do herói tem 7,7MB e estava a ser descarregado no telemóvel,
onde nem se vê — era **94% do peso da página** para um fundo que o véu quase
tapa. O `<source>` saiu da marcação e a origem passa a ser posta por JS, só em
ecrãs a partir de 861px, depois do `load`, e nunca com `prefers-reduced-motion`.
No telemóvel fica o fotograma. Medido no browser, a 390px:

| | Antes | Depois |
| --- | --- | --- |
| No arranque | 8,20 MB | **0,47 MB** |
| Página toda percorrida | 8,34 MB | **0,81 MB** |

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

Sem transbordo horizontal a 320, 360, 390, 414, 430 e 768px. Sem `100vh`, sem
alvos de toque abaixo dos 44px, sem imagens servidas acima do dobro do tamanho
a que são mostradas, sem erros de consola e sem pedidos falhados.

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

## Por ligar antes de publicar

- **O formulário não envia nada.** O `handleLeadSubmit` mostra a mensagem de
  obrigado e descarta os dados — é assim no original ("placeholder — sem backend
  ligado"). Numa página de anúncios isto significa perder todas as leads.
- **Os IDs de tracking são placeholders**: `GA_MEASUREMENT_ID`,
  `META_PIXEL_ID` e `GOOGLE_SITE_VERIFICATION_CODE`.
- **`robots` está em `noindex, nofollow`**, herdado do original.
- O conteúdo é servido do Google Fonts (Manrope e Inter) e do cdnjs (GSAP),
  como no original. A Archia é auto-alojada.
