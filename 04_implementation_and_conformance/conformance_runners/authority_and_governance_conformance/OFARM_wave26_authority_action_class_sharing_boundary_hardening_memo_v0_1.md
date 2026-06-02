# OFARM Wave 26 authority action-class and sharing-boundary hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded implementation/conformance closure for the remaining authority action-class and sharing-boundary seams after Wave 25

---

## 1. Why this wave exists

After Wave 25, the central pack-merge seam was closed, but the conformance matrix still left two closely related authority/output rows only partially covered:

- authority action-class decision tests
- sharing-boundary and no-implicit-access tests

Those rows belong together because both depend on the same runtime boundary:
explicit authorization evaluation over concrete action classes, explicit sharing grants, and explicit no-implicit-authority rules.

The open residue named in the matrix was also consistent:
- broader context-governance coverage
- broader sign/attest permutations
- richer compiled-output sharing families
- multi-party revocation evidence
- explicit proof that sharing does not silently imply write/assert/sign authority

This wave closes that cluster without changing active law.

---

## 2. What this wave does

This wave adds runtime-shaped evidence for:

- all 20 action classes in the Authority Action Matrix RFC
- all 4 baseline authorization outcomes:
  - `ALLOW`
  - `DENY`
  - `REQUIRE_REVIEW`
  - `REQUIRE_HUMAN_APPROVAL`
- the three context-governance action classes:
  - `CONTEXT_INSTALL_PACK`
  - `CONTEXT_ACTIVATE_PACK`
  - `CONTEXT_DEACTIVATE_PACK`
- the three sign/attest/output action classes:
  - `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY`
  - `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY`
  - `OUTPUT_FILE_SUBMISSION_ASSEMBLY`
- sharing-boundary evidence across:
  - `PassportView`
  - `DocumentAssembly`
  - `SubmissionAssembly`
  - underlying raw evidence / truth-bearing artifacts
- explicit no-implicit-access proof for:
  - compiled-output share without write authority
  - compiled-output share without attestation authority
  - compiled-output share without underlying raw-evidence access
  - cross-farm role presence without explicit sharing grant
  - multi-party revocation where one grantee loses access while another grantee remains allowed

The wave emits:

- action-class coverage records
- runtime-shaped authority decision records
- sharing-boundary access records
- sharing-family coverage records
- runtime telemetry and summary results

---

## 3. What this wave does not do

This wave does **not**:

- change the Constitution
- change the Platform baseline
- add new machine-contract schema families
- claim deployment-collected cross-tenant sharing telemetry
- promote any bridge-pack surface

This remains bounded implementation/conformance hardening.

---

## 4. Expected coverage effect

If the emitted records validate as designed, the matrix should move:

- `authority action-class decision tests` from `PARTIAL` to `COVERED`
- `sharing-boundary and no-implicit-access tests` from `PARTIAL` to `COVERED`

The remaining adjacent authority/output rows may still stay partial where they require deployment-produced publication or evidence-gate telemetry beyond this bounded slice.

---

## 5. Evidence posture

This wave is still package-local runtime-shaped proof, not live deployment proof.

That is acceptable for these two rows because the gap named in the matrix was breadth of action-class and sharing-boundary coverage, not missing live-field evidence.
