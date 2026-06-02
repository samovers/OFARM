# Farm-RM 1.0.0 Package Index

## Pre-release source streams included

1. `specs/v0.1` core baseline
2. `specs/v0.2` soil and disease extension pack
3. `specs/v0.3` crop suitability extension pack
4. `specs/v0.4` comprehensive planning, risk, and regulation pack
5. `specs/v0.5` canonical observation/action archetype pack
6. `specs/v0.6` equipment-energy-telematics, multilingual, and ops-workflow/warehouse deltas (source lineage: v1.5 and v1.6)
7. `specs/v0.7` everyday field operations pack (planting, weed-control loop, storage condition/aeration, harvest intake traceability)
8. `specs/v0.8` agronomy archetypes, organic recordbook persistence, evidence controls, and cross-surface content-hardening pack (source lineage: v1.7)

## Machine-readable registries

1. Global artifact manifest: `specs/generated/fadl-manifest.json`
2. Per-stream generated artifacts:
   - `specs/v0.x/generated/archetypes-fadl/*.fadl`
   - `specs/v0.x/generated/archetypes-json/*.json`
   - `specs/v0.x/generated/templates-fadl/*.fadl`
   - `specs/v0.x/generated/templates-json/*.json`

## Primary normative assets

1. API: `specs/api/v1/openapi-farm-rm.yaml`
2. Release checklist: `specs/v1.0.0/release-checklist.md`
3. SQL migration streams:
   - `specs/v0.2/sql/migrations`
   - `specs/v0.3/sql/migrations`
   - `specs/v0.4/sql/migrations`
   - `specs/v0.6/sql/migrations`
   - `specs/v0.7/sql/migrations`
   - `specs/v0.8/sql/migrations`
4. Ontology and SHACL streams:
   - `specs/v0.1/ontology`, `specs/v0.1/constraints`
   - `specs/v0.2/ontology`, `specs/v0.2/constraints`
   - `specs/v0.3/ontology`, `specs/v0.3/constraints`
   - `specs/v0.4/ontology`, `specs/v0.4/constraints`
   - `specs/v0.5/ontology`, `specs/v0.5/constraints`
   - `specs/v0.6/ontology`, `specs/v0.6/constraints`
   - `specs/v0.7/ontology`, `specs/v0.7/constraints`
   - `specs/v0.8/ontology`, `specs/v0.8/constraints`

## Current release references

1. Phase 7 content-hardening package: `docs/implementation/phase-7-detailed-spec-content-hardening-package.md`
2. Phase 7 QA fixtures and signoff matrix:
   - `docs/research/farman-lite-content-gap-analysis/phase-7-fixture-pack.json`
   - `docs/research/farman-lite-content-gap-analysis/phase-7-signoff-matrix.csv`
