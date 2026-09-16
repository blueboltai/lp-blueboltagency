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
contraste do texto. A tipografia é a da própria página — Archia no título,
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

## O que implementamos, na dobra escura

A linha do tempo ("Como funciona") saiu — marcação, JS e a copy que lhe
pertencia. O bloco do "o que implementamos" ficou com o lugar dela e passou a
escuro.

Os cartões já usavam o sistema pedido, herdado da página de IA: invólucro
exterior, cartão interior, e um aro que acende com a aproximação do cursor — um
`repeating-conic-gradient` fixo, revelado por uma máscara cónica que segue o
ângulo do rato, em CSS e um punhado de JS, sem React nem `motion`. Só mudaram de
tom, e ganharam a grelha técnica de 24px que faltava.

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
reduzido para 760px de largura, o dobro dos ~380 a que aparece, para ficar
nítido em ecrã retina. Em webp com alfa passa de 721KB a 75KB.

Ao lado do funil ficam as seis etapas numeradas, cada uma com o número na cor
da fatia correspondente. Abaixo dos 860px passam para baixo do desenho.

## O ritmo vertical

As secções vinham da página de IA cada uma com o seu número — 120, 128 e 140px
em cima e em baixo — o que dava até 290px de intervalo entre duas e deixava a
dobra meia vazia. Passaram a partilhar `--ritmo`, uma medida só que encolhe com
o ecrã (`clamp(64px, 6.6vw, 98px)`). O topo de `#quem` fica de fora: é ele que
compensa a VSL a cavalo. O diagnóstico e a secção do Ricardo levam um intervalo
mais curto entre si, por serem duas metades da mesma conversa. Medido no
browser, a página passa de ~8700px para 8098px sem perder nada.

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
