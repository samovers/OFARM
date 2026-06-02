# OFARM Wave 19 event-family and promotion hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded continuation after Wave 18

## Decision

The next continuation step should close the event-grammar conformance seam rather than drift deeper into bridge rehearsal or reopen architecture.

## Why this wave

After Wave 18, the main central uncovered rows were still:

- event-family coverage and subtype-compatibility checks
- commit-promotion safety checks
- profile compatibility
- alignment-register coverage
- graph-pattern equivalence

The event-grammar seam is the most central because it sits directly under:

- OFARM's small fixed top-level event grammar
- the dominant-semantic-consequence selection rule
- the distinction between event families and commit classes
- the promotion matrix that prevents weak inputs from silently becoming hard truth

This wave therefore adds executable proof for:

- all seven top-level event families
- subtype allow/block/review outcomes
- runtime-shaped promotion traces across all nine commit classes

## Change class

Implementation/conformance implication only.

## Files intentionally not changed

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

## Expected coverage movement

- `event-family coverage and subtype-compatibility checks` should move from `NOT_STARTED` to `COVERED`
- `commit-promotion safety checks` should move from `PARTIAL` to `COVERED`
- `event-subtype merge fixtures` should remain `PARTIAL`, but with stronger evidence because runtime subtype compatibility is now explicit

## Risk guardrail

This wave does not claim deployment event telemetry or full pack-merge legality for conflicting event subtype declarations.
It only closes the bounded conformance seam required by the active event grammar and promotion law.
