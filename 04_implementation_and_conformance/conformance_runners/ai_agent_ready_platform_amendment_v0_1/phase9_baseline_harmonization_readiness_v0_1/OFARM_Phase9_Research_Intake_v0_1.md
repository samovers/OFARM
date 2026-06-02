# OFARM Phase 9 Research Intake v0.1

Date: 2026-05-14  
Source: `deep-research-report-25.md`

## Research conclusions used

The research reinforces that Phase 9 should not rewrite the model into CRUD. The implementation route should publish sharper machine contracts, advertise capabilities explicitly, make high-consequence operations rehearseable, expose structured failure reasons, and enforce semantic-law conformance tests.

Adopted into Phase 9:

- public contract pack and public/internal boundary should be promotion candidates, not hidden runtime conventions
- capability and operation catalogues should remain discovery aids and not authority decisions
- preflight/dry-run/explain/trace behavior should be readiness-gated
- reason-code registries should be machine-stable before SDK release
- conformance must target semantic-law shortcut failures, not only protocol success
- candidate-first import, result qualification, and formula/versioned calculation contracts require explicit baseline/readiness handling

## Research conclusions rejected as law

External standards remain implementation patterns only. OpenAPI, AsyncAPI, JSON Schema, FHIR, OPA, MCP, Kubernetes, HTTP problem details, and idempotency patterns do not become OFARM semantic law by reference.

## Phase 9 use

The research is used to justify proposal wording and readiness gates. It is not used to override active baseline authority.
