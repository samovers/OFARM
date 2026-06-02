# OFARM Runtime Authority Action-Class and Sharing Boundary Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation fixture set  
Scope: runtime-shaped authority decision and sharing-boundary coverage for all action classes plus explicit no-implicit-access checks

---

## 1. Purpose

These fixtures close the remaining central authority/output cluster after Wave 25 by turning the Authority Action Matrix and sharing-boundary rules into executable runtime-shaped cases.

---

## 2. Authority action-class coverage fixtures

### Observe/report
- `OBSERVE_CREATE_OBSERVATION` allow on descendant field scope
- `OBSERVE_ATTACH_EVIDENCE` allow on operation evidence attachment

### Assert/submit
- `ASSERT_STRUCTURE` allow on exact structural scope
- `ASSERT_OPERATION_CLAIM` delegated allow with trace
- `ASSERT_COMPLIANCE` AI-assisted path requiring human approval

### Operate/intervene
- `OPERATE_PLAN_INTERVENTION` allow on descendant crop-cycle scope
- `OPERATE_REPORT_EXECUTION` delegated allow on operation scope

### Review / govern
- `REVIEW_REQUEST` allow with accountable human requester
- `REVIEW_ACCEPT` allow on exact review case scope
- `REVIEW_REJECT_OR_CONTEST` allow on exact review case scope
- `REVIEW_SUPERSEDE` allow on exact state/case scope

### Context-governance
- `CONTEXT_INSTALL_PACK` allow for human field context governor
- `CONTEXT_ACTIVATE_PACK` allow where compatible
- `CONTEXT_ACTIVATE_PACK` require review where competing active output pack context exists
- `CONTEXT_DEACTIVATE_PACK` deny for a role lacking context-governance authority

### Output / attest / sign
- `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` allow for human output approver
- `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` allow for human signatory
- `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` deny for software-agent actor on human-only attestation path
- `OUTPUT_FILE_SUBMISSION_ASSEMBLY` explicit delegated human allow
- `OUTPUT_FILE_SUBMISSION_ASSEMBLY` AI-assisted path requiring human approval

### Share / revoke / receive
- `SHARE_GRANT_ACCESS` human allow
- `SHARE_GRANT_ACCESS` AI-assisted require-human-approval path
- `SHARE_REVOKE_ACCESS` human allow
- `RECEIVE_READ_DATA` allow under explicit compiled-output sharing grant

---

## 3. Sharing-boundary fixtures

### Compiled-output families
- live `PassportView` shared to buyer with read allow but no assert/write/sign authority
- `DocumentAssembly` dossier shared to certifier with read allow but no attestation authority
- `SubmissionAssembly` shared to regulator with read allow but no filing/assert/review authority

### Underlying truth separation
- dossier share does not silently grant raw evidence access
- passport share does not silently grant operation-claim assertion rights
- submission share does not silently grant submission re-filing authority

### Cross-party and revocation boundaries
- cross-farm advisor role without explicit sharing grant is denied
- buyer loses access after explicit revocation while certifier remains allowed under a different still-valid grant
- compiled-output share remains scope-bounded rather than leaking farm-wide visibility

---

## 4. Expected outcomes

The emitted fixture family must collectively prove:

- all 20 authority action classes are represented
- all 4 baseline authorization outcomes are represented
- context-governance and sign/attest permutations are not left as one-off starter cases
- sharing does not imply write/assert/review/sign authority
- compiled-output sharing does not imply raw-evidence visibility
- cross-farm role presence does not imply access without explicit share
- revocation can deny one grantee while leaving another valid explicit grantee allowed
