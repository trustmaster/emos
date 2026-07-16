# emOS integrations

This directory holds **provider adapters** — the seam that lets emOS talk to
external tools (issue trackers, wikis, chat, document suites) without wiring any
specific product into the core workflows.

## How it fits together

```
workflow skill  ──reads──▶  config.yaml → tools.{capability}   (which provider?)
                                    │
                                    ▼
                       .agents/integrations/{provider}.md       (this dir: how?)
                                    │  names the implementing skill(s)
                                    ▼
                       provider skill (e.g. create-jira-ticket)  (does the work)
```

A workflow never names a product. It asks config which provider fills a
**capability**, opens that provider's adapter here, and follows it. Swapping
tools is a config + adapter change, never a core-workflow edit.

## Capabilities and their operation contracts

Each capability defines a small set of **operations**. An adapter for a provider
must map every operation it supports to a skill (or inline mechanics).

| Capability | `tools` key | Operations | Shipped provider |
|------------|-------------|------------|------------------|
| Issue tracker | `issue_tracker` | `create_issue`, `sync_iteration` | `jira`, `github` |
| Code host | `code_host` | `review_pr`, `browse_code` | `github` |
| Wiki | `wiki` | `load_page` (import), `save_page` (publish) | `confluence` |
| Chat | `chat` | `capture_thread` | `slack` |
| Document suite | `docs` | `read_doc`, `write_doc`, `list_files` (+ calendar/mail via the bundle) | `gws` |

Operation semantics:

- **`create_issue`** — create a ticket/issue in the tracker from a title +
  structured description; return the URL and key.
- **`sync_iteration`** — pull the current sprint/cycle/iteration into an emOS
  report grouped by status.
- **`review_pr`** — fetch a pull/merge request and produce a first-line review
  pass (summary, flagged issues, architectural/dependency changes, escalations)
  for a human to act on. Never auto-posts to the code host.
- **`browse_code`** — read-only exploration of a remote repository (search, read
  a file at a ref, path history, PRs, blame) for investigation.
- **`load_page`** — fetch a wiki page by URL/ID into `00-inbox/` for triage.
- **`save_page`** — publish/update a local emOS file as a wiki page.
- **`capture_thread`** — capture a chat thread/message into `00-inbox/` as a
  classified note.
- **`read_doc` / `write_doc` / `list_files`** — document-suite file operations.

## Shipped adapters

| Provider | Capability | Prerequisite | Config block |
|----------|------------|--------------|--------------|
| [jira](jira.md) | issue_tracker | Atlassian MCP | `jira:` + `external.jira` |
| [github](github.md) | issue_tracker + code_host | `gh` CLI | `github:` + `external.github` |
| [confluence](confluence.md) | wiki | Atlassian MCP | `confluence:` + `external.confluence` |
| [slack](slack.md) | chat | Slack MCP | `slack:` + `external.slack` |
| [gws](gws.md) | docs | `gws` CLI | `external.gdrive` |

## Adding a new provider

You never edit the core workflows. See **[docs/integrations.md](../../docs/integrations.md)**
for the full walkthrough. In short:

1. Write a provider skill (e.g. `create-linear-issue`) — keep it product-named.
2. Copy [`_adapter-template.md`](_adapter-template.md) → `linear.md` and map the
   capability's operations to your skill(s).
3. Add a `linear:` config block with the provider's coordinates.
4. Flip `tools.issue_tracker: linear` in `config.yaml`.

The old provider's skill and adapter stay in place — nothing is overwritten.
