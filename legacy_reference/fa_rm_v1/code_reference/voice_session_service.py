from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar

from app.persistence_voice_saved_targets import (
    VoiceSavedTargetStore,
    build_voice_saved_target_store,
)
from app.voice_saved_target_models import (
    A1SourceEntryDraftTarget,
    A5SourcePlanDraftTarget,
    FertilizerApplicationDraftTarget,
    IrrigationEventDraftTarget,
    PlantProtectionApplicationDraftTarget,
    ScoutingObservationDraftTarget,
    VoiceSavedTarget,
)
from app.voice_session_models import (
    TriggerInboxItem,
    VoiceAssistantAudioAsset,
    VoiceEventPayload,
    VoiceSessionEvent,
    VoiceSessionEventCode,
    VoiceSessionEventListResponse,
    VoiceSessionMutation,
    VoiceSessionSnapshot,
)
from app.voice_session_store import (
    InMemoryVoiceSessionStore,
    StoredVoiceSession,
    VoiceSessionStoreMode,
    build_voice_session_store,
    clone_events,
    clone_mutation,
    clone_snapshot,
)

MutationResult = TypeVar("MutationResult")


@dataclass(frozen=True)
class VoiceSessionService:
    store: InMemoryVoiceSessionStore
    saved_target_store: VoiceSavedTargetStore

    @property
    def store_mode(self) -> VoiceSessionStoreMode:
        return self.store.mode

    def create_session(
        self,
        *,
        trigger: TriggerInboxItem,
        snapshot: VoiceSessionSnapshot,
        initialize: Optional[Callable[[StoredVoiceSession], list[VoiceSessionEvent]]] = None,
    ) -> VoiceSessionMutation:
        def _initializer(stored: StoredVoiceSession) -> VoiceSessionMutation:
            new_events = list(initialize(stored)) if initialize is not None else []
            self.store.append_events(stored, new_events)
            return self.build_mutation(stored, new_events=new_events)

        created = self.store.create_session(
            trigger=trigger,
            snapshot=snapshot,
            initializer=_initializer,
        )
        if created is not None:
            return created
        return VoiceSessionMutation(snapshot=clone_snapshot(snapshot), newEvents=[])

    def mutate(
        self,
        voice_session_uri: str,
        mutation: Callable[[StoredVoiceSession], MutationResult],
    ) -> MutationResult:
        return self.store.mutate_session(voice_session_uri, mutation)

    def load_snapshot(self, voice_session_uri: str) -> VoiceSessionSnapshot:
        return self.store.load_snapshot(voice_session_uri)

    def list_events(
        self,
        voice_session_uri: str,
        *,
        after_sequence: Optional[int] = None,
    ) -> VoiceSessionEventListResponse:
        items = self.store.list_events(voice_session_uri, after_sequence=after_sequence)
        return VoiceSessionEventListResponse(total=len(items), items=items)

    def build_event(
        self,
        stored: StoredVoiceSession,
        code: VoiceSessionEventCode,
        payload: VoiceEventPayload,
        *,
        recorded_at: str,
    ) -> VoiceSessionEvent:
        return self.store.build_event(stored, code, payload, recorded_at=recorded_at)

    def append_events(self, stored: StoredVoiceSession, events: list[VoiceSessionEvent]) -> None:
        self.store.append_events(stored, events)

    def build_mutation(
        self,
        stored: StoredVoiceSession,
        *,
        new_events: list[VoiceSessionEvent],
    ) -> VoiceSessionMutation:
        return VoiceSessionMutation(
            snapshot=clone_snapshot(stored.snapshot),
            newEvents=clone_events(new_events),
        )

    def store_audio_asset(
        self,
        stored: StoredVoiceSession,
        *,
        asset: VoiceAssistantAudioAsset,
        payload: bytes,
    ) -> None:
        self.store.store_audio_asset(stored, asset=asset, payload=payload)

    def get_audio_asset(self, voice_session_uri: str, asset_id: str) -> tuple[VoiceAssistantAudioAsset, bytes]:
        return self.store.get_audio_asset(voice_session_uri, asset_id)

    def get_action_result(self, voice_session_uri: str, client_request_id: str) -> Optional[VoiceSessionMutation]:
        return self.store.get_action_result(voice_session_uri, client_request_id)

    def remember_action_result(
        self,
        stored: StoredVoiceSession,
        *,
        client_request_id: str,
        mutation: VoiceSessionMutation,
    ) -> None:
        self.store.remember_action_result(
            stored,
            client_request_id=client_request_id,
            mutation=clone_mutation(mutation),
        )

    def get_speech_runtime_state(self, stored: StoredVoiceSession) -> Any:
        return stored.speech_runtime_state

    def set_speech_runtime_state(self, stored: StoredVoiceSession, state: Any) -> None:
        stored.speech_runtime_state = state

    def store_scouting_observation_draft(
        self,
        target: ScoutingObservationDraftTarget,
    ) -> ScoutingObservationDraftTarget:
        return self.saved_target_store.save_scouting_observation_draft(target)

    def store_a1_source_entry_draft(
        self,
        target: A1SourceEntryDraftTarget,
    ) -> A1SourceEntryDraftTarget:
        return self.saved_target_store.save_a1_source_entry_draft(target)

    def store_fertilizer_application_draft(
        self,
        target: FertilizerApplicationDraftTarget,
    ) -> FertilizerApplicationDraftTarget:
        return self.saved_target_store.save_fertilizer_application_draft(target)

    def store_irrigation_event_draft(
        self,
        target: IrrigationEventDraftTarget,
    ) -> IrrigationEventDraftTarget:
        return self.saved_target_store.save_irrigation_event_draft(target)

    def store_a5_source_plan_draft(
        self,
        target: A5SourcePlanDraftTarget,
    ) -> A5SourcePlanDraftTarget:
        return self.saved_target_store.save_a5_source_plan_draft(target)

    def store_plant_protection_application_draft(
        self,
        target: PlantProtectionApplicationDraftTarget,
    ) -> PlantProtectionApplicationDraftTarget:
        return self.saved_target_store.save_plant_protection_application_draft(target)

    def get_saved_target(self, saved_target_uri: str) -> VoiceSavedTarget:
        return self.saved_target_store.get_saved_target(saved_target_uri)

    def patch_saved_target(self, saved_target_uri: str, changes: dict[str, Any]) -> VoiceSavedTarget:
        return self.saved_target_store.patch_saved_target(saved_target_uri, changes)

    def list_due_plant_protection_application_drafts(
        self,
        *,
        farm_uri: str,
        due_before: str | None = None,
    ) -> list[PlantProtectionApplicationDraftTarget]:
        return self.saved_target_store.list_due_plant_protection_application_drafts(
            farm_uri=farm_uri,
            due_before=due_before,
        )


def build_voice_session_service(
    *,
    store: InMemoryVoiceSessionStore | None = None,
    saved_target_store: VoiceSavedTargetStore | None = None,
) -> VoiceSessionService:
    return VoiceSessionService(
        store=store or build_voice_session_store(),
        saved_target_store=saved_target_store or build_voice_saved_target_store(),
    )
