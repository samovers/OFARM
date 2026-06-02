# OFARM Output Assembly Examples v0.1

Date: 2026-05-13  
Status: draft implementation/conformance support  
Phase: AI-agent-ready platform amendment Phase 4

## Purpose

This folder contains preview-first output assembly examples for AI coding agents.

The examples reinforce:

- PassportView is not a bucket term for every compiled output
- output previews do not create frozen truth
- DocumentAssembly requires authority, evidence, freshness, and trace posture
- stale, disputed, redacted, and permission-limited basis must be visible

## Examples

| File | Purpose |
|---|---|
| `OFARM_OutputAssemblyPreviewRequest_example_passport_field7_v0_1.json` | request non-authoritative PassportView preview |
| `OFARM_OutputAssemblyPreviewResult_example_passport_field7_v0_1.json` | return a recomputable, qualified PassportView preview |
| `OFARM_OutputAssemblyPreviewRequest_example_document_dossier_dispute_annex_v0_1.json` | request DocumentAssembly preview with dispute annex policy |
| `OFARM_OutputAssemblyPreviewResult_example_document_dossier_blocked_stale_v0_1.json` | block high-consequence document output from stale materialization |

## Usage

Generated SDK examples should call preview/dry-run before assembly and branch on `qualification.highConsequenceUseAllowed`.
