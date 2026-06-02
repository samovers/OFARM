#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this runner") from e
ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
FIX = Path(__file__).resolve().parent / "ofarm_evidence_sufficiency_fixtures_v0_2"
OUT = Path(__file__).resolve().parent / "OFARM_evidence_sufficiency_fixture_results_v0_2.json"
CASE_SCHEMA_V1 = json.loads((MC / "OFARM_EvidenceSufficiencyCase_schema_v0_1.json").read_text(encoding="utf-8"))
CASE_SCHEMA_V2 = json.loads((MC / "OFARM_EvidenceSufficiencyCase_schema_v0_2.json").read_text(encoding="utf-8"))
SNAPSHOT_SCHEMA = json.loads((MC / "OFARM_MaterializationSnapshot_schema_v0_1.json").read_text(encoding="utf-8"))
BASIS_SCHEMA = json.loads((MC / "OFARM_MaterializationBasis_schema_v0_1.json").read_text(encoding="utf-8"))
CASE_FILES_V1 = [
    "OFARM_EvidenceSufficiencyCase_example_compliance_assertion_v0_1.json",
    "OFARM_EvidenceSufficiencyCase_example_attested_document_v0_1.json",
    "OFARM_EvidenceSufficiencyCase_example_submission_package_v0_1.json",
    "OFARM_EvidenceSufficiencyCase_example_review_required_v0_1.json",
    "OFARM_EvidenceSufficiencyCase_example_refusal_v0_1.json",
]
CASE_FILES_V2 = [
    "OFARM_EvidenceSufficiencyCase_example_ambiguous_ppp_identity_upgrade_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_partial_machine_log_manual_top_up_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_late_lab_result_after_intervention_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_late_evidence_post_output_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_late_evidence_post_submission_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_timestamp_incomplete_record_time_only_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_source_quality_low_ocr_only_refusal_v0_2.json",
    "OFARM_EvidenceSufficiencyCase_example_human_machine_conflict_review_v0_2.json",
]
SNAPSHOT_FILES = [
    "OFARM_MaterializationSnapshot_example_field_submission_v0_1.json",
    "OFARM_MaterializationSnapshot_example_field_dossier_v0_1.json",
]
BASIS_FILES = [
    "OFARM_MaterializationBasis_example_field_compliance_v0_1.json",
    "OFARM_MaterializationBasis_example_field_compliance_after_orchard_context_v0_1.json",
]
FIXTURES = sorted(FIX.glob("*.json"))
PROMOTED_REASON_CODES = {
    "AMBIGUOUS_PRODUCT_ID",
    "TIMESTAMP_INCOMPLETE",
    "SOURCE_QUALITY_LOW",
    "MACHINE_RECORD_PARTIAL",
    "HUMAN_MACHINE_CONFLICT",
    "LATE_EVIDENCE_POST_OUTPUT",
    "LATE_EVIDENCE_POST_SUBMISSION",
}
PROMOTED_AXIS_FIELDS = [
    "sourceSpecificity",
    "captureIntegrity",
    "chronologyIntegrity",
    "crossSourceAgreement",
    "lateArrivalPosture",
]
def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)
def validate(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    jsonschema.validate(payload, schema)
def count_complete_bundles(case: Dict[str, Any]) -> int:
    return sum(1 for bundle in case.get("evidenceBundles", []) if bundle.get("bundleStatus") == "COMPLETE")
def index_cases() -> Dict[str, Dict[str, Any]]:
    cases = {}
    for fname in CASE_FILES_V1 + CASE_FILES_V2:
        data = load_json(MC / fname)
        cases[data["sufficiencyCaseId"]] = data
    return cases
def index_snapshots() -> Dict[str, Dict[str, Any]]:
    snaps = {}
    for fname in SNAPSHOT_FILES:
        data = load_json(MC / fname)
        snaps[data["snapshotId"]] = data
    return snaps
def index_bases() -> Dict[str, Dict[str, Any]]:
    bases = {}
    for fname in BASIS_FILES:
        data = load_json(MC / fname)
        bases[data["basisId"]] = data
    return bases
def check_case_logic(case: Dict[str, Any], bases: Dict[str, Dict[str, Any]], snaps: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    decision = case["outcome"]["decision"]
    complete_bundles = count_complete_bundles(case)
    claims = {c["claimId"] for c in case["claims"]}
    arguments = {a["argumentId"]: a for a in case["arguments"]}
    reason_codes = set(case["outcome"].get("insufficiencyReasonCodes", []))
    for claim_id in claims:
        expect(any(claim_id in arg.get("supportsClaimIds", []) for arg in case["arguments"]), f"{case['sufficiencyCaseId']} claim {claim_id} must be referenced by an argument")
    for argument_id in arguments:
        expect(any(argument_id in bundle.get("supportsArgumentIds", []) for bundle in case.get("evidenceBundles", [])), f"{case['sufficiencyCaseId']} argument {argument_id} must be referenced by an evidence bundle")
    has_snapshot = bool(case.get("materializationSnapshotRef"))
    if case["caseClass"] in {"DOCUMENT_ATTESTATION", "SUBMISSION_ASSEMBLY"}:
        expect(case.get("materializationBasisRef") in bases, f"{case['sufficiencyCaseId']} must resolve materialization basis")
        expect(case.get("materializationSnapshotRef") in snaps, f"{case['sufficiencyCaseId']} must resolve materialization snapshot")
        snap = snaps[case["materializationSnapshotRef"]]
        expect(snap["materializationBasisRef"] == case["materializationBasisRef"], f"{case['sufficiencyCaseId']} snapshot must point to same basis as the case")
        expect(case.get("attestationPlan") is not None, f"{case['sufficiencyCaseId']} output case must carry attestation plan")
        expect(case["subject"]["subjectType"] != "ASSERTION_RECORD", f"{case['sufficiencyCaseId']} output case cannot target assertion record")
    else:
        if case.get("materializationBasisRef"):
            expect(case["materializationBasisRef"] in bases, f"{case['sufficiencyCaseId']} basis ref must resolve when present")
    if case["schemaVersion"] == "ofarm.evidencesufficiencycase.v0.2":
        for bundle in case.get("evidenceBundles", []):
            if any(field in bundle for field in PROMOTED_AXIS_FIELDS):
                for field in PROMOTED_AXIS_FIELDS:
                    expect(field in bundle, f"{case['sufficiencyCaseId']} promoted bundle must carry full promoted axis set when any promoted axis is used")
    if decision == "ALLOW":
        expect(all(arg["conclusion"] == "SUPPORTED" for arg in case["arguments"]), f"{case['sufficiencyCaseId']} allow case must have SUPPORTED arguments")
        expect(complete_bundles >= 1, f"{case['sufficiencyCaseId']} allow case must have at least one COMPLETE bundle")
        for bundle in case["evidenceBundles"]:
            if bundle["bundleStatus"] == "COMPLETE":
                expect(len(bundle.get("rawSourceRefs", [])) >= 1, f"{case['sufficiencyCaseId']} complete bundle must retain raw source refs")
                expect(len(bundle.get("normalizedInterpretationRefs", [])) >= 1, f"{case['sufficiencyCaseId']} complete bundle must retain normalized interpretation refs")
                expect(len(bundle.get("provenanceRefs", [])) >= 1, f"{case['sufficiencyCaseId']} complete bundle must retain provenance refs")
        expect(case["outcome"].get("attestationAllowed") == (case["caseClass"] in {"DOCUMENT_ATTESTATION", "SUBMISSION_ASSEMBLY"}), f"{case['sufficiencyCaseId']} allow posture must align attestationAllowed with output class")
    elif decision == "REQUIRE_REVIEW":
        expect(any(arg["conclusion"] == "REVIEW_REQUIRED" for arg in case["arguments"]), f"{case['sufficiencyCaseId']} review case must carry REVIEW_REQUIRED conclusion")
        expect(len(reason_codes) >= 1, f"{case['sufficiencyCaseId']} review case must preserve insufficiency reasons")
        expect(len(case["outcome"].get("blockingGapRefs", [])) >= 1, f"{case['sufficiencyCaseId']} review case must preserve blocking gaps")
        expect(case["outcome"]["attestationAllowed"] is False, f"{case['sufficiencyCaseId']} review case must block automatic attestation")
    elif decision == "REFUSE":
        expect(any(arg["conclusion"] == "UNSUPPORTED" for arg in case["arguments"]), f"{case['sufficiencyCaseId']} refusal case must carry UNSUPPORTED conclusion")
        expect(len(reason_codes) >= 1, f"{case['sufficiencyCaseId']} refusal case must preserve insufficiency reasons")
        expect(len(case["outcome"].get("blockingGapRefs", [])) >= 1, f"{case['sufficiencyCaseId']} refusal case must preserve blocking gaps")
        expect(case["outcome"]["attestationAllowed"] is False, f"{case['sufficiencyCaseId']} refusal case must not allow attestation")
    else:
        raise AssertionError(f"Unexpected decision {decision}")
    return {
        "schemaVersion": case["schemaVersion"],
        "decision": decision,
        "subjectType": case["subject"]["subjectType"],
        "completeBundleCount": complete_bundles,
        "hasMaterializationSnapshot": has_snapshot,
        "hasAttestationPlan": case.get("attestationPlan") is not None,
        "attestationAllowed": case["outcome"]["attestationAllowed"],
        "reasonCodes": sorted(reason_codes),
    }
def main() -> int:
    result: Dict[str, Any] = {
        "exampleValidation": {},
        "fixtureResults": {},
        "promotedReasonCodeCoverage": {},
        "overall": "PASS",
    }
    try:
        jsonschema.Draft202012Validator.check_schema(CASE_SCHEMA_V1)
        jsonschema.Draft202012Validator.check_schema(CASE_SCHEMA_V2)
        jsonschema.Draft202012Validator.check_schema(SNAPSHOT_SCHEMA)
        jsonschema.Draft202012Validator.check_schema(BASIS_SCHEMA)
        cases = index_cases()
        snaps = index_snapshots()
        bases = index_bases()
        for fname in CASE_FILES_V1:
            payload = load_json(MC / fname)
            validate(payload, CASE_SCHEMA_V1)
            result["exampleValidation"][f"{fname} :: OFARM_EvidenceSufficiencyCase_schema_v0_1.json"] = "PASS"
        for fname in CASE_FILES_V2:
            payload = load_json(MC / fname)
            validate(payload, CASE_SCHEMA_V2)
            result["exampleValidation"][f"{fname} :: OFARM_EvidenceSufficiencyCase_schema_v0_2.json"] = "PASS"
        for fname in SNAPSHOT_FILES:
            payload = load_json(MC / fname)
            validate(payload, SNAPSHOT_SCHEMA)
            result["exampleValidation"][f"{fname} :: OFARM_MaterializationSnapshot_schema_v0_1.json"] = "PASS"
        for fname in BASIS_FILES:
            payload = load_json(MC / fname)
            validate(payload, BASIS_SCHEMA)
            result["exampleValidation"][f"{fname} :: OFARM_MaterializationBasis_schema_v0_1.json"] = "PASS"
        observed_codes = set()
        for fixture_path in FIXTURES:
            fixture = load_json(fixture_path)
            case = cases[fixture["facts"]["sufficiencyCaseRef"]]
            actual = check_case_logic(case, bases, snaps)
            expect(actual["decision"] == fixture["facts"]["expectedDecision"], f"{fixture['fixtureId']} decision mismatch")
            expect(actual["subjectType"] == fixture["facts"]["expectedSubjectType"], f"{fixture['fixtureId']} subject type mismatch")
            expect(actual["hasMaterializationSnapshot"] == fixture["expectedOutcome"]["requiresMaterializationSnapshot"], f"{fixture['fixtureId']} snapshot requirement mismatch")
            expect(actual["hasAttestationPlan"] == fixture["expectedOutcome"]["requiresAttestationPlan"], f"{fixture['fixtureId']} attestation plan requirement mismatch")
            expect(actual["completeBundleCount"] >= fixture["expectedOutcome"]["minimumCompleteBundles"], f"{fixture['fixtureId']} complete bundle threshold mismatch")
            expect(actual["attestationAllowed"] == fixture["expectedOutcome"]["attestationAllowed"], f"{fixture['fixtureId']} attestationAllowed mismatch")
            expect(len(actual["reasonCodes"]) >= fixture["expectedOutcome"].get("minimumReasonCodes", 0), f"{fixture['fixtureId']} reason code threshold mismatch")
            for code in fixture["expectedOutcome"].get("requiredReasonCodes", []):
                expect(code in actual["reasonCodes"], f"{fixture['fixtureId']} missing required reason code {code}")
                observed_codes.add(code)
            for field in fixture["expectedOutcome"].get("requiredBundleFields", []):
                expect(all(field in bundle for bundle in cases[fixture['facts']['sufficiencyCaseRef']].get('evidenceBundles', [])), f"{fixture['fixtureId']} missing required bundle field {field}")
            result["fixtureResults"][fixture["fixtureId"]] = {
                "status": "PASS",
                "actual": actual,
                "expectedDecision": fixture["facts"]["expectedDecision"],
            }
        # Coverage check: all promoted codes must appear at least once in v0.2 examples.
        all_v2_codes = set()
        for fname in CASE_FILES_V2:
            payload = load_json(MC / fname)
            all_v2_codes.update(payload.get("outcome", {}).get("insufficiencyReasonCodes", []))
        missing = sorted(PROMOTED_REASON_CODES - all_v2_codes)
        result["promotedReasonCodeCoverage"] = {
            "requiredCodes": sorted(PROMOTED_REASON_CODES),
            "observedCodes": sorted(all_v2_codes),
            "status": "PASS" if not missing else "FAIL",
            "missingCodes": missing,
        }
        expect(not missing, f"promoted reason code coverage incomplete: {missing}")
    except Exception as e:
        result["overall"] = "FAIL"
        result["fatalError"] = str(e)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1
if __name__ == "__main__":
    raise SystemExit(main())
