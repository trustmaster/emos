# emOS role packs

This directory holds **role packs** — the seam that lets one emOS framework serve
engineering managers, individual contributors, product managers, and directors without
forking any skill.

## How it fits together

```
config.yaml → owner.role          (which role?)
                    │
                    ▼
       .agents/roles/{role}.md      (this dir: the vocabulary + emphasis for that role)
                    │  supplies tokens + guidance
                    ▼
       role-sensitive skill         (1on1, perf-review, manager-report, morning,
                                      weekly-review, configure, rebuild)
```

A role-sensitive skill never hardcodes manager/report/team language. It reads
`config.owner.role`, opens that role's pack here, and resolves the pack's **vocabulary
tokens** and follows its **skill notes**. This mirrors how workflows resolve a tool
capability → provider → adapter (see [../integrations/README.md](../integrations/README.md)).

The **folder taxonomy is identical for every role** — packs change vocabulary, review
dimensions, report format, the default 1-on-1 relationship, and which sections a role leans
on. They never move or rename folders.

## What a pack declares

Every pack fills the same four blocks (see [`_pack-template.md`](_pack-template.md)):

1. **Vocabulary** — the role tokens skills substitute at creation time:

   | Token | Meaning |
   |-------|---------|
   | `{{role_report_slug}}` | filename suffix for the weekly status report (`10-reports/YYYY-Www-{slug}.md`) |
   | `{{role_report_title}}` | H1 title of that report |
   | `{{review_dimensions}}` | comma-separated competency dimensions for `perf-review` |
   | `{{oneonone_default_relation}}` | relationship assumed for a 1-on-1 when the person's profile has no `relation:` |
   | `{{status_report_audience}}` | who the status report is written for |

2. **People & relationships** — what "people" means for this role and the default `relation:`.
3. **Sections in focus / dormant** — which numbered folders + dashboards this role uses often
   vs. rarely (guidance for surfacing; the folders still exist for every role).
4. **Skill notes** — role-specific guidance for the role-sensitive skills.

## Shipped packs

| Role key | For | Report | 1-on-1 default |
|----------|-----|--------|----------------|
| [`em`](em.md) | Engineering manager (default) | `manager-async` | report (downward) |
| [`ic`](ic.md) | Individual contributor / senior+ | `snippets` | manager (upward) |
| [`pm`](pm.md) | Product manager | `launch-status` | stakeholder (lateral) |
| [`director`](director.md) | Director / senior leader | `portfolio` | manager / skip |

## Adding a custom role pack

You never edit the core skills. In short:

1. Copy [`_pack-template.md`](_pack-template.md) → `{role}.md` and fill the four blocks.
2. Set `owner.role: {role}` in `config.yaml` (or run `/configure`).

Full walkthrough: [../../docs/roles.md](../../docs/roles.md). Shipped packs are
framework-owned (updated by `emos update`); a pack you add yourself is yours and is never
overwritten.
