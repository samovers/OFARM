# Independent review of material occupancy R2

**Result: the R1 P2 finding is resolved; no new finding in the reviewed scope.** The review stayed within material occupancy source evidence integrity. It changed no owner candidate, source law, foreign schema, runtime integration, Git state, CI or publication. R1 and its sealed independent review remain unchanged.

The reviewed candidate is `../review-repair-02/`, delivery seal `8ce0fbd3c70a259f15de2b8a2398e50f78d79d65311cfee354cbe26794d5ede4`, raw contract SHA-256 `bbb2a060c62e05ca8f17f2dcda0d36e182a6127e75579df637b8c179a7479f0f`. All 729 manifest members match, with no omissions or extras. All 728 integration mappings have distinct safe destinations and install byte-for-byte into separate contract, checker and fixture roots.

The complete candidate was frozen before testing in `snapshot/`, including its delivery manifest. `SNAPSHOT_MANIFEST.json` covers 730 files and has SHA-256 `38e676f59127c772314261d2f87b08343da300469e50cf37c24a6ac5573de4d7`. The reviewed code adds six lines to check known start, known end and finite open-end observation against the full source applicability before returning unresolved for an unknown opposite endpoint. The contract prose clarifies the same requirement; five author regressions cover the repaired cases. Schemas and original semantic source bytes did not change. `candidate-delta.json` records the complete file delta.

## R1 finding resolution

Each saved reproduction uses the exact original R1 request, context, file map and supporting source bytes. Only the independently selected contract pin changes to R2. `exact-replay/` records per-file hashes, both reports and exact CLI arguments. All five previously accepted contradictions now fail with `INPUT_ERROR`, an explicit temporal error and an empty episode array; the installed CLI exits 1.

| Original reproduction | R2 error |
| --- | --- |
| `temporal/unknown-end/after` | `KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY` |
| `temporal/unknown-end/equal-exclusive` | `KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY` |
| `temporal/unknown-start/before` | `KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY` |
| `temporal/unknown-start/equal-exclusive` | `KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY` |
| `temporal/unknown-start-open/before` | `OPEN_END_OBSERVATION_EXCLUDES_SOURCE_APPLICABILITY` |

Compatible known boundaries paired with unknown endpoints still match, retain `temporalCoverage: UNRESOLVED`, and keep `selectedPostureSupportsUnqualifiedClaim: false`. Equal-inclusive boundaries and compatible open-end observations are preserved. Existing known-opposite negative controls remain rejected, now with the specific `INPUT_ERROR` instead of the earlier generic `MISMATCH`. The consumer must continue treating either status as failure.

Sixteen additional interval checks confirm that each known boundary covers the entire source applicability, including both endpoint-inclusion combinations. A boundary that covers the narrower selected query but excludes part of the source interval is rejected. These checks also preserve compatible unresolved intervals. Nanosecond distinctions remain covered by the original repro corpus.

## Verification

- **377/377 prior independent checks passed.** The same ordered case names and expected outcomes were replayed without changing test logic. Only the probe docstring and reviewed-seal metadata changed. `probe-reuse.json` and `corpus-continuity.json` record that continuity.
- **23/23 saved original cases passed through the API, and 23/23 through the installed CLI.** This includes all five exact R1 failures, unknown-positive cases, known-boundary controls, same-identity rejection, empty inventory, repeated/overlapping episodes and errors after earlier episodes. Request, context and supporting bytes are unchanged from the R1 review.
- **16/16 wider source-applicability interval checks passed.** The input packages and reports are retained in `interval-cases/`.
- **209/209 author conformance checks passed**, including 47 positive fixtures and 35 combinations of complete foreign event and measurement bodies.
- The prior corpus includes all 47 fixtures through the installed API, ten installed CLI comparisons, 200 semantic-leaf mismatches, source-manifest and independent-pin failures, 30 malformed-input probes, both same-identity repairs and selected empty inventory. All error cases return no partial accepted episode set. Missing source-root and changed semantic source bytes fail.

Post-test verification checks the original R2 candidate, its frozen snapshot, all installed mappings, the original R1 candidate, and the entire sealed R1 independent review. `verification.json` records these checks. `REVIEW_MANIFEST.json` seals this review and its evidence.

## Limits and handoff

This establishes the repaired comparison behavior against the exact reviewed offline interface. Test contexts and their independent caller pins are fictional. Supporting bytes remain owned by their existing validators. A matched report does not establish source truth, actual owner authority, currentness, live-store inventory completeness, event or measurement admission, runtime protection, authorization eligibility, or permission to promote an assertion. Runtime admission and actual inventory completeness remain `NOT_ESTABLISHED`.

Next: integrate only the exact R2 candidate above through the intended material occupancy evidence PR boundary, then perform the separate consumer integration and its checks.
