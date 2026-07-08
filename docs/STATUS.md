# 项目状态

## 最近更新

- 日期：2026-07-08
- 当前阶段：L0/L1/L2 分级文档路由框架已落地

## 已完成

- 将本机 `multi-agent-project-handoff` Skill 迁移到 `skills/` 目录。
- 新增项目级 `README.md`、`AGENTS.md` 和 `docs/` 协作文档。
- 新增安装脚本和校验脚本。
- 完成本地 Git 初始化和初始提交。
- 增强 `multi-agent-project-handoff`，补充短入口 `AGENTS.md`、文档分层、变更异同分析、Codex 专属偏好、跨工具薄入口、功能点提交规范和重构安全规则。
- 新增 `legacy-frontend-flow-analysis`，用于分析复杂旧前端业务流程、隐式依赖、变体差异、风险和验证清单。
- 优化 `multi-agent-project-handoff`，补充本地分析产物、设计/原型缓存和临时截图不进入提交的协作规则。
- 优化 `legacy-frontend-flow-analysis`，补充公共 helper 影响面、空数据/异常兜底、非阻塞边界和第三方 SDK 适配层检查。
- 新增 `docs/SKILL_CATALOG.md`，集中记录每个 Skill 的适用场景、不适用场景、触发关键词和示例 prompt。
- 新增 `docs/SKILL_ROUTING.md`，记录 Skill 增长后的触发优先级、description 写法和 catalog 维护规则。
- 增强 `scripts/validate.py`，校验 description 路由质量和 catalog 覆盖情况。
- 将根 `AGENTS.md` 收敛为薄入口，只保留硬规则、读取路由和阶段结束清单。
- 新增 `docs/AGENT_INDEX.md`，按任务路由项目文档，避免默认读取全部 `docs/`。
- 更新 `multi-agent-project-handoff` 生成模板，新项目默认使用薄 `AGENTS.md` + `docs/AGENT_INDEX.md`。
- 增强 `scripts/validate.py`，校验根 `AGENTS.md` 长度、`docs/AGENT_INDEX.md` 存在和上下文瘦身规则。
- 将 `docs/AGENT_INDEX.md` 调整为 L1 任务类型路由，只负责指向下一层 route file。
- 新增 `docs/routes/PROJECT_ROUTING.md`、`DEVELOPMENT_ROUTING.md`、`SKILL_ROUTING.md`、`AI_AGENT_ROUTING.md`、`CHANGE_ROUTING.md`。
- 更新 `multi-agent-project-handoff` Skill、reference 模板和初始化脚本，新项目默认生成 L0/L1/L2 文档路由。
- 增强 `scripts/validate.py`，校验 route files 存在、被 L1 索引引用，并纳入初始化 smoke test。

## 进行中

- 暂无。

## 下一步

- 继续根据真实项目使用反馈迭代两个 Skill 的内容、catalog、分级文档路由和校验规则。
- 观察真实项目里的 `docs/routes/*.md` 是否需要按领域继续拆分；没有真实膨胀前不新增更深层目录。
- 后续可考虑为 `legacy-frontend-flow-analysis` 增加可选脚本，自动生成调用关系/依赖审计草稿。

## 风险和阻塞

- 暂无。

## 最近验证

- `.\scripts\validate.cmd`：通过（2026-07-08，含 Skill Catalog、AGENTS 瘦身和 L0/L1/L2 route files 校验）。
- `.\scripts\install.cmd multi-agent-project-handoff -Force`：通过（2026-07-08，已安装到本机 Codex skills 目录）。
- `python -m py_compile skills\multi-agent-project-handoff\scripts\init_handoff_docs.py scripts\validate.py`：通过（2026-07-08）。
- `git diff --check`：通过（2026-07-08）。
- `.\scripts\install.cmd multi-agent-project-handoff -Force`、`.\scripts\install.cmd legacy-frontend-flow-analysis -Force`：通过（2026-07-06）。
- `.\scripts\install.cmd multi-agent-project-handoff -Target <temp>`：通过。
- 复跑 `install.cmd`：通过，默认跳过已有 Skill。
- `python scripts/install.py multi-agent-project-handoff --target <temp>`：通过。
