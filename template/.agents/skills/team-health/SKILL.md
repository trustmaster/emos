---
name: team-health
description: Assess a team's health across delivery, quality, morale, retention, hiring, technical health and manager capacity — assembled from incidents, 1-on-1s, projects and hiring data — and append the result to the team's health log. For directors and other leaders of managers; an EM can run it for their own team. Use when the user wants a team health check, temperature read, or quarterly team review. Pass a team slug as args; no args = every team.
roles: [director]
---

Assess one team's health (or every team) and record it.

Read `paths.teams` (default `02-people/teams`), `paths.reports` (default `10-reports`),
`paths.profiles` (default `02-people/profiles`), `paths.one_on_ones` (default
`02-people/one-on-ones`), `paths.incidents` (default `05-incidents`),
`paths.hiring_positions` (default `06-hiring/positions`), and `owner.role` from
`.agents/config.yaml`.

If `{paths.teams}/` holds no team files, say so and suggest `/team-new` — don't invent
a team from `context.team`.

> **You assemble evidence and propose ratings; the ratings are the user's to confirm.**
> Present each dimension with the evidence behind it and your suggested rating, and ask
> them to adjust before writing. A health check the manager hasn't seen is a document
> written *about* them — the template's final section exists for a reason, and the
> output should remind the user to have that conversation.

## Step 1 — Scope and period

Team(s) from args, else all. Period defaults to the current quarter (`YYYY-QN`, derived
from today's date per conventions); accept a month if the user runs this monthly.
Find the previous health check for the team — its newest Health log entry and any
`{paths.reports}/*-{team}-health.md` — so every dimension gets a trend, not just a level.

## Step 2 — Gather per dimension

- **Delivery** — projects with `teams: [{slug}]`: milestones hit vs. slipped in the
  period, `target_date` changes, `#blocked` / `#risk` lines in weeklies tagged to the team.
- **Quality & reliability** — incidents in `{paths.incidents}/` linked to the team:
  count by severity, time-to-resolve, and **unclosed action items from post-mortems**
  (a strong signal; count them explicitly).
- **Morale & engagement** — 1-on-1s with the team's manager and any skip-level files for
  its members within the period: `mood:`, `#risk`, recurring frustrations. Report themes,
  never quotes attributable to one person without care.
- **Retention** — profiles with `teams: [{slug}]`: anyone `departing` or `departed` in
  the period, plus retention signals recorded in `02-people/talent-map.md` if it exists.
- **Hiring** — open positions in `{paths.hiring_positions}/` for the team, days open,
  candidates in flight, and the current headcount plan's rows for this team.
- **Technical health** — decisions and design docs about debt, on-call load noted in
  1-on-1s or incidents, toil mentioned in retros.
- **Clarity** — does the team have current OKRs/roadmap entries in `07-strategy/`, and
  do its projects link to them?
- **Manager capacity** — span of control from the roster, plus how much of the manager's
  own 1-on-1 time goes to firefighting versus everything else.

For each: the evidence, a suggested rating (🟢 / 🟡 / 🔴), and the trend against the
previous check. Where there's no evidence, say **"no signal"** — that is a finding about
the record, not a healthy rating.

## Step 3 — Confirm with the user

Show the dimension table with suggested ratings and the two or three findings you'd lead
with. Let them adjust before anything is written. Then ask which problems are the team's
to fix and which are the user's own — the template splits these deliberately.

## Step 4 — Write

1. Create `{paths.reports}/{period}-{team-slug}-health.md` from
   `_templates/team-health-check.md`, with `team:`, `teams: [{slug}]`, `period:`,
   `manager:`, `overall:`, `assessor:` and today's `date:`. Fill the dimension table,
   what's working, what's not, the numbers you actually found (leave the rest blank —
   never estimate), and the actions.
2. **Prepend** a dated summary entry to the **Health log** section of
   `{paths.teams}/{team-slug}.md` — overall rating plus one line per dimension and the
   actions. Never rewrite earlier entries.
3. Set `last_health_check:` in the team hub's frontmatter to today.
4. Run `team-sync` for the team so the rollup picks up the new report.

## Step 5 — Report

- Paths written (report + team hub entry) per team.
- Overall rating and the trend since last time.
- The dimensions with **no signal**, and what would need to be recorded to fix that.
- The actions created, and a reminder to walk the check through with the team's manager
  before treating it as final.
