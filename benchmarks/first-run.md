# First synthetic triage evaluation

Checked on 2026-10-28 in Europe/Istanbul. Provider: GapGPT; returned model: `typesafe/jev-1.14-20261014`. One run, three billable calls, no retries. Expected evidence IDs were written before the calls and were not included in provider requests.

| Case | Critical evidence recall | Baseline bytes | Routed bytes incl. output | Byte reduction | Jev input / output tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| missing_route | 100% | 2356 | 1663 | 29.41% | 907 / 134 |
| missing_worker | 100% | 2405 | 1720 | 28.48% | 896 / 136 |
| research_leakage | 100% | 2532 | 1792 | 29.23% | 910 / 136 |

All three cases passed: all nine expected critical evidence items were selected. Total source-context byte reduction was **29.04%**, after adding one excluded verification candidate per case and serialized routing-output overhead. Total reported Jev usage was **2713 input / 406 output tokens**. Estimated Jev cost was **$0.000113946**, using the configured $0.042/M input and $0/M output assumption; this is not a provider invoice. Total observed call time was about 3.34 seconds, excluding setup.

## What this establishes

The helper can use one bounded batch per task to retain the curated critical evidence while excluding obvious irrelevant material. Required-ID preservation, provider-failure retention, duplicate-ID rejection, single-candidate bypass, portable private paths and benchmark accounting also pass eight offline unit tests. The client self-test and skill-format validator passed.

## What it does not establish

- These are easy synthetic cases with clearly described wiring gaps and irrelevant distractors. The evaluation tests triage, not automatic discovery of a missing integration in a real repository.
- No implementation or scientific experiment was completed by two independent main-model runs. End-to-end correctness and Clean Code/OOP compliance are not benchmarked here.
- Source bytes are not tokenizer output or billed input tokens. The expensive model's tokens, cached-input use, output, tool overhead, skill-loading overhead, correction cost, and actual financial savings are unknown.
- No guarantee is made for ambiguous real-world candidates, another language/provider/model, the 0.35 cutoff, or larger corpora. One run is not a held-out quality study.

The next useful evaluation is a real task with the same acceptance test and comparable primary-model billing telemetry for a direct baseline and routed workflow. Do not present 29.04% context-byte reduction as 29.04% cost or token savings.

[Machine-readable results](first-run.json) · [Frozen fixtures](../tests/fixtures/triage_cases.json) · [Method](../references/cost-routing.md)
