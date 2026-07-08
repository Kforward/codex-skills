# 决策记录

## 记录格式

- 日期：
- 决策：
- 背景：
- 取舍：
- 影响：

## 决策

### 2026-07-01 - 将个人 Skill 项目化

- 决策：创建独立 `codex-skills` 项目，集中维护可分发 Skills。
- 背景：单机 `.codex/skills` 目录不适合跨端同步和版本管理。
- 取舍：Skill 本体保持精简，安装说明和维护说明放在项目根目录。
- 影响：其他端可以拉取项目并运行安装脚本获得相同 Skill。

### 2026-07-01 - 安装脚本默认不覆盖已有 Skill

- 决策：安装脚本默认跳过已存在的目标 Skill，只有显式 `-Force` 或 `--force` 才覆盖。
- 背景：其他端可能已经有本地修改，默认覆盖会造成上下文丢失。
- 影响：更新 Skill 时需要明确使用覆盖参数，或者先手动检查差异。

### 2026-07-03 - 将长流程与工具兼容规则纳入 handoff Skill

- 决策：增强 `multi-agent-project-handoff`，补充短入口 `AGENTS.md`、`docs/ai-agent/`、`docs/change-diffs/`、可选 `.codex/CODEX_PREFERENCES.md` 和跨工具薄入口。
- 背景：真实项目里 `AGENTS.md` 变长后会占用上下文并稀释高优先级规则；不同 AI 工具也不一定自动读取同一个规则文件。
- 取舍：核心规则默认生成，Codex 专属偏好和跨工具入口通过参数显式生成。
- 影响：新项目能更早获得分层协作结构；具体业务流程分析仍应留在项目文档或未来独立 Skill。

### 2026-07-03 - 新增复杂旧前端流程分析 Skill

- 决策：新增 `legacy-frontend-flow-analysis`，专门沉淀从路由/页面/行为入口追踪旧前端业务流程的方法。
- 背景：真实旧前端项目中，业务流程常散落在路由、组件、mixins、store、API、缓存、埋点和跳转工具里，不适合放进通用 handoff Skill。
- 取舍：把代码调查方法单独成 Skill，保留 handoff Skill 的协作交接职责。
- 影响：后续遇到复杂 Vue/React/H5 历史项目时，可直接使用该 Skill 输出流程图、隐式依赖、风险和验证清单。

### 2026-07-06 - 用真实项目反馈优化既有 Skill

- 决策：把真实旧前端项目会话中反复出现的可复用经验补入既有 `multi-agent-project-handoff` 和 `legacy-frontend-flow-analysis`。
- 背景：会话暴露出本地分析产物误入暂存、公共 helper 异常分支影响面、非核心依赖阻塞页面、第三方 SDK 替换边界等通用问题。
- 取舍：只沉淀通用检查项和模板，不写入具体项目名、版本号、业务 key 或页面路径。
- 影响：后续新项目交接和旧前端分析会更早检查本地产物、公共方法兜底、非阻塞边界和 SDK 适配层。

### 2026-07-06 - 建立 Skill Catalog 和路由校验框架

- 决策：新增 `docs/SKILL_CATALOG.md` 和 `docs/SKILL_ROUTING.md`，并在 `scripts/validate.py` 中校验 description 路由质量和 catalog 覆盖。
- 背景：Skill 数量增长后，仅靠记忆或人工判断容易选错 Skill；而 Codex 隐式触发主要依赖 `name` 和 `description`。
- 取舍：先做轻量 catalog 与基础校验，不引入总控 Skill、外部索引服务或复杂关键词相似度算法。
- 影响：新增或调整 Skill 时必须维护 catalog；后续可按 Skill 数量增长再增加关键词重叠检查和分组策略。

### 2026-07-08 - 采用薄 AGENTS 和按需文档路由

- 决策：根 `AGENTS.md` 只保留硬规则和读取路由，新增 `docs/AGENT_INDEX.md` 作为任务到文档的索引；嵌套 `AGENTS.md` 只用于子目录真实增量规则。
- 背景：单个 AGENTS 文档持续膨胀会增加 Codex 上下文成本，也会让 Agent 默认读取过多无关规则。
- 取舍：保留统一 `docs/` 文档中心和官方 `AGENTS.md` 机制，不引入自定义 `AGENTS.override.md` 文件名。
- 影响：`multi-agent-project-handoff` 初始化的新项目默认生成薄入口结构；校验脚本会检查根 AGENTS 长度和 AGENT_INDEX 路由。

### 2026-07-08 - 引入 L0/L1/L2 分级文档路由

- 决策：将项目文档路由拆成 L0 根 `AGENTS.md`、L1 `docs/AGENT_INDEX.md` 和 L2 `docs/routes/*.md`。
- 背景：随着单一职责文档增加，根入口或单层索引都会逐渐变成大目录，仍会浪费 Agent 上下文。
- 取舍：先保留统一 `docs/` 中心和现有文档位置，只新增轻量 route files；暂不把所有文档迁移到更深目录。
- 影响：新增任务子类型时优先更新对应 L2 route；只有出现新的任务大类时才更新 L1 索引。
