---
name: calibration
description: Assemble a calibration pack for a review cycle — per-person evidence grouped by manager, a distribution view, and consistency cross-checks across teams — without proposing or inventing any rating. For directors and other leaders of managers who calibrate across several teams. Use when the user is preparing for a calibration or talent-review session. Pass the cycle as args (e.g. 2026-EOY); defaults to the most recent open cycle.
roles: [director]
---

Assemble the evidence pack for a calibration session across the people in your org.

Read `paths.profiles` (default `02-people/profiles`), `paths.reviews` (default
`02-people/reviews`), `paths.one_on_ones` (default `02-people/one-on-ones`),
`paths.teams` (default `02-people/teams`), and `owner.role` from `.agents/config.yaml`.
Open the role pack at `.agents/roles/{owner.role}.md` for `{{review_dimensions}}`.

> **The hard rule, same as `perf-review`: never invent, propose, or infer a rating.**
> You gather evidence and surface inconsistencies. Humans decide in the room. If a
> manager has already submitted a proposed direction, record it verbatim as *theirs* and
> attribute it — never generate one where none exists, and never "fill the gap" for a
> person with thin evidence.

## Step 1 — Scope the cycle and the population

1. Cycle from args, else the most recent directory under `{paths.reviews}/` without
   `status: finalized` files, else ask.
2. Population: everyone reporting into your org — profiles with `relation: report`
   (your managers) **and** everyone whose `manager:` is one of them. Group by manager,
   then by team (via `teams:` on the profile, or the team hub's roster).
3. Show the roster and the grouping, and ask whether to add or drop anyone **before**
   gathering evidence. Getting the population wrong wastes the whole pass.

## Step 2 — Gather evidence per person

For each person, pull only what's already written down:

- Any existing review draft at `{paths.reviews}/{cycle}/{slug}.md` — including the
  manager's proposed direction if present.
- 1-on-1 files in `{paths.one_on_ones}/{slug}/` within the cycle: `#win`, `#feedback`,
  `#risk`, growth-area movement.
- Projects in `03-projects/` where they are `owner` or in `team_members` — outcomes,
  not activity.
- Incidents in `05-incidents/` they owned or responded to.
- Weekly mentions of `@FirstName` across `01-weekly/` in the cycle window.
- Their profile: level, time in level, growth areas, strengths.

Rate each person's **evidence strength** — `strong` / `adequate` / `thin` — on the
written record alone. Thin evidence about a strong performer is a *management* finding
(their work isn't being recorded), and should be reported as such rather than held
against them.

## Step 3 — Cross-checks

This is the part that earns the session. Fill the cross-check table in the template:

- **Same words, different bars** — managers using identical language for visibly
  different scope or outcomes.
- **Same performance, different words** — comparable evidence described far more
  favourably in one team than another.
- **Thin evidence** — a proposed direction the record doesn't support in either direction.
- **Recency bias** — a case resting entirely on the final weeks of the cycle.
- **Scope vs. level** — people whose evidence sits clearly above or below their level's
  expectations, per the role pack's `{{review_dimensions}}`.
- **Coverage gaps** — people with almost no written record; name their manager.

Report each as an observation with the files behind it. Never as a verdict.

## Step 4 — Write the pack

Create `{paths.reviews}/{cycle}/_calibration.md` from `_templates/calibration-pack.md`
(the leading underscore keeps it from colliding with a person's review file). Set
`cycle:`, `status: draft`, `sensitive: true`, `teams:`, and today's `date:`.

Fill the roster, the per-person evidence blocks, the cross-checks, and the coverage
counts in the distribution table. **Leave every rating cell empty.** If the user names
the org's distribution guidance, record it under the distribution view as context.

## Step 5 — Report

- Path written, people covered, grouped by manager.
- Evidence strength counts, and the specific people whose record is too thin to assess.
- The cross-check findings, most consequential first.
- What a human still has to supply: ratings, promotion decisions, and any deviation from
  distribution guidance.

**Handling:** the pack is `sensitive: true` — never publish it to Confluence, Docs,
Drive or Slack, don't paste its contents into a shared channel, and keep quotes from
1-on-1s to what is necessary to support a point.
