<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: GREEN_WITH_REVIEW.
-->

# OFARM Publication and Output Assembly Surface RFC v0.1

Date: 2026-05-13  
Status: draft RFC, implementation/conformance support only  
Phase: AI-agent-ready platform amendment Phase 4  
Affected active authority: `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`, `03_machine_contracts/schemas/output_assembly/OFARM_PublicationAssemblyRequest_schema_v0_1.json`, `03_machine_contracts/schemas/output_assembly/OFARM_PublicationAssemblyResult_schema_v0_1.json`, `03_machine_contracts/schemas/output_assembly/OFARM_PassportViewMetadata_schema_v0_1.json`, `03_machine_contracts/schemas/output_assembly/OFARM_DocumentAssemblyMetadata_schema_v0_1.json`

## 1. Purpose

This draft RFC defines an app-facing output preview and assembly surface so AI coding agents do not treat every compiled output as a “passport” or treat previews as frozen truth.

## 2. Preserved OFARM law

This RFC does not change baseline output law.

It preserves:

- `PassportView` is a live, governed view and not a bucket term for every output.
- `DocumentAssembly` is a compiled/frozen output class with its own authority, evidence, basis, and publication rules.
- A compiled output is not a truth store.
- Advisory output is not compliance output.
- Publication, attestation, and filing require authority and traceable gate passage.

## 3. Required public operations

The public platform surface should expose operation-centric output surfaces:

| Operation | Consequence | Required behavior |
|---|---|---|
| `assemblies.preview` | no authoritative change | returns qualified preview, problems, and trace |
| `assemblies.dryRun` | no authoritative change | runs authority/evidence/freshness checks without publishing |
| `assemblies.create` | publication or freeze action | requires authority, evidence, freshness, and trace |
| `assemblies.get` | read-only | returns output metadata plus qualification envelope |
| `assemblies.trace` | read-only | retrieves publication/reconstruction trace subject to redaction |

If the Phase 2 public surface uses `assemblies.dryRun` and `assemblies.create`, `assemblies.preview` may be implemented as `assemblies.dryRun` with `previewOnly=true`.

## 4. Output action classes

The request must state one of:

- `SERVE_PASSPORT_VIEW`
- `PREVIEW_PASSPORT_VIEW`
- `PREVIEW_DOCUMENT_ASSEMBLY`
- `FREEZE_DOCUMENT_ASSEMBLY`
- `ATTEST_DOCUMENT_ASSEMBLY`
- `FILE_SUBMISSION_ASSEMBLY`
- `EXPORT_API_PAYLOAD`

Preview actions must not create frozen output, attestation, filing, or accepted truth.

## 5. Result qualification

Every output preview or assembly result must include `ResultQualificationEnvelope`.

The qualification must say:

- whether the output is advisory, compliance, or mixed
- whether it depends on materialized state
- whether the materialization is fresh, stale, invalidated, or disputed
- whether evidence is sufficient, missing, redacted, or review-required
- whether the actor has full, partial, or denied authority
- whether the preview is high-consequence-safe
- whether any annex is required

## 6. Refusal and annex behavior

The platform must refuse, downgrade, or require annex/review when:

- current state is stale or invalidated for high-consequence output
- open disputes affect the requested basis
- evidence is insufficient for requested output class
- permission limits hide required evidence or basis
- the app requests attestation of a PassportView
- the app requests compliance output from Advisory Twin-only material

A DocumentAssembly may include dispute/correction annexes when policy permits. A PassportView preview must disclose limitations rather than freezing them as a document assertion.

## 7. AI coding-agent constraints

AI-generated apps must not:

```text
call every output a passport
attest a PassportView
file a preview
hide basis limitations
reuse stale materialization for compliance output
promote advisory explanation into compliance claim
store compiled output as canonical truth
```

AI-generated apps should:

```text
call assemblies.preview/dryRun before high-consequence assembly
branch on ResultQualificationEnvelope
show annex/review/refusal states
link to trace
preserve PassportView/DocumentAssembly terms
```

## 8. Machine contracts

This draft RFC introduces candidate support schemas:

- `OFARM_OutputAssemblyPreviewRequest_schema_v0_1.json`
- `OFARM_OutputAssemblyPreviewResult_schema_v0_1.json`
- `OFARM_ResultQualificationEnvelope_schema_v0_1.json`
- `OFARM_PublicReadModelEnvelope_schema_v0_1.json`

These remain draft machine contracts until review and promotion.

## 9. Acceptance tests

A conforming implementation must pass tests that:

1. deny PassportView attestation
2. block high-consequence output from stale materialization
3. preserve open dispute status in output preview
4. show permission-limited evidence instead of “no evidence”
5. preserve advisory/compliance separation
6. return trace references for preview and assembly decisions

## 10. Promotion route

Promote only after examples validate against existing publication assembly, materialization, query, authority, and trace contracts.
