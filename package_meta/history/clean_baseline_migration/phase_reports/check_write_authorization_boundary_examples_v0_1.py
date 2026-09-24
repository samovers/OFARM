"""Fictional review examples; not a runtime gate or evidence of database safety.

Times are integer seconds from a fictional UTC origin. Bound-rule selection and
guard/identity flags are assumed facts, never verified here. commit_at is a later
observation supplied to this model, not a value placed in atomic evidence. It is
optional for the new rule. The old-rule comparison is retrospective, not its
admission workflow. NO_EFFECT describes rollback, not durable retry evidence.
Run with Python 3; no database, dependencies or executable policy imports.
"""

from dataclasses import dataclass, replace


COMMIT_RULE = "EXISTING_COMMIT_CUTOFF"  # Model name, not a new policy identifier.
CHECKPOINT_RULE = "GUARDED_WRITE_CHECK_V0_1"


@dataclass(frozen=True)
class Trace:
    checkpoint_at: int
    cutoffs: tuple
    commit_at: object
    bound_rule: str = CHECKPOINT_RULE
    boundary_label: str = CHECKPOINT_RULE
    status: str = "COMMITTED"
    action: str = "ASSERT_OPERATION_CLAIM"
    mode: str = "NOT_REQUIRED"
    same_attempt: bool = True
    fixed_result: bool = True
    guarded: bool = True
    complete: bool = True
    already_consumed: bool = False
    # Fictional (success member, purported physical time) pairs, not a schema.
    atomic_physical_times: tuple = ()


def time_gate(trace):
    if (trace.bound_rule not in (COMMIT_RULE, CHECKPOINT_RULE)
            or trace.boundary_label != trace.bound_rule):
        return False
    checkpoint_rule = trace.bound_rule == CHECKPOINT_RULE
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


def disposition(trace):
    # Expiry/absence cannot turn an unknown dispatched outcome into rollback.
    if trace.status == "UNKNOWN":
        return "UNRESOLVED"
    if trace.status == "ROLLED_BACK":
        return "NO_EFFECT"
    if trace.status == "NOT_DISPATCHED" and trace.bound_rule == COMMIT_RULE:
        raise ValueError("Existing pre-dispatch admission is outside this model")
    prerequisites = (
        trace.same_attempt and trace.fixed_result and trace.guarded
        and not trace.already_consumed and time_gate(trace)
        and (trace.bound_rule != CHECKPOINT_RULE or not trace.atomic_physical_times)
    )
    if trace.status == "NOT_DISPATCHED":
        return "FINALIZATION_PERMITTED" if prerequisites else "REFUSED"
    assert trace.status == "COMMITTED"
    chronology_consistent = (
        trace.commit_at is None
        or (type(trace.commit_at) is int and type(trace.checkpoint_at) is int
            and trace.commit_at >= trace.checkpoint_at)
    )
    return (
        "EFFECT_COMMITTED"
        if prerequisites and trace.complete and chronology_consistent
        else "INVARIANT_BREACH"
    )


def main():
    base = Trace(checkpoint_at=29, cutoffs=(30,), commit_at=29)
    comparisons = [
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
        ("verified complete commit without optional time", replace(base, commit_at=None),
         "INVARIANT_BREACH", "EFFECT_COMMITTED"),
        ("observed commit precedes checkpoint", replace(base, commit_at=28),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("malformed later observation", replace(base, commit_at=True),
         "INVARIANT_BREACH", "INVARIANT_BREACH"),
        ("no promised maximum late interval", replace(base, commit_at=10**9),
         "INVARIANT_BREACH", "EFFECT_COMMITTED"),
    ]
    for name, trace, old, proposed in comparisons:
        for rule, expected in ((COMMIT_RULE, old), (CHECKPOINT_RULE, proposed)):
            assert disposition(replace(trace, bound_rule=rule, boundary_label=rule)) == expected, (name, rule)

    old_rule = replace(base, bound_rule=COMMIT_RULE, boundary_label=COMMIT_RULE)
    cases = [
        ("excluded action retains old rule before cutoff",
         replace(old_rule, action="ASSERT_COMPLIANCE"), "EFFECT_COMMITTED"),
        ("excluded action retains old cutoff",
         replace(old_rule, action="ASSERT_COMPLIANCE", commit_at=31), "INVARIANT_BREACH"),
        ("excluded action cannot select new rule",
         replace(base, action="ASSERT_COMPLIANCE"), "INVARIANT_BREACH"),
        ("human-finalized action retains old rule",
         replace(old_rule, mode="FRESH_APPROVAL"), "EFFECT_COMMITTED"),
        ("human-finalized action retains old cutoff",
         replace(old_rule, mode="FRESH_APPROVAL", commit_at=31), "INVARIANT_BREACH"),
        ("human-finalized action cannot select new rule",
         replace(base, mode="FRESH_APPROVAL"), "INVARIANT_BREACH"),
        ("unknown label cannot silently select old rule",
         replace(base, boundary_label="UNRECOGNIZED"), "INVARIANT_BREACH"),
        ("new bound rule cannot carry old evidence label",
         replace(base, boundary_label=COMMIT_RULE), "INVARIANT_BREACH"),
        ("old bound rule cannot carry new evidence label",
         replace(old_rule, boundary_label=CHECKPOINT_RULE), "INVARIANT_BREACH"),
        ("unknown bound rule cannot borrow a known label",
         replace(base, bound_rule="UNRECOGNIZED"), "INVARIANT_BREACH"),
        ("new-rule checkpoint permits finalization before dispatch",
         replace(base, status="NOT_DISPATCHED", commit_at=None), "FINALIZATION_PERMITTED"),
        ("new-rule checkpoint at cutoff refuses before dispatch",
         replace(base, checkpoint_at=30, status="NOT_DISPATCHED", commit_at=None), "REFUSED"),
    ]
    for member in ("consumption", "attempt", "receipt"):
        for purported_time in (base.checkpoint_at, None):
            cases.append((f"{member} falsely claims physical time {purported_time!r}",
                          replace(base, atomic_physical_times=((member, purported_time),)),
                          "INVARIANT_BREACH"))
    for name, trace, expected in cases:
        assert disposition(trace) == expected, name
    assert time_gate(replace(base, checkpoint_at=True)) is False
    assert time_gate(replace(base, cutoffs=(30, None))) is False
    print(f"PASS: {len(comparisons)} paired outcome traces; {len(cases)} explicit-selection/evidence cases; 2 invalid-time checks.")
    print("Assumed guards only. No database, actual clock, producer or runtime proof.")


if __name__ == "__main__":
    main()
