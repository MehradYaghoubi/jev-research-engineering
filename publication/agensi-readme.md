# Research & Engineering Router

One free MIT-licensed skill for coding and research. Its installation identifier is `jev-research-engineering`; Jev is optional. Your chosen main model remains responsible for reasoning, implementation and verification. A configured inexpensive model can screen large approved evidence sets before main-model intake. Small, obvious tasks should skip routing.

## Install

Keep this extracted folder intact and install it through your agent's SKILL.md loader. Full helper operation requires Python 3.10+, file access and permission to run Python. No pip packages, virtual environment or downloaded dependency are required. An instruction-only MCP host that cannot expose these helper files cannot run the screening workflow; use the direct installation instead.

Project-local alternative: `npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering`

For a global installation add `--global`. Choose one scope per agent. See [agent-specific instructions](references/installation.md).

## How to use it

1. Follow [setup](references/setup.md) to copy the example profile for your chosen provider into private storage outside this skill folder. Set the endpoint/model and supply only that provider's own credential using its configured variable or optional Windows DPAPI setup.
2. Run `python scripts/jev_gate.py --config <your-private-profile.json> status` to inspect configuration without a paid inference request. Do not paste credentials into chat or this package.
3. Invoke through your host: Codex `$jev-research-engineering`, standalone Claude Code `/jev-research-engineering`, or Pi `/skill:jev-research-engineering`. Ask for the coding or research task; no second skill is needed.

For direct helper integration, start with `python scripts/prepare_context.py --corpus examples/evidence-corpus.json --config references/config.json --audit <new-local-audit.json>`. This small example skips the provider. Larger approved corpora may make billable requests. The helper must run before broad evidence intake; it cannot remove context already read by the main model.

Native System One, OpenAI-compatible Chat Completions JSON and Anthropic Messages interfaces are documented in [access methods](references/access.md). Hosted provider fees are separate from this free skill. GapGPT has live verification; not every agent/provider combination has been live-tested.

## Measured results

These historical results cover two authored evidence-intake tasks with three paired repetitions each. The coding case is a **code audit**, not a complete implementation benchmark. Counted tokens are main-model input including cached input plus output.

| Task | Primary-token reduction |
| --- | ---: |
| Code audit | 13.96% |
| Research | 6.41% |
| Combined across the six pairs | 10.20% |

Mean complete-process time increased **20.42%**. All six assisted outcomes passed the authored checks. These results do not guarantee the same improvement on new tasks or reduce a fixed subscription bill. See the [full measured report](benchmarks/retry-confirmation-results.md).

## Watch the installation guide

The silent captioned [installation video and full source](https://github.com/MehradYaghoubi/jev-research-engineering#watch-the-installation-guide) are hosted on GitHub. Binary media and development tests are deliberately outside this lightweight distribution.

Thank you for trying the skill. If it helps, consider starring the [original repository](https://github.com/MehradYaghoubi/jev-research-engineering) or sharing feedback. A star is optional. See SKILL.md for exact runtime permissions and data flow.
