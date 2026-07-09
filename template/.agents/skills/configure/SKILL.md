---
name: configure
description: Interactively set up or update your emOS configuration — owner, team, people, which tools you use (issue tracker, wiki, chat, docs), and their coordinates. Use for first-time setup or to change settings later. Nobody should hand-edit YAML; run this instead. No args (or pass a section name like "tools" or "people" to jump straight to it).
---

Walk the user through configuring emOS. You edit `.agents/config.yaml` (and
optionally `CONFIG.md`) on their behalf so they never hand-edit YAML.

**Everything is optional.** This is a convenience, not a gate — the vault works
with the seeded defaults untouched. Tell the user up front they can skip any
question (they'll press Enter / say "skip") and fill it in later. Never block on a
missing answer; leave the seeded default in place and move on. Ask questions in
small batches, not one long interrogation.

Never ask for or store secrets (passwords, API tokens). emOS stores only links
and coordinates; authentication is handled by the MCP servers / CLIs themselves.

## Step 0 — Determine state

- If `.agents/config.yaml` does **not** exist, this is first-time setup: copy
  `.agents/config.example.yaml` to `.agents/config.yaml` as the starting point.
- If it exists, this is an edit: read current values and offer each as the
  default. If args names a section (`owner`, `context`, `people`, `tools`,
  `integrations`, `report`), jump straight to it.

## Step 1 — Identity & context (all optional)

Ask, offering current values as defaults:
- **Owner**: `name`. Derive `slug` automatically (lowercase, kebab-case) — don't
  ask for it separately.
- **Context**: `team`, `tribe` (dept/org unit), `company`.

Do **not** ask about the current quarter — it's derived from today's date.

## Step 2 — People (optional)

Ask for the user's direct reports / close collaborators as a **single
comma-separated list of names** — e.g. `Alex, Sam Rivera, Jordan`. Don't make the
user think about slugs or `@mentions`.

For each name, generate the mapping yourself:
- Key: `@FirstName` (first token of the name).
- Value: kebab-case slug of the full name (`Sam Rivera` → `sam-rivera`).
- If two names collide on `@FirstName`, disambiguate the later one with a last
  initial (`@SamR`).

Write these under `people:` in the config. Show the generated mapping so the user
can eyeball it. Skipping is fine — they can re-run this later as people join.

## Step 3 — Tools (capabilities, optional)

For each capability, ask which provider they use, or `none` (the safe default —
dependent skills degrade gracefully rather than fail):

| Capability | `tools` key | Shipped providers |
|------------|-------------|-------------------|
| Issue tracker | `issue_tracker` | `jira` · `none` |
| Wiki | `wiki` | `confluence` · `none` |
| Chat | `chat` | `slack` · `none` |
| Document suite | `docs` | `gws` · `none` |

If the user names a tool that isn't shipped (Linear, Notion, Mattermost, MS
Office, …), set the `tools` key to their chosen provider slug and point them to
`docs/integrations.md` to add the matching skill + adapter — do **not** invent an
adapter here.

## Step 4 — Provider coordinates (only for tools that aren't `none`)

For each active capability, prompt for that provider's config block. Read the
provider's adapter at `.agents/integrations/{provider}.md` to see exactly which
keys it needs and set only those. Any single field the user doesn't know can be
left blank. For the shipped providers:

- **jira** → `jira.project_key`, `jira.cloud_id`, `jira.custom_fields.*`; `external.jira` base URL.
- **confluence** → `confluence.cloud_id`, `confluence.space_key`, `confluence.root_page_id`, `confluence.root_title`, `confluence.parents.*`; `external.confluence`.
- **slack** → `slack.workspace_url`, `slack.channels.*`; `external.slack`.
- **gws** → `external.gdrive` (auth is via the `gws` CLI; no keys here).

After setting a provider, note its prerequisite from the adapter (e.g. "connect
the Atlassian MCP") so the user knows what else must be in place.

## Step 5 — Other (advanced, don't prompt on first run)

Leave these at their defaults unless the user explicitly asks to change them:

- `report.async_title` — defaults to `Weekly Async Report - {team}`. Only set it
  to override that title.
- `paths:`, `agent:`, `agent.dashboards` — only touch when relocating sections.

## Step 6 — Write

Apply changes by **editing values in place** in `.agents/config.yaml` (preserve
its comments and structure). Only add a new `{provider}:` block when enabling a
provider that has none yet. Show a concise summary of what changed before saving.

## Step 7 — Personal intro (CONFIG.md, optional)

Offer to fill in `CONFIG.md` ("Who I am", current focus, working style) — free-form
prose that complements the structured `config.yaml`. Keep it short; skipping is
fine.

## Step 8 — Report & where to change things

Summarize what was set, which capabilities are active vs `none`, and any MCP/CLI
prerequisites still needed. Then tell the user **where to change any of this
later**:

- Structured settings → `.agents/config.yaml` (or just re-run this skill).
- Personal prose → `CONFIG.md`.
- Naming/tagging conventions → `.agents/conventions.md`.

Suggest `/rebuild` only if paths changed.
