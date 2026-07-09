---
name: project-sync
description: Regenerate the auto-rollup block in a project's hub doc (or every project) by scanning the vault for files linked via `projects:` frontmatter or `#project/{slug}` tags. Use when the user wants a project's Related section refreshed, or after tagging content. Optionally pass a project slug as args; no args = sync all active projects.
---

Regenerate the `<!-- rollup:start -->…<!-- rollup:end -->` block(s) in project hub docs.

Read `paths.projects` from `.agents/config.yaml` (default `03-projects`).

## Step 1 — Determine scope

- If args is a project slug (or a name that resolves to one folder in `{paths.projects}/`), sync only that project.
- Otherwise, sync every subfolder of `{paths.projects}/` **except** `archive/`.

## Step 2 — For each project {slug}

**a. Read the hub doc** `{paths.projects}/{slug}/{slug}.md`. Note `owner` and `team_members` from frontmatter. If the file has no `<!-- rollup:start -->` / `<!-- rollup:end -->` markers, append a fresh block (using the structure in `_templates/project-tracker.md`) at the end of the file.

**b. Find linked files.** Scan every `.md` in the vault — excluding `_templates/`, `_attic/`, hidden dirs, and the project's own hub doc — for either:
   - frontmatter `projects:` array containing `{slug}`, **or**
   - a `#project/{slug}` tag anywhere in the body.

**c. Group each match** by its `type:` frontmatter, falling back to its top-level folder:

| Match | Rollup section |
|-------|----------------|
| `type: meeting` / `08-meetings/` | Meetings |
| `type: decision` / `04-decisions/` | Decisions |
| `type: incident` / `05-incidents/` | Incidents |
| `type: okr`/`roadmap` / `07-strategy/` | Strategy |
| `09-knowledge/` | Knowledge |
| `10-reports/` | Reports |

**d. People.** Union of: hub `owner` + `team_members`, plus any person slugs appearing in matched items' `attendees` / `deciders` / `participants`. Resolve `@Mentions` via `.agents/config.yaml` → `people:`. Link each to `02-people/profiles/{slug}.md` **only if that file exists** — the vault owner (`config.yaml` → `owner.slug`) has no self-profile, so render them in bold without a link, e.g. `- **@Name** — owner (vault owner)`.

**e. Open TODOs.** Collect unchecked `- [ ]` lines that are either tagged `#project/{slug}` (anywhere, especially `01-weekly/`) or found inside a file linked to this project. Keep the source file reference.

## Step 3 — Rewrite only the rollup block

Replace everything **between** the markers (never the markers themselves, never a byte outside them). Format each entry as a relative link with a one-line context suffix:

```markdown
### Meetings
- [2026-05-14 Planning sync](../../08-meetings/2026-05-14-planning-sync.md) — 2026-05-14
### Decisions
- [ADR-0007 Batch adapter](../../04-decisions/0007-batch-adapter.md) — accepted · 2026-05-02
### People
- [Alex](../../02-people/profiles/alex.md) — owner
### Open TODOs
- [ ] Request provisioned capacity from Google — `01-weekly/2026-W20.md`
```

Leave a section header with `*(none)*` under it when empty. Preserve all human-authored content outside the block byte-for-byte.

## Step 4 — Report

Per project synced: the counts per section (e.g. `gcp-cost-optimization: 3 meetings, 1 decision, 2 reports, 4 open TODOs`). Flag any `#project/{slug}` reference whose target project folder does not exist (a rotted link).
