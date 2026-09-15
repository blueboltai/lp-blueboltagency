/* ==========================================================================
   app.js — comportamento da landing page.
   Substitui o que na versao WordPress era feito pelo Elementor Pro:
   carrossel, acordeao, off-canvas, formulario, video e animacoes de entrada.
   Sem dependencias externas.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------------
     Carrossel
     --------------------------------------------------------------------- */

  function initCarousel(root) {
    var track = root.querySelector('.e-carousel-track');
    var slides = Array.prototype.slice.call(track.children);
    var prev = root.querySelector('.e-carousel-prev');
    var next = root.querySelector('.e-carousel-next');
    var scrollBy = parseInt(root.dataset.scrollBy, 10) || 1;
    var autoplay = parseInt(root.dataset.autoplay, 10) || 0;
    var index = 0;
    var timer = null;

    if (!slides.length) return;

    function perView() {
      var value = getComputedStyle(root).getPropertyValue('--slides');
      return Math.max(1, parseInt(value, 10) || 1);
    }

    function maxIndex() {
      return Math.max(0, slides.length - perView());
    }

    function render() {
      index = Math.min(Math.max(index, 0), maxIndex());
      // Relativo ao primeiro slide, para o padding da pista nao deslocar o inicio.
      var origin = slides[0].offsetLeft;
      var offset = slides[index] ? slides[index].offsetLeft - origin : 0;
      track.style.transform = 'translate3d(' + -offset + 'px, 0, 0)';
      prev.disabled = index === 0;
      next.disabled = index >= maxIndex();
      slides.forEach(function (slide, i) {
        // Carrega tambem o slide seguinte, para nao aparecer vazio ao avancar.
        var visible = i >= index && i < index + perView();
        var near = i >= index - 1 && i < index + perView() + 1;
        slide.setAttribute('aria-hidden', visible ? 'false' : 'true');
        if (near) {
          // A pista esta dentro de um viewport com overflow:hidden, por isso o
          // lazy-loading nativo nunca chegaria a disparar nestas imagens.
          slide.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
            img.loading = 'eager';
          });
        }
        // Evita que conteudo fora de vista seja alcancavel por teclado.
        slide.querySelectorAll('a, button, input, iframe, [tabindex]').forEach(function (el) {
          if (visible) {
            el.removeAttribute('tabindex');
          } else {
            el.setAttribute('tabindex', '-1');
          }
        });
      });
    }

    function go(delta) {
      var limit = maxIndex();
      index += delta;
      if (index > limit) index = 0;
      if (index < 0) index = limit;
      render();
    }

    prev.addEventListener('click', function () { go(-scrollBy); restart(); });
    next.addEventListener('click', function () { go(scrollBy); restart(); });

    function restart() {
      if (!autoplay || reduceMotion) return;
      clearInterval(timer);
      timer = setInterval(function () { go(scrollBy); }, autoplay);
    }

    // Arrastar com o dedo / rato.
    var startX = null;
    track.addEventListener('pointerdown', function (event) {
      startX = event.clientX;
    });
    track.addEventListener('pointerup', function (event) {
      if (startX === null) return;
      var delta = event.clientX - startX;
      startX = null;
      if (Math.abs(delta) > 40) {
        go(delta < 0 ? scrollBy : -scrollBy);
        restart();
      }
    });

    root.addEventListener('mouseenter', function () { clearInterval(timer); });
    root.addEventListener('mouseleave', restart);

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(render, 150);
    });

    render();
    restart();
  }

  /* ---------------------------------------------------------------------
     Video: facade do YouTube (o iframe so entra depois do clique)
     --------------------------------------------------------------------- */

  function playVideo(box) {
    if (box.classList.contains('is-playing')) return;
    var id = box.dataset.video;
    if (!id) return;
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
      '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
    iframe.title = box.getAttribute('aria-label') || 'Vídeo';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    iframe.allowFullscreen = true;
    box.appendChild(iframe);
    box.classList.add('is-playing');
    box.removeAttribute('role');
    box.removeAttribute('tabindex');
  }

  /* ---------------------------------------------------------------------
     Modal (off-canvas)
     --------------------------------------------------------------------- */

  var lastFocus = null;

  function openModal(modal) {
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    var target = modal.querySelector('input, textarea, button, [href]');
    if (target) target.focus();
  }

  function closeModal(modal) {
    modal.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  function initModals() {
    var modals = document.querySelectorAll('.e-modal');
    if (!modals.length) return;

    document.addEventListener('click', function (event) {
      var closer = event.target.closest('[data-close]');
      if (closer) {
        var owner = closer.closest('.e-modal');
        if (owner) {
          event.preventDefault();
          closeModal(owner);
        }
        return;
      }
      // Qualquer ligacao para #form (ou para o id de um modal) abre-o.
      var link = event.target.closest('a[href^="#"]');
      if (!link) return;
      var id = link.getAttribute('href').slice(1);
      if (!id) return;
      var modal = document.getElementById(id);
      if (modal && modal.classList.contains('e-modal')) {
        event.preventDefault();
        openModal(modal);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      modals.forEach(function (modal) {
        if (!modal.hidden) closeModal(modal);
      });
    });
  }

  /* ---------------------------------------------------------------------
     Formulario
     --------------------------------------------------------------------- */

  function initForm(form) {
    var message = form.querySelector('.e-form-msg');
    var submit = form.querySelector('.e-form-submit');

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      message.textContent = '';
      message.className = 'e-form-msg';

      if (!form.checkValidity()) {
        var invalid = form.querySelector(':invalid');
        if (invalid) invalid.focus();
        message.textContent = 'Preencha os campos obrigatórios para continuar.';
        message.classList.add('is-error');
        return;
      }

      var endpoint = form.dataset.webhook;
      if (!endpoint) {
        message.textContent = 'Formulário sem destino configurado.';
        message.classList.add('is-error');
        return;
      }

      var payload = {};
      new FormData(form).forEach(function (value, key) { payload[key] = value; });
      payload.page_url = window.location.href;

      submit.disabled = true;
      var original = submit.textContent;
      submit.textContent = 'A enviar…';

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (response) {
          if (!response.ok) throw new Error('HTTP ' + response.status);
          form.reset();
          message.textContent = 'Recebemos o seu pedido. Entramos em contacto em menos de 24h.';
          message.classList.add('is-ok');
        })
        .catch(function () {
          message.textContent = 'Não foi possível enviar. Tente novamente ou fale connosco pelo WhatsApp.';
          message.classList.add('is-error');
        })
        .finally(function () {
          submit.disabled = false;
          submit.textContent = original;
        });
    });
  }

  /* ---------------------------------------------------------------------
     Animacoes de entrada
     --------------------------------------------------------------------- */

  function initReveal() {
    var items = document.querySelectorAll('.e-anim');
    if (!items.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    items.forEach(function (el) { observer.observe(el); });
  }

  /* ---------------------------------------------------------------------
     Arranque
     --------------------------------------------------------------------- */

  document.querySelectorAll('.e-carousel').forEach(initCarousel);
  document.querySelectorAll('.e-form').forEach(initForm);
  initModals();
  initReveal();

  document.addEventListener('click', function (event) {
    var video = event.target.closest('.e-video');
    if (video) playVideo(video);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    var video = event.target.closest('.e-video');
    if (video) {
      event.preventDefault();
      playVideo(video);
    }
  });

  // O video de fundo do hero so arranca depois do primeiro pintar, para nao
  // competir com o LCP. play() trata do carregamento — chamar load() antes
  // abortaria o pedido que ele proprio inicia.
  window.addEventListener('load', function () {
    document.querySelectorAll('.e-con-video').forEach(function (video) {
      video.preload = 'auto';
      var attempt = video.play();
      if (attempt && attempt.catch) attempt.catch(function () {});
    });
  });
})();
