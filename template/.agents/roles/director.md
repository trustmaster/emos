# Director role pack

**Role key:** `director`  ← value for `config.yaml` → `owner.role`
**Status:** `shipped`

## Who this is for

Anyone whose reports are themselves managers — **senior manager, head of, director, senior
director, VP**. One pack covers the whole M2+ band, because the shape of the job is the
same at each rung and only the scale changes: you run a **portfolio of teams** through
their managers, and your leverage is in strategy, talent, and the systems the org runs on
rather than in the work itself.

If your org's vocabulary differs enough to matter, copy this pack to
`.agents/roles/{your-key}.md` and edit it — see [docs/roles.md](../../docs/roles.md).
Shipped packs are framework-owned; a pack you add is yours.

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

## The org layer

This is the pack that most benefits from emOS's optional **team entities**
(`02-people/teams/{slug}.md`, joined with `teams: [slug]` / `#team/{slug}`). Registering
your teams with `/team-new` unlocks the rollups everything else in this pack reads:
portfolio status, team health, headcount by team, calibration grouped by manager.

It stays optional. Without teams, every skill here still runs — it just groups by project
and person instead, and says so.

## Sections in focus / dormant

In focus: `07-strategy` (OKRs, roadmaps, the portfolio hub — primary), `03-projects` framed
as **programs** spanning teams, `02-people` (teams, manager development, calibration,
talent map), `10-reports` (portfolio update, briefs, escalations, QBR, reliability),
`05-incidents` (aggregate/trend, not individual post-mortems), `06-hiring` (senior pipeline
/ headcount plan). All dashboards apply, weighted toward strategy and people.

## Skill notes

**Core role-sensitive skills**

- **1on1** — with **managers** (their team health, delivery, people risks, decisions to
  confirm) and **skip-levels** (upward signal, growth). Relation drives which framing.
- **perf-review** — you review your managers (subject ≠ owner); dimensions above emphasize
  org impact and talent development. Also supports rolling up calibration evidence.
- **manager-report** — a **portfolio update** up and out: cross-team delivery, strategic
  bets, org/people signals, escalations — aggregated across teams, not one team. Groups
  Delivery & Execution by team when team entities exist, and pulls in open escalations.
- **morning / weekly-review** — surface cross-team risks and program deadlines; 1-on-1s are
  with managers/skips.

**Org & portfolio**

- **team-new / team-sync** — register the teams you lead and keep their rollups current.
  The gateway to everything below; skipping it costs nothing but sharpness.
- **portfolio** — the org-scale `/project`: every team, work grouped by team, cross-team
  dependencies, risks, escalations, and blind spots. Your Monday-morning read.
- **team-health** — the periodic per-team assessment that feeds the portfolio and your
  1-on-1 with each manager. Run it *with* the manager, not about them.

**People at scale**

- **skip-level** — prep one, or (no args) get coverage across the org: who you're overdue
  with, recurring themes, and where skip signal contradicts what managers report.
- **calibration** — evidence grouped by manager plus cross-team consistency checks.
  Never proposes a rating; the point is a fair bar, not a generated verdict.
- **talent-map** — placement, promotion candidates, key-person risk, succession cover.
  Evergreen; refresh it each cycle.
- **promo-case** — evidence that someone *already operates* at the target level, with the
  counter-argument written out honestly.

**Cadence, comms & operations**

- **staff-meeting** — your leadership-team series, carrying open actions forward. Stale
  actions surfacing across three sessions is the signal to act on.
- **exec-brief** — a one-page decision memo when you need a specific decision from someone
  senior. **escalation** — when you need an intervention, with the ask, the impact, and
  the fallback.
- **headcount** — the org's shape for the period: reqs by team, pipeline health, attrition
  themes, and the prioritisation order decided before the budget conversation.

**Strategy rollups**

- **qbr** — commitments versus outcomes first, highlights second. Include what was dropped.
- **reliability-review** — the aggregate incident view: repeat causes and post-mortem
  actions nobody closed. This is the director's version of `05-incidents`, not a
  substitute for individual post-mortems.

**Handling note.** `talent-map`, `calibration`, `promo-case` and skip-level notes carry
personal assessments (`sensitive: true`): never published externally, never pasted into
chat tools, never shared with their subjects. See `.agents/conventions.md` → *Sensitive
Content*.
