# Thread integration note — 2026-04-15

Status: historical package assembly note
Current package entrypoint: `../../README.md`
Current change trail: `../../CURRENT_PACKAGE_CHANGELOG.md`


This package fixes the earlier packaging mistake where the OFARM source tree was wrapped under a generic `source/` directory.

The project root in this package is the OFARM source tree itself. Thread outputs from the current architectural pre-implementation work are carried under `reviewed_preimplementation_thread_v0_2/` so they are **inside the package** without being mislabeled as already-merged active law.

This package preserves three things at once:
1. the authoritative migrated source tree,
2. the reviewed thread artifacts in source-like category structure,
3. the phase and review history needed to understand what was carried forward, deferred, or superseded.
