---
name: caelestia
description: >-
  Caelestia, el estilo de su escritorio, para interfaces SUYAS: HUD o menús de un juego,
  temas de apps (Spotify, mpv, Zen, login), widgets y paneles propios. Úsala con "estilo
  caelestia", "como mi escritorio", o al hacer la interfaz de un proyecto suyo sin estilo
  dado. Las webs de negocio van con `web`.
---

# Caelestia como en sus proyectos

**Solo datos y controles**: cada elemento es un dato que él quiere ver o un control que usa,
y cada dato sale una vez. El nombre del estilo, una marca, el modo actual o de dónde salen
los datos no son datos (Flash los puso dos veces como chip y como pie). El vidrio, el color
y el movimiento también tienen un trabajo. Cómo lo resolvió en sus otras interfaces (y dónde
vive cada tema, Zen incluido): `temas.md`, en esta carpeta.

## 1. Tokens (una llamada, se pegan tal cual)
`python3 ~/.gemini/config/skills/caelestia/tokens.py` → `:root` con los colores por rol de
su fondo actual, la escala de radios y espacios, curvas, duraciones y vidrio. `--qml` para
QML, `--sin-color` para la paleta neutra (lo que no lee su `scheme.json`: algo publicado,
un juego). Si corre en su equipo, que lea `~/.local/state/caelestia/scheme.json` en vivo y
siga su modo claro/oscuro.

## 2. Cómo se usan
- **Un acento.** Superficies + `primary`; el acento puede salir del contenido (en Spotify,
  el color dominante de la carátula, animado con `@property`) o ser blanco (F1). Los
  colores de estado (sectores, banderas, avisos) van vivos y saturados para leerse sobre
  una escena.
- **Radios concéntricos**: radio de dentro = radio de fuera − margen (Spotify: panel 28 →
  margen 12 → tarjeta 16 → carátula 8), siempre de la escala. Botones, chips, pestañas y
  barras de estado en píldora; iconos y posiciones en círculo.
- **Vidrio**: `--panel` + `backdrop-filter: var(--glass)`, borde `--line` y `--shadow`. El
  brillo o tinte del acento va por dentro (`inset`), para no teñir lo de debajo.
- **Tipografía**: Rubik (la del shell) o Figtree, pesos 500-800, cifras `tabular-nums`;
  los números grandes en negrita (reloj del login 128 px, `letter-spacing: -2px`). Iconos
  Material Symbols Rounded; mono CaskaydiaCove NF.
- **Movimiento que transforma**: lo nuevo crece desde lo que había (iris que se cierra,
  panel que se expande, ventanita con la misma proporción y radio que el iris anterior para
  que empalme), con las curvas y duraciones de los tokens, y cada estado acaba en el color
  con el que empieza el siguiente.
- **Superficie limpia**: scroll sin barras; el foco de teclado cambia el fondo de la píldora
  (le molesta cualquier anillo o halo); hover = fondo o borde suave de la fila. Texto sobre
  foto o vídeo en blanco; en modo claro, las barras sobre vídeo siguen oscuras
  (`inverseSurface`).

Para escribirlo y probarlo en Hyprland/Quickshell (y las trampas de QML): skill `escritorio`.

## 3. Elegir y comprobar
Si queda una decisión abierta (acento, variante de una pieza), haz 3-6 maquetas pequeñas
lado a lado y que elija él. Hecho = mirado con `agy-ver abrir … && agy-ver foto` (o
`agy-pantalla foto` si es de escritorio), en los dos modos si lee el esquema:
`caelestia scheme set -m light|dark` cambia SU escritorio, así que acaba en el modo en que
lo encontraste.
