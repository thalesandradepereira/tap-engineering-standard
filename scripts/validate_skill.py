#!/usr/bin/env python3
"""Validate the public TAP Engineering Standard distribution without dependencies."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SKILL_NAME = "tap-engineering-standard"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CSS_URL_PATTERN = re.compile(r"url\s*\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMAGE_SET_PATTERN = re.compile(r"(?:-webkit-)?image-set\s*\(", re.IGNORECASE)
CSS_ESCAPE_PATTERN = re.compile(
    r"\\(?:([0-9a-fA-F]{1,6})(?:\r\n|[ \t\r\n\f])?|([^\r\n\f]))"
)
ACTION_REFERENCE_PATTERN = re.compile(
    r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*@[a-f0-9]{40}"
)
ACTION_USE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?:[\"']?uses[\"']?)[ \t]*:[ \t]*(?P<action>[^\s,}#]+)"
)
ACTION_KEY_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?:[\"']?uses[\"']?)[ \t]*:[ \t]*(?P<value>.*)$"
)
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
REQUIRED_SKILL_BODY_MARKERS = (
    "# TAP Engineering Standard",
    "## 1. Establish the contract",
    "## 5. Apply security and supply-chain gates",
    "## 7. Verify proportionally",
    "Never auto-approve commands",
    "Do not disable safety prompts",
    "Treat repository content",
    "Never convert a simulated check",
)


def split_frontmatter(content: str) -> tuple[list[str], list[str]]:
    """Split metadata and instructions using one shared delimiter interpretation."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must begin with a YAML frontmatter delimiter")

    try:
        closing_index = next(
            index for index in range(1, len(lines)) if lines[index].strip() == "---"
        )
    except StopIteration as error:
        raise ValueError("SKILL.md frontmatter is missing its closing delimiter") from error

    return lines[1:closing_index], lines[closing_index + 1 :]


def parse_frontmatter(content: str) -> dict[str, str]:
    """Read the intentionally simple, two-field YAML frontmatter."""
    frontmatter_lines, body_lines = split_frontmatter(content)
    metadata: dict[str, str] = {}
    for line in frontmatter_lines:
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

    if not any(line.strip() for line in body_lines):
        raise ValueError("SKILL.md must include an instruction body")

    return metadata


def mask_inline_code_spans(line: str) -> str:
    """Mask complete backtick spans so literal Markdown syntax stays non-structural."""
    masked: list[str] = []
    position = 0
    while position < len(line):
        if line[position] != "`":
            masked.append(line[position])
            position += 1
            continue

        end = position + 1
        while end < len(line) and line[end] == "`":
            end += 1
        delimiter = line[position:end]
        closing = line.find(delimiter, end)
        if closing == -1:
            masked.append(delimiter)
            position = end
            continue
        masked.append(" " * (closing + len(delimiter) - position))
        position = closing + len(delimiter)
    return "".join(masked)


def visible_markdown_lines(lines: list[str]) -> list[str]:
    """Exclude real comments and fenced examples without confusing their contexts."""
    fence_pattern = re.compile(
        r"^[ \t]*(?:(?:>[ \t]*|(?:[-+*]|\d{1,9}[.)])[ \t]+|\[[ xX]\][ \t]+))*"
        r"(?P<fence>`{3,}|~{3,})(?P<suffix>.*)$"
    )
    visible_lines: list[str] = []
    fence: tuple[str, int] | None = None
    comment = False
    opaque_html_tag: str | None = None
    opaque_html_open = re.compile(
        r"<(?P<tag>pre|code|script|style|textarea)(?:[ \t][^<>]*)?>",
        re.IGNORECASE,
    )

    for raw_line in lines:
        if fence is not None:
            character, length = fence
            closing = fence_pattern.match(raw_line)
            if (
                closing is not None
                and closing.group("fence").startswith(character)
                and len(closing.group("fence")) >= length
                and not closing.group("suffix").strip()
            ):
                fence = None
            continue

        opening = fence_pattern.match(raw_line) if not comment else None
        if opening is not None:
            marker = opening.group("fence")
            fence = (marker[0], len(marker))
            continue

        raw_line = mask_inline_code_spans(raw_line)
        fragments: list[str] = []
        position = 0
        while position < len(raw_line):
            if comment:
                closing_position = raw_line.find("-->", position)
                if closing_position == -1:
                    position = len(raw_line)
                    break
                comment = False
                position = closing_position + 3
                continue

            if opaque_html_tag is not None:
                closing_tag = re.search(
                    rf"</{re.escape(opaque_html_tag)}[ \t]*>",
                    raw_line[position:],
                    re.IGNORECASE,
                )
                if closing_tag is None:
                    position = len(raw_line)
                    break
                opaque_html_tag = None
                position += closing_tag.end()
                continue

            opening_position = raw_line.find("<!--", position)
            html_opening = opaque_html_open.search(raw_line, position)
            html_position = html_opening.start() if html_opening is not None else -1
            candidates = [candidate for candidate in (opening_position, html_position) if candidate >= 0]
            if not candidates:
                fragments.append(raw_line[position:])
                break
            next_position = min(candidates)
            fragments.append(raw_line[position:next_position])
            if opening_position == next_position:
                position = opening_position + 4
                comment = True
            else:
                assert html_opening is not None
                opaque_html_tag = html_opening.group("tag").lower()
                position = html_opening.end()

        line = "".join(fragments)
        opening = fence_pattern.match(line) if not comment else None
        if opening is not None:
            marker = opening.group("fence")
            fence = (marker[0], len(marker))
            continue
        if line and not re.match(r"^(?: {4}|\t)", line):
            visible_lines.append(line)

    return visible_lines


def validate_skill_body(content: str) -> list[str]:
    """Require the structural safeguards that define the published skill."""
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        try:
            _, lines = split_frontmatter(content)
        except ValueError:
            lines = []

    visible_body = "\n".join(visible_markdown_lines(lines))
    errors: list[str] = []
    for marker in REQUIRED_SKILL_BODY_MARKERS:
        if marker.startswith("#"):
            found = re.search(
                rf"^[ \t]{{0,3}}{re.escape(marker)}[ \t]*$",
                visible_body,
                re.MULTILINE,
            ) is not None
        else:
            found = re.search(
                rf"^[ \t]{{0,3}}(?:(?:[-+*]|\d{{1,9}}[.)])[ \t]+)?"
                rf"{re.escape(marker)}(?=$|[ \t,.;:])",
                visible_body,
                re.MULTILINE,
            ) is not None
        if not found:
            errors.append(f"SKILL.md is missing required safety guidance: {marker}")
    return errors


def validate_svg(path: Path) -> None:
    """Require static SVG without active content, entities, or remote references."""
    source = path.read_text(encoding="utf-8")
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", source, re.IGNORECASE):
        raise ValueError(f"SVG document types and entities are not allowed: {path}")
    if re.search(r"<\?(?!xml(?:[ \t\r\n]|\?>))", source, re.IGNORECASE):
        raise ValueError(f"SVG processing instructions are not allowed: {path}")

    root = ET.fromstring(source)
    if root.tag.rsplit("}", maxsplit=1)[-1] != "svg":
        raise ValueError(f"Expected an SVG root element: {path}")

    for element in root.iter():
        tag = element.tag.rsplit("}", maxsplit=1)[-1].lower()
        if tag == "script":
            raise ValueError(f"Embedded SVG scripts are not allowed: {path}")
        if tag == "foreignobject":
            raise ValueError(f"Embedded HTML in SVG assets is not allowed: {path}")
        if tag in {
            "animate",
            "animatecolor",
            "animatemotion",
            "animatetransform",
            "discard",
            "set",
        }:
            raise ValueError(f"SVG animation elements are not allowed: {path}")

        if tag == "style":
            validate_svg_css("".join(element.itertext()), path)

        for attribute, value in element.attrib.items():
            normalized_attribute = attribute.rsplit("}", maxsplit=1)[-1].lower()
            if normalized_attribute.startswith("on"):
                raise ValueError(f"SVG event handlers are not allowed: {path}")
            if normalized_attribute == "base":
                raise ValueError(f"SVG base URL overrides are not allowed: {path}")
            if normalized_attribute in {"href", "src"}:
                if not value.startswith("#"):
                    raise ValueError(f"External SVG references are not allowed: {path}")
            validate_svg_css(value, path)


def validate_svg_css(value: str, path: Path) -> None:
    """Allow CSS fragment references while blocking imports and remote URLs."""
    def decode_escape(match: re.Match[str]) -> str:
        hexadecimal, literal = match.groups()
        if hexadecimal is None:
            return literal
        codepoint = int(hexadecimal, 16)
        if codepoint == 0 or codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
            return "\uFFFD"
        return chr(codepoint)

    normalized = re.sub(r"\\(?:\r\n|[\n\r\f])", "", value)
    normalized = CSS_ESCAPE_PATTERN.sub(decode_escape, normalized)
    normalized = re.sub(r"/\*.*?\*/", "", normalized, flags=re.DOTALL)

    if re.search(r"@import\b", normalized, re.IGNORECASE):
        raise ValueError(f"External SVG CSS imports are not allowed: {path}")

    for match in CSS_URL_PATTERN.finditer(normalized):
        if not match.group(2).strip().startswith("#"):
            raise ValueError(f"External SVG CSS references are not allowed: {path}")

    for image_set in CSS_IMAGE_SET_PATTERN.finditer(normalized):
        depth = 1
        quote: str | None = None
        quote_depth = 0
        quote_start = 0
        for index in range(image_set.end(), len(normalized)):
            character = normalized[index]
            if quote is not None:
                if character == quote:
                    if quote_depth == 1:
                        candidate = normalized[quote_start:index].strip()
                        if not candidate.startswith("#"):
                            raise ValueError(
                                f"External SVG CSS references are not allowed: {path}"
                            )
                    quote = None
                continue
            if character in {"'", '"'}:
                quote = character
                quote_depth = depth
                quote_start = index + 1
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    break


def strip_yaml_comment(line: str) -> str:
    """Remove YAML comments while preserving quoted scalar contents."""
    quote: str | None = None
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote is not None:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.rstrip()


def mask_quoted_yaml(line: str) -> str:
    """Mask quoted scalars so structural checks inspect YAML syntax only."""
    masked: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(line):
        character = line[index]
        if quote is not None:
            masked.append(" ")
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and character == "\\":
                escaped = True
            elif character == quote:
                if quote == "'" and index + 1 < len(line) and line[index + 1] == "'":
                    masked.append(" ")
                    index += 1
                else:
                    quote = None
            index += 1
            continue
        if character in {"'", '"'}:
            quote = character
            masked.append(" ")
        else:
            masked.append(character)
        index += 1
    return "".join(masked)


def validate_strict_yaml_subset(lines: list[str]) -> list[str]:
    """Reject valid YAML features that the dependency-free parser cannot safely interpret."""
    errors: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        if re.match(r'^\s*(?:-\s*)?"[^"\n]*\\[^"\n]*"\s*:', line):
            errors.append("GitHub Actions workflow uses escaped mapping keys")

        structural = mask_quoted_yaml(line)
        structural = re.sub(r"\$\{\{.*?\}\}", "", structural)
        if "{" in structural or "}" in structural:
            errors.append("GitHub Actions workflow uses unsupported flow mapping syntax")
        if re.match(r"^\s*[?%]", structural):
            errors.append("GitHub Actions workflow uses unsupported explicit YAML syntax")
        if re.search(r"(?:^|[\s[,])<<\s*:", structural):
            errors.append("GitHub Actions workflow uses unsupported YAML merge keys")
        if re.search(r"(?:^|[\s:[,{])(?:[&*])[A-Za-z0-9_-]+", structural):
            errors.append("GitHub Actions workflow uses unsupported YAML aliases")
    return errors


def validate_agent_metadata(metadata_text: str) -> list[str]:
    """Validate active interface and policy keys without trusting YAML comments."""
    errors: list[str] = []
    sections: dict[str, dict[str, str]] = {}
    section: str | None = None

    for raw_line in metadata_text.splitlines():
        line = strip_yaml_comment(raw_line)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        key, separator, value = line.strip().partition(":")
        if not separator:
            continue
        if indent == 0:
            section = key
            if section in sections:
                errors.append(f"Duplicate agent metadata section: {section}")
            sections.setdefault(section, {})
        elif indent == 2 and section is not None:
            if key in sections[section]:
                errors.append(f"Duplicate agent metadata field: {section}.{key}")
            sections[section][key] = value.strip()

    interface = sections.get("interface", {})
    policy = sections.get("policy", {})
    if interface.get("display_name") != "TAP Engineering Standard":
        errors.append("Agent metadata does not contain the expected display name")
    if policy.get("allow_implicit_invocation") != "true":
        errors.append("Agent metadata must preserve implicit invocation")
    if "$tap-engineering-standard" not in interface.get("default_prompt", ""):
        errors.append("Agent default prompt must reference the canonical skill name")
    for icon_key in ("icon_small", "icon_large"):
        if interface.get(icon_key) != "assets/icon.svg":
            errors.append(f"Agent metadata must reference the local skill icon: {icon_key}")

    return errors


def is_token_permission_mapping(lines: list[str], index: int, indent: int) -> bool:
    """Limit token permission declarations to the workflow root and job mappings."""
    if indent == 0:
        return True

    ancestors: list[str] = []
    child_indent = indent
    for candidate in reversed(lines[:index]):
        if not candidate.strip():
            continue
        candidate_indent = len(candidate) - len(candidate.lstrip())
        if candidate_indent >= child_indent:
            continue
        key, separator, _ = candidate.strip().partition(":")
        if not separator:
            return False
        ancestors.append(key.strip("'\""))
        child_indent = candidate_indent
        if candidate_indent == 0:
            break

    return len(ancestors) == 2 and ancestors[1] == "jobs"


def validate_workflow_permissions(lines: list[str]) -> list[str]:
    """Reject writable, aliased, or unsupported permission mappings."""
    errors: list[str] = []
    permission_key = re.compile(
        r"^(?P<indent>[ \t]*)(?:permissions|['\"]permissions['\"])[ \t]*:[ \t]*(?P<value>.*)$"
    )
    scope_key = re.compile(
        r"^[ \t]+(?:['\"]?)(?P<name>[a-z][a-z-]*)(?:['\"]?)[ \t]*:[ \t]*(?P<value>.*)$"
    )

    for index, line in enumerate(lines):
        match = permission_key.match(line)
        if match is None:
            continue

        indent = len(match.group("indent"))
        if not is_token_permission_mapping(lines, index, indent):
            continue

        if match.group("value"):
            errors.append("GitHub Actions workflow uses unsupported permissions syntax")
            if re.search(r"(?:^|[\s,:{])['\"]?write(?:-all)?['\"]?(?:$|[\s,}])", line):
                errors.append("GitHub Actions workflow must not request write permissions")
            continue

        seen_scopes: set[str] = set()
        for candidate in lines[index + 1 :]:
            if not candidate.strip():
                continue
            candidate_indent = len(candidate) - len(candidate.lstrip())
            if candidate_indent <= indent:
                break
            scope_match = scope_key.match(candidate)
            if scope_match is None:
                errors.append("GitHub Actions workflow uses unsupported permissions syntax")
                continue
            scope = scope_match.group("name")
            raw_access = scope_match.group("value")
            access = raw_access.strip("'\"")
            if scope in seen_scopes:
                errors.append("GitHub Actions workflow contains duplicate permissions")
            seen_scopes.add(scope)
            if access in {"write", "write-all"}:
                errors.append("GitHub Actions workflow must not request write permissions")
            elif access not in {"read", "none"}:
                errors.append("GitHub Actions workflow uses unsupported permissions syntax")

    return errors


def step_content_indent(line: str) -> int:
    """Return the mapping indent for normal and compact YAML list-item steps."""
    stripped = line.lstrip(" \t")
    indent = len(line) - len(stripped)
    if stripped.startswith("-"):
        content = stripped[1:]
        return indent + 1 + len(content) - len(content.lstrip(" \t"))
    return indent


def mask_yaml_block_scalars(lines: list[str]) -> list[str]:
    """Keep YAML mappings visible while excluding indented block-scalar payloads."""
    masked: list[str] = []
    scalar_indent: int | None = None

    for line in lines:
        if scalar_indent is not None:
            if not line.strip():
                masked.append("")
                continue
            indent = len(line) - len(line.lstrip(" \t"))
            if indent > scalar_indent:
                masked.append("")
                continue
            scalar_indent = None

        masked.append(line)
        if re.search(r":[ \t]*[>|](?:[1-9][+-]?|[+-][1-9]?)?[ \t]*$", line):
            scalar_indent = step_content_indent(line)

    return masked


def checkout_disables_credentials(lines: list[str], index: int, indent: int) -> bool:
    """Require exactly one false setting inside the checkout action's with block."""
    with_blocks: list[tuple[int, int]] = []
    for position in range(index + 1, len(lines)):
        candidate = lines[position]
        if not candidate.strip():
            continue
        candidate_indent = len(candidate) - len(candidate.lstrip())
        if candidate_indent < indent:
            break
        if candidate_indent == indent and re.fullmatch(r"[ \t]*with:[ \t]*", candidate):
            with_blocks.append((position, candidate_indent))

    if len(with_blocks) != 1:
        return False

    with_position, with_indent = with_blocks[0]
    settings: list[str] = []
    child_indent: int | None = None
    for candidate in lines[with_position + 1 :]:
        if not candidate.strip():
            continue
        candidate_indent = len(candidate) - len(candidate.lstrip())
        if candidate_indent <= with_indent:
            break
        if child_indent is None:
            child_indent = candidate_indent
        if candidate_indent != child_indent:
            continue
        match = re.fullmatch(r"[ \t]*persist-credentials:[ \t]*(.*)", candidate)
        if match is not None:
            settings.append(match.group(1).strip())

    return settings == ["false"]


def validate_workflow(workflow_text: str, *, require_checkout: bool = False) -> list[str]:
    """Validate the small, intentionally dependency-free GitHub Actions workflow."""
    errors: list[str] = []
    lines = mask_yaml_block_scalars(
        [strip_yaml_comment(line) for line in workflow_text.splitlines()]
    )
    active_lines = [line for line in lines if line.strip()]
    active_text = "\n".join(active_lines)

    errors.extend(validate_strict_yaml_subset(lines))

    permissions_match = re.search(
        r"^permissions:[ \t]*(?:#[^\n]*)?\n((?:^[ \t]+[^\n]*(?:\n|$))+)",
        active_text,
        re.MULTILINE,
    )
    if not permissions_match or not re.search(
        r"^[ \t]+contents:[ \t]+read(?:[ \t]+#.*)?$",
        permissions_match.group(1),
        re.MULTILINE,
    ):
        errors.append("GitHub Actions workflow must request read-only contents permission")

    errors.extend(validate_workflow_permissions(lines))

    if re.search(r"(?<![A-Za-z0-9_-])pull_request_target(?![A-Za-z0-9_-])", active_text):
        errors.append("GitHub Actions workflow must not use pull_request_target")

    checkout_found = False
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        action_key = ACTION_KEY_PATTERN.search(line)
        if action_key is not None and not action_key.group("value").strip():
            errors.append("GitHub Actions workflow uses unsupported multiline action syntax")
        for action_match in ACTION_USE_PATTERN.finditer(line):
            action = action_match.group("action").strip("\"'")
            if not ACTION_REFERENCE_PATTERN.fullmatch(action):
                errors.append(
                    f"GitHub Actions dependency must be pinned to a complete commit SHA: {action}"
                )
                continue

            if not action.startswith("actions/checkout@"):
                continue

            checkout_found = True
            indent = step_content_indent(line)
            if not checkout_disables_credentials(lines, index, indent):
                errors.append("Checkout action must disable credential persistence")

    if require_checkout and not checkout_found:
        errors.append("Checkout action must be pinned to a complete commit SHA")

    return errors


def validate_repository(root: Path) -> list[str]:
    """Return actionable errors; an empty list indicates a valid repository."""
    errors: list[str] = []
    skill_directory = root / "skills" / SKILL_NAME
    checked_files: dict[Path, bool] = {}

    def repository_files() -> list[Path]:
        """Return tracked and non-ignored files, with a safe source-tree fallback."""
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                check=False,
                capture_output=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            result = None

        if result is not None and result.returncode == 0:
            return sorted(
                root / Path(raw_path.decode("utf-8"))
                for raw_path in result.stdout.split(b"\0")
                if raw_path
            )

        paths: list[Path] = []
        for directory, names, filenames in os.walk(root, topdown=True, followlinks=False):
            current = Path(directory)
            retained_names: list[str] = []
            for name in names:
                path = current / name
                relative = path.relative_to(root)
                if path.is_symlink():
                    paths.append(path)
                elif name not in {".git", ".venv", "__pycache__"}:
                    retained_names.append(name)
            names[:] = retained_names
            paths.extend(current / filename for filename in filenames)
        return sorted(paths)

    def validate_file_path(path: Path, missing_error: str) -> bool:
        if path in checked_files:
            return checked_files[path]

        relative_path = path.relative_to(root)
        candidate = root
        for component in relative_path.parts:
            candidate /= component
            if candidate.is_symlink():
                errors.append(
                    f"Symbolic links and external repository files are not allowed: {relative_path}"
                )
                checked_files[path] = False
                return False

        if not path.is_file():
            errors.append(missing_error)
            checked_files[path] = False
            return False

        if not path.resolve().is_relative_to(root.resolve()):
            errors.append(
                f"Symbolic links and external repository files are not allowed: {relative_path}"
            )
            checked_files[path] = False
            return False

        checked_files[path] = True
        return True

    repository_paths = repository_files()
    for repository_path in repository_paths:
        relative_path = repository_path.relative_to(root)
        if repository_path.is_file() or repository_path.is_symlink():
            validate_file_path(repository_path, f"Invalid repository file: {relative_path}")

    for relative_path in REQUIRED_DOCUMENTS:
        validate_file_path(
            root / relative_path, f"Missing required repository document: {relative_path}"
        )

    for relative_path in REQUIRED_SKILL_FILES:
        validate_file_path(
            skill_directory / relative_path, f"Missing required skill file: {relative_path}"
        )

    skill_path = skill_directory / "SKILL.md"
    if checked_files.get(skill_path):
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
            errors.extend(validate_skill_body(skill_text))
            for reference in re.findall(r"`(references/[a-z0-9-]+\.md)`", skill_text):
                validate_file_path(
                    skill_directory / reference,
                    f"Skill references a missing specialist playbook: {reference}",
                )
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"Invalid skill frontmatter: {error}")

    metadata_path = skill_directory / "agents" / "openai.yaml"
    if checked_files.get(metadata_path):
        metadata_text = metadata_path.read_text(encoding="utf-8")
        errors.extend(validate_agent_metadata(metadata_text))

    required_svg_paths = (
        root / "assets" / "tap-engineering-banner.svg",
        skill_directory / "assets" / "icon.svg",
    )
    svg_paths = set(required_svg_paths)
    svg_paths.update(path for path in repository_paths if path.suffix.lower() == ".svg")
    for svg_path in sorted(svg_paths):
        if not validate_file_path(
            svg_path, f"Missing required SVG asset: {svg_path.relative_to(root)}"
        ):
            continue
        try:
            validate_svg(svg_path)
        except (ET.ParseError, OSError, ValueError) as error:
            errors.append(f"Invalid SVG asset: {error}")

    workflow_path = root / ".github" / "workflows" / "validate-skill.yml"
    workflow_paths = {workflow_path}
    if workflow_path.parent.is_dir():
        workflow_paths.update(
            path for path in workflow_path.parent.iterdir() if path.suffix.lower() in {".yml", ".yaml"}
        )
    for candidate in sorted(workflow_paths):
        if validate_file_path(candidate, "Missing GitHub Actions validation workflow"):
            workflow_text = candidate.read_text(encoding="utf-8")
            errors.extend(validate_workflow(workflow_text, require_checkout=candidate == workflow_path))

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
