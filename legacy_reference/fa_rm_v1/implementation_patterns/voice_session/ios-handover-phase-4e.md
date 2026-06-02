# iOS Handover: Voice Session Phase 4E

Version: 0.1 (handover)
Date: 2026-03-28
Applies to: OF Platform iOS client + Farm_RM backend preview/runtime slice for A.4 plant protection

This handover extends the Phase 4A, Phase 4C, and Phase 4D contracts with the truthful Phase 4E A.4 plant-protection slice. It is written for the mobile app and QA layers that need to understand what the backend can now save, patch, and commit without pretending later evidence-follow-up work is already done.

## 0. What Phase 4E Adds

The runtime now supports the `a4_plant_protection` route on the existing `/v1/voice-sessions` control plane.

It adds four important truths:

1. same-day unknown-outcome captures stay draft-first as `plant_protection_application_draft`
2. retrospective or explicit-outcome captures can soft-commit into a real plant-protection application event
3. product identity can come from a spoken full product name or an ambiguous spoken alias, but alias-only cases stay conservative
4. resume/patch can reopen an earlier plant-protection draft and avoid duplicate draft creation

## 1. Honest Save Targets And Commit Refs

The client should expect these linked refs:

1. Plant-protection draft:
   - `savedTargetUri`
   - `savedTargetTypeCode = plant_protection_application_draft`
2. Plant-protection commit:
   - `executedOperationUri`
   - `plantProtectionApplicationEventUri`
   - `plantProtectionEventUri`
   - `operationDraftUri`

Notes:

1. `operationDraftUri` is review-draft lineage for the committed route, not a generic replacement for the saved-target contract.
2. If a commit resumes from an existing `savedTargetUri`, that lineage remains available through the linked refs and review-draft evidence trail.

## 2. Same-Day Versus Retrospective Behavior

Phase 4E is deliberately conservative about treatment outcome:

1. same-day + unknown outcome:
   - stays `draft_saved`
   - keeps `treatmentSuccessCode = unknown`
   - records `treatmentOutcomeReasonCode = same_day_not_observed`
   - can recommend evidence follow-up via `evidenceAssistStateCode = photo_recommended`
2. same-day + explicit outcome:
   - can still commit if the route also has stable identity, dose, area, and timing
3. retrospective (`včeraj`) + explicit success/failure:
   - can commit when the route has stable identity, dose, area, and timing

Identity handling:

1. a spoken full product name plus active substance is stronger than an alias
2. alias-only capture stays conservative and draft-first until the missing identity detail is supplied
3. carrier-water dose wording remains valid when the user says the dose relative to water volume instead of per hectare

## 3. Resume/Patch Behavior

Phase 4E supports truthful resume/patch flows:

1. if the new session opens with:
   - `savedTargetUri`
   - `savedTargetTypeCode = plant_protection_application_draft`
2. the route patches the existing draft instead of creating a duplicate
3. if the resumed turn now supplies the missing identity or outcome details, the route can progress from draft to commit

Client guidance:

1. draft wording can stay “draft saved” for both create and patch paths
2. if the resumed turn commits, show the committed state distinctly from the earlier draft state
3. preserve the linked refs through resume so the app can continue to reason about the same draft lineage

## 4. Useful Typed-Test Sentences

Good simulator-safe typed checks:

1. Same-day alias draft:
   - `Na Gornjem sem skropil s Cuprablauom, pol kile na sto litrov vode.`
   - expected route: `a4_plant_protection`
   - expected terminal: draft saved
2. Same-day full-name but still incomplete draft:
   - `Na Gornjem sem skropil s Cuprablau Z 35 WG, pol kile na sto litrov vode.`
   - expected route: `a4_plant_protection`
   - expected terminal: draft saved
3. Retrospective hectare-based commit:
   - `Včeraj sem skropil s Cuprablau Z 35 WG, baker v obliki bakrovega oksiklorida, 0,5 kg na hektar, uspešno.`
   - expected route: `a4_plant_protection`
   - expected terminal: committed
4. Retrospective carrier-water commit:
   - `Včeraj sem skropil s Cuprablau Z 35 WG, aktivna snov baker v obliki bakrovega oksiklorida, pol kile na sto litrov vode, uspešno.`
   - expected route: `a4_plant_protection`
   - expected terminal: committed
5. Resume alias-to-full commit:
   - `S Cuprablau Z 35 WG, aktivna snov baker v obliki bakrovega oksiklorida, uspešno.`
   - expected route: `a4_plant_protection`
   - expected terminal: committed

## 5. Simulator-Safe Mobile Guidance

The simulator can still validate Phase 4E safely with typed turns. That remains the recommended path when a physical iPhone is not available.

Recommended simulator check:

1. open a session from the app’s Route Lab
2. send a typed turn
3. inspect:
   - `What We Understood`
   - `Why This Result`
   - `Result & Advice`
4. confirm:
   - same-day unknown-outcome turns stay draft-first
   - retrospective and explicit-outcome turns commit only when identity and dose are stable
   - resume/patch does not silently duplicate the saved target

The simulator microphone path is still not the authoritative Phase 4E validation path.

## 6. Smoke Harness

The repo now includes:

`apps/control-center/scripts/smoke_voice_session_phase4e.py`

Recommended usage:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4e.py \
  --profile-id default \
  --hub-base-url http://127.0.0.1:8091
```

The smoke harness exercises:

1. same-day alias draft
2. same-day full-name unknown draft
3. retrospective success commit
4. retrospective failure commit
5. retrospective carrier-water success commit
6. same-day success commit
7. same-day failure commit
8. same-day explicit-area commit
9. resume alias-to-full commit
10. resume unknown-to-success commit
11. resume unknown-to-failure commit

It emits route/save/latency data plus duplicate-draft-avoidance counts.

## 7. What Still Remains Out Of Scope

Phase 4E does not mean:

1. photo or evidence follow-up inside the same primary voice turn
2. automatic material-lot or invoice resolution from the utterance alone
3. final farmer-corpus ASR signoff
4. full native iOS speech-capture validation inside the backend repo

Those remain later work only if a new packet explicitly authorizes them.
