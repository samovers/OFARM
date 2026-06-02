# OFARM repository cleanup initial audit

Generated: 2026-05-15T15:30:00+02:00

Scope: repository cleanup and development-handover readiness only. This cleanup does not change active OFARM semantic or runtime law.

## Counts before cleanup

- Total files: 5031
- Root files: 23
- `03_machine_contracts/` root files: 10
- `04_implementation_and_conformance/` root files: 3
- Draft-named machine-contract files: 30

## Main cleanup targets

1. Remove obsolete patch guides and package-specific READMEs from root.
2. Regenerate stale authority/navigation metadata.
3. Normalize review-holding folders.
4. Create exhaustive machine-contract indexes and separate contract files by family/kind.
5. Move implementation/conformance root files into bounded lanes.
6. Add reviewer-output schema and reviewer prompt index.
7. Add decision, audit-stress-chain, and development-handover indexes.
8. Expand repository hygiene validation.
