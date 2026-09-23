# NOT_REQUIRED transaction time and attempt binding proposal — decision version 2

Status: **non-authoritative semantic/binding review candidate; not executable**.
Owner: canonical [OFARM #25](https://github.com/samovers/OFARM/issues/25).
Primary boundary: immutable transaction time policy and attempt-bound evidence
for the first NOT_REQUIRED state-affecting consumer. This is a separate proposal
from PR #26's historical protocol; it changes no approved source or current asset.

## 1. Concrete proposal

Give each eligible operation-claim attempt a fixed **30-second original cutoff
for its write-authorization checkpoint**. Count binding, database waits,
authorization and domain checks before that checkpoint against the original
budget. Earlier authority/session/evidence cutoffs still shorten permission.
No wait, re-evaluation, clock adjustment or replacement restarts the attempt.

Thirty seconds is a **new proposed policy choice**, not existing OFARM law or
a measured workload guarantee. The approved owner rule permits the fixed original
transaction to complete after ordinary expiry once its checkpoint passes. There
is **no maximum post-checkpoint delay**, or bound on physical commit, backend
lifetime or lock release. This proposal changes no PostgreSQL role/statement/lock
timeout and does not settle #396's read/write progress requirement. A different budget requires
reviewed profile bytes and renewed semantic approval, not an environment setting.

Use the existing database clock for UTC and the source runtime's suspend-aware
elapsed clock for a second, conservative limit. This selects a PostgreSQL/Linux
binding proposal, not a universal provider architecture. No clock service,
hardware device, scheduler, cancellation interface or second evaluator is added.

## 2. Source pins and preservation

| Source | Exact inspected input used here |
| --- | --- |
| [PR #26 protocol](https://github.com/samovers/OFARM/blob/0d8123d3e6ded25a92c271cd8379030524208086/package_meta/history/clean_baseline_migration/phase_reports/not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md) | §§8–9 original attempt, checkpoint after step 10/before step 11, matching evidence and admissibility; §§10–11 outcomes; §21 materialization |
| [PR #11 authorization](https://github.com/samovers/OFARM/blob/2b46dbed647981a55704fd69fe06b92b7240be37/package_meta/history/clean_baseline_migration/phase_reports/authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md) | §18.2 full exclusive validity minimum; §18.4.1 selected operation-claim checkpoint; §8.1 scheduled TERMINATE still binds through actual commit |
| [PR #23 protected effect](https://github.com/samovers/OFARM/blob/a0a06ad99516790d5b908d5de330591691dd0dcd/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md) | One PENDING_REVIEW operation-claim assertion; pre-T domain validation; §6.3 canonical UTC spelling and separate time meanings |
| [PR #39 boundary decision v3](https://github.com/samovers/OFARM/blob/6ec9f6650c3848083742c7039ac7a673b4375c8b/package_meta/history/clean_baseline_migration/phase_reports/not_required_write_authorization_boundary_proposal_v0_1.md) | Approved checkpoint/consumption distinction; no future physical time in the atomic success set |
| [PR #359 provider](https://github.com/samovers/OFARM2/blob/7de8a2c4cf6eb1f293560af67e69565122c42f25/docs/rfcs/OFARM_Runtime_Authority_Action_Matrix_Evaluation_RFC_v0_1.md) | Consumes an owner-issued attempt and prepares a decision; it owns no transaction clock, persistence or commit |

The corrected owner triple has same-task semantic approval, quoted in the public
records for [#11](https://github.com/samovers/OFARM/pull/11#issuecomment-5800766513),
[#26](https://github.com/samovers/OFARM/pull/26#issuecomment-5800767612) and
[#23](https://github.com/samovers/OFARM/pull/23#issuecomment-5800768607).
[#39 v3 approval](https://github.com/samovers/OFARM/pull/39#issuecomment-5795648070)
also remains valid. Their source bytes and historical labels are unchanged.
Version 2 replaces this proposal's stale through-commit expiry assumption with
that approved checkpoint rule. It does not rebind those owners' dependency pins
or infer approval of this new budget, clock policy, executable binding or merge.

## 3. Closed proposed time policy

The following exact object is **review data embedded in this candidate**, not
the complete `ofarm.transaction.not-required-state-effect.v0.1` profile, a
machine schema, a runtime selection entry or a receipt. It leaves no configurable
duration or optional fallback for this proposal. Its fields describe policy,
not caller-supplied proof.

```json
{
  "proposalId": "OFARM-ISSUE25-TIME-ATTEMPT-BINDING-001",
  "version": 2,
  "status": "SEMANTIC_REVIEW_NOT_EXECUTABLE",
  "firstConsumer": "ASSERT_OPERATION_CLAIM",
  "transactionBudgetMicros": 30000000,
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
  "lockTimeoutChange": false,
  "sourceWithdrawalEnabled": false
}
```

### Origin, arithmetic and sampling

The source owner samples elapsed time `M0` immediately before dispatching the
original BEGIN on its exclusive checked-out connection. After binding, it reads
`U0 = transaction_timestamp()` from that same live transaction and verifies its
tenant, backend incarnation and full XID. `transactionStartedAt = U0` and
`transactionDeadline = U0 + 30,000,000 microseconds`. Binding delays already
count; the factory refuses an already expired attempt. `M0` is never created
after binding to give that work a fresh budget.

The current UTC sample uses `clock_timestamp()`, not `now()` or the fixed
transaction-start value. PostgreSQL documents that distinction in
[Current Date/Time](https://www.postgresql.org/docs/17/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT).
The Linux elapsed source is `clock_gettime_ns(CLOCK_BOOTTIME)`; unlike a CPU-time
counter it counts waiting and Linux system suspension represented by that clock. See
[Python clock documentation](https://docs.python.org/3.12/library/time.html#time.CLOCK_BOOTTIME).
The Python 3.12 reference names the target runtime, not the interpreter running
document checks. These readings prove neither clock trust nor physical commit.
Unmeasured VM pause/migration behavior is not covered by a general suspension
claim; the actual deployment's clock/observation contract must be admitted.

Let `D` be the evaluator's exact canonical minimum of transactionDeadline and
every applicable exclusive validity end. The source owner also fixes:

```text
Mdeadline = min(M0 + 30,000,000,000 ns, M0 + (D - U0) in ns)
checkpoint passes only if T < D AND M1 < Mdeadline
```

Before an authorization decision exists, substitute transactionDeadline for D;
that check grants no permission to perform an effect. Required earlier ends
must enter the final canonical minimum normally. Missing ends are never omitted.
First validate `U0 < D <= transactionDeadline`; the redundant first min term is
valid under that invariant, not permission to clamp an invalid D into range.
Use checked integer arithmetic. Newly minted transactionStartedAt,
transactionDeadline and writeAuthorizationCheckedAt use PR #23 §6.3's existing
canonical UTC spelling: seconds and uppercase Z; omit a zero fractional part,
otherwise use 1–9 fractional digits with no trailing zero. This binding supports
only **exact whole-microsecond UTC inputs**. A required cutoff with sub-microsecond
precision makes it unavailable, even if another cutoff is earlier. Preserve all
upstream canonical strings; no rounding, flooring, floats or post-authorization
normalization. For example `.12Z` is canonical, `.120000Z` is not; `.1234567Z` is
canonical upstream but unsupported here. Precision is separate from spelling.
Unsupported range, overflow, missing/invalid clocks or a nonpositive interval
closes the gate. Equality is expired on either axis.

After PR #26 §9.2 step 10 fixes the guarded domain result, and before step 11
hashing, the original transaction owner samples **T** with clock_timestamp() in
that transaction. After receiving T, the same owner samples **M1** from the
original elapsed domain, then verifies both strict comparisons and the original
context/trust conditions. T truthfully labels the UTC sampling point; it is not
the instant both samples or tests finished. These are ordered observations, not
an atomic cross-host clock sample. A delay before M1 may conservatively refuse
the checkpoint; sampling-to-test delay after these readings has no promised
maximum. The later elapsed verification adds no new business choice or effect.

The fixed origin converts a shorter D without resetting elapsed time. The
pre-BEGIN elapsed sample is deliberately conservative: dispatch/binding latency
can shorten the usable interval. Observed UTC/elapsed regression or lost/replaced
original clock, owner, connection or transaction context prevents a valid
checkpoint. Neither limit can increase; no same-attempt transfer or remint follows.

### Trust and completion after the checkpoint

The database and source runtime are trusted owners; callers cannot supply or
replace their readings, origin, IDs or profile selection. Caller forgery, replay,
cross-tenant and cross-attempt substitution are in scope. Compromised trusted
hosts/clocks are not claimed to be solved by two samples. Runtime admission must
establish its actual clock accuracy/rate, UTC trust and observation contract;
integer nanoseconds do not prove nanosecond accuracy. This proposal contains no
measured clock-quality or production-provider clearance.

The exact initial-release operation-claim rule and its profile digest must select
the approved checkpoint semantics. A body label or this review JSON grants no
authority. Once the checkpoint passes, only deterministic construction,
verification, persistence and completion of the fixed original transaction remain.
No business decision, effect change, callback, re-evaluation or transfer follows T.
Ordinary expiry of D or its contributing grant/session ends, or passage of the
elapsed cutoff, does not alone invalidate that continuation. Do not add a second
physical-commit expiry gate or relabel T as commit/consumption time.

Scheduled or newly recorded applicable **TERMINATE effective at or before actual
commit still prevents valid success**, even when known before T. All remaining
through-commit conditions stay binding. A timely checkpoint or guarded snapshot
does not prove that predicate about future commit. The source/storage binding
must prove it or reject the unsupported path. This unresolved storage obligation
is not solved by clock arithmetic, and no new enforcement mechanism is claimed.

After possible effect/COMMIT dispatch, clock expiry alone proves neither rollback
nor NO_EFFECT. Preserve actual status, block unsafe reapplication and reconcile
under PR #26. Never label an already dispatched transaction harmless merely
because its local time gate is now closed. Loss of original-context/trust proof
also requires truthful status handling. Actual complete atomic commit establishes
consumption; matching membership alone is insufficient without admissible evidence.
A complete but inadmissible committed set uses existing QUARANTINED_PARTIAL_SUCCESS,
preserving the commit facts. Missing optional later physical-time evidence alone
is allowed; contradictory admitted chronology is not. No new outcome is added.

## 4. Real attempt producer and evidence placement

| Value or obligation | Producer and use |
| --- | --- |
| Logical operation, original caller projection, full intent and assertedAt | #178 authoritative lookup/admission under PR #26; recover surviving bindings unchanged before a later attempt. |
| Unique attempt ID and immutable durable sequence | #178's atomic operation guard under §8.2; provisional allocation is not durable history. Full XID is not an attempt sequence. |
| Original M0, bound tenant/backend/full XID, U0 and deadline | Source transaction owner over the real #173 UnitOfWork; complete the private attempt context before #353 consumes it. Current production UoW lacks this factory. |
| D, current decision, complete authority footprint | #353 evaluator; derives all selected-rule facts and cutoffs from governed sources. It cannot mint the attempt or choose a later deadline. |
| Snapshot, complete set/absence/record guards and status lookup | #178/source-storage owner, under the admitted transaction profile. Clock checks do not manufacture these currently missing bindings. |
| One PENDING_REVIEW assertion and validation trace | Separate PR #23 protected-effect owner; ALLOW and elapsed time are not domain validation. |
| T and successful original-context clock verification | Original source transaction owner after §9.2 step 10/before step 11; matching writeAuthorizationCheckedAt and GUARDED_WRITE_CHECK_V0_1 in consumption, attempt and receipt. |
| Decision/mode/effect/consumption/attempt/receipt or truthful failure evidence | #178's complete atomic sets and reconciliation. Reuse §12's digest order and receipt self-exclusion; no separate time receipt or new ledger. |

The selected time policy's exact identity/digest and durable start/deadline/time
facts belong in the existing profile/attempt/consumption bindings at their owning
stages. Raw M0 is process/boot-relative live guard state, not a portable timestamp
or recovered authority. Any retained elapsed observation must be labelled with
its original clock domain and attempt; it cannot become proof of commit time.
Normal retention and disclosure owners still control persisted evidence.
Before hashing in the existing consumption → attempt → receipt order, bind the
same T, boundary, original cutoffs and original attempt. No atomic success member
asserts physical commit/consumption time: absent, not null, provisional or renamed
T. A truthful optional later observation preserves its separate meaning and the
original bytes. Checkpoint success itself creates no durable consumption.

An exact completed-write retry recovers the old outcome; it does not reset a
deadline and re-execute the write. A permitted fresh attempt after authoritative
NO_EFFECT has new attempt/time inputs, preserves the original operation/intent,
and repeats current checks with a fresh T. NO_EFFECT alone does not establish
durable retry eligibility. PR #26 §11.5's original first-effect/success-write or
COMMIT-dispatch withdrawal cutoff is unchanged; T does not close or extend it.
Existing eligibility/binding prerequisites remain unmet, so withdrawal remains
unavailable. No retry loop or extra withdrawal permission follows.

## 5. Focused review and verification

Clock refusal cases below govern entry to the checkpoint; they do not impose a
new expiry test on the approved continuation after it.

| Case | Required disposition |
| --- | --- |
| D equals original 30-second cutoff; both samples are strictly earlier | Checkpoint clock conditions pass only; no durable consumption or commit claim. |
| Either sample equals/exceeds its cutoff, including one nanosecond at the elapsed boundary | Time gates closed; no rounding grace. |
| A grant/session/evidence end is earlier than the transaction deadline | Exact earlier D and its original-origin elapsed cutoff govern. |
| Binding or lock waiting consumes most/all of the budget | Remaining budget shrinks or closes; no reset after the wait. |
| UTC stalls or moves backward; elapsed time continues | Elapsed cutoff never extends; observed UTC regression invalidates the attempt. |
| UTC jumps ahead | UTC can close the gate early; elapsed time cannot reopen it. |
| Supplied elapsed reading includes a suspension, or original context is lost | Represented time counts; missing original domain or replaced context cannot resume this attempt. No VM/migration proof is inferred. |
| A caller supplies a longer deadline, origin, profile or attempt frame | No trusted producer binding; no consumable decision/effect. |
| T and M1 pass, then fixed completion pauses through D before actual commit | Ordinary expiry alone permits continuation without a maximum delay; all remaining through-commit conditions still apply. |
| Scheduled TERMINATE is effective by actual commit | No valid success even if T preceded its effective time; invalid committed evidence uses existing quarantine. |
| Commit was possibly dispatched before the response/clock failed | Follow authoritative status and uncertainty rules; no inferred NO_EFFECT or automatic retry. |
| Same key after completed success or conclusively retryable failure | Preserve original operation/result or admit a genuinely fresh attempt, respectively; never reuse failed attempt authority. |

The adjacent `check_not_required_time_attempt_examples_v0_1.py` is a standalone
fictional reproducer. From the repository root run:

```sh
python3 package_meta/history/clean_baseline_migration/phase_reports/check_not_required_time_attempt_examples_v0_1.py
```

It checks this closed policy object, strict arithmetic, original-origin
non-reopening, canonical/precision examples and illustrative checkpoint/outcome
cases. It assumes governed D, trusted provenance, guards and status; it cannot
prove those assumptions. No real clock, database, runtime or network is used.
Actual clock quality, suspend/pause behavior, factory provenance, transaction
identity, scheduled-termination enforcement, guards and atomic outcomes need
separately approved real production-path tests in isolated disposable databases.

## 6. Review decision and remaining binding work

Review these new choices together: 30 seconds from the original transaction;
database UTC plus CLOCK_BOOTTIME with a pre-BEGIN origin; exact earlier cutoff
mapping and ordered T/M1 observations; supported UTC precision/canonical spelling;
refusal on lost/changed original context. The approved post-T completion exception
is an input, not a new unscoped late-write permission.
The scope is provisional pre-deployment policy. Workload evidence that valid
operations cannot reach the checkpoint, unsupported clock guarantees or an
unenforceable remaining through-commit condition requires redesign or rejection,
not a larger mutable timeout.

This candidate makes those choices concrete before machine materialization.
It does **not** complete PR #26 §21 step 3: exact operation/attempt/mode/outcome/
consumption/receipt schemas, complete guard/status/profile bindings and their
real digests remain to be materialized and reviewed under their existing owners.
No fabricated refs, null digests or placeholder executable profile is supplied.

Producer delivery order also remains open: #353 requires a real write attempt
before using it, and #178 requires its evaluator for a complete successful write.
An independently usable producer must have a reviewed complete Delivery outcome;
a type-only companion or fixture attempt is insufficient. This time proposal
does not split issues, weaken #353's two-action scope or satisfy its read inputs.
The previously inspected tenant_uow.py was at its 520/520-line budget (its group
932/940). A later producer must respect its then-current architecture and prove
actual non-reusable backend incarnation; a PID alone is insufficient. This draft
authorizes no budget increase, new public clock injection API or post-BEGIN M0.

No active law, current/default contract, legacy/runtime code, timeout, grant,
withdrawal eligibility, public route, disclosure, retention, publication custody
or deployment changes. Approved protocol/source bytes remain untouched.

Next: review the concrete time/attempt choices at this candidate head. Semantic
approval and the existing staged binding/promotion/extraction gates must precede
runtime use; do not implement a timeout patch or claim #396's progress case passed.
