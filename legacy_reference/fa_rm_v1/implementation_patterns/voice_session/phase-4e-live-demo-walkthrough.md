# Phase 4E Live Demo Walkthrough

Status: `current demo script`
Audience: demo operator, reviewer, or presenter
Use this when you want to walk someone through the current Phase 4E A.4 plant-protection voice slice live.

## Purpose

This walkthrough is for the current Phase 4E packet only.

It is designed to show:

- the A.4 plant-protection voice route as currently landed
- same-day draft-first truth when treatment outcome is not yet honestly known
- retrospective and explicit-outcome commit support
- resume/patch continuity for an earlier plant-protection draft

It is not a broad product tour and it does not widen Packet 08, public investigator routes, or the current voice-session contract line.

## Preconditions

- the local Control Center stack is available
- the operator understands the smoke runs against the currently routed local profile
- the operator understands the smoke may leave local append-only draft or committed voice artifacts behind

## Fast presenter framing

Open with this:

`This demo shows the current Phase 4E A.4 plant-protection voice slice. The point is not to claim a bigger product surface. The point is to show that same-day unknown outcome stays draft-first, while retrospective or explicit-outcome detail can move through the real commit path.`

## Demo sequence

### Step 1: frame the Phase 4E boundary

Show:

- [voice-session-ios-handover-phase-4e.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/voice-session-ios-handover-phase-4e.md)

Say:

`Phase 4E is a route-specific closeout for A.4 plant protection. It is not a new investigator packet and it does not imply broader evidence-follow-up support.`

### Step 2: open the local voice surface

Run:

```bash
cd "/Users/einstein/Documents/Codex/Semantic farming/apps/control-center"
./run_stack.sh
```

Open:

- [Control Center](http://127.0.0.1:8091)

Say:

`Control Center is the operator-facing launcher for the current local voice walkthrough family.`

### Step 3: run the Phase 4E smoke harness

Run:

```bash
cd "/Users/einstein/Documents/Codex/Semantic farming"
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4e.py --profile-id default --hub-base-url http://127.0.0.1:8091
```

Or launch the same command from the `Demo Scenarios` view in Control Center.

Say:

`This smoke drives the same route families we use for truthful same-day draft, retrospective commit, and resume/patch coverage.`

### Step 4: inspect the outcome families

Call out:

- same-day alias capture stays draft-first
- same-day unknown-outcome full-name capture stays draft-first
- retrospective success/failure commits can produce real plant-protection events
- carrier-water dose wording is accepted
- resume/patch keeps duplicate-draft avoidance visible

Expected result:

- the smoke output reports all Phase 4E scenarios as successful
- the report includes duplicate-draft-avoidance counts for resume cases

### Step 5: anchor the honesty boundary

Say:

`This proves the current Phase 4E route slice only. It does not imply in-turn photo follow-up, automatic evidence resolution, or broader native speech signoff.`

## If something fails

### If the smoke harness fails immediately

Check:

- Control Center is up
- the routed backend is reachable
- the local profile has a resolvable field and crop anchor

Then rerun:

```bash
.venv/bin/python apps/control-center/scripts/smoke_voice_session_phase4e.py --profile-id default --hub-base-url http://127.0.0.1:8091
```

### If same-day cases commit when they should stay draft-first

Stop the demo and say:

`The value of this packet is truthful same-day behavior, so we stop here rather than presenting a looser interpretation as finished.`

### If retrospective cases fail to commit

Check:

- the active routed profile still resolves field and crop context
- the backend process is current and was restarted after the latest code changes

If it still fails, fall back to the targeted test evidence and record the live smoke issue separately.

## Closing statement

Close with this:

`Phase 4E proves the current A.4 plant-protection voice route: honest same-day draft truth, retrospective or explicit-outcome commit support, and resume/patch continuity. Nothing broader is implied until a later packet explicitly authorizes it.`
