# Version Map (Pre-release to Stable Package)

This map documents the renumbering applied before first deployment.

## Stream mapping

1. `v1` -> `v0.1`
2. `v1.1` -> `v0.2`
3. `v1.2` -> `v0.3`
4. `v1.3` -> `v0.4`
5. `v1.4` -> `v0.5`
6. `v1.5` -> `v0.6`
7. `v1.6` -> `v0.6`
8. `v1.6` (everyday field ops extension stream) -> `v0.7`
9. `v1.7` -> `v0.8`

Note:
`v0.6` and `v0.7` are shared pre-release streams containing additive `v1.6` deltas before stable repackaging. The `v0.7` stream holds the everyday field-operations extension pack.

## Why

1. No production deployment had occurred yet.
2. Historical streams are therefore treated as pre-release design history.
3. Stable package starts at `v1.0.0`.

## Post-1.0 release policy

1. Stable package root remains `specs/v1.0.0` across patch releases.
2. Patch releases are published with SemVer tags (`v1.0.1`, `v1.0.2`, `v1.0.3`, ...).
3. Release tag metadata is tracked in `specs/v1.0.0/release-manifest.json`.
4. Folder renumbering under `specs/` is reserved for future major/minor baseline package changes.

## Scope of change

1. Folder-level renumbering completed under `specs/`.
2. Internal repository path references updated from `specs/v1*` to `specs/v0.*`.
3. Generated artifact registries were rebuilt after renumbering.
