# OFARM Phase 7 — Negative Case Register v0.1

| Negative case | Expected result |
|---|---|
| Agent emits request with no consequence | Blocked or downgraded |
| Agent marks request compliance-blocking without pack/rule/policy basis | Blocked, downgraded, or review-required |
| World model asks for repeated field observations after validity window has expired | Suppressed or expired |
| ObservationRequest says disease is present before observation occurs | Blocked; request cannot imply accepted fact |
| Contractor satisfies request outside delegated scope | Candidate retained; promotion blocked or review-required |
| Low-value duplicate requests flood daily brief | Collapsed by `RequestNoiseControlEnvelope` |
| EvidenceNeed is used as evidence | Blocked |
| Waived request treated as evidence existed | Blocked |
| Local narrative annotation treated as compliance fact without promotion | Blocked |
| Permission-limited answer hides that a request may be incomplete | Result qualification required |
