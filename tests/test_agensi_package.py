import json
from pathlib import Path
import sys
import unittest
import zipfile

from fixture_support import fixture_directory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_submission import AGENSI_FILES, build_agensi


class AgensiPackageTests(unittest.TestCase):
    def make_source(self, folder):
        root = Path(folder) / 'source'
        for name in (*AGENSI_FILES, 'publication/agensi-permissions.md', 'publication/agensi-readme.md'):
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('public test fixture', encoding='utf-8')
        (root / 'SKILL.md').write_text('---\nname: jev-research-engineering\ndescription: Evidence triage\n---\nSee [history](benchmarks/omitted.md).\n', encoding='utf-8', newline='\n')
        return root

    def test_only_runtime_allowlist_is_shipped_and_missing_docs_link_to_source(self):
        with fixture_directory() as folder:
            root = self.make_source(folder)
            skill_path = root / 'SKILL.md'
            skill_path.write_bytes(b'\xef\xbb\xbf' + skill_path.read_bytes().replace(b'\n', b'\r\n'))
            for name in ('tests/test_mock.py', 'media/video.mp4', '.env', 'examples/private.local.json'):
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('excluded fixture', encoding='utf-8')
            output = Path(folder) / 'skill.zip'
            result = build_agensi(root, output)
            self.assertLessEqual(result['files'], 50)
            self.assertLessEqual(result['largest_file_bytes'], 1_000_000)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(len(archive.namelist()), len(AGENSI_FILES) + 2)
                skill = archive.read('jev-research-engineering/SKILL.md').decode()
                self.assertIn('metadata:', skill)
                self.assertIn('/blob/main/benchmarks/omitted.md', skill)
                self.assertTrue(all(b'excluded fixture' not in archive.read(n) for n in archive.namelist()))
            original = output.read_bytes()
            with self.assertRaises(FileExistsError):
                build_agensi(root, output)
            self.assertEqual(output.read_bytes(), original)

    def test_invalid_skill_or_oversize_file_is_rejected_before_creating_zip(self):
        with fixture_directory() as folder:
            root = self.make_source(folder)
            output = Path(folder) / 'skill.zip'
            (root / 'SKILL.md').write_text('not frontmatter')
            with self.assertRaises(ValueError):
                build_agensi(root, output)
            self.assertFalse(output.exists())
            (root / 'SKILL.md').write_text('---\nname: test\ndescription: test\n---\n', newline='\n')
            (root / AGENSI_FILES[0]).write_bytes(b'x' * 1_000_001)
            with self.assertRaises(ValueError):
                build_agensi(root, output)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
