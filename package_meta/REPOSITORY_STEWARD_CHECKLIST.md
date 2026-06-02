# Repository steward checklist

Run on every cleanup or handover build.

1. Verify package SHA and ZIP extraction.
2. Run `python3 package_meta/tools/validate_repo_hygiene.py`.
3. Run `python3 package_meta/tools/check_generated_currentness.py`.
4. Confirm root has no obsolete overlay guides, patch guides, or stray generated reports.
5. Confirm every top-level folder has `folder.status.json` and review-held snapshots are archived/indexed under `archive/review_holding/`.
6. Confirm `AGENTS.md`, `CLAUDE.md`, `llms.txt`, and `.claude/rules/archive.md` exist and agree.
7. Confirm `03_machine_contracts/` contains source contracts/maps only, while examples/fixtures live under tier 04.
8. Confirm every tier-04 machine-contract example is mapped in `03_machine_contracts/EXAMPLE_SCHEMA_MAP.json`.
9. Confirm draft/non-default files are indexed and not marked default.
10. Confirm reviewer prompts and output schemas are under `05_project_handoff_and_prompts/prompts/` and `output_schemas/`.
11. Confirm source inputs and source-context material are checksum-locked.
12. Confirm `package_meta/PACKAGE_META_INDEX.json` path sets and hashes are current.
13. Confirm generated indexes match their source indexes or authoritative status maps.
14. Confirm `package_meta/generated/handover_gate.json` records a passing currentness gate.
15. Confirm no review-holding, legacy, research, prompt, or package-metadata file is used as active law.
