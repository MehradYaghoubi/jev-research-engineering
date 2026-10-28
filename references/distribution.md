# Distribution status

The public source of truth is [MehradYaghoubi/jev-research-engineering](https://github.com/MehradYaghoubi/jev-research-engineering). The skill identifier stays `jev-research-engineering`; its current title is Research & Engineering Router and Jev is optional.

| Channel | Method | Status |
| --- | --- | --- |
| GitHub | Public source plus versioned release ZIP and checksums | Public source; versioned release ZIP and checksums at the v0.2.1 release link |
| Claude Code | Public self-hosted marketplace and plugin manifests | Both manifests passed native Claude validation; official Anthropic directory acceptance not claimed |
| Pi | Git-installable package with explicit pi.skills metadata | Package prepared and npm pack checked; npm/Pi gallery publication requires registry authentication |
| Skills.sh | Real installation using the official Skills CLI | One real Codex install completed using Skills CLI 1.7.4; public listing not verified |
| UseThisSkill / nodegenie list | Submit the public source through its Add a skill repository issue template | Not submitted: both connected integration and existing account API returned HTTP 403; browser form did not load usable controls |
| SkillsMP | Public GitHub SKILL.md source eligible for its catalog crawl | Listing not verified; no direct submission endpoint confirmed |
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
