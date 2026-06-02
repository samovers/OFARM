# iOS Handover: Voice Session Phase 4D

Version: 0.1 (handover)
Date: 2026-03-23
Applies to: OF Platform iOS client + Farm_RM backend preview/runtime slices for A.2 fertilization, irrigation, and A.3 harvest

This handover extends the Phase 4A and Phase 4C contracts with the new truthful Phase 4D mid-tier route slices. It is written for the mobile app and QA layers that need to understand what the backend can now save, patch, and commit without pretending later routes are already done.

## 0. What Phase 4D Adds

The runtime now supports three additional live voice routes:

1. `a2_fertilization`
   - total quantity can go through a short soft-commit window into a real fertilization event
   - rate-based statements stay draft-first as `fertilizer_application_draft`
2. `irrigation`
   - full-detail statements can soft-commit into a real irrigation event
   - duration-only or otherwise incomplete statements save `irrigation_event_draft`
3. `a3_harvest`
   - full-detail statements with an existing storage-lot match can soft-commit into a real harvest event
   - draft path stays truthful and preserves period and quantity-basis meaning in an `operationDraftUri`

These routes stay on the same `/v1/voice-sessions` control plane. The iOS client does not need a separate endpoint family for Phase 4D.

## 1. Honest Save Targets And Commit Refs

The client should expect these linked refs:

1. Fertilization draft:
   - `savedTargetUri`
   - `savedTargetTypeCode = fertilizer_application_draft`
2. Fertilization commit:
   - `executedOperationUri`
   - `fertilizerApplicationEventUri`
3. Irrigation draft:
   - `savedTargetUri`
   - `savedTargetTypeCode = irrigation_event_draft`
4. Irrigation commit:
   - `executedOperationUri`
   - `irrigationEventUri`
5. Harvest draft:
   - `operationDraftUri`
6. Harvest commit:
   - `executedOperationUri`
   - `harvestEventUri`

Do not assume every successful Phase 4D save produces `savedTargetUri`. Harvest draft remains `operationDraftUri`-based on purpose.

## 2. Soft-Commit Behavior

For Phase 4D commit-ready routes, the backend uses the same honest soft-commit buffer:

1. first mutation after the utterance:
   - `statusCode = soft_commit_pending`
   - `saveReadinessCode = commit_ready`
2. commit happens on:
   - `/v1/voice-sessions/{voiceSessionUri}/soft-commit/expire`
3. final terminal outcome:
   - usually `record_committed`
   - `record_committed_with_advice` remains possible if grounded advice becomes eligible

Client guidance:

1. keep draft and commit end states visually distinct
2. do not claim advice is available unless the terminal outcome says so
3. if commit-ready turns are resumed or patched later, keep passing `linkedRefs` through unchanged

## 3. Resume/Patch Behavior

Phase 4D now supports truthful resume/patch flows:

1. Fertilization:
   - if the new session opens with:
     - `savedTargetUri`
     - `savedTargetTypeCode = fertilizer_application_draft`
   - the draft is patched instead of duplicated
2. Irrigation:
   - if the new session opens with:
     - `savedTargetUri`
     - `savedTargetTypeCode = irrigation_event_draft`
   - the draft is patched instead of duplicated
3. Harvest:
   - if the new session opens with:
     - `operationDraftUri`
   - the draft is patched instead of duplicated

Mobile does not need a new “merge complete” concept yet. The product wording can stay “draft saved” for both create and patch.

## 4. Useful Typed-Test Sentences

Good simulator-safe typed checks:

1. Fertilization commit:
   - `Pognojil sem pšenico z UREO, 150 kg.`
   - expected route: `a2_fertilization`
   - expected terminal: committed
2. Fertilization draft:
   - `Dal sem 250 kil na hektar.`
   - expected route: `a2_fertilization`
   - expected terminal: draft saved
3. Irrigation draft:
   - `Namakal sem približno dve uri iz vodnjaka.`
   - expected route: `irrigation`
   - expected terminal: draft saved
4. Irrigation commit:
   - `Namakal sem s kapljičnim sistemom iz zbiralnika, 12 m3.`
   - expected route: `irrigation`
   - expected terminal: committed
5. Harvest draft:
   - `Žel sem od 18. 9. do 20. 9., 4 t/ha.`
   - expected route: `a3_harvest`
   - expected terminal: draft saved
6. Harvest commit:
   - `Žel sem od 18. 9. do 20. 9., 14 t, 3.4 ha, lot RFHIST-realfarm-historical-seed-v1-BUCKWHEAT-2025-GRAIN.`
   - expected route: `a3_harvest`
   - expected terminal: committed

## 5. Simulator-Safe Mobile Guidance

The simulator can still validate Phase 4D safely with typed turns. That remains the recommended path when a physical iPhone is not available.

Recommended simulator check:

1. open a session from the app’s Route Lab
2. send a typed turn
3. inspect:
   - `What We Understood`
   - `Why This Result`
   - `Result & Advice`
4. confirm:
   - draft routes show draft wording
   - commit routes show committed wording
   - event timeline reaches the expected terminal state

The simulator microphone path is still not the authoritative Phase 4D validation path.

## 6. Smoke Harness

The repo now includes:

`apps/control-center/scripts/smoke_voice_session_phase4d.py`

Recommended usage:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4d.py \
  --hub-base-url http://127.0.0.1:8091
```

The smoke harness exercises:

1. fertilization total-quantity commit
2. fertilization rate-based draft
3. irrigation duration-only draft
4. irrigation full-detail commit
5. harvest period draft
6. harvest full-detail commit with existing storage lot
7. fertilization resume/patch
8. irrigation resume/patch
9. harvest resume/patch

It emits route/save/latency data plus duplicate-draft-avoidance counts.

## 7. What Still Remains Out Of Scope

Phase 4D does not mean:

1. A.4 plant-protection live route support
2. automatic storage-lot creation during harvest logging
3. final farmer-corpus ASR signoff
4. full native iOS speech capture validation inside the backend repo
5. photo/evidence follow-up inside the same primary voice turn

Those remain later packets.
