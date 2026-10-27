# Context selection and cost measurement

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

Run `python scripts/select_context.py --manifest manifest.json` from the skill directory. It emits selected/excluded IDs, one strongest excluded ID to inspect, reported Jev usage and estimated cost. Map IDs to local paths or source URLs outside the API payload; retrieve only selected bodies plus the verification candidate. Candidate IDs must be unique lowercase identifiers. Mark user-required evidence and known dependencies `required: true`; they survive a bad ranking. A single candidate or an all-required list skips the API. A provider failure retains every candidate and reports fallback.

Generate summaries using bounded index/search results, and save them directly through tools rather than printing all source bodies into the lead model's context. An example approach is an explicit allowlist of files with path, symbol signature, matched lines and nearby registration points. Read surrounding code only after selection. Manually redact secrets and obey repository data restrictions before calling the helper. It does not scan arbitrary files, discover missing architecture automatically, or promise that an excerpt is safe to send.

The 0.35 relevance cutoff is deliberately permissive but uncalibrated. It is not a statistical guarantee. No hard top-k truncation: correctness takes priority over forcing a reduction. If the task changes or a selected source points to another dependency, retrieve that dependency without asking Jev to authorize it. For broad searches, stage deterministic filtering before ranking; do not split a budget into unlimited subtasks.

## Measure the whole route

Compare a direct baseline and a routed run on equivalent tasks, model settings, acceptance checks and evidence access. Record main-model uncached/cached input and output, Jev usage, latency, tool/routing cost, retries, correction work and verified quality. Count initial routing prompt and skill-loading overhead. Log no private source bodies or secrets.

`baseline cost = main-model baseline cost + baseline tools`

`routed cost = main-model routed cost + Jev cost + routed tools + correction cost`

Savings exist only when routed cost is lower while the acceptance checks still pass. Lower main-model input alone can lose money if output or correction work grows. Main-model API billing may not map to a flat-rate chat subscription. The skill cannot change the selected chat model, compress already-read history, or inspect private billing telemetry automatically.

The included benchmark measures synthetic evidence recall and source bytes delivered after selection, including a verification candidate and serialized routing output. It reports actual provider tokens and configured-rate Jev cost. Source bytes are a context-size proxy, not tokenizer output or main-model billing. Main-model savings remain unknown until measured by the host. There are no published percentage savings claims for this skill.
