# Exact-head dependency review for PR47 F3

**Result: local content review complete, with no new in-scope Blocker, Follow-up or Preference.** This records a fresh review of all five exact dependency heads named in [PR47 F3](https://github.com/samovers/OFARM/pull/47#issuecomment-6309968029). It closes the missing **local content review** for these bytes. It does not add a GitHub review, independent human approval, source adoption, merge permission or runtime readiness. Existing owner decisions remain open as listed below.

Reviewed on 21 October 2026 by the independent reviewer chat “Verify authorization input contracts.” The overall boundary is read-only security audit. Each component was assessed within its own boundary; no implementation boundaries were combined. No source worktree, Git index, branch, PR, CI configuration or issue state was changed. This transport copy includes the review and focused result records. Review scripts, exported test inputs, full logs and diffs remain in the original local review directory; they are not installed as new verifier code here. PR47's design amendments and B1/F1/F2/P1 are outside this review.

| PR | Exact reviewed head | Component boundary | Review scope |
| --- | --- | --- | --- |
| [41](https://github.com/samovers/OFARM/pull/41) | `bfd15b98c48f70e679824005c62adf4241dd8b22` | Assertion-domain record integrity | Earlier review and `fa56c18..bfd15b9` correction; schema, checker, fixtures and limits |
| [42](https://github.com/samovers/OFARM/pull/42) | `471cb1ef20ffde56b1437949975a4c6c86c59dd5` | Authorization-input integrity | Substantive initial review of the complete component above PR41, including both schemas, extraction descriptors, helper, fixtures and source clauses |
| [43](https://github.com/samovers/OFARM/pull/43) | `546f831f495d60b45e93b55fbaaa601b1374ad7e` | Shared validation-evidence integrity | Prior reviews and three corrective commits after `453bfe5`, including actual body validation and payload subject binding |
| [44](https://github.com/samovers/OFARM/pull/44) | `6457009520257f8751ca03caa4b0704cf92160a7` | Authorization-input projection integrity | Prior input review and `898396f..6457009` witness/documentation correction; inactive input behavior and preservation of operation/read behavior |
| [45](https://github.com/samovers/OFARM/pull/45) | `2110f6d78451b50712264dba87d0b8989f134907` | Operation intent-to-result mapping integrity | Prior review, `dde9d7d..2110f6d` calendar/report correction and integrated PR44 dependency |

## Fresh checks

All tests ran from copies exported directly from the named Git objects. They did not use the current mutable source worktree. Runtime: Python 3.14.5, jsonschema 4.26.0, referencing 0.37.0 and the existing isolated rfc8785 0.1.4 installation. The component suite was run once per listed configuration. The repository-wide suite and hosted CI were not rerun, and their historical results are not claimed as fresh evidence.

| Pinned component run | Fresh result |
| --- | --- |
| PR41 assertion component | PASS: 527 cases, 75 accepted and 452 expected rejections |
| PR42 operation/read inputs | PASS: 620 cases, 123 accepted and 497 expected rejections; all 60 read kind/form pairs |
| PR43 shared envelope | PASS: 307 cases, 24 accepted and 283 expected rejections |
| PR44 inherited operation/read inputs | PASS: same 620 cases and all 60 read kind/form pairs |
| PR44 inactive structure/compliance inputs | PASS: 407 cases, 59 accepted and 348 expected rejections |
| PR45 mapping component | PASS: 147 cases, 22 MATCH, 26 MISMATCH and 99 expected UNAVAILABLE |

The six runs executed 2,628 case instances, including the repeated 620-case operation/read suite at PR44. They are not 2,628 distinct semantic obligations.

Independent controls also passed: 161 checks with the optional RFC3339 validator blocked, then six PR45 calendar controls with the validator loaded. Their breakdown is PR41 6, PR42 132, PR43 10, PR44 5 and PR45 8, followed by the six calendar repeats. These are finite review controls, not exhaustive mutation coverage.

The 118 integrity checks passed. They verify all 19 component source pins; 32 PR43 files, 15 PR44 files and 28 PR45 changed files against the earlier reviewed checkpoints; the complete PR45 reviewed tree; inactive manifests; unchanged current/default selections and current schema bytes; and preservation of all 6,474 exported files after testing. PR45's tree is exactly `2566d0f400db8f6e3c8d65df202342a3c7a2ca14`. The primary OFARM checkout is clean.

Evidence: [suite results](suite-results.json), [independent controls](independent-probes.json), [calendar with optional validator](calendar-with-optional.json) and [integrity checks](integrity-results.json). The original snapshot hashes, commands, full outputs, exact prior-to-head deltas and scripts remain in the unbundled local review record. The [transport record](transport.json) pins that original report and the omitted evidence files; only evidence-location prose and absolute workstation prefixes changed in this copy.

## Findings and dispositions

### PR41

The earlier **B1 prospective identity contradiction is repaired at the pinned head**. The checker compares the prospective subject's typed identity against the immutable anchor and typed body context. It does not allow a revision/digest spelling change to disguise an identical logical identity. Fresh controls used schema-valid prospective subjects across structure, operation and compliance branches: same-anchor identities reject at `PROSPECTIVE_SUBJECT_IS_ANCHOR`, while distinct proposed identities pass. The committed suite also exercises typed context collisions. This remains a local contradiction check, not a global identity resolver.

**F4's named rejection-evidence weaknesses are repaired**: schema negatives require exact instance/schema paths and keywords, required-member errors identify the missing member, and the checker tests relevant shape behavior without format support. The schema itself is unchanged by this correction.

**Still open:** F1 and the qualifier/absence part of F2 require source-time admission decisions; exact endpoint string equality alone does not establish performance-time eligibility. F3 has a documented source-backed explanation for allowing different immutable payload versions across roles, without a new global single-revision policy or claimed reviewer acceptance. P1 whitespace-only text remains allowed. P2's shared nine-kind subject choice still requires deliberate acceptance. No source meaning or foreign resolver was silently supplied by this review.

### PR42 — substantive initial review

The component matches the bounded input contract in pinned PR11 §§7.5–7.6 and the actor, subject, correction and time ownership in pinned PR23 §§5–6. It preserves one `TARGET_SCOPE` for operation claims and one `READ_TARGET` for reads. Query specification and plan form a fixed pair of integrity inputs; they cannot become additional authority targets. All ten scope kinds and twenty record/artifact kinds remain available for direct and query reads. Buffered mode, purpose, projection, redaction revision, snapshot request and disclosure controls stay within the complete intent digest.

I read both complete schemas, all extraction mappings, dependency bindings, the helper, the manifest and the stated limitations. An independent resource/view oracle, written without using the descriptor mappings, agrees for every fixture. Additional controls reject caller principal/assertor/result-state mirrors, excess or missing query roles, tuple swaps, streaming, malformed/duplicate projection pointers, purpose normalization attempts, missing offline evidence, online evidence injection, impossible dates, prospective anchor collision and body-time disagreement. Changed claim text changes the complete intent digest even when the extracted authorization view is identical. Duplicate JSON names, descriptor destination collisions and altered dependency bytes reject.

No concrete defect was found in the declared authorization-input boundary. The component does **not** prove authority, tenant/twin applicability, immutable resolution, source-time eligibility, query-plan support, disclosure coverage or transaction behavior. The 413 committed schema-negative cases mostly classify rejection at schema level; this review does not recast all of them as exact-path witnesses. The independent controls supplement, rather than upgrade, that evidence claim.

### PR43

The original selected body-schema binding defect remains repaired: the complete binding is carried and compared against the separately supplied expected context and resolved fictional contract. **F4 is repaired** by validating the actual result body under the selected schema. **F1 is repaired locally** by requiring four fields in the hashed payload: result digest, intent digest, protected-effect contract digest and complete selected body-schema binding. Fresh controls changed each field for both PASS and FAIL scenarios, recomputed the payload and trace digests, and still received the specific subject-mismatch rejection. Hash agreement cannot launder a payload for another declared subject.

F2's descriptions distinguish selected-target closure declarations from dependency resolution. P1's parser handling and P2's mechanism descriptions remain corrected; P4's public evidence claims remain limited to committed controls. Optional P3 hygiene coverage remains open.

**B1 is a reconciled consumer handoff, not implemented transaction enforcement.** The authoritative attempt must resolve the current trace and compare its full authorization-result binding and bundle digest; historical admitted-result provenance cannot substitute for fresh current evidence. Actual attempt resolution, failed-attempt finality, decision single-use, eligible retries and original receipt replay remain in the separate transaction boundary. This review does not mark those guarantees complete.

### PR44

The final helper requires the named unexpected property to occur in the actual failing object and to be disallowed by that error's local schema. It cannot borrow a substring, another object's error or a property admitted by `properties`/`patternProperties`. Fresh controls verified the positive witness and four false-witness cases. The committed inactive suite includes the 46 corrected member witnesses and 64 added harness controls, while the inherited 620 operation/read cases still pass.

P1's failure-code annotations, P2's witness precision and P3's prospective-ID wording are corrected for their named scope. **F1 remains open:** exact body-owned event selectors and claim/subtype/dominant-consequence compatibility still require domain-owner work. **F2 is an explicit dependency policy:** whole operation-schema byte changes require compatible repinning; this is not a newly separated ownership contract. P4's shared subject kinds and whitespace text remain deliberate unpromoted choices. The original missing F1/F2 review details were not reconstructed or invented.

### PR45

**B1 is repaired at `2110f6d`.** The component installs its pinned deterministic Gregorian calendar check, independent of the optional package. Both-side impossible `assertedAt` values including `2024-02-30T12:00:00Z` reject as `UNAVAILABLE/SCHEMA` at the intent's date-time format. Invalid non-leap and century dates also reject; `2000-02-29` passes. These outcomes hold with the optional validator blocked and loaded. No Python 3.13 result is claimed.

The supported **F1 report-consistency invariants are repaired**: fixed row shapes, references, presence/digest membership and aggregate relations are constrained; the private check rejects arbitrary compared-digest/outcome contradictions. Fresh aggregate and digest mutations reject. A standalone report still cannot authenticate its claimed whole-input digest: verification must be regenerated from the original bytes.

F2 retains schema preflight for wrong subtypes and adds a valid alternate-branch rejection rather than weakening the selected operation-body requirement. F3's 29-AR traceability, row links and event-binding visibility are explicit; full AR/PC and event compatibility remain unavailable. F4's unsupported approval language is removed. P1 distinguishes missing caller files from missing component dependencies. Missing original F1/F2 and part of F3 detail remains missing; the review verifies the supported finite repairs, not absent text.

## Scope and next step

There are no new findings to route back for component edits. All five trust boundaries stayed unchanged because this task only reviewed their pinned content. Existing semantic and consumer prerequisites remain open. Full event and measurement support is preserved as required downstream work; this review neither narrows it nor declares it implemented. OFARM2 #392/#396 remains parked. CI activation, publication, source adoption and merge remain separate decisions.

Next: review the amended PR47 head in a separate bounded review, using this record only as exact-head dependency content evidence.
