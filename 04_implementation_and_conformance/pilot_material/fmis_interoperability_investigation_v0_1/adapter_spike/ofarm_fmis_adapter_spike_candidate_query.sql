-- Redacted OFARM FMIS adapter-spike candidate packet.
-- Read-only BigQuery Standard SQL.
-- Billing project: login-eko-samoa-sbx
-- Data project: login-eko-data-layer
--
-- This query selects the strongest completed APPLICATION candidate with:
-- planned materials, actual materials, people/equipment references,
-- crop-zone actual rows, operation-zone geometry, and materialized geometry metrics.
-- It hashes identifiers and does not export field names, person names, or coordinates.

WITH planned AS (
  SELECT
    field_operation_planned_id,
    field_id,
    effective_start,
    effective_end,
    operation_status,
    operation_name_eng,
    primary_category,
    materials AS planned_materials
  FROM `login-eko-data-layer.prod__t_kis__operations.fact_field_operation_planned`
  WHERE primary_category = 'APPLICATION'
    AND ARRAY_LENGTH(materials) > 0
),
actual AS (
  SELECT
    field_operation_planned_id,
    status,
    effective_start AS actual_start,
    effective_end AS actual_end,
    materials AS actual_materials,
    vehicle_ids,
    implement_ids,
    person_ids,
    coverage_value,
    coverage_unit,
    total_fuel_consumption_value,
    total_fuel_consumption_unit,
    active_time_hours,
    last_modified_timestamp
  FROM `login-eko-data-layer.prod__t_kis__operations.fact_field_operation_actual`
  WHERE primary_category = 'APPLICATION'
    AND status = 'COMPLETED'
    AND ARRAY_LENGTH(materials) > 0
),
crop_zone_summary AS (
  SELECT
    operation_planned_id,
    COUNT(*) AS crop_zone_actual_rows,
    COUNTIF(operation_zone_geometry IS NOT NULL) AS rows_with_operation_zone_geometry,
    COUNTIF(crop_zone_geometry IS NOT NULL) AS rows_with_crop_zone_geometry,
    COUNTIF(ARRAY_LENGTH(operation_materials) > 0) AS rows_with_operation_materials,
    SUM(CAST(operation_zone_area_ha AS FLOAT64)) AS total_operation_zone_area_ha
  FROM `login-eko-data-layer.prod__t_kis__crops_fact_zone.fact_crop_zone_actual_operation`
  GROUP BY operation_planned_id
),
ranked AS (
  SELECT
    p.field_operation_planned_id,
    ROW_NUMBER() OVER (
      ORDER BY
        crop_zone_summary.rows_with_operation_zone_geometry DESC,
        crop_zone_summary.rows_with_operation_materials DESC,
        ARRAY_LENGTH(a.actual_materials) DESC,
        a.actual_end DESC
    ) AS rn
  FROM planned p
  JOIN actual a USING (field_operation_planned_id)
  LEFT JOIN crop_zone_summary
    ON crop_zone_summary.operation_planned_id = p.field_operation_planned_id
),
selected AS (
  SELECT field_operation_planned_id
  FROM ranked
  WHERE rn = 1
),
planned_materials AS (
  SELECT
    p.field_operation_planned_id,
    ARRAY_AGG(STRUCT(
      TO_HEX(SHA256(CAST(pm.material_id AS STRING))) AS material_hash,
      TO_HEX(SHA256(COALESCE(pm.material_name, ''))) AS material_name_hash,
      pm.material_quantity,
      pm.material_unit,
      pm.application_type,
      pm.application_rate,
      pm.application_unit
    ) ORDER BY pm.material_id) AS materials
  FROM planned p
  JOIN selected USING (field_operation_planned_id)
  CROSS JOIN UNNEST(p.planned_materials) AS pm
  GROUP BY p.field_operation_planned_id
),
actual_materials AS (
  SELECT
    a.field_operation_planned_id,
    ARRAY_AGG(STRUCT(
      TO_HEX(SHA256(CAST(am.material_id AS STRING))) AS material_hash,
      TO_HEX(SHA256(COALESCE(am.material_name, ''))) AS material_name_hash,
      am.material_quantity,
      am.material_unit,
      am.application_type,
      am.application_rate,
      am.application_unit
    ) ORDER BY am.material_id) AS materials
  FROM actual a
  JOIN selected USING (field_operation_planned_id)
  CROSS JOIN UNNEST(a.actual_materials) AS am
  GROUP BY a.field_operation_planned_id
),
crop_zone_rows AS (
  SELECT
    c.operation_planned_id AS field_operation_planned_id,
    ARRAY_AGG(STRUCT(
      TO_HEX(SHA256(CAST(c.crop_zone_id AS STRING))) AS crop_zone_hash,
      TO_HEX(SHA256(CAST(c.field_id AS STRING))) AS field_hash,
      TO_HEX(SHA256(CAST(c.field_geometry_id AS STRING))) AS field_geometry_hash,
      TO_HEX(SHA256(CAST(c.crop_id AS STRING))) AS crop_hash,
      TO_HEX(SHA256(COALESCE(c.crop_name, ''))) AS crop_name_hash,
      c.crop_effective_start,
      c.crop_effective_end,
      c.operation_start,
      c.operation_end,
      c.operation_status,
      c.crop_zone_geometry IS NOT NULL AS has_crop_zone_geometry,
      c.operation_zone_geometry IS NOT NULL AS has_operation_zone_geometry,
      c.crop_zone_geometry_area_ha,
      c.operation_zone_area_ha,
      c.operation_zone_to_crop_zone_intersection_ratio,
      c.crop_zone_to_operation_zone_intersection_ratio,
      ARRAY_LENGTH(c.operation_materials) AS operation_material_count
    ) ORDER BY c.crop_zone_id, c.operation_zone_area_ha) AS crop_zone_records
  FROM `login-eko-data-layer.prod__t_kis__crops_fact_zone.fact_crop_zone_actual_operation` c
  JOIN selected s
    ON s.field_operation_planned_id = c.operation_planned_id
  GROUP BY c.operation_planned_id
)
SELECT
  CURRENT_TIMESTAMP() AS extracted_at,
  TO_HEX(SHA256(CAST(p.field_operation_planned_id AS STRING))) AS operation_hash,
  TO_HEX(SHA256(CAST(p.field_id AS STRING))) AS field_hash,
  STRUCT(
    p.primary_category,
    p.operation_status,
    p.effective_start AS planned_start,
    p.effective_end AS planned_end,
    p.operation_name_eng IS NOT NULL AS has_operation_name_eng,
    planned_materials.materials AS materials
  ) AS planned_operation,
  STRUCT(
    a.status AS actual_status,
    a.actual_start,
    a.actual_end,
    a.coverage_value,
    a.coverage_unit,
    a.total_fuel_consumption_value,
    a.total_fuel_consumption_unit,
    a.active_time_hours,
    ARRAY_LENGTH(a.vehicle_ids) AS vehicle_count,
    ARRAY_LENGTH(a.implement_ids) AS implement_count,
    ARRAY_LENGTH(a.person_ids) AS person_count,
    a.last_modified_timestamp,
    actual_materials.materials AS materials
  ) AS actual_operation,
  STRUCT(
    crop_zone_summary.crop_zone_actual_rows,
    crop_zone_summary.rows_with_operation_zone_geometry,
    crop_zone_summary.rows_with_crop_zone_geometry,
    crop_zone_summary.rows_with_operation_materials,
    ROUND(crop_zone_summary.total_operation_zone_area_ha, 4) AS total_operation_zone_area_ha,
    crop_zone_rows.crop_zone_records AS crop_zone_records
  ) AS crop_zone_actual_operation,
  STRUCT(
    'redacted_hashes_only' AS identity_policy,
    'no_coordinates_exported' AS geometry_policy,
    'BigQuery marts only; original API/export payload not included' AS source_payload_policy,
    'Do not treat as accepted OFARM consequence without authority, evidence sufficiency, correction/dispute and source-health gates' AS promotion_policy
  ) AS caveats
FROM selected
JOIN planned p USING (field_operation_planned_id)
JOIN actual a USING (field_operation_planned_id)
LEFT JOIN crop_zone_summary
  ON crop_zone_summary.operation_planned_id = p.field_operation_planned_id
LEFT JOIN planned_materials USING (field_operation_planned_id)
LEFT JOIN actual_materials USING (field_operation_planned_id)
LEFT JOIN crop_zone_rows USING (field_operation_planned_id);
