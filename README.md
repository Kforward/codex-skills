# Codex Skills

这个仓库用于集中维护可复用的 Codex Skills，方便多端、多用户、多 AI Agent 共享同一套工作流。

## 当前 Skills

- `multi-agent-project-handoff`：为新项目或现有仓库建立多端、多 AI Agent 协作交接文档和恢复流程。

## 安装

安装全部 Skills：

```powershell
.\scripts\install.cmd
```

安装指定 Skill：

```powershell
.\scripts\install.cmd multi-agent-project-handoff
```

默认安装位置：

```text
$CODEX_HOME\skills
```

如果没有设置 `CODEX_HOME`，则使用：

```text
~\.codex\skills
```

默认不会覆盖本机已有 Skill。需要覆盖时：

```powershell
.\scripts\install.cmd multi-agent-project-handoff -Force
```

## 校验

```powershell
.\scripts\validate.cmd
```

校验会检查：

- 每个 Skill 是否存在 `SKILL.md`
- frontmatter 是否包含 `name` 和 `description`
- Skill 目录名是否与 `name` 一致
- `agents/openai.yaml` 的默认提示是否包含 `$skill-name`
- `multi-agent-project-handoff` 的初始化脚本是否能创建并跳过已有文档

## 新端使用流程

```powershell
git clone <this-repo-url>
cd codex-skills
.\scripts\install.cmd
.\scripts\validate.cmd
```

然后在 Codex 中即可使用：

```text
Use $multi-agent-project-handoff to initialize this repository for multi-agent collaboration.
```

## 维护规则

- Skill 本体只保留 AI 执行任务所需的信息。
- 项目级说明、安装说明、维护流程放在本仓库根目录。
- 修改 Skill 后运行 `.\scripts\validate.ps1`。
- 将新版本通过 Git 提交和同步到其他端。
