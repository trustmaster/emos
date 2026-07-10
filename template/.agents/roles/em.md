# Engineering Manager role pack

**Role key:** `em`  ← value for `config.yaml` → `owner.role`
**Status:** `shipped`

## Who this is for

Engineering managers who lead a team of direct reports. This is the default pack — it
reproduces emOS's classic behavior, so existing vaults that never set `owner.role` behave
exactly as before.

## Vocabulary

| Token | Value for this role |
|-------|---------------------|
| `{{role_report_slug}}` | `manager-async` |
| `{{role_report_title}}` | `Weekly Async Report - {{team}}` (or `report.async_title` if set) |
| `{{review_dimensions}}` | `Delivery, Technical, People, Communication, Growth` |
| `{{oneonone_default_relation}}` | `report` |
| `{{status_report_audience}}` | `your manager (upward status)` |

## People & relationships

`people:` are primarily your **direct reports**, plus close collaborators and your own
manager. Default `relation: report`. You coach reports (skill/will, growth areas), manage up
to your manager, and align laterally with peers.

## Sections in focus / dormant

In focus: `01-weekly`, `02-people` (profiles, one-on-ones, reviews), `03-projects`,
`05-incidents`, `06-hiring`, `10-reports`. All dashboards apply. This is the full taxonomy.

## Skill notes

- **1on1** — downward coaching prep: skill/will, growth, delegation, blockers to unblock.
- **perf-review** — you review your reports (subject ≠ owner); gather evidence, never invent
  ratings; competency notes use the dimensions above (the "People" dimension covers how they
  work with/through others).
- **manager-report** — weekly async to your manager: team sentiment, delivery, escalations.
- **morning / weekly-review** — surface this week's scheduled 1-on-1s and their carry-over.
