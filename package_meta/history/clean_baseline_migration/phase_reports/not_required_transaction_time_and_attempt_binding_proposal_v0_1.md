# NOT_REQUIRED transaction time and attempt binding proposal v0.1

Status: **non-authoritative semantic/binding review candidate; not executable**.
Owner: canonical [OFARM #25](https://github.com/samovers/OFARM/issues/25).
Primary boundary: immutable transaction time policy and attempt-bound evidence
for the first NOT_REQUIRED state-affecting consumer. This is a separate proposal
from PR #26's historical protocol; it changes no approved source or current asset.

## 1. Concrete proposal

Give each eligible operation-claim transaction a fixed **30-second maximum**,
starting with its original database transaction. Count binding, database waits,
authorization, domain checks and finalization against that original budget.
Earlier authority/session/evidence cutoffs still shorten permission. No wait,
re-evaluation, clock adjustment or connection replacement restarts the attempt.

Thirty seconds is a **new proposed policy choice**, not existing OFARM law or
a measured workload guarantee. It gives a finite initial development profile;
it deliberately refuses operations that cannot finish in that interval. It does
not change PostgreSQL role/statement/lock timeouts, guarantee any minimum wait,
or settle #396's read/write progress requirement. A different budget requires
reviewed profile bytes and renewed semantic approval, not an environment setting.

Use the existing database clock for UTC and the source runtime's suspend-aware
elapsed clock for a second, conservative limit. This selects a PostgreSQL/Linux
binding proposal, not a universal provider architecture. No clock service,
hardware device, scheduler, cancellation interface or second evaluator is added.

## 2. Source pins and preservation

| Source | Exact inspected input used here |
| --- | --- |
| [PR #26 protocol](https://github.com/samovers/OFARM/blob/38af7475d8cbd41b158e50ba77b60f140cbef4ba/package_meta/history/clean_baseline_migration/phase_reports/not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md) | §§5–6 original operation/intent; §§8–9 attempt and ordering; §§10–11 outcomes; §21 staged materialization |
| [PR #11 current candidate](https://github.com/samovers/OFARM/blob/e9052efcf3c673360d939e856ac866cb27d709ae/package_meta/history/clean_baseline_migration/phase_reports/authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md) | §18.2 exact exclusive validity minimum; §18.4 atomic writes; §18.5.1's late-settlement exception is read-only |
| [PR #23 protected effect](https://github.com/samovers/OFARM/blob/622376e2998cf8b3954ca19e81d2cce6fd57e5fe/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md) | One PENDING_REVIEW operation-claim assertion; independent assertion-act time and domain validation |
| [PR #359 provider](https://github.com/samovers/OFARM2/blob/7de8a2c4cf6eb1f293560af67e69565122c42f25/docs/rfcs/OFARM_Runtime_Authority_Action_Matrix_Evaluation_RFC_v0_1.md) | Consumes an owner-issued attempt and prepares a decision; it owns no transaction clock, persistence or commit |

These links do not rebind PR #26's older dependency pins. Compatibility review
must preserve the unchanged write rules across those revisions. Existing
approvals remain attached to their original decisions. No approval of this new
time policy is inferred from source-withdrawal or read-settlement approval.

## 3. Closed proposed time policy

The following exact object is **review data embedded in this candidate**, not
the complete `ofarm.transaction.not-required-state-effect.v0.1` profile, a
machine schema, a runtime selection entry or a receipt. It leaves no configurable
duration or optional fallback for this proposal. Its fields describe policy,
not caller-supplied proof.

```json
{
  "proposalId": "OFARM-ISSUE25-TIME-ATTEMPT-BINDING-001",
  "version": 1,
  "status": "SEMANTIC_REVIEW_NOT_EXECUTABLE",
  "firstConsumer": "ASSERT_OPERATION_CLAIM",
  "transactionBudgetMicros": 30000000,
  "cutoff": "EXCLUSIVE",
  "utcStartSource": "PostgreSQL.transaction_timestamp",
  "utcCurrentSource": "PostgreSQL.clock_timestamp",
  "elapsedSource": "Linux.CLOCK_BOOTTIME",
  "elapsedOrigin": "BEFORE_ORIGINAL_BEGIN_DISPATCH",
  "transactionTimeEncoding": "UTC_RFC3339_SIX_FRACTIONAL_DIGITS_Z",
  "attemptTransfer": "FORBIDDEN",
  "withinAttemptDeadlineReset": "FORBIDDEN",
  "lockTimeoutChange": false,
  "lateWritePermission": false,
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
counter it counts waiting, and it includes system suspension. See the
[Python clock documentation](https://docs.python.org/3.12/library/time.html#time.CLOCK_BOOTTIME).
These APIs supply readings, not independent evidence of clock trust or commit time.

Let `D` be the evaluator's exact canonical minimum of transactionDeadline and
every applicable exclusive validity end. The source owner also fixes:

```text
Mdeadline = min(M0 + 30,000,000,000 ns, M0 + (D - U0) in ns)
time gates open only while current UTC < D AND current elapsed time < Mdeadline
```

Before an authorization decision exists, substitute transactionDeadline for D;
that check grants no permission to perform an effect. Required earlier ends
must enter the final canonical minimum normally. Missing ends are never omitted.
Use checked integer arithmetic and exact canonical values. Transaction-owned UTC
values are finite Gregorian UTC timestamps with six fractional digits and Z.
Do not round an upstream cutoff later, use floats, or rewrite its owning time
meaning; unsupported precision/range prevents a usable binding. D at or before
U0, arithmetic overflow, missing/invalid clocks, or a nonpositive remaining
interval closes the gate. Equality is expired on either axis.

The fixed origin converts a shorter D without resetting elapsed time. The
pre-BEGIN elapsed sample is deliberately conservative: dispatch/binding latency
can shorten the usable interval. Later observations may close the gate earlier
but can never increase either limit. UTC below any prior observed UTC, elapsed
regression, a lost original clock/owner context, restart or connection/transaction
replacement invalidates the attempt. No same-attempt transfer or remint follows.

### Trust and the finalization limit

The database and source runtime are trusted owners; callers cannot supply or
replace their readings, origin, IDs or profile selection. Caller forgery, replay,
cross-tenant and cross-attempt substitution are in scope. Compromised trusted
hosts/clocks are not claimed to be solved by two samples. Runtime admission must
establish its actual clock accuracy/rate, UTC trust and observation contract;
integer nanoseconds do not prove nanosecond accuracy. This proposal contains no
measured clock-quality or production-provider clearance.

Both time gates are necessary, **not sufficient for timely write consumption**.
A sample before sending COMMIT cannot prove the actual protected-effect and
single-use consumption boundary met D. The source/storage binding must enforce
and evidence the existing write cutoff at its real boundary, with no unchecked
pause between a predicate and the act it supposedly authorizes. If it cannot,
the binding stays unavailable. The read-only late-settlement permission is not
borrowed. A late acknowledgement also does not establish late or timely commit.

After possible effect/COMMIT dispatch, clock expiry alone proves neither rollback
nor NO_EFFECT. Preserve actual status, block unsafe reapplication and reconcile
under PR #26. Never label an already dispatched transaction harmless merely
because its local time gate is now closed.

## 4. Real attempt producer and evidence placement

| Value or obligation | Producer and use |
| --- | --- |
| Logical operation, original caller projection, full intent and assertedAt | #178 authoritative lookup/admission under PR #26; recover surviving bindings unchanged before a later attempt. |
| Unique attempt ID and immutable durable sequence | #178's atomic operation guard under §8.2; provisional allocation is not durable history. Full XID is not an attempt sequence. |
| Original M0, bound tenant/backend/full XID, U0 and deadline | Source transaction owner over the real #173 UnitOfWork; complete the private attempt context before #353 consumes it. Current production UoW lacks this factory. |
| D, current decision, complete authority footprint | #353 evaluator; derives all selected-rule facts and cutoffs from governed sources. It cannot mint the attempt or choose a later deadline. |
| Snapshot, complete set/absence/record guards and status lookup | #178/source-storage owner, under the admitted transaction profile. Clock checks do not manufacture these currently missing bindings. |
| One PENDING_REVIEW assertion and validation trace | Separate PR #23 protected-effect owner; ALLOW and elapsed time are not domain validation. |
| Decision/mode/effect/consumption/attempt/receipt or truthful failure evidence | #178's complete atomic sets and reconciliation. Reuse §12's digest order and receipt self-exclusion; no separate time receipt or new ledger. |

The selected time policy's exact identity/digest and durable start/deadline/time
facts belong in the existing profile/attempt/consumption bindings at their owning
stages. Raw M0 is process/boot-relative live guard state, not a portable timestamp
or recovered authority. Any retained elapsed observation must be labelled with
its original clock domain and attempt; it cannot become proof of commit time.
Normal retention and disclosure owners still control persisted evidence.

An exact completed-write retry recovers the old outcome; it does not reset a
deadline and re-execute the write. A permitted fresh attempt after authoritative
NO_EFFECT has new attempt/time inputs, preserves the original operation/intent,
and repeats current checks. No retry loop or extra withdrawal permission follows.

## 5. Focused review and verification

| Case | Required disposition |
| --- | --- |
| D equals original 30-second cutoff; both samples are strictly earlier | Time gates open only; no authorization, domain or commit claim. |
| Either sample equals/exceeds its cutoff, including one nanosecond at the elapsed boundary | Time gates closed; no rounding grace. |
| A grant/session/evidence end is earlier than the transaction deadline | Exact earlier D and its original-origin elapsed cutoff govern. |
| Binding or lock waiting consumes most/all of the budget | Remaining budget shrinks or closes; no reset after the wait. |
| UTC stalls or moves backward; elapsed time continues | Elapsed cutoff never extends; observed UTC regression invalidates the attempt. |
| UTC jumps ahead | UTC can close the gate early; elapsed time cannot reopen it. |
| Host is suspended, process/backend restarts, or another connection is offered | Suspension counts; missing original domain or replaced context cannot resume this attempt. |
| A caller supplies a longer deadline, origin, profile or attempt frame | No trusted producer binding; no consumable decision/effect. |
| The final check passes, then execution pauses through D before consumption | Required real-boundary check refuses; a pre-check receipt cannot satisfy it. No mechanism for this is claimed here. |
| Commit was possibly dispatched before the response/clock failed | Follow authoritative status and uncertainty rules; no inferred NO_EFFECT or automatic retry. |
| Same key after completed success or conclusively retryable failure | Preserve original operation/result or admit a genuinely fresh attempt, respectively; never reuse failed attempt authority. |

Arithmetic examples can test strict comparisons, original-origin mapping and
refusal inputs locally with fictional timestamps. They are design checks only.
Actual clock quality, suspension, factory provenance, same-transaction identity,
late-consumption prevention, guards, atomic outcome and later-writer commit need
separately approved real production-path tests in isolated disposable databases.

## 6. Review decision and remaining binding work

Review these new choices together: 30 seconds from the original transaction;
database UTC plus CLOCK_BOOTTIME with a pre-BEGIN origin; exact earlier cutoff
mapping; refusal on lost/changed clock or attempt context; no late-write exception.
The scope is provisional pre-deployment policy. Workload evidence that valid
operations cannot complete, unsupported clock guarantees or an unenforceable
write boundary requires redesign or rejection, not a larger mutable timeout.

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

No active law, current/default contract, legacy/runtime code, timeout, grant,
withdrawal eligibility, public route, disclosure, retention, publication custody
or deployment changes. Approved protocol/source bytes remain untouched.

Next: review the concrete time/attempt choices at this candidate head. Semantic
approval and the existing staged binding/promotion/extraction gates must precede
runtime use; do not implement a timeout patch or claim #396's progress case passed.
