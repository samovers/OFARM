# OFARM Phase 4 Agent Run Envelope, Trace, and Handoff v0.1

Date: 2026-05-14  
Status: supporting review package; not promoted  
Base: Phase 3 agent actorship/authority working-copy package

Phase 4 prepares the governed multi-step agent layer for OFARM. It builds on Phase 3 actorship by defining candidate run envelopes, run traces, tool invocation traces, output dispositions, blocked-action traces, stop/approval/freshness records, and handoff envelopes.

This package does not modify active baseline, companion artifacts, accepted RFCs, or active machine contracts.

Core rule: a state-affecting or multi-step agent run must be bounded by `AgentRunEnvelope`, explained by `AgentRunTrace`, and prevented from transferring authority through handoff.
