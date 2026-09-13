---
name: react-hygiene
description: >-
  Strict standards for React. Activate whenever writing React or Next.js
  components to prevent hook abuse.
---

# React Hygiene: Stop the Hook Madness

LLMs are experts at writing React dependency spaghetti. Follow this absolute rule:

## 1. The `useEffect` Terror
**FORBIDDEN** to use `useEffect` to derive state.
If you have `items` and want `filteredItems`, DO NOT create a second state or effect. Calculate it directly in the render body or use `useMemo`.
`useEffect` is **EXCLUSIVELY** for synchronizing with external systems (browser listeners, pure network calls).

## 2. Functions in Dependencies
Never pass an anonymous inline function to a memoized child. Use `useCallback`. Watch out for infinite dependency arrays.
