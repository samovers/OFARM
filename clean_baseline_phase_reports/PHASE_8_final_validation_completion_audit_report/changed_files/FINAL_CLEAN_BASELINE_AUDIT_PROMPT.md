# Final Clean Baseline Audit Prompt

You are auditing the OFARM 2 CP15 materialized development baseline after Phase 8 and before final packaging.

Current package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`.
Latest controlled amendment: `CP15`.

Determine one of these outcomes:

- `ACCEPT_AS_CLEAN_BASELINE`
- `ACCEPT_WITH_MINOR_DEBT`
- `DO_NOT_ACCEPT`

Audit the repository against these questions:

1. Do the root entrypoints present current material first, lineage second, and archive/history third?
2. Do current reader views clearly state that they do not override canonical authority?
3. Do the five canonical active baseline files remain present and authoritative?
4. Are CP11 through CP15 baseline-patch effects materialized or explicitly evidenced as lineage?
5. Does CP15 merge evidence point to the relocated final acceptance gate under `package_meta/history/controlled_amendments/`?
6. Are `03_machine_contracts/schemas/` and `03_machine_contracts/drafts_non_default/` still unmoved, with drafts unpromoted?
7. Are generated views marked derived and non-authoritative?
8. Are `legacy_reference/` and `07_linked_domain_architectures/` root-visible but non-default in their stated roles?
9. Did the full validation suite and CP10, CP12, CP13, CP14, and CP15 runners pass?
10. Are there blockers or only explicitly accepted minor debt?

Use `CLEAN_BASELINE_FINAL_VALIDATION_LEDGER.json`, `CLEAN_BASELINE_FINAL_COMPLETION_AUDIT.json`, `CLEAN_BASELINE_FINAL_PACKAGE_READINESS.json`, and the Phase 8 report package as evidence. Do not assume final packaging has already occurred.
