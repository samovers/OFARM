from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.voice_models import (
    AudioCaptureConfiguration,
    VOICE_PROTOCOL_VERSION,
    VoiceSessionActionCode,
    VoiceSessionHTTPFallbackContinuationRequest,
    VoiceSessionHTTPFallbackContinuationResponse,
    VoiceSessionMutation,
    VoiceSessionResumeHandshakeRequest,
    VoiceSessionResumeHandshakeResponse,
)


class VoiceSessionStreamAudioChunkRequest(BaseModel):
    chunkIndex: int
    audioBase64: str
    durationMs: int
    startedAtOffsetMs: int


def build_voice_session_router(bindings: Any) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/v1/voice-sessions/{voiceSessionUri}/stream/audio-config",
        response_model=VoiceSessionMutation,
        response_model_exclude_none=True,
    )
    def prepare_voice_session_stream_audio(
        voiceSessionUri: str,
        request: AudioCaptureConfiguration,
    ) -> VoiceSessionMutation:
        if not bindings._voice_feature_enabled("voiceSessionStreaming"):
            raise HTTPException(
                status_code=403,
                detail=bindings.ErrorResponse(
                    code="voice_session_streaming_disabled",
                    message="Voice session streaming is disabled.",
                ).model_dump(),
            )
        try:
            return bindings._voice_runtime_service().prepare_audio(voiceSessionUri, request)
        except KeyError as exc:
            raise HTTPException(
                status_code=404,
                detail=bindings.ErrorResponse(
                    code="voice_session_not_found",
                    message="Voice session was not found.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=bindings.ErrorResponse(
                    code="invalid_voice_stream_audio_config",
                    message="Voice stream audio config payload is invalid.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc

    @router.post(
        "/v1/voice-sessions/{voiceSessionUri}/stream/audio-chunks",
        response_model=VoiceSessionMutation,
        response_model_exclude_none=True,
    )
    def preview_voice_session_stream_audio_chunk(
        voiceSessionUri: str,
        request: VoiceSessionStreamAudioChunkRequest,
    ) -> VoiceSessionMutation:
        if not bindings._voice_feature_enabled("voiceSessionStreaming"):
            raise HTTPException(
                status_code=403,
                detail=bindings.ErrorResponse(
                    code="voice_session_streaming_disabled",
                    message="Voice session streaming is disabled.",
                ).model_dump(),
            )
        try:
            return bindings._voice_runtime_service().preview_audio_chunk(
                voiceSessionUri,
                chunk_index=request.chunkIndex,
                audio_base64=request.audioBase64,
                duration_ms=request.durationMs,
                started_at_offset_ms=request.startedAtOffsetMs,
            )
        except KeyError as exc:
            raise HTTPException(
                status_code=404,
                detail=bindings.ErrorResponse(
                    code="voice_session_not_found",
                    message="Voice session was not found.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=bindings.ErrorResponse(
                    code="invalid_voice_stream_audio_chunk",
                    message="Voice stream audio chunk payload is invalid.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc

    @router.post(
        "/v1/voice-sessions/{voiceSessionUri}/stream/audio-chunks/continuation",
        response_model=VoiceSessionHTTPFallbackContinuationResponse,
        response_model_exclude_none=True,
    )
    def continue_voice_session_http_fallback(
        voiceSessionUri: str,
        request: VoiceSessionHTTPFallbackContinuationRequest,
    ) -> VoiceSessionHTTPFallbackContinuationResponse:
        if not bindings._voice_feature_enabled("voiceSessionStreaming"):
            raise HTTPException(
                status_code=403,
                detail=bindings.ErrorResponse(
                    code="voice_session_streaming_disabled",
                    message="Voice session streaming is disabled.",
                ).model_dump(),
            )
        try:
            return bindings._voice_runtime_service().http_fallback_continuation(
                voiceSessionUri,
                failed_chunk_index=request.failedChunkIndex,
            )
        except KeyError as exc:
            raise HTTPException(
                status_code=404,
                detail=bindings.ErrorResponse(
                    code="voice_session_not_found",
                    message="Voice session was not found.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail=bindings.ErrorResponse(
                    code="invalid_voice_stream_audio_chunk_continuation",
                    message="Voice stream audio chunk continuation payload is invalid.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc

    @router.post(
        "/v1/voice-sessions/{voiceSessionUri}/resume-handshake",
        response_model=VoiceSessionResumeHandshakeResponse,
        response_model_exclude_none=True,
    )
    def resume_voice_session_stream(
        voiceSessionUri: str,
        request: VoiceSessionResumeHandshakeRequest,
    ) -> VoiceSessionResumeHandshakeResponse:
        if not bindings._voice_feature_enabled("voiceSessionStreaming"):
            raise HTTPException(
                status_code=403,
                detail=bindings.ErrorResponse(
                    code="voice_session_streaming_disabled",
                    message="Voice session streaming is disabled.",
                ).model_dump(),
            )
        try:
            return bindings._voice_runtime_service().resume_handshake(
                voiceSessionUri,
                last_acked_sequence=request.lastAckedSequence,
            )
        except KeyError as exc:
            raise HTTPException(
                status_code=404,
                detail=bindings.ErrorResponse(
                    code="voice_session_not_found",
                    message="Voice session was not found.",
                    details=[str(exc)],
                ).model_dump(),
            ) from exc

    @router.websocket("/v1/voice-sessions/{voiceSessionUri}/stream")
    async def voice_session_stream(websocket: WebSocket, voiceSessionUri: str) -> None:
        if not bindings._voice_feature_enabled("voiceSessionStreaming"):
            await websocket.close(code=4403, reason="voice session streaming disabled")
            return
        try:
            bindings._voice_runtime_service().get_session(voiceSessionUri)
        except KeyError:
            await websocket.close(code=4404, reason="voice session not found")
            return

        await websocket.accept()
        after_sequence_raw = websocket.query_params.get("afterSequence")
        if after_sequence_raw:
            try:
                replay = bindings._voice_runtime_service().list_events(
                    voiceSessionUri,
                    after_sequence=int(after_sequence_raw),
                )
                for event in replay.items:
                    await websocket.send_json(event.model_dump(mode="json"))
            except Exception:
                await websocket.close(code=4400, reason="invalid afterSequence")
                return

        try:
            while True:
                message = await websocket.receive_json()
                protocol_version = str(message.get("protocolVersion") or "").strip()
                if not protocol_version:
                    await websocket.close(code=4400, reason="missing protocolVersion")
                    return
                if protocol_version != VOICE_PROTOCOL_VERSION:
                    await websocket.close(code=4400, reason="unsupported protocolVersion")
                    return
                message_code = str(message.get("messageCode") or "").strip().lower()
                payload = message.get("payload") or {}
                if not isinstance(payload, dict):
                    await websocket.close(code=4400, reason="invalid payload")
                    return
                if message_code == "audio_config":
                    configuration = AudioCaptureConfiguration.model_validate(payload)
                    mutation = bindings._voice_runtime_service().prepare_audio(voiceSessionUri, configuration)
                elif message_code == "audio_chunk":
                    mutation = bindings._voice_runtime_service().preview_audio_chunk(
                        voiceSessionUri,
                        chunk_index=int(payload.get("chunkIndex") or 0),
                        audio_base64=str(payload.get("audioBase64") or ""),
                        duration_ms=int(payload.get("durationMs") or 0),
                        started_at_offset_ms=int(payload.get("startedAtOffsetMs") or 0),
                    )
                elif message_code == "action":
                    action_code = VoiceSessionActionCode(str(payload.get("actionCode") or "").strip())
                    mutation = bindings._voice_runtime_service().perform_action(
                        voiceSessionUri,
                        action_code,
                        client_request_id=payload.get("clientRequestId"),
                    )
                else:
                    await websocket.close(code=4400, reason="unsupported messageCode")
                    return
                for event in mutation.newEvents:
                    await websocket.send_json(event.model_dump(mode="json"))
                if any(
                    event.eventCode.value in {"session_cancelled", "terminal_outcome", "session_failed"}
                    for event in mutation.newEvents
                ):
                    return
        except WebSocketDisconnect:
            return
        except ValueError as exc:
            await websocket.close(code=4400, reason=str(exc)[:120] or "invalid stream payload")
        except KeyError:
            await websocket.close(code=4404, reason="voice session not found")
        except Exception:
            await websocket.close(code=1011, reason="voice session stream failed")

    return router
