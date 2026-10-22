Review — samovers/OFARM PR #56 at 5b9b52a
Reviewed head: 5b9b52a946700acd6b48b0fe00f62a3628a8191a, one commit: "Define canonical successful authorization-path evidence [skip ci]".
Base: main at 4a3d88e, which is still the tip of main.
Delivery: #55. Consumer: #47.
Size: 1,177 files, +149,045 / −183.
• New files (1,157): 1,012 of them are fixture case directories.
• Modified files (20): all are generated indexes (CONTRACT_INDEX, MANIFEST.csv, MATERIAL_STATUS, …).
• Code under review: 297 lines, in verify_success_path.py (203), path_common.py (63), run_cases.py (18) and the 13-line opt-in wrapper.
GitHub activity: no reviews, comments or check runs exist on #56 or #55. I checked at the start and again right before writing this. CI did not run because of [skip ci], as the PR says.
Not an independent review: this review is by samovers, the PR author, so it meets no two-reviewer gate. The PR's "independent root review" is also author-side.
Classification: OFARM2's Blocker / Follow-up / Preference.
Verdict: no Blockers, five Follow-ups, two Preferences.
• The verifier is right on everything I aimed at its own checks. That includes six hostile cases that the PR's 353-case catalog never runs (§3).
• The gaps are in four places:• what it checks against the bytes: revision selectors (F1);
• what it checks inside the owner's own trace: other retained paths (F2);
• how much of its logic the evidence actually guards: 77 of 102 checks are unguarded (F3);
• one false claim about verifying its own code (F4).

• F1 is a close call. I give the case for calling it a Blocker in its section.

# | Class | Finding
-- | -- | --
F1 | Follow-up (close to Blocker) | Revision selectors are never compared with the record bytes. A profile has no way to say where a record's revision lives. Two different byte versions of one Party ID pass in one decision.
F2 | Follow-up | The verifier checks only the selected path. A trace that itself holds a lower-tuple PATH_ALLOWcandidate still passes, as do retained paths whose tuples are not valid encodings.
F3 | Follow-up | Negative cases accept any failure. Removing any one of 77 of the 102 must() checks leaves all 353 cases green. 336 of the 502 "independent" checks hit only the first two checks.
F4 | Follow-up | The code-hash check does not cover the code that actually runs. A path_common.py that shadows the real one turns a hostile case into PASS.
F5 | Follow-up | The closed result projection leaves out PR11 §17.5/§8.2 fields that #47 will need: the CP3 posture, the primary reason, the human-finalization requirement and the extractor reference/digest.
P1 | Preference | A selected path of type SHARING_GRANT_ACCESS can never pass, and it fails with the misleading DIRECT_PATH_TYPE_MISMATCH.
P2 | Preference | The intent's schemaVersion is the only owner field name that is hard-coded instead of being reached through the profile.

These are the cases F3 asks to add. K1 matters most: it is the only thing that sends a software agent through the CP3 branch.
4. Checked and decided were not findings
• Decision-bundle digest (§18.8). Exactly the two top-level members are removed. A nested decisionBundleDigest stays included, and the author's nested-bundle-field case fails correctly. The sentinel can never equal a computed sha256:value.
• format: date-time with no rfc3339-validator installed. FormatChecker silently skips it. But every date-time field reaches instant()'s regex: the result directly, the trace and snapshot by equality with the result. No gap.
• Plain == instead of equal() (line 142), and dict == on the tuple (line 134). Every binding member is a string by schema. A 1.0 tuple order equals 1 but is still pinned by the raw bytes.
• Code-point ordering of delegation IDs. Python sorted on str is code-point order, as §15.2 requires.
• Grant one-record identity (§16.1/§17.3). Digest bindings are required for the grant, delegation and sharing families. A self-digest that excludes only the top-level sourceRecordDigest matches §17.3 line 1236. Same-ID/different-bytes is rejected (K4).
• Context trust model. An expected-Party or admitted member in the context is rejected by the closed schema. The context digest is compared before parsing.
• Merge conflicts. git merge-tree shows the 20 generated index files conflicting with #47, #49, #51, #53 and #57, which all branch from 4a3d88e. That is expected for sibling drafts: whichever merges second regenerates them. It is not a defect of this PR.
• Scope. No evaluator, policy, CP3, runtime or CI change. Only generated indexes are modified, and the default suite is untouched (it passes).
5. Not checked
• A real producer profile. None exists. Every positive is the fictional profile, whose source schemas are inferred from the fixture values themselves.
• Python 3.11. I ran 3.13. Also, referencing is not pinned beside jsonschema 4.26.0.
• The 32 trailing-space warnings in the sealed log. I left them alone, as the PR asks.
6. What my method made easier than production
• The fictional schemas are closed and inferred from values. For P2 I had to extend them (adding revision and re-pinning their digests in the profile). A real producer's record carries its revision natively, so the gap is more reachable in production, not less.
• The mutation run patches two helpers for speed. It also counts a mutant as killed only when a negative case turns PASS. A check that only changes the error code counts as "survived". That is deliberate, because the runners themselves ignore codes.
• My probes reuse the author's repin(). So "coherent" means the same thing it means in the PR's own catalog.
Evidence: ofarm-pr-56-review-evidence/, containing the probe scripts and outputs, mutation.txt, the shadow-import probe and diff, the installed-runner report and the suite tail.

