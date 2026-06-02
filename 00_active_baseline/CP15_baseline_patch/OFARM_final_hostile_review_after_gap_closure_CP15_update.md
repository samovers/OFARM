# OFARM hostile review — CP15 update

Status: final CP15 amendment candidate hostile-review addendum  
Date: 2026-05-30

CP15 closes a major conceptual gap: generated software, generated adapters, generated mappings, prompt/workflow changes, model candidates, and release bundles are now governed as explicit delivery artifacts rather than hidden runtime authority.

## Closed or reduced

- Generated artifact does not become deployment authority.
- Build success, test success, scan success, conformance success, canary success, runtime receipt, telemetry, and agent tool success do not create production readiness.
- Deployment candidates, plans, authorizations, promotion decisions, release bundles, runtime bindings, receipts, canaries, rollback plans, and incidents are distinct.
- Model deployment candidates cannot bypass CP13 learning-output and CP14 training/model-improvement boundaries.
- Mission/robot-facing adapters must respect CP12.
- Sustainability-sensitive deployment surfaces must respect CP11.
- Machine contracts remain draft/non-default.

## Still open

- no production software-delivery readiness;
- no production model-deployment readiness;
- no generated-adapter production readiness;
- no cybersecurity certification;
- no autonomous release readiness;
- no full CI/CD product implementation;
- no generic MLOps platform;
- no cloud/vendor deployment topology;
- no automatic current/default schema promotion.

Hostile-reader verdict: CP15 is the correct governance closure if it remains narrow and draft/non-default until steward acceptance and currentness promotion.
