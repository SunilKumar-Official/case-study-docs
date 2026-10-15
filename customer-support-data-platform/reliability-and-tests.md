# Reliability and tests

Two problems appeared after the pipeline went live. Both were found by reviewing the running system, and both were fixed by changing the design, not by patching a symptom.

## Problem 1: a collection gap that was silent for months

**What was wrong.** Extraction had been narrower than the source since it was first configured. It filtered conversations by department and by status, so some departments and every status other than "closed" were never collected live. They appeared in the data only because an older archive happened to include them. Separately, a conversation was extracted once and then never looked at again. That is right for a normal chat, which cannot change once closed. It is wrong for two real cases: a conversation that stays open for a long time, and a messaging-app channel where the same conversation identifier is reused when a customer comes back, so new messages land in a conversation that looks finished.

**The fix.**
- The department and status filters were removed. Everything the source returns now comes through normal incremental discovery.
- Eligibility changed from "extracted or not" to three categories: never extracted (full extraction, unchanged); extracted but not yet closed (a cheap single-conversation status check each run, with a full re-fetch only if the status or last-modified time changed); and messaging-app conversations (re-fetched in full every run, because the volume is small and the API cannot return only new messages).
- "Closed" is the only status treated as final. Every other status keeps a conversation eligible for recheck, because guessing the full list of statuses wrong would stop rechecking something still in flux.
- The canonical stage now also compares last-modified time, so it notices when raw data changed after first extraction, the same way it already noticed a schema-version change.
- A failed refresh leaves the previously stored record untouched, so a record is never half-overwritten.
- The history that the old filters had skipped was handled as a separate backfill, not folded into this change.

**Result.** The pipeline now captures every real conversation channel and status, and the gap that had existed for months is closed.

## Problem 2: an outage that nobody acted on

**What was wrong.** For about five days, every extraction run failed because the vendor had revoked the authentication token. Each failure sent an alert email, and delivery worked, but the emails were ignored and nothing repeated or escalated. The two downstream stages "succeeded" every day with nothing processed, because nothing was eligible. The data healed by itself afterwards only because of the overlapping collection window. A separate gap of a few days had no logs at all, and no check existed that could have shown why.

**The fix.**
- **Run history.** Every stage records each run: start, finish, a status (success, failed, no work, or skipped because the run lock was held), and how many conversations it processed. A skipped run now leaves a record instead of exiting silently. Recording can never itself fail the job.
- **A daily watchdog** reads the run history and the data itself, and gives each check OK, WARN or FAIL:
  - a stage did not run today, which means the scheduler or host is down;
  - the latest run failed or was skipped;
  - a downstream stage processed nothing for two or more days in a row;
  - the newest enriched conversation is older than a freshness limit;
  - one stage is behind the stage before it;
  - the authentication token fails a dry-run refresh.
- **One consolidated email per day.** When everything is green the subject starts with OK, which doubles as a heartbeat. Otherwise the subject says ACTION NEEDED and names what failed, and it is sent every day until every check is green. Each failing item carries a one-line runbook. If the watchdog cannot reach the database, it emails that fact directly.
- **Token hardening.** A revoked token now raises a distinct error that points at the runbook and is not retried, since the token is dead. Server and network errors retry a few times with backoff.
- **Scaling, found in the same review.** The enrichment stage rewrote its entire status table every run and scanned every canonical file to decide what to process. It now updates only the rows it touched and decides eligibility in SQL. The new logic was run against the old on the same fixtures and had to give identical results.

The rollout was staged: run history first with no visible change, then the watchdog in report-only mode for about a week to tune the thresholds, then token hardening, then the enrichment change on a quiet day.

**Result.** An outage like that one is noticed within a day, and it keeps reminding until a person acts.

## Tests

The automated suite has several hundred tests (the per-area counts below are approximate, taken from the test definitions). It covers every stage and the shared package.

| Area | Roughly | What it protects |
|---|---|---|
| Enrichment | 130 | Each of the table builders, the cleaner, the shared turn and transition logic, eligibility and idempotent writes |
| Shared platform | 85 | Configuration, storage, validation, run history, the watchdog checks and the email alerts |
| Extraction | 85 | Collection, transcript merging and de-duplication, token refresh and retries, recheck and refresh paths |
| Canonical | 40 | Parsing into the stable structure, eligibility and rebuilds |
| Orchestration | few | Jobs load and wire together |

Some tests run against a real database and are skipped when none is configured. The watchdog was tested with a replay of the outage itself: given the same pattern of failures, it must go FAIL on the first day and send an ACTION NEEDED email every day after.
