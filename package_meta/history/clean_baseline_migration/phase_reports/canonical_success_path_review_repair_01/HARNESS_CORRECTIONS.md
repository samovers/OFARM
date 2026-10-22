# Construction and harness corrections

These are author-side corrections, not product findings or external-review claims.

The initial source-edit construction script encountered a replacement assertion after changing the schema builder but before writing the verifier. The four affected construction files in this unsealed sibling were restored from the preserved original and the corrected transformation was rerun. No sealed packet was changed. All subsequent checks exercise the completed sources.

The first full installed run matched 490 of 491 exact-code expectations. The `oversize` API case rejects a decoded evidence document with `INVALID_INPUT_BYTES`. Its base64-expanded CLI envelope is itself larger than the outer strict-document limit, so the CLI rejects it earlier with `INVALID_WIRE_OR_PACKAGE`. Both were valid rejection paths; the case index had incorrectly expected the API's error at the CLI boundary.

The final case index records CLI `expectedCodes: [INVALID_WIRE_OR_PACKAGE]`, API `apiExpectedCodes: [INVALID_INPUT_BYTES]`, and the transport distinction. No runtime code or wire bytes changed. `installed-runner-initial-results.json`, `initial-case-index.json`, and the initial log preserve the 491-case first run. `installed-runner-oversize-replay.json` and its execution record preserve the successful one-case replay with the corrected CLI oracle. The final installed report combines those 490 unchanged successful executions with that explicit replay; it does not claim a second fresh full 491-case execution. The coordinator will replay the final exact index during fresh review.

Next: independently replay the sealed final case index, retaining the distinction between API input rejection and outer CLI wire rejection.
