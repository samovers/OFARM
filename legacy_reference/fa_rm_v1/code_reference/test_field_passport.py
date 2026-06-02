from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from urllib.parse import quote

from fastapi.testclient import TestClient

import app.main as main_module
from app.field_passport import (
    _latest_item,
    build_field_passport,
    build_fact_snapshot,
    evaluate_rules,
    load_field_ops_rulepack,
    normalize_candidate_authorization_evaluation,
)
from app.main import app

DEFAULT_FARM_URI = "https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001"
DEFAULT_FIELD_URI = "https://data.farmco.si/farm-rm/v1/field/SI/FIELD-001"
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
    token = _encode_hs256_jwt(
        {
            "sub": "test-user",
            "iat": now,
            "exp": now + 3600,
            "farmUri": farm_uri,
        },
        secret=os.environ["FARM_RM_JWT_HS256_SECRET"],
    )
    return {"Authorization": f"Bearer {token}", "X-Farm-URI": farm_uri}


client = TestClient(app, headers=_auth_headers())


def _encoded_field_uri(field_uri: str = DEFAULT_FIELD_URI) -> str:
    return quote(field_uri, safe="")


def _enable_field_passport_features(monkeypatch) -> None:
    monkeypatch.setattr(type(main_module.PERSISTENCE), "enabled", property(lambda self: True))
    monkeypatch.setattr(type(main_module.PERSISTENCE), "reason", property(lambda self: "enabled"))
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_crop_context_as_of", lambda field_uri, **kwargs: None)
    monkeypatch.setenv("FIELD_PASSPORT_ENABLED", "1")
    monkeypatch.setenv("FIELD_PASSPORT_DAILY_EVALUATION_ENABLED", "1")
    monkeypatch.setenv("FIELD_PASSPORT_ACTION_EVALUATION_ENABLED", "1")
    monkeypatch.setenv("FIELD_WATER_STEWARDSHIP_ENABLED", "1")
    monkeypatch.setenv("FIELD_NITROGEN_APPLICATION_CHECK_ENABLED", "1")
    monkeypatch.setenv("FIELD_IRRIGATION_READINESS_ENABLED", "1")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_ENABLED", "1")
    monkeypatch.setenv("FIELD_BENCHMARK_CONTEXT_ENABLED", "1")
    monkeypatch.setenv("FIELD_CLIMATE_ADAPTATION_SUMMARY_ENABLED", "1")
    monkeypatch.setenv("FIELD_CLIMATE_INDICATOR_TRENDS_ENABLED", "1")
    monkeypatch.setenv("FIELD_CLIMATE_SUITABILITY_OUTLOOK_ENABLED", "1")
    monkeypatch.setenv("FIELD_EO_ANOMALY_ENABLED", "1")
    monkeypatch.setenv("FIELD_EXPLAINABILITY_SUMMARY_ENABLED", "1")
    monkeypatch.setenv("FIELD_PHENOLOGY_STATUS_ENABLED", "1")
    monkeypatch.setenv("FIELD_REGIONAL_COMPARISON_ENABLED", "1")
    monkeypatch.setenv("FIELD_SPRAY_WINDOW_ENABLED", "1")
    monkeypatch.setenv("FIELD_PLANT_HEALTH_RELEVANCE_ENABLED", "1")


def _assert_no_locked_climate_plan_states(payload: dict) -> None:
    assert payload["screenState"] != "locked"
    assert all(item["displayState"] != "locked" for item in payload.get("cards", []))


def test_latest_item_prefers_secondary_time_fields_when_primary_matches() -> None:
    chosen = _latest_item(
        [
            {
                "asOfDate": "2026-03-10",
                "observedAt": "2026-03-10T16:00:00Z",
                "createdAt": "2026-03-10T17:00:00Z",
                "sourceVersion": "older-created",
            },
            {
                "asOfDate": "2026-03-10",
                "observedAt": "2026-03-10T16:00:00Z",
                "createdAt": "2026-03-10T18:00:00Z",
                "sourceVersion": "newer-created",
            },
            {
                "asOfDate": "2026-03-10",
                "observedAt": "2026-03-10T15:00:00Z",
                "createdAt": "2026-03-10T19:00:00Z",
                "sourceVersion": "older-observed",
            },
        ],
        "asOfDate",
        "observedAt",
        "createdAt",
    )

    assert chosen is not None
    assert chosen["sourceVersion"] == "newer-created"


def test_build_field_passport_ignores_future_declaration_snapshot() -> None:
    passport = build_field_passport(
        as_of_date=main_module._parse_iso_date("2026-03-07"),
        field_row={
            "uri": DEFAULT_FIELD_URI,
            "farmUri": DEFAULT_FARM_URI,
            "label": "North parcel",
            "areaHa": 4.2,
        },
        authority_links=[],
        geometry_snapshots=[
            {
                "uri": "urn:field-geometry:current",
                "geometryRoleCode": "agricultural_parcel",
                "geometryRef": "urn:geometry:parcel:current",
                "capturedAt": "2026-03-01T08:00:00Z",
                "validFrom": "2026-01-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
            }
        ],
        declaration_snapshots=[
            {
                "uri": "urn:field-declaration:current",
                "cropInstanceUri": "urn:crop-instance:current",
                "declaredAt": "2026-03-02T09:00:00Z",
                "seasonCode": "2026",
                "productionStatus": "organic_certified",
                "declaredCropTypeUri": "urn:crop:wheat",
                "declaredCropLabel": "Wheat",
                "validFrom": "2026-03-02T09:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "complianceGeometryRef": "urn:geometry:parcel:current",
            },
            {
                "uri": "urn:field-declaration:future",
                "cropInstanceUri": "urn:crop-instance:future",
                "declaredAt": "2026-04-01T09:00:00Z",
                "seasonCode": "2026",
                "productionStatus": "organic_certified",
                "declaredCropTypeUri": "urn:crop:maize",
                "declaredCropLabel": "Maize",
                "validFrom": "2026-04-01T09:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "complianceGeometryRef": "urn:geometry:parcel:future",
            },
        ],
        latest_crop_instance=None,
        overlay_facts=[],
        condition_records=[],
        agrometeorological_observations=[],
        action_evaluations=[],
        recent_events=[],
        recent_evidence=[],
    )

    assert passport["cropContext"]["cropInstanceUri"] == "urn:crop-instance:current"
    assert passport["cropContext"]["cropTypeUri"] == "urn:crop:wheat"
    assert passport["complianceGeometryRef"] == "urn:geometry:parcel:current"


def test_build_field_passport_ignores_future_compliance_geometry_snapshot() -> None:
    passport = build_field_passport(
        as_of_date=main_module._parse_iso_date("2026-03-07"),
        field_row={
            "uri": DEFAULT_FIELD_URI,
            "farmUri": DEFAULT_FARM_URI,
            "label": "North parcel",
            "areaHa": 4.2,
        },
        authority_links=[],
        geometry_snapshots=[
            {
                "uri": "urn:field-geometry:current",
                "geometryRoleCode": "agricultural_parcel",
                "geometryRef": "urn:geometry:parcel:current",
                "capturedAt": "2026-03-01T08:00:00Z",
                "validFrom": "2026-01-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
            },
            {
                "uri": "urn:field-geometry:future",
                "geometryRoleCode": "compliance_scope",
                "geometryRef": "urn:geometry:parcel:future",
                "capturedAt": "2026-04-01T08:00:00Z",
                "validFrom": "2026-04-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "isComplianceGeometry": True,
            },
        ],
        declaration_snapshots=[],
        latest_crop_instance=None,
        overlay_facts=[],
        condition_records=[],
        agrometeorological_observations=[],
        action_evaluations=[],
        recent_events=[],
        recent_evidence=[],
    )

    assert passport["complianceGeometryRef"] == "urn:geometry:parcel:current"


def _stub_field_passport_context(monkeypatch) -> dict[str, list[dict]]:
    persisted_payloads: dict[str, list[dict]] = {
        "actionEvaluations": [],
        "authorityLinks": [],
        "benchmarkContextFacts": [],
        "climateAdaptationSignals": [],
        "climateProjectionFacts": [],
        "dailyConditions": [],
        "geometrySnapshots": [],
        "overlayFacts": [],
        "explainabilitySignals": [],
        "declarationSnapshots": [],
        "staleIssueSnapshots": [],
    }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_fields",
        lambda field_uris: [
            {
                "uri": DEFAULT_FIELD_URI,
                "farmUri": DEFAULT_FARM_URI,
                "label": "North parcel",
                "areaHa": 4.2,
                "createdAt": "2026-01-10T09:00:00Z",
            }
        ]
        if DEFAULT_FIELD_URI in field_uris
        else [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_authority_links",
        lambda field_uri: [
            {
                "uri": "urn:field-authority-link:1",
                "fieldUri": field_uri,
                "authoritySchemeCode": "gerk",
                "authorityRecordUri": "https://eprostor.gov.si/gerk/GERK-001",
                "authorityCode": "GERK-001",
                "authorityLabel": "GERK 001",
                "recordedAt": "2026-03-01T08:00:00Z",
                "validFrom": "2026-01-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "sourceVersion": "rkg-2026-03-01",
                "evidenceUri": "urn:evidence:authority-link:1",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_geometry_snapshots",
        lambda field_uri: [
            {
                "uri": "urn:field-geometry:1",
                "fieldUri": field_uri,
                "geometryRoleCode": "agricultural_parcel",
                "geometryRef": "urn:geometry:parcel:1",
                "capturedAt": "2026-03-01T08:00:00Z",
                "validFrom": "2026-01-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "areaHa": 4.15,
                "sourceVersion": "rkg-2026-03-01",
                "isComplianceGeometry": True,
                "evidenceUri": "urn:evidence:geometry:1",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_declaration_snapshots",
        lambda field_uri: [
            {
                "uri": "urn:field-declaration:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "declaredAt": "2026-03-02T09:00:00Z",
                "seasonCode": "2026",
                "declaredUseCode": "arable",
                "productionStatus": "organic_certified",
                "declaredCropLabel": "Wheat",
                "declaredCropTypeUri": "urn:crop:wheat",
                "declaredAreaHa": 4.1,
                "validFrom": "2026-03-02T09:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "complianceGeometryRef": "urn:geometry:parcel:1",
                "sourceVersion": "rkg-2026-03-02",
                "evidenceUri": "urn:evidence:declaration:1",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_species",
        lambda crop_species_uris: [
            {
                "uri": "urn:crop:wheat",
                "code": "wheat",
                "label": "Wheat",
                "vocabularyUri": "urn:ref:crop",
                "createdAt": "2026-01-01T00:00:00Z",
            }
        ]
        if "urn:crop:wheat" in crop_species_uris
        else [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_instances",
        lambda crop_instance_uris: [
            {
                "uri": "urn:crop-instance:1",
                "fieldUri": DEFAULT_FIELD_URI,
                "farmUri": DEFAULT_FARM_URI,
                "seasonCode": "2026",
                "cropTypeUri": "urn:crop:wheat",
                "productionStatus": "organic_certified",
                "certificationScopeUri": "urn:certification-scope:1",
                "cropVocabularyUri": "urn:ref:crop",
                "createdAt": "2026-01-15T12:00:00Z",
            }
        ]
        if "urn:crop-instance:1" in crop_instance_uris
        else [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_latest_crop_instance_for_field",
        lambda field_uri: {
            "uri": "urn:crop-instance:1",
            "fieldUri": field_uri,
            "farmUri": DEFAULT_FARM_URI,
            "seasonCode": "2026",
            "cropTypeUri": "urn:crop:wheat",
            "productionStatus": "organic_certified",
            "certificationScopeUri": "urn:certification-scope:1",
            "cropVocabularyUri": "urn:ref:crop",
            "createdAt": "2026-01-15T12:00:00Z",
        },
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_overlay_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-overlay:1",
                "fieldUri": field_uri,
                "overlayCode": "water_protection_zone",
                "severityCode": "info",
                "observedAt": "2026-03-03T06:00:00Z",
                "validFrom": "2026-01-01T00:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "sourceVersion": "overlay-2026-03-03",
                "evidenceUri": "urn:evidence:overlay:1",
                "attributesJson": {"zoneCode": "VVO-2"},
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_condition_daily_records",
        lambda field_uri: [
            {
                "uri": "urn:field-condition-daily:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOfDate": "2026-03-07",
                "observedAt": "2026-03-07T05:30:00Z",
                "sourceVersion": "daily-2026-03-07",
                "sprayWindowCode": "open",
                "nutrientSpreadingCode": "caution",
                "irrigationReadinessCode": "ready",
                "scoutPriorityCode": "medium",
                "weatherSummaryText": "Dry with low wind.",
                "eoAnomalyFlag": False,
                "riskSummaryText": "No blocking anomalies.",
                "evidenceUri": "urn:evidence:daily:1",
                "factsJson": {
                    "windSpeedMps": 2.1,
                    "precipitationMm24h": 9.8,
                    "referenceEtRecentMm": 3.2,
                    "referenceEtForecastMm": 5.4,
                    "slopePct": 7.5,
                    "pondingProneFlag": False,
                    "floodWatchFlag": False,
                    "eoCoveragePct": 82.0,
                    "eoChangeContext": "shifted",
                    "eoHeterogeneityStatus": "patchy",
                    "eoPhenologyProxyStatus": "behind",
                    "eoCloudOrNoiseStatus": "limited",
                },
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_agrometeorological_station_observations",
        lambda field_uri, **kwargs: [
            {
                "observationUri": "urn:agromet-observation:1",
                "stationUri": "urn:station:nova-gor",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "observedAt": "2026-03-07T05:30:00Z",
                "timeSupportStart": "2026-03-06T05:30:00Z",
                "timeSupportEnd": "2026-03-07T05:30:00Z",
                "airTemperatureC": 12.5,
                "relativeHumidityPct": 74.2,
                "rainfallMm": 0.0,
                "windSpeedMps": 2.1,
                "windDirectionDeg": 210.0,
                "qualityFlag": "estimated",
                "solarRadiationWm2": 180.0,
                "stationLatitudeDeg": 45.8958,
                "stationLongitudeDeg": 13.6289,
                "stationElevationM": 55.0,
                "providerRef": "urn:provider:arso:surface-observation-xml",
                "qcProcedureRef": "urn:procedure:realfarm-agromet-proxy:arso-surface-observation-xml:v1",
                "sensorMetadataRef": "urn:sensor-metadata:arso:surface-station:nova-gor",
                "notes": "Single-station proxy agrometeorological observation.",
                "createdAt": "2026-03-07T05:31:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_permanent_crop_component_snapshots",
        lambda field_uri, **kwargs: [
            {
                "uri": "urn:field-permanent-crop-component-snapshot:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "observedAt": "2026-02-10T13:33:26Z",
                "sourceVersion": "erkg-vineyard-last-meeting-2842476-2026-02-10",
                "authorityRecordUri": "urn:si:erkg:gerk:3544529",
                "geometryRef": "urn:si:erkg:last-meeting-geometry:2842476:3544529",
                "evidenceUri": "urn:evidence:realfarm-source-document:pdf",
                "componentOrder": 1,
                "plantCount": 250,
                "varietyUri": "urn:variety:barbera",
                "varietyLabel": "BARBERA",
                "rootstockLabel": None,
                "trainingFormLabel": 'VISEČI ŠPARONI "CASARSA"',
                "plantingYear": 1969,
                "intraRowSpacingM": 1.0,
                "interRowSpacingM": 2.8,
                "vineyardMid": "100459075",
                "sourceSectionLabel": "NA BREGU",
                "sourceAreaHa": 0.5101,
                "terraced": False,
                "grassed": False,
                "notes": "Authenticated vineyard component snapshot.",
                "createdAt": "2026-03-10T20:40:00Z",
            },
            {
                "uri": "urn:field-permanent-crop-component-snapshot:2",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "observedAt": "2026-02-10T13:33:26Z",
                "sourceVersion": "erkg-vineyard-last-meeting-2842476-2026-02-10",
                "authorityRecordUri": "urn:si:erkg:gerk:3544529",
                "geometryRef": "urn:si:erkg:last-meeting-geometry:2842476:3544529",
                "evidenceUri": "urn:evidence:realfarm-source-document:pdf",
                "componentOrder": 2,
                "plantCount": 900,
                "varietyUri": "urn:variety:laski-rizling",
                "varietyLabel": "LAŠKI RIZLING",
                "rootstockLabel": None,
                "trainingFormLabel": 'VISEČI ŠPARONI "CASARSA"',
                "plantingYear": 1980,
                "intraRowSpacingM": 1.0,
                "interRowSpacingM": 2.5,
                "vineyardMid": "100459075",
                "sourceSectionLabel": "NA BREGU",
                "sourceAreaHa": 0.5101,
                "terraced": False,
                "grassed": False,
                "notes": "Authenticated vineyard component snapshot.",
                "createdAt": "2026-03-10T20:40:00Z",
            },
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-projection-fact:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "c3s",
                "sourceId": "c3s-si-podravska-ssp245-tmean-2030s",
                "sourceVersion": "c3s-2026-03-09",
                "geographyScope": "statistical_region",
                "geographyCode": "SI-PODRAVSKA",
                "scenarioFamily": "ssp",
                "scenarioCode": "ssp245",
                "horizonScope": "mid_century",
                "periodStart": "2031-01-01",
                "periodEnd": "2040-12-31",
                "baselinePeriod": "1991-2020",
                "indicatorCode": "mean_temperature_c",
                "indicatorValue": 15.2,
                "unitCode": "celsius",
                "aggregationType": "seasonal_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:1"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "regional_proxy",
                "baselineValue": 13.6,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.8,
                "notes": "Regional climate projection context.",
                "createdAt": "2026-03-09T10:00:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_adaptation_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-adaptation-signal:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "warmingTrend",
                "priorityLevel": "high",
                "horizonScope": "mid_century",
                "confidenceStatus": "medium",
                "recommendedThemes": ["review_variety", "review_irrigation"],
                "reasonCodes": ["heat_pressure_increase", "rainfall_shift_risk"],
                "traceRefs": ["urn:trace:climate-adaptation:1"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:1"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "regional_proxy",
                "uncertaintyCodes": ["regional_proxy_only"],
                "notes": "Adaptation signal derived from regional scenario set.",
                "createdAt": "2026-03-09T10:05:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_benchmark_context_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-benchmark-context-fact:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-07",
                "sourceSystem": "surs",
                "sourceId": "surs-si-podravska-drought-2026-03",
                "sourceVersion": "surs-2026-03-07",
                "geographyScope": "statistical_region",
                "geographyCode": "SI-PODRAVSKA",
                "benchmarkDomain": "climate_stress_context",
                "metricCode": "drought_profile",
                "metricValue": 0.37,
                "unitCode": "annual_probability",
                "periodType": "annual",
                "periodStart": "2026-01-01",
                "periodEnd": "2026-12-31",
                "baselineType": "current",
                "freshnessStatus": "current",
                "confidenceStatus": "high",
                "evidenceRefs": ["urn:evidence:benchmark-context:1"],
                "traceRefs": ["urn:trace:benchmark-context:1"],
                "cropOrCommodityCode": "wheat",
                "notes": "Stored drought benchmark context.",
                "createdAt": "2026-03-07T09:00:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_explainability_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-explainability-signal:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-07",
                "signalType": "regionalStressContext",
                "signalLevel": "elevated",
                "localityStatus": "partly_regional",
                "confidenceStatus": "high",
                "recommendedNextStep": "inspect_local",
                "policyId": "si-benchmark-explainability-demo",
                "policyVersion": "1.0.0",
                "reasonCodes": ["drought_context:regional-watch"],
                "traceRefs": ["urn:trace:benchmark-explainability:1"],
                "evidenceRefs": ["urn:evidence:benchmark-explainability:1"],
                "notes": "Stored explainability signal.",
                "createdAt": "2026-03-07T09:05:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_remote_sensing_index_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [
            {
                "observationUri": "urn:remote-sensing-index:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "observedAt": "2026-03-07T08:00:00Z",
                "indexCode": "NDVI",
                "indexValue": 0.31,
                "acquisitionPlatformCode": "satellite",
                "sourceProductRef": "urn:source-product:eo:1",
                "geometryRef": "urn:geometry:parcel:1",
                "processingLevelCode": "L2A",
                "qualityFlag": "good",
                "cloudCoverPct": 18.0,
                "spatialResolutionM": 10.0,
                "confidenceScore": 0.84,
                "sensorBandConfig": "B08/B04",
                "createdAt": "2026-03-07T08:05:00Z",
            },
            {
                "observationUri": "urn:remote-sensing-index:0",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "observedAt": "2026-03-01T08:00:00Z",
                "indexCode": "NDVI",
                "indexValue": 0.58,
                "acquisitionPlatformCode": "satellite",
                "sourceProductRef": "urn:source-product:eo:0",
                "geometryRef": "urn:geometry:parcel:1",
                "processingLevelCode": "L2A",
                "qualityFlag": "good",
                "cloudCoverPct": 8.0,
                "spatialResolutionM": 10.0,
                "confidenceScore": 0.88,
                "sensorBandConfig": "B08/B04",
                "createdAt": "2026-03-01T08:05:00Z",
            },
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_scouting_signs_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [
            {
                "observationUri": "urn:crop-scouting:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "observedAt": "2026-03-06T09:00:00Z",
                "suspectedOrganismCode": "eppo:SEPTTR",
                "methodCode": "visual_severity_pct",
                "observerRef": "urn:party:scout:1",
                "bbchCode": "31",
                "symptomCodes": ["chlorosis"],
                "incidencePct": 18.0,
                "severityPct": 12.0,
                "severityClass": "medium",
                "samplesCount": 4,
                "plantsAssessedCount": 24,
                "diseaseCaseUri": "urn:disease-case:1",
                "evidenceRefs": ["urn:evidence:crop-scouting:1"],
                "qualityFlag": "good",
                "createdAt": "2026-03-06T09:05:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_pest_trap_count_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [
            {
                "observationUri": "urn:pest-trap-count:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "observedAt": "2026-03-06T07:30:00Z",
                "pestCode": "eppo:APHIDO",
                "trapTypeCode": "yellow_sticky",
                "trapCount": 14.0,
                "countUnit": "count_per_trap",
                "trapLocationRef": "north_edge",
                "observerRef": "urn:party:scout:1",
                "methodCode": "visual_count",
                "qualityFlag": "good",
                "createdAt": "2026-03-06T07:35:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_action_evaluations",
        lambda field_uri, limit=10: [
            {
                "evaluationUri": "urn:field-action-evaluation:existing",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "actionCode": "fertilizer_application",
                "asOfDate": "2026-03-05",
                "evaluatedAt": "2026-03-05T11:00:00Z",
                "outcomeCode": "allow",
                "reasonCodes": [],
                "ruleResults": [],
                "decisionContext": {"facts": {"daily": {"nutrientSpreadingCode": "open"}}},
                "rulePackUri": "https://data.ref/farm-rm/v1.7/rule-pack/SI/field-ops/2026/draft-v1",
                "rulePackCode": "SI_FIELD_OPS_2026_DRAFT_V1",
                "ruleExecutionTraceUri": "urn:rule-trace:existing",
                "evidenceUris": ["urn:evidence:daily:1"],
                "eventUri": "urn:event:existing",
                "eventType": "field_action_evaluation_recorded",
                "eventAt": "2026-03-05T11:00:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_leaf_wetness_duration_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [
            {
                "observationUri": "urn:leaf-wetness:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "fieldOrCanopyRef": "north_canopy",
                "intervalStart": "2026-03-07T00:00:00Z",
                "intervalEnd": "2026-03-07T06:00:00Z",
                "wetnessDurationHours": 9.5,
                "acquisitionMethod": "sensor",
                "qualityFlag": "good",
                "evidenceUris": ["urn:evidence:leaf-wetness:1"],
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_disease_case_assessment_evaluations",
        lambda field_uri, crop_instance_uri=None, assessed_on_or_before=None, limit=20: [
            {
                "assessmentUri": "urn:disease-assessment:1",
                "caseUri": "urn:case:phytosanitary:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "assessedAt": "2026-03-07T07:30:00Z",
                "assessmentType": "field_scouting",
                "pathogenCode": "eppo:SEPTTR",
                "caseStatus": "probable",
                "confidenceScore": 0.84,
                "evidenceUris": ["urn:evidence:disease-assessment:1"],
                "healthRiskClass": "high",
                "interventionRecommendationCode": "sample_and_test",
                "missingCriticalData": [],
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_irrigation_need_assessment_records",
        lambda field_uri, crop_instance_uri=None, assessed_on_or_before=None, limit=10: [
            {
                "irrigationNeedAssessmentUri": "urn:irrigation-need-assessment:1",
                "fieldUri": field_uri,
                "fieldOrZoneUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "assessedAt": "2026-03-07T06:30:00Z",
                "soilMoistureObservationRef": "urn:soil-moisture-observation:1",
                "weatherObservationRef": "urn:weather-observation:1",
                "cropStageObservationRef": "urn:crop-stage-observation:1",
                "stressRiskClass": "low",
                "recommendedAction": "monitor_no_irrigation",
                "thresholdCrossed": False,
                "confidenceScore": 0.81,
                "assessmentMethodCode": "checkbook_water_balance",
                "rulesetRef": "urn:ruleset:irrigation-need:1",
                "recordedAt": "2026-03-07T06:31:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_climate_hazard_profile_observations",
        lambda field_uri, crop_instance_uri=None, limit=10: [
            {
                "profileUri": "urn:climate-hazard:drought:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "hazardTypeCode": "drought",
                "hazardMetricCode": "spi",
                "frequencyKindCode": "annual_probability",
                "frequencyValue": 0.16,
                "dataSourceRef": "urn:data-source:drought:1",
                "methodRef": "urn:method:drought:1",
                "confidenceScore": 0.74,
                "recordedAt": "2026-03-06T10:00:00Z",
            },
            {
                "profileUri": "urn:climate-hazard:flood:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "hazardTypeCode": "flood",
                "hazardMetricCode": "extreme_rainfall_days",
                "frequencyKindCode": "annual_probability",
                "frequencyValue": 0.08,
                "dataSourceRef": "urn:data-source:flood:1",
                "methodRef": "urn:method:flood:1",
                "confidenceScore": 0.69,
                "recordedAt": "2026-03-06T10:00:00Z",
            },
            {
                "profileUri": "urn:climate-hazard:heatwave:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "hazardTypeCode": "heatwave",
                "hazardMetricCode": "heat_stress_days",
                "frequencyKindCode": "annual_probability",
                "frequencyValue": 0.22,
                "dataSourceRef": "urn:data-source:heat:1",
                "methodRef": "urn:method:heat:1",
                "confidenceLevelCode": "medium",
                "confidenceScore": 0.62,
                "recordedAt": "2026-03-06T10:00:00Z",
            },
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_pedoclimatic_profile_observations",
        lambda field_uri, limit=10: [
            {
                "profileUri": "urn:field-pedoclimatic:1",
                "farmUri": DEFAULT_FARM_URI,
                "fieldUri": field_uri,
                "regionCode": "SI-PODRAVSKA",
                "soilTextureClassCode": "loam",
                "drainageClassCode": "poorly_drained",
                "phMin": 6.2,
                "phMax": 7.1,
                "organicMatterPct": 3.4,
                "rainfallRegimeClassCode": "wet",
                "gddAnnual": 1450.0,
                "soilSourceRef": "urn:source:soil:1",
                "climateSourceRef": "urn:source:climate:1",
                "climateReferencePeriod": "1991-2020",
                "confidenceLevelCode": "medium",
                "confidenceScore": 0.66,
                "recordedAt": "2026-03-05T10:30:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_variety_risk_profile_evaluations",
        lambda field_uri, crop_instance_uri=None, limit=10: [
            {
                "assessmentUri": "urn:variety-risk-profile:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "varietyUri": "urn:variety:wheat:1",
                "pedoclimaticProfileUri": "urn:field-pedoclimatic:1",
                "assessedAt": "2026-03-06T11:00:00Z",
                "aggregateRiskClassCode": "high",
                "confidenceScore": 0.78,
                "methodRef": "urn:method:variety-risk:1",
                "expectedDiseasePressureRef": "urn:evidence:disease-pressure:1",
                "managementAssumptionsRef": "urn:evidence:management-assumption:1",
                "notes": "High risk under wet spring conditions.",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_adaptation_profile_observations",
        lambda variety_uris, farm_uri=None, limit=10: [
            {
                "profileUri": "urn:crop-adaptation-profile:1",
                "farmUri": farm_uri or DEFAULT_FARM_URI,
                "varietyUri": "urn:variety:wheat:1",
                "jurisdiction": "SI",
                "regionCode": "SI-PODRAVSKA",
                "recordedAt": "2026-03-04T09:00:00Z",
                "traitAssertions": [
                    {
                        "assertionUri": "urn:trait-assertion:rainfall:1",
                        "traitCode": "rainfall_regime_class",
                        "evidenceUri": "urn:evidence:trait:rainfall:1",
                        "valueText": "dry",
                    },
                    {
                        "assertionUri": "urn:trait-assertion:gdd-max:1",
                        "traitCode": "gdd_req_max",
                        "evidenceUri": "urn:evidence:trait:gdd-max:1",
                        "valueNumeric": 1300.0,
                        "unitCode": "gdd",
                    },
                ],
            }
        ]
        if "urn:variety:wheat:1" in variety_uris
        else [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_soil_moisture_profile_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [
            {
                "observationUri": "urn:soil-moisture-profile:1",
                "fieldUri": field_uri,
                "cropInstanceUri": crop_instance_uri or "urn:crop-instance:1",
                "observedAt": "2026-03-07T05:15:00Z",
                "depthFromCm": 0.0,
                "depthToCm": 30.0,
                "moistureValue": 31.0,
                "moistureUnit": "pct_vwc",
                "methodCode": "sensor_tdr",
                "sensorOrLabRef": "urn:sensor:soil:1",
                "qualityFlag": "good",
                "createdAt": "2026-03-07T05:16:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_evidence_records",
        lambda evidence_uris: [
            {
                "uri": uri,
                "evidenceType": "external_document",
                "evidenceRef": f"https://docs.example/{uri.rsplit(':', 1)[-1]}.pdf",
                "hashSha256": "abc123",
            }
            for uri in evidence_uris
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_latest_input_authorization_decision",
        lambda material_lot_uri, jurisdiction=None: {
            "inputAuthorizationUri": "urn:input-authorization:1",
            "materialLotUri": material_lot_uri,
            "jurisdiction": jurisdiction or "SI",
            "listRef": "SI-LIST-1",
            "listVersion": "2026-01",
            "decisionCode": "conditional",
            "decidedAt": "2026-03-06T08:00:00Z",
            "evidenceUri": "urn:evidence:input-authorization:1",
            "evidenceType": "external_document",
            "evidenceRef": "https://docs.example/input-authorization-1.pdf",
            "usedInExecutedOperationUris": [],
        },
    )

    def _persist_field_action_evaluation(payload: dict) -> dict:
        persisted_payloads["actionEvaluations"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedFieldActionEvaluations": 1,
            "persistedRuleExecutionTraces": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_action_evaluation",
        _persist_field_action_evaluation,
    )

    def _persist_field_authority_link(payload: dict) -> dict:
        persisted_payloads["authorityLinks"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedAuthorityLinks": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_authority_link",
        _persist_field_authority_link,
    )

    def _persist_field_geometry_snapshot(payload: dict) -> dict:
        persisted_payloads["geometrySnapshots"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedGeometrySnapshots": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_geometry_snapshot",
        _persist_field_geometry_snapshot,
    )

    def _persist_field_declaration_snapshot(payload: dict) -> dict:
        persisted_payloads["declarationSnapshots"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedDeclarationSnapshots": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_declaration_snapshot",
        _persist_field_declaration_snapshot,
    )

    def _persist_field_overlay_fact(payload: dict) -> dict:
        persisted_payloads["overlayFacts"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedOverlayFacts": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_overlay_fact",
        _persist_field_overlay_fact,
    )

    def _persist_field_condition_daily(payload: dict) -> dict:
        persisted_payloads["dailyConditions"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedDailyConditions": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_condition_daily",
        _persist_field_condition_daily,
    )

    def _persist_field_climate_projection_fact(payload: dict) -> dict:
        persisted_payloads["climateProjectionFacts"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedClimateProjectionFacts": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_climate_projection_fact",
        _persist_field_climate_projection_fact,
    )

    def _persist_field_climate_adaptation_signal(payload: dict) -> dict:
        persisted_payloads["climateAdaptationSignals"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedClimateAdaptationSignals": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_climate_adaptation_signal",
        _persist_field_climate_adaptation_signal,
    )

    def _persist_field_benchmark_context_fact(payload: dict) -> dict:
        persisted_payloads["benchmarkContextFacts"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedBenchmarkContextFacts": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_benchmark_context_fact",
        _persist_field_benchmark_context_fact,
    )

    def _persist_field_explainability_signal(payload: dict) -> dict:
        persisted_payloads["explainabilitySignals"].append(json.loads(json.dumps(payload)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedExplainabilitySignals": 1,
            "persistedEvents": 1,
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_explainability_signal",
        _persist_field_explainability_signal,
    )

    def _persist_field_passport_stale_issue_snapshots(payloads: list[dict]) -> dict:
        persisted_payloads["staleIssueSnapshots"].extend(json.loads(json.dumps(payloads)))
        return {
            "enabled": True,
            "reason": "enabled",
            "persistedFieldPassportStaleIssueSnapshots": len(payloads),
        }

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "persist_field_passport_stale_issue_snapshots",
        _persist_field_passport_stale_issue_snapshots,
    )
    return persisted_payloads


def test_capabilities_endpoint_includes_field_passport_flags(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    monkeypatch.setenv("FIELD_PASSPORT_MIN_CLIENT_VERSION", "ios-1.7.0")
    monkeypatch.setenv("FIELD_PASSPORT_DAILY_EVALUATION_MIN_CLIENT_VERSION", "ios-1.7.1")
    monkeypatch.setenv("FIELD_PASSPORT_ACTION_EVALUATION_MIN_CLIENT_VERSION", "ios-1.7.2")
    monkeypatch.setenv("FIELD_WATER_STEWARDSHIP_MIN_CLIENT_VERSION", "ios-1.7.3")
    monkeypatch.setenv("FIELD_NITROGEN_APPLICATION_CHECK_MIN_CLIENT_VERSION", "ios-1.7.4")
    monkeypatch.setenv("FIELD_IRRIGATION_READINESS_MIN_CLIENT_VERSION", "ios-1.7.5")
    monkeypatch.setenv("FIELD_BENCHMARK_CONTEXT_MIN_CLIENT_VERSION", "ios-1.7.6")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_FROST_TREND_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_HEAT_TREND_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_DRY_SPELL_TREND_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_IRRIGATION_VALUE_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_PLANNING_VARIETY_FIT_MIN_CLIENT_VERSION", "ios-1.7.17")
    monkeypatch.setenv("FIELD_CLIMATE_ADAPTATION_SUMMARY_MIN_CLIENT_VERSION", "ios-1.7.7")
    monkeypatch.setenv("FIELD_CLIMATE_INDICATOR_TRENDS_MIN_CLIENT_VERSION", "ios-1.7.8")
    monkeypatch.setenv("FIELD_CLIMATE_SUITABILITY_OUTLOOK_MIN_CLIENT_VERSION", "ios-1.7.9")
    monkeypatch.setenv("FIELD_EO_ANOMALY_MIN_CLIENT_VERSION", "ios-1.7.10")
    monkeypatch.setenv("FIELD_EXPLAINABILITY_SUMMARY_MIN_CLIENT_VERSION", "ios-1.7.11")
    monkeypatch.setenv("FIELD_PHENOLOGY_STATUS_MIN_CLIENT_VERSION", "ios-1.7.12")
    monkeypatch.setenv("FIELD_REGIONAL_COMPARISON_MIN_CLIENT_VERSION", "ios-1.7.13")
    monkeypatch.setenv("FIELD_SPRAY_WINDOW_MIN_CLIENT_VERSION", "ios-1.7.14")
    monkeypatch.setenv("FIELD_PLANT_HEALTH_RELEVANCE_MIN_CLIENT_VERSION", "ios-1.7.15")
    monkeypatch.setenv("FIELD_SCOUT_PRIORITY_QUEUE_MIN_CLIENT_VERSION", "ios-1.7.16")

    response = client.get("/v1/capabilities")

    assert response.status_code == 200
    data = response.json()
    assert data["features"]["fieldPassport"]["enabled"] is True
    assert data["features"]["fieldPassport"]["minClientVersion"] == "ios-1.7.0"
    assert data["features"]["fieldPassportDailyEvaluation"]["enabled"] is True
    assert data["features"]["fieldPassportDailyEvaluation"]["minClientVersion"] == "ios-1.7.1"
    assert data["features"]["fieldPassportActionEvaluation"]["enabled"] is True
    assert data["features"]["fieldPassportActionEvaluation"]["minClientVersion"] == "ios-1.7.2"
    assert data["features"]["fieldWaterStewardship"]["enabled"] is True
    assert data["features"]["fieldWaterStewardship"]["minClientVersion"] == "ios-1.7.3"
    assert data["features"]["fieldNitrogenApplicationCheck"]["enabled"] is True
    assert data["features"]["fieldNitrogenApplicationCheck"]["minClientVersion"] == "ios-1.7.4"
    assert data["features"]["fieldIrrigationReadiness"]["enabled"] is True
    assert data["features"]["fieldIrrigationReadiness"]["minClientVersion"] == "ios-1.7.5"
    assert data["features"]["fieldBenchmarkContext"]["enabled"] is True
    assert data["features"]["fieldBenchmarkContext"]["minClientVersion"] == "ios-1.7.6"
    assert data["features"]["fieldClimatePlanning"]["enabled"] is True
    assert data["features"]["fieldClimatePlanning"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimatePlanningFrostTrend"]["enabled"] is True
    assert data["features"]["fieldClimatePlanningFrostTrend"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimatePlanningHeatTrend"]["enabled"] is True
    assert data["features"]["fieldClimatePlanningHeatTrend"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimatePlanningDrySpellTrend"]["enabled"] is True
    assert data["features"]["fieldClimatePlanningDrySpellTrend"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimatePlanningIrrigationValue"]["enabled"] is True
    assert data["features"]["fieldClimatePlanningIrrigationValue"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimatePlanningVarietyFit"]["enabled"] is True
    assert data["features"]["fieldClimatePlanningVarietyFit"]["minClientVersion"] == "ios-1.7.17"
    assert data["features"]["fieldClimateAdaptationSummary"]["enabled"] is True
    assert data["features"]["fieldClimateAdaptationSummary"]["minClientVersion"] == "ios-1.7.7"
    assert data["features"]["fieldClimateIndicatorTrends"]["enabled"] is True
    assert data["features"]["fieldClimateIndicatorTrends"]["minClientVersion"] == "ios-1.7.8"
    assert data["features"]["fieldClimateSuitabilityOutlook"]["enabled"] is True
    assert data["features"]["fieldClimateSuitabilityOutlook"]["minClientVersion"] == "ios-1.7.9"
    assert data["features"]["fieldEoAnomaly"]["enabled"] is True
    assert data["features"]["fieldEoAnomaly"]["minClientVersion"] == "ios-1.7.10"
    assert data["features"]["fieldExplainabilitySummary"]["enabled"] is True
    assert data["features"]["fieldExplainabilitySummary"]["minClientVersion"] == "ios-1.7.11"
    assert data["features"]["fieldPhenologyStatus"]["enabled"] is True
    assert data["features"]["fieldPhenologyStatus"]["minClientVersion"] == "ios-1.7.12"
    assert data["features"]["fieldRegionalComparison"]["enabled"] is True
    assert data["features"]["fieldRegionalComparison"]["minClientVersion"] == "ios-1.7.13"
    assert data["features"]["fieldSprayWindow"]["enabled"] is True
    assert data["features"]["fieldSprayWindow"]["minClientVersion"] == "ios-1.7.14"
    assert data["features"]["fieldPlantHealthRelevance"]["enabled"] is True
    assert data["features"]["fieldPlantHealthRelevance"]["minClientVersion"] == "ios-1.7.15"
    assert data["features"]["fieldScoutPriorityQueue"]["enabled"] is True
    assert data["features"]["fieldScoutPriorityQueue"]["minClientVersion"] == "ios-1.7.16"


def test_get_field_passport_returns_parcel_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport", params={"asOfDate": "2026-03-07"})

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_compliance_passport.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["passport"]["identity"]["label"] == "North parcel"
    assert data["passport"]["complianceGeometryRef"] == "urn:geometry:parcel:1"
    assert data["passport"]["cropContext"]["seasonCode"] == "2026"
    assert data["passport"]["dailyState"]["sprayWindowCode"] == "open"
    assert data["passport"]["agrometeorologicalState"]["stationUri"] == "urn:station:nova-gor"
    assert data["passport"]["recentEvidence"]
    assert data["passport"]["freshness"]["staleFlags"] == []


def test_get_field_passport_uses_as_of_crop_context_projection_when_available(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_crop_context_as_of",
        lambda field_uri, **kwargs: {
            "cropInstanceUri": "urn:crop-instance:projection-1",
            "seasonCode": "2026",
            "cropTypeUri": "urn:crop:wheat",
            "productionStatus": "conventional",
            "warnings": [
                "crop_identity_conflicts_with_alternate_candidate",
                "production_status_selected_from_alternate_source",
            ],
            "cropIdentitySource": "declaration_snapshot",
            "cropIdentitySourceRef": "urn:field-declaration:projection-1",
            "cropIdentityAlternateSources": ["executed_operation_history"],
            "cropIdentityAlternateSourceRefs": ["urn:executed-operation:projection-1"],
            "cropIdentityAlternateCandidates": [
                {
                    "source": "executed_operation_history",
                    "sourceRef": "urn:executed-operation:projection-1",
                    "cropInstanceUri": "urn:crop-instance:history-1",
                    "seasonCode": "2026",
                    "cropTypeUri": "urn:crop:wheat",
                    "productionStatus": "organic_certified",
                    "effectiveFrom": "2026-03-05T08:00:00Z",
                    "effectiveTo": "2026-03-05T09:00:00Z",
                }
            ],
            "productionStatusSource": "executed_operation_history",
            "productionStatusSourceRef": "urn:executed-operation:projection-1",
            "productionStatusAlternateSources": ["latest_crop_instance"],
            "productionStatusAlternateSourceRefs": ["urn:crop-instance:projection-1"],
            "productionStatusAlternateCandidates": [
                {
                    "source": "latest_crop_instance",
                    "sourceRef": "urn:crop-instance:projection-1",
                    "cropInstanceUri": "urn:crop-instance:projection-1",
                    "seasonCode": "2026",
                    "cropTypeUri": "urn:crop:maize",
                    "productionStatus": "conventional",
                    "effectiveFrom": "2026-03-06T08:00:00Z",
                    "effectiveTo": None,
                }
            ],
            "declarationSnapshotUri": "urn:field-declaration:projection-1",
            "declaredCropLabel": "Projected Wheat",
            "declaredUseCode": "arable",
            "declaredAreaHa": 4.0,
            "effectiveFrom": "2026-03-02T09:00:00Z",
            "effectiveTo": "2026-12-31T23:59:59Z",
        },
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_latest_crop_instance_for_field",
        lambda field_uri: (_ for _ in ()).throw(AssertionError("should use as-of crop context projection")),
    )

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport", params={"asOfDate": "2026-03-07"})

    assert response.status_code == 200
    data = response.json()
    assert data["passport"]["cropContext"]["cropInstanceUri"] == "urn:crop-instance:projection-1"
    assert data["passport"]["cropContext"]["productionStatus"] == "conventional"
    assert data["passport"]["cropContext"]["declaredCropLabel"] == "Projected Wheat"
    assert data["passport"]["cropContext"]["declarationSnapshotUri"] == "urn:field-declaration:projection-1"
    assert data["passport"]["cropContext"]["warnings"] == [
        "crop_identity_conflicts_with_alternate_candidate",
        "production_status_selected_from_alternate_source",
    ]
    assert data["passport"]["cropContext"]["cropIdentitySource"] == "declaration_snapshot"
    assert data["passport"]["cropContext"]["cropIdentitySourceRef"] == "urn:field-declaration:projection-1"
    assert data["passport"]["cropContext"]["cropIdentityAlternateSources"] == ["executed_operation_history"]
    assert data["passport"]["cropContext"]["cropIdentityAlternateSourceRefs"] == [
        "urn:executed-operation:projection-1"
    ]
    assert data["passport"]["cropContext"]["cropIdentityAlternateCandidates"] == [
        {
            "source": "executed_operation_history",
            "sourceRef": "urn:executed-operation:projection-1",
            "cropInstanceUri": "urn:crop-instance:history-1",
            "seasonCode": "2026",
            "cropTypeUri": "urn:crop:wheat",
            "productionStatus": "organic_certified",
            "effectiveFrom": "2026-03-05T08:00:00Z",
            "effectiveTo": "2026-03-05T09:00:00Z",
        }
    ]
    assert data["passport"]["cropContext"]["productionStatusSource"] == "executed_operation_history"
    assert data["passport"]["cropContext"]["productionStatusSourceRef"] == "urn:executed-operation:projection-1"
    assert data["passport"]["cropContext"]["productionStatusAlternateSources"] == ["latest_crop_instance"]
    assert data["passport"]["cropContext"]["productionStatusAlternateSourceRefs"] == [
        "urn:crop-instance:projection-1"
    ]
    assert data["passport"]["cropContext"]["productionStatusAlternateCandidates"] == [
        {
            "source": "latest_crop_instance",
            "sourceRef": "urn:crop-instance:projection-1",
            "cropInstanceUri": "urn:crop-instance:projection-1",
            "seasonCode": "2026",
            "cropTypeUri": "urn:crop:maize",
            "productionStatus": "conventional",
            "effectiveFrom": "2026-03-06T08:00:00Z",
        }
    ]


def test_get_field_passport_keeps_crop_instance_status_when_declaration_is_unknown(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_declaration_snapshots",
        lambda field_uri: [
            {
                "uri": "urn:field-declaration:1",
                "fieldUri": field_uri,
                "declaredAt": "2026-03-02T09:00:00Z",
                "seasonCode": "2026",
                "declaredUseCode": "arable",
                "productionStatus": "unknown",
                "declaredCropLabel": "Wheat",
                "validFrom": "2026-03-02T09:00:00Z",
                "validTo": "2026-12-31T23:59:59Z",
                "complianceGeometryRef": "urn:geometry:parcel:1",
                "sourceVersion": "rkg-2026-03-02",
                "evidenceUri": "urn:evidence:declaration:1",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_latest_crop_instance_for_field",
        lambda field_uri: {
            "uri": "urn:crop-instance:1",
            "fieldUri": field_uri,
            "farmUri": DEFAULT_FARM_URI,
            "seasonCode": "2026",
            "cropTypeUri": "urn:crop:wheat",
            "productionStatus": "conventional",
            "certificationScopeUri": None,
            "createdAt": "2026-01-15T12:00:00Z",
        },
    )

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport", params={"asOfDate": "2026-03-07"})

    assert response.status_code == 200
    data = response.json()
    assert data["passport"]["cropContext"]["cropInstanceUri"] == "urn:crop-instance:1"
    assert data["passport"]["cropContext"]["productionStatus"] == "conventional"
    assert data["passport"]["cropContext"]["cropIdentitySource"] == "declaration_snapshot"
    assert data["passport"]["cropContext"]["cropIdentitySourceRef"] == "urn:field-declaration:1"
    assert data["passport"]["cropContext"]["productionStatusSource"] == "latest_crop_instance"
    assert data["passport"]["cropContext"]["productionStatusSourceRef"] == "urn:crop-instance:1"


def test_get_field_water_stewardship_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/water-stewardship",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_water_stewardship.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["waterBalanceSummary"]["soilWaterProxyStatus"] == "wet"
    assert data["waterBalanceSummary"]["waterDeficitProxyStatus"] == "low"
    assert data["waterBalanceSummary"]["droughtContextStatus"] == "regional-watch"
    assert any(item["actionType"] == "spreadNitrogen" and item["decision"] == "warn" for item in data["dailyDecisions"])
    assert any(item["actionType"] == "spreadManure" and item["decision"] == "block" for item in data["dailyDecisions"])
    assert "delay" in data["recommendedActions"]
    assert any(item["signalType"] == "manureTimingRisk" for item in data["topSignals"])


def test_post_field_water_stewardship_evaluate_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/water-stewardship/evaluate",
        json={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["dailyDecisions"]) == 4
    assert data["overlayContext"]["status"] == "waterProtection"


def test_post_field_nitrogen_application_evaluate_persists_warn_result(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/nitrogen-application/evaluate",
        json={
            "asOfDate": "2026-03-07",
            "actionType": "spreadNitrogen",
            "materialLotUri": "urn:material-lot:nitrogen:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_nitrogen_application_check.v0_8"
    assert data["decision"] == "warn"
    assert data["evaluation"]["actionCode"] == "fertilizer_application"
    assert data["persistence"]["persistedFieldActionEvaluations"] == 1
    assert any(item["code"] == "nitrate_timing_elevated" for item in data["warningFindings"])
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["phase3ActionType"] == "spreadNitrogen"
    assert persisted_payloads["actionEvaluations"][0]["materialLotUri"] == "urn:material-lot:nitrogen:1"


def test_post_field_nitrogen_application_evaluate_blocks_manure_on_wet_field(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/nitrogen-application/evaluate",
        json={
            "asOfDate": "2026-03-07",
            "actionType": "spreadManure",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "block"
    assert data["evaluation"]["actionCode"] == "soil_amendment_application"
    assert any(item["code"] == "manure_timing_high" for item in data["blockingFindings"])


def test_get_field_irrigation_readiness_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/irrigation-readiness",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_irrigation_readiness.v0_8"
    assert data["decision"] == "warn"
    assert data["urgencyStatus"] == "monitor"
    assert data["waterBalanceSummary"]["soilWaterProxyStatus"] == "wet"
    assert data["droughtContextSummary"]["status"] == "regional-watch"
    assert data["floodPondingSummary"]["status"] == "elevated"


def test_get_field_climate_plan_tab_returns_hidden_when_master_capability_off(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module,
        "_dev_capability_enabled",
        lambda capability, default=True: False if capability == "fieldClimatePlanning" else True,
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-plan-tab",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_climate_plan_tab.v0_8"
    assert data["screenState"] == "hidden"
    assert data["cards"] == []
    _assert_no_locked_climate_plan_states(data)


def test_get_field_climate_plan_tab_returns_live_cards(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-projection-fact:frost",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_1KM",
                "sourceId": "arso-1km-frost-days",
                "sourceVersion": "arso-1km-2026-03-09",
                "geographyScope": "field_context",
                "geographyCode": "GERK-001",
                "scenarioFamily": "ssp",
                "scenarioCode": "ssp245",
                "horizonScope": "mid_century",
                "periodStart": "2031-01-01",
                "periodEnd": "2040-12-31",
                "baselinePeriod": "1991-2020",
                "indicatorCode": "frost_days",
                "indicatorValue": 9.0,
                "unitCode": "days",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:frost"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:00:00Z",
            },
            {
                "uri": "urn:field-climate-projection-fact:heat",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_1KM",
                "sourceId": "arso-1km-heat-stress",
                "sourceVersion": "arso-1km-2026-03-09",
                "geographyScope": "field_context",
                "geographyCode": "GERK-001",
                "scenarioFamily": "ssp",
                "scenarioCode": "ssp245",
                "horizonScope": "mid_century",
                "periodStart": "2031-01-01",
                "periodEnd": "2040-12-31",
                "baselinePeriod": "1991-2020",
                "indicatorCode": "heat_stress_days",
                "indicatorValue": 14.0,
                "unitCode": "days",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:heat"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:00:00Z",
            },
            {
                "uri": "urn:field-climate-projection-fact:dry",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_1KM",
                "sourceId": "arso-1km-dry-spell",
                "sourceVersion": "arso-1km-2026-03-09",
                "geographyScope": "field_context",
                "geographyCode": "GERK-001",
                "scenarioFamily": "ssp",
                "scenarioCode": "ssp245",
                "horizonScope": "mid_century",
                "periodStart": "2031-01-01",
                "periodEnd": "2040-12-31",
                "baselinePeriod": "1991-2020",
                "indicatorCode": "consecutive_dry_days",
                "indicatorValue": 11.0,
                "unitCode": "days",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:dry"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:00:00Z",
            },
            {
                "uri": "urn:field-climate-projection-fact:variety",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_1KM",
                "sourceId": "arso-1km-temperature",
                "sourceVersion": "arso-1km-2026-03-09",
                "geographyScope": "field_context",
                "geographyCode": "GERK-001",
                "scenarioFamily": "ssp",
                "scenarioCode": "ssp245",
                "horizonScope": "mid_century",
                "periodStart": "2031-01-01",
                "periodEnd": "2040-12-31",
                "baselinePeriod": "1991-2020",
                "indicatorCode": "mean_temperature_c",
                "indicatorValue": 15.2,
                "unitCode": "celsius",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:temp"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:00:00Z",
            },
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_adaptation_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-adaptation-signal:frost",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "frostShiftRisk",
                "priorityLevel": "medium",
                "horizonScope": "mid_century",
                "confidenceStatus": "high",
                "recommendedThemes": ["review_frost_protection"],
                "reasonCodes": ["frost_window_shift"],
                "traceRefs": ["urn:trace:climate-adaptation:frost"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:frost"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:05:00Z",
            },
            {
                "uri": "urn:field-climate-adaptation-signal:heat",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "heatStressRisk",
                "priorityLevel": "high",
                "horizonScope": "mid_century",
                "confidenceStatus": "high",
                "recommendedThemes": ["review_variety"],
                "reasonCodes": ["heat_pressure_increase"],
                "traceRefs": ["urn:trace:climate-adaptation:heat"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:heat"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:05:00Z",
            },
            {
                "uri": "urn:field-climate-adaptation-signal:dry",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "waterDemandIncrease",
                "priorityLevel": "high",
                "horizonScope": "mid_century",
                "confidenceStatus": "high",
                "recommendedThemes": ["review_irrigation"],
                "reasonCodes": ["dry_spell_increase"],
                "traceRefs": ["urn:trace:climate-adaptation:dry"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:dry"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:05:00Z",
            },
            {
                "uri": "urn:field-climate-adaptation-signal:variety",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "cropSuitabilityPressure",
                "priorityLevel": "high",
                "horizonScope": "mid_century",
                "confidenceStatus": "high",
                "recommendedThemes": ["review_variety"],
                "reasonCodes": ["variety_pressure_high"],
                "traceRefs": ["urn:trace:climate-adaptation:variety"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:variety"],
                "geographyFitStatus": "field_matched",
                "createdAt": "2026-03-09T10:05:00Z",
            },
        ],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-plan-tab",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_climate_plan_tab.v0_8"
    assert data["screenState"] == "live"
    assert [item["cardType"] for item in data["cards"]] == [
        "frostTrend",
        "heatTrend",
        "drySpellTrend",
        "irrigationValue",
        "varietyFit",
    ]
    assert all(item["displayState"] == "live" for item in data["cards"])
    assert data["detailEndpoints"]["adaptationSummary"].endswith("/climate-adaptation-summary")
    assert data["detailEndpoints"]["irrigationReadiness"].endswith("/irrigation-readiness")
    _assert_no_locked_climate_plan_states(data)


def test_get_field_climate_plan_tab_returns_limited_when_context_is_partial(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-plan-tab",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["screenState"] == "limited"
    assert any(item["cardType"] == "heatTrend" for item in data["cards"])
    assert any(item["displayState"] == "limited" for item in data["cards"])
    assert "climate_geography_fit_partial" in data["evidenceGaps"]
    _assert_no_locked_climate_plan_states(data)


def test_get_field_climate_plan_tab_returns_insufficient_data_when_no_supported_cards(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_climate_projection_facts", lambda field_uri: [])
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_climate_adaptation_signals", lambda field_uri: [])
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_climate_hazard_profile_observations",
        lambda field_uri, crop_instance_uri=None, limit=20: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_pedoclimatic_profile_observations",
        lambda field_uri, limit=5: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_variety_risk_profile_evaluations",
        lambda field_uri, crop_instance_uri=None, limit=10: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_adaptation_profile_observations",
        lambda variety_uris, farm_uri=None, limit=10: [],
    )
    monkeypatch.setattr(
        main_module,
        "build_field_irrigation_readiness_projection",
        lambda **kwargs: {
            "decision": "unknown",
            "urgencyStatus": "unknown",
            "waterBalanceSummary": {
                "soilWaterProxyStatus": "unknown",
                "waterDeficitProxyStatus": "unknown",
                "droughtContextStatus": "unknown",
                "floodContextStatus": "unknown",
                "supportDatasetStatus": "none",
                "summary": "Water support is unavailable.",
            },
            "droughtContextSummary": {"status": "unknown", "summary": None},
            "floodPondingSummary": {"status": "unknown", "summary": None},
            "requiredEvidence": [],
            "traceRefs": [],
            "evidenceRefs": [],
        },
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-plan-tab",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["screenState"] == "insufficientData"
    assert data["cards"] == []
    _assert_no_locked_climate_plan_states(data)


def test_get_field_benchmark_context_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/benchmark-context",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_benchmark_context.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["activeCropInstanceUri"] == "urn:crop-instance:1"
    assert any(
        item["metricCode"] == "drought_profile"
        and item["status"] == "current"
        and item["metricValue"] == 0.37
        for item in data["keyIndicators"]
    )
    assert any(item["geographyScope"] == "field_authority" for item in data["geographyStrata"])
    assert any(item["geographyScope"] == "statistical_region" for item in data["geographyStrata"])
    assert data["freshnessSummary"]["status"] == "fresh"
    assert "urn:evidence:benchmark-context:1" in data["evidenceRefs"]


def test_get_field_benchmark_context_prefers_latest_period_for_duplicate_metric_codes(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_benchmark_context_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-benchmark-context-fact:latest",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2025-04-15",
                "sourceSystem": "SURS_SISTAT",
                "sourceId": "row-2024",
                "sourceVersion": "surs-sistat-1502410S-2025-04-15",
                "geographyScope": "statistical_region",
                "geographyCode": "11",
                "benchmarkDomain": "yield_context",
                "metricCode": "regional_yield_index",
                "metricValue": 0.979167,
                "unitCode": "index",
                "periodType": "annual",
                "periodStart": "2024-01-01",
                "periodEnd": "2024-12-31",
                "baselineType": "current",
                "freshnessStatus": "current",
                "confidenceStatus": "high",
                "evidenceRefs": ["urn:evidence:benchmark-context:2024"],
                "traceRefs": ["urn:trace:benchmark-context:2024"],
                "cropOrCommodityCode": "grapes",
                "notes": "Latest regional yield index.",
                "createdAt": "2026-03-11T10:54:18Z",
            },
            {
                "uri": "urn:field-benchmark-context-fact:older",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2025-04-15",
                "sourceSystem": "SURS_SISTAT",
                "sourceId": "row-2020",
                "sourceVersion": "surs-sistat-1502410S-2025-04-15",
                "geographyScope": "statistical_region",
                "geographyCode": "11",
                "benchmarkDomain": "yield_context",
                "metricCode": "regional_yield_index",
                "metricValue": 1.044118,
                "unitCode": "index",
                "periodType": "annual",
                "periodStart": "2020-01-01",
                "periodEnd": "2020-12-31",
                "baselineType": "current",
                "freshnessStatus": "current",
                "confidenceStatus": "high",
                "evidenceRefs": ["urn:evidence:benchmark-context:2020"],
                "traceRefs": ["urn:trace:benchmark-context:2020"],
                "cropOrCommodityCode": "grapes",
                "notes": "Older regional yield index.",
                "createdAt": "2026-03-11T10:54:17Z",
            },
        ],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/benchmark-context",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    yield_indicator = next(
        item
        for item in data["keyIndicators"]
        if item["domain"] == "yield_context" and item["metricCode"] == "regional_yield_index"
    )
    assert yield_indicator["metricValue"] == 0.979167
    assert yield_indicator["summary"] == "Latest regional yield index."


def test_get_field_explainability_summary_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/explainability-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_explainability_summary.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["recommendedNextStep"] == "inspect_local"
    assert data["localityConclusion"]["status"] == "partly_regional"
    assert data["confidenceSummary"]["status"] == "high"
    assert any(item["signalType"] == "regionalStressContext" for item in data["topSignals"])
    assert data["topSignals"][0]["policyId"] == "si-benchmark-explainability-demo"
    assert data["topSignals"][0]["policyVersion"] == "1.0.0"
    assert "urn:trace:benchmark-explainability:1" in data["traceRefs"]


def test_get_field_regional_comparison_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/regional-comparison",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_regional_comparison.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["normalizationPolicyVersion"] == "field-phase5-benchmark-v1"
    assert "Advisory comparison only" in data["evidencePolicy"]
    assert "climate_stress_context" in data["selectedDomains"]
    assert any(item["metricCode"] == "drought_profile" for item in data["comparisonRows"])
    assert any(item["metricCode"] == "flood_profile" for item in data["comparisonRows"])


def test_get_field_climate_adaptation_summary_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-adaptation-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_climate_adaptation_summary.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["planningContext"]["planningContextMode"] == "current_crop"
    assert data["horizonSummary"]["status"] == "resolved"
    assert data["horizonSummary"]["horizonsCovered"] == ["mid_century"]
    assert "review_irrigation" in data["recommendedThemes"]
    assert "climate_geography_fit_partial" in data["evidenceGaps"]
    assert any(item["signalType"] == "warmingTrend" for item in data["topSignals"])
    assert data["confidenceSummary"]["status"] == "medium"
    assert "urn:evidence:climate-adaptation:1" in data["evidenceRefs"]
    assert "urn:field-climate-adaptation-signal:1" in data["traceRefs"]


def test_get_field_climate_adaptation_summary_uses_permanent_crop_variety_when_risk_missing(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_variety_risk_profile_evaluations",
        lambda field_uri, crop_instance_uri=None, limit=10: [],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-adaptation-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["planningContext"]["planningContextMode"] == "current_crop"
    assert data["planningContext"]["varietyUri"] == "urn:variety:laski-rizling"
    assert "dominant permanent-crop composition" in data["planningContext"]["summary"]
    assert "urn:evidence:realfarm-source-document:pdf" in data["evidenceRefs"]


def test_get_field_climate_adaptation_summary_fetches_crop_adaptation_for_permanent_crop_variety(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    requested_variety_uris: list[str] = []

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_variety_risk_profile_evaluations",
        lambda field_uri, crop_instance_uri=None, limit=10: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_adaptation_signals",
        lambda field_uri: [],
    )

    def _fetch_crop_adaptation(variety_uris, farm_uri=None, limit=10):
        requested_variety_uris[:] = list(variety_uris)
        return [
            {
                "profileUri": "urn:crop-adaptation-profile:laski-rizling:1",
                "farmUri": farm_uri or DEFAULT_FARM_URI,
                "varietyUri": "urn:variety:laski-rizling",
                "jurisdiction": "SI",
                "regionCode": "SI-PODRAVSKA",
                "recordedAt": "2026-03-04T09:00:00Z",
                "traitAssertions": [
                    {
                        "assertionUri": "urn:trait-assertion:rainfall:laski:1",
                        "traitCode": "rainfall_regime_class",
                        "evidenceUri": "urn:evidence:trait:rainfall:laski:1",
                        "valueText": "dry",
                    },
                    {
                        "assertionUri": "urn:trait-assertion:gdd-max:laski:1",
                        "traitCode": "gdd_req_max",
                        "evidenceUri": "urn:evidence:trait:gdd-max:laski:1",
                        "valueNumeric": 1300.0,
                        "unitCode": "gdd",
                    },
                ],
            }
        ]

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_adaptation_profile_observations",
        _fetch_crop_adaptation,
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-adaptation-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert requested_variety_uris == ["urn:variety:laski-rizling"]
    assert data["planningContext"]["varietyUri"] == "urn:variety:laski-rizling"
    assert "dominant permanent-crop composition" in data["planningContext"]["summary"]
    assert any(item["signalType"] == "cropSuitabilityPressure" for item in data["topSignals"])


def test_get_field_climate_suitability_outlook_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-suitability-outlook",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_climate_suitability_outlook.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["cropOrVarietyContext"]["planningContextMode"] == "current_crop"
    assert data["horizonRows"][0]["horizonScope"] == "mid_century"
    assert data["suitabilityPressureSummary"]["status"] == "high"
    assert any(item["indicatorCode"] == "mean_temperature_c" for item in data["indicatorHighlights"])
    assert data["indicatorHighlights"][0]["aggregationType"] == "seasonal_mean"
    assert "review_variety" in data["horizonRows"][0]["recommendedThemes"]


def test_get_field_climate_indicator_trends_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-indicator-trends",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_climate_indicator_trends.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["scenarioSet"] == ["ssp245"]
    assert data["baselinePolicy"] == "1991-2020"
    assert data["geographyFitSummary"]["status"] == "regional_only"
    assert data["freshnessSummary"]["status"] == "fresh"
    assert any(item["indicatorCode"] == "mean_temperature_c" for item in data["indicatorRows"])
    assert data["indicatorRows"][0]["horizonScope"] == "mid_century"
    assert data["indicatorRows"][0]["scenarioCode"] == "ssp245"
    assert data["indicatorRows"][0]["aggregationType"] == "seasonal_mean"


def test_get_field_climate_indicator_trends_retains_distinct_seasonal_rows(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-projection-fact:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "arso_opsi",
                "sourceId": "arso-opsi-jja",
                "sourceVersion": "arso-opsi-12km-2025-08-01",
                "geographyScope": "custom",
                "geographyCode": "arso-cell-1",
                "scenarioFamily": "rcp",
                "scenarioCode": "rcp45",
                "horizonScope": "mid_century",
                "periodStart": "2041-01-01",
                "periodEnd": "2070-12-31",
                "baselinePeriod": "1981-2010",
                "indicatorCode": "max_temperature_c",
                "indicatorValue": 28.6,
                "unitCode": "celsius",
                "aggregationType": "seasonal_mean_jja",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:jja"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "baselineValue": 27.0,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.7,
                "notes": "Summer max temperature row.",
                "createdAt": "2026-03-09T10:05:00Z",
            },
            {
                "uri": "urn:field-climate-projection-fact:2",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "arso_opsi",
                "sourceId": "arso-opsi-djf",
                "sourceVersion": "arso-opsi-12km-2025-08-01",
                "geographyScope": "custom",
                "geographyCode": "arso-cell-1",
                "scenarioFamily": "rcp",
                "scenarioCode": "rcp45",
                "horizonScope": "mid_century",
                "periodStart": "2041-01-01",
                "periodEnd": "2070-12-31",
                "baselinePeriod": "1981-2010",
                "indicatorCode": "max_temperature_c",
                "indicatorValue": 9.4,
                "unitCode": "celsius",
                "aggregationType": "seasonal_mean_djf",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:djf"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "baselineValue": 8.2,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.4,
                "notes": "Winter max temperature row.",
                "createdAt": "2026-03-09T10:04:00Z",
            },
        ],
    )
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_climate_adaptation_signals", lambda field_uri: [])

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-indicator-trends",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["geographyFitSummary"]["status"] == "partial"
    assert len(data["indicatorRows"]) == 2
    assert {item["aggregationType"] for item in data["indicatorRows"]} == {"seasonal_mean_djf", "seasonal_mean_jja"}
    assert any("(seasonal_mean_jja)" in (item["summary"] or "") for item in data["indicatorRows"])


def test_get_field_climate_indicator_trends_treats_downscaled_fit_as_partial(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-projection-fact:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "sourceSystem": "arso_opsi",
                "sourceId": "arso-opsi-12km-cell-1-tas-2041-2070",
                "sourceVersion": "arso-opsi-12km-2025-08-01",
                "geographyScope": "custom",
                "geographyCode": "arso-opsi-12km-cell-13-8125-46-0625",
                "scenarioFamily": "rcp",
                "scenarioCode": "rcp45",
                "horizonScope": "mid_century",
                "periodStart": "2041-01-01",
                "periodEnd": "2070-12-31",
                "baselinePeriod": "1981-2010",
                "indicatorCode": "mean_temperature_c",
                "indicatorValue": 15.2,
                "unitCode": "celsius",
                "aggregationType": "seasonal_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:evidence:climate-projection:1"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "baselineValue": 13.6,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.8,
                "notes": "12 km downscaled climate projection context.",
                "createdAt": "2026-03-09T10:00:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_adaptation_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-adaptation-signal:1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-09",
                "planningContextMode": "current_crop",
                "signalType": "warmingTrend",
                "priorityLevel": "medium",
                "horizonScope": "mid_century",
                "confidenceStatus": "medium",
                "recommendedThemes": ["review_variety", "review_irrigation"],
                "reasonCodes": ["temperature_increase_detected"],
                "traceRefs": ["urn:trace:climate-adaptation:1"],
                "evidenceRefs": ["urn:evidence:climate-adaptation:1"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "uncertaintyCodes": ["downscaled_grid_cell"],
                "notes": "Adaptation signal derived from 12 km grid cell context.",
                "createdAt": "2026-03-09T10:05:00Z",
            }
        ],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-indicator-trends",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["geographyFitSummary"]["status"] == "partial"


def test_get_field_climate_adaptation_summary_prefers_1km_source_when_same_as_of(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_projection_facts",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-projection-fact:12km",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_12KM",
                "sourceId": "arso-12km-tas",
                "sourceVersion": "arso-opsi-12km-2025-08-01",
                "geographyScope": "custom",
                "geographyCode": "arso-opsi-12km-cell-13-8125-46-0625",
                "scenarioFamily": "rcp",
                "scenarioCode": "rcp45",
                "horizonScope": "mid_century",
                "periodStart": "2041-01-01",
                "periodEnd": "2070-12-31",
                "baselinePeriod": "1981-2010",
                "indicatorCode": "mean_temperature_c",
                "indicatorValue": 15.2,
                "unitCode": "celsius",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:zip-member:12km/RCP45/tas/tas_odklon_12km_ARSO_rcp45_2041_2070_leto.nc"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "baselineValue": 13.6,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.8,
                "notes": "12 km projection context.",
                "createdAt": "2026-03-10T10:05:00Z",
            },
            {
                "uri": "urn:field-climate-projection-fact:1km",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "planningContextMode": "current_crop",
                "sourceSystem": "ARSO_OPSI_CLIMATE_PROJECTIONS_1KM",
                "sourceId": "arso-1km-tas",
                "sourceVersion": "arso-opsi-1km-2025-08-01",
                "geographyScope": "custom",
                "geographyCode": "arso-opsi-1km-cell-406650-0000-103350-0000",
                "scenarioFamily": "rcp",
                "scenarioCode": "rcp45",
                "horizonScope": "mid_century",
                "periodStart": "2041-01-01",
                "periodEnd": "2070-12-31",
                "baselinePeriod": "1981-2010",
                "indicatorCode": "mean_temperature_c",
                "indicatorValue": 14.9,
                "unitCode": "celsius",
                "aggregationType": "annual_mean",
                "uncertaintyClass": "medium",
                "freshnessStatus": "current",
                "evidenceRefs": ["urn:zip-member:1km/RCP45/tas/tas_odklon_1km_ARSO_rcp45_2041_2070_leto.nc"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "baselineValue": 13.8,
                "baselineUnitCode": "celsius",
                "scenarioSpreadValue": 0.6,
                "notes": "1 km projection context.",
                "createdAt": "2026-03-10T10:00:00Z",
            },
        ],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_climate_adaptation_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-climate-adaptation-signal:12km",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "planningContextMode": "current_crop",
                "signalType": "warmingTrend",
                "priorityLevel": "high",
                "horizonScope": "mid_century",
                "confidenceStatus": "medium",
                "recommendedThemes": ["review_irrigation"],
                "reasonCodes": ["temperature_increase_detected"],
                "traceRefs": ["urn:trace:climate-adaptation:12km"],
                "evidenceRefs": ["urn:zip-member:12km/RCP45/tas/tas_odklon_12km_ARSO_rcp45_2041_2070_leto.nc"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "uncertaintyCodes": ["downscaled_grid_cell"],
                "notes": "12 km adaptation signal.",
                "createdAt": "2026-03-10T10:06:00Z",
            },
            {
                "uri": "urn:field-climate-adaptation-signal:1km",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "planningContextMode": "current_crop",
                "signalType": "warmingTrend",
                "priorityLevel": "medium",
                "horizonScope": "mid_century",
                "confidenceStatus": "medium",
                "recommendedThemes": ["review_variety"],
                "reasonCodes": ["temperature_increase_detected"],
                "traceRefs": ["urn:trace:climate-adaptation:1km"],
                "evidenceRefs": ["urn:zip-member:1km/RCP45/tas/tas_odklon_1km_ARSO_rcp45_2041_2070_leto.nc"],
                "cropOrVarietyCode": "wheat",
                "geographyFitStatus": "downscaled",
                "uncertaintyCodes": ["downscaled_grid_cell"],
                "notes": "1 km adaptation signal.",
                "createdAt": "2026-03-10T10:00:00Z",
            },
        ],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-adaptation-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert any(item["traceRefs"] == ["urn:trace:climate-adaptation:1km", "urn:field-climate-adaptation-signal:1km"] for item in data["topSignals"])
    assert "urn:zip-member:1km/RCP45/tas/tas_odklon_1km_ARSO_rcp45_2041_2070_leto.nc" in data["evidenceRefs"]
    assert "urn:zip-member:12km/RCP45/tas/tas_odklon_12km_ARSO_rcp45_2041_2070_leto.nc" not in data["evidenceRefs"]


def test_get_field_climate_adaptation_summary_falls_back_without_stored_facts(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_climate_projection_facts", lambda field_uri: [])
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_climate_adaptation_signals", lambda field_uri: [])

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/climate-adaptation-summary",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["horizonSummary"]["status"] == "cross_horizon_only"
    assert "scenario_horizon_context" in data["evidenceGaps"]
    assert any(item["signalType"] == "waterDemandIncrease" for item in data["topSignals"])
    assert any(item["signalType"] == "cropSuitabilityPressure" for item in data["topSignals"])
    assert data["confidenceSummary"]["status"] == "low"


def test_get_field_eo_anomaly_returns_triage_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/eo-anomaly",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_eo_anomaly_triage.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["activeCropInstanceUri"] == "urn:crop-instance:1"
    assert data["observationSummary"]["sensorSet"] == "optical"
    assert data["observationSummary"]["qualityStatus"] == "usable"
    assert data["phenologySummary"]["status"] == "behind"
    assert data["scoutRecommendation"] == "inspect_now"
    assert any(item["signalType"] == "growthLag" for item in data["topSignals"])
    assert any(item["signalType"] == "standingWaterSuspicion" for item in data["topSignals"])
    assert "urn:evidence:crop-scouting:1" in data["evidenceRefs"]
    assert "urn:remote-sensing-index:1" in data["traceRefs"]


def test_get_field_eo_anomaly_reacquires_when_observations_are_missing(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_remote_sensing_index_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [],
    )
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_scouting_signs_observations",
        lambda field_uri, crop_instance_uri=None, observed_on_or_before=None, limit=10: [],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/eo-anomaly",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["scoutRecommendation"] == "reacquire"
    assert data["requiredEvidence"] == ["remote_sensing_index_observation"]
    assert data["topSignals"][0]["signalType"] == "dataQualityGap"
    assert data["topSignals"][0]["recommendedNextStep"] == "reacquire"


def test_get_field_phenology_status_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/phenology-status",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_phenology_status.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["stageStatus"] == "behind"
    assert data["confidenceStatus"] == "high"
    assert data["baselineSummary"]["status"] == "behind"
    assert any(item["signalType"] == "growthLag" for item in data["contributingSignals"])
    assert data["evidenceGaps"] == []
    assert "urn:evidence:crop-scouting:1" in data["evidenceRefs"]


def test_get_farm_scout_priority_queue_returns_ranked_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    monkeypatch.setenv("FIELD_SCOUT_PRIORITY_QUEUE_ENABLED", "1")
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_fields_for_farm",
        lambda farm_uri: [
            {
                "uri": "https://data.farmco.si/farm-rm/v1/field/SI/FIELD-001",
                "farmUri": DEFAULT_FARM_URI,
                "label": "North parcel",
                "areaHa": 4.2,
                "createdAt": "2026-01-10T09:00:00Z",
            },
            {
                "uri": "https://data.farmco.si/farm-rm/v1/field/SI/FIELD-002",
                "farmUri": DEFAULT_FARM_URI,
                "label": "South parcel",
                "areaHa": 2.7,
                "createdAt": "2026-01-11T09:00:00Z",
            },
        ],
    )

    def _resolve_phase4_context(request_http, *, field_uri, as_of_date):
        if field_uri.endswith("FIELD-001"):
            return (
                {
                    "uri": field_uri,
                    "farmUri": DEFAULT_FARM_URI,
                    "label": "North parcel",
                    "areaHa": 4.2,
                },
                {},
                {
                    "fieldUri": field_uri,
                    "activeCropInstanceUri": "urn:crop-instance:1",
                    "scoutRecommendation": "inspect_now",
                    "confidenceStatus": "high",
                    "stageStatus": "behind",
                    "dataQualitySummary": {"status": "usable", "summary": "Clear EO support."},
                    "topSignals": [
                        {
                            "signalType": "growthLag",
                            "signalLevel": "high",
                            "scoutPriority": "urgent",
                            "reasonCodes": ["phenology_proxy:behind"],
                            "traceRefs": ["urn:trace:field-1"],
                            "evidenceRefs": ["urn:evidence:field-1"],
                        }
                    ],
                    "requiredEvidence": [],
                    "traceRefs": ["urn:trace:field-1"],
                    "evidenceRefs": ["urn:evidence:field-1"],
                },
            )
        return (
            {
                "uri": field_uri,
                "farmUri": DEFAULT_FARM_URI,
                "label": "South parcel",
                "areaHa": 2.7,
            },
            {},
            {
                "fieldUri": field_uri,
                "activeCropInstanceUri": "urn:crop-instance:2",
                "scoutRecommendation": "reacquire",
                "confidenceStatus": "low",
                "stageStatus": "unknown",
                "dataQualitySummary": {"status": "poor", "summary": "EO missing or unusable."},
                "topSignals": [
                    {
                        "signalType": "dataQualityGap",
                        "signalLevel": "high",
                        "scoutPriority": "urgent",
                        "reasonCodes": ["eo_observation_missing"],
                        "traceRefs": ["urn:trace:field-2"],
                        "evidenceRefs": [],
                    }
                ],
                "requiredEvidence": ["remote_sensing_index_observation"],
                "traceRefs": ["urn:trace:field-2"],
                "evidenceRefs": [],
            },
        )

    monkeypatch.setattr(main_module, "_resolve_field_phase4_context", _resolve_phase4_context)

    response = client.get(
        f"/v1/farms/{quote(DEFAULT_FARM_URI, safe='')}/scout-priority-queue",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_scout_priority_queue.v0_8"
    assert data["farmUri"] == DEFAULT_FARM_URI
    assert data["rankingPolicyVersion"] == "si-field-eo-scout-queue-v1"
    assert data["queueItems"][0]["fieldUri"].endswith("FIELD-002")
    assert data["queueItems"][0]["scoutRecommendation"] == "reacquire"
    assert data["queueItems"][0]["requiredEvidence"] == ["remote_sensing_index_observation"]
    assert data["queueItems"][1]["fieldUri"].endswith("FIELD-001")
    assert data["queueItems"][1]["scoutRecommendation"] == "inspect_now"
    assert data["queueItems"][1]["topSignalTypes"] == ["growthLag"]
    assert "urn:trace:field-1" in data["traceRefs"]
    assert "urn:evidence:field-1" in data["evidenceRefs"]


def test_get_field_spray_window_returns_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/spray-window",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_spray_window.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["activeCropInstanceUri"] == "urn:crop-instance:1"
    assert data["decision"] == "warn"
    assert data["weatherMetrics"]["windSpeedMps"] == 2.1
    assert data["weatherMetrics"]["relativeHumidityPct"] == 74.2
    assert data["weatherMetrics"]["leafWetnessHours"] == 9.5
    assert any(item["code"] == "leaf_wetness_elevated" for item in data["warningFindings"])
    assert "urn:agromet-observation:1" in data["traceRefs"]
    assert "urn:evidence:leaf-wetness:1" in data["evidenceRefs"]


def test_get_field_plant_health_relevance_returns_signal_projection(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/plant-health/relevance",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["templateId"] == "farm.tpl.si.field_plant_health_relevance.v0_8"
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["summaryStatus"] == "high"
    assert data["signals"][0]["hazardCode"] == "eppo:SEPTTR"
    assert data["signals"][0]["weatherSignalStatus"] == "supporting"
    assert data["signals"][0]["scoutingEvidenceStatus"] == "present"
    assert data["signals"][0]["recommendedNextStep"] == "scout"
    assert "official_plant_health_advisory_fact" in data["requiredEvidence"]
    assert "urn:evidence:disease-assessment:1" in data["evidenceRefs"]


def test_get_field_passport_accepts_header_only_farm_scope_when_auth_disabled(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setenv("FARM_RM_DISABLE_AUTH", "1")

    with TestClient(app, headers={"X-Farm-URI": DEFAULT_FARM_URI}) as local_client:
        response = local_client.get(
            f"/v1/fields/{_encoded_field_uri()}/passport",
            params={"asOfDate": "2026-03-07"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["passport"]["identity"]["label"] == "North parcel"


def test_list_field_passport_declaration_snapshots_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/declaration-snapshots")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["seasonCode"] == "2026"
    assert data["items"][0]["declaredCropTypeUri"] == "urn:crop:wheat"


def test_list_field_passport_overlay_facts_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/overlay-facts")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["overlayCode"] == "water_protection_zone"
    assert data["items"][0]["severityCode"] == "info"


def test_list_field_passport_daily_conditions_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/daily-conditions")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["asOfDate"] == "2026-03-07"
    assert data["items"][0]["sprayWindowCode"] == "open"


def test_list_field_passport_agrometeorological_observations_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/agrometeorological-observations")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["stationUri"] == "urn:station:nova-gor"
    assert data["items"][0]["relativeHumidityPct"] == 74.2


def test_list_field_passport_permanent_crop_component_snapshots_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/permanent-crop-component-snapshots")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 2
    assert data["items"][0]["varietyLabel"] == "BARBERA"
    assert data["items"][1]["plantCount"] == 900


def test_get_field_permanent_crop_composition_returns_summary(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/permanent-crop-composition",
        params={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["status"] == "available"
    assert data["activeCropInstanceUri"] == "urn:crop-instance:1"
    assert data["vineyardMid"] == "100459075"
    assert data["componentCount"] == 2
    assert data["varietyCount"] == 2
    assert data["totalPlantCount"] == 1150
    assert data["components"][0]["plantSharePct"] == 21.74
    assert data["components"][1]["varietyLabel"] == "LAŠKI RIZLING"
    assert "urn:evidence:realfarm-source-document:pdf" in data["evidenceRefs"]


def test_list_field_passport_climate_projection_facts_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/climate-projection-facts")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["indicatorCode"] == "mean_temperature_c"
    assert data["items"][0]["scenarioCode"] == "ssp245"


def test_list_field_passport_climate_adaptation_signals_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/climate-adaptation-signals")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["signalType"] == "warmingTrend"
    assert data["items"][0]["recommendedThemes"] == ["review_variety", "review_irrigation"]


def test_list_field_passport_benchmark_context_facts_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/benchmark-context-facts")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["benchmarkDomain"] == "climate_stress_context"
    assert data["items"][0]["metricCode"] == "drought_profile"


def test_list_field_passport_explainability_signals_returns_history(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport/explainability-signals")

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert len(data["items"]) == 1
    assert data["items"][0]["signalType"] == "regionalStressContext"
    assert data["items"][0]["policyId"] == "si-benchmark-explainability-demo"
    assert data["items"][0]["recommendedNextStep"] == "inspect_local"


def test_create_field_passport_authority_link_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/authority-links",
        json={
            "authoritySchemeCode": "gerk",
            "authorityRecordUri": "https://eprostor.gov.si/gerk/GERK-NEW",
            "authorityCode": "GERK-NEW",
            "authorityLabel": "GERK New",
            "recordedAt": "2026-03-08T08:00:00Z",
            "validFrom": "2026-03-08T08:00:00Z",
            "sourceVersion": "rkg-2026-03-08",
            "evidenceUri": "urn:evidence:authority-link:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["authoritySchemeCode"] == "gerk"
    assert data["persistence"]["persistedAuthorityLinks"] == 1
    assert persisted_payloads["authorityLinks"][0]["sourceVersion"] == "rkg-2026-03-08"
    assert persisted_payloads["authorityLinks"][0]["evidenceUri"] == "urn:evidence:authority-link:1"


def test_create_field_passport_geometry_snapshot_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/geometry-snapshots",
        json={
            "geometryRoleCode": "compliance_scope",
            "geometryRef": "urn:geometry:new",
            "authorityLinkUri": "urn:field-authority-link:1",
            "capturedAt": "2026-03-08T09:00:00Z",
            "areaHa": 4.2,
            "sourceVersion": "geom-2026-03-08",
            "isComplianceGeometry": True,
            "evidenceUri": "urn:evidence:geometry:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["geometryRoleCode"] == "compliance_scope"
    assert data["persistence"]["persistedGeometrySnapshots"] == 1
    assert persisted_payloads["geometrySnapshots"][0]["authorityLinkUri"] == "urn:field-authority-link:1"
    assert persisted_payloads["geometrySnapshots"][0]["isComplianceGeometry"] is True


def test_create_field_passport_declaration_snapshot_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/declaration-snapshots",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "authorityLinkUri": "urn:field-authority-link:1",
            "geometrySnapshotUri": "urn:field-geometry:1",
            "declaredAt": "2026-03-08T10:00:00Z",
            "seasonCode": "2026",
            "declaredUseCode": "arable",
            "productionStatus": "organic_certified",
            "declaredCropLabel": "Wheat",
            "declaredCropTypeUri": "urn:crop:wheat",
            "declaredAreaHa": 4.1,
            "complianceGeometryRef": "urn:geometry:parcel:1",
            "sourceVersion": "decl-2026-03-08",
            "evidenceUri": "urn:evidence:declaration:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["cropInstanceUri"] == "urn:crop-instance:1"
    assert data["persistence"]["persistedDeclarationSnapshots"] == 1
    assert persisted_payloads["declarationSnapshots"][0]["geometrySnapshotUri"] == "urn:field-geometry:1"
    assert persisted_payloads["declarationSnapshots"][0]["declaredCropTypeUri"] == "urn:crop:wheat"


def test_create_field_passport_declaration_snapshot_rejects_cross_field_crop_instance(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_instances",
        lambda crop_instance_uris: [
            {
                "uri": "urn:crop-instance:foreign",
                "fieldUri": "urn:field:foreign",
                "farmUri": DEFAULT_FARM_URI,
                "seasonCode": "2026",
                "cropTypeUri": "urn:crop:wheat",
                "productionStatus": "organic_certified",
                "certificationScopeUri": "urn:certification-scope:1",
                "cropVocabularyUri": "urn:ref:crop",
                "createdAt": "2026-01-15T12:00:00Z",
            }
        ]
        if "urn:crop-instance:foreign" in crop_instance_uris
        else [],
    )

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/declaration-snapshots",
        json={
            "cropInstanceUri": "urn:crop-instance:foreign",
            "declaredAt": "2026-03-08T10:00:00Z",
            "seasonCode": "2026",
            "declaredUseCode": "arable",
            "productionStatus": "organic_certified",
            "sourceVersion": "decl-2026-03-08",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_crop_instance_field_mismatch"


def test_create_field_passport_declaration_snapshot_accepts_matching_crop_instance_crop_type_without_species_row(
    monkeypatch,
) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_crop_species", lambda crop_species_uris: [])

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/declaration-snapshots",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "authorityLinkUri": "urn:field-authority-link:1",
            "geometrySnapshotUri": "urn:field-geometry:1",
            "declaredAt": "2026-03-08T10:00:00Z",
            "seasonCode": "2026",
            "declaredUseCode": "arable",
            "productionStatus": "organic_certified",
            "declaredCropLabel": "Wheat",
            "declaredCropTypeUri": "urn:crop:wheat",
            "declaredAreaHa": 4.1,
            "complianceGeometryRef": "urn:geometry:parcel:1",
            "sourceVersion": "decl-2026-03-08",
            "evidenceUri": "urn:evidence:declaration:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["cropInstanceUri"] == "urn:crop-instance:1"
    assert data["declaredCropTypeUri"] == "urn:crop:wheat"
    assert data["persistence"]["persistedDeclarationSnapshots"] == 1
    assert persisted_payloads["declarationSnapshots"][0]["declaredCropTypeUri"] == "urn:crop:wheat"


def test_create_field_passport_declaration_snapshot_without_crop_instance_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/declaration-snapshots",
        json={
            "authorityLinkUri": "urn:field-authority-link:1",
            "geometrySnapshotUri": "urn:field-geometry:1",
            "declaredAt": "2026-03-08T10:00:00Z",
            "seasonCode": "2026",
            "declaredUseCode": "arable",
            "productionStatus": "organic_certified",
            "declaredCropLabel": "Wheat",
            "declaredCropTypeUri": "urn:crop:wheat",
            "declaredAreaHa": 4.1,
            "complianceGeometryRef": "urn:geometry:parcel:1",
            "sourceVersion": "decl-2026-03-08",
            "evidenceUri": "urn:evidence:declaration:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "cropInstanceUri" not in data
    assert data["declaredCropTypeUri"] == "urn:crop:wheat"
    assert data["persistence"]["persistedDeclarationSnapshots"] == 1
    assert persisted_payloads["declarationSnapshots"][0]["declaredCropTypeUri"] == "urn:crop:wheat"


def test_create_field_passport_overlay_fact_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/overlay-facts",
        json={
            "geometrySnapshotUri": "urn:field-geometry:1",
            "authorityLinkUri": "urn:field-authority-link:1",
            "geometryRef": "urn:geometry:parcel:1",
            "overlayCode": "spray_restriction",
            "severityCode": "warn",
            "regimeCode": "si:demo",
            "observedAt": "2026-03-08T11:00:00Z",
            "coveragePct": 12.5,
            "validFrom": "2026-03-08T11:00:00Z",
            "sourceVersion": "overlay-2026-03-08",
            "evidenceUri": "urn:evidence:overlay:1",
            "attributesJson": {"zoneCode": "SPRAY-WARN"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["overlayCode"] == "spray_restriction"
    assert data["persistence"]["persistedOverlayFacts"] == 1
    assert persisted_payloads["overlayFacts"][0]["severityCode"] == "warn"
    assert persisted_payloads["overlayFacts"][0]["attributesJson"] == {"zoneCode": "SPRAY-WARN"}


def test_create_field_passport_overlay_fact_rejects_mismatched_geometry_authority_link(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/overlay-facts",
        json={
            "geometrySnapshotUri": "urn:field-geometry:1",
            "authorityLinkUri": "urn:field-authority-link:foreign",
            "overlayCode": "spray_restriction",
            "severityCode": "warn",
            "observedAt": "2026-03-08T11:00:00Z",
            "sourceVersion": "overlay-2026-03-08",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_authority_link_uri"


def test_create_field_passport_daily_condition_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/daily-conditions",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOfDate": "2026-03-08",
            "observedAt": "2026-03-08T05:45:00Z",
            "sourceVersion": "daily-2026-03-08",
            "sprayWindowCode": "open",
            "nutrientSpreadingCode": "caution",
            "irrigationReadinessCode": "ready",
            "scoutPriorityCode": "medium",
            "weatherSummaryText": "Dry with light wind.",
            "eoAnomalyFlag": False,
            "riskSummaryText": "No blocking anomalies.",
            "evidenceUri": "urn:evidence:daily:1",
            "factsJson": {"windSpeedMps": 2.1},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["asOfDate"] == "2026-03-08"
    assert data["persistence"]["persistedDailyConditions"] == 1
    assert persisted_payloads["dailyConditions"][0]["sprayWindowCode"] == "open"
    assert persisted_payloads["dailyConditions"][0]["eoAnomalyFlag"] is False


def test_create_field_passport_daily_condition_rejects_cross_field_crop_instance(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_crop_instances",
        lambda crop_instance_uris: [
            {
                "uri": "urn:crop-instance:foreign",
                "fieldUri": "urn:field:foreign",
                "farmUri": DEFAULT_FARM_URI,
                "seasonCode": "2026",
                "cropTypeUri": "urn:crop:wheat",
                "productionStatus": "organic_certified",
                "certificationScopeUri": "urn:certification-scope:1",
                "cropVocabularyUri": "urn:ref:crop",
                "createdAt": "2026-01-15T12:00:00Z",
            }
        ]
        if "urn:crop-instance:foreign" in crop_instance_uris
        else [],
    )

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/daily-conditions",
        json={
            "cropInstanceUri": "urn:crop-instance:foreign",
            "asOfDate": "2026-03-08",
            "observedAt": "2026-03-08T05:45:00Z",
            "sourceVersion": "daily-2026-03-08",
            "sprayWindowCode": "open",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_crop_instance_field_mismatch"


def test_create_field_passport_climate_projection_fact_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/climate-projection-facts",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOf": "2026-03-09",
            "planningContextMode": "current_crop",
            "sourceSystem": "arso_c3s",
            "sourceId": "si-podravska-ssp245-gdd-2030s",
            "sourceVersion": "arso-c3s-2026-03-09",
            "geographyScope": "statistical_region",
            "geographyCode": "SI-PODRAVSKA",
            "scenarioFamily": "ssp",
            "scenarioCode": "ssp245",
            "horizonScope": "mid_century",
            "periodStart": "2031-01-01",
            "periodEnd": "2040-12-31",
            "baselinePeriod": "1991-2020",
            "indicatorCode": "gdd_base_10_c",
            "indicatorValue": 1485.0,
            "unitCode": "gdd",
            "aggregationType": "seasonal_mean",
            "uncertaintyClass": "medium",
            "freshnessStatus": "current",
            "evidenceRefs": ["urn:evidence:climate-projection:new"],
            "cropOrVarietyCode": "wheat",
            "geographyFitStatus": "regional_proxy",
            "baselineValue": 1390.0,
            "baselineUnitCode": "gdd",
            "scenarioSpreadValue": 55.0,
            "notes": "Scenario-backed crop heat accumulation outlook.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["indicatorCode"] == "gdd_base_10_c"
    assert data["persistence"]["persistedClimateProjectionFacts"] == 1
    assert persisted_payloads["climateProjectionFacts"][0]["cropInstanceUri"] == "urn:crop-instance:1"
    assert persisted_payloads["climateProjectionFacts"][0]["scenarioCode"] == "ssp245"
    assert persisted_payloads["climateProjectionFacts"][0]["evidenceRefs"] == [
        "urn:evidence:climate-projection:new"
    ]


def test_create_field_passport_climate_projection_fact_rejects_empty_evidence_refs(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/climate-projection-facts",
        json={
            "asOf": "2026-03-09",
            "planningContextMode": "current_crop",
            "sourceSystem": "arso_c3s",
            "sourceId": "si-podravska-ssp245-gdd-2030s",
            "sourceVersion": "arso-c3s-2026-03-09",
            "geographyScope": "statistical_region",
            "geographyCode": "SI-PODRAVSKA",
            "scenarioFamily": "ssp",
            "scenarioCode": "ssp245",
            "horizonScope": "mid_century",
            "periodStart": "2031-01-01",
            "periodEnd": "2040-12-31",
            "baselinePeriod": "1991-2020",
            "indicatorCode": "gdd_base_10_c",
            "indicatorValue": 1485.0,
            "unitCode": "gdd",
            "aggregationType": "seasonal_mean",
            "uncertaintyClass": "medium",
            "freshnessStatus": "current",
            "evidenceRefs": [],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_evidence_refs"


def test_create_field_passport_climate_adaptation_signal_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/climate-adaptation-signals",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOf": "2026-03-09",
            "planningContextMode": "current_crop",
            "signalType": "warmingTrend",
            "priorityLevel": "high",
            "horizonScope": "mid_century",
            "confidenceStatus": "medium",
            "recommendedThemes": ["review_variety", "review_irrigation"],
            "reasonCodes": ["heat_pressure_increase", "rainfall_shift_risk"],
            "traceRefs": ["urn:trace:climate-adaptation:new"],
            "evidenceRefs": ["urn:evidence:climate-adaptation:new"],
            "cropOrVarietyCode": "wheat",
            "geographyFitStatus": "regional_proxy",
            "uncertaintyCodes": ["regional_proxy_only"],
            "notes": "Derived adaptation signal for the active crop.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["signalType"] == "warmingTrend"
    assert data["persistence"]["persistedClimateAdaptationSignals"] == 1
    assert persisted_payloads["climateAdaptationSignals"][0]["priorityLevel"] == "high"
    assert persisted_payloads["climateAdaptationSignals"][0]["recommendedThemes"] == [
        "review_variety",
        "review_irrigation",
    ]


def test_create_field_passport_climate_adaptation_signal_rejects_invalid_signal_type(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/climate-adaptation-signals",
        json={
            "asOf": "2026-03-09",
            "planningContextMode": "current_crop",
            "signalType": "warming_trend",
            "priorityLevel": "high",
            "horizonScope": "mid_century",
            "confidenceStatus": "medium",
            "recommendedThemes": ["review_variety"],
            "reasonCodes": ["heat_pressure_increase"],
            "traceRefs": ["urn:trace:climate-adaptation:new"],
            "evidenceRefs": ["urn:evidence:climate-adaptation:new"],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_signal_type"


def test_create_field_passport_benchmark_context_fact_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/benchmark-context-facts",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOf": "2026-03-09",
            "sourceSystem": "surs",
            "sourceId": "surs-si-podravska-yield-2026-03",
            "sourceVersion": "surs-2026-03-09",
            "geographyScope": "statistical_region",
            "geographyCode": "SI-PODRAVSKA",
            "benchmarkDomain": "yield_context",
            "metricCode": "winter_wheat_yield_index",
            "metricValue": 0.91,
            "unitCode": "index",
            "periodType": "annual",
            "periodStart": "2026-01-01",
            "periodEnd": "2026-12-31",
            "baselineType": "rolling_average",
            "freshnessStatus": "current",
            "confidenceStatus": "medium",
            "evidenceRefs": ["urn:evidence:benchmark-context:new"],
            "traceRefs": ["urn:trace:benchmark-context:new"],
            "cropOrCommodityCode": "wheat",
            "notes": "Stored seasonal yield benchmark context.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["benchmarkDomain"] == "yield_context"
    assert data["persistence"]["persistedBenchmarkContextFacts"] == 1
    assert persisted_payloads["benchmarkContextFacts"][0]["metricCode"] == "winter_wheat_yield_index"
    assert persisted_payloads["benchmarkContextFacts"][0]["traceRefs"] == [
        "urn:trace:benchmark-context:new"
    ]


def test_create_field_passport_benchmark_context_fact_rejects_empty_evidence_refs(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/benchmark-context-facts",
        json={
            "asOf": "2026-03-09",
            "sourceSystem": "surs",
            "sourceId": "surs-si-podravska-yield-2026-03",
            "sourceVersion": "surs-2026-03-09",
            "geographyScope": "statistical_region",
            "geographyCode": "SI-PODRAVSKA",
            "benchmarkDomain": "yield_context",
            "metricCode": "winter_wheat_yield_index",
            "metricValue": 0.91,
            "unitCode": "index",
            "periodType": "annual",
            "periodStart": "2026-01-01",
            "periodEnd": "2026-12-31",
            "baselineType": "rolling_average",
            "freshnessStatus": "current",
            "confidenceStatus": "medium",
            "evidenceRefs": [],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_evidence_refs"


def test_create_field_passport_benchmark_context_fact_accepts_vineyard_structure_domain(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/benchmark-context-facts",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOf": "2026-03-09",
            "sourceSystem": "surs",
            "sourceId": "surs-si-goriska-vineyards-2026-03",
            "sourceVersion": "surs-15P2107S-2023-09-07",
            "geographyScope": "statistical_region",
            "geographyCode": "11",
            "benchmarkDomain": "vineyard_structure",
            "metricCode": "vineyard_area_ha",
            "metricValue": 3990.0,
            "unitCode": "ha",
            "periodType": "annual",
            "periodStart": "2020-01-01",
            "periodEnd": "2020-12-31",
            "baselineType": "current",
            "freshnessStatus": "current",
            "confidenceStatus": "high",
            "evidenceRefs": ["https://pxweb.stat.si/SiStatData/pxweb/en/Data/-/15P2107S.px"],
            "traceRefs": ["urn:trace:surs:pxweb:15p2107s:11:2020:1"],
            "cropOrCommodityCode": "vineyards_total",
            "notes": "Stored vineyard structure benchmark context.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["benchmarkDomain"] == "vineyard_structure"
    assert persisted_payloads["benchmarkContextFacts"][0]["metricCode"] == "vineyard_area_ha"


def test_create_field_passport_explainability_signal_persists_record(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/explainability-signals",
        json={
            "cropInstanceUri": "urn:crop-instance:1",
            "asOf": "2026-03-09",
            "signalType": "marketPressureContext",
            "signalLevel": "watch",
            "localityStatus": "national_pattern",
            "confidenceStatus": "medium",
            "recommendedNextStep": "check_market_exposure",
            "policyId": "si-surs-grapes-yield-explainability-1502410S-draft-v1",
            "policyVersion": "1.0.0",
            "reasonCodes": ["price_context:stale"],
            "traceRefs": ["urn:trace:benchmark-explainability:new"],
            "evidenceRefs": ["urn:evidence:benchmark-explainability:new"],
            "notes": "Stored market explainability signal.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["fieldUri"] == DEFAULT_FIELD_URI
    assert data["signalType"] == "marketPressureContext"
    assert data["policyId"] == "si-surs-grapes-yield-explainability-1502410S-draft-v1"
    assert data["persistence"]["persistedExplainabilitySignals"] == 1
    assert persisted_payloads["explainabilitySignals"][0]["policyVersion"] == "1.0.0"
    assert persisted_payloads["explainabilitySignals"][0]["recommendedNextStep"] == "check_market_exposure"


def test_get_field_explainability_summary_prefers_active_policy_batch(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(
        main_module.PERSISTENCE,
        "fetch_field_explainability_signals",
        lambda field_uri: [
            {
                "uri": "urn:field-explainability-signal:old-policy",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "signalType": "regionalStressContext",
                "signalLevel": "elevated",
                "localityStatus": "partly_regional",
                "confidenceStatus": "high",
                "recommendedNextStep": "monitor_region",
                "policyId": "benchmark-demo-old",
                "policyVersion": "0.1.0",
                "reasonCodes": ["drought_context:regional-watch"],
                "traceRefs": ["policy:benchmark-demo-old:0.1.0"],
                "evidenceRefs": ["urn:evidence:benchmark-explainability:old"],
                "notes": "Older policy batch.",
                "createdAt": "2026-03-10T08:00:00Z",
            },
            {
                "uri": "urn:field-explainability-signal:new-policy-1",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "signalType": "localOutlierContext",
                "signalLevel": "high",
                "localityStatus": "local_only",
                "confidenceStatus": "high",
                "recommendedNextStep": "inspect_local",
                "policyId": "benchmark-reviewed",
                "policyVersion": "1.0.0",
                "reasonCodes": ["yield_context:local-outlier"],
                "traceRefs": ["policy:benchmark-reviewed:1.0.0"],
                "evidenceRefs": ["urn:evidence:benchmark-explainability:new-1"],
                "notes": "Current policy batch.",
                "createdAt": "2026-03-10T09:00:00Z",
            },
            {
                "uri": "urn:field-explainability-signal:new-policy-2",
                "fieldUri": field_uri,
                "cropInstanceUri": "urn:crop-instance:1",
                "asOf": "2026-03-10",
                "signalType": "dataCoverageGap",
                "signalLevel": "watch",
                "localityStatus": "unknown",
                "confidenceStatus": "low",
                "recommendedNextStep": "gather_more_evidence",
                "policyId": "benchmark-reviewed",
                "policyVersion": "1.0.0",
                "reasonCodes": ["missing_field_state"],
                "traceRefs": ["policy:benchmark-reviewed:1.0.0"],
                "evidenceRefs": ["urn:evidence:benchmark-explainability:new-2"],
                "notes": "Current policy batch gap.",
                "createdAt": "2026-03-10T09:00:00Z",
            },
        ],
    )

    response = client.get(
        f"/v1/fields/{_encoded_field_uri()}/explainability-summary",
        params={"asOfDate": "2026-03-10"},
    )

    assert response.status_code == 200
    data = response.json()
    assert [item["policyId"] for item in data["topSignals"]] == [
        "benchmark-reviewed",
        "benchmark-reviewed",
    ]
    assert data["topSignals"][0]["signalType"] == "localOutlierContext"
    assert "active_policy:benchmark-reviewed:1.0.0" in data["traceRefs"]


def test_create_field_passport_explainability_signal_rejects_invalid_locality_status(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/explainability-signals",
        json={
            "asOf": "2026-03-09",
            "signalType": "regionalStressContext",
            "signalLevel": "watch",
            "localityStatus": "regional_only",
            "confidenceStatus": "medium",
            "recommendedNextStep": "monitor_region",
            "reasonCodes": ["drought_context:watch"],
            "traceRefs": ["urn:trace:benchmark-explainability:new"],
            "evidenceRefs": ["urn:evidence:benchmark-explainability:new"],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_locality_status"


def test_create_field_passport_explainability_signal_requires_complete_policy_identity(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/explainability-signals",
        json={
            "asOf": "2026-03-09",
            "signalType": "regionalStressContext",
            "signalLevel": "watch",
            "localityStatus": "partly_regional",
            "confidenceStatus": "medium",
            "recommendedNextStep": "monitor_region",
            "policyId": "si-benchmark-explainability-demo",
            "reasonCodes": ["drought_context:watch"],
            "traceRefs": ["urn:trace:benchmark-explainability:new"],
            "evidenceRefs": ["urn:evidence:benchmark-explainability:new"],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_policy_identity"


def test_get_field_passport_persists_stale_issue_snapshot_when_projection_is_incomplete(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)
    monkeypatch.setattr(main_module.PERSISTENCE, "fetch_field_authority_links", lambda field_uri: [])

    response = client.get(f"/v1/fields/{_encoded_field_uri()}/passport", params={"asOfDate": "2026-03-07"})

    assert response.status_code == 200
    data = response.json()
    assert data["passport"]["freshness"]["staleFlags"] == ["no_current_authority_link"]
    assert len(persisted_payloads["staleIssueSnapshots"]) == 1
    snapshot = persisted_payloads["staleIssueSnapshots"][0]
    assert snapshot["farmUri"] == DEFAULT_FARM_URI
    assert snapshot["fieldUri"] == DEFAULT_FIELD_URI
    assert snapshot["staleFlag"] == "no_current_authority_link"
    assert snapshot["asOfDate"] == "2026-03-07"
    assert snapshot["subjectSnapshot"]["fieldLabel"] == "North parcel"
    assert snapshot["subjectSnapshot"]["seasonCode"] == "2026"
    assert snapshot["sourceSnapshot"]["authorityLinkMissingRecord"] is True
    assert str(snapshot["issueId"]).startswith("urn:dashboard-issue:")


def test_evaluate_field_passport_daily_returns_allow(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/evaluate-daily",
        json={"asOfDate": "2026-03-07"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rulePackCode"] == "SI_FIELD_OPS_2026_DRAFT_V1"
    assert data["overallOutcomeCode"] == "allow"
    assert {item["evaluationType"] for item in data["evaluations"]} == {
        "daily_irrigation",
        "daily_nutrient_spreading",
        "daily_scout_priority",
        "daily_spray_window",
    }
    assert all(item["outcomeCode"] == "allow" for item in data["evaluations"])


def test_evaluate_field_passport_action_persists_warn_result(monkeypatch) -> None:
    _enable_field_passport_features(monkeypatch)
    persisted_payloads = _stub_field_passport_context(monkeypatch)

    response = client.post(
        f"/v1/fields/{_encoded_field_uri()}/passport/evaluate-action",
        json={
            "asOfDate": "2026-03-07",
            "actionCode": "pesticide_application",
            "candidateLabel": "Approved fungicide X",
            "materialLotUri": "urn:material-lot:1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["evaluation"]["actionCode"] == "pesticide_application"
    assert data["evaluation"]["outcomeCode"] == "warn"
    assert "input_authorization_conditional" in data["evaluation"]["reasonCodes"]
    assert data["persistence"]["persistedFieldActionEvaluations"] == 1
    assert data["passport"]["actionEvaluations"][0]["outcomeCode"] == "warn"
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["candidateAuthorization"]["decisionCode"] == "conditional"
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["facts"]["daily"]["sprayWindowCode"] == "open"
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["subjectSnapshot"]["fieldLabel"] == "North parcel"
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["subjectSnapshot"]["seasonCode"] == "2026"
    assert persisted_payloads["actionEvaluations"][0]["decisionContext"]["subjectSnapshot"]["declaredCropLabel"] == "Wheat"


def test_rulepack_blocks_rejected_input_candidate() -> None:
    passport = {
        "officialLinks": [{"authoritySchemeCode": "gerk", "authorityRecordUri": "urn:gerk:1", "validFrom": "2026-01-01T00:00:00Z", "validTo": "2026-12-31T23:59:59Z"}],
        "complianceGeometryRef": "urn:geometry:1",
        "overlayFacts": [],
        "dailyState": {"sprayWindowCode": "open"},
    }

    facts = build_fact_snapshot(
        passport,
        as_of_date=main_module._parse_iso_date("2026-03-07"),
        candidate_authorization={"decisionCode": "rejected"},
    )
    evaluation = evaluate_rules(
        rulepack=load_field_ops_rulepack(),
        evaluation_type="pesticide_application",
        facts=facts,
    )

    assert evaluation["outcomeCode"] == "block"
    assert "input_authorization_missing_or_rejected" in evaluation["reasonCodes"]


def test_normalize_candidate_authorization_evaluation_strips_conditional_reason_for_rejected() -> None:
    passport = {
        "officialLinks": [{"authoritySchemeCode": "gerk", "authorityRecordUri": "urn:gerk:1", "validFrom": "2026-01-01T00:00:00Z", "validTo": "2026-12-31T23:59:59Z"}],
        "complianceGeometryRef": "urn:geometry:1",
        "overlayFacts": [],
        "dailyState": {"sprayWindowCode": "open"},
    }

    facts = build_fact_snapshot(
        passport,
        as_of_date=main_module._parse_iso_date("2026-03-07"),
        candidate_authorization={"decisionCode": "rejected"},
    )
    evaluation = evaluate_rules(
        rulepack=load_field_ops_rulepack(),
        evaluation_type="pesticide_application",
        facts=facts,
    )

    normalized = normalize_candidate_authorization_evaluation(
        evaluation,
        candidate_authorization={"decisionCode": "rejected"},
    )

    assert normalized["outcomeCode"] == "block"
    assert normalized["reasonCodes"] == ["input_authorization_missing_or_rejected"]
    assert "input_authorization_conditional" not in {
        str(item.get("reasonCode") or "") for item in normalized["ruleResults"]
    }
