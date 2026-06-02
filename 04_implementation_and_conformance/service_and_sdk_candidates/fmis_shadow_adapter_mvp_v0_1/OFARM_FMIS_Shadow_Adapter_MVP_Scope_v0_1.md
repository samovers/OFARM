# OFARM FMIS Shadow Adapter MVP Scope v0.1

Date: 2026-05-13

## In scope

- parse selected FMIS task/result exports
- preserve original payload references and hashes
- emit `SourceFidelityEnvelope`
- emit `ImportCandidate`
- emit `ImportReceipt`
- emit `ImportLossMap`
- queue unresolved identity/unit/geometry review items
- block high-consequence use until review/promotion

## Out of scope

- accepted operation truth
- current-state truth mutation
- Compliance Twin decisioning
- frozen DocumentAssembly publication
- automatic worker/contractor identity inference
- automatic product authorization binding
- live readiness claim

## Required MVP operations

- `imports.submitCandidate`
- `imports.lossMap.get`
- `identity.resolve`
- `calculations.preview` where imported quantities need governed normalization

## Required MVP conformance

The adapter fails conformance if it promotes candidate records, suppresses loss maps, hides unresolved identity, or labels candidate operation claims as accepted execution.
