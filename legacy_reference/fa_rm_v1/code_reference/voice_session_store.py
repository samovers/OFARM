from __future__ import annotations

import threading
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

from app.voice_session_models import (
    TriggerInboxItem,
    VoiceAssistantAudioAsset,
    VoiceEventPayload,
    VoiceSessionEvent,
    VoiceSessionEventCode,
    VoiceSessionMutation,
    VoiceSessionSnapshot,
)

MutationResult = TypeVar("MutationResult")


class VoiceSessionStoreMode(str, Enum):
    memory_preview = "memory_preview"


class VoiceSessionNotFoundError(KeyError):
    pass


class VoiceSessionSequenceConflictError(ValueError):
    pass


@dataclass
class StoredVoiceSession:
    trigger: TriggerInboxItem
    snapshot: VoiceSessionSnapshot
    events: list[VoiceSessionEvent] = field(default_factory=list)
    next_sequence: int = 1
    audio_assets: dict[str, VoiceAssistantAudioAsset] = field(default_factory=dict)
    audio_asset_bytes: dict[str, bytes] = field(default_factory=dict)
    action_results: dict[str, VoiceSessionMutation] = field(default_factory=dict)
    speech_runtime_state: Any = None


class InMemoryVoiceSessionStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, StoredVoiceSession] = {}

    @property
    def mode(self) -> VoiceSessionStoreMode:
        return VoiceSessionStoreMode.memory_preview

    def create_session(
        self,
        *,
        trigger: TriggerInboxItem,
        snapshot: VoiceSessionSnapshot,
        initializer: Optional[Callable[[StoredVoiceSession], MutationResult]] = None,
    ) -> Optional[MutationResult]:
        voice_session_uri = str(snapshot.voiceSessionURI or "").strip()
        with self._lock:
            if voice_session_uri in self._sessions:
                raise ValueError(f"Voice session already exists: {voice_session_uri}")
            stored = StoredVoiceSession(
                trigger=TriggerInboxItem.model_validate(trigger.model_dump()),
                snapshot=clone_snapshot(snapshot),
            )
            self._sessions[voice_session_uri] = stored
            if initializer is None:
                return None
            return initializer(stored)

    def mutate_session(
        self,
        voice_session_uri: str,
        mutation: Callable[[StoredVoiceSession], MutationResult],
    ) -> MutationResult:
        with self._lock:
            stored = self._require_session(voice_session_uri)
            return mutation(stored)

    def load_snapshot(self, voice_session_uri: str) -> VoiceSessionSnapshot:
        with self._lock:
            stored = self._require_session(voice_session_uri)
            return clone_snapshot(stored.snapshot)

    def list_events(
        self,
        voice_session_uri: str,
        *,
        after_sequence: Optional[int] = None,
    ) -> list[VoiceSessionEvent]:
        with self._lock:
            stored = self._require_session(voice_session_uri)
            items = [
                event
                for event in stored.events
                if after_sequence is None or event.sequence > int(after_sequence)
            ]
            return clone_events(items)

    def build_event(
        self,
        stored: StoredVoiceSession,
        code: VoiceSessionEventCode,
        payload: VoiceEventPayload,
        *,
        recorded_at: str,
    ) -> VoiceSessionEvent:
        event = VoiceSessionEvent(
            sequence=stored.next_sequence,
            voiceSessionURI=stored.snapshot.voiceSessionURI,
            eventCode=code,
            recordedAt=recorded_at,
            turnIndex=stored.snapshot.turnIndex,
            payload=payload,
        )
        stored.next_sequence += 1
        return event

    def append_events(self, stored: StoredVoiceSession, events: list[VoiceSessionEvent]) -> None:
        expected_sequence = stored.events[-1].sequence + 1 if stored.events else 1
        for event in events:
            if event.voiceSessionURI != stored.snapshot.voiceSessionURI:
                raise VoiceSessionSequenceConflictError(
                    f"Voice session mismatch for event sequence {event.sequence}: {event.voiceSessionURI}"
                )
            if event.sequence != expected_sequence:
                raise VoiceSessionSequenceConflictError(
                    f"Expected event sequence {expected_sequence}, got {event.sequence}"
                )
            expected_sequence += 1
        stored.events.extend(events)

    def store_audio_asset(
        self,
        stored: StoredVoiceSession,
        *,
        asset: VoiceAssistantAudioAsset,
        payload: bytes,
    ) -> None:
        stored.audio_assets[asset.assetId] = VoiceAssistantAudioAsset.model_validate(asset.model_dump())
        stored.audio_asset_bytes[asset.assetId] = bytes(payload)

    def get_audio_asset(self, voice_session_uri: str, asset_id: str) -> tuple[VoiceAssistantAudioAsset, bytes]:
        with self._lock:
            stored = self._require_session(voice_session_uri)
            asset = stored.audio_assets.get(asset_id)
            payload = stored.audio_asset_bytes.get(asset_id)
            if asset is None or payload is None:
                raise KeyError(asset_id)
            return deepcopy(asset), payload

    def get_action_result(
        self,
        voice_session_uri: str,
        client_request_id: str,
    ) -> Optional[VoiceSessionMutation]:
        with self._lock:
            stored = self._require_session(voice_session_uri)
            cached = stored.action_results.get(str(client_request_id or "").strip())
            if cached is None:
                return None
            return clone_mutation(cached)

    def remember_action_result(
        self,
        stored: StoredVoiceSession,
        *,
        client_request_id: str,
        mutation: VoiceSessionMutation,
    ) -> None:
        stored.action_results[str(client_request_id or "").strip()] = clone_mutation(mutation)

    def reset(self) -> None:
        with self._lock:
            self._sessions.clear()

    def _require_session(self, voice_session_uri: str) -> StoredVoiceSession:
        stored = self._sessions.get(str(voice_session_uri or "").strip())
        if stored is None:
            raise VoiceSessionNotFoundError(str(voice_session_uri or "").strip())
        return stored


def clone_snapshot(snapshot: VoiceSessionSnapshot) -> VoiceSessionSnapshot:
    return VoiceSessionSnapshot.model_validate(snapshot.model_dump())


def clone_events(events: list[VoiceSessionEvent]) -> list[VoiceSessionEvent]:
    return [VoiceSessionEvent.model_validate(event.model_dump()) for event in events]


def clone_mutation(mutation: VoiceSessionMutation) -> VoiceSessionMutation:
    return VoiceSessionMutation.model_validate(mutation.model_dump())


_PREVIEW_VOICE_SESSION_STORE = InMemoryVoiceSessionStore()


def build_voice_session_store() -> InMemoryVoiceSessionStore:
    return _PREVIEW_VOICE_SESSION_STORE


def reset_voice_session_preview_store() -> None:
    _PREVIEW_VOICE_SESSION_STORE.reset()
