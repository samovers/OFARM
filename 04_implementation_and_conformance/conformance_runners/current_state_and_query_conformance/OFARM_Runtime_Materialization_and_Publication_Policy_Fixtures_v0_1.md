# OFARM Runtime Materialization and Publication Policy Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

## Purpose

Provide a bounded runtime-shaped fixture family that joins together:

- freshness and invalidation
- twin policy
- evidence sufficiency
- attestation authority
- compiled-output taxonomy
- publication trace-back

## Fixture families

### 1. Advisory reuse and warning
- live field passport may reuse stale materialization with warning
- frozen advisory report may reuse stale materialization with warning
- frozen advisory alert may reuse stale materialization with warning

### 2. Compliance recompute and refuse
- compliance report must recompute on context drift
- compliance report may require review after evidence update
- compliance alert must recompute where advisory alert may only warn
- submission filing must recompute on submission-binding change
- submission filing must refuse after explicit invalidation

### 3. Attestation policy
- dossier attestation allowed on fresh materialization with sufficient evidence and signatory authority
- dossier attestation denied after signatory-scope reduction
- attested report denied when evidence sufficiency refuses
- dossier attestation recomputes after attestation-policy or shaping change

### 4. Output taxonomy
- `PassportView` supports live serving and read-only sharing only
- `DocumentAssembly` supports frozen assembly, approval, and selected attestation families
- `SubmissionAssembly` supports assemble-and-file only
- live passport objects are never silently promoted into signable or fileable assemblies

### 5. Trace-back
Each publication result should preserve package-local linkage to:

- materialization basis
- retained snapshot
- resolved context
- evidence decision
- final publication evaluation

## Non-goals

This fixture family does not claim:

- deployment-collected production telemetry
- partner-specific publication adapters
- new schema families
- closure of bridge-pack promotion readiness
