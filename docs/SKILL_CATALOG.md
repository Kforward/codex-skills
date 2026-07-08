# Skill Catalog

本文件是给人和其他 AI Agent 使用的 Skill 索引。Codex 运行时仍主要依赖每个 `SKILL.md` 的 `name` 和 `description` 触发 Skill；本 catalog 用来维护边界、示例 prompt 和增长后的可发现性。

## 使用方式

- 已确定要用哪个 Skill 时，优先在提示中显式写 `$skill-name`。
- 不确定时，先按“适用场景 / 不适用场景 / 触发关键词”选择最贴近的 Skill。
- 新增 Skill 时必须同步补充本文件，并运行 `.\scripts\validate.cmd`。

## `multi-agent-project-handoff`

- 适用场景：初始化或更新仓库级多用户、多端、多 AI Agent 协作文档；整理 `AGENTS.md`、`README.md`、`docs/` 交接体系和 L0/L1/L2 分级文档路由；规范阶段结束文档同步、功能点提交和跨工具入口。
- 不适用场景：分析某个具体业务流程的代码调用链；修复普通 bug；创建一次性项目说明文档。
- 触发关键词：新项目、协作规范、AGENTS.md、handoff、共享记忆、多端、多 Agent、文档分层、分级路由、按需读取、阶段提交、恢复流程。
- 示例 prompt：`使用 $multi-agent-project-handoff 初始化这个仓库的多 Agent 协作文档。`
- 主要资源：`references/document-set.md`、`scripts/init_handoff_docs.py`。
- 边界提示：项目事实写入目标仓库文档，不写回 Skill 本体。

## `legacy-frontend-flow-analysis`

- 适用场景：分析复杂旧前端业务流程；从路由、页面、组件、mixin/composable、store、API、缓存、埋点和跳转链路追踪行为；评估共享 helper、第三方 SDK 替换、版本变体和异常兜底影响。
- 不适用场景：新建仓库协作文档；只需要普通代码风格 review；不涉及业务调用链的简单组件改色或文案替换。
- 触发关键词：旧前端、Vue、React、H5、路由、mixin、业务流程、调用链、公共 helper、SDK 替换、埋点、跳转、小程序、兜底、变体分析。
- 示例 prompt：`使用 $legacy-frontend-flow-analysis 分析这个旧前端支付返回流程的调用链和风险。`
- 主要资源：`references/analysis-templates.md`。
- 边界提示：项目私有路由、埋点 code、业务 key 和版本差异写入目标仓库文档，不写进 Skill 本体。
