# OFARM alignment-register gap example family v0.1

Date: 2026-04-17  
Status: active supporting implementation artifact  
Scope: add minimal non-self-referential workspace evidence for `Variety / cultivar`, `LocalConditionPattern`, and `PlannedIntervention` without reopening baseline law

---

## 1. Purpose

The original alignment-register coverage wave left three concepts as explicit follow-on targets:
- `Variety / cultivar`
- `LocalConditionPattern`
- `PlannedIntervention`

This note closes that seam with a small worked orchard example that uses the concepts directly in conformance-side material rather than only in coverage bookkeeping.

---

## 2. Worked orchard example

### 2.1 Variety / cultivar
Field 17 contains apple rows managed as cultivar-specific operational units.
In this scenario the recorded variety / cultivar is **Gala**, and the vocabulary-bound variety/cultivar reference remains the controlled semantic anchor rather than an OFARM-invented replacement term.

### 2.2 LocalConditionPattern
Field 17 also carries a recurring **LocalConditionPattern**: a west-edge frost pocket that delays morning dry-down and increases early-season mildew pressure after cool, still nights.
That pattern is local, recurrent, and operationally relevant, but it is not a universal farm-wide property.

### 2.3 PlannedIntervention
Given the cultivar-specific fruit-load target and the west-edge frost-pocket condition pattern, the farmer creates a **PlannedIntervention** for row-selective pruning and canopy opening before the next mildew-risk window.
The later execution claim, accepted consequence, and successor corrected outputs remain separate from the plan itself.

---

## 3. Why this note is narrow

This note does not add new constitutional or RFC law.
It only closes the remaining low-cost semantic seam so the coverage runner can find explicit non-register evidence for the three named concepts.
