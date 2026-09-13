---
name: ui-animation
description: >-
  Animations and interactions that feel good and don't jank. Use when the task
  includes animating, transitions, movement, scroll, hover, entrances/exits,
  or when the user complains about jank or slow animations.
---

# Animation that feels good

A bad animation is noticeable even if you don't know why. It's usually one of three things: it lasts too long, has the wrong curve, or animates the wrong property.

## Only two properties are free
`transform` and `opacity`. Period. They are the only ones the browser can animate on the GPU without recalculating the page.

- **Never animate** `width`, `height`, `top`, `left`, `margin`, `padding`. Each frame forces a layout recalculation and causes jank.
- Need to move something? `transform: translate()`. Scale it? `scale()`.
- Real size change needed? Use the FLIP technique.

## Duration: shorter than you think
Keep hover transitions between 150ms and 250ms. Never use 500ms for a hover effect.
