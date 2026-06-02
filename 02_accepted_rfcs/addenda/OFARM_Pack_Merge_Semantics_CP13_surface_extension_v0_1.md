# OFARM Pack Merge Semantics CP13 surface extension v0.1

Status: accepted/merged CP13 addendum; subordinate to active baseline and CP13 RFC.

Candidate CP13 pack surfaces:

- LEARNING_POLICY
- EXPERIMENT_POLICY
- OUTCOME_MEASURE_POLICY
- CAUSAL_EVIDENCE_POLICY
- FARM_MEMORY_POLICY
- FARM_MEMORY_RETRIEVAL_POLICY
- LEARNING_OUTPUT_QUALIFICATION_POLICY

Default merge posture:

- evidence and claim-related learning policy: STRONGEST_REQUIREMENT or HARD_FAIL;
- outcome measure policy: IDENTICAL_ONLY for claim-bearing/high-consequence use unless equivalence is proven;
- farm-memory retrieval policy: STRONGEST_REQUIREMENT;
- causal evidence policy: STRONGEST_REQUIREMENT;
- conflicting learning promotion policy: HARD_FAIL.
