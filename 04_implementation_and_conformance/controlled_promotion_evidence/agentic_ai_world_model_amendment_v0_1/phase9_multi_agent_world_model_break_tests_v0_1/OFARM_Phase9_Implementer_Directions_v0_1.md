# OFARM Phase 9 Implementer Directions v0.1

These are directions for implementers, not active OFARM law.

Implementers should first make every gate executable as a policy-level and contract-level test. Do not attempt farmer-facing autonomy until these gates are passing.

Required execution layers:

1. authority and sharing decision engine
2. public operation/preflight surface
3. tool manifest validator
4. trace and blocked-action export
5. world-model invalidation evaluator
6. offline sync replay evaluator
7. output preview/publication gate
8. request lifecycle validator

A runtime must fail closed. A missing trace, missing authority envelope, missing freshness posture, or missing redaction policy is not a soft warning for high-consequence paths.
