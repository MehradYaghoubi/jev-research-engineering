"""Explicitly opt-in synthetic evidence-selection evaluation, not a billing benchmark."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

from jev_gate import load_config
from select_context import select_context

ROOT = Path(__file__).resolve().parents[1]


def context_bytes(task, candidates):
    context = {'task': task, 'evidence': {c['id']: c['body'] for c in candidates}}
    return len(json.dumps(context, ensure_ascii=False).encode('utf-8'))


def evaluate_case(cfg, case):
    manifest = {'task': case['task'], 'candidates': [
        {'id': c['id'], 'summary': c['summary']} for c in case['candidates']]}
    started = time.monotonic()
    result = select_context(cfg, manifest)
    elapsed = time.monotonic() - started
    expected = set(case['expected_critical_ids'])
    selected = set(result['selected_ids'])
    delivered = selected | set(result.get('verify_ids', []))
    baseline = context_bytes(case['task'], case['candidates'])
    routed = context_bytes(case['task'], [c for c in case['candidates'] if c['id'] in delivered])
    routed += len(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    return {'case': case['name'], 'status': result['status'],
            'passed': result['status'] == 'selected' and expected <= selected,
            'critical_recall': len(expected & selected) / len(expected),
            'missing_critical_ids': sorted(expected - selected),
            'baseline_context_bytes': baseline, 'routed_context_bytes_including_output': routed,
            'context_byte_reduction_percent': round(100 * (1 - routed / baseline), 2),
            'latency_seconds': round(elapsed, 3), 'routing': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Authorize up to three billable Jev calls')
    parser.add_argument('--config')
    parser.add_argument('--output', default=str(ROOT / 'benchmarks/first-run.json'))
    args = parser.parse_args()
    if not args.live:
        parser.error('--live is required; this command makes billable provider calls')
    cfg = load_config(args.config)
    cases = json.loads((ROOT / 'tests/fixtures/triage_cases.json').read_text(encoding='utf-8'))
    results = []
    for case in cases:
        result = evaluate_case(cfg, case)
        results.append(result)
        if result['status'] != 'selected':
            break
    complete = len(results) == len(cases)
    baseline = sum(r['baseline_context_bytes'] for r in results)
    routed = sum(r['routed_context_bytes_including_output'] for r in results)
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Three synthetic fixtures; expected IDs frozen before calls and withheld from provider',
              'passed': complete and all(r['passed'] for r in results),
              'complete': complete, 'cases': results,
              'total_jev_estimated_usd': sum(r['routing'].get('estimated_usd', 0) for r in results) if complete else None,
              'total_context_byte_reduction_percent': round(100 * (1 - routed / baseline), 2),
              'primary_model_tokens': None, 'primary_model_cost': None, 'actual_total_cost_savings': None,
              'limitations': ['Source bytes are not billed tokens.', 'No primary-model baseline or billing telemetry.',
                              'Synthetic relevance checks do not verify a real implementation or research outcome.',
                              'Prompt, search, skill-loading and correction overhead are not measured.',
                              'One run; no held-out generalization claim; failure is retained without retries.']}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
