# Choose your provider and decision model

The provider, model ID, wire protocol, credential variable, prices and private storage are configurable. Jev is optional. Your selected chat model remains the lead researcher/coder. Existing `$jev-research-engineering`, `jev_gate.py` and `JEV_GATE_CONFIG` names remain compatible.

## Available profiles

| Profile | Endpoint / protocol | Model | Credential variable | Verification |
| --- | --- | --- | --- | --- |
| [GapGPT](../examples/providers/gapgpt.json) | `https://api.gapgpt.app/v1/systemone` / `systemone` | `typesafe/jev-1.14` | `GAPGPT_API_KEY` | Live Jev calls passed |
| [TypeSafe default](config.json) | `https://api.typesafe.ai/v1/systemone` / `systemone` | `jev-1.14.0` | `DECISION_API_KEY` | Official contract; offline adapter tests |
| [OpenRouter Jev](../examples/providers/openrouter-jev.json) | `https://openrouter.ai/api/v1/systemone` / `systemone` | `typesafe/jev-1.14` | `OPENROUTER_API_KEY` | Official contract; no OpenRouter key used here |
| [OpenRouter chat model](../examples/providers/openrouter-chat.json) | `https://openrouter.ai/api/v1/chat/completions` / `openai-chat` | Your JSON-capable model | `OPENROUTER_API_KEY` | Mocked transport/response tests |
| [Anthropic Messages](../examples/providers/anthropic.json) | `https://api.anthropic.com/v1/messages` / `anthropic` | Your Messages-capable model | `ANTHROPIC_API_KEY` | Official contract; mocked transport/cache tests |
| [Local Ollama](../examples/providers/ollama.json) | `http://127.0.0.1:11434/v1/chat/completions` / `openai-chat` | Your installed JSON-capable model | None for this explicit loopback profile | Official compatibility docs; no local inference tested |

Profiles are complete JSON configs. Copy the appropriate profile to `~/.config/research-engineering-router/config.json` for one-time personal setup, outside any installed skill. Replace every `REPLACE_...` model and the illustrative chat input/output prices before calling. A native System One-compatible non-Jev model can also be selected if your provider exposes it. A chat model must actually support the request fields used below. Provider/model changes require a workload-quality check; a syntactically valid answer is not evidence of equivalent accuracy or calibration.

Config precedence: `--config`, then `DECISION_GATE_CONFIG`, then legacy `JEV_GATE_CONFIG`, then the private user config if it exists, then public `references/config.json`. Public defaults use TypeSafe, while the author's private GapGPT setup remains separate. Editing public files is unnecessary and updates cannot overwrite the private user config.

## Credentials and persistent setup

Each profile has a separate `private_dir`. On Windows run `python scripts/jev_gate.py configure` after selecting the personal config. The non-echoing prompt writes user-bound DPAPI ciphertext there. Alternatively inject the exact `api_key_env` named in the config from a secret manager. No other provider's environment variable is used as fallback. For old configs without `api_key_env`, `JEV_API_KEY` remains supported.

A GapGPT key cannot be reused at OpenRouter or TypeSafe. Do not share provider credential directories unless you intend to use the same credential. DPAPI ciphertext does not work under another user or in a Linux container. For cloud runners use a runtime environment secret and a private config; retain `usage.sqlite` in persistent private storage if its daily estimate must survive restarts. Other machines have separate ledgers, not a globally enforced quota.

```bash
python scripts/jev_gate.py status
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
python scripts/jev_gate.py decide --request examples/manifest-decision.json
```

`status` checks credential availability and selected route, not network connectivity. The dry-run validates the final wire payload without sending it. The final command is one logical request. Transient failures may cause up to three attempted calls under the bounded retry policy; every attempt can be billable, and provider failover is never automatic. See [retry accounting](protocol.md#bounded-retry-policy-local-development-revision).

## Supported contracts

**systemone** sends `{model, state, questions}` and expects `{answers, model, usage}`. Jev on GapGPT, direct TypeSafe, and OpenRouter's native System One route use this shape. Supported primitives are text-only `noul`, `choice` and `score`; no experimental images or box questions. The different OpenRouter `/api/alpha/decisions` and OpenAI-style `/v1/decisions` shapes are not this protocol.

**openai-chat** sends `model`, a system message and a JSON user message, `response_format: {type: json_object}`, and `max_tokens`. The model must return plain JSON containing an `answers` map under `choices[0].message.content` with `finish_reason: stop`. The adapter rejects truncated, malformed or wrong-ID answers. Usage maps `prompt_tokens`/`completion_tokens` to input/output. The helper does not support streaming, tools, Responses-only models, provider-specific reasoning parameters, or chat endpoints that reject JSON mode/max_tokens. Do not silently remove validation or change protocol when a model is incompatible.

JSON-mode chat outputs may imitate probabilities without meaningful calibration; use them as uncalibrated relevance judgments. Verify selected evidence and retain required IDs. Record output costs as well as input costs: another model's output is not assumed free. Missing usage stays unknown with a conservative reservation. Prices in the non-Jev chat profile are illustrative and must be replaced.

**anthropic** sends `model`, `max_tokens`, top-level `system`, and user `messages` to `/v1/messages`, using `x-api-key` and the configured `anthropic_version` header (legacy-compatible default `2023-06-01`). It does not send OpenAI's `response_format` or put a system role in messages. Only an `end_turn` plain-text JSON answer is accepted; truncated/tool/thinking outputs are not supported. Choose a version and model actually supported by your Anthropic-compatible provider. The adapter's JSON instruction is not a provider-enforced JSON schema; malformed answers are rejected without retry.

For accounting, OpenAI `prompt_tokens` includes cached input, while Anthropic `input_tokens` excludes its cache read/write counters. The adapter normalizes `usage.input_tokens` to **total input including cache** and keeps disjoint `cache_read_input_tokens` and `cache_write_input_tokens`; subtract them once to get uncached input. Configure cache prices explicitly. Mixed cache TTLs, service tiers, server tools and discounts require provider-specific rates or the provider's reported cost; they are not inferred. If an OpenRouter-style response supplies a valid `usage.cost`, that provider-reported amount takes precedence in the ledger and is identified separately. Estimates using fallback full input rates are not invoices. See [financial accounting](financial-accounting.md).

## Local, cloud and custom deployments

The same scripts run on a laptop, server, container or remote agent with Python 3.10+. Hosted inference remains remote even when the helper runs locally. This repository supplies no Jev weights or offline Jev inference. A local alternative model is a different backend, not equivalent Jev.

For a local compatible chat server, start it using its official documentation and choose an installed model in the loopback profile. Local HTTP requires explicit `allow_http_loopback: true` and a literal `127.0.0.1` or `::1` host. `auth_required: false` is allowed only on loopback. Remote HTTP is rejected; custom cloud endpoints require HTTPS and authentication. Redirects are refused and TLS verification remains enabled. A local operator may still need to restrict who can access the model server.

All runtime code uses the Python standard library. Only optional token-count measurement requires `tiktoken`. Offline unit tests use mocked responses and do not claim live provider compatibility. No paid API test runs automatically in CI or on pull requests.

## Official sources checked

- [TypeSafe System One contract](https://docs.typesafe.ai/api/system-one) and [models/pricing](https://docs.typesafe.ai/models).
- [OpenRouter System One API](https://openrouter.ai/docs/api/api-reference/systemone/submit-a-system-one-request), [TypeSafe SDK compatibility](https://openrouter.ai/docs/guides/community/typesafe-sdk), and [Chat Completions contract](https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion).
- [Anthropic Messages](https://platform.claude.com/docs/en/api/messages/create) and [prompt caching semantics](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility).

For Vercel or another gateway, select only a documented supported endpoint/contract and its own key; an advertised Jev model does not make every endpoint interchangeable. Check availability and rates again at setup time. Never print keys, headers or raw provider errors while diagnosing a rejected request.
