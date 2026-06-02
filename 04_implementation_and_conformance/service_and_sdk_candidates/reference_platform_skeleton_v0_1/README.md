# OFARM reference platform skeleton candidate v0.1

Status: implementation/conformance support only.

This skeleton gives AI coding agents a safe starting architecture for implementing an OFARM platform without flattening OFARM into CRUD or copying platform internals into applications.

## Main rule

Apps and SDKs use public operation surfaces. They do not import platform service internals.

## Included

- `OFARM_ReferencePlatformSkeletonManifest_v0_1.json`
- `OFARM_ModuleImportBoundaryMatrix_v0_1.json`
- `packages/` candidate platform modules
- `apps/` sample app shells that must use SDK only

## Not included

This is not a production implementation, storage design, deployment topology, database schema, or active baseline amendment. It is a scaffolding and conformance artifact.
