
# OFARM AI-Agent-Ready Platform Amendment Phase 5 Patch Apply Guide

Date: 2026-05-13

## Purpose

This patch adds Phase 5 workflow and UI-state artifacts on top of the Phase 0–4 preview package.

## Apply order

1. Start from `OFARM2_2026-05-13_16-01_ai_agent_ready_phase0_4_preview.zip`.
2. Overlay the contents of `OFARM2_ai_agent_ready_platform_amendment_phase5_patch_v0_1.zip` at repository root.
3. Do not move these artifacts into `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/` until promotion review passes.

## New focus

Phase 5 closes the app workflow/state-label seam:

```text
recommendation ≠ prescription ≠ work order ≠ operation claim ≠ evidence ≠ accepted execution ≠ correction ≠ dispute ≠ output
```

## Validation included

The patch includes a Phase 5 validation report confirming JSON parse checks and schema validation of bundled examples.
