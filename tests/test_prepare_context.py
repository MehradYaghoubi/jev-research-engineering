import json
from pathlib import Path
import sys
import tempfile
import unittest
import contextlib
import io
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import jev_gate
import prepare_context
import select_context


class PrepareContextTests(unittest.TestCase):
    def setUp(self):
        self.cfg = jev_gate.load_config(jev_gate.DEFAULT_CONFIG)
        self.corpus = {'task': 'Find relevant evidence', 'candidates': [
            {'id': name, 'body': name + ' evidence ' * 600} for name in ('a', 'b', 'c', 'd')]}

    def test_small_task_and_all_required_skip_provider(self):
        for corpus in ({'task': 'Small', 'candidates': [{'id': 'a', 'body': 'small'}]},
                       dict(self.corpus, candidates=[dict(c, required=True) for c in self.corpus['candidates']])):
            with patch.object(prepare_context, 'decide') as call:
                packet, audit = prepare_context.prepare_context(self.cfg, corpus)
            call.assert_not_called()
            self.assertEqual(audit['provider_calls'], 0)
            self.assertGreaterEqual(audit['elapsed_seconds'], 0)
            self.assertEqual(json.loads(packet)['evidence'], [{'id': c['id'], 'body': c['body']} for c in corpus['candidates']])

    def test_full_evidence_screening_preserves_required_and_verification(self):
        self.corpus['candidates'][0]['required'] = True
        response = {'answers': {f'source_{i}_part_0': {'choice': p} for i, p in enumerate(('irrelevant', 'direct', 'background', 'irrelevant'))},
                    'model': 'test', 'usage': {'input_tokens': 100, 'output_tokens': 10},
                    'estimated_usd': .001, 'cost_basis': 'test'}
        with patch.object(prepare_context, 'decide', return_value=response) as call:
            packet, audit = prepare_context.prepare_context(self.cfg, self.corpus)
        self.assertEqual(call.call_count, 1)
        self.assertTrue(call.call_args.args[1]['questions']['source_1_part_0']['instructions']['evidence'].endswith(self.corpus['candidates'][1]['body']))
        self.assertEqual(set(call.call_args.args[1]['state']), {'task'})
        self.assertNotIn(self.corpus['candidates'][2]['body'], call.call_args.args[1]['questions']['source_1_part_0']['instructions']['evidence'])
        self.assertEqual([c['id'] for c in json.loads(packet)['evidence']], ['a', 'b', 'c'])
        self.assertNotIn('estimated_usd', packet)
        self.assertLess(audit['delivered_bytes'], audit['baseline_bytes'])

    def test_failed_or_oversize_route_retains_evidence(self):
        for cfg in (self.cfg, dict(self.cfg, max_request_bytes=1)):
            with patch.object(prepare_context, 'decide', side_effect=OSError('offline')) as call:
                packet, audit = prepare_context.prepare_context(cfg, self.corpus)
            self.assertEqual(len(json.loads(packet)['evidence']), 4)
            self.assertEqual(audit['delivered_bytes'], audit['baseline_bytes'])
            if cfg['max_request_bytes'] == 1:
                call.assert_not_called()

    def test_unhelpful_selection_does_not_expand_packet(self):
        response = {'answers': {f'source_{i}_part_0': {'choice': 'direct'} for i in range(4)},
                    'model': 'test', 'usage': {'input_tokens': 100, 'output_tokens': 10},
                    'estimated_usd': .001, 'cost_basis': 'test'}
        with patch.object(prepare_context, 'decide', return_value=response):
            packet, audit = prepare_context.prepare_context(self.cfg, self.corpus)
        self.assertEqual(audit['status'], 'no_reduction')
        self.assertEqual(packet, prepare_context.render(self.corpus['task'], self.corpus['candidates']))

    def test_invalid_corpus_rejected_before_provider(self):
        cases = [dict(self.corpus, task=''), dict(self.corpus, secret='forbidden'),
                 dict(self.corpus, candidates=[{'id': 'a', 'body': ''}]),
                 dict(self.corpus, candidates=[{'id': 'a', 'body': 'ok', 'required': 1}]),
                 dict(self.corpus, candidates=[{'id': 'a', 'body': 'ok'}] * 4)]
        with patch.object(prepare_context, 'decide') as call:
            for corpus in cases:
                with self.subTest(corpus=corpus), self.assertRaises(ValueError):
                    prepare_context.prepare_context(self.cfg, corpus)
        call.assert_not_called()

    def test_cli_preserves_existing_audit_without_calling_provider(self):
        with tempfile.TemporaryDirectory() as folder:
            audit = Path(folder) / 'audit.json'
            audit.write_text('preserve')
            args = ['prepare_context.py', '--corpus', 'unused.json', '--audit', str(audit)]
            with patch.object(sys, 'argv', args), patch.object(prepare_context, 'prepare_context') as call, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(prepare_context.main(), 1)
            call.assert_not_called()
            self.assertEqual(audit.read_text(), 'preserve')

    def test_line_blocks_cover_source_and_selected_spans_have_provenance(self):
        candidate = {'id': 'module', 'body': ''.join(f'line {i}: exact source content\n' for i in range(140))}
        blocks = prepare_context.evidence_blocks([candidate])
        self.assertGreater(len(blocks), 1)
        covered = set().union(*(set(range(b['start'], b['end'])) for b in blocks))
        self.assertEqual(covered, set(range(140)))
        chosen = blocks[1]
        result = prepare_context.selected_evidence([candidate], blocks, {chosen['id']})
        self.assertEqual(result[0]['id'], 'module')
        self.assertIn(f"[module: lines {chosen['start'] + 1}-{chosen['end']}]", result[0]['body'])
        self.assertIn(f"line {chosen['start']}: exact source content", result[0]['body'])
        required = dict(candidate, required=True)
        self.assertEqual(prepare_context.selected_evidence([required], blocks, {chosen['id']}), [required])

    def test_excessive_block_count_falls_back_without_discarding_sources(self):
        candidates = [{'id': f'item_{i}', 'body': ('evidence line\n' * 300)} for i in range(64)]
        blocks = prepare_context.evidence_blocks(candidates)
        self.assertEqual(len(blocks), 64)
        self.assertEqual([b['summary'] for b in blocks], [c['body'] for c in candidates])

    def test_batch_limit_is_checked_before_any_call(self):
        with patch.object(prepare_context, 'decide') as call:
            packet, audit = prepare_context.prepare_context(dict(self.cfg, max_request_bytes=9000), self.corpus)
        self.assertEqual(audit['status'], 'skipped_request_bound')
        self.assertEqual(audit['provider_calls'], 0)
        call.assert_not_called()
        self.assertEqual(packet, prepare_context.render(self.corpus['task'], self.corpus['candidates']))

    def test_partial_batch_failure_retains_every_source_without_retry(self):
        self.corpus['candidates'][0]['required'] = True
        def response(cfg, request):
            if call.call_count == 2:
                raise OSError('offline')
            return {'answers': {name: {'choice': 'direct'} for name in request['questions']},
                    'model': 'test', 'usage': {'input_tokens': 100, 'output_tokens': 10},
                    'estimated_usd': .001, 'cost_basis': 'test'}
        with patch.object(prepare_context, 'decide', side_effect=response) as call:
            packet, audit = prepare_context.prepare_context(dict(self.cfg, max_request_bytes=9000), self.corpus)
        self.assertEqual(call.call_count, 2)
        self.assertEqual(audit['status'], 'fallback')
        self.assertIsNone(audit['provider_calls'])
        self.assertEqual(packet, prepare_context.render(self.corpus['task'], self.corpus['candidates']))

    def test_batch_retries_share_the_task_attempt_limit(self):
        self.corpus['candidates'][0]['required'] = True
        bounds = []
        def response(cfg, request):
            bounds.append(cfg['max_attempts'])
            return {'answers': {name: {'choice': 'direct'} for name in request['questions']},
                    'model': 'test', 'usage': {'input_tokens': 100, 'output_tokens': 10},
                    'estimated_usd': .001, 'cost_basis': 'test', 'request_attempts': cfg['max_attempts']}
        with patch.object(prepare_context, 'decide', side_effect=response):
            _, audit = prepare_context.prepare_context(dict(self.cfg, max_request_bytes=9000), self.corpus)
        self.assertEqual(bounds, [3, 2, 1])
        self.assertEqual(audit['provider_calls'], 3)
        self.assertEqual(audit['request_attempts'], 6)


if __name__ == '__main__':
    unittest.main()
