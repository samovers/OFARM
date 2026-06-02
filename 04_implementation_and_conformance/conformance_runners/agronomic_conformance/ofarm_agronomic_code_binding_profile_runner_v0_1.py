#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_agronomic_code_binding_profile_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_code_binding_profile_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def must_fail_validation(instance: dict[str, Any], schema: dict[str, Any], check_id: str) -> str:
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError:
        return "PASS"
    raise AssertionError(f"{check_id} unexpectedly validated")


def main() -> int:
    records = load_json(RECORDS)
    id_schema = load_json(MC / "OFARM_AgronomicIdentityBinding_schema_v0_1.json")
    profile_schema = load_json(MC / "OFARM_AgronomicCodeBindingProfile_schema_v0_1.json")
    jsonschema.Draft202012Validator.check_schema(id_schema)
    jsonschema.Draft202012Validator.check_schema(profile_schema)

    example_results: dict[str, str] = {}
    examples: dict[str, dict[str, Any]] = {}
    for name in records["positiveExamples"]:
        data = load_json(MC / name)
        schema = profile_schema if name.startswith("OFARM_AgronomicCodeBindingProfile") else id_schema
        jsonschema.validate(data, schema)
        example_results[name] = "PASS"
        examples[name] = data

    profile = examples["OFARM_AgronomicCodeBindingProfile_example_si_crop_protection_core_v0_1.json"]
    maize = examples["OFARM_AgronomicIdentityBinding_example_maize_crop_species_eppo_v0_1.json"]
    unresolved_product = examples["OFARM_AgronomicIdentityBinding_example_crop_protection_product_marketing_name_unresolved_v0_1.json"]
    product = examples["OFARM_AgronomicIdentityBinding_example_crop_protection_product_si_authorisation_v0_1.json"]
    rate = examples["OFARM_AgronomicIdentityBinding_example_application_rate_qudt_ucum_v0_1.json"]
    threshold = examples["OFARM_AgronomicIdentityBinding_example_advisory_threshold_source_v0_1.json"]

    negative_results: dict[str, str] = {}

    # Verified identity cannot be identifier-empty.
    mutated = copy.deepcopy(maize)
    mutated["bindingValue"].pop("code", None)
    negative_results["NEG-ID-001"] = must_fail_validation(mutated, id_schema, "NEG-ID-001")

    # Ambiguous binding cannot allow high-consequence use.
    mutated = copy.deepcopy(unresolved_product)
    mutated["promotionBoundary"]["highConsequenceUse"] = "ALLOWED_WHEN_PROFILE_AND_EVIDENCE_PASS"
    negative_results["NEG-ID-002"] = must_fail_validation(mutated, id_schema, "NEG-ID-002")

    # Profile cannot disable quantity-kind + unit-code requirement.
    mutated = copy.deepcopy(profile)
    mutated["quantityAndUnitPolicy"]["requireQuantityKindAndUnitCode"] = False
    negative_results["NEG-PROFILE-001"] = must_fail_validation(mutated, profile_schema, "NEG-PROFILE-001")

    # Binding requirements cannot omit unresolved behavior.
    mutated = copy.deepcopy(profile)
    mutated["bindingRequirements"][0].pop("unresolvedBehavior", None)
    negative_results["NEG-PROFILE-002"] = must_fail_validation(mutated, profile_schema, "NEG-PROFILE-002")

    behavior_checks: dict[str, bool] = {}
    roles_by_ref = {entry["standardRef"]: entry["role"] for entry in profile["standardRoleMap"]}
    behavior_checks["external_standards_not_ofarm_law"] = profile["normativePosture"]["externalStandardsPosture"] == "ANCHORS_AND_BINDINGS_NOT_OFARM_LAW"
    behavior_checks["pack_constrains_bindings_only"] = profile["normativePosture"]["packMutationRule"] == "PACKS_CONSTRAIN_BINDINGS_ONLY"
    behavior_checks["free_text_is_evidence"] = profile["normativePosture"]["freeTextIdentityRule"] == "FREE_TEXT_IS_EVIDENCE_NOT_ACCEPTED_IDENTITY"
    behavior_checks["role_map_has_core_code_bindings"] = all(roles_by_ref.get(ref) == "CODE_BINDING" for ref in ["eppo-codes", "bbch", "ucum"])
    behavior_checks["role_map_has_quantity_anchor"] = roles_by_ref.get("qudt") == "SEMANTIC_ANCHOR"
    behavior_checks["role_map_has_ppp_runtime_surface"] = roles_by_ref.get("registry:si:crop-protection-products") == "RUNTIME_SURFACE"
    behavior_checks["role_map_has_seed_attestation_wrapper"] = roles_by_ref.get("oecd-seed-schemes") == "ATTESTATION_WRAPPER"
    behavior_checks["quantity_policy_requires_kind_and_unit"] = profile["quantityAndUnitPolicy"]["requireQuantityKindAndUnitCode"] is True and profile["quantityAndUnitPolicy"]["preserveOriginalLexicalValueAndUnit"] is True
    behavior_checks["ppp_product_has_jurisdiction_authorisation_not_gtin_only"] = bool(product["externalScheme"].get("jurisdiction")) and bool(product["bindingValue"].get("authorisationRef")) and bool(product["bindingValue"].get("gtin"))
    behavior_checks["marketing_only_product_blocks_high_consequence"] = unresolved_product["bindingState"] == "AMBIGUOUS" and unresolved_product["promotionBoundary"]["highConsequenceUse"] == "BLOCKED_OR_REVIEW_REQUIRED" and unresolved_product["promotionBoundary"]["maySupportPromotion"] is False
    behavior_checks["quantity_binding_has_qudt_and_ucum"] = rate["bindingValue"].get("quantityKindRef") == "qudt:VolumePerArea" and rate["bindingValue"].get("unitRef") == "ucum:L.ha-1"
    behavior_checks["threshold_is_source_bound"] = bool(threshold["bindingValue"].get("sourceDocumentRef")) and bool(threshold["bindingValue"].get("effectivePeriod")) and bool(threshold["bindingValue"].get("thresholdSourceRefs"))
    behavior_checks["pack_merge_fails_closed"] = profile["packMergePolicy"]["conflictDisposition"] in {"FAIL_CLOSED", "REQUIRE_GOVERNED_REVIEW"}

    for key, value in behavior_checks.items():
        expect(value, f"behavior check failed: {key}")

    results = {
        "schemaVersion": "ofarm.agronomicCodeBindingProfileResults.v0.1",
        "date": "2026-05-13",
        "phase": "AGR-P5",
        "recordSetId": records.get("recordSetId"),
        "overallStatus": "PASS",
        "schemaChecks": {
            "OFARM_AgronomicIdentityBinding_schema_v0_1.json": "PASS",
            "OFARM_AgronomicCodeBindingProfile_schema_v0_1.json": "PASS"
        },
        "positiveExampleValidation": example_results,
        "negativeValidation": negative_results,
        "behaviorChecks": behavior_checks,
        "coverageAdvances": [
            "adds a governed code-binding profile without importing external standards as OFARM law",
            "blocks marketing-only product identity from compliance-grade promotion",
            "requires quantity kind and unit code for high-consequence quantity semantics",
            "keeps pack merge behavior fail-closed or review-bound"
        ],
        "limitations": [
            "This runner validates code-binding/profile closure only; query/output reconstruction is still pending.",
            "Baseline text is not edited by Phase AGR-P5."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
