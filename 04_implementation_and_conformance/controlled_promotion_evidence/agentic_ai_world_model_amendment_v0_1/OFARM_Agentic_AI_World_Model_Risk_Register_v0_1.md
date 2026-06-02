# OFARM Agentic AI and World-Model Amendment Risk Register v0.1

Date: 2026-05-14  
Status: draft supporting risk register; not active law until promoted.

| Risk | Severity | Controlled by | Negative case | Required guard |
|---|---:|---|---|---|
| AI output becomes governance decision | Critical | AgentOutput prohibition; preflight; review/promotion gates | AI recommendation becomes accepted compliance fact | Outputs must resolve to draft/advisory/candidate until gates pass |
| World model becomes third twin | Critical | Advisory-only WorldModelState rule | World-model state used as Compliance current state | No third twin; bridge through BridgeCandidate and enforcement chain |
| Agent memory becomes hidden truth | Critical | Agent memory persistence rule | Assistant memory used as evidence | Persist only as governed artifact or discard as scratch |
| Handoff transfers authority | High | AgentHandoffEnvelope | Scouting agent hands authority to planning agent | Receiving agent rechecks authority independently |
| Tool-call success waives semantic blockers | Critical | RuntimeProblem and trace semantics | Endpoint success labels output accepted | Tool result disposition must remain separate from OFARM governance result |
| Capability manifest overclaims | High | agentSupport deployment self-description | Manifest advertises unsupported autonomy | Manifest must describe actual deployment capability only |
| Preflight mutates state | High | no-authoritative-side-effect rule | Dry-run activates pack or resolves identity | Preflight may create only diagnostic trace marked as such |
| Evidence/observation task spam | Medium | EvidenceNeed/ObservationRequest severity and consequence fields | Farmer receives many low-value AI chores | Each request must state reason, consequence, relevance window, and basis |
| Stale scenario used for high-consequence action | High | invalidation rules and freshness posture | Old world-model result used for submission | Recheck context, pack, materialization, and authority before bridge |
| Cross-farm benchmark becomes farm fact | High | advisory-only benchmark classification | Cohort signal treated as compliance fact | Benchmark outputs remain advisory unless separately evidenced and promoted |
| Sharing agent over-discloses | Critical | SharingGrant, redaction, permission-limited result policy | Buyer sees whole-farm data via brief | Every disclosure must be scoped and traceable |
| Offline contractor capture bypasses revocation | High | delayed-sync recheck | Contractor syncs after authority revoked | Draft may be retained; promotion blocked or review-required |
