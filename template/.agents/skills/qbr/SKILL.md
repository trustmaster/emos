---
name: qbr
description: Assemble a quarterly business review — commitments versus outcomes, OKR scoring, delivery highlights, reliability and people metrics, lessons, and next quarter's bets — from OKRs, projects, incidents and hiring data across teams. For directors and other leaders of managers presenting to leadership. Use when the user is preparing a QBR, quarterly review, or end-of-quarter readout. Pass a quarter as args (e.g. 2026-Q2); defaults to the quarter just ending.
roles: [director]
---

Assemble the quarterly business review.

Read `paths.okrs` (default `07-strategy/okrs`), `paths.roadmaps` (default
`07-strategy/roadmaps`), `paths.projects` (default `03-projects`), `paths.incidents`
(default `05-incidents`), `paths.teams` (default `02-people/teams`), `paths.reports`
(default `10-reports`), `paths.hiring_positions` (default `06-hiring/positions`), and
`owner.role` from `.agents/config.yaml`. Open the role pack at
`.agents/roles/{owner.role}.md` for `{{status_report_audience}}`.

**Resolve voice:** read `agent.voice` from `.agents/config.yaml`. If it's set and the file
exists, read it (plus `samples/` alongside it) and match its register in the file you write.
Apply it to the artifact only — never to your chat reply or progress narration. If the key is
absent, write plainly and say nothing; if it's set but the file is missing, say so once and
write plainly.

> **Start with commitments, not highlights.** A QBR assembled from the best things that
> happened is a highlight reel; one assembled from what was promised is a review. Build
> the commitments table first, from the quarter's OKRs and roadmap as they stood at the
> start — including the items that were quietly dropped.

## Step 1 — Period and commitments

1. Quarter from args, else the quarter just ending (derive `YYYY-QN` from today's date
   per conventions).
2. Read `{paths.okrs}/{quarter}.md` and any roadmap in `{paths.roadmaps}/` covering it.
   Take every objective, key result, and "Now" initiative as a commitment.
3. Read the roadmap's Revision log and the OKR check-ins to find what **moved or was
   dropped mid-quarter**. Dropped commitments belong in the table with status `⏭ dropped`
   and a reason — omitting them is the most common way a QBR misleads.

## Step 2 — Gather outcomes

- **Delivery** — projects with `quarter: {quarter}` or activity in the window: completed
  vs. slipped, and each one's outcome. Group by team via `teams:`. Prefer outcome
  statements over activity; if a project records no outcome, say so.
- **OKR scoring** — actuals from the OKR file's check-ins and KR tables. Use the recorded
  numbers only; never compute a score from an absent value.
- **Reliability** — incidents in the quarter by severity, plus unclosed post-mortem
  actions. If a `{paths.reports}/{quarter}-reliability.md` exists, use it rather than
  re-deriving, and link it.
- **People** — headcount plan for the quarter, hires, departures, and each team's latest
  health rating from its hub.
- **Learnings** — the OKR retrospective, weekly Insights sections, and decisions that
  reversed an earlier one. Reversals are usually the most honest learnings available.

## Step 3 — Next quarter

Draft the bets from: the next roadmap horizon, projects with `status: proposed`, and
carry-over from missed commitments. For each, the outcome being bought and a confidence
level. Then draft **what we're explicitly not doing** — from the roadmap's Later column
and parking lot. Ask the user to confirm both; these are their calls, not derivable.

## Step 4 — Write

Create `{paths.reports}/{quarter}-qbr.md` from `_templates/qbr.md` with `quarter:`,
`teams:`, `audience:` (default the pack's `{{status_report_audience}}`),
`status: draft`, today's `date:`.

Populate every section from the sources above. Mark any figure you couldn't source
`⚠️ needs input` — **never estimate a metric for a leadership audience**. Leave the
Asks section for the user.

## Step 5 — Report

- Path written.
- **Commitment scorecard** — delivered / partial / missed / dropped counts, and which
  dropped items have no recorded reason.
- Sections that are evidence-backed vs. the `⚠️ needs input` list.
- Anything that contradicts itself across sources (an OKR marked on-track whose project
  slipped, a team rated 🟢 with three sev1s) — surface it before the audience does.
- Suggest `/reliability-review` if the reliability section had to be derived from raw
  incidents, and `/headcount` if the people numbers were thin.
