from __future__ import annotations

import copy
import json
import re
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Sequence


PROFILE_ID = "si-eu-organic-small-crop-farmers.v1"
AUTO_SELECT_MIN = 0.88
COMPETITIVE_DELTA_MIN = 0.15
MANUAL_ROUTE_MIN = 0.65
TOP_CANDIDATE_COUNT = 3

_PATH_SEGMENT_RE = re.compile(r"([^\.\[\]]+)|\[(\d+)\]")
_FERTILIZER_TEXT_RE = re.compile(r"\b(?:fertili[sz]er|gnojivo|amendment|urea|npk)\b", re.IGNORECASE)
_FERTILIZER_NPK_GRADE_RE = re.compile(
    r"\bNPK\b\s*([0-9]+(?:[.,][0-9]+)?)\s*[-/]\s*([0-9]+(?:[.,][0-9]+)?)\s*[-/]\s*([0-9]+(?:[.,][0-9]+)?)\b",
    re.IGNORECASE,
)
_FERTILIZATION_PLAN_TEXT_RE = re.compile(
    r"\b(?:fertili[sz]ation\s+plan|gnojidbeni\s+plan|gnojilni\s+plan|plan\s+gnojenja|nutrient\s+plan)\b",
    re.IGNORECASE,
)
_SEED_AUTH_TEXT_RE = re.compile(
    r"\b(?:seed|variet(?:y|ies)|planting[-\s]?stock|seedling)\b.*\b(?:authori[sz]ation|authori[sz]ed|derogation|approval|exception|unavailable|not\s+available)\b"
    r"|\b(?:authori[sz]ation|authori[sz]ed|derogation|approval|exception)\b.*\b(?:seed|variet(?:y|ies)|planting[-\s]?stock|seedling)\b",
    re.IGNORECASE,
)
_SEED_AUTH_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
_DELIVERY_NOTE_TEXT_RE = re.compile(
    r"\b(?:delivery\s+note|dispatch(?:\s+note)?|weigh(?:bridge)?\s+ticket|scale\s+ticket|otpremnica|odp(?:remnica|remni\s+list)|dobavnica)\b",
    re.IGNORECASE,
)
_STORAGE_LOT_LABEL_TEXT_RE = re.compile(
    r"\b(?:storage(?:\s+lot)?|warehouse|bin|pallet(?:\s+tag)?|lot\s+(?:label|sticker))\b",
    re.IGNORECASE,
)
_DELIVERY_TICKET_REF_RE = re.compile(
    r"\b(?:delivery\s+note|dispatch(?:\s+note)?|ticket|reference|ref)\s*(?:no\.?|number|#|ref)?\s*[:\-]?\s*([A-Za-z0-9][A-Za-z0-9._/-]{2,})\b",
    re.IGNORECASE,
)
_DELIVERY_WEIGHT_RE = re.compile(
    r"\b(net|gross|tare)\b[^0-9]{0,12}([0-9]+(?:[.,][0-9]+)?)\s*(kg|kgs|t|ton|tons|lb|lbs|bu)\b",
    re.IGNORECASE,
)
_DELIVERY_MOISTURE_RE = re.compile(
    r"\b(?:moisture|vlaga)\b[^0-9]{0,12}([0-9]+(?:[.,][0-9]+)?)\s*%",
    re.IGNORECASE,
)
_DELIVERY_DATETIME_RE = re.compile(
    r"\b(\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?)?)\b"
)
_PLAN_TARGET_YIELD_RE = re.compile(
    r"\b(?:target\s+yield|yield|ciljni\s+prinos|prinos)\b[^0-9]{0,20}([0-9]+(?:[.,][0-9]+)?)\s*(t\s*/\s*ha|kg\s*/\s*ha)\b",
    re.IGNORECASE,
)
_PLAN_TARGET_NUTRIENT_RE = re.compile(
    r"\b(N|P2O5|K2O)\b\s*[:=-]?\s*([0-9]+(?:[.,][0-9]+)?)\s*(kg\s*/\s*ha)\b",
    re.IGNORECASE,
)
_SEED_TREATMENT_SUBSTANCE_SPLIT_RE = re.compile(r"\s*(?:,|;|/|\+|&|\band\b|\bin\b|\bter\b)\s*", re.IGNORECASE)


def _discover_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "specs").exists() and (candidate / "specs/api/v1").exists():
            return candidate
    raise RuntimeError("Could not discover repository root containing /specs")


ROOT = _discover_repo_root()
REGISTRY_PATH = ROOT / "specs/api/v1/server/fastapi/app/universal_capture_route_registry.json"


@lru_cache(maxsize=1)
def load_route_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def resolve_route_alias(route_id: str | None) -> str | None:
    normalized = str(route_id or "").strip()
    if not normalized:
        return None
    registry = load_route_registry()
    return str((registry.get("routeAliases") or {}).get(normalized, normalized))


def available_route_items(
    capability_enabled: Callable[[str], bool],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for raw in list(load_route_registry().get("routes") or []):
        item = dict(raw)
        required = [str(value) for value in item.get("requiredCapabilities") or [] if str(value).strip()]
        base = str(item.get("runtimeBaseAvailability") or "catalog_only")
        if base != "catalog_only" and required and any(not capability_enabled(feature) for feature in required):
            availability = "shadow"
        else:
            availability = base
        item["availability"] = availability
        items.append(item)
    return items


def route_lookup(
    capability_enabled: Callable[[str], bool],
) -> dict[str, dict[str, Any]]:
    return {str(item["routeId"]): item for item in available_route_items(capability_enabled)}


def available_helpers() -> list[dict[str, Any]]:
    return [dict(item) for item in list(load_route_registry().get("helpers") or [])]


def parse_path_tokens(path: str) -> list[str | int]:
    tokens: list[str | int] = []
    for match in _PATH_SEGMENT_RE.finditer(str(path or "")):
        key, index = match.groups()
        if key is not None:
            tokens.append(key)
        elif index is not None:
            tokens.append(int(index))
    return tokens


def set_path_value(payload: Any, path: str, value: Any) -> None:
    tokens = parse_path_tokens(path)
    if not tokens:
        return
    current = payload
    for index, token in enumerate(tokens[:-1]):
        if isinstance(token, int):
            if not isinstance(current, list):
                return
            while len(current) <= token:
                current.append({})
            current = current[token]
        else:
            if not isinstance(current, dict):
                return
            next_token = tokens[index + 1]
            if token not in current or current[token] is None:
                current[token] = [] if isinstance(next_token, int) else {}
            current = current[token]
    last = tokens[-1]
    if isinstance(last, int):
        if not isinstance(current, list):
            return
        while len(current) <= last:
            current.append(None)
        current[last] = value
    else:
        if isinstance(current, dict):
            current[last] = value


def delete_path_value(payload: Any, path: str) -> None:
    tokens = parse_path_tokens(path)
    if not tokens:
        return
    current = payload
    for token in tokens[:-1]:
        if isinstance(token, int):
            if not isinstance(current, list) or len(current) <= token:
                return
            current = current[token]
        else:
            if not isinstance(current, dict) or token not in current:
                return
            current = current[token]
    last = tokens[-1]
    if isinstance(last, int):
        if isinstance(current, list) and len(current) > last:
            current[last] = None
    elif isinstance(current, dict):
        current.pop(last, None)


def apply_field_edits(payload: dict[str, Any], field_edits: Sequence[dict[str, Any]]) -> dict[str, Any]:
    patched = copy.deepcopy(payload)
    for edit in field_edits:
        path = str(edit.get("path") or "").strip()
        if not path:
            continue
        action = str(edit.get("action") or "edited").strip().lower()
        if action == "rejected":
            delete_path_value(patched, path)
            continue
        set_path_value(patched, path, edit.get("value"))
    return patched


def apply_field_edits_to_proposals(
    proposals: Sequence[dict[str, Any]],
    field_edits: Sequence[dict[str, Any]],
    *,
    capture_id: str | None = None,
) -> list[dict[str, Any]]:
    updated = [dict(item) for item in proposals]
    by_path = {str(item.get("path") or ""): item for item in updated}
    for edit in field_edits:
        path = str(edit.get("path") or "").strip()
        if not path:
            continue
        action = str(edit.get("action") or "edited").strip().lower()
        current = by_path.get(path)
        if current is None:
            current = {
                "path": path,
                "value": edit.get("value"),
                "confidence": 1.0,
                "authorityTier": "human_edit",
                "sourceCaptureIds": [capture_id] if capture_id else [],
                "resolution": {"status": "normalized_text", "refType": None, "refUri": None},
                "reviewState": "edited" if action != "rejected" else "rejected",
            }
            updated.append(current)
            by_path[path] = current
            continue
        if action == "rejected":
            current["reviewState"] = "rejected"
            continue
        current["value"] = edit.get("value")
        current["authorityTier"] = "human_edit"
        current["confidence"] = 1.0
        current["reviewState"] = "accepted" if action == "accepted" else "edited"
    return updated


def _tail_token(value: str | None) -> str:
    raw = str(value or "").strip()
    if not raw:
        return "capture"
    if "/" in raw:
        return raw.rsplit("/", 1)[-1]
    if ":" in raw:
        return raw.rsplit(":", 1)[-1]
    return raw


def _capture_document_hint(capture: dict[str, Any]) -> str | None:
    hints = capture.get("hints") or {}
    hint = str(hints.get("documentHint") or "").strip().lower()
    if hint:
        return hint
    derived = capture.get("derivedRefs") or {}
    return str(derived.get("documentHint") or "").strip().lower() or None


def _capture_route_hint(capture: dict[str, Any]) -> str | None:
    hints = capture.get("hints") or {}
    return resolve_route_alias(str(hints.get("routeHint") or "").strip())


def _capture_barcode_values(capture: dict[str, Any]) -> list[str]:
    derived = capture.get("derivedRefs") or {}
    return [str(item) for item in derived.get("barcodeValues") or [] if str(item).strip()]


def _capture_ref(capture: dict[str, Any], key: str) -> str | None:
    value = str(capture.get(key) or "").strip()
    if value:
        return value
    derived = capture.get("derivedRefs") or {}
    value = str(derived.get(key) or "").strip()
    return value or None


def _parse_response_payload(parse_run: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(parse_run, dict):
        return {}
    response_payload = parse_run.get("responsePayload") or {}
    if isinstance(response_payload, dict):
        return dict(response_payload)
    return {}


def _text_has_fertilizer_tokens(*values: Any) -> bool:
    for value in values:
        text = str(value or "").strip()
        if text and _FERTILIZER_TEXT_RE.search(text):
            return True
    return False


def _fertilizer_item_text(item: dict[str, Any]) -> str:
    proposals = item.get("proposals") or {}
    return " ".join(
        value
        for value in (
            _proposal_value_text(proposals.get("productLabel")),
            str(item.get("rawText") or "").strip(),
        )
        if value
    )


def _is_fertilizer_candidate_item(item: dict[str, Any]) -> bool:
    category_hint = str(item.get("categoryHint") or "").strip().lower()
    return category_hint == "amendment" or _text_has_fertilizer_tokens(_fertilizer_item_text(item))


def _primary_fertilizer_item(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    items = parse_payload.get("items") or []
    amendment_item: dict[str, Any] | None = None
    token_item: dict[str, Any] | None = None
    for raw_item in items:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        category_hint = str(item.get("categoryHint") or "").strip().lower()
        if amendment_item is None and category_hint == "amendment":
            amendment_item = item
            continue
        if token_item is None and _text_has_fertilizer_tokens(_fertilizer_item_text(item)):
            token_item = item
    return amendment_item or token_item


def _parse_decimal_number(value: Any) -> float | None:
    text = str(value or "").strip()
    if not text:
        return None
    normalized = text.replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def _nutrient_match_value(match: re.Match[str] | None) -> float | None:
    if match is None:
        return None
    return _parse_decimal_number(match.group(1))


def _infer_fertilizer_declared_nutrients(
    source_text: str,
    *,
    proposal: dict[str, Any] | None,
) -> tuple[list[dict[str, Any]], list[tuple[str, float, str, dict[str, Any] | None]]]:
    nutrients_by_code: dict[str, dict[str, Any]] = {}
    inferred_fields: list[tuple[str, float, str, dict[str, Any] | None]] = []
    base_proposal = dict(proposal or {})
    if source_text and "confidence" not in base_proposal:
        base_proposal["confidence"] = 0.86
    if source_text and "valueText" not in base_proposal:
        base_proposal["valueText"] = source_text

    grade_match = _FERTILIZER_NPK_GRADE_RE.search(source_text)
    if grade_match:
        for nutrient_code, raw_value in zip(("N", "P2O5", "K2O"), grade_match.groups()):
            value = _parse_decimal_number(raw_value)
            if value is None:
                continue
            nutrients_by_code[nutrient_code] = {
                "nutrientCode": nutrient_code,
                "value": value,
                "unit": "%",
            }

    for nutrient_code in ("N", "P2O5", "K2O"):
        if nutrient_code in nutrients_by_code:
            inferred_fields.append(
                (
                    nutrients_by_code[nutrient_code]["nutrientCode"],
                    nutrients_by_code[nutrient_code]["value"],
                    nutrients_by_code[nutrient_code]["unit"],
                    base_proposal or None,
                )
            )
            continue
        escaped_code = re.escape(nutrient_code)
        patterns = (
            re.compile(rf"\b{escaped_code}\b\s*[:=-]?\s*([0-9]+(?:[.,][0-9]+)?)\s*%", re.IGNORECASE),
            re.compile(rf"([0-9]+(?:[.,][0-9]+)?)\s*%\s*{escaped_code}\b", re.IGNORECASE),
        )
        value = None
        for pattern in patterns:
            value = _nutrient_match_value(pattern.search(source_text))
            if value is not None:
                break
        if value is None:
            continue
        nutrients_by_code[nutrient_code] = {"nutrientCode": nutrient_code, "value": value, "unit": "%"}
        inferred_fields.append((nutrient_code, value, "%", base_proposal or None))

    if not grade_match:
        inferred_fields = [
            (item["nutrientCode"], item["value"], item["unit"], base_proposal or None)
            for item in [nutrients_by_code.get(code) for code in ("N", "P2O5", "K2O")]
            if item
        ]
    return [nutrients_by_code[code] for code in ("N", "P2O5", "K2O") if code in nutrients_by_code], inferred_fields


def _fertilizer_label_payload(parse_payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("fertiliserProductComposition", "fertilizerProductComposition"):
        value = parse_payload.get(key)
        if isinstance(value, dict):
            return dict(value)
    return {}


def _fertilizer_declared_nutrient_entries(
    parse_payload: dict[str, Any],
) -> list[tuple[str, float, str, dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]]:
    payload = _fertilizer_label_payload(parse_payload)
    raw_entries = payload.get("declaredNutrients")
    if not isinstance(raw_entries, list):
        return []

    normalized_entries: list[tuple[str, float, str, dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]] = []
    for row in raw_entries:
        if not isinstance(row, dict):
            continue
        nutrient_code_proposal = _proposal_like(row.get("nutrientCode"))
        value_proposal = _proposal_like(row.get("valueNum"), preferred="number") or _proposal_like(
            row.get("valueText"), preferred="number_or_text"
        )
        unit_proposal = _proposal_like(row.get("unit"))
        nutrient_code = _proposal_value_text(nutrient_code_proposal)
        nutrient_value = _proposal_value_num(value_proposal)
        if nutrient_value is None:
            nutrient_value = _parse_decimal_number(_proposal_value_text(value_proposal))
        nutrient_unit = _proposal_value_text(unit_proposal)
        if not nutrient_code or nutrient_value is None or not nutrient_unit:
            continue
        normalized_entries.append(
            (
                nutrient_code,
                nutrient_value,
                nutrient_unit,
                nutrient_code_proposal,
                value_proposal,
                unit_proposal,
            )
        )
    return normalized_entries


def _fertilizer_density_entry(
    parse_payload: dict[str, Any],
) -> tuple[float | None, str | None, dict[str, Any] | None, dict[str, Any] | None]:
    payload = _fertilizer_label_payload(parse_payload)
    value_proposal = _proposal_like(payload.get("densityValue"), preferred="number")
    unit_proposal = _proposal_like(payload.get("densityUnit"))
    density_value = _proposal_value_num(value_proposal)
    if density_value is None:
        density_value = _parse_decimal_number(_proposal_value_text(value_proposal))
    density_unit = _proposal_value_text(unit_proposal)
    return density_value, density_unit, value_proposal, unit_proposal


def _fertilizer_marker_entries(
    parse_payload: dict[str, Any],
) -> list[tuple[str, dict[str, Any] | None]]:
    payload = _fertilizer_label_payload(parse_payload)
    raw_entries = payload.get("ceOrCategoryMarkers")
    if not isinstance(raw_entries, list):
        return []

    normalized_entries: list[tuple[str, dict[str, Any] | None]] = []
    seen_markers: set[str] = set()
    for row in raw_entries:
        proposal = _proposal_like(row)
        marker = _proposal_value_text(proposal)
        if not marker or marker in seen_markers:
            continue
        seen_markers.add(marker)
        normalized_entries.append((marker, proposal))
    return normalized_entries


def _fertilizer_text_field_entry(
    parse_payload: dict[str, Any],
    key: str,
) -> tuple[str | None, dict[str, Any] | None]:
    payload = _fertilizer_label_payload(parse_payload)
    proposal = _proposal_like(payload.get(key))
    return _proposal_value_text(proposal), proposal


def _fertilization_plan_payload(parse_payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("fertilisationPlan", "fertilizationPlan"):
        value = parse_payload.get(key)
        if isinstance(value, dict):
            return dict(value)
    return {}


def _normalize_plan_unit(value: str | None) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    compact = re.sub(r"\s+", "", text).lower()
    normalized = {
        "kg/ha": "kg/ha",
        "kgha": "kg/ha",
        "kg/ha-1": "kg/ha",
        "t/ha": "t/ha",
        "tha": "t/ha",
        "t/ha-1": "t/ha",
    }.get(compact)
    return normalized or text


def _fertilization_plan_source_text(parse_payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for container in (_fertilization_plan_payload(parse_payload), parse_payload):
        if not isinstance(container, dict):
            continue
        for key in ("title", "documentTitle", "summary", "rawText", "planTitle", "ruleProfile"):
            raw_value = container.get(key)
            if isinstance(raw_value, dict):
                value = _proposal_value_text(raw_value)
            else:
                value = str(raw_value or "").strip()
            if value:
                texts.append(value)
    receipt = parse_payload.get("receipt") or {}
    if isinstance(receipt, dict):
        for key in ("vendorName", "receiptRef", "purchaseDate"):
            value = _proposal_value_text(receipt.get(key))
            if value:
                texts.append(value)
    items = parse_payload.get("items") or []
    if isinstance(items, list):
        for raw_item in items:
            if not isinstance(raw_item, dict):
                continue
            item = dict(raw_item)
            texts.extend(
                value
                for value in (
                    str(item.get("rawText") or "").strip(),
                    _proposal_value_text((item.get("proposals") or {}).get("productLabel")),
                )
                if value
            )
    return " ".join(texts)


def _fertilization_plan_has_text_cues(parse_payload: dict[str, Any]) -> bool:
    return bool(_FERTILIZATION_PLAN_TEXT_RE.search(_fertilization_plan_source_text(parse_payload)))


def _seed_authorization_typed_payload(parse_payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("seedSourcingException", "seedException"):
        value = parse_payload.get(key)
        if isinstance(value, dict):
            return dict(value)
    return {}


def _seed_authorization_containers(parse_payload: dict[str, Any]) -> list[dict[str, Any]]:
    containers: list[dict[str, Any]] = []
    typed_payload = _seed_authorization_typed_payload(parse_payload)
    if typed_payload:
        containers.append(typed_payload)
    for key in ("authorization", "permit", "certificate"):
        value = parse_payload.get(key)
        if isinstance(value, dict):
            containers.append(dict(value))
    containers.append(parse_payload)
    return containers


def _seed_authorization_field_proposal(
    parse_payload: dict[str, Any],
    *keys: str,
    preferred: str = "text",
) -> dict[str, Any] | None:
    for container in _seed_authorization_containers(parse_payload):
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key not in container or container.get(key) is None:
                continue
            proposal = _proposal_like(container.get(key), preferred=preferred)
            if proposal is not None:
                return proposal
    items = parse_payload.get("items") or []
    if not isinstance(items, list):
        return None
    for raw_item in items:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        proposals = item.get("proposals") or {}
        for key in keys:
            proposal = (
                _proposal_from_row(item, key, preferred=preferred)
                or _proposal_like(proposals.get(key), preferred=preferred)
            )
            if proposal is not None:
                return proposal
    return None


def _seed_authorization_source_text(parse_payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for container in _seed_authorization_containers(parse_payload):
        if not isinstance(container, dict):
            continue
        for key in (
            "title",
            "documentTitle",
            "summary",
            "rawText",
            "ocrText",
            "asOfDate",
            "decisionStatusCode",
            "reasonCode",
            "reasonText",
            "availabilityEvidenceText",
            "cropLabel",
            "varietyLabel",
            "variety",
        ):
            value = str(container.get(key) or "").strip()
            if value:
                texts.append(value)
    items = parse_payload.get("items") or []
    if isinstance(items, list):
        for raw_item in items:
            if not isinstance(raw_item, dict):
                continue
            item = dict(raw_item)
            texts.extend(
                value
                for value in (
                    str(item.get("rawText") or "").strip(),
                    _proposal_value_text((item.get("proposals") or {}).get("variety")),
                    _proposal_value_text((item.get("proposals") or {}).get("cropLabel")),
                )
                if value
            )
    return " ".join(texts)


def _seed_authorization_has_text_cues(parse_payload: dict[str, Any]) -> bool:
    return bool(_SEED_AUTH_TEXT_RE.search(_seed_authorization_source_text(parse_payload)))


def _seed_authorization_date_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    proposal = _seed_authorization_field_proposal(
        parse_payload,
        "asOfDate",
        "issuedOn",
        "issuedAt",
        "decisionDate",
        "effectiveDate",
        preferred="date",
    )
    if proposal is not None:
        value = _proposal_value_text(proposal)
        parsed = _parse_iso_date_value(value)
        if parsed is not None:
            normalized = dict(proposal)
            normalized["valueDate"] = parsed.isoformat()
            normalized.pop("valueText", None)
            return normalized
    match = _SEED_AUTH_DATE_RE.search(_seed_authorization_source_text(parse_payload))
    if match:
        return {"valueDate": match.group(1), "confidence": 0.78}
    return None


def _seed_authorization_decision_code_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    explicit = _seed_authorization_field_proposal(
        parse_payload,
        "decisionStatusCode",
        "exceptionDecisionStatusCode",
        "decisionCode",
        "statusCode",
        "status",
    )
    explicit_value = str(_proposal_value_text(explicit) or "").strip().lower()
    if explicit_value in {"authorized", "conditional", "rejected", "unknown"}:
        normalized = dict(explicit or {})
        normalized["valueText"] = explicit_value
        return normalized

    source_text = _seed_authorization_source_text(parse_payload)
    if re.search(r"\b(?:rejected|denied|refused|not\s+authori[sz]ed|not\s+approved)\b", source_text, re.IGNORECASE):
        return {"valueText": "rejected", "confidence": 0.82}
    if re.search(r"\b(?:conditional|subject\s+to|under\s+condition(?:s)?)\b", source_text, re.IGNORECASE):
        return {"valueText": "conditional", "confidence": 0.8}
    if re.search(r"\b(?:authori[sz]ed|approved|granted|permission\s+granted)\b", source_text, re.IGNORECASE):
        return {"valueText": "authorized", "confidence": 0.82}
    return None


def _seed_authorization_reason_code_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    explicit = _seed_authorization_field_proposal(
        parse_payload,
        "reasonCode",
        "exceptionReasonCode",
        "reason",
    )
    explicit_value = str(_proposal_value_text(explicit) or "").strip().lower()
    if explicit_value in {
        "organic_seed_unavailable",
        "organic_variety_unavailable",
        "organic_planting_stock_unavailable",
        "supplier_evidence_pending",
        "other",
    }:
        normalized = dict(explicit or {})
        normalized["valueText"] = explicit_value
        return normalized

    source_text = _seed_authorization_source_text(parse_payload)
    reason_patterns = (
        (
            "organic_variety_unavailable",
            r"\borganic\b.{0,40}\bvariet(?:y|ies)\b.{0,40}\b(?:unavailable|not\s+available)\b",
        ),
        (
            "organic_seed_unavailable",
            r"\borganic\b.{0,40}\bseed\b.{0,40}\b(?:unavailable|not\s+available)\b",
        ),
        (
            "organic_planting_stock_unavailable",
            r"\borganic\b.{0,40}\bplanting[-\s]?stock\b.{0,40}\b(?:unavailable|not\s+available)\b",
        ),
        (
            "supplier_evidence_pending",
            r"\b(?:supplier\s+(?:evidence|statement)\s+pending|pending\s+supplier\s+(?:evidence|statement))\b",
        ),
    )
    for code, pattern in reason_patterns:
        if re.search(pattern, source_text, re.IGNORECASE):
            return {"valueText": code, "confidence": 0.8}
    return None


def _seed_authorization_attachment_role(
    capture: dict[str, Any],
    parse_payload: dict[str, Any],
) -> str:
    if _capture_document_hint(capture) == "certificate":
        return "certificate"
    if str(parse_payload.get("documentType") or "").strip().lower() == "certificate":
        return "certificate"
    return "other"


def _delivery_note_field_proposal(
    parse_payload: dict[str, Any],
    *keys: str,
    preferred: str = "text",
) -> dict[str, Any] | None:
    containers = [parse_payload.get("deliveryNote") or {}, parse_payload, parse_payload.get("receipt") or {}]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key not in container or container.get(key) is None:
                continue
            proposal = _proposal_like(container.get(key), preferred=preferred)
            if proposal is not None:
                return proposal
    items = parse_payload.get("items") or []
    if not isinstance(items, list):
        return None
    for raw_item in items:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        proposals = item.get("proposals") or {}
        for key in keys:
            proposal = (
                _proposal_from_row(item, key, preferred=preferred)
                or _proposal_like(proposals.get(key), preferred=preferred)
            )
            if proposal is not None:
                return proposal
    return None


def _delivery_note_source_text(parse_payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for key in ("title", "documentTitle", "summary", "rawText", "ocrText", "ticketRef"):
        value = str(parse_payload.get(key) or "").strip()
        if value:
            texts.append(value)
    delivery_note = parse_payload.get("deliveryNote") or {}
    if isinstance(delivery_note, dict):
        for key in (
            "deliveredAt",
            "buyerLabel",
            "buyerRegistrationId",
            "buyerVatId",
            "buyerAddress",
            "ticketRef",
            "lotCode",
            "weightUnit",
        ):
            value = _proposal_value_text(_proposal_like(delivery_note.get(key), preferred="text"))
            if value:
                texts.append(value)
    receipt = parse_payload.get("receipt") or {}
    if isinstance(receipt, dict):
        for key in ("vendorName", "receiptRef", "purchaseDate"):
            value = _proposal_value_text(receipt.get(key))
            if value:
                texts.append(value)
    items = parse_payload.get("items") or []
    if isinstance(items, list):
        for raw_item in items:
            if not isinstance(raw_item, dict):
                continue
            item = dict(raw_item)
            texts.extend(
                value
                for value in (
                    str(item.get("rawText") or "").strip(),
                    _proposal_value_text((item.get("proposals") or {}).get("productLabel")),
                )
                if value
            )
    return " ".join(texts)


def _delivery_note_has_text_cues(parse_payload: dict[str, Any]) -> bool:
    return bool(_DELIVERY_NOTE_TEXT_RE.search(_delivery_note_source_text(parse_payload)))


def _normalize_delivery_weight_unit(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    compact = re.sub(r"\s+", "", text).lower()
    return {
        "kg": "kg",
        "kgs": "kg",
        "t": "t",
        "ton": "t",
        "tons": "t",
        "lb": "lb",
        "lbs": "lb",
        "bu": "bu",
    }.get(compact)


def _delivery_note_delivered_at_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    for key in ("deliveredAt", "deliveryDate", "purchaseDate"):
        proposal = _delivery_note_field_proposal(parse_payload, key, preferred="text")
        text = _proposal_value_text(proposal)
        if text and _DELIVERY_DATETIME_RE.search(text):
            return proposal
    match = _DELIVERY_DATETIME_RE.search(_delivery_note_source_text(parse_payload))
    if match:
        return {"valueText": match.group(1), "confidence": 0.82}
    return None


def _delivery_note_ticket_ref_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    proposal = _delivery_note_field_proposal(
        parse_payload,
        "ticketRef",
        "deliveryNoteRef",
        "dispatchRef",
        "receiptRef",
        preferred="text",
    )
    if _proposal_value_text(proposal):
        return proposal
    match = _DELIVERY_TICKET_REF_RE.search(_delivery_note_source_text(parse_payload))
    if match:
        return {"valueText": match.group(1), "confidence": 0.82}
    return None


def _delivery_note_lot_code_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    return _delivery_note_field_proposal(parse_payload, "lotCode", preferred="text")


def _delivery_note_measurements(
    parse_payload: dict[str, Any],
) -> dict[str, tuple[float, str | None, dict[str, Any] | None]]:
    measurements: dict[str, tuple[float, str | None, dict[str, Any] | None]] = {}
    explicit_weight_unit_proposal = _delivery_note_field_proposal(
        parse_payload,
        "weightUnit",
        "netWeightUnit",
        preferred="text",
    )
    explicit_weight_unit = _normalize_delivery_weight_unit(_proposal_value_text(explicit_weight_unit_proposal))

    for key in ("netWeight", "grossWeight", "tareWeight"):
        proposal = _delivery_note_field_proposal(parse_payload, key, preferred="number_or_text")
        value = _proposal_value_num(proposal)
        if value is None:
            value = _parse_decimal_number(_proposal_value_text(proposal))
        if value is None:
            continue
        measurements[key] = (value, explicit_weight_unit, proposal)

    for match in _DELIVERY_WEIGHT_RE.finditer(_delivery_note_source_text(parse_payload)):
        field_name = {
            "net": "netWeight",
            "gross": "grossWeight",
            "tare": "tareWeight",
        }.get(str(match.group(1) or "").strip().lower())
        if not field_name or field_name in measurements:
            continue
        value = _parse_decimal_number(match.group(2))
        unit = _normalize_delivery_weight_unit(match.group(3))
        if value is None:
            continue
        measurements[field_name] = (value, unit, {"valueText": match.group(0), "confidence": 0.84})
    return measurements


def _delivery_note_moisture_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    proposal = _delivery_note_field_proposal(parse_payload, "moisturePct", "moisture", preferred="number_or_text")
    value = _proposal_value_num(proposal)
    if value is not None:
        return proposal
    match = _DELIVERY_MOISTURE_RE.search(_delivery_note_source_text(parse_payload))
    if match:
        value = _parse_decimal_number(match.group(1))
        if value is not None:
            return {"valueNum": value, "confidence": 0.82}
    return None


def _fertilization_plan_field_proposal(
    parse_payload: dict[str, Any],
    *keys: str,
    preferred: str = "text",
) -> dict[str, Any] | None:
    containers = [_fertilization_plan_payload(parse_payload), parse_payload]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key not in container or container.get(key) is None:
                continue
            proposal = _proposal_like(container.get(key), preferred=preferred)
            if proposal is not None:
                return proposal
    return None


def _fertilization_plan_list_value(parse_payload: dict[str, Any], *keys: str) -> list[str]:
    containers = [_fertilization_plan_payload(parse_payload), parse_payload]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            raw = container.get(key)
            if not isinstance(raw, list):
                continue
            values = [str(item).strip() for item in raw if str(item).strip()]
            if values:
                return values
    return []


def _fertilization_plan_target_nutrient_entries(
    parse_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    normalized_entries: list[dict[str, Any]] = []
    containers = [_fertilization_plan_payload(parse_payload), parse_payload]
    for container in containers:
        if not isinstance(container, dict):
            continue
        raw_entries = container.get("targetNutrients")
        if not isinstance(raw_entries, list):
            continue
        for row in raw_entries:
            if not isinstance(row, dict):
                continue
            proposals = row.get("proposals") or {}
            nutrient_code_proposal = (
                _proposal_from_row(row, "nutrientCode")
                or _proposal_like(proposals.get("nutrientCode"))
            )
            value_proposal = (
                _proposal_from_row(row, "valueNum", preferred="number")
                or _proposal_from_row(row, "valueText", preferred="number_or_text")
                or _proposal_from_row(row, "value", preferred="number_or_text")
                or _proposal_like(proposals.get("valueNum"), preferred="number")
                or _proposal_like(proposals.get("valueText"), preferred="number_or_text")
                or _proposal_like(proposals.get("value"), preferred="number_or_text")
            )
            unit_proposal = (
                _proposal_from_row(row, "unit")
                or _proposal_like(proposals.get("unit"))
            )
            if not nutrient_code_proposal or not value_proposal or not unit_proposal:
                continue
            normalized_entries.append(
                {
                    "nutrientCodeProposal": nutrient_code_proposal,
                    "valueProposal": value_proposal,
                    "unitProposal": unit_proposal,
                }
            )
        if normalized_entries:
            return normalized_entries

    items = parse_payload.get("items") or []
    if isinstance(items, list):
        for raw_item in items:
            if not isinstance(raw_item, dict):
                continue
            item = dict(raw_item)
            proposals = item.get("proposals") or {}
            nutrient_code_proposal = (
                _proposal_from_row(item, "nutrientCode")
                or _proposal_like(proposals.get("nutrientCode"))
            )
            value_proposal = (
                _proposal_from_row(item, "valueNum", preferred="number")
                or _proposal_from_row(item, "valueText", preferred="number_or_text")
                or _proposal_from_row(item, "value", preferred="number_or_text")
                or _proposal_like(proposals.get("valueNum"), preferred="number")
                or _proposal_like(proposals.get("valueText"), preferred="number_or_text")
                or _proposal_like(proposals.get("value"), preferred="number_or_text")
            )
            unit_proposal = (
                _proposal_from_row(item, "unit")
                or _proposal_like(proposals.get("unit"))
            )
            if not nutrient_code_proposal or not value_proposal or not unit_proposal:
                continue
            normalized_entries.append(
                {
                    "nutrientCodeProposal": nutrient_code_proposal,
                    "valueProposal": value_proposal,
                    "unitProposal": unit_proposal,
                }
            )
    if normalized_entries:
        return normalized_entries

    source_text = _fertilization_plan_source_text(parse_payload)
    nutrient_codes_seen: set[str] = set()
    for match in _PLAN_TARGET_NUTRIENT_RE.finditer(source_text):
        nutrient_code = str(match.group(1) or "").strip().upper()
        if nutrient_code in nutrient_codes_seen:
            continue
        value = _parse_decimal_number(match.group(2))
        unit = _normalize_plan_unit(match.group(3))
        if value is None or not unit:
            continue
        nutrient_codes_seen.add(nutrient_code)
        normalized_entries.append(
            {
                "nutrientCodeProposal": {"valueText": nutrient_code, "confidence": 0.82},
                "valueProposal": {"valueNum": value, "confidence": 0.82},
                "unitProposal": {"valueText": unit, "confidence": 0.82},
            }
        )
    return normalized_entries


def _parse_iso_date_value(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    candidate = text[:10]
    try:
        return date.fromisoformat(candidate)
    except ValueError:
        return None


def _fertilization_plan_resolution_season_code(
    planning_window_start: Any,
    planning_window_end: Any,
) -> str | None:
    start_date = _parse_iso_date_value(planning_window_start)
    end_date = _parse_iso_date_value(planning_window_end)
    if start_date and end_date and start_date.year != end_date.year:
        return None
    resolved_date = start_date or end_date
    if resolved_date is None:
        return None
    return str(resolved_date.year)


def _fertilization_plan_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("fieldUri") or "").strip():
        blockers.append("missing_field_uri")
    if not str(payload.get("cropInstanceUri") or "").strip():
        blockers.append("missing_crop_instance_uri")
    planning_window_start = str(payload.get("planningWindowStart") or "").strip()
    planning_window_end = str(payload.get("planningWindowEnd") or "").strip()
    if not planning_window_start:
        blockers.append("missing_planning_window_start")
    if not planning_window_end:
        blockers.append("missing_planning_window_end")
    start_date = _parse_iso_date_value(planning_window_start)
    end_date = _parse_iso_date_value(planning_window_end)
    if start_date and end_date and end_date < start_date:
        blockers.append("invalid_planning_window")
    if payload.get("targetYieldValue") is None or str(payload.get("targetYieldValue")).strip() == "":
        blockers.append("missing_target_yield_value")
    if not str(payload.get("targetYieldUnit") or "").strip():
        blockers.append("missing_target_yield_unit")
    if not str(payload.get("ruleProfile") or "").strip():
        blockers.append("missing_rule_profile")
    target_nutrients = payload.get("targetNutrients") or []
    if not isinstance(target_nutrients, list) or not target_nutrients:
        blockers.append("missing_target_nutrients")
    else:
        incomplete = False
        for item in target_nutrients:
            if not isinstance(item, dict):
                incomplete = True
                break
            if not str(item.get("nutrientCode") or "").strip():
                incomplete = True
                break
            if item.get("value") is None or str(item.get("value")).strip() == "":
                incomplete = True
                break
            if not str(item.get("unit") or "").strip():
                incomplete = True
                break
        if incomplete:
            blockers.append("incomplete_target_nutrients")
    return blockers


def _seed_authorization_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("asOfDate") or "").strip():
        blockers.append("missing_as_of_date")
    if not any(
        str(payload.get(key) or "").strip()
        for key in ("fieldUri", "cropTypeUri", "varietyUri", "purchaseLineUri", "seedLotUri")
    ):
        blockers.append("missing_scope_anchor")
    if not str(payload.get("decisionStatusCode") or "").strip():
        blockers.append("missing_decision_status_code")
    if not str(payload.get("reasonCode") or "").strip():
        blockers.append("missing_reason_code")
    if str(payload.get("reasonCode") or "").strip().lower() == "other" and not str(payload.get("reasonText") or "").strip():
        blockers.append("missing_reason_text")
    attachment_evidence = payload.get("attachmentEvidence") or []
    if not isinstance(attachment_evidence, list) or not attachment_evidence:
        blockers.append("missing_attachment_evidence")
    else:
        incomplete_attachment = False
        for item in attachment_evidence:
            if not isinstance(item, dict):
                incomplete_attachment = True
                break
            if not str(item.get("roleCode") or "").strip():
                incomplete_attachment = True
                break
            if not str(item.get("evidenceUri") or item.get("evidenceRef") or "").strip():
                incomplete_attachment = True
                break
        if incomplete_attachment:
            blockers.append("incomplete_attachment_evidence")
    return blockers


def _score_receipt_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    persistence_targets = [str(item) for item in parse_payload.get("persistenceTargets") or []]
    has_receipt_context = bool(parse_payload.get("receipt")) or "inventory_receipt_import" in persistence_targets
    if document_type == "receipt":
        score += 0.72
        reasons.append("document_type:receipt")
    elif document_type == "mixed" and has_receipt_context:
        # OCR can classify invoice-like receipts as "mixed" while still emitting receipt headers/import targets.
        score += 0.62
        reasons.append("document_type:mixed_receipt_context")
    if "inventory_receipt_import" in persistence_targets:
        score += 0.18
        reasons.append("persistence_target:inventory_receipt_import")
    if _capture_document_hint(capture) == "receipt":
        score += 0.08
        reasons.append("document_hint:receipt")
    if parse_payload.get("receipt"):
        score += 0.04
        reasons.append("receipt_header_present")
    if parse_payload.get("items"):
        score += 0.03
        reasons.append("line_items_present")
    if (
        _capture_document_hint(capture) != "receipt"
        and "inventory_receipt_import" not in persistence_targets
        and _fertilization_plan_has_text_cues(parse_payload)
    ):
        score = max(0.0, score - 0.18)
        reasons.append("penalty:plan_like_text")
    if (
        _capture_document_hint(capture) != "receipt"
        and "inventory_receipt_import" not in persistence_targets
        and _delivery_note_has_text_cues(parse_payload)
    ):
        score = max(0.0, score - 0.22)
        reasons.append("penalty:delivery_note_like_text")
    return min(score, 0.99), reasons


def _score_seed_label_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _capture_document_hint(capture) == "label":
        score += 0.34
        reasons.append("document_hint:label")
    if str(parse_payload.get("documentType") or "").strip().lower() == "label":
        score += 0.26
        reasons.append("document_type:label")
    items = parse_payload.get("items") or []
    label_specific = False
    for item in items:
        proposals = (item or {}).get("proposals") or {}
        if any(key in proposals for key in ("variety", "statusCode", "lotCode", "packQuantity")):
            label_specific = True
            break
    if label_specific:
        score += 0.28
        reasons.append("seed_label_fields")
    if _capture_barcode_values(capture):
        score += 0.05
        reasons.append("barcode_present")
    return min(score, 0.92), reasons


def _seed_label_primary_item(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    first_item: dict[str, Any] | None = None
    seed_item: dict[str, Any] | None = None
    for raw_item in parse_payload.get("items") or []:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        if first_item is None:
            first_item = item
        proposals = item.get("proposals") or {}
        if seed_item is None and (
            str(item.get("categoryHint") or "").strip().lower() == "seed"
            or any(key in proposals for key in ("productLabel", "cropLabel", "variety", "statusCode", "lotCode"))
        ):
            seed_item = item
    return seed_item or first_item


def _seed_label_field_proposal(parse_payload: dict[str, Any], *keys: str) -> dict[str, Any] | None:
    primary_item = _seed_label_primary_item(parse_payload) or {}
    primary_proposals = primary_item.get("proposals") or {}
    for key in keys:
        proposal = primary_proposals.get(key)
        if isinstance(proposal, dict):
            return dict(proposal)
    for raw_item in parse_payload.get("items") or []:
        if not isinstance(raw_item, dict):
            continue
        proposals = (raw_item or {}).get("proposals") or {}
        for key in keys:
            proposal = proposals.get(key)
            if isinstance(proposal, dict):
                return dict(proposal)
    return None


def _storage_lot_label_item_text(item: dict[str, Any]) -> str:
    proposals = item.get("proposals") or {}
    return " ".join(
        value
        for value in (
            _proposal_value_text(proposals.get("productLabel")),
            str(item.get("rawText") or "").strip(),
        )
        if value
    )


def _storage_lot_label_primary_item(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    items = parse_payload.get("items") or []
    storage_cue_item: dict[str, Any] | None = None
    lot_code_item: dict[str, Any] | None = None
    first_item: dict[str, Any] | None = None
    for raw_item in items:
        if not isinstance(raw_item, dict):
            continue
        item = dict(raw_item)
        if first_item is None:
            first_item = item
        proposals = item.get("proposals") or {}
        if storage_cue_item is None and _STORAGE_LOT_LABEL_TEXT_RE.search(_storage_lot_label_item_text(item)):
            storage_cue_item = item
        if lot_code_item is None and isinstance(proposals, dict) and isinstance(proposals.get("lotCode"), dict):
            lot_code_item = item
    return storage_cue_item or lot_code_item or first_item


def _storage_lot_label_lot_code_proposal(parse_payload: dict[str, Any]) -> dict[str, Any] | None:
    primary_item = _storage_lot_label_primary_item(parse_payload) or {}
    proposals = primary_item.get("proposals") or {}
    lot_code_proposal = proposals.get("lotCode")
    if isinstance(lot_code_proposal, dict):
        return dict(lot_code_proposal)
    for raw_item in parse_payload.get("items") or []:
        proposals = (raw_item or {}).get("proposals") or {}
        lot_code_proposal = proposals.get("lotCode")
        if isinstance(lot_code_proposal, dict):
            return dict(lot_code_proposal)
    return None


def _storage_lot_label_has_text_cues(parse_payload: dict[str, Any]) -> bool:
    for raw_item in parse_payload.get("items") or []:
        if not isinstance(raw_item, dict):
            continue
        if _STORAGE_LOT_LABEL_TEXT_RE.search(_storage_lot_label_item_text(dict(raw_item))):
            return True
    return False


def _score_storage_lot_label_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    primary_item = _storage_lot_label_primary_item(parse_payload) or {}
    primary_item_proposals = primary_item.get("proposals") or {}
    lot_code_proposal = _storage_lot_label_lot_code_proposal(parse_payload)

    if _capture_document_hint(capture) == "label":
        score += 0.14
        reasons.append("document_hint:label")
    if document_type == "label":
        score += 0.16
        reasons.append("document_type:label")
    if lot_code_proposal is not None:
        score += 0.28
        reasons.append("lot_code_present")
    if _storage_lot_label_has_text_cues(parse_payload):
        score += 0.34
        reasons.append("storage_lot_label_text_present")
    if parse_payload.get("items"):
        score += 0.04
        reasons.append("structured_items_present")
    if any(key in primary_item_proposals for key in ("variety", "statusCode", "packQuantity")):
        score = max(0.0, score - 0.18)
        reasons.append("penalty:seed_label_fields")
    if _fertilizer_label_payload(parse_payload):
        score = max(0.0, score - 0.24)
        reasons.append("penalty:fertilizer_label_payload")
    return min(score, 0.91), reasons


def _score_fertilizer_label_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    primary_item = _primary_fertilizer_item(parse_payload)
    if _fertilizer_label_payload(parse_payload):
        score += 0.18
        reasons.append("fertiliser_product_composition_payload_present")
    if _capture_document_hint(capture) == "fertiliser_label":
        score += 0.62
        reasons.append("document_hint:fertiliser_label")
    if document_type == "label":
        score += 0.18
        reasons.append("document_type:label")
    elif document_type == "mixed" and primary_item is not None:
        score += 0.12
        reasons.append("document_type:mixed_fertilizer_context")
    if primary_item is not None:
        category_hint = str(primary_item.get("categoryHint") or "").strip().lower()
        if category_hint == "amendment":
            score += 0.26
            reasons.append("category_hint:amendment")
        if _text_has_fertilizer_tokens(_fertilizer_item_text(primary_item)):
            score += 0.08
            reasons.append("fertilizer_text_present")
    if parse_payload.get("items"):
        score += 0.06
        reasons.append("label_items_present")
    return min(score, 0.94), reasons


def _score_fertilization_plan_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    plan_payload = _fertilization_plan_payload(parse_payload)
    has_context_scope = bool(_capture_context_ref(capture, "fieldUri") and _capture_context_ref(capture, "cropInstanceUri"))
    if _capture_document_hint(capture) == "unknown":
        score += 0.04
        reasons.append("document_hint:unknown")
    if plan_payload:
        score += 0.42
        reasons.append("plan_payload_present")
    if _fertilization_plan_has_text_cues(parse_payload):
        score += 0.46
        reasons.append("plan_text_present")
    if document_type in {"unknown", "mixed"} and (plan_payload or _fertilization_plan_has_text_cues(parse_payload)):
        score += 0.04
        reasons.append(f"document_type:{document_type or 'unknown'}")
    if has_context_scope:
        score += 0.2
        reasons.append("context_refs:field_and_crop")
    if document_type == "receipt" and _fertilization_plan_has_text_cues(parse_payload) and has_context_scope:
        score += 0.12
        reasons.append("document_type:receipt_but_plan_context")
    if _fertilization_plan_target_nutrient_entries(parse_payload):
        score += 0.08
        reasons.append("target_nutrients_present")
    if parse_payload.get("items"):
        score += 0.04
        reasons.append("structured_items_present")
    return min(score, 0.92), reasons


def _score_seed_authorization_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    if _seed_authorization_typed_payload(parse_payload):
        score += 0.2
        reasons.append("seed_sourcing_exception_payload_present")
    if _capture_document_hint(capture) == "certificate":
        score += 0.08
        reasons.append("document_hint:certificate")
    if _seed_authorization_has_text_cues(parse_payload):
        score += 0.54
        reasons.append("seed_authorization_text_present")
    if document_type == "certificate" and _seed_authorization_has_text_cues(parse_payload):
        score += 0.14
        reasons.append("document_type:certificate")
    elif document_type in {"unknown", "mixed"} and _seed_authorization_has_text_cues(parse_payload):
        score += 0.08
        reasons.append(f"document_type:{document_type or 'unknown'}")
    if _seed_authorization_decision_code_proposal(parse_payload) is not None:
        score += 0.11
        reasons.append("decision_status_present")
    if _seed_authorization_reason_code_proposal(parse_payload) is not None:
        score += 0.09
        reasons.append("reason_code_present")
    if _capture_context_ref(capture, "fieldUri"):
        score += 0.08
        reasons.append("context_refs:field")
    if _capture_ref(capture, "documentUri"):
        score += 0.04
        reasons.append("document_uri_present")
    return min(score, 0.96), reasons


def _score_delivery_note_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    document_type = str(parse_payload.get("documentType") or "").strip().lower()
    text_cues_present = _delivery_note_has_text_cues(parse_payload)
    measurements = _delivery_note_measurements(parse_payload)
    ticket_ref = _proposal_value_text(_delivery_note_ticket_ref_proposal(parse_payload))
    delivered_at = _proposal_value_text(_delivery_note_delivered_at_proposal(parse_payload))

    if _capture_document_hint(capture) == "weigh_ticket":
        score += 0.28
        reasons.append("document_hint:weigh_ticket")
    if text_cues_present:
        score += 0.46
        reasons.append("delivery_note_text_present")
    if document_type in {"receipt", "mixed", "unknown"} and text_cues_present:
        score += 0.06
        reasons.append(f"document_type:{document_type or 'unknown'}")
    if "netWeight" in measurements:
        score += 0.18
        reasons.append("net_weight_present")
    if "grossWeight" in measurements or "tareWeight" in measurements:
        score += 0.06
        reasons.append("gross_tare_present")
    if delivered_at:
        score += 0.05
        reasons.append("delivered_at_present")
    if ticket_ref:
        score += 0.07
        reasons.append("ticket_ref_present")
    return min(score, 0.93), reasons


def _score_soil_report_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _capture_document_hint(capture) == "soil_lab_report":
        score += 0.62
        reasons.append("document_hint:soil_lab_report")
    soil_report = parse_payload.get("soilReport") or {}
    if isinstance(soil_report, dict) and soil_report:
        score += 0.18
        reasons.append("soil_report_payload")
    if isinstance(soil_report, dict) and soil_report.get("parameters"):
        score += 0.08
        reasons.append("soil_report_parameters")
    if parse_payload.get("documentUri"):
        score += 0.04
        reasons.append("document_uri_present")
    if parse_payload.get("items"):
        score += 0.04
        reasons.append("structured_items_present")
    return min(score, 0.9), reasons


def _score_certificate_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if _capture_document_hint(capture) == "certificate":
        score += 0.62
        reasons.append("document_hint:certificate")
    if str(parse_payload.get("documentType") or "").strip().lower() == "certificate":
        score += 0.2
        reasons.append("document_type:certificate")
    return min(score, 0.9), reasons


def _score_unknown_review_route(capture: dict[str, Any], parse_payload: dict[str, Any]) -> tuple[float, list[str]]:
    reasons = ["fallback:manual_review"]
    if _capture_document_hint(capture):
        reasons.append(f"document_hint:{_capture_document_hint(capture)}")
    if parse_payload.get("documentType"):
        reasons.append(f"document_type:{parse_payload.get('documentType')}")
    return 0.66, reasons


def _score_route_candidate(
    route_id: str,
    capture: dict[str, Any],
    parse_payload: dict[str, Any],
) -> tuple[float, list[str]]:
    if route_id == "receipt.invoice":
        return _score_receipt_route(capture, parse_payload)
    if route_id == "seed_label_or_tag":
        return _score_seed_label_route(capture, parse_payload)
    if route_id == "storage_lot_label":
        return _score_storage_lot_label_route(capture, parse_payload)
    if route_id == "fertilizer_label":
        return _score_fertilizer_label_route(capture, parse_payload)
    if route_id == "seed_authorization_or_derogation":
        return _score_seed_authorization_route(capture, parse_payload)
    if route_id == "fertilization_plan":
        return _score_fertilization_plan_route(capture, parse_payload)
    if route_id == "delivery_note":
        return _score_delivery_note_route(capture, parse_payload)
    if route_id == "soil_analysis_report":
        return _score_soil_report_route(capture, parse_payload)
    if route_id in {"supplier_certificate", "organic_certificate", "inspection_or_noncompliance_doc"}:
        return _score_certificate_route(capture, parse_payload)
    if route_id == "unknown.review":
        return _score_unknown_review_route(capture, parse_payload)
    return 0.0, []


def route_candidates_for_session(
    captures: Sequence[dict[str, Any]],
    *,
    parse_runs_by_capture_id: dict[str, dict[str, Any]],
    route_items: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    aggregated: dict[str, dict[str, Any]] = {}
    for capture in captures:
        capture_id = str(capture.get("captureId") or "")
        route_hint = _capture_route_hint(capture)
        parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
        for route in route_items:
            route_id = str(route.get("routeId") or "")
            availability = str(route.get("availability") or route.get("runtimeBaseAvailability") or "catalog_only")
            if availability == "catalog_only" and route_id != "unknown.review":
                continue
            score, reasons = _score_route_candidate(route_id, capture, parse_payload)
            if route_hint and route_hint == route_id:
                score = min(0.999, max(score, 0.995))
                reasons = [*reasons, f"route_hint:{route_hint}"]
            if score <= 0:
                continue
            current = aggregated.get(route_id)
            if current is None or score > float(current.get("score") or 0):
                aggregated[route_id] = {
                    "routeId": route_id,
                    "score": round(score, 3),
                    "availability": availability,
                    "reasonCodes": reasons,
                    "riskClass": str(route.get("authorityClass") or route_id),
                    "requiresReview": True,
                    "sourceCaptureIds": [capture_id],
                }
            else:
                current["reasonCodes"] = sorted(
                    {
                        *[str(item) for item in current.get("reasonCodes") or [] if str(item).strip()],
                        *reasons,
                    }
                )
                current["sourceCaptureIds"] = sorted(
                    {
                        *[str(item) for item in current.get("sourceCaptureIds") or [] if str(item).strip()],
                        capture_id,
                    }
                )
    if "unknown.review" not in aggregated:
        fallback_route = next((item for item in route_items if str(item.get("routeId")) == "unknown.review"), None)
        if fallback_route and captures:
            score, reasons = _score_unknown_review_route(captures[0], _parse_response_payload(parse_runs_by_capture_id.get(str(captures[0].get("captureId") or ""))))
            aggregated["unknown.review"] = {
                "routeId": "unknown.review",
                "score": round(score, 3),
                "availability": str(fallback_route.get("availability") or "enabled"),
                "reasonCodes": reasons,
                "riskClass": "unknown.review",
                "requiresReview": True,
                "sourceCaptureIds": [str(captures[0].get("captureId") or "")],
            }
    ranked = sorted(
        aggregated.values(),
        key=lambda item: (float(item.get("score") or 0), str(item.get("routeId") or "")),
        reverse=True,
    )
    return ranked[:TOP_CANDIDATE_COUNT]


def select_route_and_helpers(
    candidates: Sequence[dict[str, Any]],
) -> tuple[str, list[str]]:
    if not candidates:
        return "unknown.review", []
    top = dict(candidates[0])
    second_score = float(candidates[1].get("score") or 0) if len(candidates) > 1 else 0.0
    top_score = float(top.get("score") or 0)
    selected = "unknown.review"
    top_enabled = str(top.get("availability") or "") == "enabled"
    if top_score >= MANUAL_ROUTE_MIN and top_enabled:
        selected = str(top.get("routeId") or "unknown.review")
    if top_enabled and top_score >= AUTO_SELECT_MIN and (top_score - second_score) >= COMPETITIVE_DELTA_MIN:
        selected = str(top.get("routeId") or selected)
    helpers: list[str] = []
    if selected == "receipt.invoice" and any(
        str(item.get("routeId") or "") == "seed_label_or_tag" and float(item.get("score") or 0) >= 0.7
        for item in candidates
    ):
        helpers.append("receipt_plus_label_link")
    return selected, helpers


def _proposal_value_text(proposal: dict[str, Any] | None) -> str | None:
    if not isinstance(proposal, dict):
        return None
    for key in ("valueText", "valueDate"):
        value = proposal.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _proposal_value_num(proposal: dict[str, Any] | None) -> float | None:
    if not isinstance(proposal, dict):
        return None
    value = proposal.get("valueNum")
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _proposal_value_int(proposal: dict[str, Any] | None) -> int | None:
    value = _proposal_value_num(proposal)
    if value is None:
        return None
    if float(value).is_integer():
        return int(value)
    return None


def _proposal_value_bool(proposal: dict[str, Any] | None) -> bool | None:
    if not isinstance(proposal, dict):
        return None
    raw_value = proposal.get("valueBool")
    if isinstance(raw_value, bool):
        return raw_value
    text = _proposal_value_text(proposal)
    if text is None:
        return None
    normalized = text.strip().lower()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def split_seed_treatment_substances_text(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        candidates = value
    else:
        text = str(value).strip()
        if not text:
            return []
        candidates = _SEED_TREATMENT_SUBSTANCE_SPLIT_RE.split(text)
    normalized: list[str] = []
    for raw_value in candidates:
        text = str(raw_value).strip(" \t\r\n:;,.")
        if not text:
            continue
        if text not in normalized:
            normalized.append(text)
    return normalized


def _seed_label_quality_follow_up_payload(
    *,
    germination_pct: float | None,
    purity_pct: float | None,
    treated_flag: bool | None,
    certified_flag: bool | None,
    test_completed_month: int | None,
    test_completed_year: int | None,
    certifying_agency_ref: str | None,
    certification_class_code: str | None,
    certification_label_ref: str | None,
    treatment_substances: Sequence[str],
    treatment_process_text: str | None,
) -> dict[str, Any] | None:
    if (
        germination_pct is None
        or purity_pct is None
        or treated_flag is None
        or certified_flag is None
        or test_completed_month is None
        or test_completed_year is None
    ):
        return None
    payload: dict[str, Any] = {
        "testCompletedMonth": test_completed_month,
        "testCompletedYear": test_completed_year,
    }
    if treated_flag:
        normalized_substances = [str(item).strip() for item in treatment_substances if str(item).strip()]
        if not normalized_substances and not str(treatment_process_text or "").strip():
            return None
        if normalized_substances:
            payload["treatmentSubstances"] = normalized_substances
        if str(treatment_process_text or "").strip():
            payload["treatmentProcessText"] = str(treatment_process_text).strip()
    if certified_flag:
        if not str(certifying_agency_ref or "").strip() or not str(certification_class_code or "").strip():
            return None
        payload["certifyingAgencyRef"] = str(certifying_agency_ref).strip()
        payload["certificationClassCode"] = str(certification_class_code).strip()
        if str(certification_label_ref or "").strip():
            payload["certificationLabelRef"] = str(certification_label_ref).strip()
    return payload


def _proposal_confidence(proposal: dict[str, Any] | None) -> float:
    if not isinstance(proposal, dict):
        return 0.5
    try:
        return max(0.0, min(float(proposal.get("confidence") or 0.5), 1.0))
    except (TypeError, ValueError):
        return 0.5


def _proposal_resolution(proposal: dict[str, Any] | None) -> dict[str, Any]:
    normalized = bool(isinstance(proposal, dict) and str(proposal.get("normalizedFrom") or "").strip())
    return {
        "status": "normalized_text" if normalized else "raw_text",
        "refType": None,
        "refUri": None,
    }


def _make_field_proposal(
    *,
    path: str,
    value: Any,
    proposal: dict[str, Any] | None,
    capture_id: str,
    authority_tier: str = "ocr_exact",
) -> dict[str, Any]:
    return {
        "path": path,
        "value": value,
        "confidence": _proposal_confidence(proposal),
        "authorityTier": authority_tier,
        "sourceCaptureIds": [capture_id],
        "resolution": _proposal_resolution(proposal),
        "reviewState": "pending",
    }


def _make_reference_field_proposal(
    *,
    path: str,
    value: Any,
    capture_id: str,
    ref_type: str,
    ref_uri: str,
    confidence: float,
    authority_tier: str = "inventory_exact_match",
) -> dict[str, Any]:
    normalized_confidence = max(0.0, min(float(confidence), 1.0))
    return {
        "path": path,
        "value": value,
        "confidence": normalized_confidence,
        "authorityTier": authority_tier,
        "sourceCaptureIds": [capture_id],
        "resolution": {
            "status": "resolved_ref",
            "refType": ref_type,
            "refUri": ref_uri,
        },
        "reviewState": "pending",
    }


def _proposal_like(value: Any, *, preferred: str = "text") -> dict[str, Any] | None:
    if isinstance(value, dict):
        return dict(value) if value else None
    if value is None:
        return None
    if preferred in {"number", "number_or_text"}:
        try:
            return {"valueNum": float(value)}
        except (TypeError, ValueError):
            pass
    text = str(value).strip()
    if not text:
        return None
    if preferred == "date":
        return {"valueDate": text}
    return {"valueText": text}


def _proposal_from_row(row: dict[str, Any], key: str, *, preferred: str = "text") -> dict[str, Any] | None:
    if key not in row or row.get(key) is None:
        return None
    proposal = _proposal_like(row.get(key), preferred=preferred)
    if proposal is None:
        return None
    for metadata_key in ("confidence", "provenance", "normalizedFrom", "notes"):
        if row.get(metadata_key) is not None and metadata_key not in proposal:
            proposal[metadata_key] = row.get(metadata_key)
    return proposal


def _capture_context_ref(capture: dict[str, Any], key: str) -> str | None:
    hints = capture.get("hints") or {}
    context_refs = hints.get("contextRefs") or {}
    value = str(context_refs.get(key) or "").strip()
    if value:
        return value
    derived = capture.get("derivedRefs") or {}
    value = str(derived.get(key) or "").strip()
    return value or None


def _build_fertilizer_label_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_input_material_resource: Callable[[str, Sequence[str], Sequence[str]], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")
    typed_payload = _fertilizer_label_payload(primary_parse_payload)
    primary_item = _primary_fertilizer_item(primary_parse_payload) or {}
    item_proposals = primary_item.get("proposals") or {}
    product_label_proposal = _proposal_like(typed_payload.get("productLabel")) or item_proposals.get("productLabel")
    product_label = _proposal_value_text(product_label_proposal) or str(primary_item.get("rawText") or "").strip() or None
    product_category_proposal = _proposal_like(typed_payload.get("productCategory"))
    product_category = _proposal_value_text(product_category_proposal)
    density_value, density_unit, density_value_proposal, density_unit_proposal = _fertilizer_density_entry(
        primary_parse_payload
    )
    marker_entries = _fertilizer_marker_entries(primary_parse_payload)
    ce_or_category_markers = [marker for marker, _ in marker_entries]
    application_text_raw, application_text_proposal = _fertilizer_text_field_entry(
        primary_parse_payload, "applicationTextRaw"
    )
    storage_text_raw, storage_text_proposal = _fertilizer_text_field_entry(primary_parse_payload, "storageTextRaw")
    typed_nutrient_entries = _fertilizer_declared_nutrient_entries(primary_parse_payload)
    inferred_fields: list[tuple[str, float, str, dict[str, Any] | None]]
    if typed_nutrient_entries:
        declared_nutrients = [
            {
                "nutrientCode": nutrient_code,
                "value": nutrient_value,
                "unit": nutrient_unit,
            }
            for nutrient_code, nutrient_value, nutrient_unit, _, _, _ in typed_nutrient_entries
        ]
        inferred_fields = [
            (
                nutrient_code,
                nutrient_value,
                nutrient_unit,
                nutrient_code_proposal or value_proposal or unit_proposal,
            )
            for nutrient_code, nutrient_value, nutrient_unit, nutrient_code_proposal, value_proposal, unit_proposal in typed_nutrient_entries
        ]
    else:
        nutrient_source_text = " ".join(
            value
            for value in (
                _proposal_value_text(product_label_proposal),
                str(primary_item.get("rawText") or "").strip(),
            )
            if value
        )
        declared_nutrients, inferred_fields = _infer_fertilizer_declared_nutrients(
            nutrient_source_text,
            proposal=product_label_proposal,
        )

    input_material_match = (
        resolve_input_material_resource(
            farm_uri,
            [product_label] if product_label else [],
            _capture_barcode_values(primary_capture),
        )
        if callable(resolve_input_material_resource)
        else None
    )
    input_material_resource_uri = str((input_material_match or {}).get("resourceUri") or "").strip() or None
    input_material_match_kind = str((input_material_match or {}).get("matchKind") or "").strip()

    payload = {
        "farmUri": farm_uri,
        "productLabel": product_label,
        "declaredNutrients": declared_nutrients,
        "inputMaterialResourceUri": input_material_resource_uri,
        "productCategory": product_category,
        "densityValue": density_value,
        "densityUnit": density_unit,
        "ceOrCategoryMarkers": ce_or_category_markers,
        "applicationTextRaw": application_text_raw,
        "storageTextRaw": storage_text_raw,
        "verificationState": "review_required",
        "documentUri": document_uri,
        "parseRunUri": parse_run_uri,
    }
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != "" and (not isinstance(value, list) or value or key == "declaredNutrients")
    }
    if "declaredNutrients" not in payload:
        payload["declaredNutrients"] = []

    proposals: list[dict[str, Any]] = []
    if product_label:
        proposals.append(
            _make_field_proposal(
                path="productLabel",
                value=product_label,
                proposal=product_label_proposal,
                capture_id=capture_id,
            )
        )
    if input_material_resource_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="inputMaterialResourceUri",
                value=input_material_resource_uri,
                capture_id=capture_id,
                ref_type="input_material_resource",
                ref_uri=input_material_resource_uri,
                confidence=0.99 if input_material_match_kind.startswith("barcode") else 0.9,
            )
        )
    if product_category:
        proposals.append(
            _make_field_proposal(
                path="productCategory",
                value=product_category,
                proposal=product_category_proposal,
                capture_id=capture_id,
            )
        )
    if density_value is not None:
        proposals.append(
            _make_field_proposal(
                path="densityValue",
                value=density_value,
                proposal=density_value_proposal,
                capture_id=capture_id,
            )
        )
    if density_unit:
        proposals.append(
            _make_field_proposal(
                path="densityUnit",
                value=density_unit,
                proposal=density_unit_proposal,
                capture_id=capture_id,
            )
        )
    if application_text_raw:
        proposals.append(
            _make_field_proposal(
                path="applicationTextRaw",
                value=application_text_raw,
                proposal=application_text_proposal,
                capture_id=capture_id,
            )
        )
    if storage_text_raw:
        proposals.append(
            _make_field_proposal(
                path="storageTextRaw",
                value=storage_text_raw,
                proposal=storage_text_proposal,
                capture_id=capture_id,
            )
        )
    for index, (marker, marker_proposal) in enumerate(marker_entries):
        proposals.append(
            _make_field_proposal(
                path=f"ceOrCategoryMarkers[{index}]",
                value=marker,
                proposal=marker_proposal,
                capture_id=capture_id,
            )
        )
    for index, (nutrient_code, nutrient_value, unit, nutrient_proposal) in enumerate(inferred_fields):
        proposals.append(
            _make_field_proposal(
                path=f"declaredNutrients[{index}].nutrientCode",
                value=nutrient_code,
                proposal=nutrient_proposal,
                capture_id=capture_id,
            )
        )
        proposals.append(
            _make_field_proposal(
                path=f"declaredNutrients[{index}].value",
                value=nutrient_value,
                proposal=nutrient_proposal,
                capture_id=capture_id,
            )
        )
        proposals.append(
            _make_field_proposal(
                path=f"declaredNutrients[{index}].unit",
                value=unit,
                proposal=nutrient_proposal,
                capture_id=capture_id,
            )
        )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _fertilizer_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _seed_label_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("lotCode") or "").strip():
        blockers.append("missing_lot_code")
    input_material = payload.get("inputMaterial") or {}
    resource_uri = str((input_material or {}).get("resourceUri") or "").strip()
    resource_label = str((((input_material or {}).get("resource") or {}).get("label")) or "").strip()
    if not resource_uri and not resource_label:
        blockers.append("missing_input_material")
    seed_payload = payload.get("seed") or {}
    if not str((seed_payload or {}).get("varietyUri") or "").strip():
        blockers.append("missing_variety_uri")
    return blockers


def _build_seed_label_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_input_material_resource: Callable[[str, Sequence[str], Sequence[str]], dict[str, Any] | None] | None = None,
    resolve_document_evidence_uri: Callable[[str], str | None] | None = None,
    resolve_crop_type_from_exact_label: Callable[[str], dict[str, Any] | None] | None = None,
    resolve_variety_from_exact_label: Callable[[str, str], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")
    source = str(primary_capture.get("source") or primary_capture.get("modality") or "intake").strip() or "intake"
    source_ref_seed = document_uri or parse_run_uri or capture_id
    source_ref = f"intake-seed-label:{_tail_token(source_ref_seed)}"
    label_evidence_uri = (
        resolve_document_evidence_uri(document_uri)
        if document_uri and callable(resolve_document_evidence_uri)
        else None
    )

    product_label_proposal = _seed_label_field_proposal(primary_parse_payload, "productLabel")
    crop_label_proposal = _seed_label_field_proposal(primary_parse_payload, "cropLabel")
    variety_label_proposal = _seed_label_field_proposal(primary_parse_payload, "variety")
    lot_code_proposal = _seed_label_field_proposal(primary_parse_payload, "lotCode")
    germination_pct_proposal = _seed_label_field_proposal(primary_parse_payload, "germinationPct")
    purity_pct_proposal = _seed_label_field_proposal(primary_parse_payload, "purityPct")
    treated_flag_proposal = _seed_label_field_proposal(primary_parse_payload, "treatedFlag")
    certified_flag_proposal = _seed_label_field_proposal(primary_parse_payload, "certifiedFlag")
    test_completed_month_proposal = _seed_label_field_proposal(primary_parse_payload, "testCompletedMonth")
    test_completed_year_proposal = _seed_label_field_proposal(primary_parse_payload, "testCompletedYear")
    certifying_agency_ref_proposal = _seed_label_field_proposal(primary_parse_payload, "certifyingAgencyRef")
    certification_class_code_proposal = _seed_label_field_proposal(primary_parse_payload, "certificationClassCode")
    certification_label_ref_proposal = _seed_label_field_proposal(primary_parse_payload, "certificationLabelRef")
    treatment_substances_proposal = _seed_label_field_proposal(primary_parse_payload, "treatmentSubstances")
    treatment_process_text_proposal = _seed_label_field_proposal(primary_parse_payload, "treatmentProcessText")

    product_label = _proposal_value_text(product_label_proposal)
    crop_label = _proposal_value_text(crop_label_proposal)
    variety_label = _proposal_value_text(variety_label_proposal)
    lot_code = _proposal_value_text(lot_code_proposal)
    germination_pct = _proposal_value_num(germination_pct_proposal)
    purity_pct = _proposal_value_num(purity_pct_proposal)
    treated_flag = _proposal_value_bool(treated_flag_proposal)
    certified_flag = _proposal_value_bool(certified_flag_proposal)
    test_completed_month = _proposal_value_int(test_completed_month_proposal)
    test_completed_year = _proposal_value_int(test_completed_year_proposal)
    certifying_agency_ref = _proposal_value_text(certifying_agency_ref_proposal)
    certification_class_code = _proposal_value_text(certification_class_code_proposal)
    certification_label_ref = _proposal_value_text(certification_label_ref_proposal)
    treatment_substances = split_seed_treatment_substances_text(_proposal_value_text(treatment_substances_proposal))
    treatment_process_text = _proposal_value_text(treatment_process_text_proposal)
    barcode_values = _capture_barcode_values(primary_capture)

    input_material_match = (
        resolve_input_material_resource(
            farm_uri,
            [product_label] if product_label else [],
            barcode_values,
        )
        if callable(resolve_input_material_resource)
        else None
    )
    input_material_resource_uri = str((input_material_match or {}).get("resourceUri") or "").strip() or None

    crop_type_match = (
        resolve_crop_type_from_exact_label(crop_label)
        if crop_label and callable(resolve_crop_type_from_exact_label)
        else None
    )
    crop_type_uri = str((crop_type_match or {}).get("cropTypeUri") or "").strip() or None
    variety_match = (
        resolve_variety_from_exact_label(crop_type_uri, variety_label)
        if crop_type_uri and variety_label and callable(resolve_variety_from_exact_label)
        else None
    )
    variety_uri = str((variety_match or {}).get("varietyUri") or "").strip() or None

    input_material_payload: dict[str, Any] = {}
    if input_material_resource_uri:
        input_material_payload["resourceUri"] = input_material_resource_uri
    elif product_label:
        input_material_payload["resource"] = {
            "label": product_label,
            "resourceType": "input_material",
        }

    seed_payload: dict[str, Any] = {}
    if variety_uri:
        seed_payload["varietyUri"] = variety_uri
    if germination_pct is not None:
        seed_payload["germinationPct"] = germination_pct
    if purity_pct is not None:
        seed_payload["purityPct"] = purity_pct
    if treated_flag is not None:
        seed_payload["treatedFlag"] = treated_flag
    if certified_flag is not None:
        seed_payload["certifiedFlag"] = certified_flag

    seed_quality_observation_payload = _seed_label_quality_follow_up_payload(
        germination_pct=germination_pct,
        purity_pct=purity_pct,
        treated_flag=treated_flag,
        certified_flag=certified_flag,
        test_completed_month=test_completed_month,
        test_completed_year=test_completed_year,
        certifying_agency_ref=certifying_agency_ref,
        certification_class_code=certification_class_code,
        certification_label_ref=certification_label_ref,
        treatment_substances=treatment_substances,
        treatment_process_text=treatment_process_text,
    )

    payload = {
        "farmUri": farm_uri,
        "lotKind": "seed",
        "inputMaterial": input_material_payload or None,
        "lotCode": lot_code,
        "evidence": {
            "labelEvidenceType": "external_document",
            "labelEvidenceRef": document_uri or parse_run_uri or capture_id,
            "labelEvidenceUri": label_evidence_uri,
        },
        "source": source,
        "sourceRef": source_ref,
        "seed": seed_payload or {},
        "seedQualityObservation": seed_quality_observation_payload or None,
    }
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != "" and (not isinstance(value, dict) or value)
    }

    proposals: list[dict[str, Any]] = [
        _make_field_proposal(
            path="lotKind",
            value="seed",
            proposal=_proposal_like("seed"),
            capture_id=capture_id,
            authority_tier="deterministic_decode",
        ),
        _make_field_proposal(
            path="source",
            value=source,
            proposal=_proposal_like(source),
            capture_id=capture_id,
            authority_tier="capture_context",
        ),
        _make_field_proposal(
            path="sourceRef",
            value=source_ref,
            proposal=_proposal_like(source_ref),
            capture_id=capture_id,
            authority_tier="deterministic_decode",
        ),
        _make_field_proposal(
            path="evidence.labelEvidenceType",
            value="external_document",
            proposal=_proposal_like("external_document"),
            capture_id=capture_id,
            authority_tier="deterministic_decode",
        ),
        _make_field_proposal(
            path="evidence.labelEvidenceRef",
            value=document_uri or parse_run_uri or capture_id,
            proposal=_proposal_like(document_uri or parse_run_uri or capture_id),
            capture_id=capture_id,
            authority_tier="source_document_binding",
        ),
    ]
    if label_evidence_uri:
        proposals.append(
            _make_field_proposal(
                path="evidence.labelEvidenceUri",
                value=label_evidence_uri,
                proposal=_proposal_like(label_evidence_uri),
                capture_id=capture_id,
                authority_tier="document_registry_evidence",
            )
        )
    if lot_code:
        proposals.append(
            _make_field_proposal(
                path="lotCode",
                value=lot_code,
                proposal=lot_code_proposal,
                capture_id=capture_id,
            )
        )
    if input_material_resource_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="inputMaterial.resourceUri",
                value=input_material_resource_uri,
                capture_id=capture_id,
                ref_type="input_material_resource",
                ref_uri=input_material_resource_uri,
                confidence=0.99,
                authority_tier="inventory_exact_match",
            )
        )
    elif product_label:
        proposals.append(
            _make_field_proposal(
                path="inputMaterial.resource.label",
                value=product_label,
                proposal=product_label_proposal,
                capture_id=capture_id,
            )
        )
        proposals.append(
            _make_field_proposal(
                path="inputMaterial.resource.resourceType",
                value="input_material",
                proposal=_proposal_like("input_material"),
                capture_id=capture_id,
                authority_tier="deterministic_decode",
            )
        )
    if variety_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="seed.varietyUri",
                value=variety_uri,
                capture_id=capture_id,
                ref_type="variety",
                ref_uri=variety_uri,
                confidence=float(((variety_match or {}).get("row") or {}).get("match", {}).get("score") or 0.98),
                authority_tier="reference_variety_exact_match",
            )
        )
    if germination_pct is not None:
        proposals.append(
            _make_field_proposal(
                path="seed.germinationPct",
                value=germination_pct,
                proposal=germination_pct_proposal,
                capture_id=capture_id,
            )
        )
    if purity_pct is not None:
        proposals.append(
            _make_field_proposal(
                path="seed.purityPct",
                value=purity_pct,
                proposal=purity_pct_proposal,
                capture_id=capture_id,
            )
        )
    if treated_flag is not None:
        proposals.append(
            _make_field_proposal(
                path="seed.treatedFlag",
                value=treated_flag,
                proposal=treated_flag_proposal,
                capture_id=capture_id,
            )
        )
    if certified_flag is not None:
        proposals.append(
            _make_field_proposal(
                path="seed.certifiedFlag",
                value=certified_flag,
                proposal=certified_flag_proposal,
                capture_id=capture_id,
            )
        )
    if test_completed_month is not None:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.testCompletedMonth",
                value=test_completed_month,
                proposal=test_completed_month_proposal,
                capture_id=capture_id,
            )
        )
    if test_completed_year is not None:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.testCompletedYear",
                value=test_completed_year,
                proposal=test_completed_year_proposal,
                capture_id=capture_id,
            )
        )
    if certifying_agency_ref:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.certifyingAgencyRef",
                value=certifying_agency_ref,
                proposal=certifying_agency_ref_proposal,
                capture_id=capture_id,
            )
        )
    if certification_class_code:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.certificationClassCode",
                value=certification_class_code,
                proposal=certification_class_code_proposal,
                capture_id=capture_id,
            )
        )
    if certification_label_ref:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.certificationLabelRef",
                value=certification_label_ref,
                proposal=certification_label_ref_proposal,
                capture_id=capture_id,
            )
        )
    if treatment_process_text:
        proposals.append(
            _make_field_proposal(
                path="seedQualityObservation.treatmentProcessText",
                value=treatment_process_text,
                proposal=treatment_process_text_proposal,
                capture_id=capture_id,
            )
        )
    for index, substance in enumerate(treatment_substances):
        proposals.append(
            _make_field_proposal(
                path=f"seedQualityObservation.treatmentSubstances[{index}]",
                value=substance,
                proposal=treatment_substances_proposal,
                capture_id=capture_id,
            )
        )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _seed_label_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _build_seed_authorization_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_field_from_gerk_ref: Callable[[str, str], dict[str, Any] | None] | None = None,
    resolve_crop_type_from_exact_label: Callable[[str], dict[str, Any] | None] | None = None,
    resolve_variety_from_exact_label: Callable[[str, str], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")
    field_uri = _capture_context_ref(primary_capture, "fieldUri")
    as_of_date_proposal = _seed_authorization_date_proposal(primary_parse_payload)
    decision_status_proposal = _seed_authorization_decision_code_proposal(primary_parse_payload)
    reason_code_proposal = _seed_authorization_reason_code_proposal(primary_parse_payload)
    reason_text_proposal = _seed_authorization_field_proposal(
        primary_parse_payload,
        "reasonText",
        "exceptionReasonText",
        "note",
        "notes",
    )
    availability_evidence_text_proposal = _seed_authorization_field_proposal(
        primary_parse_payload,
        "availabilityEvidenceText",
        "availabilityText",
        "evidenceSummary",
        "summary",
    )
    gerk_ref_proposal = _seed_authorization_field_proposal(
        primary_parse_payload,
        "gerkRef",
    )
    crop_label_proposal = _seed_authorization_field_proposal(
        primary_parse_payload,
        "cropLabel",
        "cropTypeLabel",
    )
    variety_label_proposal = _seed_authorization_field_proposal(
        primary_parse_payload,
        "varietyLabel",
        "variety",
    )
    attachment_role = _seed_authorization_attachment_role(primary_capture, primary_parse_payload)
    attachment_evidence_ref = document_uri or parse_run_uri or capture_id
    attachment_evidence = (
        [{"roleCode": attachment_role, "evidenceRef": attachment_evidence_ref}]
        if attachment_evidence_ref
        else []
    )
    gerk_ref = _proposal_value_text(gerk_ref_proposal)
    resolved_field_match = (
        resolve_field_from_gerk_ref(farm_uri, gerk_ref)
        if not field_uri and gerk_ref and callable(resolve_field_from_gerk_ref)
        else None
    )
    resolved_field_uri = str((resolved_field_match or {}).get("fieldUri") or "").strip() or None
    field_uri = field_uri or resolved_field_uri
    crop_label = _proposal_value_text(crop_label_proposal)
    variety_label = _proposal_value_text(variety_label_proposal)
    crop_type_match = (
        resolve_crop_type_from_exact_label(crop_label)
        if crop_label and callable(resolve_crop_type_from_exact_label)
        else None
    )
    crop_type_uri = str((crop_type_match or {}).get("cropTypeUri") or "").strip() or None
    variety_match = (
        resolve_variety_from_exact_label(crop_type_uri, variety_label)
        if crop_type_uri and variety_label and callable(resolve_variety_from_exact_label)
        else None
    )
    variety_uri = str((variety_match or {}).get("varietyUri") or "").strip() or None

    payload = {
        "farmUri": farm_uri,
        "asOfDate": _proposal_value_text(as_of_date_proposal),
        "fieldUri": field_uri,
        "cropTypeUri": crop_type_uri,
        "cropLabel": crop_label,
        "varietyUri": variety_uri,
        "varietyLabel": variety_label,
        "decisionStatusCode": _proposal_value_text(decision_status_proposal),
        "reasonCode": _proposal_value_text(reason_code_proposal),
        "reasonText": _proposal_value_text(reason_text_proposal),
        "availabilityEvidenceText": _proposal_value_text(availability_evidence_text_proposal),
        "attachmentEvidence": attachment_evidence,
    }
    if str(payload.get("reasonCode") or "").strip().lower() != "other":
        payload.pop("reasonText", None)
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != "" and (not isinstance(value, list) or value)
    }

    proposals: list[dict[str, Any]] = []
    if payload.get("asOfDate"):
        proposals.append(
            _make_field_proposal(
                path="asOfDate",
                value=payload["asOfDate"],
                proposal=as_of_date_proposal,
                capture_id=capture_id,
            )
        )
    if field_uri:
        if _capture_context_ref(primary_capture, "fieldUri"):
            proposals.append(
                _make_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    proposal=_proposal_like(field_uri),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
        elif resolved_field_uri:
            proposals.append(
                _make_reference_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    capture_id=capture_id,
                    ref_type="field",
                    ref_uri=field_uri,
                    confidence=0.99,
                    authority_tier="field_authority_exact_match",
                )
            )
    if crop_type_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="cropTypeUri",
                value=crop_type_uri,
                capture_id=capture_id,
                ref_type="crop_type",
                ref_uri=crop_type_uri,
                confidence=float(((crop_type_match or {}).get("row") or {}).get("match", {}).get("score") or 0.98),
                authority_tier="reference_crop_exact_match",
            )
        )
    if payload.get("cropLabel"):
        proposals.append(
            _make_field_proposal(
                path="cropLabel",
                value=payload["cropLabel"],
                proposal=crop_label_proposal,
                capture_id=capture_id,
            )
        )
    if variety_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="varietyUri",
                value=variety_uri,
                capture_id=capture_id,
                ref_type="variety",
                ref_uri=variety_uri,
                confidence=float(((variety_match or {}).get("row") or {}).get("match", {}).get("score") or 0.98),
                authority_tier="reference_variety_exact_match",
            )
        )
    if payload.get("varietyLabel"):
        proposals.append(
            _make_field_proposal(
                path="varietyLabel",
                value=payload["varietyLabel"],
                proposal=variety_label_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("decisionStatusCode"):
        proposals.append(
            _make_field_proposal(
                path="decisionStatusCode",
                value=payload["decisionStatusCode"],
                proposal=decision_status_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("reasonCode"):
        proposals.append(
            _make_field_proposal(
                path="reasonCode",
                value=payload["reasonCode"],
                proposal=reason_code_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("reasonText"):
        proposals.append(
            _make_field_proposal(
                path="reasonText",
                value=payload["reasonText"],
                proposal=reason_text_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("availabilityEvidenceText"):
        proposals.append(
            _make_field_proposal(
                path="availabilityEvidenceText",
                value=payload["availabilityEvidenceText"],
                proposal=availability_evidence_text_proposal,
                capture_id=capture_id,
            )
        )
    if attachment_evidence:
        proposals.append(
            _make_field_proposal(
                path="attachmentEvidence[0].roleCode",
                value=attachment_role,
                proposal=_proposal_like(attachment_role),
                capture_id=capture_id,
                authority_tier="deterministic_decode",
            )
        )
        proposals.append(
            _make_field_proposal(
                path="attachmentEvidence[0].evidenceRef",
                value=attachment_evidence_ref,
                proposal=_proposal_like(attachment_evidence_ref),
                capture_id=capture_id,
                authority_tier="source_document_binding",
            )
        )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _seed_authorization_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _build_fertilization_plan_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_field_from_gerk_ref: Callable[[str, str], dict[str, Any] | None] | None = None,
    resolve_crop_instance_from_field_declaration: Callable[..., dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    field_uri_context = _capture_context_ref(primary_capture, "fieldUri")
    crop_instance_uri_context = _capture_context_ref(primary_capture, "cropInstanceUri")
    planning_window_start_proposal = _fertilization_plan_field_proposal(
        primary_parse_payload,
        "planningWindowStart",
        "windowStart",
        "validFrom",
        preferred="date",
    )
    planning_window_end_proposal = _fertilization_plan_field_proposal(
        primary_parse_payload,
        "planningWindowEnd",
        "windowEnd",
        "validTo",
        preferred="date",
    )
    target_yield_value_proposal = _fertilization_plan_field_proposal(
        primary_parse_payload,
        "targetYieldValue",
        preferred="number",
    )
    target_yield_unit_proposal = _fertilization_plan_field_proposal(
        primary_parse_payload,
        "targetYieldUnit",
        preferred="text",
    )
    rule_profile_proposal = _fertilization_plan_field_proposal(primary_parse_payload, "ruleProfile", preferred="text")
    gerk_ref_proposal = _fertilization_plan_field_proposal(primary_parse_payload, "gerkRef", preferred="text")

    if target_yield_value_proposal is None or target_yield_unit_proposal is None:
        match = _PLAN_TARGET_YIELD_RE.search(_fertilization_plan_source_text(primary_parse_payload))
        if match:
            if target_yield_value_proposal is None:
                target_yield_value = _parse_decimal_number(match.group(1))
                if target_yield_value is not None:
                    target_yield_value_proposal = {"valueNum": target_yield_value, "confidence": 0.8}
            if target_yield_unit_proposal is None:
                target_yield_unit = _normalize_plan_unit(match.group(2))
                if target_yield_unit:
                    target_yield_unit_proposal = {"valueText": target_yield_unit, "confidence": 0.8}

    payload_target_nutrients: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    nutrient_entries = _fertilization_plan_target_nutrient_entries(primary_parse_payload)
    for index, entry in enumerate(nutrient_entries):
        nutrient_code = _proposal_value_text(entry.get("nutrientCodeProposal"))
        value = _proposal_value_num(entry.get("valueProposal"))
        if value is None:
            value = _parse_decimal_number(_proposal_value_text(entry.get("valueProposal")))
        unit = _normalize_plan_unit(_proposal_value_text(entry.get("unitProposal")))
        if not nutrient_code or value is None or not unit:
            continue
        payload_target_nutrients.append(
            {
                "nutrientCode": nutrient_code,
                "value": value,
                "unit": unit,
            }
        )
        proposals.append(
            _make_field_proposal(
                path=f"targetNutrients[{index}].nutrientCode",
                value=nutrient_code,
                proposal=entry.get("nutrientCodeProposal"),
                capture_id=capture_id,
            )
        )
        proposals.append(
            _make_field_proposal(
                path=f"targetNutrients[{index}].value",
                value=value,
                proposal=entry.get("valueProposal"),
                capture_id=capture_id,
            )
        )
        proposals.append(
            _make_field_proposal(
                path=f"targetNutrients[{index}].unit",
                value=unit,
                proposal=entry.get("unitProposal"),
                capture_id=capture_id,
            )
        )

    planning_window_start = _proposal_value_text(planning_window_start_proposal)
    planning_window_end = _proposal_value_text(planning_window_end_proposal)
    target_yield_value = _proposal_value_num(target_yield_value_proposal)
    target_yield_unit = _normalize_plan_unit(_proposal_value_text(target_yield_unit_proposal))
    rule_profile = _proposal_value_text(rule_profile_proposal)
    gerk_ref = _proposal_value_text(gerk_ref_proposal)
    resolved_field_match = (
        resolve_field_from_gerk_ref(farm_uri, gerk_ref)
        if not field_uri_context and gerk_ref and callable(resolve_field_from_gerk_ref)
        else None
    )
    resolved_field_uri = str((resolved_field_match or {}).get("fieldUri") or "").strip() or None
    field_uri = field_uri_context or resolved_field_uri
    resolution_season_code = _fertilization_plan_resolution_season_code(planning_window_start, planning_window_end)
    resolved_crop_instance_match = None
    if (
        not crop_instance_uri_context
        and field_uri
        and resolution_season_code
        and callable(resolve_crop_instance_from_field_declaration)
    ):
        resolved_crop_instance_match = (
            resolve_crop_instance_from_field_declaration(
                farm_uri,
                field_uri,
                resolution_season_code,
                gerk_ref=gerk_ref,
            )
            if gerk_ref
            else resolve_crop_instance_from_field_declaration(
                farm_uri,
                field_uri,
                resolution_season_code,
            )
        )
    resolved_crop_instance_uri = (
        str((resolved_crop_instance_match or {}).get("cropInstanceUri") or "").strip() or None
    )
    crop_instance_uri = crop_instance_uri_context or resolved_crop_instance_uri
    assumptions = _fertilization_plan_payload(primary_parse_payload).get("assumptions")
    linked_soil_lab_result_uris = _fertilization_plan_list_value(primary_parse_payload, "linkedSoilLabResultUris")
    linked_soil_amendment_plan_uris = _fertilization_plan_list_value(
        primary_parse_payload,
        "linkedSoilAmendmentPlanUris",
    )

    payload = {
        "farmUri": farm_uri,
        "fieldUri": field_uri,
        "cropInstanceUri": crop_instance_uri,
        "planningWindowStart": planning_window_start,
        "planningWindowEnd": planning_window_end,
        "targetYieldValue": target_yield_value,
        "targetYieldUnit": target_yield_unit,
        "ruleProfile": rule_profile,
        "targetNutrients": payload_target_nutrients,
        "linkedSoilLabResultUris": linked_soil_lab_result_uris,
        "linkedSoilAmendmentPlanUris": linked_soil_amendment_plan_uris,
    }
    if gerk_ref:
        payload["gerkRef"] = gerk_ref
    if isinstance(assumptions, dict) and assumptions:
        payload["assumptions"] = dict(assumptions)
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != "" and (not isinstance(value, list) or value or key == "targetNutrients")
    }
    if "targetNutrients" not in payload:
        payload["targetNutrients"] = []

    if field_uri:
        if field_uri_context:
            proposals.append(
                _make_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    proposal=_proposal_like(field_uri),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
        elif resolved_field_uri:
            proposals.append(
                _make_reference_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    capture_id=capture_id,
                    ref_type="field",
                    ref_uri=field_uri,
                    confidence=0.99,
                    authority_tier="field_authority_exact_match",
                )
            )
    if crop_instance_uri:
        if crop_instance_uri_context:
            proposals.append(
                _make_field_proposal(
                    path="cropInstanceUri",
                    value=crop_instance_uri,
                    proposal=_proposal_like(crop_instance_uri),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
        elif resolved_crop_instance_uri:
            proposals.append(
                _make_reference_field_proposal(
                    path="cropInstanceUri",
                    value=crop_instance_uri,
                    capture_id=capture_id,
                    ref_type="crop_instance",
                    ref_uri=crop_instance_uri,
                    confidence=0.99,
                    authority_tier="field_declaration_exact_match",
                )
            )
    if planning_window_start:
        proposals.append(
            _make_field_proposal(
                path="planningWindowStart",
                value=planning_window_start,
                proposal=planning_window_start_proposal,
                capture_id=capture_id,
            )
        )
    if planning_window_end:
        proposals.append(
            _make_field_proposal(
                path="planningWindowEnd",
                value=planning_window_end,
                proposal=planning_window_end_proposal,
                capture_id=capture_id,
            )
        )
    if target_yield_value is not None:
        proposals.append(
            _make_field_proposal(
                path="targetYieldValue",
                value=target_yield_value,
                proposal=target_yield_value_proposal,
                capture_id=capture_id,
            )
        )
    if target_yield_unit:
        proposals.append(
            _make_field_proposal(
                path="targetYieldUnit",
                value=target_yield_unit,
                proposal=target_yield_unit_proposal,
                capture_id=capture_id,
            )
        )
    if rule_profile:
        proposals.append(
            _make_field_proposal(
                path="ruleProfile",
                value=rule_profile,
                proposal=rule_profile_proposal,
                capture_id=capture_id,
            )
        )
    if gerk_ref:
        proposals.append(
            _make_field_proposal(
                path="gerkRef",
                value=gerk_ref,
                proposal=gerk_ref_proposal,
                capture_id=capture_id,
            )
        )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _fertilization_plan_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _delivery_note_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("deliveredAt") or "").strip():
        blockers.append("missing_delivered_at")
    if not str(payload.get("fromStorageLotUri") or "").strip():
        blockers.append("missing_from_storage_lot_uri")
    if not str(payload.get("buyerRef") or "").strip():
        blockers.append("missing_buyer_ref")
    if not str(payload.get("ticketRef") or "").strip():
        blockers.append("missing_ticket_ref")
    if payload.get("netWeight") is None or str(payload.get("netWeight")).strip() == "":
        blockers.append("missing_net_weight")
    if not str(payload.get("weightUnit") or "").strip():
        blockers.append("missing_weight_unit")
    if payload.get("tareWeight") is not None and payload.get("grossWeight") is None:
        blockers.append("missing_gross_weight")
    gross_weight = _parse_decimal_number(payload.get("grossWeight"))
    tare_weight = _parse_decimal_number(payload.get("tareWeight"))
    net_weight = _parse_decimal_number(payload.get("netWeight"))
    if gross_weight is not None and tare_weight is not None and gross_weight < tare_weight:
        blockers.append("invalid_gross_tare_context")
    if gross_weight is not None and net_weight is not None and net_weight > gross_weight:
        blockers.append("invalid_net_weight_context")
    weight_unit = str(payload.get("weightUnit") or "").strip().lower()
    if weight_unit == "bu" and not str(payload.get("commodityRef") or "").strip():
        blockers.append("missing_commodity_ref")
    if str(payload.get("qualityGradeCode") or "").strip() and not str(payload.get("qualityGradeSystemUri") or "").strip():
        blockers.append("missing_quality_grade_system_uri")
    value = _parse_decimal_number(payload.get("value"))
    value_eur = _parse_decimal_number(payload.get("valueEur"))
    currency = str(payload.get("currency") or "").strip().upper()
    if value is not None and not currency:
        blockers.append("missing_currency")
    if currency and value is None and value_eur is None:
        blockers.append("missing_value")
    if currency and currency != "EUR":
        blockers.append("unsupported_currency")
    if value is not None and value_eur is not None and abs(value - value_eur) > 1e-9:
        blockers.append("conflicting_value_context")
    return blockers


def _storage_lot_label_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("lotCode") or "").strip():
        blockers.append("missing_lot_code")
    if not str(payload.get("storageLotUri") or "").strip():
        blockers.append("missing_storage_lot_uri")
    attachment_items = [item for item in list(payload.get("attachmentEvidence") or []) if isinstance(item, dict)]
    if not str(payload.get("documentUri") or "").strip() and not attachment_items:
        blockers.append("missing_source_document")
    return blockers


def _build_storage_lot_label_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_storage_lot_from_lot_code: Callable[[str, Sequence[str]], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")
    primary_item = _storage_lot_label_primary_item(primary_parse_payload) or {}
    item_proposals = primary_item.get("proposals") or {}
    product_label_proposal = item_proposals.get("productLabel")
    lot_code_proposal = _storage_lot_label_lot_code_proposal(primary_parse_payload)
    product_label = _proposal_value_text(product_label_proposal) or str(primary_item.get("rawText") or "").strip() or None
    lot_code = _proposal_value_text(lot_code_proposal)
    storage_lot_match = (
        resolve_storage_lot_from_lot_code(farm_uri, [lot_code] if lot_code else [])
        if lot_code and callable(resolve_storage_lot_from_lot_code)
        else None
    )
    storage_lot_uri = str((storage_lot_match or {}).get("storageLotUri") or "").strip() or None

    payload = {
        "farmUri": farm_uri,
        "storageLotUri": storage_lot_uri,
        "lotCode": lot_code,
        "productLabel": product_label,
        "documentUri": document_uri,
        "parseRunUri": parse_run_uri,
    }
    payload = {key: value for key, value in payload.items() if value is not None and value != ""}

    proposals: list[dict[str, Any]] = []
    if product_label:
        proposals.append(
            _make_field_proposal(
                path="productLabel",
                value=product_label,
                proposal=product_label_proposal,
                capture_id=capture_id,
            )
        )
    if lot_code:
        proposals.append(
            _make_field_proposal(
                path="lotCode",
                value=lot_code,
                proposal=lot_code_proposal,
                capture_id=capture_id,
            )
        )
    if storage_lot_uri:
        proposals.append(
            _make_reference_field_proposal(
                path="storageLotUri",
                value=storage_lot_uri,
                capture_id=capture_id,
                ref_type="storage_lot",
                ref_uri=storage_lot_uri,
                confidence=0.95,
                authority_tier="storage_lot_exact_match",
            )
        )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _storage_lot_label_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _build_delivery_note_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_partner_from_exact_identifiers: Callable[..., dict[str, Any] | None] | None = None,
    resolve_storage_lot_from_lot_code: Callable[[str, Sequence[str]], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    from_storage_lot_uri = _capture_context_ref(primary_capture, "fromStorageLotUri")
    buyer_ref = _capture_context_ref(primary_capture, "buyerRef")
    commodity_ref = _capture_context_ref(primary_capture, "commodityRef")
    delivered_at_proposal = _delivery_note_delivered_at_proposal(primary_parse_payload)
    ticket_ref_proposal = _delivery_note_ticket_ref_proposal(primary_parse_payload)
    lot_code_proposal = _delivery_note_lot_code_proposal(primary_parse_payload)
    lot_code = _proposal_value_text(lot_code_proposal)
    buyer_label_proposal = _delivery_note_field_proposal(primary_parse_payload, "buyerLabel", preferred="text")
    buyer_registration_id_proposal = _delivery_note_field_proposal(
        primary_parse_payload,
        "buyerRegistrationId",
        preferred="text",
    )
    buyer_vat_id_proposal = _delivery_note_field_proposal(primary_parse_payload, "buyerVatId", preferred="text")
    buyer_label = _proposal_value_text(buyer_label_proposal)
    buyer_registration_id = _proposal_value_text(buyer_registration_id_proposal)
    buyer_vat_id = _proposal_value_text(buyer_vat_id_proposal)
    buyer_address_proposal = _delivery_note_field_proposal(
        primary_parse_payload,
        "buyerAddress",
        "destinationAddress",
        "shipToAddress",
        preferred="text",
    )
    moisture_proposal = _delivery_note_moisture_proposal(primary_parse_payload)
    measurements = _delivery_note_measurements(primary_parse_payload)
    net_weight_entry = measurements.get("netWeight")
    gross_weight_entry = measurements.get("grossWeight")
    tare_weight_entry = measurements.get("tareWeight")
    resolved_weight_unit = (
        (net_weight_entry[1] if net_weight_entry else None)
        or (gross_weight_entry[1] if gross_weight_entry else None)
        or (tare_weight_entry[1] if tare_weight_entry else None)
    )
    storage_lot_match = (
        resolve_storage_lot_from_lot_code(farm_uri, [lot_code] if lot_code else [])
        if not from_storage_lot_uri and lot_code and callable(resolve_storage_lot_from_lot_code)
        else None
    )
    if not from_storage_lot_uri:
        from_storage_lot_uri = str((storage_lot_match or {}).get("storageLotUri") or "").strip() or None
    storage_lot_row = dict((storage_lot_match or {}).get("row") or {}) if isinstance(storage_lot_match, dict) else {}
    if not commodity_ref and str(resolved_weight_unit or "").strip().lower() == "bu":
        commodity_ref = str(storage_lot_row.get("cropTypeUri") or "").strip() or None
    partner_match = (
        resolve_partner_from_exact_identifiers(
            farm_uri,
            [buyer_label] if buyer_label else [],
            [buyer_registration_id] if buyer_registration_id else [],
            [buyer_vat_id] if buyer_vat_id else [],
            role_code="customer",
        )
        if not buyer_ref
        and callable(resolve_partner_from_exact_identifiers)
        and (buyer_registration_id or buyer_vat_id)
        else None
    )
    if not buyer_ref:
        buyer_ref = str((partner_match or {}).get("partyUri") or "").strip() or None

    payload = {
        "farmUri": farm_uri,
        "deliveredAt": _proposal_value_text(delivered_at_proposal),
        "fromStorageLotUri": from_storage_lot_uri,
        "buyerRef": buyer_ref,
        "buyerAddress": _proposal_value_text(buyer_address_proposal),
        "ticketRef": _proposal_value_text(ticket_ref_proposal),
        "netWeight": net_weight_entry[0] if net_weight_entry else None,
        "weightUnit": resolved_weight_unit,
        "grossWeight": gross_weight_entry[0] if gross_weight_entry else None,
        "tareWeight": tare_weight_entry[0] if tare_weight_entry else None,
        "moisturePct": _proposal_value_num(moisture_proposal),
        "commodityRef": commodity_ref,
    }
    payload = {key: value for key, value in payload.items() if value is not None and value != ""}

    proposals: list[dict[str, Any]] = []
    if payload.get("deliveredAt"):
        proposals.append(
            _make_field_proposal(
                path="deliveredAt",
                value=payload["deliveredAt"],
                proposal=delivered_at_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("ticketRef"):
        proposals.append(
            _make_field_proposal(
                path="ticketRef",
                value=payload["ticketRef"],
                proposal=ticket_ref_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("netWeight") is not None and net_weight_entry is not None:
        proposals.append(
            _make_field_proposal(
                path="netWeight",
                value=payload["netWeight"],
                proposal=net_weight_entry[2],
                capture_id=capture_id,
            )
        )
    if payload.get("weightUnit"):
        proposals.append(
            _make_field_proposal(
                path="weightUnit",
                value=payload["weightUnit"],
                proposal=(
                    net_weight_entry[2]
                    if net_weight_entry
                    else (gross_weight_entry[2] if gross_weight_entry else (tare_weight_entry[2] if tare_weight_entry else None))
                ),
                capture_id=capture_id,
            )
        )
    if payload.get("grossWeight") is not None and gross_weight_entry is not None:
        proposals.append(
            _make_field_proposal(
                path="grossWeight",
                value=payload["grossWeight"],
                proposal=gross_weight_entry[2],
                capture_id=capture_id,
            )
        )
    if payload.get("tareWeight") is not None and tare_weight_entry is not None:
        proposals.append(
            _make_field_proposal(
                path="tareWeight",
                value=payload["tareWeight"],
                proposal=tare_weight_entry[2],
                capture_id=capture_id,
            )
        )
    if payload.get("moisturePct") is not None:
        proposals.append(
            _make_field_proposal(
                path="moisturePct",
                value=payload["moisturePct"],
                proposal=moisture_proposal,
                capture_id=capture_id,
            )
        )
    if payload.get("buyerAddress"):
        proposals.append(
            _make_field_proposal(
                path="buyerAddress",
                value=payload["buyerAddress"],
                proposal=buyer_address_proposal,
                capture_id=capture_id,
            )
        )
    if from_storage_lot_uri:
        if storage_lot_match and str((storage_lot_match or {}).get("storageLotUri") or "").strip() == from_storage_lot_uri:
            proposals.append(
                _make_reference_field_proposal(
                    path="fromStorageLotUri",
                    value=from_storage_lot_uri,
                    capture_id=capture_id,
                    ref_type="storage_lot",
                    ref_uri=from_storage_lot_uri,
                    confidence=0.95,
                    authority_tier="storage_lot_exact_match",
                )
            )
        else:
            proposals.append(
                _make_field_proposal(
                    path="fromStorageLotUri",
                    value=from_storage_lot_uri,
                    proposal=_proposal_like(from_storage_lot_uri),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
    if buyer_ref:
        if partner_match and str((partner_match or {}).get("partyUri") or "").strip() == buyer_ref:
            partner_match_kind = str((partner_match or {}).get("matchKind") or "").strip()
            proposals.append(
                _make_reference_field_proposal(
                    path="buyerRef",
                    value=buyer_ref,
                    capture_id=capture_id,
                    ref_type="party",
                    ref_uri=buyer_ref,
                    confidence=0.99 if partner_match_kind == "partner_identifier_and_label_exact" else 0.95,
                    authority_tier=f"{partner_match_kind}_match" if partner_match_kind else "partner_identifier_exact_match",
                )
            )
        else:
            proposals.append(
                _make_field_proposal(
                    path="buyerRef",
                    value=buyer_ref,
                    proposal=_proposal_like(buyer_ref),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
    if commodity_ref:
        if str(storage_lot_row.get("cropTypeUri") or "").strip() == commodity_ref:
            proposals.append(
                _make_reference_field_proposal(
                    path="commodityRef",
                    value=commodity_ref,
                    capture_id=capture_id,
                    ref_type="crop_type",
                    ref_uri=commodity_ref,
                    confidence=0.95,
                    authority_tier="storage_lot_crop_type_exact_match",
                )
            )
        else:
            proposals.append(
                _make_field_proposal(
                    path="commodityRef",
                    value=commodity_ref,
                    proposal=_proposal_like(commodity_ref),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )

    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    blockers = _delivery_note_payload_blockers(payload)
    return payload, proposals, bindings, blockers


def _soil_report_payload(parse_payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("soilReport", "soilLabReport"):
        value = parse_payload.get(key)
        if isinstance(value, dict):
            return dict(value)
    return {}


def _soil_report_field_proposal(
    parse_payload: dict[str, Any],
    *keys: str,
    preferred: str = "text",
) -> dict[str, Any] | None:
    containers = [_soil_report_payload(parse_payload), parse_payload]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key not in container or container.get(key) is None:
                continue
            proposal = _proposal_like(container.get(key), preferred=preferred)
            if proposal is not None:
                return proposal
    return None


def _soil_report_list_value(parse_payload: dict[str, Any], *keys: str) -> list[str]:
    containers = [_soil_report_payload(parse_payload), parse_payload]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            raw = container.get(key)
            if not isinstance(raw, list):
                continue
            values = [str(item).strip() for item in raw if str(item).strip()]
            if values:
                return values
    return []


def _soil_parameter_entries(parse_payload: dict[str, Any]) -> list[dict[str, Any]]:
    soil_report = _soil_report_payload(parse_payload)
    entries = soil_report.get("parameters")
    normalized_entries: list[dict[str, Any]] = []
    if isinstance(entries, list):
        for row in entries:
            if not isinstance(row, dict):
                continue
            proposals = row.get("proposals") or {}
            parameter_code_proposal = (
                _proposal_from_row(row, "parameterCode")
                or _proposal_like(proposals.get("parameterCode"))
            )
            value_proposal = (
                _proposal_from_row(row, "valueNum", preferred="number")
                or _proposal_from_row(row, "valueText", preferred="number_or_text")
                or _proposal_from_row(row, "value", preferred="number_or_text")
                or _proposal_like(proposals.get("valueNum"), preferred="number")
                or _proposal_like(proposals.get("valueText"), preferred="number_or_text")
                or _proposal_like(proposals.get("value"), preferred="number_or_text")
                or _proposal_like(proposals.get("resultValue"), preferred="number_or_text")
            )
            unit_proposal = _proposal_from_row(row, "unit") or _proposal_like(proposals.get("unit"))
            qualifier_code_proposal = (
                _proposal_from_row(row, "qualifierCode")
                or _proposal_like(proposals.get("qualifierCode"))
            )
            method_code_proposal = (
                _proposal_from_row(row, "methodCode")
                or _proposal_like(proposals.get("methodCode"))
            )
            if not parameter_code_proposal or not value_proposal:
                continue
            normalized_entries.append(
                {
                    "parameterCodeProposal": parameter_code_proposal,
                    "valueProposal": value_proposal,
                    "unitProposal": unit_proposal,
                    "qualifierCodeProposal": qualifier_code_proposal,
                    "methodCodeProposal": method_code_proposal,
                }
            )
    if normalized_entries:
        return normalized_entries

    items = parse_payload.get("items") or []
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            proposals = item.get("proposals") or {}
            parameter_code_proposal = (
                _proposal_from_row(item, "parameterCode")
                or _proposal_like(proposals.get("parameterCode"))
            )
            value_proposal = (
                _proposal_from_row(item, "valueNum", preferred="number")
                or _proposal_from_row(item, "valueText", preferred="number_or_text")
                or _proposal_from_row(item, "value", preferred="number_or_text")
                or _proposal_like(proposals.get("valueNum"), preferred="number")
                or _proposal_like(proposals.get("valueText"), preferred="number_or_text")
                or _proposal_like(proposals.get("value"), preferred="number_or_text")
                or _proposal_like(proposals.get("resultValue"), preferred="number_or_text")
            )
            if not parameter_code_proposal or not value_proposal:
                continue
            normalized_entries.append(
                {
                    "parameterCodeProposal": parameter_code_proposal,
                    "valueProposal": value_proposal,
                    "unitProposal": _proposal_from_row(item, "unit") or _proposal_like(proposals.get("unit")),
                    "qualifierCodeProposal": _proposal_from_row(item, "qualifierCode")
                    or _proposal_like(proposals.get("qualifierCode")),
                    "methodCodeProposal": _proposal_from_row(item, "methodCode")
                    or _proposal_like(proposals.get("methodCode")),
                }
            )
    if normalized_entries:
        return normalized_entries

    default_unit_proposal = _soil_report_field_proposal(parse_payload, "unitText")
    slot_mappings = (
        ("pH", "ph", "pH"),
        ("phosphorus", "phosphorus", None),
        ("potassium", "potassium", None),
        ("organicMatter", "organic_matter", None),
    )
    for source_key, parameter_code, fixed_unit in slot_mappings:
        value_proposal = _soil_report_field_proposal(parse_payload, source_key, preferred="number_or_text")
        if value_proposal is None:
            continue
        normalized_entries.append(
            {
                "parameterCodeProposal": {"valueText": parameter_code},
                "valueProposal": value_proposal,
                "unitProposal": _proposal_like(fixed_unit) if fixed_unit else default_unit_proposal,
                "qualifierCodeProposal": None,
                "methodCodeProposal": None,
            }
        )
    return normalized_entries


def _build_soil_lab_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    resolve_partner_from_exact_identifiers: Callable[..., dict[str, Any] | None] | None = None,
    resolve_field_from_gerk_ref: Callable[[str, str], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")

    field_uri_context = _capture_context_ref(primary_capture, "fieldUri")
    field_uri_proposal = _soil_report_field_proposal(primary_parse_payload, "fieldUri")
    field_uri = field_uri_context or _proposal_value_text(field_uri_proposal)
    sample_date_proposal = _soil_report_field_proposal(primary_parse_payload, "sampleDate", preferred="date")
    lab_name_proposal = _soil_report_field_proposal(primary_parse_payload, "labName")
    laboratory_partner_proposal = _soil_report_field_proposal(
        primary_parse_payload,
        "laboratoryPartnerUri",
        preferred="text",
    )
    laboratory_registration_id_proposal = _soil_report_field_proposal(
        primary_parse_payload,
        "laboratoryRegistrationId",
        preferred="text",
    )
    laboratory_vat_id_proposal = _soil_report_field_proposal(
        primary_parse_payload,
        "laboratoryVatId",
        preferred="text",
    )
    unit_schema_proposal = _soil_report_field_proposal(primary_parse_payload, "unitSchema", preferred="text")
    gerk_ref_proposal = _soil_report_field_proposal(primary_parse_payload, "gerkRef", preferred="text")
    lab_name = _proposal_value_text(lab_name_proposal)
    laboratory_registration_id = _proposal_value_text(laboratory_registration_id_proposal)
    laboratory_vat_id = _proposal_value_text(laboratory_vat_id_proposal)
    review_note_fields = {
        "labName": lab_name,
        "laboratoryRegistrationId": laboratory_registration_id,
        "laboratoryVatId": laboratory_vat_id,
        "sampleId": _proposal_value_text(_soil_report_field_proposal(primary_parse_payload, "sampleId")),
        "sampledParcelText": _proposal_value_text(
            _soil_report_field_proposal(primary_parse_payload, "sampledParcelText")
        ),
        "reportDate": _proposal_value_text(_soil_report_field_proposal(primary_parse_payload, "reportDate", preferred="date")),
        "unitText": _proposal_value_text(_soil_report_field_proposal(primary_parse_payload, "unitText")),
    }
    review_notes = "; ".join(
        f"{key}={value}"
        for key, value in review_note_fields.items()
        if value
    ) or None

    payload_parameters: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    parameter_entries = _soil_parameter_entries(primary_parse_payload)
    for index, entry in enumerate(parameter_entries):
        parameter_code = _proposal_value_text(entry.get("parameterCodeProposal"))
        value_num = _proposal_value_num(entry.get("valueProposal"))
        value_text = _proposal_value_text(entry.get("valueProposal")) if value_num is None else None
        unit = _proposal_value_text(entry.get("unitProposal"))
        qualifier_code = _proposal_value_text(entry.get("qualifierCodeProposal"))
        method_code = _proposal_value_text(entry.get("methodCodeProposal"))
        if not parameter_code or (value_num is None and value_text is None):
            continue
        parameter_payload = {"parameterCode": parameter_code}
        if value_num is not None:
            parameter_payload["valueNum"] = value_num
        if value_text is not None:
            parameter_payload["valueText"] = value_text
        if unit:
            parameter_payload["unit"] = unit
        if qualifier_code:
            parameter_payload["qualifierCode"] = qualifier_code
        if method_code:
            parameter_payload["methodCode"] = method_code
        payload_parameters.append(parameter_payload)
        proposals.append(
            _make_field_proposal(
                path=f"parameters[{index}].parameterCode",
                value=parameter_code,
                proposal=entry.get("parameterCodeProposal"),
                capture_id=capture_id,
            )
        )
        value_path = "valueNum" if value_num is not None else "valueText"
        proposals.append(
            _make_field_proposal(
                path=f"parameters[{index}].{value_path}",
                value=value_num if value_num is not None else value_text,
                proposal=entry.get("valueProposal"),
                capture_id=capture_id,
            )
        )
        if unit:
            proposals.append(
                _make_field_proposal(
                    path=f"parameters[{index}].unit",
                    value=unit,
                    proposal=entry.get("unitProposal"),
                    capture_id=capture_id,
                )
            )
        if qualifier_code:
            proposals.append(
                _make_field_proposal(
                    path=f"parameters[{index}].qualifierCode",
                    value=qualifier_code,
                    proposal=entry.get("qualifierCodeProposal"),
                    capture_id=capture_id,
                )
            )
        if method_code:
            proposals.append(
                _make_field_proposal(
                    path=f"parameters[{index}].methodCode",
                    value=method_code,
                    proposal=entry.get("methodCodeProposal"),
                    capture_id=capture_id,
                )
            )

    payload = {
        "farmUri": farm_uri,
        "fieldUri": field_uri,
        "sampleDate": _proposal_value_text(sample_date_proposal),
        "parameters": payload_parameters,
        "verificationState": "review_required",
        "documentUri": document_uri,
        "parseRunUri": parse_run_uri,
        "linkedSampleUris": _soil_report_list_value(primary_parse_payload, "linkedSampleUris"),
        "linkedAssayUris": _soil_report_list_value(primary_parse_payload, "linkedAssayUris"),
    }
    laboratory_partner_uri = _proposal_value_text(laboratory_partner_proposal)
    laboratory_partner_match = None
    if (
        not laboratory_partner_uri
        and callable(resolve_partner_from_exact_identifiers)
        and (laboratory_registration_id or laboratory_vat_id)
    ):
        laboratory_partner_match = resolve_partner_from_exact_identifiers(
            farm_uri,
            [lab_name] if lab_name else [],
            [laboratory_registration_id] if laboratory_registration_id else [],
            [laboratory_vat_id] if laboratory_vat_id else [],
            role_code=None,
        )
        resolved_laboratory_partner_uri = str((laboratory_partner_match or {}).get("partyUri") or "").strip() or None
        if resolved_laboratory_partner_uri:
            laboratory_partner_uri = resolved_laboratory_partner_uri
    if laboratory_partner_uri:
        payload["laboratoryPartnerUri"] = laboratory_partner_uri
    unit_schema = _proposal_value_text(unit_schema_proposal)
    if unit_schema:
        payload["unitSchema"] = unit_schema
    gerk_ref = _proposal_value_text(gerk_ref_proposal)
    resolved_field_match = (
        resolve_field_from_gerk_ref(farm_uri, gerk_ref)
        if not field_uri and gerk_ref and callable(resolve_field_from_gerk_ref)
        else None
    )
    resolved_field_uri = str((resolved_field_match or {}).get("fieldUri") or "").strip() or None
    if not field_uri and resolved_field_uri:
        field_uri = resolved_field_uri
        payload["fieldUri"] = field_uri
    if gerk_ref:
        payload["gerkRef"] = gerk_ref
    if review_notes:
        payload["reviewNotes"] = review_notes
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value != "" and (not isinstance(value, list) or value)
    }

    if field_uri:
        if field_uri_context:
            proposals.append(
                _make_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    proposal=_proposal_like(field_uri),
                    capture_id=capture_id,
                    authority_tier="capture_context",
                )
            )
        elif _proposal_value_text(field_uri_proposal):
            proposals.append(
                _make_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    proposal=field_uri_proposal,
                    capture_id=capture_id,
                )
            )
        elif resolved_field_uri:
            proposals.append(
                _make_reference_field_proposal(
                    path="fieldUri",
                    value=field_uri,
                    capture_id=capture_id,
                    ref_type="field",
                    ref_uri=field_uri,
                    confidence=0.99,
                    authority_tier="field_authority_exact_match",
                )
            )
    if payload.get("sampleDate"):
        proposals.append(
            _make_field_proposal(
                path="sampleDate",
                value=payload["sampleDate"],
                proposal=sample_date_proposal,
                capture_id=capture_id,
            )
        )
    if laboratory_partner_uri:
        if laboratory_partner_match and str((laboratory_partner_match or {}).get("partyUri") or "").strip() == laboratory_partner_uri:
            laboratory_partner_match_kind = str((laboratory_partner_match or {}).get("matchKind") or "").strip()
            proposals.append(
                _make_reference_field_proposal(
                    path="laboratoryPartnerUri",
                    value=laboratory_partner_uri,
                    capture_id=capture_id,
                    ref_type="party",
                    ref_uri=laboratory_partner_uri,
                    confidence=0.99 if laboratory_partner_match_kind == "partner_identifier_and_label_exact" else 0.95,
                    authority_tier=(
                        f"{laboratory_partner_match_kind}_match"
                        if laboratory_partner_match_kind
                        else "partner_identifier_exact_match"
                    ),
                )
            )
        else:
            proposals.append(
                _make_field_proposal(
                    path="laboratoryPartnerUri",
                    value=laboratory_partner_uri,
                    proposal=laboratory_partner_proposal,
                    capture_id=capture_id,
                )
            )
    if unit_schema:
        proposals.append(
            _make_field_proposal(
                path="unitSchema",
                value=unit_schema,
                proposal=unit_schema_proposal,
                capture_id=capture_id,
            )
        )
    if gerk_ref:
        proposals.append(
            _make_field_proposal(
                path="gerkRef",
                value=gerk_ref,
                proposal=gerk_ref_proposal,
                capture_id=capture_id,
            )
        )

    blockers: list[str] = []
    if not field_uri:
        blockers.append("missing_field_uri")
    if not payload.get("sampleDate"):
        blockers.append("missing_sample_date")
    if not payload_parameters:
        blockers.append("missing_parameters")
    return payload, proposals, bindings, blockers


def _build_receipt_payload_and_proposals(
    *,
    farm_uri: str,
    primary_capture: dict[str, Any],
    primary_parse_payload: dict[str, Any],
    label_captures: Sequence[tuple[dict[str, Any], dict[str, Any]]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    def _merge_label_item_into_receipt_line(
        *,
        target_line_item: dict[str, Any],
        proposals_out: list[dict[str, Any]],
        label_item: dict[str, Any],
        capture_id_for_label: str,
    ) -> None:
        label_proposals = label_item.get("proposals") or {}
        for proposal_key, target_key in (
            ("variety", "variety"),
            ("statusCode", "statusCode"),
            ("lotCode", "lotLabel"),
        ):
            value = _proposal_value_text(label_proposals.get(proposal_key))
            if not value or target_line_item.get(target_key):
                continue
            target_line_item[target_key] = value
            proposals_out.append(
                _make_field_proposal(
                    path=f"lineItems[0].{target_key}",
                    value=value,
                    proposal=label_proposals.get(proposal_key),
                    capture_id=capture_id_for_label,
                )
            )

    capture_id = str(primary_capture.get("captureId") or "")
    document_uri = _capture_ref(primary_capture, "documentUri")
    parse_run_uri = _capture_ref(primary_capture, "parseRunUri")
    receipt = primary_parse_payload.get("receipt") or {}
    items = [dict(item or {}) for item in (primary_parse_payload.get("items") or [])]
    receipt_items = [
        item for item in items if str(item.get("itemType") or "receipt_line_item").strip() != "label_lot"
    ]
    embedded_label_items = [
        item for item in items if str(item.get("itemType") or "receipt_line_item").strip() == "label_lot"
    ]
    items_for_lines = receipt_items or items
    line_items: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = [
        {
            "captureId": capture_id,
            "subjectPath": "$",
            "role": "source_document",
            "retentionClass": "compliance_record",
            "notes": None,
        }
    ]
    for index, item in enumerate(items_for_lines):
        item_proposals = item.get("proposals") or {}
        resource_label = _proposal_value_text(item_proposals.get("productLabel")) or str(item.get("rawText") or "").strip()
        quantity_proposal = item_proposals.get("quantity") or item_proposals.get("packQuantity") or {}
        quantity_value = _proposal_value_num(quantity_proposal)
        quantity_unit = str(quantity_proposal.get("unit") or "").strip() or None
        line_item = {
            "rawText": str(item.get("rawText") or "").strip(),
            "resourceLabel": resource_label,
            "categoryHint": str(item.get("categoryHint") or "other").strip() or "other",
            "cropLabel": _proposal_value_text(item_proposals.get("cropLabel")),
            "variety": _proposal_value_text(item_proposals.get("variety")),
            "statusCode": _proposal_value_text(item_proposals.get("statusCode")),
            "lotLabel": _proposal_value_text(item_proposals.get("lotCode")),
            "quantityValue": quantity_value,
            "quantityUnit": quantity_unit,
        }
        line_item = {key: value for key, value in line_item.items() if value is not None or key in {"rawText", "resourceLabel", "categoryHint"}}
        line_items.append(line_item)
        proposals.append(
            _make_field_proposal(
                path=f"lineItems[{index}].resourceLabel",
                value=resource_label,
                proposal=item_proposals.get("productLabel"),
                capture_id=capture_id,
            )
        )
        if quantity_value is not None:
            proposals.append(
                _make_field_proposal(
                    path=f"lineItems[{index}].quantityValue",
                    value=quantity_value,
                    proposal=quantity_proposal,
                    capture_id=capture_id,
                )
            )
        if quantity_unit:
            proposals.append(
                _make_field_proposal(
                    path=f"lineItems[{index}].quantityUnit",
                    value=quantity_unit,
                    proposal=quantity_proposal,
                    capture_id=capture_id,
                )
            )
        for proposal_key, target_path in (
            ("cropLabel", f"lineItems[{index}].cropLabel"),
            ("variety", f"lineItems[{index}].variety"),
            ("statusCode", f"lineItems[{index}].statusCode"),
            ("lotCode", f"lineItems[{index}].lotLabel"),
        ):
            proposal_value = _proposal_value_text(item_proposals.get(proposal_key))
            if proposal_value:
                proposals.append(
                    _make_field_proposal(
                        path=target_path,
                        value=proposal_value,
                        proposal=item_proposals.get(proposal_key),
                        capture_id=capture_id,
                    )
                )

    if len(line_items) == 1 and receipt_items:
        for label_item in embedded_label_items:
            _merge_label_item_into_receipt_line(
                target_line_item=line_items[0],
                proposals_out=proposals,
                label_item=label_item,
                capture_id_for_label=capture_id,
            )

    if len(line_items) == 1:
        for label_capture, label_parse_payload in label_captures:
            label_items = label_parse_payload.get("items") or []
            if not label_items:
                continue
            label_item = dict(label_items[0] or {})
            label_capture_id = str(label_capture.get("captureId") or "")
            _merge_label_item_into_receipt_line(
                target_line_item=line_items[0],
                proposals_out=proposals,
                label_item=label_item,
                capture_id_for_label=label_capture_id,
            )
            bindings.append(
                {
                    "captureId": label_capture_id,
                    "subjectPath": "lineItems[0]",
                    "role": "supporting_label",
                    "retentionClass": "compliance_record",
                    "notes": "Linked through receipt_plus_label_link helper.",
                }
            )

    receipt_ref = _proposal_value_text(receipt.get("receiptRef")) or _tail_token(document_uri or parse_run_uri or capture_id)
    payload = {
        "farmUri": farm_uri,
        "receiptRef": receipt_ref,
        "source": str(primary_capture.get("source") or primary_capture.get("modality") or "intake").strip() or "intake",
        "vendorName": _proposal_value_text(receipt.get("vendorName")),
        "vendorAddress": None,
        "purchaseDate": _proposal_value_text(receipt.get("purchaseDate")),
        "documentUri": document_uri,
        "parseRunUri": parse_run_uri,
        "lineItems": line_items,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    proposals.append(
        _make_field_proposal(
            path="receiptRef",
            value=receipt_ref,
            proposal=receipt.get("receiptRef"),
            capture_id=capture_id,
            authority_tier="deterministic_decode" if receipt_ref == _tail_token(document_uri or parse_run_uri or capture_id) else "ocr_exact",
        )
    )
    if payload.get("vendorName"):
        proposals.append(
            _make_field_proposal(
                path="vendorName",
                value=payload["vendorName"],
                proposal=receipt.get("vendorName"),
                capture_id=capture_id,
            )
        )
    if payload.get("purchaseDate"):
        proposals.append(
            _make_field_proposal(
                path="purchaseDate",
                value=payload["purchaseDate"],
                proposal=receipt.get("purchaseDate"),
                capture_id=capture_id,
            )
        )
    blockers: list[str] = []
    if not line_items:
        blockers.append("missing_line_items")
    return payload, proposals, bindings, blockers


def analyze_capture_session(
    *,
    farm_uri: str,
    captures: Sequence[dict[str, Any]],
    parse_runs_by_capture_id: dict[str, dict[str, Any]],
    route_items: Sequence[dict[str, Any]],
    resolve_fertilizer_input_material_resource: Callable[[str, Sequence[str], Sequence[str]], dict[str, Any] | None]
    | None = None,
    resolve_document_evidence_uri: Callable[[str], str | None] | None = None,
    resolve_partner_from_exact_identifiers: Callable[..., dict[str, Any] | None] | None = None,
    resolve_storage_lot_from_lot_code: Callable[[str, Sequence[str]], dict[str, Any] | None] | None = None,
    resolve_field_from_gerk_ref: Callable[[str, str], dict[str, Any] | None] | None = None,
    resolve_crop_instance_from_field_declaration: Callable[..., dict[str, Any] | None] | None = None,
    resolve_crop_type_from_exact_label: Callable[[str], dict[str, Any] | None] | None = None,
    resolve_variety_from_exact_label: Callable[[str, str], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    candidates = route_candidates_for_session(
        captures,
        parse_runs_by_capture_id=parse_runs_by_capture_id,
        route_items=route_items,
    )
    selected_route_id, helper_ids = select_route_and_helpers(candidates)
    route_by_id = {str(item.get("routeId")): item for item in route_items}
    selected_route = route_by_id.get(selected_route_id) or route_by_id.get("unknown.review") or {}
    field_proposals: list[dict[str, Any]] = []
    evidence_bindings: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []
    payload_draft: dict[str, Any] | None = None
    source_capture_ids: list[str] = []

    if selected_route_id == "receipt.invoice":
        primary_capture = None
        primary_parse_payload: dict[str, Any] = {}
        supporting_labels: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_receipt_route(capture, parse_payload)
            if score > 0 and primary_capture is None:
                primary_capture = capture
                primary_parse_payload = parse_payload
                continue
            label_score, _ = _score_seed_label_route(capture, parse_payload)
            if label_score >= 0.7:
                supporting_labels.append((capture, parse_payload))
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or "")))
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_receipt_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                label_captures=supporting_labels,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
            source_capture_ids.extend(str(capture.get("captureId") or "") for capture, _ in supporting_labels)
    elif selected_route_id == "seed_label_or_tag":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_seed_label_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_seed_label_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_input_material_resource=resolve_fertilizer_input_material_resource,
                resolve_document_evidence_uri=resolve_document_evidence_uri,
                resolve_crop_type_from_exact_label=resolve_crop_type_from_exact_label,
                resolve_variety_from_exact_label=resolve_variety_from_exact_label,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "fertilizer_label":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_fertilizer_label_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_fertilizer_label_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_input_material_resource=resolve_fertilizer_input_material_resource,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "seed_authorization_or_derogation":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_seed_authorization_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_seed_authorization_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_field_from_gerk_ref=resolve_field_from_gerk_ref,
                resolve_crop_type_from_exact_label=resolve_crop_type_from_exact_label,
                resolve_variety_from_exact_label=resolve_variety_from_exact_label,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "delivery_note":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_delivery_note_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_delivery_note_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_partner_from_exact_identifiers=resolve_partner_from_exact_identifiers,
                resolve_storage_lot_from_lot_code=resolve_storage_lot_from_lot_code,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "storage_lot_label":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_storage_lot_label_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_storage_lot_label_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_storage_lot_from_lot_code=resolve_storage_lot_from_lot_code,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "soil_analysis_report":
        primary_capture = None
        primary_parse_payload = {}
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_soil_report_route(capture, parse_payload)
            if score > 0:
                primary_capture = capture
                primary_parse_payload = parse_payload
                break
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_soil_lab_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_partner_from_exact_identifiers=resolve_partner_from_exact_identifiers,
                resolve_field_from_gerk_ref=resolve_field_from_gerk_ref,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif selected_route_id == "fertilization_plan":
        primary_capture = None
        primary_parse_payload = {}
        best_score = 0.0
        for capture in captures:
            capture_id = str(capture.get("captureId") or "")
            parse_payload = _parse_response_payload(parse_runs_by_capture_id.get(capture_id))
            score, _ = _score_fertilization_plan_route(capture, parse_payload)
            if score <= 0 or score < best_score:
                continue
            best_score = score
            primary_capture = capture
            primary_parse_payload = parse_payload
        if primary_capture is None and captures:
            primary_capture = captures[0]
            primary_parse_payload = _parse_response_payload(
                parse_runs_by_capture_id.get(str(primary_capture.get("captureId") or ""))
            )
        if primary_capture is not None:
            payload_draft, field_proposals, evidence_bindings, blocking_reasons = _build_fertilization_plan_payload_and_proposals(
                farm_uri=farm_uri,
                primary_capture=primary_capture,
                primary_parse_payload=primary_parse_payload,
                resolve_field_from_gerk_ref=resolve_field_from_gerk_ref,
                resolve_crop_instance_from_field_declaration=resolve_crop_instance_from_field_declaration,
            )
            source_capture_ids = [str(primary_capture.get("captureId") or "")]
    elif captures:
        source_capture_ids = [str(captures[0].get("captureId") or "")]
        evidence_bindings = [
            {
                "captureId": source_capture_ids[0],
                "subjectPath": "$",
                "role": "source_document",
                "retentionClass": "compliance_record",
                "notes": None,
            }
        ]

    commit_plan = {
        "routeId": selected_route_id,
        "targetKind": ((selected_route.get("targetForm") or {}).get("kind")) or "review",
        "targetId": ((selected_route.get("targetForm") or {}).get("id")) or "manual.intake.review.v1",
        "payloadDraft": payload_draft,
        "blockingReasonCodes": blocking_reasons,
        "evidenceBindings": evidence_bindings,
        "helperIds": helper_ids,
        "sourceCaptureIds": source_capture_ids,
    }
    status = "awaiting_review"
    if not captures:
        status = "awaiting_capture"
    elif selected_route_id == "unknown.review":
        status = "awaiting_review"
    analysis_summary = {
        "selectedRouteId": selected_route_id,
        "selectedHelperIds": helper_ids,
        "candidateCount": len(candidates),
        "primarySourceCaptureIds": source_capture_ids,
    }
    return {
        "status": status,
        "selectedRouteId": selected_route_id,
        "selectedHelperIds": helper_ids,
        "routeCandidates": candidates,
        "fieldProposals": field_proposals,
        "evidenceBindings": evidence_bindings,
        "reviewDecisions": [],
        "commitPlan": commit_plan,
        "analysisSummary": analysis_summary,
    }


def blocking_reason_codes_for_route(route_id: str, payload_draft: dict[str, Any] | None) -> list[str]:
    if route_id == "unknown.review":
        return ["manual_review_only"]
    if route_id == "seed_label_or_tag":
        return _seed_label_payload_blockers(payload_draft or {})
    if route_id == "storage_lot_label":
        return _storage_lot_label_payload_blockers(payload_draft or {})
    if route_id == "fertilizer_label":
        return _fertilizer_payload_blockers(payload_draft or {})
    if route_id == "seed_authorization_or_derogation":
        return _seed_authorization_payload_blockers(payload_draft or {})
    if route_id == "fertilization_plan":
        return _fertilization_plan_payload_blockers(payload_draft or {})
    if route_id == "delivery_note":
        return _delivery_note_payload_blockers(payload_draft or {})
    if route_id == "soil_analysis_report":
        payload = dict(payload_draft or {})
        blockers: list[str] = []
        if not str(payload.get("fieldUri") or "").strip():
            blockers.append("missing_field_uri")
        if not str(payload.get("sampleDate") or "").strip():
            blockers.append("missing_sample_date")
        parameters = payload.get("parameters") or []
        if not isinstance(parameters, list) or not parameters:
            blockers.append("missing_parameters")
        return blockers
    if route_id != "receipt.invoice":
        return ["route_not_commit_ready"]
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("receiptRef") or "").strip():
        blockers.append("missing_receipt_ref")
    line_items = payload.get("lineItems") or []
    if not isinstance(line_items, list) or not line_items:
        blockers.append("missing_line_items")
    return blockers


def _fertilizer_payload_blockers(payload_draft: dict[str, Any]) -> list[str]:
    payload = dict(payload_draft or {})
    blockers: list[str] = []
    if not str(payload.get("productLabel") or "").strip():
        blockers.append("missing_product_label")
    declared_nutrients = payload.get("declaredNutrients") or []
    if not isinstance(declared_nutrients, list) or not declared_nutrients:
        blockers.append("missing_declared_nutrients")
    else:
        incomplete = False
        for item in declared_nutrients:
            if not isinstance(item, dict):
                incomplete = True
                break
            if not str(item.get("nutrientCode") or "").strip():
                incomplete = True
                break
            if item.get("value") is None or str(item.get("value")).strip() == "":
                incomplete = True
                break
            if not str(item.get("unit") or "").strip():
                incomplete = True
                break
        if incomplete:
            blockers.append("incomplete_declared_nutrients")
    density_value_present = payload.get("densityValue") is not None
    density_unit = str(payload.get("densityUnit") or "").strip()
    if density_value_present != bool(density_unit):
        blockers.append("invalid_density_pair")
    return blockers
