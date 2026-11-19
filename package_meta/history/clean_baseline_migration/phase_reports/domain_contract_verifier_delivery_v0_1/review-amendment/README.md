# PR47 design and example amendment

This versioned amendment resolves the design findings recorded against
`e93cad876645799789956311ea091e82064cf981`. The primary trust boundary remains
**AssertionRecord domain meaning and validation integrity**. It does not
implement the complete verifier or change any pinned source component.

The [canonical-owner resolution](canonical-owner/resolution.md) explains the
exact source rules and finite construction order. The [domain-owner contribution](domain-owner-recommendation.md)
supplies the complete amended projection, typed evidence roles, selector mapping,
revised examples and focused design checks. These are agent work-owner proposals
and review evidence, not human semantic adoption or admitted producer proof.

## Review dispositions

| Review finding | Amendment and completion limit |
| --- | --- |
| B1: online submission time embedded in claimText | The author renders the domain content. Submission assertedAt, act posture, act evidence and authorization-selected reporter stay outside P for both postures. They remain fully bound and checked in their existing intent/result/owner locations. No runtime authorship permission or PR23 amendment is introduced. |
| P2: offline self-attestation cycle | Fix domain content and exact rendered body first, then authenticate that content in the owner's act record, then bind the completed record into the full intent. Neither the self-attestation nor a dependent alias may enter rendered evidence. The digest-bound example and changed-body/wrong-digest cases exercise this ordering. |
| F1: incomplete assertion evidence | An explicit typed selector map replaces field-name guessing. The amendment repairs 40 missing citation occurrences by adding 33 distinct exact bindings across 12 original examples. Required assertion-support citations belong in evidenceBindings; scope proofs and Event Ingress keep their separate roles. Every resolved input remains trace-bound. |
| F2: missing offline and existing-kind structure examples | The 23 original meanings are preserved in new versioned examples. W24 adds a FARM structure claim; W25 adds a digest-bound offline measured-pruning claim without an event. Canonical v0.2 carrier illustrations and an explicit selector map distinguish wire fields from candidate grammar. The new typed body is still a construction dependency. |
| F3: no recorded review at pinned dependency heads | A fresh dependency review records PR41–45 at the exact pinned heads, earlier findings/fix deltas, component checks and independent probes. It is content review, not GitHub approval, source adoption or a substitute for foreign-owner dependencies. |
| P1: L01 points at mutable local source | The [corrected resolver](source-pin-resolution.json) selects the [exact frozen bytes](source-evidence/frozen-coordination.md). The historical pin, review and source snapshot remain unchanged. |

The reviewed source denominator is unchanged: 99 definitions, 42 requirements,
49 AR/PC obligations, nine time profiles, 17 eligible event/profile cells, all
quantity/material roles and all measurement result/qualifier branches. Performed
instants with and without events, pending versus actual analysis output, sampling
versus analysis, original lexical values and water versus mixture remain covered.
No feature is removed to satisfy a rendering or evidence check.

## Custody and use

Every member of the original INPUT_MANIFEST remains byte-identical to the
published packet. Historical renderings are superseded as construction examples,
not edited in place. [New examples](candidate-examples-v2.json) separate claim content from fictional governed
context and retain per-example source and rendering hashes. Added references
remain fictional; evidence-list membership does not prove admission or relevance.

The [projection contract](projection-contract-v2.json), [evidence selectors](evidence-selectors.json),
[wire selector map](selector-map.json) and [repair ledger](evidence-repairs.json)
are the concrete amended design inputs. The [dependency review](dependency-review/review.md)
records the exact base heads.

The new files are bound by [AMENDMENT_MANIFEST.json](AMENDMENT_MANIFEST.json). Local checks of this amendment
prove example rendering, structural evidence membership, digest/body comparisons,
schema carrier shape and byte preservation only. No new complete domain verifier
exists at this head. Public-entry-point semantic, owner-admission and complete
AR/PC tests remain mandatory construction acceptance, including all hostile cases
specified in Phase A and the owner resolutions. The inherited repository suite
checks component regressions and does not independently validate this packet.

Next: obtain a fresh review of the concrete amended head, then construct the
candidate contract/verifier in the same draft under the documented dependencies.
OFARM2 #392/#396 remain parked; #421, CI activation and merge remain separate.
