/* Les Éclairés - effets de site partagés : curseur éclair + préloader + animations d'entrée.
   Tout est non bloquant (rAF / IntersectionObserver) et respecte prefers-reduced-motion. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. PRÉLOADER : masquer une fois la page chargée ---------- */
  (function () {
    function hide() {
      var p = document.getElementById('preloader');
      if (p) p.classList.add('hidden');
    }
    if (document.readyState === 'complete') hide();
    else window.addEventListener('load', hide);
    setTimeout(hide, 3000); // filet de sécurité si un asset traîne
  })();

  /* ---------- 2. CURSEUR ÉCLAIR (vert D.A.) ---------- */
  (function () {
    var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (!fine || reduced) return;

    var style = document.createElement('style');
    style.textContent =
      '#ec-cursor{position:fixed;top:0;left:0;width:26px;height:26px;pointer-events:none;' +
      'z-index:99999;opacity:0;transform:translate3d(-100px,-100px,0) translate(-50%,-50%);' +
      'will-change:transform;transition:opacity .25s ease,width .18s ease,height .18s ease;' +
      'filter:drop-shadow(0 2px 6px rgba(0,169,110,.45));}' +
      '#ec-cursor.is-visible{opacity:1;}' +
      '#ec-cursor.is-hover{width:38px;height:38px;}' +
      '#ec-cursor svg{width:100%;height:100%;display:block;}';
    document.head.appendChild(style);

    var dot = document.createElement('div');
    dot.id = 'ec-cursor';
    dot.setAttribute('aria-hidden', 'true');
    dot.innerHTML =
      '<svg viewBox="0 0 24 24" fill="#00A96E" stroke="#00C97F" stroke-width="1" ' +
      'stroke-linejoin="round"><path d="M13 2L4 13.5h6.2L9 22l9-12.5h-6.2L13 2z"/></svg>';
    (document.body || document.documentElement).appendChild(dot);

    var mx = 0, my = 0, dx = 0, dy = 0, visible = false, ease = 0.2;
    function loop() {
      dx += (mx - dx) * ease; dy += (my - dy) * ease;
      dot.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    }
    window.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!visible) { visible = true; dx = mx; dy = my; dot.classList.add('is-visible'); }
    }, { passive: true });
    var inter = 'a,button,input,textarea,select,label,[role="button"],summary,.btn';
    document.addEventListener('mouseover', function (e) {
      if (e.target instanceof Element && e.target.closest(inter)) dot.classList.add('is-hover');
    }, { passive: true });
    document.addEventListener('mouseout', function (e) {
      if (e.target instanceof Element && e.target.closest(inter)) dot.classList.remove('is-hover');
    }, { passive: true });
    document.addEventListener('mouseleave', function () { visible = false; dot.classList.remove('is-visible'); });
    requestAnimationFrame(loop);
  })();

  /* ---------- 3. ANIMATIONS D'ENTRÉE (auto) ----------
     Ne s'active QUE sur les pages sans le système .reveal existant (l'accueil
     gère le sien). Anime titres, textes, images et cartes au scroll. */
  (function () {
    if (reduced) return;
    function start() {
      if (document.querySelector('.reveal')) return; // accueil : géré par sa propre logique
      var sel = 'main h1,main h2,main h3,main h4,main p,main li,main img,main figure,main .card,' +
                'section h1,section h2,section h3,section h4,section p,section li,section img,section figure';
      var nodes = document.querySelectorAll(sel);
      if (!nodes.length) return;

      var style = document.createElement('style');
      style.textContent =
        '.ec-anim{opacity:0;transform:translateY(34px) scale(.985);' +
        'transition:opacity .6s cubic-bezier(.16,1,.3,1),transform .75s cubic-bezier(.34,1.56,.64,1);will-change:opacity,transform}' +
        '.ec-anim.ec-in{opacity:1;transform:none}';
      document.head.appendChild(style);

      var list = [];
      nodes.forEach(function (n) {
        if (n.closest('#preloader') || n.closest('footer') || n.closest('nav')) return;
        if (n.parentElement && n.parentElement.closest('.ec-anim')) return; // évite les imbrications
        n.classList.add('ec-anim'); list.push(n);
      });

      var shown = 0;
      var obs = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          var delay = shown < 8 ? shown * 80 : 0; // léger stagger sur le 1er écran
          shown++;
          setTimeout(function () { el.classList.add('ec-in'); }, delay);
          obs.unobserve(el);
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      list.forEach(function (n) { obs.observe(n); });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
    else start();
  })();
})();
