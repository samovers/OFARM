# OFARM Phase 7 — Farmer Burden and Noise Control Rules v0.1

## Required controls

Generated requests must include:

- farmer-facing title;
- reason;
- consequence if unresolved;
- priority;
- burden estimate;
- deadline or relevance window;
- acceptable completion criteria;
- deduplication key;
- suppress/collapse policy;
- source run/model/preflight reference where applicable.

## Noise-control outcomes

A platform may:

- emit a request;
- collapse duplicate requests;
- suppress a low-value request;
- convert a vague request into a review prompt;
- downgrade a blocker;
- escalate a high-consequence blocker;
- expire or supersede stale requests.

## Farmer-facing principle

A farmer should be able to understand every request as:

> What is needed, why it matters, what counts as acceptable, how urgent it is, how much effort it likely takes, and what happens if it is ignored.
