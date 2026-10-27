"""Count exact tokenizer text units for a recorded triage run; never infer billing."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def context_text(task, candidates):
    return json.dumps({'task': task, 'evidence': {c['id']: c['body'] for c in candidates}}, ensure_ascii=False)


def measure(cases, recorded, encode, instructions):
    rows = []
    by_name = {c['name']: c for c in cases}
    for result in recorded['cases']:
        case = by_name[result['case']]
        routing = result['routing']
        selected = set(routing['selected_ids'])
        delivered = selected | set(routing.get('verify_ids', []))
        before = context_text(case['task'], case['candidates'])
        after = context_text(case['task'], [c for c in case['candidates'] if c['id'] in delivered])
        after += '\n' + json.dumps(routing, ensure_ascii=False)
        baseline, routed = len(encode(before)), len(encode(after))
        rows.append({'case': case['name'], 'baseline_text_tokens': baseline, 'routed_text_tokens': routed,
                     'saved_text_tokens': baseline - routed,
                     'reduction_percent': round(100 * (1 - routed / baseline), 2),
                     'all_critical_evidence_selected': set(case['expected_critical_ids']) <= selected})
    if not rows:
        raise ValueError('No recorded cases to measure')
    baseline = sum(c['baseline_text_tokens'] for c in rows)
    routed = sum(c['routed_text_tokens'] for c in rows)
    overhead = len(encode(instructions))
    return {'cases': rows, 'baseline_text_tokens': baseline, 'routed_text_tokens': routed,
            'context_only_reduction_percent': round(100 * (1 - routed / baseline), 2),
            'skill_entrypoint_tokens_once': overhead,
            'routed_plus_one_skill_load_tokens': routed + overhead,
            'reduction_with_one_skill_load_percent': round(100 * (1 - (routed + overhead) / baseline), 2),
            'billed_primary_model_tokens': None, 'actual_financial_savings': None,
            'limitations': ['Exact text counts for the named encoding, not a model-specific billing measurement.',
                            'Main-model tokenizer mapping is not verified for the selected chat model.',
                            'Context-only measurement includes the selected bodies, a verification candidate and routing JSON.',
                            'One skill entrypoint load is shown separately; references, chat/tool wrappers, cached-input pricing and repeated history may add overhead.',
                            'Uses recorded selections; no new inference and no independent direct-model task run.',
                            'Tiny synthetic cases do not establish workload-wide savings.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', default=str(ROOT / 'benchmarks/first-run.json'))
    parser.add_argument('--encoding', default='o200k_base')
    parser.add_argument('--output', default=str(ROOT / 'benchmarks/token-counts.json'))
    args = parser.parse_args()
    import tiktoken
    encoding = tiktoken.get_encoding(args.encoding)
    cases = json.loads((ROOT / 'tests/fixtures/triage_cases.json').read_text(encoding='utf-8'))
    recorded = json.loads(Path(args.results).read_text(encoding='utf-8'))
    report = measure(cases, recorded, lambda text: encoding.encode(text, disallowed_special=()),
                     (ROOT / 'SKILL.md').read_text(encoding='utf-8'))
    report.update(encoding=encoding.name, tokenizer_version=tiktoken.__version__,
                  measured_at_utc=datetime.now(timezone.utc).isoformat(), provider_calls=0)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
