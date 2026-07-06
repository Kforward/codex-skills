# 项目状态

## 最近更新

- 日期：2026-07-06
- 当前阶段：搭建 Skill 精准发现和路由维护框架

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

## 进行中

- 暂无。

## 下一步

- 继续根据真实项目使用反馈迭代两个 Skill 的内容、catalog 和校验规则。
- 后续可考虑为 `legacy-frontend-flow-analysis` 增加可选脚本，自动生成调用关系/依赖审计草稿。

## 风险和阻塞

- 暂无。

## 最近验证

- `.\scripts\validate.cmd`：通过（2026-07-06，含 Skill Catalog 校验）。
- `.\scripts\install.cmd multi-agent-project-handoff -Force`、`.\scripts\install.cmd legacy-frontend-flow-analysis -Force`：通过（2026-07-06）。
- `.\scripts\install.cmd multi-agent-project-handoff -Target <temp>`：通过。
- 复跑 `install.cmd`：通过，默认跳过已有 Skill。
- `python scripts/install.py multi-agent-project-handoff --target <temp>`：通过。
