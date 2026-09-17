#!/usr/bin/env python3
"""Transforma a LP da Blue Bolt AI na LP da Blue Bolt Agency (marketing).

Parte do HTML original da pagina de IA e troca apenas o conteudo: todo o CSS,
os efeitos, as fontes e a estrutura ficam intactos. A seccao #autoridade (quem
e o Ricardo) fica palavra por palavra como estava.

Corre sobre index.html, no sitio.

    python3 lp-v2/build.py
"""

import os
import re
import urllib.parse
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(HERE, "source", "bluebolt-ai-ads.html")   # original intocado
PAGE = os.path.join(HERE, "index.html")                        # resultado

falhas = []


def troca(html, antigo, novo, etiqueta, esperado=1):
    """Substitui e confirma que aconteceu o numero de vezes esperado."""
    n = html.count(antigo)
    if n != esperado:
        falhas.append(f"{etiqueta}: esperava {esperado} ocorrencia(s), encontrou {n}")
        return html
    return html.replace(antigo, novo)


html = open(FONTE, encoding="utf-8").read()

# ══════════════════════════════════════════════════════════════════
# BARRA DE MENU — fora
# Numa pagina de anuncios a barra so oferece saidas, e aqui tapava o titulo.
# Sai a marcacao (nav + menu movel) e sai o JS que lhe pertencia, para nao
# ficar codigo a procurar elementos que ja nao existem.
# ══════════════════════════════════════════════════════════════════

nav_markup = re.search(r"<!-- NAV -->.*?</div>\n\n", html, re.S)
if not nav_markup:
    falhas.append("barra de menu: nao encontrei o bloco do nav")
else:
    html = html.replace(nav_markup.group(0), "")

html = troca(
    html,
    """// Nav aparece ao scroll
(function(){
  var nav = document.getElementById('nav');
  var threshold = 80;
  function onScroll(){
    if(window.scrollY > threshold){
      nav.classList.add('nav-visible');
    } else {
      nav.classList.remove('nav-visible');
    }
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();

/* Nav muda para estilo claro quando fica sobreposta ao bloco de fundo claro */
(function(){
  var nav = document.getElementById('nav');
  var lightBand = document.querySelector('.light-theme');
  if(!nav || !lightBand) return;
  function checkLightBand(){
    var r = lightBand.getBoundingClientRect();
    var navH = nav.offsetHeight || 72;
    if(r.top <= navH && r.bottom >= 0){
      nav.classList.add('nav-on-light');
    } else {
      nav.classList.remove('nav-on-light');
    }
  }
  window.addEventListener('scroll', checkLightBand, {passive:true});
  window.addEventListener('resize', checkLightBand, {passive:true});
  checkLightBand();
})();

function toggleNav(){
  document.getElementById('mnav').classList.toggle('open');
  document.getElementById('burger').classList.toggle('open');
}
""",
    "",
    "JS da barra de menu",
)

# Sem barra fixa por cima, o hero nao precisa da folga que a compensava.
NAV_CSS = """
/* ══ Sem barra de menu: o hero recupera a folga que a compensava ══ */
#hero{ padding-top:4rem; }
@media(max-width:900px){ #hero{ padding-top:3rem; } }
@media(max-width:640px){ #hero{ padding-top:2.5rem; } }
"""

# CSS da primeira e da segunda dobra. Fica num bloco a parte, no fim do <style>,
# para nao se confundir com o CSS original da pagina.
SECOES_CSS = """
/* ══════════════════════════════════════════════════════════════════
   PRIMEIRA DOBRA — hero em azul Blue Bolt, sobre o video do modelo
   ══════════════════════════════════════════════════════════════════ */

.hero-wrap{ background:#000122; }

.hero-bg-video{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  z-index:1;
  pointer-events:none;
}
/* ══ Veu por cima do video ══
   O texto tem de ganhar sempre ao fotograma, mas o veu estava a tapar o
   video quase por completo: medido no browser, a luminancia media por
   tras do titulo era 0,011 — praticamente preto — e dava 17:1 contra o
   branco, muito acima do que e preciso.

   Aberto ate onde o contraste deixa. O que manda nao e o branco, e o
   azul do titulo: a #2fa1ff precisa de 3:1, que e o minimo para texto
   grande, e isso poe o tecto da luminancia por tras dele em 0,075. O
   subtitulo, a 17px, precisa de 4,5:1 e tolera ate 0,10.

   O centro do halo radial e onde o video se ve — e tambem onde ele e
   mais escuro no proprio fotograma, por isso e ai que se pode abrir
   mais. A rampa vertical fecha na mesma ate ao #000122 solido em baixo:
   e essa base escura que faz o halo azul da VSL ler-se como um ecra
   aceso. */
.hero-bg-veil{
  position:absolute;
  inset:0;
  z-index:2;
  pointer-events:none;
  /* Onde comeca e acaba a faixa que protege o texto. Medido no browser:
     no computador as letras vao dos 8% aos 57% da altura do veu, no
     telemovel dos 6% aos 72% — o hero e mais estreito, o texto quebra em
     mais linhas e desce. Com um valor so, o subtitulo do telemovel caia
     fora da faixa e ia parar a uma zona clara do fotograma. */
  --faixa-ini:  4%;
  --faixa-a:   12%;
  --faixa-b:   52%;
  --faixa-fim: 64%;
  background:
    /* 1. A faixa por tras do texto. O erro anterior era ter o ponto mais
          claro do veu exactamente onde esta o titulo: o sitio que precisa
          de mais protecao era o que tinha menos. Esta faixa escurece so a
          altura em que ha letras, esbatida nas duas pontas para nao
          deixar aresta. */
    linear-gradient(180deg,
      rgba(0,1,34,0)   var(--faixa-ini),
      rgba(0,1,34,.48) var(--faixa-a),
      rgba(0,1,34,.48) var(--faixa-b),
      rgba(0,1,34,0)   var(--faixa-fim)),
    /* 2. A base, que fecha no #000122 solido em baixo — e ela que faz o
          halo azul da VSL ler-se como um ecra aceso. */
    linear-gradient(180deg, rgba(0,1,34,.38) 0%, rgba(0,1,34,.50) 55%, #000122 96%),
    /* 3. O halo radial, agora largo e quase limpo ao centro: com a faixa
          a tratar do texto, este so tem de fechar os cantos. */
    radial-gradient(80% 64% at 50% 34%, rgba(0,1,34,.04), rgba(0,1,34,.52) 100%);
}
@media(max-width:860px){
  .hero-bg-veil{ --faixa-ini:3%; --faixa-a:10%; --faixa-b:70%; --faixa-fim:82%; }
}
/* O subtitulo e o texto mais exposto do hero: cinzento, a 17px, e sem o
   corpo de letra do titulo para aguentar. Leva halo proprio — aqui chega
   `text-shadow`, que nao ha degrade recortado que se estrague. */
.hero-sub{ text-shadow:0 1px 3px rgba(0,1,34,.75), 0 2px 14px rgba(0,1,34,.7); }
.hero-orb{ z-index:3; }
#hero{ z-index:5; }
.hero-overlay-bottom{
  z-index:4;
  height:260px;
  background:linear-gradient(to top,#000122 0%,transparent 100%);
}

/* Tipografia: a da propria pagina — Archia nos titulos, Manrope no corpo.
   So se mexe na medida e na cor, que o hero centrado e o video por tras
   obrigam a ajustar; os tipos de letra e os pesos ficam como estavam. */
/* O limite e 52 e nao 58 por causa da medida. A 58px este titulo ja nao
   cabe nos 1020px que todos os titulos partilham e quebra para tres
   linhas — o que dava o absurdo de o titulo ficar mais alto num ecra
   maior: duas linhas a 1280 e tres a 1440. Medido no browser, a linha
   mais longa passava os 1020 disponiveis. Com o hook novo — 105
   caracteres — a 48px assenta em tres linhas e mantem 1,2x sobre os
   titulos de seccao, que e a hierarquia que a pagina tem. */
.hero-h1{
  /* Um halo escuro com a forma das letras. Com o veu mais aberto, as
     palavras a azul passam por cima da zona clara do fotograma, e ai o
     pior pixel dava 3,31:1 — passa o minimo de texto grande, mas sem
     folga. O halo compra essa folga onde ela falta, e nas zonas escuras
     nao se ve. E `drop-shadow` e nao `text-shadow`: o titulo pinta-se com
     `background-clip:text`, e um text-shadow ficava por cima do degrade
     em vez de por tras dele. */
  filter:drop-shadow(0 1px 3px rgba(0,1,34,.85)) drop-shadow(0 2px 20px rgba(0,1,34,.8));
  font-size:clamp(28px,3.8vw,48px);
  line-height:1.12;
  margin-bottom:1.25rem;
}

/* ══ Medida dos titulos ══
   Os titulos de seccao vinham cada um com a largura do bloco onde calharam
   ficar: 680, 786, 980 e 1100px. Passam a partilhar a mesma medida, e cada um
   centra-se sozinho — a margem calculada deixa o titulo sair de um bloco mais
   estreito sem precisar de saber a largura do pai. Ficam de fora os titulos
   das duas seccoes em duas colunas (#guia e #autoridade): ali o titulo e a
   largura da coluna, e forcar a mesma medida partia a grelha. */
:root{
  --medida-max: 1020px;
  --medida-titulo: min(var(--medida-max), 100vw - 48px);
  /* ══ Medida dos subtitulos ══
     Cada subtitulo tinha a largura do bloco onde calhou ficar: 500, 560,
     570, 600, 601 e 634px. Lado a lado nao havia dois iguais, e por baixo
     de titulos todos com a mesma medida isso lia-se como desalinho.

     Passam a partilhar a medida do titulo — a mesma, nao uma fraccao dela:
     o subtitulo comeca e acaba onde o titulo comeca e acaba.

     Foi pedido assim, sabendo o que custa: 1020px de texto a 17px sao
     cerca de 126 caracteres por linha, mais do que o olho costuma seguir
     sem perder o sitio onde ia ao mudar de linha. O que se pode fazer para
     o compensar esta feito — a entrelinha sobe para 1,85 em todos, que e a
     folga que ajuda a apanhar o inicio da linha seguinte numa medida
     larga. */
  --medida-sub: var(--medida-titulo);
}
.hero-h1,
#quem .prob-head .quem-h2,
.traj-h2,
.band-h2,
.cta-h2{
  width:var(--medida-titulo);
  max-width:none;
  margin-inline:calc(50% - var(--medida-titulo) / 2);
  /* `balance` reparte as palavras por igual pelas linhas, o que encolhia
     cada titulo ate ao seu proprio conteudo: um ficava com 940px de texto
     e o seguinte com 581. Com `pretty` as linhas enchem a medida — todas
     acabam a rondar os mesmos 1020px — e a ultima nao fica com uma palavra
     sozinha. */
  text-wrap:pretty;
}
.hero-sub{
  font-size:clamp(15px,1.25vw,18px);
  line-height:1.6;
  color:rgba(255,255,255,.82);
  margin-bottom:2.25rem;
}
/* `max-width` e nao `width`: nas duas seccoes em duas colunas (#guia e
   #autoridade) o subtitulo vive numa coluna mais estreita do que a
   medida, e ali tem de ser a coluna a mandar. */
.hero-sub,
.prob-bio,
.prob-callout,
.band-sub,
.cta-sub{
  max-width:var(--medida-sub);
  margin-inline:auto;
}
/* Regra a parte, depois das que dao corpo a cada um, senao a entrelinha
   propria de cada seccao ganhava-lhe por ordem de leitura. */
.hero-sub,
.prob-bio,
.prob-bio p,
.band-sub,
.cta-sub{ line-height:1.85; }

/* ══ Rodape ══
   Quatro colunas: marca e redes, contactos, informacoes uteis, parcerias.
   Os selos ficam a 72% de opacidade — leem-se como nota de rodape, nao
   como um bloco de logotipos — e ganham cor ao passar o rato. */
.ft-grelha{
  display:grid;
  grid-template-columns:minmax(0,1.1fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.2fr);
  gap:clamp(2rem,4vw,3.5rem);
  align-items:start;
  padding-bottom:clamp(2.25rem,4vw,3rem);
}
/* O logotipo completo, nao o simbolo: a 40px o simbolo era ilegivel. */
.ft-logo{
  width:auto;height:76px;
  object-fit:contain;
  display:block;
  margin-bottom:16px;
}
.ft-redes{ display:flex;gap:10px;margin-top:18px; }
.ft-rede{
  width:34px;height:34px;
  display:grid;place-items:center;
  border-radius:50%;
  border:1px solid rgba(255,255,255,.12);
  color:rgba(255,255,255,.62);
  transition:color .3s ease, border-color .3s ease, background .3s ease;
}
.ft-rede svg{ width:16px;height:16px; }
.ft-rede:hover{
  color:#fff;
  border-color:rgba(47,161,255,.45);
  background:rgba(47,161,255,.12);
}

.ft-col-h{
  font-family:'Archia',sans-serif;
  font-size:15px;
  font-weight:400;
  letter-spacing:-.02em;
  color:#fff;
  margin:0 0 1.1rem;
}
.ft-lista{
  list-style:none;
  margin:0;padding:0;
  display:flex;flex-direction:column;gap:.85rem;
  font-family:'Manrope',sans-serif;
  font-size:13.5px;
  line-height:1.5;
}
.ft-lista li{ display:flex;gap:10px;align-items:flex-start; }
.ft-lista-simples li{ display:block; }
.ft-lista a{
  color:rgba(200,208,224,.68);
  text-decoration:none;
  transition:color .25s ease;
}
.ft-lista a:hover{ color:#fff; }
.ft-ico{ width:15px;height:15px;flex:none;margin-top:.15em;color:rgba(255,255,255,.4); }
.ft-nota{
  display:block;
  margin-top:.3rem;
  font-size:11px;
  color:rgba(200,208,224,.38);
}

.ft-selos{ display:flex;align-items:center;flex-wrap:wrap;gap:clamp(12px,2vw,20px); }
.ft-selo{
  height:52px;width:auto;
  object-fit:contain;
  opacity:.72;
  filter:grayscale(.3);
  transition:opacity .35s ease, filter .35s ease;
}
.ft-selo-grande{ height:68px; }
.ft-selo:hover{ opacity:1;filter:none; }

/* A barra de financiamento, quando o ficheiro existe. */
.ft-fundos{
  padding:clamp(1.75rem,3vw,2.5rem) 0;
  border-top:1px solid rgba(255,255,255,.07);
  text-align:center;
}
.ft-fundos img{
  width:100%;
  max-width:560px;
  height:auto;
  opacity:.8;
}

@media(max-width:900px){
  .ft-grelha{ grid-template-columns:repeat(2,minmax(0,1fr));gap:2.25rem; }
}
@media(max-width:560px){
  .ft-grelha{ grid-template-columns:1fr;gap:2rem; }
  .ft-selo{ height:44px; }
  .ft-selo-grande{ height:56px; }
}

/* ══════════════════════════════════════════════════════════════════
   SEGUNDA DOBRA — branco/cinza, para a VSL ficar metade sobre cada uma
   ══════════════════════════════════════════════════════════════════ */

#quem{
  --lt-inc: #12141a;
  --lt-inc-2: #4b505c;
  --lt-inc-3: #6b7078;
  background:#f6f7f9;
  color:var(--lt-inc);
}
#quem::before{
  background-image:
    linear-gradient(rgba(10,15,35,.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(10,15,35,.055) 1px, transparent 1px);
}
#quem .quem-h2 .tg{
  background:linear-gradient(to bottom,#12141a 0%,#3a3f4a 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
/* A seccao passou a ser uma coluna centrada: o texto em cima, o funil a seguir. */
#quem .quem-inner{
  display:block;
  max-width:1100px;
}
.prob-head{
  /* Era 980px. O titulo saia desta caixa pela margem calculada, o corpo
     do texto nao — e com o corpo na medida do titulo era esta caixa que
     lhe cortava 20px de cada lado. */
  max-width:var(--medida-titulo);
  margin:0 auto clamp(3.5rem,7vw,6rem);
  text-align:center;
}
/* So o corpo do texto e que fica estreito, para nao passar do comprimento
   de linha que se le bem; o titulo usa a medida comum. */
.prob-head .quem-h2{ text-wrap:pretty; }
.prob-bio{
  display:flex;
  flex-direction:column;
  gap:1.25rem;
  font-family:'Manrope',sans-serif;
  font-size:17px;
  font-weight:300;
  line-height:1.75;
  color:var(--lt-inc-2);
}
.prob-bio strong{ color:var(--lt-inc);font-weight:600; }
/* A frase de fecho fecha o texto, nao e uma caixa: ganha corpo e cor, e
   a unica marca que leva e um filete da cor da marca do lado esquerdo. */
/* Ao centro, como o resto do bloco. O filete a esquerda saiu com a
   mudanca: uma barra so de um lado com o texto ao centro lia-se como
   engano. Fica um filete curto por cima, centrado — marca a mudanca de
   voz da mesma maneira e nao puxa para um dos lados. */
.prob-callout{
  margin:2.75rem auto 0;
  padding:1.5rem 0 .1rem;
  font-family:'Manrope',sans-serif;
  font-size:19px;
  font-weight:500;
  line-height:1.6;
  letter-spacing:-.01em;
  color:var(--lt-inc);
  text-align:center;
  position:relative;
}
.prob-callout::before{
  content:'';
  position:absolute;
  top:0;
  left:50%;
  transform:translateX(-50%);
  width:56px;
  height:2px;
  background:var(--accent-light);
  border-radius:2px;
}
.prob-callout em{
  font-style:normal;
  color:var(--accent);
  font-weight:700;
}

/* ══ O funil em ampulheta ══
   O desenho e da propria Blue Bolt, feito na Canva, e entra como imagem
   com fundo transparente — por isso assenta no cinzento da seccao sem
   trazer um rectangulo branco atras. Ao lado ficam as seis etapas. */
.funil{
  display:grid;
  grid-template-columns:minmax(0,400px) minmax(0,1fr);
  gap:clamp(2rem,5vw,4.5rem);
  align-items:center;
  max-width:1000px;
  margin:0 auto;
}
.funil-fig{ margin:0; }
.funil-img{
  width:100%;
  max-width:380px;
  height:auto;
  display:block;
  margin-inline:auto;
}

/* ══ As seis etapas, ao lado do funil ══ */
.funil-passos{ display:flex;flex-direction:column;gap:.9rem; }
.passos-lista{ list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.15rem; }
.passos-meia{
  font-family:'Manrope',sans-serif;
  font-size:10px;
  font-weight:600;
  letter-spacing:.24em;
  text-transform:uppercase;
  color:var(--lt-inc-3);
  margin:0;
}
/* A venda, entre as duas metades: e o ponto que a ampulheta estreita. */
.passos-venda{
  display:flex;
  align-items:center;
  gap:.7rem;
  margin:.35rem 0;
  padding:.55rem 0;
  border-top:1px solid rgba(10,15,35,.09);
  border-bottom:1px solid rgba(10,15,35,.09);
  font-family:'Manrope',sans-serif;
  font-size:13.5px;
  font-weight:500;
  color:var(--lt-inc-2);
}
.passos-venda-marca{
  flex:none;
  width:24px;height:24px;
  display:grid;place-items:center;
  border-radius:50%;
  background:linear-gradient(135deg,#2fa1ff 0%,#005da9 100%);
  color:#fff;
  font-size:12px;
  font-weight:700;
}
.passo{ display:grid;grid-template-columns:auto 1fr;gap:1rem;align-items:start; }
.passo-n{
  font-family:'Manrope',sans-serif;
  font-size:13px;
  font-weight:700;
  letter-spacing:.06em;
  color:var(--cor);
  padding-top:.2em;
  font-variant-numeric:tabular-nums;
}
.passo-txt{
  font-family:'Manrope',sans-serif;
  font-size:15px;
  font-weight:300;
  line-height:1.65;
  color:var(--lt-inc-2);
}
.passo-txt strong{
  display:block;
  font-size:17px;
  font-weight:700;
  color:var(--lt-inc);
  margin-bottom:.15rem;
}

/* ══ Animacao ══
   Pendurada no `.revealed` que o observador ja punha no `.funil`: o funil
   sobe e as etapas entram a seguir, uma a uma. O desenho esta completo
   desde o inicio — a animacao e um acrescento, nao a condicao para se ver. */
.funil-img{ opacity:0; }
.funil.revealed .funil-img{ animation:fn-sobe .9s cubic-bezier(.16,1,.3,1) forwards; }
.passo{ opacity:0; }
.funil.revealed .passo{
  animation:fn-sobe .6s cubic-bezier(.16,1,.3,1) forwards;
  animation-delay:calc(.3s + var(--i) * .09s);
}
@keyframes fn-sobe{ from{ opacity:0;transform:translateY(16px); } to{ opacity:1;transform:none; } }

@media(prefers-reduced-motion:reduce){
  .funil.revealed .funil-img,
  .funil.revealed .passo{ animation:none; }
  .funil-img,.passo{ opacity:1; }
}

@media(max-width:860px){
  .funil{ grid-template-columns:1fr;gap:2.5rem; }
  /* A 320px fixos a ampulheta ficava com 518px de altura — 61% do ecra de
     um telemovel, e a mesma coisa num de 360 ou num de 430. Passa a
     acompanhar a largura do aparelho, com tecto: a 390px da 242x391, que
     e pouco menos de metade do ecra. Os rotulos das seis fatias continuam
     a ler-se; abaixo disto e que comecavam a apertar. */
  .funil-img{ max-width:min(62vw, 250px); }
}

/* ══ Testemunhos em video ══
   Fila que rola na horizontal em vez de grelha: sao oito, e uma grelha de
   oito ou punha cartoes minusculos ou tres filas a encher o ecra. Rolar de
   lado mantem o cartao grande e diz, so pela barra, que ha mais para ver. */
.tst-section{
  position:relative;
  padding:clamp(80px,9vw,130px) 0;
  background:#f6f7f9;
  color:#12141a;
}
.tst-inner{ max-width:1120px;margin-inline:auto;padding-inline:clamp(1.25rem,4vw,2.5rem); }
.tst-head{ text-align:center;margin-bottom:clamp(2.5rem,5vw,4rem); }
.tst-section .quem-eyebrow{ color:#005da9; }
/* Escrevi este titulo de raiz quando acrescentei a seccao, e ficou fora
   do padrao: peso 400 contra 600, -.035em de espacamento contra -.06em, e
   3,1vw contra 2,8vw — o que o fazia maior do que os outros entre os 1024
   e os 1366. Passa a ter a mesma receita dos restantes. */
.tst-h2{
  font-family:'Archia',sans-serif;
  font-size:clamp(22px,2.8vw,40px);
  font-weight:600;
  letter-spacing:-.06em;
  line-height:1.15;
  width:var(--medida-titulo);
  margin-inline:calc(50% - var(--medida-titulo) / 2);
  text-wrap:pretty;
}
.tst-h2 .tg{
  background:linear-gradient(to bottom,#12141a 0%,#3a3f4a 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.tst-h2 .ta{
  background:linear-gradient(135deg,#2fa1ff 0%,#005da9 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

.tst-row{
  display:grid;
  grid-auto-flow:column;
  grid-auto-columns:minmax(280px,1fr);
  gap:clamp(1rem,2vw,1.75rem);
  overflow-x:auto;
  scroll-snap-type:x mandatory;
  padding-bottom:1.25rem;
  scrollbar-width:thin;
  scrollbar-color:rgba(0,93,169,.35) transparent;
}
@media(min-width:900px){ .tst-row{ grid-auto-columns:minmax(0,1fr);grid-auto-flow:row;grid-template-columns:repeat(3,minmax(0,1fr));overflow:visible;row-gap:2.25rem; } }
.tst-row::-webkit-scrollbar{ height:6px; }
.tst-row::-webkit-scrollbar-thumb{ background:rgba(0,93,169,.3);border-radius:3px; }
.tst-card{ margin:0;scroll-snap-align:start; }
.tst-screen{
  position:relative;
  aspect-ratio:16/9;
  border-radius:14px;
  overflow:hidden;
  cursor:pointer;
  background:#0a0f24;
  box-shadow:0 12px 34px rgba(10,15,35,.13);
}
.tst-screen img{ width:100%;height:100%;object-fit:cover;display:block; }
.tst-screen .vsl-play{
  width:52px;height:52px;
  box-shadow:0 8px 24px rgba(0,0,0,.4),0 0 0 6px rgba(255,255,255,.1);
}
.tst-screen .vsl-play svg{ width:17px;height:17px;margin-left:3px; }
.tst-cap{
  display:flex;
  flex-direction:column;
  gap:.15rem;
  padding:.85rem .2rem 0;
}
.tst-nome{
  font-family:'Manrope',sans-serif;
  font-size:15px;font-weight:700;
  color:#12141a;
}
.tst-area{
  font-family:'Manrope',sans-serif;
  font-size:11px;font-weight:500;
  letter-spacing:.14em;text-transform:uppercase;
  color:#7b8190;
}

/* ══ A parte de cima, ate a VSL ══
   Tratamento de hero de SaaS: pilula com a oferta, titulo a desvanecer
   para baixo, subtitulo em cinzento, um botao claro e um halo por tras do
   video. O azul da marca fica no acento do titulo e no halo; o resto e
   contraste, que e o que faz o texto ganhar ao fotograma do video. */

.hero-badge{
  display:inline-flex;
  align-items:center;
  gap:.6rem;
  margin-bottom:1.75rem;
  padding:.45rem 1.05rem;
  border-radius:9999px;
  border:1px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.05);
  backdrop-filter:blur(8px);
  font-family:'Manrope',sans-serif;
  font-size:12.5px;
  font-weight:500;
  letter-spacing:.01em;
  text-transform:none;
  color:rgba(215,222,236,.82);
  white-space:nowrap;
}
.hero-badge-dot{
  width:6px;height:6px;
  border-radius:50%;
  background:#2fa1ff;
  box-shadow:0 0 0 3px rgba(47,161,255,.18);
  animation:hb-pisca 2.6s ease-in-out infinite;
}
@keyframes hb-pisca{
  0%,100%{ box-shadow:0 0 0 3px rgba(47,161,255,.18); }
  50%{ box-shadow:0 0 0 6px rgba(47,161,255,.06); }
}

/* O titulo desvanece para baixo, como nos exemplos: a ultima linha fica a
   60% de branco e o bloco ganha profundidade sem precisar de sombra. */
.hero-h1 .t1{
  background:linear-gradient(to bottom,#fff 0%,#fff 42%,rgba(255,255,255,.58) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{ color:rgba(198,208,226,.84); }
.hero-sub strong{ color:#fff;font-weight:600; }

/* Halo por tras da VSL: e o que faz o video ler-se como um ecra aceso em
   vez de um rectangulo colado ao fundo. */
.vsl-straddle{ position:relative; }
/* O halo e a luz que sai por tras do topo da VSL: e ele que faz o video
   ler-se como um ecra aceso em vez de um rectangulo colado ao fundo. Fica
   forte de proposito — o resto do hero continua escuro, e e o contraste
   entre os dois que da o efeito. */
.vsl-straddle::before{
  content:'';
  position:absolute;
  left:50%;
  top:-230px;
  /* O terceiro termo e o que evita transbordo horizontal: sem ele o halo
     empurrava a pagina 150px para o lado em ecras medios. */
  width:min(1320px, 165%, calc(100vw - 32px));
  height:500px;
  transform:translateX(-50%);
  background:
    radial-gradient(40% 46% at 50% 66%, rgba(186,226,255,.78) 0%, rgba(96,186,255,.42) 34%, rgba(47,161,255,0) 68%),
    radial-gradient(58% 56% at 50% 62%, rgba(47,161,255,.48) 0%, rgba(0,93,169,.16) 48%, rgba(0,93,169,0) 76%),
    radial-gradient(76% 70% at 50% 58%, rgba(0,93,169,.42) 0%, rgba(0,93,169,0) 74%);
  filter:blur(30px);
  pointer-events:none;
  z-index:0;
}
.vsl-shell{ position:relative;z-index:1; }

@media(max-width:860px){
  .vsl-straddle::before{ top:-150px;height:330px; }
}

@media(max-width:640px){
  .hero-badge{ font-size:11.5px;padding:.4rem .85rem;margin-bottom:1.35rem;white-space:normal; }
}
@media(prefers-reduced-motion:reduce){
  .hero-badge-dot{ animation:none; }
}

/* ══ Ritmo vertical entre seccoes ══
   Vinham com 120, 128 e 140px em cima e em baixo, cada uma com o seu
   numero, o que dava ate 290px de intervalo entre duas — a dobra ficava
   meia vazia. Passam a partilhar uma medida so, que encolhe com o ecra.
   O topo de #quem fica de fora: e ele que compensa a VSL a cavalo. */
:root{ --ritmo: clamp(64px, 6.6vw, 98px); }
#bandeiras,
.guia-section,
.auth-section,
#testemunhos,
.cta-section{
  padding-top:var(--ritmo);
  padding-bottom:var(--ritmo);
}
#quem{ padding-bottom:var(--ritmo); }
/* O diagnostico e a seccao do Ricardo sao duas metades da mesma conversa:
   entre elas o intervalo e mais curto. */
.guia-section{ padding-bottom:calc(var(--ritmo) * .55); }
.auth-section{ padding-top:calc(var(--ritmo) * .75 + 43px); }

/* ══ Correccao do vao visivel ══
   O padding igual nao da intervalos iguais: cada seccao tem folga propria
   por dentro — a moldura dos cartoes, a barra de rolagem dos testemunhos,
   a sombra do funil, a pilula que abre cada seccao. Medido de tinta a
   tinta, os vaos iam de 148 a 297px no desktop.

   As correccoes estao separadas por breakpoint porque a folga interna
   tambem e outra: em grelha, os cartoes trazem moldura e sombra ao lado e
   por baixo; em coluna unica, empilham-se e a folga muda. Uma formula so
   nao servia as duas — tentei, e o que arrumava uma desarrumava a outra.
   Os numeros sairam da medicao. */

/* A pista dos testemunhos reserva espaco para a barra de rolagem; em
   grelha, acima dos 900px, essa barra nao existe. */
@media(min-width:900px){
  .tst-row{ padding-bottom:0; }

  /* Fundo: seccoes que acabam numa grelha de cartoes ou no funil. */
  #quem{ padding-bottom:calc(var(--ritmo) - 34px); }
  #bandeiras{ padding-bottom:calc(var(--ritmo) - 26px); }
  #testemunhos{ padding-bottom:calc(var(--ritmo) - 22px); }
  /* Topo: seccoes que comecam com uma pilula ou um selo. */
  #bandeiras{ padding-top:calc(var(--ritmo) - 18px); }
  /* As duas colunas passam a alinhar pelo topo. Estavam centradas, e com o
     formulario do CRM — bem mais alto do que o nosso era — isso dava uma
     seccao apertada de um lado e larga do outro: o cartao arrancava a 50px
     da emenda com a seccao clara, e o texto da esquerda afundava para 269.
     Alinhados pelo topo, os dois comecam na mesma linha e e a margem da
     seccao que manda, como em todas as outras. */
  .guia-inner{ align-items:start; }
  .guia-section{ padding-top:calc(var(--ritmo) + 48px); }
  #testemunhos{ padding-top:calc(var(--ritmo) - 46px); }
  /* +15 e nao -40: a pilula que estava aqui em cima levava consigo a
     folga que este vao precisava. Sem ela, o titulo subiu 55px. */
  .cta-section{ padding-top:calc(var(--ritmo) + 15px); }
  /* O CTA fecha contra o rodape, que tem pouco espaco proprio em cima. */
  .cta-section{ padding-bottom:calc(var(--ritmo) + 38px); }
  .ft{ padding-top:calc(var(--ritmo) - 2px); }
}

@media(max-width:899px){
  /* Em coluna unica a folga interna e outra: os cartoes ja nao trazem
     vizinhos ao lado, a pista dos testemunhos volta a rolar, e a legenda
     do ultimo cartao deixa muito espaco por baixo. */
  #quem{ padding-bottom:calc(var(--ritmo) - 20px); }
  #bandeiras{ padding-top:calc(var(--ritmo) - 20px);padding-bottom:calc(var(--ritmo) - 6px); }
  .guia-section{ padding-top:calc(var(--ritmo) + 46px); }
  .auth-section{ padding-bottom:calc(var(--ritmo) - 15px); }
  #testemunhos{ padding-top:calc(var(--ritmo) - 14px);padding-bottom:calc(var(--ritmo) - 46px); }
  .cta-section{ padding-top:calc(var(--ritmo) + 9px);padding-bottom:calc(var(--ritmo) + 35px); }
  .ft{ padding-top:calc(var(--ritmo) + 34px); }
}

/* O diagnostico e a seccao do Ricardo continuam mais juntos que os outros
   pares, por serem duas metades da mesma conversa — mas menos do que
   estavam, que 169px contra 240 lia-se como um salto. */
.guia-section{ padding-bottom:calc(var(--ritmo) * .75); }
/* +43: medido com a foto a contar como tinta, que e o que o olho ve. */
.auth-section{ padding-top:calc(var(--ritmo) + 43px); }
@media(max-width:899px){ .guia-section{ padding-bottom:calc(var(--ritmo) * .75 + 7px); }
  .auth-section{ padding-top:calc(var(--ritmo) + 50px); } }

/* ══════════════════════════════════════════════════════════════════
   O QUE IMPLEMENTAMOS — continuacao de "O problema"
   Herda o mesmo #f6f7f9 da seccao de cima, sem filete, sem halo e sem
   mudanca de cor entre elas: o problema e o que fazemos por ele leem-se
   como uma superficie so. E a transicao para escuro passa a acontecer
   uma vez so, a entrada do bloco da oferta, em vez de duas.
   ══════════════════════════════════════════════════════════════════ */

.band-section{
  position:relative;
  background:#f6f7f9;
  color:#12141a;
  overflow:hidden;
}
/* O halo azul do topo era para o fundo escuro; sobre claro so sujava. */
.band-section::before{ display:none; }
.band-inner{ position:relative;z-index:1; }
/* O halo do .ig-cta-wrap volta: agora que vem de claro, e ele que da ao
   bloco escuro uma entrada acesa, como a do hero. O filete continua
   fora — com a mudanca de fundo, a emenda ja se le sozinha. */
.ig-cta-wrap{ border-top:0; }

/* ══ Cabecalho, sobre claro, igual ao de "O problema" ══ */
.band-eyebrow{
  color:#0b74d4;
  border-color:rgba(11,116,212,.22);
  background:rgba(11,116,212,.06);
}
.band-tg{
  background:linear-gradient(to bottom,#12141a 0%,#3a3f4a 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
/* 15,8px era o unico subtitulo abaixo dos 17 da pagina; a medida comum
   so se le como comum se o corpo de letra tambem for. */
.band-sub{ color:#4b505c;font-size:17px;line-height:1.75; }

/* ══ Cartoes, com as medidas da referencia ══ */
/* As duas bordas: um aro exterior (slate-200), uma folga de 6px onde se
   ve o fundo da seccao, e a borda do cartao (slate-100). E a folga que
   se le como segunda borda — e tambem onde o brilho corre. */
.band-card{
  padding:6px;
  /* A referencia usa slate-200 sobre pagina branca. Aqui a seccao e
     #f6f7f9: a slate-200 o aro exterior desaparecia no fundo e a nuance
     das duas bordas perdia-se. Um tom acima chega. */
  border-color:#cfd8e3;
  background:transparent;
}
.band-card:hover{ border-color:rgba(47,161,255,.32); }
.band-card-inner{
  min-height:260px;
  padding:32px;
  /* Com uma altura minima, o conteudo tem de se centrar na vertical: os
     cartoes de uma linha de titulo ficavam com a folga toda em baixo, ao
     lado de um de duas linhas que a nao tinha. Na referencia o
     `justify-center` nao tem excecao por tamanho de ecra — vale sempre.
     Ja o alinhamento horizontal muda: ao centro no telemovel, onde o
     cartao ocupa a largura toda, e a esquerda a partir dos 768. */
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  text-align:center;
  border-color:#f1f5f9;
  background:#fff;
  /* shadow-xl da referencia. Sobre claro a sombra tem de ser curta e
     baixa: a que servia sobre escuro (48px de desfoque a 40%) aqui
     lia-se como uma mancha cinzenta a volta do cartao. */
  box-shadow:0 20px 25px -5px rgba(15,23,42,.08), 0 8px 10px -6px rgba(15,23,42,.06);
  transition:background .5s ease, box-shadow .5s ease, transform .4s cubic-bezier(.16,1,.3,1);
}
.band-card:hover .band-card-inner{
  background:#f8fafc;
  box-shadow:0 24px 34px -8px rgba(15,23,42,.12), 0 10px 14px -8px rgba(15,23,42,.08);
  transform:translateY(-3px);
}
/* Grelha tecnica de fundo, a 24px. Leva z-index:0 e o conteudo z-index:1:
   um ::before absoluto pinta por cima do conteudo em fluxo, e a grelha
   ficava por cima do texto. */
.band-card-inner::before{
  content:'';
  position:absolute;
  inset:0;
  z-index:0;
  pointer-events:none;
  background-image:
    linear-gradient(to right, rgba(10,15,35,.032) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(10,15,35,.032) 1px, transparent 1px);
  background-size:26px 26px;
  /* A grelha desvanece nos quatro lados em vez de bater na borda do
     cartao. Sao duas mascaras — uma na horizontal, outra na vertical —
     cruzadas: cada uma apaga um par de lados, e a interseccao apaga os
     quatro. Uma radial so fecharia os cantos, deixando o meio dos lados
     a chegar a borda.

     As paragens intermedias sao o que torna o desvanecimento gradual em
     vez de um patamar cheio no meio: a grelha so chega a sua densidade
     maxima — que ja e pouca — no centro do cartao, e desce desde ai. */
  -webkit-mask-image:
    linear-gradient(to right, transparent 0, rgba(0,0,0,.18) 20%, rgba(0,0,0,.6) 38%, #000 50%, rgba(0,0,0,.6) 62%, rgba(0,0,0,.18) 80%, transparent 100%),
    linear-gradient(to bottom, transparent 0, rgba(0,0,0,.18) 18%, rgba(0,0,0,.6) 36%, #000 50%, rgba(0,0,0,.6) 64%, rgba(0,0,0,.18) 82%, transparent 100%);
  -webkit-mask-composite:source-in;
  mask-image:
    linear-gradient(to right, transparent 0, rgba(0,0,0,.18) 20%, rgba(0,0,0,.6) 38%, #000 50%, rgba(0,0,0,.6) 62%, rgba(0,0,0,.18) 80%, transparent 100%),
    linear-gradient(to bottom, transparent 0, rgba(0,0,0,.18) 18%, rgba(0,0,0,.6) 36%, #000 50%, rgba(0,0,0,.6) 64%, rgba(0,0,0,.18) 82%, transparent 100%);
  mask-composite:intersect;
}
.band-icon-wrap,
.band-card-title,
.band-card-desc{ position:relative;z-index:1; }

/* ══ Pastilha do icone ══
   A referencia da-lhe 48px, cantos de 12px, fundo slate-100 e borda
   slate-200, e ao passar o rato no cartao troca a cor do icone e a da
   borda pelo acento. Fica a pastilha clara em vez do degrade azul que
   a pagina original punha: com o cartao ja branco, o quadrado azul
   puxava o olho para o canto em vez de para o titulo. */
.band-icon-wrap{
  border-radius:12px;
  background:#f1f5f9;
  border-color:#e2e8f0;
  /* Azul de origem, nao so ao passar o rato. Um tom abaixo do acento da
     pagina: a #2fa1ff o icone dava 2,5:1 contra a pastilha, e um desenho
     de traco a 1,5px precisa de 3:1 para se ler. A #1183e0 da 3,6:1 e
     continua a ser o azul da marca. */
  color:#1183e0;
  box-shadow:0 1px 2px rgba(15,23,42,.05);
  transition:color .5s ease, border-color .5s ease, background .5s ease;
}
/* Ao passar o rato acende para o acento, como o titulo — a pastilha e a
   borda acompanham, e e o conjunto que muda, nao so o icone. */
.band-card:hover .band-icon-wrap{
  background:#f1f7ff;
  border-color:rgba(47,161,255,.3);
  color:#2fa1ff;
}
.band-icon-wrap svg{ width:24px;height:24px;stroke-width:1.5; }

/* ══ A flutuacao dos icones ══
   O motion do original anima y de 0 a -12 e a escala de 1 a 1.1 em 3s,
   com um desfasamento de .4s por cartao. O --delay que a pagina ja
   trazia serve a entrada, nao isto: repete-se de seis em seis e punha
   dois icones da mesma coluna a subir ao mesmo tempo. A fase vem do
   nth-child, um por cartao. */
@keyframes bandFloat{
  0%,100%{ transform:translateY(0) scale(1); }
  50%    { transform:translateY(-12px) scale(1.1); }
}
.band-icon-wrap{
  animation:bandFloat 3s ease-in-out infinite;
  animation-delay:calc(var(--fase,0) * .4s);
}
.band-card:nth-child(1) .band-icon-wrap{ --fase:0; }
.band-card:nth-child(2) .band-icon-wrap{ --fase:1; }
.band-card:nth-child(3) .band-icon-wrap{ --fase:2; }
.band-card:nth-child(4) .band-icon-wrap{ --fase:3; }
.band-card:nth-child(5) .band-icon-wrap{ --fase:4; }
.band-card:nth-child(6) .band-icon-wrap{ --fase:5; }
.band-card:nth-child(7) .band-icon-wrap{ --fase:6; }
.band-card:nth-child(8) .band-icon-wrap{ --fase:7; }
.band-card:nth-child(9) .band-icon-wrap{ --fase:8; }
/* Nove icones a subir e descer sem parar sao movimento a mais para quem
   o pediu de menos. */
@media(prefers-reduced-motion:reduce){
  .band-icon-wrap{ animation:none; }
}

/* ══ Textos ══
   A referencia poe o titulo a slate-800 e so o acende ao passar o rato.
   Estava sempre em degrade azul: com nove cartoes, nove titulos azuis
   de uma vez tiravam o destaque a todos. */
.band-card-title{
  font-size:20px;
  font-weight:700;
  margin-bottom:12px;
  background:none;
  -webkit-text-fill-color:currentColor;
  color:#1e293b;
  transition:color .3s ease;
}
.band-card:hover .band-card-title{ color:#2fa1ff; }
.band-card-desc{
  font-size:15px;
  font-weight:300;
  line-height:1.625;
  color:#475569;
  transition:color .3s ease;
}
.band-card:hover .band-card-desc{ color:#334155; }
@media(min-width:768px){
  .band-card-inner{ align-items:flex-start;text-align:left; }
}

/* ══ Botao liquid metal ══
   O componente pedido monta um fragment shader; aqui o aro e um
   conic-gradient de quatro repeticoes a rodar por tras de uma pastilha
   preta com 2px de folga — e a folga que se ve como metal. As paragens
   quentes e frias ao lado do branco fazem a franja cromatica que no
   shader vinha do shiftRed/shiftBlue. A rotacao e conduzida por JS, para
   a velocidade poder subir ao passar o rato e dar um impulso no clique,
   como o setSpeed do original. */
.lm-btn{
  position:relative;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  height:48px;
  padding:0 28px;
  border-radius:100px;
  isolation:isolate;
  text-decoration:none;
  cursor:pointer;
  box-shadow:
    0 0 0 1px rgba(0,0,0,.3),
    0 36px 14px rgba(0,0,0,.02),
    0 20px 12px rgba(0,0,0,.08),
    0 9px 9px rgba(0,0,0,.12),
    0 2px 5px rgba(0,0,0,.15);
  transition:box-shadow .15s cubic-bezier(.4,0,.2,1), transform .15s cubic-bezier(.4,0,.2,1);
}
.lm-btn:hover{
  box-shadow:
    0 0 0 1px rgba(0,0,0,.4),
    0 12px 6px rgba(0,0,0,.05),
    0 8px 5px rgba(0,0,0,.1),
    0 4px 4px rgba(0,0,0,.15),
    0 1px 2px rgba(0,0,0,.2);
}
.lm-btn:active{ transform:translateY(1px) scale(.985); }

.lm-aro{
  position:absolute;
  inset:0;
  border-radius:inherit;
  overflow:hidden;
  z-index:0;
}
.lm-aro::before,
.lm-aro::after{
  content:'';
  position:absolute;
  left:50%;
  top:50%;
  width:260%;
  aspect-ratio:1;
  transform:translate(-50%,-50%) rotate(calc(var(--lm-a,0) * 1deg));
}
.lm-aro::before{
  background:repeating-conic-gradient(from 45deg,
    #0d0d0d 0deg,
    #3d3d3d 9deg,
    #ffd4c2 16deg,
    #ffffff 21deg,
    #c9ddff 26deg,
    #6e6e6e 34deg,
    #141414 56deg,
    #0d0d0d 90deg);
}
/* A segunda camada roda ao contrario e mais devagar: e a sobreposicao
   das duas que tira o ar de disco a girar e da o aspeto liquido. */
.lm-aro::after{
  opacity:.45;
  mix-blend-mode:screen;
  transform:translate(-50%,-50%) rotate(calc(var(--lm-a,0) * -.55deg));
  background:repeating-conic-gradient(from 200deg,
    transparent 0deg,
    rgba(255,255,255,.5) 24deg,
    rgba(180,205,255,.35) 32deg,
    transparent 60deg,
    transparent 120deg);
}

/* O original e preto, e sobre o azul do hero lia-se como um buraco. A
   pastilha passa a cinzento claro: num CTA sobre fundo escuro e o claro
   que salta, e o aro metalico continua a ler-se por cima dele. */
.lm-face{
  position:absolute;
  inset:2px;
  border-radius:100px;
  z-index:1;
  background:linear-gradient(180deg,#f4f6fa 0%,#dfe4ec 52%,#eef1f6 100%);
  transition:box-shadow .15s cubic-bezier(.4,0,.2,1);
}
.lm-btn:active .lm-face{
  box-shadow:inset 0 2px 4px rgba(10,20,45,.28), inset 0 1px 2px rgba(10,20,45,.2);
}
/* Sobre o claro a onda do clique tem de ser escura para se ver. */
.lm-onda{ background:radial-gradient(circle, rgba(10,20,45,.3) 0%, rgba(10,20,45,0) 70%); }

.lm-conteudo{
  position:relative;
  z-index:2;
  display:inline-flex;
  align-items:center;
  gap:9px;
  /* Texto escuro sobre a pastilha clara: 13:1, bem acima do minimo. */
  color:#0d1730;
  transition:color .35s ease;
}
.lm-btn:hover .lm-conteudo{ color:#000; }
.lm-label{
  font-family:'Manrope',sans-serif;
  font-size:14px;
  font-weight:600;
  letter-spacing:-.005em;
  white-space:nowrap;
}

/* Ondas do clique, como no original. */
.lm-onda{
  position:absolute;
  z-index:3;
  width:20px;height:20px;
  border-radius:50%;
  pointer-events:none;
  animation:lm-onda .6s ease-out forwards;
}
@keyframes lm-onda{
  from{ transform:translate(-50%,-50%) scale(0);opacity:.6; }
  to{ transform:translate(-50%,-50%) scale(4);opacity:0; }
}

/* No formulario o botao nao vai a largura toda: a 518px a pastilha
   estica-se e o aro metalico perde o desenho. Fica a medida do texto,
   centrado, como nos outros dois sitios. */
.lm-btn-bloco{ align-self:center;height:52px;margin:.5rem auto 0; }

@media(max-width:640px){
  .lm-btn{ height:46px;padding:0 22px; }
  .lm-btn-bloco{ height:50px;width:100%; }
  .lm-label{ font-size:13px; }
}

/* ══ Telemovel ══
   O que a auditoria apanhou: alvos de toque abaixo dos 44px e miudo a 8 e
   9px, que ninguem le num ecra pequeno. */
@media(max-width:768px){
  .ft-rede{ width:44px;height:44px; }
  .ft-redes{ gap:12px; }
  /* As ligacoes do rodape sao texto corrido: sem folga vertical ficam com
     15px de altura tocavel. */
  .ft-lista a{ display:inline-block;padding:.85rem 0;line-height:1.3; }
  .ft-lista{ gap:.2rem; }
  /* A folga que faz do link um alvo de toque empurra o texto para baixo;
     o icone tem de descer com ele, senao fica a flutuar acima da linha. */
  .ft-ico{ margin-top:calc(.85rem + .15em); }

  /* O iOS faz zoom a pagina ao focar um campo com corpo abaixo de 16px, e
     nao volta a sair. Num formulario de leads isso e a diferenca entre
     preencher e desistir. */
  .lead-input{ font-size:16px; }

  /* O cartao tinha 40px de folga de cada lado: num ecra de 390 sobravam
     260px para o formulario do CRM, e ele respondia com campos estreitos
     e um botao quase quadrado. A 18px sobram 306. */
  .lead-form{ padding:18px; }

  /* A saida alternativa do formulario e texto corrido: sem folga ficava
     com 14px de altura tocavel. */
  .lead-fine a{ display:inline-block;padding:.85rem 0; }

  .auth-case-label{ font-size:10px;letter-spacing:.12em; }
  .expert-role{ font-size:11px; }
  .cta-badge{ font-size:10.5px; }
  .ft-copy{ font-size:11px; }
  .lead-fine{ font-size:12.5px; }
  .tst-area{ font-size:11.5px; }
}

@media(max-width:640px){
  .hero-h1{ font-size:clamp(26px,7.6vw,36px); }
  .hero-sub{ font-size:14.5px; }
}
@media(prefers-reduced-motion:reduce){
  .hero-bg-video{ display:none; }
}

/* ══════════════════════════════════════════════════════════════════
   OS SUBTITULOS SAEM DA CAIXA, COMO OS TITULOS
   `max-width` sozinho nao chegava: o .hero-content tem 836px e o
   .cta-inner 680, e o subtitulo parava ai enquanto o titulo, que ja
   levava esta margem calculada, chegava aos 1020. Ficavam 184 e 340px de
   diferenca — exactamente o que se via.

   A margem e a mesma receita dos titulos: metade da caixa menos metade da
   medida, o que deixa o elemento sair do pai sem precisar de saber a
   largura dele. Quando o pai ja e da medida, da zero e nao faz nada.

   Fica no fim da folha de proposito. Declarada mais acima, o
   `margin:2rem auto 0` do .prob-callout e o `margin-inline:auto` do
   .prob-bio ganhavam-lhe por ordem de leitura.

   O #guia e o #autoridade ficam de fora, como os titulos: ali o subtitulo
   e uma das duas colunas, e tem de ser a coluna a mandar. Por isso e
   `#hero .hero-sub` e nao `.hero-sub` — a seccao do diagnostico usa a
   mesma classe. */
#hero .hero-sub,
.prob-head .prob-bio,
.prob-head .prob-callout,
.band-sub,
.cta-sub{
  width:var(--medida-sub);
  max-width:none;
  margin-inline:calc(50% - var(--medida-sub) / 2);
}
"""


# ══════════════════════════════════════════════════════════════════
# O FUNIL EM AMPULHETA
# E o desenho da propria Blue Bolt, feito na Canva. Chegou como imagem e
# como imagem fica — cheguei a redesenha-lo em SVG, mas o pedido foi usar
# o original. O PNG de 1080x1350 ja vinha com fundo transparente: so foi
# recortada a margem vazia. Fica a 703px de largura — acima do dobro dos
# ~340 a que aparece, o que chega para ecra retina. Em webp com alfa passa
# de 770KB a 73KB.
# ══════════════════════════════════════════════════════════════════

# (nome, descricao, cor da fatia no desenho)
FATIAS = [
    ("Atração", "Campanhas em Meta e Google Ads que trazem o perfil certo, não só volume.", "#1B7BE8"),
    ("Oportunidade", "Fluxos de email e WhatsApp que aquecem a lead antes do contacto comercial.", "#0E86F0"),
    ("Conversão", "Scripts, playbook e CRM para não se perder nenhuma oportunidade pelo caminho.", "#12A3DE"),
    ("Retenção", "Acompanhamento depois da venda, para o cliente voltar a comprar.", "#1AB9D6"),
    ("Fidelização", "Deixa de comparar preços e passa a escolher-nos por hábito.", "#0E6FD6"),
    ("Indicação", "Cada cliente satisfeito traz o próximo, sem custo de aquisição.", "#0E3E90"),
]

_ARIA = ("Funil em ampulheta da Blue Bolt: atração, oportunidade e conversão estreitam até à "
         "venda; retenção, fidelização e indicação alargam depois dela")


def funil_img():
    return (f'<img class="funil-img" src="img/funil-canva.webp" width="703" height="1137" '
            f'alt="{_ARIA}" loading="lazy" decoding="async">')


def funil_passos():
    """As seis etapas ao lado do funil, partidas nas duas metades.

    A ampulheta diz que tres etapas estreitam ate a venda e tres alargam
    depois dela; a lista corrida de 1 a 6 nao dizia nada disso. Com as duas
    metades e a venda marcada ao meio, o texto passa a explicar o desenho.
    """
    def bloco(inicio, fim):
        itens = []
        for i in range(inicio, fim):
            nome, desc, cor = FATIAS[i]
            itens.append(
                f'<li class="passo" style="--i:{i};--cor:{cor}">'
                f'<span class="passo-n">{i + 1:02d}</span>'
                f'<span class="passo-txt"><strong>{nome}</strong>{desc}</span>'
                f"</li>"
            )
        return "".join(itens)

    return (
        '<div class="funil-passos">'
        '<p class="passos-meia">Até à venda</p>'
        f'<ol class="passos-lista">{bloco(0, 3)}</ol>'
        '<p class="passos-venda"><span class="passos-venda-marca">€</span>'
        '<span>A venda. É aqui que a maioria das agências pára.</span></p>'
        '<p class="passos-meia">Depois da venda</p>'
        f'<ol class="passos-lista" start="4">{bloco(3, 6)}</ol>'
        "</div>"
    )

# A segunda dobra inteira. O funil e feito de bandas com clip-path, nao de
# imagem: fica nitido em qualquer ecra, adapta-se e le-se por um leitor de ecra.
SEGUNDA_DOBRA = """<section id="quem">
  <div class="quem-inner">

    <div class="prob-head">
      <div class="quem-eyebrow" data-reveal="fade">O problema</div>
      <h2 class="quem-h2" data-reveal data-delay="1">
        <span class="tg">Se já tem anúncios e está à procura de uma agência, é porque </span><span class="ta">algo não está a funcionar como devia.</span>
      </h2>
      <div class="prob-bio" data-reveal data-delay="2">
        <p>A maior parte das empresas de serviços que nos procura tem <strong>problema de sistema.</strong> Anúncios sem funil não convertem. Funil sem nutrição não aquece. Leads sem processo comercial não fecham.</p>
        <p>Cada etapa que falha é faturação que fica pelo caminho.</p>
      </div>
      <p class="prob-callout" data-reveal data-delay="3">Para a maioria das agências, atrair leads é o objetivo final. <em>Para nós, é o ponto de partida.</em></p>
    </div>

    <div class="funil" data-reveal="fade">
      <figure class="funil-fig">""" + funil_img() + """</figure>
      """ + funil_passos() + """
    </div>

  </div>
</section>"""

# ══════════════════════════════════════════════════════════════════
# A LINHA DO TEMPO SAI
# O "o que implementamos" passa a ocupar a dobra escura que era dela.
# Sai a marcacao, o JS que a animava e a folha que lhe pertencia.
# ══════════════════════════════════════════════════════════════════

seccao = re.search(r'<section id="trajetoria">.*?</section>\n', html, re.S)
if not seccao:
    falhas.append("linha do tempo: nao encontrei a seccao")
else:
    html = html.replace(seccao.group(0), "")

js = re.search(r"/\* Timeline scroll-driven \*/\n\(function\(\)\{.*?\n\}\)\(\);\n", html, re.S)
if not js:
    falhas.append("linha do tempo: nao encontrei o JS")
else:
    html = html.replace(js.group(0), "")

# ══════════════════════════════════════════════════════════════════
# A PILULA DO CTA FINAL
# "Vagas limitadas este mes" numa pastilha com aro e letra espacada e a
# forma mais gasta que uma landing page tem. E, pior, diz o que a frase
# de baixo ja diz melhor: "o diagnostico e gratis, mas so aceitamos um
# numero limitado de novos projetos por mes". Uma e a versao humana da
# outra. Fica a humana.
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<div class="cta-badge" data-reveal="fade">Vagas limitadas este mês</div>\n',
    "",
    "pilula do CTA final",
)


# ══════════════════════════════════════════════════════════════════
# TESTEMUNHOS EM VIDEO
# Os videos sao os da propria Blue Bolt, recuperados da LP do Elementor.
# Cada cartao mostra so a capa; o iframe do YouTube so entra ao clicar,
# senao a pagina arrastava nove players de uma vez.
# ══════════════════════════════════════════════════════════════════

# O nome de cada pessoa vem gravado na propria capa: a legenda repete-o
# para quem le a pagina de cima a baixo sem parar em cada fotograma.
TESTEMUNHOS = [
    ("8QXWiBi7Z8I", "capa-auto-avenida-scaled-1.webp", "Luís Novais", "Auto Avenida", 402),
    ("qbhpgXOUC9I", "capa-infante-scaled-1.webp", "Dr. Marco Infante da Câmara", "Infante da Câmara", 401),
    ("LbNL0YDUDdI", "capa-apametal-scaled-1.webp", "Rita Rodrigues", "Apametal", 386),
    ("kl3K2hbLHmk", "capa-foot-draft-scaled-1.webp", "Bruno Pinto", "Foot Draft", 413),
    ("pl0ah13B-CY", "capa-carmen-scaled-1.webp", "Carmen Ferreira", "Enfermagem", 386),
    ("8XSuQEaG17U", "capa-mecia-scaled-1.webp", "Mécia Correia", "Marca pessoal", 404),
]
# Ficam seis, em duas filas de tres. Os outros dois testemunhos que temos —
# Natália Teixeira e Sara Moreira — sao ambos de marca pessoal, que ja esta
# representada; sairam para a fila nao ficar a dois.

_cartoes = "".join(
    f'<figure class="tst-card">'
    f'<div class="vsl-screen tst-screen" data-video="{vid}" role="button" tabindex="0" '
    f'aria-label="Ver o testemunho de {nome}">'
    f'<img src="img/testemunhos/{capa}" width="720" height="{alt_px}" alt="" '
    f'decoding="async" fetchpriority="low">'
    f'<span class="vsl-play" aria-hidden="true">'
    f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'
    f"</div>"
    f'<figcaption class="tst-cap"><span class="tst-nome">{nome}</span>'
    f'<span class="tst-area">{area}</span></figcaption>'
    f"</figure>"
    for vid, capa, nome, area, alt_px in TESTEMUNHOS
)

TESTEMUNHOS_HTML = """<section id="testemunhos" class="tst-section">
  <div class="tst-inner">
    <div class="tst-head">
      <div class="quem-eyebrow" data-reveal="fade">Resultados</div>
      <h2 class="tst-h2" data-reveal data-delay="1">
        <span class="tg">Em palavras deles, </span><span class="ta">não nossas.</span>
      </h2>
    </div>
    <div class="tst-row" data-reveal="fade">""" + _cartoes + """</div>
  </div>
</section>

"""

# ══════════════════════════════════════════════════════════════════
# HEAD — SEO, titulo, partilha
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    "<title>Blue Bolt AI | A sua Equipa de IA a trabalhar 24/7 na sua empresa</title>",
    "<title>Blue Bolt Agency | Sistema Previsível de Aquisição de Clientes</title>",
    "title",
)
html = troca(
    html,
    'content="Construímos e instalamos agentes de IA à medida do seu negócio: atendimento, vendas e tarefas repetitivas, sem contratar mais ninguém. Peça uma análise gratuita.">',
    'content="Construímos o sistema que transforma anúncios em clientes: atração, nutrição e processo comercial, com resultados medidos todos os meses. Diagnóstico gratuito de 30 minutos.">',
    "meta description (também og:description)",
    esperado=2,
)
html = troca(
    html,
    'content="agentes de IA, automação de processos, inteligência artificial para empresas, IA para vendas, atendimento com IA, automação empresarial, Blue Bolt, Blue Bolt AI">',
    'content="agência de marketing digital, geração de leads, tráfego pago, Google Ads, Meta Ads, funil de vendas, aquisição de clientes, Blue Bolt, Blue Bolt Agency">',
    "meta keywords",
)
html = troca(html, 'content="Blue Bolt AI">', 'content="Blue Bolt Agency">', "meta author e og:site_name", esperado=2)
html = troca(
    html,
    'content="Agentes de IA e automações à medida do seu negócio, feitos e instalados por nós. Peça a sua análise de IA gratuita.">',
    'content="O sistema completo que transforma anúncios em clientes: atração, nutrição e processo comercial. Diagnóstico gratuito de 30 minutos.">',
    "twitter:description",
)
html = troca(
    html,
    'content="A sua Equipa de IA a trabalhar 24/7 na sua empresa | Blue Bolt AI">',
    'content="Aumente a sua faturação com um sistema previsível | Blue Bolt Agency">',
    "og:title e twitter:title",
    esperado=2,
)

# ══════════════════════════════════════════════════════════════════
# CAMINHOS DOS FICHEIROS — as imagens passam a viver em img/
# ══════════════════════════════════════════════════════════════════

html = troca(html, 'href="bluebolt-logo.webp"', 'href="img/bluebolt-logo.webp"', "favicon")
html = troca(
    html,
    '<img src="bluebolt-logo.webp" alt="Blue Bolt AI" style=',
    '<img src="img/bluebolt-logo.webp" alt="Blue Bolt Agency" style=',
    "logo rodape",
)
# O retrato original da pagina de IA, apanhado em blueboltai.online.
# Vinha a 1440x1800; reduzido para 1000px de largura (o dobro dos ~500 a
# que aparece), passa de 432KB a 202KB.
html = troca(html, 'src="ricardo.webp"',
             'src="img/ricardo.webp" width="1000" height="1250" loading="lazy" decoding="async"',
             "foto do Ricardo")

# ══════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════


html = troca(
    html,
    '<span class="t1">A sua equipa perde horas todos os dias em trabalho que </span><span class="t2">a IA já poderia fazer sozinha.</span>',
    '<span class="t1">Se depende de sorte com anúncios ou de alguém o recomendar, </span>'
    '<span class="t2">está a jogar à sorte, não a gerir um negócio.</span>',
    "h1",
)
html = troca(
    html,
    "Automatize processos, aumente produtividade e reduza custos com agentes de IA implementados à medida da sua operação, para que a tecnologia se adapte ao seu negócio e não o contrário.",
    "<strong>As empresas que escalam têm um sistema.</strong> Com o Sistema Previsível de Aquisição de Clientes, sabe todos os meses onde o dinheiro se perdeu, onde gerou oportunidades e onde se transformou em clientes.",
    "subtitulo do hero",
)
html = troca(
    html,
    '<span class="cta-btn-text">Quero a minha Equipa de IA</span>',
    '<span class="cta-btn-text">Agendar sessão estratégica</span>',
    "botao principal",
    esperado=2,
)

# ── Vídeo de fundo do hero (o mesmo do modelo do Elementor) ──────────
html = troca(
    html,
    """<div class="hero-wrap">

  <!-- Glow orbs animados -->""",
    """<div class="hero-wrap">

  <!-- Vídeo de fundo (o mesmo do modelo do Elementor).
       Sem <source>: a origem é posta por JS, e só em ecrãs largos. Com o
       <source> na marcação o browser descarregava os 7,7MB também no
       telemóvel, onde o vídeo nem se vê — ficava 94% do peso da página
       para um fundo. No telemóvel fica o fotograma. -->
  <video class="hero-bg-video" muted loop playsinline preload="none"
         poster="img/hero-poster.jpg" aria-hidden="true"
         data-src="img/hero-video.webm"
         data-src-movel="img/hero-video-movel.webm"></video>
  <div class="hero-bg-veil" aria-hidden="true"></div>

  <!-- Glow orbs animados -->""",
    "vídeo de fundo do hero",
)

# ── O hero fica so com o titulo, o subtitulo e um CTA ────────────────
# A faixa deslizante de provas sai e nada a substitui: as credenciais passam
# para o rodape. O botao secundario tambem sai, para o hero ter um so caminho.
faixa = re.search(
    r'\n *<div class="hero-trust-strip">.*?</div>\n\n      </div>\n    </div>\n  </section>',
    html,
    re.S,
)
if not faixa:
    falhas.append("hero: nao encontrei a faixa de confianca")
else:
    html = html.replace(faixa.group(0), "\n      </div>\n    </div>\n  </section>")

# ── A pilula por cima do titulo ──────────────────────────────────────
# Diz a oferta numa linha antes do titulo, como nos heros de SaaS: a
# primeira coisa que se le e o que se leva, nao o que se vende.
html = troca(
    html,
    '<div class="hero-content">\n\n        <h1 class="hero-h1">',
    '<div class="hero-content">\n\n'
    '        <div class="hero-badge" data-reveal="fade">\n'
    '          <span class="hero-badge-dot" aria-hidden="true"></span>\n'
    '          Diagnóstico gratuito de 30 minutos\n'
    '        </div>\n\n'
    '        <h1 class="hero-h1">',
    "pílula do hero",
)

html = troca(
    html,
    '\n          <a href="#trajetoria" class="btn-secondary">Ver como funciona</a>',
    "",
    "botão secundário do hero",
)
html = troca(
    html,
    '\n      <a href="#trajetoria" class="cta-btn-sec">Ver como funciona</a>',
    "",
    "botão secundário do CTA final",
)

# ── Credenciais no rodape: uma linha discreta, que ganha cor ao passar ─
html = troca(
    html,
    """    <div class="ft-bottom">""",
    """    <div class="ft-creds">
      <span class="ft-creds-label">Reconhecimentos</span>
      <div class="ft-creds-row">
        <img class="ft-cred" src="img/google-partner.webp" alt="Google Partner" width="110" height="110" loading="lazy" decoding="async">
        <img class="ft-cred" src="img/meta-partner.webp" alt="Meta Business Partner" width="110" height="110" loading="lazy" decoding="async">
        <img class="ft-cred" src="img/selo-top5.png" alt="Scoring Top 5% — Melhores PME de Portugal 2025, 2.º ano consecutivo" width="420" height="382" loading="lazy" decoding="async">
      </div>
    </div>

    <div class="ft-bottom">""",
    "credenciais no rodapé",
)


# ══════════════════════════════════════════════════════════════════
# VSL — nova seccao, a cavalo entre a primeira e a segunda dobra
# ══════════════════════════════════════════════════════════════════

VSL_CSS = """
/* ══ VSL — o player fica a cavalo entre a primeira e a segunda dobra ══
   Mesma tecnica da LP de referencia: o hero ganha folga em baixo, o bloco do
   video sobe com margem negativa em cima e em baixo, e a seccao seguinte
   ganha folga em cima para acomodar a metade que lhe fica por cima. */
#hero{ padding-bottom:9rem; }
.vsl-straddle{
  position:relative;
  z-index:50;
  max-width:800px;
  margin:-100px auto;
  padding:0 1rem;
}
#quem{ padding-top:11rem; }

@media(min-width:640px){
  #hero{ padding-bottom:15rem; }
  .vsl-straddle{ margin:-172px auto; }
  #quem{ padding-top:16rem; }
}
@media(min-width:1024px){
  #hero{ padding-bottom:19rem; }
  .vsl-straddle{ margin:-216px auto; }
  #quem{ padding-top:19rem; }
}

.vsl-shell{
  border-radius:24px;
  padding:6px;
  /* A sombra tem de funcionar dos dois lados da emenda: em cima o hero e
     escuro e ela nao se ve, em baixo o #f6f7f9 e claro e ela ve-se toda.
     A 75px de desfoque e 90% de preto, sobre o claro deixava de ser sombra
     e passava a ser um rectangulo cinzento por tras do video.

     O `-18px` de espalhamento e o que faz a diferenca: encolhe a sombra
     para dentro das arestas do cartao, e o que se ve passa a ser o cartao
     a levantar do fundo em vez de uma mancha com a forma dele. O brilho
     azul fica, que esse e o que faz o video ler-se como ecra aceso. */
  box-shadow:0 22px 44px -18px rgba(0,0,0,.72),
             0 6px 14px -8px rgba(0,0,0,.45),
             0 0 55px rgba(47,161,255,.15);
}
.vsl-screen{
  position:relative;
  display:block;
  width:100%;
  aspect-ratio:16/9;
  border-radius:18px;
  overflow:hidden;
  border:none;
  padding:0;
  cursor:pointer;
  background:#06080f center/cover no-repeat;
}
.vsl-screen::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(6,8,15,.12),rgba(6,8,15,.42));
  transition:background .3s;
}
.vsl-screen:hover::after{ background:linear-gradient(180deg,rgba(6,8,15,0),rgba(6,8,15,.28)); }
.vsl-play{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  z-index:2;
  width:80px;height:80px;border-radius:9999px;
  background:rgba(255,255,255,.94);
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 12px 40px rgba(0,0,0,.45),0 0 0 10px rgba(255,255,255,.08);
  transition:transform .3s cubic-bezier(.16,1,.3,1),box-shadow .3s;
}
.vsl-screen:hover .vsl-play{
  transform:translate(-50%,-50%) scale(1.07);
  box-shadow:0 16px 50px rgba(0,0,0,.5),0 0 0 14px rgba(47,161,255,.16);
}
.vsl-play svg{ width:26px;height:26px;margin-left:4px;color:#06080f; }
.vsl-screen iframe{
  position:absolute;inset:0;width:100%;height:100%;border:0;z-index:3;display:block;
}
.vsl-screen.is-playing::after,
.vsl-screen.is-playing .vsl-play{ display:none; }

@media(max-width:640px){
  .vsl-shell{ border-radius:18px;padding:5px; }
  .vsl-screen{ border-radius:14px; }
  .vsl-play{ width:58px;height:58px; }
  .vsl-play svg{ width:19px;height:19px; }
}
@media(prefers-reduced-motion:reduce){
  .vsl-screen,.vsl-screen::after,.vsl-play{ transition:none; }
}
"""

VSL_HTML = """
<!-- ===== VSL — a cavalo entre a primeira e a segunda dobra ===== -->
<div class="vsl-straddle" id="vsl">
  <div class="vsl-shell glass">
    <div class="vsl-screen" data-video="v4o2YB1vPjI" role="button" tabindex="0"
         aria-label="Reproduzir: como funciona o Sistema Previsível de Aquisição de Clientes"
         style="background-image:url('img/vsl-poster.webp')">
      <span class="vsl-play" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
      </span>
    </div>
  </div>
</div>
"""

VSL_JS = """
/* VSL — o iframe do YouTube so entra depois do clique, para nao pesar no arranque */
(function(){
  var box = document.querySelector('.vsl-screen');
  if(!box) return;
  function play(){
    if(box.classList.contains('is-playing')) return;
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + box.dataset.video +
      '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
    iframe.title = box.getAttribute('aria-label') || 'Vídeo';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    box.appendChild(iframe);
    box.classList.add('is-playing');
    box.removeAttribute('role');
    box.removeAttribute('tabindex');
  }
  box.addEventListener('click', play);
  box.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); play(); }
  });
})();
"""

AVISO_CSS = """
/* ══ Aviso de cookies ══
   Preso ao fundo e nao a meio do ecra: um painel a tapar a pagina toda
   antes de se ver o que ela e faz mais gente carregar em "Aceitar" so
   para se ver livre dele — e um "sim" desses nao vale nada. */
.ck{
  position:fixed;
  left:0;right:0;bottom:0;
  z-index:9999;
  padding:clamp(.75rem,2vw,1.25rem);
  animation:ck-sobe .45s cubic-bezier(.16,1,.3,1) both;
}
@keyframes ck-sobe{ from{ opacity:0;transform:translateY(16px); } to{ opacity:1;transform:none; } }
@media(prefers-reduced-motion:reduce){ .ck{ animation:none; } }
.ck[hidden]{ display:none; }
.ck-caixa{
  max-width:var(--medida-titulo);
  margin-inline:auto;
  background:rgba(10,13,24,.97);
  border:1px solid rgba(255,255,255,.14);
  border-radius:16px;
  padding:clamp(1.1rem,2.4vw,1.6rem);
  box-shadow:0 24px 60px rgba(0,0,0,.55);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
}
.ck-titulo{
  font-family:'Archia',sans-serif;
  font-size:17px;font-weight:600;letter-spacing:-.02em;
  color:#fff;margin:0 0 .45rem;
}
.ck-texto{
  font-family:'Manrope',sans-serif;
  font-size:14px;line-height:1.6;font-weight:300;
  color:rgba(255,255,255,.72);margin:0;
}

/* ══ Painel de escolhas ══ */
.ck-opcoes{ margin-top:1.1rem;border-top:1px solid rgba(255,255,255,.1); }
.ck-opcoes[hidden]{ display:none; }
.ck-linha{
  display:flex;align-items:flex-start;gap:1rem;
  padding:.9rem 0;
  border-bottom:1px solid rgba(255,255,255,.07);
  cursor:pointer;
}
.ck-linha-fixa{ cursor:default; }
.ck-info{ display:flex;flex-direction:column;gap:.2rem;flex:1; }
.ck-nome{ font-family:'Manrope',sans-serif;font-size:13.5px;font-weight:600;color:#fff; }
.ck-desc{ font-family:'Manrope',sans-serif;font-size:12.5px;line-height:1.5;font-weight:300;color:rgba(255,255,255,.55); }
.ck-sempre{ font-family:'Manrope',sans-serif;font-size:11.5px;color:rgba(255,255,255,.4);white-space:nowrap;padding-top:.15rem; }

/* O interruptor e uma checkbox a serio por baixo: le-se com leitor de
   ecra e apanha o teclado sem ter de se lhe ensinar nada. */
.ck-switch{
  appearance:none;-webkit-appearance:none;
  flex:0 0 auto;
  width:42px;height:24px;margin:0;
  border-radius:100px;
  background:rgba(255,255,255,.16);
  border:1px solid rgba(255,255,255,.2);
  position:relative;cursor:pointer;
  transition:background .2s ease,border-color .2s ease;
  /* Sem efeito nenhum — a caixa tem medidas fixas e nao leva texto. Esta
     aqui so para a auditoria de movel nao a apanhar como campo que faz o
     iOS aproximar a pagina, que e coisa de campos de texto, nao de
     caixas de seleccao. */
  font-size:16px;
}
.ck-switch::after{
  content:'';position:absolute;top:2px;left:2px;
  width:18px;height:18px;border-radius:50%;
  background:#fff;
  transition:transform .2s cubic-bezier(.16,1,.3,1);
}
.ck-switch:checked{ background:#2fa1ff;border-color:#2fa1ff; }
.ck-switch:checked::after{ transform:translateX(18px); }
.ck-switch:focus-visible{ outline:2px solid #2fa1ff;outline-offset:3px; }

/* ══ Botoes ══
   Os tres do mesmo tamanho e com o mesmo peso. Um "Aceitar" grande ao
   lado de um "Rejeitar" a cinzento e o que invalida o consentimento. */
.ck-botoes{
  display:flex;gap:.6rem;
  margin-top:1.1rem;
}
.ck-btn{
  flex:1;
  min-height:46px;
  padding:.7rem 1rem;
  border-radius:100px;
  border:1px solid rgba(255,255,255,.22);
  background:rgba(255,255,255,.07);
  color:#fff;
  font-family:'Manrope',sans-serif;
  font-size:13.5px;font-weight:600;
  cursor:pointer;
  transition:background .2s ease,border-color .2s ease;
}
.ck-btn:hover{ background:rgba(255,255,255,.13);border-color:rgba(255,255,255,.34); }
.ck-btn:focus-visible{ outline:2px solid #2fa1ff;outline-offset:2px; }
.ck-btn-sim{ background:#2fa1ff;border-color:#2fa1ff;color:#04060f; }
.ck-btn-sim:hover{ background:#4fb0ff;border-color:#4fb0ff; }

.ck-rodape{
  margin:.85rem 0 0;
  font-family:'Manrope',sans-serif;font-size:11.5px;
  color:rgba(255,255,255,.4);text-align:center;
}
/* Sao texto corrido dentro de um paragrafo pequeno: sem folga ficavam com
   12px de altura tocavel. */
.ck-rodape a{ color:rgba(255,255,255,.62);text-decoration:underline;
  display:inline-block;padding:.9rem .4rem; }
.ck-rodape a:hover{ color:#fff; }

@media(max-width:600px){
  .ck-botoes{ flex-direction:column; }
  .ck-texto{ font-size:13.5px; }
}
"""

html = troca(html, "</style>", VSL_CSS + NAV_CSS + SECOES_CSS + AVISO_CSS + "</style>", "CSS da VSL, do hero, das secções e do aviso de cookies")
html = troca(html, '\n<!-- QUEM É -->', VSL_HTML + '\n<!-- QUEM É -->', "marcacao da VSL")
html = troca(html, "\n/* Submissão do formulário de lead", VSL_JS + "\n/* Submissão do formulário de lead", "JS da VSL")

# ══════════════════════════════════════════════════════════════════
# BOTAO LIQUID METAL — o CTA do hero
# Replica do componente pedido sem WebGL: onde o original monta um
# fragment shader do @paper-design/shaders, aqui ha um conic-gradient
# de quatro repeticoes a rodar por tras de uma pastilha preta, com 2px
# de folga — e essa folga que faz o aro metalico. O shader tinha
# shiftRed/shiftBlue; as paragens quentes e frias ao lado do branco
# fazem a mesma franja cromatica.
# ══════════════════════════════════════════════════════════════════

def botao_lm(rotulo, *, href=None, tipo=None, classe=""):
    """O botao, de uma so receita — e usado no hero, no formulario e no CTA."""
    if href:
        abre = f'<a href="{href}" class="lm-btn{classe}" data-lm>'
        fecha = "</a>"
    else:
        abre = f'<button type="{tipo or "button"}" class="lm-btn{classe}" data-lm>'
        fecha = "</button>"
    return (abre
            + '<span class="lm-aro" aria-hidden="true"></span>'
            + '<span class="lm-face" aria-hidden="true"></span>'
            + f'<span class="lm-conteudo"><span class="lm-label">{rotulo}</span></span>'
            + fecha)

BOTAO_LM = botao_lm("Agendar sessão estratégica", href="#guia")

ctas = re.search(r'<div class="hero-ctas">\s*<a href="#guia" class="cta-btn-main">.*?</a>\s*</div>', html, re.S)
if not ctas:
    falhas.append("botao do hero: nao encontrei o bloco")
else:
    html = html.replace(ctas.group(0), '<div class="hero-ctas">\n          ' + BOTAO_LM + '\n        </div>')

# O motor da rotacao do botao. E o equivalente ao setSpeed do componente
# original: a velocidade aproxima-se da meta em vez de saltar, por isso o
# metal acelera ao passar o rato e leva um impulso no clique sem trancos.
BOTAO_LM_JS = """
/* Botao liquid metal — roda o aro e responde ao rato */
(function(){
  var botoes = Array.prototype.slice.call(document.querySelectorAll('[data-lm]'));
  if(!botoes.length) return;

  var parado = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var estados = botoes.map(function(el){
    return { el:el, angulo: 24, vel: 1.9, meta: 1.9 };
  });

  if(parado){
    estados.forEach(function(s){ s.el.style.setProperty('--lm-a', s.angulo); });
  } else {
    var anterior = performance.now();
    (function passo(agora){
      var dt = Math.min(64, agora - anterior); anterior = agora;
      estados.forEach(function(s){
        s.vel += (s.meta - s.vel) * Math.min(1, dt / 220);
        s.angulo = (s.angulo + s.vel * dt * 0.022) % 360;
        s.el.style.setProperty('--lm-a', s.angulo.toFixed(2));
      });
      requestAnimationFrame(passo);
    })(anterior);
  }

  estados.forEach(function(s){
    s.el.addEventListener('mouseenter', function(){ s.meta = 3.4; });
    s.el.addEventListener('mouseleave', function(){ s.meta = 1.9; });
    s.el.addEventListener('click', function(e){
      s.meta = 7;
      setTimeout(function(){ s.meta = s.el.matches(':hover') ? 3.4 : 1.9; }, 320);
      var r = s.el.getBoundingClientRect();
      var onda = document.createElement('span');
      onda.className = 'lm-onda';
      onda.style.left = (e.clientX - r.left) + 'px';
      onda.style.top  = (e.clientY - r.top)  + 'px';
      s.el.appendChild(onda);
      setTimeout(function(){ onda.remove(); }, 600);
    });
  });
})();
"""
html = troca(
    html,
    "\n/* Submissão do formulário de lead",
    BOTAO_LM_JS + "\n/* Submissão do formulário de lead",
    "JS do botão liquid metal",
)

# O video de fundo so e descarregado onde e visto: em ecras largos, depois
# do primeiro pintar, e nunca com movimento reduzido. Sao 7,7MB — no
# telemovel eram 94% do peso da pagina para um fundo que o veu quase tapa.
VIDEO_JS = """
/* Vídeo de fundo do herói.
   No telemóvel corre uma cópia própria: 720x405 a 24fps, sem faixa de som,
   768KB contra os 7,7MB da de secretária. Atrás de um véu a 70% o detalhe
   que se perde não se vê, e o peso deixa de ser uma razão para não o ter.
   Em qualquer dos casos só entra depois de a página pintar, e nunca com
   `prefers-reduced-motion` nem com poupança de dados ligada. */
(function(){
  var v = document.querySelector('.hero-bg-video');
  if(!v || !v.dataset.src) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* Quem tem o Poupar Dados ligado, ou está em 2G/3G, fica com o
     fotograma. Pedir-lhe 768KB de enfeite seria abusar. */
  var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if(c){
    if(c.saveData) return;
    if(/^(slow-2g|2g|3g)$/.test(c.effectiveType || '')) return;
  }

  var largo  = window.matchMedia('(min-width: 861px)').matches;
  var origem = largo ? v.dataset.src : (v.dataset.srcMovel || v.dataset.src);

  window.addEventListener('load', function(){
    v.src = origem;
    v.preload = 'auto';
    var t = v.play();
    if(t && t.catch) t.catch(function(){});
  });
})();
"""
html = troca(
    html,
    "\n/* Submissão do formulário de lead",
    VIDEO_JS + "\n/* Submissão do formulário de lead",
    "JS do vídeo de fundo",
)

# ══════════════════════════════════════════════════════════════════
# SEGUNDA DOBRA — o problema, com a ampulheta em destaque
# A seccao inteira e substituida: sai o cartao com a foto, as estatisticas
# e as credenciais; entra o texto novo e o funil em ampulheta.
# ══════════════════════════════════════════════════════════════════

seccao = re.search(r'<section id="quem">.*?\n</section>', html, re.S)
if not seccao:
    falhas.append("segunda dobra: nao encontrei a seccao #quem")
else:
    html = html.replace(seccao.group(0), SEGUNDA_DOBRA)

# ══════════════════════════════════════════════════════════════════
# CAPACIDADES — nove cartoes
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<div class="band-eyebrow" data-reveal="fade">Capacidades</div>',
    '<div class="band-eyebrow" data-reveal="fade">O que implementamos</div>',
    "sobrancelha das capacidades",
)
html = troca(
    html,
    '<span class="band-tg">O que a sua Equipa de IA </span><span class="band-ta">faz por si.</span>',
    '<span class="band-tg">Implementamos tudo o que precisa para </span><span class="band-ta">aumentar a sua faturação.</span>',
    "h2 das capacidades",
)
html = troca(
    html,
    "Não vendemos chatbots genéricos. Cada agente e sistema é construído à medida, para transformar processos reais da sua empresa.",
    "Não vendemos serviços isolados. Cada peça é construída à medida e ligada às restantes, porque é o sistema completo que traz clientes — não uma campanha à parte.",
    "subtitulo das capacidades",
)

CARTOES = [
    (
        "Atendimento 24/7",
        "Responde a clientes a qualquer hora, em segundos, com o tom da sua marca e sem deixar ninguém à espera.",
        "Design e edição de vídeo",
        "Criativos, anúncios e vídeo pensados para parar o scroll e comunicar a sua oferta com clareza.",
    ),
    (
        "Automação de processos",
        "Tarefas internas repetitivas tratadas sozinhas, sem erros e sem espera, dia e noite.",
        "Email marketing",
        "Sequências que mantêm a sua base quente e trazem de volta quem ainda não decidiu comprar.",
    ),
    (
        "Follow-up de vendas",
        "Persegue leads, agenda reuniões e faz o seguimento, sem deixar nenhuma oportunidade cair.",
        "Fluxos de WhatsApp",
        "Contacto imediato assim que a lead entra, no canal onde as pessoas respondem mesmo.",
    ),
    (
        "Conteúdo e comunicação",
        "Rascunhos de emails, respostas e conteúdos gerados em minutos, prontos a rever e enviar.",
        "Landing pages",
        "Páginas construídas para converter, testadas e ligadas ao resto do sistema de aquisição.",
    ),
    (
        "Triagem e qualificação",
        "Filtra e organiza emails, pedidos e leads, para a sua equipa focar só no que importa.",
        "CRM integrado",
        "Todas as leads num só sítio, com o estado de cada conversa visível para toda a equipa.",
    ),
    (
        "Relatórios automáticos",
        "Dados e relatórios prontos quando precisa, sem ninguém a compilar folhas de cálculo à mão.",
        "Scripts e playbook comercial",
        "O que dizer, quando dizer e como responder às objeções, para a venda não depender da inspiração do dia.",
    ),
    (
        "Sistemas e software à medida",
        "ERPs, CRMs e plataformas internas construídas de raiz para o seu negócio, não soluções genéricas.",
        "Reunião estratégica mensal",
        "Uma hora por mês a olhar para os números consigo e a decidir os próximos passos do trimestre.",
    ),
    (
        "Controlo financeiro automatizado",
        "Plataformas de gestão financeira e automação administrativa, com dados sempre atualizados.",
        "Reports semanais e dashboard",
        "Um painel só seu, com investimento, leads, custo por cliente e faturação atribuída.",
    ),
    (
        "Agentes que trabalham em equipa",
        "Vários agentes de IA a comunicar entre si, a analisar dados e a apoiar as suas decisões.",
        "Equipa dedicada",
        "Um gestor de projeto, um estratega e especialistas de tráfego, design e copy alocados ao seu negócio.",
    ),
]
for titulo_a, desc_a, titulo_n, desc_n in CARTOES:
    html = troca(html, f'<h3 class="band-card-title">{titulo_a}</h3>', f'<h3 class="band-card-title">{titulo_n}</h3>', f"cartao {titulo_a}")
    html = troca(html, f'<p class="band-card-desc">{desc_a}</p>', f'<p class="band-card-desc">{desc_n}</p>', f"desc cartao {titulo_a}")

# ══════════════════════════════════════════════════════════════════
# DIAGNOSTICO GRATUITO + FORMULARIO
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<div class="quem-eyebrow">Análise gratuita</div>',
    '<div class="quem-eyebrow">Diagnóstico gratuito</div>',
    "sobrancelha do diagnostico",
)
html = troca(
    html,
    '<span class="tg">Descubra quanto pode </span><span class="ta">poupar com uma Equipa de IA.</span>',
    '<span class="tg">Descubra o que está a travar </span><span class="ta">o crescimento do seu negócio.</span>',
    "h2 do diagnostico",
)
html = troca(
    html,
    "Fale com a nossa equipa e descubra, sem compromisso, o que a IA pode fazer pela sua empresa. Nesta análise gratuita, vai receber:",
    "Trinta minutos com a nossa equipa, sem custo e sem pitch de vendas. Neste diagnóstico, vai receber:",
    "subtitulo do diagnostico",
)
STACK = [
    ("<b>Mapa dos processos</b> que a IA já pode automatizar na sua empresa", "<b>Um raio-x do seu funil</b>, da atração ao fecho, com os pontos de perda identificados"),
    ("<b>Estimativa de horas e custos</b> que pode poupar todos os meses", "<b>Quanto lhe custa hoje cada cliente</b> e onde esse custo pode descer"),
    ("<b>As oportunidades de maior impacto</b>, por ordem de prioridade", "<b>As oportunidades de maior impacto</b>, por ordem de prioridade"),
    ("<b>Um plano claro dos próximos passos</b>, sem compromisso de compra", "<b>Um plano claro dos próximos 90 dias</b>, sem compromisso de compra"),
]
for antigo, novo in STACK:
    if antigo != novo:
        html = troca(html, antigo, novo, f"lista: {antigo[:34]}")
html = troca(
    html,
    '<div class="lead-form-title">Quanto pode poupar a minha empresa?</div>',
    '<div class="lead-form-title">Agendar a minha sessão estratégica</div>',
    "titulo do formulario",
)
html = troca(
    html,
    '<p class="lead-form-sub">Fale com a nossa equipa e perceba, sem compromisso, o que a IA pode fazer pela sua empresa.</p>',
    '<p class="lead-form-sub">Deixe os seus dados e marcamos o diagnóstico de 30 minutos. Sem custo, sem compromisso.</p>',
    "subtitulo do formulario",
)
html = troca(
    html,
    '<button class="lead-submit" type="submit">Quero a minha análise gratuita</button>',
    '<button class="lead-submit" type="submit">Quero o meu diagnóstico gratuito</button>',
    "botao do formulario",
)
html = troca(
    html,
    "Sem custo e sem compromisso. A nossa equipa entra em contacto em 24 horas.",
    "Sem spam e sem compromisso. A nossa equipa entra em contacto em menos de 24 horas.",
    "nota do formulario",
)
html = troca(
    html,
    "'O seu pedido foi registado. A nossa equipa vai analisar o seu caso e entra em contacto em 24 horas com as oportunidades de IA para a sua empresa.</p>';",
    "'O seu pedido foi registado. A nossa equipa vai analisar o seu caso e entra em contacto em menos de 24 horas para agendar o diagnóstico.</p>';",
    "mensagem de sucesso",
)

html = troca(
    html,
    '<section class="cta-section">',
    TESTEMUNHOS_HTML + '<section class="cta-section">',
    "secção dos testemunhos",
)

# O facade do YouTube servia um video so; agora ha nove na pagina.
html = troca(
    html,
    """  var box = document.querySelector('.vsl-screen');
  if(!box) return;
  function play(){""",
    """  document.querySelectorAll('.vsl-screen').forEach(function(box){
  function play(){""",
    "facade do YouTube: abrir a todos os vídeos (início)",
)
html = troca(
    html,
    """  box.addEventListener('click', play);
  box.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); play(); }
  });
})();""",
    """  box.addEventListener('click', play);
  box.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); play(); }
  });
  });
})();""",
    "facade do YouTube: abrir a todos os vídeos (fim)",
)

# ══════════════════════════════════════════════════════════════════
# QUEM E O RICARDO — a peca da Blue Bolt AI, com os textos da agencia
# Layout, foto e numeros ficam como estao; muda a copy, que era sobre IA.
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    'alt="Ricardo, CEO da Blue Bolt e cofundador da Blue Bolt AI"',
    'alt="Ricardo, CEO da Blue Bolt"',
    "alt da foto do Ricardo",
)
html = troca(
    html,
    '<div class="expert-role">CEO da Blue Bolt · Cofundador da Blue Bolt AI</div>',
    '<div class="expert-role">CEO da Blue Bolt · Google Partner · Meta Business Partner</div>',
    "cargo do Ricardo",
)
html = troca(
    html,
    '<span class="tg">Quem está por trás da </span><span class="ta">Blue Bolt AI.</span>',
    '<span class="tg">Quem está por trás da </span><span class="ta">Blue Bolt Agency.</span>',
    "título da secção do Ricardo",
)
html = troca(
    html,
    "<p>Há uns anos, o Ricardo trabalhava doze a catorze horas por dia. A empresa crescia, mas a margem não acompanhava — cada vez mais despesas com pessoas, e o tempo nunca chegava. Sentia-se preso numa roda que não parava.</p>",
    "<p>Há uns anos, o Ricardo geria um negócio que dependia de indicações. Uns meses entravam clientes, noutros não entrava nenhum — e não havia forma de saber porquê. Investir em anúncios era atirar dinheiro para o escuro e esperar.</p>",
    "bio do Ricardo, 1.º parágrafo",
)
html = troca(
    html,
    "<p>Até perceber que a IA não veio para substituir pessoas. Veio para substituir o trabalho repetitivo e de pouco valor. <strong>Por isso construímos IA para nós primeiro — e funcionou tão bem que passámos a instalar o mesmo motor nas empresas dos nossos clientes.</strong></p>",
    "<p>Até perceber que o problema nunca tinha sido o anúncio: era não haver sistema por trás dele. <strong>Por isso montámos o sistema para nós primeiro — e funcionou tão bem que passámos a instalá-lo nas empresas dos nossos clientes.</strong></p>",
    "bio do Ricardo, 2.º parágrafo",
)
html = troca(
    html,
    "<p>A Blue Bolt acompanha mais de 400 negócios, é Google Partner e está no Top 5% das PME de Portugal. Conhecemos a tecnologia por dentro, porque é isso que fazemos todos os dias.</p>",
    "<p>A Blue Bolt acompanha mais de 400 negócios, é Google Partner e Meta Business Partner, e está no Top 5% das PME de Portugal. Sabemos o que resulta porque o vemos acontecer todos os meses, em dezenas de contas.</p>",
    "bio do Ricardo, 3.º parágrafo",
)

# ══════════════════════════════════════════════════════════════════
# CTA FINAL
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<h2 class="cta-h2" data-reveal data-delay="1">Ponha a IA a trabalhar por si<br><span class="cta-ta">antes da sua concorrência.</span></h2>',
    '<h2 class="cta-h2" data-reveal data-delay="1">Pare de depender de indicações <span class="cta-ta">e monte um sistema previsível.</span></h2>',
    "h2 do CTA final",
)
html = troca(
    html,
    "Comece com uma análise gratuita e veja, em concreto, o que a sua Equipa de IA pode automatizar e quanto tempo lhe devolve todas as semanas. A IA não vai substituir a sua empresa, mas uma empresa que usa IA vai substituir a que não usa. A análise é grátis, mas as vagas por mês não são infinitas.",
    "Comece com um diagnóstico gratuito de 30 minutos e veja, em concreto, onde está a perder clientes e o que muda quando a atração, a nutrição e o processo comercial passam a trabalhar juntos. O diagnóstico é grátis, mas só aceitamos um número limitado de novos projetos por mês.",
    "subtitulo do CTA final",
)

# ══════════════════════════════════════════════════════════════════
# RODAPE
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<div class="ft-role">Uma empresa Blue Bolt · Google Partner</div>',
    '<div class="ft-role">Agência de marketing digital</div>',
    "papel no rodape",
)
html = troca(
    html,
    """        <a href="#trajetoria">Como funciona</a>
        <a href="#bandeiras">O que faz</a>
        <a href="#guia">O Motor de IA</a>
        <a href="#autoridade">Quem somos</a>
        <a href="bluebolt-ai-blog.html">Blog</a>""",
    """        <a href="#vsl">O sistema</a>
        <a href="#trajetoria">Como funciona</a>
        <a href="#bandeiras">O que implementamos</a>
        <a href="#autoridade">Quem somos</a>
        <a href="#guia">Diagnóstico gratuito</a>""",
    "navegacao do rodape",
)
html = troca(
    html,
    '<span class="ft-copy">2026 Blue Bolt AI. Todos os direitos reservados.</span>',
    '<span class="ft-copy">2026 Blue Bolt Agency. Todos os direitos reservados.</span>',
    "copyright",
)
html = troca(
    html,
    '<a href="bluebolt-ai-privacidade.html">Privacidade</a> &middot; <a href="bluebolt-ai-termos.html">Termos</a> &middot; <a href="bluebolt-ai-eliminacao-dados.html">Elimina&ccedil;&atilde;o de dados</a>',
    '<a href="https://bluebolt.pt/politica-de-privacidade/" target="_blank" rel="noopener">Política de privacidade</a>',
    "legais do rodape",
)

# ══════════════════════════════════════════════════════════════════
# RODAPE — quatro colunas, como no site
# Contactos, informacoes uteis, parcerias, e a barra de financiamento.
# A barra (PRR / Republica Portuguesa / Uniao Europeia) so entra se o
# ficheiro estiver em img/: assim quem o puser nao precisa de mexer aqui,
# e sem ele o rodape nao fica com uma imagem partida.
# ══════════════════════════════════════════════════════════════════

REDES = [
    ("Facebook", "https://www.facebook.com/blueboltagency",
     '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    ("Instagram", "https://www.instagram.com/bluebolt.agency/",
     '<rect x="2" y="2" width="20" height="20" rx="5"/>'
     '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
     '<line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>'),
    ("LinkedIn", "https://pt.linkedin.com/company/blue-bolt-agency",
     '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/>'
     '<rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>'),
    ("TikTok", "https://www.tiktok.com/@blueboltagency",
     '<path d="M15 3a5.5 5.5 0 0 0 5.5 5.5v3A8.5 8.5 0 0 1 15 9.6V15a6 6 0 1 1-6-6 6 6 0 0 1 1 .09v3.2A2.8 2.8 0 1 0 12 15V3z"/>'),
]

UTEIS = [
    ("Política de Privacidade", "https://bluebolt.pt/politica-de-privacidade/"),
    ("Política de Cookies", "https://bluebolt.pt/politica-de-cookies/"),
    ("Livro de Reclamações", "https://www.livroreclamacoes.pt/Inicio/"),
]

_redes = "".join(
    f'<a class="ft-rede" href="{u}" target="_blank" rel="noopener" aria-label="{n}">'
    f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    f'stroke-linecap="round" stroke-linejoin="round">{d}</svg></a>'
    for n, u, d in REDES
)
_uteis = "".join(
    f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in UTEIS
)

# A barra de financiamento so aparece se o ficheiro existir.
_barra = ""
if os.path.exists(os.path.join(HERE, "img", "barra-logos.webp")):
    _barra = (
        '\n    <div class="ft-fundos">\n'
        '      <img src="img/barra-logos.webp" alt="PRR — Plano de Recuperação e Resiliência · '
        'República Portuguesa · Financiado pela União Europeia, NextGenerationEU" '
        'width="1024" height="125" loading="lazy" decoding="async">\n'
        '    </div>\n'
    )

RODAPE_HTML = """<footer class="ft">
  <div class="ft-inner">

    <div class="ft-grelha">

      <div class="ft-marca">
        <img class="ft-logo" src="img/bluebolt-lockup.webp" alt="Blue Bolt Agency" width="300" height="287">
        <div class="ft-role">Agência de marketing digital</div>
        <div class="ft-redes">""" + _redes + """</div>
      </div>

      <div class="ft-col">
        <h3 class="ft-col-h">Contacte-nos</h3>
        <ul class="ft-lista">
          <li>
            <svg class="ft-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>
            <a href="mailto:geral@bluebolt.pt">geral@bluebolt.pt</a>
          </li>
          <li>
            <svg class="ft-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
            <span>
              <a href="tel:+351927135702">+351 927 135 702</a>
              <small class="ft-nota">Chamada para rede móvel nacional</small>
            </span>
          </li>
        </ul>
      </div>

      <div class="ft-col">
        <h3 class="ft-col-h">Informações úteis</h3>
        <ul class="ft-lista ft-lista-simples">""" + _uteis + """</ul>
      </div>

      <div class="ft-col">
        <h3 class="ft-col-h">Parcerias</h3>
        <div class="ft-selos">
          <img class="ft-selo" src="img/google-partner.webp" alt="Google Partner" width="110" height="110" loading="lazy" decoding="async">
          <img class="ft-selo" src="img/meta-partner.webp" alt="Meta Business Partner" width="110" height="110" loading="lazy" decoding="async">
          <img class="ft-selo ft-selo-grande" src="img/selo-top5.png" alt="Scoring Top 5% — Melhores PME de Portugal 2025, 2.º ano consecutivo" width="420" height="382" loading="lazy" decoding="async">
        </div>
      </div>

    </div>
""" + _barra + """
    <div class="ft-bottom">
      <span class="ft-copy">© 2026 Blue Bolt Agency · Todos os direitos reservados</span>
    </div>

  </div>
</footer>"""

rodape = re.search(r"<footer class=\"ft\">.*?</footer>", html, re.S)
if not rodape:
    falhas.append("rodape: nao encontrei o bloco")
else:
    html = html.replace(rodape.group(0), RODAPE_HTML)

# ── O mesmo botao no formulario e no CTA final ───────────────────────
html = troca(
    html,
    '<button class="lead-submit" type="submit">Quero o meu diagnóstico gratuito</button>',
    botao_lm("Quero o meu diagnóstico gratuito", tipo="submit", classe=" lm-btn-bloco"),
    "botão do formulário",
)

cta = re.search(r'<a href="#guia" class="cta-btn-main">.*?</a>', html, re.S)
if not cta:
    falhas.append("CTA final: nao encontrei o botao")
else:
    html = html.replace(cta.group(0), botao_lm("Agendar sessão estratégica", href="#guia"))

# ══════════════════════════════════════════════════════════════════
# DADOS ESTRUTURADOS (JSON-LD) — tem de descrever a empresa certa
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '    "name": "Blue Bolt AI",\n'
    '    "description": "Blue Bolt AI constrói e instala agentes de IA e automações à medida das empresas, '
    'para automatizar atendimento, vendas e processos internos. Uma empresa Blue Bolt, agência Google Partner.",\n'
    '    "url": "https://bluebolt.pt/ai",',
    '    "name": "Blue Bolt Agency",\n'
    '    "description": "A Blue Bolt Agency constrói sistemas previsíveis de aquisição de clientes: atração com '
    'tráfego pago, nutrição por email e WhatsApp, processo comercial e medição de resultados. Agência Google '
    'Partner e Meta Business Partner.",\n'
    '    "url": "https://bluebolt.pt",',
    "JSON-LD: nome, descrição e url",
)
html = troca(
    html,
    '    "knowsAbout": ["Agentes de IA", "Automação de Processos", "Inteligência Artificial para Empresas", '
    '"IA para Vendas", "Atendimento com IA"],',
    '    "knowsAbout": ["Marketing Digital", "Tráfego Pago", "Google Ads", "Meta Ads", "Geração de Leads", '
    '"Funis de Aquisição de Clientes"],',
    "JSON-LD: knowsAbout",
)
html = troca(
    html,
    '    "parentOrganization": {\n'
    '      "@type": "Organization",\n'
    '      "name": "Blue Bolt",\n'
    '      "url": "https://bluebolt.pt"\n'
    '    },\n',
    "",
    "JSON-LD: parentOrganization",
)

# ══════════════════════════════════════════════════════════════════
# O FORMULARIO PASSA A SER O DO CRM
# O nosso era bonito e nao servia para nada: mostrava "Obrigado!" e
# deitava a lead fora. Este e o formulario do Go High Level, e as
# submissoes caem no CRM.
#
# Ja vem estilizado para fundo escuro — campos a #FFFFFF0D, texto branco,
# marcador a #D5D5D5 — que e quase o que a nossa caixa tinha, por isso
# encaixa na seccao sem parecer colado. E tem campo de telefone, que o
# nosso nao tinha.
#
# O titulo e o subtitulo ficam fora do iframe: sao texto nosso, e dentro
# do iframe nao os podiamos compor nem traduzir.
# ══════════════════════════════════════════════════════════════════

FORMULARIO_CRM = "ZBEyR6JAk4CBl4jVfnSD"

IFRAME_CRM = (
    '<div class="lead-form" id="lead-form">'
    '<div class="lead-form-title">Agendar a minha sessão estratégica</div>'
    '<p class="lead-form-sub">Deixe os seus dados e marcamos o diagnóstico de 30 minutos. '
    "Sem custo, sem compromisso.</p>"
    f'<iframe src="https://api.leadconnectorhq.com/widget/form/{FORMULARIO_CRM}" '
    'class="lead-crm" '
    f'id="inline-{FORMULARIO_CRM}" '
    'title="Formulário de contacto" '
    'style="width:100%;height:640px;border:none;background:transparent" '
    "data-layout=\"{'id':'INLINE'}\" "
    'data-trigger-type="alwaysShow" '
    'data-activation-type="alwaysActivated" '
    'data-deactivation-type="neverDeactivate" '
    'data-form-name="Diagnóstico gratuito" '
    'data-height="640" '
    f'data-layout-iframe-id="inline-{FORMULARIO_CRM}" '
    f'data-form-id="{FORMULARIO_CRM}"></iframe>'
    '<p class="lead-fine">Sem spam e sem compromisso. '
    "A nossa equipa entra em contacto em menos de 24 horas.<br>"
    # O formulario passou a ser o unico caminho de conversao da pagina, e
    # vive num iframe de outro dominio. Se o CRM estiver em baixo ou for
    # bloqueado, fica uma caixa vazia e o visitante nao tem por onde ir.
    'Se o formulário não carregar, escreva para '
    '<a href="mailto:geral@bluebolt.pt">geral@bluebolt.pt</a>.</p>'
    "</div>"
)

alvo = re.search(r'<form class="lead-form".*?</form>', html, re.S)
if not alvo:
    falhas.append("formulario: nao encontrei o bloco a substituir")
else:
    html = html.replace(alvo.group(0), IFRAME_CRM)

# O script do embed trata de ajustar a altura do iframe ao conteudo — sem
# ele fica com a altura fixa e corta o botao em ecras pequenos.
html = troca(
    html,
    "</body>",
    '<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>\n</body>',
    "script do embed do CRM",
)

# ══════════════════════════════════════════════════════════════════
# GOOGLE TAG MANAGER
# O contentor entra em dois sitios: o script o mais cedo possivel no
# <head>, e o <iframe> de recurso logo a abrir o <body>, para quem tem o
# JavaScript desligado. O `dataLayer` e declarado pelo proprio snippet.
#
# O snippet do Google Analytics que a pagina trazia ficou para tras com um
# GA_MEASUREMENT_ID por preencher: sai. Se for preciso GA, e o GTM que o
# deve carregar — dois carregadores a fazer o mesmo trabalho e a receita
# para eventos contados a dobrar.
# ══════════════════════════════════════════════════════════════════

GTM_ID = "GTM-WG4ZH4LF"

GTM_HEAD = (
    "  <!-- Google Tag Manager -->\n"
    "  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
    "  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
    "  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
    "  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
    f"  }})(window,document,'script','dataLayer','{GTM_ID}');</script>\n"
    "  <!-- End Google Tag Manager -->\n"
)

GTM_BODY = (
    "<!-- Google Tag Manager (noscript) -->\n"
    f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
    'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
    "<!-- End Google Tag Manager -->\n"
)

# Fora o GA meio ligado.
ga = re.search(
    r'  <script async src="https://www\.googletagmanager\.com/gtag/js\?id=GA_MEASUREMENT_ID"></script>.*?</script>\n',
    html, re.S)
if not ga:
    falhas.append("snippet do Google Analytics por preencher")
else:
    html = html.replace(ga.group(0), GTM_HEAD)

html = troca(html, "<body>", "<body>\n" + GTM_BODY, "iframe de recurso do GTM")

# ══════════════════════════════════════════════════════════════════
# META PIXEL
# O ID do pixel e publico por definicao — vive no codigo da pagina e
# qualquer visitante o le. O token da Conversions API e que nao: e uma
# credencial de servidor, e nao entra aqui nem em ficheiro nenhum deste
# repositorio, que e publico. Vive numa variavel de ambiente, no sitio
# onde correr o codigo que recebe o formulario.
# ══════════════════════════════════════════════════════════════════

META_PIXEL = "260575891666892"

html = troca(html, "fbq('init', 'META_PIXEL_ID');", f"fbq('init', '{META_PIXEL}');", "init do pixel")
html = troca(
    html,
    'src="https://www.facebook.com/tr?id=META_PIXEL_ID&ev=PageView&noscript=1"',
    f'src="https://www.facebook.com/tr?id={META_PIXEL}&ev=PageView&noscript=1"',
    "pixel sem javascript",
)

# ══════════════════════════════════════════════════════════════════
# CONSENTIMENTO DE COOKIES
# O pixel do Meta em Portugal precisa de consentimento previo, e o rodape
# ja apontava para uma Politica de Cookies que a pagina nao cumpria.
#
# Como esta montado:
#
#   Meta Pixel — nao carrega de todo antes do "sim". Nao ha meio-termo: ou
#   o fbevents.js entra, ou nao entra. O <noscript> que a pagina trazia sai
#   de vez — disparava um pedido ao Meta para quem tem o JavaScript
#   desligado, e a esses nao ha como perguntar nada.
#
#   GTM — carrega, mas com o Consent Mode v2 tudo em "denied" antes de o
#   fazer. E o modelo da propria Google: o contentor corre, nao poe cookies
#   nem envia identificadores enquanto nao houver consentimento. Sem isto,
#   o Google Ads deixa de medir seja o que for no EEE.
#
#   Formulario do CRM — continua a carregar. E o servico que a pessoa veio
#   buscar, nao rastreio, e bloquea-lo era deixar a pagina sem o unico
#   caminho de conversao que tem. Fica dito no texto do aviso.
#
# Rejeitar tem o mesmo tamanho e o mesmo peso visual que aceitar. Um
# "Aceitar" grande e colorido ao lado de um "Rejeitar" a cinzento e o que a
# CNPD e o EDPB chamam padrao enganoso, e invalida o consentimento.
# ══════════════════════════════════════════════════════════════════

PIXEL_CONDICIONAL = """  <!-- Meta Pixel: so carrega com consentimento de marketing -->
  <script>
  window.carregarPixel = function(){
    if(window.fbq) return;
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', 'PIXEL_AQUI');
    fbq('track', 'PageView');
  };
  </script>
""".replace("PIXEL_AQUI", META_PIXEL)

antigo = re.search(r'  <!-- Meta Pixel -->\n  <script>\n.*?</script>\n', html, re.S)
if not antigo:
    falhas.append("pixel: nao encontrei o bloco para condicionar ao consentimento")
else:
    html = html.replace(antigo.group(0), PIXEL_CONDICIONAL)

# O <noscript> do pixel sai: dispara sem hipotese de perguntar.
ns = re.search(r'  <noscript><img height="1" width="1".*?</noscript>\n', html, re.S)
if not ns:
    falhas.append("pixel sem javascript: nao encontrei o <noscript> para remover")
else:
    html = html.replace(ns.group(0), "")

CONSENT_MODE = """  <!-- Consent Mode v2: tudo negado ate haver escolha -->
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  (function(){
    var guardado = null;
    try{ guardado = JSON.parse(localStorage.getItem('bb-cookies') || 'null'); }catch(e){}
    var valido = guardado && guardado.v === 1 &&
                 (Date.now() - guardado.quando) < 15552000000;   /* 6 meses */
    var analise   = valido && guardado.analise   ? 'granted' : 'denied';
    var marketing = valido && guardado.marketing ? 'granted' : 'denied';
    gtag('consent', 'default', {
      ad_storage: marketing,
      ad_user_data: marketing,
      ad_personalization: marketing,
      analytics_storage: analise,
      functionality_storage: 'granted',
      security_storage: 'granted',
      wait_for_update: 500
    });
  })();
  </script>
"""
html = troca(html, "  <!-- Google Tag Manager -->",
             CONSENT_MODE + "  <!-- Google Tag Manager -->", "consent mode antes do GTM")


# ══════════════════════════════════════════════════════════════════
# O AVISO DE COOKIES — marcacao, estilo e logica
# ══════════════════════════════════════════════════════════════════

AVISO_HTML = """<div class="ck" id="ck" role="dialog" aria-labelledby="ck-titulo" aria-describedby="ck-texto" hidden>
  <div class="ck-caixa">
    <div class="ck-corpo">
      <h2 class="ck-titulo" id="ck-titulo">Este site usa cookies</h2>
      <p class="ck-texto" id="ck-texto">Usamos cookies para perceber como a página é usada e para medir os nossos anúncios. Nada disto arranca sem a sua autorização. O formulário de contacto funciona de qualquer maneira.</p>
    </div>

    <div class="ck-opcoes" id="ck-opcoes" hidden>
      <label class="ck-linha ck-linha-fixa">
        <span class="ck-info"><span class="ck-nome">Necessários</span>
          <span class="ck-desc">Fazem a página funcionar e guardam esta escolha. Não podem ser desligados.</span></span>
        <span class="ck-sempre">Sempre ativos</span>
      </label>
      <label class="ck-linha">
        <span class="ck-info"><span class="ck-nome">Análise</span>
          <span class="ck-desc">Contam visitas e mostram que partes da página são lidas, para a sabermos melhorar.</span></span>
        <input type="checkbox" id="ck-analise" class="ck-switch">
      </label>
      <label class="ck-linha">
        <span class="ck-info"><span class="ck-nome">Marketing</span>
          <span class="ck-desc">Pixel do Meta. Mede os resultados dos anúncios e permite mostrar-lhe os nossos noutros sítios.</span></span>
        <input type="checkbox" id="ck-marketing" class="ck-switch">
      </label>
    </div>

    <div class="ck-botoes">
      <button type="button" class="ck-btn" data-ck="rejeitar">Rejeitar</button>
      <button type="button" class="ck-btn" data-ck="personalizar" id="ck-personalizar">Personalizar</button>
      <button type="button" class="ck-btn ck-btn-sim" data-ck="aceitar">Aceitar</button>
    </div>
    <p class="ck-rodape"><a href="https://bluebolt.pt/politica-de-cookies/" target="_blank" rel="noopener">Política de Cookies</a> &middot; <a href="https://bluebolt.pt/politica-de-privacidade/" target="_blank" rel="noopener">Política de Privacidade</a></p>
  </div>
</div>
"""

AVISO_JS = """
/* Consentimento de cookies. O que decide o que carrega está aqui; o
   Consent Mode, no <head>, trata do lado da Google. */
function iniciarCookies(){
  /* A marcação do aviso é inserida depois deste script, por isso à primeira
     passagem ainda não está no DOM. Espera-se que esteja. Função com nome e
     não `arguments.callee`, que é proibido em modo estrito. */
  var CHAVE = 'bb-cookies', VERSAO = 1, SEIS_MESES = 15552000000;
  var caixa = document.getElementById('ck');
  if(!caixa) return;
  var opcoes    = document.getElementById('ck-opcoes');
  var swAnalise = document.getElementById('ck-analise');
  var swMktg    = document.getElementById('ck-marketing');

  function lido(){
    try{
      var g = JSON.parse(localStorage.getItem(CHAVE) || 'null');
      if(g && g.v === VERSAO && (Date.now() - g.quando) < SEIS_MESES) return g;
    }catch(e){}
    return null;
  }

  function aplicar(escolha){
    /* O Consent Mode primeiro: é o que diz à Google o que pode fazer. */
    if(window.gtag){
      gtag('consent', 'update', {
        ad_storage:          escolha.marketing ? 'granted' : 'denied',
        ad_user_data:        escolha.marketing ? 'granted' : 'denied',
        ad_personalization:  escolha.marketing ? 'granted' : 'denied',
        analytics_storage:   escolha.analise   ? 'granted' : 'denied'
      });
    }
    /* O pixel do Meta não tem meio-termo: ou entra, ou não entra. E uma
       vez carregado não se descarrega — quem disser que não depois de ter
       dito que sim só fica sem ele na próxima visita. */
    if(escolha.marketing && window.carregarPixel) window.carregarPixel();

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'consentimento',
      consent_analise: !!escolha.analise,
      consent_marketing: !!escolha.marketing
    });
  }

  function guardar(analise, marketing){
    var escolha = { v: VERSAO, quando: Date.now(), analise: !!analise, marketing: !!marketing };
    try{ localStorage.setItem(CHAVE, JSON.stringify(escolha)); }catch(e){}
    aplicar(escolha);
    esconder();
  }

  function mostrar(){
    var g = lido();
    if(g){ swAnalise.checked = !!g.analise; swMktg.checked = !!g.marketing; }
    caixa.hidden = false;
  }
  function esconder(){ caixa.hidden = true; opcoes.hidden = true; }

  caixa.addEventListener('click', function(e){
    var b = e.target.closest('[data-ck]');
    if(!b) return;
    var q = b.getAttribute('data-ck');
    if(q === 'aceitar')  return guardar(true, true);
    if(q === 'rejeitar') return guardar(false, false);
    if(q === 'personalizar'){
      if(opcoes.hidden){
        opcoes.hidden = false;
        b.textContent = 'Guardar escolhas';
      } else {
        guardar(swAnalise.checked, swMktg.checked);
      }
    }
  });

  /* Para se poder mudar de ideias: o link no rodapé reabre isto. */
  window.abrirCookies = function(e){ if(e) e.preventDefault(); mostrar(); };

  var guardado = lido();
  if(guardado) aplicar(guardado); else mostrar();
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', iniciarCookies);
} else {
  iniciarCookies();
}
"""

# A logica do aviso e injectada no fim, com o resto do JS que acrescentamos.

# O link no rodape, para se poder mudar de ideias depois.
html = troca(
    html,
    'politica-de-cookies/" target="_blank" rel="noopener">Política de Cookies</a></li>',
    'politica-de-cookies/" target="_blank" rel="noopener">Política de Cookies</a></li>'
    '<li><a href="#" onclick="return abrirCookies(event)">Definições de cookies</a></li>',
    "link para reabrir as definicoes",
)


# ══════════════════════════════════════════════════════════════════
# O EVENTO DE LEAD
# O formulario e agora um iframe de outro dominio: nao se lhe pode pendurar
# um `onsubmit`. O que da e ouvir o que ele grita para a pagina ao submeter.
#
# ATENCAO, ISTO PRECISA DE UMA SUBMISSAO DE TESTE. O formato da mensagem
# que o Go High Level envia nao esta documentado e o script deles vem
# minificado — nao o adivinhei. O ouvinte aceita varias formas conhecidas e
# escreve na consola tudo o que chega do dominio deles, para se ver o que e
# que aparece de facto. Confirmar no Test Events do Events Manager.
#
# E SE LIGAREM O PIXEL DENTRO DO CRM, DESLIGUEM ISTO. O Go High Level tem
# integracao propria com o Meta; com as duas ligadas, cada lead e contada
# duas vezes.
# ══════════════════════════════════════════════════════════════════

OUVINTE_LEAD = """
/* Evento de Lead vindo do formulário do CRM. Ver a nota no build.py. */
(function(){
  var ORIGEM = 'https://api.leadconnectorhq.com';
  var jaDisparou = false;

  function pareceSubmissao(d){
    if(!d) return false;
    var t = (typeof d === 'string') ? d : (d.type || d.event || d.action || '');
    return /submit|submission|form-?sent|thank/i.test(String(t));
  }

  window.addEventListener('message', function(e){
    if(e.origin !== ORIGEM) return;
    /* Deixado de propósito: é isto que diz qual é a forma verdadeira da
       mensagem, na primeira submissão a sério. */
    try{ console.debug('[crm]', JSON.stringify(e.data).slice(0,300)); }catch(err){}

    if(jaDisparou || !pareceSubmissao(e.data)) return;
    jaDisparou = true;

    var eid = 'lead-' + Date.now() + '-' + Math.random().toString(16).slice(2);
    if(window.fbq){
      fbq('track', 'Lead', {
        content_name: 'Diagnóstico gratuito de 30 minutos',
        content_category: 'formulario'
      }, { eventID: eid });
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'lead_enviada', event_id: eid });
  });
})();
"""

# O ouvinte e injectado no fim, com o resto do JS que acrescentamos.

# O nosso tratador de formulario deixa de ter formulario para tratar.
antigo = re.search(
    r'/\* Submissão do formulário de lead.*?\nfunction handleLeadSubmit\(e\)\{.*?\n\}\n',
    html, re.S)
if not antigo:
    falhas.append("tratador do formulario antigo: nao encontrei para remover")
else:
    html = html.replace(antigo.group(0), "")

# ══════════════════════════════════════════════════════════════════
# O JS QUE ACRESCENTAMOS VAI NUM <script> SO DELE
# Estava a ser enfiado antes do ultimo `</script>` da pagina — mas o
# ultimo passou a ser o `<script src=...form_embed.js>` do CRM, e um
# `<script>` com `src` ignora o que tenha la dentro. O ouvinte do
# formulario e o aviso de cookies ficaram no ficheiro, visiveis no codigo
# fonte, e nunca correram. A tag propria tira a duvida de vez.
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    "</body>",
    AVISO_HTML + "<script>\n" + OUVINTE_LEAD + "\n" + AVISO_JS + "</script>\n</body>",
    "marcacao e logica do aviso de cookies, e ouvinte do formulario",
)

# ══════════════════════════════════════════════════════════════════

if falhas:
    print("SUBSTITUIÇÕES FALHADAS:", file=sys.stderr)
    for f in falhas:
        print("  -", f, file=sys.stderr)
    sys.exit(1)

open(PAGE, "w", encoding="utf-8").write(html)
print(f"index.html reescrito: {len(html):,} bytes")

# ══════════════════════════════════════════════════════════════════
# AS DUAS PAGINAS: /meta/ e /google/
# A mesma pagina em dois enderecos, um para cada canal, para o trafego e
# as conversoes de cada plataforma se medirem em separado.
#
# Nao sao duas copias: sao geradas da mesma construcao, e as imagens, o
# CSS e as fontes ficam uma so vez na raiz. As duas paginas apontam para
# `../img/` e `../assets/`. Sao 8MB que nao se duplicam, e trocar uma
# imagem serve as duas.
#
# Estrutura a subir para o public_html da Hostinger:
#
#   public_html/
#     index.html          ← a pagina solta, se for precisa
#     meta/index.html
#     google/index.html
#     img/  assets/  archia-regular.woff2  archia-regular.woff
#
# NOTA SOBRE O GOOGLE: duas paginas iguais em dois enderecos sao conteudo
# duplicado. Enquanto o `robots` estiver em `noindex` nao ha problema —
# e e assim que se costuma deixar uma pagina de campanha paga, que nao se
# quer a competir nos resultados organicos. Se alguma vez for para
# indexar, uma delas tem de levar `canonical` a apontar para a outra.
# ══════════════════════════════════════════════════════════════════

# Subdominio proprio, de segundo nivel. Nao e o agencia.bluebolt.pt porque
# esse ja tem um WordPress em cima, e nao e lp.agencia.bluebolt.pt porque um
# wildcard *.bluebolt.pt nao chega a terceiro nivel e o certificado dava
# trabalho. A verificacao de dominio do Meta Business Manager tambem abrange
# subdominios: se o bluebolt.pt ja esta verificado, este herda-o.
DOMINIO = "https://sessaoestrategica.bluebolt.pt"

CANAIS = {
    "meta":   "Meta Ads",
    "google": "Google Ads",
}

# O formulario do CRM tem um campo escondido "LandingPage" com a chave de
# query `landingpage` (visto no HTML do proprio widget: data-q="landingpage").
# Sem lhe passar nada, o campo vai vazio e o CRM mostra o texto de exemplo
# — que ainda por cima traz um dominio que ja nao existe. Passando-lhe o
# valor no endereco do iframe, cada lead chega a dizer de onde veio.
FORMULARIO_BASE = f"https://api.leadconnectorhq.com/widget/form/{FORMULARIO_CRM}"


def origem_do_canal(canal, rotulo):
    """O que aparece no campo Origem do CRM. Curto de proposito: quem olha
    para a ficha quer ler "Google Ads", nao um endereco."""
    return rotulo


def pagina_do_canal(base_html, canal, rotulo):
    """A mesma pagina, um nivel mais abaixo e marcada com o canal."""
    h = base_html

    # 1. Os caminhos sobem um nivel. Sao poucos e todos na raiz da lp-v2:
    #    img/, img/testemunhos/, assets/ e as duas fontes.
    for antes, depois in (
        ('="img/', '="../img/'),
        ('="assets/', '="../assets/'),
        ("url('img/", "url('../img/"),
        ("url('archia-regular.", "url('../archia-regular."),
    ):
        if antes not in h:
            falhas.append(f"{canal}: nao encontrei o caminho {antes!r} para reescrever")
        h = h.replace(antes, depois)

    # 2. A origem que vai para o CRM, no endereco do formulario.
    origem = origem_do_canal(canal, rotulo)
    if f'src="{FORMULARIO_BASE}"' not in h:
        falhas.append(f"{canal}: nao encontrei o iframe do formulario para marcar a origem")
    h = h.replace(
        f'src="{FORMULARIO_BASE}"',
        f'src="{FORMULARIO_BASE}?landingpage={urllib.parse.quote(origem)}"',
    )

    # 3. O endereco proprio, para as partilhas e para o dia em que deixar
    #    de estar em `noindex`.
    h = h.replace('<link rel="canonical" href="https://bluebolt.pt/ai">',
                  f'<link rel="canonical" href="{DOMINIO}/{canal}/">')
    h = h.replace('<meta property="og:url" content="https://bluebolt.pt/ai/ads">',
                  f'<meta property="og:url" content="{DOMINIO}/{canal}/">')

    # 4. A mesma origem, agora tambem na query string da propria pagina.
    #    O form_embed.js do GHL le o `window.top.location.search` — a query
    #    da PAGINA, nao a do iframe — e e essa que reencaminha para dentro
    #    do formulario. So no endereco do iframe podia nao chegar la.
    #    O `replaceState` nao recarrega nada e corre antes de o embed
    #    arrancar. Se a pessoa ja vier com `landingpage` no endereco (nao
    #    deve acontecer), respeita-se o que vier.
    h = h.replace(
        "  <!-- Google Tag Manager -->",
        "  <script>(function(){try{"
        "var u=new URL(location.href);"
        "if(!u.searchParams.has('landingpage')){"
        f"u.searchParams.set('landingpage','{origem}');"
        "history.replaceState(null,'',u);}"
        "}catch(e){}})();</script>\n"
        "  <!-- Google Tag Manager -->",
        1,
    )

    # 5. O canal no dataLayer, antes de o GTM arrancar: assim a primeira
    #    visualizacao ja o traz e o GA4 consegue separar os dois sem
    #    depender de a UTM ter sido posta no anuncio.
    h = h.replace(
        "  <!-- Google Tag Manager -->",
        f"  <script>window.dataLayer=window.dataLayer||[];"
        f"dataLayer.push({{canal:'{canal}',canal_nome:'{rotulo}'}});</script>\n"
        "  <!-- Google Tag Manager -->",
    )
    return h


for canal, rotulo in CANAIS.items():
    pasta = os.path.join(os.path.dirname(PAGE), canal)
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, "index.html")
    open(destino, "w", encoding="utf-8").write(pagina_do_canal(html, canal, rotulo))
    print(f"{canal}/index.html reescrito: {len(html):,} bytes")


restos = [t for t in ("Equipa de IA", "agentes de IA", "bluebolt-ai-brand", "ricardo.webp") if t in html]
fora_da_seccao_ricardo = [t for t in restos if t not in ("Equipa de IA",)]
print("menções a IA restantes (secção do Ricardo incluída):", html.count("IA"))

# ══════════════════════════════════════════════════════════════════
# A PAGINA DE OBRIGADO
# O formulario do CRM redireciona ao submeter. Estava a mandar para
# lp.blueboltagency.pt/obrigado/ — existe e funciona, mas e outro dominio,
# e isso custa duas coisas:
#
#   O evento de Lead do pixel. O ouvinte da pagina espera uma mensagem do
#   iframe, mas a pagina navega para fora antes — e uma corrida que se
#   perde. Numa pagina de obrigado propria o Lead dispara no carregamento:
#   deterministico, sem depender de mensagens que o GHL nao documenta.
#
#   A atribuicao. Saltar de dominio faz o GA4 abrir sessao nova com
#   origem "referral", e perde-se a campanha que gerou a conversao.
#
# E a pagina mais simples do sitio de proposito: quem chega aqui ja
# converteu, e o unico trabalho que lhe resta e marcar a hora.
# ══════════════════════════════════════════════════════════════════

OBRIGADO_HTML = """<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Obrigado | Blue Bolt Agency</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../img/bluebolt-logo.webp">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700&display=swap" rel="stylesheet">
CABECA_MARCACAO
<style>
@font-face{font-family:'Archia';src:url('../archia-regular.woff2') format('woff2'),url('../archia-regular.woff') format('woff');font-weight:400;font-style:normal;font-display:swap}
*{box-sizing:border-box}
body{
  margin:0;min-height:100vh;
  display:flex;align-items:center;justify-content:center;
  padding:clamp(1.5rem,5vw,3rem);
  background:#000122;color:#fff;
  font-family:'Manrope',system-ui,sans-serif;
  text-align:center;
}
/* O mesmo halo azul do topo da VSL: e o que liga esta pagina a de onde se veio. */
body::before{
  content:'';position:fixed;inset:0;pointer-events:none;
  background:radial-gradient(70% 55% at 50% 22%, rgba(47,161,255,.16), transparent 70%);
}
.ob{position:relative;max-width:560px}
.ob-logo{height:34px;width:auto;margin-bottom:2.5rem;opacity:.9}
.ob-selo{
  width:64px;height:64px;margin:0 auto 1.75rem;
  display:flex;align-items:center;justify-content:center;
  border-radius:50%;
  background:rgba(47,161,255,.12);
  border:1px solid rgba(47,161,255,.35);
}
.ob-selo svg{width:30px;height:30px;stroke:#2fa1ff;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
h1{
  font-family:'Archia',sans-serif;
  font-size:clamp(28px,4.4vw,40px);font-weight:600;
  letter-spacing:-.03em;line-height:1.15;margin:0 0 1rem;
}
.ob-sub{font-size:clamp(15px,1.5vw,17px);line-height:1.75;font-weight:300;color:rgba(255,255,255,.72);margin:0 0 2.5rem}
.ob-passo{
  display:flex;gap:1rem;text-align:left;
  padding:1.1rem 1.25rem;margin-bottom:.75rem;
  border:1px solid rgba(255,255,255,.12);border-radius:14px;
  background:rgba(255,255,255,.03);
}
.ob-num{
  flex:0 0 auto;width:26px;height:26px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:rgba(47,161,255,.15);color:#6cc0ff;
  font-size:12.5px;font-weight:700;
}
.ob-passo p{margin:0;font-size:14.5px;line-height:1.6;font-weight:300;color:rgba(255,255,255,.75)}
.ob-passo strong{color:#fff;font-weight:600}
.ob-fim{margin:2.5rem 0 0;font-size:13px;color:rgba(255,255,255,.45)}
.ob-fim a{color:rgba(255,255,255,.7)}
@media(max-width:600px){ .ob-passo{padding:1rem} }
</style>
</head>
<body>
<div class="ob">
  <img class="ob-logo" src="../img/bluebolt-lockup.webp" alt="Blue Bolt Agency" width="300" height="287" style="height:34px;width:auto">
  <div class="ob-selo" aria-hidden="true">
    <svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>
  </div>
  <h1>Recebemos o seu pedido.</h1>
  <p class="ob-sub">Falta um passo para o diagnóstico ficar marcado.</p>

  <div class="ob-passo">
    <span class="ob-num">1</span>
    <p><strong>Vá ao seu email.</strong> Acabámos de lhe enviar uma mensagem com o link para escolher o horário que lhe dá jeito.</p>
  </div>
  <div class="ob-passo">
    <span class="ob-num">2</span>
    <p><strong>Escolha a hora.</strong> São 30 minutos, por videochamada. Se não estiver na caixa de entrada, veja no spam ou nas promoções.</p>
  </div>
  <div class="ob-passo">
    <span class="ob-num">3</span>
    <p><strong>Traga os números que tiver.</strong> Quanto gasta em anúncios e quantos clientes entram por mês chega para começarmos com coisas concretas.</p>
  </div>

  <p class="ob-fim">Alguma coisa correu mal? Escreva para <a href="mailto:geral@bluebolt.pt">geral@bluebolt.pt</a>.</p>
</div>
CORPO_MARCACAO
</body>
</html>
"""


def pagina_obrigado(base_html):
    """Leva a marcacao da pagina principal, para o Lead e a conversao
    dispararem aqui — que e o unico sitio onde se sabe, de certeza, que a
    submissao chegou ao fim."""
    consent = re.search(r'  <!-- Consent Mode v2.*?</script>\n', base_html, re.S)
    gtm     = re.search(r'  <!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->\n', base_html, re.S)
    pixel   = re.search(r'  <!-- Meta Pixel.*?</script>\n', base_html, re.S)
    gtmbody = re.search(r'<!-- Google Tag Manager \(noscript\).*?<!-- End Google Tag Manager -->\n', base_html, re.S)
    if not all((consent, gtm, pixel, gtmbody)):
        falhas.append("pagina de obrigado: nao encontrei os blocos de marcacao para copiar")
        return None

    cabeca = (consent.group(0) + gtm.group(0) + pixel.group(0)).replace("../", "../").replace('href="img/', 'href="../img/')
    corpo = gtmbody.group(0) + """<script>
/* A conversao dispara aqui, no carregamento: quem chega a esta pagina
   submeteu mesmo. Nao ha mensagens de iframe a adivinhar nem corridas
   com o redireccionamento. */
(function(){
  var eid = 'lead-' + Date.now() + '-' + Math.random().toString(16).slice(2);
  function marcar(){
    if(window.fbq){
      fbq('track', 'Lead', {
        content_name: 'Diagnóstico gratuito de 30 minutos',
        content_category: 'formulario'
      }, { eventID: eid });
    }
  }
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event: 'lead_enviada', event_id: eid });

  /* O pixel só existe se houve consentimento de marketing; a pagina
     anterior guardou a escolha no mesmo dominio, por isso le-se aqui. */
  try{
    var g = JSON.parse(localStorage.getItem('bb-cookies') || 'null');
    if(g && g.marketing && window.carregarPixel){ window.carregarPixel(); }
  }catch(e){}
  setTimeout(marcar, 400);
})();
</script>
"""
    h = OBRIGADO_HTML.replace("CABECA_MARCACAO", cabeca.rstrip()).replace("CORPO_MARCACAO", corpo.rstrip())
    return h


_ob = pagina_obrigado(html)
if _ob:
    pasta = os.path.join(os.path.dirname(PAGE), "obrigado")
    os.makedirs(pasta, exist_ok=True)
    open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(_ob)
    print(f"obrigado/index.html reescrito: {len(_ob):,} bytes")
