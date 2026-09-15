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
/* Veu por cima do video: o texto tem de ganhar sempre ao fotograma. */
.hero-bg-veil{
  position:absolute;
  inset:0;
  z-index:2;
  pointer-events:none;
  background:
    linear-gradient(180deg, rgba(0,1,34,.72) 0%, rgba(0,1,34,.84) 55%, #000122 96%),
    radial-gradient(65% 50% at 50% 34%, rgba(0,1,34,.34), rgba(0,1,34,.8) 100%);
}
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

/* ══ O funil em ampulheta, em 3D ══
   Desenhado a partir do modelo da Blue Bolt feito na Canva. Cada fatia e uma
   taca: o corpo entre duas elipses, o aro claro por cima e a cavidade escura
   la dentro. O volume vem de dois gradientes sobrepostos — um vertical, que
   faz a fatia escurecer para baixo, e um horizontal, que lhe arredonda os
   lados. As duas metades tocam-se na cintura, onde fica o simbolo da venda. */
.funil{
  display:grid;
  grid-template-columns:minmax(0,420px) minmax(0,1fr);
  gap:clamp(2rem,5vw,4.5rem);
  align-items:center;
  max-width:1000px;
  margin:0 auto;
}
.funil-fig{ margin:0; }
.funil-svg{ width:100%;height:auto;display:block; }

.fatia-nome{
  font-family:'Manrope',sans-serif;
  font-size:23px;
  font-weight:600;
  letter-spacing:-.01em;
  fill:#fff;
  paint-order:stroke;
}
.funil-euro{
  font-family:'Manrope',sans-serif;
  font-size:17px;
  font-weight:600;
  fill:#fff;
  fill-opacity:.8;
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
   Tudo pendurado no `.revealed` que o observador ja punha no `.funil`: o
   desenho esta completo desde o inicio e a animacao e um acrescento, nunca
   a condicao para se ver o funil. As fatias caem de cima para baixo, uma a
   seguir a outra, como se o funil se montasse; as etapas do lado entram a
   seguir; e depois de assentar, um lustro percorre os aros de seis em seis
   segundos. E o unico movimento que fica, e e discreto. */
.fatia{ transform-box:view-box; }
.funil.revealed .fatia{
  animation:fn-cai .8s cubic-bezier(.16,1,.3,1) backwards;
  animation-delay:calc(var(--i) * .11s);
}
@keyframes fn-cai{
  from{ opacity:0;transform:translateY(-26px); }
  to{ opacity:1;transform:translateY(0); }
}
.funil-euro{ opacity:0; }
.funil.revealed .funil-euro{ animation:fn-entra .5s ease-out .95s forwards; }

.passo{ opacity:0; }
.funil.revealed .passo{
  animation:fn-sobe .6s cubic-bezier(.16,1,.3,1) forwards;
  animation-delay:calc(.35s + var(--i) * .09s);
}
@keyframes fn-entra{ to{ opacity:1; } }
@keyframes fn-sobe{ from{ opacity:0;transform:translateY(14px); } to{ opacity:1;transform:none; } }

/* O lustro so arranca depois de as seis fatias terem assentado. */
.funil.revealed .fn-lustro,
.funil.revealed .fn-lustro-2{
  animation:fn-brilha 6s ease-in-out infinite;
  animation-delay:calc(1.4s + var(--i) * .2s);
}
@keyframes fn-brilha{
  0%,62%,100%{ stroke-opacity:.42; }
  72%{ stroke-opacity:.95; }
}
.funil.revealed .fn-lustro-2{ animation-name:fn-brilha-2; }
@keyframes fn-brilha-2{
  0%,62%,100%{ stroke-opacity:.18; }
  72%{ stroke-opacity:.5; }
}

/* Ao passar o rato numa fatia, ela sobe e as outras recuam um pouco.
   O `:has()` e que faz isto so acontecer quando o rato esta mesmo sobre uma
   fatia: com `.funil-svg:hover` bastava entrar na moldura do SVG — que e um
   rectangulo com muito vazio — para o funil todo esmorecer. Onde nao houver
   `:has()`, a regra cai e fica so o realce da fatia. */
.fatia{ transition:transform .3s cubic-bezier(.16,1,.3,1), opacity .3s ease; }
.funil-svg:has(.fatia:hover) .fatia{ opacity:.78; }
.funil-svg:has(.fatia:hover) .fatia:hover{ opacity:1;transform:translateY(-5px); }
/* A sombra estende-se para a folga; sem isto seria ela a apanhar o rato. */
.fatia-sombra{ pointer-events:none; }

@media(prefers-reduced-motion:reduce){
  .funil.revealed .fatia,
  .funil.revealed .passo,
  .funil.revealed .funil-euro,
  .funil.revealed .fn-lustro,
  .funil.revealed .fn-lustro-2{ animation:none; }
  .passo,.funil-euro{ opacity:1; }
  .funil-svg:has(.fatia:hover) .fatia,
  .funil-svg:has(.fatia:hover) .fatia:hover{ opacity:1;transform:none; }
}

@media(max-width:860px){
  .funil{ grid-template-columns:1fr;gap:2.5rem; }
  .funil-fig{ max-width:340px;margin-inline:auto; }
}

/* ══════════════════════════════════════════════════════════════════
   A LINHA DO TEMPO — o mesmo sistema, redesenhado
   O numero era um "01" gigante e esbatido numa coluna que existia para
   uma foto que nunca chegou: ocupava metade da seccao a nao dizer nada.
   Passa a ser o no que a linha de progresso atravessa, e o texto passa a
   cartao — cada passo le-se como uma peca, nao como texto solto no preto.
   ══════════════════════════════════════════════════════════════════ */

#trajetoria .traj-list{ max-width:1060px;margin-inline:auto; }

/* Os passos por ler ficavam a 20% e desfocados: a seccao lia-se sempre
   como um so passo aceso no meio do escuro. A 45% e sem desfoque, ve-se
   para onde se vai sem deixar de se perceber onde se esta. */
#trajetoria .traj-item{
  gap:0 7rem;
  margin-bottom:clamp(1.75rem,3.5vw,2.75rem);
  opacity:.45;
  filter:none;
}
#trajetoria .traj-item.active{ opacity:1; }
#trajetoria .traj-item::before{ display:none; }

/* O no, na linha */
.traj-no{
  position:absolute;
  left:50%;top:50%;
  transform:translate(-50%,-50%);
  width:58px;height:58px;
  display:grid;
  place-items:center;
  border-radius:50%;
  /* opaco de proposito: e ele que corta a linha por tras */
  background:#070a16;
  border:1px solid rgba(255,255,255,.1);
  z-index:4;
  transition:border-color .45s ease, box-shadow .45s ease, background .45s ease;
}
.traj-no span{
  font-family:'Archia',sans-serif;
  font-size:17px;
  letter-spacing:-.02em;
  color:rgba(255,255,255,.4);
  transition:color .45s ease;
}
.traj-item.active .traj-no{
  border-color:rgba(47,161,255,.5);
  background:radial-gradient(120% 120% at 50% 0%, rgba(47,161,255,.2), #070a16 70%);
  box-shadow:0 0 0 5px rgba(47,161,255,.07), 0 0 28px rgba(47,161,255,.3);
}
.traj-item.active .traj-no span{ color:#fff; }

/* O passo passa a cartao */
#trajetoria .traj-content{
  position:relative;
  padding:1.45rem 1.6rem;
  border-radius:18px;
  background:linear-gradient(160deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
  border:1px solid rgba(255,255,255,.07);
  transition:opacity .65s cubic-bezier(.16,1,.3,1), transform .65s cubic-bezier(.16,1,.3,1),
             border-color .45s ease, background .45s ease;
}
#trajetoria .traj-item.active .traj-content{
  border-color:rgba(47,161,255,.22);
  background:linear-gradient(160deg, rgba(47,161,255,.07), rgba(255,255,255,.02));
}
/* Filete da cor da marca do lado que da para a linha */
#trajetoria .traj-content::before{
  content:'';
  position:absolute;top:1.45rem;bottom:1.45rem;
  width:2px;
  border-radius:2px;
  background:linear-gradient(to bottom, rgba(47,161,255,.7), rgba(0,93,169,0));
  opacity:0;
  transition:opacity .45s ease;
}
#trajetoria .traj-item.active .traj-content::before{ opacity:1; }
/* Traco curto a ligar o cartao ao no */
#trajetoria .traj-content::after{
  content:'';
  position:absolute;top:50%;
  width:2.4rem;height:1px;
  background:rgba(255,255,255,.12);
  transition:background .45s ease;
}
#trajetoria .traj-item.active .traj-content::after{ background:rgba(47,161,255,.4); }

#trajetoria .traj-item:nth-child(odd) .traj-content{ padding-right:1.6rem; }
#trajetoria .traj-item:nth-child(odd) .traj-content::before{ right:0; }
#trajetoria .traj-item:nth-child(odd) .traj-content::after{ left:100%; }
#trajetoria .traj-item:nth-child(even) .traj-content{ padding-left:1.6rem; }
#trajetoria .traj-item:nth-child(even) .traj-content::before{ left:0; }
#trajetoria .traj-item:nth-child(even) .traj-content::after{ right:100%; }

#trajetoria .traj-desc{ max-width:none;color:rgba(200,204,216,.62); }
#trajetoria .traj-item:nth-child(odd) .traj-desc{ margin-left:0; }
#trajetoria .traj-title{ font-size:clamp(17px,1.5vw,22px); }
#trajetoria .traj-tag{ font-size:8.5px; }

@media(max-width:768px){
  #trajetoria .traj-item{ gap:.9rem;padding-left:4.75rem; }
  .traj-no{
    left:1.5rem;top:1.9rem;
    width:44px;height:44px;
  }
  .traj-no span{ font-size:14px; }
  #trajetoria .traj-content{ grid-row:1; }
  #trajetoria .traj-item:nth-child(odd) .traj-content::after,
  #trajetoria .traj-item:nth-child(even) .traj-content::after{ display:none; }
  #trajetoria .traj-item:nth-child(odd) .traj-content::before,
  #trajetoria .traj-item:nth-child(even) .traj-content::before{ left:0;right:auto; }
}

@media(max-width:640px){
  .hero-h1{ font-size:clamp(26px,7.6vw,36px); }
  .hero-sub{ font-size:14.5px; }
}
@media(prefers-reduced-motion:reduce){
  .hero-bg-video{ display:none; }
}
"""


# ══════════════════════════════════════════════════════════════════
# O FUNIL EM AMPULHETA, EM 3D
# Desenhado a partir do modelo da Blue Bolt feito na Canva: todo azul,
# com os nomes dentro das fatias, sem icones, e as duas metades unidas
# na cintura, onde fica o simbolo da venda. Cada fatia e a superficie
# lateral entre duas elipses; os valores sao calculados aqui, para a
# geometria nao depender de numeros escritos a mao.
# ══════════════════════════════════════════════════════════════════

ACHAT = 0.095            # achatamento das elipses (ry = rx * ACHAT)
CAVA_RX = 0.90           # raio da cavidade, em fracao do raio exterior
CAVA_RY = 0.84           # a cavidade e ainda mais achatada que o aro
CAVA_DY = 0.05           # e desce um pouco, em unidades de ry do aro
RAIO_MINIMO_ARO = 26     # abaixo disto a fatia nao mostra aro nem cavidade

# (nome, descricao, raio de cima, raio de baixo, altura, folga acima, cor)
# A folga a None significa "unida a de cima": e o que fecha a cintura, onde
# o cone que estreita e o que alarga partilham o mesmo ponto.
FATIAS = [
    ("Atração", "Campanhas em Meta e Google Ads que trazem o perfil certo, não só volume.",
     247, 201, 120, 0, "#1B7BE8"),
    ("Oportunidade", "Fluxos de email e WhatsApp que aquecem a lead antes do contacto comercial.",
     190, 138, 116, 11, "#0E86F0"),
    ("Conversão", "Scripts, playbook e CRM para não se perder nenhuma oportunidade pelo caminho.",
     133, 6, 166, 13, "#12A3DE"),
    ("Retenção", "Acompanhamento depois da venda, para o cliente voltar a comprar.",
     6, 148, 130, None, "#1AB9D6"),
    ("Fidelização", "Deixa de comparar preços e passa a escolher-nos por hábito.",
     163, 200, 113, 9, "#0E6FD6"),
    ("Indicação", "Cada cliente satisfeito traz o próximo, sem custo de aquisição.",
     213, 258, 116, 9, "#0E3E90"),
]


# ── cor ─────────────────────────────────────────────────────────────

def _rgb(cor):
    return [int(cor[i:i + 2], 16) for i in (1, 3, 5)]


def _hex(vals):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in vals)


def clarear(cor, q):
    """Aproxima a cor do branco."""
    return _hex([v + (255 - v) * q for v in _rgb(cor)])


def escurecer(cor, q):
    """Aproxima a cor do preto."""
    return _hex([v * (1 - q) for v in _rgb(cor)])


# ── geometria ───────────────────────────────────────────────────────
# A folga mede-se entre silhuetas, nao entre centros: o ponto mais baixo
# de uma fatia inclui o arco da elipse de baixo, e o mais alto da seguinte
# inclui o arco da de cima. Somar so altura + folga colava-as.

MARGEM_X = 46
MARGEM_TOPO = 16
MARGEM_BASE = 30         # acomoda a sombra da ultima fatia


def _geometria():
    fora = []
    for nome, _d, rt, rb, alt, folga, cor in FATIAS:
        ryt, ryb = rt * ACHAT, rb * ACHAT
        if not fora:
            yt = MARGEM_TOPO + ryt
        elif folga is None:
            yt = fora[-1]["yb"]                 # cintura: partilham o ponto
        else:
            yt = fora[-1]["yb"] + fora[-1]["ryb"] + folga + ryt
        fora.append({"nome": nome, "rt": rt, "rb": rb, "ryt": ryt, "ryb": ryb,
                     "yt": yt, "yb": yt + alt, "alt": alt, "cor": cor})
    return fora


GEO = _geometria()
RAIO_MAX = max(max(g["rt"], g["rb"]) for g in GEO)
LARGURA = round(RAIO_MAX * 2 + MARGEM_X * 2)
ALTURA_TOTAL = round(GEO[-1]["yb"] + GEO[-1]["ryb"] + MARGEM_BASE)
CX = LARGURA / 2
CINTURA = GEO[2]["yb"]   # onde os dois cones se tocam


def _n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _defs():
    """Um gradiente de corpo, de aro e de cavidade por fatia, mais o comum.

    Os gradientes do corpo sao em coordenadas do desenho (userSpaceOnUse):
    e assim que o escurecer acompanha a altura real da fatia em vez de se
    repetir igual em todas.
    """
    partes = ["""<linearGradient id="fn-curva" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#000" stop-opacity=".22"/>
        <stop offset=".10" stop-color="#000" stop-opacity=".08"/>
        <stop offset=".32" stop-color="#fff" stop-opacity=".15"/>
        <stop offset=".54" stop-color="#fff" stop-opacity="0"/>
        <stop offset=".88" stop-color="#000" stop-opacity=".10"/>
        <stop offset="1" stop-color="#000" stop-opacity=".24"/>
      </linearGradient>
      <filter id="fn-sombra" x="-40%" y="-140%" width="180%" height="380%">
        <feGaussianBlur stdDeviation="5.5"/>
      </filter>"""]
    for i, g in enumerate(GEO):
        cor = g["cor"]
        partes.append(
            f'<linearGradient id="fn-corpo{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yb"] + g["ryb"])}">'
            f'<stop offset="0" stop-color="{clarear(cor, .24)}"/>'
            f'<stop offset=".34" stop-color="{clarear(cor, .04)}"/>'
            f'<stop offset="1" stop-color="{escurecer(cor, .30)}"/>'
            f"</linearGradient>"
            f'<linearGradient id="fn-aro{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yt"] + g["ryt"])}">'
            f'<stop offset="0" stop-color="{clarear(cor, .46)}"/>'
            f'<stop offset="1" stop-color="{clarear(cor, .22)}"/>'
            f"</linearGradient>"
            f'<linearGradient id="fn-cava{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yt"] + g["ryt"])}">'
            f'<stop offset="0" stop-color="{escurecer(cor, .26)}"/>'
            f'<stop offset="1" stop-color="{escurecer(cor, .44)}"/>'
            f"</linearGradient>"
        )
    return "<defs>" + "".join(partes) + "</defs>"


def _corpo(g):
    """Superficie lateral entre as duas elipses: as metades da frente."""
    return (f'M {_n(CX - g["rt"])} {_n(g["yt"])} '
            f'A {_n(g["rt"])} {_n(g["ryt"])} 0 0 1 {_n(CX + g["rt"])} {_n(g["yt"])} '
            f'L {_n(CX + g["rb"])} {_n(g["yb"])} '
            f'A {_n(g["rb"])} {_n(g["ryb"])} 0 0 1 {_n(CX - g["rb"])} {_n(g["yb"])} Z')


def _arco(g, a1, a2, opacidade, grossura, classe):
    """Lampejo no aro: um arco curto, para a peca ler como vidrada."""
    import math
    rx, ry = g["rt"] * .95, g["ryt"] * .95
    p = lambda a: (CX + rx * math.cos(math.radians(a)), g["yt"] + ry * math.sin(math.radians(a)))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return (f'<path class="{classe}" d="M {_n(x1)} {_n(y1)} A {_n(rx)} {_n(ry)} 0 0 1 {_n(x2)} {_n(y2)}" '
            f'fill="none" stroke="#fff" stroke-opacity="{opacidade}" '
            f'stroke-width="{_n(max(grossura, g["ryt"] * .075))}" stroke-linecap="round"/>')


CORPO_LETRA = 23         # tamanho do nome dentro da fatia
LARGURA_LETRA = 0.55     # largura media de um caracter, em fracao do corpo


def _altura_do_nome(g, nome):
    """A que altura da fatia o nome cabe entre as duas paredes do cone.

    Procura-se o ponto mais baixo que sirva, que e onde a referencia os
    poe; se nem no topo couber, fica no topo. Sem isto o nome da Conversao
    — que estreita ate quase um ponto — saia por fora do cone.
    """
    meio = len(nome) * CORPO_LETRA * LARGURA_LETRA / 2 + 16
    melhor = None
    f = 0.80
    while f >= 0.16:
        raio = g["rt"] + (g["rb"] - g["rt"]) * f
        if raio >= meio:
            melhor = f
            break
        f -= 0.02
    if melhor is None:
        melhor = 0.16
    return g["yt"] + g["alt"] * melhor + CORPO_LETRA * 0.34


def _fatia(i):
    """Uma fatia: sombra, corpo, aro, cavidade, lampejos e o nome."""
    g = GEO[i]
    cor = g["cor"]
    d = _corpo(g)

    # A sombra cai na folga, por baixo. As fatias sao desenhadas de baixo
    # para cima para esta ficar por cima da peca seguinte.
    sy = g["yb"] + g["ryb"] + 4.5
    sombra = (f'<ellipse class="fatia-sombra" cx="{_n(CX)}" cy="{_n(sy)}" rx="{_n(g["rb"] * .94)}" '
              f'ry="{_n(g["rb"] * .085)}" fill="#0c2233" opacity=".2" filter="url(#fn-sombra)"/>')

    # Aro e cavidade so fazem sentido enquanto ha boca; na cintura nao ha.
    if g["rt"] >= RAIO_MINIMO_ARO:
        cava_rx, cava_ry = g["rt"] * CAVA_RX, g["ryt"] * CAVA_RY
        cava_y = g["yt"] + g["ryt"] * CAVA_DY
        boca = (
            f'<ellipse cx="{_n(CX)}" cy="{_n(g["yt"])}" rx="{_n(g["rt"])}" ry="{_n(g["ryt"])}" '
            f'fill="url(#fn-aro{i})"/>'
            f'<ellipse cx="{_n(CX)}" cy="{_n(cava_y)}" rx="{_n(cava_rx)}" ry="{_n(cava_ry)}" '
            f'fill="url(#fn-cava{i})"/>'
            f'<ellipse cx="{_n(CX)}" cy="{_n(cava_y)}" rx="{_n(cava_rx)}" ry="{_n(cava_ry)}" '
            f'fill="none" stroke="{escurecer(cor, .58)}" stroke-opacity=".22" stroke-width=".7"/>'
            + _arco(g, 196, 250, ".48", 1.3, "fn-lustro")
            + _arco(g, 300, 332, ".20", 1.1, "fn-lustro-2")
        )
    else:
        boca = ""

    nome = (f'<text class="fatia-nome" x="{_n(CX)}" y="{_n(_altura_do_nome(g, g["nome"]))}" '
            f'text-anchor="middle">{g["nome"]}</text>')

    return (
        f'<g class="fatia" style="--i:{i}">'
        + sombra
        + f'<path d="{d}" fill="url(#fn-corpo{i})"/>'
        + f'<path d="{d}" fill="url(#fn-curva)"/>'
        + f'<path d="{d}" fill="none" stroke="{escurecer(cor, .38)}" stroke-opacity=".3" stroke-width=".9"/>'
        + boca
        + nome
        + "</g>"
    )


_ARIA = ("Funil em ampulheta: atração, oportunidade e conversão estreitam até à venda; "
         "retenção, fidelização e indicação alargam depois dela")


def funil_svg():
    """As fatias sao emitidas de baixo para cima.

    Em SVG a ordem de desenho e o unico z-index que ha: assim a sombra de
    cada fatia cai sobre a de baixo, que ja esta desenhada.
    """
    fatias = "".join(_fatia(i) for i in reversed(range(len(FATIAS))))
    # O simbolo da venda, mesmo na cintura, onde os dois cones se tocam.
    euro = (f'<text class="funil-euro" x="{_n(CX)}" y="{_n(CINTURA - 2)}" '
            f'text-anchor="middle">€</text>')
    return (f'<svg class="funil-svg" viewBox="0 0 {LARGURA} {ALTURA_TOTAL}" '
            f'role="img" aria-label="{_ARIA}">{_defs()}{fatias}{euro}</svg>')


def funil_passos():
    """As seis etapas em texto, ao lado do funil."""
    itens = []
    for i, (nome, desc, _rt, _rb, _a, _f, cor) in enumerate(FATIAS):
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
      <figure class="funil-fig">""" + funil_svg() + """</figure>
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
html = troca(html, 'src="ricardo.webp"', 'src="img/ricardo.avif"', "foto do Ricardo")

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
    html = html.replace(faixa.group(0), "\n\n      </div>\n    </div>\n  </section>")

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
