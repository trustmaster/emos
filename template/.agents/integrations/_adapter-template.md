# {Provider Name} integration adapter

<!--
Copy this file to {provider-key}.md and fill it in to add a new tool.
{provider-key} is the value users set in config.yaml → tools.{capability}.
Delete these HTML comments when done. See docs/integrations.md for the full guide.
-->

**Capability:** `{issue_tracker | wiki | chat | docs}`
**Provider key:** `{provider-key}`  ← value for `config.yaml` → `tools.{capability}`
**Status:** `example`  ← `shipped` (ships with emOS) · `community` · `example`

## Prerequisites

- {The MCP server or CLI that must be connected/installed for this provider.}
- {How to verify it's available; any auth/token step.}

## Config

Reads `.agents/config.yaml` → `{provider-key}:` block:

| Key | Meaning |
|-----|---------|
| `{key}` | {what it is} |

Link base URL: `external.{provider-key}` (used to render `[ID](url)` links).

## Operations

Map every operation in this capability's contract (see [README.md](README.md))
to the skill or inline mechanics that implement it. Leave unsupported operations
out and note the gap.

| Operation | Implemented by | Notes |
|-----------|----------------|-------|
| `{operation}` | skill: `{skill-name}` | {any provider-specific caveat} |

## Notes

- {Field mappings, ID quirks, rate limits, anything a workflow or future
  maintainer needs to know about this provider.}
