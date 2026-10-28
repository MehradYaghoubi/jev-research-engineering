# Research & Engineering Router

[![skills.sh](https://skills.sh/b/MehradYaghoubi/jev-research-engineering)](https://skills.sh/MehradYaghoubi/jev-research-engineering)

A portable Agent Skills package for Codex, Claude Code, Pi, OpenCode and compatible hosts, with provider-configurable evidence triage, Clean Code/OOP, missing-integration checks, and reproducible research. Route bounded decisions to your chosen inexpensive model while your selected chat model owns reasoning, implementation, synthesis and verification.

The historical name and invocation **`$jev-research-engineering`** remain compatible. **Jev is optional:** System One, OpenAI-compatible Chat Completions, and Anthropic Messages contracts are supported. The author's personal GapGPT route is not bundled into other users' setup.

**Experimental v0.3.0:** a six-pair code-audit/research evaluation measured **10.20% fewer total primary-model tokens** with all six assisted answers passing quality checks. The **whole process took 20.42% longer** (66.45 → 80.02 seconds per task). These are limited evidence-intake results, not a guarantee for every task or agent. See the [complete measurement](benchmarks/retry-confirmation-results.md).

## Install

```bash
# Choose your agents interactively
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g

# Or target specific agents
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g -a codex claude-code pi opencode
```

Pi-native: `pi install git:github.com/MehradYaghoubi/jev-research-engineering@v0.3.1`.

Claude marketplace: `/plugin marketplace add MehradYaghoubi/jev-research-engineering`, then `/plugin install research-engineering-router@mehrad-research-tools`.

[Full installation guide](references/installation.md) covers activation commands, VS Code extensions, manual ZIP installs, runtime requirements, compatibility limits and avoiding duplicate installs. Python 3.10+ is needed for the helpers; runtime code uses only the standard library. Existing private provider setup survives updates. No other skill is required.

## Configure and connect (complete quickstart)

Install the skill as above. To configure it from a terminal, clone this repository and run the commands from that checkout; the private user configuration is shared with your installed copies:

```bash
git clone https://github.com/MehradYaghoubi/jev-research-engineering.git
cd jev-research-engineering
```

Python 3.10+ is required. Use `python3` on systems where `python` is unavailable, or `py -3` on Windows. No runtime pip dependencies are needed.

### 1. Choose the API contract and provider

| Provider / model | Copy this complete profile | Protocol | Secret environment variable |
| --- | --- | --- | --- |
| GapGPT / Jev | [gapgpt.json](examples/providers/gapgpt.json) | `systemone` | `GAPGPT_API_KEY` |
| TypeSafe / Jev direct | [config.json](references/config.json) | `systemone` | `DECISION_API_KEY` |
| OpenRouter / Jev | [openrouter-jev.json](examples/providers/openrouter-jev.json) | `systemone` | `OPENROUTER_API_KEY` |
| OpenRouter / another JSON-capable chat model | [openrouter-chat.json](examples/providers/openrouter-chat.json) | `openai-chat` | `OPENROUTER_API_KEY` |
| Anthropic-compatible Messages model | [anthropic.json](examples/providers/anthropic.json) | `anthropic` | `ANTHROPIC_API_KEY` |
| Local Ollama / installed chat model | [ollama.json](examples/providers/ollama.json) | `openai-chat` | None for explicit loopback profile |

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

Troubleshooting: missing credentials → configure or inject the exact named variable; request rejected → check model, protocol and JSON-mode support; TLS/network error → verify the documented endpoint and connectivity; budget exhausted → inspect `usage` and continue with the lead model. Do not print keys, auth headers or raw provider errors. [Full access requirements and tested routes](references/access.md).

### 4. Activate in your agent

Use the host's skills menu/name: Codex standalone `$jev-research-engineering` (plugin-aware builds may show `$research-engineering-router:jev-research-engineering`), Claude standalone `/jev-research-engineering`, Claude plugin `/research-engineering-router:jev-research-engineering`, Pi `/skill:jev-research-engineering`, or ask OpenCode to load the named skill. Start a new session if discovery has not refreshed.

Example task: “Use Research & Engineering Router. Before loading a large corpus, triage evidence with my configured provider, retain required dependencies, check missing wiring, and verify the smallest complete change. Skip routing for small tasks and report actual usage without promising savings.”

## Use

Evidence intake with atomic Jev screening (v0.3.0):

```bash
python scripts/prepare_context.py --corpus examples/evidence-corpus.json --audit new-audit.json
```

This example is deliberately small and makes no provider call. For a larger authorized corpus, the helper screens complete evidence blocks before primary-model intake, emits only delivered evidence, and keeps usage in the separate new audit file. The entrypoint is shorter and detailed workflow guidance loads progressively. This is caller-controlled preprocessing; a portable skill does not intercept every agent's input automatically. See the [corpus contract](references/cost-routing.md) and [preregistered test plan](benchmarks/adaptive-plan.md). The [18-run local pilot](benchmarks/adaptive-results.md) measured 0.832% fewer total primary tokens overall (3.58% fewer on its engineering case), but task-reader time increased 1.084% and total model tokens including the two decision calls increased 6.668%. These small authored cases do not establish general savings or speed improvement. Earlier pilot results are retained for comparison.

The newer [retry-policy replication](benchmarks/retry-confirmation-results.md) reached the registered aggregate primary-token target: **200,037 → 179,634 tokens (10.20% fewer)** with 6/6 quality checks. Whole-process mean time was **66.45 → 80.02 seconds (20.42% slower)**. This is not a financial-savings claim. This is a narrow code-audit/research evidence-intake test, not an autonomous-agent benchmark. One repetition was below 10%. The release is experimental; official directory approval is separate.

```bash
python scripts/jev_gate.py status
python scripts/select_context.py --manifest examples/context-manifest.json
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
python scripts/jev_gate.py decide --request examples/manifest-decision.json
python scripts/jev_gate.py usage
```

`status` and dry-run are offline. Nontrivial selection and `decide` without dry-run call the configured model and may be billable. The selector accepts compact candidate summaries and returns source IDs; read full selected bodies afterward. Preserve required evidence and inspect the strongest excluded alternative. Do not load the whole corpus into the main model first. Transient requests use at most three attempts with bounded backoff; no provider switching or independent supervisor.

[Wire protocol](references/protocol.md) · [Cost routing and manifests](references/cost-routing.md)

## Quality rules

- **Clean Code and meaningful OOP:** cohesive responsibilities, encapsulated invariants, composition and explicit collaborators; follow existing architecture without ceremonial classes or frameworks.
- **Missing connections:** trace required trigger-to-result behavior and check route registration, DI, events, workers, config, permissions, persistence, exports and API mappings. A graph of existing references cannot prove an unwritten edge exists. Verify through an actual entry point.
- **Research and R&D:** current primary evidence, provenance, contrary findings, explicit hypothesis, baseline, discriminating experiment, reproducibility and stopping conditions. No invented citations or benchmark outcomes.
- **Cost and privacy:** routing must replace work; count instruction/output/correction overhead, keep secrets out of requests, validate answers, retain mandatory context and visibly fall back on failure. Chat-model probabilities are uncalibrated judgments, not confidence guarantees.

## Tests and measured results

Runtime helpers and offline tests use only the Python standard library; no pip packages are required or installed. The historical tokenizer counter has been retired. For current comparisons, record actual primary-model usage from equivalent baseline and assisted runs, including cached input and output; see the [measurement guide](references/cost-routing.md).

```bash
python -m unittest discover -s tests -v
python scripts/jev_gate.py self-test
# Explicitly opt-in billable synthetic rerun:
python scripts/benchmark_triage.py --live --output benchmarks/new-run.json
```

[The first live run](benchmarks/first-run.md) retained all nine critical evidence items across three easy synthetic cases. [Exact tokenizer text counts](benchmarks/token-counts.md) show **1316 → 1093 tokens (16.95% fewer)** for the routed context with `o200k_base`. At the measured pre-portability revision, one **923-token** entrypoint load gave **2016 tokens (53.19% more)** across those small cases. This is a negative net-token result, not a savings claim. The new [real primary-agent A/B test](benchmarks/real-agent-ab.md) measured whole CLI runs: **617,245 baseline versus 877,518 routed input + output tokens (+42.17%)** across two pairs. Uncached input fell 1.82%; this is not total-token savings. All four outputs passed the same 13 acceptance cases and independent full-suite reruns. One decision call added 5,544 tokens and an estimated $0.000201684; subscription-bill savings remain unproven.

Protocol tests cover native request compatibility, Anthropic Messages/header/cache handling, chat JSON/usage normalization, rejected truncation/malformed responses, configured credential variables, loopback restrictions, transport accounting, and preservation of personal configuration. Selection tests cover required evidence and safe fallback. Live GapGPT succeeded; other provider profiles have documented contracts and offline tests, not live-provider certification.

## Financial interpretation

A fixed subscription does not have the same marginal billing as a metered API. Under an unchanged subscription with no paid overage, reduced context does not directly lower the subscription bill; the decision API adds its configured-rate cost. Quota/capacity effects remain unmeasured. The [financial accounting guide](references/financial-accounting.md) separates subscription and API scenarios and explains cache normalization, failed reservations and exact decimal arithmetic.

```bash
python scripts/compare_costs.py --input examples/subscription-cost-comparison.json
python scripts/compare_costs.py --input examples/api-cost-comparison.json
```

Missing API usage or prices stays unknown; the calculator never fills it with a fake zero. Provider-reported cost is distinguished from configured-rate estimates and explicit fixed-cost assumptions.

## Official marketplace publication

A public GitHub release or self-hosted Claude marketplace is not an approved official directory listing.

- **OpenAI public Plugins Directory:** upload the dedicated OpenAI plugin ZIP at [OpenAI Platform → Plugins](https://platform.openai.com/plugins). The publisher needs organization/project access with Apps Management Write (or owner access) and a verified publishing identity. Validate the imported package, resolve findings, submit for review, and publish only after approval. See the [official submission instructions](https://developers.openai.com/plugins/deploy/submission).
- **Anthropic Directory:** submit the GitHub plugin through [claude.ai/directory/manage](https://claude.ai/directory/manage). A paid Claude plan and the appropriate role are required. Run strict local validation, then the portal's own validation and review. `claude-plugins-official` is a separate partner-managed marketplace; its listing is not obtained by submitting a generic GitHub PR. See [official publication guidance](https://code.claude.com/docs/en/plugins/publish).
- **Pi package catalog:** publish the prepared npm package under your authenticated npm account with `pi-package` metadata; its catalog indexes npm packages. Git installation already works independently. `npm pack --dry-run` checks packaging; it is not npm publication.
- **Skills.sh:** genuine installs through its CLI drive discovery. Do not create artificial installs/stars or describe an unverified listing as approved.

[Submission packet and current blockers](references/official-submission.md) distinguishes prepared files, completed checks, submitted drafts and accepted listings. Account login/identity verification and final publisher attestations must be completed by the account owner; do not send passwords or authenticator codes in chat.

## Discovery

[Versioned downloads and releases](https://github.com/MehradYaghoubi/jev-research-engineering/releases) · [Agent installation guide](references/installation.md) · [Compatibility checks](benchmarks/agent-installation.json)

Install through the command above and share the public repository. Skills.sh discovery uses real installation telemetry; submission or an install does not guarantee a ranking. [Distribution status](references/distribution.md) records submissions separately from confirmed listings. No popularity, usage or financial-savings claims are fabricated.

## فارسی

ارائه‌دهنده و مدل تصمیم‌گیر قابل‌تغییر است: Jev از GapGPT، TypeSafe یا OpenRouter، یا مدل دیگری با API سازگار و خروجی JSON. تنظیمات شخصی خارج از پوشهٔ نصب می‌مانند. در آزمون محدود نسخهٔ ۰٫۳٫۰، مجموع توکن مدل اصلی ۱۰٫۲۰٪ کمتر و زمان کل فرایند ۲۰٫۴۲٪ بیشتر شد؛ هر شش پاسخ مسیر کمکی کنترل کیفیت را پاس کردند. این نتیجه تضمین عمومی یا اثبات صرفه‌جویی مالی نیست. راهنمای تنظیم اتصال، انتخاب پروتکل و تست آنلاین در بخش Configure and connect آمده است. اصول Clean Code، OOP معنادار و بررسی اتصال‌های جاافتاده حفظ شده‌اند.

## License

MIT. Independent community project; not affiliated with OpenAI, TypeSafe, GapGPT, OpenRouter, Ollama or Vercel. Provider software, models and service terms are separate.
