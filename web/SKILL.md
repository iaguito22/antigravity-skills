---
name: web
description: >-
  Gusto de Iago y proceso para cualquier web o página nueva o rediseñada: landing, web de
  negocio, portfolio, tienda, html/css. Úsala antes de escribir la primera línea.
---

# Web con su gusto

Los scripts de esta carpeta se ejecutan, no se leen.

## 1. Dirección (una llamada)
`python3 ~/.gemini/config/skills/web/dado.py` → estilo, hero, firma y tipografías. Úsalo
tal cual; si él ya dio un estilo, sáltalo. Escribe tres líneas antes de programar:
- **Concepto:** un objeto, gesto o lugar de ESTE negocio ("la pizarra donde apuntan el
  lote del día"), no un adjetivo.
- **Paleta:** fondo, tinta y un acento, lejos de la obvia del sector (café ≠ crema y marrón).
- **Firma:** la del dado aplicada al concepto.

## 2. Lo que le gusta
Minimal, suave y redondeado, liquid glass, Nothing, mucho aire. La imagen manda:
- **Hero** = una foto a pantalla completa (`100svh`, o en un lienzo redondeado con 12-16 px
  de margen) con el titular encima y 2-4 widgets pequeños de vidrio o blanco al 90 %
  (240-340 px) repartidos por las esquinas: una ficha de producto, chips, un dato real.
- **Cards** con foto arriba (4:5 o 4:3, radio 20-24), nombre y precio en una línea, una
  línea gris de 2-3 datos con `·`.
- Escala tipográfica extrema (`clamp(2.5rem, 10vw, 10rem)`, tracking negativo) junto a
  texto pequeño; botones en píldora; una sola escala de radios.
- Movimiento ligado al scroll (`animation-timeline: view()` dentro de `@supports` y
  `prefers-reduced-motion: no-preference`).

Si no es un negocio sino una herramienta, panel o app suya, el estilo es el de la skill
`caelestia`.

## 3. Lo que le parece "muy IA" (fuera siempre)
Hero partido texto | imagen · una palabra del H1 en otro color, cursiva de color o
degradado (el H1 va en una tinta) · fila o cinta de cifras ("10x · 24/7") · brillos,
blobs y neón · fondo crema + H1 con serifa · etiqueta en mayúsculas espaciadas sobre cada
título · datos en vivo o coordenadas GPS · frases hechas ("artesanal", "pasión por",
"experiencia única", "sin prisa") · fuentes por defecto (Inter, DM Sans, Plus Jakarta,
Poppins, Montserrat, Fraunces, Playfair, Cormorant). Escribe como el dueño: precios,
horas, nombres propios.

## 4. Construir
- Por defecto un sitio pequeño: `index.html` + como mucho dos páginas que el negocio
  necesite (`carta.html`, `contacto.html`), con `css/styles.css` y `js/main.js` compartidos
  y el catálogo en `js/data.js`. Escribe `index.html` entero; las demás, copiándolo y
  cambiando el `<main>`.
- Fotos: el hero se genera. En la CLI, con `invoke_subagent` (un subagente con un prompt
  de director de arte: objeto, encuadre, luz, "35mm film, natural grain"; te devuelve la
  ruta). El resto, de Unsplash (`https://images.unsplash.com/photo-<id>?w=900&q=70`), sin
  buscar IDs a ciegas: si dudas de uno, genera. `foto.py <origen> img/hero.jpg` comprime lo
  generado. Cada `img` con `alt`, `width` y `height`.
- Lo interactivo es lo que sirve para elegir (filtros, galería, menú móvil) y funciona de
  verdad. Calculadoras, reservas, carritos o áreas de cliente solo si los pide: cuestan
  mucho y él no los pidió. HTML sin dependencias salvo que el proyecto ya use un framework.

## 5. Comprobar (hecho = revisor limpio y fotos miradas)
`python3 ~/.gemini/config/skills/web/revisa.py *.html; agy-ver abrir index.html && agy-ver foto && agy-ver ve 900 && agy-ver movil && agy-ver logs`
Corrige cada línea del revisor y cada error de consola. Abre las fotos y busca el
detalle: menú en una línea, nada que se salga del lienzo o de la pantalla, textos sin
cortar, móvil, contraste. Corrige todo lo visto en una tanda de ediciones puntuales y
compruébalo con una sola pasada más (revisor + la foto de lo que cambiaste), no repitas la
ronda entera.
