# Atomic confirmation before retry authorization

This cycle completed 14 reader runs. Full intake and routed answers each passed 6/6 quality cases. Primary tokens were 178,806 versus 160,724: an observed 10.1126% reduction. The lexical competitor failed both quality cases. No trial was removed.

One routed primitive-research trial fell back after a timeout-like provider failure; its preparation took 27.443 seconds and decision usage was unknown. The preregistered completeness gate therefore **rejects this cycle as a confirmed savings result**. A correct fallback answer does not recover missing auxiliary telemetry. The narrow aggregate margin also does not establish stable performance.

End-to-end task-duration sums were 415.790 seconds full versus 493.952 seconds routed. These are sums of individual complete task latencies, including preprocessing, fresh decision calls and independent answer checks, not concurrent batch makespan. Speed was not an acceptance target after the user's clarification.

The user subsequently authorized bounded retries for transient connectivity/provider errors. That prospective policy change does not alter this cycle's original results. The next confirmation keeps the same frozen corpora and factual criteria, includes retry time/charges, and distinguishes the precisely measurable primary-token target from potentially unknown failed decision usage. No rescore or selective rerun rescues this old cycle.

[Structured summary](atomic-results.json) · [Original plan](atomic-plan.md). Complete local traces remain in `.agent-qa/atomic-confirmation/`.
