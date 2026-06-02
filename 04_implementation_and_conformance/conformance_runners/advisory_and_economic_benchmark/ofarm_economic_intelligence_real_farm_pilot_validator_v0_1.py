import json
import sys
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
DEFAULT_DATASET = HERE / 'ofarm_economic_intelligence_real_farm_pilot_dataset_illustrative_v0_1.json'
OUT_JSON = HERE / 'OFARM_economic_intelligence_real_farm_pilot_illustrative_readiness_report_v0_1.json'
OUT_MD = HERE / 'OFARM_economic_intelligence_real_farm_pilot_illustrative_readiness_report_v0_1.md'


def load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def missing(v: Any) -> bool:
    return v is None or v == '' or v == [] or v == {}


def check_lane_a(data: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    lane = data.get('laneA', {})
    if len(lane.get('candidates', [])) < 2:
        issues.append('Need at least two crop/system alternatives.')
    for idx, c in enumerate(lane.get('candidates', []), start=1):
        for key in ['areaHa', 'labourHoursPerHa', 'machineHoursPerHa', 'fuelLitresPerHa', 'inputQuantityIndex']:
            if missing(c.get(key)):
                issues.append(f'Candidate {idx} missing {key}.')
        for path in [
            ('expectedYield', 'value'), ('expectedYield', 'low'), ('expectedYield', 'high'),
            ('expectedSellingPrice', 'value'), ('expectedSellingPrice', 'low'), ('expectedSellingPrice', 'high')
        ]:
            if missing(c.get(path[0], {}).get(path[1])):
                issues.append(f'Candidate {idx} missing {path[0]}.{path[1]}.')
    status = 'READY' if not issues else 'BLOCKED'
    return {'status': status, 'issues': issues, 'claimBoundary': 'screening only; not profitability'}


def check_lane_b(data: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    lane = data.get('laneB', {})
    for key in ['areaHa', 'cropSystem']:
        if missing(lane.get(key)):
            issues.append(f'Missing {key}.')
    for path in [
        ('expectedYield', 'value'), ('expectedSellingPrice', 'value'),
        ('bottleneckWindow', 'availableDays'), ('bottleneckWindow', 'ownMachineHoursAvailable'),
        ('bottleneckWindow', 'ownLabourHoursAvailable'), ('bottleneckWindow', 'contractorGuaranteedCapacityHaPerDay'),
        ('ownOption', 'machineHoursPerHa'), ('ownOption', 'labourHoursPerHa'), ('ownOption', 'fuelLitresPerHa'), ('ownOption', 'benchmarkWearPartsPerHaEUR'),
        ('contractorOption', 'contractorRatePerHaEUR'), ('contractorOption', 'mobilizationEUR'),
        ('rateInputs', 'fuelPriceEURPerL'), ('rateInputs', 'labourRateEURPerH'),
        ('timingPenaltyAssumption', 'untimelyAreaRevenuePenaltyRate'),
    ]:
        if missing(lane.get(path[0], {}).get(path[1])):
            issues.append(f'Missing {path[0]}.{path[1]}.')
    status = 'READY' if not issues else 'BLOCKED'
    return {'status': status, 'issues': issues, 'claimBoundary': 'relevant-cost + bottleneck screen only; not field profitability'}


def check_lane_c(data: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    lane = data.get('laneC', {})
    for path in [
        ('candidateAsset', 'indicativeCapexEUR'), ('candidateAsset', 'nameplateTonnesPerHour'), ('candidateAsset', 'availableSeasonHours'),
        ('volumeBasis', 'baseHarvestTonnes'), ('volumeBasis', 'downsideHarvestTonnes'), ('volumeBasis', 'qualityFitShareBasePct'), ('volumeBasis', 'qualityFitShareDownsidePct'),
        ('marketBasis', 'committedOutletSharePct'), ('marketBasis', 'minimumCommittedOutletSharePct'),
        ('lossBasis', 'currentProcessLossSharePct'), ('lossBasis', 'candidateProcessLossSharePct'),
        ('workingCapitalBasis', 'assumedDays'), ('workingCapitalBasis', 'maximumAcceptableDays'),
        ('thresholds', 'minimumBaseUtilizationPct'), ('thresholds', 'minimumDownsideUtilizationPct'),
        ('thresholds', 'minimumQualityFitBasePct'), ('thresholds', 'minimumQualityFitDownsidePct'),
    ]:
        if missing(lane.get(path[0], {}).get(path[1])):
            issues.append(f'Missing {path[0]}.{path[1]}.')
    if len(lane.get('importedFactExtractRefs', [])) == 0:
        issues.append('Need importedFactExtractRefs for Lane C.')
    if len(lane.get('operationalRefs', [])) == 0:
        issues.append('Need operationalRefs for Lane C.')
    status = 'READY' if not issues else 'BLOCKED'
    return {'status': status, 'issues': issues, 'claimBoundary': 'pre-gate screening only; not full appraisal'}


def assess(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'datasetId': data.get('datasetId'),
        'datasetKind': data.get('datasetKind'),
        'actualFarmData': data.get('provenance', {}).get('actualFarmData'),
        'laneA': check_lane_a(data),
        'laneB': check_lane_b(data),
        'laneC': check_lane_c(data),
    }


def render_md(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append('# OFARM economic intelligence real-farm pilot readiness report v0.1')
    lines.append('')
    lines.append(f"Dataset: **{report.get('datasetId')}**")
    lines.append('')
    lines.append(f"Dataset kind: **{report.get('datasetKind')}**")
    lines.append('')
    lines.append(f"Actual farm data: **{report.get('actualFarmData')}**")
    lines.append('')
    for lane_key, title in [('laneA', 'Lane A'), ('laneB', 'Lane B'), ('laneC', 'Lane C')]:
        lane = report[lane_key]
        lines.append(f'## {title} — {lane["status"]}')
        lines.append('')
        lines.append(f'- Claim boundary: {lane["claimBoundary"]}')
        if lane['issues']:
            lines.append('- Issues:')
            for issue in lane['issues']:
                lines.append(f'  - {issue}')
        else:
            lines.append('- No blocking issues found for this lane.')
        lines.append('')
    if report.get('actualFarmData') is not True:
        lines.append('**Warning:** this is not a real farm dataset. Use only as a mechanical test of the pilot kit.')
        lines.append('')
    return '\n'.join(lines) + '\n'


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATASET
    report = assess(load(path))
    out_json = path.with_name(path.stem + '_readiness_report.json') if path != DEFAULT_DATASET else OUT_JSON
    out_md = path.with_name(path.stem + '_readiness_report.md') if path != DEFAULT_DATASET else OUT_MD
    out_json.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    out_md.write_text(render_md(report), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
