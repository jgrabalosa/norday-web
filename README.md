# norday-web

La web de Norday (`norday.app`): la casa de las apps de Norday, con Nori.
HTML, CSS y JavaScript estáticos, sin compilar. La servirá Caddy desde el VPS.

**Estado:** borrador v1 (23-nov-2026), sin publicar.

## Verla en local

```
python3 -m http.server 8000
```

en la raíz del repo, y abrir `http://localhost:8000/`. Con `file://` no
funciona: el `.wasm` de Rive no carga.

## Las páginas

| Página | Qué es |
|---|---|
| `index.html` | Norday: Nori crece al bajar (huevo → cría → adulto) y, de adulto, te mira (Rive) |
| `habits.html` | Norday Habits: la demo, cómo funciona, «Pruébalo aquí», las identidades y las preguntas |
| `apps.html` | Lo que viene: Norday Focus, la app de ideas y el club fundador (el formulario aún no guarda) |
| `ideas.html` | Las ideas de la semana: carruseles, infografías e historietas, con su texto |
| `prensa.html` | La frase, los datos, qué la hace distinta y las imágenes |

## Qué no es la web

- `scripts-rive/`: cómo se hizo la escena de Rive de Nori.
- `prototipos/nori-te-mira/`: el prototipo del 21-nov.

Nada de eso se publica.

## Para quien trabaje en el repo

Las reglas (CSP, solo español, Nori, textos) están en `CLAUDE.md`.
