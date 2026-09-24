# Operation-claim and data-read intent component

Status: **draft/non-default, non-executable**. This is an incomplete input
component of AuthorizationPolicyBundle v0.2, containing
`EI_OPERATION_ASSERTION_V0_2`, `EI_DATA_READ_V0_2` and their identity-only
authorization-view extraction descriptors. It is not a complete resolved rule,
policy bundle or admitted release. Proposed wire choices require exact review.

Primary trust boundary: authorization-input integrity. The component describes
closed input shapes and exact field selection; it does not evaluate authority,
issue grants or implement a transaction or disclosure protocol.

## Stacked dependency and ownership

This draft depends on [PR #41](https://github.com/samovers/OFARM/pull/41) at
`bfd15b98c48f70e679824005c62adf4241dd8b22`. The initial PR targets that branch,
keeping the authorization-input diff separate from the proposed domain schema.
The AssertionRecord schema is an exact-byte draft dependency, not an accepted
runtime contract. Its SHA-256 is
`3a7044086a2b0a226109ac00b361332503d77b07efd602b29402662515b67f1e`.

The component manifest pins both real intent schemas, extraction descriptors,
referenced local schema bytes and approved source revisions. File SHA-256 names
the checked-in bytes; RFC 8785 JCS/SHA-256 names a complete JSON value. No
placeholder rule, policy or release digest stands in for an unmaterialized
owner contract. Current/default schemas and the PR #40/#41 components remain
unchanged.

## Two input profiles

The operation profile retains one `TARGET_SCOPE`, a prospective
`OPERATION_ASSERTION` effect identity and the complete operation claim content.
It reuses the exact domain definitions for compatible subject, body, time and
immutable bindings. Reporting authorization is separate from alleged performer
provenance. Selected-path asserting Party and pending result state are not
caller-authoritative input fields. The full AssertionRecord result is not used
as an intent envelope.

The operation checker rejects a prospective claim subject whose kind/reference
equals the immutable `TARGET_SCOPE` or a typed immutable body context binding.
A distinct proposed reference still requires the domain identity-admission owner
to establish truthful prospective posture; local non-collision proves neither
global nonexistence nor authority.

Designated foreign temporal endpoints must already be canonical and exactly
string-equal to the claimed domain time. No offset or fraction normalization can
make them match. Actual source resolution, admitted `timeBasis` qualifiers,
qualifier-to-posture compatibility and omitted-qualifier meaning remain domain
and evidence-time dependencies. A fixed pointer cannot admit result, record or
capture time as performance time. Other versioned payload context cannot override
the designated `temporalBasis`.

The read profile retains one `READ_TARGET` across all ten scope kinds and twenty
named record/artifact kinds, including `AUTHORIZATION_TRACE`. Direct reads have
neither query input; query reads have one `QUERY_SPECIFICATION` and one
`QUERY_PLAN` as integrity inputs. They never become extra authority targets.
The intent binds projection, redaction-policy revision, a single authorization
use purpose, buffered response, snapshot policy and requested disclosure controls.
There is no receipt target or streaming mode.

The existing query schemas describe eight scope kinds. Their syntax cannot
silently narrow the authorization profile's ten-kind union. An input reference
passing this component does not prove that a real query plan supports its target,
that a redaction policy authorizes its projection, or that disclosure is allowed.

The extractor descriptors are immutable declarative data. They select exact
JSON Pointers from one validated intent using identity transformations only.
They do not supply defaults, normalize values, repair conflicts, resolve records,
inject principal/time facts or choose an authority path. A runtime's selected
rule must eventually bind the exact schema and extractor; the caller cannot
choose a weaker pair.

The concrete draft uses fixed resource tuple order: authority target at index 0,
then the two query integrity inputs when present. The proposed effect ID occurs
only in `effectSubject`. Purpose uses the source's exact uppercase token grammar,
with no normalization. Read projection is a nonempty set of RFC 6901 pointers
relative to each logical result item; the empty pointer requests the whole item.
Four booleans request aggregate, count, metadata and lineage content. They grant
no permission and cannot override projection, redaction or coverage checks.
`ONE_GOVERNED_READ_SNAPSHOT` names the requested one-snapshot invariant, not a
database isolation setting or proof that the snapshot exists.

Every resource kind permits the same optional `COMPLIANCE`/`ADVISORY` twin
encoding. The source does not supply an exhaustive kind-to-twin applicability
predicate, so this component does not invent one. Absence is not proof that a
twin is inapplicable; actual resource/context proof must establish applicability
and the required value before executable use. Operation domain time is required
for every anchor kind. No read-action occurrence time is selected here; historical
query time remains bound inside the query/plan and cannot become the authorization
clock. These limits keep the component incomplete and non-executable.

## Verification and remaining dependencies

The fictional runner uses real local pinned schemas, JSON Schema validation
and the existing RFC 8785 implementation. Duplicate JSON names, unknown or
inapplicable fields, malformed selectors/cardinality, mirrored trusted facts,
extraction conflicts and dependency drift must reject. The complete intent is
covered by its JCS digest without an exclusion or result-style self-digest field.
No remote schema download or permissive replacement is a valid dependency.

From the repository root with the existing validation dependencies:

```sh
python3 -m pip install 'jsonschema>=4.22,<5' 'rfc8785==0.1.4'
python3 04_implementation_and_conformance/conformance_runners/ofarm_authorization_effect_intents_v0_2.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The fictional bundle contains 123 positive and 497 rejection cases, including
every one of the 60 read kind/form pairs. Rejections cover 413 schema, 28
extraction, fourteen local component, 23 integrity, twelve binding, six strict-JSON
and one canonical-domain failure. Expected extracted views are independent of
the descriptor mappings. The complete repository suite retains the previous
eleven checks and adds this checker as the twelfth.

Shape and fictional extraction checks do not prove foreign immutable resolution,
tenant/twin relationships, authority, online/offline clock trust, prior assertion
snapshot compatibility, read policy/coverage, source history, custody, retention
or atomic finalization. Optional semantic-event association still needs the
domain owner's compatibility predicate; intended-window association remains
unavailable under the existing event envelope.

The full protected-effect contract still names three assertion intent/body
bindings. This two-profile component does not close it or rewrite it as an
operation-only contract. Complete resolved rules, relevant-state projections,
the shared validation trace, write/read protocols and the selected release's
transitive dependencies remain required. `NO_STATE_EFFECT` does not remove
protected-read evidence obligations. OFARM2 #392/#396 remains parked.

Next: review the exact proposed input and extraction bytes, then complete their
separately owned binding prerequisites before any admission or runtime use.
