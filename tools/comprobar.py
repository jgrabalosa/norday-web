#!/usr/bin/env python3
"""Comprueba que las páginas de la web cumplen la CSP estricta con la que las sirve Caddy.

    python3 tools/comprobar.py            (desde la raíz del repo)

La CSP es `script-src 'self'` y `style-src` sin `'unsafe-inline'`: el navegador
ignora todo lo que va en línea, y la página se rompe sin avisar. Por eso, en las
páginas de la raíz (`*.html`; no `prototipos/` ni `scripts-rive/`, que no se
publican), falla si encuentra:

  - un atributo `style="…"`;
  - un bloque `<style>`;
  - un `<script>` sin `src`, salvo el JSON-LD (`type="application/ld+json"`,
    que es un dato y no se ejecuta);
  - un atributo de evento (`onclick`, `onload`…) o un enlace `javascript:`.

Python 3, sin dependencias. Sale con 0 si todo está bien y con 1 si no, con la
página y la línea de cada problema.
"""
import glob
import os
import sys
from html.parser import HTMLParser

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Revisor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.problemas = []

    def _apuntar(self, texto):
        self.problemas.append((self.getpos()[0], texto))

    def handle_starttag(self, etiqueta, atributos):
        nombres = {nombre.lower(): (valor or "") for nombre, valor in atributos}
        if "style" in nombres:
            self._apuntar(f'atributo style en <{etiqueta}>: pásalo a una clase de css/sitio.css')
        for nombre in nombres:
            if nombre.startswith("on"):
                self._apuntar(f"atributo de evento {nombre} en <{etiqueta}>: va en un .js")
        for nombre in ("href", "src", "action", "formaction"):
            if nombres.get(nombre, "").strip().lower().startswith("javascript:"):
                self._apuntar(f"enlace javascript: en <{etiqueta}>: va en un .js")
        if etiqueta == "style":
            self._apuntar("bloque <style>: va en css/sitio.css")
        if etiqueta == "script" and "src" not in nombres:
            if nombres.get("type", "").strip().lower() != "application/ld+json":
                self._apuntar("<script> sin src: va en un .js (solo el JSON-LD puede ir en línea)")

    handle_startendtag = handle_starttag


def revisar(ruta):
    revisor = Revisor()
    with open(ruta, encoding="utf-8") as f:
        revisor.feed(f.read())
    revisor.close()
    return revisor.problemas


def main():
    paginas = sorted(glob.glob(os.path.join(RAIZ, "*.html")))
    if not paginas:
        print("comprobar: no hay páginas .html en la raíz")
        return 1
    total = 0
    for ruta in paginas:
        for linea, texto in revisar(ruta):
            print(f"{os.path.basename(ruta)}:{linea}: {texto}")
            total += 1
    if total:
        print(f"MAL: {total} problema(s) en {len(paginas)} páginas")
        return 1
    print(f"BIEN: {len(paginas)} páginas, sin nada en línea")
    return 0


if __name__ == "__main__":
    sys.exit(main())
