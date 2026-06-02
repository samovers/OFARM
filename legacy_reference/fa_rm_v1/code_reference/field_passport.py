from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional
from uuid import uuid4

from app.dev_context import dev_context_rulepack_path


def _discover_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "specs").exists() and (candidate / "specs/api/v1").exists():
            return candidate
    raise RuntimeError("Could not discover repository root containing /specs")


ROOT = _discover_repo_root()
RULEPACK_PATH = ROOT / "specs/v0.4/regulatory/rulepacks/si-field-ops-2026-draft.json"
WATER_STEWARDSHIP_RULEPACK_PATH = ROOT / "specs/v0.4/regulatory/rulepacks/si-field-ops-water-stewardship-2026-draft.json"

FIELD_PASSPORT_TEMPLATE_ID = "farm.tpl.si.field_compliance_passport.v0_8"
FIELD_ACTION_CHECK_TEMPLATE_ID = "farm.tpl.si.field_action_check.v0_8"
FIELD_SPRAY_WINDOW_TEMPLATE_ID = "farm.tpl.si.field_spray_window.v0_8"
FIELD_PLANT_HEALTH_RELEVANCE_TEMPLATE_ID = "farm.tpl.si.field_plant_health_relevance.v0_8"
FIELD_EO_ANOMALY_TEMPLATE_ID = "farm.tpl.si.field_eo_anomaly_triage.v0_8"
FIELD_PHENOLOGY_STATUS_TEMPLATE_ID = "farm.tpl.si.field_phenology_status.v0_8"
FIELD_SCOUT_PRIORITY_QUEUE_TEMPLATE_ID = "farm.tpl.si.field_scout_priority_queue.v0_8"
FIELD_WATER_STEWARDSHIP_TEMPLATE_ID = "farm.tpl.si.field_water_stewardship.v0_8"
FIELD_NITROGEN_APPLICATION_CHECK_TEMPLATE_ID = "farm.tpl.si.field_nitrogen_application_check.v0_8"
FIELD_IRRIGATION_READINESS_TEMPLATE_ID = "farm.tpl.si.field_irrigation_readiness.v0_8"
FIELD_BENCHMARK_CONTEXT_TEMPLATE_ID = "farm.tpl.si.field_benchmark_context.v0_8"
FIELD_EXPLAINABILITY_SUMMARY_TEMPLATE_ID = "farm.tpl.si.field_explainability_summary.v0_8"
FIELD_REGIONAL_COMPARISON_TEMPLATE_ID = "farm.tpl.si.field_regional_comparison.v0_8"
FIELD_CLIMATE_ADAPTATION_SUMMARY_TEMPLATE_ID = "farm.tpl.si.field_climate_adaptation_summary.v0_8"
FIELD_CLIMATE_SUITABILITY_OUTLOOK_TEMPLATE_ID = "farm.tpl.si.field_climate_suitability_outlook.v0_8"
FIELD_CLIMATE_INDICATOR_TRENDS_TEMPLATE_ID = "farm.tpl.si.field_climate_indicator_trends.v0_8"
FIELD_CLIMATE_PLAN_TAB_TEMPLATE_ID = "farm.tpl.si.field_climate_plan_tab.v0_8"

DAILY_EVALUATION_TYPES = (
    "daily_spray_window",
    "daily_nutrient_spreading",
    "daily_irrigation",
    "daily_scout_priority",
)
SUPPORTED_ACTION_CODES = (
    "pesticide_application",
    "fertilizer_application",
    "soil_amendment_application",
    "irrigation_event",
)

_GEOMETRY_ROLE_PREFERENCE = (
    "compliance_scope",
    "agricultural_parcel",
    "farm_drawn",
    "cadastre_parcel",
    "orthophoto_observation",
    "other",
)

_SPRAY_BLOCKING_OVERLAYS = {"spray_restriction"}
_NUTRIENT_BLOCKING_OVERLAYS = {"nutrient_restriction"}
_IRRIGATION_BLOCKING_OVERLAYS = {"irrigation_restriction", "flood_hazard"}

_OUTCOME_RANK = {
    "low": 0,
    "watch": 1,
    "elevated": 2,
    "high": 3,
    "unknown": -1,
}
_SCOUT_PRIORITY_RANK = {
    "none": 0,
    "low": 1,
    "normal": 2,
    "high": 3,
    "urgent": 4,
    "unknown": -1,
}
_CLIMATE_PRIORITY_RANK = {
    "exploratory": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


def load_field_ops_rulepack() -> dict[str, Any]:
    path = dev_context_rulepack_path("fieldOps") or RULEPACK_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def load_field_water_stewardship_rulepack() -> dict[str, Any]:
    path = dev_context_rulepack_path("fieldWaterStewardship") or WATER_STEWARDSHIP_RULEPACK_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_as_of_date(value: str) -> date:
    return date.fromisoformat(str(value).strip())


def _parse_iso_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_iso_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        parsed = _parse_iso_datetime(text)
        return parsed.date() if parsed else None


def _time_sort_tuple(item: dict[str, Any], *time_fields: str) -> tuple[datetime, ...]:
    values: list[datetime] = []
    for field_name in time_fields:
        current_dt = _parse_iso_datetime(item.get(field_name))
        if current_dt is None:
            current_date = _parse_iso_date(item.get(field_name))
            if current_date is not None:
                current_dt = datetime.combine(current_date, datetime.min.time(), tzinfo=timezone.utc)
        values.append(current_dt or datetime.min.replace(tzinfo=timezone.utc))
    return tuple(values)


def _latest_item(items: Iterable[dict[str, Any]], *time_fields: str) -> Optional[dict[str, Any]]:
    chosen: Optional[dict[str, Any]] = None
    chosen_key: Optional[tuple[datetime, ...]] = None
    min_dt = datetime.min.replace(tzinfo=timezone.utc)
    for item in items:
        current_key = _time_sort_tuple(item, *time_fields)
        if all(current_dt == min_dt for current_dt in current_key):
            continue
        if chosen is None or chosen_key is None or current_key > chosen_key:
            chosen = item
            chosen_key = current_key
    return chosen


def _interval_active(item: dict[str, Any], as_of_date: date) -> bool:
    start_dt = _parse_iso_datetime(item.get("validFrom"))
    end_dt = _parse_iso_datetime(item.get("validTo"))
    start_date = start_dt.date() if start_dt else None
    end_date = end_dt.date() if end_dt else None
    if start_date and as_of_date < start_date:
        return False
    if end_date and as_of_date > end_date:
        return False
    return True


def _current_authority_links(links: list[dict[str, Any]], as_of_date: date) -> list[dict[str, Any]]:
    return [item for item in links if _interval_active(item, as_of_date)]


def _current_interval_items(items: Iterable[dict[str, Any]], as_of_date: date) -> list[dict[str, Any]]:
    return [item for item in items if _interval_active(item, as_of_date)]


def resolve_compliance_geometry_ref(
    declarations: list[dict[str, Any]],
    geometries: list[dict[str, Any]],
    *,
    as_of_date: Optional[date] = None,
) -> Optional[str]:
    relevant_declarations = list(declarations)
    relevant_geometries = list(geometries)
    if as_of_date is not None:
        relevant_declarations = _current_interval_items(relevant_declarations, as_of_date)
        relevant_geometries = _current_interval_items(relevant_geometries, as_of_date)

    latest_declaration = _latest_item(relevant_declarations, "declaredAt", "validFrom", "createdAt")
    if latest_declaration:
        explicit_ref = str(latest_declaration.get("complianceGeometryRef") or "").strip()
        if explicit_ref:
            return explicit_ref

    for item in sorted(
        relevant_geometries,
        key=lambda row: _parse_iso_datetime(row.get("capturedAt")) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    ):
        if bool(item.get("isComplianceGeometry")):
            geometry_ref = str(item.get("geometryRef") or "").strip()
            if geometry_ref:
                return geometry_ref

    for role in _GEOMETRY_ROLE_PREFERENCE:
        for item in sorted(
            relevant_geometries,
            key=lambda row: _parse_iso_datetime(row.get("capturedAt")) or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        ):
            if str(item.get("geometryRoleCode") or "").strip() != role:
                continue
            geometry_ref = str(item.get("geometryRef") or "").strip()
            if geometry_ref:
                return geometry_ref
    return None


def _select_daily_state(
    condition_records: list[dict[str, Any]],
    as_of_date: date,
) -> Optional[dict[str, Any]]:
    dated_records = [
        item
        for item in condition_records
        if (_parse_iso_date(item.get("asOfDate")) or as_of_date) <= as_of_date
    ]
    selected = _latest_item(dated_records, "asOfDate", "observedAt", "createdAt")
    if selected is None:
        selected = _latest_item(condition_records, "asOfDate", "observedAt", "createdAt")
    return selected


def _overlay_blocked(overlays: list[dict[str, Any]], *, as_of_date: date, blocked_codes: set[str]) -> bool:
    for item in overlays:
        if not _interval_active(item, as_of_date):
            continue
        if str(item.get("severityCode") or "").strip() != "block":
            continue
        if str(item.get("overlayCode") or "").strip() in blocked_codes:
            return True
    return False


def build_field_passport(
    *,
    as_of_date: date,
    field_row: dict[str, Any],
    authority_links: list[dict[str, Any]],
    geometry_snapshots: list[dict[str, Any]],
    declaration_snapshots: list[dict[str, Any]],
    latest_crop_instance: Optional[dict[str, Any]],
    resolved_crop_context: Optional[dict[str, Any]] = None,
    overlay_facts: list[dict[str, Any]],
    condition_records: list[dict[str, Any]],
    agrometeorological_observations: list[dict[str, Any]],
    action_evaluations: list[dict[str, Any]],
    recent_events: list[dict[str, Any]],
    recent_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    current_declarations = _current_interval_items(declaration_snapshots, as_of_date)
    compliance_geometry_ref = resolve_compliance_geometry_ref(
        current_declarations,
        geometry_snapshots,
        as_of_date=as_of_date,
    )
    latest_declaration = _latest_item(current_declarations, "declaredAt", "validFrom", "createdAt")
    daily_state = _select_daily_state(condition_records, as_of_date)
    agrometeorological_state = _latest_item(
        agrometeorological_observations,
        "observedAt",
        "timeSupportEnd",
        "createdAt",
    )
    current_overlays = [item for item in overlay_facts if _interval_active(item, as_of_date)]

    crop_context: dict[str, Any] = {
        "cropInstanceUri": None,
        "seasonCode": None,
        "cropTypeUri": None,
        "productionStatus": None,
        "warnings": [],
        "cropIdentitySource": None,
        "cropIdentitySourceRef": None,
        "cropIdentityAlternateSources": [],
        "cropIdentityAlternateSourceRefs": [],
        "productionStatusSource": None,
        "productionStatusSourceRef": None,
        "productionStatusAlternateSources": [],
        "productionStatusAlternateSourceRefs": [],
        "cropIdentityAlternateCandidates": [],
        "productionStatusAlternateCandidates": [],
        "declarationSnapshotUri": None,
        "declaredCropLabel": None,
        "declaredUseCode": None,
        "declaredAreaHa": None,
        "effectiveFrom": None,
        "effectiveTo": None,
    }
    if isinstance(resolved_crop_context, dict):
        crop_context.update(
            {
                "cropInstanceUri": resolved_crop_context.get("cropInstanceUri"),
                "seasonCode": resolved_crop_context.get("seasonCode"),
                "cropTypeUri": resolved_crop_context.get("cropTypeUri"),
                "productionStatus": resolved_crop_context.get("productionStatus"),
                "warnings": [str(item) for item in resolved_crop_context.get("warnings") or [] if str(item)],
                "cropIdentitySource": resolved_crop_context.get("cropIdentitySource"),
                "cropIdentitySourceRef": resolved_crop_context.get("cropIdentitySourceRef"),
                "cropIdentityAlternateSources": [
                    str(item)
                    for item in resolved_crop_context.get("cropIdentityAlternateSources") or []
                    if str(item)
                ],
                "cropIdentityAlternateSourceRefs": [
                    str(item)
                    for item in resolved_crop_context.get("cropIdentityAlternateSourceRefs") or []
                    if str(item)
                ],
                "cropIdentityAlternateCandidates": [
                    dict(item)
                    for item in resolved_crop_context.get("cropIdentityAlternateCandidates") or []
                    if isinstance(item, dict)
                ],
                "productionStatusSource": resolved_crop_context.get("productionStatusSource"),
                "productionStatusSourceRef": resolved_crop_context.get("productionStatusSourceRef"),
                "productionStatusAlternateSources": [
                    str(item)
                    for item in resolved_crop_context.get("productionStatusAlternateSources") or []
                    if str(item)
                ],
                "productionStatusAlternateSourceRefs": [
                    str(item)
                    for item in resolved_crop_context.get("productionStatusAlternateSourceRefs") or []
                    if str(item)
                ],
                "productionStatusAlternateCandidates": [
                    dict(item)
                    for item in resolved_crop_context.get("productionStatusAlternateCandidates") or []
                    if isinstance(item, dict)
                ],
                "declarationSnapshotUri": resolved_crop_context.get("declarationSnapshotUri"),
                "declaredCropLabel": resolved_crop_context.get("declaredCropLabel"),
                "declaredUseCode": resolved_crop_context.get("declaredUseCode"),
                "declaredAreaHa": resolved_crop_context.get("declaredAreaHa"),
                "effectiveFrom": resolved_crop_context.get("effectiveFrom"),
                "effectiveTo": resolved_crop_context.get("effectiveTo"),
            }
        )
    else:
        if latest_crop_instance:
            latest_crop_status = str(latest_crop_instance.get("productionStatus") or "").strip()
            latest_crop_status_known = bool(latest_crop_status and latest_crop_status.lower() != "unknown")
            crop_context.update(
                {
                    "cropInstanceUri": latest_crop_instance.get("uri"),
                    "seasonCode": latest_crop_instance.get("seasonCode"),
                    "cropTypeUri": latest_crop_instance.get("cropTypeUri"),
                    "productionStatus": latest_crop_instance.get("productionStatus"),
                    "cropIdentitySource": "latest_crop_instance",
                    "cropIdentitySourceRef": latest_crop_instance.get("uri"),
                    "productionStatusSource": (
                        "latest_crop_instance"
                        if latest_crop_status_known
                        else crop_context.get("productionStatusSource")
                    ),
                    "productionStatusSourceRef": (
                        latest_crop_instance.get("uri")
                        if latest_crop_status_known
                        else crop_context.get("productionStatusSourceRef")
                    ),
                }
            )
        if latest_declaration:
            declaration_source_ref = latest_declaration.get("declarationSnapshotUri") or latest_declaration.get("uri")
            declaration_status_value = str(latest_declaration.get("productionStatus") or "").strip()
            declaration_status = (
                declaration_status_value
                if declaration_status_value and declaration_status_value.lower() != "unknown"
                else None
            )
            crop_context.update(
                {
                    "cropInstanceUri": latest_declaration.get("cropInstanceUri") or crop_context.get("cropInstanceUri"),
                    "seasonCode": latest_declaration.get("seasonCode") or crop_context.get("seasonCode"),
                    "cropTypeUri": latest_declaration.get("declaredCropTypeUri") or crop_context.get("cropTypeUri"),
                    "productionStatus": _prefer_non_unknown_text(
                        latest_declaration.get("productionStatus"),
                        crop_context.get("productionStatus"),
                    ),
                    "cropIdentitySource": (
                        "declaration_snapshot"
                        if any(
                            latest_declaration.get(key)
                            for key in ("cropInstanceUri", "seasonCode", "declaredCropTypeUri")
                        )
                        else crop_context.get("cropIdentitySource")
                    ),
                    "cropIdentitySourceRef": (
                        declaration_source_ref
                        if any(
                            latest_declaration.get(key)
                            for key in ("cropInstanceUri", "seasonCode", "declaredCropTypeUri")
                        )
                        else crop_context.get("cropIdentitySourceRef")
                    ),
                    "productionStatusSource": (
                        "declaration_snapshot" if declaration_status else crop_context.get("productionStatusSource")
                    ),
                    "productionStatusSourceRef": (
                        declaration_source_ref if declaration_status else crop_context.get("productionStatusSourceRef")
                    ),
                    "declarationSnapshotUri": declaration_source_ref,
                    "declaredCropLabel": latest_declaration.get("declaredCropLabel"),
                    "declaredUseCode": latest_declaration.get("declaredUseCode"),
                    "declaredAreaHa": latest_declaration.get("declaredAreaHa"),
                    "effectiveFrom": latest_declaration.get("validFrom"),
                    "effectiveTo": latest_declaration.get("validTo"),
                }
            )

    freshness = {
        "authorityRecordedAt": (_latest_item(authority_links, "recordedAt", "createdAt") or {}).get("recordedAt"),
        "geometryCapturedAt": (_latest_item(geometry_snapshots, "capturedAt", "createdAt") or {}).get("capturedAt"),
        "declarationDeclaredAt": (latest_declaration or {}).get("declaredAt"),
        "overlayObservedAt": (_latest_item(current_overlays, "observedAt", "createdAt") or {}).get("observedAt"),
        "dailyObservedAt": (daily_state or {}).get("observedAt"),
        "agrometeorologicalObservedAt": (agrometeorological_state or {}).get("observedAt"),
        "actionEvaluatedAt": (_latest_item(action_evaluations, "evaluatedAt", "createdAt") or {}).get("evaluatedAt"),
        "generatedAt": utc_now_iso(),
        "staleFlags": [],
    }
    if not _current_authority_links(authority_links, as_of_date):
        freshness["staleFlags"].append("no_current_authority_link")
    if not compliance_geometry_ref:
        freshness["staleFlags"].append("missing_compliance_geometry")
    if daily_state is None:
        freshness["staleFlags"].append("missing_daily_condition")

    return {
        "identity": {
            "fieldUri": field_row.get("uri"),
            "farmUri": field_row.get("farmUri"),
            "label": field_row.get("label"),
            "areaHa": field_row.get("areaHa"),
        },
        "officialLinks": authority_links,
        "geometrySnapshots": geometry_snapshots,
        "complianceGeometryRef": compliance_geometry_ref,
        "cropContext": crop_context,
        "overlayFacts": current_overlays,
        "dailyState": daily_state,
        "agrometeorologicalState": agrometeorological_state,
        "actionEvaluations": action_evaluations,
        "recentEvents": recent_events,
        "recentEvidence": recent_evidence,
        "freshness": freshness,
    }


def select_latest_permanent_crop_component_snapshot_batch(
    component_snapshots: list[dict[str, Any]],
    *,
    as_of_date: Optional[date] = None,
) -> list[dict[str, Any]]:
    candidates = [row for row in component_snapshots if isinstance(row, dict)]
    if as_of_date is not None:
        filtered: list[dict[str, Any]] = []
        for row in candidates:
            observed_at = _parse_iso_datetime(row.get("observedAt"))
            if observed_at is not None and observed_at.date() <= as_of_date:
                filtered.append(row)
        candidates = filtered

    latest_row = _latest_item(candidates, "observedAt", "createdAt")
    if not latest_row:
        return []

    latest_observed_at = str(latest_row.get("observedAt") or "").strip()
    latest_source_version = str(latest_row.get("sourceVersion") or "").strip()
    latest_crop_instance_uri = str(latest_row.get("cropInstanceUri") or "").strip()
    latest_field_uri = str(latest_row.get("fieldUri") or "").strip()

    batch = [
        row
        for row in candidates
        if str(row.get("observedAt") or "").strip() == latest_observed_at
        and str(row.get("sourceVersion") or "").strip() == latest_source_version
        and str(row.get("fieldUri") or "").strip() == latest_field_uri
        and str(row.get("cropInstanceUri") or "").strip() == latest_crop_instance_uri
    ]
    return sorted(
        batch,
        key=lambda row: (
            int(row.get("componentOrder") or 0),
            str(row.get("varietyLabel") or "").strip(),
            str(row.get("uri") or "").strip(),
        ),
    )


def build_field_permanent_crop_composition_projection(
    *,
    passport: dict[str, Any],
    as_of_date: date,
    component_snapshots: list[dict[str, Any]],
) -> dict[str, Any]:
    batch = select_latest_permanent_crop_component_snapshot_batch(
        component_snapshots,
        as_of_date=as_of_date,
    )
    crop_context = passport.get("cropContext") if isinstance(passport.get("cropContext"), dict) else {}
    active_crop_instance_uri = str(crop_context.get("cropInstanceUri") or "").strip() or None
    evidence_refs = collect_passport_evidence_uris(passport)
    trace_refs: list[str] = []

    if not batch:
        return {
            "fieldUri": passport.get("identity", {}).get("fieldUri"),
            "asOfDate": as_of_date.isoformat(),
            "activeCropInstanceUri": active_crop_instance_uri,
            "status": "missing",
            "componentCount": 0,
            "varietyCount": 0,
            "components": [],
            "evidenceRefs": evidence_refs,
            "traceRefs": trace_refs,
        }

    total_plant_count = sum(int(row.get("plantCount") or 0) for row in batch if row.get("plantCount") is not None)
    resolved_total_plant_count = total_plant_count if total_plant_count > 0 else None
    components: list[dict[str, Any]] = []
    seen_variety_labels: set[str] = set()

    for row in batch:
        component_uri = str(row.get("uri") or "").strip()
        variety_uri = str(row.get("varietyUri") or "").strip() or None
        authority_record_uri = str(row.get("authorityRecordUri") or "").strip()
        evidence_uri = str(row.get("evidenceUri") or "").strip()
        plant_count = int(row.get("plantCount") or 0) if row.get("plantCount") is not None else None
        if component_uri:
            _append_unique(trace_refs, component_uri)
        if authority_record_uri:
            _append_unique(trace_refs, authority_record_uri)
        if evidence_uri:
            _append_unique(evidence_refs, evidence_uri)
        variety_label = str(row.get("varietyLabel") or "").strip()
        if variety_label:
            seen_variety_labels.add(variety_label)

        plant_share_pct = None
        if plant_count is not None and resolved_total_plant_count:
            plant_share_pct = round((plant_count / resolved_total_plant_count) * 100.0, 2)

        components.append(
            {
                "componentUri": component_uri or None,
                "componentOrder": int(row.get("componentOrder") or 0),
                "plantCount": plant_count,
                "plantSharePct": plant_share_pct,
                "varietyUri": variety_uri,
                "varietyLabel": variety_label,
                "rootstockLabel": row.get("rootstockLabel"),
                "trainingFormLabel": row.get("trainingFormLabel"),
                "plantingYear": int(row.get("plantingYear") or 0) if row.get("plantingYear") is not None else None,
                "intraRowSpacingM": _as_number(row.get("intraRowSpacingM")),
                "interRowSpacingM": _as_number(row.get("interRowSpacingM")),
                "notes": row.get("notes"),
            }
        )

    first_row = batch[0]
    return {
        "fieldUri": passport.get("identity", {}).get("fieldUri"),
        "asOfDate": as_of_date.isoformat(),
        "activeCropInstanceUri": active_crop_instance_uri or first_row.get("cropInstanceUri"),
        "status": "available",
        "sourceVersion": first_row.get("sourceVersion"),
        "observedAt": first_row.get("observedAt"),
        "sourceSectionLabel": first_row.get("sourceSectionLabel"),
        "sourceAreaHa": _as_number(first_row.get("sourceAreaHa")),
        "vineyardMid": first_row.get("vineyardMid"),
        "terraced": first_row.get("terraced"),
        "grassed": first_row.get("grassed"),
        "componentCount": len(components),
        "varietyCount": len(seen_variety_labels),
        "totalPlantCount": resolved_total_plant_count,
        "components": components,
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
    }


def resolve_permanent_crop_variety_context(
    component_snapshots: list[dict[str, Any]],
    *,
    as_of_date: Optional[date] = None,
) -> dict[str, Any]:
    batch = select_latest_permanent_crop_component_snapshot_batch(
        component_snapshots,
        as_of_date=as_of_date,
    )
    if not batch:
        return {}

    trace_refs: list[str] = []
    evidence_refs: list[str] = []
    totals_by_variety: dict[str, dict[str, Any]] = {}
    known_plant_count_total = 0

    for row in batch:
        row_uri = str(row.get("uri") or "").strip()
        authority_record_uri = str(row.get("authorityRecordUri") or "").strip()
        evidence_uri = str(row.get("evidenceUri") or "").strip()
        if row_uri:
            _append_unique(trace_refs, row_uri)
        if authority_record_uri:
            _append_unique(trace_refs, authority_record_uri)
        if evidence_uri:
            _append_unique(evidence_refs, evidence_uri)

        variety_uri = str(row.get("varietyUri") or "").strip()
        plant_count = row.get("plantCount")
        if not variety_uri or plant_count is None:
            continue
        plant_count_value = int(plant_count)
        if plant_count_value <= 0:
            continue
        known_plant_count_total += plant_count_value
        current = totals_by_variety.setdefault(
            variety_uri,
            {
                "varietyUri": variety_uri,
                "varietyLabel": str(row.get("varietyLabel") or "").strip() or None,
                "plantCount": 0,
            },
        )
        current["plantCount"] = int(current.get("plantCount") or 0) + plant_count_value
        if current.get("varietyLabel") in {None, ""}:
            current["varietyLabel"] = str(row.get("varietyLabel") or "").strip() or None

    if not totals_by_variety:
        return {}

    dominant = max(
        totals_by_variety.values(),
        key=lambda item: (
            int(item.get("plantCount") or 0),
            str(item.get("varietyLabel") or ""),
            str(item.get("varietyUri") or ""),
        ),
    )
    dominant_plant_count = int(dominant.get("plantCount") or 0)
    dominant_share_pct = (
        round((dominant_plant_count / known_plant_count_total) * 100.0, 2)
        if known_plant_count_total > 0
        else None
    )
    dominant_threshold_met = len(totals_by_variety) == 1 or (
        dominant_share_pct is not None and dominant_share_pct > 50.0
    )
    summary = (
        f"Dominant permanent-crop variety {str(dominant.get('varietyLabel') or dominant.get('varietyUri') or '').strip()} "
        f"covers about {dominant_share_pct:.2f}% of known plant count."
        if dominant_threshold_met and dominant_share_pct is not None
        else "Permanent-crop composition resolves to a single variety."
        if dominant_threshold_met
        else "Permanent-crop composition is mixed and does not resolve a dominant variety."
    )
    return {
        "varietyUri": str(dominant.get("varietyUri") or "").strip() or None,
        "varietyLabel": str(dominant.get("varietyLabel") or "").strip() or None,
        "dominantSharePct": dominant_share_pct,
        "dominantPlantCount": dominant_plant_count if dominant_plant_count > 0 else None,
        "knownPlantCountTotal": known_plant_count_total if known_plant_count_total > 0 else None,
        "varietyCount": len(totals_by_variety),
        "contextStatus": "dominant" if dominant_threshold_met else "mixed",
        "summary": summary,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def collect_passport_evidence_uris(
    passport: dict[str, Any],
    *,
    candidate_authorization: Optional[dict[str, Any]] = None,
) -> list[str]:
    evidence_uris: set[str] = set()
    for link in passport.get("officialLinks") or []:
        uri = str(link.get("evidenceUri") or "").strip()
        if uri:
            evidence_uris.add(uri)
    for geometry in passport.get("geometrySnapshots") or []:
        uri = str(geometry.get("evidenceUri") or "").strip()
        if uri:
            evidence_uris.add(uri)
    daily_state = passport.get("dailyState") or {}
    uri = str(daily_state.get("evidenceUri") or "").strip()
    if uri:
        evidence_uris.add(uri)
    for overlay in passport.get("overlayFacts") or []:
        overlay_uri = str(overlay.get("evidenceUri") or "").strip()
        if overlay_uri:
            evidence_uris.add(overlay_uri)
    for evaluation in passport.get("actionEvaluations") or []:
        for evaluation_uri in evaluation.get("evidenceUris") or []:
            uri_text = str(evaluation_uri).strip()
            if uri_text:
                evidence_uris.add(uri_text)
    if candidate_authorization is not None:
        auth_evidence = str(candidate_authorization.get("evidenceUri") or "").strip()
        if auth_evidence:
            evidence_uris.add(auth_evidence)
    return sorted(evidence_uris)


def build_fact_snapshot(
    passport: dict[str, Any],
    *,
    as_of_date: date,
    candidate_authorization: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    daily_state = passport.get("dailyState") or {}
    facts = {
        "authority": {
            "linksCurrent": bool(_current_authority_links(passport.get("officialLinks") or [], as_of_date)),
        },
        "geometry": {
            "complianceResolved": bool(str(passport.get("complianceGeometryRef") or "").strip()),
        },
        "daily": {
            "sprayWindowCode": daily_state.get("sprayWindowCode"),
            "nutrientSpreadingCode": daily_state.get("nutrientSpreadingCode"),
            "irrigationReadinessCode": daily_state.get("irrigationReadinessCode"),
            "scoutPriorityCode": daily_state.get("scoutPriorityCode"),
        },
        "overlay": {
            "sprayBlocked": _overlay_blocked(
                passport.get("overlayFacts") or [],
                as_of_date=as_of_date,
                blocked_codes=_SPRAY_BLOCKING_OVERLAYS,
            ),
            "nutrientBlocked": _overlay_blocked(
                passport.get("overlayFacts") or [],
                as_of_date=as_of_date,
                blocked_codes=_NUTRIENT_BLOCKING_OVERLAYS,
            ),
            "irrigationBlocked": _overlay_blocked(
                passport.get("overlayFacts") or [],
                as_of_date=as_of_date,
                blocked_codes=_IRRIGATION_BLOCKING_OVERLAYS,
            ),
        },
        "candidate": {},
    }
    if candidate_authorization is not None:
        decision_code = str(candidate_authorization.get("decisionCode") or "").strip()
        if decision_code:
            facts["candidate"]["authorizationDecisionCode"] = decision_code
    return facts


def _lookup_fact_value(facts: dict[str, Any], fact_key: str) -> tuple[bool, Any]:
    current: Any = facts
    for part in fact_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    if current in {None, ""}:
        return False, None
    return True, current


def _as_number(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _append_unique(items: list[str], value: Optional[str]) -> None:
    normalized = str(value or "").strip()
    if normalized and normalized not in items:
        items.append(normalized)


def _append_unique_many(items: list[str], values: Iterable[Any]) -> None:
    for value in values:
        _append_unique(items, str(value or "").strip())


def _prefer_non_unknown_text(*values: Any) -> Optional[str]:
    normalized = [str(value or "").strip() for value in values if str(value or "").strip()]
    for value in normalized:
        if value.lower() != "unknown":
            return value
    return normalized[0] if normalized else None


def _daily_fact_text(daily_state: dict[str, Any], *keys: str) -> Optional[str]:
    facts = daily_state.get("factsJson") if isinstance(daily_state.get("factsJson"), dict) else {}
    if not isinstance(facts, dict):
        return None
    for key in keys:
        value = str(facts.get(key) or "").strip()
        if value:
            return value
    return None


def _field_passport_ready(passport: dict[str, Any], as_of_date: date) -> bool:
    return bool(
        _current_authority_links(passport.get("officialLinks") or [], as_of_date)
        and str(passport.get("complianceGeometryRef") or "").strip()
        and isinstance(passport.get("dailyState"), dict)
    )


def _daily_metric(daily_state: dict[str, Any], *keys: str) -> Optional[float]:
    facts = daily_state.get("factsJson") if isinstance(daily_state.get("factsJson"), dict) else {}
    if not isinstance(facts, dict):
        return None
    for key in keys:
        value = _as_number(facts.get(key))
        if value is not None:
            return value
    return None


def _daily_bool(daily_state: dict[str, Any], *keys: str) -> Optional[bool]:
    facts = daily_state.get("factsJson") if isinstance(daily_state.get("factsJson"), dict) else {}
    if not isinstance(facts, dict):
        return None
    for key in keys:
        value = facts.get(key)
        if isinstance(value, bool):
            return value
    return None


def _latest_by_group(
    rows: list[dict[str, Any]],
    *,
    group_key: str,
    time_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        group_value = str(row.get(group_key) or "").strip()
        if not group_value:
            continue
        existing = latest.get(group_value)
        if existing is None:
            latest[group_value] = row
            continue
        current_dt = _parse_iso_datetime(row.get(time_fields[0]))
        if current_dt is None and len(time_fields) > 1:
            current_dt = _parse_iso_datetime(row.get(time_fields[1]))
        existing_dt = _parse_iso_datetime(existing.get(time_fields[0]))
        if existing_dt is None and len(time_fields) > 1:
            existing_dt = _parse_iso_datetime(existing.get(time_fields[1]))
        if existing_dt is None or (current_dt is not None and current_dt > existing_dt):
            latest[group_value] = row
    return list(latest.values())


def _sorted_items_desc(rows: Iterable[dict[str, Any]], *time_fields: str) -> list[dict[str, Any]]:
    def _sort_key(row: dict[str, Any]) -> datetime:
        for field_name in time_fields:
            parsed = _parse_iso_datetime(row.get(field_name))
            if parsed is not None:
                return parsed
        return datetime.min.replace(tzinfo=timezone.utc)

    return sorted(
        [row for row in rows if isinstance(row, dict)],
        key=_sort_key,
        reverse=True,
    )


def _map_disease_relevance_status(row: dict[str, Any]) -> str:
    case_status = str(row.get("caseStatus") or "").strip().lower()
    health_risk = str(row.get("healthRiskClass") or "").strip().lower()
    if case_status == "resolved":
        return "low"
    if health_risk in {"high", "very_high"} or case_status == "confirmed":
        return "high"
    if health_risk == "medium" or case_status == "probable":
        return "elevated"
    if case_status == "suspected" or health_risk == "low":
        return "watch"
    return "unknown"


def _map_weather_signal_status(*, leaf_wetness_hours: Optional[float]) -> str:
    if leaf_wetness_hours is None:
        return "unknown"
    if leaf_wetness_hours >= 8:
        return "supporting"
    if leaf_wetness_hours > 0:
        return "neutral"
    return "contradicting"


def _map_scouting_evidence_status(row: dict[str, Any]) -> str:
    assessment_type = str(row.get("assessmentType") or "").strip().lower()
    if assessment_type in {"field_scouting", "lab_test", "expert_judgement"}:
        return "present"
    if assessment_type:
        return "unknown"
    return "missing"


def _map_eo_context_status(
    *,
    daily_state: dict[str, Any],
    assessment_type: Optional[str] = None,
) -> str:
    if str(assessment_type or "").strip().lower() == "remote_sensing":
        return "supporting"
    eo_anomaly_flag = daily_state.get("eoAnomalyFlag")
    if eo_anomaly_flag is None:
        eo_anomaly_flag = _daily_bool(daily_state, "eoAnomalyFlag")
    if eo_anomaly_flag is True:
        return "supporting"
    if eo_anomaly_flag is False:
        return "neutral"
    return "unknown"


def _map_recommended_next_step(value: Optional[str]) -> str:
    normalized = str(value or "").strip().lower()
    if normalized == "monitor":
        return "monitor"
    if normalized == "sample_and_test":
        return "scout"
    if normalized == "treat_now":
        return "prepare-treatment"
    if normalized == "no_action":
        return "none"
    if normalized == "escalate":
        return "candidate-check"
    return "candidate-check"


def _active_overlay_rows(passport: dict[str, Any], as_of_date: date) -> list[dict[str, Any]]:
    return [
        item
        for item in (passport.get("overlayFacts") or [])
        if isinstance(item, dict) and _interval_active(item, as_of_date)
    ]


def _active_overlay_codes(passport: dict[str, Any], as_of_date: date) -> set[str]:
    return {
        str(item.get("overlayCode") or "").strip()
        for item in _active_overlay_rows(passport, as_of_date)
        if str(item.get("overlayCode") or "").strip()
    }


def _map_overlay_context_status(overlay_codes: set[str]) -> str:
    water_protection = "water_protection_zone" in overlay_codes
    flood_hazard = "flood_hazard" in overlay_codes
    if water_protection and flood_hazard:
        return "multi-regime"
    if water_protection:
        return "waterProtection"
    if flood_hazard:
        return "floodHazard"
    return "none"


def _map_terrain_status(daily_state: dict[str, Any]) -> str:
    ponding_prone = _daily_bool(daily_state, "pondingProneFlag", "pondingFlag")
    if ponding_prone is True:
        return "depression"
    slope_pct = _daily_metric(daily_state, "slopePct", "terrainSlopePct", "fieldSlopePct")
    if slope_pct is None:
        return "unknown"
    if slope_pct >= 12:
        return "steep"
    if slope_pct >= 5:
        return "moderate"
    return "flat"


def _map_drought_context_status(row: Optional[dict[str, Any]]) -> str:
    if not isinstance(row, dict) or not row:
        return "unknown"
    frequency_value = _as_number(row.get("frequencyValue"))
    frequency_kind = str(row.get("frequencyKindCode") or "").strip().lower()
    if frequency_value is None:
        return "unknown"
    if frequency_kind == "annual_probability":
        if frequency_value >= 0.25:
            return "regional-elevated"
        if frequency_value > 0:
            return "regional-watch"
        return "none"
    if frequency_kind == "percentile":
        if frequency_value >= 80:
            return "regional-elevated"
        if frequency_value >= 60:
            return "regional-watch"
        return "none"
    if frequency_kind == "expected_occurrences_per_year":
        if frequency_value >= 2:
            return "regional-elevated"
        if frequency_value > 0:
            return "regional-watch"
        return "none"
    return "regional-watch" if frequency_value > 0 else "none"


def _map_flood_context_status(
    *,
    row: Optional[dict[str, Any]],
    overlay_codes: set[str],
    daily_state: dict[str, Any],
) -> str:
    flood_watch = _daily_bool(daily_state, "floodWatchFlag", "surfaceFloodWatchFlag")
    if "flood_hazard" in overlay_codes:
        return "elevated"
    if not isinstance(row, dict) or not row:
        if flood_watch is True:
            return "watch"
        return "unknown"
    frequency_value = _as_number(row.get("frequencyValue"))
    frequency_kind = str(row.get("frequencyKindCode") or "").strip().lower()
    if frequency_value is None:
        return "watch" if flood_watch is True else "unknown"
    if frequency_kind == "annual_probability":
        if frequency_value >= 0.2:
            return "elevated"
        if frequency_value > 0:
            return "watch"
        return "none"
    if frequency_kind == "percentile":
        if frequency_value >= 75:
            return "elevated"
        if frequency_value >= 50:
            return "watch"
        return "none"
    if frequency_kind == "expected_occurrences_per_year":
        if frequency_value >= 1:
            return "elevated"
        if frequency_value > 0:
            return "watch"
        return "none"
    return "watch" if frequency_value > 0 or flood_watch is True else "none"


def _map_soil_water_proxy_status(
    *,
    daily_state: dict[str, Any],
    soil_moisture_rows: list[dict[str, Any]],
    precipitation_mm_24h: Optional[float],
) -> str:
    latest_soil_moisture = _latest_item(soil_moisture_rows, "observedAt", "createdAt") or {}
    moisture_pct = _as_number(latest_soil_moisture.get("moistureValue"))
    moisture_unit = str(latest_soil_moisture.get("moistureUnit") or "").strip().lower()
    if moisture_pct is not None and moisture_unit in {"pct_vwc", "%", "pct"}:
        if moisture_pct >= 35:
            return "saturated"
        if moisture_pct >= 28:
            return "wet"
        if moisture_pct >= 18:
            return "balanced"
        return "drying"

    ponding_prone = _daily_bool(daily_state, "pondingProneFlag", "pondingFlag")
    if precipitation_mm_24h is not None:
        if precipitation_mm_24h >= 15:
            return "saturated"
        if precipitation_mm_24h >= 6 or ponding_prone is True:
            return "wet"
        if precipitation_mm_24h == 0:
            return "drying"
        return "balanced"

    return "unknown"


def _map_water_deficit_proxy_status(
    *,
    precipitation_mm_24h: Optional[float],
    reference_et_recent_mm: Optional[float],
    soil_water_proxy_status: str,
    irrigation_assessment_row: Optional[dict[str, Any]],
) -> str:
    if isinstance(irrigation_assessment_row, dict) and irrigation_assessment_row:
        stress_risk = str(irrigation_assessment_row.get("stressRiskClass") or "").strip().lower()
        if stress_risk in {"critical", "high"}:
            return "high"
        if stress_risk == "medium":
            return "moderate"
        if stress_risk == "low":
            return "low"

    if reference_et_recent_mm is not None and precipitation_mm_24h is not None:
        deficit_delta = reference_et_recent_mm - precipitation_mm_24h
        if deficit_delta >= 8:
            return "high"
        if deficit_delta >= 3:
            return "moderate"
        return "low"

    if soil_water_proxy_status == "drying":
        return "moderate"
    if soil_water_proxy_status in {"wet", "saturated"}:
        return "low"
    return "unknown"


def _map_support_dataset_status(
    *,
    reference_et_recent_mm: Optional[float],
    reference_et_forecast_mm: Optional[float],
    drought_row: Optional[dict[str, Any]],
    flood_row: Optional[dict[str, Any]],
) -> str:
    has_et = reference_et_recent_mm is not None or reference_et_forecast_mm is not None
    has_drought = bool(drought_row)
    has_flood = bool(flood_row)
    if has_et and (has_drought or has_flood):
        return "multi-source"
    if has_drought or has_flood:
        return "regional-drought"
    if has_et:
        return "regional-et"
    return "none"


def _map_recent_weather_status(
    *,
    precipitation_mm_24h: Optional[float],
    flood_context_status: str,
) -> str:
    if precipitation_mm_24h is None and flood_context_status == "unknown":
        return "unknown"
    if precipitation_mm_24h is not None and precipitation_mm_24h >= 10:
        return "adverse"
    if flood_context_status == "elevated":
        return "adverse"
    if precipitation_mm_24h is not None and precipitation_mm_24h == 0:
        return "supporting"
    return "neutral"


def _map_sensor_support_status(
    *,
    soil_moisture_rows: list[dict[str, Any]],
    soil_water_proxy_status: str,
) -> str:
    latest_soil_moisture = _latest_item(soil_moisture_rows, "observedAt", "createdAt") or {}
    moisture_pct = _as_number(latest_soil_moisture.get("moistureValue"))
    if moisture_pct is None:
        return "none"
    if soil_water_proxy_status in {"wet", "saturated"} and moisture_pct < 18:
        return "contradicting"
    if soil_water_proxy_status == "drying" and moisture_pct >= 28:
        return "contradicting"
    return "supporting"


def _map_irrigation_urgency_level(
    *,
    water_deficit_proxy_status: str,
    irrigation_assessment_row: Optional[dict[str, Any]],
) -> str:
    if isinstance(irrigation_assessment_row, dict) and irrigation_assessment_row:
        recommended_action = str(irrigation_assessment_row.get("recommendedAction") or "").strip().lower()
        if recommended_action == "irrigate_now":
            return "high"
        if recommended_action == "irrigate_within_24h":
            return "elevated"
        if recommended_action == "monitor_no_irrigation":
            return "low"
    if water_deficit_proxy_status == "high":
        return "high"
    if water_deficit_proxy_status == "moderate":
        return "elevated"
    if water_deficit_proxy_status == "low":
        return "low"
    return "unknown"


def _max_signal_level(*levels: str) -> str:
    chosen = "unknown"
    for level in levels:
        normalized = str(level or "").strip().lower() or "unknown"
        if _OUTCOME_RANK.get(normalized, -1) > _OUTCOME_RANK.get(chosen, -1):
            chosen = normalized
    return chosen


def _max_scout_priority(*priorities: str) -> str:
    chosen = "none"
    for priority in priorities:
        normalized = str(priority or "").strip().lower() or "unknown"
        if _SCOUT_PRIORITY_RANK.get(normalized, -1) > _SCOUT_PRIORITY_RANK.get(chosen, -1):
            chosen = normalized
    return chosen


def build_field_water_stewardship_context(
    *,
    passport: dict[str, Any],
    as_of_date: date,
    irrigation_need_assessments: list[dict[str, Any]],
    climate_hazard_profiles: list[dict[str, Any]],
    soil_moisture_observations: list[dict[str, Any]],
) -> dict[str, Any]:
    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    crop_instance_uri = str((passport.get("cropContext") or {}).get("cropInstanceUri") or "").strip() or None
    active_overlay_codes = _active_overlay_codes(passport, as_of_date)
    overlay_status = _map_overlay_context_status(active_overlay_codes)
    nutrient_blocked = _overlay_blocked(
        passport.get("overlayFacts") or [],
        as_of_date=as_of_date,
        blocked_codes=_NUTRIENT_BLOCKING_OVERLAYS,
    )
    irrigation_blocked = _overlay_blocked(
        passport.get("overlayFacts") or [],
        as_of_date=as_of_date,
        blocked_codes=_IRRIGATION_BLOCKING_OVERLAYS,
    )
    precipitation_mm_24h = _daily_metric(daily_state, "precipitationMm24h", "rainMm24h", "rainMm", "rainfallMm")
    reference_et_recent_mm = _daily_metric(
        daily_state,
        "referenceEtRecentMm",
        "referenceEtMm24h",
        "referenceEtMm",
    )
    reference_et_forecast_mm = _daily_metric(
        daily_state,
        "referenceEtForecastMm",
        "forecastReferenceEtMm",
        "referenceEtForecast3dMm",
    )
    latest_irrigation_assessment = (
        _latest_item(irrigation_need_assessments, "assessedAt", "recordedAt", "createdAt") or {}
    )
    drought_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "drought"
        ],
        "recordedAt",
        "createdAt",
    )
    flood_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "flood"
        ],
        "recordedAt",
        "createdAt",
    )
    terrain_status = _map_terrain_status(daily_state)
    soil_water_proxy_status = _map_soil_water_proxy_status(
        daily_state=daily_state,
        soil_moisture_rows=soil_moisture_observations,
        precipitation_mm_24h=precipitation_mm_24h,
    )
    water_deficit_proxy_status = _map_water_deficit_proxy_status(
        precipitation_mm_24h=precipitation_mm_24h,
        reference_et_recent_mm=reference_et_recent_mm,
        soil_water_proxy_status=soil_water_proxy_status,
        irrigation_assessment_row=latest_irrigation_assessment,
    )
    drought_context_status = _map_drought_context_status(drought_row)
    flood_context_status = _map_flood_context_status(
        row=flood_row,
        overlay_codes=active_overlay_codes,
        daily_state=daily_state,
    )
    support_dataset_status = _map_support_dataset_status(
        reference_et_recent_mm=reference_et_recent_mm,
        reference_et_forecast_mm=reference_et_forecast_mm,
        drought_row=drought_row,
        flood_row=flood_row,
    )
    recent_weather_status = _map_recent_weather_status(
        precipitation_mm_24h=precipitation_mm_24h,
        flood_context_status=flood_context_status,
    )
    sensor_support_status = _map_sensor_support_status(
        soil_moisture_rows=soil_moisture_observations,
        soil_water_proxy_status=soil_water_proxy_status,
    )

    required_evidence: list[str] = []
    trace_refs: list[str] = []
    evidence_refs = collect_passport_evidence_uris(passport)

    if not _current_authority_links(passport.get("officialLinks") or [], as_of_date):
        _append_unique(required_evidence, "field_authority_link")
    if not str(passport.get("complianceGeometryRef") or "").strip():
        _append_unique(required_evidence, "field_geometry_snapshot")
    if not daily_state:
        _append_unique(required_evidence, "field_condition_daily")
    if precipitation_mm_24h is None:
        _append_unique(required_evidence, "recent_precipitation_context")
    if reference_et_recent_mm is None and not latest_irrigation_assessment:
        _append_unique(required_evidence, "reference_et_context")

    if latest_irrigation_assessment:
        _append_unique(trace_refs, str(latest_irrigation_assessment.get("irrigationNeedAssessmentUri") or "").strip())
        _append_unique(trace_refs, str(latest_irrigation_assessment.get("rulesetRef") or "").strip())
        _append_unique(trace_refs, str(latest_irrigation_assessment.get("recommendedIrrigationPlanUri") or "").strip())
        _append_unique_many(
            evidence_refs,
            [
                latest_irrigation_assessment.get("soilMoistureObservationRef"),
                latest_irrigation_assessment.get("weatherObservationRef"),
                latest_irrigation_assessment.get("cropStageObservationRef"),
            ],
        )
    if drought_row:
        _append_unique(trace_refs, str(drought_row.get("profileUri") or "").strip())
        _append_unique(trace_refs, str(drought_row.get("dataSourceRef") or "").strip())
        _append_unique(trace_refs, str(drought_row.get("methodRef") or "").strip())
    if flood_row:
        _append_unique(trace_refs, str(flood_row.get("profileUri") or "").strip())
        _append_unique(trace_refs, str(flood_row.get("dataSourceRef") or "").strip())
        _append_unique(trace_refs, str(flood_row.get("methodRef") or "").strip())
    latest_soil_moisture = _latest_item(soil_moisture_observations, "observedAt", "createdAt") or {}
    if latest_soil_moisture:
        _append_unique(trace_refs, str(latest_soil_moisture.get("observationUri") or "").strip())

    runoff_reasons: list[str] = []
    leaching_reasons: list[str] = []
    ponding_reasons: list[str] = []
    flood_reasons: list[str] = []
    irrigation_reasons: list[str] = []
    nitrate_reasons: list[str] = []
    manure_reasons: list[str] = []

    runoff_level = "low"
    if flood_context_status == "elevated" or soil_water_proxy_status == "saturated":
        runoff_level = "high"
    elif (
        (precipitation_mm_24h is not None and precipitation_mm_24h >= 8)
        or terrain_status == "steep"
        or overlay_status == "waterProtection"
    ):
        runoff_level = "elevated"
    elif overlay_status == "floodHazard" or soil_water_proxy_status == "wet":
        runoff_level = "watch"
    if precipitation_mm_24h is not None and precipitation_mm_24h >= 8:
        _append_unique(runoff_reasons, "recent_rain_elevated")
    if terrain_status in {"steep", "moderate"}:
        _append_unique(runoff_reasons, f"terrain_status:{terrain_status}")
    if overlay_status == "waterProtection":
        _append_unique(runoff_reasons, "overlay_water_protection")
    if soil_water_proxy_status in {"wet", "saturated"}:
        _append_unique(runoff_reasons, f"soil_water:{soil_water_proxy_status}")
    if flood_context_status in {"watch", "elevated"}:
        _append_unique(runoff_reasons, f"flood_context:{flood_context_status}")

    leaching_level = "low"
    if soil_water_proxy_status == "saturated" or (precipitation_mm_24h is not None and precipitation_mm_24h >= 12):
        leaching_level = "high"
    elif soil_water_proxy_status == "wet" or (precipitation_mm_24h is not None and precipitation_mm_24h >= 6):
        leaching_level = "elevated"
    elif overlay_status == "waterProtection":
        leaching_level = "watch"
    if soil_water_proxy_status in {"wet", "saturated"}:
        _append_unique(leaching_reasons, f"soil_water:{soil_water_proxy_status}")
    if precipitation_mm_24h is not None and precipitation_mm_24h >= 6:
        _append_unique(leaching_reasons, "recent_rain_supporting")
    if overlay_status == "waterProtection":
        _append_unique(leaching_reasons, "overlay_water_protection")

    ponding_level = "low"
    if terrain_status == "depression" and (
        soil_water_proxy_status == "saturated"
        or (precipitation_mm_24h is not None and precipitation_mm_24h >= 6)
    ):
        ponding_level = "high"
    elif terrain_status == "depression" or soil_water_proxy_status == "wet":
        ponding_level = "elevated"
    elif flood_context_status == "watch":
        ponding_level = "watch"
    if terrain_status == "depression":
        _append_unique(ponding_reasons, "terrain_depression")
    if soil_water_proxy_status in {"wet", "saturated"}:
        _append_unique(ponding_reasons, f"soil_water:{soil_water_proxy_status}")

    flood_level = "low"
    if overlay_status == "floodHazard" or flood_context_status == "elevated":
        flood_level = "high"
    elif flood_context_status == "watch" or ponding_level in {"watch", "elevated"}:
        flood_level = "elevated"
    if overlay_status in {"floodHazard", "multi-regime"}:
        _append_unique(flood_reasons, "overlay_flood_hazard")
    if flood_context_status in {"watch", "elevated"}:
        _append_unique(flood_reasons, f"flood_context:{flood_context_status}")
    if ponding_level in {"watch", "elevated", "high"}:
        _append_unique(flood_reasons, f"ponding_risk:{ponding_level}")

    irrigation_urgency_level = _map_irrigation_urgency_level(
        water_deficit_proxy_status=water_deficit_proxy_status,
        irrigation_assessment_row=latest_irrigation_assessment,
    )
    if water_deficit_proxy_status in {"moderate", "high"}:
        _append_unique(irrigation_reasons, f"water_deficit:{water_deficit_proxy_status}")
    if drought_context_status in {"regional-watch", "regional-elevated"}:
        _append_unique(irrigation_reasons, f"drought_context:{drought_context_status}")
    if latest_irrigation_assessment:
        _append_unique(
            irrigation_reasons,
            f"irrigation_recommendation:{latest_irrigation_assessment.get('recommendedAction')}",
        )

    nitrate_timing_level = "unknown"
    nutrient_code = str(daily_state.get("nutrientSpreadingCode") or "").strip().lower()
    if nutrient_code == "closed" or nutrient_blocked or _max_signal_level(runoff_level, leaching_level, flood_level) == "high":
        nitrate_timing_level = "high"
    elif nutrient_code == "caution" or _max_signal_level(runoff_level, leaching_level, flood_level) == "elevated":
        nitrate_timing_level = "elevated"
    elif nutrient_code == "open" and _max_signal_level(runoff_level, leaching_level, flood_level) == "watch":
        nitrate_timing_level = "watch"
    elif nutrient_code == "open":
        nitrate_timing_level = "low"
    if nutrient_code:
        _append_unique(nitrate_reasons, f"nutrient_window:{nutrient_code}")
    if nutrient_blocked:
        _append_unique(nitrate_reasons, "overlay_nutrient_restriction")
    _append_unique(nitrate_reasons, f"runoff_risk:{runoff_level}")
    _append_unique(nitrate_reasons, f"leaching_risk:{leaching_level}")
    if overlay_status == "waterProtection":
        _append_unique(nitrate_reasons, "overlay_water_protection")

    manure_timing_level = "unknown"
    if nutrient_code == "closed" or nutrient_blocked or soil_water_proxy_status in {"wet", "saturated"}:
        manure_timing_level = "high"
    elif nutrient_code == "caution" or _max_signal_level(runoff_level, leaching_level, flood_level) in {"watch", "elevated"}:
        manure_timing_level = "elevated"
    elif nutrient_code == "open":
        manure_timing_level = "low"
    if nutrient_code:
        _append_unique(manure_reasons, f"nutrient_window:{nutrient_code}")
    if soil_water_proxy_status in {"wet", "saturated"}:
        _append_unique(manure_reasons, f"soil_water:{soil_water_proxy_status}")
    if nutrient_blocked:
        _append_unique(manure_reasons, "overlay_nutrient_restriction")
    if overlay_status == "waterProtection":
        _append_unique(manure_reasons, "overlay_water_protection")

    jurisdiction_status = "clear"
    if nutrient_blocked or irrigation_blocked or overlay_status == "floodHazard":
        jurisdiction_status = "blocked"
    elif overlay_status in {"waterProtection", "multi-regime"}:
        jurisdiction_status = "restricted"

    signal_rows = [
        {
            "signalType": "runoffRisk",
            "signalLevel": runoff_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "delay" if runoff_level in {"elevated", "high"} else "inspect" if runoff_level == "watch" else "none",
            "reasonCodes": runoff_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "leachingRisk",
            "signalLevel": leaching_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "delay" if leaching_level in {"elevated", "high"} else "inspect" if leaching_level == "watch" else "none",
            "reasonCodes": leaching_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "pondingRisk",
            "signalLevel": ponding_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "inspect" if ponding_level in {"watch", "elevated", "high"} else "none",
            "reasonCodes": ponding_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "floodRisk",
            "signalLevel": flood_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "delay" if flood_level in {"watch", "elevated", "high"} else "none",
            "reasonCodes": flood_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "irrigationUrgency",
            "signalLevel": irrigation_urgency_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "irrigate" if irrigation_urgency_level in {"elevated", "high"} else "monitor",
            "reasonCodes": irrigation_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "nitrateTimingRisk",
            "signalLevel": nitrate_timing_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "delay" if nitrate_timing_level in {"watch", "elevated", "high"} else "prepare-application",
            "reasonCodes": nitrate_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
        {
            "signalType": "manureTimingRisk",
            "signalLevel": manure_timing_level,
            "jurisdictionStatus": jurisdiction_status,
            "overlayStatus": overlay_status,
            "terrainStatus": terrain_status,
            "recentWeatherStatus": recent_weather_status,
            "waterBalanceStatus": soil_water_proxy_status,
            "sensorSupportStatus": sensor_support_status,
            "recommendedNextStep": "delay" if manure_timing_level in {"watch", "elevated", "high"} else "prepare-application",
            "reasonCodes": manure_reasons,
            "traceRefs": trace_refs,
            "evidenceRefs": evidence_refs,
        },
    ]
    signal_rows = [
        item
        for item in signal_rows
        if str(item.get("signalLevel") or "").strip().lower() != "unknown"
    ]
    top_signals = sorted(
        signal_rows,
        key=lambda row: (-_OUTCOME_RANK.get(str(row.get("signalLevel") or "unknown").strip().lower(), -1), str(row.get("signalType") or "")),
    )[:4]

    facts = build_fact_snapshot(passport, as_of_date=as_of_date)
    facts["overlay"]["waterProtectionActive"] = "water_protection_zone" in active_overlay_codes
    facts["overlay"]["floodHazardActive"] = "flood_hazard" in active_overlay_codes
    facts["water"] = {
        "soilWaterProxyStatus": soil_water_proxy_status,
        "waterDeficitProxyStatus": water_deficit_proxy_status,
        "droughtContextStatus": drought_context_status,
        "floodContextStatus": flood_context_status,
        "supportDatasetStatus": support_dataset_status,
    }
    facts["signals"] = {
        "runoffRiskLevel": runoff_level,
        "leachingRiskLevel": leaching_level,
        "pondingRiskLevel": ponding_level,
        "floodRiskLevel": flood_level,
        "irrigationUrgencyLevel": irrigation_urgency_level,
        "nitrateTimingRiskLevel": nitrate_timing_level,
        "manureTimingRiskLevel": manure_timing_level,
    }

    recommended_actions: list[str] = []
    for signal in top_signals:
        next_step = str(signal.get("recommendedNextStep") or "").strip()
        if next_step and next_step != "none":
            _append_unique(recommended_actions, next_step)

    overlay_summary = "No current stewardship overlay is active for this field."
    if overlay_status == "waterProtection":
        overlay_summary = "A water-protection overlay applies to this field."
    elif overlay_status == "floodHazard":
        overlay_summary = "A flood-hazard overlay applies to this field."
    elif overlay_status == "multi-regime":
        overlay_summary = "Multiple water and flood stewardship overlays apply to this field."

    recent_weather_summary = str(daily_state.get("weatherSummaryText") or "").strip() or None
    if recent_weather_summary is None and precipitation_mm_24h is not None:
        recent_weather_summary = f"Recent precipitation over 24h: {precipitation_mm_24h:.1f} mm."

    water_balance_summary = {
        "soilWaterProxyStatus": soil_water_proxy_status,
        "waterDeficitProxyStatus": water_deficit_proxy_status,
        "droughtContextStatus": drought_context_status,
        "floodContextStatus": flood_context_status,
        "supportDatasetStatus": support_dataset_status,
        "summary": (
            f"Soil-water proxy is {soil_water_proxy_status}; deficit proxy is {water_deficit_proxy_status}."
            if soil_water_proxy_status != "unknown" or water_deficit_proxy_status != "unknown"
            else "Water-balance support is incomplete for the selected date."
        ),
    }

    return {
        "fieldUri": str((passport.get("identity") or {}).get("fieldUri") or "").strip(),
        "activeCropInstanceUri": crop_instance_uri,
        "facts": facts,
        "requiredEvidence": required_evidence,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
        "topSignals": top_signals,
        "allSignals": signal_rows,
        "recommendedActions": recommended_actions,
        "regionalProfiles": {
            "droughtProfile": dict(drought_row) if isinstance(drought_row, dict) else None,
            "floodProfile": dict(flood_row) if isinstance(flood_row, dict) else None,
        },
        "overlayContext": {
            "status": overlay_status,
            "summary": overlay_summary,
        },
        "recentWeatherSummary": {
            "status": recent_weather_status,
            "summary": recent_weather_summary,
        },
        "waterBalanceSummary": water_balance_summary,
        "dailyState": daily_state,
        "nutrientBlocked": nutrient_blocked,
        "irrigationBlocked": irrigation_blocked,
        "latestIrrigationAssessment": latest_irrigation_assessment,
    }


def build_projection_findings_from_rule_results(
    rule_results: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    blocking: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for item in rule_results:
        result = str(item.get("result") or "").strip().lower()
        severity = str(item.get("severity") or "").strip().lower()
        if result == "pass":
            continue
        finding = {
            "code": str(item.get("reasonCode") or item.get("factKey") or "rule_triggered").strip(),
            "severity": "block" if result == "fail" and severity == "hard" else "warn",
            "message": str(item.get("message") or item.get("label") or "Rule triggered.").strip(),
            "source": str(item.get("category") or item.get("factKey") or "").strip() or None,
        }
        if finding["severity"] == "block":
            blocking.append(finding)
        else:
            warnings.append(finding)
    return blocking, warnings


def build_field_water_stewardship_projection(
    *,
    context: dict[str, Any],
    rulepack: dict[str, Any],
) -> dict[str, Any]:
    facts = context.get("facts") or {}
    nitrogen_eval = evaluate_rules(
        rulepack=rulepack,
        evaluation_type="spread_nitrogen",
        facts=facts,
    )
    manure_eval = evaluate_rules(
        rulepack=rulepack,
        evaluation_type="spread_manure",
        facts=facts,
    )
    irrigate_eval = evaluate_rules(
        rulepack=rulepack,
        evaluation_type="irrigate",
        facts=facts,
    )
    flood_risk_level = str(((context.get("facts") or {}).get("signals") or {}).get("floodRiskLevel") or "unknown")
    flood_reason_codes = next(
        (
            list(item.get("reasonCodes") or [])
            for item in context.get("allSignals") or []
            if str(item.get("signalType") or "").strip() == "floodRisk"
        ),
        [],
    )
    delay_decision = "unknown"
    if flood_risk_level == "high":
        delay_decision = "block"
    elif flood_risk_level in {"watch", "elevated"}:
        delay_decision = "warn"
    elif flood_risk_level == "low":
        delay_decision = "allow"

    return {
        "dailyDecisions": [
            {
                "actionType": "spreadNitrogen",
                "decision": nitrogen_eval.get("outcomeCode") or "unknown",
                "reasonCodes": nitrogen_eval.get("reasonCodes") or [],
            },
            {
                "actionType": "spreadManure",
                "decision": manure_eval.get("outcomeCode") or "unknown",
                "reasonCodes": manure_eval.get("reasonCodes") or [],
            },
            {
                "actionType": "irrigate",
                "decision": irrigate_eval.get("outcomeCode") or "unknown",
                "reasonCodes": irrigate_eval.get("reasonCodes") or [],
            },
            {
                "actionType": "delayForFloodRisk",
                "decision": delay_decision,
                "reasonCodes": flood_reason_codes,
            },
        ],
        "topSignals": context.get("topSignals") or [],
        "overlayContext": context.get("overlayContext") or {},
        "recentWeatherSummary": context.get("recentWeatherSummary") or {},
        "waterBalanceSummary": context.get("waterBalanceSummary") or {},
        "recommendedActions": context.get("recommendedActions") or [],
        "requiredEvidence": context.get("requiredEvidence") or [],
        "traceRefs": context.get("traceRefs") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
    }


def build_field_nitrogen_application_check_projection(
    *,
    context: dict[str, Any],
    action_type: str,
    rulepack: dict[str, Any],
) -> dict[str, Any]:
    evaluation_type = "spread_nitrogen" if action_type == "spreadNitrogen" else "spread_manure"
    evaluation_result = evaluate_rules(
        rulepack=rulepack,
        evaluation_type=evaluation_type,
        facts=context.get("facts") or {},
    )
    blocking_findings, warning_findings = build_projection_findings_from_rule_results(
        evaluation_result.get("ruleResults") or []
    )
    runoff_leaching_level = _max_signal_level(
        str((((context.get("facts") or {}).get("signals") or {}).get("runoffRiskLevel")) or "unknown"),
        str((((context.get("facts") or {}).get("signals") or {}).get("leachingRiskLevel")) or "unknown"),
    )
    recent_weather_status = str(((context.get("recentWeatherSummary") or {}).get("status")) or "unknown")
    weather_summary = str(((context.get("recentWeatherSummary") or {}).get("summary")) or "").strip() or None
    jurisdiction_status = "clear"
    if context.get("nutrientBlocked"):
        jurisdiction_status = "blocked"
    elif str(((context.get("overlayContext") or {}).get("status")) or "") in {"waterProtection", "multi-regime"}:
        jurisdiction_status = "restricted"

    return {
        "decision": evaluation_result.get("outcomeCode") or "unknown",
        "blockingFindings": blocking_findings,
        "warningFindings": warning_findings,
        "jurisdictionSummary": {
            "status": jurisdiction_status,
            "summary": str(((context.get("overlayContext") or {}).get("summary")) or "").strip() or None,
        },
        "runoffLeachingSummary": {
            "status": runoff_leaching_level,
            "summary": (
                "Runoff or leaching risk is elevated for the selected action."
                if runoff_leaching_level in {"elevated", "high"}
                else "No elevated runoff or leaching warning was inferred."
                if runoff_leaching_level == "low"
                else None
            ),
        },
        "weatherWindowSummary": {
            "status": recent_weather_status,
            "summary": weather_summary,
        },
        "requiredEvidence": context.get("requiredEvidence") or [],
        "traceRefs": context.get("traceRefs") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
        "evaluationResult": evaluation_result,
    }


def build_field_irrigation_readiness_projection(
    *,
    context: dict[str, Any],
    rulepack: dict[str, Any],
) -> dict[str, Any]:
    evaluation_result = evaluate_rules(
        rulepack=rulepack,
        evaluation_type="irrigate",
        facts=context.get("facts") or {},
    )
    latest_irrigation_assessment = context.get("latestIrrigationAssessment") or {}
    recommended_action = str(latest_irrigation_assessment.get("recommendedAction") or "").strip().lower()
    urgency_status = "unknown"
    if recommended_action == "irrigate_now":
        urgency_status = "urgent"
    elif recommended_action == "irrigate_within_24h":
        urgency_status = "recommended"
    elif recommended_action == "monitor_no_irrigation":
        urgency_status = "monitor"
    else:
        water_deficit_status = str(((context.get("waterBalanceSummary") or {}).get("waterDeficitProxyStatus")) or "unknown")
        if water_deficit_status == "high":
            urgency_status = "urgent"
        elif water_deficit_status == "moderate":
            urgency_status = "recommended"
        elif water_deficit_status == "low":
            urgency_status = "monitor"

    if evaluation_result.get("outcomeCode") == "block" and urgency_status in {"recommended", "urgent"}:
        urgency_status = "monitor"

    flood_ponding_status = _max_signal_level(
        str((((context.get("facts") or {}).get("signals") or {}).get("floodRiskLevel")) or "unknown"),
        str((((context.get("facts") or {}).get("signals") or {}).get("pondingRiskLevel")) or "unknown"),
    )
    flood_summary = None
    if flood_ponding_status in {"elevated", "high"}:
        flood_summary = "Flood or ponding conditions make irrigation hard to justify today."
    elif flood_ponding_status == "low":
        flood_summary = "No strong flood or ponding contradiction was detected."

    required_evidence = list(context.get("requiredEvidence") or [])
    if not latest_irrigation_assessment and str(((context.get("waterBalanceSummary") or {}).get("waterDeficitProxyStatus")) or "unknown") == "unknown":
        _append_unique(required_evidence, "irrigation_need_assessment")

    return {
        "decision": evaluation_result.get("outcomeCode") or "unknown",
        "urgencyStatus": urgency_status,
        "waterBalanceSummary": context.get("waterBalanceSummary") or {},
        "droughtContextSummary": {
            "status": str(((context.get("waterBalanceSummary") or {}).get("droughtContextStatus")) or "unknown"),
            "summary": (
                "Regional drought support is elevated for the selected field."
                if str(((context.get("waterBalanceSummary") or {}).get("droughtContextStatus")) or "") == "regional-elevated"
                else "Regional drought support is present but not elevated."
                if str(((context.get("waterBalanceSummary") or {}).get("droughtContextStatus")) or "") == "regional-watch"
                else None
            ),
        },
        "floodPondingSummary": {
            "status": flood_ponding_status,
            "summary": flood_summary,
        },
        "requiredEvidence": required_evidence,
        "traceRefs": context.get("traceRefs") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
        "evaluationResult": evaluation_result,
    }


def build_field_spray_window_projection(
    *,
    passport: dict[str, Any],
    as_of_date: date,
    leaf_wetness_observations: list[dict[str, Any]],
    agrometeorological_observations: list[dict[str, Any]],
) -> dict[str, Any]:
    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    agrometeorological_state = (
        passport.get("agrometeorologicalState")
        if isinstance(passport.get("agrometeorologicalState"), dict)
        else {}
    )
    blocking_findings: list[dict[str, Any]] = []
    warning_findings: list[dict[str, Any]] = []
    required_evidence: list[str] = []
    trace_refs: list[str] = []
    evidence_refs = collect_passport_evidence_uris(passport)

    leaf_wetness = _latest_item(leaf_wetness_observations, "intervalEnd", "intervalStart", "createdAt") or {}
    agrometeorological_observation = (
        _latest_item(agrometeorological_observations, "observedAt", "timeSupportEnd", "createdAt")
        or agrometeorological_state
        or {}
    )
    leaf_wetness_hours = _as_number(leaf_wetness.get("wetnessDurationHours"))
    if leaf_wetness_hours is None:
        _append_unique(required_evidence, "leaf_wetness_duration_observation")
    else:
        _append_unique_many(evidence_refs, leaf_wetness.get("evidenceUris") or [])
    agromet_observation_uri = str(agrometeorological_observation.get("observationUri") or "").strip()
    if agromet_observation_uri:
        _append_unique(trace_refs, agromet_observation_uri)

    daily_wind_speed_mps = _daily_metric(daily_state, "windSpeedMps")
    agromet_wind_speed_mps = _as_number(agrometeorological_observation.get("windSpeedMps"))
    wind_speed_mps = daily_wind_speed_mps if daily_wind_speed_mps is not None else agromet_wind_speed_mps
    wind_source = "field_condition_daily" if daily_wind_speed_mps is not None else (
        "agrometeorological_station_observation" if agromet_wind_speed_mps is not None else None
    )

    daily_precipitation_mm_24h = _daily_metric(daily_state, "precipitationMm24h", "rainMm24h", "rainMm")
    agromet_rainfall_mm = _as_number(agrometeorological_observation.get("rainfallMm"))
    precipitation_mm_24h = (
        daily_precipitation_mm_24h
        if daily_precipitation_mm_24h is not None
        else agromet_rainfall_mm
    )

    daily_relative_humidity_pct = _daily_metric(daily_state, "relativeHumidityPct", "humidityPct")
    agromet_relative_humidity_pct = _as_number(agrometeorological_observation.get("relativeHumidityPct"))
    relative_humidity_pct = (
        daily_relative_humidity_pct
        if daily_relative_humidity_pct is not None
        else agromet_relative_humidity_pct
    )
    eo_anomaly_flag = daily_state.get("eoAnomalyFlag")
    if eo_anomaly_flag is None:
        eo_anomaly_flag = _daily_bool(daily_state, "eoAnomalyFlag")

    if not _current_authority_links(passport.get("officialLinks") or [], as_of_date):
        blocking_findings.append(
            {
                "code": "missing_current_authority_link",
                "severity": "block",
                "message": "The field passport has no current authority link for the selected date.",
                "source": "field_passport",
            }
        )
        _append_unique(required_evidence, "field_authority_link")
    if not str(passport.get("complianceGeometryRef") or "").strip():
        blocking_findings.append(
            {
                "code": "missing_compliance_geometry",
                "severity": "block",
                "message": "The field passport does not resolve a compliance geometry for this field.",
                "source": "field_passport",
            }
        )
        _append_unique(required_evidence, "field_geometry_snapshot")
    if not daily_state:
        blocking_findings.append(
            {
                "code": "missing_daily_condition",
                "severity": "block",
                "message": "No daily field condition was available for the selected date.",
                "source": "field_condition_daily",
            }
        )
        _append_unique(required_evidence, "field_condition_daily")

    if _overlay_blocked(
        passport.get("overlayFacts") or [],
        as_of_date=as_of_date,
        blocked_codes=_SPRAY_BLOCKING_OVERLAYS,
    ):
        blocking_findings.append(
            {
                "code": "overlay_spray_restriction",
                "severity": "block",
                "message": "An active spray restriction overlay blocks spraying for this field.",
                "source": "field_overlay_fact",
            }
        )

    spray_window_code = str(daily_state.get("sprayWindowCode") or "").strip().lower()
    if spray_window_code == "closed":
        blocking_findings.append(
            {
                "code": "daily_spray_window_closed",
                "severity": "block",
                "message": "The daily spray window is currently closed.",
                "source": "field_condition_daily",
            }
        )
    elif spray_window_code == "caution":
        warning_findings.append(
            {
                "code": "daily_spray_window_caution",
                "severity": "warn",
                "message": "The daily spray window currently requires caution.",
                "source": "field_condition_daily",
            }
        )
    elif spray_window_code in {"", "unknown"}:
        _append_unique(required_evidence, "field_condition_daily")

    if leaf_wetness_hours is not None and leaf_wetness_hours >= 8:
        warning_findings.append(
            {
                "code": "leaf_wetness_elevated",
                "severity": "warn",
                "message": "Recent leaf wetness suggests elevated canopy moisture.",
                "source": "leaf_wetness_duration_observation",
            }
        )

    if wind_speed_mps is not None and wind_speed_mps >= 6:
        warning_findings.append(
            {
                "code": "wind_speed_elevated",
                "severity": "warn",
                "message": "Observed wind speed is elevated for a clean spray window.",
                "source": wind_source or "field_condition_daily",
            }
        )

    if blocking_findings:
        decision = "unknown" if not _field_passport_ready(passport, as_of_date) else "block"
    elif warning_findings:
        decision = "warn"
    elif spray_window_code == "open":
        decision = "allow"
    else:
        decision = "unknown"

    surface_status = "unknown"
    if precipitation_mm_24h is not None:
        if precipitation_mm_24h >= 5:
            surface_status = "wet"
        elif precipitation_mm_24h > 0:
            surface_status = "damp"
        else:
            surface_status = "dry"

    drift_status = "unknown"
    if wind_speed_mps is not None:
        if wind_speed_mps >= 6:
            drift_status = "high"
        elif wind_speed_mps >= 3:
            drift_status = "moderate"
        else:
            drift_status = "low"

    advisory_status = "unknown"
    if leaf_wetness_hours is not None:
        advisory_status = "watch" if leaf_wetness_hours >= 8 else "neutral"

    return {
        "decision": decision,
        "blockingFindings": blocking_findings,
        "warningFindings": warning_findings,
        "weatherMetrics": {
            "windSpeedMps": wind_speed_mps,
            "precipitationMm24h": precipitation_mm_24h,
            "relativeHumidityPct": relative_humidity_pct,
            "leafWetnessHours": leaf_wetness_hours,
            "eoAnomalyFlag": eo_anomaly_flag,
        },
        "surfaceConditionSummary": {
            "status": surface_status,
            "summary": (
                str(daily_state.get("weatherSummaryText") or "").strip()
                or (
                    f"Agrometeorological proxy from {agrometeorological_observation.get('stationUri')} "
                    f"at {agrometeorological_observation.get('observedAt')}"
                    if agromet_observation_uri
                    else None
                )
            ),
        },
        "driftRiskSummary": {
            "status": drift_status,
            "summary": (
                "Wind conditions increase drift risk."
                if drift_status == "high"
                else "No elevated drift signal was detected."
                if drift_status == "low"
                else None
            ),
        },
        "advisoryContextSummary": {
            "status": advisory_status,
            "summary": (
                "Leaf wetness suggests canopy moisture may shorten the practical spray window."
                if advisory_status == "watch"
                else "No plant-health weather caution was inferred from current evidence."
                if advisory_status == "neutral"
                else "Official plant-health advisory ingest is not yet integrated for this field."
            ),
        },
        "requiredEvidence": required_evidence,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def build_field_plant_health_relevance_projection(
    *,
    passport: dict[str, Any],
    as_of_date: date,
    disease_assessments: list[dict[str, Any]],
    leaf_wetness_observations: list[dict[str, Any]],
) -> dict[str, Any]:
    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    signals: list[dict[str, Any]] = []
    required_evidence: list[str] = ["official_plant_health_advisory_fact"]
    trace_refs: list[str] = []
    evidence_refs = collect_passport_evidence_uris(passport)

    leaf_wetness = _latest_item(leaf_wetness_observations, "intervalEnd", "intervalStart", "createdAt") or {}
    leaf_wetness_hours = _as_number(leaf_wetness.get("wetnessDurationHours"))
    if leaf_wetness_hours is None:
        _append_unique(required_evidence, "leaf_wetness_duration_observation")
    else:
        _append_unique_many(evidence_refs, leaf_wetness.get("evidenceUris") or [])

    latest_assessments = _latest_by_group(
        [row for row in disease_assessments if isinstance(row, dict)],
        group_key="pathogenCode",
        time_fields=("assessedAt", "recordedAt"),
    )
    for assessment in latest_assessments:
        assessment_uri = str(assessment.get("assessmentUri") or "").strip()
        if assessment_uri:
            _append_unique(trace_refs, assessment_uri)
        _append_unique(trace_refs, str(assessment.get("caseUri") or "").strip())
        _append_unique_many(evidence_refs, assessment.get("evidenceUris") or [])

        relevance_status = _map_disease_relevance_status(assessment)
        signal_reasons: list[str] = []
        _append_unique(signal_reasons, f"case_status:{assessment.get('caseStatus')}")
        _append_unique(signal_reasons, f"health_risk:{assessment.get('healthRiskClass')}")
        _append_unique_many(signal_reasons, assessment.get("missingCriticalData") or [])
        if _map_eo_context_status(daily_state=daily_state, assessment_type=assessment.get("assessmentType")) == "supporting":
            _append_unique(signal_reasons, "eo_context_supporting")
        if leaf_wetness_hours is not None and leaf_wetness_hours >= 8:
            _append_unique(signal_reasons, "leaf_wetness_supporting")

        signals.append(
            {
                "hazardCode": str(assessment.get("pathogenCode") or "").strip() or "unknown_pathogen",
                "hazardLabel": str(assessment.get("pathogenCode") or "").strip() or "Unknown pathogen",
                "relevanceStatus": relevance_status,
                "phenologyStatus": "unknown",
                "officialAdvisoryStatus": "unknown",
                "weatherSignalStatus": _map_weather_signal_status(
                    leaf_wetness_hours=leaf_wetness_hours
                ),
                "scoutingEvidenceStatus": _map_scouting_evidence_status(assessment),
                "eoContextStatus": _map_eo_context_status(
                    daily_state=daily_state,
                    assessment_type=assessment.get("assessmentType"),
                ),
                "recommendedNextStep": _map_recommended_next_step(
                    assessment.get("interventionRecommendationCode")
                ),
                "reasonCodes": signal_reasons,
                "traceRefs": [
                    value
                    for value in [assessment_uri, str(assessment.get("caseUri") or "").strip()]
                    if value
                ],
                "evidenceRefs": [
                    str(value).strip()
                    for value in (assessment.get("evidenceUris") or [])
                    if str(value).strip()
                ],
            }
        )

    if not signals:
        scout_priority = str(daily_state.get("scoutPriorityCode") or "").strip().lower()
        eo_context_status = _map_eo_context_status(daily_state=daily_state)
        relevance_status = "unknown"
        recommended_next_step = "monitor"
        reason_codes: list[str] = []
        if scout_priority in {"urgent", "high"} or eo_context_status == "supporting":
            relevance_status = "elevated"
            recommended_next_step = "scout"
            _append_unique(reason_codes, "field_scout_priority_elevated")
        elif scout_priority in {"medium", "low"}:
            relevance_status = "watch" if scout_priority == "medium" else "low"
            _append_unique(reason_codes, f"field_scout_priority:{scout_priority}")
        if leaf_wetness_hours is not None and leaf_wetness_hours >= 8:
            relevance_status = "elevated" if relevance_status != "unknown" else "watch"
            _append_unique(reason_codes, "leaf_wetness_supporting")
        if eo_context_status == "supporting":
            _append_unique(reason_codes, "eo_context_supporting")

        if reason_codes:
            signals.append(
                {
                    "hazardCode": "field_health_attention",
                    "hazardLabel": "Field health attention",
                    "relevanceStatus": relevance_status,
                    "phenologyStatus": "unknown",
                    "officialAdvisoryStatus": "unknown",
                    "weatherSignalStatus": _map_weather_signal_status(
                        leaf_wetness_hours=leaf_wetness_hours
                    ),
                    "scoutingEvidenceStatus": "missing",
                    "eoContextStatus": eo_context_status,
                    "recommendedNextStep": recommended_next_step,
                    "reasonCodes": reason_codes,
                    "traceRefs": [],
                    "evidenceRefs": [],
                }
            )
            _append_unique(required_evidence, "disease_case_assessment")

    if not signals:
        _append_unique(required_evidence, "disease_case_assessment")

    summary_status = "unknown"
    for signal in signals:
        candidate_status = str(signal.get("relevanceStatus") or "unknown").strip().lower()
        if _OUTCOME_RANK.get(candidate_status, -1) > _OUTCOME_RANK.get(summary_status, -1):
            summary_status = candidate_status

    return {
        "summaryStatus": summary_status,
        "signals": signals,
        "requiredEvidence": required_evidence,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def _map_eo_quality_status(
    *,
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoQualityStatus") or "").strip().lower()
    if explicit in {"usable", "partial", "poor", "unusable", "unknown"}:
        return explicit

    if not latest_observation:
        return "unknown"

    cloud_cover = _as_number(latest_observation.get("cloudCoverPct"))
    confidence = _as_number(latest_observation.get("confidenceScore"))
    quality_flag = str(latest_observation.get("qualityFlag") or "").strip().lower()

    if cloud_cover is not None and cloud_cover >= 90:
        return "unusable"
    if quality_flag == "suspect" or (cloud_cover is not None and cloud_cover >= 70):
        return "poor"
    if quality_flag == "good" and (cloud_cover is None or cloud_cover <= 25) and (
        confidence is None or confidence >= 0.75
    ):
        return "usable"
    if quality_flag in {"good", "estimated"}:
        return "partial"
    return "unknown"


def _map_cloud_or_noise_status(
    *,
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoCloudOrNoiseStatus") or "").strip().lower()
    if explicit in {"clear", "limited", "obstructed", "not_applicable", "unknown"}:
        return explicit

    if not latest_observation:
        return "unknown"

    cloud_cover = _as_number(latest_observation.get("cloudCoverPct"))
    if cloud_cover is None:
        return "unknown"
    if cloud_cover >= 70:
        return "obstructed"
    if cloud_cover >= 25:
        return "limited"
    return "clear"


def _map_change_context(
    *,
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
    previous_observation: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoChangeContext") or "").strip().lower()
    if explicit in {"stable", "shifted", "unknown"}:
        return explicit

    if not latest_observation or not previous_observation:
        return "unknown"

    latest_value = _as_number(latest_observation.get("indexValue"))
    previous_value = _as_number(previous_observation.get("indexValue"))
    if latest_value is None or previous_value is None:
        return "unknown"
    if abs(latest_value - previous_value) >= 0.12:
        return "shifted"
    return "stable"


def _map_eo_moisture_proxy_status(
    *,
    passport: dict[str, Any],
    daily_state: dict[str, Any],
    water_context: Optional[dict[str, Any]],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoMoistureProxyStatus") or "").strip().lower()
    if explicit in {"dry", "balanced", "wet", "saturated", "unknown"}:
        return explicit

    if isinstance(water_context, dict):
        water_balance = water_context.get("waterBalanceSummary") or {}
        water_status = str(water_balance.get("soilWaterProxyStatus") or "").strip().lower()
        if water_status in {"dry", "balanced", "wet", "saturated"}:
            return water_status

    flood_watch = _daily_bool(daily_state, "floodWatchFlag")
    ponding_prone = _daily_bool(daily_state, "pondingProneFlag")
    precipitation_mm_24h = _daily_metric(daily_state, "precipitationMm24h", "rainMm24h", "rainMm")
    if flood_watch is True or ponding_prone is True:
        return "saturated"
    if precipitation_mm_24h is not None and precipitation_mm_24h >= 10:
        return "wet"
    if precipitation_mm_24h is not None and precipitation_mm_24h <= 1:
        return "balanced"
    if passport.get("dailyState"):
        return "unknown"
    return "unknown"


def _map_eo_heterogeneity_status(
    *,
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoHeterogeneityStatus") or "").strip().lower()
    if explicit in {"uniform", "patchy", "highly_variable", "unknown"}:
        return explicit

    if not latest_observation:
        return "unknown"

    if _daily_bool(daily_state, "eoAnomalyFlag") is True:
        scout_priority_code = str(daily_state.get("scoutPriorityCode") or "").strip().lower()
        if scout_priority_code in {"high", "urgent"}:
            return "highly_variable"
        return "patchy"
    return "uniform"


def _parse_bbch_code(value: Any) -> Optional[int]:
    text = str(value or "").strip()
    if len(text) == 2 and text.isdigit():
        return int(text)
    return None


def _map_eo_phenology_proxy_status(
    *,
    passport: dict[str, Any],
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
    latest_scouting: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoPhenologyProxyStatus") or "").strip().lower()
    if explicit in {"behind", "aligned", "ahead", "unknown"}:
        return explicit

    if not latest_observation:
        return "unknown"

    crop_context = passport.get("cropContext") or {}
    if not (crop_context.get("seasonCode") or crop_context.get("cropTypeUri") or crop_context.get("declaredUseCode")):
        return "unknown"

    latest_value = _as_number(latest_observation.get("indexValue"))
    bbch_code = _parse_bbch_code(latest_scouting.get("bbchCode"))
    if latest_value is None or bbch_code is None:
        return "unknown"
    if bbch_code >= 30 and latest_value < 0.35:
        return "behind"
    if bbch_code <= 19 and latest_value > 0.75:
        return "ahead"
    return "aligned"


def _map_support_context_status(
    *,
    passport: dict[str, Any],
    scouting_observations: list[dict[str, Any]],
    pest_trap_observations: list[dict[str, Any]],
    water_context: Optional[dict[str, Any]],
) -> str:
    has_ground = bool(scouting_observations or pest_trap_observations)
    support_dataset_status = str(
        (((water_context or {}).get("waterBalanceSummary") or {}).get("supportDatasetStatus")) or ""
    ).strip().lower()
    has_water = support_dataset_status not in {"", "unknown", "none"}
    crop_context = passport.get("cropContext") or {}
    has_passport_context = bool(
        crop_context.get("seasonCode")
        or crop_context.get("cropTypeUri")
        or crop_context.get("declaredUseCode")
        or passport.get("complianceGeometryRef")
    )
    if has_ground and has_water:
        return "multi-source"
    if has_ground:
        return "ground-evidence"
    if has_water:
        return "water-context"
    if has_passport_context:
        return "passport-context"
    return "none"


def _map_cross_sensor_status(
    *,
    daily_state: dict[str, Any],
    latest_observation: dict[str, Any],
) -> str:
    explicit = str(_daily_fact_text(daily_state, "eoCrossSensorStatus") or "").strip().lower()
    if explicit in {"unconfirmed", "optical_only", "radar_only", "cross_confirmed", "unknown"}:
        return explicit

    if latest_observation:
        return "optical_only"
    if _daily_bool(daily_state, "eoAnomalyFlag") is True:
        return "unconfirmed"
    return "unknown"


def _map_scouting_support_level(latest_scouting: dict[str, Any]) -> str:
    if not latest_scouting:
        return "unknown"

    severity_class = str(latest_scouting.get("severityClass") or "").strip().lower()
    severity_pct = _as_number(latest_scouting.get("severityPct"))
    incidence_pct = _as_number(latest_scouting.get("incidencePct"))
    if severity_class in {"high", "severe"} or (severity_pct is not None and severity_pct >= 20) or (
        incidence_pct is not None and incidence_pct >= 30
    ):
        return "high"
    if severity_class == "medium" or (severity_pct is not None and severity_pct >= 8) or (
        incidence_pct is not None and incidence_pct >= 12
    ):
        return "elevated"
    return "watch"


def _map_trap_pressure_level(latest_pest_trap: dict[str, Any]) -> str:
    if not latest_pest_trap:
        return "unknown"

    trap_count = _as_number(latest_pest_trap.get("trapCount"))
    if trap_count is None:
        return "unknown"
    if trap_count >= 20:
        return "high"
    if trap_count >= 10:
        return "elevated"
    if trap_count > 0:
        return "watch"
    return "low"


def _map_signal_persistence_status(
    *,
    signal_type: str,
    quality_status: str,
    previous_quality_status: str,
    latest_observation: dict[str, Any],
    previous_observation: dict[str, Any],
) -> str:
    if not previous_observation:
        return "single"

    if signal_type == "dataQualityGap":
        if quality_status in {"poor", "unusable"} and previous_quality_status in {"poor", "unusable"}:
            return "persistent"
        return "repeated"

    latest_value = _as_number(latest_observation.get("indexValue"))
    previous_value = _as_number(previous_observation.get("indexValue"))
    if latest_value is not None and previous_value is not None and latest_value < 0.5 and previous_value < 0.5:
        return "persistent"
    return "repeated"


def _map_daily_scout_priority(daily_state: dict[str, Any]) -> str:
    scout_priority_code = str(daily_state.get("scoutPriorityCode") or "").strip().lower()
    mapping = {
        "unknown": "none",
        "low": "low",
        "medium": "normal",
        "high": "high",
        "urgent": "urgent",
    }
    return mapping.get(scout_priority_code, "none")


def _bump_scout_priority(priority: str) -> str:
    normalized = str(priority or "none").strip().lower()
    if normalized == "none":
        return "low"
    if normalized == "low":
        return "normal"
    if normalized == "normal":
        return "high"
    if normalized == "high":
        return "urgent"
    return normalized


def _make_field_anomaly_signal(
    *,
    signal_type: str,
    signal_level: str,
    quality_status: str,
    latest_observation: dict[str, Any],
    previous_observation: dict[str, Any],
    daily_state: dict[str, Any],
    latest_scouting: dict[str, Any],
    latest_pest_trap: dict[str, Any],
    phenology_status: str,
    recommended_next_step: str,
    trace_refs: list[str],
    evidence_refs: list[str],
    reason_codes: list[str],
) -> dict[str, Any]:
    priority = "none"
    if signal_type != "dataQualityGap":
        if signal_level == "high":
            priority = "high"
        elif signal_level == "elevated":
            priority = "normal"
        elif signal_level == "watch":
            priority = "low"
        priority = _max_scout_priority(priority, _map_daily_scout_priority(daily_state))

    scouting_support_level = _map_scouting_support_level(latest_scouting)
    trap_pressure_level = _map_trap_pressure_level(latest_pest_trap)
    if signal_type != "dataQualityGap" and scouting_support_level in {"elevated", "high"}:
        priority = _bump_scout_priority(priority)
        _append_unique(reason_codes, "scouting_ground_truth_present")
    if signal_type in {"growthLag", "abnormalHeterogeneity"} and trap_pressure_level in {"elevated", "high"}:
        priority = _bump_scout_priority(priority)
        _append_unique(reason_codes, "pest_trap_pressure_supporting")

    return {
        "signalType": signal_type,
        "signalLevel": signal_level,
        "persistenceStatus": _map_signal_persistence_status(
            signal_type=signal_type,
            quality_status=quality_status,
            previous_quality_status=_map_eo_quality_status(
                daily_state=daily_state,
                latest_observation=previous_observation,
            ),
            latest_observation=latest_observation,
            previous_observation=previous_observation,
        ),
        "crossSensorStatus": _map_cross_sensor_status(
            daily_state=daily_state,
            latest_observation=latest_observation,
        ),
        "phenologyStatus": phenology_status,
        "scoutPriority": priority,
        "recommendedNextStep": recommended_next_step,
        "reasonCodes": reason_codes,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def build_field_eo_context(
    *,
    passport: dict[str, Any],
    as_of_date: date,
    remote_sensing_observations: list[dict[str, Any]],
    crop_scouting_observations: list[dict[str, Any]],
    pest_trap_observations: list[dict[str, Any]],
    water_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    del as_of_date
    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    crop_context = passport.get("cropContext") if isinstance(passport.get("cropContext"), dict) else {}
    active_crop_instance_uri = str(crop_context.get("cropInstanceUri") or "").strip() or None

    remote_rows = _sorted_items_desc(remote_sensing_observations, "observedAt", "recordedAt", "createdAt")
    scouting_rows = _sorted_items_desc(crop_scouting_observations, "observedAt", "createdAt")
    pest_rows = _sorted_items_desc(pest_trap_observations, "observedAt", "createdAt")
    latest_observation = remote_rows[0] if remote_rows else {}
    previous_observation = remote_rows[1] if len(remote_rows) > 1 else {}
    latest_scouting = scouting_rows[0] if scouting_rows else {}
    latest_pest_trap = pest_rows[0] if pest_rows else {}

    trace_refs: list[str] = []
    evidence_refs = collect_passport_evidence_uris(passport)
    required_evidence: list[str] = []
    evidence_gaps: list[str] = []

    if isinstance(water_context, dict):
        _append_unique_many(trace_refs, water_context.get("traceRefs") or [])
        _append_unique_many(evidence_refs, water_context.get("evidenceRefs") or [])

    latest_observation_uri = str(latest_observation.get("observationUri") or "").strip()
    latest_source_product_ref = str(latest_observation.get("sourceProductRef") or "").strip()
    _append_unique(trace_refs, latest_observation_uri)
    _append_unique(trace_refs, latest_source_product_ref)

    latest_scouting_uri = str(latest_scouting.get("observationUri") or "").strip()
    _append_unique(trace_refs, latest_scouting_uri)
    _append_unique(trace_refs, str(latest_scouting.get("diseaseCaseUri") or "").strip())
    _append_unique_many(evidence_refs, latest_scouting.get("evidenceRefs") or [])

    latest_pest_uri = str(latest_pest_trap.get("observationUri") or "").strip()
    _append_unique(trace_refs, latest_pest_uri)

    quality_status = _map_eo_quality_status(
        daily_state=daily_state,
        latest_observation=latest_observation,
    )
    cloud_or_noise_status = _map_cloud_or_noise_status(
        daily_state=daily_state,
        latest_observation=latest_observation,
    )
    change_context = _map_change_context(
        daily_state=daily_state,
        latest_observation=latest_observation,
        previous_observation=previous_observation,
    )
    moisture_proxy_status = _map_eo_moisture_proxy_status(
        passport=passport,
        daily_state=daily_state,
        water_context=water_context,
    )
    heterogeneity_status = _map_eo_heterogeneity_status(
        daily_state=daily_state,
        latest_observation=latest_observation,
    )
    phenology_proxy_status = _map_eo_phenology_proxy_status(
        passport=passport,
        daily_state=daily_state,
        latest_observation=latest_observation,
        latest_scouting=latest_scouting,
    )
    support_context_status = _map_support_context_status(
        passport=passport,
        scouting_observations=scouting_rows,
        pest_trap_observations=pest_rows,
        water_context=water_context,
    )
    coverage_pct = _daily_metric(daily_state, "eoCoveragePct")
    if coverage_pct is None:
        cloud_cover_pct = _as_number(latest_observation.get("cloudCoverPct"))
        if cloud_cover_pct is not None:
            coverage_pct = max(0.0, min(100.0, 100.0 - cloud_cover_pct))

    observation_type = "optical_stats" if latest_observation else "unknown"
    explicit_observation_type = str(_daily_fact_text(daily_state, "eoObservationType") or "").strip().lower()
    if explicit_observation_type in {"optical_stats", "radar_stats", "multi_sensor_summary"}:
        observation_type = explicit_observation_type

    sensor_set = "optical" if latest_observation else "unknown"
    explicit_sensor_set = str(_daily_fact_text(daily_state, "eoSensorSet") or "").strip().lower()
    if explicit_sensor_set in {"optical", "radar", "multi", "unknown"}:
        sensor_set = explicit_sensor_set

    latest_index_value = _as_number(latest_observation.get("indexValue"))
    previous_index_value = _as_number(previous_observation.get("indexValue"))
    delta_value = None
    if latest_index_value is not None and previous_index_value is not None:
        delta_value = latest_index_value - previous_index_value

    if not latest_observation:
        _append_unique(required_evidence, "remote_sensing_index_observation")
        _append_unique(evidence_gaps, "remote_sensing_index_observation")
    if not active_crop_instance_uri or not (
        crop_context.get("declarationSnapshotUri")
        or crop_context.get("seasonCode")
        or crop_context.get("cropTypeUri")
        or crop_context.get("declaredUseCode")
    ):
        _append_unique(required_evidence, "field_declaration_snapshot")
        _append_unique(evidence_gaps, "field_declaration_snapshot")
    if not latest_scouting:
        _append_unique(evidence_gaps, "crop_scouting_signs")

    data_quality_summary = {
        "status": quality_status,
        "summary": (
            f"Latest EO observation is {quality_status} with {cloud_or_noise_status} cloud/noise context."
            if latest_observation
            else "No recent EO parcel observation is available for this field."
        ),
    }

    stage_status = phenology_proxy_status
    if stage_status == "unknown" and not latest_scouting:
        _append_unique(evidence_gaps, "crop_scouting_signs")

    if quality_status == "usable" and stage_status in {"aligned", "behind", "ahead"} and latest_scouting:
        confidence_status = "high"
    elif quality_status in {"usable", "partial"} and stage_status in {"aligned", "behind", "ahead"}:
        confidence_status = "medium"
    elif quality_status in {"partial", "poor"} or stage_status == "unknown":
        confidence_status = "low"
    else:
        confidence_status = "unknown"

    baseline_summary = {
        "status": stage_status,
        "summary": (
            f"Phenology proxy is {stage_status} against current crop and scouting context."
            if stage_status in {"aligned", "behind", "ahead"}
            else "Phenology alignment is not decision-ready from current EO context."
        ),
    }

    flood_or_ponding_level = _max_signal_level(
        str(((((water_context or {}).get("facts") or {}).get("signals") or {}).get("floodRiskLevel")) or "unknown"),
        str(((((water_context or {}).get("facts") or {}).get("signals") or {}).get("pondingRiskLevel")) or "unknown"),
    )
    eo_anomaly_flag = _daily_bool(daily_state, "eoAnomalyFlag")
    signal_rows: list[dict[str, Any]] = []

    if not latest_observation or quality_status in {"poor", "unusable"} or cloud_or_noise_status == "obstructed":
        signal_level = "high" if (not latest_observation or quality_status == "unusable") else "elevated"
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="dataQualityGap",
                signal_level=signal_level,
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="reacquire",
                trace_refs=[value for value in [latest_observation_uri, latest_source_product_ref] if value],
                evidence_refs=[],
                reason_codes=[
                    code
                    for code in [
                        "missing_remote_observation" if not latest_observation else None,
                        f"quality_status:{quality_status}" if quality_status != "unknown" else None,
                        f"cloud_or_noise:{cloud_or_noise_status}" if cloud_or_noise_status != "unknown" else None,
                    ]
                    if code
                ],
            )
        )

    if latest_observation and (
        phenology_proxy_status == "behind"
        or (latest_index_value is not None and latest_index_value < 0.45)
        or (delta_value is not None and delta_value <= -0.12)
        or eo_anomaly_flag is True
    ):
        signal_level = "watch"
        if (latest_index_value is not None and latest_index_value < 0.32) or (
            delta_value is not None and delta_value <= -0.22
        ):
            signal_level = "high"
        elif phenology_proxy_status == "behind" or (delta_value is not None and delta_value <= -0.15):
            signal_level = "elevated"
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="growthLag",
                signal_level=signal_level,
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="scout_now" if signal_level in {"elevated", "high"} else "scout_later",
                trace_refs=[
                    value
                    for value in [
                        latest_observation_uri,
                        latest_source_product_ref,
                        latest_scouting_uri,
                    ]
                    if value
                ],
                evidence_refs=list(latest_scouting.get("evidenceRefs") or []),
                reason_codes=[
                    code
                    for code in [
                        f"phenology_proxy:{phenology_proxy_status}" if phenology_proxy_status != "unknown" else None,
                        "eo_anomaly_flag" if eo_anomaly_flag is True else None,
                        "negative_index_shift" if delta_value is not None and delta_value <= -0.12 else None,
                    ]
                    if code
                ],
            )
        )

    if latest_observation and delta_value is not None and delta_value <= -0.2 and quality_status in {"usable", "partial"}:
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="disturbanceSuspicion",
                signal_level="high" if delta_value <= -0.28 else "elevated",
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="scout_now",
                trace_refs=[value for value in [latest_observation_uri, latest_source_product_ref] if value],
                evidence_refs=[],
                reason_codes=["abrupt_index_drop"],
            )
        )

    if heterogeneity_status in {"patchy", "highly_variable"}:
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="abnormalHeterogeneity",
                signal_level="high" if heterogeneity_status == "highly_variable" else "elevated",
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="compare_history" if change_context == "stable" else "scout_later",
                trace_refs=[value for value in [latest_observation_uri, latest_source_product_ref] if value],
                evidence_refs=[],
                reason_codes=[
                    f"heterogeneity_status:{heterogeneity_status}",
                    f"change_context:{change_context}" if change_context != "unknown" else "change_context:unknown",
                ],
            )
        )

    if moisture_proxy_status in {"wet", "saturated"} and (
        flood_or_ponding_level in {"watch", "elevated", "high"}
        or eo_anomaly_flag is True
        or _daily_bool(daily_state, "floodWatchFlag") is True
    ):
        signal_level = "high" if moisture_proxy_status == "saturated" or flood_or_ponding_level in {"elevated", "high"} else "elevated"
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="standingWaterSuspicion",
                signal_level=signal_level,
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="scout_now",
                trace_refs=[value for value in [latest_observation_uri, latest_source_product_ref] if value],
                evidence_refs=[],
                reason_codes=[
                    f"moisture_proxy:{moisture_proxy_status}",
                    f"flood_or_ponding:{flood_or_ponding_level}" if flood_or_ponding_level != "unknown" else None,
                ],
            )
        )

    if phenology_proxy_status in {"behind", "ahead"}:
        signal_rows.append(
            _make_field_anomaly_signal(
                signal_type="phenologyMismatch",
                signal_level="elevated" if phenology_proxy_status == "behind" else "watch",
                quality_status=quality_status,
                latest_observation=latest_observation,
                previous_observation=previous_observation,
                daily_state=daily_state,
                latest_scouting=latest_scouting,
                latest_pest_trap=latest_pest_trap,
                phenology_status=stage_status,
                recommended_next_step="compare_history" if latest_scouting else "scout_later",
                trace_refs=[
                    value
                    for value in [
                        latest_observation_uri,
                        latest_source_product_ref,
                        latest_scouting_uri,
                    ]
                    if value
                ],
                evidence_refs=list(latest_scouting.get("evidenceRefs") or []),
                reason_codes=[f"phenology_proxy:{phenology_proxy_status}"],
            )
        )

    signal_rows = [
        item
        for item in signal_rows
        if str(item.get("signalLevel") or "").strip().lower() != "unknown"
    ]
    top_signals = sorted(
        signal_rows,
        key=lambda row: (
            0 if str(row.get("recommendedNextStep") or "").strip() == "reacquire" else 1,
            -_SCOUT_PRIORITY_RANK.get(str(row.get("scoutPriority") or "none").strip().lower(), 0),
            -_OUTCOME_RANK.get(str(row.get("signalLevel") or "unknown").strip().lower(), -1),
            str(row.get("signalType") or ""),
        ),
    )[:4]

    scout_recommendation = "not_decision_ready"
    if any(str(item.get("recommendedNextStep") or "") == "reacquire" for item in top_signals):
        scout_recommendation = "reacquire"
    elif any(str(item.get("scoutPriority") or "") in {"urgent", "high"} for item in top_signals):
        scout_recommendation = "inspect_now"
    elif any(str(item.get("scoutPriority") or "") == "normal" for item in top_signals):
        scout_recommendation = "inspect_later"
    elif top_signals:
        scout_recommendation = "monitor"
    elif latest_observation:
        scout_recommendation = "monitor"

    return {
        "fieldUri": str((passport.get("identity") or {}).get("fieldUri") or "").strip(),
        "activeCropInstanceUri": active_crop_instance_uri,
        "observationSummary": {
            "observationType": observation_type,
            "sensorSet": sensor_set,
            "qualityStatus": quality_status,
            "cloudOrNoiseStatus": cloud_or_noise_status,
            "changeContext": change_context,
            "moistureProxyStatus": moisture_proxy_status,
            "heterogeneityStatus": heterogeneity_status,
            "phenologyProxyStatus": phenology_proxy_status,
            "supportContextStatus": support_context_status,
            "coveragePct": coverage_pct,
            "summary": (
                f"Latest {sensor_set} EO observation shows {quality_status} quality and {phenology_proxy_status} phenology proxy."
                if latest_observation
                else "No recent EO parcel observation is available."
            ),
        },
        "topSignals": top_signals,
        "allSignals": signal_rows,
        "dataQualitySummary": data_quality_summary,
        "phenologySummary": baseline_summary,
        "stageStatus": stage_status,
        "confidenceStatus": confidence_status,
        "baselineSummary": baseline_summary,
        "scoutRecommendation": scout_recommendation,
        "evidenceGaps": evidence_gaps,
        "requiredEvidence": required_evidence,
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def build_field_eo_anomaly_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "observationSummary": context.get("observationSummary") or {},
        "topSignals": context.get("topSignals") or [],
        "dataQualitySummary": context.get("dataQualitySummary") or {},
        "phenologySummary": context.get("phenologySummary") or {},
        "scoutRecommendation": context.get("scoutRecommendation") or "not_decision_ready",
        "requiredEvidence": context.get("requiredEvidence") or [],
        "traceRefs": context.get("traceRefs") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
    }


def build_field_phenology_status_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    contributing_signals = [
        item
        for item in context.get("allSignals") or []
        if str(item.get("signalType") or "").strip() in {"growthLag", "phenologyMismatch", "standingWaterSuspicion"}
    ]
    return {
        "stageStatus": context.get("stageStatus") or "unknown",
        "confidenceStatus": context.get("confidenceStatus") or "unknown",
        "baselineSummary": context.get("baselineSummary") or {},
        "contributingSignals": contributing_signals[:4],
        "evidenceGaps": context.get("evidenceGaps") or [],
        "traceRefs": context.get("traceRefs") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
    }


def _scout_queue_recommendation_rank(value: Any) -> int:
    return {
        "reacquire": 4,
        "inspect_now": 3,
        "inspect_later": 2,
        "monitor": 1,
        "not_decision_ready": 0,
    }.get(str(value or "").strip().lower(), -1)


def _confidence_rank(value: Any) -> int:
    return {
        "high": 3,
        "medium": 2,
        "low": 1,
        "unknown": 0,
    }.get(str(value or "").strip().lower(), 0)


def build_farm_scout_priority_queue_projection(
    *,
    farm_uri: str,
    as_of_date: date,
    field_contexts: list[dict[str, Any]],
) -> dict[str, Any]:
    queue_items: list[dict[str, Any]] = []
    trace_refs: list[str] = []
    evidence_refs: list[str] = []

    for item in field_contexts:
        field_row = item.get("fieldRow") if isinstance(item.get("fieldRow"), dict) else {}
        context = item.get("context") if isinstance(item.get("context"), dict) else {}
        field_uri = str(field_row.get("uri") or context.get("fieldUri") or "").strip()
        if not field_uri:
            continue

        top_signals = [signal for signal in context.get("topSignals") or [] if isinstance(signal, dict)]
        top_signal = top_signals[0] if top_signals else {}
        scout_recommendation = str(context.get("scoutRecommendation") or "not_decision_ready").strip() or "not_decision_ready"
        scout_priority = str(top_signal.get("scoutPriority") or "unknown").strip() or "unknown"
        signal_level = str(top_signal.get("signalLevel") or "unknown").strip() or "unknown"
        confidence_status = str(context.get("confidenceStatus") or "unknown").strip() or "unknown"
        stage_status = str(context.get("stageStatus") or "unknown").strip() or "unknown"
        data_quality = context.get("dataQualitySummary") if isinstance(context.get("dataQualitySummary"), dict) else {}
        observation_quality_status = str(data_quality.get("status") or "unknown").strip() or "unknown"

        reason_codes: list[str] = []
        top_signal_types: list[str] = []
        for signal in top_signals[:4]:
            _append_unique(top_signal_types, str(signal.get("signalType") or "").strip())
            _append_unique_many(reason_codes, signal.get("reasonCodes") or [])
            _append_unique_many(trace_refs, signal.get("traceRefs") or [])
            _append_unique_many(evidence_refs, signal.get("evidenceRefs") or [])
        _append_unique_many(trace_refs, context.get("traceRefs") or [])
        _append_unique_many(evidence_refs, context.get("evidenceRefs") or [])

        queue_items.append(
            {
                "fieldUri": field_uri,
                "fieldLabel": str(field_row.get("label") or "").strip() or None,
                "fieldAreaHa": _as_number(field_row.get("areaHa")),
                "activeCropInstanceUri": str(context.get("activeCropInstanceUri") or "").strip() or None,
                "scoutRecommendation": scout_recommendation,
                "scoutPriority": scout_priority,
                "signalLevel": signal_level,
                "confidenceStatus": confidence_status,
                "stageStatus": stage_status,
                "observationQualityStatus": observation_quality_status,
                "topSignalTypes": top_signal_types,
                "reasonCodes": reason_codes,
                "requiredEvidence": list(context.get("requiredEvidence") or []),
                "traceRefs": list(context.get("traceRefs") or []),
                "evidenceRefs": list(context.get("evidenceRefs") or []),
            }
        )

    queue_items.sort(
        key=lambda row: (
            -_scout_queue_recommendation_rank(row.get("scoutRecommendation")),
            -_SCOUT_PRIORITY_RANK.get(str(row.get("scoutPriority") or "unknown").strip().lower(), -1),
            -_OUTCOME_RANK.get(str(row.get("signalLevel") or "unknown").strip().lower(), -1),
            -_confidence_rank(row.get("confidenceStatus")),
            str(row.get("fieldLabel") or row.get("fieldUri") or ""),
        )
    )
    for index, row in enumerate(queue_items, start=1):
        row["rank"] = index

    return {
        "farmUri": farm_uri,
        "asOfDate": as_of_date.isoformat(),
        "queueItems": queue_items,
        "rankingPolicyVersion": "si-field-eo-scout-queue-v1",
        "filters": {
            "includedRecommendations": [
                "reacquire",
                "inspect_now",
                "inspect_later",
                "monitor",
                "not_decision_ready",
            ],
        },
        "evidencePolicy": {
            "advisoryOnly": True,
            "reacquireOutranksScoutWhenEvidenceMissing": True,
            "requiredEvidenceField": "requiredEvidence",
        },
        "traceRefs": trace_refs,
        "evidenceRefs": evidence_refs,
    }


def _field_phase5_signal_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return (
        -_OUTCOME_RANK.get(str(row.get("signalLevel") or "unknown").strip().lower(), -1),
        -_SCOUT_PRIORITY_RANK.get(str(row.get("scoutPriority") or "none").strip().lower(), 0),
        str(row.get("signalType") or ""),
    )


def _context_status_to_signal_level(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"high", "urgent", "blocked"}:
        return "high"
    if normalized in {"elevated", "regional-elevated", "partial"}:
        return "elevated"
    if normalized in {"watch", "regional-watch", "medium"}:
        return "watch"
    if normalized in {"low", "none", "clear", "aligned", "ready"}:
        return "low"
    return "unknown"


def _field_phase5_local_signal(passport: dict[str, Any], water_context: dict[str, Any], eo_context: dict[str, Any]) -> tuple[Optional[dict[str, Any]], str]:
    local_candidates: list[dict[str, Any]] = []
    for item in eo_context.get("allSignals") or []:
        signal_type = str(item.get("signalType") or "").strip()
        if signal_type == "dataQualityGap":
            continue
        local_candidates.append(dict(item))
    for item in water_context.get("allSignals") or []:
        signal_type = str(item.get("signalType") or "").strip()
        if signal_type not in {"runoffRisk", "leachingRisk", "pondingRisk", "floodRisk", "irrigationUrgency"}:
            continue
        local_candidates.append(dict(item))

    if local_candidates:
        local_candidates.sort(key=_field_phase5_signal_sort_key)
        top_signal = local_candidates[0]
        return top_signal, str(top_signal.get("signalLevel") or "unknown").strip().lower() or "unknown"

    observation_summary = eo_context.get("observationSummary") if isinstance(eo_context.get("observationSummary"), dict) else {}
    quality_status = str(observation_summary.get("qualityStatus") or "").strip().lower()
    if quality_status in {"usable", "partial"}:
        return None, "low"

    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    scout_priority = str(daily_state.get("scoutPriorityCode") or "").strip().lower()
    if scout_priority in {"low", "medium"}:
        return None, "watch"
    return None, "unknown"


def _field_phase5_regional_signal_level(water_context: dict[str, Any]) -> str:
    water_balance = water_context.get("waterBalanceSummary") if isinstance(water_context.get("waterBalanceSummary"), dict) else {}
    levels = [
        _context_status_to_signal_level(water_balance.get("droughtContextStatus")),
        _context_status_to_signal_level(water_balance.get("floodContextStatus")),
    ]
    chosen = "unknown"
    for level in levels:
        chosen = _max_signal_level(chosen, level)
    return chosen


def _field_phase5_locality_status(*, local_level: str, regional_level: str) -> str:
    local_active = local_level in {"watch", "elevated", "high"}
    regional_active = regional_level in {"watch", "elevated", "high"}
    if local_active and regional_active:
        return "partly_regional"
    if local_active and regional_level in {"low", "unknown"}:
        return "local_only"
    if regional_active and local_level in {"low", "unknown"}:
        return "largely_regional"
    if local_level == "low" and regional_level == "low":
        return "unknown"
    if local_level == "unknown" and regional_level == "unknown":
        return "unknown"
    return "mixed"


def _field_phase5_confidence_status(
    *,
    eo_context: dict[str, Any],
    has_regional_profiles: bool,
    evidence_gaps: list[str],
) -> str:
    eo_confidence = str(eo_context.get("confidenceStatus") or "").strip().lower()
    if eo_confidence == "high" and has_regional_profiles and not evidence_gaps:
        return "high"
    if eo_confidence in {"high", "medium"} and has_regional_profiles:
        return "medium"
    if eo_confidence in {"high", "medium", "low"} or has_regional_profiles:
        return "low"
    return "unknown"


_FIELD_PHASE5_NEXT_STEP_RANK = {
    "verify_crop_context": 5,
    "inspect_local": 4,
    "monitor_region": 3,
    "gather_more_evidence": 2,
    "check_market_exposure": 1,
    "no_action": 0,
    "unknown": -1,
}


def _field_phase5_select_crop_relevant_rows(
    rows: list[dict[str, Any]],
    *,
    crop_instance_uri: Optional[str],
) -> list[dict[str, Any]]:
    candidates = [dict(item) for item in rows if isinstance(item, dict)]
    if not crop_instance_uri:
        return candidates
    matching = [
        item
        for item in candidates
        if str(item.get("cropInstanceUri") or "").strip() == crop_instance_uri
    ]
    if matching:
        return matching
    generic = [item for item in candidates if not str(item.get("cropInstanceUri") or "").strip()]
    return generic or candidates


def _field_phase5_latest_slice(
    rows: list[dict[str, Any]],
    *,
    primary_key: str,
) -> list[dict[str, Any]]:
    candidates = [dict(item) for item in rows if isinstance(item, dict)]
    latest = _latest_item(candidates, primary_key, "createdAt") or {}
    latest_value = str(latest.get(primary_key) or "").strip()
    if not latest_value:
        return candidates
    return [item for item in candidates if str(item.get(primary_key) or "").strip() == latest_value]


def _field_phase5_explainability_record_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return (
        -_OUTCOME_RANK.get(str(row.get("signalLevel") or "unknown").strip().lower(), -1),
        -_FIELD_PHASE5_NEXT_STEP_RANK.get(str(row.get("recommendedNextStep") or "unknown").strip(), -1),
        str(row.get("signalType") or ""),
    )


def _field_phase5_explainability_policy_batch_sort_key(row: dict[str, Any]) -> tuple[object, ...]:
    return (
        *_time_sort_tuple(row, "asOf", "createdAt"),
        str(row.get("policyId") or "").strip(),
        str(row.get("policyVersion") or "").strip(),
        str(row.get("uri") or ""),
    )


def _field_phase5_select_active_policy_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], Optional[tuple[str, str]]]:
    candidates = [dict(item) for item in rows if isinstance(item, dict)]
    policy_rows = [
        item
        for item in candidates
        if str(item.get("policyId") or "").strip() and str(item.get("policyVersion") or "").strip()
    ]
    if not policy_rows:
        return candidates, None
    active_row = max(policy_rows, key=_field_phase5_explainability_policy_batch_sort_key)
    active_policy = (
        str(active_row.get("policyId") or "").strip(),
        str(active_row.get("policyVersion") or "").strip(),
    )
    return [
        item
        for item in candidates
        if (
            str(item.get("policyId") or "").strip(),
            str(item.get("policyVersion") or "").strip(),
        )
        == active_policy
    ], active_policy


def _field_phase5_stored_confidence_summary(rows: list[dict[str, Any]]) -> str:
    statuses = {
        str(item.get("confidenceStatus") or "").strip().lower()
        for item in rows
        if str(item.get("confidenceStatus") or "").strip()
    }
    if not statuses:
        return "unknown"
    if len(statuses) == 1:
        return next(iter(statuses))
    if "mixed" in statuses or len(statuses) > 1:
        return "mixed"
    return "unknown"


def _field_phase5_stored_locality_status(rows: list[dict[str, Any]]) -> str:
    statuses = {
        str(item.get("localityStatus") or "").strip()
        for item in rows
        if str(item.get("localityStatus") or "").strip()
    }
    if not statuses:
        return "unknown"
    if len(statuses) == 1:
        return next(iter(statuses))
    return "mixed"


def _field_phase5_stored_freshness_status(rows: list[dict[str, Any]]) -> str:
    statuses = {
        str(item.get("freshnessStatus") or "").strip().lower()
        for item in rows
        if str(item.get("freshnessStatus") or "").strip()
    }
    if not statuses:
        return "unknown"
    if statuses == {"current"}:
        return "fresh"
    if "stale" in statuses:
        return "stale"
    return "partial"


def build_field_benchmark_explainability_context(
    *,
    passport: dict[str, Any],
    water_context: dict[str, Any],
    eo_context: dict[str, Any],
    benchmark_context_facts: Optional[list[dict[str, Any]]] = None,
    explainability_signal_rows: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    identity = passport.get("identity") if isinstance(passport.get("identity"), dict) else {}
    crop_context = passport.get("cropContext") if isinstance(passport.get("cropContext"), dict) else {}
    official_links = passport.get("officialLinks") or []
    latest_authority = _latest_item(official_links, "recordedAt", "createdAt") or {}
    water_balance = water_context.get("waterBalanceSummary") if isinstance(water_context.get("waterBalanceSummary"), dict) else {}
    regional_profiles = water_context.get("regionalProfiles") if isinstance(water_context.get("regionalProfiles"), dict) else {}
    drought_profile = regional_profiles.get("droughtProfile") if isinstance(regional_profiles.get("droughtProfile"), dict) else {}
    flood_profile = regional_profiles.get("floodProfile") if isinstance(regional_profiles.get("floodProfile"), dict) else {}
    observation_summary = eo_context.get("observationSummary") if isinstance(eo_context.get("observationSummary"), dict) else {}
    top_local_signal, local_signal_level = _field_phase5_local_signal(passport, water_context, eo_context)
    regional_signal_level = _field_phase5_regional_signal_level(water_context)
    locality_status = _field_phase5_locality_status(local_level=local_signal_level, regional_level=regional_signal_level)

    evidence_refs: list[str] = []
    trace_refs: list[str] = []
    _append_unique_many(evidence_refs, water_context.get("evidenceRefs") or [])
    _append_unique_many(evidence_refs, eo_context.get("evidenceRefs") or [])
    _append_unique_many(trace_refs, water_context.get("traceRefs") or [])
    _append_unique_many(trace_refs, eo_context.get("traceRefs") or [])

    evidence_gaps: list[str] = []
    _append_unique_many(evidence_gaps, water_context.get("requiredEvidence") or [])
    _append_unique_many(evidence_gaps, eo_context.get("evidenceGaps") or [])
    _append_unique_many(evidence_gaps, eo_context.get("requiredEvidence") or [])
    if not str(crop_context.get("cropInstanceUri") or "").strip() and not str(crop_context.get("seasonCode") or "").strip():
        _append_unique(evidence_gaps, "field_declaration_snapshot")

    confidence_status = _field_phase5_confidence_status(
        eo_context=eo_context,
        has_regional_profiles=bool(drought_profile or flood_profile),
        evidence_gaps=evidence_gaps,
    )

    key_indicators: list[dict[str, Any]] = [
        {
            "domain": "climate_stress_context",
            "metricCode": "drought_profile",
            "geographyScope": "regional_context",
            "status": str(water_balance.get("droughtContextStatus") or "unknown"),
            "metricValue": _as_number(drought_profile.get("frequencyValue")),
            "unitCode": str(drought_profile.get("frequencyKindCode") or "").strip() or None,
            "summary": (
                "Regional drought support is present for this parcel context."
                if str(water_balance.get("droughtContextStatus") or "") in {"regional-watch", "regional-elevated"}
                else "No elevated regional drought support was found for this parcel context."
                if str(water_balance.get("droughtContextStatus") or "") == "none"
                else "Regional drought support is not yet decision-ready for this parcel context."
            ),
        },
        {
            "domain": "climate_stress_context",
            "metricCode": "flood_profile",
            "geographyScope": "regional_context",
            "status": str(water_balance.get("floodContextStatus") or "unknown"),
            "metricValue": _as_number(flood_profile.get("frequencyValue")),
            "unitCode": str(flood_profile.get("frequencyKindCode") or "").strip() or None,
            "summary": (
                "Regional flood support is present for this parcel context."
                if str(water_balance.get("floodContextStatus") or "") in {"watch", "elevated"}
                else "No elevated regional flood support was found for this parcel context."
                if str(water_balance.get("floodContextStatus") or "") == "none"
                else "Regional flood support is not yet decision-ready for this parcel context."
            ),
        },
        {
            "domain": "field_condition",
            "metricCode": "local_field_signal",
            "geographyScope": "field_authority",
            "status": local_signal_level,
            "metricValue": _as_number(observation_summary.get("coveragePct")),
            "unitCode": "percent" if observation_summary.get("coveragePct") is not None else None,
            "summary": (
                f"Top local field signal is {str(top_local_signal.get('signalType') or '').strip()}."
                if isinstance(top_local_signal, dict) and str(top_local_signal.get("signalType") or "").strip()
                else str(observation_summary.get("summary") or "").strip() or "No strong local field signal was inferred."
            ),
        },
    ]

    explainability_signals: list[dict[str, Any]] = []
    if isinstance(top_local_signal, dict) and local_signal_level in {"watch", "elevated", "high"} and regional_signal_level in {"low", "unknown"}:
        explainability_signals.append(
            {
                "signalType": "localOutlierContext",
                "signalLevel": local_signal_level,
                "localityStatus": "local_only",
                "confidenceStatus": confidence_status,
                "recommendedNextStep": "inspect_local",
                "reasonCodes": [
                    f"source_signal:{str(top_local_signal.get('signalType') or '').strip()}",
                    *list(top_local_signal.get("reasonCodes") or []),
                ],
                "traceRefs": list(top_local_signal.get("traceRefs") or []),
                "evidenceRefs": list(top_local_signal.get("evidenceRefs") or []),
            }
        )

    if regional_signal_level in {"watch", "elevated", "high"}:
        regional_reasons: list[str] = []
        drought_status = str(water_balance.get("droughtContextStatus") or "").strip()
        flood_status = str(water_balance.get("floodContextStatus") or "").strip()
        if drought_status:
            regional_reasons.append(f"drought_context:{drought_status}")
        if flood_status:
            regional_reasons.append(f"flood_context:{flood_status}")
        explainability_signals.append(
            {
                "signalType": "regionalStressContext",
                "signalLevel": regional_signal_level,
                "localityStatus": "partly_regional" if local_signal_level in {"watch", "elevated", "high"} else "largely_regional",
                "confidenceStatus": confidence_status,
                "recommendedNextStep": "inspect_local" if local_signal_level in {"watch", "elevated", "high"} else "monitor_region",
                "reasonCodes": regional_reasons,
                "traceRefs": list(trace_refs),
                "evidenceRefs": list(evidence_refs),
            }
        )

    if isinstance(top_local_signal, dict) and local_signal_level in {"watch", "elevated", "high"} and regional_signal_level in {"watch", "elevated", "high"}:
        explainability_signals.append(
            {
                "signalType": "mixedSignalContext",
                "signalLevel": _max_signal_level(local_signal_level, regional_signal_level),
                "localityStatus": "mixed",
                "confidenceStatus": confidence_status,
                "recommendedNextStep": "inspect_local",
                "reasonCodes": [
                    f"source_signal:{str(top_local_signal.get('signalType') or '').strip()}",
                    f"drought_context:{str(water_balance.get('droughtContextStatus') or '').strip() or 'unknown'}",
                    f"flood_context:{str(water_balance.get('floodContextStatus') or '').strip() or 'unknown'}",
                ],
                "traceRefs": list(trace_refs),
                "evidenceRefs": list(evidence_refs),
            }
        )

    if "field_declaration_snapshot" in evidence_gaps:
        explainability_signals.append(
            {
                "signalType": "benchmarkGap",
                "signalLevel": "elevated",
                "localityStatus": "unknown",
                "confidenceStatus": "low",
                "recommendedNextStep": "verify_crop_context",
                "reasonCodes": ["missing_crop_context"],
                "traceRefs": list(trace_refs),
                "evidenceRefs": list(evidence_refs),
            }
        )
    elif evidence_gaps:
        explainability_signals.append(
            {
                "signalType": "dataCoverageGap",
                "signalLevel": "watch",
                "localityStatus": "unknown",
                "confidenceStatus": "low",
                "recommendedNextStep": "gather_more_evidence",
                "reasonCodes": list(evidence_gaps),
                "traceRefs": list(trace_refs),
                "evidenceRefs": list(evidence_refs),
            }
        )

    explainability_signals = sorted(explainability_signals, key=_field_phase5_signal_sort_key)[:4]

    locality_summary = "No strong local-versus-regional conclusion is available from current evidence."
    if locality_status == "local_only":
        locality_summary = "The strongest current signal looks field-local rather than region-wide."
    elif locality_status == "partly_regional":
        locality_summary = "The field issue is partly regional, but parcel-local review is still warranted."
    elif locality_status == "largely_regional":
        locality_summary = "The strongest current signal is supported by broader regional stress context."
    elif locality_status == "mixed":
        locality_summary = "Local and regional signals both contribute to the current explanation."

    recommended_next_step = "no_action"
    if any(str(item.get("recommendedNextStep") or "") == "verify_crop_context" for item in explainability_signals):
        recommended_next_step = "verify_crop_context"
    elif any(str(item.get("recommendedNextStep") or "") == "inspect_local" for item in explainability_signals):
        recommended_next_step = "inspect_local"
    elif any(str(item.get("recommendedNextStep") or "") == "monitor_region" for item in explainability_signals):
        recommended_next_step = "monitor_region"
    elif any(str(item.get("recommendedNextStep") or "") == "gather_more_evidence" for item in explainability_signals):
        recommended_next_step = "gather_more_evidence"

    comparison_rows: list[dict[str, Any]] = [
        {
            "domain": "climate_stress_context",
            "metricCode": "drought_profile",
            "fieldStatus": str(water_balance.get("waterDeficitProxyStatus") or "unknown"),
            "benchmarkStatus": str(water_balance.get("droughtContextStatus") or "unknown"),
            "localityStatus": _field_phase5_locality_status(
                local_level=_context_status_to_signal_level(water_balance.get("waterDeficitProxyStatus")),
                regional_level=_context_status_to_signal_level(water_balance.get("droughtContextStatus")),
            ),
            "fieldValue": None,
            "benchmarkValue": _as_number(drought_profile.get("frequencyValue")),
            "unitCode": str(drought_profile.get("frequencyKindCode") or "").strip() or None,
            "summary": "Compare parcel water-deficit proxy against the current regional drought profile support.",
        },
        {
            "domain": "climate_stress_context",
            "metricCode": "flood_profile",
            "fieldStatus": str((((water_context.get("facts") or {}).get("signals") or {}).get("floodRiskLevel")) or "unknown"),
            "benchmarkStatus": str(water_balance.get("floodContextStatus") or "unknown"),
            "localityStatus": _field_phase5_locality_status(
                local_level=str((((water_context.get("facts") or {}).get("signals") or {}).get("floodRiskLevel")) or "unknown"),
                regional_level=_context_status_to_signal_level(water_balance.get("floodContextStatus")),
            ),
            "fieldValue": None,
            "benchmarkValue": _as_number(flood_profile.get("frequencyValue")),
            "unitCode": str(flood_profile.get("frequencyKindCode") or "").strip() or None,
            "summary": "Compare parcel flood or ponding pressure against the current regional flood support.",
        },
        {
            "domain": "field_condition",
            "metricCode": "local_field_signal",
            "fieldStatus": local_signal_level,
            "benchmarkStatus": regional_signal_level,
            "localityStatus": locality_status,
            "fieldValue": _as_number(observation_summary.get("coveragePct")),
            "benchmarkValue": None,
            "unitCode": "percent" if observation_summary.get("coveragePct") is not None else None,
            "summary": "Compare the strongest parcel-local signal against the broader regional context status.",
        },
    ]
    comparison_rows = [
        row
        for row in comparison_rows
        if row["fieldStatus"] != "unknown" or row["benchmarkStatus"] != "unknown" or row["benchmarkValue"] is not None
    ]

    freshness_status = "fresh"
    stale_flags = list(((passport.get("freshness") or {}).get("staleFlags")) or [])
    if stale_flags:
        freshness_status = "stale"
    elif evidence_gaps:
        freshness_status = "partial"

    geography_strata = [
        {
            "geographyScope": "field_authority",
            "geographyCode": str(latest_authority.get("authorityCode") or identity.get("fieldUri") or "").strip() or None,
            "status": "resolved" if str(latest_authority.get("authorityCode") or "").strip() else "inferred",
            "mappingBasis": str(latest_authority.get("authoritySchemeCode") or "field_uri").strip() or "field_uri",
        },
        {
            "geographyScope": "regional_context",
            "geographyCode": str((drought_profile or flood_profile).get("dataSourceRef") or "").strip() or None,
            "status": "available" if drought_profile or flood_profile else "missing",
            "mappingBasis": "climate_hazard_profile",
        },
        {
            "geographyScope": "crop_context",
            "geographyCode": str(crop_context.get("seasonCode") or crop_context.get("cropTypeUri") or "").strip() or None,
            "status": "resolved" if str(crop_context.get("seasonCode") or crop_context.get("cropTypeUri") or "").strip() else "missing",
            "mappingBasis": "field_declaration_snapshot",
        },
    ]

    context = {
        "fieldUri": str(identity.get("fieldUri") or "").strip(),
        "activeCropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
        "geographyStrata": geography_strata,
        "keyIndicators": key_indicators,
        "freshnessSummary": {
            "status": freshness_status,
            "summary": (
                "Benchmark context is fresh against the current parcel evidence."
                if freshness_status == "fresh"
                else "Benchmark context is usable but still has evidence gaps."
                if freshness_status == "partial"
                else "Passport freshness flags reduce confidence in the current benchmark context."
            ),
        },
        "topSignals": explainability_signals,
        "localityConclusion": {
            "status": locality_status,
            "summary": locality_summary,
        },
        "confidenceSummary": {
            "status": confidence_status,
            "summary": (
                "Regional context and parcel evidence align with high confidence."
                if confidence_status == "high"
                else "Regional context is usable, but the explanation still relies on partial evidence."
                if confidence_status == "medium"
                else "The explanation should be treated cautiously because evidence is incomplete or weakly mapped."
                if confidence_status == "low"
                else "Explainability confidence is not yet decision-ready."
            ),
        },
        "recommendedNextStep": recommended_next_step,
        "evidenceGaps": evidence_gaps,
        "comparisonRows": comparison_rows,
        "selectedDomains": sorted({str(row.get("domain") or "").strip() for row in comparison_rows if str(row.get("domain") or "").strip()}),
        "normalizationPolicyVersion": "field-phase5-benchmark-v1",
        "evidencePolicy": (
            "Advisory comparison only; regional context explains parcel signals but does not override official parcel facts or legal overlays."
        ),
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
    }

    stored_benchmark_context_facts = _field_phase5_select_crop_relevant_rows(
        benchmark_context_facts or [],
        crop_instance_uri=str(crop_context.get("cropInstanceUri") or "").strip() or None,
    )
    stored_explainability_signal_rows = _field_phase5_select_crop_relevant_rows(
        explainability_signal_rows or [],
        crop_instance_uri=str(crop_context.get("cropInstanceUri") or "").strip() or None,
    )
    active_policy_signal_rows, active_policy_identity = _field_phase5_select_active_policy_rows(
        stored_explainability_signal_rows
    )
    latest_benchmark_context_facts = _field_phase5_latest_slice(
        stored_benchmark_context_facts,
        primary_key="asOf",
    )
    latest_explainability_signal_rows = _field_phase5_latest_slice(
        active_policy_signal_rows,
        primary_key="asOf",
    )

    if not latest_benchmark_context_facts and not latest_explainability_signal_rows:
        return context

    stored_evidence_refs = list(context.get("evidenceRefs") or [])
    stored_trace_refs = list(context.get("traceRefs") or [])
    for item in latest_benchmark_context_facts:
        _append_unique_many(stored_evidence_refs, item.get("evidenceRefs") or [])
        _append_unique_many(stored_trace_refs, item.get("traceRefs") or [])
    for item in latest_explainability_signal_rows:
        _append_unique_many(stored_evidence_refs, item.get("evidenceRefs") or [])
        _append_unique_many(stored_trace_refs, item.get("traceRefs") or [])

    geography_rows = [dict(item) for item in context.get("geographyStrata") or [] if isinstance(item, dict)]
    seen_geographies = {
        (
            str(item.get("geographyScope") or "").strip(),
            str(item.get("geographyCode") or "").strip(),
        )
        for item in geography_rows
    }
    for item in latest_benchmark_context_facts:
        geography_scope = str(item.get("geographyScope") or "").strip()
        geography_code = str(item.get("geographyCode") or "").strip()
        if not geography_scope:
            continue
        key = (geography_scope, geography_code)
        if key in seen_geographies:
            continue
        seen_geographies.add(key)
        geography_rows.append(
            {
                "geographyScope": geography_scope,
                "geographyCode": geography_code or None,
                "status": "available",
                "mappingBasis": str(item.get("sourceSystem") or "field_benchmark_context_fact").strip()
                or "field_benchmark_context_fact",
            }
        )

    key_indicator_rows = [dict(item) for item in context.get("keyIndicators") or [] if isinstance(item, dict)]
    key_indicator_index = {
        (
            str(item.get("domain") or "").strip(),
            str(item.get("metricCode") or "").strip(),
        ): index
        for index, item in enumerate(key_indicator_rows)
    }
    for item in reversed(latest_benchmark_context_facts):
        indicator_row = {
            "domain": str(item.get("benchmarkDomain") or "").strip() or "benchmark_context",
            "metricCode": str(item.get("metricCode") or "").strip() or "unknown",
            "geographyScope": str(item.get("geographyScope") or "").strip() or "unknown",
            "status": str(item.get("freshnessStatus") or item.get("confidenceStatus") or "unknown").strip() or "unknown",
            "metricValue": _as_number(item.get("metricValue")),
            "unitCode": str(item.get("unitCode") or "").strip() or None,
            "summary": str(item.get("notes") or "").strip()
            or f"Stored benchmark metric from {str(item.get('sourceSystem') or 'benchmark_source').strip() or 'benchmark_source'}.",
        }
        key = (
            str(indicator_row.get("domain") or "").strip(),
            str(indicator_row.get("metricCode") or "").strip(),
        )
        if key in key_indicator_index:
            key_indicator_rows[key_indicator_index[key]] = indicator_row
        else:
            key_indicator_index[key] = len(key_indicator_rows)
            key_indicator_rows.append(indicator_row)

    top_signal_rows = [dict(item) for item in context.get("topSignals") or [] if isinstance(item, dict)]
    locality_conclusion = dict(context.get("localityConclusion") or {})
    confidence_summary = dict(context.get("confidenceSummary") or {})
    recommended_next_step_value = str(context.get("recommendedNextStep") or "unknown").strip() or "unknown"
    if latest_explainability_signal_rows:
        top_signal_rows = [
            {
                "signalType": str(item.get("signalType") or "").strip() or "dataCoverageGap",
                "signalLevel": str(item.get("signalLevel") or "unknown").strip().lower() or "unknown",
                "localityStatus": str(item.get("localityStatus") or "unknown").strip() or "unknown",
                "confidenceStatus": str(item.get("confidenceStatus") or "unknown").strip().lower() or "unknown",
                "recommendedNextStep": str(item.get("recommendedNextStep") or "unknown").strip() or "unknown",
                "policyId": str(item.get("policyId") or "").strip() or None,
                "policyVersion": str(item.get("policyVersion") or "").strip() or None,
                "reasonCodes": list(item.get("reasonCodes") or []),
                "traceRefs": list(item.get("traceRefs") or []),
                "evidenceRefs": list(item.get("evidenceRefs") or []),
            }
            for item in sorted(latest_explainability_signal_rows, key=_field_phase5_explainability_record_sort_key)[:4]
        ]
        stored_locality_status = _field_phase5_stored_locality_status(top_signal_rows)
        locality_conclusion = {
            "status": stored_locality_status,
            "summary": (
                "Stored explainability signals indicate the strongest current explanation is field-local."
                if stored_locality_status == "local_only"
                else "Stored explainability signals indicate both local and regional context matter."
                if stored_locality_status in {"partly_regional", "mixed"}
                else "Stored explainability signals indicate the strongest current explanation is largely regional."
                if stored_locality_status in {"largely_regional", "national_pattern", "eu_pattern"}
                else "Stored explainability signals do not yet support a strong locality conclusion."
            ),
        }
        stored_confidence_status = _field_phase5_stored_confidence_summary(top_signal_rows)
        confidence_summary = {
            "status": stored_confidence_status,
            "summary": (
                "Stored explainability signals are strongly supported by current benchmark evidence."
                if stored_confidence_status == "high"
                else "Stored explainability signals are usable but still rely on partial evidence."
                if stored_confidence_status == "medium"
                else "Stored explainability signals should be treated cautiously because evidence is mixed or incomplete."
                if stored_confidence_status in {"low", "mixed"}
                else "Stored explainability confidence is not yet decision-ready."
            ),
        }
        recommended_next_step_value = (
            str(top_signal_rows[0].get("recommendedNextStep") or "unknown").strip() or "unknown"
        )

    comparison_rows = [dict(item) for item in context.get("comparisonRows") or [] if isinstance(item, dict)]
    comparison_index = {
        (
            str(item.get("domain") or "").strip(),
            str(item.get("metricCode") or "").strip(),
        ): index
        for index, item in enumerate(comparison_rows)
    }
    locality_status_value = str(locality_conclusion.get("status") or "unknown").strip() or "unknown"
    for item in reversed(latest_benchmark_context_facts):
        comparison_row = {
            "domain": str(item.get("benchmarkDomain") or "").strip() or "benchmark_context",
            "metricCode": str(item.get("metricCode") or "").strip() or "unknown",
            "fieldStatus": "unknown",
            "benchmarkStatus": str(item.get("freshnessStatus") or item.get("confidenceStatus") or "unknown").strip()
            or "unknown",
            "localityStatus": locality_status_value,
            "fieldValue": None,
            "benchmarkValue": _as_number(item.get("metricValue")),
            "unitCode": str(item.get("unitCode") or "").strip() or None,
            "summary": str(item.get("notes") or "").strip()
            or f"Stored benchmark metric from {str(item.get('sourceSystem') or 'benchmark_source').strip() or 'benchmark_source'}.",
        }
        key = (
            str(comparison_row.get("domain") or "").strip(),
            str(comparison_row.get("metricCode") or "").strip(),
        )
        if key in comparison_index:
            existing = comparison_rows[comparison_index[key]]
            comparison_row["fieldStatus"] = str(existing.get("fieldStatus") or "unknown").strip() or "unknown"
            comparison_row["fieldValue"] = _as_number(existing.get("fieldValue"))
            comparison_row["localityStatus"] = (
                str(existing.get("localityStatus") or locality_status_value).strip() or locality_status_value
            )
            comparison_rows[comparison_index[key]] = comparison_row
        else:
            comparison_index[key] = len(comparison_rows)
            comparison_rows.append(comparison_row)

    stored_evidence_gaps = list(context.get("evidenceGaps") or [])
    if not latest_benchmark_context_facts:
        _append_unique(stored_evidence_gaps, "field_benchmark_context_fact")
    if not latest_explainability_signal_rows:
        _append_unique(stored_evidence_gaps, "field_explainability_signal")
    elif active_policy_identity is not None:
        _append_unique(stored_trace_refs, f"active_policy:{active_policy_identity[0]}:{active_policy_identity[1]}")

    freshness_status = str(context.get("freshnessSummary", {}).get("status") or "unknown").strip() or "unknown"
    freshness_summary_text = str(context.get("freshnessSummary", {}).get("summary") or "").strip()
    if latest_benchmark_context_facts:
        freshness_status = _field_phase5_stored_freshness_status(latest_benchmark_context_facts)
        freshness_summary_text = (
            "Stored benchmark facts are fresh against the current parcel evidence."
            if freshness_status == "fresh"
            else "Stored benchmark facts are usable but still partially fresh."
            if freshness_status == "partial"
            else "Stored benchmark facts are stale relative to the current parcel evidence."
            if freshness_status == "stale"
            else "Stored benchmark freshness is not yet decision-ready."
        )

    context["geographyStrata"] = geography_rows
    context["keyIndicators"] = key_indicator_rows
    context["freshnessSummary"] = {
        "status": freshness_status,
        "summary": freshness_summary_text,
    }
    context["topSignals"] = top_signal_rows
    context["localityConclusion"] = locality_conclusion
    context["confidenceSummary"] = confidence_summary
    context["recommendedNextStep"] = recommended_next_step_value
    context["evidenceGaps"] = stored_evidence_gaps
    context["comparisonRows"] = comparison_rows
    context["selectedDomains"] = sorted(
        {
            str(row.get("domain") or "").strip()
            for row in comparison_rows
            if str(row.get("domain") or "").strip()
        }
    )
    context["evidenceRefs"] = stored_evidence_refs
    context["traceRefs"] = stored_trace_refs
    return context


def build_field_benchmark_context_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "geographyStrata": context.get("geographyStrata") or [],
        "keyIndicators": context.get("keyIndicators") or [],
        "freshnessSummary": context.get("freshnessSummary") or {},
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


def build_field_explainability_summary_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "topSignals": context.get("topSignals") or [],
        "localityConclusion": context.get("localityConclusion") or {},
        "confidenceSummary": context.get("confidenceSummary") or {},
        "recommendedNextStep": context.get("recommendedNextStep") or "unknown",
        "evidenceGaps": context.get("evidenceGaps") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


def build_field_regional_comparison_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "comparisonRows": context.get("comparisonRows") or [],
        "selectedDomains": context.get("selectedDomains") or [],
        "normalizationPolicyVersion": context.get("normalizationPolicyVersion") or "field-phase5-benchmark-v1",
        "evidencePolicy": context.get("evidencePolicy") or "",
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


def _field_phase6_signal_sort_key(row: dict[str, Any]) -> tuple[int, int, str]:
    return (
        -_CLIMATE_PRIORITY_RANK.get(str(row.get("priorityLevel") or "exploratory").strip().lower(), 0),
        -_OUTCOME_RANK.get(str(row.get("confidenceStatus") or "unknown").strip().lower(), -1),
        str(row.get("signalType") or ""),
    )


def _field_phase6_confidence_status(
    *,
    climate_profiles: list[dict[str, Any]],
    pedoclimatic_profile: Optional[dict[str, Any]],
    evidence_gaps: list[str],
) -> str:
    if not climate_profiles:
        return "unknown"
    if pedoclimatic_profile and "scenario_horizon_context" not in evidence_gaps:
        return "medium"
    if pedoclimatic_profile:
        return "low"
    if climate_profiles:
        return "low"
    return "unknown"


def _field_phase6_signal_confidence(
    *,
    row: Optional[dict[str, Any]],
    default_status: str,
) -> str:
    if not isinstance(row, dict) or not row:
        return default_status
    confidence_level = str(row.get("confidenceLevelCode") or "").strip().lower()
    if confidence_level in {"high", "medium", "low", "unknown"}:
        return confidence_level
    confidence_score = _as_number(row.get("confidenceScore"))
    if confidence_score is None:
        return default_status
    if confidence_score >= 0.8:
        return "high"
    if confidence_score >= 0.55:
        return "medium"
    return "low"


def _field_phase6_priority_from_level(level: str) -> str:
    normalized = str(level or "").strip().lower()
    if normalized in {"high", "blocked"}:
        return "high"
    if normalized in {"elevated", "medium", "watch"}:
        return "medium"
    if normalized in {"low", "ready", "aligned", "clear"}:
        return "low"
    return "exploratory"


def _field_phase6_horizon_summary(
    *,
    climate_profiles: list[dict[str, Any]],
    evidence_gaps: list[str],
) -> dict[str, Any]:
    if not climate_profiles:
        return {
            "status": "missing",
            "horizonsCovered": [],
            "summary": "No climate profile support is available for adaptation planning.",
        }
    if "scenario_horizon_context" in evidence_gaps:
        return {
            "status": "cross_horizon_only",
            "horizonsCovered": ["cross_horizon"],
            "summary": (
                "Current climate support is usable only as cross-horizon advisory context because "
                "scenario and named horizon metadata are not encoded in the available records."
            ),
        }
    return {
        "status": "resolved",
        "horizonsCovered": ["cross_horizon"],
        "summary": "Climate support resolves only as cross-horizon advisory context in the current repo state.",
    }


def _field_phase6_field_datetime(row: dict[str, Any], field_name: str) -> Optional[datetime]:
    current_dt = _parse_iso_datetime(row.get(field_name))
    if current_dt is not None:
        return current_dt
    current_date = _parse_iso_date(row.get(field_name))
    if current_date is not None:
        return datetime.combine(current_date, datetime.min.time(), tzinfo=timezone.utc)
    return None


def _field_phase6_row_datetime(row: dict[str, Any], *time_fields: str) -> datetime:
    for field_name in time_fields:
        current_dt = _field_phase6_field_datetime(row, field_name)
        if current_dt is not None:
            return current_dt
    return datetime.min.replace(tzinfo=timezone.utc)


def _field_phase6_latest_rows(rows: list[dict[str, Any]], *time_fields: str) -> list[dict[str, Any]]:
    for field_name in time_fields:
        latest_rows: list[dict[str, Any]] = []
        latest_dt: Optional[datetime] = None
        for row in rows:
            current_dt = _field_phase6_field_datetime(row, field_name)
            if current_dt is None:
                continue
            if latest_dt is None or current_dt > latest_dt:
                latest_rows = [row]
                latest_dt = current_dt
                continue
            if current_dt == latest_dt:
                latest_rows.append(row)
        if latest_rows:
            return latest_rows
    return list(rows)


def _field_phase6_source_priority(row: dict[str, Any]) -> int:
    source_system = str(row.get("sourceSystem") or "").strip().lower()
    geography_code = str(row.get("geographyCode") or "").strip().lower()
    texts = [source_system, geography_code]
    for ref in row.get("evidenceRefs") or []:
        texts.append(str(ref or "").strip().lower())
    for ref in row.get("traceRefs") or []:
        texts.append(str(ref or "").strip().lower())
    combined = " ".join(texts)
    if "1km" in combined or "_1km" in combined:
        return 30
    if "5km" in combined or "_5km" in combined:
        return 25
    if "12km" in combined or "_12km" in combined:
        return 20
    if source_system or geography_code or combined.strip():
        return 10
    return 0


def _field_phase6_preferred_source_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(rows) <= 1:
        return list(rows)
    ranked_rows = [(row, _field_phase6_source_priority(row)) for row in rows]
    max_priority = max(priority for _, priority in ranked_rows)
    return [row for row, priority in ranked_rows if priority == max_priority]


def _field_phase6_stored_geography_fit_status(rows: list[dict[str, Any]]) -> str:
    statuses = {
        str(row.get("geographyFitStatus") or "").strip().lower()
        for row in rows
        if str(row.get("geographyFitStatus") or "").strip()
    }
    if not statuses:
        return "missing"
    mapped_statuses = {"mapped", "field_exact", "field_matched", "field_context"}
    partial_statuses = {"partial", "mixed", "downscaled"}
    regional_statuses = {"regional_proxy", "regional_only", "regional_context", "regional"}
    if any(status in mapped_statuses for status in statuses) and any(
        status in partial_statuses or status in regional_statuses for status in statuses
    ):
        return "partial"
    if any(status in mapped_statuses for status in statuses):
        return "mapped"
    if any(status in partial_statuses for status in statuses):
        return "partial"
    if any(status in regional_statuses for status in statuses):
        return "regional_only"
    return "missing"


def _field_phase6_stored_confidence_status(
    *,
    climate_projection_facts: list[dict[str, Any]],
    climate_adaptation_signals: list[dict[str, Any]],
    geography_fit_status: str,
) -> str:
    confidence_rank = {"low": 0, "medium": 1, "high": 2}
    known_statuses = [
        str(row.get("confidenceStatus") or "").strip().lower()
        for row in climate_adaptation_signals
        if str(row.get("confidenceStatus") or "").strip().lower() in confidence_rank
    ]
    if known_statuses:
        selected = min(known_statuses, key=lambda value: confidence_rank[value])
        if geography_fit_status == "regional_only" and selected == "high":
            return "medium"
        return selected
    if climate_projection_facts:
        return "low" if geography_fit_status != "missing" else "unknown"
    return "unknown"


def _field_phase6_stored_freshness_status(climate_projection_facts: list[dict[str, Any]]) -> str:
    statuses = {
        str(row.get("freshnessStatus") or "").strip().lower()
        for row in climate_projection_facts
        if str(row.get("freshnessStatus") or "").strip()
    }
    if not statuses:
        return "partial"
    if "stale" in statuses:
        return "stale"
    if statuses.issubset({"current", "fresh"}):
        return "fresh"
    return "partial"


def _field_phase6_indicator_supporting_label(row: dict[str, Any]) -> str | None:
    indicator_code = str(row.get("indicatorCode") or row.get("indicator_code") or "").strip()
    if not indicator_code:
        return None
    aggregation_type = str(row.get("aggregationType") or row.get("aggregation_type") or "").strip()
    if not aggregation_type:
        return indicator_code
    return f"{indicator_code}@{aggregation_type}"


def _build_field_climate_adaptation_context_from_stored(
    *,
    passport: dict[str, Any],
    water_context: dict[str, Any],
    eo_context: dict[str, Any],
    benchmark_context: dict[str, Any],
    climate_projection_facts: list[dict[str, Any]],
    climate_adaptation_signals: list[dict[str, Any]],
    candidate_variety_uri: Optional[str],
    variety_context_source: Optional[str] = None,
    permanent_crop_component_snapshots: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    identity = passport.get("identity") if isinstance(passport.get("identity"), dict) else {}
    crop_context = passport.get("cropContext") if isinstance(passport.get("cropContext"), dict) else {}
    permanent_crop_variety_context = resolve_permanent_crop_variety_context(
        permanent_crop_component_snapshots or [],
    )
    resolved_variety_uri = (
        candidate_variety_uri
        or str(permanent_crop_variety_context.get("varietyUri") or "").strip()
        or None
    )
    if variety_context_source is None:
        variety_context_source = (
            "permanent_crop_component_snapshot"
            if resolved_variety_uri
            else None
        )

    current_projection_facts = _field_phase6_preferred_source_rows(
        _field_phase6_latest_rows(climate_projection_facts, "asOf", "createdAt", "periodEnd")
    )
    current_adaptation_signals = _field_phase6_preferred_source_rows(
        _field_phase6_latest_rows(climate_adaptation_signals, "asOf", "createdAt")
    )
    current_rows = [*current_projection_facts, *current_adaptation_signals]

    planning_context_mode = (
        str(
            (_latest_item(current_adaptation_signals, "asOf", "createdAt") or {}).get("planningContextMode")
            or (_latest_item(current_projection_facts, "asOf", "createdAt") or {}).get("planningContextMode")
            or ""
        ).strip()
        or (
            "current_crop"
            if str(crop_context.get("cropInstanceUri") or "").strip()
            else "candidate_crop"
            if resolved_variety_uri
            else "generic_field"
        )
    )
    planning_context_summary = (
        "Climate adaptation summary is anchored to stored current-crop climate facts."
        if planning_context_mode == "current_crop" and variety_context_source != "permanent_crop_component_snapshot"
        else "Climate adaptation summary is anchored to stored current-crop climate facts and uses dominant permanent-crop composition for variety context."
        if planning_context_mode == "current_crop"
        else "Climate adaptation summary is anchored to stored candidate-crop climate facts."
        if planning_context_mode == "candidate_crop" and variety_context_source != "permanent_crop_component_snapshot"
        else "Climate adaptation summary is anchored to source-native permanent-crop composition because no variety-risk record is available."
        if planning_context_mode == "candidate_crop"
        else "Stored climate context is field-generic because crop or variety context is incomplete."
    )

    evidence_refs = collect_passport_evidence_uris(passport)
    trace_refs: list[str] = []
    _append_unique_many(evidence_refs, water_context.get("evidenceRefs") or [])
    _append_unique_many(evidence_refs, eo_context.get("evidenceRefs") or [])
    _append_unique_many(evidence_refs, benchmark_context.get("evidenceRefs") or [])
    _append_unique_many(trace_refs, water_context.get("traceRefs") or [])
    _append_unique_many(trace_refs, eo_context.get("traceRefs") or [])
    _append_unique_many(trace_refs, benchmark_context.get("traceRefs") or [])
    if variety_context_source == "permanent_crop_component_snapshot":
        _append_unique_many(evidence_refs, permanent_crop_variety_context.get("evidenceRefs") or [])
        _append_unique_many(trace_refs, permanent_crop_variety_context.get("traceRefs") or [])

    for row in current_projection_facts:
        _append_unique(trace_refs, str(row.get("uri") or "").strip())
        _append_unique(trace_refs, str(row.get("sourceId") or "").strip())
        _append_unique_many(evidence_refs, row.get("evidenceRefs") or [])
    for row in current_adaptation_signals:
        _append_unique(trace_refs, str(row.get("uri") or "").strip())
        _append_unique_many(trace_refs, row.get("traceRefs") or [])
        _append_unique_many(evidence_refs, row.get("evidenceRefs") or [])

    geography_fit_status = _field_phase6_stored_geography_fit_status(current_rows)
    confidence_status = _field_phase6_stored_confidence_status(
        climate_projection_facts=current_projection_facts,
        climate_adaptation_signals=current_adaptation_signals,
        geography_fit_status=geography_fit_status,
    )
    freshness_status = _field_phase6_stored_freshness_status(current_projection_facts)

    evidence_gaps: list[str] = []
    if not current_projection_facts:
        _append_unique(evidence_gaps, "field_climate_projection_fact")
    if not current_adaptation_signals:
        _append_unique(evidence_gaps, "field_climate_adaptation_signal")
    if planning_context_mode == "generic_field":
        _append_unique(evidence_gaps, "field_declaration_snapshot")
    if geography_fit_status in {"partial", "regional_only"}:
        _append_unique(evidence_gaps, "climate_geography_fit_partial")
    if current_projection_facts and not any(
        str(row.get("scenarioCode") or "").strip() and str(row.get("horizonScope") or "").strip()
        for row in current_projection_facts
    ):
        _append_unique(evidence_gaps, "scenario_horizon_context")

    projected_signals: list[dict[str, Any]] = []
    seen_signal_types: set[str] = set()
    sorted_signal_rows = sorted(
        current_adaptation_signals,
        key=lambda row: (
            _field_phase6_row_datetime(row, "createdAt", "asOf"),
            _CLIMATE_PRIORITY_RANK.get(str(row.get("priorityLevel") or "exploratory").strip().lower(), 0),
        ),
        reverse=True,
    )
    for row in sorted_signal_rows:
        signal_type = str(row.get("signalType") or "").strip()
        if not signal_type or signal_type in seen_signal_types:
            continue
        seen_signal_types.add(signal_type)
        row_trace_refs = list(row.get("traceRefs") or [])
        _append_unique(row_trace_refs, str(row.get("uri") or "").strip())
        projected_signals.append(
            {
                "signalType": signal_type,
                "priorityLevel": str(row.get("priorityLevel") or "exploratory").strip() or "exploratory",
                "horizonScope": str(row.get("horizonScope") or "unknown").strip() or "unknown",
                "confidenceStatus": str(row.get("confidenceStatus") or confidence_status).strip() or confidence_status,
                "recommendedThemes": list(row.get("recommendedThemes") or []),
                "reasonCodes": list(row.get("reasonCodes") or []),
                "traceRefs": row_trace_refs,
                "evidenceRefs": list(row.get("evidenceRefs") or []),
            }
        )
    if not projected_signals and current_projection_facts:
        first_fact = current_projection_facts[0]
        projected_signals.append(
            {
                "signalType": "climateDataGap",
                "priorityLevel": "exploratory",
                "horizonScope": str(first_fact.get("horizonScope") or "unknown").strip() or "unknown",
                "confidenceStatus": confidence_status,
                "recommendedThemes": ["gather_more_evidence"],
                "reasonCodes": ["field_climate_adaptation_signal"],
                "traceRefs": [str(first_fact.get("uri") or "").strip()] if str(first_fact.get("uri") or "").strip() else [],
                "evidenceRefs": list(first_fact.get("evidenceRefs") or []),
            }
        )

    top_signals = sorted(projected_signals, key=_field_phase6_signal_sort_key)[:4]

    recommended_themes: list[str] = []
    for row in top_signals:
        _append_unique_many(recommended_themes, row.get("recommendedThemes") or [])
    if not recommended_themes:
        recommended_themes.append("gather_more_evidence" if evidence_gaps else "no_change")

    indicator_rows: list[dict[str, Any]] = []
    seen_indicator_keys: set[tuple[str, str, str, str]] = set()
    for row in sorted(
        current_projection_facts,
        key=lambda current: (
            _field_phase6_row_datetime(current, "createdAt", "asOf", "periodEnd"),
            str(current.get("indicatorCode") or ""),
        ),
        reverse=True,
    ):
        indicator_code = str(row.get("indicatorCode") or "").strip()
        scenario_code = str(row.get("scenarioCode") or row.get("scenarioFamily") or "").strip()
        horizon_scope = str(row.get("horizonScope") or "unknown").strip() or "unknown"
        geography_scope = str(row.get("geographyScope") or "regional_context").strip() or "regional_context"
        aggregation_type = str(row.get("aggregationType") or "").strip()
        if not indicator_code:
            continue
        dedupe_key = (indicator_code, scenario_code, horizon_scope, geography_scope, aggregation_type)
        if dedupe_key in seen_indicator_keys:
            continue
        seen_indicator_keys.add(dedupe_key)
        indicator_rows.append(
            {
                "indicatorCode": indicator_code,
                "scenarioCode": scenario_code or None,
                "aggregationType": aggregation_type or None,
                "indicatorValue": _as_number(row.get("indicatorValue")),
                "unitCode": str(row.get("unitCode") or "").strip() or None,
                "geographyScope": geography_scope,
                "horizonScope": horizon_scope,
                "uncertaintyClass": str(row.get("uncertaintyClass") or "unknown").strip() or "unknown",
                "sourceRef": str(row.get("sourceId") or row.get("sourceSystem") or "").strip() or None,
                "summary": (
                    f"Stored climate projection fact for {indicator_code} under {scenario_code or 'unspecified_scenario'} "
                    f"at {horizon_scope.replace('_', ' ')} horizon"
                    f"{'' if not aggregation_type else f' ({aggregation_type})'}."
                ),
            }
        )
    indicator_highlights = indicator_rows[:4]

    scenario_set = sorted(
        {
            str(row.get("scenarioCode") or row.get("scenarioFamily") or "").strip()
            for row in current_projection_facts
            if str(row.get("scenarioCode") or row.get("scenarioFamily") or "").strip()
        }
    )
    baseline_policy = "not_available"
    latest_projection = _latest_item(current_projection_facts, "asOf", "createdAt", "periodEnd") or {}
    if str(latest_projection.get("baselinePeriod") or "").strip():
        baseline_policy = str(latest_projection.get("baselinePeriod") or "").strip()
    elif str(latest_projection.get("periodStart") or "").strip() and str(latest_projection.get("periodEnd") or "").strip():
        baseline_policy = (
            f"{str(latest_projection.get('periodStart')).strip()}:{str(latest_projection.get('periodEnd')).strip()}"
        )

    horizon_values = sorted(
        {
            str(row.get("horizonScope") or "").strip()
            for row in current_rows
            if str(row.get("horizonScope") or "").strip()
        }
    )
    if not horizon_values:
        horizon_summary = {
            "status": "missing",
            "horizonsCovered": [],
            "summary": "Stored climate facts are not available for adaptation planning.",
        }
    elif horizon_values == ["cross_horizon"]:
        horizon_summary = {
            "status": "cross_horizon_only",
            "horizonsCovered": horizon_values,
            "summary": "Stored climate facts only resolve as cross-horizon advisory context.",
        }
    else:
        horizon_summary = {
            "status": "resolved",
            "horizonsCovered": horizon_values,
            "summary": "Stored climate facts resolve named scenario horizons for this field context.",
        }

    horizon_rows: list[dict[str, Any]] = []
    horizon_order = list(
        dict.fromkeys(
            [
                *[str(row.get("horizonScope") or "unknown").strip() or "unknown" for row in top_signals],
                *[str(row.get("horizonScope") or "unknown").strip() or "unknown" for row in indicator_rows],
            ]
        )
    )
    for horizon_scope in horizon_order:
        signal_rows = [row for row in top_signals if str(row.get("horizonScope") or "").strip() == horizon_scope]
        indicator_codes = [
            str(_field_phase6_indicator_supporting_label(row) or "").strip()
            for row in indicator_rows
            if str(row.get("horizonScope") or "").strip() == horizon_scope
            and str(_field_phase6_indicator_supporting_label(row) or "").strip()
        ]
        recommended_for_horizon: list[str] = []
        for row in signal_rows:
            _append_unique_many(recommended_for_horizon, row.get("recommendedThemes") or [])
        pressure_level = "exploratory"
        if signal_rows:
            pressure_level = max(
                (str(row.get("priorityLevel") or "exploratory").strip().lower() for row in signal_rows),
                key=lambda value: _CLIMATE_PRIORITY_RANK.get(value, 0),
            )
        elif indicator_codes:
            pressure_level = "low"
        horizon_rows.append(
            {
                "horizonScope": horizon_scope,
                "suitabilityStatus": "pressure" if pressure_level in {"medium", "high"} else "monitor",
                "pressureLevel": pressure_level,
                "recommendedThemes": recommended_for_horizon or (["gather_more_evidence"] if indicator_codes else []),
                "supportingIndicators": indicator_codes,
                "summary": (
                    "Stored adaptation signals indicate material planning pressure for this horizon."
                    if pressure_level in {"medium", "high"}
                    else "Stored climate facts support monitoring at this horizon."
                ),
            }
        )

    suitability_signal_rows = [
        row
        for row in top_signals
        if str(row.get("signalType") or "").strip() != "climateDataGap"
    ]
    if suitability_signal_rows:
        suitability_pressure_status = max(
            (str(row.get("priorityLevel") or "exploratory").strip().lower() for row in suitability_signal_rows),
            key=lambda value: _CLIMATE_PRIORITY_RANK.get(value, 0),
        )
    elif indicator_rows:
        suitability_pressure_status = "low"
    else:
        suitability_pressure_status = "exploratory"

    return {
        "fieldUri": str(identity.get("fieldUri") or "").strip(),
        "activeCropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
        "planningContext": {
            "planningContextMode": planning_context_mode,
            "cropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
            "cropTypeUri": str(crop_context.get("cropTypeUri") or "").strip() or None,
            "varietyUri": resolved_variety_uri,
            "summary": planning_context_summary,
        },
        "topSignals": top_signals,
        "horizonSummary": horizon_summary,
        "recommendedThemes": recommended_themes,
        "confidenceSummary": {
            "status": confidence_status,
            "summary": (
                "Stored climate facts provide a coherent planning signal for this field."
                if confidence_status == "high"
                else "Stored climate facts are usable, but geography-fit or uncertainty still limits confidence."
                if confidence_status == "medium"
                else "Stored climate facts exist, but adaptation confidence remains limited."
                if confidence_status == "low"
                else "Stored climate facts are not yet sufficient for a decision-ready adaptation summary."
            ),
        },
        "evidenceGaps": evidence_gaps,
        "cropOrVarietyContext": {
            "planningContextMode": planning_context_mode,
            "cropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
            "cropTypeUri": str(crop_context.get("cropTypeUri") or "").strip() or None,
            "varietyUri": resolved_variety_uri,
            "contextStatus": "resolved" if planning_context_mode != "generic_field" else "generic",
            "summary": planning_context_summary,
        },
        "horizonRows": horizon_rows,
        "indicatorHighlights": indicator_highlights,
        "suitabilityPressureSummary": {
            "status": suitability_pressure_status,
            "summary": (
                "Stored climate adaptation signals indicate elevated suitability pressure for the active crop context."
                if suitability_pressure_status in {"medium", "high"}
                else "Stored climate facts support monitoring rather than immediate crop-change pressure."
                if suitability_pressure_status == "low"
                else "Suitability outlook remains exploratory because stored adaptation signals are incomplete."
            ),
        },
        "indicatorRows": indicator_rows,
        "scenarioSet": scenario_set or (["unspecified_scenario"] if current_projection_facts else []),
        "baselinePolicy": baseline_policy,
        "geographyFitSummary": {
            "status": geography_fit_status,
            "summary": (
                "Stored climate facts are field-mapped for this parcel context."
                if geography_fit_status == "mapped"
                else "Stored climate facts are only partly reconciled to parcel geography."
                if geography_fit_status == "partial"
                else "Stored climate facts currently resolve only through broader regional proxies."
                if geography_fit_status == "regional_only"
                else "No usable geography-fit summary is available for stored climate facts."
            ),
        },
        "freshnessSummary": {
            "status": freshness_status,
            "summary": (
                "Stored climate facts are fresh against the current phase-6 runtime."
                if freshness_status == "fresh"
                else "Stored climate facts are present but freshness handling is incomplete."
                if freshness_status == "partial"
                else "Stored climate facts are stale and should be refreshed before operational use."
            ),
        },
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
    }


def _field_phase6_trait_assertion_map(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for item in profile.get("traitAssertions") or []:
        if not isinstance(item, dict):
            continue
        trait_code = str(item.get("traitCode") or "").strip().lower()
        if trait_code and trait_code not in mapped:
            mapped[trait_code] = item
    return mapped


def _field_phase6_adaptation_trait_mismatches(
    *,
    pedoclimatic_profile: Optional[dict[str, Any]],
    crop_adaptation_profile: Optional[dict[str, Any]],
) -> list[str]:
    if not isinstance(pedoclimatic_profile, dict) or not isinstance(crop_adaptation_profile, dict):
        return []

    pedo_rainfall = str(pedoclimatic_profile.get("rainfallRegimeClassCode") or "").strip().lower()
    gdd_annual = _as_number(pedoclimatic_profile.get("gddAnnual"))
    traits = _field_phase6_trait_assertion_map(crop_adaptation_profile)
    mismatches: list[str] = []

    rainfall_trait = traits.get("rainfall_regime_class") or {}
    rainfall_trait_value = str(rainfall_trait.get("valueText") or "").strip().lower()
    if pedo_rainfall and rainfall_trait_value and rainfall_trait_value not in {"other", pedo_rainfall}:
        mismatches.append("trait_rainfall_regime_mismatch")

    gdd_req_min = _as_number((traits.get("gdd_req_min") or {}).get("valueNumeric"))
    gdd_req_max = _as_number((traits.get("gdd_req_max") or {}).get("valueNumeric"))
    if gdd_annual is not None and gdd_req_min is not None and gdd_annual < gdd_req_min:
        mismatches.append("trait_gdd_below_min")
    if gdd_annual is not None and gdd_req_max is not None and gdd_annual > gdd_req_max:
        mismatches.append("trait_gdd_above_max")
    return mismatches


def build_field_climate_adaptation_context(
    *,
    passport: dict[str, Any],
    water_context: dict[str, Any],
    eo_context: dict[str, Any],
    benchmark_context: dict[str, Any],
    climate_hazard_profiles: list[dict[str, Any]],
    pedoclimatic_profiles: list[dict[str, Any]],
    variety_risk_profiles: list[dict[str, Any]],
    crop_adaptation_profiles: list[dict[str, Any]],
    climate_projection_facts: Optional[list[dict[str, Any]]] = None,
    climate_adaptation_signals: Optional[list[dict[str, Any]]] = None,
    permanent_crop_component_snapshots: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    identity = passport.get("identity") if isinstance(passport.get("identity"), dict) else {}
    crop_context = passport.get("cropContext") if isinstance(passport.get("cropContext"), dict) else {}
    daily_state = passport.get("dailyState") if isinstance(passport.get("dailyState"), dict) else {}
    water_balance = (
        water_context.get("waterBalanceSummary") if isinstance(water_context.get("waterBalanceSummary"), dict) else {}
    )
    latest_pedoclimatic = _latest_item(pedoclimatic_profiles, "recordedAt", "createdAt") or {}
    latest_risk = _latest_item(variety_risk_profiles, "assessedAt", "createdAt") or {}
    risk_variety_uri = str(latest_risk.get("varietyUri") or "").strip() or None
    permanent_crop_variety_context = resolve_permanent_crop_variety_context(
        permanent_crop_component_snapshots or [],
    )
    candidate_variety_uri = (
        risk_variety_uri
        or str(permanent_crop_variety_context.get("varietyUri") or "").strip()
        or None
    )
    variety_context_source = (
        "variety_risk_profile"
        if risk_variety_uri
        else "permanent_crop_component_snapshot"
        if candidate_variety_uri
        else None
    )
    matching_adaptation_profiles = [
        row
        for row in crop_adaptation_profiles
        if str(row.get("varietyUri") or "").strip()
        and (
            candidate_variety_uri is None
            or str(row.get("varietyUri") or "").strip() == candidate_variety_uri
        )
    ]
    latest_adaptation = _latest_item(matching_adaptation_profiles or crop_adaptation_profiles, "recordedAt", "createdAt") or {}

    stored_projection_facts = climate_projection_facts or []
    stored_adaptation_signals = climate_adaptation_signals or []
    if stored_projection_facts or stored_adaptation_signals:
        return _build_field_climate_adaptation_context_from_stored(
            passport=passport,
            water_context=water_context,
            eo_context=eo_context,
            benchmark_context=benchmark_context,
            climate_projection_facts=stored_projection_facts,
            climate_adaptation_signals=stored_adaptation_signals,
            candidate_variety_uri=candidate_variety_uri,
            variety_context_source=variety_context_source,
            permanent_crop_component_snapshots=permanent_crop_component_snapshots,
        )

    drought_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "drought"
        ],
        "recordedAt",
        "createdAt",
    )
    flood_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "flood"
        ],
        "recordedAt",
        "createdAt",
    )
    frost_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "frost"
        ],
        "recordedAt",
        "createdAt",
    )
    heat_row = _latest_item(
        [
            row
            for row in climate_hazard_profiles
            if str(row.get("hazardTypeCode") or "").strip().lower() == "heatwave"
            or "heat" in str(row.get("hazardMetricCode") or "").strip().lower()
        ],
        "recordedAt",
        "createdAt",
    )

    evidence_refs = collect_passport_evidence_uris(passport)
    trace_refs: list[str] = []
    _append_unique_many(evidence_refs, water_context.get("evidenceRefs") or [])
    _append_unique_many(evidence_refs, eo_context.get("evidenceRefs") or [])
    _append_unique_many(evidence_refs, benchmark_context.get("evidenceRefs") or [])
    _append_unique_many(trace_refs, water_context.get("traceRefs") or [])
    _append_unique_many(trace_refs, eo_context.get("traceRefs") or [])
    _append_unique_many(trace_refs, benchmark_context.get("traceRefs") or [])
    if variety_context_source == "permanent_crop_component_snapshot":
        _append_unique_many(evidence_refs, permanent_crop_variety_context.get("evidenceRefs") or [])
        _append_unique_many(trace_refs, permanent_crop_variety_context.get("traceRefs") or [])

    for row in climate_hazard_profiles:
        _append_unique(trace_refs, str(row.get("profileUri") or "").strip())
        _append_unique(trace_refs, str(row.get("dataSourceRef") or "").strip())
        _append_unique(trace_refs, str(row.get("methodRef") or "").strip())
    if latest_pedoclimatic:
        _append_unique(trace_refs, str(latest_pedoclimatic.get("profileUri") or "").strip())
        _append_unique(trace_refs, str(latest_pedoclimatic.get("soilSourceRef") or "").strip())
        _append_unique(trace_refs, str(latest_pedoclimatic.get("climateSourceRef") or "").strip())
        _append_unique(trace_refs, str(latest_pedoclimatic.get("gddMethodRef") or "").strip())
    if latest_risk:
        _append_unique(trace_refs, str(latest_risk.get("assessmentUri") or latest_risk.get("uri") or "").strip())
        _append_unique(trace_refs, str(latest_risk.get("methodRef") or "").strip())
        _append_unique(trace_refs, str(latest_risk.get("pedoclimaticProfileUri") or "").strip())
    if latest_adaptation:
        _append_unique(trace_refs, str(latest_adaptation.get("profileUri") or latest_adaptation.get("uri") or "").strip())
        for item in latest_adaptation.get("traitAssertions") or []:
            if not isinstance(item, dict):
                continue
            _append_unique(evidence_refs, str(item.get("evidenceUri") or "").strip())

    evidence_gaps: list[str] = []
    if not climate_hazard_profiles:
        _append_unique(evidence_gaps, "climate_hazard_profile_observation")
    if not latest_pedoclimatic:
        _append_unique(evidence_gaps, "field_pedoclimatic_profile_observation")
    if not str(crop_context.get("cropInstanceUri") or "").strip() and not str(crop_context.get("cropTypeUri") or "").strip():
        _append_unique(evidence_gaps, "field_declaration_snapshot")
    if climate_hazard_profiles and not any(
        str(row.get("baselineStartDate") or "").strip() and str(row.get("baselineEndDate") or "").strip()
        for row in climate_hazard_profiles
    ):
        _append_unique(evidence_gaps, "climate_projection_baseline_context")
    if climate_hazard_profiles:
        _append_unique(evidence_gaps, "scenario_horizon_context")
    if candidate_variety_uri and not latest_adaptation:
        _append_unique(evidence_gaps, "crop_adaptation_profile_observation")

    planning_context_mode = (
        "current_crop"
        if str(crop_context.get("cropInstanceUri") or "").strip()
        else "candidate_crop"
        if candidate_variety_uri
        else "generic_field"
    )
    planning_context_summary = (
        "Climate adaptation summary is anchored to the current crop instance."
        if planning_context_mode == "current_crop" and variety_context_source != "permanent_crop_component_snapshot"
        else "Climate adaptation summary is anchored to the current crop instance and uses dominant permanent-crop composition for variety context."
        if planning_context_mode == "current_crop"
        else "Climate adaptation summary is anchored to candidate variety evidence."
        if planning_context_mode == "candidate_crop" and variety_context_source != "permanent_crop_component_snapshot"
        else "Climate adaptation summary is anchored to source-native permanent-crop composition because no variety-risk record is available."
        if planning_context_mode == "candidate_crop"
        else "Climate adaptation summary is field-generic because crop or variety context is incomplete."
    )

    confidence_status = _field_phase6_confidence_status(
        climate_profiles=climate_hazard_profiles,
        pedoclimatic_profile=latest_pedoclimatic,
        evidence_gaps=evidence_gaps,
    )
    horizon_summary = _field_phase6_horizon_summary(
        climate_profiles=climate_hazard_profiles,
        evidence_gaps=evidence_gaps,
    )

    top_signals: list[dict[str, Any]] = []
    water_deficit_status = str(water_balance.get("waterDeficitProxyStatus") or "unknown").strip().lower()
    drought_context_status = str(water_balance.get("droughtContextStatus") or "unknown").strip()
    flood_context_status = str(water_balance.get("floodContextStatus") or "unknown").strip()
    drainage_class = str(latest_pedoclimatic.get("drainageClassCode") or "").strip().lower()
    eo_stage_status = str(eo_context.get("stageStatus") or "").strip().lower()
    trait_mismatches = _field_phase6_adaptation_trait_mismatches(
        pedoclimatic_profile=latest_pedoclimatic if latest_pedoclimatic else None,
        crop_adaptation_profile=latest_adaptation if latest_adaptation else None,
    )
    aggregate_risk = str(latest_risk.get("aggregateRiskClassCode") or "").strip().lower()

    if drought_row or heat_row or water_deficit_status in {"moderate", "high"} or drought_context_status in {"regional-watch", "regional-elevated"}:
        priority = "medium"
        if water_deficit_status == "high" or drought_context_status == "regional-elevated" or heat_row:
            priority = "high"
        reasons = []
        if drought_context_status:
            reasons.append(f"drought_context:{drought_context_status}")
        if water_deficit_status:
            reasons.append(f"water_deficit_proxy:{water_deficit_status}")
        if drought_row:
            reasons.append(f"hazard_metric:{str(drought_row.get('hazardMetricCode') or 'drought').strip()}")
        if heat_row:
            reasons.append(f"hazard_metric:{str(heat_row.get('hazardMetricCode') or 'heatwave').strip()}")
        top_signals.append(
            {
                "signalType": "waterDemandIncrease",
                "priorityLevel": priority,
                "horizonScope": "cross_horizon" if climate_hazard_profiles else "unknown",
                "confidenceStatus": _field_phase6_signal_confidence(
                    row=heat_row or drought_row,
                    default_status=confidence_status,
                ),
                "recommendedThemes": ["review_irrigation", "review_soil_cover"],
                "reasonCodes": reasons,
                "traceRefs": [item for item in [str((heat_row or {}).get("profileUri") or "").strip(), str((drought_row or {}).get("profileUri") or "").strip()] if item],
                "evidenceRefs": [],
            }
        )

    if flood_row or flood_context_status in {"watch", "elevated"} or drainage_class in {"very_poorly_drained", "poorly_drained", "somewhat_poorly_drained"}:
        signal_type = (
            "waterloggingRisk"
            if drainage_class in {"very_poorly_drained", "poorly_drained", "somewhat_poorly_drained"}
            else "heavyRainRunoffRisk"
        )
        priority = "medium"
        if flood_context_status == "elevated" or signal_type == "waterloggingRisk":
            priority = "high"
        reasons = []
        if flood_context_status:
            reasons.append(f"flood_context:{flood_context_status}")
        if drainage_class:
            reasons.append(f"drainage_class:{drainage_class}")
        if flood_row:
            reasons.append(f"hazard_metric:{str(flood_row.get('hazardMetricCode') or 'flood').strip()}")
        top_signals.append(
            {
                "signalType": signal_type,
                "priorityLevel": priority,
                "horizonScope": "cross_horizon" if climate_hazard_profiles else "unknown",
                "confidenceStatus": _field_phase6_signal_confidence(
                    row=flood_row,
                    default_status=confidence_status,
                ),
                "recommendedThemes": ["review_drainage", "review_soil_cover"],
                "reasonCodes": reasons,
                "traceRefs": [str((flood_row or {}).get("profileUri") or "").strip()] if flood_row else [],
                "evidenceRefs": [],
            }
        )

    if frost_row or heat_row or eo_stage_status in {"behind", "ahead"} or latest_pedoclimatic.get("gddAnnual") is not None:
        reasons = []
        if eo_stage_status:
            reasons.append(f"phenology_status:{eo_stage_status}")
        if frost_row:
            reasons.append(f"hazard_metric:{str(frost_row.get('hazardMetricCode') or 'frost').strip()}")
        if heat_row:
            reasons.append(f"hazard_metric:{str(heat_row.get('hazardMetricCode') or 'heatwave').strip()}")
        if latest_pedoclimatic.get("gddAnnual") is not None:
            reasons.append("pedoclimatic_gdd_context")
        top_signals.append(
            {
                "signalType": "phenologyShift",
                "priorityLevel": "medium" if frost_row or heat_row or eo_stage_status in {"behind", "ahead"} else "low",
                "horizonScope": "cross_horizon" if climate_hazard_profiles else "unknown",
                "confidenceStatus": _field_phase6_signal_confidence(
                    row=frost_row or heat_row or latest_pedoclimatic,
                    default_status=confidence_status,
                ),
                "recommendedThemes": ["review_sowing_window", "review_variety"],
                "reasonCodes": reasons,
                "traceRefs": [
                    item
                    for item in [
                        str((frost_row or {}).get("profileUri") or "").strip(),
                        str((heat_row or {}).get("profileUri") or "").strip(),
                    ]
                    if item
                ],
                "evidenceRefs": [],
            }
        )

    if aggregate_risk in {"medium", "high"} or trait_mismatches:
        priority = "high" if aggregate_risk == "high" or len(trait_mismatches) >= 2 else "medium"
        reasons = []
        if aggregate_risk:
            reasons.append(f"aggregate_risk:{aggregate_risk}")
        reasons.extend(trait_mismatches)
        top_signals.append(
            {
                "signalType": "cropSuitabilityPressure",
                "priorityLevel": priority,
                "horizonScope": "cross_horizon" if climate_hazard_profiles else "unknown",
                "confidenceStatus": _field_phase6_signal_confidence(
                    row=latest_risk or latest_adaptation or latest_pedoclimatic,
                    default_status=confidence_status,
                ),
                "recommendedThemes": ["review_variety", "review_crop_mix"],
                "reasonCodes": reasons or ["generic_crop_suitability_review"],
                "traceRefs": [
                    item
                    for item in [
                        str((latest_risk or {}).get("assessmentUri") or (latest_risk or {}).get("uri") or "").strip(),
                        str((latest_adaptation or {}).get("profileUri") or "").strip(),
                    ]
                    if item
                ],
                "evidenceRefs": [
                    item
                    for item in [
                        str((latest_risk or {}).get("expectedDiseasePressureRef") or "").strip(),
                        str((latest_risk or {}).get("managementAssumptionsRef") or "").strip(),
                    ]
                    if item
                ],
            }
        )

    if evidence_gaps:
        gap_reasons = list(evidence_gaps)
        top_signals.append(
            {
                "signalType": "climateDataGap",
                "priorityLevel": "exploratory",
                "horizonScope": "cross_horizon" if climate_hazard_profiles else "unknown",
                "confidenceStatus": "low" if climate_hazard_profiles else "unknown",
                "recommendedThemes": ["gather_more_evidence"],
                "reasonCodes": gap_reasons,
                "traceRefs": [],
                "evidenceRefs": [],
            }
        )

    top_signals = sorted(top_signals, key=_field_phase6_signal_sort_key)[:4]
    recommended_themes: list[str] = []
    for row in top_signals:
        _append_unique_many(recommended_themes, row.get("recommendedThemes") or [])
    if not recommended_themes:
        recommended_themes.append("gather_more_evidence" if evidence_gaps else "no_change")

    indicator_rows: list[dict[str, Any]] = []
    for row in climate_hazard_profiles:
        hazard_type = str(row.get("hazardTypeCode") or "").strip().lower() or "other"
        metric_code = str(row.get("hazardMetricCode") or "").strip() or hazard_type
        indicator_rows.append(
            {
                "indicatorCode": metric_code,
                "indicatorValue": _as_number(row.get("frequencyValue")),
                "unitCode": str(row.get("frequencyKindCode") or "").strip() or None,
                "geographyScope": "regional_context",
                "horizonScope": "cross_horizon",
                "uncertaintyClass": _field_phase6_signal_confidence(row=row, default_status="unknown"),
                "sourceRef": str(row.get("dataSourceRef") or "").strip() or None,
                "summary": f"{hazard_type} support recorded for metric {metric_code}.",
            }
        )
    if latest_pedoclimatic and latest_pedoclimatic.get("gddAnnual") is not None:
        indicator_rows.append(
            {
                "indicatorCode": "gdd_annual",
                "indicatorValue": _as_number(latest_pedoclimatic.get("gddAnnual")),
                "unitCode": "gdd",
                "geographyScope": "field_context",
                "horizonScope": "cross_horizon",
                "uncertaintyClass": _field_phase6_signal_confidence(row=latest_pedoclimatic, default_status=confidence_status),
                "sourceRef": str(latest_pedoclimatic.get("climateSourceRef") or "").strip() or None,
                "summary": "Field pedoclimatic profile contributes annual growing degree day context.",
            }
        )

    indicator_highlights = indicator_rows[:4]
    suitability_pressure_status = "exploratory"
    if any(str(item.get("signalType") or "").strip() == "cropSuitabilityPressure" for item in top_signals):
        suitability_pressure_status = "high" if aggregate_risk == "high" else "medium"
    elif any(str(item.get("signalType") or "").strip() == "waterDemandIncrease" for item in top_signals):
        suitability_pressure_status = "medium"
    elif climate_hazard_profiles:
        suitability_pressure_status = "low"

    horizon_rows = [
        {
            "horizonScope": "cross_horizon",
            "suitabilityStatus": "pressure" if suitability_pressure_status in {"medium", "high"} else "monitor",
            "pressureLevel": suitability_pressure_status,
            "recommendedThemes": recommended_themes,
            "supportingIndicators": [
                str(item.get("indicatorCode") or "").strip()
                for item in indicator_highlights
                if str(item.get("indicatorCode") or "").strip()
            ],
            "summary": (
                "Current repo climate inputs support only cross-horizon suitability review."
                if climate_hazard_profiles
                else "Suitability outlook is not decision-ready without climate support records."
            ),
        }
    ]

    latest_authority = _latest_item(passport.get("officialLinks") or [], "recordedAt", "createdAt") or {}
    geography_fit_status = "missing"
    if climate_hazard_profiles and latest_pedoclimatic and str(latest_pedoclimatic.get("regionCode") or "").strip():
        geography_fit_status = "mapped"
    elif climate_hazard_profiles and latest_authority:
        geography_fit_status = "partial"
    elif climate_hazard_profiles:
        geography_fit_status = "regional_only"

    stale_flags = list(((passport.get("freshness") or {}).get("staleFlags")) or [])
    freshness_status = "fresh"
    if stale_flags:
        freshness_status = "stale"
    elif evidence_gaps:
        freshness_status = "partial"

    baseline_policy = "not_available"
    if str(latest_pedoclimatic.get("climateReferencePeriod") or "").strip():
        baseline_policy = str(latest_pedoclimatic.get("climateReferencePeriod") or "").strip()
    elif str(latest_pedoclimatic.get("baselineStartDate") or "").strip() and str(latest_pedoclimatic.get("baselineEndDate") or "").strip():
        baseline_policy = (
            f"{str(latest_pedoclimatic.get('baselineStartDate')).strip()}:{str(latest_pedoclimatic.get('baselineEndDate')).strip()}"
        )
    elif climate_hazard_profiles:
        baseline_rows = [
            row
            for row in climate_hazard_profiles
            if str(row.get("baselineStartDate") or "").strip() and str(row.get("baselineEndDate") or "").strip()
        ]
        latest_baseline = _latest_item(baseline_rows, "recordedAt", "createdAt") or {}
        if latest_baseline:
            baseline_policy = (
                f"{str(latest_baseline.get('baselineStartDate')).strip()}:{str(latest_baseline.get('baselineEndDate')).strip()}"
            )

    return {
        "fieldUri": str(identity.get("fieldUri") or "").strip(),
        "activeCropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
        "planningContext": {
            "planningContextMode": planning_context_mode,
            "cropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
            "cropTypeUri": str(crop_context.get("cropTypeUri") or "").strip() or None,
            "varietyUri": candidate_variety_uri,
            "summary": planning_context_summary,
        },
        "topSignals": top_signals,
        "horizonSummary": horizon_summary,
        "recommendedThemes": recommended_themes,
        "confidenceSummary": {
            "status": confidence_status,
            "summary": (
                "Climate adaptation support is usable only as low-confidence advisory context until scenario and horizon metadata are available."
                if confidence_status == "low"
                else "Climate adaptation support is reasonably coherent across the current parcel context."
                if confidence_status == "medium"
                else "Climate adaptation support is not yet decision-ready."
            ),
        },
        "evidenceGaps": evidence_gaps,
        "cropOrVarietyContext": {
            "planningContextMode": planning_context_mode,
            "cropInstanceUri": str(crop_context.get("cropInstanceUri") or "").strip() or None,
            "cropTypeUri": str(crop_context.get("cropTypeUri") or "").strip() or None,
            "varietyUri": candidate_variety_uri,
            "contextStatus": "resolved" if planning_context_mode != "generic_field" else "generic",
            "summary": planning_context_summary,
        },
        "horizonRows": horizon_rows,
        "indicatorHighlights": indicator_highlights,
        "suitabilityPressureSummary": {
            "status": suitability_pressure_status,
            "summary": (
                "Candidate crop or variety suitability pressure is elevated in the current climate context."
                if suitability_pressure_status in {"medium", "high"}
                else "Current climate context supports monitoring rather than an immediate suitability change."
                if suitability_pressure_status == "low"
                else "Suitability outlook remains exploratory because the climate context is incomplete."
            ),
        },
        "indicatorRows": indicator_rows,
        "scenarioSet": ["unspecified_scenario"] if climate_hazard_profiles else [],
        "baselinePolicy": baseline_policy,
        "geographyFitSummary": {
            "status": geography_fit_status,
            "summary": (
                "Field, regional, and pedoclimatic mapping strata are available for this climate context."
                if geography_fit_status == "mapped"
                else "Climate context is only partially mapped back to parcel-specific geography."
                if geography_fit_status == "partial"
                else "Climate context currently resolves only at a broader regional layer."
                if geography_fit_status == "regional_only"
                else "No usable climate geography fit summary is available."
            ),
        },
        "freshnessSummary": {
            "status": freshness_status,
            "summary": (
                "Climate adaptation context is current against parcel freshness checks."
                if freshness_status == "fresh"
                else "Climate adaptation context is usable but still carries evidence gaps."
                if freshness_status == "partial"
                else "Freshness issues reduce confidence in the current climate adaptation context."
            ),
        },
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
    }


def build_field_climate_adaptation_summary_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "planningContext": context.get("planningContext") or {},
        "topSignals": context.get("topSignals") or [],
        "horizonSummary": context.get("horizonSummary") or {},
        "recommendedThemes": context.get("recommendedThemes") or [],
        "confidenceSummary": context.get("confidenceSummary") or {},
        "evidenceGaps": context.get("evidenceGaps") or [],
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


def build_field_climate_suitability_outlook_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "cropOrVarietyContext": context.get("cropOrVarietyContext") or {},
        "horizonRows": context.get("horizonRows") or [],
        "indicatorHighlights": context.get("indicatorHighlights") or [],
        "suitabilityPressureSummary": context.get("suitabilityPressureSummary") or {},
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


def build_field_climate_indicator_trends_projection(
    *,
    context: dict[str, Any],
) -> dict[str, Any]:
    return {
        "indicatorRows": context.get("indicatorRows") or [],
        "scenarioSet": context.get("scenarioSet") or [],
        "baselinePolicy": context.get("baselinePolicy") or "not_available",
        "geographyFitSummary": context.get("geographyFitSummary") or {},
        "freshnessSummary": context.get("freshnessSummary") or {},
        "evidenceRefs": context.get("evidenceRefs") or [],
        "traceRefs": context.get("traceRefs") or [],
    }


_CLIMATE_PLAN_CARD_SIGNAL_TYPES: dict[str, tuple[str, ...]] = {
    "frostTrend": ("frostShiftRisk",),
    "heatTrend": ("heatStressRisk", "warmingTrend"),
    "drySpellTrend": ("waterDemandIncrease",),
    "varietyFit": ("cropSuitabilityPressure", "adaptationOpportunity"),
}

_CLIMATE_PLAN_CARD_INDICATOR_HINTS: dict[str, tuple[str, ...]] = {
    "frostTrend": ("frost", "chill", "cold", "vernal"),
    "heatTrend": ("heat", "temp", "warm", "gdd"),
    "drySpellTrend": ("dry", "drought", "precip", "rain", "et", "evapo", "spi"),
}

_CLIMATE_PLAN_CARD_DEFAULT_THEME: dict[str, str] = {
    "frostTrend": "review_frost_protection",
    "heatTrend": "review_variety",
    "drySpellTrend": "review_irrigation",
    "irrigationValue": "review_irrigation",
    "varietyFit": "review_variety",
}


def _field_climate_plan_supporting_indicators(
    *,
    card_type: str,
    indicator_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hints = _CLIMATE_PLAN_CARD_INDICATOR_HINTS.get(card_type, ())
    if not hints:
        return []
    matched: list[dict[str, Any]] = []
    for row in indicator_rows:
        combined = " ".join(
            [
                str(row.get("indicatorCode") or "").strip().lower(),
                str(row.get("summary") or "").strip().lower(),
                str(row.get("sourceRef") or "").strip().lower(),
            ]
        )
        if any(hint in combined for hint in hints):
            matched.append(row)
    return matched


def _field_climate_plan_first_signal(
    *,
    card_type: str,
    top_signals: list[dict[str, Any]],
) -> Optional[dict[str, Any]]:
    allowed_types = _CLIMATE_PLAN_CARD_SIGNAL_TYPES.get(card_type, ())
    for row in top_signals:
        if str(row.get("signalType") or "").strip() in allowed_types:
            return row
    return None


def _field_climate_plan_recommended_theme(
    *,
    card_type: str,
    values: list[str],
) -> str:
    for value in values:
        current = str(value or "").strip()
        if current:
            return current
    return _CLIMATE_PLAN_CARD_DEFAULT_THEME.get(card_type, "unknown")


def _field_climate_plan_signal_display_state(
    *,
    confidence_status: str,
    evidence_gaps: list[str],
) -> str:
    normalized = str(confidence_status or "").strip().lower()
    if normalized in {"low", "unknown"} or evidence_gaps:
        return "limited"
    return "live"


def _field_climate_plan_signal_headline(
    *,
    card_type: str,
    trend_direction: str,
    display_state: str,
) -> str:
    if card_type == "frostTrend":
        return (
            "Frost planning signal is limited"
            if display_state == "limited"
            else "Frost pressure is shifting"
            if trend_direction == "mixed"
            else "Frost pressure is rising"
            if trend_direction == "up"
            else "Frost trend is stable"
        )
    if card_type == "heatTrend":
        return (
            "Heat planning signal is limited"
            if display_state == "limited"
            else "Heat pressure is rising"
            if trend_direction == "up"
            else "Heat trend is stable"
        )
    if card_type == "drySpellTrend":
        return (
            "Dry-spell planning signal is limited"
            if display_state == "limited"
            else "Dry-spell pressure is building"
            if trend_direction == "up"
            else "Dry-spell trend is stable"
        )
    if card_type == "varietyFit":
        return (
            "Variety fit is only partly resolved"
            if display_state == "limited"
            else "Variety fit is under pressure"
            if trend_direction == "up"
            else "Variety fit looks stable"
        )
    return "Climate planning signal"


def _field_climate_plan_signal_summary(
    *,
    card_type: str,
    display_state: str,
) -> str:
    summaries = {
        "frostTrend": (
            "Frost-related climate evidence exists, but geography fit or crop context still limits confidence."
            if display_state == "limited"
            else "Stored climate support points to a frost-related planning shift for this field."
        ),
        "heatTrend": (
            "Heat-related climate evidence exists, but the current planning context is still partial."
            if display_state == "limited"
            else "Stored climate support indicates rising heat pressure for this field."
        ),
        "drySpellTrend": (
            "Dry-spell planning evidence exists, but the climate and water context is still partial."
            if display_state == "limited"
            else "Stored climate support indicates rising dry-spell pressure for this field."
        ),
        "varietyFit": (
            "Current crop or variety fit can only be assessed partially from the available climate context."
            if display_state == "limited"
            else "Current crop or variety context is under climate suitability pressure."
        ),
    }
    return summaries.get(card_type, "Climate planning evidence is available.")


def _field_climate_plan_signal_trend_direction(
    *,
    card_type: str,
    signal: Optional[dict[str, Any]],
    supporting_indicators: list[dict[str, Any]],
) -> str:
    signal_type = str((signal or {}).get("signalType") or "").strip()
    if card_type == "frostTrend":
        if signal_type == "frostShiftRisk":
            return "mixed"
        return "mixed" if supporting_indicators else "unknown"
    if card_type == "heatTrend":
        if signal_type in {"heatStressRisk", "warmingTrend"} or supporting_indicators:
            return "up"
        return "stable"
    if card_type == "drySpellTrend":
        if signal_type == "waterDemandIncrease" or supporting_indicators:
            return "up"
        return "stable"
    if card_type == "varietyFit":
        if signal_type in {"cropSuitabilityPressure", "adaptationOpportunity"}:
            priority = str((signal or {}).get("priorityLevel") or "").strip().lower()
            if priority in {"medium", "high"}:
                return "up"
            if priority == "low":
                return "stable"
        return "unknown"
    return "unknown"


def _build_field_climate_plan_signal_card(
    *,
    card_type: str,
    top_signals: list[dict[str, Any]],
    indicator_rows: list[dict[str, Any]],
    evidence_gaps: list[str],
    fallback_evidence_refs: list[str],
    fallback_trace_refs: list[str],
) -> Optional[dict[str, Any]]:
    signal = _field_climate_plan_first_signal(card_type=card_type, top_signals=top_signals)
    supporting_indicators = _field_climate_plan_supporting_indicators(
        card_type=card_type,
        indicator_rows=indicator_rows,
    )
    if signal is None and not supporting_indicators:
        return None

    confidence_status = str((signal or {}).get("confidenceStatus") or "unknown").strip() or "unknown"
    display_state = _field_climate_plan_signal_display_state(
        confidence_status=confidence_status,
        evidence_gaps=evidence_gaps,
    )
    trend_direction = _field_climate_plan_signal_trend_direction(
        card_type=card_type,
        signal=signal,
        supporting_indicators=supporting_indicators,
    )
    horizon_scope = (
        str((signal or {}).get("horizonScope") or "").strip()
        or str((supporting_indicators[0] if supporting_indicators else {}).get("horizonScope") or "").strip()
        or "unknown"
    )

    reason_codes = [str(item or "").strip() for item in ((signal or {}).get("reasonCodes") or []) if str(item or "").strip()]
    if not reason_codes and signal is not None:
        _append_unique(reason_codes, f"signalType:{str(signal.get('signalType') or '').strip()}")
    for row in supporting_indicators[:2]:
        _append_unique(reason_codes, f"indicator:{str(row.get('indicatorCode') or '').strip()}")
    for gap in evidence_gaps:
        _append_unique(reason_codes, gap)

    evidence_refs = [str(item or "").strip() for item in ((signal or {}).get("evidenceRefs") or []) if str(item or "").strip()]
    trace_refs = [str(item or "").strip() for item in ((signal or {}).get("traceRefs") or []) if str(item or "").strip()]
    if not evidence_refs:
        for item in fallback_evidence_refs:
            _append_unique(evidence_refs, str(item or "").strip())
    if not trace_refs:
        for item in fallback_trace_refs:
            _append_unique(trace_refs, str(item or "").strip())
        for row in supporting_indicators[:2]:
            _append_unique(trace_refs, str(row.get("sourceRef") or "").strip())

    recommended_theme = _field_climate_plan_recommended_theme(
        card_type=card_type,
        values=list((signal or {}).get("recommendedThemes") or []),
    )
    return {
        "cardType": card_type,
        "displayState": display_state,
        "headline": _field_climate_plan_signal_headline(
            card_type=card_type,
            trend_direction=trend_direction,
            display_state=display_state,
        ),
        "summary": _field_climate_plan_signal_summary(
            card_type=card_type,
            display_state=display_state,
        ),
        "trendDirection": trend_direction,
        "horizonScope": horizon_scope,
        "confidenceStatus": confidence_status,
        "recommendedTheme": recommended_theme,
        "reasonCodes": reason_codes,
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
    }


def _build_field_climate_plan_irrigation_card(
    *,
    irrigation_projection: dict[str, Any],
) -> Optional[dict[str, Any]]:
    water_balance = (
        irrigation_projection.get("waterBalanceSummary")
        if isinstance(irrigation_projection.get("waterBalanceSummary"), dict)
        else {}
    )
    decision = str(irrigation_projection.get("decision") or "unknown").strip().lower() or "unknown"
    urgency_status = str(irrigation_projection.get("urgencyStatus") or "unknown").strip().lower() or "unknown"
    support_dataset_status = str(water_balance.get("supportDatasetStatus") or "").strip().lower()
    water_deficit_status = str(water_balance.get("waterDeficitProxyStatus") or "unknown").strip().lower()
    drought_context_status = str(water_balance.get("droughtContextStatus") or "unknown").strip().lower()
    flood_context_status = str(water_balance.get("floodContextStatus") or "unknown").strip().lower()
    required_evidence = [str(item or "").strip() for item in (irrigation_projection.get("requiredEvidence") or []) if str(item or "").strip()]
    has_support = support_dataset_status not in {"", "unknown", "none"}

    if decision == "unknown" and not has_support and not required_evidence:
        return None

    if flood_context_status in {"watch", "elevated"} and urgency_status in {"recommended", "urgent"}:
        trend_direction = "mixed"
    elif urgency_status in {"recommended", "urgent"} or water_deficit_status in {"moderate", "high"} or drought_context_status in {"regional-watch", "regional-elevated"}:
        trend_direction = "up"
    elif decision == "allow" and water_deficit_status == "low":
        trend_direction = "stable"
    else:
        trend_direction = "unknown"

    display_state = (
        "limited"
        if decision == "unknown" or required_evidence or not has_support
        else "live"
    )
    confidence_status = (
        "high"
        if support_dataset_status == "multi-source" and not required_evidence
        else "medium"
        if has_support and not required_evidence
        else "low"
        if has_support or required_evidence
        else "unknown"
    )
    reason_codes = [
        f"decision:{decision}",
        f"urgency:{urgency_status}",
        f"water_deficit_proxy:{water_deficit_status}",
        f"drought_context:{drought_context_status}",
        f"support_dataset:{support_dataset_status or 'none'}",
    ]
    if flood_context_status not in {"", "unknown"}:
        _append_unique(reason_codes, f"flood_context:{flood_context_status}")
    for item in required_evidence:
        _append_unique(reason_codes, item)

    return {
        "cardType": "irrigationValue",
        "displayState": display_state,
        "headline": (
            "Irrigation review is partially resolved"
            if display_state == "limited"
            else "Irrigation review is becoming relevant"
            if trend_direction == "up"
            else "Irrigation signal is mixed"
            if trend_direction == "mixed"
            else "Irrigation value looks stable"
        ),
        "summary": (
            "Irrigation review is relevant, but support data is still partial or indirect."
            if display_state == "limited"
            else "Current water-balance and climate context support irrigation review."
        ),
        "trendDirection": trend_direction,
        "horizonScope": "cross_horizon",
        "confidenceStatus": confidence_status,
        "recommendedTheme": "review_irrigation",
        "reasonCodes": reason_codes,
        "evidenceRefs": list(irrigation_projection.get("evidenceRefs") or []),
        "traceRefs": list(irrigation_projection.get("traceRefs") or []),
    }


def _build_field_climate_plan_variety_card(
    *,
    suitability_outlook: dict[str, Any],
    evidence_gaps: list[str],
) -> Optional[dict[str, Any]]:
    context = (
        suitability_outlook.get("cropOrVarietyContext")
        if isinstance(suitability_outlook.get("cropOrVarietyContext"), dict)
        else {}
    )
    horizon_rows = suitability_outlook.get("horizonRows") or []
    first_horizon = horizon_rows[0] if horizon_rows else {}
    context_status = str(context.get("contextStatus") or "missing").strip().lower() or "missing"
    pressure_status = str(((suitability_outlook.get("suitabilityPressureSummary") or {}).get("status")) or "exploratory").strip().lower() or "exploratory"

    if not horizon_rows and context_status == "missing":
        return None
    if pressure_status in {"exploratory", "unknown"} and not (first_horizon.get("supportingIndicators") or []):
        return None

    if pressure_status in {"medium", "high"}:
        trend_direction = "up"
    elif pressure_status == "low":
        trend_direction = "stable"
    else:
        trend_direction = "unknown"

    display_state = (
        "limited"
        if context_status != "resolved" or pressure_status in {"exploratory", "unknown"} or evidence_gaps
        else "live"
    )
    reason_codes = [
        f"context_status:{context_status}",
        f"pressure:{pressure_status}",
    ]
    for indicator in first_horizon.get("supportingIndicators") or []:
        _append_unique(reason_codes, f"indicator:{str(indicator or '').strip()}")
    for gap in evidence_gaps:
        _append_unique(reason_codes, gap)

    recommended_theme = _field_climate_plan_recommended_theme(
        card_type="varietyFit",
        values=list(first_horizon.get("recommendedThemes") or []),
    )
    confidence_status = "low" if display_state == "limited" else "medium"

    return {
        "cardType": "varietyFit",
        "displayState": display_state,
        "headline": (
            "Variety fit is only partly resolved"
            if display_state == "limited"
            else "Variety fit is under pressure"
            if trend_direction == "up"
            else "Variety fit looks stable"
        ),
        "summary": (
            "Current crop or variety fit can only be assessed partially from the available climate context."
            if display_state == "limited"
            else "Current crop or variety context is under climate suitability pressure."
            if trend_direction == "up"
            else "Current crop or variety context supports monitoring rather than an immediate change."
        ),
        "trendDirection": trend_direction,
        "horizonScope": str(first_horizon.get("horizonScope") or "unknown").strip() or "unknown",
        "confidenceStatus": confidence_status,
        "recommendedTheme": recommended_theme,
        "reasonCodes": reason_codes,
        "evidenceRefs": list(suitability_outlook.get("evidenceRefs") or []),
        "traceRefs": list(suitability_outlook.get("traceRefs") or []),
    }


def build_field_climate_plan_tab_projection(
    *,
    planning_context: dict[str, Any],
    adaptation_summary: dict[str, Any],
    suitability_outlook: dict[str, Any],
    indicator_trends: dict[str, Any],
    irrigation_readiness: dict[str, Any],
    master_enabled: bool,
    card_capabilities: dict[str, bool],
    detail_endpoints: Optional[dict[str, Optional[str]]] = None,
) -> dict[str, Any]:
    if not master_enabled or not any(card_capabilities.values()):
        return {
            "screenState": "hidden",
            "planningContext": planning_context or {},
            "freshness": {
                "projectionFacts": "unknown",
                "adaptationSignals": "unknown",
                "irrigationReadiness": "unknown",
                "varietyContext": str(
                    (((suitability_outlook.get("cropOrVarietyContext") or {}).get("contextStatus")) or "unknown")
                ).strip()
                or "unknown",
            },
            "cards": [],
            "evidenceGaps": [],
            "evidenceRefs": [],
            "traceRefs": [],
            "detailEndpoints": detail_endpoints or {},
        }

    top_signals = list(adaptation_summary.get("topSignals") or [])
    indicator_rows = list(indicator_trends.get("indicatorRows") or [])
    evidence_gaps = list(adaptation_summary.get("evidenceGaps") or [])
    fallback_evidence_refs = list(adaptation_summary.get("evidenceRefs") or [])
    fallback_trace_refs = list(adaptation_summary.get("traceRefs") or [])

    cards: list[dict[str, Any]] = []
    for card_type in ("frostTrend", "heatTrend", "drySpellTrend"):
        if not card_capabilities.get(card_type, False):
            continue
        card = _build_field_climate_plan_signal_card(
            card_type=card_type,
            top_signals=top_signals,
            indicator_rows=indicator_rows,
            evidence_gaps=evidence_gaps,
            fallback_evidence_refs=fallback_evidence_refs,
            fallback_trace_refs=fallback_trace_refs,
        )
        if card is not None:
            cards.append(card)

    if card_capabilities.get("irrigationValue", False):
        irrigation_card = _build_field_climate_plan_irrigation_card(
            irrigation_projection=irrigation_readiness,
        )
        if irrigation_card is not None:
            cards.append(irrigation_card)

    if card_capabilities.get("varietyFit", False):
        variety_card = _build_field_climate_plan_variety_card(
            suitability_outlook=suitability_outlook,
            evidence_gaps=evidence_gaps,
        )
        if variety_card is not None:
            cards.append(variety_card)

    ordered_cards: list[dict[str, Any]] = []
    for card_type in ("frostTrend", "heatTrend", "drySpellTrend", "irrigationValue", "varietyFit"):
        for card in cards:
            if str(card.get("cardType") or "").strip() == card_type:
                ordered_cards.append(card)

    top_level_evidence_gaps = list(evidence_gaps)
    _append_unique_many(top_level_evidence_gaps, irrigation_readiness.get("requiredEvidence") or [])

    evidence_refs: list[str] = []
    trace_refs: list[str] = []
    for source in (
        adaptation_summary.get("evidenceRefs") or [],
        suitability_outlook.get("evidenceRefs") or [],
        indicator_trends.get("evidenceRefs") or [],
        irrigation_readiness.get("evidenceRefs") or [],
    ):
        _append_unique_many(evidence_refs, source)
    for source in (
        adaptation_summary.get("traceRefs") or [],
        suitability_outlook.get("traceRefs") or [],
        indicator_trends.get("traceRefs") or [],
        irrigation_readiness.get("traceRefs") or [],
    ):
        _append_unique_many(trace_refs, source)

    projection_facts_freshness = str(((indicator_trends.get("freshnessSummary") or {}).get("status")) or "unknown").strip() or "unknown"
    adaptation_signal_freshness = (
        "fresh"
        if top_signals and "field_climate_adaptation_signal" not in top_level_evidence_gaps
        else "partial"
        if top_signals or top_level_evidence_gaps
        else "unknown"
    )
    irrigation_freshness = (
        "fresh"
        if any(str(card.get("cardType") or "") == "irrigationValue" and str(card.get("displayState") or "") == "live" for card in ordered_cards)
        else "partial"
        if any(str(card.get("cardType") or "") == "irrigationValue" for card in ordered_cards)
        else "unknown"
    )
    variety_context_status = str((((suitability_outlook.get("cropOrVarietyContext") or {}).get("contextStatus")) or "unknown")).strip() or "unknown"

    if not ordered_cards:
        screen_state = "insufficientData"
    elif any(str(card.get("displayState") or "").strip() == "limited" for card in ordered_cards) or top_level_evidence_gaps:
        screen_state = "limited"
    else:
        screen_state = "live"

    return {
        "screenState": screen_state,
        "planningContext": planning_context or {},
        "freshness": {
            "projectionFacts": projection_facts_freshness,
            "adaptationSignals": adaptation_signal_freshness,
            "irrigationReadiness": irrigation_freshness,
            "varietyContext": variety_context_status,
        },
        "cards": ordered_cards,
        "evidenceGaps": top_level_evidence_gaps,
        "evidenceRefs": evidence_refs,
        "traceRefs": trace_refs,
        "detailEndpoints": detail_endpoints or {},
    }


def _compare(operator: str, actual: Any, expected: Any) -> bool:
    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator == "in_set":
        return isinstance(expected, list) and actual in expected

    actual_num = _as_number(actual)
    expected_num = _as_number(expected)
    if actual_num is None or expected_num is None:
        return False
    if operator == "<":
        return actual_num < expected_num
    if operator == "<=":
        return actual_num <= expected_num
    if operator == ">":
        return actual_num > expected_num
    if operator == ">=":
        return actual_num >= expected_num
    return False


def evaluate_rules(
    *,
    rulepack: dict[str, Any],
    evaluation_type: str,
    facts: dict[str, Any],
) -> dict[str, Any]:
    selected_rules = [
        rule
        for rule in rulepack.get("rules", [])
        if isinstance(rule, dict) and evaluation_type in (rule.get("evaluationTypes") or [])
    ]
    if not selected_rules:
        return {
            "outcomeCode": "unknown",
            "reasonCodes": ["no_matching_rules"],
            "ruleResults": [
                {
                    "ruleUri": None,
                    "label": "No matching rules",
                    "category": "rulepack",
                    "severity": "hard",
                    "result": "unknown",
                    "message": f"No rules matched evaluationType={evaluation_type}",
                    "factKey": None,
                    "reasonCode": "no_matching_rules",
                }
            ],
        }

    rule_results: list[dict[str, Any]] = []
    for rule in selected_rules:
        fact_key = str(rule.get("factKey") or "").strip()
        severity = str(rule.get("severity") or "soft").strip()
        reason_code = str(rule.get("reasonCode") or "").strip() or None
        label = str(rule.get("label") or rule.get("ruleUri") or "").strip()
        category = str(rule.get("category") or "").strip() or None
        operator = str(rule.get("operator") or "").strip()
        expected_value = rule.get("value")

        has_fact, actual_value = _lookup_fact_value(facts, fact_key) if fact_key else (False, None)
        if not has_fact:
            missing_policy = str(rule.get("onMissingFact") or "warn").strip()
            if missing_policy == "unknown":
                result = "unknown"
            elif missing_policy in {"block", "fail"}:
                result = "fail"
            else:
                result = "warn"
            message = f"Missing fact '{fact_key}'"
        else:
            passes = _compare(operator, actual_value, expected_value)
            if passes:
                result = "pass"
                message = f"Fact '{fact_key}' satisfied rule."
            elif severity == "hard":
                result = "fail"
                message = f"Fact '{fact_key}' value '{actual_value}' failed hard rule."
            else:
                result = "warn"
                message = f"Fact '{fact_key}' value '{actual_value}' triggered warning."

        rule_results.append(
            {
                "ruleUri": rule.get("ruleUri"),
                "label": label,
                "category": category,
                "severity": severity,
                "result": result,
                "message": message,
                "factKey": fact_key or None,
                "reasonCode": reason_code,
            }
        )

    if any(item["result"] == "fail" and item["severity"] == "hard" for item in rule_results):
        outcome_code = "block"
    elif any(item["result"] == "unknown" for item in rule_results):
        outcome_code = "unknown"
    elif any(item["result"] in {"warn", "fail"} for item in rule_results):
        outcome_code = "warn"
    else:
        outcome_code = "allow"

    seen_reasons: set[str] = set()
    ordered_reasons: list[str] = []
    for item in rule_results:
        if item["result"] == "pass":
            continue
        reason_code = str(item.get("reasonCode") or "").strip()
        if not reason_code or reason_code in seen_reasons:
            continue
        seen_reasons.add(reason_code)
        ordered_reasons.append(reason_code)

    return {
        "outcomeCode": outcome_code,
        "reasonCodes": ordered_reasons,
        "ruleResults": rule_results,
    }


def normalize_candidate_authorization_evaluation(
    evaluation_result: dict[str, Any],
    *,
    candidate_authorization: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    decision_code = str((candidate_authorization or {}).get("decisionCode") or "").strip()
    normalized = dict(evaluation_result)
    normalized_rule_results: list[dict[str, Any]] = []
    for item in evaluation_result.get("ruleResults") or []:
        current = dict(item)
        reason_code = str(current.get("reasonCode") or "").strip()
        if reason_code == "input_authorization_conditional" and decision_code != "conditional":
            current["reasonCode"] = None
        elif reason_code == "input_authorization_missing_or_rejected" and decision_code == "conditional":
            current["reasonCode"] = None
        normalized_rule_results.append(current)

    seen_reasons: set[str] = set()
    normalized_reasons: list[str] = []
    for item in normalized_rule_results:
        if str(item.get("result") or "").strip() == "pass":
            continue
        reason_code = str(item.get("reasonCode") or "").strip()
        if not reason_code or reason_code in seen_reasons:
            continue
        seen_reasons.add(reason_code)
        normalized_reasons.append(reason_code)

    normalized["ruleResults"] = normalized_rule_results
    normalized["reasonCodes"] = normalized_reasons
    return normalized


def build_action_evaluation_record(
    *,
    field_uri: str,
    crop_instance_uri: Optional[str],
    as_of_date: date,
    action_code: str,
    rulepack: dict[str, Any],
    evaluation_result: dict[str, Any],
    decision_context: dict[str, Any],
    candidate_label: Optional[str] = None,
    material_lot_uri: Optional[str] = None,
    input_authorization_uri: Optional[str] = None,
) -> dict[str, Any]:
    evaluation_uri = f"urn:field-action-evaluation:{uuid4()}"
    trace_uri = f"urn:rule-execution-trace:field-action-evaluation:{uuid4()}"
    evaluated_at = utc_now_iso()
    return {
        "evaluationUri": evaluation_uri,
        "fieldUri": field_uri,
        "cropInstanceUri": crop_instance_uri,
        "actionCode": action_code,
        "candidateLabel": candidate_label,
        "materialLotUri": material_lot_uri,
        "inputAuthorizationUri": input_authorization_uri,
        "asOfDate": as_of_date.isoformat(),
        "evaluatedAt": evaluated_at,
        "outcomeCode": evaluation_result["outcomeCode"],
        "reasonCodes": evaluation_result.get("reasonCodes") or [],
        "ruleResults": evaluation_result.get("ruleResults") or [],
        "decisionContext": decision_context,
        "rulePackUri": rulepack.get("rulePackUri"),
        "rulePackCode": rulepack.get("code"),
        "ruleExecutionTraceUri": trace_uri,
        "notes": None,
        "evidenceUris": decision_context.get("evidenceUris") or [],
    }


def summarize_recent_events(action_evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for item in action_evaluations:
        if not item.get("eventUri"):
            continue
        summaries.append(
            {
                "eventUri": item.get("eventUri"),
                "eventType": item.get("eventType"),
                "eventAt": item.get("eventAt"),
                "relatedEntityUri": item.get("evaluationUri") or item.get("uri"),
            }
        )
    return summaries
