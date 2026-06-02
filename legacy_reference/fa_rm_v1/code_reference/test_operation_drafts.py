from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import os
import time
from typing import Any

from fastapi.testclient import TestClient

from app.main import app

DEFAULT_FARM_URI = "https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001"
DEFAULT_FIELD_URI = "urn:field:test-1"
DEFAULT_CROP_INSTANCE_URI = "urn:crop-instance:test-1"
os.environ.setdefault("FARM_RM_JWT_HS256_SECRET", "test-secret")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _encode_hs256_jwt(claims: dict, *, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(claims, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}"
    signature = hmac.new(secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
    signature_segment = _b64url_encode(signature)
    return f"{signing_input}.{signature_segment}"


def _auth_headers(*, farm_uri: str = DEFAULT_FARM_URI, roles: list[str] | None = None) -> dict[str, str]:
    now = int(time.time())
    claims = {
        "sub": "test-user",
        "iat": now,
        "exp": now + 3600,
        "farmUri": farm_uri,
    }
    if roles:
        claims["roles"] = roles
    token = _encode_hs256_jwt(
        claims,
        secret=os.environ["FARM_RM_JWT_HS256_SECRET"],
    )
    return {"Authorization": f"Bearer {token}", "X-Farm-URI": farm_uri}


client = TestClient(app, headers=_auth_headers())


def _enable_operation_features(monkeypatch) -> None:
    import app.main as main_module

    monkeypatch.setattr(type(main_module.PERSISTENCE), "enabled", property(lambda self: True))
    monkeypatch.setattr(type(main_module.PERSISTENCE), "reason", property(lambda self: "enabled"))
    monkeypatch.setenv("OPERATION_PROPOSALS_ENABLED", "1")
    monkeypatch.setenv("OPERATION_DRAFTS_ENABLED", "1")
    monkeypatch.setenv("OPERATION_ASSESSMENTS_ENABLED", "1")


def _install_operation_runtime(monkeypatch) -> dict[str, Any]:
    import app.main as main_module

    state: dict[str, Any] = {
        "proposals": {},
        "drafts": {},
        "assessments": [],
        "actions": [],
        "executed_operations": {},
        "report_binding_snapshots": [],
    }

    def _deepcopy(value: Any) -> Any:
        return copy.deepcopy(value)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_fields",
        lambda field_uris: [{"uri": DEFAULT_FIELD_URI, "farmUri": DEFAULT_FARM_URI, "label": "Rona"}]
        if DEFAULT_FIELD_URI in field_uris
        else [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_instances",
        lambda crop_instance_uris: [
            {
                "uri": DEFAULT_CROP_INSTANCE_URI,
                "fieldUri": DEFAULT_FIELD_URI,
                "farmUri": DEFAULT_FARM_URI,
                "seasonCode": "2026",
                "cropTypeUri": "urn:crop:wheat",
                "productionStatus": "organic_certified",
                "certificationScopeUri": "urn:cert-scope:1",
                "cropVocabularyUri": "urn:ref:crop",
            }
        ]
        if DEFAULT_CROP_INSTANCE_URI in crop_instance_uris
        else [],
    )

    def _persist_operation_proposals(payloads: list[dict[str, Any]]) -> dict[str, Any]:
        for payload in payloads:
            state["proposals"][payload["proposalUri"]] = _deepcopy(payload)
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOperationProposals": len(payloads),
            "persistedEvents": len(payloads),
        }

    def _fetch_operation_proposal(proposal_uri: str) -> dict[str, Any] | None:
        item = state["proposals"].get(proposal_uri)
        return _deepcopy(item) if item else None

    def _link_operation_proposal_to_draft(*, proposal_uri: str, operation_draft_uri: str) -> dict[str, Any]:
        item = state["proposals"].get(proposal_uri)
        if item is None:
            return {
                "enabled": True,
                "reason": "enabled",
                "updatedOperationProposals": 0,
                "persistedEvents": 0,
            }
        item["acceptedOperationDraftUri"] = operation_draft_uri
        return {
            "enabled": True,
            "reason": "enabled",
            "updatedOperationProposals": 1,
            "persistedEvents": 1,
        }

    def _persist_operation_draft(payload: dict[str, Any]) -> dict[str, Any]:
        state["drafts"][payload["operationDraftUri"]] = _deepcopy(payload)
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOperationDrafts": 1,
            "persistedEvents": 1,
        }

    def _update_operation_draft(payload: dict[str, Any]) -> dict[str, Any]:
        state["drafts"][payload["operationDraftUri"]] = _deepcopy(payload)
        return {
            "enabled": True,
            "reason": "enabled",
            "updatedOperationDrafts": 1,
            "persistedEvents": 1,
        }

    def _persist_operation_draft_commit(payload: dict[str, Any]) -> dict[str, Any]:
        state["drafts"][payload["operationDraftUri"]] = _deepcopy(payload)
        return {
            "enabled": True,
            "reason": "enabled",
            "updatedOperationDrafts": 1,
            "persistedEvents": 1,
        }

    def _list_operation_drafts(
        *,
        farm_uri: str,
        operation_family_code: str | None = None,
        profile_key: str | None = None,
        state_filter: str | None = None,
        operation_draft_uri: str | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        state_filter = state_filter or kwargs.get("state")
        items = []
        for item in state["drafts"].values():
            if item["farmUri"] != farm_uri:
                continue
            if operation_family_code and item["operationFamilyCode"] != operation_family_code:
                continue
            if profile_key and item["profileKey"] != profile_key:
                continue
            if state_filter and item["state"] != state_filter:
                continue
            if operation_draft_uri and item["operationDraftUri"] != operation_draft_uri:
                continue
            items.append(_deepcopy(item))
        items.sort(key=lambda item: (item.get("updatedAt") or "", item["operationDraftUri"]), reverse=True)
        return items

    def _fetch_operation_draft(operation_draft_uri: str) -> dict[str, Any] | None:
        item = state["drafts"].get(operation_draft_uri)
        return _deepcopy(item) if item else None

    def _fetch_operation_draft_for_executed_operation(executed_operation_uri: str) -> dict[str, Any] | None:
        for item in state["drafts"].values():
            if item.get("committedExecutedOperationUri") == executed_operation_uri:
                return _deepcopy(item)
        return None

    def _fetch_executed_operations(operation_uris: list[str]) -> list[dict[str, Any]]:
        return [
            _deepcopy(state["executed_operations"][uri])
            for uri in operation_uris
            if uri in state["executed_operations"]
        ]

    def _persist_operation_assessment(payload: dict[str, Any]) -> dict[str, Any]:
        state["assessments"].append(_deepcopy(payload))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOperationAssessments": 1,
            "persistedEvents": 1,
        }

    def _list_operation_assessments(
        *,
        farm_uri: str,
        executed_operation_uri: str,
        profile_key: str | None = None,
    ) -> list[dict[str, Any]]:
        items = [
            _deepcopy(item)
            for item in state["assessments"]
            if item["farmUri"] == farm_uri
            and item["executedOperationUri"] == executed_operation_uri
            and (profile_key is None or item["profileKey"] == profile_key)
        ]
        items.sort(key=lambda item: (item.get("recordedAt") or "", item["assessmentUri"]), reverse=True)
        return items

    def _persist_operation_attestation_action(payload: dict[str, Any]) -> dict[str, Any]:
        state["actions"].append(_deepcopy(payload))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOperationAttestationActions": 1,
            "persistedEvents": 1,
        }

    def _list_operation_attestation_actions(
        *,
        farm_uri: str,
        executed_operation_uri: str,
        profile_key: str | None = None,
    ) -> list[dict[str, Any]]:
        items = [
            _deepcopy(item)
            for item in state["actions"]
            if item["farmUri"] == farm_uri
            and item["executedOperationUri"] == executed_operation_uri
            and (profile_key is None or item["profileKey"] == profile_key)
        ]
        items.sort(key=lambda item: (item.get("recordedAt") or "", item["operationAttestationActionUri"]))
        return items

    def _persist_operation_report_binding_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
        state["report_binding_snapshots"].append(_deepcopy(payload))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOperationReportBindingSnapshots": 1,
            "persistedEvents": 1,
        }

    def _list_operation_report_binding_snapshots(
        *,
        farm_uri: str,
        executed_operation_uri: str,
        profile_key: str | None = None,
        template_code: str | None = None,
        layout_code: str | None = None,
    ) -> list[dict[str, Any]]:
        items = [
            _deepcopy(item)
            for item in state["report_binding_snapshots"]
            if item["farmUri"] == farm_uri
            and item["executedOperationUri"] == executed_operation_uri
            and (profile_key is None or item["profileKey"] == profile_key)
            and (template_code is None or item["templateCode"] == template_code)
            and (layout_code is None or item["layoutCode"] == layout_code)
        ]
        items.sort(key=lambda item: (item.get("recordedAt") or "", item["operationReportBindingSnapshotUri"]), reverse=True)
        return items

    def _create_planting_event(request) -> dict[str, Any]:
        state["executed_operations"][request.executedOperationUri] = {
            "uri": request.executedOperationUri,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "status": request.status,
            "startTime": request.plantingStart,
            "endTime": request.plantingEnd,
        }
        return {
            "plantingEventUri": f"urn:planting-event:{len(state['executed_operations'])}",
            "executedOperationUri": request.executedOperationUri,
            "plannedOperationUri": request.plannedOperationUri,
            "status": request.status,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "plantingStart": request.plantingStart,
            "plantingEnd": request.plantingEnd,
            "areaPlantedHa": request.areaPlantedHa,
            "seedLotUri": request.seedLotUri,
            "methodCode": request.methodCode,
            "seedingRate": request.seedingRate,
            "seedingRateUnit": request.seedingRateUnit,
            "operatorRef": request.operatorRef,
            "equipmentRef": request.equipmentRef,
            "recordedAt": "2026-03-11T10:00:00Z",
            "persistence": {
                "enabled": True,
                "reason": "enabled",
                "persistedPlantingEvents": 1,
            },
        }

    def _create_harvest_event(request) -> dict[str, Any]:
        state["executed_operations"][request.executedOperationUri] = {
            "uri": request.executedOperationUri,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "status": request.status,
            "startTime": request.harvestStart,
            "endTime": request.harvestEnd,
        }
        return {
            "harvestEventUri": f"urn:harvest-event:{len(state['executed_operations'])}",
            "executedOperationUri": request.executedOperationUri,
            "plannedOperationUri": request.plannedOperationUri,
            "status": request.status,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "storageLotUri": request.storageLotUri,
            "harvestStart": request.harvestStart,
            "harvestEnd": request.harvestEnd,
            "areaHarvestedHa": request.areaHarvestedHa,
            "grossYield": request.grossYield,
            "yieldUnit": request.yieldUnit,
            "yieldMeasurementMethodCode": request.yieldMeasurementMethodCode,
            "yieldEvidenceRefs": list(request.yieldEvidenceRefs or []),
            "recordedAt": "2026-09-18T11:30:00Z",
            "persistence": {
                "enabled": True,
                "reason": "enabled",
                "persistedHarvestEvents": 1,
            },
        }

    def _create_tillage_event(request) -> dict[str, Any]:
        state["executed_operations"][request.executedOperationUri] = {
            "uri": request.executedOperationUri,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "status": request.status,
            "startTime": request.operationStart,
            "endTime": request.operationEnd,
        }
        return {
            "tillageEventUri": f"urn:tillage-event:{len(state['executed_operations'])}",
            "executedOperationUri": request.executedOperationUri,
            "plannedOperationUri": request.plannedOperationUri,
            "status": request.status,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "operationStart": request.operationStart,
            "operationEnd": request.operationEnd,
            "tillageTypeCode": request.tillageTypeCode,
            "implementCode": request.implementCode,
            "depthCm": request.depthCm,
            "operatorRef": request.operatorRef,
            "equipmentRef": request.equipmentRef,
            "recordedAt": "2026-03-12T09:30:00Z",
            "persistence": {
                "enabled": True,
                "reason": "enabled",
                "persistedTillageEvents": 1,
            },
        }

    def _create_mechanical_weeding_event(request) -> dict[str, Any]:
        state["executed_operations"][request.executedOperationUri] = {
            "uri": request.executedOperationUri,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "status": request.status,
            "startTime": request.operationStart,
            "endTime": request.operationEnd,
        }
        return {
            "mechanicalWeedingEventUri": f"urn:mechanical-weeding-event:{len(state['executed_operations'])}",
            "executedOperationUri": request.executedOperationUri,
            "plannedOperationUri": request.plannedOperationUri,
            "status": request.status,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "operationStart": request.operationStart,
            "operationEnd": request.operationEnd,
            "bbchCode": request.bbchCode,
            "methodCode": request.methodCode,
            "areaTreatedHa": request.areaTreatedHa,
            "operatorRef": request.operatorRef,
            "equipmentRef": request.equipmentRef,
            "recordedAt": "2026-03-12T10:15:00Z",
            "persistence": {
                "enabled": True,
                "reason": "enabled",
                "persistedMechanicalWeedingEvents": 1,
            },
        }

    def _create_cover_crop_management_event(request) -> dict[str, Any]:
        action_start = f"{request.actionDate}T00:00:00Z"
        state["executed_operations"][request.executedOperationUri] = {
            "uri": request.executedOperationUri,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "status": request.status,
            "startTime": action_start,
            "endTime": action_start,
        }
        return {
            "coverCropManagementEventUri": f"urn:cover-crop-event:{len(state['executed_operations'])}",
            "executedOperationUri": request.executedOperationUri,
            "plannedOperationUri": request.plannedOperationUri,
            "status": request.status,
            "fieldUri": request.fieldUri,
            "cropInstanceUri": request.cropInstanceUri,
            "seasonRef": request.seasonRef,
            "coverCropSpeciesCode": request.coverCropSpeciesCode,
            "managementActionCode": request.managementActionCode,
            "actionDate": request.actionDate,
            "methodCode": request.methodCode,
            "operatorRef": request.operatorRef,
            "equipmentRef": request.equipmentRef,
            "seedingRate": request.seedingRate,
            "rateUnit": request.rateUnit,
            "recordedAt": "2026-09-20T09:00:00Z",
            "persistence": {
                "enabled": True,
                "reason": "enabled",
                "persistedCoverCropEvents": 1,
            },
        }

    monkeypatch.setattr(main_module.PERSISTENCE, "persist_operation_proposals", _persist_operation_proposals)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_operation_proposal", _fetch_operation_proposal)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "link_operation_proposal_to_draft",
        _link_operation_proposal_to_draft,
    )
    monkeypatch.setattr(main_module.PERSISTENCE, "persist_operation_draft", _persist_operation_draft)
    monkeypatch.setattr(main_module.PERSISTENCE, "update_operation_draft", _update_operation_draft)
    monkeypatch.setattr(main_module.PERSISTENCE, "persist_operation_draft_commit", _persist_operation_draft_commit)
    monkeypatch.setattr(main_module.PERSISTENCE, "list_operation_drafts", _list_operation_drafts)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_operation_draft", _fetch_operation_draft)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_operation_draft_for_executed_operation",
        _fetch_operation_draft_for_executed_operation,
    )
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_executed_operations", _fetch_executed_operations)
    monkeypatch.setattr(main_module.PERSISTENCE, "persist_operation_assessment", _persist_operation_assessment)
    monkeypatch.setattr(main_module.PERSISTENCE, "list_operation_assessments", _list_operation_assessments)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_operation_attestation_action",
        _persist_operation_attestation_action,
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "list_operation_attestation_actions",
        _list_operation_attestation_actions,
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_operation_report_binding_snapshot",
        _persist_operation_report_binding_snapshot,
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "list_operation_report_binding_snapshots",
        _list_operation_report_binding_snapshots,
    )
    monkeypatch.setattr(main_module, "create_planting_event", _create_planting_event)
    monkeypatch.setattr(main_module, "create_harvest_event", _create_harvest_event)
    monkeypatch.setattr(main_module, "create_tillage_event", _create_tillage_event)
    monkeypatch.setattr(main_module, "create_mechanical_weeding_event", _create_mechanical_weeding_event)
    monkeypatch.setattr(main_module, "create_cover_crop_management_event", _create_cover_crop_management_event)

    def _build_si_org_control_pack_payload(*, persistence, farm_uri: str, period_start: str, period_end: str, include_evidence: bool):
        a1_rows = []
        a2_rows = []
        a3_rows = []
        for draft in state["drafts"].values():
            if draft.get("farmUri") != farm_uri:
                continue
            executed_operation_uri = str(draft.get("committedExecutedOperationUri") or "").strip()
            if not executed_operation_uri:
                continue
            operation_family_code = str(draft.get("operationFamilyCode") or "").strip().lower()
            if operation_family_code == "harvest":
                a3_rows.append(
                    {
                        "executedOperationUri": executed_operation_uri,
                        "executedOperationUris": [executed_operation_uri],
                    }
                )
            elif operation_family_code == "fertilizer_application":
                a2_rows.append({"executedOperationUri": executed_operation_uri})
            elif operation_family_code in {
                "planting",
                "irrigation",
                "tillage",
                "mechanical_weeding",
                "cover_crop_management",
            }:
                a1_rows.append({"executedOperationUri": executed_operation_uri})
        return {
            "bindingWarnings": [],
            "recordbook": {
                "A_plantProduction": {
                    "A1_workDiary": a1_rows,
                    "A2_fertilizationDiary": a2_rows,
                    "A3_harvestLog": a3_rows,
                }
            },
        }

    monkeypatch.setattr(main_module, "build_si_org_control_pack_payload", _build_si_org_control_pack_payload)
    return state


def _seed_committed_review_draft(
    state: dict[str, Any],
    *,
    operation_family_code: str,
    executed_operation_uri: str,
    start_time: str,
    end_time: str,
    draft_payload: dict[str, Any],
    commit_result: dict[str, Any],
) -> str:
    draft_uri = f"urn:operation-draft:test:{operation_family_code}:1"
    state["drafts"][draft_uri] = {
        "operationDraftUri": draft_uri,
        "farmUri": DEFAULT_FARM_URI,
        "operationFamilyCode": operation_family_code,
        "profileKey": "si:organic:crops_only:2026",
        "proposalUri": None,
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "committedExecutedOperationUri": executed_operation_uri,
        "note": f"{operation_family_code} voice commit",
        "cropContext": {"cropInstanceUri": DEFAULT_CROP_INSTANCE_URI, "cropLabel": "Wheat"},
        "draftPayload": copy.deepcopy(draft_payload),
        "draftEvidence": [
            {
                "evidenceType": "voice_transcript",
                "payload": {"routeCode": "voice_test"},
            }
        ],
        "commitResult": copy.deepcopy(commit_result),
        "state": "committed",
        "committedAt": "2026-03-18T10:00:00Z",
        "recordedAt": "2026-03-18T09:59:00Z",
        "updatedAt": "2026-03-18T10:00:00Z",
    }
    state["executed_operations"][executed_operation_uri] = {
        "uri": executed_operation_uri,
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "status": "completed",
        "startTime": start_time,
        "endTime": end_time,
    }
    return draft_uri


def _draft_create_payload(*, include_operator_attestation: bool) -> dict[str, Any]:
    draft_evidence = []
    if include_operator_attestation:
        draft_evidence.append(
            {
                "evidenceType": "operator_attestation",
                "evidenceRef": "attest://operator/1",
            }
        )
    return {
        "operationFamilyCode": "planting",
        "profileKey": "si:organic:crops_only:2026",
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "draftPayload": {
            "plantingStart": "2026-03-11T08:00:00Z",
            "plantingEnd": "2026-03-11T09:00:00Z",
            "areaPlantedHa": 3.4,
            "seedLotUri": "urn:seed-lot:1",
            "methodCode": "drill",
            "seedingRate": 180.0,
            "seedingRateUnit": "kg/ha",
            "operatorRef": "urn:party:operator:1",
            "equipmentRef": "urn:asset:tractor:1",
            "status": "completed",
        },
        "draftEvidence": draft_evidence,
        "note": "Planting draft",
    }


def _harvest_draft_create_payload(*, include_operator_attestation: bool) -> dict[str, Any]:
    draft_evidence = []
    if include_operator_attestation:
        draft_evidence.append(
            {
                "evidenceType": "operator_attestation",
                "evidenceRef": "attest://operator/harvest/1",
            }
        )
    return {
        "operationFamilyCode": "harvest",
        "profileKey": "si:organic:crops_only:2026",
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "draftPayload": {
            "harvestStart": "2026-09-18T07:00:00Z",
            "harvestEnd": "2026-09-18T11:00:00Z",
            "areaHarvestedHa": 3.4,
            "grossYield": 14250.0,
            "yieldUnit": "kg",
            "storageLotUri": "urn:storage-lot:1",
            "status": "completed",
            "yieldMeasurementMethodCode": "scale_ticket",
            "yieldEvidenceRefs": ["urn:evidence:scale-ticket:1"],
        },
        "draftEvidence": draft_evidence,
        "note": "Harvest draft",
    }


def _tillage_draft_create_payload(*, include_operator_attestation: bool) -> dict[str, Any]:
    draft_evidence = []
    if include_operator_attestation:
        draft_evidence.append(
            {
                "evidenceType": "operator_attestation",
                "evidenceRef": "attest://operator/tillage/1",
            }
        )
    return {
        "operationFamilyCode": "tillage",
        "profileKey": "si:organic:crops_only:2026",
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "draftPayload": {
            "operationStart": "2026-03-12T08:00:00Z",
            "operationEnd": "2026-03-12T09:30:00Z",
            "tillageTypeCode": "primary",
            "implementCode": "plough",
            "depthCm": 24,
            "operatorRef": "urn:party:operator:1",
            "equipmentRef": "urn:asset:tractor:1",
            "status": "completed",
        },
        "draftEvidence": draft_evidence,
        "note": "Tillage draft",
    }


def _mechanical_weeding_draft_create_payload(*, include_operator_attestation: bool) -> dict[str, Any]:
    draft_evidence = []
    if include_operator_attestation:
        draft_evidence.append(
            {
                "evidenceType": "operator_attestation",
                "evidenceRef": "attest://operator/mechanical-weeding/1",
            }
        )
    return {
        "operationFamilyCode": "mechanical_weeding",
        "profileKey": "si:organic:crops_only:2026",
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "draftPayload": {
            "operationStart": "2026-04-08T07:30:00Z",
            "operationEnd": "2026-04-08T09:00:00Z",
            "bbchCode": "14",
            "methodCode": "inter_row_cultivation",
            "areaTreatedHa": 3.4,
            "operatorRef": "urn:party:operator:1",
            "equipmentRef": "urn:asset:tractor:1",
            "status": "completed",
        },
        "draftEvidence": draft_evidence,
        "note": "Mechanical weeding draft",
    }


def _cover_crop_management_draft_create_payload(*, include_operator_attestation: bool) -> dict[str, Any]:
    draft_evidence = []
    if include_operator_attestation:
        draft_evidence.append(
            {
                "evidenceType": "operator_attestation",
                "evidenceRef": "attest://operator/cover-crop/1",
            }
        )
    return {
        "operationFamilyCode": "cover_crop_management",
        "profileKey": "si:organic:crops_only:2026",
        "fieldUri": DEFAULT_FIELD_URI,
        "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
        "draftPayload": {
            "seasonRef": "2026",
            "coverCropSpeciesCode": "phacelia",
            "managementActionCode": "establish",
            "actionDate": "2026-09-20",
            "methodCode": "drill",
            "operatorRef": "urn:party:operator:1",
            "equipmentRef": "urn:asset:tractor:1",
            "status": "completed",
            "seedingRate": 14.0,
            "rateUnit": "kg/ha",
        },
        "draftEvidence": draft_evidence,
        "note": "Cover crop management draft",
    }


def test_capabilities_endpoint_includes_operation_feature_flags(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    monkeypatch.setenv("OPERATION_PROPOSALS_MIN_CLIENT_VERSION", "ios-1.7.9")
    monkeypatch.setenv("OPERATION_DRAFTS_MIN_CLIENT_VERSION", "ios-1.8.0")
    monkeypatch.setenv("OPERATION_ASSESSMENTS_MIN_CLIENT_VERSION", "ios-1.8.1")
    monkeypatch.setenv("CONTROL_CENTER_ATTESTATION_WORKBENCH_MIN_CLIENT_VERSION", "ios-1.8.2")

    response = client.get("/v1/capabilities")

    assert response.status_code == 200
    data = response.json()
    assert data["features"]["operationProposals"]["enabled"] is True
    assert data["features"]["operationProposals"]["minClientVersion"] == "ios-1.7.9"
    assert data["features"]["operationCatalog"]["enabled"] is True
    assert data["features"]["operationCatalog"]["minClientVersion"] == "ios-1.8.0"
    assert data["features"]["operationDrafts"]["enabled"] is True
    assert data["features"]["operationDrafts"]["minClientVersion"] == "ios-1.8.0"
    assert data["features"]["operationAssessments"]["enabled"] is True
    assert data["features"]["operationAssessments"]["minClientVersion"] == "ios-1.8.1"
    assert data["features"]["operationAttestation"]["enabled"] is True
    assert data["features"]["operationAttestation"]["minClientVersion"] == "ios-1.8.2"
    assert data["features"]["controlCenterReviewQueue"]["enabled"] is True
    assert data["features"]["controlCenterReviewQueue"]["minClientVersion"] == "ios-1.8.2"
    assert data["features"]["controlCenterAttestationWorkbench"]["enabled"] is True
    assert data["features"]["controlCenterAttestationWorkbench"]["minClientVersion"] == "ios-1.8.2"


def test_operation_catalog_lists_regulatory_operation_families(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)

    response = client.get("/v1/operations/catalog")

    assert response.status_code == 200
    items = {item["operationFamilyCode"]: item for item in response.json()["items"]}
    assert items["planting"]["commitRoute"] == "/v1/field-ops/planting-events"
    assert items["harvest"]["commitRoute"] == "/v1/field-ops/harvest-events"
    assert items["tillage"]["commitRoute"] == "/v1/field-ops/tillage-events"
    assert items["mechanical_weeding"]["commitRoute"] == "/v1/field-ops/mechanical-weeding-events"
    assert items["cover_crop_management"]["commitRoute"] == "/v1/field-ops/cover-crop-management-events"


def test_operation_draft_lifecycle_reaches_report_ready_with_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    state = _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=True))
    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft["state"] == "saveable"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    executed_operation_uri = committed["operationDraft"]["committedExecutedOperationUri"]
    assert committed["operationDraft"]["state"] == "committed"
    assert committed["operationDraft"]["persistence"]["refreshedOperationReportBindingSnapshots"] == 1
    assert committed["assessment"]["attestationState"] == "non_attested"
    assert committed["assessment"]["lifecycleState"] == "non_attested"
    assert committed["assessment"]["reportReady"] is False
    assert len(state["report_binding_snapshots"]) == 1

    partial_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_partially_attested"},
    )
    assert partial_response.status_code == 200
    partial = partial_response.json()
    assert partial["attestationState"] == "partially_attested"
    assert partial["lifecycleState"] == "partially_attested"
    assert partial["reportReady"] is False
    assert partial["persistence"]["refreshedOperationReportBindingSnapshots"] == 1
    assert len(state["report_binding_snapshots"]) == 2

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    attested = attest_response.json()
    assert attested["attestationState"] == "attested"
    assert attested["lifecycleState"] == "report_ready"
    assert attested["reportReady"] is True
    assert attested["persistence"]["refreshedOperationReportBindingSnapshots"] == 1
    assert len(state["report_binding_snapshots"]) == 3

    assessments_response = client.get(f"/v1/operations/{executed_operation_uri}/assessments")
    assert assessments_response.status_code == 200
    assessments = assessments_response.json()
    assert assessments["total"] == 3
    assert assessments["items"][0]["lifecycleState"] == "report_ready"
    assert assessments["items"][0]["requirementResults"]
    assert assessments["items"][0]["evidenceSummary"]["operatorAttestationPresent"] is True


def test_harvest_operation_draft_lifecycle_reaches_report_ready_with_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_harvest_draft_create_payload(include_operator_attestation=True))
    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft["state"] == "saveable"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    executed_operation_uri = committed["operationDraft"]["committedExecutedOperationUri"]
    assert committed["operationDraft"]["state"] == "committed"
    assert committed["harvestEvent"]["storageLotUri"] == "urn:storage-lot:1"
    requirement_codes = {
        item["requirementCode"]: item["status"]
        for item in committed["assessment"]["requirementResults"]
    }
    assert requirement_codes["storage_lot_recorded"] == "met"
    assert requirement_codes["yield_recorded"] == "met"
    assert committed["assessment"]["reportReady"] is False

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    attested = attest_response.json()
    assert attested["attestationState"] == "attested"
    assert attested["lifecycleState"] == "report_ready"
    assert attested["reportReady"] is True


def test_tillage_operation_draft_lifecycle_reaches_report_ready_with_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_tillage_draft_create_payload(include_operator_attestation=True))
    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft["state"] == "saveable"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    executed_operation_uri = committed["operationDraft"]["committedExecutedOperationUri"]
    assert committed["operationDraft"]["state"] == "committed"
    assert committed["tillageEvent"]["tillageTypeCode"] == "primary"
    requirement_codes = {
        item["requirementCode"]: item["status"]
        for item in committed["assessment"]["requirementResults"]
    }
    assert requirement_codes["tillage_type_recorded"] == "met"
    assert requirement_codes["implement_recorded"] == "met"
    assert committed["assessment"]["reportReady"] is False

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    attested = attest_response.json()
    assert attested["attestationState"] == "attested"
    assert attested["lifecycleState"] == "report_ready"
    assert attested["reportReady"] is True


def test_mechanical_weeding_operation_draft_lifecycle_reaches_report_ready_with_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post(
        "/v1/operations/drafts",
        json=_mechanical_weeding_draft_create_payload(include_operator_attestation=True),
    )
    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft["state"] == "saveable"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    executed_operation_uri = committed["operationDraft"]["committedExecutedOperationUri"]
    assert committed["operationDraft"]["state"] == "committed"
    assert committed["mechanicalWeedingEvent"]["methodCode"] == "inter_row_cultivation"
    requirement_codes = {
        item["requirementCode"]: item["status"]
        for item in committed["assessment"]["requirementResults"]
    }
    assert requirement_codes["weeding_method_recorded"] == "met"
    assert requirement_codes["area_treated_recorded"] == "met"
    assert committed["assessment"]["reportReady"] is False

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    attested = attest_response.json()
    assert attested["attestationState"] == "attested"
    assert attested["lifecycleState"] == "report_ready"
    assert attested["reportReady"] is True


def test_cover_crop_management_operation_draft_lifecycle_reaches_report_ready_with_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post(
        "/v1/operations/drafts",
        json=_cover_crop_management_draft_create_payload(include_operator_attestation=True),
    )
    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft["state"] == "saveable"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    executed_operation_uri = committed["operationDraft"]["committedExecutedOperationUri"]
    assert committed["operationDraft"]["state"] == "committed"
    assert committed["coverCropManagementEvent"]["coverCropSpeciesCode"] == "phacelia"
    requirement_codes = {
        item["requirementCode"]: item["status"]
        for item in committed["assessment"]["requirementResults"]
    }
    assert requirement_codes["cover_crop_species_recorded"] == "met"
    assert requirement_codes["management_action_recorded"] == "met"
    assert committed["assessment"]["reportReady"] is False

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    attested = attest_response.json()
    assert attested["attestationState"] == "attested"
    assert attested["lifecycleState"] == "report_ready"
    assert attested["reportReady"] is True


def test_operation_attested_state_stays_not_report_ready_without_operator_attestation(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    executed_operation_uri = commit_response.json()["operationDraft"]["committedExecutedOperationUri"]

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    data = attest_response.json()
    assert data["attestationState"] == "attested"
    assert data["lifecycleState"] == "attested"
    assert data["reportReady"] is False
    requirement_codes = {item["requirementCode"]: item["status"] for item in data["requirementResults"]}
    assert requirement_codes["operator_attestation"] == "missing"


def test_operation_draft_commit_resolves_missing_crop_instance_from_crop_context(monkeypatch) -> None:
    import app.main as main_module

    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    def _ensure_crop_context(request):
        assert request.fieldUri == DEFAULT_FIELD_URI
        assert request.seedLotUri == "urn:seed-lot:1"
        assert request.cropLabel == "Wheat"
        assert request.productionStatus == "organic_certified"
        return main_module.CropContextEnsureResponse(
            cropInstanceUri="urn:crop-instance:ensured-1",
            cropUri="urn:crop:wheat",
            seasonCode="2026",
            productionStatus="organic_certified",
            cropIdentitySource="draft_crop_label",
            varietyIdentitySource="unknown",
            productionStatusSource="draft_crop_context",
            matchedBy="crop_context_ensure",
            warnings=[],
        )

    monkeypatch.setattr(main_module, "ensure_crop_context", _ensure_crop_context)

    create_response = client.post(
        "/v1/operations/drafts",
        json={
            "operationFamilyCode": "planting",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "cropContext": {
                "seasonCode": "2026",
                "cropLabel": "Wheat",
                "productionStatus": "organic_certified",
                "seedLotUri": "urn:seed-lot:1",
            },
                "draftPayload": {
                    "plantingStart": "2026-03-11T08:00:00Z",
                    "plantingEnd": "2026-03-11T09:00:00Z",
                    "areaPlantedHa": 3.4,
                    "seedLotUri": "urn:seed-lot:1",
                    "methodCode": "drill",
                    "seedingRate": 180.0,
                    "seedingRateUnit": "kg/ha",
                    "operatorRef": "urn:party:operator:1",
                    "equipmentRef": "urn:asset:tractor:1",
                    "status": "completed",
                },
            },
        )

    assert create_response.status_code == 200
    draft = create_response.json()
    assert draft.get("cropInstanceUri") is None
    assert draft["cropContext"]["seasonCode"] == "2026"
    assert draft["cropContext"]["cropLabel"] == "Wheat"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    assert committed["operationDraft"]["cropInstanceUri"] == "urn:crop-instance:ensured-1"
    assert committed["operationDraft"]["cropContext"]["cropInstanceUri"] == "urn:crop-instance:ensured-1"
    assert committed["operationDraft"]["cropContext"]["seasonCode"] == "2026"
    assert committed["plantingEvent"]["cropInstanceUri"] == "urn:crop-instance:ensured-1"


def test_patch_operation_draft_incrementally_merges_payload_evidence_and_crop_context(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post(
        "/v1/operations/drafts",
        json={
            "operationFamilyCode": "planting",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "cropContext": {
                "seasonCode": "2026",
                "cropLabel": "Wheat",
            },
            "draftPayload": {
                "plantingStart": "2026-03-11T08:00:00Z",
                "seedLotUri": "urn:seed-lot:1",
                "methodCode": "drill",
                "operatorRef": "urn:party:operator:1",
                "equipmentRef": "urn:asset:tractor:1",
                "status": "completed",
            },
            "draftEvidence": [
                {
                    "evidenceType": "operator_attestation",
                    "evidenceRef": "attest://operator/seed/1",
                }
            ],
            "note": "Initial draft",
        },
    )
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    patch_response = client.patch(
        f"/v1/operations/drafts/{draft_uri}",
        json={
            "cropContext": {
                "cropVarietyLabel": "Renan",
            },
            "draftPayload": {
                "plantingEnd": "2026-03-11T09:00:00Z",
                "areaPlantedHa": 3.4,
            },
            "draftEvidence": [
                {
                    "evidenceType": "external_document",
                    "evidenceRef": "urn:evidence:seed-label:1",
                }
            ],
            "note": "Updated draft",
        },
    )

    assert patch_response.status_code == 200
    patched = patch_response.json()
    assert patched["note"] == "Updated draft"
    assert patched["cropContext"]["seasonCode"] == "2026"
    assert patched["cropContext"]["cropLabel"] == "Wheat"
    assert patched["cropContext"]["cropVarietyLabel"] == "Renan"
    assert patched["draftPayload"]["plantingStart"] == "2026-03-11T08:00:00Z"
    assert patched["draftPayload"]["plantingEnd"] == "2026-03-11T09:00:00Z"
    assert patched["draftPayload"]["seedLotUri"] == "urn:seed-lot:1"
    assert patched["draftPayload"]["areaPlantedHa"] == 3.4
    evidence_pairs = {
        (item["evidenceType"], item.get("evidenceRef"))
        for item in patched["draftEvidence"]
    }
    assert ("operator_attestation", "attest://operator/seed/1") in evidence_pairs
    assert ("external_document", "urn:evidence:seed-label:1") in evidence_pairs

    get_response = client.get(f"/v1/operations/drafts/{draft_uri}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["cropContext"]["cropVarietyLabel"] == "Renan"
    assert fetched["draftPayload"]["plantingEnd"] == "2026-03-11T09:00:00Z"
    fetched_pairs = {
        (item["evidenceType"], item.get("evidenceRef"))
        for item in fetched["draftEvidence"]
    }
    assert fetched_pairs == evidence_pairs


def test_patch_operation_draft_rejects_all_changes_after_commit(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=True))
    draft_uri = create_response.json()["operationDraftUri"]
    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200

    patch_response = client.patch(
        f"/v1/operations/drafts/{draft_uri}",
        json={"draftPayload": {"plantingStart": "2026-03-11T07:00:00Z"}},
    )
    assert patch_response.status_code == 409
    assert patch_response.json()["detail"]["code"] == "draft_already_committed"


def test_operation_proposal_from_ocr_prefills_and_links_draft(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    proposal_response = client.post(
        "/v1/operations/proposals",
        json={
            "operationFamilyCode": "planting",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "sourceKind": "ocr",
            "promptText": "Seed label intake",
            "structuredInput": {
                "plantingStart": "2026-03-11T08:00:00Z",
                "methodCode": "drill",
            },
            "ocrParseResult": {
                "status": "OK",
                "documentType": "label",
                "documentUri": "urn:document:seed-label:1",
                "items": [
                    {
                        "itemType": "label_lot",
                        "rawText": "Organic wheat seed Renan lot LOT-123 25 kg",
                        "warnings": [],
                        "proposals": {
                            "cropLabel": {
                                "valueText": "Wheat",
                                "confidence": 0.93,
                                "provenance": {"lineIndices": [0]},
                            },
                            "variety": {
                                "valueText": "Renan",
                                "confidence": 0.91,
                                "provenance": {"lineIndices": [0]},
                            },
                            "lotCode": {
                                "valueText": "LOT-123",
                                "confidence": 0.95,
                                "provenance": {"lineIndices": [0]},
                            },
                            "statusCode": {
                                "valueText": "E",
                                "confidence": 0.9,
                                "provenance": {"lineIndices": [0]},
                            },
                            "quantity": {
                                "valueNum": 25,
                                "unit": "kg",
                                "confidence": 0.88,
                                "provenance": {"lineIndices": [0]},
                            },
                        },
                    }
                ],
            },
            "note": "OCR seed label",
        },
    )

    assert proposal_response.status_code == 200
    proposal_batch = proposal_response.json()
    assert proposal_batch["total"] == 1
    proposal = proposal_batch["items"][0]
    assert proposal["cropContext"]["cropLabel"] == "Wheat"
    assert proposal["cropContext"]["cropVarietyLabel"] == "Renan"
    assert proposal["cropContext"]["productionStatus"] == "organic_certified"
    assert proposal["payloadDraft"]["seedLotCodeHint"] == "LOT-123"
    assert proposal["payloadDraft"]["seedQuantityValueHint"] == 25
    assert proposal["sourceEvidence"][0]["evidenceType"] == "ocr_parse_item"

    draft_response = client.post(
        "/v1/operations/drafts",
        json={
            "operationFamilyCode": "planting",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "proposalUri": proposal["proposalUri"],
            "draftPayload": {
                "plantingStart": "2026-03-11T08:00:00Z",
                "plantingEnd": "2026-03-11T09:00:00Z",
                "areaPlantedHa": 3.4,
                "seedLotUri": "urn:seed-lot:1",
                "methodCode": "drill",
                "status": "completed",
            },
        },
    )

    assert draft_response.status_code == 200
    draft = draft_response.json()
    assert draft["proposalUri"] == proposal["proposalUri"]
    assert draft["cropContext"]["cropLabel"] == "Wheat"
    assert draft["cropContext"]["cropVarietyLabel"] == "Renan"
    assert draft["draftPayload"]["seedLotCodeHint"] == "LOT-123"
    assert draft["draftPayload"]["seedLotUri"] == "urn:seed-lot:1"
    assert draft["note"] == "OCR seed label"

    get_response = client.get(f"/v1/operations/proposals/{proposal['proposalUri']}")
    assert get_response.status_code == 200
    assert get_response.json()["acceptedOperationDraftUri"] == draft["operationDraftUri"]


def test_operation_proposal_manual_harvest_prefills_and_commits(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    proposal_response = client.post(
        "/v1/operations/proposals",
        json={
            "operationFamilyCode": "harvest",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
            "sourceKind": "manual",
            "structuredInput": {
                "harvestStart": "2026-09-18T07:00:00Z",
                "harvestEnd": "2026-09-18T11:00:00Z",
                "areaHarvestedHa": 3.4,
                "grossYield": 14250.0,
                "yieldUnit": "kg",
                "storageLotUri": "urn:storage-lot:1",
                "yieldMeasurementMethodCode": "scale_ticket",
                "yieldEvidenceRefs": ["urn:evidence:scale-ticket:1"],
                "status": "completed",
            },
            "note": "Manual harvest proposal",
        },
    )

    assert proposal_response.status_code == 200
    proposal_batch = proposal_response.json()
    assert proposal_batch["total"] == 1
    proposal = proposal_batch["items"][0]
    assert proposal["payloadDraft"]["grossYield"] == 14250.0
    assert proposal["payloadDraft"]["storageLotUri"] == "urn:storage-lot:1"

    draft_response = client.post(
        "/v1/operations/drafts",
        json={
            "operationFamilyCode": "harvest",
            "profileKey": "si:organic:crops_only:2026",
            "fieldUri": DEFAULT_FIELD_URI,
            "cropInstanceUri": DEFAULT_CROP_INSTANCE_URI,
            "proposalUri": proposal["proposalUri"],
            "draftEvidence": [
                {
                    "evidenceType": "operator_attestation",
                    "evidenceRef": "attest://operator/harvest/proposal",
                }
            ],
        },
    )

    assert draft_response.status_code == 200
    draft = draft_response.json()
    assert draft["proposalUri"] == proposal["proposalUri"]
    assert draft["draftPayload"]["grossYield"] == 14250.0
    assert draft["draftPayload"]["storageLotUri"] == "urn:storage-lot:1"

    commit_response = client.post(f"/v1/operations/drafts/{draft['operationDraftUri']}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()
    assert committed["harvestEvent"]["grossYield"] == 14250.0
    assert committed["assessment"]["reportReady"] is False

    get_response = client.get(f"/v1/operations/proposals/{proposal['proposalUri']}")
    assert get_response.status_code == 200
    assert get_response.json()["acceptedOperationDraftUri"] == draft["operationDraftUri"]


def test_control_center_review_queue_and_detail_surface_missing_requirements(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()

    queue_response = client.get("/v1/control-center/review-queue")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["executedOperationUri"] == committed["operationDraft"]["committedExecutedOperationUri"]
    assert review_item["attestationState"] == "non_attested"
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]
    assert review_item["reportBindingRecordedAt"]
    assert review_item["reportBindingNeedsRefresh"] is False
    assert review_item["nextActionCode"] == "attach_operator_attestation"
    assert review_item["blocking"] is True

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["draft"]["operationDraftUri"] == draft_uri
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/planting-events"
    assert detail["reportBindings"][0]["templateCode"] == "ORG-CONTROL-PACK"
    assert detail["reportBindings"][0]["recordedAt"]
    assert detail["reportBindings"][0]["needsRefresh"] is False
    assert detail["reportBindingRecordedAt"] == review_item["reportBindingRecordedAt"]
    assert detail["reportBindingNeedsRefresh"] is False
    assert detail["auditTrail"][0]["eventCode"] == "draft_committed"


def test_control_center_review_detail_uses_harvest_commit_route(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_harvest_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=harvest")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["executedOperationUri"] == committed["operationDraft"]["committedExecutedOperationUri"]
    assert "storage_lot_recorded" not in review_item["missingRequirementCodes"]
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/harvest-events"
    assert detail["assessment"]["operationFamilyCode"] == "harvest"
    assert detail["reportBindings"][0]["blockingReasonCodes"] == ["operator_attestation"]


def test_control_center_review_detail_uses_tillage_commit_route(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_tillage_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=tillage")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["executedOperationUri"] == committed["operationDraft"]["committedExecutedOperationUri"]
    assert "tillage_type_recorded" not in review_item["missingRequirementCodes"]
    assert "implement_recorded" not in review_item["missingRequirementCodes"]
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/tillage-events"
    assert detail["assessment"]["operationFamilyCode"] == "tillage"


def test_control_center_review_detail_uses_mechanical_weeding_commit_route(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post(
        "/v1/operations/drafts",
        json=_mechanical_weeding_draft_create_payload(include_operator_attestation=False),
    )
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=mechanical_weeding")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["executedOperationUri"] == committed["operationDraft"]["committedExecutedOperationUri"]
    assert "weeding_method_recorded" not in review_item["missingRequirementCodes"]
    assert "area_treated_recorded" not in review_item["missingRequirementCodes"]
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/mechanical-weeding-events"
    assert detail["assessment"]["operationFamilyCode"] == "mechanical_weeding"


def test_control_center_review_detail_uses_cover_crop_management_commit_route(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post(
        "/v1/operations/drafts",
        json=_cover_crop_management_draft_create_payload(include_operator_attestation=False),
    )
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    committed = commit_response.json()

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=cover_crop_management")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["executedOperationUri"] == committed["operationDraft"]["committedExecutedOperationUri"]
    assert "cover_crop_species_recorded" not in review_item["missingRequirementCodes"]
    assert "management_action_recorded" not in review_item["missingRequirementCodes"]
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/cover-crop-management-events"
    assert detail["assessment"]["operationFamilyCode"] == "cover_crop_management"
    assert detail["reportBindings"][0]["blockingReasonCodes"] == ["operator_attestation"]


def test_control_center_detail_report_binding_uses_real_binder_presence(monkeypatch) -> None:
    import app.main as main_module

    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    monkeypatch.setattr(
        main_module,
        "build_si_org_control_pack_payload",
        lambda **kwargs: {
            "bindingWarnings": [],
            "recordbook": {
                "A_plantProduction": {
                    "A1_workDiary": [],
                    "A3_harvestLog": [],
                }
            },
        },
    )

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=True))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]

    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200
    executed_operation_uri = commit_response.json()["operationDraft"]["committedExecutedOperationUri"]

    attest_response = client.post(
        f"/v1/operations/{executed_operation_uri}/attestations",
        json={"actionCode": "mark_attested"},
    )
    assert attest_response.status_code == 200
    assert attest_response.json()["reportReady"] is True

    queue_response = client.get("/v1/control-center/review-queue")
    assert queue_response.status_code == 200
    review_item_uri = queue_response.json()["items"][0]["reviewItemUri"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item_uri}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["assessment"]["reportReady"] is True
    assert detail["reportBindings"][0]["reportReady"] is False
    assert detail["reportBindings"][0]["recordedAt"]
    assert detail["reportBindings"][0]["needsRefresh"] is False
    assert "report_binding_missing:A_plantProduction.A1_workDiary" in detail["reportBindings"][0]["blockingReasonCodes"]


def test_control_center_detail_reuses_cached_report_binding_snapshot(monkeypatch) -> None:
    import app.main as main_module

    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    build_calls = {"count": 0}
    original_builder = main_module.build_si_org_control_pack_payload

    def _counting_builder(**kwargs):
        build_calls["count"] += 1
        return original_builder(**kwargs)

    monkeypatch.setattr(main_module, "build_si_org_control_pack_payload", _counting_builder)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]
    client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    review_item_uri = client.get("/v1/control-center/review-queue").json()["items"][0]["reviewItemUri"]

    first_detail = client.get(f"/v1/control-center/review-items/{review_item_uri}")
    second_detail = client.get(f"/v1/control-center/review-items/{review_item_uri}")

    assert first_detail.status_code == 200
    assert second_detail.status_code == 200
    assert first_detail.json()["reportBindings"][0]["recordedAt"] == second_detail.json()["reportBindings"][0]["recordedAt"]
    assert second_detail.json()["reportBindings"][0]["needsRefresh"] is False
    assert build_calls["count"] == 1


def test_backfill_operation_report_binding_snapshots_populates_and_reuses_cache(monkeypatch) -> None:
    import app.main as main_module

    _enable_operation_features(monkeypatch)
    state = _install_operation_runtime(monkeypatch)

    build_calls = {"count": 0}
    original_builder = main_module.build_si_org_control_pack_payload

    def _counting_builder(**kwargs):
        build_calls["count"] += 1
        return original_builder(**kwargs)

    monkeypatch.setattr(main_module, "build_si_org_control_pack_payload", _counting_builder)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]
    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200

    first = main_module.backfill_operation_report_binding_snapshots(farm_uri=DEFAULT_FARM_URI)
    second = main_module.backfill_operation_report_binding_snapshots(farm_uri=DEFAULT_FARM_URI)

    assert first["totalCommittedDrafts"] == 1
    assert first["processedDrafts"] == 1
    assert first["refreshedBindings"] == 0
    assert first["cachedBindings"] == 1
    assert first["failedDrafts"] == 0
    assert len(state["report_binding_snapshots"]) == 1

    assert second["totalCommittedDrafts"] == 1
    assert second["processedDrafts"] == 1
    assert second["cachedBindings"] == 1
    assert second["refreshedBindings"] == 0
    assert second["failedDrafts"] == 0
    assert build_calls["count"] == 1


def test_backfill_operation_report_binding_snapshots_force_refresh_rebuilds_cache(monkeypatch) -> None:
    import app.main as main_module

    _enable_operation_features(monkeypatch)
    state = _install_operation_runtime(monkeypatch)

    build_calls = {"count": 0}
    original_builder = main_module.build_si_org_control_pack_payload

    def _counting_builder(**kwargs):
        build_calls["count"] += 1
        return original_builder(**kwargs)

    monkeypatch.setattr(main_module, "build_si_org_control_pack_payload", _counting_builder)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]
    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200

    initial = main_module.backfill_operation_report_binding_snapshots(
        farm_uri=DEFAULT_FARM_URI,
        force_refresh=True,
    )
    refreshed = main_module.backfill_operation_report_binding_snapshots(
        farm_uri=DEFAULT_FARM_URI,
        force_refresh=True,
    )

    assert initial["refreshedBindings"] == 1
    assert refreshed["refreshedBindings"] == 1
    assert refreshed["cachedBindings"] == 0
    assert refreshed["failedDrafts"] == 0
    assert len(state["report_binding_snapshots"]) == 3
    assert build_calls["count"] == 3


def test_operation_report_binding_backfill_route_requires_admin_role(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    response = client.post("/v1/operations/report-bindings:backfill", json={})

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "forbidden_operation_report_binding_backfill"


def test_operation_report_binding_backfill_route_returns_summary(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]
    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200

    response = client.post(
        "/v1/operations/report-bindings:backfill",
        json={"limit": 1, "forceRefresh": True},
        headers=_auth_headers(roles=["compliance_admin"]),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["farmUri"] == DEFAULT_FARM_URI
    assert body["limit"] == 1
    assert body["processedDrafts"] == 1
    assert body["refreshedBindings"] == 1
    assert body["failedDrafts"] == 0


def test_control_center_review_actions_attach_attestation_and_mark_attested(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    assert create_response.status_code == 200
    draft_uri = create_response.json()["operationDraftUri"]
    commit_response = client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    assert commit_response.status_code == 200

    queue_response = client.get("/v1/control-center/review-queue")
    review_item_uri = queue_response.json()["items"][0]["reviewItemUri"]

    attach_response = client.post(
        f"/v1/control-center/review-items/{review_item_uri}/actions",
        json={
            "actionCode": "attach_operator_attestation",
            "evidenceRef": "attest://operator/cc/1",
            "note": "Operator declared completion",
        },
    )
    assert attach_response.status_code == 200
    attached = attach_response.json()
    assert attached["reviewItem"]["missingRequirementCodes"] == []
    assert attached["reviewItem"]["nextActionCode"] == "mark_attested"
    assert attached["persistence"]["updatedOperationDrafts"] == 1

    attested_response = client.post(
        f"/v1/control-center/review-items/{review_item_uri}/actions",
        json={"actionCode": "mark_attested"},
    )
    assert attested_response.status_code == 200
    attested = attested_response.json()
    assert attested["reviewItem"]["attestationState"] == "attested"
    assert attested["reviewItem"]["reportReady"] is True
    assert attested["reviewItem"].get("nextActionCode") is None


def test_control_center_review_supports_fertilizer_application_voice_commits(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)

    state = _install_operation_runtime(monkeypatch)
    executed_operation_uri = "urn:executed-operation:test:fertilizer:1"
    _seed_committed_review_draft(
        state,
        operation_family_code="fertilizer_application",
        executed_operation_uri=executed_operation_uri,
        start_time="2026-03-18T08:00:00Z",
        end_time="2026-03-18T09:00:00Z",
        draft_payload={
            "applicationStart": "2026-03-18T08:00:00Z",
            "applicationEnd": "2026-03-18T09:00:00Z",
            "fertilizerType": "UREA",
            "quantityValue": 150.0,
            "quantityUnit": "kg",
            "operatorRef": "urn:party:operator:1",
        },
        commit_result={
            "targetRoute": "/v1/field-ops/fertilizer-application-events",
            "fertilizerApplicationEvent": {
                "fertilizerApplicationEventUri": "urn:fertilizer-application-event:test:1",
                "executedOperationUri": executed_operation_uri,
                "recordedAt": "2026-03-18T10:00:00Z",
            },
        },
    )

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=fertilizer_application")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["operationFamilyCode"] == "fertilizer_application"
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/fertilizer-application-events"
    assert detail["reportBindings"][0]["blockingReasonCodes"] == ["operator_attestation"]

    attach_response = client.post(
        f"/v1/control-center/review-items/{review_item['reviewItemUri']}/actions",
        json={"actionCode": "attach_operator_attestation", "evidenceRef": "attest://operator/fertilizer/1"},
    )
    assert attach_response.status_code == 200

    mark_response = client.post(
        f"/v1/control-center/review-items/{review_item['reviewItemUri']}/actions",
        json={"actionCode": "mark_attested"},
    )
    assert mark_response.status_code == 200
    assert mark_response.json()["reviewItem"]["reportReady"] is True


def test_control_center_review_supports_irrigation_voice_commits(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    state = _install_operation_runtime(monkeypatch)

    executed_operation_uri = "urn:executed-operation:test:irrigation:1"
    _seed_committed_review_draft(
        state,
        operation_family_code="irrigation",
        executed_operation_uri=executed_operation_uri,
        start_time="2026-03-19T06:00:00Z",
        end_time="2026-03-19T07:15:00Z",
        draft_payload={
            "startTime": "2026-03-19T06:00:00Z",
            "endTime": "2026-03-19T07:15:00Z",
            "volumeM3": 12.0,
            "waterSourceRef": "urn:water-source:test:1",
            "methodCode": "drip",
        },
        commit_result={
            "targetRoute": "/v1/field-ops/irrigation-events",
            "irrigationEvent": {
                "irrigationEventUri": "urn:irrigation-event:test:1",
                "executedOperationUri": executed_operation_uri,
                "recordedAt": "2026-03-19T08:00:00Z",
            },
        },
    )

    queue_response = client.get("/v1/control-center/review-queue?operationFamilyCode=irrigation")
    assert queue_response.status_code == 200
    queue = queue_response.json()
    assert queue["total"] == 1
    review_item = queue["items"][0]
    assert review_item["operationFamilyCode"] == "irrigation"
    assert review_item["missingRequirementCodes"] == ["operator_attestation"]

    detail_response = client.get(f"/v1/control-center/review-items/{review_item['reviewItemUri']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["committedOperation"]["commitRoute"] == "/v1/field-ops/irrigation-events"
    assert detail["reportBindings"][0]["blockingReasonCodes"] == ["operator_attestation"]

    attach_response = client.post(
        f"/v1/control-center/review-items/{review_item['reviewItemUri']}/actions",
        json={"actionCode": "attach_operator_attestation", "evidenceRef": "attest://operator/irrigation/1"},
    )
    assert attach_response.status_code == 200

    mark_response = client.post(
        f"/v1/control-center/review-items/{review_item['reviewItemUri']}/actions",
        json={"actionCode": "mark_attested"},
    )
    assert mark_response.status_code == 200
    assert mark_response.json()["reviewItem"]["reportReady"] is True


def test_control_center_request_evidence_action_is_advisory(monkeypatch) -> None:
    _enable_operation_features(monkeypatch)
    _install_operation_runtime(monkeypatch)

    create_response = client.post("/v1/operations/drafts", json=_draft_create_payload(include_operator_attestation=False))
    draft_uri = create_response.json()["operationDraftUri"]
    client.post(f"/v1/operations/drafts/{draft_uri}/commit")
    review_item_uri = client.get("/v1/control-center/review-queue").json()["items"][0]["reviewItemUri"]

    response = client.post(
        f"/v1/control-center/review-items/{review_item_uri}/actions",
        json={"actionCode": "request_evidence", "note": "Need operator declaration"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["actionCode"] == "request_evidence"
    assert payload["advisory"]["status"] == "advisory_only"
    assert payload["advisory"]["requestedEvidenceType"] == "operator_attestation"
