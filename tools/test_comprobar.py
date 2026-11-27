"""Pruebas del comprobador: python3 -m unittest discover -s tools (desde la raíz del repo)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comprobar import Revisor  # noqa: E402


def problemas(html):
    r = Revisor()
    r.feed(html)
    r.close()
    return [texto for _, texto in r.problemas]


class Comprobar(unittest.TestCase):
    def test_una_pagina_limpia_pasa(self):
        self.assertEqual(problemas(
            '<html lang="es"><head><link rel="stylesheet" href="css/sitio.css">'
            '<script type="application/ld+json">{"@type":"WebSite"}</script></head>'
            '<body><p class="lema">Hola</p><script src="js/sitio.js"></script></body></html>'), [])

    def test_un_atributo_style_falla(self):
        self.assertEqual(len(problemas('<p style="margin-top:12px">x</p>')), 1)
        self.assertEqual(len(problemas('<img src="a.webp" alt="" STYLE="padding:4px">')), 1)

    def test_un_bloque_style_falla(self):
        self.assertEqual(len(problemas('<style>p{color:red}</style>')), 1)

    def test_un_script_en_linea_falla_salvo_el_json_ld(self):
        self.assertEqual(len(problemas('<script>alert(1)</script>')), 1)
        self.assertEqual(len(problemas('<script type="module">x()</script>')), 1)
        self.assertEqual(problemas('<script type="application/ld+json">{}</script>'), [])

    def test_eventos_y_javascript_fallan(self):
        self.assertEqual(len(problemas('<button onclick="x()">b</button>')), 1)
        self.assertEqual(len(problemas('<a href="javascript:x()">a</a>')), 1)

    def test_dice_la_linea(self):
        r = Revisor()
        r.feed('<p>uno</p>\n<p>dos</p>\n<p style="x">tres</p>')
        r.close()
        self.assertEqual(r.problemas[0][0], 3)


if __name__ == "__main__":
    unittest.main()
