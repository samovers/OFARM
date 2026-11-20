# Pre-verdict Event Ingress classification proof

This draft, non-default component provides a concrete offline interface for an
Event Ingress classification proof that is available before a dependent domain
verdict. The primary trust boundary is **Event Ingress classification and evidence
admission**. The component creates no live admission, event, accepted claim,
authorization, signing authority or transaction guarantee.

The existing SemanticEventEnvelope and CommitIngressRequest remain unchanged.
CommitIngressResult and PromotionTrace describe later processing; neither is
relabelled as this earlier proof. This proposal adds no event family, subtype
dictionary, commit class or promotion law. All seven existing families and all
nine commit classes remain representable. A family is never inferred from a
commit class.

The owner selects an exact classification profile and verification context
independently of the supplied proof. The checker recomputes the source bindings,
exact envelope/request byte hashes, complete dominant-consequence and subtype
comparison, classified family, selected commit class and reuse conditions. It
consumes the original input bytes. Rehashing a caller-supplied report does not
verify a proof.

The dependency order is schema/source closure, contract, classification profile,
fixed envelope/request, independently selected owner context, completed proof,
and then the consumer's verdict. Both a preexisting proof and a proof completed
during validation are supported. This is not a guarantee of pre-submission
production. This verdict, its trace, the final assertion effect and this
attempt's later receipt cannot supply an earlier proof.

Trusted pins and the immutable proof selector are independent configuration.
The fixture profile and contexts are explicit fictional owner selections, not
proof that a real source owner admitted a record. Conditional offline conformance
does not establish producer identity, clock trust, event occurrence, runtime
admission, claim acceptance, or permission to replay a commit. Runtime selection
and admission require their separately governed owners.

The component is a prerequisite interface for the domain verifier in
[PR #47](https://github.com/samovers/OFARM/pull/47), not a claim that #47 is complete.
It is based independently on main so that the consumer dependency cannot form a
PR cycle. Assertion-act and transaction snapshot/guard contracts remain separate.
OFARM2 #392/#396 stay parked; CI activation and merge are separate decisions.

Next: review the exact contract and offline evidence, then let consumers bind its
specific schema, contract and verifier bytes under their own reviewed package.

Run these opt-in local checks from the repository root. The existing default
validation suite and GitHub workflows are unchanged, so CI activation remains a
separate decision:

```sh
python3 -B 04_implementation_and_conformance/conformance_runners/ofarm_event_ingress_classification_proof_v0_1.py
```

The [proposal](PROPOSAL.md) defines the exact conditional trust root and limits.
[Portable usage](PORTABLE_USAGE.md) documents the function, CLI and split layout.
Install the dependencies listed in [dependency-manifest.json](dependency-manifest.json)
in a local environment before running. The checker never downloads dependencies.
