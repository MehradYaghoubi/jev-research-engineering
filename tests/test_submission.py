import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_submission import build


class SubmissionTests(unittest.TestCase):
    def test_layout_preserves_helper_paths_and_excludes_private_artifacts(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source'
            for name in ('scripts', 'references', 'publication', 'examples', 'agents', 'benchmarks', 'tests'):
                (source / name).mkdir(parents=True, exist_ok=True)
            for name in ('SKILL.md', 'README.md', 'LICENSE', 'PRIVACY.md'):
                (source / name).write_text('test')
            (source / 'publication/openai-plugin.json').write_text(json.dumps({'name': 'research-engineering-router', 'extensions': {'com.openai': {'requires_local_executor': True}}}))
            (source / 'scripts/jev_gate.py').write_text('pass')
            (source / 'references/config.json').write_text('{}')
            for name in ('credential.dpapi', 'usage.sqlite', 'secret.local.json', '.env'):
                (source / 'references' / name).write_text('private-test-placeholder')
            output = Path(folder) / 'plugin.zip'
            build(source, output)
            with zipfile.ZipFile(output) as archive:
                self.assertIn('plugin.json', archive.namelist())
                self.assertIn('skills/jev-research-engineering/LICENSE', archive.namelist())
                self.assertIn('skills/jev-research-engineering/scripts/jev_gate.py', archive.namelist())
                self.assertFalse(any('private-test-placeholder' in archive.read(name).decode() for name in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
