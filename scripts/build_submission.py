"""Build a skills-only OpenAI directory ZIP without private files or MCP wiring."""
import argparse
import json
from pathlib import Path
import zipfile


def build(source, destination):
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    manifest = json.loads((source / 'publication/openai-plugin.json').read_text(encoding='utf-8'))
    if manifest.get('name') != 'research-engineering-router' or not manifest.get('extensions', {}).get('com.openai', {}).get('requires_local_executor'):
        raise ValueError('Expected the reviewed desktop skills-only manifest')
    destination.parent.mkdir(parents=True, exist_ok=True)
    sources = [source / name for name in ('SKILL.md', 'README.md', 'LICENSE', 'PRIVACY.md')]
    for name in ('scripts', 'references', 'examples', 'agents', 'benchmarks', 'tests', 'publication'):
        sources.extend(p for p in (source / name).rglob('*') if p.is_file())
    prefix = 'skills/jev-research-engineering/'
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('plugin.json', json.dumps(manifest, indent=2) + '\n')
        for name in ('LICENSE', 'PRIVACY.md'):
            archive.write(source / name, name)
        archive.writestr('README.md', '# Research & Engineering Router\n\nDesktop skills-only plugin. Python 3.10+ is required. Read skills/jev-research-engineering/README.md for full provider setup and connection checks.\n\nNo provider credential is bundled. Configure your provider outside the package. No MCP server or lifecycle hook is included.\n')
        for path in sorted(sources):
            relative = path.relative_to(source)
            if path.is_symlink() or source not in path.resolve().parents:
                raise ValueError('Source must stay inside the package')
            if '__pycache__' in relative.parts or (path.name != 'LICENSE' and path.suffix not in ('.md', '.py', '.json', '.yaml', '.txt')) or path.name.startswith('.') or '.local.' in path.name:
                continue
            archive.write(path, prefix + relative.as_posix())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity failed')
        names = archive.namelist()
        for required in ('plugin.json', prefix + 'SKILL.md', prefix + 'scripts/jev_gate.py', prefix + 'references/config.json'):
            if required not in names:
                raise ValueError('Required package component missing')
    return {'archive': str(destination), 'files': len(names), 'skills': 1, 'mcp_servers': 0, 'credentials_bundled': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(build(Path(__file__).resolve().parents[1], args.output)))


if __name__ == '__main__':
    main()
