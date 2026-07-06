# 交接说明

## 当前上下文

- 项目路径：`outputs/codex-skills`
- 当前目标：根据真实旧前端项目会话反馈优化既有 Skills，保持通用可复用。
- 当前 Skills：`multi-agent-project-handoff`、`legacy-frontend-flow-analysis`
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
- `skills/legacy-frontend-flow-analysis/SKILL.md`

## 下一步建议

- 后续继续根据真实项目使用反馈迭代两个 Skill，避免为了文案润色而频繁改动。
- 如要新增旧前端静态扫描能力，可优先评估 `legacy-frontend-flow-analysis` 的可选脚本，而不是把脚本逻辑塞进 `SKILL.md`。
- 如要支持更多平台，可以补充 Bash 安装脚本。

## 已知问题

- 官方 `quick_validate.py` 在部分 Windows Python 环境下需要额外 `PyYAML` 和 UTF-8 环境变量；本项目提供的 `scripts/validate.py` 避免了这个依赖。
