# Director role pack

**Role key:** `director`  ← value for `config.yaml` → `owner.role`
**Status:** `shipped`

## Who this is for

Directors and senior leaders who run a **portfolio of teams** through their managers. Work
spans strategy and OKRs, cross-team programs, talent and calibration across many people,
headcount, and up-and-out reporting.

## Vocabulary

| Token | Value for this role |
|-------|---------------------|
| `{{role_report_slug}}` | `portfolio` |
| `{{role_report_title}}` | `Portfolio Update - {{team}}` |
| `{{review_dimensions}}` | `Org Impact, Strategy, Talent, Execution, Stakeholder` |
| `{{oneonone_default_relation}}` | `report` |
| `{{status_report_audience}}` | `your leadership / VP (up and out)` |

## People & relationships

`people:` are the **managers who report to you** (default `relation: report`) and your
**skip-levels** (`relation: skip`), plus peer directors and your own leadership. Coaching is
manager-development-flavored; skip 1-on-1s are for signal, not day-to-day direction.

## Sections in focus / dormant

In focus: `07-strategy` (OKRs, roadmaps — primary), `03-projects` framed as **programs**
spanning teams, `02-people` (manager development + calibration), `10-reports` (portfolio
summary), `05-incidents` (aggregate/trend, not individual post-mortems), `06-hiring` (senior
pipeline / headcount). All dashboards apply, weighted toward strategy and people.

## Skill notes

- **1on1** — with **managers** (their team health, delivery, people risks, decisions to
  confirm) and **skip-levels** (upward signal, growth). Relation drives which framing.
- **perf-review** — you review your managers (subject ≠ owner); dimensions above emphasize
  org impact and talent development. Also supports rolling up calibration evidence.
- **manager-report** — a **portfolio update** up and out: cross-team delivery, strategic
  bets, org/people signals, escalations — aggregated across teams, not one team.
- **morning / weekly-review** — surface cross-team risks and program deadlines; 1-on-1s are
  with managers/skips.
