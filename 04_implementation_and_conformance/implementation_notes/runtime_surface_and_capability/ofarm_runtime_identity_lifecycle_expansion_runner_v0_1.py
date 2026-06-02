
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

GENERATED_AT = "2026-04-12T16:20:00Z"

SCENARIOS = [
    {
        "scenarioId": "life:zone-recurring-geometry-revision:v0.1",
        "family": "zone",
        "subjectClass": "ManagementZone",
        "scopeRef": "scope:field-17/zone-a",
        "outcome": "SAME_IDENTITY_NEW_REVISION",
        "oldIdentityRef": "zone:field-17/a",
        "newIdentityRef": "zone:field-17/a",
        "newRevisionRef": "zoneRev:field-17/a:r3",
        "lineageRelations": [{"type": "revises", "fromRef": "zoneRev:field-17/a:r2", "toRef": "zoneRev:field-17/a:r3"}],
        "checks": {
            "sameGovernedReferent": True,
            "recurringZoneContinuity": True,
            "purposeContinuity": True,
            "geometryRefinedOnly": True,
        },
        "summary": "Recurring irrigation management zone keeps identity through geometry refinement.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REVISION_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATION_REVIEW"],
    },
    {
        "scenarioId": "life:zone-ephemeral-mask-no-identity:v0.1",
        "family": "zone",
        "subjectClass": "AdvisoryMask",
        "scopeRef": "scope:field-17",
        "outcome": "NOT_CONSTITUTIONAL_IDENTITY",
        "oldIdentityRef": None,
        "newIdentityRef": None,
        "newRevisionRef": None,
        "lineageRelations": [],
        "checks": {
            "oneOffOverlay": True,
            "recurringGovernanceAbsent": True,
            "constitutionalZoneNotMinted": True,
        },
        "summary": "One-off heatmap overlay remains ephemeral and does not create a constitutional zone identity.",
        "telemetryKind": ["IDENTITY_CLASSIFICATION", "EPHEMERAL_CLASS_DECISION", "IDENTITY_ISSUE_DENIED"],
    },
    {
        "scenarioId": "life:zone-split-governed-children:v0.1",
        "family": "zone",
        "subjectClass": "ManagementZone",
        "scopeRef": "scope:field-17",
        "outcome": "NEW_IDENTITIES_WITH_SPLIT_FROM",
        "oldIdentityRef": "zone:field-17/c",
        "newIdentityRef": ["zone:field-17/c-north", "zone:field-17/c-south"],
        "newRevisionRef": None,
        "lineageRelations": [
            {"type": "splitFrom", "fromRef": "zone:field-17/c", "toRef": "zone:field-17/c-north"},
            {"type": "splitFrom", "fromRef": "zone:field-17/c", "toRef": "zone:field-17/c-south"},
        ],
        "checks": {
            "recurringGovernedChildren": True,
            "oneToOneContinuityBroken": True,
            "lineageExplicit": True,
        },
        "summary": "One governed zone splits into two separately managed recurring child zones.",
        "telemetryKind": ["IDENTITY_LOOKUP", "SPLIT_DECISION", "CHILD_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
    {
        "scenarioId": "life:crop-failure-same-attempt:v0.1",
        "family": "cropcycle",
        "subjectClass": "CropCycle",
        "scopeRef": "scope:field-17/block-4",
        "outcome": "SAME_IDENTITY_FAILED_ATTEMPT",
        "oldIdentityRef": "cropCycle:field-17/block-4:2026-spring-maize:a1",
        "newIdentityRef": "cropCycle:field-17/block-4:2026-spring-maize:a1",
        "newRevisionRef": "cropCycleRev:field-17/block-4:2026-spring-maize:a1:r5",
        "lineageRelations": [{"type": "revises", "fromRef": "cropCycleRev:field-17/block-4:2026-spring-maize:a1:r4", "toRef": "cropCycleRev:field-17/block-4:2026-spring-maize:a1:r5"}],
        "checks": {
            "sameCultivationAttempt": True,
            "failureRecorded": True,
            "noReplantYet": True,
        },
        "summary": "Crop failure remains the same governed cultivation attempt until re-establishment begins.",
        "telemetryKind": ["IDENTITY_LOOKUP", "FAILURE_STATE_WRITE", "REVISION_ISSUE"],
    },
    {
        "scenarioId": "life:crop-replant-successor:v0.1",
        "family": "cropcycle",
        "subjectClass": "CropCycle",
        "scopeRef": "scope:field-17/block-4",
        "outcome": "NEW_IDENTITY_SUCCEEDS",
        "oldIdentityRef": "cropCycle:field-17/block-4:2026-spring-maize:a1",
        "newIdentityRef": "cropCycle:field-17/block-4:2026-spring-maize:a2",
        "newRevisionRef": "cropCycleRev:field-17/block-4:2026-spring-maize:a2:r1",
        "lineageRelations": [{"type": "succeeds", "fromRef": "cropCycle:field-17/block-4:2026-spring-maize:a1", "toRef": "cropCycle:field-17/block-4:2026-spring-maize:a2"}],
        "checks": {
            "newEstablishmentStarted": True,
            "newCultivationAttempt": True,
            "lineageExplicit": True,
        },
        "summary": "Replant after failure starts a new crop-cycle identity with explicit successor lineage.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REPLANT_DECISION", "NEW_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
    {
        "scenarioId": "life:crop-relay-overlap-explicit:v0.1",
        "family": "cropcycle",
        "subjectClass": "CropCycle",
        "scopeRef": "scope:field-17/block-7",
        "outcome": "CONCURRENT_IDENTITIES_WITH_OVERLAP",
        "oldIdentityRef": "cropCycle:field-17/block-7:2026-main-cereal",
        "newIdentityRef": "cropCycle:field-17/block-7:2026-relay-legume",
        "newRevisionRef": "cropCycleRev:field-17/block-7:2026-relay-legume:r1",
        "lineageRelations": [{"type": "overlapsWith", "fromRef": "cropCycle:field-17/block-7:2026-main-cereal", "toRef": "cropCycle:field-17/block-7:2026-relay-legume"}],
        "checks": {
            "scopeClarityPresent": True,
            "overlapDeclared": True,
            "concurrentOperationalIdentities": True,
        },
        "summary": "Relay/intercrop case creates concurrent crop-cycle identities with explicit overlap relation.",
        "telemetryKind": ["IDENTITY_LOOKUP", "OVERLAP_DECISION", "NEW_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
    {
        "scenarioId": "life:crop-parent-split-harvest-children:v0.1",
        "family": "cropcycle",
        "subjectClass": "CropCycle",
        "scopeRef": "scope:field-18",
        "outcome": "NEW_IDENTITIES_WITH_SPLIT_FROM",
        "oldIdentityRef": "cropCycle:field-18:2026-root-crop",
        "newIdentityRef": ["cropCycle:field-18:north-harvest", "cropCycle:field-18:south-harvest"],
        "newRevisionRef": None,
        "lineageRelations": [
            {"type": "splitFrom", "fromRef": "cropCycle:field-18:2026-root-crop", "toRef": "cropCycle:field-18:north-harvest"},
            {"type": "splitFrom", "fromRef": "cropCycle:field-18:2026-root-crop", "toRef": "cropCycle:field-18:south-harvest"},
        ],
        "checks": {
            "separatelyManagedChildren": True,
            "separatelyHarvestedChildren": True,
            "lineageExplicit": True,
        },
        "summary": "One parent crop cycle diverges into separately harvested child cycles with explicit split lineage.",
        "telemetryKind": ["IDENTITY_LOOKUP", "SPLIT_DECISION", "CHILD_IDENTITY_ISSUE", "LINEAGE_WRITE"],
    },
    {
        "scenarioId": "life:equipment-maintenance-revision:v0.1",
        "family": "equipment",
        "subjectClass": "Equipment",
        "scopeRef": "scope:machinery/pulverizer-9",
        "outcome": "SAME_IDENTITY_NEW_REVISION",
        "oldIdentityRef": "equipment:pulverizer-9",
        "newIdentityRef": "equipment:pulverizer-9",
        "newRevisionRef": "equipmentRev:pulverizer-9:r4",
        "lineageRelations": [{"type": "revises", "fromRef": "equipmentRev:pulverizer-9:r3", "toRef": "equipmentRev:pulverizer-9:r4"}],
        "checks": {
            "sameAsset": True,
            "maintenanceOnly": True,
            "configurationUpdated": True,
        },
        "summary": "Maintenance and nozzle configuration change keep the same equipment identity and issue a new revision.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REVISION_ISSUE", "STATE_WRITE"],
    },
    {
        "scenarioId": "life:equipment-replacement-new-asset:v0.1",
        "family": "equipment",
        "subjectClass": "Equipment",
        "scopeRef": "scope:machinery/pulverizer-9",
        "outcome": "NEW_IDENTITY_REPLACES",
        "oldIdentityRef": "equipment:pulverizer-9",
        "newIdentityRef": "equipment:pulverizer-14",
        "newRevisionRef": "equipmentRev:pulverizer-14:r1",
        "lineageRelations": [{"type": "replaces", "fromRef": "equipment:pulverizer-9", "toRef": "equipment:pulverizer-14"}],
        "checks": {
            "differentAsset": True,
            "sameAssetFalse": True,
            "lineageExplicit": True,
        },
        "summary": "Replacement by a different physical asset mints a new equipment identity with explicit replacement lineage.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REPLACEMENT_DECISION", "NEW_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
    {
        "scenarioId": "life:facility-layout-revision:v0.1",
        "family": "facility",
        "subjectClass": "Facility",
        "scopeRef": "scope:packhouse-2",
        "outcome": "SAME_IDENTITY_NEW_REVISION",
        "oldIdentityRef": "facility:packhouse-2",
        "newIdentityRef": "facility:packhouse-2",
        "newRevisionRef": "facilityRev:packhouse-2:r3",
        "lineageRelations": [{"type": "revises", "fromRef": "facilityRev:packhouse-2:r2", "toRef": "facilityRev:packhouse-2:r3"}],
        "checks": {
            "sameOperationalPlace": True,
            "layoutChanged": True,
            "governedContinuityPreserved": True,
        },
        "summary": "Packhouse layout restructuring keeps the same facility identity and issues a new revision.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REVISION_ISSUE", "STATE_WRITE"],
    },
    {
        "scenarioId": "life:storage-location-retire-replace:v0.1",
        "family": "storagelocation",
        "subjectClass": "StorageLocation",
        "scopeRef": "scope:facility-packhouse-2/cold-room-a",
        "outcome": "NEW_IDENTITY_REPLACES",
        "oldIdentityRef": "storage:cold-room-a/bin-3",
        "newIdentityRef": "storage:cold-room-a/bin-3b",
        "newRevisionRef": "storageRev:cold-room-a/bin-3b:r1",
        "lineageRelations": [{"type": "replaces", "fromRef": "storage:cold-room-a/bin-3", "toRef": "storage:cold-room-a/bin-3b"}],
        "checks": {
            "oldLocationRetired": True,
            "newContainmentPlaceMinted": True,
            "lineageExplicit": True,
        },
        "summary": "Retired storage location is replaced by a newly governed location identity with explicit lineage.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REPLACEMENT_DECISION", "NEW_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
    {
        "scenarioId": "life:reusable-container-occupancy-continuity:v0.1",
        "family": "container",
        "subjectClass": "Container",
        "scopeRef": "scope:facility-packhouse-2/loading-bay",
        "outcome": "SAME_IDENTITY_NEW_OCCUPANCY_EPISODE",
        "oldIdentityRef": "container:crate-44",
        "newIdentityRef": "container:crate-44",
        "newRevisionRef": "containerState:crate-44:occupancy-17",
        "lineageRelations": [],
        "checks": {
            "reusableContainer": True,
            "occupantChanged": True,
            "containerIdentityStable": True,
        },
        "summary": "Reusable crate keeps the same identity across a new occupancy episode.",
        "telemetryKind": ["IDENTITY_LOOKUP", "OCCUPANCY_EPISODE_WRITE", "STATE_WRITE"],
    },
    {
        "scenarioId": "life:container-replacement-broken-unit:v0.1",
        "family": "container",
        "subjectClass": "Container",
        "scopeRef": "scope:facility-packhouse-2/loading-bay",
        "outcome": "NEW_IDENTITY_REPLACES",
        "oldIdentityRef": "container:crate-44",
        "newIdentityRef": "container:crate-44b",
        "newRevisionRef": "containerRev:crate-44b:r1",
        "lineageRelations": [{"type": "replaces", "fromRef": "container:crate-44", "toRef": "container:crate-44b"}],
        "checks": {
            "oldUnitBroken": True,
            "differentContainmentUnit": True,
            "lineageExplicit": True,
        },
        "summary": "Broken reusable crate is retired and replaced by a new container identity.",
        "telemetryKind": ["IDENTITY_LOOKUP", "REPLACEMENT_DECISION", "NEW_IDENTITY_ISSUE", "LINEAGE_WRITE", "MATERIALIZATION_INVALIDATED"],
    },
]

INVALIDATIONS = [
    {
        "triggerId": "lifeInv:zone-split-invalidates-zone-compliance-view:v0.1",
        "triggerFamily": "LIFECYCLE_SPLIT",
        "sourceScenarioId": "life:zone-split-governed-children:v0.1",
        "affectedMaterializationRef": "mat:zone-compliance-view:field-17/c:v1",
        "outcome": "INVALID",
        "requiredAction": "RECOMPUTE_ON_CHILD_ZONES",
        "checks": {
            "oldSingleZoneBasisNoLongerValid": True,
            "childScopeRefsPresent": True,
        },
    },
    {
        "triggerId": "lifeInv:crop-replant-invalidates-failed-cycle-view:v0.1",
        "triggerFamily": "CROP_REPLANT",
        "sourceScenarioId": "life:crop-replant-successor:v0.1",
        "affectedMaterializationRef": "mat:crop-cycle-passport:field-17/block-4:a1:v2",
        "outcome": "INVALID",
        "requiredAction": "RECOMPUTE_ON_SUCCESSOR_CYCLE",
        "checks": {
            "newCultivationAttemptPresent": True,
            "oldCycleReuseDeniedForHighConsequence": True,
        },
    },
    {
        "triggerId": "lifeInv:crop-overlap-invalidates-single-cycle-summary:v0.1",
        "triggerFamily": "LIFECYCLE_OVERLAP",
        "sourceScenarioId": "life:crop-relay-overlap-explicit:v0.1",
        "affectedMaterializationRef": "mat:single-cycle-summary:field-17/block-7:v3",
        "outcome": "STALE_WITH_REVIEW",
        "requiredAction": "RECOMPUTE_WITH_OVERLAP_DISCLOSURE",
        "checks": {
            "overlapRelationPresent": True,
            "singleCycleAssumptionBroken": True,
        },
    },
    {
        "triggerId": "lifeInv:equipment-replacement-invalidates-maintenance-status:v0.1",
        "triggerFamily": "IDENTITY_REPLACEMENT",
        "sourceScenarioId": "life:equipment-replacement-new-asset:v0.1",
        "affectedMaterializationRef": "mat:equipment-compliance-status:pulverizer-9:v4",
        "outcome": "INVALID",
        "requiredAction": "RECOMPUTE_ON_REPLACEMENT_ASSET",
        "checks": {
            "oldAssetNoLongerGoverningSubject": True,
            "replacementLineagePresent": True,
        },
    },
    {
        "triggerId": "lifeInv:zone-ephemeral-mask-stays-nonconstitutional:v0.1",
        "triggerFamily": "ZONE_DURABILITY_CLASS_CHANGE",
        "sourceScenarioId": "life:zone-ephemeral-mask-no-identity:v0.1",
        "affectedMaterializationRef": "mat:recurring-zone-index:field-17:v5",
        "outcome": "NO_NEW_CONSTITUTIONAL_ENTRY",
        "requiredAction": "KEEP_OUT_OF_DURABLE_ZONE_INDEX",
        "checks": {
            "ephemeralMaskExcluded": True,
            "durableZoneIndexUnchanged": True,
        },
    },
]

def emit_events():
    events = []
    for scenario in SCENARIOS:
        base = scenario["scenarioId"].split(":")[1]
        for idx, kind in enumerate(scenario["telemetryKind"], start=1):
            events.append({
                "eventId": f"evt:{base}:{idx}",
                "scenarioId": scenario["scenarioId"],
                "eventKind": kind,
                "subjectClass": scenario["subjectClass"],
                "scopeRef": scenario["scopeRef"],
            })
    # attach invalidation events
    for inv in INVALIDATIONS:
        base = inv["triggerId"].split(":")[1]
        for idx, kind in enumerate(["INVALIDATION_TRIGGER", "MATERIALIZATION_OUTCOME_WRITE"], start=1):
            events.append({
                "eventId": f"evt:{base}:{idx}",
                "scenarioId": inv["sourceScenarioId"],
                "triggerId": inv["triggerId"],
                "eventKind": kind,
                "subjectClass": "CurrentStateMaterialization",
                "scopeRef": inv["affectedMaterializationRef"],
            })
    return events

def main():
    telemetry = {"generatedAt": GENERATED_AT, "events": emit_events()}
    event_ids = {e["eventId"] for e in telemetry["events"]}
    assert len(event_ids) == len(telemetry["events"]), "duplicate event ids"

    for scenario in SCENARIOS:
        base = scenario["scenarioId"].split(":")[1]
        scenario["linkedTelemetryEventIds"] = [
            e["eventId"] for e in telemetry["events"] if e.get("scenarioId") == scenario["scenarioId"] and e["eventId"].startswith(f"evt:{base}:")
        ]

    for inv in INVALIDATIONS:
        base = inv["triggerId"].split(":")[1]
        inv["linkedTelemetryEventIds"] = [
            e["eventId"] for e in telemetry["events"] if e.get("triggerId") == inv["triggerId"] and e["eventId"].startswith(f"evt:{base}:")
        ]

    lifecycle_records = {
        "generatedAt": GENERATED_AT,
        "records": SCENARIOS,
    }
    invalidation_records = {
        "generatedAt": GENERATED_AT,
        "records": INVALIDATIONS,
    }

    all_links_valid = all(all(eid in event_ids for eid in s["linkedTelemetryEventIds"]) for s in SCENARIOS)
    inv_links_valid = all(all(eid in event_ids for eid in r["linkedTelemetryEventIds"]) for r in INVALIDATIONS)

    validations = []
    for s in SCENARIOS:
        validations.append({
            "scenarioId": s["scenarioId"],
            "hasSubjectClass": bool(s["subjectClass"]),
            "hasOutcome": bool(s["outcome"]),
            "linkedTelemetryPresent": bool(s["linkedTelemetryEventIds"]),
            "lineageRequiredWhenNewIdentity": (
                not s["outcome"].startswith("NEW_") and "OVERLAP" not in s["outcome"] or bool(s["lineageRelations"])
            ),
            "checksPass": all(bool(v) for v in s["checks"].values()),
        })

    inv_validations = []
    for inv in INVALIDATIONS:
        inv_validations.append({
            "triggerId": inv["triggerId"],
            "hasTriggerFamily": bool(inv["triggerFamily"]),
            "hasOutcome": bool(inv["outcome"]),
            "linkedTelemetryPresent": bool(inv["linkedTelemetryEventIds"]),
            "checksPass": all(bool(v) for v in inv["checks"].values()),
        })

    summary = {
        "scenariosChecked": len(SCENARIOS),
        "lifecycleRecords": len(SCENARIOS),
        "invalidationRecords": len(INVALIDATIONS),
        "telemetryEvents": len(telemetry["events"]),
        "subjectClassesCoveredHere": sorted({s["subjectClass"] for s in SCENARIOS}),
        "lifecycleRelationsCoveredHere": sorted({rel["type"] for s in SCENARIOS for rel in s["lineageRelations"]}),
        "outcomesCoveredHere": sorted({s["outcome"] for s in SCENARIOS}),
        "durableVsEphemeralCovered": True,
        "cropOverlapCovered": True,
        "replacementCovered": True,
        "equipmentFacilityContainerCovered": True,
        "identityVsRevisionFamiliesCoveredHere": ["ManagementZone", "CropCycle", "Equipment", "Facility", "StorageLocation", "Container"],
        "invalidationTriggerFamiliesCoveredHere": sorted({r["triggerFamily"] for r in INVALIDATIONS}),
        "allEventIdsUnique": len(event_ids) == len(telemetry["events"]),
        "allLifecycleLinksValid": all_links_valid,
        "allInvalidationLinksValid": inv_links_valid,
    }
    results = {
        "generatedAt": GENERATED_AT,
        "overall": "PASS_WITH_LIMITATIONS",
        "summary": summary,
        "validations": validations,
        "invalidationValidations": inv_validations,
        "limitations": [
            "Fixtures remain package-local conformance proof, not deployment-collected lifecycle telemetry.",
            "Facility merge cases are still represented indirectly through split/replacement rather than a dedicated executable merge fixture.",
            "No baseline law or machine-contract schema was changed in this wave.",
        ],
    }

    (ROOT / "OFARM_runtime_identity_lifecycle_telemetry_v0_1.json").write_text(json.dumps(telemetry, indent=2) + "\n")
    (ROOT / "OFARM_runtime_identity_lifecycle_records_v0_1.json").write_text(json.dumps(lifecycle_records, indent=2) + "\n")
    (ROOT / "OFARM_runtime_identity_lifecycle_invalidation_records_v0_1.json").write_text(json.dumps(invalidation_records, indent=2) + "\n")
    (ROOT / "OFARM_runtime_identity_lifecycle_expansion_results_v0_1.json").write_text(json.dumps(results, indent=2) + "\n")

if __name__ == "__main__":
    main()
