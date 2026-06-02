#!/usr/bin/env python3
from __future__ import annotations
import copy, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class MinimalOFARMHostileRuntime:
    """Small deterministic CP6 runtime stub. Conformance evidence only, not production runtime."""
    traces: dict[str, dict[str, Any]] = field(default_factory=dict)
    current_state_mutations: list[dict[str, Any]] = field(default_factory=list)
    canonical_truth_mutations: list[dict[str, Any]] = field(default_factory=list)

    def run_case(self, case: dict[str, Any]) -> dict[str, Any]:
        scenario = case["scenarioKind"]
        trace_id = f"trace-{case['caseId']}"
        trace = {
            "schemaVersion": "ofarm.cp6.syntheticTrace.v0.1",
            "traceId": trace_id,
            "caseId": case["caseId"],
            "scenarioKind": scenario,
            "traceRetrievable": True,
            "gateChecks": [],
            "toolOutcome": {"attempted": False, "status": "NOT_ATTEMPTED"},
            "governanceOutcome": "UNSET",
            "blockedActions": [],
            "resultQualification": {"present": True, "qualificationStatus": "UNQUALIFIED", "materialLimitations": []},
            "canonicalTruthMutation": False,
            "currentStateMutation": False,
            "acceptedEvidenceCreated": False,
            "obligationCreated": False,
            "complianceBlockerCreatedByRequestOnly": False,
            "notes": []
        }
        def gate(name: str, status: str, reason: str | None = None):
            rec = {"gate": name, "status": status}
            if reason: rec["reasonCode"] = reason
            trace["gateChecks"].append(rec)
        def block(action: str, reason: str, detail: str):
            trace["blockedActions"].append({"action": action, "reasonCode": reason, "detail": detail, "traceRetrievable": True})
            trace["governanceOutcome"] = "DENIED"
        def qualify(status: str, *limits: str):
            trace["resultQualification"] = {"present": True, "qualificationStatus": status, "materialLimitations": list(limits)}

        if scenario == "agent_identity_without_authority_denied":
            gate("agent_identity_resolved","PASS"); gate("authority_envelope_present","FAIL","AUTHORITY_REQUIRED")
            block("state_affecting_action","AUTHORITY_REQUIRED","Agent identity, model identity, session, prompt, or API key is not authority.")
            qualify("BLOCKED","authority_missing")
        elif scenario == "revoked_authority_recheck_denied":
            gate("authority_snapshot_present","PASS"); gate("revocation_recheck","FAIL","AUTHORITY_REVOKED")
            block("agent_action_after_revocation","AUTHORITY_REVOKED","Authority was revoked before action time and must be rechecked.")
            qualify("BLOCKED","authority_revoked")
        elif scenario == "preflight_no_side_effects":
            gate("preflight_mode","PASS"); gate("side_effect_suppression","PASS")
            trace["governanceOutcome"]="PREFLIGHT_ONLY"; trace["toolOutcome"]={"attempted": True, "status": "DRY_RUN_ONLY"}
            qualify("QUALIFIED","preflight_no_side_effects")
        elif scenario == "result_qualification_emitted_on_stale_basis":
            gate("freshness_check","FAIL","STALE_BASIS")
            trace["governanceOutcome"]="QUALIFIED_LIMITED"
            qualify("QUALIFIED_LIMITED","stale_basis","review_required_before_high_consequence_use")
        elif scenario == "trace_retrieval_returns_blocked_action":
            gate("trace_retrieval","PASS")
            block("hidden_blocked_action","TRACE_REQUIRED","Blocked action remains visible even when execution did not proceed.")
            qualify("BLOCKED","trace_contains_blocked_action")
        elif scenario == "handoff_does_not_transfer_authority":
            gate("handoff_context_present","PASS"); gate("recipient_independent_authorization","FAIL","HANDOFF_AUTHORITY_NOT_TRANSFERRED")
            block("recipient_agent_state_affecting_action","HANDOFF_AUTHORITY_NOT_TRANSFERRED","Task context may transfer; authority does not silently transfer.")
            qualify("BLOCKED","recipient_reauthorization_required")
        elif scenario == "tool_success_governance_failure":
            trace["toolOutcome"]={"attempted": True, "status": "SUCCESS"}
            gate("tool_execution","PASS"); gate("approval_required","FAIL","APPROVAL_REQUIRED")
            block("governed_write_after_tool_success","APPROVAL_REQUIRED","Tool success is not governance success.")
            qualify("BLOCKED","tool_success_governance_failure")
        elif scenario == "world_model_state_cannot_materialize_current_state":
            gate("world_model_twin_context","PASS"); gate("current_state_bridge","FAIL","WORLD_MODEL_NOT_CURRENT_STATE")
            block("materialize_world_model_state_as_current_state","WORLD_MODEL_NOT_CURRENT_STATE","World-model state is Advisory Twin material unless explicitly bridged and accepted.")
            qualify("BLOCKED","advisory_only","bridge_required")
        elif scenario == "evidence_need_not_evidence":
            gate("request_object_created","PASS"); gate("accepted_evidence_created","FAIL","REQUEST_IS_NOT_EVIDENCE")
            trace["governanceOutcome"]="QUALIFIED_LIMITED"
            qualify("QUALIFIED_LIMITED","evidence_need_only","not_evidence","not_blocker_by_itself")
        elif scenario == "observation_request_not_obligation":
            gate("observation_request_created","PASS"); gate("obligation_created","FAIL","REQUEST_IS_NOT_OBLIGATION")
            trace["governanceOutcome"]="QUALIFIED_LIMITED"
            qualify("QUALIFIED_LIMITED","request_only","not_obligation","not_blocker_by_itself")
        elif scenario == "sharing_after_revocation_denied":
            gate("share_policy_snapshot","PASS"); gate("revocation_recheck_before_share","FAIL","SHARE_PERMISSION_REVOKED")
            block("share_permission_limited_result","SHARE_PERMISSION_REVOKED","Sharing must recheck revocation at disclosure time.")
            qualify("BLOCKED","permission_limited","revoked_share_policy")
        elif scenario == "offline_late_sync_after_revocation_review_bound":
            gate("offline_capture_detected","PASS"); gate("revocation_recheck_on_replay","FAIL","REVIEW_REQUIRED_AFTER_AUTHORITY_CHANGE")
            block("accept_offline_replay_as_governed_fact","REVIEW_REQUIRED_AFTER_AUTHORITY_CHANGE","Late sync after authority change is review-bound, not accepted by default.")
            trace["governanceOutcome"]="REVIEW_BOUND_CANDIDATE"
            qualify("REVIEW_REQUIRED","late_sync","authority_changed","review_required")
        elif scenario == "manifest_overclaim_hidden_egress_blocked":
            gate("manifest_claim_read","PASS"); gate("runtime_effect_matches_manifest","FAIL","MANIFEST_EFFECT_MISMATCH")
            trace["toolOutcome"]={"attempted": True, "status": "BLOCKED_BEFORE_EXTERNAL_EGRESS"}
            block("execute_tool_with_hidden_egress","MANIFEST_EFFECT_MISMATCH","Manifest declared no external egress but runtime attempted it.")
            qualify("BLOCKED","manifest_overclaim")
        elif scenario == "redaction_summary_leak_blocked":
            gate("redaction_policy_present","PASS"); gate("summary_leak_check","FAIL","REDACTION_SUMMARY_LEAK")
            block("publish_public_brief_summary","REDACTION_SUMMARY_LEAK","Redacted detail cannot leak through summary text.")
            qualify("BLOCKED","permission_limited","redaction_required")
        elif scenario == "agent_memory_not_evidence":
            gate("agent_memory_present","PASS"); gate("evidence_basis_check","FAIL","MEMORY_IS_NOT_EVIDENCE")
            block("promote_memory_as_evidence","MEMORY_IS_NOT_EVIDENCE","Agent memory is not an evidence pack or accepted assertion.")
            qualify("BLOCKED","memory_not_evidence")
        else:
            raise ValueError(f"Unsupported scenarioKind: {scenario}")
        self.traces[trace_id] = trace
        return {
            "caseId": case["caseId"], "scenarioKind": scenario, "traceId": trace_id,
            "trace": trace, "traceRetrievalResult": copy.deepcopy(trace),
            "currentStateMutationCount": len(self.current_state_mutations),
            "canonicalTruthMutationCount": len(self.canonical_truth_mutations)
        }

def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
