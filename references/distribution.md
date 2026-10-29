# Distribution status

The public source of truth is [MehradYaghoubi/jev-research-engineering](https://github.com/MehradYaghoubi/jev-research-engineering). The skill identifier stays `jev-research-engineering`; its current title is Research & Engineering Router and Jev is optional.

| Channel | Method | Status |
| --- | --- | --- |
| GitHub | Public source plus versioned release ZIP and checksums | Public source; versioned release ZIP and checksums linked below |
| Claude Code | Public self-hosted marketplace and plugin manifests | Both manifests passed native Claude validation; official Anthropic directory acceptance not claimed |
| Pi | Git-installable package with explicit pi.skills metadata | Package prepared and npm pack checked; npm/Pi gallery publication requires registry authentication |
| Skills.sh | Real installation using the official Skills CLI | Public listing verified on 2026-10-28; its Snyk audit still references the older optional tokenizer dependency pending refresh |
| UseThisSkill / nodegenie list | Submit the public source through its Add a skill repository issue template | Not submitted: both connected integration and existing account API returned HTTP 403; browser form did not load usable controls |
| SkillsMP | Public GitHub SKILL.md source eligible for its catalog crawl | Listing not verified; no direct submission endpoint confirmed |
| Agensi | Free, non-exclusive listing linked to the MIT-licensed GitHub source | [Free public listing](https://www.agensi.io/skills/research-engineering-router) verified on 2026-10-29 after lightweight resubmission |
| VoltAgent awesome-agent-skills | PR after community adoption | Not submitted: contribution rules exclude brand-new unproven skills |

Sources: [Skills.sh discovery FAQ](https://skills.sh/docs/faq), [UseThisSkill submission template](https://github.com/nodegenie/awesome-agent-skills/blob/main/.github/ISSUE_TEMPLATE/add-skill-repo.yml), [SkillsMP about](https://skillsmp.com/about), [VoltAgent contribution criteria](https://github.com/VoltAgent/awesome-agent-skills/blob/main/CONTRIBUTING.md).

An installation is not approval, a submission is not acceptance, and a crawlable source is not a confirmed listing. No stars, downloads or users were purchased or artificially generated. This project makes no net cost-saving claim from its synthetic results.

## Prepared submission

The [official issue form](https://github.com/nodegenie/awesome-agent-skills/issues/new?template=add-skill-repo.yml) accepts the repository URL, MIT license, and a one/two-sentence description. Suggested description: Research & Engineering Router is a Codex-tested, provider-configurable skill for evidence triage, Clean Code/OOP, missing-integration checks and reproducible research. It supports native System One and JSON-capable OpenAI-compatible chat models, while the selected chat model owns reasoning and implementation.

Disclose that this project and submission were authored with Codex, and link the token report including its negative cold-start result. Publication/indexing remains pending; no external issue was created.

## v0.2.0 portability

The Skills CLI all-agent installer was exercised in an isolated project with telemetry disabled: 53 unique skill-target directories, semantic instruction integrity and required helper/config files verified. This is an installation test across CLI-supported profiles, not proof of every agent runtime. A real Codex model run fixed a missing route connection; all three behavioral checks passed independently. Native model execution is recorded in [the runtime report](../benchmarks/agent-runtime.json). Download the versioned release and verify its checksum before manual installation.

Versioned release: [v0.2.0](https://github.com/MehradYaghoubi/jev-research-engineering/releases/tag/v0.2.0). The release publishes source and a portable ZIP worldwide; it does not imply acceptance into an official Anthropic directory, npm, Pi gallery, SkillsMP or another curated market.

## v0.2.1 setup and official submission packet

[Release v0.2.1](https://github.com/MehradYaghoubi/jev-research-engineering/releases/tag/v0.2.1) includes complete connection setup, a dedicated OpenAI directory ZIP, privacy notice and [two real A/B pairs](../benchmarks/real-agent-ab.md). The owner signed in, but the OpenAI portal requires verified developer identity before upload or draft creation; no official draft or review submission exists. See [submission steps and blockers](official-submission.md).

## v0.3.0 atomic screening and bounded retries

[Release v0.3.0](https://github.com/MehradYaghoubi/jev-research-engineering/releases/tag/v0.3.0) publishes atomic evidence screening, transient retries and the [confirmation report](../benchmarks/retry-confirmation-results.md). The limited code-audit/research evaluation measured **10.20% fewer primary-model tokens** and **20.42% longer whole-process time**, with all six assisted quality checks passed. Code audit and research individually measured 13.96% and 6.41% token reduction. This is an experimental release, not a universal savings claim or official directory approval.

## v0.3.1 dependency removal

The [Snyk report](https://skills.sh/mehradyaghoubi/jev-research-engineering/jev-research-engineering/security/snyk), analyzed 2026-10-27 and checked 2026-10-28, flags W012 for the optional historical tokenizer package. v0.3.1 removes the counter, its package requirement, installation commands and package-manifest entry. Runtime helpers and offline tests use only the Python standard library. Archived results retain their original provenance; the routing algorithm and measured v0.3.0 results are unchanged. This removes the reported dependency rather than suppressing the audit.

The listing and audit can retain an older snapshot. A Skills maintainer [states that a new installation triggers a rescan](https://github.com/vercel-labs/skills/issues/575); a new install is not proof that the public audit has refreshed. Check the audit date and current finding before claiming W012 has cleared. No fresh Snyk PASS is claimed here.

## Agensi packaging correction, 2026-10-29

The first 70-file submission was rejected after a 60/100 scan. The reported test line was a deliberately invalid corpus fixture, not an active credential. The corrected Agensi distribution omits development tests/runners, installer tooling, plugin manifests and binary media. It contains 28 files in a 54,523-byte ZIP; the largest file is 28,838 bytes. All four runtime files exactly match the original stable submission at `074ba23`; unpublished optimization changes are excluded.

The submitted SKILL.md declares the approved evidence boundary, configured endpoint and authentication variable, optional private Windows DPAPI storage, configuration writes and lack of runtime telemetry. Setup-path, credential-name and documentation-URL findings are explained for manual review rather than disguising required behavior. The full video and test sources remain linked on GitHub. Forty-seven stable offline tests and the unpacked zero-provider-call example passed.

Use `python scripts/build_submission.py --target agensi --source <reviewed-tree> --output <new-zip>` with the Agensi publication templates present in the reviewed tree. The builder uses an explicit runtime allowlist, checks count/size and obvious credential patterns, redirects omitted documentation links to public source, and refuses to overwrite an archive. The corrected free listing was initially Pending Review after resubmission. On 2026-10-29 the public creator page and [skill listing](https://www.agensi.io/skills/research-engineering-router) confirmed it was available for free. This does not establish universal security or a new performance result.

The GitHub repository retains the complete video, captions, test suite and benchmark history. Only the marketplace ZIP uses the lean allowlist. The GitHub skill links the permission disclosure rather than loading it for every task. Rebuilding from another reviewed revision can change archive bytes and sizes; the counts above describe the originally resubmitted archive.
