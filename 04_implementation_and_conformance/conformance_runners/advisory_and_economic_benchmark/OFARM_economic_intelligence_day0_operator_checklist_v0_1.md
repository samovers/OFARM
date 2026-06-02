# OFARM economic intelligence day-0 operator checklist v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: minimal day-0 checklist for starting the bounded economics spike without reopening design

---

## Day-0 checklist

- [ ] Freeze the consolidated checked candidate as the only working tree.
- [ ] Archive earlier economics packages as superseded lineage.
- [ ] Confirm the three economics/scenario notes are present in `01_companion_artifacts/`.
- [ ] Confirm contracts/examples/runners remain in `04_implementation_and_conformance/` only.
- [ ] Confirm the acceptance gate outcome is still `PARTIAL_PASS` and promotion remains blocked.
- [ ] Open one backlog with exactly three lanes: Scenario 1 ranking, Scenario 2 own-vs-contract, Scenario 3 capex pre-gate.
- [ ] Attach one hostile matrix to that backlog.
- [ ] Instrument trace capture for basis refs, target twin, freshness status, output family, and bridge review state.
- [ ] Re-run the economics validators before any code changes.
- [ ] Start Lane A first. Do not start Lane C first.

## Day-0 anti-checklist

- [ ] Do **not** open a new architecture round.
- [ ] Do **not** create a new economics RFC.
- [ ] Do **not** promote economics schemas into `03_machine_contracts/`.
- [ ] Do **not** patch the Alignment Register.
- [ ] Do **not** add broad finance-entry surfaces.
- [ ] Do **not** let "economic passport" language enter the working tree.
