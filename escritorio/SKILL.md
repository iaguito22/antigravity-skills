---
name: escritorio
description: >-
  Hyprland, Quickshell y el shell Caelestia de su escritorio: atajos, reglas de ventanas,
  barra, widgets u overlays QML, lo que pasa al arrancar y el login (SDDM). Úsala con
  "hyprland", "quickshell", "atajo", "widget", "barra", "mi escritorio", "al arrancar".
---

# Su escritorio (Hyprland 0.56 + Caelestia)

Hyprland 0.56 se configura **en Lua** (`hl.bind`, `hl.layer_rule`, `hl.config`…): copia la
forma de `~/.config/hypr/hyprland/*.lua`, porque lo que encuentres en internet suele ser la
sintaxis `.conf` de versiones anteriores. El aspecto visual, con la skill `caelestia`.

## 1. Dónde se escribe
- Lo suyo va en `~/.config/caelestia/hypr-user.lua`: `caelestia install` regenera los `.lua`
  de `~/.config/hypr/` y borra lo que haya ahí (ya pasó).
- Opciones del shell (barra, reloj, transparencia, escalas): `~/.config/caelestia/shell.json`.
- Antes de editar, `cp f f.bak-$(date +%s)`: un error deja la sesión sin atajos.

```lua
hl.bind("SUPER + T", hl.dsp.exec_cmd("kitty"))
hl.layer_rule({ match = { namespace = "mi-overlay" }, no_anim = true })
hl.config({ misc = { background_color = "rgb(000000)" } })
hl.on("hyprland.start", function() hl.exec_cmd("qs -p ~/ruta/shell.qml") end)
```
Desde la terminal: `hyprctl dispatch 'hl.dsp.exec_cmd("app", { workspace = "special:music silent" })'`,
`hyprctl dispatch 'hl.dsp.cursor.move({ x = 1600, y = 880 })'`, `hyprctl eval '<lua>'`.

## 2. Quickshell / QML
- Overlay propio: `PanelWindow` con `WlrLayershell.layer: WlrLayer.Overlay`, un
  `WlrLayershell.namespace` propio, `keyboardFocus: WlrKeyboardFocus.None` y
  `exclusionMode: ExclusionMode.Ignore`. Caelestia anima las capas deslizándolas desde
  arriba: para que el tuyo aparezca en su sitio, `hl.layer_rule({ … no_anim = true })`.
- Probar con `qs -p fichero.qml` (Ctrl+C lo cierra; su shell sigue igual). Tokens del
  shell en QML: `import Caelestia.Config` → `Tokens.rounding/spacing/anim` (pide `screen`
  en el `ShellRoot`).
- Su shell: `qs -c caelestia ipc show` lista lo que expone (`toaster`, `mpris`, `drawers`,
  `idleInhibitor`…) y `qs -c caelestia ipc call <target> <función> [args]` lo usa.
  Reiniciarlo: `qs -c caelestia kill; sleep .1; caelestia shell -d` (desacoplado; nunca
  `caelestia shell -r` en comandos síncronos porque se queda en primer plano y bloquea);
  su log: `caelestia shell -l`.
- Trampas de QML: las propiedades de color se llaman `fg…`/`c…` (una que empiece por `on`
  se toma por manejador de señal y sale negra); el blur se aplica a la imagen antes de
  cargarla (`MultiEffect` en vivo deja anillos); un `Repeater` lleva un modelo de tamaño
  fijo + `visible` (si el tamaño cambia, lo recrea todo y parpadea).
- Para matar un proceso, `pkill -x nombre` o su PID: `pkill -f` con un patrón que aparezca
  en tu propio comando mata tu shell.
- SDDM: `~/PROYECTOS/login-caelestia/probar.sh` (o `sddm-greeter-qt6 --test-mode --theme
  <carpeta>`); instalarlo pide sudo con contraseña: eso lo hace él.

## 3. Hecho
`hyprctl reload config-only && hyprctl configerrors` sin salida, y el cambio visto con
`agy-pantalla foto` (o el atajo pulsado con `agy-pantalla tecla`).
