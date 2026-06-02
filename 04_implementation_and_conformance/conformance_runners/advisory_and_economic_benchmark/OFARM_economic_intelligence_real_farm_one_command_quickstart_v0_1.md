# OFARM economic intelligence real-farm quickstart v0.1

## One-command run

```bash
python ofarm_economic_intelligence_real_farm_pilot_cli_v0_1.py path/to/realfarm_dataset.json --output-dir out
```

## What it writes

- readiness report JSON
- readiness report markdown
- pilot results JSON
- pilot summary markdown

## Honest interpretation

A successful run means only this:
- the farm supplied enough bounded input for the requested lane(s)
- the mechanics executed cleanly
- the outputs stayed inside their declared claim boundaries

It does **not** mean:
- OFARM has become an ERP
- field profitability is known as truth
- capex is approved
- financing is ready
- the result is a Compliance-Twin fact
