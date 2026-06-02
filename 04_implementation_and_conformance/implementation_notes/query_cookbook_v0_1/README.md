# OFARM Query Cookbook v0.1

Date: 2026-05-13  
Status: draft implementation/conformance support  
Phase: AI-agent-ready platform amendment Phase 4

## Purpose

This cookbook gives AI coding agents app-facing query examples. It is not model law and does not replace the active QuerySpecification, QueryPlanIR, or QueryExecutionResult contracts.

Each case must preserve:

- assertion/history-first truth
- materialization as governed derivative state
- advisory/compliance separation
- evidence and permission limitations
- stale/disputed/candidate-only/result-qualified states

## Cases in this folder

| Case | Purpose |
|---|---|
| `OFARM_QueryCookbookCase_field7_treatment_history_last_week_v0_1.json` | answer “what happened on Field 7 last week?” without treating projection as truth |
| `OFARM_QueryCookbookCase_field7_stale_materialization_block_v0_1.json` | show stale current-state blocking high-consequence output |
| `OFARM_QueryCookbookCase_permission_limited_evidence_v0_1.json` | show restricted evidence without fabricating “no evidence” |
| `OFARM_QueryCookbookCase_prescribed_vs_applied_rate_v0_1.json` | preserve prescribed versus accepted as-applied quantity distinctions |

## Cookbook result rule

Each case points to expected public read/result qualification behavior. The app must render safe labels from the qualification envelope rather than inventing labels from raw payload shape.
