# Mutation evidence and remaining redundancy

This is author-side fault-injection evidence, not runtime attestation or a formal two-reviewer gate. The harness clones only the verifier function's AST into a separate in-memory function and removes one `must()` call at a time. It does not change the installed files or disable package, helper, schema or digest checks. The instrumented baseline must satisfy the same exact code/detail oracles as the ordinary API.

The final corpus has 493 API cases: 491 portable cases plus two invalid-map-argument cases that cannot be represented by the closed wire schema. It executes all 115 static `must()` sites. There are direct first-error negative witnesses for 112 sites:

- Removing 84 sites makes at least one formerly rejected case return PASS.
- Removing 28 sites changes the expected error code or required detail, so the conformance test fails. These are reported separately from newly accepted inputs; a changed error is not described as an admission bypass.
- No directly witnessed mutant retains the same expected error in all its exercised witnesses.

The other three sites execute on valid input but have no independently reachable failure branch after earlier checks. They remain as repeated defensive comparisons. They are not counted as mutation kills and were not subjected to an exhaustive whole-corpus removal run.

| Repeated check | Earlier guard and reason its failure is unreachable |
| --- | --- |
| `BASIS_REFERENCE_CLOSURE_MISMATCH` (line 165) | `TRACE_PATH_BASIS_CLOSURE_MISMATCH` (line 154) already checks the identical ordered binding list for every trace path, including the chosen path. The chosen object is the object from that list; nothing mutates it before the repeated check. |
| `BASIS_SOURCE_BINDING_MISMATCH` (line 168) | `TRACE_PATH_SOURCE_MISMATCH` (line 158) already compares the same basis entry's binding and artifact family with the same catalog record. `use()` only adds a key to a set; it does not change those values. |
| `SNAPSHOT_VISIBILITY_LINK_MISMATCH` (line 172) | `TRACE_PATH_VISIBILITY_MISMATCH` (line 159) already compares the same source and snapshot bindings. Closed bindings contain strings, so the earlier canonical equality implies the later ordinary equality for the source binding. No intervening mutation changes them. |

`mutation-results.json` contains every check site, expression, witness, observed result, and classification. `mutation-coverage-ledger.json` records the explicit redundancy classification. This evidence covers `must()` guards; it does not claim exhaustive mutation coverage of every Python operation, schema keyword, dependency, helper function, or the CLI. Helper-origin behavior has seven separate fresh-process probes, and installed runner oracle enforcement has two separate probes.

Next: independently verify the exact sealed code and witnesses, keeping newly accepted negatives distinct from changed-error detections.
