# Independent review of material occupancy R1

**Result: one P2 finding; repair before integration.** This review stayed within the material occupancy source evidence trust boundary. It made no changes to the owner candidate, source law, foreign schemas, runtime admission, Git, CI or publication. Any repair belongs in a new sibling candidate and must receive its own seal and review.

The reviewed candidate is `../review-repair-01/`. Its delivery manifest SHA-256 is `b9e97569b5cfb27d6d61f28af347857fb178717792a10e9bcf8c24b7d9d29d13`; its raw contract SHA-256 is `b93369fcbcc958888d7550b3f83625fa3102db08e0cc4d51dae7d50df6261488`. All 728 declared members match, and there are no unlisted files. The 727 integration mappings have distinct safe destinations and match their declared bytes. The manifest and integration map are construction-only as declared.

The full candidate, including its manifest, was copied before testing into `snapshot/`. `SNAPSHOT_MANIFEST.json` seals those 729 files; its SHA-256 is `ec0ba8a7b56fb0910471d69f6f48d80ee3af75cf80d157e75faf9c8008646a1e`. Post-test checks found no changes in either the snapshot or original candidate.

## P2: Unknown endpoint masks a contradictory known endpoint

In `snapshot/verify_occupancy.py`, lines 118–119 return unresolved temporal coverage immediately if either endpoint is unknown. Lines 270–272 then skip the source-applicability coverage error whenever that is true. This removes checks on the other, known endpoint. `snapshot/CONTRACT.md` requires known occupancy endpoints to cover the source's applicability. An unknown endpoint should leave coverage unresolved only when the known constraints do not already contradict that applicability.

All five independent reproductions preserve complete original source bytes, source selectors, raw hashes, value digests, expected facts and independently selected fictional caller pins. The selected applicability is `2026-10-20T10:00:00Z`.

| Saved case under `cases/temporal/` | Contradictory fact |
| --- | --- |
| `unknown-end/after` | Known start is one nanosecond after applicability; end is unknown. |
| `unknown-end/equal-exclusive` | Known start equals applicability but excludes it; end is unknown. |
| `unknown-start/before` | Known end is one nanosecond before applicability; start is unknown. |
| `unknown-start/equal-exclusive` | Known end equals applicability but excludes it; start is unknown. |
| `unknown-start-open/before` | Open-end observation is one second before applicability; start is unknown. |

Expected: reject contradictory temporal facts and return no accepted episode set. Observed: `MATCHED_SELECTED_OCCUPANCY_EVIDENCE`, no errors, one retained episode, and `temporalCoverage: UNRESOLVED`. The corresponding known-opposite controls correctly return `MISMATCH` with `OCCUPANCY_INTERVAL_DOES_NOT_COVER_SOURCE_APPLICABILITY`. Equal-inclusive and compatible endpoints remain matched and unresolved when the other endpoint is unknown, which is the intended distinction.

This is a conditional comparison defect, not a demonstrated admission or authorization bypass. Each unexpected success still reports `selectedPostureSupportsUnqualifiedClaim: false`, `runtimeAdmission: NOT_ESTABLISHED` and `actualInventoryCompleteness: NOT_ESTABLISHED`. Those qualifications limit the impact but do not satisfy the contract's rejection requirement.

Suggested repair: compare each known start, known end, and finite open-end observation independently against the full source applicability, including endpoint inclusion. Reject any contradiction before representing remaining unknown coverage as unresolved. Preserve unknown facts, nanosecond precision and original source bytes. Do not infer a missing boundary or add lifecycle law.

## Verification and limits

The author conformance rerun passed all 204 checks, including 47 positive fixtures and 35 combinations of full foreign event and measurement bodies. The independent suite completed 377 checks: 372 behaved as expected and five exposed the single finding above. `independent-results.json` records every outcome; `independent_probes.py` records the independently authored construction and oracle. Test pins are explicitly fictional selected inputs, not authentic production owner decisions.

Independent coverage includes:

- All 47 baseline cases retain exact facts, selectors and selected record mappings, including mixed revision/digest references, repeated and overlapping episodes, historical/disputed/superseded/unresolved posture, and zero episodes.
- Both same-identity repairs reject a LOT occupant and CONTAINER place with the same logical ref, including different revisions with complete source closure.
- Two hundred changed semantic leaves across full amount, unit, quantity kind, cohort, extent and posture variants are rejected without changing the selected source bytes.
- Missing, extra, duplicate, reordered and incorrectly mapped source/episode inventories fail. Changed raw bytes and all three wrong independent pins fail.
- Thirty malformed request, context and supporting-JSON cases cover duplicate names, invalid UTF-8, BOMs, nonfinite/overflow/unsafe numbers, excessive depth and size, surrogates and trailing input.
- Semantic failure in a later episode and an exception in the third episode both clear the entire accepted episode array. No failure checked by the suite retained a partial accepted episode set.
- All 727 mappings install byte-for-byte into separate contract, checker and fixture roots. All 47 baseline cases pass the installed API. Ten installed CLI checks agree exactly with API reports and exit codes, including three of the contradictory temporal cases, negative controls, same-identity rejection, empty inventory, overlap and later-episode failures. Missing source-root and changed semantic source bytes fail.

Supporting records remain opaque to this owner verifier. Tests do not establish their source truth, actual owner authority, currentness, exhaustive live-store inventory, event or measurement admission, runtime protection, or permission to promote an assertion. A matched report is conditional fidelity to the independently selected owner inputs.

## Reproduction

Each persisted case contains original request/context/source bytes, a CLI file map, selected test pins and its API report. CLI cases also contain `cli-execution.json` with exact arguments and `cli-report.json`. For example, from this review directory with the pinned local Python dependencies selected:

```sh
python3 -B installed/04_implementation_and_conformance/conformance_runners/material_occupancy_evidence/verify_occupancy.py \
  --request cases/temporal/unknown-end/after/request.json \
  --context cases/temporal/unknown-end/after/context.json \
  --record-map cases/temporal/unknown-end/after/record-map.json \
  --trusted-pins cases/temporal/unknown-end/after/trusted-pins.json \
  --package-root installed/03_machine_contracts/drafts_non_default/material_occupancy_evidence \
  --source-root installed/04_implementation_and_conformance/examples_and_fixtures/fixtures/material_occupancy_evidence
```

This returns exit code 0 and the erroneous matched report on frozen R1. Use `cases/temporal/control-start/after/` for the corresponding rejected control.

Next: the owner should repair the temporal comparison in a separately sealed sibling revision, then submit that exact revision for an independent recheck before integration.
