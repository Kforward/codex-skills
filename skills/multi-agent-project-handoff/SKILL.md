---
name: multi-agent-project-handoff
description: "Initialize or update repository-level documentation and workflows for multi-user, multi-device, multi-AI-agent collaboration. Use when creating a new project, making a repository AI-agent-ready, adding or slimming AGENTS.md/README/docs handoff files, resuming work after git pull, enforcing document-as-shared-memory, adding project-level Codex preferences or thin cross-tool AI entrypoints, defining feature-scoped commit rules, or improving cross-agent handoff conventions."
---

# Multi-Agent Project Handoff

## Purpose

Establish a repository-level "document as shared memory" workflow so different users, devices, and AI agents can continue the same project without relying on hidden chat history.

Keep universal collaboration rules in this skill. Write project-specific facts, progress, decisions, risks, and next steps into the target repository.

## Decision Flow

- For a new project or a repository missing handoff docs, create the standard document set, then customize it from the actual project context.
- For an existing project, read current docs first and merge improvements; do not overwrite user-authored content blindly.
- For a resumed project after another agent worked on it, pull latest changes if requested, then reread the handoff docs before editing code.
- For a request to improve this reusable workflow itself, update this skill rather than copying the same rules into every project.

Read `references/document-set.md` when creating or substantially refreshing the handoff docs.

## Standard Document Set

Prefer this structure unless the repository already has an equivalent convention:

- `AGENTS.md`: short, high-priority rules for AI agents working in this repository.
- `README.md`: human and agent entry point with setup, commands, and documentation map.
- `docs/PROJECT.md`: project purpose, scope, constraints, assumptions.
- `docs/STATUS.md`: current state, completed work, next actions, known risks.
- `docs/HANDOFF.md`: resume workflow, environment notes, validation commands, latest handoff.
- `docs/ROADMAP.md`: now/next/later milestones and out-of-scope items.
- `docs/DECISIONS.md`: architecture/product decisions and rationale.
- `docs/CODE_STANDARDS.md`: coding, testing, security, naming, and commit conventions.
- `docs/ai-agent/README.md`: stable, detailed AI-agent workflow docs that should not bloat `AGENTS.md`.
- `docs/change-diffs/README.md`: feature, version, or requirement-level difference analyses.

If the project has a different docs layout, map these responsibilities to existing files instead of duplicating them.

Optional additions:

- `.codex/CODEX_PREFERENCES.md`: Codex-only project preferences referenced from `AGENTS.md`.
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules`: thin cross-tool entrypoints that only point readers to `AGENTS.md`.

## Workflow

1. Inspect the repository:
   - Check `git status`.
   - List existing root docs and `docs/` files.
   - Read existing `AGENTS.md`, `README.md`, and relevant docs before writing.
2. Decide the mode:
   - Bootstrap missing handoff docs.
   - Retrofit and improve existing docs.
   - Resume after a pull or another agent's changes.
3. Bootstrap when useful:
   - Run `scripts/init_handoff_docs.py <repo-path> --project-name "<name>"` from this skill to create missing skeleton files.
   - Add `--with-codex-preferences` when the project needs Codex-specific preferences.
   - Add `--with-compat-entrypoints` when other AI tools should be nudged toward `AGENTS.md`.
   - The script skips existing files by default; use `--force` only when the user explicitly wants regeneration.
4. Customize the docs:
   - Replace placeholders with facts from the actual repository.
   - Mark uncertain items as `TBD` or `Assumption`; do not invent project state.
   - Include the exact validation commands this repo expects.
   - Include the cross-client startup prompt if another AI agent may join later.
   - Generalize from representative examples; do not name a long-lived guide after a one-off page, module, or feature unless the document is intentionally specific.
5. Keep code and docs together:
   - After meaningful code changes, update `STATUS.md` and `HANDOFF.md`.
   - Update `DECISIONS.md` for architecture/product decisions.
   - Update `ROADMAP.md` when priorities or milestones change.
   - Update feature/version difference docs when a new variant reuses shared logic but changes business behavior.
6. Validate:
   - Run the repository's normal checks when available.
   - For docs-only changes, still run lightweight checks if the project protocol asks for them.
   - Report any checks that could not be run.

## Cross-Agent Resume Protocol

When resuming a collaborative project, follow this order before making changes:

1. `git status`
2. `git pull --ff-only` if the user asked to sync and the worktree permits it.
3. Read `AGENTS.md`.
4. Read `README.md`.
5. Read `docs/PROJECT.md`.
6. Read `docs/STATUS.md`.
7. Read `docs/HANDOFF.md`.
8. Read `docs/ROADMAP.md`.
9. Read `docs/DECISIONS.md`.
10. Read `docs/CODE_STANDARDS.md`.
11. Summarize the current state and next planned change before editing.

## Documentation Architecture

Keep `AGENTS.md` short enough to be read reliably. It should contain mandatory rules, the read order, document links, and critical checklists. Move long workflows, domain walkthroughs, and analysis templates to `docs/ai-agent/` or another linked docs folder.

When a representative page, module, or feature is used for discovery, write the durable document as a general workflow. Keep the representative as an example or verification anchor, not the document identity.

When comparing a new feature or version against existing shared logic, write a difference analysis under `docs/change-diffs/` or the repository's equivalent folder. Capture what is shared, what changed, compatibility impact, risks, and validation points.

## Git Commit Rules

Only commit when the user asks for git operations or the repository protocol explicitly requires a stage-end commit.

When committing:

- Split commits by feature point, fix point, or documentation point.
- Keep unrelated formatting, refactors, docs, and business logic out of the same commit.
- Do not stage unrelated user or agent changes.
- Use Conventional Commits: `<type>(<scope>): <subject>`.

## Cross-Client Startup Prompt

When the user opens the repository in another client or with another AI agent, suggest this prompt:

```text
请先阅读本仓库根目录的 AGENTS.md、README.md，以及 docs/PROJECT.md、docs/STATUS.md、docs/ROADMAP.md、docs/HANDOFF.md、docs/DECISIONS.md、docs/CODE_STANDARDS.md。
严格按照 AGENTS.md 中的协作协议继续开发。
在理解当前项目目标、已完成内容、待完成内容、代码规范和关键决策前，不要修改代码。
开始前请先总结你理解到的当前状态和下一步计划。
```

## Guardrails

- Do not delete existing docs or project files unless the user explicitly asks.
- Do not overwrite local changes from another user or agent.
- Prefer merging into existing conventions over imposing a new structure.
- Keep shared memory in the repository, not only in chat.
- Keep the skill generic; keep project facts inside the target repository.
- Review documentation for real conflicts, ambiguity, excessive length, or over-specific naming; do not rewrite wording just for polish.
