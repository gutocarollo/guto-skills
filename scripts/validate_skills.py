#!/usr/bin/env python3
"""Validate the Guto Skills package.

The default mode validates the complete checked-out repository, including
byte-for-byte upstream files and explicitly tracked local adaptations.
``--custom-only`` validates the original/adapted Guto surfaces without requiring
the complete vendored tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

CUSTOM_SKILLS = {
    "guto-plan",
    "guto-build",
    "guto-verify",
    "guto-review",
    "clarification-plan",
}

VENDORED_SKILLS = {
    "context-engineering",
    "interview-me",
    "idea-refine",
    "spec-driven-development",
    "planning-and-task-breakdown",
    "source-driven-development",
    "incremental-implementation",
    "browser-testing-with-devtools",
    "debugging-and-error-recovery",
    "code-review-and-quality",
    "code-simplification",
    "security-and-hardening",
    "performance-optimization",
}

EXACT_SKILLS = CUSTOM_SKILLS | VENDORED_SKILLS

ORCHESTRATOR_ORDER = {
    "guto-plan": [
        "context-engineering",
        "interview-me",
        "idea-refine",
        "clarification-plan",
        "spec-driven-development",
        "planning-and-task-breakdown",
    ],
    "guto-build": [
        "context-engineering",
        "planning-and-task-breakdown",
        "source-driven-development",
        "incremental-implementation",
    ],
    "guto-verify": [
        "context-engineering",
        "browser-testing-with-devtools",
        "debugging-and-error-recovery",
    ],
    "guto-review": [
        "context-engineering",
        "code-review-and-quality",
        "code-simplification",
        "security-and-hardening",
        "performance-optimization",
    ],
}

MANIFEST_PATHS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
]

CUSTOM_ENGLISH_PATHS = [
    "README.md",
    "NOTICE.md",
    "skills/guto-plan/SKILL.md",
    "skills/guto-build/SKILL.md",
    "skills/guto-verify/SKILL.md",
    "skills/guto-review/SKILL.md",
    "skills/clarification-plan/SKILL.md",
    "skills/context-engineering/SKILL.md",
    *MANIFEST_PATHS,
]

FORBIDDEN_COUNCIL_TOKENS = {
    ".harness",
    "edge_id",
    "CRITICAL_BLOCK",
    "HIGH_FIX_NOW",
    "council-active",
    "PLAN-ADVERSARIAL-VERIFICATION",
    "agent_swarm_ledger",
    "execution-graph",
    "DELIVERY-COUNCIL",
}

PORTUGUESE_MARKERS = {
    " habilidades ",
    " planejamento ",
    " execução ",
    " verificação ",
    " revisão ",
    " obrigatório ",
    " obrigatória ",
    " contexto completo ",
    " não ",
    " usuário ",
    " decisão ",
    " evidência ",
    " objetivo ",
    " escopo ",
}

FRONTMATTER_RE = re.compile(r"\A---\n(?P<header>.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*([^\n]+)\s*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)
CHILD_LINK_RE = re.compile(r"\.\./([a-z0-9-]+)/SKILL\.md")

UPSTREAM_REPOSITORY = "https://github.com/addyosmani/agent-skills"
UPSTREAM_COMMIT = "7676817c12a1317454ae3898a0c5c1eacf5dd3d5"
ADAPTED_UPSTREAM_EXPECTED = {
    "skills/context-engineering/SKILL.md": "be991103fe2b13f7e5f6f5da9d3c6029ad30ac64",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing file: {path.relative_to(ROOT)}")
    except UnicodeDecodeError:
        errors.append(f"not valid UTF-8: {path.relative_to(ROOT)}")
    return ""


def unique_in_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def validate_frontmatter(skill_dir: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = read_text(skill_file, errors)
    if not text:
        return

    match = FRONTMATTER_RE.search(text)
    if not match:
        errors.append(f"missing YAML frontmatter: {skill_file.relative_to(ROOT)}")
        return

    header = match.group("header")
    name_match = NAME_RE.search(header)
    description_match = DESCRIPTION_RE.search(header)

    if not name_match:
        errors.append(f"frontmatter missing name: {skill_file.relative_to(ROOT)}")
    elif name_match.group(1).strip() != skill_dir.name:
        errors.append(
            f"frontmatter name mismatch in {skill_file.relative_to(ROOT)}: "
            f"{name_match.group(1).strip()!r} != {skill_dir.name!r}"
        )

    if not description_match or len(description_match.group(1).strip()) < 20:
        errors.append(f"frontmatter description is missing or too short: {skill_file.relative_to(ROOT)}")

    if len(text.splitlines()) > 500:
        errors.append(f"SKILL.md exceeds 500 lines: {skill_file.relative_to(ROOT)}")


def validate_exact_skill_tree(errors: list[str], custom_only: bool) -> None:
    if not SKILLS_DIR.is_dir():
        errors.append("missing skills/ directory")
        return

    actual = {
        path.name
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    expected = CUSTOM_SKILLS if custom_only else EXACT_SKILLS

    missing = sorted(expected - actual)
    extra = sorted(actual - EXACT_SKILLS)

    if missing:
        errors.append(f"missing skill directories: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected skill directories: {', '.join(extra)}")

    for name in sorted(actual & EXACT_SKILLS):
        validate_frontmatter(SKILLS_DIR / name, errors)


def validate_orchestrators(errors: list[str], custom_only: bool) -> None:
    for orchestrator, expected_order in ORCHESTRATOR_ORDER.items():
        path = SKILLS_DIR / orchestrator / "SKILL.md"
        text = read_text(path, errors)
        if not text:
            continue

        links = unique_in_order(CHILD_LINK_RE.findall(text))
        if links != expected_order:
            errors.append(
                f"{orchestrator} child-skill order/scope mismatch: "
                f"expected {expected_order}, got {links}"
            )

        if "context-engineering" not in links or links[0] != "context-engineering":
            errors.append(f"{orchestrator} must call context-engineering first")

        lower = text.lower()
        if "mandatory" not in lower or "context-engineering" not in lower:
            errors.append(f"{orchestrator} does not state mandatory context engineering")

        if orchestrator == "guto-review":
            for phrase in ["fresh independent", "context_gap_audit", "omitted_or_stale_context"]:
                if phrase not in lower:
                    errors.append(f"guto-review missing context-gap rule: {phrase}")

        if orchestrator == "guto-build":
            first_positions = [text.find(f"../{name}/SKILL.md") for name in expected_order]
            if any(position < 0 for position in first_positions) or first_positions != sorted(first_positions):
                errors.append("guto-build does not preserve the required fixed child-skill order")

        if not custom_only:
            for name in expected_order:
                sibling = SKILLS_DIR / name / "SKILL.md"
                if not sibling.is_file():
                    errors.append(f"{orchestrator} child skill is not vendored locally: skills/{name}/SKILL.md")


def validate_context_engineering(errors: list[str]) -> None:
    path = SKILLS_DIR / "context-engineering" / "SKILL.md"
    text = read_text(path, errors)
    if not text:
        return
    lower = text.lower()
    required_phrases = [
        "lexical search — always attempt",
        "codegraph — always attempt",
        "exploration loop",
        "material gap left?",
        "context pack contract",
        "lexical-only and graph-only",
        "task shape changes ordering, not inclusion",
    ]
    for phrase in required_phrases:
        if phrase not in lower:
            errors.append(f"context-engineering missing exploration contract: {phrase}")


def validate_english_custom_files(errors: list[str]) -> None:
    for relative in CUSTOM_ENGLISH_PATHS:
        path = ROOT / relative
        text = read_text(path, errors)
        if not text:
            continue
        normalized = " " + re.sub(r"\s+", " ", text.lower()) + " "
        found = sorted(marker.strip() for marker in PORTUGUESE_MARKERS if marker in normalized)
        if found:
            errors.append(f"non-English marker(s) in {relative}: {', '.join(found)}")


def validate_no_council_contract(errors: list[str]) -> None:
    for relative in [
        "README.md",
        "skills/guto-plan/SKILL.md",
        "skills/guto-build/SKILL.md",
        "skills/guto-verify/SKILL.md",
        "skills/guto-review/SKILL.md",
        "skills/clarification-plan/SKILL.md",
    ]:
        text = read_text(ROOT / relative, errors)
        for token in FORBIDDEN_COUNCIL_TOKENS:
            if token.lower() in text.lower():
                errors.append(f"forbidden Council contract token in {relative}: {token}")
        if "adaptive-" in text.lower():
            errors.append(f"forbidden adaptive-* naming in {relative}")


def manifest_version(data: object, path: str, errors: list[str]) -> str | None:
    if not isinstance(data, dict):
        errors.append(f"manifest root must be an object: {path}")
        return None

    if path.endswith("plugin.json"):
        version = data.get("version")
        return version if isinstance(version, str) else None

    plugins = data.get("plugins")
    if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
        version = plugins[0].get("version")
        return version if isinstance(version, str) else None
    return None


def validate_manifests(errors: list[str]) -> None:
    versions: dict[str, str] = {}
    for relative in MANIFEST_PATHS:
        path = ROOT / relative
        text = read_text(path, errors)
        if not text:
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in {relative}: {exc}")
            continue

        if not isinstance(data, dict) or data.get("name") != "guto-skills":
            errors.append(f"manifest name must be guto-skills: {relative}")

        version = manifest_version(data, relative, errors)
        if version is None:
            errors.append(f"manifest version missing: {relative}")
        else:
            versions[relative] = version

    if versions and len(set(versions.values())) != 1:
        errors.append(f"manifest versions do not match: {versions}")


def validate_mode(path: Path, expected_mode: str | None, relative: str, errors: list[str]) -> None:
    executable = bool(path.stat().st_mode & stat.S_IXUSR)
    actual_mode = "100755" if executable else "100644"
    if expected_mode != actual_mode:
        errors.append(f"upstream mode mismatch for {relative}: {actual_mode} != {expected_mode}")


def validate_upstream_lock(errors: list[str]) -> int:
    lock_path = ROOT / "UPSTREAM_LOCK.json"
    text = read_text(lock_path, errors)
    if not text:
        return 0

    try:
        lock = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid UPSTREAM_LOCK.json: {exc}")
        return 0

    source = lock.get("source", {})
    if source.get("repository") != UPSTREAM_REPOSITORY:
        errors.append("UPSTREAM_LOCK source repository mismatch")
    if source.get("commit") != UPSTREAM_COMMIT:
        errors.append("UPSTREAM_LOCK commit is not the reviewed pinned commit")
    if source.get("license") != "MIT":
        errors.append("UPSTREAM_LOCK license mismatch")

    files = lock.get("files")
    if not isinstance(files, dict):
        errors.append("UPSTREAM_LOCK files must be an object")
        return 0

    adapted = lock.get("adapted_files", {})
    if not isinstance(adapted, dict):
        errors.append("UPSTREAM_LOCK adapted_files must be an object")
        adapted = {}

    overlap = set(files) & set(adapted)
    if overlap:
        errors.append(f"UPSTREAM_LOCK paths cannot be both exact and adapted: {sorted(overlap)}")

    for relative, metadata in sorted(files.items()):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"locked upstream file missing: {relative}")
            continue
        data = path.read_bytes()
        actual_sha = git_blob_sha(data)
        expected_sha = metadata.get("sha") if isinstance(metadata, dict) else None
        if actual_sha != expected_sha:
            errors.append(f"upstream blob hash mismatch for {relative}: {actual_sha} != {expected_sha}")
        expected_mode = metadata.get("mode") if isinstance(metadata, dict) else None
        validate_mode(path, expected_mode, relative, errors)

    if set(adapted) != set(ADAPTED_UPSTREAM_EXPECTED):
        errors.append(
            "UPSTREAM_LOCK adapted file set mismatch: "
            f"expected {sorted(ADAPTED_UPSTREAM_EXPECTED)}, got {sorted(adapted)}"
        )

    for relative, metadata in sorted(adapted.items()):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"adapted upstream file missing: {relative}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"adapted upstream metadata must be an object: {relative}")
            continue
        expected_upstream = ADAPTED_UPSTREAM_EXPECTED.get(relative)
        if metadata.get("upstream_sha") != expected_upstream:
            errors.append(
                f"adapted upstream source mismatch for {relative}: "
                f"{metadata.get('upstream_sha')} != {expected_upstream}"
            )
        actual_local = git_blob_sha(path.read_bytes())
        if metadata.get("local_sha") != actual_local:
            errors.append(
                f"adapted local blob hash mismatch for {relative}: "
                f"{actual_local} != {metadata.get('local_sha')}"
            )
        validate_mode(path, metadata.get("mode"), relative, errors)
        if not str(metadata.get("adaptation") or "").strip():
            errors.append(f"adapted upstream file missing adaptation note: {relative}")

    return len(files) + len(adapted)


def validate_links(errors: list[str]) -> None:
    markdown_files = list(ROOT.glob("skills/**/*.md")) + list(ROOT.glob("references/*.md"))
    relative_link_re = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)|`(\.\./\.\./references/[^`]+)`")
    for path in markdown_files:
        text = read_text(path, errors)
        for match in relative_link_re.finditer(text):
            target = match.group(1) or match.group(2)
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository in {path.relative_to(ROOT)}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative link in {path.relative_to(ROOT)}: {target}")


def validate_no_symlinks(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink not allowed in package: {path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--custom-only",
        action="store_true",
        help="validate original/adapted Guto files without requiring the complete vendored tree",
    )
    args = parser.parse_args()

    errors: list[str] = []
    validate_exact_skill_tree(errors, args.custom_only)
    validate_orchestrators(errors, args.custom_only)
    validate_context_engineering(errors)
    validate_english_custom_files(errors)
    validate_no_council_contract(errors)
    validate_manifests(errors)
    validate_no_symlinks(errors)

    locked_files = 0
    if not args.custom_only:
        locked_files = validate_upstream_lock(errors)
        validate_links(errors)

    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.custom_only:
        print("PASSED: custom/adapted English skills, exact child scopes, exploration contract, and manifests")
    else:
        print(
            f"PASSED: {len(EXACT_SKILLS)} skills, {locked_files} pinned/adapted upstream files, "
            f"{len(MANIFEST_PATHS)} manifests, 0 errors"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
