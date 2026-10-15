# Validation and tests

Two separate safety nets: checks that run on the data in every run, and an automated test suite that guards the code.

## Checks inside every run

**Output validation.** Every metric's output is checked before it can be scored. The checks cover:

- null values and duplicate rows;
- wrong data types and out-of-range values;
- rows outside the reporting window;
- people who are not in the employee master;
- metrics that are not registered, so a stray key inside a registered query is still caught;
- missing or unexpected coverage: a person who should have a value for a metric and does not, or the reverse.

Each check is either a **hard check** or a **warning**. Rows that fail a hard check are quarantined, written to a review file and kept out of scoring. Warnings are reported without removing rows.

**Coverage.** The definitions file is compared against the registered metrics, so a KPI cannot exist on paper without a working query, and a query cannot run without a definition.

**Source checks.** For metrics where "no rows" could mean either "nothing happened" or "the query broke", the source data is checked separately for records in the window.

**Reconciliation.** Row counts are compared between stages so that people are not lost or invented between the employee master, the actuals and the final output. A mismatch marks the run as having problems.

**Not-scored report.** Anyone who ends up without a score is listed with the reason, so a gap is never silent.

This validation layer has caught real data problems before they reached a report, including a production query that claimed to filter on a field it actually did not.

## Run health

A run's final folder name states its outcome (`OK`, `PROBLEMS`, `INCOMPLETE`), and its manifest records every step. A run that finishes with problems still writes scores, but they are marked and must be reviewed before use.

## Test suite

The suite is more than 500 automated tests. The areas below add up to roughly 410; the remainder covers a separate workflow module that this write-up does not describe. Counts are approximate.

| Area | Roughly | What it protects |
|---|---|---|
| Run orchestration | 100 | Step order, error handling, status and exit codes, the manifest |
| Scoring | 70 | CPS calculation, stack ranking, joining actuals to definitions, gaps and the not-scored report |
| Output validation | 60 | Each hard check and warning, quarantine behaviour, audience coverage |
| Metric registry, coverage and catalogue | 60 | Registered metrics against definitions, the query runner, the generated KPI catalogue |
| Employee master and employment window | 45 | Full-month, joined, left and both cases, and the as-of-month rule |
| Per-metric query checks | 40 | The calculation behind individual KPIs, such as ratios, windows and edge cases |
| Run record and reconciliation | 25 | Run folder lifecycle, manifest content, row-count reconciliation |

The tests use fixed example data and need no connection to the warehouse.
