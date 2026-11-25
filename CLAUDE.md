# norday-web — la web de Norday (`norday.app`)

La web de Norday: la casa de las apps de Norday (Norday Habits, Norday Focus
y, más adelante, Norday Ideas), con Nori como protagonista. Es HTML, CSS y
JavaScript **estáticos, sin compilar y sin framework** (Astro, descartado).
La servirá **Caddy directamente** desde el VPS, fuera del backend.

**Estado:** borrador v1 (de marketing, 23-nov-2026), **sin publicar**. La web
que hay hoy en `norday.app` es la landing antigua, que vive en el backend
(`habitos-app`) y **no se toca**. Esta se publica cuando Quim lo decida.

## Qué hay en el repo

| Ruta | Qué es | ¿Es la web? |
|---|---|---|
| `*.html` de la raíz | Las páginas: `index.html` (Norday), `habits.html`, `apps.html` (lo que viene), `ideas.html` y `prensa.html` | Sí |
| `css/sitio.css`, `js/sitio.js`, `js/crece.js` | Estilos y comportamiento de todas las páginas | Sí |
| `rive.js`, `rive.wasm`, `nori-riv.js` | Nori de Rive en la portada (`nori-riv.js` es el `.riv` en base64) | Sí |
| `img/`, `media/` | Imágenes y el vídeo de la demo | Sí |
| `scripts-rive/` | `extraer.py` y `escena.py`: cómo se hizo la escena de Rive de Nori (660×880, máquina `Nori`, entradas `mirarX`, `mirarY` y `dormido`). Archivo: sus rutas son del entorno donde se hicieron | No |
| `prototipos/nori-te-mira/` | El prototipo del 21-nov (Nori que sigue el cursor). Archivo | No |

**El repo es público.** Nada interno aquí: ni notas de trabajo, ni
decisiones, ni claves. Lo que hace falta saber de cada tarea va en su ficha.

**Lo que no es la web no se toca** salvo que la tarea lo pida: ni
`scripts-rive/` ni `prototipos/`. Las comprobaciones
de la web (CSP, enlaces, pesos) miran **solo las páginas de la raíz y lo que
cargan**; el prototipo lleva JavaScript y estilos en línea y no se publica.

## Cómo se prueba

Con un servidor estático en la raíz del repo (con `file://` el `.wasm` no
carga):

```
python3 -m http.server 8000
```

y abrir `http://localhost:8000/`. Sin errores en la consola. **Móvil
primero:** mirar también a 360 px de ancho.

## Reglas que no se rompen

- **Solo español.** `lang="es"` en todas las páginas.
- **CSP estricta** (la pondrá Caddy): `script-src 'self'` y `style-src` sin
  `'unsafe-inline'`.
  - **Nada de JavaScript en línea:** todo `<script>` lleva `src`. La única
    excepción es el JSON-LD (`<script type="application/ld+json">`), que es un
    dato y no se ejecuta.
  - **Nada de `style="…"`** en lo nuevo (los que quedan del borrador los quita
    una tarea).
  - **Nada de terceros** (scripts, letras, iframes) sin que la tarea lo diga.
- **Las letras están por decidir:** no se cambia la fuente ni el `@import` de
  Google Fonts de `css/sitio.css` salvo que la tarea lo pida.
- **Ligera y móvil primero.** Casi todo el tráfico llega desde las redes, en el
  móvil. Imágenes en `webp`; Rive se carga tarde (solo cuando Nori llega a
  adulto en la portada).
- **«Reducir movimiento»** (`prefers-reduced-motion`) para todas las
  animaciones, y Rive no se carga.
- **Accesible:** textos alternativos, botones con nombre, contraste suficiente.

## Textos y marca

- **Nori es chico** («Nori está contento», «él»). La moneda se llama
  **puntos**.
- La web es de **Norday**, no solo de Norday Habits, y **sí habla de las otras
  apps** (Norday Focus y Norday Ideas, provisional).
- **La web no dice dónde están los datos** («se quedan en Europa» ni nada
  parecido). **Sin promesas científicas** ni valoraciones inventadas.
- **La insignia de Google Play, oficial y sin cambiar**, con los enlaces cortos
  `https://norday.app/web` (botón) y `https://norday.app/qr` (QR).
- **Las páginas legales** siguen en `api.norday.app` (`privacidad.html` y
  `eliminar-cuenta.html`): se enlazan, no se copian.
- El autor: su LinkedIn y la letra «Q», sin foto.
- Los textos marcados como provisionales los decide Quim: no se inventan.

## Git

- Se trabaja en ramas (`robot/**` el robot, `wip-*` Claude), nunca en `main`.
  Quim decide cuándo se mergea y cuándo se publica.
- **`git diff` y `git log` abren paginador**: `git --no-pager`.
- Un PR por tarea, con lo que cambia página a página.
