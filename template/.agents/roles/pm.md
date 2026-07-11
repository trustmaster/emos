# Product Manager role pack

**Role key:** `pm`  ← value for `config.yaml` → `owner.role`
**Status:** `shipped`

## Who this is for

Product managers who own outcomes through influence rather than authority. Work centers on
PRDs and initiatives, roadmap and OKRs, launches and experiments, user research, and keeping
a wide set of stakeholders aligned.

## Vocabulary

| Token | Value for this role |
|-------|---------------------|
| `{{role_report_slug}}` | `launch-status` |
| `{{role_report_title}}` | `Product Status - {{team}}` |
| `{{review_dimensions}}` | `Product Sense, Execution, Influence, Data, Strategy` |
| `{{oneonone_default_relation}}` | `stakeholder` |
| `{{status_report_audience}}` | `your stakeholders and eng/design partners` |

## People & relationships

`people:` are your **stakeholders** and cross-functional partners — eng lead, design, data,
execs — plus user-research contacts. Default `relation: stakeholder` (or `peer` for your eng
lead). You align and influence; you don't coach or manage. Leave `skill_will` blank.

## Sections in focus / dormant

In focus: `03-projects` (PRDs / initiatives), `07-strategy` (roadmaps, OKRs — heavy),
`08-meetings`, `10-reports` (launch/roadmap updates), `04-decisions` (product decisions),
`09-knowledge` (user research, feedback). Dormant: `05-incidents`, `06-hiring`.

## Skill notes

- **1on1** — lateral **stakeholder alignment**: shared goals, dependencies you owe/are owed,
  risks, decisions to land. Not coaching.
- **perf-review** — self-review by default (subject = owner) using the dimensions above;
  evidence from your own launches, PRDs, experiments, research, projects, and decisions. If
  your org has you review others, subject can be another person.
- **manager-report** — a **product status update** for stakeholders: launch/experiment
  progress, roadmap movement, metrics, decisions needed, cross-functional asks.
- **morning / weekly-review** — surface launch dates and decision deadlines rather than
  1-on-1s.

## PM artifact skills

These create the PM-specific deliverables the sections above lean on. They are ordinary
skills (any role may use them) but are the daily tools of this role — reach for them instead
of hand-rolling the docs:

- **`prd-new <title/project>`** — a Product Requirements Doc in the parent project's `docs/`
  (`03-projects/{slug}/docs/prd.md`). The spec behind an initiative: problem, goals/non-goals,
  requirements, success metrics, rollout.
- **`experiment-new <name/project>`** — an A-B test / experiment brief in
  `03-projects/{slug}/docs/experiments/`: hypothesis, primary + guardrail metrics, variants,
  sizing, results log, decision.
- **`roadmap-new <horizon>`** — a Now / Next / Later roadmap in `07-strategy/roadmaps/`
  (`type: roadmap`). Set `projects:` to have it surface in those hubs' **Strategy** rollup.
- **`research-new <topic>`** — a user-research / interview-synthesis note in
  `09-knowledge/research/`. Link `projects:` to surface it in the hub's **Knowledge** rollup.
  Keep PII out — reference participants as P1, P2, ….

PRDs and experiments live **inside** the project folder (browsable there); roadmaps and
research are cross-cutting and roll up to any project they link.
