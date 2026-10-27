import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import jev_gate


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.cfg = jev_gate.load_config()
        self.supplied = {'state': 'Refund requested', 'questions': {
            'refund': {'type': 'noul', 'instructions': 'Is a refund requested?'}}}

    def test_chat_request_uses_configured_model_and_json_contract(self):
        cfg = dict(self.cfg, protocol='openai-chat', model='another-model', max_output_tokens=512)
        body = json.loads(jev_gate.payload(cfg, self.supplied))
        self.assertEqual(body['model'], 'another-model')
        self.assertEqual(body['response_format'], {'type': 'json_object'})
        self.assertEqual(body['max_tokens'], 512)
        self.assertEqual(json.loads(body['messages'][1]['content']), self.supplied)

    def test_native_request_remains_unchanged(self):
        body = json.loads(jev_gate.payload(dict(self.cfg, protocol='systemone'), self.supplied))
        self.assertEqual(body, dict(self.supplied, model=self.cfg['model']))

    def test_chat_response_normalizes_usage_and_rejects_truncation(self):
        response = {'model': 'another-model-v1', 'choices': [{'finish_reason': 'stop', 'message': {
            'content': json.dumps({'answers': {'refund': {'noul': 0.95}}})}}],
            'usage': {'prompt_tokens': 80, 'completion_tokens': 12}}
        cfg = dict(self.cfg, protocol='openai-chat')
        result = jev_gate.normalize_result(cfg, response)
        self.assertEqual(result['usage'], {'input_tokens': 80, 'output_tokens': 12})
        jev_gate.validate_answers(result, self.supplied['questions'])
        response['choices'][0]['finish_reason'] = 'length'
        with self.assertRaises(ValueError):
            jev_gate.normalize_result(cfg, response)

    def test_chat_invalid_json_and_answer_ids_are_rejected(self):
        cfg = dict(self.cfg, protocol='openai-chat')
        with self.assertRaises(ValueError):
            jev_gate.normalize_result(cfg, {'choices': [{'finish_reason': 'stop', 'message': {'content': 'not JSON'}}]})
        with self.assertRaises(ValueError):
            jev_gate.validate_answers({'answers': {'other': {'noul': 0.9}}}, self.supplied['questions'])

    def test_selected_credential_variable_does_not_use_another_provider_key(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-provider-secret', 'JEV_API_KEY': 'other-provider'}, clear=True):
            self.assertEqual(jev_gate.get_key(dict(self.cfg, api_key_env='OPENROUTER_API_KEY')), 'test-provider-secret')
        self.assertIsNone(jev_gate.get_key(dict(self.cfg, auth_required=False)))

    def test_loopback_http_is_explicit_and_remote_http_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'config.json'
            cfg = dict(self.cfg, endpoint='http://127.0.0.1:11434/v1/chat/completions',
                       protocol='openai-chat', allow_http_loopback=True, auth_required=False)
            path.write_text(json.dumps(cfg))
            self.assertEqual(jev_gate.load_config(path)['protocol'], 'openai-chat')
            for endpoint, allow in [('http://example.com/v1/chat/completions', True),
                                    ('http://127.0.0.1:11434/v1/chat/completions', False)]:
                path.write_text(json.dumps(dict(cfg, endpoint=endpoint, allow_http_loopback=allow)))
                with self.assertRaises(ValueError):
                    jev_gate.load_config(path)

    def test_chat_transport_records_provider_usage_and_nonzero_output_cost(self):
        with tempfile.TemporaryDirectory() as temp:
            cfg = dict(self.cfg, protocol='openai-chat', private_dir=temp,
                       input_usd_per_million=1, output_usd_per_million=2)
            response = {'model': 'test-chat', 'choices': [{'finish_reason': 'stop', 'message': {
                'content': json.dumps({'answers': {'refund': {'noul': 0.9}}})}}],
                'usage': {'prompt_tokens': 80, 'completion_tokens': 12}}
            with patch.object(jev_gate, 'get_key', return_value='test-only'), patch.object(jev_gate.request, 'build_opener') as opener:
                opener.return_value.open.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
                result = jev_gate.decide(cfg, self.supplied)
            self.assertEqual(result['usage']['output_tokens'], 12)
            self.assertAlmostEqual(result['estimated_usd'], 0.000104)
            self.assertEqual(json.loads(opener.return_value.open.call_args.args[0].data)['messages'][1]['role'], 'user')

    def test_private_user_configuration_survives_public_skill_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'config.json'
            path.write_text(json.dumps(dict(self.cfg, model='personal-model')))
            with patch.object(jev_gate, 'DEFAULT_USER_CONFIG', path), patch.dict(os.environ, {}, clear=True):
                self.assertEqual(jev_gate.load_config()['model'], 'personal-model')


if __name__ == '__main__':
    unittest.main()
