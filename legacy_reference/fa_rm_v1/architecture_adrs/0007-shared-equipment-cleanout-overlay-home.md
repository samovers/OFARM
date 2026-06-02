# ADR 0007: Shared-equipment cleanout overlay stays advisor-owned and reuses existing cleanout and draft authority

## Status

Accepted

## Context

The Farm Compiler handover leaves `FC-AS-05` explicitly overlay-dependent. It describes a same-day mixed-equipment scenario where:

- at least two crop contexts compete around one shared cleanout boundary
- sequencing matters before work starts
- operator, inspector, and buyer consequences should become visible together

The repository already proves several adjacent pieces:

- advisor recommendation authority under `/v1/advisor/*`
- existing advisor proof, mitigation, and compliance structures
- executed cleanout event capture under `/v1/assets/equipment-cleanout-events`
- mutable saveable pre-commit work through `OperationDraft`
- reporting and inspector-note cleanout parity for the already-proven SI corridor

What the repo does not yet prove is a cross-crop, pre-execution sequencing layer that turns shared-equipment and shared-cleanout risk into a truthful advisor-owned recommendation before the day starts.

Without an explicit decision, future FC-AS-05 work could drift into:

- a second planning contract family
- a new cleanout-task transport model beside the existing cleanout execution surface
- crop packs absorbing cross-crop equipment logic they should not own

## Decision

Adopt the following rules for FC-AS-05 and any future shared-equipment cleanout overlay work:

1. The canonical recommendation home remains the advisor family.
   - use `/v1/advisor/*`
   - use existing advisor bundle, option, proof, mitigation, and compliance structures first
2. The canonical execution-record home for actual cleanout events remains `/v1/assets/equipment-cleanout-events`.
   - do not invent a sibling cleanout execution endpoint
   - do not let advisor recommendations pretend they already executed cleanout work
3. If a mutable pre-execution bridge is later needed, reuse `OperationDraft` and existing planned-operation authority first.
   - do not create top-level `Planning*` or cleanout-specific mutable transport families unless `OperationDraft` is proven insufficient by a concrete gap audit
4. The canonical overlay concept name is `SharedEquipmentCleanoutOverlay`.
   - accepted aliases: `FC-AS-05 overlay`, `shared-cleanout overlay`, `mixed-equipment overlay`
   - handover names such as `kp.overlay.mixed_veg.postharvest` remain migration aliases only, not canonical repo names
5. Buyer-facing, inspector-facing, or reporting-facing consequences remain projections or later overlays unless the current advisor plus runtime surfaces are proven insufficient.

## Consequences

Positive:

- FC-AS-05 work now has one canonical recommendation home and one canonical cleanout execution home
- the repo can reuse already-proven cleanout runtime and draft authority instead of creating a second transport family
- crop packs stay narrow and avoid absorbing cross-crop sequencing logic
- future overlay implementation can proceed in phases: advisor-only first, `OperationDraft` bridge only if needed

Costs:

- the handover's raw overlay identifiers and framing cannot become canonical repo symbols unchanged
- FC-AS-05 remains deferred until the cross-crop sequencing layer is actually authored
- future implementation must do an explicit gap audit before proposing any runtime transport delta
