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

The API is verify_state(proof_bytes, *, package_root, selected, context_bytes, policy_bytes, snapshot_bytes, records, source_root=None). records maps exact logical refs to original UTF-8 JSON bytes. selected has contractRawSha256, contextRawSha256, policyRawSha256 and proofBinding. Refer to the schemas and complete fictional cases for exact fields. The CLI accepts explicit local files and writes one report; records-manifest paths must stay within its directory.

This is a separate prerequisite for #47. It does not complete the domain verifier. All active/default choices, default validation commands and workflow files remain unchanged. OFARM2 #392/#396 stay parked and #421 remains separate. Runtime work, CI activation and merge are separate.

Independent review passed 94 checks and replayed all 111 owner checks with no actionable findings within the declared conditional scope. See REVIEW.md.

Next: review the separate draft and bind its exact interface in #47.
