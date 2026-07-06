# 项目说明

## 目标

集中维护可复用的 Codex Skills，让不同客户端、不同设备和不同 AI Agent 可以安装并使用同一套工作流。

## 当前范围

- 维护 `multi-agent-project-handoff` Skill。
- 维护 `legacy-frontend-flow-analysis` Skill。
- 提供本地安装脚本。
- 提供无外部依赖的基础校验脚本。
- 提供 Skill catalog 和路由维护规则，避免 Skill 增长后难以选择。
- 用项目文档记录 Skill 项目的状态、路线、决策和交接。

## 非目标

- 暂不发布到 npm、PyPI 或插件市场。
- 暂不自动修改用户全局 Codex 配置。
- 暂不自动创建远程 GitHub 仓库。

## 使用场景

- 新端拉取本仓库后安装 Skills。
- 迭代已有 Skill 并同步给其他端。
- 在新项目中使用 `multi-agent-project-handoff` 初始化多 Agent 协作文档。
- 在复杂旧前端项目中使用 `legacy-frontend-flow-analysis` 追踪业务流程和风险。

## 关键约束

- Skill 文件夹内不放 README、安装说明或变更日志。
- 安装脚本默认不覆盖用户本机已有 Skill。
- 校验脚本尽量只依赖 Python 标准库，方便新端直接运行。
