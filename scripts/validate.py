#!/usr/bin/env python3
"""Validate the distributable Codex skills project without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
CATALOG_HEADING_RE = re.compile(r"^##\s+`?(?P<name>[a-z0-9-]{1,64})`?\s*$", re.MULTILINE)
ROUTE_FILES = [
    "PROJECT_ROUTING.md",
    "DEVELOPMENT_ROUTING.md",
    "SKILL_ROUTING.md",
    "AI_AGENT_ROUTING.md",
    "CHANGE_ROUTING.md",
]


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def parse_simple_frontmatter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError("missing YAML frontmatter")

    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        value = value.strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {'"', "'"}
        ):
            value = value[1:-1]
        data[key.strip()] = value
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]

    try:
        frontmatter = parse_simple_frontmatter(skill_md)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    if not name:
        errors.append(f"{skill_dir.name}: missing name")
    if not description:
        errors.append(f"{skill_dir.name}: missing description")
    if description:
        if len(description) < 80:
            errors.append(f"{skill_dir.name}: description is too short for routing")
        if len(description) > 1000:
            errors.append(f"{skill_dir.name}: description is too long for routing")
        if "Use when" not in description:
            errors.append(f"{skill_dir.name}: description should include 'Use when'")
    if name and name != skill_dir.name:
        errors.append(f"{skill_dir.name}: name does not match folder ({name})")
    if name and not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append(f"{skill_dir.name}: invalid skill name")
    if "TODO" in description or "[TODO" in description:
        errors.append(f"{skill_dir.name}: description still contains TODO")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists() and name:
        text = openai_yaml.read_text(encoding="utf-8")
        if f"${name}" not in text:
            errors.append(f"{skill_dir.name}: agents/openai.yaml missing ${name}")

    return errors


def collect_skill_metadata(skill_dirs: list[Path]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        try:
            frontmatter = parse_simple_frontmatter(skill_md)
        except ValueError:
            continue
        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()
        if name:
            metadata[name] = description
    return metadata


def extract_catalog_sections(catalog_text: str) -> dict[str, str]:
    matches = list(CATALOG_HEADING_RE.finditer(catalog_text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(catalog_text)
        sections[match.group("name")] = catalog_text[start:end]
    return sections


def validate_skill_catalog(project_root: Path, skills: dict[str, str]) -> list[str]:
    errors: list[str] = []
    catalog = project_root / "docs" / "SKILL_CATALOG.md"
    routing = project_root / "docs" / "SKILL_ROUTING.md"

    if not catalog.is_file():
        return ["docs/SKILL_CATALOG.md: missing skill catalog"]
    if not routing.is_file():
        errors.append("docs/SKILL_ROUTING.md: missing skill routing rules")

    catalog_text = catalog.read_text(encoding="utf-8")
    sections = extract_catalog_sections(catalog_text)
    required_labels = ["适用场景", "不适用场景", "触发关键词", "示例 prompt"]

    for name in sorted(skills):
        section = sections.get(name)
        if not section:
            errors.append(f"docs/SKILL_CATALOG.md: missing section for {name}")
            continue
        for label in required_labels:
            if label not in section:
                errors.append(f"docs/SKILL_CATALOG.md: {name} missing {label}")
        if f"${name}" not in section:
            errors.append(f"docs/SKILL_CATALOG.md: {name} example prompt missing ${name}")

    extra_sections = sorted(set(sections) - set(skills))
    for name in extra_sections:
        errors.append(f"docs/SKILL_CATALOG.md: unknown skill section {name}")

    return errors


def validate_agent_docs(project_root: Path) -> list[str]:
    errors: list[str] = []
    agents = project_root / "AGENTS.md"
    index = project_root / "docs" / "AGENT_INDEX.md"
    routes_dir = project_root / "docs" / "routes"

    if not agents.is_file():
        errors.append("AGENTS.md: missing root agent instructions")
    else:
        text = agents.read_text(encoding="utf-8")
        non_empty_lines = [line for line in text.splitlines() if line.strip()]
        if len(non_empty_lines) > 80:
            errors.append("AGENTS.md: root instructions should stay under 80 non-empty lines")
        if "docs/AGENT_INDEX.md" not in text:
            errors.append("AGENTS.md: missing docs/AGENT_INDEX.md routing")
        if "Do not read every file in `docs/` by default" not in text:
            errors.append("AGENTS.md: missing targeted-read guardrail")

    if not index.is_file():
        errors.append("docs/AGENT_INDEX.md: missing task routing index")
    else:
        text = index.read_text(encoding="utf-8")
        for required in ["Route By Task Type", "Keep Context Small", "AGENTS.md"]:
            if required not in text:
                errors.append(f"docs/AGENT_INDEX.md: missing {required}")
        for route_file in ROUTE_FILES:
            route_path = f"docs/routes/{route_file}"
            if route_path not in text:
                errors.append(f"docs/AGENT_INDEX.md: missing route {route_path}")

    if not routes_dir.is_dir():
        errors.append("docs/routes: missing route directory")
    else:
        for route_file in ROUTE_FILES:
            route_path = routes_dir / route_file
            if not route_path.is_file():
                errors.append(f"docs/routes/{route_file}: missing route file")
                continue
            text = route_path.read_text(encoding="utf-8")
            if "| Task | Read |" not in text:
                errors.append(f"docs/routes/{route_file}: missing task routing table")

    return errors


def run_handoff_smoke(project_root: Path) -> list[str]:
    errors: list[str] = []
    script = (
        project_root
        / "skills"
        / "multi-agent-project-handoff"
        / "scripts"
        / "init_handoff_docs.py"
    )
    if not script.is_file():
        return ["multi-agent-project-handoff: missing init_handoff_docs.py"]

    with tempfile.TemporaryDirectory(prefix="codex-skill-test-") as tmp:
        tmp_path = Path(tmp)
        first = subprocess.run(
            [
                sys.executable,
                str(script),
                str(tmp_path),
                "--project-name",
                "Smoke Test",
                "--with-codex-preferences",
                "--with-compat-entrypoints",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        if first.returncode != 0:
            errors.append(f"handoff smoke create failed: {first.stderr.strip()}")
            return errors

        expected = [
            "AGENTS.md",
            "README.md",
            "docs/PROJECT.md",
            "docs/STATUS.md",
            "docs/HANDOFF.md",
            "docs/AGENT_INDEX.md",
            "docs/routes/PROJECT_ROUTING.md",
            "docs/routes/DEVELOPMENT_ROUTING.md",
            "docs/routes/SKILL_ROUTING.md",
            "docs/routes/AI_AGENT_ROUTING.md",
            "docs/routes/CHANGE_ROUTING.md",
            "docs/ROADMAP.md",
            "docs/DECISIONS.md",
            "docs/CODE_STANDARDS.md",
            "docs/ai-agent/README.md",
            "docs/change-diffs/README.md",
            ".codex/CODEX_PREFERENCES.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".cursorrules",
        ]
        for relative in expected:
            if not (tmp_path / relative).is_file():
                errors.append(f"handoff smoke missing generated file: {relative}")

        second = subprocess.run(
            [
                sys.executable,
                str(script),
                str(tmp_path),
                "--project-name",
                "Smoke Test",
                "--with-codex-preferences",
                "--with-compat-entrypoints",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        if second.returncode != 0:
            errors.append(f"handoff smoke skip failed: {second.stderr.strip()}")
        if "[skipped]" not in second.stdout:
            errors.append("handoff smoke did not skip existing files on second run")

    return errors


def main() -> int:
    configure_stdout()

    project_root = Path(__file__).resolve().parents[1]
    skills_root = project_root / "skills"
    if not skills_root.is_dir():
        print(f"[error] Missing skills directory: {skills_root}")
        return 1

    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_dirs:
        print("[error] No skills found.")
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    skill_metadata = collect_skill_metadata(skill_dirs)
    errors.extend(validate_skill_catalog(project_root, skill_metadata))
    errors.extend(validate_agent_docs(project_root))
    errors.extend(run_handoff_smoke(project_root))

    if errors:
        for error in errors:
            print(f"[error] {error}")
        return 1

    for skill_dir in skill_dirs:
        print(f"[ok] {skill_dir.name}")
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
