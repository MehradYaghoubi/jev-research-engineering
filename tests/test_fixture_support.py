from pathlib import Path
import unittest

from fixture_support import fixture_directory


class FixtureTests(unittest.TestCase):
    def test_public_fixture_lifecycle_and_idempotent_cleanup(self):
        fixture = fixture_directory()
        with fixture as folder:
            path = Path(folder)
            (path / 'synthetic.txt').write_text('public fixture', encoding='utf-8')
            self.assertEqual((path / 'synthetic.txt').read_text(), 'public fixture')
            self.assertTrue(path.parent.is_dir())
        self.assertFalse(path.exists())
        fixture.cleanup()

    def test_windows_cleanup_rejects_parent_directory_without_deleting_it(self):
        fixture = fixture_directory()
        try:
            if not hasattr(fixture, '_path'):
                self.skipTest('Windows-specific cleanup guard')
            owned = fixture._path
            try:
                fixture._path = owned.parent
                with self.assertRaises(ValueError):
                    fixture.cleanup()
                self.assertTrue(owned.is_dir())
                self.assertTrue(owned.parent.is_dir())
            finally:
                fixture._path = owned
        finally:
            fixture.cleanup()
