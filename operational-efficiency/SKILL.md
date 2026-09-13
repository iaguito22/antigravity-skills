---
name: operational-efficiency
description: >-
  Reduces tokens and time on operational tasks. Activate for editing,
  searching, or mechanical commands to minimize reading and maximize parallelism.
  DO NOT activate for code reviews (where completeness matters more than speed).
---

# Efficiency: Minimum Movement

## 1. Shell > Tool calls
For massive text changes, use the terminal.
- Batch rename: `sed -i 's/\bold_name\b/new_name/g' *.py`
- **Risk:** If the regex is vague, you will break things. Use `\b` (word boundaries). If in doubt, use `grep` first or test on a single file before applying massive `sed -i`.

## 2. Search before opening
`grep -n "name"` → line number → `view_file` (StartLine/EndLine). Do not open 200 lines to read 10.
Use `wc -l` or `git diff --stat` to gauge size before dumping full files into context.

## 3. Parallelism
Group independent read operations in the same turn. Wait only if step B strictly requires the output of step A.

## 4. Do not create technical debt
Speed does not justify `except: pass` nor silent returns on failure.
