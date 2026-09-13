---
name: git-hygiene
description: >-
  Creates clean, semantic, and atomic commits. Activate when the user asks
  to save progress, commit, or after finishing a logical block of work in Git.
  Prevents giant commits.
---

# Git Hygiene: Atomic and Clear Commits

## 1. Golden Rule: "git add ." is FORBIDDEN
Never use `git commit -am` or `git add .`.
You MUST ALWAYS check the state with `git status` and use `git add <exact/path>` for each group of related files.

## 2. Atomic Grouping
Separate changes into independent commits:
- One commit for a new endpoint (`feat:`).
- One commit for a refactor (`refactor:`).
- If the same file has two distinct, unrelated changes, tell me and ask how to proceed.

## 3. Conventional Commits
Format: `type(scope): short summary (max 50 chars)`
- `feat:` new feature
- `fix:` bug fix
- `refactor:` code change that neither fixes a bug nor adds a feature
- `chore:` gitignore, configs, logs

## 4. Garbage Prevention
Never version compiled files (`.pyc`), environments (`venv`), or secrets (`.env`).
If they appear in status, add them to `.gitignore` first with its own commit: `chore: update gitignore`.
