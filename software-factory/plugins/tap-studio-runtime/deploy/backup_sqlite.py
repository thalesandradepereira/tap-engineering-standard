"""Consistent offline SQLite snapshot of TAP Studio via the SQLite backup API.

Use only on authorized deployment. The tool creates no network connections, does
not read secrets, and keeps backups separate from the live SQLite volume.
"""
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import secrets
import sqlite3
import tempfile


def make_backup(source: Path, directory: Path) -> Path:
    source = Path(source)
    directory = Path(directory)
    if source.is_symlink() or not source.is_file():
        raise ValueError('Expected an existing regular SQLite database')
    if directory.is_symlink() or directory.resolve() == source.parent.resolve():
        raise ValueError('Backup directory must not be the live database directory')
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not directory.is_dir():
        raise ValueError('Backup destination is not a directory')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    filename = f'tap-studio-{stamp}-{secrets.token_hex(4)}.sqlite3'
    fd, temp_name = tempfile.mkstemp(prefix='.tap-pending-', suffix='.sqlite3', dir=directory)
    os.fchmod(fd, 0o600)
    os.close(fd)
    temporary = Path(temp_name)
    final = directory / filename
    try:
        with closing(sqlite3.connect(f'file:{source.resolve()}?mode=ro', uri=True, timeout=10)) as live:
            with closing(sqlite3.connect(temporary, timeout=10)) as snapshot:
                live.backup(snapshot, pages=100, sleep=0.1)
                if snapshot.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise RuntimeError('Backup integrity check failed')
        os.replace(temporary, final)
        return final
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    source = Path(os.environ.get('TAP_STUDIO_DB_PATH', '/data/studio.db'))
    backups = Path(os.environ.get('TAP_STUDIO_BACKUP_DIR', '/backups'))
    completed = make_backup(source, backups)
    sha256 = hashlib.sha256(completed.read_bytes()).hexdigest()
    print(f'Backup completed: {completed.name}; SHA256={sha256}; copy to offsite encrypted storage')


if __name__ == '__main__':
    main()
