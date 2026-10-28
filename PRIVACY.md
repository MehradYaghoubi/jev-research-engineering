# Privacy and data handling

This repository distributes local instructions and Python scripts; it does not provide a hosted inference or telemetry service operated by the repository author.

When the user or agent invokes a live decision command, the configured endpoint receives the supplied task state/questions and the configured provider credential in an authentication header. Context selection sends candidate summaries. Requests may contain source excerpts, research passages or other task information the operator includes. Review and minimize that data, obey repository restrictions and exclude secrets and unrelated personal information. Full chat history and whole repositories are not required by the helper.

Endpoint, model, API contract and credential variable are configurable. The selected provider's privacy, retention, billing and processing terms apply to live calls. This project cannot promise third-party retention or training policies. Local inference remains under the operator's control; hosted inference crosses the provider trust boundary.

Private configuration and the SQLite usage ledger live outside the installed skill. The ledger stores request hashes, dates, status, reported token counts and cost estimates, not request text or API keys. Windows optional key setup stores user-bound DPAPI ciphertext; environment secrets are another option. The operator can manage/remove private data at the configured private directory and revoke keys with the provider. Do not put those files in a shared repository.

The helper permits at most three attempts for transient failures, records each attempt with unknown failed-request billing preserved, has no background collector and contains no installation lifecycle hooks. Offline tests and dry-run do not send provider requests. The selected agent host, package manager and Skills CLI are separate software with their own behavior and optional installation telemetry; this notice does not override their policies.

The operator must check source material and permissions before a live request. Public reports should contain non-sensitive test data and aggregate measurements, not private prompts, keys, account identifiers or raw logs. Security/privacy questions can be reported through this repository's GitHub issues without including credentials or sensitive source material.

The MIT license governs this software. Provider accounts and services have their own terms. This description is a notice of the implemented behavior, not a guarantee of third-party service behavior.
