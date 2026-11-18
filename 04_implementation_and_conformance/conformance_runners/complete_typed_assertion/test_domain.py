"""Offline conformance checks for the typed draft and the v0.2 handoff."""
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import rfc8785

import contract_refs as refs
import ofarm_assertion_record_domain as api


FIXTURES = api.ROOT / "04_implementation_and_conformance/examples_and_fixtures/fixtures/complete_typed_assertion"
LEGACY_CASES = FIXTURES.parent / "machine_contracts/OFARM_AssertionRecord_submission_cases_v0_2.json"
EVALUATION_SELECTION = "e61a6a30757d4e7962ba940eb5cf2715ef042c5972d2e630c6d1715a250fec7c"
CONTRACT_DIGEST = "sha256:ab41daa1426672b38bf98e6b4358f133b4a97639e26b8847e35116a70ef48e24"
PREVIOUS_DIGEST = "sha256:c568a34f54bc09341ca23e39a96c810f016649debe68c55e2964ba1b399c1029"


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pkg = api.Package()
        cls.receipt = api.contract_references()
        cls.schemas = {p: json.loads(cls.pkg.read(p)) for p in refs.SCHEMA_MEMBERS}
        cls.registry = Registry().with_resources(
            (s["$id"], Resource.from_contents(s)) for s in cls.schemas.values()
        )
        cls.intent = json.loads((FIXTURES / "intent.json").read_bytes())
        cls.result = json.loads((FIXTURES / "result.json").read_bytes())

    def test_independent_contract_and_schema_hashes(self):
        raw = self.pkg.read("domain-contract.json")
        whole = json.loads(raw)
        declared = whole.pop("contractDigest")
        self.assertEqual(declared, CONTRACT_DIGEST)
        self.assertEqual(declared, "sha256:" + hashlib.sha256(rfc8785.dumps(whole)).hexdigest())
        self.assertEqual(declared, self.receipt["contractDigest"])
        self.assertNotEqual(declared, "sha256:" + hashlib.sha256(raw).hexdigest())
        self.assertEqual(3, len(self.receipt["actions"]))
        for uri, source in self.receipt["schemaFiles"].items():
            blob = (api.ROOT / source["path"]).read_bytes()
            self.assertEqual(uri, json.loads(blob)["$id"])
            self.assertEqual(source["rawSha256"], hashlib.sha256(blob).hexdigest())
        registry = json.loads(self.pkg.read("domain-definitions.json"))
        graph = json.loads(self.pkg.read("duty-graph.json"))
        self.assertEqual(len(registry["definitions"]), 99)
        self.assertEqual(len(registry["requirements"]), 42)
        self.assertEqual(len(graph["duties"]), 49)

    def test_nested_change_previous_digest_and_stale_registry_fail(self):
        current = json.loads(self.pkg.read("domain-contract.json"))
        mutations = []
        old = dict(current, contractDigest=PREVIOUS_DIGEST)
        mutations.append((old, "Whole-contract digest mismatch"))
        nested = copy.deepcopy(current)
        nested["actions"]["ASSERT_COMPLIANCE"]["bodySchemaBinding"]["schemaDigest"] = "sha256:" + "0" * 64
        mutations.append((nested, "Whole-contract digest mismatch"))
        stale = dict(current, definitionRegistryDigest="sha256:019ae04537d5a2a0864cbc28325c956b681f9e1b7f120bd824c707313f4830b3")
        stale["contractDigest"] = PREVIOUS_DIGEST
        mutations.append((stale, "Definition registry digest mismatch"))
        wrong_body = copy.deepcopy(current)
        row = wrong_body["actions"]["ASSERT_OPERATION_CLAIM"]
        row["bodySchemaBinding"]["schemaRef"] = wrong_body["actions"]["ASSERT_STRUCTURE"]["bodySchemaBinding"]["schemaRef"]
        wrong_body["contractDigest"] = refs.digest({k: v for k, v in wrong_body.items() if k != "contractDigest"})
        mutations.append((wrong_body, "Mismatched schema binding"))
        for changed, error in mutations:
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                refs.verify_references(lambda path: json.dumps(changed).encode() if path == "domain-contract.json" else self.pkg.read(path))

    def test_fixture_formats_and_forbidden_typed_fields(self):
        def errors(member, value):
            return list(Draft202012Validator(self.schemas[member], registry=self.registry).iter_errors(value))

        typed_intent = "outer/carriers/operation-intent.schema.json"
        self.assertEqual([], errors(typed_intent, self.intent))
        self.assertEqual([], errors(refs.RESULT, self.result))
        legacy = json.loads(LEGACY_CASES.read_bytes())["fixtures"]["PERFORMED_INTERVAL"]["value"]
        self.assertEqual([], errors(refs.LEGACY_RESULT, legacy))
        self.assertTrue(errors(refs.RESULT, legacy))
        typed_fields = {"claimLanguageRevision", "performedByBinding", "proposition"}
        for root, old_schema, old_version in [
            (self.intent, refs.LEGACY_INTENT, "ofarm.operationassertioneffectintent.v0.2"),
            (self.result, refs.LEGACY_RESULT, "ofarm.assertionrecord.v0.2"),
        ]:
            for record in [root, dict(root, schemaVersion=old_version)]:
                found = errors(old_schema, record)
                self.assertTrue(any(e.validator == "additionalProperties"
                                    and list(e.absolute_path) == ["assertionBody"]
                                    and all(key in e.message for key in typed_fields) for e in found))
        self.assertEqual("OPERATION_CLAIM_ASSERTION", self.result["assertionType"])
        self.assertEqual("PENDING_REVIEW", self.result["claimState"])
        for field in typed_fields:
            changed = copy.deepcopy(self.result)
            del changed["assertionBody"][field]
            self.assertTrue(errors(refs.RESULT, changed), field)

    def test_missing_external_package(self):
        report = api.verify_domain(b"{}", b"{}", package={"externalRoot": FIXTURES / "absent",
                                                        "selectedAction": "ASSERT_OPERATION_CLAIM"}, owner_inputs={})
        self.assertEqual("UNAVAILABLE", report["status"])
        self.assertIsNone(report["payload"])

    @unittest.skipUnless(os.environ.get("OFARM_TYPED_EXTERNAL"), "Set OFARM_TYPED_EXTERNAL to run the sealed worker")
    def test_each_branch_consumes_original_protected_state(self):
        external = Path(os.environ["OFARM_TYPED_EXTERNAL"])
        cases = (external / "owners/state/04_implementation_and_conformance/examples_and_fixtures"
                 / "fixtures/preverdict_protected_state_evidence/fixtures/review-repair-02/cases")
        for action in refs.BRANCHES:
            with self.subTest(action=action):
                case = cases / (action.lower() + "-initial")
                inputs = {key + "_bytes": (case / (key + ".json")).read_bytes()
                          for key in ("proof", "context", "policy", "snapshot")}
                context = json.loads(inputs["context_bytes"])
                files = json.loads((case / "records.json").read_bytes())
                records = {ref: (case / path).read_bytes() for ref, path in files.items()}
                inputs.update(records=records, selected=json.loads((case / "selected.json").read_bytes()))
                report = api.verify_domain(records[context["effectIntent"]["binding"]["ref"]],
                                           records[context["proposedAssertion"]["binding"]["ref"]],
                                           package={"externalRoot": external, "selectedAction": action},
                                           owner_inputs={"state": inputs})
                self.assertEqual("CONDITIONAL_CONFORMANCE_PASS", report["ownerReports"]["state"]["status"])
                self.assertEqual((29, 20), (len(report["mappingFindings"]), len(report["postconditionFindings"])))
                self.assertIn(report["status"], {"FAIL", "DEPENDENCY_UNAVAILABLE"})
                self.assertIsNone(report["payload"])

    @unittest.skipUnless(os.environ.get("OFARM_TYPED_EXTERNAL"), "Set OFARM_TYPED_EXTERNAL to run the sealed worker")
    def test_original_bytes_through_callable(self):
        def as_bytes(value):
            if set(value) == {"originalBytesBase64"}:
                return base64.b64decode(value["originalBytesBase64"], validate=True)
            return value

        owners = json.loads((FIXTURES / "owner-inputs.json").read_bytes(), object_hook=as_bytes)
        settings = {"externalRoot": Path(os.environ["OFARM_TYPED_EXTERNAL"]), "selectedAction": "ASSERT_OPERATION_CLAIM",
                    "evaluationSelectionRawSha256": EVALUATION_SELECTION}
        report = api.verify_domain((FIXTURES / "intent.json").read_bytes(), (FIXTURES / "result.json").read_bytes(),
                                   package=settings, owner_inputs=owners)
        self.assertEqual("FAIL", report["status"])
        self.assertEqual((29, 20), (len(report["mappingFindings"]), len(report["postconditionFindings"])))
        findings = report["mappingFindings"] + report["postconditionFindings"]
        self.assertEqual({"AR_EVENT_ASSOCIATION", "PC_INPUTS_IMMUTABLE"},
                         {f["id"] for f in findings if f["disposition"] == "FAIL"})
        self.assertIn("RESOLVED_INPUT_CLOSURE", report["failedDependencyIds"])
        self.assertIsNone(report["payload"])
        forged = api.verify_domain(b"{}", b"{}", package=settings, owner_inputs={"pass": True})
        self.assertEqual("INPUT_ERROR", forged["status"])
        self.assertIsNone(forged["payload"])


if __name__ == "__main__":
    unittest.main()
