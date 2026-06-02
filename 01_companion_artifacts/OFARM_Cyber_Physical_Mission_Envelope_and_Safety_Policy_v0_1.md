# OFARM Cyber-Physical Mission Envelope and Safety Policy v0.1

Status: CP12 companion artifact candidate; subordinate to baseline and accepted RFC law.

## Purpose

This companion note interprets CP12 mission-envelope law for implementers, agents, runtime surfaces, and conformance authors.

## Principles

1. **Mission stages are separate.** Intent, candidate, plan, preflight, dispatch authorisation, command, acknowledgement, telemetry, receipt, verification, and accepted consequence are different things.
2. **Dispatch is a governed act.** Dispatch requires mission envelope, authority trace, safety envelope, command integrity, and applicable current-state/CP11 gates.
3. **Safety envelope is not optional.** Geofence/no-go/geometry validation, emergency stop, human override, fallback, lost-link, capability compatibility, and autonomy posture are mission gates where applicable.
4. **Physical evidence is still evidence.** Telemetry, acknowledgements, and receipts are evidence candidates, not accepted truth.
5. **Agents prepare; authority governs.** Agents may prepare candidate missions and review packages inside authority envelopes; they do not become physical governors by default.
6. **Vendor payloads are mapped surfaces.** External robot/machine/drone/tasking payloads do not become OFARM law or truth by being valid vendor payloads.

## Example allowed pattern

```text
Observation -> current-state materialisation -> CP11 charter check -> mission candidate -> preflight -> human/policy dispatch authorisation -> command envelope -> command acknowledgement -> telemetry -> execution receipt -> mission verification -> review/promotion -> accepted execution consequence if justified
```

## Example prohibited shortcut

```text
Agent recommends mission -> tool invocation succeeds -> command sent -> telemetry received -> current state updated as executed
```

That shortcut is prohibited because it bypasses dispatch authorisation, command integrity, safety envelope, verification, and accepted-consequence promotion.
