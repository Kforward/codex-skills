# 交接说明

## 当前上下文

- 项目路径：`outputs/codex-skills`
- 当前目标：把个人 Skill 项目化，方便其他端安装和继续迭代。
- 当前 Skill：`multi-agent-project-handoff`
- 当前分支：`main`
- 当前远程：`git@github.com:Kforward/codex-skills.git`

## 恢复工作流程

```powershell
git pull --ff-only
.\scripts\validate.cmd
```

如果尚未初始化 Git，则先在项目根目录检查文件结构：

```powershell
Get-ChildItem -Recurse
.\scripts\validate.cmd
```

## 接手必读

- `README.md`
- `AGENTS.md`
- `docs/PROJECT.md`
- `docs/STATUS.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/CODE_STANDARDS.md`
- `skills/multi-agent-project-handoff/SKILL.md`

## 下一步建议

- 根据真实项目使用反馈继续迭代 `multi-agent-project-handoff`。
- 可单独创建复杂前端流程分析类 Skill，避免把业务代码分析方法塞进 handoff Skill。
- 如要支持更多平台，可以补充 Bash 安装脚本。

## 已知问题

- 官方 `quick_validate.py` 在部分 Windows Python 环境下需要额外 `PyYAML` 和 UTF-8 环境变量；本项目提供的 `scripts/validate.py` 避免了这个依赖。
