# Context selection and cost measurement

## Screen evidence before lead-model intake

`python scripts/prepare_context.py --corpus corpus.json --audit new-audit.json` accepts an explicitly authorized JSON corpus: `{"task":"question", "candidates":[{"id":"source_a", "body":"complete evidence block", "required":true}, {"id":"source_b", "body":"other evidence"}]}`. IDs follow the manifest rules below. Generate this file directly with search/export tools, without first printing full bodies to the lead model. The operator must approve the evidence trust boundary; this helper does not scan the filesystem or redact arbitrary secrets.

For fewer than four blocks or under 16 KB serialized evidence, it skips the provider. This is a conservative heuristic, not a measured universal break-even point. The current local candidate splits larger bodies into bounded line blocks, preserving source IDs and line ranges within the supplied body (not necessarily original file line numbers). It shares only the task across questions and puts each block inside its own typed Choice question. Direct evidence, explicit uncertainty, mandatory blocks and direct/uncertain probability mass of at least .35 are retained. The strongest excluded verification block is retained too. Scores are judgments, not correctness guarantees.

All requests are planned and validated before sending: at most three independent batches per corpus, bounded further by `max_jev_calls_per_task`, the configured byte limit and shared daily ledger. Batches contain different questions; transient failures may be retried under the bounded policy below; invalid credentials and invalid responses are not retried. If planning exceeds these bounds, the helper keeps original evidence with no call. A partial provider failure keeps the complete original corpus, records completed batch information, and leaves unknown billing/attempt status unknown. Callers must also respect the remaining task-wide decision-call allowance. There is no forced top-k.

Stdout contains only task and delivered evidence; provider usage/cost, preprocessing `elapsed_seconds` (monotonic wall time, including a decision call when made) and selection bookkeeping go to the optional new audit file. Existing audit files are never overwritten. An unhelpful selection returns the original packet. This prevents packet expansion; it does **not** bound skill/tool overhead or guarantee fewer total primary-model tokens. A portable skill cannot automatically intercept every host's input: the caller must invoke the helper before lead-model intake. The older summary-only selector remains compatible for callers that already have summaries.

Detailed failure tracebacks should be kept in a local log, with a bounded error summary delivered to the lead. After an unchanged environment failure, diagnose or report it instead of rerunning the same full suite. Do not weaken the sandbox to improve benchmark scores.

## Manifest

The helper accepts only the task and compact candidate summaries, not full bodies:

```json
{
  "task": "Make the refund endpoint reachable from application startup",
  "candidates": [
    {"id": "startup", "summary": "app.py registers orders and users routers", "required": true},
    {"id": "refund", "summary": "refunds.py exports a router; no startup registration found"},
    {"id": "theme", "summary": "CSS color tokens"}
  ]
}
```

Run `python scripts/select_context.py --manifest manifest.json` from the skill directory. It emits selected/excluded IDs, one strongest excluded ID to inspect, reported the decision model usage and estimated cost. Map IDs to local paths or source URLs outside the API payload; retrieve only selected bodies plus the verification candidate. Candidate IDs must be unique lowercase identifiers. Mark user-required evidence and known dependencies `required: true`; they survive a bad ranking. A single candidate or an all-required list skips the API. A provider failure retains every candidate and reports fallback.

Generate summaries using bounded index/search results, and save them directly through tools rather than printing all source bodies into the lead model's context. An example approach is an explicit allowlist of files with path, symbol signature, matched lines and nearby registration points. Read surrounding code only after selection. Manually redact secrets and obey repository data restrictions before calling the helper. It does not scan arbitrary files, discover missing architecture automatically, or promise that an excerpt is safe to send.

The 0.35 relevance cutoff is deliberately permissive but uncalibrated. It is not a statistical guarantee. No hard top-k truncation: correctness takes priority over forcing a reduction. If the task changes or a selected source points to another dependency, retrieve that dependency without asking the decision model to authorize it. For broad searches, stage deterministic filtering before ranking; do not split a budget into unlimited subtasks.

## Measure the whole route

Compare a direct baseline and a routed run on equivalent tasks, model settings, acceptance checks and evidence access. Record main-model uncached/cached input and output, the decision model usage, latency, tool/routing cost, retries, correction work and verified quality. Count initial routing prompt and skill-loading overhead. Log no private source bodies or secrets.

`baseline cost = main-model baseline cost + baseline tools`

`routed cost = main-model routed cost + the decision model cost + routed tools + correction cost`

Savings exist only when routed cost is lower while the acceptance checks still pass. Lower main-model input alone can lose money if output or correction work grows. Main-model API billing may not map to a flat-rate chat subscription. The skill cannot change the selected chat model, compress already-read history, or inspect private billing telemetry automatically.

The included benchmark measures synthetic evidence recall and source bytes delivered after selection, including a verification candidate and serialized routing output. It reports actual provider tokens and configured-rate the decision model cost. Source bytes are a context-size proxy, not tokenizer output or main-model billing. Main-model savings remain unknown until measured by the host. There are no published percentage savings claims for this skill.

## Token-count result

Run `python scripts/measure_tokens.py` to count the recorded selections with optional `tiktoken` (`benchmarks/requirements.txt`). This makes no inference calls. Report both context-only counts and one entrypoint load. The selected chat model has no verified tokenizer mapping in the installed library, so `o200k_base` is an explicit text-count encoding, not billed chat usage. `cl100k_base` is reported as a sensitivity check.

The small synthetic workload shows that routing can lose after instruction overhead. Read [the measured token comparison](../benchmarks/token-counts.md). Skip routing when eliminated work is too small to justify the extra instructions, requests and result metadata. Do not promote the byte reduction as token or cost savings.
