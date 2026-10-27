# Jev Research & Engineering

A Codex skill that routes bounded decisions and evidence triage to Jev while keeping your selected chat model responsible for reasoning, research synthesis, and code.

**Goal:** reduce total workflow cost by giving the main model less irrelevant context to process. **Status:** early experimental release; live connectivity and synthetic triage are tested, but real main-model cost savings are not established.

## How it works

1. Deterministic search/indexing produces compact candidate summaries without returning every source body to chat.
2. Jev ranks relevance or makes a narrow typed decision over those summaries.
3. The main model reads selected evidence, required dependencies, and the strongest excluded alternative that could matter.
4. It implements or synthesizes the result and runs the appropriate acceptance checks.

No independent supervisor, model switching, automatic retries, or extra runtime dependencies. Compatible with Ponytail full. Jev returns typed decisions; it does not write the implementation or research report. Routing adds a cost and should be skipped for simple tasks.

## Engineering and research behavior

- **Clean Code and OOP:** cohesive responsibilities, encapsulated invariants, explicit dependencies, composition, and the existing architecture. No ceremonial classes or speculative frameworks.
- **Missing connections:** compare the required trigger-to-result path with actual route registration, DI, events, workers, config, permissions, persistence, exports and frontend/API mappings. Existing-reference graphs alone cannot prove a never-written edge exists. Verify behavior through a real entry-point test.
- **Research:** primary sources, provenance, contrary evidence, freshness, and separation of observations from inference. Jev cannot create valid citations or verify unread sources.
- **R&D:** explicit hypothesis, baseline, discriminating experiment, measurable success, reproducibility, negative results, and a stopping condition.
- **Budget and privacy:** bounded requests, a shared estimated daily ledger, encrypted Windows credentials or runtime secrets, required-context retention and visible fallback.

## Install in Codex

Requires Python 3.10+ and Git. Python runtime code uses only the standard library.

```bash
git clone https://github.com/MehradYaghoubi/jev-research-engineering.git
```

Copy the cloned folder to your Codex skills directory (`~/.codex/skills/jev-research-engineering`, or the corresponding skills directory under your configured Codex home). Do not overwrite an existing installation without preserving its private configuration. Invoke `$jev-research-engineering`; if a running client has not discovered it yet, reopen the chat/client.

Suggested prompt:

> Use $jev-research-engineering with Ponytail full. Triage relevant evidence before loading full files, preserve required dependencies, check missing wiring, and verify the smallest complete solution. Report actual usage without promising savings.

## Configure once

From the installed skill folder:

```bash
python scripts/jev_gate.py configure
python scripts/jev_gate.py status
```

Windows setup uses a non-echoing prompt and user-bound DPAPI. On Linux/macOS or cloud runners, inject `JEV_API_KEY` from a secret manager. Never commit a key. Configure endpoint/model/prices in a private JSON config and point `JEV_GATE_CONFIG` or `--config` to it. The public defaults use GapGPT; no credential is bundled. `private_dir` defaults to `~/.jev-research-engineering`, outside the repository.

[Access methods](references/access.md) covers local execution, cloud runners, direct TypeSafe, external gateways, and private compatible servers. Local execution does not imply local Jev inference. [The protocol](references/protocol.md) documents the wire contract and accounting.

## Select context or make a decision

```bash
python scripts/select_context.py --manifest examples/context-manifest.json
python scripts/jev_gate.py decide --request examples/manifest-decision.json --dry-run
python scripts/jev_gate.py decide --request examples/manifest-decision.json
python scripts/jev_gate.py usage
```

The selector emits IDs and usage rather than full evidence bodies. Keep the ID-to-source mapping locally and retrieve the selected sources afterward. Mark essential candidates required. See [cost routing](references/cost-routing.md) for manifests, failure behavior and the comparison method. `--dry-run` does not call the provider; `decide` without it and nontrivial selection are billable.

## Tests and first evaluation

```bash
python -m unittest discover -s tests -v
python scripts/jev_gate.py self-test
python scripts/benchmark_triage.py --live --output benchmarks/first-run.json
```

The first two commands are offline. The benchmark makes up to three provider calls on synthetic tasks: a missing HTTP registration, a missing worker subscription, and a research comparison with data leakage. Expected evidence IDs are frozen in the fixture before the call and never sent to Jev. It reports critical-evidence recall, delivered-context bytes including a verification candidate and routing-output overhead, elapsed time, actual provider usage, and configured-rate Jev cost. It does not run a second expensive main model or measure this chat's billing. [First-run results](benchmarks/first-run.md) state the observed outcome and limits.

Compare real end-to-end quality, primary-model billed input/output and total cost before claiming savings. Context-byte reduction is only a proxy. Results on three synthetic cases do not establish generalization or safe autonomous routing.

## Limits

The task call limit is agent-enforced, while the helper enforces per-request size and an estimated daily ledger. The ledger cannot cap billing in unrelated software or other machines. Source privacy review remains the operator's responsibility. The permissive relevance cutoff is not calibrated; missed context can harm quality. Fallback retains all candidates instead of forcing a reduction. No networked test runs in CI by default.

## فارسی

هدف این اسکیل کاهش هزینهٔ کل از طریق سپردن تصمیم‌های محدود به Jev و کاهش زمینهٔ غیرضروری مدل اصلی است. مدل اصلی مسئول تحقیق، طراحی، کدنویسی و آزمون می‌ماند. اصول Clean Code، استفادهٔ معنادار از OOP و بررسی اتصال‌هایی که باید وجود داشته باشند اما پیاده نشده‌اند، جزو روند کار هستند. اتصال موفق و کاهش حجم متن به‌تنهایی اثبات صرفه‌جویی واقعی نیستند. کلید API در ریپوی عمومی قرار ندارد.

## License

MIT. Independent community skill; not affiliated with TypeSafe, GapGPT, OpenAI or Vercel. Provider models, services and terms are separate from this repository's license.
