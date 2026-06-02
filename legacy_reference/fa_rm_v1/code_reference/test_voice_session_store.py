from __future__ import annotations

import pytest

from app.voice_models import (
    AdviceReadinessCode,
    AdviceSurfaceCode,
    AuthorityClass,
    ConfidenceClass,
    CTACode,
    EntrySourceCode,
    FreshnessClass,
    LeadReasonCode,
    OpenerModeCode,
    PromptIntentCode,
    RouteCode,
    TriggerContextEnvelope,
    TriggerKindCode,
    VoiceAdviceEnvelope,
    VoiceEntryState,
    VoiceEventPayload,
    VoiceRuntimeAdapterKind,
    VoiceSessionEventCode,
    VoiceSessionStatusCode,
)
from app.voice_session_models import TriggerInboxItem, VoiceSessionSnapshot
from app.voice_session_service import build_voice_session_service
from app.voice_session_store import (
    VoiceSessionSequenceConflictError,
    VoiceSessionStoreMode,
    reset_voice_session_preview_store,
)


def setup_function() -> None:
    reset_voice_session_preview_store()


def _sample_trigger() -> TriggerInboxItem:
    return TriggerInboxItem(
        id="demo-store",
        entrySource=EntrySourceCode.manual,
        fieldLabel="Polje 12",
        leadTextSl="Povej, kaj si naredil.",
        subtitleSl="Store contract test.",
        openerModeCode=OpenerModeCode.listen_immediately,
        triggerContext=TriggerContextEnvelope(
            triggerKindCode=TriggerKindCode.manual,
            leadReasonCode=LeadReasonCode.manual_open,
            supportingReasonCodes=[],
            promptIntentCode=PromptIntentCode.manual_start,
            routeHintCode=RouteCode.a1_general_work,
            authorityClass=AuthorityClass.advisory,
            freshnessClass=FreshnessClass.fresh,
            confidenceClass=ConfidenceClass.likely,
            whyNowTextSl="Ročni začetek.",
        ),
        accentHex="#2C5E73",
    )


def _sample_snapshot(voice_session_uri: str, trigger: TriggerInboxItem) -> VoiceSessionSnapshot:
    return VoiceSessionSnapshot(
        voiceSessionURI=voice_session_uri,
        statusCode=VoiceSessionStatusCode.created,
        openerModeCode=trigger.openerModeCode,
        triggerContext=trigger.triggerContext,
        advice=VoiceAdviceEnvelope(
            adviceReadinessCode=AdviceReadinessCode.not_applicable,
            adviceSurfaceCode=AdviceSurfaceCode.none,
            ctaCode=CTACode.none,
        ),
        adapterKind=VoiceRuntimeAdapterKind.mock,
        entryState=VoiceEntryState.idle,
        currentPromptTextSl=trigger.leadTextSl,
        latestTranscriptText=None,
        latestInterpretation=None,
        semanticDecision=None,
        terminalOutcome=None,
        clarificationCount=0,
        clarificationLimit=3,
        audioConfiguration=None,
        turnIndex=0,
        pendingCommitSecondsRemaining=None,
    )


def test_voice_session_store_create_load_round_trip_uses_preview_mode() -> None:
    service = build_voice_session_service()
    trigger = _sample_trigger()
    snapshot = _sample_snapshot("urn:voice-session:test-store-round-trip", trigger)

    created = service.create_session(trigger=trigger, snapshot=snapshot)
    loaded = service.load_snapshot(snapshot.voiceSessionURI)

    assert service.store_mode == VoiceSessionStoreMode.memory_preview
    assert created.snapshot.voiceSessionURI == snapshot.voiceSessionURI
    assert created.newEvents == []
    assert loaded.voiceSessionURI == snapshot.voiceSessionURI
    assert loaded.statusCode == "created"


def test_voice_session_store_orders_and_replays_events_after_sequence() -> None:
    service = build_voice_session_service()
    trigger = _sample_trigger()
    snapshot = _sample_snapshot("urn:voice-session:test-store-replay", trigger)
    service.create_session(trigger=trigger, snapshot=snapshot)

    def _append_events(stored):
        events = [
            service.build_event(
                stored,
                VoiceSessionEventCode.session_created,
                VoiceEventPayload(detail="created"),
                recorded_at="2026-03-22T10:00:00Z",
            ),
            service.build_event(
                stored,
                VoiceSessionEventCode.stream_ready,
                VoiceEventPayload(detail="stream"),
                recorded_at="2026-03-22T10:00:01Z",
            ),
            service.build_event(
                stored,
                VoiceSessionEventCode.prompt_ready,
                VoiceEventPayload(promptTextSl="Pozdrav."),
                recorded_at="2026-03-22T10:00:02Z",
            ),
        ]
        service.append_events(stored, events)
        return [event.sequence for event in events]

    sequences = service.mutate(snapshot.voiceSessionURI, _append_events)
    replay = service.list_events(snapshot.voiceSessionURI, after_sequence=1)

    assert sequences == [1, 2, 3]
    assert [event.sequence for event in replay.items] == [2, 3]
    assert replay.total == 2


def test_voice_session_store_rejects_sequence_gaps_and_duplicate_reuse() -> None:
    service = build_voice_session_service()
    trigger = _sample_trigger()
    snapshot = _sample_snapshot("urn:voice-session:test-store-sequence-conflict", trigger)
    service.create_session(trigger=trigger, snapshot=snapshot)

    def _append_invalid_event(stored):
        invalid_event = service.build_event(
            stored,
            VoiceSessionEventCode.session_created,
            VoiceEventPayload(detail="created"),
            recorded_at="2026-03-22T10:00:00Z",
        )
        invalid_event.sequence = 7
        service.append_events(stored, [invalid_event])

    with pytest.raises(VoiceSessionSequenceConflictError):
        service.mutate(snapshot.voiceSessionURI, _append_invalid_event)
