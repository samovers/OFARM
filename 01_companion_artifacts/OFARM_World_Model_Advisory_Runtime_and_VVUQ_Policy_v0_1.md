# OFARM World Model Advisory Runtime and VVUQ Policy v0.1

Status: active companion artifact by AAI-CP7  
Scope: policy guidance for Advisory Twin world-model use, validation, uncertainty, invalidation, and reconciliation.

## 1. Policy posture

World-model artifacts are governed Advisory Twin artifacts. They are useful for explanation, scenario analysis, risk flags, draft plans, and review prompts. They are not truth stores, current-state materializations, Compliance Twin state, or evidence sufficiency by themselves.

## 2. Minimum policy requirements

A world-model run must expose:

- input basis;
- observation basis;
- assumptions;
- model/method identity;
- calibration evidence references, if any;
- uncertainty statement;
- validity window;
- invalidation rules;
- output disposition;
- governance blockers;
- reconciliation route.

## 3. VVUQ caution

Verification, validation, and uncertainty quantification remain evidence obligations, not labels. CP7 does not make any calibration or validation reference sufficient by itself. A deployment may not claim world-model readiness without separate conformance evidence, pilot evidence, monitoring plan, and live invalidation/reconciliation evidence.

## 4. High-consequence use

High-consequence or compliance-relevant use requires a separate bridge into ordinary OFARM governance. The bridge must re-evaluate authority, evidence, freshness, pack context, query basis, sharing/revocation posture, output disposition, and review/promotion law.

## 5. Farmer-facing disclosure

Farmer-facing world-model outputs must show advisory-only status, validity window, uncertainty, observed basis, assumptions, missing data, and prohibited uses in a compact qualification surface. A scenario result must not be phrased as an accepted farm fact.

## 6. Invalidation and reconciliation

Invalidated world-model artifacts must be marked and blocked from governed use until re-run or reviewed. Observed-outcome reconciliation may update advisory confidence or trigger review, but it does not alter canonical truth without normal correction/promotion.
