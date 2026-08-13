---
name: reliability-review
description: Aggregate incident trends across teams for a period — volume and severity, repeat causes, detection and response times, and post-mortem actions that were agreed and never closed. The org-level view an individual post-mortem can't give you. Use when the user wants an incident trend review, reliability roll-up, or to know whether reliability is actually improving. Pass a period as args (e.g. 2026-Q2); defaults to the current quarter.
roles: [director]
---

Aggregate incident data across the org for the period.

Read `paths.incidents` (default `05-incidents`), `paths.teams` (default
`02-people/teams`), `paths.reports` (default `10-reports`), `paths.projects` (default
`03-projects`), and `owner.role` from `.agents/config.yaml`.

If `{paths.incidents}/` has no files in the period, say so plainly and stop — an empty
quarter is a result, not an error, though it's worth asking whether incidents are being
recorded at all.

> Blameless at the aggregate level too. The unit of analysis is the system: causes,
> detection gaps, and unfinished follow-through. Never rank teams or people by incident
> count — a team owning the riskiest surface will always top that list, and publishing it
> teaches people to under-report.

## Step 1 — Period and population

Period from args, else the current quarter (`YYYY-QN` derived from today's date per
conventions). Collect every incident whose `date_detected` falls in the window. Attribute
each to a team via `teams:`, or the owner's team, or the linked project's team — in that
order. List anything you couldn't attribute rather than dropping it.

Find the previous period's review (`{paths.reports}/*-reliability.md`) so every metric
has a comparison. Without a trend, this document is just a count.

## Step 2 — Derive the metrics

Use only fields that are actually recorded — `severity`, `date_detected`,
`date_started`, `date_resolved`, `time_to_detect_days`, `time_to_resolve_days`,
`status`, `impact`. Where a field is missing, exclude that incident from *that* metric
and report the coverage (e.g. "median TTR over 7 of 11 incidents"). **Never impute a
duration.**

- Volume by severity, with the trend.
- Per team: count, sev1/2, median time to resolve, unclosed actions.
- Median time to detect and to resolve; how many were found by monitoring versus by a
  person (from the post-mortem's detection notes).
- How many incidents have a completed post-mortem (`status: reviewed`) versus not.

## Step 3 — Repeat causes

The section that earns the review. Group incidents by root cause and contributing
factors from their post-mortems — the same dependency, the same missing alert, the same
deploy pattern, the same overloaded component. Two occurrences is a pattern worth a row.
For each: occurrences, links, the underlying gap, and who owns closing it.

Also scan for **near-misses** recorded in incident notes or weeklies but never opened as
incidents; note them separately.

## Step 4 — Unclosed post-mortem actions

Walk every post-mortem in the period **and the two before it**, and collect unchecked
`- [ ]` action items. Age each from the incident's date. This list is usually the single
most useful output — old actions either get an owner and a date, or get formally dropped.

## Step 5 — Write

Create `{paths.reports}/{period}-reliability.md` from
`_templates/reliability-review.md` with `period:`, `teams:`, `owner:`, `status: draft`,
today's `date:`. Fill the tables from the steps above; leave unsourced cells blank with
`⚠️ needs input`.

Then draft recommendations — each tied to a specific finding, with an owner and a date.
Recommendations without an owner get dropped; say so rather than listing them.

## Step 6 — Report

- Path written and the headline: is reliability improving, flat, or worse, and on what
  evidence.
- Metric coverage — which metrics rest on partial data, and which incident records are
  missing fields (name them; that's a fixable process problem).
- Top repeat causes and the count of unclosed actions with the oldest age.
- Incidents that couldn't be attributed to a team.
- Suggest `/team-health` for any team whose reliability picture looks like the binding
  constraint, and `/escalation` if a repeat cause needs a decision above the user.
