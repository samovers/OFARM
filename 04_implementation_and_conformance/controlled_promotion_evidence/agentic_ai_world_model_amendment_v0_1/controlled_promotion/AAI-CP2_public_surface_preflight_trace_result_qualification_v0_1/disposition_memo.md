# AAI-CP2 disposition memo

Decision: promote the narrow public-surface contract layer required to execute the CP1 AI-facing release-qualification gate.

## Promotion class

- Accepted RFC extension.
- Active machine-contract promotion.
- Supporting implementation/conformance artifacts.

## Why this is the smallest safe patch

CP1 made release qualification mandatory but deliberately did not promote the concrete schemas. CP2 promotes only the schemas needed to make that baseline gate executable: operation description, preflight request/result, result qualification, trace retrieval, public read-model wrapping, source-fidelity posture, and registered runtime problem reason codes.

## Risks controlled

- Public operation success being mistaken for governance success.
- Preflight/dry-run creating authoritative side effects.
- AI-facing results hiding stale, permission-limited, evidence-insufficient, advisory-only, disputed, corrected, or redacted posture.
- Runtime failures being handled with inconsistent free-text messages.
- Trace retrieval masking redaction or access-denial as missing data.

## Remaining risks

- No agent actorship or agent-run trace law is promoted by CP2.
- No runtime implementation has executed the CP2 conformance suite under real load.
- Output assembly preview remains unpromoted.
- World-model and request-layer contracts remain supporting-only.
