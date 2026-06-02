# Codex FMIS Unresolved Questions

1. Is the first implementation spike meant to use the `prod__t_kis__*` BigQuery marts as the primary FMIS source, or should they be treated only as derived analytical surfaces over a separate source API/database?

2. Which table or source object carries recommendation or prescription authority, as distinct from planned operation scheduling?

3. Where are corrections, cancellations, deleted rows, superseded geometry versions, disputes, and late contractor sync events stored?

4. Do `operation_zone_geometry` values come from machine as-applied logs, manually drawn operation zones, crop-zone intersections, or another derived process?

5. Which material categories and `application_type` values correspond to crop-protection products, and how are they bound to product authorizations or active substances?

6. Are scouting image URLs stable evidence references with upload metadata and deletion audit, or convenience links without custody guarantees?

7. Are planned operation future dates intentional scheduling records, and what source-health rule should distinguish future planned work from stale or impossible execution evidence?
