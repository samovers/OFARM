# OFARM KIS adapter spike plan v0.1

Date: 2026-05-13  
Status: active supporting implementation plan  
Change class: implementation/conformance implication  
Baseline impact: none

---

## Purpose

Build the first deterministic OFARM adapter fixture skeleton from the redacted KIS BigQuery candidate packet.

The spike must prove separation of intent, execution evidence, geometry evidence, local identity binding, and reconstruction trace. It must also prove that promotion remains blocked until external evidence gates are supplied.

## Source surface

Primary source: `prod__t_kis__*` BigQuery tables as represented in the Codex report.

Current interpretation: these are discovery/projection surfaces, not OFARM truth stores.

## Selected candidate

The selected candidate is a completed `APPLICATION` operation with:

- planned status `COMPLETED`,
- actual status `COMPLETED`,
- planned window 2026-04-20 to 2026-04-26,
- actual execution 2026-04-28 11:48:40 to 2026-04-28 12:15:01,
- actual last-modified timestamp 2026-05-07 21:47:14,
- two planned material entries,
- two actual material entries,
- one vehicle reference,
- one implement reference,
- one person reference,
- five crop-zone actual rows,
- source-side planned-operation audit entries,
- one work-order link,
- one finished work order,
- one finished task result.

No field names, farm names, person names, material names, crop names, coordinates, or WKT geometries are included.

## Candidate mapping

| Source evidence | OFARM candidate carrier | Promotion status |
|---|---|---|
| Planned operation + planned material audit rows | `InterventionIntentPayload` candidate | candidate only |
| Actual operation + task result + work-order status | `ExecutionRecordPayload` candidate | candidate only |
| Crop-zone and operation-zone area/intersection metrics | `PartialExtent` candidate | candidate only |
| Material hashes + rate/unit fields | `AgronomicIdentityBinding` candidate | local identity only |
| Source-side audit/task/work-order rows | `AgronomicReconstructionTrace` partial candidate | partial reconstruction only |

## No-go controls

The spike must not create:

- accepted execution truth,
- compliance-grade product-use consequence,
- regulatory product identity,
- authority decision,
- evidence sufficiency decision,
- direct scouting-to-treatment causal claim,
- geometry precision claim beyond the redacted metrics,
- wire-level ADAPT / ISOXML / EFDI conformance claim.

## Pass criteria

The fixture passes only when:

1. planned intent and actual execution are separate;
2. actual execution is represented as evidence/claim, not accepted consequence;
3. partial extent candidates are event-bound and do not become durable field/crop-zone truth;
4. material identity remains local and unresolved for regulatory compliance;
5. source-side audit rows support reconstruction but do not become authority;
6. promotion is explicitly blocked with named blockers;
7. P0 evidence requests remain open.

## Next implementation step

After this fixture skeleton passes, build a thin read-only adapter prototype that:

- reads a similarly redacted BigQuery packet,
- emits OFARM candidate carrier records,
- emits a source-health/loss-map report,
- refuses promotion by default,
- produces an agronomic reconstruction trace with blockers.

## Addendum adjustment — entity-guided probe expansion

The Logineko entity package addendum makes the first read-only KIS adapter spike more precise. The adapter should now include entity-guided probes for scouting relationships, work-order checkpoints, task-result/task-hub fields, material sessions, external identity, and audit timestamp/user attribution.

The selected candidate now has source-side checkpoint evidence, but no linked source-side scouting rows and no material sessions. Therefore the adapter may emit stronger `ExecutionRecordPayload` and `AgronomicReconstructionTrace` candidates, but it must still refuse accepted execution and compliance-grade promotion.
