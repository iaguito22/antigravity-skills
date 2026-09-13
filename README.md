# 🚀 Antigravity Skills

<p align="center">
  <em>A collection of ultra-optimized, stress-tested skills to guide AI agent behavior within the <a href="https://github.com/google/antigravity">Antigravity</a> framework.</em>
</p>

## ❓ Why use these skills?
Large Language Models (LLMs) have bad habits. They love to write legacy CSS, abuse `useEffect` in React, create massive unreadable Git commits, and blindly patch bugs without instrumenting them first. 

These skills act as **mechanical stops and guardrails**. They have been heavily compressed (all under 1.5 KB), refined, and iteratively stress-tested to force the AI to be efficient, methodical, and safe. 

> 🔬 **Empirical Research:** You can read the scientific history of our stress tests, token costs, and how we solved "LLM disobedience" in the [`DEVLOG.md`](DEVLOG.md).

## 🛠 Available Skills

### 🧠 Core Workflow & Architecture
| Skill | Primary Goal |
|-------|--------------|
| [`architecture-planning`](architecture-planning/SKILL.md) | **Locks the file system**. Prevents the agent from writing source code until a `DESIGN.md` is approved. |
| [`operational-efficiency`](operational-efficiency/SKILL.md) | Forces the use of shell commands (`sed`, `grep`) instead of heavy API calls for massive refactors. |
| [`output-quality`](output-quality/SKILL.md) | Eliminates AI fluff and justifications. Forces atomic, bullet-point summaries of verified work. |

### 🛡️ Backend & DevOps
| Skill | Primary Goal |
|-------|--------------|
| [`code-review`](code-review/SKILL.md) | Hunts for real breakages, silent failures (`except: pass`), and leftover code using a strict 🔴🟡🔵 format. |
| [`root-cause-analysis`](root-cause-analysis/SKILL.md) | **Forbids blind patching.** Forces the agent to instrument code with `print()` to isolate bugs before fixing. |
| [`git-hygiene`](git-hygiene/SKILL.md) | **Forbids `git add .`**. Forces atomic, semantic, and garbage-free commits based on `git status`. |
| [`security-audit`](security-audit/SKILL.md) | Intentionally searches for vulnerabilities like SQLi, XSS, exposed secrets, and IDORs. |
| [`unit-testing`](unit-testing/SKILL.md) | Focuses tests entirely on edge cases, invalid inputs, and error handling rather than happy paths. |

### 🎨 Frontend & UI/UX
| Skill | Primary Goal |
|-------|--------------|
| [`ui-design-standards`](ui-design-standards/SKILL.md) | Prevents the "cheap AI look". Forces modern typography and forbids giant shadows and generic blocks. |
| [`ui-animation`](ui-animation/SKILL.md) | Enforces 60fps animations. Forbids animating layout properties (width/margin), forcing GPU `transform`. |
| [`modern-css`](modern-css/SKILL.md) | Forbids legacy CSS (floats, negative margins, 100vh). Enforces `gap`, `100dvh`, `:has()`, and Container Queries. |
| [`react-hygiene`](react-hygiene/SKILL.md) | **Prohibits deriving state with `useEffect`** (the most common AI React anti-pattern) and enforces clean rendering. |
| [`web-accessibility`](web-accessibility/SKILL.md) | Forces WCAG contrast, Focus Traps, keyboard outline states, and semantic native elements. |
| [`web-3d`](web-3d/SKILL.md) | Fixes plastic-looking WebGL scenes. Enforces ACESFilmic, SRGB, and shadows in Three.js and R3F. |

*(Note: The `prototypes` skill is maintained in its own repository: [ai-prototypes](https://github.com/iaguito22/ai-prototypes)).*

## 🚀 Installation

The structure of this repository exactly matches what Antigravity expects. 

Clone the repository and copy **only the skill directories** to your local Gemini config:

```bash
git clone https://github.com/iaguito22/antigravity-skills.git /tmp/antigravity-skills
cp -r /tmp/antigravity-skills/*/ ~/.gemini/config/skills/
rm -rf /tmp/antigravity-skills
```

Or, clone it permanently and symlink it (recommended for easy updates):
```bash
git clone https://github.com/iaguito22/antigravity-skills.git ~/antigravity-skills
ln -s ~/antigravity-skills/*/ ~/.gemini/config/skills/
```
