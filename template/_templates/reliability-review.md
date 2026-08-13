---
type: reliability-review
title: "Reliability Review - {{team}} - YYYY-QN"
period: "YYYY-QN"
date: YYYY-MM-DD
owner: "{{owner_slug}}"
teams: []
status: draft             # draft · final
---

<!-- The aggregate view of incidents across the org — the one an individual post-mortem
     can't give you. Look for patterns, repeat causes, and post-mortem actions that were
     written down and never done. Blameless at the aggregate level too: the unit of
     analysis is the system, not the responder. -->

## TL;DR

Two or three sentences: is reliability improving, and what's the single biggest lever.

## Volume & severity

| | This period | Last period | Trend |
|---|---|---|---|
| Sev1 | | | ↑ / → / ↓ |
| Sev2 | | | |
| Sev3+ | | | |
| Total | | | |

## By team

| Team | Incidents | Sev1/2 | Median time to resolve | Unclosed actions | Trend |
|------|-----------|--------|------------------------|------------------|-------|
|      |           |        |                        |                  | ↑/→/↓ |

## Repeat causes

_The same failure arriving twice is the most actionable thing in this document._

| Cause / pattern | Occurrences | Incidents | Underlying gap | Owner |
|-----------------|-------------|-----------|----------------|-------|
|                 |             |           |                |       |

## Detection & response

| Metric | This period | Last period |
|--------|-------------|-------------|
| Median time to detect | | |
| Median time to resolve | | |
| Detected by monitoring vs. by a human | | |
| Incidents with a completed post-mortem | | |

Where detection failed, say how it failed — no alert, wrong alert, alert ignored.

## Unclosed post-mortem actions

_Actions agreed after an incident and still not done. Age them; old ones either get
owned with a date or get formally dropped._

| Action | From incident | Age (days) | Owner | Status |
|--------|---------------|------------|-------|--------|
|        |               |            |       |        |

## What changed for the better

Fixes that landed, and evidence they worked — recurrences that stopped, detection that
improved.

## Recommendations

| Recommendation | Rationale | Owner | By |
|----------------|-----------|-------|-----|
|                |           |       |     |

## Notes

Anything the numbers don't capture — a near-miss, a fragile dependency, a team carrying
more on-call load than the incident count suggests.
