# Material occupancy source evidence

This draft stays inside the material occupancy source evidence boundary. Three closed schemas and an opt-in checker retain complete material/lot-to-place episodes, exact immutable selectors and original bytes, explicit temporal posture, quantity or cohort, unit, extent and source status. Repeated and overlapping episodes remain separate.

The checker compares independently selected owner evidence. It cannot authenticate that selection, prove a live inventory complete, decide source validity or change occupancy. Disputed, superseded and unresolved source facts remain visible and qualified. Supporting event and measurement bytes remain whole and owned by their existing contracts. See CONTRACT.md and PORTABLE_USAGE.md for the exact interface and trust assumptions.

Run the optional conformance checks from the repository root:

```sh
python3 -B 04_implementation_and_conformance/conformance_runners/ofarm_material_occupancy_evidence_v0_1.py
```

This separate prerequisite supports #47. Runtime behavior, current/default contracts, default validation commands and workflows are unchanged. OFARM2 #392/#396 stay parked, and #421 remains separate. CI activation and merge remain separate.

Next: independently review this draft and consume the exact reviewed source interface in #47.
