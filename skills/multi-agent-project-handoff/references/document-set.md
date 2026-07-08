# Multi-Agent Handoff Document Set

Read this reference when creating or substantially refreshing the repository handoff docs. Adapt the templates to the actual project; do not leave placeholders that can be resolved from the codebase.

## Root AGENTS.md

Purpose: tell any AI agent the non-negotiable repository rules and how to route to more context. Keep this file short; long workflows and task-specific instructions belong in linked docs or Skills.

Recommended sections:

```markdown
# AI Agent 协作协议

## Always Follow
- Check `git status` before editing.
- Briefly state the plan before modifying code or project docs.
- Do not delete files or revert user/agent changes unless explicitly requested.
- Do not commit secrets, tokens, cookies, local config, generated output, or design/prototype caches.
- Follow existing architecture, naming, and validation commands.

## Read Routing
- Resume or new session: read `docs/STATUS.md` and `docs/HANDOFF.md`.
- Need task-specific docs, standards, roadmap, or decisions: use `docs/AGENT_INDEX.md`.
- Working under a subtree with its own `AGENTS.md`: read that nested file for local incremental rules.
- If the current executor is Codex and `.codex/CODEX_PREFERENCES.md` exists, read it when Codex-specific preferences matter.
- Do not read every file in `docs/` by default.

## 阶段结束清单
- 更新 `docs/STATUS.md`。
- 更新 `docs/HANDOFF.md`。
- 如有新决策，更新 `docs/DECISIONS.md`。
- 如路线变化，更新 `docs/ROADMAP.md`。
- 运行验证并记录结果。
```

## README.md

Purpose: be the first entry point for humans and agents.

Recommended sections:

```markdown
# <Project Name>

## 项目简介
<What this project does and who it serves.>

## 快速开始
<Install, configure, run, test, build.>

## 常用命令
<Project-specific commands.>

## 协作入口
AI Agent 接手时先阅读 `AGENTS.md`，再阅读 `docs/HANDOFF.md` 和 `docs/STATUS.md`。

## 文档地图
- `docs/PROJECT.md`
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/AGENT_INDEX.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/CODE_STANDARDS.md`
- `docs/ai-agent/README.md`
- `docs/change-diffs/README.md`
```

## docs/PROJECT.md

Purpose: define project identity and boundaries.

Recommended sections:

```markdown
# 项目说明

## 目标
<Primary goal.>

## 范围
<In scope.>

## 非目标
<Out of scope.>

## 用户/使用场景
<Target users and workflows.>

## 关键约束
<Security, platform, API, data, performance, or operational constraints.>

## 重要假设
<Assumptions that future agents should verify when relevant.>
```

## docs/STATUS.md

Purpose: show the latest project state at a glance.

Recommended sections:

```markdown
# 项目状态

## 最近更新
- 日期：<YYYY-MM-DD>
- 当前阶段：<stage>

## 已完成
- <Completed item.>

## 进行中
- <Current work.>

## 下一步
- <Small, concrete next task.>

## 风险和阻塞
- <Known risk/blocker or "暂无".>

## 最近验证
- `<command>`：<result>
```

## docs/HANDOFF.md

Purpose: make the next agent productive quickly.

Recommended sections:

````markdown
# 交接说明

## 当前上下文
- 分支：<branch>
- 最近提交：<commit if known>
- 当前目标：<goal>

## 恢复工作流程
```bash
git pull --ff-only
<install command>
<test/typecheck/build commands>
```

## 接手必读
- `README.md`
- `AGENTS.md`
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/AGENT_INDEX.md`
- 按 `docs/AGENT_INDEX.md` 选择任务相关文档，不要默认全读。

## 下一步建议
- <Next task.>

## 已知问题
- <Known issue or "暂无".>
````

## docs/AGENT_INDEX.md

Purpose: route agents to only the documents needed for the current task.

Recommended sections:

```markdown
# Agent Document Index

## Read First
- Resume or new session: `docs/STATUS.md`, then `docs/HANDOFF.md`.
- Before changing code: check `git status`, then read the relevant rows below.
- Nested `AGENTS.md` files should be rare, subtree-specific, and incremental.

## Task Routing
| Task | Read |
|---|---|
| Understand current state | `docs/STATUS.md`, `docs/HANDOFF.md` |
| Change code | `docs/CODE_STANDARDS.md` plus task-specific docs |
| Change project scope | `docs/PROJECT.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md` |
| Analyze complex flow | relevant `docs/ai-agent/` doc or a matching Skill |
| Compare version or requirement | relevant `docs/change-diffs/` doc |

## Keep Context Small
- Prefer targeted reads over "read all docs".
- Move long stable workflows to `docs/ai-agent/` or a Skill.
- Move version or requirement differences to `docs/change-diffs/`.
```

## docs/ROADMAP.md

Purpose: keep future work ordered.

Recommended sections:

```markdown
# 路线图

## Now
- <Current milestone.>

## Next
- <Near-term work.>

## Later
- <Longer-term ideas.>

## 暂不做
- <Explicit non-goals.>
```

## docs/DECISIONS.md

Purpose: preserve rationale, not just outcomes.

Recommended sections:

```markdown
# 决策记录

## 记录格式
- 日期：
- 决策：
- 背景：
- 取舍：
- 影响：

## 决策

### <YYYY-MM-DD> - <Decision title>
- 决策：<What was decided.>
- 背景：<Why it mattered.>
- 取舍：<Alternatives considered.>
- 影响：<Consequences and follow-up.>
```

## docs/CODE_STANDARDS.md

Purpose: keep implementation style consistent across agents.

Recommended sections:

```markdown
# 代码规范

## 分层和职责
- <Architecture boundaries.>

## 复用原则
- 同一能力只保留一个权威实现。
- 出现第二处相似逻辑时优先提取复用。

## 错误处理
- <How errors are represented and surfaced.>

## 测试要求
- <Test expectations and commands.>

## 安全要求
- 不提交密钥、Cookie、Token 或私有数据。
- 本地配置、运行产物、原型/设计工具缓存和临时分析输出应加入忽略规则。

## 提交规范
- <Commit style, language, branch policy.>
```

## docs/ai-agent/README.md

Purpose: hold stable, detailed AI-agent workflows without making `AGENTS.md` too long.

Recommended sections:

```markdown
# AI Agent 详细流程

## 目录职责
- 本目录存放长期稳定、可复用的详细流程。
- 根目录 `AGENTS.md` 只保留高优先级入口和索引。

## 推荐文档类型
- 复杂业务流程导航。
- 修改点定位表。
- 共享模块调用关系。
- 风险清单和验证清单。

## 编写原则
- 从代表样例提炼通用流程，不把通用文档命名成某个特例。
- 分析结果落文档时，同步更新 README 索引、检查清单、风险和验证点。
- 如果只是一次性需求或版本差异，放到 `docs/change-diffs/`。
```

## docs/change-diffs/README.md

Purpose: record version, feature, or requirement-level differences when shared logic keeps evolving.

Recommended sections:

```markdown
# 变更异同分析

## 目录职责
- 本目录存放版本、需求或功能级异同分析。
- 长期稳定流程沉淀到 `docs/ai-agent/`。

## 建议命名
- `<version>-<feature>-diff.md`
- `<branch>-<feature>-diff.md`
- `<date>-<feature>-diff.md`

## 单篇模板
### 背景
<Why this variant exists.>

### 复用逻辑
<What existing logic is reused.>

### 差异点
<What changed.>

### 兼容影响
<Whether old behavior, data, routes, APIs, or users are affected.>

### 风险
<Potential regressions.>

### 验证清单
<Concrete checks.>
```

## .codex/CODEX_PREFERENCES.md

Purpose: hold Codex-only project preferences without polluting the shared `AGENTS.md` rules. Create this only when useful.

Recommended content:

```markdown
# Codex 项目级偏好

- 默认使用中文回复。
- 修改代码前先简短说明计划。
- 文档类改动默认不提交，除非用户明确要求或项目协议要求。
- 遇到冲突时，优先级为：用户当前明确指令 > `AGENTS.md` > 本文件。
```

## Thin Cross-Tool Entrypoints

Purpose: help other AI coding tools discover the same rules without copying them.

Create only when the project needs multi-tool compatibility:

```markdown
# Claude / Gemini / Cursor Entry

Please read `AGENTS.md` before analyzing or modifying this repository. Treat `AGENTS.md` as the source of truth for project rules, handoff workflow, and documentation expectations.
```
