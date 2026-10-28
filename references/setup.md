# Provider setup and connection checks

Install the skill using the [README instructions](../README.md#install). To configure it from a terminal, clone this repository and run the commands from that checkout; the private user configuration is shared with your installed copies:

```bash
git clone https://github.com/MehradYaghoubi/jev-research-engineering.git
cd jev-research-engineering
```

Python 3.10+ is required. Use `python3` on systems where `python` is unavailable, or `py -3` on Windows. No runtime pip dependencies are needed.

### 1. Choose the API contract and provider

| Provider / model | Copy this complete profile | Protocol | Secret environment variable |
| --- | --- | --- | --- |
| GapGPT / Jev | [gapgpt.json](../examples/providers/gapgpt.json) | `systemone` | `GAPGPT_API_KEY` |
| TypeSafe / Jev direct | [config.json](../references/config.json) | `systemone` | `DECISION_API_KEY` |
| OpenRouter / Jev | [openrouter-jev.json](../examples/providers/openrouter-jev.json) | `systemone` | `OPENROUTER_API_KEY` |
| OpenRouter / another JSON-capable chat model | [openrouter-chat.json](../examples/providers/openrouter-chat.json) | `openai-chat` | `OPENROUTER_API_KEY` |
| Anthropic-compatible Messages model | [anthropic.json](../examples/providers/anthropic.json) | `anthropic` | `ANTHROPIC_API_KEY` |
| Local Ollama / installed chat model | [ollama.json](../examples/providers/ollama.json) | `openai-chat` | None for explicit loopback profile |

The provider name does not determine the wire format: `openai-chat` means Chat Completions JSON (`messages`, `response_format`, `choices`), `anthropic` means Messages (`system`, `messages`, text blocks and `x-api-key`), and `systemone` means native typed decisions (`state`, `questions`, `answers`). An OpenAI-compatible chat endpoint cannot serve a Jev System One request merely by changing the model ID. Choose a supported model and matching endpoint/contract.

### 2. Create your private configuration

Example for **GapGPT on Windows PowerShell**. If a config already exists, preserve it and use `--config` for a separate profile instead of overwriting it:

```powershell
$routerConfigDir = Join-Path $env:USERPROFILE '.config\research-engineering-router'
$routerConfigFile = Join-Path $routerConfigDir 'config.json'
New-Item -ItemType Directory -Force -Path $routerConfigDir | Out-Null
if (Test-Path -LiteralPath $routerConfigFile) { throw 'A private config already exists; preserve it or choose another --config path.' }
Copy-Item -LiteralPath '.\examples\providers\gapgpt.json' -Destination $routerConfigFile
python scripts/jev_gate.py configure
```

`configure` asks for the key without echo and stores Windows user-bound DPAPI ciphertext outside the skill. **Do not paste a real key into JSON, README, a command argument, or Git.** A provider environment variable overrides the encrypted stored key.

Example for **Linux/macOS using Bash**:

```bash
mkdir -p "$HOME/.config/research-engineering-router"
# Stop here if this file already exists; preserve an existing private configuration.
test ! -e "$HOME/.config/research-engineering-router/config.json" || exit 1
cp examples/providers/gapgpt.json "$HOME/.config/research-engineering-router/config.json"
read -r -s -p "GapGPT API key: " GAPGPT_API_KEY
export GAPGPT_API_KEY
```

That environment secret lasts for this shell/session. For cloud, CI, or another agent process, inject the same configured variable through that host's secret manager; it cannot inherit a key entered in an unrelated terminal. DPAPI setup is Windows-only; environment secrets work across platforms. Ollama's explicit unauthenticated loopback profile does not need `configure`.

To use another provider, copy its profile instead and use its credential variable. Edit `REPLACE_...` model IDs and illustrative prices before sending any request. Never reuse the GapGPT key at OpenRouter or Anthropic.

| Setting | Meaning |
| --- | --- |
| `endpoint`, `model`, `protocol` | Full endpoint URL, provider-supported model ID, and matching contract |
| `api_key_env`, `private_dir` | Secret variable name and provider-specific private credential/usage directory |
| `input_usd_per_million`, `output_usd_per_million` | Actual rates for your chosen provider/model; example chat rates are placeholders |
| `cached_input_usd_per_million`, `cache_write_input_usd_per_million` | Optional cache rates; set correctly when comparing cached requests |
| `daily_budget_usd`, `max_request_bytes`, `max_output_tokens` | Estimated shared daily budget and request/output bounds |
| `anthropic_version` | API version supported by your Anthropic-compatible provider |
| `max_attempts`, `retry_budget_seconds` | At most 3 attempts (1 disables replay), bounded retry window; every attempted request is accounted separately |

Config precedence: `--config`, `DECISION_GATE_CONFIG`, legacy `JEV_GATE_CONFIG`, private `~/.config/research-engineering-router/config.json`, then public defaults. Existing legacy configs without `api_key_env` use `JEV_API_KEY`. Updating the installed skill does not overwrite the private user config.

### 3. Verify setup, then test the connection

```bash
# Offline: selected endpoint/model/protocol and credential availability
python scripts/jev_gate.py status
# Offline: validate the request without sending it (sent=false)
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
# Live: one logical request, up to three billable attempts for transient errors
python scripts/jev_gate.py decide --request examples/manifest-decision.json
# Inspect the local estimated usage ledger
python scripts/jev_gate.py usage
```

`credential_ready: true` does not prove connectivity. A successful live test returns validated `answers`, the served model, reported `usage` and a cost basis. Missing usage is reported unknown. Do not repeatedly run a failed request without diagnosis.

For a separate config, place `--config /path/to/provider.json` **before** the command, for example `python scripts/jev_gate.py --config /path/to/provider.json status`. The context selector accepts `--config` too.

Troubleshooting: missing credentials → configure or inject the exact named variable; request rejected → check model, protocol and JSON-mode support; TLS/network error → verify the documented endpoint and connectivity; budget exhausted → inspect `usage` and continue with the lead model. Do not print keys, auth headers or raw provider errors. [Full access requirements and tested routes](../references/access.md).

### 4. Run a task

Use the invocation and task examples in [How to use it](../README.md#how-to-use-it). You can use the same skill for code work and research; no second activation or separate Jev skill is needed.

For integration into your own tooling, `prepare_context.py` accepts evidence bodies and returns selected evidence; the older `select_context.py` accepts summaries and returns source IDs. These are two helper interfaces inside the same skill. Start with `prepare_context.py` for new integrations:

```bash
python scripts/prepare_context.py --corpus examples/evidence-corpus.json --audit new-audit.json
```

This deliberately small example makes no provider call. Larger authorized corpora can make billable calls. The helper must run before primary-model intake; it cannot remove evidence already read by the primary model. Usage is stored in the separate audit file. See the [corpus contract](../references/cost-routing.md).

