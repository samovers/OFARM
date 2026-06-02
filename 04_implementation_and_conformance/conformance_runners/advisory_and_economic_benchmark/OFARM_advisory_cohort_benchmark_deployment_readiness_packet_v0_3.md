# OFARM advisory cohort benchmark deployment-readiness packet v0.3

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: deployment-readiness and real-pilot handoff tranche for the advisory cohort benchmark seam

---

## 1. Purpose

This tranche follows the bounded pre-implementation packet and the runtime proof packet.

It remains entirely inside `04_implementation_and_conformance/`.
It does **not** patch:

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`
- `06_active_supporting_research/`

The purpose here is narrower than “deployment”.
It is to make the seam **ready for one redacted real pilot handoff** without making any false claim that a real tenant pilot already happened in this workspace.

---

## 2. Affected active-baseline files

None.

---

## 3. Change type

- implementation/conformance implication

---

## 4. What this tranche adds

### Operator handoff set
- `OFARM_advisory_cohort_benchmark_real_pilot_handoff_packet_v0_3.md`
- `OFARM_advisory_cohort_benchmark_real_pilot_runbook_v0_3.md`
- `OFARM_advisory_cohort_benchmark_real_pilot_data_request_sheet_v0_3.md`
- `OFARM_advisory_cohort_benchmark_real_pilot_redaction_and_sovereignty_note_v0_3.md`
- `OFARM_advisory_cohort_benchmark_real_pilot_day0_operator_checklist_v0_3.md`

### Real-pilot spike workspace
`04_implementation_and_conformance/spikes_incubation/ofarm_advisory_cohort_benchmark_real_pilot_spike_v0_3/`

Contains:
- a `REAL_REDACTED_TEMPLATE` intake dataset
- a tenant-shaped `REDACTED_REHEARSAL_NON_REAL` dataset
- operator validator and runner scripts
- generated rehearsal readiness and result outputs
- request-history long-horizon examples
- view-module examples for allow / broaden / refuse / recompute states
- experimental schemas for:
  - `BenchmarkPilotExecutionRecord`
  - `BenchmarkViewSurfaceAudit`
- positive and negative examples
- a validation runner and report

### Root-level runtime records
This packet also adds root runtime record sets for:
- pilot execution summaries
- view-surface audit summaries

---

## 5. What this tranche proves

1. The benchmark seam can be handed to an operator without reopening OFARM architecture.
2. A redacted real-pilot intake shape now exists and is mechanically checkable.
3. The operator path requests only bounded evidence-backed receipt/extract inputs rather than raw accounting or raw document payloads.
4. The validator rejects obvious posture violations such as wrong dataset honesty markers or missing benchmark boundaries.
5. The runner can generate bounded benchmark cards from a tenant-shaped rehearsal dataset while preserving no-raw-row / no-raw-evidence / no-exact-count behavior.
6. Promotion remains explicitly blocked.

---

## 6. What this tranche does not prove

- an actual real tenant pilot inside this workspace
- deployment telemetry or live service hardening
- multi-viewer collusion closure at production scale
- permission to promote into `01`, `02`, or `03`
- any reason to change OFARM law

The strongest honest claim after this packet is:

**READY_FOR_REAL_PILOT_HANDOFF**

Not:
- deployment complete
- production safe
- law-ready
- RFC-ready
- machine-contract ready

---

## 7. Why this is the smallest controlled patch

The runtime packet already closed the main representational gaps:
- request-history differencing
- revocation invalidation
- forced recompute

The next missing seam was operational, not architectural:
- how to intake one redacted tenant cohort
- how to validate it
- how to run it without broadening semantics
- how to stop the operator from drifting into raw spend disclosure or finance-system scope

This packet solves exactly that and nothing larger.

---

## 8. Bottom line

The benchmark seam is now past “pre-implementation only”.

It is now:
- executable in rehearsal
- bounded in operator handoff shape
- ready for one redacted real pilot

It is still **not** promoted OFARM law and still **not** a production deployment claim.
