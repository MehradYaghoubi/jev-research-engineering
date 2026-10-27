# Real primary-agent A/B test

Two paired Codex CLI runs on a real bug in this repository **increased total primary-model tokens by 42.17%**. Uncached input decreased 1.82%. Neither pair demonstrated net token savings. This small-task result supports skipping routing for small changes.

| Run | Baseline input + output | Routed input + output | Change |
| --- | ---: | ---: | ---: |
| Pair 1 | 250,570 | 412,410 | +64.59% |
| Pair 2 | 366,675 | 465,108 | +26.84% |
| Sum | 617,245 | 877,518 | +42.17% |

| Sum across both runs | Baseline | Routed |
| --- | ---: | ---: |
| Input, including cached input | 613,291 | 872,541 |
| Cached input (subset of input) | 524,672 | 785,536 |
| Uncached input | 88,619 | 87,005 |
| Output | 3,954 | 4,977 |

## Method and quality

Source: `1e5ffceea29d472ef9a5841cdc7b4efb193f198b`. Task: reject JSON booleans for `max_request_bytes`, preserve inclusive integer bounds 1–100000, add regression coverage, and run the suite. Each arm received a separate copy of the same source. Baseline used ordinary search; it was not forced to read the entire corpus. Routed loaded the skill and a Jev shortlist, with permission to inspect other sources. Both used Codex CLI 0.162.1 with no model override; configured defaults were `gpt-6.1-sol`, medium effort. This records configuration, not independent verification of serving identity.

Each arm passed the same 13 independently checked valid/invalid configuration cases. All four full suites passed when independently rerun outside the Windows sandbox. Inside the sandbox, each arm encountered five temporary-directory permission errors; these environmental failures and associated agent work remain included in token counts. Consequently this is not a clean estimate for an environment without those failures.

One live GapGPT/Jev call supplied the shortlist: 4,802 input + 742 output tokens, served model `typesafe/jev-1.14-20261014`. Configured-rate estimated cost: **$0.000201684**, not an invoice-confirmed charge. Pair 2 reused that shortlist, so no second decision charge was incurred. These 5,544 decision tokens are additional to the primary-model totals above. Total measured model tokens across both pairs were 617,245 baseline versus 883,062 routed including this one decision call (+43.07%).

The observed primary-model increase is dominated by additional cached input. The routed arms also produced more output. The traces show more tool work in the first routed arm; they do not isolate a causal explanation for every extra token.

## Interpretation and limits

Counts come from final CLI `turn.completed.usage`, including repeated host/skill context and tool turns. Cached input is already part of input; separately reported reasoning output is not added again. The controller conversation, benchmark preparation and independent parent verification are outside these totals. This is therefore the whole measured primary-agent run, not the whole production conversation.

The second pair was started while the first summary was delayed; both are reported without choosing the favorable result. Two repetitions of one small bug do not predict results on large research corpora or other agents. For a subscription with no metered overage, there is no demonstrated reduction to the subscription bill; quota effects are unmeasured. API costs cannot be inferred from token totals without actual model/cache prices.

Structured counts and checks: [real-agent-ab.json](real-agent-ab.json). Historical synthetic context-only results remain separate: [token-counts.md](token-counts.md).
