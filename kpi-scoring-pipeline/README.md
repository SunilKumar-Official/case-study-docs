# KPI Scoring Pipeline

One scoring method for every operational team, replacing manual monthly calculations. It feeds HR's appraisal process and Finance's incentive payouts.

This folder is documentation only. There is no code, query or data here, and no names from the business the pipeline was built for.

Case study on the portfolio site: <https://sunilkumar-official.github.io/projects/kpi-scoring-pipeline/>

## The problem

Every team calculated performance differently. Some used weighted models, some used slabs, one used points instead of percentages, and some tracked KPIs by hand in spreadsheets. Results could not be compared across departments, and most of it was recalculated manually every month.

## What I built

I designed one Combined Performance Score (CPS) method that works the same way for every role, agreed the weightings with each department's stakeholders, and built the pipeline that runs it.

- 100+ KPI metrics defined; each role has five core KPIs plus three gateway metrics.
- Every KPI is converted to an achievement percentage (target against actual), multiplied by its weight, and summed into one score per person.
- Gateway metrics decide incentive eligibility without changing the score, so measuring performance and qualifying for an incentive stay separate.
- People are then stack-ranked within their department, split into gateway-qualified and not.

## What is in this folder

| File | What it covers |
|---|---|
| [architecture.md](architecture.md) | The stages of a run, how data moves between them, and why it is built that way |
| [validation-and-tests.md](validation-and-tests.md) | What the output checks catch, how a run reports its own health, and what the test suite covers |

## Scope and limits

- This is a description of the design, not a runnable project.
- A small number of KPI definitions still lack a working query, and the incentive structure for one team is under review. Both are separate from the scoring pipeline.
