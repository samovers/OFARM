# Exact source projection contract

These are named projections of complete, schema-validated original records selected by the independently pinned source profile. They are not free-form predicates, expected-Party hints, admission flags, or a replacement authorization evaluator. All unprojected fields remain in the original-byte and canonical-value hashes.

| Core source | Required projection content compared by this interface |
|---|---|
| REQUEST | `requestId`, `actionClass`, complete `intentBinding`, `effectIntentDigest`, `effectIntentCanonicalization` |
| RESULT | Closed `types.schema.json#/$defs/resultProjection`, with selected path, Party/basis, rule/policy identity, exact intent/schema/view/snapshot bindings and decision times |
| TRACE | Closed `traceProjection`, same result/request/rule/intent/snapshot context, unique path identities, complete retained paths and typed basis references |
| POLICY | `policyId`, `policyVersion`; the JCS digest covers the selected complete packaged policy record |
| RULE | `selectedRuleId`, `ruleRevision`, `actionClass`, `intentSchema`; the JCS digest covers the selected complete per-action semantic-closure record |
| BINDING_MANIFEST | Exact `policyBinding` and `ruleBinding` |
| EFFECT_INTENT | Complete original record validated against the rule-selected schema ID/version/raw schema digest; its complete JCS digest is compared with request/result/trace |
| DERIVED_VIEW | Exact `intentBinding` and `actionClass`; complete original view digest |
| AUTHORIZATION_VIEW_EXTRACTOR | Complete independently selected declarative extractor bytes, with a digest binding compared to rule, result, trace and derived view; no extractor is executed |
| EVALUATION_SNAPSHOT | Closed `snapshotProjection`: policy, evaluation time, history position, three index watermarks, principal-resolution binding, resolved evidence-policy registry and sovereignty-policy bindings, complete typed visible-basis entries, and CP3 snapshot binding for agent paths |

The successful path is the exact object found at the result's `selectedPathId` in the retained full trace. Every selected basis entry carries a semantic role, source key, artifact family, immutable binding, and a separately resolved snapshot-visibility record. The basis-ref array must equal the complete ordered entry binding list. General source keys are resolution addresses inside the independently selected catalog; they never carry proof by themselves.

Every visibility projection supplies `sourceBinding` and `snapshotBinding`. The corresponding snapshot entry supplies the source binding, artifact family, and the visibility record's immutable binding. All three records are independently pinned and must agree. Verifying these equalities does not authenticate visibility or prove the owner index was complete.

The four bases require these distinct source relationships:

| Basis | Compared source relationships |
|---|---|
| NATURAL_PERSON_SELF | Authenticated principal → resolution → natural-person Party = authority-subject Party; source grant targets that Party or a RoleAssignment whose Party matches |
| REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION | Natural-person resolution plus representation record's `naturalPersonPartyRef` and `representedPartyRef`; represented Party = authority-subject Party; source grant/role targets that Party |
| AGENT_PARTY_DIRECT_GRANT | Agent principal resolution and recognized identity (`agentInstanceRef`, `agentPartyRef`); agent Party = authority-subject Party; exact CP3 instance, sponsor, profile, actorship, envelope, authority snapshot and revocation references; direct/role grant targets agent Party |
| REPRESENTED_PARTY_EXPLICIT_DELEGATION | Same agent/CP3 closure; DelegationGrant links `delegatePartyRef` to agent Party and `delegatingPartyRef` to represented/authority-subject Party; its existing `sourceAuthorityGrantRefs` must resolve exact immutable grant bindings, and its delegation tuple binding must be present |

CP3 comparisons use existing field spellings: actorship `agentInstanceRef`; envelope and revocation `executingAgentInstanceRef`; envelope `agentActorshipBindingRef`, `revocationStateRef`, `authorizationDecisionResultRef`, `authorizationDecisionTraceRef`, and `requestedActionClass`; revocation `authorityEnvelopeRef`. No CP3 field is added. These equalities do not evaluate CP3 permission or freshness.

Authority-grant target comparisons read the existing `grantTarget.targetKind` and `grantTarget.targetRef` fields. Delegation comparisons retain `sourceAuthorityGrantRefs` and resolve every named source record through the complete typed basis catalog; no replacement grant field is introduced.

The Party basis role always resolves artifact family `PARTY`. Grant/delegation roles resolve their exact families, not a Party object or consumer report. Additional typed basis records may be retained under `ADDITIONAL_AUTHORITY_BASIS`; they remain fully byte-bound and visible in the selected snapshot but never replace a mandatory named role.

Grant/delegation/sharing formats use `SOURCE_RECORD_EXCLUDING_TOP_DIGEST`: require `sourceRecordDigest`, remove exactly that top-level member, compute JCS/SHA-256, and compare the resulting digest with both record and binding. No other member is excluded. Other records use `FULL_VALUE`, even where the selected immutable reference is a revision. The format must supply `revisionPointer` for every revision-bound record; the original record value must equal `revisionRef`. `schemaVersionPointer` selects the native complete intent version field and must equal the rule-selected schema version. Neither pointer is inferred from a field name. A logical identity (artifact family plus ref) has only one exact byte representation in the supplied decision, even across different revision labels. Full original-byte hashes are independently checked in either case. This is bounded evidence integrity, not proof that an external historical store has never reused an ID.

Foreign schemas are exact original bytes, identified by `$id`, raw hash and selected format. Conflicting owned IDs, unresolved references, nested `$id`, and dynamic/recursive references are rejected by this v0.1 profile. It does not fall back to the network. A later profile may separately add a proven schema feature without weakening current pins.

Next: select an actual producer's complete source profile through the authorization owner's trusted integration boundary; do not relabel the fictional conformance profile as live evidence.

The closed result and trace projections also require `resolvedPrincipalKind`, `agentActionPosture` (null for a natural-person decision), `humanFinalizationRequirement`, `primaryReasonCode`, `authorizationViewExtractorRef` and `authorizationViewExtractorDigest`. The rule projection supplies its exact accepted agent posture, finalization requirement and extractor ref/digest. The extractor is an additional complete source under `AUTHORIZATION_VIEW_EXTRACTOR`, always digest-bound. The derived view also identifies that extractor. These are normalized projections of owner records, not new fields in foreign CP3 contracts. `AUTHORIZED_BY_SELECTED_PATH` is the required successful primary reason under PR11 §15.6.

The source profile explicitly limits `selectedPathTypes` to direct, role-targeted and delegated grant paths. A selected sharing path produces `SELECTED_SHARING_PATH_OUTSIDE_PROFILE`; it is never misreported as a direct-grant mismatch. Retained sharing paths remain schema-, tuple- and source-bound. Full SharingGrant selected-path semantics require a separately reviewed profile extension, not an invented direct grant or authority-subject rule.

Next: independently review this repaired profile and its exact byte-bound examples before integrating it.
