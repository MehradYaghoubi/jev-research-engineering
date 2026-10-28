# Token target replication with bounded transient retries

Measurements were captured locally before the experimental v0.3.0 release. The [prospective plan](retry-confirmation-plan.md) fixed the user-confirmed target at **at least 10% fewer total primary-model input + output tokens**, preserving answer quality. Speed was recorded for later assessment.

## Registered result

| Six matched operational trials | Primary alone | Jev-assisted |
| --- | ---: | ---: |
| Input including cached input | 199,537 | 179,104 |
| Output | 500 | 530 |
| Total primary tokens | **200,037** | **179,634** |
| Quality checks passed | 6/6 | 6/6 |

Observed reduction: **20,403 primary tokens, 10.1996%**. The registered aggregate target passed on these cases. Cached input (a subset of input) was 0 versus 24,960; it was included rather than subtracted from the target metric. Separately reported reasoning output is not added twice.

| Workload, three paired repetitions | Primary alone | Jev-assisted | Reduction |
| --- | ---: | ---: | ---: |
| Authentication-boundary code audit | 100,506 | 86,480 | 13.9554% |
| TypeSafe primitive-contract research | 99,531 | 93,154 | 6.4070% |

Combined reductions by repetition were **10.5856%, 9.8660%, 10.1451%**. One repetition and the research category alone were below 10%. The margin is small; this is not a guarantee, a robust population estimate or proof of a 10% gain on every task.

All twelve reader runs completed with reported usage, explicit JSON schema validation, unchanged factual/source-ID checks, no reader tool calls and no reader retries. Same installed CLI/default model settings; no forced smaller output or alternative lead model. The configured defaults were `gpt-6.1-sol`, medium effort; serving identity was not independently attested. Every adaptive repetition made fresh decision requests: no reused selections or amortization.

## Whole-process time, as requested by the user

Timers started before corpus preparation/configuration loading and ended after the primary response and independent quality check. They include fresh Jev calls, local processing and any applicable retry/backoff. Frozen-corpus construction was common experiment setup and was outside operational timers. Queue wait was excluded. Two jobs ran concurrently; the following sums are **individual task latencies, not batch makespan**.

| Complete operational task time | Primary alone | Jev-assisted |
| --- | ---: | ---: |
| Mean per task | 66.452 s | 80.020 s |
| Sum across six tasks | 398.712 s | 480.123 s |
| Preparation component, sum | 0.005 s | 77.128 s |

The complete Jev-assisted path was **20.4186% slower**. This is a measured whole-process comparison, not reader time plus an estimated routing duration. No speed improvement is claimed.

## Decision usage and money

Twelve logical decision batches produced twelve HTTP attempts, all successful on their first attempt in this replication. Decision usage: **98,083 tokens**. The configured-rate decision estimate was **$0.003549672** for the six assisted tasks, not an invoice-confirmed charge.

All-model tokens including Jev were **277,717 versus 200,037**, an increase of **38.8328%**. The accepted target concerns the primary model, not this all-model total. A fixed ChatGPT/Codex subscription bill was not reduced by this experiment; quota/capacity effects remain unmeasured. Do not convert the observed primary-token decrease into a financial-savings claim.

## Reliability changes

The user authorized bounded replay after the earlier cycle's timeout-like failure. The shared client now permits at most three attempts for eligible timeout/connection and temporary HTTP errors, with 1/2-second backoff, server `Retry-After` support, a bounded retry window, independent ledger reservations and task-wide attempt allocation across context batches. It never retries invalid credentials, permanent HTTP errors, invalid typed responses or certificate failures.

Failed attempts keep unknown usage/billing and conservative reservations, even when a later response succeeds. Successful final usage is available separately; it is never substituted for unknown aggregate usage. Exhaustion retains the original evidence. This replication had no cloud retry event, so it does not prove recovery from an actual provider outage. Separate tests exercise simulated timeouts, budget/deadline exhaustion and a real loopback HTTP server returning 503 then 200. The loopback integration is an actual transport test with injected failure, not a live GapGPT outage.

Final local suite: **49 tests passed**. The earlier [rejected confirmation](atomic-results.md), development attempts and [18-run intake pilot](adaptive-results.md) remain separate; no failure was discarded or rescored to rescue a result.

## Scope and reproducibility

This is a **single-turn evidence-intake replication on two authored code-audit/research tasks**, not an autonomous implementation/R&D benchmark or proof across every agent. The shared helper uses atomic evidence questions and smaller source spans to replace lead-model reading. The caller must integrate it before lead-model intake; a portable Markdown skill cannot erase already-read history or intercept every host automatically.

The exact corpus/tasks/schemas and evaluator were frozen from the earlier confirmation; new implementation hashes and skill text were frozen before inference. Runtime source hashes still matched at analysis time. This is replication on known tasks after a reliability-policy change, not a newly held-out dataset. Host context/input counts varied across repetitions; broader tasks and stronger replication are needed before publication.

[Structured per-run results and hashes](retry-confirmation-results.json). Complete private operational artifacts remain in local `.agent-qa/retry-confirmation/`; runners are `.agent-qa/run_atomic_confirmation.py` and `.agent-qa/run_retry_replication.py`. The initial frozen corpora remain in `.agent-qa/atomic-confirmation/frozen.json`.

Relevant primary sources: [TypeSafe atomic fan-out](https://docs.typesafe.ai/patterns/fan-out), [Choice contract](https://docs.typesafe.ai/primitives/choice), [transient-error guidance](https://help.typesafe.ai/articles/2769560962-what-is-the-difference-between-429-and-529), [Anthropic programmatic context filtering](https://www.anthropic.com/research/code-execution-with-mcp). Their architectural ideas informed the implementation; their performance figures are not claimed here.
