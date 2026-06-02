# OFARM economic intelligence real-farm data request sheet v0.1

## Rule zero

Do **not** ask the farm for data just because software could theoretically ingest it.
Ask only for what the three bounded lanes require.

## Lane A — operational-only screening

Need:
- 2+ crop/system alternatives
- area (ha)
- expected yield range
- expected selling price range
- labour hours/ha
- machine hours/ha
- fuel litres/ha
- seed quantity/ha
- input quantity index or comparable operational intensity proxy
- basis refs

Do not ask for:
- full accounting export
- fixed-cost allocations
- whole-farm overhead buckets
- tax or payroll detail

## Lane B — own vs contractor / bottleneck screen

Need:
- crop/system
- area
- expected yield and price
- available days in the bottleneck window
- own machine hours available
- own labour hours available
- contractor guaranteed capacity
- own fuel litres/ha
- own labour hours/ha
- benchmark wear/parts per ha
- contractor rate/ha
- mobilisation cost
- fuel price
- labour rate
- untimely-area penalty assumption

Optional but useful:
- stronger contractor guarantee basis
- stronger penalty basis

Do not ask for:
- full field profitability allocations
- whole-farm fixed cost tables unless later justified

## Lane C — capex pre-gate screening

Need:
- candidate asset name
- indicative capex
- nameplate tonnes/hour
- available season hours
- base harvest tonnes
- downside harvest tonnes
- quality-fit shares
- committed outlet share and minimum acceptable committed share
- current vs candidate loss shares
- working-capital days assumption and maximum acceptable days
- utilization and quality-fit thresholds
- imported fact extract refs
- operational refs

Do not ask for initially:
- full NPV model
- full IRR model
- full debt schedule
- banker pack
- full board/investment committee paper
- line-by-line GL export

## Redaction minimum

Replace with stable redacted refs:
- farm ids
- field ids
- facility ids
- operation ids
- contractor extract ids
- settlement extract ids

Remove unless indispensable:
- staff names
- government ids
- bank details
- raw invoice payloads
- buyer names if coded refs are enough
