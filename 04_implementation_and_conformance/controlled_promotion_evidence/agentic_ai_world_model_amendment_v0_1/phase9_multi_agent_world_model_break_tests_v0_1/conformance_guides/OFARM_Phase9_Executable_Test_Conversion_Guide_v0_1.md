# OFARM Phase 9 Executable Test Conversion Guide v0.1

To convert a Phase 9 fixture into an executable test:

1. Load the hostile fixture.
2. Prepare the specified input signals.
3. Invoke the public operation or preflight surface, never an internal store write.
4. Assert the expected disposition.
5. Assert that every `mustPrevent` item did not occur.
6. Assert that all required blockers are present.
7. Retrieve trace evidence.
8. Assert required trace assertions.
9. Mark runtime status as passed or failed.

Do not mark a fixture as passed if the runtime blocks the action but fails to emit the required blocked-action trace.
