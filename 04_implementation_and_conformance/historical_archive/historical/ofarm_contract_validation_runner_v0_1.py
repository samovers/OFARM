
#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_machine_contract_validation_results_v0_1.json"

SCHEMAS = [
    "OFARM_QuerySpecification_schema_v0_1.json",
    "OFARM_QueryPlanIR_schema_v0_1.json",
    "OFARM_Capability_Manifest_schema_v0_1.json",
    "OFARM_PackMergeResolutionTrace_schema_v0_1.json",
    "OFARM_AuthorizationDecisionTrace_schema_v0_1.json",
    "OFARM_MaterializationBasis_schema_v0_1.json",
    "OFARM_MaterializationSnapshot_schema_v0_1.json",
]

EXAMPLES = [
    ("OFARM_QuerySpecification_schema_v0_1.json", "OFARM_QuerySpecification_example_field_passport_v0_1.json"),
    ("OFARM_QueryPlanIR_schema_v0_1.json", "OFARM_QueryPlanIR_example_field_passport_v0_1.json"),
    ("OFARM_Capability_Manifest_schema_v0_1.json", "OFARM_Capability_Manifest_example_core_deployment_v0_1.json"),
    ("OFARM_Capability_Manifest_schema_v0_1.json", "OFARM_Capability_Manifest_example_partner_deployment_v0_1.json"),
    ("OFARM_PackMergeResolutionTrace_schema_v0_1.json", "OFARM_PackMergeResolutionTrace_example_evidence_policy_merge_v0_1.json"),
    ("OFARM_AuthorizationDecisionTrace_schema_v0_1.json", "OFARM_AuthorizationDecisionTrace_example_service_provider_allow_v0_1.json"),
    ("OFARM_MaterializationBasis_schema_v0_1.json", "OFARM_MaterializationBasis_example_field_compliance_v0_1.json"),
    ("OFARM_MaterializationSnapshot_schema_v0_1.json", "OFARM_MaterializationSnapshot_example_field_submission_v0_1.json"),
]

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    result = {"schemaChecks": {}, "exampleValidation": {}, "overall": "PASS"}
    schemas = {}
    for schema_name in SCHEMAS:
        path = MC / schema_name
        try:
            schema = load_json(path)
            jsonschema.Draft202012Validator.check_schema(schema)
            result["schemaChecks"][schema_name] = "PASS"
            schemas[schema_name] = schema
        except Exception as e:
            result["schemaChecks"][schema_name] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    for schema_name, example_name in EXAMPLES:
        key = f"{example_name} :: {schema_name}"
        try:
            schema = schemas[schema_name]
            data = load_json(MC / example_name)
            jsonschema.validate(data, schema)
            result["exampleValidation"][key] = "PASS"
        except Exception as e:
            result["exampleValidation"][key] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
