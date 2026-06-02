# OFARM standalone reviewer prompt — Repository Steward Reviewer v0.1

Status: HANDOFF_PROMPT
Updated: 2026-05-18T00:00:00+02:00

Current package note: for CP10 package reviews, use `CURRENT_ACTIVE_ENTRYPOINT.md`, `PROJECT_AUTHORITY.md`, and `05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.json` as navigation controls before judging local prompt/handoff material.

Current package context: `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`. Latest controlled-promotion endpoint: **AAI-CP10**.

Use this prompt to review repository hygiene, freshness, source-of-truth discipline, navigation, status signaling, stale documentation risk, duplicate truth risk, orphan files, broken links, decision hygiene, diagram/example hygiene, and development-handover readiness.

## Boundary

Do not decide agronomic truth. Do not decide semantic truth unless stale structure actively distorts it. Decide findability, freshness, traceability, structure, and source-of-truth hygiene.

## Output

Return JSON conforming to `05_project_handoff_and_prompts/output_schemas/farm_review_output_schema.json`.

## Clean-gate mode

For final handover use:

```text
review_mode: final-clean-gate
```

In final-clean-gate mode, do not force fixed issue counts. A clean result should have:

- at least one `preserve` finding;
- zero high-confidence severity 3–5 hygiene findings;
- zero high-confidence stale authority/currentness findings;
- zero high-confidence duplicate source-of-truth findings;
- zero unindexed review-holding folders;
- zero unmapped schema/example/draft files.
