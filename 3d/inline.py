#!/usr/bin/env python3
"""inline.py <index.html> — puts vegetation.js inside the page.

A <script type="module"> that imports './vegetation.js' doesn't load on double click
(file:// blocks modules from another file). This swaps that import line for the whole
module, wrapped so its internal names don't clash with the page's. Idempotent.
"""
import pathlib
import re
import sys

MOD = pathlib.Path(__file__).with_name("vegetation.js")
html_p = pathlib.Path(sys.argv[1])
html = html_p.read_text(encoding="utf-8")

imp = re.search(r"^[ \t]*import\s*\{([^}]*)\}\s*from\s*['\"]\./vegetation\.js['\"];?[ \t]*$", html, re.M)
if not imp:
    sys.exit("no `import { … } from './vegetation.js'` in " + str(html_p) + " (already inlined?)")

body = MOD.read_text(encoding="utf-8")
body = re.sub(r"^import \* as THREE from 'three';\n", "", body, flags=re.M)
body = re.sub(r"^export function ", "function ", body, flags=re.M)
names = [n.strip() for n in imp.group(1).split(",") if n.strip()]
block = (
    "// vegetation.js inlined (3d skill)\n"
    f"const {{ {', '.join(names)} }} = (() => {{\n{body}\nreturn {{ tree, cloud, rock, sway }};\n}})();"
)

# THREE as a namespace: if the page imports named pieces only, add it
script_start = html.rfind("<script", 0, imp.start())
if not re.search(r"\*\s*as\s+THREE\b", html[script_start:imp.start()] + html[imp.end():html.find("</script>", imp.end())]):
    block = "import * as THREE from 'three';\n" + block

html = html[:imp.start()] + block + html[imp.end():]
html_p.write_text(html, encoding="utf-8")
print(f"inlined into {html_p} ({len(body) // 1024} KB); vegetation.js is no longer needed next to it")
