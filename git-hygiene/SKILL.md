---
name: git-hygiene
description: >-
  Use for "commit", "commit this", "save the changes", "push this" (also "haz commit",
  "guarda los cambios"), or after finishing a logical block of work in a Git repo.
  Clean, atomic, conventional commits.
---

# Clean commits

1. **`git status` and `git diff --stat` in a single call.** Never `git add .` or `commit -am`:
   `git add <path>` per group.
2. **One commit per logical change**: a new feature (`feat:`), a fix (`fix:`), a cleanup
   (`refactor:`), config (`chore:`). One file with two unrelated changes → ask.
3. **Format**: `type(scope): summary` in ≤ 50 characters, in the repo's language
   (check `git log --oneline -5`).
4. **Junk**: `.pyc`, `__pycache__`, `venv`, `node_modules`, `.env` → into `.gitignore` in its
   own commit (`chore: update gitignore`). If there's an unversioned secrets file
   (`.env`, keys), mention it in the report.
5. **No push** unless asked.

Report: the commits (`git log --oneline -N`) and the final `git status`.
