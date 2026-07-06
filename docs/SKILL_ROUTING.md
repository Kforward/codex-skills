# Skill Routing Rules

## 目标

让 Skill 数量增加后仍能被准确发现和选择。这里维护的是路由规则，不是某个 Skill 的执行说明。

## 触发优先级

1. 显式 `$skill-name`：用户或自动化已经知道目标 Skill 时优先使用。
2. `SKILL.md` frontmatter `description`：Codex 的主要隐式匹配依据。
3. `docs/SKILL_CATALOG.md`：给人和维护 Agent 查边界、示例和关键词。
4. `agents/openai.yaml`：桌面 UI 展示和默认 prompt 辅助。

## 新增 Skill 检查

- 名称使用小写字母、数字和短横线，尽量是动作或工作流名。
- `description` 必须说明“做什么”和“什么时候用”，并包含 `Use when`。
- 不创建万能 Skill；一个 Skill 只负责一个稳定工作流。
- 与已有 Skill 有重叠时，先改边界或合并，不急着新增。
- 同步更新 `docs/SKILL_CATALOG.md`。
- 如 Skill 面向 UI 展示，同步检查 `agents/openai.yaml`。
- 运行 `.\scripts\validate.cmd`。

## Description 写法

推荐结构：

```text
<Action and scope>. Use when <concrete triggers, task types, and contexts>.
```

好的 description 应该包含：

- 任务对象：例如 repository handoff、legacy frontend flow、PDF、spreadsheet。
- 入口词：例如 route、component、SDK、handoff、AGENTS.md。
- 使用时机：例如 creating、updating、analyzing、auditing、resuming。
- 边界词：避免和其他 Skill 混成同一个“helper”。

## Catalog 维护规则

每个 Skill 条目至少包含：

- 适用场景
- 不适用场景
- 触发关键词
- 示例 prompt，且包含 `$skill-name`
- 主要资源
- 边界提示

## 增长策略

- 1-7 个 Skill：维护清晰 description 和 catalog 即可。
- 8-20 个 Skill：开始检查关键词重叠，并按领域整理 catalog。
- 20 个以上：考虑拆分仓库、插件化分发，或建立更强的索引/安装分组。

## 不做的事

- 不为了路由而把所有 Skill 合并成一个总控 Skill。
- 不在 Skill 本体里放项目级 catalog。
- 不把 catalog 当成 Codex 运行时唯一事实来源；真正触发仍依赖 `name` 和 `description`。
