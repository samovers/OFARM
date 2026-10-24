# Pre-verdict protected-state evidence

This non-default owner contract defines exact snapshot, guard, immutable-input and proposed-write evidence for the AssertionRecord domain verifier in PR #47. Its one primary trust boundary is **transaction and history evidence for protected proposed state**.

The checker uses the existing transaction schema's attemptContext without changing its bytes or finalization-mode scope. It verifies independently selected context/policy/proof bindings, original raw bytes and complete JCS values, positive start-snapshot visibility, selected negative/set predicates, unchanged pre-verdict guard versions, and exactly one proposed assertion insert. A correction's prior record must be committed and visible at transaction start. Inputs produced during validation can instead be fixed and guarded before the verdict, preserving validation-phase Event Ingress support.

The creation-context extraction binds exact immutable source bytes and JSON pointers for prior identity, governance boundary/twin, recorded anchors and original creator attempt when present. Legacy ingress needs no invented attempt ID; original creation/ingress source bytes require positive transaction-start visibility. The creation/transaction owner retains source validity and truthful storage provenance; #47 retains supported prior schema and domain compatibility comparisons. The consuming domain contract derives and compares the complete immutable-input manifest. The storage checker cannot establish coverage from a caller-shortened list.

Every positive fixture is explicitly fictional and conditional. These checks do not establish actual isolation, guard continuity through commit, clock trust, atomic commit, prior source-owner admission, authorization or finalization-mode eligibility. The earlier proof does not depend on this attempt's later verdict, checkpoint, receipt or consumption. The complete report always says runtimeProtection=NOT_ESTABLISHED and laterTransactionGate=NOT_EVALUATED.

The API accepts original bytes and independently selected raw pins. It never downloads schemas or dependencies and never accepts an admitted Boolean in place of evidence. See PROPOSAL.md for the exact limits. The original source documents are verbatim copies in the implementation evidence lane; pass its root as source_root when using the split repository layout.

Run the opt-in local checks from the repository root:

```sh
python3 -B 04_implementation_and_conformance/conformance_runners/ofarm_preverdict_protected_state_v0_1.py
```

The API is verify_state(proof_bytes, *, package_root, selected, context_bytes, policy_bytes, snapshot_bytes, records, source_root=None). records maps exact logical refs to original bytes. Structured reads use `JCS_JSON` (also the meaning when digestMode is absent); selected supporting reads can use `RAW_BYTES` with only a raw SHA-256 content pin and no JCS digest. Full read facts retain roles, revisions, availability and guard versions. Required creation-route facts are derived from original committed sources, and recognized current-attempt later artifacts are rejected. selected has contractRawSha256, contextRawSha256, policyRawSha256 and proofBinding. Refer to PROPOSAL.md, the schemas and complete fictional cases for exact fields and owner responsibilities. The CLI accepts explicit local files and writes one report; records-manifest paths must stay within its directory.

This is a separate prerequisite for #47. It does not complete the domain verifier. All active/default choices, default validation commands and workflow files remain unchanged. OFARM2 #392/#396 stay parked and #421 remains separate. Runtime work, CI activation and merge are separate.

The historical local review reported 94 checks and replayed 111 owner checks. Its complete archive was not published, so those 94 checks are not independently replayable from the original PR and do not validate this repair. The opt-in runner now also runs the published review-repair regressions. To retain every generated input and output, run `run_review_repair_02.py --output-dir <local-output-directory>` from the checker directory. See REVIEW.md for the separate fresh review status.

Next: independently review the repaired draft before a separate consumer binding decision; the saved #47 runtime stays unchanged.

The independently authored probe generator is published as `run_independent_review_02.py`. It has its own binding and case construction, rather than importing either authored test generator. From the checker directory, run `PYTHONDONTWRITEBYTECODE=1 python3 -B run_independent_review_02.py --output-dir <local-output-directory>` and then the same command with `--replay-cli`. The output contains every generated original, selection, guard and report. The portable copy's path/exit-code changes and exact public #56 fixture origin are recorded in `fixtures/review-repair-02/independent-generator-origin.json` under the fixture package. Executing these probes is a replay of technical checks, not new owner or human approval.

Next: inspect the separate fresh-review result before any consumer binding decision; runtime integration remains outside this draft.
