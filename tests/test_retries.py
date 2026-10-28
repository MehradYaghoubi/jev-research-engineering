import json
from contextlib import closing
from pathlib import Path
import sqlite3
import ssl
import sys
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import jev_gate


class RetryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.cfg = dict(jev_gate.load_config(jev_gate.DEFAULT_CONFIG), private_dir=self.folder.name)
        self.request = {'state': 'test only', 'questions': {'ok': {'type': 'noul', 'instructions': 'Is this a test?'}}}
        self.response = MagicMock()
        self.response.__enter__.return_value.read.return_value = json.dumps({
            'answers': {'ok': {'noul': .9}}, 'model': 'test',
            'usage': {'input_tokens': 12, 'output_tokens': 3}}).encode()

    def invoke(self, effects, cfg=None):
        opener = MagicMock()
        opener.open.side_effect = effects
        with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener', return_value=opener), patch.object(jev_gate.time, 'sleep') as sleep:
            result = jev_gate.decide(cfg or self.cfg, self.request)
        return result, opener, sleep

    def test_timeout_then_success_keeps_unknown_usage_and_every_ledger_charge(self):
        result, opener, sleep = self.invoke([TimeoutError('private-test-detail'), self.response])
        self.assertEqual(opener.open.call_count, 2)
        self.assertEqual(sleep.call_args.args[0], 1)
        self.assertEqual(result['request_attempts'], 2)
        self.assertIsNone(result['usage']['input_tokens'])
        self.assertEqual(result['successful_usage']['input_tokens'], 12)
        self.assertNotIn('private-test-detail', json.dumps(result))
        with closing(sqlite3.connect(Path(self.folder.name) / 'usage.sqlite')) as conn:
            rows = conn.execute('SELECT status,charge FROM calls ORDER BY id').fetchall()
        self.assertEqual([x[0] for x in rows], ['failed-billing-unknown', 'ok'])
        self.assertAlmostEqual(sum(x[1] for x in rows), result['estimated_usd'])

    def test_transient_http_uses_retry_after_and_succeeds(self):
        failure = HTTPError(self.cfg['endpoint'], 529, 'private-message', {'Retry-After': '3'}, None)
        result, opener, sleep = self.invoke([failure, self.response])
        self.assertEqual(result['request_attempts'], 2)
        self.assertEqual(sleep.call_args.args[0], 3)
        self.assertEqual(result['attempts'][0]['http_status'], 529)

    def test_permanent_http_and_malformed_response_do_not_retry(self):
        for code in (400, 401, 403, 422, 501):
            opener = MagicMock()
            opener.open.side_effect = HTTPError(self.cfg['endpoint'], code, 'private-detail', {}, None)
            with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener', return_value=opener), patch.object(jev_gate.time, 'sleep') as sleep:
                with self.assertRaises(jev_gate.DecisionError) as caught:
                    jev_gate.decide(self.cfg, self.request)
            self.assertEqual(opener.open.call_count, 1)
            sleep.assert_not_called()
            self.assertNotIn('private-detail', str(caught.exception))
        self.response.__enter__.return_value.read.return_value = b'not JSON'
        with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'sleep') as sleep:
            opener.return_value.open.return_value = self.response
            with self.assertRaises(jev_gate.DecisionError):
                jev_gate.decide(self.cfg, self.request)
            self.assertEqual(opener.return_value.open.call_count, 1)
            sleep.assert_not_called()

    def test_exhaustion_is_three_attempts_with_backoff(self):
        with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'sleep') as sleep:
            opener.return_value.open.side_effect = TimeoutError('test')
            with self.assertRaises(jev_gate.DecisionError) as caught:
                jev_gate.decide(self.cfg, self.request)
            self.assertEqual(opener.return_value.open.call_count, 3)
            self.assertEqual([x.args[0] for x in sleep.call_args_list], [1, 2])
            self.assertEqual(len(caught.exception.attempts), 3)

    def test_long_retry_after_and_disabled_retry_do_not_replay(self):
        for cfg, error in [(self.cfg, HTTPError(self.cfg['endpoint'], 429, 'test', {'Retry-After': '3600'}, None)),
                           (dict(self.cfg, max_attempts=1), TimeoutError('test'))]:
            with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'sleep') as sleep:
                opener.return_value.open.side_effect = error
                with self.assertRaises(jev_gate.DecisionError):
                    jev_gate.decide(cfg, self.request)
                self.assertEqual(opener.return_value.open.call_count, 1)
                sleep.assert_not_called()

    def test_budget_can_block_retry_without_second_network_request(self):
        reserved = jev_gate.cost(self.cfg, len(jev_gate.payload(self.cfg, self.request)) + 4096, 4096)
        cfg = dict(self.cfg, daily_budget_usd=reserved * 1.5)
        with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'sleep'):
            opener.return_value.open.side_effect = TimeoutError('test')
            with self.assertRaises(jev_gate.DecisionError) as caught:
                jev_gate.decide(cfg, self.request)
            self.assertEqual(opener.return_value.open.call_count, 1)
            self.assertEqual(len(caught.exception.attempts), 1)

    def test_certificate_failures_are_not_retried(self):
        for failure in (ssl.SSLCertVerificationError('test'), URLError(ssl.SSLCertVerificationError('test'))):
            with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'sleep') as sleep:
                opener.return_value.open.side_effect = failure
                with self.assertRaises(jev_gate.DecisionError):
                    jev_gate.decide(self.cfg, self.request)
                self.assertEqual(opener.return_value.open.call_count, 1)
                sleep.assert_not_called()

    def test_http_date_retry_after_and_retry_deadline(self):
        with closing(HTTPError(self.cfg['endpoint'], 429, 'test', {'Retry-After': 'Wed, 28 Oct 2026 12:00:30 GMT'}, None)) as failure:
            with patch.object(jev_gate, 'datetime') as clock:
                clock.now.return_value = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)
                self.assertEqual(jev_gate.retry_failure(failure, 0).retry_after, 30)
        with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener, patch.object(jev_gate.time, 'monotonic', side_effect=[0, 0, 100]), patch.object(jev_gate.time, 'sleep') as sleep:
            opener.return_value.open.side_effect = TimeoutError('test')
            with self.assertRaises(jev_gate.DecisionError):
                jev_gate.decide(self.cfg, self.request)
            self.assertEqual(opener.return_value.open.call_count, 1)
            sleep.assert_not_called()

    def test_invalid_retry_config_is_rejected_offline(self):
        for key, values in [('max_attempts', [True, 0, 4, 3.0, '3']), ('retry_budget_seconds', [True, 0, 181, float('nan')])]:
            for value in values:
                with self.subTest(key=key, value=value), patch.object(Path, 'read_text', return_value=json.dumps(dict(self.cfg, **{key: value}))):
                    with self.assertRaises(ValueError):
                        jev_gate.load_config('test-config.json')

    def test_real_loopback_http_recovers_from_503_without_sending_credentials(self):
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers['Content-Length']))
                seen.append((body, self.headers.get('Authorization')))
                if len(seen) == 1:
                    self.send_response(503)
                    self.send_header('Retry-After', '0')
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'answers': {'ok': {'noul': .9}},
                                            'usage': {'input_tokens': 12, 'output_tokens': 3}}).encode())
        server = HTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            cfg = dict(self.cfg, endpoint=f'http://127.0.0.1:{server.server_port}/v1/systemone',
                       auth_required=False, allow_http_loopback=True,
                       input_usd_per_million=0, output_usd_per_million=0)
            result = jev_gate.decide(cfg, self.request)
            self.assertEqual(result['request_attempts'], 2)
            self.assertEqual(len(seen), 2)
            self.assertEqual(seen[0][0], seen[1][0])
            self.assertEqual([auth for _, auth in seen], [None, None])
            self.assertIsNone(result['usage']['input_tokens'])
            self.assertEqual(result['successful_usage']['input_tokens'], 12)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)


if __name__ == '__main__':
    unittest.main()
