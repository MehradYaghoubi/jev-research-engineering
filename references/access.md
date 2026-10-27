# Access methods

The Python helpers use the native System One JSON contract: HTTPS POST with `model`, `state`, keyed `questions`, bearer authentication, and keyed `answers`. They do not use `/chat/completions`. Credentials belong to the selected provider; a GapGPT key is not a TypeSafe or Vercel key. Only GapGPT has been tested live in this repository's first evaluation.

## 1. Run locally, call GapGPT (tested)

Use the public default endpoint `https://api.gapgpt.app/v1/systemone` and model `typesafe/jev-1.14`. On Windows run `python scripts/jev_gate.py configure` once. It prompts without echo and encrypts the key using Windows user-bound DPAPI outside the skill. `status` checks whether it can be loaded; use a live `decide` for an actual connection test. Existing users can keep their private config via `--config` or `JEV_GATE_CONFIG`.

The helper is local; inference happens at the remote provider. This is not offline Jev inference. Request-size and estimated-budget controls apply, but provider billing is authoritative.

## 2. Direct TypeSafe API (documented; not tested here)

Get your own key from the [TypeSafe console](https://console.typesafe.ai/keys). Copy `references/config.json` to a private path outside the repository, set `endpoint` to `https://api.typesafe.ai/v1/systemone`, `model` to `jev-1.14.0` (or a model returned by its model-list endpoint), and set the correct prices and private directory. The published input rate was $0.042 per million tokens and output free when these docs were checked; verify current rates before use.

```bash
export JEV_GATE_CONFIG="$HOME/.config/jev/typesafe.json"
# Inject JEV_API_KEY from your shell's secret manager, not a committed .env file.
python scripts/jev_gate.py status
python scripts/jev_gate.py decide --request examples/manifest-decision.json
```

The sample request pins no model, so the configuration supplies it. Official sources: [quickstart](https://docs.typesafe.ai/introduction/quickstart), [HTTP contract](https://docs.typesafe.ai/api/system-one), [models and prices](https://docs.typesafe.ai/models). Provider limits can exceed this helper's conservative limits; the helper supports only text, noul, choice and score, not experimental assets or box questions.

## 3. Run in cloud CI, container, or remote agent

Use the same Python scripts and a private configuration, with `JEV_API_KEY` injected as a runtime secret and `JEV_GATE_CONFIG` pointing to that config. The helper explicitly reads `JEV_API_KEY`; map a provider-specific secret into that name. Windows DPAPI ciphertext cannot be copied into a Linux container or another user's account.

Mount a persistent private directory for `usage.sqlite` if the daily estimate must survive restarts. Processes sharing that directory use the same SQLite ledger. Separate machines or ephemeral directories have separate estimates, not a globally enforced spending cap. Never run paid API calls automatically on untrusted pull requests or print secrets in CI logs. The bundled offline tests require no credentials; there is no live-test GitHub Action.

## 4. Vercel AI Gateway or another external API

Vercel documents Jev via its AI SDK decision integration and a TypeSafe-compatible API. See [the official integration](https://vercel.com/i/jev-agent-control) and [current SDK naming](https://vercel.com/i/ai-sdk-evaluation-to-decisions). These are alternative integration paths, not a claim that all gateway endpoints accept this helper's wire format.

Use this helper only with a provider's documented native System One endpoint and model ID, then run a schema/usage test with that provider's key. A Gateway `/v1/decisions` endpoint uses a different request/response contract; changing only `endpoint` is insufficient. SDK `boolean` and native `noul` are not interchangeable field names without an adapter. No gateway adapter or failover is bundled. OpenRouter and other providers may offer Jev, but availability, native route, model IDs and pricing must be verified in their current docs before configuration.

## 5. Local or private compatible server

The helpers can call an explicitly configured HTTPS System One-compatible server with a trusted TLS certificate, a nonempty bearer credential and the same answer schema. For a private CA, install trust through your runtime/OS configuration; certificate verification must remain enabled. HTTP loopback and disabled TLS verification are deliberately unsupported. A reverse proxy can expose an existing compatible local service over trusted HTTPS, but this repository does not install a server, issue certificates, or supply a decision model.

A compatible open model is an alternative backend, not proof of identical Jev quality, calibration, or cost. This repository contains no Jev weights and provides no verified offline Jev inference method. Re-evaluate the selection threshold and quality gates after changing any model/provider. For fully offline use, run the deterministic tests or direct local analysis without Jev; simulated responses are test fixtures, not inference.

## Connection and troubleshooting

```bash
python scripts/jev_gate.py self-test
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
python scripts/jev_gate.py decide --request examples/manifest-decision.json
```

The first two commands are offline. The third is a billable live call; do not repeat it automatically. Check endpoint/model, provider account access, credential readiness, TLS and network if it fails. Never display raw provider errors or authorization headers. If the route returns an unsupported envelope or usage shape, keep usage unknown rather than inventing token counts. No silent endpoint fallback occurs.
