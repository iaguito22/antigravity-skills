---
name: caelestia
description: >-
  Caelestia, the Hyprland/Quickshell desktop style, for the user's own interfaces: a game HUD
  or menus, app themes (Spotify, mpv, a browser, an SDDM login), widgets and personal
  dashboards. Use it on "caelestia style" / "estilo caelestia", "like my desktop", or when
  building the UI of one of the user's own projects with no style given. Business websites
  go to `web`.
---

# Caelestia, the way it looks on the desktop

**Data and controls only**: every element is a figure the user wants to see or a control
they use, and each figure appears once. The style's name, a brand, the current mode or where
the data comes from are not data (models add them as a chip or a footer). Glass, colour and
motion have a job too. The scripts are run, not read.

## 1. Tokens (one call, paste as is)
`python3 ~/.gemini/config/skills/caelestia/tokens.py` → a `:root` block with the role
colours of the current wallpaper scheme, radii, spacing, curves and glass. `--qml` for QML,
`--neutral` for a neutral palette (anything that won't read `scheme.json`: a published
page, a game). If it runs on the user's machine, read
`~/.local/state/caelestia/scheme.json` live and follow its light/dark `mode`.

## 2. How to use them
- **One accent.** Surfaces + `primary`; the accent can come from the content (album art's
  dominant colour, animated with `@property`) or be white. Status colours (sectors, flags,
  warnings) are vivid and saturated so they read over a busy scene.
- **Concentric radii**: inner radius = outer radius − the gap between them (panel 28 → gap
  12 → card 16 → artwork 8), always from the scale. Buttons, chips, tabs and status bars
  are pills; icons and positions are circles.
- **Glass**: `--panel` + `backdrop-filter: var(--glass)`, `--line` border and `--shadow`.
  Accent sheen or tint goes on the inside (`inset`), so it doesn't tint what's underneath.
- **Type**: Rubik (the shell's sans) or Figtree, weights 500-800, `tabular-nums` for
  figures; big numbers bold (a 128 px clock with `letter-spacing: -2px`). Material Symbols
  Rounded icons; CaskaydiaCove NF for mono.
- **Motion that transforms**: the new state grows out of the old one (an iris closing, a
  panel expanding, a window that opens with the same aspect ratio and radius as the iris
  before it so they join), with the tokens' curves and durations, and each state ends on
  the colour the next one starts with.
- **Clean surface**: scrolling without scrollbars; keyboard focus changes the pill's
  background (rings and halos read as noise); hover = a soft background or border on the
  row. Text over a photo or video is white; in light mode, bars over video stay dark
  (`inverseSurface`).

## 3. QML traps
- Colour properties are named `fg…`/`c…` (as `tokens.py --qml` prints them): one starting
  with `on` is parsed as a signal handler and renders black.
- Blur the image before loading it: a live `MultiEffect` blur leaves rings.
- A `Repeater` gets a fixed-size model + `visible`: when the size changes it recreates
  everything and flickers.
- Test without touching the session: `qs -p <file>.qml`.

## 4. Choose and check
If a decision is still open (accent, a variant of one piece), make 3-6 small mock-ups side
by side and let the user pick. Done = looked at (screenshot), in both modes if it reads the
scheme: `caelestia scheme set -m light|dark` changes the user's whole desktop, so finish in
the mode you found it in.
