---
name: react-hygiene
description: >-
  Use whenever writing or editing React/Next.js/JSX components: React component, hook,
  useEffect, state, props (also "componente React"). Prevents hook misuse.
---

# React without hook spaghetti

1. **No `useEffect` to derive state.** `filtered` from `items` + `query` is computed during
   render (or `useMemo` if it's expensive). `useEffect` is only for syncing with the outside:
   listeners, network, timers, always with cleanup (`return () => …`, `AbortController`).
2. **Minimal state**: if it can be computed from other state or props, it isn't state.
3. **Stable keys** (`id`), never the index in lists that get filtered or reordered.
4. **`useCallback`/`useMemo` only with a reason**: a child wrapped in `memo`, or an expensive
   calculation. Don't add them "just in case".
5. Controlled inputs with an associated `<label>`.

Check: if the project has build/lint (`package.json`), run it once. A standalone `.jsx`
can't be opened in the browser: check it by compiling
(`npx -y esbuild X.jsx --loader:.jsx=jsx --outfile=/dev/null`) plus one case in `node`.
Don't build a throwaway `index.html` unless asked. If there's already a page, type into
inputs with `agy-ver escribe '<selector>' 'text'` (setting `.value` doesn't fire `onChange`).
