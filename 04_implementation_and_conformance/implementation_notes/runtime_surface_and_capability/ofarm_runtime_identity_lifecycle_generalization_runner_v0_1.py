#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMP = ROOT / "04_implementation_and_conformance"
SCHEMA = MC / "OFARM_IdentityLifecycleChange_schema_v0_1.json"
SUPPORT_RESULTS = IMP / "OFARM_runtime_identity_lifecycle_expansion_results_v0_1.json"
MAT_RESULT = MC / "OFARM_MaterializationResult_example_field_split_submission_invalid_v0_1.json"
OUT = IMP / "OFARM_runtime_identity_lifecycle_generalization_results_v0_1.json"

EXAMPLES = sorted(MC.glob("OFARM_IdentityLifecycleChange_example_*_v0_1.json"))

REQUIRED_FAMILIES = {
    "FIELD",
    "ZONE",
    "CROP_CYCLE",
    "EQUIPMENT",
    "FACILITY",
    "STORAGE_LOCATION",
    "CONTAINER",
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    schema = load_json(SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)

    validated = []
    families = set()
    change_kinds = set()
    continuity_outcomes = set()
    no_mint_present = False
    invalidation_link_present = False

    for path in EXAMPLES:
        obj = load_json(path)
        jsonschema.validate(obj, schema)
        families.add(obj["subjectFamily"])
        change_kinds.add(obj["changeKind"])
        continuity_outcomes.add(obj["continuityOutcome"])
        if obj["continuityOutcome"] == "NOT_CONSTITUTIONAL_IDENTITY":
            no_mint_present = True
        lineage_needed = obj["changeKind"] in {"SPLIT", "MERGE", "REPLACEMENT", "REPLANT", "REVISION"} or obj["continuityOutcome"] in {
            "NEW_IDENTITIES_WITH_SPLIT_FROM",
            "NEW_IDENTITY_REPLACES",
            "NEW_IDENTITY_SUCCEEDS",
            "SAME_IDENTITY_NEW_REVISION",
        }
        validated.append({
            "exampleFile": path.name,
            "subjectFamily": obj["subjectFamily"],
            "changeKind": obj["changeKind"],
            "continuityOutcome": obj["continuityOutcome"],
            "hasAnchorScopes": bool(obj["anchorScopes"]),
            "lineageRequiredWhenExpected": bool(obj["lineageRelations"]) if lineage_needed else True,
            "hasInvalidationImpacts": bool(obj["invalidationImpacts"]),
            "checksPass": True
        })

    mat = load_json(MAT_RESULT)
    related_refs = []
    for problem in mat.get("problems", []):
        related_refs.extend(problem.get("relatedRefs", []))
    invalidation_link_present = (
        mat["decisionOutcome"] == "REFUSE_USE"
        and mat["freshnessState"] == "INVALID"
        and "IDENTITY_LIFECYCLE" in mat["invalidationTriggerFamilies"]
        and "idlife:field-17:split:2026-04-18" in related_refs
    )

    support = load_json(SUPPORT_RESULTS)
    support_seed_still_passing = support.get("overall") == "PASS_WITH_LIMITATIONS"

    summary = {
        "examplesValidated": len(validated),
        "subjectFamiliesCovered": sorted(families),
        "requiredSubjectFamiliesCovered": sorted(REQUIRED_FAMILIES),
        "requiredFamilyCoveragePass": REQUIRED_FAMILIES.issubset(families),
        "changeKindsCovered": sorted(change_kinds),
        "continuityOutcomesCovered": sorted(continuity_outcomes),
        "explicitNoMintOutcomePresent": no_mint_present,
        "fieldSplitInvalidationLinkPresent": invalidation_link_present,
        "supportSeedStillPassing": support_seed_still_passing
    }

    overall_pass = (
        all(v["checksPass"] and v["hasAnchorScopes"] and v["hasInvalidationImpacts"] and v["lineageRequiredWhenExpected"] for v in validated)
        and summary["requiredFamilyCoveragePass"]
        and no_mint_present
        and invalidation_link_present
        and support_seed_still_passing
    )

    results = {
        "generatedAt": "2026-04-19T10:15:00Z",
        "overall": "PASS_WITH_LIMITATIONS" if overall_pass else "FAIL",
        "summary": summary,
        "validations": validated,
        "limitations": [
            "This wave promotes a minimal generic contract and starter examples only.",
            "Lot-specific lineage still remains specialized under OFARM_LotLineageChange_schema_v0_1.json.",
            "The support seed remains package-local proof rather than deployment-collected lifecycle telemetry."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if overall_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
