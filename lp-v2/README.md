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

**Hero** em azul Blue Bolt (`#000122`) com o vídeo do modelo do Elementor
(`img/hero-video.webm`) a correr ao fundo, por baixo de um véu que garante o
contraste do texto. A tipografia é a da própria página — Archia no título,
Manrope no corpo — e só a medida e a cor foram ajustadas, que o hero centrado
e o vídeo por trás obrigam. Por baixo dos CTAs ficam os três selos: Google
Partner, Meta Business Partner e Scoring Top 5% PME 2025. A faixa deslizante
de provas que vinha da página de IA saiu, substituída por eles.

O selo da Scoring vinha num SVG de 542 KB que era, na verdade, um PNG de
1527×1527 embrulhado num `<pattern>` — o embrulho reenquadrava o desenho e
tirava-lhe nitidez. Extraí o bitmap, recortei a margem transparente e reduzi-o
para 420×382 (`img/selo-top5.png`, 123 KB). É o selo da Blue Bolt, NIF
516 751 808, com a menção "2.º ano consecutivo".

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

O funil não é imagem: é SVG desenhado em `build.py`, onde a geometria é
calculada em vez de escrita à mão. Cada fatia é uma taça: o corpo entre duas
elipses, um aro claro por cima e uma cavidade escura lá dentro. É a cavidade que
lhe dá espessura; sem ela cada fatia lia-se como um triângulo chapado.

O que faz a diferença entre parecer desenhado e parecer renderizado são três
números e uma ordem:

- **Achatamento de 0,10** (`ry = rx × 0,10`). Elipses mais abertas fazem o
  conjunto ler-se como um cone contínuo em vez de peças empilhadas.
- **Fatias de 78px** de altura. Mais altas parecem candeeiros, não taças.
- **Folga medida entre silhuetas**, não entre centros: o ponto mais baixo de uma
  fatia inclui o arco da elipse de baixo e o mais alto da seguinte inclui o da de
  cima. Somar só altura + folga colava-as.
- **Fatias desenhadas de baixo para cima**, para a sombra desfocada de cada uma
  cair sobre a de baixo, que já está lá.

O volume vem de dois gradientes sobrepostos — um vertical, em coordenadas do
desenho, que faz a fatia escurecer para o fundo, e um horizontal, que lhe
arredonda os lados — mais dois lampejos curtos no aro. A paleta vai do azul da
marca ao verde, um degrau por etapa.

As etiquetas vivem ao lado, alternando esquerda e direita, ligadas à fatia por
uma linha de chamada com um ponto em cada ponta. Abaixo dos 900px o texto dentro
do SVG ficaria minúsculo, por isso aí mostra-se só o funil e a mesma informação
passa a uma lista normal em HTML.

A animação está toda pendurada no `.revealed` que o observador da página já
punha no `.funil` — o desenho está completo desde o início e a animação é um
acréscimo, nunca a condição para se ver o funil. São três tempos: as fatias caem
de cima para baixo, uma a seguir à outra, como se o funil se montasse; as
chamadas saem da fatia para fora, primeiro a linha a desenhar-se e depois o
texto; e, já com tudo assente, um lustro percorre os aros de seis em seis
segundos — o único movimento que fica, e é discreto. Ao passar o rato numa
fatia, ela sobe e as outras recuam.

O realce ao passar o rato usa `:has()` e não `.funil-svg:hover`: a moldura do
SVG é um retângulo com muito espaço vazio, e bastaria entrar nela para o funil
todo esmorecer. Onde não houver `:has()` a regra cai e fica só o realce da
fatia. Com `prefers-reduced-motion` não há animação nenhuma — o funil aparece
feito.

Quatro armadilhas de SVG que apanhei pelo caminho. Três são da mesma família:
**em SVG a ordem de desenho é o único z-index que existe**. O aro de cada fatia
tapava a etiqueta da fatia anterior, e depois tapava-lhe o ícone — a solução é
sempre a mesma, desenhar as formas todas primeiro e o que vai por cima só no fim.
A moldura (`viewBox`) ficou curta quando aumentei a altura das fatias, cortando o
cone de baixo; passou a ser calculada a partir da geometria. E a quarta: as duas
versões do funil viviam na mesma página com os mesmos `id` de gradiente, e um
`url(#...)` duplicado resolve sempre para o primeiro — que em ecrã estreito está
escondido. O funil do telemóvel saía sem cor nenhuma. Cada versão passou a levar
o seu prefixo.

O botão secundário "Ver como funciona" saiu das duas posições onde aparecia
(hero e CTA final) e os três selos deixaram o hero: passaram a uma faixa
discreta no rodapé, a 72% de opacidade, que ganha cor ao passar o rato.

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

A página de IA não está online, por isso três ficheiros não puderam ser
recuperados e foram substituídos por equivalentes do repositório:

| Original | Substituto | Nota |
| --- | --- | --- |
| `ricardo.webp` | `img/ricardo.avif` | Retrato do Ricardo da secção de equipa |
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
