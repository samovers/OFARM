# Canonical authorization evidence repair delivery

This packet addresses F1–F5 and P1/P2 from the current-head review of PR #56. The primary trust/PR boundary remains **canonical authorization decision evidence integrity**; scope stayed inside it. The original owner packet and author-side independent review are unchanged, as verified in `preserved-originals.json`.

The repair binds native source revisions, rejects conflicting versions of one logical source identity, checks every retained tuple and the selected path's ordering against retained PATH_ALLOW claims, loads the actual adjacent helper bytes, retains the missing PR11 output fields and exact extractor bytes, and selects the intent's native schema-version field through its profile. Selected sharing paths get an explicit out-of-profile error; retained sharing paths remain checked. `REPAIR_DESIGN.md` explains each source-backed decision and limitation.

Validation completed:

- 332 full conformance cases, 138 targeted specific-code cases and 31 edge/installation checks passed.
- Seven fresh-process helper-origin/identity probes and two API-only invalid-map checks passed.
- All 491 portable cases have matching actual split installed CLI executions, with exact error-code and applicable detail expectations: 490 from the initial full run and the oversized-wire case from a targeted replay after correcting its CLI-specific error expectation. Runtime and wire bytes did not change. Initial results and correction evidence are preserved. Two deliberately incorrect runner oracles were correctly rejected.
- The 493-case mutation baseline reaches all 115 must() sites. There are direct negative witnesses for 112: removing 84 accepts an invalid input; removing 28 changes the required error. The remaining three failure branches repeat earlier trace guards. They are explicitly classified rather than counted as kills.

These are author-side checks, not a formal two-reviewer gate. They establish conditional evidence integrity only. Eligibility, principal trust, candidate completeness, globally correct canonical selection, live owner origin, CP3 admission, runtime protection and effect permission remain unestablished. No extractor is executed. No runtime, foreign source law, CI activation, merge or publication was performed. Selected SharingGrant support and a real complete producer profile remain outside this narrow draft. Python 3.14.5 was tested; Python 3.11 was not.

The integration map keeps runtime code, package contracts, fixtures and verbatim semantic sources in separate existing lanes. New repair history uses a new history directory so the original delivery seal is preserved. `cases.json` is the portable exact-code index. API-only, helper-origin and mutation evidence are separately labelled. Temporary split installation copies were removed after verification; rebuild only in a separate review/install directory using the map.

Next: the coordinator performs a fresh review of these exact sealed bytes, integrates only the reviewed repair into #56 with [skip ci], and leaves consumer integration and all other trust boundaries separate.
