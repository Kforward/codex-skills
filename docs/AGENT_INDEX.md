# Agent Route Index

Use this first-level route only to choose the next route file. Do not treat it as a full document map.

## Route By Task Type

| Task Type | Next Route |
|---|---|
| 接手项目、恢复上下文、查看当前进度 | `docs/routes/PROJECT_ROUTING.md` |
| 修改代码、脚本、校验、架构或安全规范 | `docs/routes/DEVELOPMENT_ROUTING.md` |
| 新增、维护、选择或安装 Skill | `docs/routes/SKILL_ROUTING.md` |
| AI Agent 协作流程、交接、review、文档瘦身 | `docs/routes/AI_AGENT_ROUTING.md` |
| 版本差异、需求变更、功能对比 | `docs/routes/CHANGE_ROUTING.md` |

## Keep Context Small

- Read exactly one route file first, then only the concrete docs it names.
- Prefer targeted reads over "read all docs".
- If a nested directory contains its own `AGENTS.md`, read it only when working in that subtree; nested files should contain incremental local rules, not copied root rules.
