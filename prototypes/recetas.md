## liquid-glass
`backdrop-filter: blur(24px) saturate(180%)`, fondo `rgba(255,255,255,.18)`,
`border: 1px solid rgba(255,255,255,.5)`, `box-shadow: inset 0 1px 0 rgba(255,255,255,.7), 0 8px 32px rgb(0 0 0 / .12)`,
y SIEMPRE una foto detrás.

## nothing
Sacado de la app Nothing X (2025): negro puro, tarjetas `#1b1b1b` de radio 20 en rejilla de
2 columnas; titulares en serifa fina (peso 300, 28-34 px), UI en sans pequeña y gris. Piezas:
grupos de 3 botones redondos (activo blanco con icono negro, resto `#2a2a2a`); cifras finas
con barra (`7/40`); filas icono · nombre · valor · chevron; segmentado en píldora con el
activo blanco; columnas de puntos en SVG (`r=3`, el de arriba rojo); anillo de progreso;
dial. Sin fuente de puntos; el rojo `#d71921` solo en el anillo, el punto activo o UN botón.
Movimiento: la selección salta entre botones con un anillo que se desplaza; cambio de tema
fundido en 300 ms; las columnas de puntos se encienden de abajo arriba al entrar en vista;
el anillo se dibuja con `stroke-dashoffset`; al pulsar `scale(.96)`; curvas
`cubic-bezier(.2,0,0,1)`, sin rebotes.

## suizo
Texto a la izquierda sobre rejilla de 12 columnas, filetes de 1px, números de sección en
mono, titular a `clamp(3.5rem, 10vw, 9rem)`, radios de 0-8 px y el acento en un solo sitio.

## lienzo
`body` con el color exterior y `padding: 16px`; un `.lienzo` con `border-radius: 36px;
overflow: hidden` que lo contiene todo.

## estudio
Fondo plano `#0a0a0b` sin degradado; el render lo hace todo.

## editorial
Productos recortados (PNG sin fondo, o JPEG sobre blanco puro que se funde con la tarjeta),
titular Didone a `clamp(3rem, 8vw, 7rem)` peso 400.

## suave
Su favorito: hazlo con mimo y nunca vacío. Fondo de un tono muy claro, tarjetas blancas de
radio 28, sombras amplias teñidas (`0 24px 48px -16px rgb(20 30 60 / .12)`), botones píldora
negros con flecha en círculo, micro-tarjetas con datos reales y un bento con UI de verdad.

## minimal
Pocas piezas, no ninguna: la demo del producto o la foto tienen que estar.
