import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any

from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app

DEFAULT_FARM_URI = "https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001"
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


def _auth_headers(*, farm_uri: str = DEFAULT_FARM_URI) -> dict[str, str]:
    now = int(time.time())
    claims = {
        "sub": "test-user",
        "iat": now,
        "exp": now + 3600,
        "farmUri": farm_uri,
    }
    token = _encode_hs256_jwt(claims, secret=os.environ["FARM_RM_JWT_HS256_SECRET"])
    return {"Authorization": f"Bearer {token}", "X-Farm-URI": farm_uri}


client = TestClient(app, headers=_auth_headers())


def _install_universal_capture_session_store(
    monkeypatch,
    *,
    document_rows: dict[str, dict[str, Any]],
    parse_runs: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    session_rows: dict[str, dict[str, Any]] = {}
    capture_rows: dict[str, list[dict[str, Any]]] = {}

    monkeypatch.setattr(type(main_module.PERSISTENCE), "enabled", property(lambda self: True))
    monkeypatch.setattr(type(main_module.PERSISTENCE), "reason", property(lambda self: "enabled"))

    def _persist_intake_session_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
        session_rows[payload["sessionId"]] = {
            "sessionId": payload["sessionId"],
            "farmUri": payload["farmUri"],
            "profileId": payload["profileId"],
            "status": payload["status"],
            "selectedRouteId": payload.get("selectedRouteId"),
            "revisionNo": payload["revisionNo"],
            "currentRevisionUri": payload["currentRevisionUri"],
            "snapshot": dict(payload.get("snapshot") or {}),
            "commitResult": dict(payload.get("commitResult") or {}) if payload.get("commitResult") is not None else None,
            "createdAt": payload.get("createdAt"),
            "updatedAt": payload.get("updatedAt"),
        }
        return {"enabled": True, "persistedSessions": 1, "persistedSessionRevisions": 1}

    def _persist_intake_capture_envelope(payload: dict[str, Any]) -> dict[str, Any]:
        capture_rows.setdefault(payload["sessionId"], []).append(
            {
                "captureId": payload["captureId"],
                "sessionId": payload["sessionId"],
                "farmUri": payload["farmUri"],
                "documentUri": payload.get("documentUri"),
                "parseRunUri": payload.get("parseRunUri"),
                "modality": payload["modality"],
                "source": payload["source"],
                "locale": payload.get("locale"),
                "createdAt": payload.get("createdAt"),
                "payloadRef": dict(payload.get("payloadRef") or {}),
                "derivedRefs": dict(payload.get("derivedRefs") or {}),
                "hints": dict(payload.get("hints") or {}),
                "quality": dict(payload.get("quality") or {}),
            }
        )
        return {"enabled": True, "persistedCaptures": 1}

    monkeypatch.setattr(main_module.PERSISTENCE, "persist_intake_session_snapshot", _persist_intake_session_snapshot)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_intake_session", lambda session_id: session_rows.get(session_id))
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "list_intake_capture_envelopes",
        lambda *, session_id: list(capture_rows.get(session_id, [])),
    )
    monkeypatch.setattr(main_module.PERSISTENCE, "persist_intake_capture_envelope", _persist_intake_capture_envelope)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_document_ingest_item", lambda document_uri: document_rows.get(document_uri))
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_document_parse_run", lambda parse_run_uri: parse_runs.get(parse_run_uri))
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_latest_document_parse_run",
        lambda document_uri: next(
            (row for row in parse_runs.values() if row["documentUri"] == document_uri),
            None,
        ),
    )
    monkeypatch.setattr(main_module.PERSISTENCE, "find_resources_for_farm", lambda **kwargs: [])
    monkeypatch.setattr(main_module.PERSISTENCE, "find_field_authority_links_for_farm", lambda **kwargs: [])
    monkeypatch.setattr(main_module.PERSISTENCE, "find_field_declaration_snapshots_for_farm", lambda **kwargs: [])
    return session_rows, capture_rows


def test_universal_capture_receipt_session_ignores_embedded_label_lot_as_second_line(monkeypatch) -> None:
    document_rows = {
        "urn:document:receipt-mixed:1": {
            "documentUri": "urn:document:receipt-mixed:1",
            "farmUri": DEFAULT_FARM_URI,
            "documentHint": "receipt",
        }
    }
    parse_runs = {
        "urn:parse-run:receipt-mixed:1": {
            "parseRunUri": "urn:parse-run:receipt-mixed:1",
            "documentUri": "urn:document:receipt-mixed:1",
            "responsePayload": {
                "status": "ok",
                "documentType": "mixed",
                "documentConfidence": 0.74,
                "signals": [],
                "receipt": {
                    "vendorName": {
                        "valueText": "AGRO TRGOVINA d.o.o.",
                        "confidence": 0.72,
                        "provenance": {"lineIndices": [0]},
                    },
                    "purchaseDate": {
                        "valueDate": "2026-02-28",
                        "confidence": 0.9,
                        "provenance": {"lineIndices": [2]},
                    },
                    "receiptRef": {
                        "valueText": "Racun 2026-00017",
                        "confidence": 0.68,
                        "provenance": {"lineIndices": [1]},
                    },
                },
                "items": [
                    {
                        "itemType": "receipt_line_item",
                        "rawText": "Sunflower seed 20 kg 45.00 EUR",
                        "categoryHint": "seed",
                        "proposals": {
                            "productLabel": {
                                "valueText": "Sunflower seed EUR",
                                "confidence": 0.78,
                                "provenance": {"lineIndices": [3]},
                            },
                            "quantity": {
                                "valueNum": 20.0,
                                "unit": "kg",
                                "confidence": 0.92,
                                "provenance": {"lineIndices": [3]},
                            },
                            "cropLabel": {
                                "valueText": "Sončnica",
                                "confidence": 0.68,
                                "provenance": {"lineIndices": [3]},
                            },
                        },
                    },
                    {
                        "itemType": "label_lot",
                        "rawText": "AGRO TRGOVINA d.o.o. Racun 2026-00017 28.02.2026 Sunflower seed 20 kg 45.00 EUR LOT: LOT-2026-001",
                        "categoryHint": "seed",
                        "proposals": {
                            "productLabel": {
                                "valueText": "AGRO TRGOVINA d.o.o.",
                                "confidence": 0.7,
                                "provenance": {"lineIndices": [0]},
                            },
                            "packQuantity": {
                                "valueNum": 20.0,
                                "unit": "kg",
                                "confidence": 0.93,
                                "provenance": {"lineIndices": [3]},
                            },
                            "cropLabel": {
                                "valueText": "Sončnica",
                                "confidence": 0.68,
                                "provenance": {"lineIndices": [3]},
                            },
                            "lotCode": {
                                "valueText": "LOT-2026-001",
                                "confidence": 0.97,
                                "provenance": {"lineIndices": [4]},
                            },
                        },
                    },
                ],
                "referenceHints": {"cropTokens": ["sunflower"], "varietyTokens": [], "suggestedQueries": []},
                "persistenceTargets": ["inventory_receipt_import", "material_lot_candidate"],
                "model": {"provider": "stub", "model": "ocr-stub", "schemaVersion": "1"},
                "documentUri": "urn:document:receipt-mixed:1",
                "parseRunUri": "urn:parse-run:receipt-mixed:1",
            },
        }
    }
    captured_import_payload: dict[str, Any] = {}

    _install_universal_capture_session_store(
        monkeypatch,
        document_rows=document_rows,
        parse_runs=parse_runs,
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "create_partner_candidate",
        lambda payload: {"enabled": True, "persistedPartnerCandidates": 1},
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_inventory_receipt_import",
        lambda payload: captured_import_payload.update(payload)
        or {
            "enabled": True,
            "reason": "enabled",
            "persistedImports": 1,
            "persistedResources": len(payload.get("lineItems", [])),
            "persistedMaterialLots": len(payload.get("lineItems", [])),
            "persistedSeedLots": 1,
            "persistedLineItems": len(payload.get("lineItems", [])),
            "persistedMovements": len(payload.get("lineItems", [])),
            "persistedSeedSourcingExceptions": 0,
            "persistedEvidenceRecords": 0,
            "persistedEvents": 1,
        },
    )

    original_inventory_feature_enabled = main_module._inventory_phase1_feature_enabled

    def _inventory_feature_enabled(feature: str) -> bool:
        if feature == "inventoryReviewQueue":
            return False
        return original_inventory_feature_enabled(feature)

    monkeypatch.setattr(main_module, "_inventory_phase1_feature_enabled", _inventory_feature_enabled)

    create_response = client.post(
        "/v1/intake/captures",
        json={
            "farmUri": DEFAULT_FARM_URI,
            "modality": "photo",
            "source": "ios",
            "createdAt": "2026-03-12T09:00:00Z",
            "locale": "sl-SI",
            "documentUri": "urn:document:receipt-mixed:1",
            "parseRunUri": "urn:parse-run:receipt-mixed:1",
            "payloadRef": {"kind": "upload", "id": "upl-receipt-mixed-1", "mimeType": "image/jpeg"},
            "derivedRefs": {"barcodeValues": []},
            "hints": {"documentHint": "receipt"},
            "quality": {"adequate": True, "issues": []},
        },
    )
    assert create_response.status_code == 200

    analyze_response = client.post("/v1/intake/analyze", json={"sessionId": create_response.json()["sessionId"]})
    assert analyze_response.status_code == 200
    analyze_data = analyze_response.json()
    payload_draft = analyze_data["commitPlan"]["payloadDraft"]
    assert analyze_data["selectedRouteId"] == "receipt.invoice"
    assert len(payload_draft["lineItems"]) == 1
    assert payload_draft["lineItems"][0]["resourceLabel"] == "Sunflower seed EUR"
    assert payload_draft["lineItems"][0]["lotLabel"] == "LOT-2026-001"
    assert payload_draft["lineItems"][0]["cropLabel"] == "Sončnica"
    assert not any(item["resourceLabel"] == "AGRO TRGOVINA d.o.o." for item in payload_draft["lineItems"])

    commit_response = client.post(
        f"/v1/intake/sessions/{create_response.json()['sessionId']}/commit",
        json={},
    )
    assert commit_response.status_code == 200
    assert len(captured_import_payload["lineItems"]) == 1
    assert captured_import_payload["lineItems"][0]["resourceLabel"] == "Sunflower seed EUR"
    assert captured_import_payload["lineItems"][0]["lotLabel"] == "LOT-2026-001"
    assert captured_import_payload["receiptRef"] == "Racun 2026-00017"
