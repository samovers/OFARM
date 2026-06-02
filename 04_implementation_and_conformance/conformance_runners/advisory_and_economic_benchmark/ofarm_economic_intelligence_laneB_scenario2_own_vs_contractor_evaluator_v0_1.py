import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / 'ofarm_economic_intelligence_laneB_scenario2_own_vs_contractor_sample_dataset_v0_1.json'
RESULTS_JSON = HERE / 'OFARM_economic_intelligence_laneB_scenario2_example_results_v0_1.json'
SUMMARY_MD = HERE / 'OFARM_economic_intelligence_laneB_scenario2_example_summary_v0_1.md'

SCENARIO_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_b_capacity_screening_v0_1' / 'OFARM_AdvisoryScenarioSpec_example_lane_b_capacity_screening_v0_1.json'
EXTRACT_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_b_capacity_screening_v0_1' / 'OFARM_ImportedFactExtract_example_lane_b_capacity_screening_v0_1.json'
RESULTSET_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_b_capacity_screening_v0_1' / 'OFARM_AdvisoryScenarioResultSet_example_lane_b_capacity_screening_v0_1.json'
BRIDGE_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_b_capacity_screening_v0_1' / 'OFARM_BridgeCandidate_example_lane_b_capacity_screening_v0_1.json'
NEG_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'negative' / 'OFARM_AdvisoryScenarioResultSet_example_invalid_lane_b_field_profitability_claim_v0_1.json'


def load():
    return json.loads(DATASET.read_text(encoding='utf-8'))


def evaluate(data):
    area = data['areaHa']
    gross_rev_per_ha = data['expectedYield']['value'] * data['expectedSellingPrice']['value']

    own = data['ownOption']
    contractor = data['contractorOption']
    rates = data['rateInputs']
    window = data['bottleneckWindow']
    penalty = data['timingPenaltyAssumption']['untimelyAreaRevenuePenaltyRate']

    own_timely_area = min(
        area,
        window['ownMachineHoursAvailable'] / own['machineHoursPerHa'],
        window['ownLabourHoursAvailable'] / own['labourHoursPerHa'],
    )
    contractor_timely_area = min(area, window['contractorGuaranteedCapacityHaPerDay'] * window['availableDays'])

    own_untimely = max(0.0, area - own_timely_area)
    contractor_untimely = max(0.0, area - contractor_timely_area)

    own_direct_per_ha = own['fuelLitresPerHa'] * rates['fuelPriceEURPerL'] + own['labourHoursPerHa'] * rates['labourRateEURPerH'] + own['benchmarkWearPartsPerHaEUR']
    contractor_direct_per_ha = contractor['contractorRatePerHaEUR'] + contractor['mobilizationEUR'] / area

    own_direct_total = own_direct_per_ha * area
    contractor_direct_total = contractor_direct_per_ha * area

    own_exposure = own_untimely * gross_rev_per_ha * penalty
    contractor_exposure = contractor_untimely * gross_rev_per_ha * penalty

    options = [
        {
            'optionId': 'OWN_COMBINE',
            'label': own['label'],
            'directCostTotalEUR': round(own_direct_total, 2),
            'directCostPerHaEUR': round(own_direct_per_ha, 2),
            'timelyCoveragePct': round(own_timely_area / area * 100, 2),
            'untimelyAreaHa': round(own_untimely, 2),
            'estimatedUntimelyRevenueExposureEUR': round(own_exposure, 2),
            'screenedCombinedOutlayAndExposureEUR': round(own_direct_total + own_exposure, 2),
        },
        {
            'optionId': 'CONTRACTOR',
            'label': contractor['label'],
            'directCostTotalEUR': round(contractor_direct_total, 2),
            'directCostPerHaEUR': round(contractor_direct_per_ha, 2),
            'timelyCoveragePct': round(contractor_timely_area / area * 100, 2),
            'untimelyAreaHa': round(contractor_untimely, 2),
            'estimatedUntimelyRevenueExposureEUR': round(contractor_exposure, 2),
            'screenedCombinedOutlayAndExposureEUR': round(contractor_direct_total + contractor_exposure, 2),
        },
    ]
    options = sorted(options, key=lambda o: o['screenedCombinedOutlayAndExposureEUR'])
    for idx, o in enumerate(options, start=1):
        o['rank'] = idx

    headline = {
        'recommendedOption': options[0]['optionId'],
        'extraDirectOutlayForRecommendedOptionEUR': round(contractor_direct_total - own_direct_total, 2),
        'timingProtectionValueEstimateEUR': round(own_exposure - contractor_exposure, 2),
    }

    return {
        'lane': 'B',
        'scenario': 'Scenario 2 own-versus-contractor capacity screen',
        'basisPosture': {
            'targetTwin': 'ADVISORY',
            'importedFinancePosture': 'bounded extract input only',
            'claimBoundary': 'decision support only, not ledger truth, not profitability'
        },
        'decisionContext': {
            'fieldRef': data['anchorScope']['scopeRef'],
            'cropSystem': data['cropSystem'],
            'operationRef': data['operationScope']['scopeRef'],
            'areaHa': area,
            'windowDays': window['availableDays']
        },
        'options': options,
        'headline': headline,
        'requiredDisplayNote': 'Decision support only. Partial finance plus benchmark assumptions. Imported contractor rates are not ledger truth. Not a profitability statement.'
    }


def write_summary(result):
    lines = []
    lines.append('# OFARM economic intelligence Lane B — Scenario 2 example summary v0.1')
    lines.append('')
    lines.append(result['requiredDisplayNote'])
    lines.append('')
    lines.append('## Screened options')
    lines.append('')
    lines.append('| Rank | Option | Direct cost total € | Timely coverage % | Untimely area ha | Estimated untimely revenue exposure € | Combined outlay + exposure € |')
    lines.append('|---|---|---:|---:|---:|---:|---:|')
    for row in result['options']:
        lines.append(f"| {row['rank']} | {row['label']} | {row['directCostTotalEUR']:.2f} | {row['timelyCoveragePct']:.2f} | {row['untimelyAreaHa']:.2f} | {row['estimatedUntimelyRevenueExposureEUR']:.2f} | {row['screenedCombinedOutlayAndExposureEUR']:.2f} |")
    lines.append('')
    lines.append('## Interpretation')
    lines.append('')
    lines.append(f"- Recommended option: **{result['headline']['recommendedOption']}**.")
    lines.append(f"- Extra direct outlay for the recommended option = **{result['headline']['extraDirectOutlayForRecommendedOptionEUR']:.2f} EUR**.")
    lines.append(f"- Timing-protection value estimate = **{result['headline']['timingProtectionValueEstimateEUR']:.2f} EUR** under the declared delay assumption.")
    lines.append('- This is a relevant-cost plus capacity screen, not a field-profitability statement and not accounting truth.')
    SUMMARY_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    result = evaluate(load())
    RESULTS_JSON.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    write_summary(result)
    # Load contract files as a smoke test
    for p in [SCENARIO_JSON, EXTRACT_JSON, RESULTSET_JSON, BRIDGE_JSON, NEG_JSON]:
        json.loads(p.read_text(encoding='utf-8'))
