# OFARM Phase 9 Break-Test Gates v0.1

## Gate rule

An OFARM implementation cannot claim agentic or world-model runtime readiness unless it can execute and pass the relevant hostile gates.

## Gate families

1. Identity and authority gates
2. Handoff gates
3. Tool manifest and untrusted hint gates
4. External-data and import promotion gates
5. Hidden truth-store gates
6. Pack/profile semantic mutation gates
7. Query and sharing gates
8. World-model invalidation gates
9. Memory-to-truth gates
10. Benchmarking and data-learning gates
11. Trace-completeness gates
12. Offline sync gates
13. BridgeCandidate promotion gates
14. Output preview and publication gates
15. EvidenceNeed and ObservationRequest gates
16. Capability manifest readiness-claim gates
17. Review/promotion gates
18. Freshness and materialization gates

## Pass criterion

A gate passes only if the platform blocks the forbidden shortcut, preserves any safe candidate/context material, emits required RuntimeProblem/reason-code information, and produces trace evidence for the block.

## Runtime status

All gates in this phase are defined only. No runtime has executed them.
