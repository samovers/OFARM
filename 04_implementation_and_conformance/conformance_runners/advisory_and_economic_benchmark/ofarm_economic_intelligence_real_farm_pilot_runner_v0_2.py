import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
DEFAULT_DATASET = HERE / 'ofarm_economic_intelligence_real_farm_pilot_dataset_illustrative_v0_2.json'


def load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def lane_a(lane: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for c in lane['candidates']:
        revenue_per_ha = c['expectedYield']['value'] * c['expectedSellingPrice']['value']
        revenue_total = revenue_per_ha * c['areaHa']
        downside = c['expectedYield']['low'] * c['expectedSellingPrice']['low'] * c['areaHa']
        upside = c['expectedYield']['high'] * c['expectedSellingPrice']['high'] * c['areaHa']
        rows.append({
            'alternativeId': c['alternativeId'],
            'label': c['label'],
            'cropSystem': c['cropSystem'],
            'expectedRevenuePerHaEUR': round(revenue_per_ha, 2),
            'expectedRevenueTotalEUR': round(revenue_total, 2),
            'downsideRevenueTotalEUR': round(downside, 2),
            'upsideRevenueTotalEUR': round(upside, 2),
            'estimatedRevenuePerLaborHourEUR': round(revenue_per_ha / c['labourHoursPerHa'], 2),
            'estimatedRevenuePerMachineHourEUR': round(revenue_per_ha / c['machineHoursPerHa'], 2),
            'estimatedRevenuePerFuelLitreEUR': round(revenue_per_ha / c['fuelLitresPerHa'], 2),
        })
    metric = {
        'MACHINE_HOUR': 'estimatedRevenuePerMachineHourEUR',
        'LABOUR_HOUR': 'estimatedRevenuePerLaborHourEUR',
        'FUEL_LITRE': 'estimatedRevenuePerFuelLitreEUR',
    }[lane['controllingBottleneck']['resourceType']]
    ranked = sorted(rows, key=lambda r: r[metric], reverse=True)
    return {
        'status': 'EXECUTED',
        'rankingMetric': metric,
        'screeningOnly': True,
        'rankedAlternatives': ranked,
        'claimBoundary': 'operational-only screening; not profitability',
    }


def lane_b(lane: Dict[str, Any]) -> Dict[str, Any]:
    area = lane['areaHa']
    gross_rev_per_ha = lane['expectedYield']['value'] * lane['expectedSellingPrice']['value']
    own = lane['ownOption']
    contractor = lane['contractorOption']
    rates = lane['rateInputs']
    window = lane['bottleneckWindow']
    penalty = lane['timingPenaltyAssumption']['untimelyAreaRevenuePenaltyRate']
    own_timely_area = min(area, window['ownMachineHoursAvailable'] / own['machineHoursPerHa'], window['ownLabourHoursAvailable'] / own['labourHoursPerHa'])
    contractor_timely_area = min(area, window['contractorGuaranteedCapacityHaPerDay'] * window['availableDays'])
    own_untimely = max(0.0, area - own_timely_area)
    contractor_untimely = max(0.0, area - contractor_timely_area)
    own_direct_per_ha = own['fuelLitresPerHa'] * rates['fuelPriceEURPerL'] + own['labourHoursPerHa'] * rates['labourRateEURPerH'] + own['benchmarkWearPartsPerHaEUR']
    contractor_direct_per_ha = contractor['contractorRatePerHaEUR'] + contractor['mobilizationEUR'] / area
    own_total = own_direct_per_ha * area
    contractor_total = contractor_direct_per_ha * area
    own_exposure = own_untimely * gross_rev_per_ha * penalty
    contractor_exposure = contractor_untimely * gross_rev_per_ha * penalty
    options = [
        {
            'optionId': 'OWN',
            'label': own['label'],
            'directCostTotalEUR': round(own_total, 2),
            'timelyCoveragePct': round(own_timely_area / area * 100, 2),
            'untimelyAreaHa': round(own_untimely, 2),
            'estimatedUntimelyRevenueExposureEUR': round(own_exposure, 2),
            'screenedCombinedOutlayAndExposureEUR': round(own_total + own_exposure, 2),
        },
        {
            'optionId': 'CONTRACTOR',
            'label': contractor['label'],
            'directCostTotalEUR': round(contractor_total, 2),
            'timelyCoveragePct': round(contractor_timely_area / area * 100, 2),
            'untimelyAreaHa': round(contractor_untimely, 2),
            'estimatedUntimelyRevenueExposureEUR': round(contractor_exposure, 2),
            'screenedCombinedOutlayAndExposureEUR': round(contractor_total + contractor_exposure, 2),
        },
    ]
    options = sorted(options, key=lambda o: o['screenedCombinedOutlayAndExposureEUR'])
    return {
        'status': 'EXECUTED',
        'screeningOnly': True,
        'options': options,
        'recommendedOption': options[0]['optionId'],
        'claimBoundary': 'relevant-cost and bottleneck screen only; not field profitability',
    }


def lane_c(lane: Dict[str, Any]) -> Dict[str, Any]:
    asset = lane['candidateAsset']
    annual_capacity = asset['nameplateTonnesPerHour'] * asset['availableSeasonHours']
    base_eligible = lane['volumeBasis']['baseHarvestTonnes'] * lane['volumeBasis']['qualityFitShareBasePct'] / 100.0
    downside_eligible = lane['volumeBasis']['downsideHarvestTonnes'] * lane['volumeBasis']['qualityFitShareDownsidePct'] / 100.0
    base_util = base_eligible / annual_capacity * 100.0
    downside_util = downside_eligible / annual_capacity * 100.0
    all_pass = (
        base_util >= lane['thresholds']['minimumBaseUtilizationPct'] and
        downside_util >= lane['thresholds']['minimumDownsideUtilizationPct'] and
        lane['volumeBasis']['qualityFitShareBasePct'] >= lane['thresholds']['minimumQualityFitBasePct'] and
        lane['volumeBasis']['qualityFitShareDownsidePct'] >= lane['thresholds']['minimumQualityFitDownsidePct'] and
        lane['marketBasis']['committedOutletSharePct'] >= lane['marketBasis']['minimumCommittedOutletSharePct'] and
        lane['workingCapitalBasis']['assumedDays'] <= lane['workingCapitalBasis']['maximumAcceptableDays']
    )
    outcome = 'PROCEED_TO_FULL_APPRAISAL' if all_pass else 'HOLD_FOR_MORE_EVIDENCE'
    return {
        'status': 'EXECUTED',
        'screeningOnly': True,
        'fullExternalAppraisalRequired': True,
        'annualCapacityTonnes': round(annual_capacity, 2),
        'baseEligibleTonnes': round(base_eligible, 2),
        'downsideEligibleTonnes': round(downside_eligible, 2),
        'baseUtilizationPct': round(base_util, 2),
        'downsideUtilizationPct': round(downside_util, 2),
        'outcome': outcome,
        'claimBoundary': 'pre-gate screening only; not full appraisal or financing approval',
    }


def has_nulls(obj: Any) -> bool:
    if obj is None:
        return True
    if isinstance(obj, dict):
        return any(has_nulls(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_nulls(v) for v in obj)
    return False


def run(data: Dict[str, Any]) -> Dict[str, Any]:
    results: Dict[str, Any] = {
        'datasetId': data['datasetId'],
        'datasetKind': data['datasetKind'],
        'actualFarmData': data['provenance']['actualFarmData'],
        'lanes': {},
    }
    for key, fn in [('laneA', lane_a), ('laneB', lane_b), ('laneC', lane_c)]:
        lane = data.get(key)
        if not lane or has_nulls(lane):
            results['lanes'][key] = {'status': 'NOT_EXECUTED', 'reason': 'incomplete data section'}
        else:
            results['lanes'][key] = fn(lane)
    return results


def render_md(results: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append('# OFARM economic intelligence real-farm pilot summary v0.2')
    lines.append('')
    lines.append(f"Dataset: **{results['datasetId']}**")
    lines.append('')
    lines.append(f"Dataset kind: **{results['datasetKind']}**")
    lines.append('')
    if results['actualFarmData'] is not True:
        lines.append('**Warning:** illustrative non-real dataset. Mechanical proof only.')
        lines.append('')
    for key, title in [('laneA', 'Lane A'), ('laneB', 'Lane B'), ('laneC', 'Lane C')]:
        lane = results['lanes'][key]
        lines.append(f'## {title} — {lane["status"]}')
        lines.append('')
        if lane['status'] != 'EXECUTED':
            lines.append(f"- Reason: {lane['reason']}")
            lines.append('')
            continue
        lines.append(f"- Claim boundary: {lane['claimBoundary']}")
        if key == 'laneA':
            top = lane['rankedAlternatives'][0]
            lines.append(f"- Top operational screen: **{top['label']}** using metric **{lane['rankingMetric']}**.")
        elif key == 'laneB':
            lines.append(f"- Recommended option: **{lane['recommendedOption']}**.")
        elif key == 'laneC':
            lines.append(f"- Pre-gate outcome: **{lane['outcome']}**.")
        lines.append('')
    lines.append('No lane output here is authoritative financial truth.')
    return '\n'.join(lines) + '\n'


def output_paths(dataset: Path, out_dir: Optional[Path]) -> Tuple[Path, Path]:
    base = dataset.stem
    target_dir = out_dir or dataset.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / f'{base}_results.json', target_dir / f'{base}_summary.md'


def main() -> None:
    parser = argparse.ArgumentParser(description='Run bounded OFARM economics pilot lanes.')
    parser.add_argument('dataset', nargs='?', default=str(DEFAULT_DATASET), help='Path to pilot dataset JSON.')
    parser.add_argument('--output-dir', default=None, help='Optional output directory for results.')
    args = parser.parse_args()

    dataset = Path(args.dataset).resolve()
    results = run(load(dataset))
    out_json, out_md = output_paths(dataset, Path(args.output_dir).resolve() if args.output_dir else None)
    out_json.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    out_md.write_text(render_md(results), encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
