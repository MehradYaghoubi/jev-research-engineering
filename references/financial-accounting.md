# Financial and token accounting

## State the billing arrangement first

A fixed subscription and a metered API have different marginal costs. If the same Codex/ChatGPT subscription is paid in both alternatives, with no paid overage or avoided upgrade, its fixed fee cancels. Fewer text tokens do not directly refund subscription money. An additional decision API introduces a small incremental charge. Reduced quota pressure is a possible operational benefit, but this repository has no verified mapping from a text-token count to Codex quota consumption or avoided subscription cost.

A metered API comparison needs both baseline and routed provider usage, actual model/provider prices, cached-input categories, output, tools and correction work. A tokenizer count is not billed usage; output, repeated history and caches cannot be assumed unchanged without evidence. Provider-reported request cost is preferred where supplied, and final provider billing remains authoritative.

## Per-call formula and units

All rates below are **USD per million tokens**, counts are nonnegative integers, and the four categories are disjoint:

`call USD = (uncached input × input rate + cache read × read rate + cache write × write rate + output × output rate) / 1,000,000`

Normalized helper `usage.input_tokens` is total input. Therefore:

`uncached input = input_tokens - cache_read_input_tokens - cache_write_input_tokens`

OpenAI-style usage includes cache-read tokens in prompt_tokens. Anthropic-style raw input_tokens excludes cache-read and cache-creation counts, so those counts are added into normalized total input before applying this formula. Output tokens include the provider's reported completion usage; do not subtract reasoning tokens already included in that total. The helper does not enable prompt caching automatically. Mixed write TTLs or special tiers need correct effective rates/split accounting or provider-reported cost, not an assumed discount.

`baseline USD = sum(baseline calls) + baseline other costs`

`routed USD = sum(primary + decision calls + retries/corrections) + routed other costs`

`saving USD = baseline USD - routed USD`

`saving % = saving USD / baseline USD × 100`, undefined when the baseline incremental cost is zero.

The helper ledger uses configured prices when request cost is not reported; it is an estimate. Failed-call reservations are held because billing is unknown: a reservation is neither confirmed spend nor a free failed call. Different model tokenizers and prices mean summing all tokens cannot alone decide which route is cheaper. Report actual token categories per model, then sum dollar charges.

## Reproducible decimal calculator

```bash
python scripts/compare_costs.py --input examples/subscription-cost-comparison.json
python scripts/compare_costs.py --input examples/api-cost-comparison.json
```

The calculator uses Decimal arithmetic and reports each call separately. Supply normalized usage, the relevant rates, and explicit `baseline_other_usd` / `routed_other_usd` values. Null means unknown, not zero. A rate is required for each nonzero bucket. A provider-reported cost can be supplied as `provider_reported_usd`; an explicit fixed/marginal assumption uses `fixed_cost_usd` and is labelled as such, not falsely labelled provider-reported. Keep the source of usage (`provider-reported`, `tokenizer scenario`, etc.) visible.

The API example intentionally has null primary usage/prices and other costs. Its result remains incomplete until real inputs are provided. Do not populate those fields with guessed model billing data merely to produce a percentage.

## Known result for the published three-case test

- Full evidence input text: 1316 tokens under o200k_base.
- Routed evidence, verification source and routing output: 1093 tokens, 16.95% lower.
- One 923-token skill entrypoint load gives 2016 tokens, 53.19% above this small baseline. This extra input is in the primary model, not Jev usage. Actual quota/billing effects are unmeasured.
- Decision provider reported 2713 input and 406 output tokens. At configured rates of $0.042/M input and $0/M output: **$0.000113946**, or **0.0113946 cents**. This is a configured-rate estimate, not a verified invoice.
- Under the unchanged-fixed-subscription/no-overage assumption, baseline incremental main-model charge is zero and the routed alternative adds that estimated decision charge. A percentage saving against a zero incremental baseline is undefined. [Calculator output](../benchmarks/subscription-cost-comparison.json).
- For metered API users, the [warm/cold illustrative calculation](../benchmarks/token-counts.md) is arithmetic under explicitly hypothetical rates; it is not this subscriber's saving. [Incomplete API comparison](../benchmarks/api-cost-comparison.json).

A useful next experiment needs a real task, the same acceptance check, comparable baseline/routed primary usage reports and a stated quota/billing measure. Loading all evidence into the main model before routing cannot save already-consumed tokens. A fixed instruction may be repeatedly charged or cached in multi-turn API use; do not assume it is financially free after its first load.
