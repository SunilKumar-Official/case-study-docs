# Customer Support Data Platform

A scheduled data pipeline that turns raw support-chat conversations into clean, queryable relational tables, with monitoring that escalates until someone acts. It also includes the shared platform the pipeline runs on.

This folder is documentation only. There is no code, query, credential or data here, and no names from the business the platform was built for.

Case study on the portfolio site: <https://sunilkumar-official.github.io/projects/customer-support-data-platform/>

## The problem

Raw support-chat conversations arrive one API call at a time, in a source-specific shape that changes meaning depending on who is asking. Reporting, workforce planning and later analysis all need the same clean, structural view of what happened in a conversation, and none of them should re-derive it from the raw format every time.

## What I built

- **A three-stage pipeline:** extraction, a canonical conversation model, and enrichment into relational tables. Each stage is its own project, runs on its own schedule, and depends on the others only through the shape of the data it reads.
- **180,000+ conversations** processed through it.
- **Ten relational tables** covering conversations, customers, messages, event timelines, turns and response times, bot menu interactions, handoffs, abandonments, contact reasons and per-conversation metrics. Since then an hourly agent-activity table and a set of workforce-planning views (chat volume, demand pattern, peak intervals, volume forecast) have been added on top.
- **The platform underneath:** a shared Python package for configuration, storage and validation, an orchestrator (Dagster) that composes the projects, and a Postgres store. I designed it and I administer it.
- **Two production problems found and fixed** after it went live, described in [reliability-and-tests.md](reliability-and-tests.md): a silent gap in what was being collected, and an outage that went unnoticed for days.

## What is in this folder

| File | What it covers |
|---|---|
| [architecture.md](architecture.md) | The platform, the three stages, how data moves between them, and why it is built that way |
| [reliability-and-tests.md](reliability-and-tests.md) | The two production problems and their fixes, the monitoring design, and what the test suite covers |

## Scope and limits

- This is a description of the design, not a runnable project.
- The deterministic tables are the scope of this pipeline. Language-model interpretation and joining to a business-outcome system were deliberately left out of this build, because no such data source was connected.
- Alerting uses email only. A second channel and an external heartbeat were considered and left out of scope.
