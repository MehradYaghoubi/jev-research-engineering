"""Build OpenAI or lightweight Agensi ZIPs without private files or MCP wiring."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import zipfile


AGENSI_FILES = (
    'LICENSE', 'PRIVACY.md', 'agents/openai.yaml',
    'scripts/jev_gate.py', 'scripts/select_context.py', 'scripts/prepare_context.py',
    'scripts/compare_costs.py', 'references/config.json', 'references/access.md',
    'references/cost-routing.md', 'references/financial-accounting.md',
    'references/installation.md', 'references/protocol.md', 'references/setup.md',
    'references/workflow.md', 'examples/api-cost-comparison.json',
    'examples/context-manifest.json', 'examples/evidence-corpus.json',
    'examples/manifest-decision.json', 'examples/subscription-cost-comparison.json',
    'examples/providers/anthropic.json', 'examples/providers/gapgpt.json',
    'examples/providers/ollama.json', 'examples/providers/openrouter-chat.json',
    'examples/providers/openrouter-jev.json', 'benchmarks/retry-confirmation-results.md',
)


def build_agensi(source, destination):
    """Ship reviewed runtime files, not the repository's development tree."""
    source, destination = Path(source).resolve(), Path(destination).resolve()

    def read(name):
        path = source / name
        if path.is_symlink() or source not in path.resolve().parents:
            raise ValueError('Source must stay inside the package')
        return path.read_bytes()

    entries = {name: read(name) for name in AGENSI_FILES}
    skill = read('SKILL.md').decode('utf-8-sig').replace('\r\n', '\n')
    if not skill.startswith('---\n'):
        raise ValueError('A valid SKILL.md frontmatter is required')
    _, header, body = skill.split('---', 2)
    if not all(re.search(rf'(?m)^{field}:\s*\S', header) for field in ('name', 'description')):
        raise ValueError('Skill name and description are required')
    if not re.search(r'(?m)^metadata:', header):
        header += 'metadata:\n  tags: "coding, research, evidence-triage"\n'
    entries['SKILL.md'] = ('---' + header + '---' + body + '\n' +
                            read('publication/agensi-permissions.md').decode('utf-8')).encode('utf-8')
    entries['README.md'] = read('publication/agensi-readme.md')
    for name, data in list(entries.items()):
        if name.endswith('.md'):
            def link(match):
                target = match.group(2)
                if '://' in target or target.startswith(('#', 'mailto:')):
                    return match.group(0)
                path, separator, anchor = target.partition('#')
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), path))
                if resolved in entries:
                    return match.group(0)
                if resolved.startswith('../') or resolved.startswith('/'):
                    raise ValueError('Documentation link leaves the source tree')
                return '[' + match.group(1) + '](https://github.com/MehradYaghoubi/jev-research-engineering/blob/main/' + resolved + (separator + anchor if separator else '') + ')'
            entries[name] = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link,
                                   data.decode('utf-8')).encode('utf-8')
    secret_pattern = re.compile(rb'\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{25,})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    if len(entries) > 50 or any(len(data) > 1_000_000 for data in entries.values()):
        raise ValueError('Agensi package exceeds the conservative file/count limits')
    if any(secret_pattern.search(data) for data in entries.values()):
        raise ValueError('Possible credential found; inspect locally before packaging')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            archive.writestr('jev-research-engineering/' + name, data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or destination.stat().st_size > 50_000_000:
            raise ValueError('ZIP integrity or size validation failed')
    return {'archive': str(destination), 'files': len(entries),
            'largest_file_bytes': max(map(len, entries.values())),
            'zip_bytes': destination.stat().st_size,
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
            'runtime_sha256': {name: hashlib.sha256(entries[name]).hexdigest()
                               for name in AGENSI_FILES if name.startswith('scripts/')}}


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
    parser.add_argument('--target', choices=('openai', 'agensi'), default='openai')
    parser.add_argument('--source', help='Reviewed source tree; required for Agensi')
    args = parser.parse_args()
    if args.target == 'agensi' and not args.source:
        parser.error('Choose an explicit reviewed --source for Agensi packaging')
    builder = build_agensi if args.target == 'agensi' else build
    print(json.dumps(builder(args.source or Path(__file__).resolve().parents[1], args.output)))


if __name__ == '__main__':
    main()
