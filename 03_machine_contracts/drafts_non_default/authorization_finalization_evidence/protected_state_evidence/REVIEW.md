# Protected-state evidence review record

Primary trust boundary: **transaction and history evidence for protected proposed state**. Scope stayed inside that boundary. The package is draft/non-default; #47 remains a separate consumer with unchanged runtime bytes.

## Historical evidence

At published head `3b56df8f75219bb40cf430164d17e61b59237e23`, a local review reported 94 independent checks and replayed 111 authored checks within the original JSON-only scope. Only its summary and compact results were published, not its complete generator/input archive. Those 94 checks cannot be independently replayed from the original PR and do not validate this repair. The ten repository validation commands reported then were historical integration evidence. Their original records remain preserved.

The 23 October author review identified B1 and F1–F4. The first fresh independent AI review of the repair found one additional blocker, R1: object/array-valued schemaVersion fields caused INPUT_ERROR in otherwise valid supporting reads. The original failed review snapshot and results were retained. The checker now type-checks known string labels while preserving independent recognized-shape rejection; the original sixteen failures have explicit regression coverage.

## Fresh review of the repaired candidate

**Fresh independent AI review: 0 blockers, 0 follow-ups and 0 preferences. B1, F1–F4 and R1 are resolved within the declared conditional scope.**

The core review manifest contains 259 exact files, with SHA-256 `1b4ce05af6ac251e7b9e43bb061fe2b9820cbfb9018609209f05657fb37a54ba`. This outcome record is outside that seal so the review can be recorded afterward. Mechanical generated indexes and separately hashed supplementary review evidence are outside the semantic core seal. No contract/checker/fixture covered by that core seal changed after review.

Exact contract raw SHA-256: 4f7cabc08dfc18401d0b8a753f42ef11849b626c6c690dba381e74f6513db4c2
Exact checker raw SHA-256: f39246128862e7eab65aa17855c2ada177b32b23cac38aede3e9e9915c5ec4d5

| Finding | Resolution in this conditional interface |
| --- | --- |
| B1 / R1 | Explicit RAW_BYTES reads guard exact original bytes without JSON wrapping or a JCS digest. Supporting source-specific JSON values remain supported, including object/list schemaVersion values. Structured core inputs keep their existing JSON/JCS requirements. |
| F1 | Complete read facts preserve key, role, revision selectors, effective digest mode, original-byte pin, availability, fixed version and observed/snapshot versions. Repeated refs must agree. |
| F2 | Recognized current-attempt receipt, consumption, transaction-result, checkpoint and gate shapes fail in either digest mode and either availability route. Unknown/opaque encoding and actual availability remain the selected transaction/storage owner's responsibility. The domain consumer must independently derive the full required manifest. |
| F3 | CreationKind and the other required extraction values are source-derived through exact pointers into committed original records. Relabelling an unchanged governed source as legacy fails. Authentic source-route admission stays with its owner. |
| F4 | Historical review claims are explicitly qualified. Public authored and independently authored generators retain exact original input bytes and reports for replay. |

The 111 existing checks and 108 authored repair checks pass. All 127 prior independent probes and 144 fresh later-shape probes meet their expectations. The two CLI replay sets match their API reports and exit codes in 24 and 6 cases respectively; those are parity observations, not additional semantic cases. Portable generator adaptation preserves case logic and expectations. This is independent AI technical review, not human/domain acceptance or a formal two-human approval gate.

The authored family/result cases preserve bytes across all seven event families, five measurement result kinds and absent events. Domain meaning, full interval support, original-evidence admission and producer facts remain the consumer and respective owners' duties. The exact public #57 raw observation and #56 source-byte bundle are fictional compatibility fixtures. Guarding authorization inputs does not perform authorization or prove source completeness.

## Replay and preservation

From the protected-state checker directory, with the declared Python dependencies installed:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B run_review_repair_02.py --output-dir <authored-output>
PYTHONDONTWRITEBYTECODE=1 python3 -B run_independent_review_02.py --output-dir <independent-output>
PYTHONDONTWRITEBYTECODE=1 python3 -B run_independent_review_02.py --output-dir <independent-output> --replay-cli
```

The 144 fresh later-shape probes and their exact provenance are published under `review_evidence_02/` in the checker directory. Run `PYTHONDONTWRITEBYTECODE=1 python3 -B review_evidence_02/run_independent_late_shapes_02.py --repository-root <reviewed-repository> --output-dir <late-shape-output>`. Its README and public-review-manifest.json define the exact published subset; core-files.json contains the 259 reviewed relative paths and hashes.

The original 108 fixture files, four source documents and transaction schema remain byte-identical. New fictional correction revisions are separate. All 342 saved domain-runtime members retain manifest `ca5e4540781a1fe069b7d24a079716f85db5115716f93165301e5074a5e6ff26`. Source seals establish custody of this finite reviewed material, not production facts.

Every report retains `runtimeProtection=NOT_ESTABLISHED` and `laterTransactionGate=NOT_EVALUATED`. No database isolation, real transaction, guard continuity through commit, atomic persistence, actual source admission or end-to-end #47 integration was exercised. Default schemas, validation commands and workflow files remain unchanged. #392/#396 remain parked; #421, CI activation and merge remain separate.

Next: review the exact published prerequisite and make any #47 consumer-binding decision separately, with full owner evidence and runtime obligations intact.
