import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import jev_gate
import select_context
import benchmark_triage


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = jev_gate.load_config()
        self.manifest = {'task': 'Wire the refund route into startup', 'candidates': [
            {'id': 'startup', 'summary': 'Application startup and router registration', 'required': True},
            {'id': 'refund', 'summary': 'Refund route implementation'},
            {'id': 'theme', 'summary': 'Site colors'},
        ]}

    def answer(self, scores):
        return {'answers': {key: {'noul': value} for key, value in scores.items()},
                'model': 'test', 'usage': {'input_tokens': 10, 'output_tokens': 2},
                'estimated_usd': 0.000001, 'cost_basis': 'test fixture'}

    def test_required_candidate_survives_bad_rank_and_borderline_is_checked(self):
        with patch.object(select_context, 'decide', return_value=self.answer({'startup': 0, 'refund': 0.9, 'theme': 0.1})) as call:
            result = select_context.select_context(self.cfg, self.manifest)
        self.assertEqual(result['selected_ids'], ['startup', 'refund'])
        self.assertEqual(result['verify_ids'], ['theme'])
        self.assertEqual(call.call_count, 1)

    def test_provider_failure_keeps_every_candidate(self):
        with patch.object(select_context, 'decide', side_effect=ValueError('fixture')):
            result = select_context.select_context(self.cfg, self.manifest)
        self.assertEqual(result['status'], 'fallback')
        self.assertEqual(result['selected_ids'], ['startup', 'refund', 'theme'])

    def test_all_low_scores_keep_context(self):
        for candidate in self.manifest['candidates']:
            candidate.pop('required', None)
        with patch.object(select_context, 'decide', return_value=self.answer(dict.fromkeys(['startup', 'refund', 'theme'], 0))):
            result = select_context.select_context(self.cfg, self.manifest)
        self.assertEqual(len(result['selected_ids']), 3)

    def test_duplicate_ids_rejected_before_network(self):
        self.manifest['candidates'][1]['id'] = 'startup'
        with patch.object(select_context, 'decide') as call, self.assertRaises(ValueError):
            select_context.select_context(self.cfg, self.manifest)
        call.assert_not_called()

    def test_single_candidate_needs_no_api(self):
        self.manifest['candidates'] = self.manifest['candidates'][:1]
        with patch.object(select_context, 'decide') as call:
            result = select_context.select_context(self.cfg, self.manifest)
        self.assertEqual(result['provider_calls'], 0)
        call.assert_not_called()

    def test_benchmark_counts_verification_and_routing_overhead(self):
        case = {'name': 'test', 'task': 'test', 'expected_critical_ids': ['a'], 'candidates': [
            {'id': 'a', 'summary': 'Relevant', 'body': 'A' * 100},
            {'id': 'b', 'summary': 'Alternative', 'body': 'B' * 100},
            {'id': 'c', 'summary': 'Irrelevant', 'body': 'C' * 1000}]}
        routing = {'status': 'selected', 'selected_ids': ['a'], 'verify_ids': ['b']}
        with patch.object(benchmark_triage, 'select_context', return_value=routing) as call:
            result = benchmark_triage.evaluate_case(self.cfg, case)
        self.assertTrue(result['passed'])
        expected_bytes = benchmark_triage.context_bytes('test', case['candidates'][:2]) + len(json.dumps(routing).encode())
        self.assertEqual(result['routed_context_bytes_including_output'], expected_bytes)
        self.assertNotIn('expected_critical_ids', call.call_args.args[1])
        self.assertNotIn('body', call.call_args.args[1]['candidates'][0])

    def test_benchmark_does_not_count_a_missed_critical_source_as_success(self):
        case = {'name': 'test', 'task': 'test', 'expected_critical_ids': ['a'], 'candidates': [
            {'id': 'a', 'summary': 'Critical', 'body': 'Needed'},
            {'id': 'b', 'summary': 'Other', 'body': 'Other'}]}
        with patch.object(benchmark_triage, 'select_context', return_value={
                'status': 'selected', 'selected_ids': ['b'], 'verify_ids': ['a']}):
            result = benchmark_triage.evaluate_case(self.cfg, case)
        self.assertFalse(result['passed'])
        self.assertEqual(result['missing_critical_ids'], ['a'])

    def test_home_expansion_and_private_directory_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'config.json'
            cfg = dict(self.cfg, private_dir='~/.jev-test')
            path.write_text(json.dumps(cfg))
            self.assertEqual(jev_gate.load_config(path)['private_dir'], str((Path.home() / '.jev-test').resolve()))
            cfg['private_dir'] = str(Path(jev_gate.__file__).resolve().parents[1] / 'private')
            path.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):
                jev_gate.load_config(path)


if __name__ == '__main__':
    unittest.main()
