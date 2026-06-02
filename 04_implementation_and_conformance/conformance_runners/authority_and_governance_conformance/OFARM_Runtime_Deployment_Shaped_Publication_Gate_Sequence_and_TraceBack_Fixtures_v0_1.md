# OFARM runtime deployment-shaped publication gate-sequence and trace-back fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: executable runtime-shaped publication-sequencing and partner-surface trace-back fixtures

This fixture family exists to close the last package-internal partials for:
- enforcement-gate sequencing tests
- projection trace-back tests

The fixtures stay honest about their boundary:
- they are **runtime-emitted package-local fixtures**
- they are **not** live field-collected bridge telemetry
- they do **not** promote any same-standard bridge surface beyond `DRAFT`

## Scenario families

### Positive publication sequences
1. live passport publication to NGSI-LD partner surface
2. live passport publication to partner dashboard JSON surface
3. advisory report publication to partner CSV surface with stale-warning posture
4. compliance report publication to partner PDF surface after human approval
5. dossier attestation publication to partner dossier JSON surface after governance review and human approval
6. submission filing publication to partner XML surface after full authority, freshness, evidence, and publication gate closure

### Blocked publication sequences
7. dossier publication blocked because review chain is incomplete
8. submission publication blocked because the external surface has a schema mismatch
9. live passport publication blocked because recipient-facing surface constraints conflict with the requested profile
10. compliance report publication blocked because revocation recheck flips authority before publication commit

## What gets emitted
- gate-sequence records with monotonic gate ordering
- multi-action review-chain records
- partner-surface publication trace-back records
- runtime-emitted publication telemetry
- a summary result object used to advance the conformance matrix
