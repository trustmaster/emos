---
name: exec-brief
description: Draft a one-page decision memo or pre-read for leadership — the ask, situation, options with trade-offs, a recommendation, risks, and next steps — assembled from project, decision, and incident context already in the vault. For anyone who needs to get a decision from someone senior. Use when the user wants a brief, exec summary, pre-read, one-pager, or decision memo. Pass the topic as args.
roles: [director]
---

Draft a one-page decision brief on the topic in args.

Read `paths.reports` (default `10-reports`), `paths.projects` (default `03-projects`),
`paths.decisions` (default `04-decisions`), and `owner.role` from `.agents/config.yaml`.
Open the role pack at `.agents/roles/{owner.role}.md` for `{{status_report_audience}}`
as the default audience.

> A brief exists to get **a specific decision** from a specific person. If the user
> can't name the decision and the decider, say so — what they want is probably a status
> update (`manager-report`) or an escalation (`escalation`). Ask before writing.

## Step 1 — Frame it

Ask, in one batch:

- **The decision** — what exactly are you asking them to decide?
- **The decider / audience** — default to the pack's `{{status_report_audience}}`.
- **By when** — and what happens if it slips.

Then form your own view of the answer to "why is this on their desk and not yours?" and
state it in the brief. A brief that could have been an email you sent yourself wastes a
senior person's attention.

## Step 2 — Gather

Pull only what bears on the decision:

- **Projects** matching the topic — status, target dates, blockers, the hub's Risks table.
- **Decisions** — existing ADRs that constrain the options, and any `status: proposed`
  ADR this brief would resolve.
- **Incidents** — anything that motivates urgency, with dates and impact.
- **Design docs / PRDs** in project `docs/` — for the options and their costs.
- **Strategy** — the OKR or roadmap commitment this affects.
- **Numbers** — cost, latency, revenue, headcount figures already recorded somewhere.
  Cite the source file for each. **Never estimate a number that isn't written down** —
  leave it blank and flag it as needing input.

## Step 3 — Build the options

At least two real options plus **do nothing**, each with cost, risk, and whether it's
reversible. A reversible option with a mediocre outcome often beats an irreversible
better one, and the table should make that visible.

Then write the recommendation: which option, the trade-off you're accepting, your
confidence, and what would change your mind. If the evidence doesn't support a
recommendation, say that rather than manufacturing one.

## Step 4 — Write

Create `{paths.reports}/briefs/YYYY-MM-DD-{slug}.md` from `_templates/exec-brief.md`
(create the `briefs/` folder if needed). Fill `title`, `slug`, `audience`,
`decision_by`, `status: draft`, and the `teams:` / `projects:` join keys.

Keep it to one page. Anything that isn't needed to make the decision goes in the
appendix or gets cut. Mark every unfilled figure `⚠️ needs input` rather than guessing.

## Step 5 — Report

- Path written and the one-line ask.
- Which sections are evidence-backed and which need the user's own judgement.
- Every `⚠️ needs input` item.
- Whether an ADR should follow the decision (`/decision`), and whether this should be
  circulated as a pre-read before the forum.

**Never send or publish it.** Circulating a brief is the user's call — if they want it
in Confluence or Docs, they'll ask, and the publishing skills need an explicit go-ahead.
