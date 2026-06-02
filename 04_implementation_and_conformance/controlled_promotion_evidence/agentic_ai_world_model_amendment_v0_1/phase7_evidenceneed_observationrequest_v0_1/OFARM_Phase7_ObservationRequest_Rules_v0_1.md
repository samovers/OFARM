# OFARM Phase 7 — ObservationRequest Rules v0.1

## Definition

`ObservationRequest` is a candidate OFARM object that asks a human, contractor, sensor process, agent, or workflow to capture a real-world observation.

## Required meaning

An `ObservationRequest` must identify:

- target scope and location;
- observation type;
- acceptable collection methods;
- acceptable artifact forms;
- minimum and preferred capture;
- deadline or relevance window;
- priority and burden;
- local-knowledge option;
- linked EvidenceNeed where applicable;
- status and satisfaction path.

## Non-goals

`ObservationRequest` is not:

- an accepted observation;
- a sensor record;
- a scouting fact;
- a compliance fact;
- a materialized current-state record;
- an automatic task assignment unless implementation policy says so.
