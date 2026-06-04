# CLEAN BASELINE CP11 MATERIALIZATION PROPOSAL

Generated or curated at: 2026-06-02T21:08:37+02:00

Phase: phase_1a - CP11 Hardening Rule Resolution

Outcome: NEEDS_CANONICAL_MATERIALIZATION

## 1. Source CP11 text

Source file:

`00_active_baseline/CP11_baseline_patch/CP11_Baseline_Patch_Text_FINAL.md`

Source text:

```md
9. **REPORT_ONLY_LIMIT is not a constraint strength.**
   Report-only posture belongs to objective/metric/priority surfaces, not hard constraints.
```

## 2. Target canonical baseline file

`00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

## 3. Target section or heading

`### CP11-C.3 Hard constraints and optimisation objectives`

Recommended insertion point:

After the existing paragraph that begins:

```md
A `SustainabilityObjective` is an optimisation target used to compare, rank, recommend, simulate, plan, or explain candidate actions.
```

## 4. Exact proposed insertion text

```md
Report-only posture is not a constraint strength. A report-only sustainability indicator, metric posture, objective note, or priority annotation may require disclosure, monitoring, evidence request, or review, but it must not be represented as a `SustainabilityConstraint` or used as a hard-constraint pass/fail condition unless separate active charter law classifies it as a hard constraint. Report-only posture belongs to objective, metric, or priority surfaces and remains subordinate to hard constraints, evidence sufficiency, claim-basis, authority, and output-qualification gates.
```

## 5. Why this is not new law

This is materialization of accepted CP11 hardening text, not a semantic expansion. The CP11 final baseline patch already states that `REPORT_ONLY_LIMIT` is not a constraint strength and that report-only posture belongs to objective, metric, or priority surfaces, not hard constraints.

The five canonical active baseline files already distinguish `SustainabilityConstraint`, `SustainabilityObjective`, hard constraints, metric method posture, and `ObjectivePriority`. The missing piece is the explicit report-only posture rule from the accepted CP11 patch text.

## 6. Semantic risk

Risk is low if inserted into `CP11-C.3` because the text only preserves the CP11 distinction between hard constraints and non-hard objective, metric, or priority surfaces.

Residual risk is that the phrase `REPORT_ONLY_LIMIT` may imply a named enum or machine-contract value. The proposed text avoids promoting any schema enum or draft contract. It names report-only posture generically and keeps machine-contract promotion out of scope.

## 7. Validation required after approval

After approval and materialization, run non-mutating checks first:

```bash
git status --short
python3 -c "import json; [json.load(open(p)) for p in ['CLEAN_BASELINE_CURRENTNESS_STRING_AUDIT.json', 'CLEAN_BASELINE_COMPLETION_LEDGER.json', 'CLEAN_BASELINE_SEMANTIC_EQUIVALENCE_LEDGER.json']]; print('json parse ok')"
rg -n "Report-only posture is not a constraint strength|REPORT_ONLY_LIMIT|report-only|report only|constraint strength|ObjectivePriority|SustainabilityConstraint" 00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
```

Later full package validation remains required before package readiness, but should wait until the phase that allows conformance runners that may write tracked result files.

## 8. Companion, runtime, or alignment cross-reference need

No immediate companion, runtime, or alignment cross-reference is required for the minimal materialization.

Reason:

- `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md` already distinguishes hard constraints, objectives, objective priorities, metric method posture, and runtime outcome distinctions.
- `OFARM_Alignment_Register_v0_13.md` already includes `SustainabilityConstraint`, `SustainabilityObjective`, `ObjectivePriority`, and `SustainabilityMetricProfile`.
- The missing accepted CP11 text is best materialized in the Constitution where the hard-constraint/objective boundary is normative.

If later navigation wants a machine-readable currentness note for `REPORT_ONLY_LIMIT`, that should be handled in a later index or contract-currentness phase without promoting draft/non-default CP11 contracts.
