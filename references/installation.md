# Install across agents

This is a portable Agent Skills directory: standard `SKILL.md`, relative references and standard-library Python helpers. It does not require Codex tools, a particular model, an installed Ponytail skill, Node runtime inside the agent, or a supervisor. Python 3.10+ and permission to read files/run helpers are needed for full API-assisted operation. Choose one installation method per agent to avoid duplicate skill names.

## Shared installer

```bash
# Interactive: choose the agents you use
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g

# Explicit examples
npx skills add MehradYaghoubi/jev-research-engineering --skill jev-research-engineering -g -a codex claude-code pi opencode
```

The official Skills CLI supports these profiles and many others. Use `-a cursor`, `-a gemini-cli`, `-a github-copilot`, etc. for a specific supported profile; use `--copy` if symlinks are unavailable. `--all` selects every skill and agent profile; avoid it unless you actually want that scope. Global installs affect the user profile; omit `-g` for project-local installation. The CLI requires its documented Node.js version, but the installed Python helper does not depend on Node.

## Agent-specific loading

| Agent | Load/invoke | Manual global location |
| --- | --- | --- |
| Codex | `$jev-research-engineering` | `~/.agents/skills/jev-research-engineering/` or its configured skills path |
| Claude Code, standalone skill | `/jev-research-engineering` | `~/.claude/skills/jev-research-engineering/` |
| Pi | `/skill:jev-research-engineering` | `~/.agents/skills/jev-research-engineering/` (shared skills supported by Pi) |
| OpenCode | Ask the agent to load `jev-research-engineering` with its skill tool | `~/.config/opencode/skills/jev-research-engineering/` or shared `~/.agents/skills/` |
| Cursor, Gemini CLI, Copilot and other supported agents | Use that host's skill loader and permissions | Let the Skills CLI choose the supported path |

A bare VS Code editor is not an agent. For VS Code, choose the installed agent extension (such as Copilot, Cline or Roo Code) and its corresponding Skills CLI profile. If by “code” you mean OpenCode, use `-a opencode`; if Codex, use `-a codex`.

Paths above follow official current documentation. Agent versions, enterprise policies and host permissions can change discovery behavior. Reload or restart a host after install. Never claim that filesystem installation proves model behavior or access to shell tools.

## Pi-native package

The repository's `package.json` declares `pi.skills: ["./"]`; there are no JavaScript dependencies or install hooks.

```bash
pi install git:github.com/MehradYaghoubi/jev-research-engineering@v0.2.1
```

This is a git-backed Pi package. It does not require npm registry publication. Do not advertise the scoped npm name as installable from npm until it is actually published there. `pi-package` metadata prepares it for Pi packaging, but does not itself confirm gallery indexing.

## Claude Code marketplace

The repository also provides a public, self-hosted Claude plugin catalog:

```text
/plugin marketplace add MehradYaghoubi/jev-research-engineering
/plugin install research-engineering-router@mehrad-research-tools
```

The plugin exposes the root skill; Claude namespaces plugin-provided commands, so use the command shown in its skills menu (normally `/research-engineering-router:jev-research-engineering`). For the plain `/jev-research-engineering` command choose standalone skill installation instead. A self-hosted catalog is not acceptance into Anthropic's official directory.

## Manual / download install

Download the GitHub release ZIP and verify its SHA256 against the accompanying checksum. Extract the `jev-research-engineering` folder into the selected host's skills directory, keeping `SKILL.md`, `scripts/` and `references/` together. Do not flatten or copy only SKILL.md: relative links and scripts need the full folder. Run the helper from its installation folder or use an absolute script path.

Configure a private provider profile once as explained in [access methods](access.md). Configuration and credentials stay outside installation folders, so copying/updating the skill does not erase them. Headless hosts use environment secrets; Windows-only DPAPI configuration is optional. A host without shell/file access can only apply the written research/engineering guidance and cannot run API-assisted triage; disclose this degraded mode.

## Verification scope

[Compatibility results](../benchmarks/agent-installation.json) distinguish installer/file checks, native manifest validation and real agent task execution. No paid model calls are needed for installer tests. Only explicitly recorded runtimes have been exercised; the standard format cannot guarantee support in every existing or future agent.

Official references: [Skills CLI agent profiles](https://github.com/vercel-labs/skills/blob/main/docs/agents.md), [Pi skills](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md), [Pi packages](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md), [Claude skills](https://code.claude.com/docs/en/skills), [Claude plugin paths](https://code.claude.com/docs/en/plugins-reference), [OpenCode skills](https://opencode.ai/docs/skills/).
