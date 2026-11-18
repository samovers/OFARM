"""Compare a domain-derived #51 obligation set with original owner artifacts.

This is a conditional technical comparison, not a source-admission or runtime
protection decision. ``expected`` must be derived independently from the full
domain requirement/use graph. The offered owner context, proof, snapshot and
report may never create or shorten that expected set.

This module has no foreign-owner imports and does not invoke an owner checker.
The caller must first verify the exact selected #51 package and report transport.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping

from strict_inputs import digest


HEX = re.compile(r"[0-9a-f]{64}\Z")
EXPECTED_FIELDS = {"status", "artifactPins", "identities", "reads", "negativeReads",
                   "setReads", "writes"}
IDENTITY_FIELDS = {"actionClass", "storageOwnerRef", "transactionAttemptId",
                   "atomicPersistenceBoundaryRef", "proposedAssertionId"}
PIN_FIELDS = {"contextRawSha256", "policyRawSha256", "proofRawSha256",
              "snapshotRawSha256"}


def _exact(left, right):
    """JSON equality without Python's bool/int equality or unordered arrays."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_exact(v, right[k]) for k, v in left.items())
    if isinstance(left, list):
        return len(left) == len(right) and all(_exact(a, b) for a, b in zip(left, right))
    return left == right


def _strict_json(raw):
    if type(raw) is not bytes:
        raise ValueError("Original artifact must be bytes.")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON member: " + key)
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError("Non-finite JSON value: " + value)

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                       parse_constant=nonfinite)
    if type(value) is not dict:
        raise ValueError("Original artifact must be a JSON object.")
    return value


def _mode(row):
    if type(row) is not dict:
        return row
    value = dict(row)
    value["digestMode"] = value.get("digestMode", "JCS_JSON")
    return value


def _without(row, *fields):
    return {key: value for key, value in row.items() if key not in fields}


def _index(rows, label, errors):
    if type(rows) is not list:
        errors.append({"code": "INVALID_ROWS", "path": label})
        return {}
    result = {}
    for position, row in enumerate(rows):
        if type(row) is not dict or type(row.get("key")) is not str or not row["key"]:
            errors.append({"code": "INVALID_ROW_KEY", "path": label + "/" + str(position)})
            continue
        key = row["key"]
        if key in result:
            errors.append({"code": "DUPLICATE_ROW_KEY", "path": label, "key": key})
        result[key] = row
    return result


def _result(status, checks, errors, expected_status, owner_status=None,
            obligation_digest=None, artifact_pins=None, owner_report_digest=None,
            identity_digest=None, identities=None):
    return {"status": status, "comparisonScope": "CONDITIONAL_TECHNICAL_ONLY",
            "expectedDerivationStatus": expected_status, "ownerStatus": owner_status,
            "sourceAdmission": "NOT_ESTABLISHED", "runtimeProtection": "NOT_ESTABLISHED",
            "comparisons": checks, "errors": errors,
            **({"expectedObligationDigest": obligation_digest,
                "expectedIdentities": identities,
                "expectedIdentityDigest": identity_digest,
                "artifactPins": artifact_pins,
                "ownerReportWholeJcsDigest": owner_report_digest}
               if status == "PASS" and obligation_digest is not None and identity_digest is not None else {})}


def _obligation_digest(expected):
    """Bind the four independently derived obligation sets without row order noise."""
    return digest({name: sorted(expected[name], key=lambda row: row["key"])
                   if name != "writes" else expected[name]
                   for name in ("reads", "negativeReads", "setReads", "writes")})


def compare(expected, *, context_bytes, policy_bytes, proof_bytes,
            snapshot_bytes, owner_report):
    """Return PASS, FAIL or NOT_EVALUATED with exact, granular comparisons.

    ``expected`` has status COMPLETE or PARTIAL; exact independent context,
    guard-policy, proof and snapshot raw-SHA pins; independent
    action/owner/attempt/boundary/proposed-ID values; and four separate lists:
    reads, negativeReads, setReads and writes. Their
    rows use the exact #51 context/proof shapes. COMPLETE compares every key
    and requires one exact AssertionRecord INSERT plus its absence guard.
    PARTIAL compares known rows but cannot pass; unknown offered rows remain
    unassessed, and contradictions among known rows still fail.

    A passing returned owner report is required, but never substitutes for
    expected obligations. Its readBindings are compared as returned facts;
    negative, set and write obligations are compared through the original
    context, proof and snapshot because readBindings do not contain them.
    Only PASS returns a digest and detached copy of the independently supplied
    identity vector; that binding grants no source admission or runtime claim.
    """
    checks, errors = [], []
    if type(expected) is not dict or set(expected) not in (EXPECTED_FIELDS, EXPECTED_FIELDS | {"reason"}):
        return _result("NOT_EVALUATED", checks, [{"code": "EXPECTED_SET_UNAVAILABLE", "path": "/expected"}], None)
    status = expected.get("status")
    if status not in ("COMPLETE", "PARTIAL") or status == "PARTIAL" and not expected.get("reason"):
        return _result("NOT_EVALUATED", checks, [{"code": "EXPECTED_DERIVATION_UNAVAILABLE", "path": "/expected/status"}], status)
    pins, identity = expected["artifactPins"], expected["identities"]
    if (type(pins) is not dict or set(pins) != PIN_FIELDS
            or any(type(value) is not str or HEX.fullmatch(value) is None for value in pins.values())
            or type(identity) is not dict or set(identity) != IDENTITY_FIELDS
            or any(type(value) is not str or not value for value in identity.values())
            or any(type(expected[name]) is not list for name in ("reads", "negativeReads", "setReads", "writes"))):
        return _result("NOT_EVALUATED", checks, [{"code": "EXPECTED_SET_INVALID", "path": "/expected"}], status)
    if status == "COMPLETE" and (not expected["reads"] or len(expected["writes"]) != 1):
        return _result("NOT_EVALUATED", checks, [{"code": "EXPECTED_CLOSURE_INCOMPLETE", "path": "/expected"}], status)

    def check(kind, key, code, passed):
        checks.append({"kind": kind, "key": key, "code": code,
                       "disposition": "PASS" if passed else "FAIL"})
        if not passed:
            errors.append({"code": code, "path": "/" + kind + "/" + str(key)})

    artifacts = (("context", context_bytes), ("policy", policy_bytes),
                 ("proof", proof_bytes), ("snapshot", snapshot_bytes))
    parsed, original_digests = {}, {}
    for name, raw in artifacts:
        if type(raw) is not bytes:
            return _result("FAIL", checks, [{"code": "ORIGINAL_BYTES_INVALID", "path": "/" + name}], status)
        check("artifact", name, "ORIGINAL_RAW_PIN_MISMATCH",
              hashlib.sha256(raw).hexdigest() == pins[name + "RawSha256"])
        try:
            parsed[name] = _strict_json(raw)
        except (UnicodeError, ValueError, TypeError, RecursionError) as exc:
            return _result("FAIL", checks, errors + [{"code": "ORIGINAL_JSON_INVALID", "path": "/" + name,
                                                       "detail": str(exc)[:200]}], status)
        try:
            original_digests[name] = digest(parsed[name])
        except (UnicodeError, ValueError, TypeError, RecursionError) as exc:
            return _result("FAIL", checks, errors + [{"code": "ORIGINAL_JCS_INVALID", "path": "/" + name,
                                                       "detail": str(exc)[:200]}], status)
    context, policy, proof, snapshot = (
        parsed[name] for name in ("context", "policy", "proof", "snapshot"))

    def at(document, *path):
        value = document
        for member in path:
            if type(value) is not dict or member not in value:
                return None
            value = value[member]
        return value

    for key, actual in (("actionClass", at(context, "actionClass")),
                        ("storageOwnerRef", at(context, "storageOwnerRef")),
                        ("transactionAttemptId", at(context, "attempt", "transactionAttemptId")),
                        ("atomicPersistenceBoundaryRef", at(context, "attempt", "atomicPersistenceBoundaryRef")),
                        ("proposedAssertionId", at(context, "proposedAssertionId"))):
        check("identity", key, "INDEPENDENT_IDENTITY_MISMATCH", _exact(identity[key], actual))
    for key, actual in (("storageOwnerRef/proof", at(proof, "storageOwnerRef")),
                        ("storageOwnerRef/snapshot", at(snapshot, "storageOwnerRef")),
                        ("storageOwnerRef/policy", at(policy, "storageOwnerRef")),
                        ("transactionAttemptId/proof", at(proof, "transactionAttemptId")),
                        ("transactionAttemptId/snapshot", at(snapshot, "transactionAttemptId")),
                        ("atomicPersistenceBoundaryRef/snapshot", at(snapshot, "atomicPersistenceBoundaryRef")),
                        ("atomicPersistenceBoundaryRef/policy", at(policy, "atomicPersistenceBoundaryRef"))):
        target = identity[key.split("/")[0]]
        check("identity", key, "ORIGINAL_IDENTITY_MISMATCH", _exact(target, actual))
    check("identity", "proofId", "PROOF_ID_MISMATCH", _exact(at(context, "proofId"), at(proof, "proofId")))
    check("identity", "contextBinding", "CONTEXT_BINDING_MISMATCH",
          type(at(context, "contextId")) is str and bool(at(context, "contextId"))
          and _exact(at(proof, "context"),
                     {"ref": at(context, "contextId"), "digest": original_digests["context"]}))
    check("identity", "snapshotBinding", "SNAPSHOT_BINDING_MISMATCH",
          type(at(context, "attempt", "transactionSnapshot")) is dict
          and type(at(proof, "snapshot")) is dict
          and type(at(snapshot, "snapshotId")) is str and bool(at(snapshot, "snapshotId"))
          and _exact(at(context, "attempt", "transactionSnapshot"), at(proof, "snapshot"))
          and _exact(at(proof, "snapshot"),
                     {"ref": at(snapshot, "snapshotId"), "digest": original_digests["snapshot"]}))
    selected_policy_binding = (
        {"ref": at(policy, "policyId"), "digest": original_digests["policy"]}
        if type(at(policy, "policyId")) is str and bool(at(policy, "policyId")) else None)
    check("identity", "guardPolicyBinding", "POLICY_BINDING_MISMATCH",
          selected_policy_binding is not None
          and _exact(at(context, "attempt", "guardPolicyBinding"), selected_policy_binding)
          and _exact(at(proof, "guardPolicy"), selected_policy_binding))
    check("identity", "phase", "PRE_VERDICT_PHASE_MISMATCH",
          at(proof, "phase") == "AFTER_PROPOSED_WRITES_BEFORE_DOMAIN_VERDICT")
    check("identity", "proposedBinding", "PROPOSED_BINDING_ID_MISMATCH",
          _exact(identity["proposedAssertionId"],
                 at(context, "proposedAssertion", "binding", "ref")))

    expected_rows = {}
    original_rows = {}
    row_pairs = (("reads", "requiredReads"), ("negativeReads", "requiredNegativeReads"),
                 ("setReads", "requiredSetReads"))
    for name, source in row_pairs:
        expected_rows[name] = _index(expected[name], "/expected/" + name, errors)
        original_rows[name] = _index(at(context, source), "/context/" + source, errors)
        wanted, offered = set(expected_rows[name]), set(original_rows[name])
        if status == "COMPLETE":
            check(name, "keys", "OBLIGATION_KEY_SET_MISMATCH", wanted == offered)
        else:
            check(name, "known-keys", "KNOWN_OBLIGATION_MISSING", wanted <= offered)

    guards = {
        "reads": _index(at(proof, "readGuards"), "/proof/readGuards", errors),
        "negativeReads": _index(at(proof, "negativeGuards"), "/proof/negativeGuards", errors),
        "setReads": _index(at(proof, "setGuards"), "/proof/setGuards", errors),
    }
    observations = {
        "reads": _index(at(snapshot, "positiveRecords"), "/snapshot/positiveRecords", errors),
        "negativeReads": _index(at(snapshot, "negativeRecords"), "/snapshot/negativeRecords", errors),
        "setReads": _index(at(snapshot, "setRecords"), "/snapshot/setRecords", errors),
    }
    if status == "COMPLETE":
        for name in ("reads", "negativeReads", "setReads"):
            check(name, "guard-keys", "GUARD_KEY_SET_MISMATCH",
                  set(guards[name]) == set(expected_rows[name]))
            observed = ({key for key, row in expected_rows[name].items()
                         if row.get("availability") == "COMMITTED_AT_TRANSACTION_START"}
                        if name == "reads" else set(expected_rows[name]))
            check(name, "snapshot-keys", "SNAPSHOT_KEY_SET_MISMATCH",
                  set(observations[name]) == observed)
    else:
        for name in ("reads", "negativeReads", "setReads"):
            check(name, "known-guard-keys", "KNOWN_GUARD_MISSING",
                  set(expected_rows[name]) <= set(guards[name]))
            observed = ({key for key, row in expected_rows[name].items()
                         if row.get("availability") == "COMMITTED_AT_TRANSACTION_START"}
                        if name == "reads" else set(expected_rows[name]))
            check(name, "known-snapshot-keys", "KNOWN_SNAPSHOT_MISSING",
                  observed <= set(observations[name]))

    report_status = owner_report.get("status") if type(owner_report) is dict else None
    if report_status == "FAIL":
        errors.append({"code": "OWNER_REPORTED_FAILURE", "path": "/ownerReport/status"})
    elif owner_report is not None and report_status not in ("CONDITIONAL_CONFORMANCE_PASS", "INPUT_ERROR", "DEPENDENCY_UNAVAILABLE"):
        errors.append({"code": "OWNER_REPORT_INVALID", "path": "/ownerReport/status"})
    report_facts = owner_report.get("facts", {}) if type(owner_report) is dict else {}
    returned = _index(report_facts.get("readBindings") if type(report_facts) is dict else None,
                      "/ownerReport/facts/readBindings", errors) if report_status == "CONDITIONAL_CONFORMANCE_PASS" else {}
    if report_status == "CONDITIONAL_CONFORMANCE_PASS":
        bindings = owner_report.get("bindings", {})
        returned_checks = owner_report.get("checks")
        check("report", "schema", "OWNER_REPORT_SCHEMA_MISMATCH",
              owner_report.get("schemaVersion") == "ofarm.preVerdictProtectedStateReport.v0.1")
        check("report", "runtime", "OWNER_RUNTIME_PROTECTION_INVALID",
              owner_report.get("runtimeProtection") == "NOT_ESTABLISHED")
        check("report", "later-gate", "OWNER_LATER_TRANSACTION_GATE_INVALID",
              owner_report.get("laterTransactionGate") == "NOT_EVALUATED")
        check("report", "errors", "OWNER_PASS_HAS_ERRORS",
              type(owner_report.get("errors")) is list and not owner_report["errors"])
        check("report", "checks", "OWNER_PASS_CHECKS_INVALID",
              type(returned_checks) is list and bool(returned_checks)
              and all(type(row) is dict and type(row.get("id")) is str and bool(row["id"])
                      and row.get("disposition") == "PASS" for row in returned_checks))
        check("report", "independent-proof-check", "OWNER_PROOF_CHECK_MISSING",
              type(returned_checks) is list
              and any(type(row) is dict and row.get("id") == "INDEPENDENT_PROOF_BINDING"
                      and row.get("disposition") == "PASS" for row in returned_checks))
        check("report", "context", "RETURNED_CONTEXT_BINDING_MISMATCH",
              type(at(bindings, "context")) is dict
              and _exact(at(bindings, "context"), at(proof, "context")))
        check("report", "snapshot", "RETURNED_SNAPSHOT_BINDING_MISMATCH",
              type(at(bindings, "snapshot")) is dict
              and _exact(at(bindings, "snapshot"), at(proof, "snapshot"))
              and _exact(at(report_facts, "snapshotBinding"), at(proof, "snapshot")))
        check("report", "policy", "RETURNED_POLICY_BINDING_MISMATCH",
              type(at(bindings, "guardPolicy")) is dict
              and selected_policy_binding is not None
              and _exact(at(bindings, "guardPolicy"), selected_policy_binding))
        check("report", "proof", "RETURNED_PROOF_BINDING_MISMATCH",
              type(at(bindings, "proof")) is dict
              and type(at(proof, "proofId")) is str and bool(at(proof, "proofId"))
              and _exact(at(bindings, "proof"),
                         {"ref": at(proof, "proofId"), "digest": original_digests["proof"]}))
        check("report", "proposed", "RETURNED_PROPOSED_RESULT_MISMATCH",
              type(at(report_facts, "proposedResult")) is dict
              and _exact(at(report_facts, "proposedResult"), at(context, "proposedAssertion")))
        if status == "COMPLETE":
            check("report", "read-keys", "RETURNED_READ_KEY_SET_MISMATCH",
                  set(returned) == set(expected_rows["reads"]))
        else:
            check("report", "known-read-keys", "KNOWN_RETURNED_READ_MISSING",
                  set(expected_rows["reads"]) <= set(returned))

    read_by_ref = {}
    for key, row in expected_rows["reads"].items():
        context_row, guard, positive = (original_rows["reads"].get(key), guards["reads"].get(key),
                                        observations["reads"].get(key))
        check("read", key, "READ_SELECTION_MISMATCH", _exact(_mode(row), _mode(context_row)))
        if type(row.get("binding")) is not dict or type(row.get("rawSha256")) is not str:
            errors.append({"code": "EXPECTED_READ_INVALID", "path": "/expected/reads/" + key})
            continue
        mode = row.get("digestMode", "JCS_JSON")
        check("read", key, "READ_MODE_INVALID", mode in ("JCS_JSON", "RAW_BYTES")
              and (("digest" not in row["binding"]) if mode == "RAW_BYTES" else ("digest" in row["binding"])))
        check("read", key, "READ_REVISION_CONFLICT",
              "revisionRef" not in row or "revisionRef" not in row["binding"]
              or row["revisionRef"] == row["binding"]["revisionRef"])
        core = _without(_mode(row), "role")
        guard_core = _without(_mode(guard), "snapshotVersion", "observedVersion") if type(guard) is dict else None
        check("read", key, "READ_GUARD_SELECTION_MISMATCH", _exact(core, guard_core))
        availability = row.get("availability")
        if availability == "COMMITTED_AT_TRANSACTION_START":
            snapshot_core = (_without(_mode(positive), "rowVersion", "visibility")
                             if type(positive) is dict else None)
            expected_snapshot_core = _without(core, "availability")
            check("read", key, "READ_SNAPSHOT_SELECTION_MISMATCH",
                  _exact(expected_snapshot_core, snapshot_core) and at(positive, "visibility") == availability)
            check("read", key, "READ_VERSION_MISMATCH",
                  type(guard) is dict and type(positive) is dict
                  and type(guard.get("snapshotVersion")) is str
                  and _exact(positive.get("rowVersion"), guard.get("snapshotVersion"))
                  and _exact(guard.get("snapshotVersion"), guard.get("observedVersion"))
                  and "fixedInputVersion" not in guard)
        elif availability == "FIXED_BEFORE_DOMAIN_VERDICT":
            check("read", key, "FIXED_READ_SNAPSHOT_FORBIDDEN", positive is None)
            check("read", key, "FIXED_READ_VERSION_MISMATCH",
                  type(guard) is dict and type(row.get("fixedInputVersion")) is str
                  and _exact(row["fixedInputVersion"], guard.get("fixedInputVersion"))
                  and _exact(guard.get("fixedInputVersion"), guard.get("observedVersion"))
                  and "snapshotVersion" not in guard)
        else:
            errors.append({"code": "READ_AVAILABILITY_INVALID", "path": "/expected/reads/" + key})
        if report_status == "CONDITIONAL_CONFORMANCE_PASS":
            expected_fact = _mode(row)
            if type(guard) is dict:
                expected_fact = {**expected_fact,
                                 **{field: guard[field] for field in ("snapshotVersion", "observedVersion")
                                    if field in guard}}
            check("read", key, "RETURNED_READ_FACT_MISMATCH",
                  _exact(expected_fact, _mode(returned.get(key))))
        ref = row["binding"].get("ref")
        if type(ref) is str:
            prior = read_by_ref.get(ref)
            selected = (row["binding"], row["rawSha256"], mode, availability,
                        row.get("revisionRef"), row.get("fixedInputVersion"),
                        guard.get("snapshotVersion") if type(guard) is dict else None,
                        guard.get("observedVersion") if type(guard) is dict else None)
            check("read", key, "REPEATED_REF_CONFLICT", prior is None or _exact(prior, selected))
            read_by_ref[ref] = selected

    for name in ("negativeReads", "setReads"):
        for key, row in expected_rows[name].items():
            original, guard, observed = original_rows[name].get(key), guards[name].get(key), observations[name].get(key)
            check(name, key, "GUARDED_PREDICATE_SELECTION_MISMATCH", _exact(row, original))
            guard_core = _without(guard, "snapshotVersion", "observedVersion", "observation") if type(guard) is dict else None
            snapshot_core = _without(observed, "guardVersion", "observation") if type(observed) is dict else None
            check(name, key, "GUARDED_PREDICATE_PROOF_MISMATCH", _exact(row, guard_core))
            check(name, key, "GUARDED_PREDICATE_SNAPSHOT_MISMATCH", _exact(row, snapshot_core))
            check(name, key, "GUARD_VERSION_MISMATCH",
                  type(guard) is dict and type(observed) is dict
                  and type(guard.get("snapshotVersion")) is str
                  and _exact(guard["snapshotVersion"], guard.get("observedVersion"))
                  and _exact(guard["snapshotVersion"], observed.get("guardVersion")))
            if name == "negativeReads":
                check(name, key, "NEGATIVE_OBSERVATION_MISMATCH",
                      at(guard, "observation") == "ABSENT"
                      and at(observed, "observation") == "ABSENT_AT_TRANSACTION_START")
            else:
                members = row.get("members")
                if type(members) is not list:
                    errors.append({"code": "EXPECTED_SET_MEMBERS_INVALID", "path": "/expected/setReads/" + key})
                    continue
                check(name, key, "SET_MEMBERS_NOT_UNIQUE",
                      all(type(v) is dict and type(v.get("ref")) is str for v in members)
                      and len({v["ref"] for v in members}) == len(members))
                for position, member in enumerate(members):
                    ref = member.get("ref") if type(member) is dict else None
                    selected = read_by_ref.get(ref)
                    expected_member = None
                    if selected is not None:
                        binding, raw_sha, mode, availability, _, _, _, _ = selected
                        expected_member = (dict(binding) | {"digestMode": "RAW_BYTES", "rawSha256": raw_sha}
                                           if mode == "RAW_BYTES" else binding)
                        if availability != "COMMITTED_AT_TRANSACTION_START":
                            expected_member = None
                    check(name, key + "/" + str(position), "SET_MEMBER_NOT_COMMITTED_READ",
                          expected_member is not None and _exact(member, expected_member))

    writes = expected["writes"]
    if writes:
        expected_write = writes[0]
        proposed = at(context, "proposedAssertion")
        derived_write = ({"operation": "INSERT", "recordType": "AssertionRecord",
                          "key": identity["proposedAssertionId"], **proposed}
                         if type(proposed) is dict else None)
        check("write", "single", "EXPECTED_INSERT_MISMATCH",
              len(writes) == 1 and _exact(expected_write, derived_write))
        check("write", "proof", "PROPOSED_WRITE_SET_MISMATCH",
              type(at(proof, "proposedDomainWrites")) is list
              and _exact(writes, at(proof, "proposedDomainWrites")))
        check("write", "absence", "ASSERTION_ID_ABSENCE_MISSING",
              len([row for row in expected["negativeReads"]
                   if type(row) is dict and row.get("purpose") == "ASSERTION_ID_ABSENCE"
                   and row.get("key") == identity["proposedAssertionId"]]) == 1)
        check("write", "new-id", "PROPOSED_ID_ALREADY_SELECTED_AS_READ",
              all(type(row) is dict and at(row, "binding", "ref") != identity["proposedAssertionId"]
                  for row in expected["reads"]))
    elif status == "COMPLETE":
        errors.append({"code": "PROPOSED_WRITE_UNAVAILABLE", "path": "/expected/writes"})

    obligation_digest = identity_digest = None
    if status == "COMPLETE" and report_status == "CONDITIONAL_CONFORMANCE_PASS" and not errors:
        try:
            obligation_digest = _obligation_digest(expected)
        except (KeyError, TypeError, ValueError, RecursionError) as exc:
            errors.append({"code": "EXPECTED_OBLIGATION_DIGEST_INVALID", "path": "/expected",
                           "detail": str(exc)[:200]})
        if obligation_digest is not None:
            try:
                identity_digest = digest(identity)
            except (TypeError, ValueError, RecursionError) as exc:
                errors.append({"code": "EXPECTED_IDENTITY_DIGEST_INVALID", "path": "/expected/identities",
                               "detail": str(exc)[:200]})
                obligation_digest = None
    if errors:
        final = "FAIL"
    elif status == "PARTIAL" or report_status != "CONDITIONAL_CONFORMANCE_PASS":
        final = "NOT_EVALUATED"
    else:
        final = "PASS"
    owner_report_digest = None
    if obligation_digest is not None:
        try:
            owner_report_digest = digest(owner_report)
        except (TypeError, ValueError, RecursionError) as exc:
            errors.append({"code": "OWNER_REPORT_DIGEST_INVALID", "path": "/ownerReport",
                           "detail": str(exc)[:200]})
            final = "FAIL"
            obligation_digest = identity_digest = None
    return _result(final, checks, errors, status, report_status, obligation_digest,
                   dict(expected["artifactPins"]) if obligation_digest is not None else None,
                   owner_report_digest, identity_digest,
                   dict(identity) if identity_digest is not None else None)
