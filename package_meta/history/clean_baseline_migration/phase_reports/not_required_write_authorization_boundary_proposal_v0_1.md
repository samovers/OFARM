# Guarded write authorization checkpoint proposal v0.1

Status: **proposed semantic change; unapproved and non-executable**.
Decision: `OFARM-NOT-REQUIRED-WRITE-BOUNDARY-001`, version 1.
Owner: canonical [issue #25](https://github.com/samovers/OFARM/issues/25), with the
authorization and protected-effect owners identified below.
Primary boundary: **when a write may use its authorization, and the time facts
that truthfully evidence that use**. This is separate from
[PR #38](https://github.com/samovers/OFARM/pull/38)'s clock/budget proposal.

## 1. Decision proposed for review

For **`ASSERT_OPERATION_CLAIM` under an explicitly selected `NOT_REQUIRED` rule
only**, test temporal authorization at one final guarded checkpoint inside the
original database transaction. Require its trusted time `T < D`, where D is
the complete existing exclusive minimum, including the original transaction
deadline. Then permit only that already checked, fixed write and its complete
evidence set to finish committing in that same transaction after D.

Example: a fictional claim passes the checkpoint at 29 seconds, D is 30 seconds,
and the transaction commits at 31 seconds. This proposal permits that result.
The previous strict consumption-at-commit rule does not. A checkpoint at exactly
30 seconds is refused. No new attempt or changed claim can reuse the earlier T.

**This is a real relaxation of the write timing rule**, not clarification of an
existing approval. A session, grant or other authority cutoff contributing to D
can pass between T and commit without that passage alone invalidating the sealed
write. There is no promised maximum interval from T to commit or visibility.
Existing database interruption limits still apply; they do not extend authority
or guarantee exact-time cleanup. A requirement that no new claim become durable
after D is incompatible with this option: retain that requirement and reject
this proposal rather than claim that this checkpoint implements it.

Only one `PENDING_REVIEW` operation-claim assertion is in scope. Other writes,
human finalization, filing, governed reads, accepted-force emission and external
effects retain their own rules. No 30-second budget, clock implementation,
source-wait exception, source withdrawal or runtime activation is approved here.

## 2. Exact inputs and required owner changes

| Pinned input | Proposed change, limited to this selected write branch |
| --- | --- |
| [PR #11, e9052ef](https://github.com/samovers/OFARM/blob/e9052efcf3c673360d939e856ac866cb27d709ae/package_meta/history/clean_baseline_migration/phase_reports/authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md), §§8.1, 18.2, 18.4 | Temporal eligibility is T < full D; durable single-use consumption still occurs only with the complete atomic effect. Add an explicit immutable rule selection, never infer it from NOT_REQUIRED alone. |
| [PR #26, 38af747](https://github.com/samovers/OFARM/blob/38af7475d8cbd41b158e50ba77b60f140cbef4ba/package_meta/history/clean_baseline_migration/phase_reports/not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md), §§8–9, 12, invariants 12–15 | Introduce the checkpoint order below; replace this branch's through-commit time test and receipt commit-time requirement. Preserve guarded facts, complete atomic success and reconciliation. |
| [PR #23, 622376e](https://github.com/samovers/OFARM/blob/622376e2998cf8b3954ca19e81d2cce6fd57e5fe/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md), §§6.2–6.5 | Distinguish the new checkpoint fact from physical commit time. Preserve assertedAt, subjectTime, domain validation and the single pending-review result. |
| [PR #38, 04e7a1e](https://github.com/samovers/OFARM/blob/04e7a1e3651226fe78f15bcb04955a172223e6e7/package_meta/history/clean_baseline_migration/phase_reports/not_required_transaction_time_and_attempt_binding_proposal_v0_1.md), §§3–6 | Align its gate lifetime and evidence claims with this decision if approved; the current no-late-write proposal cannot be combined unchanged with it. |

These are proposed changes, not amendments applied to those sources. Historical
pins and approvals stay attached to their original meanings. The task user's
approval of PR #26's conditional withdrawal semantics at 38af747 remains valid
for that scope and supplies no approval for this write-timing change.

The existing sources require validity through commit and a receipt containing a
trusted commit time. PostgreSQL runs deferred triggers before recording commit;
later commit processing can still wait before other sessions see the transaction.
See the [PostgreSQL 17.10 transaction source](https://github.com/postgres/postgres/blob/REL_17_10/src/backend/access/transam/xact.c).
Consequently an earlier predicate is not proof of timely physical commit.
This proposal accepts the interval explicitly instead of claiming to eliminate it.

## 3. One checkpoint, then completion or abort

The trusted transaction owner must implement this order; an application flag,
caller timestamp or preallocated receipt is not a checkpoint.

1. Establish the original operation/attempt, transaction, tenant and trusted time
   context. Run the existing current authorization evaluation and all applicable
   domain checks. Resolve and guard the complete positive, negative and set-valued
   facts under the admitted profile. No missing predicate is treated as stable.
2. Fix the exact decision, intent, result bytes/digest, rule/profile selection and
   evidence inputs. Recheck all guard and uniqueness conditions. Domain result
   selection and every authority-affecting decision are complete before T.
3. Inside the same trusted database finalization path, sample the admitted current
   time T and require T < full D. T is the clock-observation event at this check;
   it is not an earlier request time or a claim about when later processing ends.
   Sampling and testing can themselves be separated by scheduling delay: that
   interval is included in the explicitly accepted post-T interval. Missing clock
   trust or an original-context mismatch prevents a successful checkpoint.
4. After a successful checkpoint, retain exclusive owner control and the same
   original transaction. Only deterministic construction, verification and
   persistence of its fixed complete success set, followed by transaction
   completion, may remain. No caller callback, new business decision, changed
   effect, new authorization evaluation or handoff to another attempt is allowed.
   Ordinary processing, database waits, scheduling and durability work may cross D.
5. Keep the complete non-temporal guards valid through actual commit or abort on
   invalidation. Commit every success member atomically. Only authoritative
   complete-success verification permits the existing success response.

No durable authority reservation exists at step 3. T creates no consumable token,
does not spend the decision outside the transaction and survives in authoritative
success evidence only if that complete set commits. Rollback past the checkpoint,
savepoint recovery after its failure, replaced context or altered fixed inputs
cannot resume the same finalization. A fresh permitted attempt needs fresh checks
and a fresh T under the existing operation/attempt rules.

A newly recorded revocation, changed guarded fact or lost completeness proof
still invalidates the write unless the storage guard prevents that change until
commit. Pure passage through a cutoff already represented in D is the explicit
exception. Independently governed persistence, retention or domain prohibitions
are not waived; an incompatible obligation prevents admission of this branch.

## 4. Truthful time and receipt evidence

The following are proposed semantic fields, not executable schemas.

| Fact | Source and meaning |
| --- | --- |
| `authorizationEvaluatedAt` | Existing evaluator time; unchanged and distinct from T. |
| `writeAuthorizationCheckedAt` | T from the successful final guarded database checkpoint, scoped to the original operation/attempt and fixed decision/result. |
| `decisionValidUntil` and `transactionDeadline` | Original exact exclusive cutoffs; stored unchanged. Neither is moved to make late commit look timely. |
| `writeAuthorizationBoundary` | Proposed closed label `GUARDED_WRITE_CHECK_V0_1`, admitted only by an exact versioned rule/profile binding for the stated action. |
| Actual commit outcome | Existing authoritative status lookup plus complete matching atomic membership. A success label or receipt alone remains insufficient. |

Put T and the boundary label in the existing consumption, attempt and receipt
bindings before their final hashes; complete-set verification must require the
same exact T, boundary, cutoffs and attempt across those bindings. Allocate IDs
first, then finalize/hash the
consumption, attempt and receipt in PR #26 §12.2's existing acyclic order.
The receipt's self-entry and other digest exclusions remain unchanged. This
requires moving the checkpoint before final consumption/attempt/receipt hashing,
not inserting T into records that have already been hashed.

For this new versioned branch, the atomic receipt does **not** contain
`effectCommittedAt` or another purported physical commit timestamp. It binds the
truthful checkpoint fact and transaction-status key instead. These fields are
absent, not null or provisional values. Existing historical records are neither
rewritten nor interpreted as this new branch. Final source/schema alignment must
make the conditional time-field meaning explicit in all three owning contracts.

If an actual commit-record or visibility observation is separately retained, it
belongs in truthful later owner evidence pointing back to the original immutable
receipt. It is not required by this proposal, does not repair its original bytes
and is never backdated to T. No new timestamp service, success member or ledger
is introduced. The status/complete-set proof, not that optional timestamp,
establishes whether the original write succeeded.

Use PR #23 §6.3's canonical UTC spelling for T: omit a zero fraction; otherwise
retain one through nine digits ending in a nonzero digit. Preserve upstream
canonical strings and exact instants; no post-authorization normalization or
rounding. Precision and trusted-clock admission remain with the time-profile
owner. No original assertion-act time is replaced by T.

## 5. Failure, expiry and clocks

T >= D refuses finalization even if every earlier check passed. After a valid
checkpoint, expiry alone proves neither rollback nor success. Authoritative
complete commit is success even after D; conclusive rollback is no effect;
uncertainty remains blocked for reconciliation. A partial or mismatched committed
set remains an invariant breach. No automatic retry or new outcome category is
created. A completed retry resolves the old result without another consumption.

PR #38's application CLOCK_BOOTTIME gate could guard entry to the trusted
finalization path, before the database checkpoint. That earlier elapsed sample
would not prove elapsed time at T or physical commit. This proposal therefore
does not claim the existing two-clock draft already supplies the new binding.
A revised time owner must explicitly select and review those clock roles; loss
of source control cannot be treated as evidence that a possibly dispatched
transaction rolled back.

The through-commit freshness of non-temporal facts, exact effect bytes and atomic
membership is unchanged. The elapsed clock cannot stand in for those guards.
This is also not a promise that a waiting source survives its two-second lock
timeout or eventually commits; OFARM2 #396's progress obligation remains open.

## 6. Review cases and smallest next delivery

The companion `check_write_authorization_boundary_examples_v0_1.py` is a small
fictional trace model, runnable with Python 3 and no dependencies or database.
It makes the proposed old/new timing difference and outcome claims reproducible.
Its flags assume guard/provenance facts; it does not prove their implementation.
Its outcome labels are model conclusions, not new wire outcomes. A trace with an
observed inadmissible commit cannot be called refused or rolled back afterward.
Run from the repository root:

```sh
python3 package_meta/history/clean_baseline_migration/phase_reports/check_write_authorization_boundary_examples_v0_1.py
```

Review must cover: T strictly before/equal/after D; commit before and after D;
an earlier authority cutoff; altered result or invalidated guards; wrong attempt;
rollback and unknown status after T; incomplete committed membership; a second
consumption; and excluded actions retaining their original cutoff. Real binding
tests must use fictional data and isolated disposable databases over the actual
owner path, including a pause after the checkpoint and after COMMIT dispatch.

This candidate selects a semantic option only. It does not supply the complete
guard, real attempt factory, trusted clock contract or authoritative status
provider. It does not complete PR #26 §21 or OFARM2 #178/#353's producer ordering.
The concrete next owner work, if approved, is the matching authorization rule,
transaction-time evidence and protected-effect time alignment named in §2.
No independently scoped custody, public-disclosure or source-withdrawal changes
may be attached to that alignment. Runtime implementation follows the existing
materialization, admission, promotion and extraction gates.

Semantic approval must explicitly accept that the stated operation claim can
become durable after a contributing authority expiry, solely through its original
fixed, guarded transaction. Approval of this candidate would not approve a clock
budget, waive remaining bindings, authorize merge or change active/current law.

Next: review this exact decision and its post-cutoff consequence before any owner
source amendments or runtime work. PR #38 stays blocked pending that decision
and compatible owner alignment.
