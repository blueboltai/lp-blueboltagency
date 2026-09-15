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
   Cada fatia e uma taca: o corpo entre duas elipses, o aro claro por cima e
   a cavidade escura la dentro. O volume vem de dois gradientes sobrepostos —
   um vertical, que faz a fatia escurecer para baixo, e um horizontal, que
   lhe arredonda os lados. As fatias ficam separadas por uma folga medida
   entre silhuetas, para cada uma se ler como peca solta. */
.funil{ max-width:1180px;margin:0 auto; }
.funil-largo,.funil-so{ margin:0; }
.funil-svg{ width:100%;height:auto;display:block; }

/* O SVG e desenhado a 1296 de largura e mostrado a ~1100: o texto encolhe
   com ele, por isso os corpos vao um pouco acima do tamanho final. */
.chamada-nome{
  font-family:'Manrope',sans-serif;
  font-size:25px;
  font-weight:700;
  letter-spacing:-.01em;
}
.chamada-txt{
  font-family:'Manrope',sans-serif;
  font-size:17px;
  font-weight:300;
  fill:var(--lt-inc-2);
}

/* Em ecras estreitos o texto dentro do SVG ficaria minusculo: mostra-se so
   o funil e a mesma informacao passa a lista normal, em HTML. */
.funil-curto{ display:none; }
.funil-lista{ list-style:none;margin:2.25rem 0 0;padding:0;display:flex;flex-direction:column;gap:1rem; }
.funil-item{
  display:flex;
  gap:12px;
  font-family:'Manrope',sans-serif;
  font-size:14.5px;
  font-weight:300;
  line-height:1.6;
  color:var(--lt-inc-2);
}
.funil-item strong{ font-weight:700; }
.funil-item-ponto{
  flex:none;
  width:9px;height:9px;
  border-radius:50%;
  margin-top:.55em;
}

@media(max-width:900px){
  .funil-largo{ display:none; }
  .funil-curto{ display:block; }
  .funil-so{ max-width:340px;margin-inline:auto; }
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

ACHAT = 0.10             # achatamento das elipses (ry = rx * ACHAT)
ALTURA = 78              # altura do eixo de cada fatia
FOLGA = 8                # folga entre a silhueta de uma fatia e a seguinte
CAVA_RX = 0.90           # raio da cavidade, em fracao do raio exterior
CAVA_RY = 0.84           # a cavidade e ainda mais achatada que o aro
CAVA_DY = 0.05           # e desce um pouco, em unidades de ry do aro
ICONE_PX = 34            # lado do icone, ja desenhado

# (nome, descricao em duas linhas, raio de cima, raio de baixo, cor, icone)
FATIAS = [
    ("Atração", ("Meta e Google Ads que trazem o", "perfil certo, não só volume."),
     255, 200, "#2B5FE3", "alvo"),
    ("Oportunidade", ("Email e WhatsApp que aquecem a", "lead antes do contacto comercial."),
     200, 145, "#1D7BDF", "pessoas"),
    ("Conversão", ("Scripts, playbook e CRM para não", "perder nenhuma oportunidade."),
     145, 62, "#1296C9", "visto"),
    ("Retenção", ("Acompanhamento depois da venda,", "para o cliente voltar a comprar."),
     68, 130, "#10ACA2", "voltar"),
    ("Lealdade", ("Deixa de comparar preços e passa", "a escolher-nos por hábito."),
     130, 192, "#18BC7C", "estrela"),
    ("Indicação", ("Cada cliente satisfeito traz o", "próximo, sem custo de aquisição."),
     192, 258, "#33CC5C", "rede"),
]

# Icones a 24x24, traco branco. Desenhados a mao para nao trazer dependencias.
ICONES = {
    "alvo": '<circle cx="12" cy="12" r="9.3"/><circle cx="12" cy="12" r="4.9"/>'
            '<circle cx="12" cy="12" r="1.25" fill="#fff" stroke="none"/>',
    "pessoas": '<circle cx="9.1" cy="8.1" r="3.25"/><path d="M3.1 18.9c0-3.35 2.7-5.45 6-5.45s6 2.1 6 5.45"/>'
               '<circle cx="17.2" cy="9.1" r="2.45"/><path d="M16.8 14.2c2.65.12 4.3 2.02 4.3 4.9"/>',
    "visto": '<circle cx="12" cy="12" r="9.3"/><path d="M7.5 12.3 10.6 15.4 16.5 9.1"/>',
    "voltar": '<path d="M4.95 9.43A7.5 7.5 0 0 1 19.05 9.43"/><path d="M19.75 5.49 19.05 9.43 15.99 6.86"/>'
              '<path d="M19.05 14.57A7.5 7.5 0 0 1 4.95 14.57"/><path d="M4.25 18.51 4.95 14.57 8.01 17.14"/>',
    "estrela": '<path d="M12 3.6 14.29 9.45 20.56 9.82 15.71 13.81 17.29 19.88 12 16.5 6.71 19.88 '
               '8.29 13.81 3.44 9.82 9.71 9.45Z"/>',
    "rede": '<path d="M9.96 10.39 6.65 7.80M14.04 10.39 17.35 7.80M10.16 13.84 6.98 17.02M13.84 13.84 17.02 17.02"/>'
            '<circle cx="12" cy="12" r="2.6"/><circle cx="5" cy="6.5" r="2.1"/><circle cx="19" cy="6.5" r="2.1"/>'
            '<circle cx="5.5" cy="18.5" r="2.1"/><circle cx="18.5" cy="18.5" r="2.1"/>',
}


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
# inclui o arco da de cima. Somar so ALTURA + FOLGA colava-as.

MARGEM_X = 54            # folga lateral a volta do funil
MARGEM_TOPO = 22
MARGEM_BASE = 30         # acomoda a sombra da ultima fatia
ESPACO_TXT = 336         # largura reservada a cada coluna de etiquetas


def _geometria():
    """Para cada fatia: raios, achatamentos e os dois centros verticais."""
    fora, y = [], MARGEM_TOPO
    for _n, _d, rt, rb, cor, _ic in FATIAS:
        ryt, ryb = rt * ACHAT, rb * ACHAT
        yt = y + ryt
        yb = yt + ALTURA
        fora.append({"rt": rt, "rb": rb, "ryt": ryt, "ryb": ryb, "yt": yt, "yb": yb, "cor": cor})
        y = yb + ryb + FOLGA
    return fora


GEO = _geometria()
RAIO_MAX = max(max(g["rt"], g["rb"]) for g in GEO)
LARGURA_FUNIL = round(RAIO_MAX * 2 + MARGEM_X * 2)
ALTURA_TOTAL = round(GEO[-1]["yb"] + GEO[-1]["ryb"] + MARGEM_BASE)
LARGURA_TOTAL = LARGURA_FUNIL + ESPACO_TXT * 2
CX = LARGURA_TOTAL / 2


def _n(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _defs(p):
    """Um gradiente de corpo, de aro e de cavidade por fatia, mais o comum.

    Os gradientes do corpo sao em coordenadas do desenho (userSpaceOnUse):
    e assim que o escurecer acompanha a altura real da fatia em vez de se
    repetir igual em todas.
    """
    partes = [f"""<linearGradient id="{p}curva" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#000" stop-opacity=".20"/>
        <stop offset=".10" stop-color="#000" stop-opacity=".07"/>
        <stop offset=".30" stop-color="#fff" stop-opacity=".13"/>
        <stop offset=".52" stop-color="#fff" stop-opacity="0"/>
        <stop offset=".88" stop-color="#000" stop-opacity=".09"/>
        <stop offset="1" stop-color="#000" stop-opacity=".22"/>
      </linearGradient>
      <filter id="{p}sombra" x="-40%" y="-140%" width="180%" height="380%">
        <feGaussianBlur stdDeviation="5.5"/>
      </filter>"""]
    for i, g in enumerate(GEO):
        cor = g["cor"]
        partes.append(
            f'<linearGradient id="{p}corpo{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yb"] + g["ryb"])}">'
            f'<stop offset="0" stop-color="{clarear(cor, .22)}"/>'
            f'<stop offset=".34" stop-color="{clarear(cor, .04)}"/>'
            f'<stop offset="1" stop-color="{escurecer(cor, .26)}"/>'
            f"</linearGradient>"
            f'<linearGradient id="{p}aro{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yt"] + g["ryt"])}">'
            f'<stop offset="0" stop-color="{clarear(cor, .44)}"/>'
            f'<stop offset="1" stop-color="{clarear(cor, .20)}"/>'
            f"</linearGradient>"
            f'<linearGradient id="{p}cava{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{_n(g["yt"] - g["ryt"])}" x2="0" y2="{_n(g["yt"] + g["ryt"])}">'
            f'<stop offset="0" stop-color="{escurecer(cor, .23)}"/>'
            f'<stop offset="1" stop-color="{escurecer(cor, .40)}"/>'
            f"</linearGradient>"
        )
    return "<defs>" + "".join(partes) + "</defs>"


def _corpo(g):
    """Superficie lateral entre as duas elipses: as metades da frente."""
    return (f'M {_n(CX - g["rt"])} {_n(g["yt"])} '
            f'A {_n(g["rt"])} {_n(g["ryt"])} 0 0 1 {_n(CX + g["rt"])} {_n(g["yt"])} '
            f'L {_n(CX + g["rb"])} {_n(g["yb"])} '
            f'A {_n(g["rb"])} {_n(g["ryb"])} 0 0 1 {_n(CX - g["rb"])} {_n(g["yb"])} Z')


def _arco(g, a1, a2, opacidade, grossura):
    """Lampejo no aro: um arco curto, para a peca ler como vidrada."""
    import math
    rx, ry = g["rt"] * .95, g["ryt"] * .95
    p = lambda a: (CX + rx * math.cos(math.radians(a)), g["yt"] + ry * math.sin(math.radians(a)))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return (f'<path d="M {_n(x1)} {_n(y1)} A {_n(rx)} {_n(ry)} 0 0 1 {_n(x2)} {_n(y2)}" fill="none" '
            f'stroke="#fff" stroke-opacity="{opacidade}" stroke-width="{_n(max(grossura, g["ryt"] * .075))}" '
            f'stroke-linecap="round"/>')


def _fatia(i, p):
    """Uma fatia: sombra, corpo, aro, cavidade, lampejos e icone."""
    g = GEO[i]
    cor = g["cor"]
    d = _corpo(g)

    # A sombra cai na folga, por baixo. As fatias sao desenhadas de baixo
    # para cima para esta ficar por cima da peca seguinte.
    sy = g["yb"] + g["ryb"] + 4.5
    sombra = (f'<ellipse cx="{_n(CX)}" cy="{_n(sy)}" rx="{_n(g["rb"] * .94)}" ry="{_n(g["rb"] * .085)}" '
              f'fill="#0c2233" opacity=".21" filter="url(#{p}sombra)"/>')

    cava_rx = g["rt"] * CAVA_RX
    cava_ry = g["ryt"] * CAVA_RY
    cava_y = g["yt"] + g["ryt"] * CAVA_DY

    k = ICONE_PX / 24
    iy = g["yt"] + .55 * ALTURA + g["ryt"] * .25
    icone = (f'<g transform="translate({_n(CX)} {_n(iy)}) scale({_n(k)}) translate(-12 -12)" fill="none" '
             f'stroke="#fff" stroke-width="2.05" stroke-linecap="round" stroke-linejoin="round">'
             f'{ICONES[FATIAS[i][5]]}</g>')

    return (
        "<g>"
        + sombra
        + f'<path d="{d}" fill="url(#{p}corpo{i})"/>'
        + f'<path d="{d}" fill="url(#{p}curva)"/>'
        + f'<path d="{d}" fill="none" stroke="{escurecer(cor, .36)}" stroke-opacity=".30" stroke-width=".9"/>'
        + f'<ellipse cx="{_n(CX)}" cy="{_n(g["yt"])}" rx="{_n(g["rt"])}" ry="{_n(g["ryt"])}" fill="url(#{p}aro{i})"/>'
        + f'<ellipse cx="{_n(CX)}" cy="{_n(cava_y)}" rx="{_n(cava_rx)}" ry="{_n(cava_ry)}" fill="url(#{p}cava{i})"/>'
        + f'<ellipse cx="{_n(CX)}" cy="{_n(cava_y)}" rx="{_n(cava_rx)}" ry="{_n(cava_ry)}" fill="none" '
          f'stroke="{escurecer(cor, .55)}" stroke-opacity=".22" stroke-width=".7"/>'
        + _arco(g, 196, 250, ".46", 1.3)
        + _arco(g, 300, 332, ".20", 1.1)
        + icone
        + "</g>"
    )


def _etiqueta(i):
    """Etiqueta lateral com linha de chamada, alternando esquerda e direita."""
    nome, (l1, l2), _rt, _rb, cor, _ic = FATIAS[i]
    g = GEO[i]
    ym = (g["yt"] + g["yb"]) / 2
    borda = (g["rt"] + g["rb"]) / 2          # raio do cone a meia altura
    escuro = escurecer(cor, .12)
    if i % 2 == 0:
        x_txt, ancora = CX - RAIO_MAX - MARGEM_X - 22, "end"
        x_ponto, x_fim = x_txt + 16, CX - borda - 14
    else:
        x_txt, ancora = CX + RAIO_MAX + MARGEM_X + 22, "start"
        x_ponto, x_fim = x_txt - 16, CX + borda + 14
    return (
        "<g>"
        f'<line x1="{_n(x_ponto)}" y1="{_n(ym)}" x2="{_n(x_fim)}" y2="{_n(ym)}" stroke="{cor}" '
        f'stroke-width="1.4" stroke-opacity=".75"/>'
        f'<circle cx="{_n(x_ponto)}" cy="{_n(ym)}" r="4.5" fill="{cor}"/>'
        f'<circle cx="{_n(x_fim)}" cy="{_n(ym)}" r="4.5" fill="{cor}"/>'
        f'<text x="{_n(x_txt)}" y="{_n(ym - 23)}" text-anchor="{ancora}" fill="{escuro}" '
        f'class="chamada-nome">{nome}</text>'
        f'<text x="{_n(x_txt)}" y="{_n(ym + 7)}" text-anchor="{ancora}" class="chamada-txt">{l1}</text>'
        f'<text x="{_n(x_txt)}" y="{_n(ym + 32)}" text-anchor="{ancora}" class="chamada-txt">{l2}</text>'
        "</g>"
    )


_ARIA = ("Funil em ampulheta: atração, oportunidade e conversão estreitam até à venda; "
         "retenção, lealdade e indicação alargam depois dela")


def funil_svg(com_etiquetas=True):
    """As fatias sao emitidas de baixo para cima e as etiquetas so no fim.

    Duas razoes, a mesma raiz: em SVG a ordem de desenho e o unico z-index
    que ha. De baixo para cima, a sombra de cada fatia cai sobre a de baixo,
    que ja esta desenhada; e as etiquetas no fim nao sao cortadas pelo aro
    da fatia seguinte.
    """
    # Cada variante leva o seu prefixo de id: as duas convivem na mesma
    # pagina e um url(#...) duplicado resolveria sempre para a primeira,
    # que em ecra estreito esta escondida — e o funil saia sem cor nenhuma.
    p = "fn-" if com_etiquetas else "fc-"
    fatias = "".join(_fatia(i, p) for i in reversed(range(len(FATIAS))))
    if not com_etiquetas:
        # So o funil, para ecras estreitos: mesma geometria, moldura recortada.
        x0 = CX - LARGURA_FUNIL / 2
        return (f'<svg class="funil-svg" viewBox="{_n(x0)} 0 {LARGURA_FUNIL} {ALTURA_TOTAL}" '
                f'role="img" aria-label="{_ARIA}">{_defs(p)}{fatias}</svg>')
    chamadas = "".join(_etiqueta(i) for i in range(len(FATIAS)))
    return (f'<svg class="funil-svg" viewBox="0 0 {LARGURA_TOTAL} {ALTURA_TOTAL}" '
            f'role="img" aria-label="{_ARIA}">{_defs(p)}{fatias}{chamadas}</svg>')


def funil_lista():
    """A mesma informacao em lista, para ecras estreitos."""
    itens = []
    for nome, (l1, l2), _rt, _rb, cor, _ic in FATIAS:
        itens.append(
            f'<li class="funil-item"><span class="funil-item-ponto" style="background:{cor}"></span>'
            f'<span><strong style="color:{escurecer(cor, .12)}">{nome}</strong> {l1} {l2}</span></li>'
        )
    return '<ul class="funil-lista">' + "".join(itens) + "</ul>"

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
      <figure class="funil-largo">""" + funil_svg(True) + """</figure>
      <div class="funil-curto">
        <figure class="funil-so">""" + funil_svg(False) + """</figure>
        """ + funil_lista() + """
      </div>
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
