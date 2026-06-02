# OFARM Phase 6 Advisory-Only Boundary Rules v0.1

## Boundary rule

World-model artifacts are Advisory Twin artifacts by default.

They may produce:

- advisory explanations;
- hypotheses;
- risk flags;
- scenario results;
- evidence needs;
- observation requests;
- draft planned interventions;
- BridgeCandidate proposals;
- review prompts;
- governance blockers.

They may not directly produce:

- accepted compliance facts;
- accepted current-state materializations;
- accepted operation execution consequences;
- pack activation/deactivation;
- attested documents;
- filed submissions;
- unqualified external disclosures;
- hidden truth-store updates.

## Required labels

Each world-model state or scenario result must carry explicit posture labels:

- `originTwin=ADVISORY`
- `advisoryOnly=true`
- `notCurrentStateMaterialization=true` where state-shaped
- `notComplianceState=true` where state-shaped
- `notThirdTwin=true` where state-shaped
- output disposition refs
- uncertainty statement refs where uncertainty matters
- validity or freshness posture
- invalidation rule refs where the output can become stale or unsafe

## Use in farmer-facing products

A farmer-facing brief may summarize world-model outputs only if it preserves:

- advisory status;
- stale or invalidated status;
- evidence gaps;
- missing observation needs;
- unresolved conflicts;
- human-review requirements.
