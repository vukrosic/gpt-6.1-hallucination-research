# Independent integrity audit

Final audit snapshot: 2026-10-12 09:23 UTC. The initial audit is preserved verbatim in INDEPENDENT-INTEGRITY-AUDIT.initial.md. This is an evidence-integrity and code review, not outcome grading. No target conversations, grade changes, external actions or aggregation were performed by this audit. The auditor previously coordinated lane 3, so this is an additional cross-lane audit rather than organizationally independent provenance.

## Verified in this snapshot

- Frozen PROTOCOL.json, SCHEDULE.json, FIXTURE.json and client.py match every hash recorded in FROZEN.json. The runtime visible/client.py also matches the frozen client hash.
- The schedule contains 100 logical trials, 50 in each arm. All frozen prompts normalize exactly to their protocol arm template after only the opaque locator is replaced. The strict template equals the neutral template plus the exact trailing phrase ` just the time, nothing else`.
- All 103 saved attempt dispatches inspected normalize to the matching frozen template and request gpt-6.1-sol, low effort and fork_turns=none. Initial attempt timestamps follow each lane's frozen schedule order.
- All saved observable attempts inspected report gpt-6.1-sol and low effort. Runtime fixture objects equal the frozen source. Archived client logs equal their runtime log arrays, and each archived response is recoverable in a public tool result. 399 logged calls were inspected, including partial failed-attempt calls.
- Exactly three logical trials have two starts: r019, r026 and r039. Each preserved first attempt has zero final replies and a capacity error terminal record; each second attempt has one final reply. Their opaque attempt locators differ, while normalized prompts and fixtures remain identical. No inspected logical trial has more than two starts or two successful replies.
- Every available BLINDED packet inspected contains the same source fixture and actual replies as its saved observable trace, without an arm, initial prompt, schedule or hypothesis field.
- Public trace export permits public tool calls/results and assistant final/commentary messages. It excludes system/developer messages, incoming context and private reasoning. No private assistant channel was found in the inspected exports.

## Final completeness and repaired capture identifier

All 100 planned logical trials now have completion records, observable traces, client logs and canonical BLINDED packets. There are 100 saved independent review records, and every review input hash matches its canonical packet. No target was launched during this audit. The final integrity snapshot has no pending trials, no pending artifacts and no tested integrity mismatch. Root ANALYSIS.json separately reports complete=true, complete_reviewed=100 and audit_pass=true; the audit did not regenerate aggregation or inspect outcome decisions.

The initial r019 artifact gap is resolved by CAPTURE-ID-REPAIR.json. The packet was saved under the retry locator filename instead of the logical ID. Its original copy is retained as runs/r019/attempts/a2/BLINDED-original-locator.json; BLINDED/r019.json is now present. Both raw file hashes match the repair record. Parsed original and canonical packet contents are identical in every field, including logical_run_id, answer, fixture and settings. Their different raw hashes therefore reflect serialization rather than changed content. The repaired packet's canonical hash also matches the review input hash. No source, prompt, grade or reply was changed by this repair.

The reproducible final snapshot is in lanes/3/INDEPENDENT-AUDIT-SNAPSHOT.json. It records 100 completed trials, 103 starts, three first attempts without final replies, exactly three one-time retries (r019/r026/r039), 399 logged calls, and zero mismatches. All first-start dispatch timestamps still follow each lane's frozen order. No successful reply was rerun; each successful final trace has exactly one reply.

## Statistics and aggregation review

analyze.py uses the standard 95% Wilson interval for arm proportions, neutral-minus-strict risk difference, probability-ordered two-sided Fisher exact test with fixed margins, and a two-sided exact binomial test on discordant matched pairs. Simple exact identities and Fisher arm-swap symmetry were checked without grade outcomes. The matched comparison appropriately uses only blocks with both arms present.

Disputed primary decisions (`null`) contribute no positive event to the main count but remain in its denominator. This is a conservative-negative main coding rule. The script separately records strict sensitivity-positive counts and disputed counts, but does not calculate strict-sensitivity Fisher/matched tests or confidence intervals. The final report should make this coding rule explicit and avoid presenting strict sensitivity inference as already computed.

analyze.py's `audit_pass` examines only completed runs with review files. On its own, `audit_pass=true` does not establish that all 100 planned trials are completed/reviewed; its independent `complete` field and missing/unreviewed lists must also be considered. The code does not itself enforce the per-trial two-start cap or inspect failed attempt status; this cross-lane audit inspected those separately.

## Scope limits

- Saved exact intended plaintext prompts can be hash-verified. Native incoming context is opaque/encrypted and was excluded; delivered plaintext is not independently verified.
- Observed model/effort come from native session metadata, not an independent provider execution attestation.
- Per-run latencies are heterogeneous coordinator measurements: lane 3 now uses dispatch-to-public-final timestamps; other saved completion records may include the interval until coordinator capture. They include queue time and cannot be interpreted as model-only compute time or overall parallel batch duration.
- The selected synthetic case has no established Castro closing time and no source-present controls. This supports a wording-effect measurement on that case, not a general hallucination rate or private internal causal mechanism.
- Separate same-family reviewer grading can be blind to assigned condition in the input packet, while reply style may reveal condition. This audit did not inspect or modify grading decisions.
