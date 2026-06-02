# AAI-CP3 disposition memo

Disposition: promote to active baseline clarification, accepted RFC, and active machine contracts.

## Rationale

The synthesis finding identified promotion sequencing as the main bottleneck. CP3 promotes only the minimum actorship and sponsor-bound authority layer needed before agent run/handoff law can be safely addressed.

## Controlled scope

CP3 creates no autonomous software-agent authority. It requires agent actions to resolve sponsor, executing instance, actorship basis, authority snapshot, revocation state, action-class posture, and authorization trace.

## Risk controls

- Model/tool/session identity is explicitly not authority.
- Missing sponsor or authority snapshot blocks the action.
- Active revocation blocks or requires review.
- Human-governed defaults remain in force.
- Handoff, run trace, blocked-action trace, and tool-manifest law remain unpromoted.

## CP3 quality patch — authority-action posture map

Added `03_machine_contracts/maps/authority/OFARM_Agent_Authority_Action_Class_Posture_Map_v0_1.json` so every software-agent AuthorityActionClass posture is explicitly declared rather than left as prose-only guidance.
