# OFARM Agentic Capability and Tool Manifest Policy v0.1 Candidate

Status: SUPPORTING_DRAFT_NOT_ACCEPTED

## Policy

Agentic runtime capabilities should be visible, inspectable, and bounded. The Capability Manifest and AgentToolManifest are the primary candidate surfaces for that self-description.

## Required distinctions

- Capability versus authority
- Discovery versus approval
- Tool hint versus policy decision
- Transport success versus semantic success
- Static validation versus runtime conformance
- Advisory world-model support versus Compliance Twin mutation

## Farmer-facing implication

A farmer or farm administrator should be able to ask:

> What can this agent actually do, what does it need approval for, what data can it see, what does it retain, and what will be traced?

The answer should come from manifest and trace surfaces, not from vendor prose alone.
