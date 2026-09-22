"""Fictional review examples; not a runtime gate or evidence of database safety.

Times are integer seconds from a fictional UTC origin. Guard/identity flags are
assumed facts, never verified here. commit_at is a later observation supplied to
this model, not a value placed in a pre-commit receipt. No I/O or runtime imports.
Run directly with Python 3; this script is outside all executable policy lanes.
"""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Trace:
    checkpoint_at: int
    cutoffs: tuple
    commit_at: object
    status: str = "COMMITTED"
    action: str = "ASSERT_OPERATION_CLAIM"
    mode: str = "NOT_REQUIRED"
    same_attempt: bool = True
    fixed_result: bool = True
    guarded: bool = True
    complete: bool = True
    already_consumed: bool = False


def time_gate(trace, checkpoint_rule):
    if checkpoint_rule and (
        trace.action != "ASSERT_OPERATION_CLAIM" or trace.mode != "NOT_REQUIRED"
    ):
        return False  # This proposal cannot select an excluded action.
    point = trace.checkpoint_at if checkpoint_rule else trace.commit_at
    return (
        type(point) is int
        and bool(trace.cutoffs)
        and all(type(end) is int for end in trace.cutoffs)
        and point < min(trace.cutoffs)
    )


def disposition(trace, checkpoint_rule):
    # Expiry/absence cannot turn an unknown dispatched outcome into rollback.
    if trace.status == "UNKNOWN":
        return "UNRESOLVED"
    if trace.status == "ROLLED_BACK":
        return "NO_EFFECT"
    prerequisites = (
        trace.same_attempt and trace.fixed_result and trace.guarded
        and not trace.already_consumed and time_gate(trace, checkpoint_rule)
    )
    if trace.status == "NOT_DISPATCHED":
        return "FINALIZATION_PERMITTED" if prerequisites else "REFUSED"
    assert trace.status == "COMMITTED"
    chronology_known = (
        type(trace.commit_at) is int and type(trace.checkpoint_at) is int
        and trace.commit_at >= trace.checkpoint_at
    )
    return (
        "EFFECT_COMMITTED"
        if prerequisites and trace.complete and chronology_known
        else "INVARIANT_BREACH"
    )


def main():
    base = Trace(checkpoint_at=29, cutoffs=(30,), commit_at=29)
    cases = [
        ("ordinary success", base, "EFFECT_COMMITTED", "EFFECT_COMMITTED"),
        ("commit after cutoff", replace(base, commit_at=31),
         "INVARIANT_BREACH", "EFFECT_COMMITTED"),
        ("commit exactly at cutoff", replace(base, commit_at=30),
         "INVARIANT_BREACH", "EFFECT_COMMITTED"),
        ("checkpoint exactly at cutoff", replace(base, checkpoint_at=30, commit_at=31),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("checkpoint after cutoff", replace(base, checkpoint_at=31, commit_at=32),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("earlier grant cutoff", replace(base, checkpoint_at=4, cutoffs=(30, 5), commit_at=6),
         "INVARIANT_BREACH", "EFFECT_COMMITTED"),
        ("changed effect", replace(base, fixed_result=False),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("lost guard", replace(base, guarded=False),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("different attempt", replace(base, same_attempt=False),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("partial committed membership", replace(base, complete=False),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("second consumption", replace(base, already_consumed=True),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("rollback after checkpoint", replace(base, status="ROLLED_BACK", commit_at=None),
         "NO_EFFECT", "NO_EFFECT"),
        ("unknown after dispatch", replace(base, status="UNKNOWN", commit_at=None),
         "UNRESOLVED", "UNRESOLVED"),
        ("unknown with expired checkpoint", replace(base, checkpoint_at=31, status="UNKNOWN", commit_at=None),
         "UNRESOLVED", "UNRESOLVED"),
        ("excluded action cannot select new rule", replace(base, action="ASSERT_COMPLIANCE"),
         "EFFECT_COMMITTED", "INVARIANT_BREACH"),
        ("human-finalized action cannot select new rule", replace(base, mode="FRESH_APPROVAL"),
         "EFFECT_COMMITTED", "INVARIANT_BREACH"),
        ("expired before dispatch", replace(base, checkpoint_at=30, status="NOT_DISPATCHED", commit_at=None),
         "REFUSED", "REFUSED"),
    ]
    for name, trace, old, proposed in cases:
        assert disposition(trace, False) == old, (name, "existing rule")
        assert disposition(trace, True) == proposed, (name, "proposed rule")
    assert time_gate(replace(base, checkpoint_at=True), True) is False
    assert time_gate(replace(base, cutoffs=(30, None)), True) is False
    print(f"PASS: {len(cases)} fictional traces, both rule interpretations; 2 invalid-time checks.")
    print("Assumed guards only. No database, actual clock, producer or runtime proof.")


if __name__ == "__main__":
    main()
