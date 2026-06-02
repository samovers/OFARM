-- OFARM AGR-P10 Logineko entity-guided source-side recheck query skeleton
-- Status: active supporting implementation evidence
-- Purpose: guide KIS BigQuery source-side probing after the Logineko entity package addendum.
-- Boundary: this query skeleton does not create OFARM truth or accepted execution.

-- Selected adapter-spike operation hash:
-- 3bdbb71f4697ab0efa344f6d36e12c842904720c4972384a90b5828b05c59b88

-- Probe families identified by the entity package:
-- 1. planned operation -> scouting reports
-- 2. planned operation -> work order -> task result
-- 3. work order -> checkpoints
-- 4. work order -> material sessions
-- 5. audit timestamps and user attribution

-- Implementer note:
-- Replace `<operation_join_key>` and `<work_order_join_key>` with the redacted join fields available in the approved BigQuery environment.

WITH selected_operation AS (
  SELECT '<redacted-operation-hash>' AS operation_hash
),
scouting_reports AS (
  SELECT
    COUNT(*) AS linked_scouting_reports
  FROM `prod__t_kis__source_farming.evpss_scouting_report`
  WHERE TO_HEX(SHA256(CAST(<operation_join_key> AS STRING))) = (SELECT operation_hash FROM selected_operation)
),
scouting_report_items AS (
  SELECT
    COUNT(*) AS linked_scouting_report_items
  FROM `prod__t_kis__source_farming.evpss_scouting_report_item`
  WHERE TO_HEX(SHA256(CAST(<operation_join_key> AS STRING))) = (SELECT operation_hash FROM selected_operation)
),
work_order_checkpoints AS (
  SELECT
    COUNT(*) AS checkpoint_count,
    ARRAY_AGG(DISTINCT checkpoint_type IGNORE NULLS) AS checkpoint_types,
    MIN(checkpoint_at) AS checkpoint_start,
    MAX(checkpoint_at) AS checkpoint_end,
    COUNTIF(coverage_value IS NOT NULL) AS checkpoints_with_coverage,
    COUNTIF(fuel_value IS NOT NULL) AS checkpoints_with_fuel,
    COUNTIF(coverage_image_path IS NOT NULL) AS checkpoint_coverage_images,
    COUNTIF(fuel_image_path IS NOT NULL) AS checkpoint_fuel_images,
    COUNTIF(completed IS TRUE) AS completed_checkpoint_count,
    COUNTIF(incomplete_reason IS NOT NULL) AS incomplete_reason_count
  FROM `prod__t_kis__source_farming.evpos_work_order_checkpoint`
  WHERE TO_HEX(SHA256(CAST(<work_order_join_key> AS STRING))) = (SELECT operation_hash FROM selected_operation)
),
material_sessions AS (
  SELECT
    COUNT(*) AS material_session_count,
    COUNTIF(quantity IS NOT NULL) AS sessions_with_quantity,
    COUNTIF(lot_uuid IS NOT NULL OR location_uuid IS NOT NULL) AS sessions_with_lot_or_location,
    COUNTIF(image_path IS NOT NULL) AS sessions_with_images,
    COUNTIF(unknown_quantity_reason IS NOT NULL) AS sessions_with_unknown_quantity_reason,
    COUNTIF(lost_material IS TRUE) AS sessions_with_lost_material
  FROM `prod__t_kis__source_farming.evpos_material_session`
  WHERE TO_HEX(SHA256(CAST(<work_order_join_key> AS STRING))) = (SELECT operation_hash FROM selected_operation)
)
SELECT
  scouting_reports.*,
  scouting_report_items.*,
  work_order_checkpoints.*,
  material_sessions.*
FROM scouting_reports, scouting_report_items, work_order_checkpoints, material_sessions;
