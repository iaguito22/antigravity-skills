---
name: prototypes
description: >-
  Seis prototipos visuales distintos de una misma web, app o panel para comparar y elegir.
  Úsala con "/prototypes", "prototipos", "varias versiones", "opciones de diseño", o al
  empezar un diseño sin dirección decidida.
---

# Seis prototipos que no se parecen

El fallo de siempre son seis pieles del mismo esqueleto (mismo titular, mismas secciones,
cambia el color). Cada prototipo es **una idea distinta**, y en todas la imagen es la
página. La dirección la pone el dado, no tú. Los scripts se ejecutan, no se leen.

## 1. Dado (una llamada)
`python3 ~/.gemini/config/skills/prototypes/dado.py "<encargo tal cual>"` en la carpeta
de trabajo. Da seis fichas (concepto, estructura, voz, hero, foto, paleta, tipos, trampa),
las recetas de sus estilos y deja `fichas.json` para el comparador. Opciones:
`--tipo movil|panel`, `--evitar nothing`, `--solo liquid-glass`.
Todo lo de cada ficha es obligatorio; la FIRMA solo si sirve al concepto.

## 2. Datos y textos
Una ficha de datos común del encargo (qué ofrece, precios orientativos, horario). Los
datos se comparten; los textos no: cada prototipo escribe su titular y su CTA con su VOZ,
ninguno repetido. 4-5 bloques por landing, sin relleno (testimonios, "por qué elegirnos").
Datos no dados: `000 000 000`, `Calle, nº`, `hola@ejemplo.com` y **Datos que faltan**.

## 3. Construir `p1.html` … `p6.html`
- Antes de programar, una frase por prototipo sin color, fuente ni foto ("una ficha de
  taller que vas rellenando"). Dos frases parecidas = uno no ha cogido su CONCEPTO.
- Autónomos, < 30 KB, cada uno en su modo (estudio y nothing en negro) con `toggleTheme()`
  (`body.dark-mode`, o `body.light-mode` si arranca en negro), sin botón propio.
- La primera pantalla ES la foto de su ficha, grande; el concepto va encima. La estructura
  se nota al bajar (horizontal avanza de lado, apiladas se tapan). La interacción
  protagonista funciona de verdad.
- Lo "muy IA" de la skill `web` (§3) está fuera también aquí. Titular peso 500,
  `letter-spacing: -0.03em`, `text-wrap: balance`; una escala de radios; nav de 13-14 px.
- `movil`: lienzo 1280×1000 con pantallas 390×844 de radio 48 y UI real.
  `panel`: 1440 de ancho, widgets de radio 24 con datos coherentes y gráficas en SVG.
- Fotos: las seis del dado se generan en UNA llamada a `invoke_subagent` con seis
  subagentes, cada uno con su línea FOTO HERO como prompt de director de arte; cada uno
  devuelve su ruta. Si alguno falla (429), solo ese va de Unsplash. Comprímelas todas en
  una llamada: `python3 ~/.gemini/config/skills/web/foto.py <origen1> img1.jpg <origen2> img2.jpg …`.

## 4. Comparar y mirar (hecho = revisor limpio y los seis mirados)
`python3 ~/.gemini/config/skills/prototypes/comparar.py; python3 ~/.gemini/config/skills/web/revisa.py p?.html; agy-ver abrir comparar.html && agy-ver foto && agy-ver logs`
Corrige cada aviso con ediciones puntuales. En las fotos: ¿seis ideas o seis colores?
¿algún hero partido, palabra en color o fila de cifras? ¿cada titular se lee bien sobre su
foto? ¿el `suave` está hecho con mimo?
Baja por dos prototipos sueltos (`agy-ver abrir p2.html && agy-ver ve 900`).

## 5. Entrega
Una línea por prototipo: su idea en una frase y sus ingredientes. Una recomendación con
motivo, y **Datos que faltan** si los hay.
