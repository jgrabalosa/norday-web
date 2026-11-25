/* Norday — lo común a todas las páginas. Sin JavaScript en línea (la CSP de Caddy lo bloquea). */
{
  // Menú en el móvil
  const abre = document.querySelector('.abre'), menu = document.getElementById('menu');
  if (abre && menu) abre.addEventListener('click', () => {
    const si = menu.classList.toggle('abierto');
    abre.setAttribute('aria-expanded', si ? 'true' : 'false');
  });
  // Página actual en el menú
  const aqui = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.menu a').forEach(a => { if (a.getAttribute('href') === aqui) a.setAttribute('aria-current', 'page'); });

  // Nori celebra al acercarse a «Descargar»
  document.querySelectorAll('[data-celebra-btn]').forEach(btn => {
    const sec = btn.closest('section');
    const img = sec && sec.querySelector('[data-celebra] img');
    if (!img) return;
    const normal = img.getAttribute('src'), feliz = img.dataset.alt;
    const si = () => { img.src = feliz; }, no = () => { img.src = normal; };
    ['pointerenter', 'focus'].forEach(e => btn.addEventListener(e, si));
    ['pointerleave', 'blur'].forEach(e => btn.addEventListener(e, no));
  });

  // Identidades (habits): cambia el color de la página
  const raiz = document.querySelector('[data-id]');
  document.querySelectorAll('.idents [data-pon]').forEach(b => b.addEventListener('click', () => {
    if (!raiz) return;
    raiz.dataset.id = b.dataset.pon;
    document.querySelectorAll('.idents [data-pon]').forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    const n = document.getElementById('id-nombre'); if (n) n.textContent = b.querySelector('h3').textContent;
  }));

  // Prueba aquí: tres hábitos de ejemplo
  const prueba = document.getElementById('prueba');
  if (prueba) {
    const botones = [...prueba.querySelectorAll('.habito')];
    const ritmo = document.getElementById('ritmo'), puntos = [...prueba.querySelectorAll('.puntos i')];
    const cara = document.getElementById('prueba-nori'), cuenta = document.getElementById('cuenta');
    const TXT = ['Hoy aún no has empezado', 'Cogiendo ritmo', 'Buen ritmo', '¡Todo hecho por hoy!'];
    const pinta = () => {
      const n = botones.filter(b => b.getAttribute('aria-pressed') === 'true').length;
      ritmo.textContent = TXT[n];
      puntos.forEach((p, i) => p.classList.toggle('lleno', i < n + 1));
      cuenta.textContent = n + ' de ' + botones.length;
      cara.src = n === 3 ? 'img/nori-cria-exultante.webp' : n === 0 ? 'img/nori-cria-dormido.webp' : 'img/nori-cria-sonriente.webp';
      cara.alt = n === 3 ? 'Nori, contento' : n === 0 ? 'Nori, dormido hasta tu primer paso' : 'Nori, sonriente';
    };
    botones.forEach(b => b.addEventListener('click', () => {
      b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      b.querySelector('.check').textContent = b.getAttribute('aria-pressed') === 'true' ? '✓' : '';
      pinta();
    }));
    pinta();
  }

  // Club fundador: todavía no guarda nada (borrador)
  document.querySelectorAll('form.club').forEach(f => f.addEventListener('submit', ev => {
    ev.preventDefault();
    const out = f.querySelector('.aviso');
    out.hidden = false;
    out.textContent = 'Gracias. Esto es un borrador de la web: todavía no se guarda nada. En la de verdad te llegará un correo de confirmación.';
  }));
}
