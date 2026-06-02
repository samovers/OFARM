#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = ROOT / "04_implementation_and_conformance" / "OFARM_reference_resolution_results_v0_1.json"
REPORT_OUT = MC / "OFARM_ReferenceResolutionReport_example_generated_package_local_v0_1.json"
MANIFEST_ID = "reference-resolution-manifest:ontology-semint:v0.1"
PACKAGE_LOCAL_PREFIXES = ("reference-snapshot:",)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def primary_ids(obj: Any) -> list[tuple[str, str]]:
    if not isinstance(obj, dict):
        return []
    # Only index true object identities, not trace fields such as sourceObjectId or targetObjectId.
    primary_fields = {
        "referenceSnapshotId", "agronomicCodeBindingProfileId", "agronomicIdentityBindingId",
        "agronomicObservationContextId", "measurementEvidenceId", "interventionIntentPayloadId",
        "executionRecordPayloadId", "partialExtentId", "assertionRecordId", "reviewDecisionId",
        "acceptedEventConsequenceId", "queryId", "semanticPathAliasCatalogId",
        "agronomicReconstructionPolicyId", "agronomicReconstructionTraceId",
        "referenceResolutionManifestId", "referenceResolutionReportId", "temporalFieldConformanceMatrixId",
        "contextSnapshotId", "currentStateMaterializationId", "passportViewMetadataId",
        "documentAssemblyMetadataId", "authorityGrantId", "delegationGrantId",
        "sharingGrantId", "revocationDecisionId", "roleAssignmentId"
    }
    out = []
    for key, value in obj.items():
        if isinstance(value, str) and (key in primary_fields or key == "artifactId" or key == "id"):
            out.append((key, value))
    return out


def source_object_id(obj: Any) -> str | None:
    ids = primary_ids(obj)
    return ids[0][1] if ids else None


def source_object_class(filename: str) -> str:
    if filename.startswith("OFARM_") and "_example_" in filename:
        return filename[len("OFARM_"):].split("_example_", 1)[0]
    return "UNKNOWN"


def walk_refs(node: Any, path: list[str], refs: list[dict[str, str]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = path + [key]
            if isinstance(value, str) and (key.endswith("Ref") or key.endswith("Refs") or key.endswith("ProfileRef") or key.endswith("PolicyRef")):
                refs.append({"path": ".".join(next_path), "field": key, "value": value})
            elif isinstance(value, list) and (key.endswith("Refs") or key.endswith("BindingRefs")):
                for idx, item in enumerate(value):
                    if isinstance(item, str):
                        refs.append({"path": ".".join(next_path + [str(idx)]), "field": key, "value": item})
            walk_refs(value, next_path, refs)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            walk_refs(item, path + [str(idx)], refs)


def main() -> int:
    examples = sorted(MC.glob("*_example_*.json"))
    id_index: dict[str, list[dict[str, str]]] = defaultdict(list)
    payloads: dict[str, Any] = {}
    for path in examples:
        try:
            obj = load_json(path)
        except Exception:
            continue
        payloads[path.name] = obj
        for field, value in primary_ids(obj):
            id_index[value].append({"targetArtifact": f"03_machine_contracts/{path.name}", "idField": field, "idValue": value, "targetObjectClass": source_object_class(path.name)})

    findings = []
    refs_checked = 0
    for filename, obj in payloads.items():
        refs: list[dict[str, str]] = []
        walk_refs(obj, [], refs)
        for ref in refs:
            value = ref["value"]
            if not value.startswith(PACKAGE_LOCAL_PREFIXES):
                continue
            refs_checked += 1
            base = {
                "schemaVersion": "ofarm.referenceresolutionfinding.v0.1",
                "findingId": f"ref-find:ontology-semint:{refs_checked:04d}",
                "sourceArtifact": f"03_machine_contracts/{filename}",
                "sourceObjectId": source_object_id(obj) or "unknown",
                "sourceObjectClass": source_object_class(filename),
                "refPath": ref["path"],
                "refField": ref["field"],
                "refValue": value,
                "expectedTargetClass": "ReferenceSnapshot",
                "consequenceClass": "HIGH" if "crop-protection" in value or "passport" in filename.lower() else "MEDIUM",
            }
            targets = id_index.get(value, [])
            if len(targets) == 1:
                target = targets[0]
                finding = {**base, "targetArtifact": target["targetArtifact"], "targetObjectId": value, "targetObjectClass": target["targetObjectClass"], "resolutionStatus": "RESOLVED_PACKAGE_LOCAL", "severity": "INFO", "notes": "Package-local ReferenceSnapshot resolved."}
            elif len(targets) > 1:
                finding = {**base, "targetObjectId": value, "targetObjectClass": "ReferenceSnapshot", "resolutionStatus": "TYPE_MISMATCH", "severity": "ERROR", "notes": f"Reference resolved to {len(targets)} targets; expected exactly one."}
            else:
                finding = {**base, "resolutionStatus": "UNRESOLVED_PACKAGE_LOCAL", "severity": "FAIL_CLOSED", "notes": "Package-local ReferenceSnapshot did not resolve."}
            findings.append(finding)

    unresolved = [f for f in findings if f["resolutionStatus"] == "UNRESOLVED_PACKAGE_LOCAL"]
    errors = [f for f in findings if f["severity"] in {"ERROR", "FAIL_CLOSED"}]
    summary = {
        "filesChecked": len(payloads),
        "refsChecked": refs_checked,
        "resolvedPackageLocalCount": sum(1 for f in findings if f["resolutionStatus"] == "RESOLVED_PACKAGE_LOCAL"),
        "unresolvedPackageLocalCount": len(unresolved),
        "externalDeclaredCount": 0,
        "externalVerifiedCount": 0,
        "warningCount": 0,
        "errorCount": len(errors),
    }
    overall = "PASS" if not errors else "FAIL_CLOSED"
    report = {
        "schemaVersion": "ofarm.referenceresolutionreport.v0.1",
        "reportId": "reference-resolution-report:ontology-semint:package-local:v0.1",
        "manifestRef": MANIFEST_ID,
        "generatedAt": "2026-05-14T12:30:00+02:00",
        "runner": Path(__file__).name,
        "scope": "Package-local ReferenceSnapshot resolution across machine-contract examples.",
        "overallStatus": overall,
        "summary": summary,
        "findings": findings,
        "notes": "This runner hard-requires package-local ReferenceSnapshot IDs. It does not claim live external registry verification."
    }
    OUT.write_text(json.dumps({"overallStatus": overall, "summary": summary, "unresolved": unresolved, "reportArtifact": "03_machine_contracts/" + REPORT_OUT.name}, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
