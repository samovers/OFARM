# CP12 Phase 7.2 Acceptance Gate

## Verdict

ACCEPT WITH RESIDUAL NON-BLOCKING NOTES.

CP12 is acceptable as a controlled amendment candidate after Phase 7.2 hardening. Machine contracts remain draft/non-default pending a separate currentness-promotion decision.

## Passed gates

- Dispatch authorisation cannot rely on failed preflight, incompatible capability, stale emergency stop, or unready override when supporting records are provided.
- Commands cannot bind to denied/expired/mismatched dispatch authorisations when supporting records are provided.
- PASS preflight must cover hard check classes or declare not-applicable basis.
- Mission outputs cannot grant dispatch authority.
- Temporal and recipient-binding conformance checks are present.
- End-to-end positive and negative mission-chain fixtures are present.

## Still not claimed

- Production robot/machine readiness.
- Autonomous field-operation readiness.
- Legal or safety certification.
- Fleet optimisation law.
- Vendor protocol law.
- CP13, CP14, or CP15 readiness.
