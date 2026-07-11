---
type: design-doc
title: "System / Feature Name"
slug: "feature-name"
status: draft            # draft · review · accepted · implemented · superseded
owner: "{{owner_slug}}"
projects: "parent-project-slug"   # parent project (for humans; lives in that project's docs/)
reviewers: []            # slugs of people reviewing this design
jira_epic: null          # e.g. PROJ-1234
target_date: null
supersedes: null         # path to a design doc this replaces, if any
tags: []
---

## Summary

One paragraph: what we're building and the gist of the approach. Write this last, read it
first. This doc is the engineering **how** — if the **what/why** lives in a PRD, link it and
don't repeat it.

## Context & problem

Background, the current state, and the problem this design solves. What's forcing the change
now (scale, incidents, a new requirement). Enough for a reviewer who wasn't in the room.

## Goals & non-goals

**Goals**

- Technical outcomes this design must achieve.

**Non-goals**

- Explicitly out of scope for this design, so reviewers don't assume it.

## Proposed design

The core of the doc. The architecture and how the pieces fit — components, data flow, and the
key choices that define the approach. Add a diagram (ASCII or a linked image) where it's faster
than prose.

## Detailed design

The specifics an implementer needs:

- **Data model / schema** — new or changed entities, fields, indexes, migrations.
- **APIs / interfaces** — endpoints, signatures, message formats, contracts.
- **Key flows** — the important paths step by step, including failure and retry handling.

## Alternatives considered

### Alternative 1 — {name}

What it is and why it was not chosen.

### Alternative 2 — {name}

What it is and why it was not chosen.

## Cross-cutting concerns

- **Security & privacy** — data handled, access control, and any PII / compliance impact.
- **Performance & scale** — expected load, hotspots, and known limits.
- **Observability** — metrics, logs, and alerts to add.
- **Testing** — how correctness is verified before and after rollout.

## Rollout & migration

Phasing (behind a flag → gradual → default on), data backfills/migrations, dependencies, and
the fallback if it goes wrong.

## Risks & open questions

- [ ] Risk or question to resolve before or during the build.

## Appendix

Links to the PRD (`docs/prd.md`), decisions this design produces (record each as an ADR via
`/decision`, linked with `projects:`), and external references.
