# Event association and measured-operand amendment

This amendment addresses B2 and F4 from the [review of `8e86208`](https://github.com/samovers/OFARM/pull/47#issuecomment-6310698661).
The primary trust boundary remains **AssertionRecord domain meaning and
validation integrity**. It changes the proposed design and examples, with no
change to PR23, Event Ingress authority, evidence admission or runtime behavior.

The [canonical/Event Ingress resolution](canonical-owner/resolution.md) removes
the complete technical event-association object from the rendered projection.
The optional immutable envelope binding stays in the complete intent. The
protected-effect trace retains the complete association, classification,
selectors, compatibility results and independent ingress proof. Existing domain
activity, performer, extent, time, measurement meaning and pending-output
qualifications remain in the body. Association presence does not assert whether
a world event occurred.

The envelope must be fixed and resolvable before intent hashing and
authorization. Ingress evidence may be eligible pre-existing proof or separately
completed validation-phase proof, but must be available before its dependent
domain verdict. The sources guarantee neither pre-submission production nor
blanket reuse. The existing owner must close the actual artifact, producer,
admission, context, reuse and availability interface. A later result/receipt or
proof depending on this verdict cannot serve as its prerequisite. The verifier
consumes completed owner inputs and does not produce or rewrite them.

The domain contribution makes required measurement-source presence a separate
completeness obligation. W05/C04 retains its censored operand and INDETERMINATE
outcome while gaining an exact source, value pointer and bound criterion.
Expected property, scope, method/use, time, units and bounds come from that
criterion and existing owner rules, independently of the selected measurement.
Omitting a required citation or citing a valid-shaped measurement of the wrong
property cannot satisfy the check. Equivalent measured compliance roles and
qualifiers are audited without narrowing the measurement language.

All 25 previous example meanings and every original frozen input remain.
Coverage still requires 99 definitions, 42 requirements, 49 AR/PC obligations,
nine time profiles and 17 eligible event/profile cells, with full event and
measurement support. Finite fictional examples do not establish owner admission,
source adoption, new schema completion or a full domain-verifier PASS.

## Concrete construction inputs

The [domain-owner recommendation](domain-owner-recommendation.md) records the
source reasoning, audit and finite check limits. Its complete authored delivery,
including reconstruction scripts, is copied with two prose-link adjustments
and the subsequent F5 correction declared in [the transport record](domain-owner-transport.json). The original
owner manifest describes the source filenames; use this amendment's manifest
for the integrated filenames and bytes.

- [Projection v3](projection-contract-v3.json), [wire selector map](selector-map-v3.json)
  and [typed evidence selectors](evidence-selectors-v3.json).
- [All 25 versioned examples](candidate-examples-v3.json), their
  [source/transform map](source-transform-map-v3.json) and
  [coverage preservation](coverage-preservation-v3.json).
- [Measured compliance role contract](measurement-role-contract-v3.json),
  [17-row compliance audit](compliance-role-audit-v3.json),
  [independent fictional criterion expectations](criterion-expectations-v3.json),
  [measurement records](measurement-fixtures-v3.json),
  [hostile measurement cases](measurement-hostiles-v3.json) and
  [required-role cases](compliance-role-cases-v3.json).
- [Event placement/timing cases](event-cases-v3.json), their
  [fixed compatibility package](event-compatibility-package-v3.json) and
  [canonical timing integration](canonical-timing-integration-v3.json).

The [portable checker](check_examples_v3.py) and its finite
[measurement](measurement_checks_v3.py) and [event](event_checks_v3.py)
reference calculations exercise this design corpus. They do not implement
`verify_domain`, authenticate owner facts or replace the future public-entry-point
tests. Fictional proof fields describe test assumptions; a caller's successful
Boolean is not an owner admission mechanism. The checker takes `--packet`,
`--repo-root`, an optional `--dependency-dir` for pinned local libraries, and
an optional `--frozen-root` for checking the original full source snapshot.
Write rerun outputs outside this packet so the recorded owner runs remain
historical evidence. Reconstruction scripts are authoring aids, not installed
verifier code; use their explicit source arguments and regenerate custody records
after any intentional reconstruction. The [owner delivery notes](OWNER_DELIVERY_README.md)
record their original execution context.

## Fresh-review correction

The independent review of `228b7f4` closed B2/F4 but found F5: both fictional
event rules and proofs used the record subtype as the commit class. The
[owner correction](review-repair-01/recommendation-fix01.md) changes those exact
roles to `OPERATION_CLAIM`, preserving result subtype `OPERATION_CLAIM_ASSERTION`
and effect-subject kind `OPERATION_ASSERTION`. All 25 claim examples and all
12 existing event-case intent/result/envelope values remain unchanged.

The [new source-backed checker](commit_class_checks_v3.py) reads the byte-pinned
PR23 mapping and both ingress schema enums, independently of the fictional
package. The files under `commit-class-sources/` are exact pinned source copies;
their original navigation resolves at the recorded repository path and commit,
not relative to this evidence folder. [Additional hostile cases](commit-class-cases-fix01.json) reject a
package, proof and trace that agree on the same wrong value, including a valid
enum token for the wrong action, and reject changing the correct result subtype.
The [correction transport](review-repair-01/transport.json) records all six
replacements and eight required additions.

The original 655/603-check owner reports describe the initial amendment at
`228b7f4`; they did not detect F5. The [corrected full run](review-repair-01/check-results-fix01.json)
passes 723 checks and the [corrected portable run](review-repair-01/portable-check-results-fix01.json)
passes 671. These remain finite fictional design checks with the same limits.

The first [review amendment](../review-amendment/README.md) is preserved as
historical evidence at source commit `8e86208f96756b8f271f490696e6aa7cf23605fe`.
Its members remain byte-identical; its related Phase A/README hashes refer to
that commit. The new amendment manifest binds this version and records the
historical source selection. No original source pin or frozen rendering is
silently rewritten.

Next: validate and independently review this concrete amendment, then construct
the complete candidate contract/verifier in the same draft under its documented
owner dependencies. OFARM2 #392/#396 remain parked; #421, CI activation and merge
remain separate.
