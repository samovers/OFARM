#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_external_code_binding_currentness_records_v0_1.json"
OUT = IMPL / "OFARM_external_code_binding_currentness_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def schema_for(filename: str) -> str:
    prefix = filename.split("_example_")[0]
    return f"{prefix}_schema_v0_1.json"


def main() -> int:
    records = load_json(RECORDS)
    schema_checks: dict[str, str] = {}
    example_results: dict[str, str] = {}
    schemas: dict[str, Any] = {}

    all_examples = records["positiveExamples"] + records["negativePostureExamples"]
    for name in all_examples:
        schema_name = schema_for(name)
        if schema_name not in schemas:
            schema = load_json(MC / schema_name)
            jsonschema.Draft202012Validator.check_schema(schema)
            schemas[schema_name] = schema
            schema_checks[schema_name] = "PASS"
        jsonschema.validate(load_json(MC / name), schemas[schema_name])
        example_results[name] = "PASS"

    profile = load_json(MC / "OFARM_AgronomicCodeBindingProfile_example_be_crop_protection_authorisation_currentness_v0_1.json")
    profile_roles = {r["standardRef"]: r for r in profile["standardRoleMap"]}
    profile_reqs = {r["bindingRole"]: r for r in profile["bindingRequirements"]}
    pass_trace = load_json(MC / "OFARM_ExternalRegistryVerificationTrace_example_be_phytoweb_authorisation_pass_v0_1.json")
    gtin_trace = load_json(MC / "OFARM_ExternalRegistryVerificationTrace_example_be_gtin_only_review_required_v0_1.json")
    eu_trace = load_json(MC / "OFARM_ExternalRegistryVerificationTrace_example_be_eu_active_substance_only_refuse_output_v0_1.json")
    unavailable_trace = load_json(MC / "OFARM_ExternalRegistryVerificationTrace_example_be_registry_unavailable_refuse_output_v0_1.json")
    verified_binding = load_json(MC / "OFARM_AgronomicIdentityBinding_example_crop_protection_product_be_authorisation_verified_v0_1.json")
    gtin_binding = load_json(MC / "OFARM_AgronomicIdentityBinding_example_crop_protection_product_be_gtin_only_review_required_v0_1.json")
    eu_binding = load_json(MC / "OFARM_AgronomicIdentityBinding_example_crop_protection_product_be_eu_active_substance_only_review_required_v0_1.json")

    behavior: dict[str, bool] = {}
    behavior["profile_is_be_crop_protection"] = profile["profileScope"]["jurisdiction"] == "BE" and profile["profileScope"]["profileDomain"] == "CROP_PROTECTION"
    behavior["phytoweb_is_mandatory_runtime_surface"] = profile_roles["registry:be:phytoweb-authorisations"]["role"] == "RUNTIME_SURFACE" and profile_roles["registry:be:phytoweb-authorisations"]["status"] == "PREFERRED"
    behavior["eu_pesticides_not_product_authorisation_replacement"] = profile_roles["eu-pesticides-database"]["role"] == "SEMANTIC_ANCHOR" and profile_roles["eu-pesticides-database"]["status"] == "ALLOWED"
    behavior["gtin_is_exchange_mapping_not_regulatory_key"] = profile_roles["gs1-gtin"]["role"] == "EXCHANGE_MAPPING"
    behavior["ppp_authorisation_requires_jurisdiction_snapshot_evidence"] = all(profile_reqs["CROP_PROTECTION_PRODUCT"].get(k) is True for k in ["requiresJurisdiction", "requiresEvidence", "requiresReferenceSnapshot"])
    behavior["ppp_authorisation_blocks_unresolved_promotion"] = profile_reqs["CROP_PROTECTION_PRODUCT"]["unresolvedBehavior"] == "BLOCK_PROMOTION"
    behavior["verified_binding_uses_authorisation_ref"] = bool(verified_binding["bindingValue"].get("authorisationRef")) and verified_binding["externalScheme"]["jurisdiction"] == "BE"
    behavior["verified_binding_has_trace_and_snapshots"] = bool(verified_binding.get("evidenceRefs")) and len(verified_binding.get("referenceSnapshotRefs", [])) >= 2
    behavior["gtin_binding_blocks_high_consequence"] = gtin_binding["bindingState"] == "AMBIGUOUS" and gtin_binding["promotionBoundary"]["highConsequenceUse"] == "BLOCKED_OR_REVIEW_REQUIRED"
    behavior["eu_only_binding_blocks_high_consequence"] = eu_binding["bindingState"] == "PROVISIONAL" and eu_binding["promotionBoundary"]["maySupportPromotion"] is False
    behavior["pass_trace_requires_authorisation_number"] = pass_trace["selectedExternalId"]["externalIdRole"] == "AUTHORISATION_NUMBER" and pass_trace["candidateCount"] == 1
    behavior["pass_trace_has_label_certificate_when_required"] = pass_trace["labelCertificateCorrelated"]["requiredForHighConsequence"] is True and pass_trace["labelCertificateCorrelated"]["correlationStatus"] == "CORRELATED"
    behavior["pass_trace_allows_passport"] = pass_trace["finalOutcome"] == "PASS" and pass_trace["downstreamOutputDisposition"] == "PASSPORTVIEW_ALLOWED"
    behavior["gtin_only_requires_review"] = gtin_trace["finalOutcome"] == "REVIEW_REQUIRED" and gtin_trace["highConsequenceUse"] == "REQUIRE_REVIEW"
    behavior["eu_only_refuses_output"] = eu_trace["finalOutcome"] == "REFUSE_OUTPUT" and eu_trace["highConsequenceUse"] == "REFUSE_OUTPUT"
    behavior["registry_unavailable_refuses_passport_allows_annex"] = unavailable_trace["finalOutcome"] == "UNVERIFIED_DUE_TO_SOURCE_UNAVAILABLE" and unavailable_trace["downstreamOutputDisposition"] == "PASSPORTVIEW_REFUSED_DOCUMENTANNEX_ALLOWED"

    for key, value in behavior.items():
        expect(value, f"behavior check failed: {key}")

    fail_closed_results = {}
    expected = {
        "free_text_product_name_only": "REVIEW_REQUIRED_OR_REFUSE_OUTPUT",
        "gtin_only": "REVIEW_REQUIRED",
        "eu_active_substance_only": "REFUSE_OUTPUT",
        "stale_or_missing_accessedAt": "REVIEW_REQUIRED_OR_REFUSE_OUTPUT",
        "wrong_jurisdiction": "FAIL_CLOSED",
        "missing_reference_snapshot": "FAIL_CLOSED",
        "registry_unavailable": "REFUSE_OUTPUT_DOCUMENTANNEX_ALLOWED",
        "prescription_as_applied_identity_mismatch": "REVIEW_REQUIRED",
    }
    for case in records["failClosedRules"]:
        fail_closed_results[case["caseId"]] = "PASS" if case["expectedDisposition"] == expected[case["condition"]] else "FAIL"
    expect(all(v == "PASS" for v in fail_closed_results.values()), "fail-closed rule mismatch")

    result = {
        "schemaVersion": "ofarm.externalCodeBindingCurrentnessResults.v0.1",
        "date": "2026-05-14",
        "phase": "ONT-SEMINT Phase 4",
        "recordSetId": records.get("recordSetId"),
        "overallStatus": "PASS",
        "schemaChecks": schema_checks,
        "exampleValidation": example_results,
        "behaviorChecks": behavior,
        "failClosedRuleChecks": fail_closed_results,
        "coverageAdvances": [
            "adds a narrow Belgium/Phytoweb external currentness profile",
            "adds ExternalRegistryVerificationTrace as an OFARM-owned trace carrier",
            "distinguishes jurisdictional product authorisation from EU active-substance context and commercial GTIN evidence",
            "hardens PassportView refusal/review behavior for external-binding uncertainty"
        ],
        "limitations": records.get("nonClaims", [])
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overallStatus"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
