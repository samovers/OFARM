# OFARM Farm-Owner Predeployment Adapter MVP Scope v0.1

Generated: 2026-05-13T17:53:02+00:00

## MVP purpose

Build a shadow adapter for existing FMIS/KIS data before OFARM deployment. The adapter is not a live OFARM runtime and must not mutate governed current state.

## Required outputs

- source inventory summary;
- candidate execution/intervention/material/storage records;
- temporal qualifier assignment;
- unresolved actor identity markers;
- evidence-reference mappings;
- report-basis classification;
- review queue;
- loss map;
- high-consequence output block status;
- export/portability caveats.

## Strictly forbidden outputs

- accepted governance facts;
- auto-promoted Compliance Twin decisions;
- contractor/carrier identity inferred from hints alone;
- document references promoted to custody-grade evidence;
- report marts promoted to frozen submissions;
- current-state projections treated as canonical truth.

## Minimum acceptance criteria

1. Every imported record is candidate-only unless review/promotion proof exists.
2. Every missing evidence/review/actor/report/export basis produces a review gap or loss-map item.
3. Every high-consequence output is blocked from candidate-only imports.
4. Every unresolved actor remains unresolved rather than guessed.
5. Every current-state projection has a declared basis or is rejected as hidden truth.
