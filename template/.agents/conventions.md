# emOS Conventions

This file is the single source of truth for naming, tagging, and status vocabularies. Both humans and the agent follow these rules.

## File Naming

| Content Type       | Pattern                          | Example                              |
|--------------------|----------------------------------|--------------------------------------|
| Weekly             | `YYYY-Www.md`                    | `2026-W13.md`                        |
| One-on-one         | `YYYY-MM-DD.md` in person subdir | `one-on-ones/alex/2026-03-28.md`     |
| Person profile     | `{slug}.md`                      | `profiles/alex.md`                   |
| Project            | `{slug}/` folder + `{slug}.md` hub | `03-projects/incident-prevention/incident-prevention.md` |
| Project-local docs | `{slug}/docs/{name}.md`          | `incident-prevention/docs/rollout-plan.md` |
| Decision           | `{NNNN}-{slug}.md`               | `0001-observability-first.md`        |
| Incident           | `YYYY-MM-DD-{slug}.md`           | `2026-02-24-checkout-outage.md`      |
| Interview          | `{firstname}-{lastname}.md`      | `jane-doe.md`                        |
| OKR                | `YYYY-QN.md`                     | `2026-Q1.md`                         |
| Meeting            | `YYYY-MM-DD-{slug}.md`           | `2026-05-14-planning-sync.md`        |
| Performance review | `{person-slug}.md` in cycle dir  | `reviews/2024-EOY/alex.md`           |

**Slug rules**: lowercase, words separated by hyphens, no spaces, no special characters.

## Person References

- **In prose**: `@FirstName` (e.g., `@Alex`, `@Sam`)
- **In YAML frontmatter**: lowercase slug matching profile filename (e.g., `alex`, `sam`)
- **Mapping**: Defined in `.agents/config.yaml` under `people:`

## Tag Taxonomy

| Tag          | Meaning                                        |
|--------------|------------------------------------------------|
| `#delegate`  | Task delegated to someone else                 |
| `#blocked`   | Task is blocked by a dependency                |
| `#follow-up` | Needs follow-up in a future session            |
| `#feedback`  | Feedback to give or received                   |
| `#win`       | Notable positive outcome (useful for reviews)  |
| `#risk`      | Identified risk requiring attention            |
| `#decision`  | Implies or references a decision record        |
| `#project/{slug}` | Links a prose line or TODO to a project (used where frontmatter isn't available, e.g. weekly checkboxes) |

## Status Vocabularies

Each `type:` has a specific set of valid `status:` values.

| Type               | Valid statuses                                                |
|--------------------|--------------------------------------------------------------|
| weekly             | `active` · `completed` · `skipped`                           |
| project            | `proposed` · `active` · `paused` · `completed` · `cancelled` |
| incident           | `detected` · `mitigating` · `resolved` · `reviewed`          |
| hiring-position    | `draft` · `open` · `interviewing` · `offer` · `filled` · `cancelled` |
| candidate          | `screening` · `interviewing` · `offer` · `hired` · `rejected` · `withdrawn` |
| performance-review | `draft` · `submitted` · `discussed` · `finalized`            |
| okr                | `planning` · `active` · `reviewing` · `closed`               |
| decision           | `proposed` · `accepted` · `superseded` · `deprecated`        |
| person             | `active` · `on-leave` · `departing` · `departed`             |

## Priority Levels

Used in project and incident frontmatter:

| Level | Meaning                                      |
|-------|----------------------------------------------|
| `P0`  | Drop everything — active incident / blocker  |
| `P1`  | This quarter's top priority                  |
| `P2`  | Important but not urgent                     |
| `P3`  | Nice to have / backlog                       |

## YAML Frontmatter

Every file **must** have a `type:` field. Every file **should** have a `status:` field. Dates use ISO 8601 (`YYYY-MM-DD`). Lists use YAML arrays. Person references use slugs.

## Agent File Operations

The agent follows three operation patterns:

1. **Create**: Read template from `_templates/`, fill frontmatter, write to correct directory
2. **Update frontmatter**: Change status, update dates, add tags
3. **Append log entry**: Add dated heading to append-only sections (e.g., `## Current Status`, `## Key Observations`). Never delete or modify existing log entries.

## Cross-References

- Link to other emOS files using relative paths: `[Alex's profile](../02-people/profiles/alex.md)`
- Link to external systems using full URLs with ticket/doc IDs visible in link text (base URLs from `.agents/config.yaml` → `external:`)
- Example: `[PROJ-1434](https://your-org.atlassian.net/browse/PROJ-1434)`

## Project Links (the `projects:` join key)

emOS is filed by *type* (meetings, decisions, people…) but work is organized by *project*. The `projects:` frontmatter field is the connective tissue that lets any file be traced back to the projects it belongs to — without moving it out of its home folder.

- **Any file may carry `projects: [slug, ...]`** in its frontmatter, where each `slug` is a project folder name under `03-projects/`. It is an **array** — one meeting, decision, or report can belong to several projects.
- **In prose and weekly TODOs** (which have no frontmatter), use the `#project/{slug}` tag on the line instead.
- **The slug is the single stable key.** Never rename a project folder without updating the references (or run `project-sync` afterward to detect breakage).
- **The project hub doc does not link to itself** — it aggregates the reverse direction (see below).

### Hub rollup blocks

Each project's hub doc (`03-projects/{slug}/{slug}.md`) has a generated **rollup** section fenced by HTML markers:

```
<!-- rollup:start — generated by project-sync, do not hand-edit -->
## Related
### Meetings
...
<!-- rollup:end -->
```

Everything **between** the markers is regenerated by the `project-sync` skill (scanning the vault for `projects: {slug}` and `#project/{slug}`). Everything **outside** the markers is human-authored and never touched. When adding a project link to a file, you do not edit the hub by hand — it surfaces on the next `project-sync`.

**Bidirectional rule:** intake and create skills (`meeting-new`, `inbox`, `confluence-load`, `slack-capture`, `decision`, `incident`, etc.) set `projects:` on the item they create. The hub picks it up via sync. This keeps forward links (item → project) and the hub rollup (project → items) consistent by construction.

## Integrations (external tools)

External tools are chosen by **capability**, not hardcoded. `.agents/config.yaml` → `tools:` maps each capability (`issue_tracker`, `wiki`, `chat`, `docs`) to a provider; each provider has an adapter in `.agents/integrations/{provider}.md` that names the skill(s) implementing it. Workflows resolve capability → provider → adapter → skill, so they use whatever you've configured. New tools ship as new product-named skills + a new adapter — never by renaming or editing existing ones. See [docs/integrations.md](../docs/integrations.md) and [.agents/integrations/README.md](integrations/README.md).
