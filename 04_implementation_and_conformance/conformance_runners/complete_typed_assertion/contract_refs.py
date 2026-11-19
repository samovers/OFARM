"""Reproduce the domain-owned contract and schema references offline."""
from hashlib import sha256
import json
from typing import NamedTuple
from urllib.parse import urldefrag

import rfc8785


class Branch(NamedTuple):
    profile: str
    body: str
    effect_kind: str
    assertion_type: str
    commit_label: str
    commit_token: str


# The three action rows in the submission contract (#23, section 7.2).
BRANCHES = {
    "ASSERT_STRUCTURE": Branch("structure", "structureAssertionBody", "STRUCTURE_ASSERTION",
                               "STRUCTURE_ASSERTION", "structure assertion", "STRUCTURE_ASSERTION"),
    "ASSERT_OPERATION_CLAIM": Branch("operation", "operationClaimBody", "OPERATION_ASSERTION",
                                     "OPERATION_CLAIM_ASSERTION", "operation claim", "OPERATION_CLAIM"),
    "ASSERT_COMPLIANCE": Branch("compliance", "complianceAssertionBody", "COMPLIANCE_ASSERTION",
                                "COMPLIANCE_ASSERTION", "compliance assertion", "COMPLIANCE_ASSERTION"),
}
RESULT = "outer/carriers/result.schema.json"
PAYLOAD = "schemas/payload.schema.json"
TRACE = "source-contracts/ProtectedEffectValidationTrace.schema.json"
OLD_SOURCES = "components/revision-02/sources/OFARM/2110f6d78451/03_machine_contracts/"
LEGACY_RESULT = OLD_SOURCES + "drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json"
LEGACY_INTENT = "source-contracts/OperationAssertionEffectIntent.schema.json"
SCHEMA_MEMBERS = (
    RESULT, PAYLOAD, TRACE, "schemas/immutable-input-closure.schema.json",
    "components/revision-02/proposition.schema.json",
    "components/revision-02/owned-value-types-amendment.schema.json",
    LEGACY_RESULT, LEGACY_INTENT,
    OLD_SOURCES + "schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json",
    OLD_SOURCES + "schemas/event_ingress/OFARM_SemanticEventEnvelope_schema_v0_1.json",
    *("outer/carriers/" + branch.profile + "-intent.schema.json" for branch in BRANCHES.values()),
)


def digest(value):
    return "sha256:" + sha256(rfc8785.dumps(value)).hexdigest()


def pointer(document, fragment):
    if fragment and not fragment.startswith("/"):
        raise ValueError("Unsupported schema fragment: " + fragment)
    for part in fragment.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def refs(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref":
                yield child
            else:
                yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def verify_references(read):
    """read takes a pinned package member name and returns its original bytes."""
    contract_raw = read("domain-contract.json")
    contract = json.loads(contract_raw)
    computed = digest({k: v for k, v in contract.items() if k != "contractDigest"})
    if computed != contract["contractDigest"]:
        raise ValueError("Whole-contract digest mismatch")
    definitions = json.loads(read("domain-definitions.json"))["definitions"]
    if digest({"definitions": definitions}) != contract["definitionRegistryDigest"]:
        raise ValueError("Definition registry digest mismatch")
    graph = json.loads(read("duty-graph.json"))
    if digest(graph) != contract["dutyGraphDigest"]:
        raise ValueError("Duty graph digest mismatch")

    schemas, hashes, members = {}, {}, {}
    for member in SCHEMA_MEMBERS:
        raw = read(member)
        schema = json.loads(raw)
        uri = schema["$id"]
        if uri in schemas:
            raise ValueError("Ambiguous schema identity: " + uri)
        schemas[uri] = schema
        hashes[uri] = "sha256:" + sha256(raw).hexdigest()
        members[uri] = member
    for uri, schema in schemas.items():
        for ref in refs(schema):
            target, fragment = urldefrag(ref)
            pointer(schemas[target or uri], fragment)

    def check_binding(binding, member, fragment=""):
        uri, actual = urldefrag(binding["schemaRef"])
        if (members[uri] != member or hashes[uri] != binding["schemaDigest"]
                or actual != fragment or binding["canonicalization"] != "JCS_RFC8785_SHA256"):
            raise ValueError("Mismatched schema binding: " + binding["schemaRef"])
        target = pointer(schemas[uri], actual)
        if not actual and "$ref" in target:
            target = pointer(target, urldefrag(target["$ref"]).fragment)
        key = "claimLanguageRevision" if actual else "schemaVersion"
        if target["properties"][key]["const"] != binding["schemaVersion"]:
            raise ValueError("Mismatched schema version: " + binding["schemaRef"])
        return target

    result_schema = check_binding(contract["resultSchemaBinding"], RESULT)
    check_binding(contract["payloadSchemaBinding"], PAYLOAD)
    if set(contract["actions"]) != set(BRANCHES):
        raise ValueError("Incomplete action set")
    for action, branch in BRANCHES.items():
        row = contract["actions"][action]
        intent_schema = check_binding(row["intentSchemaBinding"], "outer/carriers/" + branch.profile + "-intent.schema.json")
        check_binding(row["bodySchemaBinding"], RESULT, "/$defs/" + branch.body)
        intent_properties = intent_schema["properties"]
        if intent_properties["assertionBody"]["$ref"] != row["bodySchemaBinding"]["schemaRef"]:
            raise ValueError("Intent selects a different body: " + action)
        result_bodies = [rule["then"]["properties"]["assertionBody"]["$ref"]
                         for rule in result_schema["allOf"]
                         if rule["if"]["properties"].get("assertionType") == {"const": branch.assertion_type}]
        if result_bodies != ["#/$defs/" + branch.body]:
            raise ValueError("Result selects a different body: " + action)
        subject = intent_properties["effectSubject"]["properties"]
        constants = {
            "intent.schemaVersion": intent_properties["schemaVersion"]["const"],
            "result.schemaVersion": result_schema["properties"]["schemaVersion"]["const"],
            "intent.effectKind": subject["subjectKind"]["const"],
            "intent.effectPosture": subject["existencePosture"]["const"],
            "result.assertionType": branch.assertion_type,
            "result.pending": result_schema["properties"]["claimState"]["const"],
        }
        if (constants != row["predicateConstants"] or constants["intent.effectKind"] != branch.effect_kind
                or constants["intent.effectPosture"] != "PROSPECTIVE_TARGET_ALLOWED"
                or constants["result.pending"] != "PENDING_REVIEW"):
            raise ValueError("Mismatched action predicates: " + action)
        if row["recordCommitClass"] != {"constitutionalLabel": branch.commit_label, "serializationToken": branch.commit_token}:
            raise ValueError("Mismatched record commit class: " + action)
    trace_uri = next(uri for uri, member in members.items() if member == TRACE)
    return {
        "status": "DRAFT_REFERENCES_REPRODUCED",
        "implementationCompleteness": contract["implementationCompleteness"],
        "contractId": contract["contractId"], "contractVersion": contract["contractVersion"],
        "contractRef": contract["contractRef"], "contractDigest": computed,
        "contractFileSha256": sha256(contract_raw).hexdigest(),
        "definitionRegistryDigest": contract["definitionRegistryDigest"], "dutyGraphDigest": contract["dutyGraphDigest"],
        "actions": contract["actions"], "resultSchemaBinding": contract["resultSchemaBinding"],
        "payloadSchemaBinding": contract["payloadSchemaBinding"],
        "traceSchemaBinding": {
            "schemaRef": trace_uri, "schemaVersion": schemas[trace_uri]["properties"]["schemaVersion"]["const"],
            "schemaDigest": hashes[trace_uri],
        },
        "schemaFiles": {uri: {"member": member, "rawSha256": hashes[uri][7:]} for uri, member in members.items()},
    }
