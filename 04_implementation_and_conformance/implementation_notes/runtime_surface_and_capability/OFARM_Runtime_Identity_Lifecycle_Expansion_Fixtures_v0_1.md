# OFARM Runtime Identity/Lifecycle Expansion Fixtures v0.1

Date: 2026-04-12  
Status: implementation/conformance hardening  
Scope: bounded executable expansion for central identity/lifecycle seams that remained partial or uncovered after Wave 17

## Goal

Extend runtime-shaped conformance proof for the identity/lifecycle families that were still materially thin in the coverage matrix:
- replacement
- overlap
- durable-versus-ephemeral zone treatment
- equipment / facility / storage / container lifecycle

This wave stays inside `04_implementation_and_conformance/`.
It does not amend baseline law, accepted RFCs, companion policy, or machine-contract substance.

## Source grounding

These fixtures are grounded in the already accepted/active identity law:
- Constitution §7.1–§7.5 identity/revision/new-identity/lifecycle lineage
- Constitution §7.20 zone lifecycle rule
- Constitution §7.21 crop-cycle lifecycle rule
- Constitution §7.23 equipment/facility/storage/container lifecycle rule
- Identity and Lifecycle RFC §4–§7

## Fixture families

### Zones
- recurring governed zone geometry refinement keeps the same identity and creates a new revision
- one-off advisory heatmap/mask remains ephemeral and does not mint a constitutional zone identity
- governed zone split creates child identities with explicit `splitFrom` lineage

### Crop cycles
- failed crop cycle remains the same cultivation attempt until replant
- replant starts a new crop-cycle identity with explicit successor/replacement lineage
- relay/intercrop overlap creates concurrent identities with explicit `overlapsWith`
- separately harvested child cycles create split lineage from a parent attempt

### Equipment / facility / storage / container
- equipment maintenance/reconfiguration keeps the same asset identity and creates a new revision
- equipment replacement mints a new identity with explicit `replaces` lineage
- facility layout restructure keeps the same facility identity and creates a new revision
- storage-location restructuring can retire a prior location and mint a new identity with explicit lineage
- reusable container occupancy changes do not create a new container identity
- broken container replacement creates a new container identity with explicit `replaces` lineage

## Invalidation cross-link

A bounded supplemental check links identity/lifecycle changes back into current-state invalidation pressure.
The added trigger families are:
- `ZONE_DURABILITY_CLASS_CHANGE`
- `CROP_REPLANT`
- `LIFECYCLE_OVERLAP`
- `IDENTITY_REPLACEMENT`
- `LIFECYCLE_SPLIT`

## Expected outcomes

This wave is intended to:
- close replacement and overlap gaps that were still open after lot and crop starter coverage
- close durable-zone versus ephemeral-overlay ambiguity
- materially advance equipment/facility/container lifecycle proof
- sharpen the invalidation row by adding identity/lifecycle-trigger evidence
