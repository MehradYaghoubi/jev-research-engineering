# Token comparison against the full-context baseline

Measured with `tiktoken 0.14.0`, encoding `o200k_base`. The exact strings are reconstructed from the frozen fixtures and recorded successful provider selections. No new model inference is used for counting.

| Case | Full-context tokens | Routed tokens incl. result JSON | Tokens removed | Context reduction |
| --- | ---: | ---: | ---: | ---: |
| missing_route | 448 | 375 | 73 | 16.29% |
| missing_worker | 433 | 358 | 75 | 17.32% |
| research_leakage | 435 | 360 | 75 | 17.24% |
| **Total** | **1316** | **1093** | **223** | **16.95%** |

Every expected critical source remains selected. Routed strings include selected source bodies, one excluded verification source per case, and the selector's full JSON output. This comparison counts tokens, replacing the older byte-only proxy; 29.04% fewer bytes was not 29.04% fewer tokens.

## Instruction overhead changes the conclusion

The pre-portability entrypoint measured at revision `3a6c2ab` cost **923 tokens** in this encoding. Adding one load across these three tasks gives **2016 tokens**, compared with **1316** in the direct full-context baseline: **53.19% more input text tokens**. The small workload therefore does **not** demonstrate a net token saving. Per-request references, tool wrappers, repeated chat history, cache behavior and output/correction work can add further differences.

The right response is to skip decision-model routing on small workloads, not to advertise the context-only percentage as end-to-end savings. The skill now explicitly checks whether likely eliminated work justifies routing overhead.

As an encoding sensitivity check, `cl100k_base` counts 1324 baseline and 1105 routed tokens (**16.54% context reduction**); with one 930-token skill load, the result is **53.7% more**. Neither encoding has a verified mapping to the selected `gpt-6.1-sol` chat model in this installed library. These are exact tokenizer text counts, **not actual billed primary-model usage** or a measured financial saving.

## Reproduce

```bash
python -m pip install -r benchmarks/requirements.txt
python scripts/measure_tokens.py
python scripts/measure_tokens.py --encoding cl100k_base --output benchmarks/token-counts-cl100k.json
```

The optional tokenizer dependency is separate from the standard-library runtime. Counts require no inference calls. Compare primary-model billing and verified task outcomes in a controlled direct-versus-routed run before claiming financial savings. Jev's observed input/output usage and estimated cost remain in [the original provider run](first-run.json); tokens from different models have different prices and tokenizer conventions.

[Machine-readable o200k results](token-counts.json) · [cl100k sensitivity](token-counts-cl100k.json)

## Cost interpretation (illustrative, not observed billing)

More inexpensive-model tokens need not increase total dollars. For the recorded context, the warm-route input saving is 223 primary text tokens, while Jev's configured-rate cost was $0.000113946. Ignoring other differences, it breaks even when primary input costs more than approximately **$0.511 per million tokens** and no incremental instruction charge is incurred.

For example, at a purely hypothetical primary input rate of **$3/M**, baseline input is **$0.003948** and warm routed input plus Jev is **$0.003392946**: approximately **14.06% lower**, after the Jev charge. Counting one 923-token skill load instead gives **$0.006161946**, approximately **56.08% higher** on these tiny cases. These are arithmetic scenarios, not the selected chat model's current price or a measured cost reduction. Real output, tool costs, cached-input rates, repeated-history charges and correctness/correction work must be measured.

[Reproducible cost assumptions](cost-example.json). The 53.19% cold input-token increase came from added **primary-model instructions**, not from adding Jev's differently priced token usage. A skill already present in context may still incur repeated or cached input charges on subsequent requests; warm accounting must be verified by the host.

The v0.2.0 portability instructions change entrypoint length. Recorded results above remain historical; running the counter against a newer revision measures its current instruction overhead.
