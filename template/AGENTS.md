# emOS Agent Guide

You are operating inside **emOS** — *Everyone's Markdown Organizer System* (engineering
managers still feel right at home). One vault, many roles: `.agents/config.yaml` →
`owner.role` (`em` · `ic` · `pm` · `director`) selects a role pack that tunes vocabulary and
emphasis — see the **Roles** section below.

Read `.agents/config.yaml` first to orient yourself. It defines who the vault
belongs to (`owner:`), the team/org context (`context:`), the people map
(`people:`), directory paths (`paths:`), external system URLs (`external:`),
the active tool per capability (`tools:`), and provider settings
(`jira:`, `confluence:`, `slack:`, `report:`).

If a `CONFIG.md` file exists at the vault root, read it too — it's free-form
personal context from the owner (current focus, working style) that
complements the structured fields in `config.yaml`. (`CONFIG.md` is prose;
`.agents/config.yaml` is the structured settings — two different files.)

This vault is a pure Markdown knowledge system. There is no code, no build system, no test suite. Your job is to read, create, and update `.md` files according to the conventions below.

---

## Orientation

```
00-inbox/         Quick capture — unsorted items
01-weekly/        Weekly planning files (YYYY-Www.md) + _index.md dashboard
02-people/        profiles/, one-on-ones/, reviews/ + _index.md dashboard
03-projects/      {slug}/ project folders (flat) + archive/ + _index.md dashboard
04-decisions/     ADRs (NNNN-slug.md) + _index.md dashboard
05-incidents/     Post-mortems (YYYY-MM-DD-slug.md) + _index.md dashboard
06-hiring/        positions/, interviews/, rubrics/ + _index.md dashboard
07-strategy/      okrs/, roadmaps/ + _index.md dashboard
08-meetings/      Ad-hoc meeting notes (YYYY-MM-DD-slug.md)
09-knowledge/     management/, coaching/, tech/ reference docs
10-reports/       Recurring reports
_templates/       Source templates for all file types
_attic/           Archived/optional material excluded from the active framework
docs/             Human-facing guides (adding tools, authoring skills)
.agents/          config.yaml (owner, people map, paths, org context), conventions.md,
                  skills/, integrations/ (provider adapters), commands/,
                  settings.local.json (personal, not framework-managed)
.claude/          symlink -> .agents/, so Claude Code discovers skills/commands unchanged
.emos/            framework update tooling (manifest, emos.mjs) — see README.md
CONFIG.md         optional personal intro from the owner, prose (not framework-managed)
```

**Key rule**: `_index.md` files are **generated views** — never edit them by hand. Always regenerate after content changes.

---

## Roles

emOS serves engineering managers, ICs, product managers, and directors from one framework.
`.agents/config.yaml` → `owner.role` (`em` · `ic` · `pm` · `director`, default `em`) selects
a **role pack** at `.agents/roles/{role}.md`.

When running a **role-sensitive skill** (`1on1`, `perf-review`, `manager-report`, `morning`,
`weekly-review`, `configure`, `rebuild`):

1. Read `config.owner.role` (default `em` if absent).
2. Open the pack at `.agents/roles/{role}.md`.
3. Resolve the pack's **vocabulary tokens** (see the Config Substitution table) and follow
   its **skill notes** for framing, review dimensions, report format, and the default 1-on-1
   relationship.

The **folder taxonomy is the same for every role** — packs change vocabulary and emphasis,
never folder locations. A person's `relation:` (`report` · `manager` · `peer` · `stakeholder`
· `skip`, from their profile) refines framing per person; absent ⇒ the pack's
`{{oneonone_default_relation}}`. Full guide: [docs/roles.md](docs/roles.md).

---

## Person Reference Resolution

Resolve `@Mentions` using `.agents/config.yaml` → `people:` map. Each entry maps
`@FirstName` to a lowercase slug; the profile lives at
`02-people/profiles/{slug}.md`. If a mention isn't in the map, ask before
creating a new profile.

---

## Config Substitution

Templates and skills use `{{token}}` placeholders that you resolve from
`.agents/config.yaml` at creation time. Never write a literal token into a file.

| Token | Source |
|-------|--------|
| `{{owner_slug}}` | `owner.slug` |
| `{{owner_name}}` | `owner.name` |
| `{{team}}` | `context.team` |
| `{{report_async_title}}` | `report.async_title`, or `{{role_report_title}}` if blank |
| `{{jira_browse_url}}` | `external.jira` |

Role tokens are resolved from the active role pack (`.agents/roles/{owner.role}.md`, default
`em`) — see the **Roles** section:

| Token | Source (active role pack) |
|-------|---------------------------|
| `{{role_report_slug}}` | report filename suffix, e.g. `manager-async` (em), `snippets` (ic) |
| `{{role_report_title}}` | status-report H1 title |
| `{{review_dimensions}}` | competency dimensions for `perf-review` |
| `{{oneonone_default_relation}}` | default `relation:` when a person's profile has none |
| `{{status_report_audience}}` | who the status report addresses |

---

## File Creation Rules

1. **Read the template first** — always copy from `_templates/` as the starting point.
2. **Fill all frontmatter fields** — never leave `null` unless the template says it's optional. Resolve `{{tokens}}` from config.
3. **Dates**: ISO 8601 (`YYYY-MM-DD`). Weeks: `YYYY-Www`. Slugs: lowercase, hyphen-separated.
4. **Person references**: slugs in YAML frontmatter, `@FirstName` in prose.
5. **Write to the correct directory** — see directory map above and `.agents/config.yaml` → `paths:`.

### Content type → correct path

| type: | Directory |
|-------|-----------|
| `weekly` | `01-weekly/YYYY-Www.md` |
| `one-on-one` | `02-people/one-on-ones/{slug}/YYYY-MM-DD.md` |
| `person` | `02-people/profiles/{slug}.md` |
| `project` | `03-projects/{slug}/` |
| `decision` | `04-decisions/{NNNN}-{slug}.md` |
| `incident` | `05-incidents/YYYY-MM-DD-{slug}.md` |
| `hiring-position` | `06-hiring/positions/{slug}.md` |
| `candidate` | `06-hiring/interviews/{firstname}-{lastname}.md` |
| `performance-review` | `02-people/reviews/{cycle}/{slug}.md` |
| `okr` | `07-strategy/okrs/YYYY-QN.md` |
| `meeting` | `08-meetings/YYYY-MM-DD-{slug}.md` |

---

## Update Rules (append-only)

- **Never delete or overwrite existing log entries** in sections like `## Current Status`, `## Key Observations`, `## 1-on-1 Log`.
- **Prepend** new dated entries at the top of append-only sections with `### YYYY-MM-DD`.
- **Frontmatter fields** (`status:`, `updated:`, tags) may be updated in place.

---

## Tag Taxonomy

`#delegate` `#blocked` `#follow-up` `#feedback` `#win` `#risk` `#decision`

Use tags inline in prose. Surface `#follow-up` and `#blocked` items when preparing briefings.

---

## Status Vocabularies

| Type | Valid values |
|------|-------------|
| weekly | `active` · `completed` · `skipped` |
| project | `proposed` · `active` · `paused` · `completed` · `cancelled` |
| incident | `detected` · `mitigating` · `resolved` · `reviewed` |
| hiring-position | `draft` · `open` · `interviewing` · `offer` · `filled` · `cancelled` |
| candidate | `screening` · `interviewing` · `offer` · `hired` · `rejected` · `withdrawn` |
| performance-review | `draft` · `submitted` · `discussed` · `finalized` |
| okr | `planning` · `active` · `reviewing` · `closed` |
| decision | `proposed` · `accepted` · `superseded` · `deprecated` |
| person | `active` · `on-leave` · `departing` · `departed` |

---

## Priority Levels

| Level | Meaning |
|-------|---------|
| P0 | Drop everything — active incident or blocker |
| P1 | This quarter's top priority |
| P2 | Important but not urgent |
| P3 | Nice to have / backlog |

---

## Dashboard Rebuild

After creating or updating content files, regenerate the relevant dashboard. The dashboard files are listed in `.agents/config.yaml` → `agent.dashboards`:

```
01-weekly/_index.md
02-people/_index.md
03-projects/_index.md
04-decisions/_index.md
05-incidents/_index.md
06-hiring/_index.md
07-strategy/_index.md
```

Each `_index.md` is a **summary view** generated by scanning the content files in that section. Include: file title/name, `status:`, `priority:` (if applicable), key dates, and any `#blocked` or `#follow-up` tags.

---

## Integrations (tools & capabilities)

emOS talks to external tools through **capabilities**, not hardcoded products.
Four capabilities exist — `issue_tracker`, `wiki`, `chat`, `docs` — and
`.agents/config.yaml` → `tools:` declares which provider fills each one:

```yaml
tools:
  issue_tracker: jira        # jira | none
  wiki:          confluence   # confluence | none
  chat:          slack        # slack | none
  docs:          gws          # gws | none
```

**When a workflow needs a capability**, resolve it like this:

1. Read `config.tools.{capability}`. If it's `none`, tell the user that
   capability isn't configured and stop (don't guess a tool).
2. Open the provider's adapter at `.agents/integrations/{provider}.md`. It lists
   the provider's prerequisites, the config block it reads, and which **skill**
   implements each operation.
3. Follow the adapter — usually by invoking the named provider skill (e.g.
   `create-jira-ticket`), which reads its own `{provider}:` config block.

**Provider skills are product-named on purpose** (`create-jira-ticket`,
`confluence-load`, `slack-capture`, `gws-*`). To add a tool (Linear, Notion,
Mattermost, MS Office…), you write a *new* skill and adapter and flip the
`tools` key — you never rename or overwrite the existing ones, and you never edit
the core workflows. Full walkthrough: [docs/integrations.md](docs/integrations.md).

Shipped adapters live in `.agents/integrations/` (see its `README.md` for the
per-capability operation contracts).

---

## External Systems (links only, no credentials)

Base URLs live in `.agents/config.yaml` → `external:` (jira, confluence, slack,
github, tableau, opsgenie, gdrive) — each keyed by provider. Always format
external links as `[TICKET-ID](full-url)` so the identifier is visible in plain
text. Provider-specific auth/setup notes live in that provider's adapter under
`.agents/integrations/` (e.g. the `gws` token-refresh step is in `gws.md`).

---

## Available Slash Commands

Skills live in `.agents/skills/` (discoverable by Claude Code via the
`.claude -> .agents` symlink). Slash commands, if defined, live in
`.agents/commands/`.

| Command | Description |
|---------|-------------|
| `/configure` | Interactive setup/edit of your config (owner, people, tools) — no hand-editing YAML |
| `/morning` | Morning briefing — what's on the plate today |
| `/1on1 <person>` | Prep a 1-on-1 session with a team member |
| `/weekly-new` | Create the current week's planning file |
| `/weekly-review` | Review current week, prep next week's file |
| `/incident <description>` | Start a new incident post-mortem |
| `/decision <title>` | Create a new Architecture Decision Record |
| `/project-new <title>` | Create a new project tracker |
| `/project <slug>` | Load a project's full context into the session |
| `/project-sync [slug]` | Regenerate project hub rollups from linked content |
| `/meeting-new <title>` | Create a meeting note, optionally linked to a project |
| `/capture <text>` | Quick capture to 00-inbox |
| `/perf-review <person>` | Prepare evidence and narrative for a performance review |
| `/inbox` | Process the next inbox item — classify, extract actions, prompt resolution |
| `/inbox <filename>` | Process a specific inbox item by name |
| `/rebuild` | Regenerate all _index.md dashboards |
| `/emos-update` | Check for and apply emOS framework updates |

Provider skills (active based on `config.tools`): `/create-jira-ticket`,
`/jira-sync`, `/confluence-load`, `/confluence-save`, `/slack-capture`, and the
`/gws-*` family — see `.agents/integrations/`.
