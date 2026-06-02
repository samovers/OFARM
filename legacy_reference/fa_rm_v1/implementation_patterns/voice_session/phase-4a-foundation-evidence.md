# Voice Session Phase 4A Foundation Evidence

Date: 2026-03-22
Scope: Phase 4A foundation closeout evidence for WP-60

## Purpose

Record the concrete runtime, test, and smoke evidence that the Phase 4A voice foundation is stable enough to support later live speech and route-family slices.

This note is evidence only. Runtime code, tests, and frozen contracts remain the authority.

## Runtime Surfaces Proven

The repo now proves these Phase 4A surfaces:

1. `/v1/voice-sessions` create, get, action, and replay behavior
2. `WS /v1/voice-sessions/{voiceSessionUri}/stream` preview control-plane behavior
3. typed trigger-context compilation and richer merged envelopes
4. grounded-advice shaping and post-save advice gating
5. mobile handover fixtures and a local smoke client

## Command Evidence

### Consolidated Phase 4A voice suite

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="/Users/einstein/Documents/Codex/Semantic farming/specs/api/v1/server/fastapi" \
.venv/bin/pytest -p no:cacheprovider \
  specs/api/v1/server/fastapi/tests/test_voice_api.py \
  specs/api/v1/server/fastapi/tests/test_voice_session_store.py \
  specs/api/v1/server/fastapi/tests/test_voice_trigger_context.py \
  specs/api/v1/server/fastapi/tests/test_voice_advice_grounding.py \
  specs/api/v1/server/fastapi/tests/test_voice_session_fixtures.py \
  specs/api/v1/server/fastapi/tests/test_api.py \
  -k "voice or capabilities_endpoint_exposes_preview_voice_streaming_and_tts_when_enabled"
```

Observed result:

- `28 passed, 673 deselected`

### Voice API and preview behavior

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="/Users/einstein/Documents/Codex/Semantic farming/specs/api/v1/server/fastapi" \
.venv/bin/pytest -p no:cacheprovider \
  specs/api/v1/server/fastapi/tests/test_voice_api.py \
  specs/api/v1/server/fastapi/tests/test_voice_session_store.py \
  specs/api/v1/server/fastapi/tests/test_api.py \
  -k "voice or capabilities_endpoint_exposes_preview_voice_streaming_and_tts_when_enabled"
```

Observed result:

- `17 passed, 673 deselected`

### OpenAPI voice alignment

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="/Users/einstein/Documents/Codex/Semantic farming/specs/api/v1/server/fastapi" \
.venv/bin/pytest -p no:cacheprovider \
  specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py \
  -k "capabilities or voice"
```

Observed result:

- `2 passed, 42 deselected`

### Mobile handover fixture sanity

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="/Users/einstein/Documents/Codex/Semantic farming/specs/api/v1/server/fastapi" \
.venv/bin/pytest -p no:cacheprovider \
  specs/api/v1/server/fastapi/tests/test_voice_session_fixtures.py
```

Observed result:

- `3 passed`

### Runtime contract check

Command:

```bash
make runtime-contract-check
```

Observed result:

- primary runtime suite: `50 passed`
- targeted auth/capability follow-up: `5 passed`

### OpenAPI export parity

Commands:

```bash
./specs/api/v1/server/fastapi/run-openapi-export.sh
make openapi-export-check
```

Observed result:

- snapshot regenerated successfully
- export parity check reported `OpenAPI snapshot is current`

### Live local smoke

Command:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4a.py \
  --hub-base-url http://127.0.0.1:8091 \
  --profile-id default
```

Observed result:

```json
{
  "ok": true,
  "backendBaseURL": "http://127.0.0.1:8080",
  "activeProfile": "default",
  "websocketEventCodes": [
    "stream_ready",
    "transcript_partial",
    "session_cancelled"
  ],
  "replayEventCount": 4,
  "finalStatusCode": "cancelled"
}
```

## Replay And Smoke Notes

1. The first live smoke attempt failed with `404` because the long-running local backend process predated the Phase 4A route work.
2. Restarting the default `:8080` backend from Control Center brought the live capability flags and `/v1/voice-sessions` routes online.
3. After restart, the smoke path proved create, preview stream, cancel action, and `/events` replay against a live local stack.

## Closeout Summary

Phase 4A foundation now has:

1. typed runtime contracts
2. replay-backed preview behavior
3. stable capability exposure
4. mobile handover fixtures
5. live smoke evidence against the local stack

No further Phase 4A foundation runtime gaps were discovered during WP-60 validation.
