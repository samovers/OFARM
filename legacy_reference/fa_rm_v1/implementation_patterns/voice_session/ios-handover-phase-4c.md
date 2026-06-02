# iOS Handover: Voice Session Phase 4C

Version: 0.1 (handover)
Date: 2026-03-23
Applies to: OF Platform iOS client + Farm_RM backend preview/runtime slices for A.1 general work and A.5 plan change

This handover extends the Phase 4A contract with the new truthful Phase 4C route slices. It is written for the mobile app and QA layers that need to understand what the backend can now save, patch, and summarize without inferring that unsupported families are already done.

## 0. What Phase 4C Adds

The runtime now supports two additional live voice routes beyond scouting:

1. `a1_general_work`
   - can distinguish structured family work from general-safe fallback work
   - structured family work saves or patches an `operation_draft`
   - general-safe work saves or patches an `a1_source_entry_draft.v1`
2. `a5_plan_change`
   - saves or patches an `a5_source_plan_draft.v1`
   - stays draft-first in this phase

These routes are live in the same `/v1/voice-sessions` control plane. The client does not need a separate endpoint family for Phase 4C.

## 1. New Honest Save Targets

Phase 4C adds these truthful draft targets:

1. `a1_source_entry_draft`
   - schema: `a1_source_entry_draft.v1`
   - used when work is legitimate A.1 content but not cleanly mappable to a structured operation family
2. `a5_source_plan_draft`
   - schema: `a5_source_plan_draft.v1`
   - used for planning/rotation updates

Structured A.1 continues to use `operationDraftUri` instead of the generic saved-target family.

## 2. Linked Refs The Client Must Expect

The mobile client should treat these terminal linked refs as canonical:

1. Structured A.1:
   - `operationDraftUri`
2. General-safe A.1:
   - `savedTargetUri`
   - `savedTargetTypeCode = a1_source_entry_draft`
3. A.5 plan change:
   - `savedTargetUri`
   - `savedTargetTypeCode = a5_source_plan_draft`

Do not assume every successful draft path produces `savedTargetUri`. Structured A.1 is intentionally different.

## 3. Resume/Patch Behavior

The backend now supports truthful resume/patch behavior for these Phase 4C targets:

1. If a new session opens with `triggerContext.linkedRefs.operationDraftUri`, structured A.1 can patch that existing `operation_draft`.
2. If a new session opens with:
   - `savedTargetUri`
   - `savedTargetTypeCode = a1_source_entry_draft`
   then general-safe A.1 can patch the existing A.1 source-entry draft.
3. If a new session opens with:
   - `savedTargetUri`
   - `savedTargetTypeCode = a5_source_plan_draft`
   then A.5 can patch the existing plan draft instead of duplicating it.

For mobile:

1. Keep showing the same “draft saved” end state when a patch happens.
2. If linked refs are present on the trigger/opening context, pass them through unchanged.
3. Do not invent a separate “merge completed” UI concept yet. Phase 4C keeps the product wording simple.

## 4. Useful Typed-Test Sentences

These are good typed-session checks for the current runtime:

1. A.1 structured:
   - `Sejal sem lan.`
   - expected route: `a1_general_work`
   - expected family: `planting`
   - expected linked ref: `operationDraftUri`
2. A.1 general-safe:
   - `Samo zrahljal sem malo po robu.`
   - expected route: `a1_general_work`
   - expected linked ref: `savedTargetUri` + `a1_source_entry_draft`
3. A.5 create:
   - `Naslednje leto bo tukaj ajda.`
   - expected route: `a5_plan_change`
   - expected linked ref: `savedTargetUri` + `a5_source_plan_draft`
4. A.5 patch:
   - first: `Naslednje leto bo tukaj ajda.`
   - second, resumed with linked refs: `Naslednje leto bo tukaj ajda, po njej pa detelja.`
   - expected result: same `savedTargetUri`, now patched with catch crop

## 5. Simulator-Safe Mobile Guidance

The simulator can still use typed turns safely. That remains the recommended validation path when a physical iPhone is not available.

For simulator-safe validation:

1. open a session from the app’s Route Lab
2. send a typed turn
3. inspect:
   - `What We Understood`
   - `Why This Result`
   - `Result & Advice`
4. confirm the final route family matches the sentence family above

The simulator microphone path is still not the authoritative Phase 4C validation path.

## 6. Smoke Harness

The repo now includes:

`apps/control-center/scripts/smoke_voice_session_phase4c.py`

Recommended usage:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4c.py \
  --hub-base-url http://127.0.0.1:8091
```

The smoke harness exercises:

1. A.1 structured create
2. A.1 general-safe create
3. A.5 single-year create
4. A.1 resume/patch without manual database edits
5. A.5 resume/patch without manual database edits

It emits route/save/latency data plus duplicate-draft-avoidance counts.

## 7. What Still Remains Out Of Scope

Phase 4C does not mean:

1. direct visible commit for structured A.1 families
2. live A.2 fertilization, A.3 harvest, irrigation, or A.4 plant protection slices
3. a full native iOS implementation inside the backend repo
4. pilot-farmer validation of spoken audio quality

Those remain later packets.
