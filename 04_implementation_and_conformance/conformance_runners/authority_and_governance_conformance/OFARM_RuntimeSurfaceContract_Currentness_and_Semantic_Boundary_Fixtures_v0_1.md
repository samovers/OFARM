# OFARM RuntimeSurfaceContract currentness and semantic-boundary fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation fixture set  
Scope: bounded runtime-surface hardening proof for default-current v0.1 coexistence with a non-default v0.2 draft extension for meaning-bearing surface fields

---

## 1. Purpose

These fixtures harden the runtime-surface seam without reopening RC2.1 or replacing the accepted interoperability/runtime-surface RFC.

The bounded target is:
- keep `OFARM_RuntimeSurfaceContract_schema_v0_1.json` as the default current contract
- add a non-default v0.2 draft for fields that make surface identity and conflict comparison more explicit
- prove that discovery, query, API, event, and file-exchange surfaces can expose binding/auth/delivery/idempotency posture without turning OFARM into an API-first standard

## 2. Positive draft-surface fixtures

### Stable discovery surface
- explicit discovery path binding
- public discovery posture
- lookup-safe retry posture

### Partner HTTP export surface
- explicit HTTP path binding
- partner-scoped auth posture
- request/response delivery
- safe repeat-call posture

### Optional query façade
- explicit query-namespace binding
- authenticated façade posture
- non-default experimental compatibility posture
- QuerySpecification / QueryPlanIR remains authoritative

### Semantic event ingress surface
- explicit topic namespace
- at-least-once stream delivery
- consumer dedup requirement
- event transport remains subordinate to semantic event and commit-ingress law

### File-exchange bridge export surface
- explicit file-pattern binding
- out-of-band controlled posture
- batch export delivery
- retries may mint a distinct package artifact

## 3. Negative fixtures

- missing surface binding should fail schema validation
- query façade with non-query binding kind should fail
- event surface without consumer-dedup posture should fail
- file-exchange surface with request/response delivery should fail

## 4. Currentness rule under test

These fixtures are not a silent promotion of v0.2.
They exist to prove all of the following simultaneously:
- v0.1 remains the package default
- v0.2 draft is usable for bounded hostile-integrator comparison work
- service-description documents remain references, not hidden semantic authority
- discovery refs may now point at the governed discovery-surface identity when a discovery surface is itself represented as a governed OFARM artifact

## 5. Expected result

The runner should emit `PASS_WITH_LIMITATIONS` when:
- v0.1 examples still validate as current defaults
- v0.2 draft examples validate with the new meaning-bearing fields
- the negative mutations fail as expected
- no package map or currentness text treats v0.2 draft as the new default
