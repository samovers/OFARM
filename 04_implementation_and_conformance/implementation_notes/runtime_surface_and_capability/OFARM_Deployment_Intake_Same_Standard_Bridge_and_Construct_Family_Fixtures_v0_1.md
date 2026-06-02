# OFARM deployment-intake same-standard bridge and construct-family fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded redacted deployment-intake fixtures and broader construct-family sample coverage for the ADAPT and ISOXML same-standard draft bridge pairs

---

## Purpose

These fixtures extend the same-standard bridge work one step beyond Wave 13 partner-variant sample replay.

They still do **not** claim live field-collected production telemetry.
They ingest **package-local redacted deployment-intake samples** so the package can test:

- intake-shaped bridge telemetry emission for supported and blocked same-standard bridge paths
- broader construct-family sample coverage beyond the earlier minimum reversible subsets
- explicit retention of the `DRAFT` surface boundary even when broader intake samples succeed
- explicit stop conditions for known unsupported or high-consequence construct families

## Included intake families

### ADAPT
- partner delta quantified-input application subset success
- partner epsilon equipment-configuration reference subset success
- partner zeta blocked nested vendor-extension quantified-input sample

### ISOXML
- partner delta worker-allocation reference subset success
- partner epsilon operational-summary quantity subset success
- partner zeta blocked timezone-ambiguous worker-summary sample

## Guardrail

These fixtures are **redacted deployment-intake samples**, not live field-collected production telemetry.
They strengthen bridge promotion readiness evidence and broader construct-family coverage, but they do **not** remove the promotion blocker around missing live field telemetry, non-draft surface approval, or full production-grade construct breadth.
