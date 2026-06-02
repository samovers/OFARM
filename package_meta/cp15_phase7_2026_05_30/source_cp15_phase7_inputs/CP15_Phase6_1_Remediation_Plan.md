# CP15 Phase 6.1 — Remediation and Schema Hardening Plan

Status: remediation candidate; draft/non-default only.

This pass remediates the P0/P1 defects from CP15 Phase 6 hostile review without expanding CP15 scope.

## Remediated defect classes

| Defect class | RFC text change | Baseline patch change | Schema change | Conformance change | Blocking for Phase 7 |
|---|---|---|---|---|---:|
| No executable conformance runner | Add requirement for schema-aware, cross-record CP15 runner | No baseline change | N/A | Added executable runner and fixtures | Yes |
| DeploymentCandidate can approve failed evidence | Clarify evidence sufficiency is cross-record, not ref presence | No baseline change | Added review/authority/waiver fields | Cross-check build/SBOM/dependency/static/security/conformance | Yes |
| Security/static contradictions | Add severity/disposition consistency rule | No baseline change | Added waiver refs | Critical/high/failure scan fixtures | Yes |
| Dependency risk contradictions | Add critical/unknown risk gate | No baseline change | Added review/waiver refs | Critical/unknown dependency fixtures | Yes |
| DeploymentPlan unsafe CP gates/blast radius | Add blast-radius and CP-gate minimums | No baseline change | Added noApplicableCPGatesBasis and blast approval refs | CP gate / rollback / canary / blast fixtures | Yes |
| DeploymentAuthorization temporal/support weakness | Add temporal and plan-state checks | No baseline change | Existing fields used | Expiry/plan-state fixtures | Yes |
| Promotion chain too weak | Add promotion-chain sufficiency rule | No baseline change | Added release/binding/rollback/canary refs | Runtime-promotion chain fixtures | Yes |
| Runtime binding too weak | Add active non-default binding support rule | No baseline change | Added incident refs | Binding/release/auth fixtures | Yes |
| Runtime receipt too strong | Add receipt-only and authorization-window checks | No baseline change | Added authorization window fields | Runtime receipt fixtures | Yes |
| Canary contradictions | Add state/disposition/telemetry consistency | No baseline change | Added incidentTelemetryRefs | Canary fixtures | Yes |
| Rollback readiness too weak | Add freshness/test evidence rule | No baseline change | Added freshness/test-result fields | Rollback fixtures | Yes |
| Security waiver temporal/scope weakness | Add bounded/current waiver rule | No baseline change | Added severity/special authority | Waiver fixtures | Yes |
| Model evaluation bias sufficiency | Add bias/evidence disposition rule | No baseline change | Added limitation/review refs | Model evidence fixtures | Yes |
| CP13/CP14 model deployment boundaries | Clarify refs are not deployment authority | No baseline change | Added model review/training refs | Model candidate boundary fixtures | Yes |
| Prompt/policy high-consequence review | Add review/conformance/security requirements | No baseline change | Added authority/conformance/security refs | Prompt/policy fixtures | Yes |
| Adapter-kind CP gates | Add CP12/CP14/registry gates by adapter kind | No baseline change | Added CP gate/currentness/conformance/security fields | Adapter fixtures | Yes |
| Semantic mapping confidence | Add loss/coverage sufficiency | No baseline change | Added mappingCoverageSufficient/lossMapDisposition | Mapping/adapter fixtures | P1 |
| ReleaseBundle consistency | Add signature/SBOM/conformance/candidate consistency | No baseline change | Added signature coverage classes | Release bundle fixtures | Yes |
| DeploymentOutputQualification lifecycle | Add advisory/prod-readiness blocking | No baseline change | Added reviewBasisRef | Output qualification fixtures | P1 |
| Incident-driven blocking | Add confirmed high/critical incident blocking | No baseline change | Existing + optional incident refs | Incident fixtures | P1 |

## Scope preserved

CP15 still does not create production CI/CD, generic MLOps, legal/security certification, OFARM Social, OFARM Exchange, robot mission law, farm-to-farm intelligence law, or current/default schema promotion.
