---
name: modern-css
description: >-
  Forces the model to use modern CSS properties instead of legacy ones.
  Activate for any HTML/CSS layout task.
---

# Modern CSS: Code like it's 2024

Ignore legacy CSS from your training data. Apply modern standards:

## 1. Box Model and Spacing
- **Negative margins are forbidden**.
- If using Flexbox or Grid, ALWAYS separate children using `gap`. Do not use margins on child elements for spacing.

## 2. Units and Viewport
- Never use `100vh` for full screen. It fails miserably on mobile Safari. ALWAYS use `100dvh`.

## 3. Magic Selectors
- Use `:has()` for parent component states based on children.
- Use **Container Queries** (`@container`) instead of media queries for reusable components.

## 4. Native Styles
- Exploit `scroll-behavior: smooth`, `backdrop-filter`, and native `aspect-ratio`. Do not simulate them with JS.
