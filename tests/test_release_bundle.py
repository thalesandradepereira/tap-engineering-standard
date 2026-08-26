from __future__ import annotations

import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_release_bundle import (
    ARCHIVE_NAME,
    CHECKSUM_NAME,
    SKILL_RELATIVE_DIR,
    build_release_bundle,
)


ROOT = Path(__file__).resolve().parents[1]


class ReleaseBundleTests(unittest.TestCase):
    def test_bundle_is_deterministic_and_checksum_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            first_archive, first_checksum = build_release_bundle(ROOT, temporary_root / "first")
            second_archive, second_checksum = build_release_bundle(ROOT, temporary_root / "second")

            self.assertEqual(first_archive.read_bytes(), second_archive.read_bytes())
            self.assertEqual(first_checksum.read_text(), second_checksum.read_text())

            digest = hashlib.sha256(first_archive.read_bytes()).hexdigest()
            self.assertEqual(first_checksum.read_text(), f"{digest}  {ARCHIVE_NAME}\n")
            self.assertEqual(first_checksum.name, CHECKSUM_NAME)

    def test_bundle_contains_the_complete_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            archive_path, _ = build_release_bundle(ROOT, Path(temporary_directory))
            skill_directory = ROOT / SKILL_RELATIVE_DIR
            expected = {
                f"tap-engineering-standard/{path.relative_to(skill_directory).as_posix()}"
                for path in skill_directory.rglob("*")
                if path.is_file() and not path.is_symlink()
            }

            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(set(archive.namelist()), expected)

    def test_release_builder_rejects_symbolic_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            fake_root = Path(temporary_directory)
            fake_skill = fake_root / SKILL_RELATIVE_DIR
            fake_skill.mkdir(parents=True)
            (fake_skill / "SKILL.md").write_text("safe\n", encoding="utf-8")
            (fake_skill / "target.txt").write_text("target\n", encoding="utf-8")
            (fake_skill / "link.txt").symlink_to(fake_skill / "target.txt")

            with self.assertRaisesRegex(ValueError, "Symbolic links are not allowed"):
                build_release_bundle(fake_root, fake_root / "dist")


if __name__ == "__main__":
    unittest.main()
