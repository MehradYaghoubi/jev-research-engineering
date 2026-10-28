# Research & Engineering Router

[![skills.sh](https://skills.sh/b/MehradYaghoubi/jev-research-engineering)](https://skills.sh/MehradYaghoubi/jev-research-engineering)

A free, open-source skill that helps your coding agent read less irrelevant material before solving a coding or research task.

Your main model stays in charge. When there is a large set of files or research sources, a cheaper model can first select the relevant evidence. The main model then checks that evidence and does the work. Small tasks skip the extra call.

**Free to install and use under MIT.** Your chosen model provider may charge for API calls; local model hosting has its own requirements.

If this helps your work, thank you for trying it. **[Give the project a GitHub star](https://github.com/MehradYaghoubi/jev-research-engineering)** if you find it useful, or share it with someone who could use it. Stars are optional; feedback and reproducible bug reports are welcome too.

[Watch setup video](#watch-the-installation-guide) · [Install](#install) · [How to use it](#how-to-use-it) · [Configure a provider](#configure-and-connect-complete-quickstart) · [Results table](#measured-results) · [فارسی](#فارسی)

## Watch the installation guide

https://github.com/user-attachments/assets/9155c730-eed7-4c1a-8668-9ed964611643

**3 min 31 sec · 1080p · English narration and visible captions.** Follow a Windows PowerShell project installation for Codex, choose a provider, keep credentials private, check the route, and see a real connection result. Commands appear gradually with reading pauses. Actual installer/provider excerpts are labelled separately from setup instructions and the example agent prompt. This is an authored walkthrough, not an unedited desktop recording or a new savings benchmark.

[Watch / download MP4](https://github.com/user-attachments/assets/9155c730-eed7-4c1a-8668-9ed964611643) · [Chapter guide and transcript](references/video-guide.md) · [English subtitle file](media/installation-walkthrough.en.srt)

## What it helps with

| Your task | How the skill helps |
| --- | --- |
| Understand a large codebase | Select relevant evidence before the main model reads it all |
| Fix a feature that looks complete but does not work | Check missing connections such as routes, startup registration and background workers |
| Write or review code | Apply Clean Code, meaningful OOP and checks through the actual entry point |
| Research an API or technical question | Preserve source references, conflicting evidence and claims that need verification |

Works with Codex, Claude Code, Pi, OpenCode and compatible skill loaders. API-assisted routing requires Python 3.10+, file/shell access and a configured provider. Jev is optional; see [provider setup](references/setup.md).

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

Install once, choose a provider, then run a task. No second skill or extra supervisor is needed.

1. **Pick the model connection.** Use a matching System One, OpenAI-compatible Chat Completions or Anthropic Messages profile. A provider name alone does not determine the protocol.
2. **Save private settings and credentials.** Follow the [Windows or Linux/macOS setup steps](references/setup.md#2-create-your-private-configuration). Keep API keys out of Git and chat. Existing working configuration needs no replacement.
3. **Check the route.** From a repository checkout or the installed skill folder, run:

```bash
python scripts/jev_gate.py status
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
# Optional live connection test; may be billable
python scripts/jev_gate.py decide --request examples/manifest-decision.json
```

4. **Invoke the skill and give it your task**, using the [examples above](#how-to-use-it). The agent decides whether routing would replace enough reading to justify the extra call. It does not reduce context already read by the main model.

| Connection | Example profiles |
| --- | --- |
| Jev through GapGPT, TypeSafe or OpenRouter | [Choose a native System One profile](references/setup.md#1-choose-the-api-contract-and-provider) |
| A JSON-capable model through an OpenAI-compatible endpoint | [OpenRouter chat](examples/providers/openrouter-chat.json) |
| An Anthropic-compatible model | [Anthropic Messages](examples/providers/anthropic.json) |
| A locally hosted compatible model | [Ollama example](examples/providers/ollama.json) |

[Full setup, budgets, retries and troubleshooting](references/setup.md) · [Integrate evidence screening into your own tools](references/cost-routing.md)

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

For a **live connection check**, use the [connection-check commands](#configure-and-connect-complete-quickstart). It may be billable and confirms the configured route works; it does not establish savings. An optional small triage exercise is also available:

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

## Share and support the project

Thanks for using the skill. If it is useful, [star the GitHub repository](https://github.com/MehradYaghoubi/jev-research-engineering), share the source link, or [report a reproducible problem](https://github.com/MehradYaghoubi/jev-research-engineering/issues). No payment or star is required to use it.

Use the same repository link in free marketplace listings, technical posts and demos so people can inspect the source, read the limitations and get updates. [Ready-to-use English social posts and listing copy](publication/community.md) are available. Agensi listing is not yet confirmed.

[Versioned downloads and releases](https://github.com/MehradYaghoubi/jev-research-engineering/releases) · [Agent installation guide](references/installation.md) · [Compatibility checks](benchmarks/agent-installation.json)

Install through the command above and share the public repository. Skills.sh discovery uses real installation telemetry; submission or an install does not guarantee a ranking. [Distribution status](references/distribution.md) records submissions separately from confirmed listings. No popularity, usage or financial-savings claims are fabricated.

## فارسی

این اسکیل **رایگان و متن‌باز با مجوز MIT** است. هدف آن این است که پیش از خواندن حجم زیادی کد یا منبع تحقیق، شواهد مرتبط را انتخاب کند تا مدل اصلی کمتر مطالب نامرتبط بخواند. هزینهٔ احتمالی API به ارائه‌دهندهٔ انتخابی شما مربوط است.

[ویدئوی نصب و اتصال](https://github.com/user-attachments/assets/9155c730-eed7-4c1a-8668-9ed964611643) حدود سه‌ونیم دقیقه است؛ گویندگی و زیرنویس انگلیسی، نمایش تدریجی فرمان‌ها و مکث برای خواندن دارد. نصب آزمایشی و اتصال واقعی از مثال‌های تنظیمات و درخواست نمونه تفکیک شده‌اند.

اگر برایتان مفید بود، ممنون می‌شویم به [مخزن GitHub ستاره بدهید](https://github.com/MehradYaghoubi/jev-research-engineering) یا آن را به دیگران معرفی کنید؛ استفاده از اسکیل به ستاره یا پرداخت وابسته نیست.

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
