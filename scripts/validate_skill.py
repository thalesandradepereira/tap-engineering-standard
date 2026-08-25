#!/usr/bin/env python3
"""Validate the public TAP Engineering Standard distribution without dependencies."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SKILL_NAME = "tap-engineering-standard"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_DOCUMENTS = (
    "README.md",
    "README.pt-BR.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
)
REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "references/qa-playbooks.md",
    "references/security-gate.md",
)


def parse_frontmatter(content: str) -> dict[str, str]:
    """Read the intentionally simple, two-field YAML frontmatter."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must begin with a YAML frontmatter delimiter")

    try:
        closing_index = next(
            index for index in range(1, len(lines)) if lines[index].strip() == "---"
        )
    except StopIteration as error:
        raise ValueError("SKILL.md frontmatter is missing its closing delimiter") from error

    metadata: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            raise ValueError(f"Invalid frontmatter entry: {line!r}")
        normalized_key = key.strip()
        if normalized_key in metadata:
            raise ValueError(f"Duplicate frontmatter field: {normalized_key}")
        metadata[normalized_key] = value.strip()

    unexpected = set(metadata) - {"name", "description"}
    if unexpected:
        raise ValueError(f"Unsupported frontmatter fields: {', '.join(sorted(unexpected))}")

    missing = {"name", "description"} - set(metadata)
    if missing:
        raise ValueError(f"Missing frontmatter fields: {', '.join(sorted(missing))}")

    if closing_index + 1 >= len(lines):
        raise ValueError("SKILL.md must include an instruction body")

    return metadata


def validate_svg(path: Path) -> None:
    """Require parseable SVG without embedded scripts or remote references."""
    root = ET.parse(path).getroot()
    if root.tag.rsplit("}", maxsplit=1)[-1] != "svg":
        raise ValueError(f"Expected an SVG root element: {path}")

    for element in root.iter():
        if element.tag.rsplit("}", maxsplit=1)[-1].lower() == "script":
            raise ValueError(f"Embedded SVG scripts are not allowed: {path}")
        for attribute, value in element.attrib.items():
            if attribute.lower().startswith("on"):
                raise ValueError(f"SVG event handlers are not allowed: {path}")
            if attribute.rsplit("}", maxsplit=1)[-1] in {"href", "src"}:
                if not value.startswith("#"):
                    raise ValueError(f"External SVG references are not allowed: {path}")


def validate_repository(root: Path) -> list[str]:
    """Return actionable errors; an empty list indicates a valid repository."""
    errors: list[str] = []
    skill_directory = root / "skills" / SKILL_NAME

    for relative_path in REQUIRED_DOCUMENTS:
        if not (root / relative_path).is_file():
            errors.append(f"Missing required repository document: {relative_path}")

    for relative_path in REQUIRED_SKILL_FILES:
        if not (skill_directory / relative_path).is_file():
            errors.append(f"Missing required skill file: {relative_path}")

    skill_path = skill_directory / "SKILL.md"
    if skill_path.is_file():
        try:
            skill_text = skill_path.read_text(encoding="utf-8")
            metadata = parse_frontmatter(skill_text)
            name = metadata["name"]
            if name != SKILL_NAME:
                errors.append(f"Expected skill name {SKILL_NAME!r}, found {name!r}")
            if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
                errors.append("Skill name must be lowercase kebab-case and at most 64 characters")
            if len(metadata["description"]) < 80:
                errors.append("Skill description must explain both its purpose and triggers")
            for reference in re.findall(r"`(references/[a-z0-9-]+\.md)`", skill_text):
                if not (skill_directory / reference).is_file():
                    errors.append(f"Skill references a missing specialist playbook: {reference}")
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"Invalid skill frontmatter: {error}")

    metadata_path = skill_directory / "agents" / "openai.yaml"
    if metadata_path.is_file():
        metadata_text = metadata_path.read_text(encoding="utf-8")
        if "display_name: TAP Engineering Standard" not in metadata_text:
            errors.append("Agent metadata does not contain the expected display name")
        if "allow_implicit_invocation: true" not in metadata_text:
            errors.append("Agent metadata must preserve implicit invocation")
        if "$tap-engineering-standard" not in metadata_text:
            errors.append("Agent default prompt must reference the canonical skill name")

    for svg_path in (
        root / "assets" / "tap-engineering-banner.svg",
        skill_directory / "assets" / "icon.svg",
    ):
        if not svg_path.is_file():
            errors.append(f"Missing required SVG asset: {svg_path.relative_to(root)}")
            continue
        try:
            validate_svg(svg_path)
        except (ET.ParseError, OSError, ValueError) as error:
            errors.append(f"Invalid SVG asset: {error}")

    workflow_path = root / ".github" / "workflows" / "validate-skill.yml"
    if not workflow_path.is_file():
        errors.append("Missing GitHub Actions validation workflow")
    else:
        workflow_text = workflow_path.read_text(encoding="utf-8")
        if "contents: read" not in workflow_text:
            errors.append("GitHub Actions workflow must request read-only contents permission")
        if "pull_request_target:" in workflow_text:
            errors.append("GitHub Actions workflow must not use pull_request_target")
        if not re.search(r"actions/checkout@[a-f0-9]{40}\b", workflow_text):
            errors.append("Checkout action must be pinned to a complete commit SHA")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {SKILL_NAME} distribution and security invariants validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
