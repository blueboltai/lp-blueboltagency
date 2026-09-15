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
    '<span class="t1">Aumente a sua faturação com um </span><span class="t2">sistema previsível de aquisição de clientes.</span>',
    "h1",
)
html = troca(
    html,
    "Automatize processos, aumente produtividade e reduza custos com agentes de IA implementados à medida da sua operação, para que a tecnologia se adapte ao seu negócio e não o contrário.",
    "Ajudamos o seu negócio a crescer com um sistema que transforma anúncios em vendas e dá controlo real sobre os resultados, para escalar com decisões estratégicas em vez de palpites.",
    "subtitulo do hero",
)
html = troca(
    html,
    '<span class="cta-btn-text">Quero a minha Equipa de IA</span>',
    '<span class="cta-btn-text">Agendar sessão estratégica</span>',
    "botao principal",
    esperado=2,
)

# Barra de confianca — sete provas, nas duas copias do marquee.
TRUST = """<div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Parceiro</span><span class="stackstrip-strong">Google Partner</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M6.5 6C3.46 6 1 8.69 1 12s2.46 6 5.5 6c2.04 0 3.62-1.2 5.5-4.2C13.88 16.8 15.46 18 17.5 18c3.04 0 5.5-2.69 5.5-6s-2.46-6-5.5-6c-2.04 0-3.62 1.2-5.5 4.2C10.12 7.2 8.54 6 6.5 6m0 2.4c1.05 0 2.02.79 3.6 3.6-1.58 2.81-2.55 3.6-3.6 3.6C4.98 15.6 3.9 14 3.9 12s1.08-3.6 2.6-3.6m11 0c1.52 0 2.6 1.6 2.6 3.6s-1.08 3.6-2.6 3.6c-1.05 0-2.02-.79-3.6-3.6 1.58-2.81 2.55-3.6 3.6-3.6"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Parceiro</span><span class="stackstrip-strong">Meta Business</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8.5 8 9 4.5-.5 8-4 8-9V6z"/><path d="m9.5 12 1.8 1.8L15 10.2"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Distinção</span><span class="stackstrip-strong">Top 5% PME Portugal</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Experiência</span><span class="stackstrip-strong">+400 negócios</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m7 15 4-5 3.5 3L21 6"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Foco</span><span class="stackstrip-strong">ROI medido</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 3.5"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Resposta</span><span class="stackstrip-strong">Em menos de 24h</span></span></div>
              <span class="trust-dot"></span>
              <div class="stackstrip-item"><svg class="stackstrip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 2v4M16 2v4M3 10h18"/></svg><span class="stackstrip-text"><span class="stackstrip-lbl">Acompanhamento</span><span class="stackstrip-strong">Reunião mensal</span></span></div>
              <span class="trust-dot"></span>"""

blocos = re.findall(
    r'(<div class="trust-strip-items stack-marquee"[^>]*>)(.*?)(\n\s*</div>)', html, re.S
)
if len(blocos) != 2:
    falhas.append(f"barra de confianca: esperava 2 blocos, encontrou {len(blocos)}")
else:
    for abre, conteudo, fecha in blocos:
        html = html.replace(abre + conteudo + fecha, abre + "\n              " + TRUST + fecha, 1)

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

html = troca(html, "</style>", VSL_CSS + NAV_CSS + "</style>", "CSS da VSL e do hero")
html = troca(html, '\n<!-- QUEM É -->', VSL_HTML + '\n<!-- QUEM É -->', "marcacao da VSL")
html = troca(html, "\n/* Submissão do formulário de lead", VSL_JS + "\n/* Submissão do formulário de lead", "JS da VSL")

# ══════════════════════════════════════════════════════════════════
# SECCAO "O CUSTO SILENCIOSO"
# ══════════════════════════════════════════════════════════════════

html = troca(
    html,
    '<img class="quem-visual-img" src="bluebolt-ai-brand.png" alt="O seu funcionário de IA: um agente Blue Bolt AI a trabalhar lado a lado com a sua equipa">',
    '<img class="quem-visual-img" src="img/equipa.webp" alt="A equipa da Blue Bolt a trabalhar no sistema de aquisição de clientes de um cliente">',
    "imagem da seccao do custo",
)
html = troca(
    html,
    """          <div class="quem-visual-tag">O seu funcionário de IA</div>
          <div class="quem-visual-fine">Trabalha lado a lado com a sua equipa. Nunca falta, nunca se cansa.</div>""",
    """          <div class="quem-visual-tag">A sua equipa de aquisição</div>
          <div class="quem-visual-fine">Estratégia, tráfego, conteúdo e comercial, alinhados no mesmo sistema.</div>""",
    "legenda da imagem",
)
html = troca(
    html,
    """            <div class="quem-stat-num">24/7</div>
            <div class="quem-stat-label">Sempre a trabalhar</div>""",
    """            <div class="quem-stat-num">+400</div>
            <div class="quem-stat-label">Negócios acompanhados</div>""",
    "estatistica 1",
)
html = troca(
    html,
    """            <div class="quem-stat-num">20h+</div>
            <div class="quem-stat-label">Poupadas/semana</div>""",
    """            <div class="quem-stat-num">30min</div>
            <div class="quem-stat-label">Diagnóstico gratuito</div>""",
    "estatistica 2",
)
html = troca(
    html,
    """            <div class="quem-stat-num">+400</div>
            <div class="quem-stat-label">Negócios transformados</div>""",
    """            <div class="quem-stat-num">Top 5%</div>
            <div class="quem-stat-label">PME de Portugal</div>""",
    "estatistica 3",
)
html = troca(
    html,
    '<div class="quem-eyebrow" data-reveal data-delay="1">O custo silencioso</div>',
    '<div class="quem-eyebrow" data-reveal data-delay="1">O custo silencioso</div>',
    "sobrancelha do custo",
)
html = troca(
    html,
    '<span class="tg">O custo escondido que está a travar </span><span class="ta">o crescimento da sua empresa.</span>',
    '<span class="tg">O dinheiro que perde todos os meses </span><span class="ta">em leads que nunca fecham.</span>',
    "h2 do custo",
)
html = troca(
    html,
    """        <p><strong>Quanto custa um colaborador que perde duas horas por dia em tarefas repetitivas? Multiplique pela equipa toda, e depois por doze meses.</strong> Isto não é ineficiência pontual — é dinheiro que sai da empresa todos os meses, de forma silenciosa, porque ninguém para para o calcular.</p>
        <p>Responder aos mesmos emails. Fazer o follow-up de leads à mão. Copiar dados de um lado para o outro. Compilar relatórios. Horas todas as semanas em tarefas que não precisam de uma pessoa.</p>
        <p>Enquanto isso, a sua concorrência já começou a automatizar. Cada dia que adia esta decisão está a financiar a vantagem competitiva de quem já o fez.</p>
        <p>Nós construímos esse sistema para si, à medida do seu negócio. Fica com a sua equipa livre para o que realmente traz dinheiro.</p>""",
    """        <p><strong>Quanto vale um mês em que investiu em anúncios e não sabe dizer quantos clientes vieram daí?</strong> Multiplique pelos meses em que isso aconteceu. Não é um mau mês pontual — é dinheiro que sai da empresa sem deixar rasto, porque ninguém está a medir o que acontece depois do clique.</p>
        <p>Leads que entram e ninguém responde a tempo. Contactos que pedem informação e desaparecem a meio da conversa. Campanhas que geram volume, mas não geram vendas. Meses bons seguidos de meses maus, sem se perceber porquê.</p>
        <p>A maior parte das agências pára no lead. Entregam contactos e o problema passa a ser seu. Só que um anúncio não resolve um negócio sem processo comercial, e uma rede social bonita não traz clientes novos todos os meses por si só.</p>
        <p>Nós construímos o sistema completo, à medida do seu negócio: da atração ao cliente fechado, com visibilidade mensal sobre o que está a funcionar.</p>""",
    "texto do custo",
)
html = troca(
    html,
    """        <div>
          <div class="quem-cred-label">Atendimento</div>
          <div class="quem-cred-value">Respostas 24/7, sem espera</div>
        </div>
        <div>
          <div class="quem-cred-label">Vendas</div>
          <div class="quem-cred-value">Follow-up automático de leads</div>
        </div>
        <div>
          <div class="quem-cred-label">Processos</div>
          <div class="quem-cred-value">Tarefas internas no piloto automático</div>
        </div>
        <div>
          <div class="quem-cred-label">Relatórios</div>
          <div class="quem-cred-value">Dados prontos, sem trabalho manual</div>
        </div>""",
    """        <div>
          <div class="quem-cred-label">Atração</div>
          <div class="quem-cred-value">Campanhas que trazem o perfil certo</div>
        </div>
        <div>
          <div class="quem-cred-label">Nutrição</div>
          <div class="quem-cred-value">Email e WhatsApp que aquecem a lead</div>
        </div>
        <div>
          <div class="quem-cred-label">Conversão</div>
          <div class="quem-cred-value">Processo comercial com scripts e CRM</div>
        </div>
        <div>
          <div class="quem-cred-label">Medição</div>
          <div class="quem-cred-value">Custo por cliente, mês a mês</div>
        </div>""",
    "credenciais do custo",
)

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
    '<div class="ft-role">Google Partner · Meta Business Partner · Top 5% PME Portugal</div>',
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
