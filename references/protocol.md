# Configuration and decision protocol

Run `python <skill>/scripts/jev_gate.py configure` once for a non-echoing key prompt. The helper stores Windows user-bound DPAPI ciphertext outside the skill. A private directory outside the skill is required. Keep its existing value when upgrading if you want to preserve that credential and usage ledger; the public TypeSafe default is `~/.research-engineering-router/typesafe`. Home and environment variables in this path are expanded. Another machine needs its own private path and credential. The configured `api_key_env` overrides the stored key (legacy configs default to `JEV_API_KEY`). `--config` and `DECISION_GATE_CONFIG`/legacy `JEV_GATE_CONFIG` select a config; otherwise a private user config is preferred over the public default. Never include a key in a request file or a shared skill.

Commands: `status`, `self-test`, `usage`, and `decide --request <file.json> --dry-run` make no provider calls. `decide --request <file.json>` sends one logical request with up to three bounded attempts for transient failures. Use the installed Python runtime if `python` is not on PATH. Status means the credential can be loaded; only a live request verifies connectivity and acceptance.

## Bounded retry policy (local development revision)

`max_attempts` defaults to 3, including the initial attempt; set 1 to disable replay. Only integers 1–3 are accepted. `retry_budget_seconds` defaults to 90 (accepted range 1–180). Transient HTTP 408/429/500/502/503/504/529, timeouts and connection failures may replay. Invalid credentials, permanent HTTP errors, invalid JSON/typed answers, certificate verification failures and local validation errors do not. Backoff is 1 then 2 seconds; a valid `Retry-After` or `retry-after-ms` can require longer. Do not retry earlier than the server's delay: if it cannot fit the remaining retry window, return failure. Socket timeouts are capped by the remaining window; local credential/ledger bookkeeping can add overhead.

Each actual attempt reserves and records its own ledger charge. A timeout/reset may occur after provider processing, so replay can incur another charge; no idempotency guarantee is invented. The successful response has `request_attempts` and sanitized `attempts` metadata. After an ambiguous failed attempt, aggregate `usage` stays unknown, `successful_usage` records only the final response, and `estimated_usd` includes failed-attempt reservations. It is not an invoice-confirmed total. Exhaustion preserves attempt details for helper audit/fallback. Dry-run makes no attempts.

The context preprocessor budgets retries across its batches using the existing task call limit; there is no second outer retry loop. Unknown attempts are not converted to zero. Every backoff, failed attempt and final fallback belongs in whole-task timing. See [TypeSafe guidance](https://help.typesafe.ai/articles/2769560962-what-is-the-difference-between-429-and-529).

The public default is direct TypeSafe with model `jev-1.14.0`; a private user config preserves personal choices such as GapGPT. `protocol` selects `systemone`, `openai-chat` or `anthropic`; see [access methods](access.md) for ready-to-edit profiles. The native question types are described in [TypeSafe's introduction](https://docs.typesafe.ai/introduction); provider limits and billing may differ. The helper accepts the user's string, list-of-strings, or question-object instruction forms and validates returned IDs, values, and probability distributions.

## Example: select the next experiment

```json
{
  "state": {
    "goal": "Determine whether candidate retrieval improves answer quality",
    "evidence": {
      "e1": "Baseline: 12 correct answers in 20 fixed cases; retrieval: 13 in the same cases",
      "e2": "Cases and scoring were selected after inspecting retrieval outputs"
    },
    "constraint": "One hour; existing dataset only"
  },
  "questions": {
    "next_step": {
      "type": "choice",
      "instructions": "Which next step best tests whether the apparent improvement generalizes under the constraint?",
      "criteria": {
        "held_out": "Freeze scoring and compare both methods on untouched cases",
        "repeat_selected": "Repeat only the selected examples",
        "insufficient": "The supplied evidence cannot distinguish these options"
      }
    },
    "selection_bias": {
      "type": "noul",
      "instructions": "Does e2 describe a risk of selection bias?"
    },
    "evidence_strength": {
      "type": "score",
      "instructions": "How strong is the supplied evidence for generalizable improvement?",
      "criteria": ["Exploratory and biased", "Controlled but limited", "Independent and replicated"]
    }
  }
}
```

This is synthetic evidence, not a benchmark result. Parse `answers` by question ID: `noul` is a probability in [0,1], `choice` is an option ID, and `score` lies between zero and the last rubric index. Scores can be fractional. Confidence is advisory; do not treat it as a calibrated guarantee for this workload. Each question sees the same state independently. Never chain dependent questions in one batch.

## Accounting and failure behavior

Read `references/config.json` for endpoint, model, private storage, request limit, timeout, estimated prices, and budget. The helper pins the model, requires HTTPS except explicitly allowed literal loopback HTTP, refuses redirects, limits response size, and validates the response. `max_jev_calls_per_task` is an agent-side limit, not a helper-enforced quota.

The SQLite ledger reserves an estimate before a call under a transaction, shared by users of this private directory. It stores request hashes, status, usage, and estimated charges, never request text or keys. Failed calls retain reservations because billing is unknown. Missing usage keeps the conservative reservation. The daily boundary is UTC. This budget does not cap other software or replace provider billing; rate changes and estimation error can affect actual spend. Prices are configured estimates. The helper does not enable experimental long context or assume a long-context surcharge. Update rates for your provider; the default request cap is 32,000 bytes.

An unavailable API or rejected response means report the limitation and continue with the selected model. Do not silently loosen validation, switch endpoints, or retry. Diagnose a failed connection with secret-free status information before another user-authorized test.

For local, cloud, first-party and third-party access, read [access methods](access.md). For context manifests and measured-versus-estimated cost, read [cost routing](cost-routing.md).

For disjoint cache categories, subscription versus metered billing, provider-reported cost and the decimal comparison tool, read [financial accounting](financial-accounting.md).
