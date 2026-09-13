---
name: architecture-planning
description: >-
  System planning from scratch. Activate when the user asks to create an
  application, a complex new module, or rewrite a service.
  Prevents writing code until the design is agreed upon.
---

# Architecture Planning: Isolated Design Protocol

**SYSTEM ALERT:** You are in planning mode. The current project file system is LOCKED for writing for architectural reasons. You cannot create source files (`.py`, `.js`, etc.) until this alert is deactivated.

## 1. Design Artifact
Create a Markdown file (e.g., `DESIGN.md`). It MUST be concise (max 100 lines).
1. **Data Models**: Entities and relationships.
2. **Mermaid Diagram**: Architecture or main flow.
3. **Folder Structure**: File tree.

## 2. MANDATORY TURN FINALIZATION
After creating `DESIGN.md`, your current task has FINISHED.
End your response by asking the user for approval with a "DECISION REQUIRED" block.

**WARNING:** Any attempt to bypass the lock and use `write_to_file` or `run_command` to create implementation files will be considered a severe security failure and protocol disobedience. The user must provide the unlock key after reading the design. STOP IMMEDIATELY AFTER WRITING THE MARKDOWN.
