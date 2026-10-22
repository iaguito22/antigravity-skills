# Writing for agy (Antigravity CLI)

The agy branch of [`writing-for-agents`](SKILL.md): where each kind of document lives, what
it costs, and how to tell a live line from a no-op. Everything about the writing itself is
in `SKILL.md`.

## Where each piece lives
- `~/.gemini/config/GEMINI.md`: always loaded, every turn. Only what changes the model's
  behaviour in every kind of task (format, how to check what it built, the user's habits).
- `~/.gemini/config/rules/*.md`: frontmatter `trigger: always_on` (same cost as GEMINI.md)
  or `trigger: model_decision` with a `description` (a pointer, like a skill's).
- `~/.gemini/config/skills/<name>/SKILL.md`: frontmatter `name` + `description`. Only the
  description is paid every turn; the body is read when it fires. Skills fire only through
  the description, so it carries the user's real words for each branch (Spanish and English).
- `~/.gemini/config/hooks.json` + a script: for what must happen even when the model
  forgets (blocking a destructive command, a recipe injected after it touches a file). A
  rule the model can ignore is a suggestion; a hook is a guardrail. All hooks go in ONE
  named group: separate groups overwrite each other.
- Scripts next to a skill: anything deterministic (a die, a linter, a generator, a tested
  module) beats prose. Write "the scripts are run, not read" and give the exact command.

## Measuring (the no-op test, for real)
- Run the job on a factory agy first (`agy -p "<prompt>" --model <model> --output-format json`
  in an empty folder) and only write a line for what it gets wrong. A line that describes
  what the model already does is a no-op: delete it.
- Then run it again with the document and compare output tokens, time and the result itself
  (open it, run it). Watch the quota (`agy -p /usage`): each model has its own limit.
- No time or quota to measure? Then the report says so: `No verificado: falta medirlo
  contra agy de fábrica`, and the document stays short (every unmeasured line is a guess).
- Asking the model "is X in your instructions?" gives false yeses. Check with a rule that
  changes BEHAVIOUR.
