# 交接说明

## 当前上下文

- 项目路径：`outputs/codex-skills`
- 当前目标：维护可扩展的 Skill 项目；薄 `AGENTS.md` + `docs/AGENT_INDEX.md` + `docs/routes/*.md` 分级路由框架已落地。
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
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/AGENT_INDEX.md`
- 按 `docs/AGENT_INDEX.md` 选择一个 `docs/routes/` 路由文件，再读取任务相关文档；不要默认全读。

## 下一步建议

- 后续继续根据真实项目使用反馈迭代两个 Skill，避免为了文案润色而频繁改动。
- 新增项目文档时优先更新对应 `docs/routes/*.md`；只有新增任务大类时才更新 `docs/AGENT_INDEX.md`。
- 后续真实项目使用中，如果某个 route file 变长，优先拆分其指向的详细文档；确认任务子类型足够稳定后再考虑新增更深层 route。
- 新增或调整 Skill 时先更新 `docs/SKILL_CATALOG.md`，并确认 `description` 仍能精准触发。
- 如要新增旧前端静态扫描能力，可优先评估 `legacy-frontend-flow-analysis` 的可选脚本，而不是把脚本逻辑塞进 `SKILL.md`。
- 如要支持更多平台，可以补充 Bash 安装脚本。

## 已知问题

- 官方 `quick_validate.py` 在部分 Windows Python 环境下需要额外 `PyYAML` 和 UTF-8 环境变量；本项目提供的 `scripts/validate.py` 避免了这个依赖。
