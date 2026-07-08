# 路线图

## Now

- 维护薄 `AGENTS.md`、`docs/AGENT_INDEX.md`、Skill Catalog、路由规则和基础校验，降低上下文负担。

## Next

- 增加更多 Skill 的管理能力，例如列出、安装、更新、卸载。
- 根据真实项目使用反馈优化 `multi-agent-project-handoff`。
- 根据真实旧前端项目分析反馈优化 `legacy-frontend-flow-analysis`。
- 当项目文档继续增加时，评估 `docs/AGENT_INDEX.md` 分组和 AGENTS 长度阈值是否合理。
- 当 Skill 数量增加到 8 个左右时，评估关键词重叠检查和 catalog 分组。

## Later

- 增加跨平台 Bash 安装脚本。
- 增加版本号和发布标签策略。
- 增加 Skill 变更测试夹具。
- 为复杂前端分析增加可选静态扫描脚本。
- 如 Skill 数量超过 20 个，评估插件化分发或按领域拆分仓库。

## 暂不做

- 暂不做图形化安装器。
- 暂不做自动远程发布。
- 暂不将项目级 README 放入 Skill 本体。
