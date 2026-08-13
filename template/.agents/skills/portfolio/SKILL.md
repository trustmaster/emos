---
name: portfolio
description: Load your whole portfolio into one session — every team with its manager and health, active work grouped by team, cross-team dependencies, top risks, and open escalations — as a single briefing. For directors and other leaders of managers; the org-level counterpart of the project skill. Use when the user wants to see the state of the org, get up to speed across teams, or run a portfolio review. No args needed; pass a team slug to scope it to one branch.
roles: [director]
---

Assemble a single-session briefing across every team you lead. This is primarily a
**read + brief** workflow; the only file it may write is the portfolio hub, and only
with the user's say-so.

Read `paths.teams` (default `02-people/teams`), `paths.projects` (default
`03-projects`), `paths.reports` (default `10-reports`), and `owner.role` from
`.agents/config.yaml`. Open the role pack at `.agents/roles/{owner.role}.md`
(default `em`) and follow its portfolio note for framing.

## Step 0 — Check the ground

- If `{paths.teams}/` holds no team files, this vault hasn't adopted teams yet. Say
  so, brief on active projects only (grouped by `owner`), and suggest `/team-new`.
  Don't treat it as an error and don't create anything.
- If `07-strategy/portfolio.md` doesn't exist, **offer** to create it from
  `_templates/portfolio.md` — the narrative sections are the user's to write, so
  create it only if they say yes, and continue the briefing either way.

## Step 1 — Refresh

Run the `team-sync` logic (all teams, plus the portfolio hub if it exists) so every
rollup reflects current reality before you read it.

## Step 2 — Read the org layer

For each team hub in `{paths.teams}/` (scoped to args if given):

- frontmatter: `manager`, `status`, `headcount`, `last_health_check`, `parent_team`
- the newest **Health log** entry and its overall rating
- the freshly-regenerated Related rollup — projects, incidents, open TODOs
- the **Interfaces & dependencies** table

## Step 3 — Pull the cross-cutting context

Don't dump files; read enough to brief.

- **Work** — every active project in `{paths.projects}/` (excluding `archive/`),
  grouped by team via `teams:`. Note status, priority, target date. Projects with no
  team link go in an **Unattributed** group — that's a finding, not a failure.
- **Reliability** — incidents from the last quarter, by team; anything not yet
  `reviewed`.
- **Strategy** — active OKRs and roadmaps in `07-strategy/`, and which teams carry them.
- **Escalations** — open items in `{paths.reports}/escalations/` and any `#escalate`
  tags in the last ~6 weeks of `01-weekly/`.
- **People signals** — teams with no manager, headcount gaps, anyone `departing` in
  `{paths.profiles}/`, and skip-level coverage gaps if `skip-level` data exists.

## Step 4 — Brief

Output, in this order:

- **Snapshot** — a table: team · manager · health · headcount (current +open) ·
  active projects · last health check. Sort worst health first.
- **Where the org stands** — 3–5 sentences synthesizing delivery, reliability, and
  people across teams. Name the single thing most needing attention.
- **Strategic bets** — the portfolio hub's bets with current confidence, or the OKRs
  standing in for them.
- **Risks & cross-team dependencies** — consolidated, deduplicated across teams, each
  with the team that owns it.
- **Open escalations** — what's stuck and who owes what.
- **Blind spots** — stale health checks, unattributed projects, teams without a
  manager, unreviewed incidents, missing skip coverage. Be specific and short.
- **Suggested next actions** — 3–5 concrete items, most important first.

State whether the portfolio hub was refreshed, created, or is absent. Do not edit any
team hub's prose — health entries belong to `team-health`.
