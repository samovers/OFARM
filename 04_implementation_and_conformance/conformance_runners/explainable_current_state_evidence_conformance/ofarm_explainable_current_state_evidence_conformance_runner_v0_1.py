#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FIXTURE_FILE = BASE / "fixtures_explainable_current_state_evidence_v0_1.json"
SUMMARY_JSON = BASE / "OFARM_explainable_current_state_evidence_conformance_summary_v0_1.json"
SUMMARY_MD = BASE / "OFARM_explainable_current_state_evidence_conformance_summary_v0_1.md"

EXPECTED_FIXTURE_IDS = {
    "ecse-001-scoped-assertion-invalidation",
    "ecse-002-review-decision-supersession",
    "ecse-003-pack-profile-activation-change",
    "ecse-004-identity-lifecycle-revision",
    "ecse-005-reference-snapshot-update",
    "ecse-006-advisory-twin-stale-display",
    "ecse-007-compliance-twin-high-consequence-block",
    "ecse-008-trace-tier-enforcement",
    "ecse-009-projection-corruption-detection",
    "ecse-010-dependency-index-failure",
    "ecse-011-permission-redaction-boundary",
    "ecse-012-cold-rebuild-equivalence",
}

REQUIRED_FIXTURE_FIELDS = {
    "fixtureId",
    "purpose",
    "requiredInputFamilies",
    "expectedStatuses",
    "expectedTraceTier",
    "expectedBehavior",
    "passFailCriteria",
    "requiredMetricsIfBenchmarked",
    "syntheticFixturePassIsNotFleetReadinessEvidence",
}

REQUIRED_BEHAVIOR_FIELDS = {
    "recompute",
    "refuse",
    "review",
    "discloseLimitation",
}

TRACE_TIERS = {
    "TIER_1_QUALIFICATION",
    "TIER_2_RECONSTRUCTION",
    "TIER_3_FORENSIC_REPLAY",
}

STATUS_VALUES = {
    "FRESH",
    "STALE",
    "INVALID",
    "RECOMPUTE_REQUIRED",
}


def load_fixture_pack() -> dict:
    return json.loads(FIXTURE_FILE.read_text(encoding="utf-8"))


def nonempty_list(value: object) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(bool(item) for item in value)


def validate_fixture_pack(pack: dict) -> list[str]:
    issues: list[str] = []

    if pack.get("benchmarkClaimed") is not False:
        issues.append("fixture pack must not claim benchmark execution")
    if pack.get("productionReadinessClaimed") is not False:
        issues.append("fixture pack must not claim production readiness")
    if pack.get("fleetReadinessClaimed") is not False:
        issues.append("fixture pack must not claim fleet readiness")
    if pack.get("benchmarkArtifactsAreEvidenceNotTruth") is not True:
        issues.append("fixture pack must keep benchmark artifacts as evidence, not truth")
    if pack.get("doesNotOverrideActiveBaseline") is not True:
        issues.append("fixture pack must not override active baseline law")
    if pack.get("syntheticFixturePassIsNotFleetReadinessEvidence") is not True:
        issues.append("fixture pack must state synthetic fixture pass is not fleet-readiness evidence")

    fixtures = pack.get("fixtures")
    if not isinstance(fixtures, list):
        issues.append("fixtures must be a list")
        return issues

    fixture_ids = {fx.get("fixtureId") for fx in fixtures if isinstance(fx, dict)}
    if fixture_ids != EXPECTED_FIXTURE_IDS:
        missing = sorted(EXPECTED_FIXTURE_IDS - fixture_ids)
        extra = sorted(fixture_ids - EXPECTED_FIXTURE_IDS)
        issues.append(f"fixture id set mismatch; missing={missing}; extra={extra}")

    for fx in fixtures:
        if not isinstance(fx, dict):
            issues.append("fixture entry must be an object")
            continue
        fixture_id = fx.get("fixtureId", "<missing>")
        missing_fields = sorted(REQUIRED_FIXTURE_FIELDS - set(fx))
        if missing_fields:
            issues.append(f"{fixture_id}: missing required fields {missing_fields}")
            continue
        for field in ["requiredInputFamilies", "expectedStatuses", "passFailCriteria", "requiredMetricsIfBenchmarked"]:
            if not nonempty_list(fx.get(field)):
                issues.append(f"{fixture_id}: {field} must be a non-empty list")
        if fx.get("syntheticFixturePassIsNotFleetReadinessEvidence") is not True:
            issues.append(f"{fixture_id}: synthetic fixture pass disclaimer must be true")
        if fx.get("expectedTraceTier") not in TRACE_TIERS:
            issues.append(f"{fixture_id}: expectedTraceTier is invalid")
        bad_statuses = sorted(set(fx.get("expectedStatuses", [])) - STATUS_VALUES)
        if bad_statuses:
            issues.append(f"{fixture_id}: expectedStatuses contains invalid values {bad_statuses}")

        behavior = fx.get("expectedBehavior")
        if not isinstance(behavior, dict):
            issues.append(f"{fixture_id}: expectedBehavior must be an object")
            continue
        missing_behavior = sorted(REQUIRED_BEHAVIOR_FIELDS - set(behavior))
        if missing_behavior:
            issues.append(f"{fixture_id}: expectedBehavior missing fields {missing_behavior}")
        for field in REQUIRED_BEHAVIOR_FIELDS:
            if field in behavior and not isinstance(behavior[field], str):
                issues.append(f"{fixture_id}: expectedBehavior.{field} must be a string")
            if field in behavior and not behavior[field].strip():
                issues.append(f"{fixture_id}: expectedBehavior.{field} must not be empty")

    return issues


def write_summary(pack: dict, issues: list[str]) -> dict:
    fixtures = pack.get("fixtures", [])
    summary = {
        "schemaVersion": "ofarm.explainableCurrentStateEvidence.conformanceSummary.v0.1",
        "fixturePackId": pack.get("fixturePackId"),
        "rfcRef": pack.get("rfcRef"),
        "runner": "ofarm_explainable_current_state_evidence_conformance_runner_v0_1.py",
        "deterministicSkeleton": True,
        "benchmarkExecuted": False,
        "benchmarkClaimed": False,
        "productionReadinessClaimed": False,
        "fleetReadinessClaimed": False,
        "benchmarkArtifactsAreEvidenceNotTruth": True,
        "doesNotOverrideAcceptedRfcOrBaselineLaw": True,
        "syntheticFixturePassIsNotFleetReadinessEvidence": True,
        "fixtureCount": len(fixtures) if isinstance(fixtures, list) else 0,
        "expectedFixtureCount": len(EXPECTED_FIXTURE_IDS),
        "fixtureDefinitionValidationPassed": len(issues) == 0,
        "issues": issues,
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# Explainable Current-State Evidence Conformance Summary",
        "",
        "Status: deterministic fixture metadata validation only.",
        "",
        f"- Fixture pack: `{summary['fixturePackId']}`",
        f"- Fixture count: {summary['fixtureCount']}",
        f"- Fixture definition validation passed: {str(summary['fixtureDefinitionValidationPassed']).lower()}",
        "- Benchmark executed: false",
        "- Production readiness claimed: false",
        "- Fleet readiness claimed: false",
        "",
        "Synthetic fixture validation is not fleet-readiness evidence. Benchmark artifacts remain conformance evidence only and do not become canonical farm truth.",
    ]
    if issues:
        md.append("")
        md.append("## Issues")
        for issue in issues:
            md.append(f"- {issue}")
    SUMMARY_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    pack = load_fixture_pack()
    issues = validate_fixture_pack(pack)
    summary = write_summary(pack, issues)
    print(json.dumps({k: summary[k] for k in [
        "fixtureCount",
        "expectedFixtureCount",
        "fixtureDefinitionValidationPassed",
        "benchmarkExecuted",
        "productionReadinessClaimed",
        "fleetReadinessClaimed",
    ]}, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
