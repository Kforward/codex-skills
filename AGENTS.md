# AI Agent 协作协议

## 接手顺序
- 先读 `README.md`。
- 再读本文件。
- 再读 `docs/PROJECT.md`、`docs/STATUS.md`、`docs/HANDOFF.md`、`docs/ROADMAP.md`、`docs/DECISIONS.md`、`docs/CODE_STANDARDS.md`。
- 查看 `git status` 和最近提交。
- 修改 Skill 前先简短说明计划。

## 项目原则
- Skill 本体必须保持精简，只放 AI 执行任务时真正需要的内容。
- 安装、维护、分发说明放在项目根目录，不放进 Skill 文件夹。
- 新增或修改 Skill 后必须运行 `scripts/validate.ps1` 或 `scripts/validate.py`。
- 不提交密钥、Token、Cookie、个人本地配置或运行产物。
- 不删除已有 Skill 或文档，除非用户明确要求。

## 阶段结束清单
- 更新 `docs/STATUS.md`。
- 更新 `docs/HANDOFF.md`。
- 如有新决策，更新 `docs/DECISIONS.md`。
- 如路线变化，更新 `docs/ROADMAP.md`。
- 运行校验并记录结果。
