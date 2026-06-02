# OFARM FMIS Shadow Adapter MVP v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance candidate; candidate-only

## Purpose

This MVP scope turns Phase 6 source-fidelity and import-candidate contracts into a small predevelopment adapter lane. It is designed to let a platform team test FMIS reconstruction without creating accepted OFARM truth.

## Boundary

The FMIS shadow adapter emits candidate records, source-fidelity envelopes, import receipts, loss maps, identity-resolution requests/results, and review queues.

It must not emit accepted governance facts, frozen DocumentAssemblies, Compliance Twin decisions, accepted current-state materializations, or inferred contractor identity.
