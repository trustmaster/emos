# Confluence integration adapter

**Capability:** `wiki`
**Provider key:** `confluence`  ← value for `config.yaml` → `tools.wiki`
**Status:** `shipped`

## Prerequisites

- Atlassian MCP connected (tools prefixed `mcp__atlassian__`).
- Read/write access to the target space.

## Config

Reads `.agents/config.yaml` → `confluence:` block:

| Key | Meaning |
|-----|---------|
| `cloud_id` | Atlassian cloud UUID. |
| `space_key` | Target space key. |
| `root_page_id` | Page the vault's pages nest under. |
| `root_title` | Human title of the root page. |
| `parents.*` | Section titles under the root (e.g. `projects`, `meetings`). |

Link base URL: `external.confluence`.

## Operations

| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `load_page` | skill: `confluence-load` | Fetch by URL → `00-inbox/` with import frontmatter → classify + propose destination (does not move without confirmation). |
| `save_page` | skill: `confluence-save` | Publish/update a local file under the type-appropriate parent; writes `confluence_url:` back into the local frontmatter. |

## Notes

- Use `contentFormat: markdown` for create/update.
- Parent-page routing is by the local file's `type:` frontmatter → `parents.*`.
