#!/usr/bin/env python3
"""Create missing multi-agent handoff docs for a repository.

The script is intentionally conservative: it creates missing files and skips
existing files unless --force is passed.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


ROOT_FILES = {
    "AGENTS.md": """# AI Agent 协作协议

## 接手顺序
- 先读 `README.md`。
- 再读 `AGENTS.md`。
- 再读 `docs/PROJECT.md`、`docs/STATUS.md`、`docs/HANDOFF.md`、`docs/ROADMAP.md`、`docs/DECISIONS.md`、`docs/CODE_STANDARDS.md`。
- 查看 `git status` 和最近提交。
- 修改代码前先简短说明计划。

## 工作规则
- 优先遵循仓库已有架构、命名和测试方式。
- 不要删除文件或回滚用户/其他 Agent 的改动，除非用户明确要求。
- 代码变更要同步更新状态、交接或决策文档。
- 阶段结束前运行项目约定的验证命令。

## 恢复工作流程
- 拉取最新代码后重新阅读状态、交接、路线图和决策文档。
- 先总结当前状态和下一步，再继续开发。

## 阶段结束清单
- 更新 `docs/STATUS.md`。
- 更新 `docs/HANDOFF.md`。
- 如有新决策，更新 `docs/DECISIONS.md`。
- 如路线变化，更新 `docs/ROADMAP.md`。
- 运行验证并记录结果。
""",
    "README.md": """# {{PROJECT_NAME}}

## 项目简介
TBD: 说明项目目标、使用者和核心能力。

## 快速开始
TBD: 补充安装、配置、运行、测试和构建命令。

## 常用命令
TBD: 列出本项目最常用的开发命令。

## 协作入口
AI Agent 接手本项目时，先阅读 `AGENTS.md`，再阅读 `docs/HANDOFF.md` 和 `docs/STATUS.md`。

## 文档地图
- `docs/PROJECT.md`
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/CODE_STANDARDS.md`
""",
}


DOC_FILES = {
    "PROJECT.md": """# 项目说明

## 目标
TBD: 说明项目要解决的问题。

## 范围
TBD: 说明当前版本包含的能力。

## 非目标
TBD: 说明明确暂不处理的事项。

## 用户/使用场景
TBD: 说明主要用户和关键流程。

## 关键约束
TBD: 说明平台、安全、接口、数据或性能约束。

## 重要假设
TBD: 记录后续 Agent 需要知道或验证的假设。
""",
    "STATUS.md": """# 项目状态

## 最近更新
- 日期：{{DATE}}
- 当前阶段：TBD

## 已完成
- TBD

## 进行中
- TBD

## 下一步
- TBD

## 风险和阻塞
- 暂无

## 最近验证
- TBD
""",
    "HANDOFF.md": """# 交接说明

## 当前上下文
- 分支：TBD
- 最近提交：TBD
- 当前目标：TBD

## 恢复工作流程
```bash
git pull --ff-only
```

TBD: 补充安装、测试、构建命令。

## 接手必读
- `README.md`
- `AGENTS.md`
- `docs/PROJECT.md`
- `docs/STATUS.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/CODE_STANDARDS.md`

## 下一步建议
- TBD

## 已知问题
- 暂无
""",
    "ROADMAP.md": """# 路线图

## Now
- TBD

## Next
- TBD

## Later
- TBD

## 暂不做
- TBD
""",
    "DECISIONS.md": """# 决策记录

## 记录格式
- 日期：
- 决策：
- 背景：
- 取舍：
- 影响：

## 决策

### {{DATE}} - 初始化协作交接文档
- 决策：使用仓库文档作为多端、多 AI Agent 协作的共享记忆。
- 背景：不同客户端和 Agent 不能天然共享完整聊天上下文。
- 取舍：把长期上下文写入仓库，避免依赖单次会话记忆。
- 影响：后续阶段结束时需要同步更新状态、交接、路线图和决策文档。
""",
    "CODE_STANDARDS.md": """# 代码规范

## 分层和职责
- TBD: 说明项目的模块边界和职责划分。

## 复用原则
- 同一能力只保留一个权威实现。
- 出现第二处相似逻辑时优先提取复用。

## 错误处理
- TBD: 说明错误类型、返回方式和日志策略。

## 测试要求
- TBD: 说明单测、集成测试、构建或手工验证要求。

## 安全要求
- 不提交密钥、Cookie、Token 或私有数据。
- 本地配置和运行产物应加入忽略规则。

## 提交规范
- TBD: 说明 commit 语言、格式和分支策略。
""",
}


def render(template: str, project_name: str) -> str:
    return (
        template.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{DATE}}", date.today().isoformat())
        .rstrip()
        + "\n"
    )


def write_file(path: Path, content: str, force: bool) -> str:
    existed = path.exists()
    if existed and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "written" if existed else "created"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create missing multi-agent project handoff docs."
    )
    parser.add_argument("repo", nargs="?", default=".", help="Repository path.")
    parser.add_argument("--project-name", help="Project name for generated README.")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing handoff docs."
    )
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        parser.error(f"Repository path does not exist: {repo}")
    if not repo.is_dir():
        parser.error(f"Repository path is not a directory: {repo}")

    project_name = args.project_name or repo.name
    results: list[tuple[str, str]] = []

    for relative_path, template in ROOT_FILES.items():
        target = repo / relative_path
        status = write_file(target, render(template, project_name), args.force)
        results.append((status, str(target)))

    docs_dir = repo / "docs"
    for relative_path, template in DOC_FILES.items():
        target = docs_dir / relative_path
        status = write_file(target, render(template, project_name), args.force)
        results.append((status, str(target)))

    for status, path in results:
        print(f"[{status}] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
