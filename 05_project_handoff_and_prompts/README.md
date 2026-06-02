# 05_project_handoff_and_prompts

Status: supporting handoff, prompt, reviewer-workflow, output-schema, and evaluation material only. This folder does not create active OFARM law.

Current package context: `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`. Latest controlled-promotion endpoint: **AAI-CP10**.

Use this lane for reproducible prompting, handoff, reviewer output validation, and historical review maps. Before relying on any prompt here, read the active package entrypoints:

1. `CURRENT_ACTIVE_ENTRYPOINT.md`
2. `PROJECT_AUTHORITY.md`
3. `ACTIVE_SUBSTANCE_README.md`

Current structure:

- `prompts/` — reusable project, deep-research, handoff, and reviewer prompts.
- `output_schemas/` — JSON schemas for structured reviewer outputs.
- `eval_datasets/` — reserved lane for reviewer/evaluator datasets.
- `review_runs/` — reserved lane for reproducible review-run records.
- `reports_and_maps/` — historical handoff reports, slotting maps, and consistency notes.

Navigation:

- `HANDOFF_PROMPT_INDEX.json` — machine-readable index for this entire lane.
- `HANDOFF_PROMPT_INDEX.md` — human-readable index for this entire lane.
- `prompts/REVIEWER_PROMPT_INDEX.json` — reviewer/prompt and output-schema index.
- `prompts/REVIEWER_PROMPT_INDEX.md` — human-readable reviewer/prompt index.

Authority boundary:

- prompt text is a workflow aid, not active law;
- old prompt starting points may be historical and must be checked against `CURRENT_ACTIVE_ENTRYPOINT.md`;
- review outputs do not become governance decisions unless later promoted through the active decision process;
- this folder does not override CP10 claim limits.
