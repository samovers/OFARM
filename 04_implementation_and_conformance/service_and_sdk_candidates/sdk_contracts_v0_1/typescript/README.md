# TypeScript SDK shape candidate

This is a shape contract, not production SDK code.

The safe client exposes explicit OFARM operations such as `commits.dryRun`, `commits.submit`, `queries.plan`, `queries.execute`, `materializations.get`, `assemblies.preview`, `identity.resolve`, and `imports.submitCandidate`.

Forbidden: generic CRUD helpers for truth objects, direct projection mutation, and local promotion/materialization helpers.
