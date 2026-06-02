
> **OFARM 2 legacy currentness note**  
> This file is preserved inside `legacy_reference/` as read-only historical context. It does not define active OFARM 2 law, active schema authority, current package status, or implementation direction. Read the active authority set and `legacy_reference/LEGACY_REFERENCE_INDEX.json` before using this material.

# Agronomy Archetype Authority Review

This folder contains a one-archetype-at-a-time re-review of the Farm-RM v0.8 agronomy archetype set (58 archetypes)
against authoritative agronomy guidance:

1. Extension / university protocols and how-to guidance (field/lab protocol, recordkeeping norms).
2. Standards / method references (ISO/ASTM/AOAC/ASABE/EPPO/USDA/FAO/GS1/ISO-traceability, as applicable).
3. Peer-reviewed scientific literature (papers or review papers).

For each archetype:

- If **no change** is needed, we produce a citation-backed memo explaining why it is sufficient.
- If a **change** is needed, we produce a decision-complete change spec (archetype + vocab + SHACL + SQL + API + tests impact).

Implementation of model/schema changes is intentionally out of scope for this review folder unless explicitly requested.

## Files

- `tracker.md`: canonical checklist of the 58 archetypes and their review status.
- `gap-analysis.md`: roll-up of cross-cutting gaps and recommended backlog after all reviews.
- `archetypes/*.review.md`: one review per archetype.

## Status Codes

- `pending`: not yet reviewed.
- `in_review`: currently being reviewed (one-at-a-time rule).
- `no_change`: review complete; no changes required.
- `change_spec_ready`: review complete; changes required and spec is written (but not implemented).

## Citation Format

Each archetype review uses reference IDs like:

- `[EXT-01]` for extension/university sources
- `[STD-01]` for standards/method references
- `[PAPER-01]` for peer-reviewed papers

Each requirement statement in the review must cite at least one reference ID.
