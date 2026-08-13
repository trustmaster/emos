---
name: escalation
description: Record an escalation — what's blocked, the quantified impact, what has already been tried, the specific ask with an owner and a deadline, and the fallback if the ask isn't granted — and add a follow-up TODO to the current week. Use when the user says something is blocked, stuck, needs escalating, or needs a decision from someone above them. Pass a short description as args.
roles: [director]
---

Create an escalation record for the situation in args, and put a follow-up in this
week's plan so it doesn't get quietly dropped.

Read `paths.reports` (default `10-reports`), `paths.weekly` (default `01-weekly`),
`paths.teams` (default `02-people/teams`), `paths.projects` (default `03-projects`),
`people:`, and `owner.role` from `.agents/config.yaml`.

> An escalation carries a **specific ask** — a decision, a resource, an intervention —
> to a **specific person** by a **specific date**. If there's no ask, it's a status
> update; if the user owns the fix themselves, it's a risk on a project. Say which one
> you think it is and confirm before writing a file.

## Step 1 — Establish the shape

Ask in one batch, offering your own inferences from the vault as defaults:

- **What's blocked**, and since when.
- **Who** the escalation goes to (`raised_to`).
- **The ask** — the specific thing they must do.
- **Needed by** — and the consequence of slipping.
- **Severity** — `low` · `medium` · `high`.

## Step 2 — Gather the supporting record

- **Project** — match the topic to a project in `{paths.projects}/`; take its status,
  target date, and existing Risks/Blockers rows. Set `projects:`.
- **Team** — the team that owns it, via `teams:` on the project or its hub. Set `teams:`.
- **What's already been tried** — scan the last ~8 weeks of `{paths.weekly}/`, related
  meeting notes, and the project hub for attempts, `#blocked` lines, and prior asks.
  This section is what separates an escalation from a complaint; build it from the
  record rather than asking the user to remember.
- **Impact** — pull quantified figures from incidents, dashboards, or the project hub.
  Cite the source. **Don't invent numbers** — leave a row blank and flag it.
- **Prior escalations** — check `{paths.reports}/escalations/` for the same topic. If
  this is a repeat, say so prominently: a second escalation on the same thing is a
  different conversation from a first.

## Step 3 — Fallbacks

Draft what happens if the ask isn't granted, with the cost of each option. Bringing the
fallback is what makes an escalation actionable rather than a hand-off; derive candidates
from the project's options and the do-nothing consequence.

## Step 4 — Write

Create `{paths.reports}/escalations/YYYY-MM-DD-{slug}.md` from
`_templates/escalation.md` (create the folder if needed) with `title`, `slug`,
`raised_by` (owner), `raised_to`, `status: open`, `severity`, `needed_by`, `teams:`,
`projects:`, and today's `date:`.

Then add to the current week's active file in `{paths.weekly}/`:

```
- [ ] Follow up on escalation: {title} with @{raised_to} #follow-up #escalate #project/{slug}
```

Include `#team/{team-slug}` too when a team is set.

If `07-strategy/portfolio.md` exists, mention that `/portfolio` and `/team-sync` will
surface this in the Open escalations section — don't hand-edit the portfolio here.

## Step 5 — Report

- Path written and the one-line ask, recipient, and date.
- Whether this is a repeat of an earlier escalation, with a link.
- Which impact figures are evidence-backed and which are `⚠️ needs input`.
- The follow-up TODO added to the week.

**Never contact anyone.** This skill writes a record; raising it with a person — Slack,
email, or in a meeting — is the user's to do.
