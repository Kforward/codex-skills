# Agent Document Index

Use this file to choose only the project documents needed for the current task. The root `AGENTS.md` is intentionally short and should not duplicate these details.

## Read First

- Resume or new session: `docs/STATUS.md`, then `docs/HANDOFF.md`.
- Before changing code or Skills: check `git status`, then read the task-specific rows below.
- If a nested directory contains its own `AGENTS.md`, read it only when working in that subtree; nested files should contain incremental local rules, not copied root rules.

## Task Routing

| Task | Read |
|---|---|
| Understand current project state | `docs/STATUS.md`, `docs/HANDOFF.md` |
| Change or create a Skill | `docs/SKILL_CATALOG.md`, `docs/SKILL_ROUTING.md`, target `skills/<name>/SKILL.md` |
| Change install or validation scripts | `docs/CODE_STANDARDS.md`, `README.md`, related files under `scripts/` |
| Change project scope or maintenance process | `docs/PROJECT.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md` |
| Update handoff, status, or roadmap only | Relevant target doc plus `docs/CODE_STANDARDS.md` if validation rules change |
| Analyze a complex legacy frontend flow in another repo | Use `$legacy-frontend-flow-analysis`; write durable findings to that repo, not here |
| Initialize another repo for multi-agent collaboration | Use `$multi-agent-project-handoff`; customize docs from that repo's facts |

## Document Roles

- `docs/PROJECT.md`: project purpose, scope, non-goals, and constraints.
- `docs/STATUS.md`: latest completed work, current state, next steps, risks, and recent validation.
- `docs/HANDOFF.md`: resume workflow, required context, and next-agent guidance.
- `docs/ROADMAP.md`: now/next/later priorities.
- `docs/DECISIONS.md`: durable decisions and rationale.
- `docs/CODE_STANDARDS.md`: repository maintenance, script, Skill, security, and commit rules.
- `docs/SKILL_CATALOG.md`: Skill selection catalog for humans and agents.
- `docs/SKILL_ROUTING.md`: rules for Skill names, descriptions, catalog coverage, and growth strategy.

## Keep Context Small

- Prefer targeted reads over "read all docs".
- Move long stable workflows to `docs/ai-agent/` or a Skill.
- Move version or requirement differences to `docs/change-diffs/`.
- Keep nested `AGENTS.md` files rare and short; use them only for subtree-specific commands, tests, or constraints.
