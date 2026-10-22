#!/usr/bin/env python3
"""Tokens de Caelestia listos para pegar: colores por rol del scheme.json en vivo
(o la paleta neutra "sin color" del juego de F1), radios, espacios, curvas y vidrio.
Uso: tokens.py [--css | --qml] [--sin-color]"""
import json, os, sys

SCHEME = os.path.expanduser("~/.local/state/caelestia/scheme.json")
ROLES = ["primary", "onPrimary", "primaryContainer", "onPrimaryContainer", "secondaryContainer",
         "onSecondaryContainer", "surface", "surfaceContainerLow", "surfaceContainer",
         "surfaceContainerHigh", "surfaceContainerHighest", "onSurface", "onSurfaceVariant",
         "outline", "outlineVariant", "inverseSurface", "inverseOnSurface", "inversePrimary",
         "error", "onError", "success"]
# Neutra: la que eligió para la interfaz de F1 (acento blanco; el color solo en datos de estado).
SIN_COLOR = {"primary": "ececef", "onPrimary": "1a1a1c", "primaryContainer": "2a2a2e",
             "onPrimaryContainer": "ececef", "secondaryContainer": "26262a", "onSecondaryContainer": "d0d0d5",
             "surface": "0b0b0d", "surfaceContainerLow": "121215", "surfaceContainer": "141417",
             "surfaceContainerHigh": "1c1c20", "surfaceContainerHighest": "242428", "onSurface": "ececef",
             "onSurfaceVariant": "a3a3a9", "outline": "55555b", "outlineVariant": "2e2e33",
             "inverseSurface": "ececef", "inverseOnSurface": "1a1a1c", "inversePrimary": "1a1a1c",
             "error": "ff4b45", "onError": "ffffff", "success": "2fd35a"}
RADIO = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 28, "pill": 999}   # Tokens.rounding del shell
ESPACIO = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 28}             # Tokens.spacing / padding
CURVAS = {  # M3 expressive, las del shell
    "standard": "0.2, 0, 0, 1", "emphasized-decel": "0.05, 0.7, 0.1, 1", "emphasized-accel": "0.3, 0, 0.8, 0.15",
    "spatial-fast": "0.42, 1.67, 0.21, 0.9", "spatial": "0.38, 1.21, 0.22, 1", "spatial-slow": "0.39, 1.29, 0.35, 0.98",
    "effects": "0.34, 0.8, 0.34, 1"}
DURACION = {"effects-fast": 150, "effects": 200, "spatial-fast": 350, "spatial": 500, "spatial-slow": 650,
            "sm": 200, "md": 400, "lg": 600}

def kebab(s):
    return "".join("-" + c.lower() if c.isupper() else c for c in s)

def main():
    args = set(sys.argv[1:])
    modo, cols = "dark", SIN_COLOR
    if "--sin-color" not in args:
        try:
            d = json.load(open(SCHEME))
            modo, cols = d.get("mode", "dark"), d["colours"]
        except Exception:
            print("/* sin scheme.json: paleta neutra */", file=sys.stderr)
    if "--qml" in args:
        print(f"// modo {modo}")
        print("readonly property var standard: [0.2, 0, 0, 1, 1, 1]")
        print("readonly property var emphasized: [0.05, 0.7, 0.1, 1, 1, 1]")
        print("readonly property var spatial: [0.38, 1.21, 0.22, 1, 1, 1]")
        for r in ROLES:  # prefijo fg/bg: una propiedad llamada onSurface se toma por manejador de señal
            print(f'readonly property color {"fg" if r.startswith("on") else "c"}{r[0].upper() + r[1:]}: "#{cols[r]}"')
        return
    print(f":root {{ /* Caelestia, modo {modo} */")
    print(f"  color-scheme: {modo};")
    for r in ROLES:
        print(f"  --{kebab(r)}: #{cols[r]};")
    for k, v in RADIO.items():
        print(f"  --r-{k}: {v}px;")
    for k, v in ESPACIO.items():
        print(f"  --s-{k}: {v}px;")
    for k, v in CURVAS.items():
        print(f"  --ease-{k}: cubic-bezier({v});")
    for k, v in DURACION.items():
        print(f"  --dur-{k}: {v}ms;")
    sup = cols["surfaceContainer"]
    rgb = ", ".join(str(int(sup[i:i + 2], 16)) for i in (0, 2, 4))
    print(f"  --panel: rgba({rgb}, 0.78);")
    print("  --glass: blur(16px) saturate(1.4);")
    print(f"  --line: {'rgba(255,255,255,0.07)' if modo == 'dark' else 'rgba(0,0,0,0.07)'};")
    print("  --shadow: 0 8px 32px rgba(0,0,0,0.28);")
    print('  --font: "Rubik", "Figtree", system-ui, sans-serif;')
    print('  --mono: "CaskaydiaCove NF", "Geist Mono", monospace;')
    print("}")

main()
