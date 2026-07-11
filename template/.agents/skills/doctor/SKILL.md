---
name: doctor
description: Health-check the vault for integrity problems — missing or invalid frontmatter, bad status values, rotted project links, unmapped @mentions, misfiled files, broken cross-links, and stale dashboards or rollups. Read-only: it reports findings and suggests fixes but changes nothing on its own. Use when the user wants to lint, check, validate, audit, or health-check the vault, or asks "what's broken?". Optionally pass a folder path or a check name (frontmatter · projects · people · links · dashboards · naming) as args to narrow the scope.
---

Audit the vault for integrity problems and report them. **This skill is
read-only** — it never creates, moves, deletes, or edits files. Its output is the
findings list plus suggested remediation. Only act on a fix after the user
explicitly asks.

## Step 0 — Load context

1. Read `.agents/config.yaml`: `paths:`, `people:`, `owner.slug`, `tools:`, and
   `agent.dashboards`.
2. Read `.agents/conventions.md` — source of truth for **File Naming**, the
   **Status Vocabularies** table, and the **Tag Taxonomy** — and `AGENTS.md` for
   the **Content type → correct path** mapping. Validate against those tables; do
   not hardcode a copy here.
3. **Scope** from args:
   - empty → scan the whole vault, run every check;
   - a folder (e.g. `03-projects`, `02-people`, or a `paths:` key) → limit scanning
     to that area;
   - a check name (`frontmatter` · `projects` · `people` · `links` · `dashboards` ·
     `naming`) → run only that check.

Throughout, **exclude** from scanning: `_templates/**`, `_attic/**`, the
top-level `docs/` guides only (`/docs/**` — *not* project-local `*/docs/`, which
is a freeform zone handled below), `.agents/**`, `.emos/**`, `.claude/**`,
`.git/**`, any hidden dir, all `_index.md` files, and top-level `README.md` /
`CONFIG.md`.

**Freeform zones — no frontmatter contract.** Two areas hold intentionally
unstructured files; do **not** run the frontmatter/naming checks (A, B) on them:
- `{paths.inbox}/` (default `00-inbox/`) — quick-capture notes, pre-classification.
- project-local `docs/` folders, `{paths.projects}/*/docs/**` — working docs and
  drafts.

These are still read by the link checks: a `#project/{slug}` tag or relative link
inside a freeform file is validated normally (C, E). Non-`.md` files anywhere are
skipped by content checks but counted in the scan total.

## The checks

Each finding carries a **severity**: `ERROR` (breaks a convention or a link),
`WARN` (probably wrong / will confuse a rollup), or `INFO` (worth a glance).

### A. Frontmatter contract — ERROR / WARN
For every content `.md` in scope:
- **Missing `type:`** → ERROR. Every file must declare a `type:`.
- **`type:` not a known content type** (weekly · one-on-one · person · project ·
  decision · incident · hiring-position · candidate · interview ·
  performance-review · okr · roadmap · meeting · knowledge, plus the import types
  `confluence-import` · `slack-capture`) → WARN. **Reports are role-variant**: any file under
  `{paths.reports}/` (default `10-reports/`) is a report — its `type:` is the
  active role's report slug (`manager-async`, `snippets`, `product-status`,
  `program-update`, …), so accept whatever token it carries and never warn on it.
- **Missing `status:`** on a type that has a Status Vocabulary → WARN.
- **`status:` value not in that type's vocabulary** → ERROR.
- **Malformed dates** — any `date`/`started`/`updated`/`imported`/etc. field that
  isn't ISO 8601 `YYYY-MM-DD` (or `YYYY-Www` for weeks) → WARN.

### B. Naming & placement — WARN
- **Filename doesn't match the pattern** for its `type:` (see conventions →
  File Naming; e.g. weekly `YYYY-Www.md`, incident `YYYY-MM-DD-{slug}.md`,
  decision `NNNN-{slug}.md`) → WARN.
- **File is in the wrong folder** for its `type:` (see AGENTS.md → Content type →
  correct path) → WARN (misfiled).
- **Slug not kebab-case** (uppercase, spaces, or underscores in a slug) → WARN.
- **Import types are staged, not misfiled.** A file with `type: confluence-import`
  or `type: slack-capture` keeps its import filename (`confluence-…` / `slack-…`)
  and may sit in `00-inbox/` **or** in a destination type folder while it awaits
  reclassification — skip the naming-pattern and folder-placement checks for it
  (check A and the link checks still apply). Only once a human retypes it to a
  native type (e.g. `decision`) does that type's naming/placement rule kick in —
  at which point a lingering `YYYY-MM-DD-{slug}` name on a `decision` correctly
  becomes a WARN to rename it `NNNN-{slug}`.

### C. Project link integrity — ERROR / WARN
Read `paths.projects` (default `03-projects`).
- **Rotted link** — any `projects: [slug]` entry or `#project/{slug}` tag whose
  target folder `{paths.projects}/{slug}/` does not exist → ERROR. Report the
  referencing file and the missing slug.
- **Missing hub doc** — a project folder (excluding `archive/`) with no
  `{slug}/{slug}.md` → ERROR.
- **Missing rollup markers** — a hub doc lacking the
  `<!-- rollup:start -->` / `<!-- rollup:end -->` pair → WARN (`/project-sync`
  will add it).
- **Duplicate slug** — the same project slug under both the active tree and
  `archive/`, or two folders resolving to one slug → ERROR.

### D. Person references — WARN
- **Unmapped mention** — an `@FirstName` in prose that has no entry in the
  `people:` map → WARN. (Skip code fences and links.) **Exempt the owner's own
  first name** (derived from `owner.name`): the owner has no self-profile and is
  not in the map, so `@Alex` for owner "Alex Rivera" is expected, not a finding.
  (First-token heuristic — if the owner is mentioned by a form that differs from
  the first token of `owner.name`, e.g. an accent-stripped or shortened name,
  report it as `INFO` rather than `WARN` so a real typo still surfaces without
  crying wolf on the owner.)
- **Missing profile** — a person slug in frontmatter (`person`, `owner`,
  `team_members`, `attendees`, `deciders`, `participants`) with no
  `{paths.profiles}/{slug}.md`. **Exempt the vault owner** (`owner.slug`) — the
  owner has no self-profile by design → WARN for everyone else.
- **Dangling map entry** — a `people:` entry pointing to a profile file that
  doesn't exist → WARN.

### E. Cross-link integrity — WARN
- **Broken relative link** — a Markdown link `](relative/path.md…)` whose target
  file doesn't resolve from the linking file's location → WARN. Ignore
  `http(s)://`, `mailto:`, and pure `#anchor` links.

### F. Dashboard & rollup freshness — WARN / INFO
- For each path in `agent.dashboards`: if a content file in that folder is newer
  than the `_index.md` (mtime), or the `_index.md` is missing while the folder has
  content → WARN, recommend `/rebuild`.
- If a file links a project (`projects:` / `#project/{slug}`) but does **not**
  appear in that project hub's rollup block → INFO, recommend `/project-sync`.

### G. Sequence & staleness — INFO
- **Decision numbering** — duplicate `NNNN` prefixes, or gaps in the sequence, in
  `04-decisions/` → INFO.
- **Stale active weekly** — a weekly with `status: active` that isn't the current
  ISO week (compute it with `date +%G-W%V` — portable across macOS/BSD and
  GNU/Linux) → INFO.
- **Unreviewed incident** — an incident whose `status:` is not `reviewed` → INFO.

## Output

Group findings by severity, most severe first. For each finding give the file
(as a clickable relative path with a line number where one applies), a one-line
description, and the concrete fix. Example shape:

```
## 🔴 Errors (2)
- 03-projects/gcp-cost/gcp-cost.md — status `in-progress` is not valid for `project`
  (use: proposed · active · paused · completed · cancelled). Fix the frontmatter.
- 08-meetings/2026-05-14-planning-sync.md — `projects: [gcp-cost-optimzation]` has no
  matching folder (typo? closest: `gcp-cost-optimization`). Fix the slug.

## 🟡 Warnings (3)
- 02-people/one-on-ones/priya/2026-06-02.md — @Jordan is not in the people map. Add
  them via /configure or fix the mention.
- 01-weekly/_index.md is older than 01-weekly/2026-W24.md → run /rebuild.
...

## 🔵 Info (1)
- 05-incidents/2026-02-24-checkout-outage.md — status `resolved`, not yet `reviewed`.
```

End with:
1. A **one-line summary** — counts by severity and how many files were scanned.
2. A **remediation list** — the specific skills to run (`/rebuild`,
   `/project-sync`, `/configure`) and which findings each would clear. Findings
   that need a manual frontmatter/slug edit are called out as such.

Then stop. Do not fix anything unless the user asks; if they do, make the smallest
change that clears the finding and re-run the affected check to confirm.
