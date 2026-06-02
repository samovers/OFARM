# OFARM advisory cohort benchmark real-pilot runbook v0.3

## Purpose

Run one bounded redacted tenant cohort through the advisory benchmark seam without changing OFARM architecture again.

This runbook assumes the active posture already agreed:
- operations and evidence remain the authoritative substrate
- receipt/invoice capture remains document-first with reviewed extracts
- benchmarking lives in the Advisory Twin only
- cross-tenant visibility remains explicit-share-only and disclosure-controlled
- outputs remain bounded `VIEW_MODULE` / `SUMMARY_ROWS`
- no raw row disclosure, no shadow ledger, no procurement system semantics

## Pilot scope

Run exactly these bounded benchmark cases:

1. **Fertilizer product-class cohort benchmark**  
2. **Seed exact-product cohort benchmark** only if normalization, cohort size, dominance, and request history all pass  
3. **One broadened or blocked request-history case** to prove differencing control  
4. **One revocation/recompute case** to prove stale view refusal and fresh recompute behavior

Do **not** expand to:
- raw peer spend inspection
- generalized analytics
- arbitrary pivots or distributions
- whole-farm accounting
- AP/AR or ledger semantics

## Inputs

Use `OFARM_advisory_cohort_benchmark_real_pilot_dataset_template_v0_3.json` as the intake shape.

Fill it with:
- stable redacted tenant / farm / viewer refs
- explicit share-grant refs
- reviewed extract refs
- evidence refs only, not raw documents
- normalized product class / product refs
- quantity, unit, amount, and comparability basis
- one request-history block or broaden case
- one revocation simulation or real revocation event if available

## Execution steps

1. Redact the dataset according to the sovereignty note.  
2. Fill the dataset template and save it as a new JSON file.  
3. Run the validator first.  
4. If the dataset is `READY_FOR_REAL_PILOT_EXECUTION`, run the pilot runner.  
5. Review the JSON result set and markdown summary.  
6. Confirm the surface still hides exact contributor count, raw rows, raw evidence, peer total spend, and forbidden metrics.  
7. Keep all outputs in Advisory-only posture.  
8. If stronger claims are requested, stop and narrow instead of widening semantics.

## Command examples

```bash
python ofarm_advisory_cohort_benchmark_real_pilot_validator_v0_3.py real_benchmark_pilot_dataset.json readiness_report.json
python ofarm_advisory_cohort_benchmark_real_pilot_runner_v0_3.py real_benchmark_pilot_dataset.json benchmark_results.json benchmark_summary.md
```

## Stop rules

Stop the pilot immediately if any of these happens:
- the request surface starts showing raw peer rows, raw evidence refs, exact contributor count, peer total spend, or spend-per-hectare
- the implementation starts behaving like a second economic truth store
- share-grant or reviewed-extract posture is missing
- exact-product benchmarking is served without passing normalization and request-history safety
- revoked contributions remain visible in a supposedly fresh benchmark view
- Advisory output is treated as Compliance truth

## Expected honest outcomes

- a fertilizer product-class benchmark card may be served
- a seed exact-product benchmark card may be served only if the safe conditions hold
- unsafe exact-product narrowing should broaden or refuse
- stale/invalid materialization should refuse until recompute completes

Anything stronger than that is a bug, not a success.
