# Research & Engineering Router

[![skills.sh](https://skills.sh/b/MehradYaghoubi/jev-research-engineering)](https://skills.sh/MehradYaghoubi/jev-research-engineering)

A portable Agent Skills package for Codex, Claude Code, Pi, OpenCode and compatible hosts, with provider-configurable evidence triage, Clean Code/OOP, missing-integration checks, and reproducible research. Route bounded decisions to your chosen inexpensive model while your selected chat model owns reasoning, implementation, synthesis and verification.

[Install](#install) · [How to use it](#how-to-use-it) · [Configure a provider](#configure-and-connect-complete-quickstart) · [Results table](#measured-results) · [فارسی](#فارسی)

## One skill, several installation formats

**There is one skill: `jev-research-engineering`.** Its display title is **Research & Engineering Router**. The plugin named `research-engineering-router` packages this same skill; it is not a second workflow, model or supervisor. Jev is an optional decision model, not another skill to install.

| Name you see | What it means |
| --- | --- |
| Research & Engineering Router | Human-readable title |
| `jev-research-engineering` | Skill identifier used to install and invoke it |
| `research-engineering-router` | Plugin package containing the same skill |

Choose **one installation method per agent**. Installing both the standalone skill and its plugin can display duplicate entries. The code and research workflows belong to the same skill.

## Install

Recommended: install the standalone skill for the agents you use:

```bash
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g
```

Choose your agents in the installer, or append `-a codex` for Codex only. Python 3.10+ is required for API-assisted routing; helpers and offline tests use only the standard library. Provider configuration is private and shared across your installed copies.

Alternative formats are optional: [Pi-native package, Claude plugin and manual ZIP installation](references/installation.md). Do not install an alternative on top of the standalone skill for the same agent.

## How to use it

1. Install once and configure your provider using the next section. An existing working configuration needs no replacement.
2. Start a new agent session if the skill is not visible, then invoke the skill as shown below.
3. Give it the actual coding or research task. The primary model remains in charge. On a large evidence set it can ask the cheaper model to select relevant evidence **before** reading all of it; on a small task it skips that call.

| Agent / installation | Invoke |
| --- | --- |
| Codex, standalone | `$jev-research-engineering` |
| Claude Code, standalone | `/jev-research-engineering` |
| Claude Code, plugin alternative | `/research-engineering-router:jev-research-engineering` |
| Pi | `/skill:jev-research-engineering` |
| OpenCode / other compatible agents | Ask the agent to load the `jev-research-engineering` skill using its skill loader |

Codex example:

```text
$jev-research-engineering
Find why the refund endpoint is unreachable. Check startup registration and
callers, apply the smallest complete fix, and verify the real entry point.
Use my configured decision model only if it replaces substantial evidence reading.
```

Research example:

```text
$jev-research-engineering
Compare these API contracts using primary sources. Screen the supplied evidence
before reading it all, preserve contradictory findings, and cite decisive sources.
```

You do not need to run the helper commands manually for every task; the agent invokes them when its tools and permissions allow it. A host without file/shell access cannot perform API-assisted routing. Installing the skill alone does not connect a provider or guarantee token savings.

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

### 4. Run a task

Use the invocation and task examples in [How to use it](#how-to-use-it). You can use the same skill for code work and research; no second activation or separate Jev skill is needed.

For integration into your own tooling, `prepare_context.py` accepts evidence bodies and returns selected evidence; the older `select_context.py` accepts summaries and returns source IDs. These are two helper interfaces inside the same skill. Start with `prepare_context.py` for new integrations:

```bash
python scripts/prepare_context.py --corpus examples/evidence-corpus.json --audit new-audit.json
```

This deliberately small example makes no provider call. Larger authorized corpora can make billable calls. The helper must run before primary-model intake; it cannot remove evidence already read by the primary model. Usage is stored in the separate audit file. See the [corpus contract](references/cost-routing.md).

## Quality rules

- **Clean Code and meaningful OOP:** cohesive responsibilities, encapsulated invariants, composition and explicit collaborators; follow existing architecture without ceremonial classes or frameworks.
- **Missing connections:** trace required trigger-to-result behavior and check route registration, DI, events, workers, config, permissions, persistence, exports and API mappings. A graph of existing references cannot prove an unwritten edge exists. Verify through an actual entry point.
- **Research and R&D:** current primary evidence, provenance, contrary findings, explicit hypothesis, baseline, discriminating experiment, reproducibility and stopping conditions. No invented citations or benchmark outcomes.
- **Cost and privacy:** routing must replace work; count instruction/output/correction overhead, keep secrets out of requests, validate answers, retain mandatory context and visibly fall back on failure. Chat-model probabilities are uncalibrated judgments, not confidence guarantees.

## Measured results

**What was compared:** the primary model alone versus the same primary model with fresh Jev evidence screening. Two authored tasks—one code audit and one research task—were each repeated three times: **six matched pairs, twelve primary-model runs**. These are evidence-reading and answer checks, not autonomous implementation benchmarks.

The following results were recorded for **v0.3.0**. v0.3.1 removed an optional historical tokenizer tool; v0.3.2 clarifies documentation. Neither patch changes routing or supplies a new performance measurement.

| Metric | Primary model alone | With Jev screening | Observed change |
| --- | ---: | ---: | --- |
| Primary-model tokens, all six tasks | 200,037 | 179,634 | **10.20% fewer** |
| Primary tokens, code audit (three runs) | 100,506 | 86,480 | **13.96% fewer** |
| Primary tokens, research (three runs) | 99,531 | 93,154 | **6.41% fewer** |
| Mean whole-process time per task | 66.45 s | 80.02 s | **20.42% longer** |
| Answers passing the same quality checks | 6/6 | 6/6 | All checked answers passed |

**How to read the table:** primary tokens include input (cached input included once) plus output. Time runs from preparation through Jev calls, the primary response and quality checks. The observed trade-off is less primary-model context processing with a longer overall process. Passing these checks does not prove correctness on other tasks.

The aggregate met the 10% target narrowly. Research alone and one paired repetition were below 10%. The tasks were known from an earlier experiment, not a newly held-out test set. No universal saving, speed improvement or reduction in a fixed subscription bill is claimed. All decision calls succeeded on their first attempt in this measurement, so it does not demonstrate recovery from a real provider outage.

[Full methodology and limitations](benchmarks/retry-confirmation-results.md) · [Recorded per-run data](benchmarks/retry-confirmation-results.json) · [Plan fixed before the replication](benchmarks/retry-confirmation-plan.md)

## Software checks: different from a performance benchmark

**47 offline tests passed for v0.3.2.** They check protocol parsing, credentials/configuration boundaries, context selection, bounded retries, accounting and ZIP packaging. Two tests belonging solely to the retired tokenizer counter were removed in v0.3.1. These tests validate software behavior; they do not measure token savings.

Run from the repository or installed skill directory:

```bash
# Offline tests; -S disables third-party site-packages
python -S -m unittest discover -s tests -v
# Offline request/accounting self-check; no inference call
python -S scripts/jev_gate.py self-test
```

For a **live connection check**, use step 3 of the quickstart. It may be billable and confirms the configured route works; it does not establish savings. An optional small triage exercise is also available:

```bash
python scripts/benchmark_triage.py --live --output benchmarks/new-run.json
```

That command checks synthetic evidence selection only. It **does not rerun the twelve-run primary-model comparison** in the results table. A new savings experiment needs matched baseline/assisted tasks, the same primary-model settings and quality checks, and actual usage and whole-process timings; see the [measurement guide](references/cost-routing.md). The confirmation's complete runner/corpus artifacts remain local, so the public records support inspection rather than a one-command reproduction of that experiment.

<details>
<summary>Earlier experiments, including regressions</summary>

Earlier results are retained rather than replaced by the latest result:

| Earlier experiment | What it measured | Primary-token outcome |
| --- | --- | --- |
| [Initial full agent A/B](benchmarks/real-agent-ab.md) | Two pairs of real agent runs | **42.17% more**; an unsuccessful routing setup |
| [18-run evidence-intake pilot](benchmarks/adaptive-results.md) | Three tasks, full/lexical/assisted arms | **0.83% fewer** overall; below target |
| [First atomic confirmation](benchmarks/atomic-results.md) | Code/research evidence intake | Rejected under its original completeness gate after a provider failure |
| [Archived tokenizer experiment](benchmarks/token-counts.md) | Text encoding counts on tiny synthetic cases | Not actual primary-model usage; instruction overhead erased context-only gains |

These use different tasks and protocols and should not be averaged with the latest replication. Historical records are not current setup instructions.

</details>

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

**فقط یک اسکیل داریم:** شناسهٔ نصب و اجرا `jev-research-engineering` و نام نمایشی آن **Research & Engineering Router** است. پلاگین `research-engineering-router` بستهٔ نصب همان اسکیل است؛ اسکیل دوم یا ناظر جداگانه نیست. برای هر ایجنت فقط یکی از روش‌های نصب را انتخاب کنید. دو اسکریپت انتخاب شواهد هم ابزار داخلی همین اسکیل هستند.

پس از یک‌بار نصب و تنظیم ارائه‌دهنده، در Codex بنویسید `$jev-research-engineering` و سپس درخواست برنامه‌نویسی یا تحقیق را مطرح کنید. مدل اصلی کار را هدایت می‌کند؛ مدل ارزان‌تر فقط وقتی کمک می‌کند که بتواند بخشی از خواندن شواهد را جایگزین کند. Jev اجباری نیست و ارائه‌دهنده از بخش Configure and connect قابل تنظیم است.

| معیار در آزمون محدود نسخهٔ ۰٫۳٫۰ | مدل اصلی تنها | همراه Jev | تغییر |
| --- | ---: | ---: | --- |
| توکن مدل اصلی، مجموع شش اجرا | ۲۰۰٬۰۳۷ | ۱۷۹٬۶۳۴ | **۱۰٫۲۰٪ کاهش** |
| توکن مدل اصلی، بررسی کد | ۱۰۰٬۵۰۶ | ۸۶٬۴۸۰ | **۱۳٫۹۶٪ کاهش** |
| توکن مدل اصلی، تحقیق | ۹۹٬۵۳۱ | ۹۳٬۱۵۴ | **۶٫۴۱٪ کاهش** |
| میانگین زمان کل هر تسک | ۶۶٫۴۵ ثانیه | ۸۰٫۰۲ ثانیه | **۲۰٫۴۲٪ افزایش** |
| پاسخ‌های قبول‌شده در کنترل کیفیت | ۶ از ۶ | ۶ از ۶ | همه قبول شدند |

توکن مدل اصلی شامل ورودی با احتساب کش و خروجی است. زمان کل از آماده‌سازی تا پایان پاسخ و کنترل کیفیت محاسبه شده است. این آزمون روی دو مسئله با سه تکرار انجام شد؛ معیار ۱۰٪ در مجموع محقق شد، اما تحقیق به‌تنهایی و یک تکرار کمتر از ۱۰٪ بودند. نتیجه تضمین عمومی یا اثبات کاهش مبلغ اشتراک نیست. تست‌های آفلاین سلامت کد را می‌سنجند و آزمون کاهش مصرف توکن محسوب نمی‌شوند.

## License

MIT. Independent community project; not affiliated with OpenAI, TypeSafe, GapGPT, OpenRouter, Ollama or Vercel. Provider software, models and service terms are separate.
