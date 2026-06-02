# Forbidden OFARM SDK patterns. Generated public SDKs must not expose these calls.

# db.current_state.update({"fieldId": "field:7", "status": "treated"})
# ofarm.internal.materialization_store.write(...)
# app.mark_as_accepted_execution("contractor-claim-1")
# ai_output.promote_to_compliance_fact(...)
# client.generic_crud.save("canonicalAssertion", payload)
# client.packs.merge_core_meaning(...)
