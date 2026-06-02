from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
import uuid
from pathlib import Path

from fastapi.testclient import TestClient

import app.voice_engine as voice_engine_module
from app.main import app
from app.voice_models import (
    AdviceReadinessCode,
    TerminalOutcomeCode,
    TriggerContextEnvelope,
    VoiceSessionCreateRequest,
    VoiceSessionEvent,
    VoiceSessionMutation,
)

DEFAULT_FARM_URI = "https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "voice_session"
os.environ.setdefault("FARM_RM_JWT_HS256_SECRET", "test-secret")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _encode_hs256_jwt(claims: dict, *, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(claims, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}"
    signature = hmac.new(secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url_encode(signature)}"


def _auth_headers(*, farm_uri: str = DEFAULT_FARM_URI) -> dict[str, str]:
    now = int(time.time())
    token = _encode_hs256_jwt(
        {
            "sub": "test-user",
            "iat": now,
            "exp": now + 3600,
            "farmUri": farm_uri,
        },
        secret=os.environ["FARM_RM_JWT_HS256_SECRET"],
    )
    return {"Authorization": f"Bearer {token}", "X-Farm-URI": farm_uri}


client = TestClient(app, headers=_auth_headers())


def setup_function() -> None:
    voice_engine_module.reset_voice_session_preview_store()


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def _assert_roundtrip(model_type, fixture_name: str) -> None:
    payload = _load_fixture(fixture_name)
    validated = model_type.model_validate(payload)
    assert validated.model_dump(mode="json", exclude_unset=True) == payload


def test_voice_session_mobile_handover_fixtures_roundtrip() -> None:
    _assert_roundtrip(VoiceSessionCreateRequest, "session_create_request.json")
    _assert_roundtrip(VoiceSessionMutation, "opener_mutation.json")
    _assert_roundtrip(TriggerContextEnvelope, "merged_trigger_context.json")
    _assert_roundtrip(VoiceSessionEvent, "transcript_update_event.json")
    _assert_roundtrip(VoiceSessionMutation, "clarification_turn_mutation.json")
    _assert_roundtrip(VoiceSessionMutation, "draft_terminal_mutation.json")
    _assert_roundtrip(VoiceSessionMutation, "commit_terminal_mutation.json")
    _assert_roundtrip(VoiceSessionMutation, "grounded_advice_terminal_mutation.json")


def test_voice_session_mobile_handover_create_fixture_is_runtime_accepted() -> None:
    payload = _load_fixture("session_create_request.json")
    payload["trigger"]["id"] = f"{payload['trigger']['id']}-{uuid.uuid4().hex[:8]}"

    response = client.post("/v1/voice-sessions", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["snapshot"]["statusCode"] == "created"
    assert data["snapshot"]["triggerContext"]["routeHintCode"] == "scouting_note"
    assert [event["eventCode"] for event in data["newEvents"]] == [
        "session_created",
        "trigger_context_resolved",
    ]


def test_voice_session_mobile_handover_terminal_fixtures_preserve_advice_boundaries() -> None:
    draft = VoiceSessionMutation.model_validate(_load_fixture("draft_terminal_mutation.json"))
    commit_only = VoiceSessionMutation.model_validate(_load_fixture("commit_terminal_mutation.json"))
    grounded = VoiceSessionMutation.model_validate(_load_fixture("grounded_advice_terminal_mutation.json"))

    assert draft.snapshot.terminalOutcome.terminalOutcomeCode == TerminalOutcomeCode.draft_saved
    assert draft.snapshot.advice.adviceReadinessCode != AdviceReadinessCode.grounded

    assert commit_only.snapshot.terminalOutcome.terminalOutcomeCode == TerminalOutcomeCode.record_committed
    assert commit_only.snapshot.advice.adviceReadinessCode == AdviceReadinessCode.not_grounded

    assert grounded.snapshot.terminalOutcome.terminalOutcomeCode == TerminalOutcomeCode.record_committed_with_advice
    assert grounded.snapshot.advice.adviceReadinessCode == AdviceReadinessCode.grounded
