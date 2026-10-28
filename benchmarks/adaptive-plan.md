# Adaptive evidence-intake test plan

Status: preregistered before inference. Local development only; publication is stopped.

## Hypothesis and scope

Full-evidence screening by Jev can replace primary-model evidence reading on larger tasks. Small tasks should bypass the provider. This tests a caller-controlled, single-turn evidence handoff, not a complete autonomous coding agent, every host integration, or subscription quota accounting. The previous Windows sandbox recovery runs remain published historical failures and are not overwritten.

## Workloads and arms

Freeze a small deterministic validation question, an engineering task on the real repository at `1e5ffceea29d472ef9a5841cdc7b4efb193f198b`, and a research-method comparison using current primary-source snapshots from Microsoft LLMLingua, RouteLLM and TypeSafe. Store source hashes, corpus content, evaluator and prompts before calling any models. These are authored engineering/research cases, not a public held-out benchmark or a universal accuracy estimate.

For each case run two repetitions of three arms: full supplied evidence, simple lexical evidence selection, and the revised adaptive Jev route. The full-evidence arm represents ordinary document intake; it is not a fair substitute for every code-search workflow, so the lexical competitor is required. Lexical selection uses query-word matches without gold answers. The adaptive arm includes the revised skill text in primary-model input. There is no instruction to use tools or troubleshoot test-environment problems inside the reader. All arms use the same installed CLI, model defaults, required response fields and task. Alternate arm order; no output-length/model changes between arms.

## Measurements and quality gates

- Primary metric: sum of reported `input_tokens + output_tokens` for the complete CLI run, including cached input. Preserve each arm and repetition.
- Secondary: cached/uncached input, output, decision calls/tokens/configured-rate estimate, context size, wall time and tool count. Tokenizer counts are diagnostic proxies only.
- Engineering: execute the returned replacement condition against the same valid/invalid bounds and verify the caller set. Research: check explicit factual propositions and cited evidence IDs. Small: exact answer. Keep gold checks out of decision/reader input.
- Unit/integration coverage: small-input bypass; full-body decision input; mandatory and verification evidence; malformed input; provider failure; oversized request; non-expanding output; audit separation. Run the entire helper suite outside the affected Windows sandbox.
- No claim of improvement unless all adaptive quality gates pass, summed primary tokens fall versus full intake, and total measured primary + decision tokens stay within 20% of full intake. Report lexical comparison even when it wins. An adaptive route that fails a quality gate is rejected regardless of token reduction.

## Stop rules and limitations

Maximum 18 primary-model reader runs (3 cases × 3 arms × 2 repetitions), plus at most one Jev call per eligible corpus; reuse frozen selections for reader repetitions and show one-shot versus amortized decision accounting. No retry after provider failure. Missing usage, authentication/network errors or unexpected reader tool execution invalidate the affected comparison and are reported. Do not weaken sandbox protections. Do not tune the implementation on reader answers and rerun until favorable. A negative result remains negative; no new release, push or marketplace submission is authorized by this experiment.

## Related methods consulted

[LLMLingua-2 paper](https://arxiv.org/abs/2403.12968) and [released evaluation scripts](https://github.com/microsoft/LLMLingua/blob/main/experiments/llmlingua2/README.md) motivate downstream-quality evaluation rather than compression ratio alone. Its learned token compressor is different from selecting intact evidence blocks; its reported gains cannot be copied to Jev.

[RouteLLM paper](https://arxiv.org/abs/2406.18665) and [evaluation implementation](https://github.com/lm-sys/RouteLLM) motivate baseline comparisons and cost/quality trade-offs. It routes between answer models, while this project keeps the user's primary model; those financial results are not evidence of primary-model token savings here.

[TypeSafe introduction](https://docs.typesafe.ai/introduction) defines atomic typed judgments. Jev can screen supplied evidence; it does not generate the patch or research explanation. No third-party savings percentage is adopted as this project's result.
