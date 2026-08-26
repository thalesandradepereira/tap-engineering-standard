#!/usr/bin/env python3
"""Build a deterministic Agent Skill release bundle and SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import stat
import zipfile
from pathlib import Path

ARCHIVE_NAME = "tap-engineering-standard-skill.zip"
CHECKSUM_NAME = "SHA256SUMS"
SKILL_RELATIVE_DIR = Path("skills") / "tap-engineering-standard"
ARCHIVE_ROOT = Path("tap-engineering-standard")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def iter_skill_files(root: Path) -> list[Path]:
    """Return regular skill files in stable order and reject symbolic links."""
    skill_directory = root / SKILL_RELATIVE_DIR
    if not skill_directory.is_dir():
        raise FileNotFoundError(f"Skill directory not found: {skill_directory}")

    resolved_skill_directory = skill_directory.resolve()
    files: list[Path] = []
    for path in skill_directory.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not allowed in release bundles: {path}")
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(resolved_skill_directory):
            raise ValueError(f"Release file escapes the skill directory: {path}")
        files.append(path)

    return sorted(files, key=lambda path: path.relative_to(skill_directory).as_posix())


def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release_bundle(root: Path, output_directory: Path) -> tuple[Path, Path]:
    """Create a byte-for-byte deterministic ZIP and a matching checksum file."""
    root = root.resolve()
    skill_directory = root / SKILL_RELATIVE_DIR
    resolved_skill_directory = skill_directory.resolve()

    output_directory.mkdir(parents=True, exist_ok=True)
    resolved_output_directory = output_directory.resolve()
    if resolved_output_directory.is_relative_to(resolved_skill_directory):
        raise ValueError("Release output directory must be outside the distributable skill directory")

    archive_path = resolved_output_directory / ARCHIVE_NAME
    checksum_path = resolved_output_directory / CHECKSUM_NAME

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in iter_skill_files(root):
            relative_path = path.relative_to(skill_directory)
            archive_name = (ARCHIVE_ROOT / relative_path).as_posix()
            info = zipfile.ZipInfo(archive_name, date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, path.read_bytes())

    digest = sha256_file(archive_path)
    checksum_path.write_text(f"{digest}  {ARCHIVE_NAME}\n", encoding="utf-8")
    return archive_path, checksum_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the deterministic TAP Engineering Standard skill release bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to <repository>/dist.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    output_directory = args.output_dir or root / "dist"
    archive_path, checksum_path = build_release_bundle(root, output_directory)
    print(f"Built: {archive_path}")
    print(f"Checksum: {checksum_path}")
    print(f"SHA-256: {sha256_file(archive_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
