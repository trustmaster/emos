---
type: team-health
title: "Team Health - {Team}"
team: "team-slug"
teams: []                 # normally just [team-slug]
period: "YYYY-QN"         # or YYYY-MM for a monthly cadence
date: YYYY-MM-DD
assessor: "{{owner_slug}}"
manager: "slug"           # the team's manager
overall: null             # 🟢 healthy · 🟡 watch · 🔴 at risk
status: draft             # draft · final
---

<!-- A periodic read on one team, assembled from what's already recorded plus your own
     judgement. Ratings are yours to set — the evidence columns are what make them
     defensible three months later. Discuss it WITH the team's manager; a health check
     written about a manager rather than with them is a performance review in disguise. -->

## Overall

🟢 healthy / 🟡 watch / 🔴 at risk — and one sentence on why.

## Dimensions

| Dimension | Rating | Evidence | Trend |
|-----------|--------|----------|-------|
| Delivery — are commitments landing? | 🟢/🟡/🔴 | | ↑ / → / ↓ |
| Quality & reliability — incidents, escaped defects, toil | | | |
| Morale & engagement — signals from 1-on-1s and skips | | | |
| Retention — attrition, flight risk, key-person concentration | | | |
| Hiring — open reqs, pipeline, time-to-fill | | | |
| Technical health — debt, on-call load, maintainability | | | |
| Clarity — do they know what matters and why? | | | |
| Manager capacity — is the manager over-extended? | | | |

## What's working

Two or three things worth protecting. Name them so they don't get optimized away.

## What's not

The real problems, most consequential first. Distinguish problems the team owns from
problems you own.

| Problem | Whose to fix | Since | Action |
|---------|--------------|-------|--------|
|         | team / me / elsewhere | | |

## Numbers

_Only the ones you actually track. An empty row is better than an invented figure._

| Metric | This period | Last period |
|--------|-------------|-------------|
| Incidents (sev1/sev2) | | |
| Unclosed post-mortem actions | | |
| Headcount (filled / open) | | |
| Attrition (period) | | |
| On-call pages per week | | |

## Actions

- [ ] Owner — action — by YYYY-MM-DD

## Discussed with the manager

Date, and what they disagreed with. Their pushback is the most useful part of this
document — record it rather than smoothing it out.
