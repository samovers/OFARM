# OFARM Gate Sequencing and Commit Promotion Fixtures v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: starter end-to-end gate-ordering and promotion-safety fixtures for the post-amendment proof/hardening phase

---

## Purpose

These fixtures do not amend OFARM law.
They bind the already-shipped authority, evidence, materialization, publication, and commit-promotion rules into explicit gate sequences.

The goal is to close the two remaining conformance rows that were still fully open after Wave 6:
- commit-promotion safety checks
- enforcement-gate sequencing tests

---

## What this fixture set proves

The starter set checks that OFARM can represent and validate the following safety behaviors in executable form:
- a `note` may not shortcut into a `compliance fact`
- an `advisory output` may not shortcut into hard truth
- an `operation claim` does not become accepted execution truth when evidence is missing
- an `operation claim` can become accepted execution truth only after the required gates pass
- a `compliance assertion` can become a compliance fact only after evidence sufficiency and review/promotion pass
- AI-assisted finalization can stop at the authority gate with `REQUIRE_HUMAN_APPROVAL`
- a prepared action crossing a revocation boundary can be denied at final promotion
- high-consequence submission filing can pass only when authority, evidence, current-state, and publication gates line up in order

---

## Scope limits

This fixture set is intentionally narrow.
It is still fixture-level proof, not full runtime-produced gate tracing.

It does **not** yet prove:
- every event family and subtype path
- every commit class and bridge family
- executor-backed review-decision generation
- projection trace-back completion
- broad import-to-promotion sequencing

---

## Relationship to active OFARM law

These fixtures are derived from, and remain subordinate to:
- Constitution §11 commit classes and promotion law
- Constitution §12 advisory/compliance boundary
- Platform §3 enforcement chain
- Platform §4 governed materialization and freshness
- the Event Grammar and Commit Matrix companion artifact
- the accepted authority and current-state RFC set

They exist to prove sequencing discipline, not to create new semantics.
