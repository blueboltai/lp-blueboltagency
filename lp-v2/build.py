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

.hero-wrap{ background:#03113a; }

.hero-bg-video{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  z-index:1;
  pointer-events:none;
}
/* Veu por cima do video: o texto tem de ganhar sempre ao fotograma. */
/* O veu deixou de ser preto-azulado e passou a azul: o fundo acende sem
   deixar de garantir o contraste do texto sobre o fotograma do video. A
   ultima paragem volta ao #000122 para a base do hero continuar a fechar
   contra o halo da VSL. */
.hero-bg-veil{
  position:absolute;
  inset:0;
  z-index:2;
  pointer-events:none;
  background:
    /* O clarao fica a meia altura, por baixo do texto: acende o azul onde
       ha espaco livre e deixa a zona do titulo com bed escuro que baste. */
    radial-gradient(76% 50% at 50% 60%, rgba(30,120,232,.5) 0%, rgba(10,52,128,.3) 46%, rgba(3,17,58,0) 80%),
    linear-gradient(180deg, rgba(1,13,50,.84) 0%, rgba(1,15,56,.74) 40%, rgba(0,9,42,.84) 82%, #000122 100%);
}
/* Os halos ganham corpo, agora que o fundo os aguenta. */
.hero-orb{ z-index:3; }
.hero-orb-1{ background:radial-gradient(circle,rgba(47,161,255,.3) 0%,transparent 70%); }
.hero-orb-2{ background:radial-gradient(circle,rgba(47,161,255,.18) 0%,transparent 70%); }
#hero{ z-index:5; }
.hero-overlay-bottom{
  z-index:4;
  height:260px;
  background:linear-gradient(to top,#000122 0%,transparent 100%);
}

/* Tipografia: a da propria pagina — Archia nos titulos, Manrope no corpo.
   So se mexe na medida e na cor, que o hero centrado e o video por tras
   obrigam a ajustar; os tipos de letra e os pesos ficam como estavam. */
.hero-h1{
  font-size:clamp(30px,4.2vw,58px);
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
:root{ --medida-titulo: min(1020px, 100vw - 48px); }
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
  max-width:60ch;
  margin-inline:auto;
  margin-bottom:2.25rem;
}

/* ══ Credenciais no rodape ══
   Em repouso ficam quase apagadas — leem-se como uma nota de rodape, nao
   como um bloco de logotipos. Ao passar o rato recuperam a cor toda. */
.ft-creds{
  display:flex;
  align-items:center;
  flex-wrap:wrap;
  gap:clamp(16px,3vw,36px);
  padding:30px 0;
  border-bottom:1px solid rgba(255,255,255,.06);
}
.ft-creds-label{
  font-family:'Manrope',sans-serif;
  font-size:9px;
  font-weight:500;
  letter-spacing:.24em;
  text-transform:uppercase;
  color:rgba(255,255,255,.26);
  white-space:nowrap;
}
.ft-creds-row{
  display:flex;
  align-items:center;
  flex-wrap:wrap;
  gap:clamp(14px,2.4vw,28px);
}
.ft-cred{
  height:60px;
  width:auto;
  object-fit:contain;
  opacity:.72;
  filter:grayscale(.3);
  transition:opacity .35s ease, filter .35s ease;
}
.ft-cred:hover,
.ft-cred:focus-visible{
  opacity:1;
  filter:none;
}
.light-theme .ft-creds{ border-bottom-color:rgba(10,15,35,.09); }
.light-theme .ft-creds-label{ color:rgba(10,15,35,.38); }

@media(max-width:640px){
  .ft-creds{ gap:14px;padding:24px 0; }
  .ft-cred{ height:46px; }
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
  max-width:min(980px,100%);
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
  font-size:16px;
  font-weight:300;
  line-height:1.75;
  color:var(--lt-inc-2);
  max-width:64ch;
  margin-inline:auto;
}
.prob-bio strong{ color:var(--lt-inc);font-weight:600; }
/* A frase de fecho fecha o texto, nao e uma caixa: ganha corpo e cor, e
   a unica marca que leva e um filete da cor da marca do lado esquerdo. */
.prob-callout{
  margin:2rem auto 0;
  max-width:60ch;
  padding:.1rem 0 .1rem 1.5rem;
  border-left:2px solid var(--accent-light);
  font-family:'Manrope',sans-serif;
  font-size:19px;
  font-weight:500;
  line-height:1.6;
  letter-spacing:-.01em;
  color:var(--lt-inc);
  text-align:left;
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
.funil-passos{ list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.4rem; }
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
  .funil-img{ max-width:320px; }
}

/* ══════════════════════════════════════════════════════════════════
   A LINHA DO TEMPO — em lista, nao em ziguezague
   O desenho alternado deixava, a qualquer altura, mais de metade da
   seccao em preto: cinco passos a ocupar 1600px para dizer o que cabe em
   550. Os passos passam a linhas de largura toda — numero, etiqueta e
   titulo a esquerda, texto a direita — separadas por um filete, com o
   carril a esquerda a encher conforme se desce. Continua a ser a linha do
   tempo; deixa de ser um ziguezague com o dobro do espaco vazio.
   ══════════════════════════════════════════════════════════════════ */

#trajetoria .traj-list{
  max-width:var(--medida-titulo);
  margin-inline:calc(50% - var(--medida-titulo) / 2);
  min-height:0;
}
/* O carril passa da coluna do meio para a esquerda, ao pe dos numeros. */
#trajetoria .traj-list::before,
#trajetoria .traj-progress-line{ left:23px;transform:none; }
#trajetoria .traj-progress-dot{ left:50%;transform:translateX(-50%); }

#trajetoria .traj-item{
  display:grid;
  grid-template-columns:70px minmax(0,1fr);
  gap:0;
  align-items:start;
  margin-bottom:0;
  padding:clamp(1.4rem,2.4vw,1.9rem) 0;
  border-bottom:1px solid rgba(255,255,255,.06);
  opacity:.5;
  filter:none;
  transition:opacity .55s ease;
}
#trajetoria .traj-item:first-child{ padding-top:0; }
#trajetoria .traj-item:last-child{ border-bottom:0; }
#trajetoria .traj-item.active{ opacity:1; }
#trajetoria .traj-item::before{ display:none; }
/* A entrada vinha de lado, do tempo em que os passos alternavam esquerda e
   direita. Numa lista alinhada isso lia-se como desalinhamento; sobe. */
#trajetoria .traj-item:nth-child(odd) .traj-content,
#trajetoria .traj-item:nth-child(even) .traj-content{ transform:translateY(12px); }
#trajetoria .traj-item.active .traj-content{ transform:none; }

/* O no, no carril */
.traj-no{
  grid-column:1;
  grid-row:1;
  justify-self:start;
  align-self:start;
  margin-top:-4px;
  width:46px;height:46px;
  display:grid;
  place-items:center;
  border-radius:50%;
  /* opaco de proposito: e ele que corta o carril por tras */
  background:#070a16;
  border:1px solid rgba(255,255,255,.1);
  position:relative;
  z-index:3;
  transition:border-color .45s ease, box-shadow .45s ease, background .45s ease;
}
.traj-no span{
  font-family:'Archia',sans-serif;
  font-size:15px;
  letter-spacing:-.02em;
  color:rgba(255,255,255,.42);
  transition:color .45s ease;
}
.traj-item.active .traj-no{
  border-color:rgba(47,161,255,.5);
  background:radial-gradient(120% 120% at 50% 0%, rgba(47,161,255,.22), #070a16 70%);
  box-shadow:0 0 0 4px rgba(47,161,255,.07), 0 0 22px rgba(47,161,255,.28);
}
.traj-item.active .traj-no span{ color:#fff; }

/* A direita do numero, duas colunas: etiqueta e titulo numa, texto na
   outra. A linha fica com a altura do que la esta dentro — era o segundo
   `row` implicito do titulo que abria o vazio por baixo de cada passo. */
#trajetoria .traj-content{
  grid-column:2;
  grid-row:1;
  display:grid;
  grid-template-columns:minmax(0,290px) minmax(0,1fr);
  grid-template-rows:auto auto;
  column-gap:clamp(1.5rem,3vw,3rem);
  align-items:start;
  text-align:left;
  padding:0;
}
#trajetoria .traj-year{ grid-column:1;grid-row:1;margin-bottom:.4rem; }
#trajetoria .traj-tag{ display:none; }
#trajetoria .traj-title{
  grid-column:1;
  grid-row:2;
  font-size:clamp(17px,1.5vw,21px);
  margin:0;
}
#trajetoria .traj-desc{
  grid-column:2;
  grid-row:1 / span 2;
  max-width:none;
  margin:0;
  font-size:14px;
  line-height:1.7;
  color:rgba(200,204,216,.6);
}

@media(max-width:820px){
  #trajetoria .traj-item{ grid-template-columns:52px minmax(0,1fr); }
  #trajetoria .traj-content{ grid-template-columns:1fr;grid-template-rows:auto auto auto; }
  #trajetoria .traj-desc{ grid-column:1;grid-row:3;margin-top:.55rem; }
  #trajetoria .traj-list::before,
  #trajetoria .traj-progress-line{ left:19px; }
  .traj-no{ width:38px;height:38px; }
  .traj-no span{ font-size:13px; }
}

/* ══ Prova social, por baixo do botao do hero ══
   Retratos da equipa em pilha, com um aro da cor do fundo a separa-los —
   e o aro que faz a pilha ler-se como pessoas e nao como mancha. */
/* Sem capsula: os retratos e a frase chegam para se lerem como um bloco,
   e sem a moldura o hero fica com menos uma caixa a competir com o botao. */
.hero-prova{
  display:inline-flex;
  align-items:center;
  gap:.85rem;
  margin-top:1.75rem;
}
.hero-prova-caras{ display:inline-flex; }
.hero-prova-caras img{
  width:38px;height:38px;
  border-radius:50%;
  object-fit:cover;
  border:2px solid #0a0f24;
  background:#0a0f24;
}
.hero-prova-caras img + img{ margin-left:-13px; }
.hero-prova-txt{
  font-family:'Manrope',sans-serif;
  font-size:14px;
  font-weight:400;
  color:rgba(255,255,255,.76);
  white-space:nowrap;
}
.hero-prova-txt strong{ font-weight:700;color:#fff; }

@media(max-width:640px){
  .hero-prova{ gap:.6rem; }
  .hero-prova-caras img{ width:32px;height:32px; }
  .hero-prova-caras img + img{ margin-left:-11px; }
  .hero-prova-txt{ font-size:12.5px;white-space:normal;text-align:left; }
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
.tst-h2{
  font-family:'Archia',sans-serif;
  font-size:clamp(26px,3.1vw,40px);
  font-weight:400;
  letter-spacing:-.035em;
  line-height:1.14;
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

/* O botao do hero passa a claro. Na dobra escura e o branco que salta;
   no CTA final, que esta sobre fundo claro, o azul continua a ser o certo. */
#hero .cta-btn-main{
  background:linear-gradient(to bottom,#fff 0%,rgba(255,255,255,.95) 55%,rgba(255,255,255,.72) 100%);
  border-color:rgba(255,255,255,.5);
  color:#08101f;
  box-shadow:0 14px 38px rgba(0,0,0,.42), 0 0 0 1px rgba(255,255,255,.12);
  transition:transform .25s cubic-bezier(.16,1,.3,1), padding .5s cubic-bezier(.16,1,.3,1), box-shadow .3s;
}
#hero .cta-btn-main:hover{ transform:scale(1.035); }
#hero .cta-btn-main:active{ transform:scale(.98); }
#hero .cta-btn-text{ color:#08101f; }
#hero .cta-btn-circle{ background:#08101f;color:#fff; }
#hero .cta-btn-circle svg{ color:#fff; }

/* Halo por tras da VSL: e o que faz o video ler-se como um ecra aceso em
   vez de um rectangulo colado ao fundo. */
.vsl-straddle{ position:relative; }
.vsl-straddle::before{
  content:'';
  position:absolute;
  left:50%;
  top:-190px;
  /* O terceiro termo e o que evita transbordo horizontal: sem ele o halo
     empurrava a pagina 150px para o lado em ecras medios. */
  width:min(1240px, 150%, calc(100vw - 32px));
  height:420px;
  transform:translateX(-50%);
  background:
    radial-gradient(46% 52% at 50% 62%, rgba(120,200,255,.5) 0%, rgba(47,161,255,.22) 38%, rgba(47,161,255,0) 70%),
    radial-gradient(60% 60% at 50% 55%, rgba(0,93,169,.42) 0%, rgba(0,93,169,0) 72%);
  filter:blur(26px);
  pointer-events:none;
  z-index:0;
}
.vsl-shell{ position:relative;z-index:1; }

@media(max-width:860px){
  .vsl-straddle::before{ top:-120px;height:280px; }
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
#trajetoria,
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
.auth-section{ padding-top:calc(var(--ritmo) * .75); }

@media(max-width:640px){
  .hero-h1{ font-size:clamp(26px,7.6vw,36px); }
  .hero-sub{ font-size:14.5px; }
}
@media(prefers-reduced-motion:reduce){
  .hero-bg-video{ display:none; }
}
"""


# ══════════════════════════════════════════════════════════════════
# O FUNIL EM AMPULHETA
# E o desenho da propria Blue Bolt, feito na Canva. Chegou como imagem e
# como imagem fica — cheguei a redesenha-lo em SVG, mas o pedido foi usar
# o original. O PNG de 1080x1350 ja vinha com fundo transparente: so foi
# recortada a margem vazia e reduzido para 760px de largura (o dobro dos
# ~380 a que aparece, para ficar nitido em ecra retina). Em webp com alfa
# passa de 721KB a 75KB.
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
    return (f'<img class="funil-img" src="img/funil-canva.webp" width="760" height="1121" '
            f'alt="{_ARIA}" loading="lazy" decoding="async">')


def funil_passos():
    """As seis etapas em texto, ao lado do funil."""
    itens = []
    for i, (nome, desc, cor) in enumerate(FATIAS):
        itens.append(
            f'<li class="passo" style="--i:{i};--cor:{cor}">'
            f'<span class="passo-n">{i + 1:02d}</span>'
            f'<span class="passo-txt"><strong>{nome}</strong>{desc}</span>'
            f"</li>"
        )
    return '<ol class="funil-passos">' + "".join(itens) + "</ol>"

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
        <p>O digital não é barato nem fácil, e qualquer agência que diga o contrário está a vender o que quer ouvir, não o que precisa de saber.</p>
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
# A LINHA DO TEMPO — o numero deixa de ser um fantasma na coluna vazia
# e passa a ser o no que a linha de progresso atravessa.
# ══════════════════════════════════════════════════════════════════

n_nos = len(re.findall(r'<div class="traj-photo-wrap">\s*<div class="traj-date-panel">\s*'
                       r'<div class="traj-date-panel-day">\d+</div>\s*</div>\s*</div>', html))
if n_nos != 5:
    falhas.append(f"linha do tempo: esperava 5 numeros, encontrei {n_nos}")
html = re.sub(
    r'<div class="traj-photo-wrap">\s*<div class="traj-date-panel">\s*'
    r'<div class="traj-date-panel-day">(\d+)</div>\s*</div>\s*</div>',
    lambda m: f'<div class="traj-no"><span>{m.group(1)}</span></div>',
    html,
)

# O ultimo passo so acendia depois de a seccao ja ter saido do ecra: a
# barra de progresso conta a altura toda da lista, mas o gatilho ficava
# em idx/total. Comprimindo a escala, os cinco passos acendem dentro da
# seccao, que e onde se esta a olhar.
html = troca(
    html,
    "var threshold = (idx / total) + 0.02;",
    "var threshold = (idx / total) * 0.8;",
    "gatilho dos passos da linha do tempo",
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
    ("8QXWiBi7Z8I", "capa-auto-avenida-scaled-1.webp", "Luís Novais", "Auto Avenida"),
    ("qbhpgXOUC9I", "capa-infante-scaled-1.webp", "Dr. Marco Infante da Câmara", "Infante da Câmara"),
    ("LbNL0YDUDdI", "capa-apametal-scaled-1.webp", "Rita Rodrigues", "Apametal"),
    ("kl3K2hbLHmk", "capa-foot-draft-scaled-1.webp", "Bruno Pinto", "Foot Draft"),
    ("pl0ah13B-CY", "capa-carmen-scaled-1.webp", "Carmen Ferreira", "Enfermagem"),
    ("8XSuQEaG17U", "capa-mecia-scaled-1.webp", "Mécia Correia", "Marca pessoal"),
]
# Ficam seis, em duas filas de tres. Os outros dois testemunhos que temos —
# Natália Teixeira e Sara Moreira — sao ambos de marca pessoal, que ja esta
# representada; sairam para a fila nao ficar a dois.

_cartoes = "".join(
    f'<figure class="tst-card">'
    f'<div class="vsl-screen tst-screen" data-video="{vid}" role="button" tabindex="0" '
    f'aria-label="Ver o testemunho de {nome}">'
    f'<img src="img/testemunhos/{capa}" alt="" decoding="async" fetchpriority="low">'
    f'<span class="vsl-play" aria-hidden="true">'
    f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'
    f"</div>"
    f'<figcaption class="tst-cap"><span class="tst-nome">{nome}</span>'
    f'<span class="tst-area">{area}</span></figcaption>'
    f"</figure>"
    for vid, capa, nome, area in TESTEMUNHOS
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
html = troca(html, 'src="ricardo.webp"', 'src="img/ricardo.webp"', "foto do Ricardo")

# ══════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════


html = troca(
    html,
    '<span class="t1">A sua equipa perde horas todos os dias em trabalho que </span><span class="t2">a IA já poderia fazer sozinha.</span>',
    '<span class="t1">Transforme o que investe em anúncios em </span>'
    '<span class="t2">faturação que consegue ver e explicar</span>',
    "h1",
)
html = troca(
    html,
    "Automatize processos, aumente produtividade e reduza custos com agentes de IA implementados à medida da sua operação, para que a tecnologia se adapte ao seu negócio e não o contrário.",
    "Com um Sistema Previsível de Aquisição de Clientes, sabe todos os meses onde o dinheiro se perdeu, onde gerou oportunidades e onde se transformou em clientes.",
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

  <!-- Vídeo de fundo (o mesmo do modelo do Elementor) -->
  <video class="hero-bg-video" autoplay muted loop playsinline preload="none"
         poster="img/hero-poster.jpg" aria-hidden="true">
    <source src="img/hero-video.webm" type="video/webm">
  </video>
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

# ── Prova social por baixo do botao ─────────────────────────────────
# Retratos da propria equipa da Blue Bolt, os mesmos do site. Sao seis:
# mais do que isso e a pilha deixa de se ler e passa a mancha.
EQUIPA = ["andreia", "bruno", "daniela", "mariana", "hugo", "diego"]
CARAS = "".join(
    f'<img src="img/prova/{n}.avif" alt="" width="38" height="38" loading="lazy" decoding="async">'
    for n in EQUIPA
)
html = troca(
    html,
    "</div>\n\n      </div>\n    </div>\n  </section>",
    '</div>\n\n        <div class="hero-prova" data-reveal="fade">\n'
    f'          <span class="hero-prova-caras" aria-hidden="true">{CARAS}</span>\n'
    '          <span class="hero-prova-txt"><strong>+400</strong> negócios transformados</span>\n'
    '        </div>\n\n      </div>\n    </div>\n  </section>',
    "prova social do hero",
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
  box-shadow:0 30px 75px rgba(0,0,0,.9),0 0 55px rgba(47,161,255,.15);
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

html = troca(html, "</style>", VSL_CSS + NAV_CSS + SECOES_CSS + "</style>", "CSS da VSL, do hero e das secções")
html = troca(html, '\n<!-- QUEM É -->', VSL_HTML + '\n<!-- QUEM É -->', "marcacao da VSL")
html = troca(html, "\n/* Submissão do formulário de lead", VSL_JS + "\n/* Submissão do formulário de lead", "JS da VSL")

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
# COMO FUNCIONA — cinco passos
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<span class="tg">Da primeira conversa ao </span><span class="ta">piloto automático.</span>',
    '<span class="tg">Da primeira conversa ao </span><span class="ta">primeiro cliente fechado.</span>',
    "h2 do processo",
)

PASSOS = [
    (
        "Diagnóstico",
        "Diagnóstico e Mapa de Automação",
        "Analisamos a sua operação e identificamos onde a IA poupa mais tempo e dinheiro. É por aqui que começamos, sem custo.",
        "Diagnóstico",
        "Diagnóstico e estrutura",
        "Antes de investir um euro em anúncios, analisamos o negócio, a oferta, o processo comercial e onde estão os pontos de perda. Não começamos sem perceber o que já existe.",
    ),
    (
        "Desenho",
        "Desenho do Motor de IA",
        "Desenhamos o sistema de agentes e automações à medida do seu negócio e das ferramentas que já usa.",
        "Atração",
        "Atração de leads qualificadas",
        "Campanhas em Meta Ads e Google Ads orientadas a conversão. Criativos, copy e segmentação pensados para trazer o perfil certo, não só volume.",
    ),
    (
        "Construção",
        "Construção dos agentes",
        "Construímos e testamos os agentes de IA e as automações, prontos a assumir o trabalho repetitivo.",
        "Nutrição",
        "Nutrição e qualificação",
        "Fluxos de email e WhatsApp que aquecem e filtram antes do contacto comercial, para a sua equipa falar só com quem está pronto.",
    ),
    (
        "Integração",
        "Integração e formação",
        "Ligamos tudo às suas ferramentas e formamos a sua equipa para trabalhar com a nova Equipa de IA.",
        "Conversão",
        "Processo comercial e CRM",
        "Scripts, playbook e CRM integrado, para que nenhuma oportunidade se perca entre o pedido de informação e a venda.",
    ),
    (
        "Otimização",
        "Otimização contínua",
        "Acompanhamos, medimos e melhoramos o sistema todos os meses, para render cada vez mais.",
        "Otimização",
        "Acompanhamento e otimização",
        "Analisamos o pipeline, o que fecha e o que não fecha, e entregamos os próximos passos concretos. Todos os meses, com dados à frente.",
    ),
]
for tag_a, titulo_a, desc_a, tag_n, titulo_n, desc_n in PASSOS:
    html = troca(html, f'<div class="traj-tag">{tag_a}</div>', f'<div class="traj-tag">{tag_n}</div>', f"etiqueta {tag_a}")
    html = troca(html, f'<h3 class="traj-title">{titulo_a}</h3>', f'<h3 class="traj-title">{titulo_n}</h3>', f"titulo {titulo_a}")
    html = troca(html, f'<p class="traj-desc">{desc_a}</p>', f'<p class="traj-desc">{desc_n}</p>', f"descricao {tag_a}")

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

if falhas:
    print("SUBSTITUIÇÕES FALHADAS:", file=sys.stderr)
    for f in falhas:
        print("  -", f, file=sys.stderr)
    sys.exit(1)

open(PAGE, "w", encoding="utf-8").write(html)
print(f"index.html reescrito: {len(html):,} bytes")

restos = [t for t in ("Equipa de IA", "agentes de IA", "bluebolt-ai-brand", "ricardo.webp") if t in html]
fora_da_seccao_ricardo = [t for t in restos if t not in ("Equipa de IA",)]
print("menções a IA restantes (secção do Ricardo incluída):", html.count("IA"))
