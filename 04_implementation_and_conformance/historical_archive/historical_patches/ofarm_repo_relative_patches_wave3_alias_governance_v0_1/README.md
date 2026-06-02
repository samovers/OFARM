# Wave 3 alias governance patch bundle v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: repo-relative patch bundle for the Wave 3 alias-governance and query-reproducibility closure pass

---

## What this patch contains

This patch adds:
- the accepted RFC for `SemanticPathAlias` governance closure
- the `SemanticPathAliasCatalog` and `SemanticPathAliasResolutionTrace` machine contracts
- starter query fixtures for active, deprecated, and unpinned alias cases
- starter resolution traces for direct resolution, deprecated rollover, and ambiguity hard-fail
- an alternate `QueryPlanIR` example for cross-target semantic-equivalence checking
- v0.5 machine-contract validation runner/results
- alias-governance fixture runner/results
- conformance matrix updates
- package index/status updates, excluding the patch bundle directory itself

## Apply posture

This is a repo-relative unified diff against the package state represented by:
- `OFARM2_project_migration_seed_v0_6_wave2_context_snapshot_v0_1.zip`

The patch file intentionally excludes the patch bundle directory itself.

## Patch file

- `OFARM_wave3_alias_governance_v0_1.patch`
