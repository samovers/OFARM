# Wave 1 lot traceability patch bundle v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: repo-relative patch bundle for the Wave 1 lot traceability and claim-basis closure pass

---

## What this patch contains

This patch adds:
- the accepted RFC for lot traceability and claim-basis closure
- `LotLineageChange` and `TraceabilityClaimBasis` machine contracts
- starter example payloads for split, commingle, transform, shipment-reference continuity, and claim-basis reset
- lot-fixture notes
- v0.3 machine-contract validation runner/results
- lot traceability fixture runner/results
- conformance matrix updates
- package index/status updates

## Apply posture

This is a repo-relative unified diff against the package state represented by:
- `OFARM2_project_migration_seed_v0_6_hardest_design_amendment_plan_v0_1.zip`

The patch file intentionally excludes the patch bundle directory itself.

## Patch file

- `OFARM_wave1_lot_traceability_v0_1.patch`
