# Individual Contributor role pack

**Role key:** `ic`  ← value for `config.yaml` → `owner.role`
**Status:** `shipped`

## Who this is for

Individual contributors and senior+/staff engineers with no direct reports. Work is organized
around your own delivery, technical craft, and collaboration — plus managing up and keeping a
running record of your impact for reviews.

## Vocabulary

| Token | Value for this role |
|-------|---------------------|
| `{{role_report_slug}}` | `snippets` |
| `{{role_report_title}}` | `Weekly Snippets - {{owner_name}}` |
| `{{review_dimensions}}` | `Delivery, Technical, Craft, Collaboration, Growth` |
| `{{oneonone_default_relation}}` | `manager` |
| `{{status_report_audience}}` | `your manager and teammates` |

## People & relationships

`people:` are your **manager**, close collaborators, and mentors — not reports. Default
`relation: manager` for the person you most often meet 1-on-1. You rarely coach anyone; you
align, get unblocked, and manage up. Leave `skill_will` / `growth_areas` blank on others'
profiles.

## Sections in focus / dormant

In focus: `01-weekly`, `03-projects` (your **design docs / RFCs** live in each project's
`docs/`), `04-decisions` (ADRs that fall out of your design work), `10-reports` (weekly
snippets + your evergreen brag log), `09-knowledge` (learning notes), `05-incidents` (on-call
participation). Dormant: `06-hiring` (unless you interview), most of `02-people/reviews` except
your **own** self-review.

## Skill notes

- **1on1** — default is your 1-on-1 with your **manager** (upward): topics to raise, decisions
  to confirm, help needed, wins to make visible. Peer/mentor 1-on-1s use lateral framing.
- **perf-review** — **self-review / brag-doc** is the default: subject is the owner. Gather
  evidence from the owner's **own** weeklies, projects, decisions, and incidents (not
  `@mention` scans of someone else) — and from the **brag log** (`10-reports/brag-log.md`) if
  it exists, which is the richest source. Use the dimensions above; never invent ratings.
- **manager-report** — weekly **snippets**: what you shipped, what's next, blockers/asks —
  accomplishment-oriented, not team-sentiment.
- **morning / weekly-review** — 1-on-1 surfacing is optional; lead with your own TODOs,
  blockers, and project deadlines.

## IC artifact skills

These create the IC-specific deliverables the sections above lean on. They are ordinary skills
(any role may use them) but are the daily tools of this role — reach for them instead of
hand-rolling the docs:

- **`design-doc-new <title/project>`** — a technical design doc / RFC in the parent project's
  `docs/` (`03-projects/{slug}/docs/design-doc.md`). The engineering **how** behind a piece of
  work: context, proposed design, detailed interfaces, alternatives, cross-cutting concerns
  (security/privacy, performance, observability, testing), and rollout. Distinct from a PRD
  (the product **what/why**) and heavier than an ADR — decisions it resolves get recorded as
  ADRs via **`decision`**, linked back with `projects:`.
- **`brag-log [accomplishment]`** — appends to your evergreen **impact log**
  (`10-reports/brag-log.md`): what you shipped, the measurable impact, and the evidence, tagged
  by review dimension. Run it with an accomplishment to log one, or with no args to harvest
  recent wins from your weeklies, projects, decisions, and incidents. It's the raw material
  `perf-review` and `manager-report` read first, so self-reviews and snippets stop being a
  scramble.

Design docs live **inside** the project folder (browsable there); the brag log is a single
evergreen doc that accumulates across cycles.
