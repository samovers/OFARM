# OFARM partner-output surface governance boundary fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation artifact  
Scope: executable decision-support lane for distinguishing implementation-local compiled-output channels from governed runtime-surface or equivalent deployment-facing boundary lanes

---

## Purpose

This wave closes the next narrow seam after live deployment evidence capture readiness.

It does **not** create new runtime-surface contracts.
It does **not** reopen the compiled-output taxonomy.
It makes the current package posture explicit so partner-output telemetry no longer implies that every observed adapter is "pending promotion" by default.

## Included artifacts

- `OFARM_partner_output_surface_governance_decision_matrix_v0_1.json`
- `OFARM_runtime_surface_partner_output_telemetry_linkage_v0_2.json`
- `ofarm_partner_output_surface_governance_boundary_runner_v0_1.py`
- `OFARM_partner_output_surface_governance_boundary_results_v0_1.json`

## What this wave does

- binds the current partner-output telemetry lane to one explicit decision matrix
- distinguishes already-governed export/runtime surfaces from implementation-local compiled-output channels
- removes the implication that every observed dashboard/CSV/PDF/dossier/submission adapter is automatically pending promotion into `RuntimeSurfaceContract`
- keeps future promotion possible only where the accepted closure-note threshold is crossed
- preserves the current release-bundle lane without forcing new Capability Manifest rows or new runtime-surface contracts

## Current package decisions

### Already governed runtime-surface lane

- `NGSI_LD_PARTNER_EXPORT` remains linked to:
  - `surface:ngsi-ld-export:v1`
  - `surface-contract:ngsi-ld-export:v0.2-draft`
  - the current manifest/release-bundle lane

### Retained implementation-local support output channels

The following partner-output channels remain explicit implementation-local support identities in the current package:

- `PARTNER_DASHBOARD_JSON`
- `PARTNER_ADVISORY_CSV`
- `PARTNER_COMPLIANCE_PDF`
- `PARTNER_DOSSIER_JSON`
- `PARTNER_SUBMISSION_XML`

These channels remain traceable through publication telemetry, trace-back records, publication request/result artifacts, and governed compiled-output metadata.
They are not promoted to governed runtime-surface law in this wave.

## Promotion threshold reminder

A later promotion move should happen only if the channel becomes a stable external boundary in its own right, for example because OFARM must govern:

- stable external identity
- published service-description or schema boundary
- independent compatibility/version promises
- auth/delivery/idempotency posture
- pack/deployment collision semantics at that lane

## What this wave does not do

- it does **not** add new machine-contract schemas
- it does **not** add new manifest rows
- it does **not** say partner-output channels can never be promoted
- it does **not** treat the current package-local telemetry as live deployment evidence

## Current package posture

The package now has:

- one accepted closure note that defines the promotion boundary
- one executable decision matrix for the current partner-output lane
- one updated telemetry-linkage summary aligned with that decision

The package still does **not** have governed runtime-surface contracts for the current dashboard/CSV/PDF/dossier/submission adapters, and that is now an explicit modeling choice rather than an unresolved ambiguity.
