# 代码规范

## 分层和职责

- `skills/` 只放可被 Codex 安装和使用的 Skill 本体。
- `scripts/` 放项目维护脚本。
- `docs/` 放项目状态、路线、决策和交接。
- 根目录 `README.md` 面向人和其他端安装使用。

## Skill 规范

- 每个 Skill 文件夹必须包含 `SKILL.md`。
- `SKILL.md` frontmatter 只包含 `name` 和 `description`。
- `description` 是隐式触发的主要依据，应说明做什么和什么时候用，并包含 `Use when`。
- Skill 名称必须与文件夹名一致。
- `agents/openai.yaml` 如存在，默认提示应包含 `$skill-name`。
- 新增或调整 Skill 时，同步维护 `docs/SKILL_CATALOG.md`；明显改变触发边界时同步维护 `docs/SKILL_ROUTING.md`。
- Skill 本体不要加入 README、安装指南、变更日志等项目级文档。

## 脚本规范

- 优先使用 Python 标准库，减少新端安装依赖。
- PowerShell 脚本作为 Windows 入口，可调用 Python 脚本。
- 文件读写显式使用 UTF-8。
- 默认行为必须保守，避免覆盖用户本地已有内容。

## 测试要求

- 修改 Skill 后运行 `scripts/validate.cmd`、`scripts/validate.ps1` 或 `scripts/validate.py`。
- 修改安装脚本后使用临时目录测试安装。
- 修改 `multi-agent-project-handoff` 的生成脚本后，验证创建和复跑跳过两种情况。

## 安全要求

- 不提交密钥、Cookie、Token 或个人账号信息。
- 不提交 `.codex` 本机配置副本。
- 不提交临时安装目录或测试输出。

## 提交规范

- 使用 Conventional Commits。
- 中文提交信息优先，例如 `feat: 项目化多 Agent 协作 Skill`。
