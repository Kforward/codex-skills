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

## Always Follow
- Check `git status` before editing.
- Briefly state the plan before modifying code or project docs.
- Do not delete files or revert user/agent changes unless explicitly requested.
- Do not commit secrets, tokens, cookies, local config, generated output, or design/prototype caches.
- Follow existing architecture, naming, and validation commands.

## Read Routing
- Resume or new session: read `docs/STATUS.md` and `docs/HANDOFF.md`.
- Need task-specific docs, standards, roadmap, or decisions: start with `docs/AGENT_INDEX.md` and choose one route file under `docs/routes/`.
- Read the selected route file, then only the concrete docs it names.
- Working under a subtree with its own `AGENTS.md`: read that nested file for local incremental rules.
- If the current executor is Codex and `.codex/CODEX_PREFERENCES.md` exists, read it when Codex-specific preferences matter.
- Do not read every file in `docs/` by default.

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
AI Agent 接手本项目时，先阅读 `AGENTS.md`，再阅读 `docs/HANDOFF.md`、`docs/STATUS.md` 和 `docs/AGENT_INDEX.md`。

## 文档地图
- `docs/PROJECT.md`
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/AGENT_INDEX.md`
- `docs/routes/*.md`
- `docs/ROADMAP.md`
- `docs/DECISIONS.md`
- `docs/CODE_STANDARDS.md`
- `docs/ai-agent/README.md`
- `docs/change-diffs/README.md`
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
- `docs/STATUS.md`
- `docs/HANDOFF.md`
- `docs/AGENT_INDEX.md`
- 按 `docs/AGENT_INDEX.md` 选择一个 `docs/routes/` 路由文件，再读取任务相关文档；不要默认全读。

## 下一步建议
- TBD

## 已知问题
- 暂无
""",
    "AGENT_INDEX.md": """# Agent Route Index

Use this first-level route only to choose the next route file. Do not treat it as a full document map.

## Route By Task Type

| Task Type | Next Route |
|---|---|
| Resume project, inspect status, roadmap, or decisions | `docs/routes/PROJECT_ROUTING.md` |
| Change code, scripts, validation, architecture, or security rules | `docs/routes/DEVELOPMENT_ROUTING.md` |
| Create, update, choose, install, or validate Skills | `docs/routes/SKILL_ROUTING.md` |
| Adjust AI-agent collaboration, handoff, review, or documentation routing | `docs/routes/AI_AGENT_ROUTING.md` |
| Compare versions, requirements, or feature differences | `docs/routes/CHANGE_ROUTING.md` |

## Keep Context Small
- Read exactly one route file first, then only the concrete docs it names.
- Prefer targeted reads over "read all docs".
- If a nested directory contains its own `AGENTS.md`, read it only when working in that subtree; nested files should contain incremental local rules, not copied root rules.
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
- 决策：使用仓库文档和 L0/L1/L2 分级路由作为多端、多 AI Agent 协作的共享记忆。
- 背景：不同客户端和 Agent 不能天然共享完整聊天上下文。
- 取舍：把长期上下文写入仓库，用薄 `AGENTS.md`、`docs/AGENT_INDEX.md` 和 `docs/routes/*.md` 避免依赖单次会话记忆或默认全量读取。
- 影响：后续阶段结束时需要同步更新状态、交接、路线图和决策文档；新增长期文档时应更新对应路由。
""",
    "CODE_STANDARDS.md": """# 代码规范

## 分层和职责
- TBD: 说明项目的模块边界和职责划分。
- 根目录 `AGENTS.md` 只放硬规则和 L0 入口。
- `docs/AGENT_INDEX.md` 只做 L1 任务类型路由。
- `docs/routes/*.md` 做 L2 任务子类型路由，指向具体单一职责文档。
- 任务细节、流程说明和分析模板放入单一职责文档或 Skill，不塞回根入口。

## 业务更新原则
- 修改前先判断是否影响已有逻辑。
- 影响旧逻辑时要做兼容与适配。
- 不影响旧逻辑时按模块化方式新增。
- 优先复用基础方法；基础方法不足时优先做兼容改造。
- 推荐按“基础方法层 -> 业务功能方法层 -> 页面编排层”封装变化。

## 复用原则
- 同一能力只保留一个权威实现。
- 出现第二处相似逻辑时优先提取复用。

## 注释与文档
- 新增或修改函数方法时补充规范注释。
- 注释应说明业务场景、参数、返回值、副作用和兼容策略。
- 可以不写额外长注释，但不代表业务函数/方法可以省略必要说明。

## 重构安全
- 重构旧逻辑前先做隐式依赖审计。
- 检查 `this.xxx`、全局状态、生命周期副作用、模块级变量、同名覆盖、回调残留和执行顺序。
- 技术债治理优先采用“禁止新增 -> 旧逻辑抽函数 -> 保留兼容壳 -> 新业务直接用函数”的渐进方式。

## 错误处理
- TBD: 说明错误类型、返回方式和日志策略。

## 测试要求
- TBD: 说明单测、集成测试、构建或手工验证要求。

## 安全要求
- 不提交密钥、Cookie、Token 或私有数据。
- 本地配置、运行产物、原型/设计工具缓存和临时分析输出应加入忽略规则。

## 提交规范
- 只有用户明确要求或项目协议要求阶段提交时才操作 git commit。
- commit 必须按功能点、修复点或文档点拆分。
- 一个 commit 只表达一个功能点；不要混入无关改动。
- commit message 遵循 Conventional Commits：`<type>(<scope>): <subject>`。
""",
    "ai-agent/README.md": """# AI Agent 详细流程

## 目录职责
- 本目录存放长期稳定、可复用的详细流程。
- 根目录 `AGENTS.md` 只保留高优先级入口；`docs/AGENT_INDEX.md` 和 `docs/routes/*.md` 负责路由。

## 推荐文档类型
- 复杂业务流程导航。
- 修改点定位表。
- 共享模块调用关系。
- 风险清单和验证清单。

## 编写原则
- 从代表样例提炼通用流程，不把通用文档命名成某个特例。
- 分析结果落文档时，同步更新 README 索引、检查清单、风险和验证点。
- 如果只是一次性需求或版本差异，放到 `docs/change-diffs/`。
""",
    "change-diffs/README.md": """# 变更异同分析

## 目录职责
- 本目录存放版本、需求或功能级异同分析。
- 长期稳定流程沉淀到 `docs/ai-agent/`。

## 建议命名
- `<version>-<feature>-diff.md`
- `<branch>-<feature>-diff.md`
- `<date>-<feature>-diff.md`

## 单篇模板
### 背景
TBD

### 复用逻辑
TBD

### 差异点
TBD

### 兼容影响
TBD

### 风险
TBD

### 验证清单
TBD
""",
}


ROUTE_FILES = {
    "PROJECT_ROUTING.md": """# Project Routing

Use this route for project understanding, resume, status, roadmap, and decisions.

| Task | Read |
|---|---|
| Resume work or start a new session | `docs/STATUS.md`, `docs/HANDOFF.md` |
| Understand project purpose and boundaries | `docs/PROJECT.md` |
| Check current priorities | `docs/ROADMAP.md` |
| Understand why a choice was made | `docs/DECISIONS.md` |
| Update project state after work | `docs/STATUS.md`, `docs/HANDOFF.md` |

Return to `docs/AGENT_INDEX.md` only if the task type changes.
""",
    "DEVELOPMENT_ROUTING.md": """# Development Routing

Use this route for code, scripts, validation, architecture, security, and implementation conventions.

| Task | Read |
|---|---|
| Change code | `docs/CODE_STANDARDS.md`, task-specific source files, and nearby docs |
| Change validation, build, install, or maintenance scripts | `README.md`, `docs/CODE_STANDARDS.md`, related files under `scripts/` |
| Change architecture or security-sensitive behavior | `docs/PROJECT.md`, `docs/DECISIONS.md`, `docs/CODE_STANDARDS.md` |
| Prepare commit or release notes | `docs/CODE_STANDARDS.md`, `docs/STATUS.md` |

If the project later adds `docs/development/COMMANDS.md`, `TESTING.md`, `ARCHITECTURE.md`, or `SECURITY.md`, route to those single-responsibility files from here.
""",
    "SKILL_ROUTING.md": """# Skill Routing

Use this route for selecting, creating, updating, installing, or validating Skills.

| Task | Read |
|---|---|
| Choose which Skill to use | `docs/SKILL_CATALOG.md` and `docs/SKILL_ROUTING.md` if present |
| Add or update a Skill | target `skills/<name>/SKILL.md`, relevant bundled resources, and Skill catalog/routing docs if present |
| Update handoff workflow Skill | `skills/multi-agent-project-handoff/SKILL.md`, `skills/multi-agent-project-handoff/references/document-set.md`, `skills/multi-agent-project-handoff/scripts/init_handoff_docs.py` |
| Install or validate Skills | `README.md`, `scripts/install.py`, `scripts/validate.py` |

Run the repository validation command after Skill changes.
""",
    "AI_AGENT_ROUTING.md": """# AI Agent Routing

Use this route for AI-agent collaboration rules, handoff structure, document routing, and review workflow.

| Task | Read |
|---|---|
| Adjust root agent instructions | `AGENTS.md`, `docs/AGENT_INDEX.md`, this route |
| Change document routing | `docs/AGENT_INDEX.md`, `docs/routes/*.md`, `docs/CODE_STANDARDS.md` |
| Slim bulky agent docs | `AGENTS.md`, `docs/AGENT_INDEX.md`, `docs/ai-agent/README.md` |
| Initialize another repo for multi-agent work | Use `$multi-agent-project-handoff` |
| Record a collaboration decision | `docs/DECISIONS.md` |

Keep root `AGENTS.md` thin. Add detail to route files, `docs/ai-agent/`, or Skills.
""",
    "CHANGE_ROUTING.md": """# Change Routing

Use this route for version, requirement, and feature-difference documentation.

| Task | Read |
|---|---|
| Compare a new version or requirement with existing behavior | `docs/change-diffs/README.md` |
| Record a feature-level difference | `docs/change-diffs/README.md`, relevant project docs |
| Update project roadmap after a change | `docs/ROADMAP.md` |
| Record a product or architecture decision | `docs/DECISIONS.md` |
| Analyze a complex frontend variant | Use `$legacy-frontend-flow-analysis` if available |

Keep stable workflows in `docs/ai-agent/` or Skills. Keep one-off version differences in `docs/change-diffs/`.
""",
}


OPTIONAL_FILES = {
    ".codex/CODEX_PREFERENCES.md": """# Codex 项目级偏好

- 默认使用中文回复。
- 修改代码前先简短说明计划。
- 文档类改动默认不提交，除非用户明确要求或项目协议要求。
- 遇到冲突时，优先级为：用户当前明确指令 > `AGENTS.md` > 本文件。
""",
    "CLAUDE.md": """# Claude Entry

Please read `AGENTS.md` before analyzing or modifying this repository. Treat `AGENTS.md` as the source of truth for project rules, handoff workflow, and documentation expectations.
""",
    "GEMINI.md": """# Gemini Entry

Please read `AGENTS.md` before analyzing or modifying this repository. Treat `AGENTS.md` as the source of truth for project rules, handoff workflow, and documentation expectations.
""",
    ".cursorrules": """Read AGENTS.md before analyzing or modifying this repository. Treat AGENTS.md as the source of truth for project rules, handoff workflow, and documentation expectations.
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
    parser.add_argument(
        "--with-codex-preferences",
        action="store_true",
        help="Create .codex/CODEX_PREFERENCES.md if missing.",
    )
    parser.add_argument(
        "--with-compat-entrypoints",
        action="store_true",
        help="Create thin CLAUDE.md, GEMINI.md, and .cursorrules entrypoints.",
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

    routes_dir = docs_dir / "routes"
    for relative_path, template in ROUTE_FILES.items():
        target = routes_dir / relative_path
        status = write_file(target, render(template, project_name), args.force)
        results.append((status, str(target)))

    selected_optional_files: list[str] = []
    if args.with_codex_preferences:
        selected_optional_files.append(".codex/CODEX_PREFERENCES.md")
    if args.with_compat_entrypoints:
        selected_optional_files.extend(["CLAUDE.md", "GEMINI.md", ".cursorrules"])

    for relative_path in selected_optional_files:
        target = repo / relative_path
        status = write_file(
            target, render(OPTIONAL_FILES[relative_path], project_name), args.force
        )
        results.append((status, str(target)))

    for status, path in results:
        print(f"[{status}] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
