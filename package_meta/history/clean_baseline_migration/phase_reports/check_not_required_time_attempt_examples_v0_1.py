"""Fictional #38 arithmetic/evidence examples, NOT a runtime conformance checker.

No clock, database, network or kernel imports. Governed D, trustworthy observations,
original identity, guards and authoritative status are supplied assumptions.
The completion examples illustrate approved owner rules, not their implementation.
"""

from datetime import datetime
import json
from pathlib import Path
import re


DOCUMENT = Path(__file__).with_name(
    "not_required_transaction_time_and_attempt_binding_proposal_v0_1.md"
)
POLICY = {
    "proposalId": "OFARM-ISSUE25-TIME-ATTEMPT-BINDING-001",
    "version": 2,
    "status": "SEMANTIC_REVIEW_NOT_EXECUTABLE",
    "firstConsumer": "ASSERT_OPERATION_CLAIM",
    "transactionBudgetMicros": 30_000_000,
    "cutoff": "EXCLUSIVE",
    "utcStartSource": "PostgreSQL.transaction_timestamp",
    "utcCurrentSource": "PostgreSQL.clock_timestamp",
    "elapsedSource": "Linux.CLOCK_BOOTTIME",
    "elapsedOrigin": "BEFORE_ORIGINAL_BEGIN_DISPATCH",
    "transactionTimeEncoding": "ASSERTION_CONTRACT_6_3_CANONICAL_UTC",
    "supportedUtcPrecision": "WHOLE_MICROSECONDS",
    "writeAuthorizationBoundary": "GUARDED_WRITE_CHECK_V0_1",
    "ordinaryExpiryAfterCheckpoint": "FIXED_ORIGINAL_TRANSACTION_ONLY",
    "attemptTransfer": "FORBIDDEN",
    "withinAttemptDeadlineReset": "FORBIDDEN",
    "lockTimeoutChange": False,
    "sourceWithdrawalEnabled": False,
}


def supported_utc(text):
    """Check spelling/precision examples, without rewriting the supplied bytes."""
    if not isinstance(text, str):
        return False
    match = re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.([0-9]{1,9}))?Z", text
    )
    if not match:
        return False
    fraction = match[1]
    if fraction and (fraction.endswith("0") or len(fraction) > 6):
        return False
    try:
        datetime(int(text[:4]), int(text[5:7]), int(text[8:10]),
                 int(text[11:13]), int(text[14:16]), int(text[17:19]))
    except ValueError:
        return False
    return True


def gate(d_us, utc_us, elapsed_ns, previous_utc_us=0, previous_elapsed_ns=0,
         original_context=True, trusted_observations=True):
    # UTC offsets from fictional 2030-01-01T00:00:00Z; elapsed offsets from
    # ONE fictional pre-BEGIN M0. No caller-supplied real provenance is accepted.
    values = (d_us, utc_us, elapsed_ns, previous_utc_us, previous_elapsed_ns)
    if any(type(value) is not int or value < 0 for value in values):
        return False
    if original_context is not True or trusted_observations is not True:
        return False
    if not 0 < d_us <= POLICY["transactionBudgetMicros"]:
        return False
    if utc_us < previous_utc_us or elapsed_ns < previous_elapsed_ns:
        return False
    elapsed_cutoff = min(POLICY["transactionBudgetMicros"] * 1000, d_us * 1000)
    return utc_us < d_us and elapsed_ns < elapsed_cutoff


def completion(status, checkpoint, t_us=29_000_000, observed_commit_us=None,
               original_context=True, admissible_members=True,
               through_commit_conditions=True, atomic_physical_time=False):
    # Illustrative dispositions only. No post-T expiry recheck or invented time.
    if status == "UNKNOWN":
        return "UNRESOLVED"
    if status == "ROLLED_BACK":
        return "NO_EFFECT_NOT_RETRY_PERMISSION"
    if status == "NOT_DISPATCHED":
        return "CHECKPOINT_ONLY" if checkpoint else "CHECKPOINT_REFUSED"
    assert status == "COMMITTED"
    chronology = observed_commit_us is None or observed_commit_us >= t_us >= 0
    valid = (checkpoint and original_context and admissible_members
             and through_commit_conditions and chronology and not atomic_physical_time)
    return "VERIFIED_SUCCESS" if valid else "QUARANTINED_PARTIAL_SUCCESS"


def main():
    blocks = re.findall(r"```json\n(.*?)\n```", DOCUMENT.read_text(), re.S)
    assert len(blocks) == 1, "one closed policy object required"
    actual = json.dumps(json.loads(blocks[0]), sort_keys=True)
    assert actual == json.dumps(POLICY, sort_keys=True), "candidate policy value or type changed"
    arithmetic = [
        ("ordinary", (30_000_000, 2_000_000, 2_000_000_000), {}, True),
        ("just_before", (30_000_000, 29_999_999, 29_999_999_999), {}, True),
        ("utc_equal", (30_000_000, 30_000_000, 29_999_999_999), {}, False),
        ("elapsed_equal", (30_000_000, 29_999_999, 30_000_000_000), {}, False),
        ("shorter", (5_000_000, 4_999_999, 4_999_999_999), {}, True),
        ("shorter_utc_equal", (5_000_000, 5_000_000, 4_999_999_999), {}, False),
        ("shorter_elapsed_equal", (5_000_000, 1_000_000, 5_000_000_000), {}, False),
        ("binding_wait_included", (30_000_000, 20_000_000, 31_000_000_000), {}, False),
        ("utc_stalled", (30_000_000, 1_000_000, 31_000_000_000), {}, False),
        ("utc_regressed", (30_000_000, 1_000_000, 3_000_000_000), {"previous_utc_us": 2_000_000}, False),
        ("utc_jump", (30_000_000, 31_000_000, 2_000_000_000), {}, False),
        ("represented_suspend", (30_000_000, 29_000_000, 31_000_000_000), {}, False),
        ("before_origin", (30_000_000, 1, -1), {}, False),
        ("elapsed_regressed", (30_000_000, 2, 1000), {"previous_elapsed_ns": 2000}, False),
        ("zero_interval", (0, 0, 0), {}, False),
        ("replaced_context", (30_000_000, 1, 1000), {"original_context": False}, False),
        ("untrusted_readings", (30_000_000, 1, 1000), {"trusted_observations": False}, False),
        ("no_clamping_later_d", (40_000_000, 1, 1000), {}, False),
        ("boolean_deadline", (True, 0, 0), {}, False),
        ("missing_end", (None, 0, 0), {}, False),
        ("float_time", (30_000_000, 0.0, 0), {}, False),
        ("utc_before_start", (30_000_000, -1, 0), {}, False),
    ]
    for name, args, kwargs, expected in arithmetic:
        assert gate(*args, **kwargs) is expected, name
    grid_checks = 0
    for d in (1, 2_000_000, 5_000_000, 30_000_000):
        for u in (0, d - 1, d, d + 1):
            ordered = (0, d * 1000 - 1, d * 1000, d * 1000 + 1, 31_000_000_000)
            readings = [gate(d, u, m) for m in ordered]
            assert readings == sorted(readings, reverse=True), (d, u)
            grid_checks += 1
    spellings = [
        ("2030-01-01T00:00:00Z", True),
        ("2030-01-01T00:00:00.12Z", True),
        ("2030-01-01T00:00:00.000001Z", True),
        ("2030-01-01T00:00:00.120000Z", False),
        ("2030-01-01T00:00:00.0Z", False),
        ("2030-01-01T00:00:00.1234567Z", False),
        ("2030-01-01T00:00:00+00:00", False),
        ("2030-01-01T00:00:00z", False),
        ("2030-01-01T00:00:60Z", False),
        ("2030-02-30T00:00:00Z", False),
        ("2030-01-01T24:00:00Z", False),
        (None, False),
    ]
    for value, expected in spellings:
        assert supported_utc(value) is expected, value
    passed = gate(30_000_000, 29_000_000, 29_000_000_000)
    refused = gate(30_000_000, 30_000_000, 30_000_000_000)
    outcomes = [
        ("checkpoint_not_consumption", "NOT_DISPATCHED", passed, {}, "CHECKPOINT_ONLY"),
        ("refused_before_dispatch", "NOT_DISPATCHED", refused, {}, "CHECKPOINT_REFUSED"),
        ("late_ordinary_commit", "COMMITTED", passed, {"observed_commit_us": 31_000_000}, "VERIFIED_SUCCESS"),
        ("no_post_t_max", "COMMITTED", passed, {"observed_commit_us": 90_000_000_000}, "VERIFIED_SUCCESS"),
        ("optional_time_absent", "COMMITTED", passed, {}, "VERIFIED_SUCCESS"),
        ("scheduled_terminate", "COMMITTED", passed, {"through_commit_conditions": False}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("contradictory_chronology", "COMMITTED", passed, {"observed_commit_us": 28_000_000}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("atomic_future_time", "COMMITTED", passed, {"atomic_physical_time": True}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("bad_membership", "COMMITTED", passed, {"admissible_members": False}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("lost_original_context", "COMMITTED", passed, {"original_context": False}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("commit_after_failed_check", "COMMITTED", refused, {}, "QUARANTINED_PARTIAL_SUCCESS"),
        ("unknown_after_expiry", "UNKNOWN", refused, {}, "UNRESOLVED"),
        ("rollback_is_not_retry_admission", "ROLLED_BACK", passed, {}, "NO_EFFECT_NOT_RETRY_PERMISSION"),
    ]
    for name, status, checkpoint, kwargs, expected in outcomes:
        assert completion(status, checkpoint, **kwargs) == expected, name
    print(json.dumps({
        "result": "PASS", "kind": "FICTIONAL_DESIGN_EXAMPLES_ONLY",
        "policyObjectChecks": 1, "arithmeticCases": len(arithmetic),
        "fixedOriginNonReopeningChecks": grid_checks,
        "utcEncodingAndPrecisionCases": len(spellings),
        "checkpointOutcomeCases": len(outcomes),
        "realClockDatabaseRuntimeTests": False,
        "clockTrustGuardsStatusOrCommitTimingProved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
