#!/usr/bin/env python3
"""Validate the structural contracts of the guto-skills pack."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

REQUIRED_SKILLS = {
    "guto-plan",
    "guto-build",
    "guto-verify",
    "guto-review",
    "clarification-plan",
}

COUNCIL_ONLY_TOKENS = {
    "edge_id",
    "CRITICAL_BLOCK",
    "HIGH_FIX_NOW",
    "PHASE-PLAN",
    "LOCAL-COMMIT",
    ".harness/",
    "council_session.py",
    "agent_swarm_ledger",
}

JSON_MANIFESTS = (
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            self.fail(message)


def parse_frontmatter(path: Path, validation: Validation) -> tuple[str, str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        validation.fail(f"{path.relative_to(ROOT)}: missing opening YAML frontmatter marker")
        return None

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        validation.fail(f"{path.relative_to(ROOT)}: missing closing YAML frontmatter marker")
        return None

    frontmatter = "\n".join(lines[1:end])
    name_match = re.search(r"(?m)^name:\s*([^\s#]+)\s*$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)

    if not name_match:
        validation.fail(f"{path.relative_to(ROOT)}: frontmatter has no simple name field")
        return None
    if not description_match:
        validation.fail(f"{path.relative_to(ROOT)}: frontmatter has no single-line description")
        return None

    return name_match.group(1), description_match.group(1)


def validate_skills(validation: Validation) -> None:
    validation.check(SKILLS_DIR.is_dir(), "skills/ directory is missing")
    if not SKILLS_DIR.is_dir():
        return

    skill_dirs = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}
    missing = REQUIRED_SKILLS - skill_dirs
    validation.check(not missing, f"missing required skills: {sorted(missing)}")

    for directory in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        relative_dir = directory.relative_to(ROOT)
        skill_file = directory / "SKILL.md"
        validation.check(skill_file.is_file(), f"{relative_dir}: missing SKILL.md")
        if not skill_file.is_file():
            continue

        parsed = parse_frontmatter(skill_file, validation)
        if parsed is None:
            continue
        name, description = parsed

        validation.check(
            name == directory.name,
            f"{skill_file.relative_to(ROOT)}: frontmatter name {name!r} != directory {directory.name!r}",
        )
        validation.check(
            "adaptive" not in name and not name.endswith("-loop"),
            f"{skill_file.relative_to(ROOT)}: legacy adaptive/loop naming is forbidden",
        )
        validation.check(
            len(description) <= 1024,
            f"{skill_file.relative_to(ROOT)}: description exceeds 1024 characters",
        )
        validation.check(
            re.search(r"\bUse (quando|depois|para)\b", description) is not None,
            f"{skill_file.relative_to(ROOT)}: description must state when to use the skill",
        )

        text = skill_file.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        validation.check(
            line_count <= 500,
            f"{skill_file.relative_to(ROOT)}: {line_count} lines; keep SKILL.md at or below 500",
        )

        if name.startswith("guto-") or name == "clarification-plan":
            for token in sorted(COUNCIL_ONLY_TOKENS):
                if token in text:
                    validation.fail(
                        f"{skill_file.relative_to(ROOT)}: Council-only token {token!r} must not leak into clean skills"
                    )

        validation.check(
            "../../references/" not in text,
            f"{skill_file.relative_to(ROOT)}: skills must be self-contained; root references are not installed by every CLI",
        )


def validate_manifests(validation: Validation) -> None:
    versions: dict[str, str] = {}
    for manifest in JSON_MANIFESTS:
        relative = manifest.relative_to(ROOT)
        validation.check(manifest.is_file(), f"{relative}: missing manifest")
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            validation.fail(f"{relative}: invalid JSON: {exc}")
            continue

        if "version" in data:
            versions[str(relative)] = str(data["version"])
        plugins = data.get("plugins")
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            plugin_version = plugins[0].get("version")
            if plugin_version is not None:
                versions[str(relative)] = str(plugin_version)

    unique_versions = set(versions.values())
    validation.check(
        len(unique_versions) <= 1,
        f"plugin versions diverge: {versions}",
    )


def validate_docs(validation: Validation) -> None:
    for relative in (
        "README.md",
        "PROVENANCE.md",
        "references/routing-contract.md",
        "references/lifecycle-contract.md",
        "references/artifact-contract.md",
    ):
        validation.check((ROOT / relative).is_file(), f"{relative}: required file is missing")


def main() -> int:
    validation = Validation()
    validate_skills(validation)
    validate_manifests(validation)
    validate_docs(validation)

    if validation.errors:
        print(f"FAILED: {len(validation.errors)} error(s)")
        for error in validation.errors:
            print(f"- {error}")
        return 1

    skill_count = len([path for path in SKILLS_DIR.iterdir() if path.is_dir()])
    print(f"PASSED: {skill_count} skills, {len(JSON_MANIFESTS)} manifests, 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
