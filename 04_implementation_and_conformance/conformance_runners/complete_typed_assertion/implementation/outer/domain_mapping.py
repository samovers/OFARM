"""Pure domain-owned projection and copy predicates for the complete evaluator.

These functions do not resolve records, admit evidence or issue a domain verdict.
The public evaluator must validate the selected schemas and owner interfaces and
account for all 49 duties. Copy facts never substitute for those obligations.
"""
from __future__ import annotations

import copy
import hashlib

import rfc8785

LANGUAGE = "ofarm.complete-typed-claims.v0.1"
RESULT_VERSION = "ofarm.assertionrecord.typed.v0.1"
BRANCHES = {
    "ASSERT_STRUCTURE": ("structure", "STRUCTURE_ASSERTION", "STRUCTURE_ASSERTION"),
    "ASSERT_OPERATION_CLAIM": ("operation", "OPERATION_ASSERTION", "OPERATION_CLAIM_ASSERTION"),
    "ASSERT_COMPLIANCE": ("compliance", "COMPLIANCE_ASSERTION", "COMPLIANCE_ASSERTION"),
}
COMMON_BODY = {"assertionPosture", "claimText", "claimLanguageRevision", "proposition", "contextBindings"}
OP_BODY = {"temporalBasis", "temporalQualifications", "allegesSoftwareAgentPerformance", "performedByBinding", "interventionIntentPayloadBindings", "executionRecordPayloadBindings"}
COMMON_OPTIONAL = ["subjectScopeProofBindings", "supersedesAssertionRecordBinding"]
OP_OPTIONAL = ["softwareAgentActorshipBindings", "performerAuthorityEvidenceBindings"]


class ProjectionError(ValueError):
    def __init__(self, code, pointer):
        super().__init__(code)
        self.code, self.pointer = code, pointer


def canonical(value):
    return rfc8785.dumps(value)


def value_digest(value):
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def same(left, right):
    # JSON booleans cannot equal numeric one or zero through Python coercion.
    return canonical(left) == canonical(right)


def selected(value, pointer):
    current = value
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and str(int(token)) == token and int(token) < len(current):
            current = current[int(token)]
        else:
            return False, None
    return True, current


def _project(intent, selected_action, reads=None):
    """Project a schema-valid intent without accepting or rewriting its body.

    The package selects the action. The complete evaluator checks all remaining
    owner and branch predicates independently, including content copied to the
    result. Only exact submission-act and event-association roles are excluded.
    """
    def observe(path, kind="VALUE"):
        if reads is not None:
            present, value = selected(intent, path)
            reads.append({"pointer": path, "kind": kind, "present": present,
                          **({"valueDigest": value_digest(value)} if present else {})})

    if selected_action not in BRANCHES:
        raise ProjectionError("UNKNOWN_SELECTED_ACTION", "/selectedAction")
    observe("", "OBJECT_TYPE")
    if isinstance(intent, dict):
        observe("/assertionBody", "OBJECT_TYPE")
    if not isinstance(intent, dict) or not isinstance(intent.get("assertionBody"), dict):
        raise ProjectionError("BODY_OBJECT_REQUIRED", "/assertionBody")
    body = intent["assertionBody"]
    allowed = COMMON_BODY | (OP_BODY if selected_action == "ASSERT_OPERATION_CLAIM" else {"applicability"})
    observe("/assertionBody", "OBJECT_KEYS")
    if set(body) - allowed:
        raise ProjectionError("UNKNOWN_BODY_MEMBER", "/assertionBody")
    observe("/assertionBody/claimLanguageRevision")
    if body.get("claimLanguageRevision") != LANGUAGE:
        raise ProjectionError("UNKNOWN_CLAIM_LANGUAGE", "/assertionBody/claimLanguageRevision")

    def need(value, pointer):
        observe(("/assertionBody" if value is body else "") + pointer)
        present, result = selected(value, pointer)
        if not present:
            raise ProjectionError("REQUIRED_PROJECTION_INPUT_MISSING", pointer)
        return copy.deepcopy(result)

    p = {
        "candidateGrammar": LANGUAGE, "selectedAction": selected_action,
        "subject": need(intent, "/subject"),
        "soleAuthorityAnchor": need(intent, "/resources/0/scope"),
        "assertionPosture": need(body, "/assertionPosture"),
        "subjectTime": need(intent, "/subjectTime"),
        "proposition": need(body, "/proposition"),
        "evidenceBindings": need(intent, "/evidenceBindings"),
        "claimState": "PENDING_REVIEW",
    }
    for key in COMMON_OPTIONAL:
        observe("/" + key, "FIELD_PRESENCE")
        if key in intent:
            observe("/" + key)
            p[key] = copy.deepcopy(intent[key])
    observe("/assertionBody/contextBindings", "FIELD_PRESENCE")
    if "contextBindings" in body:
        observe("/assertionBody/contextBindings")
        p["contextBindings"] = copy.deepcopy(body["contextBindings"])
    if selected_action == "ASSERT_OPERATION_CLAIM":
        p["claimPosture"] = need(intent, "/claimPosture")
        p["performedBy"] = need(body, "/performedByBinding")
        for key in ["allegesSoftwareAgentPerformance", "temporalBasis"]:
            p[key] = need(body, "/" + key)
        for key in OP_OPTIONAL:
            observe("/" + key, "FIELD_PRESENCE")
            if key in intent:
                observe("/" + key)
                p[key] = copy.deepcopy(intent[key])
        for key in ["temporalQualifications", "interventionIntentPayloadBindings", "executionRecordPayloadBindings"]:
            observe("/assertionBody/" + key, "FIELD_PRESENCE")
            if key in body:
                observe("/assertionBody/" + key)
                p[key] = copy.deepcopy(body[key])
    else:
        if not same(need(body, "/applicability"), p["subjectTime"]):
            raise ProjectionError("BODY_APPLICABILITY_TIME_MISMATCH", "/assertionBody/applicability")
        if selected_action == "ASSERT_COMPLIANCE":
            for key in ["ruleRevisionBindings", "evidencePolicyRevisionBindings"]:
                p[key] = need(intent, "/" + key)
    return p


def project(intent, selected_action):
    return _project(intent, selected_action)


def project_traced(intent, selected_action):
    """Observe the same projection core; derived text is never an original."""
    reads = []
    try:
        projected = _project(intent, selected_action, reads)
    except ProjectionError as exc:
        return {"status": "PROJECTION_ERROR", "reads": reads,
                "error": {"code": exc.code, "pointer": exc.pointer}, "projection": None}
    return {"status": "RETURNED", "reads": reads, "projection": projected}


def render(intent, selected_action):
    return "Pending claim: " + canonical(project(intent, selected_action)).decode("utf-8") + "."


def copy_facts(intent, result, selected_action):
    """Return all independent copy facts; this never returns AR/PC PASS.

    Invalid input shape may produce several false facts instead of suppressing
    a contradiction behind a missing unrelated value. Semantic and source-owner
    obligations are evaluated by their own contract predicates.
    """
    if selected_action not in BRANCHES:
        raise ProjectionError("UNKNOWN_SELECTED_ACTION", "/selectedAction")
    branch, effect_kind, assertion_type = BRANCHES[selected_action]
    facts = []

    def compare(identifier, source, source_pointer, destination, destination_pointer, optional=False):
        sp, sv = selected(source, source_pointer)
        dp, dv = selected(destination, destination_pointer)
        equal = sp == dp and (not sp or same(sv, dv)) and (optional or sp)
        row = {"predicateId": identifier, "sourcePointer": source_pointer, "destinationPointer": destination_pointer,
               "sourcePresent": sp, "destinationPresent": dp, "equal": bool(equal)}
        if sp:
            row["sourceValueDigest"] = value_digest(sv)
        if dp:
            row["destinationValueDigest"] = value_digest(dv)
        facts.append(row)

    def fixed(identifier, expected, document, destination):
        compare(identifier, {"selectedConstant": expected}, "/selectedConstant", document, destination)

    fixed("intent.schemaVersion", "ofarm." + branch + "assertioneffectintent.typed.v0.1", intent, "/schemaVersion")
    fixed("result.schemaVersion", RESULT_VERSION, result, "/schemaVersion")
    fixed("intent.effectKind", effect_kind, intent, "/effectSubject/subjectKind")
    fixed("intent.effectPosture", "PROSPECTIVE_TARGET_ALLOWED", intent, "/effectSubject/existencePosture")
    fixed("result.assertionType", assertion_type, result, "/assertionType")
    fixed("result.pending", "PENDING_REVIEW", result, "/claimState")
    compare("mapping.id", intent, "/effectSubject/subjectRef", result, "/assertionRecordId")
    compare("mapping.scope", intent, "/resources/0/scope", result, "/anchorScopes/0")
    for key in ["subject", "assertedAt", "assertionActPosture", "subjectTime", "assertionBody", "evidenceBindings"]:
        compare("mapping." + key, intent, "/" + key, result, "/" + key)
    for key in ["assertionActEvidenceBinding", "subjectScopeProofBindings", "supersedesAssertionRecordBinding"]:
        compare("mapping." + key, intent, "/" + key, result, "/" + key, True)
    if selected_action == "ASSERT_OPERATION_CLAIM":
        for key in ["claimPosture", "performedByPartyRef"]:
            compare("mapping." + key, intent, "/" + key, result, "/operationClaimContext/" + key)
        for key in OP_OPTIONAL:
            compare("mapping." + key, intent, "/" + key, result, "/operationClaimContext/" + key, True)
        compare("body.performerRef", intent, "/performedByPartyRef", intent, "/assertionBody/performedByBinding/ref")
    elif selected_action == "ASSERT_COMPLIANCE":
        for key in ["ruleRevisionBindings", "evidencePolicyRevisionBindings"]:
            compare("mapping." + key, intent, "/" + key, result, "/complianceBasis/" + key)
    if selected_action != "ASSERT_OPERATION_CLAIM":
        compare("body.applicability", intent, "/subjectTime", intent, "/assertionBody/applicability")
    return facts
