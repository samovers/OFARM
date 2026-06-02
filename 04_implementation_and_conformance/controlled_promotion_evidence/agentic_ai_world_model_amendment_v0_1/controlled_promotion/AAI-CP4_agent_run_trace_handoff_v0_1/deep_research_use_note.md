# CP4 Deep Research use note

The attached Deep Research report was used to tighten CP4 around multi-agent traceability, handoff failure modes, trace propagation, and the distinction between tool execution success and governance success.

Applied CP4 consequences:

- `AgentRunTrace` includes trace identifiers, assumption records, tool calls, approval checkpoints, blocked actions, revocation events, result qualifications, and retention class.
- `AgentHandoffEnvelope` requires rights transferred, rights not transferred, required revalidation checks, recipient acceptance, and explicit `authorityTransferred: false`.
- `AgentToolInvocationTrace` separates `toolResultState` from `governanceOutcome`.
- `AgentBlockedActionTrace` is promoted as first-class audit material.

The report's world-model, EvidenceNeed, ObservationRequest, and farmer-facing UX findings remain queued for later CP phases and are not promoted by CP4.
