# OFARM Wave 20 profile compatibility and activation-set hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded runtime/conformance hardening for profile compatibility and PackActivationSet evaluation depth

---

## Purpose

This wave closes the previously untouched `profile compatibility tests` row and deepens the `pack activation-set compatibility checks` row without reopening OFARM law.

It stays in `04_implementation_and_conformance/` and does **not** amend:
- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

---

## Why this wave is on-plan

The original hardest-design amendment plan says the next phase after the six-wave closure set is proof and hardening rather than more architecture work. Profile compatibility is explicitly named in the constitutional minimum conformance baseline, and it remains one of the last untouched central rows in the coverage matrix.

This wave therefore:
- stays on the pack/profile/context seam already governed by RC2.1
- adds executable activation-set evidence rather than new semantics
- avoids drift into bridge-specific or deployment-specific work

---

## What this wave adds

This wave adds a bounded runtime-shaped suite for profile compatibility across the following cases:
- approved narrowing profile allowed under an already-active higher-precedence baseline
- disjoint recipient-facing view profile allowed as plain compatibility
- lower-precedence weakening attempt denied deterministically
- same-precedence output-slot conflict routed to governance
- scope-separated profile coexistence allowed
- time-window-separated seasonal profile coexistence allowed
- missing required pack dependency denied deterministically
- declared exclusion denied deterministically

It also adds activation-set depth evidence for:
- dependency checks
- exclusion checks
- cross-precedence contradiction handling
- multi-scope evaluation
- multi-time evaluation

---

## Intended conformance effect

This wave is intended to:
- move `profile compatibility tests` from `NOT_STARTED` to `COVERED`
- move `pack activation-set compatibility checks` from `PARTIAL` to `COVERED`
- strengthen, but not fully close, broader `pack compatibility tests` and `pack conflict determinism checks`

---

## Scope guardrail

This wave does **not** claim:
- full pack-manifest law closure
- full surface-family merge legality closure
- deployment-collected profile telemetry
- new machine-contract substance for profile manifests

It remains a bounded conformance proof wave against already-governed pack/profile law.
