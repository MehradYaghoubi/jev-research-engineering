# Installation walkthrough

An authored, silent PowerShell walkthrough with real CLI excerpts. Both Local (project) and Global (user) installation are explained as alternatives. There is no audio track. This is not an unedited desktop recording. Setup/credential scenes and the Codex prompt are instructional examples, labelled on screen. No coding-agent response is claimed. Network and installer wait times are omitted; each scene includes a reading pause.

## Chapters and on-screen explanations

### 00:00:00.000 — One skill. Your main model stays in charge.

This guide installs Research and Engineering Router for Codex on Windows. Your main model stays in charge. The skill is free, while provider API charges may apply.

### 00:00:07.000 — 1. Check the prerequisites

Start in your project folder. You need Node for the Skills installer, and Python three point ten or newer for the helpers. The helper runtime needs no third party Python packages.

### 00:00:16.000 — 2. Local install: this project only

Choose Local for this project only. This is the actual local installation, with output shortened for readability.

### 00:00:29.000 — 3. Global install: all your projects

Choose Global for all projects under your user account. Add --global or -g. You do not need to run both installation commands.

### 00:00:41.000 — 4. Open the installed skill folder

Open the folder matching your installation scope. Use the project path for Local, or your user profile path for Global.

### 00:00:53.000 — 5. Choose a matching provider profile

Jev is optional. Choose a provider profile with a matching endpoint, model and protocol. This demonstration uses an existing GapGPT profile. Other profiles are documented, but are not live tested in this video.

### 00:01:04.000 — 6. New users: create private configuration

New users create a private configuration outside the skill folder. These are setup instructions, not commands executed during this recording. Keep an existing working configuration. For another provider, copy its profile and replace placeholder settings.

### 00:01:21.000 — 7. Enter your provider key privately

On Windows, configure prompts for the provider key without echoing it, and stores encrypted credentials outside the skill. Secret input is not recorded here. Headless hosts can inject the configured environment variable instead.

### 00:01:32.000 — 8. Inspect configuration, without a network call

Status confirms the selected route and credential availability without sending a model request. These are selected fields from the real run. Credential ready does not prove connectivity.

### 00:01:42.000 — 9. Validate a request offline

Dry run checks the request without sending it. The real output says sent false. This step is useful before a potentially billable connection test.

### 00:01:52.000 — 10. Make one live connection test

Remove dry run to make the live call. Our real request succeeded on the first attempt and returned a refund score of zero point nine nine. This verifies the connection, not token savings. Provider charges may apply.

### 00:02:05.000 — 11. Give Codex the actual task

Now mention the skill in Codex and describe your real task. Reload the agent if necessary. This is an example prompt, not a recorded coding result. The skill screens large evidence sets and skips routing for small tasks.

### 00:02:19.000 — What earlier measurements showed

Earlier matched comparisons recorded thirteen point nine six percent fewer main model tokens for code audit, and six point four one percent fewer for research. Overall task time increased twenty point four two percent. These were two authored tasks, not a guarantee for every workload.

### 00:02:33.000 — Try it. Share what you learn.

The repository has provider setup, examples and the full recorded results. Try a real task and share feedback. If the skill helps your work, consider giving it a GitHub star. Thank you.

## Verification

Project installation and the native GapGPT connection succeeded on 2026-10-28. Live request: 287 input tokens, 20 output tokens, one attempt. Other providers are documented examples, not live-tested by this video. API cost is separate from the free MIT-licensed skill.

The 13.96% code-audit reduction, 6.41% research reduction and 20.42% longer overall time come from the earlier two-task, three-repetition experiment. This video is not a new savings benchmark.

Private setup is outside the installed skill. Secrets and machine-specific paths are not displayed. The audio track has been removed; all explanations are on screen and in the subtitle file.

[Full provider setup](setup.md) · [Recorded performance report](../benchmarks/retry-confirmation-results.md)
