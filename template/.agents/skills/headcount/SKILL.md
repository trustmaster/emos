---
name: headcount
description: Build or refresh the headcount plan for a period — reqs by team with status, growth versus backfill, pipeline health, attrition themes, and the prioritisation order if you get fewer reqs than you asked for. For directors and other leaders of managers who own an org's hiring plan. Use when the user wants a headcount plan, hiring plan, org shape, or req status roll-up. Pass a quarter as args (e.g. 2026-Q3); defaults to the current quarter.
roles: [director]
---

Build or refresh the headcount plan.

Read `paths.hiring_positions` (default `06-hiring/positions`), `paths.hiring_interviews`
(default `06-hiring/interviews`), `paths.teams` (default `02-people/teams`),
`paths.profiles` (default `02-people/profiles`), and `owner.role` from
`.agents/config.yaml`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

> Roles, not people. This file is about the shape of the org — it never carries
> individual performance, compensation, or attributed departure reasons. Those live in
> profiles, reviews, and the talent map.

## Step 1 — Period and scope

Quarter from args, else the current quarter (`YYYY-QN`, derived from today's date per
conventions). Teams: every hub in `{paths.teams}/`. If none exist, group by the
`team:` string on each position instead, and mention that `/team-new` would make the
roll-up exact.

## Step 2 — Gather

- **Filled headcount** per team — profiles with `teams: [{slug}]` and
  `status: active` (or the team hub's `headcount.current` where profiles are incomplete;
  say which source you used).
- **Requisitions** — every file in `{paths.hiring_positions}/`: title, team, level,
  `status`, `opened`, hiring manager. Compute **days open** for anything not `filled` or
  `cancelled`. Classify growth vs. backfill — from the position doc if it says, otherwise
  ask rather than guessing.
- **Pipeline** — candidates in `{paths.hiring_interviews}/` per open role, by stage.
  Flag roles open with zero candidates in flight, and the oldest req per team.
- **Departures** — profiles with `status: departing` or `departed` with a date in the
  period. Count them per team and summarise reason **themes** only.
- **Previous plan** — the most recent `06-hiring/headcount-*.md`. Carry forward
  unresolved asks and note what changed against it.

## Step 3 — Prioritisation

Ask the user to rank the roles, and record the rationale. Offer a starting order derived
from evidence — teams at 🔴 health, teams carrying on-call with too few people, reqs
open longest, single points of failure named in the talent map — and let them override
it. Doing this before the budget conversation is the point of the section.

## Step 4 — Write

Create `headcount-{period}.md` in the hiring root — the parent of
`paths.hiring_positions`, i.e. `06-hiring/headcount-YYYY-QN.md` by default — from
`_templates/headcount-plan.md`, with `period:`,
`teams:`, `owner:`, today's `date:`, and `status:` reflecting where the plan stands
(`planned` until approved).

If the file already exists, refresh the tables in place, preserve human-written
rationale, and **prepend** a dated entry to the Log naming what changed.

Leave any figure you couldn't source blank with `⚠️ needs input` — never estimate
headcount or budget numbers.

## Step 5 — Report

- Path written, and the summary line: filled / open / planned / expected leavers / net.
- **Pipeline risks** — open roles with no candidates, reqs open longest, teams whose
  hiring is behind the plan.
- Teams whose headcount data came from the hub rather than profiles (less reliable).
- Open asks carried forward from the previous plan that are still unanswered.
- Suggest `/team-health` for any team where the hiring gap looks like the binding
  constraint.
