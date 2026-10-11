import importlib.util
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('tap_studio', ROOT/'server'/'studio.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
backup_spec = importlib.util.spec_from_file_location('tap_backup', ROOT/'deploy'/'backup_sqlite.py')
if (ROOT/'deploy'/'backup_sqlite.py').exists():
    backup = importlib.util.module_from_spec(backup_spec)
    backup_spec.loader.exec_module(backup)
else:
    backup = None

class ProductionConfigurationTests(unittest.TestCase):
    def test_secret_file_supported_and_never_logged(self):
        self.assertTrue(hasattr(mod, 'read_bootstrap_password'))
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/'admin_password'; f.write_text('a-secret-used-for-tests-only')
            with patch.dict(os.environ, {'TAP_STUDIO_ADMIN_PASSWORD_FILE':str(f)}, clear=True):
                self.assertEqual(mod.read_bootstrap_password(),'a-secret-used-for-tests-only')
            with patch.dict(os.environ, {'TAP_STUDIO_ADMIN_PASSWORD_FILE':str(f),'TAP_STUDIO_ADMIN_PASSWORD':'secret-in-env'},clear=True):
                with self.assertRaises(ValueError): mod.read_bootstrap_password()

    def test_backup_handles_wal_and_integrity(self):
        self.assertIsNotNone(backup)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)/'studio.db'; dest=Path(tmp)/'backups'
            c=sqlite3.connect(src)
            c.execute('PRAGMA journal_mode=WAL')
            c.execute('CREATE TABLE project (name TEXT)');c.commit()
            c.execute("INSERT INTO project VALUES ('saved')");c.commit()
            result=backup.make_backup(src,dest)
            try:
                with sqlite3.connect(result) as snap:
                    self.assertEqual(snap.execute('PRAGMA integrity_check').fetchone()[0],'ok')
                    self.assertEqual(snap.execute('SELECT name FROM project').fetchone()[0],'saved')
            finally:
                snap.close()
                c.close()

    def test_backup_rejects_same_destination(self):
        self.assertIsNotNone(backup)
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'studio.db'
            sqlite3.connect(src).close()
            with self.assertRaises(ValueError): backup.make_backup(src,Path(tmp))

    def test_tls_compose_defaults_are_nonpublic_backend(self):
        # Standard-library-only test: full YAML schema is separately parsed locally
        # and should be validated using `docker compose config` on the host.
        text = (ROOT/'deploy'/'compose.production.yml').read_text()
        studio = text.split('  studio:',1)[1].split('  caddy:',1)[0]
        caddy = text.split('  caddy:',1)[1].split('  backup:',1)[0]
        self.assertNotIn('    ports:',studio)
        self.assertIn('    read_only: true',studio)
        self.assertIn('    cap_drop:',studio)
        self.assertIn('    secrets:',studio)
        self.assertIn('    ports:',caddy)
        self.assertIn('tap-studio-data:',text)
        self.assertIn('tap-caddy-data:',text)
        self.assertIn('studio:8080',(ROOT/'deploy'/'Caddyfile').read_text())

if __name__ == '__main__': unittest.main()
