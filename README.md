# Antigravity Skills

A collection of ultra-optimized, stress-tested *skills* to guide AI agent behavior within the [Antigravity](https://github.com/google/antigravity) environment.

These skills have been compressed (all between 1 KB and 1.5 KB), refined, and iteratively stress-tested to force the model to be efficient, methodical, and safe. You can read the scientific history of these tests and our empirical findings (token costs per KB, model disobediences under pressure, etc.) in the [`DEVLOG.md`](DEVLOG.md).

## 🛠 Available Skills
| [`ui-design-standards`](ui-design-standards/SKILL.md) | Prevents the "cheap AI look". Forces modern typography and forbids giant shadows and generic blocks. |
| [`ui-animation`](ui-animation/SKILL.md) | Enforces 60fps animations. Forbids animating layout properties like width/margin, forcing GPU-accelerated transforms. |
| [`web-3d`](web-3d/SKILL.md) | Fixes plastic-looking WebGL scenes. Enforces ACESFilmic, SRGB, and casting/receiving shadows in Three.js and R3F. |
| [`modern-css`](modern-css/SKILL.md) | Forbids legacy CSS (floats, negative margins, 100vh). Enforces `gap`, `dvh`, `:has()`, and Container Queries. |
| [`react-hygiene`](react-hygiene/SKILL.md) | Prohibits deriving state with `useEffect` (the most common AI React anti-pattern) and enforces clean rendering. |
| [`web-accessibility`](web-accessibility/SKILL.md) | Forces WCAG contrast, Focus Traps, keyboard outline states, and semantic native elements. |

| Skill | Primary Goal |
|-------|--------------|
| [`code-review`](code-review/SKILL.md) | Finds breakages, silent failures, and leftover code with a strict 🔴🟡🔵 reporting format. |
| [`operational-efficiency`](operational-efficiency/SKILL.md) | Uses shell commands (`sed`, `grep`) instead of API calls for massive refactors to save tokens. |
| [`output-quality`](output-quality/SKILL.md) | Eliminates fluff, justifications, and generates atomic summaries of what was verified. |
| [`unit-testing`](unit-testing/SKILL.md) | Focuses tests on edge cases, invalid inputs, and error handling rather than happy paths. |
| [`git-hygiene`](git-hygiene/SKILL.md) | Forbids global `git add .`. Forces atomic, semantic, and garbage-free commits. |
| [`root-cause-analysis`](root-cause-analysis/SKILL.md) | Forbids blind patching. Forces the agent to instrument the code with prints to isolate unknown bugs. |
| [`security-audit`](security-audit/SKILL.md) | Intentionally searches for vectors like SQLi, XSS, exposed secrets, and IDORs. |
| [`architecture-planning`](architecture-planning/SKILL.md) | Locks the file system, preventing the agent from writing source code until the design document is accepted. |

## 🚀 Installation

The structure of this repository exactly matches what Antigravity expects. 

Clone the repository and copy **only the skill directories** to your local Gemini config:

```bash
git clone https://github.com/iaguito22/antigravity-skills.git /tmp/antigravity-skills
cp -r /tmp/antigravity-skills/*/ ~/.gemini/config/skills/
rm -rf /tmp/antigravity-skills
```

Or, if you prefer to clone it permanently and symlink it (recommended to keep them updated):
```bash
git clone https://github.com/iaguito22/antigravity-skills.git ~/antigravity-skills
# Remove the loose markdown files from the target so only dirs are linked
ln -s ~/antigravity-skills/*/ ~/.gemini/config/skills/
```
