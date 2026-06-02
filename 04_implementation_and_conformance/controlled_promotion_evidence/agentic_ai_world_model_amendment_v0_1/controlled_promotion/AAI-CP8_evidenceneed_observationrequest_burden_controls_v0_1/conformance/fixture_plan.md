# CP8 conformance fixture plan

The CP8 conformance runner validates positive request-layer examples against promoted schemas and checks request-layer invariants:

- EvidenceNeed and ObservationRequest must be non-evidence, non-obligation, and non-blocker-by-itself.
- Blocking status must cite a non-null RequestBlockingBasis.
- RequestBlockingBasis must cite an external rule or gate when blockApplies is true.
- RequestDisplayEnvelope must tell the user what is blocked and what is not blocked.
- RequestSatisfactionTrace must not create evidence by itself.
- Accepted evidence references require review or explicit promotion-decision reference.

Negative policy examples are intentionally not schema-clean or invariant-clean and are expected to be blocked or qualified.
