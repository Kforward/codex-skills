# AI Agent Instructions

## Always Follow
- Check `git status` before editing.
- Briefly state the plan before modifying code or Skills.
- Do not delete files or revert user/agent changes unless explicitly requested.
- Do not commit secrets, tokens, cookies, local config, or generated test output.
- Keep Skill bodies lean; put project maintenance docs in this repository, not inside Skill folders.

## Read Routing
- Start with `docs/AGENT_INDEX.md` to choose the route for this task.
- Working under a subtree with its own `AGENTS.md`: read that nested file for local incremental rules.
- Do not read every file in `docs/` by default.

## End Checklist
- Update `docs/STATUS.md` or `docs/HANDOFF.md` when project state changes.
- Record new decisions in `docs/DECISIONS.md`.
- Update `docs/ROADMAP.md` when priorities change.
- Run `scripts/validate.cmd` before finishing Skill changes.
