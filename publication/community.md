# Community sharing kit

Draft copy for human publication. No email or social post has been sent by preparing this file. Keep the skill free, retain MIT licensing and link to the original GitHub source. Model-provider API charges are separate. Request stars only from people who find it useful.

## LinkedIn post

How much of your AI coding agent's context is spent reading material it never uses?

I built Research & Engineering Router to explore that question. It's a free, open-source skill for coding and research workflows in Codex, Claude Code, Pi, OpenCode and compatible agents.

The idea is simple: let a cheaper model screen a large set of evidence before the main model reads it. The main model still owns reasoning, code changes, research conclusions and verification. Small tasks skip the extra call.

The workflow also asks the agent to check missing integrations—like a route that was written but never registered—and to preserve sources and conflicting evidence during research.

In a limited evaluation of two code-audit/research tasks, repeated three times:

- Primary-model tokens fell by 10.20% overall.
- Whole-process time increased by 20.42%.
- All six assisted answers passed the same quality checks.

That's a trade-off, not a promise: research alone was below 10%, and this was an evidence-intake test, not a full autonomous coding benchmark. Lower token use also does not mean a lower fixed subscription bill.

Jev is optional. You can configure a compatible provider or local model. The skill is MIT-licensed and free; provider API charges may apply.

I'd love feedback from people working on larger codebases or research workflows. If you try it and find it useful, a GitHub star or a share would mean a lot. Thank you!

Source, setup and measured results:
https://github.com/MehradYaghoubi/jev-research-engineering

#OpenSource #AIAgents #Codex #ClaudeCode #ContextEngineering

## Instagram story — one slide

I built a free AI agent skill 🚀

Research & Engineering Router
Smarter evidence screening for code + research.

Limited test: 10.20% fewer main-model tokens.
Trade-off: 20.42% longer total time.

Open source · MIT · Bring your own provider
API charges may apply.

Try it. If it helps, leave a ⭐ on GitHub.
Thank you for the support!

Link sticker: https://github.com/MehradYaghoubi/jev-research-engineering

## Free marketplace listing

Title: Research & Engineering Router — Evidence Screening for Coding and Research

Price: Free / $0. No paid tier or subscription requested.

Description: A free MIT-licensed skill that helps your coding agent select relevant files and research sources before its main model reads a large evidence set. Your main model remains in charge of reasoning, implementation and verification. Includes guidance for Clean Code, meaningful OOP, missing integration checks and source-based research. Jev is optional; choose a compatible decision-model provider. Python 3.10+, file/shell access and private provider setup are needed for API-assisted routing. Provider charges are separate.

Measured trade-off: A limited six-pair evidence-intake evaluation recorded 10.20% fewer primary-model tokens and 20.42% longer whole-process time, with six of six assisted quality checks passed. Results are not a guarantee for other tasks or agents.

Source and installation: https://github.com/MehradYaghoubi/jev-research-engineering

Support: If the skill helps your work, thank you! Consider starring the original GitHub repository or sharing feedback. A star is never required.

Distribution note: Preserve the complete scripts/references layout and MIT notice. Do not describe a remote instruction-only listing as fully functional API-assisted routing unless that host can access and execute the helper files.

## Distribution checklist

| Channel | Useful next step | What counts as success |
| --- | --- | --- |
| GitHub | Clear README, source link and optional star invitation | Published source and readable setup/results |
| Skills.sh | Commit official page metadata and update a real installation | Current public page verified; security re-audit verified separately |
| Agensi | Confirm free listing, source attribution and helper-file support | A public free listing, not just an invitation or draft |
| LinkedIn / Instagram | Share the drafts above with the GitHub link | User-approved publication; no fabricated endorsements or metrics |
| Technical communities | Share a concrete demo where community rules permit | Useful discussion and real feedback, not repeated promotional spam |

Agensi's [free catalog](https://www.agensi.io/skills/free) and [creator page](https://www.agensi.io/sell) were checked on 2026-10-28. An invitation is not a listing or endorsement; the email's traffic figure has not been independently verified. Skills.sh's [page customization guide](https://www.skills.sh/docs/customize) describes metadata refresh after a genuine CLI installation and warns that page caches may delay changes.
