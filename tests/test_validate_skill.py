"""Regression coverage for the dependency-free skill validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_skill.py"
MODULE_SPEC = importlib.util.spec_from_file_location("tap_validate_skill", MODULE_PATH)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
validator = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(validator)


class FrontmatterValidationTests(unittest.TestCase):
    def test_accepts_valid_frontmatter(self) -> None:
        metadata = validator.parse_frontmatter(
            "---\nname: tap-engineering-standard\ndescription: Useful engineering instructions\n---\n# Body\n"
        )
        self.assertEqual(metadata["name"], "tap-engineering-standard")

    def test_rejects_missing_delimiter(self) -> None:
        with self.assertRaisesRegex(ValueError, "must begin"):
            validator.parse_frontmatter("name: example\n")

    def test_rejects_unclosed_frontmatter(self) -> None:
        with self.assertRaisesRegex(ValueError, "closing delimiter"):
            validator.parse_frontmatter("---\nname: example\ndescription: example\n")

    def test_rejects_missing_description(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing frontmatter"):
            validator.parse_frontmatter("---\nname: example\n---\n# Body\n")

    def test_rejects_empty_instruction_body(self) -> None:
        with self.assertRaisesRegex(ValueError, "instruction body"):
            validator.parse_frontmatter("---\nname: example\ndescription: example\n---")

    def test_rejects_duplicate_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validator.parse_frontmatter(
                "---\nname: one\nname: two\ndescription: example\n---\n# Body\n"
            )

    def test_rejects_unsupported_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            validator.parse_frontmatter(
                "---\nname: example\ndescription: example\nauthor: someone\n---\n# Body\n"
            )


class SvgValidationTests(unittest.TestCase):
    def test_rejects_embedded_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.svg"
            path.write_text("<svg><script>alert(1)</script></svg>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "scripts"):
                validator.validate_svg(path)

    def test_rejects_remote_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.svg"
            path.write_text('<svg><image href="https://example.com/image.png"/></svg>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "External"):
                validator.validate_svg(path)

    def test_rejects_event_handlers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.svg"
            path.write_text('<svg onload="alert(1)"/>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "event handlers"):
                validator.validate_svg(path)

    def test_accepts_internal_fragment_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "safe.svg"
            path.write_text('<svg><use href="#shape"/></svg>', encoding="utf-8")
            validator.validate_svg(path)

    def test_rejects_non_svg_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.svg"
            path.write_text("<html/>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SVG root"):
                validator.validate_svg(path)

    def test_rejects_namespaced_remote_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.svg"
            path.write_text(
                '<svg xmlns:xlink="http://www.w3.org/1999/xlink">'
                '<use xlink:href="https://example.com/icon.svg"/></svg>',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "External"):
                validator.validate_svg(path)


class RepositoryValidationTests(unittest.TestCase):
    def test_current_repository_is_valid(self) -> None:
        root = MODULE_PATH.parents[1]
        self.assertEqual(validator.validate_repository(root), [])

    def test_empty_repository_reports_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_repository(Path(directory))
            self.assertTrue(any("README.md" in error for error in errors))
            self.assertTrue(any("SKILL.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
