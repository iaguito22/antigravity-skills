---
name: web-accessibility
description: >-
  Forces compliance with accessibility (a11y) standards. Activate whenever
  generating interactive components, modals, forms, or navigation to ensure
  contrast and keyboard support.
---

# Web Accessibility: Zero Excuses

Never sacrifice accessibility for aesthetics.

## 1. Keyboard Navigation
Every clickable element must be reachable with `Tab`.
- **NEVER** remove the `outline` on focus without a clear visual replacement (`:focus-visible`).
- Modals must apply a Focus Trap.

## 2. Real Semantics
- Do not use `<div onClick={...}>`. Use a `<button>`. If you hate default styles, reset them (`all: unset`).
- Use `<nav>`, `<main>`, `<article>`, and logical heading levels (`h1` to `h6`).

## 3. Contrast and Tap Targets
- No pale gray text on white. Ensure WCAG AA minimum contrast.
- On mobile, clickable touch targets must be at least `44px` by `44px`.
