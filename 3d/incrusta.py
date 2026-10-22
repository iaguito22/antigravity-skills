#!/usr/bin/env python3
"""incrusta.py <index.html> — mete vegetacion.js dentro de la página.

Un <script type="module"> que importa './vegetacion.js' no carga con doble clic (file://
bloquea módulos de otro fichero). Esto cambia esa línea de import por el módulo entero,
envuelto para que sus nombres internos no choquen con los de la página. Idempotente.
"""
import pathlib
import re
import sys

MOD = pathlib.Path(__file__).with_name("vegetacion.js")
html_p = pathlib.Path(sys.argv[1])
html = html_p.read_text(encoding="utf-8")

imp = re.search(r"^[ \t]*import\s*\{([^}]*)\}\s*from\s*['\"]\./vegetacion\.js['\"];?[ \t]*$", html, re.M)
if not imp:
    sys.exit("no hay `import { … } from './vegetacion.js'` en " + str(html_p) + " (¿ya incrustado?)")

cuerpo = MOD.read_text(encoding="utf-8")
cuerpo = re.sub(r"^import \* as THREE from 'three';\n", "", cuerpo, flags=re.M)
cuerpo = re.sub(r"^export function ", "function ", cuerpo, flags=re.M)
nombres = [n.strip() for n in imp.group(1).split(",") if n.strip()]
bloque = (
    "// vegetacion.js incrustado (skill 3d)\n"
    f"const {{ {', '.join(nombres)} }} = (() => {{\n{cuerpo}\nreturn {{ arbol, nube, roca, mecer }};\n}})();"
)

# THREE como espacio de nombres: si la página importa piezas sueltas, se añade
script_ini = html.rfind("<script", 0, imp.start())
if not re.search(r"\*\s*as\s+THREE\b", html[script_ini:imp.start()] + html[imp.end():html.find("</script>", imp.end())]):
    bloque = "import * as THREE from 'three';\n" + bloque

html = html[:imp.start()] + bloque + html[imp.end():]
html_p.write_text(html, encoding="utf-8")
print(f"incrustado en {html_p} ({len(cuerpo) // 1024} KB); ya no hace falta vegetacion.js al lado")
