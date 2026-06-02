# Wave 4 evidence sufficiency patch bundle v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: repo-relative patch bundle for the Wave 4 evidence sufficiency and attestation closure pass

---

## What this patch contains

This patch adds:
- the companion policy for evidence sufficiency and attestation posture
- the `EvidenceSufficiencyCase` machine contract
- starter allow/review/refuse example payloads for compliance assertions, attested dossier/document outputs, and submission packages
- a dossier-specific `MaterializationSnapshot` example for attested-output grounding
- v0.6 machine-contract validation runner/results
- evidence-sufficiency fixture runner/results
- conformance matrix updates
- package index/status updates

## Apply posture

This is a repo-relative unified diff against the package state represented by:
- `OFARM2_project_migration_seed_v0_6_wave3_alias_governance_v0_1.zip`

The patch file intentionally excludes the patch bundle directory itself.

## Patch file

- `OFARM_wave4_evidence_sufficiency_v0_1.patch`
