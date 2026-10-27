from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from compare_costs import call_cost, compare


class CostTests(unittest.TestCase):
    def test_cache_buckets_are_not_double_counted(self):
        call = {'usage': {'input_tokens': 100, 'output_tokens': 5, 'cache_read_input_tokens': 80},
                'rates': {'input_usd_per_million': '2', 'output_usd_per_million': '8', 'cached_input_usd_per_million': '0.2'}}
        self.assertEqual(call_cost(call)[0], Decimal('0.000096'))

    def test_unknown_is_not_zero_and_extra_cost_is_required(self):
        known = {'provider_reported_usd': '0.01'}
        result = compare({'baseline': [known], 'routed': [{'usage': None}], 'baseline_other_usd': 0, 'routed_other_usd': 0})
        self.assertFalse(result['complete'])
        self.assertIsNone(result['savings_usd'])
        self.assertFalse(compare({'baseline': [known], 'routed': [known]})['complete'])

    def test_provider_cost_overrides_estimate_and_loss_is_negative(self):
        result = compare({'baseline': [{'provider_reported_usd': '0.01'}],
                          'routed': [{'provider_reported_usd': '0.02'}],
                          'baseline_other_usd': 0, 'routed_other_usd': 0})
        self.assertEqual(result['savings_usd'], '-0.01')
        self.assertEqual(result['savings_percent'], '-100.00')

    def test_flat_subscription_has_no_fabricated_per_token_saving(self):
        result = compare({'baseline': [{'fixed_cost_usd': '0'}],
                          'routed': [{'fixed_cost_usd': '0'}, {'fixed_cost_usd': '0.0001'}],
                          'baseline_other_usd': 0, 'routed_other_usd': 0})
        self.assertEqual(result['savings_usd'], '-0.0001')
        self.assertIsNone(result['savings_percent'])


if __name__ == '__main__':
    unittest.main()
