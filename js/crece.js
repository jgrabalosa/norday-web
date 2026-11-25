/* Norday — portada: Nori crece al bajar (huevo → cría → adulto) y, de adulto,
   te mira con Rive (el prototipo «Nori te mira»). Sin JavaScript en línea. */
{
  const lienzo = document.getElementById('lienzo');
  const canvas = document.getElementById('rive');
  if (lienzo) {
    const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const fases = [...lienzo.querySelectorAll('.fase')];
    const huevo = lienzo.querySelector('.fase.huevo img');
    const QUE = ['huevo', 'huevo', 'cria', 'adulto'];
    let actual = 0;

    const pon = (n) => {
      if (n === actual) return;
      const antes = QUE[actual], ahora = QUE[n];
      actual = n;
      // en el paso 1 el huevo se pone contento y se mueve más
      huevo.src = n === 1 ? 'img/nori-huevo-exultante.webp' : 'img/nori-huevo-sonriente.webp';
      fases.forEach(f => f.classList.toggle('ve', f.classList.contains(ahora)));
      canvas.classList.toggle('ve', ahora === 'adulto');
      if (ahora === 'adulto') arrancaRive();
      if (antes !== ahora && !quieto) {
        lienzo.classList.remove('pop'); void lienzo.offsetWidth; lienzo.classList.add('pop');
      }
    };

    const io = new IntersectionObserver((ents) => {
      ents.forEach(e => { if (e.isIntersecting) pon(+e.target.dataset.paso); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    document.querySelectorAll('.paso').forEach(p => io.observe(p));

    // Rive: se carga cuando Nori llega a adulto (o al estar la página quieta)
    let r = null, mx, my, dormido;
    const CARA = { x: (514 - 182) / 660, y: (451 - 60) / 880 };
    let objX = 50, objY = 50, curX = 50, curY = 50, ultimo = performance.now(), proxima = 0, durmiendo = false;

    function arrancaRive() {
      if (r || quieto || !window.rive || !window.NORI_RIV) return;
      try {
        rive.RuntimeLoader.setWasmUrl('rive.wasm');
        rive.Rive.suppressDeprecationWarnings = ['state-machine-inputs'];
        r = new rive.Rive({
          buffer: Uint8Array.from(atob(window.NORI_RIV), c => c.charCodeAt(0)).buffer,
          canvas, autoplay: true, stateMachine: 'Nori',
          layout: new rive.Layout({ fit: rive.Fit.Contain, alignment: rive.Alignment.Center }),
          onLoad: () => {
            r.resizeDrawingSurfaceToCanvas();
            const ins = r.stateMachineInputs('Nori') || [];
            mx = ins.find(i => i.name === 'mirarX'); my = ins.find(i => i.name === 'mirarY'); dormido = ins.find(i => i.name === 'dormido');
            lienzo.classList.add('rive');
            requestAnimationFrame(paso);
          },
          onLoadError: () => { r = null; }
        });
        new ResizeObserver(() => { try { r && r.resizeDrawingSurfaceToCanvas(); } catch (e) {} }).observe(canvas);
      } catch (e) { r = null; }
    }

    function mira(ev) {
      const b = canvas.getBoundingClientRect();
      const cx = b.left + b.width * CARA.x, cy = b.top + b.height * CARA.y;
      objX = 50 + 50 * Math.max(-1, Math.min(1, (ev.clientX - cx) / Math.max(240, innerWidth * 0.42)));
      objY = 50 + 50 * Math.max(-1, Math.min(1, (ev.clientY - cy) / Math.max(240, innerHeight * 0.42)));
      ultimo = performance.now();
      if (durmiendo) { durmiendo = false; if (dormido) dormido.value = false; }
    }
    addEventListener('pointermove', mira, { passive: true });
    addEventListener('pointerdown', mira, { passive: true });
    addEventListener('scroll', () => { ultimo = performance.now(); if (durmiendo) { durmiendo = false; if (dormido) dormido.value = false; } }, { passive: true });

    function paso(t) {
      const q = t - ultimo;
      if (q > 15000 && !durmiendo) { durmiendo = true; if (dormido) dormido.value = true; objX = 50; objY = 55; }
      else if (q > 4000 && !durmiendo && t > proxima) { objX = 15 + Math.random() * 70; objY = 30 + Math.random() * 45; proxima = t + 1400 + Math.random() * 1800; }
      curX += (objX - curX) * 0.12; curY += (objY - curY) * 0.12;
      if (mx && Math.abs(mx.value - curX) > 0.05) mx.value = curX;
      if (my && Math.abs(my.value - curY) > 0.05) my.value = curY;
      requestAnimationFrame(paso);
    }
  }
}
