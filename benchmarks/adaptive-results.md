# Adaptive evidence-intake pilot

Local, unpublished development result. The [plan](adaptive-plan.md) was frozen before inference. Eighteen real Codex CLI reader runs completed: three authored cases, three arms, two repetitions. The selected CLI model defaults were preserved. No reader tool calls or Windows temporary-directory recovery loops occurred.

## Primary-model result

| Case, two repetitions | Full intake tokens | Adaptive tokens | Adaptive change |
| --- | ---: | ---: | ---: |
| Small, provider bypassed | 47,422 | 47,822 | +0.843% |
| Engineering, real repository source | 58,136 | 56,055 | -3.580% |
| Research, primary-source snapshots | 58,696 | 59,010 | +0.535% |
| Total | 164,254 | 162,887 | -0.832% |

Tokens are reported input plus output, including cached input. Separately reported reasoning output is not added again. This is a small observed reduction, not proof of reliable savings. Host-provided input counts varied between repetitions with identical frozen user prompts; this variation is material relative to the aggregate difference. The research route kept all evidence, so its reader variation is not evidence of compression benefit.

| Arm | Passed quality cases | Total primary tokens |
| --- | ---: | ---: |
| Full supplied evidence | 6/6 | 164,254 |
| Simple lexical selection | 4/6 | 160,577 |
| Adaptive Jev screening | 6/6 | 162,887 |

Lexical selection saved more tokens but omitted the defining script's own `load_config` caller in both engineering responses. The adaptive responses retained it. Research responses were checked for four explicit propositions and supporting source IDs. Returned engineering conditions were executed against 13 fixed valid/invalid values. These checks establish correctness for these cases, not broad research or coding competence.

## Routing and total overhead

Small input: zero decision calls. Engineering: one live Jev call, 5,807 input + 120 output tokens; evidence packet 20,835 → 15,837 bytes. Research: one live Jev call, 6,291 input + 101 output tokens; no useful selection reduction, so the original 20,458-byte packet was retained. Provider-reported served model: `typesafe/jev-1.14-20261014` through the configured GapGPT route.

Both reader repetitions reused frozen selections. Actual routing usage: 12,319 tokens and **$0.000508116 configured-rate estimated cost**, not invoice-confirmed spend. Primary plus decision tokens: **175,206, +6.668%** versus full intake. If a new routing call were charged for each reader repetition, the corresponding total would be **187,525, +14.168%**. Reuse accounting is explicit; neither total includes this controller's development/setup conversation.

Cached input was 36,480 full versus 7,296 adaptive; uncached input was **127,240 versus 154,922**. Therefore a lower total token count does not establish lower metered cost. Under the user's unchanged fixed subscription, no subscription-bill reduction is demonstrated; the decision provider adds its estimated charge. Quota effects are unmeasured.

## Task completion speed

Speed was examined after the user's additional request using all already-recorded monotonic reader durations; no inference was repeated. Each duration covers CLI subprocess launch through completed output, including startup. Two jobs ran concurrently; queue wait is excluded. These are task-reader wall times, not isolated model inference latency or benchmark throughput.

| Case | Full intake mean seconds | Adaptive mean seconds | Change |
| --- | ---: | ---: | ---: |
| Small | 68.485 | 66.615 | -2.73% |
| Engineering | 70.130 | 72.010 | +2.68% |
| Research | 67.990 | 70.220 | +3.28% |

Sum of the six full-intake task durations: **413.21 s**; adaptive: **417.69 s**, **1.084% slower**, before adding external preparation. This is a sum of individual task latencies, not elapsed makespan of a concurrent batch. The interval between frozen-input and completed-routing file timestamps was approximately 3.153 s across all three preparations and two live Jev calls. Adding that interval once gives approximately **1.847% slower** with selection reuse; it is not a precisely instrumented end-to-end measurement or per-provider latency.

There is **no demonstrated speed improvement**. The small-case difference happened without Jev and cannot be credited to it. All adaptive answers passed; two lexical engineering failures are incomplete tasks and cannot count as successful faster completions. Two samples per case/arm and external service/startup variation do not support a p95 or general speed claim. The helper now writes monotonic preprocessing `elapsed_seconds` to future audit files; this instrumentation was added after the original selection calls and is not retroactively fabricated for them.

## Changes tested

- Shorter entrypoint: 997 → 395 local `o200k_base` text tokens; detailed workflow remains available progressively. These are tokenizer proxies, not served-model billing counts.
- `prepare_context.py` screens complete, explicitly supplied evidence blocks before lead-model intake. Unlike summary-only file triage, it can replace reading those full blocks in the primary model.
- Small-input bypass, configured request bound, mandatory evidence, strongest excluded verification block, safe fallback and no packet expansion. Routing bookkeeping goes to an audit file, not the primary evidence packet.
- Reader evaluation isolates evidence intake from unrelated sandbox debugging. Existing host sandbox protections were retained. Detailed unchanged environmental failures should not be repeatedly sent into model context.

The helper requires an actual caller integration before lead-model reading. A portable Markdown skill cannot intercept every agent's input, erase already-read context, or guarantee savings on all tasks. The original summary-only selector remains available for compatibility.

## Evaluation correction and limits

The prompt did not specify whether `evidence_ids` must be a list or a map of claims to lists. The original evaluator incorrectly rejected three factually correct research responses using the latter format. Its source was preserved; a documented structural normalization was applied symmetrically to all 18 saved responses, without model reruns or changes to factual/engineering criteria. Raw results and corrected results remain separate locally. This post-run correction limits the strength of the experiment; future studies should enforce an explicit output schema upfront.

All registered aggregate pilot gates passed: adaptive quality 6/6, total primary tokens lower, overall model-token growth below the preselected 20% pilot cap. **This does not meet a stronger standard of demonstrated general savings.** Two cases increased primary tokens, the aggregate gain is small, and uncached input increased. The 20% cap was a test design choice, not an inferred user-approved universal threshold.

This is a single-turn evidence-handoff pilot, not an autonomous implementation/R&D benchmark. It is not directly comparable to the earlier multi-step sandbox bug-fix A/B. Do not claim the old +42.17% was causally converted into -0.832% by these edits. No full agent deployment or new official/public release occurred.

Structured per-run counts, source hashes and limitations: [adaptive-results.json](adaptive-results.json). Complete frozen corpus, reader prompts, raw responses, evaluator versions and logs remain in the workspace's local `.agent-qa/adaptive-intake/` directory. The local runner is `.agent-qa/run_adaptive.py`; a new experiment needs a new output directory rather than overwriting the original.

Related work: [LLMLingua-2](https://arxiv.org/abs/2403.12968), its [released downstream evaluation](https://github.com/microsoft/LLMLingua/blob/main/experiments/llmlingua2/README.md), and [RouteLLM](https://arxiv.org/abs/2406.18665). Their experiment methodology informed this plan; their models were not installed or benchmarked here and their savings percentages are not transferred to Jev.
