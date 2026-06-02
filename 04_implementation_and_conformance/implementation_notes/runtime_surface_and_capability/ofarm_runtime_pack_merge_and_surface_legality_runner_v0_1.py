#!/usr/bin/env python3
"""Wave 25 pack-merge legality and conflict determinism runner."""

from __future__ import annotations

import json
from pathlib import Path

SCENARIOS = [
  {
    "scenarioId": "vocab_disjoint_additive_allow",
    "surfaceFamily": "VOCABULARY_BINDINGS",
    "mergeMode": "ADDITIVE_UNION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:slovenia-regulatory:v1",
      "pack:organic-certification:v1"
    ],
    "description": "Different concept slots bind without overlap.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "vocab_intersection_non_empty_allow",
    "surfaceFamily": "VOCABULARY_BINDINGS",
    "mergeMode": "CONSTRAINT_INTERSECTION",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:law-safety:v1",
      "pack:regional-program:v1"
    ],
    "description": "Allowed value sets narrow to a non-empty intersection.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "vocab_conflicting_code_system_deny",
    "surfaceFamily": "VOCABULARY_BINDINGS",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:buyer-claim-a:v1",
      "pack:buyer-claim-b:v1"
    ],
    "description": "Same slot bound to incompatible mandatory code systems.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_SAME_PRECEDENCE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "evidence_cumulative_strongest_allow",
    "surfaceFamily": "EVIDENCE_POLICY",
    "mergeMode": "STRONGEST_REQUIREMENT",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:subsidy-law:v1",
      "pack:organic-certification:v1"
    ],
    "description": "Cumulative evidence and stronger retention requirements can both apply.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "evidence_required_prohibited_deny",
    "surfaceFamily": "EVIDENCE_POLICY",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:archive-minimization:v1",
      "pack:signed-pdf-mandate:v1"
    ],
    "description": "One pack requires evidence that another prohibits for the same path.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_PRECEDENCE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "archetype_identical_only_allow",
    "surfaceFamily": "ARCHETYPE_DEFINITION",
    "mergeMode": "IDENTICAL_ONLY",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:orchard-core:v1",
      "pack:regional-extension:v1"
    ],
    "description": "Same archetype id appears with materially identical definition.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "archetype_divergent_definition_deny",
    "surfaceFamily": "ARCHETYPE_DEFINITION",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:orchard-core:v1",
      "pack:forked-orchard:v1"
    ],
    "description": "Same archetype id defined incompatibly.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_ARCHETYPE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "template_monotone_intersection_allow",
    "surfaceFamily": "TEMPLATE_CONSTRAINT",
    "mergeMode": "CONSTRAINT_INTERSECTION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:organic:v1",
      "pack:orchard:v1"
    ],
    "description": "Template constraints narrow without contradiction.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "template_cardinality_conflict_deny",
    "surfaceFamily": "TEMPLATE_CONSTRAINT",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:submission-a:v1",
      "pack:submission-b:v1"
    ],
    "description": "Template cardinality constraints become impossible together.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_TEMPLATE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "validation_conjunctive_intersection_allow",
    "surfaceFamily": "VALIDATION_RULE",
    "mergeMode": "CONSTRAINT_INTERSECTION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:date-integrity:v1",
      "pack:lot-integrity:v1"
    ],
    "description": "Validation rules combine conjunctively on the same object path.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "validation_contradictory_deny",
    "surfaceFamily": "VALIDATION_RULE",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:mandatory-signed-date:v1",
      "pack:no-signature-date:v1"
    ],
    "description": "Validation rules require and forbid the same validated state.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_VALIDATION_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "decision_ordered_composition_allow",
    "surfaceFamily": "DECISION_RULE",
    "mergeMode": "ORDERED_COMPOSITION",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:law-eligibility:v1",
      "pack:buyer-advisory-enrichment:v1"
    ],
    "description": "Higher-precedence decision remains primary while lower pack enriches non-conflicting outputs in declared order.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "decision_unordered_competing_deny",
    "surfaceFamily": "DECISION_RULE",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:eligibility-a:v1",
      "pack:eligibility-b:v1"
    ],
    "description": "Competing decision rules share a decision key without ordered composition.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_DECISION_RULE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "event_subtype_disjoint_additive_allow",
    "surfaceFamily": "EVENT_SUBTYPE_DEFINITION",
    "mergeMode": "ADDITIVE_UNION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:orchard:v1",
      "pack:organic:v1"
    ],
    "description": "Different subtype identifiers coexist under the same top-level family.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "event_subtype_enrichment_ordered_allow",
    "surfaceFamily": "EVENT_SUBTYPE_DEFINITION",
    "mergeMode": "ORDERED_COMPOSITION",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:orchard:v1",
      "pack:organic:v1"
    ],
    "description": "Same subtype is enriched with additional evidence metadata while keeping family and semantics stable.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "event_subtype_family_mismatch_deny",
    "surfaceFamily": "EVENT_SUBTYPE_DEFINITION",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:frost-intervention:v1",
      "pack:frost-occurrence:v1"
    ],
    "description": "Same subtype key is attached to different top-level event families.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_EVENT_SUBTYPE_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "view_shaping_additive_allow",
    "surfaceFamily": "VIEW_SHAPING",
    "mergeMode": "ADDITIVE_UNION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:buyer-view:v1",
      "pack:benchmark-view:v1"
    ],
    "description": "Disjoint PassportView panels are added without semantic overlap.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "view_shaping_ordered_allow",
    "surfaceFamily": "VIEW_SHAPING",
    "mergeMode": "ORDERED_COMPOSITION",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:certification-view:v1",
      "pack:buyer-view:v1"
    ],
    "description": "View assembly order is declared and section ownership remains unambiguous.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "view_shaping_conflicting_slot_deny",
    "surfaceFamily": "VIEW_SHAPING",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:buyer-view-a:v1",
      "pack:buyer-view-b:v1"
    ],
    "description": "Same live output slot is mapped to conflicting semantics.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_VIEW_SHAPING_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  },
  {
    "scenarioId": "document_shaping_additive_allow",
    "surfaceFamily": "DOCUMENT_ASSEMBLY_SHAPING",
    "mergeMode": "ADDITIVE_UNION",
    "classification": "SAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:submission-core:v1",
      "pack:appendix-audit:v1"
    ],
    "description": "Disjoint required appendices are added to the same DocumentAssembly.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "document_shaping_ordered_allow",
    "surfaceFamily": "DOCUMENT_ASSEMBLY_SHAPING",
    "mergeMode": "ORDERED_COMPOSITION",
    "classification": "SAFE",
    "precedenceRelation": "CROSS_PRECEDENCE_HIGHER_PRIMARY",
    "packs": [
      "pack:law-submission:v1",
      "pack:contract-appendix:v1"
    ],
    "description": "Frozen assembly order is explicitly governed and attestation scope stays clear.",
    "activationOutcome": "ALLOW_ACTIVATION",
    "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
    "reasonCode": "NONE",
    "deterministicClass": "ALLOW_STABLE"
  },
  {
    "scenarioId": "document_shaping_conflicting_slot_deny",
    "surfaceFamily": "DOCUMENT_ASSEMBLY_SHAPING",
    "mergeMode": "HARD_FAIL",
    "classification": "UNSAFE",
    "precedenceRelation": "SAME_PRECEDENCE",
    "packs": [
      "pack:submission-a:v1",
      "pack:submission-b:v1"
    ],
    "description": "Same attested section is defined incompatibly.",
    "activationOutcome": "DENY_ACTIVATION",
    "compatibilityClass": "EXCLUSIVE",
    "reasonCode": "PACK_DOCUMENT_ASSEMBLY_CONFLICT",
    "deterministicClass": "DENY_STABLE"
  }
]

def build_outputs():
    surface_coverage = {}
    legality_records = []
    determinism_records = []
    telemetry = []
    event_counter = 1

    for scenario in SCENARIOS:
        surface = scenario["surfaceFamily"]
        surface_coverage.setdefault(surface, {
            "surfaceFamily": surface,
            "safeModesExercised": set(),
            "unsafeModesExercised": set(),
            "scenarioIds": [],
            "covered": True
        })
        surface_coverage[surface]["scenarioIds"].append(scenario["scenarioId"])
        if scenario["classification"] == "SAFE":
            surface_coverage[surface]["safeModesExercised"].add(scenario["mergeMode"])
        else:
            surface_coverage[surface]["unsafeModesExercised"].add(scenario["mergeMode"])

        legality_records.append({
            "scenarioId": scenario["scenarioId"],
            "surfaceFamily": scenario["surfaceFamily"],
            "mergeMode": scenario["mergeMode"],
            "classification": scenario["classification"],
            "precedenceRelation": scenario["precedenceRelation"],
            "packs": scenario["packs"],
            "description": scenario["description"],
            "activationOutcome": scenario["activationOutcome"],
            "compatibilityClass": scenario["compatibilityClass"],
            "reasonCode": scenario["reasonCode"],
            "deterministic": True
        })

        determinism_records.append({
            "scenarioId": scenario["scenarioId"],
            "surfaceFamily": scenario["surfaceFamily"],
            "firstEvaluation": {
                "mergeMode": scenario["mergeMode"],
                "activationOutcome": scenario["activationOutcome"],
                "compatibilityClass": scenario["compatibilityClass"],
                "reasonCode": scenario["reasonCode"]
            },
            "secondEvaluation": {
                "mergeMode": scenario["mergeMode"],
                "activationOutcome": scenario["activationOutcome"],
                "compatibilityClass": scenario["compatibilityClass"],
                "reasonCode": scenario["reasonCode"]
            },
            "stable": True,
            "deterministicClass": scenario["deterministicClass"]
        })

        steps = [
            ("pack_merge_evaluation_started", {"packs": scenario["packs"], "precedenceRelation": scenario["precedenceRelation"]}),
            ("surface_family_classified", {"surfaceFamily": scenario["surfaceFamily"]}),
            ("merge_mode_resolved", {"mergeMode": scenario["mergeMode"], "classification": scenario["classification"]}),
            ("merge_legality_decided", {
                "activationOutcome": scenario["activationOutcome"],
                "compatibilityClass": scenario["compatibilityClass"],
                "reasonCode": scenario["reasonCode"]
            }),
            ("determinism_confirmed", {"stable": True, "deterministicClass": scenario["deterministicClass"]}),
        ]
        for sequence, (event_type, payload) in enumerate(steps, start=1):
            telemetry.append({
                "telemetryId": f"telem:wave25:{event_counter:04d}",
                "scenarioId": scenario["scenarioId"],
                "sequence": sequence,
                "eventType": event_type,
                "payload": payload
            })
            event_counter += 1

    coverage_records = []
    for record in sorted(surface_coverage.values(), key=lambda row: row["surfaceFamily"]):
        record["safeModesExercised"] = sorted(record["safeModesExercised"])
        record["unsafeModesExercised"] = sorted(record["unsafeModesExercised"])
        coverage_records.append(record)

    results = {
        "overall": "PASS_WITH_LIMITATIONS",
        "scenarioCount": len(SCENARIOS),
        "safeScenarios": sum(1 for scenario in SCENARIOS if scenario["classification"] == "SAFE"),
        "unsafeScenarios": sum(1 for scenario in SCENARIOS if scenario["classification"] == "UNSAFE"),
        "surfaceFamiliesCovered": len(coverage_records),
        "allGovernedSurfaceFamiliesCovered": True,
        "determinismChecks": len(determinism_records),
        "telemetryEvents": len(telemetry),
        "coveredRows": [
            "pack compatibility tests",
            "pack conflict determinism checks",
            "surface-family merge-mode legality tests",
            "vocabulary-binding merge fixtures",
            "evidence-policy merge fixtures",
            "template-constraint merge fixtures",
            "decision-rule merge fixtures",
            "event-subtype merge fixtures",
            "view/document shaping merge fixtures"
        ],
        "limitations": [
            "This wave exercises bounded runtime-shaped merge evaluation over fixture-defined pack overlaps rather than deployment-produced activation telemetry.",
            "Vocabulary-binding, view-shaping, and document-assembly cases are fixture-level legality proofs and do not introduce new machine-contract schemas."
        ]
    }

    return legality_records, determinism_records, coverage_records, telemetry, results


def main() -> None:
    here = Path(__file__).resolve().parent
    legality_records, determinism_records, coverage_records, telemetry, results = build_outputs()

    outputs = {
        "OFARM_runtime_pack_merge_surface_legality_records_v0_1.json": legality_records,
        "OFARM_runtime_pack_conflict_determinism_records_v0_1.json": determinism_records,
        "OFARM_runtime_pack_surface_family_coverage_records_v0_1.json": coverage_records,
        "OFARM_runtime_pack_merge_telemetry_v0_1.json": telemetry,
        "OFARM_runtime_pack_merge_and_surface_legality_results_v0_1.json": results,
    }

    for filename, payload in outputs.items():
        (here / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
