"""Offline entry points for the non-default complete typed AssertionRecord draft."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST_SHA256 = "49c57b9c593510400afa393c9a9a75dd73a15b5ec152ad3ffa973d9f5c6e1d78"


def file_hash(raw):
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON member: " + key)
        result[key] = value
    return result


class Package:
    def __init__(self):
        self.manifest = (HERE / "package-manifest.json").read_bytes()
        if file_hash(self.manifest) != MANIFEST_SHA256:
            raise ValueError("Package manifest digest mismatch")
        members = json.loads(self.manifest, object_pairs_hook=unique_object)["members"]
        self.members = {item["path"]: item for item in members}
        if len(self.members) != len(members):
            raise ValueError("Duplicate package member")

    def source(self, member, external=None):
        row = self.members[member]
        if "external" in row:
            if external is None:
                raise ValueError("External owner package required: " + member)
            return external / row["external"]
        return ROOT / row["source"] if "source" in row else HERE / "implementation" / member

    def read(self, member, external=None):
        row = self.members[member]
        raw = self.source(member, external).read_bytes()
        if len(raw) != row["byteLength"] or file_hash(raw) != row["rawSha256"]:
            raise ValueError("Package file digest mismatch: " + member)
        return raw

    def stage(self, worker, external):
        worker.mkdir()
        for member in self.members:
            target = worker / member
            target.parent.mkdir(exist_ok=True, parents=True)
            target.write_bytes(self.read(member, external))
        (worker / "candidate-manifest.json").write_bytes(self.manifest)


def contract_references():
    """Return reproducible candidate references for a reviewer with this checkout."""
    pkg = Package()
    separate_sources = {}
    for member, item in pkg.members.items():
        if "external" in item:
            separate_sources[item["external"]] = item["rawSha256"]
        else:
            pkg.read(member)
    checker = runpy.run_path(str(pkg.source("contract_refs.py")))
    report = checker["verify_references"](pkg.read)
    report["contractPath"] = pkg.source("domain-contract.json").relative_to(ROOT).as_posix()
    report["externalSourceFilePins"] = separate_sources
    for entry in report["schemaFiles"].values():
        entry["path"] = pkg.source(entry.pop("member")).relative_to(ROOT).as_posix()
    report["verifier"] = {
        "entryPoint": Path(__file__).resolve().relative_to(ROOT).as_posix() + ":verify_domain",
        "manifestPath": (HERE / "package-manifest.json").relative_to(ROOT).as_posix(),
        "manifestRawSha256": MANIFEST_SHA256,
        "entryPointFileSha256": file_hash(Path(__file__).read_bytes()),
    }
    return report


def unavailable(reason):
    return {"status": "UNAVAILABLE", "error": str(reason), "payload": None}


def _evaluate(intent_bytes, result_bytes, package, owner_inputs, *, encoded=False):
    required = {"externalRoot", "selectedAction"}
    if not isinstance(package, dict) or not required <= set(package) <= required | {"evaluationSelectionRawSha256"}:
        return unavailable("Supply externalRoot, selectedAction and the optional independent evaluation selection pin.")
    try:
        external = Path(package["externalRoot"]).resolve(strict=True)
        if not external.is_dir():
            raise ValueError("The selected external package directory is missing.")
        pkg = Package()
        with tempfile.TemporaryDirectory(prefix="ofarm-domain-") as tmp:
            workspace = Path(tmp).resolve()
            worker = workspace / "worker"
            pkg.stage(worker, external)
            (workspace / "external").symlink_to(external, target_is_directory=True)
            # Only verified project code is loaded here. The existing transport verifies
            # the selected interpreter and all five external packages before invocation.
            transport = runpy.run_path(str(worker / "owner_calls.py"))
            selected = {"root": str(worker), "manifestRawSha256": MANIFEST_SHA256,
                        "selectedAction": package["selectedAction"]}
            if "evaluationSelectionRawSha256" in package:
                selected["evaluationSelectionRawSha256"] = package["evaluationSelectionRawSha256"]
            if encoded:
                owner_inputs = transport["decode"](owner_inputs)
            outcome = transport["evaluate_domain"](intent_bytes, result_bytes, package=selected, owner_inputs=owner_inputs)
        if outcome["status"] == "DOMAIN_REPORT":
            return outcome["domainReport"]
        return unavailable({"status": outcome["status"], "detail": outcome.get("error")})
    except (OSError, ValueError, TypeError, KeyError) as error:
        return unavailable(error)


def verify_domain(intent_bytes, result_bytes, *, package, owner_inputs):
    """Evaluate original byte strings. Owner inputs use the domain owner's Python bytes API."""
    return _evaluate(intent_bytes, result_bytes, package, owner_inputs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("references", help="Reproduce draft contract, schema and verifier references")
    verify = commands.add_parser("verify", help="Evaluate original claim and evidence bytes offline")
    verify.add_argument("--intent", type=Path, required=True)
    verify.add_argument("--result", type=Path, required=True)
    verify.add_argument("--external", type=Path, required=True)
    verify.add_argument("--action", choices=["ASSERT_STRUCTURE", "ASSERT_OPERATION_CLAIM", "ASSERT_COMPLIANCE"], required=True)
    verify.add_argument("--owner-inputs", type=Path, required=True)
    verify.add_argument("--evaluation-selection-sha256")
    args = parser.parse_args()
    try:
        if args.operation == "references":
            report = contract_references()
        else:
            package = {"externalRoot": args.external, "selectedAction": args.action}
            if args.evaluation_selection_sha256 is not None:
                package["evaluationSelectionRawSha256"] = args.evaluation_selection_sha256
            encoded_inputs = json.loads(args.owner_inputs.read_bytes(), object_pairs_hook=unique_object)
            report = _evaluate(args.intent.read_bytes(), args.result.read_bytes(), package, encoded_inputs, encoded=True)
    except (OSError, ValueError, KeyError, ImportError) as error:
        report = unavailable(error)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False))
    if report["status"] in {"DRAFT_REFERENCES_REPRODUCED", "CONDITIONAL_CONFORMANCE_PASS"}:
        return 0
    return 1 if report["status"] == "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
