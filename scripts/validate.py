#!/usr/bin/env python3
"""Validate the distributable Codex skills project without third-party packages."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)


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
