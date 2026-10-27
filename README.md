# Research & Engineering Router

[![skills.sh](https://skills.sh/b/MehradYaghoubi/jev-research-engineering)](https://skills.sh/MehradYaghoubi/jev-research-engineering)

A portable Agent Skills package for Codex, Claude Code, Pi, OpenCode and compatible hosts, with provider-configurable evidence triage, Clean Code/OOP, missing-integration checks, and reproducible research. Route bounded decisions to your chosen inexpensive model while your selected chat model owns reasoning, implementation, synthesis and verification.

The historical name and invocation **`$jev-research-engineering`** remain compatible. **Jev is optional:** System One, OpenAI-compatible Chat Completions, and Anthropic Messages contracts are supported. The author's personal GapGPT route is not bundled into other users' setup.

**Experimental:** context-only token reduction has been measured, but total cost savings have not. The small synthetic workload uses more input text after instruction overhead. Skip routing for small tasks; see the full [token comparison](benchmarks/token-counts.md).

## Install

```bash
# Choose your agents interactively
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g

# Or target specific agents
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g -a codex claude-code pi opencode
```

Pi-native: `pi install git:github.com/MehradYaghoubi/jev-research-engineering@v0.2.0`.

Claude marketplace: `/plugin marketplace add MehradYaghoubi/jev-research-engineering`, then `/plugin install research-engineering-router@mehrad-research-tools`.

[Full installation guide](references/installation.md) covers activation commands, VS Code extensions, manual ZIP installs, runtime requirements, compatibility limits and avoiding duplicate installs. Python 3.10+ is needed for the helpers; runtime code uses only the standard library. Existing private provider setup survives updates. No other skill is required.

## Choose a provider once

Copy one complete JSON profile to `~/.config/research-engineering-router/config.json`:

| Decision route | Profile | Notes |
| --- | --- | --- |
| GapGPT / Jev | [gapgpt.json](examples/providers/gapgpt.json) | Live tested; use your own GapGPT key |
| TypeSafe / Jev direct | [default config](references/config.json) | Published native contract |
| OpenRouter / Jev | [openrouter-jev.json](examples/providers/openrouter-jev.json) | Native `/api/v1/systemone`; use an OpenRouter key |
| OpenRouter / another chat model | [openrouter-chat.json](examples/providers/openrouter-chat.json) | Replace model and both illustrative prices; JSON mode required |
| Anthropic-compatible Messages model | [anthropic.json](examples/providers/anthropic.json) | Model, API version, key and all prices configurable |
| Local Ollama / another model | [ollama.json](examples/providers/ollama.json) | Replace with your installed model; explicit loopback HTTP |

Cloud workers and private endpoints use the same contracts. Endpoint, model, protocol, key environment variable, private storage and prices are configurable. [Access methods](references/access.md) lists requirements, official sources and which routes were actually tested. This repository supplies no Jev weights and no claim of offline Jev inference.

For authenticated Windows routes, run `python scripts/jev_gate.py configure` from the skill directory. It prompts without echo and stores DPAPI ciphertext outside the skill. For cloud/Linux/macOS, inject the exact configured credential environment variable through a secret manager. Existing configs without `api_key_env` still use `JEV_API_KEY`. Never commit credentials or reuse one provider's key at another provider.

Private config precedence is `--config`, `DECISION_GATE_CONFIG`, legacy `JEV_GATE_CONFIG`, then the private user config, then public defaults. Public updates cannot overwrite the private user config.

## Use

```bash
python scripts/jev_gate.py status
python scripts/select_context.py --manifest examples/context-manifest.json
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
python scripts/jev_gate.py decide --request examples/manifest-decision.json
python scripts/jev_gate.py usage
```

`status` and dry-run are offline. Nontrivial selection and `decide` without dry-run call the configured model and may be billable. The selector accepts compact candidate summaries and returns source IDs; read full selected bodies afterward. Preserve required evidence and inspect the strongest excluded alternative. Do not load the whole corpus into the main model first. No automatic retry, provider switching or independent supervisor.

[Wire protocol](references/protocol.md) · [Cost routing and manifests](references/cost-routing.md)

## Quality rules

- **Clean Code and meaningful OOP:** cohesive responsibilities, encapsulated invariants, composition and explicit collaborators; follow existing architecture without ceremonial classes or frameworks.
- **Missing connections:** trace required trigger-to-result behavior and check route registration, DI, events, workers, config, permissions, persistence, exports and API mappings. A graph of existing references cannot prove an unwritten edge exists. Verify through an actual entry point.
- **Research and R&D:** current primary evidence, provenance, contrary findings, explicit hypothesis, baseline, discriminating experiment, reproducibility and stopping conditions. No invented citations or benchmark outcomes.
- **Cost and privacy:** routing must replace work; count instruction/output/correction overhead, keep secrets out of requests, validate answers, retain mandatory context and visibly fall back on failure. Chat-model probabilities are uncalibrated judgments, not confidence guarantees.

## Tests and measured results

```bash
python -m unittest discover -s tests -v
python scripts/jev_gate.py self-test
# Optional tokenizer measurement; no inference calls:
python -m pip install -r benchmarks/requirements.txt
python scripts/measure_tokens.py
# Explicitly opt-in billable synthetic rerun:
python scripts/benchmark_triage.py --live --output benchmarks/new-run.json
```

[The first live run](benchmarks/first-run.md) retained all nine critical evidence items across three easy synthetic cases. [Exact tokenizer text counts](benchmarks/token-counts.md) show **1316 → 1093 tokens (16.95% fewer)** for the routed context with `o200k_base`. At the measured pre-portability revision, one **923-token** entrypoint load, gave **2016 tokens (53.19% more)** across those small cases. This is a negative net-token result, not a savings claim. Actual primary-model billing and financial savings remain unmeasured.

Protocol tests cover native request compatibility, Anthropic Messages/header/cache handling, chat JSON/usage normalization, rejected truncation/malformed responses, configured credential variables, loopback restrictions, transport accounting, and preservation of personal configuration. Selection tests cover required evidence and safe fallback. Live GapGPT succeeded; other provider profiles have documented contracts and offline tests, not live-provider certification.

## Financial interpretation

A fixed subscription does not have the same marginal billing as a metered API. Under an unchanged subscription with no paid overage, reduced context does not directly lower the subscription bill; the decision API adds its configured-rate cost. Quota/capacity effects remain unmeasured. The [financial accounting guide](references/financial-accounting.md) separates subscription and API scenarios and explains cache normalization, failed reservations and exact decimal arithmetic.

```bash
python scripts/compare_costs.py --input examples/subscription-cost-comparison.json
python scripts/compare_costs.py --input examples/api-cost-comparison.json
```

Missing API usage or prices stays unknown; the calculator never fills it with a fake zero. Provider-reported cost is distinguished from configured-rate estimates and explicit fixed-cost assumptions.

## Discovery

[Versioned downloads and releases](https://github.com/MehradYaghoubi/jev-research-engineering/releases) · [Agent installation guide](references/installation.md) · [Compatibility checks](benchmarks/agent-installation.json)

Install through the command above and share the public repository. Skills.sh discovery uses real installation telemetry; submission or an install does not guarantee a ranking. [Distribution status](references/distribution.md) records submissions separately from confirmed listings. No popularity, usage or financial-savings claims are fabricated.

## فارسی

ارائه‌دهنده و مدل تصمیم‌گیر قابل‌تغییر است: Jev از GapGPT، TypeSafe یا OpenRouter، یا مدل دیگری با API سازگار و خروجی JSON. تنظیمات شخصی خارج از پوشهٔ نصب می‌مانند. در آزمون کوچک، زمینه ۱۶٫۹۵٪ توکن کمتر داشت اما با سربار اسکیل مصرف بیشتر شد؛ صرفه‌جویی مالی هنوز اثبات نشده است. اصول Clean Code، OOP معنادار و بررسی اتصال‌های جاافتاده حفظ شده‌اند.

## License

MIT. Independent community project; not affiliated with OpenAI, TypeSafe, GapGPT, OpenRouter, Ollama or Vercel. Provider software, models and service terms are separate.
