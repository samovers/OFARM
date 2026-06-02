# OFARM Phase 7 — Request Posture and Blocking Rules v0.1

## Request postures

- `ADVISORY`: useful for interpretation, scenario reasoning, local memory, or planning.
- `OPERATIONAL`: useful for planned work, contractor coordination, or workflow completion.
- `EVIDENCE_SUFFICIENCY_RELATED`: may affect whether an evidence sufficiency case can pass.
- `COMPLIANCE_BLOCKING`: blocks a compliance-grade output, promotion path, filing, attestation, or accepted consequence until resolved or reviewed.

## Compliance-blocking rule

A generated request may be marked `COMPLIANCE_BLOCKING` only if it cites a valid `RequestBlockingBasis` tied to at least one of:

- active pack rule;
- evidence sufficiency policy;
- authority or delegation requirement;
- output assembly or publication gate;
- promotion path requirement;
- accepted RFC requirement;
- explicit human review decision.

## Downgrade rule

If a request claims compliance-blocking posture without sufficient basis, the platform must block the request, downgrade it to advisory/operational, or route it for human review. It must not let the request silently become a compliance obligation.
