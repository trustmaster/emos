# Slack integration adapter

**Capability:** `chat`
**Provider key:** `slack`  ← value for `config.yaml` → `tools.chat`
**Status:** `shipped`

## Prerequisites

- Slack MCP connected.
- Access to the channels/threads being captured.

## Config

Reads `.agents/config.yaml` → `slack:` block:

| Key | Meaning |
|-----|---------|
| `workspace_url` | Base workspace URL (for archive links). |
| `channels.*` | Named channel shortcuts (e.g. `incidents`, `team`). |

Link base URL: `external.slack`.

## Operations

| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `capture_thread` | skill: `slack-capture` | Resolve a URL or search → fetch parent + replies → classify (`decision`/`action-items`/`discussion`) → `00-inbox/slack-YYYY-MM-DD-{slug}.md`. |

## Notes

- Omit sensitive personal information; keep thread quotes faithful to the original.
- Captured notes support the `projects: [slug]` join key so they surface in the
  linked project's hub on the next `project-sync`.
