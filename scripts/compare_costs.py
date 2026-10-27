"""Compare normalized usage with explicit rates; missing inputs stay unknown."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def nonnegative(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a cost or rate')
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError('Cost and rates must be finite and nonnegative')
    return number


def call_cost(call):
    if call.get('provider_reported_usd') is not None:
        return nonnegative(call['provider_reported_usd']), 'provider-reported request cost', []
    if call.get('fixed_cost_usd') is not None:
        return nonnegative(call['fixed_cost_usd']), 'explicit fixed/incremental cost assumption', []
    usage, rates = call.get('usage') or {}, call.get('rates') or {}
    missing = [k for k in ('input_tokens', 'output_tokens') if usage.get(k) is None]
    if missing:
        return None, 'unknown', missing
    counts = [usage.get(k, 0) for k in ('input_tokens', 'output_tokens', 'cache_read_input_tokens', 'cache_write_input_tokens')]
    if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in counts):
        raise ValueError('Counts must be nonnegative integers')
    total, output, read, write = counts
    if read + write > total:
        raise ValueError('Cache categories exceed total input')
    buckets = [(total - read - write, 'input_usd_per_million'),
               (output, 'output_usd_per_million'), (read, 'cached_input_usd_per_million'),
               (write, 'cache_write_input_usd_per_million')]
    missing = [key for tokens, key in buckets if tokens and rates.get(key) is None]
    if missing:
        return None, 'unknown', missing
    amount = sum((Decimal(tokens) * nonnegative(rates[key]) for tokens, key in buckets if tokens), Decimal(0)) / Decimal(1000000)
    return amount, 'configured rates times supplied usage', []


def compare(data):
    result = {}
    totals = {}
    for mode in ('baseline', 'routed'):
        calls = data.get(mode)
        if not isinstance(calls, list) or not calls:
            raise ValueError('Supply nonempty baseline and routed call lists')
        rows, subtotal, complete = [], Decimal(0), True
        for call in calls:
            amount, basis, missing = call_cost(call)
            rows.append({'label': call.get('label'), 'usd': str(amount) if amount is not None else None,
                         'basis': basis, 'usage_source': call.get('usage_source', 'unspecified'), 'missing': missing})
            complete = complete and amount is not None
            subtotal += amount if amount is not None else Decimal(0)
        extra = data.get(mode + '_other_usd')
        complete = complete and extra is not None
        if extra is not None:
            subtotal += nonnegative(extra)
        totals[mode] = subtotal if complete else None
        result[mode] = {'calls': rows, 'other_usd': extra, 'total_usd': str(subtotal) if complete else None}
    ready = all(value is not None for value in totals.values())
    saved = totals['baseline'] - totals['routed'] if ready else None
    result.update(savings_usd=str(saved) if ready else None,
                  savings_percent=str((saved / totals['baseline'] * 100).quantize(Decimal('0.01'))) if ready and totals['baseline'] else None,
                  complete=ready,
                  note='Arithmetic over supplied usage/rates; scenario counts are not billed usage. Explicit other costs are required; zero means an assumption of no difference. Currency is USD.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    try:
        result = compare(json.loads(Path(args.input).read_text(encoding='utf-8')))
        text = json.dumps(result, indent=2)
        if args.output:
            Path(args.output).write_text(text + '\n', encoding='utf-8')
        print(text)
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, InvalidOperation, OSError):
        print(json.dumps({'error': 'Invalid cost input; use nonnegative counts/rates and disjoint cache categories.'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
