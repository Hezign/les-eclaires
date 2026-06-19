/* Les Éclairés — curseur personnalisé en forme d'éclair (vert D.A. #00A96E)
   Non bloquant : mousemove n'enregistre que les coordonnées (aucun reflow),
   une seule boucle requestAnimationFrame applique le transform (GPU).
   Désactivé sur tactile et si prefers-reduced-motion. */
(function () {
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!fine || reduced) return;

  // Styles
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

  // Élément curseur : éclair
  var dot = document.createElement('div');
  dot.id = 'ec-cursor';
  dot.setAttribute('aria-hidden', 'true');
  dot.innerHTML =
    '<svg viewBox="0 0 24 24" fill="#00A96E" stroke="#00C97F" stroke-width="1" ' +
    'stroke-linejoin="round"><path d="M13 2L4 13.5h6.2L9 22l9-12.5h-6.2L13 2z"/></svg>';
  (document.body || document.documentElement).appendChild(dot);

  var mx = 0, my = 0, dx = 0, dy = 0, visible = false;
  var ease = 0.2; // 0 = lent, 1 = collé au pointeur

  function loop() {
    dx += (mx - dx) * ease;
    dy += (my - dy) * ease;
    dot.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0) translate(-50%,-50%)';
    requestAnimationFrame(loop);
  }

  window.addEventListener('mousemove', function (e) {
    mx = e.clientX; my = e.clientY;
    if (!visible) { visible = true; dx = mx; dy = my; dot.classList.add('is-visible'); }
  }, { passive: true });

  var interactive = 'a,button,input,textarea,select,label,[role="button"],summary,.btn';
  document.addEventListener('mouseover', function (e) {
    if (e.target instanceof Element && e.target.closest(interactive)) dot.classList.add('is-hover');
  }, { passive: true });
  document.addEventListener('mouseout', function (e) {
    if (e.target instanceof Element && e.target.closest(interactive)) dot.classList.remove('is-hover');
  }, { passive: true });
  document.addEventListener('mouseleave', function () {
    visible = false; dot.classList.remove('is-visible');
  });

  requestAnimationFrame(loop);
})();
