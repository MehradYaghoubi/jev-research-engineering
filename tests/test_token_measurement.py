from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from measure_tokens import measure


class TokenMeasurementTests(unittest.TestCase):
    def test_routing_output_verification_and_instructions_are_counted(self):
        cases = [{'name': 'test', 'task': 'task', 'expected_critical_ids': ['a'], 'candidates': [
            {'id': 'a', 'body': 'selected'}, {'id': 'b', 'body': 'verify'}, {'id': 'c', 'body': 'other' * 100}]}]
        recorded = {'cases': [{'case': 'test', 'routing': {'selected_ids': ['a'], 'verify_ids': ['b']}}]}
        seen = []
        def encode(text):
            seen.append(text)
            return list(text)
        report = measure(cases, recorded, encode, 'instruction overhead')
        self.assertIn('verify', seen[1])
        self.assertIn('selected_ids', seen[1])
        self.assertNotIn('otherother', seen[1])
        self.assertEqual(report['routed_plus_one_skill_load_tokens'], report['routed_text_tokens'] + 20)
        self.assertIsNone(report['billed_primary_model_tokens'])

    def test_empty_recording_is_rejected(self):
        with self.assertRaises(ValueError):
            measure([], {'cases': []}, list, '')


if __name__ == '__main__':
    unittest.main()
