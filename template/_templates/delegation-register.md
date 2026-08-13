---
type: delegation-register
title: "Delegation & Decision Rights - {{team}}"
owner: "{{owner_slug}}"
status: active            # active · archived
teams: []
updated: YYYY-MM-DD
---

<!-- Who decides what, written down before it's contested. Most delegation friction is
     not disagreement about the answer — it's two people with a different idea of whose
     call it was. Keep this short enough that people actually read it. -->

## How to read this

Each row names a decision type and who owns it. "Consulted" means their input is
required before deciding; "informed" means they hear about it after. If a row is
ambiguous in practice, that's the row to fix.

## Decision rights

| Decision | Decides | Consulted | Informed | Notes |
|----------|---------|-----------|----------|-------|
| Technical approach within a team's scope | team manager / tech lead | | me | |
| Cross-team architectural change | | | | write an ADR |
| Hiring: level and offer | | | | |
| Hiring: headcount allocation | me | managers | | |
| Performance ratings | manager | me (calibration) | | |
| Promotions | | | | via calibration |
| Roadmap commitments for a quarter | | | | |
| Adding work mid-quarter | | | | |
| Vendor / spend above {threshold} | | | | |
| Declaring an incident sev1 | on-call | | me | no permission needed |
| Public / customer communication | | | | |

## Escalation paths

| Situation | Goes to | Within |
|-----------|---------|--------|
| Cross-team dependency stuck | | 2 working days |
| Sev1 incident | | immediately |
| Attrition risk on a key person | | same week |
| Scope conflict between teams | | next staff meeting |

## Delegated with a safety net

_Things you've handed over but are still watching, with the date you stop watching.
Delegation without an end date is supervision._

| What | To | Since | Checkpoint | Fully theirs when |
|------|-----|-------|------------|-------------------|
|      |     |       |            |                   |

## Reserved

The small number of decisions you're deliberately keeping, and why. Being explicit about
these buys credibility for everything you did delegate.

| Decision | Why it stays with me | Revisit |
|----------|----------------------|---------|
|          |                      |         |

## Log

<!-- Append-only. Newest on top. Record what moved and when. -->

### YYYY-MM-DD

- Change and rationale.
