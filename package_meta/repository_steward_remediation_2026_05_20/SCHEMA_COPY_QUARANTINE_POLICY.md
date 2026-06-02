# Schema-copy quarantine policy

Non-active schema copies must not be used as current/default machine contracts. Use `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json`, `03_machine_contracts/CONTRACT_INDEX.json`, and `03_machine_contracts/schemas/` for current/default schema selection.

Existing same-basename copies are retained for path stability but are indexed and default-search-excluded. Future physical renames should use visible suffixes when safe.
