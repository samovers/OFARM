# Authorization repair 01 fresh review

The frozen owner repair passed 178 independently written semantic checks, seven process-isolated helper checks and one fresh 491-case installed CLI replay. No new actionable findings were found. This is a technical model-agent review, not formal GitHub approval or a two-human governance gate.

Install the dependencies declared in the candidate, then run `replay_independent_review.py --repo /absolute/path/to/OFARM --out /absolute/path/to/new-review-directory`. The destination must not exist. The script reconstructs and hashes every sealed candidate member, runs the two unchanged independent harnesses, and replays the installed 491-case CLI suite. Add `--prepare-only` to reconstruct and verify without running checks. It writes only in the new output directory. Its separate reports avoid overstating author mutation evidence as independent probes.

The exact selected review reports are also in the implementation fixture lane. The complete local review archive is not duplicated here; its manifest remains available. Earlier reports belong to the earlier candidate and are retained as history.

Next: review the repaired owner interface before separate #47 consumption; CI activation and merge remain separate.
