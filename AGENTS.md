# AI Agent Instructions

## Always Follow
- Check `git status` before editing.
- Briefly state the plan before modifying code or Skills.
- Do not delete files or revert user/agent changes unless explicitly requested.
- Do not commit secrets, tokens, cookies, local config, or generated test output.
- Keep Skill bodies lean; put project maintenance docs in this repository, not inside Skill folders.

## Read Routing
- Resume or new session: read `docs/STATUS.md` and `docs/HANDOFF.md`.
- Need to choose or modify a Skill: read `docs/SKILL_CATALOG.md` and `docs/SKILL_ROUTING.md`.
- Need task-specific docs, standards, roadmap, or decisions: use `docs/AGENT_INDEX.md`.
- Working under a subtree with its own `AGENTS.md`: read that nested file for local incremental rules.
- Do not read every file in `docs/` by default.

## End Checklist
- Update `docs/STATUS.md` or `docs/HANDOFF.md` when project state changes.
- Record new decisions in `docs/DECISIONS.md`.
- Update `docs/ROADMAP.md` when priorities change.
- Run `scripts/validate.cmd` before finishing Skill changes.
