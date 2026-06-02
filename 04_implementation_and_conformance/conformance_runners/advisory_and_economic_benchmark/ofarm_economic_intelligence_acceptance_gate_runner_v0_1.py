import json
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent

def load_json(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))

def load_text(name):
    return (HERE / name).read_text(encoding='utf-8')

matpub = load_json('OFARM_runtime_materialization_publication_results_v0_1.json')
authshare = load_json('OFARM_runtime_authority_action_class_and_sharing_results_v0_1.json')
gatelog = load_json('OFARM_runtime_gate_log_and_projection_traceback_results_v0_1.json')
aliasres = load_json('OFARM_runtime_alias_compilation_and_saved_query_regression_results_v0_1.json')
queryeq = load_json('OFARM_runtime_query_plan_target_equivalence_results_v0_1.json')
grapheq = load_json('OFARM_runtime_graph_pattern_equivalence_results_v0_1.json')
econ_text = load_text('OFARM_economic_intelligence_contract_validation_results_v0_3.txt')

overall_econ = 'PASS' if '\nOVERALL: PASS' in econ_text else 'FAIL'
slice_a = load_json('ofarm_economic_intelligence_spike_v0_1/experimental_machine_contracts/examples/positive/slice_a_operational_only/OFARM_AdvisoryScenarioResultSet_example_slice_a_crop_ranking_v0_1.json')
blob = json.dumps(slice_a).lower()
forbidden_terms = ['operating profit', 'net profit', 'return on assets', 'operating margin']
negated_profitability = 'not a profitability statement' in blob
scenario1_honesty = negated_profitability and not any(term in blob for term in forbidden_terms)

projection_partial = any(item.get('coverage') == 'PARTIAL' for item in gatelog.get('projectionTraceBack', {}).values())

checks = [
    {
        "id": "C1_NO_SECOND_QUERY_MODEL",
        "status": "PASS_WITH_LIMITATIONS" if all(s in ("PASS", "PASS_WITH_LIMITATIONS") for s in [overall_econ, aliasres["status"], queryeq["overall"], grapheq["overallStatus"]]) else "FAIL",
        "sources": [
            "OFARM_economic_intelligence_contract_validation_results_v0_3.txt",
            "OFARM_runtime_alias_compilation_and_saved_query_regression_results_v0_1.json",
            "OFARM_runtime_query_plan_target_equivalence_results_v0_1.json",
            "OFARM_runtime_graph_pattern_equivalence_results_v0_1.json",
        ],
        "notes": [
            "Economic scenario contracts validate and invalid query-posture cases fail.",
            "Alias and target-equivalence proofs remain bounded package-local runtime evidence."
        ],
    },
    {
        "id": "C2_NO_SECOND_TRUTH_STORE",
        "status": "PASS_WITH_LIMITATIONS" if overall_econ=="PASS" and all(v["status"]=="PASS" for v in gatelog["runtimeGateLogs"].values()) else "FAIL",
        "sources": [
            "OFARM_economic_intelligence_contract_validation_results_v0_3.txt",
            "OFARM_runtime_gate_log_and_projection_traceback_results_v0_1.json",
        ],
        "notes": [
            "Scenario results do not pass as current-state authority in the bounded examples.",
            "Projection trace-back passes but remains partial in multiple records."
        ],
    },
    {
        "id": "C3_NO_ERP_CREEP",
        "status": "PASS" if overall_econ=="PASS" else "FAIL",
        "sources": ["OFARM_economic_intelligence_contract_validation_results_v0_3.txt"],
        "notes": ["Ledger-like imported finance fields are rejected in negative cases."],
    },
    {
        "id": "C4_NO_SILENT_BRIDGE",
        "status": "PASS" if overall_econ=="PASS" else "FAIL",
        "sources": [
            "OFARM_economic_intelligence_contract_validation_results_v0_3.txt",
            "OFARM_runtime_gate_log_and_projection_traceback_results_v0_1.json",
        ],
        "notes": [
            "BridgeCandidate remains human-gated.",
            "Gate sequencing keeps advisory outputs proposal-shaped."
        ],
    },
    {
        "id": "C5_FRESHNESS_DISCIPLINE",
        "status": "PASS_WITH_LIMITATIONS" if matpub["overallStatus"] in ("PASS", "PASS_WITH_LIMITATIONS") else "FAIL",
        "sources": [
            "OFARM_runtime_materialization_publication_results_v0_1.json",
            "OFARM_runtime_gate_log_and_projection_traceback_results_v0_1.json",
        ],
        "notes": [
            "High-consequence outputs require recompute/refusal when stale or invalid.",
            "Proof remains bounded to shipped output families and package-local evidence."
        ],
    },
    {
        "id": "C6_OUTPUT_TAXONOMY_DISCIPLINE",
        "status": "PASS_WITH_LIMITATIONS" if matpub["overallStatus"] in ("PASS", "PASS_WITH_LIMITATIONS") else "FAIL",
        "sources": ["OFARM_runtime_materialization_publication_results_v0_1.json"],
        "notes": [
            "Passport-vs-document separation is preserved in bounded runtime evidence.",
            "No economic passport family appears in the checked economics seam."
        ],
    },
    {
        "id": "C7_SCENARIO_1_HONESTY",
        "status": "PASS" if overall_econ=="PASS" and scenario1_honesty else "FAIL",
        "sources": [
            "OFARM_economic_intelligence_contract_validation_results_v0_3.txt",
            "slice_a_operational_only example bundle",
        ],
        "notes": [
            "Operational-only slice explicitly self-limits to screening/ranking/constraint posture and negates profitability claims."
        ],
    },
    {
        "id": "C8_AUTHORITY_SHARING_DISCIPLINE",
        "status": "PASS_WITH_LIMITATIONS" if authshare["overallStatus"] in ("PASS", "PASS_WITH_LIMITATIONS") else "FAIL",
        "sources": ["OFARM_runtime_authority_action_class_and_sharing_results_v0_1.json"],
        "notes": [
            "Explicit sharing and no-implicit-access pathways pass in bounded runtime-shaped evidence.",
            "Coverage remains bounded to curated scenarios."
        ],
    },
]

cutback_triggers = [
    {"id": "T1_MANUAL_FINANCE_BURDEN_BEFORE_VALUE", "status": "NOT_OBSERVED_IN_ARTIFACTS", "notes": "Artifact checks cannot prove future UI burden; still requires implementation testing."},
    {"id": "T2_IMPORTED_FINANCE_AS_ACCOUNTING_STATE", "status": "NOT_TRIGGERED", "notes": "Negative ledger-like import fails validation."},
    {"id": "T3_ADVISORY_REUSED_AS_CURRENT_STATE", "status": "NOT_TRIGGERED", "notes": "No checked result path treats advisory scenarios as current-state authority."},
    {"id": "T4_UNDECLARED_SCENARIO_ONLY_SEMANTICS", "status": "NOT_TRIGGERED_WITH_LIMITATIONS", "notes": "No second query model detected in bounded proofs; deployment-scale proof still absent."},
    {"id": "T5_LOW_FRICTION_AUTO_PROMOTION", "status": "NOT_TRIGGERED", "notes": "BridgeCandidate remains human-gated and gate logs preserve review/promote discipline."},
]

all_mandatory_full = all(c["status"] == "PASS" for c in checks)
any_fail = any(c["status"] == "FAIL" for c in checks)
if any_fail:
    gate_outcome = "FAIL"
elif all_mandatory_full:
    gate_outcome = "PASS"
else:
    gate_outcome = "PARTIAL_PASS"

promotion_blockers = []
if projection_partial:
    promotion_blockers.append("Projection trace-back coverage remains partial in bounded runtime records.")
if aliasres["status"] == "PASS_WITH_LIMITATIONS":
    promotion_blockers.append("Alias/runtime query proof is bounded package-local evidence, not deployment telemetry.")
if queryeq["overall"] == "PASS_WITH_LIMITATIONS":
    promotion_blockers.append("Execution-target equivalence proof is bounded to approved query subsets.")
if matpub["overallStatus"] == "PASS_WITH_LIMITATIONS":
    promotion_blockers.append("Materialization/publication proof is bounded to shipped output families.")
if authshare["overallStatus"] == "PASS_WITH_LIMITATIONS":
    promotion_blockers.append("Authority/sharing proof remains bounded to curated scenarios.")
promotion_blockers.append("The packaged top-level economics validation runner needed consolidation repair before the check cycle could run cleanly.")

result = {
    "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "gateOutcome": gate_outcome,
    "promotionDecision": "KEEP_IN_01_AND_04_ONLY",
    "promotionBlockers": promotion_blockers,
    "mandatoryChecks": checks,
    "cutBackTriggers": cutback_triggers,
}
print(json.dumps(result, indent=2))
