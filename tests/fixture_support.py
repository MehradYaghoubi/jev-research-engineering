"""Synthetic non-secret fixtures only; inherit Windows ACLs without changing them."""
import os
from pathlib import Path
import shutil
import tempfile
import uuid


class _WindowsFixtureDirectory:
    def __init__(self):
        self._root = Path(tempfile.gettempdir()).resolve()
        self._path = self._root / ('jev-tests-' + uuid.uuid4().hex)
        self._path.mkdir()
        self.name = str(self._path)

    def __enter__(self):
        return self.name

    def __exit__(self, *_):
        self.cleanup()

    def cleanup(self):
        target = self._path.resolve()
        if target != self._path or target.parent != self._root or not target.name.startswith('jev-tests-'):
            raise ValueError('Refuse cleanup outside the owned fixture directory')
        if self._path.is_symlink():
            raise ValueError('Refuse cleanup through a symlink')
        if self._path.exists():
            shutil.rmtree(target)


def fixture_directory():
    # Windows private tempfile ACLs are incompatible with the legacy restricted token.
    return _WindowsFixtureDirectory() if os.name == 'nt' else tempfile.TemporaryDirectory()
