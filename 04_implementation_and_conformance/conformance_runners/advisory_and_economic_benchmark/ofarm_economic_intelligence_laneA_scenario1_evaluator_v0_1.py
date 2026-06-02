import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / 'ofarm_economic_intelligence_laneA_scenario1_sample_dataset_v0_1.json'
RESULTS_JSON = HERE / 'OFARM_economic_intelligence_laneA_scenario1_example_results_v0_1.json'
SUMMARY_MD = HERE / 'OFARM_economic_intelligence_laneA_scenario1_example_summary_v0_1.md'
SCENARIO_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_a_operational_screening_v0_1' / 'OFARM_AdvisoryScenarioSpec_example_lane_a_operational_screening_v0_1.json'
RESULTSET_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_a_operational_screening_v0_1' / 'OFARM_AdvisoryScenarioResultSet_example_lane_a_operational_screening_v0_1.json'
BRIDGE_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'positive' / 'lane_a_operational_screening_v0_1' / 'OFARM_BridgeCandidate_example_lane_a_operational_screening_v0_1.json'
NEG_JSON = HERE / 'ofarm_economic_intelligence_spike_v0_1' / 'experimental_machine_contracts' / 'examples' / 'negative' / 'OFARM_AdvisoryScenarioResultSet_example_invalid_operational_only_profitability_claim_v0_1.json'


def load():
    return json.loads(DATASET.read_text(encoding='utf-8'))


def compute_row(c):
    revenue_per_ha = c['expectedYield']['value'] * c['expectedSellingPrice']['value']
    revenue_total = revenue_per_ha * c['areaHa']
    downside = c['expectedYield']['low'] * c['expectedSellingPrice']['low'] * c['areaHa']
    upside = c['expectedYield']['high'] * c['expectedSellingPrice']['high'] * c['areaHa']
    per_labor = revenue_per_ha / c['labourHoursPerHa']
    per_machine = revenue_per_ha / c['machineHoursPerHa']
    per_fuel = revenue_per_ha / c['fuelLitresPerHa']
    return {
        'alternativeId': c['alternativeId'],
        'label': c['label'],
        'cropSystem': c['cropSystem'],
        'expectedRevenuePerHaEUR': round(revenue_per_ha, 2),
        'expectedRevenueTotalEUR': round(revenue_total, 2),
        'downsideRevenueTotalEUR': round(downside, 2),
        'upsideRevenueTotalEUR': round(upside, 2),
        'estimatedRevenuePerLaborHourEUR': round(per_labor, 2),
        'estimatedRevenuePerMachineHourEUR': round(per_machine, 2),
        'estimatedRevenuePerFuelLitreEUR': round(per_fuel, 2),
        'operationalBurden': {
            'labourHoursPerHa': c['labourHoursPerHa'],
            'machineHoursPerHa': c['machineHoursPerHa'],
            'fuelLitresPerHa': c['fuelLitresPerHa'],
            'inputQuantityIndex': c['inputQuantityIndex'],
        },
    }


def rank(rows, bottleneck):
    key = {
        'MACHINE_HOUR': 'estimatedRevenuePerMachineHourEUR',
        'LABOUR_HOUR': 'estimatedRevenuePerLaborHourEUR',
        'FUEL_LITRE': 'estimatedRevenuePerFuelLitreEUR',
    }[bottleneck]
    return sorted(rows, key=lambda r: r[key], reverse=True), key


def build_summary(data, rows, ranking_metric):
    top = rows[0]
    potato = next(r for r in rows if r['cropSystem'] == 'PROCESSING_POTATO')
    summary = []
    summary.append('# OFARM economic intelligence Lane A — Scenario 1 example summary v0.1')
    summary.append('')
    summary.append(f"Bottleneck assumption: **{data['controllingBottleneck']['resourceType']}**")
    summary.append('')
    summary.append('Screening only. Operational/planning basis plus estimate assumptions. Not a profitability statement.')
    summary.append('')
    summary.append('## Ranked alternatives')
    summary.append('')
    summary.append('| Rank | Crop | Expected revenue €/ha | Revenue per machine-hour €/h | Revenue per labour-hour €/h | Downside total € | Upside total € |')
    summary.append('|---|---|---:|---:|---:|---:|---:|')
    for i, row in enumerate(rows, start=1):
        summary.append(f"| {i} | {row['label']} | {row['expectedRevenuePerHaEUR']:.2f} | {row['estimatedRevenuePerMachineHourEUR']:.2f} | {row['estimatedRevenuePerLaborHourEUR']:.2f} | {row['downsideRevenueTotalEUR']:.2f} | {row['upsideRevenueTotalEUR']:.2f} |")
    summary.append('')
    summary.append('## Interpretation')
    summary.append('')
    summary.append(f"- Highest machine-hour screen: **{top['label']}** at **{top[ranking_metric]:.2f} EUR per machine-hour**.")
    summary.append(f"- Highest gross revenue per hectare is **{potato['label']}** at **{potato['expectedRevenuePerHaEUR']:.2f} EUR/ha**, but it is also the heaviest on labour, machinery, and fuel.")
    summary.append('- This is a ranking of estimated gross-revenue-to-resource pressure, not a statement of profit, margin, or financial viability.')
    summary.append('- Stronger claims require cost rates, contractor rates, land/overhead treatment, and later accounting-backed reconciliation.')
    return '\n'.join(summary) + '\n'


def write_contract_examples(data, rows, ranking_metric):
    scenario_id = 'econ.laneA.operational-screening.2026-04-13'
    result_set_id = 'econ.laneA.operational-screening.results.2026-04-13'
    scenario = {
        'schemaVersion': 'ofarm.advisoryscenariospec.v0.1',
        'scenarioId': scenario_id,
        'targetTwin': 'ADVISORY',
        'anchorScopes': [data['anchorScope']],
        'evaluationTimePolicy': {'policyType': 'NOW'},
        'scenarioClass': 'CROP_SYSTEM_RANKING',
        'basisRefs': {
            'operationalRefs': [f"dataset:{data['datasetId']}"] + [ref for c in data['candidates'] for ref in c['basisRefs']],
            'currentStateMaterializationRefs': ['mat.advisory.field17.now'],
            'contextSnapshotRefs': ['ctx.base.field17.2026']
        },
        'assumptions': [
            {
                'assumptionId': f"assumption.price.{c['cropSystem'].lower()}",
                'label': f"Expected selling price for {c['label']}",
                'valueExpression': f"{c['expectedSellingPrice']['value']} EUR/t (range {c['expectedSellingPrice']['low']}–{c['expectedSellingPrice']['high']})",
                'evidenceClass': 'ESTIMATE',
                'sourceRef': f"plan.price.{c['cropSystem'].lower()}.2026"
            }
            for c in data['candidates']
        ] + [
            {
                'assumptionId': 'assumption.bottleneck.machinehour',
                'label': 'Controlling bottleneck',
                'valueExpression': data['controllingBottleneck']['resourceType'],
                'evidenceClass': 'PROXY',
                'sourceRef': 'op.window.machine_constrained'
            }
        ],
        'methodRef': 'method.driver_based_operational_screening.v0_1',
        'requestedOutputClass': 'VIEW',
        'notes': 'Operational-only screening. Screening only. Not a profitability statement.'
    }
    results = {
        'schemaVersion': 'ofarm.advisoryscenarioresultset.v0.1',
        'scenarioResultSetId': result_set_id,
        'sourceScenarioId': scenario_id,
        'generatedAt': '2026-04-13T16:00:00Z',
        'freshnessState': 'FRESH',
        'resultClass': 'RANKED_ALTERNATIVES',
        'results': [
            {
                'resultId': f'result.rank.{i}',
                'label': row['label'],
                'valueExpression': f"Estimated gross revenue per machine-hour = {row['estimatedRevenuePerMachineHourEUR']:.2f} EUR/h; gross revenue per ha = {row['expectedRevenuePerHaEUR']:.2f} EUR/ha",
                'rank': i,
                'uncertaintyExpression': f"Downside/upside total revenue range = {row['downsideRevenueTotalEUR']:.2f}–{row['upsideRevenueTotalEUR']:.2f} EUR for the sample field area",
                'evidenceClassesUsed': ['ESTIMATE', 'PROXY']
            }
            for i, row in enumerate(rows, start=1)
        ],
        'basisTraceRefs': ['trace.dataset.operational', 'trace.assumption.price_bands', 'trace.assumption.bottleneck'],
        'notes': 'Screening only. Operational/planning basis plus estimate assumptions. Not a profitability statement.'
    }
    bridge = {
        'schemaVersion': 'ofarm.bridgecandidate.v0.1',
        'bridgeCandidateId': 'econ.laneA.operational-screening.bridge.2026-04-13',
        'sourceScenarioResultSetId': result_set_id,
        'proposedNextStepClass': 'REQUEST_EVIDENCE',
        'targetScopes': [data['anchorScope']],
        'requiresHumanApproval': True,
        'rationale': 'Collect labour rate tables, contractor rates, and major cost extracts before any stronger economic comparison is used.',
        'prerequisiteRefs': ['missing.labor.rate.table', 'missing.contractor.rate.extract', 'missing.major_input_price.extract']
    }
    negative = {
        'schemaVersion': 'ofarm.advisoryscenarioresultset.v0.1',
        'scenarioResultSetId': 'econ.laneA.invalid-profit.results.2026-04-13',
        'sourceScenarioId': scenario_id,
        'generatedAt': '2026-04-13T16:00:00Z',
        'freshnessState': 'FRESH',
        'resultClass': 'GENERAL_SUMMARY',
        'results': [
            {
                'resultId': 'bad1',
                'label': 'Processing potato',
                'valueExpression': 'Highest estimated profit per hectare under the operational-only basis.',
                'rank': 1,
                'uncertaintyExpression': 'Assumes missing costs are acceptable.',
                'evidenceClassesUsed': ['ESTIMATE']
            }
        ],
        'basisTraceRefs': ['trace.dataset.operational'],
        'notes': 'Claims profitability from operational-only screening.'
    }
    SCENARIO_JSON.parent.mkdir(parents=True, exist_ok=True)
    SCENARIO_JSON.write_text(json.dumps(scenario, indent=2) + '\n', encoding='utf-8')
    RESULTSET_JSON.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    BRIDGE_JSON.write_text(json.dumps(bridge, indent=2) + '\n', encoding='utf-8')
    NEG_JSON.write_text(json.dumps(negative, indent=2) + '\n', encoding='utf-8')


def main():
    data = load()
    rows = [compute_row(c) for c in data['candidates']]
    ranked, metric = rank(rows, data['controllingBottleneck']['resourceType'])
    payload = {
        'datasetId': data['datasetId'],
        'rankingObjective': data['rankingObjective'],
        'controllingBottleneck': data['controllingBottleneck'],
        'rankingMetric': metric,
        'screeningOnly': True,
        'notAllowedClaims': ['profitability', 'gross_margin', 'operating_margin', 'npv', 'irr', 'dscr'],
        'rankedAlternatives': ranked,
    }
    RESULTS_JSON.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    SUMMARY_MD.write_text(build_summary(data, ranked, metric), encoding='utf-8')
    write_contract_examples(data, ranked, metric)

if __name__ == '__main__':
    main()
