# Atomic evidence screening: confirmation plan

Local development; publication remains stopped. Target explicitly confirmed by the user: at least **10% reduction of total primary-model input plus output**, with preserved answer quality. Speed is recorded, but acceptance focuses on tokens first. No broad claim that every small task saves 10% is possible; this confirmation concerns the evidence-heavy workload for which routing is designed. Small-input bypass remains covered by regression tests.

## Why change the design

Development on the previously seen corpora showed that merely dividing files into smaller blocks retained too much background. The original shared-state selection also exposed every question to every candidate. The new path shares the task, puts each evidence block in its own atomic typed question, and separates direct evidence, background, unrelated material and uncertainty. Required blocks, uncertain labels, probability mass of at least .35 on direct/uncertain (when provided), and the strongest excluded verification block remain protected. No top-k cap is used.

Small line blocks require more question metadata. Plan all bounded requests before inference; at most three independent batches per corpus, each respecting the existing configured byte bound and daily ledger. This is batching different questions, not retrying a failed call. Stop and retain the original corpus after a partial failure. Preserve unknown attempt/cost status. If preflight exceeds the call budget, make no calls and return the original evidence.

## Frozen confirmation

Use two **new tasks** distinct from the development tasks: authentication/configuration boundaries in actual repository code, and TypeSafe primitive/uncertainty contracts from official documentation. Freeze actual source text, source hashes, queries, response schemas, hidden factual checks and implementation hashes before the first confirmation model/API call. These are authored confirmation tasks, not a public benchmark or evidence of all-agent performance. Do not pad corpora with generated filler or tune the implementation after inspecting reader answers.

Compare normal full evidence intake with the atomic Jev route: three paired repetitions per task, alternate full-first and routed-first order, same installed CLI/model defaults and response schema. No model change or weakened sandbox. Add one lexical-comparator run per task; report its quality even when it is cheaper. Maximum fourteen primary reader runs in this confirmation cycle. Existing development failures remain separate.

For each routed repetition make fresh decision calls; **no amortized reuse** in acceptance totals. Start a monotonic end-to-end timer before evidence preparation/config loading and stop after the primary answer and independent quality check. Baseline starts at the same boundary, with its own normal preparation. Record preparation, reader and end-to-end times separately; do not add a file-timestamp estimate to an unrelated run. Do not retry failed readers or providers.

## Acceptance and reporting

All six routed confirmations must pass every factual and citation check. Compare sums of actual CLI input + output, including cached input, against the six full-intake runs; require at least 10% reduction. Report per-task and per-repetition results, cached/uncached differences, all decision tokens and configured-rate estimates, and total model-token growth. Readers must make no unexpected tool calls; missing usage or protocol/runtime errors invalidate a positive claim. Record speed but do not declare speed improvement before examining the whole-process durations.

Enforce an explicit JSON output schema before inference, including an array of evidence IDs; do not modify the evaluator to rescue answer formats. A failed quality gate rejects the variant even if token reduction is large. Passing this small confirmation does not establish statistical generality, actual subscription savings, or autonomous-agent integration. Broader real task verification is still required before publication.

## Primary evidence consulted

[TypeSafe atomic decisions and fan-out](https://docs.typesafe.ai/patterns/fan-out), [Choice contract](https://docs.typesafe.ai/primitives/choice), [Anthropic programmatic filtering](https://www.anthropic.com/research/code-execution-with-mcp), and [LLMLingua downstream evaluation](https://github.com/microsoft/LLMLingua/blob/main/experiments/llmlingua2/README.md). They inform the architecture and experiment; their savings numbers are not adopted as this project's result.
