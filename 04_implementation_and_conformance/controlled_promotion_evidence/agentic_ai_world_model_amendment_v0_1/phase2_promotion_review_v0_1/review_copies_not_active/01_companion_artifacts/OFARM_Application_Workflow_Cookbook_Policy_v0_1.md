<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: AMBER_SUPPORT_ONLY.
-->


# OFARM Application Workflow Cookbook Policy v0.1

Date: 2026-05-13  
Status: draft companion candidate under AI-agent-ready platform amendment  
Authority posture: implementation support only unless promoted

## Purpose

This policy defines how application workflow recipes should be written for AI coding agents. A recipe must show how a user-facing farm workflow crosses public OFARM platform surfaces without bypassing authority, evidence, promotion, pack, current-state, query, or publication law.

## Required shape of each recipe

Every recipe must include:

- scenario summary;
- intended builder use;
- source authority references;
- starting assumptions;
- step-by-step public operation calls;
- canonical states before and after each step;
- safe user-facing label for each step;
- forbidden labels and shortcuts;
- required preflight/dry-run behavior;
- required human approval flags;
- trace references expected from the platform;
- RuntimeProblem reason codes expected for failure cases;
- final-state acceptance checks.

## Mandatory workflow families

The first cookbook must cover:

1. field setup;
2. crop-cycle setup;
3. observation-to-decision;
4. recommendation-to-prescription-to-work-order;
5. execution claim and as-applied evidence;
6. delayed contractor sync;
7. correction and dispute;
8. inventory update;
9. treatment history/audit query;
10. PassportView and DocumentAssembly preview.

## Forbidden recipe patterns

A recipe must not teach an agent to:

- mutate the canonical assertion store directly;
- mutate a materialization store directly;
- save a query result as application truth;
- label an operation claim as accepted execution;
- label a recommendation as approved or compliant;
- use stale current state for high-consequence output;
- hide evidence gaps, redactions, disputes, or unresolved identity;
- treat an imported FMIS/machinery record as accepted truth;
- call every compiled output a passport.

## Promotion posture

This policy is a candidate companion artifact. It should remain under implementation/conformance until the cookbook and conformance gates pass two-agent compatibility testing.
