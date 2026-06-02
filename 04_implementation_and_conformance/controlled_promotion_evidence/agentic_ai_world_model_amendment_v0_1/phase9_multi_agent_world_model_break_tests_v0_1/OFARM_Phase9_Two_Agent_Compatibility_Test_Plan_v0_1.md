# OFARM Phase 9 Two-Agent Compatibility Test Plan v0.1

## Status

Defined only. Not executed.

## Purpose

The two-agent compatibility path should prove that two independently implemented agents can interoperate through OFARM public contracts without transferring hidden authority or bypassing governance.

## Required scenario

1. Agent A operates as a scouting/evidence agent under sponsor-bound authority.
2. Agent A produces Advisory context and a handoff package.
3. Agent B operates as a planning/compliance-support agent.
4. Agent B receives the handoff context but must acquire its own authority.
5. Agent B attempts both a permitted draft action and a forbidden promotion/pack-activation action.
6. The runtime must allow the permitted draft action only if its authority envelope permits it, and block the forbidden action with trace evidence.

## Required artifacts

- Agent A run envelope and trace
- Agent A handoff envelope
- Agent B actorship binding
- Agent B authority envelope
- Agent B run envelope and trace
- blocked action trace for forbidden action
- result qualification for any user-facing answer
