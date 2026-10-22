# PR57 review response — occupancy repair 03

Primary trust boundary: **material occupancy source evidence**. Scope stays inside that boundary. This sibling candidate addresses the review of `ae9db62d90ac054e76bbc4fb493df9b7e151efc2`; the original candidate and both earlier repaired candidates and reviews remain sealed. The domain owner's exact decision is retained in `DOMAIN_OWNER_DECISION.md`. That decision approves the interpretation, not this implementation.

## B1 — complete interval inventory

Both INTERVAL and AS_OF remain supported. INTERVAL requires overlap, rather than requiring every episode to span the entire query. The owner may retain each episode's own supported applicability. Each source's full applicability still respects every known episode boundary, including when the opposite endpoint is unresolved. This preserves the earlier contradiction repair.

The report retains full original episode facts and separately reports the known/observed query intersection, actually supported applicability, and full/partial/unresolved window coverage. Partial-window support does not establish presence throughout the query. A known episode that spans the query but has narrower applicability also receives partial coverage. Included-point intersections remain points; excluded touching boundaries do not overlap. No union, sum, clipping of original facts or omission of selected episodes is performed.

New complete examples include A-to-B turnover, A/B turnover with whole-window C, two separated visits by the same occupant, and a qualified owner-selected empty interval inventory. Dropping partial episodes from a selected complete inventory fails with `EPISODE_SET_OR_ORDER_MISMATCH`. Completeness of the actual live inventory remains NOT_ESTABLISHED.

## B2 — fixed observational horizon

The full selection and each source applicability must end at or before independently selected `fixedAt`. Every KNOWN boundary, status assessment and open-end observation is subject to that same nanosecond-precise horizon. Future known boundaries are rejected with `KNOWN_BOUNDARY_AFTER_CONTEXT`, including when the query itself is historical. Original future-source bytes are not rewritten by the verifier. Fictional positive examples now use an observed end at the context horizon; the previous November-end examples remain preserved in the previous commit and sealed candidate.

UNKNOWN and UNBOUNDED endpoints are retained as unresolved, never as observed infinity. OPEN_AS_OF supports only the finite recorded observation range. The report labels that intersection basis `OBSERVED_OPEN_RANGE`, without treating the observation instant as a departure.

## F1 — qualified amounts

All quantity qualifiers, full decimals, unit and quantity identities, original lexical values and cohort references remain retained. A reported quantity supports an unqualified amount only with qualifier EXACT. An identified cohort cannot erase a simultaneous reported amount's qualification. Explicitly unreported quantities may support only the separately identified cohort branch, with no numerical claim.

## Evidence and limits

The opt-in conformance runner includes 51 positive examples and 83 targeted B1/B2/F1 regression checks. All 296 checks pass, including all 35 full event-family/measurement-kind combinations and original-byte mutation checks. Each new hostile regression requires its specific error code and no partially accepted episode set; each positive verifies the complete returned facts and relevant derived coverage/quantity fields. Schemas and original semantic/foreign source bytes are unchanged.

These are author checks, pending a fresh independent technical review of this exact candidate. They establish conditional offline comparison behavior, not authentic owner selection, source truth, runtime admission, live completeness, formal GitHub approval, or a two-reviewer governance gate.

No lifecycle law, identity, movement, occupancy state, authorization, current/default promotion or CI behavior changes. OFARM2 #392/#396 stay parked. CI activation and merge remain separate.

Next: freeze this candidate, obtain a fresh review of its exact bytes, then publish the repair in #57 and update the separate #47 consumer only against the reviewed contract pin.
