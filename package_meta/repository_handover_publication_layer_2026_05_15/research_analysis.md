# Research analysis — repository handover publication layer

Input: `06_active_supporting_research/source_inputs/deep-research-report-repository-cleanup-and-handover-readiness-2026-05-15.md`.

Applied implications:

1. Treat OFARM as a standards-style publication system, not a generic monorepo.
2. Encode authority/status in paths, sidecars, generated indexes, and validators.
3. Keep source schemas in `03_machine_contracts/`; move examples and fixtures to `04_implementation_and_conformance/`.
4. Add a short root `AGENTS.md`, thin `CLAUDE.md`, and generated `llms.txt` navigation surface.
5. Add `folder.status.json` sidecars for top-level and review-holding folders.
6. Add generated indexes under `package_meta/generated/` and a machine-readable `handover_gate.json`.
7. Normalize reviewer prompts and output schemas into reproducible workflow lanes.

Non-actions:

- No active OFARM law changed.
- No draft contract was promoted.
- No review-holding or legacy material was promoted.
- Accepted RFC physical-path splitting was deferred to avoid unnecessary active-reference churn.
