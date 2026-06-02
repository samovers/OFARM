# OFARM 1.0.0 Package

This directory is the stable release package baseline for OFARM. Legacy file paths and artifact names still retain `Farm-RM` where compatibility matters.

## Release status

1. `packageVersion`: `1.0.0` (stable baseline package root)
2. `currentReleaseTag`: `v1.0.26` (latest published patch release)
3. `status`: stable
4. `published`: `2026-03-28`

## Packaging model

1. `v1.0.0` is the public release package version.
2. Historical design iterations are preserved as pre-release streams:
   - `specs/v0.1` (formerly `v1`)
   - `specs/v0.2` (formerly `v1.1`)
   - `specs/v0.3` (formerly `v1.2`)
   - `specs/v0.4` (formerly `v1.3`)
   - `specs/v0.5` (formerly `v1.4`)
   - `specs/v0.6` (formerly `v1.5`, plus additive `v1.6` deltas)
   - `specs/v0.7` (v1.6 everyday field operations extension stream)
   - `specs/v0.8` (v1.7 agronomy, recordbook persistence, and evidence controls extension stream)

## Canonical entry points for implementers

1. Release manifest: `specs/v1.0.0/release-manifest.json`
2. Source package index: `specs/v1.0.0/package-index.md`
3. Machine artifact registry: `specs/generated/fadl-manifest.json`
4. API contract: `specs/api/v1/openapi-farm-rm.yaml`
5. Release playbook: `specs/v1.0.0/release-checklist.md`

## Notes

1. Archetype IDs remain at their existing artifact-level IDs (for example `.v1` suffixes).
2. Release versioning and artifact versioning are intentionally separate.
3. Patch releases (`v1.0.x`) can update APIs, rule packs, templates, and docs without renumbering the stable package root folder.
4. Local integration delta log for profile-backed dev bootstrap: `specs/v1.0.0/deltas/v1.0.8-local-dev-profile-bootstrap.md`.
5. `v1.0.26` publishes the voice session protocol closeout, transport recovery routes, and refreshed stable bundle metadata so the packaged OpenAPI artifact matches the current checked-in contract on the active branch.
