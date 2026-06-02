# OFARM Operational Break Test Suite v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance  
Amendment line: ONT-SEMINT v0.2 / Phase 5

## Purpose

This suite converts the ontology-steward stress checks into package-local break tests. It complements the AGR-P8 runtime-chain fixtures and the Phase 4 Belgium currentness profile.

## Break tests

1. Delayed contractor sync after revoked authority, partial execution, correction, and dispute.
2. Stale or unpinned query alias plus conflicting product binding.
3. Recommendation → prescription → execution claim → as-applied evidence → accepted consequence.
4. Observation → treatment decision → audit reconstruction.
5. Schema / glossary / example semantic divergence detection.

## Expected result

Every scenario must either pass with a governed promotion path or fail closed / require review. No scenario may silently promote Advisory output, machine logs, free text, GTIN-only identity, stale current state, disputed material, or unresolved external bindings into compliance truth.

## Non-claims

This is package-local conformance evidence only. It does not claim production runtime readiness or live registry integration.
