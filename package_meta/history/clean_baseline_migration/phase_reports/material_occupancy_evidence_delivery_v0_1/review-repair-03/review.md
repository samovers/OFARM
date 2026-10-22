# Fresh technical review of material occupancy repair R3

**Verdict: PASS for the reviewed repair. No blocking or follow-up defect was found in this review. B1, B2 and F1 are closed by the inspected implementation and reproduced behavior.** This is a technical review of the frozen local candidate, not formal GitHub approval, a two-human review gate, runtime admission, or permission to activate CI or merge.

The reviewed trust boundary is **material occupancy source evidence**. The review is read-only with respect to the candidate and repository. Review scripts, a frozen snapshot, an isolated installed layout and reports were written only inside this domain-owner review directory. No #47 pin, #57 packet, source schema, shared worktree, Git state, public comment or outgoing chat message was changed. The implementation scope stayed inside the occupancy source-evidence boundary.

Candidate: `plans/material-occupancy-evidence-20261021/review-repair-03`.

- `DELIVERY_MANIFEST.json`: `5c0a0119085d77223060d30c92a79990d525133f338e17f2e405ed71c57e3609`.
- Raw `contract.json`: `8d0bf72d370b08601d5bd8e909609095f54ab15bb20d95d0c28beea70a188ea0`.
- All 791 sealed members verified before review. All 792 candidate files, including the manifest, and all 792 snapshot files remained byte-identical after review.
- All 790 split-lane integration mappings were installed inside this review directory and their hashes verified.
- The three schemas, four semantic source files and six foreign fixture/schema files are byte-identical to R2. The adopted domain decision is an exact copy of the domain-owner record.

## Review provenance

The reviewer is the domain-owner model agent, which authored the requested interval/quantity domain interpretation but did not implement this R3 repair. This is fresh technical review of new frozen bytes with independently written test construction and an independent interval oracle. It is not a claim of organizational independence from the domain-semantics decision or two independent human approvals. The author conformance replay and the independent review corpus are reported separately.

The tests use explicit fictional owner selections and supporting-source assumptions. Recomputed pins model independently selected inputs for a test; they do not authenticate a real source owner or prove a live inventory exhaustive. The occupancy checker deliberately preserves foreign originals without validating their foreign semantics. The foreign shape checks below do not replace those owners' admission or truth checks.

## Evidence and decisions

The author suite reproduced **296/296 passes**, including its 83 specific-code review regressions, 51 positive cases and 35 complete foreign pairs. See `author-conformance-replay.json`.

The separate `independent_probes.py` suite passed **241/241 checks**, including **12 installed CLI cases**, **35 full foreign pairs**, and their raw-byte mutation negatives. It does not import the author's fixture generator, conformance expectations or private temporal helpers. It imports the frozen public `verify` function and constructs new original-byte contexts, requests and records. See `independent-results.json`; materialized originals and API/CLI reports are under `cases/`.

B1 is closed. Independently constructed A-to-B turnover, A/B plus a full-window C, and repeated visits by the same lot all remain in the returned ordered inventory. Full original intervals are unchanged. The query intersection and source-supported portion differ correctly when a full-window original has narrower applicability. Coverage is PARTIAL_WINDOW for partial visits and FULL_WINDOW only for whole-window source support. The independent 96-case interval matrix covers intersecting, disjoint and touching windows with every boundary-inclusion combination. AS_OF endpoint inclusion, a singleton original episode and a one-nanosecond included/excluded boundary also behave correctly. A successful empty inventory remains expressly conditional on owner selection; it does not prove actual absence.

B2 is closed. Independent tests reject a future point query, future interval end, future source applicability, future known start/end, future open-as-of time and future source assessment, each just one nanosecond beyond the fixed horizon. Future known boundaries fail even when the selected query is earlier. UNKNOWN and UNBOUNDED starts/ends remain in the selected inventory with unresolved temporal support, null supported/query intersections and a false unqualified-claim indicator. Their known opposite boundaries still reject contradictions. An OPEN_AS_OF source supports its observed point but rejects the next nanosecond. The implementation contains no infinite-end sentinel in coverage evaluation.

F1 is closed. All nine quantity qualifiers were independently tested with and without an identified cohort. Only EXACT reported amounts support the amount indicator or the broad unqualified indicator when the other requirements hold. An identified cohort does not erase MAXIMUM, MINIMUM, ESTIMATED, UNKNOWN or other reported qualifications. Unreported amounts support only the explicit cohort branch, without inventing a numerical amount. Original decimal strings, labels, units, kinds and qualifiers remain identical in returned full facts.

Selection and original-source integrity also held. Independently generated missing, extra, reordered and duplicate request episodes; reordered EPISODE manifest entries; changed quantity facts; missing/extra original records; equal-value whitespace changes; binary changes; and consistently repinned missing/extra reference-closure attacks all fail with no partially accepted episode set. Digest-selected episodes also pass the correct case. These tests supplement the author's broader malformed-input and selector corpus.

All seven event families crossed with all five measurement result forms remain representable as complete supporting records. Each newly fictional JSON body was separately checked against the unchanged frozen event/measurement schema. The occupancy report retains the selected raw hashes and source mappings, and changing a measurement's original whitespace without changing the independently selected original-byte pin fails in all 35 pairs. Binary source bytes, including non-UTF-8 content, remain bound as RAW_BYTES; they were not replaced with JSON or narrowed away.

The installed CLI was invoked with separately installed checker, package and source roots for turnover, repeated visits, singleton/nanosecond boundaries, future known end, qualified amount with cohort, unresolved end, a full pending foreign measurement, binary tampering and digest selectors. Its exit codes and complete reports exactly match the public API. No candidate or snapshot file was modified by these invocations.

## #47 integration requirements and limits

This result permits using the frozen repair as a technically reviewed dependency candidate. It does not itself update or approve the #47 consumer, and it does not resolve the separate #56 review. The existing #47 R2 pin remains historical construction evidence until the coordinated dependency update is made.

The broad `selectedPostureSupportsUnqualifiedClaim` indicator now requires FULL_WINDOW temporal support. A partial-window episode can still support the distinct statement that the episode occurred during the window. #47 must choose the predicate for its actual allegation, inspect the returned coverage and source qualifications, and retain every original episode, original interval, query intersection and supported portion. It must not discard partial episodes to make an unqualified throughout-window claim pass. An inventory union does not establish continuous occupancy. Comparison success is neither source truth nor runtime authority.

The existing JSON-only state-protection versus RAW_BYTES question remains a separate consumer/state-owner interface issue. It is not repaired by weakening #57's raw support, narrowing event/measurement coverage or wrapping binary bytes in surrogate JSON. This review neither reopens nor resolves that separate boundary.

Reproduction: use the recorded local dependency environment with `PYTHONDONTWRITEBYTECODE=1`; run `independent_probes.py` in a new copy of this review directory if repeating the frozen review. `baseline.json` and `post-review-integrity.json` identify exact input and post-review hashes. The author replay command is retained in the task tool record and its result in `author-conformance-replay.json`.

Next: the coordinator combines the fresh technical review records and handles the separate publication decision; the domain lane then updates #47 consumption against the exact accepted owner candidate and tests all retained qualifications. CI activation, merge and #392/#396 remain separate or parked.
