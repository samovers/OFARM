# OFARM Request Burden, Noise, and Farmer Display Policy v0.1

Status: active companion artifact by AAI-CP8  
Scope: policy guidance for EvidenceNeed, ObservationRequest, request burden, request noise, and farmer-facing display.

## 1. Policy posture

Request-layer artifacts are governed request artifacts. They help the platform explain missing information and ask for useful observations. They are not evidence, accepted assertions, obligations, compliance blockers, or promotion decisions by themselves.

## 2. Minimum policy requirements

A farmer-facing request must expose:

- why the request exists;
- what the system believes is missing;
- what will change if the request is ignored;
- whether the request is advisory-helpful, preflight-relevant, or gate-relevant under another explicit rule;
- how burdensome the request is;
- when the request is relevant;
- how to complete, decline, defer, or dispute it;
- which alternatives may satisfy the need;
- whether any result remains stale, permission-limited, advisory-only, disputed, or evidence-insufficient.

## 3. Burden and noise control

Request generation must prefer batching, deduplication, and non-interruptive display unless an external gate or timing-sensitive risk justifies interruption.

A request that cannot identify a consequence, relevance window, completion criterion, and burden estimate should not be presented as a task.

## 4. Blocking-force rule

An EvidenceNeed or ObservationRequest cannot create blocking force by itself. Any blocking display must cite a RequestBlockingBasis that points to an external rule, governance gate, pack requirement, output policy, sharing policy, or human decision.

## 5. Evidence and satisfaction rule

Completing a request may create candidate evidence, a submitted payload, or a review item. It does not create accepted evidence unless normal OFARM evidence, quality, authority, review, promotion, and dispute rules are satisfied.

## 6. Farmer-facing disclosure

Farmer-facing surfaces should use compact qualification markers for advisory-only status, missing evidence, stale data, permission limits, approval needs, dispute status, and non-blocker status. Detail views must allow reconstruction of why the request was generated and how it was handled.
