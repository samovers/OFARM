# OFARM runtime graph-pattern equivalence fixtures v0.1

Status:
- active supporting implementation artifact
- bounded `04_implementation_and_conformance/` hardening wave

Purpose:
- provide executable same-semantics query-graph equivalence coverage at the normalized internal-pattern layer
- keep this distinct from:
  - alias-governance fixture work
  - query-plan semantic-equivalence across execution targets
  - public query-language design

Fixture model:
- each scenario compares two bounded internal query fragments
- both fragments are normalized by:
  - alias-version path resolution
  - alias-version relation resolution
  - variable-name-insensitive graph canonicalization
- semantic posture stays part of equivalence:
  - twin selection matters
  - temporal frame matters
  - anchor identity set matters
  - optional versus required edges matter

Positive equivalence families:
1. variable renaming and predicate reordering
2. alias-version path equivalence
3. branch reordering under one anchor
4. lineage-branch equivalence
5. operation/evidence branch equivalence
6. identifier alias-version equivalence

Explicit non-equivalence families:
1. optional versus required edge
2. anchor shift
3. ComplianceTwin versus AdvisoryTwin posture shift
4. current-state versus as-observed temporal shift
5. alias-path drift
6. relation change

Important boundary:
- this suite does **not** prove cross-target query-plan equivalence
- this suite does **not** prove deployment-produced alias-regression stability
- this suite does **not** reopen query-language design

Expected result:
- all 12 scenarios pass
- graph-pattern equivalence row becomes `COVERED`
- query-plan semantic-equivalence across execution targets remains a separate row
