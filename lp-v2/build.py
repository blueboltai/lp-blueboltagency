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
  max-width:min(1060px, 94%);
  margin-inline:auto;
  margin-bottom:1.25rem;
  text-wrap:balance;
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
/* O titulo ocupa a largura toda do bloco; so o corpo do texto e que fica
   estreito, para nao passar do comprimento de linha que se le bem. */
.prob-head .quem-h2{ max-width:none;text-wrap:balance; }
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
.prob-callout{
  margin:2.25rem auto 0;
  max-width:52ch;
  padding:1.1rem 1.75rem;
  border-radius:16px;
  background:rgba(47,161,255,.08);
  border:1px solid rgba(0,93,169,.16);
  font-family:'Manrope',sans-serif;
  font-size:15.5px;
  font-weight:500;
  line-height:1.6;
  color:var(--lt-inc);
}

/* ══ O funil em ampulheta, em 3D ══
   Cada fatia e a superficie lateral entre duas elipses, com um aro por cima
   e um gradiente de volume. Fica nitido em qualquer ecra e continua a ser
   texto la dentro. As leads descem a convergir ate a venda e alargam depois. */
.funil{
  display:grid;
  grid-template-columns:minmax(0,1fr) minmax(300px,430px);
  align-items:center;
  gap:clamp(28px,5vw,64px);
  max-width:920px;
  margin:0 auto;
}
.funil-glass{ margin:0;min-width:0; }
.funil-svg{ width:100%;height:auto;display:block;overflow:visible; }
.fatia-txt{
  font-family:'Manrope',sans-serif;
  font-size:15px;
  font-weight:600;
  text-anchor:middle;
  letter-spacing:.005em;
}
.venda line{ stroke:rgba(10,15,35,.2);stroke-width:1; }
.venda-txt{
  font-family:'Manrope',sans-serif;
  font-size:11px;
  font-weight:700;
  letter-spacing:.2em;
  text-anchor:middle;
  fill:#005da9;
}

/* As leads */
.lead{
  transform-box:view-box;
  transform-origin:0 0;
  animation:lead-desce 3.6s linear infinite;
}
.lead-topo{ fill:#2fa1ff; }
.lead-base{ fill:#17a37b; }
@keyframes lead-desce{
  0%   { transform:translate(var(--x0),var(--y0));opacity:0 }
  12%  { opacity:1 }
  82%  { opacity:1 }
  100% { transform:translate(var(--x1),var(--y1));opacity:0 }
}

/* As duas notas, empilhadas ao lado do funil */
.funil-notas{
  display:flex;
  flex-direction:column;
  gap:clamp(1.75rem,3.5vw,3rem);
  justify-self:end;   /* encosta as notas ao funil, em vez de as deixar a boiar */
}
.funil-nota{ max-width:34ch; }
.funil-nota-eyebrow{
  display:block;
  font-family:'Manrope',sans-serif;
  font-size:9px;
  font-weight:700;
  letter-spacing:.28em;
  text-transform:uppercase;
  color:#005da9;
  margin-bottom:.6rem;
}
.funil-nota-base .funil-nota-eyebrow{ color:#0c8a66; }
.funil-nota p{
  font-family:'Manrope',sans-serif;
  font-size:14.5px;
  font-weight:300;
  line-height:1.7;
  color:var(--lt-inc-2);
}

@media(max-width:860px){
  .funil{ grid-template-columns:1fr;gap:2.25rem; }
  .funil-glass{ grid-row:1;max-width:400px;margin-inline:auto; }
  .funil-notas{ grid-row:2;gap:1.75rem; }
  .funil-nota{ max-width:52ch;margin-inline:auto;text-align:center; }
}
@media(prefers-reduced-motion:reduce){
  .lead{ animation:none;opacity:.85;transform:translate(var(--x1),var(--y1)); }
}
}

@media(max-width:640px){
  .hero-h1{ max-width:100%; font-size:clamp(26px,7.6vw,36px); }
  .hero-sub{ font-size:14.5px; }
}
@media(prefers-reduced-motion:reduce){
  .hero-bg-video{ display:none; }
}
"""


# ══════════════════════════════════════════════════════════════════
# O FUNIL EM AMPULHETA, EM 3D
# Desenhado em SVG e nao em imagem: cada fatia e a superficie lateral
# entre duas elipses, o que da a leitura de volume sem deixar de ser
# nitido em qualquer ecra. Os valores sao calculados aqui, para a
# geometria nao depender de numeros escritos a mao.
# ══════════════════════════════════════════════════════════════════

CX = 210                 # eixo da ampulheta
ACHAT = 0.26             # achatamento das elipses: quanto mais baixo, mais de cima se olha

# (y, raio) de cima para baixo. Estreita ate a venda e volta a alargar.
NIVEIS = [(60, 185), (128, 141), (196, 97), (264, 53),
          (300, 53), (368, 97), (436, 141), (504, 185)]

FATIAS = [
    # (indice do nivel de cima, etiqueta, cor do corpo, cor do aro, cor do texto)
    (0, "Atração",      "#cfe4f7", "#e8f3fc", "#15507f"),
    (1, "Oportunidade", "#96c5ee", "#b7d9f5", "#123f66"),
    (2, "Conversão",    "#1f74c0", "#4595d5", "#ffffff"),
    (4, "Retenção",     "#0d8763", "#17a37b", "#ffffff"),
    (5, "Lealdade",     "#83cab2", "#a3dac6", "#0a4d3a"),
    (6, "Indicação",    "#cbe7dd", "#dff1e9", "#0a4d3a"),
]


def _corpo(yt, rt, yb, rb):
    """Superficie lateral entre duas elipses: as duas metades da frente."""
    return (f"M{CX - rt} {yt} A{rt} {rt * ACHAT:.1f} 0 0 0 {CX + rt} {yt} "
            f"L{CX + rb} {yb} A{rb} {rb * ACHAT:.1f} 0 0 1 {CX - rb} {yb} Z")


def _leads():
    """Pontos que descem: convergem ate a venda, alargam depois dela."""
    topo = [(-152, -12), (-84, 2), (-22, 8), (46, -6), (112, 10), (164, -10)]
    base = [(6, -146), (-8, -78), (3, 8), (-4, 78), (7, 150)]
    saida = []
    for i, (x0, x1) in enumerate(topo):
        atraso = -i * 0.58
        saida.append(
            f'<circle class="lead lead-topo" cx="{CX}" cy="0" r="4.5" '
            f'style="--x0:{x0}px;--y0:58px;--x1:{x1}px;--y1:262px;animation-delay:{atraso:.2f}s"/>'
        )
    for i, (x0, x1) in enumerate(base):
        atraso = -0.3 - i * 0.62
        saida.append(
            f'<circle class="lead lead-base" cx="{CX}" cy="0" r="4.5" '
            f'style="--x0:{x0}px;--y0:302px;--x1:{x1}px;--y1:500px;animation-delay:{atraso:.2f}s"/>'
        )
    return "\n        ".join(saida)


def funil_svg():
    """As formas todas primeiro, as etiquetas so no fim.

    Se cada fatia levasse o seu texto, o aro da fatia seguinte — que e
    desenhado depois — tapava-o. Separar os dois passos resolve-o sem
    truques de z-index, que em SVG nao existem.
    """
    formas, etiquetas = [], []
    for topo_i, etiqueta, corpo_cor, aro_cor, texto_cor in FATIAS:
        yt, rt = NIVEIS[topo_i]
        yb, rb = NIVEIS[topo_i + 1]
        d = _corpo(yt, rt, yb, rb)
        formas.append(
            f'<g class="fatia">'
            f'<ellipse cx="{CX}" cy="{yt}" rx="{rt}" ry="{rt * ACHAT:.1f}" fill="{aro_cor}"/>'
            f'<path d="{d}" fill="{corpo_cor}"/>'
            f'<path d="{d}" fill="url(#volume)"/>'
            f"</g>"
        )
        # A etiqueta fica na banda livre da fatia, acima do aro seguinte.
        y = yt + (yb - yt) * 0.46 + rt * ACHAT * 0.42
        etiquetas.append(
            f'<text x="{CX}" y="{y:.0f}" fill="{texto_cor}" class="fatia-txt">{etiqueta}</text>'
        )
    partes = formas + etiquetas
    return """<svg class="funil-svg" viewBox="0 0 420 564" role="img"
       aria-label="Funil em ampulheta: atração, oportunidade e conversão estreitam até à venda; retenção, lealdade e indicação alargam depois dela">
    <defs>
      <linearGradient id="volume" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#fff" stop-opacity=".30"/>
        <stop offset="42%" stop-color="#fff" stop-opacity="0"/>
        <stop offset="100%" stop-color="#000" stop-opacity=".16"/>
      </linearGradient>
    </defs>
    """ + "\n    ".join(partes) + f"""
    <g class="venda">
      <line x1="46" y1="282" x2="168" y2="282"/>
      <line x1="252" y1="282" x2="374" y2="282"/>
      <text x="{CX}" y="286" class="venda-txt">€ VENDA</text>
    </g>
    <g class="leads">
        {_leads()}
    </g>
  </svg>"""


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
      <p class="prob-callout" data-reveal data-delay="3">Para a maioria das agências, atrair leads é o objetivo final. Para nós, é o ponto de partida.</p>
    </div>

    <div class="funil" data-reveal="fade">

      <div class="funil-notas">
        <div class="funil-nota">
          <span class="funil-nota-eyebrow">Antes da venda</span>
          <p>Estreitamos de propósito. Cada etapa filtra até sobrar quem tem o problema, o orçamento e a urgência certos.</p>
        </div>
        <div class="funil-nota funil-nota-base">
          <span class="funil-nota-eyebrow">Depois da venda</span>
          <p>A partir daqui alarga. Cada cliente que fica compra outra vez e traz o próximo — e é aqui que a maioria das agências já saiu.</p>
        </div>
      </div>

      <figure class="funil-glass">""" + funil_svg() + """</figure>

    </div>

  </div>
</section>"""

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
    '<h2 class="cta-h2" data-reveal data-delay="1">Pare de depender de indicações<br><span class="cta-ta">e monte um sistema previsível.</span></h2>',
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
