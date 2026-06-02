# CP13 Phase 7.2 — Final Gate Hardening Summary

Status: **complete**.

This is a narrow hardening pass against the CP13 Phase 7 final acceptance-gate blockers. It does not reopen CP13 scope, does not split CP13, does not start CP14 or CP15, does not promote CP11/CP12/CP13 schemas to current/default, and does not claim production autonomous self-improvement readiness.

## Repairs applied

1. **FarmMemoryEntry ↔ LearningPromotionDecision cross-check**
   - Active farm memory now requires an approved, matching `PROMOTE_TO_FARM_MEMORY` decision with review and authority trace.
   - Proposed, rejected, invalidated, or superseded promotion decisions cannot support active farm memory.

2. **LearningPromotionDecision ↔ LearningEvaluationTrace cross-check**
   - Farm-memory promotion requires a complete `LearningEvaluationTrace` with `overallDisposition = PROMOTION_CANDIDATE` and no failed hard checks.

3. **CausalEstimate method/strength/trace/bias/missingness consistency**
   - High-confidence causal estimates cannot use exploratory, expert-only, or insufficient methods.
   - High-confidence estimates require complete supporting evaluation, low/known bias, and non-blocking missingness.
   - Moderate estimates cannot cite failed/blocked traces.

4. **LearningEvidenceBundle sufficiency/current-state/missingness/bias consistency**
   - Sufficiency is blocked for `UNKNOWN_BLOCKING` current-state reliance.
   - Current-state reliance requires materialisation and freshness/qualification basis.
   - Severe/unknown missingness or high/unknown/disputed bias cannot support farm-memory or claim sufficiency without review.
   - CP11/CP12 evidence items are now typed consistently in schema, examples, and runner.

5. **LearningEvaluationTrace promotion-candidate completeness and hard-check coverage**
   - `PROMOTION_CANDIDATE` requires complete evaluation and required hard-check coverage.
   - CP11/CP12 checks are required where CP11/CP12 evidence is used.

6. **ExperimentProtocol ACTIVE approval/authority requirements**
   - Active protocols require approval and authority trace.
   - Charter-sensitive active protocols require charter-evaluation trace references.

7. **FarmMemoryRetrievalQualification blocked-use minimums**
   - Retrieval qualification now requires non-empty blocked uses and default blocked classes, including current state, compliance fact, automatic execution, claim-bearing output, model deployment, and cross-farm sharing.

## Revised affected schemas

- `FarmMemoryEntry`
- `LearningPromotionDecision`
- `LearningEvaluationTrace`
- `CausalEstimate`
- `LearningEvidenceBundle`
- `ExperimentProtocol`
- `FarmMemoryRetrievalQualification`
- `LearningOutputQualification` where necessary for consistency/currentness
- related affected examples and conformance fixtures

## Validation

```text
Schema validation: PASS
schemaCount: 22

Example validation: PASS
exampleCount: 22

Conformance runner: PASS
fixtureCount: 81
positiveFixtureCount: 29
negativeFixtureCount: 52
allFixturesPassed: true
```

## Boundary preserved

CP13 still does **not** create:

```text
farm-to-farm intelligence law
federated learning law
regional alert law
cross-farm benchmark law
generated-software delivery law
model deployment governance
adapter generation / rollback / SBOM law
livestock-specific learning law
production autonomous self-improvement readiness
production agronomic advice certification
```

CP13 schemas remain staged as:

```text
03_machine_contracts/drafts_non_default/learning_experimentation_farm_memory/
```

with schema version:

```text
cp13-v0.1-draft-phase7-2-temporal-causal-evidence-chain-hardening
```

They are not current/default.

## Acceptance recommendation

```text
ACCEPT WITH RESIDUAL NON-BLOCKING NOTES.
Do not merge until the architect accepts this hardening package.
Do not start CP14 yet.
```
