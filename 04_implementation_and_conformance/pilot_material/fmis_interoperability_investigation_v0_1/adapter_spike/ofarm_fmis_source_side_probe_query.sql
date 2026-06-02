-- Source-side redacted probe for the selected adapter-spike candidate.
-- Read-only BigQuery Standard SQL.
-- Billing project: login-eko-samoa-sbx
-- Data project: login-eko-data-layer
--
-- The query reselects the same strongest completed APPLICATION candidate used
-- by ofarm_fmis_adapter_spike_candidate_query.sql, then checks source-facing
-- planned operation, work order, audit, material audit, and task-result tables.

WITH planned AS (
  SELECT
    field_operation_planned_id,
    field_id,
    materials
  FROM `login-eko-data-layer.prod__t_kis__operations.fact_field_operation_planned`
  WHERE primary_category = 'APPLICATION'
    AND ARRAY_LENGTH(materials) > 0
),
actual AS (
  SELECT
    field_operation_planned_id,
    materials
  FROM `login-eko-data-layer.prod__t_kis__operations.fact_field_operation_actual`
  WHERE primary_category = 'APPLICATION'
    AND status = 'COMPLETED'
    AND ARRAY_LENGTH(materials) > 0
),
crop_zone_summary AS (
  SELECT
    operation_planned_id,
    COUNT(*) AS crop_zone_actual_row_count,
    COUNTIF(operation_zone_geometry IS NOT NULL) AS rows_with_operation_zone_geometry,
    COUNTIF(ARRAY_LENGTH(operation_materials) > 0) AS rows_with_operation_materials
  FROM `login-eko-data-layer.prod__t_kis__crops_fact_zone.fact_crop_zone_actual_operation`
  GROUP BY operation_planned_id
),
selected AS (
  SELECT p.field_operation_planned_id
  FROM planned p
  JOIN actual a USING (field_operation_planned_id)
  LEFT JOIN crop_zone_summary cz
    ON cz.operation_planned_id = p.field_operation_planned_id
  ORDER BY
    cz.rows_with_operation_zone_geometry DESC,
    cz.rows_with_operation_materials DESC,
    ARRAY_LENGTH(a.materials) DESC
  LIMIT 1
),
source_plan AS (
  SELECT sp.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_field_operation_planned` sp
  JOIN selected s
    ON s.field_operation_planned_id = sp.id
),
wo_link AS (
  SELECT l.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_field_operation_planned_work_order` l
  JOIN selected s USING (field_operation_planned_id)
),
wo AS (
  SELECT w.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_work_order` w
  JOIN wo_link l
    ON l.work_order_id = w.id
),
audit AS (
  SELECT a.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_field_operation_planned_auditing` a
  JOIN selected s USING (field_operation_planned_id)
),
audit_material AS (
  SELECT am.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_field_operation_planned_auditing_material` am
  JOIN audit a
    ON am.field_operation_planned_auditing_id = a.id
),
task AS (
  SELECT t.*
  FROM `login-eko-data-layer.prod__t_kis__source_farming.frm2_task_result_hub` t
  JOIN wo
    ON t.work_order_id = wo.id
)
SELECT
  CURRENT_TIMESTAMP() AS extracted_at,
  (SELECT TO_HEX(SHA256(CAST(field_operation_planned_id AS STRING))) FROM selected) AS operation_hash,
  STRUCT(
    (SELECT COUNT(*) FROM source_plan) AS row_count,
    (SELECT MIN(created_timestamp) FROM source_plan) AS created_min,
    (SELECT MAX(last_modified_timestamp) FROM source_plan) AS modified_max,
    (SELECT ARRAY_AGG(DISTINCT calculated_status IGNORE NULLS) FROM source_plan) AS statuses,
    (SELECT ARRAY_AGG(DISTINCT origin IGNORE NULLS) FROM source_plan) AS origins,
    (SELECT ARRAY_AGG(DISTINCT TO_HEX(SHA256(COALESCE(created_by, ''))) IGNORE NULLS) FROM source_plan) AS created_by_hashes,
    (SELECT ARRAY_AGG(DISTINCT TO_HEX(SHA256(COALESCE(last_modified_by, ''))) IGNORE NULLS) FROM source_plan) AS modified_by_hashes,
    (SELECT COUNTIF(deleted_id IS NOT NULL) FROM source_plan) AS deleted_marker_count
  ) AS source_plan,
  STRUCT(
    (SELECT COUNT(*) FROM wo_link) AS row_count,
    (SELECT ARRAY_AGG(DISTINCT TO_HEX(SHA256(CAST(work_order_id AS STRING))) IGNORE NULLS) FROM wo_link) AS work_order_hashes,
    (SELECT MIN(created_timestamp) FROM wo_link) AS created_min,
    (SELECT MAX(last_modified_timestamp) FROM wo_link) AS modified_max
  ) AS work_order_links,
  STRUCT(
    (SELECT COUNT(*) FROM wo) AS row_count,
    (SELECT ARRAY_AGG(DISTINCT status IGNORE NULLS) FROM wo) AS statuses,
    (SELECT COUNTIF(deleted_id IS NOT NULL) FROM wo) AS deleted_marker_count,
    (SELECT MIN(created_timestamp) FROM wo) AS created_min,
    (SELECT MAX(last_modified_timestamp) FROM wo) AS modified_max
  ) AS work_orders,
  STRUCT(
    (SELECT COUNT(*) FROM audit) AS row_count,
    (
      SELECT ARRAY_AGG(STRUCT(
        action,
        change_type,
        status,
        old_status,
        creation_time,
        TO_HEX(SHA256(CAST(user_id AS STRING))) AS user_hash
      ) ORDER BY creation_time)
      FROM audit
    ) AS entries
  ) AS planned_audit,
  STRUCT(
    (SELECT COUNT(*) FROM audit_material) AS row_count,
    (
      SELECT ARRAY_AGG(STRUCT(
        TO_HEX(SHA256(CAST(field_operation_planned_material_id AS STRING))) AS planned_material_hash,
        is_new,
        application_rate,
        unit
      ) ORDER BY field_operation_planned_material_id)
      FROM audit_material
    ) AS entries
  ) AS planned_audit_material,
  STRUCT(
    (SELECT COUNT(*) FROM task) AS row_count,
    (
      SELECT ARRAY_AGG(STRUCT(
        TO_HEX(SHA256(CAST(task_result_hub_id AS STRING))) AS task_hash,
        TO_HEX(SHA256(CAST(user_id AS STRING))) AS user_hash,
        TO_HEX(SHA256(CAST(vehicle_id AS STRING))) AS vehicle_hash,
        status,
        start_time,
        end_time,
        field_coverage_start_value,
        field_coverage_start_unit,
        field_coverage_end_value,
        field_coverage_end_unit,
        active_hours,
        machine_hours,
        TO_HEX(SHA256(COALESCE(created_by, ''))) AS created_by_hash,
        TO_HEX(SHA256(COALESCE(last_modified_by, ''))) AS last_modified_by_hash
      ) ORDER BY start_time)
      FROM task
    ) AS entries
  ) AS task_results,
  STRUCT(
    'redacted_hashes_only' AS identity_policy,
    'source-side audit/work-order/task probe; no names or coordinates exported' AS redaction_policy,
    'Auditing rows support reconstruction but are not by themselves authority, evidence sufficiency, or OFARM acceptance decisions' AS interpretation_policy
  ) AS caveats;
