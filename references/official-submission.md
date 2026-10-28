# Official directory submission packet

A prepared package, an uploaded draft, a submitted review and a published listing are different states. Only portal evidence can confirm the later states.

## OpenAI public Plugins Directory

Official sources: [submission](https://developers.openai.com/plugins/deploy/submission), [package format](https://developers.openai.com/plugins/build/plugins), [desktop-only skills](https://developers.openai.com/plugins/deploy/desktop-only).

Prepared source: `publication/openai-plugin.json`, with Agent Plugins 1.0.0 identity and OpenAI listing metadata. It declares `requires_local_executor: true` because the helper executes local Python. The builder creates root `plugin.json` and `skills/jev-research-engineering/`, preserving bundled relative paths. It contains no MCP server, app reference, lifecycle hook or credential. The root manifest passed the public Agent Plugins JSON schema; OpenAI extension fields and directory acceptance still require portal validation.

```bash
python scripts/build_submission.py --output ../release-artifacts/research-engineering-router-openai-v0.3.1.zip
```

Upload this dedicated ZIP, not the original source-layout release ZIP. The factual [privacy notice](../PRIVACY.md) describes local storage and configured-provider data transmission; software terms link to the MIT license. Confirm publisher details and URLs before submitting.

Owner steps:

1. Sign in at [OpenAI Platform → Plugins](https://platform.openai.com/plugins).
2. Select the owning organization/project. An owner or Apps Management Write member can submit; complete publishing identity verification if required.
3. Upload the ZIP as a desktop skills-only plugin. Check imported identity, capabilities, listing/category, privacy/terms links and local-execution flag. Resolve automated findings.
4. Follow the portal review steps. Supply actual requested test evidence; do not invent reviewer credentials, demo URLs or savings claims.
5. The publisher reviews the final policy attestations and submits. Approval is external; publish only after approval.

Current access evidence: the account owner signed in successfully. Upload was blocked by the portal message: "You need a verified developer identity before you can create or upload a plugin." The portal opened Organization settings → Verifications, offering Individual or Business verification. The account owner must complete the appropriate identity flow directly. No ZIP upload, draft, review submission or official listing has been created. Passwords, authenticator codes and identity documents belong in the official verification flow, not chat.

## Anthropic Directory

Official sources: [plugin publication](https://code.claude.com/docs/en/plugins/publish), [submit a plugin](https://claude.com/docs/plugins/submit), [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).

Prepared: public `.claude-plugin/plugin.json`, self-hosted marketplace, README, MIT license, privacy notice and tests. Plugin and marketplace pass strict native validation. These checks do not replace the portal's directory validation/security scan.

Use [claude.ai/directory/manage](https://claude.ai/directory/manage) with an eligible paid plan/role, connect the public GitHub source and run Validate. Account eligibility and final review remain external. `claude-plugins-official` is a separate partner-managed marketplace, not the destination of a generic community PR or the directory portal. No official listing is claimed.

## Pi / npm

[Pi's package catalog](https://pi.dev/packages) indexes npm packages. `pi-package` metadata and packaging checks are already present, while Git installation works independently. npm authentication is absent, so registry publication and Pi catalog listing are incomplete. Verify the actual account's scope/name before publishing. Complete npm login/2FA directly; never paste tokens or OTPs into chat.

## Skills.sh and community lists

Skills.sh discovery follows genuine CLI installs. Installation tests disable telemetry to avoid manufactured popularity. Third-party lists have separate contribution rules; earlier issue writes returned 403. No blocked write is described as a successful submission.

## Review evidence

[Agent installation](../benchmarks/agent-installation.json) · [Actual Codex task](../benchmarks/agent-runtime.json) · [Historical token results and negative overhead finding](../benchmarks/token-counts.md).

[Real primary-agent A/B evidence](../benchmarks/real-agent-ab.md): two pairs increased total primary-model tokens 42.17%; all four outputs passed independent acceptance and suite checks. No generalized savings claim is supported.
