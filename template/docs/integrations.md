# Integrations: using and adding tools

emOS ships wired for Jira (issue tracker), Confluence (wiki), Slack (chat), and
Google Workspace (documents). None of that is baked into the workflows — each is
a swappable **provider** behind a **capability**. This guide explains the model
and how to add your own tool (Linear, Notion, Mattermost, MS Office, …).

## The model

```
config.yaml → tools.{capability}   picks a provider
        │
        ▼
.agents/integrations/{provider}.md  adapter: prerequisites, config, operations → skill
        │
        ▼
provider skill (e.g. create-jira-ticket)  does the work, reads its own config block
```

Five capabilities, each with a small operation contract (full list in
[`.agents/integrations/README.md`](../.agents/integrations/README.md)):

| Capability | `tools` key | Operations | Shipped provider |
|------------|-------------|------------|------------------|
| Issue tracker | `issue_tracker` | `create_issue`, `sync_iteration` | `jira`, `github` |
| Code host | `code_host` | `review_pr`, `browse_code` | `github` |
| Wiki | `wiki` | `load_page`, `save_page` | `confluence` |
| Chat | `chat` | `capture_thread` | `slack` |
| Document suite | `docs` | `read_doc`, `write_doc`, `list_files` | `gws` |

One provider may fill several capabilities — `github` fills both `issue_tracker`
(`create-github-issue`) and `code_host` (`pr-review` + `github-browse`) from a
single [`github.md`](../.agents/integrations/github.md) adapter, each section
gated independently by config (e.g. `issue_tracker: jira` + `code_host: github`).

A workflow never names a product — it resolves `config.tools.{capability}`, reads
that provider's adapter, and follows it. If a capability is set to `none`, the
dependent skills say so and stop instead of guessing.

## Turning a capability off

Don't use a wiki? Set it to `none`:

```yaml
tools:
  wiki: none
```

`confluence-load` / `confluence-save` will report that no wiki is configured. You
can leave the `confluence:` config block in place or delete it.

## A note on the Google Workspace (`gws-*`) skills

The `gws-*` skills (`gws-gmail`, `gws-drive`, `gws-sheets`, …) originate from the
[`gws` CLI](https://github.com/googleworkspace/cli)'s `gws generate-skills`
command, but the copies shipped with emOS are **hand-curated**, not raw generator
output. They've been trimmed to the handful of operations a vault actually uses,
stripped of generator boilerplate, and aligned with emOS conventions (house-style
frontmatter, the untrusted-content rule in `gws-shared`). For the full API surface
of any service, use the discovery commands each skill documents —
`gws <service> --help` and `gws schema <service>.<resource>.<method>`.

**Don't run `gws generate-skills` on top of them.** It regenerates the verbose,
un-curated versions and overwrites the curated ones. If you need an operation a
skill doesn't cover, reach for the discovery commands above, or add your own
helper skill beside them (e.g. `gws-gmail-send`) — the same way you'd add any
other skill. Being shipped framework files, they're updated by emOS on
`emos update`, and any local edit you make is preserved as a `.emos-new` sidecar
(see the main README, "Staying Up to Date").

## Adding a new tool — worked example: Linear

Say you use **Linear** instead of Jira. You add a skill and an adapter; you do
**not** rename `create-jira-ticket` or edit any core workflow.

**1. Write the provider skill.** Create `.agents/skills/create-linear-issue/SKILL.md`,
product-named like the Jira one. Give it frontmatter and the concrete mechanics
(which MCP tool to call, field mapping, how to return the URL/key). Start the
body with a binding line so its role is obvious:

```markdown
---
name: create-linear-issue
description: Create a Linear issue from a title + structured description. …
---

> **Provider skill** for the `issue_tracker` capability (`linear`) — the
> `create_issue` operation. Active when `config.yaml` → `tools.issue_tracker: linear`.
> Adapter: ../../integrations/linear.md

… step-by-step instructions using the Linear MCP …
```

See [authoring-skills.md](authoring-skills.md) for skill structure.

**2. Write the adapter.** Copy [`.agents/integrations/_adapter-template.md`](../.agents/integrations/_adapter-template.md)
to `.agents/integrations/linear.md` and fill it in:

```markdown
# Linear integration adapter
**Capability:** `issue_tracker`
**Provider key:** `linear`
**Status:** community

## Prerequisites
- Linear MCP connected.

## Config
Reads `.agents/config.yaml` → `linear:` — `team_id`, `api base`, …

## Operations
| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `create_issue`   | skill: `create-linear-issue` | |
| `sync_iteration` | skill: `linear-sync`         | Linear "cycles" ≈ sprints |
```

Implement only the operations you need; note any you skip.

**3. Add the config block.** In `.agents/config.yaml`:

```yaml
linear:
  team_id: "TEAM"
  # …whatever your skill/adapter reads
```

Add the browse URL under `external:` if you link to issues:
`external.linear: "https://linear.app/your-org/issue"`.

**4. Flip the capability.**

```yaml
tools:
  issue_tracker: linear
```

Done. Every workflow that creates or syncs issues now uses Linear. The Jira skill
and adapter stay on disk, unused, ready if you switch back — nothing was
overwritten.

## Where things live

| Thing | Location | Owner |
|-------|----------|-------|
| Capability → provider map | `.agents/config.yaml` → `tools:` | you |
| Provider config blocks | `.agents/config.yaml` → `{provider}:` | you |
| Provider adapters | `.agents/integrations/{provider}.md` | framework (shipped) / you (new) |
| Provider skills | `.agents/skills/{skill}/SKILL.md` | framework (shipped) / you (new) |
| Operation contracts | `.agents/integrations/README.md` | framework |

New adapters and skills you add are **yours** — the framework updater only
overwrites shipped paths, and it preserves any local edit to a shipped file as a
`.emos-new` sidecar (see the main README, "Staying Up to Date").
