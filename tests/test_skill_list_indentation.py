"""Regression coverage for safe list-marker spacing in executable SKILL.md guidance."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_skill.py"
MODULE_SPEC = importlib.util.spec_from_file_location("tap_validate_skill_list_spacing", MODULE_PATH)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
validator = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(validator)


class SkillListIndentationValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.headings = "\n".join(
            marker for marker in validator.REQUIRED_SKILL_BODY_MARKERS if marker.startswith("#")
        )
        self.guidance = [
            marker for marker in validator.REQUIRED_SKILL_BODY_MARKERS if not marker.startswith("#")
        ]

    def test_rejects_five_spaces_after_bullet_marker(self) -> None:
        hidden = "\n".join("-     " + marker for marker in self.guidance)
        errors = validator.validate_skill_body(self.headings + "\n" + hidden + "\n")
        self.assertTrue(any("unsafe list indentation" in error for error in errors))
        self.assertTrue(any("required safety guidance" in error for error in errors))

    def test_rejects_five_spaces_after_ordered_marker(self) -> None:
        hidden = "\n".join("1.     " + marker for marker in self.guidance)
        errors = validator.validate_skill_body(self.headings + "\n" + hidden + "\n")
        self.assertTrue(any("unsafe list indentation" in error for error in errors))
        self.assertTrue(any("required safety guidance" in error for error in errors))

    def test_rejects_tab_after_list_marker(self) -> None:
        hidden = "\n".join("-\t" + marker for marker in self.guidance)
        errors = validator.validate_skill_body(self.headings + "\n" + hidden + "\n")
        self.assertTrue(any("unsafe list indentation" in error for error in errors))

    def test_accepts_one_to_four_spaces_after_list_marker(self) -> None:
        visible = "\n".join(
            "-" + (" " * spacing) + marker
            for spacing, marker in enumerate(self.guidance, start=1)
        )
        self.assertEqual(
            validator.validate_skill_body(self.headings + "\n" + visible + "\n"),
            [],
        )


if __name__ == "__main__":
    unittest.main()
