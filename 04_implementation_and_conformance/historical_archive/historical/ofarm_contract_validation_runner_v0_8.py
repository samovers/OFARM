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
OUT = Path(__file__).resolve().parent / "OFARM_machine_contract_validation_results_v0_8.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def infer_schema(example_name: str, schema_names: list[str]) -> str | None:
    if "_example_" not in example_name:
        return None
    prefix = example_name.split("_example_")[0]
    candidates = sorted([s for s in schema_names if s.startswith(prefix + "_schema_")])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    for candidate in candidates:
        if "v0_2_draft" in example_name and "v0_2_draft" in candidate:
            return candidate
    for candidate in candidates:
        if "v0_1" in candidate:
            return candidate
    return candidates[0]


def main() -> int:
    result = {"schemaChecks": {}, "exampleValidation": {}, "overall": "PASS"}
    schema_names = sorted([p.name for p in MC.glob("*_schema_*.json")])
    schemas = {}

    for schema_name in schema_names:
        path = MC / schema_name
        try:
            schema = load_json(path)
            jsonschema.Draft202012Validator.check_schema(schema)
            schemas[schema_name] = schema
            result["schemaChecks"][schema_name] = "PASS"
        except Exception as e:
            result["schemaChecks"][schema_name] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    example_names = sorted([p.name for p in MC.glob("*_example_*.json")])
    for example_name in example_names:
        schema_name = infer_schema(example_name, schema_names)
        key = f"{example_name} :: {schema_name or 'NO_MATCH'}"
        try:
            if schema_name is None:
                raise ValueError("could not infer matching schema")
            data = load_json(MC / example_name)
            jsonschema.validate(data, schemas[schema_name])
            result["exampleValidation"][key] = "PASS"
        except Exception as e:
            result["exampleValidation"][key] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
