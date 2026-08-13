---
name: team-sync
description: Regenerate the auto-rollup block in a team hub doc (or every team) and in the portfolio hub, by scanning the vault for files linked via `teams:` frontmatter or `#team/{slug}` tags. For directors and other leaders of managers. Use when the user wants a team's or the portfolio's Related section refreshed, or after tagging content to a team. Optionally pass a team slug as args; no args = sync every team plus the portfolio.
roles: [director]
---

Regenerate the `<!-- rollup:start -->…<!-- rollup:end -->` block(s) in team hub docs
and in the portfolio hub. This is the org-level counterpart of `project-sync`, and it
is the **only** skill that writes team rollups — `project-sync` never touches them,
and this skill never touches a project hub's block.

Read `paths.teams` (default `02-people/teams`), `paths.projects` (default
`03-projects`), and `paths.profiles` (default `02-people/profiles`) from
`.agents/config.yaml`.

If `{paths.teams}/` doesn't exist or holds no team files, say so and stop — there is
nothing to sync, and this is not an error. Suggest `/team-new`.

## Step 1 — Determine scope

- If args is a team slug (or a name that resolves to one file in `{paths.teams}/`),
  sync only that team.
- Otherwise, sync every `{paths.teams}/*.md`, then the portfolio hub.

## Step 2 — For each team {slug}

**a. Read the hub doc** `{paths.teams}/{slug}.md`. Note `manager`, `projects`, and
`status`. If the file has no `<!-- rollup:start -->` / `<!-- rollup:end -->` markers,
append a fresh block (using the structure in `_templates/team-profile.md`) at the end
of the file.

**b. Find linked files.** Scan every `.md` in the vault — excluding `_templates/`,
`_attic/`, hidden dirs, and the team's own hub doc — for either:
   - frontmatter `teams:` array containing `{slug}`, **or**
   - a `#team/{slug}` tag anywhere in the body.

**c. Group each match** by its `type:` frontmatter, falling back to its top-level folder:

| Match | Rollup section |
|-------|----------------|
| `type: person` / `{paths.profiles}/` | People |
| `type: project` / `03-projects/` | Projects |
| `type: incident` / `05-incidents/` | Incidents |
| `type: meeting` / `08-meetings/` | Meetings |
| `type: decision` / `04-decisions/` | Decisions |
| `type: okr`/`roadmap`/`portfolio` / `07-strategy/` | Strategy |
| `type: hiring-position`/`candidate`/`headcount` / `06-hiring/` | Hiring |
| `10-reports/` | Reports |

**d. People.** Union of: the hub's `manager`, plus every profile carrying
`teams: [{slug}]`, plus person slugs appearing in matched items' `owner` /
`team_members` / `attendees`. Resolve `@Mentions` via `.agents/config.yaml` →
`people:`. Link each to `{paths.profiles}/{slug}.md` **only if that file exists** —
the vault owner (`config.yaml` → `owner.slug`) has no self-profile, so render them in
bold without a link. Mark the manager, e.g. `— manager`.

**e. Projects.** Union of the hub's `projects:` list and every project hub carrying
`teams: [{slug}]`. Show `status` and `priority` after each.

**f. Open TODOs.** Collect unchecked `- [ ]` lines that are either tagged
`#team/{slug}` (anywhere, especially `01-weekly/`) or found inside a file linked to
this team. Keep the source file reference.

## Step 3 — Rewrite only the rollup block

Replace everything **between** the markers (never the markers themselves, never a byte
outside them). Format each entry as a relative link with a one-line context suffix:

```markdown
### People
- [Priya](../profiles/priya.md) — manager
- [Sam](../profiles/sam.md) — IC3
### Projects
- [Checkout resilience](../../03-projects/checkout-resilience/checkout-resilience.md) — active · P1
### Incidents
- [2026-02-24 Checkout outage](../../05-incidents/2026-02-24-checkout-outage.md) — sev2 · reviewed
### Open TODOs
- [ ] Confirm on-call rotation change — `01-weekly/2026-W20.md`
```

Leave a section header with `*(none)*` under it when empty. Preserve all
human-authored content outside the block byte-for-byte.

## Step 4 — Portfolio hub

Only when args was empty **and** `07-strategy/portfolio.md` exists (never create it
here — `/portfolio` does that). Rewrite its rollup block with one row per team:

```markdown
| Team | Manager | Status | Headcount | Active projects | Last health check |
|------|---------|--------|-----------|-----------------|-------------------|
| [Payments](../02-people/teams/payments.md) | @Priya | active | 6 (+1 open) | 3 | 2026-05-02 |
```

Flag in the table (not by editing prose) any team whose `last_health_check` is more
than a quarter old, or that has no manager set.

## Step 5 — Report

Per team synced: counts per section (e.g. `payments: 5 people, 3 projects, 2 incidents,
4 open TODOs`). Then flag:

- any `teams: [slug]` or `#team/{slug}` reference whose target hub doesn't exist (a
  rotted link) — name the referencing file;
- any team hub whose `manager:` slug has no profile;
- whether the portfolio hub was refreshed or is absent.
