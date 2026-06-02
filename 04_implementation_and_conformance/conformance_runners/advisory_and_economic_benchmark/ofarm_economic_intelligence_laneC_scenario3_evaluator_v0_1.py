import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / "ofarm_economic_intelligence_laneC_scenario3_sample_dataset_v0_1.json"
RESULTS_JSON = HERE / "OFARM_economic_intelligence_laneC_scenario3_example_results_v0_1.json"


def load():
    return json.loads(DATASET.read_text(encoding="utf-8"))


def compute(data):
    asset = data["candidateAsset"]
    annual_capacity = asset["nameplateTonnesPerHour"] * asset["availableSeasonHours"]
    base_eligible = data["volumeBasis"]["baseHarvestTonnes"] * data["volumeBasis"]["qualityFitShareBasePct"] / 100.0
    downside_eligible = data["volumeBasis"]["downsideHarvestTonnes"] * data["volumeBasis"]["qualityFitShareDownsidePct"] / 100.0
    base_util = base_eligible / annual_capacity * 100.0
    downside_util = downside_eligible / annual_capacity * 100.0
    recoverable_loss = data["volumeBasis"]["baseHarvestTonnes"] * (data["lossBasis"]["currentProcessLossSharePct"] - data["lossBasis"]["candidateProcessLossSharePct"]) / 100.0
    energy_annual = 278000.0
    energy_per_eligible_t = energy_annual / base_eligible
    capex_per_annual_capacity = asset["indicativeCapexEUR"] / annual_capacity
    all_pass = (
        base_util >= data["thresholds"]["minimumBaseUtilizationPct"] and
        downside_util >= data["thresholds"]["minimumDownsideUtilizationPct"] and
        data["volumeBasis"]["qualityFitShareBasePct"] >= data["thresholds"]["minimumQualityFitBasePct"] and
        data["volumeBasis"]["qualityFitShareDownsidePct"] >= data["thresholds"]["minimumQualityFitDownsidePct"] and
        data["marketBasis"]["committedOutletSharePct"] >= data["marketBasis"]["minimumCommittedOutletSharePct"] and
        data["workingCapitalBasis"]["assumedDays"] <= data["workingCapitalBasis"]["maximumAcceptableDays"]
    )
    outcome = "PROCEED_TO_FULL_APPRAISAL" if all_pass else "HOLD_FOR_MORE_EVIDENCE"
    return {
        "annual_capacity": round(annual_capacity, 2),
        "base_eligible": round(base_eligible, 2),
        "downside_eligible": round(downside_eligible, 2),
        "base_util": round(base_util, 2),
        "downside_util": round(downside_util, 2),
        "recoverable_loss": round(recoverable_loss, 2),
        "energy_per_eligible_t": round(energy_per_eligible_t, 2),
        "capex_per_annual_capacity": round(capex_per_annual_capacity, 2),
        "outcome": outcome,
    }


def main():
    data = load()
    metrics = compute(data)
    payload = {
        "datasetId": data["datasetId"],
        "scenarioId": data["scenarioId"],
        "screeningOnly": True,
        "fullExternalAppraisalRequired": True,
        "metrics": metrics,
    }
    RESULTS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
