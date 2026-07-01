#!/usr/bin/env python3
"""Install skills from this repository into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def resolve_selected(source_root: Path, names: list[str], install_all: bool) -> list[str]:
    if install_all or not names:
        return sorted(path.name for path in source_root.iterdir() if path.is_dir())
    return names


def assert_inside(child: Path, parent: Path) -> None:
    child_resolved = child.resolve()
    parent_resolved = parent.resolve()
    if parent_resolved not in child_resolved.parents and child_resolved != parent_resolved:
        raise RuntimeError(f"Refusing to remove path outside target root: {child_resolved}")


def main() -> int:
    configure_stdout()

    parser = argparse.ArgumentParser(
        description="Install Codex skills from this repository."
    )
    parser.add_argument("skills", nargs="*", help="Skill names to install.")
    parser.add_argument("--all", action="store_true", help="Install all skills.")
    parser.add_argument("--target", help="Target skills directory.")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing installed skills."
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    source_root = project_root / "skills"
    if not source_root.is_dir():
        parser.error(f"Cannot find skills directory: {source_root}")

    target_root = Path(args.target).expanduser() if args.target else default_target()
    target_root.mkdir(parents=True, exist_ok=True)

    selected = resolve_selected(source_root, args.skills, args.all)
    if not selected:
        parser.error("No skills found to install.")

    for skill_name in selected:
        source = source_root / skill_name
        if not source.is_dir():
            parser.error(f"Skill not found: {skill_name}")

        destination = target_root / skill_name
        if destination.exists():
            if not args.force:
                print(f"[skipped] {skill_name} already exists at {destination}")
                continue
            assert_inside(destination, target_root)
            shutil.rmtree(destination)

        shutil.copytree(source, destination)
        print(f"[installed] {skill_name} -> {destination}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
