---
name: configure
description: Interactively set up or update your emOS configuration — owner, team, people, which tools you use (issue tracker, wiki, chat, docs), and their coordinates. Use for first-time setup or to change settings later. Nobody should hand-edit YAML; run this instead. No args (or pass a section name like "tools" or "people" to jump straight to it).
---

Walk the user through configuring emOS. You edit `.agents/config.yaml` (and
optionally `CONFIG.md`) on their behalf so they never hand-edit YAML.

Never ask for or store secrets (passwords, API tokens). emOS stores only links
and coordinates; authentication is handled by the MCP servers / CLIs themselves.

## Step 0 — Determine state

- If `.agents/config.yaml` does **not** exist, this is first-time setup: copy
  `.agents/config.example.yaml` to `.agents/config.yaml` as the starting point,
  then fill it in through the steps below.
- If it exists, this is an edit: read current values and offer each as the
  default so the user can press through unchanged. If args names a section
  (`owner`, `context`, `people`, `tools`, `integrations`, `report`), jump to it.

## Step 1 — Identity & context

Prompt (showing current values as defaults):
- **Owner**: `name`, `slug` (lowercase, matches their profile filename).
- **Context**: `team`, `tribe` (dept/org unit — optional), `company`, `current_quarter`.

## Step 2 — People map

Ask whether to add/edit teammates. For each: `@FirstName` → `slug`. These resolve
`@Mentions` in prose to `02-people/profiles/{slug}.md`. Offer to skip and add later.

## Step 3 — Tools (capabilities)

For each capability, ask which provider they use, or `none`:

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

## Step 4 — Provider coordinates

For each capability **not** set to `none`, prompt for that provider's config
block. Read the provider's adapter at `.agents/integrations/{provider}.md` to see
exactly which keys it needs and set only those. For the shipped providers:

- **jira** → `jira.project_key`, `jira.cloud_id`, `jira.custom_fields.*`; `external.jira` base URL.
- **confluence** → `confluence.cloud_id`, `confluence.space_key`, `confluence.root_page_id`, `confluence.root_title`, `confluence.parents.*`; `external.confluence`.
- **slack** → `slack.workspace_url`, `slack.channels.*`; `external.slack`.
- **gws** → `external.gdrive` (auth is via the `gws` CLI; no keys here).

After setting a provider, note its prerequisite from the adapter (e.g. "connect
the Atlassian MCP") so the user knows what else must be in place.

## Step 5 — Other

- `report.async_title` (used by manager-report).
- Leave `paths:`, `agent:`, and `agent.dashboards` at their defaults unless the
  user explicitly wants to relocate sections (advanced).

## Step 6 — Write

Apply changes by **editing values in place** in `.agents/config.yaml` (preserve
its comments and structure). Only add a new `{provider}:` block when enabling a
provider that has none yet. Show the user a concise summary of what changed
before saving, and confirm.

## Step 7 — Personal intro (CONFIG.md)

If `CONFIG.md` does not exist, offer to create it from `CONFIG.example.md` and
prompt for the "Who I am" fields. `CONFIG.md` is free-form prose (current focus,
working style) that complements the structured `config.yaml` — keep it short.

## Step 8 — Report

Summarize: what was set, which capabilities are active vs `none`, any MCP/CLI
prerequisites still needed, and suggest `/rebuild` only if paths changed.
