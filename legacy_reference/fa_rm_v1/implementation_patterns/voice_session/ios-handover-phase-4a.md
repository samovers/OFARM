# iOS Handover: Voice Session Phase 4A

Version: 0.1 (handover)
Date: 2026-03-22
Applies to: OF Platform iOS client + Farm_RM backend preview voice runtime

This handover defines the current Phase 4A integration seam for preview voice sessions. It is a product-plus-engineering handoff for a future iOS client. It is not a new backend contract, not a promise of live Google or RSDO speech, and not a claim that this repo contains a production Swift codebase.

## 0. Purpose

Define how a mobile client should integrate with the preview-safe `/v1/voice-sessions` control plane and stream skeleton so product, QA, and mobile can validate the session lifecycle before live speech vendors land.

Hard boundaries:

- The repo now proves the voice session runtime contract, trigger-context envelope, advice-grounding envelope, event replay, and preview websocket path.
- The repo does not yet prove live vendor speech adapters, a polished farmer task inbox, or a production iOS implementation.
- The mobile client must keep transcript, interpreted meaning, save result, and advice eligibility separate at all times.
- Trigger context may guide the opener and route prior, but it must not be treated as committed farm truth.

## 1. Authority And Current Runtime Baseline

### 1.1 Authority order

For this handover, use this precedence order:

1. Runtime implementation and tests in `specs/api/v1/server/fastapi/app/` and `specs/api/v1/server/fastapi/tests/`
2. Frozen Phase 3A, Phase 3B, and Phase 3C voice contracts
3. The Phase 4A work-packet contracts
4. This handover document
5. The sample fixtures under `specs/api/v1/server/fastapi/tests/fixtures/voice_session/`

If this handover disagrees with runtime code or tests, the repo-backed runtime contract wins.

### 1.2 Observed current state

Observed current state:

1. Runtime exposes `POST /v1/voice-sessions`, `GET /v1/voice-sessions/{voiceSessionUri}`, `GET /v1/voice-sessions/{voiceSessionUri}/events`, `POST /v1/voice-sessions/{voiceSessionUri}/audio-config`, `POST /v1/voice-sessions/{voiceSessionUri}/utterances`, `POST /v1/voice-sessions/{voiceSessionUri}/actions`, `POST /v1/voice-sessions/{voiceSessionUri}/soft-commit/expire`, and `GET /v1/voice-sessions/{voiceSessionUri}/assistant-audio/{assetId}`.
2. Runtime exposes `WS /v1/voice-sessions/{voiceSessionUri}/stream` for preview `audio_config`, `audio_chunk`, and `action` messages.
3. Runtime supports ordered event replay through `GET /v1/voice-sessions/{voiceSessionUri}/events?afterSequence=<n>`.
4. Capability reporting now includes `voiceSessions`, `voiceSessionRuntime`, `voiceSessionStreaming`, `voiceSessionTts`, `voiceSessionShadowAsr`, `voiceSessionRsdoPrimary`, and `voiceSessionAudioRetentionOptIn`.
5. Control Center proves routing discovery through `/api/status`, including `routing.activeProfile`, `routing.backendBaseURL`, and `routing.defaultFarmUri`.

### 1.3 Truthful local-routing limitation

Control Center currently proves routing discovery, not a dedicated Phase 4A voice websocket proxy.

For local development:

1. Use Control Center `/api/status` to discover the active backend and default farm.
2. Treat `routing.backendBaseURL` as the canonical Phase 4A voice-session transport base URL.
3. Open the websocket directly against that backend base URL unless a later runtime packet proves a Control Center websocket proxy.

This keeps the handover truthful and avoids promising a hub transport path the repo does not currently prove.

## 2. Capability Gating The Client Must Respect

The mobile client should treat these flags as the canonical voice gate set:

- `voiceSessions`
- `voiceSessionRuntime`
- `voiceSessionStreaming`
- `voiceSessionTts`

Client policy:

1. If `voiceSessions` or `voiceSessionRuntime` is false, do not show a live voice-session flow.
2. If `voiceSessionStreaming` is false, do not open the websocket stream.
3. If `voiceSessionTts` is false, do not fetch assistant audio. Render `promptTextSl`, terminal copy, and advice text visually only.
4. Treat `voiceSessionShadowAsr`, `voiceSessionRsdoPrimary`, and `voiceSessionAudioRetentionOptIn` as descriptive runtime facts, not as required Phase 4A UI gates.

## 3. Canonical Network Flow

Use this runtime-backed sequence:

1. `GET /v1/capabilities`
2. `POST /v1/voice-sessions`
3. `GET /v1/voice-sessions/{voiceSessionUri}` when the client needs a fresh snapshot
4. `WS /v1/voice-sessions/{voiceSessionUri}/stream`
5. `GET /v1/voice-sessions/{voiceSessionUri}/events?afterSequence=<n>` for reconnect or replay
6. `GET /v1/voice-sessions/{voiceSessionUri}/assistant-audio/{assetId}` only when a prompt or advice event includes an audio asset id and TTS is enabled

Preview websocket messages currently supported:

1. `audio_config`
2. `audio_chunk`
3. `action`

Preview-safe action codes currently useful for mobile:

1. `cancel_session`
2. `barge_in`
3. `cancel_pending_commit`
4. `replay_prompt`
5. `switch_to_manual`

## 4. Rendering Rules

The client must keep these surfaces separate:

1. Transcript
   - render from `transcript_partial`, `transcript_final`, and `snapshot.latestTranscriptText`
2. Interpreted meaning
   - render from `snapshot.latestInterpretation`
3. Save result
   - render from `snapshot.semanticDecision` and `snapshot.terminalOutcome`
4. Advice eligibility and advice
   - render from `snapshot.advice`
   - only treat spoken advice as valid when the terminal outcome is `record_committed_with_advice`

Recommended UI mapping:

1. Use `snapshot.statusCode` as the primary session-state driver.
2. Use `eventCode` for incremental updates and animation only.
3. Use `snapshot.triggerContext` to explain why the session opened, not as proof that work happened.
4. Use `snapshot.terminalOutcome` as the only canonical session end summary.

## 5. Reconnect And Replay

The client should keep the highest received event sequence locally. On reconnect:

1. reload `GET /v1/voice-sessions/{voiceSessionUri}` for the latest snapshot head
2. call `GET /v1/voice-sessions/{voiceSessionUri}/events?afterSequence=<lastSeenSequence>`
3. apply replayed events in sequence order

Do not infer missed state from local guesses when replay data is available.

## 6. TTS-Disabled Behavior

If `voiceSessionTts` is false:

1. still create the session
2. still allow websocket preview streaming when `voiceSessionStreaming` is true
3. render `promptTextSl`, terminal summary text, and grounded advice text without attempting `assistant-audio` fetches
4. keep the same terminal-outcome rules

TTS-off is a rendering downgrade, not a license to skip the session contract.

## 7. Fixture Catalog

Canonical sample payloads now live under `specs/api/v1/server/fastapi/tests/fixtures/voice_session/`:

- `session_create_request.json`
- `opener_mutation.json`
- `merged_trigger_context.json`
- `transcript_update_event.json`
- `clarification_turn_mutation.json`
- `draft_terminal_mutation.json`
- `commit_terminal_mutation.json`
- `grounded_advice_terminal_mutation.json`

Use these fixtures as transport examples only. They are not seed data for backend persistence.

## 8. Local Smoke Path

The repo now includes `apps/control-center/scripts/smoke_voice_session_phase4a.py`.

Recommended local usage:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4a.py \
  --hub-base-url http://127.0.0.1:8091
```

If auth is enabled locally, provide either:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4a.py \
  --hub-base-url http://127.0.0.1:8091 \
  --jwt-secret "$FARM_RM_JWT_HS256_SECRET"
```

or:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4a.py \
  --hub-base-url http://127.0.0.1:8091 \
  --bearer-token "$FARM_RM_SMOKE_BEARER_TOKEN"
```

The smoke path:

1. resolves the active routed backend from Control Center
2. loads the canonical `session_create_request.json` fixture
3. creates a preview session
4. opens the websocket stream
5. sends `audio_config`, one preview `audio_chunk`, and a `cancel_session` action
6. verifies replay through `/events`

## 9. Explicit Non-Goals

This handover does not promise:

1. live microphone capture implementation in Swift
2. geofence scheduling
3. notification plumbing on iOS
4. live Google or RSDO ASR
5. a Control Center websocket proxy
6. a production iOS app in this repository
