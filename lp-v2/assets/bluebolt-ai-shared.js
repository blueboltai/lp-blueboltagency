// Nav aparece ao scroll
(function(){
  var nav = document.getElementById('nav');
  if(!nav) return;
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

function toggleNav(){
  document.getElementById('mnav').classList.toggle('open');
  document.getElementById('burger').classList.toggle('open');
}

// Reveal on scroll
(function(){
  var els = document.querySelectorAll('[data-reveal]');
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('revealed'); obs.unobserve(e.target); }
    });
  }, {threshold:0.12});
  els.forEach(function(el){ obs.observe(el); });
})();
