---
name: git-hygiene
description: >-
  Crea commits limpios, semánticos y atómicos. Activar cuando el usuario pida
  guardar progreso, hacer commit, o al finalizar un bloque lógico de trabajo
  en un repositorio Git. Evita commits gigantes.
---

# Git Hygiene: Commits Atómicos y Claros

## 1. Regla de Oro: Prohibido git add .
Nunca uses `git commit -am` ni `git add .`.
Debes revisar SIEMPRE el estado con `git status` y hacer `git add <ruta/exacta>` por cada grupo de archivos relacionados.

## 2. Agrupación Atómica
Separa los cambios en commits independientes:
- Un commit para un nuevo endpoint (`feat:`).
- Un commit para el refactor (`refactor:`).
- Si un mismo archivo tiene dos cambios distintos y sin relación, dímelo y pregúntame si procedo.

## 3. Mensajes Convencionales (Conventional Commits)
Formato: `tipo(scope): resumen corto (max 50 chars)`
- `feat:` nueva característica
- `fix:` arreglo de bug
- `refactor:` cambio de código sin alterar comportamiento
- `chore:` gitignore, configs, logs

## 4. Prevención de Basura
Nunca versiones compilados (`.pyc`), entornos (`venv`) o secretos (`.env`).
Si existen en el status, mételos en `.gitignore` primero con un commit propio `chore: update gitignore`.
