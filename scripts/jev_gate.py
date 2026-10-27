"""Small synchronous System One decision client. No automatic retries or raw-error logs."""
import argparse
import ctypes
import getpass
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone
from urllib import request, error, parse

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / 'references' / 'config.json'


def load_config(path=None):
    cfg = json.loads(Path(path or os.getenv('JEV_GATE_CONFIG') or DEFAULT_CONFIG).read_text(encoding='utf-8-sig'))
    url = parse.urlsplit(cfg['endpoint'])
    if url.scheme != 'https' or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError('Endpoint must be an HTTPS URL without embedded credentials, query or fragment')
    for key in ('daily_budget_usd', 'input_usd_per_million', 'output_usd_per_million'):
        if not finite(cfg[key], 0, 1000000):
            raise ValueError('Invalid nonnegative price or budget')
    if not isinstance(cfg['model'], str) or not cfg['model'].strip():
        raise ValueError('A model ID is required')
    if not isinstance(cfg['max_request_bytes'], int) or not 1 <= cfg['max_request_bytes'] <= 100000:
        raise ValueError('Request bound must be between 1 and 100000 bytes')
    if not finite(cfg['timeout_seconds'], 1, 120):
        raise ValueError('Invalid timeout')
    private = Path(os.path.expandvars(cfg['private_dir'])).expanduser().resolve()
    cfg['private_dir'] = str(private)
    skill = Path(__file__).resolve().parents[1]
    if private == skill or skill in private.parents:
        raise ValueError('Private data must live outside the skill')
    return cfg


def finite(value, lo, hi):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and lo <= value <= hi


def instruction_ok(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(x, str) and x.strip() for x in value)
    return isinstance(value, dict) and isinstance(value.get('question'), str) and bool(value['question'].strip())


def payload(cfg, supplied):
    if not isinstance(supplied, dict) or set(supplied) - {'state', 'questions', 'model'}:
        raise ValueError('Supply only state, questions and optional matching model')
    if supplied.get('model', cfg['model']) != cfg['model']:
        raise ValueError('Request model does not match persistent configuration')
    if 'state' not in supplied or not isinstance(supplied['state'], (str, dict, list)):
        raise ValueError('Missing or invalid state')
    questions = supplied.get('questions')
    if not isinstance(questions, dict) or not 1 <= len(questions) <= 64:
        raise ValueError('Supply between 1 and 64 named questions')
    for name, question in questions.items():
        if not isinstance(name, str) or not name or not isinstance(question, dict):
            raise ValueError('Invalid question')
        kind = question.get('type')
        criteria = question.get('criteria')
        if not instruction_ok(question.get('instructions')):
            raise ValueError('Invalid question instructions')
        if kind == 'choice':
            if not isinstance(criteria, dict) or len(criteria) < 2 or not all(isinstance(x, str) and x for x in criteria.values()):
                raise ValueError('Choice needs at least two described options')
        elif kind == 'score':
            if not isinstance(criteria, list) or not 2 <= len(criteria) <= 10 or not all(isinstance(x, str) and x for x in criteria):
                raise ValueError('Score needs 2 to 10 ordered descriptions')
        elif kind != 'noul':
            raise ValueError('Unsupported question type')
    body = json.dumps({**supplied, 'model': cfg['model']}, ensure_ascii=False, allow_nan=False).encode('utf-8')
    if len(body) > cfg['max_request_bytes']:
        raise ValueError('Request exceeds configured byte limit; reduce context or split questions')
    return body


def validate_answers(data, questions):
    answers = data.get('answers') if isinstance(data, dict) else None
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise ValueError('Provider returned missing or unexpected answer IDs')
    for name, question in questions.items():
        answer = answers[name]
        kind = question['type']
        if not isinstance(answer, dict) or answer.get('type', kind) != kind:
            raise ValueError('Provider answer type mismatch')
        if kind == 'noul' and not finite(answer.get('noul'), 0, 1):
            raise ValueError('Invalid true/false probability')
        if kind == 'choice' and answer.get('choice') not in question['criteria']:
            raise ValueError('Provider chose an unknown option')
        if kind == 'score' and not finite(answer.get('score'), 0, len(question['criteria']) - 1):
            raise ValueError('Provider score outside rubric')
        if 'confidence' in answer and not finite(answer['confidence'], 0, 1):
            raise ValueError('Invalid provider confidence')
        probabilities = answer.get('probabilities')
        if probabilities is not None:
            expected = set(question['criteria']) if kind == 'choice' else {str(i) for i in range(len(question.get('criteria', [])))}
            if not isinstance(probabilities, dict) or (kind != 'noul' and set(probabilities) != expected):
                raise ValueError('Invalid probability option IDs')
            if not probabilities or not all(finite(x, 0, 1) for x in probabilities.values()) or abs(sum(probabilities.values()) - 1) > 0.02:
                raise ValueError('Invalid probability distribution')
    return answers


def cost(cfg, input_tokens, output_tokens=0):
    return (input_tokens * cfg['input_usd_per_million'] + output_tokens * cfg['output_usd_per_million']) / 1000000


def ledger(cfg, memory=False):
    private = Path(cfg['private_dir'])
    private.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(':memory:' if memory else private / 'usage.sqlite', timeout=10, isolation_level=None)
    conn.execute('CREATE TABLE IF NOT EXISTS calls (id INTEGER PRIMARY KEY, day TEXT, fingerprint TEXT, status TEXT, input_tokens INTEGER, output_tokens INTEGER, charge REAL)')
    return conn


def reserve(conn, cfg, body):
    # UTF-8 bytes plus provider overhead is deliberately conservative, not a tokenizer.
    estimated = cost(cfg, len(body) + 4096, 4096)
    day = datetime.now(timezone.utc).date().isoformat()
    conn.execute('BEGIN IMMEDIATE')
    try:
        used = conn.execute('SELECT COALESCE(SUM(charge),0) FROM calls WHERE day=?', (day,)).fetchone()[0]
        if used + estimated > cfg['daily_budget_usd']:
            raise ValueError('Daily UTC budget exhausted; continue with the current chat model')
        row = conn.execute('INSERT INTO calls(day,fingerprint,status,charge) VALUES(?,?,?,?)', (day, hashlib.sha256(body).hexdigest(), 'reserved', estimated))
        conn.execute('COMMIT')
        return row.lastrowid, estimated
    except Exception:
        conn.execute('ROLLBACK')
        raise


def dpapi(data, protect):
    if os.name != 'nt':
        raise ValueError('Use JEV_API_KEY on this platform; encrypted local setup requires Windows')
    from ctypes import wintypes
    class Blob(ctypes.Structure):
        _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_ubyte))]
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    result = Blob()
    api = ctypes.windll.crypt32.CryptProtectData if protect else ctypes.windll.crypt32.CryptUnprotectData
    if not api(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(result)):
        raise ValueError('Local credential encryption/decryption failed')
    try:
        return ctypes.string_at(result.data, result.size)
    finally:
        ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        ctypes.windll.kernel32.LocalFree(ctypes.cast(result.data, ctypes.c_void_p))


def get_key(cfg):
    key = os.getenv('JEV_API_KEY')
    if not key:
        file = Path(cfg['private_dir']) / 'credential.dpapi'
        if not file.exists():
            raise ValueError('Credential missing; run configure once')
        key = dpapi(file.read_bytes(), False).decode('utf-8')
    if not key.strip() or '\r' in key or '\n' in key:
        raise ValueError('Invalid credential')
    return key.strip()


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def decide(cfg, supplied, dry_run=False):
    body = payload(cfg, supplied)
    if dry_run:
        return {'mode': 'dry-run', 'bytes': len(body), 'input_reservation_usd': cost(cfg, len(body) + 4096, 4096), 'sent': False}
    key = get_key(cfg)
    conn = ledger(cfg)
    try:
        call_id, reserved = reserve(conn, cfg, body)
        try:
            req = request.Request(cfg['endpoint'], body, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
            with request.build_opener(NoRedirect()).open(req, timeout=cfg['timeout_seconds']) as response:
                raw = response.read(1048577)
            if len(raw) > 1048576:
                raise ValueError('Provider response too large')
            result = json.loads(raw, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))
            answers = validate_answers(result, supplied['questions'])
            usage = result.get('usage') or {}
            it, ot = usage.get('input_tokens'), usage.get('output_tokens', 0)
            valid_usage = isinstance(it, int) and not isinstance(it, bool) and it >= 0 and isinstance(ot, int) and not isinstance(ot, bool) and ot >= 0
            charge = cost(cfg, it, ot) if valid_usage else reserved
            conn.execute('UPDATE calls SET status=?,input_tokens=?,output_tokens=?,charge=? WHERE id=?', ('ok' if valid_usage else 'usage-unknown', it if valid_usage else None, ot if valid_usage else None, charge, call_id))
            return {'answers': answers, 'model': result.get('model', cfg['model']), 'usage': {'input_tokens': it if valid_usage else None, 'output_tokens': ot if valid_usage else None}, 'estimated_usd': charge, 'cost_basis': 'reported tokens' if valid_usage else 'conservative reservation; usage unknown'}
        except Exception as exc:
            conn.execute('UPDATE calls SET status=? WHERE id=?', ('failed-billing-unknown', call_id))
            if isinstance(exc, error.HTTPError):
                raise ValueError('Provider HTTP status ' + str(exc.code) + '; no retry; reservation retained') from None
            raise ValueError('Provider call or validation failed; no retry; reservation retained') from None
    finally:
        conn.close()


def self_test(cfg):
    import contextlib
    import io
    from unittest.mock import patch
    example = {'state': {'text': 'Duplicate payment refund'}, 'questions': {'refund': {'type': 'noul', 'instructions': {'question': 'Refund requested?'}}, 'team': {'type': 'choice', 'instructions': ['Which team?'], 'criteria': {'billing': 'Payments', 'technical': 'Errors'}}, 'urgency': {'type': 'score', 'instructions': 'Urgency?', 'criteria': ['Routine', 'Urgent', 'Emergency']}}}
    assert payload(cfg, example)
    valid = {'answers': {'refund': {'noul': 0.9}, 'team': {'choice': 'billing'}, 'urgency': {'score': 1.2}}}
    validate_answers(valid, example['questions'])
    for malformed in ({'answers': {}}, {'answers': {**valid['answers'], 'refund': {'noul': float('nan')}}}, {'answers': {**valid['answers'], 'team': {'choice': 'other'}}}, {'answers': {**valid['answers'], 'urgency': {'score': 3}}}):
        try:
            validate_answers(malformed, example['questions'])
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed answer accepted')
    try:
        payload({**cfg, 'max_request_bytes': 1}, example)
    except ValueError:
        pass
    else:
        raise AssertionError('Oversize request accepted')
    pricing = {**cfg, 'input_usd_per_million': 0.042, 'output_usd_per_million': 0}
    assert math.isclose(cost(pricing, 10000), 0.00042)
    assert math.isclose(cost(pricing, 300000), 0.0126)
    local = {**cfg, 'daily_budget_usd': 0.00000001}
    conn = ledger(local, memory=True)
    try:
        try:
            reserve(conn, local, b'test')
        except ValueError:
            pass
        else:
            raise AssertionError('Budget not enforced')
        assert conn.execute('SELECT COUNT(*) FROM calls').fetchone()[0] == 0
        reserve(conn, {**cfg, 'daily_budget_usd': 1}, b'test')
        assert conn.execute('SELECT COUNT(*) FROM calls').fetchone()[0] == 1
    finally:
        conn.close()
    if os.name == 'nt':
        assert dpapi(dpapi(b'test-placeholder-only', True), False) == b'test-placeholder-only'
    with patch.object(sys, 'argv', ['jev_gate.py', 'usage']), patch(__name__ + '.ledger', side_effect=sqlite3.OperationalError('database is locked')), contextlib.redirect_stderr(io.StringIO()) as captured:
        assert main() == 1
        assert json.loads(captured.getvalue()).get('error')
        assert 'Traceback' not in captured.getvalue()
    return {'self_test': 'passed', 'provider_calls': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument('command', choices=['configure', 'status', 'usage', 'self-test', 'decide'])
    parser.add_argument('--request')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--key-stdin', action='store_true', help='Configure from a secure non-echoing automation pipe')
    args = parser.parse_args()
    try:
        cfg = load_config(args.config)
        if args.command == 'configure':
            secret = sys.stdin.read().strip() if args.key_stdin else getpass.getpass('Decision provider API key: ').strip()
            if not secret or '\r' in secret or '\n' in secret:
                raise ValueError('Invalid credential')
            file = Path(cfg['private_dir']) / 'credential.dpapi'
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(dpapi(secret.encode('utf-8'), True))
            result = {'configured': True, 'storage': 'Windows user-bound DPAPI; outside skill'}
        elif args.command == 'status':
            try:
                get_key(cfg)
                ready = True
            except (ValueError, OSError):
                ready = False
            result = {'credential_ready': ready, 'endpoint': cfg['endpoint'], 'model': cfg['model'], 'daily_budget_usd': cfg['daily_budget_usd'], 'main_model': 'current chat selection'}
        elif args.command == 'self-test':
            result = self_test(cfg)
        elif args.command == 'usage':
            conn = ledger(cfg)
            try:
                result = {'days': conn.execute('SELECT day,COUNT(*),SUM(input_tokens),SUM(charge) FROM calls GROUP BY day').fetchall(), 'columns': ['UTC day', 'attempted calls', 'reported input tokens (nullable)', 'estimated USD incl unknown reservations']}
            finally:
                conn.close()
        else:
            if not args.request:
                raise ValueError('--request is required')
            result = decide(cfg, json.loads(Path(args.request).read_text(encoding='utf-8-sig')), args.dry_run)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (ValueError, KeyError, OSError, TypeError, sqlite3.Error):
        # Do not print exceptions which may include remote payloads or secrets.
        print(json.dumps({'error': 'Operation failed: check configuration, input, credential or connectivity. No automatic retry; main model fallback required.'}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
