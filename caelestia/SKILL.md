---
name: caelestia
description: >-
  Caelestia style (the Hyprland/Quickshell shell) for the user's own interfaces: a game HUD
  or menus, app themes (Spotify/Spicetify, mpv, SDDM), widgets, QML overlays, dashboards and
  personal tools. Use it on "caelestia style", "like caelestia", "like my desktop",
  "estilo caelestia", "como caelestia", "como mi escritorio", or when building the UI of
  one of the user's own projects with no style given. Not for business websites (that is
  the `web` skill).
---

# Caelestia, the way it looks on the desktop

The scripts are run, not read.

## 1. Tokens (one call, paste as is)
`python3 ~/.gemini/config/skills/caelestia/tokens.py` → a `:root` block with the role
colours of the current wallpaper scheme, radii, spacing, curves and glass. `--qml` for QML,
`--neutral` for a neutral palette (anything that won't read `scheme.json`: a published
page, a game). If it runs on the user's machine, read
`~/.local/state/caelestia/scheme.json` live and follow its light/dark `mode`.

## 2. What makes it Caelestia
- **Colour by role, one accent.** Surfaces + `primary`; the accent can come from the
  content (album art's dominant colour, animated with `@property`) or not exist at all
  (white accent). Status colours (sectors, flags, warnings) stay vivid, not pastel: over a
  busy scene pastels disappear.
- **Concentric radii from one scale** (4 · 8 · 12 · 16 · 28 · pill): inner radius = outer
  radius − the gap between them (panel 28 → gap 12 → card 16 → artwork 8). Buttons, chips,
  tabs and status bars are pills; icons and positions are circles.
- **Glass with a job**: panels at ~78 % of `surfaceContainer` + `blur(16px) saturate(1.4)`,
  an almost invisible 1 px border and a wide soft shadow. Accent sheen or tint only on the
  INSIDE (inset): a coloured outer shadow tints whatever is underneath.
- **Type**: Rubik (the shell's sans) or Figtree, weights 500-800, `tabular-nums` for
  figures; big numbers bold (a 128 px clock with `letter-spacing: -2px`). Material Symbols
  Rounded icons; CaskaydiaCove NF for mono.
- **Motion that transforms**: what appears grows out of what was there (an iris closing, a
  panel expanding, a window that opens with the same aspect ratio and radius as the iris
  before it so they join). M3 curves from the tokens, 150-650 ms. Never a hard cut, a white
  flash or a background peeking between two states.
- **Clean**: no visible scrollbars, no focus ring or halo (with a keyboard, at most the
  pill's background changes), hover = a soft background or border on the row. Text over a
  photo or video is always white; in light mode, bars over video stay dark
  (`inverseSurface`).
- **No decoration**: no chip saying "Caelestia", no spaced-out uppercase labels; every
  piece shows data or does something.

## 3. QML traps
- Don't name a property `onSurface`/`onPrimary`: QML parses it as a signal handler and it
  renders black. `tokens.py --qml` already uses `fg…`.
- `MultiEffect` blur leaves rings: blur the image beforehand, not live.
- A `Repeater` whose `model` changes size recreates everything and flickers: fixed model +
  `visible`.
- Test without touching the session: `qs -p <file>.qml`.

## 4. Choose and check
If a decision is still open (accent, a variant of one piece), make 3-6 small mock-ups side
by side and let the user pick; don't decide with a single one. Done = looked at (screenshot)
in both modes if it reads the scheme. `caelestia scheme set -m light|dark` changes the
user's whole desktop: put it back as it was.
