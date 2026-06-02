
# OFARM Phase 5 Workflow and UI-State Conformance Gates v0.1

Date: 2026-05-13  
Status: candidate implementation/conformance gate  
Scope: AI application-builder workflow and UI-state safety

## Gate objective

A platform/app implementation must prove that AI-built client workflows preserve OFARM state boundaries. Passing API validation is not enough. The implementation must also preserve safe labels, state transitions, trace visibility, and forbidden shortcuts.

## Required gates

### P5-G1 — State matrix coverage

The implementation must load the application workflow state matrix and apply its safe/forbidden labels in generated UI or SDK examples.

Fail if:

- operation claim is labeled completed, verified, or accepted;
- recommendation is labeled approved, prescribed, or compliant;
- materialization is labeled source of truth;
- restricted data is rendered as no data exists;
- every compiled output is called passport.

### P5-G2 — Recipe operation discipline

Each cookbook recipe must use public operation references from the public surface candidate or documented platform boundary. It must not call internal stores.

Fail if any recipe or generated example writes:

```text
canonical assertion store
materialization store
promotion state
authority decision state
publication/frozen output state
```

### P5-G3 — Golden path compatibility

A generated app must implement the golden path without collapsing:

```text
recommendation → prescription → work order → operation claim → evidence → accepted execution → materialization → PassportView preview
```

Fail if accepted execution appears before promotion or if PassportView preview is treated as a filed/frozen document.

### P5-G4 — Hard path safety

A generated app must implement delayed sync/revocation/dispute/correction behavior without accepting offline drafts, hiding disputes, or using invalid materialization for high-consequence output.

### P5-G5 — Trace and qualification visibility

Every displayed accepted execution, current-state view, query result, PassportView preview, and DocumentAssembly preview must provide trace or qualification access.

### P5-G6 — Two-agent state-machine equivalence

Two independent AI coding agents given the same package should produce compatible state machines. Differences in endpoint naming may be allowed only if public operation references, state meanings, and forbidden labels remain equivalent.

## Phase 5 exit criterion

Phase 5 exits when bundled schemas/examples validate and the conformance matrix identifies executable checks for each state-collapse risk.
