# Occupancy repair 03 review evidence

This directory retains the exact candidate manifest/map and selected fresh technical review. The review found no new findings in 241 independent checks; author/installed conformance passed 296 checks. Earlier evidence at the parent and in independent-review-01/02 remains historical, not the current R3 review.

To reproduce, install the declared Python dependencies, then run `replay_independent_review.py --repo /absolute/path/to/OFARM --out /absolute/path/to/new-review-directory`. Add `--prepare-only` to reconstruct and verify the exact snapshot without executing the probes. The destination must not already exist. The script copies exact mapped bytes, verifies every sealed member, and executes the unchanged independent harness in that new directory. It does not edit the repository, run CI, authenticate source truth or authorize an effect.

Next: review the scoped repair and its exact dependency pin before separate #47 consumption.
